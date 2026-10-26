"""Commands: plan, run, status, resume, verify, report, preflight, coherence-view."""

from __future__ import annotations

import argparse
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

from rrc import ENGINE_VERSION
from rrc.items import execute_lumpability, execute_propagation
from rrc.constraints import kernel_fingerprint, resolve_carrier, weight_table_hash
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
        if result.get("engine_version") != store.plan.get("engine_version"):
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
        if item["type"] == "atlas_core":
            problems.extend(_atlas_problems(item, result))
        if item["type"] == "composition_observation":
            problems.extend(_composition_problems(item, result))
        if item["type"] == "successive_observation":
            problems.extend(_successive_problems(item, result))
        if item["type"] == "event_kernel":
            problems.extend(_event_kernel_problems(item, result))
        if item["type"] == "strict_event_comparison":
            problems.extend(_strict_event_problems(item, result))
        if item["type"] == "event_horizon":
            problems.extend(_event_horizon_problems(item, result))
    return problems


def _composition_problems(item: dict, result: dict) -> list[str]:
    """Record consistency for one label map. This does not recompute the law."""
    problems = []
    name = item["id"]
    if result.get("observation") != item.get("observation"):
        problems.append(f"{name} observation drifted")
    if result.get("new_state") is not False:
        problems.append(f"{name} reports new state")
    if result.get("further_label") != "undefined":
        problems.append(f"{name} further label is not undefined")
    exact = result.get("exact")
    numerator = (result.get("defect_l1") or {}).get("num")
    if exact != (numerator == "0"):
        problems.append(f"{name} exact flag disagrees with the defect")
    n_states = result.get("n_states")
    n_edges = result.get("n_edges")
    if not isinstance(n_states, int) or not isinstance(n_edges, int) or n_states != (1 << n_edges):
        problems.append(f"{name} state count is not 2 to the carrier size")
    if result.get("n_blocks") != result.get("n_distinct_labels"):
        problems.append(f"{name} block count disagrees with the label count")
    if result.get("kernel_method") != "row_gcd_halt_self_loop":
        problems.append(f"{name} kernel method is not the halt_self_loop reduction")
    quotient = result.get("quotient")
    if isinstance(quotient, dict):
        defined = quotient.get("defined") is True
        if exact != defined:
            problems.append(f"{name} quotient flag disagrees with exactness")
        rows = quotient.get("rows")
        if exact:
            if not isinstance(rows, list) or len(rows) != result.get("n_blocks"):
                problems.append(f"{name} quotient shape disagrees with the block count")
            else:
                for row in rows:
                    total = sum(Fraction(int(cell["num"]), int(cell["den"])) for cell in row)
                    if total != 1:
                        problems.append(f"{name} quotient row does not sum to 1")
                        break
        elif rows is not None:
            problems.append(f"{name} stores a quotient row without strong lumpability")
    problems.extend(_stored_table_problems(name, result))
    return problems


