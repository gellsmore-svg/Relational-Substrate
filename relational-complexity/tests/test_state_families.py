"""Typed state and event families. Not a frozen round."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from rrc import ENGINE_VERSION
from rrc.coordinate_examples import derived_pair_count
from rrc.state_families import (
    changing_family_report,
    derived_report,
    encode_family_state,
    extended_report,
    family_records,
    identified_to_duplicated,
    interface_report,
    intervention_report,
    joint_event_report,
    single_toggle_successors,
    swap_pair_bits,
)

ROOT = Path(__file__).resolve().parents[1]


def _hamming(left: int, right: int) -> int:
    return (left ^ right).bit_count()


def test_derived_count_adds_no_bit_and_survives_a_bit_swap():
    report = derived_report()
    assert report["classification"] == "reducible_observation"
    assert report["new_state"] is False
    assert report["counts"][1] == report["counts"][2] == 1
    for mask in range(4):
        assert report["counts"][mask] == derived_pair_count(mask)
        assert report["counts_after_bit_swap"][mask] == derived_pair_count(swap_pair_bits(mask))
        assert report["counts"][mask] == report["counts_after_bit_swap"][mask]
    assert report["edge_names"] != report["edge_names_after_bit_swap"]
    with pytest.raises(ValueError, match="width 2"):
        swap_pair_bits(4)
    with pytest.raises(ValueError, match="integer mask"):
        swap_pair_bits(True)


def test_extended_bit_is_listed_and_states_1_and_5_differ():
    report = extended_report()
    assert report["classification"] == "reducible_to_listed_bit"
    assert report["equivalence"] == "EQ-027"
    assert report["new_event_type"] is False
    assert report["states_sharing_pair_mask"] == (1, 5)
    assert (1 & 3) == (5 & 3) == report["pair_mask"] == 1
    assert report["third_bits"] == (0, 1)
    assert derived_pair_count(1 & 3) == derived_pair_count(5 & 3) == 1
    assert report["n_bits"] == 3
    assert report["n_states"] == 8


def test_joint_step_is_outside_one_step_support_and_reachable_in_two():
    report = joint_event_report()
    assert report["classification"] == "outside_one_step_single_toggle"
    assert report["universal_impossibility"] is False
    successors = single_toggle_successors(3, 0)
    assert successors == [1, 2, 4]
    assert report["one_step_successors"] == successors
    assert report["target"] == 5
    assert report["reachable_in_one_step"] is False
    assert report["hamming"] == 2
    assert 5 not in successors
    paths = report["two_step_paths"]
    assert paths == [(0, 1, 5), (0, 4, 5)]
    for source, mid, target in paths:
        assert _hamming(source, mid) == 1
        assert _hamming(mid, target) == 1
        assert mid in single_toggle_successors(3, source)
        assert target in single_toggle_successors(3, mid)
    assert (0 ^ 5).bit_count() == 2


def test_identified_and_duplicated_interfaces_have_different_widths():
    report = interface_report()
    identified = report["identified"]
    duplicated = report["duplicated"]
    assert identified["family"] == "identified_interface"
    assert duplicated["family"] == "duplicated_interface"
    assert identified["classification"] == "reducible_to_listed_carrier"
    assert identified["n_bits"] == 3
    assert identified["n_states"] == 8
    assert duplicated["n_bits"] == 4
    assert duplicated["n_states"] == 16
    assert identified["n_bits"] != duplicated["n_bits"]
    assert duplicated["free_product_classification"] == "single_toggle_on_more_bits"
    assert duplicated["coupled_update_classification"] == "outside_one_step_single_toggle"
    assert duplicated["map_is_bijection_onto_agreement"] is True
    assert len(duplicated["agreement_states"]) == 8
    assert duplicated["one_copy_toggle_leaves_agreement"] is True
    assert duplicated["coupled_update_matches_identified_toggle"] is True
    assert duplicated["coupled_update_from_zero"] == 6
    assert duplicated["coupled_update_in_one_step_support"] is False
    assert 6 not in single_toggle_successors(4, 0)
    assert _hamming(0, 6) == 2
    image = []
    for e0 in (0, 1):
        for e1 in (0, 1):
            for e2 in (0, 1):
                image.append(identified_to_duplicated(e0, e1, e2))
                identified_state = e0 | (e1 << 1) | (e2 << 2)
                copied = identified_to_duplicated(e0, e1, e2)
                toggled_copy = identified_to_duplicated(e0, 1 - e1, e2)
                assert toggled_copy == copied ^ (1 << 1) ^ (1 << 2)
                assert _hamming(identified_state, identified_state ^ (1 << 1)) == 1
    assert sorted(set(image)) == duplicated["agreement_states"]
    assert len(set(image)) == 8
    with pytest.raises(ValueError, match="0 or 1"):
        identified_to_duplicated(0, 2, 0)


def test_changing_family_bit_is_listed_and_the_joint_change_is_not():
    report = changing_family_report()
    assert report["split_block_count"] == 2
    assert report["joined_block_count"] == 1
    assert report["split_blocks"] != report["joined_blocks"]
    assert encode_family_state(0, 0) == 0
    assert encode_family_state(0, 1) == 4
    assert encode_family_state(1, 1) == 5
    assert report["family_bit_classification"] == "reducible_to_listed_bit"
    assert report["same_step_classification"] == "outside_one_step_single_toggle"
    assert report["family_bit_hamming"] == 1
    assert report["family_bit_in_one_step_support"] is True
    assert report["joint_hamming"] == 2
    assert report["joint_in_one_step_support"] is False
    assert report["two_step_paths"] == [(0, 1, 5), (0, 4, 5)]
    assert report["fixed_instrument_states"] == 4
    assert report["encoded_states"] == 8
    assert 4 in single_toggle_successors(3, 0)
    assert 5 not in single_toggle_successors(3, 0)
    with pytest.raises(ValueError, match="0 or 1"):
        encode_family_state(0, True)


def test_intervention_operator_is_undefined():
    report = intervention_report()
    assert report["defined"] is False
    assert report["operator"] is None
    assert report["distribution"] is None
    assert report["comparison_law"] is None
    assert report["propagation"] == "undefined"
    assert report["statement"] == "No intervention operator is defined."
    assert "probability" not in report


def test_families_are_not_collapsed_and_the_note_is_not_a_round():
    records = family_records()
    names = [record["family"] for record in records]
    assert names == [
        "derived",
        "extended",
        "joint_event",
        "identified_interface",
        "duplicated_interface",
        "changing_family",
    ]
    assert len(set(names)) == len(names)
    classifications = {
        "derived": "reducible_observation",
        "extended": "reducible_to_listed_bit",
        "joint_event": "outside_one_step_single_toggle",
        "identified_interface": "reducible_to_listed_carrier",
    }
    by_name = {record["family"]: record for record in records}
    for name, classification in classifications.items():
        assert by_name[name]["classification"] == classification
    assert len(set(classifications.values())) == 4
    source = (ROOT / "src" / "rrc" / "state_families.py").read_text(encoding="utf-8")
    assert "compile_weight_table" not in source
    assert "ENGINE_VERSION" not in source
    assert ENGINE_VERSION == "rrc-0.4.0"
    note = (ROOT / "docs" / "state-event-families.md").read_text(encoding="utf-8")
    for phrase in (
        "not a frozen round",
        "rrc-0.4.0",
        "No intervention operator is defined",
        "EQ-027",
        "not a new primitive",
        "States 1 and 5",
        "No universal impossibility is claimed",
        "Hamming distance is 2",
        "widths are 3 and 4",
        "IDEA-L23",
        "not selected",
        "ATLAS-Q15 stays open",
        "Potential intersection",
        "realised intersection",
    ):
        assert phrase in note
    for heading in (
        "## Derived coordinate",
        "## Extended state",
        "## Joint event",
        "## Identified interface",
        "## Duplicated interface",
        "## Changing block family",
        "## Intervention",
    ):
        assert heading in note
    ideas = {
        json.loads(line)["idea_id"]: json.loads(line)
        for line in (ROOT / "atlas" / "ideas.jsonl").read_text(encoding="utf-8").splitlines()
    }
    assert ideas["IDEA-L22"]["status"] == "partial"
    assert "not a frozen cell" in ideas["IDEA-L22"]["methods"]
    assert "EQ-027" in ideas["IDEA-L22"]["methods"]
    assert ideas["IDEA-L23"]["status"] == "open"
    assert ideas["IDEA-L23"]["status"] != "selected"
    assert "not a frozen cell" in ideas["IDEA-L23"]["methods"]
    assert "not selected" in ideas["IDEA-L23"]["methods"]
    coverage = {
        json.loads(line)["coverage_id"]: json.loads(line)
        for line in (ROOT / "atlas" / "coverage.jsonl").read_text(encoding="utf-8").splitlines()
    }
    assert coverage["COV-HIGHER-ORDER-STATE"]["status"] == "open"
    assert "not a frozen round" in coverage["COV-HIGHER-ORDER-STATE"]["method"]
    assert "state-event-families.md" in coverage["COV-HIGHER-ORDER-STATE"]["notes"]
    assert coverage["COV-DYNAMICAL-PROPAGATION"]["status"] == "open"
    assert "not implemented" in coverage["COV-DYNAMICAL-PROPAGATION"]["method"]
    assert "No intervention operator is defined" in coverage["COV-DYNAMICAL-PROPAGATION"]["notes"]
    gate = (ROOT / "docs" / "compilation-gate.md").read_text(encoding="utf-8")
    assert "not a new primitive" in gate
    assert "state-event-families.md" in gate
