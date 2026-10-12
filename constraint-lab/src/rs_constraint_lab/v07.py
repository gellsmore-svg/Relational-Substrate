"""Generation 7 effect-matched lower-order controls.

The higher-order singleton is a triad-gated dissolution. A lower-order
control keeps that action and replaces the named finite factor with a
positive multiplier ``m``, or with deletion at ``m = 0``. The multiplier is
an analysis parameter. It is not a new name in the permanent weight alphabet.

Calibration matches the controlled singleton committor. Composition is a
later comparison and is not used to choose ``m``.
"""

from __future__ import annotations

import hashlib
import math
import time
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import numpy as np

from rs_constraint_lab.constraints import DISSOLVE, Constraint, parse_expression, relabel_constraint
from rs_constraint_lab.durable import atomic_write_json, json_ready, read_json, sha256_file
from rs_constraint_lab.memory_clocks import epoch_kernel_block, epoch_kernel_float
from rs_constraint_lab.passage import eventual_committor, interaction_residual, kernel_layout_index, super_singleton_gap
from rs_constraint_lab.reconfiguration import RECONFIGURATION_HORIZON
from rs_constraint_lab.state import relation_slots, slot_permutation_maps
from rs_constraint_lab.v05 import (
    PRIMARY_RHO,
    _baseline_pack,
    _cached_direction,
    _constrained_pack,
    _direction_names,
    _grammar,
    _num,
    _release_landings,
    _support_violations,
    require_effect_floor,
)
from rs_constraint_lab.v06 import (
    ANALYSIS_VERSION as ANALYSIS_VERSION_6,
    WEIGHT_ORDER,
    _constraints_of,
    _roles,
    graded_catalogue,
)
from rs_constraint_lab.version import HYPERGRAPH_N4_SEMANTIC_VERSION
from rs_constraint_lab.weights import ENUMERATED_WEIGHTS, alphabet_factors

ANALYSIS_7 = "n4-effect-matched-controls"
ANALYSIS_VERSION = "0.7.0"
CALIBRATION_VERSION = "0.7.0"
CALIBRATION_WEIGHT = "continuous"
# Named alphabets stay W4/W3/W16. This token is only a kernel factor key.
if CALIBRATION_WEIGHT in ENUMERATED_WEIGHTS:
    raise RuntimeError("the calibration token collided with a named grade")

M_MIN = Fraction(1, 10000)
M_MAX = Fraction(10000)
# The empty choreography does not read factors. One key per rho keeps a
# single baseline object, so a continuous kernel can be shared across
# alphabets without failing the controlled-source identity check.
BASELINE_FACTORS = {"neutral": Fraction(1)}
GRID_DENOMINATOR = 4
GRID_DECADES = 8
# log10(m) = -4 + i/4 for i = 0..32. Endpoints are the domain bounds.
MATCH_TOLERANCE_DEFAULT = 1e-8
EFFECT_FLOOR_DEFAULT = 1e-8
JOINT_SCALE_FLOOR_DEFAULT = 1e-8
FLAT_SPAN_TOLERANCE = 1e-8
MONOTONE_DIFF_TOLERANCE = 1e-9
SIGN_FLOOR = 1e-8
BISECTION_STEPS = 60
BISECTION_LOG_WIDTH = 1e-12
GOLDEN_STEPS = 48
# Distances within this band are the same joint match. The tie breaks by
# log-distance to the nominal multiplier, and m = 0 wins that tie when the
# nominal grade is deletion. The band is not tuned to a scientific margin.
JOINT_DISTANCE_TIE = 1e-12
# Declared before any composed margin is read. They describe shape. They are
# not a score, and they are not the match tolerance.
STATE_SHAPE_ABS_BAND = 1e-4
STATE_SHAPE_RELATIVE = 0.05
AMPLIFICATION_FLOOR_USES = "effect_floor"

TARGET_CELLS = (
    ("prohibit", "prohibit", "anchor"),
    ("strong_suppress", "strong_suppress", "strong_suppress"),
    ("weak_suppress", "weak_suppress", "weak_suppress"),
    ("weak_favour", "weak_favour", "weak_favour"),
    ("strong_favour", "strong_favour", "strong_favour"),
    ("strong_suppress", "strong_favour", "opposite_suppress_favour"),
    ("strong_favour", "strong_suppress", "opposite_favour_suppress"),
)
CELL_INDEX = {(left, right): label for left, right, label in TARGET_CELLS}
ROBUSTNESS_CELLS = (
    ("contains_p_companion_edge", "absent", "prohibit", "prohibit"),
    ("contains_p_companion_edge", "absent", "strong_suppress", "strong_suppress"),
    ("contains_p_companion_edge", "absent", "strong_favour", "strong_favour"),
    ("contains_p_companion_edge", "absent", "strong_suppress", "strong_favour"),
    ("contains_t_action_edge", "absent", "prohibit", "prohibit"),
    ("contains_p_companion_edge", "present", "prohibit", "prohibit"),
)
CONTROL_ORDER = {"erasure": 0, "adjacent": 1, "disjoint": 2}
DIRECTIONS = ("path_to_matching", "matching_to_path")


def multiplier_text(value: Fraction) -> str:
    """Stable decimal key. The key is not a raw binary float dump."""
    if value == 0:
        return "0"
    decimal = Decimal(value.numerator) / Decimal(value.denominator)
    return format(decimal, ".12e")


def parse_multiplier_text(text: str) -> Fraction:
    if text == "0":
        return Fraction(0)
    return Fraction(Decimal(text))


def stabilise_multiplier(value: Fraction) -> Fraction:
    return parse_multiplier_text(multiplier_text(value))


def require_multiplier(value: Fraction, *, allow_zero: bool = False) -> Fraction:
    if value == 0:
        if allow_zero:
            return value
        raise ValueError("m = 0 is the deletion boundary and is not inside the positive domain")
    if value < M_MIN or value > M_MAX:
        raise ValueError(f"multiplier {value} is outside [{M_MIN}, {M_MAX}]")
    return value


def _grid_points() -> tuple[Fraction, ...]:
    """log10(m) = -4 + i/4 for i = 0..32. The endpoints are the domain bounds."""
    points = []
    start = -4 * GRID_DENOMINATOR
    for index in range(GRID_DECADES * GRID_DENOMINATOR + 1):
        whole, remainder = divmod(start + index, GRID_DENOMINATOR)
        magnitude = Decimal(10) ** whole
        if remainder:
            magnitude *= Decimal(10) ** (Decimal(remainder) / Decimal(GRID_DENOMINATOR))
        points.append(parse_multiplier_text(format(magnitude, ".12e")))
    points[0] = M_MIN
    points[-1] = M_MAX
    ordered = tuple(sorted(set(points)))
    if ordered[0] != M_MIN or ordered[-1] != M_MAX:
        raise RuntimeError("the calibration grid does not meet the declared domain")
    if any(right <= left for left, right in zip(ordered, ordered[1:])):
        raise RuntimeError("the calibration grid is not strictly increasing")
    return ordered


POSITIVE_GRID = _grid_points()
GRID_SHA256 = hashlib.sha256(
    "\n".join(multiplier_text(point) for point in POSITIVE_GRID).encode("utf-8")
).hexdigest()


def factors_for(alphabet: str, multiplier: Fraction | None) -> dict[str, Fraction]:
    factors = alphabet_factors(alphabet)
    if multiplier is None:
        return factors
    factors = dict(factors)
    factors[CALIBRATION_WEIGHT] = multiplier
    return factors


def with_multiplier(constraint: Constraint) -> Constraint:
    return Constraint(
        constraint.polarity,
        constraint.action,
        constraint.conditions,
        CALIBRATION_WEIGHT,
        constraint.counts,
    )


def nominal_multiplier(grade: str, alphabet: str = "W4") -> Fraction:
    return alphabet_factors(alphabet)[grade]


def log_distance(multiplier: Fraction, nominal: Fraction) -> float:
    """Distance used only to select among roots that are already recorded.

    A nominal of zero has no logarithm. Deletion is then closer than every
    positive multiplier, and positive candidates are ordered by ``m`` itself.
    """
    if nominal == 0:
        if multiplier == 0:
            return 0.0
        return float(multiplier) + 1e9
    if multiplier == 0:
        return float("inf")
    return abs(math.log(float(multiplier) / float(nominal)))


def classify_monotonicity(values: list[float]) -> dict:
    if len(values) < 2:
        raise ValueError("monotonicity needs at least two samples")
    span = max(values) - min(values)
    diffs = [right - left for left, right in zip(values, values[1:])]
    labels = []
    if span <= FLAT_SPAN_TOLERANCE:
        labels.append("flat")
    increasing = all(diff >= -MONOTONE_DIFF_TOLERANCE for diff in diffs)
    decreasing = all(diff <= MONOTONE_DIFF_TOLERANCE for diff in diffs)
    if "flat" not in labels:
        labels.append("monotone" if increasing or decreasing else "non-monotone")
    sign_changing = min(values) < -SIGN_FLOOR and max(values) > SIGN_FLOOR
    if sign_changing:
        labels.append("sign-changing")
    return {
        "labels": labels,
        "span": float(span),
        "sign_changing": sign_changing,
        "monotone": "monotone" in labels or "flat" in labels,
    }


def bracket_sign_changes(grid: tuple[Fraction, ...], values: list[float], target: float, tolerance: float) -> list[dict]:
    residual = [value - target for value in values]
    brackets = []
    for index, (left, right) in enumerate(zip(grid, grid[1:])):
        left_gap = residual[index]
        right_gap = residual[index + 1]
        if abs(left_gap) <= tolerance:
            brackets.append({"kind": "grid", "left": left, "right": left, "index": index})
        if left_gap * right_gap < 0.0:
            brackets.append({"kind": "sign_change", "left": left, "right": right, "index": index})
    if abs(residual[-1]) <= tolerance:
        brackets.append({"kind": "grid", "left": grid[-1], "right": grid[-1], "index": len(grid) - 1})
    return brackets


def _bisection(evaluate, left: Fraction, right: Fraction, target: float, tolerance: float) -> dict:
    """Safeguarded regula falsi in log10(m). A stalled interpolation bisects.

    Endpoint values come from the grid cache when the bracket is a grid
    step. Only the interior samples are new kernel solves.
    """
    lo = math.log10(float(left))
    hi = math.log10(float(right))
    f_lo = evaluate(left) - target
    f_hi = evaluate(right) - target
    if f_lo * f_hi > 0.0:
        raise RuntimeError("bisection was asked for a bracket that does not change sign")
    best_m = left if abs(f_lo) <= abs(f_hi) else right
    best_gap = f_lo if abs(f_lo) <= abs(f_hi) else f_hi
    for _step in range(BISECTION_STEPS):
        if hi - lo <= BISECTION_LOG_WIDTH or abs(best_gap) <= tolerance:
            break
        span = f_hi - f_lo
        if span == 0.0:
            mid_log = (lo + hi) / 2.0
        else:
            mid_log = lo - f_lo * (hi - lo) / span
        width = hi - lo
        if not lo < mid_log < hi or min(mid_log - lo, hi - mid_log) < 0.125 * width:
            mid_log = (lo + hi) / 2.0
        mid = require_multiplier(stabilise_multiplier(parse_multiplier_text(format(10 ** mid_log, ".12e"))))
        gap = evaluate(mid) - target
        if abs(gap) < abs(best_gap):
            best_m = mid
            best_gap = gap
        if abs(gap) <= tolerance:
            best_m = mid
            best_gap = gap
            break
        if f_lo * gap <= 0.0:
            hi = mid_log
            f_hi = gap
        else:
            lo = mid_log
            f_lo = gap
    confirmed = evaluate(best_m) - target
    return {
        "m": best_m,
        "m_text": multiplier_text(best_m),
        "solver_gap": float(best_gap),
        "confirmed_gap": float(confirmed),
        "absolute_mismatch": abs(float(confirmed)),
        "accepted": abs(float(confirmed)) <= tolerance,
    }


