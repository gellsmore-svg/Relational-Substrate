"""Gravity-time programme, Round E1 (prompt GT-P004, OTR 1.0): option B.

Chosen in the GT-P003 pre-freeze review (gravity-time/docs/e1-design-alternatives.md)
and authorised by the human researcher in GT-P004.

* Tranche I: the eight E0B W4 cells at HELD N=7 (six non-gradient families,
  the NULL identity control and the CLOSEW gradient control).
* Tranche II: the six non-gradient families under the existing W3 and W16
  sensitivity alphabets at HELD N=5 and N=6 (a within-grammar strength
  bracket: every log-factor x 1.585 or x 2).
* Baselines: the eight families at HELD N=5 and N=6 under W4, re-derived by
  gtobs so that every comparison uses one observable implementation. These
  cells were published in E0B and are not new observations.

One cell: gtkernel chain -> gtobs.stationary (two starts) -> gtobs.analyse
with that law -> round channels (fixed handover index) -> numerical checks
(a third start, a long-double per-entry residual, the GTH referee where
dense is feasible, and the rule strings evaluated on a seeded state sample).
Each cell runs in its own process under a wall watchdog, so that a slow
cell is recorded as unresolved instead of stalling the round.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import resource
import signal
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

from rs_constraint_lab import gte0a, gte0b, gtkernel, gtobs
from rs_constraint_lab.gte0a import SOURCE
from rs_constraint_lab.state import edges
from rs_constraint_lab.weights import alphabet_factors

ROUND_ID = "round-e1"
EXPERIMENT_ID = "gt-round-e1-scale-and-strength"
ANALYSIS_VERSION = "gt-e1/v1"
PROMPT_ID = "GT-P004"
MODE = "HELD"

FAMILY_ORDER = ("CSPH", "CSPF", "CWPH", "CWPF", "PATHF", "PATHH", "NULL", "CLOSEW")
FAMILIES: dict[str, dict[str, list[tuple[str, str]]]] = {f: dict(gte0b.FAMILIES[f]) for f in FAMILY_ORDER}
NON_GRADIENT = FAMILY_ORDER[:6]
COMPOSITES = ("CSPH", "CSPF", "CWPH", "CWPF")
SINGLE_COMPONENT = ("PATHF", "PATHH")
NATIVE_N = 7
BRACKET_SIZES = (5, 6)
BRACKET_ALPHABETS = ("W3", "W16")
BASELINE_SIZES = (5, 6)
EQUAL_RATIO_PAIRS = (("CWPF", "CWPH"), ("CSPF", "CSPH"), ("PATHF", "PATHH"))


def log_strength(alphabet: str) -> float:
    """Log-factor scale of an alphabet relative to W4 (W4 = 1, W3 = log2 3, W16 = 2)."""
    return math.log(float(alphabet_factors(alphabet)["weak_favour"])) / math.log(2.0)


# --- frozen numerical policy ---------------------------------------------------------------

WATCHDOG_SECONDS = {5: 900, 6: 900, 7: 3600}
ROUND_WALL_CAP_SECONDS = 4 * 3600
WORKERS = 4
CHILD_THREAD_ENV = {"MKL_NUM_THREADS": "1", "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1"}
IDENTITY_TOLERANCE = 1e-9
REVERSIBLE_FLUX_TOLERANCE = gte0a.REVERSIBLE_FLUX_TOLERANCE
NON_REVERSIBLE_FLOOR = 1e-6
FRAME_REVERSIBLE_TOLERANCE = 1e-9
REPLICATION_ABS = 1e-10
REPLICATION_REL = 1e-8
REFEREE_L1 = 1e-10
REFEREE_MAX_RELATIVE = 1e-8
REFEREE_CHANNEL_ABS = 1e-10
RESIDUAL_MAX_RELATIVE = 1e-9
KERNEL_SAMPLE = 400
KERNEL_RELATIVE_TOLERANCE = 1e-12
RARE_MASS_FLOOR = 1e-12
LOW_MASS_FLOOR = 1e-6
NEGLIGIBLE_CHANGE = 1e-3
COMPARABLE_RATIO = (0.5, 2.0)
PROXY_SHARE = 2.0 / 3.0

FINAL_STATUSES = ("complete", "complete_checks_interrupted", "unresolved_watchdog", "failed", "interrupted_wall_cap", "not_started_wall_cap")


def grade_of(family: str) -> str:
    (grade,) = FAMILIES[family]
    return grade


def item_id(n: int, alphabet: str, family: str) -> str:
    return f"{MODE}-N{n}-{alphabet}-{family}-{grade_of(family)}"


def items() -> list[dict]:
    """Execution order: tranche I, then the published baselines, then tranche II."""
    out = []
    for family in FAMILY_ORDER:
        role = "identity_control_exposed" if family == "NULL" else ("gradient_control" if family == "CLOSEW" else "open_scientific")
        out.append({"alphabet": "W4", "family": family, "grade": grade_of(family), "item_id": item_id(NATIVE_N, "W4", family), "mode": MODE, "n": NATIVE_N, "role": role, "tranche": "I"})
    for n in BASELINE_SIZES:
        for family in FAMILY_ORDER:
            out.append({"alphabet": "W4", "family": family, "grade": grade_of(family), "item_id": item_id(n, "W4", family), "mode": MODE, "n": n, "role": "baseline_rederivation_published", "tranche": "baseline"})
    for n in BRACKET_SIZES:
        for alphabet in BRACKET_ALPHABETS:
            for family in NON_GRADIENT:
                out.append({"alphabet": alphabet, "family": family, "grade": grade_of(family), "item_id": item_id(n, alphabet, family), "mode": MODE, "n": n, "role": "open_scientific_bracket", "tranche": "II"})
    return out


def authorised_cells() -> list[dict]:
    return [it for it in items() if it["tranche"] in ("I", "II")]


# --- one cell ---------------------------------------------------------------------------------

HANDOVER_STEPS = (("F", "P", "F", "A"), ("F", "A", "D", "P"), ("D", "P", "D", "A"), ("D", "A", "F", "P"))
FLIP = {"F": "D", "D": "F"}


def handover_statistics(probs: dict[tuple, float]) -> dict:
    """Fixed handover index from the full event-pair table (source frame).

    The E0 handover is the cycle probe-probe forms (FP) -> attachment forms
    (FA) -> probe-probe dissolves (DP) -> attachment dissolves (DA). Each of
    its four consecutive steps is compared with its time reverse
    (t1 c1 t2 c2 -> flip(t2) c2 flip(t1) c1). The index is the sum of the
    four forward-minus-reverse probabilities; positive means the E0
    orientation, negative the reverse orientation, ~0 no handover.
    """
    steps = {}
    index = {"adjacent": 0.0, "disjoint": 0.0}
    forward = 0
    for t1, c1, t2, c2 in HANDOVER_STEPS:
        rev = (FLIP[t2], c2, FLIP[t1], c1)
        for rel in ("adjacent", "disjoint"):
            f = probs.get((t1, c1, t2, c2, rel), 0.0)
            b = probs.get(rev + (rel,), 0.0)
            steps[f"{t1}{c1}{t2}{c2}:{rel}"] = {"difference": f - b, "forward": f, "reverse": b}
            index[rel] += f - b
            if rel == "adjacent" and f - b > 0:
                forward += 1
    return {"forward_oriented_adjacent_steps": forward, "index_adjacent": index["adjacent"], "index_all": index["adjacent"] + index["disjoint"], "index_disjoint": index["disjoint"], "steps": steps}


def _factors(alphabet: str) -> dict | None:
    """None keeps gtkernel's W4 default (bit-identical to every earlier GT round)."""
    return None if alphabet == "W4" else alphabet_factors(alphabet)


def headline_from_law(chain, n: int, ct: np.ndarray, jump: np.ndarray, D: np.ndarray, arrays: dict) -> dict:
    """The attachment and irreversibility channels under a given law (for the referee comparison)."""
    hc = gtobs.held_observables(chain, ct, n, D, per_unit_time=True)
    hj = gtobs.held_observables(chain, jump, n, D)
    add = gtobs.held_additions(chain, ct, jump, n, D, arrays)
    rev = gte0a.reversibility(chain, ct, float(ct @ chain.rates))
    return {
        "attachment_fraction_ct": hc["attachment_fraction"],
        "attachment_fraction_jump": hj["attachment_fraction"],
        "detached_fraction_ct": hc["distance_distribution"].get("inf", 0.0),
        "entropy_production_per_event": rev["entropy_production_per_event"],
        "irreversible_flux_fraction": rev["irreversible_flux_fraction"],
        "margin_standardised_ct": add["continuous"]["attachment_margin_null_density_standardised"],
        "margin_standardised_jump": add["jump"]["attachment_margin_null_density_standardised"],
    }


