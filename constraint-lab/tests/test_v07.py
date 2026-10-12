"""v0.7 effect-matched controls. Generation 6 outputs are not redefined here."""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from rs_constraint_lab.cli import main
from rs_constraint_lab.constraints import DISSOLVE, Constraint
from rs_constraint_lab.execution import IncompatibleGeneration, build_plan
from rs_constraint_lab.spec import validate_spec
from rs_constraint_lab.v05 import _grammar
from rs_constraint_lab.v06 import WEIGHT_ORDER, graded_catalogue
from rs_constraint_lab.v07 import (
    ANALYSIS_7,
    CALIBRATION_VERSION,
    CALIBRATION_WEIGHT,
    CELL_INDEX,
    DIRECTIONS,
    EFFECT_FLOOR_DEFAULT,
    JOINT_DISTANCE_TIE,
    M_MAX,
    M_MIN,
    MATCH_TOLERANCE_DEFAULT,
    POSITIVE_GRID,
    _catalogue_view,
    _composition_numbers,
    _live_controls,
    _minimal_spec,
    _require_v07_spec,
    calibrate_control,
    coverage_plan,
    joint_distance,
    joint_scales,
    minimise_joint,
    multiplier_text,
    nominal_multiplier,
    numerical_reference,
    parse_multiplier_text,
    relabelled_kernel_gap,
    require_multiplier,
    selected_records,
    solve_roots,
    state_shape_report,
)
from rs_constraint_lab.weights import ENUMERATED_WEIGHTS, alphabet_factors

LAB = Path(__file__).resolve().parents[1]
RULE = Constraint(DISSOLVE, 0, (), CALIBRATION_WEIGHT, ())


def _rows():
    path = LAB / "provenance" / "ledger.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _book(forward, reverse, zero_forward=-100.0, zero_reverse=-100.0):
    class Book:
        def curve(self, rule):
            points = {
                multiplier_text(multiplier): {
                    "path_to_matching": {"delta": forward(multiplier)},
                    "matching_to_path": {"delta": reverse(multiplier)},
                }
                for multiplier in POSITIVE_GRID
            }
            return {
                "points": points,
                "zero": {
                    "path_to_matching": {"delta": zero_forward},
                    "matching_to_path": {"delta": zero_reverse},
                },
            }

        def evaluate(self, rule, multiplier):
            stored = self.curve(rule)
            if multiplier == 0:
                return stored["zero"]
            text = multiplier_text(multiplier)
            hit = stored["points"].get(text)
            if hit is not None:
                return hit
            return {
                "path_to_matching": {"delta": forward(multiplier)},
                "matching_to_path": {"delta": reverse(multiplier)},
            }

    return Book()


def _target(forward: float, reverse: float, q0_forward=0.2, q0_reverse=0.8) -> dict:
    return {
        "path_to_matching": {"delta": forward, "Q0": q0_forward},
        "matching_to_path": {"delta": reverse, "Q0": q0_reverse},
    }


def test_review_006_links_the_final_v06_head_and_run():
    review = (LAB / "provenance" / "reviews" / "006-chatgpt-review-v0.6.md").read_text(encoding="utf-8")
    assert "not a line-by-line audit" in review
    assert "4deef3aa272a3ceadb5c610fcc95eaa24fde3901" in review
    assert "37193089700" in review
    assert "37192986304" in review
    assert "research/constraint-lab-v0.6" in review
    assert "96.0" in review
    filed = next(row for row in _rows() if row.get("review_id") == "006")
    assert filed["target_of_review"] == "research/constraint-lab-v0.6"
    assert filed["reviewed_commit"] == "4deef3aa272a3ceadb5c610fcc95eaa24fde3901"
    assert filed["ci_run_id"] == "37193089700"
    assert filed["preceding_ci_run_id"] == "37192986304"
    assert filed["ci_conclusion_recorded"] == "success"
    assert filed["line_by_line_audit"] is False