def minimise_absolute(grid, values, target: float, evaluate) -> dict:
    """Smallest |Delta(m) - target| on the log grid, polished in log space.

    A non-monotone curve can meet the tolerance at a turning point without
    changing sign. Sign-change brackets do not see that point.
    """
    gaps = [abs(value - target) for value in values]
    valleys = []
    for index, gap in enumerate(gaps):
        left = gaps[index - 1] if index else gap
        right = gaps[index + 1] if index + 1 < len(gaps) else gap
        if gap <= left and gap <= right:
            valleys.append(index)
    best = None
    for index in valleys:
        lower = grid[max(0, index - 1)]
        upper = grid[min(len(grid) - 1, index + 1)]
        if lower == upper:
            multiplier = grid[index]
            gap = abs(evaluate(multiplier) - target)
        else:
            def objective(log_value: float, _lower=lower, _upper=upper) -> float:
                multiplier = require_multiplier(
                    stabilise_multiplier(parse_multiplier_text(format(10 ** log_value, ".12e")))
                )
                return abs(evaluate(multiplier) - target)

            _log_best, _gap = _golden(objective, math.log10(float(lower)), math.log10(float(upper)))
            multiplier = require_multiplier(
                stabilise_multiplier(parse_multiplier_text(format(10 ** _log_best, ".12e")))
            )
            gap = abs(evaluate(multiplier) - target)
        row = {"m": multiplier, "m_text": multiplier_text(multiplier), "absolute_mismatch": float(gap)}
        if best is None or row["absolute_mismatch"] < best["absolute_mismatch"]:
            best = row
    return best


def solve_roots(grid, values, target: float, evaluate, tolerance: float) -> list[dict]:
    found = []
    seen = set()
    for bracket in bracket_sign_changes(grid, values, target, tolerance):
        if bracket["kind"] == "grid":
            solved = {
                "m": bracket["left"],
                "m_text": multiplier_text(bracket["left"]),
                "solver_gap": float(values[bracket["index"]] - target),
                "confirmed_gap": float(evaluate(bracket["left"]) - target),
                "absolute_mismatch": abs(float(evaluate(bracket["left"]) - target)),
                "accepted": True,
            }
        else:
            solved = _bisection(evaluate, bracket["left"], bracket["right"], target, tolerance)
        if solved["m_text"] in seen:
            continue
        seen.add(solved["m_text"])
        solved["bracket"] = bracket["kind"]
        found.append(solved)
    return found


def select_root(roots: list[dict], nominal: Fraction, *, flat: bool, flat_matches: bool) -> dict | None:
    """Closest accepted root to the nominal multiplier. Every root stays listed.

    A flat curve that stays inside tolerance selects the nominal multiplier
    when that multiplier is inside the positive domain. It does not invent a
    distinguished dynamical root.
    """
    accepted = [root for root in roots if root["accepted"]]
    if flat and flat_matches and nominal > 0 and M_MIN <= nominal <= M_MAX:
        return {
            "m": nominal,
            "m_text": multiplier_text(nominal),
            "absolute_mismatch": None,
            "selection": "flat_nominal",
            "accepted": True,
        }
    if not accepted:
        return None
    return min(accepted, key=lambda root: (log_distance(root["m"], nominal), multiplier_text(root["m"])))


def joint_scales(delta_forward: float, delta_reverse: float, q0_forward: float, q0_reverse: float, scale_floor: float) -> dict:
    """Scales are functions of the target only. They are not adjusted to the control."""
    if max(abs(delta_forward), abs(delta_reverse)) < scale_floor:
        return {
            "forward": max(abs(q0_forward), scale_floor),
            "reverse": max(abs(q0_reverse), scale_floor),
            "rule": "baseline_committor",
        }
    return {
        "forward": max(abs(delta_forward), scale_floor),
        "reverse": max(abs(delta_reverse), scale_floor),
        "rule": "target_effect",
    }


def joint_distance(delta_forward: float, delta_reverse: float, target_forward: float, target_reverse: float, scales: dict) -> float:
    forward = (delta_forward - target_forward) / scales["forward"]
    reverse = (delta_reverse - target_reverse) / scales["reverse"]
    return float(math.sqrt(forward * forward + reverse * reverse))


def _golden(objective, log_left: float, log_right: float) -> tuple[float, float]:
    ratio = (math.sqrt(5.0) - 1.0) / 2.0
    left = log_left
    right = log_right
    probe_left = right - ratio * (right - left)
    probe_right = left + ratio * (right - left)
    value_left = objective(probe_left)
    value_right = objective(probe_right)
    for _step in range(GOLDEN_STEPS):
        # A log10 width of 1e-7 is a relative multiplier change near 2e-7.
        # Steep singleton curves in the preflight moved the committor by
        # more than the match tolerance across a wider bracket.
        if right - left <= 1e-7:
            break
        if value_left < value_right:
            right = probe_right
            probe_right = probe_left
            value_right = value_left
            probe_left = right - ratio * (right - left)
            value_left = objective(probe_left)
        else:
            left = probe_left
            probe_left = probe_right
            value_left = value_right
            probe_right = left + ratio * (right - left)
            value_right = objective(probe_right)
    if value_left <= value_right:
        return probe_left, value_left
    return probe_right, value_right


def minimise_joint(grid, forward_values, reverse_values, target_forward, target_reverse, scales, evaluate_pair, nominal: Fraction) -> dict:
    """Grid local minima, polished in log space. Stochastic search is not used."""
    distances = [
        joint_distance(left, right, target_forward, target_reverse, scales)
        for left, right in zip(forward_values, reverse_values)
    ]
    valleys = []
    for index, distance in enumerate(distances):
        left = distances[index - 1] if index else distance
        right = distances[index + 1] if index + 1 < len(distances) else distance
        if distance <= left and distance <= right:
            valleys.append(index)
    if not valleys:
        valleys = [min(range(len(distances)), key=distances.__getitem__)]
    polished = []
    for index in valleys:
        lower = grid[max(0, index - 1)]
        upper = grid[min(len(grid) - 1, index + 1)]
        if lower == upper:
            multiplier = grid[index]
            pair = evaluate_pair(multiplier)
            distance = joint_distance(pair[0], pair[1], target_forward, target_reverse, scales)
        else:
            def objective(log_value: float, _lower=lower, _upper=upper) -> float:
                multiplier = require_multiplier(
                    stabilise_multiplier(parse_multiplier_text(format(10 ** log_value, ".12e")))
                )
                pair = evaluate_pair(multiplier)
                return joint_distance(pair[0], pair[1], target_forward, target_reverse, scales)

            log_best, distance = _golden(objective, math.log10(float(lower)), math.log10(float(upper)))
            multiplier = require_multiplier(
                stabilise_multiplier(parse_multiplier_text(format(10 ** log_best, ".12e")))
            )
            pair = evaluate_pair(multiplier)
            distance = joint_distance(pair[0], pair[1], target_forward, target_reverse, scales)
        polished.append({"m": multiplier, "m_text": multiplier_text(multiplier), "distance": float(distance), "deltas": pair})
    best = min(polished, key=lambda row: (row["distance"], log_distance(row["m"], nominal), row["m_text"]))
    log_best = math.log10(float(best["m"]))
    neighbours = []
    for shift in (-0.01, 0.01):
        probe_log = log_best + shift
        if probe_log < math.log10(float(M_MIN)) or probe_log > math.log10(float(M_MAX)):
            continue
        probe = require_multiplier(stabilise_multiplier(parse_multiplier_text(format(10 ** probe_log, ".12e"))))
        pair = evaluate_pair(probe)
        neighbours.append(joint_distance(pair[0], pair[1], target_forward, target_reverse, scales))
    locally_minimal = all(best["distance"] <= neighbour + 1e-12 for neighbour in neighbours)
    boundary = None
    if best["m"] == M_MIN:
        boundary = "lower-bound"
    elif best["m"] == M_MAX:
        boundary = "upper-bound"
    return {
        "candidates": [
            {"m_text": row["m_text"], "distance": row["distance"]}
            for row in sorted(polished, key=lambda item: item["distance"])
        ],
        "selected": best,
        "local_valley_count": len(valleys),
        "locally_minimal": locally_minimal,
        "boundary_status": boundary,
    }


def _minimal_spec(**overrides) -> dict:
    spec = {
        "schema": "rs-constraint-lab.experiment/v1",
        "experiment_id": "generation-007-effect-matched-controls",
        "generation": 7,
        "semantics": "hypergraph",
        "G": 0,
        "S": 0,
        "H": 0,
        "L": 0,
        "O": 3,
        "alphabet": "W4",
        "composition": "structural-simple",
        "analysis": ANALYSIS_7,
        "analysis_version": ANALYSIS_VERSION,
        "calibration_version": CALIBRATION_VERSION,
        "predicates": ["pair", "triad"],
        "weights": list(WEIGHT_ORDER),
        "cells": [{"N": 4, "K_max": 2, "A_max": 4, "cardinalities": [2]}],
        "reconfiguration_horizon": 16,
        "effect_floor": EFFECT_FLOOR_DEFAULT,
        "match_tolerance": MATCH_TOLERANCE_DEFAULT,
        "joint_scale_floor": JOINT_SCALE_FLOOR_DEFAULT,
        "sensitivity_alphabets": ["W3", "W16"],
        "rho3_sensitivity": ["1/2", "1", "2"],
        "focused_transition": ["e2-deg2110-tri0-comp2", "e2-deg1111-tri0-comp2"],
    }
    spec.update(overrides)
    return spec


