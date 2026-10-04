"""Passive multi-observer, checkpoint and recurrence measurements for SC-026+."""

import argparse
from collections import Counter, defaultdict
from dataclasses import asdict
import gzip
from hashlib import sha256
import json
from pathlib import Path
import random
import shutil
import statistics
import time

from .constraint_lab import encode
from .metrics import wilson
from .proposal_kernel import Constraints, proposals, transition
from .recurrent_kernel import RecurrentRule, transition as recurrent_transition
from .provenance import ROOT, archive_sources, manifest, timestamp, write_json


def observations(state):
    """Two boundary decoders; mixed-sign subtraction is diagnostic only."""
    positive = sum(b.positive for b in state)
    negative = len(state) - positive
    pure = not (positive and negative)
    value = (len(state) if positive else -len(state)) if pure else None
    return {"pure": value, "ready": value if all(b.ready for b in state) else None}, positive - negative, min(positive, negative)


class ReadoutWindow:
    def __init__(self, previous, start=0):
        self.previous = previous
        self.initial_correct = previous
        self.start = start
        self.readable = self.correct = self.captures = self.escapes = 0
        self.entered = self.left = None
        self.residences = []
        self.recoveries = []

    def update(self, value, expected, step):
        correct = value == expected
        self.readable += value is not None
        self.correct += correct
        if correct and not self.previous:
            self.captures += 1
            self.entered = step
            if self.left is not None:
                self.recoveries.append(step - self.left)
                self.left = None
        if self.previous and not correct:
            self.escapes += 1
            self.left = step
            if self.entered is not None:
                self.residences.append(step - self.entered)
                self.entered = None
        self.previous = correct

    def snapshot(self, value, expected, step):
        return {"result": value, "correct": value == expected,
                "readable_steps": self.readable, "correct_steps": self.correct,
                "captures": self.captures, "escapes": self.escapes,
                "complete_residences": list(self.residences),
                "complete_recoveries": list(self.recoveries),
                "window_initial_correct": self.initial_correct,
                "right_censored_residence": step - (self.entered if self.entered is not None else self.start) if self.previous else None,
                "right_censored_recovery": step - (self.left if self.left is not None else self.start) if not self.previous else None,
                "terminal_episode_left_censored": self.entered is None if self.previous else self.left is None}


def trial(cell, seed, config):
    state = encode(cell["inputs"], config["neutral_pairs"], config["regions"], cell["capacity"])
    initial = [asdict(b) for b in state]
    c = Constraints(**cell["constraints"])
    rule = RecurrentRule(cell["birth_admission"]) if "birth_admission" in cell else None
    if rule is not None and c != Constraints(conservation=1, no_growth=False, readiness=False):
        raise ValueError("Recurrent cells require conserving, bidirectional constraints")
    expected = sum(cell["inputs"])
    values, _, _ = observations(state)
    windows = {name: ReadoutWindow(value == expected) for name, value in values.items()}
    counts, window_counts, defects, populations = Counter(), Counter(), Counter(), Counter()
    tape, trajectory = sha256(), sha256()
    violations = 0
    rows = []
    start = time.perf_counter()
    for step, p in enumerate(proposals(seed, max(config["horizons"]), config["regions"]), 1):
        tape.update(repr(p).encode())
        if rule is None:
            state, status = transition(state, p, c, cell["capacity"])
        else:
            state, status = recurrent_transition(state, p, rule, cell["capacity"])
        counts[p.kind + ":" + status] += 1
        if status == "accepted":
            trajectory.update(repr((p.kind, state)).encode())
        values, charge, defect = observations(state)
        violations += charge != expected
        if step <= config["burn_in"]:
            windows = {name: ReadoutWindow(value == expected, step) for name, value in values.items()}
        else:
            window_counts[p.kind + ":" + status] += 1
            defects[str(defect)] += 1
            populations[str(len(state))] += 1
            for name, value in values.items():
                windows[name].update(value, expected, step)
        if step in config["horizons"]:
            rows.append({"experiment": config["experiment"], "cell": cell["label"],
                         "seed": seed, "timestamp": timestamp(), "seconds": time.perf_counter() - start,
                         "horizon": step, "burn_in": config["burn_in"], "window_steps": step - config["burn_in"],
                         "configuration": cell, "initial": initial, "final": [asdict(b) for b in state],
                         "expected": expected, "terminal_charge": charge, "identity_violating_steps": violations,
                         "observers": {name: w.snapshot(values[name], expected, step) for name,w in windows.items()},
                         "events": dict(counts), "window_events": dict(window_counts),
                         "defect_occupancy": dict(defects), "population_occupancy": dict(populations),
                         "proposal_tape": tape.hexdigest(), "trajectory": trajectory.hexdigest(),
                         "converged": None, "stopping_rule": "fixed checkpoints; observers do not control dynamics"})
    return rows


def mean_interval(values):
    """Percentile bootstrap over independent seed trajectories, not time steps."""
    rng = random.Random(260027)
    estimates = sorted(statistics.mean(rng.choices(values, k=len(values))) for _ in range(1000))
    return [estimates[24], estimates[974]]