def _successive_problems(item: dict, result: dict) -> list[str]:
    """Record consistency for a sequence of label maps. This does not recompute them."""
    problems = []
    name = item["id"]
    if result.get("observations") != item.get("observations"):
        problems.append(f"{name} observations drifted")
    if result.get("new_state") is not False:
        problems.append(f"{name} reports new state")
    if result.get("conditional_exactness") != "not_computed":
        problems.append(f"{name} computes conditional exactness")
    if result.get("history_dependent") != "not_computed":
        problems.append(f"{name} computes a history-dependent kernel")
    stages = result.get("stages")
    direct = result.get("direct")
    names = item.get("observations")
    if (
        not isinstance(stages, list)
        or not isinstance(direct, list)
        or not isinstance(names, list)
        or len(stages) != len(names)
        or len(direct) != len(stages)
    ):
        problems.append(f"{name} stage count disagrees with the named maps")
        return problems
    prefix = 0
    for stage, law in zip(stages, direct):
        if stage.get("new_state") is not False:
            problems.append(f"{name} stage reports new state")
        problems.extend(_exact_row_problems(name, stage.get("exact"), stage.get("defect_l1"), stage.get("quotient_rows")))
        problems.extend(_exact_row_problems(name, law.get("exact"), law.get("defect_l1"), law.get("quotient_rows"), allow_none=False))
        if stage.get("exact") is True and len(stage.get("quotient_rows") or []) != stage.get("n_distinct_labels"):
            problems.append(f"{name} sequential quotient shape disagrees with its labels")
        if law.get("exact") is True and len(law.get("quotient_rows") or []) != law.get("n_distinct_labels"):
            problems.append(f"{name} direct quotient shape disagrees with its labels")
        if stage.get("typed") is True and stage.get("exact") is True and prefix == stage.get("depth"):
            prefix += 1
        elif stage.get("exact") is None and stage.get("quotient_defined") is not False:
            problems.append(f"{name} undefined stage claims a quotient")
    if result.get("exact_prefix") != prefix:
        problems.append(f"{name} exact prefix disagrees with the leading exact stages")
    agreement = result.get("agreement")
    kernels = result.get("kernels_agree")
    if agreement == "exact" and kernels is not True:
        problems.append(f"{name} agreement disagrees with the kernel flag")
    elif agreement == "disagreement" and kernels is not False:
        problems.append(f"{name} disagreement flag is not false")
    elif agreement == "undefined" and kernels is not None:
        problems.append(f"{name} undefined agreement stores a kernel flag")
    elif agreement not in {"exact", "disagreement", "undefined"}:
        problems.append(f"{name} agreement is {agreement}")
    if prefix < 2 and agreement != "undefined":
        problems.append(f"{name} claims kernel agreement before two exact stages")
    if prefix >= 2 and agreement == "undefined":
        problems.append(f"{name} leaves two exact stages without an agreement")
    n_states = result.get("n_states")
    n_edges = result.get("n_edges")
    if not isinstance(n_states, int) or not isinstance(n_edges, int) or n_states != (1 << n_edges):
        problems.append(f"{name} state count is not 2 to the carrier size")
    problems.extend(_stored_table_problems(name, result))
    return problems


def _exact_row_problems(name: str, exact, defect, rows, allow_none: bool = True) -> list[str]:
    problems = []
    numerator = defect.get("num") if isinstance(defect, dict) else None
    if exact is True:
        if numerator != "0" or not isinstance(rows, list) or not rows:
            problems.append(f"{name} exact stage disagrees with its rows")
        else:
            for row in rows:
                total = sum(Fraction(int(cell["num"]), int(cell["den"])) for cell in row)
                if total != 1:
                    problems.append(f"{name} quotient row does not sum to 1")
                    break
    elif exact is False:
        if numerator == "0" or rows is not None or not isinstance(defect, dict):
            problems.append(f"{name} inexact stage stores a quotient or a zero defect")
    elif exact is None and allow_none:
        if defect is not None or rows is not None:
            problems.append(f"{name} undefined stage stores a defect or a row")
    else:
        problems.append(f"{name} exact flag is {exact}")
    return problems


