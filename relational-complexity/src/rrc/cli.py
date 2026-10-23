"""Commands: plan, run, status, resume, verify, report, preflight, coherence-view."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from rrc import ENGINE_VERSION
from rrc.model import (
    build_weights,
    lumpability,
    lumpable_closure,
    partition_labels,
    stationary_balanced,
)
from rrc.runner import execute_plan, project_root, worker_main
from rrc.store import IncompatiblePlan, Store, digest


def package_root() -> Path:
    return project_root()


def repo_root() -> Path:
    return package_root().parent


def plan_path(round_id: str) -> Path:
    return package_root() / "plans" / f"{round_id}.json"


def load_plan(round_id: str) -> dict:
    path = plan_path(round_id)
    if not path.is_file():
        raise SystemExit(f"no frozen plan at {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def default_out(round_id: str) -> Path:
    return package_root() / "generated" / round_id


def _print_counts(summary: dict) -> None:
    counts = summary["counts"]
    print(
        f"ran {summary['ran']} item(s) in {summary['elapsed_s']}s; "
        f"complete {counts['complete']}, pending {counts['pending']}, "
        f"failed {counts['failed']}, timeout {counts['timeout']}, "
        f"unresolved {counts['unresolved']}, invalid {counts['invalid']}, "
        f"running {counts['running']}, partial {counts['partial']}"
    )
    print(f"plan_hash {summary['plan_hash']}")
    print(f"output {summary['out']}")


def command_plan(args: argparse.Namespace) -> int:
    plan = load_plan(args.round)
    print(f"round {plan['round_id']}")
    print(f"engine {plan['engine_version']}")
    print(f"items {len(plan['items'])}")
    print(f"watchdog_seconds {plan['watchdog_seconds']}")
    print(f"plan_hash {digest(plan)}")
    print("plan does not execute scientific cells")
    kinds: dict[str, int] = {}
    for item in plan["items"]:
        kinds[item["type"]] = kinds.get(item["type"], 0) + 1
    for kind, count in sorted(kinds.items()):
        print(f"  {kind}: {count}")
    return 0


def command_run(args: argparse.Namespace) -> int:
    plan = load_plan(args.round)
    out = Path(args.out) if args.out else default_out(args.round)
    try:
        summary = execute_plan(
            plan,
            out,
            max_items=args.max_items,
            budget_seconds=args.budget_seconds,
            timeout=args.timeout,
        )
    except IncompatiblePlan as exc:
        print(str(exc), file=sys.stderr)
        return 2
    _print_counts(summary)
    counts = summary["counts"]
    remaining = (
        counts["pending"] + counts["running"] + counts["partial"] + counts["invalid"]
    )
    if counts["failed"] or counts["timeout"] or counts["unresolved"]:
        print("next: inspect failed, timed-out or unresolved items; do not edit their frozen specs")
    elif remaining:
        print(f"next: resume --round {args.round}")
    else:
        print("next: verify, then report")
    if counts["failed"] or counts["timeout"] or counts["unresolved"] or counts["invalid"]:
        return 1
    return 0


def command_status(args: argparse.Namespace) -> int:
    plan = load_plan(args.round)
    out = Path(args.out) if args.out else default_out(args.round)
    if not (out / "manifest.json").exists():
        print("no execution directory")
        print(f"pending {len(plan['items'])}")
        return 1
    try:
        store = Store(out, plan)
        store.prepare()
    except IncompatiblePlan as exc:
        print(str(exc), file=sys.stderr)
        return 2
    counts = store.counts()
    for key in sorted(counts):
        print(f"{key} {counts[key]}")
    remaining = counts["pending"] + counts["running"] + counts["partial"] + counts["invalid"]
    print(f"remaining {remaining}")
    return 0 if remaining == 0 and counts["failed"] == 0 and counts["timeout"] == 0 and counts["unresolved"] == 0 else 1


def _problems(store: Store) -> list[str]:
    problems = []
    for item in store.plan["items"]:
        state = store.classify(item["id"])
        if state != "complete":
            problems.append(f"{item['id']} is {state}")
            continue
        result = store.load_result(item["id"])
        if result.get("engine_version") != ENGINE_VERSION:
            problems.append(f"{item['id']} engine version drifted")
        if item["type"] == "lumpability":
            exact = result.get("exact")
            numerator = (result.get("defect_l1") or {}).get("num")
            if exact != (numerator == "0"):
                problems.append(f"{item['id']} exact flag disagrees with the defect")
            if item.get("role") == "identity_check":
                identity = result.get("identity") or {}
                if not identity.get("ok"):
                    problems.append(f"{item['id']} identity check did not hold")
        if item["type"] == "propagation" and item.get("role") == "identity_check":
            identity = result.get("identity") or {}
            if not identity.get("ok"):
                problems.append(f"{item['id']} propagation identity did not hold")
        if item["type"] == "probe" and result.get("value") != item.get("value") and item.get("mode") == "ok":
            problems.append(f"{item['id']} probe value drifted")
    return problems


def command_verify(args: argparse.Namespace) -> int:
    plan = load_plan(args.round)
    out = Path(args.out) if args.out else default_out(args.round)
    try:
        store = Store(out, plan)
        store.prepare()
    except IncompatiblePlan as exc:
        print(str(exc), file=sys.stderr)
        return 2
    problems = _problems(store)
    counts = store.counts()
    for key in sorted(counts):
        print(f"{key} {counts[key]}")
    for problem in problems:
        print(problem)
    if problems:
        return 1
    print("verified")
    return 0


def command_report(args: argparse.Namespace) -> int:
    plan = load_plan(args.round)
    out = Path(args.out) if args.out else default_out(args.round)
    try:
        store = Store(out, plan)
        store.prepare()
    except IncompatiblePlan as exc:
        print(str(exc), file=sys.stderr)
        return 2
    lines = [
        f"# {plan['round_id']} report",
        "",
        "Generated from completed item files. Items that are not complete are listed as not run.",
        "Exact means strong lumpability (defect zero), not a small stationary distance.",
        "",
        "| Item | Type | Role | State | Exact or status | Defect L1 | Blocks | Closure blocks |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in plan["items"]:
        state = store.classify(item["id"])
        if state != "complete":
            lines.append(f"| {item['id']} | {item['type']} | {item.get('role', '')} | {state} | not run |  |  |  |")
            continue
        result = store.load_result(item["id"])
        if item["type"] == "lumpability":
            defect = result["defect_l1"]["float"]
            closure = result.get("closure") or {}
            lines.append(
                f"| {item['id']} | lumpability | {item.get('role', '')} | complete | {result['exact']} | {defect} | {result['n_blocks']} | {closure.get('n_blocks', '')} |"
            )
        elif item["type"] == "propagation":
            lines.append(
                f"| {item['id']} | propagation | {item.get('role', '')} | {result['status']} | tv {result['stationary_tv']} |  |  |  |"
            )
        else:
            lines.append(f"| {item['id']} | {item['type']} |  | {state} | {result.get('status')} |  |  |  |")
    text = "\n".join(lines) + "\n"
    sys.stdout.write(text)
    if args.write:
        destination = Path(args.write)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")
    return 0


def command_preflight(args: argparse.Namespace) -> int:
    """Time calibration kernels. This is not an RRC scientific cell."""
    sizes = [int(value) for value in args.sizes.split(",")]
    records = []
    for n in sizes:
        rule = {"family": "calibration_weights"}
        partition = {"kind": "hide_subset", "members": list(range(max(1, n - 1)))}
        started = time.perf_counter()
        weights = build_weights(n, rule)
        build_s = time.perf_counter() - started
        started = time.perf_counter()
        labels, blocks, _hidden, _visible = partition_labels(n, partition, "interface")
        report = lumpability(weights, labels)
        lump_s = time.perf_counter() - started
        closure_s = None
        closure_blocks = None
        if n <= args.closure_max_n:
            started = time.perf_counter()
            closure = lumpable_closure(weights, labels)
            closure_s = time.perf_counter() - started
            closure_blocks = closure["n_blocks"]
        stationary_s = None
        converged = None
        if n <= args.stationary_max_n:
            started = time.perf_counter()
            solved = stationary_balanced(weights, "uniform", 1e-10, 20000)
            stationary_s = time.perf_counter() - started
            converged = solved["converged"]
        records.append(
            {
                "n": n,
                "states": int(weights.shape[0]),
                "edges": int(weights.shape[1]),
                "blocks": blocks,
                "build_s": round(build_s, 6),
                "lumpability_s": round(lump_s, 6),
                "closure_s": None if closure_s is None else round(closure_s, 6),
                "closure_blocks": closure_blocks,
                "stationary_s": None if stationary_s is None else round(stationary_s, 6),
                "stationary_converged": converged,
                "defect_recorded": False,
                "scientific": False,
                "rule_family": "calibration_weights",
            }
        )
        # The defect is intentionally omitted. Calibration is a timing cell.
        del report
    payload = {
        "scientific": False,
        "engine_version": ENGINE_VERSION,
        "records": records,
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.out:
        destination = Path(args.out)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    slow = [
        row["n"]
        for row in records
        if (row["lumpability_s"] or 0) > 120
        or (row["closure_s"] or 0) > 120
        or (row["stationary_s"] or 0) > 120
    ]
    if slow:
        print(f"sizes over the 120-second item budget: {slow}", file=sys.stderr)
        return 1
    return 0


def command_coherence_view(_args: argparse.Namespace) -> int:
    source = repo_root() / "constraint-lab" / "src"
    sys.path.insert(0, str(source))
    from rs_constraint_lab.coherence import write_views

    summary = write_views(package_root() / "coherence")
    print(json.dumps(summary, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rrc")
    sub = parser.add_subparsers(dest="command", required=True)

    plan = sub.add_parser("plan", help="show a frozen plan without running it")
    plan.add_argument("--round", required=True)
    plan.set_defaults(func=command_plan)

    for name in ("run", "resume"):
        command = sub.add_parser(name, help="execute pending items inside a budget")
        command.add_argument("--round", required=True)
        command.add_argument("--out", default=None)
        command.add_argument("--max-items", type=int, default=10**9)
        command.add_argument("--budget-seconds", type=float, default=10**9)
        command.add_argument("--timeout", type=float, default=None)
        command.set_defaults(func=command_run)

    status = sub.add_parser("status", help="count complete, pending, failed and invalid items")
    status.add_argument("--round", required=True)
    status.add_argument("--out", default=None)
    status.set_defaults(func=command_status)

    verify = sub.add_parser("verify", help="validate results against the frozen plan")
    verify.add_argument("--round", required=True)
    verify.add_argument("--out", default=None)
    verify.set_defaults(func=command_verify)

    report = sub.add_parser("report", help="summarise completed items")
    report.add_argument("--round", required=True)
    report.add_argument("--out", default=None)
    report.add_argument("--write", default=None)
    report.set_defaults(func=command_report)

    preflight = sub.add_parser("preflight", help="time calibration kernels; not a scientific round")
    preflight.add_argument("--sizes", default="4,5")
    preflight.add_argument("--closure-max-n", type=int, default=5)
    preflight.add_argument("--stationary-max-n", type=int, default=5)
    preflight.add_argument("--out", default=None)
    preflight.set_defaults(func=command_preflight)

    view = sub.add_parser("coherence-view", help="regenerate the ledger view with the laboratory renderer")
    view.set_defaults(func=command_coherence_view)

    worker = sub.add_parser("worker", help=argparse.SUPPRESS)
    worker.set_defaults(func=lambda _args: worker_main())
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
