"""Crash recovery: an interrupted generation must match an uninterrupted one."""

from __future__ import annotations

import json
import shutil

import pytest

from rs_constraint_lab.cli import main
from rs_constraint_lab.execution import (
    IncompatibleGeneration,
    merge_directory,
    resume_directory,
    run_spec,
    scientific_projection,
    verify_directory,
)


def _spec():
    return {
        "schema": "rs-constraint-lab.experiment/v1",
        "experiment_id": "miniature-resilience",
        "generation": 0,
        "semantics": "graph",
        "G": 0,
        "S": 0,
        "H": 0,
        "L": 0,
        "O": 2,
        "alphabet": "W4",
        "weights": ["prohibit", "strong_favour"],
        "cells": [{"N": 2, "K_max": 1, "A_max": 2, "cardinalities": [1, 2]}],
        "trajectory": {"horizon": 4, "seeds": [0]},
        "rise_release_horizon": 2,
        "composition": "structural-simple",
        "analysis": "heavy-every-canonical",
        "predicates": ["edge"],
    }


def _receipts(directory):
    found = {}
    plan = json.loads((directory / "plan.json").read_text(encoding="utf-8"))
    for shard in plan["shards"]:
        path = directory / "shards" / shard["shard_id"] / "receipt.json"
        if path.is_file():
            found[shard["shard_id"]] = path.read_text(encoding="utf-8")
    return found


def test_plan_prints_without_writing_and_interruption_matches(tmp_path, monkeypatch):
    monkeypatch.delenv("RS_LAB_FAULT", raising=False)
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(_spec()), encoding="utf-8")
    assert main(["plan", str(spec_path), "--shard-items", "2"]) == 0
    assert not (tmp_path / "plan.json").exists()

    interrupted = tmp_path / "interrupted"
    code = main([
        "run", str(spec_path),
        "--out", str(interrupted),
        "--workers", "2",
        "--shard-items", "2",
        "--max-shards", "2",
    ])
    assert code == 0
    progress = json.loads((interrupted / "progress.json").read_text(encoding="utf-8"))
    assert progress["status"] == "IN_PROGRESS"
    assert progress["completed"] == 2
    assert main(["status", str(interrupted)]) == 0
    kept = _receipts(interrupted)
    assert len(kept) == 2
    plan = json.loads((interrupted / "plan.json").read_text(encoding="utf-8"))
    pending = [shard["shard_id"] for shard in plan["shards"] if shard["shard_id"] not in kept]
    assert len(pending) >= 2
    progress["shards"][pending[0]]["status"] = "running"
    (interrupted / "progress.json").write_text(json.dumps(progress), encoding="utf-8")
    planted = interrupted / "shards" / pending[1]
    planted.mkdir(parents=True, exist_ok=True)
    (planted / "result.json.tmp").write_text("{truncated", encoding="utf-8")
    report = verify_directory(interrupted)
    assert report["ok"] is False
    assert any("temporary" in error for error in report["errors"])

    assert main(["resume", str(interrupted), "--workers", "2"]) == 0
    assert _receipts(interrupted).keys() >= kept.keys()
    for shard_id, text in kept.items():
        assert (interrupted / "shards" / shard_id / "receipt.json").read_text(encoding="utf-8") == text
    assert not (planted / "result.json.tmp").exists()
    assert verify_directory(interrupted)["ok"] is True

    clean = tmp_path / "clean"
    assert main([
        "run", str(spec_path),
        "--out", str(clean),
        "--workers", "1",
        "--shard-items", "2",
    ]) == 0
    left = scientific_projection(json.loads((interrupted / "summary.json").read_text(encoding="utf-8")))
    right = scientific_projection(json.loads((clean / "summary.json").read_text(encoding="utf-8")))
    assert left == right
    assert left["status"] == "COMPLETE"
    card = right["cells"][0]["cardinalities"]["2"]
    assert card["labelled_stacked"] > 0
    assert card["stacked_canonical"] > 0
    assert (
        card["canonical"] + card["stacked_canonical"] + card["removed_by_symmetry"]
        == card["labelled_combinations"]
    )
    examples = right["cells"][0]["cancellations"].get("genuine_global_examples") or []
    for row in examples:
        heads = [text.split(" => ")[0] for text in row]
        assert len(heads) == len(set(heads))

    again = _receipts(clean)
    assert main(["run", str(spec_path), "--out", str(clean), "--resume", "--workers", "2"]) == 0
    assert _receipts(clean) == again


