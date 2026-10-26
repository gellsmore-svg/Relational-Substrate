"""Replacement-aware episode observables and the layer-traffic comparator NK (GT-P010, E5B).

Read-only functionals of a finite single-toggle chain (``gte0a.Chain``) and its
continuous-time stationary law. No rule reads an anchor, an entry set, a
participant or any quantity defined here: entry-set tracking is an analyst's
observer, solved as hitting problems on the killed jump chain, and never a
state read by the stochastic rules (the 8G compilation gate is not engaged).
Definitions and proofs: ``gravity-time/docs/e5b-definitions-controls-and-feasibility.md``.

* Anchor-local event count L_local(A) = sum_{x in A} pi(x) q_loc(x) / J_A.
* Entrance (Palm) weights mu_in(y) proportional to the stationary entering flux into y.
* Entry participants S0(y): the anchor's neighbours (F_STAR, F_2PATH) or the
  triangle completers of the anchor edge (F_TRI) immediately after entry.
* Distinct departures: P(a given entry participant is absent in some A-state before exit).
* Complete renewal: P(reach an A-state in which no entry participant participates,
  before exit), with its structural feasibility class.
* F_STAR maximal partial renewal: P(reach an A-state with N-4 entry participants absent).
* Flicker: probability that the event after an eligible turnover toggle reverses it
  (next event of the full process, and next anchor-local event).
* NK: the reversible exchangeable surrogate matching the target's CT edge-count
  profile and every adjacent-layer stationary flux.
"""

from __future__ import annotations

import itertools
import math

import numpy as np

from rs_constraint_lab import gtobs
from rs_constraint_lab import gtpersist as P
from rs_constraint_lab.gte0a import Chain
from rs_constraint_lab.state import edges

RENEW_VERSION = "gt-renew/v1"
FLEXIBLE = ("F_TRI", "F_STAR", "F_2PATH")
HIT_TOLERANCE = 1e-12
HIT_CAP = 20_000
HIT_SECONDS = 600.0
DENSE_LIMIT = 4096  # killed systems up to this size are also solved densely (independent route)


# --- predicate geometry ------------------------------------------------------


def anchor_vertices(predicate: str, vertices: tuple[int, ...]) -> tuple[int, ...]:
    """Vertices held fixed by the anchor: (c,) for the vertex predicates, (a, b) for F_TRI."""
    if predicate == "F_TRI":
        return tuple(vertices[:2])
    if predicate in ("F_STAR", "F_2PATH"):
        return (vertices[0],)
    raise ValueError(f"not a flexible predicate: {predicate}")


def candidates(n: int, predicate: str, vertices: tuple[int, ...]) -> list[int]:
    """Vertices that can ever participate."""
    anc = set(anchor_vertices(predicate, vertices))
    return [v for v in range(n) if v not in anc]


def local_mask(n: int, predicate: str, vertices: tuple[int, ...]) -> np.ndarray:
    """Slots incident on an anchor vertex (fixed by the predicate, never chosen from data)."""
    anc = set(anchor_vertices(predicate, vertices))
    return np.array([bool(anc & set(pair)) for pair in edges(n)])


def participation(states: np.ndarray, n: int, predicate: str, vertices: tuple[int, ...]) -> np.ndarray:
    """Boolean (states, n): vertex v currently participates (neighbour of c, or completer of ab)."""
    x = P.bits(states, n)
    out = np.zeros((len(states), n), dtype=bool)
    if predicate == "F_TRI":
        a, b = vertices[:2]
        for v in candidates(n, predicate, vertices):
            out[:, v] = x[:, P.slot(n, a, v)] & x[:, P.slot(n, b, v)]
    else:
        c = vertices[0]
        for v in candidates(n, predicate, vertices):
            out[:, v] = x[:, P.slot(n, c, v)]
    return out


def threshold(predicate: str) -> int:
    """Minimum number of simultaneous participants the predicate needs."""
    return {"F_TRI": 1, "F_STAR": 3, "F_2PATH": 2}[predicate]


def renewal_feasible(n: int, predicate: str, vertices: tuple[int, ...], s0_size: int) -> bool:
    """Complete renewal possible: enough candidates outside S0 to satisfy the predicate alone."""
    return len(candidates(n, predicate, vertices)) - s0_size >= threshold(predicate)


def max_partial_absent(n: int, predicate: str, vertices: tuple[int, ...], s0_size: int) -> int:
    """Largest number of entry participants that can be absent while the predicate still holds."""
    outside = len(candidates(n, predicate, vertices)) - s0_size
    return max(0, min(s0_size, s0_size + outside - threshold(predicate)))


