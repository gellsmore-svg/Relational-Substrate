"""Durable executor for the Generation 007B two-level control.

Kernel evaluations happen only inside ``execute_item``. ``advance`` reads
stored points and requests the next stencil.
"""

from __future__ import annotations

import time
from fractions import Fraction
from pathlib import Path

import numpy as np

from rs_constraint_lab.constraints import parse_expression
from rs_constraint_lab.durable import atomic_write_json, read_json
from rs_constraint_lab.spec import load_spec, spec_hash
from rs_constraint_lab.v05 import PRIMARY_RHO, _num
from rs_constraint_lab.v07 import (
    DIRECTIONS,
    parse_multiplier_text,
    state_shape_report,
)
from rs_constraint_lab.v07b import (
    ADAPTIVE_CAP,
    ANALYSIS_VERSION,
    CALIBRATION_VERSION,
    COARSE_PAIRS,
    COARSE_SHA256,
    COMPLEXITY_CONTROL,
    COMPLEXITY_TARGET,
    EFFECT_FLOOR,
    MATCH_TOLERANCE,
    ROBUSTNESS_RHOS,
    SEMANTIC_VERSION,
    TERMINAL_STATUSES,
    _point_key,
    build_problems,
    coarse_complete,
    complexity_rows,
    composition_ids,
    fresh_calibration,
    is_preflight,
    is_robustness,
    scales_for,
    solve_control_composition,
    solve_pair_point,
    solve_target_composition,
    step_problem,
    work_count,
)
from rs_constraint_lab.workstore import (
    Layout,
    load_state,
    log_event,
    log_progress,
    make_item_record,
    read_valid_item,
    work_index,
)

SPEC_PATH = Path(__file__).resolve().parents[2] / "experiments" / "specs" / "generation-007b.json"
_WORLD: dict = {}


class MissingPoint(Exception):
    def __init__(self, structure_id: str, m_off: str, m_on: str, rho: str, alphabet: str):
        self.structure_id = structure_id
        self.m_off = m_off
        self.m_on = m_on
        self.rho = rho
        self.alphabet = alphabet
        super().__init__(f"missing {structure_id} m_off={m_off} m_on={m_on} rho={rho} alphabet={alphabet}")


def _spec() -> dict:
    if "spec" not in _WORLD:
        data = load_spec(SPEC_PATH)
        if data["analysis_version"] != ANALYSIS_VERSION:
            raise RuntimeError("generation 007B spec version does not match the executor")
        _WORLD["spec"] = data
        _WORLD["spec_hash"] = spec_hash(data)
    return _WORLD["spec"]


def _digest() -> str:
    _spec()
    return _WORLD["spec_hash"]


def _problems() -> list[dict]:
    if "problems" not in _WORLD:
        _WORLD["problems"] = build_problems(_spec())
    return _WORLD["problems"]


def _rule(expression: str):
    return parse_expression(expression, 4, order=3)


def _slots():
    from rs_constraint_lab.v05 import _grammar
    from rs_constraint_lab.v06 import WEIGHT_ORDER

    return _grammar(WEIGHT_ORDER, 4).slot_list()


def _pair_record(problem: dict, m_off: str, m_on: str, rho: str | None = None) -> dict:
    item_input = {
        "alphabet": problem["alphabet"],
        "m_off": m_off,
        "m_on": m_on,
        "off_expression": problem["off_expression"],
        "on_expression": problem["on_expression"],
        "rho": rho or problem["rho"],
        "structure_id": problem["structure_id"],
    }
    return make_item_record(_digest(), SEMANTIC_VERSION, ANALYSIS_VERSION, "pair_point", item_input)


def _target_record(problem: dict, rho: str | None = None) -> dict:
    item_input = {
        "alphabet": problem["alphabet"],
        "expression": problem["t_expression"],
        "rho": rho or problem["rho"],
    }
    return make_item_record(_digest(), SEMANTIC_VERSION, ANALYSIS_VERSION, "target_singleton", item_input)


def _target_composition_record(problem: dict, rho: str | None = None) -> dict:
    item_input = {
        "alphabet": problem["alphabet"],
        "p_expression": problem["p_expression"],
        "rho": rho or problem["rho"],
        "t_expression": problem["t_expression"],
    }
    return make_item_record(_digest(), SEMANTIC_VERSION, ANALYSIS_VERSION, "target_composition", item_input)


