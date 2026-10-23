"""Run frozen items inside a wall-clock budget.

Each item is a child process. The parent kills the process group when the
watchdog expires and records a terminal timeout. It does not change the spec.
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

from rrc import ENGINE_VERSION
from rrc.items import execute_spec_catching
from rrc.store import RERUN, TERMINAL, IncompatiblePlan, Store


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def python_path() -> str:
    source = Path(__file__).resolve().parents[1]
    current = os.environ.get("PYTHONPATH", "")
    parts = [str(source)]
    if current:
        parts.append(current)
    return os.pathsep.join(parts)


def run_child(spec: dict, timeout: float) -> dict:
    env = dict(os.environ)
    env["PYTHONPATH"] = python_path()
    process = subprocess.Popen(
        [sys.executable, "-m", "rrc", "worker"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        start_new_session=True,
        cwd=str(project_root()),
    )
    payload = json.dumps(spec).encode("utf-8")
    try:
        stdout, stderr = process.communicate(payload, timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait(timeout=5)
        return {
            "status": "timeout",
            "item_id": spec.get("id"),
            "round_id": spec.get("round_id"),
            "type": spec.get("type"),
            "error": f"item exceeded {timeout} seconds and was killed",
            "engine_version": ENGINE_VERSION,
        }
    if process.returncode != 0:
        text = stderr.decode("utf-8", errors="replace")
        try:
            parsed = json.loads(stdout.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            parsed = None
        if isinstance(parsed, dict) and parsed.get("status") in TERMINAL:
            return parsed
        return {
            "status": "failed",
            "item_id": spec.get("id"),
            "round_id": spec.get("round_id"),
            "type": spec.get("type"),
            "error": text or f"worker exit {process.returncode}",
            "engine_version": ENGINE_VERSION,
        }
    try:
        parsed = json.loads(stdout.decode("utf-8"))
    except json.JSONDecodeError:
        return {
            "status": "failed",
            "item_id": spec.get("id"),
            "error": "worker returned invalid JSON",
            "engine_version": ENGINE_VERSION,
        }
    if parsed.get("status") not in TERMINAL:
        parsed["status"] = "failed"
        parsed["error"] = parsed.get("error") or "worker returned a non-terminal status"
    return parsed


def execute_plan(
    plan: dict,
    out: Path,
    *,
    max_items: int,
    budget_seconds: float,
    timeout: float | None = None,
    child=run_child,
) -> dict:
    if plan.get("engine_version") != ENGINE_VERSION:
        raise SystemExit(
            f"plan engine {plan.get('engine_version')} does not match {ENGINE_VERSION}"
        )
    store = Store(out, plan)
    store.prepare()
    watchdog = float(timeout if timeout is not None else plan["watchdog_seconds"])
    if watchdog > float(plan.get("hard_ceiling_seconds", 300)):
        raise SystemExit("watchdog exceeds the hard ceiling")
    started = time.perf_counter()
    ran = 0
    for item in plan["items"]:
        if ran >= max_items:
            break
        if time.perf_counter() - started >= budget_seconds:
            break
        state = store.classify(item["id"])
        if state in TERMINAL:
            continue
        if state in RERUN and state != "pending":
            store.quarantine(item["id"])
        store.write_status(item["id"], "running")
        result = child(item, watchdog)
        store.commit_result(item["id"], result)
        ran += 1
    counts = store.counts()
    return {
        "ran": ran,
        "elapsed_s": round(time.perf_counter() - started, 6),
        "counts": counts,
        "plan_hash": store.plan_hash,
        "out": str(out),
    }


def worker_main() -> int:
    raw = sys.stdin.buffer.read()
    spec = json.loads(raw.decode("utf-8"))
    result = execute_spec_catching(spec)
    sys.stdout.write(json.dumps(result))
    return 0 if result.get("status") in TERMINAL else 1