def _law_difference(a: np.ndarray, b: np.ndarray) -> dict:
    positive = a > 0
    return {"l1": float(np.abs(a - b).sum()), "max_relative": float((np.abs(a - b)[positive] / a[positive]).max()) if positive.any() else None}


def long_double_residual(chain, jump: np.ndarray) -> dict:
    """Per-entry relative residual |(pi P)_i - pi_i| / pi_i in extended precision, and zero-mass states."""
    P = (chain.W / chain.rates[:, None]).astype(np.longdouble)
    pi = jump.astype(np.longdouble)
    valid = chain.T >= 0
    pred, _ = gtobs._incoming(chain, chain.W / chain.rates[:, None])
    moved = np.zeros(len(pi), dtype=np.longdouble)
    for e in range(chain.n_slots):
        p_in = np.where(valid[:, e], P[pred[:, e], e], 0)
        moved += pi[pred[:, e]] * p_in
    positive = pi > 0
    rel = np.abs(moved - pi)[positive] / pi[positive]
    return {"max_relative": float(rel.max()) if positive.any() else None, "min_mass": float(pi.min()), "zero_mass_states": int((~positive).sum())}


def kernel_sample_check(item: dict, chain, start: int, *, families: dict | None = None, round_id: str = ROUND_ID) -> dict:
    """The rule strings, evaluated with exact Fractions on a seeded sample of states, against gtkernel."""
    from rs_constraint_lab.constraints import Choreography

    n, family, grade = item["n"], item["family"], item["grade"]
    factors = alphabet_factors(item.get("alphabet", "W4"))
    choreography = Choreography(0, 0, gte0a.rules_for(family, grade, n, item.get("mode", MODE), families or FAMILIES))
    seed = int(hashlib.sha256(f"{round_id}:kernel:{item['item_id']}".encode()).hexdigest()[:16], 16)
    rng = np.random.default_rng(seed)
    size = len(chain.states)
    edge_totals = ((chain.states[:, None] >> np.arange(chain.n_slots)) & 1).sum(axis=1)
    chosen = set(rng.choice(size, size=min(KERNEL_SAMPLE, size), replace=False).tolist()) | {start, int(np.argmax(edge_totals))}
    worst = 0.0
    zero_mismatch = 0
    target_mismatch = 0
    for i in sorted(chosen):
        state = int(chain.states[i])
        active = choreography.active(state, (), {})
        for e in range(chain.n_slots):
            weight = Fraction(1)
            for constraint in active:
                if constraint.matches(state, e):
                    weight *= factors[constraint.weight]
            ref, got = float(weight), float(chain.W[i, e])
            if ref == 0.0 or got == 0.0:
                zero_mismatch += int(ref != got)
            else:
                worst = max(worst, abs(got - ref) / ref)
            t = int(chain.T[i, e])
            if t >= 0 and int(chain.states[t]) != state ^ (1 << e):
                target_mismatch += 1
            if t < 0 and got > 0:
                target_mismatch += 1
    return {"max_relative_weight_difference": worst, "sampled_states": len(chosen), "seed": seed, "target_mismatches": target_mismatch, "zero_pattern_mismatches": zero_mismatch}


def analyse_item(item: dict, *, with_trajectories: bool = True, checks: bool = True, on_main=None) -> tuple[dict, dict | None]:
    n, alphabet, family, grade = item["n"], item["alphabet"], item["family"], item["grade"]
    factors = _factors(alphabet)
    started = time.perf_counter()
    chain, kernel_timing = gtkernel.reachable_chain(n, MODE, FAMILIES[family][grade], factors)
    start = gtobs.start_index(chain, n, MODE)
    regime = gtobs.class_regime(chain, start)
    stat = gtobs.stationary(chain, start, cross_check=True) if regime["regime"] == "recurrent" else None
    result, trajectories = gtobs.analyse(chain, family=family, grade=grade, n=n, mode=MODE, families=FAMILIES, factors=factors, item_id=item["item_id"], round_id=ROUND_ID, with_trajectories=with_trajectories, stationary_override=stat)
    result["alphabet"] = alphabet
    result["kernel_timing"] = kernel_timing
    result["spectrum_status"] = "unavailable: gtobs does not form the dense generator at any N (GT-P003); not zero, not compared"
    round_block: dict = {"analysis_version": ANALYSIS_VERSION}
    resolved = stat is not None and stat.get("resolved")
    if resolved:
        t0 = time.perf_counter()
        round_block["handover"] = handover_statistics(gtobs.event_pattern_probabilities(chain, stat["jump"], n, MODE))
        round_block["handover_seconds"] = time.perf_counter() - t0
    result["e1_round"] = round_block
    result["timings"]["main_total"] = time.perf_counter() - started
    if on_main is not None:
        on_main(result, trajectories)
    if checks:
        t0 = time.perf_counter()
        result["e1_round"]["checks"] = numerical_checks(item, chain, start, stat if resolved else None)
        result["timings"]["checks"] = time.perf_counter() - t0
    return result, trajectories


def numerical_checks(item: dict, chain, start: int, stat: dict | None) -> dict:
    n = item["n"]
    out: dict = {"kernel_sample": kernel_sample_check(item, chain, start)}
    if stat is None:
        return out
    ct, jump = stat["ct"], stat["jump"]
    R = chain.rates
    P = chain.W / R[:, None]
    pred, p_in = gtobs._incoming(chain, P)
    edge_totals = ((chain.states[:, None] >> np.arange(chain.n_slots)) & 1).sum(axis=1)
    far = int(np.argmax(edge_totals))
    point = np.zeros(len(R))
    point[far] = 1.0
    t0 = time.perf_counter()
    third, iterations, _, relative = gtobs._lazy_power(pred, p_in, point, gtobs.STATIONARY_TOLERANCE, gtobs.STATIONARY_CAP)
    third = np.clip(third, 0.0, None)
    third /= third.sum()
    out["third_start"] = {"iterations": iterations, "last_max_relative_change": relative, "seconds": time.perf_counter() - t0, "start_state": int(chain.states[far]), **_law_difference(jump, third)}
    out["long_double_residual"] = long_double_residual(chain, jump)
    arrays = gtobs.structure_arrays(chain, n)
    D = gtobs.source_distances(chain.states, n)
    main = headline_from_law(chain, n, ct, jump, D, arrays)
    referees = {"third_start": (lambda: (third / R / (third / R).sum(), third))}
    if len(chain.states) <= gtobs.DENSE_LIMIT:
        def gth():
            from rs_constraint_lab import gtobs_validate

            law = gtobs_validate.gth_stationary(chain)
            return law["ct"], law["jump"]

        referees["gth"] = gth
    for name, make in referees.items():
        t0 = time.perf_counter()
        rct, rjump = make()
        other = headline_from_law(chain, n, rct, rjump, D, arrays)
        diffs = {k: abs(main[k] - other[k]) for k in main if main[k] is not None and other[k] is not None}
        out.setdefault("referees", {})[name] = {"channel_max_abs_difference": max(diffs.values()) if diffs else None, "ct": _law_difference(ct, rct), "jump": _law_difference(jump, rjump), "seconds": time.perf_counter() - t0}
    return out