def _require_v07_spec(spec: dict) -> None:
    if spec.get("analysis") != ANALYSIS_7:
        raise ValueError("generation 7 analysis is n4-effect-matched-controls")
    if spec.get("analysis_version") != ANALYSIS_VERSION:
        raise ValueError("generation 7 analysis version is 0.7.0")
    if spec.get("calibration_version") != CALIBRATION_VERSION:
        raise ValueError("generation 7 calibration version is 0.7.0")
    if int(spec["G"]) or int(spec["S"]) or int(spec["H"]) or int(spec["L"]):
        raise ValueError("generation 7 keeps G = S = H = L = 0")
    if int(spec["O"]) != 3:
        raise ValueError("generation 7 keeps O = 3")
    if spec.get("semantics") != "hypergraph":
        raise ValueError("generation 7 keeps the independent hypergraph")
    if list(spec.get("weights", [])) != list(WEIGHT_ORDER):
        raise ValueError("generation 7 does not enlarge the named weight alphabet")
    if float(spec.get("match_tolerance", 0.0)) <= 0.0:
        raise ValueError("match_tolerance must be declared and positive")
    if float(spec.get("joint_scale_floor", 0.0)) <= 0.0:
        raise ValueError("joint_scale_floor must be declared and positive")
    cell = spec["cells"][0]
    if int(cell["N"]) != 4 or list(cell["cardinalities"]) != [2]:
        raise ValueError("generation 7 stays at N = 4 and cardinality 2")


def _catalogue_view(spec: dict) -> dict:
    """Read the historical Generation 6 catalogue without retargeting it.

    The catalogue refuses any analysis name other than its own. Generation 7
    does not edit that gate. It passes a view whose analysis fields are the
    Generation 6 names. Target ids do not include the caller spec hash.
    """
    viewed = dict(spec)
    viewed["analysis"] = "n4-graded-matched-controls"
    viewed["analysis_version"] = ANALYSIS_VERSION_6
    return viewed


def selected_records(catalogue: dict) -> list[dict]:
    rows = [row for row in catalogue["records"] if (row["w_P"], row["w_T"]) in CELL_INDEX]
    rows.sort(
        key=lambda row: (
            row["geometry"],
            row["polarity"],
            WEIGHT_ORDER.index(row["w_P"]),
            WEIGHT_ORDER.index(row["w_T"]),
            row["target_id"],
        )
    )
    if len(rows) != 4 * len(TARGET_CELLS):
        raise RuntimeError(f"predeclared cells produced {len(rows)} targets, not {4 * len(TARGET_CELLS)}")
    return rows


def _live_controls(record: dict, grammar, slots) -> list[dict]:
    members = _constraints_of(grammar, record["canonical_ids"])
    t_rule, p_rule = _roles(members, slots)
    if t_rule.weight != record["w_T"] or p_rule.weight != record["w_P"]:
        raise RuntimeError("target roles drifted from the recorded grades")
    controls = [
        {
            "control_type": "erasure",
            "relation": "unconditional",
            "face": None,
            "rule": with_multiplier(Constraint(DISSOLVE, t_rule.action, (), t_rule.weight, ())),
            "named_rule": Constraint(DISSOLVE, t_rule.action, (), t_rule.weight, ()),
        }
    ]
    for face in record["faces"]:
        if face["status"] != "live" or face.get("duplicate_of_earlier_face"):
            continue
        gated_text = next(text for text in face["expressions"] if " | " in text)
        parsed = parse_expression(gated_text, 4, order=3)
        if parsed.action != t_rule.action:
            raise RuntimeError("a pair-face control changed the action edge")
        if parsed.conditions != tuple() and ("present" if parsed.conditions[0][1] else "absent") != record["polarity"]:
            raise RuntimeError("a pair-face control changed polarity")
        if face["relation_to_action"] not in {"adjacent", "disjoint"}:
            raise RuntimeError("a live face is not adjacent or disjoint")
        controls.append(
            {
                "control_type": "pair_face",
                "relation": face["relation_to_action"],
                "face": face["face"],
                "control_id": face["control_id"],
                "rule": with_multiplier(parsed),
                "named_rule": parsed,
            }
        )
    controls.sort(key=_control_sort_key)
    return t_rule, p_rule, controls


def _control_sort_key(row: dict) -> tuple:
    """Erasure, then adjacent faces, then disjoint faces. Same-as-action faces are absent."""
    rank = {"unconditional": 0, "adjacent": 1, "disjoint": 2}[row["relation"]]
    face = row["face"]
    return (rank, "" if face is None else str(face))


def coverage_plan(catalogue: dict) -> dict:
    grammar = _grammar(WEIGHT_ORDER, 4)
    slots = grammar.slot_list()
    records = selected_records(catalogue)
    erased = set()
    faces = set()
    target_singletons = set()
    one_direction = 0
    joint = 0
    for record in records:
        t_rule, _p_rule, controls = _live_controls(record, grammar, slots)
        target_singletons.add(t_rule.key())
        for control in controls:
            key = (control["rule"].structural_key(), t_rule.key())
            if control["control_type"] == "erasure":
                erased.add(key)
            else:
                faces.add(key)
            one_direction += 2
            joint += 1
    structures = {control_key[0] for control_key in erased | faces}
    grid_evals = len(structures) * (len(POSITIVE_GRID) + 1)
    return {
        "target_cells": len(records),
        "geometries": sorted({row["geometry"] for row in records}),
        "polarities": sorted({row["polarity"] for row in records}),
        "unique_target_singletons": len(target_singletons),
        "unique_erased_calibration_problems": len(erased),
        "unique_face_calibration_problems": len(faces),
        "unique_control_structures": len(structures),
        "one_direction_root_solves": one_direction,
        "joint_minimisations": joint,
        "grid_points": len(POSITIVE_GRID),
        "expected_grid_kernel_evaluations": grid_evals,
        "expected_target_singleton_evaluations": len(target_singletons),
        "grid_sha256": GRID_SHA256,
    }


class EffectBook:
    """Kernel cache keyed by structure, multiplier text, rho, and alphabet."""

    def __init__(self, slots, cache: dict, alphabet: str, rho: Fraction):
        self.slots = slots
        self.cache = cache
        self.alphabet = alphabet
        self.rho = rho
        self.curves: dict = {}
        self.evaluations = 0

    def baseline(self):
        return _baseline_pack(BASELINE_FACTORS, self.rho, self.slots, self.cache)

    def _solve_rule(self, rule: Constraint, multiplier: Fraction) -> dict:
        require_multiplier(multiplier, allow_zero=True)
        if rule.weight == CALIBRATION_WEIGHT:
            factors = {CALIBRATION_WEIGHT: multiplier}
        else:
            factors = factors_for(self.alphabet, None)
        baseline = self.baseline()
        pack = _constrained_pack((rule,), factors, self.rho, self.slots, self.cache)
        self.evaluations += 1
        table = baseline["table"]
        out = {}
        for key, source_name, target_name in _direction_names(table):
            solved = _cached_direction(pack, baseline, source_name, target_name, RECONFIGURATION_HORIZON)
            base = _cached_direction(baseline, baseline, source_name, target_name, RECONFIGURATION_HORIZON)
            q = solved["q_controlled"]
            q0 = base["q_controlled"]
            out[key] = {
                "delta": None if q is None or q0 is None else float(q - q0),
                "Q": None if q is None else float(q),
                "Q0": None if q0 is None else float(q0),
                "spread": None if solved["triad"].get("spread") is None else float(solved["triad"]["spread"]),
                "residual": float(solved["solver"]["residual"] or 0.0),
                "q": solved["q"],
                "q0": base["q"],
                "mu": base["mu_ref"],
            }
        _release_landings(self.cache)
        return out

    def curve(self, rule: Constraint) -> dict:
        key = rule.structural_key()
        cached = self.curves.get(key)
        if cached is not None:
            return cached
        points = {}
        for multiplier in POSITIVE_GRID:
            points[multiplier_text(multiplier)] = self._solve_rule(rule, multiplier)
        zero = self._solve_rule(rule, Fraction(0))
        stored = {"points": points, "zero": zero, "structure": key}
        self.curves[key] = stored
        return stored

    def evaluate(self, rule: Constraint, multiplier: Fraction) -> dict:
        stored = self.curve(rule)
        if multiplier == 0:
            return stored["zero"]
        text = multiplier_text(require_multiplier(multiplier))
        point = stored["points"].get(text)
        if point is None:
            point = self._solve_rule(rule, parse_multiplier_text(text))
            stored["points"][text] = point
        return point


def _series(curve: dict, direction: str) -> tuple[list[Fraction], list[float]]:
    grid = list(POSITIVE_GRID)
    values = [curve["points"][multiplier_text(multiplier)][direction]["delta"] for multiplier in grid]
    return grid, values


def _boundary_of(grid, values, target: float) -> str | None:
    gaps = [abs(value - target) for value in values]
    index = min(range(len(gaps)), key=gaps.__getitem__)
    if index == 0:
        return "lower-bound"
    if index == len(grid) - 1:
        return "upper-bound"
    return None