def test_prompt_006_authored_metadata_stays_apart_from_agent_input():
    agent = LAB / "provenance" / "prompts" / "006-v0.6-agent-input.md"
    assert agent.stat().st_size == 42694
    assert _sha(agent) == "980d809393477c146fd45b63bf41e7d0af4cb1ef84141d7062d6e82965c487b0"
    external = next(
        row
        for row in _rows()
        if row["record_type"] == "prompt_representation"
        and row["prompt_id"] == "006"
        and row["authored_prompt_status"] == "externally_verified_pending_import"
    )
    assert external["authored_prompt_sha256"] == "b441a33f66b3376d9a009d1be18d9ac808311230cf0309762159c1164f3694f5"
    assert external["authored_prompt_bytes"] == 42598
    assert external["authored_prompt_locally_present"] is False
    assert external["relationship"] == "unknown"
    assert external["agent_input_prompt_sha256"] != external["authored_prompt_sha256"]
    original = next(row for row in _rows() if row["record_type"] == "prompt" and row["prompt_id"] == "006")
    assert original["authored_prompt_sha256"] is None
    assert original["authored_prompt_status"] == "pending_verbatim_import"


def test_prompt_007_provenance_does_not_contain_its_own_hash():
    path = LAB / "provenance" / "prompts" / "007-v0.7-agent-input.md"
    digest = _sha(path)
    text = path.read_text(encoding="utf-8")
    assert path.stat().st_size == 36986
    assert digest == "c87d1e7d851d0a8e4be10f120c3fa866aeb5e067570bdf7c039c6658834730bc"
    assert digest not in text
    assert text.startswith("\n# Relational Substrate Constraint Laboratory v0.7")
    assert text.endswith("the ontology or the passage.\n")
    stored = next(row for row in _rows() if row["record_type"] == "prompt" and row["prompt_id"] == "007")
    assert stored["prompt_sha256"] == digest
    assert stored["prompt_bytes"] == 36986
    assert stored["authored_prompt_sha256"] is None
    assert stored["authored_prompt_status"] == "pending_verbatim_import"
    assert stored["relationship"] == "unknown"
    assert stored["agent_input_prompt_sha256"] == digest
    assert stored["starting_commit"] == "4deef3aa272a3ceadb5c610fcc95eaa24fde3901"


def test_continuous_multiplier_reproduces_named_w4_factors_and_the_domain():
    factors = alphabet_factors("W4")
    assert factors["prohibit"] == Fraction(0)
    assert factors["strong_suppress"] == Fraction(1, 4)
    assert factors["weak_suppress"] == Fraction(1, 2)
    assert factors["weak_favour"] == Fraction(2)
    assert factors["strong_favour"] == Fraction(4)
    assert factors["neutral"] == Fraction(1)
    assert "neutral" not in _minimal_spec()["weights"]
    assert CALIBRATION_WEIGHT not in ENUMERATED_WEIGHTS
    for grade, factor in factors.items():
        assert nominal_multiplier(grade, "W4") == factor
    assert parse_multiplier_text(multiplier_text(Fraction(1))) == Fraction(1)
    assert multiplier_text(Fraction(1)) == "1.000000000000e+0"
    assert parse_multiplier_text("0") == 0
    assert parse_multiplier_text(multiplier_text(Fraction(1, 4))) == Fraction(1, 4)
    assert POSITIVE_GRID[0] == M_MIN
    assert POSITIVE_GRID[-1] == M_MAX
    assert len(POSITIVE_GRID) == 33
    assert all(M_MIN <= point <= M_MAX for point in POSITIVE_GRID)
    with pytest.raises(ValueError):
        require_multiplier(Fraction(0))
    with pytest.raises(ValueError):
        require_multiplier(Fraction(1, 100000))
    with pytest.raises(ValueError):
        require_multiplier(Fraction(10001))
    assert require_multiplier(Fraction(0), allow_zero=True) == 0
    assert require_multiplier(M_MIN) == M_MIN
    assert require_multiplier(M_MAX) == M_MAX


