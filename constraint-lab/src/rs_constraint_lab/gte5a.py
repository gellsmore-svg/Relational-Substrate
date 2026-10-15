"""GT round E5A: FREE relational persistence, turnover and a lagged hub (GT-P009).

Twelve FREE kernels (NULL, PATHF weak_suppress, PATHH weak_favour, CSPH,
CLOSEW, PCOMP at N = 5, 6; all published in E0B). Each item recomputes the
kernel and its stationary law (a labelled replication of E0B), then computes
on the target law and on its density-matched comparator ND:

* six predicates (three intact, three flexible) on a primary instance and on
  its relabelled image, by stationary boundary flux (``gtpersist``);
* the edge present-episode lifetime of slot (0, 1) and its relabelled image;
* the lagged hub at lags (0, 1, 2, 4, 8, 16) in both clocks;
* after the main result is saved: residual (occupation-sampled) lifetimes and
  the entrance first-passage check (secondary).

N0 is the NULL item of the same size. Definitions:
``gravity-time/docs/e5-definitions-and-null-construction.md``.
"""

from __future__ import annotations

import argparse
import math
import sys
import time
from pathlib import Path

import numpy as np

from rs_constraint_lab import gte0b, gte1, gtkernel, gtobs
from rs_constraint_lab import gtpersist as P
from rs_constraint_lab.state import edges

ROUND_ID = "round-e5a"
EXPERIMENT_ID = "gt-round-e5a-free-persistence"
ANALYSIS_VERSION = "gt-e5a/v1"
PROMPT_ID = "GT-P009"
MODE = "FREE"
FAMILY_GRADES = (("NULL", "none"), ("PATHF", "weak_suppress"), ("PATHH", "weak_favour"), ("CSPH", "strong_favour+weak_favour"), ("CLOSEW", "weak_favour"), ("PCOMP", "weak_favour+weak_favour"))
SIZES = (5, 6)
LAGS = (0, 1, 2, 4, 8, 16)
IDENTITY = 1e-9
REPLICATION_ABS = 1e-10
REPLICATION_REL = 1e-8
LAG_TOLERANCE = 1e-9
ND_CROSS_CHECK_CAP = 20_000
ROLE = {"NULL": "null_control_N0", "PCOMP": "control_equal_ratio", "CLOSEW": "control_reversible_closure"}


def components(family: str, grade: str) -> list[tuple[str, str]]:
    return [] if family == "NULL" else gte0b.FAMILIES[family][grade]


def item_id(n: int, family: str, grade: str) -> str:
    return f"FREE-N{n}-{family}-{grade}"


def items() -> list[dict]:
    out = []
    for n in SIZES:
        for f, g in FAMILY_GRADES:
            out.append({"components": [list(c) for c in components(f, g)], "family": f, "grade": g, "item_id": item_id(n, f, g), "n": n, "prior_cell": f"round-e0b {item_id(n, f, g)}", "role": ROLE.get(f, "open_scientific")})
    return out


def predicate_ids() -> list[str]:
    return [f"{it['item_id']}:{p}" for it in items() for p in P.PREDICATES]


# --- analysis ----------------------------------------------------------------


def analyse_law(chain, ct: np.ndarray, n: int, *, lumped=None) -> dict:
    """Every primary channel of one law (target or ND)."""
    out = {"predicates": {}, "relabelled": {}}
    for p in P.PREDICATES:
        out["predicates"][p] = P.analyse_predicate(chain, ct, n, p, P.primary_instance(p))
        out["relabelled"][p] = P.analyse_predicate(chain, ct, n, p, P.relabelled_instance(p, n))
    out["edge"] = P.edge_episode(chain, ct, n, 0, 1)
    out["edge_relabelled"] = P.edge_episode(chain, ct, n, n - 2, n - 1)
    out["density_ct"] = [float(v) for v in P.density_profile(chain.states, ct, len(edges(n)))]
    out["density_jump"] = [float(v) for v in P.jump_density(chain, ct, n)]
    out["mean_rate_ct"] = float(ct @ chain.rates)
    out["lagged_hub"] = P.lagged_hub(chain, ct, n, LAGS, lumped=lumped)
    return out


def covariance_gap(block: dict) -> float:
    worst = 0.0
    for p in P.PREDICATES:
        a, b = block["predicates"][p], block["relabelled"][p]
        for key in ("prevalence_ct", "prevalence_jump", "lifetime_ct", "lifetime_jump", "omega", "entries_per_unit_time"):
            if a.get(key) is None and b.get(key) is None:
                continue
            worst = max(worst, abs(a[key] - b[key]) / max(abs(a[key]), 1e-300))
    e, f = block["edge"], block["edge_relabelled"]
    worst = max(worst, abs(e["lifetime_ct"] - f["lifetime_ct"]) / e["lifetime_ct"])
    return worst


def law_checks(block: dict) -> dict:
    flux = max([block["predicates"][p]["flux_balance_relative"] for p in P.PREDICATES] + [block["edge"]["flux_balance_relative"]])
    jl = max(block["predicates"][p].get("jump_length_identity_gap", 0.0) for p in P.PREDICATES)
    intact_internal = max(block["predicates"][p]["required_edge_internal_flux"] for p in P.INTACT)
    intact_omega = max(block["predicates"][p]["omega"] for p in P.INTACT)
    lag = block["lagged_hub"]["checks"]
    degs = [row["comparison_degree"] for row in block["lagged_hub"]["continuous"].values()]
    jdegs = [row["comparison_degree"] for row in block["lagged_hub"]["jump"].values()]
    return {
        "classifications": sorted({block["predicates"][p]["classification"] for p in P.PREDICATES}),
        "comparison_degree_ptp_ct": float(np.ptp(degs)),
        "comparison_degree_ptp_jump": float(np.ptp(jdegs)),
        "covariance_max_relative": covariance_gap(block),
        "flux_balance_max_relative": flux,
        "intact_omega_max": intact_omega,
        "intact_required_internal_flux_max": intact_internal,
        "jump_length_identity_max": jl,
        "lag": lag,
    }