def _control_composition_record(problem: dict, solution: dict, rho: str | None = None) -> dict:
    item_input = {
        "alphabet": problem["alphabet"],
        "basin_id": solution["basin_id"],
        "m_off": solution["m_off"],
        "m_on": solution["m_on"],
        "off_expression": problem["off_expression"],
        "on_expression": problem["on_expression"],
        "p_expression": problem["p_expression"],
        "rho": rho or problem["rho"],
    }
    return make_item_record(_digest(), SEMANTIC_VERSION, ANALYSIS_VERSION, "control_composition", item_input)


def _select_profile(profile: str) -> list[dict]:
    problems = _problems()
    if profile == "census":
        return problems
    if profile == "preflight":
        return [row for row in problems if is_preflight(row)]
    if profile == "smoke":
        return problems[:1]
    raise ValueError(f"unknown profile {profile}")


def _write_plan(root: Path, profile: str) -> dict:
    from rs_constraint_lab.supervisor import ensure_planned

    layout = Layout(root)
    layout.ensure()
    chosen = _select_profile(profile)
    frozen = work_count(_problems())
    if profile == "census":
        counted = work_count(chosen)
        if counted["logical_calibration_problems"] != 42 or counted["unique_two_level_structures"] != 4:
            raise RuntimeError(f"work count drifted from the frozen census: {counted}")
        if counted["initial_atomic_items"] != 344:
            raise RuntimeError(f"initial item count drifted: {counted}")
    atomic_write_json(layout.plan() / "problems.json", chosen)
    atomic_write_json(layout.plan() / "work-count.json", frozen)
    atomic_write_json(
        layout.dependency_path(),
        {"profile": profile, "robustness_started": False},
    )
    manifest = {
        "advance": "rs_constraint_lab.gen007b_exec:advance",
        "analysis_version": ANALYSIS_VERSION,
        "calibration_version": CALIBRATION_VERSION,
        "coarse_sha256": COARSE_SHA256,
        "counts": "rs_constraint_lab.gen007b_exec:counts",
        "executor": "rs_constraint_lab.gen007b_exec:execute_item",
        "experiment_id": _spec()["experiment_id"] if profile == "census" else f"generation-007b-{profile}",
        "heartbeat_seconds": 10,
        "merge": "rs_constraint_lab.gen007b_exec:merge_items",
        "phase": "rs_constraint_lab.gen007b_exec:phase",
        "profile": profile,
        "semantic_version": SEMANTIC_VERSION,
        "spec_hash": _digest(),
        "watchdog_seconds": 120,
    }
    atomic_write_json(layout.manifest_path(), manifest)
    seen = set()
    planned = 0
    structures = {}
    for problem in chosen:
        structures.setdefault(problem["structure_id"], problem)
        record = _target_record(problem)
        if record["item_id"] not in seen:
            seen.add(record["item_id"])
            if ensure_planned(layout, record):
                planned += 1
    for problem in structures.values():
        for m_off, m_on in COARSE_PAIRS:
            record = _pair_record(problem, m_off, m_on)
            if record["item_id"] in seen:
                continue
            seen.add(record["item_id"])
            if ensure_planned(layout, record):
                planned += 1
    summary = {
        "adaptive_cap_per_problem": ADAPTIVE_CAP,
        "coarse_points_per_structure": len(COARSE_PAIRS),
        "experiment_id": manifest["experiment_id"],
        "initial_atomic_items": planned,
        "logical_calibration_problems": len(chosen),
        "planned_new_items": planned,
        "profile": profile,
        "spec_hash": _digest(),
        "unique_structures_in_profile": len(structures),
        "work_count": frozen,
    }
    atomic_write_json(layout.plan() / "plan.json", summary)
    log_progress(layout, f"PLAN profile={profile} problems={len(chosen)} new_items={planned}")
    return summary


def plan(root: Path) -> dict:
    return _write_plan(root, "census")


def plan_preflight(root: Path) -> dict:
    return _write_plan(root, "preflight")


def plan_smoke(root: Path) -> dict:
    return _write_plan(root, "smoke")


def _compact_pair(result: dict) -> dict:
    forward = result["directions"]["path_to_matching"]
    reverse = result["directions"]["matching_to_path"]
    return {
        "delta_forward": forward["delta"],
        "delta_reverse": reverse["delta"],
        "q0_forward": forward["Q0"],
        "q0_reverse": reverse["Q0"],
        "spread_forward": forward["spread"],
        "spread_reverse": reverse["spread"],
    }


