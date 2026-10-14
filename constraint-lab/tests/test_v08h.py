"""Pre-freeze neutral/synthetic fixtures; target verification opens only after H0."""

from __future__ import annotations

import json
import subprocess
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import pytest

from rs_constraint_lab.durable import sha256_file
from rs_constraint_lab.explore08 import FrozenPlanError, plan_hash, source_masks
from rs_constraint_lab.gen008h_exec import (
    PALETTE, PLAN_RELPATH, HistoryRunError, prepare_h0_plan,
    require_h0_execution, validate_result,
)
from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.history import (
    HistoryError, HistoryState, RecentReversal, analyse_kernel, analyse_temporal,
    analyse_witness, entropy_information, js, mutual_information, witness_specification,
)

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "constraint-lab/reports/tables"
PUBLISHED = (ROOT / "constraint-lab/reports/generation-008h-round-h0-tables.json").exists()
POST_FREEZE = pytest.mark.skipif(not PUBLISHED, reason="actual non-neutral H0 verification stays unopened before frozen publication")


def test_history_update_and_reversal_across_hidden_events():
    model = RecentReversal(Fraction(2), pair_slots=3, triad_slots=1)
    start = HistoryState(0, None)
    changed = model.advance(start, 1)
    assert changed == HistoryState(2, 1)
    hidden = model.advance(changed, 3)
    assert hidden == HistoryState(10, 1)
    reversed_pair = model.advance(hidden, 1)
    assert reversed_pair == HistoryState(8, 1)
    assert reversed_pair.material & 7 == start.material & 7
    assert model.weights(None) == (1, 1, 1, 1)
    assert model.full_probabilities(1) == (Fraction(1, 5), Fraction(2, 5), Fraction(1, 5), Fraction(1, 5))
    assert model.pair_probabilities(1) == (Fraction(1, 4), Fraction(1, 2), Fraction(1, 4))


def test_synthetic_label_covariance():
    model = RecentReversal(Fraction(2), pair_slots=3, triad_slots=1)
    permutation = (2, 0, 1)
    for h in range(3):
        for event in range(3):
            assert model.pair_probabilities(h)[event] == model.pair_probabilities(permutation[h])[permutation[event]]


def test_indices_are_bijective_neutral_only():
    model = RecentReversal(Fraction(1))
    for index in range(7168):
        assert model.full_index(model.state_from_index(index)) == index
    for index in range(384):
        mask, history = model.epoch_state(index)
        assert model.epoch_index(mask, history) == index
        state = HistoryState(mask, history)
        for event in range(6):
            target = model.advance(state, event)
            assert model.epoch_index(target.material, target.recent_pair) in model.epoch_row(mask, history)


@pytest.mark.parametrize("multiplier,pairs,hidden", [(0, 3, 1), (-1, 3, 1), (1, 0, 1), (1, 3, -1)])
def test_invalid_controller_rejected(multiplier, pairs, hidden):
    with pytest.raises(HistoryError):
        RecentReversal(Fraction(multiplier), pairs, hidden)


def test_invalid_state_history_and_event_rejected():
    model = RecentReversal(Fraction(1))
    for state in (HistoryState(-1, None), HistoryState(1024, None), HistoryState(0, 6)):
        with pytest.raises(HistoryError):
            model.full_row(state)
    with pytest.raises(HistoryError):
        model.advance(HistoryState(0, None), 10)
    with pytest.raises(HistoryError):
        model.epoch_index(0, None)
    with pytest.raises(HistoryError):
        model.direct_next_pair_slots(64, None)


def test_neutral_witness_and_historical_path_representative():
    spec = witness_specification()
    assert spec["endpoint_state"] == 41
    assert source_masks()["path"] == spec["canonical_path_class"] == 13
    assert pair_classes().class_of[41] == 13
    result = analyse_witness(Fraction(1))
    assert result["path_probability_A"] == result["path_probability_B"] == Fraction(1, 100)
    assert result["endpoint_history_A"] == 3 and result["endpoint_history_B"] == 5
    assert result["endpoint_material_bytes_A"] == result["endpoint_material_bytes_B"]
    assert Decimal(result["pair_row_JS"]) == Decimal(result["graph_class_JS"]) == 0
    assert result["equal_event_multiset"] and result["same_program"]
    validate_result("witness", result)


