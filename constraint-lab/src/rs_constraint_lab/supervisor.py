"""Micro-batch supervisor.

The supervisor owns scheduling, heartbeat, watchdog, retries, splitting,
quarantine, status, and receipts. A worker owns one batch and then exits.
No scientific run is a single long-lived process.
"""

from __future__ import annotations

import importlib
import json
import os
import shutil
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

from rs_constraint_lab.durable import atomic_write_json, read_json
from rs_constraint_lab.version import EXECUTION_BOUNDS
from rs_constraint_lab.workstore import (
    ITEM_SCHEMA,
    RECEIPT_SCHEMA,
    Layout,
    append_jsonl,
    hostname,
    load_state,
    load_work_items,
    log_event,
    log_progress,
    pid_alive,
    publish_item,
    publish_receipt,
    read_heartbeat,
    read_receipt,
    read_status,
    read_valid_item,
    result_hash,
    save_state,
    tail_lines,
    utc_now,
    work_index,
    write_heartbeat,
    write_status,
)

DEFAULT_WATCHDOG = 120.0
DEFAULT_HEARTBEAT = 10.0
DEFAULT_WORKERS = 2
DEFAULT_ATTEMPTS = 3
THREAD_ENV = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")


class DuplicateSupervisor(RuntimeError):
    pass


class ExperimentIncomplete(RuntimeError):
    pass


def _import_executor(dotted: str):
    module_name, function_name = dotted.split(":")
    module = importlib.import_module(module_name)
    return getattr(module, function_name)


def _thread_env() -> dict[str, str]:
    env = os.environ.copy()
    for name in THREAD_ENV:
        env[name] = "1"
    return env


def _load_manifest(layout: Layout) -> dict:
    return read_json(layout.manifest_path())


def _save_manifest(layout: Layout, manifest: dict) -> None:
    atomic_write_json(layout.manifest_path(), manifest)


def ensure_planned(layout: Layout, record: dict) -> bool:
    """Append a work item once. Return True when the item is new."""
    existing = work_index(layout)
    if record["item_id"] in existing:
        return False
    append_jsonl(layout.work_items_path(), record)
    state = load_state(layout)
    state.setdefault(
        record["item_id"],
        {"attempts": 0, "kind": record["kind"], "last_error": None, "status": "pending", "timeouts": 0},
    )
    save_state(layout, state)
    return True


def reconcile(layout: Layout) -> dict:
    """Rebuild item status from files. Valid items are not recomputed."""
    manifest = _load_manifest(layout)
    spec_hash = manifest["spec_hash"]
    state = load_state(layout)
    items = load_work_items(layout)
    for record in items:
        slot = state.setdefault(
            record["item_id"],
            {"attempts": 0, "kind": record["kind"], "last_error": None, "status": "pending", "timeouts": 0},
        )
        slot["kind"] = record["kind"]
        if slot.get("status") == "quarantined":
            continue
        valid = read_valid_item(layout, record["item_id"], spec_hash)
        if valid is not None:
            slot["status"] = "complete"
            slot["last_error"] = None
        elif slot.get("status") == "complete":
            slot["status"] = "pending"
    # A running batch without a receipt keeps its valid items and returns the rest.
    running = layout.batches() / "running"
    if running.exists():
        for batch_dir in sorted(path for path in running.iterdir() if path.is_dir()):
            _recover_running_batch(layout, batch_dir.name, spec_hash, state)
    save_state(layout, state)
    return state


def _recover_running_batch(layout: Layout, batch_id: str, spec_hash: str, state: dict) -> None:
    if read_receipt(layout, batch_id) is not None:
        _move_batch(layout, batch_id, "running", "complete")
        return
    batch_path = layout.batch_dir("running", batch_id) / "batch.json"
    if not batch_path.exists():
        return
    batch = read_json(batch_path)
    missing = []
    for item_id in batch["item_ids"]:
        if read_valid_item(layout, item_id, spec_hash) is None:
            missing.append(item_id)
            slot = state.setdefault(item_id, {"attempts": 0, "kind": "unknown", "last_error": None, "status": "pending", "timeouts": 0})
            if slot.get("status") != "quarantined":
                slot["status"] = "pending"
    log_event(
        layout,
        "batch_recovered",
        f"running batch {batch_id} had no receipt; {len(missing)} items return to the queue",
        batch_id=batch_id,
        counts={"missing": len(missing), "planned": len(batch["item_ids"])},
    )
    log_progress(layout, f"RECOVER batch {batch_id} missing={len(missing)} kept={len(batch['item_ids']) - len(missing)}")
    _move_batch(layout, batch_id, "running", "failed")
    if missing:
        _queue_split(layout, missing, state, reason="recovered running batch")


def _move_batch(layout: Layout, batch_id: str, source: str, dest: str) -> None:
    src = layout.batch_dir(source, batch_id)
    if not src.exists():
        return
    dst = layout.batch_dir(dest, batch_id)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        shutil.rmtree(dst)
    shutil.move(str(src), str(dst))


def _next_batch_id(layout: Layout) -> str:
    path = layout.batch_seq_path()
    current = 0 if not path.exists() else int(read_json(path)["next"])
    current += 1
    atomic_write_json(path, {"next": current})
    return f"{current:06d}"


def _policy_size(layout: Layout, kind: str, override: int | None) -> int:
    if override is not None:
        return max(1, int(override))
    path = layout.policy_path()
    if not path.exists():
        return 1
    policy = read_json(path)
    kinds = policy.get("kinds", {})
    row = kinds.get(kind) or kinds.get("default") or {"items": 1}
    return max(1, int(row.get("items", 1)))


