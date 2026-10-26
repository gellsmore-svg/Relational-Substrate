"""Fault injection for the micro-batch supervisor.

These tests use the fault experiment. They do not solve a scientific kernel.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

from rs_constraint_lab.durable import atomic_write_json
from rs_constraint_lab.faultlab import plan
from rs_constraint_lab.supervisor import supervise, verify_root
from rs_constraint_lab.workstore import Layout, make_item_record, publish_item, read_valid_item, utc_now

PYTHON = sys.executable
LAB = Path(__file__).resolve().parents[1]


def _request(root: Path, items: list[dict], **extra) -> None:
    root.mkdir(parents=True, exist_ok=True)
    payload = {"items": items, "heartbeat_seconds": 0.2, "watchdog_seconds": 30}
    payload.update(extra)
    atomic_write_json(root / "fault-request.json", payload)
    plan(root)


def _run_batch(root: Path, *args: str, timeout: float = 30) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PYTHON, "-m", "rs_constraint_lab", "batch", *args, "--root", str(root)],
        cwd=LAB,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def _start_batch(root: Path, *args: str) -> subprocess.Popen:
    return subprocess.Popen(
        [PYTHON, "-m", "rs_constraint_lab", "batch", *args, "--root", str(root)],
        cwd=LAB,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _wait_for(path: Path, needle: str, timeout: float = 10) -> str:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if path.exists() and needle in path.read_text(encoding="utf-8"):
            return path.read_text(encoding="utf-8")
        time.sleep(0.05)
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    raise AssertionError(f"{needle!r} not seen in {path}: {text[-500:]}")


def _executions(root: Path) -> list[str]:
    path = root / "fault-executions.log"
    if not path.exists():
        return []
    return [line for line in path.read_text(encoding="utf-8").splitlines() if line]


def test_atomic_item_ignores_partial_write(tmp_path: Path) -> None:
    layout = Layout(tmp_path)
    layout.ensure()
    record = make_item_record("fault-spec", "fault-1", "fault-1", "fault", {"behavior": "ok", "key": "a", "seconds": 0, "spawn": False})
    temporary = layout.item_path(record["item_id"]).with_name(layout.item_path(record["item_id"]).name + ".tmp")
    temporary.write_text("{not json", encoding="utf-8")
    assert read_valid_item(layout, record["item_id"], "fault-spec") is None
    publish_item(
        layout,
        {
            "analysis_version": record["analysis_version"],
            "completed_at": utc_now(),
            "input": record["input"],
            "input_hash": record["input_hash"],
            "item_id": record["item_id"],
            "kind": record["kind"],
            "result": {"key": "a", "ok": True, "solver_residuals": {}},
            "result_hash": __import__("rs_constraint_lab.workstore", fromlist=["result_hash"]).result_hash(
                {"key": "a", "ok": True, "solver_residuals": {}}
            ),
            "schema": "rs-constraint-lab.item/v1",
            "semantic_version": record["semantic_version"],
            "solver_residuals": {},
            "spec_hash": record["spec_hash"],
            "started_at": utc_now(),
        },
        "fault-spec",
    )
    assert read_valid_item(layout, record["item_id"], "fault-spec") is not None
    assert not temporary.exists()


def test_completed_item_is_not_recomputed(tmp_path: Path) -> None:
    _request(tmp_path, [{"behavior": "ok", "key": "a"}, {"behavior": "ok", "key": "b"}])
    first = supervise(tmp_path, workers=1, batch_size=2, heartbeat=0.2, watchdog=10)
    assert first["state"] == "COMPLETE"
    before = list(_executions(tmp_path))
    hashes = {path.name: path.read_bytes() for path in (tmp_path / "items").glob("*.json")}
    second = supervise(tmp_path, workers=1, batch_size=2, heartbeat=0.2, watchdog=10)
    assert second["state"] == "COMPLETE"
    assert _executions(tmp_path) == before
    after = {path.name: path.read_bytes() for path in (tmp_path / "items").glob("*.json")}
    assert after == hashes


def test_receipt_and_verify(tmp_path: Path) -> None:
    _request(tmp_path, [{"behavior": "ok", "key": "a"}])
    supervise(tmp_path, workers=1, batch_size=1, heartbeat=0.2, watchdog=10)
    report = verify_root(tmp_path)
    assert report["ok"] is True
    assert report["receipts"] == 1
    receipt = json.loads(next((tmp_path / "receipts").glob("*.json")).read_text(encoding="utf-8"))
    assert receipt["exit_code"] == 0
    assert receipt["completed_item_ids"]


def test_timeout_kills_process_tree_and_splits(tmp_path: Path) -> None:
    _request(
        tmp_path,
        [
            {"behavior": "spawn_sleep", "key": "slow", "seconds": 30, "spawn": True},
            {"behavior": "ok", "key": "later"},
        ],
        watchdog_seconds=2,
    )
    supervise(tmp_path, workers=1, batch_size=2, heartbeat=0.2, watchdog=2, max_batches=1, max_attempts=3)
    child = json.loads((tmp_path / "fault-children" / "slow.json").read_text(encoding="utf-8"))
    assert _alive(child["pid"]) is False
    log = (tmp_path / "progress" / "progress.log").read_text(encoding="utf-8")
    assert "TIMEOUT" in log
    assert "SPLIT" in log or "action=split" in log


def test_repeated_single_item_timeout_quarantines(tmp_path: Path) -> None:
    _request(tmp_path, [{"behavior": "sleep", "key": "stuck", "seconds": 30}], watchdog_seconds=1)
    payload = supervise(tmp_path, workers=1, batch_size=4, heartbeat=0.2, watchdog=1, max_attempts=3, max_wall=20)
    assert payload["quarantined_items"] == 1
    assert payload["state"] == "PARTIAL"
    log = (tmp_path / "progress" / "progress.log").read_text(encoding="utf-8")
    assert "QUARANTINE" in log


def test_killed_worker_is_rescheduled(tmp_path: Path) -> None:
    _request(tmp_path, [{"behavior": "sleep", "key": "slow", "seconds": 30}], heartbeat_seconds=0.2, watchdog_seconds=30)
    proc = _start_batch(tmp_path, "supervise", "--workers", "1", "--batch-size", "1", "--max-wall", "20", "--heartbeat", "0.2", "--watchdog", "30")
    try:
        heartbeat = _wait_json(tmp_path / "progress" / "heartbeat.json", "worker_pid", timeout=10)
        worker_pid = heartbeat["worker_pid"]
        assert worker_pid
        assert proc.poll() is None
        os.kill(worker_pid, 9)
        _wait_for(tmp_path / "progress" / "progress.log", "FAIL", timeout=10)
        assert proc.poll() is None
        fresh = json.loads((tmp_path / "progress" / "heartbeat.json").read_text(encoding="utf-8"))
        assert fresh["supervisor_pid"] == proc.pid or _alive(proc.pid)
    finally:
        # The replacement batch is a 30s sleeper. Graceful stop waits for it.
        # This test has already checked survival. Cleanup must not wait that out.
        if proc.poll() is None:
            proc.kill()
            proc.wait(timeout=5)


def test_running_batches_lists_each_live_worker(tmp_path: Path) -> None:
    from rs_constraint_lab.supervisor import build_status

    layout = Layout(tmp_path)
    layout.ensure()
    atomic_write_json(layout.manifest_path(), {"experiment_id": "fault", "spec_hash": "fault-spec", "watchdog_seconds": 30})
    payload = build_status(
        layout,
        supervisor_pid=1,
        phase="01_COARSE",
        state_name="RUNNING",
        current=None,
        started_at="2026-10-12T00:00:00Z",
        last_error=None,
        running=[
            {"batch_id": "000001", "items": 2, "pid": 11, "started_at": "2026-10-12T00:00:01Z", "started_epoch": time.time()},
            {"batch_id": "000002", "items": 3, "pid": 12, "started_at": "2026-10-12T00:00:02Z", "started_epoch": time.time()},
        ],
    )
    assert [row["batch_id"] for row in payload["running_batches"]] == ["000001", "000002"]
    assert [row["worker_pid"] for row in payload["running_batches"]] == [11, 12]
    assert [row["items"] for row in payload["running_batches"]] == [2, 3]
    assert payload["current_batch_id"] == "000001"
    assert payload["watchdog_seconds"] == 30
    _request(
        tmp_path / "live",
        [
            {"behavior": "sleep", "key": "a", "seconds": 3},
            {"behavior": "sleep", "key": "b", "seconds": 3},
        ],
        heartbeat_seconds=0.2,
        watchdog_seconds=30,
    )
    proc = _start_batch(
        tmp_path / "live",
        "supervise",
        "--workers",
        "2",
        "--batch-size",
        "1",
        "--heartbeat",
        "0.2",
        "--watchdog",
        "30",
        "--max-wall",
        "12",
    )
    try:
        deadline = time.time() + 10
        seen = None
        while time.time() < deadline:
            path = tmp_path / "live" / "progress" / "status.json"
            if path.exists():
                seen = json.loads(path.read_text(encoding="utf-8"))
                if len(seen.get("running_batches") or []) >= 2:
                    break
            time.sleep(0.05)
        assert seen is not None
        rows = seen["running_batches"]
        assert len(rows) == 2
        assert seen["current_batch_id"] == rows[0]["batch_id"]
        assert len({row["worker_pid"] for row in rows}) == 2
        for row in rows:
            assert row["items"] == 1
            assert row["watchdog_seconds"] == 30
            assert row["started_at"]
            assert row["elapsed_seconds"] is not None
    finally:
        if proc.poll() is None:
            proc.send_signal(15)
            proc.wait(timeout=20)


def test_status_is_visible_before_the_heartbeat_interval(tmp_path: Path) -> None:
    _request(tmp_path, [{"behavior": "sleep", "key": "slow", "seconds": 2}], heartbeat_seconds=5, watchdog_seconds=30)
    proc = _start_batch(tmp_path, "supervise", "--workers", "1", "--batch-size", "1", "--heartbeat", "5", "--watchdog", "30", "--max-wall", "8")
    try:
        status = _wait_json(tmp_path / "progress" / "status.json", "state", timeout=1)
        assert status["state"] == "RUNNING"
        assert status["phase"]
        assert status["supervisor_pid"] == proc.pid
    finally:
        proc.send_signal(15)
        proc.wait(timeout=20)


def test_heartbeat_moves_while_worker_is_busy(tmp_path: Path) -> None:
    _request(tmp_path, [{"behavior": "sleep", "key": "slow", "seconds": 3}], heartbeat_seconds=0.2, watchdog_seconds=10)
    proc = _start_batch(tmp_path, "supervise", "--workers", "1", "--batch-size", "1", "--heartbeat", "0.2", "--watchdog", "10", "--max-wall", "10")
    try:
        first = _wait_json(tmp_path / "progress" / "heartbeat.json", "worker_pid", timeout=10)
        time.sleep(0.6)
        second = json.loads((tmp_path / "progress" / "heartbeat.json").read_text(encoding="utf-8"))
        assert second["worker_elapsed_seconds"] > first["worker_elapsed_seconds"]
        assert second["supervisor_pid"] != second["worker_pid"]
        status = json.loads((tmp_path / "progress" / "status.json").read_text(encoding="utf-8"))
        assert status["current_batch_elapsed_seconds"] is not None
        assert status["state"] == "RUNNING"
    finally:
        proc.wait(timeout=15)


def test_progress_log_records_batch_lifecycle(tmp_path: Path) -> None:
    _request(tmp_path, [{"behavior": "ok", "key": "a"}])
    supervise(tmp_path, workers=1, batch_size=1, heartbeat=0.2, watchdog=10)
    log = (tmp_path / "progress" / "progress.log").read_text(encoding="utf-8")
    assert "START" in log
    assert "BATCH" in log and "COMPLETE" in log
    events = (tmp_path / "progress" / "events.jsonl").read_text(encoding="utf-8")
    assert "batch_complete" in events


def test_status_watch_prints(tmp_path: Path) -> None:
    _request(tmp_path, [{"behavior": "ok", "key": "a"}])
    supervise(tmp_path, workers=1, batch_size=1, heartbeat=0.2, watchdog=10)
    completed = _run_batch(tmp_path, "status", "--watch", "0.1", "--max-snapshots", "2", timeout=10)
    assert completed.returncode == 0
    assert "State:" in completed.stdout
    assert completed.stdout.count("State:") >= 2


def test_graceful_stop(tmp_path: Path) -> None:
    _request(tmp_path, [{"behavior": "sleep", "key": f"s{i}", "seconds": 1} for i in range(4)], watchdog_seconds=10)
    proc = _start_batch(tmp_path, "supervise", "--workers", "1", "--batch-size", "1", "--heartbeat", "0.2", "--watchdog", "10", "--max-wall", "30")
    try:
        _wait_for(tmp_path / "progress" / "progress.log", "BATCH", timeout=10)
        stopped = _run_batch(tmp_path, "stop", timeout=10)
        assert stopped.returncode == 0
        proc.wait(timeout=15)
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait(timeout=5)
    status = json.loads((tmp_path / "progress" / "status.json").read_text(encoding="utf-8"))
    assert status["state"] == "STOPPED"
    # The lock is released, so a new supervisor is accepted.
    follow = supervise(tmp_path, workers=1, batch_size=1, heartbeat=0.2, watchdog=10, max_wall=8)
    assert follow["state"] in {"STOPPED", "COMPLETE"}


def test_duplicate_supervisor_is_refused(tmp_path: Path) -> None:
    _request(tmp_path, [{"behavior": "sleep", "key": "slow", "seconds": 10}], watchdog_seconds=20)
    proc = _start_batch(tmp_path, "supervise", "--workers", "1", "--batch-size", "1", "--heartbeat", "0.2", "--watchdog", "20", "--max-wall", "15")
    try:
        _wait_json(tmp_path / "progress" / "supervisor.lock", "pid", timeout=10)
        second = _run_batch(tmp_path, "supervise", "--workers", "1", "--max-wall", "2", "--heartbeat", "0.2", "--watchdog", "20", timeout=10)
        assert second.returncode == 2
        assert "already running" in second.stderr
    finally:
        proc.send_signal(15)
        proc.wait(timeout=20)


def test_stale_lock_is_recovered(tmp_path: Path) -> None:
    _request(tmp_path, [{"behavior": "ok", "key": "a"}])
    atomic_write_json(
        tmp_path / "progress" / "supervisor.lock",
        {"hostname": "old", "last_heartbeat": utc_now(), "pid": 2**22, "spec_hash": "fault-spec", "started_at": utc_now()},
    )
    payload = supervise(tmp_path, workers=1, batch_size=1, heartbeat=0.2, watchdog=10)
    assert payload["state"] == "COMPLETE"
    log = (tmp_path / "progress" / "progress.log").read_text(encoding="utf-8")
    assert "STALE LOCK" in log


def test_merge_is_restartable(tmp_path: Path) -> None:
    _request(tmp_path, [{"behavior": "ok", "key": "a"}, {"behavior": "ok", "key": "b"}])
    supervise(tmp_path, workers=1, batch_size=2, heartbeat=0.2, watchdog=10)
    from rs_constraint_lab.faultlab import merge_items

    first = merge_items(tmp_path)
    row_bytes = {path.name: path.read_bytes() for path in (tmp_path / "merge" / "items").glob("*.json")}
    (tmp_path / "merge" / "summary.json").unlink()
    one = next((tmp_path / "merge" / "items").glob("*.json"))
    one.unlink()
    second = merge_items(tmp_path)
    assert [row["result_hash"] for row in first["items"]] == [row["result_hash"] for row in second["items"]]
    restored = {path.name: path.read_bytes() for path in (tmp_path / "merge" / "items").glob("*.json")}
    assert restored.keys() == row_bytes.keys()
    for name, blob in row_bytes.items():
        if name != one.name:
            assert restored[name] == blob


def test_verify_detects_missing_item_and_duplicate(tmp_path: Path) -> None:
    _request(tmp_path, [{"behavior": "ok", "key": "a"}])
    supervise(tmp_path, workers=1, batch_size=1, heartbeat=0.2, watchdog=10)
    item = next((tmp_path / "items").glob("*.json"))
    item.unlink()
    report = verify_root(tmp_path)
    assert report["ok"] is False
    assert report["missing_completed"] or any("missing" in problem for problem in report["problems"])
    line = (tmp_path / "plan" / "work-items.jsonl").read_text(encoding="utf-8").splitlines()[0]
    with (tmp_path / "plan" / "work-items.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
    again = verify_root(tmp_path)
    assert any("duplicate" in problem for problem in again["problems"])


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _wait_json(path: Path, field: str, timeout: float) -> dict:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if path.exists():
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                payload = {}
            if payload.get(field):
                return payload
        time.sleep(0.05)
    raise AssertionError(f"{field} not published in {path}")
