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


def _default_generation_b_root() -> Path:
    return _lab_root() / "generated" / "generation-007b"


def _default_generation_008_root() -> Path:
    return _lab_root() / "generated" / "generation-008" / "round-000"


def _repo_root() -> Path:
    return _lab_root().parent


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: python -m rs_constraint_lab generation007 <command>", file=sys.stderr)
        return 2
    if argv[0] == "worker":
        return worker_main(argv[1:])
    if argv[0] == "generation007":
        return _generation(argv[1:])
    if argv[0] == "generation007b":
        return _generation_b(argv[1:])
    if argv[0] == "generation008":
        return _generation_008(argv[1:])
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
        return _start(root, workers=args.workers, command="generation007")
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


def _generation_b(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="rs_constraint_lab generation007b")
    parser.add_argument("command", choices=["plan", "run-next", "run-batches", "supervise", "start", "restart", "status", "verify", "merge", "retry", "stop", "benchmark", "smoke", "preflight"])
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--watch", type=float, default=None)
    parser.add_argument("--max-snapshots", type=int, default=None)
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--max-wall", type=float, default=60.0)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args(argv)
    root = args.root or _default_generation_b_root()
    if args.command == "plan":
        from rs_constraint_lab.gen007b_exec import plan

        summary = plan(root)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    if args.command == "benchmark":
        from rs_constraint_lab.gen007b_exec import benchmark

        summary = benchmark(root)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    if args.command == "smoke":
        from rs_constraint_lab.gen007b_exec import plan_smoke

        smoke_root = args.root or (_lab_root() / "generated" / "generation-007b-smoke")
        summary = plan_smoke(smoke_root)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    if args.command == "preflight":
        from rs_constraint_lab.gen007b_exec import plan_preflight

        preflight_root = args.root or (_lab_root() / "generated" / "generation-007b-preflight")
        summary = plan_preflight(preflight_root)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    if args.command == "run-next":
        return _supervise(root, max_batches=1, max_wall=args.max_wall, workers=args.workers)
    if args.command == "run-batches":
        return _supervise(root, max_batches=args.count, max_wall=None, workers=args.workers)
    if args.command == "supervise":
        return _supervise(root, max_batches=None, max_wall=None, workers=args.workers)
    if args.command in {"start", "restart"}:
        return _start(root, workers=args.workers, command="generation007b")
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
        print(json.dumps({"rows": len(summary.get("rows", []))}, indent=2, sort_keys=True))
        return 0
    if args.command == "retry":
        return _retry(root)
    if args.command == "stop":
        request_stop(root)
        print(f"stop requested for {root}")
        return 0
    return 2