def test_neutral_full_to_pair_quotient_all_raw_hidden_masks():
    model = RecentReversal(Fraction(1))
    for mask in (0, 41, 63):
        for history in (None, 0, 5):
            rows = model.direct_next_pair_slots(mask, history)
            assert len(rows) == 16
            assert all(tuple(row) == (Fraction(1, 6),) * 6 for row in rows)


def test_synthetic_non_neutral_kernel_and_temporal_identities():
    model = RecentReversal(Fraction(2), pair_slots=3, triad_slots=1)
    kernel = analyse_kernel(model, (0, 7))
    assert kernel["state_count"] == 24
    assert kernel["stationary_residual"] == kernel["history_pair_independence_gap"] == 0
    assert kernel["strong_lumpability"] is False
    assert kernel["stationary_one_step_gap_vs_H0"] == 0
    temporal = analyse_temporal(model)
    assert temporal["repeat_probability"] == temporal["two_step_backtrack_probability"] == Fraction(1, 2)
    assert temporal["nontrivial_eigenvalue"] == Fraction(1, 4)
    assert temporal["projected_markov_order"] == 2
    assert temporal["order2_sufficiency_gap"] == 0
    assert Decimal(temporal["consecutive_event_MI"]) > 0
    assert temporal["consistent_triples_checked"] == 8 * 3 * 3
    assert all(cell["TV_to_uniform"] == cell["TV_formula"] for cell in temporal["initial_history_decay"])
    validate_result("kernel", kernel)
    validate_result("temporal", temporal)


def test_neutral_kernel_and_temporal_collapse():
    model = RecentReversal(Fraction(1), pair_slots=3, triad_slots=1)
    result = analyse_temporal(model)
    assert result["projected_markov_order"] == 1
    assert result["order1_witness_gap"] == result["nontrivial_eigenvalue"] == 0
    assert result["repeat_probability"] == result["H0_backtrack_probability"] == Fraction(1, 3)
    assert Decimal(result["consecutive_event_MI"]) == 0
    assert all(Decimal(cell["initial_history_MI"]) == 0 for cell in result["initial_history_decay"] if cell["checkpoint"] > 0)
    assert analyse_kernel(model)["strong_lumpability"]


def test_information_helpers_rational_synthetic():
    row = [Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)]
    assert js(row, row) == 0
    joint = [[v / 3 for v in row], [row[1] / 3, row[0] / 3, row[2] / 3], [row[1] / 3, row[2] / 3, row[0] / 3]]
    assert abs(mutual_information(joint) - entropy_information(Fraction(1, 2), Fraction(1, 4), 3)) <= Decimal("1e-13")
    with pytest.raises(HistoryError):
        js([Fraction(1)], [Fraction(2)])
    with pytest.raises(HistoryError):
        mutual_information([[Fraction(-1), Fraction(2)]])


def test_plan_construction_never_executes_scientific_targets(monkeypatch):
    import rs_constraint_lab.gen008h_exec as runner

    def forbidden(*args, **kwargs):
        raise AssertionError("actual H0 scientific exposure during planning")

    for name in ("analyse_kernel", "analyse_temporal", "analyse_witness", "RecentReversal"):
        monkeypatch.setattr(runner, name, forbidden)
    plan = prepare_h0_plan()
    assert plan_hash(plan) == plan["plan_hash"]
    assert plan["work_counts"]["atomic_items"] == 11
    assert plan["work_counts"]["pair_epoch_transition_entries"] == 6912
    assert plan["pre_freeze_exposure"]["actual_non_neutral_H0_rows_kernels_cells"] == 0
    assert len(plan["items"]) == 11
    assert [item["m"] for item in plan["targets"]] == ["1/4", "1", "4"]


