"""Bounded execution for gravity-time Round G0.

Each item is one (N, mode, family, grade) cell. A completed item file is not
recomputed when a later item fails. The runner refuses an item past the
120-second watchdog. No stochastic trajectory is sampled.
"""

from __future__ import annotations

import time
from pathlib import Path

from rs_constraint_lab.durable import atomic_write_json, canonical_json, read_json, sha256_bytes
from rs_constraint_lab.explore08 import plan_hash
from rs_constraint_lab.gt0 import (
    ANALYSIS_VERSION,
    EXPERIMENT_ID,
    FAMILY_GRADES,
    FAMILY_K,
    MODES,
    NULL_IDENTITY_TOLERANCE,
    ROUND_ID,
    SIZES,
    SOURCE,
    STATIONARY_RESIDUAL_TOLERANCE,
    analyse_item,
    items,
    null_triangles_given_edges,
    scaffold_expressions,
    template_expressions,
)

PLAN_RELPATH = "gravity-time/plans/round-g0-plan.json"
WATCHDOG_SECONDS = 120
ONTOLOGY = {"G": 0, "H": 0, "L": 0, "O": 2, "S": 0, "grammar": "ordinary pair DSL", "N": list(SIZES)}
BASIN_MARGIN = 1e-9


class BasinRunError(RuntimeError):
    """The G0 runner refused a plan, an item or a table."""


def item_path(root: Path, item: dict) -> Path:
    return root / "items" / f"{item['item_id']}.json"


def prepare_g0_plan() -> dict:
    document = {
        "analysis_only": True,
        "analysis_version": ANALYSIS_VERSION,
        "basin_criteria": {
            "attachment_above_null": f"jump and continuous attachment fraction each exceed the HELD null fraction by more than {BASIN_MARGIN}",
            "inward_drift_beyond_null": f"radial drift at shell 2 is below the NULL value at the same N under both clocks by more than {BASIN_MARGIN}",
            "classification": {
                "relational_basin": "recurrent; both criteria true under both clocks",
                "clock_dependent": "recurrent; the pair of criterion flags differs between the clocks",
                "capture": "absorbing regime; reported by absorption, not as a stationary basin",
                "none": "recurrent; neither criterion under either clock",
                "partial": "recurrent; the same single criterion holds under both clocks",
            },
            "scope": "HELD mode only; FREE mode reports clustering against the uniform conditional law",
        },
        "clocks": {
            "continuous": "per-slot exponential rates equal to the event weights; stationary law proportional to jump law divided by total rate; drift per unit time",
            "jump": "lab full-event kernel, one admissible toggle per event, normalised weights; drift per event",
        },
        "experiment_id": EXPERIMENT_ID,
        "families": {
            family: {
                "grades": [g for g in grades if g is not None],
                "K": FAMILY_K[family],
                "template_example": (template_expressions(family, 5, grades[0])[:1] or [None])[0],
            }
            for family, grades in FAMILY_GRADES.items()
        },
        "frozen_comparison_targets": {
            "T1_dens_attachment_equals_null": "HELD DENS attachment fraction equals the HELD null fraction under both clocks within 1e-12 (exchangeable free relations; CL-T18-type factorisation)",
            "T2_dens_triangles_equal_uniform_conditional": "FREE DENS triangles given edge count equal the uniform conditional mean within 1e-12 under both clocks",
            "T3_null_uniform": "NULL stationary law is uniform on the reachable class under both clocks within 1e-12",
            "T4_lock_absorbs_to_complete_graph": "LOCK is absorbing in both modes and the only absorbing state is the complete graph (derivation: formations stay admissible, and an edge in a triangle can never dissolve)",
        },
        "history": False,
        "items": items(),
        "meta_constraints": False,
        "mode": "B",
        "modes": {
            "FREE": "no held structure; full state space from the empty graph",
            "HELD": {"scaffold": scaffold_expressions("HELD"), "source": list(SOURCE), "start": "the source triangle alone"},
        },
        "new_primitives": False,
        "null_triangles_given_edges": {str(n): null_triangles_given_edges(n) for n in SIZES},
        "observables": [
            "reachable class size, recurrent classes, absorbing states",
            "jump-chain and continuous-time stationary laws (recurrent regime)",
            "HELD: probe-to-source distance distribution, attachment fraction and its conditional on free-edge count, radial drift among finite moves by shell, escape and capture rates",
            "FREE: edge-count distribution, expected triangles, triangles given edge count",
            "absorbing regime: absorption probabilities and expected steps from the start state",
        ],
        "ontology": ONTOLOGY,
        "parameter_fit": False,
        "pre_freeze_exposure": {
            "note": "Before freezing, the implementation was exercised on N=4 fixtures (not a G0 size) for NULL, DENS, CLOSE and LOCK in both modes; on N=6 FREE NULL to time the lazy solver (theorem-fixed uniform law); and on N=5 FREE DENS to compare the dense and lazy solvers' stationary vectors only. No G0 observable of any family other than NULL was computed."
        },
        "programme": "GT",
        "question": "Does any minimal, label-covariant, relation-reading rule template on the O=2 pair grammar produce a stable relational basin distinct from density, boundary, combinatorial and clock artefacts?",
        "round_id": ROUND_ID,
        "schema": "rs-gt.basin-plan/v1",
        "stochastic_trajectories": False,
        "tolerances": {"null_identity": NULL_IDENTITY_TOLERANCE, "stationary_residual": STATIONARY_RESIDUAL_TOLERANCE, "basin_margin": BASIN_MARGIN},
        "work_count": {
            "items": len(items()),
            "largest_state_space": 32768,
            "watchdog_seconds": WATCHDOG_SECONDS,
            "wall_time_estimate_seconds": 600,
            "workers": 1,
        },
    }
    document["plan_hash"] = plan_hash(document)
    return document


