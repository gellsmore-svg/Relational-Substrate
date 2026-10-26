"""Typed synchronization, exact counterexamples and independent matrix checks."""

from __future__ import annotations

from fractions import Fraction
import importlib.util
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "provenance/label-sync-analysis-check.py"
MODULE_SPEC = importlib.util.spec_from_file_location("label_sync_analysis", SCRIPT)
ANALYSIS = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(ANALYSIS)


def partner():
    return ANALYSIS.component(2, [ANALYSIS.event("a", 0, 1), ANALYSIS.event("a", 1, 0)], ("a", "b"))


def test_joint_handshake_private_events_and_duplicate_weights_match_hand_table():
    left = ANALYSIS.component(2, [ANALYSIS.event("sync", 0, 1), ANALYSIS.event("sync", 0, 1, 2),
                                  ANALYSIS.event("private", 0, 0)])
    right = ANALYSIS.component(2, [ANALYSIS.event("sync", 0, 1, 2)])
    combined = ANALYSIS.compose(left, right)
    assert ANALYSIS.labelled_weights(combined) == ANALYSIS.matrix_product_oracle(left, right)
    assert ANALYSIS.kernel(combined)[0] == [Fraction(1, 7), 0, 0, Fraction(6, 7)]


def test_halt_is_not_a_synchronising_unit_despite_the_same_aggregate_kernel():
    neutral = ANALYSIS.unit(("a", "b"))
    dead = ANALYSIS.component(1, [], ("a", "b"))
    assert ANALYSIS.kernel(neutral) == ANALYSIS.kernel(dead) == [[1]]
    assert ANALYSIS.weighted_equal(ANALYSIS.compose(partner(), neutral), partner())
    assert ANALYSIS.kernel(ANALYSIS.compose(partner(), dead)) == [[1, 0], [0, 1]]


def test_standalone_lumpability_can_fail_after_sync_with_a_fixed_partner():
    hidden = ANALYSIS.hidden_component(("a", "b"))
    labels = [0, 0, 1, 1]
    assert ANALYSIS.observed_kernel(hidden, labels)["rows"] == [[0, 1], [1, 0]]
    assert ANALYSIS.weighted_quotient(hidden, labels)["component"] is None
    combined = ANALYSIS.compose(hidden, partner())
    report = ANALYSIS.observed_kernel(combined, ANALYSIS.product_observation(labels, [0, 1]))
    assert report["exact"] is False and report["rows"] is None
    assert report["witness"]["states"] == [0, 2]
    assert report["witness"]["first_row"] == [0, 0, 0, 1]
    assert report["witness"]["second_row"] == [1, 0, 0, 0]


def test_private_context_exposes_raw_scaling_without_requiring_a_new_mask():
    scaled = ANALYSIS.hidden_component(("a", "a"), (1, 2))
    labels = ANALYSIS.product_observation([0, 0, 1, 1], [0, 1])
    assert ANALYSIS.observed_kernel(ANALYSIS.compose(scaled, partner()), labels)["exact"] is True
    tick = ANALYSIS.component(2, partner()["events"] + [ANALYSIS.event("tick", 0, 0), ANALYSIS.event("tick", 1, 1)], ("a", "b"))
    report = ANALYSIS.observed_kernel(ANALYSIS.compose(scaled, tick), labels)
    assert report["rows"] is None
    assert report["witness"]["first_row"] == [Fraction(1, 2), 0, 0, Fraction(1, 2)]
    assert report["witness"]["second_row"] == [Fraction(1, 3), 0, 0, Fraction(2, 3)]


@pytest.mark.parametrize("mode", ["hold", "flip", "reset"])
def test_weighted_quotients_can_hide_fixed_or_evolving_state(mode):
    macro = partner()
    micro = ANALYSIS.lift(macro, mode)
    labels = [0, 0, 1, 1]
    quotient = ANALYSIS.weighted_quotient(micro, labels)
    assert quotient["exact"] and ANALYSIS.weighted_equal(quotient["component"], macro)
    combined = ANALYSIS.compose(micro, macro)
    observed = ANALYSIS.observed_kernel(combined, ANALYSIS.product_observation(labels, [0, 1]))
    assert observed["rows"] == ANALYSIS.kernel(ANALYSIS.compose(macro, macro))


def test_constant_and_identity_observations_do_not_create_false_necessity():
    hidden = ANALYSIS.hidden_component(("a", "b"))
    assert ANALYSIS.observed_kernel(hidden, [0, 0, 0, 0])["rows"] == [[1]]
    assert ANALYSIS.weighted_quotient(hidden, [0, 0, 0, 0])["exact"] is False
    identity = ANALYSIS.weighted_quotient(hidden, list(range(4)))
    assert identity["exact"] and ANALYSIS.weighted_equal(identity["component"], hidden)


def test_empty_handshake_interleaves_private_updates_and_all_halt_stays_halt():
    left = ANALYSIS.component(2, [ANALYSIS.event("move", 0, 1)], ())
    right = ANALYSIS.component(2, [ANALYSIS.event("move", 0, 1)], ())
    assert ANALYSIS.kernel(ANALYSIS.compose(left, right))[0] == [0, Fraction(1, 2), Fraction(1, 2), 0]
    dead = ANALYSIS.component(2, [], ())
    assert ANALYSIS.observed_kernel(dead, [0, 0])["rows"] == [[1]]
    assert ANALYSIS.weighted_equal(ANALYSIS.compose(left, ANALYSIS.unit(())), left)


def test_invalid_interface_states_weights_and_observations_are_rejected():
    with pytest.raises(ValueError, match="handshake"):
        ANALYSIS.compose(partner(), ANALYSIS.unit(("different",)))
    for invalid in (-1, True, Fraction(1, 2)):
        with pytest.raises(ValueError, match="weight"):
            ANALYSIS.component(2, [ANALYSIS.event("a", 0, 1, invalid)])
    with pytest.raises(ValueError, match="state"):
        ANALYSIS.component(2, [ANALYSIS.event("a", 0, 2)])
    for labels in ([0], [0, 2], [False, True]):
        with pytest.raises(ValueError, match="observation"):
            ANALYSIS.observed_kernel(partner(), labels)


def test_bounded_event_matrix_associativity_and_quotient_oracles_agree():
    checked = ANALYSIS.run_checks()
    assert checked["status"] == "verified"
    assert checked["pair_oracle_checks"] == checked["basis_component_count"] ** 2
    assert checked["associative_triples_checked"] == checked["basis_component_count"] ** 3
    assert checked["weighted_quotient_contexts_checked"] == 3 * checked["basis_component_count"] ** 2
    assert checked["scientific_worker_invocations"] == checked["new_atlas_cells"] == 0
