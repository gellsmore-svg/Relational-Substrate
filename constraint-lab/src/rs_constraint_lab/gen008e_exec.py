"""Bounded Generation 8E conjunctive-gate execution.

Each item is one K3 structural orbit at its four W4 grades, or one small
algebra item. A completed item file is not recomputed when a later item
fails. The runner records wall time and refuses an item past the
120-second watchdog. No stochastic trajectory is sampled.
"""

from __future__ import annotations

import csv
import io
import time
from pathlib import Path

from rs_constraint_lab.durable import atomic_write_json, atomic_write_text, canonical_json, read_json, sha256_bytes
from rs_constraint_lab.explore08 import plan_hash
from rs_constraint_lab.explore08e import (
    ANALYSIS_VERSION,
    BASIS_TOLERANCE,
    CMI_TOLERANCE,
    COMPARISON_TOLERANCE,
    D8_SYSTEMS_RELPATH,
    D8_SYSTEMS_SHA256,
    EXPERIMENT_ID,
    GRADES,
    INTERACTION_TOLERANCE,
    N_FULL_STATES,
    PROBABILITY_TOLERANCE,
    ROUND_ID,
    analyse_orbit,
    basis_items,
    boolean_constructions,
    census_summary,
    general_conjunction_check,
    k3_surface,
    load_d8_index,
    load_universe,
    parser_semantics,
    symbolic_additive_comparison,
    universe_public,
    w4_coverage,
)
from rs_constraint_lab.weights import alphabet_factors

PLAN_RELPATH = "constraint-lab/exploration/generation-008e/round-e0-plan.json"
WATCHDOG_SECONDS = 120
WALL_TIME_ESTIMATE_SECONDS = 120
DISK_ESTIMATE_BYTES = 5_000_000
SCHEMA = "rs-constraint-lab.conjunction-tables/v1"
ALGEBRA_ITEMS = ("parser", "symbolic", "basis", "w4-coverage", "boolean", "general-r", "surface")
ONTOLOGY = {"G": 0, "H": 0, "hypergraph": "independent", "L": 0, "N": 4, "O": 3, "S": 0}


class ConjunctionRunError(RuntimeError):
    """The E0 runner refused a plan, an item, or a table."""


def item_id(item: dict) -> str:
    if item["kind"] == "orbit":
        return f"orbit-{item['orbit_id']}"
    return item["kind"]


def item_path(root: Path, item: dict) -> Path:
    return root / "items" / f"{item_id(item)}.json"


def e0_items() -> list[dict]:
    items = [{"kind": "orbit", "orbit_id": orbit["orbit_id"]} for orbit in load_universe()["orbits"]]
    items.extend({"kind": kind, "orbit_id": None} for kind in ALGEBRA_ITEMS)
    return items


def _universe_record() -> dict:
    public = universe_public()
    return {
        "labelled_rule_count": public["labelled_rule_count"],
        "sha256": sha256_bytes(canonical_json(public).encode("utf-8")),
        "structural_orbit_count": public["structural_orbit_count"],
        "weighted_system_count": public["weighted_system_count"],
    }


