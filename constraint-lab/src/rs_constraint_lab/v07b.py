"""Generation 007B two-level pair-face control.

The control keeps one live pair face and one dissolve action. It replaces the
single conditional multiplier with two complementary levels, ``m_on`` and
``m_off``. Exactly one of those rules matches in any admissible action state.

The planner reads stored passage vectors. A missing ``(m_off, m_on)`` point
is a request, not a kernel call.
"""

from __future__ import annotations

import math
from decimal import Decimal
from fractions import Fraction

import numpy as np

from rs_constraint_lab.constraints import Constraint
from rs_constraint_lab.durable import canonical_json, sha256_bytes
from rs_constraint_lab.passage import interaction_residual, super_singleton_gap
from rs_constraint_lab.reconfiguration import RECONFIGURATION_HORIZON
from rs_constraint_lab.v05 import (
    _baseline_pack,
    _cached_direction,
    _constrained_pack,
    _direction_names,
    _grammar,
    _num,
    _release_landings,
    _support_violations,
)
from rs_constraint_lab.v06 import WEIGHT_ORDER, graded_catalogue
from rs_constraint_lab.v07 import (
    BASELINE_FACTORS,
    CELL_INDEX,
    DIRECTIONS,
    EFFECT_FLOOR_DEFAULT,
    JOINT_SCALE_FLOOR_DEFAULT,
    MATCH_TOLERANCE_DEFAULT,
    _catalogue_view,
    _live_controls,
    factors_for,
    joint_distance,
    joint_scales,
    log_distance,
    multiplier_text,
    nominal_multiplier,
    parse_multiplier_text,
    selected_records,
)
from rs_constraint_lab.version import HYPERGRAPH_N4_SEMANTIC_VERSION

ANALYSIS_7B = "n4-two-level-pair-face"
ANALYSIS_VERSION = "0.7.1"
CALIBRATION_VERSION = "0.7.1"
SEMANTIC_VERSION = HYPERGRAPH_N4_SEMANTIC_VERSION
M_ON = "m_on"
M_OFF = "m_off"
MATCH_TOLERANCE = MATCH_TOLERANCE_DEFAULT
EFFECT_FLOOR = EFFECT_FLOOR_DEFAULT
SCALE_FLOOR = JOINT_SCALE_FLOOR_DEFAULT
ADAPTIVE_CAP = 250
CLUSTER_LOG10 = Decimal("0.02")
MAX_INITIAL_BASINS = 12
NEWTON_WIDTH = Decimal("0.05")
CONDITION_LIMIT = 1e6
SMALL_SOLUTION_FAMILY = 8
LOG_QUANTUM = Decimal("0.000001")
DOMAIN_LO = Decimal("-4")
DOMAIN_HI = Decimal("4")
COARSE_LOGS = tuple(Decimal(index) for index in range(-4, 5))
TERMINAL_STATUSES = {"represented", "unrepresented", "unresolved_at_cap"}
ROBUSTNESS_RHOS = ("1/2", "2")
ROBUSTNESS_ROWS = (
    ("contains_p_companion_edge", "absent", "prohibit", "prohibit", "adjacent"),
    ("contains_p_companion_edge", "absent", "prohibit", "prohibit", "disjoint"),
    ("contains_p_companion_edge", "present", "prohibit", "prohibit", "adjacent"),
    ("contains_t_action_edge", "absent", "strong_suppress", "strong_suppress", "adjacent"),
    ("contains_p_companion_edge", "absent", "strong_favour", "strong_favour", "adjacent"),
    ("contains_p_companion_edge", "absent", "strong_suppress", "strong_favour", "disjoint"),
)
PREFLIGHT_ABSENT = {
    ("prohibit", "prohibit"),
    ("strong_suppress", "strong_suppress"),
    ("strong_favour", "strong_favour"),
    ("strong_suppress", "strong_favour"),
}
COMPLEXITY_TARGET = (3, 1, 1, 2, 1, 0, 0)
COMPLEXITY_CONTROL = (2, 2, 2, 2, 1, 0, 0)
GRADE_ORDER = (
    "prohibit",
    "strong_suppress",
    "weak_suppress",
    "weak_favour",
    "strong_favour",
)


def text_from_log(log_value: Decimal) -> str:
    magnitude = Decimal(10) ** log_value
    return multiplier_text(parse_multiplier_text(format(magnitude, ".12e")))


COARSE_TEXTS = tuple(text_from_log(value) for value in COARSE_LOGS)
COARSE_SHA256 = sha256_bytes("\n".join(COARSE_TEXTS).encode("utf-8"))
COARSE_PAIRS = tuple((left, right) for left in COARSE_TEXTS for right in COARSE_TEXTS)


def log_from_text(text: str) -> Decimal | None:
    if text == "0":
        return None
    value = Decimal(parse_multiplier_text(text).numerator) / Decimal(parse_multiplier_text(text).denominator)
    return value.ln() / Decimal(10).ln()


def quantize_log(value: Decimal) -> Decimal:
    return value.quantize(LOG_QUANTUM)


def two_level_rules(named: Constraint) -> tuple[Constraint, Constraint]:
    """Complementary pair-face rules. ``on`` keeps the named literal."""
    if len(named.conditions) != 1 or named.counts:
        raise ValueError("a two-level pair-face control needs exactly one pair literal")
    slot, bit = named.conditions[0]
    on_rule = Constraint(named.polarity, named.action, ((slot, bit),), M_ON, ())
    off_rule = Constraint(named.polarity, named.action, ((slot, 1 - bit),), M_OFF, ())
    return off_rule, on_rule


def active_rule_count(rules: tuple[Constraint, Constraint], state: int, edge: int) -> int:
    return sum(1 for rule in rules if rule.matches(state, edge))


def structure_id(off_rule: Constraint, on_rule: Constraint) -> str:
    payload = {
        "off": list(off_rule.structural_key()),
        "off_weight": off_rule.weight,
        "on": list(on_rule.structural_key()),
        "on_weight": on_rule.weight,
    }
    return sha256_bytes(canonical_json(payload).encode("utf-8"))


def _identity(payload: dict) -> str:
    return sha256_bytes(canonical_json(payload).encode("utf-8"))