def test_published_runtime_is_the_run_wall_clock(tmp_path):
    spec = _spec()
    out = tmp_path / "out"
    publish = tmp_path / "pub"
    summary = run_spec(spec, out, workers=1, shard_items=2, publish=publish)
    manifest = publish / "experiments" / "manifests" / f"{spec['experiment_id']}-summary.json"
    stored = json.loads(manifest.read_text(encoding="utf-8"))
    assert stored["runtime_seconds"] == summary["runtime_seconds"]
    assert stored["runtime_seconds"] > 0
    merged = merge_directory(out, publish=publish)
    republished = json.loads(manifest.read_text(encoding="utf-8"))
    assert merged["runtime_seconds"] == summary["runtime_seconds"]
    assert republished["runtime_seconds"] == summary["runtime_seconds"]


def test_fault_injection_quarantines_or_retries(tmp_path, monkeypatch):
    monkeypatch.setenv("RS_LAB_FAULT", "always:0")
    partial = run_spec(_spec(), tmp_path / "always", workers=2, shard_items=2)
    assert partial["status"] == "PARTIAL"
    progress = json.loads((tmp_path / "always" / "progress.json").read_text(encoding="utf-8"))
    assert progress["quarantined"] == 1
    assert progress["completed"] == progress["total_shards"] - 1
    plan = json.loads((tmp_path / "always" / "plan.json").read_text(encoding="utf-8"))
    failed = next(shard for shard in plan["shards"] if shard["ordinal"] == 0)
    failure = json.loads(
        (tmp_path / "always" / "shards" / failed["shard_id"] / "failure.json").read_text(encoding="utf-8")
    )
    assert failure["attempt"] == 3
    assert failure["exception_type"] == "RuntimeError"
    assert failure["shard_id"] == failed["shard_id"]
    assert main(["verify", str(tmp_path / "always")]) == 1

    monkeypatch.setenv("RS_LAB_FAULT", "once:1")
    recovered = run_spec(_spec(), tmp_path / "once", workers=2, shard_items=2)
    assert recovered["status"] == "COMPLETE"
    clean = run_spec(_spec(), tmp_path / "clean", workers=2, shard_items=2)
    assert scientific_projection(recovered) == scientific_projection(clean)


def test_incompatible_identity_is_refused_before_mutation(tmp_path):
    base = tmp_path / "base"
    spec = _spec()
    run_spec(spec, base, workers=1, shard_items=2, max_shards=0)

    def trial(name):
        path = tmp_path / name
        shutil.copytree(base, path)
        return path

    semantic = trial("semantic")
    plan = json.loads((semantic / "plan.json").read_text(encoding="utf-8"))
    plan["header"]["semantic_version"] = "9.9.9"
    (semantic / "plan.json").write_text(json.dumps(plan), encoding="utf-8")
    before = (semantic / "progress.json").read_bytes()
    with pytest.raises(IncompatibleGeneration, match="semantic_version"):
        resume_directory(semantic, workers=1)
    assert (semantic / "progress.json").read_bytes() == before
    assert main(["resume", str(semantic), "--workers", "1"]) == 3
    assert (semantic / "progress.json").read_bytes() == before

    changed = trial("spec")
    before = (changed / "progress.json").read_bytes()
    other = dict(spec)
    other["experiment_id"] = "different-spec"
    with pytest.raises(IncompatibleGeneration, match="spec_hash"):
        run_spec(other, changed, workers=1, shard_items=2)
    assert (changed / "progress.json").read_bytes() == before

    numpy_dir = trial("numpy")
    plan = json.loads((numpy_dir / "plan.json").read_text(encoding="utf-8"))
    plan["header"]["numpy"] = "9.9.9"
    (numpy_dir / "plan.json").write_text(json.dumps(plan), encoding="utf-8")
    before = (numpy_dir / "progress.json").read_bytes()
    with pytest.raises(IncompatibleGeneration, match="numpy"):
        resume_directory(numpy_dir, workers=1)
    assert (numpy_dir / "progress.json").read_bytes() == before