def _compact_target(result: dict) -> dict:
    forward = result["directions"]["path_to_matching"]
    reverse = result["directions"]["matching_to_path"]
    return {
        "delta_forward": forward["delta"],
        "delta_reverse": reverse["delta"],
        "q0_forward": forward["Q0"],
        "q0_reverse": reverse["Q0"],
        "spread_forward": forward["spread"],
        "spread_reverse": reverse["spread"],
    }


def execute_item(record: dict, context: dict) -> dict:
    slots = _slots()
    cache = context.setdefault("cache", {})
    item_input = record["input"]
    rho = Fraction(item_input["rho"])
    alphabet = item_input["alphabet"]
    kind = record["kind"]
    if kind == "pair_point":
        result = solve_pair_point(
            _rule(item_input["off_expression"]),
            _rule(item_input["on_expression"]),
            parse_multiplier_text(item_input["m_off"]),
            parse_multiplier_text(item_input["m_on"]),
            alphabet,
            rho,
            slots,
            cache,
        )
    elif kind == "target_singleton":
        from rs_constraint_lab.gen007_exec import solve_singleton

        result = _num(solve_singleton(_rule(item_input["expression"]), Fraction(1), alphabet, rho, slots, cache, context))
    elif kind == "target_composition":
        result = solve_target_composition(
            _rule(item_input["t_expression"]),
            _rule(item_input["p_expression"]),
            alphabet,
            rho,
            slots,
            cache,
            EFFECT_FLOOR,
        )
    elif kind == "control_composition":
        result = solve_control_composition(
            _rule(item_input["off_expression"]),
            _rule(item_input["on_expression"]),
            _rule(item_input["p_expression"]),
            parse_multiplier_text(item_input["m_off"]),
            parse_multiplier_text(item_input["m_on"]),
            alphabet,
            rho,
            slots,
            cache,
        )
    else:
        raise RuntimeError(f"unknown generation 007B item kind {kind}")
    if kind in {"pair_point", "target_singleton"}:
        folder = Layout(context["root"]).cache() / "points"
        folder.mkdir(parents=True, exist_ok=True)
        compact = _compact_pair(result) if kind == "pair_point" else _compact_target(result)
        atomic_write_json(folder / f"{record['item_id']}.json", compact)
    return result


class PointIndex:
    def __init__(self, layout: Layout):
        self.layout = layout
        self.pairs: dict[tuple, dict] = {}
        self.targets: dict[tuple, dict] = {}

    def load(self) -> None:
        state = load_state(self.layout)
        index = work_index(self.layout)
        folder = self.layout.cache() / "points"
        folder.mkdir(parents=True, exist_ok=True)
        for record in index.values():
            if state.get(record["item_id"], {}).get("status") != "complete":
                continue
            if record["kind"] not in {"pair_point", "target_singleton"}:
                continue
            path = folder / f"{record['item_id']}.json"
            if not path.exists():
                payload = read_valid_item(self.layout, record["item_id"], _digest())
                if payload is None:
                    continue
                compact = _compact_pair(payload["result"]) if record["kind"] == "pair_point" else _compact_target(payload["result"])
                atomic_write_json(path, compact)
            row = read_json(path)
            item_input = record["input"]
            if record["kind"] == "pair_point":
                key = (item_input["structure_id"], item_input["m_off"], item_input["m_on"], item_input["rho"], item_input["alphabet"])
                self.pairs[key] = row
            else:
                key = (item_input["expression"], item_input["rho"], item_input["alphabet"])
                self.targets[key] = row

    def pair_map(self, structure_id: str, rho: str, alphabet: str) -> dict:
        found = {}
        for (structure, m_off, m_on, point_rho, point_alphabet), row in self.pairs.items():
            if structure == structure_id and point_rho == rho and point_alphabet == alphabet:
                found[_point_key(m_off, m_on)] = row
        return found

    def target(self, expression: str, rho: str, alphabet: str) -> dict | None:
        return self.targets.get((expression, rho, alphabet))

    def require_pair(self, structure_id: str, m_off: str, m_on: str, rho: str, alphabet: str) -> dict:
        row = self.pairs.get((structure_id, m_off, m_on, rho, alphabet))
        if row is None:
            raise MissingPoint(structure_id, m_off, m_on, rho, alphabet)
        return row


