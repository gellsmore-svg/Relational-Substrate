"""Shared-state interfaces: dynamics, consistency and representation boundaries."""

from fractions import Fraction
import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_checker(filename, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "provenance" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


A = load_checker("shared-port-analysis-check.py", "shared_port_analysis")
OLD = load_checker("label-sync-analysis-check.py", "accepted_cartesian_analysis")


@pytest.mark.parametrize("feedback", [False, True])
def test_dynamic_shared_port_has_eight_states_and_a_listed_bit_encoding(feedback):
    left, right = A.feedback_pair(feedback)
    identified = A.compose(left, right)
    assert identified["n_states"] == 8
    assert A.kernel(identified) == A.bit_kernel(feedback)
    for record in identified["events"]:
        assert (record["source"] ^ record["target"]).bit_count() == 1
        if record["label"] == "h":
            assert identified["ports"][record["source"]] != identified["ports"][record["target"]]


def test_port_feedback_changes_the_next_retained_state_law():
    combined = A.compose(*A.feedback_pair(True))
    observation = [2 * (c[0] // 2) + c[1] % 2 for c in combined["coordinates"]]
    report = A.observed_kernel(A.kernel(combined), observation)
    assert not report["exact"] and report["rows"] is None
    assert report["witness"]["states"] == [0, 2]
    assert report["witness"]["first_row"] == [Fraction(1, 3), Fraction(1, 3), Fraction(1, 3), 0]
    assert report["witness"]["second_row"] == [Fraction(1, 4), Fraction(1, 4), Fraction(1, 2), 0]


def test_a_closed_no_feedback_prediction_need_not_inherit_the_port_type():
    combined = A.compose(*A.feedback_pair(False))
    observation = [2 * (c[0] // 2) + c[1] % 2 for c in combined["coordinates"]]
    assert A.observed_kernel(A.kernel(combined), observation)["exact"]
    boundary = A.boundary_factor(combined, observation)
    assert not boundary["defined"] and boundary["port_map"] is None
    assert boundary["witness"] == [0, 2]
    assert A.boundary_factor(combined, combined["ports"])["port_map"] == [0, 1]


def test_preserving_a_boundary_is_not_by_itself_a_closed_prediction():
    system = A.component([0, 0, 1, 1], [A.event("h", 0, 2), A.event("h", 1, 3, 2),
                                      A.event("clock", 0, 0), A.event("clock", 1, 1)])
    observation = system["ports"]
    assert A.boundary_factor(system, observation)["defined"]
    assert not A.observed_kernel(A.kernel(system), observation)["exact"]


def test_target_agreement_is_required_even_when_the_shared_label_matches():
    left = A.component([0, 1], [A.event("h", 0, 1, 2), A.event("tick", 0, 0)])
    right = A.component([0, 1], [A.event("h", 0, 0, 3)])
    report = A.agreement_report(left, right)
    assert report["leakage"] == [Fraction(6, 7), 0]
    assert not report["invariant"] and report["restricted_rows"] is None
    assert report["conditional_rows"] == report["identified_rows"] == [[1, 0], [0, 1]]
    assert report["support"]["witness"]["positive_product_weight"] == 6


def test_all_rejected_events_make_conditioning_undefined_but_the_guarded_row_halts():
    left = A.component([0, 1], [A.event("h", 0, 1, 2)])
    right = A.component([0, 1], [A.event("h", 0, 0, 3)])
    report = A.agreement_report(left, right)
    assert report["leakage"][0] == 1
    assert report["conditional_rows"][0] is None
    assert report["identified_rows"][0] == [1, 0]
    assert A.compose(left, right)["events"] == []


def test_equal_component_port_marginals_do_not_supply_a_shared_random_choice():
    system = A.component([0, 1], [A.event("h", s, t, t + 1) for s in range(2) for t in range(2)])
    assert A.kernel(system) == [[Fraction(1, 3), Fraction(2, 3)]] * 2
    report = A.agreement_report(system, system)
    assert report["leakage"] == [Fraction(4, 9), Fraction(4, 9)]
    assert report["identified_rows"] == [[Fraction(1, 5), Fraction(4, 5)]] * 2
    assert report["restricted_rows"] is None


def test_compatible_copies_have_an_invariant_image_and_raw_restriction():
    left, right = A.feedback_pair(True)
    report = A.agreement_report(left, right)
    assert report["invariant"]
    assert report["restricted_rows"] == report["identified_rows"]
    assert report["agreement_image"] == [0, 1, 6, 7, 8, 9, 14, 15]


def test_counting_rejected_attempts_as_holds_is_a_different_declared_clock():
    system = A.component([0, 1], [A.event("h", s, t, t + 1) for s in range(2) for t in range(2)])
    report = A.agreement_report(system, system)
    assert report["rejected_attempts_hold_control"] == [[Fraction(5, 9), Fraction(4, 9)],
                                                      [Fraction(1, 9), Fraction(8, 9)]]
    assert report["rejected_attempts_hold_control"] != report["identified_rows"]


@pytest.mark.parametrize("mode", ["hold", "flip", "reset"])
def test_internal_private_updates_preserve_the_interface_contract(mode):
    base = A.component([0, 1], [A.event("h", 0, 1), A.event("private", 0, 0)])
    lifted = A.lift(base, mode)
    combined = A.compose(lifted, base)
    assert A.matrices(combined) == A.restriction_oracle(lifted, base)
    A.validate(combined)


def test_the_unit_relays_port_values_and_preserves_internal_private_moves():
    system, _ = A.feedback_pair(True)
    neutral = A.unit(2)
    assert len(neutral["events"]) == 4
    assert A.canonical_weights(A.compose(neutral, system), lambda c: c[1:]) == A.canonical_weights(system)
    assert A.canonical_weights(A.compose(system, neutral), lambda c: c[:-1]) == A.canonical_weights(system)
    assert not A.agreement_report(system, neutral)["invariant"]


def test_a_singleton_port_reduces_to_the_accepted_cartesian_product():
    left = A.component([0, 0], [A.event("h", 0, 1), A.event("p", 1, 0, 2)], 1)
    right = A.component([0, 0], [A.event("h", 0, 1, 3), A.event("p", 0, 0)], 1)
    assert A.matrices(A.compose(left, right)) == OLD.labelled_weights(OLD.compose(left, right))


def test_empty_handshake_has_a_unit_and_only_port_preserving_private_moves():
    system = A.component([0, 0, 1, 1], [A.event("p", 0, 1), A.event("q", 2, 3, 2)], 2, ())
    neutral = A.unit(2, ())
    assert A.canonical_weights(A.compose(system, neutral), lambda c: c[:-1]) == A.canonical_weights(system)
    assert A.agreement_report(system, system)["invariant"]


def test_duplicate_weights_and_zero_weight_port_writes_have_no_hidden_effect():
    first = A.component([0, 1], [A.event("h", 0, 1), A.event("h", 0, 1, 2), A.event("p", 0, 1, 0)])
    second = A.component([0, 1], [A.event("h", 0, 1, 3)])
    assert A.matrices(first) == A.matrices(second)
    assert A.canonical_weights(A.compose(first, A.unit(2))) == A.canonical_weights(A.compose(second, A.unit(2)))


def test_nonbinary_port_and_multiple_shared_labels_iterate_without_a_bit_assumption():
    system = A.component([0, 1, 2], [A.event("h", 0, 1), A.event("h", 1, 2, 2),
                                   A.event("h", 2, 0), A.event("g", 1, 1)], 3, ("h", "g"))
    assert A.canonical_weights(A.compose(A.compose(system, system), system)) == A.canonical_weights(A.compose(system, A.compose(system, system)))
    assert A.agreement_report(system, system)["invariant"]


def test_dense_cartesian_oracle_matches_the_previous_sparse_event_implementation():
    left, right = A.feedback_pair(True)
    assert A.cartesian_matrices(left, right) == OLD.labelled_weights(OLD.compose(left, right))


def test_positive_private_port_writes_and_invalid_boundaries_are_rejected():
    with pytest.raises(ValueError, match="private event changes"):
        A.component([0, 1], [A.event("p", 0, 1)])
    with pytest.raises(ValueError, match="onto"):
        A.component([0, 0], [], 2)
    with pytest.raises(ValueError, match="port types"):
        A.compose(A.component([0, 1], []), A.component([0, 0], [], 1))
    with pytest.raises(ValueError, match="handshake"):
        A.compose(A.unit(2), A.unit(2, ("other",)))
    for observation in ([0], [0, 2], [False, True]):
        with pytest.raises(ValueError, match="observation"):
            A.boundary_factor(A.unit(2), observation)


@pytest.mark.parametrize("weight", [-1, True, Fraction(1, 2)])
def test_weights_must_be_nonnegative_integers(weight):
    with pytest.raises(ValueError, match="weight"):
        A.component([0, 1], [A.event("h", 0, 1, weight)])


def test_predeclared_sparse_dense_support_and_iteration_domains_agree():
    result = A.run_checks()
    assert result["basis_components"] == 7
    assert result["pair_oracle_checks"] == 49
    assert result["associativity_triples"] == 343
    assert result["lifted_pair_oracle_checks"] == 147
    assert result["scientific_worker_invocations"] == result["new_atlas_cells"] == 0
    assert result["status"] == "verified"
