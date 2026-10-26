"""Derived counts and one coupled activity bit. Not a frozen round."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from rrc.constraints import compile_weight_table
from rrc.coordinate_examples import activity_weight_rows, derived_pair_count

ROOT = Path(__file__).resolve().parents[1]
CHAIN = [[0, 1], [1, 2], [2, 3]]
# Hand rows. Column order is pair0, pair1, activity.
HAND = [
    [1, 1, 0],
    [1, 1, 1],
    [1, 1, 0],
    [1, 1, 1],
    [3, 1, 0],
    [3, 1, 1],
    [3, 1, 0],
    [3, 1, 1],
]


def _probability(rows, state, event):
    row = rows[state]
    total = sum(row)
    return Fraction(int(row[event]), int(total))


def test_derived_count_is_one_value_of_the_pair_mask():
    for mask in range(4):
        assert derived_pair_count(mask) == (mask & 1) + ((mask >> 1) & 1)
    assert derived_pair_count(1) == derived_pair_count(2) == 1
    # States 1 and 5 share the pair mask and differ in the activity bit.
    assert (1 & 3) == (5 & 3) == 1
    assert derived_pair_count(1 & 3) == derived_pair_count(5 & 3)
    assert ((1 >> 2) & 1) != ((5 >> 2) & 1)
    with pytest.raises(ValueError, match="0 .. 3"):
        derived_pair_count(4)
    with pytest.raises(ValueError, match="0 .. 3"):
        derived_pair_count(True)


def test_activity_rows_match_the_hand_table_and_the_compiled_chain():
    rows = activity_weight_rows()
    assert rows == HAND
    source = (ROOT / "src" / "rrc" / "coordinate_examples.py").read_text(encoding="utf-8")
    assert "compile_weight_table" not in source
    weights = compile_weight_table(
        4,
        {"kind": "listed", "edges": CHAIN},
        [
            {
                "effect": "multiply",
                "factor": 3,
                "action": "either",
                "event": [0, 1],
                "when": {"edge": [2, 3], "polarity": "present"},
            },
            {
                "effect": "prohibit",
                "action": "either",
                "event": [2, 3],
                "when": {"edge": [0, 1], "polarity": "absent"},
            },
        ],
    )
    assert weights.tolist() == HAND
    assert _probability(HAND, 1, 0) == Fraction(1, 3)
    assert _probability(HAND, 5, 0) == Fraction(3, 5)
    assert HAND[1] != HAND[5]
    # The empty list is a free third bit: the pair-toggle probability agrees.
    free = compile_weight_table(4, {"kind": "listed", "edges": CHAIN}, [])
    assert free.tolist() == [[1, 1, 1]] * 8
    assert _probability(free.tolist(), 1, 0) == _probability(free.tolist(), 5, 0) == Fraction(1, 3)
    # A joint flip of bit 0 and bit 2 is not a single-toggle successor.
    successors = {1 << bit for bit in range(3)}
    assert 5 not in successors
    assert (0 ^ 5).bit_count() == 2


def test_activity_equality_is_a_method_row_and_the_question_stays_open():
    equivalences = {
        json.loads(line)["equivalence_id"]: json.loads(line)
        for line in (ROOT / "atlas" / "equivalences.jsonl").read_text(encoding="utf-8").splitlines()
    }
    row = equivalences["EQ-027"]
    assert row["status"] == "method"
    assert row["equivalence_type"] == "weight_table"
    for phrase in ("higher-order", "two-edge", "History"):
        assert phrase in row["not_claimed"]
    ideas = {
        json.loads(line)["idea_id"]: json.loads(line)
        for line in (ROOT / "atlas" / "ideas.jsonl").read_text(encoding="utf-8").splitlines()
    }
    assert ideas["IDEA-L22"]["status"] == "partial"
    assert "not a frozen cell" in ideas["IDEA-L22"]["methods"]
    assert ideas["IDEA-L16"]["status"] == "partial"
    assert "src/rrc/composition.py" in ideas["IDEA-L16"]["methods"]
    assert "independent bit" in ideas["IDEA-L16"]["methods"]
    coverage = {
        json.loads(line)["coverage_id"]: json.loads(line)
        for line in (ROOT / "atlas" / "coverage.jsonl").read_text(encoding="utf-8").splitlines()
    }
    assert coverage["COV-HIGHER-ORDER-STATE"]["status"] == "open"
    questions = {
        json.loads(line)["question_id"]: json.loads(line)
        for line in (ROOT / "atlas" / "questions.jsonl").read_text(encoding="utf-8").splitlines()
    }
    assert questions["ATLAS-Q15"]["status"] == "open"
    assert "not a new primitive" in (ROOT / "docs" / "compilation-gate.md").read_text(encoding="utf-8")