def test_multiple_roots_are_preserved_and_the_nominal_selects_one():
    grid = (Fraction(1, 10), Fraction(1), Fraction(10))
    values = [-1.0, 1.0, -1.0]

    def evaluate(multiplier: Fraction) -> float:
        log_value = math.log10(float(multiplier))
        if log_value <= 0.0:
            return -1.0 + 2.0 * (log_value + 1.0)
        return 1.0 - 2.0 * log_value

    roots = solve_roots(grid, values, 0.0, evaluate, 1e-8)
    assert len(roots) == 2
    assert all(root["accepted"] for root in roots)
    assert roots[0]["m_text"] != roots[1]["m_text"]


def test_deletion_is_preferred_when_the_nominal_grade_is_prohibit():
    book = _book(lambda multiplier: 0.0, lambda multiplier: 0.0, zero_forward=0.0, zero_reverse=0.0)
    result = calibrate_control(RULE, _target(0.0, 0.0), Fraction(0), book, 1e-8, 1e-8)
    forward = result["directions"]["path_to_matching"]
    assert forward["m_text"] == "0"
    assert forward["match_class"] == "zero-boundary solution"
    assert forward["matched"] is True
    assert forward["only_exact_solution_is_zero"] is False
    assert forward["root_count"] > 0
    assert all(root["role"] == "alternate" for root in forward["roots"])
    assert result["joint"]["m_text"] == "0"
    assert result["joint"]["matched"] is True
    assert result["joint"]["match_class"] == "zero-boundary solution"


def test_only_the_deletion_boundary_matches_when_no_finite_root_does():
    book = _book(lambda multiplier: 1.0, lambda multiplier: 1.0, zero_forward=0.0, zero_reverse=0.0)
    result = calibrate_control(RULE, _target(0.0, 0.0), Fraction(0), book, 1e-8, 1e-8)
    forward = result["directions"]["path_to_matching"]
    assert forward["m_text"] == "0"
    assert forward["only_exact_solution_is_zero"] is True
    assert forward["root_count"] == 0
    assert forward["matched"] is True


def test_an_unmatched_curve_is_not_a_finite_solution():
    book = _book(lambda multiplier: 1.0, lambda multiplier: 1.0, zero_forward=1.0, zero_reverse=1.0)
    result = calibrate_control(RULE, _target(0.0, 0.0), Fraction(1), book, 1e-8, 1e-8)
    assert result["directions"]["path_to_matching"]["matched"] is False
    assert result["directions"]["path_to_matching"]["match_class"] == "no finite solution"
    assert result["joint"]["matched"] is False


def test_forward_and_reverse_roots_are_recorded_separately():
    book = _book(
        lambda multiplier: math.log10(float(multiplier)),
        lambda multiplier: math.log10(float(multiplier)) - 1.0,
    )
    result = calibrate_control(RULE, _target(0.0, 0.0, 1.0, 1.0), Fraction(1), book, 1e-6, 1e-8)
    forward = parse_multiplier_text(result["directions"]["path_to_matching"]["m_text"])
    reverse = parse_multiplier_text(result["directions"]["matching_to_path"]["m_text"])
    assert result["directions"]["path_to_matching"]["matched"] is True
    assert result["directions"]["matching_to_path"]["matched"] is True
    assert abs(math.log10(float(forward))) < 1e-6
    assert abs(math.log10(float(reverse)) - 1.0) < 1e-6
    assert result["joint"]["matched"] is False
    joint = parse_multiplier_text(result["joint"]["m_text"])
    assert abs(math.log10(float(joint)) - 0.5) < 0.05


def test_a_touch_without_a_sign_change_is_recorded_as_a_residual_minimum():
    def touched(multiplier: Fraction) -> float:
        return (math.log10(float(multiplier)) - 0.3) ** 2

    book = _book(touched, touched, zero_forward=1.0, zero_reverse=1.0)
    result = calibrate_control(RULE, _target(0.0, 0.0, 1.0, 1.0), Fraction(1), book, 1e-8, 1e-8)
    row = result["directions"]["path_to_matching"]
    assert row["matched"] is True
    assert row["match_class"] == "finite solution"
    assert row["selection"] == "residual_minimum"
    assert row["roots"][0]["bracket"] == "residual_minimum"
    assert abs(math.log10(float(parse_multiplier_text(row["m_text"]))) - 0.3) < 1e-5
    assert row["absolute_mismatch"] <= 1e-8
    assert result["joint"]["matched"] is True


