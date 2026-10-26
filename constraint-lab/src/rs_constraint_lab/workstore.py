"""Durable files for a micro-batch experiment.

Progress lives on disk. A crash may lose only the batch that was open.
A temporary file is never a completed item.
"""

from __future__ import annotations

import json
import os
import socket
from datetime import datetime, timezone
from pathlib import Path

from rs_constraint_lab.durable import atomic_write_json, canonical_json, read_json, sha256_bytes

ITEM_SCHEMA = "rs-constraint-lab.item/v1"
RECEIPT_SCHEMA = "rs-constraint-lab.batch-receipt/v1"
STATUS_SCHEMA = "rs-constraint-lab.status/v1"

ITEM_FIELDS = (
    "analysis_version",
    "completed_at",
    "input",
    "input_hash",
    "item_id",
    "kind",
    "result",
    "result_hash",
    "schema",
    "semantic_version",
    "solver_residuals",
    "spec_hash",
    "started_at",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_utc(text: str) -> datetime:
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    return datetime.fromisoformat(text)


def identity_payload(spec_hash: str, semantic_version: str, analysis_version: str, kind: str, item_input: dict) -> dict:
    return {
        "analysis_version": analysis_version,
        "input": item_input,
        "kind": kind,
        "semantic_version": semantic_version,
        "spec_hash": spec_hash,
    }


def item_id_for(spec_hash: str, semantic_version: str, analysis_version: str, kind: str, item_input: dict) -> str:
    return sha256_bytes(canonical_json(identity_payload(spec_hash, semantic_version, analysis_version, kind, item_input)).encode("utf-8"))


def input_hash_for(item_input: dict) -> str:
    return sha256_bytes(canonical_json(item_input).encode("utf-8"))


def make_item_record(spec_hash: str, semantic_version: str, analysis_version: str, kind: str, item_input: dict) -> dict:
    return {
        "analysis_version": analysis_version,
        "input": item_input,
        "input_hash": input_hash_for(item_input),
        "item_id": item_id_for(spec_hash, semantic_version, analysis_version, kind, item_input),
        "kind": kind,
        "schema": "rs-constraint-lab.work-item/v1",
        "semantic_version": semantic_version,
        "spec_hash": spec_hash,
    }


class Layout:
    def __init__(self, root: Path):
        self.root = Path(root)

    def plan(self) -> Path:
        return self.root / "plan"

    def items(self) -> Path:
        return self.root / "items"

    def batches(self) -> Path:
        return self.root / "batches"

    def receipts(self) -> Path:
        return self.root / "receipts"

    def calibration(self) -> Path:
        return self.root / "calibration"

    def progress(self) -> Path:
        return self.root / "progress"

    def cache(self) -> Path:
        return self.root / "cache"

    def merge(self) -> Path:
        return self.root / "merge"

    def ensure(self) -> None:
        for path in (
            self.plan(),
            self.items(),
            self.batches() / "planned",
            self.batches() / "running",
            self.batches() / "complete",
            self.batches() / "failed",
            self.batches() / "quarantined",
            self.receipts(),
            self.calibration(),
            self.progress(),
            self.cache(),
            self.merge(),
        ):
            path.mkdir(parents=True, exist_ok=True)

    def item_path(self, item_id: str) -> Path:
        return self.items() / f"{item_id}.json"

    def error_path(self, item_id: str) -> Path:
        return self.items() / f"{item_id}.error.json"

    def batch_dir(self, state: str, batch_id: str) -> Path:
        return self.batches() / state / batch_id

    def receipt_path(self, batch_id: str) -> Path:
        return self.receipts() / f"{batch_id}.json"

    def status_path(self) -> Path:
        return self.progress() / "status.json"

    def heartbeat_path(self) -> Path:
        return self.progress() / "heartbeat.json"

    def log_path(self) -> Path:
        return self.progress() / "progress.log"

    def events_path(self) -> Path:
        return self.progress() / "events.jsonl"

    def lock_path(self) -> Path:
        return self.progress() / "supervisor.lock"

    def stop_path(self) -> Path:
        return self.progress() / "stop.request"

    def manifest_path(self) -> Path:
        return self.plan() / "manifest.json"

    def work_items_path(self) -> Path:
        return self.plan() / "work-items.jsonl"

    def item_state_path(self) -> Path:
        return self.plan() / "item-state.json"

    def dependency_path(self) -> Path:
        return self.plan() / "dependency-state.json"

    def batch_seq_path(self) -> Path:
        return self.plan() / "batch-seq.json"

    def policy_path(self) -> Path:
        return self.plan() / "batch-policy.json"


def append_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())