def calibrate_control(rule: Constraint, target_effects: dict, nominal: Fraction, book: EffectBook, tolerance: float, scale_floor: float, stage: str = "all") -> dict:
    curve = book.curve(rule)
    scales = joint_scales(
        target_effects["path_to_matching"]["delta"],
        target_effects["matching_to_path"]["delta"],
        target_effects["path_to_matching"]["Q0"],
        target_effects["matching_to_path"]["Q0"],
        scale_floor,
    )
    directions = {}
    for direction in DIRECTIONS:
        grid, values = _series(curve, direction)
        target = target_effects[direction]["delta"]
        monotonicity = classify_monotonicity(values)
        evaluate = lambda multiplier, _direction=direction: book.evaluate(rule, multiplier)[_direction]["delta"]
        roots = solve_roots(tuple(grid), values, target, evaluate, tolerance)
        # A turning point can meet the tolerance without a sign change.
        # Search that valley only after bracketing has found nothing.
        if not any(root["accepted"] for root in roots):
            closest = minimise_absolute(tuple(grid), values, target, evaluate)
            if closest is not None and closest["absolute_mismatch"] <= tolerance:
                confirmed = evaluate(closest["m"]) - target
                roots.append(
                    {
                        "m": closest["m"],
                        "m_text": closest["m_text"],
                        "solver_gap": closest["absolute_mismatch"],
                        "confirmed_gap": float(confirmed),
                        "absolute_mismatch": abs(float(confirmed)),
                        "accepted": abs(float(confirmed)) <= tolerance,
                        "bracket": "residual_minimum",
                        "selection": "residual_minimum",
                    }
                )
        zero = book.evaluate(rule, Fraction(0))[direction]
        zero_gap = abs(zero["delta"] - target)
        zero_match = zero_gap <= tolerance
        flat_nominal_gap = None
        flat_matches = False
        if "flat" in monotonicity["labels"] and nominal > 0:
            flat_nominal_gap = abs(evaluate(require_multiplier(stabilise_multiplier(nominal))) - target)
            flat_matches = flat_nominal_gap <= tolerance
        selected = select_root(roots, nominal, flat="flat" in monotonicity["labels"], flat_matches=flat_matches)
        if selected is not None and selected.get("selection") == "flat_nominal":
            selected["absolute_mismatch"] = flat_nominal_gap
            selected["confirmed_gap"] = evaluate(selected["m"]) - target
        accepted_finite = any(root["accepted"] for root in roots)
        only_zero = False
        zero_claim = {
            "m": Fraction(0),
            "m_text": "0",
            "absolute_mismatch": zero_gap,
            "confirmed_gap": zero["delta"] - target,
            "selection": "zero_boundary",
            "accepted": True,
        }
        # Nominal deletion prefers m = 0 whenever deletion meets the tolerance,
        # even if a finite root also meets it. Those finite roots stay listed
        # as alternates. only_exact_solution_is_zero is true only when no
        # finite accepted root exists.
        if nominal == 0 and zero_match:
            selected = dict(zero_claim)
            match_class = "zero-boundary solution"
            only_zero = not accepted_finite and not flat_matches
        elif selected is None and zero_match:
            selected = dict(zero_claim)
            match_class = "zero-boundary solution"
            only_zero = not accepted_finite and not flat_matches
        elif selected is None:
            match_class = "no finite solution"
        elif selected.get("selection") == "zero_boundary" or selected["m"] == 0:
            match_class = "zero-boundary solution"
            only_zero = not accepted_finite and not flat_matches
        elif selected["accepted"]:
            match_class = "finite solution"
        else:
            match_class = "unresolved"
        if selected is not None and selected["m"] != 0:
            confirmed = book.evaluate(rule, selected["m"])[direction]
            selected["absolute_mismatch"] = abs(confirmed["delta"] - target)
            selected["confirmed_gap"] = confirmed["delta"] - target
            selected["rechecked_delta"] = confirmed["delta"]
            if selected["absolute_mismatch"] > tolerance:
                match_class = "unresolved"
                selected["accepted"] = False
        relative = None
        if selected is not None and selected.get("absolute_mismatch") is not None:
            relative = selected["absolute_mismatch"] / max(abs(target), scale_floor)
        if match_class == "zero-boundary solution":
            boundary = "zero-boundary"
        elif selected is not None and selected["m"] == M_MIN:
            boundary = "lower-bound"
        elif selected is not None and selected["m"] == M_MAX:
            boundary = "upper-bound"
        elif match_class == "finite solution":
            boundary = None
        else:
            boundary = _boundary_of(grid, values, target)
        selected_text = None if selected is None else selected["m_text"]
        directions[direction] = {
            "m_text": None if selected is None else selected["m_text"],
            "absolute_mismatch": None if selected is None else selected.get("absolute_mismatch"),
            "relative_mismatch": relative,
            "solver_residual": None if selected is None else selected.get("confirmed_gap"),
            "match_class": match_class,
            "matched": match_class in {"finite solution", "zero-boundary solution"}
            and selected is not None
            and selected.get("absolute_mismatch") is not None
            and selected["absolute_mismatch"] <= tolerance,
            "root_count": sum(1 for root in roots if root["accepted"]),
            "roots": [
                {
                    "m_text": root["m_text"],
                    "absolute_mismatch": root["absolute_mismatch"],
                    "accepted": root["accepted"],
                    "bracket": root["bracket"],
                    "role": "selected" if root["m_text"] == selected_text else "alternate",
                }
                for root in roots
            ],
            "monotonicity": monotonicity["labels"],
            "boundary_status": boundary,
            "zero_absolute_mismatch": zero_gap,
            "zero_matches": zero_match,
            "only_exact_solution_is_zero": only_zero,
            "selection": None if selected is None else selected.get("selection", "closest_log_nominal"),
        }
    if stage == "directions":
        return {"directions": directions, "joint": None}
    if stage != "all":
        raise ValueError(f"unknown calibration stage {stage}")

    def evaluate_pair(multiplier: Fraction) -> tuple[float, float]:
        solved = book.evaluate(rule, multiplier)
        return (
            solved["path_to_matching"]["delta"],
            solved["matching_to_path"]["delta"],
        )

    grid, forward_values = _series(curve, "path_to_matching")
    _grid, reverse_values = _series(curve, "matching_to_path")
    polished = minimise_joint(
        grid,
        forward_values,
        reverse_values,
        target_effects["path_to_matching"]["delta"],
        target_effects["matching_to_path"]["delta"],
        scales,
        evaluate_pair,
        nominal,
    )
    zero_pair = evaluate_pair(Fraction(0))
    zero_distance = joint_distance(
        zero_pair[0],
        zero_pair[1],
        target_effects["path_to_matching"]["delta"],
        target_effects["matching_to_path"]["delta"],
        scales,
    )
    chosen = polished["selected"]
    # One-direction roots are already solved. A joint grid can miss a sharp
    # well between quarter-decade samples, so those roots are candidates too.
    scored = [chosen]
    seen = {chosen["m_text"]}
    for row in directions.values():
        texts = [root["m_text"] for root in row["roots"] if root["accepted"]]
        if row["matched"] and row["m_text"]:
            texts.append(row["m_text"])
        for text in texts:
            if text in seen or text == "0":
                continue
            seen.add(text)
            multiplier = parse_multiplier_text(text)
            pair = evaluate_pair(multiplier)
            scored.append(
                {
                    "m": multiplier,
                    "m_text": text,
                    "distance": joint_distance(
                        pair[0],
                        pair[1],
                        target_effects["path_to_matching"]["delta"],
                        target_effects["matching_to_path"]["delta"],
                        scales,
                    ),
                    "deltas": pair,
                }
            )
    chosen = min(scored, key=lambda row: (row["distance"], log_distance(row["m"], nominal), row["m_text"]))
    selected_from = "grid_polish" if chosen["m_text"] == polished["selected"]["m_text"] else "one_direction_root"
    boundary = "lower-bound" if chosen["m"] == M_MIN else "upper-bound" if chosen["m"] == M_MAX else None
    zero_choice = {
        "m": Fraction(0),
        "m_text": "0",
        "distance": zero_distance,
        "deltas": zero_pair,
    }
    distance_gap = chosen["distance"] - zero_distance
    zero_closer = log_distance(Fraction(0), nominal) < log_distance(chosen["m"], nominal)
    if distance_gap > JOINT_DISTANCE_TIE or (abs(distance_gap) <= JOINT_DISTANCE_TIE and zero_closer):
        chosen = zero_choice
        boundary = "zero-boundary"
        selected_from = "zero_boundary"
    confirmed_pair = evaluate_pair(chosen["m"])
    mismatches = {
        "path_to_matching": abs(confirmed_pair[0] - target_effects["path_to_matching"]["delta"]),
        "matching_to_path": abs(confirmed_pair[1] - target_effects["matching_to_path"]["delta"]),
    }
    distance = joint_distance(
        confirmed_pair[0],
        confirmed_pair[1],
        target_effects["path_to_matching"]["delta"],
        target_effects["matching_to_path"]["delta"],
        scales,
    )
    joint_matched = all(gap <= tolerance for gap in mismatches.values())
    if chosen["m"] == 0 and joint_matched:
        joint_class = "zero-boundary solution"
    elif joint_matched:
        joint_class = "finite solution"
    elif boundary not in {"lower-bound", "upper-bound", "zero-boundary"} and not polished["locally_minimal"]:
        joint_class = "unresolved"
    else:
        joint_class = "no finite solution"
    return {
        "directions": directions,
        "joint": {
            "m_text": chosen["m_text"],
            "distance": distance,
            "absolute_mismatch": mismatches,
            "scales": scales,
            "match_class": joint_class,
            "matched": joint_matched,
            "boundary_status": boundary,
            "local_valley_count": polished["local_valley_count"],
            "locally_minimal": polished["locally_minimal"],
            "candidate_count": len(polished["candidates"]),
            "selected_from": selected_from,
            "solver_residual": distance,
            "zero_distance": zero_distance,
        },
    }


def _named_factors(factors: dict) -> dict:
    """Drop the calibration token. Baseline and the companion rule do not read it."""
    return {key: value for key, value in factors.items() if key != CALIBRATION_WEIGHT}


def _pack_directions(c_rule, p_rule, factors, rho, slots, cache, floor: float) -> dict:
    del floor
    named = _named_factors(factors)
    if c_rule.weight == CALIBRATION_WEIGHT:
        # The singleton curve is alphabet-independent. The pair still needs
        # the companion's named factor, so the composed pack keeps both.
        c_factors = {CALIBRATION_WEIGHT: factors[CALIBRATION_WEIGHT]}
        cp_factors = dict(named)
        cp_factors[CALIBRATION_WEIGHT] = factors[CALIBRATION_WEIGHT]
    else:
        c_factors = named
        cp_factors = named
    baseline = _baseline_pack(BASELINE_FACTORS, rho, slots, cache)
    packs = {
        "0": baseline,
        "C": _constrained_pack((c_rule,), c_factors, rho, slots, cache),
        "P": _constrained_pack((p_rule,), named, rho, slots, cache),
        "CP": _constrained_pack((c_rule, p_rule), cp_factors, rho, slots, cache),
    }
    table = baseline["table"]
    out = {}
    for key, source_name, target_name in _direction_names(table):
        solved = {
            label: _cached_direction(pack, baseline, source_name, target_name, RECONFIGURATION_HORIZON)
            for label, pack in packs.items()
        }
        q0 = solved["0"]["q_controlled"]
        qc = solved["C"]["q_controlled"]
        qp = solved["P"]["q_controlled"]
        qcp = solved["CP"]["q_controlled"]
        delta_c = float(qc - q0)
        delta_p = float(qp - q0)
        delta_cp = float(qcp - q0)
        spread_c = solved["C"]["triad"].get("spread")
        spread_cp = solved["CP"]["triad"].get("spread")
        out[key] = {
            "Q0": float(q0),
            "QC": float(qc),
            "QP": float(qp),
            "QCP": float(qcp),
            "delta_C": delta_c,
            "delta_P": delta_p,
            "delta_CP": delta_cp,
            "I": interaction_residual(qcp, qc, qp, q0),
            "G": super_singleton_gap(delta_cp, delta_c, delta_p),
            "delta_S": None if spread_c is None or spread_cp is None else float(spread_cp - spread_c),
            "S_C": None if spread_c is None else float(spread_c),
            "S_CP": None if spread_cp is None else float(spread_cp),
            "q": solved["C"]["q"],
            "q0": solved["0"]["q"],
            "mu": solved["0"]["mu_ref"],
            "source_name": source_name,
        }
    violations = _support_violations(packs["CP"]["kernel"], packs["C"]["kernel"])
    violations += _support_violations(packs["CP"]["kernel"], packs["P"]["kernel"])
    removed = _support_violations(packs["0"]["kernel"], packs["CP"]["kernel"])
    _release_landings(cache)
    return {"directions": out, "support_violations": violations, "support_removed": removed, "baseline_q0_id": id(baseline["mu_ref"])}