def build_problems(spec: dict) -> list[dict]:
    catalogue = graded_catalogue(_catalogue_view(spec))
    grammar = _grammar(WEIGHT_ORDER, 4)
    slots = grammar.slot_list()
    problems = []
    for record in selected_records(catalogue):
        target, companion, controls = _live_controls(record, grammar, slots)
        for control in controls:
            if control["control_type"] != "pair_face":
                continue
            named = control["named_rule"]
            off_rule, on_rule = two_level_rules(named)
            identity = {
                "alphabet": spec["alphabet"],
                "analysis_version": ANALYSIS_VERSION,
                "off_expression": off_rule.expression(slots),
                "on_expression": on_rule.expression(slots),
                "rho": "1",
                "target_id": record["target_id"],
            }
            problems.append(
                {
                    "alphabet": spec["alphabet"],
                    "calibration_id": _identity(identity),
                    "cell": CELL_INDEX[(record["w_P"], record["w_T"])],
                    "face": control.get("face"),
                    "geometry": record["geometry"],
                    "nominal": multiplier_text(nominal_multiplier(record["w_T"], spec["alphabet"])),
                    "off_expression": off_rule.expression(slots),
                    "on_expression": on_rule.expression(slots),
                    "p_expression": companion.expression(slots),
                    "polarity": record["polarity"],
                    "relation": control["relation"],
                    "rho": "1",
                    "role": "primary",
                    "structure_id": structure_id(off_rule, on_rule),
                    "t_expression": target.expression(slots),
                    "target_id": record["target_id"],
                    "w_P": record["w_P"],
                    "w_T": record["w_T"],
                }
            )
    problems.sort(key=lambda row: (row["geometry"], row["polarity"], row["w_T"], row["w_P"], row["relation"], row["face"] or "", row["target_id"]))
    return problems


def is_preflight(problem: dict) -> bool:
    grades = (problem["w_T"], problem["w_P"])
    if problem["polarity"] == "absent" and grades in PREFLIGHT_ABSENT:
        return True
    return problem["polarity"] == "present" and grades == ("prohibit", "prohibit")


def is_robustness(problem: dict) -> bool:
    row = (problem["geometry"], problem["polarity"], problem["w_T"], problem["w_P"], problem["relation"])
    return row in ROBUSTNESS_ROWS


def work_count(problems: list[dict]) -> dict:
    structures = {row["structure_id"] for row in problems}
    targets = {row["t_expression"] for row in problems}
    return {
        "adaptive_cap_per_problem": ADAPTIVE_CAP,
        "coarse_points_per_structure": len(COARSE_PAIRS),
        "initial_atomic_items": len(structures) * len(COARSE_PAIRS) + len(targets),
        "logical_calibration_problems": len(problems),
        "unique_target_singletons": len(targets),
        "unique_two_level_structures": len(structures),
        "worst_case_adaptive_items": len(problems) * ADAPTIVE_CAP,
        "worst_case_primary_items": len(structures) * len(COARSE_PAIRS) + len(targets) + len(problems) * ADAPTIVE_CAP,
    }


def _point_key(m_off: str, m_on: str) -> str:
    return f"{m_off}\t{m_on}"


def _split_key(key: str) -> tuple[str, str]:
    left, right = key.split("\t", 1)
    return left, right


def _residual(point: dict, target: dict) -> tuple[float, float]:
    return (
        float(point["delta_forward"]) - float(target["delta_forward"]),
        float(point["delta_reverse"]) - float(target["delta_reverse"]),
    )


def _distance(point: dict, target: dict, scales: dict) -> float:
    return joint_distance(
        float(point["delta_forward"]),
        float(point["delta_reverse"]),
        float(target["delta_forward"]),
        float(target["delta_reverse"]),
        scales,
    )


def _within(point: dict, target: dict, tolerance: float) -> bool:
    forward, reverse = _residual(point, target)
    return abs(forward) <= tolerance and abs(reverse) <= tolerance


def _spans_zero(values: list[float]) -> bool:
    return min(values) <= 0.0 <= max(values)


def _new_basin(basin_id: str, log_off_lo: Decimal, log_off_hi: Decimal, log_on_lo: Decimal, log_on_hi: Decimal, origin: str) -> dict:
    return {
        "basin_id": basin_id,
        "best": None,
        "depth": 0,
        "jacobian": None,
        "log_off_hi": format(log_off_hi, "f"),
        "log_off_lo": format(log_off_lo, "f"),
        "log_on_hi": format(log_on_hi, "f"),
        "log_on_lo": format(log_on_lo, "f"),
        "mode": "subdivide",
        "newton_steps": 0,
        "origin": origin,
        "probe_alpha": "1",
        "status": "open",
        "waiting": [],
        "zero_probed": False,
    }


def _logs(basin: dict) -> tuple[Decimal, Decimal, Decimal, Decimal]:
    return (
        Decimal(basin["log_off_lo"]),
        Decimal(basin["log_off_hi"]),
        Decimal(basin["log_on_lo"]),
        Decimal(basin["log_on_hi"]),
    )


def _set_logs(basin: dict, log_off_lo: Decimal, log_off_hi: Decimal, log_on_lo: Decimal, log_on_hi: Decimal) -> None:
    basin["log_off_lo"] = format(quantize_log(log_off_lo), "f")
    basin["log_off_hi"] = format(quantize_log(log_off_hi), "f")
    basin["log_on_lo"] = format(quantize_log(log_on_lo), "f")
    basin["log_on_hi"] = format(quantize_log(log_on_hi), "f")


def _widths(basin: dict) -> tuple[Decimal, Decimal]:
    off_lo, off_hi, on_lo, on_hi = _logs(basin)
    return off_hi - off_lo, on_hi - on_lo


def _clamp_log(value: Decimal) -> Decimal:
    return min(DOMAIN_HI, max(DOMAIN_LO, quantize_log(value)))


def _pair_from_logs(log_off: Decimal, log_on: Decimal) -> tuple[str, str]:
    return text_from_log(_clamp_log(log_off)), text_from_log(_clamp_log(log_on))


def _stencil(basin: dict) -> list[tuple[str, str]]:
    off_lo, off_hi, on_lo, on_hi = _logs(basin)
    if off_hi <= off_lo and on_hi <= on_lo:
        return [_pair_from_logs(off_lo, on_lo)]
    off_mid = (off_lo + off_hi) / 2
    on_mid = (on_lo + on_hi) / 2
    logs = (
        (off_mid, on_mid),
        (off_mid, on_lo),
        (off_mid, on_hi),
        (off_lo, on_mid),
        (off_hi, on_mid),
    )
    found = []
    seen = set()
    for log_off, log_on in logs:
        pair = _pair_from_logs(log_off, log_on)
        if pair not in seen:
            seen.add(pair)
            found.append(pair)
    return found[:5]