def _queue_split(layout: Layout, item_ids: list[str], state: dict, reason: str) -> None:
    if not item_ids:
        return
    if len(item_ids) == 1:
        _requeue(layout, item_ids, state, reason=reason)
        return
    midpoint = (len(item_ids) + 1) // 2
    _place_batch(layout, item_ids[:midpoint], forced=True)
    _place_batch(layout, item_ids[midpoint:], forced=True)
    log_event(layout, "batch_split", reason, counts={"remaining": len(item_ids), "left": midpoint, "right": len(item_ids) - midpoint})
    log_progress(layout, f"SPLIT remaining={len(item_ids)} left={midpoint} right={len(item_ids) - midpoint} reason={reason}")


def _requeue(layout: Layout, item_ids: list[str], state: dict, reason: str) -> None:
    del reason
    for item_id in item_ids:
        slot = state.setdefault(item_id, {"attempts": 0, "kind": "unknown", "last_error": None, "status": "pending", "timeouts": 0})
        if slot.get("status") != "quarantined":
            slot["status"] = "pending"
    save_state(layout, state)


def _place_batch(layout: Layout, item_ids: list[str], *, forced: bool) -> str:
    batch_id = _next_batch_id(layout)
    payload = {"batch_id": batch_id, "forced": forced, "item_ids": list(item_ids), "queued_at": utc_now()}
    dest = layout.batch_dir("planned", batch_id)
    dest.mkdir(parents=True, exist_ok=True)
    atomic_write_json(dest / "batch.json", payload)
    return batch_id


def _reserved_ids(layout: Layout) -> set[str]:
    reserved = set()
    for state_name in ("planned", "running"):
        folder = layout.batches() / state_name
        if not folder.exists():
            continue
        for batch_dir in folder.iterdir():
            path = batch_dir / "batch.json"
            if path.exists():
                reserved.update(read_json(path)["item_ids"])
    return reserved


def _fill_batches(layout: Layout, state: dict, *, workers: int, batch_size: int | None) -> None:
    planned = list((layout.batches() / "planned").iterdir()) if (layout.batches() / "planned").exists() else []
    running = list((layout.batches() / "running").iterdir()) if (layout.batches() / "running").exists() else []
    open_count = len([path for path in planned if path.is_dir()]) + len([path for path in running if path.is_dir()])
    if open_count >= workers:
        return
    reserved = _reserved_ids(layout)
    pending = []
    index = work_index(layout)
    for item_id, slot in state.items():
        if slot.get("status") != "pending" or item_id in reserved or item_id not in index:
            continue
        pending.append(index[item_id])
    pending.sort(key=lambda row: (row["kind"], row["item_id"]))
    singles = [row for row in pending if state.get(row["item_id"], {}).get("force_single")]
    while singles and open_count < workers:
        _place_batch(layout, [singles[0]["item_id"]], forced=True)
        pending = [row for row in pending if row["item_id"] != singles[0]["item_id"]]
        singles = singles[1:]
        open_count += 1
    while pending and open_count < workers:
        kind = pending[0]["kind"]
        group = [row for row in pending if row["kind"] == kind]
        size = _policy_size(layout, kind, batch_size)
        chosen = group[:size]
        _place_batch(layout, [row["item_id"] for row in chosen], forced=False)
        chosen_ids = {row["item_id"] for row in chosen}
        pending = [row for row in pending if row["item_id"] not in chosen_ids]
        open_count += 1


def _launch_worker(layout: Layout, batch_id: str) -> subprocess.Popen:
    src = layout.batch_dir("planned", batch_id)
    batch = read_json(src / "batch.json")
    dest = layout.batch_dir("running", batch_id)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.move(str(src), str(dest))
    command = [
        sys.executable,
        "-m",
        "rs_constraint_lab",
        "worker",
        "--root",
        str(layout.root),
        "--batch",
        batch_id,
    ]
    popen_kwargs = {
        "args": command,
        "cwd": str(Path(__file__).resolve().parents[2]),
        "env": _thread_env(),
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.DEVNULL,
        "stderr": (dest / "worker.err").open("wb"),
    }
    if os.name == "nt":
        popen_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP  # type: ignore[attr-defined]
    else:
        popen_kwargs["start_new_session"] = True
    process = subprocess.Popen(**popen_kwargs)
    atomic_write_json(
        dest / "worker.json",
        {"batch_id": batch_id, "pid": process.pid, "started_at": utc_now(), "started_epoch": time.time()},
    )
    log_event(layout, "batch_start", f"batch {batch_id} started", batch_id=batch_id, counts={"items": len(batch["item_ids"])})
    log_progress(layout, f"BATCH {batch_id} START items={len(batch['item_ids'])}")
    return process


def kill_process_tree(pid: int, *, grace: float = 1.0) -> None:
    """Stop a worker and every descendant. A timed-out parent must not leave solvers behind."""
    if pid <= 0 or not pid_alive(pid):
        return
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return
    try:
        group = os.getpgid(pid)
    except ProcessLookupError:
        return
    try:
        os.killpg(group, signal.SIGTERM)
    except ProcessLookupError:
        return
    deadline = time.time() + grace
    while time.time() < deadline and pid_alive(pid):
        time.sleep(0.05)
    if pid_alive(pid):
        try:
            os.killpg(group, signal.SIGKILL)
        except ProcessLookupError:
            return


