"""Line-graph total domination for one incident-prohibit template.

This is a compiler identity. It does not run a new scientific round.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from rrc.constraints import compile_weight_table
from rrc.model import recurrent_class_count

ROOT = Path(__file__).resolve().parents[1]

CHAIN = [(0, 1), (1, 2), (2, 3)]
BRANCH = [(0, 1), (0, 2), (0, 3)]
CYCLE = [(0, 1), (1, 2), (2, 3), (0, 3)]
DISJOINT = [(0, 1), (2, 3)]
ADJACENT = [(0, 1), (1, 2)]
TRIANGLE = [(0, 1), (1, 2), (0, 2)]


def line_adjacency(edges):
    adjacency = [[] for _ in edges]
    for left, edge in enumerate(edges):
        nodes = set(edge)
        for right in range(left + 1, len(edges)):
            if nodes & set(edges[right]):
                adjacency[left].append(right)
                adjacency[right].append(left)
    return adjacency


def total_dominating_states(edges):
    """Masks whose present edges are a total dominating set of the line graph.

    Every line-graph vertex, including members of the set, needs a neighbour
    in the set. An isolated line-graph vertex makes the collection empty.
    """
    adjacency = line_adjacency(edges)
    found = []
    for mask in range(1 << len(edges)):
        dominated = True
        for vertex, neighbours in enumerate(adjacency):
            if not any((mask >> neighbour) & 1 for neighbour in neighbours):
                dominated = False
                break
        if dominated:
            found.append(mask)
    return found


def uniform(edges, effect="prohibit", polarity="present", action="either"):
    rows = []
    for edge in edges:
        row = {
            "action": action,
            "effect": effect,
            "event": [edge[0], edge[1]],
            "when": {"kind": "incident_neighbour", "polarity": polarity},
        }
        if effect == "multiply":
            row["factor"] = 3
        rows.append(row)
    return rows


def deadlock_states(weights):
    return [state for state in range(weights.shape[0]) if not np.any(weights[state])]


def listed(n, edges, constraints):
    return compile_weight_table(n, {"kind": "listed", "edges": [list(edge) for edge in edges]}, constraints)


def test_deadlocks_are_the_total_dominating_sets():
    cases = (
        (4, CHAIN, (0b011, 0b110, 0b111)),
        (4, BRANCH, (0b011, 0b101, 0b110, 0b111)),
        (4, CYCLE, None),
        (4, DISJOINT, ()),
        (3, ADJACENT, (0b11,)),
        (3, TRIANGLE, (0b011, 0b101, 0b110, 0b111)),
    )
    for n, edges, hand in cases:
        weights = listed(n, edges, uniform(edges))
        deadlocks = deadlock_states(weights)
        dominating = total_dominating_states(edges)
        assert deadlocks == dominating
        if hand is not None:
            assert tuple(deadlocks) == hand
    assert len(total_dominating_states(CYCLE)) == 9
    chain = listed(4, CHAIN, uniform(CHAIN))
    classes = recurrent_class_count(chain)
    assert classes["deadlock_states"] == 3
    assert classes["recurrent_classes"] > classes["deadlock_states"]


def test_a_triangle_and_a_three_star_have_the_same_prohibit_table():
    triangle = listed(3, TRIANGLE, uniform(TRIANGLE))
    star = listed(4, BRANCH, uniform(BRANCH))
    assert np.array_equal(triangle, star)


def test_the_identity_fails_when_the_template_changes():
    full = total_dominating_states(CHAIN)
    assert full
    missing = uniform(CHAIN)[:-1]
    assert deadlock_states(listed(4, CHAIN, missing)) == []
    multiplied = listed(4, CHAIN, uniform(CHAIN, effect="multiply"))
    assert deadlock_states(multiplied) == []
    absent = listed(4, CHAIN, uniform(CHAIN, polarity="absent"))
    assert deadlock_states(absent) != full
    formed = listed(4, CHAIN, uniform(CHAIN, action="form"))
    assert deadlock_states(formed) != full


def test_atlas_004_deadlock_counts_match_the_enumerator():
    stored = {
        "A4-chain-inc-pro": CHAIN,
        "A4-branch-inc-pro": BRANCH,
        "A4-cycle-inc-pro": CYCLE,
        "A4-disconnected-inc-pro": DISJOINT,
    }
    for item_id, edges in stored.items():
        result = json.loads((ROOT / "results" / "atlas-004" / "items" / item_id / "result.json").read_text())
        assert result["classes"]["deadlock_states"] == len(total_dominating_states(edges))
