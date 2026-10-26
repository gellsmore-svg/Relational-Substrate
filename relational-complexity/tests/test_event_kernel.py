"""Fixtures for a declared event catalogue. They do not run an atlas round."""

from __future__ import annotations

from fractions import Fraction

import pytest

from rrc import ENGINE_VERSION
from rrc.event_kernel import kernel, single_toggle_catalogue, strict_kernel
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


def test_strict_kind_rejects_a_mislabeled_distance_and_keeps_the_old_method():
    mislabeled = {"name": "two", "kind": "toggle", "source": 0, "target": 3, "weight": 1}
    one_bit = {"name": "one", "kind": "joint", "source": 0, "target": 1, "weight": 1}
    loose = kernel(4, [mislabeled])
    assert loose["method"] == "event-kernel-0.1.0"
    assert loose["probabilities"][0][3] == 1
    assert kernel(4, [one_bit])["probabilities"][0][1] == 1
    with pytest.raises(ValueError, match="exactly one bit"):
        strict_kernel(4, [mislabeled], bit_width=2)
    with pytest.raises(ValueError, match="at least two bits"):
        strict_kernel(4, [one_bit], bit_width=2)
    with pytest.raises(ValueError, match="declared bit width"):
        strict_kernel(4, [mislabeled])
    with pytest.raises(ValueError, match="toggle, joint, or noop"):
        kernel(4, [{"name": "move", "kind": "transition", "source": 0, "target": 3, "weight": 1}])
    silent = {"name": "quiet", "kind": "toggle", "source": 0, "target": 3, "weight": 0}
    assert kernel(4, [silent])["completions"] == [
        "halt_self_loop",
        "halt_self_loop",
        "halt_self_loop",
        "halt_self_loop",
    ]
    with pytest.raises(ValueError, match="exactly one bit"):
        strict_kernel(4, [silent], bit_width=2)


def test_strict_kernel_checks_width_and_keeps_zero_weight_syntax():
    with pytest.raises(ValueError, match="positive integer"):
        strict_kernel(4, [], bit_width=True)
    with pytest.raises(ValueError, match="positive integer"):
        strict_kernel(4, [], bit_width=0)
    with pytest.raises(ValueError, match="2 to the bit width"):
        strict_kernel(4, [], bit_width=3)
    with pytest.raises(ValueError, match="2 to the bit width"):
        strict_kernel(3, [], bit_width=2)
    with pytest.raises(ValueError, match="integer state"):
        strict_kernel(
            4,
            [{"name": "far", "kind": "transition", "source": 0, "target": 4, "weight": 1}],
            bit_width=2,
        )
    with pytest.raises(ValueError, match="stays in its source"):
        strict_kernel(
            4,
            [{"name": "slip", "kind": "noop", "source": 0, "target": 1, "weight": 0}],
            bit_width=2,
        )
    with pytest.raises(ValueError, match="changes the state"):
        strict_kernel(3, [{"name": "stay", "kind": "transition", "source": 1, "target": 1, "weight": 0}])
    with pytest.raises(ValueError, match="at least two bits"):
        strict_kernel(
            2,
            [{"name": "wide", "kind": "joint", "source": 0, "target": 1, "weight": 1}],
            bit_width=1,
        )
    quiet = strict_kernel(
        4,
        [{"name": "bit", "kind": "toggle", "source": 0, "target": 1, "weight": 0}],
        bit_width=2,
    )
    assert quiet["events"][0]["kind"] == "toggle"
    assert quiet["events"][0]["weight"] == 0
    assert quiet["enabled_event_counts"][0] == 0
    assert quiet["completions"][0] == "halt_self_loop"
    full = strict_kernel(
        8,
        [{"name": "all", "kind": "joint", "source": 0, "target": 7, "weight": 1}],
        bit_width=3,
    )
    assert (0 ^ 7).bit_count() == 3
    assert full["probabilities"][0][7] == 1
    assert full["events"][0]["kind"] == "joint"