def _harvest(layout: Layout, batch_id: str, process: subprocess.Popen, started: float, *, timed_out: bool, max_attempts: int) -> dict:
    if process.poll() is None:
        kill_process_tree(process.pid)
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
    stderr = ""
    if process.stderr is not None:
        process.stderr.close()
    err_path = layout.batch_dir("running", batch_id) / "worker.err"
    if err_path.exists():
        stderr = err_path.read_text(encoding="utf-8", errors="replace")[-2000:]
    exit_code = process.returncode if process.returncode is not None else -9
    manifest = _load_manifest(layout)
    batch = read_json(layout.batch_dir("running", batch_id) / "batch.json")
    state = load_state(layout)
    completed = []
    failed = []
    hashes = {}
    for item_id in batch["item_ids"]:
        valid = read_valid_item(layout, item_id, manifest["spec_hash"])
        state.setdefault(item_id, {"attempts": 0, "kind": "unknown", "last_error": None, "status": "pending", "timeouts": 0})
        if valid is not None:
            state[item_id]["status"] = "complete"
            state[item_id]["last_error"] = None
            completed.append(item_id)
            hashes[item_id] = valid["result_hash"]
        else:
            failed.append(item_id)
    # A multi-item timeout must not spend the retries of items that merely
    # sat behind a slow neighbour. A one-item timeout does.
    single_timeout = timed_out and len(failed) == 1
    unfinished = []
    for item_id in failed:
        slot = state[item_id]
        error_path = layout.batch_dir("running", batch_id) / "errors" / f"{item_id}.json"
        message = "worker ended before this item was published"
        if error_path.exists():
            message = read_json(error_path).get("message", message)
        elif timed_out:
            message = "batch watchdog expired"
        elif stderr:
            message = stderr.strip().splitlines()[-1]
        count_attempt = bool(error_path.exists()) or not timed_out or single_timeout
        if count_attempt:
            slot["attempts"] = int(slot.get("attempts", 0)) + 1
        if timed_out:
            slot["timeouts"] = int(slot.get("timeouts", 0)) + 1
        slot["last_error"] = message
        if count_attempt and slot["attempts"] >= max_attempts:
            slot["status"] = "quarantined"
            log_event(layout, "quarantine", message, batch_id=batch_id, item_id=item_id)
            log_progress(layout, f"QUARANTINE item={item_id} attempts={slot['attempts']} error={message}")
        else:
            slot["status"] = "pending"
            if single_timeout:
                slot["force_single"] = True
            unfinished.append(item_id)
    receipt = {
        "batch_id": batch_id,
        "completed_at": utc_now(),
        "completed_item_ids": completed,
        "exit_code": exit_code,
        "failed_item_ids": [item_id for item_id in batch["item_ids"] if item_id not in completed],
        "planned_item_ids": list(batch["item_ids"]),
        "result_hashes": hashes,
        "schema": RECEIPT_SCHEMA,
        "started_at": read_json(layout.batch_dir("running", batch_id) / "worker.json")["started_at"],
        "stderr_tail": stderr,
        "timed_out": timed_out,
        "wall_seconds": round(time.time() - started, 6),
        "worker_pid": process.pid,
    }
    publish_receipt(layout, receipt)
    dest = "failed" if timed_out or unfinished or failed else "complete"
    if timed_out:
        log_event(layout, "batch_timeout", "watchdog expired", batch_id=batch_id, counts={"completed": len(completed), "remaining": len(unfinished)})
        log_progress(layout, f"BATCH {batch_id} TIMEOUT completed={len(completed)} remaining={len(unfinished)} action=split")
        _queue_split(layout, unfinished, state, reason="watchdog")
    elif unfinished:
        log_event(layout, "batch_failed", "batch ended with missing items", batch_id=batch_id, counts={"completed": len(completed), "failed": len(unfinished)})
        log_progress(layout, f"BATCH {batch_id} FAIL completed={len(completed)} failed={len(unfinished)}")
        for item_id in unfinished:
            if state[item_id]["status"] == "pending":
                pass
        save_state(layout, state)
    else:
        save_state(layout, state)
        _log_complete(layout, batch_id, len(completed))
    save_state(layout, state)
    _move_batch(layout, batch_id, "running", dest if not timed_out else "failed")
    return receipt


def _log_complete(layout: Layout, batch_id: str, items: int) -> None:
    state = load_state(layout)
    total = len(state)
    done = sum(1 for slot in state.values() if slot.get("status") == "complete")
    receipts = _receipts(layout)
    elapsed = sum(float(row.get("wall_seconds") or 0.0) for row in receipts) or 1e-9
    produced = sum(len(row.get("completed_item_ids") or []) for row in receipts)
    rate = produced / elapsed
    pending = sum(1 for slot in state.values() if slot.get("status") == "pending")
    eta = _format_eta(pending / rate if rate else None)
    log_event(layout, "batch_complete", f"batch {batch_id} complete", batch_id=batch_id, counts={"items": items, "completed": done, "planned": total})
    log_progress(layout, f"BATCH {batch_id} COMPLETE items={items} total={done}/{total} rate={rate:.2f}/s eta_current={eta}")


def _format_eta(seconds: float | None) -> str:
    if seconds is None:
        return "unknown"
    seconds = max(0, int(seconds))
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def _receipts(layout: Layout) -> list[dict]:
    folder = layout.receipts()
    if not folder.exists():
        return []
    rows = []
    for path in sorted(folder.glob("*.json")):
        rows.append(read_json(path))
    return rows