def log_progress(layout: Layout, message: str) -> None:
    append_text(layout.log_path(), f"{utc_now()} {message}\n")


def log_event(layout: Layout, event_type: str, message: str, *, phase: str | None = None, batch_id: str | None = None, item_id: str | None = None, counts: dict | None = None) -> None:
    payload = {
        "batch_id": batch_id,
        "counts": counts or {},
        "event_type": event_type,
        "item_id": item_id,
        "message": message,
        "phase": phase,
        "timestamp": utc_now(),
    }
    append_text(layout.events_path(), json.dumps(payload, sort_keys=True) + "\n")


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def append_jsonl(path: Path, payload: dict) -> None:
    append_text(path, json.dumps(payload, sort_keys=True) + "\n")


def load_state(layout: Layout) -> dict:
    path = layout.item_state_path()
    if not path.exists():
        return {}
    return read_json(path)


def save_state(layout: Layout, state: dict) -> None:
    atomic_write_json(layout.item_state_path(), state)


def load_work_items(layout: Layout) -> list[dict]:
    return load_jsonl(layout.work_items_path())


def work_index(layout: Layout) -> dict[str, dict]:
    found = {}
    for row in load_work_items(layout):
        found[row["item_id"]] = row
    return found


def result_hash(result: dict) -> str:
    return sha256_bytes(canonical_json(result).encode("utf-8"))


def validate_item_payload(payload: dict, expected_spec: str | None = None) -> None:
    if payload.get("schema") != ITEM_SCHEMA:
        raise ValueError("item schema is not a completed item")
    for field in ITEM_FIELDS:
        if field not in payload:
            raise ValueError(f"item is missing {field}")
    identity = item_id_for(
        payload["spec_hash"],
        payload["semantic_version"],
        payload["analysis_version"],
        payload["kind"],
        payload["input"],
    )
    if payload["item_id"] != identity:
        raise ValueError("item_id does not match the input identity")
    if payload["input_hash"] != input_hash_for(payload["input"]):
        raise ValueError("input_hash does not match the input")
    if payload["result_hash"] != result_hash(payload["result"]):
        raise ValueError("result_hash does not match the result")
    if expected_spec is not None and payload["spec_hash"] != expected_spec:
        raise ValueError("item spec_hash does not match the plan")
    if not isinstance(payload["result"], dict):
        raise ValueError("item result must be an object")


def publish_item(layout: Layout, payload: dict, expected_spec: str | None = None) -> None:
    validate_item_payload(payload, expected_spec)
    atomic_write_json(layout.item_path(payload["item_id"]), payload)


def read_valid_item(layout: Layout, item_id: str, expected_spec: str | None = None) -> dict | None:
    path = layout.item_path(item_id)
    if not path.exists():
        return None
    try:
        payload = read_json(path)
        validate_item_payload(payload, expected_spec)
    except (OSError, ValueError, json.JSONDecodeError):
        return None
    if payload["item_id"] != item_id:
        return None
    return payload


def publish_receipt(layout: Layout, receipt: dict) -> None:
    required = (
        "batch_id",
        "completed_at",
        "completed_item_ids",
        "exit_code",
        "failed_item_ids",
        "planned_item_ids",
        "result_hashes",
        "schema",
        "started_at",
        "wall_seconds",
        "worker_pid",
    )
    if receipt.get("schema") != RECEIPT_SCHEMA:
        raise ValueError("receipt schema is wrong")
    for field in required:
        if field not in receipt:
            raise ValueError(f"receipt is missing {field}")
    path = layout.receipt_path(receipt["batch_id"])
    if path.exists():
        raise ValueError(f"receipt {receipt['batch_id']} already exists")
    atomic_write_json(path, receipt)


def read_receipt(layout: Layout, batch_id: str) -> dict | None:
    path = layout.receipt_path(batch_id)
    if not path.exists():
        return None
    return read_json(path)


def hostname() -> str:
    return socket.gethostname()


def pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def write_status(layout: Layout, payload: dict) -> None:
    payload = dict(payload)
    payload["schema"] = STATUS_SCHEMA
    atomic_write_json(layout.status_path(), payload)


def read_status(layout: Layout) -> dict:
    path = layout.status_path()
    if not path.exists():
        return {}
    return read_json(path)


def write_heartbeat(layout: Layout, payload: dict) -> None:
    atomic_write_json(layout.heartbeat_path(), payload)


def read_heartbeat(layout: Layout) -> dict:
    path = layout.heartbeat_path()
    if not path.exists():
        return {}
    return read_json(path)


def tail_lines(path: Path, count: int) -> list[str]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    return lines[-count:]
