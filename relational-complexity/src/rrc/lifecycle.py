"""Disposable end-to-end checks for a plan that has not been frozen.

The worker is the real child process. The directory belongs to the caller.
Nothing written here is a scientific result.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from rrc.runner import execute_plan, run_child
from rrc.store import Store


REQUIRED_RESULT_FIELDS = (
    "status",
    "item_id",
    "round_id",
    "plan_hash",
    "spec_hash",
    "engine_version",
)


def exercise(plan: dict, out: Path) -> dict:
    """Run every item, check receipts, interrupt the first item, and resume.

    A second invocation must recompute only the interrupted item. Completed
    items stay byte-for-byte in place until that interruption.
    """
    width = max(len(plan["items"]), 1)
    first = execute_plan(
        plan,
        out,
        max_items=width,
        budget_seconds=60,
        timeout=float(plan["watchdog_seconds"]),
        child=run_child,
    )
    store = Store(out, plan)
    problems = []
    for item in plan["items"]:
        item_id = item["id"]
        result_path = store.item_dir(item_id) / "result.json"
        receipt_path = store.item_dir(item_id) / "receipt.json"
        if not result_path.exists() or not receipt_path.exists():
            problems.append(f"{item_id} is missing a result or a receipt")
            continue
        body = result_path.read_bytes()
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        digest = hashlib.sha256(body).hexdigest()
        if receipt.get("result_sha256") != digest:
            problems.append(f"{item_id} receipt hash disagrees with the result bytes")
        if receipt.get("plan_hash") != store.plan_hash:
            problems.append(f"{item_id} receipt plan hash disagrees")
        result = store.load_result(item_id)
        for field in REQUIRED_RESULT_FIELDS:
            if field not in result:
                problems.append(f"{item_id} result omits {field}")
        if result.get("round_id") != plan["round_id"]:
            problems.append(f"{item_id} round id was not taken from the plan")
        if result.get("spec_hash") != store.spec_hash(item_id):
            problems.append(f"{item_id} spec hash disagrees")
    preserved = {}
    if plan["items"]:
        head = plan["items"][0]["id"]
        for item in plan["items"][1:]:
            preserved[item["id"]] = (store.item_dir(item["id"]) / "result.json").read_bytes()
        # A running item with no result is the parent-death case. Resume
        # recomputes that item and leaves a finished neighbour in place.
        directory = store.item_dir(head)
        (directory / "result.json").unlink()
        (directory / "receipt.json").unlink()
        store.write_status(head, "running")
    second = execute_plan(
        plan,
        out,
        max_items=width,
        budget_seconds=60,
        timeout=float(plan["watchdog_seconds"]),
        child=run_child,
    )
    for item_id, body in preserved.items():
        current = (store.item_dir(item_id) / "result.json").read_bytes()
        if current != body:
            problems.append(f"{item_id} changed during resume")
    return {
        "first": first,
        "second": second,
        "problems": problems,
        "plan_hash": store.plan_hash,
    }
