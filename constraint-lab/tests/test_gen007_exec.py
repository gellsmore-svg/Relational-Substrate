"""Planner and disk-book tests. They do not run the generation census."""

from __future__ import annotations

from fractions import Fraction

import pytest

from rs_constraint_lab.constraints import parse_expression
from rs_constraint_lab.gen007_exec import DiskBook, MissingPoint, PointIndex, choose_batch_count, plan_smoke
from rs_constraint_lab.v07 import POSITIVE_GRID
from rs_constraint_lab.workstore import Layout


def test_batch_count_respects_the_45_second_target_and_the_slow_item_floor():
    assert choose_batch_count([]) == 1
    assert choose_batch_count([61.0]) == 1
    assert choose_batch_count([0.5, 0.5, 0.5]) == 90
    assert choose_batch_count([0.3]) == 150


def test_plan_smoke_is_idempotent_and_keeps_two_problems(tmp_path):
    first = plan_smoke(tmp_path)
    second = plan_smoke(tmp_path)
    assert first["problems"] == 2
    assert first["planned_new_items"] > 0
    assert second["planned_new_items"] == 0
    assert len(list((tmp_path / "items").glob("*.json"))) == 0


def test_verify_checks_generation_rows_and_item_hashes(tmp_path):
    from rs_constraint_lab.durable import atomic_write_json
    from rs_constraint_lab.supervisor import verify_root
    from rs_constraint_lab.workstore import load_state, load_work_items, publish_item, result_hash, save_state, utc_now

    plan_smoke(tmp_path)
    layout = Layout(tmp_path)
    record = load_work_items(layout)[0]
    result = {"ok": True}
    digest = result_hash(result)
    publish_item(
        layout,
        {
            "analysis_version": record["analysis_version"],
            "completed_at": utc_now(),
            "input": record["input"],
            "input_hash": record["input_hash"],
            "item_id": record["item_id"],
            "kind": record["kind"],
            "result": result,
            "result_hash": digest,
            "schema": "rs-constraint-lab.item/v1",
            "semantic_version": record["semantic_version"],
            "solver_residuals": {},
            "spec_hash": record["spec_hash"],
            "started_at": utc_now(),
        },
        record["spec_hash"],
    )
    state = load_state(layout)
    state[record["item_id"]]["status"] = "complete"
    save_state(layout, state)
    atomic_write_json(layout.progress() / "status.json", {"state": "COMPLETE"})
    atomic_write_json(
        layout.merge() / "summary.json",
        {"items": [{"item_id": record["item_id"], "result_hash": digest}], "rows": [{"target_id": "target-a"}]},
    )
    missing = verify_root(tmp_path)
    assert any("missing row target-a" in problem for problem in missing["problems"])
    atomic_write_json(layout.merge() / "rows" / "target-a.json", {"row": {"target_id": "target-a"}, "stamp": "x"})
    report = verify_root(tmp_path)
    assert report["ok"] is True
    atomic_write_json(
        layout.merge() / "summary.json",
        {"items": [{"item_id": record["item_id"], "result_hash": "0" * 64}], "rows": [{"target_id": "target-a"}]},
    )
    drifted = verify_root(tmp_path)
    assert any("hash mismatch" in problem for problem in drifted["problems"])


def test_disk_book_raises_until_a_point_is_durable(tmp_path):
    plan_smoke(tmp_path)
    layout = Layout(tmp_path)
    index = PointIndex(layout)
    index.load()
    book = DiskBook(index=index, slots=__import__("rs_constraint_lab.gen007_exec", fromlist=["_world"])._world()["slots"], alphabet="W4", rho="1")
    rule = parse_expression("dissolve(0-1) => continuous", 4, order=3)
    with pytest.raises(MissingPoint):
        book.evaluate(rule, Fraction(1))
    assert POSITIVE_GRID[0] > 0
