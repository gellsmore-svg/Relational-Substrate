"""Predeclared scenarios; expected results are calculated only by this harness."""

import argparse
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict
import gzip
import json
from pathlib import Path
import time

from .engine import Config, Engine, ResourceLimit, digest, snapshot, structural
from .metrics import summarize
from .numbers import decode, encode
from .operations import Value, add, divide, multiply, subtract
from .provenance import ROOT, archive_sources, manifest, timestamp, write_json
from .radix import decode_decimal, encode_decimal, resolve, view
from .verification import expected_binary


def scenarios(config: dict) -> list[dict]:
    cells = []
    n = config["runs_per_cell"]

    def cell(experiment, label, kind="arithmetic", runs=n, **kwargs):
        cells.append({"experiment": experiment, "label": label, "kind": kind,
                      "runs": runs, **kwargs})

    for identity in [0, 1, 7, 9]:
        cell("SC-002", f"identity-{identity}", kind="identity", a=identity, perturb="neutral")
    for strength in config["strengths"]:
        cell("SC-003", f"identity-strength-{strength}", kind="identity", a=7,
             perturb="neutral", strength=strength, fault_rate=config["fault_rate"])
    cell("SC-004", "first-addition", op="add", a=3, b=4)
    for a, b in [(3, 4), (17, 28)]:
        cell("SC-005", f"trajectory-{a}-{b}", runs=config["trajectory_runs"], op="add", a=a, b=b)
    for strength in config["strengths"]:
        cell("SC-006", f"addition-strength-{strength}", op="add", a=3, b=4,
             strength=strength, fault_rate=config["fault_rate"])
    for a, b in [(100, 100), (3, 7), (0, 0), (-7, -3)]:
        cell("SC-007", f"cancellation-{a}-{b}", op="sub", a=a, b=b)
    for perturb in ["neutral", "erase"]:
        for pairs in [1, 6, 20]:
            cell("SC-008", f"midrun-{perturb}-{pairs}", op="add", a=17, b=28,
                 intervention={"at": 10, "mode": perturb, "pairs": pairs})
    for perturb in ["neutral", "flip"]:
        cell("SC-009", f"occupancy-{perturb}", kind="basin", a=7, perturb=perturb, rounds=24)
    for model in ["product", "repeated"]:
        for a, b in [(3, 4), (-7, 6), (12, 13)]:
            cell("SC-010", f"{model}-{a}-{b}", op="mul", a=a, b=b, model=model)
    for a, b in [(12, 3), (13, 3), (-13, 3), (13, -3), (-13, -3), (2, 5), (0, 3)]:
        cell("SC-011", f"partition-{a}-{b}", op="div", a=a, b=b)
    for a, b in [(37, 48), (999, 1), (100, -1), (1, -100), (-37, -48)]:
        cell("SC-012", f"decimal-{a}-{b}", kind="radix", a=a, b=b)
    for locality in ["global", "local"]:
        for regions in [2, 8, 32]:
            cell("SC-013", f"{locality}-{regions}", op="sub", a=12, b=9,
                 locality=locality, regions=regions, max_steps=10000)
    for coordinated in [True, False]:
        for fault_rate in [0.0, 0.15, 0.5]:
            cell("SC-014", f"coordination-{coordinated}-noise-{fault_rate}", kind="radix",
                 a=37, b=48, coordination=coordinated, fault_rate=fault_rate)
    for a, b in [(7, 5), (37, 48), (137, 148), (500, 500)]:
        cell("SC-015", f"scale-{a}-{b}", op="add", a=a, b=b, runs=50)
    for scheduler in ["random", "ordered"]:
        cell("SC-016", f"scheduler-{scheduler}", op="sub", a=17, b=9, scheduler=scheduler)
    for perturb in ["neutral", "erase"]:
        cell("SC-017", f"covariance-{perturb}", kind="covariance", a=7, perturb=perturb)
    for budget in [10, 50, 200]:
        cell("SC-018", f"local-budget-{budget}", op="sub", a=12, b=9,
             locality="local", regions=32, max_steps=budget)
    for a, b in [(3, 4), (17, 28)]:
        cell("SC-019", f"fixed-initial-{a}-{b}", runs=1000, op="add", a=a, b=b,
             fixed_initial=True)
    return cells