def _counts(layout: Layout, state: dict) -> dict:
    values = list(state.values())
    return {
        "completed_items": sum(1 for slot in values if slot.get("status") == "complete"),
        "failed_items": sum(1 for slot in values if slot.get("status") == "pending" and slot.get("last_error")),
        "pending_items": sum(1 for slot in values if slot.get("status") == "pending"),
        "planned_items_current": len(values),
        "quarantined_items": sum(1 for slot in values if slot.get("status") == "quarantined"),
        "running_items": _running_item_count(layout),
    }


def _visible_error(state: dict) -> str | None:
    for item_id, slot in state.items():
        if slot.get("last_error") and slot.get("status") in {"pending", "quarantined"}:
            return f"item={item_id} status={slot.get('status')} error={slot.get('last_error')}"
    return None


def _running_item_count(layout: Layout) -> int:
    folder = layout.batches() / "running"
    if not folder.exists():
        return 0
    total = 0
    for batch_dir in folder.iterdir():
        path = batch_dir / "batch.json"
        if path.exists():
            total += len(read_json(path)["item_ids"])
    return total


def _experiment_counts(layout: Layout) -> dict:
    manifest = _load_manifest(layout)
    dotted = manifest.get("counts")
    if not dotted:
        return {
            "cache_hits": 0,
            "cache_misses": 0,
            "calibrations_complete": 0,
            "calibrations_total": 0,
            "calibrations_unresolved": 0,
        }
    function = _import_executor(dotted)
    return function(layout.root)


def build_status(layout: Layout, *, supervisor_pid: int | None, phase: str, state_name: str, current: dict | None, started_at: str, last_error: str | None) -> dict:
    state = load_state(layout)
    counts = _counts(layout, state)
    extra = _experiment_counts(layout) if layout.manifest_path().exists() else {}
    heartbeat = read_heartbeat(layout)
    age = None
    if heartbeat.get("timestamp"):
        age = max(0.0, (time.time() - _epoch(heartbeat["timestamp"])))
    receipts = _receipts(layout)
    produced = sum(len(row.get("completed_item_ids") or []) for row in receipts)
    walls = [float(row["wall_seconds"]) for row in receipts if row.get("wall_seconds") is not None]
    runtime = None
    if layout.progress().joinpath("run-started.json").exists():
        runtime = time.time() - float(read_json(layout.progress() / "run-started.json")["epoch"])
    rate = produced / runtime if runtime and runtime > 0 else 0.0
    recent_receipts = receipts[-3:]
    recent_items = sum(len(row.get("completed_item_ids") or []) for row in recent_receipts)
    recent_wall = sum(float(row.get("wall_seconds") or 0.0) for row in recent_receipts)
    recent_rate = recent_items / recent_wall if recent_wall else 0.0
    remaining = counts["pending_items"] / recent_rate if recent_rate else None
    completion = None
    if remaining is not None:
        completion = utc_now_plus(remaining)
    manifest = _load_manifest(layout) if layout.manifest_path().exists() else {}
    visible = _visible_error(state)
    if visible:
        last_error = visible
    return {
        "cache_hits": extra.get("cache_hits", 0),
        "cache_misses": extra.get("cache_misses", 0),
        "calibrations_complete": extra.get("calibrations_complete", 0),
        "calibrations_total": extra.get("calibrations_total", 0),
        "calibrations_unresolved": extra.get("calibrations_unresolved", 0),
        "completed_batches": sum(1 for row in receipts if not row.get("timed_out") and not row.get("failed_item_ids")),
        "completed_items": counts["completed_items"],
        "current_batch_elapsed_seconds": None if current is None else round(time.time() - current["started_epoch"], 3),
        "current_batch_id": None if current is None else current["batch_id"],
        "current_batch_items": 0 if current is None else current["items"],
        "estimated_completion_time": completion,
        "estimated_remaining_seconds": None if remaining is None else round(remaining, 3),
        "eta_label": "ETA for current plan",
        "experiment_id": manifest.get("experiment_id"),
        "failed_items": counts["failed_items"],
        "heartbeat_age_seconds": None if age is None else round(age, 3),
        "items_per_second": round(rate, 6),
        "last_activity_at": utc_now(),
        "last_error": last_error,
        "pending_items": counts["pending_items"],
        "phase": phase,
        "planned_items_current": counts["planned_items_current"],
        "quarantined_items": counts["quarantined_items"],
        "recent_items_per_second": round(recent_rate, 6),
        "retried_batches": sum(1 for row in receipts if row.get("failed_item_ids")),
        "running_items": counts["running_items"],
        "spec_hash": manifest.get("spec_hash"),
        "started_at": started_at,
        "state": state_name,
        "supervisor_pid": supervisor_pid,
        "timed_out_batches": sum(1 for row in receipts if row.get("timed_out")),
        "watchdog_seconds": manifest.get("watchdog_seconds", DEFAULT_WATCHDOG),
    }


def utc_now_plus(seconds: float) -> str:
    from datetime import datetime, timedelta, timezone

    moment = datetime.now(timezone.utc) + timedelta(seconds=seconds)
    return moment.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _epoch(text: str) -> float:
    from datetime import datetime

    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    return datetime.fromisoformat(text).timestamp()


