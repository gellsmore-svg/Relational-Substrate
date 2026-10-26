"""Atomic, resumable item store.

A valid completed result is adopted even if the status file was not updated.
A failed or timed-out result stays terminal: resume does not edit it and does
not run it again. Incomplete, partial and invalid records are quarantined
and may be recomputed under the same spec.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


class IncompatiblePlan(RuntimeError):
    """The output directory was opened under a different frozen plan."""


def canonical_bytes(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(payload: dict) -> str:
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def read_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeError):
        return None


TERMINAL = {"complete", "failed", "timeout", "unresolved"}
RERUN = {"pending", "running", "partial", "invalid"}


class Store:
    def __init__(self, root: Path, plan: dict):
        self.root = Path(root)
        self.plan = plan
        self.plan_hash = digest(plan)
        self.items = {item["id"]: item for item in plan["items"]}
        if len(self.items) != len(plan["items"]):
            raise ValueError("item ids are not unique")

    def prepare(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        manifest_path = self.root / "manifest.json"
        if manifest_path.exists():
            manifest = read_json(manifest_path)
            if manifest is None or manifest.get("plan_hash") != self.plan_hash:
                raise IncompatiblePlan(
                    f"{self.root} was written for plan {None if manifest is None else manifest.get('plan_hash')}, "
                    f"not {self.plan_hash}"
                )
            return
        atomic_write(
            manifest_path,
            json.dumps(
                {
                    "plan_hash": self.plan_hash,
                    "round_id": self.plan["round_id"],
                    "engine_version": self.plan["engine_version"],
                },
                sort_keys=True,
            )
            + "\n",
        )

    def item_dir(self, item_id: str) -> Path:
        return self.root / "items" / item_id

    def spec_hash(self, item_id: str) -> str:
        return digest(self.items[item_id])

    def classify(self, item_id: str) -> str:
        directory = self.item_dir(item_id)
        result_path = directory / "result.json"
        if result_path.exists():
            result = read_json(result_path)
            if not self._result_matches(item_id, result):
                return "invalid"
            status = result.get("status")
            if status in TERMINAL:
                return status
            return "invalid"
        if (directory / "result.json.tmp").exists() or (directory / "status.json.tmp").exists():
            return "partial"
        status_path = directory / "status.json"
        if status_path.exists():
            status = read_json(status_path)
            if status is None:
                return "invalid"
            if status.get("status") == "running":
                return "running"
            return "invalid"
        return "pending"

    def _result_matches(self, item_id: str, result: dict | None) -> bool:
        if not isinstance(result, dict):
            return False
        return (
            result.get("item_id") == item_id
            and result.get("plan_hash") == self.plan_hash
            and result.get("spec_hash") == self.spec_hash(item_id)
            and result.get("status") in TERMINAL
        )

    def quarantine(self, item_id: str) -> None:
        directory = self.item_dir(item_id)
        if not directory.exists():
            return
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        destination = directory / "corrupt" / stamp
        destination.mkdir(parents=True, exist_ok=True)
        for child in list(directory.iterdir()):
            if child.name == "corrupt":
                continue
            child.rename(destination / child.name)

    def write_status(self, item_id: str, status: str) -> None:
        atomic_write(
            self.item_dir(item_id) / "status.json",
            json.dumps({"item_id": item_id, "status": status, "plan_hash": self.plan_hash}, sort_keys=True) + "\n",
        )

    def commit_result(self, item_id: str, result: dict) -> None:
        result = dict(result)
        result["item_id"] = item_id
        result["plan_hash"] = self.plan_hash
        result["spec_hash"] = self.spec_hash(item_id)
        result["round_id"] = self.plan["round_id"]
        body = json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n"
        atomic_write(self.item_dir(item_id) / "result.json", body)
        receipt = {
            "item_id": item_id,
            "plan_hash": self.plan_hash,
            "result_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
            "spec_hash": result["spec_hash"],
            "status": result["status"],
        }
        atomic_write(
            self.item_dir(item_id) / "receipt.json",
            json.dumps(receipt, sort_keys=True) + "\n",
        )
        self.write_status(item_id, result["status"])

    def load_result(self, item_id: str) -> dict | None:
        return read_json(self.item_dir(item_id) / "result.json")

    def counts(self) -> dict[str, int]:
        counts = {name: 0 for name in ("complete", "failed", "timeout", "unresolved", "pending", "running", "partial", "invalid")}
        for item_id in self.items:
            counts[self.classify(item_id)] += 1
        return counts
