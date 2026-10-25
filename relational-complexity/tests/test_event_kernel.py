"""Fixtures for a declared event catalogue. They do not run an atlas round."""

from __future__ import annotations

from fractions import Fraction

import pytest

from rrc import ENGINE_VERSION
from rrc.event_kernel import kernel, single_toggle_catalogue
from rrc.state_families import single_toggle_successors

ROOT_NOTE = "docs/event-kernel.md"


def _note(root):
    return (root / ROOT_NOTE).read_text(encoding="utf-8")


def test_rows_sum_to_one_and_duplicate_targets_add():
    events = [
        {"name": "a", "kind": "toggle", "source": 0, "target": 1, "weight": 1},
        {"name": "b", "kind": "toggle", "source": 0, "target": 1, "weight": 3},
        {"name": "c", "kind": "toggle", "source": 0, "target": 2, "weight": 2},
    ]
    forward = kernel(3, events)
    backward = kernel(3, list(reversed(events)))
    assert forward["probabilities"] == backward["probabilities"]
    assert forward["aggregated_weights"] == backward["aggregated_weights"]
    assert forward["completions"] == backward["completions"]
    assert forward["aggregated_weights"][0] == [0, 4, 2]
    assert forward["probabilities"][0] == [Fraction(0), Fraction(2, 3), Fraction(1, 3)]
    assert forward["completions"][0] == "normalised_events"
    assert forward["completions"][1] == "halt_self_loop"
    assert forward["enabled_event_counts"][1] == 0
    for row in forward["probabilities"]:
        assert sum(row) == 1


def test_halt_self_loop_is_not_a_noop_event():
    halted = kernel(1, [])
    waiting = kernel(
        1,
        [{"name": "stay", "kind": "noop", "source": 0, "target": 0, "weight": 1}],
    )
    assert halted["probabilities"] == waiting["probabilities"] == [[Fraction(1)]]
    assert halted["completions"] == ["halt_self_loop"]
    assert waiting["completions"] == ["noop_event"]
    assert halted["halt_self_loop_is_event"] is False
    assert halted["enabled_event_counts"] == [0]
    assert waiting["enabled_event_counts"] == [1]
    mixed = kernel(
        2,
        [
            {"name": "stay", "kind": "noop", "source": 0, "target": 0, "weight": 1},
            {"name": "go", "kind": "toggle", "source": 0, "target": 1, "weight": 1},
        ],
    )
    assert mixed["probabilities"][0] == [Fraction(1, 2), Fraction(1, 2)]
    assert mixed["completions"][0] == "normalised_events_including_noop"
    silent = kernel(
        1,
        [{"name": "idle", "kind": "noop", "source": 0, "target": 0, "weight": 0}],
    )
    assert silent["completions"] == ["halt_self_loop"]
    assert silent["enabled_event_counts"] == [0]


def test_invalid_events_are_rejected():
    with pytest.raises(ValueError, match="nonnegative integer"):
        kernel(2, [{"name": "bad", "kind": "toggle", "source": 0, "target": 1, "weight": -1}])
    with pytest.raises(ValueError, match="nonnegative integer"):
        kernel(2, [{"name": "bad", "kind": "toggle", "source": 0, "target": 1, "weight": True}])
    with pytest.raises(ValueError, match="integer state"):
        kernel(2, [{"name": "bad", "kind": "toggle", "source": 0, "target": 2, "weight": 1}])
    with pytest.raises(ValueError, match="changes the state"):
        kernel(2, [{"name": "bad", "kind": "toggle", "source": 0, "target": 0, "weight": 1}])
    with pytest.raises(ValueError, match="stays in its source"):
        kernel(2, [{"name": "bad", "kind": "noop", "source": 0, "target": 1, "weight": 1}])
    with pytest.raises(ValueError, match="duplicate event name"):
        kernel(
            2,
            [
                {"name": "same", "kind": "toggle", "source": 0, "target": 1, "weight": 1},
                {"name": "same", "kind": "toggle", "source": 1, "target": 0, "weight": 1},
            ],
        )
    with pytest.raises(ValueError, match="positive integer"):
        kernel(True, [])
    with pytest.raises(ValueError, match="at most 16"):
        kernel(17, [])