def test_execution_refuses_missing_freeze_before_any_scientific_call(monkeypatch):
    import rs_constraint_lab.gen008h_exec as runner

    monkeypatch.setattr(runner, "analyse_witness", lambda *args: pytest.fail("unfrozen target execution"))
    with pytest.raises(FrozenPlanError):
        require_h0_execution(ROOT, None)


def test_execution_refuses_unpushed_plan(monkeypatch):
    import rs_constraint_lab.gen008h_exec as runner

    plan = prepare_h0_plan()
    monkeypatch.setattr(runner, "require_frozen_plan", lambda *args, **kwargs: plan)
    monkeypatch.setattr(runner, "remote_contains", lambda *args: False)
    with pytest.raises(FrozenPlanError, match="pushed"):
        require_h0_execution(ROOT, "f" * 40)


def test_validation_rejects_corrupted_exact_result():
    result = analyse_temporal(RecentReversal(Fraction(2), pair_slots=3, triad_slots=1))
    result["order2_sufficiency_gap"] = Fraction(1, 100)
    with pytest.raises(HistoryRunError):
        validate_result("temporal", result)


def test_prompt_storage_and_review_metadata():
    prompt = ROOT / "constraint-lab/provenance/prompts/008H-v0.8h-agent-input.md"
    assert len(prompt.read_bytes()) == 46117
    assert sha256_file(prompt) == "b55eb3a4d0050a32a1560fe5faaf5303683cff0d4540ab9abd7dd6a6451725b3"
    assert "b55eb3a4d0050a32a1560fe5faaf5303683cff0d4540ab9abd7dd6a6451725b3" not in prompt.read_text()
    ledger = [json.loads(line) for line in (ROOT / "constraint-lab/provenance/ledger.jsonl").read_text().splitlines()]
    metadata = next(row for row in ledger if row.get("prompt_id") == "008G" and row["record_type"] == "prompt_representation")
    assert metadata["authored_prompt_bytes"] == 45624
    assert metadata["agent_input_prompt_sha256"] != metadata["authored_prompt_sha256"]


@POST_FREEZE
@pytest.mark.parametrize("label,m", PALETTE)
def test_published_witness_target(label, m):
    multiplier = Fraction(m)
    result = next(row for row in json.loads((TABLES / "generation-008h-witness.json").read_text()) if Fraction(row["m"]) == multiplier)
    validate_result("witness", result)
    assert Fraction(result["path_probability_A"]) == 1 / (10 * (multiplier + 9))
    assert result["endpoint_state"] == 41 and result["endpoint_triad_mask"] == 0
    assert result["endpoint_material_bytes_A"] == result["endpoint_material_bytes_B"]
    assert Fraction(result["full_row_max_difference"]) == abs(multiplier - 1) / (multiplier + 9)
    assert Fraction(result["pair_row_max_difference"]) == abs(multiplier - 1) / (multiplier + 5)
    assert Decimal(result["edge_count_JS"]) == 0
    assert (Decimal(result["graph_class_JS"]) == 0) == (multiplier == 1)
    denom = multiplier + 5
    expected_M = {"two_edge_path": 2 / denom, "two_edge_matching": multiplier / denom, "triangle_pendant": 2 / denom, "four_cycle": 1 / denom}
    expected_E = {**expected_M, "two_edge_path": (multiplier + 1) / denom, "two_edge_matching": 1 / denom}
    assert {k: Fraction(v) for k, v in result["shape_distributions"][0].items()} == expected_M
    assert {k: Fraction(v) for k, v in result["shape_distributions"][1].items()} == expected_E


