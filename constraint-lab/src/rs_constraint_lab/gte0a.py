"""Gravity-time programme, open-thetical Round E0A (prompt GT-P002, OTR 1.0).

E0A crosses the gradient / non-gradient boundary of the O=2 pair grammar.
Every rule is ordinary DSL text parsed by ``parse_expression`` and compiled by
``build_kernel``. Templates are label-covariant: each is instantiated over
every ordered witness, so no rule names a direction, a place or a source. The
held source is G0's declared scaffold.

New observation channels, all exact kernel quantities:
  reversibility   entropy production, irreversible flux fraction, maximum
                  elementary-square cycle affinity, projected 2-D net current
  event order     time-reversal asymmetry of consecutive event pairs on the
                  jump chain (event order is clock-free), immediate reversal
  relaxation      continuous generator spectrum (gap, oscillatory modes),
                  integrated autocorrelation times of local and global
                  quantities (persistence of a centre against density)
  occupancy       full class-level stationary table, degree structure,
                  moment-matched triple-Gibbs projection (KL)
Replayable trajectories are sampled from the exact kernel for the atlas only.
They are illustrations; no statistic in the tables is estimated from them.
"""

from __future__ import annotations

import hashlib
import itertools
import math
import time
from dataclasses import dataclass

import numpy as np

from rs_constraint_lab import gt0
from rs_constraint_lab.constraints import Choreography, parse_expression
from rs_constraint_lab.kernel import Kernel, build_kernel
from rs_constraint_lab.state import edges

PROGRAMME = "GT"
ROUND_ID = "round-e0a"
EXPERIMENT_ID = "gt-round-e0a-open-thetical"
ANALYSIS_VERSION = "gt-e0a/v1"
SOURCE = gt0.SOURCE
FACTORS = gt0.FACTORS
MODES = ("HELD", "FREE")
SIZES = (5, 6)
PROBE = 3
DENSE_LIMIT = 4096
LAZY_CAP = 200_000
LAZY_TOLERANCE = 1e-15
STATIONARY_RESIDUAL_TOLERANCE = 1e-12
SYMMETRY_TOLERANCE = 1e-10
IMAG_RELATIVE_THRESHOLD = 1e-6
TRAJECTORIES_PER_CELL = 4
EVENTS_PER_TRAJECTORY = 400

COMPONENT_K = {"close_form": 3, "close_dissolve": 3, "adj_form": 2, "path_form": 3, "path_dissolve": 3}

FAMILIES: dict[str, dict[str, list[tuple[str, str]]]] = {
    "NULL": {"none": []},
    "CLOSE": {"strong_favour": [("close_form", "strong_favour")]},
    "HOLD": {"strong_suppress": [("close_dissolve", "strong_suppress")]},
    "SPLIT": {"weak_favour+weak_suppress": [("close_form", "weak_favour"), ("close_dissolve", "weak_suppress")]},
    "COMPETE": {"strong_favour+strong_favour": [("close_form", "strong_favour"), ("close_dissolve", "strong_favour")]},
    "ANTI": {"strong_suppress": [("close_form", "strong_suppress")]},
    "EXCL": {"prohibit": [("close_form", "prohibit")]},
    "FRUST": {"weak_favour+strong_favour": [("adj_form", "weak_favour"), ("close_dissolve", "strong_favour")]},
    "PATHF": {"weak_favour": [("path_form", "weak_favour")], "weak_suppress": [("path_form", "weak_suppress")]},
    "PATHH": {"weak_suppress": [("path_dissolve", "weak_suppress")], "weak_favour": [("path_dissolve", "weak_favour")]},
}
NON_GRADIENT_KINDS = ("path_form", "path_dissolve")


class E0AError(ValueError):
    """An E0A invariant did not hold."""


def _e(a: int, b: int) -> str:
    return f"{min(a, b)}-{max(a, b)}"


def component_expressions(kind: str, n: int, grade: str) -> list[str]:
    """Label-covariant instances of one component template over every ordered witness."""
    out: list[str] = []
    for a, b in itertools.combinations(range(n), 2):
        others = [c for c in range(n) if c not in (a, b)]
        if kind in ("close_form", "close_dissolve"):
            act = "form" if kind == "close_form" else "dissolve"
            for c in others:
                out.append(f"{act}({_e(a, b)}) | present({_e(a, c)}) & present({_e(b, c)}) => {grade}")
        elif kind == "adj_form":
            for c in others:
                out.append(f"form({_e(a, b)}) | present({_e(a, c)}) => {grade}")
                out.append(f"form({_e(a, b)}) | present({_e(b, c)}) => {grade}")
        elif kind in ("path_form", "path_dissolve"):
            act = "form" if kind == "path_form" else "dissolve"
            for end in (a, b):
                for c in others:
                    for d in others:
                        if d != c:
                            out.append(f"{act}({_e(a, b)}) | present({_e(end, c)}) & present({_e(c, d)}) => {grade}")
        else:
            raise E0AError(f"unknown component {kind}")
    return out


def template_expressions(family: str, grade: str, n: int, families: dict | None = None) -> list[str]:
    out: list[str] = []
    for kind, component_grade in (families or FAMILIES)[family][grade]:
        out.extend(component_expressions(kind, n, component_grade))
    return out


def rules_for(family: str, grade: str, n: int, mode: str, families: dict | None = None):
    template = template_expressions(family, grade, n, families)
    rules = [parse_expression(text, n, order=2) for text in template]
    expected = []
    for kind, component_grade in (families or FAMILIES)[family][grade]:
        expected.extend([COMPONENT_K[kind]] * len(component_expressions(kind, n, component_grade)))
    if [rule.k() for rule in rules] != expected:
        raise E0AError(f"{family} rule has the wrong K")
    rules.extend(parse_expression(text, n, order=2) for text in gt0.scaffold_expressions(mode))
    return tuple(rules)


def build(family: str, grade: str, n: int, mode: str, families: dict | None = None) -> Kernel:
    return build_kernel(n, Choreography(0, 0, rules_for(family, grade, n, mode, families)), FACTORS)


def is_gradient(family: str, families: dict | None = None) -> bool:
    fam = families or FAMILIES
    return not any(kind in NON_GRADIENT_KINDS for grade in fam[family] for kind, _g in fam[family][grade])


def predicted_potential(family: str, grade: str, families: dict | None = None) -> dict | None:
    """Triple-local Gibbs coefficients (natural log) for a gradient family; None if non-gradient.

    Derivation (coverage audit section 3): a form factor f on a witness motif
    multiplies the rate ratio by f, a dissolve factor d divides it. Closure
    witnesses count triangles, adjacency witnesses count wedges. A prohibit
    on a formation restricts the chain to a closed class and adds nothing.
    """
    if not is_gradient(family, families):
        return None
    theta = {"E": 0.0, "W": 0.0, "T": 0.0}
    restricted = False
    for kind, component_grade in (families or FAMILIES)[family][grade]:
        factor = float(FACTORS[component_grade])
        if factor == 0.0:
            restricted = True
            continue
        sign = 1.0 if kind.endswith("_form") else -1.0
        motif = "T" if kind.startswith("close") else "W"
        theta[motif] += sign * math.log(factor)
    return {"restricted_support": restricted, "theta": theta}


