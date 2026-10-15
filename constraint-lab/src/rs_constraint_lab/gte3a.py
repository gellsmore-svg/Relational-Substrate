"""Gravity-time programme, Round E3A (prompt GT-P006, OTR 1.0): one-way release and recovery.

Question: how do local prohibitions and conditional rates reshape the space of
possible histories? What generates and orients one-way release, how is a
released relation recovered, and when is absence persistent?

Pre-freeze facts (docs/e3-formal-support-and-recovery.md): under hard
path-formation prohibition (path_form prohibit) with any positive-factor soft
components,
  (T1) dissolution is always admissible;
  (T2) dissolving relation e from x is one-way exactly when e is path-witnessed
       in x (witness counts never read e itself);
  (T3) every state reaches the empty graph by dissolutions, so the FREE
       reachable class is one communicating class: nothing is absorbed and
       every released relation can be recovered;
  (T4) the shortest recovery path is 1 + the minimum number of dissolutions
       that break every path witness of e.

Cells reuse gte2a.analyse_item (every gtobs and E2 channel) with a per-cell
alphabet. Added per cell:
  * release census: every dissolution transition classified one-way /
    witnessed two-way / unwitnessed, with stationary flux;
  * recovery from each release destination y for the released slot e: gate
    distance (shortest admissible path to a state with e present), expected
    recovery time (jump events and continuous time), recovery within H jump
    events, and the share of recoveries that re-form e while it is still
    path-witnessed ("direct recovery");
  * partner-index split into event pairs that include a one-way transition and
    pairs that do not.
Two companion scans (GT-Q12 counterexample search) evaluate the partner index
of path_form(m_f) + path_dissolve(m_d) on a frozen 9x9 grid of synthetic
factors at FREE N=4 and N=5.
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

from rs_constraint_lab import gte0a, gte1, gte2a, gtkernel, gtobs
from rs_constraint_lab.state import edges

ROUND_ID = "round-e3a"
EXPERIMENT_ID = "gt-round-e3a-release-and-recovery"
ANALYSIS_VERSION = "gt-e3a/v1"
PROMPT_ID = "GT-P006"

FAMILIES: dict[str, dict[str, list[tuple[str, str]]]] = {
    "PF": {g: [("path_form", g)] for g in ("weak_suppress", "strong_suppress", "prohibit")},
    "HPD": {"prohibit+weak_suppress": [("path_form", "prohibit"), ("path_dissolve", "weak_suppress")], "prohibit+strong_suppress": [("path_form", "prohibit"), ("path_dissolve", "strong_suppress")]},
    "PFD": {"strong_suppress+strong_suppress": [("path_form", "strong_suppress"), ("path_dissolve", "strong_suppress")], "weak_suppress+strong_suppress": [("path_form", "weak_suppress"), ("path_dissolve", "strong_suppress")]},
    "EXCL": {"prohibit": [("close_form", "prohibit")]},
    "NULL": {"none": []},
}
HORIZONS = (1, 2, 4, 8)
SCAN_EXPONENTS = (-3.0, -2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0, 3.0)


def _cell(stratum, family, grade, alphabet, mode, n, reuse=None):
    return {"alphabet": alphabet, "family": family, "grade": grade, "item_id": f"{mode}-N{n}-{alphabet}-{family}-{grade}", "kind": "cell", "mode": mode, "n": n, "reuse": reuse, "stratum": stratum}


def items() -> list[dict]:
    out = []
    for n in (4, 5):
        pub = (lambda name: name if n == 5 else None)
        for g, a in (("weak_suppress", "W4"), ("strong_suppress", "W4"), ("strong_suppress", "W3"), ("strong_suppress", "W16"), ("prohibit", "W4")):
            reuse = pub(f"E2A FREE-N5-PATHF-{g}") if a == "W4" else None
            out.append(_cell("L_formation_ladder", "PF", g, a, "FREE", n, reuse))
        for g, a in (("prohibit+weak_suppress", "W4"), ("prohibit+strong_suppress", "W4"), ("prohibit+strong_suppress", "W16")):
            reuse = pub("E2B FREE-N5-HPF-PDws-prohibit+weak_suppress") if g == "prohibit+weak_suppress" else None
            out.append(_cell("H_hard_against_dissolution", "HPD", g, a, "FREE", n, reuse))
        out.append(_cell("C_soft_controls", "PFD", "strong_suppress+strong_suppress", "W16", "FREE", n))
        out.append(_cell("C_soft_controls", "PFD", "weak_suppress+strong_suppress", "W4", "FREE", n))
        out.append(_cell("C_reversible_hard", "EXCL", "prohibit", "W4", "FREE", n, pub("E2A FREE-N5-EXCL-prohibit")))
        out.append(_cell("C_null", "NULL", "none", "W4", "FREE", n, pub("E2A FREE-N5-NULL-none")))
    out.append(_cell("S_held_scaffold", "PF", "strong_suppress", "W4", "HELD", 5, "E2A HELD-N5-PATHF-strong_suppress"))
    out.append(_cell("S_held_scaffold", "PF", "strong_suppress", "W16", "HELD", 5))
    out.append(_cell("S_held_scaffold", "PF", "prohibit", "W4", "HELD", 5, "E2A HELD-N5-PATHF-prohibit"))
    for n in (4, 5):
        out.append({"item_id": f"SCAN-FREE-N{n}-sigma-sign", "kind": "scan", "mode": "FREE", "n": n, "stratum": "Q12_counterexample_scan", "exponents": list(SCAN_EXPONENTS)})
    return out


# --- release and recovery -----------------------------------------------------------------------


def _witnessed(chain, n: int) -> np.ndarray:
    return gtkernel.witness_counts(chain.states, n, "path_form") > 0


def gate_distance(chain, e: int) -> np.ndarray:
    """Shortest admissible path length from every state to a state with slot e present (inf if none)."""
    size = len(chain.states)
    bits_e = (chain.states >> e) & 1
    dist = np.full(size, np.inf)
    frontier = np.nonzero(bits_e == 1)[0]
    dist[frontier] = 0
    d = 0
    while frontier.size:
        d += 1
        preds = chain.T[frontier]  # predecessor through slot g is T[z, g]; edge exists if W[p, g] > 0
        slot = np.broadcast_to(np.arange(chain.n_slots), preds.shape)
        ok = preds >= 0
        p, g = preds[ok], slot[ok]
        p = p[chain.W[p, g] > 0]
        fresh = np.unique(p[np.isinf(dist[p])])
        dist[fresh] = d
        frontier = fresh
    return dist


def recovery_solves(chain, e: int, witnessed_e: np.ndarray) -> dict:
    """Expected events / time until slot e toggles, and the direct-recovery probability, from states with e absent."""
    R = chain.rates
    P = chain.W / R[:, None]
    absent = np.nonzero(((chain.states >> e) & 1) == 0)[0]
    pos = np.full(len(chain.states), -1)
    pos[absent] = np.arange(len(absent))
    k = len(absent)
    A = np.eye(k)
    for g in range(chain.n_slots):
        if g == e:
            continue
        t = chain.T[absent, g]
        ok = (t >= 0) & (P[absent, g] > 0)
        rows = np.nonzero(ok)[0]
        A[rows, pos[t[ok]]] -= P[absent[rows], g]
    reach = np.isfinite(gate_distance(chain, e))[absent]
    out = {"jump": np.full(len(chain.states), np.inf), "time": np.full(len(chain.states), np.inf), "direct": np.full(len(chain.states), np.nan)}
    if reach.all():
        sol = np.linalg.solve(A, np.stack([np.ones(k), 1.0 / R[absent], P[absent, e] * witnessed_e[absent]], axis=1))
        out["jump"][absent] = sol[:, 0]
        out["time"][absent] = sol[:, 1]
        out["direct"][absent] = sol[:, 2]
    else:
        sub = np.nonzero(reach)[0]
        if sub.size:
            sol = np.linalg.solve(A[np.ix_(sub, sub)], np.stack([np.ones(sub.size), 1.0 / R[absent[sub]], P[absent[sub], e] * witnessed_e[absent[sub]]], axis=1))
            out["jump"][absent[sub]] = sol[:, 0]
            out["time"][absent[sub]] = sol[:, 1]
            out["direct"][absent[sub]] = sol[:, 2]
    return out


def release_and_recovery(chain, n: int, mode: str, ct: np.ndarray, jump: np.ndarray) -> dict:
    classes = gte2a.slot_classes(n, mode)
    W, T = chain.W, chain.T
    P = W / chain.rates[:, None]
    bits = gte2a._bits(chain)
    wit = _witnessed(chain, n)
    u = gte2a.hit_probabilities(chain)
    groups: dict[str, dict] = {}
    totals = {"flux": 0.0}
    mismatch = 0
    gate_ok = {"one_way_ge2": True, "two_way_eq1": True}
    per_slot = {}
    for e in range(chain.n_slots):
        if classes[e] == "S":
            continue
        X = np.nonzero((bits[:, e] == 1) & (T[:, e] >= 0) & (W[:, e] > 0))[0]
        if not X.size:
            continue
        Y = T[X, e]
        one_way = W[Y, e] <= 0
        w_e = wit[:, e]
        mismatch += int((one_way != w_e[X]).sum()) if (one_way.any() or w_e[X].any()) else 0
        dist = gate_distance(chain, e)
        sol = recovery_solves(chain, e, w_e)
        flux = ct[X] * W[X, e]
        jw = jump[X] * P[X, e]
        totals["flux"] += float(flux.sum())
        if one_way.any() and not (dist[Y[one_way]] >= 2).all():
            gate_ok["one_way_ge2"] = False
        if (~one_way).any() and not (dist[Y[~one_way]] == 1).all():
            gate_ok["two_way_eq1"] = False
        for label, sel in (("one_way", one_way), ("witnessed_two_way", (~one_way) & w_e[X]), ("unwitnessed", (~one_way) & ~w_e[X])):
            if not sel.any():
                continue
            G = groups.setdefault(f"{classes[e]}:{label}", {"flux": 0.0, "jump_weight": 0.0, "gate": 0.0, "gate_hist": {}, "m_jump": 0.0, "m_time": 0.0, "direct": 0.0, "u": {h: 0.0 for h in HORIZONS}, "infinite": 0.0, "transitions": 0})
            ys, wj, fl = Y[sel], jw[sel], flux[sel]
            G["transitions"] += int(sel.sum())
            G["flux"] += float(fl.sum())
            G["jump_weight"] += float(wj.sum())
            finite = np.isfinite(sol["jump"][ys])
            G["infinite"] += float(wj[~finite].sum())
            G["gate"] += float((wj * np.where(np.isfinite(dist[ys]), dist[ys], 0)).sum())
            for dv, ww in zip(dist[ys], wj):
                key = "inf" if not np.isfinite(dv) else str(int(dv))
                G["gate_hist"][key] = G["gate_hist"].get(key, 0.0) + float(ww)
            G["m_jump"] += float((wj[finite] * sol["jump"][ys][finite]).sum())
            G["m_time"] += float((wj[finite] * sol["time"][ys][finite]).sum())
            G["direct"] += float((wj[finite] * sol["direct"][ys][finite]).sum())
            for h in HORIZONS:
                G["u"][h] += float((wj * u[h][ys, e]).sum())
        per_slot[e] = True
    out = {}
    tf = totals["flux"] or 1.0
    for key, G in sorted(groups.items()):
        jwt = G["jump_weight"] or 1.0
        fin = jwt - G["infinite"]
        out[key] = {
            "direct_recovery_share": G["direct"] / fin if fin > 0 else None,
            "expected_recovery_events": G["m_jump"] / fin if fin > 0 else None,
            "expected_recovery_time": G["m_time"] / fin if fin > 0 else None,
            "gate_distance_distribution": {k: v / jwt for k, v in sorted(G["gate_hist"].items(), key=lambda kv: (kv[0] == "inf", kv[0]))},
            "mean_gate_distance": G["gate"] / jwt,
            "recovery_within": {str(h): G["u"][h] / jwt for h in HORIZONS},
            "release_flux_share": G["flux"] / tf,
            "transitions": G["transitions"],
            "unrecoverable_weight_share": G["infinite"] / jwt,
        }
    return {"groups": out, "one_way_witness_mismatches": mismatch, "gate_checks": gate_ok}


def partner_split(chain, n: int, jump: np.ndarray) -> dict:
    """Partner-frame index split into event pairs with and without a one-way transition."""
    E = edges(n)
    P = chain.W / chain.rates[:, None]
    deg = gte2a._degrees(chain, n)
    bits = gte2a._bits(chain)
    valid = chain.T >= 0
    rev_zero = np.zeros_like(chain.W, dtype=bool)
    for g in range(chain.n_slots):
        m = valid[:, g] & (chain.W[:, g] > 0)
        rev_zero[m, g] = chain.W[chain.T[m, g], g] <= 0
    parts = {"with_one_way": 0.0, "two_way_only": 0.0}
    mass = {"with_one_way": 0.0, "two_way_only": 0.0}
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
        ow = rev_zero[y, e] | rev_zero[ye, f]
        contrib = prob * np.sign(D) * chi
        parts["with_one_way"] += float(contrib[ow].sum())
        parts["two_way_only"] += float(contrib[~ow].sum())
        mass["with_one_way"] += float(prob[ow].sum())
        mass["two_way_only"] += float(prob[~ow].sum())
    return {"index_parts": parts, "pair_probability": mass}


def extra(block, chain, n, mode, stat):
    block["support"] = {"irreducible": gtobs.class_regime(chain, 0 if mode == "FREE" else gtobs.start_index(chain, n, mode))["irreducible"] if len(chain.states) else None, "states": len(chain.states)}
    if stat is None:
        return
    block["release_recovery"] = release_and_recovery(chain, n, mode, stat["ct"], stat["jump"])
    block["partner_split"] = partner_split(chain, n, stat["jump"])
    from rs_constraint_lab import gte2b

    block["one_way_flux"] = gte2b.one_way_flux(chain, n, mode, stat["ct"])


# --- references --------------------------------------------------------------------------------


def recovery_reference(item: dict, chain, samples: int = 25) -> dict:
    """Gate distances and one-way classification from the rule strings (exact Fractions), by forward BFS."""
    from rs_constraint_lab.constraints import Choreography
    from rs_constraint_lab.weights import alphabet_factors

    n, mode = item["n"], item["mode"]
    factors = alphabet_factors(item["alphabet"])
    chor = Choreography(0, 0, gte0a.rules_for(item["family"], item["grade"], n, mode, FAMILIES))
    cache: dict[tuple[int, int], Fraction] = {}

    def rate(s: int, g: int) -> Fraction:
        key = (s, g)
        if key not in cache:
            w = Fraction(1)
            for c in chor.active(s, (), {}):
                if c.matches(s, g):
                    w *= factors[c.weight]
            cache[key] = w
        return cache[key]

    states = [int(s) for s in chain.states]
    index = {s: i for i, s in enumerate(states)}
    rng = np.random.default_rng(int(hashlib.sha256(f"{ROUND_ID}:recovery:{item['item_id']}".encode()).hexdigest()[:16], 16))
    worst_gate = 0
    oneway_mismatch = 0
    checked = 0
    classes = gte2a.slot_classes(n, mode)
    tries = 0
    while checked < samples and tries < samples * 40:
        tries += 1
        x = states[int(rng.integers(len(states)))]
        e = int(rng.integers(chain.n_slots))
        if classes[e] == "S" or not (x >> e) & 1 or rate(x, e) == 0:
            continue
        y = x ^ (1 << e)
        if y not in index:
            continue
        one_way_ref = rate(y, e) == 0
        one_way_kernel = chain.W[index[y], e] <= 0
        oneway_mismatch += int(one_way_ref != one_way_kernel)
        seen = {y: 0}
        frontier = [y]
        found = None
        while frontier and found is None:
            nxt = []
            for s in frontier:
                for g in range(chain.n_slots):
                    if rate(s, g) == 0:
                        continue
                    t = s ^ (1 << g)
                    if t in seen:
                        continue
                    seen[t] = seen[s] + 1
                    if (t >> e) & 1:
                        found = seen[t]
                        break
                    nxt.append(t)
                if found is not None:
                    break
            frontier = nxt
        kernel_gate = gate_distance(chain, e)[index[y]]
        ref = float("inf") if found is None else float(found)
        worst_gate = max(worst_gate, 0 if ref == kernel_gate else 1)
        checked += 1
    return {"checked_releases": checked, "gate_distance_mismatches": worst_gate, "one_way_mismatches": oneway_mismatch}


def iterative_recovery_reference(chain, e: int, witnessed_e, cap: int = 200000) -> float:
    """Expected recovery events by fixed-point iteration (independent of the linear solve); max abs difference."""
    R = chain.rates
    P = chain.W / R[:, None]
    absent = ((chain.states >> e) & 1) == 0
    m = np.zeros(len(chain.states))
    for _ in range(cap):
        new = np.ones(len(chain.states))
        for g in range(chain.n_slots):
            if g == e:
                continue
            t = chain.T[:, g]
            ok = t >= 0
            new[ok] += P[ok, g] * np.where(absent[t[ok]], m[t[ok]], 0.0)
        new[~absent] = 0.0
        if np.abs(new - m).max() < 1e-12 * max(1.0, np.abs(new).max()):
            m = new
            break
        m = new
    solved = recovery_solves(chain, e, witnessed_e)["jump"]
    fin = absent & np.isfinite(solved)
    return float(np.abs(m[fin] - solved[fin]).max()) if fin.any() else 0.0


# --- scans ---------------------------------------------------------------------------------------


def scan(item: dict) -> dict:
    n = item["n"]
    rows = []
    for a in item["exponents"]:
        for b in item["exponents"]:
            mf, md = 2.0 ** a, 2.0 ** b
            table = {"prohibit": 0.0, "neutral": 1.0, "weak_suppress": mf, "weak_favour": md, "strong_suppress": 0.25, "strong_favour": 4.0}
            comps = [("path_form", "weak_suppress"), ("path_dissolve", "weak_favour")]
            chain, _ = gtkernel.reachable_chain(n, "FREE", comps, table)
            stat = gtobs.stationary(chain, 0, cross_check=True)
            sg = math.log(md) - math.log(mf)
            if not stat.get("resolved"):
                rows.append({"log2_m_dissolve": b, "log2_m_form": a, "resolved": False, "sigma": sg})
                continue
            pf = gte2a.partner_frame(chain, n, stat["jump"])["index"]
            rev = gte0a.reversibility(chain, stat["ct"], stat["mean_rate_ct"])
            edges_mean = float(stat["ct"] @ ((chain.states[:, None] >> np.arange(chain.n_slots)) & 1).sum(axis=1))
            agree = None if abs(sg) < 1e-12 or abs(pf) <= 1e-12 else bool(np.sign(pf) == np.sign(sg))
            rows.append({"expected_edges": edges_mean, "irreversible_flux_fraction": rev["irreversible_flux_fraction"], "log2_m_dissolve": b, "log2_m_form": a, "partner_index": pf, "resolved": True, "residual": stat["residual"], "sigma": sg, "sign_agrees": agree})
    judged = [r for r in rows if r.get("sign_agrees") is not None]
    return {"grid_points": len(rows), "judged": len(judged), "disagreements": [r for r in judged if not r["sign_agrees"]], "below_floor": sum(1 for r in rows if r.get("resolved") and abs(r["sigma"]) >= 1e-12 and abs(r["partner_index"]) <= 1e-12), "rows": rows, "unresolved": sum(1 for r in rows if not r["resolved"])}


# --- one item -------------------------------------------------------------------------------------


def analyse_item(item: dict, *, with_trajectories: bool = True, checks: bool = True, on_main=None):
    if item["kind"] == "scan":
        t0 = time.perf_counter()
        result = {"kind": "scan", "scan": scan(item), "seconds": time.perf_counter() - t0, "n": item["n"], "mode": "FREE"}
        return result, None
    result, traj = gte2a.analyse_item(item, with_trajectories=with_trajectories, checks=checks, on_main=on_main, families=FAMILIES, round_id=ROUND_ID, extra=extra)
    result["kind"] = "cell"
    if checks and result.get("regime") == "recurrent" and (result.get("stationary") or {}).get("resolved"):
        chain, _ = gtkernel.reachable_chain(item["n"], item["mode"], FAMILIES[item["family"]][item["grade"]], None if item["alphabet"] == "W4" else gte2a._alphabet(item["alphabet"]))
        wit = _witnessed(chain, item["n"])
        refs = {"recovery_reference": recovery_reference(item, chain)}
        worst = 0.0
        for e in range(min(chain.n_slots, 4)):
            if gte2a.slot_classes(item["n"], item["mode"])[e] != "S":
                worst = max(worst, iterative_recovery_reference(chain, e, wit[:, e]))
        refs["recovery_time_iterative_max_difference"] = worst
        result["e2a"]["checks"].update(refs)
    return result, traj


def check_problems(result: dict) -> list[str]:
    if result.get("kind") == "scan":
        sc = result["scan"]
        return ["scan unresolved points"] if sc["unresolved"] else []
    problems = gte2a.check_problems(result) if result.get("regime") == "recurrent" else []
    checks = (result.get("e2a") or {}).get("checks") or {}
    rr = checks.get("recovery_reference")
    if rr and (rr["gate_distance_mismatches"] or rr["one_way_mismatches"]):
        problems.append("recovery reference (rule strings) mismatch")
    if checks.get("recovery_time_iterative_max_difference", 0.0) > 1e-8:
        problems.append("recovery time iterative reference")
    return problems


# --- assembly -------------------------------------------------------------------------------------

HARD_PATH_FORM = ("PF:prohibit", "HPD:prohibit+weak_suppress", "HPD:prohibit+strong_suppress")
RATE_SYMMETRIC = ("PFD:strong_suppress+strong_suppress", "NULL:none")


def assemble(results: dict[str, dict], plan_items: list[dict]) -> dict:
    cells = {k: r for k, r in results.items() if r.get("kind") == "cell"}
    base = gte2a.assemble(cells)
    meta = {it["item_id"]: it for it in plan_items}
    checks = base["frozen_expectations"]
    for k in list(checks):
        if k.startswith(("I3-", "I4-", "I5-", "Z5-")):
            checks.pop(k)
    for key, r in cells.items():
        it = meta[key]
        fg = f"{it['family']}:{it['grade']}"
        b = r.get("e2a", {})
        rr = b.get("release_recovery")
        probs = check_problems(r)
        if r.get("regime") == "recurrent" and (r.get("stationary") or {}).get("resolved"):
            checks[f"Z5-{key}"] = {"holds": not probs, "problems": probs}
        if fg in HARD_PATH_FORM and it["mode"] == "FREE":
            checks[f"S1-{key}"] = {"holds": bool(b.get("support", {}).get("irreducible")) and rr is not None and rr["one_way_witness_mismatches"] == 0 and rr["gate_checks"]["one_way_ge2"] and rr["gate_checks"]["two_way_eq1"], "irreducible": b.get("support", {}).get("irreducible"), "one_way_witness_mismatches": None if rr is None else rr["one_way_witness_mismatches"], "gate_checks": None if rr is None else rr["gate_checks"]}
        if not b.get("hard_component") and rr is not None:
            ow = b["one_way"]["one_way_transitions"]
            checks[f"S2-{key}"] = {"holds": ow == 0 and rr["gate_checks"]["two_way_eq1"], "one_way_transitions": ow}
        if fg in RATE_SYMMETRIC and r.get("class_table"):
            uniform = 1.0 / r["reachable_states"]
            l1 = sum(abs(t["ct"] - t["orbit_size"] * uniform) for t in r["class_table"])
            flux = r["reversibility"]["irreversible_flux_fraction"]
            checks[f"S3-{key}"] = {"holds": l1 <= 1e-9 and flux <= 1e-9, "l1_to_uniform": l1, "irreversible_flux_fraction": flux}
        if fg == "EXCL:prohibit" and "reversibility" in r:
            checks[f"S4-{key}"] = {"holds": r["reversibility"]["irreversible_flux_fraction"] <= 1e-9 and b["one_way"]["one_way_transitions"] == 0, "irreversible_flux_fraction": r["reversibility"]["irreversible_flux_fraction"]}
        row = base["cell_rows"].get(key)
        if row is not None:
            row["alphabet"] = it["alphabet"]
            if rr is not None:
                row["recovery"] = {g: {k2: v[k2] for k2 in ("release_flux_share", "mean_gate_distance", "expected_recovery_events", "expected_recovery_time", "direct_recovery_share")} for g, v in rr["groups"].items()}
            if "partner_split" in b:
                row["partner_split"] = b["partner_split"]["index_parts"]
            if "one_way_flux" in b:
                row["one_way_flux_share"] = b["one_way_flux"]["share_of_total_flux"]
    scans = {k: r["scan"] for k, r in results.items() if r.get("kind") == "scan"}
    for k, sc in scans.items():
        diag = [row for row in sc["rows"] if row.get("resolved") and abs(row["sigma"]) < 1e-12]
        checks[f"S5-{k}"] = {"holds": all(row["irreversible_flux_fraction"] <= 1e-9 and abs(row["partner_index"]) <= 1e-12 for row in diag), "diagonal_points": len(diag)}
    base["scans"] = {k: {kk: v for kk, v in sc.items() if kk != "rows"} for k, sc in scans.items()}
    return base


# --- plan and execution ---------------------------------------------------------------------------

PLAN_RELPATH = "gravity-time/plans/round-e3a-plan.json"
GENERATED_RELPATH = "gravity-time/generated/round-e3a"
TABLES_RELPATH = "gravity-time/reports/round-e3a-tables.json"
ATLAS_RELPATH = "gravity-time/reports/gt-e3a-atlas.md"
WATCHDOG_SECONDS = {4: 600, 5: 900}
ROUND_WALL_CAP_SECONDS = 2 * 3600
WORKERS = 4
ONTOLOGY = {"G": 0, "H": 0, "L": 0, "N": [4, 5], "O": 2, "S": 0, "grammar": "ordinary pair DSL"}
REFERENCE_FILES = (
    "research-methods/open-thetical-research.md",
    "gravity-time/provenance/prompts/GT-P006-agent-input.md",
    "gravity-time/docs/e3-coverage-and-question-selection.md",
    "gravity-time/docs/foundational-bridge-map.md",
    "gravity-time/docs/e3-formal-support-and-recovery.md",
    "gravity-time/docs/e2-formal-mechanism.md",
    "gravity-time/reports/gt-e2-synthesis.md",
    "gravity-time/reports/round-e2a-tables.json",
    "gravity-time/reports/round-e2b-tables.json",
    "gravity-time/plans/round-e2a-plan.json",
    "gravity-time/plans/round-e2b-plan.json",
    "constraint-lab/docs/scientific-plan-discipline.md",
    "constraint-lab/formal/open-problems.md",
)


def prepare_plan(repo: Path) -> dict:
    from rs_constraint_lab.durable import sha256_file
    from rs_constraint_lab.explore08 import plan_hash
    from rs_constraint_lab.weights import alphabet_factors

    cells = items()
    document = {
        "analysis_only": True,
        "analysis_version": ANALYSIS_VERSION,
        "alphabets": {a: {g: str(v) for g, v in alphabet_factors(a).items()} for a in ("W4", "W3", "W16")},
        "chosen_because": "GT-E2 synthesis section 7 (one-way release recommended) and GT-P006; coverage audit gravity-time/docs/e3-coverage-and-question-selection.md",
        "clocks": {"jump": "events of the stationary jump chain: event order, partner frame, recovery events, recovery within H, gate distance (admissible steps)", "continuous": "pi_ct = pi_jump / R; release flux, one-way flux, expected recovery time (sum of mean holding times 1/R)"},
        "comparisons": {
            "R1_ladder": "path_form factor 1/2 (W4 weak), 1/4 (W4 strong), 1/9 (W3 strong), 1/16 (W16 strong), 0 (prohibit), FREE N=4 and 5: partner index and its split, one-way flux, recovery of witnessed releases (gate distance, expected recovery events and time, recovery within H, direct-recovery share) against unwitnessed releases. The soft rungs and the hard zero are qualitatively different (positive versus zero support); no limit is claimed",
            "R2_hard_against_dissolution": "path_form prohibit with path_dissolve weak_suppress (W4), strong_suppress (W4) and strong_suppress (W16): soft sigma -log 2, -log 4, -log 16; sign and split of the partner index",
            "R3_soft_controls": "path_form and path_dissolve strong_suppress (W16): rate-symmetric, sigma 0; path_form weak_suppress + path_dissolve strong_suppress (W4): soft sigma = -log 2 with no hard component",
            "R4_reversible_hard_and_null": "EXCL (strict enabling, reversible) and NULL: recovery of path-witnessed versus unwitnessed releases with no rule acting on path witnesses (structural baseline)",
            "R5_scaffold": "HELD N=5 path_form strong_suppress (W4, W16) and prohibit: the held triangle as a soft and as a hard witness",
            "R6_q12_scan": "partner index of path_form(m_f) + path_dissolve(m_d) at FREE N=4 and N=5 on the 9x9 grid m = 2^k, k in {-3,-2,-1,-0.5,0,0.5,1,2,3} (synthetic factors; a bounded counterexample search for GT-Q12, not a model of hard limits)",
            "no_aggregate_score": "no ranking",
        },
        "controls_and_identities": {
            "I1_I2": "square identity on intact squares, zero on disjoint squares, with each cell's alphabet",
            "S1_hard_path_form_support": "every FREE cell with path_form prohibit: the reachable class is irreducible; a release is one-way exactly when the released relation is path-witnessed; every one-way release has gate distance >= 2 and every two-way release gate distance 1 (theorem T1-T4)",
            "S2_soft_support": "every cell without a hard component: no one-way transition and gate distance 1 for every release",
            "S3_rate_symmetric": "PFD strong_suppress+strong_suppress (W16) and NULL: uniform law (class L1 <= 1e-9) and flux <= 1e-9",
            "S4_reversible_hard": "EXCL: flux <= 1e-9 and no one-way transition",
            "S5_scan_diagonal": "scan points with m_f = m_d: flux <= 1e-9 and |partner index| <= 1e-12",
            "Z5_numerical": "gte2a checks (GTH, residual, symmetry, kernel and affinity references from rule strings, partner-frame loop, passage enumeration) plus: gate distance and one-way classification from the rule strings by forward BFS on 25 seeded releases per cell; expected recovery events by fixed-point iteration against the linear solve (|difference| <= 1e-8) on up to four slots",
            "separation_note": "S1-S5 are theorems or identities; none predicts the sign or size of any partner index, recovery time, direct-recovery share or scan outcome",
        },
        "deliberate_omissions": {"n6_n7": "not needed: T1-T4 hold at every N, and N=4/5 show nontrivial one-way release; no FREE N=7", "new_alphabets": "only W4, W3, W16 (existing); scan factors are a declared mathematical search", "entropy_production": "with one-way transitions the logarithmic entropy production diverges; gte0a excludes one-sided pairs from its sum, so reported values are of the two-sided part only and are flagged", "e3b": "not preselected"},
        "estimands": "every gte2a channel plus release census, recovery (gate distance, expected recovery events/time, recovery within H, direct-recovery share), partner split and one-way flux; scans: sign agreement of partner index with sigma",
        "experiment_id": EXPERIMENT_ID,
        "families": {f: {g: {"components": [{"grade": cg, "kind": k} for k, cg in comps]} for g, comps in grades.items()} for f, grades in FAMILIES.items()},
        "history": False,
        "horizons_jump_events": list(HORIZONS),
        "initial_conditions": "FREE starts at the empty graph and HELD at the source triangle; the reachable class from the start is analysed (gte2a policy: restriction to a unique closed class, otherwise structure only)",
        "items": cells,
        "meta_constraints": False,
        "method": {"name": "Open-Thetical Research", "path": "research-methods/open-thetical-research.md", "version": "1.0"},
        "mode": "B",
        "new_primitives": False,
        "ontology": ONTOLOGY,
        "open_questions_without_prediction": [
            "Along the formation ladder 1/2, 1/4, 1/9, 1/16, 0, how do the partner index, its one-way part, and the recovery of witnessed releases change, and is the hard zero continuous with the soft rungs or qualitatively separate?",
            "Can any available opposing dissolution term (soft sigma down to -log 16) reverse the orientation of hard path-form exclusion?",
            "How long does a released, witnessed relation stay absent, by which route is it recovered, and how does that compare with unwitnessed releases and with the same structural event under soft rules?",
            "How much of the partner index comes from event pairs that include a one-way transition?",
            "What does the held triangle do as a soft witness (strong suppression) compared with a hard one?",
            "Does any grid point of the scan have a partner index whose sign disagrees with sigma (GT-Q12)?",
            "Anything not anticipated above.",
        ],
        "parameter_fit": False,
        "pre_freeze_exposure": {
            "published_kernels": {it["item_id"]: it["reuse"] for it in cells if it.get("reuse")},
            "gt_p005_smoke": "the GT-P005 pre-freeze smoke run printed flux, partner index and one-way counts for FREE N=4 W4 PATHF weak_suppress, strong_suppress, prohibit, EXCL and NULL (now E3A cells FREE-N4-W4-PF-*, EXCL, NULL); recovery, gate, split and scan channels were never computed",
            "derivations": "T1-T4 derived before freezing; the support theorem was checked on synthetic fixtures (see execution record); no round cell's law, recovery or scan value was computed before freezing",
            "reference_hashes": {rel: sha256_file(repo / rel) for rel in REFERENCE_FILES},
        },
        "programme": "GT",
        "prompt_id": PROMPT_ID,
        "question": "How do local prohibitions and conditional rates reshape the space of possible histories: what generates and orients one-way release, how is a released relation recovered, and when is absence persistent?",
        "round_id": ROUND_ID,
        "sampling": f"{sum(1 for c in cells if c['kind'] == 'cell')} cells ({sum(1 for c in cells if c.get('reuse'))} on published kernels with new channels) and {sum(1 for c in cells if c['kind'] == 'scan')} companion scans of 81 grid points each",
        "schema": "rs-gt.e3a-plan/v1",
        "seeds": "sha256('round-e3a:<channel>:<item_id>')[:16] for kernel, affinity, passage and recovery reference samples; trajectories as E0",
        "software": {"analysis_module": "rs_constraint_lab.gte3a", "numpy": np.__version__, "observables": gtobs.OBSERVABLES_VERSION, "python": __import__("platform").python_version()},
        "stochastic_trajectories": "illustrative_only",
        "stop_conditions": {"item": f"watchdog {WATCHDOG_SECONDS} seconds by N", "round": f"all items or {ROUND_WALL_CAP_SECONDS} s, then stop", "unresolved": "recorded; no retuning", "amendment": "cell or estimand changes stop the round"},
        "tolerances": {"formula": 1e-12, "identity": 1e-9, "partner_floor": 1e-12, "recovery_iterative": 1e-8, "e2a_numerical": "as E2A"},
        "work_count": {"items": len(cells), "largest_state_space": 1024, "round_wall_cap_seconds": ROUND_WALL_CAP_SECONDS, "watchdog_seconds": {str(k): v for k, v in WATCHDOG_SECONDS.items()}, "workers": WORKERS, "estimate_note": "measured before freezing on synthetic cells (execution record)"},
    }
    document["plan_hash"] = plan_hash(document)
    return document


def require_execution(repo: Path, commit: str | None, *, require_remote: bool = True) -> dict:
    from rs_constraint_lab.explore08 import FrozenPlanError, remote_contains, require_frozen_plan

    plan = require_frozen_plan(repo, commit, PLAN_RELPATH, disk_path=repo / PLAN_RELPATH)
    if require_remote and not remote_contains(repo, commit or ""):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    if plan.get("items") != items() or plan.get("new_primitives") is not False or plan.get("ontology") != ONTOLOGY:
        raise FrozenPlanError("execution refused: E3A plan contract drifted")
    return plan


def execute_item(root: Path, item: dict) -> dict:
    import resource

    from rs_constraint_lab.durable import atomic_write_json

    started = time.perf_counter()

    def payload(result, status):
        return {"item": item, "item_id": item["item_id"], "peak_rss_mb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, "result": result, "status": status, "wall_seconds": time.perf_counter() - started}

    def on_main(result, trajectories):
        atomic_write_json(root / "items" / f"{item['item_id']}.partial.json", payload(result, "complete_checks_interrupted"))

    result, _ = analyse_item(item, on_main=on_main)
    final = payload(result, "complete")
    atomic_write_json(root / "items" / f"{item['item_id']}.json", final)
    partial = root / "items" / f"{item['item_id']}.partial.json"
    if partial.exists():
        partial.unlink()
    return final


def run(root: Path, plan: dict, *, workers: int = WORKERS, **kwargs) -> list[dict]:
    return gte1.run(root, plan, workers=workers, watchdogs=kwargs.pop("watchdogs", WATCHDOG_SECONDS), wall_cap=kwargs.pop("wall_cap", ROUND_WALL_CAP_SECONDS), module="rs_constraint_lab.gte3a", **kwargs)


def publish(root: Path, plan: dict, out: Path, *, frozen_plan_commit: str) -> str:
    from rs_constraint_lab.durable import atomic_write_json, canonical_json, read_json, sha256_bytes

    records = {}
    for it in plan["items"]:
        path = root / "items" / f"{it['item_id']}.json"
        records[it["item_id"]] = read_json(path) if path.is_file() else {"item_id": it["item_id"], "status": "missing"}
    results = {k: v["result"] for k, v in records.items() if "result" in v}
    assembled = assemble(results, plan["items"])
    item_records = {k: {"kind": next(it["kind"] for it in plan["items"] if it["item_id"] == k), "numerical_problems": check_problems(results[k]) if k in results else None, "peak_rss_mb": v.get("peak_rss_mb_parent_view", v.get("peak_rss_mb")), "reuse": next(it.get("reuse") for it in plan["items"] if it["item_id"] == k), "status": v["status"], "wall_seconds": v.get("wall_seconds")} for k, v in records.items()}
    payload = {"analysis_version": ANALYSIS_VERSION, "experiment_id": EXPERIMENT_ID, "frozen_analysis_plan_commit": frozen_plan_commit, "item_records": item_records, "plan_hash": plan["plan_hash"], "results": results, "round_id": ROUND_ID, "schema": "rs-gt.e3a-tables/v1", "status_counts": {s: sum(r["status"] == s for r in item_records.values()) for s in sorted({r["status"] for r in item_records.values()})}, **assembled}
    body = dict(payload)
    body["payload_sha256"] = sha256_bytes(canonical_json(payload).encode("utf-8"))
    atomic_write_json(out, body)
    return body["payload_sha256"]


def render_atlas(repo: Path, tables: Path | None = None, plan_path: Path | None = None) -> str:
    """E2-style sections for the cells, plus recovery, partner split and scan tables."""
    import json
    import tempfile

    from rs_constraint_lab import gte2a_atlas

    t = json.loads((tables or repo / TABLES_RELPATH).read_text())
    plan = json.loads((plan_path or repo / PLAN_RELPATH).read_text())
    cell_plan = dict(plan, items=[it for it in plan["items"] if it["kind"] == "cell"])
    with tempfile.TemporaryDirectory() as tmp:
        tp, pp = Path(tmp) / "t.json", Path(tmp) / "p.json"
        cell_t = dict(t, results={k: v for k, v in t["results"].items() if v.get("kind") == "cell"}, item_records={k: v for k, v in t["item_records"].items() if v["kind"] == "cell"})
        tp.write_text(json.dumps(cell_t))
        pp.write_text(json.dumps(cell_plan))
        text = gte2a_atlas.build(repo, tp, pp, title="GT-E3A release and recovery atlas", tables_rel=TABLES_RELPATH, generator="rs_constraint_lab.gte3a atlas")
    fmt = lambda v, d=3: "—" if v is None else (f"{v:.1e}" if isinstance(v, float) and v != 0 and abs(v) < 1e-3 else (f"{v:.{d}f}" if isinstance(v, float) else str(v)))
    L = ["## 7. Release census and recovery (R1-R5)", "", "Per cell and release class (slot class : one_way / witnessed_two_way / unwitnessed): share of release flux, mean gate distance (admissible steps back to the relation), expected recovery in jump events and in continuous time, recovery within 1/2/4/8 events, direct-recovery share (re-formed while still path-witnessed), unrecoverable weight.", ""]
    L += ["| Cell | Class | flux share | gate | E[events] | E[time] | within 1/2/4/8 | direct | unrecoverable |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for it in cell_plan["items"]:
        rr = (t["results"][it["item_id"]].get("e2a") or {}).get("release_recovery")
        if not rr:
            L.append(f"| {it['item_id']} | — | — | — | — | — | — | — | — |")
            continue
        for g, v in rr["groups"].items():
            w = "/".join(fmt(v["recovery_within"][h]) for h in ("1", "2", "4", "8"))
            L.append(f"| {it['item_id']} | {g} | {fmt(v['release_flux_share'])} | {fmt(v['mean_gate_distance'], 2)} | {fmt(v['expected_recovery_events'], 2)} | {fmt(v['expected_recovery_time'], 2)} | {w} | {fmt(v['direct_recovery_share'])} | {fmt(v['unrecoverable_weight_share'])} |")
    L += ["", "## 8. Partner-index split (Q5)", "", "| Cell | partner index | pairs with a one-way step | two-way pairs only | one-way flux share |", "| --- | --- | --- | --- | --- |"]
    for it in cell_plan["items"]:
        row = t["cell_rows"].get(it["item_id"], {})
        sp = row.get("partner_split")
        if sp:
            L.append(f"| {it['item_id']} | {fmt(row.get('partner_index'), 4)} | {fmt(sp['with_one_way'], 4)} | {fmt(sp['two_way_only'], 4)} | {fmt(row.get('one_way_flux_share'))} |")
    L += ["", "## 9. GT-Q12 counterexample scans (R6)", ""]
    for k, r in t["results"].items():
        if r.get("kind") != "scan":
            continue
        sc = r["scan"]
        L += [f"**{k}**: {sc['grid_points']} points, {sc['judged']} judged (sigma != 0 and |index| > 1e-12), {len(sc['disagreements'])} disagreements, {sc['below_floor']} below the floor, {sc['unresolved']} unresolved.", "", "| log2 m_form | log2 m_dissolve | sigma | partner index | flux | E | agrees |", "| --- | --- | --- | --- | --- | --- | --- |"]
        for row in sc["rows"]:
            L.append(f"| {row['log2_m_form']} | {row['log2_m_dissolve']} | {fmt(row['sigma'], 2)} | {fmt(row.get('partner_index'), 5)} | {fmt(row.get('irreversible_flux_fraction'))} | {fmt(row.get('expected_edges'), 2)} | {row.get('sign_agrees')} |")
        L.append("")
    return text + "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m rs_constraint_lab.gte3a")
    sub = parser.add_subparsers(dest="command", required=True)
    one = sub.add_parser("item")
    one.add_argument("--root", required=True)
    one.add_argument("--item-id", required=True)
    sub.add_parser("atlas")
    args = parser.parse_args(argv)
    from rs_constraint_lab.durable import read_json

    if args.command == "atlas":
        repo = Path(__file__).resolve().parents[3]
        text = render_atlas(repo)
        (repo / ATLAS_RELPATH).write_text(text)
        print(f"wrote {ATLAS_RELPATH} ({len(text)} bytes)")
        return 0
    root = Path(args.root)
    plan = read_json(root / "plan.json")
    (item,) = [it for it in plan["items"] if it["item_id"] == args.item_id]
    if item not in items() and not plan.get("synthetic_fixture"):
        raise SystemExit("item is not in the E3A manifest")
    execute_item(root, item)
    return 0


if __name__ == "__main__":
    sys.exit(main())
