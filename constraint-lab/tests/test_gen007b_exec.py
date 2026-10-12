"""Durable two-level scheduling tests. They do not solve the scientific census."""

from __future__ import annotations

import json
from decimal import Decimal

import pytest

from rs_constraint_lab.durable import atomic_write_json
from rs_constraint_lab.gen007b_exec import MissingPoint, PointIndex, _pair_record, advance, execute_item, plan, plan_smoke
from rs_constraint_lab.supervisor import ensure_planned
from rs_constraint_lab.v07b import fresh_calibration, is_robustness, text_from_log
from rs_constraint_lab.workstore import Layout, load_state, publish_item, read_valid_item, result_hash, save_state, utc_now, work_index


def test_plan_freezes_344_items_and_a_second_plan_adds_none(tmp_path):
    first = plan(tmp_path)
    second = plan(tmp_path)
    assert first["logical_calibration_problems"] == 42
    assert first["unique_structures_in_profile"] == 4
    assert first["initial_atomic_items"] == 344
    assert first["work_count"]["initial_atomic_items"] == 344
    assert second["planned_new_items"] == 0
    assert len(work_index(Layout(tmp_path))) == 344


def test_a_missing_parameter_point_is_one_durable_item_and_a_duplicate_is_not(tmp_path):
    plan_smoke(tmp_path)
    layout = Layout(tmp_path)
    problem = json.loads((layout.plan() / "problems.json").read_text(encoding="utf-8"))[0]
    index = PointIndex(layout)
    index.load()
    with pytest.raises(MissingPoint):
        index.require_pair(problem["structure_id"], "1.000000000000e+0", "1.000000000000e+0", problem["rho"], problem["alphabet"])
    odd = text_from_log(Decimal("-3.5"))
    record = _pair_record(problem, odd, odd)
    assert ensure_planned(layout, record) is True
    assert ensure_planned(layout, record) is False
    assert sum(1 for row in work_index(layout).values() if row["input"].get("m_off") == odd) == 1


def test_a_completed_parameter_point_stays_complete(tmp_path):
    plan_smoke(tmp_path)
    layout = Layout(tmp_path)
    record = next(row for row in work_index(layout).values() if row["kind"] == "pair_point")
    result = {"delta_forward": 0.0, "delta_reverse": 0.0}
    payload = {
        "analysis_version": record["analysis_version"],
        "completed_at": utc_now(),
        "input": record["input"],
        "input_hash": record["input_hash"],
        "item_id": record["item_id"],
        "kind": record["kind"],
        "result": result,
        "result_hash": result_hash(result),
        "schema": "rs-constraint-lab.item/v1",
        "semantic_version": record["semantic_version"],
        "solver_residuals": {},
        "spec_hash": record["spec_hash"],
        "started_at": utc_now(),
    }
    publish_item(layout, payload, record["spec_hash"])
    before = layout.item_path(record["item_id"]).read_bytes()
    state = load_state(layout)
    state[record["item_id"]]["status"] = "complete"
    save_state(layout, state)
    assert ensure_planned(layout, record) is False
    assert read_valid_item(layout, record["item_id"], record["spec_hash"])["result"] == result
    assert layout.item_path(record["item_id"]).read_bytes() == before


def test_unresolved_calibration_does_not_schedule_composition(tmp_path):
    plan(tmp_path)
    layout = Layout(tmp_path)
    problems = json.loads((layout.plan() / "problems.json").read_text(encoding="utf-8"))
    represented = next(problem for problem in problems if not is_robustness(problem))
    for problem in problems:
        state = fresh_calibration(problem)
        if problem["calibration_id"] == represented["calibration_id"]:
            state["status"] = "represented"
            state["solutions"] = [
                {
                    "basin_id": "b0",
                    "boundary_class": "finite interior solution",
                    "d_neutral": 0.0,
                    "m_off": problem["nominal"],
                    "m_on": problem["nominal"],
                }
            ]
            state["solution_count"] = 1
            state["selected_solution"] = state["solutions"][0]
        else:
            state["status"] = "unresolved_at_cap"
            state["solutions"] = [
                {
                    "basin_id": "b0",
                    "boundary_class": "finite interior solution",
                    "d_neutral": 0.0,
                    "m_off": problem["nominal"],
                    "m_on": problem["nominal"],
                }
            ]
            state["solution_count"] = 1
            state["selected_solution"] = state["solutions"][0]
        atomic_write_json(layout.calibration() / f"{problem['calibration_id']}.json", state)
    added = advance(tmp_path)
    assert added == 2
    kinds = [row["kind"] for row in work_index(layout).values()]
    assert kinds.count("target_composition") == 1
    assert kinds.count("control_composition") == 1
    assert advance(tmp_path) == 0


def test_target_singleton_item_serializes(tmp_path):
    plan_smoke(tmp_path)
    layout = Layout(tmp_path)
    record = next(row for row in work_index(layout).values() if row["kind"] == "target_singleton")
    result = execute_item(record, {"cache": {}, "root": tmp_path})
    json.dumps(result)
    assert len(result["directions"]["path_to_matching"]["q"]) == 1024


def test_verify_accepts_007b_terminal_status_and_calibration_rows(tmp_path):
    from rs_constraint_lab.supervisor import verify_root

    plan_smoke(tmp_path)
    layout = Layout(tmp_path)
    problem = json.loads((layout.plan() / "problems.json").read_text(encoding="utf-8"))[0]
    atomic_write_json(layout.progress() / "status.json", {"state": "COMPLETE"})
    atomic_write_json(
        layout.calibration() / f"{problem['calibration_id']}.json",
        {"calibration_id": problem["calibration_id"], "status": "represented"},
    )
    atomic_write_json(
        layout.merge() / "summary.json",
        {"items": [], "rows": [{"target_id": problem["target_id"], "calibration_id": problem["calibration_id"]}]},
    )
    missing = verify_root(tmp_path)
    assert any(problem["calibration_id"] in item for item in missing["problems"])
    atomic_write_json(
        layout.merge() / "rows" / f"{problem['calibration_id']}.json",
        {"row": {"calibration_id": problem["calibration_id"], "target_id": problem["target_id"]}},
    )
    report = verify_root(tmp_path, require_complete=True)
    assert report["ok"] is True
    assert report["complete"] is True
    atomic_write_json(
        layout.calibration() / f"{problem['calibration_id']}.json",
        {"calibration_id": problem["calibration_id"], "status": "refining"},
    )
    refused = verify_root(tmp_path)
    assert any("is not terminal" in item for item in refused["problems"])
