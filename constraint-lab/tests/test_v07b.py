"""Generation 007B planner tests. They do not run the scientific census."""

from __future__ import annotations

import json
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import pytest

from rs_constraint_lab.constraints import parse_expression
from rs_constraint_lab.execution import IncompatibleGeneration, build_plan
from rs_constraint_lab.gen007_exec import solve_singleton
from rs_constraint_lab.spec import load_spec
from rs_constraint_lab.v05 import _grammar
from rs_constraint_lab.v06 import WEIGHT_ORDER
from rs_constraint_lab.v07 import DIRECTIONS, parse_multiplier_text, with_multiplier
from rs_constraint_lab.v07b import (
    ADAPTIVE_CAP,
    COARSE_PAIRS,
    COMPLEXITY_CONTROL,
    COMPLEXITY_TARGET,
    NEWTON_WIDTH,
    ROBUSTNESS_ROWS,
    TERMINAL_STATUSES,
    _consume,
    _corners,
    _new_basin,
    _point_key,
    _quadrants,
    _select,
    _stencil,
    _widths,
    active_rule_count,
    build_problems,
    fresh_calibration,
    is_preflight,
    is_robustness,
    scales_for,
    solve_pair_point,
    step_problem,
    text_from_log,
    two_level_rules,
    work_count,
    log_from_text,
)

SPEC = Path(__file__).resolve().parents[1] / "experiments" / "specs" / "generation-007b.json"


@pytest.fixture(scope="module")
def problems():
    return build_problems(load_spec(SPEC))


def _target():
    return {"delta_forward": 0.0, "delta_reverse": 0.0, "q0_forward": 1.0, "q0_reverse": 1.0}


def _store(residual, m_off: str, m_on: str) -> dict:
    if m_off == "0" or m_on == "0":
        forward, reverse = 1.0, 1.0
    else:
        forward, reverse = residual(float(log_from_text(m_off)), float(log_from_text(m_on)))
    return {"delta_forward": forward, "delta_reverse": reverse}


def _grid(residual) -> dict:
    return {_point_key(m_off, m_on): _store(residual, m_off, m_on) for m_off, m_on in COARSE_PAIRS}


def _state():
    return fresh_calibration(
        {
            "calibration_id": "analytic",
            "nominal": text_from_log(Decimal(0)),
            "structure_id": "analytic",
            "target_id": "analytic",
        }
    )


def _drive(residual, limit: int = 80):
    points = _grid(residual)
    target = _target()
    scales = scales_for(target)
    state = _state()
    for _step in range(limit):
        state, requests = step_problem(state, points, target, scales, 1e-8)
        if state["status"] in TERMINAL_STATUSES:
            return state
        assert requests, state["status"]
        assert len(requests) == len(set(requests))
        for m_off, m_on in requests:
            key = _point_key(m_off, m_on)
            assert key not in points
            points[key] = _store(residual, m_off, m_on)
    raise AssertionError(state["status"])


def test_frozen_work_count_matches_the_live_catalogue(problems):
    counted = work_count(problems)
    assert counted["logical_calibration_problems"] == 42
    assert counted["unique_two_level_structures"] == 4
    assert counted["unique_target_singletons"] == 20
    assert counted["coarse_points_per_structure"] == 81
    assert counted["initial_atomic_items"] == 344
    assert counted["adaptive_cap_per_problem"] == ADAPTIVE_CAP == 250
    assert COMPLEXITY_TARGET == (3, 1, 1, 2, 1, 0, 0)
    assert COMPLEXITY_CONTROL == (2, 2, 2, 2, 1, 0, 0)
    preflight = [row for row in problems if is_preflight(row)]
    assert len(preflight) == 15
    assert len({row["structure_id"] for row in preflight}) == 4
    assert len([row for row in problems if is_robustness(row)]) == 6
    assert any(row["polarity"] == "present" for row in preflight)
    assert any(row["polarity"] == "absent" for row in preflight)
    for row in ROBUSTNESS_ROWS:
        assert any(is_robustness(problem) and (problem["geometry"], problem["polarity"], problem["w_T"], problem["w_P"], problem["relation"]) == row for problem in problems)


