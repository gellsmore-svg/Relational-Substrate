"""Kernel fingerprints and the incident-neighbour predicate.

These are compiler checks. They do not run a frozen atlas round.
"""

from __future__ import annotations

import numpy as np
import pytest

from rrc.constraints import (
    compile_model,
    compile_weight_table,
    kernel_fingerprint,
    kernels_equal,
    present_component_count,
    present_graph,
    reduce_weight_table,
    weight_table_hash,
)
from rrc.items import execute_atlas_core


BUDGET = {
    "tolerance": 1e-12,
    "cross_tolerance": 1e-8,
    "max_iter": 10000,
    "dense_max_states": 1024,
}


def _spec(**overrides):
    payload = {
        "id": "fixture",
        "round_id": "fixture",
        "type": "atlas_core",
        "n": 3,
        "carrier": {"kind": "complete"},
        "constraints": [],
        "baseline": 1,
        "role": "fixture",
    }
    payload.update(BUDGET)
    payload.update(overrides)
    return payload


def _multiply(event, condition, factor=4):
    return {
        "effect": "multiply",
        "factor": factor,
        "action": "either",
        "event": [event[0], event[1]],
        "when": {"edge": [condition[0], condition[1]], "polarity": "present"},
    }


def _prohibit(event, condition, polarity="present"):
    return {
        "effect": "prohibit",
        "action": "either",
        "event": [event[0], event[1]],
        "when": {"edge": [condition[0], condition[1]], "polarity": polarity},
    }


def _incident(event, effect="multiply", factor=3, polarity="present", action="either"):
    payload = {
        "effect": effect,
        "action": action,
        "event": [event[0], event[1]],
        "when": {"kind": "incident_neighbour", "polarity": polarity},
    }
    if effect == "multiply":
        payload["factor"] = factor
    return payload


def test_row_gcd_reduces_positive_rows_and_keeps_zero_rows():
    table = np.array([[4, 8, 4], [0, 0, 0], [0, 2, 4], [7, 0, 0]], dtype=np.int64)
    reduced = reduce_weight_table(table)
    assert reduced.tolist() == [[1, 2, 1], [0, 0, 0], [0, 1, 2], [1, 0, 0]]
    scaled = np.array([[2, 4, 2], [0, 0, 0], [0, 4, 8], [21, 0, 0]], dtype=np.int64)
    assert kernels_equal(table, scaled)
    assert weight_table_hash(table) != weight_table_hash(scaled)
    assert kernel_fingerprint(table) == kernel_fingerprint(scaled)
    halt = np.zeros((2, 2), dtype=np.int64)
    other = np.array([[0, 0], [1, 0]], dtype=np.int64)
    assert kernels_equal(halt, np.zeros_like(halt))
    assert not kernels_equal(halt, other)
    assert not kernels_equal(table, scaled[:, :2])
    with pytest.raises(ValueError):
        reduce_weight_table(np.array([[-1, 2]], dtype=np.int64))


def test_a_larger_baseline_changes_the_table_and_not_the_kernel():
    ones = compile_weight_table(3, {"kind": "complete"}, [], baseline=1)
    twos = compile_weight_table(3, {"kind": "complete"}, [], baseline=2)
    assert not np.array_equal(ones, twos)
    assert kernels_equal(ones, twos)
    assert np.array_equal(reduce_weight_table(twos), np.ones_like(twos))


def test_a_multiply_can_change_raw_weights_and_leave_the_kernel():
    """Once the other column is identically zero, scaling the live column is a row scale."""
    carrier = {"kind": "listed", "edges": [[0, 1], [1, 2]]}
    prohibits = [
        _prohibit((1, 2), (0, 1), "present"),
        _prohibit((1, 2), (0, 1), "absent"),
    ]
    scaled = prohibits + [_multiply((0, 1), (1, 2), factor=4)]
    plain = compile_weight_table(3, carrier, prohibits)
    rich = compile_weight_table(3, carrier, scaled)
    assert not np.array_equal(plain, rich)
    assert kernels_equal(plain, rich)
    assert np.all(rich[:, 1] == 0)
    assert set(int(value) for value in rich[:, 0]) == {1, 4}
    book = compile_model(3, carrier, scaled)["bookkeeping"]
    assert book["declared_cardinality"] == 3
    assert book["effective_cardinality"] == 3
    assert book["removal_sensitive_count"] == 3
    assert book["kernel_effective_cardinality"] == 2
    assert book["kernel_removal_sensitive_count"] == 2


def test_incident_neighbour_matches_a_designated_bit_only_when_the_neighbourhood_is_that_bit():
    chain = {"kind": "listed", "edges": [[0, 1], [1, 2], [2, 3]]}
    branch = {"kind": "listed", "edges": [[0, 1], [0, 2], [0, 3]]}
    designated = [_multiply((0, 1), (1, 2), factor=3)]
    # On the chain the only edge incident to (0,1) is (1,2).
    chain_designated = compile_weight_table(4, chain, designated)
    chain_incident = compile_weight_table(4, chain, [_incident((0, 1), factor=3)])
    assert np.array_equal(chain_designated, chain_incident)
    # On the branch, (0,1) is incident to both other edges. State bit 2 is not bit 1.
    branch_designated = compile_weight_table(4, branch, [_multiply((0, 1), (0, 2), factor=3)])
    branch_incident = compile_weight_table(4, branch, [_incident((0, 1), factor=3)])
    assert not np.array_equal(branch_designated, branch_incident)
    only_far = 0b100
    assert int(branch_incident[only_far, 0]) == 3
    assert int(branch_designated[only_far, 0]) == 1
    disconnected = {"kind": "listed", "edges": [[0, 1], [2, 3]]}
    alone = compile_weight_table(4, disconnected, [_incident((0, 1), factor=3)])
    assert np.all(alone == 1)