def test_joint_minimisation_on_a_toy_analytic_function():
    forward = [math.log10(float(multiplier)) for multiplier in POSITIVE_GRID]
    reverse = [math.log10(float(multiplier)) - 1.0 for multiplier in POSITIVE_GRID]
    scales = joint_scales(0.0, 0.0, 1.0, 1.0, 1e-8)
    assert scales["rule"] == "baseline_committor"

    def evaluate_pair(multiplier: Fraction):
        return (math.log10(float(multiplier)), math.log10(float(multiplier)) - 1.0)

    found = minimise_joint(POSITIVE_GRID, forward, reverse, 0.0, 0.0, scales, evaluate_pair, Fraction(1))
    assert found["locally_minimal"] is True
    assert abs(math.log10(float(found["selected"]["m"])) - 0.5) < 0.05
    distance = joint_distance(
        math.log10(float(found["selected"]["m"])),
        math.log10(float(found["selected"]["m"])) - 1.0,
        0.0,
        0.0,
        scales,
    )
    assert abs(distance - found["selected"]["distance"]) < 1e-9
    assert JOINT_DISTANCE_TIE == 1e-12


def test_interaction_margin_keeps_I_and_G_apart():
    target = {
        "I": -0.2,
        "G": 0.4,
        "delta_S": 0.01,
        "delta_TP": 0.3,
        "delta_T": 0.05,
        "delta_P": 0.04,
    }
    control = {
        "I": 0.5,
        "G": 0.9,
        "delta_S": 0.0,
        "delta_CP": 0.8,
        "delta_C": 0.05,
        "delta_P": 0.04,
    }
    numbers = _composition_numbers(target, control, 1e-8)
    assert numbers["M_I"] == pytest.approx(abs(target["I"]) - abs(control["I"]))
    assert numbers["M_G"] == pytest.approx(target["G"] - control["G"])
    assert numbers["M_I"] != numbers["M_G"]
    assert numbers["A_target"] == pytest.approx(abs(target["delta_TP"]) / max(abs(target["delta_T"]), abs(target["delta_P"])))
    assert numbers["A_ratio"] == pytest.approx(numbers["A_target"] / numbers["A_control"])


def test_state_shape_classes_use_the_predeclared_bands():
    mu = np.ones(16)
    flat = state_shape_report(np.zeros(16), mu, 4, 0.0, 0.01, 1e-8, 1e-8)
    assert flat["classification"] == "aggregate + approximately state-shape matched"
    assert flat["sign_pattern"] == "flat"
    mixed = np.zeros(16)
    mixed[0] = 0.2
    mixed[1] = -0.2
    poor = state_shape_report(mixed, mu, 4, 0.0, 0.01, 1e-8, 1e-8)
    assert poor["classification"] == "poorly state-shape matched"
    assert poor["sign_pattern"] == "mixed"
    unmatched = state_shape_report(np.full(16, 0.2), mu, 4, 0.2, 0.01, 1e-8, 1e-8)
    assert unmatched["classification"] == "not matched"