def test_exactly_one_complementary_rule_is_active_on_an_admissible_dissolve(problems):
    for problem in problems:
        off = parse_expression(problem["off_expression"], 4, order=3)
        on = parse_expression(problem["on_expression"], 4, order=3)
        assert two_level_rules(on)[0].conditions != two_level_rules(on)[1].conditions
        assert off.action == on.action
        assert off.conditions[0][0] != off.action
        other = (off.action + 1) % 10
        for state in range(1024):
            admissible = ((state >> off.action) & 1) == 1
            assert active_rule_count((off, on), state, off.action) == (1 if admissible else 0)
            assert active_rule_count((off, on), state, other) == 0


def test_one_analytic_root_is_a_unique_well_conditioned_representation():
    state = _drive(lambda log_off, log_on: (log_off, log_on - 1.0))
    assert state["representation_label"] == "R2"
    assert state["solution_count"] == 1
    selected = state["selected_solution"]
    assert abs(float(log_from_text(selected["m_off"]))) <= 0.02
    assert abs(float(log_from_text(selected["m_on"])) - 1.0) <= 0.02
    assert selected["condition_number"] is not None
    assert selected["condition_number"] < 1e6
    assert state["adaptive_count"] <= ADAPTIVE_CAP


def test_two_separated_analytic_roots_stay_distinct():
    state = _drive(lambda log_off, log_on: (log_off * (log_off - 1.0), log_on))
    assert state["representation_label"] == "R3"
    assert state["solution_count"] == 2
    logs = sorted((float(log_from_text(row["m_off"])), float(log_from_text(row["m_on"]))) for row in state["solutions"])
    assert logs[0][0] == pytest.approx(0.0, abs=0.02)
    assert logs[1][0] == pytest.approx(1.0, abs=0.02)
    assert state["selected_solution"]["m_off"] == text_from_log(Decimal(0))


def test_adaptive_cap_rejects_a_stencil_that_does_not_fit(monkeypatch):
    monkeypatch.setattr("rs_constraint_lab.v07b.ADAPTIVE_CAP", 0)
    points = _grid(lambda log_off, log_on: (log_off - 0.5, log_on - 0.5))
    target = _target()
    state, requests = step_problem(_state(), points, target, scales_for(target), 1e-8)
    assert requests == []
    assert state["status"] == "unresolved_at_cap"
    assert state["adaptive_count"] == 0
    assert state["representation_label"] == "unresolved"


def test_a_repeated_request_does_not_increase_the_adaptive_count():
    points = _grid(lambda log_off, log_on: (log_off - 0.5, log_on - 0.5))
    target = _target()
    scales = scales_for(target)
    state, requests = step_problem(_state(), points, target, scales, 1e-8)
    assert requests
    assert state["adaptive_count"] == len(requests)
    again, repeated = step_problem(state, points, target, scales, 1e-8)
    assert repeated == requests
    assert again["adaptive_count"] == state["adaptive_count"]


def test_multi_solution_state_is_unchanged_when_the_search_is_reloaded():
    state = _drive(lambda log_off, log_on: (log_off * (log_off - 1.0), log_on))
    points = _grid(lambda log_off, log_on: (log_off * (log_off - 1.0), log_on))
    target = _target()
    restored = json.loads(json.dumps(state))
    again, requests = step_problem(restored, points, target, scales_for(target), 1e-8)
    assert requests == []
    assert again["solution_count"] == state["solution_count"]
    assert again["selected_solution"]["m_off"] == state["selected_solution"]["m_off"]
    assert again["selected_solution"]["m_on"] == state["selected_solution"]["m_on"]
    assert again["representation_label"] == "R3"


def test_two_level_matches_the_scalar_pair_face_and_the_erasure(problems):
    problem = problems[0]
    slots = _grammar(WEIGHT_ORDER, 4).slot_list()
    off = parse_expression(problem["off_expression"], 4, order=3)
    on = parse_expression(problem["on_expression"], 4, order=3)
    scalar = with_multiplier(parse_expression(problem["on_expression"].replace(" => m_on", " => " + problem["w_T"]), 4, order=3))
    erased = with_multiplier(parse_expression(problem["t_expression"].split(" | ")[0] + " => " + problem["w_T"], 4, order=3))
    rho = Fraction(1)
    gaps = []
    for text in ("1.000000000000e+0", "1.000000000000e-1"):
        multiplier = parse_multiplier_text(text)
        pair = solve_pair_point(off, on, Fraction(1), multiplier, problem["alphabet"], rho, slots, {})
        one = solve_singleton(scalar, multiplier, problem["alphabet"], rho, slots, {}, None)
        both = solve_pair_point(off, on, multiplier, multiplier, problem["alphabet"], rho, slots, {})
        blank = solve_singleton(erased, multiplier, problem["alphabet"], rho, slots, {}, None)
        for direction in DIRECTIONS:
            gaps.append(abs(pair["directions"][direction]["delta"] - one["directions"][direction]["delta"]))
            gaps.append(abs(both["directions"][direction]["delta"] - blank["directions"][direction]["delta"]))
    assert max(gaps) < 1e-10


