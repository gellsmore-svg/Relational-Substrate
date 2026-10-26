"""Changing participation, fixed-protocol compilation and minimal actor-view refinement."""

from fractions import Fraction
import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def load(filename, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "provenance" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


A = load("switching-link-analysis-check.py", "switching_link_analysis")
OLD = load("label-sync-analysis-check.py", "accepted_label_sync")


def active(switch=(1, 1)):
    return A.network([[0, 1], [1, 0]], [[0, 1], [1, 0]], switch)


def as_component(weights, size):
    return {"n_states": size, "handshake": list(A.CHANNELS),
            "events": [A.event(label, s, t, value) for label, matrix in weights.items()
                       for s, row in enumerate(matrix) for t, value in enumerate(row) if value]}


def test_separate_joint_and_switch_steps_match_hand_derived_full_rows():
    model = active()
    matrix = A.normalise(A.direct_weights(model), 8)
    assert matrix[0] == [0, Fraction(1, 3), Fraction(1, 3), 0, Fraction(1, 3), 0, 0, 0]
    assert matrix[1] == [Fraction(1, 2), 0, 0, 0, 0, 0, 0, Fraction(1, 2)]
    report = A.block_report(matrix, [i // 2 for i in range(8)])
    assert report["rows"] is None and report["witness"]["states"] == [0, 1]
    assert report["witness"]["first_row"] == [Fraction(1, 3), Fraction(1, 3), Fraction(1, 3), 0]
    assert report["witness"]["second_row"] == [Fraction(1, 2), 0, 0, Fraction(1, 2)]


def test_nonunit_raw_weights_and_one_event_clock_survive_compilation():
    model = A.network([[0, 2], [1, 0]], [[0, 3], [1, 0]], (5, 7))
    direct = A.direct_weights(model)
    assert direct == A.matched_protocol_weights(A.compile_protocol(model))
    assert direct["left"][0][4] == 2 and direct["right"][0][2] == 3
    assert direct["joint"][1][7] == 6 and direct["switch"][1][0] == 7
    assert A.normalise(direct, 8)[1][7] == Fraction(6, 13)


@pytest.mark.parametrize("case", ["active", "partial", "nonbinary"])
def test_compiled_network_matches_the_previous_binary_sparse_composition(case):
    model = {"active": active(), "partial": A.network([[0, 1], [0, 0]], [[0, 1], [0, 0]]),
             "nonbinary": A.network([[0, 1, 0], [0, 0, 2], [1, 0, 0]], [[0, 2], [1, 0]], (1, 2))}[case]
    left, right, controller = A.compile_protocol(model)
    combined = OLD.compose(OLD.compose(left, right), controller)
    assert OLD.labelled_weights(combined) == A.direct_weights(model)
    assert OLD.kernel(combined) == A.normalise(A.direct_weights(model), combined["n_states"])


def test_passive_self_loops_are_real_protocol_participation():
    model = active()
    parts = A.compile_protocol(model)
    assert any(e["label"] == "right" and e["source"] == e["target"] and e["weight"] == 1 for e in parts[0]["events"])
    parts[0]["events"] = [e for e in parts[0]["events"] if e["label"] != "right"]
    assert A.matched_protocol_weights(parts) != A.direct_weights(model)
    assert "right" not in A.matched_protocol_weights(parts)


def test_raw_protocol_equality_survives_a_further_private_competing_context():
    model = active((1, 2))
    direct = as_component(A.direct_weights(model), 8)
    parts = A.compile_protocol(model)
    compiled = OLD.compose(OLD.compose(parts[0], parts[1]), parts[2])
    partner = OLD.component(1, [OLD.event(label, 0, 0) for label in A.CHANNELS] + [OLD.event("private-clock", 0, 0)], A.CHANNELS)
    assert OLD.labelled_weights(OLD.compose(direct, partner)) == OLD.labelled_weights(OLD.compose(compiled, partner))
    assert OLD.kernel(OLD.compose(direct, partner)) == OLD.kernel(OLD.compose(compiled, partner))


def test_fully_active_actor_view_requires_all_eight_current_states():
    model = active()
    matrix = A.normalise(A.direct_weights(model), 8)
    brute = A.exhaustive_refinements(matrix, 4)
    assert A.active_mask(model) == 15
    assert brute["minimal_masks"] == [15] and brute["exact_mask_count"] == 1
    assert A.refinement_labels(4, 15) == list(range(8))
    # A constant quotient is exact too, but does not retain actor configuration.
    assert A.block_report(matrix, [0] * 8)["exact"]


def test_inactive_actor_pair_can_forget_the_mode_in_the_coarsest_refinement():
    model = A.network([[0, 1], [0, 0]], [[0, 1], [0, 0]])
    matrix = A.normalise(A.direct_weights(model), 8)
    labels = A.refinement_labels(4, A.active_mask(model))
    assert labels == [0, 1, 2, 3, 4, 5, 6, 6]
    assert A.block_report(matrix, labels)["exact"]
    assert A.exhaustive_refinements(matrix, 4)["minimal_masks"] == [7]
    assert not A.block_report(matrix, A.refinement_labels(4, 6))["exact"]


def test_link_can_keep_changing_with_no_effect_on_the_actor_only_prediction():
    model = A.network([[0, 0], [0, 0]], [[0, 0], [0, 0]], (1, 2))
    matrix = A.normalise(A.direct_weights(model), 8)
    assert matrix[0][1] == matrix[1][0] == 1
    report = A.block_report(matrix, [i // 2 for i in range(8)])
    assert report["rows"] == [[int(s == t) for t in range(4)] for s in range(4)]
    brute = A.exhaustive_refinements(matrix, 4)
    assert brute["minimal_masks"] == [0] and brute["exact_mask_count"] == 16


@pytest.mark.parametrize("switch", [(0, 0), (1, 0), (0, 2), (1, 2)])
def test_refinement_criterion_does_not_require_a_positive_switch_rate(switch):
    model = active(switch)
    assert A.exhaustive_refinements(A.normalise(A.direct_weights(model), 8), 4)["minimal_masks"] == [15]


def test_no_phantom_global_event_comes_from_passive_components_or_halt():
    model = A.network([[0, 0], [0, 0]], [[0, 0], [0, 0]], (0, 0))
    assert A.direct_weights(model) == A.matched_protocol_weights(A.compile_protocol(model)) == {}
    assert A.normalise({}, 8) == [[int(s == t) for t in range(8)] for s in range(8)]


def test_state_only_minimality_does_not_claim_safety_for_every_later_context():
    null = A.network([[0, 0], [0, 0]], [[0, 0], [0, 0]], (1, 2))
    original = as_component(A.direct_weights(null), 8)
    partner = OLD.component(2, [OLD.event("switch", 0, 1), OLD.event("switch", 1, 0),
                                OLD.event("clock", 0, 0), OLD.event("clock", 1, 1)], A.CHANNELS)
    combined = OLD.compose(original, partner)
    labels = OLD.product_observation([state // 2 for state in range(8)], [0, 1])
    report = OLD.observed_kernel(combined, labels)
    assert not report["exact"] and report["rows"] is None
    assert report["witness"]["first_row"][1] == Fraction(1, 2)
    assert report["witness"]["second_row"][1] == Fraction(2, 3)


def test_positive_switching_support_contains_a_directed_five_cycle():
    model = A.network([[0, 2], [1, 0]], [[0, 1], [2, 0]], (2, 1))
    matrix = A.normalise(A.direct_weights(model), 8)
    cycle = [0, 4, 6, 7, 1, 0]
    assert len(set(cycle[:-1])) == 5
    assert all(matrix[s][t] > 0 for s, t in zip(cycle, cycle[1:]))
    assert not A.bipartite_support(matrix)


def test_each_frozen_mode_admits_its_declared_one_bit_support_encoding():
    model = active((0, 0))
    controls = A.frozen_binary_controls(model)
    assert [r["encoded_actor_states"] for r in controls] == [[0, 1, 2, 3], [0, 1, 3, 2]]
    assert A.bipartite_support(A.normalise(A.direct_weights(model), 8))


def test_a_single_state_actor_is_a_valid_null_with_a_distinct_link_policy():
    model = A.network([[0]], [[0, 1], [1, 0]])
    weights = A.direct_weights(model)
    assert "left" not in weights and "joint" not in weights
    assert weights == A.matched_protocol_weights(A.compile_protocol(model))
    assert A.exhaustive_refinements(A.normalise(weights, 4), 2)["minimal_masks"] == [3]


def test_nonbinary_actors_and_invalid_input_boundaries():
    model = A.network([[0, 1, 0], [0, 0, 2], [1, 0, 0]], [[0, 2], [1, 0]], (1, 2))
    assert A.exhaustive_refinements(A.normalise(A.direct_weights(model), 12), 6)["minimal_masks"] == [63]
    for matrix in ([[1, 0], [0, 0]], [[0, -1], [1, 0]], [[0, True], [1, 0]], [[0, Fraction(1, 2)], [1, 0]], [[0], [1, 0]], []):
        with pytest.raises(ValueError):
            A.network(matrix, [[0]])
    for switch in ((1,), (1, -1), (True, 1)):
        with pytest.raises(ValueError, match="switch"):
            active(switch)
    with pytest.raises(ValueError, match="observation"):
        A.block_report([[Fraction(1)]], [False])
    with pytest.raises(ValueError, match="refinement"):
        A.refinement_labels(4, 16)


def test_predeclared_compiler_and_all_refinements_agree():
    result = A.run_checks()
    assert result["binary_networks"] == result["raw_compiler_checks"] == 729
    assert result["refinement_checks"] == 11664
    assert result["exact_refinement_masks"] == 1224
    assert result["actor_only_exact_cases"] == 9
    assert result["coarsest_block_count_histogram"] == {4: 9, 6: 72, 7: 144, 8: 504}
    assert result["scientific_worker_invocations"] == result["new_atlas_cells"] == 0
    assert result["status"] == "verified"