def _calibration_path(layout: Layout, calibration_id: str) -> Path:
    return layout.calibration() / f"{calibration_id}.json"


def _read_calibration(layout: Layout, calibration_id: str) -> dict | None:
    path = _calibration_path(layout, calibration_id)
    if not path.exists():
        return None
    return read_json(path)


def _problems_on_disk(layout: Layout) -> list[dict]:
    return read_json(layout.plan() / "problems.json")


def _robustness_problems(problems: list[dict]) -> list[dict]:
    from rs_constraint_lab.durable import canonical_json, sha256_bytes

    rows = []
    for problem in problems:
        if not is_robustness(problem):
            continue
        for rho in ROBUSTNESS_RHOS:
            copied = dict(problem)
            copied["rho"] = rho
            copied["role"] = "recalibration"
            copied["primary_calibration_id"] = problem["calibration_id"]
            identity = {
                "alphabet": copied["alphabet"],
                "analysis_version": ANALYSIS_VERSION,
                "off_expression": copied["off_expression"],
                "on_expression": copied["on_expression"],
                "rho": rho,
                "role": "recalibration",
                "target_id": copied["target_id"],
            }
            copied["calibration_id"] = sha256_bytes(canonical_json(identity).encode("utf-8"))
            rows.append(copied)
    return rows


def advance(root: Path) -> int:
    from rs_constraint_lab.supervisor import ensure_planned

    layout = Layout(root)
    manifest = read_json(layout.manifest_path())
    profile = manifest["profile"]
    problems = _problems_on_disk(layout)
    index = PointIndex(layout)
    index.load()
    added = 0
    for problem in problems:
        existing = _read_calibration(layout, problem["calibration_id"]) or fresh_calibration(problem)
        if existing.get("status") in TERMINAL_STATUSES:
            continue
        target = index.target(problem["t_expression"], problem["rho"], problem["alphabet"])
        points = index.pair_map(problem["structure_id"], problem["rho"], problem["alphabet"])
        if target is None or not coarse_complete(points):
            continue
        updated, requests = step_problem(existing, points, target, scales_for(target), MATCH_TOLERANCE)
        atomic_write_json(_calibration_path(layout, problem["calibration_id"]), updated)
        for m_off, m_on in requests:
            record = _pair_record(problem, m_off, m_on)
            if ensure_planned(layout, record):
                added += 1
    if profile != "census":
        return added
    if not _primary_terminal(layout, problems):
        return added
    represented_ids = set()
    for problem in problems:
        state = _read_calibration(layout, problem["calibration_id"])
        if state is None or state.get("status") != "represented" or not state.get("solutions"):
            continue
        represented_ids.add(problem["calibration_id"])
        for basin_id in composition_ids(state):
            solution = next(row for row in state["solutions"] if row["basin_id"] == basin_id)
            for builder in (
                _target_composition_record(problem),
                _control_composition_record(problem, solution),
            ):
                if ensure_planned(layout, builder):
                    added += 1
        if not is_robustness(problem) or state.get("selected_solution") is None:
            continue
        for rho in ROBUSTNESS_RHOS:
            selected = state["selected_solution"]
            for builder in (
                _pair_record(problem, selected["m_off"], selected["m_on"], rho),
                _target_record(problem, rho),
                _target_composition_record(problem, rho),
                _control_composition_record(problem, selected, rho),
            ):
                if ensure_planned(layout, builder):
                    added += 1
    for problem in _robustness_problems(problems):
        if problem["primary_calibration_id"] not in represented_ids:
            continue
        for m_off, m_on in COARSE_PAIRS:
            record = _pair_record(problem, m_off, m_on, problem["rho"])
            if ensure_planned(layout, record):
                added += 1
        record = _target_record(problem, problem["rho"])
        if ensure_planned(layout, record):
            added += 1
        existing = _read_calibration(layout, problem["calibration_id"]) or fresh_calibration(problem)
        if existing.get("status") in TERMINAL_STATUSES:
            if existing.get("selected_solution"):
                if ensure_planned(layout, _control_composition_record(problem, existing["selected_solution"], problem["rho"])):
                    added += 1
                if ensure_planned(layout, _target_composition_record(problem, problem["rho"])):
                    added += 1
            continue
        target = index.target(problem["t_expression"], problem["rho"], problem["alphabet"])
        points = index.pair_map(problem["structure_id"], problem["rho"], problem["alphabet"])
        if target is None or not coarse_complete(points):
            continue
        updated, requests = step_problem(existing, points, target, scales_for(target), MATCH_TOLERANCE)
        atomic_write_json(_calibration_path(layout, problem["calibration_id"]), updated)
        for m_off, m_on in requests:
            record = _pair_record(problem, m_off, m_on, problem["rho"])
            if ensure_planned(layout, record):
                added += 1
    return added