def analyse_item(item: dict, *, on_main=None, secondary: bool = True) -> dict:
    n = item["n"]
    m = len(edges(n))
    comps = [tuple(c) for c in item["components"]]
    timings: dict[str, float] = {}
    t0 = time.perf_counter()
    chain, build = gtkernel.reachable_chain(n, MODE, comps)
    timings["build"] = time.perf_counter() - t0
    result: dict = {"analysis_version": ANALYSIS_VERSION, "item_id": item["item_id"], "kernel_version": gtkernel.KERNEL_VERSION, "persist_version": P.PERSIST_VERSION}
    result["ergodicity"] = {"all_rates_positive": bool((chain.W > 0).all()), "reachable_states": int(len(chain.states)), "full_space": bool(len(chain.states) == 1 << m)}
    t0 = time.perf_counter()
    stat = gtobs.stationary(chain, 0)
    timings["stationary"] = time.perf_counter() - t0
    result["stationary"] = {k: v for k, v in stat.items() if k not in ("ct", "jump")}
    if not stat["resolved"]:
        result["status_note"] = "target stationary law unresolved"
        return result
    ct, jump = stat["ct"], stat["jump"]
    t0 = time.perf_counter()
    arrays = gtobs.structure_arrays(chain, n)
    table, symmetry = gtobs.class_table(chain, ct, jump, n, MODE, arrays)
    result["class_table"] = table
    result["symmetry_max_abs_difference"] = symmetry
    timings["class_table"] = time.perf_counter() - t0
    lumped = P.lump_index(chain.states, n)
    t0 = time.perf_counter()
    result["target"] = analyse_law(chain, ct, n, lumped=lumped)
    result["target_checks"] = law_checks(result["target"])
    timings["target"] = time.perf_counter() - t0
    # ND comparator
    t0 = time.perf_counter()
    p = P.density_profile(chain.states, ct, m)
    rates = P.nd_rates(p)
    if not rates["resolved"]:
        result["nd_construction"] = {"resolved": False, "reason": rates["reason"], "zero_bins": rates["zero_bins"]}
    else:
        nd, pi_nd, info = P.nd_chain(n, p, float(ct @ chain.rates))
        cross = gtkernel.stationary_sparse(nd, cap=ND_CROSS_CHECK_CAP)
        info["iterative_cross_check"] = {"resolved": bool(cross["resolved"]), "iterations": cross["iterations"], "residual": cross["residual"], "l1_vs_analytic": float(np.abs(cross["ct"] - pi_nd).sum()) if cross["resolved"] else None}
        info["resolved"] = True
        result["nd_construction"] = info
        result["nd"] = analyse_law(nd, pi_nd, n, lumped=lumped)
        result["nd_checks"] = law_checks(result["nd"])
        result["jump_density_l1_target_vs_nd"] = float(np.abs(np.array(result["nd"]["density_jump"]) - np.array(result["target"]["density_jump"])).sum())
    timings["nd"] = time.perf_counter() - t0
    result["timings"] = timings
    if on_main is not None:
        on_main(result)
    if secondary:
        t0 = time.perf_counter()
        sec = {"target": {}}
        for p_name in P.PREDICATES:
            A = P.predicate_mask(chain.states, n, p_name, P.primary_instance(p_name))
            sec["target"][p_name] = P.residual_lifetimes(chain, ct, A)
        if "nd" in result:
            sec["nd"] = {}
            for p_name in P.PREDICATES:
                A = P.predicate_mask(nd.states, n, p_name, P.primary_instance(p_name))
                sec["nd"][p_name] = P.residual_lifetimes(nd, pi_nd, A)
        result["secondary_residual_life"] = sec
        timings["secondary"] = time.perf_counter() - t0
    return result


def lag_problems(lag: dict) -> list[str]:
    out = []
    if lag["lumpability_defect_relative"] > 1e-12:
        out.append("lumpability defect")
    if lag["row_sum_max_error"] > LAG_TOLERANCE or lag["min_entry"] < -1e-12:
        out.append("propagator not stochastic")
    if lag["stationarity_l1"] > LAG_TOLERANCE:
        out.append("propagator not stationary")
    if lag["semigroup_max"] > LAG_TOLERANCE:
        out.append("semigroup check")
    if lag["lumped_vs_full_jump_max"] > 1e-10:
        out.append("lumped and full jump chains disagree")
    if lag["pair_permutation_covariance_max"] > 1e-10:
        out.append("pair permutation covariance")
    if lag.get("uniformisation_vs_expm_max") is not None and lag["uniformisation_vs_expm_max"] > LAG_TOLERANCE:
        out.append("uniformisation cross-check")
    return out


def law_problems(c: dict, label: str) -> list[str]:
    out = []
    if c["flux_balance_max_relative"] > IDENTITY:
        out.append(f"{label}: entry/exit flux imbalance")
    if c["jump_length_identity_max"] > IDENTITY:
        out.append(f"{label}: jump length identity")
    if c["covariance_max_relative"] > IDENTITY:
        out.append(f"{label}: relabelled instance disagrees")
    if c["intact_required_internal_flux_max"] != 0.0 or c["intact_omega_max"] != 0.0:
        out.append(f"{label}: intact motif with required-edge turnover")
    if c["classifications"] != ["ergodic_episodes"]:
        out.append(f"{label}: classification {c['classifications']}")
    if max(c["comparison_degree_ptp_ct"], c["comparison_degree_ptp_jump"]) > LAG_TOLERANCE:
        out.append(f"{label}: comparison degree not stationary")
    out += [f"{label}: {p}" for p in lag_problems(c["lag"])]
    return out


def check_problems(r: dict) -> list[str]:
    out = []
    e = r.get("ergodicity", {})
    if not (e.get("all_rates_positive") and e.get("full_space")):
        out.append("not the positive-rate full FREE space")
    s = r.get("stationary", {})
    if not s.get("resolved"):
        out.append("stationary unresolved")
        return out
    if r.get("symmetry_max_abs_difference", 1.0) > 1e-10:
        out.append("law not symmetric")
    out += law_problems(r["target_checks"], "target")
    nc = r.get("nd_construction", {})
    if not nc.get("resolved"):
        out.append("ND unresolved")
    else:
        if nc["detailed_balance_max_relative"] > 1e-12 or nc["global_balance_relative"] > 1e-10:
            out.append("ND balance")
        if nc["density_l1_vs_target"] > 1e-10 or nc["mean_rate_relative_gap"] > 1e-10:
            out.append("ND calibration")
        out += law_problems(r["nd_checks"], "nd")
    return out


# --- assembly ------------------------------------------------------------------


def _sign(a: float | None, b: float | None, larger: str, smaller: str) -> str:
    if a is None or b is None:
        return "undefined"
    if abs(a - b) <= P.TIE_RELATIVE * max(abs(a), abs(b)):
        return "tie"
    return larger if a > b else smaller