def check_problems(result: dict) -> list[str]:
    """Frozen per-cell numerical acceptance; a failure marks the cell, it never changes its values."""
    problems = []
    st = result.get("stationary") or {}
    if result.get("regime") != "recurrent":
        problems.append(f"regime {result.get('regime')}")
        return problems
    if not st.get("resolved"):
        problems.append(f"stationary unresolved: {st.get('reason')}")
        return problems
    if st["residual"] > gtobs.STATIONARY_RESIDUAL_TOLERANCE:
        problems.append("stationary residual")
    if result.get("symmetry_max_abs_difference") is not None and result["symmetry_max_abs_difference"] > gte0a.SYMMETRY_TOLERANCE:
        problems.append("symmetry")
    diag = result.get("autocorrelation_diagnostics") or {}
    if diag.get("cap_reached"):
        problems.append("autocorrelation cap reached")
    checks = (result.get("e1_round") or {}).get("checks")
    if checks is None:
        problems.append("numerical checks not completed")
        return problems
    ks = checks["kernel_sample"]
    if ks["max_relative_weight_difference"] > KERNEL_RELATIVE_TOLERANCE or ks["zero_pattern_mismatches"] or ks["target_mismatches"]:
        problems.append("kernel sample check")
    ld = checks.get("long_double_residual") or {}
    if ld.get("zero_mass_states"):
        problems.append("zero-mass reachable states (underflow or clipping)")
    if ld.get("max_relative") is not None and ld["max_relative"] > RESIDUAL_MAX_RELATIVE:
        problems.append("per-entry relative residual")
    for name, ref in (checks.get("referees") or {}).items():
        for clock in ("ct", "jump"):
            if ref[clock]["l1"] > REFEREE_L1 or (ref[clock]["max_relative"] or 0.0) > REFEREE_MAX_RELATIVE:
                problems.append(f"referee {name} {clock} law")
        if ref["channel_max_abs_difference"] is not None and ref["channel_max_abs_difference"] > REFEREE_CHANNEL_ABS:
            problems.append(f"referee {name} channels")
    return problems


# --- channels and comparisons ---------------------------------------------------------------

DECLARED_CHANNELS = (
    "margin_raw_ct", "margin_raw_jump",
    "margin_standardised_ct", "margin_standardised_jump",
    "margin_normalised_ct", "margin_normalised_jump",
    "detached_fraction_ct", "detached_fraction_jump",
    "free_edge_density_ct", "free_edge_density_jump",
    "irreversible_flux_fraction", "entropy_production_per_event",
    "event_order_asymmetry", "handover_index_adjacent",
    "near_far_ratio_jump", "near_far_ratio_ct",
    "hub_probe_only",
)


def channels(r: dict) -> dict | None:
    """The scalar behaviour profile of one resolved cell (no weighting, no aggregate score)."""
    if r.get("regime") != "recurrent" or not (r.get("stationary") or {}).get("resolved"):
        return None
    hc, hj = r["held_continuous"], r["held_jump"]
    add = r["e1_additions"]["held"]
    r0 = hc["null_attachment_fraction"]
    out: dict = {"null_attachment_fraction": r0, "source_share": len(SOURCE) / r["n"]}
    for clock, h, a in (("ct", hc, add["continuous"]), ("jump", hj, add["jump"])):
        af = h["attachment_fraction"]
        out[f"attachment_fraction_{clock}"] = af
        out[f"margin_raw_{clock}"] = None if af is None else af - r0
        out[f"margin_normalised_{clock}"] = None if af is None or r0 >= 1.0 else (af - r0) / (1.0 - r0)
        out[f"margin_standardised_{clock}"] = a["attachment_margin_null_density_standardised"]
        out[f"detached_fraction_{clock}"] = h["distance_distribution"].get("inf", 0.0)
        out[f"free_edge_density_{clock}"] = h["expected_free_edges"] / h["free_slots"]
        out[f"capture_rate_when_detached_{clock}"] = h["capture_rate_when_detached"]
        out[f"detached_probe_count_distribution_{clock}"] = a["detached_probe_count_distribution"]
    sa = r["shell_activity"]
    out["near_far_ratio_jump"] = sa["jump"]["near_far_ratio"]
    out["near_far_ratio_ct"] = sa["continuous"]["near_far_ratio"]
    rev = r["reversibility"]
    for k in ("irreversible_flux_fraction", "entropy_production_per_event", "entropy_production_per_time", "max_square_affinity", "nonzero_affinity_squares", "one_sided_transitions"):
        out[k] = rev[k]
    out["event_order_asymmetry"] = r["event_order"]["pattern_asymmetry"]
    out["immediate_reversal_probability"] = r["event_order"]["immediate_reversal_probability"]
    ho = r["e1_round"].get("handover") or {}
    out["handover_index_adjacent"] = ho.get("index_adjacent")
    out["handover_index_all"] = ho.get("index_all")
    out["handover_forward_oriented_adjacent_steps"] = ho.get("forward_oriented_adjacent_steps")
    out["hub_frame_asymmetry"] = r["hub_frame"]["event_order"]["pattern_asymmetry"]
    out["hub_frame_net_current"] = r["hub_frame"]["projected_current"]["net_flux_fraction"]
    out["projected_net_current"] = r["projected_current"]["net_flux_fraction"]
    hs = r["e1_additions"]["hub_structure_ct"]
    out["hub_probe_only"] = hs["hub_probe_only"]
    out["hub_includes_source"] = hs["hub_includes_source"]
    out["expected_edges"] = r["occupancy_ct"]["expected_edges"]
    out["expected_triangles"] = r["occupancy_ct"]["expected_triangles"]
    out["full_centre_probability"] = r["occupancy_ct"]["full_centre_probability"]
    ac = r.get("autocorrelation") or {}
    for key in ("attached_probe", "detached_probe", "free_edges", "degree_probe"):
        v = ac.get(key)
        out[f"tau_{key}_time"] = v["time"] if v else None
        out[f"tau_{key}_events"] = v["events"] if v else None
    out["localisation_persistence_index"] = r.get("localisation_persistence_index")
    out["mean_rate_ct"] = r["mean_rate_ct"]
    return out


def rare_mass_flags(r: dict) -> dict:
    """Conditional channels whose conditioning mass is rare (< 1e-12: not interpreted) or low (< 1e-6)."""
    flags = {"low": [], "rare": []}
    if r.get("regime") != "recurrent" or "held_continuous" not in r:
        return flags

    def note(path: str, mass: float) -> None:
        if mass < RARE_MASS_FLOOR:
            flags["rare"].append({"mass": mass, "path": path})
        elif mass < LOW_MASS_FLOOR:
            flags["low"].append({"mass": mass, "path": path})

    for key in ("held_continuous", "held_jump"):
        h = r[key]
        masses = h["free_edge_count_distribution"]
        for k, v in h["attachment_fraction_by_free_edge_count"].items():
            if v is not None:
                note(f"{key}/attachment_fraction_by_free_edge_count/{k}", masses[k])
        for shell, mass in h["distance_distribution"].items():
            note(f"{key}/distance_distribution/{shell}", mass)
    for clock in ("jump", "continuous"):
        for shell, mass in r["shell_activity"][clock]["shell_mass"].items():
            note(f"shell_activity/{clock}/shell_mass/{shell}", mass)
    return flags


def _sign(x: float) -> int:
    return (x > 0) - (x < 0)


def classify_calibration(c5w4: float | None, c5w16: float | None, c6w4: float | None) -> dict:
    """Does doubling the log-strength at N=5 reproduce the published N=5 -> N=6 step on this channel?"""
    if None in (c5w4, c5w16, c6w4):
        return {"class": "unavailable"}
    ds, dw = c6w4 - c5w4, c5w16 - c5w4
    row = {"size_step": ds, "strength_step": dw}
    if abs(ds) < NEGLIGIBLE_CHANGE and abs(dw) < NEGLIGIBLE_CHANGE:
        row["class"] = "both_negligible"
    elif abs(ds) < NEGLIGIBLE_CHANGE:
        row["class"] = "size_step_negligible"
    elif abs(dw) < NEGLIGIBLE_CHANGE:
        row["class"] = "strength_step_negligible"
    elif _sign(ds) != _sign(dw):
        row["class"] = "opposite"
    else:
        ratio = dw / ds
        row["ratio"] = ratio
        row["class"] = "same_sign_comparable_size" if COMPARABLE_RATIO[0] <= ratio <= COMPARABLE_RATIO[1] else "same_sign_different_size"
    return row