def trial(task: tuple[dict, dict, int, int]) -> dict:
    cell, base, seed, replication = task
    fields = Config.__dataclass_fields__
    config = Config(**{**base, **{k: v for k, v in cell.items() if k in fields}})
    engine = Engine(seed, config)
    initial, final = {}, {}
    result, expected, error = None, None, None
    diagnostics = {}
    started = time.perf_counter()
    try:
        a = cell["a"]
        if cell["kind"] == "radix":
            state = encode_decimal(a, engine)
            state.extend(encode_decimal(cell["b"], engine))
            initial = view(state)
            state = resolve(state, engine, cell.get("coordination", True))
            final = view(state)
            result = {"value": int(decode_decimal(state)), "remainder": 0}
            expected = expected_binary("add", a, cell["b"])
        else:
            encoder = Engine(20260910, config) if cell.get("fixed_initial") else engine
            left = encode(a, encoder)
            initial = {"left": snapshot(left)}
            if cell["kind"] == "identity":
                left = engine.perturb(left, cell["perturb"])
                initial["perturbed"] = snapshot(left)
                value = Value(engine.normalize(left))
                expected = {"value": a, "remainder": 0}
            elif cell["kind"] == "arithmetic":
                right = encode(cell["b"], encoder)
                if encoder is not engine:
                    engine.serial = encoder.serial
                initial["right"] = snapshot(right)
                engine.intervention = cell.get("intervention")
                op = cell["op"]
                if op == "add":
                    value = Value(add(left, right, engine))
                elif op == "sub":
                    value = Value(subtract(left, right, engine))
                elif op == "mul":
                    value = Value(multiply(left, right, engine, cell.get("model", "product")))
                else:
                    value = divide(left, right, engine)
                expected = expected_binary(op, a, cell["b"])
                diagnostics["intervention_applied"] = engine._intervened
            elif cell["kind"] == "basin":
                state = engine.normalize(left)
                occupancy = [decode(state)]
                for _ in range(cell["rounds"]):
                    state = engine.normalize(engine.perturb(state, cell["perturb"], 3))
                    occupancy.append(decode(state))
                diagnostics["occupancy"] = occupancy
                diagnostics["escape_events"] = sum(x == a and y != a for x, y in zip(occupancy, occupancy[1:]))
                diagnostics["return_events"] = sum(x != a and y == a for x, y in zip(occupancy, occupancy[1:]))
                value, expected = Value(state), {"value": a, "remainder": 0}
            elif cell["kind"] == "covariance":
                pairs = engine.rng.randrange(30)
                state = engine.perturb(left, "neutral", pairs)
                if cell["perturb"] == "erase":
                    for _ in range(engine.rng.randrange(8)):
                        if state:
                            state.remove(engine.choose(state))
                initial["perturbed"] = snapshot(state)
                positive = sum(e.positive for e in state)
                negative = -sum(not e.positive for e in state)
                diagnostics.update(positive=positive, negative=negative, net=positive + negative)
                value, expected = Value(engine.normalize(state)), {"value": a, "remainder": 0}
            else:
                raise ValueError("Unknown trial kind")
            result = {"value": decode(value.population),
                      "remainder": decode(value.remainder) if value.remainder else 0}
            final = {"population": snapshot(value.population), "remainder": snapshot(value.remainder or [])}
        converged = True
    except (ResourceLimit, ZeroDivisionError) as exc:
        converged, error = False, str(exc)
        diagnostics["last_active_state"] = json.loads(json.dumps(engine.context, default=asdict))
        # Even censored trials retain a conventional comparator, independently.
        expected = expected_binary(cell.get("op", "add"), cell["a"], cell.get("b", 0))
    if isinstance(final, dict):
        final_signature = {key: sorted((e["positive"], e["source"], e["target"], e["ready"])
                                      for e in edges) for key, edges in final.items()}
    else:
        final_signature = final
    return {"experiment": cell["experiment"], "cell": cell["label"], "replication": replication,
            "timestamp": timestamp(), "seed": seed, "configuration": asdict(config),
            "initial": initial, "final": final, "result": result, "expected": expected,
            "final_state_status": "normal_form" if converged else "incomplete_see_diagnostics",
            "converged": converged, "correct": converged and result == expected,
            "iterations": engine.steps, "seconds": time.perf_counter() - started,
            "trajectory": engine.trajectory, "final_structure": digest(final_signature),
            "events": dict(engine.counts), "diagnostics": diagnostics, "error": error}


def run(config: dict, output: Path, workers: int = 1, only: set[str] | None = None):
    if workers < 1 or config["replications"] < 1 or config["runs_per_cell"] < 1:
        raise ValueError("Worker, replication, and run counts must be positive")
    declared = config["cells"] if "cells" in config else scenarios(config)
    cells = [c for c in declared if only is None or c["experiment"] in only]
    if not cells:
        raise ValueError("No experiments selected")
    for cell in cells:
        if cell["runs"] < 1:
            raise ValueError("Every cell requires at least one trial")
        if cell.get("op") == "div" and cell.get("b") == 0:
            raise ValueError("Division experiments require a nonzero input divisor")
        Config(**{**config["engine"], **{k: v for k, v in cell.items() if k in Config.__dataclass_fields__}})
    output.mkdir(parents=True, exist_ok=False)
    pre = manifest({**config, "cells": cells, "workers": workers})
    write_json(output / "manifest.json", pre)
    archive_sources(output)
    tasks = []
    ordinal = 0
    for replication in range(config["replications"]):
        for cell in cells:
            for _ in range(cell["runs"]):
                tasks.append((cell, config["engine"], config["base_seed"] + ordinal, replication))
                ordinal += 1
    groups = defaultdict(list)
    pool = ProcessPoolExecutor(max_workers=workers) if workers > 1 else None
    rows = pool.map(trial, tasks, chunksize=32) if pool else map(trial, tasks)
    try:
        with gzip.open(output / "trials.jsonl.gz", "wt") as log:
            for index, row in enumerate(rows, 1):
                row["source_sha256"] = pre["source_sha256"]
                log.write(json.dumps(row, separators=(",", ":")) + "\n")
                key = f'{row["experiment"]}:{row["cell"]}:rep-{row["replication"]}'
                # Keep statistical fields only; full populations remain in the log.
                groups[key].append({k: v for k, v in row.items() if k not in {"initial", "final"}})
                if index % 2000 == 0:
                    print(f"Completed {index}/{len(tasks)} trials", flush=True)
    finally:
        if pool:
            pool.shutdown(wait=True, cancel_futures=True)
    summaries = {key: summarize(batch) for key, batch in groups.items()}
    write_json(output / "summary.json", summaries)
    print(f"Recorded {len(tasks)} trials in {output}", flush=True)
    return summaries


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "configs/programme.json")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--only", nargs="*")
    args = parser.parse_args()
    run(json.loads(args.config.read_text()), args.output, args.workers, set(args.only) if args.only else None)


if __name__ == "__main__":
    main()
