"""GT round E5B: replacement-aware persistence, local event counts and the NK comparator (GT-P010).

The same twelve FREE kernels as E5A (N = 5, 6). Each item recomputes the kernel and
its stationary law, replicates the published E5A episode values (a labelled check,
not evidence), then computes for the three flexible predicates on the target law,
on ND (E5A's density-matched comparator, unchanged) and on NK (density- and
adjacent-layer-flux-matched), with primary and relabelled anchors:

* E5A episode quantities (L_ct, L_jump, Omega, prevalence) and the anchor-local count L_local;
* entry-set tracking: feasibility classes, distinct departures, complete renewal
  (STRUCTURALLY_IMPOSSIBLE where T10 says so), F_STAR maximal partial renewal;
* the immediate-reversal (flicker) diagnostic;
* layer diagnostics (p_k, adjacent fluxes, E[q|k], within-layer dispersion) and local hazard given k.

N0 is the NULL item of the same size. Definitions:
``gravity-time/docs/e5b-definitions-controls-and-feasibility.md``.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np

from rs_constraint_lab import gte1, gte5a, gtkernel, gtobs
from rs_constraint_lab import gtpersist as P
from rs_constraint_lab import gtrenew as R
from rs_constraint_lab.state import edges

ROUND_ID = "round-e5b"
EXPERIMENT_ID = "gt-round-e5b-free-replacement"
ANALYSIS_VERSION = "gt-e5b/v1"
PROMPT_ID = "GT-P010"
MODE = "FREE"
FAMILY_GRADES = gte5a.FAMILY_GRADES
SIZES = (5, 6)
IDENTITY = 1e-9
REPLICATION_ABS = 1e-10
REPLICATION_REL = 1e-8
NK_MATCH = 1e-9
HUB_COMMIT = "38c2501bbab22ca1eb2288ea76a962ac0170d5e6"
ROLE = gte5a.ROLE


def items() -> list[dict]:
    return [{**it, "prior_cell": f"round-e5a {it['item_id']}"} for it in gte5a.items()]


def predicate_ids() -> list[str]:
    return [f"{it['item_id']}:{p}" for it in items() for p in R.FLEXIBLE]


# --- per-item analysis ------------------------------------------------------------


def law_problems(block: dict, label: str) -> list[str]:
    out = []
    for key in ("predicates", "relabelled"):
        for p in R.FLEXIBLE:
            b = block[key][p]
            ep, lc, rep = b["episode"], b["local"], b["replacement"]
            if ep["flux_balance_relative"] > IDENTITY:
                out.append(f"{label}/{key}/{p}: entry/exit flux imbalance")
            if abs(lc["entry_flux"] - 0.5 * (ep["entry_flux"] + ep["exit_flux"])) > IDENTITY * lc["entry_flux"]:
                out.append(f"{label}/{key}/{p}: entrance weights do not sum to J_A")
            if lc["lifetime_local"] > lc["lifetime_jump"] * (1 + 1e-12):
                out.append(f"{label}/{key}/{p}: L_local exceeds L_jump")
            if abs(lc["exit_local_share"] - 1.0) > 1e-12:
                out.append(f"{label}/{key}/{p}: a non-local exit")
            for name, s in rep["solves"].items():
                if not s.get("resolved"):
                    out.append(f"{label}/{key}/{p}: {name} UNRESOLVED")
                if s.get("bounds_violation", 0.0) > 1e-10:
                    out.append(f"{label}/{key}/{p}: {name} outside [0,1]")
                if s.get("dense_max_abs_difference") is not None and s["dense_max_abs_difference"] > IDENTITY:
                    out.append(f"{label}/{key}/{p}: {name} dense and iterative disagree")
            if p == "F_STAR" and rep["renewal_status"] != "STRUCTURALLY_IMPOSSIBLE":
                out.append(f"{label}/{key}/{p}: F_STAR renewal not labelled STRUCTURALLY_IMPOSSIBLE")
    for p in R.FLEXIBLE:
        a, b = block["predicates"][p], block["relabelled"][p]
        pairs = [(a["local"]["lifetime_local"], b["local"]["lifetime_local"]), (a["replacement"]["expected_distinct_departures_per_episode"], b["replacement"]["expected_distinct_departures_per_episode"])]
        if a["replacement"].get("renewal_unconditional") is not None:
            pairs.append((a["replacement"]["renewal_unconditional"], b["replacement"]["renewal_unconditional"]))
        if a["flicker"].get("reversal_next_event") is not None:
            pairs.append((a["flicker"]["reversal_next_event"], b["flicker"]["reversal_next_event"]))
        if a["replacement"].get("partial_renewal_probability") is not None:
            pairs.append((a["replacement"]["partial_renewal_probability"], b["replacement"]["partial_renewal_probability"]))
        if any(abs(x - y) > IDENTITY * max(abs(x), abs(y), 1e-300) for x, y in pairs):
            out.append(f"{label}/{p}: relabelled anchor disagrees")
    return out


def analyse_item(item: dict, *, on_main=None, published: dict | None = None) -> dict:
    n = item["n"]
    m = len(edges(n))
    comps = [tuple(c) for c in item["components"]]
    timings: dict[str, float] = {}
    t0 = time.perf_counter()
    chain, _ = gtkernel.reachable_chain(n, MODE, comps)
    result: dict = {"analysis_version": ANALYSIS_VERSION, "item_id": item["item_id"], "kernel_version": gtkernel.KERNEL_VERSION, "renew_version": R.RENEW_VERSION, "persist_version": P.PERSIST_VERSION}
    result["ergodicity"] = {"all_rates_positive": bool((chain.W > 0).all()), "full_space": bool(len(chain.states) == 1 << m)}
    stat = gtobs.stationary(chain, 0)
    timings["build_stationary"] = time.perf_counter() - t0
    result["stationary"] = {k: v for k, v in stat.items() if k not in ("ct", "jump")}
    if not stat["resolved"]:
        result["status_note"] = "target stationary law unresolved"
        return result
    ct = stat["ct"]
    result["pcomp_uniform_max_relative"] = float(np.abs(ct * (1 << m) - 1.0).max()) if item["family"] == "PCOMP" else None
    # replication of published E5A episode values (a check, not evidence)
    rep = {}
    for p in R.FLEXIBLE:
        e = P.analyse_predicate(chain, ct, n, p, P.primary_instance(p))
        rep[p] = {k: e.get(k) for k in ("prevalence_ct", "prevalence_jump", "lifetime_ct", "lifetime_jump", "omega")}
    result["e5a_replication_values"] = rep
    if published is not None:
        worst = 0.0
        for p in R.FLEXIBLE:
            old = published[p]["target"]
            for k, v in rep[p].items():
                if old.get(k) is None:
                    continue
                worst = max(worst, abs(v - old[k]) / max(REPLICATION_ABS, REPLICATION_REL * abs(old[k])))  # > 1 fails
        result["e5a_replication_worst_over_tolerance"] = worst
    t0 = time.perf_counter()
    result["target"] = R.analyse_law(chain, ct, n)
    result["target_problems"] = law_problems(result["target"], "target")
    timings["target"] = time.perf_counter() - t0
    lf = R.layer_fluxes(chain, ct, n)
    # ND (unchanged from E5A)
    t0 = time.perf_counter()
    p_k = P.density_profile(chain.states, ct, m)
    nd_r = P.nd_rates(p_k)
    if not nd_r["resolved"]:
        result["nd_construction"] = {"resolved": False, "reason": nd_r["reason"]}
    else:
        nd, pi_nd, info = P.nd_chain(n, p_k, float(ct @ chain.rates))
        info["resolved"] = True
        result["nd_construction"] = info
        result["nd"] = R.analyse_law(nd, pi_nd, n)
        result["nd_problems"] = law_problems(result["nd"], "nd")
        result["nd_jump_density_l1_vs_target"] = float(np.abs(np.array(result["nd"]["density_jump"]) - np.array(result["target"]["density_jump"])).sum())
    timings["nd"] = time.perf_counter() - t0
    # NK
    t0 = time.perf_counter()
    nk_r = R.nk_rates(lf["p"], lf["up"])
    if not nk_r["resolved"]:
        result["nk_construction"] = {"resolved": False, "reason": nk_r["reason"], "zero_bins": nk_r["zero_bins"], "zero_fluxes": nk_r["zero_fluxes"]}
    else:
        nk, pi_nk, info = R.nk_chain(n, lf["p"], lf["up"])
        lnk = R.layer_fluxes(nk, pi_nk, n)
        info["identities"] = R.nk_identities(lf, lnk)
        info["mean_rate_relative_gap"] = abs(float(pi_nk @ nk.rates) - float(ct @ chain.rates)) / float(ct @ chain.rates)
        info["jump_density_max_abs_gap"] = float(np.abs(P.jump_density(nk, pi_nk, n) - P.jump_density(chain, ct, n)).max())
        info["resolved"] = True
        result["nk_construction"] = info
        result["nk"] = R.analyse_law(nk, pi_nk, n)
        result["nk_problems"] = law_problems(result["nk"], "nk")
    timings["nk"] = time.perf_counter() - t0
    result["timings"] = timings
    if on_main is not None:
        on_main(result)
    return result


def check_problems(r: dict) -> list[str]:
    out = []
    e = r.get("ergodicity", {})
    if not (e.get("all_rates_positive") and e.get("full_space")):
        out.append("not the positive-rate full FREE space")
    if not r.get("stationary", {}).get("resolved"):
        return out + ["stationary unresolved"]
    if r.get("e5a_replication_worst_over_tolerance") is None:
        out.append("E5A replication not checked")
    elif r["e5a_replication_worst_over_tolerance"] > 1.0:
        out.append("E5A replication failed")
    if r.get("pcomp_uniform_max_relative") is not None and r["pcomp_uniform_max_relative"] > IDENTITY:
        out.append("PCOMP law not uniform")
    out += r.get("target_problems", [])
    nc = r.get("nd_construction", {})
    if not nc.get("resolved"):
        out.append("ND UNRESOLVED")
    else:
        if nc["detailed_balance_max_relative"] > 1e-12 or nc["global_balance_relative"] > 1e-10:
            out.append("ND balance")
        if nc["density_l1_vs_target"] > 1e-10 or nc["mean_rate_relative_gap"] > 1e-10:
            out.append("ND calibration")
        out += r.get("nd_problems", [])
    kc = r.get("nk_construction", {})
    if not kc.get("resolved"):
        out.append("NK UNRESOLVED")
    else:
        if kc["detailed_balance_max_relative"] > 1e-12 or kc["global_balance_relative"] > 1e-10:
            out.append("NK balance")
        ids = kc["identities"]
        if max(ids["p_relative"], ids["up_flux_relative"], ids["down_flux_relative"], ids["mean_q_given_k_relative"], kc["mean_rate_relative_gap"]) > NK_MATCH or kc["jump_density_max_abs_gap"] > 1e-12:
            out.append("NK matched quantities disagree with the target")
        if kc["min_rate"] <= 0:
            out.append("NK nonpositive rate")
        out += r.get("nk_problems", [])
    return out


# --- assembly ----------------------------------------------------------------------------

CHANNELS = (
    ("lifetime_ct", lambda b: b["episode"].get("lifetime_ct")),
    ("lifetime_jump", lambda b: b["episode"].get("lifetime_jump")),
    ("lifetime_local", lambda b: b["local"]["lifetime_local"]),
    ("omega", lambda b: b["episode"].get("omega")),
    ("departures_per_episode", lambda b: b["replacement"]["expected_distinct_departures_per_episode"]),
    ("departure_fraction", lambda b: b["replacement"]["departure_fraction_of_entry_participants"]),
    ("renewal_unconditional", lambda b: b["replacement"].get("renewal_unconditional")),
    ("renewal_conditional", lambda b: b["replacement"].get("renewal_conditional_on_feasible")),
    ("partial_renewal", lambda b: b["replacement"].get("partial_renewal_probability")),
    ("reversal_next_event", lambda b: b["flicker"].get("reversal_next_event")),
    ("reversal_next_local_event", lambda b: b["flicker"].get("reversal_next_local_event")),
    ("prevalence_ct", lambda b: b["episode"]["prevalence_ct"]),
    ("prevalence_jump", lambda b: b["episode"]["prevalence_jump"]),
    ("local_share", lambda b: b["local"]["local_share_of_events_in_A"]),
    ("local_hazard", lambda b: b["local"]["local_hazard_mean_ct"]),
)


def _view(block: dict | None, p: str) -> dict | None:
    if block is None:
        return None
    b = block["predicates"][p]
    v = {name: fn(b) for name, fn in CHANNELS}
    v["renewal_status"] = b["replacement"]["renewal_status"]
    v["feasible_entry_fraction"] = b["replacement"]["feasible_entry_fraction"]
    v["entry_set_size_distribution"] = b["replacement"]["entry_set_size_distribution"]
    return v


def predicate_row(tgt: dict, n0: dict, nd: dict | None, nk: dict | None, p: str) -> dict:
    row = {"target": _view(tgt, p), "N0": _view(n0, p), "ND": _view(nd, p), "NK": _view(nk, p)}
    t = row["target"]
    for name in ("N0", "ND", "NK"):
        c = row[name]
        if c is None:
            row[f"vs_{name}"] = None
            continue
        signs, ratios = {}, {}
        for ch, _ in CHANNELS:
            signs[ch] = gte5a._sign(t[ch], c[ch], "higher", "lower")
            ratios[ch] = t[ch] / c[ch] if t[ch] is not None and c[ch] not in (None, 0.0) else None
        row[f"vs_{name}"] = {"signs": signs, "ratios": ratios}
    return row


def frozen_checks(results: dict, sizes: tuple[int, ...] = SIZES, manifest: list[dict] | None = None) -> dict:
    checks = {}
    for it in manifest or items():
        r = results.get(it["item_id"])
        checks[it["item_id"]] = "missing" if r is None else (check_problems(r) or "pass")
    # N0 analytic control
    n0 = {}
    for n in sizes:
        r = results.get(gte5a.item_id(n, "NULL", "none"))
        if r is None:
            n0[str(n)] = "missing"
            continue
        bad = []
        for p in R.FLEXIBLE:
            b = r["target"]["predicates"][p]
            slots = 2 * n - 3 if p == "F_TRI" else n - 1
            if abs(b["local"]["lifetime_local"] - slots * b["episode"]["lifetime_ct"]) > IDENTITY * b["local"]["lifetime_local"]:
                bad.append(f"{p}: L_local != |LOCAL| L_ct")
            if r["nk_construction"].get("resolved") and (abs(np.array(r["nk_construction"]["birth"][:-1]) - 1).max() > 1e-12 or abs(np.array(r["nk_construction"]["death"][1:]) - 1).max() > 1e-12):
                bad.append("NK(NULL) is not NULL")
        n0[str(n)] = bad or "pass"
    checks["N0_analytic"] = n0
    return checks


def assemble(results: dict, sizes: tuple[int, ...] = SIZES, manifest: list[dict] | None = None) -> dict:
    rows = {}
    for it in manifest or items():
        if it["family"] == "NULL" or it["item_id"] not in results:
            continue
        r = results[it["item_id"]]
        n0 = results.get(gte5a.item_id(it["n"], "NULL", "none"))
        for p in R.FLEXIBLE:
            rows[f"{it['item_id']}:{p}"] = predicate_row(r["target"], n0["target"] if n0 else None, r.get("nd"), r.get("nk"), p)
    return {"predicate_rows": rows, "frozen_checks": frozen_checks(results, sizes, manifest)}


# --- plan, execution, publication ------------------------------------------------------------

PLAN_RELPATH = "gravity-time/plans/round-e5b-plan.json"
GENERATED_RELPATH = "gravity-time/generated/round-e5b"
TABLES_RELPATH = "gravity-time/reports/round-e5b-tables.json"
ATLAS_RELPATH = "gravity-time/reports/gt-e5b-atlas.md"
E5A_TABLES_RELPATH = "gravity-time/reports/round-e5a-tables.json"
WATCHDOG_SECONDS = {5: 900, 6: 2400}
ROUND_WALL_CAP_SECONDS = 3 * 3600
WORKERS = 4
ONTOLOGY = gte5a.ONTOLOGY
REFERENCE_FILES = (
    "research-methods/open-thetical-research.md",
    "gravity-time/provenance/prompts/GT-P010-agent-input.md",
    "gravity-time/docs/gt-p010-hub-and-e5b-audit.md",
    "gravity-time/docs/e5b-definitions-controls-and-feasibility.md",
    "gravity-time/docs/e5-definitions-and-null-construction.md",
    "gravity-time/reports/round-e5a-tables.json",
    "gravity-time/plans/round-e5a-plan.json",
    "gravity-time/docs/foundational-bridge-map.md",
    "constraint-lab/docs/scientific-plan-discipline.md",
    "constraint-lab/src/rs_constraint_lab/gtrenew.py",
    "constraint-lab/src/rs_constraint_lab/gte5b.py",
    "constraint-lab/src/rs_constraint_lab/gtpersist.py",
    "constraint-lab/tests/test_gtrenew.py",
)


def prepare_plan(repo: Path, *, source_commit: str, gt_baseline: str) -> dict:
    from rs_constraint_lab.durable import sha256_file
    from rs_constraint_lab.explore08 import plan_hash

    document = {
        "analysis_only": True,
        "analysis_version": ANALYSIS_VERSION,
        "chosen_because": "GT-P009 recommended E5B (local clock + replacement completion); authorised by GT-P010 as the only scientific round",
        "consulted_hub": {"commit": HUB_COMMIT, "ref": "origin/main", "method": "git show (read-only; no merge or cherry-pick)", "shared_questions": ["XQ::01", "XQ::04", "XQ::07", "XQ::03"], "hub_pins_at_consultation": {"CL": "e650d71bda7203c8018d8bd134c5496a03d74a11 (008N unreviewed)", "GT": "79fa6b0119449bd56359acf4436015df27855f43 (GT-P009 unreviewed)", "SC": "aa06213 catalogued only"}, "note": "a later movement of main does not re-motivate this frozen round"},
        "gt_baseline_commit": gt_baseline,
        "clocks": {"continuous": "E5A L_ct", "jump": "E5A L_jump", "local": "L_local = sum_A pi q_loc / J_A, LOCAL = slots incident on an anchor vertex (N-1 for F_STAR/F_2PATH, 2N-3 for F_TRI); a count in the same jump trajectory, not a duration"},
        "comparators": {
            "N0": "NULL item at the same N",
            "ND": "E5A T6, unchanged (gtpersist.nd_chain)",
            "NK": "p_k = target CT profile; J[k,k+1] = sum_{|x|=k} pi(x) sum_{e absent} W(x,e) (positive sums); b_k = J/((M-k)p_k), d_{k+1} = J/((k+1)p_{k+1}); analytic law p_|x|/C(M,|x|); matches p_k, every adjacent-layer flux, E[q|k], CT mean rate and JT density; not within-layer rates, local activity, correlations; zero bin or flux -> UNRESOLVED; p_k < 1e-12 flagged; nothing smoothed",
            "not_implemented": ["CL matched-source passage control (no faithful mapping: audit section 4)", "anchor-local sensitivity analysis (optional; omitted to keep the round bounded)"],
        },
        "deliberate_omissions": {"e5c": "not authorised", "n7": "not authorised", "strength_sweep": "not authorised", "new_cl_run": "not authorised", "durable_renewal_filter": "not attempted (definitions note section 3)", "trajectories": "none (exact finite-generator functionals)", "hub_writes": "none"},
        "estimands": {
            "episode": "E5A L_ct, L_jump, Omega, prevalence (both clocks) on target, ND, NK",
            "local": "L_local, local share of events in A, mean local hazard, exit local share (=1 by T9), local hazard given k",
            "entry_sets": "S0(y) = participants of the entrance state; entry-set size distribution under Palm entrance weights",
            "departures": "expected distinct departures per episode and fraction of entry participants (A-states only, before exit)",
            "renewal": "P_full_renewal unconditional and conditional on feasible entry classes; STRUCTURALLY_IMPOSSIBLE where T10 gives zero feasibility (F_STAR at N=5,6); F_STAR maximal partial renewal (N-4 originals absent)",
            "flicker": "reversal_next_event, reversal_next_local_event, reversals per episode, for eligible internal toggles",
            "layers": "p_k, adjacent fluxes, E[q|k], within-layer sd and range of q (two-pass), JT density",
        },
        "experiment_id": EXPERIMENT_ID,
        "families": {f: {g: {"components": [{"grade": cg, "kind": k} for k, cg in gte5a.components(f, g)]}} for f, g in FAMILY_GRADES},
        "frozen_checks": {
            "replication": "published E5A target prevalence, lifetimes and Omega for the three flexible predicates within max(1e-10, 1e-8 |value|)",
            "N0": "L_local = |LOCAL| L_ct within 1e-9; NK(NULL) rates all 1 within 1e-12",
            "ND": "E5A balance and calibration tolerances (1e-12, 1e-10)",
            "PCOMP": "CT law uniform within 1e-9 relative per state",
            "NK": "detailed balance <= 1e-12; global balance <= 1e-10; p_k, adjacent fluxes, E[q|k], mean rate within 1e-9 relative; JT density within 1e-12 absolute; all rates positive",
            "every_law": "flux balance <= 1e-9; entrance weights sum to J_A; L_local <= L_jump; exit local share = 1 (1e-12); relabelled anchors agree within 1e-9 relative (L_local, departures, renewal, partial renewal, flicker); hitting probabilities in [0,1] (1e-10); dense vs iterative <= 1e-9 where dense is run; unresolved solves recorded as UNRESOLVED",
            "F_STAR": "renewal status STRUCTURALLY_IMPOSSIBLE at N=5 and N=6",
            "E5A_lag_channels": "not part of E5B; the two numerically qualified E5A CT hub-lag channels are not reclassified",
        },
        "history": False,
        "hypotheses_without_prediction": ["H1 genuine replacement-supported organisation", "H2 kinetic heterogeneity", "H3 prevalence/density composition", "H4 flicker", "H5 remote-event clock", "H6 null or mixed", "H7 surprising structure"],
        "items": items(),
        "meta_constraints": False,
        "method": {"name": "Open-Thetical Research", "path": "research-methods/open-thetical-research.md", "version": "1.0"},
        "new_primitives": False,
        "ontology": ONTOLOGY,
        "parameter_fit": False,
        "predicate_ids": predicate_ids(),
        "predicates": {"F_TRI": "anchor edge {0,1} present and >=1 completer; participants = completers", "F_STAR": "deg(0) >= 3; participants = neighbours of 0", "F_2PATH": "deg(0) >= 2; participants = neighbours of 0", "relabelled": "image under v -> N-1-v", "anchors": "analyst-fixed labels, not a mobile or unlabelled reference"},
        "pre_freeze_exposure": {
            "published": "E5A target, N0 and ND values for the same laws and predicates (prevalence, lifetimes, Omega, rho, JT densities, lagged hub)",
            "engineering": "proof fixtures on synthetic chains, N<=4 kernels and a synthetic N=5 neighbourhood rule; timing only on published NULL N=6 (about 9 s per law per anchor set); no E5B observable of any N=5 or N=6 scientific cell computed before freezing",
            "reference_hashes": {rel: sha256_file(repo / rel) for rel in REFERENCE_FILES},
        },
        "programme": "GT",
        "prompt_id": PROMPT_ID,
        "question": "In the same FREE relational laws, does a labelled anchored organisation persist through meaningful replacement of its participants, beyond what is accounted for by density, aggregate and density-resolved kinetics, activity at its own anchor, and immediate reversals?",
        "round_id": ROUND_ID,
        "rule_reading": "no rule reads an anchor, entry set, participant, renewal state or history; all are analysis-defined observers",
        "schema": "rs-gt.e5b-plan/v1",
        "software": {"analysis_module": "rs_constraint_lab.gte5b", "kernel": gtkernel.KERNEL_VERSION, "numpy": np.__version__, "observables": gtobs.OBSERVABLES_VERSION, "persistence": P.PERSIST_VERSION, "renewal": R.RENEW_VERSION, "python": __import__("platform").python_version(), "scipy": "not used"},
        "solver": {"method": "BiCGSTAB on the killed jump chain (gtpersist.bicgstab)", "tolerance": R.HIT_TOLERANCE, "cap_iterations": R.HIT_CAP, "cap_seconds": R.HIT_SECONDS, "dense_cross_check_max_size": R.DENSE_LIMIT, "canonical_frames": "one canonical entry set per size; entry states mapped by permutations fixing the anchor (definitions note section 5)"},
        "source_commit": source_commit,
        "stochastic_trajectories": "none",
        "stop_conditions": {"item": f"watchdog {WATCHDOG_SECONDS} s by N", "round": f"all items or {ROUND_WALL_CAP_SECONDS} s", "unresolved": "recorded as UNRESOLVED; no retuning, no substitute statistic, no changed tolerance", "amendment": "any cell, predicate, comparator or estimand change stops the round", "after_round": "no E5C"},
        "tolerances": {"identity": IDENTITY, "tie_relative": P.TIE_RELATIVE, "replication": [REPLICATION_ABS, REPLICATION_REL], "nk_match": NK_MATCH, "rare_mass": P.RARE_MASS, "hit": [R.HIT_TOLERANCE, R.HIT_CAP, R.HIT_SECONDS]},
        "work_count": {"items": 12, "kernels": 12, "predicate_analyses": len(predicate_ids()), "laws_per_item": "target, ND, NK; primary and relabelled anchors", "largest_state_space": 32768, "memory_ceiling_per_worker_bytes": 2_000_000_000, "round_wall_cap_seconds": ROUND_WALL_CAP_SECONDS, "watchdog_seconds": {str(k): v for k, v in WATCHDOG_SECONDS.items()}, "workers": WORKERS, "estimate_note": "about 1-2 min per N=6 item from the NULL timing (6 law-anchor sets x ~9 s), longer for slow-mixing laws; well under the 3 h cap expected, not promised"},
    }
    document["plan_hash"] = plan_hash(document)
    return document


def require_execution(repo: Path, commit: str | None, *, require_remote: bool = True) -> dict:
    from rs_constraint_lab.explore08 import FrozenPlanError, remote_contains, require_frozen_plan

    plan = require_frozen_plan(repo, commit, PLAN_RELPATH, disk_path=repo / PLAN_RELPATH)
    if require_remote and not remote_contains(repo, commit or ""):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    if plan.get("items") != items() or plan.get("new_primitives") is not False or plan.get("ontology") != ONTOLOGY or plan.get("consulted_hub", {}).get("commit") != HUB_COMMIT:
        raise FrozenPlanError("execution refused: E5B plan contract drifted")
    return plan


def execute_item(root: Path, item: dict) -> dict:
    import resource

    from rs_constraint_lab.durable import atomic_write_json, read_json

    started = time.perf_counter()
    repo = Path(__file__).resolve().parents[3]
    pub = read_json(repo / E5A_TABLES_RELPATH)["predicates"].get(item["item_id"]) if (repo / E5A_TABLES_RELPATH).is_file() else None

    def payload(result, status):
        return {"item": item, "item_id": item["item_id"], "peak_rss_mb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, "result": result, "status": status, "wall_seconds": time.perf_counter() - started}

    def on_main(result):
        atomic_write_json(root / "items" / f"{item['item_id']}.partial.json", payload(result, "complete_checks_interrupted"))

    result = analyse_item(item, on_main=on_main, published=pub)
    atomic_write_json(root / "items" / f"{item['item_id']}.json", payload(result, "complete"))
    partial = root / "items" / f"{item['item_id']}.partial.json"
    if partial.exists():
        partial.unlink()
    return {}


def run(root: Path, plan: dict, *, workers: int = WORKERS, **kwargs) -> list[dict]:
    return gte1.run(root, plan, workers=workers, watchdogs=kwargs.pop("watchdogs", WATCHDOG_SECONDS), wall_cap=kwargs.pop("wall_cap", ROUND_WALL_CAP_SECONDS), module=kwargs.pop("module", "rs_constraint_lab.gte5b"), **kwargs)


def publish(root: Path, plan: dict, out: Path, *, frozen_plan_commit: str) -> str:
    from rs_constraint_lab.durable import atomic_write_json, canonical_json, read_json, sha256_bytes

    records = {}
    for it in plan["items"]:
        path = root / "items" / f"{it['item_id']}.json"
        records[it["item_id"]] = read_json(path) if path.is_file() else {"item_id": it["item_id"], "status": "missing"}
    results = {k: v["result"] for k, v in records.items() if "result" in v}
    assembled = assemble(results)
    item_records = {k: {"numerical_problems": check_problems(results[k]) if k in results else None, "peak_rss_mb": v.get("peak_rss_mb"), "role": next(it["role"] for it in plan["items"] if it["item_id"] == k), "status": v["status"], "wall_seconds": v.get("wall_seconds"), **({"interruption": v["interruption"]} if "interruption" in v else {})} for k, v in records.items()}
    payload = {"analysis_version": ANALYSIS_VERSION, "consulted_hub": HUB_COMMIT, "experiment_id": EXPERIMENT_ID, "frozen_analysis_plan_commit": frozen_plan_commit, "item_records": item_records, "plan_hash": plan["plan_hash"], "results": results, "round_id": ROUND_ID, "schema": "rs-gt.e5b-tables/v1", "source_commit": plan.get("source_commit"), "status_counts": {s: sum(r["status"] == s for r in item_records.values()) for s in sorted({r["status"] for r in item_records.values()})}, **assembled}
    body = dict(payload)
    body["payload_sha256"] = sha256_bytes(canonical_json(payload).encode("utf-8"))
    atomic_write_json(out, body)
    return body["payload_sha256"]


def _f(v, d: int = 3) -> str:
    if v is None:
        return "—"
    if isinstance(v, str):
        return v
    if v == 0:
        return "0"
    if abs(v) >= 1e4 or abs(v) < 1e-3:
        return f"{v:.{d}e}"
    return f"{v:.{d + 1}g}"


def render_atlas(repo: Path, tables: Path | None = None) -> str:
    from rs_constraint_lab.durable import read_json

    t = read_json(tables or repo / TABLES_RELPATH)
    L = ["# GT-E5B atlas: replacement, local counts and the NK comparator", "", f"*Frozen plan `{t['frozen_analysis_plan_commit'][:7]}` (plan_hash `{t['plan_hash'][:12]}…`); payload `{t['payload_sha256'][:12]}…`; consulted hub `{t['consulted_hub'][:7]}`. Exact finite-generator values; NaN-free; ties use relative 1e-9.*", ""]
    L += ["## Item status", "", "| Item | Status | Wall s | Problems |", "| --- | --- | ---: | --- |"]
    for k, v in t["item_records"].items():
        L.append(f"| {k} | {v['status']} | {_f(v.get('wall_seconds'), 1)} | {'; '.join(v.get('numerical_problems') or []) or 'none'} |")
    L += ["", "## Frozen checks", ""] + [f"- `{k}`: {v if isinstance(v, str) else v}" for k, v in t["frozen_checks"].items()]
    keys = ("lifetime_ct", "lifetime_jump", "lifetime_local", "departure_fraction", "renewal_unconditional", "renewal_conditional", "partial_renewal", "reversal_next_event", "prevalence_ct")
    for rid, row in t["predicate_rows"].items():
        L += ["", f"## {rid}", "", f"Renewal status: {row['target']['renewal_status']}; feasible entry fraction {_f(row['target']['feasible_entry_fraction'])}; entry-set sizes {row['target']['entry_set_size_distribution']}.", "", "| Channel | target | N0 | ND | NK | vs N0 | vs ND | vs NK |", "| --- | ---: | ---: | ---: | ---: | --- | --- | --- |"]
        for ch in keys:
            vals = [row[c][ch] if row[c] else None for c in ("target", "N0", "ND", "NK")]
            signs = [(row[f"vs_{c}"]["signs"][ch] + (f" ×{_f(row[f'vs_{c}']['ratios'][ch])}" if row[f"vs_{c}"]["ratios"][ch] is not None else "")) if row[f"vs_{c}"] else "—" for c in ("N0", "ND", "NK")]
            L.append(f"| {ch} | " + " | ".join(_f(v) for v in vals) + " | " + " | ".join(signs) + " |")
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m rs_constraint_lab.gte5b")
    sub = parser.add_subparsers(dest="command", required=True)
    one = sub.add_parser("item")
    one.add_argument("--root", required=True)
    one.add_argument("--item-id", required=True)
    pl = sub.add_parser("plan")
    pl.add_argument("--source-commit", required=True)
    pl.add_argument("--gt-baseline", required=True)
    ex = sub.add_parser("run")
    ex.add_argument("--commit", required=True)
    pb = sub.add_parser("publish")
    pb.add_argument("--commit", required=True)
    sub.add_parser("atlas")
    args = parser.parse_args(argv)
    from rs_constraint_lab.durable import atomic_write_json, read_json

    repo = Path(__file__).resolve().parents[3]
    if args.command == "plan":
        plan = prepare_plan(repo, source_commit=args.source_commit, gt_baseline=args.gt_baseline)
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
        digest = publish(repo / GENERATED_RELPATH, plan, repo / TABLES_RELPATH, frozen_plan_commit=args.commit)
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
        raise SystemExit("item is not in the E5B manifest")
    execute_item(root, item)
    return 0


if __name__ == "__main__":
    sys.exit(main())