def proxy_verdict(rows: dict[str, dict]) -> dict:
    """Frozen family-level reading of the calibration; the per-channel rows are always reported."""
    judged = [r for r in rows.values() if r["class"] not in ("unavailable", "both_negligible", "size_step_negligible")]
    if not judged:
        return {"judged_channels": 0, "verdict": "no_non_negligible_size_step"}
    comparable = sum(r["class"] == "same_sign_comparable_size" for r in judged)
    same = sum(r["class"] in ("same_sign_comparable_size", "same_sign_different_size") for r in judged)
    if comparable / len(judged) >= PROXY_SHARE:
        verdict = "usable_proxy"
    elif same / len(judged) >= PROXY_SHARE:
        verdict = "direction_only_proxy"
    else:
        verdict = "poor_proxy"
    return {"comparable": comparable, "judged_channels": len(judged), "same_sign": same, "verdict": verdict}


def classify_n7(c6w4: float | None, c6w3: float | None, c6w16: float | None, c7w4: float | None) -> dict:
    """Is the N=6 -> N=7 step on this channel in the direction (and range) of strengthening at N=6?"""
    if None in (c6w4, c6w3, c6w16, c7w4):
        return {"class": "unavailable"}
    d7, d3, d16 = c7w4 - c6w4, c6w3 - c6w4, c6w16 - c6w4
    row = {"size_step": d7, "strength_step_w3": d3, "strength_step_w16": d16}
    responses = [d for d in (d3, d16) if abs(d) >= NEGLIGIBLE_CHANGE]
    if abs(d7) < NEGLIGIBLE_CHANGE:
        row["class"] = "size_step_negligible"
    elif not responses:
        row["class"] = "no_strength_response"
    elif len(responses) == 2 and _sign(d3) != _sign(d16):
        row["class"] = "strength_response_non_monotone"
    elif _sign(d7) != _sign(responses[0]):
        row["class"] = "opposite_to_strength_response"
    else:
        lo = COMPARABLE_RATIO[0] * min(abs(d) for d in responses)
        hi = COMPARABLE_RATIO[1] * max(abs(d) for d in responses)
        row["class"] = "same_sign_within_bracket_range" if lo <= abs(d7) <= hi else "same_sign_outside_bracket_range"
    return row


def engagement(r: dict) -> dict:
    census = (r.get("e1_additions") or {}).get("witness_census_jump") or {}
    return {k: {"event_share": v["event_share"], "mean_log_weight": v["mean_log_weight"], "mean_witnesses": v["mean_witnesses"]} for k, v in census.items()}


def assemble(results: dict[str, dict], published: dict[str, dict]) -> dict:
    by_key = {(r["n"], r["alphabet"], r["family"]): r for r in results.values() if "n" in r}
    profile = {k: channels(r) for k, r in results.items()}

    def ch(n, alphabet, family, name):
        r = by_key.get((n, alphabet, family))
        p = profile.get(item_id(n, alphabet, family)) if r else None
        return None if p is None else p.get(name)

    checks: dict[str, dict] = {}
    for key, r in results.items():
        p = profile.get(key)
        fam = r.get("family")
        if p is None:
            continue
        if fam == "NULL":
            uniform = 1.0 / r["reachable_states"]
            l1 = sum(abs(row["ct"] - row["orbit_size"] * uniform) for row in r["class_table"])
            margins = [abs(p[f"margin_{f}_{c}"]) for f in ("raw", "standardised") for c in ("ct", "jump")]
            checks[f"Z1-{key}"] = {"holds": l1 <= IDENTITY_TOLERANCE and p["irreversible_flux_fraction"] <= REVERSIBLE_FLUX_TOLERANCE and max(margins) <= IDENTITY_TOLERANCE, "irreversible_flux_fraction": p["irreversible_flux_fraction"], "l1_to_uniform": l1, "max_abs_margin": max(margins)}
        if fam == "CLOSEW":
            gap = r.get("predicted_law_l1_gap")
            checks[f"Z2-{key}"] = {"holds": gap is not None and gap <= IDENTITY_TOLERANCE and p["irreversible_flux_fraction"] <= REVERSIBLE_FLUX_TOLERANCE, "irreversible_flux_fraction": p["irreversible_flux_fraction"], "l1_gap": gap}
        if fam in NON_GRADIENT:
            checks[f"Z3-{key}"] = {"holds": p["max_square_affinity"] > NON_REVERSIBLE_FLOOR, "irreversible_flux_fraction": p["irreversible_flux_fraction"], "max_square_affinity": p["max_square_affinity"]}
        if fam in ("NULL", "CLOSEW"):
            checks[f"Z6-{key}"] = {"holds": p["hub_frame_asymmetry"] <= FRAME_REVERSIBLE_TOLERANCE and p["hub_frame_net_current"] <= FRAME_REVERSIBLE_TOLERANCE, "hub_frame_net_current": p["hub_frame_net_current"], "hub_frame_pattern_asymmetry": p["hub_frame_asymmetry"]}
    for key, r in results.items():
        if r.get("alphabet") == "W4" and r.get("n") in BASELINE_SIZES:
            old = published.get(f"{MODE}-N{r['n']}-{r['family']}-{r['grade']}")
            checks[f"Z4-{key}"] = replication_check(r, old)
    for key, r in results.items():
        if "n" not in r:
            continue
        problems = check_problems(r)
        checks[f"Z5-{key}"] = {"holds": not problems, "problems": problems}

    size_sequence = {f: {f"N{n}": profile.get(item_id(n, "W4", f)) for n in (5, 6, 7)} for f in FAMILY_ORDER}
    strength_response = {}
    for f in NON_GRADIENT:
        for n in BRACKET_SIZES:
            rows = {}
            for name in DECLARED_CHANNELS:
                values = [ch(n, a, f, name) for a in ("W4", "W3", "W16")]
                monotone = None
                if None not in values:
                    d1, d2 = values[1] - values[0], values[2] - values[1]
                    monotone = _sign(d1) == _sign(d2) or abs(d1) < NEGLIGIBLE_CHANGE or abs(d2) < NEGLIGIBLE_CHANGE
                rows[name] = {"W16": values[2], "W3": values[1], "W4": values[0], "monotone_in_log_strength": monotone}
            strength_response[f"{f}-N{n}"] = rows
    calibration = {}
    for f in NON_GRADIENT:
        rows = {name: classify_calibration(ch(5, "W4", f, name), ch(5, "W16", f, name), ch(6, "W4", f, name)) for name in DECLARED_CHANNELS}
        calibration[f] = {"channels": rows, "clean_case": f in SINGLE_COMPONENT, **proxy_verdict(rows)}
    n7_reading = {}
    for f in NON_GRADIENT:
        rows = {name: classify_n7(ch(6, "W4", f, name), ch(6, "W3", f, name), ch(6, "W16", f, name), ch(7, "W4", f, name)) for name in DECLARED_CHANNELS}
        tally: dict[str, int] = {}
        for row in rows.values():
            tally[row["class"]] = tally.get(row["class"], 0) + 1
        n7_reading[f] = {"calibration_verdict": calibration[f]["verdict"], "channels": rows, "class_counts": tally}
    engaged = {}
    for f in NON_GRADIENT + ("CLOSEW",):
        cells = {f"N{n}-{a}": engagement(by_key[(n, a, f)]) for (n, a, fam) in by_key if fam == f}
        ratios = {}
        e6, e7 = cells.get("N6-W4", {}), cells.get("N7-W4", {})
        for comp in e7:
            a, b = e6.get(comp, {}).get("mean_log_weight"), e7[comp].get("mean_log_weight")
            if a and b:
                ratio = b / a
                ratios[comp] = {"n7_over_n6_mean_log_weight": ratio, "position_against_bracket": "below_W3" if ratio < log_strength("W3") else ("above_W16" if ratio > log_strength("W16") else "within_W3_W16")}
        engaged[f] = {"cells": dict(sorted(cells.items())), "n7_over_n6": ratios}
    equal_ratio = {}
    for a, b in EQUAL_RATIO_PAIRS:
        for (n, alphabet) in sorted({(k[0], k[1]) for k in by_key}):
            ra, rb = by_key.get((n, alphabet, a)), by_key.get((n, alphabet, b))
            if ra and rb and "class_table" in ra and "class_table" in rb:
                equal_ratio[f"N{n}-{alphabet}-{a}|{b}"] = {"class_l1": gte0a._class_l1(ra, rb), a: profile.get(ra["item_id"]) if "item_id" in ra else None, b: profile.get(rb["item_id"]) if "item_id" in rb else None}
    reference = {f"N{n}": {"null_attachment_fraction": ch(n, "W4", "NULL", "null_attachment_fraction"), "null_hub_includes_source": ch(n, "W4", "NULL", "hub_includes_source"), "null_hub_probe_only": ch(n, "W4", "NULL", "hub_probe_only"), "source_share": len(SOURCE) / n} for n in (5, 6, 7)}
    return {
        "behaviour_profiles": profile,
        "calibration_n5w16_vs_n6w4": calibration,
        "component_engagement": engaged,
        "equal_ratio": equal_ratio,
        "frozen_expectations": checks,
        "geometric_reference": reference,
        "n7_against_n6_strength_response": n7_reading,
        "rare_mass_flags": {k: rare_mass_flags(r) for k, r in results.items()},
        "size_sequence_w4": size_sequence,
        "strength_response": strength_response,
    }


