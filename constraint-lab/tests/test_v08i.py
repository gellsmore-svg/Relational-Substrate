"""Neutral/synthetic pre-freeze fixtures; primary scientific checks only post-publication."""

from __future__ import annotations

import copy
import json
import subprocess
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

import pytest

from rs_constraint_lab.durable import read_json, sha256_file
from rs_constraint_lab.explore08 import FrozenPlanError, plan_hash
from rs_constraint_lab.gen008i_exec import (
    PLAN, decode, equivalence_atlas, execute, prepare_plan, require_execution, validate_result,
)
from rs_constraint_lab.history import HistoryError, HistoryState, RecentReversal, js
from rs_constraint_lab.history_roles import (
    FEATURES, RoleController, action_direction, aggregate_quotient, covariance_gap,
    role_descriptors, role_orbits, slot_relation, structural_record,
)
from rs_constraint_lab.role_atlas import analyse_controller, balance_gap, conditional_model_information
from rs_constraint_lab.state import edges

ROOT = Path(__file__).resolve().parents[2]
SUMMARY = ROOT / "constraint-lab/reports/generation-008i-round-i0-tables.json"
PUBLISHED = pytest.mark.skipif(not SUMMARY.exists(), reason="non-neutral I0 verification stays unopened until frozen publication")


def test_feature_palette_and_independent_boolean_classification():
    assert [sum(f.family == name for f in FEATURES) for name in "ABC"] == [3, 2, 6]
    pairs = edges(4)
    for h in range(6):
        assert [sum(slot_relation(4, e, h) == relation for e in range(6)) for relation in ("SAME", "ADJACENT", "DISJOINT")] == [1, 4, 1]
        for p in range(64):
            for e in range(6):
                expected_relation = "SAME" if e == h else "ADJACENT" if set(pairs[e]) & set(pairs[h]) else "DISJOINT"
                expected_direction = "DISSOLVE" if p & (1 << e) else "FORM"
                assert action_direction(p, e) == expected_direction
                for feature in FEATURES:
                    expected = (feature.relation is None or feature.relation == expected_relation) and (feature.direction is None or feature.direction == expected_direction)
                    assert feature.active(p, h, e) == expected


def test_structural_orbits_covariance_and_descriptor_collisions():
    record = structural_record()
    assert record["orbit_count"] == 28
    assert record["state_count"] == record["orbit_size_sum"] == 384
    assert record["boolean_covariance_comparisons"] == 11 * 24 * 384 * 6
    assert record["descriptor_vector_count"] == 24
    assert len(record["descriptor_collisions"]) == 4
    structure = role_orbits()
    assert sorted(state for group in structure.members for state in group) == list(range(384))
    for collision in record["descriptor_collisions"]:
        assert len(collision["orbit_ids"]) == 2
        assert collision["orbit_ids"][0] != collision["orbit_ids"][1]
    for row in record["orbits"]:
        p, h = row["canonical_pair_mask"], row["canonical_h"]
        assert (row["R"], row["A_h"], row["D_h"], row["C_h"]) == role_descriptors(p, h)


def test_history_update_sentinel_and_full_pair_consistency_synthetic_only():
    model = RoleController("ADJ_FORM", Fraction(2), 3)
    start = HistoryState(0, None)
    pair = model.updates.advance(start, 0)
    hidden = model.updates.advance(pair, 3)
    assert pair == HistoryState(1, 0) and hidden == HistoryState(9, 0)
    assert model.pair_probabilities(0, None) == (Fraction(1, 3),) * 3
    assert RoleController("FORM_ANY", Fraction(2), 3).full_probabilities(0, None) == (Fraction(2, 7),) * 3 + (Fraction(1, 7),)
    for feature in FEATURES:
        fixture = RoleController(feature.name, Fraction(2), 3)
        for p in range(8):
            for h in (None, 0, 1, 2):
                full = fixture.full_probabilities(p, h)
                assert fixture.pair_probabilities(p, h) == tuple(value / sum(full[:3]) for value in full[:3])
    neutral = RoleController("SAME_ANY", Fraction(1))
    historical = RecentReversal(Fraction(1))
    for h in (None, *range(6)):
        assert neutral.pair_probabilities(41, h) == historical.pair_probabilities(h)
    for bad in (("unknown", 1, 4), ("SAME_ANY", 0, 4), ("ADJ_ANY", 1, 5)):
        with pytest.raises(HistoryError):
            RoleController(*bad)