def predicate_row(tgt: dict, n0: dict, nd: dict | None, p: str) -> dict:
    def view(block):
        if block is None:
            return None
        r, e = block["predicates"][p], block["edge"]
        return {
            "edge_lifetime_ct": e["lifetime_ct"],
            "edge_lifetime_jump": e["lifetime_jump"],
            "eligible_share": r.get("eligible_share_of_internal_events"),
            "entries_per_event": r.get("entries_per_event"),
            "entries_per_unit_time": r.get("entries_per_unit_time"),
            "exit_share_anchor": r.get("exit_share_anchor"),
            "internal_events_per_episode": r.get("internal_events_per_episode"),
            "lifetime_ct": r.get("lifetime_ct"),
            "lifetime_jump": r.get("lifetime_jump"),
            "off_lifetime_ct": r.get("off_lifetime_ct"),
            "off_lifetime_jump": r.get("off_lifetime_jump"),
            "omega": r.get("omega"),
            "prevalence_ct": r["prevalence_ct"],
            "prevalence_jump": r["prevalence_jump"],
            "rho_ct": r["lifetime_ct"] / e["lifetime_ct"] if r.get("lifetime_ct") else None,
            "rho_jump": r["lifetime_jump"] / e["lifetime_jump"] if r.get("lifetime_jump") else None,
        }

    row = {"target": view(tgt), "N0": view(n0), "ND": view(nd)}
    t = row["target"]
    for name in ("N0", "ND"):
        c = row[name]
        if c is None:
            row[f"vs_{name}"] = None
            continue
        row[f"vs_{name}"] = {
            "lifetime_ratio_ct": t["lifetime_ct"] / c["lifetime_ct"],
            "lifetime_ratio_jump": t["lifetime_jump"] / c["lifetime_jump"],
            "rho_ratio_ct": t["rho_ct"] / c["rho_ct"],
            "rho_ratio_jump": t["rho_jump"] / c["rho_jump"],
            "omega_difference": t["omega"] - c["omega"],
            "prevalence_ratio_ct": t["prevalence_ct"] / c["prevalence_ct"],
            "prevalence_ratio_jump": t["prevalence_jump"] / c["prevalence_jump"],
            "signs": {
                "lifetime_ct": _sign(t["lifetime_ct"], c["lifetime_ct"], "longer", "shorter"),
                "lifetime_jump": _sign(t["lifetime_jump"], c["lifetime_jump"], "longer", "shorter"),
                "rho_ct": _sign(t["rho_ct"], c["rho_ct"], "higher", "lower"),
                "rho_jump": _sign(t["rho_jump"], c["rho_jump"], "higher", "lower"),
                "omega": _sign(t["omega"], c["omega"], "more", "fewer") if p in P.FLEXIBLE else "zero_by_theorem",
                "prevalence_ct": _sign(t["prevalence_ct"], c["prevalence_ct"], "higher", "lower"),
            },
        }
        row[f"vs_{name}"]["pattern"] = discovery_pattern(row[f"vs_{name}"]["signs"], p)
    return row


def discovery_pattern(signs: dict, predicate: str) -> str:
    """Predeclared discovery-matrix cell from signs only (no magnitude threshold)."""
    ct, jt = signs["lifetime_ct"], signs["lifetime_jump"]
    if ct == "longer" and jt == "longer":
        life = "longer_both_clocks"
    elif ct == "longer":
        life = "longer_ct_only"
    elif jt == "longer":
        life = "longer_jump_only"
    elif ct == "tie" and jt == "tie":
        life = "tie_both_clocks"
    else:
        life = "not_longer"
    if predicate in P.INTACT:
        return f"{life}|intact_no_turnover"
    return f"{life}|turnover_{signs['omega']}"


def lag_row(tgt: dict, n0: dict, nd: dict | None) -> dict:
    out = {}
    for clock in ("continuous", "jump"):
        rows = {}
        for d in LAGS:
            k = str(d)
            t, z = tgt["lagged_hub"][clock][k], n0["lagged_hub"][clock][k]
            c = nd["lagged_hub"][clock][k] if nd else None
            rows[k] = {
                "gap": {"target": t["gap"], "N0": z["gap"], "ND": c["gap"] if c else None},
                "normalised_gap": {"target": t["normalised_gap"], "N0": z["normalised_gap"], "ND": c["normalised_gap"] if c else None},
                "hub_retention": {"target": t["hub_retention_fraction"], "N0": z["hub_retention_fraction"], "ND": c["hub_retention_fraction"] if c else None},
                "comparison_retention": {"target": t["comparison_retention_fraction"], "N0": z["comparison_retention_fraction"], "ND": c["comparison_retention_fraction"] if c else None},
                "slower_decay_than_ND": _sign(t["normalised_gap"], c["normalised_gap"], "slower", "faster") if c and d > 0 else None,
                "slower_decay_than_N0": _sign(t["normalised_gap"], z["normalised_gap"], "slower", "faster") if d > 0 else None,
            }
        out[clock] = rows
    return out


