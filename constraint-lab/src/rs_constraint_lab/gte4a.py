"""Gravity-time programme, Round E4A (prompt GT-P007, OTR 1.0): native held-reference structure.

First label-covariant test of the E3B scaffold explanation. The same unmodified
rules run under three held references (gt0.Scaffold):
  K2  one held edge {0,1}; no internal held two-path;
  P3  held path 0-1-2; the closing chord (0,2) is a free relation;
  K3  the original held triangle (published cells: labelled replications).
The scaffold enters the kernel only through its held relations being present
and their dissolution prohibited; no rule reads source membership.

Per cell: every gtobs channel under the active scaffold, plus
  * attachment by source orbit (per eligible slot), both clocks;
  * P3 chord occupancy and attachment / orbit attachment conditional on it;
  * witness census at attachment slots: held-only floor, source-internal with
    the free chord, and witnesses involving probes or other free relations;
  * attachment-slot activity per source orbit (per unit time and per event);
  * overlap diagnostics for the null-density-standardised margin;
  * handover index (source frame), partner-frame index, square identity.
"""

from __future__ import annotations

import argparse
import itertools
import math
import sys
import time
from pathlib import Path

import numpy as np

from rs_constraint_lab import gt0, gte0a, gte0b, gte1, gte2a, gtkernel, gtobs
from rs_constraint_lab.state import edges

ROUND_ID = "round-e4a"
EXPERIMENT_ID = "gt-round-e4a-native-held-reference"
ANALYSIS_VERSION = "gt-e4a/v1"
PROMPT_ID = "GT-P007"
MODE = "HELD"

FAMILY_GRADES = (("NULL", "none"), ("PATHF", "weak_suppress"), ("PATHH", "weak_favour"), ("CSPH", "strong_favour+weak_favour"), ("PCOMP", "weak_favour+weak_favour"), ("CLOSEW", "weak_favour"))
FAMILIES: dict[str, dict[str, list[tuple[str, str]]]] = {f: {g: list(gte0b.FAMILIES[f][g])} for f, g in FAMILY_GRADES}
SCAFFOLD_ORDER = ("K2", "P3", "K3")
SIZES = (5, 6)
RARE = 1e-12
LOW = 1e-6


def item_id(scaffold: str, n: int, family: str, grade: str) -> str:
    return f"HELD-{scaffold}-N{n}-{family}-{grade}"


def items() -> list[dict]:
    out = []
    for scaffold in SCAFFOLD_ORDER:
        for n in SIZES:
            for f, g in FAMILY_GRADES:
                role = "replication_published_triangle" if scaffold == "K3" else ("geometry_null" if f == "NULL" else ("control" if f in ("PCOMP", "CLOSEW") else "open_scientific"))
                out.append({"alphabet": "W4", "family": f, "grade": g, "item_id": item_id(scaffold, n, f, g), "mode": MODE, "n": n, "role": role, "scaffold": scaffold, "held": [list(e) for e in gt0.SCAFFOLDS[scaffold].held]})
    return out


# --- analytic geometry and witness census ------------------------------------------------------


def null_geometry(scaffold: str, n: int) -> dict:
    sc = gt0.SCAFFOLDS[scaffold]
    k, K = len(sc.source), len(sc.held)
    M = math.comb(n, 2) - K
    return {"attachment_slots": k * (n - k), "free_slots": M, "held_edges": K, "nonheld_source_internal_slots": math.comb(k, 2) - K, "pair_slots": math.comb(n, 2), "probe_probe_slots": math.comb(n - k, 2), "probes": n - k, "r0": k * (n - k) / M, "source_vertices": k}


def source_orbits(n: int) -> list[list[int]]:
    """Orbits of the source vertices under the active scaffold's automorphism group."""
    src = gt0.source()
    auts = gt0.active_scaffold().automorphisms(n)
    seen, orbits = set(), []
    for v in src:
        if v in seen:
            continue
        orb = sorted({perm[v] for perm in auts})
        seen.update(orb)
        orbits.append(orb)
    return orbits


def witness_census(states: np.ndarray, n: int) -> dict[str, np.ndarray]:
    """Per state and slot: path witnesses split into held-only, source-internal with a free chord, and other."""
    E = edges(n)
    pos = {pair: i for i, pair in enumerate(E)}
    held = set(gt0.held_pairs())
    src = set(gt0.source())
    out = {k: np.zeros((len(states), len(E)), dtype=np.int64) for k in ("held_floor", "chord_internal", "other")}
    for e, (a, b) in enumerate(E):
        for end in (a, b):
            for c in range(n):
                if c in (a, b):
                    continue
                for d in range(n):
                    if d in (a, b) or d == c:
                        continue
                    p1, p2 = (min(end, c), max(end, c)), (min(c, d), max(c, d))
                    present = ((states >> pos[p1]) & 1) * ((states >> pos[p2]) & 1)
                    if p1 in held and p2 in held:
                        key = "held_floor"
                    elif {end, c, d} <= src:
                        key = "chord_internal"
                    else:
                        key = "other"
                    out[key][:, e] += present
    return out