# --- episodes: entrance, local clock, flicker ---------------------------------


def entrance_weights(chain: Chain, ct: np.ndarray, A: np.ndarray) -> np.ndarray:
    """Unnormalised stationary entering flux into each state (zero outside A); sums to J_A."""
    valid, target_in = P._boundary(chain, A)
    entering = valid & ~A[:, None] & target_in
    return np.bincount(chain.T[entering], weights=(ct[:, None] * chain.W)[entering], minlength=len(A))


def local_clock(chain: Chain, ct: np.ndarray, A: np.ndarray, local: np.ndarray) -> dict:
    """L_local and companions; all counts in the same jump trajectory (not a duration)."""
    J = float(entrance_weights(chain, ct, A).sum())
    q_loc = chain.W[:, local].sum(axis=1)
    R = chain.rates
    loc_mass = float(ct[A] @ q_loc[A])
    all_mass = float(ct[A] @ R[A])
    valid, target_in = P._boundary(chain, A)
    leaving = valid & A[:, None] & ~target_in
    exit_local = float((ct[:, None] * chain.W)[leaving & local[None, :]].sum())
    exit_all = float((ct[:, None] * chain.W)[leaving].sum())
    return {
        "lifetime_local": loc_mass / J,
        "lifetime_jump": all_mass / J,
        "local_share_of_events_in_A": loc_mass / all_mass,
        "local_hazard_mean_ct": loc_mass / float(ct[A].sum()),
        "exit_local_share": exit_local / exit_all,
        "entry_flux": J,
    }


def flicker(chain: Chain, ct: np.ndarray, A: np.ndarray, eligible: np.ndarray, local: np.ndarray) -> dict:
    """Immediate reversal after an eligible (participant-changing) internal toggle.

    next_event: probability that the next event of the full process toggles the same slot back;
    next_local_event: probability that the next anchor-local event does. Both exact.
    """
    valid, target_in = P._boundary(chain, A)
    internal = valid & A[:, None] & target_in & eligible
    flow = ct[:, None] * chain.W
    rows, cols = np.nonzero(internal)
    if len(rows) == 0:
        return {"eligible_flux": 0.0, "reversal_next_event": None, "reversal_next_local_event": None}
    w = flow[rows, cols]
    y = chain.T[rows, cols]
    back = chain.W[y, cols]
    q_y = chain.rates[y]
    ql_y = chain.W[y][:, local].sum(axis=1)
    J = float(entrance_weights(chain, ct, A).sum())
    return {
        "eligible_flux": float(w.sum()),
        "reversal_next_event": float((w * back / q_y).sum() / w.sum()),
        "reversal_next_local_event": float((w * back / ql_y).sum() / w.sum()),
        "reversals_next_event_per_episode": float((w * back / q_y).sum() / J),
    }


# --- hitting problems on the killed jump chain --------------------------------


def hit_before_exit(chain: Chain, A: np.ndarray, target: np.ndarray, *, cap: int = HIT_CAP, seconds: float = HIT_SECONDS, dense: bool | None = None) -> dict:
    """h(x) = P_x(hit target before leaving A), target a subset of A; jump chain (clock-free).

    Solves (I - P_BB) h_B = P_B,target 1 on B = A minus target. BiCGSTAB always; a dense
    direct solve as an independent route when |B| <= DENSE_LIMIT (or dense=True).
    """
    target = target & A
    B = A & ~target
    h = np.zeros(len(A))
    h[target] = 1.0
    out = {"killed_size": int(B.sum()), "target_size": int(target.sum())}
    if not B.any():
        out.update({"h": h, "resolved": True, "method": "no_transient_states", "relative_residual": 0.0, "iterations": 0})
        return out
    if not target.any():
        out.update({"h": h, "resolved": True, "method": "empty_target", "relative_residual": 0.0, "iterations": 0})
        return out
    idx, apply = P._killed_operator(chain, B)
    Pj = chain.W[idx] / chain.rates[idx, None]
    T = chain.T[idx]
    into_target = np.where(T >= 0, target[np.maximum(T, 0)], False)
    rhs = (Pj * into_target).sum(axis=1)
    if not rhs.any():
        out.update({"h": h, "resolved": True, "method": "target_unreachable_in_one_step_from_B_and_B_closed", "relative_residual": 0.0, "iterations": 0})
        # still need to check reachability through B: rhs all zero means no B state steps into target,
        # and target states are absorbing for this problem, so h_B = 0 exactly.
        return out
    sol = P.bicgstab(apply, rhs, tolerance=HIT_TOLERANCE, cap=cap, seconds=seconds)
    hb = sol["x"]
    out.update({"iterations": sol["iterations"], "relative_residual": sol["relative_residual"], "resolved": bool(sol["resolved"]), "seconds": sol["seconds"], "method": "bicgstab"})
    use_dense = dense if dense is not None else len(idx) <= DENSE_LIMIT
    if use_dense:
        local = np.full(len(A), -1, dtype=np.int64)
        local[idx] = np.arange(len(idx))
        M = np.eye(len(idx))
        keep = (T >= 0) & np.where(T >= 0, B[np.maximum(T, 0)], False)
        r_i, c_i = np.nonzero(keep)
        np.add.at(M, (r_i, local[T[r_i, c_i]]), -Pj[r_i, c_i])
        hd = np.linalg.solve(M, rhs)
        out["dense_max_abs_difference"] = float(np.abs(hd - hb).max())
    h[idx] = hb
    out["h"] = h
    out["bounds_violation"] = float(max(0.0, -hb.min(), hb.max() - 1.0))
    return out


