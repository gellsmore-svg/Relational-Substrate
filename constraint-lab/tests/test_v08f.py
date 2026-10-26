"""8F contracts. Pre-freeze numerical tests use historical or synthetic laws."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
from dataclasses import replace
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from rs_constraint_lab.coherence import load_ledger, snapshot_text, validate_ledger
from rs_constraint_lab.durable import atomic_write_json, sha256_file
from rs_constraint_lab.explore08 import source_masks
from rs_constraint_lab.explore08b import epoch_landing
from rs_constraint_lab.explore08c import _kernel
from rs_constraint_lab.explore08f import (
    BridgeError, LawSpec, all_laws, build_law_kernel, canonical_fingerprint,
    condition_triads, decomposition, drift_root, epoch_residual,
    full_transition_matrix, law_fingerprint, local_table, path_middle_action,
    prepare_f0_plan, raw_to_canonical, reference_probability_gap,
    source_initial, stationary_distribution,
)
from rs_constraint_lab.gen008f_exec import _completed_item, require_f0_execution
from rs_constraint_lab.state import edges, relation_slots

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "constraint-lab/reports/tables"


def test_plan_does_not_evaluate_scientific_kernels(monkeypatch):
    import rs_constraint_lab.explore08f as bridge

    def forbidden(*args, **kwargs):
        raise AssertionError("pre-freeze target kernel execution")

    monkeypatch.setattr(bridge, "build_law_kernel", forbidden)
    monkeypatch.setattr(bridge, "epoch_landing", forbidden)
    plan = prepare_f0_plan()
    assert plan["pre_freeze_exposure"]["actual_scientific_target_kernels"] == []
    assert plan["work_count"]["unique_full_kernels"] == 16
    assert plan["work_count"]["labelled_laws"] == 48
    assert plan["work_count"]["s4_laws"] == 48
    assert plan["work_count"]["source_checkpoint_comparison_cells"] == 756
    assert plan["work_count"]["labelled_source_checkpoint_distribution_cells"] == 1008
    assert plan["plan_hash"] == prepare_f0_plan()["plan_hash"]


@pytest.mark.parametrize("m", [Fraction(1, 3), Fraction(1), Fraction(3, 2), Fraction(7)])
def test_synthetic_drift_root_is_unique_and_balanced(m):
    result = drift_root(m)
    r = Decimal(result["root_decimal"])
    assert r > 0
    assert Decimal(result["residual_decimal"]) < Decimal("1e-70")
    assert Decimal(result["final_bracket"][0]) <= r <= Decimal(result["final_bracket"][1])
    if m == 1:
        assert abs(r - 1) < Decimal("1e-70")


@pytest.mark.parametrize("grade", ["strong_suppress", "strong_favour"])
def test_comparator_corners_and_orthogonal_residual(grade):
    plan = prepare_f0_plan()
    laws = {r.model: r for r in all_laws(plan["drift_roots"]) if r.incidence_motif == "BOTH" and r.direction == "form" and r.grade == grade}
    c = math.log(float(Fraction(laws["K3"].m)))
    endpoint = local_table(laws["ENDPOINT"])
    projection = local_table(laws["PROJECTION"])
    k3 = local_table(laws["K3"])
    drift = local_table(laws["DRIFT"])
    np.testing.assert_allclose(endpoint["action_log_multiplier"], [0, c/2, c/2, c], atol=1e-15)
    np.testing.assert_allclose(projection["action_log_multiplier"], [-c/4, c/4, c/4, 3*c/4], atol=1e-15)
    residual = np.array(k3["action_log_multiplier"]) - projection["action_log_multiplier"]
    np.testing.assert_allclose(residual, [c/4, -c/4, -c/4, c/4], atol=1e-15)
    assert abs(residual.mean()) < 1e-15
    assert abs(np.dot(residual, [-0.5, 0.5, -0.5, 0.5])) < 1e-15
    assert abs(np.dot(residual, [-0.5, -0.5, 0.5, 0.5])) < 1e-15
    for row in (endpoint, projection, drift):
        assert abs(row["local_delta12"]) < 1e-70
    assert abs(drift["balanced_action_probability"] - k3["balanced_action_probability"]) <= 1e-14
    assert abs(drift["balanced_edge_drift"] - k3["balanced_edge_drift"]) <= 1e-14
    expected = float(5 * (Fraction(laws["K3"].m)-1) / (48 * (Fraction(laws["K3"].m)+5)))
    assert abs(k3["balanced_edge_drift"] - expected) < 1e-15


def test_canonical_source_action_incidence_and_unquotiented_prior():
    assert source_masks() == {"star": 7, "triangle": 11, "path": 13}
    action = path_middle_action()
    degrees = [sum((13 >> i) & 1 for i, edge in enumerate(edges(4)) if v in edge) for v in range(4)]
    assert (13 >> action) & 1
    assert all(degrees[v] == 2 for v in edges(4)[action])
    slots = relation_slots(4, 3)
    for motif, count in (("BOTH", 2), ("ONE", 1), ("NEITHER", 0)):
        triads = condition_triads(action, motif)
        assert len(set(triads)) == 2
        assert sum(set(slots[action]) <= set(slots[t]) for t in triads) == count
    initial = source_initial("path")
    assert np.count_nonzero(initial) == 16
    assert np.all(initial[initial > 0] == 1/16)


def test_canonical_fingerprint_and_state_map_are_semantic():
    plan = prepare_f0_plan()
    laws = all_laws(plan["drift_roots"])
    equivalent = [x for x in laws if x.model == "K3" and x.direction == "form" and x.grade == "strong_favour"]
    assert len({law_fingerprint(x) for x in equivalent}) == 3
    assert len({canonical_fingerprint(x) for x in equivalent}) == 1
    for law in equivalent:
        mapped = raw_to_canonical(law)
        assert sorted(mapped.tolist()) == list(range(1024))
        assert np.all((mapped & 63) == (np.arange(1024) & 63))
        np.testing.assert_array_equal(source_initial("star")[mapped], source_initial("star"))


@pytest.mark.parametrize("masks,component", [((0, 1), "I_model_edgecount"), ((3, 33), "I_model_shape_given_edgecount"), ((1, 2), "I_model_label_given_class")])
def test_information_chain_with_pure_projection_channels(masks, component):
    left, right = np.zeros(64), np.zeros(64)
    left[masks[0]], right[masks[1]] = 1, 1
    row = decomposition(left, right)
    assert abs(row["I_model_pairmask"] - math.log(2)) < 1e-15
    assert abs(row[component] - math.log(2)) < 1e-15
    assert abs(row["pairmask_chain_gap"]) < 1e-15
    assert abs(row["class_chain_gap"]) < 1e-15


def test_historical_epoch_matches_direct_sum_and_repeated_propagation():
    kernel = _kernel("R01")
    full = full_transition_matrix(kernel)
    epoch, _ = epoch_landing(kernel)
    triad = np.zeros_like(full)
    pair = np.zeros_like(full)
    for bit in range(10):
        states = np.arange(1024)
        targets = states ^ (1 << bit)
        (pair if bit < 6 else triad)[states, targets] = full[states, targets]
    initial = source_initial("path")
    visiting = initial.copy()
    direct = np.zeros(1024)
    for _ in range(80):
        direct += visiting @ pair
        visiting = visiting @ triad
    np.testing.assert_allclose(initial @ epoch, direct, atol=1e-14)
    assert epoch_residual(full, epoch) < 1e-11
    for count in (2, 4, 8):
        repeated = initial.copy()
        for _ in range(count):
            repeated = repeated @ epoch
        np.testing.assert_allclose(repeated, initial @ np.linalg.matrix_power(epoch, count), atol=1e-13)


def test_synthetic_precision_and_stationary_communicating_structure():
    law = LawSpec("synthetic", "PROJECTION", "ONE", "form", "synthetic", "3/2", 5, (6, 9), (("unconditional", "1.23456789012345678901234567890123456789"), ("u1", "1.5"), ("u2", "1.5")))
    kernel = build_law_kernel(law)
    gap = reference_probability_gap(law, kernel)
    assert 0 < gap["reference_probability_gap"] < 1e-13
    cycle = np.roll(np.eye(4), 1, axis=1)
    result = stationary_distribution(cycle)
    assert result["period"] == 4
    assert result["communicating_classes"] == 1
    assert result["residual"] < 1e-11
    np.testing.assert_allclose(result["pi"], [0.25]*4)
    with pytest.raises(BridgeError, match="communicating"):
        stationary_distribution(np.eye(4))


def test_unfrozen_execution_is_refused_and_incomplete_cache_is_ignored(tmp_path):
    with pytest.raises(Exception, match="frozen plan commit"):
        require_f0_execution(ROOT, None)
    result, matrix = tmp_path / "result.json", tmp_path / "matrices.npz"
    matrix.write_bytes(b"synthetic")
    atomic_write_json(result, {"cache_key": "key", "plan_hash": "plan", "matrix_sha256": sha256_file(matrix)})
    assert _completed_item(result, matrix, "key", {"plan_hash": "plan"})
    assert not _completed_item(result, matrix, "key", {"plan_hash": "different-plan"})
    matrix.write_bytes(b"incomplete")
    assert not _completed_item(result, matrix, "key", {"plan_hash": "plan"})


def test_review_prompt_representation_and_historical_qualification():
    ledger = [json.loads(x) for x in (ROOT / "constraint-lab/provenance/ledger.jsonl").read_text().splitlines()]
    prompt = next(r for r in ledger if r.get("prompt_id") == "008F" and r["record_type"] == "agent_input_prompt")
    raw = (ROOT / prompt["agent_input_prompt_path"]).read_bytes()
    assert len(raw) == prompt["agent_input_prompt_bytes"]
    assert hashlib.sha256(raw).hexdigest() == prompt["agent_input_prompt_sha256"]
    assert prompt["relationship"] == "unknown"
    assert prompt["authored_prompt_sha256"] is None
    assert prompt["agent_input_prompt_sha256"].encode() not in raw
    authored = next(r for r in ledger if r.get("prompt_id") == "008E" and r["record_type"] == "prompt_representation")
    assert authored["authored_prompt_bytes"] == 44720
    assert authored["agent_input_prompt_bytes"] == 44734
    assert authored["authored_prompt_sha256"] != authored["agent_input_prompt_sha256"]
    findings, relations = load_ledger(ROOT / "constraint-lab/coherence")
    assert validate_ledger(findings, relations) == []
    by_id = {r["finding_id"]: r for r in findings}
    assert by_id["F8E-GENERAL-K-INTERACTION"]["status"] == "qualified"
    historical = subprocess.run(
        ["git", "-C", str(ROOT), "show", "19d243a83105d0082866b38190ec269d78294e94:constraint-lab/coherence/findings.jsonl"],
        check=True, capture_output=True, text=True,
    ).stdout
    original = next(json.loads(line) for line in historical.splitlines() if json.loads(line)["finding_id"] == "F8E-GENERAL-K-INTERACTION")
    assert by_id["F8E-GENERAL-K-INTERACTION"]["statement"] == original["statement"]
    assert "a rule reading r literals has gate interaction order exactly r" in by_id["F8E-GENERAL-K-INTERACTION"]["statement"]
    assert "F8F-GENERAL-K-SCOPE" in by_id
    assert "F8F-PREFREEZE-SCIENCE-GATE" in by_id
    assert any(r["from_finding"] == "F8F-GENERAL-K-SCOPE" and r["to_finding"] == "F8E-GENERAL-K-INTERACTION" and r["relation_type"] == "qualifies" for r in relations)


@pytest.mark.skipif(not (TABLES / "generation-008f-checkpoint-bridge.json").exists(), reason="F0 scientific output checks only after freeze and publication")
def test_published_cells_reproduce_independent_chain_rule_and_precision():
    checkpoint = json.loads((TABLES / "generation-008f-checkpoint-bridge.json").read_text())
    stationary = json.loads((TABLES / "generation-008f-stationary-bridge.json").read_text())
    assert len(checkpoint) == 756
    assert len(stationary) == 36
    distributions = json.loads((TABLES / "generation-008f-checkpoint-distributions.json").read_text())
    by_key = {(r["target_id"], r["model"], r["source"], r["checkpoint"]): r for r in distributions}
    stationary_dist = json.loads((TABLES / "generation-008f-stationary-distributions.json").read_text())
    stationary_by_key = {(r["target_id"], r["model"]): r for r in stationary_dist}
    for row in checkpoint + stationary:
        assert abs(row["pairmask_chain_gap"]) <= 1e-12
        assert abs(row["class_chain_gap"]) <= 1e-12
        if "checkpoint" in row:
            left = by_key[row["target_id"], "K3", row["source"], row["checkpoint"]]
            right = by_key[row["target_id"], row["comparator"], row["source"], row["checkpoint"]]
        else:
            left = stationary_by_key[row["target_id"], "K3"]
            right = stationary_by_key[row["target_id"], row["comparator"]]
        independent = decomposition(left["pair_mask"], right["pair_mask"])
        assert all(abs(row[field] - value) <= 1e-12 for field, value in independent.items())
    summary = json.loads((ROOT / "constraint-lab/reports/generation-008f-round-f0-tables.json").read_text())
    for name, digest in summary["detail_sha256"].items():
        assert sha256_file(TABLES / ("generation-008f-" + name.replace("_", "-") + ".json")) == digest
    numeric = json.loads((TABLES / "generation-008f-numeric-validation.json").read_text())
    assert len(numeric) == 48
    for row in numeric:
        assert row["epoch_period"] == 2
        assert row["communicating_classes"] == 1
        assert row["epoch_kernel_residual"] <= 1e-11
        assert row["reference_probability_gap"] <= 1e-13
        assert row["stationary_residual"] <= 1e-11
    polarity = json.loads((TABLES / "generation-008f-polarity-conjugacy.json").read_text())
    assert polarity["holds"]
    assert len(polarity["checks"]) == 2


@pytest.mark.skipif(not (ROOT / "constraint-lab/coherence/snapshots/through-generation-008f.md").exists(), reason="8F snapshot checked after scientific close-out")
def test_8f_snapshot_is_deterministic_and_observations_cite_committed_tables(tmp_path):
    directory = ROOT / "constraint-lab/coherence"
    # A historical snapshot is generated from its closing ledger, not later appends.
    closing = "ec319f24faa66ca9898363ccd7531334e82544c1"
    for name in ("findings.jsonl", "relations.jsonl"):
        content = subprocess.run(["git", "-C", str(ROOT), "show", f"{closing}:constraint-lab/coherence/{name}"], check=True, capture_output=True).stdout
        (tmp_path / name).write_bytes(content)
    text = snapshot_text(tmp_path, title="Through Generation 008F")
    assert (directory / "snapshots/through-generation-008f.md").read_text() == text
    findings, _ = load_ledger(directory)
    for row in findings:
        if row["created_generation"] == "008F" and row["epistemic_layer"] == "OBSERVATION":
            assert any("reports/tables/generation-008f-" in path for path in row["evidence_refs"])
            assert all((ROOT / path).exists() for path in row["evidence_refs"])
            for path in row["evidence_refs"]:
                subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", "HEAD:" + path], check=True, capture_output=True)
            assert "overall_score" not in row and "master_score" not in row