@pytest.fixture(scope="module")
def neutral_result():
    return analyse_controller(RoleController("SAME_ANY", Fraction(1)), independent_full=True)


@pytest.fixture(scope="module")
def synthetic_result():
    return analyse_controller(RoleController("ADJ_FORM", Fraction(2), 3), independent_full=True)


def test_neutral_production_all_feature_rows_and_exact_diagnostics(neutral_result):
    validate_result(neutral_result)
    assert neutral_result["stationary_joint"] == [Fraction(1, 384)] * 384
    assert neutral_result["material"]["pair_mask"] == [Fraction(1, 64)] * 64
    assert neutral_result["atlas"]["strong_lumpability"]
    assert neutral_result["atlas"]["projected_markov_order"] == 1
    assert neutral_result["temporal"]["repeat_probability"] == Fraction(1, 6)
    assert neutral_result["temporal"]["two_step_backtrack_probability"] == Fraction(1, 6)
    assert Decimal(neutral_result["atlas"]["neutral_JS_pairmask"]) == 0
    for feature in FEATURES:
        model = RoleController(feature.name, Fraction(1))
        assert covariance_gap(model) == 0
        assert model.kernel() == RoleController("SAME_ANY", Fraction(1)).kernel()


def test_synthetic_exact_balance_KU_Kpi_and_markov_order(synthetic_result):
    validate_result(synthetic_result)
    model = RoleController("ADJ_FORM", Fraction(2), 3)
    assert balance_gap(synthetic_result["stationary_joint"], model.kernel()) == 0
    assert synthetic_result["atlas"]["projected_markov_order"] == 2
    witness = synthetic_result["temporal"]["order1_witness"]
    assert witness["positive_past_mass_A"] > 0 and witness["positive_past_mass_B"] > 0
    assert witness["probability_A"] != witness["probability_B"]
    assert synthetic_result["temporal"]["order2_sufficiency_gap"] == 0
    assert synthetic_result["temporal"]["consistent_material_triples"] == 8 * 3 * 3
    assert synthetic_result["temporal"]["repeat_probability"] == synthetic_result["temporal"]["two_step_backtrack_probability"]


def test_information_chain_with_unequal_conditional_model_priors():
    left = [Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 8)]
    right = left[::-1]
    conditional = conditional_model_information(left, right, [0, 0, 1, 1])
    with localcontext() as context:
        context.prec = 160
        expected = js(left, right) - js([sum(left[:2]), sum(left[2:])], [sum(right[:2]), sum(right[2:])])
        assert abs(conditional - expected) <= Decimal("1e-25")
    assert conditional_model_information(left, left, [0, 0, 1, 1]) == 0


def test_equivalence_engine_on_neutral_palette_only(neutral_result):
    records = []
    for feature in FEATURES:
        row = copy.deepcopy(neutral_result)
        row["controller_id"] = feature.name + "-neutral"
        row["catalog"].update(feature=feature.name, m=Fraction(1))
        records.append(row)
    neutral = copy.deepcopy(neutral_result)
    neutral["controller_id"] = "neutral"
    result = equivalence_atlas(records, neutral)
    validate_result(result)
    assert all(row["equivalent"] for row in result["reciprocity_checks"])
    assert len(result["groups"]["full_kernel_fingerprint"]) == 1


def test_plan_does_not_execute_actual_scientific_cells(monkeypatch):
    import rs_constraint_lab.gen008i_exec as runner

    def forbidden(*args, **kwargs):
        pytest.fail("actual I0 execution during planning")

    monkeypatch.setattr(runner, "RoleController", forbidden)
    monkeypatch.setattr(runner, "analyse_controller", forbidden)
    plan = prepare_plan()
    assert plan_hash(plan) == plan["plan_hash"]
    assert plan["work_counts"]["primary_cells"] == 22
    assert plan["work_counts"]["atomic_items"] == 24
    assert len(plan["features"]) == 11 and len(plan["items"]) == 24
    assert plan["pre_freeze_exposure"]["actual_non_neutral_I0_cells"] == 0


