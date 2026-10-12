"""Commands for the micro-batch supervisor.

`generation007` is the scientific entry. `batch` is the same supervisor with
an explicit experiment module, used by the fault-injection tests.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

from rs_constraint_lab.supervisor import (
    DuplicateSupervisor,
    merge_root,
    request_stop,
    status_text,
    supervise,
    verify_root,
    watch_status,
    worker_main,
)
from rs_constraint_lab.workstore import Layout, load_state, save_state


def _lab_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _default_generation_root() -> Path:
    return _lab_root() / "generated" / "generation-007"


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: python -m rs_constraint_lab generation007 <command>", file=sys.stderr)
        return 2
    if argv[0] == "worker":
        return worker_main(argv[1:])
    if argv[0] == "generation007":
        return _generation(argv[1:])
    if argv[0] == "batch":
        return _batch(argv[1:])
    print(f"unknown command {argv[0]}", file=sys.stderr)
    return 2


def _generation(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="rs_constraint_lab generation007")
    parser.add_argument("command", choices=["plan", "run-next", "run-batches", "supervise", "start", "status", "verify", "merge", "retry", "stop", "benchmark", "smoke"])
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--watch", type=float, default=None)
    parser.add_argument("--max-snapshots", type=int, default=None)
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--max-wall", type=float, default=60.0)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args(argv)
    root = args.root or _default_generation_root()
    if args.command == "plan":
        from rs_constraint_lab.gen007_exec import plan

        summary = plan(root)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    if args.command == "benchmark":
        from rs_constraint_lab.gen007_exec import benchmark

        summary = benchmark(root)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    if args.command == "smoke":
        from rs_constraint_lab.gen007_exec import plan_smoke

        smoke_root = args.root or (_lab_root() / "generated" / "generation-007-smoke")
        summary = plan_smoke(smoke_root)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    if args.command == "run-next":
        return _supervise(root, max_batches=1, max_wall=args.max_wall, workers=args.workers)
    if args.command == "run-batches":
        return _supervise(root, max_batches=args.count, max_wall=None, workers=args.workers)
    if args.command == "supervise":
        return _supervise(root, max_batches=None, max_wall=None, workers=args.workers)
    if args.command == "start":
        return _start(root, workers=args.workers)
    if args.command == "status":
        if args.watch is None:
            print(status_text(root))
            return 0
        return watch_status(root, args.watch, args.max_snapshots)
    if args.command == "verify":
        report = verify_root(root, require_complete=args.require_complete)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report["ok"] else 1
    if args.command == "merge":
        summary = merge_root(root)
        print(json.dumps({"merged_items": len(summary.get("rows", summary.get("items", [])))}, indent=2, sort_keys=True))
        return 0
    if args.command == "retry":
        return _retry(root)
    if args.command == "stop":
        request_stop(root)
        print(f"stop requested for {root}")
        return 0
    return 2


def _batch(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="rs_constraint_lab batch")
    parser.add_argument("command", choices=["plan", "supervise", "status", "stop", "verify", "merge"])
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--module", default="rs_constraint_lab.faultlab")
    parser.add_argument("--max-batches", type=int, default=None)
    parser.add_argument("--max-wall", type=float, default=None)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--watchdog", type=float, default=None)
    parser.add_argument("--heartbeat", type=float, default=None)
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument("--watch", type=float, default=None)
    parser.add_argument("--max-snapshots", type=int, default=None)
    args = parser.parse_args(argv)
    if args.command == "plan":
        module = __import__(args.module, fromlist=["plan"])
        summary = module.plan(args.root)
        print(json.dumps(summary, sort_keys=True))
        return 0
    if args.command == "supervise":
        try:
            payload = supervise(
                args.root,
                max_batches=args.max_batches,
                max_wall=args.max_wall,
                workers=args.workers,
                batch_size=args.batch_size,
                watchdog=args.watchdog,
                heartbeat=args.heartbeat,
                max_attempts=args.max_attempts,
            )
        except DuplicateSupervisor as exc:
            print(str(exc), file=sys.stderr)
            return 2
        print(json.dumps({"state": payload.get("state"), "phase": payload.get("phase")}, sort_keys=True))
        return 0
    if args.command == "status":
        if args.watch is None:
            print(status_text(args.root))
            return 0
        return watch_status(args.root, args.watch, args.max_snapshots)
    if args.command == "stop":
        request_stop(args.root)
        return 0
    if args.command == "verify":
        report = verify_root(args.root)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report["ok"] else 1
    if args.command == "merge":
        summary = merge_root(args.root)
        print(json.dumps({"items": len(summary.get("items", []))}, sort_keys=True))
        return 0
    return 2


def _supervise(root: Path, *, max_batches: int | None, max_wall: float | None, workers: int) -> int:
    try:
        payload = supervise(root, max_batches=max_batches, max_wall=max_wall, workers=workers)
    except DuplicateSupervisor as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(status_text(root))
    print(json.dumps({"state": payload.get("state")}, sort_keys=True))
    return 0


def _start(root: Path, *, workers: int) -> int:
    layout = Layout(root)
    layout.ensure()
    log_path = layout.progress() / "supervisor.out"
    handle = log_path.open("ab")
    command = [
        sys.executable,
        "-m",
        "rs_constraint_lab",
        "generation007",
        "supervise",
        "--root",
        str(root),
        "--workers",
        str(workers),
    ]
    process = subprocess.Popen(
        command,
        cwd=str(_lab_root()),
        stdin=subprocess.DEVNULL,
        stdout=handle,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    handle.close()
    from rs_constraint_lab.durable import atomic_write_json
    from rs_constraint_lab.workstore import utc_now

    atomic_write_json(layout.progress() / "launcher.json", {"pid": process.pid, "started_at": utc_now()})
    # Return as soon as the child has had a chance to create its session.
    time.sleep(0.2)
    print(json.dumps({"pid": process.pid, "root": str(root), "log": str(log_path)}, sort_keys=True))
    return 0


def _retry(root: Path) -> int:
    layout = Layout(root)
    state = load_state(layout)
    reset = 0
    for slot in state.values():
        if slot.get("status") == "quarantined" or slot.get("last_error"):
            if slot.get("status") != "complete":
                slot["status"] = "pending"
                slot["attempts"] = 0
                slot["force_single"] = True
                reset += 1
    save_state(layout, state)
    print(json.dumps({"requeued": reset}, sort_keys=True))
    return 0