REPLICATION_CHANNELS = (
    ("held_continuous", "attachment_fraction"),
    ("held_jump", "attachment_fraction"),
    ("reversibility", "irreversible_flux_fraction"),
    ("reversibility", "entropy_production_per_event"),
    ("event_order", "pattern_asymmetry"),
    ("occupancy_ct", "expected_edges"),
    ("hub_frame", "event_order", "pattern_asymmetry"),
)


def replication_check(new: dict, old: dict | None) -> dict:
    if old is None:
        return {"holds": False, "reason": "no published cell"}
    if new.get("regime") != "recurrent" or not (new.get("stationary") or {}).get("resolved"):
        return {"holds": False, "reason": "re-derived cell unresolved"}
    rows = {}
    ok = True
    for path in REPLICATION_CHANNELS:
        a, b = new, old
        for k in path:
            a, b = a[k], b[k]
        good = abs(a - b) <= max(REPLICATION_ABS, REPLICATION_REL * abs(b))
        ok &= good
        rows["/".join(path)] = {"published": b, "rederived": a, "within_tolerance": good}
    return {"channels": rows, "holds": ok}


# --- plan -------------------------------------------------------------------------------------

PLAN_RELPATH = "gravity-time/plans/round-e1-plan.json"
GENERATED_RELPATH = "gravity-time/generated/round-e1"
TABLES_RELPATH = "gravity-time/reports/round-e1-tables.json"
E0B_TABLES_RELPATH = gte0b.TABLES_RELPATH
ONTOLOGY = {"G": 0, "H": 0, "L": 0, "N": [5, 6, 7], "O": 2, "S": 0, "grammar": "ordinary pair DSL"}
REFERENCE_FILES = (
    "research-methods/open-thetical-research.md",
    "gravity-time/provenance/prompts/GT-P004-agent-input.md",
    "gravity-time/docs/e1-design-alternatives.md",
    "gravity-time/reports/gt-e1-prefreeze-review.md",
    "gravity-time/docs/e1-scale-confound-audit.md",
    "gravity-time/docs/e1-held-free-feasibility.md",
    "gravity-time/docs/e1-observables.md",
    "gravity-time/docs/e1-kernel.md",
    "gravity-time/docs/roadmap.md",
    "gravity-time/provenance/execution-GT-P003.md",
    "gravity-time/provenance/e1-observables-validation.log",
    "gravity-time/provenance/e1-fixtures/fx-held-null.json",
    "gravity-time/provenance/e1-fixtures/fx-held-close.json",
    "gravity-time/provenance/e1-fixtures/fx-free-null.json",
    "gravity-time/reports/e1-scale-census.json",
    "gravity-time/reports/e1-engaged-witness-n5-n6.json",
    "gravity-time/reports/e1-margin-decomposition-n5-n6.json",
    "gravity-time/plans/round-e0b-plan.json",
    "gravity-time/reports/round-e0a-tables.json",
    "gravity-time/reports/round-e0b-tables.json",
)