def analytic_floor(scaffold: str, n: int) -> dict[int, int]:
    """Held-only path witnesses on an attachment slot at each source vertex (state independent)."""
    sc = gt0.SCAFFOLDS[scaffold]
    held = set(sc.held)
    out = {}
    for s in sc.source:
        p = next(v for v in range(n) if v not in sc.source)
        count = 0
        for c in sc.source:
            for d in sc.source:
                if len({s, c, d}) < 3:
                    continue
                if (min(s, c), max(s, c)) in held and (min(c, d), max(c, d)) in held:
                    count += 1
        out[s] = count
        del p
    return out


# --- per-cell E4 channels ------------------------------------------------------------------------


def e4_channels(chain, n: int, ct: np.ndarray, jump: np.ndarray, D: np.ndarray) -> dict:
    E = edges(n)
    classes = gt0.slot_classes(n)
    src = gt0.source()
    bits = ((chain.states[:, None] >> np.arange(chain.n_slots)) & 1).astype(np.int64)
    P = chain.W / chain.rates[:, None]
    orbits = source_orbits(n)
    probes = [v for v in range(n) if v not in src]
    out: dict = {"orbits": orbits}
    att_by_vertex = {v: [i for i, (a, b) in enumerate(E) if classes[i] == "A" and v in (a, b)] for v in src}
    chord = [i for i, c in enumerate(classes) if c == "C"]
    census = witness_census(chain.states, n)
    for clock, law in (("continuous", ct), ("jump", jump)):
        block = {}
        for orb in orbits:
            key = "+".join(map(str, orb))
            slots = [i for v in orb for i in att_by_vertex[v]]
            occ = float(law @ bits[:, slots].sum(axis=1)) / len(slots)
            wf = {k: float(law @ census[k][:, slots].sum(axis=1)) / len(slots) for k in census}
            rate_slots = (chain.W if clock == "continuous" else P)[:, slots]
            act = float(law @ rate_slots.sum(axis=1)) / len(slots)
            block[key] = {"attachment_occupancy_per_slot": occ, "attachment_activity_per_slot": act, "witness_means_per_slot": wf}
        if chord:
            c = chord[0]
            present = bits[:, c] == 1
            mass = float(law[present].sum())
            att_slots = [i for i, cl in enumerate(classes) if cl == "A"]
            free_slots = gt0.free_slot_indices(n)
            cond = {}
            for label, sel in (("chord_present", present), ("chord_absent", ~present)):
                m = float(law[sel].sum())
                if m <= 0:
                    cond[label] = None
                    continue
                ea = float((law * bits[:, att_slots].sum(axis=1))[sel].sum()) / m
                ek = float((law * bits[:, free_slots].sum(axis=1))[sel].sum()) / m
                per_orbit = {}
                for orb in orbits:
                    slots = [i for v in orb for i in att_by_vertex[v]]
                    per_orbit["+".join(map(str, orb))] = float((law * bits[:, slots].sum(axis=1))[sel].sum()) / m / len(slots)
                cond[label] = {"mass": m, "attachment_fraction": (ea / ek) if ek > 0 else None, "orbit_attachment_occupancy_per_slot": per_orbit}
            block["chord"] = {"occupancy": mass, "conditional": cond, "activity": float(law @ (chain.W if clock == "continuous" else P)[:, c])}
        pp = [i for i, cl in enumerate(classes) if cl == "P"]
        if pp:
            block["probe_probe_occupancy_per_slot"] = float(law @ bits[:, pp].sum(axis=1)) / len(pp)
            block["probe_probe_activity_per_slot"] = float(law @ (chain.W if clock == "continuous" else P)[:, pp].sum(axis=1)) / len(pp)
        att_count = bits[:, [i for i, cl in enumerate(classes) if cl == "A"]].sum(axis=1)
        block["attachment_count_distribution"] = {str(int(v)): float(law[att_count == v].sum()) for v in np.unique(att_count)}
        attached_probes = np.zeros(len(chain.states), dtype=np.int64)
        for pr in probes:
            attached_probes += (D[:, pr] == 1).astype(np.int64)
        block["attached_probe_count_distribution"] = {str(int(v)): float(law[attached_probes == v].sum()) for v in np.unique(attached_probes)}
        out[clock] = block
    return out


def standardised_overlap(h: dict, M: int) -> dict:
    """Where the NULL binomial weight sits relative to the cell's own free-edge mass."""
    mass = {int(k): v for k, v in h["free_edge_count_distribution"].items()}
    w = {k: math.comb(M, k) / 2 ** M for k in range(M + 1)}
    rare = [k for k in w if mass.get(k, 0.0) < RARE]
    low = [k for k in w if RARE <= mass.get(k, 0.0) < LOW]
    supported = [k for k in w if mass.get(k, 0.0) >= LOW]
    return {"null_weight_on_rare_k": sum(w[k] for k in rare), "null_weight_on_low_k": sum(w[k] for k in low), "supported_k_range": [min(supported), max(supported)] if supported else None}