def _perm_map(n: int, mapping: dict[int, int]) -> tuple[int, ...]:
    """Complete a partial vertex map to a permutation, filling the rest in increasing order."""
    used_src = set(mapping)
    used_dst = set(mapping.values())
    rest_src = [v for v in range(n) if v not in used_src]
    rest_dst = [v for v in range(n) if v not in used_dst]
    full = dict(mapping)
    full.update(zip(rest_src, rest_dst))
    return tuple(full[v] for v in range(n))


def _index_of(chain: Chain) -> np.ndarray:
    index = np.full(int(chain.states.max()) + 1, -1, dtype=np.int64)
    index[chain.states] = np.arange(len(chain.states))
    return index


def replacement(chain: Chain, ct: np.ndarray, n: int, predicate: str, vertices: tuple[int, ...], **solve) -> dict:
    """Entry-set tracking for one flexible predicate: feasibility, departures, renewal, partial renewal."""
    A = P.predicate_mask(chain.states, n, predicate, vertices)
    mu = entrance_weights(chain, ct, A)
    J = float(mu.sum())
    part = participation(chain.states, n, predicate, vertices)
    anc = anchor_vertices(predicate, vertices)
    cand = candidates(n, predicate, vertices)
    index = _index_of(chain)
    entries = np.nonzero(mu > 0)[0]
    sizes = part[entries].sum(axis=1)
    out: dict = {"entry_flux": J, "entry_set_size_distribution": {}, "solves": {}}
    for s in sorted(set(int(v) for v in sizes)):
        out["entry_set_size_distribution"][str(s)] = float(mu[entries][sizes == s].sum() / J)
    dep_total = 0.0
    renew = 0.0
    partial = 0.0
    feasible_mass = 0.0
    size_mass = 0.0
    unresolved = []
    for s in sorted(set(int(v) for v in sizes)):
        can = cand[:s]  # canonical entry set of size s
        sel = entries[sizes == s]
        # map every entry state of this size to the canonical frame: sigma fixes the anchor, S0 -> can
        maps = []
        for i in sel:
            s0 = [v for v in cand if part[i, v]]
            perm = _perm_map(n, {**{a: a for a in anc}, **dict(zip(s0, can))})
            maps.append((i, s0, perm))
        # departures: one solve for the first canonical member; other members by a permutation fixing anchor and can setwise
        tgt_dep = A & ~part[:, can[0]]
        dep = hit_before_exit(chain, A, tgt_dep, **solve)
        out["solves"][f"departure_size{s}"] = {k: v for k, v in dep.items() if k != "h"}
        if not dep["resolved"]:
            unresolved.append(f"departure_size{s}")
        feas = renewal_feasible(n, predicate, vertices, s)
        if feas:
            tgt_ren = A & ~part[:, can].any(axis=1)
            ren = hit_before_exit(chain, A, tgt_ren, **solve)
            out["solves"][f"renewal_size{s}"] = {k: v for k, v in ren.items() if k != "h"}
            if not ren["resolved"]:
                unresolved.append(f"renewal_size{s}")
        r_max = max_partial_absent(n, predicate, vertices, s)
        if predicate == "F_STAR" and r_max > 0:
            absent = (~part[:, can]).sum(axis=1)
            par = hit_before_exit(chain, A, A & (absent >= r_max), **solve)
            out["solves"][f"partial_size{s}"] = {k: v for k, v in par.items() if k != "h"}
            if not par["resolved"]:
                unresolved.append(f"partial_size{s}")
        for i, s0, perm in maps:
            w = mu[i]
            size_mass += w * s
            tables = gtobs.permutation_tables(n, perm)
            yi = index[gtobs.permute_codes(chain.states[i : i + 1], tables)[0]]
            for member in s0:
                # sigma_m: anchor fixed, member -> can[0], rest of S0 -> rest of can
                others = [v for v in s0 if v != member]
                pm = _perm_map(n, {**{a: a for a in anc}, member: can[0], **dict(zip(others, can[1:]))})
                ym = index[gtobs.permute_codes(chain.states[i : i + 1], gtobs.permutation_tables(n, pm))[0]]
                dep_total += w * dep["h"][ym]
            if feas:
                feasible_mass += w
                renew += w * ren["h"][yi]
            if predicate == "F_STAR" and r_max > 0:
                partial += w * par["h"][yi]
    out["expected_distinct_departures_per_episode"] = dep_total / J
    out["departure_fraction_of_entry_participants"] = dep_total / size_mass
    out["feasible_entry_fraction"] = feasible_mass / J
    if feasible_mass == 0.0:
        out["renewal_status"] = "STRUCTURALLY_IMPOSSIBLE"
        out["renewal_unconditional"] = None
        out["renewal_conditional_on_feasible"] = None
    else:
        out["renewal_status"] = "computed"
        out["renewal_unconditional"] = renew / J
        out["renewal_conditional_on_feasible"] = renew / feasible_mass
    if predicate == "F_STAR":
        out["partial_renewal_max_absent"] = {s: max_partial_absent(n, predicate, vertices, int(s)) for s in out["entry_set_size_distribution"]}
        out["partial_renewal_probability"] = partial / J
    out["unresolved"] = unresolved
    out["resolved"] = not unresolved
    return out