def frozen_checks(results: dict, sizes: tuple[int, ...] = SIZES) -> dict:
    """Identities and acceptance checks declared in the plan."""
    out = {}
    for key, r in results.items():
        probs = check_problems(r)
        out[f"Z-{key}"] = {"holds": not probs, "problems": probs}
    for n in sizes:
        null = results.get(item_id(n, "NULL", "none"))
        if null and "target" in null:
            forms = P.null_closed_forms(n)
            m = len(edges(n))
            worst = 0.0
            for p, f in forms.items():
                r = null["target"]["predicates"][p]
                worst = max(worst, abs(r["prevalence_ct"] - f["prevalence"]), abs(r["entries_per_unit_time"] - f["flux"]), abs(r["lifetime_ct"] - f["prevalence"] / f["flux"]) / (f["prevalence"] / f["flux"]), abs(r["lifetime_jump"] - m * f["prevalence"] / f["flux"]) / (m * f["prevalence"] / f["flux"]), abs(r["omega"] * r["entries_per_unit_time"] - f["omega_flux"]))
            e = null["target"]["edge"]
            worst = max(worst, abs(e["lifetime_ct"] - 1.0), abs(e["lifetime_jump"] - m) / m)
            out[f"N0-closed-forms-N{n}"] = {"holds": worst <= IDENTITY, "max_deviation": worst}
            lag = P.null_lag_closed_forms(n, LAGS)
            lw = 0.0
            for clock in ("continuous", "jump"):
                for d in LAGS:
                    row = null["target"]["lagged_hub"][clock][str(d)]
                    lw = max(lw, abs(row["normalised_gap"] - lag[clock][str(d)]["normalised_gap"]), abs(row["hub_retention_fraction"] - lag[clock][str(d)]["retention"]))
            out[f"N0-lag-closed-forms-N{n}"] = {"holds": lw <= IDENTITY, "max_deviation": lw}
            nc = null.get("nd_construction", {})
            fp = nc.get("resolved") and abs(nc["activity_scale"] - 1.0) <= 1e-12 and max(abs(v - 1.0) for v in nc["birth"][:-1] + nc["death"][1:]) <= 1e-12
            out[f"ND-fixed-point-N{n}"] = {"holds": bool(fp), "activity_scale": nc.get("activity_scale")}
        pc = results.get(item_id(n, "PCOMP", "weak_favour+weak_favour"))
        if pc and "target" in pc and null and "target" in null:
            m = len(edges(n))
            unif = max(abs(row["ct"] / row["orbit_size"] - 2.0**-m) * 2.0**m for row in pc["class_table"])
            out[f"PCOMP-uniform-ct-N{n}"] = {"holds": unif <= IDENTITY, "max_relative_deviation": unif}
            nc = pc.get("nd_construction", {})
            if nc.get("resolved"):
                c = nc["activity_scale"]
                worst = max(abs(v - 1.0) for v in nc["birth"][:-1] + nc["death"][1:])
                for p in P.PREDICATES:
                    a, z = pc["nd"]["predicates"][p], null["target"]["predicates"][p]
                    worst = max(worst, abs(a["lifetime_ct"] * c - z["lifetime_ct"]) / z["lifetime_ct"], abs(a["lifetime_jump"] - z["lifetime_jump"]) / z["lifetime_jump"], abs(a["omega"] - z["omega"]) / max(z["omega"], 1e-300) if z["omega"] else abs(a["omega"]))
                out[f"PCOMP-ND-is-scaled-NULL-N{n}"] = {"holds": worst <= IDENTITY, "activity_scale": c, "max_deviation": worst}
    return out


def replication(r: dict, old: dict | None) -> dict:
    """Class-level CT and JT masses and the mean rate against the published E0B cell."""
    if old is None:
        return {"holds": False, "reason": "no published cell"}
    pub = {row["canonical_state"]: row for row in old["class_table"]}
    worst_ct = worst_jump = 0.0
    ok = len(pub) == len(r["class_table"])
    for row in r["class_table"]:
        o = pub.get(row["canonical_state"])
        if o is None:
            ok = False
            continue
        for key in ("ct", "jump"):
            d = abs(row[key] - o[key])
            good = d <= max(REPLICATION_ABS, REPLICATION_REL * abs(o[key]))
            ok &= good
            if key == "ct":
                worst_ct = max(worst_ct, d)
            else:
                worst_jump = max(worst_jump, d)
    rate_gap = abs(r["target"]["mean_rate_ct"] - old["mean_rate_ct"])
    ok &= rate_gap <= max(REPLICATION_ABS, REPLICATION_REL * old["mean_rate_ct"])
    return {"holds": bool(ok), "max_abs_ct": worst_ct, "max_abs_jump": worst_jump, "mean_rate_abs_gap": rate_gap}


def assemble(results: dict, published: dict, sizes: tuple[int, ...] = SIZES) -> dict:
    tables: dict = {"predicates": {}, "lagged_hub": {}, "nd": {}, "replication": {}}
    for n in sizes:
        null = results.get(item_id(n, "NULL", "none"))
        for f, g in FAMILY_GRADES:
            key = item_id(n, f, g)
            r = results.get(key)
            if not r or "target" not in r:
                tables["predicates"][key] = None
                continue
            tables["replication"][key] = replication(r, published.get(key))
            nd = r.get("nd")
            if null and "target" in null:
                tables["predicates"][key] = {p: predicate_row(r["target"], null["target"], nd, p) for p in P.PREDICATES}
                tables["lagged_hub"][key] = lag_row(r["target"], null["target"], nd)
            nc = r.get("nd_construction", {})
            tables["nd"][key] = {k: nc.get(k) for k in ("resolved", "activity_scale", "rare_bins", "log_phi_range", "min_unscaled_transition_rate", "density_l1_vs_target", "mean_rate_relative_gap", "detailed_balance_max_relative", "global_balance_relative", "iterative_cross_check")}
            tables["nd"][key]["jump_density_l1_target_vs_nd"] = r.get("jump_density_l1_target_vs_nd")
            tables["nd"][key]["mean_edges_jump"] = {"target": float(np.arange(len(r["target"]["density_jump"])) @ np.array(r["target"]["density_jump"])), "ND": float(np.arange(len(nd["density_jump"])) @ np.array(nd["density_jump"])) if nd else None}
    checks = frozen_checks(results, sizes)
    for key, rep in tables["replication"].items():
        checks[f"REP-{key}"] = rep
    tables["frozen_expectations"] = checks
    return tables


# --- plan, execution, publication ---------------------------------------------


PLAN_RELPATH = "gravity-time/plans/round-e5a-plan.json"
GENERATED_RELPATH = "gravity-time/generated/round-e5a"
TABLES_RELPATH = "gravity-time/reports/round-e5a-tables.json"
ATLAS_RELPATH = "gravity-time/reports/gt-e5a-atlas.md"
E0B_TABLES_RELPATH = "gravity-time/reports/round-e0b-tables.json"
WATCHDOG_SECONDS = {5: 900, 6: 3600}
ROUND_WALL_CAP_SECONDS = 4 * 3600
WORKERS = 4
ONTOLOGY = {"G": 0, "H": 0, "L": 0, "N": [5, 6], "O": 2, "S": 0, "grammar": "ordinary pair DSL"}
REFERENCE_FILES = (
    "research-methods/open-thetical-research.md",
    "gravity-time/provenance/prompts/GT-P009-agent-input.md",
    "gravity-time/docs/e5-coverage-and-definition-audit.md",
    "gravity-time/docs/e5-definitions-and-null-construction.md",
    "gravity-time/docs/gt-p008-next-round-options.md",
    "gravity-time/docs/reference-architecture-review.md",
    "gravity-time/reports/round-e0b-tables.json",
    "gravity-time/plans/round-e0b-plan.json",
    "gravity-time/docs/foundational-bridge-map.md",
    "constraint-lab/docs/scientific-plan-discipline.md",
    "constraint-lab/src/rs_constraint_lab/gtpersist.py",
    "constraint-lab/src/rs_constraint_lab/gte5a.py",
    "constraint-lab/tests/test_gtpersist.py",
)