def _atlas_problems(item: dict, result: dict) -> list[str]:
    """Record consistency. This does not recompute the weight table."""
    problems = []
    name = item["id"]
    constraints = item.get("constraints")
    book = result.get("bookkeeping") or {}
    if not isinstance(constraints, list):
        return [f"{name} has no constraint list"]
    if book.get("declared_cardinality") != len(constraints):
        problems.append(f"{name} declared cardinality drifted")
    if book.get("j_positive", 0) + book.get("j_prohibit", 0) != len(constraints):
        problems.append(f"{name} J fields do not add up to the constraint list")
    n_states = result.get("n_states")
    n_edges = result.get("n_edges")
    if not isinstance(n_states, int) or not isinstance(n_edges, int) or n_states != (1 << n_edges):
        problems.append(f"{name} state count is not 2 to the carrier size")
    try:
        edges, _kind = resolve_carrier(item["n"], item["carrier"])
    except (TypeError, ValueError, KeyError):
        problems.append(f"{name} carrier does not resolve")
        edges = None
    if edges is not None and len(edges) != n_edges:
        problems.append(f"{name} edge count drifted from the carrier")
    digest = result.get("weight_sha256")
    if not isinstance(digest, str) or len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
        problems.append(f"{name} weight hash is missing")
    positive = result.get("positive_transitions")
    zeros = result.get("zero_cells")
    if not isinstance(positive, int) or not isinstance(zeros, int) or positive + zeros != n_states * n_edges:
        problems.append(f"{name} support cells do not cover the table")
    occupation = result.get("occupation") or {}
    status = occupation.get("status")
    classes = (result.get("classes") or {}).get("recurrent_classes")
    if status == "unique":
        if classes != 1:
            problems.append(f"{name} reports a unique law with several recurrent classes")
        if "mean_present_edges" not in occupation:
            problems.append(f"{name} unique law has no mean")
    elif status == "not_unique":
        if "mean_present_edges" in occupation or "distribution" in occupation:
            problems.append(f"{name} reports a mean for a non-unique law")
    else:
        problems.append(f"{name} occupation status is {status}")
    if result.get("engine_version") not in {"rrc-0.1.0", "rrc-0.2.0"}:
        problems.extend(_stored_table_problems(name, result))
    return problems


def _stored_table_problems(name: str, result: dict) -> list[str]:
    """Checksum the stored integer table. This does not recompile the rule."""
    problems = []
    raw = result.get("weights")
    if not isinstance(raw, list) or not raw:
        return [f"{name} does not store its weight table"]
    try:
        weights = np.asarray(raw, dtype=np.int64)
    except (TypeError, ValueError):
        return [f"{name} weight table is not integral"]
    if weights.shape != (result.get("n_states"), result.get("n_edges")):
        problems.append(f"{name} stored weight table has the wrong shape")
        return problems
    if weight_table_hash(weights) != result.get("weight_sha256"):
        problems.append(f"{name} weight hash does not match the stored table")
    if result.get("kernel_method") != "row_gcd_halt_self_loop":
        problems.append(f"{name} kernel method is not the halt_self_loop reduction")
    elif kernel_fingerprint(weights) != result.get("kernel_sha256"):
        problems.append(f"{name} kernel hash does not match the stored table")
    digest = result.get("structure_sha256")
    if not isinstance(digest, str) or len(digest) != 64:
        problems.append(f"{name} structure hash is missing")
    return problems


_EVENT_COMPLETIONS = {
    "halt_self_loop",
    "noop_event",
    "normalised_events",
    "normalised_events_including_noop",
}


