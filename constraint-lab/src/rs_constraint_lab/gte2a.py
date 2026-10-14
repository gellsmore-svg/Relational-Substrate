"""Gravity-time programme, Round E2A (prompt GT-P005, OTR 1.0): mechanism-diversity atlas.

Question: what makes relational changes occur in directionally ordered
sequences, and when does dissolving a relation enable a later change rather
than merely precede it?

Pre-freeze algebra (formal note, docs/e2-formal-mechanism.md): for any rule
built from close, adjacency and path components with positive factors, the
elementary square on two slots e = (p, q), f = (p, r) sharing vertex p, taken
in the orientation "form e, form f, dissolve e, dissolve f" from a base state
x where both are absent, has log affinity

    A = sigma * (deg_x(r) - deg_x(q)),
    sigma = sum(log m, path_dissolve components) - sum(log m, path_form components),

and every square on disjoint slots has A = 0. Closure and adjacency
components cancel. A component with factor 0 leaves only squares on which it
reads no witness, where its contribution is 0.

Channels added to the gtobs suite (each per cell):

* square census: every square whose four states are in the class; intact
  (all eight rates positive) or broken; signed affinity, formula residual,
  stationary circulation around the square, alignment of circulation with
  affinity, role classes, frozen-rule exemplars;
* partner-frame event order: consecutive events on adjacent slots, classified
  by the sign of the far-endpoint degree difference; generalises the handover
  without a held source;
* matched dissolution: for every present relation g and every other slot f,
  the state x and its matched partner x- = x without g; strict support
  change, rate ratio, jump-probability ratio (and its normalisation part),
  probability that f toggles within H jump events, and the observed
  precedence ratio after an executed dissolution of g;
* one-way structure: transitions whose reverse has zero rate.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

from rs_constraint_lab import gte0a, gte0b, gte1, gtkernel, gtobs
from rs_constraint_lab.gte0a import SOURCE
from rs_constraint_lab.state import edges

ROUND_ID = "round-e2a"
EXPERIMENT_ID = "gt-round-e2a-mechanism-atlas"
ANALYSIS_VERSION = "gt-e2a/v1"
PROMPT_ID = "GT-P005"

PATH_GRADES = ("prohibit", "strong_suppress", "weak_suppress", "weak_favour", "strong_favour")
FAMILIES: dict[str, dict[str, list[tuple[str, str]]]] = {
    "PATHF": {g: [("path_form", g)] for g in PATH_GRADES},
    "PATHH": {g: [("path_dissolve", g)] for g in PATH_GRADES},
    "PFD": {f"{a}+{b}": [("path_form", a), ("path_dissolve", b)] for a in ("weak_suppress", "weak_favour") for b in ("weak_suppress", "weak_favour")},
    "NULL": {"none": []},
    "CLOSEW": {"weak_favour": [("close_form", "weak_favour")]},
    "EXCL": {"prohibit": [("close_form", "prohibit")]},
    "EXPH": {"prohibit+weak_favour": [("close_form", "prohibit"), ("path_dissolve", "weak_favour")]},
    "EXPF": {"prohibit+weak_suppress": [("close_form", "prohibit"), ("path_form", "weak_suppress")]},
    "ADPF": {"strong_suppress+weak_favour": [("adj_form", "strong_suppress"), ("path_form", "weak_favour")]},
    "ADPS": {"strong_suppress+weak_suppress": [("adj_form", "strong_suppress"), ("path_form", "weak_suppress")]},
}
STRATA = {
    "S1_single_path_ladder": [("PATHF", g) for g in PATH_GRADES] + [("PATHH", g) for g in PATH_GRADES],
    "S2_form_dissolve_pairs": [("PFD", g) for g in FAMILIES["PFD"]],
    "S3_reversible_and_hard_controls": [("NULL", "none"), ("CLOSEW", "weak_favour"), ("EXCL", "prohibit")],
    "S4_hard_support_plus_path": [("EXPH", "prohibit+weak_favour"), ("EXPF", "prohibit+weak_suppress")],
    "S5_opposing_density": [("ADPF", "strong_suppress+weak_favour"), ("ADPS", "strong_suppress+weak_suppress")],
}
N6_HELD = [("PATHF", "weak_suppress"), ("PATHH", "weak_favour"), ("PATHF", "strong_suppress"), ("PATHH", "strong_favour")]
HORIZONS = (1, 2, 4, 8)
SIGMA_ZERO_TOLERANCE = 1e-12


def sigma(components: list[tuple[str, str]], factors: dict | None = None) -> float:
    table = factors or gte0a.FACTORS
    total = 0.0
    for kind, grade in components:
        m = float(table[grade])
        if not kind.startswith("path") or m == 0.0:
            continue
        total += math.log(m) if kind == "path_dissolve" else -math.log(m)
    return total


def has_hard(components) -> bool:
    return any(float(gte0a.FACTORS[g]) == 0.0 for _k, g in components)


def item_id(mode: str, n: int, family: str, grade: str) -> str:
    return f"{mode}-N{n}-{family}-{grade}"


def items() -> list[dict]:
    out = []
    for stratum, cells in STRATA.items():
        for family, grade in cells:
            for mode in ("HELD", "FREE"):
                out.append({"family": family, "grade": grade, "item_id": item_id(mode, 5, family, grade), "mode": mode, "n": 5, "stratum": stratum})
    for family, grade in N6_HELD:
        out.append({"family": family, "grade": grade, "item_id": item_id("HELD", 6, family, grade), "mode": "HELD", "n": 6, "stratum": "S6_n6_held_robustness"})
    return out


# --- recurrent class ---------------------------------------------------------------------------


def terminal_classes(chain) -> list[np.ndarray]:
    """Closed communicating classes of the reachable chain (iterative Tarjan)."""
    size = len(chain.states)
    succ = [[int(t) for t, w in zip(chain.T[i], chain.W[i]) if t >= 0 and w > 0] for i in range(size)]
    index = [-1] * size
    low = [0] * size
    on = [False] * size
    stack: list[int] = []
    comps: list[list[int]] = []
    counter = 0
    for root in range(size):
        if index[root] >= 0:
            continue
        work = [(root, 0)]
        while work:
            v, pos = work.pop()
            if pos == 0:
                index[v] = low[v] = counter
                counter += 1
                stack.append(v)
                on[v] = True
            recurse = False
            for k in range(pos, len(succ[v])):
                w = succ[v][k]
                if index[w] < 0:
                    work.append((v, k + 1))
                    work.append((w, 0))
                    recurse = True
                    break
                if on[w]:
                    low[v] = min(low[v], index[w])
            if recurse:
                continue
            if low[v] == index[v]:
                comp = []
                while True:
                    w = stack.pop()
                    on[w] = False
                    comp.append(w)
                    if w == v:
                        break
                comps.append(comp)
            if work:
                parent = work[-1][0]
                low[parent] = min(low[parent], low[v])
    member = np.full(size, -1)
    for c, comp in enumerate(comps):
        member[comp] = c
    closed = []
    for c, comp in enumerate(comps):
        if all(member[w] == c for v in comp for w in succ[v]):
            closed.append(np.array(sorted(comp)))
    return closed


def restrict(chain, keep: np.ndarray):
    remap = np.full(len(chain.states), -1, dtype=np.int64)
    remap[keep] = np.arange(len(keep))
    T = chain.T[keep]
    T = np.where(T >= 0, remap[np.maximum(T, 0)], -1)
    W = chain.W[keep].copy()
    if ((T < 0) & (W > 0)).any():
        raise ValueError("restricted class is not closed")
    return gte0a.Chain(chain.n_slots, chain.states[keep], W, T)


# --- square census -----------------------------------------------------------------------------


def _bits(chain) -> np.ndarray:
    return ((chain.states[:, None] >> np.arange(chain.n_slots)) & 1).astype(np.int64)


def _degrees(chain, n: int) -> np.ndarray:
    E = edges(n)
    bits = _bits(chain)
    deg = np.zeros((len(chain.states), n), dtype=np.int64)
    for i, (a, b) in enumerate(E):
        deg[:, a] += bits[:, i]
        deg[:, b] += bits[:, i]
    return deg


def slot_classes(n: int, mode: str) -> list[str]:
    if mode != "HELD":
        return ["X"] * len(edges(n))
    return ["A" if (a in SOURCE) != (b in SOURCE) else ("S" if a in SOURCE else "P") for a, b in edges(n)]


def square_role(n: int, mode: str, e: int, f: int) -> str:
    E = edges(n)
    shared = set(E[e]) & set(E[f])
    if not shared:
        return "disjoint"
    if mode != "HELD":
        return "adjacent"
    k = slot_classes(n, mode)
    (p,) = shared
    where = "src" if p in SOURCE else "prb"
    return "".join(sorted(k[e] + k[f])) + "@" + where


def square_census(chain, n: int, mode: str, components, ct: np.ndarray | None, factors: dict | None = None) -> dict:
    E = edges(n)
    sg = sigma(components, factors)
    deg = _degrees(chain, n)
    bits = _bits(chain)
    logW = np.where(chain.W > 0, np.log(np.where(chain.W > 0, chain.W, 1.0)), -np.inf)
    J = None
    if ct is not None:
        F = ct[:, None] * chain.W
        Frev = np.zeros_like(F)
        valid = chain.T >= 0
        for e in range(chain.n_slots):
            m = valid[:, e]
            Frev[m, e] = F[chain.T[m, e], e]
        J = F - Frev
        total_flux = float(F.sum())
    roles: dict[str, dict] = {}
    rows = []
    formula_err = 0.0
    disjoint_max = 0.0
    broken = 0
    intact = 0
    for e, f in itertools.combinations(range(chain.n_slots), 2):
        base = np.nonzero((bits[:, e] == 0) & (bits[:, f] == 0))[0]
        i1 = chain.T[base, e]
        i3 = chain.T[base, f]
        ok = (i1 >= 0) & (i3 >= 0)
        base, i1, i3 = base[ok], i1[ok], i3[ok]
        i2 = chain.T[i1, f]
        ok = i2 >= 0
        base, i1, i2, i3 = base[ok], i1[ok], i2[ok], i3[ok]
        if not len(base):
            continue
        fw = np.stack([logW[base, e], logW[i1, f], logW[i2, e], logW[i3, f]])
        bw = np.stack([logW[base, f], logW[i3, e], logW[i2, f], logW[i1, e]])
        good = np.isfinite(fw).all(axis=0) & np.isfinite(bw).all(axis=0)
        broken += int((~good).sum())
        intact += int(good.sum())
        if not good.any():
            continue
        b0, b1, b2, b3 = base[good], i1[good], i2[good], i3[good]
        A = fw[:, good].sum(axis=0) - bw[:, good].sum(axis=0)
        shared = set(E[e]) & set(E[f])
        role = square_role(n, mode, e, f)
        if shared:
            (p,) = shared
            q = E[e][0] if E[e][1] == p else E[e][1]
            r = E[f][0] if E[f][1] == p else E[f][1]
            D = deg[b0, r] - deg[b0, q]
            pred = sg * D
            formula_err = max(formula_err, float(np.abs(A - pred).max()))
        else:
            D = np.zeros(len(b0), dtype=np.int64)
            disjoint_max = max(disjoint_max, float(np.abs(A).max()))
        C = J[b0, e] + J[b1, f] + J[b2, e] + J[b3, f] if J is not None else np.zeros(len(b0))
        # Orient HELD attachment/probe squares as (P first, A second) = handover orientation.
        orient = 1.0
        if mode == "HELD" and slot_classes(n, mode)[e] == "A" and slot_classes(n, mode)[f] == "P":
            orient = -1.0
        Ao, Co, Do = orient * A, orient * C, orient * D
        r_ = roles.setdefault(role, {"squares": 0, "affinity_nonzero": 0, "affinity_positive": 0, "affinity_negative": 0, "max_abs_affinity": 0.0, "degree_difference_negative": 0, "circulation_abs": 0.0, "circulation_aligned_abs": 0.0, "circulation_counter_abs": 0.0, "circulation_on_zero_affinity_abs": 0.0, "circulation_signed_oriented": 0.0})
        nz = np.abs(Ao) > 1e-12
        r_["squares"] += int(len(Ao))
        r_["affinity_nonzero"] += int(nz.sum())
        r_["affinity_positive"] += int((Ao > 1e-12).sum())
        r_["affinity_negative"] += int((Ao < -1e-12).sum())
        r_["max_abs_affinity"] = max(r_["max_abs_affinity"], float(np.abs(Ao).max()))
        r_["degree_difference_negative"] += int((Do < 0).sum())
        r_["circulation_abs"] += float(np.abs(Co).sum())
        r_["circulation_aligned_abs"] += float(np.abs(Co)[nz & (np.sign(Co) == np.sign(Ao))].sum())
        r_["circulation_counter_abs"] += float(np.abs(Co)[nz & (np.sign(Co) == -np.sign(Ao)) & (Co != 0)].sum())
        r_["circulation_on_zero_affinity_abs"] += float(np.abs(Co)[~nz].sum())
        r_["circulation_signed_oriented"] += float(Co.sum())
        for j in range(len(b0)):
            rows.append((float(A[j]), float(C[j]), int(D[j]), e, f, int(b0[j]), int(b1[j]), int(b2[j]), int(b3[j]), role))
    out = {"broken_squares": broken, "disjoint_max_abs_affinity": disjoint_max, "formula_max_abs_error": formula_err, "intact_squares": intact, "roles": roles, "sigma": sg}
    if J is not None:
        norm = total_flux if total_flux > 0 else 1.0
        for r_ in roles.values():
            for k in ("circulation_abs", "circulation_aligned_abs", "circulation_counter_abs", "circulation_on_zero_affinity_abs", "circulation_signed_oriented"):
                r_[k + "_per_total_flux"] = r_.pop(k) / norm
        out["exemplars"] = _exemplars(rows, chain, n, ct)
    return out


def _exemplars(rows, chain, n, ct) -> dict:
    """Frozen selection: largest |circulation|, largest |affinity|, largest |circulation| against its affinity."""
    if not rows:
        return {}
    E = edges(n)

    def describe(row):
        A, C, D, e, f, *states, role = row
        b0, b1, b2, b3 = states
        return {
            "affinity": A, "circulation": C, "degree_difference_far_endpoints": D, "role": role,
            "slots": [list(E[e]), list(E[f])], "orientation": "form e, form f, dissolve e, dissolve f from the base state",
            "states": [int(chain.states[s]) for s in states],
            "stationary_ct": [float(ct[s]) for s in states],
            "forward_rates": [float(chain.W[b0, e]), float(chain.W[b1, f]), float(chain.W[b2, e]), float(chain.W[b3, f])],
            "reverse_rates": [float(chain.W[b0, f]), float(chain.W[b3, e]), float(chain.W[b2, f]), float(chain.W[b1, e])],
        }

    out = {"max_circulation": describe(max(rows, key=lambda r: (abs(r[1]), r[3], r[4], r[5]))), "max_affinity": describe(max(rows, key=lambda r: (abs(r[0]), r[3], r[4], r[5])))}
    counter = [r for r in rows if abs(r[0]) > 1e-12 and r[0] * r[1] < 0]
    out["max_counter_circulation"] = describe(max(counter, key=lambda r: (abs(r[1]), r[3], r[4], r[5]))) if counter else None
    return out


# --- partner-frame event order --------------------------------------------------------------


def partner_frame(chain, n: int, jump: np.ndarray) -> dict:
    """Consecutive events on adjacent slots, classified by sgn(deg(far end of second) - deg(far end of first)).

    D is computed with the two slots' own bits removed, so it is the same for a
    pair and its time reverse with the sign flipped; a reversible chain gives 0.
    Index = sum p * sgn(D) * chi, chi = +1 for (F,F) and (D,D), -1 for (F,D) and
    (D,F). In HELD the handover steps FPFA, FADP, DPDA, DAFP all contribute +.
    """
    E = edges(n)
    P = chain.W / chain.rates[:, None]
    deg = _degrees(chain, n)
    bits = _bits(chain)
    index = 0.0
    by_class = {"D>0": 0.0, "D=0": 0.0}
    pair_mass = 0.0
    zero_mass = 0.0
    for e, f in itertools.permutations(range(chain.n_slots), 2):
        shared = set(E[e]) & set(E[f])
        if not shared:
            continue
        (p,) = shared
        q = E[e][0] if E[e][1] == p else E[e][1]
        r = E[f][0] if E[f][1] == p else E[f][1]
        y = np.arange(len(chain.states))
        ye = chain.T[:, e]
        ok = (ye >= 0) & (P[:, e] > 0)
        y, ye = y[ok], ye[ok]
        prob = jump[y] * P[y, e] * P[ye, f]
        D = (deg[y, r] - bits[y, f]) - (deg[y, q] - bits[y, e])
        chi = np.where(bits[y, e] == bits[ye, f], 1.0, -1.0)
        index += float((prob * np.sign(D) * chi).sum())
        pair_mass += float(prob.sum())
        zero_mass += float(prob[D == 0].sum())
        by_class["D>0"] += float((prob * chi)[D > 0].sum())
    return {"adjacent_pair_probability": pair_mass, "index": index, "probability_d_zero": zero_mass, "signed_chi_mass_d_positive": by_class["D>0"]}


def partner_frame_reference(chain, n: int, jump: np.ndarray) -> float:
    """Loop reference for the partner index (independent implementation)."""
    E = edges(n)
    P = chain.W / chain.rates[:, None]
    total = 0.0
    for i, s in enumerate(chain.states):
        s = int(s)
        nbr = lambda v, st: sum(1 for u in range(n) if u != v and (st >> E.index((min(u, v), max(u, v)))) & 1)
        for e in range(chain.n_slots):
            j = int(chain.T[i, e])
            if j < 0 or P[i, e] <= 0:
                continue
            for f in range(chain.n_slots):
                if f == e or not (set(E[e]) & set(E[f])) or P[j, f] <= 0:
                    continue
                (p,) = set(E[e]) & set(E[f])
                q = E[e][0] if E[e][1] == p else E[e][1]
                r = E[f][0] if E[f][1] == p else E[f][1]
                cleared = s & ~(1 << e) & ~(1 << f)
                D = nbr(r, cleared) - nbr(q, cleared)
                chi = 1.0 if ((s >> e) & 1) == ((int(chain.states[j]) >> f) & 1) else -1.0
                total += jump[i] * P[i, e] * P[j, f] * float(np.sign(D)) * chi
    return total


# --- matched dissolution ----------------------------------------------------------------------


def hit_probabilities(chain, horizons=HORIZONS) -> dict[int, np.ndarray]:
    """u_H[y, f] = probability that slot f toggles at least once within H jump events from y."""
    P = chain.W / chain.rates[:, None]
    valid = chain.T >= 0
    target = np.where(valid, chain.T, 0)
    Pv = np.where(valid, P, 0.0)
    slots = chain.n_slots
    u = np.zeros((len(chain.states), slots))
    out = {}
    for h in range(1, max(horizons) + 1):
        new = np.zeros_like(u)
        for f in range(slots):
            acc = Pv[:, f].copy()
            for e in range(slots):
                if e != f:
                    acc += Pv[:, e] * u[target[:, e], f]
            new[:, f] = acc
        u = new
        if h in horizons:
            out[h] = u.copy()
    return out


def hit_reference_exact(chain, y: int, f: int, horizon: int) -> float:
    """Exact recursive enumeration without multiplicity: sum over first-hit paths."""
    P = chain.W / chain.rates[:, None]

    def go(state: int, h: int) -> float:
        if h == 0:
            return 0.0
        acc = 0.0
        for e in range(chain.n_slots):
            t = int(chain.T[state, e])
            if t < 0 or P[state, e] <= 0:
                continue
            acc += P[state, e] * (1.0 if e == f else go(t, h - 1))
        return acc

    return go(y, horizon)


def relation_class(n: int, mode: str, g: int, f: int) -> str:
    E = edges(n)
    shared = set(E[g]) & set(E[f])
    k = slot_classes(n, mode)
    rel = "disjoint" if not shared else ("adj@src" if (mode == "HELD" and next(iter(shared)) in SOURCE) else ("adj@prb" if mode == "HELD" else "adjacent"))
    return f"{k[g]}->{k[f]}:{rel}"


def matched_dissolution(chain, n: int, mode: str, jump: np.ndarray) -> dict:
    E = edges(n)
    P = chain.W / chain.rates[:, None]
    bits = _bits(chain)
    k = slot_classes(n, mode)
    u = hit_probabilities(chain)
    groups: dict[str, dict] = {}
    for g in range(chain.n_slots):
        if k[g] == "S":
            continue
        X = np.nonzero((bits[:, g] == 1) & (chain.T[:, g] >= 0))[0]
        if not len(X):
            continue
        Xm = chain.T[X, g]
        w = jump[X]
        if w.sum() <= 0:
            continue
        w = w / w.sum()
        dissolvable = chain.W[X, g] > 0
        den_prec = float((jump[X] * P[X, g]).sum())
        for f in range(chain.n_slots):
            if f == g:
                continue
            action = np.where(bits[X, f] == 0, "F", "D")
            for act in ("F", "D"):
                sel = action == act
                if not sel.any():
                    continue
                key = f"{relation_class(n, mode, g, f)}:{act}"
                G = groups.setdefault(key, {"mass": 0.0, "enabled": 0.0, "disabled": 0.0, "both_zero": 0.0, "rate_lr": 0.0, "rate_mass": 0.0, "rate_pos": 0.0, "rate_neg": 0.0, "jump_lr": 0.0, "norm_lr": 0.0, "du": {h: 0.0 for h in HORIZONS}, "du_pos": {h: 0.0 for h in HORIZONS}, "du_neg": {h: 0.0 for h in HORIZONS}, "prec_num": 0.0, "prec_den": 0.0, "prec_base": 0.0, "dissolvable_mass": 0.0, "pairs": 0})
                xs, xm, ws = X[sel], Xm[sel], w[sel]
                Wx, Wm = chain.W[xs, f], chain.W[xm, f]
                G["pairs"] += 1
                G["mass"] += float(ws.sum())
                G["dissolvable_mass"] += float(ws[dissolvable[sel]].sum())
                G["enabled"] += float(ws[(Wx == 0) & (Wm > 0)].sum())
                G["disabled"] += float(ws[(Wx > 0) & (Wm == 0)].sum())
                G["both_zero"] += float(ws[(Wx == 0) & (Wm == 0)].sum())
                both = (Wx > 0) & (Wm > 0)
                if both.any():
                    lr = np.log(Wm[both] / Wx[both])
                    jl = np.log(P[xm[both], f] / P[xs[both], f])
                    wb = ws[both]
                    G["rate_lr"] += float((wb * lr).sum())
                    G["jump_lr"] += float((wb * jl).sum())
                    G["norm_lr"] += float((wb * (jl - lr)).sum())
                    G["rate_mass"] += float(wb.sum())
                    G["rate_pos"] += float(wb[lr > 1e-12].sum())
                    G["rate_neg"] += float(wb[lr < -1e-12].sum())
                for h in HORIZONS:
                    d = u[h][xm, f] - u[h][xs, f]
                    G["du"][h] += float((ws * d).sum())
                    G["du_pos"][h] += float(ws[d > 1e-12].sum())
                    G["du_neg"][h] += float(ws[d < -1e-12].sum())
                G["prec_num"] += float((jump[xs] * P[xs, g] * P[xm, f]).sum())
                G["prec_den"] += den_prec * float(sel.mean())
                G["prec_base"] += float((jump * P[:, f]).sum())
    out = {}
    for key, G in sorted(groups.items()):
        m = G["mass"] or 1.0
        rm = G["rate_mass"]
        prec = (G["prec_num"] / G["prec_den"]) / (G["prec_base"] / G["pairs"]) if G["prec_den"] > 0 and G["prec_base"] > 0 else None
        mean_rate_lr = G["rate_lr"] / rm if rm > 0 else None
        mean_norm = G["norm_lr"] / rm if rm > 0 else None
        mechanisms = []
        if G["enabled"] > 0:
            mechanisms.append("strict_enabling")
        if G["disabled"] > 0:
            mechanisms.append("strict_disabling")
        if mean_rate_lr is not None and abs(mean_rate_lr) > 1e-9:
            mechanisms.append("rate_facilitation" if mean_rate_lr > 0 else "rate_suppression")
        if mean_norm is not None and abs(mean_norm) > 1e-9 and (mean_rate_lr is None or abs(mean_norm) > abs(mean_rate_lr)):
            mechanisms.append("normalisation_dominated")
        d8 = G["du"][max(HORIZONS)] / m
        if abs(d8) > 1e-9:
            mechanisms.append("passage_raised" if d8 > 0 else "passage_lowered")
        out[key] = {
            "both_zero_share": G["both_zero"] / m,
            "conditioning_pairs": G["pairs"],
            "disabled_share": G["disabled"] / m,
            "dissolvable_share": G["dissolvable_mass"] / m,
            "enabled_share": G["enabled"] / m,
            "mean_jump_log_ratio": G["jump_lr"] / rm if rm > 0 else None,
            "mean_normalisation_log_ratio": mean_norm,
            "mean_rate_log_ratio": mean_rate_lr,
            "mechanisms": mechanisms,
            "passage_delta": {str(h): G["du"][h] / m for h in HORIZONS},
            "passage_raised_share": {str(h): G["du_pos"][h] / m for h in HORIZONS},
            "passage_lowered_share": {str(h): G["du_neg"][h] / m for h in HORIZONS},
            "precedence_ratio": prec,
            "rate_raised_share": G["rate_pos"] / m,
            "rate_lowered_share": G["rate_neg"] / m,
        }
    return out


def one_way(chain) -> dict:
    valid = chain.T >= 0
    count = 0
    mass_states = set()
    for e in range(chain.n_slots):
        m = valid[:, e] & (chain.W[:, e] > 0)
        rev = np.zeros(len(chain.states), dtype=bool)
        rev[m] = chain.W[chain.T[m, e], e] <= 0
        count += int(rev.sum())
    return {"one_way_transitions": count}


# --- one cell ------------------------------------------------------------------------------


def analyse_item(item: dict, *, with_trajectories: bool = True, checks: bool = True, on_main=None) -> tuple[dict, dict | None]:
    n, mode, family, grade = item["n"], item["mode"], item["family"], item["grade"]
    components = FAMILIES[family][grade]
    started = time.perf_counter()
    full, kernel_timing = gtkernel.reachable_chain(n, mode, components)
    start = gtobs.start_index(full, n, mode)
    regime = gtobs.class_regime(full, start)
    chain, class_note, start_in = full, "reachable class from the declared start is recurrent", start
    closed = None
    if regime["regime"] != "recurrent":
        closed = terminal_classes(full)
        nonabs = [c for c in closed if len(c) > 1]
        class_note = f"reachable class not recurrent ({regime['regime']}): {len(closed)} closed classes, sizes {[len(c) for c in closed]}"
        if len(nonabs) == 1 and len(closed) == 1:
            chain = restrict(full, nonabs[0])
            start_in = 0
            class_note += "; analysing the unique closed class"
    stat = gtobs.stationary(chain, start_in, cross_check=True) if gtobs.class_regime(chain, start_in)["regime"] == "recurrent" else None
    result, trajectories = gtobs.analyse(chain, family=family, grade=grade, n=n, mode=mode, families=FAMILIES, item_id=item["item_id"], round_id=ROUND_ID, with_trajectories=with_trajectories and chain is full, stationary_override=stat, start=start_in)
    if stat is not None and not stat.get("resolved") and stat.get("reason") == "zero total rate in the class":
        result["regime"] = "arrested"
        class_note += "; arrested: a state of the class admits no event"
    result["class_note"] = class_note
    result["reachable_states_from_start"] = len(full.states)
    result["closed_class_sizes"] = [len(c) for c in closed] if closed is not None else None
    result["kernel_timing"] = kernel_timing
    result["spectrum_status"] = "unavailable: not computed by gtobs; not zero"
    block: dict = {"analysis_version": ANALYSIS_VERSION, "sigma": sigma(components), "hard_component": has_hard(components), "one_way": one_way(chain)}
    resolved = stat is not None and stat.get("resolved")
    t0 = time.perf_counter()
    block["squares"] = square_census(chain, n, mode, components, stat["ct"] if resolved else None)
    if resolved:
        block["partner_frame"] = partner_frame(chain, n, stat["jump"])
        if mode == "HELD":
            block["handover"] = gte1.handover_statistics(gtobs.event_pattern_probabilities(chain, stat["jump"], n, mode))
        block["matched_dissolution"] = matched_dissolution(chain, n, mode, stat["jump"])
    block["seconds"] = time.perf_counter() - t0
    result["e2a"] = block
    result["timings"]["main_total"] = time.perf_counter() - started
    if on_main is not None:
        on_main(result, trajectories)
    if checks:
        t0 = time.perf_counter()
        block["checks"] = numerical_checks(item, chain, start_in, stat if resolved else None)
        result["timings"]["checks"] = time.perf_counter() - t0
    return result, trajectories


def numerical_checks(item: dict, chain, start: int, stat: dict | None) -> dict:
    from rs_constraint_lab import gtobs_validate

    n, mode = item["n"], item["mode"]
    out: dict = {"kernel_sample": gte1.kernel_sample_check(item, chain, start, families=FAMILIES, round_id=ROUND_ID)}
    out["affinity_reference"] = affinity_reference(item, chain)
    if stat is None:
        return out
    out["long_double_residual"] = gte1.long_double_residual(chain, stat["jump"])
    law = gtobs_validate.gth_stationary(chain)
    out["gth"] = {"ct": gte1._law_difference(stat["ct"], law["ct"]), "jump": gte1._law_difference(stat["jump"], law["jump"])}
    pf = partner_frame(chain, n, stat["jump"])["index"]
    out["partner_frame_reference_difference"] = abs(pf - partner_frame_reference(chain, n, stat["jump"]))
    rng = np.random.default_rng(int(hashlib.sha256(f"{ROUND_ID}:hit:{item['item_id']}".encode()).hexdigest()[:16], 16))
    u = hit_probabilities(chain, horizons=(1, 2, 3))
    worst = 0.0
    for _ in range(12):
        y = int(rng.integers(len(chain.states)))
        f = int(rng.integers(chain.n_slots))
        for h in (1, 2, 3):
            worst = max(worst, abs(u[h][y, f] - hit_reference_exact(chain, y, f, h)))
    out["passage_reference_max_difference"] = worst
    return out


def affinity_reference(item: dict, chain, samples: int = 120) -> dict:
    """Signed affinities of seeded intact squares recomputed from the rule strings with exact Fractions."""
    from rs_constraint_lab.constraints import Choreography
    from rs_constraint_lab.weights import alphabet_factors

    n, mode, family, grade = item["n"], item["mode"], item["family"], item["grade"]
    factors = alphabet_factors("W4")
    choreography = Choreography(0, 0, gte0a.rules_for(family, grade, n, mode, FAMILIES))

    def rate(state: int, e: int) -> Fraction:
        w = Fraction(1)
        for c in choreography.active(state, (), {}):
            if c.matches(state, e):
                w *= factors[c.weight]
        return w

    rng = np.random.default_rng(int(hashlib.sha256(f"{ROUND_ID}:affinity:{item['item_id']}".encode()).hexdigest()[:16], 16))
    states = set(int(s) for s in chain.states)
    E = edges(n)
    sg = sigma(FAMILIES[family][grade])
    worst = 0.0
    checked = 0
    tries = 0
    while checked < samples and tries < samples * 50:
        tries += 1
        x = int(chain.states[int(rng.integers(len(chain.states)))])
        e, f = (int(v) for v in rng.choice(chain.n_slots, size=2, replace=False))
        if (x >> e) & 1 or (x >> f) & 1:
            continue
        quad = [x, x | 1 << e, x | 1 << e | 1 << f, x | 1 << f]
        if any(s not in states for s in quad):
            continue
        fw = [rate(quad[0], e), rate(quad[1], f), rate(quad[2], e), rate(quad[3], f)]
        bw = [rate(quad[0], f), rate(quad[3], e), rate(quad[2], f), rate(quad[1], e)]
        if min(fw + bw) == 0:
            continue
        A = sum(math.log(v) for v in fw) - sum(math.log(v) for v in bw)
        shared = set(E[e]) & set(E[f])
        if shared:
            (p,) = shared
            q = E[e][0] if E[e][1] == p else E[e][1]
            r = E[f][0] if E[f][1] == p else E[f][1]
            deg = lambda v: sum(1 for i, (a, b) in enumerate(E) if v in (a, b) and (x >> i) & 1)
            pred = sg * (deg(r) - deg(q))
        else:
            pred = 0.0
        worst = max(worst, abs(A - pred))
        checked += 1
    return {"checked_squares": checked, "max_abs_difference_to_formula": worst}


def check_problems(result: dict) -> list[str]:
    problems = []
    st = result.get("stationary") or {}
    if result.get("regime") != "recurrent":
        problems.append(f"regime {result.get('regime')}")
        return problems
    if not st.get("resolved"):
        return [f"stationary unresolved: {st.get('reason')}"]
    if st["residual"] > gtobs.STATIONARY_RESIDUAL_TOLERANCE:
        problems.append("stationary residual")
    if (result.get("symmetry_max_abs_difference") or 0.0) > gte0a.SYMMETRY_TOLERANCE:
        problems.append("symmetry")
    if (result.get("autocorrelation_diagnostics") or {}).get("cap_reached"):
        problems.append("autocorrelation cap reached")
    checks = result["e2a"].get("checks")
    if checks is None:
        return problems + ["numerical checks not completed"]
    ks = checks["kernel_sample"]
    if ks["max_relative_weight_difference"] > gte1.KERNEL_RELATIVE_TOLERANCE or ks["zero_pattern_mismatches"] or ks["target_mismatches"]:
        problems.append("kernel sample check")
    if checks["affinity_reference"]["max_abs_difference_to_formula"] > 1e-12:
        problems.append("affinity reference (rule strings) differs from the formula")
    ld = checks["long_double_residual"]
    if ld["zero_mass_states"]:
        problems.append("zero-mass reachable states")
    if ld["max_relative"] is not None and ld["max_relative"] > gte1.RESIDUAL_MAX_RELATIVE:
        problems.append("per-entry relative residual")
    for clock in ("ct", "jump"):
        g = checks["gth"][clock]
        if g["l1"] > gte1.REFEREE_L1 or (g["max_relative"] or 0.0) > gte1.REFEREE_MAX_RELATIVE:
            problems.append(f"gth {clock}")
    if checks["partner_frame_reference_difference"] > 1e-12:
        problems.append("partner-frame reference")
    if checks["passage_reference_max_difference"] > 1e-12:
        problems.append("passage reference")
    return problems


# --- assembly ------------------------------------------------------------------------------


def compact_row(r: dict) -> dict:
    b = r.get("e2a", {})
    row = {"class_note": r.get("class_note"), "family": r["family"], "grade": r["grade"], "hard": b.get("hard_component"), "mode": r["mode"], "n": r["n"], "one_way_transitions": (b.get("one_way") or {}).get("one_way_transitions"), "reachable_states": r.get("reachable_states"), "regime": r.get("regime"), "sigma": b.get("sigma")}
    sq = b.get("squares") or {}
    row.update({"broken_squares": sq.get("broken_squares"), "formula_max_abs_error": sq.get("formula_max_abs_error"), "intact_squares": sq.get("intact_squares")})
    if r.get("regime") != "recurrent" or not (r.get("stationary") or {}).get("resolved"):
        return row
    rev = r["reversibility"]
    row.update({
        "entropy_production_per_event": rev["entropy_production_per_event"],
        "event_order_asymmetry": r["event_order"]["pattern_asymmetry"],
        "expected_edges": r["occupancy_ct"]["expected_edges"],
        "hub_frame_asymmetry": r["hub_frame"]["event_order"]["pattern_asymmetry"],
        "irreversible_flux_fraction": rev["irreversible_flux_fraction"],
        "max_square_affinity": rev["max_square_affinity"],
        "partner_index": b["partner_frame"]["index"],
        "partner_pair_probability": b["partner_frame"]["adjacent_pair_probability"],
    })
    roles = sq.get("roles", {})
    adj = {k: v for k, v in roles.items() if k != "disjoint"}
    tot = sum(v["circulation_abs_per_total_flux"] for v in adj.values())
    row["adjacent_circulation_per_flux"] = tot
    row["circulation_aligned_share"] = (sum(v["circulation_aligned_abs_per_total_flux"] for v in adj.values()) / tot) if tot > 0 else None
    row["circulation_counter_share"] = (sum(v["circulation_counter_abs_per_total_flux"] for v in adj.values()) / tot) if tot > 0 else None
    row["circulation_zero_affinity_share"] = (sum(v["circulation_on_zero_affinity_abs_per_total_flux"] for v in adj.values()) / tot) if tot > 0 else None
    if r["mode"] == "HELD":
        row["handover_index"] = b["handover"]["index_adjacent"]
        row["handover_forward_steps"] = b["handover"]["forward_oriented_adjacent_steps"]
        row["attachment_fraction_ct"] = r["held_continuous"]["attachment_fraction"]
        row["null_attachment_fraction"] = r["held_continuous"]["null_attachment_fraction"]
        pa = roles.get("AP@prb", {})
        row["pa_squares"] = pa.get("squares")
        row["pa_negative_degree_difference"] = pa.get("degree_difference_negative")
        row["pa_circulation_signed_per_flux"] = pa.get("circulation_signed_oriented_per_total_flux")
    return row


SIGMA_ZERO_CELLS = (("NULL", "none"), ("CLOSEW", "weak_favour"), ("EXCL", "prohibit"), ("PFD", "weak_suppress+weak_suppress"), ("PFD", "weak_favour+weak_favour"))
RATE_SYMMETRIC_CELLS = (("NULL", "none"), ("PFD", "weak_suppress+weak_suppress"), ("PFD", "weak_favour+weak_favour"))


def assemble(results: dict[str, dict]) -> dict:
    rows = {k: compact_row(r) for k, r in results.items()}
    checks = {}
    for key, r in results.items():
        b = r.get("e2a", {})
        sq = b.get("squares") or {}
        checks[f"I1-{key}"] = {"holds": (sq.get("formula_max_abs_error") or 0.0) <= 1e-12, "formula_max_abs_error": sq.get("formula_max_abs_error"), "intact_squares": sq.get("intact_squares")}
        checks[f"I2-{key}"] = {"holds": (sq.get("disjoint_max_abs_affinity") or 0.0) <= 1e-12, "disjoint_max_abs_affinity": sq.get("disjoint_max_abs_affinity")}
        fam = (r["family"], r["grade"])
        row = rows[key]
        if fam in SIGMA_ZERO_CELLS and "irreversible_flux_fraction" in row:
            vals = [row["irreversible_flux_fraction"], abs(row["partner_index"]), row["hub_frame_asymmetry"]] + ([abs(row["handover_index"])] if r["mode"] == "HELD" else [])
            checks[f"I3-{key}"] = {"holds": max(vals) <= 1e-9, "max_value": max(vals)}
        if fam in RATE_SYMMETRIC_CELLS and r.get("class_table"):
            uniform = 1.0 / r["reachable_states"]
            l1 = sum(abs(t["ct"] - t["orbit_size"] * uniform) for t in r["class_table"])
            checks[f"I4-{key}"] = {"holds": l1 <= 1e-9, "l1_to_uniform": l1}
        if r["mode"] == "HELD" and r["n"] == 5 and "pa_negative_degree_difference" in row:
            checks[f"I5-{key}"] = {"holds": (row["pa_negative_degree_difference"] or 0) == 0, "pa_negative_degree_difference": row["pa_negative_degree_difference"]}
        problems = check_problems(r)
        if r.get("regime") == "recurrent":
            checks[f"Z5-{key}"] = {"holds": not problems, "problems": problems}
    sign_table = []
    for key, row in rows.items():
        if "partner_index" not in row:
            continue
        s = row["sigma"]
        sign_table.append({"cell": key, "sigma": s, "partner_index": row["partner_index"], "handover_index": row.get("handover_index"), "flux": row["irreversible_flux_fraction"],
                           "partner_sign_matches_sigma": None if abs(s) <= SIGMA_ZERO_TOLERANCE else (np.sign(row["partner_index"]) == np.sign(s) if abs(row["partner_index"]) > 1e-12 else "partner_zero"),
                           "handover_sign_matches_sigma": None if abs(s) <= SIGMA_ZERO_TOLERANCE or row.get("handover_index") is None else (np.sign(row["handover_index"]) == np.sign(s) if abs(row["handover_index"]) > 1e-12 else "handover_zero")})
    for t in sign_table:
        for k in ("partner_sign_matches_sigma", "handover_sign_matches_sigma"):
            if isinstance(t[k], np.bool_):
                t[k] = bool(t[k])
    dissolution = {k: r["e2a"]["matched_dissolution"] for k, r in results.items() if "matched_dissolution" in r.get("e2a", {})}
    mech_summary = {}
    for k, groups in dissolution.items():
        tally: dict[str, int] = {}
        for g in groups.values():
            for m in g["mechanisms"]:
                tally[m] = tally.get(m, 0) + 1
        mech_summary[k] = tally
    return {"cell_rows": rows, "frozen_expectations": checks, "mechanism_tally": mech_summary, "sigma_sign_table": sign_table}


# --- plan and execution ---------------------------------------------------------------------

PLAN_RELPATH = "gravity-time/plans/round-e2a-plan.json"
GENERATED_RELPATH = "gravity-time/generated/round-e2a"
TABLES_RELPATH = "gravity-time/reports/round-e2a-tables.json"
WATCHDOG_SECONDS = {5: 900, 6: 900}
ROUND_WALL_CAP_SECONDS = 2 * 3600
WORKERS = 4
ONTOLOGY = {"G": 0, "H": 0, "L": 0, "N": [5, 6], "O": 2, "S": 0, "grammar": "ordinary pair DSL"}
REFERENCE_FILES = (
    "research-methods/open-thetical-research.md",
    "gravity-time/provenance/prompts/GT-P005-agent-input.md",
    "gravity-time/docs/e2-coverage-audit.md",
    "gravity-time/docs/e2-formal-mechanism.md",
    "gravity-time/reports/gt-e1-report.md",
    "gravity-time/reports/gt-e1-reflection.md",
    "gravity-time/reports/round-e1-tables.json",
    "gravity-time/reports/round-e0a-tables.json",
    "gravity-time/reports/round-e0b-tables.json",
    "gravity-time/plans/round-e1-plan.json",
    "constraint-lab/formal/open-problems.md",
    "constraint-lab/docs/scientific-plan-discipline.md",
)


def published_overlap() -> dict[str, str]:
    """Round cells whose (mode, N, components) were executed and published in E0A, E0B or E1."""
    known = {}
    for fams, round_name, sizes in ((gte0a.FAMILIES, "E0A", (5, 6)), (gte0b.FAMILIES, "E0B", (5, 6)), (gte1.FAMILIES, "E1", (5, 6, 7))):
        for fam, grades in fams.items():
            for grade, comps in grades.items():
                for n in sizes:
                    for mode in (("HELD", "FREE") if round_name != "E1" else ("HELD",)):
                        known.setdefault((mode, n, tuple(map(tuple, comps))), f"{round_name} {mode}-N{n}-{fam}-{grade}")
    out = {}
    for it in items():
        key = (it["mode"], it["n"], tuple(map(tuple, FAMILIES[it["family"]][it["grade"]])))
        if key in known:
            out[it["item_id"]] = known[key]
    return out


def prepare_plan(repo: Path) -> dict:
    from rs_constraint_lab.durable import sha256_file
    from rs_constraint_lab.explore08 import plan_hash

    cells = items()
    exposed = published_overlap()
    document = {
        "analysis_only": True,
        "analysis_version": ANALYSIS_VERSION,
        "chosen_because": "GT-E1 reflection section 6 (handover mechanism recommended) and GT-P005; coverage audit gravity-time/docs/e2-coverage-audit.md",
        "clocks": {"continuous": "pi_ct = pi_jump / R; currents and circulations per unit time", "jump": "pi_jump; event-order, partner frame, matched-dissolution weights and passage horizons in jump events"},
        "comparisons": {
            "C1_sigma_versus_orientation": "for every irreversible cell, the sign of sigma against the sign of the partner-frame index and (HELD) the handover index; no expectation beyond the local identity",
            "C2_circulation_alignment": "share of adjacent-square circulation (|C| mass) aligned with, counter to, or on squares without local affinity",
            "C3_matched_dissolution": "per relation class and action, the mechanism list (strict enabling/disabling, rate facilitation/suppression, normalisation-dominated, passage raised/lowered at H=8) and the precedence ratio beside the intervention effects",
            "C4_frames": "partner-frame index against class-free and hub-frame event-order asymmetry, HELD and FREE",
            "C5_n5_n6": "HELD attachment/probe squares with negative far-endpoint degree difference (impossible at N=5 by I5) and their circulation share at N=6",
            "C6_grade_ladder": "PATHF and PATHH across prohibit, strong_suppress, weak_suppress, weak_favour, strong_favour: flux, density, partner index, handover index",
            "C7_hard_support": "EXCL, EXPH, EXPF and the two prohibit path cells: closed-class structure, one-way transitions, strict-enabling shares, and whether strict enabling coexists with circulation",
            "no_aggregate_score": "no handover-strength or relevance score is formed; cells are not ranked",
        },
        "controls_and_identities": {
            "I1_square_formula": "on every intact square of every cell, |A - sigma*(deg_x(r) - deg_x(q))| <= 1e-12 (theorem, docs/e2-formal-mechanism.md; checked pre-freeze on synthetic factor tables at N=4, 5)",
            "I2_disjoint_squares": "every intact square on disjoint slots has |A| <= 1e-12 (corollary)",
            "I3_sigma_zero": "cells with sigma = 0 (NULL, CLOSEW, EXCL, PFD ws+ws, PFD wf+wf): irreversible flux, |partner index|, hub-frame asymmetry and (HELD) |handover index| <= 1e-9 (corollary of I1 plus Kolmogorov, where the class has no one-way transitions)",
            "I4_rate_symmetric": "NULL, PFD ws+ws, PFD wf+wf: form and dissolve factors are equal on every pair, so pi is uniform on the class (class-level L1 <= 1e-9)",
            "I5_held_n5": "at HELD N=5 no attachment/probe square has a negative far-endpoint degree difference (a source vertex has the two other source vertices; a probe has at most two other neighbours besides the pair), so every such square has the sign of sigma",
            "Z5_numerical": "stationary two-start agreement, residual, symmetry, autocorrelation cap, kernel sample (rule strings), affinity reference (rule strings, exact Fractions), long-double residual, GTH referee, partner-frame loop reference and passage path-enumeration reference; tolerances as E1 (gte1) and 1e-12 for the new references",
            "separation_note": "I1-I5 are identities; none predicts the sign or size of a stationary current, an event-order index, a matched-dissolution effect or a passage probability",
        },
        "deliberate_omissions": {"free_n7_and_n7": "not run (GT-P005 boundary; no N=7)", "spectrum": "unavailable in every cell", "fine_grade_tuning": "grades are the W4 alphabet as listed; no interpolation", "new_primitives": "none; 'prohibit' and adj_form are existing grammar"},
        "estimands": "every gtobs channel, the square census, partner frame, matched dissolution and one-way structure of each cell, and C1-C7",
        "experiment_id": EXPERIMENT_ID,
        "families": {f: {g: {"components": [{"grade": cg, "kind": k} for k, cg in comps], "gradient": gte0a.is_gradient(f, FAMILIES), "hard_component": has_hard(comps), "sigma": sigma(comps)} for g, comps in grades.items()} for f, grades in FAMILIES.items()},
        "history": False,
        "horizons_jump_events": list(HORIZONS),
        "initial_conditions": "as E0: HELD starts at the source triangle, FREE at the empty graph; the reachable class from the start is analysed; if it is not recurrent and has exactly one closed class of more than one state, that class is analysed and the restriction is recorded; otherwise the cell is reported by its class structure only",
        "items": cells,
        "matched_dissolution_definition": "for every non-source slot g and every state x with g present whose partner x- = x without g is in the class: conditioning weight pi_jump(x) normalised over those x (an intervention instrument that removes g from a stationary state; not a claim that the model contains interventions). For every other slot f and action (form if f absent in x, else dissolve): strict enabling share (W(x,f)=0, W(x-,f)>0), strict disabling share, mean log rate ratio log W(x-,f)/W(x,f) where both positive, mean log jump-probability ratio and its normalisation part (jump minus rate), passage delta u_H(x-,f) - u_H(x,f) for H in {1,2,4,8} jump events with u_H the probability that f toggles at least once within H events, and the precedence ratio p(next event toggles f | dissolve g just executed) / p(an event toggles f). Grouped by slot class of g and f, adjacency and the shared vertex type",
        "meta_constraints": False,
        "method": {"name": "Open-Thetical Research", "path": "research-methods/open-thetical-research.md", "version": "1.0"},
        "mode": "B",
        "new_primitives": False,
        "numerical_policy": "gtobs stationary (two starts, relative stop), GTH referee on every cell (every class has at most 4,096 states), long-double per-entry residual, kernel sample check (rule strings, exact Fractions, 400 states), affinity reference (120 seeded intact squares from rule strings), partner-frame loop reference, passage path-enumeration reference (12 seeded (state, slot) pairs, H = 1, 2, 3); children single-threaded",
        "observables": {"gtobs": f"every channel of gtobs.analyse ({gtobs.OBSERVABLES_VERSION})", "round": "square census, partner frame, handover index (HELD), matched dissolution, one-way transitions, frozen exemplars (largest |circulation|, largest |affinity|, largest |circulation| against its affinity)", "trajectories": "illustrative, as E0, seeds sha256('round-e2a:<item_id>:<k>')[:16]"},
        "ontology": ONTOLOGY,
        "open_questions_without_prediction": [
            "Does the sign of every irreversible cell's partner-frame index (and HELD handover index) follow the sign of sigma, or do aggregated statistics cancel or reverse it anywhere?",
            "How much stationary circulation sits on squares with no local affinity, and how much runs against local affinity?",
            "When sigma < 0, is there a reversed stationary current of comparable size, or does saturation hide it (S1, S5)?",
            "Which cells show strict enabling by dissolution, and does strict enabling coexist with circulation or only with reversible dynamics?",
            "Does the observed precedence after a dissolution agree with the intervention effect, or is it a selection effect?",
            "Does the partner frame make FREE circulation legible where the class-free frame does not, and how does it compare with the hub frame?",
            "At HELD N=6, how much circulation sits on reversed attachment/probe squares?",
            "Anything not anticipated above.",
        ],
        "parameter_fit": False,
        "pre_freeze_exposure": {
            "published_cells_standard_channels": exposed,
            "note": "the cells listed have published standard gtobs/E0 channels; their square census, partner frame, matched-dissolution and one-way channels have never been computed. No other round cell was computed before freezing",
            "formula_fixtures": "the square formula was checked before freezing on synthetic factor tables (non-alphabet factors 0.13, 0.41, 2.7, 6.3 and 0) at N=4 and N=5, HELD and FREE, for four synthetic mixes; no round cell kernel or law was used",
            "engineering": "plumbing tests and a smoke run use synthetic N=4 cells (all 21 family-grades, HELD and FREE; N=4 is not a round size) and synthetic factor tables. The smoke run was read: among other things it showed one-way irreversibility without square affinity in FREE N=4 path_form prohibit (flux 0.12) and an arrested single state in HELD N=4 path_form prohibit. Timing used the published HELD N=6 CLOSEW cell (not a round cell; only costs read)",
            "reference_hashes": {rel: sha256_file(repo / rel) for rel in REFERENCE_FILES},
        },
        "programme": "GT",
        "prompt_id": PROMPT_ID,
        "question": "What makes relational changes occur in directionally ordered sequences, and when does dissolving a relation enable a later change rather than merely precede it?",
        "round_id": ROUND_ID,
        "sampling": f"exact census of {len(cells)} declared cells: five strata at N=5 in HELD and FREE, plus four HELD N=6 robustness cells",
        "schema": "rs-gt.e2a-plan/v1",
        "selection_rule": "strata chosen from the coverage audit: (S1) every W4 grade of each single path component; (S2) all four form/dissolve weak-grade pairs, which give sigma = -2 log 2, 0, 0, +2 log 2; (S3) the reversible gradient control, the null and the hard closure exclusion (strict support without path terms); (S4) hard closure exclusion plus each unsaturated path component; (S5) the strong adjacency suppression opposed to each weak path-form grade (one sigma<0, one sigma>0 comparator), fixed before results; (S6) HELD N=6 for the two published weak path cells and the two strong grades with sigma>0. Excluded: other closure/adjacency grades, three-component mixes, N=7, FREE N=6",
        "software": {"analysis_module": "rs_constraint_lab.gte2a", "numpy": np.__version__, "observables": gtobs.OBSERVABLES_VERSION, "python": __import__("platform").python_version()},
        "stochastic_trajectories": "illustrative_only",
        "stop_conditions": {"item": f"watchdog {WATCHDOG_SECONDS} seconds by N; a killed cell is recorded unresolved", "round": f"all items or the {ROUND_WALL_CAP_SECONDS}-second wall cap; then stop", "unresolved": "recorded as unresolved; no retuning", "amendment": "any change of cells or estimands after freeze stops the round for explicit amendment"},
        "tolerances": {"identity": 1e-9, "formula": 1e-12, "references": 1e-12, "sigma_zero": SIGMA_ZERO_TOLERANCE, "e1_numerical": "gte1 constants (referee 1e-10 L1 and 1e-8 relative; residual 1e-9; kernel 1e-12)"},
        "work_count": {"items": len(cells), "largest_state_space": 4096, "round_wall_cap_seconds": ROUND_WALL_CAP_SECONDS, "watchdog_seconds": {str(k): v for k, v in WATCHDOG_SECONDS.items()}, "workers": WORKERS, "estimate_note": "measured before freezing: synthetic N=4 cells 0.04-0.08 s; published HELD N=6 CLOSEW (not a round cell) 48 s at 312 MB, of which 47 s are the GTH referee and loop references. Round estimate: 42 N=5 cells at seconds each plus 4 N=6 cells at about 1 minute: under 10 minutes on 4 workers"},
    }
    document["plan_hash"] = plan_hash(document)
    return document


def require_execution(repo: Path, commit: str | None, *, require_remote: bool = True) -> dict:
    from rs_constraint_lab.explore08 import FrozenPlanError, remote_contains, require_frozen_plan

    plan = require_frozen_plan(repo, commit, PLAN_RELPATH, disk_path=repo / PLAN_RELPATH)
    if require_remote and not remote_contains(repo, commit or ""):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    if plan.get("items") != items() or plan.get("new_primitives") is not False or plan.get("ontology") != ONTOLOGY:
        raise FrozenPlanError("execution refused: E2A plan contract drifted")
    return plan


def execute_item(root: Path, item: dict) -> dict:
    import resource

    from rs_constraint_lab.durable import atomic_write_json

    started = time.perf_counter()

    def payload(result, status):
        return {"item": item, "item_id": item["item_id"], "peak_rss_mb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, "result": result, "status": status, "wall_seconds": time.perf_counter() - started}

    def on_main(result, trajectories):
        atomic_write_json(root / "items" / f"{item['item_id']}.partial.json", payload(result, "complete_checks_interrupted"))
        if trajectories is not None:
            atomic_write_json(root / "trajectories" / f"{item['item_id']}.json", trajectories)

    result, _ = analyse_item(item, on_main=on_main)
    final = payload(result, "complete")
    atomic_write_json(root / "items" / f"{item['item_id']}.json", final)
    partial = root / "items" / f"{item['item_id']}.partial.json"
    if partial.exists():
        partial.unlink()
    return final


def run(root: Path, plan: dict, *, workers: int = WORKERS, **kwargs) -> list[dict]:
    return gte1.run(root, plan, workers=workers, watchdogs=kwargs.pop("watchdogs", WATCHDOG_SECONDS), wall_cap=kwargs.pop("wall_cap", ROUND_WALL_CAP_SECONDS), module="rs_constraint_lab.gte2a", **kwargs)


def publish(root: Path, plan: dict, out: Path, *, frozen_plan_commit: str) -> str:
    from rs_constraint_lab.durable import atomic_write_json, canonical_json, read_json, sha256_bytes

    records = {}
    for it in plan["items"]:
        path = root / "items" / f"{it['item_id']}.json"
        records[it["item_id"]] = read_json(path) if path.is_file() else {"item_id": it["item_id"], "status": "missing"}
    results = {k: v["result"] for k, v in records.items() if "result" in v}
    assembled = assemble(results)
    item_records = {k: {"numerical_problems": check_problems(results[k]) if k in results and results[k].get("regime") == "recurrent" else None, "peak_rss_mb": v.get("peak_rss_mb_parent_view", v.get("peak_rss_mb")), "status": v["status"], "stratum": next(it["stratum"] for it in plan["items"] if it["item_id"] == k), "wall_seconds": v.get("wall_seconds"), **({"interruption": v["interruption"]} if "interruption" in v else {})} for k, v in records.items()}
    payload = {
        "analysis_version": ANALYSIS_VERSION,
        "experiment_id": EXPERIMENT_ID,
        "frozen_analysis_plan_commit": frozen_plan_commit,
        "item_records": item_records,
        "plan_hash": plan["plan_hash"],
        "results": results,
        "round_id": ROUND_ID,
        "schema": "rs-gt.e2a-tables/v1",
        "status_counts": {s: sum(r["status"] == s for r in item_records.values()) for s in sorted({r["status"] for r in item_records.values()})},
        **assembled,
    }
    body = dict(payload)
    body["payload_sha256"] = sha256_bytes(canonical_json(payload).encode("utf-8"))
    atomic_write_json(out, body)
    return body["payload_sha256"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m rs_constraint_lab.gte2a")
    sub = parser.add_subparsers(dest="command", required=True)
    one = sub.add_parser("item")
    one.add_argument("--root", required=True)
    one.add_argument("--item-id", required=True)
    args = parser.parse_args(argv)
    from rs_constraint_lab.durable import read_json

    root = Path(args.root)
    plan = read_json(root / "plan.json")
    (item,) = [it for it in plan["items"] if it["item_id"] == args.item_id]
    if item not in items() and not plan.get("synthetic_fixture"):
        raise SystemExit("item is not in the E2A manifest")
    execute_item(root, item)
    return 0


if __name__ == "__main__":
    sys.exit(main())