def _fd_offsets(basin: dict) -> tuple[Decimal, Decimal]:
    off_width, on_width = _widths(basin)
    off_h = min(Decimal("0.01"), max(off_width / Decimal(4), Decimal("0.0001")))
    on_h = min(Decimal("0.01"), max(on_width / Decimal(4), Decimal("0.0001")))
    return off_h, on_h


def _shifted_pair(log_off: Decimal, log_on: Decimal) -> tuple[str, str]:
    return _pair_from_logs(_clamp_log(log_off), _clamp_log(log_on))


def _jacobian_stencil(basin: dict, points: dict) -> list[tuple[str, str]]:
    best = basin.get("best")
    if best is None:
        return []
    log_off = log_from_text(best["m_off"])
    log_on = log_from_text(best["m_on"])
    if log_off is None or log_on is None:
        return []
    off_h, on_h = _fd_offsets(basin)
    pairs = []
    for shifted_off, shifted_on in (
        (_clamp_log(log_off + off_h), log_on),
        (_clamp_log(log_off - off_h), log_on),
        (log_off, _clamp_log(log_on + on_h)),
        (log_off, _clamp_log(log_on - on_h)),
    ):
        if quantize_log(shifted_off) == quantize_log(log_off) and quantize_log(shifted_on) == quantize_log(log_on):
            continue
        pair = _pair_from_logs(shifted_off, shifted_on)
        if _lookup(points, pair) is None and pair not in pairs and pair != (best["m_off"], best["m_on"]):
            pairs.append(pair)
    return pairs[:4]


def _lookup(points: dict, pair: tuple[str, str]) -> dict | None:
    return points.get(_point_key(*pair))


def _corners(log_off_lo: Decimal, log_off_hi: Decimal, log_on_lo: Decimal, log_on_hi: Decimal) -> list[tuple[str, str]]:
    return [
        _pair_from_logs(log_off_lo, log_on_lo),
        _pair_from_logs(log_off_lo, log_on_hi),
        _pair_from_logs(log_off_hi, log_on_lo),
        _pair_from_logs(log_off_hi, log_on_hi),
    ]


def _cell_encloses(points: dict, target: dict, corners: list[tuple[str, str]]) -> bool:
    rows = [_lookup(points, pair) for pair in corners]
    if any(row is None for row in rows):
        return False
    forward = [_residual(row, target)[0] for row in rows]
    reverse = [_residual(row, target)[1] for row in rows]
    return _spans_zero(forward) and _spans_zero(reverse)


def _grid_index() -> dict[str, int]:
    return {text: index for index, text in enumerate(COARSE_TEXTS)}


def detect_basins(points: dict, target: dict, scales: dict, tolerance: float) -> tuple[list[dict], bool]:
    index = _grid_index()
    cells = []
    for off_index in range(len(COARSE_LOGS) - 1):
        for on_index in range(len(COARSE_LOGS) - 1):
            corners = _corners(
                COARSE_LOGS[off_index],
                COARSE_LOGS[off_index + 1],
                COARSE_LOGS[on_index],
                COARSE_LOGS[on_index + 1],
            )
            if _cell_encloses(points, target, corners):
                distance = min(_distance(_lookup(points, pair), target, scales) for pair in corners)
                cells.append((off_index, on_index, distance))
    seen = set()
    components = []
    for off_index, on_index, _distance_value in cells:
        if (off_index, on_index) in seen:
            continue
        stack = [(off_index, on_index)]
        seen.add((off_index, on_index))
        members = []
        while stack:
            current_off, current_on = stack.pop()
            members.append((current_off, current_on))
            for step_off, step_on in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nxt = (current_off + step_off, current_on + step_on)
                if nxt in seen:
                    continue
                if any(left == nxt[0] and right == nxt[1] for left, right, _value in cells):
                    seen.add(nxt)
                    stack.append(nxt)
        components.append(members)
    ranked = []
    for members in components:
        distance = min(
            next(value for left, right, value in cells if left == off_index and right == on_index)
            for off_index, on_index in members
        )
        off_values = [index for index, _on in members]
        on_values = [index for _off, index in members]
        ranked.append((distance, members, min(off_values), max(off_values), min(on_values), max(on_values)))
    ranked.sort(key=lambda row: (row[0], row[2], row[4]))
    truncated = len(ranked) > MAX_INITIAL_BASINS
    chosen = ranked[:MAX_INITIAL_BASINS]
    covered = set()
    basins = []
    for _component_distance, _members, off_lo, off_hi, on_lo, on_hi in chosen:
        for off_index in range(off_lo, off_hi + 1):
            for on_index in range(on_lo, on_hi + 1):
                covered.add((off_index, on_index))
        basins.append(
            _new_basin(
                f"b{len(basins)}",
                COARSE_LOGS[off_lo],
                COARSE_LOGS[off_hi + 1],
                COARSE_LOGS[on_lo],
                COARSE_LOGS[on_hi + 1],
                "sign_enclosure",
            )
        )
    local = []
    for off_text in COARSE_TEXTS:
        for on_text in COARSE_TEXTS:
            row = _lookup(points, (off_text, on_text))
            if row is None:
                continue
            distance = _distance(row, target, scales)
            off_index = index[off_text]
            on_index = index[on_text]
            smaller = False
            for step_off in (-1, 0, 1):
                for step_on in (-1, 0, 1):
                    if step_off == 0 and step_on == 0:
                        continue
                    neighbor_off = off_index + step_off
                    neighbor_on = on_index + step_on
                    if neighbor_off < 0 or neighbor_on < 0 or neighbor_off >= len(COARSE_TEXTS) or neighbor_on >= len(COARSE_TEXTS):
                        continue
                    neighbor = _lookup(points, (COARSE_TEXTS[neighbor_off], COARSE_TEXTS[neighbor_on]))
                    if neighbor is not None and _distance(neighbor, target, scales) < distance - 1e-15:
                        smaller = True
            if not smaller:
                local.append((off_index, on_index, distance))
    seen_local = set()
    plateaus = []
    for off_index, on_index, distance in local:
        if (off_index, on_index) in seen_local:
            continue
        stack = [(off_index, on_index)]
        seen_local.add((off_index, on_index))
        members = [(off_index, on_index)]
        while stack:
            current_off, current_on = stack.pop()
            for step_off in (-1, 0, 1):
                for step_on in (-1, 0, 1):
                    nxt = (current_off + step_off, current_on + step_on)
                    if nxt in seen_local:
                        continue
                    if any(left == nxt[0] and right == nxt[1] for left, right, _value in local):
                        seen_local.add(nxt)
                        stack.append(nxt)
                        members.append(nxt)
        if any((off_index, on_index) in covered for off_index, on_index in members):
            continue
        plateaus.append(members)
    plateaus.sort(key=lambda members: (min(index for index, _on in members), min(index for _off, index in members)))
    for members in plateaus:
        if len(basins) >= MAX_INITIAL_BASINS:
            truncated = True
            break
        off_values = [index for index, _on in members]
        on_values = [index for _off, index in members]
        off_lo = max(0, min(off_values) - 1)
        off_hi = min(len(COARSE_LOGS) - 1, max(off_values) + 1)
        on_lo = max(0, min(on_values) - 1)
        on_hi = min(len(COARSE_LOGS) - 1, max(on_values) + 1)
        basins.append(_new_basin(f"b{len(basins)}", COARSE_LOGS[off_lo], COARSE_LOGS[off_hi], COARSE_LOGS[on_lo], COARSE_LOGS[on_hi], "local_distance"))
    for off_text in COARSE_TEXTS:
        for on_text in COARSE_TEXTS:
            row = _lookup(points, (off_text, on_text))
            if row is not None and _within(row, target, tolerance):
                log_off = log_from_text(off_text)
                log_on = log_from_text(on_text)
                if log_off is None or log_on is None:
                    continue
                if any(_inside_logs(basin, log_off, log_on) for basin in basins):
                    continue
                if len(basins) >= MAX_INITIAL_BASINS:
                    truncated = True
                    break
                basins.append(_new_basin(f"b{len(basins)}", log_off, log_off, log_on, log_on, "grid_root"))
    return basins, truncated