def prepare_plan(repo: Path) -> dict:
    from rs_constraint_lab.durable import sha256_file
    from rs_constraint_lab.explore08 import plan_hash

    cells = items()
    document = {
        "alphabets": {a: {"factors": {g: str(v) for g, v in alphabet_factors(a).items()}, "log_strength_vs_W4": log_strength(a)} for a in ("W4", "W3", "W16")},
        "analysis_only": True,
        "analysis_version": ANALYSIS_VERSION,
        "baseline_sources": {
            "published_tables": E0B_TABLES_RELPATH,
            "published_plan_commit": "50c4b2cb01813fb71d0e4702657fccfbf1535e94",
            "published_result_commit": "d99f97280d42be92f690f53c9152096688076313",
            "qualifications": "GT-F34 (CSPH margin clock- and density-dependent, post hoc) and GT-F35 (E0 rare-mass numerical artefacts) qualify the published N<=6 values; comparisons use the in-round gtobs re-derivations, and the published values are checked against them on robust channels only (Z4)",
        },
        "chosen_because": "GT-P003 pre-freeze review (gravity-time/reports/gt-e1-prefreeze-review.md; gravity-time/docs/e1-design-alternatives.md option B, head 31620b6f6d0ccb1d381a95803c7552d506ae96e3), authorised by the human researcher in GT-P004",
        "clocks": {
            "continuous": "pi_ct = pi_jump / R (event weights as rates); per-unit-time observables",
            "jump": "pi_jump, the stationary law of the embedded jump chain; per-event observables",
            "event_order": "consecutive event pairs on the stationary jump chain",
        },
        "comparisons": {
            "C1_native_size_sequence": "every declared channel at HELD W4 for N=5, 6 (in-round gtobs re-derivations of published cells) and N=7, per family",
            "C2_strength_response": "W4 -> W3 -> W16 at N=5 and N=6 for each non-gradient family; per channel, the three values and whether they are monotone in log-strength (a step below the negligible floor counts as consistent); monotonicity is not presumed",
            "C3_calibration": {
                "contrast": "N=5 W16 (every log-factor x2, matching the path-witness maximum 12 -> 24) against N=6 W4, both relative to N=5 W4, per declared channel",
                "classes": "both_negligible | size_step_negligible | strength_step_negligible | opposite | same_sign_comparable_size (strength/size step ratio in [0.5, 2]) | same_sign_different_size | unavailable",
                "family_verdict": f"among channels whose size step is non-negligible and strength step available: usable_proxy if >= {PROXY_SHARE:.3f} are same_sign_comparable_size; direction_only_proxy if >= {PROXY_SHARE:.3f} share the sign; otherwise poor_proxy",
                "clean_cases": list(SINGLE_COMPONENT),
                "reading_rule": "a poor_proxy family's N=7 strength readings are reported but not used as evidence for or against witness amplification; matching the witness maximum does not match engaged loads, state-space combinatorics or transition laws",
            },
            "C4_n7_against_strength_response": {
                "contrast": "N=6 -> N=7 step at W4 against the W3 and W16 responses at N=6 (the path-witness maximum ratio 40/24 = 1.667 lies between log-strength 1.585 and 2)",
                "classes": "size_step_negligible | no_strength_response | strength_response_non_monotone | opposite_to_strength_response | same_sign_within_bracket_range ([0.5 x smallest, 2 x largest] non-negligible response) | same_sign_outside_bracket_range | unavailable",
            },
            "C5_component_engagement": "per component, event share, mean engaged witnesses and mean engaged log-weight on the jump chain (gtobs witness census) at every cell; N7/N6 mean log-weight ratio placed below W3 (1.585), within W3-W16, or above W16 (2)",
            "C6_geometric_reference": "null attachment fraction r0, source share 3/N and NULL hub rates at N=5, 6, 7, reported beside every margin; neither is separately identified by the N sequence",
            "C7_clock_and_density": "every margin in four forms (raw, ceiling-normalised (af-r0)/(1-r0), null-density-standardised, full a/k profile) in both clocks, side by side; none is primary. The standardised margin is a counterfactual reweighting to the NULL law's free-edge-count distribution and may weight free-edge counts that are rare under the cell's own law; rare-mass flags mark such conditionals",
            "C8_equal_ratio": [list(p) for p in EQUAL_RATIO_PAIRS],
            "declared_channels": list(DECLARED_CHANNELS),
            "negligible_change": NEGLIGIBLE_CHANGE,
            "comparable_ratio": list(COMPARABLE_RATIO),
            "no_aggregate_score": "profiles are reported per channel; no weighted score is formed",
        },
        "controls_and_structural_expectations": {
            "Z1_null_identity": f"NULL at N=5, 6, 7: pi uniform (class-level L1 <= {IDENTITY_TOLERANCE}), irreversible flux <= {REVERSIBLE_FLUX_TOLERANCE}, raw and standardised margins |.| <= {IDENTITY_TOLERANCE} in both clocks (theorem; N=7 previously evaluated as a fixture)",
            "Z2_gradient_control": f"CLOSEW at N=5, 6, 7 (W4): predicted triple-Gibbs law (L1 <= {IDENTITY_TOLERANCE}) and irreversible flux <= {REVERSIBLE_FLUX_TOLERANCE}",
            "Z3_non_gradient_rates": f"every non-gradient cell (all sizes and alphabets): maximum square affinity > {NON_REVERSIBLE_FLOOR}. A rate property of the rules; stationary flux is not predicted (E0A X4 saturation)",
            "Z4_baseline_replication": f"each N=5, 6 W4 re-derivation agrees with its published E0B cell on {['/'.join(p) for p in REPLICATION_CHANNELS]} within max({REPLICATION_ABS}, {REPLICATION_REL} x |published|). Rare-mass channels qualified by GT-F35 are excluded by declaration",
            "Z5_numerical_acceptance": "per cell: stationary resolved (residual <= 1e-12; two starts within 1e-10 L1; iteration cap not reached), symmetry <= 1e-10, autocorrelation cap not reached, kernel sample check, no zero-mass reachable state, per-entry long-double residual, referee agreement (tolerances below). A tally, not a prediction: a failed cell is reported as unresolved or numerically qualified, never as a scientific counterexample, and never re-run with weaker tolerances",
            "Z6_hub_frame_reversible_controls": f"NULL and CLOSEW cells: hub-frame pattern asymmetry and hub-frame net current <= {FRAME_REVERSIBLE_TOLERANCE}",
            "separation_note": "Z1-Z6 are identities, rule properties and numerical acceptance. None predicts the sign or size of any margin, flux, handover index or strength response",
        },
        "deliberate_omissions": {
            "free_n7": "FREE N=7 (option D) is not authorised in GT-P004; preserved as a separate future decision",
            "spectrum": "the generator spectrum is unavailable at every N in this round: gtobs never forms the dense generator (GT-P003). Reported as unavailable, not zero; published N<=6 spectra are not compared",
            "recurrent_class_list": "reducible classes are not decomposed beyond [size] (gtobs)",
            "grade_or_alphabet_sweeps": "no further grades, alphabets, interpolations or sizes",
            "pcomp": "PCOMP (E0B rules-vs-ratio control) is not part of option B",
        },
        "estimands": "the declared channels and every gtobs channel of each cell, the comparisons C1-C8, and the controls Z1-Z6",
        "experiment_id": EXPERIMENT_ID,
        "families": {
            family: {
                "components": [{"K": gte0a.COMPONENT_K[k], "grade": g, "kind": k, "template_example": gte0a.component_expressions(k, 5, g)[0]} for k, g in FAMILIES[family][grade_of(family)]],
                "gradient": gte0a.is_gradient(family, FAMILIES),
                "grade": grade_of(family),
            }
            for family in FAMILY_ORDER
        },
        "history": False,
        "initial_conditions": "as E0: the HELD start state gt0.start_state(n, 'HELD'), the source triangle {0,1,2} present and no other relation; source slots are present and cannot dissolve; the reachable class from that start is analysed",
        "items": cells,
        "meta_constraints": False,
        "method": {"name": "Open-Thetical Research", "path": "research-methods/open-thetical-research.md", "version": "1.0"},
        "mode": "B",
        "new_primitives": False,
        "numerical_policy": {
            "stationary": f"gtobs.stationary: lazy power iteration by gathers from the uniform law until L1 change < {gtobs.STATIONARY_TOLERANCE} and per-entry relative change < {gtobs.STATIONARY_RELATIVE_TOLERANCE}; second run from the point mass on the start must agree within {gtobs.CROSS_CHECK_TOLERANCE} L1; residual <= {gtobs.STATIONARY_RESIDUAL_TOLERANCE}; cap {gtobs.STATIONARY_CAP} iterations; no dense solve, no clipping of positive mass",
            "third_start": f"a third run from the point mass on the reachable state with the most relations; law L1 <= {REFEREE_L1}, per-entry relative <= {REFEREE_MAX_RELATIVE}, headline channels within {REFEREE_CHANNEL_ABS}",
            "gth_referee": f"where the class has at most {gtobs.DENSE_LIMIT} states (N=5, 6): the Grassmann-Taksar-Heyman dense solve (subtraction-free) with the same tolerances",
            "long_double_residual": f"per-entry relative residual |(pi P)_i - pi_i| / pi_i in numpy longdouble <= {RESIDUAL_MAX_RELATIVE}; zero-mass reachable states must be 0 (guards against the GT-F35 clipping)",
            "kernel_sample_check": f"the family's rule strings and scaffold, parsed by the laboratory DSL and evaluated with exact Fraction factors on {KERNEL_SAMPLE} seeded states plus the start and the fullest state (seed sha256('round-e1:kernel:<item_id>')[:16]); gtkernel weights within relative {KERNEL_RELATIVE_TOLERANCE}, identical zero pattern, correct targets. W3/W16 are float in gtkernel and exact in the DSL, so the comparison is by tolerance",
            "autocorrelation": f"gtobs lazy Poisson series to relative term {gtobs.POISSON_RELATIVE_TOLERANCE}, cap {gtobs.POISSON_CAP}",
            "symmetry": f"class tables over the HELD symmetry group (S3 on the source x S(N-3) on the probes); max orbit disagreement <= {gte0a.SYMMETRY_TOLERANCE}",
            "rare_conditionals": f"any conditional channel whose conditioning mass is < {RARE_MASS_FLOOR} is flagged rare and not interpreted; < {LOW_MASS_FLOOR} is flagged low. Values are kept, never clipped",
            "threads": "children run with single-threaded BLAS/OpenMP; results reproducible to about 1e-15, not bitwise",
        },
        "observables": {
            "gtobs": f"every channel of rs_constraint_lab.gtobs.analyse ({gtobs.OBSERVABLES_VERSION}): occupancy, held observables in both clocks (attachment, a/k profile, distance distribution, radial drift, escape and capture), shell activity in both clocks, reversibility (flux, entropy production, square affinities), projected currents, class-free and hub-frame event order, class tables, Gibbs projection, autocorrelation times, e1 additions (standardised margin, detached-probe counts, hub structure, engaged witness census, hub persistence)",
            "round": "handover index: the four steps of the E0 handover cycle (FPFA, FADP, DPDA, DAFP), forward minus reverse probability, adjacent and disjoint, and the count of forward-oriented adjacent steps",
            "trajectories": f"illustrative only, {gte0a.TRAJECTORIES_PER_CELL} x {gte0a.EVENTS_PER_TRAJECTORY} events per cell, seeds sha256('round-e1:<item_id>:<k>')[:16]; no table statistic uses them",
        },
        "ontology": ONTOLOGY,
        "open_questions_without_prediction": [
            "GT-Q07: at N=7, is CSPH's attachment margin above or below the size-specific null, in each clock and each form, and does it coexist with irreversible flux?",
            "Does the handover keep the E0 orientation at N=7 in every non-gradient family, reverse, or vanish?",
            "Does the equal-ratio occupancy gap keep growing at N=7, and under strengthening?",
            "How does shell structure (shells 1-4, activity in both clocks) change at N=7?",
            "How much does the engaged witness load grow from N=6 to N=7, per component, and where does it sit against the W3/W16 bracket?",
            "Does the W3/W16 bracket reproduce the published N=5 -> N=6 step (calibration), especially for PATHF and PATHH?",
            "Is any N=6 -> N=7 change in the direction of strengthening at N=6, opposite to it, or outside its range?",
            "Do hub structure and the hub-frame arrow change with N beyond the changing null hub rates?",
            "Anything not anticipated above.",
        ],
        "parameter_fit": False,
        "pre_freeze_exposure": {
            "published_n_le_6": "all E0A and E0B tables (N=5, 6, W4) were read in full; the 16 baseline items re-derive published cells and are not new observations",
            "gt_p003_reproduction": "all 84 published E0 cells were recomputed by gtobs in GT-P003 (validation log); this includes every N=5, 6 W4 baseline of this round",
            "post_hoc_channels": "engaged witness census, margin decomposition (raw, standardised, jump/continuous) and hub structure on published N=5, 6 cells (reports/e1-engaged-witness-n5-n6.json, reports/e1-margin-decomposition-n5-n6.json); GT-F34 is post hoc",
            "theorem_fixed": "NULL baselines at N=5, 6, 7 (uniform law) and the scale census (reports/e1-scale-census.json)",
            "n7_fixtures": "three N=7 cost fixtures were run in GT-P003: HELD NULL (identity; this round's N=7 NULL cell is therefore exposed), HELD CLOSE strong_favour (not a round cell), FREE NULL (not a round cell). The GT-P003 design draft listed FREE CLOSE as exposed; it was never run",
            "n7_kernel_build": "the HELD N=7 PATHF weak_suppress chain was built for timing in the E1 kernel step (4dacd11); no stationary law or observable was computed",
            "bracket_kernel_builds": "tests/test_gtobs.py builds HELD N=5 W3 and W16 kernels of CSPH, PATHF and CLOSEW and compares weights and targets with build_kernel; no stationary law or observable was computed. No other W3/W16 cell of these families was computed",
            "engineering_after_gt_p003": "before freezing, gte1 was exercised only on synthetic N=4 cells (W4, W3, W16), on published N=5 and N=6 W4 cells (baseline items: CSPH, PATHH, NULL, CLOSEW at N=5; CSPH at N=6, for timing), and on the theorem-fixed HELD N=7 CLOSE strong_favour fixture (not a round cell; costs and solver checks only). The HELD N=5 W16 PATHF kernel was rebuilt by a test (weights only). No N=7 round cell and no W3/W16 stationary law at N=5 or 6 was computed",
            "reference_hashes": {rel: sha256_file(repo / rel) for rel in REFERENCE_FILES},
        },
        "programme": "GT",
        "prompt_id": PROMPT_ID,
        "question": "How do occupancy, kinetics, stationary circulation (the handover) and source-relative attachment reorganise from N=5, 6 to N=7 at fixed grades, and how much of that change resembles what uniform strengthening of the same rules does at fixed N?",
        "round_id": ROUND_ID,
        "sampling": f"exact census of {len(authorised_cells())} authorised cells (tranche I: 8; tranche II: 24) plus {len(cells) - len(authorised_cells())} baseline re-derivations",
        "schema": "rs-gt.e1-plan/v1",
        "software": {"analysis_module": "rs_constraint_lab.gte1", "kernel": gtkernel.KERNEL_VERSION, "numpy": np.__version__, "observables": gtobs.OBSERVABLES_VERSION, "python": __import__("platform").python_version()},
        "stochastic_trajectories": "illustrative_only",
        "stop_conditions": {
            "item": f"each cell runs in its own process; past its watchdog ({WATCHDOG_SECONDS} seconds by N) it is killed and recorded unresolved_watchdog, or complete_checks_interrupted if its main result was already written; the round continues",
            "round": f"all items have final records, or the {ROUND_WALL_CAP_SECONDS}-second wall cap from the first launch: running cells are recorded interrupted_wall_cap, unstarted cells not_started_wall_cap, and the round stops",
            "unresolved": "an unresolved stationary law is recorded without stationary observables; no post-freeze retuning of tolerances, grades, alphabets, cells or channels",
            "amendment": "a solver-only correction after freeze keeps this plan, is documented with its effect and validated independently, and marks affected results; any change to cells or estimands stops the round for explicit amendment",
            "stop_rule_reading": "per GT-P004 section 5 (matching the GT-P003 roadmap proposal): a margin crossing below null is an observation for that family, N, clock and definition; it does not by itself establish a finite-size effect, amplification or a failure of the ontology; grades are not retuned",
        },
        "tolerances": {"comparable_ratio": list(COMPARABLE_RATIO), "frame_reversible": FRAME_REVERSIBLE_TOLERANCE, "identity": IDENTITY_TOLERANCE, "kernel_relative": KERNEL_RELATIVE_TOLERANCE, "low_mass_floor": LOW_MASS_FLOOR, "negligible_change": NEGLIGIBLE_CHANGE, "non_reversible_floor": NON_REVERSIBLE_FLOOR, "proxy_share": PROXY_SHARE, "rare_mass_floor": RARE_MASS_FLOOR, "referee_channel_abs": REFEREE_CHANNEL_ABS, "referee_l1": REFEREE_L1, "referee_max_relative": REFEREE_MAX_RELATIVE, "replication_abs": REPLICATION_ABS, "replication_rel": REPLICATION_REL, "residual_max_relative": RESIDUAL_MAX_RELATIVE, "reversible_flux": REVERSIBLE_FLUX_TOLERANCE, "symmetry": gte0a.SYMMETRY_TOLERANCE},
        "work_count": {
            "authorised_cells": len(authorised_cells()),
            "baseline_items": len(cells) - len(authorised_cells()),
            "disk_budget_bytes": 300_000_000,
            "estimate_note": "measured on this host before freezing (16 cores, about 8 GB available): the full gte1 cell pipeline on the theorem-fixed HELD N=7 CLOSE strong_favour fixture took 156 s (main 126 s, checks 31 s) at 590 MB peak; on the published HELD N=6 W4 CSPH baseline 43 s (GTH referee 42 s) at 300 MB; N=5 under 1 s. Scientific N=7 cells are extrapolated at 3-6 min (stationary iterations 300-1,100 against the fixture's 537). Round: about 40-65 cell-minutes, 15-30 min wall with 4 workers. Estimates, not guarantees",
            "items": len(cells),
            "largest_state_space": 262144,
            "memory_budget_bytes_per_worker": 1_500_000_000,
            "round_wall_cap_seconds": ROUND_WALL_CAP_SECONDS,
            "wall_time_estimate_seconds": 1800,
            "watchdog_seconds": {str(k): v for k, v in WATCHDOG_SECONDS.items()},
            "workers": WORKERS,
        },
    }
    document["plan_hash"] = plan_hash(document)
    return document


