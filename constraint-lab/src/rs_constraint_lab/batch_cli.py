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


def _default_generation_008a_root() -> Path:
    return _lab_root() / "generated" / "generation-008a" / "round-a0"


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
    if argv[0] == "generation008a":
        return _generation_008a(argv[1:])
    if argv[0] == "generation008b":
        return _generation_008b(argv[1:])
    if argv[0] == "generation008c":
        return _generation_008c(argv[1:])
    if argv[0] == "generation008d":
        return _generation_008d(argv[1:])
    if argv[0] == "generation008e":
        return _generation_008e(argv[1:])
    if argv[0] == "generation008f":
        return _generation_008f(argv[1:])
    if argv[0] == "batch":
        return _batch(argv[1:])
    print(f"unknown command {argv[0]}", file=sys.stderr)
    return 2


def _generation_008f(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="rs_constraint_lab generation008f")
    parser.add_argument("command", choices=["plan", "run-f0", "publish", "verify", "status"])
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--frozen-plan-commit", default=None)
    args = parser.parse_args(argv)
    repo = _repo_root()
    root = args.root or (_lab_root() / "generated" / "generation-008f" / "round-f0")
    if args.command == "plan":
        from rs_constraint_lab.gen008f_exec import write_plan

        document = write_plan(repo)
        print(json.dumps({"path": "constraint-lab/exploration/generation-008f/round-f0-plan.json", "plan_hash": document["plan_hash"]}, indent=2, sort_keys=True))
        return 0
    if args.command == "run-f0":
        from rs_constraint_lab.gen008f_exec import execute, require_f0_execution

        plan = require_f0_execution(repo, args.frozen_plan_commit)
        payload = execute(root, plan, frozen_plan_commit=args.frozen_plan_commit)
        print(json.dumps({"summary": payload["summary"], "validation": payload["validation"]}, indent=2, sort_keys=True))
        return 0 if payload["validation"]["ok"] else 1
    if args.command == "publish":
        from rs_constraint_lab.durable import read_json
        from rs_constraint_lab.gen008f_exec import publish_tables

        payload = read_json(root / "round-f0-tables.json")
        hashes = publish_tables(payload, _lab_root() / "reports")
        print(json.dumps(hashes, indent=2, sort_keys=True))
        return 0
    if args.command == "verify":
        from rs_constraint_lab.gen008f_exec import verify_payload

        report = verify_payload(root / "round-f0-tables.json")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report["complete"] else 1
    if args.command == "status":
        from rs_constraint_lab.durable import read_json

        print(json.dumps(read_json(root / "status.json"), indent=2, sort_keys=True))
        return 0
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