def test_predeclared_cells_keep_action_edge_polarity_and_companion():
    spec = _minimal_spec()
    catalogue = graded_catalogue(_catalogue_view(spec))
    with pytest.raises(ValueError, match="different analysis"):
        graded_catalogue(spec)
    records = selected_records(catalogue)
    assert len(records) == 28
    assert set(CELL_INDEX) == {(row["w_P"], row["w_T"]) for row in records}
    grammar = _grammar(WEIGHT_ORDER, 4)
    slots = grammar.slot_list()
    plan = coverage_plan(catalogue)
    assert plan["target_cells"] == 28
    assert plan["one_direction_root_solves"] == plan["joint_minimisations"] * 2
    assert plan["unique_erased_calibration_problems"] >= 1
    assert plan["unique_face_calibration_problems"] >= 1
    disjoint_geometries = set()
    for record in records:
        target, companion, controls = _live_controls(record, grammar, slots)
        assert companion.weight == record["w_P"]
        assert target.weight == record["w_T"]
        assert companion.action != target.action
        assert controls[0]["control_type"] == "erasure"
        assert controls[0]["rule"].conditions == ()
        for control in controls:
            assert control["rule"].action == target.action
            assert control["rule"].weight == CALIBRATION_WEIGHT
            assert control["rule"].polarity == DISSOLVE
            if control["control_type"] == "pair_face":
                assert control["relation"] in {"adjacent", "disjoint"}
                assert control["rule"].conditions
        if record["geometry"] == "contains_t_action_edge":
            assert all(control["relation"] != "disjoint" for control in controls)
        if any(control["relation"] == "disjoint" for control in controls):
            disjoint_geometries.add(record["geometry"])
        for face in record["faces"]:
            if face["relation_to_action"] == "same":
                assert face["status"] != "live"
    assert disjoint_geometries == {"contains_p_companion_edge"}
    with pytest.raises(IncompatibleGeneration, match="generation007"):
        build_plan(spec, 14)


def test_v07_spec_refuses_simplicial_semantics_and_nonzero_axes():
    spec = _minimal_spec()
    validate_spec(spec)
    _require_v07_spec(spec)
    assert spec["analysis"] == ANALYSIS_7
    assert spec["analysis_version"] == CALIBRATION_VERSION == "0.7.0"
    assert spec["G"] == spec["S"] == spec["H"] == spec["L"] == 0
    assert spec["O"] == 3
    assert spec["weights"] == list(WEIGHT_ORDER)
    assert CALIBRATION_WEIGHT not in spec["weights"]
    assert spec["match_tolerance"] == MATCH_TOLERANCE_DEFAULT
    assert spec["effect_floor"] == EFFECT_FLOOR_DEFAULT
    assert spec["joint_scale_floor"] == EFFECT_FLOOR_DEFAULT
    refused = dict(spec)
    refused["semantics"] = "simplicial"
    with pytest.raises(ValueError, match="simplicial"):
        validate_spec(refused)
    for axis in ("G", "S", "H", "L"):
        moved = dict(spec)
        moved[axis] = 1
        with pytest.raises(ValueError, match=axis):
            validate_spec(moved)
        with pytest.raises(ValueError):
            _require_v07_spec(moved)


def test_reference_kernels_agree_and_the_anchor_singleton_is_unchanged():
    report = numerical_reference()
    assert report["match_tolerance_decision"] == "keep_1e-8"
    assert report["worst_numerical_gap"] < 1e-10
    for name, gap in report["weight_gaps"].items():
        assert gap == 0.0, name
    for name, gap in report["landing_block_vs_dense"].items():
        assert gap < 1e-10, name
    for name, gap in report["committor_block_vs_dense"].items():
        assert gap < 1e-10, name
    for name, gap in report["committor_direct_vs_iterative"].items():
        assert gap < 1e-10, name
    assert report["anchor_singleton_versus_published_delta_T"] < 1e-12
    for row in report["unconditional_control_triad_spread"].values():
        for direction in DIRECTIONS:
            assert abs(row[direction]) < 1e-8


def test_relabelled_continuous_kernel_is_equivariant():
    assert relabelled_kernel_gap(Fraction(1, 4)) == 0.0


def test_generation7_monolithic_run_is_refused(tmp_path):
    spec = _minimal_spec(
        experiment_id="miniature-effect-matched-resume",
        rho3_sensitivity=["1"],
        sensitivity_alphabets=[],
    )
    path = tmp_path / "spec.json"
    path.write_text(json.dumps(spec), encoding="utf-8")
    code = main(["run", str(path), "--out", str(tmp_path / "out"), "--workers", "1", "--shard-items", "1", "--max-shards", "1"])
    assert code != 0
