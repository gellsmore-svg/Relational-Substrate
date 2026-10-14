"""Scalable GT observables for the E1 machinery.

``gte0a.analyse_item`` and ``gte0b.analyse_item`` measure a cell through the
reference ``build_kernel`` path, Python loops over states, a breadth-first
search per (state, probe), dictionary state lookups and dense linear
algebra. None of that reaches N=7. This module takes a ``gtkernel`` chain
and computes the same published channels with array operations, plus a
small set of separately labelled additions.

Status of each E0 channel (validation matrix: gravity-time/docs/e1-observables.md):

  reproduced exactly in definition, array form   occupancy, held/free observables,
      shell activity, reversibility, projected currents, event order (class-free
      and hub frame), class tables, Gibbs projection, trajectories
  reproduced by an iterative method with a declared tolerance
      stationary law (gather iteration), integrated autocorrelation times
      (lazy Poisson series)
  omitted above the dense limit, as in E0     generator spectrum
  not computed for reducible classes          recurrent class sizes beyond [size]

Additions (key ``e1_additions``) are new channels. They were checked on
synthetic fixtures and by identities against published channels; their
values on E0 cells are engineering checks, not findings.
"""

from __future__ import annotations

import itertools
import math
import time

import numpy as np

from rs_constraint_lab import gt0, gte0a, gte0b
from rs_constraint_lab.gte0a import PROBE, SOURCE, Chain
from rs_constraint_lab.state import edges

OBSERVABLES_VERSION = "gt-e1-observables/v1"
DENSE_LIMIT = gte0a.DENSE_LIMIT
STATIONARY_TOLERANCE = 1e-15
STATIONARY_RELATIVE_TOLERANCE = 1e-13
STATIONARY_RESIDUAL_TOLERANCE = 1e-12
STATIONARY_CAP = 2_000_000
POISSON_RELATIVE_TOLERANCE = 1e-13
POISSON_CAP = 2_000_000
CROSS_CHECK_TOLERANCE = 1e-10
UNREACHED = -1


# --- class structure -----------------------------------------------------


def start_index(chain: Chain, n: int, mode: str) -> int:
    position = np.searchsorted(chain.states, gt0.start_state(n, mode))
    if position >= len(chain.states) or chain.states[position] != gt0.start_state(n, mode):
        raise ValueError("the declared start is not in the chain")
    return int(position)


def class_regime(chain: Chain, start: int) -> dict:
    """Regime of a reachable class, the label ``gt0.class_structure`` would give.

    The class is closed (it is the reachable set of ``start``), so it is one
    recurrent class exactly when every state reaches ``start``. Toggles are
    involutions, so the predecessor of j through slot e is T[j, e], and that
    edge exists when W[T[j, e], e] > 0. A state with zero total rate is the
    only possible singleton recurrent class (toggles never self-loop), so
    "absorbing" and "mixed" are distinguished by R = 0 alone.
    """
    R = chain.rates
    absorbing = int((R <= 0).sum())
    seen = np.zeros(len(chain.states), dtype=bool)
    seen[start] = True
    frontier = np.array([start])
    while frontier.size:
        pred = chain.T[frontier]
        ok = pred >= 0
        slot = np.broadcast_to(np.arange(chain.n_slots), pred.shape)[ok]
        cand = pred[ok]
        cand = cand[chain.W[cand, slot] > 0]
        fresh = np.unique(cand[~seen[cand]])
        seen[fresh] = True
        frontier = fresh
    irreducible = bool(seen.all())
    regime = "recurrent" if irreducible else ("absorbing" if absorbing else "mixed")
    return {
        "absorbing_state_count": absorbing,
        "irreducible": irreducible,
        "recurrent_class_sizes": [len(chain.states)] if irreducible else None,
        "regime": regime,
    }


# --- stationary law --------------------------------------------------------


