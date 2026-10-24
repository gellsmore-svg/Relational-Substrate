"""Effective cardinality of one uniform ge-2 multiply.

This is a compiler identity. It does not run a new scientific round.
"""

from __future__ import annotations

import numpy as np

from rrc.constraints import compile_model, compile_weight_table, reduce_weight_table


CHAIN = [(0, 1), (1, 2), (2, 3)]
BRANCH = [(0, 1), (0, 2), (0, 3)]
PATH5 = [(0, 1), (1, 2), (2, 3), (3, 4)]
CYCLE4 = [(0, 1), (1, 2), (2, 3), (0, 3)]
CYCLE5 = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)]
TRIANGLE = [(0, 1), (1, 2), (0, 2)]
STAR4 = [(0, 1), (0, 2), (0, 3), (0, 4)]
DISJOINT = [(0, 1), (2, 3)]
ADJACENT = [(0, 1), (1, 2)]
ONE = [(0, 1)]


def neighbourhood_sizes(edges):
    sizes = []
    for index, edge in enumerate(edges):
        nodes = set(edge)
        sizes.append(sum(1 for other, pair in enumerate(edges) if other != index and nodes & set(pair)))
    return sizes


def wide_count(edges):
    return sum(1 for size in neighbourhood_sizes(edges) if size >= 2)


def uniform(edges, relation="ge", threshold=2, factor=3, action="either"):
    return [
        {
            "action": action,
            "effect": "multiply",
            "factor": factor,
            "event": [edge[0], edge[1]],
            "when": {"kind": "incident_count", "relation": relation, "threshold": threshold},
        }
        for edge in edges
    ]


def listed(edges):
    return {"kind": "listed", "edges": [list(edge) for edge in edges]}


def book_of(n, edges, constraints, baseline=1):
    model = compile_model(n, listed(edges), constraints, baseline)
    return model["bookkeeping"]


def _assert_weight_side(book, expected):
    assert book["effective_cardinality"] == expected
    assert book["removal_sensitive_count"] == expected
    assert book["kernel_removal_sensitive_count"] == expected


def test_effective_cardinality_equals_the_wide_edge_count():
    cases = (
        (4, CHAIN, 1),
        (4, BRANCH, 3),
        (5, PATH5, 2),
        (4, CYCLE4, 4),
        (5, CYCLE5, 5),
        (3, TRIANGLE, 3),
        (5, STAR4, 4),
        (4, DISJOINT, 0),
        (3, ADJACENT, 0),
        (2, ONE, 0),
    )
    for n, edges, expected in cases:
        assert wide_count(edges) == expected
        for action in ("either", "form"):
            book = book_of(n, edges, uniform(edges, action=action))
            _assert_weight_side(book, expected)
            assert book["kernel_effective_cardinality"] == expected
        dissolved = book_of(n, edges, uniform(edges, action="dissolve"))
        _assert_weight_side(dissolved, expected)
        if edges in (TRIANGLE, BRANCH):
            assert dissolved["kernel_effective_cardinality"] == 0
        else:
            assert dissolved["kernel_effective_cardinality"] == expected
    scaled = book_of(3, TRIANGLE, uniform(TRIANGLE, factor=4), baseline=2)
    assert scaled["effective_cardinality"] == 3
    assert scaled["kernel_effective_cardinality"] == 3


def test_dissolve_on_the_triangle_matches_the_baseline_kernel_only():
    full = compile_weight_table(3, listed(TRIANGLE), uniform(TRIANGLE, action="dissolve"))
    baseline = compile_weight_table(3, listed(TRIANGLE), [])
    assert not np.array_equal(full, baseline)
    assert np.array_equal(reduce_weight_table(full), baseline)
    star = compile_weight_table(4, listed(BRANCH), uniform(BRANCH, action="dissolve"))
    star_base = compile_weight_table(4, listed(BRANCH), [])
    assert not np.array_equal(star, star_base)
    assert np.array_equal(reduce_weight_table(star), star_base)


def test_a_narrow_constraint_leaves_the_baseline_column():
    weights = compile_weight_table(4, listed(DISJOINT), uniform(DISJOINT))
    baseline = compile_weight_table(4, listed(DISJOINT), [])
    assert np.array_equal(weights, baseline)
    chain = compile_weight_table(4, listed(CHAIN), uniform(CHAIN))
    ends_only = compile_weight_table(4, listed(CHAIN), [uniform(CHAIN)[0], uniform(CHAIN)[2]])
    middle_only = compile_weight_table(4, listed(CHAIN), [uniform(CHAIN)[1]])
    assert np.array_equal(chain, middle_only)
    assert not np.array_equal(chain, ends_only)


def test_a_duplicate_multiply_raises_the_count():
    rows = uniform(TRIANGLE)
    rows.append(dict(rows[0]))
    book = book_of(3, TRIANGLE, rows)
    assert wide_count(TRIANGLE) == 3
    assert book["declared_cardinality"] == 4
    assert book["effective_cardinality"] == 4
    assert book["kernel_effective_cardinality"] == 4
    assert book["removal_sensitive_count"] == 4
    assert book["kernel_removal_sensitive_count"] == 4


def test_a_prohibit_on_the_same_guard_makes_the_multiply_redundant():
    rows = uniform(TRIANGLE)
    rows.append(
        {
            "action": "either",
            "effect": "prohibit",
            "event": [0, 1],
            "when": {"kind": "incident_count", "relation": "ge", "threshold": 2},
        }
    )
    book = book_of(3, TRIANGLE, rows)
    assert book["declared_cardinality"] == 4
    assert book["effective_cardinality"] == 3
    assert book["kernel_effective_cardinality"] == 3
    without_multiply = [rows[1], rows[2], rows[3]]
    full = compile_weight_table(3, listed(TRIANGLE), rows)
    reduced = compile_weight_table(3, listed(TRIANGLE), without_multiply)
    assert np.array_equal(full, reduced)
    assert book["removal_sensitive_count"] == 3


def test_eq_1_on_the_chain_is_not_this_count():
    book = book_of(4, CHAIN, uniform(CHAIN, relation="eq", threshold=1))
    assert wide_count(CHAIN) == 1
    assert book["effective_cardinality"] != 1