def items() -> list[dict]:
    out = []
    for n in SIZES:
        for mode in MODES:
            for family, grades in FAMILIES.items():
                for grade in grades:
                    out.append({"family": family, "grade": grade, "item_id": f"{mode}-N{n}-{family}-{grade}", "mode": mode, "n": n})
    return out


# --- numeric chain -----------------------------------------------------


@dataclass
class Chain:
    """A finite continuous-time toggle chain on a closed reachable class.

    ``W[i, e]`` is the rate of toggling slot e from state ``states[i]``, and
    ``T[i, e]`` the index of the resulting state (-1 when the rate is zero
    and the target lies outside the class).
    """

    n_slots: int
    states: np.ndarray
    W: np.ndarray
    T: np.ndarray

    @property
    def rates(self) -> np.ndarray:
        return self.W.sum(axis=1)


def chain_from_kernel(kernel: Kernel, start: int) -> Chain:
    states = np.array(gt0.reachable(kernel, start), dtype=np.int64)
    index = np.full(1 << kernel.n_edges, -1, dtype=np.int64)
    index[states] = np.arange(len(states))
    W = np.array([[float(w) for w in kernel.weights[int(s)]] for s in states])
    T = np.empty_like(W, dtype=np.int64)
    for e in range(kernel.n_edges):
        T[:, e] = index[states ^ (1 << e)]
    if ((T < 0) & (W > 0)).any():
        raise E0AError("a positive rate leaves the reachable class")
    return Chain(kernel.n_edges, states, W, T)


def stationary(chain: Chain) -> dict:
    """Jump-chain stationary law (G0 convention), then the continuous-time law pi/R."""
    R = chain.rates
    if (R <= 0).any():
        return {"resolved": False, "reason": "zero total rate in the class"}
    P = chain.W / R[:, None]
    size = len(chain.states)
    valid = chain.T >= 0
    rows = np.repeat(np.arange(size), chain.n_slots).reshape(size, chain.n_slots)[valid]
    cols = chain.T[valid]
    vals = P[valid]
    if size <= DENSE_LIMIT:
        matrix = np.zeros((size, size))
        np.add.at(matrix, (rows, cols), vals)
        system = matrix.T - np.eye(size)
        system[-1, :] = 1.0
        rhs = np.zeros(size)
        rhs[-1] = 1.0
        pi = np.linalg.solve(system, rhs)
        method, iterations = "dense_solve", None
    else:
        pi = np.full(size, 1.0 / size)
        iterations = 0
        for iterations in range(1, LAZY_CAP + 1):
            moved = np.bincount(cols, weights=pi[rows] * vals, minlength=size)
            nxt = 0.5 * (pi + moved)
            delta = float(np.abs(nxt - pi).sum())
            pi = nxt
            if delta < LAZY_TOLERANCE:
                break
        method = "lazy_iteration"
    moved = np.bincount(cols, weights=pi[rows] * vals, minlength=size)
    residual = float(np.abs(moved - pi).sum())
    if residual > STATIONARY_RESIDUAL_TOLERANCE or (pi < -1e-15).any():
        return {"iterations": iterations, "method": method, "reason": "residual above tolerance", "residual": residual, "resolved": False}
    pi = np.clip(pi, 0.0, None)
    pi /= pi.sum()
    ct = pi / R
    ct /= ct.sum()
    return {"ct": ct, "iterations": iterations, "jump": pi, "mean_rate_ct": float(ct @ R), "method": method, "residual": residual, "resolved": True}


def reversibility(chain: Chain, ct: np.ndarray, mean_rate: float) -> dict:
    """Entropy production, irreversible flux and elementary-square affinities.

    Jump-chain flux is proportional to continuous flux (pi_jump * P = pi_ct * W
    up to the constant mean rate), so per-event entropy production is the
    per-time value divided by the mean rate.
    """
    valid = chain.T >= 0
    F = ct[:, None] * chain.W
    Frev = np.zeros_like(F)
    for e in range(chain.n_slots):
        mask = valid[:, e]
        Frev[mask, e] = ct[chain.T[mask, e]] * chain.W[chain.T[mask, e], e]
    both = (F > 0) & (Frev > 0)
    one_sided = int(((F > 0) ^ (Frev > 0)).sum())
    sigma = 0.5 * float(((F[both] - Frev[both]) * np.log(F[both] / Frev[both])).sum())
    total = float((F + Frev).sum())
    irreversible = float(np.abs(F - Frev).sum()) / total if total > 0 else 0.0
    max_affinity = 0.0
    nonzero_squares = 0
    squares = 0
    logW = np.where(chain.W > 0, np.log(np.where(chain.W > 0, chain.W, 1.0)), -np.inf)
    idx = np.arange(len(chain.states))
    for e, f in itertools.combinations(range(chain.n_slots), 2):
        ie = chain.T[:, e]
        if_ = chain.T[:, f]
        ok = (ie >= 0) & (if_ >= 0)
        ief = np.full_like(ie, -1)
        ief[ok] = chain.T[ie[ok], f]
        ok &= ief >= 0
        if not ok.any():
            continue
        i, a, b, c = idx[ok], ie[ok], ief[ok], if_[ok]
        fwd = logW[i, e] + logW[a, f] + logW[b, e] + logW[c, f]
        bwd = logW[i, f] + logW[c, e] + logW[b, f] + logW[a, e]
        finite = np.isfinite(fwd) & np.isfinite(bwd)
        if not finite.any():
            continue
        affinity = np.abs(fwd[finite] - bwd[finite])
        squares += int(finite.sum())
        nonzero_squares += int((affinity > 1e-9).sum())
        max_affinity = max(max_affinity, float(affinity.max()))
    return {
        "elementary_squares": squares,
        "entropy_production_per_event": sigma / mean_rate,
        "entropy_production_per_time": sigma,
        "irreversible_flux_fraction": irreversible,
        "max_square_affinity": max_affinity,
        "nonzero_affinity_squares": nonzero_squares,
        "one_sided_transitions": one_sided,
    }