def state_shape_report(
    error: np.ndarray,
    mu: np.ndarray,
    n_pairs: int,
    aggregate: float,
    delta_target: float,
    effect_floor: float,
    match_tolerance: float | None = None,
) -> dict:
    defined = np.isfinite(error) & (mu > 0.0)
    if not np.any(defined):
        return {"defined": False, "classification": "undefined"}
    values = error[defined]
    mean = float(np.average(values, weights=mu[defined]))
    max_abs = float(np.max(np.abs(values)))
    positive = int(np.sum(values > effect_floor))
    negative = int(np.sum(values < -effect_floor))
    if positive and negative:
        sign_pattern = "mixed"
        sign = "mixed"
    elif positive:
        sign_pattern = "one_sign"
        sign = "positive"
    elif negative:
        sign_pattern = "one_sign"
        sign = "negative"
    else:
        sign_pattern = "flat"
        sign = "none"
    triad_means = []
    n_triads = error.shape[0] >> n_pairs
    span = 1 << n_pairs
    for triad in range(n_triads):
        window = slice(triad << n_pairs, (triad << n_pairs) + span)
        mask = defined[window]
        if not np.any(mask):
            continue
        local = error[window][mask]
        weight = mu[window][mask]
        triad_means.append(float(np.average(local, weights=weight)))
    triad_mismatch = None if not triad_means else float(max(abs(value) for value in triad_means))
    triad_sign = "undefined"
    if triad_means:
        if min(triad_means) < -effect_floor and max(triad_means) > effect_floor:
            triad_sign = "mixed"
        elif max(abs(value) for value in triad_means) <= effect_floor:
            triad_sign = "flat"
        elif max(triad_means) > effect_floor:
            triad_sign = "one_sign"
        else:
            triad_sign = "one_sign"
    scale = max(abs(delta_target), effect_floor)
    approximately = max_abs <= STATE_SHAPE_ABS_BAND or max_abs <= STATE_SHAPE_RELATIVE * scale
    severe = (
        max_abs > max(STATE_SHAPE_ABS_BAND, 10.0 * max(abs(aggregate), effect_floor))
        and max_abs > STATE_SHAPE_RELATIVE * scale
    )
    mixed_severe = sign_pattern == "mixed" and max_abs > STATE_SHAPE_ABS_BAND
    if match_tolerance is not None and abs(aggregate) > match_tolerance:
        classification = "not matched"
    elif severe or mixed_severe:
        classification = "poorly state-shape matched"
    elif approximately:
        classification = "aggregate + approximately state-shape matched"
    else:
        classification = "aggregate-only matched"
    return {
        "defined": True,
        "mean": mean,
        "max_abs": max_abs,
        "aggregate_mismatch": float(aggregate),
        "sign_pattern": sign_pattern,
        "sign": sign,
        "triad_bucket_mismatch": triad_mismatch,
        "triad_sign_pattern": triad_sign,
        "classification": classification,
    }


def _composition_numbers(target_direction: dict, control_direction: dict, effect_floor: float) -> dict:
    i_target = target_direction["I"]
    i_control = control_direction["I"]
    g_target = target_direction["G"]
    g_control = control_direction["G"]
    a_target = _amplification(target_direction["delta_TP"], target_direction["delta_T"], target_direction["delta_P"], effect_floor)
    a_control = _amplification(control_direction["delta_CP"], control_direction["delta_C"], control_direction["delta_P"], effect_floor)
    ratio = None
    if a_target is not None and a_control is not None and abs(a_control) > effect_floor:
        ratio = a_target / a_control
    return {
        "I_target": i_target,
        "I_control": i_control,
        "M_I": float(abs(i_target) - abs(i_control)),
        "G_target": g_target,
        "G_control": g_control,
        "M_G": float(g_target - g_control),
        "delta_S_target": target_direction["delta_S"],
        "delta_S_control": control_direction["delta_S"],
        "delta_TP_target": target_direction["delta_TP"],
        "delta_CP_control": control_direction["delta_CP"],
        "A_target": a_target,
        "A_control": a_control,
        "A_difference": None if a_target is None or a_control is None else float(a_target - a_control),
        "A_ratio": ratio,
    }


def _amplification(delta_pair, delta_rule, delta_companion, floor: float):
    if None in {delta_pair, delta_rule, delta_companion}:
        return None
    denominator = max(abs(delta_rule), abs(delta_companion))
    if denominator <= floor:
        return None
    return float(abs(delta_pair) / denominator)


def _target_effects(t_rule, book: EffectBook) -> dict:
    factors = factors_for(book.alphabet, None)
    baseline = book.baseline()
    pack = _constrained_pack((t_rule,), factors, book.rho, book.slots, book.cache)
    book.evaluations += 1
    table = baseline["table"]
    out = {}
    for key, source_name, target_name in _direction_names(table):
        solved = _cached_direction(pack, baseline, source_name, target_name, RECONFIGURATION_HORIZON)
        base = _cached_direction(baseline, baseline, source_name, target_name, RECONFIGURATION_HORIZON)
        q = solved["q_controlled"]
        q0 = base["q_controlled"]
        out[key] = {
            "delta": float(q - q0),
            "Q": float(q),
            "Q0": float(q0),
            "spread": None if solved["triad"].get("spread") is None else float(solved["triad"]["spread"]),
            "q": solved["q"],
            "q0": base["q"],
            "mu": base["mu_ref"],
            "residual": float(solved["solver"]["residual"] or 0.0),
        }
    _release_landings(book.cache)
    return out


def _composed_target(t_rule, p_rule, book: EffectBook, floor: float) -> dict:
    factors = factors_for(book.alphabet, None)
    solved = _pack_directions(t_rule, p_rule, factors, book.rho, book.slots, book.cache, floor)
    # Rename C fields to the target names used by the comparison.
    directions = {}
    for key, row in solved["directions"].items():
        directions[key] = {
            "Q0": row["Q0"],
            "QT": row["QC"],
            "QP": row["QP"],
            "QTP": row["QCP"],
            "delta_T": row["delta_C"],
            "delta_P": row["delta_P"],
            "delta_TP": row["delta_CP"],
            "I": row["I"],
            "G": row["G"],
            "delta_S": row["delta_S"],
            "q": row["q"],
            "q0": row["q0"],
            "mu": row["mu"],
        }
    return {"directions": directions, "support_violations": solved["support_violations"]}


def _strategy_multiplier(calibration: dict, strategy: str) -> str | None:
    if strategy == "joint":
        return calibration["joint"]["m_text"] if calibration["joint"]["matched"] else None
    direction = "path_to_matching" if strategy == "forward" else "matching_to_path"
    row = calibration["directions"][direction]
    return row["m_text"] if row["matched"] else None


def _shape_for(target_effects, control_effects, mismatches: dict, floor: float, n_pairs: int, tolerance: float) -> dict:
    reports = {}
    for direction in DIRECTIONS:
        target = target_effects[direction]
        control = control_effects[direction]
        error = np.asarray(control["q"], dtype=np.float64) - np.asarray(target["q"], dtype=np.float64)
        # E(s) = (q_C - q_0) - (q_T - q_0) = q_C - q_T on states where both exist.
        undefined = ~np.isfinite(control["q"]) | ~np.isfinite(target["q"])
        error = error.astype(float)
        error[undefined] = np.nan
        reports[direction] = state_shape_report(
            error,
            np.asarray(control["mu"], dtype=np.float64),
            n_pairs,
            mismatches[direction],
            target["delta"],
            floor,
            tolerance,
        )
    return reports


def assess_target(record: dict, spec: dict, grammar, cache: dict, books: dict) -> dict:
    floor = require_effect_floor(spec)
    tolerance = float(spec["match_tolerance"])
    scale_floor = float(spec["joint_scale_floor"])
    slots = grammar.slot_list()
    t_rule, p_rule, controls = _live_controls(record, grammar, slots)
    if p_rule.weight != record["w_P"] or p_rule.action == t_rule.action:
        raise RuntimeError("companion rule is not the recorded disjoint P rule")
    book = books.setdefault((spec["alphabet"], str(PRIMARY_RHO)), EffectBook(slots, cache, spec["alphabet"], PRIMARY_RHO))
    target_effects = _target_effects(t_rule, book)
    composed_target = _composed_target(t_rule, p_rule, book, floor)
    nominal = nominal_multiplier(record["w_T"], spec["alphabet"])
    control_rows = []
    for control in controls:
        if control["rule"].action != t_rule.action:
            raise RuntimeError("calibration changed the action edge")
        calibration = calibrate_control(control["rule"], target_effects, nominal, book, tolerance, scale_floor)
        strategies = {}
        for strategy in ("forward", "reverse", "joint"):
            multiplier_text_value = _strategy_multiplier(calibration, strategy)
            entry = {"matched": multiplier_text_value is not None, "m_text": multiplier_text_value}
            if multiplier_text_value is None:
                entry["used_as_matched"] = False
                strategies[strategy] = entry
                continue
            multiplier = parse_multiplier_text(multiplier_text_value)
            factors = factors_for(spec["alphabet"], multiplier)
            solved = _pack_directions(control["rule"], p_rule, factors, PRIMARY_RHO, slots, cache, floor)
            if solved["directions"]["path_to_matching"]["Q0"] != composed_target["directions"]["path_to_matching"]["Q0"]:
                raise RuntimeError("controlled baseline diverged between target and calibrated control")
            compared = {}
            for direction in DIRECTIONS:
                compared[direction] = _composition_numbers(
                    composed_target["directions"][direction],
                    solved["directions"][direction],
                    floor,
                )
                compared[direction]["singleton_mismatch"] = abs(
                    solved["directions"][direction]["delta_C"] - target_effects[direction]["delta"]
                )
            control_at_m = book.evaluate(control["rule"], multiplier)
            recheck_ok = True
            for direction in DIRECTIONS:
                mismatch = compared[direction]["singleton_mismatch"]
                required = strategy == "joint" or (
                    strategy == "forward" and direction == "path_to_matching"
                ) or (
                    strategy == "reverse" and direction == "matching_to_path"
                )
                if required and mismatch > tolerance:
                    recheck_ok = False
            shapes = _shape_for(
                target_effects,
                control_at_m,
                {direction: compared[direction]["singleton_mismatch"] for direction in DIRECTIONS},
                floor,
                book.baseline()["n_pairs"],
                tolerance,
            )
            entry.update(
                {
                    "used_as_matched": recheck_ok,
                    "composition": compared,
                    "state_shape": shapes,
                    "support_violations": solved["support_violations"],
                    "companion_key": list(p_rule.key()),
                    "control_action": int(control["rule"].action),
                    "target_action": int(t_rule.action),
                }
            )
            strategies[strategy] = entry
        control_rows.append(
            {
                "control_type": control["control_type"],
                "relation": control["relation"],
                "face": control["face"],
                "calibration": _public_calibration(calibration),
                "strategies": _public_strategies(strategies),
            }
        )
    robustness = None
    if (record["geometry"], record["polarity"], record["w_P"], record["w_T"]) in ROBUSTNESS_CELLS:
        robustness = _robustness(record, t_rule, p_rule, controls, spec, slots, cache, books, floor, tolerance, scale_floor)
    return _num(
        {
            "target_id": record["target_id"],
            "cell": CELL_INDEX[(record["w_P"], record["w_T"])],
            "geometry": record["geometry"],
            "polarity": record["polarity"],
            "w_P": record["w_P"],
            "w_T": record["w_T"],
            "expressions": record["expressions"],
            "nominal_multiplier": multiplier_text(nominal),
            "target_singleton": {
                direction: {
                    "delta": target_effects[direction]["delta"],
                    "Q": target_effects[direction]["Q"],
                    "Q0": target_effects[direction]["Q0"],
                    "spread": target_effects[direction]["spread"],
                }
                for direction in DIRECTIONS
            },
            "target_composition": {
                direction: {
                    "I": composed_target["directions"][direction]["I"],
                    "G": composed_target["directions"][direction]["G"],
                    "delta_S": composed_target["directions"][direction]["delta_S"],
                    "delta_T": composed_target["directions"][direction]["delta_T"],
                    "delta_P": composed_target["directions"][direction]["delta_P"],
                    "delta_TP": composed_target["directions"][direction]["delta_TP"],
                }
                for direction in DIRECTIONS
            },
            "controls": control_rows,
            "robustness": robustness,
            "analysis_version": ANALYSIS_VERSION,
            "calibration_version": CALIBRATION_VERSION,
        }
    )


