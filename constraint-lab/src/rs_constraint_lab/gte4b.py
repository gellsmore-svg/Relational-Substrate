"""Gravity-time programme, Round E4B (prompt GT-P007, OTR 1.0): floor heterogeneity at equal source size.

Chosen after E4A (gravity-time/reports/gt-e4a-reflection.md section 6). Two
held references with four source vertices and three held edges each, N=6:
  S4  star K1,3, centre 0, leaves 1, 2, 3: permanent witness floor centre 0, leaves 2;
  P4  path 0-1-2-3: floor 1 at every source vertex.
Same unmodified rules and measurements as E4A (gte4a). Non-held source pairs
(star leaf-leaf; P4 (0,2), (1,3), (0,3)) are free chords (class C).
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np

from rs_constraint_lab import gt0, gte1, gte2a, gte4a, gtkernel, gtobs

ROUND_ID = "round-e4b"
EXPERIMENT_ID = "gt-round-e4b-floor-heterogeneity"
ANALYSIS_VERSION = "gt-e4b/v1"
PROMPT_ID = "GT-P007"
SCAFFOLD_ORDER = ("S4", "P4")
SIZES = (6,)
FAMILY_GRADES = gte4a.FAMILY_GRADES
FAMILIES = gte4a.FAMILIES


def items() -> list[dict]:
    out = []
    for scaffold in SCAFFOLD_ORDER:
        for n in SIZES:
            for f, g in FAMILY_GRADES:
                role = "geometry_null" if f == "NULL" else ("control" if f in ("PCOMP", "CLOSEW") else "open_scientific")
                out.append({"alphabet": "W4", "family": f, "grade": g, "item_id": gte4a.item_id(scaffold, n, f, g), "mode": "HELD", "n": n, "role": role, "scaffold": scaffold, "held": [list(e) for e in gt0.SCAFFOLDS[scaffold].held]})
    return out


def analyse_item(item: dict, **kwargs):
    return gte4a.analyse_item(item, **kwargs)


check_problems = gte4a.check_problems


def assemble(results: dict[str, dict]) -> dict:
    return gte4a.assemble(results, {}, cells=items(), scaffold_order=SCAFFOLD_ORDER, sizes=SIZES)


PLAN_RELPATH = "gravity-time/plans/round-e4b-plan.json"
GENERATED_RELPATH = "gravity-time/generated/round-e4b"
TABLES_RELPATH = "gravity-time/reports/round-e4b-tables.json"
ATLAS_RELPATH = "gravity-time/reports/gt-e4b-atlas.md"
WATCHDOG_SECONDS = {6: 1800}
ROUND_WALL_CAP_SECONDS = 90 * 60
WORKERS = 4
ONTOLOGY = gte4a.ONTOLOGY | {"N": [6]}
REFERENCE_FILES = ("gravity-time/reports/gt-e4a-reflection.md", "gravity-time/reports/round-e4a-tables.json", "gravity-time/plans/round-e4a-plan.json", "gravity-time/docs/e4-configurable-scaffold.md", "gravity-time/provenance/prompts/GT-P007-agent-input.md")


def prepare_plan(repo: Path) -> dict:
    from rs_constraint_lab.durable import sha256_file
    from rs_constraint_lab.explore08 import plan_hash

    cells = items()
    document = {
        "adaptive_choice_note": "E4B was chosen because of E4A (within-P3 orbit contrast; floor formula; K2 the only zero-floor connected reference) in gt-e4a-reflection.md section 6 (commit 8127d24); it is not independent confirmation of the P3 finding and E4A is unchanged",
        "analysis_only": True,
        "analysis_version": ANALYSIS_VERSION,
        "analytic_floor": {f"{sc}-N{n}": {str(k): v for k, v in gte4a.analytic_floor(sc, n).items()} for sc in SCAFFOLD_ORDER for n in SIZES},
        "chosen_because": "gravity-time/reports/gt-e4a-reflection.md section 6",
        "clocks": "as E4A",
        "comparisons": {
            "B1_star_orbits": "for sigma>0 families (PATHF ws, PATHH wf, CSPH): attachment occupancy per slot at the star centre (floor 0) against the leaves (floor 2), both clocks; conditional on leaf-leaf chords",
            "B2_p4_orbits": "P4 ends against inner vertices (floor 1 everywhere): orbit selectivity without floor heterogeneity, both clocks",
            "B3_star_vs_p4": "raw, normalised and standardised margins against each scaffold's own NULL (r0 = 8/12 for both) at equal k=4, K=3, N=6",
            "B4_direction": "handover index, partner index, flux across the two scaffolds",
            "no_aggregate_score": "no ranking",
        },
        "controls_and_identities": {
            "W_floor": "held-only witness count on every attachment slot equals the analytic floor at every state (S4: centre 0, leaves 2; P4: 1 everywhere)",
            "N_null": "NULL: margins |.| <= 1e-9, flux <= 1e-9, r0 = 8/12",
            "R_reversible": "PCOMP, CLOSEW: flux and |handover|, |partner| <= 1e-9",
            "U_pcomp": "PCOMP continuous raw margin |.| <= 1e-9",
            "G_closew": "CLOSEW Gibbs gap <= 1e-9",
            "Z5_numerical": "as E4A (GTH referee: every class has 4,096 states)",
            "separation_note": "no expectation on any target channel",
        },
        "deliberate_omissions": {"n5": "N=5 with k=4 leaves one probe and no probe-probe slot (no handover)", "n7": "not authorised", "other_scaffolds": "none"},
        "estimands": "as E4A, per cell",
        "experiment_id": EXPERIMENT_ID,
        "families": {f: {g: {"components": [{"grade": cg, "kind": k} for k, cg in FAMILIES[f][g]]}} for f, g in FAMILY_GRADES},
        "geometry": {f"{sc}-N{n}": gte4a.null_geometry(sc, n) for sc in SCAFFOLD_ORDER for n in SIZES},
        "history": False,
        "initial_conditions": "held relations present, all others absent; reachable class",
        "items": cells,
        "meta_constraints": False,
        "method": {"name": "Open-Thetical Research", "path": "research-methods/open-thetical-research.md", "version": "1.0"},
        "mode": "B",
        "new_primitives": False,
        "ontology": ONTOLOGY,
        "open_questions_without_prediction": ["B1-B4", "Anything not anticipated"],
        "parameter_fit": False,
        "pre_freeze_exposure": {"e4a": "all E4A results read", "engineering": "S4/P4 scaffold tests (rule-string kernel equality, floor census, NULL geometry, symmetry) at N=4/5/6; no S4/P4 law under a non-NULL family computed before freezing", "reference_hashes": {rel: sha256_file(repo / rel) for rel in REFERENCE_FILES}},
        "programme": "GT",
        "prompt_id": PROMPT_ID,
        "question": "At equal source size and held-edge count, does redistributing the permanent witness floor (star: 0 at the centre, 2 at the leaves; path P4: 1 everywhere) change where and how much relations attach?",
        "round_id": ROUND_ID,
        "sampling": f"exact census of {len(cells)} cells",
        "schema": "rs-gt.e4b-plan/v1",
        "scaffolds": {name: {"held": [list(e) for e in gt0.SCAFFOLDS[name].held], "source": list(gt0.SCAFFOLDS[name].source)} for name in SCAFFOLD_ORDER},
        "software": {"analysis_module": "rs_constraint_lab.gte4b", "kernel": gtkernel.KERNEL_VERSION, "numpy": np.__version__, "observables": gtobs.OBSERVABLES_VERSION, "python": __import__("platform").python_version()},
        "stochastic_trajectories": "none",
        "stop_conditions": {"item": f"watchdog {WATCHDOG_SECONDS} seconds", "round": f"all items or {ROUND_WALL_CAP_SECONDS} s; then stop", "unresolved": "recorded; no retuning", "amendment": "cell or estimand changes stop the round"},
        "tolerances": "as E4A",
        "work_count": {"items": len(cells), "largest_state_space": 4096, "round_wall_cap_seconds": ROUND_WALL_CAP_SECONDS, "workers": WORKERS},
    }
    document["plan_hash"] = plan_hash(document)
    return document


def require_execution(repo: Path, commit: str | None, *, require_remote: bool = True) -> dict:
    from rs_constraint_lab.explore08 import FrozenPlanError, remote_contains, require_frozen_plan

    plan = require_frozen_plan(repo, commit, PLAN_RELPATH, disk_path=repo / PLAN_RELPATH)
    if require_remote and not remote_contains(repo, commit or ""):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    if plan.get("items") != items() or plan.get("new_primitives") is not False or plan.get("ontology") != ONTOLOGY:
        raise FrozenPlanError("execution refused: E4B plan contract drifted")
    return plan


def execute_item(root: Path, item: dict):
    return gte4a.execute_item(root, item)


def run(root: Path, plan: dict, *, workers: int = WORKERS, **kwargs):
    return gte1.run(root, plan, workers=workers, watchdogs=kwargs.pop("watchdogs", WATCHDOG_SECONDS), wall_cap=kwargs.pop("wall_cap", ROUND_WALL_CAP_SECONDS), module="rs_constraint_lab.gte4b", **kwargs)


def publish(root: Path, plan: dict, out: Path, *, frozen_plan_commit: str) -> str:
    from rs_constraint_lab.durable import atomic_write_json, canonical_json, read_json, sha256_bytes

    records = {}
    for it in plan["items"]:
        path = root / "items" / f"{it['item_id']}.json"
        records[it["item_id"]] = read_json(path) if path.is_file() else {"item_id": it["item_id"], "status": "missing"}
    results = {k: v["result"] for k, v in records.items() if "result" in v}
    assembled = assemble(results)
    item_records = {k: {"numerical_problems": check_problems(results[k]) if k in results else None, "peak_rss_mb": v.get("peak_rss_mb_parent_view", v.get("peak_rss_mb")), "role": next(it["role"] for it in plan["items"] if it["item_id"] == k), "scaffold": next(it["scaffold"] for it in plan["items"] if it["item_id"] == k), "status": v["status"], "wall_seconds": v.get("wall_seconds")} for k, v in records.items()}
    payload = {"analysis_version": ANALYSIS_VERSION, "experiment_id": EXPERIMENT_ID, "frozen_analysis_plan_commit": frozen_plan_commit, "item_records": item_records, "plan_hash": plan["plan_hash"], "results": results, "round_id": ROUND_ID, "schema": "rs-gt.e4b-tables/v1", "status_counts": {s: sum(r["status"] == s for r in item_records.values()) for s in sorted({r["status"] for r in item_records.values()})}, **assembled}
    body = dict(payload)
    body["payload_sha256"] = sha256_bytes(canonical_json(payload).encode("utf-8"))
    atomic_write_json(out, body)
    return body["payload_sha256"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m rs_constraint_lab.gte4b")
    sub = parser.add_subparsers(dest="command", required=True)
    one = sub.add_parser("item")
    one.add_argument("--root", required=True)
    one.add_argument("--item-id", required=True)
    sub.add_parser("atlas")
    args = parser.parse_args(argv)
    from rs_constraint_lab.durable import read_json

    if args.command == "atlas":
        repo = Path(__file__).resolve().parents[3]
        text = gte4a.render_atlas(repo, repo / TABLES_RELPATH, title="GT-E4B floor-heterogeneity atlas", tables_rel=TABLES_RELPATH, scaffold_order=SCAFFOLD_ORDER)
        (repo / ATLAS_RELPATH).write_text(text)
        print(f"wrote {ATLAS_RELPATH} ({len(text)} bytes)")
        return 0
    root = Path(args.root)
    plan = read_json(root / "plan.json")
    (item,) = [it for it in plan["items"] if it["item_id"] == args.item_id]
    if item not in items() and not plan.get("synthetic_fixture"):
        raise SystemExit("item is not in the E4B manifest")
    execute_item(root, item)
    return 0


if __name__ == "__main__":
    sys.exit(main())