def _event_kernel_problems(item: dict, result: dict) -> list[str]:
    """Record consistency for one declared event list. This does not rebuild it."""
    problems = []
    name = item["id"]
    if result.get("type") != "event_kernel":
        problems.append(f"{name} type drifted")
    if result.get("method") != "event-kernel-0.1.0":
        problems.append(f"{name} method drifted")
    if result.get("clock") != "one_declared_event":
        problems.append(f"{name} clock drifted")
    if result.get("halt_self_loop_is_event") is not False:
        problems.append(f"{name} treats a halt self-loop as an event")
    if result.get("new_primitive") is not False:
        problems.append(f"{name} reports a new primitive")
    if result.get("family") != item.get("family"):
        problems.append(f"{name} family drifted")
    if result.get("catalogue") != item.get("catalogue"):
        problems.append(f"{name} catalogue drifted")
    if "occupation" in result or "weight_sha256" in result or "kernel_method" in result:
        problems.append(f"{name} stores a carrier weight table")
    n_states = item.get("n_states")
    if result.get("n_states") != n_states or isinstance(n_states, bool) or not isinstance(n_states, int):
        problems.append(f"{name} state count drifted")
        return problems
    if "bit_width" in item and result.get("bit_width") != item["bit_width"]:
        problems.append(f"{name} bit width drifted")
    if "bit_width" not in item and "bit_width" in result:
        problems.append(f"{name} stores a bit width")
    probabilities = result.get("probabilities")
    aggregated = result.get("aggregated_weights")
    completions = result.get("completions")
    enabled = result.get("enabled_event_counts")
    row_sums = result.get("row_sums")
    rows = (probabilities, aggregated, completions, enabled, row_sums)
    if not all(isinstance(value, list) and len(value) == n_states for value in rows):
        problems.append(f"{name} row count drifted")
        return problems
    for state in range(n_states):
        row = probabilities[state]
        weights = aggregated[state]
        if not isinstance(row, list) or len(row) != n_states or not isinstance(weights, list) or len(weights) != n_states:
            problems.append(f"{name} row shape drifted")
            return problems
        completion = completions[state]
        if completion not in _EVENT_COMPLETIONS:
            problems.append(f"{name} completion is {completion}")
            return problems
        count = enabled[state]
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            problems.append(f"{name} enabled count is not a nonnegative integer")
            return problems
        total_weight = 0
        positive_cells = 0
        for weight in weights:
            if isinstance(weight, bool) or not isinstance(weight, int) or weight < 0:
                problems.append(f"{name} aggregated weight is not a nonnegative integer")
                return problems
            total_weight += weight
            if weight:
                positive_cells += 1
        if row_sums[state] != total_weight:
            problems.append(f"{name} row sum disagrees with the aggregated weights")
            return problems
        if (count == 0) != (total_weight == 0):
            problems.append(f"{name} enabled count disagrees with the row sum")
            return problems
        if count < positive_cells:
            problems.append(f"{name} enabled count is below the positive cells")
            return problems
        total = Fraction(0)
        for target, cell in enumerate(row):
            if not isinstance(cell, dict) or "num" not in cell or "den" not in cell:
                problems.append(f"{name} probability is not a fraction")
                return problems
            probability = Fraction(int(cell["num"]), int(cell["den"]))
            total += probability
            if total_weight == 0:
                expected = Fraction(1 if target == state else 0)
            else:
                expected = Fraction(int(weights[target]), int(total_weight))
            if probability != expected:
                problems.append(f"{name} probability disagrees with the aggregated weights")
                return problems
        if total != 1:
            problems.append(f"{name} probability row does not sum to 1")
            return problems
        diagonal = weights[state]
        if completion == "halt_self_loop" and (total_weight != 0 or count != 0):
            problems.append(f"{name} halt row has positive weight")
        elif completion == "noop_event" and (total_weight == 0 or diagonal != total_weight):
            problems.append(f"{name} noop row is not diagonal")
        elif completion == "normalised_events" and (total_weight == 0 or diagonal != 0):
            problems.append(f"{name} event row stores a self-loop weight")
        elif completion == "normalised_events_including_noop" and (diagonal <= 0 or diagonal >= total_weight):
            problems.append(f"{name} mixed row does not split the self-loop")
    return problems


def _probability_rows_sum(name: str, probabilities, n_states: int) -> list[str]:
    problems = []
    if not isinstance(probabilities, list) or len(probabilities) != n_states:
        return [f"{name} row count drifted"]
    for row in probabilities:
        if not isinstance(row, list) or len(row) != n_states:
            return [f"{name} row shape drifted"]
        total = Fraction(0)
        for cell in row:
            if not isinstance(cell, dict) or "num" not in cell or "den" not in cell:
                return [f"{name} probability is not a fraction"]
            total += Fraction(int(cell["num"]), int(cell["den"]))
        if total != 1:
            problems.append(f"{name} probability row does not sum to 1")
    return problems