def projected_current(chain: Chain, ct: np.ndarray, bins: np.ndarray, labels: list[str]) -> dict:
    """Net stationary flux between bins of a 2-D projection, as a fraction of total flux."""
    valid = chain.T >= 0
    size = len(chain.states)
    nb = int(bins.max()) + 1
    src = np.repeat(np.arange(size), chain.n_slots).reshape(size, chain.n_slots)[valid]
    dst = chain.T[valid]
    flux = (ct[:, None] * chain.W)[valid]
    keys = bins[src] * nb + bins[dst]
    matrix = np.bincount(keys, weights=flux, minlength=nb * nb).reshape(nb, nb)
    net = matrix - matrix.T
    total = float(matrix.sum())
    pairs = []
    for i, j in zip(*np.nonzero(np.triu(np.abs(net) > 1e-15 * max(total, 1e-300)))):
        pairs.append({"from": labels[i] if net[i, j] > 0 else labels[j], "net_fraction": float(abs(net[i, j]) / total), "to": labels[j] if net[i, j] > 0 else labels[i]})
    pairs.sort(key=lambda r: -r["net_fraction"])
    return {"net_flux_fraction": float(0.5 * np.abs(net).sum() / total) if total > 0 else 0.0, "top_net_currents": pairs[:6]}


def _slot_vertices(n: int) -> list[tuple[int, int]]:
    return edges(n)


def event_order(chain: Chain, jump: np.ndarray, n: int, mode: str) -> dict:
    """Time-reversal asymmetry of consecutive event pairs on the stationary jump chain.

    A pattern is (type1, class1, type2, class2, relation): type F (formation)
    or D (dissolution); class A (probe-source attachment) or P (probe-probe)
    in HELD, X in FREE; relation same / adjacent / disjoint. Its time reverse
    is (flip type2, class2, flip type1, class1, relation). A reversible chain
    gives every pattern the probability of its reverse.
    """
    edge_list = _slot_vertices(n)
    R = chain.rates
    P = chain.W / R[:, None]
    if mode == "HELD":
        klass = ["A" if (a in SOURCE) != (b in SOURCE) else ("S" if a in SOURCE else "P") for a, b in edge_list]
    else:
        klass = ["X"] * len(edge_list)
    probs: dict[tuple, float] = {}
    for e in range(chain.n_slots):
        ie = chain.T[:, e]
        ok_e = (ie >= 0) & (P[:, e] > 0)
        if not ok_e.any():
            continue
        first = jump * P[:, e]
        t1 = np.where(((chain.states >> e) & 1) == 0, "F", "D")
        for f in range(chain.n_slots):
            prob = np.zeros(len(chain.states))
            prob[ok_e] = first[ok_e] * P[ie[ok_e], f]
            if not (prob > 0).any():
                continue
            if e == f:
                rel = "same"
            elif set(edge_list[e]) & set(edge_list[f]):
                rel = "adjacent"
            else:
                rel = "disjoint"
            after = chain.states ^ (1 << e)
            t2 = np.where(((after >> f) & 1) == 0, "F", "D")
            for a in ("F", "D"):
                for b in ("F", "D"):
                    mask = (t1 == a) & (t2 == b)
                    value = float(prob[mask].sum())
                    if value > 0:
                        key = (a, klass[e], b, klass[f], rel)
                        probs[key] = probs.get(key, 0.0) + value
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
    # asym sums |P(p) - P(p*)| once per reverse pair, which is half the sum over all patterns.
    return {"immediate_reversal_probability": reversal, "pattern_asymmetry": asym, "top_asymmetric_patterns": rows[:6]}


def spectrum(chain: Chain, mean_rate: float) -> dict:
    """Continuous generator spectrum, in units of the mean stationary event rate."""
    size = len(chain.states)
    G = np.zeros((size, size))
    valid = chain.T >= 0
    rows = np.repeat(np.arange(size), chain.n_slots).reshape(size, chain.n_slots)[valid]
    np.add.at(G, (rows, chain.T[valid]), chain.W[valid])
    G[np.arange(size), np.arange(size)] -= chain.rates
    lam = np.linalg.eigvals(G) / mean_rate
    order = np.argsort(-lam.real)
    lam = lam[order]
    if abs(lam[0]) > 1e-8:
        raise E0AError(f"leading eigenvalue {lam[0]} is not zero")
    rest = lam[1:]
    scale = float(np.abs(lam).max())
    complex_mask = np.abs(rest.imag) > IMAG_RELATIVE_THRESHOLD * scale
    slow = rest[0]
    osc = rest[complex_mask]
    out = {
        "complex_eigenvalue_count": int(complex_mask.sum()),
        "max_abs_imag_relative": float(np.abs(lam.imag).max() / scale),
        "relaxation_gap": float(-slow.real),
        "slowest_mode": [float(slow.real), float(abs(slow.imag))],
        "spectral_radius": scale,
    }
    if osc.size:
        lead = osc[np.argmax(osc.real)]
        out["slowest_oscillatory_mode"] = [float(lead.real), float(abs(lead.imag))]
        out["max_oscillation_index"] = float((np.abs(osc.imag) / np.abs(osc.real)).max())
    else:
        out["slowest_oscillatory_mode"] = None
        out["max_oscillation_index"] = 0.0
    return out


def autocorrelation_times(chain: Chain, ct: np.ndarray, mean_rate: float, functions: dict[str, np.ndarray]) -> dict:
    """Integrated autocorrelation time int_0^inf C(t)/C(0) dt of each function.

    Uses (-G + 1 pi)^{-1} on pi-centred functions, which equals the group
    inverse there, so it holds for non-reversible chains too. Reported per
    unit time and in mean events.
    """
    size = len(chain.states)
    A = np.zeros((size, size))
    valid = chain.T >= 0
    rows = np.repeat(np.arange(size), chain.n_slots).reshape(size, chain.n_slots)[valid]
    np.add.at(A, (rows, chain.T[valid]), -chain.W[valid])
    A[np.arange(size), np.arange(size)] += chain.rates
    A += np.outer(np.ones(size), ct)
    names = list(functions)
    centred = np.stack([functions[k] - ct @ functions[k] for k in names], axis=1)
    solved = np.linalg.solve(A, centred)
    out = {}
    for j, name in enumerate(names):
        var = float(ct @ centred[:, j] ** 2)
        if var < 1e-14:
            out[name] = None
            continue
        tau = float(ct @ (centred[:, j] * solved[:, j])) / var
        out[name] = {"events": tau * mean_rate, "time": tau, "variance": var}
    return out


# --- structure ---------------------------------------------------------