def format_status(payload: dict, *, last_progress: str | None = None) -> str:
    elapsed = payload.get("current_batch_elapsed_seconds")
    watchdog = payload.get("watchdog_seconds") or DEFAULT_WATCHDOG
    worker_line = "idle" if elapsed is None else f"{int(elapsed)}s / {int(watchdog)}s"
    eta = payload.get("estimated_remaining_seconds")
    eta_text = "unknown" if eta is None else _format_eta(eta)
    heartbeat = payload.get("heartbeat_age_seconds")
    heartbeat_text = "unknown" if heartbeat is None else f"{int(heartbeat)}s ago"
    lines = [
        f"Generation {payload.get('experiment_id')}",
        f"State: {payload.get('state')}",
        f"Phase: {payload.get('phase')}",
        f"Batch: {payload.get('current_batch_id') or '-'}",
        f"Worker: {worker_line}",
        f"Items: {payload.get('completed_items')} complete / {payload.get('planned_items_current')} currently planned",
        f"Calibrations: {payload.get('calibrations_complete')} / {payload.get('calibrations_total')} complete",
        f"Failures: {payload.get('failed_items')}",
        f"Timeouts: {payload.get('timed_out_batches')}",
        f"Quarantined: {payload.get('quarantined_items')}",
        f"Recent rate: {payload.get('recent_items_per_second')} items/s",
        f"ETA current plan: {eta_text}",
        f"Heartbeat: {heartbeat_text}",
        f"Last progress: {last_progress or '-'}",
        f"Last error: {payload.get('last_error') or '-'}",
    ]
    return "\n".join(lines)


def _phase(layout: Layout) -> str:
    manifest = _load_manifest(layout)
    dotted = manifest.get("phase")
    if not dotted:
        return "01_INFRASTRUCTURE"
    return _import_executor(dotted)(layout.root)


def _advance(layout: Layout) -> int:
    manifest = _load_manifest(layout)
    dotted = manifest.get("advance")
    if not dotted:
        return 0
    return int(_import_executor(dotted)(layout.root))