def prepare_e0_plan(repo: Path | None = None) -> dict:
    """Analysis contract. No E0 measurement is stored here."""
    del repo
    universe = _universe_record()
    weighted = universe["weighted_system_count"]
    factors = alphabet_factors("W4")
    document = {
        "analysis_only": True,
        "analysis_version": ANALYSIS_VERSION,
        "canonicalisation": {
            "bit_complement": False,
            "condition_order": "sorted by triad slot",
            "vertex_permutations": 24,
            "weight_reciprocity": False,
        },
        "comparison": {
            "d8_table": D8_SYSTEMS_RELPATH,
            "d8_table_sha256": D8_SYSTEMS_SHA256,
            "d8_weighted_systems": 3584,
            "fingerprints": ["labelled_law_sha256", "local_law_class (S4 minimum)"],
            "one_rule_catalogue": "the 433 empty, unconditional and one-gate laws of Generation 8D",
        },
        "estimands": [
            "labelled K3 rules: pair action, two distinct triad literals, one weight",
            "S4 structural orbits and W4 weighted systems",
            "parser semantics and K for a two-triad conjunction",
            "exact local law and truth table in literal coordinates",
            "minimal raw coordinates and effective gate dimension",
            "literal and raw second discrete differences of the action log multiplier",
            "gate interaction order",
            "balanced I(current triad; next pair slot | full pair mask), enumerated and analytic",
            "balanced rule-induced edge drift, enumerated and analytic",
            "exact labelled and S4 law matches against the Generation 8D weighted systems",
            "symbolic additive non-representability by exact rank",
            "Moebius and corner bases and their transformation",
            "W4 coverage of the two bases",
            "targeted XOR, XNOR and four-corner constructions",
            "targeted check of the r-literal monomial law for r = 1..4",
        ],
        "execution": {
            "atomic_item": "one K3 structural orbit at its four W4 grades, or one algebra item",
            "commands": ["execute-item", "run-e0", "assemble"],
            "heartbeat": "status.json rewritten after each completed or skipped item",
            "resume": "an item file that already exists is not recomputed",
            "stochastic_trajectories": False,
            "supervisor": "not used; the whole round is a few seconds",
            "watchdog_seconds": WATCHDOG_SECONDS,
            "workers": 1,
        },
        "experiment_id": EXPERIMENT_ID,
        "history": False,
        "items": e0_items(),
        "meta_constraints": False,
        "mode": "B",
        "new_controls": False,
        "ontology": ONTOLOGY,
        "parameter_fit": False,
        "question": "What genuinely new local relational structure appears when one ordinary constraint can read two higher-order relations conjunctively?",
        "round_id": ROUND_ID,
        "schema": "rs-constraint-lab.conjunction-plan/v1",
        "stochastic_trajectories": False,
        "timing_sample": {
            "note": "Before this plan was frozen, orbit K3-00 was analysed as a smoke test, and the unit tests analysed K3-00 and K3-03 as representatives and ran every algebra item. Those values were seen. The smoke test took about 3.7 seconds of process time, including the universe build and the 8D index load. No other orbit was analysed before the freeze.",
            "pre_freeze_algebra_items_run_by_tests": ["parser", "symbolic", "basis", "w4-coverage", "boolean", "general-r"],
            "smoke_test_orbits": ["K3-00", "K3-03"],
        },
        "tolerances": {
            "basis_reconstruction": BASIS_TOLERANCE,
            "canonicalisation": "exact",
            "cmi": CMI_TOLERANCE,
            "d8_comparison_law_equality": COMPARISON_TOLERANCE,
            "fraction_law_equality": "exact",
            "interaction_coefficient": INTERACTION_TOLERANCE,
            "probability_gap": PROBABILITY_TOLERANCE,
        },
        "universe": universe,
        "weight_alphabet": {
            "factors": {name: f"{factors[name].numerator}/{factors[name].denominator}" for name in GRADES},
            "grades": list(GRADES),
            "name": "W4",
            "neutral_excluded": True,
        },
        "work_count": {
            "algebra_items": len(ALGEBRA_ITEMS),
            "d8_comparison_fingerprints": weighted * 2,
            "disk_estimate_bytes": DISK_ESTIMATE_BYTES,
            "full_state_evaluations": weighted * N_FULL_STATES,
            "items": universe["structural_orbit_count"] + len(ALGEBRA_ITEMS),
            "kernel_agreement_evaluations": weighted * N_FULL_STATES,
            "s4_law_images": weighted * 24,
            "structural_orbit_items": universe["structural_orbit_count"],
            "wall_time_estimate_seconds": WALL_TIME_ESTIMATE_SECONDS,
        },
    }
    document["plan_hash"] = plan_hash(document)
    return document


def _require_plan_contract(plan: dict) -> None:
    if plan.get("stochastic_trajectories") is not False or plan.get("history") is not False or plan.get("meta_constraints") is not False:
        raise ConjunctionRunError("execution refused: E0 does not add trajectories, history or meta-constraints")
    if plan.get("new_controls") is not False or plan.get("parameter_fit") is not False:
        raise ConjunctionRunError("execution refused: E0 does not add controls or fit a parameter")
    if plan.get("ontology") != ONTOLOGY:
        raise ConjunctionRunError("execution refused: E0 ontology drifted")
    if plan.get("experiment_id") != EXPERIMENT_ID or plan.get("round_id") != ROUND_ID:
        raise ConjunctionRunError("execution refused: plan identity drifted")
    if plan.get("universe") != _universe_record():
        raise ConjunctionRunError("execution refused: the K3 universe drifted from the frozen plan")
    if plan.get("items") != e0_items():
        raise ConjunctionRunError("execution refused: the item list drifted")


def require_e0_execution(repo: Path, commit: str | None, relpath: str, disk_path: Path | None = None, *, require_remote: bool = True) -> dict:
    from rs_constraint_lab.explore08 import FrozenPlanError, remote_contains, require_frozen_plan

    plan = require_frozen_plan(repo, commit, relpath, disk_path=disk_path)
    if require_remote and not remote_contains(repo, commit or ""):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    _require_plan_contract(plan)
    return plan


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def execute_plan_item(item: dict, *, repo: Path | None = None) -> dict:
    started = time.perf_counter()
    kind = item["kind"]
    if kind == "orbit":
        result = analyse_orbit(item["orbit_id"], d8_index=load_d8_index(repo or _repo_root()))
    elif kind == "parser":
        result = parser_semantics()
    elif kind == "symbolic":
        result = symbolic_additive_comparison()
    elif kind == "basis":
        result = basis_items()
    elif kind == "w4-coverage":
        result = w4_coverage()
    elif kind == "boolean":
        result = boolean_constructions()
    elif kind == "general-r":
        result = general_conjunction_check()
    elif kind == "surface":
        result = k3_surface()
    else:
        raise ConjunctionRunError(f"unknown E0 item kind {kind}")
    wall = time.perf_counter() - started
    if wall > WATCHDOG_SECONDS:
        raise ConjunctionRunError(f"{item_id(item)} exceeded the {WATCHDOG_SECONDS}s watchdog ({wall:.1f}s)")
    return {"item": item, "item_id": item_id(item), "result": result, "wall_seconds": wall}