def test_same_kernel_can_hide_different_event_kinds():
    joint = [{"name": "both", "kind": "joint", "source": 0, "target": 3, "weight": 1}]
    neutral = [{"name": "move", "kind": "transition", "source": 0, "target": 3, "weight": 1}]
    left = strict_kernel(4, joint, bit_width=2)
    right = strict_kernel(4, neutral, bit_width=2)
    assert left["probabilities"] == right["probabilities"]
    assert left["probabilities"][0] == [Fraction(0), Fraction(0), Fraction(0), Fraction(1)]
    assert left["completions"][1] == "halt_self_loop"
    assert left["events"][0]["kind"] == "joint"
    assert right["events"][0]["kind"] == "transition"
    assert (0 ^ 3).bit_count() == 2
    forward = [
        {"name": "a", "kind": "joint", "source": 0, "target": 3, "weight": 1},
        {"name": "b", "kind": "transition", "source": 0, "target": 3, "weight": 3},
    ]
    backward = list(reversed(forward))
    first = strict_kernel(4, forward, bit_width=2)
    second = strict_kernel(4, backward, bit_width=2)
    assert first["probabilities"] == second["probabilities"]
    assert first["aggregated_weights"][0][3] == 4
    assert [event["kind"] for event in first["events"]] == ["joint", "transition"]
    assert [event["kind"] for event in second["events"]] == ["transition", "joint"]
    with pytest.raises(ValueError, match="duplicate event name"):
        strict_kernel(4, forward + [{"name": "a", "kind": "toggle", "source": 1, "target": 0, "weight": 1}], bit_width=2)
    enumerated = strict_kernel(
        3,
        [{"name": "hop", "kind": "transition", "source": 0, "target": 2, "weight": 1}],
    )
    assert enumerated["semantics"] == "enumerated"
    assert enumerated["bit_width"] is None
    assert enumerated["probabilities"][0] == [Fraction(0), Fraction(0), Fraction(1)]
    halted = strict_kernel(1, [])
    waiting = strict_kernel(
        1,
        [{"name": "stay", "kind": "noop", "source": 0, "target": 0, "weight": 1}],
    )
    assert halted["probabilities"] == waiting["probabilities"] == [[Fraction(1)]]
    assert halted["completions"] == ["halt_self_loop"]
    assert waiting["completions"] == ["noop_event"]
    for row in first["probabilities"]:
        assert sum(row) == 1


def test_atlas_017_catalogues_meet_the_strict_kind_check():
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    plan = json.loads((root / "plans" / "atlas-017.json").read_text(encoding="utf-8"))
    assert plan["method_id"] == "event-kernel-0.1.0"
    for item in plan["items"]:
        if item.get("catalogue") == "single_toggle":
            events = single_toggle_catalogue(item["rows"])
        else:
            events = item["events"]
        width = item.get("bit_width")
        loose = kernel(item["n_states"], events)
        strict = strict_kernel(item["n_states"], events, bit_width=width)
        assert loose["method"] == "event-kernel-0.1.0"
        assert strict["method"] == "event-kernel-0.2.0"
        assert loose["probabilities"] == strict["probabilities"]
        assert loose["completions"] == strict["completions"]
        if width is None:
            assert strict["semantics"] == "enumerated"
            assert all(event["kind"] in {"noop", "transition"} for event in strict["events"])
        else:
            assert strict["semantics"] == "bitmask"
            for event in strict["events"]:
                distance = (event["source"] ^ event["target"]).bit_count()
                if event["kind"] == "toggle":
                    assert distance == 1
                elif event["kind"] == "joint":
                    assert distance >= 2
                elif event["kind"] == "noop":
                    assert distance == 0
        stored = json.loads(
            (root / "results" / "atlas-017" / "items" / item["id"] / "result.json").read_text(
                encoding="utf-8"
            )
        )
        assert stored["method"] == "event-kernel-0.1.0"
    note = (root / "docs" / "event-semantics.md").read_text(encoding="utf-8")
    for phrase in (
        "not a frozen round",
        "event-kernel-0.1.0",
        "event-kernel-0.2.0",
        "exactly one bit",
        "at least two bits",
        "does not infer a bit width",
        "Atlas-017 was not rerun",
        "not a new primitive",
        "No intervention operator is defined",
    ):
        assert phrase in note


def test_event_kernel_item_serialises_fractions_without_a_weight_table():
    from rrc.cli import _event_kernel_problems
    from rrc.items import execute_event_kernel

    halt = execute_event_kernel(
        {
            "id": "halt",
            "round_id": "fixture",
            "type": "event_kernel",
            "role": "control",
            "family": "empty_catalogue",
            "n_states": 1,
            "events": [],
        }
    )
    noop = execute_event_kernel(
        {
            "id": "noop",
            "round_id": "fixture",
            "type": "event_kernel",
            "role": "comparison",
            "family": "noop_event",
            "n_states": 1,
            "events": [{"name": "stay", "kind": "noop", "source": 0, "target": 0, "weight": 1}],
        }
    )
    assert halt["engine_version"] == "rrc-0.4.0"
    assert halt["method"] == "event-kernel-0.1.0"
    assert halt["new_primitive"] is False
    assert halt["halt_self_loop_is_event"] is False
    assert halt["completions"] == ["halt_self_loop"]
    assert noop["completions"] == ["noop_event"]
    assert halt["probabilities"] == noop["probabilities"]
    assert halt["probabilities"][0][0]["num"] == "1"
    assert halt["probabilities"][0][0]["den"] == "1"
    assert "weight_sha256" not in halt
    assert "occupation" not in halt
    assert "kernel_method" not in halt
    assert _event_kernel_problems(
        {"id": "halt", "family": "empty_catalogue", "n_states": 1, "events": []},
        halt,
    ) == []
    mislabelled = dict(noop)
    mislabelled["completions"] = ["halt_self_loop"]
    assert _event_kernel_problems(
        {"id": "noop", "family": "noop_event", "n_states": 1},
        mislabelled,
    )
    with pytest.raises(ValueError, match="catalogue or an event list"):
        execute_event_kernel(
            {
                "id": "both",
                "type": "event_kernel",
                "family": "single_toggle",
                "n_states": 2,
                "catalogue": "single_toggle",
                "rows": [[1], [1]],
                "events": [],
            }
        )