def analyse_item(item: dict, *, with_trajectories: bool = False, checks: bool = True, on_main=None) -> tuple[dict, None]:
    n, family, grade = item["n"], item["family"], item["grade"]
    components = FAMILIES[family][grade]
    with gt0.use_scaffold(item["scaffold"]):
        t0 = time.perf_counter()
        chain, kt = gtkernel.reachable_chain(n, MODE, components)
        start = gtobs.start_index(chain, n, MODE)
        stat = gtobs.stationary(chain, start, cross_check=True)
        result, _ = gtobs.analyse(chain, family=family, grade=grade, n=n, mode=MODE, families=FAMILIES, item_id=item["item_id"], round_id=ROUND_ID, with_trajectories=False, stationary_override=stat)
        result["scaffold"] = {"name": item["scaffold"], "held": [list(e) for e in gt0.held_pairs()], "source": list(gt0.source())}
        result["geometry"] = null_geometry(item["scaffold"], n)
        block = {"analysis_version": ANALYSIS_VERSION, "analytic_floor": {str(k): v for k, v in analytic_floor(item["scaffold"], n).items()}}
        census = witness_census(chain.states, n)
        classes = gt0.slot_classes(n)
        floor_ok = True
        for i, (a, b) in enumerate(edges(n)):
            if classes[i] == "A":
                s = a if a in gt0.source() else b
                floor_ok &= bool((census["held_floor"][:, i] == block["analytic_floor"][str(s)]).all())
            elif classes[i] in ("P", "C", "S"):
                floor_ok &= bool((census["held_floor"][:, i] == 0).all()) if classes[i] == "P" else True
        block["census_floor_matches_analytic"] = floor_ok
        if stat.get("resolved"):
            D = gtobs.source_distances(chain.states, n)
            block["channels"] = e4_channels(chain, n, stat["ct"], stat["jump"], D)
            block["standardised_overlap"] = {clock: standardised_overlap(result[key], result["geometry"]["free_slots"]) for clock, key in (("continuous", "held_continuous"), ("jump", "held_jump"))}
            block["handover"] = gte1.handover_statistics(gtobs.event_pattern_probabilities(chain, stat["jump"], n, MODE))
            block["partner"] = gte2a.partner_frame(chain, n, stat["jump"])
            sq = gte2a.square_census(chain, n, MODE, components, stat["ct"])
            block["square_formula_max_abs_error"] = sq["formula_max_abs_error"]
            block["square_disjoint_max_abs"] = sq["disjoint_max_abs_affinity"]
            block["rare_mass_flags"] = gte1.rare_mass_flags(result)
        result["e4"] = block
        result["timings"]["main_total"] = time.perf_counter() - t0
        if on_main is not None:
            on_main(result, None)
        if checks:
            t1 = time.perf_counter()
            block["checks"] = gte1.numerical_checks(item, chain, start, stat if stat.get("resolved") else None, families=FAMILIES, round_id=ROUND_ID)
            result["timings"]["checks"] = time.perf_counter() - t1
    return result, None


def check_problems(result: dict) -> list[str]:
    problems = []
    st = result.get("stationary") or {}
    if result.get("regime") != "recurrent":
        return [f"regime {result.get('regime')}"]
    if not st.get("resolved"):
        return [f"stationary unresolved: {st.get('reason')}"]
    if st["residual"] > gtobs.STATIONARY_RESIDUAL_TOLERANCE:
        problems.append("stationary residual")
    if (result.get("symmetry_max_abs_difference") or 0.0) > gte0a.SYMMETRY_TOLERANCE:
        problems.append("symmetry")
    if (result.get("autocorrelation_diagnostics") or {}).get("cap_reached"):
        problems.append("autocorrelation cap reached")
    b = result.get("e4", {})
    if not b.get("census_floor_matches_analytic"):
        problems.append("witness floor census differs from the analytic floor")
    if (b.get("square_formula_max_abs_error") or 0.0) > 1e-12:
        problems.append("square identity")
    checks = b.get("checks")
    if checks is None:
        return problems + ["numerical checks not completed"]
    ks = checks["kernel_sample"]
    if ks["max_relative_weight_difference"] > gte1.KERNEL_RELATIVE_TOLERANCE or ks["zero_pattern_mismatches"] or ks["target_mismatches"]:
        problems.append("kernel sample check")
    ld = checks.get("long_double_residual") or {}
    if ld.get("zero_mass_states"):
        problems.append("zero-mass reachable states")
    if ld.get("max_relative") is not None and ld["max_relative"] > gte1.RESIDUAL_MAX_RELATIVE:
        problems.append("per-entry relative residual")
    for name, ref in (checks.get("referees") or {}).items():
        for clock in ("ct", "jump"):
            if ref[clock]["l1"] > gte1.REFEREE_L1 or (ref[clock]["max_relative"] or 0.0) > gte1.REFEREE_MAX_RELATIVE:
                problems.append(f"referee {name} {clock} law")
        if ref["channel_max_abs_difference"] is not None and ref["channel_max_abs_difference"] > gte1.REFEREE_CHANNEL_ABS:
            problems.append(f"referee {name} channels")
    return problems