def _primary_terminal(layout: Layout, problems: list[dict]) -> bool:
    for problem in problems:
        state = _read_calibration(layout, problem["calibration_id"])
        if state is None or state.get("status") not in TERMINAL_STATUSES:
            return False
    return True


def phase(root: Path) -> str:
    layout = Layout(root)
    if not (layout.plan() / "problems.json").exists():
        return "00_PLAN"
    manifest = read_json(layout.manifest_path())
    problems = _problems_on_disk(layout)
    if not _primary_terminal(layout, problems):
        state = load_state(layout)
        index = work_index(layout)
        pending = [
            index[item_id]
            for item_id, slot in state.items()
            if slot.get("status") == "pending" and item_id in index
        ]
        if any(row["kind"] == "pair_point" for row in pending) and not any(
            (_read_calibration(layout, problem["calibration_id"]) or {}).get("status") == "refining" for problem in problems
        ):
            return "01_COARSE"
        return "02_ADAPTIVE"
    if manifest.get("profile") != "census":
        return "COMPLETE"
    state = load_state(layout)
    if any(slot.get("status") == "pending" for slot in state.values()):
        kinds = {work_index(layout)[item_id]["kind"] for item_id, slot in state.items() if slot.get("status") == "pending"}
        if kinds & {"target_composition", "control_composition"} and not (kinds & {"pair_point", "target_singleton"}):
            return "04_COMPOSITION"
        return "05_ROBUSTNESS"
    robustness = _robustness_problems(problems)
    if not _primary_terminal(layout, robustness):
        return "05_ROBUSTNESS"
    return "COMPLETE"


def counts(root: Path) -> dict:
    layout = Layout(root)
    if not (layout.plan() / "problems.json").exists():
        return {"calibrations_complete": 0, "calibrations_total": 0, "calibrations_unresolved": 0, "cache_hits": 0, "cache_misses": 0}
    problems = _problems_on_disk(layout)
    complete = 0
    unresolved = 0
    for problem in problems:
        state = _read_calibration(layout, problem["calibration_id"])
        if state is None:
            continue
        if state.get("status") in TERMINAL_STATUSES:
            complete += 1
        if state.get("status") == "unresolved_at_cap":
            unresolved += 1
    return {
        "cache_hits": 0,
        "cache_misses": 0,
        "calibrations_complete": complete,
        "calibrations_total": len(problems),
        "calibrations_unresolved": unresolved,
    }


def _vector(values) -> np.ndarray:
    return np.asarray(values, dtype=float)


def _erasure_baseline() -> dict:
    # SPEC_PATH lives in experiments/specs. The Generation 7 merge is under constraint-lab/generated.
    path = SPEC_PATH.parents[2] / "generated" / "generation-007" / "merge" / "summary.json"
    if not path.exists():
        return {}
    summary = read_json(path)
    found = {}
    for row in summary.get("rows") or []:
        erasure = next((control for control in row.get("controls") or [] if control.get("control_type") == "erasure"), None)
        if erasure is None:
            continue
        found[row["target_id"]] = (erasure.get("strategies") or {}).get("joint", {}).get("state_shape")
    return found


def merge_items(root: Path) -> dict:
    layout = Layout(root)
    problems = _problems_on_disk(layout)
    index = {row["item_id"]: row for row in work_index(layout).values()}
    items = {}
    for item_id, record in index.items():
        payload = read_valid_item(layout, item_id, _digest())
        if payload is not None:
            items[item_id] = payload
    baseline = _erasure_baseline()
    rows = []
    for problem in problems:
        state = _read_calibration(layout, problem["calibration_id"]) or {}
        rows.append(_assemble(layout, problem, state, items, index, baseline))
    unresolved = sum(1 for row in rows if row["status"] == "unresolved_at_cap")
    summary = {
        "analysis_version": ANALYSIS_VERSION,
        "calibration_version": CALIBRATION_VERSION,
        "complexity": complexity_rows(),
        "complexity_control": list(COMPLEXITY_CONTROL),
        "complexity_target": list(COMPLEXITY_TARGET),
        "completion_state": "COMPLETE_WITH_UNRESOLVED_CALIBRATIONS" if unresolved else "COMPLETE",
        "experiment_id": read_json(layout.manifest_path())["experiment_id"],
        "rows": rows,
        "schema": "rs-constraint-lab.generation-007b-merge/v1",
        "spec_hash": _digest(),
    }
    atomic_write_json(layout.root / "merge" / "summary.json", summary)
    for row in rows:
        atomic_write_json(layout.root / "merge" / "rows" / f"{row['calibration_id']}.json", {"row": row})
    return summary