@POST_FREEZE
def test_published_kernels_and_stationary_averaging_exact():
    kernels = json.loads((TABLES / "generation-008h-kernels.json").read_text())
    for record in kernels:
        rows = [{int(target): Fraction(value) for target, value in row} for row in record["transitions"]]
        assert len(rows) == 384
        columns = [Fraction(0)] * 384
        for source, row in enumerate(rows):
            assert len(row) == 6 and sum(row.values()) == 1
            for target, value in row.items():
                columns[target] += value
                assert (source // 6).bit_count() % 2 != (target // 6).bit_count() % 2
        assert columns == [Fraction(1)] * 384
        for mask in range(64):
            projected = {}
            for history in range(6):
                for target, value in rows[mask * 6 + history].items():
                    projected[target // 6] = projected.get(target // 6, Fraction(0)) + value / 6
            assert projected == {mask ^ (1 << event): Fraction(1, 6) for event in range(6)}


@POST_FREEZE
def test_published_temporal_and_markov_order():
    histories = json.loads((TABLES / "generation-008h-history-chain.json").read_text())
    projected = json.loads((TABLES / "generation-008h-projected-process.json").read_text())
    for history, process in zip(histories, projected):
        m = Fraction(history["m"])
        assert Fraction(history["nontrivial_eigenvalue"]) == (m - 1) / (m + 5)
        assert Fraction(history["repeat_probability"]) == Fraction(process["two_step_backtrack_probability"]) == m / (m + 5)
        assert Fraction(process["order2_sufficiency_gap"]) == 0
        assert process["projected_markov_order"] == (1 if m == 1 else 2)
        assert process["consistent_triples_checked"] == 2304
        q = [[Fraction(value) for value in row] for row in history["transition_matrix"]]
        joint = [[value / 6 for value in row] for row in q]
        assert abs(mutual_information(joint) - Decimal(history["consecutive_event_MI"])) <= Decimal("1e-13")


@POST_FREEZE
def test_published_direct_quotient_on_all_raw_triads():
    for _label, m in PALETTE:
        model = RecentReversal(Fraction(m))
        for history in (None, 3, 5):
            direct = model.direct_next_pair_slots(41, history)
            assert len(direct) == 16
            assert all(tuple(row) == model.pair_probabilities(history) for row in direct)


@POST_FREEZE
def test_frozen_plan_published_hashes_and_zero_unopened_exposure():
    summary = json.loads((ROOT / "constraint-lab/reports/generation-008h-round-h0-tables.json").read_text())
    plan = require_h0_execution(ROOT, summary["frozen_analysis_plan_commit"])
    assert plan["plan_hash"] == summary["plan_hash"]
    assert plan["pre_freeze_exposure"]["actual_non_neutral_H0_rows_kernels_cells"] == 0
    assert plan["work_counts"]["pair_epoch_kernels"] == 3
    assert plan["work_counts"]["direct_raw_triad_rows"] == 1008
    for path, digest in summary["detail_sha256"].items():
        assert sha256_file(ROOT / path) == digest


@POST_FREEZE
@pytest.mark.parametrize("label,m", PALETTE)
def test_full_material_projection_uses_explicit_destination_blocks(label, m):
    model = RecentReversal(Fraction(m))
    start = HistoryState(1, None)
    endpoints = []
    probabilities = []
    for events in ((5, 3), (3, 5)):
        state, probability = start, Fraction(1)
        for event in events:
            target = model.advance(state, event)
            probability *= model.full_row(state)[target]
            state = target
        endpoints.append(state)
        probabilities.append(probability)
    assert probabilities[0] == probabilities[1] > 0
    assert endpoints[0].material == endpoints[1].material == 41
    blocks = []
    for state in endpoints:
        projected = {}
        for target, probability in model.full_row(state).items():
            projected[target.material] = projected.get(target.material, Fraction(0)) + probability
        blocks.append(projected)
    destination = 41 ^ (1 << 3)
    assert blocks[0][destination] == Fraction(m) / (Fraction(m) + 9)
    assert blocks[1][destination] == 1 / (Fraction(m) + 9)
    assert (blocks[0] == blocks[1]) == (Fraction(m) == 1)
    neutral = RecentReversal(Fraction(1))
    reference = {target.material: p for target, p in neutral.full_row(HistoryState(41, None)).items()}
    for history in range(6):
        assert {target.material: p for target, p in neutral.full_row(HistoryState(41, history)).items()} == reference


@POST_FREEZE
@pytest.mark.parametrize("label,m", PALETTE)
def test_shape_conditional_information_from_classified_distributions(label, m):
    result = analyse_witness(Fraction(m))
    left, right = result["graph_class_distributions"]
    conditional_information = Decimal(0)
    for count in (2, 4):
        classes = [key for key in left if key.bit_count() == count]
        left_mass = sum(left[key] for key in classes)
        right_mass = sum(right[key] for key in classes)
        assert left_mass == right_mass
        row_js = js([left[key] / left_mass for key in classes], [right[key] / right_mass for key in classes])
        conditional_information += Decimal(left_mass.numerator) / Decimal(left_mass.denominator) * row_js
    assert abs(conditional_information - Decimal(result["graph_class_JS"])) <= Decimal("1e-13")


def _git_history(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True).stdout


def test_8h_preserves_reviewed_artifacts_with_one_recorded_question_status_change():
    parent = "22e252e560cc711d337b6ae506b0fb76728247d6"
    old_paths = set(_git_history("ls-tree", "-r", "--name-only", parent).decode().splitlines())
    changed = set(_git_history("diff", "--name-only", parent, "--", "books", "constraint-lab/reports", "constraint-lab/exploration", "constraint-lab/provenance", "constraint-lab/coherence/snapshots").decode().splitlines())
    assert old_paths & changed <= {"constraint-lab/provenance/ledger.jsonl"}
    for name in ("formal/theorem-catalog.jsonl", "provenance/ledger.jsonl", "coherence/relations.jsonl"):
        path = "constraint-lab/" + name
        assert (ROOT / path).read_bytes().startswith(_git_history("show", f"{parent}:{path}"))
    path = "constraint-lab/coherence/findings.jsonl"
    old = _git_history("show", f"{parent}:{path}").splitlines()
    current = (ROOT / path).read_bytes().splitlines()
    for before, after in zip(old, current):
        if json.loads(before)["finding_id"] == "Q-H-POSITIVE":
            assert after == before.replace(b'"status":"unresolved"', b'"status":"qualified"')
        else:
            assert before == after
    findings = [json.loads(line) for line in current]
    resolution = next(row for row in findings if row["finding_id"] == "F8H-H-QUESTION-RESOLUTION")
    assert "unresolved to qualified" in resolution["statement"]
    assert len([row for row in findings if row["created_generation"] == "008H"]) == 19


def test_8h_snapshot_and_formal_links_match_canonical_ledgers(tmp_path):
    from rs_constraint_lab.coherence import load_ledger, snapshot_text
    from rs_constraint_lab.formal import load_catalog, validate_catalog

    directory = ROOT / "constraint-lab/coherence"
    for name in ("findings.jsonl", "relations.jsonl"):
        (tmp_path / name).write_bytes(_git_history("show", "ad5b656e26fe66610b583aedccdd34593e13791a:constraint-lab/coherence/" + name))
    assert (directory / "snapshots/through-generation-008h.md").read_text() == snapshot_text(tmp_path, title="Through Generation 008H")
    catalog = load_catalog()
    assert validate_catalog(catalog) == []
    assert len([row for row in catalog if row["status"] == "ALGEBRAIC_THEOREM" and row["source_generations"] == ["008H"]]) == 10
    findings, relations = load_ledger(directory)
    assert any(row["from_finding"] == "Q-H-POSITIVE" and row["relation_type"] == "partially_answered_by" for row in relations)
    historical_findings, _ = load_ledger(tmp_path)
    assert next(row for row in historical_findings if row["finding_id"] == "Q-H-MINIMAL-STATE")["status"] == "unresolved"
