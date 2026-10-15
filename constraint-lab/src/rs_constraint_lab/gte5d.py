"""GT round E5D: durable renewal against the anchor-local traffic comparator NL (GT-P012).

The same twelve FREE kernels. Matrix: F_TRI({0,1}) on all 12 laws; F_2PATH(0) on the six N=6
laws (N=5 F_2PATH is structurally zero after renewal, T14). For each analysis and each anchor
(primary and relabelled): E5C durability (R0, U_h, C_h at h = 0,1,2,4,8, return/exit,
immediate return, entry-size classes) on the target, ND (E5A), NK (E5B) and NL (E5D, built on
that anchor's LOCAL/REMOTE partition), each with its own entrance and first-renewal law. Target,
ND and NK replicate the published E5C values. Diagnostics: the target's macro-flux conservation,
projected net currents on the (l, r) grid, rare cells, and within-cell local-rate dispersion.
Definitions: ``gravity-time/docs/e5d-local-traffic-comparator.md``.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np

from rs_constraint_lab import gte1, gte5a, gte5b, gte5c, gtkernel, gtobs
from rs_constraint_lab import gtdurable as D
from rs_constraint_lab import gtlocalcontrol as NLm
from rs_constraint_lab import gtpersist as P
from rs_constraint_lab import gtrenew as RN
from rs_constraint_lab.state import edges

ROUND_ID = "round-e5d"
EXPERIMENT_ID = "gt-round-e5d-anchor-local-traffic"
ANALYSIS_VERSION = "gt-e5d/v1"
PROMPT_ID = "GT-P012"
MODE = "FREE"
FAMILY_GRADES = gte5a.FAMILY_GRADES
SIZES = (5, 6)
IDENTITY = 1e-9
REPLICATION_ABS = 1e-10
REPLICATION_REL = 1e-8
NL_MATCH = 1e-9
HUB_COMMIT = "38c2501bbab22ca1eb2288ea76a962ac0170d5e6"
LAWS = ("target", "nd", "nk", "nl")


def items() -> list[dict]:
    return [{**it, "prior_cell": f"round-e5c {it['item_id']}"} for it in gte5a.items()]


def predicates_for(n: int) -> tuple[str, ...]:
    return ("F_TRI", "F_2PATH") if n == 6 else ("F_TRI",)


def predicate_ids() -> list[str]:
    return [f"{it['item_id']}:{p}" for it in items() for p in predicates_for(it["n"])]


def anchors(p: str, n: int) -> dict:
    return {"predicates": P.primary_instance(p), "relabelled": P.relabelled_instance(p, n)}


# --- checks --------------------------------------------------------------------------------------


def durable_problems(block: dict, label: str, preds: tuple[str, ...]) -> list[str]:
    out = []
    for key in ("predicates", "relabelled"):
        for p in preds:
            d = block[key][p]
            out += [f"{label}/{key}/{p}: {u} UNRESOLVED" for u in d.get("unresolved", [])]
            if d.get("status") == "STRUCTURALLY_IMPOSSIBLE":
                continue
            U = [d["U"][str(h)] for h in D.HORIZONS]
            if any(a < b - 1e-15 for a, b in zip(U, U[1:])):
                out.append(f"{label}/{key}/{p}: U_h not monotone")
            for s, c in d["classes"].items():
                if c.get("status") != "computed":
                    continue
                if c["remote_closure_violations"] != 0:
                    out.append(f"{label}/{key}/{p}/s{s}: T13 violated")
                if abs(c["return_before_exit"] + c["exit_before_return"] - 1.0) > IDENTITY or abs(c["first_local_split_sum"] - 1.0) > IDENTITY:
                    out.append(f"{label}/{key}/{p}/s{s}: leave-R causes do not sum to 1")
                for name, sv in c["solves"].items():
                    if sv.get("dense_max_abs_difference") is not None and sv["dense_max_abs_difference"] > IDENTITY:
                        out.append(f"{label}/{key}/{p}/s{s}: {name} dense and iterative disagree")
    for p in preds:
        a, b = block["predicates"][p], block["relabelled"][p]
        if a.get("status") != b.get("status"):
            out.append(f"{label}/{p}: relabelled status differs")
            continue
        if a.get("status") == "STRUCTURALLY_IMPOSSIBLE":
            continue
        for h in D.HORIZONS:
            x, y = a["U"][str(h)], b["U"][str(h)]
            if abs(x - y) > IDENTITY * max(abs(x), abs(y), 1e-300) and abs(x - y) > 1e-15:
                out.append(f"{label}/{p}: relabelled anchor disagrees at h={h}")
    return out


def replication_problems(block: dict, published: dict | None, label: str, preds: tuple[str, ...]) -> list[str]:
    if published is None:
        return [f"{label}: E5C replication not checked"]
    out = []
    for p in preds:
        new, old = block["predicates"][p], published[p]
        if new.get("status") != old.get("status"):
            out.append(f"{label}/{p}: status differs from E5C")
            continue
        if new.get("status") == "STRUCTURALLY_IMPOSSIBLE":
            continue
        for h in D.HORIZONS:
            a, b = new["U"][str(h)], old["U"][str(h)]
            if abs(a - b) > max(REPLICATION_ABS, REPLICATION_REL * abs(b)):
                out.append(f"{label}/{p}: U_{h} does not replicate E5C")
    return out


# --- per-item analysis ----------------------------------------------------------------------------


def analyse_item(item: dict, *, on_main=None, published: dict | None = None) -> dict:
    n = item["n"]
    m = len(edges(n))
    preds = predicates_for(n) if n in SIZES else ("F_TRI", "F_2PATH")
    comps = [tuple(c) for c in item["components"]]
    timings: dict[str, float] = {}
    t0 = time.perf_counter()
    chain, _ = gtkernel.reachable_chain(n, MODE, comps)
    result: dict = {"analysis_version": ANALYSIS_VERSION, "item_id": item["item_id"], "kernel_version": gtkernel.KERNEL_VERSION, "durable_version": D.DURABLE_VERSION, "localcontrol_version": NLm.LOCALCONTROL_VERSION, "predicates_in_matrix": list(preds)}
    result["ergodicity"] = {"all_rates_positive": bool((chain.W > 0).all()), "full_space": bool(len(chain.states) == 1 << m)}
    stat = gtobs.stationary(chain, 0)
    timings["build_stationary"] = time.perf_counter() - t0
    result["stationary"] = {k: v for k, v in stat.items() if k not in ("ct", "jump")}
    if not stat["resolved"]:
        result["status_note"] = "target stationary law unresolved"
        return result
    ct = stat["ct"]
    laws = {"target": (chain, ct)}
    p_k = P.density_profile(chain.states, ct, m)
    if P.nd_rates(p_k)["resolved"]:
        nd, pi_nd, _ = P.nd_chain(n, p_k, float(ct @ chain.rates))
        laws["nd"] = (nd, pi_nd)
    lf = RN.layer_fluxes(chain, ct, n)
    if RN.nk_rates(lf["p"], lf["up"])["resolved"]:
        nk, pi_nk, _ = RN.nk_chain(n, lf["p"], lf["up"])
        laws["nk"] = (nk, pi_nk)
    for name, (ch, lw) in laws.items():
        t0 = time.perf_counter()
        block = {"predicates": {}, "relabelled": {}}
        for p in preds:
            for key, inst in anchors(p, n).items():
                block[key][p] = D.durable(ch, lw, n, p, inst)
        result[name] = block
        result[f"{name}_problems"] = durable_problems(block, name, preds)
        if published is not None:
            result[f"{name}_problems"] += replication_problems(block, published.get(name), name, preds)
        elif n in SIZES:
            result[f"{name}_problems"].append(f"{name}: E5C replication not checked")
        timings[name] = time.perf_counter() - t0
    # NL per predicate and anchor
    t0 = time.perf_counter()
    nlb = {"predicates": {}, "relabelled": {}}
    nl_info = {"predicates": {}, "relabelled": {}}
    target_macro = {"predicates": {}, "relabelled": {}}
    for p in preds:
        for key, inst in anchors(p, n).items():
            local = RN.local_mask(n, p, inst)
            mf = NLm.macro_fluxes(chain, ct, n, local)
            diag = NLm.macro_diagnostics(mf)
            target_macro[key][p] = {**diag, "within_cell_local_rate_sd_max": float(mf["local_rate_sd"].max()), "within_cell_local_rate_cv_max": float(np.max(np.divide(mf["local_rate_sd"], mf["local_rate_mean"], out=np.zeros_like(mf["p"]), where=mf["local_rate_mean"] > 0)))}
            if not NLm.nl_rates(mf)["resolved"]:
                nl_info[key][p] = {"resolved": False, "reason": NLm.nl_rates(mf)["reason"]}
                nlb[key][p] = {"status": "UNRESOLVED", "unresolved": ["NL construction"], "U": {}, "C": {}, "classes": {}}
                continue
            nl, pi_nl, info = NLm.nl_chain(n, local, mf)
            cross = gtkernel.stationary_sparse(nl, cap=20_000)
            info["iterative_cross_check"] = {"resolved": bool(cross["resolved"]), "l1_vs_analytic": float(np.abs(cross["ct"] - pi_nl).sum()) if cross["resolved"] else None}
            info["resolved"] = True
            nl_info[key][p] = info
            nlb[key][p] = D.durable(nl, pi_nl, n, p, inst)
    result["nl"] = nlb
    result["nl_construction"] = nl_info
    result["target_macro"] = target_macro
    result["nl_problems"] = durable_problems(nlb, "nl", preds) if all(nlb[k][p].get("status") != "UNRESOLVED" for k in nlb for p in preds) else ["NL UNRESOLVED"]
    timings["nl"] = time.perf_counter() - t0
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
    for name in LAWS:
        if name not in r:
            out.append(f"{name.upper()} UNRESOLVED")
            continue
        out += r.get(f"{name}_problems", [])
    for key, per in r.get("nl_construction", {}).items():
        for p, info in per.items():
            if not info.get("resolved"):
                out.append(f"NL {key}/{p}: {info.get('reason')}")
                continue
            if info["global_balance_relative"] > 1e-10:
                out.append(f"NL {key}/{p}: global balance")
            if max(info["identities"].values()) > NL_MATCH:
                out.append(f"NL {key}/{p}: p or ordered macro flux not matched")
            if info["min_rate"] <= 0:
                out.append(f"NL {key}/{p}: nonpositive rate")
            ic = info.get("iterative_cross_check", {})
            if ic.get("resolved") and ic["l1_vs_analytic"] > 1e-8:
                out.append(f"NL {key}/{p}: analytic law disagrees with iterative solve")
    for key, per in r.get("target_macro", {}).items():
        for p, dg in per.items():
            if dg["conservation_max_relative"] > IDENTITY:
                out.append(f"target macro {key}/{p}: flux conservation fails")
    return out


# --- assembly -------------------------------------------------------------------------------------


def _view(block, p):
    if block is None:
        return None
    return gte5c._view(block, p)


def predicate_row(tgt, n0, nd, nk, nl, p) -> dict:
    row = {"target": _view(tgt, p), "N0": _view(n0, p), "ND": _view(nd, p), "NK": _view(nk, p), "NL": _view(nl, p)}
    t = row["target"]
    keys = ["R0"] + [f"U{h}" for h in D.HORIZONS] + [f"C{h}" for h in D.HORIZONS]
    for name in ("N0", "ND", "NK", "NL"):
        c = row[name]
        if c is None or t["status"] == "STRUCTURALLY_IMPOSSIBLE" or c.get("status") == "UNRESOLVED":
            row[f"vs_{name}"] = None
            continue
        signs, ratios = {}, {}
        for k in keys:
            signs[k], ratios[k] = gte5c._cmp(t[k], c[k])
        row[f"vs_{name}"] = {"signs": signs, "ratios": ratios}
    return row


def frozen_checks(results: dict, sizes=SIZES, manifest=None) -> dict:
    checks = {}
    for it in manifest or items():
        r = results.get(it["item_id"])
        checks[it["item_id"]] = "missing" if r is None else (check_problems(r) or "pass")
    nulls = {}
    for n in sizes:
        r = results.get(gte5a.item_id(n, "NULL", "none"))
        if r is None:
            nulls[str(n)] = "missing"
            continue
        bad = []
        for p in r["predicates_in_matrix"]:
            vals = [r[law]["predicates"][p] for law in LAWS if law in r]
            if vals[0].get("status") == "STRUCTURALLY_IMPOSSIBLE":
                continue
            for h in D.HORIZONS:
                xs = [v["U"][str(h)] for v in vals]
                if max(xs) - min(xs) > 1e-10 * max(max(xs), 1e-300) and max(xs) - min(xs) > 1e-15:
                    bad.append(f"{p}: N0/ND/NK/NL differ at h={h}")
        nulls[str(n)] = bad or "pass"
    checks["NULL_fixed_point"] = nulls
    return checks


def assemble(results: dict, sizes=SIZES, manifest=None) -> dict:
    rows = {}
    for it in manifest or items():
        if it["family"] == "NULL" or it["item_id"] not in results:
            continue
        r = results[it["item_id"]]
        n0 = results.get(gte5a.item_id(it["n"], "NULL", "none"))
        for p in r["predicates_in_matrix"]:
            rows[f"{it['item_id']}:{p}"] = predicate_row(r["target"], n0["target"] if n0 else None, r.get("nd"), r.get("nk"), r.get("nl"), p)
            rows[f"{it['item_id']}:{p}"]["target_macro"] = r["target_macro"]["predicates"][p]
            rows[f"{it['item_id']}:{p}"]["nl_reversible"] = r["nl_construction"]["predicates"][p].get("reversible")
    return {"predicate_rows": rows, "frozen_checks": frozen_checks(results, sizes, manifest)}


# --- plan, execution, publication -----------------------------------------------------------------

PLAN_RELPATH = "gravity-time/plans/round-e5d-plan.json"
GENERATED_RELPATH = "gravity-time/generated/round-e5d"
TABLES_RELPATH = "gravity-time/reports/round-e5d-tables.json"
ATLAS_RELPATH = "gravity-time/reports/gt-e5d-atlas.md"
E5C_TABLES_RELPATH = "gravity-time/reports/round-e5c-tables.json"
WATCHDOG_SECONDS = {5: 900, 6: 2400}
ROUND_WALL_CAP_SECONDS = 3 * 3600
WORKERS = 4
ONTOLOGY = gte5a.ONTOLOGY
REFERENCE_FILES = (
    "research-methods/open-thetical-research.md",
    "gravity-time/provenance/prompts/GT-P012-agent-input.md",
    "gravity-time/docs/gt-p012-starting-audit.md",
    "gravity-time/docs/e5d-local-traffic-comparator.md",
    "gravity-time/docs/e5c-durable-renewal-definitions.md",
    "gravity-time/docs/e5b-definitions-controls-and-feasibility.md",
    "gravity-time/reports/round-e5c-tables.json",
    "gravity-time/plans/round-e5c-plan.json",
    "constraint-lab/docs/scientific-plan-discipline.md",
    "constraint-lab/src/rs_constraint_lab/gtlocalcontrol.py",
    "constraint-lab/src/rs_constraint_lab/gte5d.py",
    "constraint-lab/src/rs_constraint_lab/gtdurable.py",
    "constraint-lab/src/rs_constraint_lab/gtrenew.py",
    "constraint-lab/tests/test_gtlocalcontrol.py",
)


def prepare_plan(repo: Path, *, source_commit: str, gt_baseline: str) -> dict:
    from rs_constraint_lab.durable import sha256_file
    from rs_constraint_lab.explore08 import plan_hash

    document = {
        "analysis_only": True,
        "analysis_version": ANALYSIS_VERSION,
        "chosen_because": "GT-P011 reflection option A (anchor-local comparator; GT-Q25), authorised by GT-P012 as the only scientific round",
        "consulted_hub": {"commit": HUB_COMMIT, "ref": "origin/main", "method": "git show (read-only)", "shared_questions": ["XQ::01", "XQ::03", "XQ::04", "XQ::07"]},
        "gt_baseline_commit": gt_baseline,
        "comparators": {
            "N0": "NULL item at the same N", "ND": "E5A T6 unchanged", "NK": "E5B T11 unchanged",
            "NL": "anchor-relative local/remote traffic lift: LOCAL = slots incident on an anchor vertex (F_TRI: 0 or 1, 2N-3 slots; F_2PATH: vertex 0, N-1 slots), REMOTE = the rest; z = (l, r) present counts; p_z and ORDERED macro fluxes J_{z->z'} from the target's stationary generator (positive sums); per-slot rates J/(p_z x eligible slots) by pool and direction; no symmetrisation; analytic law p_z / (C(L,l) C(R,r)) (T16); built separately for the primary and relabelled anchors; zero cell or zero admissible flux -> UNRESOLVED; nothing smoothed",
            "not_implemented": ["source-standardised diagnostics (not defined)", "within-cell arrangement control (a future round)"],
        },
        "matrix": {"F_TRI": "all 12 laws (N=5,6)", "F_2PATH": "the six N=6 laws only (N=5 structurally zero after renewal, T14)", "analyses": len(predicate_ids())},
        "estimands": {"durability": "E5C objects unchanged (R0, U_h, C_h at h = 0,1,2,4,8, return/exit, immediate return, entry-size classes, size>=2 pooled) on target, N0, ND, NK and NL, each with its own entrance and first-renewal law", "diagnostics": "target macro-flux conservation; net currents on the (l,r) grid (max relative, abs sum over total flux); rare and zero cells; within-cell local-rate sd and CV; NL reversibility (detailed balance), min/max rate, identity gaps, iterative cross-check"},
        "horizons": list(D.HORIZONS),
        "experiment_id": EXPERIMENT_ID,
        "families": {f: {g: {"components": [{"grade": cg, "kind": k} for k, cg in gte5a.components(f, g)]}} for f, g in FAMILY_GRADES},
        "frozen_checks": {
            "replication": "target, ND and NK U_h equal the published E5C values within max(1e-10, 1e-8 |value|) (statuses equal)",
            "NL": "global balance of pi_NL <= 1e-10; p_z and every ordered macro flux matched within 1e-9 relative; all rates positive; analytic law vs iterative solve (cap 20,000) L1 <= 1e-8 when the iterative solve resolves",
            "target_macro": "macro-flux conservation within 1e-9 (premise of T16)",
            "durability": "E5C checks: monotone U_h; T13 zero violations; return + exit = 1; next-local split sums to 1 (1e-9); dense vs iterative <= 1e-9; relabelled anchors agree within 1e-9 relative",
            "NULL": "target, ND, NK and NL identical on NULL items (1e-10)",
        },
        "history": False,
        "hypotheses_without_prediction": ["D1 structural residual beyond NL", "D2 anchor-relative traffic (residual collapses against NL)", "D3 within-cell configuration", "D4 flicker/entry composition", "D5 null or sign reversal", "D6 projection circulation"],
        "items": items(),
        "meta_constraints": False,
        "method": {"name": "Open-Thetical Research", "path": "research-methods/open-thetical-research.md", "version": "1.0"},
        "new_primitives": False,
        "ontology": ONTOLOGY,
        "parameter_fit": False,
        "predicate_ids": predicate_ids(),
        "pre_freeze_exposure": {
            "published": "E5A-E5C values for the same laws (E5C durability for target/ND/NK, which E5D replicates)",
            "engineering": "NL fixtures on N<=4 kernels and synthetic N=4 chains (including a non-reversible circulating chain); timing on a synthetic N=6 rule only; no NL value or new E5D readout of any N=5 or N=6 scientific cell computed before freezing",
            "reference_hashes": {rel: sha256_file(repo / rel) for rel in REFERENCE_FILES},
        },
        "programme": "GT",
        "prompt_id": PROMPT_ID,
        "question": "Are the residual PATHH triangle and PCOMP within-entry-class durability effects explained by where transition traffic is situated around the analyst's anchor (local versus remote edge counts), or do residual organisation-sensitive properties remain after that is controlled?",
        "round_id": ROUND_ID,
        "rule_reading": "no rule reads an anchor, S0, renewal state, local count or pool partition; NL is a comparison process, not a constraint family",
        "schema": "rs-gt.e5d-plan/v1",
        "software": {"analysis_module": "rs_constraint_lab.gte5d", "localcontrol": NLm.LOCALCONTROL_VERSION, "durable": D.DURABLE_VERSION, "kernel": gtkernel.KERNEL_VERSION, "numpy": np.__version__, "python": __import__("platform").python_version(), "scipy": "not used"},
        "solver": {"method": "E5C row solves in canonical frames (gtdurable)", "tolerance": D.SOLVE_TOLERANCE, "cap_iterations": D.SOLVE_CAP, "cap_seconds": D.SOLVE_SECONDS, "dense_cross_check_max_size": D.DENSE_LIMIT},
        "source_commit": source_commit,
        "stochastic_trajectories": "none",
        "stop_conditions": {"item": f"watchdog {WATCHDOG_SECONDS} s by N", "round": f"all items or {ROUND_WALL_CAP_SECONDS} s", "unresolved": "recorded as UNRESOLVED or FAILED_FROZEN_CHECK; no retuning", "amendment": "any cell, predicate, horizon, comparator or estimand change stops the round", "after_round": "no E5E"},
        "tolerances": {"identity": IDENTITY, "tie_relative": P.TIE_RELATIVE, "replication": [REPLICATION_ABS, REPLICATION_REL], "nl_match": NL_MATCH, "rare_mass": P.RARE_MASS},
        "work_count": {"items": 12, "analyses": len(predicate_ids()), "laws_per_analysis": "target, ND, NK, NL (NL per anchor); primary and relabelled anchors", "largest_state_space": 32768, "memory_ceiling_per_worker_bytes": 2_000_000_000, "round_wall_cap_seconds": ROUND_WALL_CAP_SECONDS, "watchdog_seconds": {str(k): v for k, v in WATCHDOG_SECONDS.items()}, "workers": WORKERS, "estimate_note": "about 2 min per N=6 item from synthetic timing; under 30 min in total expected, not promised"},
    }
    document["plan_hash"] = plan_hash(document)
    return document


def require_execution(repo: Path, commit: str | None, *, require_remote: bool = True) -> dict:
    from rs_constraint_lab.explore08 import FrozenPlanError, remote_contains, require_frozen_plan

    plan = require_frozen_plan(repo, commit, PLAN_RELPATH, disk_path=repo / PLAN_RELPATH)
    if require_remote and not remote_contains(repo, commit or ""):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    if plan.get("items") != items() or plan.get("new_primitives") is not False or plan.get("ontology") != ONTOLOGY or plan.get("consulted_hub", {}).get("commit") != HUB_COMMIT or plan.get("horizons") != list(D.HORIZONS) or plan.get("predicate_ids") != predicate_ids():
        raise FrozenPlanError("execution refused: E5D plan contract drifted")
    return plan


def execute_item(root: Path, item: dict) -> dict:
    import resource

    from rs_constraint_lab.durable import atomic_write_json, read_json

    started = time.perf_counter()
    repo = Path(__file__).resolve().parents[3]
    pub = None
    if (repo / E5C_TABLES_RELPATH).is_file():
        r5c = read_json(repo / E5C_TABLES_RELPATH)["results"].get(item["item_id"])
        if r5c:
            pub = {law: r5c[law]["predicates"] for law in ("target", "nd", "nk") if law in r5c}

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
    return gte1.run(root, plan, workers=workers, watchdogs=kwargs.pop("watchdogs", WATCHDOG_SECONDS), wall_cap=kwargs.pop("wall_cap", ROUND_WALL_CAP_SECONDS), module=kwargs.pop("module", "rs_constraint_lab.gte5d"), **kwargs)


def publish(root: Path, plan: dict, out: Path, *, frozen_plan_commit: str) -> str:
    from rs_constraint_lab.durable import atomic_write_json, canonical_json, read_json, sha256_bytes

    records = {}
    for it in plan["items"]:
        path = root / "items" / f"{it['item_id']}.json"
        records[it["item_id"]] = read_json(path) if path.is_file() else {"item_id": it["item_id"], "status": "missing"}
    results = {k: v["result"] for k, v in records.items() if "result" in v}
    assembled = assemble(results)
    item_records = {k: {"numerical_problems": check_problems(results[k]) if k in results else None, "peak_rss_mb": v.get("peak_rss_mb"), "status": v["status"], "wall_seconds": v.get("wall_seconds")} for k, v in records.items()}
    payload = {"analysis_version": ANALYSIS_VERSION, "consulted_hub": HUB_COMMIT, "experiment_id": EXPERIMENT_ID, "frozen_analysis_plan_commit": frozen_plan_commit, "item_records": item_records, "plan_hash": plan["plan_hash"], "results": results, "round_id": ROUND_ID, "schema": "rs-gt.e5d-tables/v1", "source_commit": plan.get("source_commit"), "status_counts": {s: sum(r["status"] == s for r in item_records.values()) for s in sorted({r["status"] for r in item_records.values()})}, **assembled}
    body = dict(payload)
    body["payload_sha256"] = sha256_bytes(canonical_json(payload).encode("utf-8"))
    atomic_write_json(out, body)
    return body["payload_sha256"]


def render_atlas(repo: Path, tables: Path | None = None) -> str:
    from rs_constraint_lab.durable import read_json

    f = gte5b._f
    t = read_json(tables or repo / TABLES_RELPATH)
    L = ["# GT-E5D atlas: durable renewal against the anchor-local traffic comparator NL", "", f"*Frozen plan `{t['frozen_analysis_plan_commit'][:7]}` (plan_hash `{t['plan_hash'][:12]}…`); payload `{t['payload_sha256'][:12]}…`; consulted hub `{t['consulted_hub'][:7]}`. Exact finite-generator values; ties relative 1e-9.*", ""]
    L += ["## Item status", "", "| Item | Status | Wall s | Problems |", "| --- | --- | ---: | --- |"]
    for k, v in t["item_records"].items():
        L.append(f"| {k} | {v['status']} | {f(v.get('wall_seconds'), 1)} | {'; '.join(v.get('numerical_problems') or []) or 'none'} |")
    L += ["", "## Frozen checks", ""] + [f"- `{k}`: {v}" for k, v in t["frozen_checks"].items()]
    for rid, row in t["predicate_rows"].items():
        tg, mac = row["target"], row["target_macro"]
        L += ["", f"## {rid}", "", f"Status {tg['status']}; target macro net current (max relative) {f(mac['net_current_max_relative'])}; NL reversible: {row['nl_reversible']}; within-cell local-rate CV max {f(mac['within_cell_local_rate_cv_max'])}."]
        if tg["status"] == "STRUCTURALLY_IMPOSSIBLE":
            continue
        L += ["", "| Quantity | target | N0 | ND | NK | NL | vs NK | vs NL |", "| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |"]
        for k in ["R0"] + [f"U{h}" for h in (1, 2, 4, 8)] + [f"C{h}" for h in (1, 2, 4, 8)]:
            vals = [row[c][k] if row[c] else None for c in ("target", "N0", "ND", "NK", "NL")]
            cmp_ = [(row[f"vs_{c}"]["signs"][k] + (" ×" + f(row[f"vs_{c}"]["ratios"][k]) if row[f"vs_{c}"]["ratios"][k] is not None else "")) if row[f"vs_{c}"] else "—" for c in ("NK", "NL")]
            L.append(f"| {k} | " + " | ".join(f(v) for v in vals) + " | " + " | ".join(cmp_) + " |")
        L += ["", "| Entry size | weight | status | C1 target/NK/NL | C4 target/NK/NL | return before exit target/NK/NL |", "| --- | ---: | --- | --- | --- | --- |"]
        for s, c in tg["classes"].items():
            if c["status"] != "computed":
                L.append(f"| {s} | {f(c['entry_weight'])} | {c['status']} | — | — | — |")
                continue
            nk_c = row["NK"]["classes"].get(s, {}) if row["NK"] else {}
            nl_c = row["NL"]["classes"].get(s, {}) if row["NL"] else {}
            g = lambda d, h: (d.get("C") or {}).get(h)  # noqa: E731
            L.append(f"| {s} | {f(c['entry_weight'])} | {c.get('post_renewal_status')} | {f(g(c,'1'))} / {f(g(nk_c,'1'))} / {f(g(nl_c,'1'))} | {f(g(c,'4'))} / {f(g(nk_c,'4'))} / {f(g(nl_c,'4'))} | {f(c.get('return_before_exit'))} / {f(nk_c.get('return_before_exit'))} / {f(nl_c.get('return_before_exit'))} |")
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m rs_constraint_lab.gte5d")
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
        raise SystemExit("item is not in the E5D manifest")
    execute_item(root, item)
    return 0


if __name__ == "__main__":
    sys.exit(main())
