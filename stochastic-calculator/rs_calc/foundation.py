"""SC-001. Run before any arithmetic mechanism is implemented."""

import argparse
import json
from pathlib import Path

from .engine import Config, Engine, ResourceLimit, digest, snapshot, structural
from .metrics import summarize
from .numbers import decode, encode
from .provenance import ROOT, archive_sources, manifest, timestamp, write_json


def run(config: dict, output: Path):
    output.mkdir(parents=True, exist_ok=False)
    pre = manifest(config)
    write_json(output / "manifest.json", pre)
    archive_sources(output)
    summaries = {}
    ordinal = 0
    with (output / "trials.jsonl").open("w") as log:
        for identity in config["identities"]:
            for perturbation in config["perturbations"]:
                batch = []
                for _ in range(config["runs"]):
                    seed = config["base_seed"] + ordinal
                    ordinal += 1
                    engine = Engine(seed, Config(**config["engine"]))
                    clean = encode(identity, engine)
                    state = engine.perturb(clean, perturbation, config["neutral_pairs"])
                    initial = snapshot(state)
                    converged, result, error = True, None, None
                    try:
                        final = engine.normalize(state)
                        result = decode(final)
                    except ResourceLimit as exc:
                        converged, final, error = False, [], str(exc)
                    row = {"experiment": "SC-001", "timestamp": timestamp(), "seed": seed,
                           "source_sha256": pre["source_sha256"], "identity": identity,
                           "perturbation": perturbation, "initial": initial,
                           "final": snapshot(final), "result": result, "expected": identity,
                           "converged": converged, "correct": converged and result == identity,
                           "iterations": engine.steps, "trajectory": engine.trajectory,
                           "final_structure": digest(structural(final)),
                           "events": dict(engine.counts), "error": error}
                    log.write(json.dumps(row, separators=(",", ":")) + "\n")
                    batch.append(row)
                summaries[f"{identity}:{perturbation}"] = summarize(batch)
    write_json(output / "summary.json", summaries)
    return summaries


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "configs/foundation.json")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(json.loads(args.config.read_text()), args.output)
    for key, summary in result.items():
        print(key, summary["correct"], "/", summary["runs"],
              "unique final structures:", summary["unique_final_structures"])


if __name__ == "__main__":
    main()