# --- assembly ------------------------------------------------------------------------------------

DECLARED = ("margin_raw_ct", "margin_raw_jump", "margin_normalised_ct", "margin_normalised_jump", "margin_standardised_ct", "margin_standardised_jump", "detached_fraction_ct", "detached_fraction_jump", "free_edge_density_ct", "irreversible_flux_fraction", "handover_index", "partner_index", "expected_edges", "near_far_ratio_ct", "near_far_ratio_jump")


def profile(r: dict) -> dict | None:
    if r.get("regime") != "recurrent" or not (r.get("stationary") or {}).get("resolved"):
        return None
    hc, hj = r["held_continuous"], r["held_jump"]
    add = r["e1_additions"]["held"]
    r0 = hc["null_attachment_fraction"]
    p = {"r0": r0}
    for clock, h, a in (("ct", hc, add["continuous"]), ("jump", hj, add["jump"])):
        af = h["attachment_fraction"]
        p[f"attachment_fraction_{clock}"] = af
        p[f"margin_raw_{clock}"] = af - r0
        p[f"margin_normalised_{clock}"] = None if r0 >= 1 else (af - r0) / (1 - r0)
        p[f"margin_standardised_{clock}"] = a["attachment_margin_null_density_standardised"]
        p[f"detached_fraction_{clock}"] = h["distance_distribution"].get("inf", 0.0)
        p[f"free_edge_density_{clock}"] = h["expected_free_edges"] / h["free_slots"]
    p["irreversible_flux_fraction"] = r["reversibility"]["irreversible_flux_fraction"]
    p["expected_edges"] = r["occupancy_ct"]["expected_edges"]
    p["handover_index"] = r["e4"]["handover"]["index_adjacent"]
    p["handover_forward_steps"] = r["e4"]["handover"]["forward_oriented_adjacent_steps"]
    p["partner_index"] = r["e4"]["partner"]["index"]
    p["near_far_ratio_ct"] = r["shell_activity"]["continuous"]["near_far_ratio"]
    p["near_far_ratio_jump"] = r["shell_activity"]["jump"]["near_far_ratio"]
    ch = r["e4"]["channels"]
    p["orbits"] = {clock: {k: v for k, v in ch[clock].items() if k not in ("chord", "attachment_count_distribution", "attached_probe_count_distribution", "probe_probe_occupancy_per_slot", "probe_probe_activity_per_slot")} for clock in ("continuous", "jump")}
    p["chord"] = {clock: ch[clock].get("chord") for clock in ("continuous", "jump")}
    p["standardised_overlap"] = r["e4"]["standardised_overlap"]
    return p


def replication(r: dict, old: dict | None) -> dict:
    if old is None:
        return {"holds": False, "reason": "no published cell"}
    rows, ok = {}, True
    for path in (("held_continuous", "attachment_fraction"), ("held_jump", "attachment_fraction"), ("reversibility", "irreversible_flux_fraction"), ("occupancy_ct", "expected_edges"), ("event_order", "pattern_asymmetry")):
        a, b = r, old
        for k in path:
            a, b = a[k], b[k]
        good = abs(a - b) <= max(gte1.REPLICATION_ABS, gte1.REPLICATION_REL * abs(b))
        ok &= good
        rows["/".join(path)] = {"published": b, "rederived": a, "within_tolerance": good}
    return {"channels": rows, "holds": ok}