def _find_item(items: dict, index: dict, kind: str, predicate) -> dict | None:
    for item_id, record in index.items():
        if record["kind"] != kind:
            continue
        if predicate(record["input"]) and item_id in items:
            return items[item_id]["result"]
    return None


def _direction_composition(control_direction: dict, target_direction: dict, solution_id: str, direction: str) -> dict:
    return {
        "Delta_S_C2": control_direction["delta_S"],
        "Delta_S_target": target_direction["delta_S"],
        "G_C2": control_direction["G"],
        "G_target": target_direction["G"],
        "I_C2": control_direction["I"],
        "I_target": target_direction["I"],
        "M_G_2": None
        if control_direction["G"] is None or target_direction["G"] is None
        else float(target_direction["G"] - control_direction["G"]),
        "M_I_2": None
        if control_direction["I"] is None or target_direction["I"] is None
        else float(abs(target_direction["I"]) - abs(control_direction["I"])),
        "direction": direction,
        "solution_id": solution_id,
        "spread_C2": control_direction["spread_C"],
        "spread_target": target_direction["spread_C"],
    }


def _paired_composition(control: dict | None, target_composition: dict | None, solution_id: str) -> list[dict]:
    if control is None or target_composition is None:
        return []
    return [
        _direction_composition(
            control["directions"][direction],
            target_composition["directions"][direction],
            solution_id,
            direction,
        )
        for direction in DIRECTIONS
    ]


def _component_mismatch(pair: dict | None, target: dict | None) -> tuple[float | None, float | None]:
    if pair is None or target is None:
        return None, None
    forward = float(pair["directions"]["path_to_matching"]["delta"] - target["directions"]["path_to_matching"]["delta"])
    reverse = float(pair["directions"]["matching_to_path"]["delta"] - target["directions"]["matching_to_path"]["delta"])
    return forward, reverse