def _require_plan_contract(plan: dict) -> None:
    if plan.get("stochastic_trajectories") is not False or plan.get("history") is not False or plan.get("meta_constraints") is not False or plan.get("new_primitives") is not False:
        raise BasinRunError("execution refused: G0 adds no trajectories, history, meta-constraints or primitives")
    if plan.get("ontology") != ONTOLOGY or plan.get("round_id") != ROUND_ID:
        raise BasinRunError("execution refused: plan identity drifted")
    if plan.get("items") != items():
        raise BasinRunError("execution refused: the item list drifted")


def require_g0_execution(repo: Path, commit: str | None, *, require_remote: bool = True) -> dict:
    from rs_constraint_lab.explore08 import FrozenPlanError, remote_contains, require_frozen_plan

    plan = require_frozen_plan(repo, commit, PLAN_RELPATH, disk_path=repo / PLAN_RELPATH)
    if require_remote and not remote_contains(repo, commit or ""):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    _require_plan_contract(plan)
    return plan


def run_g0(root: Path, plan: dict) -> list[dict]:
    summaries = []
    for index, item in enumerate(plan["items"], start=1):
        path = item_path(root, item)
        if path.is_file() and read_json(path).get("item_id") == item["item_id"]:
            payload = read_json(path)
            reused = True
        else:
            started = time.perf_counter()
            result = analyse_item(item)
            wall = time.perf_counter() - started
            if wall > WATCHDOG_SECONDS:
                raise BasinRunError(f"{item['item_id']} exceeded the watchdog ({wall:.1f}s)")
            payload = {"item": item, "item_id": item["item_id"], "result": result, "wall_seconds": wall}
            atomic_write_json(path, payload)
            reused = False
        summaries.append({"item_id": item["item_id"], "skipped": reused, "wall_seconds": payload["wall_seconds"]})
        atomic_write_json(root / "status.json", {"completed_items": index, "item_count": len(plan["items"]), "last_item_id": item["item_id"], "updated_unix": time.time()})
    return summaries


