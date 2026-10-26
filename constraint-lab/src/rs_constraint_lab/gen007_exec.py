"""Generation 7 executor for the micro-batch supervisor.

An item is one structure, one multiplier, and one rho. Calibration replays
from those files. A missing multiplier becomes the next item. No item walks
the multiplier grid inside itself.
"""

from __future__ import annotations

import math
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

from rs_constraint_lab.constraints import parse_expression
from rs_constraint_lab.reconfiguration import RECONFIGURATION_HORIZON
from rs_constraint_lab.durable import atomic_write_json, json_ready, read_json, sha256_bytes
from rs_constraint_lab.spec import load_spec, spec_hash
from rs_constraint_lab.v05 import (
    _baseline_pack,
    _constrained_pack,
    _factors_key,
    _grammar,
    _num,
    _release_landings,
    require_effect_floor,
)
from rs_constraint_lab.v06 import WEIGHT_ORDER, graded_catalogue
from rs_constraint_lab.v07 import (
    ANALYSIS_VERSION,
    BASELINE_FACTORS,
    CALIBRATION_VERSION,
    CALIBRATION_WEIGHT,
    CELL_INDEX,
    DIRECTIONS,
    GRID_SHA256,
    M_MAX,
    M_MIN,
    POSITIVE_GRID,
    PRIMARY_RHO,
    ROBUSTNESS_CELLS,
    _catalogue_view,
    _composed_target,
    _composition_numbers,
    _live_controls,
    _pack_directions,
    _require_v07_spec,
    _shape_for,
    _strategy_multiplier,
    calibrate_control,
    coverage_plan,
    factors_for,
    joint_distance,
    joint_scales,
    multiplier_text,
    nominal_multiplier,
    parse_multiplier_text,
    require_multiplier,
    selected_records,
    stabilise_multiplier,
    summarise_calibrated,
)
from rs_constraint_lab.version import HYPERGRAPH_N4_SEMANTIC_VERSION
from rs_constraint_lab.workstore import (
    Layout,
    load_state,
    log_event,
    log_progress,
    make_item_record,
    read_valid_item,
    utc_now,
    work_index,
)

TERMINAL = {"converged", "smoke_capped", "blocked"}
SPEC_PATH = Path(__file__).resolve().parents[2] / "experiments" / "specs" / "generation-007.json"
_WORLD: dict = {}


class MissingPoint(Exception):
    """The next multiplier is not on disk. The caller schedules that item and stops."""

    def __init__(self, expression: str, multiplier: Fraction, rho: str, alphabet: str):
        self.expression = expression
        self.multiplier = multiplier
        self.rho = rho
        self.alphabet = alphabet
        super().__init__(f"missing {expression} m={multiplier_text(multiplier)} rho={rho} alphabet={alphabet}")


