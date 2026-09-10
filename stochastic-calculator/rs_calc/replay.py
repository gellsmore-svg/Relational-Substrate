"""Replay a logged trial and compare structural output and trajectory."""

import argparse
import gzip
import json
from pathlib import Path

from .experiments import trial
from .provenance import manifest


def replay(directory: Path, seed: int, allow_source_change=False):
    pre = json.loads((directory / "manifest.json").read_text())
    current = manifest({})
    # Additional analysis files do not invalidate a recorded mechanism snapshot.
    mismatch = [path for path, digest in pre["source_files"].items()
                if current["source_files"].get(path) != digest]
    if mismatch and not allow_source_change:
        raise ValueError("Recorded sources differ: " + ", ".join(mismatch)
                         + ". Restore source.tar.gz in an isolated directory or pass --allow-source-change.")
    with gzip.open(directory / "trials.jsonl.gz", "rt") as log:
        for line in log:
            row = json.loads(line)
            if row["seed"] != seed:
                continue
            cell = next(c for c in pre["config"]["cells"] if c["experiment"] == row["experiment"]
                        and c["label"] == row["cell"])
            reproduced = trial((cell, pre["config"]["engine"], seed, row["replication"]))
            fields = ["initial", "final", "result", "expected", "converged", "correct",
                      "iterations", "trajectory", "events", "diagnostics", "error"]
            differences = [key for key in fields if reproduced[key] != row[key]]
            return {"seed": seed, "matches": not differences, "differing_fields": differences,
                    "source_changes": mismatch, "trajectory": reproduced["trajectory"]}
    raise ValueError("Seed not found in this run")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--allow-source-change", action="store_true")
    args = parser.parse_args()
    result = replay(args.directory, args.seed, args.allow_source_change)
    print(json.dumps(result, indent=2))
    if not result["matches"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