def test_single_toggle_embedding_matches_hand_enumeration():
    rows = [(1, 1), (0, 0), (3, 1), (1, 1)]
    report = kernel(4, single_toggle_catalogue(rows))
    assert report["method"] == "event-kernel-0.1.0"
    assert report["clock"] == "one_declared_event"
    for state, row in enumerate(rows):
        total = sum(row)
        if total == 0:
            assert report["completions"][state] == "halt_self_loop"
            assert report["probabilities"][state][state] == 1
            continue
        assert report["completions"][state] == "normalised_events"
        for bit, weight in enumerate(row):
            target = state ^ (1 << bit)
            assert report["probabilities"][state][target] == Fraction(weight, total)
            if weight:
                assert target in single_toggle_successors(2, state)
    assert report["probabilities"][0] == [Fraction(0), Fraction(1, 2), Fraction(1, 2), Fraction(0)]
    assert report["probabilities"][2][3] == Fraction(3, 4)
    assert report["probabilities"][2][0] == Fraction(1, 4)


def test_joint_event_changes_one_step_support():
    events = []
    for state in range(4):
        events.append(
            {
                "name": f"bit0-{state}",
                "kind": "toggle",
                "source": state,
                "target": state ^ 1,
                "weight": 1,
            }
        )
        events.append(
            {
                "name": f"both-{state}",
                "kind": "joint",
                "source": state,
                "target": state ^ 3,
                "weight": 1,
            }
        )
    joint = kernel(4, events)
    ordinary = kernel(4, single_toggle_catalogue([(1, 1), (1, 1), (1, 1), (1, 1)]))
    assert ordinary["probabilities"][0][3] == 0
    assert joint["probabilities"][0] == [Fraction(0), Fraction(1, 2), Fraction(0), Fraction(1, 2)]
    assert (0 ^ 3).bit_count() == 2
    assert 3 not in single_toggle_successors(2, 0)
    assert 3 in single_toggle_successors(2, 1)
    for row in joint["probabilities"]:
        assert sum(row) == 1


def test_identified_toggle_matches_coupled_copies_and_not_the_free_product():
    identified = kernel(
        2,
        [
            {"name": "up", "kind": "toggle", "source": 0, "target": 1, "weight": 1},
            {"name": "down", "kind": "toggle", "source": 1, "target": 0, "weight": 1},
        ],
    )
    coupled = kernel(
        4,
        [
            {"name": "together-up", "kind": "joint", "source": 0, "target": 3, "weight": 1},
            {"name": "together-down", "kind": "joint", "source": 3, "target": 0, "weight": 1},
        ],
    )
    free = kernel(4, single_toggle_catalogue([(1, 1), (1, 1), (1, 1), (1, 1)]))
    image = {0: 0, 1: 3}
    assert identified["probabilities"][0][1] == 1
    assert coupled["probabilities"][image[0]][image[1]] == 1
    assert coupled["probabilities"][image[1]][image[0]] == 1
    assert (0 ^ 1).bit_count() == 1
    assert (0 ^ 3).bit_count() == 2
    assert free["probabilities"][0][1] == Fraction(1, 2)
    assert free["probabilities"][0][2] == Fraction(1, 2)
    assert free["probabilities"][0][3] == 0
    agreement = {0, 3}
    assert 1 not in agreement and 2 not in agreement


def test_event_kernel_note_is_not_a_frozen_round():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    note = _note(root)
    for phrase in (
        "not a frozen round",
        "rrc-0.4.0",
        "event-kernel-0.1.0",
        "not a new primitive",
        "No intervention operator is defined",
        "halt_self_loop",
        "noop_event",
        "2/3",
        "1/3",
        "1/2",
        "Hamming distance is 2",
        "EQ-027",
        "ATLAS-Q15 stays open",
        "No universal impossibility is claimed",
    ):
        assert phrase in note
    source = (root / "src" / "rrc" / "event_kernel.py").read_text(encoding="utf-8")
    assert "compile_weight_table" not in source
    assert "ENGINE_VERSION" not in source
    assert ENGINE_VERSION == "rrc-0.4.0"