def _public_calibration(calibration: dict) -> dict:
    return json_ready(calibration)


def _public_strategies(strategies: dict) -> dict:
    cleaned = {}
    for name, entry in strategies.items():
        copied = dict(entry)
        cleaned[name] = copied
    return json_ready(cleaned)


def _robustness(record, t_rule, p_rule, controls, spec, slots, cache, books, floor, tolerance, scale_floor) -> dict:
    """Fixed-control holds the primary joint multiplier. Recalibrated solves again."""
    out = {"rho": {}, "alphabet": {}}
    primary = books[(spec["alphabet"], str(PRIMARY_RHO))]
    nominal = nominal_multiplier(record["w_T"], spec["alphabet"])
    primary_calibration = {
        control["relation"]: calibrate_control(
            control["rule"], _target_effects(t_rule, primary), nominal, primary, tolerance, scale_floor
        )
        for control in controls
    }
    for label in spec.get("rho3_sensitivity", ["1/2", "1", "2"]):
        if label in {"1", "1/1"}:
            continue
        rho = Fraction(label)
        book = books.setdefault((spec["alphabet"], str(rho)), EffectBook(slots, cache, spec["alphabet"], rho))
        out["rho"][label] = _probe_pair(
            t_rule, p_rule, controls, primary_calibration, book, nominal, tolerance, scale_floor, floor, slots, cache
        )
    for alphabet in spec.get("sensitivity_alphabets", ["W3", "W16"]):
        book = books.setdefault((alphabet, str(PRIMARY_RHO)), EffectBook(slots, cache, alphabet, PRIMARY_RHO))
        out["alphabet"][alphabet] = _probe_pair(
            t_rule,
            p_rule,
            controls,
            primary_calibration,
            book,
            nominal_multiplier(record["w_T"], alphabet),
            tolerance,
            scale_floor,
            floor,
            slots,
            cache,
        )
    return out


def _probe_pair(t_rule, p_rule, controls, primary_calibration, book, nominal, tolerance, scale_floor, floor, slots, cache) -> dict:
    target_effects = _target_effects(t_rule, book)
    composed_target = _composed_target(t_rule, p_rule, book, floor)
    rows = []
    for control in controls:
        held = primary_calibration[control["relation"]]["joint"]
        fixed = None
        if held["matched"]:
            fixed = _one_probe(
                control, t_rule, p_rule, held["m_text"], target_effects, composed_target, book, floor, slots, cache
            )
        fresh = calibrate_control(control["rule"], target_effects, nominal, book, tolerance, scale_floor)
        multiplier = fresh["joint"]["m_text"] if fresh["joint"]["matched"] else None
        recalibrated = None
        if multiplier is not None:
            recalibrated = _one_probe(
                control, t_rule, p_rule, multiplier, target_effects, composed_target, book, floor, slots, cache
            )
        rows.append(
            {
                "relation": control["relation"],
                "fixed_control": fixed,
                "recalibrated_control": recalibrated,
                "recalibrated_matched": fresh["joint"]["matched"],
                "recalibrated_m": fresh["joint"]["m_text"],
                "recalibrated_distance": fresh["joint"]["distance"],
                "recalibrated_class": fresh["joint"]["match_class"],
            }
        )
    return {"controls": rows}


def _one_probe(control, t_rule, p_rule, m_text, target_effects, composed_target, book, floor, slots, cache) -> dict:
    multiplier = parse_multiplier_text(m_text)
    factors = factors_for(book.alphabet, multiplier)
    solved = _pack_directions(control["rule"], p_rule, factors, book.rho, slots, cache, floor)
    compared = {}
    for direction in DIRECTIONS:
        numbers = _composition_numbers(composed_target["directions"][direction], solved["directions"][direction], floor)
        numbers["singleton_mismatch"] = abs(solved["directions"][direction]["delta_C"] - target_effects[direction]["delta"])
        compared[direction] = numbers
    return {"m_text": m_text, "directions": compared}


def numerical_reference(spec: dict | None = None) -> dict:
    """Solver gaps and multiplier semantics. Scientific margins are not an input."""
    spec = _minimal_spec() if spec is None else spec
    _require_v07_spec(spec)
    grammar = _grammar(WEIGHT_ORDER, 4)
    slots = grammar.slot_list()
    catalogue = graded_catalogue(_catalogue_view(spec))
    anchor = next(
        row
        for row in selected_records(catalogue)
        if row["geometry"] == "contains_p_companion_edge"
        and row["polarity"] == "absent"
        and row["w_P"] == "prohibit"
        and row["w_T"] == "prohibit"
    )
    t_rule, p_rule, controls = _live_controls(anchor, grammar, slots)
    erasure = next(control for control in controls if control["control_type"] == "erasure")
    named = erasure["named_rule"]
    continuous = erasure["rule"]
    rho = PRIMARY_RHO
    cache: dict = {}
    baseline = _baseline_pack(alphabet_factors("W4"), rho, slots, cache)
    neutral = _constrained_pack((continuous,), factors_for("W4", Fraction(1)), rho, slots, cache)
    deleted = _constrained_pack((continuous,), factors_for("W4", Fraction(0)), rho, slots, cache)
    prohibited = _constrained_pack((Constraint(named.polarity, named.action, named.conditions, "prohibit", ()),), alphabet_factors("W4"), rho, slots, cache)
    weight_gaps = {"neutral_versus_baseline": _weight_gap(neutral["kernel"], baseline["kernel"]), "zero_versus_prohibit": _weight_gap(deleted["kernel"], prohibited["kernel"])}
    for grade in ENUMERATED_WEIGHTS:
        if grade == "prohibit":
            continue
        factor = nominal_multiplier(grade, "W4")
        left = _constrained_pack((continuous,), factors_for("W4", factor), rho, slots, cache)
        right = _constrained_pack((Constraint(named.polarity, named.action, named.conditions, grade, ()),), alphabet_factors("W4"), rho, slots, cache)
        weight_gaps[grade] = _weight_gap(left["kernel"], right["kernel"])
    landing_gaps = {}
    committor_gaps = {}
    direct_gaps = {}
    for name, kernel in {
        "baseline": baseline["kernel"],
        "neutral": neutral["kernel"],
        "zero": deleted["kernel"],
        "named_strong_suppress": _constrained_pack(
            (Constraint(named.polarity, named.action, named.conditions, "strong_suppress", ()),),
            alphabet_factors("W4"),
            rho,
            slots,
            cache,
        )["kernel"],
    }.items():
        dense, _dense_defect = epoch_kernel_float(kernel)
        block, _block_defect = epoch_kernel_block(kernel)
        landing_gaps[name] = float(np.max(np.abs(dense - block)))
        _n_pairs, class_index, table = kernel_layout_index(kernel)
        gaps = []
        iterative = []
        for source_name, target_name in (
            (table.path_name, table.matching_name),
            (table.matching_name, table.path_name),
        ):
            source = baseline["positions"][source_name]
            target = baseline["positions"][target_name]
            left = eventual_committor(dense, class_index, source, target)
            right = eventual_committor(block, class_index, source, target)
            both = np.isfinite(left["q"]) & np.isfinite(right["q"])
            gaps.append(float(np.max(np.abs(left["q"][both] - right["q"][both]))))
            iterated = eventual_committor(block, class_index, source, target, method="iterative")
            both_i = np.isfinite(right["q"]) & np.isfinite(iterated["q"])
            iterative.append(float(np.max(np.abs(right["q"][both_i] - iterated["q"][both_i]))))
        committor_gaps[name] = max(gaps)
        direct_gaps[name] = max(iterative)
    book = EffectBook(slots, cache, "W4", rho)
    effects = _target_effects(t_rule, book)
    control_spreads = {}
    for name, pack in (("neutral", neutral), ("zero", deleted)):
        control_spreads[name] = {}
        for key, source_name, target_name in _direction_names(baseline["table"]):
            solved = _cached_direction(pack, baseline, source_name, target_name, RECONFIGURATION_HORIZON)
            spread = solved["triad"].get("spread")
            control_spreads[name][key] = None if spread is None else float(spread)
    from rs_constraint_lab.v06 import PUBLISHED_ANCHOR

    published_gap = 0.0
    for direction, published in PUBLISHED_ANCHOR.items():
        published_gap = max(published_gap, abs(effects[direction]["delta"] - published["delta_T"]))
    spread_gap = max(
        abs(value)
        for row in control_spreads.values()
        for value in row.values()
        if value is not None
    )
    worst = max(
        [
            *weight_gaps.values(),
            *landing_gaps.values(),
            *committor_gaps.values(),
            *direct_gaps.values(),
            published_gap,
            spread_gap,
        ]
    )
    return {
        "weight_gaps": weight_gaps,
        "landing_block_vs_dense": landing_gaps,
        "committor_block_vs_dense": committor_gaps,
        "committor_direct_vs_iterative": direct_gaps,
        "anchor_singleton_versus_published_delta_T": published_gap,
        "unconditional_control_triad_spread": control_spreads,
        "worst_numerical_gap": worst,
        "match_tolerance_decision": "keep_1e-8" if worst < 1e-10 else "stop_and_document_before_census",
        "effect_floor_decision": "keep_1e-8" if worst < 1e-10 else "stop_and_document_before_census",
        "grid_length": len(POSITIVE_GRID),
        "grid_sha256": GRID_SHA256,
        "companion_weight": p_rule.weight,
        "analysis_version_read_from_v06": ANALYSIS_VERSION_6,
        "semantic_version": HYPERGRAPH_N4_SEMANTIC_VERSION,
    }


def _weight_gap(left, right) -> float:
    gaps = []
    for left_row, right_row in zip(left.weights, right.weights):
        for left_weight, right_weight in zip(left_row, right_row):
            gaps.append(abs(float(left_weight) - float(right_weight)))
    return float(max(gaps) if gaps else 0.0)


