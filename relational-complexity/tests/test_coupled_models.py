"""Typed couplings. They do not run an atlas round."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from rrc import ENGINE_VERSION
from rrc.coupled_models import (
    correspondence,
    coupled_records,
    subset_invariant,
)

ROOT = Path(__file__).resolve().parents[1]
SEVENTH = Fraction(1, 7)


def test_agreement_is_a_conjugacy_only_when_the_image_is_invariant():
    records = coupled_records()
    coupled = records["coupled_agreement"]
    identified = records["identified_toggle"]["probabilities"]
    assert coupled["method"] == "event-kernel-0.2.0"
    assert coupled["new_primitive"] is False
    assert coupled["joint_in_one_step_support"] is False
    assert coupled["universal_impossibility"] is False
    assert coupled["two_step_paths"] == [(0, 1, 3), (0, 2, 3)]
    assert coupled["one_step_successors_of_zero"] == [1, 2]
    assert coupled["completions"] == [
        "normalised_events",
        "halt_self_loop",
        "halt_self_loop",
        "normalised_events",
    ]
    assert coupled["forward"]["image_invariant"] is True
    assert coupled["forward"]["conjugate"] is True
    assert coupled["forward"]["restricted_rows"] == identified
    assert coupled["reverse"]["conjugate"] is True
    assert coupled["reverse"]["restricted_rows"] == identified
    assert coupled["leaked_image"]["injective"] is True
    assert coupled["leaked_image"]["image_invariant"] is False
    assert coupled["leaked_image"]["conjugate"] is False
    assert coupled["leaked_image"]["restricted_rows"] is None
    assert subset_invariant(coupled["probabilities"], {1, 2}) is True
    assert coupled["x_projection"]["exact"] is False
    assert coupled["x_projection"]["rows"] is None
    assert coupled["x_projection"]["defect_l1"] == 1
    assert coupled["h_projection"]["rows"] is None
    free = records["free_product"]
    assert free["agreement_correspondence"]["image_invariant"] is False
    assert free["agreement_correspondence"]["restricted_rows"] is None
    with pytest.raises(ValueError, match="cover the smaller"):
        correspondence(identified, coupled["probabilities"], {0: 0})
    with pytest.raises(ValueError, match="injective"):
        correspondence(identified, coupled["probabilities"], {0: 0, 1: 0})


def test_rate_support_and_rescaling_stay_inside_single_toggles():
    records = coupled_records()
    independent = records["independent_product"]
    rescaled = records["rescaled_rates"]
    support = records["support_constraint"]
    assert independent["classification"] == "ordinary_single_toggle"
    assert rescaled["classification"] == "ordinary_single_toggle"
    assert support["classification"] == "ordinary_single_toggle"
    assert independent["new_event_type"] is False
    assert support["new_primitive"] is False
    hand = [
        [Fraction(0), Fraction(2, 7), Fraction(5, 7), Fraction(0)],
        [Fraction(2, 7), Fraction(0), Fraction(0), Fraction(5, 7)],
        [Fraction(5, 7), Fraction(0), Fraction(0), Fraction(2, 7)],
        [Fraction(0), Fraction(5, 7), Fraction(2, 7), Fraction(0)],
    ]
    assert independent["probabilities"] == hand
    assert rescaled["probabilities"] == hand
    assert independent["aggregated_weights"][0] == [0, 2, 5, 0]
    assert rescaled["aggregated_weights"][0] == [0, 2, 5, 0]
    assert rescaled["aggregated_weights"][2] == [10, 0, 0, 4]
    assert independent["aggregated_weights"][2] == [5, 0, 0, 2]
    x_rows = [[Fraction(5, 7), Fraction(2, 7)], [Fraction(2, 7), Fraction(5, 7)]]
    h_rows = [[Fraction(2, 7), Fraction(5, 7)], [Fraction(5, 7), Fraction(2, 7)]]
    assert independent["x_projection"]["exact"] is True
    assert independent["x_projection"]["rows"] == x_rows
    assert independent["h_projection"]["rows"] == h_rows
    assert rescaled["x_projection"]["rows"] == x_rows
    assert rescaled["h_projection"]["rows"] == h_rows
    assert independent["x_projection"]["defect_l1"] == 0
    support_hand = [
        [Fraction(0), Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(0), Fraction(1)],
        [Fraction(5, 7), Fraction(0), Fraction(0), Fraction(2, 7)],
        [Fraction(0), Fraction(5, 7), Fraction(2, 7), Fraction(0)],
    ]
    assert support["probabilities"] == support_hand
    assert support["enabled_event_counts"] == [1, 1, 2, 2]
    assert {event["kind"] for event in support["events"]} == {"toggle"}
    assert all((event["source"] ^ event["target"]).bit_count() == 1 for event in support["events"])
    assert support["x_projection"]["exact"] is False
    assert support["x_projection"]["rows"] is None
    assert support["x_projection"]["defect_l1"] == 2 * SEVENTH
    assert support["h_projection"]["exact"] is True
    assert support["h_projection"]["rows"] == [
        [Fraction(0), Fraction(1)],
        [Fraction(5, 7), Fraction(2, 7)],
    ]
    for record in (independent, rescaled, support):
        for row in record["probabilities"]:
            assert sum(row) == 1


def test_a_family_bit_is_listed_and_the_joint_flip_is_not():
    family = coupled_records()["family_membership"]
    assert family["fixed"]["n_states"] == 2
    assert family["fixed"]["classification"] == "family_not_in_the_state"
    assert family["listed"]["classification"] == "reducible_to_listed_bit"
    assert family["joint"]["classification"] == "outside_one_step_single_toggle"
    assert family["joint"]["hamming"] == 2
    assert family["joint"]["in_one_step_support"] is False
    assert family["joint"]["probabilities"][0][3] == 1
    assert family["split_block_count"] == 2
    assert family["joined_block_count"] == 1
    assert family["block_count_is_state"] is False
    assert family["fixed"]["new_primitive"] is False


def test_typed_couplings_reuse_the_atlas_017_lists_and_are_not_a_round():
    records = coupled_records()
    plan = json.loads((ROOT / "plans" / "atlas-017.json").read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in plan["items"]}
    assert by_id["A17-coupled"]["events"] == records["coupled_agreement"]["events"]
    assert by_id["A17-identified"]["events"] == records["identified_toggle"]["events"]
    assert by_id["A17-g0"]["rows"] == [[1, 1], [1, 1], [1, 1], [1, 1]]
    assert plan["method_id"] == "event-kernel-0.1.0"
    stored = json.loads(
        (ROOT / "results" / "atlas-017" / "items" / "A17-coupled" / "result.json").read_text(
            encoding="utf-8"
        )
    )
    assert stored["method"] == "event-kernel-0.1.0"
    source = (ROOT / "src" / "rrc" / "coupled_models.py").read_text(encoding="utf-8")
    assert "compile_weight_table" not in source
    assert "ENGINE_VERSION" not in source
    assert ENGINE_VERSION == "rrc-0.4.0"
    note = (ROOT / "docs" / "coupled-models.md").read_text(encoding="utf-8")
    for phrase in (
        "not a frozen round",
        "rrc-0.4.0",
        "event-kernel-0.2.0",
        "not a new primitive",
        "No intervention operator is defined",
        "image is not invariant",
        "quotient rows are absent",
        "2/7",
        "5/7",
        "Atlas-017 was not rerun",
        "no ledger row",
        "no equivalence",
        "does not exclude every history-dependent description",
        "two single toggles",
        "No universal impossibility is claimed",
    ):
        assert phrase in note
    assert "occupation" not in records["support_constraint"]
    assert "stationary" not in note
