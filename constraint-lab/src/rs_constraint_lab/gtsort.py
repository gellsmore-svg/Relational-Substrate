"""GT-P008: witness algebra of held references and post hoc views of published E4 tables.

Nothing here builds a scientific kernel or computes a new E4/E5 cell.

* Template algebra: path and closure witness templates of a slot, their split
  into held / one-held / free classes, the permanent floor, and expectations
  under the NULL product law (held relations present, free relations
  independent with probability 1/2). Written independently of ``gte4a``.
* First-order (weak-coupling) coefficients: d(log odds)/d(epsilon) at
  epsilon = 0 for every factor written as exp(grade * epsilon); the
  continuous-clock value follows from the stationary balance identity
  (docs/e4-sorting-mechanism-derivation.md, S1 and S4), the jump-clock value
  adds Cov_0(x_e, q') / M.
* Post hoc views of ``round-e4a-tables.json`` and ``round-e4b-tables.json``,
  as defined (D1-D8) in docs/gt-p008-coverage-and-integrity-audit.md before
  they were computed. They are explanatory, not new evidence.

CLI: ``python -m rs_constraint_lab.gtsort write [--out PATH]``.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np

TABLES = {"e4a": "gravity-time/reports/round-e4a-tables.json", "e4b": "gravity-time/reports/round-e4b-tables.json"}
OUT_RELPATH = "gravity-time/reports/gt-p008-secondary-analyses.json"
ANALYSIS_VERSION = "gt-p008-sorting/v1"
LN2 = math.log(2.0)

# Held graphs (independent copy; tests check equality with gt0.SCAFFOLDS).
HELD = {
    "K2": ((0, 1),),
    "P3": ((0, 1), (1, 2)),
    "K3": ((0, 1), (0, 2), (1, 2)),
    "S4": ((0, 1), (0, 2), (0, 3)),
    "P4": ((0, 1), (1, 2), (2, 3)),
}
CELLS = {"e4a": (("K2", 5), ("K2", 6), ("P3", 5), ("P3", 6), ("K3", 5), ("K3", 6)), "e4b": (("S4", 6), ("P4", 6))}
FAMILY_GRADES = (
    ("NULL", "none"),
    ("PATHF", "weak_suppress"),
    ("PATHH", "weak_favour"),
    ("CSPH", "strong_favour+weak_favour"),
    ("PCOMP", "weak_favour+weak_favour"),
    ("CLOSEW", "weak_favour"),
)
# Within-reference contrasts: (lower-floor orbit L, higher-floor orbit H). P4 has
# equal floors; there L is the inner orbit by convention.
CONTRASTS = {"P3": ("1", "0+2"), "S4": ("0", "1+2+3"), "P4": ("1+2", "0+3")}


def pair(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)


def pairs(n: int) -> list[tuple[int, int]]:
    return list(itertools.combinations(range(n), 2))


def source(held) -> list[int]:
    return sorted({v for e in held for v in e})


def held_degree(held, v: int) -> int:
    return sum(v in e for e in held)


def path_templates(n: int, e: tuple[int, int]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """Ordered path witnesses (end, c, d) of slot e, as their two pair relations."""
    a, b = e
    out = []
    for end in (a, b):
        for c in range(n):
            if c in (a, b):
                continue
            for d in range(n):
                if d in (a, b) or d == c:
                    continue
                out.append((pair(end, c), pair(c, d)))
    return out


def closure_templates(n: int, e: tuple[int, int]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    a, b = e
    return [(pair(a, c), pair(b, c)) for c in range(n) if c not in (a, b)]


def template_classes(n: int, held, e) -> dict[str, int]:
    """Path templates of e by number of held relations: h2 (floor), h1, h0."""
    H = set(held)
    out = {"h2": 0, "h1": 0, "h0": 0}
    for p1, p2 in path_templates(n, e):
        k = (p1 in H) + (p2 in H)
        out[("h0", "h1", "h2")[k]] += 1
    return out


def floor_enumerated(n: int, held, s: int) -> int:
    probe = next(v for v in range(n) if v not in source(held))
    return template_classes(n, held, pair(probe, s))["h2"]


def floor_formula(held, s: int) -> int:
    """F1: sum over held neighbours c of s of (deg_H(c) - 1)."""
    nbrs = [b if a == s else a for a, b in held if s in (a, b)]
    return sum(held_degree(held, c) - 1 for c in nbrs)


def _present_probability(H: set, p: tuple[int, int]) -> Fraction:
    return Fraction(1) if p in H else Fraction(1, 2)


def e0_path(n: int, held, e) -> Fraction:
    """E_0[w_e] under the NULL product law."""
    H = set(held)
    return sum((_present_probability(H, p1) * _present_probability(H, p2) for p1, p2 in path_templates(n, e)), Fraction(0))


def e0_close(n: int, held, e) -> Fraction:
    H = set(held)
    return sum((_present_probability(H, p1) * _present_probability(H, p2) for p1, p2 in closure_templates(n, e)), Fraction(0))


def e0_path_attachment_formula(n: int, held, s: int) -> Fraction:
    """S3 closed form for an attachment slot (p, s): T/4 + D/2 + floor/4 + (N - 7) deg/4."""
    T = 2 * (n - 2) * (n - 3)
    D = 2 * len(held)
    return Fraction(T, 4) + Fraction(D, 2) + Fraction(floor_formula(held, s), 4) + Fraction((n - 7) * held_degree(held, s), 4)


# --- first-order coefficients -------------------------------------------------------------------
#
# Each factor is exp(g * eps) with g its grade (weak +-1, strong +-2); W4 has eps = ln 2.
# components: (kind, grade) with kind in path_form, path_dissolve, close_form.

COMPONENTS = {
    "NULL": (),
    "PATHF": (("path_form", -1),),
    "PATHH": (("path_dissolve", 1),),
    "CSPH": (("close_form", 2), ("path_dissolve", 1)),
    "PCOMP": (("path_form", 1), ("path_dissolve", 1)),
    "CLOSEW": (("close_form", 1),),
}


def kappa(family: str, n: int, held, e) -> Fraction:
    """Continuous clock: d log odds(x_e) / d eps at 0 = sum of g E_0[witnesses] (form) - (dissolve)."""
    out = Fraction(0)
    for kind, g in COMPONENTS[family]:
        mean = e0_path(n, held, e) if kind.startswith("path") else e0_close(n, held, e)
        out += g * mean if kind.endswith("form") else -g * mean
    return out


def slot_class(held, e) -> str:
    S = set(source(held))
    if e in set(held):
        return "H"
    inside = (e[0] in S) + (e[1] in S)
    return {2: "C", 1: "A", 0: "P"}[inside]


def free_slots(n: int, held) -> list[tuple[int, int]]:
    return [e for e in pairs(n) if e not in set(held)]


def orbit_representative(n: int, held, orbit_key: str) -> tuple[int, int]:
    s = int(orbit_key.split("+")[0])
    probe = next(v for v in range(n) if v not in source(held))
    return pair(probe, s)


def margin_slope(family: str, n: int, held) -> float:
    """d(raw margin)/d eps at 0, raw margin = E[attachments]/E[free relations] - r0 (continuous clock)."""
    F = free_slots(n, held)
    A = [e for e in F if slot_class(held, e) == "A"]
    M = len(F)
    r0 = len(A) / M
    ka = sum(float(kappa(family, n, held, e)) for e in A)
    kf = sum(float(kappa(family, n, held, e)) for e in F)
    return (ka - r0 * kf) / (2.0 * M)


def _null_configurations(n: int, held) -> tuple[np.ndarray, list[tuple[int, int]], dict]:
    """All free configurations (uniform NULL law) as a 0/1 matrix over all pairs (held = 1)."""
    P = pairs(n)
    idx = {p: i for i, p in enumerate(P)}
    F = free_slots(n, held)
    m = len(F)
    codes = np.arange(1 << m, dtype=np.int64)
    X = np.zeros((1 << m, len(P)), dtype=np.int64)
    for j, f in enumerate(F):
        X[:, idx[f]] = (codes >> j) & 1
    for h in held:
        X[:, idx[h]] = 1
    return X, P, idx


def _witness_counts(X: np.ndarray, n: int, P, idx) -> tuple[np.ndarray, np.ndarray]:
    w = np.zeros_like(X)
    t = np.zeros_like(X)
    for i, e in enumerate(P):
        for p1, p2 in path_templates(n, e):
            w[:, i] += X[:, idx[p1]] * X[:, idx[p2]]
        for p1, p2 in closure_templates(n, e):
            t[:, i] += X[:, idx[p1]] * X[:, idx[p2]]
    return w, t


def jump_first_order(family: str, n: int, held) -> dict[tuple[int, int], float]:
    """d E_nu[x_e]/d eps at 0 for every free slot, nu = jump-chain law = pi q / E_pi[q].

    At eps = 0 the law is uniform and q = M, so the derivative is
    kappa_e / 4 + Cov_0(x_e, q') / M with q' = d q / d eps at 0.
    """
    X, P, idx = _null_configurations(n, held)
    w, t = _witness_counts(X, n, P, idx)
    F = free_slots(n, held)
    M = len(F)
    qd = np.zeros(X.shape[0])
    for f in F:
        i = idx[f]
        for kind, g in COMPONENTS[family]:
            wit = w[:, i] if kind.startswith("path") else t[:, i]
            if kind.endswith("form"):
                qd += g * wit * (1 - X[:, i])
            else:
                qd += g * wit * X[:, i]
    out = {}
    for f in F:
        x = X[:, idx[f]].astype(float)
        cov = float((x * qd).mean() - x.mean() * qd.mean())
        out[f] = float(kappa(family, n, held, f)) / 4.0 + cov / M
    return out


def closew_gibbs_orbits(n: int, held) -> dict[str, dict[str, float]]:
    """Independent CLOSEW law: pi proportional to 2^(#triangles); jump law nu ~ pi q."""
    X, P, idx = _null_configurations(n, held)
    tri = np.zeros(X.shape[0])
    for a, b, c in itertools.combinations(range(n), 3):
        tri += X[:, idx[(a, b)]] * X[:, idx[(a, c)]] * X[:, idx[(b, c)]]
    pi = np.exp2(tri - tri.max())
    pi /= pi.sum()
    _, t = _witness_counts(X, n, P, idx)
    F = free_slots(n, held)
    q = np.zeros(X.shape[0])
    for f in F:
        i = idx[f]
        q += np.where(X[:, i] == 1, 1.0, np.exp2(t[:, i]))
    nu = pi * q
    nu /= nu.sum()
    out = {}
    S = source(held)
    probe_set = [v for v in range(n) if v not in S]
    for clock, law in (("continuous", pi), ("jump", nu)):
        block = {}
        for orbit in _orbit_keys(n, held):
            verts = [int(v) for v in orbit.split("+")]
            slots = [idx[pair(p, s)] for s in verts for p in probe_set]
            block[orbit] = float(law @ X[:, slots].sum(axis=1)) / len(slots)
        out[clock] = block
    return out


def _automorphisms(held, S):
    H = set(held)
    for perm in itertools.permutations(S):
        m = dict(zip(S, perm))
        if {pair(m[a], m[b]) for a, b in H} == H:
            yield m


def _orbit_keys(n: int, held) -> list[str]:
    S = source(held)
    seen, keys = set(), []
    for s in S:
        if s in seen:
            continue
        orb = sorted({m[s] for m in _automorphisms(held, S)})
        seen.update(orb)
        keys.append("+".join(map(str, orb)))
    return keys


# --- post hoc views of published tables (D1-D8) --------------------------------------------------


def _load(repo: Path) -> dict[str, dict]:
    return {k: json.loads((repo / rel).read_text(encoding="utf-8")) for k, rel in TABLES.items()}


def _profile(tables: dict, scaffold: str, n: int, family: str, grade: str) -> dict:
    key = "e4b" if scaffold in ("S4", "P4") else "e4a"
    return tables[key]["comparisons"]["profiles"][f"HELD-{scaffold}-N{n}-{family}-{grade}"]


def _result(tables: dict, scaffold: str, n: int, family: str, grade: str) -> dict:
    key = "e4b" if scaffold in ("S4", "P4") else "e4a"
    return tables[key]["results"][f"HELD-{scaffold}-N{n}-{family}-{grade}"]


def _logit(p: float) -> float:
    return math.log(p / (1.0 - p))


def orbit_views(tables: dict) -> list[dict]:
    """D2-D5 per cell and orbit (continuous clock), with D6 coefficients."""
    rows = []
    for key in ("e4a", "e4b"):
        for scaffold, n in CELLS[key]:
            held = HELD[scaffold]
            for family, grade in FAMILY_GRADES:
                prof = _profile(tables, scaffold, n, family, grade)
                mean_rate = _result(tables, scaffold, n, family, grade)["mean_rate_ct"]
                for orbit, ct in prof["orbits"]["continuous"].items():
                    jp = prof["orbits"]["jump"][orbit]
                    occ, act = ct["attachment_occupancy_per_slot"], ct["attachment_activity_per_slot"]
                    J = act / 2.0
                    s = int(orbit.split("+")[0])
                    e = orbit_representative(n, held, orbit)
                    rows.append({
                        "cell": f"HELD-{scaffold}-N{n}-{family}-{grade}",
                        "scaffold": scaffold, "n": n, "family": family, "orbit": orbit,
                        "floor": floor_formula(held, s), "held_degree": held_degree(held, s),
                        "occ_ct": occ, "occ_jump": jp["attachment_occupancy_per_slot"],
                        "act_ct": act, "act_jump": jp["attachment_activity_per_slot"],
                        "flux_J": J,
                        "F_bar": J / (1.0 - occ), "D_bar": J / occ,
                        "sojourn_present": occ / J, "sojourn_absent": (1.0 - occ) / J,
                        "jump_activity_check": abs(jp["attachment_activity_per_slot"] - act / mean_rate),
                        "witness_means_ct": ct["witness_means_per_slot"],
                        "e0_path": float(e0_path(n, held, e)), "e0_close": float(e0_close(n, held, e)),
                        "kappa_ct": float(kappa(family, n, held, e)),
                    })
    return rows


FLOOR_ENTERS = {"PATHF": True, "PATHH": True, "CSPH": True}


def contrasts(tables: dict, rows: list[dict]) -> list[dict]:
    """D4 and D6: within-reference orbit contrasts, observed against floor term and first order."""
    by = {(r["cell"], r["orbit"]): r for r in rows}
    jump_cache: dict = {}
    out = []
    for scaffold, (L, H) in CONTRASTS.items():
        sizes = (5, 6) if scaffold == "P3" else (6,)
        held = HELD[scaffold]
        for n in sizes:
            for family, grade in FAMILY_GRADES:
                cell = f"HELD-{scaffold}-N{n}-{family}-{grade}"
                rl, rh = by[(cell, L)], by[(cell, H)]
                d_ct = _logit(rl["occ_ct"]) - _logit(rh["occ_ct"])
                d_jump = _logit(rl["occ_jump"]) - _logit(rh["occ_jump"])
                dfloor = rh["floor"] - rl["floor"]
                floor_term = dfloor * LN2 if FLOOR_ENTERS.get(family) else 0.0
                fo_ct = LN2 * (rl["kappa_ct"] - rh["kappa_ct"])
                if (family, scaffold, n) not in jump_cache:
                    jump_cache[(family, scaffold, n)] = jump_first_order(family, n, held)
                jd = jump_cache[(family, scaffold, n)]
                eL, eH = orbit_representative(n, held, L), orbit_representative(n, held, H)
                fo_jump = LN2 * 4.0 * (jd[eL] - jd[eH])
                share = (floor_term / d_ct) if (abs(d_ct) > 0.05 and d_ct * floor_term >= 0 and floor_term != 0.0) else None
                out.append({
                    "cell": cell, "scaffold": scaffold, "n": n, "family": family,
                    "orbits": {"L": L, "H": H},
                    "floor_gap": dfloor, "held_degree_gap": rl["held_degree"] - rh["held_degree"],
                    "delta_log_odds_ct": d_ct, "delta_log_odds_jump": d_jump,
                    "floor_term": floor_term, "residue_ct": d_ct - floor_term,
                    "floor_share_ct": share,
                    "first_order_ct": fo_ct, "first_order_jump": fo_jump,
                    "first_order_floor_part": LN2 * dfloor / 4.0 * (1 if family in ("PATHF", "PATHH", "CSPH") else 0),
                    "F_bar_ratio_L_over_H": rl["F_bar"] / rh["F_bar"], "D_bar_ratio_L_over_H": rl["D_bar"] / rh["D_bar"],
                    "sojourn_present_L_over_H": rl["sojourn_present"] / rh["sojourn_present"],
                    "sojourn_absent_L_over_H": rl["sojourn_absent"] / rh["sojourn_absent"],
                })
    return out


def margin_views(tables: dict) -> list[dict]:
    """D6 (margin slope) and D8 (collation of published margins and overlap)."""
    out = []
    for key in ("e4a", "e4b"):
        for scaffold, n in CELLS[key]:
            for family, grade in FAMILY_GRADES:
                p = _profile(tables, scaffold, n, family, grade)
                out.append({
                    "cell": f"HELD-{scaffold}-N{n}-{family}-{grade}", "scaffold": scaffold, "n": n, "family": family,
                    "r0": p["r0"],
                    "margin_raw_ct": p["margin_raw_ct"], "margin_raw_jump": p["margin_raw_jump"],
                    "margin_standardised_ct": p["margin_standardised_ct"], "margin_standardised_jump": p["margin_standardised_jump"],
                    "free_edge_density_ct": p["free_edge_density_ct"],
                    "null_weight_on_low_k_ct": p["standardised_overlap"]["continuous"]["null_weight_on_low_k"],
                    "null_weight_on_rare_k_ct": p["standardised_overlap"]["continuous"]["null_weight_on_rare_k"],
                    "first_order_margin_slope_ct": margin_slope(family, n, HELD[scaffold]),
                })
    return out


def chord_views(tables: dict) -> list[dict]:
    """D7: P3 chord strata (log odds within strata; association only)."""
    out = []
    for n in (5, 6):
        for family, grade in FAMILY_GRADES:
            p = _profile(tables, "P3", n, family, grade)
            for clock in ("continuous", "jump"):
                ch = p["chord"][clock]
                row = {"cell": f"HELD-P3-N{n}-{family}-{grade}", "family": family, "n": n, "clock": clock, "chord_occupancy": ch["occupancy"]}
                for stratum in ("chord_absent", "chord_present"):
                    c = ch["conditional"][stratum]
                    o = c["orbit_attachment_occupancy_per_slot"]
                    row[stratum] = {"mass": c["mass"], "middle": o["1"], "ends": o["0+2"], "delta_log_odds_middle_minus_ends": _logit(o["1"]) - _logit(o["0+2"])}
                out.append(row)
    return out


def extraction_checks(tables: dict, rows: list[dict]) -> dict:
    """D1 and D2."""
    worst = {"null_orbits": 0.0, "pcomp_ct_orbits": 0.0, "closew_ct": 0.0, "closew_jump": 0.0,
             "balance_pathf": 0.0, "balance_pathh": 0.0, "jump_activity": 0.0, "floor_vs_census": 0.0,
             "floor_vs_published_analytic": 0, "null_witness_total_vs_e0": 0.0}
    for r in rows:
        if r["family"] == "NULL":
            worst["null_orbits"] = max(worst["null_orbits"], abs(r["occ_ct"] - 0.5), abs(r["occ_jump"] - 0.5))
        if r["family"] == "PCOMP":
            worst["pcomp_ct_orbits"] = max(worst["pcomp_ct_orbits"], abs(r["occ_ct"] - 0.5))
        if r["family"] == "PATHF":
            worst["balance_pathf"] = max(worst["balance_pathf"], abs(r["act_ct"] - 2 * r["occ_ct"]))
        if r["family"] == "PATHH":
            worst["balance_pathh"] = max(worst["balance_pathh"], abs(r["act_ct"] - 2 * (1 - r["occ_ct"])))
        worst["jump_activity"] = max(worst["jump_activity"], r["jump_activity_check"])
        worst["floor_vs_census"] = max(worst["floor_vs_census"], abs(r["witness_means_ct"]["held_floor"] - r["floor"]))
        if r["family"] == "NULL":
            worst["null_witness_total_vs_e0"] = max(worst["null_witness_total_vs_e0"], abs(sum(r["witness_means_ct"].values()) - r["e0_path"]))
    for key in ("e4a", "e4b"):
        for scaffold, n in CELLS[key]:
            g = closew_gibbs_orbits(n, HELD[scaffold])
            prof = _profile(tables, scaffold, n, "CLOSEW", "weak_favour")
            for clock in ("continuous", "jump"):
                for orbit, v in g[clock].items():
                    k = "closew_ct" if clock == "continuous" else "closew_jump"
                    worst[k] = max(worst[k], abs(prof["orbits"][clock][orbit]["attachment_occupancy_per_slot"] - v))
    af = {**tables["e4a"]["analytic_floor"], **tables["e4b"]["analytic_floor"]}
    for cell, floors in af.items():
        scaffold, n = cell.split("-N")
        for s, f in floors.items():
            worst["floor_vs_published_analytic"] += int(floor_formula(HELD[scaffold], int(s)) != f)
    selected = {
        "P3-N5-PATHF middle/ends ct": [by_orbit(rows, "HELD-P3-N5-PATHF-weak_suppress", o)["occ_ct"] for o in ("1", "0+2")],
        "S4-N6-PATHF centre/leaves ct": [by_orbit(rows, "HELD-S4-N6-PATHF-weak_suppress", o)["occ_ct"] for o in ("0", "1+2+3")],
        "P4-N6-PATHH inner/ends ct": [by_orbit(rows, "HELD-P4-N6-PATHH-weak_favour", o)["occ_ct"] for o in ("1+2", "0+3")],
    }
    return {"max_abs_deviation": worst, "selected_published_values": selected}


def by_orbit(rows: list[dict], cell: str, orbit: str) -> dict:
    return next(r for r in rows if r["cell"] == cell and r["orbit"] == orbit)


def first_order_monotonicity_counterexamples(n: int = 6, max_source: int = 5) -> list[dict]:
    """Pure algebra: connected held graphs on <= max_source vertices with two source vertices whose
    floor order and first-order PATHF/PATHH coefficient order disagree (or tie) at size n."""
    found = []
    for k in range(3, max_source + 1):
        all_pairs = list(itertools.combinations(range(k), 2))
        seen = set()
        for r in range(k - 1, len(all_pairs) + 1):
            for held in itertools.combinations(all_pairs, r):
                if source(held) != list(range(k)) or not _connected(held, k):
                    continue
                canon = _canonical(held, k)
                if canon in seen:
                    continue
                seen.add(canon)
                for s, t in itertools.combinations(range(k), 2):
                    fs, ft = floor_formula(held, s), floor_formula(held, t)
                    if fs == ft:
                        continue
                    lo, hi = (s, t) if fs < ft else (t, s)
                    kl = -float(e0_path_attachment_formula(n, held, lo))
                    kh = -float(e0_path_attachment_formula(n, held, hi))
                    if kl <= kh:
                        found.append({"held": [list(e) for e in held], "lower_floor_vertex": lo, "higher_floor_vertex": hi,
                                      "floors": [floor_formula(held, lo), floor_formula(held, hi)],
                                      "held_degrees": [held_degree(held, lo), held_degree(held, hi)],
                                      "kappa_lower_minus_higher": kl - kh})
    return found


def _connected(held, k: int) -> bool:
    adj = {v: set() for v in range(k)}
    for a, b in held:
        adj[a].add(b)
        adj[b].add(a)
    seen, stack = {0}, [0]
    while stack:
        for w in adj[stack.pop()]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) == k


def _canonical(held, k: int) -> tuple:
    return min(tuple(sorted(pair(p[a], p[b]) for a, b in held)) for p in itertools.permutations(range(k)))


def build(repo: Path) -> dict:
    tables = _load(repo)
    rows = orbit_views(tables)
    return {
        "analysis_version": ANALYSIS_VERSION,
        "status": "post hoc / explanatory analysis of exposed E4 tables; not E5 evidence; no kernel built",
        "definitions": "gravity-time/docs/gt-p008-coverage-and-integrity-audit.md section 6 (D1-D8)",
        "sources": {k: {"path": TABLES[k], "payload_sha256": tables[k]["payload_sha256"]} for k in TABLES},
        "extraction_checks": extraction_checks(tables, rows),
        "orbits": rows,
        "contrasts": contrasts(tables, rows),
        "margins": margin_views(tables),
        "chord_strata_p3": chord_views(tables),
        "first_order_monotonicity_counterexamples_n6": first_order_monotonicity_counterexamples(6),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m rs_constraint_lab.gtsort")
    sub = parser.add_subparsers(dest="cmd", required=True)
    w = sub.add_parser("write")
    w.add_argument("--repo", default=str(Path(__file__).resolve().parents[3]))
    w.add_argument("--out", default=None)
    args = parser.parse_args(argv)
    repo = Path(args.repo)
    out = Path(args.out) if args.out else repo / OUT_RELPATH
    out.write_text(json.dumps(build(repo), indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