def _incoming(chain: Chain, P: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Predecessor index and incoming jump probability for every (state, slot)."""
    valid = chain.T >= 0
    pred = np.where(valid, chain.T, 0)
    p_in = np.zeros_like(P)
    for e in range(chain.n_slots):
        p_in[:, e] = np.where(valid[:, e], P[pred[:, e], e], 0.0)
    return pred, p_in


def _push(pi: np.ndarray, pred: np.ndarray, p_in: np.ndarray) -> np.ndarray:
    """pi P for a toggle chain, by one gather per slot."""
    moved = np.zeros_like(pi)
    for e in range(pred.shape[1]):
        moved += pi[pred[:, e]] * p_in[:, e]
    return moved


def _lazy_power(pred, p_in, pi, tolerance, cap, relative_tolerance=STATIONARY_RELATIVE_TOLERANCE):
    """Lazy power iteration until the L1 change and the largest per-entry relative change are small.

    The L1 test alone stops while states of probability ~1e-12 still carry
    relative errors ~1e-7 (measured against an exact rational solve of HELD
    N5 PATHF weak_favour); every term of the iteration is non-negative, so
    continuing to a relative test reaches ~1e-15 relative error on every entry.
    """
    deltas = []
    iterations = 0
    relative = math.inf
    for iterations in range(1, cap + 1):
        nxt = 0.5 * (pi + _push(pi, pred, p_in))
        delta = float(np.abs(nxt - pi).sum())
        positive = nxt > 0
        relative = float((np.abs(nxt - pi)[positive] / nxt[positive]).max()) if positive.any() else math.inf
        pi = nxt
        deltas.append(delta)
        if delta < tolerance and relative < relative_tolerance:
            break
    return pi, iterations, deltas, relative


def _tail_estimate(deltas: list[float]) -> dict:
    """Geometric tail of the remaining L1 change, from the last decay ratios."""
    tail = deltas[-40:]
    if len(tail) < 10 or tail[-1] <= 0:
        return {"decay_ratio": None, "remaining_l1_estimate": None}
    ratios = [b / a for a, b in zip(tail[:-1], tail[1:]) if a > 0]
    ratio = float(np.exp(np.mean(np.log(np.clip(ratios, 1e-300, None)))))
    remaining = tail[-1] * ratio / (1.0 - ratio) if ratio < 1.0 else math.inf
    return {"decay_ratio": ratio, "remaining_l1_estimate": remaining}


def stationary(chain: Chain, start: int, *, method: str = "iterative", cross_check: bool = True, tolerance: float = STATIONARY_TOLERANCE, cap: int = STATIONARY_CAP) -> dict:
    """Jump-chain stationary law (G0/E0 convention), then pi_ct = pi_jump / R.

    ``method="iterative"``: lazy power iteration by gathers, from the uniform
    law. With ``cross_check`` a second run starts from the point mass on the
    declared start, and the L1 distance between the two limits is reported.
    ``method="auto"`` uses the E0 dense solve up to the dense limit.
    """
    R = chain.rates
    if (R <= 0).any():
        return {"resolved": False, "reason": "zero total rate in the class"}
    if method == "auto" and len(R) <= DENSE_LIMIT:
        ref = gte0a.stationary(chain)
        ref["cross_check_l1"] = None
        return ref
    P = chain.W / R[:, None]
    pred, p_in = _incoming(chain, P)
    size = len(R)
    started = time.perf_counter()
    pi, iterations, deltas, relative = _lazy_power(pred, p_in, np.full(size, 1.0 / size), tolerance, cap)
    out = {"iterations": iterations, "last_max_relative_change": relative, "method": "lazy_iteration_gather", **_tail_estimate(deltas)}
    if cross_check:
        point = np.zeros(size)
        point[start] = 1.0
        other, other_iterations, _, _ = _lazy_power(pred, p_in, point, tolerance, cap)
        out["cross_check_iterations"] = other_iterations
        out["cross_check_l1"] = float(np.abs(other - pi).sum())
        positive = pi > 0
        out["cross_check_max_relative"] = float((np.abs(other - pi)[positive] / pi[positive]).max())
    else:
        out["cross_check_l1"] = None
    residual = float(np.abs(_push(pi, pred, p_in) - pi).sum())
    out["residual"] = residual
    out["seconds"] = time.perf_counter() - started
    failed = []
    if residual > STATIONARY_RESIDUAL_TOLERANCE or (pi < -1e-15).any():
        failed.append("residual above tolerance")
    if iterations >= cap:
        failed.append("iteration cap reached")
    if out["cross_check_l1"] is not None and out["cross_check_l1"] > CROSS_CHECK_TOLERANCE:
        failed.append("two starts disagree")
    if failed:
        out.update({"reason": "; ".join(failed), "resolved": False})
        return out
    pi = np.clip(pi, 0.0, None)
    pi /= pi.sum()
    ct = pi / R
    ct /= ct.sum()
    out.update({"ct": ct, "jump": pi, "mean_rate_ct": float(ct @ R), "resolved": True})
    return out


# --- distances and structure -------------------------------------------------


def source_distances(states: np.ndarray, n: int) -> np.ndarray:
    """Graph distance from the source set to every vertex, per state (int8; -1 = unreached).

    Multi-source breadth-first search on neighbour bitmasks, all states at
    once. The distance of a probe to the nearest source vertex equals
    ``gt0.distance_to_source``; source vertices are at 0.
    """
    edge_list = edges(n)
    adj = [np.zeros(len(states), dtype=np.int64) for _ in range(n)]
    for e, (a, b) in enumerate(edge_list):
        bit = (states >> e) & 1
        adj[a] |= bit << b
        adj[b] |= bit << a
    src = gt0.source()
    source_mask = sum(1 << v for v in src)
    D = np.full((len(states), n), UNREACHED, dtype=np.int8)
    D[:, list(src)] = 0
    reached = np.full(len(states), source_mask, dtype=np.int64)
    frontier = reached.copy()
    level = 0
    while frontier.any():
        level += 1
        nxt = np.zeros(len(states), dtype=np.int64)
        for v in range(n):
            nxt |= np.where((frontier >> v) & 1 == 1, adj[v], 0)
        nxt &= ~reached
        for v in range(n):
            D[((nxt >> v) & 1) == 1, v] = level
        reached |= nxt
        frontier = nxt
    return D


def _shell_key(d: int) -> str:
    return "inf" if d < 0 else str(int(d))


def held_observables(chain: Chain, law: np.ndarray, n: int, D: np.ndarray, *, per_unit_time: bool = False) -> dict:
    """``gt0.held_observables`` on arrays: same keys, definitions and clock conventions."""
    edge_list = edges(n)
    probes = [p for p in range(n) if p not in gt0.source()]
    attach_slots = gt0.attach_slot_indices(n)
    free_slots = gt0.free_slot_indices(n)
    bits = (chain.states[:, None] >> np.arange(chain.n_slots)) & 1
    attach = bits[:, attach_slots].sum(axis=1)
    free = bits[:, free_slots].sum(axis=1)
    R = chain.rates
    rate = chain.W if per_unit_time else chain.W / R[:, None]
    valid = (chain.T >= 0) & (chain.W > 0)
    target = np.where(valid, chain.T, 0)
    ks = np.unique(free)
    by_k_mass = {int(k): float(law[free == k].sum()) for k in ks}
    by_k_attach = {int(k): float((law * attach)[free == k].sum()) for k in ks}
    dist_mass: dict[str, float] = {}
    drift_num: dict[str, float] = {}
    drift_den: dict[str, float] = {}
    escape_num: dict[str, float] = {}
    capture_num = 0.0
    capture_den = 0.0
    for p in probes:
        d = D[:, p].astype(np.int64)
        dt = np.where(valid, D[target, p].astype(np.int64), UNREACHED)
        finite = d >= 0
        change = (np.where(valid & (dt >= 0), rate * (dt - d[:, None]), 0.0)).sum(axis=1)
        escape = np.where(valid & (dt < 0), rate, 0.0).sum(axis=1)
        enter = np.where(valid & (dt >= 0), rate, 0.0).sum(axis=1)
        for shell in np.unique(d):
            key = _shell_key(int(shell))
            mask = d == shell
            dist_mass[key] = dist_mass.get(key, 0.0) + float(law[mask].sum()) / len(probes)
            if shell >= 0:
                drift_num[key] = drift_num.get(key, 0.0) + float((law * change)[mask].sum())
                escape_num[key] = escape_num.get(key, 0.0) + float((law * escape)[mask].sum())
                drift_den[key] = drift_den.get(key, 0.0) + float(law[mask].sum())
        capture_num += float((law * enter)[~finite].sum())
        capture_den += float(law[~finite].sum())
    drift = {k: drift_num[k] / drift_den[k] for k in sorted(drift_den) if drift_den[k] > 0}
    escape_out = {k: escape_num[k] / drift_den[k] for k in sorted(drift_den) if drift_den[k] > 0}
    exp_attach = float(law @ attach)
    exp_free = float(law @ free)
    return {
        "attachment_fraction": exp_attach / exp_free if exp_free > 0 else None,
        "attachment_fraction_by_free_edge_count": {str(k): (by_k_attach[k] / (by_k_mass[k] * k) if k > 0 and by_k_mass[k] > 0 else None) for k in sorted(by_k_mass)},
        "attachment_slots": len(attach_slots),
        "distance_distribution": dict(sorted(dist_mass.items())),
        "expected_free_edges": exp_free,
        "free_edge_count_distribution": {str(k): by_k_mass[k] for k in sorted(by_k_mass)},
        "free_slots": len(free_slots),
        "null_attachment_fraction": len(attach_slots) / len(free_slots),
        "capture_rate_when_detached": capture_num / capture_den if capture_den > 0 else None,
        "clock": "continuous_per_unit_time" if per_unit_time else "jump_per_event",
        "escape_rate_to_detached": escape_out,
        "radial_drift_among_finite_moves": drift,
    }


def shell_activity(chain: Chain, ct: np.ndarray, jump: np.ndarray, n: int, D: np.ndarray) -> dict:
    """``gte0a.shell_activity`` on arrays: activity A(d) of probe-incident slots by shell, both clocks."""
    edge_list = edges(n)
    probes = [p for p in range(n) if p not in gt0.source()]
    R = chain.rates
    out = {}
    for clock, law in (("jump", jump), ("continuous", ct)):
        num: dict[str, float] = {}
        mass: dict[str, float] = {}
        for p in probes:
            incident = [i for i, (a, b) in enumerate(edge_list) if p in (a, b)]
            local = chain.W[:, incident].sum(axis=1)
            activity = local / R if clock == "jump" else local
            d = D[:, p]
            for shell in np.unique(d):
                key = _shell_key(int(shell))
                mask = d == shell
                num[key] = num.get(key, 0.0) + float((law * activity)[mask].sum())
                mass[key] = mass.get(key, 0.0) + float(law[mask].sum())
        activity = {k: num[k] / mass[k] for k in sorted(mass) if mass[k] > 1e-12}
        rho = activity["1"] / activity["2"] if "1" in activity and "2" in activity and activity["2"] > 0 else None
        out[clock] = {"near_far_ratio": rho, "shell_activity": activity, "shell_mass": {k: float(mass[k]) for k in sorted(mass)}}
    return out


def free_observables(chain: Chain, law: np.ndarray, arrays: dict) -> dict:
    """``gt0.free_observables`` on arrays."""
    k_all = arrays["edges"]
    ks = np.unique(k_all)
    mass = {int(k): float(law[k_all == k].sum()) for k in ks}
    tri = {int(k): float((law * arrays["triangles"])[k_all == k].sum()) for k in ks}
    return {
        "edge_count_distribution": {str(k): mass[k] for k in sorted(mass)},
        "expected_edges": sum(k * m for k, m in mass.items()),
        "expected_triangles": sum(tri.values()),
        "triangles_given_edge_count": {str(k): (tri[k] / mass[k] if mass[k] > 0 else None) for k in sorted(mass)},
    }


def structure_arrays(chain: Chain, n: int) -> dict:
    """``gte0a.structure_arrays`` with narrower integer types (same values)."""
    edge_list = edges(n)
    bits = ((chain.states[:, None] >> np.arange(chain.n_slots)) & 1).astype(np.int8)
    degree = np.zeros((len(chain.states), n), dtype=np.int64)
    for e, (a, b) in enumerate(edge_list):
        degree[:, a] += bits[:, e]
        degree[:, b] += bits[:, e]
    position = {pair: i for i, pair in enumerate(edge_list)}
    tri = np.zeros(len(chain.states), dtype=np.int64)
    for a, b, c in itertools.combinations(range(n), 3):
        tri += bits[:, position[(a, b)]] & bits[:, position[(a, c)]] & bits[:, position[(b, c)]]
    return {"bits": bits, "degree": degree, "edges": bits.sum(axis=1, dtype=np.int64), "triangles": tri, "wedges": (degree * (degree - 1) // 2).sum(axis=1)}


# --- event order ---------------------------------------------------------------


def event_pattern_probabilities(chain: Chain, jump: np.ndarray, n: int, mode: str) -> dict[tuple, float]:
    """Stationary probability of every consecutive event pair (type, slot class, type, slot class, relation)."""
    edge_list = edges(n)
    P = chain.W / chain.rates[:, None]
    if mode == "HELD":
        klass = gt0.slot_classes(n)
    else:
        klass = ["X"] * len(edge_list)
    names = ("F", "D")
    probs: dict[tuple, float] = {}
    for e in range(chain.n_slots):
        ie = chain.T[:, e]
        ok_e = (ie >= 0) & (P[:, e] > 0)
        if not ok_e.any():
            continue
        first = jump * P[:, e]
        t1 = ((chain.states >> e) & 1).astype(np.int64)
        after = chain.states ^ (1 << e)
        safe = np.where(ok_e, ie, 0)
        for f in range(chain.n_slots):
            prob = np.where(ok_e, first * P[safe, f], 0.0)
            if not (prob > 0).any():
                continue
            rel = "same" if e == f else ("adjacent" if set(edge_list[e]) & set(edge_list[f]) else "disjoint")
            t2 = ((after >> f) & 1).astype(np.int64)
            sums = np.bincount(t1 * 2 + t2, weights=prob, minlength=4)
            for code in np.nonzero(sums > 0)[0]:
                a, b = divmod(int(code), 2)
                key = (names[a], klass[e], names[b], klass[f], rel)
                probs[key] = probs.get(key, 0.0) + float(sums[code])
    return probs


def event_order(chain: Chain, jump: np.ndarray, n: int, mode: str) -> dict:
    """``gte0a.event_order`` with integer type codes and one bincount per slot pair."""
    probs = event_pattern_probabilities(chain, jump, n, mode)
    flip = {"F": "D", "D": "F"}
    seen = set()
    asym = 0.0
    rows = []
    for key in sorted(probs):
        t1, c1, t2, c2, rel = key
        rev = (flip[t2], c2, flip[t1], c1, rel)
        pair = tuple(sorted([key, rev]))
        if pair in seen:
            continue
        seen.add(pair)
        diff = probs.get(key, 0.0) - probs.get(rev, 0.0)
        if key != rev:
            asym += abs(diff)
            rows.append({"forward": "".join(key[:4]) + ":" + rel, "forward_probability": probs.get(key, 0.0), "reverse": "".join(rev[:4]) + ":" + rel, "reverse_probability": probs.get(rev, 0.0)})
    rows.sort(key=lambda r: -abs(r["forward_probability"] - r["reverse_probability"]))
    reversal = sum(v for k, v in probs.items() if k[4] == "same")
    return {"immediate_reversal_probability": reversal, "pattern_asymmetry": asym, "top_asymmetric_patterns": rows[:6]}


# --- symmetry classes ------------------------------------------------------------

CHUNK_BITS = 8


def permutation_tables(n: int, perm: tuple[int, ...]) -> list[np.ndarray]:
    """Lookup tables mapping each 8-bit chunk of a state code to its permuted bits."""
    edge_list = edges(n)
    position = {pair: i for i, pair in enumerate(edge_list)}
    target = [position[tuple(sorted((perm[a], perm[b])))] for a, b in edge_list]
    tables = []
    for start in range(0, len(edge_list), CHUNK_BITS):
        width = min(CHUNK_BITS, len(edge_list) - start)
        values = np.arange(1 << width, dtype=np.int64)
        table = np.zeros(1 << width, dtype=np.int64)
        for j in range(width):
            table |= ((values >> j) & 1) << target[start + j]
        tables.append(table)
    return tables


def permute_codes(states: np.ndarray, tables: list[np.ndarray]) -> np.ndarray:
    out = np.zeros_like(states)
    for c, table in enumerate(tables):
        out |= table[(states >> (c * CHUNK_BITS)) & ((1 << CHUNK_BITS) - 1)]
    return out


def canonical_labels(states: np.ndarray, n: int, mode: str, ct: np.ndarray | None = None) -> tuple[np.ndarray, float | None]:
    """Minimum code over the mode's symmetry group, and the symmetry check of a law.

    Raises if the class is not closed under the group, as ``gte0a.class_table`` does.
    """
    canonical = states.copy()
    max_diff = 0.0 if ct is not None else None
    full_space = len(states) == 1 << len(edges(n)) and states[0] == 0 and states[-1] == len(states) - 1
    for perm in gte0a.group_permutations(n, mode):
        codes = permute_codes(states, permutation_tables(n, perm))
        canonical = np.minimum(canonical, codes)
        if full_space:
            position = codes  # every code is present and is its own index
        else:
            position = np.searchsorted(states, codes)
            position = np.minimum(position, len(states) - 1)
            if not np.array_equal(states[position], codes):
                raise gte0a.E0AError("the reachable class is not closed under the symmetry group")
        if ct is not None:
            max_diff = max(max_diff, float(np.abs(ct[position] - ct).max()))
    return canonical, max_diff


def class_table(chain: Chain, ct: np.ndarray, jump: np.ndarray, n: int, mode: str, arrays: dict) -> tuple[list[dict], float]:
    """``gte0a.class_table`` with table-driven permutations and grouped sums."""
    canonical, max_diff = canonical_labels(chain.states, n, mode, ct)
    keys, first, inverse = np.unique(canonical, return_index=True, return_inverse=True)
    ct_sum = np.bincount(inverse, weights=ct, minlength=len(keys))
    jump_sum = np.bincount(inverse, weights=jump, minlength=len(keys))
    orbit = np.bincount(inverse, minlength=len(keys))
    rows = []
    for j, code in enumerate(keys):
        i = first[j]
        rows.append({"canonical_state": int(code), "ct": float(ct_sum[j]), "degree_sequence": sorted(arrays["degree"][i].tolist(), reverse=True), "edges": int(arrays["edges"][i]), "jump": float(jump_sum[j]), "orbit_size": int(orbit[j]), "triangles": int(arrays["triangles"][i])})
    rows.sort(key=lambda r: (r["edges"], r["canonical_state"]))
    return rows, max_diff


# --- autocorrelation ---------------------------------------------------------------


def autocorrelation_times(chain: Chain, ct: np.ndarray, jump: np.ndarray, mean_rate: float, functions: dict[str, np.ndarray], *, relative_tolerance: float = POISSON_RELATIVE_TOLERANCE, cap: int = POISSON_CAP) -> dict:
    """Integrated autocorrelation time of each function by a lazy Poisson series.

    E0 solves (-G + 1 pi) x = f~ densely. For pi-centred f~ the solution
    satisfies -G x = f~, i.e. (I - P) x = f~ / R with P the jump chain. The
    jump chain of a toggle chain has period 2, so the series uses the lazy
    chain: (I - P_L) = (I - P) / 2, so x = (1/2) sum_k P_L^k g with g = f~ / R, each term re-centred under
    pi_jump. tau = pi_ct . (f~ x) / var, unchanged by constants added to x.
    The series stops when the largest term is below ``relative_tolerance``
    times the largest partial sum; the geometric tail estimate is reported.
    """
    R = chain.rates
    P = chain.W / R[:, None]
    valid = chain.T >= 0
    target = np.where(valid, chain.T, 0)
    names = list(functions)
    centred = np.stack([functions[k] - ct @ functions[k] for k in names], axis=1)
    variance = ct @ centred**2
    # Function-major layout (functions x states): each slot's gather is contiguous and reuses one buffer.
    p_out = np.ascontiguousarray(np.where(valid, P, 0.0).T)
    target_t = np.ascontiguousarray(target.T)
    term = np.ascontiguousarray((centred / R[:, None]).T)
    term -= (term @ jump)[:, None]
    total = np.zeros_like(term)
    moved = np.empty_like(term)
    buffer = np.empty_like(term)
    iterations = 0
    norms: list[float] = []
    for iterations in range(1, cap + 1):
        total += term
        moved.fill(0.0)
        for e in range(chain.n_slots):
            np.take(term, target_t[e], axis=1, out=buffer)
            buffer *= p_out[e]
            moved += buffer
        term += moved
        term *= 0.5
        term -= (term @ jump)[:, None]
        norm = float(np.abs(term).max())
        norms.append(norm)
        if norm <= relative_tolerance * float(np.abs(total).max()):
            break
    x = 0.5 * total.T
    tail = _tail_estimate(norms)
    out: dict = {}
    for j, name in enumerate(names):
        var = float(variance[j])
        if var < 1e-14:
            out[name] = None
            continue
        tau = float(ct @ (centred[:, j] * x[:, j])) / var
        out[name] = {"events": tau * mean_rate, "time": tau, "variance": var}
    diagnostics = {"iterations": iterations, "cap_reached": iterations >= cap, "decay_ratio": tail["decay_ratio"], "last_relative_term": norms[-1] / max(float(np.abs(total).max()), 1e-300) if norms else None}
    return {"taus": out, "diagnostics": diagnostics}


# --- additions ------------------------------------------------------------------------


def witness_census(chain: Chain, jump: np.ndarray, n: int, components: list[tuple[str, str]], factors: dict | None = None) -> dict:
    """Witness counts actually engaged by each component, per executed event (jump law).

    For a component, an executed event is one on a slot it acts on (absent
    slot for a form component, present slot for a dissolve component). The
    distribution of its witness count w over executed events, and the mean
    log-weight w log(m), show how strongly the rule is engaged at a given N.
    """
    from rs_constraint_lab import gtkernel

    table = gte0a.FACTORS if factors is None else factors
    P = chain.W / chain.rates[:, None]
    present = ((chain.states[:, None] >> np.arange(chain.n_slots)) & 1).astype(bool)
    out = {}
    for kind, grade in components:
        counts = gtkernel.witness_counts(chain.states, n, kind)
        acts = ~present if kind.endswith("_form") else present
        mass = (jump[:, None] * P) * acts
        total = float(mass.sum())
        dist = np.bincount(counts.ravel(), weights=mass.ravel())
        factor = float(table[grade])
        mean_w = float((np.arange(len(dist)) * dist).sum() / total) if total > 0 else None
        out[f"{kind}:{grade}"] = {
            "event_share": total,
            "mean_log_weight": (mean_w * math.log(factor) if factor > 0 and mean_w is not None else None),
            "mean_witnesses": mean_w,
            "witness_distribution": {str(w): float(v / total) for w, v in enumerate(dist) if v > 0} if total > 0 else {},
        }
    return out


def hub_structure(degree: np.ndarray, law: np.ndarray, n: int, mode: str) -> dict:
    """Maximum degree, number of tied hubs, and (HELD) whether a hub is a source vertex."""
    top = degree.max(axis=1)
    tied = (degree == top[:, None]).sum(axis=1)
    out = {
        "max_degree_distribution": {str(int(k)): float(law[top == k].sum()) for k in np.unique(top)},
        "tied_hub_count_distribution": {str(int(k)): float(law[tied == k].sum()) for k in np.unique(tied)},
    }
    if mode == "HELD":
        hubs = degree == top[:, None]
        source_hub = hubs[:, list(gt0.source())].any(axis=1)
        probe_hub = hubs[:, [v for v in range(n) if v not in gt0.source()]].any(axis=1)
        out["hub_includes_source"] = float(law[source_hub].sum())
        out["hub_includes_probe"] = float(law[probe_hub].sum())
        out["hub_probe_only"] = float(law[probe_hub & ~source_hub].sum())
    return out


def held_additions(chain: Chain, ct: np.ndarray, jump: np.ndarray, n: int, D: np.ndarray, arrays: dict) -> dict:
    """Detachment counts and a density-standardised attachment margin.

    ``attachment_margin`` is attachment_fraction - slot ratio r0 =
    (E[a] - r0 E[k]) / E[k]. Under any law uniform within each free-edge
    count k, E[a | k] = r0 k, so the margin is the excess over the
    combinatorial expectation at the realised densities. The standardised
    version reweights E[a | k] to the NULL law's distribution of k
    (binomial over free slots), so cells with different densities are
    compared at one reference density profile.
    """
    edge_list = edges(n)
    probes = [p for p in range(n) if p not in gt0.source()]
    attach_slots = gt0.attach_slot_indices(n)
    free_slots = gt0.free_slot_indices(n)
    bits = arrays["bits"]
    attach = bits[:, attach_slots].sum(axis=1, dtype=np.int64)
    free = bits[:, free_slots].sum(axis=1, dtype=np.int64)
    r0 = len(attach_slots) / len(free_slots)
    detached = (D[:, probes] < 0).sum(axis=1)
    out: dict = {}
    for clock, law in (("continuous", ct), ("jump", jump)):
        ea, ek = float(law @ attach), float(law @ free)
        cond = {}
        for k in np.unique(free):
            m = float(law[free == k].sum())
            if k > 0 and m > 1e-300:
                cond[int(k)] = float((law * attach)[free == k].sum()) / m
        weights = {k: math.comb(len(free_slots), k) / 2 ** len(free_slots) for k in cond}
        num = sum(weights[k] * cond[k] for k in cond)
        den = sum(weights[k] * k for k in cond)
        out[clock] = {
            "attachment_margin": (ea / ek - r0) if ek > 0 else None,
            "attachment_margin_null_density_standardised": (num / den - r0) if den > 0 else None,
            "detached_probe_count_distribution": {str(int(c)): float(law[detached == c].sum()) for c in np.unique(detached)},
            "probe_count": len(probes),
        }
    return out


# --- trajectories ---------------------------------------------------------------------


def trajectory_summary(chain: Chain, path: dict, arrays: dict, start: int) -> dict:
    """``gte0a.trajectory_summary`` with sorted-array state lookup."""
    codes = np.array([path["start_state"]] + [0] * len(path["events"]), dtype=np.int64)
    state = path["start_state"]
    for j, (e, _bit, _t) in enumerate(path["events"], start=1):
        state ^= 1 << e
        codes[j] = state
    idx = np.searchsorted(chain.states, codes)
    edge_series = [int(v) for v in arrays["edges"][idx]]
    times = [0.0] + [t for _e, _b, t in path["events"]]
    durations = [b - a for a, b in zip(times[:-1], times[1:])]
    last = times[-1]
    time_avg = float(np.dot(edge_series[:-1], durations) / last) if last > 0 else float(edge_series[0])
    return {"distinct_states": len(set(idx.tolist())), "event_mean_edges": float(np.mean(edge_series)), "final_state": int(codes[-1]), "max_edges": max(edge_series), "min_edges": min(edge_series), "time_mean_edges": time_avg, "total_time": last}


# --- one cell ----------------------------------------------------------------------------


def analyse(
    chain: Chain,
    *,
    family: str,
    grade: str,
    n: int,
    mode: str,
    families: dict,
    factors: dict | None = None,
    item_id: str | None = None,
    round_id: str | None = None,
    with_trajectories: bool = True,
    with_autocorrelation: bool = True,
    hub_frame: bool = True,
    stationary_method: str = "iterative",
    cross_check: bool = True,
    stationary_override: dict | None = None,
    start: int | None = None,
) -> tuple[dict, dict | None]:
    """All E0A/E0B channels of one cell, plus ``e1_additions`` and solver diagnostics.

    ``rule_instances`` and ``predicted_potential`` come from the template
    definitions (no kernel build). The spectrum is omitted above the dense
    limit, as in E0.
    """
    timings: dict[str, float] = {}
    components = families[family][grade]
    start = start_index(chain, n, mode) if start is None else start
    regime = class_regime(chain, start)
    out: dict = {
        "family": family,
        "gradient_family": gte0a.is_gradient(family, families),
        "grade": grade,
        "mode": mode,
        "n": n,
        "reachable_states": len(chain.states),
        "recurrent_class_sizes": regime["recurrent_class_sizes"],
        "absorbing_state_count": regime["absorbing_state_count"],
        "rule_instances": sum(len(gte0a.component_expressions(kind, n, g)) for kind, g in components) + len(gt0.scaffold_expressions(mode)),
        "observables_version": OBSERVABLES_VERSION,
    }
    if regime["regime"] != "recurrent":
        out["regime"] = regime["regime"]
        out["timings"] = timings
        return out, None
    out["regime"] = "recurrent"
    t0 = time.perf_counter()
    stat = stationary_override if stationary_override is not None else stationary(chain, start, method=stationary_method, cross_check=cross_check)
    timings["stationary"] = time.perf_counter() - t0
    out["stationary"] = {k: v for k, v in stat.items() if k not in ("ct", "jump")}
    if not stat["resolved"]:
        out["timings"] = timings
        return out, None
    ct, jump, mean_rate = stat["ct"], stat["jump"], stat["mean_rate_ct"]
    arrays = structure_arrays(chain, n)
    t0 = time.perf_counter()
    out["reversibility"] = gte0a.reversibility(chain, ct, mean_rate)
    timings["reversibility"] = time.perf_counter() - t0
    t0 = time.perf_counter()
    out["event_order"] = event_order(chain, jump, n, mode)
    timings["event_order"] = time.perf_counter() - t0
    edge_list = edges(n)
    if mode == "HELD":
        attach_slots = gt0.attach_slot_indices(n)
        free_slots = gt0.free_slot_indices(n)
        free_edges = arrays["bits"][:, free_slots].sum(axis=1, dtype=np.int64)
        attachments = arrays["bits"][:, attach_slots].sum(axis=1, dtype=np.int64)
        width = int(attachments.max()) + 1
        bins = free_edges * width + attachments
        labels = [f"k{k}a{a}" for k in range(int(free_edges.max()) + 1) for a in range(width)]
        out["projected_current"] = gte0a.projected_current(chain, ct, bins, labels)
        out["projected_current"]["projection"] = "(free-edge count, attachment count)"
    else:
        width = int(arrays["triangles"].max()) + 1
        bins = arrays["edges"] * width + arrays["triangles"]
        labels = [f"k{k}t{t}" for k in range(int(arrays["edges"].max()) + 1) for t in range(width)]
        out["projected_current"] = gte0a.projected_current(chain, ct, bins, labels)
        out["projected_current"]["projection"] = "(edge count, triangle count)"
    out["mean_rate_ct"] = mean_rate
    t0 = time.perf_counter()
    table, sym = class_table(chain, ct, jump, n, mode, arrays)
    timings["classes"] = time.perf_counter() - t0
    out["class_table"] = table
    out["symmetry_max_abs_difference"] = sym
    t0 = time.perf_counter()
    out["gibbs_projection"] = gte0a.gibbs_projection(ct, arrays)
    timings["gibbs_projection"] = time.perf_counter() - t0
    potential = gte0a.predicted_potential(family, grade, families) if factors is None else None
    out["predicted_potential"] = potential
    out["predicted_law_l1_gap"] = gte0a.predicted_law_gap(ct, arrays, potential) if potential is not None else None
    deg = arrays["degree"]
    occupancy = {
        "edge_count_distribution": {str(k): float(ct[arrays["edges"] == k].sum()) for k in range(int(arrays["edges"].min()), int(arrays["edges"].max()) + 1)},
        "expected_degree_variance": float(ct @ deg.var(axis=1)),
        "expected_edges": float(ct @ arrays["edges"]),
        "expected_max_degree": float(ct @ deg.max(axis=1)),
        "expected_triangles": float(ct @ arrays["triangles"]),
        "expected_wedges": float(ct @ arrays["wedges"]),
        "full_centre_probability": float(ct[(deg == n - 1).any(axis=1)].sum()),
    }
    dist = occupancy["edge_count_distribution"]
    keys = sorted(dist, key=int)
    values = [dist[k] for k in keys]
    occupancy["edge_count_modes"] = [int(keys[j]) for j in range(len(keys)) if values[j] > 1e-12 and (j == 0 or values[j] > values[j - 1]) and (j == len(keys) - 1 or values[j] > values[j + 1])]
    out["occupancy_ct"] = occupancy
    additions: dict = {"hub_structure_ct": hub_structure(deg, ct, n, mode), "witness_census_jump": witness_census(chain, jump, n, components, factors)}
    D = None
    if mode == "FREE":
        out["free_jump"] = free_observables(chain, jump, arrays)
        out["free_continuous"] = free_observables(chain, ct, arrays)
    else:
        t0 = time.perf_counter()
        D = source_distances(chain.states, n)
        out["held_jump"] = held_observables(chain, jump, n, D)
        out["held_continuous"] = held_observables(chain, ct, n, D, per_unit_time=True)
        out["shell_activity"] = shell_activity(chain, ct, jump, n, D)
        additions["held"] = held_additions(chain, ct, jump, n, D, arrays)
        timings["held"] = time.perf_counter() - t0
    out["spectrum"] = None
    out["spectrum_note"] = "generator spectrum not computed by gtobs (dense; omitted above the E0 dense limit, and not reproduced below it)"
    if with_autocorrelation:
        t0 = time.perf_counter()
        hubs = deg == deg.max(axis=1, keepdims=True)
        if mode == "FREE":
            functions = {"centre_indicator_v0": (deg[:, 0] == n - 1).astype(float), "degree_v0": deg[:, 0].astype(float), "edges": arrays["edges"].astype(float), "triangles": arrays["triangles"].astype(float)}
            extra = {"hub_indicator_v0": hubs[:, 0].astype(float)}
            ratio_keys = ("degree_v0", "edges")
        else:
            dist_probe = D[:, PROBE]
            functions = {
                "attached_probe": (dist_probe == 1).astype(float),
                "degree_probe": deg[:, PROBE].astype(float),
                "detached_probe": (dist_probe < 0).astype(float),
                "free_edges": free_edges.astype(float),
                "triangles": arrays["triangles"].astype(float),
            }
            extra = {"hub_indicator_probe": hubs[:, PROBE].astype(float)}
            ratio_keys = ("degree_probe", "free_edges")
        solved = autocorrelation_times(chain, ct, jump, mean_rate, {**functions, **extra})
        taus = solved["taus"]
        out["autocorrelation"] = {k: taus[k] for k in functions}
        additions["autocorrelation_extra"] = {k: taus[k] for k in extra}
        out["autocorrelation_diagnostics"] = solved["diagnostics"]
        local, global_ = taus.get(ratio_keys[0]), taus.get(ratio_keys[1])
        out["localisation_persistence_index"] = local["time"] / global_["time"] if local and global_ else None
        timings["autocorrelation"] = time.perf_counter() - t0
    else:
        out["autocorrelation"] = None
        out["localisation_persistence_index"] = None
    if hub_frame:
        t0 = time.perf_counter()
        classes = gte0b.hub_classes(chain, n)
        frame = gte0b.event_order_frame(chain, jump, n, classes)
        hb = arrays["edges"] * n + deg.max(axis=1)
        hl = [f"k{k}m{m}" for k in range(int(arrays["edges"].max()) + 1) for m in range(n)]
        current = gte0a.projected_current(chain, ct, hb, hl)
        current["projection"] = "(edge count, maximum degree)"
        out["hub_frame"] = {"event_order": frame, "projected_current": current}
        timings["hub_frame"] = time.perf_counter() - t0
    out["e1_additions"] = additions
    trajectories = None
    if with_trajectories and item_id is not None and round_id is not None:
        t0 = time.perf_counter()
        paths = []
        for k in range(gte0a.TRAJECTORIES_PER_CELL):
            path = gte0a.sample_trajectory(chain, start, gte0a.trajectory_seed(item_id, k, round_id), gte0a.EVENTS_PER_TRAJECTORY)
            path["summary"] = trajectory_summary(chain, path, arrays, start)
            paths.append(path)
        trajectories = {"item_id": item_id, "label": "illustrative exact-kernel samples; no table statistic uses them", "numpy_version": np.__version__, "trajectories": paths}
        timings["trajectories"] = time.perf_counter() - t0
    out["timings"] = timings
    return out, trajectories