def _inside_logs(basin: dict, log_off: Decimal, log_on: Decimal) -> bool:
    off_lo, off_hi, on_lo, on_hi = _logs(basin)
    return off_lo - LOG_QUANTUM <= log_off <= off_hi + LOG_QUANTUM and on_lo - LOG_QUANTUM <= log_on <= on_hi + LOG_QUANTUM


def _remember_best(basin: dict, points: dict, target: dict, scales: dict) -> None:
    best = basin.get("best")
    for key, row in points.items():
        m_off, m_on = _split_key(key)
        log_off = log_from_text(m_off)
        log_on = log_from_text(m_on)
        if log_off is None or log_on is None:
            if not basin.get("zero_probed"):
                continue
        elif not _inside_logs(basin, log_off, log_on):
            continue
        distance = _distance(row, target, scales)
        forward, reverse = _residual(row, target)
        candidate = {
            "distance": distance,
            "forward_mismatch": forward,
            "m_off": m_off,
            "m_on": m_on,
            "reverse_mismatch": reverse,
        }
        if best is None or (distance, m_off, m_on) < (best["distance"], best["m_off"], best["m_on"]):
            best = candidate
    basin["best"] = best


def _quadrants(basin: dict) -> list[tuple[Decimal, Decimal, Decimal, Decimal]]:
    off_lo, off_hi, on_lo, on_hi = _logs(basin)
    off_mid = (off_lo + off_hi) / 2
    on_mid = (on_lo + on_hi) / 2
    return [
        (off_lo, off_mid, on_lo, on_mid),
        (off_lo, off_mid, on_mid, on_hi),
        (off_mid, off_hi, on_lo, on_mid),
        (off_mid, off_hi, on_mid, on_hi),
    ]


def _axis_column(center_residual: tuple[float, float], center_log: Decimal, plus_log: Decimal, minus_log: Decimal, plus_residual, minus_residual):
    plus_log = _clamp_log(plus_log)
    minus_log = _clamp_log(minus_log)
    center_log = quantize_log(center_log)
    plus_ok = quantize_log(plus_log) != center_log
    minus_ok = quantize_log(minus_log) != center_log
    if plus_ok and minus_ok:
        if plus_residual is None or minus_residual is None:
            return None
        span = float(plus_log - minus_log)
    elif plus_ok:
        if plus_residual is None:
            return None
        minus_residual = center_residual
        span = float(plus_log - center_log)
    elif minus_ok:
        if minus_residual is None:
            return None
        plus_residual = center_residual
        span = float(center_log - minus_log)
    else:
        return None
    if span == 0.0:
        return None
    return (
        (plus_residual[0] - minus_residual[0]) / span,
        (plus_residual[1] - minus_residual[1]) / span,
    )


def _jacobian_at(basin: dict, points: dict, target: dict) -> dict | None:
    best = basin.get("best")
    if best is None:
        return None
    log_off = log_from_text(best["m_off"])
    log_on = log_from_text(best["m_on"])
    if log_off is None or log_on is None:
        return None
    center = _lookup(points, (best["m_off"], best["m_on"]))
    if center is None:
        return None
    center_residual = _residual(center, target)
    off_h, on_h = _fd_offsets(basin)
    samples = {}
    for name, shifted_off, shifted_on in (
        ("off_plus", log_off + off_h, log_on),
        ("off_minus", log_off - off_h, log_on),
        ("on_plus", log_off, log_on + on_h),
        ("on_minus", log_off, log_on - on_h),
    ):
        samples[name] = _lookup(points, _shifted_pair(shifted_off, shifted_on))
    off_column = _axis_column(
        center_residual,
        log_off,
        log_off + off_h,
        log_off - off_h,
        None if samples["off_plus"] is None else _residual(samples["off_plus"], target),
        None if samples["off_minus"] is None else _residual(samples["off_minus"], target),
    )
    on_column = _axis_column(
        center_residual,
        log_on,
        log_on + on_h,
        log_on - on_h,
        None if samples["on_plus"] is None else _residual(samples["on_plus"], target),
        None if samples["on_minus"] is None else _residual(samples["on_minus"], target),
    )
    if off_column is None or on_column is None:
        return None
    matrix = np.array(
        [
            [off_column[0], on_column[0]],
            [off_column[1], on_column[1]],
        ],
        dtype=float,
    )
    singular = np.linalg.svd(matrix, compute_uv=False)
    smallest = float(singular[-1]) if len(singular) else 0.0
    largest = float(singular[0]) if len(singular) else 0.0
    condition = None if smallest == 0.0 else largest / smallest
    return {
        "condition_number": condition,
        "determinant": float(np.linalg.det(matrix)),
        "matrix": matrix.tolist(),
        "singular_values": [float(value) for value in singular],
    }