def _robustness_rows(layout: Layout, problem: dict, primary: dict, items: dict, index: dict) -> list[dict]:
    if not is_robustness(problem) or not primary.get("selected_solution"):
        return []
    selected = primary["selected_solution"]
    rows = []
    recalibrations = {row["rho"]: row for row in _robustness_problems([problem])}
    for rho in ROBUSTNESS_RHOS:
        pair = _find_item(
            items,
            index,
            "pair_point",
            lambda item, rho=rho, selected=selected: item["structure_id"] == problem["structure_id"]
            and item["m_off"] == selected["m_off"]
            and item["m_on"] == selected["m_on"]
            and item["rho"] == rho
            and item["alphabet"] == problem["alphabet"],
        )
        target = _find_item(
            items,
            index,
            "target_singleton",
            lambda item, rho=rho: item["expression"] == problem["t_expression"] and item["rho"] == rho and item["alphabet"] == problem["alphabet"],
        )
        forward, reverse = _component_mismatch(pair, target)
        fixed_control = _find_item(
            items,
            index,
            "control_composition",
            lambda item, rho=rho, selected=selected: item.get("basin_id") == selected["basin_id"]
            and item["rho"] == rho
            and item["m_off"] == selected["m_off"]
            and item["m_on"] == selected["m_on"]
            and item["off_expression"] == problem["off_expression"]
            and item["p_expression"] == problem["p_expression"],
        )
        fixed_target = _find_item(
            items,
            index,
            "target_composition",
            lambda item, rho=rho: item["t_expression"] == problem["t_expression"]
            and item["p_expression"] == problem["p_expression"]
            and item["rho"] == rho,
        )
        recalibration = _read_calibration(layout, recalibrations[rho]["calibration_id"]) or {}
        recalibrated_solution = recalibration.get("selected_solution")
        recalibrated_composition = []
        if recalibrated_solution is not None:
            recalibrated_composition = _paired_composition(
                _find_item(
                    items,
                    index,
                    "control_composition",
                    lambda item, rho=rho, solution=recalibrated_solution: item.get("basin_id") == solution["basin_id"]
                    and item["rho"] == rho
                    and item["m_off"] == solution["m_off"]
                    and item["m_on"] == solution["m_on"]
                    and item["off_expression"] == problem["off_expression"]
                    and item["p_expression"] == problem["p_expression"],
                ),
                _find_item(
                    items,
                    index,
                    "target_composition",
                    lambda item, rho=rho: item["t_expression"] == problem["t_expression"]
                    and item["p_expression"] == problem["p_expression"]
                    and item["rho"] == rho,
                ),
                recalibrated_solution["basin_id"],
            )
        rows.append(
            {
                "fixed": {
                    "composition": _paired_composition(fixed_control, fixed_target, selected["basin_id"]),
                    "forward_mismatch": forward,
                    "inside_tolerance": forward is not None
                    and reverse is not None
                    and abs(forward) <= MATCH_TOLERANCE
                    and abs(reverse) <= MATCH_TOLERANCE,
                    "m_off": selected["m_off"],
                    "m_on": selected["m_on"],
                    "reverse_mismatch": reverse,
                },
                "recalibrated": {
                    "boundary_class": None if recalibrated_solution is None else recalibrated_solution.get("boundary_class"),
                    "composition": recalibrated_composition,
                    "forward_mismatch": None if recalibrated_solution is None else recalibrated_solution.get("forward_mismatch"),
                    "jacobian_condition": None if recalibrated_solution is None else recalibrated_solution.get("condition_number"),
                    "m_off": None if recalibrated_solution is None else recalibrated_solution.get("m_off"),
                    "m_on": None if recalibrated_solution is None else recalibrated_solution.get("m_on"),
                    "representation_label": recalibration.get("representation_label"),
                    "reverse_mismatch": None if recalibrated_solution is None else recalibrated_solution.get("reverse_mismatch"),
                    "solution_count": recalibration.get("solution_count", 0),
                    "status": recalibration.get("status"),
                },
                "rho": rho,
            }
        )
    return rows


def _assemble(layout: Layout, problem: dict, state: dict, items: dict, index: dict, baseline: dict) -> dict:
    selected = state.get("selected_solution")
    shape = None
    if selected is not None:
        pair = _find_item(
            items,
            index,
            "pair_point",
            lambda item: item["structure_id"] == problem["structure_id"]
            and item["m_off"] == selected["m_off"]
            and item["m_on"] == selected["m_on"]
            and item["rho"] == problem["rho"]
            and item["alphabet"] == problem["alphabet"],
        )
        target = _find_item(
            items,
            index,
            "target_singleton",
            lambda item: item["expression"] == problem["t_expression"] and item["rho"] == problem["rho"] and item["alphabet"] == problem["alphabet"],
        )
        if pair is not None and target is not None:
            shape = {}
            for direction, forward in (("path_to_matching", True), ("matching_to_path", False)):
                control = pair["directions"][direction]
                target_direction = target["directions"][direction]
                error = _vector(control["q"]) - _vector(target_direction["q"])
                aggregate = float(control["delta"]) - float(target_direction["delta"])
                shape[direction] = state_shape_report(
                    error,
                    _vector(control["mu"]),
                    int(pair["n_pairs"]),
                    aggregate,
                    float(target_direction["delta"]),
                    EFFECT_FLOOR,
                    MATCH_TOLERANCE,
                )
    compositions = []
    for solution in state.get("solutions") or []:
        if solution["basin_id"] not in set(composition_ids(state)):
            continue
        control = _find_item(
            items,
            index,
            "control_composition",
            lambda item, solution=solution: item.get("basin_id") == solution["basin_id"]
            and item["rho"] == problem["rho"]
            and item["p_expression"] == problem["p_expression"]
            and item["off_expression"] == problem["off_expression"],
        )
        target_composition = _find_item(
            items,
            index,
            "target_composition",
            lambda item: item["t_expression"] == problem["t_expression"]
            and item["p_expression"] == problem["p_expression"]
            and item["rho"] == problem["rho"],
        )
        compositions.extend(_paired_composition(control, target_composition, solution["basin_id"]))
    erasure = baseline.get(problem["target_id"])
    return {
        "adaptive_evaluations": state.get("adaptive_count"),
        "boundary_class": None if selected is None else selected.get("boundary_class"),
        "calibration_id": problem["calibration_id"],
        "cell": problem["cell"],
        "composition": compositions,
        "face": problem["face"],
        "forward_mismatch": None if selected is None else selected.get("forward_mismatch"),
        "geometry": problem["geometry"],
        "jacobian_condition": None if selected is None else selected.get("condition_number"),
        "joint_distance": None if selected is None else selected.get("distance"),
        "nominal": problem["nominal"],
        "polarity": problem["polarity"],
        "relation": problem["relation"],
        "representation_label": state.get("representation_label"),
        "reverse_mismatch": None if selected is None else selected.get("reverse_mismatch"),
        "robustness": _robustness_rows(layout, problem, state, items, index),
        "scalar_erasure_state_shape": erasure,
        "selected_m_off": None if selected is None else selected.get("m_off"),
        "selected_m_on": None if selected is None else selected.get("m_on"),
        "selection_reason": state.get("selection_reason"),
        "solution_count": state.get("solution_count", 0),
        "solutions": state.get("solutions") or [],
        "state_shape": shape,
        "status": state.get("status"),
        "target_id": problem["target_id"],
        "w_P": problem["w_P"],
        "w_T": problem["w_T"],
    }


