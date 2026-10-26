"""Fault-injection experiment for the micro-batch supervisor.

This module is not a scientific generation. It sleeps, fails, and spawns a
child so the watchdog, restart, and process-tree tests have a bounded target.
"""

from __future__ import annotations

import subprocess
import time
from pathlib import Path

from rs_constraint_lab.durable import atomic_write_json, read_json
from rs_constraint_lab.workstore import Layout, append_text, load_state, make_item_record

SPEC_HASH = "fault-spec"
SEMANTIC_VERSION = "fault-1"
ANALYSIS_VERSION = "fault-1"


def plan(root: Path) -> dict:
    layout = Layout(root)
    layout.ensure()
    request = read_json(Path(root) / "fault-request.json")
    manifest = {
        "advance": "rs_constraint_lab.faultlab:advance",
        "analysis_version": ANALYSIS_VERSION,
        "counts": "rs_constraint_lab.faultlab:counts",
        "executor": "rs_constraint_lab.faultlab:execute_item",
        "experiment_id": "fault",
        "heartbeat_seconds": float(request.get("heartbeat_seconds", 0.2)),
        "merge": "rs_constraint_lab.faultlab:merge_items",
        "phase": "rs_constraint_lab.faultlab:phase",
        "semantic_version": SEMANTIC_VERSION,
        "spec_hash": SPEC_HASH,
        "watchdog_seconds": float(request.get("watchdog_seconds", 120)),
    }
    atomic_write_json(layout.manifest_path(), manifest)
    planned = 0
    for row in request["items"]:
        item_input = {
            "behavior": row["behavior"],
            "key": row["key"],
            "seconds": float(row.get("seconds", 0)),
            "spawn": bool(row.get("spawn", False)),
        }
        record = make_item_record(SPEC_HASH, SEMANTIC_VERSION, ANALYSIS_VERSION, "fault", item_input)
        from rs_constraint_lab.supervisor import ensure_planned

        if ensure_planned(layout, record):
            planned += 1
    return {"planned": planned}


def execute_item(record: dict, context: dict) -> dict:
    root = Path(context["root"])
    item_input = record["input"]
    append_text(root / "fault-executions.log", record["item_id"] + "\n")
    behavior = item_input["behavior"]
    if behavior == "fail":
        raise RuntimeError(f"injected failure {item_input['key']}")
    if behavior in {"sleep", "spawn_sleep"}:
        if item_input.get("spawn"):
            child = subprocess.Popen(["sleep", str(item_input["seconds"])])
            atomic_write_json(root / "fault-children" / f"{item_input['key']}.json", {"pid": child.pid})
        time.sleep(float(item_input["seconds"]))
    if behavior not in {"ok", "sleep", "spawn_sleep", "fail"}:
        raise RuntimeError(f"unknown fault behavior {behavior}")
    return {"key": item_input["key"], "ok": True, "solver_residuals": {"stationary": 0.0, "epoch_defect": 0.0}}


def advance(root: Path) -> int:
    del root
    return 0


def phase(root: Path) -> str:
    layout = Layout(root)
    if not layout.item_state_path().exists():
        return "02_FAULT_TESTS"
    state = load_state(layout)
    if state and all(slot.get("status") == "complete" for slot in state.values()):
        return "COMPLETE"
    if any(slot.get("status") == "quarantined" for slot in state.values()) and not any(slot.get("status") == "pending" for slot in state.values()):
        return "02_FAULT_TESTS"
    return "02_FAULT_TESTS"


def counts(root: Path) -> dict:
    del root
    return {
        "cache_hits": 0,
        "cache_misses": 0,
        "calibrations_complete": 0,
        "calibrations_total": 0,
        "calibrations_unresolved": 0,
    }


def merge_items(root: Path) -> dict:
    layout = Layout(root)
    from rs_constraint_lab.workstore import read_valid_item, work_index

    rows = []
    for item_id, record in sorted(work_index(layout).items()):
        payload = read_valid_item(layout, item_id, SPEC_HASH)
        if payload is None:
            continue
        dest = layout.merge() / "items" / f"{item_id}.json"
        if not dest.exists():
            atomic_write_json(dest, {"item_id": item_id, "result_hash": payload["result_hash"]})
        rows.append(read_json(dest))
    summary = {"items": rows, "schema": "rs-constraint-lab.fault-merge/v1"}
    atomic_write_json(layout.merge() / "summary.json", summary)
    return summary