def _newton_trial(basin: dict, points: dict, target: dict) -> tuple[str, str] | None:
    best = basin.get("best")
    jacobian = _jacobian_at(basin, points, target)
    basin["jacobian"] = jacobian
    if best is None or jacobian is None:
        return None
    matrix = np.array(jacobian["matrix"], dtype=float)
    residual = np.array([best["forward_mismatch"], best["reverse_mismatch"]], dtype=float)
    try:
        step = np.linalg.solve(matrix, -residual)
    except np.linalg.LinAlgError:
        return None
    if not np.all(np.isfinite(step)):
        return None
    alpha = Decimal(basin.get("probe_alpha") or "1")
    log_off = log_from_text(best["m_off"])
    log_on = log_from_text(best["m_on"])
    if log_off is None or log_on is None:
        return None
    trial_off = _clamp_log(log_off + alpha * Decimal(str(float(step[0]))))
    trial_on = _clamp_log(log_on + alpha * Decimal(str(float(step[1]))))
    pair = _pair_from_logs(trial_off, trial_on)
    if pair == (best["m_off"], best["m_on"]):
        return None
    return pair


def _zero_probes(basin: dict) -> list[tuple[str, str]]:
    best = basin.get("best")
    if best is None or basin.get("zero_probed"):
        return []
    probes = []
    if best["m_off"] in {COARSE_TEXTS[0], COARSE_TEXTS[-1]} or best["m_on"] in {COARSE_TEXTS[0], COARSE_TEXTS[-1]}:
        probes.append(("0", best["m_on"]))
        probes.append((best["m_off"], "0"))
        probes.append(("0", "0"))
    return probes


def _waiting_missing(basin: dict, points: dict) -> list[tuple[str, str]]:
    missing = []
    for raw in basin.get("waiting") or []:
        pair = (raw[0], raw[1])
        if _lookup(points, pair) is None and pair not in missing:
            missing.append(pair)
    return missing


def _assign_waiting(basin: dict, pairs: list[tuple[str, str]], points: dict) -> None:
    waiting = []
    for pair in pairs:
        if _lookup(points, pair) is None and list(pair) not in waiting:
            waiting.append(list(pair))
    basin["waiting"] = waiting[:9]


def _consume(basin: dict, points: dict, target: dict, scales: dict, tolerance: float, siblings: list[dict]) -> None:
    _remember_best(basin, points, target, scales)
    best = basin.get("best")
    if best is not None and abs(best["forward_mismatch"]) <= tolerance and abs(best["reverse_mismatch"]) <= tolerance:
        jacobian = _jacobian_at(basin, points, target)
        if jacobian is None:
            _assign_waiting(basin, _jacobian_stencil(basin, points), points)
            if basin["waiting"]:
                basin["mode"] = "jacobian"
                return
            basin["jacobian"] = {"condition_number": None, "determinant": None, "singular_values": [], "status": "not_estimated"}
        else:
            basin["jacobian"] = jacobian
        basin["status"] = "solved"
        basin["waiting"] = []
        return
    probes = _zero_probes(basin)
    if probes:
        missing = [pair for pair in probes if _lookup(points, pair) is None]
        if missing:
            basin["mode"] = "zero"
            _assign_waiting(basin, missing, points)
            return
        basin["zero_probed"] = True
        _remember_best(basin, points, target, scales)
        best = basin["best"]
        if best is not None and abs(best["forward_mismatch"]) <= tolerance and abs(best["reverse_mismatch"]) <= tolerance:
            basin["status"] = "solved"
            basin["waiting"] = []
            return
    off_width, on_width = _widths(basin)
    # Newton starts only after both log10 widths are inside the frozen bound.
    # An empty stencil means those points are already stored, so keep splitting.
    if max(off_width, on_width) > NEWTON_WIDTH:
        quadrants = []
        for off_lo, off_hi, on_lo, on_hi in _quadrants(basin):
            corners = _corners(off_lo, off_hi, on_lo, on_hi)
            distance = None
            rows = [_lookup(points, pair) for pair in corners]
            if all(row is not None for row in rows):
                distance = min(_distance(row, target, scales) for row in rows)
            enclosed = _cell_encloses(points, target, corners)
            quadrants.append((enclosed, distance if distance is not None else 1e300, off_lo, off_hi, on_lo, on_hi))
        enclosed = [row for row in quadrants if row[0]]
        pool = enclosed or [row for row in quadrants if row[1] < 1e300]
        if not pool:
            basin["status"] = "exhausted"
            basin["waiting"] = []
            return
        pool.sort(key=lambda row: (row[1], format(row[2], "f"), format(row[4], "f")))
        keep = pool[0]
        previous = _logs(basin)
        _set_logs(basin, keep[2], keep[3], keep[4], keep[5])
        basin["depth"] = int(basin["depth"]) + 1
        basin["mode"] = "subdivide"
        if _logs(basin) == previous:
            basin["status"] = "exhausted"
            basin["waiting"] = []
            return
        for extra in pool[1:]:
            if len(siblings) >= MAX_INITIAL_BASINS:
                break
            child = _new_basin(f"b{len(siblings)}", extra[2], extra[3], extra[4], extra[5], "split")
            child["depth"] = basin["depth"]
            siblings.append(child)
        _assign_waiting(basin, _stencil(basin), points)
        return
    if basin["mode"] != "newton":
        basin["mode"] = "newton"
        basin["probe_alpha"] = "1"
        _assign_waiting(basin, _jacobian_stencil(basin, points), points)
        if basin["waiting"]:
            return
    # A missing finite-difference sample is a request, not an exhausted basin.
    if _jacobian_at(basin, points, target) is None:
        _assign_waiting(basin, _jacobian_stencil(basin, points), points)
        if basin["waiting"]:
            return
        trial = None
    else:
        trial = _newton_trial(basin, points, target)
        basin["newton_steps"] = int(basin.get("newton_steps") or 0) + 1
    if trial is None or basin["newton_steps"] > 12:
        probes = [] if basin.get("zero_probed") else _zero_probes(basin)
        missing = [pair for pair in probes if _lookup(points, pair) is None]
        if missing:
            basin["mode"] = "zero"
            _assign_waiting(basin, missing, points)
            return
        if probes:
            basin["zero_probed"] = True
            _remember_best(basin, points, target, scales)
            best = basin.get("best")
            if best is not None and abs(best["forward_mismatch"]) <= tolerance and abs(best["reverse_mismatch"]) <= tolerance:
                basin["status"] = "solved"
                basin["waiting"] = []
                return
        basin["status"] = "exhausted"
        basin["waiting"] = []
        return
    current = _lookup(points, trial)
    if current is None:
        _assign_waiting(basin, [trial], points)
        return
    forward, reverse = _residual(current, target)
    trial_distance = _distance(current, target, scales)
    if abs(forward) <= tolerance and abs(reverse) <= tolerance:
        basin["best"] = {
            "distance": trial_distance,
            "forward_mismatch": forward,
            "m_off": trial[0],
            "m_on": trial[1],
            "reverse_mismatch": reverse,
        }
        basin["mode"] = "jacobian"
        _assign_waiting(basin, _jacobian_stencil(basin, points), points)
        if not basin["waiting"]:
            basin["status"] = "solved"
        return
    if best is not None and trial_distance < best["distance"]:
        basin["best"] = {
            "distance": trial_distance,
            "forward_mismatch": forward,
            "m_off": trial[0],
            "m_on": trial[1],
            "reverse_mismatch": reverse,
        }
        trial_off = log_from_text(trial[0])
        trial_on = log_from_text(trial[1])
        if trial_off is not None and trial_on is not None:
            _set_logs(basin, trial_off, trial_off, trial_on, trial_on)
        basin["probe_alpha"] = "1"
        _assign_waiting(basin, _jacobian_stencil(basin, points), points)
        return
    alpha = Decimal(basin.get("probe_alpha") or "1") / 2
    basin["probe_alpha"] = format(alpha, "f")
    if alpha < Decimal(1) / Decimal(1024):
        basin["status"] = "exhausted"
        basin["waiting"] = []


