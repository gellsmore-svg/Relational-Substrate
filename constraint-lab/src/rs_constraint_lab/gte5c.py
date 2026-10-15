"""GT round E5C: durable renewal and post-renewal survival over anchor-local events (GT-P011).

The same twelve FREE kernels as E5A/E5B (N = 5, 6). Each item recomputes the kernel and its
stationary law, then, for F_2PATH and F_TRI (primary and relabelled anchors), on the target law,
ND (E5A, unchanged) and NK (E5B, unchanged): the first-renewal probability R0 (replicating E5B),
unconditional durable renewal U_h and conditional survival C_h at h = 0, 1, 2, 4, 8 anchor-local
events, return versus exit after renewal, and immediate original return, stratified by entry-set
size. N0 is the NULL item of the same size. Definitions: ``gravity-time/docs/e5c-durable-renewal-definitions.md``.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np

from rs_constraint_lab import gte1, gte5a, gte5b, gtkernel, gtobs
from rs_constraint_lab import gtdurable as D
from rs_constraint_lab import gtpersist as P
from rs_constraint_lab import gtrenew as RN
from rs_constraint_lab.state import edges

ROUND_ID = "round-e5c"
EXPERIMENT_ID = "gt-round-e5c-free-durable-renewal"
ANALYSIS_VERSION = "gt-e5c/v1"
PROMPT_ID = "GT-P011"
MODE = "FREE"
FAMILY_GRADES = gte5a.FAMILY_GRADES
SIZES = (5, 6)
IDENTITY = 1e-9
REPLICATION_ABS = 1e-10
REPLICATION_REL = 1e-8
HUB_COMMIT = "38c2501bbab22ca1eb2288ea76a962ac0170d5e6"
ROLE = gte5a.ROLE
LAWS = ("target", "nd", "nk")


def items() -> list[dict]:
    return [{**it, "prior_cell": f"round-e5b {it['item_id']}"} for it in gte5a.items()]


def predicate_ids() -> list[str]:
    return [f"{it['item_id']}:{p}" for it in items() for p in D.PREDICATES]


# --- per-item analysis ------------------------------------------------------------------------


def law_problems(block: dict, label: str, published: dict | None) -> list[str]:
    out = []
    for key in ("predicates", "relabelled"):
        for p in D.PREDICATES:
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
                    out.append(f"{label}/{key}/{p}/s{s}: remote transition leaves R (T13 violated)")
                if abs(c["return_before_exit"] + c["exit_before_return"] - 1.0) > IDENTITY or abs(c["first_local_split_sum"] - 1.0) > IDENTITY:
                    out.append(f"{label}/{key}/{p}/s{s}: leave-R causes do not sum to 1")
                for h in D.HORIZONS:
                    if abs(c["U"][str(h)] - c["R0"] * c["C"][str(h)]) > 1e-12 * max(1.0, c["U"][str(h)]):
                        out.append(f"{label}/{key}/{p}/s{s}: U != R0 C")
                for name, sv in c["solves"].items():
                    if sv.get("dense_max_abs_difference") is not None and sv["dense_max_abs_difference"] > IDENTITY:
                        out.append(f"{label}/{key}/{p}/s{s}: {name} dense and iterative disagree")
    for p in D.PREDICATES:
        a, b = block["predicates"][p], block["relabelled"][p]
        if a.get("status") == "STRUCTURALLY_IMPOSSIBLE" or b.get("status") == "STRUCTURALLY_IMPOSSIBLE":
            if a.get("status") != b.get("status"):
                out.append(f"{label}/{p}: relabelled anchor status differs")
            continue
        for h in D.HORIZONS:
            x, y = a["U"][str(h)], b["U"][str(h)]
            if abs(x - y) > IDENTITY * max(abs(x), abs(y), 1e-300) and abs(x - y) > 1e-15:
                out.append(f"{label}/{p}: relabelled anchor disagrees at h={h}")
        if published is not None:
            old = published[p]["replacement"].get("renewal_unconditional")
            if old is not None and abs(a["R0"] - old) > max(REPLICATION_ABS, REPLICATION_REL * abs(old)):
                out.append(f"{label}/{p}: R0 does not replicate E5B renewal")
    return out


def analyse_item(item: dict, *, on_main=None, published: dict | None = None) -> dict:
    n = item["n"]
    m = len(edges(n))
    comps = [tuple(c) for c in item["components"]]
    timings: dict[str, float] = {}
    t0 = time.perf_counter()
    chain, _ = gtkernel.reachable_chain(n, MODE, comps)
    result: dict = {"analysis_version": ANALYSIS_VERSION, "item_id": item["item_id"], "kernel_version": gtkernel.KERNEL_VERSION, "durable_version": D.DURABLE_VERSION, "renew_version": RN.RENEW_VERSION}
    result["ergodicity"] = {"all_rates_positive": bool((chain.W > 0).all()), "full_space": bool(len(chain.states) == 1 << m)}
    stat = gtobs.stationary(chain, 0)
    timings["build_stationary"] = time.perf_counter() - t0
    result["stationary"] = {k: v for k, v in stat.items() if k not in ("ct", "jump")}
    if not stat["resolved"]:
        result["status_note"] = "target stationary law unresolved"
        return result
    ct = stat["ct"]
    result["pcomp_uniform_max_relative"] = float(np.abs(ct * (1 << m) - 1.0).max()) if item["family"] == "PCOMP" else None
    laws = {"target": (chain, ct)}
    p_k = P.density_profile(chain.states, ct, m)
    if P.nd_rates(p_k)["resolved"]:
        nd, pi_nd, _ = P.nd_chain(n, p_k, float(ct @ chain.rates))
        laws["nd"] = (nd, pi_nd)
        result["nd_construction"] = {"resolved": True}
    else:
        result["nd_construction"] = {"resolved": False}
    lf = RN.layer_fluxes(chain, ct, n)
    if RN.nk_rates(lf["p"], lf["up"])["resolved"]:
        nk, pi_nk, info = RN.nk_chain(n, lf["p"], lf["up"])
        laws["nk"] = (nk, pi_nk)
        result["nk_construction"] = {"resolved": True, "detailed_balance_max_relative": info["detailed_balance_max_relative"], "global_balance_relative": info["global_balance_relative"]}
    else:
        result["nk_construction"] = {"resolved": False}
    for name, (ch, law) in laws.items():
        t0 = time.perf_counter()
        result[name] = D.analyse_law(ch, law, n)
        pub = published.get(name) if published else None
        result[f"{name}_problems"] = law_problems(result[name], name, pub)
        timings[name] = time.perf_counter() - t0
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
    if r.get("pcomp_uniform_max_relative") is not None and r["pcomp_uniform_max_relative"] > IDENTITY:
        out.append("PCOMP law not uniform")
    for name in LAWS:
        if name not in r:
            out.append(f"{name.upper()} UNRESOLVED")
            continue
        out += r.get(f"{name}_problems", [])
    return out


# --- assembly ----------------------------------------------------------------------------------


def _view(block: dict | None, p: str) -> dict | None:
    if block is None:
        return None
    d = block["predicates"][p]
    v = {"status": d.get("status"), "R0": d.get("R0"), "feasible_entry_fraction": d.get("feasible_entry_fraction")}
    for h in D.HORIZONS:
        v[f"U{h}"] = d["U"][str(h)]
        v[f"C{h}"] = d["C"][str(h)]
    v["classes"] = {s: {k: c.get(k) for k in ("entry_weight", "feasible", "status", "post_renewal_status", "R0", "U", "C", "return_before_exit", "exit_before_return", "immediate_original_return", "immediate_exit", "first_hit_vs_stationary_l1", "local_share_at_first_renewal")} for s, c in d["classes"].items()}
    if "size_ge2" in d:
        v["size_ge2"] = d["size_ge2"]
    return v


def _cmp(t, c):
    if t is None or c is None:
        return "undefined", None
    sign = gte5a._sign(t, c, "higher", "lower")
    return sign, (t / c if c not in (0.0,) else None)


def predicate_row(tgt, n0, nd, nk, p) -> dict:
    row = {"target": _view(tgt, p), "N0": _view(n0, p), "ND": _view(nd, p), "NK": _view(nk, p)}
    t = row["target"]
    keys = ["R0"] + [f"U{h}" for h in D.HORIZONS] + [f"C{h}" for h in D.HORIZONS]
    for name in ("N0", "ND", "NK"):
        c = row[name]
        if c is None or t["status"] == "STRUCTURALLY_IMPOSSIBLE":
            row[f"vs_{name}"] = None
            continue
        signs, ratios = {}, {}
        for k in keys:
            signs[k], ratios[k] = _cmp(t[k], c[k])
        row[f"vs_{name}"] = {"signs": signs, "ratios": ratios}
    return row


def frozen_checks(results: dict, sizes: tuple[int, ...] = SIZES, manifest: list[dict] | None = None) -> dict:
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
        for p in D.PREDICATES:
            vals = [r[law]["predicates"][p] for law in LAWS if law in r]
            if vals[0].get("status") == "STRUCTURALLY_IMPOSSIBLE":
                continue
            for h in D.HORIZONS:
                xs = [v["U"][str(h)] for v in vals]
                if max(xs) - min(xs) > 1e-10 * max(max(xs), 1e-300) and max(xs) - min(xs) > 1e-15:
                    bad.append(f"{p}: N0/ND/NK differ at h={h}")
        nulls[str(n)] = bad or "pass"
    checks["NULL_fixed_point"] = nulls
    return checks


def assemble(results: dict, sizes: tuple[int, ...] = SIZES, manifest: list[dict] | None = None) -> dict:
    rows = {}
    for it in manifest or items():
        if it["family"] == "NULL" or it["item_id"] not in results:
            continue
        r = results[it["item_id"]]
        n0 = results.get(gte5a.item_id(it["n"], "NULL", "none"))
        for p in D.PREDICATES:
            rows[f"{it['item_id']}:{p}"] = predicate_row(r["target"], n0["target"] if n0 else None, r.get("nd"), r.get("nk"), p)
    return {"predicate_rows": rows, "frozen_checks": frozen_checks(results, sizes, manifest)}


# --- plan, execution, publication -------------------------------------------------------------

PLAN_RELPATH = "gravity-time/plans/round-e5c-plan.json"
GENERATED_RELPATH = "gravity-time/generated/round-e5c"
TABLES_RELPATH = "gravity-time/reports/round-e5c-tables.json"
ATLAS_RELPATH = "gravity-time/reports/gt-e5c-atlas.md"
E5B_TABLES_RELPATH = "gravity-time/reports/round-e5b-tables.json"
WATCHDOG_SECONDS = {5: 900, 6: 2400}
ROUND_WALL_CAP_SECONDS = 3 * 3600
WORKERS = 4
ONTOLOGY = gte5a.ONTOLOGY
REFERENCE_FILES = (
    "research-methods/open-thetical-research.md",
    "gravity-time/provenance/prompts/GT-P011-agent-input.md",
    "gravity-time/docs/gt-p011-starting-audit.md",
    "gravity-time/docs/e5c-durable-renewal-definitions.md",
    "gravity-time/docs/e5b-definitions-controls-and-feasibility.md",
    "gravity-time/docs/e5-definitions-and-null-construction.md",
    "gravity-time/reports/round-e5b-tables.json",
    "gravity-time/plans/round-e5b-plan.json",
    "constraint-lab/docs/scientific-plan-discipline.md",
    "constraint-lab/src/rs_constraint_lab/gtdurable.py",
    "constraint-lab/src/rs_constraint_lab/gte5c.py",
    "constraint-lab/src/rs_constraint_lab/gtrenew.py",
    "constraint-lab/src/rs_constraint_lab/gtpersist.py",
    "constraint-lab/tests/test_gtdurable.py",
)


def prepare_plan(repo: Path, *, source_commit: str, gt_baseline: str) -> dict:
    from rs_constraint_lab.durable import sha256_file
    from rs_constraint_lab.explore08 import plan_hash

    document = {
        "analysis_only": True,
        "analysis_version": ANALYSIS_VERSION,
        "chosen_because": "GT-P010 reflection section 8 option A (durable renewal), authorised by GT-P011 as the only scientific round",
        "consulted_hub": {"commit": HUB_COMMIT, "ref": "origin/main", "method": "git show (read-only)", "shared_questions": ["XQ::01", "XQ::04", "XQ::07", "XQ::03"], "note": "later hub movement does not re-motivate this frozen round"},
        "gt_baseline_commit": gt_baseline,
        "clock": "anchor-local event count (slots incident on an anchor vertex), within one jump trajectory; remote events are integrated through the local-event kernel, never discarded",
        "comparators": {"N0": "NULL item at the same N", "ND": "E5A T6 unchanged (gtpersist.nd_chain)", "NK": "E5B T11 unchanged (gtrenew.nk_chain)", "not_implemented": ["any local/within-layer comparator (a future round)", "CL matched-source control (not mapped)"]},
        "predicates": {"F_2PATH": "deg(0) >= 2; entry set S0 = the two neighbours after entry", "F_TRI": "edge {0,1} present with >= 1 completer; S0 = completers after entry; stratified by |S0|", "relabelled": "image under v -> N-1-v", "excluded": "F_STAR (complete renewal impossible at N<=6; partial-renewal durability not defined in this round)"},
        "estimands": {
            "R0": "P_Palm(first renewal before exit); replicates E5B renewal_unconditional (check, not evidence)",
            "U_h": "P_Palm(first renewal before exit AND the next h anchor-local events each leave the state in R(S0)); U_0 = R0",
            "C_h": "U_h / R0 (conditional post-renewal survival)",
            "causes": "after first renewal: P(an original partner returns before exit) and P(exit before return); exclusive, exhaustive (T15)",
            "immediate": "P(next anchor-local event returns an original partner | renewal), P(next local event exits | renewal)",
            "strata": "entry-set size distribution under Palm entry; every quantity per size class; F_TRI pooled over |S0| >= 2 reported separately from |S0| = 1",
            "diagnostics": "L1 distance between the first-renewal law and the stationary law restricted to R (first-hit versus stationary); local share of events at first renewal",
        },
        "horizons": list(D.HORIZONS),
        "structural_statuses": {"STRUCTURALLY_IMPOSSIBLE": "no feasible entry class (T10)", "STRUCTURALLY_ZERO_FOR_H_GE_1": "no local transition from R back to R exists (T14; e.g. F_2PATH at N=5)", "renewal_probability_zero": "feasible but R not reached (none expected with positive rates)"},
        "experiment_id": EXPERIMENT_ID,
        "families": {f: {g: {"components": [{"grade": cg, "kind": k} for k, cg in gte5a.components(f, g)]}} for f, g in FAMILY_GRADES},
        "frozen_checks": {
            "replication": "R0 of target, ND and NK equals the published E5B renewal_unconditional within max(1e-10, 1e-8 |value|)",
            "monotonicity": "U_0 >= U_1 >= U_2 >= U_4 >= U_8",
            "consistency": "U_h = R0 C_h per class (1e-12)",
            "T13": "no remote transition from R leaves R (exact count 0)",
            "causes": "return + exit = 1 and next-local split sums to 1 (1e-9)",
            "relabelling": "relabelled anchors agree within 1e-9 relative (or 1e-15 absolute)",
            "NULL": "target, ND and NK identical on NULL items (1e-10)",
            "PCOMP": "CT law uniform (1e-9)",
            "solver": "BiCGSTAB relative residual 1e-12 (resolved at 10x); dense versus iterative <= 1e-9 where dense is run (<= 4096 states); unresolved solves recorded UNRESOLVED",
        },
        "history": False,
        "hypotheses_without_prediction": ["D1 durable reconstruction", "D2 flicker-assisted renewal", "D3 density-layer traffic", "D4 within-layer/local kinetics", "D5 occupancy and entrance composition", "D6 clock/readout dependence", "D7 null, structural impossibility or unanticipated"],
        "items": items(),
        "meta_constraints": False,
        "method": {"name": "Open-Thetical Research", "path": "research-methods/open-thetical-research.md", "version": "1.0"},
        "new_primitives": False,
        "ontology": ONTOLOGY,
        "parameter_fit": False,
        "predicate_ids": predicate_ids(),
        "pre_freeze_exposure": {
            "published": "E5A and E5B values for the same 12 laws (including E5B renewal R0, which E5C replicates)",
            "engineering": "proof fixtures on N<=4 kernels and synthetic neighbourhood rules at N=5,6 (not GT families); timing on the synthetic N=6 rule only (about 21 s per law for both predicates and both anchors; 346 MB); no E5C quantity of any N=5 or N=6 scientific cell computed before freezing",
            "structural_discovery": "T14 (F_2PATH at N=5 cannot survive any local event after renewal) was found on the synthetic N=5 rule; it is combinatorial and law-independent",
            "reference_hashes": {rel: sha256_file(repo / rel) for rel in REFERENCE_FILES},
        },
        "programme": "GT",
        "prompt_id": PROMPT_ID,
        "question": "Once a flexible relational property has reached a fully renewed partner set, how often does it remain continuously true with the original partners absent over several subsequent anchor-local changes, relative to N0, ND and NK?",
        "round_id": ROUND_ID,
        "rule_reading": "no rule reads an anchor, S0, renewal state or local-event count; all are analysis-defined observers",
        "schema": "rs-gt.e5c-plan/v1",
        "software": {"analysis_module": "rs_constraint_lab.gte5c", "durable": D.DURABLE_VERSION, "kernel": gtkernel.KERNEL_VERSION, "numpy": np.__version__, "renewal": RN.RENEW_VERSION, "persistence": P.PERSIST_VERSION, "python": __import__("platform").python_version(), "scipy": "not used"},
        "solver": {"method": "row (forward) BiCGSTAB on killed sub-chains in canonical frames", "tolerance": D.SOLVE_TOLERANCE, "cap_iterations": D.SOLVE_CAP, "cap_seconds": D.SOLVE_SECONDS, "dense_cross_check_max_size": D.DENSE_LIMIT},
        "source_commit": source_commit,
        "stochastic_trajectories": "none",
        "stop_conditions": {"item": f"watchdog {WATCHDOG_SECONDS} s by N", "round": f"all items or {ROUND_WALL_CAP_SECONDS} s", "unresolved": "recorded as UNRESOLVED or FAILED_FROZEN_CHECK; no retuning, no substitute cell", "amendment": "any cell, predicate, horizon or estimand change stops the round", "after_round": "no E5D"},
        "tolerances": {"identity": IDENTITY, "tie_relative": P.TIE_RELATIVE, "replication": [REPLICATION_ABS, REPLICATION_REL], "solve": [D.SOLVE_TOLERANCE, D.SOLVE_CAP, D.SOLVE_SECONDS]},
        "work_count": {"items": 12, "kernels": 12, "predicate_analyses": len(predicate_ids()), "laws_per_item": "target, ND, NK; primary and relabelled anchors", "largest_state_space": 32768, "memory_ceiling_per_worker_bytes": 2_000_000_000, "round_wall_cap_seconds": ROUND_WALL_CAP_SECONDS, "watchdog_seconds": {str(k): v for k, v in WATCHDOG_SECONDS.items()}, "workers": WORKERS, "estimate_note": "about 1-2 min per N=6 item from the synthetic timing (3 laws x ~21 s); a few minutes in total expected, not promised"},
    }
    document["plan_hash"] = plan_hash(document)
    return document


def require_execution(repo: Path, commit: str | None, *, require_remote: bool = True) -> dict:
    from rs_constraint_lab.explore08 import FrozenPlanError, remote_contains, require_frozen_plan

    plan = require_frozen_plan(repo, commit, PLAN_RELPATH, disk_path=repo / PLAN_RELPATH)
    if require_remote and not remote_contains(repo, commit or ""):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    if plan.get("items") != items() or plan.get("new_primitives") is not False or plan.get("ontology") != ONTOLOGY or plan.get("consulted_hub", {}).get("commit") != HUB_COMMIT or plan.get("horizons") != list(D.HORIZONS):
        raise FrozenPlanError("execution refused: E5C plan contract drifted")
    return plan


def execute_item(root: Path, item: dict) -> dict:
    import resource

    from rs_constraint_lab.durable import atomic_write_json, read_json

    started = time.perf_counter()
    repo = Path(__file__).resolve().parents[3]
    pub = None
    if (repo / E5B_TABLES_RELPATH).is_file():
        r5b = read_json(repo / E5B_TABLES_RELPATH)["results"].get(item["item_id"])
        if r5b:
            pub = {law: r5b[law]["predicates"] for law in LAWS if law in r5b}

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
    return gte1.run(root, plan, workers=workers, watchdogs=kwargs.pop("watchdogs", WATCHDOG_SECONDS), wall_cap=kwargs.pop("wall_cap", ROUND_WALL_CAP_SECONDS), module=kwargs.pop("module", "rs_constraint_lab.gte5c"), **kwargs)


def publish(root: Path, plan: dict, out: Path, *, frozen_plan_commit: str) -> str:
    from rs_constraint_lab.durable import atomic_write_json, canonical_json, read_json, sha256_bytes

    records = {}
    for it in plan["items"]:
        path = root / "items" / f"{it['item_id']}.json"
        records[it["item_id"]] = read_json(path) if path.is_file() else {"item_id": it["item_id"], "status": "missing"}
    results = {k: v["result"] for k, v in records.items() if "result" in v}
    assembled = assemble(results)
    item_records = {k: {"numerical_problems": check_problems(results[k]) if k in results else None, "peak_rss_mb": v.get("peak_rss_mb"), "role": next(it["role"] for it in plan["items"] if it["item_id"] == k), "status": v["status"], "wall_seconds": v.get("wall_seconds")} for k, v in records.items()}
    payload = {"analysis_version": ANALYSIS_VERSION, "consulted_hub": HUB_COMMIT, "experiment_id": EXPERIMENT_ID, "frozen_analysis_plan_commit": frozen_plan_commit, "item_records": item_records, "plan_hash": plan["plan_hash"], "results": results, "round_id": ROUND_ID, "schema": "rs-gt.e5c-tables/v1", "source_commit": plan.get("source_commit"), "status_counts": {s: sum(r["status"] == s for r in item_records.values()) for s in sorted({r["status"] for r in item_records.values()})}, **assembled}
    body = dict(payload)
    body["payload_sha256"] = sha256_bytes(canonical_json(payload).encode("utf-8"))
    atomic_write_json(out, body)
    return body["payload_sha256"]


def render_atlas(repo: Path, tables: Path | None = None) -> str:
    from rs_constraint_lab.durable import read_json

    f = gte5b._f
    t = read_json(tables or repo / TABLES_RELPATH)
    L = ["# GT-E5C atlas: durable renewal over anchor-local events", "", f"*Frozen plan `{t['frozen_analysis_plan_commit'][:7]}` (plan_hash `{t['plan_hash'][:12]}…`); payload `{t['payload_sha256'][:12]}…`; consulted hub `{t['consulted_hub'][:7]}`. Exact finite-generator values; ties relative 1e-9.*", ""]
    L += ["## Item status", "", "| Item | Status | Wall s | Problems |", "| --- | --- | ---: | --- |"]
    for k, v in t["item_records"].items():
        L.append(f"| {k} | {v['status']} | {f(v.get('wall_seconds'), 1)} | {'; '.join(v.get('numerical_problems') or []) or 'none'} |")
    L += ["", "## Frozen checks", ""] + [f"- `{k}`: {v}" for k, v in t["frozen_checks"].items()]
    for rid, row in t["predicate_rows"].items():
        tg = row["target"]
        L += ["", f"## {rid}", "", f"Status {tg['status']}; feasible entry fraction {f(tg['feasible_entry_fraction'])}."]
        if tg["status"] == "STRUCTURALLY_IMPOSSIBLE":
            continue
        L += ["", "| Quantity | target | N0 | ND | NK | vs NK |", "| --- | ---: | ---: | ---: | ---: | --- |"]
        for k in ["R0"] + [f"U{h}" for h in (1, 2, 4, 8)] + [f"C{h}" for h in (1, 2, 4, 8)]:
            vals = [row[c][k] if row[c] else None for c in ("target", "N0", "ND", "NK")]
            vs = row["vs_NK"]
            L.append(f"| {k} | " + " | ".join(f(v) for v in vals) + f" | {vs['signs'][k] + (' ×' + f(vs['ratios'][k]) if vs['ratios'][k] is not None else '') if vs else '—'} |")
        L += ["", "| Entry size | weight | status | post-renewal | R0 | C1 | C2 | C4 | return before exit | immediate return |", "| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
        for s, c in tg["classes"].items():
            L.append(f"| {s} | {f(c['entry_weight'])} | {c['status']} | {c.get('post_renewal_status') or '—'} | {f(c.get('R0'))} | {f((c.get('C') or {}).get('1'))} | {f((c.get('C') or {}).get('2'))} | {f((c.get('C') or {}).get('4'))} | {f(c.get('return_before_exit'))} | {f(c.get('immediate_original_return'))} |")
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m rs_constraint_lab.gte5c")
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
        raise SystemExit("item is not in the E5C manifest")
    execute_item(root, item)
    return 0


if __name__ == "__main__":
    sys.exit(main())