def relabelled_kernel_gap(multiplier: Fraction = Fraction(1, 4)) -> float:
    """Kernel-weight equivariance under a non-identity slot permutation.

    Relabelling a rule and keeping the path and matching classes fixed is not
    an invariant. The weights must agree after the state and the slot are
    both pulled back by the same slot map.
    """
    grammar = _grammar(WEIGHT_ORDER, 4)
    slots = grammar.slot_list()
    catalogue = graded_catalogue(_catalogue_view(_minimal_spec()))
    anchor = next(
        row
        for row in selected_records(catalogue)
        if row["w_T"] == "strong_suppress"
        and row["w_P"] == "strong_suppress"
        and row["polarity"] == "absent"
        and row["geometry"] == "contains_p_companion_edge"
    )
    _t_rule, _p_rule, controls = _live_controls(anchor, grammar, slots)
    rule = next(control["rule"] for control in controls if control["control_type"] == "erasure")
    slot_map = next(
        item for item in slot_permutation_maps(4, relation_slots(4, 3)) if item != tuple(range(len(slots)))
    )
    image = relabel_constraint(rule, slot_map)
    cache: dict = {}
    factors = factors_for("W4", multiplier)
    left = _constrained_pack((rule,), factors, PRIMARY_RHO, slots, cache)["kernel"]
    right = _constrained_pack((image,), factors, PRIMARY_RHO, slots, cache)["kernel"]
    gap = 0.0
    for state in range(left.n_states):
        image_state = 0
        for bit, dest in enumerate(slot_map):
            if (state >> bit) & 1:
                image_state |= 1 << dest
        for slot in range(len(slots)):
            gap = max(
                gap,
                abs(float(left.weights[state][slot]) - float(right.weights[image_state][slot_map[slot]])),
            )
    return gap


def curve_timing(spec: dict | None = None) -> dict:
    """Time one full positive grid plus the deletion boundary.

    ``EffectBook.evaluate`` builds that whole curve on the first call, so a
    short prefix would not be a per-point measurement. The returned deltas
    are not kept. This does not read a composed margin.
    """
    spec = _minimal_spec() if spec is None else spec
    grammar = _grammar(WEIGHT_ORDER, 4)
    slots = grammar.slot_list()
    catalogue = graded_catalogue(_catalogue_view(spec))
    anchor = next(
        row
        for row in selected_records(catalogue)
        if row["w_T"] == "weak_suppress"
        and row["w_P"] == "weak_suppress"
        and row["polarity"] == "absent"
        and row["geometry"] == "contains_p_companion_edge"
    )
    _t_rule, _p_rule, controls = _live_controls(anchor, grammar, slots)
    erasure = next(control for control in controls if control["control_type"] == "erasure")
    cache: dict = {}
    book = EffectBook(slots, cache, "W4", PRIMARY_RHO)
    started = time.perf_counter()
    book.curve(erasure["rule"])
    elapsed = time.perf_counter() - started
    points = len(POSITIVE_GRID) + 1
    per_point = elapsed / points
    plan = coverage_plan(catalogue)
    return {
        "sample_points": points,
        "sample_seconds": elapsed,
        "seconds_per_grid_point": per_point,
        "estimated_grid_seconds": per_point * plan["expected_grid_kernel_evaluations"],
        "curve_evaluations": book.evaluations,
        "coverage": plan,
    }


def build_effect_plan(spec: dict, items: int, header: dict) -> dict:
    from rs_constraint_lab.execution import PLAN_SCHEMA, _hypergraph_accounting, _shard_id, _shard_identity
    from rs_constraint_lab.version import DEFAULT_WORKERS, PROFILE_NOTE

    _require_v07_spec(spec)
    require_effect_floor(spec)
    catalogue = graded_catalogue(_catalogue_view(spec))
    records = selected_records(catalogue)
    plan_counts = coverage_plan(catalogue)
    count = len(records)
    cell = spec["cells"][0]
    grammar = _grammar(WEIGHT_ORDER, 4)
    shards = []
    start = 0
    while start < count:
        end = min(start + items, count)
        identity = _shard_identity(spec, header, 0, cell, 2, start, end)
        identity["analysis_version"] = ANALYSIS_VERSION
        identity["calibration_version"] = CALIBRATION_VERSION
        identity["match_tolerance"] = float(spec["match_tolerance"])
        identity["joint_scale_floor"] = float(spec["joint_scale_floor"])
        identity["grid_sha256"] = GRID_SHA256
        identity["effect_floor"] = float(spec["effect_floor"])
        shards.append(
            {
                "shard_id": _shard_id(identity),
                "ordinal": len(shards),
                "cell_index": 0,
                "n": 4,
                "k_max": 2,
                "a_max": 4,
                "cardinality": 2,
                "start": start,
                "end": end,
                "identity": identity,
            }
        )
        start = end
    header = dict(header)
    header["analysis_version"] = ANALYSIS_VERSION
    header["calibration_version"] = CALIBRATION_VERSION
    header["grid_sha256"] = GRID_SHA256
    return {
        "schema": PLAN_SCHEMA,
        "header": header,
        "spec": spec,
        "estimates": {
            "cells": [
                {
                    "N": 4,
                    "K_max": 2,
                    "A_max": 4,
                    "labelled_states": 1024,
                    "canonical_states": None,
                    "grammar": grammar.stats,
                    "edge_accounting": _hypergraph_accounting(grammar),
                    "cardinalities": {
                        "2": {
                            "labelled_combinations": count,
                            "labelled_simple": count,
                            "labelled_stacked": 0,
                            "canonical_simple_exact": count,
                            "shards": len(shards),
                            "disk_upper_bound_bytes": count * 80000,
                            "symmetry_estimate_simple_over_factorial": count / 24,
                            "canonicalisation_comparisons": count,
                        }
                    },
                    "calibration_coverage": plan_counts,
                }
            ],
            "shard_count": len(shards),
            "disk_upper_bound_bytes": count * 80000,
            "shard_items": items,
            "profile_note": PROFILE_NOTE,
            "workers_default": DEFAULT_WORKERS,
            "calibration_coverage": plan_counts,
            "effect_floor": float(spec["effect_floor"]),
            "match_tolerance": float(spec["match_tolerance"]),
        },
        "shards": shards,
    }


def execute_7_shard(task: dict) -> None:
    del task
    raise RuntimeError(
        "generation 007 refuses a monolithic shard. "
        "Use python -m rs_constraint_lab generation007 supervise"
    )
    spec = dict(task["spec"])
    _require_v07_spec(spec)
    if task["identity"].get("calibration_version") != CALIBRATION_VERSION:
        raise RuntimeError("calibration version does not match the shard identity")
    if task["identity"].get("grid_sha256") != GRID_SHA256:
        raise RuntimeError("calibration grid does not match the shard identity")
    if int(spec.get("reconfiguration_horizon", RECONFIGURATION_HORIZON)) != RECONFIGURATION_HORIZON:
        raise RuntimeError("refusing to run: the horizon is not the predeclared value 16")
    catalogue = graded_catalogue(_catalogue_view(spec))
    records = selected_records(catalogue)
    shard_dir = Path(task["shard_dir"])
    shard_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(
        shard_dir / "running.json",
        {"shard_id": task["shard_id"], "attempt": task["attempt"], "started_at": _now(), "pid": _pid()},
    )
    started = time.perf_counter()
    grammar = _grammar(WEIGHT_ORDER, 4)
    cache: dict = {}
    books: dict = {}
    rows = []
    for record in records[int(task["start"]):int(task["end"])]:
        rows.append(assess_target(record, spec, grammar, cache, books))
        _release_landings(cache)
    counts = {"analysed": len(rows), "solver_failures": 0, "start": int(task["start"]), "end": int(task["end"])}
    result = {"identity": task["identity"], "counts": counts, "calibrated_rows": rows}
    _finish_receipt(task, shard_dir, json_ready(result), started, counts)


def _now() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _pid() -> int:
    import os

    return os.getpid()


def summarise_calibrated(rows: list[dict], floor: float) -> dict:
    """Counts only. A matched flag that is false is not counted as a match."""
    summary = {"directions": {}, "strategies": {}}
    for direction in DIRECTIONS:
        summary["directions"][direction] = {
            "target_delta_S_above_floor": 0,
            "finite_target_delta_S_above_floor": 0,
            "finite_targets": 0,
        }
    for row in rows:
        finite = row["w_P"] != "prohibit" and row["w_T"] != "prohibit"
        for direction in DIRECTIONS:
            delta_s = row["target_composition"][direction]["delta_S"]
            if delta_s is not None and delta_s > floor:
                summary["directions"][direction]["target_delta_S_above_floor"] += 1
                if finite:
                    summary["directions"][direction]["finite_target_delta_S_above_floor"] += 1
            if finite:
                summary["directions"][direction]["finite_targets"] += 1
    for strategy in ("forward", "reverse", "joint"):
        bucket = {
            "matched": 0,
            "not_matched": 0,
            "classes": {},
            "by_direction": {direction: _empty_margin_counts() for direction in DIRECTIONS},
            "by_relation": {},
        }
        for row in rows:
            finite = row["w_P"] != "prohibit" and row["w_T"] != "prohibit"
            for control in row["controls"]:
                relation = control["relation"]
                relation_bucket = bucket["by_relation"].setdefault(
                    relation,
                    {
                        "matched": 0,
                        "not_matched": 0,
                        "by_direction": {direction: _empty_margin_counts() for direction in DIRECTIONS},
                    },
                )
                claim = control["strategies"][strategy]
                match_class = _strategy_class(control, strategy)
                bucket["classes"][match_class] = bucket["classes"].get(match_class, 0) + 1
                if not claim.get("used_as_matched"):
                    bucket["not_matched"] += 1
                    relation_bucket["not_matched"] += 1
                    continue
                bucket["matched"] += 1
                relation_bucket["matched"] += 1
                for direction, numbers in claim["composition"].items():
                    if not finite:
                        continue
                    _tally_sign(bucket["by_direction"][direction], numbers, floor)
                    _tally_sign(relation_bucket["by_direction"][direction], numbers, floor)
                    delta_s = numbers["delta_S_control"]
                    key = (
                        "matched_control_delta_S_within_floor"
                        if delta_s is None or abs(delta_s) <= floor
                        else "matched_control_delta_S_above_floor"
                    )
                    bucket["by_direction"][direction][key] += 1
        summary["strategies"][strategy] = bucket
    return summary


def _empty_margin_counts() -> dict:
    return {
        "finite_matched_M_I_positive": 0,
        "finite_matched_M_I_negative": 0,
        "finite_matched_M_I_within_floor": 0,
        "finite_matched_M_G_positive": 0,
        "finite_matched_M_G_negative": 0,
        "finite_matched_M_G_within_floor": 0,
        "matched_control_delta_S_above_floor": 0,
        "matched_control_delta_S_within_floor": 0,
    }


def _strategy_class(control: dict, strategy: str) -> str:
    if strategy == "joint":
        return control["calibration"]["joint"]["match_class"]
    direction = "path_to_matching" if strategy == "forward" else "matching_to_path"
    return control["calibration"]["directions"][direction]["match_class"]