def assemble(results: dict[str, dict], published: dict[str, dict], *, cells: list[dict] | None = None, scaffold_order: tuple[str, ...] = SCAFFOLD_ORDER, sizes: tuple[int, ...] = SIZES, family_grades=FAMILY_GRADES) -> dict:
    meta = {it["item_id"]: it for it in (cells or items())}
    profiles = {k: profile(r) for k, r in results.items()}
    checks = {}
    for key, r in results.items():
        it = meta[key]
        p = profiles[key]
        probs = check_problems(r)
        checks[f"Z5-{key}"] = {"holds": not probs, "problems": probs}
        checks[f"W-{key}"] = {"holds": bool(r.get("e4", {}).get("census_floor_matches_analytic")), "analytic_floor": r.get("e4", {}).get("analytic_floor")}
        if p is None:
            continue
        if it["family"] == "NULL":
            vals = [abs(p["margin_raw_ct"]), abs(p["margin_raw_jump"]), abs(p["margin_standardised_ct"]), p["irreversible_flux_fraction"]]
            checks[f"N-{key}"] = {"holds": max(vals) <= 1e-9 and abs(p["r0"] - r["geometry"]["r0"]) <= 1e-15, "max_value": max(vals), "r0": p["r0"], "r0_geometry": r["geometry"]["r0"]}
        if it["family"] in ("PCOMP", "CLOSEW"):
            checks[f"R-{key}"] = {"holds": p["irreversible_flux_fraction"] <= 1e-9 and abs(p["handover_index"]) <= 1e-9 and abs(p["partner_index"]) <= 1e-9, "flux": p["irreversible_flux_fraction"]}
        if it["family"] == "PCOMP":
            checks[f"U-{key}"] = {"holds": abs(p["margin_raw_ct"]) <= 1e-9, "margin_raw_ct": p["margin_raw_ct"]}
        if it["family"] == "CLOSEW":
            gap = r.get("predicted_law_l1_gap")
            checks[f"G-{key}"] = {"holds": gap is not None and gap <= 1e-9, "l1_gap": gap}
        if it["scaffold"] == "K3":
            checks[f"K3-{key}"] = replication(r, published.get(f"HELD-N{it['n']}-{it['family']}-{it['grade']}"))
    comparisons = {"profiles": profiles}
    by = {(m["scaffold"], m["n"], m["family"]): k for k, m in meta.items()}
    table = {}
    for f, g in family_grades:
        for n in sizes:
            table[f"{f}-N{n}"] = {sc: ({c: profiles[by[(sc, n, f)]].get(c) for c in DECLARED} if profiles.get(by.get((sc, n, f))) else None) for sc in scaffold_order}
    comparisons["scaffold_table"] = table
    return {"comparisons": comparisons, "frozen_expectations": checks, "geometry": {f"{sc}-N{n}": null_geometry(sc, n) for sc in scaffold_order for n in sizes}, "analytic_floor": {f"{sc}-N{n}": {str(k): v for k, v in analytic_floor(sc, n).items()} for sc in scaffold_order for n in sizes}}


# --- plan, execution, publication -----------------------------------------------------------------

PLAN_RELPATH = "gravity-time/plans/round-e4a-plan.json"
GENERATED_RELPATH = "gravity-time/generated/round-e4a"
TABLES_RELPATH = "gravity-time/reports/round-e4a-tables.json"
ATLAS_RELPATH = "gravity-time/reports/gt-e4a-atlas.md"
E0B_TABLES_RELPATH = "gravity-time/reports/round-e0b-tables.json"
WATCHDOG_SECONDS = {5: 900, 6: 1800}
ROUND_WALL_CAP_SECONDS = 3 * 3600
WORKERS = 4
ONTOLOGY = {"G": 0, "H": 0, "L": 0, "N": [5, 6], "O": 2, "S": 0, "grammar": "ordinary pair DSL"}
REFERENCE_FILES = (
    "research-methods/open-thetical-research.md",
    "gravity-time/provenance/prompts/GT-P007-agent-input.md",
    "gravity-time/docs/e4-coverage-and-selection.md",
    "gravity-time/docs/e4-configurable-scaffold.md",
    "gravity-time/docs/e3-formal-support-and-recovery.md",
    "gravity-time/reports/round-e3b-tables.json",
    "gravity-time/plans/round-e3b-plan.json",
    "gravity-time/reports/round-e0b-tables.json",
    "gravity-time/docs/foundational-bridge-map.md",
    "constraint-lab/docs/scientific-plan-discipline.md",
)