def test_execution_refuses_missing_or_unpushed_freeze(monkeypatch, tmp_path):
    import rs_constraint_lab.gen008i_exec as runner

    monkeypatch.setattr(runner, "analyse_controller", lambda *args, **kwargs: pytest.fail("unfrozen scientific call"))
    with pytest.raises(FrozenPlanError):
        execute(ROOT, tmp_path, None)
    monkeypatch.setattr(runner, "require_frozen_plan", lambda *args, **kwargs: prepare_plan())
    monkeypatch.setattr(runner, "remote_contains", lambda *args: False)
    with pytest.raises(FrozenPlanError, match="pushed"):
        require_execution(ROOT, "f" * 40)


def test_source_drift_is_refused_before_execution(monkeypatch):
    import rs_constraint_lab.gen008i_exec as runner

    plan = prepare_plan()
    plan["analysis_source_sha256"] = {"constraint-lab/src/rs_constraint_lab/history_roles.py": "0" * 64}
    monkeypatch.setattr(runner, "require_frozen_plan", lambda *args, **kwargs: plan)
    monkeypatch.setattr(runner, "remote_contains", lambda *args: True)
    with pytest.raises(FrozenPlanError, match="drift"):
        require_execution(ROOT, "f" * 40)


def test_corrupt_rational_diagnostic_is_not_a_scientific_null(synthetic_result):
    broken = copy.deepcopy(synthetic_result)
    broken["validation"]["stationary_residual"] = Fraction(1, 10**50)
    with pytest.raises(HistoryError, match="stationary_residual"):
        validate_result(broken)


def test_prompt_and_canonical_method_representations():
    prompt = ROOT / "constraint-lab/provenance/prompts/008I-v0.8i-agent-input.md"
    assert prompt.stat().st_size == 54988
    assert sha256_file(prompt) == "dbd4e70f24adc7f23aa529748226ed0f26944a84db0e1b952f31e204e5ac817f"
    assert sha256_file(prompt) not in prompt.read_text()
    assert sha256_file(ROOT / "research-methods/open-thetical-research.md") == "2d9023955ddfaf269131033589c547cea7090c72caf2577ab28f7138dfb388dd"
    rows = [json.loads(line) for line in (ROOT / "constraint-lab/provenance/ledger.jsonl").read_text().splitlines()]
    metadata = next(row for row in rows if row.get("prompt_id") == "008H" and row["record_type"] == "prompt_representation")
    assert metadata["authored_prompt_bytes"] == 46109 and metadata["agent_input_prompt_bytes"] == 46117
    assert metadata["authored_prompt_sha256"] != metadata["agent_input_prompt_sha256"]


@PUBLISHED
def test_all_published_primary_cells_and_exact_full_balance():
    summary = read_json(SUMMARY)
    plan = require_execution(ROOT, summary["frozen_analysis_plan_commit"])
    assert plan["work_counts"]["primary_cells"] == 22
    checks = 0
    for item in plan["items"]:
        if item["kind"] != "controller":
            continue
        envelope = read_json(ROOT / "constraint-lab/reports/items/generation-008i" / (item["item_id"] + ".json"))
        result = decode(envelope["result"])
        validate_result(result)
        model = RoleController(item["feature"], Fraction(item["m"]))
        assert covariance_gap(model) == 0
        structure = role_orbits()
        quotient, gap = aggregate_quotient(model.kernel(), structure.members, structure.orbit_of)
        assert gap == 0 and [dict(row) for row in result["quotient_kernel"]] == list(quotient)
        assert balance_gap(result["stationary_joint"], model.kernel()) == 0
        assert result["atlas"]["projected_markov_order"] == (1 if result["atlas"]["strong_lumpability"] else 2)
        assert result["temporal"]["order2_sufficiency_gap"] == 0
        assert result["temporal"]["consistent_material_triples"] == 2304
        if model.feature.family == "A":
            assert result["stationary_joint"] == [Fraction(1, 384)] * 384
            columns = [Fraction(0)] * 384
            for row in model.kernel():
                for target, value in row.items():
                    columns[target] += value
            assert columns == [Fraction(1)] * 384
        if model.feature.family == "B":
            for p in range(64):
                assert all(model.pair_probabilities(p, h) == model.pair_probabilities(p, 0) for h in range(6))
            assert result["atlas"]["strong_lumpability"] and result["atlas"]["projected_markov_order"] == 1
        assert Decimal(result["atlas"]["neutral_JS_label_given_class"]) == 0
        assert Fraction(result["validation"]["Kpi_stationary_residual"]) == 0
        checks += result["full_crosscheck"]["performed"]
    assert checks == 6
    for path, digest in summary["detail_sha256"].items():
        assert sha256_file(ROOT / path) == digest


