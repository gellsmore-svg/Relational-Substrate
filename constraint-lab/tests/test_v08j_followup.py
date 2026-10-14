"""Synthetic-only J1 plumbing until its independent projection freeze."""

from fractions import Fraction
from pathlib import Path

import pytest

from rs_constraint_lab.durable import read_json
from rs_constraint_lab.gen008j_followup import (
    ITEMS, SUMMARY, class_pair_probe, edge_role_probe, partition_labels,
    reconstruction_record, same_edge_formula,
)
from rs_constraint_lab.history_roles import RoleController

ROOT = Path(__file__).resolve().parents[2]
PUBLISHED = pytest.mark.skipif(not (ROOT / SUMMARY).exists(), reason="J1 target checks stay unopened until independent freeze/publication")


def test_reconstruction_detects_collisions_and_nonconstant_fibres():
    record = reconstruction_record(((0,), (1,)), (("a", "b"), ("b", "a")))
    assert record["bijection"]
    assert not reconstruction_record(((0,), (1,)), (("a", "b"), ("a", "b")))["bijection"]
    assert not reconstruction_record(((0, 1),), (("a", "b"), ("b", "a")))["constant_on_orbits"]


def test_synthetic_partition_does_not_drop_states():
    keys, groups, group_of = partition_labels(((1, 0), (0, 1), (1, 0)))
    assert keys == ((0, 1), (1, 0))
    assert groups == ((1,), (0, 2)) and group_of == (1, 0, 1)


def test_three_slot_synthetic_SAME_count_formula():
    for feature in ("SAME_ANY", "SAME_FORM", "SAME_DISSOLVE"):
        model = RoleController(feature, Fraction(2), 3)
        for p in range(8):
            for h in range(3):
                actual = {}
                for event, mass in enumerate(model.pair_probabilities(p, h)):
                    target = p ^ (1 << event)
                    role = target.bit_count(), (target >> event) & 1
                    actual[role] = actual.get(role, Fraction(0)) + mass
                assert actual == same_edge_formula(feature, Fraction(2), p.bit_count(), (p >> h) & 1, 3)


@PUBLISHED
def test_published_class_reconstruction_and_all_system_triples():
    result = class_pair_probe(ROOT)
    assert result["bijection"] and result["class_pair_count"] == 28
    assert not result["collisions"] and len(result["systems"]) == 23
    assert sum(row["projected_class_order"] == 2 for row in result["systems"]) == 18
    assert all(row["triple_conditional_gap"] == 0 for row in result["systems"])


@PUBLISHED
def test_published_SAME_edge_role_closure_and_boundaries():
    result = edge_role_probe(ROOT)
    assert result["edge_role_count"] == 12 and len(result["systems"]) == 23
    assert sum(row["strongly_lumpable"] for row in result["systems"]) == 11
    assert sum("formula_gap" in row for row in result["systems"]) == 7
    assert all(row.get("formula_gap", 0) == row.get("J0_word_gap", 0) == 0 for row in result["systems"])
