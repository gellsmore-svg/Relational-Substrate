"""Interruption, invalid output, timeout and incompatible-plan recovery."""

from __future__ import annotations

import json

import pytest

from rrc import ENGINE_VERSION
from rrc.cli import main
from rrc.items import execute_spec_catching
from rrc.runner import execute_plan, run_child
from rrc.store import IncompatiblePlan, Store


def _plan(items, round_id="probe"):
    for item in items:
        item.setdefault("round_id", round_id)
    return {
        "round_id": round_id,
        "engine_version": ENGINE_VERSION,
        "watchdog_seconds": 120,
        "hard_ceiling_seconds": 300,
        "items": items,
    }


def _ok(item_id, value=1):
    return {"id": item_id, "type": "probe", "mode": "ok", "value": value}


def _inprocess(item, _timeout):
    return execute_spec_catching(item)


def test_plan_command_refuses_an_unfrozen_round_and_does_not_run_the_frozen_one():
    with pytest.raises(SystemExit) as caught:
        main(["plan", "--round", "rrc-999"])
    assert caught.value.code != 0
    assert main(["plan", "--round", "rrc-001"]) == 0


def test_completed_item_is_not_repeated(tmp_path):
    plan = _plan([_ok("a", 7), _ok("b", 8)])
    calls = []

    def child(item, timeout):
        calls.append(item["id"])
        return _inprocess(item, timeout)

    first = execute_plan(plan, tmp_path, max_items=10, budget_seconds=30, child=child)
    assert first["ran"] == 2
    before = (tmp_path / "items" / "a" / "result.json").read_bytes()
    second = execute_plan(plan, tmp_path, max_items=10, budget_seconds=30, child=child)
    assert second["ran"] == 0
    assert calls == ["a", "b"]
    assert (tmp_path / "items" / "a" / "result.json").read_bytes() == before


def test_max_items_stops_cleanly(tmp_path):
    plan = _plan([_ok("a"), _ok("b"), _ok("c")])
    summary = execute_plan(plan, tmp_path, max_items=1, budget_seconds=30, child=_inprocess)
    assert summary["ran"] == 1
    assert summary["counts"]["complete"] == 1
    assert summary["counts"]["pending"] == 2


def test_parent_death_during_an_item_is_rerun(tmp_path):
    plan = _plan([_ok("a", 3)])
    store = Store(tmp_path, plan)
    store.prepare()
    store.write_status("a", "running")
    summary = execute_plan(plan, tmp_path, max_items=5, budget_seconds=30, child=_inprocess)
    assert summary["counts"]["complete"] == 1
    assert store.load_result("a")["value"] == 3
    assert any((tmp_path / "items" / "a" / "corrupt").iterdir())


def test_death_after_a_valid_result_adopts_it(tmp_path):
    plan = _plan([_ok("a", 4)])
    execute_plan(plan, tmp_path, max_items=5, budget_seconds=30, child=_inprocess)
    before = (tmp_path / "items" / "a" / "result.json").read_bytes()
    Store(tmp_path, plan).write_status("a", "running")
    calls = []

    def child(item, timeout):
        calls.append(item["id"])
        return _inprocess(item, timeout)

    execute_plan(plan, tmp_path, max_items=5, budget_seconds=30, child=child)
    assert calls == []
    assert (tmp_path / "items" / "a" / "result.json").read_bytes() == before


def test_partial_write_is_detected_and_rerun(tmp_path):
    plan = _plan([_ok("a", 5)])
    directory = tmp_path / "items" / "a"
    directory.mkdir(parents=True)
    (directory / "result.json.tmp").write_text("not finished", encoding="utf-8")
    store = Store(tmp_path, plan)
    store.prepare()
    assert store.classify("a") == "partial"
    execute_plan(plan, tmp_path, max_items=5, budget_seconds=30, child=_inprocess)
    assert store.classify("a") == "complete"
    assert json.loads((directory / "result.json").read_text())["value"] == 5


