"""Boundary preparation, independent measurement, logging, and replay for SC-023+."""

import argparse
from collections import Counter, defaultdict
from dataclasses import asdict
import gzip
from hashlib import sha256
import json
from pathlib import Path
import statistics
import time

from .metrics import entropy, wilson
from .proposal_kernel import Bond, Constraints, proposals, transition
from .provenance import archive_sources, manifest, timestamp, write_json


def encode(inputs: list[int], neutral_pairs: int, regions: int,
           capacity: int | None = None) -> tuple[Bond, ...]:
    """Declared unary boundary; joins operands without computing their sum."""
    state = []
    for value in inputs:
        for _ in range(abs(value)):
            state.append(Bond(value >= 0, 0, len(state) % regions))
            if capacity is not None and len(state) > capacity:
                raise ValueError("Initial state exceeds capacity")
    for _ in range(neutral_pairs):
        state.extend((Bond(True, 0, 1), Bond(False, 1, 0)))
        if capacity is not None and len(state) > capacity:
            raise ValueError("Initial state exceeds capacity")
    return tuple(state)


def observe(state):
    positive = sum(b.positive for b in state)
    negative = len(state) - positive
    readable = all(b.ready for b in state) and not (positive and negative)
    return positive - negative, readable


def trial(cell: dict, seed: int, config: dict) -> dict:
    c = Constraints(**cell["constraints"])
    state = encode(cell["inputs"], config["neutral_pairs"], config["regions"], config["capacity"])
    initial = [asdict(b) for b in state]
    # This expected value is an observer only; it is never passed to transition.
    expected = sum(cell["inputs"])
    tape_hash, path_hash = sha256(), sha256()
    counts, occupancy = Counter(), Counter()
    first_readable = first_correct = None
    escapes = captures = invariant_violations = correct_steps = readable_steps = 0
    was_correct = False
    started = time.perf_counter()
    for step, p in enumerate(proposals(seed, config["horizon"], config["regions"]), 1):
        tape_hash.update(json.dumps(asdict(p), sort_keys=True).encode())
        state, status = transition(state, p, c, config["capacity"])
        counts[status] += 1
        counts[p.kind + ":" + status] += 1
        if status == "accepted":
            # Only actual state-changing events; excludes proposal RNG and noops.
            path_hash.update(repr((p.kind, state)).encode())
        charge, readable = observe(state)
        correct = readable and charge == expected
        invariant_violations += charge != expected
        readable_steps += readable
        correct_steps += correct
        occupancy[str(charge)] += 1
        if readable and first_readable is None:
            first_readable = step
        if correct and first_correct is None:
            first_correct = step
        escapes += was_correct and not correct
        captures += correct and not was_correct
        was_correct = correct
    return {"experiment": cell["experiment"], "cell": cell["label"], "seed": seed,
            "timestamp": timestamp(), "configuration": config, "constraints": asdict(c),
            "inputs": cell["inputs"], "initial": initial, "final": [asdict(b) for b in state],
            "result": charge if readable else None, "expected": expected,
            "terminal_charge": charge, "readable": readable, "correct": correct,
            "converged": None, "stopping_rule": "fixed horizon, not convergence",
            "iterations": step, "seconds": time.perf_counter() - started,
            "first_readable": first_readable, "first_correct": first_correct,
            "captures": captures, "escapes": escapes,
            "identity_violating_steps": invariant_violations,
            "readable_steps": readable_steps, "correct_steps": correct_steps,
            "charge_occupancy": dict(occupancy), "events": dict(counts),
            "proposal_tape": tape_hash.hexdigest(), "trajectory": path_hash.hexdigest()}


def summarize(rows):
    n = len(rows)
    correct = sum(r["correct"] for r in rows)
    captured = [r["first_correct"] for r in rows if r["first_correct"] is not None]
    return {"runs": n, "correct": correct, "accuracy": correct / n,
            "wilson95": wilson(correct, n),
            "terminal_readability": statistics.mean(r["readable"] for r in rows),
            "identity_preserved_runs": sum(not r["identity_violating_steps"] for r in rows),
            "correct_occupancy": statistics.mean(r["correct_steps"] / r["iterations"] for r in rows),
            "ever_captured": len(captured), "mean_first_capture_conditional": statistics.mean(captured) if captured else None,
            "mean_escapes": statistics.mean(r["escapes"] for r in rows),
            "capacity_rejections": sum(r["events"].get("capacity", 0) for r in rows),
            "unique_accepted_trajectories": len({r["trajectory"] for r in rows}),
            "outcomes": dict(Counter(str(r["result"]) for r in rows)),
            "outcome_entropy_bits": entropy(str(r["result"]) for r in rows)}


def run(config: dict, output: Path):
    if type(config["base_seed"]) is not int:
        raise ValueError("Integer base_seed required")
    for key in ("runs", "horizon", "capacity", "regions"):
        if type(config[key]) is not int or config[key] < (2 if key == "regions" else 1):
            raise ValueError("Invalid " + key)
    if type(config["neutral_pairs"]) is not int or config["neutral_pairs"] < 0:
        raise ValueError("Invalid neutral_pairs")
    labels = [cell["label"] for cell in config["cells"]]
    if not labels or len(set(labels)) != len(labels):
        raise ValueError("Cells need unique labels")
    for cell in config["cells"]:
        Constraints(**cell["constraints"])
        if not cell["inputs"] or any(type(v) is not int for v in cell["inputs"]):
            raise ValueError("Integer inputs required")
        encode(cell["inputs"], config["neutral_pairs"], config["regions"], config["capacity"])
    output.mkdir(parents=True, exist_ok=False)
    metadata = manifest(config)
    metadata["seed_policy"] = "base_seed + replication index, SAME tape across all cells; paired, not independent cells"
    write_json(output / "manifest.json", metadata)
    archive_sources(output)
    groups = defaultdict(list)
    with gzip.open(output / "trials.jsonl.gz", "wt") as stream:
        for rep in range(config["runs"]):
            for cell in config["cells"]:
                row = trial(cell, config["base_seed"] + rep, config)
                stream.write(json.dumps(row, sort_keys=True) + "\n")
                groups[cell["label"]].append(row)
    result = {name: summarize(rows) for name, rows in groups.items()}
    write_json(output / "summary.json", result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--replay", type=Path, help="Replay every row in a lab run with current source")
    args = parser.parse_args()
    if args.replay:
        metadata = json.loads((args.replay / "manifest.json").read_text())
        config = metadata["config"]
        cells = {c["label"]: c for c in config["cells"]}
        checked = 0
        with gzip.open(args.replay / "trials.jsonl.gz", "rt") as stream:
            for line in stream:
                old = json.loads(line)
                new = trial(cells[old["cell"]], old["seed"], config)
                for key in old.keys() - {"timestamp", "seconds"}:
                    if old[key] != new[key]:
                        raise ValueError(f"Replay mismatch: {old['cell']} seed {old['seed']} {key}")
                checked += 1
        print(f"Replayed {checked} rows exactly (excluding time fields).")
    else:
        if args.config is None or args.output is None:
            parser.error("--config and --output required without --replay")
        print(json.dumps(run(json.loads(args.config.read_text()), args.output), indent=2))


if __name__ == "__main__":
    main()