def prepare_plan(repo: Path, *, source_commit: str) -> dict:
    from rs_constraint_lab.durable import sha256_file
    from rs_constraint_lab.explore08 import plan_hash

    cells = items()
    document = {
        "analysis_only": True,
        "analysis_version": ANALYSIS_VERSION,
        "chosen_because": "GT-P008 next-round option C (FREE persistence feasibility, definitions first); authorised by GT-P009",
        "clocks": {"continuous": "generator W, CT stationary law pi; lifetimes in model time units", "jump": "jump chain P = W/q, law nu = pi q / E_pi[q]; lengths in jumps"},
        "comparators": {
            "N0": "the NULL item at the same N (all rates 1); same predicates and formulas",
            "ND": "per target item: p_k = CT edge-count profile of the target law; phi_k = p_k / C(M,k); birth_k = min(1, phi_{k+1}/phi_k), death_{k+1} = min(1, phi_k/phi_{k+1}); all rates multiplied by c = E_pi_target[q] / E_pi_ND,unscaled[q]. Reversible and label-covariant; matches the CT density marginal and the CT mean event rate only, NOT the full state law, local rates, correlations or the jump-clock density marginal (reported). Analytic law pi_ND(x) = phi_|x| verified by detailed and global balance; an iterative solve (cap 20,000 lazy iterations) is a cross-check only. Rare bins p_k < 1e-12 flagged with their masses; the smallest unscaled transition rate is reported (interior rare bins make ND near-reducible). A zero bin makes ND unresolved for that item; nothing is smoothed",
            "static_reference": "ND's motif prevalence equals the static density-standardised prevalence (uniform within each k); it is reported as that and never as a dynamical result",
            "underdetermination": "ND is one reasonable dynamics at a matched density profile; any contrast against it is a fact about that comparison",
        },
        "deliberate_omissions": {"n7": "not authorised", "e5b": "not authorised", "held_or_multi_source": "not authorised", "grade_sweep": "not authorised", "trajectories": "none", "survival_curves": "not computed (optional in GT-P009)", "identity_tracking": "not defined in E5A (Omega counts toggles, not replacements)"},
        "discovery_matrix": {
            "per_row": "for every non-NULL family, N and predicate, against N0 and against ND: signs of lifetime (CT, jump), rho (CT, jump), Omega (flexible only) and CT prevalence; a sign is 'tie' when |a-b| <= 1e-9 max(|a|,|b|)",
            "cells": ["longer_both_clocks", "longer_ct_only", "longer_jump_only", "tie_both_clocks", "not_longer"],
            "turnover_suffix": "intact rows: intact_no_turnover (theorem); flexible rows: turnover_more / turnover_fewer / turnover_tie",
            "family_level_patterns_to_report": ["sustained episode lifetime with Omega ~ comparator (intact-like persistence)", "Omega above comparator without longer life", "CT-only or jump-only enhancement", "closure-only persistence (CLOSEW, CSPH)", "path-family persistence (PATHF, PATHH, CSPH) together with their published nonzero circulation", "no enhancement anywhere", "unexpected distinctions"],
            "no_threshold": "no magnitude threshold, aggregate score or success criterion; magnitudes are reported beside signs",
        },
        "estimands": {
            "episode": "J_A (entry = exit flux, both computed), L_ct = pi(A)/J_A, L_jump = E_pi[q 1_A]/J_A (jumps from A states per episode, exit jump included), off-episode means (1-pi(A))/J_A and (E_pi[q]-E_pi[q 1_A])/J_A, entry-to-entry recurrence 1/J_A and E_pi[q]/J_A (algebraically dependent on the above; not independent confirmations), entries per unit time J_A and per event J_A/E_pi[q], internal events per episode (= L_jump - 1)",
            "turnover": "Omega = flux of eligible internal toggles / J_A (definitions note D-4, D-5); eligible share Omega/(L_jump - 1); intact predicates: required-edge internal flux (identically 0) and required-edge exit share (1); F_TRI exit shares: anchor dissolution versus loss of the last completer",
            "edge": "present-episode lifetime of slot (0,1) by the same formulas; rho_ct = L_ct(A)/L_ct(edge), rho_jump = L_jump(A)/L_jump(edge)",
            "prevalence": "pi(A), nu(A) (re-expressions of published laws)",
            "lagged_hub": "x0 ~ pi (CT) or nu (jump); hub chosen once uniformly among maximum-degree vertices; comparison vertex uniform over all N vertices; at each lag: expected degree of hub and comparison vertex, gap, gap/gap(0), expected number of the hub's initial neighbours still adjacent and its ratio to the expected initial degree (and the same for the comparison vertex)",
            "secondary": "residual (occupation-sampled) life in both clocks and the entrance first-passage mean life, from the killed jump chain on A by BiCGSTAB (relative residual 1e-12, cap 20,000 iterations or 60 s per solve); unresolved solves are recorded",
            "density": "CT and jump edge-count profiles of target and ND; jump-profile L1 discrepancy and mean jump-clock edge count",
        },
        "experiment_id": EXPERIMENT_ID,
        "families": {f: {g: {"components": [{"grade": cg, "kind": k} for k, cg in components(f, g)]}} for f, g in FAMILY_GRADES},
        "frozen_identities": {
            "Z_item": "per item: positive-rate full FREE space; stationary resolved (two starts within 1e-10, residual <= 1e-12); law symmetric under S_N within 1e-10; for target and ND: entry/exit flux balance and jump-length identity within 1e-9; relabelled instances within 1e-9 relative; intact required-edge internal flux and Omega exactly 0; every predicate classified ergodic_episodes; comparison-vertex degree constant over lags within 1e-9; lag checks: lumpability defect <= 1e-12, propagator row sums within 1e-9 and entries >= -1e-12, stationarity L1 <= 1e-9, non-dyadic semigroup <= 1e-9, lumped versus full jump chain <= 1e-10, pair-permutation covariance <= 1e-10, uniformisation cross-check (where cheap) <= 1e-9; ND detailed balance <= 1e-12, global balance <= 1e-10, density L1 and mean-rate gap <= 1e-10",
            "N0_closed_forms": "NULL items: every predicate's prevalence, J, L_ct, L_jump (= M L_ct) and Omega J equal gtpersist.null_closed_forms within 1e-9; edge L_ct = 1 and L_jump = M; lag normalised gap exp(-2t) (t = lag/M) and (1-2/M)^lag, retention 1/2 + 1/2 of the same",
            "ND_fixed_point": "NULL items: ND activity scale 1 and every unscaled rate 1 within 1e-12",
            "PCOMP_uniform_ct": "PCOMP: CT law uniform within 1e-9 relative per state",
            "PCOMP_ND_is_scaled_NULL": "PCOMP: ND rates all 1 before scaling (uniform CT law gives a binomial profile), so ND CT lifetimes x c, jump lifetimes and Omega equal N0's within 1e-9",
            "REP": "replication of the published E0B cell: class-level CT and jump masses and mean rate within max(1e-10, 1e-8 x |published|)",
            "separation_note": "no expectation on any target lifetime, ratio, Omega or lag decay",
        },
        "history": False,
        "initial_conditions": "primary estimates are stationary (unique class); no transient or cold-start observable is computed",
        "instances": {p: {"primary": list(P.primary_instance(p)), "relabelled": "image under v -> N-1-v"} for p in P.PREDICATES},
        "items": cells,
        "lag_set": {"jump_events": list(LAGS), "continuous": "t = lag / E_pi[q] of each law (its own mean rate; ND equals the target's by calibration), plus t = 0; a translation of average activity, not an equivalence of clocks", "method": "jump: exact full-space propagation; continuous: exact Pade-13 scaling-and-squaring matrix exponential of the generator lumped by the permutations fixing vertices 0 and 1 (240 states at N=5, 1,992 at N=6)"},
        "meta_constraints": False,
        "method": {"name": "Open-Thetical Research", "path": "research-methods/open-thetical-research.md", "version": "1.0"},
        "new_primitives": False,
        "ontology": ONTOLOGY,
        "open_questions_without_prediction": ["central E5 question (GT-P009 section 0)", "outcomes 1-7 of GT-P009 section 0", "anything not anticipated"],
        "parameter_fit": False,
        "predicate_ids": predicate_ids(),
        "predicates": {
            "I_TRI": "ab, bc, ac present (non-induced)",
            "I_STAR": "spokes ca, cb, cd present; leaf-leaf edges free",
            "I_2PATH": "ab, bc present; ac free (instance (1,0,2): edges 01, 02)",
            "F_TRI": "anchor ab present and at least one c with ac, bc present; eligible turnover: toggle of ac or bc whose other leg is present, A before and after",
            "F_STAR": "deg(c) >= 3; eligible turnover: toggle of an edge at c, A before and after",
            "F_2PATH": "deg(c) >= 2; eligible turnover: as F_STAR",
            "notes": "F_STAR implies F_2PATH (not independent species); a persistent anchored centre is not an unlabelled mobile structure; anchors are measurement-only",
        },
        "pre_freeze_exposure": {
            "published": "all 12 kernels are published E0B FREE cells; their class tables (hence every prevalence, the CT density profile p_k and E_pi[q], the ND inputs) are known; E0B/E0A N=5 autocorrelation times and E2A N=5 hub statistics are published (audit section 3)",
            "agent_viewed": "published values of FREE-N5-PATHF-weak_suppress (E0B hub_frame, autocorrelation; E2A hub_structure, partner frame) and two class-table rows of FREE-N6-CSPH during the audit",
            "engineering": "proof fixtures: synthetic CTMCs and N<=4 FREE kernels of the six families (tests/test_gtpersist.py); timing: NULL N=6 with all rates x 2^24 and a synthetic density-only N=6 rule (dissolution 2^k); no E5A observable of any N=5 or N=6 cell was computed before freezing",
            "reference_hashes": {rel: sha256_file(repo / rel) for rel in REFERENCE_FILES},
        },
        "programme": "GT",
        "prompt_id": PROMPT_ID,
        "question": "Without any held reference, do the existing label-covariant relational constraints sustain recognisable configurations longer than appropriate null dynamics would, and can an organisation persist through turnover of some of its constituent relations?",
        "round_id": ROUND_ID,
        "rule_reading": "no rule reads a motif, anchor, selected hub, source label or history; all are analysis-defined",
        "schema": "rs-gt.e5a-plan/v1",
        "software": {"analysis_module": "rs_constraint_lab.gte5a", "kernel": gtkernel.KERNEL_VERSION, "numpy": np.__version__, "observables": gtobs.OBSERVABLES_VERSION, "persistence": P.PERSIST_VERSION, "python": __import__("platform").python_version(), "scipy": "not used"},
        "source_commit": source_commit,
        "stochastic_trajectories": "none",
        "stop_conditions": {"item": f"watchdog {WATCHDOG_SECONDS} seconds by N", "round": f"all items or {ROUND_WALL_CAP_SECONDS} s; then stop", "unresolved": "recorded; no retuning, no replacement cell, no changed tolerance", "amendment": "any cell, predicate or estimand change stops the round", "after_round": "no E5B"},
        "tolerances": {"identity": IDENTITY, "tie_relative": P.TIE_RELATIVE, "lag": LAG_TOLERANCE, "replication": [REPLICATION_ABS, REPLICATION_REL], "rare_mass": P.RARE_MASS, "killed_solve": [P.KILLED_TOLERANCE, P.KILLED_CAP, P.KILLED_SECONDS]},
        "work_count": {"items": len(cells), "kernels": 12, "predicate_analyses": len(predicate_ids()), "laws_per_item": "target and ND", "largest_state_space": 32768, "largest_lumped_chain": 1992, "memory_ceiling_per_worker_bytes": 2_000_000_000, "round_wall_cap_seconds": ROUND_WALL_CAP_SECONDS, "watchdog_seconds": {str(k): v for k, v in WATCHDOG_SECONDS.items()}, "workers": WORKERS, "estimate_note": "about 1-3 min per N=6 item and seconds per N=5 item, measured on synthetic N=6 fixtures (execution record); under 30 min in total expected, not promised"},
    }
    document["plan_hash"] = plan_hash(document)
    return document