def test_invalid_result_is_not_accepted(tmp_path):
    plan = _plan([_ok("a", 6)])
    directory = tmp_path / "items" / "a"
    directory.mkdir(parents=True)
    (directory / "result.json").write_text("{", encoding="utf-8")
    store = Store(tmp_path, plan)
    store.prepare()
    assert store.classify("a") == "invalid"
    execute_plan(plan, tmp_path, max_items=5, budget_seconds=30, child=_inprocess)
    assert json.loads((directory / "result.json").read_text())["value"] == 6


def test_failed_item_stays_failed(tmp_path):
    plan = _plan([_ok("a", 1), {"id": "b", "type": "probe", "mode": "raise"}, _ok("c", 2)])

    def child(item, timeout):
        return _inprocess(item, timeout)

    summary = execute_plan(plan, tmp_path, max_items=10, budget_seconds=30, child=child)
    assert summary["counts"]["complete"] == 2
    assert summary["counts"]["failed"] == 1
    failed_bytes = (tmp_path / "items" / "b" / "result.json").read_bytes()
    calls = []

    def counting(item, timeout):
        calls.append(item["id"])
        return child(item, timeout)

    again = execute_plan(plan, tmp_path, max_items=10, budget_seconds=30, child=counting)
    assert again["ran"] == 0
    assert calls == []
    assert (tmp_path / "items" / "b" / "result.json").read_bytes() == failed_bytes


def test_timeout_stays_timeout(tmp_path):
    plan = _plan([_ok("a", 1), {"id": "slow", "type": "probe", "mode": "sleep", "seconds": 30}])

    def child(item, timeout):
        if item["id"] == "slow":
            return {"status": "timeout", "error": "killed", "item_id": "slow"}
        return _inprocess(item, timeout)

    execute_plan(plan, tmp_path, max_items=10, budget_seconds=30, child=child)
    before = (tmp_path / "items" / "slow" / "result.json").read_bytes()
    execute_plan(plan, tmp_path, max_items=10, budget_seconds=30, child=child)
    assert (tmp_path / "items" / "slow" / "result.json").read_bytes() == before
    assert b"timeout" in before


def test_incompatible_plan_refuses_and_keeps_bytes(tmp_path):
    plan = _plan([_ok("a", 9)])
    execute_plan(plan, tmp_path, max_items=5, budget_seconds=30, child=_inprocess)
    before = (tmp_path / "items" / "a" / "result.json").read_bytes()
    changed = dict(plan)
    changed["note"] = "different experiment"
    with pytest.raises(IncompatiblePlan):
        execute_plan(changed, tmp_path, max_items=5, budget_seconds=30, child=_inprocess)
    assert (tmp_path / "items" / "a" / "result.json").read_bytes() == before


def test_subprocess_timeout_kills_a_sleeping_item(tmp_path):
    plan = _plan([{"id": "slow", "type": "probe", "mode": "sleep", "seconds": 30}])
    summary = execute_plan(plan, tmp_path, max_items=2, budget_seconds=20, timeout=1, child=run_child)
    assert summary["counts"]["timeout"] == 1
    again = execute_plan(plan, tmp_path, max_items=2, budget_seconds=20, timeout=1, child=run_child)
    assert again["ran"] == 0


def test_preflight_records_time_and_not_a_defect(tmp_path):
    destination = tmp_path / "preflight.json"
    assert main([
        "preflight",
        "--sizes",
        "4",
        "--closure-max-n",
        "4",
        "--stationary-max-n",
        "4",
        "--out",
        str(destination),
    ]) == 0
    text = destination.read_text(encoding="utf-8")
    assert '"scientific": false' in text
    assert "defect_l1" not in text
    assert "exact" not in text


def test_subprocess_probe_completes(tmp_path):
    plan = _plan([_ok("a", 11)])
    summary = execute_plan(plan, tmp_path, max_items=2, budget_seconds=20, timeout=15, child=run_child)
    assert summary["counts"]["complete"] == 1
    assert Store(tmp_path, plan).load_result("a")["value"] == 11