def _reusable(path: Path, item: dict) -> bool:
    if not path.is_file():
        return False
    try:
        payload = read_json(path)
    except (OSError, ValueError):
        return False
    return payload.get("item_id") == item_id(item) and "result" in payload


def run_e0(root: Path, plan: dict, *, repo: Path | None = None) -> list[dict]:
    summaries = []
    max_wall = 0.0
    skipped = 0
    total = len(plan["items"])
    for index, item in enumerate(plan["items"], start=1):
        path = item_path(root, item)
        reused = _reusable(path, item)
        if reused:
            payload = read_json(path)
            skipped += 1
        else:
            payload = execute_plan_item(item, repo=repo)
            atomic_write_json(path, payload)
        wall = float(payload["wall_seconds"])
        max_wall = max(max_wall, wall)
        summaries.append({"item_id": payload["item_id"], "skipped": reused, "wall_seconds": wall})
        atomic_write_json(
            root / "status.json",
            {
                "completed_items": index,
                "item_count": total,
                "last_item_id": payload["item_id"],
                "last_wall_seconds": wall,
                "max_wall_seconds": max_wall,
                "skipped_existing_items": skipped,
                "updated_unix": time.time(),
            },
        )
    return summaries


def validate(systems: list[dict], algebra: dict) -> list[str]:
    """Software checks. A failure is an execution problem, not a scientific ranking."""
    problems = []
    for s in systems:
        label = s["system_id"]
        if s["K"] != 3 or s["rule_cardinality"] != 1:
            problems.append(f"{label} is not one K=3 rule")
        if s["kernel_max_abs_gap"] != 0:
            problems.append(f"{label} kernel weights disagree with the product formula")
        if sum(row["state_count"] for row in s["truth_table"]) != N_FULL_STATES:
            problems.append(f"{label} truth table does not cover the state space")
        if sum(1 for row in s["truth_table"] if row["active"]) != 1:
            problems.append(f"{label} is not active on exactly one admissible literal corner")
        if s["interaction"]["literal_gap"] > INTERACTION_TOLERANCE or s["interaction"]["raw_gap"] > INTERACTION_TOLERANCE:
            problems.append(f"{label} interaction coefficient missed its derivation")
        if s["balanced_cmi_gap"] > CMI_TOLERANCE:
            problems.append(f"{label} balanced information missed the analytic form")
        if s["balanced_edge_drift"] != s["balanced_edge_drift_analytic"]:
            problems.append(f"{label} drift missed the analytic form")
    for row in algebra["surface"]["rows"]:
        if row["review_prediction_gap"] > CMI_TOLERANCE:
            problems.append(f"{row['grade']} analytic information differs from the review prediction")
    if algebra["parser"]["k"] != 3:
        problems.append("the parsed two-triad conjunction is not K=3")
    return problems


def _load_items(root: Path, plan: dict) -> dict[str, dict]:
    loaded = {}
    missing = []
    for item in plan["items"]:
        path = item_path(root, item)
        if not path.is_file():
            missing.append(item_id(item))
            continue
        loaded[item_id(item)] = read_json(path)
    if missing:
        raise ConjunctionRunError("E0 assemble is missing items: " + ", ".join(missing))
    return loaded