# --- NK: density- and layer-flux-matched comparator ----------------------------


def layer_fluxes(chain: Chain, ct: np.ndarray, n: int) -> dict:
    """Target p_k, upward flux J[k,k+1], downward flux J[k+1,k] (positive sums), E[q|k] and within-layer q dispersion."""
    m = len(edges(n))
    x = P.bits(chain.states, n)
    k = x.sum(axis=1)
    up_rate = np.where(~x, chain.W, 0.0).sum(axis=1)
    down_rate = np.where(x, chain.W, 0.0).sum(axis=1)
    p = np.bincount(k, weights=ct, minlength=m + 1)
    up = np.bincount(k, weights=ct * up_rate, minlength=m + 1)[:m]
    down = np.bincount(k, weights=ct * down_rate, minlength=m + 1)[1:]
    q = chain.rates
    mean_q = np.bincount(k, weights=ct * q, minlength=m + 1) / p
    var_q = np.bincount(k, weights=ct * (q - mean_q[k]) ** 2, minlength=m + 1) / p  # two-pass: no cancellation
    return {"p": p, "up": up, "down": down, "mean_q_given_k": mean_q, "sd_q_given_k": np.sqrt(np.maximum(var_q, 0.0)), "q_range_given_k": [float(np.ptp(q[k == j])) if (k == j).any() else 0.0 for j in range(m + 1)]}


def nk_rates(p: np.ndarray, up: np.ndarray) -> dict:
    """b_k = J[k,k+1]/((M-k) p_k), d_{k+1} = J[k,k+1]/((k+1) p_{k+1}); unresolved on any zero bin or flux."""
    m = len(p) - 1
    if (p <= 0).any() or (up <= 0).any():
        return {"resolved": False, "reason": "a zero density bin or zero adjacent-layer flux", "zero_bins": [int(j) for j in np.nonzero(p <= 0)[0]], "zero_fluxes": [int(j) for j in np.nonzero(up <= 0)[0]]}
    ks = np.arange(m)
    birth = np.concatenate([up / ((m - ks) * p[:m]), [0.0]])
    death = np.concatenate([[0.0], up / ((ks + 1) * p[1:])])
    return {"birth": birth, "death": death, "rare_bins": {str(j): float(p[j]) for j in range(m + 1) if p[j] < P.RARE_MASS}, "resolved": True}