def _generation_008(argv: list[str]) -> int:
    if not argv:
        print("usage: python -m rs_constraint_lab generation008 <command>", file=sys.stderr)
        return 2
    if argv[0] == "atlas":
        return _atlas008(argv[1:])
    if argv[0] == "transitions":
        return _transitions008(argv[1:])
    parser = argparse.ArgumentParser(prog="rs_constraint_lab generation008")
    parser.add_argument(
        "command",
        choices=[
            "benchmark",
            "write-plan",
            "plan",
            "run-next",
            "run-batches",
            "supervise",
            "start",
            "restart",
            "status",
            "verify",
            "merge",
            "retry",
            "stop",
        ],
    )
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--plan", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--frozen-plan-commit", default=None)
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--relpath", default=None)
    parser.add_argument("--horizon", type=int, default=None)
    parser.add_argument("--watch", type=float, default=None)
    parser.add_argument("--max-snapshots", type=int, default=None)
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--max-wall", type=float, default=60.0)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args(argv)
    root = args.root or _default_generation_008_root()
    if args.command == "benchmark":
        from rs_constraint_lab.gen008_exec import benchmark_cost, choose_horizon
        from rs_constraint_lab.explore08 import REPLICATES, build_round0_systems, enumerate_hidden_contexts

        sample = benchmark_cost(horizon=args.horizon or 512)
        sources = enumerate_hidden_contexts()
        episodes = len(build_round0_systems()) * sum(row["orbit_count"] for row in sources.values()) * REPLICATES
        decision = choose_horizon(sample, episodes)
        print(json.dumps({"decision": decision, "episodes": episodes, "sample": sample}, indent=2, sort_keys=True))
        return 0 if not decision["refused"] else 2
    if args.command == "write-plan":
        from rs_constraint_lab.durable import atomic_write_json
        from rs_constraint_lab.gen008_exec import prepare_round0_plan

        if args.output is None:
            print("write-plan requires --output", file=sys.stderr)
            return 2
        prepared = prepare_round0_plan(horizon=args.horizon)
        if prepared["plan"] is None:
            print(json.dumps({"decision": prepared["decision"], "refused": True}, indent=2, sort_keys=True))
            return 2
        atomic_write_json(args.output, prepared["plan"])
        work = prepared["plan"]["work_count"]
        print(json.dumps(
            {
                "episodes": work["total_round_episodes"],
                "output": str(args.output),
                "pair_horizon": prepared["plan"]["pair_horizon"],
                "plan_hash": prepared["plan"]["plan_hash"],
            },
            indent=2,
            sort_keys=True,
        ))
        return 0
    if args.command == "plan":
        from rs_constraint_lab.gen008_exec import install_plan

        if args.plan is None or not args.frozen_plan_commit or args.root is None:
            print("plan requires --plan, --frozen-plan-commit, and --root", file=sys.stderr)
            return 2
        repo = args.repo or _repo_root()
        relpath = args.relpath or str(args.plan.resolve().relative_to(repo.resolve()))
        try:
            summary = install_plan(args.root, args.plan, args.frozen_plan_commit, repo, relpath)
        except Exception as exc:
            print(str(exc), file=sys.stderr)
            return 2
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    if args.command == "run-next":
        return _supervise(root, max_batches=1, max_wall=args.max_wall, workers=args.workers)
    if args.command == "run-batches":
        return _supervise(root, max_batches=args.count, max_wall=None, workers=args.workers)
    if args.command == "supervise":
        return _supervise(root, max_batches=None, max_wall=None, workers=args.workers)
    if args.command in {"start", "restart"}:
        return _start(root, workers=args.workers, command="generation008")
    if args.command == "status":
        if args.watch is None:
            print(status_text(root))
            return 0
        return watch_status(root, args.watch, args.max_snapshots)
    if args.command == "verify":
        from rs_constraint_lab.gen008_exec import verify_generation

        report = verify_generation(root, require_complete=args.require_complete)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report["ok"] else 1
    if args.command == "merge":
        summary = merge_root(root)
        print(json.dumps({"episodes": summary.get("episodes"), "replay_exact": summary.get("replay_exact")}, indent=2, sort_keys=True))
        return 0
    if args.command == "retry":
        return _retry(root)
    if args.command == "stop":
        request_stop(root)
        print(f"stop requested for {root}")
        return 0
    return 2


def _atlas008(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="rs_constraint_lab generation008 atlas")
    parser.add_argument("view", choices=["summary", "routes", "contexts", "motifs", "episode", "replay", "compare"])
    parser.add_argument("selectors", nargs="*")
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args(argv)
    from rs_constraint_lab.gen008_exec import atlas_view

    try:
        print(atlas_view(args.root or _default_generation_008_root(), args.view, args.selectors, limit=args.limit))
    except (FileNotFoundError, KeyError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


def _transitions008(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="rs_constraint_lab generation008 transitions")
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--source", default=None)
    parser.add_argument("--target", default=None)
    parser.add_argument("--orbit", default=None)
    parser.add_argument("--system", default=None)
    parser.add_argument("--triad-count", type=int, default=None)
    parser.add_argument("--motif", default=None)
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args(argv)
    from rs_constraint_lab.gen008_exec import transitions_view

    motif = [part for part in args.motif.split(",") if part] if args.motif else None
    try:
        print(transitions_view(
            args.root or _default_generation_008_root(),
            source_class=args.source,
            target_class=args.target,
            orbit_id=args.orbit,
            system_id=args.system,
            triad_count=args.triad_count,
            motif=motif,
            limit=args.limit,
        ))
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


def _start(root: Path, *, workers: int, command: str = "generation007") -> int:
    layout = Layout(root)
    layout.ensure()
    log_path = layout.progress() / "supervisor.out"
    handle = log_path.open("ab")
    command = [
        sys.executable,
        "-m",
        "rs_constraint_lab",
        command,
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