def _generation_008a(argv: list[str]) -> int:
    if not argv:
        print("usage: python -m rs_constraint_lab generation008a <command>", file=sys.stderr)
        return 2
    parser = argparse.ArgumentParser(prog="rs_constraint_lab generation008a")
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
            "chronology",
        ],
    )
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--plan", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--frozen-plan-commit", default=None)
    parser.add_argument("--result-commit", default=None)
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--relpath", default=None)
    parser.add_argument("--expect-hash", default=None)
    parser.add_argument("--horizon", type=int, default=None)
    parser.add_argument("--watch", type=float, default=None)
    parser.add_argument("--max-snapshots", type=int, default=None)
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--max-wall", type=float, default=60.0)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args(argv)
    root = args.root or _default_generation_008a_root()
    if args.command == "benchmark":
        from rs_constraint_lab.gen008_exec import choose_horizon
        from rs_constraint_lab.gen008a_exec import benchmark_cost

        sample = benchmark_cost(horizon=args.horizon or 512)
        episodes = 8 * 48 * 16
        decision = choose_horizon(sample, episodes)
        print(json.dumps({"decision": decision, "episodes": episodes, "sample": sample}, indent=2, sort_keys=True))
        return 0 if not decision["refused"] else 2
    if args.command == "write-plan":
        from rs_constraint_lab.durable import atomic_write_json
        from rs_constraint_lab.gen008a_exec import prepare_a0_plan

        if args.output is None:
            print("write-plan requires --output", file=sys.stderr)
            return 2
        prepared = prepare_a0_plan(sample_horizon=args.horizon or 512)
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
                "starts_per_system": work["starts_per_system"],
            },
            indent=2,
            sort_keys=True,
        ))
        return 0
    if args.command == "plan":
        from rs_constraint_lab.gen008a_exec import install_plan

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
    if args.command == "chronology":
        from rs_constraint_lab.explore08a import ChronologyError, verify_plan_result_chronology

        if not args.frozen_plan_commit or not args.result_commit or not args.relpath:
            print("chronology requires --frozen-plan-commit, --result-commit, and --relpath", file=sys.stderr)
            return 2
        repo = args.repo or _repo_root()
        try:
            report = verify_plan_result_chronology(
                repo,
                args.frozen_plan_commit,
                args.result_commit,
                args.relpath,
                args.expect_hash,
            )
        except ChronologyError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    if args.command == "run-next":
        return _supervise(root, max_batches=1, max_wall=args.max_wall, workers=args.workers)
    if args.command == "run-batches":
        return _supervise(root, max_batches=args.count, max_wall=None, workers=args.workers)
    if args.command == "supervise":
        return _supervise(root, max_batches=None, max_wall=None, workers=args.workers)
    if args.command in {"start", "restart"}:
        return _start(root, workers=args.workers, command="generation008a")
    if args.command == "status":
        if args.watch is None:
            print(status_text(root))
            return 0
        return watch_status(root, args.watch, args.max_snapshots)
    if args.command == "verify":
        from rs_constraint_lab.gen008a_exec import verify_generation

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


def _default_generation_008b_root() -> Path:
    return _lab_root() / "generated" / "generation-008b" / "round-b0"