def benchmark(root: Path) -> dict:
    from rs_constraint_lab.gen007_exec import choose_batch_count, solve_singleton
    from rs_constraint_lab.v07 import with_multiplier

    layout = Layout(root)
    layout.ensure()
    problems = _problems()
    problem = problems[0]
    slots = _slots()
    alphabet = problem["alphabet"]
    rho = PRIMARY_RHO
    off_rule = _rule(problem["off_expression"])
    on_rule = _rule(problem["on_expression"])
    samples = []
    for _repeat in range(3):
        for m_off, m_on in (("1.000000000000e+0", "1.000000000000e+0"), ("1.000000000000e-4", "1.000000000000e+4"), ("0", "1.000000000000e+0")):
            started = time.perf_counter()
            solve_pair_point(
                off_rule,
                on_rule,
                parse_multiplier_text(m_off),
                parse_multiplier_text(m_on),
                alphabet,
                rho,
                slots,
                {},
            )
            samples.append(time.perf_counter() - started)
    ordered = sorted(samples)
    from rs_constraint_lab.gen007_exec import _percentile

    pair_policy = {
        "items": choose_batch_count(samples),
        "max": ordered[-1],
        "p50": _percentile(ordered, 0.50),
        "p90": _percentile(ordered, 0.90),
        "samples": samples,
    }
    named = _rule(problem["on_expression"].replace(" => m_on", " => " + problem["w_T"]))
    scalar = with_multiplier(named)
    reference = []
    for text in ("1.000000000000e+0", "1.000000000000e-1"):
        multiplier = parse_multiplier_text(text)
        two = solve_pair_point(off_rule, on_rule, Fraction(1), multiplier, alphabet, rho, slots, {})
        one = solve_singleton(scalar, multiplier, alphabet, rho, slots, {}, None)
        both = solve_pair_point(off_rule, on_rule, multiplier, multiplier, alphabet, rho, slots, {})
        erased_rule = with_multiplier(_rule(problem["t_expression"].split(" | ")[0] + " => " + problem["w_T"]))
        erased = solve_singleton(erased_rule, multiplier, alphabet, rho, slots, {}, None)
        for label, left, right in (
            ("pair_face", two, one),
            ("erasure", both, erased),
        ):
            for direction in DIRECTIONS:
                reference.append(abs(float(left["directions"][direction]["delta"]) - float(right["directions"][direction]["delta"])))
    gap = max(reference)
    policy = {
        "calculation": "count = floor(45 / p90), then reduced while count * p90 > 60 or count * max > 100. count = 1 when p90 > 60.",
        "hard_timeout_seconds": 120,
        "kinds": {"default": {"items": 1}, "pair_point": pair_policy, "target_singleton": pair_policy, "target_composition": {"items": 1}, "control_composition": {"items": 1}},
        "numerical_reference_max_abs": gap,
        "numerical_reference_ok": gap < 1e-10,
        "schema": "rs-constraint-lab.batch-policy/v1",
        "target_seconds": 45,
        "watchdog_seconds": 120,
    }
    atomic_write_json(layout.policy_path(), policy)
    atomic_write_json(layout.plan() / "benchmark.json", policy)
    return policy