def structure_arrays(chain: Chain, n: int) -> dict:
    edge_list = edges(n)
    bits = ((chain.states[:, None] >> np.arange(chain.n_slots)) & 1).astype(np.int64)
    incidence = np.zeros((chain.n_slots, n), dtype=np.int64)
    for e, (a, b) in enumerate(edge_list):
        incidence[e, a] = incidence[e, b] = 1
    degree = bits @ incidence
    position = {pair: i for i, pair in enumerate(edge_list)}
    tri = np.zeros(len(chain.states), dtype=np.int64)
    for a, b, c in itertools.combinations(range(n), 3):
        tri += bits[:, position[(a, b)]] & bits[:, position[(a, c)]] & bits[:, position[(b, c)]]
    return {"bits": bits, "degree": degree, "edges": bits.sum(axis=1), "triangles": tri, "wedges": (degree * (degree - 1) // 2).sum(axis=1)}


def group_permutations(n: int, mode: str) -> list[tuple[int, ...]]:
    if mode == "FREE":
        return list(itertools.permutations(range(n)))
    probes = [v for v in range(n) if v not in SOURCE]
    out = []
    for s in itertools.permutations(SOURCE):
        for p in itertools.permutations(probes):
            perm = list(range(n))
            for old, new in zip(SOURCE, s):
                perm[old] = new
            for old, new in zip(probes, p):
                perm[old] = new
            out.append(tuple(perm))
    return out


def permuted_codes(states: np.ndarray, n: int, perm: tuple[int, ...]) -> np.ndarray:
    edge_list = edges(n)
    position = {pair: i for i, pair in enumerate(edge_list)}
    out = np.zeros_like(states)
    for e, (a, b) in enumerate(edge_list):
        target = position[tuple(sorted((perm[a], perm[b])))]
        out |= ((states >> e) & 1) << target
    return out


def class_table(chain: Chain, ct: np.ndarray, jump: np.ndarray, n: int, mode: str, arrays: dict) -> tuple[list[dict], float]:
    """Stationary occupancy by symmetry class, and the symmetry check of the law."""
    perms = group_permutations(n, mode)
    index = {int(s): i for i, s in enumerate(chain.states)}
    canonical = chain.states.copy()
    max_diff = 0.0
    for perm in perms:
        codes = permuted_codes(chain.states, n, perm)
        canonical = np.minimum(canonical, codes)
        mapped = np.array([index.get(int(c), -1) for c in codes])
        if (mapped < 0).any():
            raise E0AError("the reachable class is not closed under the symmetry group")
        max_diff = max(max_diff, float(np.abs(ct[mapped] - ct).max()))
    rows = {}
    for i, code in enumerate(canonical):
        key = int(code)
        row = rows.setdefault(key, {"canonical_state": key, "ct": 0.0, "degree_sequence": sorted(arrays["degree"][i].tolist(), reverse=True), "edges": int(arrays["edges"][i]), "jump": 0.0, "orbit_size": 0, "triangles": int(arrays["triangles"][i])})
        row["ct"] += float(ct[i])
        row["jump"] += float(jump[i])
        row["orbit_size"] += 1
    table = sorted(rows.values(), key=lambda r: (r["edges"], r["canonical_state"]))
    return table, max_diff


def gibbs_projection(ct: np.ndarray, arrays: dict) -> dict:
    """Moment-matched triple-local Gibbs law over the class and KL(pi_ct || it).

    The M-projection onto exp(theta . (E, W, T)) matches the three means; a
    gradient family's law is in the family, so KL is zero up to numerics.
    """
    S = np.stack([arrays["edges"], arrays["wedges"], arrays["triangles"]], axis=1).astype(float)
    target = ct @ S
    spread = S.std(axis=0)
    usable = spread > 0
    X = (S[:, usable] - S[:, usable].mean(axis=0)) / spread[usable]
    m = ct @ X
    theta = np.zeros(X.shape[1])

    def dual(t: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
        z = X @ t
        zmax = z.max()
        w = np.exp(z - zmax)
        Z = w.sum()
        p = w / Z
        mean = p @ X
        return float(np.log(Z) + zmax - t @ m), mean, p

    value, mean, p = dual(theta)
    converged = False
    for _ in range(500):
        grad = mean - m
        if float(np.abs(grad).max()) < 1e-11:
            converged = True
            break
        cov = (X * p[:, None]).T @ X - np.outer(mean, mean)
        step = np.linalg.solve(cov + 1e-14 * np.eye(len(theta)), grad)
        scale = 1.0
        while scale > 1e-8:
            trial = theta - scale * step
            tv, tm, tp = dual(trial)
            if tv <= value + 1e-15:
                theta, value, mean, p = trial, tv, tm, tp
                break
            scale *= 0.5
        else:
            break
    support = ct > 0
    kl = float((ct[support] * np.log(ct[support] / np.maximum(p[support], 1e-300))).sum())
    return {"converged": converged, "kl_nats": kl, "matched_means": {"E": float(target[0]), "T": float(target[2]), "W": float(target[1])}}


def predicted_law_gap(ct: np.ndarray, arrays: dict, potential: dict) -> float:
    theta = potential["theta"]
    h = theta["E"] * arrays["edges"] + theta["W"] * arrays["wedges"] + theta["T"] * arrays["triangles"]
    g = np.exp(h - h.max())
    g /= g.sum()
    return float(np.abs(ct - g).sum())


# --- trajectories (illustrative) ----------------------------------------


def trajectory_seed(item_id: str, k: int, round_id: str = ROUND_ID) -> int:
    return int(hashlib.sha256(f"{round_id}:{item_id}:{k}".encode()).hexdigest()[:16], 16)


def sample_trajectory(chain: Chain, start_index: int, seed: int, events: int) -> dict:
    """Exact Gillespie path of the continuous chain; events are (slot, new bit, time)."""
    rng = np.random.Generator(np.random.PCG64(seed))
    i = start_index
    t = 0.0
    out = []
    R = chain.rates
    for _ in range(events):
        if R[i] <= 0:
            break
        t += float(rng.exponential(1.0 / R[i]))
        cumulative = np.cumsum(chain.W[i])
        e = int(np.searchsorted(cumulative, rng.random() * cumulative[-1], side="right"))
        e = min(e, chain.n_slots - 1)
        while chain.W[i, e] == 0:
            e -= 1
        new_bit = int(((chain.states[i] >> e) & 1) ^ 1)
        i = int(chain.T[i, e])
        out.append([e, new_bit, t])
    return {"events": out, "seed": seed, "start_state": int(chain.states[start_index])}


def trajectory_summary(chain: Chain, path: dict, arrays: dict, start_index: int) -> dict:
    index = {int(s): i for i, s in enumerate(chain.states)}
    state = path["start_state"]
    i = start_index
    visited = {i}
    edge_series = [int(arrays["edges"][i])]
    durations = []
    last = 0.0
    for e, _bit, t in path["events"]:
        durations.append(t - last)
        last = t
        state ^= 1 << e
        i = index[state]
        visited.add(i)
        edge_series.append(int(arrays["edges"][i]))
    time_avg = float(np.dot(edge_series[:-1], durations) / last) if last > 0 else float(edge_series[0])
    return {"distinct_states": len(visited), "event_mean_edges": float(np.mean(edge_series)), "final_state": state, "max_edges": max(edge_series), "min_edges": min(edge_series), "time_mean_edges": time_avg, "total_time": last}


# --- HELD observables reused from G0/G1 ----------------------------------


def shell_activity(chain: Chain, ct: np.ndarray, jump: np.ndarray, n: int) -> dict:
    """G1 shell activity and near/far ratio rho = A(1)/A(2) for every probe, both clocks."""
    edge_list = edges(n)
    probes = [p for p in range(n) if p not in SOURCE]
    incident = {p: [i for i, (a, b) in enumerate(edge_list) if p in (a, b)] for p in probes}
    R = chain.rates
    out = {}
    for clock, law in (("jump", jump), ("continuous", ct)):
        num: dict[str, float] = {}
        mass: dict[str, float] = {}
        for i, s in enumerate(chain.states):
            for p in probes:
                d = gt0.distance_to_source(int(s), n, edge_list, p)
                shell = "inf" if math.isinf(d) else str(int(d))
                local = float(chain.W[i, incident[p]].sum())
                activity = local / R[i] if clock == "jump" else local
                num[shell] = num.get(shell, 0.0) + law[i] * activity
                mass[shell] = mass.get(shell, 0.0) + law[i]
        activity = {k: num[k] / mass[k] for k in sorted(mass) if mass[k] > 1e-12}
        rho = activity["1"] / activity["2"] if "1" in activity and "2" in activity and activity["2"] > 0 else None
        out[clock] = {"near_far_ratio": rho, "shell_activity": activity, "shell_mass": {k: float(mass[k]) for k in sorted(mass)}}
    return out


# --- one item ----------------------------------------------------------


def analyse_item(item: dict, *, with_trajectories: bool = True, families: dict | None = None, round_id: str = ROUND_ID) -> tuple[dict, dict | None]:
    family, grade, n, mode = item["family"], item["grade"], item["n"], item["mode"]
    timings = {}
    started = time.perf_counter()
    kernel = build(family, grade, n, mode, families)
    start = gt0.start_state(n, mode)
    states_list = gt0.reachable(kernel, start)
    structure = gt0.class_structure(kernel, states_list)
    chain = chain_from_kernel(kernel, start)
    timings["build"] = time.perf_counter() - started
    out: dict = {
        "family": family,
        "gradient_family": is_gradient(family, families),
        "grade": grade,
        "mode": mode,
        "n": n,
        "reachable_states": len(chain.states),
        "recurrent_class_sizes": [len(c) for c in structure["recurrent_classes"]],
        "absorbing_state_count": len(structure["absorbing_states"]),
        "rule_instances": len(rules_for(family, grade, n, mode, families)),
    }
    if len(structure["recurrent_classes"]) != 1 or len(structure["recurrent_classes"][0]) != len(states_list):
        out["regime"] = "absorbing" if structure["absorbing_states"] else "mixed"
        out["timings"] = timings
        return out, None
    out["regime"] = "recurrent"
    t0 = time.perf_counter()
    stat = stationary(chain)
    timings["stationary"] = time.perf_counter() - t0
    out["stationary"] = {k: v for k, v in stat.items() if k not in ("ct", "jump")}
    if not stat["resolved"]:
        out["timings"] = timings
        return out, None
    ct, jump, mean_rate = stat["ct"], stat["jump"], stat["mean_rate_ct"]
    arrays = structure_arrays(chain, n)
    t0 = time.perf_counter()
    out["reversibility"] = reversibility(chain, ct, mean_rate)
    timings["reversibility"] = time.perf_counter() - t0
    t0 = time.perf_counter()
    out["event_order"] = event_order(chain, jump, n, mode)
    timings["event_order"] = time.perf_counter() - t0
    edge_list = edges(n)
    if mode == "HELD":
        attach_slots = [i for i, (a, b) in enumerate(edge_list) if (a in SOURCE) != (b in SOURCE)]
        free_slots = [i for i, (a, b) in enumerate(edge_list) if not (a in SOURCE and b in SOURCE)]
        free_edges = arrays["bits"][:, free_slots].sum(axis=1)
        attachments = arrays["bits"][:, attach_slots].sum(axis=1)
        width = int(attachments.max()) + 1
        bins = free_edges * width + attachments
        labels = [f"k{k}a{a}" for k in range(int(free_edges.max()) + 1) for a in range(width)]
        out["projected_current"] = projected_current(chain, ct, bins, labels)
        out["projected_current"]["projection"] = "(free-edge count, attachment count)"
    else:
        width = int(arrays["triangles"].max()) + 1
        bins = arrays["edges"] * width + arrays["triangles"]
        labels = [f"k{k}t{t}" for k in range(int(arrays["edges"].max()) + 1) for t in range(width)]
        out["projected_current"] = projected_current(chain, ct, bins, labels)
        out["projected_current"]["projection"] = "(edge count, triangle count)"
    out["mean_rate_ct"] = mean_rate
    t0 = time.perf_counter()
    table, sym = class_table(chain, ct, jump, n, mode, arrays)
    timings["classes"] = time.perf_counter() - t0
    out["class_table"] = table
    out["symmetry_max_abs_difference"] = sym
    out["gibbs_projection"] = gibbs_projection(ct, arrays)
    potential = predicted_potential(family, grade, families)
    out["predicted_potential"] = potential
    out["predicted_law_l1_gap"] = predicted_law_gap(ct, arrays, potential) if potential is not None else None
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
    if mode == "FREE":
        out["free_jump"] = gt0.free_observables(states_list, jump, n)
        out["free_continuous"] = gt0.free_observables(states_list, ct, n)
    else:
        t0 = time.perf_counter()
        out["held_jump"] = gt0.held_observables(kernel, states_list, jump, n)
        out["held_continuous"] = gt0.held_observables(kernel, states_list, ct, n, per_unit_time=True)
        out["shell_activity"] = shell_activity(chain, ct, jump, n)
        timings["held"] = time.perf_counter() - t0
    if len(chain.states) <= DENSE_LIMIT:
        t0 = time.perf_counter()
        out["spectrum"] = spectrum(chain, mean_rate)
        timings["spectrum"] = time.perf_counter() - t0
        t0 = time.perf_counter()
        if mode == "FREE":
            functions = {"centre_indicator_v0": (deg[:, 0] == n - 1).astype(float), "degree_v0": deg[:, 0].astype(float), "edges": arrays["edges"].astype(float), "triangles": arrays["triangles"].astype(float)}
            ratio_keys = ("degree_v0", "edges")
        else:
            dist_probe = np.array([gt0.distance_to_source(int(s), n, edge_list, PROBE) for s in chain.states])
            functions = {
                "attached_probe": (dist_probe == 1).astype(float),
                "degree_probe": deg[:, PROBE].astype(float),
                "detached_probe": np.isinf(dist_probe).astype(float),
                "free_edges": free_edges.astype(float),
                "triangles": arrays["triangles"].astype(float),
            }
            ratio_keys = ("degree_probe", "free_edges")
        taus = autocorrelation_times(chain, ct, mean_rate, functions)
        out["autocorrelation"] = taus
        local, global_ = taus.get(ratio_keys[0]), taus.get(ratio_keys[1])
        out["localisation_persistence_index"] = local["time"] / global_["time"] if local and global_ else None
        timings["autocorrelation"] = time.perf_counter() - t0
    else:
        out["spectrum"] = None
        out["autocorrelation"] = None
        out["localisation_persistence_index"] = None
        out["dense_limit_note"] = f"spectrum and autocorrelation omitted above {DENSE_LIMIT} states (declared budget)"
    trajectories = None
    if with_trajectories:
        t0 = time.perf_counter()
        start_index = int(np.nonzero(chain.states == start)[0][0])
        paths = []
        for k in range(TRAJECTORIES_PER_CELL):
            path = sample_trajectory(chain, start_index, trajectory_seed(item["item_id"], k, round_id), EVENTS_PER_TRAJECTORY)
            path["summary"] = trajectory_summary(chain, path, arrays, start_index)
            paths.append(path)
        trajectories = {"item_id": item["item_id"], "label": "illustrative exact-kernel samples; no table statistic uses them", "numpy_version": np.__version__, "trajectories": paths}
        timings["trajectories"] = time.perf_counter() - t0
    out["timings"] = timings
    return out, trajectories


# --- plan, execution and publication -------------------------------------

PLAN_RELPATH = "gravity-time/plans/round-e0a-plan.json"
GENERATED_RELPATH = "gravity-time/generated/round-e0a"
TABLES_RELPATH = "gravity-time/reports/round-e0a-tables.json"
WATCHDOG_SECONDS = 900
ROUND_WALL_CAP_SECONDS = 3 * 3600
IDENTITY_TOLERANCE = 1e-9
REVERSIBLE_FLUX_TOLERANCE = 1e-9
NON_REVERSIBLE_FLOOR = 1e-6
ONTOLOGY = {"G": 0, "H": 0, "L": 0, "O": 2, "S": 0, "grammar": "ordinary pair DSL", "N": list(SIZES)}
TRIAD = ("CLOSE-strong_favour", "HOLD-strong_suppress", "SPLIT-weak_favour+weak_suppress")
PATH_PAIRS = (("PATHF-weak_favour", "PATHH-weak_suppress"), ("PATHF-weak_suppress", "PATHH-weak_favour"))


def prepare_plan() -> dict:
    from rs_constraint_lab.explore08 import plan_hash

    document = {
        "analysis_only": True,
        "analysis_version": ANALYSIS_VERSION,
        "clocks": {
            "continuous": "per-slot exponential rates equal to the event weights (declared scaffold); stationary law pi_jump / R normalised; spectra and autocorrelation times reported per unit time and in mean stationary events",
            "event_order": "the stationary jump chain; event order is the same under both clocks because the continuous chain's embedded jump chain is the lab kernel",
            "jump": "lab full-event kernel, one admissible toggle per event",
        },
        "comparisons": {
            "kinetic_triad": list(TRIAD),
            "path_equal_ratio_pairs": [list(p) for p in PATH_PAIRS],
            "notes": "Class-level L1 distance of continuous-time stationary laws within each comparison, plus side-by-side kinetic observables. Pairs in path_equal_ratio_pairs have identical local rate ratios r_ab(x); in the gradient class that fixes pi_ct, here it is open.",
        },
        "experiment_id": EXPERIMENT_ID,
        "families": {
            family: {
                grade: {
                    "components": [{"grade": g, "K": COMPONENT_K[k], "kind": k, "template_example": component_expressions(k, 5, g)[0]} for k, g in components],
                    "gradient": is_gradient(family),
                    "predicted_potential": predicted_potential(family, grade),
                }
                for grade, components in grades.items()
            }
            for family, grades in FAMILIES.items()
        },
        "frozen_expectations": {
            "X1_gradient_cells_reversible": f"every gradient-family cell has irreversible flux fraction <= {REVERSIBLE_FLUX_TOLERANCE} and, where the spectrum is computed, max |Im lambda| / spectral radius <= {IMAG_RELATIVE_THRESHOLD} (derivation: coverage audit section 3)",
            "X2_gradient_cells_follow_the_predicted_triple_gibbs_law": f"every gradient-family cell has L1(pi_ct, exp(theta . (E, W, T)) / Z on the reachable class) <= {IDENTITY_TOLERANCE}, theta as recorded per family (derivation: coverage audit section 3)",
            "X3_kinetic_triad_shares_one_law": f"CLOSE-strong, HOLD-strong and SPLIT have pairwise class-level L1 <= {IDENTITY_TOLERANCE} in every mode and N (implied by X2)",
            "X4_path_cells_are_not_reversible": f"every PATHF and PATHH cell has irreversible flux fraction > {NON_REVERSIBLE_FLOOR} and maximum square affinity > {NON_REVERSIBLE_FLOOR} (derivation: coverage audit section 3, the elementary square on ab and ac). Magnitude is not predicted",
            "X5_null_autocorrelation": f"NULL FREE N=5 has integrated autocorrelation time 1/2 per unit time for edges and for the degree of vertex 0, so the localisation persistence index is 1 within {IDENTITY_TOLERANCE} (independent unit-rate bits)",
        },
        "history": False,
        "initial_conditions": {"FREE": "empty graph; analysed on the full state space", "HELD": "the source triangle alone; analysed on its reachable class"},
        "items": items(),
        "meta_constraints": False,
        "method": {"name": "Open-Thetical Research", "path": "research-methods/open-thetical-research.md", "sha256": "2d9023955ddfaf269131033589c547cea7090c72caf2577ab28f7138dfb388dd", "version": "1.0"},
        "mode": "B",
        "modes": {
            "FREE": "no held structure",
            "HELD": {"meaning": "declared exploratory instrument, not mass; same scaffold as G0", "scaffold": gt0.scaffold_expressions("HELD"), "source": list(SOURCE)},
        },
        "new_primitives": False,
        "observables": {
            "reversibility": "entropy production per unit time and per mean event; irreversible flux fraction sum|F-F_rev|/sum(F+F_rev); maximum |cycle affinity| over all elementary squares (x, x^e, x^e^f, x^f) and the count of non-zero ones; one-sided transitions",
            "projected_current": "net stationary flux fraction on (edge count, triangle count) in FREE and (free-edge count, attachment count) in HELD; top six net currents",
            "event_order": "probability of each consecutive event pair pattern (type, slot class, type, slot class, relation) on the stationary jump chain; pattern asymmetry = sum over reverse pairs of |P(p) - P(p*)|; immediate reversal probability",
            "spectrum": f"continuous generator eigenvalues in mean-event units for classes of at most {DENSE_LIMIT} states: relaxation gap, slowest mode, complex eigenvalue count (|Im| > {IMAG_RELATIVE_THRESHOLD} x spectral radius), slowest oscillatory mode, maximum oscillation index |Im|/|Re|",
            "autocorrelation": f"integrated autocorrelation times (per unit time and in mean events) for classes of at most {DENSE_LIMIT} states. FREE: edges, triangles, degree of vertex 0, indicator that vertex 0 is a full centre. HELD: free edges, triangles, degree of probe {PROBE}, probe attached (distance 1), probe detached. Localisation persistence index = tau(local degree) / tau(global edge count)",
            "occupancy": "class-level stationary table under both clocks (FREE: S_N orbits; HELD: S_3 x S_(N-3) orbits), edge-count distribution and its modes, expected edges, wedges, triangles, max degree, degree variance, probability of a full centre; moment-matched triple-Gibbs projection KL(pi_ct || pi_theta*)",
            "held_reused": "G0 held observables (attachment fraction, density-conditioned attachment, distance distribution, drift, escape, capture) under both clocks; G1 shell activity and near/far ratio rho under both clocks",
            "free_reused": "G0 free observables (edge-count distribution, triangles given edge count) under both clocks",
            "trajectories": f"{TRAJECTORIES_PER_CELL} exact Gillespie paths of {EVENTS_PER_TRAJECTORY} events per cell from the declared start, seeds sha256('{ROUND_ID}:<item_id>:<k>')[:16] as PCG64; atlas selection rule: representative = lower median of time-mean edges, atypical = farthest time-mean edges from the stationary expected edges. Illustrative; no table statistic uses them",
        },
        "ontology": ONTOLOGY,
        "open_questions_without_prediction": [
            "Do non-gradient PATH cells carry visible arrows in the projected current and in event order, and how large are they relative to the full entropy production (projection loss)?",
            "Do equal-ratio PATHF/PATHH pairs share a stationary law?",
            "Does COMPETE (uniform pi_ct) change near/far activity, relaxation or reversal probability relative to NULL?",
            "How do approach, retention and the symmetric split differ in relaxation, autocorrelation and event order at one shared law?",
            "Does ANTI repel probes from the held source, and does EXCL differ from ANTI beyond its restricted support?",
            "Does FRUST produce centre-like structure (degree heterogeneity, full-centre probability, localisation persistence index above 1) in FREE mode?",
            "Is any non-gradient stationary law far from the moment-matched triple-Gibbs law?",
            "Anything not anticipated above.",
        ],
        "parameter_fit": False,
        "pre_freeze_exposure": {
            "note": "Before freezing: observables were exercised on a synthetic 4-state cycle fixture (analytic sigma, spectrum, autocorrelation) and on N=4 fixtures (not an E0A size) for NULL and CLOSE in both modes; full analysis was timed on N=6 NULL in both modes (theorem-fixed values); the PATHF weak_favour N=6 FREE kernel was built for timing only, with no observable computed. No E0A observable of any non-NULL family at N=5 or N=6 was computed.",
        },
        "programme": "GT",
        "prompt_id": "GT-P002",
        "question": "Across the gradient / non-gradient boundary of the O=2 pair grammar, and across cooperating, opposing and competing compositions and soft and hard repulsion, which relational conditions produce basins, centres, stationary direction of succession, oscillatory return or kinetic differences at a shared occupancy, in HELD and FREE arrangements?",
        "round_id": ROUND_ID,
        "sampling": "exact census of the declared 48 cells; no sampling of the rule space; trajectories are illustrations only",
        "schema": "rs-gt.e0a-plan/v1",
        "software": {"analysis_module": "rs_constraint_lab.gte0a", "numpy": np.__version__, "python": __import__("platform").python_version()},
        "stochastic_trajectories": "illustrative_only",
        "stop_conditions": {
            "item": f"an item past the {WATCHDOG_SECONDS}-second watchdog stops the round; it is recorded and not retried with changed parameters",
            "round": f"the round stops when all items are written or the {ROUND_WALL_CAP_SECONDS}-second wall cap is reached",
            "unresolved": f"an item whose stationary residual exceeds {STATIONARY_RESIDUAL_TOLERANCE} after {LAZY_CAP} lazy iterations is recorded as unresolved, without stationary observables; no solver or tolerance is changed after the freeze without a recorded post-freeze note",
        },
        "tolerances": {"identity": IDENTITY_TOLERANCE, "imag_relative": IMAG_RELATIVE_THRESHOLD, "non_reversible_floor": NON_REVERSIBLE_FLOOR, "reversible_flux": REVERSIBLE_FLUX_TOLERANCE, "stationary_residual": STATIONARY_RESIDUAL_TOLERANCE, "symmetry": SYMMETRY_TOLERANCE},
        "work_count": {
            "disk_budget_bytes": 50_000_000,
            "items": len(items()),
            "largest_state_space": 32768,
            "memory_budget_bytes": 4_000_000_000,
            "round_wall_cap_seconds": ROUND_WALL_CAP_SECONDS,
            "wall_time_estimate_seconds": 900,
            "watchdog_seconds": WATCHDOG_SECONDS,
            "workers": 1,
        },
    }
    document["plan_hash"] = plan_hash(document)
    return document


def require_execution(repo, commit, *, require_remote=True) -> dict:
    from rs_constraint_lab.explore08 import FrozenPlanError, remote_contains, require_frozen_plan

    plan = require_frozen_plan(repo, commit, PLAN_RELPATH, disk_path=repo / PLAN_RELPATH)
    if require_remote and not remote_contains(repo, commit or ""):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    if plan.get("items") != items() or plan.get("history") is not False or plan.get("new_primitives") is not False or plan.get("ontology") != ONTOLOGY:
        raise FrozenPlanError("execution refused: E0A plan contract drifted")
    return plan


def run(root, plan) -> list[dict]:
    from rs_constraint_lab.durable import atomic_write_json, read_json

    round_started = time.perf_counter()
    rows = []
    for index, item in enumerate(plan["items"], start=1):
        path = root / "items" / f"{item['item_id']}.json"
        if path.is_file() and read_json(path).get("item_id") == item["item_id"]:
            payload = read_json(path)
        else:
            if time.perf_counter() - round_started > ROUND_WALL_CAP_SECONDS:
                raise RuntimeError("round wall cap reached")
            started = time.perf_counter()
            result, trajectories = analyse_item(item)
            wall = time.perf_counter() - started
            if wall > WATCHDOG_SECONDS:
                raise RuntimeError(f"{item['item_id']} exceeded the watchdog ({wall:.1f}s)")
            payload = {"item": item, "item_id": item["item_id"], "result": result, "wall_seconds": wall}
            atomic_write_json(path, payload)
            if trajectories is not None:
                atomic_write_json(root / "trajectories" / f"{item['item_id']}.json", trajectories)
        rows.append(payload)
        atomic_write_json(root / "status.json", {"completed_items": index, "item_count": len(plan["items"]), "last_item_id": item["item_id"], "updated_unix": time.time()})
    return rows


def _class_l1(a: dict, b: dict) -> float | None:
    if "class_table" not in a or "class_table" not in b:
        return None
    ta = {row["canonical_state"]: row["ct"] for row in a["class_table"]}
    tb = {row["canonical_state"]: row["ct"] for row in b["class_table"]}
    return float(sum(abs(ta.get(k, 0.0) - tb.get(k, 0.0)) for k in set(ta) | set(tb)))


def _kinetic_row(r: dict) -> dict:
    row = {
        "immediate_reversal_probability": r["event_order"]["immediate_reversal_probability"],
        "irreversible_flux_fraction": r["reversibility"]["irreversible_flux_fraction"],
        "mean_rate_ct": r["mean_rate_ct"],
        "pattern_asymmetry": r["event_order"]["pattern_asymmetry"],
    }
    if r.get("spectrum"):
        row["relaxation_gap"] = r["spectrum"]["relaxation_gap"]
    if r.get("autocorrelation"):
        row["autocorrelation_events"] = {k: (v["events"] if v else None) for k, v in r["autocorrelation"].items()}
        row["localisation_persistence_index"] = r["localisation_persistence_index"]
    if "shell_activity" in r:
        row["near_far_ratio"] = {c: r["shell_activity"][c]["near_far_ratio"] for c in ("jump", "continuous")}
    return row


def assemble(results: dict[str, dict]) -> dict:
    checks: dict[str, dict] = {}
    comparisons: dict[str, dict] = {}
    for key, r in results.items():
        if r.get("regime") != "recurrent" or "reversibility" not in r:
            continue
        if r["gradient_family"]:
            flux = r["reversibility"]["irreversible_flux_fraction"]
            imag = r["spectrum"]["max_abs_imag_relative"] if r.get("spectrum") else None
            checks[f"X1-{key}"] = {"holds": flux <= REVERSIBLE_FLUX_TOLERANCE and (imag is None or imag <= IMAG_RELATIVE_THRESHOLD), "irreversible_flux_fraction": flux, "max_abs_imag_relative": imag}
            gap = r["predicted_law_l1_gap"]
            checks[f"X2-{key}"] = {"holds": gap is not None and gap <= IDENTITY_TOLERANCE, "l1_gap": gap}
        if r["family"] in ("PATHF", "PATHH"):
            flux = r["reversibility"]["irreversible_flux_fraction"]
            aff = r["reversibility"]["max_square_affinity"]
            checks[f"X4-{key}"] = {"holds": flux > NON_REVERSIBLE_FLOOR and aff > NON_REVERSIBLE_FLOOR, "irreversible_flux_fraction": flux, "max_square_affinity": aff}
    for n in SIZES:
        for mode in MODES:
            prefix = f"{mode}-N{n}-"
            triad = {name: results.get(prefix + name) for name in TRIAD}
            if all(v and "class_table" in v for v in triad.values()):
                gaps = {f"{a}|{b}": _class_l1(triad[a], triad[b]) for a, b in itertools.combinations(TRIAD, 2)}
                checks[f"X3-{mode}-N{n}"] = {"holds": all(g is not None and g <= IDENTITY_TOLERANCE for g in gaps.values()), "l1": gaps}
                comparisons[f"kinetic_triad-{mode}-N{n}"] = {name: _kinetic_row(v) for name, v in triad.items()}
            for a, b in PATH_PAIRS:
                ra, rb = results.get(prefix + a), results.get(prefix + b)
                if ra and rb and "class_table" in ra and "class_table" in rb:
                    comparisons[f"path_pair-{mode}-N{n}-{a}|{b}"] = {"class_l1": _class_l1(ra, rb), a: _kinetic_row(ra), b: _kinetic_row(rb)}
            null, compete = results.get(prefix + "NULL-none"), results.get(prefix + "COMPETE-strong_favour+strong_favour")
            if null and compete and "class_table" in null and "class_table" in compete:
                comparisons[f"compete_vs_null-{mode}-N{n}"] = {"class_l1": _class_l1(null, compete), "COMPETE": _kinetic_row(compete), "NULL": _kinetic_row(null)}
    null5 = results.get("FREE-N5-NULL-none")
    if null5 and null5.get("autocorrelation"):
        tau = null5["autocorrelation"]
        gap = max(abs(tau["edges"]["time"] - 0.5), abs(tau["degree_v0"]["time"] - 0.5), abs(null5["localisation_persistence_index"] - 1.0))
        checks["X5-FREE-N5"] = {"holds": gap <= IDENTITY_TOLERANCE, "gap": gap}
    return {"comparisons": comparisons, "frozen_expectations": checks}


def publish(root, plan, out, *, frozen_plan_commit) -> str:
    from rs_constraint_lab.durable import atomic_write_json, canonical_json, read_json, sha256_bytes

    loaded = {item["item_id"]: read_json(root / "items" / f"{item['item_id']}.json") for item in plan["items"]}
    results = {k: v["result"] for k, v in loaded.items()}
    problems = []
    for key, r in results.items():
        if r.get("regime") == "recurrent":
            st = r.get("stationary", {})
            if not st.get("resolved"):
                problems.append(f"{key}: stationary unresolved")
            elif st["residual"] > STATIONARY_RESIDUAL_TOLERANCE:
                problems.append(f"{key}: residual")
            if "symmetry_max_abs_difference" in r and r["symmetry_max_abs_difference"] > SYMMETRY_TOLERANCE:
                problems.append(f"{key}: symmetry")
    assembled = assemble(results)
    payload = {
        "analysis_version": ANALYSIS_VERSION,
        "comparisons": assembled["comparisons"],
        "experiment_id": EXPERIMENT_ID,
        "frozen_analysis_plan_commit": frozen_plan_commit,
        "frozen_expectations": assembled["frozen_expectations"],
        "plan_hash": plan["plan_hash"],
        "results": results,
        "round_id": ROUND_ID,
        "schema": "rs-gt.e0a-tables/v1",
        "validation": {"ok": not problems, "problems": problems},
        "wall_seconds_max": max(v["wall_seconds"] for v in loaded.values()),
        "wall_seconds_total": sum(v["wall_seconds"] for v in loaded.values()),
    }
    body = dict(payload)
    body["payload_sha256"] = sha256_bytes(canonical_json(payload).encode("utf-8"))
    atomic_write_json(out, body)
    return body["payload_sha256"]