def fresh_calibration(problem: dict) -> dict:
    return {
        "adaptive_count": 0,
        "adaptive_keys": [],
        "basins": [],
        "basins_truncated": False,
        "calibration_id": problem["calibration_id"],
        "nominal": problem["nominal"],
        "role": problem.get("role", "primary"),
        "selected_solution": None,
        "selection_reason": None,
        "solution_count": 0,
        "solutions": [],
        "status": "needs_coarse",
        "structure_id": problem["structure_id"],
        "target_id": problem["target_id"],
    }


def coarse_complete(points: dict) -> bool:
    return all(_point_key(left, right) in points for left, right in COARSE_PAIRS)


def _apply_cap(state: dict, pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Accept a whole next stencil or stop. A stencil that does not fit is not partial."""
    counted = set(state.get("adaptive_keys") or [])
    already = []
    fresh = []
    for pair in pairs:
        key = _point_key(*pair)
        if key in counted:
            if pair not in already:
                already.append(pair)
        elif pair not in fresh:
            fresh.append(pair)
    stencil = fresh[:9]
    room = ADAPTIVE_CAP - len(counted)
    if stencil and len(stencil) > room:
        if already:
            return already
        state["status"] = "unresolved_at_cap"
        return []
    for pair in stencil:
        counted.add(_point_key(*pair))
    state["adaptive_count"] = len(counted)
    state["adaptive_keys"] = sorted(counted)
    return already + stencil


def _boundary_class(m_off: str, m_on: str) -> str:
    if m_off == "0" or m_on == "0":
        return "zero-boundary solution"
    logs = [log_from_text(m_off), log_from_text(m_on)]
    if any(value is None for value in logs):
        return "zero-boundary solution"
    endpoint = {DOMAIN_LO, DOMAIN_HI}
    if any(quantize_log(value) in endpoint for value in logs):
        return "finite boundary solution"
    return "finite interior solution"


def _log_departure(m_off: str, m_on: str, nominal: str) -> tuple[float, float, str, str]:
    """Lexicographic distance from the named nominal multiplier.

    A nominal of zero uses Generation 7's rule: deletion is closer than every
    positive multiplier, and positive candidates are ordered by the multiplier
    itself. The returned Euclidean coordinate is the same pair of distances.
    """
    nominal_value = parse_multiplier_text(nominal)
    departures = [log_distance(parse_multiplier_text(text), nominal_value) for text in (m_off, m_on)]
    chebyshev = max(departures)
    euclidean = math.hypot(departures[0], departures[1])
    return chebyshev, euclidean, m_off, m_on


def _neutral_distance(m_off: str, m_on: str) -> float | None:
    if m_off == "0" or m_on == "0":
        return None
    off = math.log(float(parse_multiplier_text(m_off)))
    on = math.log(float(parse_multiplier_text(m_on)))
    return math.sqrt(off * off + on * on)


def _cluster_key(solution: dict) -> tuple:
    off = log_from_text(solution["m_off"])
    on = log_from_text(solution["m_on"])
    if off is None or on is None:
        return (solution["m_off"], solution["m_on"])
    return (quantize_log(off / CLUSTER_LOG10), quantize_log(on / CLUSTER_LOG10))


def _same_cluster(left: dict, right: dict) -> bool:
    if left["m_off"] == "0" or left["m_on"] == "0" or right["m_off"] == "0" or right["m_on"] == "0":
        return left["m_off"] == right["m_off"] and left["m_on"] == right["m_on"]
    off_left = log_from_text(left["m_off"])
    off_right = log_from_text(right["m_off"])
    on_left = log_from_text(left["m_on"])
    on_right = log_from_text(right["m_on"])
    if None in {off_left, off_right, on_left, on_right}:
        return False
    return max(abs(off_left - off_right), abs(on_left - on_right)) <= CLUSTER_LOG10


def _select(solutions: list[dict], nominal: str) -> tuple[dict | None, str]:
    if not solutions:
        return None, "no solution inside tolerance"
    ordered = sorted(solutions, key=lambda row: _log_departure(row["m_off"], row["m_on"], nominal))
    chosen = ordered[0]
    if parse_multiplier_text(nominal) == 0:
        reason = "least departure under the zero-nominal rule, then parameter text"
    else:
        reason = "least absolute log departure from the named nominal multiplier, then Euclidean log distance, then parameter text"
    return chosen, reason


def _label(solutions: list[dict], status: str) -> str:
    if status == "unresolved_at_cap" and not solutions:
        return "unresolved"
    if not solutions:
        return "R0"
    interior = [row for row in solutions if row["boundary_class"] == "finite interior solution"]
    if not interior:
        return "R1"
    if len(solutions) >= 2:
        return "R3"
    condition = solutions[0].get("condition_number")
    if condition is None or condition > CONDITION_LIMIT:
        return "R4"
    return "R2"


def _finalize(state: dict, nominal: str, points: dict | None = None, target: dict | None = None, scales: dict | None = None, tolerance: float = MATCH_TOLERANCE) -> None:
    solved = []
    for basin in state["basins"]:
        best = basin.get("best")
        if basin.get("status") != "solved" or best is None:
            continue
        jacobian = basin.get("jacobian") or {}
        solved.append(
            {
                "basin_id": basin["basin_id"],
                "boundary_class": _boundary_class(best["m_off"], best["m_on"]),
                "condition_number": jacobian.get("condition_number"),
                "d_neutral": _neutral_distance(best["m_off"], best["m_on"]),
                "determinant": jacobian.get("determinant"),
                "distance": best["distance"],
                "forward_mismatch": best["forward_mismatch"],
                "m_off": best["m_off"],
                "m_on": best["m_on"],
                "origin": basin.get("origin"),
                "reverse_mismatch": best["reverse_mismatch"],
                "singular_values": jacobian.get("singular_values"),
            }
        )
    if points is not None and target is not None and scales is not None:
        for key in sorted(points):
            row = points[key]
            if not _within(row, target, tolerance):
                continue
            m_off, m_on = _split_key(key)
            if any(_same_cluster({"m_off": m_off, "m_on": m_on}, kept) for kept in solved):
                continue
            forward, reverse = _residual(row, target)
            solved.append(
                {
                    "basin_id": f"point:{m_off}:{m_on}",
                    "boundary_class": _boundary_class(m_off, m_on),
                    "condition_number": None,
                    "d_neutral": _neutral_distance(m_off, m_on),
                    "determinant": None,
                    "distance": _distance(row, target, scales),
                    "forward_mismatch": forward,
                    "m_off": m_off,
                    "m_on": m_on,
                    "origin": "stored_point",
                    "reverse_mismatch": reverse,
                    "singular_values": None,
                }
            )
    clusters: list[dict] = []
    for solution in solved:
        if any(_same_cluster(solution, kept) for kept in clusters):
            continue
        clusters.append(solution)
    state["solutions"] = clusters
    state["solution_count"] = len(clusters)
    selected, reason = _select(clusters, nominal)
    state["selected_solution"] = selected
    state["selection_reason"] = reason
    if state.get("status") != "unresolved_at_cap":
        state["status"] = "represented" if clusters else "unrepresented"
    state["representation_label"] = _label(clusters, state["status"])


def step_problem(state: dict, points: dict, target: dict, scales: dict, tolerance: float = MATCH_TOLERANCE) -> tuple[dict, list[tuple[str, str]]]:
    """Advance a calibration using stored points only.

    Waves that need no new kernel point are consumed immediately. A wave that
    needs points returns those requests and stops.
    """
    if state.get("status") in TERMINAL_STATUSES:
        return state, []
    for _wave in range(48):
        state, requests = _step_once(state, points, target, scales, tolerance)
        if requests or state.get("status") in TERMINAL_STATUSES | {"needs_coarse"}:
            return state, requests
    return state, []


def _step_once(state: dict, points: dict, target: dict, scales: dict, tolerance: float) -> tuple[dict, list[tuple[str, str]]]:
    if state.get("status") in TERMINAL_STATUSES:
        return state, []
    if not coarse_complete(points):
        state["status"] = "needs_coarse"
        return state, []
    if not state.get("basins"):
        basins, truncated = detect_basins(points, target, scales, tolerance)
        state["basins"] = basins
        state["basins_truncated"] = truncated
        state["status"] = "refining"
        for basin in state["basins"]:
            _remember_best(basin, points, target, scales)
            best = basin.get("best")
            if best is not None and abs(best["forward_mismatch"]) <= tolerance and abs(best["reverse_mismatch"]) <= tolerance:
                _assign_waiting(basin, _jacobian_stencil(basin, points), points)
                basin["mode"] = "jacobian"
                if not basin["waiting"]:
                    basin["jacobian"] = _jacobian_at(basin, points, target) or {
                        "condition_number": None,
                        "status": "not_estimated",
                    }
                    basin["status"] = "solved"
            else:
                _assign_waiting(basin, _stencil(basin), points)
                basin["mode"] = "subdivide"
    else:
        index = 0
        while index < len(state["basins"]):
            basin = state["basins"][index]
            if basin.get("status") == "open" and not _waiting_missing(basin, points):
                _consume(basin, points, target, scales, tolerance, state["basins"])
            index += 1
    if state.get("status") == "unresolved_at_cap":
        _finalize(state, state["nominal"], points, target, scales, tolerance)
        state["status"] = "unresolved_at_cap"
        return state, []
    open_basins = [basin for basin in state["basins"] if basin.get("status") == "open"]
    if not open_basins:
        _finalize(state, state["nominal"], points, target, scales, tolerance)
        return state, []
    requested = []
    for basin in open_basins:
        for pair in _waiting_missing(basin, points):
            if pair not in requested:
                requested.append(pair)
    accepted = _apply_cap(state, requested)
    if state.get("status") == "unresolved_at_cap":
        for basin in state["basins"]:
            if basin.get("status") == "open":
                basin["status"] = "capped"
                basin["waiting"] = []
        _finalize(state, state["nominal"], points, target, scales, tolerance)
        state["status"] = "unresolved_at_cap"
        return state, []
    state["status"] = "refining"
    return state, accepted


def composition_ids(state: dict) -> list[str]:
    solutions = list(state.get("solutions") or [])
    if not solutions:
        return []
    if len(solutions) <= SMALL_SOLUTION_FAMILY:
        return [row["basin_id"] for row in solutions]
    selected = state.get("selected_solution") or solutions[0]
    finite = [row for row in solutions if row["m_off"] != "0" and row["m_on"] != "0"] or solutions
    neutral = min(finite, key=lambda row: (row.get("d_neutral") if row.get("d_neutral") is not None else 1e300, row["m_off"], row["m_on"]))
    distant = max(finite, key=lambda row: _log_departure(row["m_off"], row["m_on"], state["nominal"]))
    chosen = []
    for row in (selected, neutral, distant):
        if row["basin_id"] not in chosen:
            chosen.append(row["basin_id"])
    return chosen


def scales_for(target: dict) -> dict:
    return joint_scales(
        float(target["delta_forward"]),
        float(target["delta_reverse"]),
        float(target.get("q0_forward", 0.0)),
        float(target.get("q0_reverse", 0.0)),
        SCALE_FLOOR,
    )


def _direction_block(pack: dict, baseline: dict, table) -> dict:
    out = {}
    for key, source_name, target_name in _direction_names(table):
        solved = _cached_direction(pack, baseline, source_name, target_name, RECONFIGURATION_HORIZON)
        base = _cached_direction(baseline, baseline, source_name, target_name, RECONFIGURATION_HORIZON)
        q = solved["q_controlled"]
        q0 = base["q_controlled"]
        spread = solved["triad"].get("spread")
        out[key] = {
            "Q": None if q is None else float(q),
            "Q0": None if q0 is None else float(q0),
            "delta": None if q is None or q0 is None else float(q - q0),
            "mu": _num(base["mu_ref"]),
            "q": _num(solved["q"]),
            "q0": _num(base["q"]),
            "residual": float(solved["solver"]["residual"] or 0.0),
            "spread": None if spread is None else float(spread),
        }
    return out


def solve_pair_point(off_rule: Constraint, on_rule: Constraint, m_off: Fraction, m_on: Fraction, alphabet: str, rho: Fraction, slots, cache: dict) -> dict:
    factors = {M_OFF: m_off, M_ON: m_on}
    baseline = _baseline_pack(BASELINE_FACTORS, rho, slots, cache)
    pack = _constrained_pack((off_rule, on_rule), factors, rho, slots, cache)
    directions = _direction_block(pack, baseline, baseline["table"])
    _release_landings(cache)
    return {
        "alphabet": alphabet,
        "directions": directions,
        "m_off": multiplier_text(m_off),
        "m_on": multiplier_text(m_on),
        "n_pairs": int(baseline["n_pairs"]),
        "off_expression": off_rule.expression(slots),
        "on_expression": on_rule.expression(slots),
        "rho": str(rho),
        "solver_residuals": {
            "epoch_defect": float(pack["defect"]),
            "stationary": float(pack["residual"]),
        },
        "triad_spread": {name: directions[name]["spread"] for name in DIRECTIONS},
    }


def solve_target_composition(target: Constraint, companion: Constraint, alphabet: str, rho: Fraction, slots, cache: dict, floor: float) -> dict:
    del floor
    factors = factors_for(alphabet, None)
    baseline = _baseline_pack(BASELINE_FACTORS, rho, slots, cache)
    packs = {
        "0": baseline,
        "C": _constrained_pack((target,), factors, rho, slots, cache),
        "P": _constrained_pack((companion,), factors, rho, slots, cache),
        "CP": _constrained_pack((target, companion), factors, rho, slots, cache),
    }
    return _composition_payload(packs, baseline, alphabet, rho, slots, cache, None, None)


def solve_control_composition(off_rule: Constraint, on_rule: Constraint, companion: Constraint, m_off: Fraction, m_on: Fraction, alphabet: str, rho: Fraction, slots, cache: dict) -> dict:
    named = factors_for(alphabet, None)
    control = {M_OFF: m_off, M_ON: m_on}
    combined = dict(named)
    combined.update(control)
    baseline = _baseline_pack(BASELINE_FACTORS, rho, slots, cache)
    packs = {
        "0": baseline,
        "C": _constrained_pack((off_rule, on_rule), control, rho, slots, cache),
        "P": _constrained_pack((companion,), named, rho, slots, cache),
        "CP": _constrained_pack((off_rule, on_rule, companion), combined, rho, slots, cache),
    }
    return _composition_payload(packs, baseline, alphabet, rho, slots, cache, multiplier_text(m_off), multiplier_text(m_on))


def _composition_payload(packs: dict, baseline: dict, alphabet: str, rho: Fraction, slots, cache: dict, m_off: str | None, m_on: str | None) -> dict:
    table = baseline["table"]
    directions = {}
    for key, source_name, target_name in _direction_names(table):
        solved = {label: _cached_direction(pack, baseline, source_name, target_name, RECONFIGURATION_HORIZON) for label, pack in packs.items()}
        q0 = solved["0"]["q_controlled"]
        qc = solved["C"]["q_controlled"]
        qp = solved["P"]["q_controlled"]
        qcp = solved["CP"]["q_controlled"]
        spread_c = solved["C"]["triad"].get("spread")
        spread_cp = solved["CP"]["triad"].get("spread")
        directions[key] = {
            "G": super_singleton_gap(float(qcp - q0), float(qc - q0), float(qp - q0)),
            "I": interaction_residual(qcp, qc, qp, q0),
            "Q0": float(q0),
            "QC": float(qc),
            "QCP": float(qcp),
            "QP": float(qp),
            "delta_C": float(qc - q0),
            "delta_CP": float(qcp - q0),
            "delta_P": float(qp - q0),
            "delta_S": None if spread_c is None or spread_cp is None else float(spread_cp - spread_c),
            "spread_C": None if spread_c is None else float(spread_c),
            "spread_CP": None if spread_cp is None else float(spread_cp),
        }
    violations = _support_violations(packs["CP"]["kernel"], packs["C"]["kernel"])
    violations += _support_violations(packs["CP"]["kernel"], packs["P"]["kernel"])
    _release_landings(cache)
    return {
        "alphabet": alphabet,
        "directions": directions,
        "m_off": m_off,
        "m_on": m_on,
        "rho": str(rho),
        "solver_residuals": {"epoch_defect": float(packs["CP"]["defect"]), "stationary": float(packs["CP"]["residual"])},
        "support_violations": int(violations),
    }


def complexity_rows() -> list[dict]:
    names = (
        "predicate_order",
        "rule_count",
        "fitted_parameters",
        "partition_size",
        "action_edges",
        "history_depth",
        "geometry",
    )
    return [
        {"model": "higher_order_singleton", **dict(zip(names, COMPLEXITY_TARGET))},
        {"model": "two_level_pair_face", **dict(zip(names, COMPLEXITY_CONTROL))},
    ]