def assemble_tables(root: Path, plan: dict, *, frozen_plan_commit: str | None = None) -> dict:
    loaded = _load_items(root, plan)
    orbits, systems = [], []
    for item in plan["items"]:
        if item["kind"] != "orbit":
            continue
        result = loaded[item_id(item)]["result"]
        orbits.append(result)
        systems.extend(result["systems"])
    algebra = {kind: loaded[kind]["result"] for kind in ALGEBRA_ITEMS}
    problems = validate(systems, algebra)
    structural = [
        {
            "action_direction": o["descriptors"]["action_direction"],
            "canonical_rule": o["canonical_rule"],
            "condition_polarities": o["descriptors"]["condition_polarities"],
            "incidence_class": o["descriptors"]["incidence_class"],
            "literal_pattern": o["descriptors"]["literal_pattern"],
            "literal_polarity_relation": o["descriptors"]["literal_polarity_relation"],
            "orbit_id": o["orbit_id"],
            "orbit_size": o["orbit_size"],
            "shared_pair_relation": "action_is_shared_pair" if o["descriptors"]["action_equals_shared_pair"] else "action_is_not_shared_pair",
        }
        for o in orbits
    ]
    weighted = [
        {
            "balanced_CMI": s["balanced_cmi"],
            "balanced_edge_drift": s["balanced_edge_drift"],
            "distinct_local_law_rows": s["distinct_local_law_rows"],
            "effective_gate_dimension": s["effective_gate_dimension"],
            "gate_interaction_order": s["gate_interaction_order"],
            "grade": s["grade"],
            "K": s["K"],
            "labelled_law_sha256": s["labelled_law_sha256"],
            "local_law_class": s["local_law_class"],
            "minimal_coordinate_count": s["minimal_coordinate_count"],
            "multiplier": s["multiplier"],
            "orbit_id": s["structural_orbit_id"],
            "rule": s["canonical_weighted_rule"],
            "rule_cardinality": s["rule_cardinality"],
            "system_id": s["system_id"],
        }
        for s in systems
    ]
    truth = [dict(row, system_id=s["system_id"]) for s in systems for row in s["truth_table"]]
    interaction = [
        {
            "expected_literal_delta12": s["interaction"]["expected_literal_delta12"],
            "expected_raw_delta12": s["interaction"]["expected_raw_delta12"],
            "gap": max(s["interaction"]["literal_gap"], s["interaction"]["raw_gap"]),
            "literal_delta12": s["interaction"]["literal_delta12"],
            "raw_delta12": s["interaction"]["raw_delta12"],
            "system_id": s["system_id"],
        }
        for s in systems
    ]
    comparison = [
        {
            "8d_exact_labelled_match_count": s["comparison"]["d8_exact_labelled_match_count"],
            "8d_exact_s4_match_count": s["comparison"]["d8_exact_s4_match_count"],
            "one_rule_labelled_match": s["comparison"]["one_rule_k2_or_k1_labelled_match"],
            "symbolic_additive_representable": s["comparison"]["symbolic_additive_representable"],
            "system_id": s["system_id"],
        }
        for s in systems
    ]
    payload = {
        "algebra": algebra,
        "analysis_version": ANALYSIS_VERSION,
        "experiment_id": EXPERIMENT_ID,
        "frozen_analysis_plan_commit": frozen_plan_commit,
        "plan_hash": plan["plan_hash"],
        "round_id": ROUND_ID,
        "schema": SCHEMA,
        "stochastic_trajectories": False,
        "summary": census_summary(systems, orbits),
        "tables": {
            "basis": algebra["basis"]["examples"],
            "comparison_8d": comparison,
            "interaction": interaction,
            "structural_orbits": structural,
            "truth_tables": truth,
            "weighted_systems": weighted,
        },
        "validation": {"ok": not problems, "problems": problems},
        "wall_seconds_max": max(loaded[k]["wall_seconds"] for k in loaded),
    }
    return payload


def _csv(rows: list[dict], columns: list[str]) -> str:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=columns, lineterminator="\n", extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        writer.writerow({key: (canonical_json(row[key]) if isinstance(row[key], (list, dict)) else row[key]) for key in columns})
    return buffer.getvalue()


def publish_tables(payload: dict, reports: Path) -> dict[str, str]:
    tables = payload["tables"]
    summary = {key: value for key, value in payload.items() if key != "tables"}
    detail = {name: sha256_bytes(canonical_json(rows).encode("utf-8")) for name, rows in tables.items()}
    summary["detail_sha256"] = detail
    body = dict(summary)
    body["payload_sha256"] = sha256_bytes(canonical_json(summary).encode("utf-8"))
    atomic_write_json(reports / "generation-008e-round-e0-tables.json", body)
    table_dir = reports / "tables"
    for name, rows in tables.items():
        atomic_write_json(table_dir / f"generation-008e-{name.replace('_', '-')}.json", rows)
    atomic_write_text(
        table_dir / "generation-008e-weighted-systems.csv",
        _csv(tables["weighted_systems"], ["system_id", "orbit_id", "grade", "multiplier", "K", "rule_cardinality", "minimal_coordinate_count", "effective_gate_dimension", "gate_interaction_order", "distinct_local_law_rows", "balanced_CMI", "balanced_edge_drift"]),
    )
    atomic_write_text(
        table_dir / "generation-008e-structural-orbits.csv",
        _csv(tables["structural_orbits"], ["orbit_id", "canonical_rule", "orbit_size", "action_direction", "literal_polarity_relation", "literal_pattern", "incidence_class", "shared_pair_relation"]),
    )
    return {"payload_sha256": body["payload_sha256"], **detail}