def prepare_plan(repo: Path) -> dict:
    from rs_constraint_lab.durable import sha256_file
    from rs_constraint_lab.explore08 import plan_hash

    cells = items()
    document = {
        "analysis_only": True,
        "analysis_version": ANALYSIS_VERSION,
        "chosen_because": "GT-E3 synthesis section 6 (covariant source-structure control) and GT-P007; coverage audit gravity-time/docs/e4-coverage-and-selection.md",
        "clocks": {"continuous": "pi_ct = pi_jump / R; per-unit-time observables", "jump": "pi_jump; per-event observables and event order"},
        "comparisons": {
            "Q1_k2_gathering": "does K2 give a raw, normalised or null-density-standardised margin above its own NULL (r0 = 2(N-2)/M) for PATHF weak_suppress, PATHH weak_favour or CSPH, in either clock, without any rule reading source membership?",
            "Q2_p3": "does P3 sit between K2 and K3, or differ qualitatively; do its endpoint and middle orbits follow the witness census (endpoint floor 1, middle 0; 2 everywhere once the chord is present), and how does the chord's occupancy condition attachment?",
            "Q3_p3_to_k3": "at three source vertices, does K3 versus P3 follow the permanent-witness floor or do density, support and kinetic changes dominate?",
            "Q4_clock_and_density": "is any gathering consistent across clocks, margin forms and non-rare density regions (standardised-margin overlap diagnostics, rare-mass flags)?",
            "Q5_joint_regime": "does any family show source-selective occupancy and an oriented handover together natively; does one change without the other across scaffolds?",
            "Q6_sign_versus_magnitude": "does removing the triangle floor explain the sign but not the magnitude of differences (native K2 law is not expected to equal E3B's neutralised K3 law: sources, free slots and witnesses differ)?",
            "Q7_controls": "NULL, PCOMP and CLOSEW behave as their mathematics requires (identities N, R, U, G); a failed control is investigated before target cells are interpreted",
            "Q8_artefacts": "separate structural change from null-geometry normalisation, density, source participation and observer frame (per-slot orbit measures, own-NULL margins)",
            "e3b_reference": "E3B neutralised K3 margins (round-e3b-tables.json) are cited beside native results, never pooled",
            "no_aggregate_score": "profiles per channel; no ranking",
        },
        "controls_and_identities": {
            "W_floor": "at every reachable state the held-only path-witness count on each attachment slot equals the analytic floor (K2: 0; P3: endpoints 1, middle 0; K3: 2) and is 0 on probe-probe slots",
            "N_null": "NULL under each scaffold: uniform law; raw and standardised margins |.| <= 1e-9 in both clocks (raw ct and jump), flux <= 1e-9; r0 equals k(N-k)/M",
            "R_reversible": "PCOMP and CLOSEW: flux, |handover index| and |partner index| <= 1e-9",
            "U_pcomp": "PCOMP: continuous-time raw margin |.| <= 1e-9 (rate-symmetric, uniform continuous law); jump-clock channels are not expected to vanish",
            "G_closew": "CLOSEW: predicted triple-Gibbs law, L1 gap <= 1e-9",
            "K3_replication": "K3 cells reproduce the published E0B cells on attachment fractions (both clocks), flux, expected edges and event-order asymmetry within max(1e-10, 1e-8 x |published|)",
            "Z5_numerical": "stationary resolved (two starts within 1e-10, residual <= 1e-12), symmetry under the scaffold's automorphism group <= 1e-10, autocorrelation within cap, kernel sample from rule strings (scaffold prohibitions included), long-double residual, GTH referee for classes <= 4,096 states and a third start above, witness floor census, square identity",
            "separation_note": "no expectation on any target margin, index or flux",
        },
        "deliberate_omissions": {"n7": "not authorised", "other_scaffolds": "candidates for E4B only", "disconnected_references": "not included", "trajectories": "not generated", "spectrum": "unavailable"},
        "estimands": "every gtobs channel, the E4 channels and identities of each cell; Q1-Q8",
        "experiment_id": EXPERIMENT_ID,
        "families": {f: {g: {"components": [{"grade": cg, "kind": k} for k, cg in FAMILIES[f][g]], "sigma": gte2a.sigma(FAMILIES[f][g])}} for f, g in FAMILY_GRADES},
        "geometry": {f"{sc}-N{n}": null_geometry(sc, n) for sc in SCAFFOLD_ORDER for n in SIZES},
        "analytic_floor": {f"{sc}-N{n}": {str(k): v for k, v in analytic_floor(sc, n).items()} for sc in SCAFFOLD_ORDER for n in SIZES},
        "history": False,
        "initial_conditions": "HELD start state = the scaffold's held relations present, every other relation absent; the reachable class from it (every non-held slot toggles freely under NULL, so it is the full space of 2^M states)",
        "items": cells,
        "meta_constraints": False,
        "method": {"name": "Open-Thetical Research", "path": "research-methods/open-thetical-research.md", "version": "1.0"},
        "mode": "B",
        "new_primitives": False,
        "ontology": ONTOLOGY,
        "open_questions_without_prediction": ["Q1-Q8 above", "Anything not anticipated"],
        "p3_chord": "the P3 closing chord (0,2) is an ordinary free relation, class C in event order and slot classes; it is never held",
        "parameter_fit": False,
        "pre_freeze_exposure": {
            "published_k3": "all 12 K3 cells are published E0B cells (standard channels known); they are labelled replications",
            "engineering": "scaffold tests used N=4 and N=5 kernels of K2 and P3 for rule-string equality, relabelling covariance, symmetry and NULL geometry, and held-observable equality for P3 N=5 PATHF weak_suppress (attachment fraction compared between two implementations; the value was not inspected or recorded). NULL margins at N=5, 6 under K2/P3 are theorem-fixed. No other K2 or P3 law was computed before freezing",
            "timing": "costs measured on synthetic-factor K2/P3 N=6 fixtures (execution record); no science observable read",
            "reference_hashes": {rel: sha256_file(repo / rel) for rel in REFERENCE_FILES},
        },
        "programme": "GT",
        "prompt_id": PROMPT_ID,
        "question": "What aspects of source-probe gathering, directional succession, local activity and persistence follow from the held reference's internal relational structure, and what aspects belong to the unmodified rules?",
        "round_id": ROUND_ID,
        "rare_state_rule": f"conditionals on mass < {RARE} are flagged rare and not interpreted; < {LOW} low; the standardised margin is reported with the NULL weight on rare and low free-edge counts and the supported range",
        "sampling": f"exact census of {len(cells)} cells (12 published K3 replications, 24 K2/P3 cells)",
        "schema": "rs-gt.e4a-plan/v1",
        "scaffolds": {name: {"held": [list(e) for e in gt0.SCAFFOLDS[name].held], "source": list(gt0.SCAFFOLDS[name].source)} for name in SCAFFOLD_ORDER},
        "software": {"analysis_module": "rs_constraint_lab.gte4a", "kernel": gtkernel.KERNEL_VERSION, "numpy": np.__version__, "observables": gtobs.OBSERVABLES_VERSION, "python": __import__("platform").python_version()},
        "stochastic_trajectories": "none",
        "stop_conditions": {"item": f"watchdog {WATCHDOG_SECONDS} seconds by N", "round": f"all items or {ROUND_WALL_CAP_SECONDS} s; then stop", "unresolved": "recorded; no retuning", "amendment": "cell or estimand changes stop the round"},
        "tolerances": {"identity": 1e-9, "floor": "exact", "square": 1e-12, "numerical": "as E1 (gte1)"},
        "work_count": {"items": len(cells), "largest_state_space": 16384, "memory_ceiling_per_worker_bytes": 2_500_000_000, "round_wall_cap_seconds": ROUND_WALL_CAP_SECONDS, "watchdog_seconds": {str(k): v for k, v in WATCHDOG_SECONDS.items()}, "workers": WORKERS, "estimate_note": "see execution record (measured on synthetic fixtures before freezing)"},
    }
    document["plan_hash"] = plan_hash(document)
    return document