@PUBLISHED
def test_published_complement_and_reciprocity_receipts_are_distinct_levels():
    result = decode(read_json(ROOT / "constraint-lab/reports/tables/generation-008i-equivalence.json"))
    validate_result(result)
    assert len(result["complement_checks"]) == 22
    assert len(result["reciprocity_checks"]) == 22 * 11 * 2
    assert all(row["kernel_gap"] == 0 for row in result["reciprocity_matches"])
    assert "full_kernel_fingerprint" in result["groups"]


def _git(*args, check=True):
    return subprocess.run(["git", "-C", str(ROOT), *args], check=check, capture_output=True)


@PUBLISHED
def test_generation_008i_preserves_historical_artifacts_and_separate_freezes():
    parent = "ad5b656e26fe66610b583aedccdd34593e13791a"
    old = set(_git("ls-tree", "-r", "--name-only", parent).stdout.decode().splitlines())
    changed = set(_git("diff", "--name-only", parent, "--", "books", "constraint-lab/reports", "constraint-lab/exploration", "constraint-lab/provenance", "constraint-lab/coherence/snapshots").stdout.decode().splitlines())
    assert old & changed <= {"constraint-lab/provenance/ledger.jsonl"}
    for path in ("constraint-lab/formal/theorem-catalog.jsonl", "constraint-lab/coherence/findings.jsonl", "constraint-lab/coherence/relations.jsonl", "constraint-lab/provenance/ledger.jsonl", "constraint-lab/formal/book-integration-map.md"):
        assert (ROOT / path).read_bytes().startswith(_git("show", f"{parent}:{path}").stdout)
    for summary_name, item_path in (
        ("generation-008i-round-i0-tables.json", "constraint-lab/reports/items/generation-008i/I0-ADJ_FORM-m025.json"),
        ("generation-008i-round-i1-tables.json", "constraint-lab/reports/items/generation-008i-i1/I1-COORDINATE-SYMMETRY.json"),
    ):
        summary = read_json(ROOT / "constraint-lab/reports" / summary_name)
        commit = summary["frozen_analysis_plan_commit"]
        assert _git("merge-base", "--is-ancestor", commit, "HEAD").returncode == 0
        assert _git("cat-file", "-e", f"{commit}:{item_path}", check=False).returncode != 0
        assert _git("cat-file", "-e", "HEAD:" + item_path).returncode == 0


@pytest.mark.skipif(not (ROOT / "constraint-lab/coherence/snapshots/through-generation-008i.md").exists(), reason="8I coherence checked after close-out")
def test_generation_008i_coherence_snapshot_and_reusable_catalogue():
    from rs_constraint_lab.coherence import load_ledger, snapshot_text
    from rs_constraint_lab.formal import load_catalog, validate_catalog

    directory = ROOT / "constraint-lab/coherence"
    assert (directory / "snapshots/through-generation-008i.md").read_text() == snapshot_text(directory, title="Through Generation 008I")
    catalog = load_catalog()
    assert validate_catalog(catalog) == []
    new = [row for row in catalog if row["source_generations"] == ["008I"]]
    assert {row["theorem_id"] for row in new} == {*(f"CL-T{n}" for n in range(36, 45)), "CL-F06"}
    findings, relations = load_ledger(directory)
    method = next(row for row in findings if row["finding_id"] == "F8I-OTR-METHODOLOGICAL-ADOPTION")
    assert method["epistemic_layer"] == "METHODOLOGICAL"
    assert "constraint-lab/methodology/open-thetical-application.md" in method["evidence_refs"]
    assert next(row for row in findings if row["finding_id"] == "Q-H-CONSEQUENTIAL-FUNCTIONS")["status"] == "unresolved"
    assert any(row["from_finding"] == "Q-H-CONSEQUENTIAL-FUNCTIONS" and row["relation_type"] == "partially_answered_by" and row["created_generation"] == "008I" for row in relations)