def test_a_uniform_incident_template_is_covariant_under_path_reversal():
    chain = [(0, 1), (1, 2), (2, 3)]
    image = [(2, 3), (1, 2), (0, 1)]

    def template(edges):
        return [_incident(edge, factor=3) for edge in edges]

    left = compile_weight_table(4, {"kind": "listed", "edges": [list(edge) for edge in chain]}, template(chain))
    right = compile_weight_table(4, {"kind": "listed", "edges": [list(edge) for edge in image]}, template(image))
    assert np.array_equal(left, right)
    end = compile_weight_table(4, {"kind": "listed", "edges": [list(edge) for edge in chain]}, [_incident((0, 1))])
    middle = compile_weight_table(4, {"kind": "listed", "edges": [list(edge) for edge in chain]}, [_incident((1, 2))])
    assert not np.array_equal(end, middle)


def test_incident_expansion_is_not_declared_j():
    branch = {"kind": "listed", "edges": [[0, 1], [0, 2], [0, 3]]}
    model = compile_model(4, branch, [_incident((0, 1), factor=3)])
    book = model["bookkeeping"]
    assert book["j_positive"] == 1
    assert book["declared_cardinality"] == 1
    assert book["max_positive_k"] == 0
    assert book["max_incident_edges"] == 2
    assert book["expansion_j_total"] == 3
    assert book["max_expansion_k"] == 3
    feature = book["features"][0]
    assert "exact minterms" in feature["expansion_note"]
    assert "CL-T12" in feature["expansion_note"]
    assert model["grammar_id"] == "incident-neighbour-v1"
    absent = compile_model(4, branch, [_incident((0, 1), polarity="absent")])
    assert absent["bookkeeping"]["expansion_j_total"] == 1
    assert absent["bookkeeping"]["max_expansion_k"] == 3
    mutual = compile_model(
        4,
        {"kind": "listed", "edges": [[0, 1], [1, 2]]},
        [_incident((0, 1)), _incident((1, 2))],
    )
    assert mutual["imposed_rule_dependency"]["has_cycle"] is True
    assert "not an observed dynamical cascade" in mutual["imposed_rule_dependency"]["note"]


def test_forest_states_obey_the_component_identity_and_a_cycle_does_not():
    chain = [(0, 1), (1, 2), (2, 3)]
    for state in range(8):
        graph = present_graph(4, chain, state)
        assert graph["has_cycle"] is False
        assert graph["components"] == 4 - graph["present_edges"]
        assert graph["components"] == present_component_count(4, chain, state)
    cycle = [(0, 1), (1, 2), (2, 3), (0, 3)]
    full = present_graph(4, cycle, 0b1111)
    assert full["has_cycle"] is True
    assert full["components"] != 4 - full["present_edges"]
    chain_hash_carrier = {"kind": "listed", "edges": [[0, 1], [1, 2], [2, 3]]}
    branch_carrier = {"kind": "listed", "edges": [[0, 1], [0, 2], [0, 3]]}
    assert compile_model(4, chain_hash_carrier, [])["structure_sha256"] != compile_model(4, branch_carrier, [])[
        "structure_sha256"
    ]


def test_opening_cells_still_report_the_opening_grammar_and_store_the_table():
    result = execute_atlas_core(_spec(constraints=[_multiply((0, 1), (0, 2), factor=2)]))
    assert result["status"] == "complete"
    assert result["grammar_id"] == "opening-prohibit-multiply-v1"
    assert result["kernel_method"] == "row_gcd_halt_self_loop"
    assert result["compilation"]["new_primitive"] is False
    weights = np.asarray(result["weights"], dtype=np.int64)
    assert weights.shape == (8, 3)
    assert weight_table_hash(weights) == result["weight_sha256"]
    assert kernel_fingerprint(weights) == result["kernel_sha256"]
    assert result["bookkeeping"]["max_positive_k"] == 2
    with pytest.raises(ValueError):
        compile_weight_table(3, {"kind": "complete"}, [_incident((0, 1)) | {"when": {"kind": "incident_neighbour", "polarity": "present", "edge": [0, 2]}}])


def test_two_incident_multiplies_reinforce():
    carrier = {"kind": "listed", "edges": [[0, 1], [1, 2]]}
    weights = compile_weight_table(3, carrier, [_incident((0, 1), factor=3), _incident((0, 1), factor=3)])
    # The neighbour of (0,1) is (1,2), bit 1. Both copies match together.
    assert int(weights[0b10, 0]) == 9
    assert int(weights[0b00, 0]) == 1