def require_execution(repo: Path, commit: str | None, *, require_remote: bool = True) -> dict:
    from rs_constraint_lab.explore08 import FrozenPlanError, remote_contains, require_frozen_plan

    plan = require_frozen_plan(repo, commit, PLAN_RELPATH, disk_path=repo / PLAN_RELPATH)
    if require_remote and not remote_contains(repo, commit or ""):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    if plan.get("items") != items() or plan.get("new_primitives") is not False or plan.get("ontology") != ONTOLOGY:
        raise FrozenPlanError("execution refused: E5A plan contract drifted")
    return plan


def execute_item(root: Path, item: dict) -> dict:
    import resource

    from rs_constraint_lab.durable import atomic_write_json

    started = time.perf_counter()

    def payload(result, status):
        return {"item": item, "item_id": item["item_id"], "peak_rss_mb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, "result": result, "status": status, "wall_seconds": time.perf_counter() - started}

    def on_main(result):
        atomic_write_json(root / "items" / f"{item['item_id']}.partial.json", payload(result, "complete_checks_interrupted"))

    result = analyse_item(item, on_main=on_main)
    atomic_write_json(root / "items" / f"{item['item_id']}.json", payload(result, "complete"))
    partial = root / "items" / f"{item['item_id']}.partial.json"
    if partial.exists():
        partial.unlink()
    return {}


def run(root: Path, plan: dict, *, workers: int = WORKERS, **kwargs) -> list[dict]:
    return gte1.run(root, plan, workers=workers, watchdogs=kwargs.pop("watchdogs", WATCHDOG_SECONDS), wall_cap=kwargs.pop("wall_cap", ROUND_WALL_CAP_SECONDS), module=kwargs.pop("module", "rs_constraint_lab.gte5a"), **kwargs)


def publish(root: Path, plan: dict, out: Path, *, frozen_plan_commit: str, e0b_tables: Path) -> str:
    from rs_constraint_lab.durable import atomic_write_json, canonical_json, read_json, sha256_bytes

    records = {}
    for it in plan["items"]:
        path = root / "items" / f"{it['item_id']}.json"
        records[it["item_id"]] = read_json(path) if path.is_file() else {"item_id": it["item_id"], "status": "missing"}
    results = {k: v["result"] for k, v in records.items() if "result" in v}
    published = read_json(e0b_tables)["results"]
    assembled = assemble(results, published)
    item_records = {k: {"numerical_problems": check_problems(results[k]) if k in results else None, "peak_rss_mb": v.get("peak_rss_mb_parent_view", v.get("peak_rss_mb")), "role": next(it["role"] for it in plan["items"] if it["item_id"] == k), "status": v["status"], "wall_seconds": v.get("wall_seconds"), **({"interruption": v["interruption"]} if "interruption" in v else {}), **({"exit_code": v.get("exit_code"), "log_tail": v.get("log_tail")} if v["status"] == "failed" else {})} for k, v in records.items()}
    payload = {"analysis_version": ANALYSIS_VERSION, "experiment_id": EXPERIMENT_ID, "frozen_analysis_plan_commit": frozen_plan_commit, "item_records": item_records, "plan_hash": plan["plan_hash"], "results": results, "round_id": ROUND_ID, "schema": "rs-gt.e5a-tables/v1", "source_commit": plan.get("source_commit"), "status_counts": {s: sum(r["status"] == s for r in item_records.values()) for s in sorted({r["status"] for r in item_records.values()})}, **assembled}
    body = dict(payload)
    body["payload_sha256"] = sha256_bytes(canonical_json(payload).encode("utf-8"))
    atomic_write_json(out, body)
    return body["payload_sha256"]


def _f(v, d: int = 3) -> str:
    if v is None:
        return "—"
    if isinstance(v, str):
        return v
    if v != 0 and (abs(v) < 1e-3 or abs(v) >= 1e4):
        return f"{v:.2e}"
    return f"{v:.{d}f}"


def render_atlas(repo: Path, tables: Path | None = None) -> str:
    import json

    t = json.loads((tables or repo / TABLES_RELPATH).read_text())
    L = [
        "# GT-E5A FREE persistence atlas",
        "",
        f"Generated from `{TABLES_RELPATH}` (payload `{t['payload_sha256'][:12]}…`), frozen plan `{t['frozen_analysis_plan_commit'][:7]}`. Every item, predicate, comparator and diagnostic is listed. **N0** = NULL at the same N; **ND** = the density-matched comparator (CT edge-count profile and CT mean rate only; not jump-density matched). Lifetimes: CT in model time units, jump in jumps. ρ = motif lifetime / edge present-lifetime in the same law and clock. Ω = eligible within-episode toggles per episode (intact motifs: 0 by theorem). Prevalences are re-expressions of published E0B laws.",
        "",
    ]
    fx = t["frozen_expectations"]
    L += [f"Frozen identities and checks: **{sum(c['holds'] for c in fx.values())}/{len(fx)} hold**.", ""]
    bad = [(k, c) for k, c in fx.items() if not c["holds"]]
    if bad:
        L += ["Not holding: " + "; ".join(f"{k} ({c.get('problems') or c.get('reason') or c.get('max_deviation')})" for k, c in bad) + ".", ""]
    L += ["## Item records", "", "| Item | Role | Status | Wall s | Peak MB | Problems |", "| --- | --- | --- | --- | --- | --- |"]
    for k, rec in t["item_records"].items():
        L.append(f"| {k} | {rec['role']} | {rec['status']} | {_f(rec['wall_seconds'], 1)} | {_f(rec['peak_rss_mb'], 0)} | {'; '.join(rec['numerical_problems'] or []) or 'none'} |")
    L += ["", "## ND construction", "", "| Item | scale c | rare bins (p_k < 1e-12) | log φ range | min unscaled rate | CT density L1 | jump density L1 target vs ND | mean jump edges target / ND | iterative cross-check |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for k, nd in t["nd"].items():
        ic = nd.get("iterative_cross_check") or {}
        L.append(f"| {k} | {_f(nd.get('activity_scale'))} | {nd.get('rare_bins') or 'none'} | {_f(nd.get('log_phi_range'), 1)} | {_f(nd.get('min_unscaled_transition_rate'))} | {_f(nd.get('density_l1_vs_target'))} | {_f(nd.get('jump_density_l1_target_vs_nd'))} | {_f(nd['mean_edges_jump']['target'], 2)} / {_f(nd['mean_edges_jump']['ND'], 2)} | {'resolved' if ic.get('resolved') else 'unresolved'} ({ic.get('iterations')}) |")
    L += ["", "## Predicates: target, N0, ND", ""]
    for key, rows in t["predicates"].items():
        if rows is None:
            L += [f"**{key}**: unresolved", ""]
            continue
        L += [f"**{key}**", "", "| Predicate | law | π(A) | ν(A) | L_ct | L_jump | entries/unit t | ρ_ct | ρ_jump | Ω | eligible share | vs N0 | vs ND |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        for p, row in rows.items():
            for law in ("target", "N0", "ND"):
                v = row[law]
                if v is None:
                    continue
                pat0 = row["vs_N0"]["pattern"] if law == "target" and row["vs_N0"] else ""
                patd = row["vs_ND"]["pattern"] if law == "target" and row["vs_ND"] else ""
                L.append(f"| {p if law == 'target' else ''} | {law} | {_f(v['prevalence_ct'])} | {_f(v['prevalence_jump'])} | {_f(v['lifetime_ct'])} | {_f(v['lifetime_jump'], 2)} | {_f(v['entries_per_unit_time'])} | {_f(v['rho_ct'])} | {_f(v['rho_jump'])} | {_f(v['omega'])} | {_f(v['eligible_share'])} | {pat0} | {patd} |")
        L.append("")
    L += ["## Lifetime and ρ ratios (target / comparator)", "", "| Item | Predicate | L_ct/N0 | L_jump/N0 | L_ct/ND | L_jump/ND | ρ_ct/ND | ρ_jump/ND | Ω − Ω_ND | π/π_ND |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for key, rows in t["predicates"].items():
        if not rows:
            continue
        for p, row in rows.items():
            a, b = row["vs_N0"], row["vs_ND"]
            if b is None:
                L.append(f"| {key} | {p} | {_f(a['lifetime_ratio_ct'])} | {_f(a['lifetime_ratio_jump'])} | — | — | — | — | — | — |")
            else:
                L.append(f"| {key} | {p} | {_f(a['lifetime_ratio_ct'])} | {_f(a['lifetime_ratio_jump'])} | {_f(b['lifetime_ratio_ct'])} | {_f(b['lifetime_ratio_jump'])} | {_f(b['rho_ratio_ct'])} | {_f(b['rho_ratio_jump'])} | {_f(b['omega_difference'])} | {_f(b['prevalence_ratio_ct'])} |")
    L += ["", "## Lagged hub (hub chosen once at a stationary start)", "", "Normalised gap = (hub degree − comparison degree at lag) / (same at lag 0). Retention = expected initial neighbours still adjacent / expected initial degree.", ""]
    for key, rows in t["lagged_hub"].items():
        L += [f"**{key}**", "", "| clock | lag | gap target / N0 / ND | normalised gap target / N0 / ND | hub retention target / N0 / ND | comparison retention target | decay vs ND | decay vs N0 |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
        for clock in ("continuous", "jump"):
            for d, r in rows[clock].items():
                g, ng, hr = r["gap"], r["normalised_gap"], r["hub_retention"]
                L.append(f"| {clock} | {d} | {_f(g['target'])} / {_f(g['N0'])} / {_f(g['ND'])} | {_f(ng['target'])} / {_f(ng['N0'])} / {_f(ng['ND'])} | {_f(hr['target'])} / {_f(hr['N0'])} / {_f(hr['ND'])} | {_f(r['comparison_retention']['target'])} | {r['slower_decay_than_ND'] or '—'} | {r['slower_decay_than_N0'] or '—'} |")
        L.append("")
    L += ["## Secondary: residual life and entrance first passage", "", "Occupation-sampled residual life is a different quantity from the entrance mean life L (Palm: R_ct = E[L²]/(2E[L]) ≥ L/2).", "", "| Item | law | Predicate | resolved | entrance mean ct / L_ct | entrance mean jump / L_jump | residual ct | residual jump |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for key, r in t["results"].items():
        sec = r.get("secondary_residual_life") or {}
        for law in ("target", "nd"):
            for p, s in (sec.get(law) or {}).items():
                base = r[law]["predicates"][p]
                if s.get("resolved"):
                    L.append(f"| {key} | {law} | {p} | yes | {_f(s['entrance_mean_life_ct'] / base['lifetime_ct'], 9)} | {_f(s['entrance_mean_life_jump'] / base['lifetime_jump'], 9)} | {_f(s['occupation_residual_life_ct'])} | {_f(s['occupation_residual_life_jump'], 2)} |")
                else:
                    L.append(f"| {key} | {law} | {p} | no ({s.get('reason')}) | — | — | — | — |")
    L += ["", "## Replication of published E0B laws", "", "| Item | holds | max |Δct| | max |Δjump| | mean-rate gap |", "| --- | --- | --- | --- | --- |"]
    for k, rep in t["replication"].items():
        L.append(f"| {k} | {rep['holds']} | {_f(rep.get('max_abs_ct'))} | {_f(rep.get('max_abs_jump'))} | {_f(rep.get('mean_rate_abs_gap'))} |")
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m rs_constraint_lab.gte5a")
    sub = parser.add_subparsers(dest="command", required=True)
    one = sub.add_parser("item")
    one.add_argument("--root", required=True)
    one.add_argument("--item-id", required=True)
    pl = sub.add_parser("plan")
    pl.add_argument("--source-commit", required=True)
    ex = sub.add_parser("run")
    ex.add_argument("--commit", required=True)
    pb = sub.add_parser("publish")
    pb.add_argument("--commit", required=True)
    sub.add_parser("atlas")
    args = parser.parse_args(argv)
    from rs_constraint_lab.durable import atomic_write_json, read_json

    repo = Path(__file__).resolve().parents[3]
    if args.command == "plan":
        plan = prepare_plan(repo, source_commit=args.source_commit)
        atomic_write_json(repo / PLAN_RELPATH, plan)
        print(f"wrote {PLAN_RELPATH} plan_hash {plan['plan_hash']}")
        return 0
    if args.command == "run":
        plan = require_execution(repo, args.commit)
        out = run(repo / GENERATED_RELPATH, plan)
        print({s: sum(r.get("status") == s for r in out) for s in sorted({r.get("status") for r in out})})
        return 0
    if args.command == "publish":
        plan = require_execution(repo, args.commit)
        digest = publish(repo / GENERATED_RELPATH, plan, repo / TABLES_RELPATH, frozen_plan_commit=args.commit, e0b_tables=repo / E0B_TABLES_RELPATH)
        print(f"wrote {TABLES_RELPATH} payload {digest}")
        return 0
    if args.command == "atlas":
        text = render_atlas(repo)
        (repo / ATLAS_RELPATH).write_text(text)
        print(f"wrote {ATLAS_RELPATH} ({len(text)} bytes)")
        return 0
    root = Path(args.root)
    plan = read_json(root / "plan.json")
    (item,) = [it for it in plan["items"] if it["item_id"] == args.item_id]
    if item not in items() and not plan.get("synthetic_fixture"):
        raise SystemExit("item is not in the E5A manifest")
    execute_item(root, item)
    return 0


if __name__ == "__main__":
    sys.exit(main())