def _generation_008b(argv: list[str]) -> int:
    if not argv:
        print("usage: python -m rs_constraint_lab generation008b <command>", file=sys.stderr)
        return 2
    parser = argparse.ArgumentParser(prog="rs_constraint_lab generation008b")
    parser.add_argument(
        "command",
        choices=["write-plan", "exact", "permute-initial", "permute-current", "assemble", "reproduce", "verify"],
    )
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--plan", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--frozen-plan-commit", default=None)
    parser.add_argument("--result-commit", default=None)
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--relpath", default=None)
    parser.add_argument("--system", default=None)
    parser.add_argument("--source", default=None)
    parser.add_argument("--allow-unpushed", action="store_true")
    args = parser.parse_args(argv)
    from rs_constraint_lab.explore08 import FrozenPlanError
    from rs_constraint_lab.explore08a import ChronologyError, verify_plan_result_chronology
    from rs_constraint_lab.explore08b import CalibrationError, load_a0_palette, reproduce_plugin_tables
    from rs_constraint_lab.gen008b_exec import (
        PARENT_TABLES_RELPATH,
        PLAN_RELPATH,
        SOURCES,
        _index_tables,
        _load_tables,
        _system_row,
        analyse_exact,
        assemble_tables,
        permute_current,
        permute_initial,
        prepare_b0_plan,
        require_b0_execution,
        write_payload,
    )

    root = args.root or _default_generation_008b_root()
    repo = args.repo or _repo_root()
    if args.command == "write-plan":
        from rs_constraint_lab.durable import atomic_write_json

        if args.output is None:
            print("write-plan requires --output", file=sys.stderr)
            return 2
        plan = prepare_b0_plan()
        atomic_write_json(args.output, plan)
        print(json.dumps({"output": str(args.output), "plan_hash": plan["plan_hash"], "systems": len(plan["systems"])}, indent=2, sort_keys=True))
        return 0
    if args.command == "reproduce":
        report = reproduce_plugin_tables(_load_tables())
        print(
            json.dumps(
                {
                    "cell_count": len(report["cells"]),
                    "max_abs_gap": report["max_abs_gap"],
                    "within_tolerance": report["within_tolerance"],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0 if report["within_tolerance"] else 1
    if args.command == "verify":
        if args.frozen_plan_commit and args.result_commit:
            relpath = args.relpath or PLAN_RELPATH
            try:
                report = verify_plan_result_chronology(repo, args.frozen_plan_commit, args.result_commit, relpath)
            except ChronologyError as exc:
                print(str(exc), file=sys.stderr)
                return 1
            print(json.dumps(report, indent=2, sort_keys=True))
        missing = []
        for row in load_a0_palette():
            system_id = row["system_id"]
            for kind in ("exact", "permute-initial"):
                if not (root / kind / f"{system_id}.json").is_file():
                    missing.append(f"{kind}/{system_id}.json")
            for source in SOURCES:
                if not (root / "permute-current" / f"{system_id}-{source}.json").is_file():
                    missing.append(f"permute-current/{system_id}-{source}.json")
        print(json.dumps({"complete": not missing, "missing": missing, "root": str(root)}, indent=2, sort_keys=True))
        return 0 if not missing else 1

    relpath = args.relpath or (args.plan.resolve().relative_to(repo.resolve()).as_posix() if args.plan else PLAN_RELPATH)
    plan_path = args.plan or (repo / PLAN_RELPATH)
    try:
        plan = require_b0_execution(
            repo,
            args.frozen_plan_commit,
            relpath,
            disk_path=plan_path,
            require_remote=not args.allow_unpushed,
        )
    except (FrozenPlanError, CalibrationError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    indexed = _index_tables(_load_tables())
    try:
        if args.command == "exact":
            if not args.system:
                print("exact requires --system", file=sys.stderr)
                return 2
            payload = analyse_exact(_system_row(plan, args.system), indexed)
            path = root / "exact" / f"{args.system}.json"
        elif args.command == "permute-initial":
            if not args.system:
                print("permute-initial requires --system", file=sys.stderr)
                return 2
            payload = permute_initial(_system_row(plan, args.system), indexed)
            path = root / "permute-initial" / f"{args.system}.json"
        elif args.command == "permute-current":
            if not args.system or args.source not in SOURCES:
                print("permute-current requires --system and --source star|path|triangle", file=sys.stderr)
                return 2
            payload = permute_current(_system_row(plan, args.system), indexed, args.source)
            path = root / "permute-current" / f"{args.system}-{args.source}.json"
        elif args.command == "assemble":
            exact_payloads = []
            initial_payloads = []
            current_payloads = []
            for row in plan["systems"]:
                system_id = row["system_id"]
                exact_payloads.append(json.loads((root / "exact" / f"{system_id}.json").read_text(encoding="utf-8")))
                initial_payloads.append(json.loads((root / "permute-initial" / f"{system_id}.json").read_text(encoding="utf-8")))
                for source in SOURCES:
                    current_payloads.append(
                        json.loads((root / "permute-current" / f"{system_id}-{source}.json").read_text(encoding="utf-8"))
                    )
            payload = assemble_tables(exact_payloads, initial_payloads, current_payloads, indexed)
            payload["frozen_plan_commit"] = args.frozen_plan_commit
            payload["parent_tables"] = PARENT_TABLES_RELPATH
            payload["plan_hash"] = plan["plan_hash"]
            path = args.output or (_lab_root() / "reports" / "generation-008b-round-b0-tables.json")
        else:
            return 2
        written = write_payload(path, payload)
    except (CalibrationError, FrozenPlanError, FileNotFoundError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps({"bytes_sha256": written["payload_sha256"], "output": str(path), "system": args.system}, indent=2, sort_keys=True))
    return 0


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


def _default_generation_008d_root() -> Path:
    return _lab_root() / "generated" / "generation-008d" / "round-d0"


def _default_generation_008c_root() -> Path:
    return _lab_root() / "generated" / "generation-008c" / "round-c0"


def _generation_008c(argv: list[str]) -> int:
    if not argv:
        print("usage: python -m rs_constraint_lab generation008c <command>", file=sys.stderr)
        return 2
    parser = argparse.ArgumentParser(prog="rs_constraint_lab generation008c")
    parser.add_argument("command", choices=["write-plan", "execute-item", "run-c0", "assemble", "verify"])
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--plan", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--frozen-plan-commit", default=None)
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--relpath", default=None)
    parser.add_argument("--kind", default=None)
    parser.add_argument("--system", default=None)
    parser.add_argument("--source", default=None)
    parser.add_argument("--allow-unpushed", action="store_true")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args(argv)
    from rs_constraint_lab.durable import atomic_write_json
    from rs_constraint_lab.explore08 import FrozenPlanError
    from rs_constraint_lab.explore08c import MechanismError
    from rs_constraint_lab.gen008c_exec import (
        PLAN_RELPATH,
        assemble_tables,
        execute_plan_item,
        item_path,
        prepare_c0_plan,
        publish_tables,
        require_c0_execution,
        run_c0,
        write_payload,
    )

    repo = args.repo or _repo_root()
    root = args.root or _default_generation_008c_root()
    if args.command == "write-plan":
        if args.output is None:
            print("write-plan requires --output", file=sys.stderr)
            return 2
        plan = prepare_c0_plan(repo)
        atomic_write_json(args.output, plan)
        print(json.dumps({"items": len(plan["items"]), "output": str(args.output), "plan_hash": plan["plan_hash"]}, indent=2, sort_keys=True))
        return 0
    if args.command == "verify":
        relpath = args.relpath or PLAN_RELPATH
        plan_path = args.plan or (repo / PLAN_RELPATH)
        try:
            plan = require_c0_execution(
                repo,
                args.frozen_plan_commit,
                relpath,
                disk_path=plan_path,
                require_remote=not args.allow_unpushed,
            )
        except (FrozenPlanError, MechanismError) as exc:
            print(str(exc), file=sys.stderr)
            return 2
        missing = [item["kind"] for item in plan["items"] if not item_path(root, item).is_file()]
        print(json.dumps({"complete": not missing, "missing_count": len(missing), "plan_hash": plan["plan_hash"]}, indent=2, sort_keys=True))
        return 0 if not missing else 1

    relpath = args.relpath or PLAN_RELPATH
    plan_path = args.plan or (repo / PLAN_RELPATH)
    try:
        plan = require_c0_execution(
            repo,
            args.frozen_plan_commit,
            relpath,
            disk_path=plan_path,
            require_remote=not args.allow_unpushed,
        )
    except (FrozenPlanError, MechanismError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    try:
        if args.command == "execute-item":
            matches = [
                item
                for item in plan["items"]
                if item["kind"] == args.kind and item.get("system") == args.system and item.get("source") == args.source
            ]
            if len(matches) != 1:
                print("execute-item requires one --kind and the matching --system/--source", file=sys.stderr)
                return 2
            payload = execute_plan_item(matches[0])
            path = item_path(root, matches[0])
            atomic_write_json(path, payload)
            print(json.dumps({"item_id": payload["item_id"], "output": str(path), "wall_seconds": payload["wall_seconds"]}, indent=2, sort_keys=True))
            return 0
        if args.command == "run-c0":
            written = run_c0(root, plan)
            print(json.dumps({"items": len(written), "max_wall_seconds": max(row["wall_seconds"] for row in written), "root": str(root)}, indent=2, sort_keys=True))
            return 0
        if args.command == "assemble":
            payload = assemble_tables(root, plan, repo=repo, frozen_plan_commit=args.frozen_plan_commit)
            if not payload["validation"]["ok"]:
                print(json.dumps(payload["validation"], indent=2, sort_keys=True), file=sys.stderr)
                return 1
            output = args.output or (root / "round-c0-tables.json")
            written = write_payload(output, payload)
            if args.publish:
                publish_tables(payload, _lab_root() / "reports")
            print(json.dumps({"bytes_sha256": written["payload_sha256"], "output": str(output), "validation": "ok"}, indent=2, sort_keys=True))
            return 0
    except MechanismError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 2


def _generation_008d(argv: list[str]) -> int:
    if not argv:
        print("usage: python -m rs_constraint_lab generation008d <command>", file=sys.stderr)
        return 2
    parser = argparse.ArgumentParser(prog="rs_constraint_lab generation008d")
    parser.add_argument("command", choices=["write-plan", "execute-item", "run-d0", "assemble", "verify"])
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--plan", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--frozen-plan-commit", default=None)
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--relpath", default=None)
    parser.add_argument("--kind", default=None)
    parser.add_argument("--orbit", default=None)
    parser.add_argument("--allow-unpushed", action="store_true")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args(argv)
    from rs_constraint_lab.durable import atomic_write_json
    from rs_constraint_lab.explore08 import FrozenPlanError
    from rs_constraint_lab.explore08d import CompositionError
    from rs_constraint_lab.gen008d_exec import (
        PLAN_RELPATH,
        CompositionRunError,
        assemble_tables,
        execute_plan_item,
        item_path,
        prepare_d0_plan,
        publish_tables,
        require_d0_execution,
        run_d0,
    )

    repo = args.repo or _repo_root()
    root = args.root or _default_generation_008d_root()
    if args.command == "write-plan":
        if args.output is None:
            print("write-plan requires --output", file=sys.stderr)
            return 2
        plan = prepare_d0_plan(repo)
        atomic_write_json(args.output, plan)
        print(json.dumps({"items": len(plan["items"]), "output": str(args.output), "plan_hash": plan["plan_hash"], "weighted_canonical_count": plan["universe"]["weighted_canonical_count"]}, indent=2, sort_keys=True))
        return 0
    relpath = args.relpath or PLAN_RELPATH
    plan_path = args.plan or (repo / PLAN_RELPATH)
    try:
        plan = require_d0_execution(
            repo,
            args.frozen_plan_commit,
            relpath,
            disk_path=plan_path,
            require_remote=not args.allow_unpushed,
        )
    except (FrozenPlanError, CompositionRunError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.command == "verify":
        missing = [item["kind"] for item in plan["items"] if not item_path(root, item).is_file()]
        print(json.dumps({"complete": not missing, "missing_count": len(missing), "plan_hash": plan["plan_hash"]}, indent=2, sort_keys=True))
        return 0 if not missing else 1
    try:
        if args.command == "execute-item":
            matches = [
                item
                for item in plan["items"]
                if item["kind"] == args.kind and item.get("orbit_id") == (args.orbit if args.kind == "orbit" else None)
            ]
            if len(matches) != 1:
                print("execute-item requires --kind orbit --orbit ORB-id, or --kind surface", file=sys.stderr)
                return 2
            payload = execute_plan_item(matches[0])
            path = item_path(root, matches[0])
            atomic_write_json(path, payload)
            print(json.dumps({"item_id": payload["item_id"], "output": str(path), "wall_seconds": payload["wall_seconds"]}, indent=2, sort_keys=True))
            return 0
        if args.command == "run-d0":
            written = run_d0(root, plan)
            print(json.dumps({"items": len(written), "max_wall_seconds": max(row["wall_seconds"] for row in written), "root": str(root), "skipped": sum(1 for row in written if row["skipped"])}, indent=2, sort_keys=True))
            return 0
        if args.command == "assemble":
            payload = assemble_tables(root, plan, repo=repo, frozen_plan_commit=args.frozen_plan_commit)
            if not payload["validation"]["ok"]:
                print(json.dumps(payload["validation"], indent=2, sort_keys=True), file=sys.stderr)
                return 1
            output = args.output or (root / "round-d0-tables.json")
            atomic_write_json(output, {key: value for key, value in payload.items() if key != "tables"})
            hashes = {}
            if args.publish:
                hashes = publish_tables(payload, _lab_root() / "reports")
            print(json.dumps({"output": str(output), "payload_sha256": hashes.get("payload_sha256"), "validation": "ok"}, indent=2, sort_keys=True))
            return 0
    except (CompositionRunError, CompositionError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 2


def _generation_008e(argv: list[str]) -> int:
    if not argv:
        print("usage: python -m rs_constraint_lab generation008e <command>", file=sys.stderr)
        return 2
    parser = argparse.ArgumentParser(prog="rs_constraint_lab generation008e")
    parser.add_argument("command", choices=["write-plan", "execute-item", "run-e0", "assemble", "verify"])
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--plan", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--frozen-plan-commit", default=None)
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--relpath", default=None)
    parser.add_argument("--kind", default=None)
    parser.add_argument("--orbit", default=None)
    parser.add_argument("--allow-unpushed", action="store_true")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args(argv)
    from rs_constraint_lab.durable import atomic_write_json
    from rs_constraint_lab.explore08 import FrozenPlanError
    from rs_constraint_lab.explore08e import ConjunctionError
    from rs_constraint_lab.gen008e_exec import (
        PLAN_RELPATH,
        ConjunctionRunError,
        assemble_tables,
        execute_plan_item,
        item_path,
        prepare_e0_plan,
        publish_tables,
        require_e0_execution,
        run_e0,
    )

    repo = args.repo or _repo_root()
    root = args.root or (_lab_root() / "generated" / "generation-008e" / "round-e0")
    if args.command == "write-plan":
        if args.output is None:
            print("write-plan requires --output", file=sys.stderr)
            return 2
        plan = prepare_e0_plan(repo)
        atomic_write_json(args.output, plan)
        print(json.dumps({"items": len(plan["items"]), "output": str(args.output), "plan_hash": plan["plan_hash"], "weighted_system_count": plan["universe"]["weighted_system_count"]}, indent=2, sort_keys=True))
        return 0
    relpath = args.relpath or PLAN_RELPATH
    plan_path = args.plan or (repo / PLAN_RELPATH)
    try:
        plan = require_e0_execution(repo, args.frozen_plan_commit, relpath, disk_path=plan_path, require_remote=not args.allow_unpushed)
    except (FrozenPlanError, ConjunctionRunError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.command == "verify":
        missing = [item["kind"] for item in plan["items"] if not item_path(root, item).is_file()]
        print(json.dumps({"complete": not missing, "missing_count": len(missing), "plan_hash": plan["plan_hash"]}, indent=2, sort_keys=True))
        return 0 if not missing else 1
    try:
        if args.command == "execute-item":
            matches = [item for item in plan["items"] if item["kind"] == args.kind and item.get("orbit_id") == (args.orbit if args.kind == "orbit" else None)]
            if len(matches) != 1:
                print("execute-item requires --kind orbit --orbit K3-id, or an algebra kind", file=sys.stderr)
                return 2
            payload = execute_plan_item(matches[0], repo=repo)
            path = item_path(root, matches[0])
            atomic_write_json(path, payload)
            print(json.dumps({"item_id": payload["item_id"], "output": str(path), "wall_seconds": payload["wall_seconds"]}, indent=2, sort_keys=True))
            return 0
        if args.command == "run-e0":
            written = run_e0(root, plan, repo=repo)
            print(json.dumps({"items": len(written), "max_wall_seconds": max(row["wall_seconds"] for row in written), "root": str(root), "skipped": sum(1 for row in written if row["skipped"])}, indent=2, sort_keys=True))
            return 0
        if args.command == "assemble":
            payload = assemble_tables(root, plan, frozen_plan_commit=args.frozen_plan_commit)
            if not payload["validation"]["ok"]:
                print(json.dumps(payload["validation"], indent=2, sort_keys=True), file=sys.stderr)
                return 1
            output = args.output or (root / "round-e0-tables.json")
            atomic_write_json(output, {key: value for key, value in payload.items() if key != "tables"})
            hashes = {}
            if args.publish:
                hashes = publish_tables(payload, _lab_root() / "reports")
            print(json.dumps({"output": str(output), "payload_sha256": hashes.get("payload_sha256"), "validation": "ok"}, indent=2, sort_keys=True))
            return 0
    except (ConjunctionRunError, ConjunctionError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 2