def require_execution(repo: Path, commit: str | None, *, require_remote: bool = True) -> dict:
    from rs_constraint_lab.explore08 import FrozenPlanError, remote_contains, require_frozen_plan

    plan = require_frozen_plan(repo, commit, PLAN_RELPATH, disk_path=repo / PLAN_RELPATH)
    if require_remote and not remote_contains(repo, commit or ""):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    if plan.get("items") != items() or plan.get("history") is not False or plan.get("new_primitives") is not False or plan.get("ontology") != ONTOLOGY:
        raise FrozenPlanError("execution refused: E1 plan contract drifted")
    families = {f: [[k, g] for k, g in FAMILIES[f][grade_of(f)]] for f in FAMILY_ORDER}
    if {f: [[c["kind"], c["grade"]] for c in v["components"]] for f, v in plan["families"].items()} != families:
        raise FrozenPlanError("execution refused: E1 family components drifted")
    return plan


# --- execution --------------------------------------------------------------------------------


def _item_path(root: Path, item: dict, suffix: str = "") -> Path:
    return root / "items" / f"{item['item_id']}{suffix}.json"


def execute_item(root: Path, item: dict) -> dict:
    """Child-process body: analyse one cell, write the main result, then the checked result."""
    from rs_constraint_lab.durable import atomic_write_json

    started = time.perf_counter()

    def persist(result, trajectories, status):
        payload = {"item": item, "item_id": item["item_id"], "peak_rss_mb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, "result": result, "status": status, "wall_seconds": time.perf_counter() - started}
        return payload

    def on_main(result, trajectories):
        atomic_write_json(_item_path(root, item, ".partial"), persist(result, trajectories, "complete_checks_interrupted"))
        if trajectories is not None:
            atomic_write_json(root / "trajectories" / f"{item['item_id']}.json", trajectories)

    result, trajectories = analyse_item(item, on_main=on_main)
    payload = persist(result, trajectories, "complete")
    atomic_write_json(_item_path(root, item), payload)
    partial = _item_path(root, item, ".partial")
    if partial.exists():
        partial.unlink()
    return payload


def _final(root: Path, item: dict) -> dict | None:
    from rs_constraint_lab.durable import read_json

    path = _item_path(root, item)
    if path.is_file():
        payload = read_json(path)
        if payload.get("item_id") == item["item_id"] and payload.get("status") in FINAL_STATUSES:
            return payload
    return None


def run(root: Path, plan: dict, *, workers: int = WORKERS, python: str = sys.executable, wall_cap: float = ROUND_WALL_CAP_SECONDS, watchdogs: dict | None = None, poll: float = 1.0, module: str = "rs_constraint_lab.gte1") -> list[dict]:
    """Resumable runner: one process per cell, at most ``workers`` at once, watchdog per cell, round wall cap."""
    from rs_constraint_lab.durable import atomic_write_json, read_json

    watchdogs = watchdogs or WATCHDOG_SECONDS
    (root / "items").mkdir(parents=True, exist_ok=True)
    (root / "logs").mkdir(parents=True, exist_ok=True)
    meta_path = root / "round.json"
    meta = read_json(meta_path) if meta_path.is_file() else {"plan_hash": plan["plan_hash"], "round_started_unix": time.time()}
    if meta.get("plan_hash") != plan["plan_hash"]:
        raise RuntimeError("generated round directory belongs to a different plan")
    atomic_write_json(meta_path, meta)
    plan_file = root / "plan.json"
    atomic_write_json(plan_file, plan)
    pending = [it for it in plan["items"] if _final(root, it) is None]
    running: dict[int, tuple[dict, float, object]] = {}
    env = {**os.environ, **CHILD_THREAD_ENV}

    def record(item, status, extra):
        partial = _item_path(root, item, ".partial")
        if partial.is_file() and status in ("unresolved_watchdog", "interrupted_wall_cap", "failed"):
            payload = read_json(partial)
            payload["status"] = "complete_checks_interrupted"
            payload["interruption"] = {"cause": status, **extra}
            partial.unlink()
        else:
            payload = {"item": item, "item_id": item["item_id"], "status": status, **extra}
        atomic_write_json(_item_path(root, item), payload)
        finished.add(item["item_id"])

    finished = {it["item_id"] for it in plan["items"] if it not in pending}

    def status_file():
        atomic_write_json(root / "status.json", {"completed_items": len(finished), "item_count": len(plan["items"]), "running": sorted(it["item_id"] for it, _, _ in running.values()), "updated_unix": time.time(), "elapsed_seconds": time.time() - meta["round_started_unix"]})

    procs: dict[int, subprocess.Popen] = {}

    def reap(pid: int, flags: int):
        """os.wait4 that keeps the Popen object consistent and tolerates a child reaped elsewhere."""
        try:
            waited, code, usage = os.wait4(pid, flags)
        except ChildProcessError:
            rc = procs[pid].poll()
            rc = 1 if rc is None else rc
            return pid, (rc & 0xFF) << 8 if rc >= 0 else -rc, None
        if waited:
            procs[pid].returncode = os.waitstatus_to_exitcode(code)
        return waited, code, usage

    def rss(usage) -> float | None:
        return usage.ru_maxrss / 1024 if usage is not None else None

    capped = False
    while pending or running:
        elapsed = time.time() - meta["round_started_unix"]
        if elapsed > wall_cap and not capped:
            capped = True
            for pid, (item, t0, log) in list(running.items()):
                os.kill(pid, signal.SIGKILL)
                reap(pid, 0)
                log.close()
                record(item, "interrupted_wall_cap", {"wall_seconds": time.time() - t0})
                running.pop(pid)
                procs.pop(pid)
            for item in pending:
                record(item, "not_started_wall_cap", {})
            pending = []
            break
        while pending and len(running) < workers:
            item = pending.pop(0)
            log = open(root / "logs" / f"{item['item_id']}.log", "w")
            proc = subprocess.Popen([python, "-m", module, "item", "--root", str(root), "--item-id", item["item_id"]], stdout=log, stderr=subprocess.STDOUT, env=env)
            running[proc.pid] = (item, time.time(), log)
            procs[proc.pid] = proc
        status_file()
        time.sleep(poll)
        for pid, (item, t0, log) in list(running.items()):
            waited, code, usage = reap(pid, os.WNOHANG)
            age = time.time() - t0
            if waited == 0:
                if age > watchdogs.get(item["n"], max(watchdogs.values())):
                    os.kill(pid, signal.SIGKILL)
                    _, code, usage = reap(pid, 0)
                    log.close()
                    record(item, "unresolved_watchdog", {"peak_rss_mb": rss(usage), "wall_seconds": age, "watchdog_seconds": watchdogs.get(item["n"], max(watchdogs.values()))})
                    running.pop(pid)
                    procs.pop(pid)
                continue
            log.close()
            running.pop(pid)
            procs.pop(pid)
            final = _final(root, item)
            if final is None or os.waitstatus_to_exitcode(code) != 0:
                tail = (root / "logs" / f"{item['item_id']}.log").read_text()[-2000:]
                record(item, "failed", {"exit_code": os.waitstatus_to_exitcode(code), "log_tail": tail, "peak_rss_mb": rss(usage), "wall_seconds": age})
            else:
                final["peak_rss_mb_parent_view"] = rss(usage)
                atomic_write_json(_item_path(root, item), final)
                finished.add(item["item_id"])
    status_file()
    return [_final(root, it) or {"item_id": it["item_id"], "status": "missing"} for it in plan["items"]]


def publish(root: Path, plan: dict, out: Path, *, frozen_plan_commit: str, e0b_tables: Path) -> str:
    from rs_constraint_lab.durable import atomic_write_json, canonical_json, read_json, sha256_bytes

    records = {it["item_id"]: (_final(root, it) or {"item_id": it["item_id"], "status": "missing"}) for it in plan["items"]}
    results = {}
    for key, rec in records.items():
        if "result" in rec:
            r = dict(rec["result"])
            r["item_id"] = key
            results[key] = r
    published = read_json(e0b_tables)["results"]
    assembled = assemble(results, published)
    item_records = {
        key: {
            "numerical_problems": check_problems(results[key]) if key in results else None,
            "peak_rss_mb": rec.get("peak_rss_mb_parent_view", rec.get("peak_rss_mb")),
            "role": next(it["role"] for it in plan["items"] if it["item_id"] == key),
            "status": rec["status"],
            "tranche": next(it["tranche"] for it in plan["items"] if it["item_id"] == key),
            "wall_seconds": rec.get("wall_seconds"),
            **({"interruption": rec["interruption"]} if "interruption" in rec else {}),
            **({"exit_code": rec["exit_code"], "log_tail": rec["log_tail"]} if rec["status"] == "failed" else {}),
        }
        for key, rec in records.items()
    }
    walls = [r["wall_seconds"] for r in item_records.values() if r["wall_seconds"] is not None]
    payload = {
        "analysis_version": ANALYSIS_VERSION,
        "experiment_id": EXPERIMENT_ID,
        "frozen_analysis_plan_commit": frozen_plan_commit,
        "item_records": item_records,
        "plan_hash": plan["plan_hash"],
        "results": results,
        "round_id": ROUND_ID,
        "schema": "rs-gt.e1-tables/v1",
        "status_counts": {s: sum(r["status"] == s for r in item_records.values()) for s in sorted({r["status"] for r in item_records.values()})},
        "wall_seconds_max": max(walls) if walls else None,
        "wall_seconds_total_cpu_cells": sum(walls),
        **assembled,
    }
    body = dict(payload)
    body["payload_sha256"] = sha256_bytes(canonical_json(payload).encode("utf-8"))
    atomic_write_json(out, body)
    return body["payload_sha256"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m rs_constraint_lab.gte1")
    sub = parser.add_subparsers(dest="command", required=True)
    one = sub.add_parser("item", help="internal: run one cell of the frozen plan copied into --root")
    one.add_argument("--root", required=True)
    one.add_argument("--item-id", required=True)
    args = parser.parse_args(argv)
    from rs_constraint_lab.durable import read_json

    root = Path(args.root)
    plan = read_json(root / "plan.json")
    (item,) = [it for it in plan["items"] if it["item_id"] == args.item_id]
    if item not in items() and not plan.get("synthetic_fixture"):
        raise SystemExit("item is not in the E1 manifest")
    execute_item(root, item)
    return 0


if __name__ == "__main__":
    sys.exit(main())