def require_execution(repo: Path, commit: str | None, *, require_remote: bool = True) -> dict:
    from rs_constraint_lab.explore08 import FrozenPlanError, remote_contains, require_frozen_plan

    plan = require_frozen_plan(repo, commit, PLAN_RELPATH, disk_path=repo / PLAN_RELPATH)
    if require_remote and not remote_contains(repo, commit or ""):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    if plan.get("items") != items() or plan.get("new_primitives") is not False or plan.get("ontology") != ONTOLOGY:
        raise FrozenPlanError("execution refused: E4A plan contract drifted")
    return plan


def execute_item(root: Path, item: dict) -> dict:
    import resource

    from rs_constraint_lab.durable import atomic_write_json

    started = time.perf_counter()

    def payload(result, status):
        return {"item": item, "item_id": item["item_id"], "peak_rss_mb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, "result": result, "status": status, "wall_seconds": time.perf_counter() - started}

    def on_main(result, _):
        atomic_write_json(root / "items" / f"{item['item_id']}.partial.json", payload(result, "complete_checks_interrupted"))

    result, _ = analyse_item(item, on_main=on_main)
    atomic_write_json(root / "items" / f"{item['item_id']}.json", payload(result, "complete"))
    partial = root / "items" / f"{item['item_id']}.partial.json"
    if partial.exists():
        partial.unlink()
    return {}


def run(root: Path, plan: dict, *, workers: int = WORKERS, **kwargs) -> list[dict]:
    return gte1.run(root, plan, workers=workers, watchdogs=kwargs.pop("watchdogs", WATCHDOG_SECONDS), wall_cap=kwargs.pop("wall_cap", ROUND_WALL_CAP_SECONDS), module=kwargs.pop("module", "rs_constraint_lab.gte4a"), **kwargs)


def publish(root: Path, plan: dict, out: Path, *, frozen_plan_commit: str, e0b_tables: Path) -> str:
    from rs_constraint_lab.durable import atomic_write_json, canonical_json, read_json, sha256_bytes

    records = {}
    for it in plan["items"]:
        path = root / "items" / f"{it['item_id']}.json"
        records[it["item_id"]] = read_json(path) if path.is_file() else {"item_id": it["item_id"], "status": "missing"}
    results = {k: v["result"] for k, v in records.items() if "result" in v}
    published = read_json(e0b_tables)["results"]
    assembled = assemble(results, published)
    item_records = {k: {"numerical_problems": check_problems(results[k]) if k in results else None, "peak_rss_mb": v.get("peak_rss_mb_parent_view", v.get("peak_rss_mb")), "role": next(it["role"] for it in plan["items"] if it["item_id"] == k), "scaffold": next(it["scaffold"] for it in plan["items"] if it["item_id"] == k), "status": v["status"], "wall_seconds": v.get("wall_seconds")} for k, v in records.items()}
    payload = {"analysis_version": ANALYSIS_VERSION, "experiment_id": EXPERIMENT_ID, "frozen_analysis_plan_commit": frozen_plan_commit, "item_records": item_records, "plan_hash": plan["plan_hash"], "results": results, "round_id": ROUND_ID, "schema": "rs-gt.e4a-tables/v1", "status_counts": {s: sum(r["status"] == s for r in item_records.values()) for s in sorted({r["status"] for r in item_records.values()})}, **assembled}
    body = dict(payload)
    body["payload_sha256"] = sha256_bytes(canonical_json(payload).encode("utf-8"))
    atomic_write_json(out, body)
    return body["payload_sha256"]


def render_atlas(repo: Path, tables: Path | None = None, *, title: str = "GT-E4A native held-reference atlas", tables_rel: str = TABLES_RELPATH, scaffold_order: tuple[str, ...] = SCAFFOLD_ORDER) -> str:
    import json

    t = json.loads((tables or repo / tables_rel).read_text())
    f = lambda v, d=3: "—" if v is None else (f"{v:+.1e}" if isinstance(v, float) and v != 0 and abs(v) < 1e-3 else (f"{v:+.{d}f}" if isinstance(v, float) else str(v)))
    L = [f"# {title}", "", f"Generated from `{tables_rel}` (payload `{t['payload_sha256'][:12]}…`), frozen plan `{t['frozen_analysis_plan_commit'][:7]}`. Every cell is listed. Margins are against each scaffold's own NULL r0 = k(N−k)/M. K3 cells are replications of published E0B cells.", ""]
    groups: dict[str, list] = {}
    for k, c in t["frozen_expectations"].items():
        groups.setdefault(k.split("-")[0], []).append(c["holds"])
    L += ["Identities and acceptance: " + "; ".join(f"**{z}** {sum(v)}/{len(v)}" for z, v in sorted(groups.items())) + ".", ""]
    fails = [(k, c) for k, c in t["frozen_expectations"].items() if not c["holds"]]
    if fails:
        L += ["Checks not holding: " + "; ".join(f"{k} ({c.get('problems') or c.get('reason') or ''})" for k, c in fails) + ".", ""]
    L += ["## Geometry (own NULL)", "", "| Scaffold-N | k | held | free M | attachment slots | r0 | analytic floor per source vertex |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for key, g in t["geometry"].items():
        L.append(f"| {key} | {g['source_vertices']} | {g['held_edges']} | {g['free_slots']} | {g['attachment_slots']} | {g['r0']:.4f} | {t['analytic_floor'][key]} |")
    L += ["", "## Item records", "", "| Item | Role | Status | Wall s | Peak MB | Problems |", "| --- | --- | --- | --- | --- | --- |"]
    for k, rec in t["item_records"].items():
        L.append(f"| {k} | {rec['role']} | {rec['status']} | {rec['wall_seconds']:.1f} | {rec['peak_rss_mb']:.0f} | {'; '.join(rec['numerical_problems'] or []) or 'none'} |")
    L += ["", "## Scaffold comparison by family and size", ""]
    for fam, row in t["comparisons"]["scaffold_table"].items():
        L += [f"**{fam}**", "", "| Channel | " + " | ".join(scaffold_order) + " |", "| --- |" + " --- |" * len(scaffold_order)]
        for c in DECLARED:
            L.append(f"| {c} | " + " | ".join(f(row[sc][c]) if row[sc] else "—" for sc in scaffold_order) + " |")
        L.append("")
    L += ["## Source orbits, chord and witnesses", "", "Per cell and clock: per-slot attachment occupancy, per-slot attachment activity and mean witnesses per attachment slot (held floor / chord-internal / other) for each source orbit; P3 chord occupancy and attachment conditional on the chord.", ""]
    for k, p in t["comparisons"]["profiles"].items():
        if p is None:
            L.append(f"- **{k}**: unresolved")
            continue
        parts = []
        for clock in ("continuous", "jump"):
            orb = p["orbits"][clock]
            s = "; ".join(f"orbit {o}: occ {v['attachment_occupancy_per_slot']:.3f}, act {v['attachment_activity_per_slot']:.3f}, wit {v['witness_means_per_slot']['held_floor']:.2f}/{v['witness_means_per_slot']['chord_internal']:.2f}/{v['witness_means_per_slot']['other']:.2f}" for o, v in orb.items())
            ch = p["chord"][clock]
            if ch:
                cp, ca = ch["conditional"]["chord_present"], ch["conditional"]["chord_absent"]
                s += f"; chord occ {ch['occupancy']:.3f}, att|chord {f(cp['attachment_fraction'] if cp else None)}, att|no chord {f(ca['attachment_fraction'] if ca else None)}"
                if cp and ca:
                    s += ", orbit occ|chord " + ", ".join(f"{o} {cp['orbit_attachment_occupancy_per_slot'][o]:.3f}/{ca['orbit_attachment_occupancy_per_slot'][o]:.3f}" for o in cp["orbit_attachment_occupancy_per_slot"])
            parts.append(f"{clock}: {s}")
        ov = p["standardised_overlap"]
        parts.append(f"standardised-margin overlap (ct): NULL weight on rare k {ov['continuous']['null_weight_on_rare_k']:.3f}, low {ov['continuous']['null_weight_on_low_k']:.3f}, supported k {ov['continuous']['supported_k_range']}")
        L.append(f"- **{k}** — " + " | ".join(parts))
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m rs_constraint_lab.gte4a")
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
        raise SystemExit("item is not in the E4A manifest")
    execute_item(root, item)
    return 0


if __name__ == "__main__":
    sys.exit(main())
