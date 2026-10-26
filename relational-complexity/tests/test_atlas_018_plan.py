"""Frozen plans for atlas-018, atlas-019, and atlas-020. They do not read results."""

from __future__ import annotations

import json
from pathlib import Path

from rrc.cli import main
from rrc.store import digest

ROOT = Path(__file__).resolve().parents[1]

PLANS = {
    "atlas-018": "2468bf59c1fce72fb909482dc94e1abeae30e627f0bd71e4536ed8b10b7a27e0",
    "atlas-019": "b38fc52ecf2082229f8e3a972df76ca5c25b57db251241e2605caa8a25564a86",
    "atlas-020": "8bc18f3947ed128deddaab0ed5ede7d2d4d6698bfe27937b78fb57aadc306191",
}


def _plan(round_id: str) -> tuple[str, dict]:
    assert main(["plan", "--round", round_id]) == 0
    text = (ROOT / "plans" / f"{round_id}.json").read_text(encoding="utf-8")
    return text, json.loads(text)


def _questions() -> dict:
    return {
        json.loads(line)["question_id"]: json.loads(line)
        for line in (ROOT / "atlas" / "questions.jsonl").read_text(encoding="utf-8").splitlines()
    }


def test_three_plans_are_frozen_before_their_runs():
    questions = _questions()
    for question in (f"ATLAS-Q{index:02d}" for index in range(1, 16)):
        assert questions[question]["status"] == "open"
    ideas = {
        json.loads(line)["idea_id"]: json.loads(line)
        for line in (ROOT / "atlas" / "ideas.jsonl").read_text(encoding="utf-8").splitlines()
    }
    assert ideas["IDEA-L23"]["status"] == "open"
    assert ideas["IDEA-L23"]["status"] != "selected"
    for round_id, plan_hash in PLANS.items():
        text, plan = _plan(round_id)
        assert digest(plan) == plan_hash
        assert plan["engine_version"] == "rrc-0.4.0"
        assert plan["definitions_commit"] == "81389d9d50eafe53ccd0e6eee339602989f13886"
        assert plan["preflight_summary"]["scientific"] is False
        assert plan["preflight_summary"]["heaviest_cell_s"] == 0.002
        assert plan["coverage"]["six_is_not_a_target"] is True
        assert plan["coverage"]["cells"] == len(plan["items"])
        preflight = (ROOT / "docs" / f"{round_id}-preflight.md").read_text(encoding="utf-8")
        assert "scientific` is false" in preflight
        assert "Observables were not retained" in preflight
        for phrase in ("1/2", "2/7", "5/7", "1/3", "2/3", "13/8"):
            assert phrase not in text
        for item in plan["items"]:
            assert "idea_ids" not in item


def test_atlas_018_declares_the_copy_map_and_not_a_horizon():
    _text, plan = _plan("atlas-018")
    assert plan["questions"] == ["ATLAS-Q10"]
    assert "ATLAS-Q15" in plan["questions_not_in_this_round"]
    assert "ATLAS-Q06" in plan["questions_not_in_this_round"]
    assert plan["method_id"] == "event-kernel-0.2.0"
    assert [item["id"] for item in plan["items"]] == ["A18-identified", "A18-free", "A18-coupled"]
    identified, free, coupled = plan["items"]
    assert identified["catalogue"] == "single_toggle"
    assert identified["n_states"] == 8
    assert "image_map" not in identified
    assert free["n_states"] == coupled["n_states"] == 16
    assert free["image_map"] == coupled["image_map"]
    mapped = []
    for state in range(8):
        e0 = state & 1
        e1 = (state >> 1) & 1
        e2 = (state >> 2) & 1
        mapped.append(e0 | (e1 << 1) | (e1 << 2) | (e2 << 3))
    assert free["image_map"] == mapped
    assert len(set(mapped)) == 8
    assert free["reference"]["rows"] == identified["rows"]
    assert coupled["reference"]["rows"] == identified["rows"]
    assert "events" not in free
    assert "catalogue" not in coupled
    joints = [event for event in coupled["events"] if event["kind"] == "joint"]
    toggles = [event for event in coupled["events"] if event["kind"] == "toggle"]
    assert len(joints) == 16
    assert len(toggles) == 32
    assert all(event["target"] == event["source"] ^ 6 for event in joints)
    assert all(event["weight"] == 1 for event in coupled["events"])
    assert all("horizon" not in item for item in plan["items"])
    assert "ATLAS-Q10" in (ROOT / "docs" / "atlas-018-preflight.md").read_text(encoding="utf-8")


def test_atlas_019_restates_the_laws_and_names_one_partition():
    _text, plan = _plan("atlas-019")
    assert plan["questions"] == ["ATLAS-Q13"]
    assert "ATLAS-Q10" in plan["questions_not_in_this_round"]
    assert [item["id"] for item in plan["items"]] == ["A19-free", "A19-coupled", "A19-frozen"]
    labels = []
    for state in range(16):
        labels.append(1 if ((state >> 1) & 1) == ((state >> 2) & 1) else 0)
    subset = [state for state, label in enumerate(labels) if label == 1]
    for item in plan["items"]:
        assert item["type"] == "event_horizon"
        assert item["horizon"] == 2
        assert item["initial_state"] == 0
        assert item["labels"] == labels
        assert item["subset"] == subset
        assert item["n_states"] == 16
    frozen = plan["items"][2]
    assert all(event["kind"] == "toggle" for event in frozen["events"])
    assert all(event["target"] in {event["source"] ^ 1, event["source"] ^ 8} for event in frozen["events"])
    assert "reading results/atlas-018" in plan["coverage"]["excluded"]
    assert "ATLAS-Q13" in (ROOT / "docs" / "atlas-019-preflight.md").read_text(encoding="utf-8")


def test_atlas_020_pairs_form_with_dissolve_on_one_path():
    _text, plan = _plan("atlas-020")
    assert plan["questions"] == ["ATLAS-Q04"]
    assert "ATLAS-Q10" in plan["questions_not_in_this_round"]
    assert "ATLAS-Q13" in plan["questions_not_in_this_round"]
    assert [item["id"] for item in plan["items"]] == [
        "A20-base",
        "A20-either",
        "A20-form",
        "A20-dissolve",
    ]
    assert plan["items"][0]["constraints"] == []
    actions = []
    for item in plan["items"][1:]:
        assert item["n"] == 4
        assert item["carrier"]["edges"] == [[0, 1], [1, 2]]
        assert len(item["constraints"]) == 1
        constraint = item["constraints"][0]
        assert constraint["effect"] == "prohibit"
        assert constraint["event"] == [0, 1]
        assert constraint["when"] == {"edge": [1, 2], "polarity": "present"}
        actions.append(constraint["action"])
        assert "factor" not in constraint
    assert actions == ["either", "form", "dissolve"]
    assert "ATLAS-Q04" in (ROOT / "docs" / "atlas-020-preflight.md").read_text(encoding="utf-8")