def summarize(rows):
    observers = {}
    for name in ("pure", "ready"):
        data = [r["observers"][name] for r in rows]
        occupancy = [d["correct_steps"] / r["window_steps"] for d,r in zip(data,rows)]
        correct = sum(d["correct"] for d in data)
        observers[name] = {"terminal_correct": correct, "terminal_wilson95": wilson(correct, len(rows)),
                           "mean_correct_occupancy": statistics.mean(occupancy),
                           "occupancy_bootstrap95": mean_interval(occupancy),
                           "total_captures": sum(d["captures"] for d in data),
                           "total_escapes": sum(d["escapes"] for d in data),
                           "runs_with_escape_and_return": sum(bool(d["complete_recoveries"]) for d in data),
                           "complete_recovery_episodes": sum(len(d["complete_recoveries"]) for d in data)}
    return {"runs": len(rows), "identity_preserved_runs": sum(not r["identity_violating_steps"] for r in rows),
            "unique_trajectories": len({r["trajectory"] for r in rows}),
            "mean_population": statistics.mean(sum(int(k)*v for k,v in r["population_occupancy"].items())/r["window_steps"] for r in rows),
            "capacity_rejections": sum(sum(v for k,v in r["window_events"].items() if k.endswith(":capacity")) for r in rows),
            "accepted_pair_births": sum(r["window_events"].get("pair_birth:accepted", 0) for r in rows),
            "observers": observers}


def validate(config):
    if type(config["base_seed"]) is not int or type(config["runs"]) is not int or config["runs"] < 1:
        raise ValueError("Invalid seed or trial count")
    if type(config["regions"]) is not int or config["regions"] < 2:
        raise ValueError("Invalid region count")
    if type(config["neutral_pairs"]) is not int or config["neutral_pairs"] < 0:
        raise ValueError("Invalid neutral pairs")
    hs = config["horizons"]
    if not hs or any(type(h) is not int or h < 1 for h in hs) or hs != sorted(set(hs)):
        raise ValueError("Horizons must be distinct, positive and sorted")
    if type(config["burn_in"]) is not int or not 0 <= config["burn_in"] < min(hs):
        raise ValueError("Burn-in must precede all checkpoints")
    labels = [c["label"] for c in config["cells"]]
    if not labels or len(set(labels)) != len(labels):
        raise ValueError("Unique nonempty cells required")
    for cell in config["cells"]:
        c = Constraints(**cell["constraints"])
        if "birth_admission" in cell:
            RecurrentRule(cell["birth_admission"])
            if c != Constraints(conservation=1, no_growth=False, readiness=False):
                raise ValueError("Recurrent cells require full conservation with growth and readiness reversals allowed")
        if type(cell["capacity"]) is not int or cell["capacity"] < 1:
            raise ValueError("Invalid capacity")
        if not cell["inputs"] or any(type(v) is not int for v in cell["inputs"]):
            raise ValueError("Integer inputs required")
        encode(cell["inputs"], config["neutral_pairs"], config["regions"], cell["capacity"])


def run(config, output):
    validate(config)
    protocol = ROOT / "research" / "RELAXATION_LAB.md"
    protocol_bytes = protocol.read_bytes()
    output.mkdir(parents=True, exist_ok=False)
    metadata = manifest(config)
    metadata["seed_policy"] = "base_seed + replication index; paired tapes across cells and prefixes across horizons"
    metadata["protocol_sha256"] = sha256(protocol_bytes).hexdigest()
    write_json(output / "manifest.json", metadata)
    shutil.copyfile(protocol, output / "protocol.md")
    archive_sources(output)
    grouped = defaultdict(list)
    with gzip.open(output / "trials.jsonl.gz", "wt") as stream:
        for rep in range(config["runs"]):
            for cell in config["cells"]:
                for row in trial(cell, config["base_seed"] + rep, config):
                    stream.write(json.dumps(row, sort_keys=True) + "\n")
                    grouped[f"{cell['label']}:{row['horizon']}"].append(row)
    result = {key: summarize(rows) for key, rows in grouped.items()}
    write_json(output / "summary.json", result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--replay", type=Path)
    args = parser.parse_args()
    if args.replay:
        config = json.loads((args.replay / "manifest.json").read_text())["config"]
        cells = {c["label"]: c for c in config["cells"]}
        cached = {}
        seen = set()
        checked = 0
        with gzip.open(args.replay / "trials.jsonl.gz", "rt") as stream:
            for line in stream:
                old = json.loads(line)
                key = (old["cell"], old["seed"])
                checkpoint = (*key, old["horizon"])
                if checkpoint in seen:
                    raise ValueError("Duplicate replay checkpoint")
                seen.add(checkpoint)
                if key not in cached:
                    cached[key] = {r["horizon"]: r for r in trial(cells[key[0]], key[1], config)}
                new = cached[key].pop(old["horizon"])
                for field in old.keys() - {"timestamp", "seconds"}:
                    if old[field] != new[field]:
                        raise ValueError(f"Replay mismatch {key} {old['horizon']} {field}")
                if not cached[key]:
                    del cached[key]
                checked += 1
        expected = {(c["label"], seed, h) for c in config["cells"]
                    for seed in range(config["base_seed"], config["base_seed"]+config["runs"])
                    for h in config["horizons"]}
        if seen != expected or cached:
            raise ValueError("Incomplete replay dataset")
        print(f"Replayed {checked} checkpoint records exactly except time fields.")
    else:
        if not args.config or not args.output:
            parser.error("--config and --output required")
        result = run(json.loads(args.config.read_text()), args.output)
        for key, s in result.items():
            print(key, {name: d["terminal_correct"] for name,d in s["observers"].items()}, "of", s["runs"])


if __name__ == "__main__":
    main()