def test_monolithic_generation_007b_plan_is_refused():
    with pytest.raises(IncompatibleGeneration, match="generation007b"):
        build_plan(load_spec(SPEC), 14)


def test_zero_nominal_prefers_deletion_and_does_not_divide_by_zero():
    deletion = {"basin_id": "deletion", "m_off": "0", "m_on": "0"}
    small = {"basin_id": "small", "m_off": "1.000000000000e-1", "m_on": "1.000000000000e+0"}
    large = {"basin_id": "large", "m_off": "1.000000000000e+1", "m_on": "1.000000000000e+1"}
    chosen, reason = _select([small, large, deletion], "0")
    assert chosen["basin_id"] == "deletion"
    assert "zero-nominal" in reason
    chosen, _reason = _select([large, small], "0")
    assert chosen["basin_id"] == "small"
    near = {"basin_id": "near", "m_off": "1.000000000000e+0", "m_on": "1.000000000000e+0"}
    far = {"basin_id": "far", "m_off": "1.000000000000e+2", "m_on": "1.000000000000e-2"}
    chosen, reason = _select([far, deletion, near], "1.000000000000e+0")
    assert chosen["basin_id"] == "near"
    assert "log departure" in reason
    chosen, _reason = _select([deletion, far], "1.000000000000e+0")
    assert chosen["basin_id"] == "far"


def test_a_zero_nominal_calibration_closes_without_dividing_by_zero():
    residual = lambda log_off, log_on: (log_off, log_on - 1.0)
    points = _grid(residual)
    target = _target()
    scales = scales_for(target)
    state = fresh_calibration(
        {
            "calibration_id": "analytic-zero-nominal",
            "nominal": "0",
            "structure_id": "analytic",
            "target_id": "analytic",
        }
    )
    for _step in range(80):
        state, requests = step_problem(state, points, target, scales, 1e-8)
        if state["status"] in TERMINAL_STATUSES:
            break
        assert requests
        for m_off, m_on in requests:
            key = _point_key(m_off, m_on)
            assert key not in points
            points[key] = _store(residual, m_off, m_on)
    assert state["status"] == "represented"
    assert state["solution_count"] == 1
    assert state["selected_solution"]["m_on"] != "0"


def _plant(points: dict, pairs) -> None:
    for m_off, m_on in pairs:
        points[_point_key(m_off, m_on)] = {"delta_forward": 1.0, "delta_reverse": 1.0}


def test_newton_requests_a_missing_jacobian_instead_of_exhausting():
    basin = _new_basin("b0", Decimal("0.375"), Decimal("0.40625"), Decimal("0.375"), Decimal("0.40625"), "sign_enclosure")
    basin["mode"] = "newton"
    centre = text_from_log(Decimal("0.404"))
    points = {_point_key(centre, centre): {"delta_forward": 1e-6, "delta_reverse": 4e-6}}
    _consume(basin, points, _target(), scales_for(_target()), 1e-8, [basin])
    assert basin["status"] == "open"
    assert basin["mode"] == "newton"
    assert basin["waiting"]
    assert basin["newton_steps"] == 0


def test_a_wide_basin_keeps_subdividing_when_the_stencil_is_already_stored():
    basin = _new_basin("b0", Decimal("-3"), Decimal("-1"), Decimal("-4"), Decimal("-3"), "sign_enclosure")
    basin["mode"] = "zero"
    basin["zero_probed"] = True
    points = {}
    _plant(points, _corners(Decimal("-3"), Decimal("-1"), Decimal("-4"), Decimal("-3")))
    for quad in _quadrants(basin):
        _plant(points, _corners(*quad))
        child = _new_basin("child", *quad, "split")
        _plant(points, _stencil(child))
    target = _target()
    before = max(_widths(basin))
    _consume(basin, points, target, scales_for(target), 1e-8, [basin])
    assert basin["status"] == "open"
    assert basin["mode"] == "subdivide"
    assert basin["newton_steps"] == 0
    assert basin["waiting"] == []
    assert NEWTON_WIDTH < max(_widths(basin)) < before