def choose_batch_count(samples: list[float]) -> int:
    """Item count for a 30–60s batch. One item when a single evaluation is already slow."""
    if not samples:
        return 1
    ordered = sorted(float(value) for value in samples)
    p90 = _percentile(ordered, 0.90)
    maximum = ordered[-1]
    if p90 <= 0 or p90 > 60:
        return 1
    count = max(1, int(45 // p90))
    while count > 1 and (count * p90 > 60 or count * maximum > 100):
        count -= 1
    return count


def _percentile(ordered: list[float], fraction: float) -> float:
    index = min(len(ordered) - 1, max(0, math.ceil(fraction * len(ordered)) - 1))
    return ordered[index]


def _spec() -> dict:
    if "spec" not in _WORLD:
        data = load_spec(SPEC_PATH)
        _require_v07_spec(data)
        _WORLD["spec"] = data
        _WORLD["spec_hash"] = spec_hash(data)
    return _WORLD["spec"]


def _digest() -> str:
    _spec()
    return _WORLD["spec_hash"]


def _world() -> dict:
    if "records" not in _WORLD:
        spec = _spec()
        grammar = _grammar(WEIGHT_ORDER, 4)
        slots = grammar.slot_list()
        catalogue = graded_catalogue(_catalogue_view(spec))
        _WORLD["slots"] = slots
        _WORLD["records"] = selected_records(catalogue)
        _WORLD["coverage"] = coverage_plan(catalogue)
    return _WORLD


def _rule(expression: str):
    return parse_expression(expression, 4, order=3)


def _note(context: dict | None, key, cache: dict) -> None:
    if context is None:
        return
    if key in cache:
        context["cache_hits"] = int(context.get("cache_hits", 0)) + 1
    else:
        context["cache_misses"] = int(context.get("cache_misses", 0)) + 1


def _direction_public(solved: dict, baseline_direction: dict) -> dict:
    q = solved["q_controlled"]
    q0 = baseline_direction["q_controlled"]
    spread = solved["triad"].get("spread")
    return {
        "Q": None if q is None else float(q),
        "Q0": None if q0 is None else float(q0),
        "delta": None if q is None or q0 is None else float(q - q0),
        "mu": _num(baseline_direction["mu_ref"]),
        "q": _num(solved["q"]),
        "q0": _num(baseline_direction["q"]),
        "residual": float(solved["solver"]["residual"] or 0.0),
        "spread": None if spread is None else float(spread),
    }


def solve_singleton(rule, multiplier: Fraction, alphabet: str, rho: Fraction, slots, cache: dict, context: dict | None = None) -> dict:
    """One structure at one multiplier. Both passage directions. No grid."""
    require_multiplier(multiplier, allow_zero=True)
    if rule.weight == CALIBRATION_WEIGHT:
        factors = {CALIBRATION_WEIGHT: multiplier}
    else:
        factors = factors_for(alphabet, None)
    baseline_key = ("baseline", _factors_key(BASELINE_FACTORS), str(rho))
    _note(context, baseline_key, cache)
    baseline = _baseline_pack(BASELINE_FACTORS, rho, slots, cache)
    rule_key = ((rule.key(),), _factors_key(factors), str(rho))
    _note(context, rule_key, cache)
    pack = _constrained_pack((rule,), factors, rho, slots, cache)
    table = baseline["table"]
    from rs_constraint_lab.v05 import _cached_direction, _direction_names

    directions = {}
    for key, source_name, target_name in _direction_names(table):
        solved = _cached_direction(pack, baseline, source_name, target_name, RECONFIGURATION_HORIZON)
        base = _cached_direction(baseline, baseline, source_name, target_name, RECONFIGURATION_HORIZON)
        directions[key] = _direction_public(solved, base)
    _release_landings(cache)
    residuals = {
        "committor_matching_to_path": directions["matching_to_path"]["residual"],
        "committor_path_to_matching": directions["path_to_matching"]["residual"],
        "epoch_defect": float(pack["defect"]),
        "stationary": float(pack["residual"]),
    }
    return {
        "alphabet": alphabet,
        "directions": directions,
        "expression": rule.expression(slots),
        "multiplier": multiplier_text(multiplier) if rule.weight == CALIBRATION_WEIGHT else None,
        "n_pairs": int(baseline["n_pairs"]),
        "rho": str(rho),
        "solver_residuals": residuals,
        "triad_spread": {name: directions[name]["spread"] for name in DIRECTIONS},
    }


def _compact(result: dict, item_id: str, kind: str) -> dict:
    directions = {}
    for name, row in result["directions"].items():
        directions[name] = {key: row[key] for key in ("Q", "Q0", "delta", "residual", "spread")}
    return {
        "alphabet": result["alphabet"],
        "directions": directions,
        "expression": result["expression"],
        "item_id": item_id,
        "kind": kind,
        "multiplier": result.get("multiplier"),
        "n_pairs": result["n_pairs"],
        "rho": result["rho"],
        "solver_residuals": result["solver_residuals"],
        "triad_spread": result["triad_spread"],
    }


class PointIndex:
    def __init__(self, layout: Layout):
        self.layout = layout
        self.by_key: dict[tuple, dict] = {}

    def load(self) -> None:
        state = load_state(self.layout)
        index = work_index(self.layout)
        folder = self.layout.cache() / "points"
        folder.mkdir(parents=True, exist_ok=True)
        for record in index.values():
            if record["kind"] not in {"multiplier", "target_singleton"}:
                continue
            if state.get(record["item_id"], {}).get("status") != "complete":
                continue
            path = folder / f"{record['item_id']}.json"
            if not path.exists():
                payload = read_valid_item(self.layout, record["item_id"], _digest())
                if payload is None:
                    continue
                atomic_write_json(path, _compact(payload["result"], record["item_id"], record["kind"]))
            row = read_json(path)
            item_input = record["input"]
            key = (
                record["kind"],
                item_input.get("expression") or item_input.get("c_expression"),
                item_input.get("multiplier"),
                item_input["rho"],
                item_input["alphabet"],
            )
            self.by_key[key] = row

    def multiplier(self, expression: str, text: str, rho: str, alphabet: str) -> dict | None:
        return self.by_key.get(("multiplier", expression, text, rho, alphabet))

    def singleton(self, expression: str, rho: str, alphabet: str) -> dict | None:
        return self.by_key.get(("target_singleton", expression, None, rho, alphabet))


class DiskBook:
    """Reads persisted multiplier points. A miss raises MissingPoint and solves nothing."""

    def __init__(self, slots, alphabet: str, rho: str, index: PointIndex):
        self.slots = slots
        self.alphabet = alphabet
        self.rho = rho
        self.index = index
        self.cache: dict = {}
        self.evaluations = 0

    def curve(self, rule) -> dict:
        expression = rule.expression(self.slots)
        points = {multiplier_text(multiplier): self._require(expression, multiplier) for multiplier in POSITIVE_GRID}
        zero = self._require(expression, Fraction(0))
        return {"points": points, "zero": zero, "structure": rule.structural_key()}

    def evaluate(self, rule, multiplier: Fraction) -> dict:
        return self._require(rule.expression(self.slots), multiplier)

    def _require(self, expression: str, multiplier: Fraction) -> dict:
        if multiplier != 0:
            multiplier = require_multiplier(stabilise_multiplier(multiplier))
        text = multiplier_text(multiplier)
        row = self.index.multiplier(expression, text, self.rho, self.alphabet)
        if row is None:
            raise MissingPoint(expression, multiplier, self.rho, self.alphabet)
        return row["directions"]


def _problems_for(records, slots, *, role: str, rho: str, alphabet: str, erasure: bool, face: bool) -> list[dict]:
    problems = []
    grammar = _grammar(WEIGHT_ORDER, 4)
    for record in records:
        target, companion, controls = _live_controls(record, grammar, slots)
        chosen = []
        for control in controls:
            if control["control_type"] == "erasure" and erasure:
                chosen.append(control)
            if control["control_type"] == "pair_face" and face:
                chosen.append(control)
                if role == "smoke":
                    break
        target_expression = target.expression(slots)
        for control in chosen:
            expression = control["rule"].expression(slots)
            identity = {
                "alphabet": alphabet,
                "control_expression": expression,
                "relation": control["relation"],
                "rho": rho,
                "target_id": record["target_id"],
            }
            problems.append(
                {
                    "alphabet": alphabet,
                    "calibration_id": sha256_bytes(json_ready_text(identity).encode("utf-8")),
                    "cell": CELL_INDEX[(record["w_P"], record["w_T"])],
                    "control_expression": expression,
                    "control_type": control["control_type"],
                    "face": control.get("face"),
                    "geometry": record["geometry"],
                    "nominal": multiplier_text(nominal_multiplier(record["w_T"], alphabet)),
                    "p_expression": companion.expression(slots),
                    "polarity": record["polarity"],
                    "relation": control["relation"],
                    "rho": rho,
                    "role": "primary" if role != "robustness" else "robustness",
                    "t_expression": target_expression,
                    "target_id": record["target_id"],
                    "w_P": record["w_P"],
                    "w_T": record["w_T"],
                }
            )
    return problems


def json_ready_text(payload: dict) -> str:
    from rs_constraint_lab.durable import canonical_json

    return canonical_json(payload)


def _smoke_records(records, slots) -> tuple[list, bool, bool]:
    """Two records: the erasure comes from the first, the face from the first record that has one."""
    del slots
    faced = next(row for row in records if any(face["status"] == "live" and not face.get("duplicate_of_earlier_face") for face in row["faces"]))
    erased = next(row for row in records if row["target_id"] != faced["target_id"])
    return [erased, faced], True, True


def _select(profile: str) -> tuple[list, bool, bool, str]:
    world = _world()
    records = world["records"]
    if profile == "census":
        return records, True, True, "primary"
    erased_and_faced, erasure, face = _smoke_records(records, world["slots"])
    return erased_and_faced, erasure, face, "smoke"


def _grid_item(expression: str, text: str, rho: str, alphabet: str) -> dict:
    return make_item_record(
        _digest(),
        HYPERGRAPH_N4_SEMANTIC_VERSION,
        ANALYSIS_VERSION,
        "multiplier",
        {"alphabet": alphabet, "expression": expression, "multiplier": text, "rho": rho},
    )


def _singleton_item(expression: str, rho: str, alphabet: str) -> dict:
    return make_item_record(
        _digest(),
        HYPERGRAPH_N4_SEMANTIC_VERSION,
        ANALYSIS_VERSION,
        "target_singleton",
        {"alphabet": alphabet, "expression": expression, "multiplier": None, "rho": rho},
    )


def _target_composition_item(problem: dict) -> dict:
    return make_item_record(
        _digest(),
        HYPERGRAPH_N4_SEMANTIC_VERSION,
        ANALYSIS_VERSION,
        "target_composition",
        {
            "alphabet": problem["alphabet"],
            "p_expression": problem["p_expression"],
            "rho": problem["rho"],
            "t_expression": problem["t_expression"],
        },
    )


def _control_composition_item(problem: dict, text: str) -> dict:
    return make_item_record(
        _digest(),
        HYPERGRAPH_N4_SEMANTIC_VERSION,
        ANALYSIS_VERSION,
        "control_composition",
        {
            "alphabet": problem["alphabet"],
            "c_expression": problem["control_expression"],
            "multiplier": text,
            "p_expression": problem["p_expression"],
            "relation": problem["relation"],
            "rho": problem["rho"],
            "t_expression": problem["t_expression"],
        },
    )


def _write_plan(root: Path, profile: str) -> dict:
    from rs_constraint_lab.supervisor import ensure_planned

    layout = Layout(root)
    layout.ensure()
    spec = _spec()
    world = _world()
    records, erasure, face, role = _select(profile)
    if profile == "smoke":
        # Erasure on the first chosen record only. One face on the faced record only.
        erased, faced = records
        problems = _problems_for([erased], world["slots"], role="primary", rho=str(PRIMARY_RHO), alphabet=spec["alphabet"], erasure=True, face=False)
        problems += _problems_for([faced], world["slots"], role="smoke", rho=str(PRIMARY_RHO), alphabet=spec["alphabet"], erasure=False, face=True)
    else:
        problems = _problems_for(records, world["slots"], role=role, rho=str(PRIMARY_RHO), alphabet=spec["alphabet"], erasure=erasure, face=face)
    atomic_write_json(layout.plan() / "problems.json", problems)
    atomic_write_json(layout.dependency_path(), {"calibrations": {}, "profile": profile})
    manifest = {
        "advance": "rs_constraint_lab.gen007_exec:advance",
        "analysis_version": ANALYSIS_VERSION,
        "calibration_version": CALIBRATION_VERSION,
        "counts": "rs_constraint_lab.gen007_exec:counts",
        "executor": "rs_constraint_lab.gen007_exec:execute_item",
        "experiment_id": spec["experiment_id"] if profile == "census" else "generation-007-smoke",
        "grid_sha256": GRID_SHA256,
        "heartbeat_seconds": 10,
        "merge": "rs_constraint_lab.gen007_exec:merge_items",
        "phase": "rs_constraint_lab.gen007_exec:phase",
        "profile": profile,
        "refinement_cap": 1 if profile == "smoke" else None,
        "semantic_version": HYPERGRAPH_N4_SEMANTIC_VERSION,
        "sensitivity_divergence": (
            "The frozen spec lists sensitivity alphabets W3 and W16. "
            "Prompt 007R section 59 schedules rho3 = 1/2 and rho3 = 2. "
            "Alphabet recalibration is not a scheduled generation-007 item."
        ),
        "spec_hash": _digest(),
        "watchdog_seconds": 120,
    }
    atomic_write_json(layout.manifest_path(), manifest)
    planned = 0
    seen = set()
    for problem in problems:
        for text in [multiplier_text(multiplier) for multiplier in POSITIVE_GRID] + ["0"]:
            record = _grid_item(problem["control_expression"], text, problem["rho"], problem["alphabet"])
            if record["item_id"] in seen:
                continue
            seen.add(record["item_id"])
            if ensure_planned(layout, record):
                planned += 1
        for builder in (_singleton_item(problem["t_expression"], problem["rho"], problem["alphabet"]), _target_composition_item(problem)):
            if builder["item_id"] in seen:
                continue
            seen.add(builder["item_id"])
            if ensure_planned(layout, builder):
                planned += 1
    summary = {
        "coverage": world["coverage"] if profile == "census" else {"smoke_problems": len(problems)},
        "experiment_id": manifest["experiment_id"],
        "planned_new_items": planned,
        "problems": len(problems),
        "profile": profile,
        "spec_hash": _digest(),
    }
    atomic_write_json(layout.plan() / "plan.json", summary)
    log_progress(layout, f"PLAN profile={profile} problems={len(problems)} new_items={planned}")
    return summary


def plan(root: Path) -> dict:
    return _write_plan(root, "census")


def plan_smoke(root: Path) -> dict:
    return _write_plan(root, "smoke")


def execute_item(record: dict, context: dict) -> dict:
    world = _world()
    slots = world["slots"]
    cache = context.setdefault("cache", {})
    kind = record["kind"]
    item_input = record["input"]
    rho = Fraction(item_input["rho"])
    alphabet = item_input["alphabet"]
    if kind in {"multiplier", "target_singleton"}:
        expression = item_input["expression"]
        rule = _rule(expression)
        point = parse_multiplier_text(item_input["multiplier"]) if kind == "multiplier" else Fraction(1)
        result = _num(solve_singleton(rule, point, alphabet, rho, slots, cache, context))
        if kind == "target_singleton":
            result["multiplier"] = None
        _write_point(context, record, result)
        return result
    if kind == "target_composition":
        result = _execute_target_composition(item_input, slots, cache, context)
        return _num(result)
    if kind == "control_composition":
        result = _execute_control_composition(item_input, slots, cache, context)
        return _num(result)
    raise RuntimeError(f"unknown item kind {kind}")


def _write_point(context: dict, record: dict, result: dict) -> None:
    layout = Layout(context["root"])
    atomic_write_json(layout.cache() / "points" / f"{record['item_id']}.json", _compact(result, record["item_id"], record["kind"]))


def _execute_target_composition(item_input: dict, slots, cache: dict, context: dict) -> dict:
    rho = Fraction(item_input["rho"])
    alphabet = item_input["alphabet"]
    target = _rule(item_input["t_expression"])
    companion = _rule(item_input["p_expression"])
    factors = factors_for(alphabet, None)

    class _View:
        pass

    view = _View()
    view.alphabet = alphabet
    view.rho = rho
    view.slots = slots
    view.cache = cache
    _note(context, ("baseline", _factors_key(BASELINE_FACTORS), str(rho)), cache)
    solved = _composed_target(target, companion, view, require_effect_floor(_spec()))
    _release_landings(cache)
    directions = {}
    for name, row in solved["directions"].items():
        directions[name] = {key: row[key] for key in ("Q0", "QT", "QP", "QTP", "delta_T", "delta_P", "delta_TP", "I", "G", "delta_S")}
    pack = _constrained_pack((target,), factors, rho, slots, cache)
    return {
        "directions": directions,
        "solver_residuals": {"epoch_defect": float(pack["defect"]), "stationary": float(pack["residual"])},
        "support_violations": solved["support_violations"],
    }


def _execute_control_composition(item_input: dict, slots, cache: dict, context: dict) -> dict:
    rho = Fraction(item_input["rho"])
    alphabet = item_input["alphabet"]
    control = _rule(item_input["c_expression"])
    companion = _rule(item_input["p_expression"])
    multiplier = parse_multiplier_text(item_input["multiplier"])
    factors = factors_for(alphabet, multiplier)
    floor = require_effect_floor(_spec())
    solved = _pack_directions(control, companion, factors, rho, slots, cache, floor)
    _release_landings(cache)
    layout = Layout(context["root"])
    target_item = _target_composition_item(
        {
            "alphabet": alphabet,
            "p_expression": item_input["p_expression"],
            "rho": item_input["rho"],
            "t_expression": item_input["t_expression"],
        }
    )
    target_payload = read_valid_item(layout, target_item["item_id"], _digest())
    if target_payload is None:
        raise RuntimeError("target composition is not on disk")
    singleton = _singleton_item(item_input["t_expression"], item_input["rho"], alphabet)
    singleton_payload = read_valid_item(layout, singleton["item_id"], _digest())
    if singleton_payload is None:
        raise RuntimeError("target singleton is not on disk")
    compared = {}
    for direction in DIRECTIONS:
        numbers = _composition_numbers(target_payload["result"]["directions"][direction], solved["directions"][direction], floor)
        target_delta = singleton_payload["result"]["directions"][direction]["delta"]
        numbers["singleton_mismatch"] = abs(solved["directions"][direction]["delta_C"] - target_delta)
        compared[direction] = numbers
    pack = _constrained_pack((control,), {CALIBRATION_WEIGHT: multiplier}, rho, slots, cache)
    return {
        "directions": compared,
        "multiplier": item_input["multiplier"],
        "solver_residuals": {"epoch_defect": float(pack["defect"]), "stationary": float(pack["residual"])},
        "support_violations": solved["support_violations"],
    }


def _load_problems(layout: Layout) -> list[dict]:
    path = layout.plan() / "problems.json"
    if not path.exists():
        return []
    return read_json(path)


def _calibration_path(layout: Layout, calibration_id: str) -> Path:
    return layout.calibration() / f"{calibration_id}.json"


def _read_calibration(layout: Layout, calibration_id: str) -> dict | None:
    path = _calibration_path(layout, calibration_id)
    if not path.exists():
        return None
    return read_json(path)


def _pending(state: dict) -> int:
    return sum(1 for slot in state.values() if slot.get("status") == "pending")


def advance(root: Path) -> int:
    from rs_constraint_lab.supervisor import ensure_planned

    layout = Layout(root)
    state = load_state(layout)
    if _pending(state):
        return 0
    problems = _load_problems(layout)
    if not problems:
        return 0
    manifest = read_json(layout.manifest_path())
    index = PointIndex(layout)
    index.load()
    added = 0
    if manifest.get("profile") != "smoke" and _role_terminal(layout, problems, "primary"):
        added += _ensure_robustness(layout, problems, ensure_planned)
        problems = _load_problems(layout)
    for problem in problems:
        if problem["role"] == "robustness":
            added += _ensure_fixed_control(layout, problem, ensure_planned)
        existing = _read_calibration(layout, problem["calibration_id"])
        if existing and existing.get("convergence_status") in TERMINAL:
            added += _ensure_matched_compositions(layout, problem, existing, ensure_planned)
            continue
        ready, blocked = _inputs_ready(layout, problem, index, state)
        if blocked:
            _save_calibration(layout, problem, status="blocked", requested=[], directions=None, joint=None, extra={"error": "a required point is quarantined"})
            continue
        if not ready:
            added += _ensure_grid(layout, problem, ensure_planned)
            continue
        added += _step(layout, problem, index, manifest, ensure_planned)
    _write_dependency(layout)
    return added


def _role_terminal(layout: Layout, problems: list[dict], role: str) -> bool:
    rows = [problem for problem in problems if problem["role"] == role]
    if not rows:
        return False
    for problem in rows:
        existing = _read_calibration(layout, problem["calibration_id"])
        if not existing or existing.get("convergence_status") not in TERMINAL:
            return False
    return True


def _inputs_ready(layout: Layout, problem: dict, index: PointIndex, state: dict) -> tuple[bool, bool]:
    if index.singleton(problem["t_expression"], problem["rho"], problem["alphabet"]) is None:
        item = _singleton_item(problem["t_expression"], problem["rho"], problem["alphabet"])
        if state.get(item["item_id"], {}).get("status") == "quarantined":
            return False, True
        return False, False
    for text in [multiplier_text(multiplier) for multiplier in POSITIVE_GRID] + ["0"]:
        if index.multiplier(problem["control_expression"], text, problem["rho"], problem["alphabet"]) is not None:
            continue
        item = _grid_item(problem["control_expression"], text, problem["rho"], problem["alphabet"])
        if state.get(item["item_id"], {}).get("status") == "quarantined":
            return False, True
        return False, False
    return True, False


def _ensure_grid(layout: Layout, problem: dict, ensure_planned) -> int:
    added = 0
    item = _singleton_item(problem["t_expression"], problem["rho"], problem["alphabet"])
    if ensure_planned(layout, item):
        added += 1
    composition = _target_composition_item(problem)
    if ensure_planned(layout, composition):
        added += 1
    for text in [multiplier_text(multiplier) for multiplier in POSITIVE_GRID] + ["0"]:
        record = _grid_item(problem["control_expression"], text, problem["rho"], problem["alphabet"])
        if ensure_planned(layout, record):
            added += 1
    return added


def _step(layout, problem, index: PointIndex, manifest: dict, ensure_planned) -> int:
    slots = _world()["slots"]
    book = DiskBook(slots, problem["alphabet"], problem["rho"], index)
    target_row = index.singleton(problem["t_expression"], problem["rho"], problem["alphabet"])
    target_effects = target_row["directions"]
    nominal = parse_multiplier_text(problem["nominal"])
    spec = _spec()
    tolerance = float(spec["match_tolerance"])
    scale_floor = float(spec["joint_scale_floor"])
    existing = _read_calibration(layout, problem["calibration_id"]) or {}
    rule = _rule(problem["control_expression"])
    stage = "all" if existing.get("convergence_status") == "directions_done" else "directions"
    try:
        result = calibrate_control(rule, target_effects, nominal, book, tolerance, scale_floor, stage=stage)
    except MissingPoint as missing:
        return _request_point(layout, problem, existing, missing, manifest, ensure_planned, index, target_effects)
    if stage == "directions":
        _save_calibration(layout, problem, status="directions_done", requested=[], directions=result["directions"], joint=None, extra={})
        log_progress(layout, f"CALIBRATION {problem['calibration_id'][:12]} directions-done roots={_root_total(result['directions'])}")
        return _step(layout, problem, index, manifest, ensure_planned)
    _save_calibration(layout, problem, status="converged", requested=[], directions=result["directions"], joint=result["joint"], extra={})
    log_progress(
        layout,
        f"CALIBRATION {problem['calibration_id'][:12]} converged class={result['joint']['match_class']} m={result['joint']['m_text']}",
    )
    return 0


def _root_total(directions: dict) -> int:
    return sum(int(row.get("root_count") or 0) for row in directions.values())


def _request_point(layout, problem, existing, missing: MissingPoint, manifest, ensure_planned, index, target_effects) -> int:
    requested = int(existing.get("refinement_requests") or 0)
    if manifest.get("profile") == "smoke" and requested >= int(manifest.get("refinement_cap") or 1):
        _cap_smoke(layout, problem, existing, index, target_effects)
        return 0
    text = multiplier_text(missing.multiplier)
    record = _grid_item(missing.expression, text, missing.rho, missing.alphabet)
    state = load_state(layout)
    if state.get(record["item_id"], {}).get("status") == "quarantined":
        _save_calibration(layout, problem, status="blocked", requested=[text], directions=existing.get("directions"), joint=existing.get("joint"), extra={"error": "refinement point quarantined"})
        return 0
    added = 1 if ensure_planned(layout, record) else 0
    # A joint search must stay in the joint stage. Replaying the one-direction
    # search would still be correct, and it would spend another scheduler wave.
    status = "directions_done" if existing.get("convergence_status") == "directions_done" else "needs_point"
    _save_calibration(
        layout,
        problem,
        status=status,
        requested=[text],
        directions=existing.get("directions"),
        joint=existing.get("joint"),
        extra={"refinement_requests": requested + (1 if added else 0)},
    )
    log_progress(layout, f"CALIBRATION {problem['calibration_id'][:12]} request m={text}")
    return added


def _cap_smoke(layout, problem, existing, index: PointIndex, target_effects) -> None:
    spec = _spec()
    scales = joint_scales(
        target_effects["path_to_matching"]["delta"],
        target_effects["matching_to_path"]["delta"],
        target_effects["path_to_matching"]["Q0"],
        target_effects["matching_to_path"]["Q0"],
        float(spec["joint_scale_floor"]),
    )
    best_text = None
    best_distance = None
    texts = [multiplier_text(multiplier) for multiplier in POSITIVE_GRID] + ["0"]
    for text in texts:
        point = index.multiplier(problem["control_expression"], text, problem["rho"], problem["alphabet"])
        if point is None:
            continue
        distance = joint_distance(
            point["directions"]["path_to_matching"]["delta"],
            point["directions"]["matching_to_path"]["delta"],
            target_effects["path_to_matching"]["delta"],
            target_effects["matching_to_path"]["delta"],
            scales,
        )
        if best_distance is None or distance < best_distance:
            best_distance = distance
            best_text = text
    _save_calibration(
        layout,
        problem,
        status="smoke_capped",
        requested=[],
        directions=existing.get("directions"),
        joint=None,
        extra={"smoke_best_m": best_text, "smoke_best_distance": best_distance},
    )
    log_progress(layout, f"CALIBRATION {problem['calibration_id'][:12]} smoke-capped m={best_text}")


def _save_calibration(layout, problem, *, status: str, requested, directions, joint, extra: dict) -> None:
    payload = {
        "alphabet": problem["alphabet"],
        "best_joint_point": None if not joint else {"boundary_status": joint.get("boundary_status"), "distance": joint.get("distance"), "m_text": joint.get("m_text"), "match_class": joint.get("match_class")},
        "calibration_id": problem["calibration_id"],
        "candidate_roots": _roots(directions),
        "control_expression": problem["control_expression"],
        "control_type": problem["control_type"],
        "convergence_status": status,
        "current_brackets": _brackets(directions),
        "directions": directions,
        "evaluated_points": _evaluated(layout, problem),
        "face": problem.get("face"),
        "joint": joint,
        "last_updated": utc_now(),
        "next_requested_points": list(requested or []),
        "nominal": problem["nominal"],
        "objective": "singleton_controlled_committor",
        "relation": problem["relation"],
        "rho": problem["rho"],
        "role": problem["role"],
        "search_domain": {"max": multiplier_text(M_MAX), "min": multiplier_text(M_MIN), "zero": "0"},
        "target_id": problem["target_id"],
    }
    payload.update(extra)
    atomic_write_json(_calibration_path(layout, problem["calibration_id"]), json_ready(payload))


def _roots(directions) -> list:
    if not directions:
        return []
    rows = []
    for direction, row in directions.items():
        for root in row.get("roots") or []:
            rows.append({"direction": direction, **root})
    return rows


def _brackets(directions) -> list:
    return [row for row in _roots(directions) if row.get("bracket")]


def _evaluated(layout, problem) -> list[str]:
    index = PointIndex(layout)
    # Caller may have a loaded index. A fresh scan here would repeat work.
    # The sidecar directory is the durable list.
    texts = []
    folder = layout.cache() / "points"
    if not folder.exists():
        return texts
    state = load_state(layout)
    items = work_index(layout)
    for item_id, record in items.items():
        if record["kind"] != "multiplier":
            continue
        if state.get(item_id, {}).get("status") != "complete":
            continue
        item_input = record["input"]
        if item_input.get("expression") != problem["control_expression"]:
            continue
        if item_input.get("rho") != problem["rho"] or item_input.get("alphabet") != problem["alphabet"]:
            continue
        texts.append(item_input["multiplier"])
    return sorted(set(texts))


def _ensure_matched_compositions(layout, problem, existing, ensure_planned) -> int:
    added = 0
    texts = []
    if existing.get("convergence_status") == "smoke_capped" and existing.get("smoke_best_m"):
        texts.append(existing["smoke_best_m"])
    else:
        for strategy in ("forward", "reverse", "joint"):
            text = _safe_multiplier(existing, strategy)
            if text:
                texts.append(text)
    seen = set()
    for text in texts:
        if text in seen:
            continue
        seen.add(text)
        record = _control_composition_item(problem, text)
        if ensure_planned(layout, record):
            added += 1
    return added


def _ensure_robustness(layout, problems, ensure_planned) -> int:
    if any(problem["role"] == "robustness" for problem in problems):
        return 0
    spec = _spec()
    added_problems = []
    slots = _world()["slots"]
    records = [
        record
        for record in _world()["records"]
        if (record["geometry"], record["polarity"], record["w_P"], record["w_T"]) in set(ROBUSTNESS_CELLS)
    ]
    for label in spec.get("rho3_sensitivity", ["1/2", "1", "2"]):
        if label in {"1", "1/1"}:
            continue
        rho = str(Fraction(label))
        added_problems.extend(
            _problems_for(records, slots, role="robustness", rho=rho, alphabet=spec["alphabet"], erasure=True, face=True)
        )
    if not added_problems:
        return 0
    atomic_write_json(layout.plan() / "problems.json", problems + added_problems)
    added = 0
    for problem in added_problems:
        added += _ensure_grid(layout, problem, ensure_planned)
    log_progress(layout, f"ROBUSTNESS problems={len(added_problems)} new_items={added}")
    log_event(layout, "robustness_scheduled", "rho robustness scheduled", counts={"problems": len(added_problems), "items": added})
    return added


def _primary_held_multiplier(layout: Layout, problem: dict) -> str | None:
    """The primary joint multiplier, held fixed at a robustness rho."""
    if problem["role"] != "robustness":
        return None
    for row in _load_problems(layout):
        if row["role"] != "primary" or row["target_id"] != problem["target_id"]:
            continue
        if row["relation"] != problem["relation"] or row["alphabet"] != problem["alphabet"]:
            continue
        if row["rho"] != str(PRIMARY_RHO):
            continue
        existing = _read_calibration(layout, row["calibration_id"]) or {}
        joint = existing.get("joint") or {}
        if joint.get("matched") and joint.get("m_text"):
            return joint["m_text"]
    return None


def _ensure_fixed_control(layout: Layout, problem: dict, ensure_planned) -> int:
    text = _primary_held_multiplier(layout, problem)
    if not text:
        return 0
    state = load_state(layout)
    singleton = _singleton_item(problem["t_expression"], problem["rho"], problem["alphabet"])
    composition = _target_composition_item(problem)
    if state.get(singleton["item_id"], {}).get("status") != "complete":
        return 0
    if state.get(composition["item_id"], {}).get("status") != "complete":
        return 0
    added = 0
    point = _grid_item(problem["control_expression"], text, problem["rho"], problem["alphabet"])
    if ensure_planned(layout, point):
        added += 1
    record = _control_composition_item(problem, text)
    if ensure_planned(layout, record):
        added += 1
    return added


def _composition_probe(layout: Layout, problem: dict, text: str | None) -> dict | None:
    if not text:
        return None
    payload = read_valid_item(layout, _control_composition_item(problem, text)["item_id"], _digest())
    if payload is None:
        return None
    return {"directions": payload["result"]["directions"], "m_text": text}


def _safe_multiplier(existing: dict, strategy: str) -> str | None:
    if strategy == "joint":
        joint = existing.get("joint") or {}
        return joint.get("m_text") if joint.get("matched") else None
    if not existing.get("directions"):
        return None
    return _strategy_multiplier(existing, strategy)


def _write_dependency(layout: Layout) -> None:
    rows = {}
    folder = layout.calibration()
    if folder.exists():
        for path in folder.glob("*.json"):
            payload = read_json(path)
            joint = payload.get("joint") or {}
            rows[payload.get("calibration_id") or path.stem] = {
                "directions": bool(payload.get("directions")),
                "status": payload.get("convergence_status"),
                "unresolved": payload.get("convergence_status") == "blocked" or joint.get("match_class") == "unresolved",
            }
    atomic_write_json(layout.dependency_path(), {"calibrations": rows, "updated_at": utc_now()})


def _dependency(layout: Layout) -> dict:
    path = layout.dependency_path()
    if not path.exists():
        return {"calibrations": {}}
    return read_json(path)


def phase(root: Path) -> str:
    layout = Layout(root)
    if not (layout.plan() / "problems.json").exists():
        return "03_SCIENCE_PLAN"
    manifest = read_json(layout.manifest_path())
    problems = _load_problems(layout)
    state = load_state(layout)
    known = _dependency(layout).get("calibrations") or {}
    primary = [problem["calibration_id"] for problem in problems if problem["role"] == "primary"]

    def status(calibration_id: str) -> str | None:
        row = known.get(calibration_id) or {}
        return row.get("status")

    if not primary or any(status(calibration_id) not in TERMINAL for calibration_id in primary):
        if not any(status(calibration_id) for calibration_id in primary):
            return "04_INITIAL_GRID"
        if any((known.get(calibration_id) or {}).get("directions") for calibration_id in primary):
            return "06_JOINT_MATCH"
        return "05_ROOT_REFINEMENT"
    if any(slot.get("status") == "pending" and slot.get("kind") in {"target_composition", "control_composition"} for slot in state.values()):
        return "07_COMPOSITION"
    if manifest.get("profile") != "smoke":
        robustness = [problem["calibration_id"] for problem in problems if problem["role"] == "robustness"]
        if not robustness or any(status(calibration_id) not in TERMINAL for calibration_id in robustness):
            return "09_ROBUSTNESS"
        if any(slot.get("status") == "pending" for slot in state.values()):
            return "09_ROBUSTNESS"
    if any(slot.get("status") == "pending" for slot in state.values()):
        return "08_STATE_VALIDATION"
    if not (layout.merge() / "summary.json").exists():
        return "10_MERGE"
    return "11_REPORT"


def counts(root: Path) -> dict:
    layout = Layout(root)
    problems = _load_problems(layout)
    known = _dependency(layout).get("calibrations") or {}
    complete = 0
    unresolved = 0
    for problem in problems:
        row = known.get(problem["calibration_id"]) or {}
        if row.get("status") in TERMINAL:
            complete += 1
        if row.get("unresolved"):
            unresolved += 1
    hits = 0
    misses = 0
    folder = layout.batches()
    if folder.exists():
        for path in folder.glob("*/*/cache.json"):
            payload = read_json(path)
            hits += int(payload.get("cache_hits") or 0)
            misses += int(payload.get("cache_misses") or 0)
    return {
        "cache_hits": hits,
        "cache_misses": misses,
        "calibrations_complete": complete,
        "calibrations_total": len(problems),
        "calibrations_unresolved": unresolved,
    }


def merge_items(root: Path) -> dict:
    layout = Layout(root)
    problems = _load_problems(layout)
    spec = _spec()
    floor = require_effect_floor(spec)
    grouped: dict[str, list] = {}
    for problem in problems:
        if problem["role"] != "primary":
            continue
        grouped.setdefault(problem["target_id"], []).append(problem)
    rows = []
    for target_id, group in sorted(grouped.items()):
        dest = layout.merge() / "rows" / f"{target_id}.json"
        stamp = _group_stamp(layout, group)
        if dest.exists():
            stored = read_json(dest)
            if stored.get("stamp") == stamp:
                rows.append(stored["row"])
                continue
        row = _assemble_row(layout, group, floor)
        atomic_write_json(dest, {"row": row, "stamp": stamp})
        rows.append(row)
    questions = summarise_calibrated(rows, floor) if rows else {}
    operational = _operational(layout)
    summary = {
        "analysis_version": ANALYSIS_VERSION,
        "calibration_version": CALIBRATION_VERSION,
        "experiment_id": read_json(layout.manifest_path()).get("experiment_id"),
        "items": _completed_item_index(layout),
        "operational": operational,
        "questions": questions,
        "rows": rows,
        "schema": "rs-constraint-lab.generation-007-merge/v1",
        "spec_hash": _digest(),
    }
    atomic_write_json(layout.merge() / "summary.json", json_ready(summary))
    log_progress(layout, f"MERGE rows={len(rows)}")
    return summary


def _completed_item_index(layout: Layout) -> list[dict]:
    state = load_state(layout)
    rows = []
    for item_id, slot in sorted(state.items()):
        if slot.get("status") != "complete":
            continue
        payload = read_valid_item(layout, item_id, _digest())
        if payload is None:
            continue
        rows.append({"item_id": item_id, "result_hash": payload["result_hash"]})
    return rows


def _group_stamp(layout: Layout, group: list[dict]) -> str:
    parts = []
    target_id = group[0]["target_id"]
    related = [problem for problem in _load_problems(layout) if problem["target_id"] == target_id]
    for problem in related:
        existing = _read_calibration(layout, problem["calibration_id"]) or {}
        texts = []
        for strategy in ("forward", "reverse", "joint"):
            text = _safe_multiplier(existing, strategy)
            if text:
                texts.append(text)
        held = _primary_held_multiplier(layout, problem)
        if held:
            texts.append(held)
        probes = []
        for text in sorted(set(texts)):
            payload = read_valid_item(layout, _control_composition_item(problem, text)["item_id"], _digest())
            probes.append({"hash": None if payload is None else payload["result_hash"], "m": text})
        parts.append(
            {
                "calibration": existing.get("last_updated"),
                "id": problem["calibration_id"],
                "probes": probes,
                "status": existing.get("convergence_status"),
            }
        )
    from rs_constraint_lab.durable import canonical_json

    return sha256_bytes(canonical_json(parts).encode("utf-8"))


def _assemble_row(layout: Layout, group: list[dict], floor: float) -> dict:
    problem = group[0]
    singleton = read_valid_item(layout, _singleton_item(problem["t_expression"], problem["rho"], problem["alphabet"])["item_id"], _digest())
    composed = read_valid_item(layout, _target_composition_item(problem)["item_id"], _digest())
    controls = []
    for control in group:
        existing = _read_calibration(layout, control["calibration_id"]) or {}
        if not existing.get("directions"):
            existing = dict(existing)
            existing["directions"] = {
                direction: {
                    "absolute_mismatch": None,
                    "boundary_status": None,
                    "m_text": None,
                    "match_class": "unresolved",
                    "matched": False,
                    "monotonicity": [],
                    "only_exact_solution_is_zero": False,
                    "root_count": 0,
                }
                for direction in DIRECTIONS
            }
        if not existing.get("joint"):
            existing = dict(existing)
            existing["joint"] = {
                "boundary_status": None,
                "distance": existing.get("smoke_best_distance"),
                "m_text": existing.get("smoke_best_m"),
                "match_class": "unresolved",
                "matched": False,
            }
        strategies = {}
        for strategy in ("forward", "reverse", "joint"):
            text = None
            if existing.get("convergence_status") == "smoke_capped" and strategy == "joint":
                text = existing.get("smoke_best_m")
            elif existing.get("directions") or existing.get("joint"):
                text = _safe_multiplier(existing, strategy)
            entry = {"m_text": text, "matched": text is not None and existing.get("convergence_status") != "smoke_capped", "used_as_matched": False}
            if text is None:
                strategies[strategy] = entry
                continue
            composition = read_valid_item(layout, _control_composition_item(control, text)["item_id"], _digest())
            if composition is None:
                strategies[strategy] = entry
                continue
            entry["composition"] = composition["result"]["directions"]
            entry["support_violations"] = composition["result"].get("support_violations")
            entry["state_shape"] = _state_shape(layout, control, text, singleton, entry["composition"], floor)
            required = _required_directions(strategy)
            entry["used_as_matched"] = all(entry["composition"][direction]["singleton_mismatch"] <= float(_spec()["match_tolerance"]) for direction in required)
            if existing.get("convergence_status") == "smoke_capped":
                entry["used_as_matched"] = False
                entry["matched"] = False
            strategies[strategy] = entry
        controls.append(
            {
                "calibration": {"directions": existing.get("directions"), "joint": existing.get("joint")},
                "control_type": control["control_type"],
                "face": control.get("face"),
                "relation": control["relation"],
                "strategies": strategies,
            }
        )
    target_singleton = {}
    target_composition = {}
    if singleton is not None:
        for direction in DIRECTIONS:
            row = singleton["result"]["directions"][direction]
            target_singleton[direction] = {key: row[key] for key in ("delta", "Q", "Q0", "spread")}
    if composed is not None:
        target_composition = composed["result"]["directions"]
    return json_ready(
        {
            "analysis_version": ANALYSIS_VERSION,
            "calibration_version": CALIBRATION_VERSION,
            "cell": problem["cell"],
            "controls": controls,
            "geometry": problem["geometry"],
            "nominal_multiplier": problem["nominal"],
            "polarity": problem["polarity"],
            "robustness": _robustness_row(layout, problem, floor),
            "target_composition": target_composition,
            "target_id": problem["target_id"],
            "target_singleton": target_singleton,
            "w_P": problem["w_P"],
            "w_T": problem["w_T"],
        }
    )


def _required_directions(strategy: str) -> tuple[str, ...]:
    if strategy == "forward":
        return ("path_to_matching",)
    if strategy == "reverse":
        return ("matching_to_path",)
    return DIRECTIONS


def _state_shape(layout, problem, text, singleton, composition, floor: float) -> dict | None:
    if singleton is None:
        return None
    point = _grid_item(problem["control_expression"], text, problem["rho"], problem["alphabet"])
    payload = read_valid_item(layout, point["item_id"], _digest())
    if payload is None:
        return None
    target_effects = singleton["result"]["directions"]
    control_effects = payload["result"]["directions"]
    mismatches = {direction: composition[direction]["singleton_mismatch"] for direction in DIRECTIONS}
    n_pairs = int(payload["result"]["n_pairs"])
    restored_target = _restore_vectors(target_effects)
    restored_control = _restore_vectors(control_effects)
    return _shape_for(restored_target, restored_control, mismatches, floor, n_pairs, float(_spec()["match_tolerance"]))


def _restore_vectors(directions: dict) -> dict:
    restored = {}
    for name, row in directions.items():
        restored[name] = dict(row)
        for key in ("q", "q0", "mu"):
            if key in row and row[key] is not None:
                restored[name][key] = np.asarray([math.nan if value is None else float(value) for value in row[key]], dtype=np.float64)
    return restored


def _robustness_row(layout, problem, floor: float) -> dict | None:
    del floor
    problems = [row for row in _load_problems(layout) if row["role"] == "robustness" and row["target_id"] == problem["target_id"]]
    if not problems:
        return None
    out = {"alphabet": {}, "rho": {}}
    for row in problems:
        existing = _read_calibration(layout, row["calibration_id"]) or {}
        joint = existing.get("joint") or {}
        held = _primary_held_multiplier(layout, row)
        recalibrated_text = joint.get("m_text") if joint.get("matched") else None
        fixed = _composition_probe(layout, row, held)
        label = row["rho"]
        bucket = out["rho"].setdefault(label, {"controls": []})
        if fixed is not None:
            fixed_status = "matched_probe"
        elif held:
            fixed_status = "missing"
        else:
            fixed_status = "not_matched"
        bucket["controls"].append(
            {
                "fixed_control": fixed,
                "fixed_m": held,
                "fixed_status": fixed_status,
                "recalibrated_class": joint.get("match_class"),
                "recalibrated_control": _composition_probe(layout, row, recalibrated_text),
                "recalibrated_distance": joint.get("distance"),
                "recalibrated_m": joint.get("m_text"),
                "recalibrated_matched": bool(joint.get("matched")),
                "relation": row["relation"],
            }
        )
    return out


def _operational(layout: Layout) -> dict:
    receipts = []
    folder = layout.receipts()
    if folder.exists():
        receipts = [read_json(path) for path in sorted(folder.glob("*.json"))]
    walls = sorted(float(row.get("wall_seconds") or 0.0) for row in receipts)
    events = layout.events_path()
    splits = timeouts = quarantines = resumes = 0
    if events.exists():
        for line in events.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            payload = read_json_line(line)
            kind = payload.get("event_type")
            if kind == "batch_split":
                splits += 1
            elif kind == "batch_timeout":
                timeouts += 1
            elif kind == "quarantine":
                quarantines += 1
            elif kind == "batch_recovered":
                resumes += 1
            elif kind == "stale_lock":
                resumes += 1
    return {
        "completed_batches": len(receipts),
        "maximum_batch_wall_time": None if not walls else walls[-1],
        "median_batch_wall_time": None if not walls else walls[len(walls) // 2],
        "p90_batch_wall_time": None if not walls else _percentile(walls, 0.90),
        "quarantines": quarantines,
        "resume_events": resumes,
        "splits": splits,
        "timeouts": timeouts,
    }


def read_json_line(line: str) -> dict:
    import json

    return json.loads(line)


def benchmark(root: Path) -> dict:
    """Time representative atomic items and freeze the batch policy. No generation items are written."""
    layout = Layout(root)
    layout.ensure()
    world = _world()
    spec = _spec()
    slots = world["slots"]
    grammar_slots = slots
    samples: dict[str, list[float]] = {"multiplier": [], "target_singleton": [], "target_composition": [], "control_composition": []}
    record = world["records"][0]
    grammar = _grammar(WEIGHT_ORDER, 4)
    target, companion, controls = _live_controls(record, grammar, grammar_slots)
    erasure = next(control for control in controls if control["control_type"] == "erasure")
    faced = next((control for control in controls if control["control_type"] == "pair_face"), None)
    if faced is None:
        for candidate in world["records"][1:]:
            _target, _companion, more = _live_controls(candidate, grammar, grammar_slots)
            faced = next((control for control in more if control["control_type"] == "pair_face"), None)
            if faced is not None:
                break
    alphabet = spec["alphabet"]
    rho = PRIMARY_RHO
    jobs = [("multiplier", erasure["rule"], text) for text in ("1.000000000000e+0", "0", multiplier_text(M_MIN), multiplier_text(M_MAX))]
    if faced is not None:
        jobs.append(("multiplier", faced["rule"], "1.000000000000e+0"))
    for _repeat in range(3):
        for kind, rule, text in jobs:
            cache: dict = {}
            started = time.perf_counter()
            solve_singleton(rule, parse_multiplier_text(text), alphabet, rho, slots, cache, None)
            samples["multiplier"].append(time.perf_counter() - started)
        cache = {}
        started = time.perf_counter()
        solve_singleton(target, Fraction(1), alphabet, rho, slots, cache, None)
        samples["target_singleton"].append(time.perf_counter() - started)
        cache = {}
        started = time.perf_counter()
        _execute_target_composition(
            {"alphabet": alphabet, "p_expression": companion.expression(slots), "rho": str(rho), "t_expression": target.expression(slots)},
            slots,
            cache,
            {"cache": cache, "root": root},
        )
        samples["target_composition"].append(time.perf_counter() - started)
        cache = {}
        context = {"cache": cache, "root": root}
        # The composition reader expects the target files. Time the kernel portion by calling the pack directly.
        started = time.perf_counter()
        _pack_directions(erasure["rule"], companion, factors_for(alphabet, Fraction(1)), rho, slots, cache, require_effect_floor(spec))
        _release_landings(cache)
        samples["control_composition"].append(time.perf_counter() - started)
        del context
    kinds = {}
    for kind, values in samples.items():
        ordered = sorted(values)
        kinds[kind] = {
            "items": choose_batch_count(values),
            "max": ordered[-1],
            "p50": _percentile(ordered, 0.50),
            "p90": _percentile(ordered, 0.90),
            "samples": values,
        }
    kinds["default"] = {"items": 1}
    policy = {
        "calculation": "count = floor(45 / p90), then reduced while count * p90 > 60 or count * max > 100. count = 1 when p90 > 60.",
        "hard_timeout_seconds": 120,
        "kinds": kinds,
        "schema": "rs-constraint-lab.batch-policy/v1",
        "target_seconds": 45,
        "watchdog_seconds": 120,
    }
    atomic_write_json(layout.policy_path(), policy)
    atomic_write_json(layout.plan() / "benchmark.json", policy)
    return policy