def _strict_event_problems(item: dict, result: dict) -> list[str]:
    """Record consistency for one strict event law. This does not rebuild it."""
    problems = []
    name = item["id"]
    if result.get("type") != "strict_event_comparison":
        problems.append(f"{name} type drifted")
    if result.get("method") != "event-kernel-0.2.0":
        problems.append(f"{name} method drifted")
    if result.get("clock") != "one_declared_event":
        problems.append(f"{name} clock drifted")
    if result.get("new_primitive") is not False:
        problems.append(f"{name} reports a new primitive")
    if result.get("halt_self_loop_is_event") is not False:
        problems.append(f"{name} treats a halt self-loop as an event")
    if "occupation" in result or "weight_sha256" in result or "stationary" in result:
        problems.append(f"{name} stores a carrier weight table")
    if result.get("family") != item.get("family"):
        problems.append(f"{name} family drifted")
    n_states = item.get("n_states")
    if result.get("n_states") != n_states:
        problems.append(f"{name} state count drifted")
        return problems
    if "bit_width" in item and result.get("bit_width") != item["bit_width"]:
        problems.append(f"{name} bit width drifted")
    problems.extend(_probability_rows_sum(name, result.get("probabilities"), n_states))
    events = result.get("events")
    if not isinstance(events, list) or len(events) != result.get("event_count"):
        problems.append(f"{name} event count drifted")
        return problems
    width = item.get("bit_width")
    for event in events:
        kind = event.get("kind")
        if width is None:
            continue
        distance = (int(event["source"]) ^ int(event["target"])).bit_count()
        if kind == "toggle" and distance != 1:
            problems.append(f"{name} toggle distance drifted")
        elif kind == "joint" and distance < 2:
            problems.append(f"{name} joint distance drifted")
        elif kind == "noop" and distance != 0:
            problems.append(f"{name} noop distance drifted")
        elif kind == "transition" and distance == 0:
            problems.append(f"{name} transition distance drifted")
    compared = result.get("correspondence")
    if item.get("image_map") is None:
        if compared is not None:
            problems.append(f"{name} stores a correspondence without a map")
    else:
        if not isinstance(compared, dict):
            problems.append(f"{name} correspondence is missing")
            return problems
        invariant = compared.get("image_invariant")
        if compared.get("conjugate") is True and invariant is not True:
            problems.append(f"{name} conjugacy claims a leaking image")
        if invariant is not True and compared.get("restricted_rows") is not None:
            problems.append(f"{name} leaking image stores restricted rows")
    return problems


def _event_horizon_problems(item: dict, result: dict) -> list[str]:
    """Record consistency for one horizon. This does not rebuild the power."""
    problems = []
    name = item["id"]
    if result.get("type") != "event_horizon":
        problems.append(f"{name} type drifted")
    if result.get("method") != "event-kernel-0.2.0":
        problems.append(f"{name} method drifted")
    if result.get("clock") != "one_declared_event":
        problems.append(f"{name} clock drifted")
    if result.get("new_primitive") is not False:
        problems.append(f"{name} reports a new primitive")
    if result.get("intervention") is not None:
        problems.append(f"{name} stores an intervention")
    if "occupation" in result or "stationary" in result or "stationary_tv" in result:
        problems.append(f"{name} stores a stationary law")
    if result.get("horizon") != item.get("horizon"):
        problems.append(f"{name} horizon drifted")
    if result.get("initial_state") != item.get("initial_state"):
        problems.append(f"{name} initial state drifted")
    if result.get("subset") != item.get("subset"):
        problems.append(f"{name} subset drifted")
    n_states = item.get("n_states")
    if result.get("n_states") != n_states:
        problems.append(f"{name} state count drifted")
        return problems
    problems.extend(_probability_rows_sum(name, result.get("probabilities"), n_states))
    distribution = result.get("horizon_distribution")
    if not isinstance(distribution, list) or len(distribution) != n_states:
        problems.append(f"{name} horizon distribution drifted")
    else:
        total = Fraction(0)
        for cell in distribution:
            if not isinstance(cell, dict) or "num" not in cell:
                problems.append(f"{name} horizon cell is not a fraction")
                return problems
            total += Fraction(int(cell["num"]), int(cell["den"]))
        if total != 1:
            problems.append(f"{name} horizon distribution does not sum to 1")
    lump = result.get("lumpability")
    if not isinstance(lump, dict):
        problems.append(f"{name} lumpability is missing")
        return problems
    exact = lump.get("exact")
    numerator = (lump.get("defect_l1") or {}).get("num")
    if exact != (numerator == "0"):
        problems.append(f"{name} exact flag disagrees with the defect")
    if exact is True and not isinstance(lump.get("rows"), list):
        problems.append(f"{name} exact partition stores no rows")
    if exact is not True and lump.get("rows") is not None:
        problems.append(f"{name} inexact partition stores rows")
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