def _classify(result: dict, null: dict) -> dict:
    if result["regime"] == "absorbing":
        return {"classification": "capture"}
    if result["regime"] != "recurrent" or result["mode"] != "HELD":
        return {"classification": None}
    flags = {}
    for clock in ("jump", "continuous"):
        obs, base = result[clock], null[clock]
        attach = obs["attachment_fraction"] - obs["null_attachment_fraction"] > BASIN_MARGIN
        d2, b2 = obs["radial_drift_among_finite_moves"].get("2"), base["radial_drift_among_finite_moves"].get("2")
        inward = d2 is not None and b2 is not None and (b2 - d2) > BASIN_MARGIN
        flags[clock] = {"attachment_above_null": attach, "inward_drift_beyond_null": inward}
    signature = {c: (flags[c]["attachment_above_null"], flags[c]["inward_drift_beyond_null"]) for c in flags}
    if signature["jump"] != signature["continuous"]:
        label = "clock_dependent"
    elif all(signature["jump"]):
        label = "relational_basin"
    elif any(signature["jump"]):
        label = "partial"
    else:
        label = "none"
    return {"classification": label, "criteria": flags}


def assemble(root: Path, plan: dict, *, frozen_plan_commit: str | None) -> dict:
    loaded = {}
    for item in plan["items"]:
        path = item_path(root, item)
        if not path.is_file():
            raise BasinRunError(f"missing item {item['item_id']}")
        loaded[item["item_id"]] = read_json(path)
    results = {k: v["result"] for k, v in loaded.items()}
    problems = []
    targets = {}
    for n in SIZES:
        null_held = results[f"HELD-N{n}-NULL-none"]
        null_free = results[f"FREE-N{n}-NULL-none"]
        for key, res in results.items():
            if res["n"] != n:
                continue
            res.update(_classify(res, null_held) if res["mode"] == "HELD" else {"classification": None})
        for grade in FAMILY_GRADES["DENS"]:
            held = results[f"HELD-N{n}-DENS-{grade}"]
            gaps = [abs(held[c]["attachment_fraction"] - held[c]["null_attachment_fraction"]) for c in ("jump", "continuous")]
            free = results[f"FREE-N{n}-DENS-{grade}"]
            uniform = plan["null_triangles_given_edges"][str(n)]
            tgap = max(abs(v - uniform[k]) for c in ("jump", "continuous") for k, v in free[c]["triangles_given_edge_count"].items() if v is not None)
            targets[f"T1-N{n}-{grade}"] = {"gap": max(gaps), "holds": max(gaps) <= NULL_IDENTITY_TOLERANCE}
            targets[f"T2-N{n}-{grade}"] = {"gap": tgap, "holds": tgap <= NULL_IDENTITY_TOLERANCE}
        for mode, res in (("HELD", null_held), ("FREE", null_free)):
            dist = res["jump"].get("distance_distribution") if mode == "HELD" else res["jump"]["edge_count_distribution"]
            deviation = max(res["max_deviation_from_uniform"].values())
            targets[f"T3-N{n}-{mode}"] = {"gap": deviation, "holds": res["regime"] == "recurrent" and deviation <= NULL_IDENTITY_TOLERANCE}
            del dist
        for mode in MODES:
            lock = results[f"{mode}-N{n}-LOCK-prohibit"]
            complete = (1 << (n * (n - 1) // 2)) - 1
            holds = lock["regime"] == "absorbing" and lock.get("absorbing_states") == [complete]
            targets[f"T4-N{n}-{mode}"] = {"absorbing_states": lock.get("absorbing_states"), "holds": holds}
    for key, res in results.items():
        if res["regime"] == "recurrent" and res["stationary_residual"] > STATIONARY_RESIDUAL_TOLERANCE:
            problems.append(f"{key} residual")
    return {
        "analysis_version": ANALYSIS_VERSION,
        "experiment_id": EXPERIMENT_ID,
        "frozen_analysis_plan_commit": frozen_plan_commit,
        "frozen_comparison_targets": targets,
        "plan_hash": plan["plan_hash"],
        "results": results,
        "round_id": ROUND_ID,
        "schema": "rs-gt.basin-tables/v1",
        "validation": {"ok": not problems, "problems": problems},
        "wall_seconds_max": max(v["wall_seconds"] for v in loaded.values()),
    }


def publish(payload: dict, out: Path) -> str:
    body = dict(payload)
    body["payload_sha256"] = sha256_bytes(canonical_json(payload).encode("utf-8"))
    atomic_write_json(out, body)
    return body["payload_sha256"]