def _tally_sign(bucket: dict, numbers: dict, floor: float) -> None:
    for name, key in (("M_I", "finite_matched_M_I"), ("M_G", "finite_matched_M_G")):
        value = numbers[name]
        if value > floor:
            bucket[f"{key}_positive"] += 1
        elif value < -floor:
            bucket[f"{key}_negative"] += 1
        else:
            bucket[f"{key}_within_floor"] += 1


def merge_v07(out_dir: Path, plan: dict, publish: Path | None = None) -> dict:
    from rs_constraint_lab.execution import _fingerprint, _reconcile
    from rs_constraint_lab.generation import _git_commit, _publish
    from rs_constraint_lab.version import EXECUTION_PRINCIPLE, MAX_ATTEMPTS, PROFILE_NOTE

    out_dir = Path(out_dir)
    progress = _reconcile(out_dir, plan)
    spec = plan["spec"]
    floor = require_effect_floor(spec)
    rows: list[dict] = []
    work = 0.0
    analysed = 0
    for shard in plan["shards"]:
        state = progress["shards"][shard["shard_id"]]
        if state["status"] != "completed":
            continue
        result = read_json(out_dir / "shards" / shard["shard_id"] / "result.json")
        rows.extend(result.get("calibrated_rows") or [])
        analysed += int(result["counts"].get("analysed", 0))
        receipt = read_json(out_dir / "shards" / shard["shard_id"] / "receipt.json")
        work += float(receipt.get("elapsed_seconds") or 0.0)
    questions = summarise_calibrated(rows, floor) if rows else None
    if progress["status"] == "COMPLETE":
        expected = plan["estimates"]["cells"][0]["cardinalities"]["2"]["canonical_simple_exact"]
        if analysed != expected:
            raise RuntimeError(f"generation 7 analysed {analysed}, planned {expected}")
        atomic_write_json(out_dir / "calibration-table.json", json_ready(_calibration_table(rows)))
        atomic_write_json(out_dir / "composition-table.json", json_ready(_composition_table(rows)))
        atomic_write_json(out_dir / "state-shape-table.json", json_ready(_state_table(rows)))
        atomic_write_json(out_dir / "robustness-table.json", json_ready(_robustness_table(rows)))
    cell = spec["cells"][0]
    n = int(cell["N"])
    k_max = int(cell["K_max"])
    estimate = plan["estimates"]["cells"][0]
    v07_summary = None
    if questions is not None and progress["status"] == "COMPLETE":
        v07_summary = {
            "coverage": plan["estimates"]["calibration_coverage"],
            "questions": questions,
            "match_tolerance": float(spec["match_tolerance"]),
            "joint_scale_floor": float(spec["joint_scale_floor"]),
            "grid_sha256": GRID_SHA256,
        }
    summary = {
        "status": progress["status"],
        "engine_version": plan["header"]["engine_version"],
        "semantic_version": plan["header"]["semantic_version"],
        "git_commit": _git_commit(),
        "python": __import__("sys").version.split()[0],
        "numpy": np.__version__,
        "platform": __import__("sys").platform,
        "spec_hash": plan["header"]["spec_hash"],
        "experiment_id": spec["experiment_id"],
        "generation": spec["generation"],
        "composition": spec.get("composition", "structural-simple"),
        "predicates": list(spec.get("predicates", [])),
        "analysis": spec.get("analysis"),
        "analysis_version": ANALYSIS_VERSION,
        "calibration_version": CALIBRATION_VERSION,
        "normalisation_version": plan["header"]["normalisation_version"],
        "grammar_version": plan["header"]["grammar_version"],
        "runtime_seconds": 0.0,
        "shard_work_seconds": work,
        "receipt_fingerprint": _fingerprint(out_dir, plan),
        "execution": {
            "workers_last": progress.get("workers_last"),
            "worker_history": progress.get("worker_history", []),
            "shard_items": plan["header"]["shard_items"],
            "shard_count": plan["estimates"]["shard_count"],
            "max_attempts": MAX_ATTEMPTS,
            "multiprocessing": "spawn",
            "principle": EXECUTION_PRINCIPLE,
            "profile_note": PROFILE_NOTE,
        },
        "cells": [
            {
                "coordinate": {
                    "N": n,
                    "A_max": cell.get("A_max"),
                    "O": 3,
                    "G": 0,
                    "S": 0,
                    "H": 0,
                    "K_max": k_max,
                    "L": 0,
                    "semantics": "hypergraph",
                    "alphabet": spec["alphabet"],
                    "composition": spec.get("composition", "structural-simple"),
                    "predicates": list(spec.get("predicates", ["pair", "triad"])),
                    "analysis": spec.get("analysis"),
                },
                "runtime_seconds": work,
                "accounting": {"edge": estimate["edge_accounting"], "grammar": estimate["grammar"]},
                "canonical_states": None,
                "relation_slots": estimate["edge_accounting"]["relation_slots"],
                "labelled_states": estimate["labelled_states"],
                "cardinalities": {
                    "2": {
                        "labelled_combinations": estimate["cardinalities"]["2"].get("labelled_combinations"),
                        "labelled_simple": estimate["cardinalities"]["2"].get("labelled_simple"),
                        "labelled_stacked": 0,
                        "canonical": analysed,
                        "analysed": analysed,
                    }
                },
                "families": 0,
                "family_histogram": {},
                "structural_families": 0,
                "screened_families": 0,
                "baseline_equivalent_families": 0,
                "cancellations": {},
                "extremes": {},
                "family_index_sha256": "",
                "singles_sha256": "",
                "kernel_index_sha256": "",
                "kernel_index_count": 0,
                "qualitative_index_sha256": "",
                "observable_index_sha256": "",
                "v07_census": v07_summary,
            }
        ],
        "unsearched_declared": list(spec.get("unsearched", [])),
        "territory": None,
        "effect_floor": floor,
        "effect_floor_reason": spec.get("effect_floor_reason"),
        "match_tolerance": float(spec["match_tolerance"]),
        "v07": v07_summary,
    }
    if publish is not None and summary["status"] == "COMPLETE":
        _publish(summary, spec, Path(publish), out_dir)
        _publish_tables(out_dir, spec, Path(publish))
    return summary


def _publish_tables(out_dir: Path, spec: dict, publish: Path) -> None:
    from rs_constraint_lab.execution import FAMILY_INDEX_COMMIT_LIMIT_BYTES

    tables = publish / "reports" / "tables"
    tables.mkdir(parents=True, exist_ok=True)
    for name in ("calibration-table.json", "composition-table.json", "state-shape-table.json", "robustness-table.json"):
        path = out_dir / name
        if path.exists() and path.stat().st_size <= FAMILY_INDEX_COMMIT_LIMIT_BYTES:
            target = tables / f"{spec['experiment_id']}-{name}"
            target.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")


def _calibration_table(rows: list[dict]) -> list[dict]:
    table = []
    for row in rows:
        for control in row["controls"]:
            forward = control["calibration"]["directions"]["path_to_matching"]
            reverse = control["calibration"]["directions"]["matching_to_path"]
            joint = control["calibration"]["joint"]
            table.append(
                {
                    "target_id": row["target_id"],
                    "cell": row["cell"],
                    "geometry": row["geometry"],
                    "polarity": row["polarity"],
                    "w_P": row["w_P"],
                    "w_T": row["w_T"],
                    "control_type": control["control_type"],
                    "relation": control["relation"],
                    "face": control["face"],
                    "m_forward": forward["m_text"],
                    "forward_mismatch": forward["absolute_mismatch"],
                    "forward_class": forward["match_class"],
                    "forward_matched": forward["matched"],
                    "m_reverse": reverse["m_text"],
                    "reverse_mismatch": reverse["absolute_mismatch"],
                    "reverse_class": reverse["match_class"],
                    "reverse_matched": reverse["matched"],
                    "m_joint": joint["m_text"],
                    "joint_distance": joint["distance"],
                    "joint_class": joint["match_class"],
                    "joint_matched": joint["matched"],
                    "boundary_status": {
                        "forward": forward["boundary_status"],
                        "reverse": reverse["boundary_status"],
                        "joint": joint["boundary_status"],
                    },
                    "root_count": {"forward": forward["root_count"], "reverse": reverse["root_count"]},
                    "monotonicity": {"forward": forward["monotonicity"], "reverse": reverse["monotonicity"]},
                    "only_exact_solution_is_zero": {
                        "forward": forward["only_exact_solution_is_zero"],
                        "reverse": reverse["only_exact_solution_is_zero"],
                    },
                }
            )
    return table


def _composition_table(rows: list[dict]) -> list[dict]:
    table = []
    for row in rows:
        for control in row["controls"]:
            for strategy, claim in control["strategies"].items():
                if not claim.get("composition"):
                    table.append(
                        {
                            "target_id": row["target_id"],
                            "relation": control["relation"],
                            "strategy": strategy,
                            "used_as_matched": False,
                        }
                    )
                    continue
                for direction, numbers in claim["composition"].items():
                    table.append(
                        {
                            "target_id": row["target_id"],
                            "cell": row["cell"],
                            "geometry": row["geometry"],
                            "polarity": row["polarity"],
                            "w_P": row["w_P"],
                            "w_T": row["w_T"],
                            "relation": control["relation"],
                            "strategy": strategy,
                            "direction": direction,
                            "used_as_matched": bool(claim.get("used_as_matched")),
                            **numbers,
                        }
                    )
    return table


def _state_table(rows: list[dict]) -> list[dict]:
    table = []
    for row in rows:
        for control in row["controls"]:
            for strategy, claim in control["strategies"].items():
                shape = claim.get("state_shape")
                if not shape:
                    continue
                for direction, report in shape.items():
                    table.append(
                        {
                            "target_id": row["target_id"],
                            "relation": control["relation"],
                            "strategy": strategy,
                            "direction": direction,
                            "used_as_matched": bool(claim.get("used_as_matched")),
                            "aggregate_mismatch": report.get("aggregate_mismatch"),
                            "max_state_mismatch": report.get("max_abs"),
                            "triad_bucket_mismatch": report.get("triad_bucket_mismatch"),
                            "sign_pattern": report.get("sign_pattern"),
                            "triad_sign_pattern": report.get("triad_sign_pattern"),
                            "classification": report.get("classification"),
                        }
                    )
    return table


def _robustness_table(rows: list[dict]) -> list[dict]:
    table = []
    for row in rows:
        if not row.get("robustness"):
            continue
        for kind in ("rho", "alphabet"):
            for label, probe in row["robustness"][kind].items():
                for control in probe["controls"]:
                    table.append(
                        {
                            "target_id": row["target_id"],
                            "cell": row["cell"],
                            "kind": kind,
                            "label": label,
                            "relation": control["relation"],
                            "fixed_control": control["fixed_control"],
                            "recalibrated_control": control["recalibrated_control"],
                            "recalibrated_matched": control["recalibrated_matched"],
                            "recalibrated_m": control["recalibrated_m"],
                            "recalibrated_class": control["recalibrated_class"],
                        }
                    )
    return table