def _report_atlas(plan: dict, store: Store) -> str:
    lines = [
        f"# {plan['round_id']} report",
        "",
        "Generated from completed item files. A weight hash identifies the integer table.",
        "Occupation is reported only when the stationary law is unique.",
        "The carrier and the imposed rule-dependency path are instruments.",
        "",
        "| Item | N | Edges | Declared | Effective | Removal-sensitive | max K | Classes | Deadlocks | Occupation | Hash |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    show_kernel = False
    for item in plan["items"]:
        if store.classify(item["id"]) != "complete":
            continue
        if "kernel_sha256" in store.load_result(item["id"]):
            show_kernel = True
            break
    if show_kernel:
        lines[-2] = lines[-2] + " Kernel |"
        lines[-1] = lines[-1] + " --- |"
    for item in plan["items"]:
        state = store.classify(item["id"])
        if state != "complete":
            gap = " |  |" if show_kernel else " |"
            lines.append(f"| {item['id']} | {item.get('n', '')} |  |  |  |  |  |  |  | {state} |  {gap}")
            continue
        result = store.load_result(item["id"])
        book = result["bookkeeping"]
        occupation = result["occupation"]["status"]
        kernel = ""
        if show_kernel:
            kernel = " `{0}` |".format(result.get("kernel_sha256", "")[:12])
        lines.append(
            "| {id} | {n} | {edges} | {declared} | {effective} | {sensitive} | {k} | {classes} | {dead} | {occupation} | `{digest}` |{kernel}".format(
                id=item["id"],
                n=result["n"],
                edges=result["n_edges"],
                declared=book["declared_cardinality"],
                effective=book["effective_cardinality"],
                sensitive=book["removal_sensitive_count"],
                k=book["max_positive_k"],
                classes=result["classes"]["recurrent_classes"],
                dead=result["classes"]["deadlock_states"],
                occupation=occupation,
                digest=result["weight_sha256"][:12],
                kernel=kernel,
            )
        )
    return "\n".join(lines) + "\n"


def _report_successive(plan: dict, store: Store) -> str:
    lines = [
        f"# {plan['round_id']} report",
        "",
        "Generated from completed item files. A sequential stage is exact only when its quotient is defined.",
        "Direct laws are maps of the carrier. An undefined sequential stage does not store a kernel.",
        "",
        "| Item | Maps | Prefix | Agreement | Direct exact | Sequential exact | Hash |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in plan["items"]:
        state = store.classify(item["id"])
        if state != "complete":
            lines.append(f"| {item['id']} | {', '.join(item.get('observations', []))} |  |  |  |  | {state} |")
            continue
        result = store.load_result(item["id"])
        direct = ",".join("exact" if law["exact"] else "not exact" for law in result["direct"])
        sequential = ",".join(
            "exact" if stage["exact"] is True else ("not exact" if stage["exact"] is False else "undefined")
            for stage in result["stages"]
        )
        lines.append(
            "| {id} | {maps} | {prefix} | {agreement} | {direct} | {sequential} | `{digest}` |".format(
                id=item["id"],
                maps=", ".join(result["observations"]),
                prefix=result["exact_prefix"],
                agreement=result["agreement"],
                direct=direct,
                sequential=sequential,
                digest=result["weight_sha256"][:12],
            )
        )
    return "\n".join(lines) + "\n"


def _report_composition(plan: dict, store: Store) -> str:
    lines = [
        f"# {plan['round_id']} report",
        "",
        "Generated from completed item files. Exact means strong lumpability of the named label map.",
        "The label is a function of the current carrier state. A positive defect is not an approximate closure.",
        "",
        "| Item | Observation | States | Labels | Exact | Defect | Injective | Hash |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in plan["items"]:
        state = store.classify(item["id"])
        if state != "complete":
            lines.append(f"| {item['id']} | {item.get('observation', '')} |  |  |  |  |  | {state} |")
            continue
        result = store.load_result(item["id"])
        lines.append(
            "| {id} | {observation} | {states} | {labels} | {exact} | {defect} | {injective} | `{digest}` |".format(
                id=item["id"],
                observation=result["observation"],
                states=result["n_states"],
                labels=result["n_distinct_labels"],
                exact=result["exact"],
                defect=result["defect_l1"]["float"],
                injective=result["injective"],
                digest=result["weight_sha256"][:12],
            )
        )
    return "\n".join(lines) + "\n"


def _report_strict_event(plan: dict, store: Store) -> str:
    lines = [
        f"# {plan['round_id']} report",
        "",
        "Generated from completed item files. Probabilities are the stored numerator and denominator.",
        "A correspondence is recorded only when the item names an image map.",
        "A leaking image stores no restricted rows. No occupation is stored.",
        "",
        "| Item | Family | States | Events | Invariant | Conjugate |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in plan["items"]:
        state = store.classify(item["id"])
        if state != "complete":
            lines.append(f"| {item['id']} | {item.get('family', '')} |  |  |  | {state} |")
            continue
        result = store.load_result(item["id"])
        compared = result.get("correspondence") or {}
        lines.append(
            f"| {result['item_id']} | {result['family']} | {result['n_states']} | {result['event_count']} | {compared.get('image_invariant', '')} | {compared.get('conjugate', '')} |"
        )
    return "\n".join(lines) + "\n"


def _report_event_horizon(plan: dict, store: Store) -> str:
    lines = [
        f"# {plan['round_id']} report",
        "",
        "Generated from completed item files. The horizon distribution is the stored power of the one-step kernel.",
        "An inexact partition stores no quotient rows. No intervention operator is defined.",
        "",
        "| Item | Family | Horizon | Subset | Exact | Defect |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in plan["items"]:
        state = store.classify(item["id"])
        if state != "complete":
            lines.append(f"| {item['id']} | {item.get('family', '')} |  |  |  | {state} |")
            continue
        result = store.load_result(item["id"])
        lump = result["lumpability"]
        lines.append(
            "| {id} | {family} | {horizon} | {subset} | {exact} | {defect} |".format(
                id=result["item_id"],
                family=result["family"],
                horizon=result["horizon"],
                subset=_fraction_text(result["subset_probability"]),
                exact=lump["exact"],
                defect=_fraction_text(lump["defect_l1"]),
            )
        )
    return "\n".join(lines) + "\n"


def command_report(args: argparse.Namespace) -> int:
    plan = load_plan(args.round)
    out = Path(args.out) if args.out else default_out(args.round)
    try:
        store = Store(out, plan)
        store.prepare()
    except IncompatiblePlan as exc:
        print(str(exc), file=sys.stderr)
        return 2
    kinds = {item["type"] for item in plan["items"]}
    if kinds == {"successive_observation"}:
        text = _report_successive(plan, store)
        sys.stdout.write(text)
        if args.write:
            destination = Path(args.write)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(text, encoding="utf-8")
        return 0
    if kinds == {"composition_observation"}:
        text = _report_composition(plan, store)
        sys.stdout.write(text)
        if args.write:
            destination = Path(args.write)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(text, encoding="utf-8")
        return 0
    if kinds == {"event_kernel"}:
        text = _report_event_kernel(plan, store)
        sys.stdout.write(text)
        if args.write:
            destination = Path(args.write)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(text, encoding="utf-8")
        return 0
    if kinds == {"strict_event_comparison"}:
        text = _report_strict_event(plan, store)
        sys.stdout.write(text)
        if args.write:
            destination = Path(args.write)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(text, encoding="utf-8")
        return 0
    if kinds == {"event_horizon"}:
        text = _report_event_horizon(plan, store)
        sys.stdout.write(text)
        if args.write:
            destination = Path(args.write)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(text, encoding="utf-8")
        return 0
    if kinds == {"atlas_core"}:
        text = _report_atlas(plan, store)
        sys.stdout.write(text)
        if args.write:
            destination = Path(args.write)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(text, encoding="utf-8")
        return 0
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


def _fraction_text(cell: dict) -> str:
    numerator = str(cell["num"])
    denominator = str(cell["den"])
    if denominator == "1":
        return numerator
    return f"{numerator}/{denominator}"


def _report_event_kernel(plan: dict, store: Store) -> str:
    lines = [
        f"# {plan['round_id']} report",
        "",
        "Generated from completed item files. Probabilities are the stored numerator and denominator.",
        "A halt self-loop is a completion. A no-op is an event. No occupation is stored.",
        "",
        "| Item | Family | States | Events | Completions |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in plan["items"]:
        state = store.classify(item["id"])
        if state != "complete":
            lines.append(f"| {item['id']} | {item.get('family', '')} |  |  | {state} |")
            continue
        result = store.load_result(item["id"])
        completions = ", ".join(result["completions"])
        lines.append(
            f"| {result['item_id']} | {result['family']} | {result['n_states']} | {result['event_count']} | {completions} |"
        )
    lines.extend(["", "## Probabilities", ""])
    for item in plan["items"]:
        if store.classify(item["id"]) != "complete":
            continue
        result = store.load_result(item["id"])
        lines.append(f"### {item['id']}")
        lines.append("")
        for index, row in enumerate(result["probabilities"]):
            rendered = ", ".join(_fraction_text(cell) for cell in row)
            lines.append(f"State {index}: {rendered}.")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


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
        started = time.perf_counter()
        bundle = execute_lumpability(
            {
                "id": f"calibration-bundle-{n}",
                "round_id": "preflight",
                "n": n,
                "role": "calibration",
                "rule": {"family": "calibration_weights"},
                "partition": partition,
                "augmentations": ["edge_count", "parity", "interface_wedge_counts"],
                "closure": n <= args.closure_max_n,
            }
        )
        bundle_s = time.perf_counter() - started
        propagation_s = None
        if n <= args.stationary_max_n:
            started = time.perf_counter()
            propagation = execute_propagation(
                {
                    "id": f"calibration-propagation-{n}",
                    "round_id": "preflight",
                    "n": n,
                    "tolerance": 1e-12,
                    "cross_tolerance": 1e-8,
                    "max_iter": 10000,
                    "dense_max_states": 1024,
                    "base_rule": {"family": "calibration_weights"},
                    "perturbed_rule": {"family": "unconstrained"},
                }
            )
            propagation_s = time.perf_counter() - started
            del propagation
        records.append(
            {
                "n": n,
                "states": int(weights.shape[0]),
                "edges": int(weights.shape[1]),
                "blocks": blocks,
                "build_s": round(build_s, 6),
                "lumpability_s": round(lump_s, 6),
                "closure_s": None if closure_s is None else round(closure_s, 6),
                "stationary_s": None if stationary_s is None else round(stationary_s, 6),
                "stationary_converged": converged,
                "bundle_s": round(bundle_s, 6),
                "bundle_elapsed_reported_s": bundle["elapsed_s"],
                "propagation_bundle_s": None if propagation_s is None else round(propagation_s, 6),
                "defect_recorded": False,
                "scientific": False,
                "rule_family": "calibration_weights",
            }
        )
        # Scientific fields of the calibration bundle are discarded.
        del report
        del bundle
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