class _Lock:
    def __init__(self, layout: Layout, spec_hash: str):
        self.layout = layout
        self.spec_hash = spec_hash
        self.handle = None
        self.held = False

    def acquire(self) -> None:
        path = self.layout.lock_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        # r+ replaces the inode in place. Append mode would ignore seek() and
        # glue a second JSON object onto the lock on every heartbeat.
        path.touch(exist_ok=True)
        self.handle = path.open("r+", encoding="utf-8")
        try:
            import fcntl

            fcntl.flock(self.handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            self.handle.seek(0)
            previous = self.handle.read().strip()
            self.handle.close()
            self.handle = None
            pid = _lock_pid(previous)
            if pid and pid_alive(pid):
                raise DuplicateSupervisor(f"supervisor already running as pid {pid}") from exc
            raise DuplicateSupervisor("supervisor lock is held and was not taken") from exc
        except AttributeError:
            # fcntl is absent. The lock file and pid check are the fallback.
            pass
        self.handle.seek(0)
        previous_text = self.handle.read().strip()
        previous_pid = _lock_pid(previous_text)
        if previous_pid and previous_pid != os.getpid() and not pid_alive(previous_pid):
            log_event(self.layout, "stale_lock", f"recovered stale supervisor pid {previous_pid}", counts={"pid": previous_pid})
            log_progress(self.layout, f"STALE LOCK recovered pid={previous_pid}")
        self.held = True
        self.update()

    def update(self, **extra) -> None:
        if not self.held or self.handle is None:
            return
        payload = {
            "hostname": hostname(),
            "last_heartbeat": utc_now(),
            "pid": os.getpid(),
            "spec_hash": self.spec_hash,
            "started_at": extra.get("started_at", utc_now()),
        }
        payload.update(extra)
        text = json.dumps(payload, sort_keys=True)
        self.handle.seek(0)
        self.handle.write(text)
        self.handle.truncate()
        self.handle.flush()
        os.fsync(self.handle.fileno())

    def release(self) -> None:
        if self.handle is None:
            return
        try:
            import fcntl

            fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
        except (AttributeError, OSError):
            pass
        self.handle.close()
        self.handle = None
        self.held = False


def _lock_pid(text: str) -> int | None:
    if not text:
        return None
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return None
    pid = payload.get("pid")
    return int(pid) if isinstance(pid, int) else None


def stop_requested(layout: Layout) -> bool:
    return layout.stop_path().exists()


def request_stop(root: Path) -> None:
    layout = Layout(root)
    layout.ensure()
    atomic_write_json(layout.stop_path(), {"requested_at": utc_now()})
    log_progress(layout, "STOP requested")
    log_event(layout, "stop_requested", "stop file written")


def clear_stop(layout: Layout) -> None:
    if layout.stop_path().exists():
        layout.stop_path().unlink()


def supervise(root: Path, *, max_batches: int | None = None, max_wall: float | None = None, workers: int = DEFAULT_WORKERS, batch_size: int | None = None, watchdog: float | None = None, heartbeat: float | None = None, max_attempts: int = DEFAULT_ATTEMPTS) -> dict:
    layout = Layout(root)
    layout.ensure()
    if not layout.manifest_path().exists():
        raise ExperimentIncomplete("plan is missing; run plan before supervise")
    manifest = _load_manifest(layout)
    watchdog_seconds = float(manifest.get("watchdog_seconds", DEFAULT_WATCHDOG) if watchdog is None else watchdog)
    heartbeat_seconds = float(manifest.get("heartbeat_seconds", DEFAULT_HEARTBEAT) if heartbeat is None else heartbeat)
    manifest["watchdog_seconds"] = watchdog_seconds
    manifest["heartbeat_seconds"] = heartbeat_seconds
    manifest["execution_bounds"] = list(EXECUTION_BOUNDS)
    _save_manifest(layout, manifest)
    lock = _Lock(layout, manifest["spec_hash"])
    lock.acquire()
    clear_stop(layout)
    started_at = utc_now()
    atomic_write_json(layout.progress() / "run-started.json", {"epoch": time.time(), "started_at": started_at, "supervisor_pid": os.getpid()})
    reconcile(layout)
    state_box = {
        "current": None,
        "last_completed": None,
        "last_error": None,
        "phase": _phase(layout),
        "stop": False,
    }
    finished = threading.Event()

    def on_signal(signum, _frame):
        del signum
        state_box["stop"] = True
        request_stop(layout.root)

    previous_term = signal.signal(signal.SIGTERM, on_signal)
    previous_int = signal.signal(signal.SIGINT, on_signal)

    def emit_running() -> None:
        current = state_box["current"]
        counts = _counts(layout, load_state(layout))
        payload = {
            "completed_items": counts["completed_items"],
            "current_batch_id": None if current is None else current["batch_id"],
            "failed_items": counts["failed_items"],
            "last_completed_item_id": state_box["last_completed"],
            "pending_items": counts["pending_items"],
            "phase": state_box["phase"],
            "quarantined_items": counts["quarantined_items"],
            "supervisor_pid": os.getpid(),
            "timestamp": utc_now(),
            "worker_elapsed_seconds": None if current is None else round(time.time() - current["started_epoch"], 3),
            "worker_pid": None if current is None else current["pid"],
            "worker_started_at": None if current is None else current["started_at"],
        }
        write_heartbeat(layout, payload)
        lock.update(started_at=started_at, phase=state_box["phase"])
        write_status(
            layout,
            build_status(
                layout,
                supervisor_pid=os.getpid(),
                phase=state_box["phase"],
                state_name="RUNNING",
                current=current,
                started_at=started_at,
                last_error=state_box["last_error"],
            ),
        )

    def beat() -> None:
        while not finished.wait(heartbeat_seconds):
            emit_running()

    # Status and heartbeat exist before the first wait. A second terminal must
    # not see an empty status file for a whole heartbeat interval.
    emit_running()
    thread = threading.Thread(target=beat, name="supervisor-heartbeat", daemon=True)
    thread.start()
    jobs = {}
    launched = 0
    wall_start = time.time()
    final_state = "STOPPED"
    try:
        state = load_state(layout)
        log_progress(layout, f"START phase={state_box['phase']} planned={len(state)}")
        log_event(layout, "start", "supervisor started", phase=state_box["phase"], counts={"planned": len(state), "workers": workers})
        while True:
            if state_box["stop"] or stop_requested(layout):
                final_state = "STOPPED"
                break
            if max_wall is not None and time.time() - wall_start >= max_wall and not jobs:
                final_state = "STOPPED"
                break
            if max_batches is not None and launched >= max_batches and not jobs:
                final_state = "STOPPED"
                break
            state = load_state(layout)
            if len(jobs) < workers and (max_batches is None or launched < max_batches):
                added = _advance(layout)
                if added:
                    log_event(layout, "advance", f"planner requested {added} items", phase=_phase(layout), counts={"added": added})
                    state = load_state(layout)
            state_box["phase"] = _phase(layout)
            _fill_batches(layout, state, workers=workers, batch_size=batch_size)
            if len(jobs) < workers and (max_batches is None or launched < max_batches) and not stop_requested(layout):
                planned_dir = layout.batches() / "planned"
                planned = sorted(path.name for path in planned_dir.iterdir() if (path / "batch.json").exists()) if planned_dir.exists() else []
                if planned:
                    batch_id = planned[0]
                    process = _launch_worker(layout, batch_id)
                    worker_meta = read_json(layout.batch_dir("running", batch_id) / "worker.json")
                    batch = read_json(layout.batch_dir("running", batch_id) / "batch.json")
                    jobs[batch_id] = {
                        "batch_id": batch_id,
                        "items": len(batch["item_ids"]),
                        "pid": process.pid,
                        "process": process,
                        "started_at": worker_meta["started_at"],
                        "started_epoch": worker_meta["started_epoch"],
                    }
                    state_box["current"] = jobs[batch_id]
                    launched += 1
                    continue
            if not jobs:
                pending = sum(1 for slot in load_state(layout).values() if slot.get("status") == "pending")
                quarantined = sum(1 for slot in load_state(layout).values() if slot.get("status") == "quarantined")
                if pending == 0 and _advance(layout) == 0:
                    final_state = "PARTIAL" if quarantined else "COMPLETE"
                    state_box["phase"] = "COMPLETE" if final_state == "COMPLETE" else state_box["phase"]
                    break
                time.sleep(min(0.2, heartbeat_seconds))
                continue
            time.sleep(0.1)
            for batch_id, job in list(jobs.items()):
                process = job["process"]
                elapsed = time.time() - job["started_epoch"]
                done = process.poll() is not None
                timed_out = elapsed > watchdog_seconds
                if not done and not timed_out:
                    continue
                receipt = _harvest(layout, batch_id, process, job["started_epoch"], timed_out=timed_out and not done, max_attempts=max_attempts)
                if receipt["completed_item_ids"]:
                    state_box["last_completed"] = receipt["completed_item_ids"][-1]
                if receipt["failed_item_ids"]:
                    state_box["last_error"] = f"batch {batch_id} failed_items={len(receipt['failed_item_ids'])}"
                jobs.pop(batch_id)
                state_box["current"] = next(iter(jobs.values()), None) if jobs else None
    finally:
        for job in jobs.values():
            if job["process"].poll() is None and (state_box["stop"] or stop_requested(layout)):
                # Graceful stop lets the current bounded batch finish, up to the watchdog.
                remaining = watchdog_seconds - (time.time() - job["started_epoch"])
                try:
                    job["process"].wait(timeout=max(0.1, remaining))
                except subprocess.TimeoutExpired:
                    pass
            if job["process"].poll() is None:
                _harvest(layout, job["batch_id"], job["process"], job["started_epoch"], timed_out=True, max_attempts=max_attempts)
            elif not read_receipt(layout, job["batch_id"]):
                _harvest(layout, job["batch_id"], job["process"], job["started_epoch"], timed_out=False, max_attempts=max_attempts)
        finished.set()
        thread.join(timeout=heartbeat_seconds + 1)
        signal.signal(signal.SIGTERM, previous_term)
        signal.signal(signal.SIGINT, previous_int)
        phase = state_box["phase"] if final_state != "COMPLETE" else "COMPLETE"
        write_status(
            layout,
            build_status(layout, supervisor_pid=None, phase=phase, state_name=final_state, current=None, started_at=started_at, last_error=state_box["last_error"]),
        )
        log_progress(layout, f"{final_state} phase={phase}")
        log_event(layout, "supervisor_exit", final_state, phase=phase)
        lock.release()
    return read_status(layout)


def worker_main(argv: list[str]) -> int:
    root = None
    batch_id = None
    index = 0
    while index < len(argv):
        if argv[index] == "--root":
            root = Path(argv[index + 1])
            index += 2
            continue
        if argv[index] == "--batch":
            batch_id = argv[index + 1]
            index += 2
            continue
        raise SystemExit(f"unknown worker argument {argv[index]}")
    if root is None or batch_id is None:
        raise SystemExit("worker requires --root and --batch")
    for name in THREAD_ENV:
        os.environ[name] = "1"
    layout = Layout(root)
    manifest = _load_manifest(layout)
    execute = _import_executor(manifest["executor"])
    batch = read_json(layout.batch_dir("running", batch_id) / "batch.json")
    index_rows = work_index(layout)
    context = {"cache": {}, "root": root, "batch_id": batch_id, "cache_hits": 0, "cache_misses": 0}
    errors = layout.batch_dir("running", batch_id) / "errors"
    for item_id in batch["item_ids"]:
        if read_valid_item(layout, item_id, manifest["spec_hash"]) is not None:
            continue
        record = index_rows[item_id]
        started = utc_now()
        try:
            result = execute(record, context)
            if not isinstance(result, dict):
                raise TypeError("execute_item must return an object")
            payload = {
                "analysis_version": record["analysis_version"],
                "completed_at": utc_now(),
                "input": record["input"],
                "input_hash": record["input_hash"],
                "item_id": record["item_id"],
                "kind": record["kind"],
                "result": result,
                "result_hash": result_hash(result),
                "schema": ITEM_SCHEMA,
                "semantic_version": record["semantic_version"],
                "solver_residuals": result.get("solver_residuals", {}),
                "spec_hash": record["spec_hash"],
                "started_at": started,
            }
            publish_item(layout, payload, manifest["spec_hash"])
        except Exception as exc:  # one item must not hide the rest of a bounded batch
            errors.mkdir(parents=True, exist_ok=True)
            atomic_write_json(errors / f"{item_id}.json", {"item_id": item_id, "message": f"{type(exc).__name__}: {exc}", "at": utc_now()})
    atomic_write_json(
        layout.batch_dir("running", batch_id) / "cache.json",
        {"cache_hits": int(context.get("cache_hits", 0)), "cache_misses": int(context.get("cache_misses", 0))},
    )
    return 0


def verify_root(root: Path, *, require_complete: bool = False) -> dict:
    layout = Layout(root)
    problems = []
    if not layout.manifest_path().exists():
        return {"ok": False, "problems": ["manifest missing"], "complete": False}
    manifest = _load_manifest(layout)
    spec_hash = manifest["spec_hash"]
    seen = {}
    orphans = []
    items_on_disk = list(layout.items().glob("*.json")) if layout.items().exists() else []
    known_rows = load_work_items(layout)
    seen_ids = set()
    for row in known_rows:
        if row["item_id"] in seen_ids:
            problems.append(f"duplicate item id {row['item_id']}")
        seen_ids.add(row["item_id"])
    known = {row["item_id"]: row for row in known_rows}
    for path in items_on_disk:
        if path.name.endswith(".error.json"):
            continue
        item_id = path.name[:-5]
        if item_id not in known:
            orphans.append(item_id)
            continue
        try:
            payload = read_valid_item(layout, item_id, spec_hash)
            if payload is None:
                problems.append(f"invalid item {item_id}")
                continue
            if item_id in seen:
                problems.append(f"duplicate item {item_id}")
            seen[item_id] = payload["result_hash"]
        except (OSError, ValueError, KeyError) as exc:
            problems.append(f"{item_id}: {exc}")
    missing = []
    state = load_state(layout) if layout.item_state_path().exists() else {}
    for item_id, record in known.items():
        slot = state.get(item_id, {})
        if slot.get("status") == "quarantined":
            continue
        if item_id not in seen and slot.get("status") == "complete":
            missing.append(item_id)
        if record["spec_hash"] != spec_hash:
            problems.append(f"work item {item_id} spec_hash drifted")
    receipt_problems = []
    for receipt in _receipts(layout):
        for item_id in receipt.get("completed_item_ids", []):
            if item_id not in seen:
                receipt_problems.append(f"receipt {receipt['batch_id']} cites missing {item_id}")
            elif receipt.get("result_hashes", {}).get(item_id) not in {None, seen[item_id]}:
                receipt_problems.append(f"receipt {receipt['batch_id']} hash mismatch {item_id}")
        claimed = set(receipt.get("planned_item_ids", []))
        if set(receipt.get("completed_item_ids", [])) - claimed:
            receipt_problems.append(f"receipt {receipt['batch_id']} completed an unplanned item")
    problems.extend(receipt_problems)
    quarantined = [item_id for item_id, slot in state.items() if slot.get("status") == "quarantined"]
    calibrations = []
    if layout.calibration().exists():
        for path in sorted(layout.calibration().glob("*.json")):
            row = read_json(path)
            calibrations.append({"calibration_id": row.get("calibration_id"), "convergence_status": row.get("convergence_status")})
            if "convergence_status" not in row:
                problems.append(f"calibration {path.name} has no convergence_status")
    status = read_status(layout)
    complete = status.get("state") == "COMPLETE" and not missing and not quarantined
    merge_summary = layout.merge() / "summary.json"
    merge_item_rows = list((layout.merge() / "items").glob("*.json")) if (layout.merge() / "items").exists() else []
    merge_science_rows = list((layout.merge() / "rows").glob("*.json")) if (layout.merge() / "rows").exists() else []
    if merge_summary.exists():
        summary = read_json(merge_summary)
        listed = {row.get("item_id"): row.get("result_hash") for row in summary.get("items", []) if isinstance(row, dict)}
        for item_id, digest in listed.items():
            path = layout.merge() / "items" / f"{item_id}.json"
            if path.exists():
                stored = read_json(path)
                if stored.get("result_hash") not in {None, digest}:
                    problems.append(f"merge file hash mismatch {item_id}")
            if item_id in seen:
                if digest not in {None, seen[item_id]}:
                    problems.append(f"merge hash mismatch {item_id}")
            elif not path.exists():
                problems.append(f"merge summary cites missing {item_id}")
        for path in merge_item_rows:
            if path.name[:-5] not in listed:
                problems.append(f"merge row {path.name[:-5]} is absent from the summary")
        science = [row for row in summary.get("rows", []) if isinstance(row, dict) and row.get("target_id")]
        listed_targets = {row["target_id"] for row in science}
        for target_id in sorted(listed_targets):
            path = layout.merge() / "rows" / f"{target_id}.json"
            if not path.exists():
                problems.append(f"merge summary cites missing row {target_id}")
                continue
            stored = read_json(path).get("row") or {}
            if stored.get("target_id") != target_id:
                problems.append(f"merge row {target_id} target_id drifted")
        for path in merge_science_rows:
            if path.name[:-5] not in listed_targets:
                problems.append(f"merge row {path.name[:-5]} is absent from the summary")
    elif merge_item_rows or merge_science_rows:
        problems.append("merge summary missing")
    report = {
        "calibrations": calibrations,
        "complete": complete,
        "items": len(seen),
        "missing_completed": missing,
        "ok": not problems and not missing,
        "orphans": orphans,
        "problems": problems,
        "quarantined": quarantined,
        "receipts": len(_receipts(layout)),
        "spec_hash": spec_hash,
    }
    if require_complete and not complete:
        report["ok"] = False
        report["problems"].append("generation is not complete")
    if require_complete and manifest.get("merge") and not merge_summary.exists():
        report["ok"] = False
        report["problems"].append("merge summary missing")
    return report


def merge_root(root: Path) -> dict:
    layout = Layout(root)
    manifest = _load_manifest(layout)
    dotted = manifest.get("merge")
    if not dotted:
        raise ExperimentIncomplete("this experiment has no merge hook")
    return _import_executor(dotted)(root)


def status_text(root: Path) -> str:
    layout = Layout(root)
    payload = read_status(layout)
    if not payload:
        payload = {"experiment_id": "unplanned", "state": "ABSENT", "phase": "-", "completed_items": 0, "planned_items_current": 0, "calibrations_complete": 0, "calibrations_total": 0, "failed_items": 0, "timed_out_batches": 0, "quarantined_items": 0, "recent_items_per_second": 0, "estimated_remaining_seconds": None, "heartbeat_age_seconds": None, "last_error": None, "current_batch_id": None, "current_batch_elapsed_seconds": None}
    last = tail_lines(layout.log_path(), 1)
    return format_status(payload, last_progress=last[-1] if last else None)


def watch_status(root: Path, interval: float, snapshots: int | None = None) -> int:
    produced = 0
    while True:
        print(status_text(root), flush=True)
        print("", flush=True)
        produced += 1
        if snapshots is not None and produced >= snapshots:
            return 0
        layout = Layout(root)
        payload = read_status(layout)
        if payload.get("state") in {"COMPLETE", "STOPPED", "PARTIAL"} and snapshots is None:
            # One extra beat after a terminal state so a watcher sees the end.
            if produced > 1:
                return 0
        time.sleep(interval)