def nk_chain(n: int, p: np.ndarray, up: np.ndarray) -> tuple[Chain, np.ndarray, dict]:
    """NK on the full FREE space, its analytic CT law pi_NK(x) = p_|x| / C(M,|x|), and diagnostics."""
    m = len(edges(n))
    rates = nk_rates(p, up)
    if not rates["resolved"]:
        raise ValueError(rates["reason"])
    states = np.arange(1 << m, dtype=np.int64)
    x = P.bits(states, n)
    k = x.sum(axis=1)
    W = np.where(x, rates["death"][k][:, None], rates["birth"][k][:, None])
    log_binom = np.array([math.lgamma(m + 1) - math.lgamma(j + 1) - math.lgamma(m - j + 1) for j in range(m + 1)])
    log_pi = np.log(p)[k] - log_binom[k]
    pi = np.exp(log_pi - log_pi.max())
    pi /= pi.sum()
    T = states[:, None] ^ (1 << np.arange(m))[None, :]
    chain = Chain(m, states, W, T)
    flow_in = np.zeros(len(states))
    for e in range(m):
        flow_in += pi[T[:, e]] * W[T[:, e], e]
    db = 0.0
    for e in range(m):
        a = pi * W[:, e]
        b = pi[T[:, e]] * W[T[:, e], e]
        db = max(db, float((np.abs(a - b) / np.maximum(np.maximum(a, b), 1e-300)).max()))
    info = {
        "birth": [float(v) for v in rates["birth"]],
        "death": [float(v) for v in rates["death"]],
        "detailed_balance_max_relative": db,
        "global_balance_relative": float(np.abs(flow_in - pi * chain.rates).sum() / (pi * chain.rates).sum()),
        "min_rate": float(min(rates["birth"][:m].min(), rates["death"][1:].min())),
        "max_rate": float(max(rates["birth"][:m].max(), rates["death"][1:].max())),
        "rare_bins": rates["rare_bins"],
    }
    return chain, pi, info


def nk_identities(target: dict, nk: dict) -> dict:
    """Relative gaps of the matched quantities (p_k, J up, E[q|k]) between target and NK layer summaries."""

    def rel(a, b):
        a, b = np.asarray(a, float), np.asarray(b, float)
        return float((np.abs(a - b) / np.maximum(np.maximum(np.abs(a), np.abs(b)), 1e-300)).max())

    return {"p_relative": rel(target["p"], nk["p"]), "up_flux_relative": rel(target["up"], nk["up"]), "down_flux_relative": rel(target["down"], nk["down"]), "mean_q_given_k_relative": rel(target["mean_q_given_k"], nk["mean_q_given_k"]), "nk_within_layer_sd_max": float(np.max(nk["sd_q_given_k"]))}


# --- per-law bundle -------------------------------------------------------------


def analyse_law(chain: Chain, ct: np.ndarray, n: int, *, relabelled: bool = True, **solve) -> dict:
    """Every E5B channel of one law for the three flexible predicates (primary and relabelled anchors)."""
    out: dict = {"predicates": {}, "relabelled": {}}
    lf = layer_fluxes(chain, ct, n)
    out["layers"] = {"p": [float(v) for v in lf["p"]], "up_flux": [float(v) for v in lf["up"]], "mean_q_given_k": [float(v) for v in lf["mean_q_given_k"]], "sd_q_given_k": [float(v) for v in lf["sd_q_given_k"]], "q_range_given_k": lf["q_range_given_k"]}
    out["density_jump"] = [float(v) for v in P.jump_density(chain, ct, n)]
    out["mean_rate_ct"] = float(ct @ chain.rates)
    instances = [("predicates", P.primary_instance)]
    if relabelled:
        instances.append(("relabelled", lambda p: P.relabelled_instance(p, n)))
    for key, inst in instances:
        for p in FLEXIBLE:
            v = inst(p)
            A = P.predicate_mask(chain.states, n, p, v)
            loc = local_mask(n, p, v)
            elig = P.eligible_toggles(chain.states, n, p, v)
            block = {"episode": P.episode_statistics(chain, ct, A, eligible=elig), "local": local_clock(chain, ct, A, loc), "flicker": flicker(chain, ct, A, elig, loc), "replacement": replacement(chain, ct, n, p, v, **solve)}
            # local intensity given the predicate and density (diagnostic)
            k = P.bits(chain.states, n).sum(axis=1)
            ql = chain.W[:, loc].sum(axis=1)
            m = len(edges(n))
            mass = np.bincount(k[A], weights=ct[A], minlength=m + 1)
            block["local_hazard_given_k"] = [float(v) if mass[j] > 0 else None for j, v in enumerate(np.bincount(k[A], weights=(ct * ql)[A], minlength=m + 1) / np.maximum(mass, 1e-300))]
            block["vertices"] = list(v)
            out[key][p] = block
    return out
