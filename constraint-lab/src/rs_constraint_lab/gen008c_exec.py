"""Bounded Generation 8C mechanism execution.

Each item is one deterministic kernel or enumeration. The runner records
its wall clock and refuses an item that exceeds the 120-second watchdog.
No stochastic trajectory is sampled.
"""

from __future__ import annotations

import csv
import io
import time
from pathlib import Path

import numpy as np

from rs_constraint_lab.durable import atomic_write_json, read_json, sha256_file
from rs_constraint_lab.explore08 import plan_hash
from rs_constraint_lab.explore08a import PALETTE, load_repair_palette
from rs_constraint_lab.explore08c import (
    ANALYSIS_VERSION,
    CHAIN_RULE_TOLERANCE,
    CHECKPOINT_REPRODUCTION_TOLERANCE,
    CLOSED_FORM_TOLERANCE,
    CMI_TOLERANCE,
    DRIFT_TOLERANCE,
    EXPERIMENT_ID,
    GATE_MEMORY_TOLERANCE,
    KERNEL_ROW_TOLERANCE,
    MEMORY_CHECKPOINTS,
    MEMORY_SYSTEMS,
    PUBLISHED_BALANCED_CMI,
    PUBLISHED_CHECKPOINT,
    ROUND_ID,
    SINGLE_RULE_SYSTEMS,
    SOURCES,
    STATIONARY_DRIFT_TOLERANCE,
    SYMMETRY_TOLERANCE,
    ZERO_SYSTEMS,
    MechanismError,
    action_on_source,
    asymmetry_table,
    checkpoint_source,
    contribution_atlas,
    drift_report,
    excursion_report,
    gate_memory_curve,
    hierarchy_report,
    local_law_table,
    projection_counterfactual,
    projection_report,
    r05_local_law,
    single_rule_local_law,
    symmetry_report,
    topology_atlas,
    topology_shape_summary,
)

PLAN_RELPATH = "constraint-lab/exploration/generation-008c/round-c0-plan.json"
PARENT_TABLES_RELPATH = "constraint-lab/reports/generation-008b-round-b0-tables.json"
WATCHDOG_SECONDS = 120
SCHEMA = "rs-constraint-lab.mechanism-tables/v1"
ROUNDED_CHECKPOINT_TOLERANCE = 5e-6


def _plain(value):
    if isinstance(value, dict):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    if isinstance(value, np.generic):
        return value.item()
    return value


def c0_items() -> list[dict]:
    items: list[dict] = []
    for system_id in (*SINGLE_RULE_SYSTEMS, "R05"):
        items.append({"kind": "local-law", "source": None, "system": system_id})
    for source in SOURCES:
        items.append({"kind": "topology", "source": source, "system": None})
    for system_id in ("R00", "R01", "R02", "R04", "R06"):
        for source in SOURCES:
            items.append({"kind": "checkpoint", "source": source, "system": system_id})
    for system_id in MEMORY_SYSTEMS:
        for source in SOURCES:
            items.append({"kind": "excursion", "source": source, "system": system_id})
            items.append({"kind": "memory", "source": source, "system": system_id})
    for system_id, _round_id, _parent in PALETTE:
        items.append({"kind": "atlas", "source": None, "system": system_id})
        items.append({"kind": "drift", "source": None, "system": system_id})
    items.append({"kind": "symmetry", "source": None, "system": None})
    items.append({"kind": "counterfactual", "source": None, "system": None})
    items.append({"kind": "hierarchy", "source": None, "system": None})
    return items


def item_id(item: dict) -> str:
    parts = [item["kind"]]
    if item.get("system"):
        parts.append(item["system"])
    if item.get("source"):
        parts.append(item["source"])
    return "-".join(parts)


def item_path(root: Path, item: dict) -> Path:
    return root / item["kind"] / f"{item_id(item)}.json"


def _dispatch(item: dict) -> dict:
    kind = item["kind"]
    system_id = item.get("system")
    source = item.get("source")
    if kind == "local-law":
        if system_id == "R05":
            return r05_local_law()
        return single_rule_local_law(system_id)
    if kind == "topology":
        rows = [row for row in topology_atlas() if row["source_graph"] == source]
        return {"rows": rows, "source": source, "summary": topology_shape_summary(rows)[source]}
    if kind == "checkpoint":
        return checkpoint_source(system_id, source)
    if kind == "excursion":
        return excursion_report(system_id, source)
    if kind == "memory":
        return {"curve": gate_memory_curve(system_id, source), "source": source, "system": system_id}
    if kind == "atlas":
        atlas = contribution_atlas(system_id)
        projection = projection_report(system_id)
        return {"contribution": atlas, "projection": projection, "system": system_id}
    if kind == "drift":
        return drift_report(system_id)
    if kind == "symmetry":
        return symmetry_report()
    if kind == "counterfactual":
        return projection_counterfactual()
    if kind == "hierarchy":
        return hierarchy_report()
    raise MechanismError(f"unknown C0 item kind {kind}")


def execute_plan_item(item: dict) -> dict:
    started = time.perf_counter()
    result = _plain(_dispatch(item))
    wall = time.perf_counter() - started
    if wall > WATCHDOG_SECONDS:
        raise MechanismError(f"{item_id(item)} exceeded the {WATCHDOG_SECONDS}s watchdog ({wall:.1f}s)")
    return {"item": item, "item_id": item_id(item), "result": result, "wall_seconds": wall}


def prepare_c0_plan(repo: Path | None = None) -> dict:
    """Analysis contract. No C0 measurement is stored here."""
    systems = []
    for row in load_repair_palette():
        systems.append(
            {
                "expressions": list(row["expressions"]),
                "parent_round_id": row["parent_round_id"],
                "parent_system_id": row["parent_system_id"],
                "role": row.get("role"),
                "system_id": row["system_id"],
            }
        )
    parent = None
    if repo is not None:
        parent = sha256_file(repo / PARENT_TABLES_RELPATH)
    document = {
        "analysis_only": True,
        "analysis_version": ANALYSIS_VERSION,
        "comparison_contract": {
            "closed_form_balanced_cmi_candidates": {
                "strong_favour": PUBLISHED_BALANCED_CMI["favour"],
                "strong_suppress": PUBLISHED_BALANCED_CMI["suppress"],
            },
            "parent_tables_relpath": PARENT_TABLES_RELPATH,
            "parent_tables_sha256": parent,
            "role": "Previously published Generation 8B figures and the closed-form candidates. C0 does not read them as inputs to the derivation.",
            "rounded_checkpoint_1": [
                {"class_given_edge_count": values["class_given_edge_count"], "class_information": values["class_information"], "edge_count_information": values["edge_count_information"], "source": source, "system": system}
                for (system, source), values in PUBLISHED_CHECKPOINT.items()
            ],
            "rounded_checkpoint_tolerance": ROUNDED_CHECKPOINT_TOLERANCE,
        },
        "estimands": [
            "minimal sufficient coordinates of the six-slot pair-event law",
            "closed-form six-slot law and balanced I(current triad; next pair slot | full pair mask)",
            "R05 stratum mixture of that conditional mutual information",
            "one-step toggle atlas from each canonical 3-edge source",
            "checkpoint-1 joint of the initial triad, edge count, and graph class, from the pair-event epoch kernel",
            "triad-only excursion length and gate survival before the first pair event",
            "gate-bit and full-triad memory at pair-event checkpoints 0, 1, 2, 4, 8, 16, 32, 64",
            "per-mask contribution to full-mask slot information",
            "labelled information discarded by graph-isomorphism projection",
            "expected pair-event edge-count drift and its rule-induced part",
        ],
        "execution": {
            "commands": ["execute-item", "run-c0", "assemble"],
            "heartbeat": "one JSON file per item",
            "stochastic_trajectories": False,
            "supervisor": "not used; each item is an in-process kernel read under the watchdog",
            "watchdog_seconds": WATCHDOG_SECONDS,
        },
        "experiment_id": EXPERIMENT_ID,
        "items": c0_items(),
        "mode": "B",
        "new_controls": False,
        "parameter_fit": False,
        "question": "How does a higher-order triadic condition alter the local lower-order event law, how does visible graph topology convert that local event bias into edge-count versus shape changes, and why is the influence of the initial triadic context rapidly forgotten?",
        "round_id": ROUND_ID,
        "schema": "rs-constraint-lab.mechanism-plan/v1",
        "sources": list(SOURCES),
        "stochastic_trajectories": False,
        "systems": systems,
        "tolerances": {
            "chain_rule": CHAIN_RULE_TOLERANCE,
            "checkpoint_kernel_reproduction": CHECKPOINT_REPRODUCTION_TOLERANCE,
            "closed_form": CLOSED_FORM_TOLERANCE,
            "cmi_equality": CMI_TOLERANCE,
            "drift_identity": DRIFT_TOLERANCE,
            "gate_memory": GATE_MEMORY_TOLERANCE,
            "kernel_row": KERNEL_ROW_TOLERANCE,
            "stationary_drift": STATIONARY_DRIFT_TOLERANCE,
            "symmetry": SYMMETRY_TOLERANCE,
            "zero_information_floor": 1e-10,
        },
    }
    document["plan_hash"] = plan_hash(document)
    return document


def _require_plan_contract(plan: dict) -> None:
    if plan.get("stochastic_trajectories") is not False:
        raise MechanismError("execution refused: C0 does not add stochastic trajectories")
    if plan.get("new_controls") is not False or plan.get("parameter_fit") is not False:
        raise MechanismError("execution refused: C0 does not add controls or fit a parameter")
    if [row["system_id"] for row in plan.get("systems", [])] != [row[0] for row in PALETTE]:
        raise MechanismError("execution refused: C0 system palette drifted")
    if plan.get("experiment_id") != EXPERIMENT_ID or plan.get("round_id") != ROUND_ID:
        raise MechanismError("execution refused: plan identity drifted")


def require_c0_execution(
    repo: Path,
    commit: str | None,
    relpath: str,
    disk_path: Path | None = None,
    *,
    require_remote: bool = True,
) -> dict:
    from rs_constraint_lab.explore08 import FrozenPlanError, remote_contains, require_frozen_plan

    plan = require_frozen_plan(repo, commit, relpath, disk_path=disk_path)
    if require_remote and not remote_contains(repo, commit or ""):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    _require_plan_contract(plan)
    digest = sha256_file(repo / PARENT_TABLES_RELPATH)
    if digest != plan.get("comparison_contract", {}).get("parent_tables_sha256"):
        raise FrozenPlanError("execution refused: Generation 8B tables drifted from the frozen plan")
    return plan


def run_c0(root: Path, plan: dict) -> list[dict]:
    written = []
    for item in plan["items"]:
        payload = execute_plan_item(item)
        path = item_path(root, item)
        atomic_write_json(path, payload)
        written.append(payload)
    return written


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
        raise MechanismError("C0 assemble is missing items: " + ", ".join(missing))
    return loaded


def _parent_checkpoint(repo: Path, system_id: str, source: str) -> dict:
    document = read_json(repo / PARENT_TABLES_RELPATH)
    for row in document["checkpoints"]:
        if row["system_id"] == system_id and row["source_graph_class"] == source and row["checkpoint"] == 1:
            return row
    raise MechanismError(f"Generation 8B has no checkpoint 1 cell for {system_id} {source}")


def validate_payload(payload: dict, repo: Path | None = None) -> dict:
    """Tolerance checks. A failure is an execution problem, not a scientific verdict."""
    problems = []

    def check(name: str, gap: float, tolerance: float) -> None:
        if abs(gap) > tolerance:
            problems.append(f"{name} gap {gap} exceeds {tolerance}")

    laws = {row["system"]: row for row in payload["local_law"]}
    for system_id in SINGLE_RULE_SYSTEMS:
        row = laws[system_id]
        check(f"{system_id} closed form", row["gap"], CLOSED_FORM_TOLERANCE)
    check("R05 mixture", laws["R05"]["gap"], CLOSED_FORM_TOLERANCE)
    suppress = [laws[system_id]["enumerated_balanced_CMI"] for system_id in ("R01", "R02", "R04")]
    check("R01/R02/R04 equality", max(suppress) - min(suppress), CMI_TOLERANCE)
    if abs(laws["R01"]["analytic_balanced_CMI"] - laws["R06"]["analytic_balanced_CMI"]) <= CMI_TOLERANCE:
        problems.append("reciprocal multipliers produced the same balanced CMI")
    for row in payload["checkpoint_mi"]:
        check(f"{row['system']} {row['source']} chain rule", row["chain_rule_gap"], CHAIN_RULE_TOLERANCE)
        check(f"{row['system']} {row['source']} kernel row", row["kernel_row_error"], KERNEL_ROW_TOLERANCE)
    for summary in payload["topology_summary"].values():
        if summary["source_graph"] == "path" and summary["one_class_per_edge_count"]:
            problems.append("path has one class per edge count")
        if summary["source_graph"] in ("star", "triangle") and not summary["one_class_per_edge_count"]:
            problems.append(f"{summary['source_graph']} splits a class inside one edge count")
    for row in payload["gate_memory"]:
        check(f"{row['system']} {row['source']} checkpoint {row['checkpoint']} mass", row["distribution_mass"] - 1.0, GATE_MEMORY_TOLERANCE)
        if row["system"] == "R00":
            check(
                f"R00 {row['source']} checkpoint {row['checkpoint']} pair-mask information",
                row["I_initial_full_triad_current_pair_mask"],
                1e-10,
            )
    for system_id, atlas in payload["contribution_summary"].items():
        check(f"{system_id} balanced contribution sum", atlas["sum_gap_balanced"], CMI_TOLERANCE)
        check(f"{system_id} stationary contribution sum", atlas["sum_gap_stationary"], CMI_TOLERANCE)
    for system_id, projection in payload["projection_summary"].items():
        check(f"{system_id} projection loss account", projection["loss_sum_gap"], CMI_TOLERANCE)
    for row in payload["drift_summary"]:
        check(f"{row['system']} direct drift", row["direct_identity_gap"], DRIFT_TOLERANCE)
        check(f"{row['system']} per-state drift", row["per_state_drift_gap"], DRIFT_TOLERANCE)
        check(f"{row['system']} stationary drift", row["stationary_expected_drift"], STATIONARY_DRIFT_TOLERANCE)
        if row["closed_form_defined"]:
            check(f"{row['system']} closed-form drift", row["closed_form_gap"], DRIFT_TOLERANCE)
    symmetry = payload["symmetry"]
    check("R02 conjugacy", symmetry["r02_to_r01_transition_gap"], SYMMETRY_TOLERANCE)
    check("R04 conjugacy", symmetry["r04_to_r01_transition_gap"], SYMMETRY_TOLERANCE)
    if symmetry["preserves_graph_class"]:
        problems.append("a recorded conjugacy preserved every pair class")
    for row in payload["excursions"]:
        check(f"{row['system']} {row['source']} excursion mass", row["excursion_length_mass"] - 1.0, 1e-9)
        check(f"{row['system']} {row['source']} excursion residual", row["residual_unabsorbed"], 1e-9)
    if repo is not None:
        for system_id, source in (("R01", "path"), ("R06", "path"), ("R01", "star"), ("R06", "star")):
            parent = _parent_checkpoint(repo, system_id, source)
            got = next(row for row in payload["checkpoint_mi"] if row["system"] == system_id and row["source"] == source)
            for key, parent_key in (
                ("class_information", "exact_class_MI"),
                ("edge_count_information", "exact_edge_count_MI"),
                ("class_given_edge_count", "exact_class_given_edge_count_MI"),
            ):
                check(f"{system_id} {source} {key} vs 8B", got[key] - parent[parent_key], CHECKPOINT_REPRODUCTION_TOLERANCE)
        for system_id, source, field, target in (
            ("R06", "path", "class_information", 0.02798),
            ("R06", "path", "edge_count_information", 0.008801),
            ("R06", "path", "class_given_edge_count", 0.01918),
            ("R01", "path", "class_information", 0.01023),
            ("R01", "path", "edge_count_information", 0.001393),
            ("R01", "path", "class_given_edge_count", 0.008838),
        ):
            got = next(row for row in payload["checkpoint_mi"] if row["system"] == system_id and row["source"] == source)
            check(f"{system_id} rounded {field}", got[field] - target, ROUNDED_CHECKPOINT_TOLERANCE)
    return {"ok": not problems, "problems": problems}


def assemble_tables(root: Path, plan: dict, *, repo: Path | None = None, frozen_plan_commit: str | None = None) -> dict:
    loaded = _load_items(root, plan)
    local_rows = []
    for system_id in (*SINGLE_RULE_SYSTEMS, "R05"):
        local_rows.append(loaded[f"local-law-{system_id}"]["result"])
    topology_rows = []
    topology_summary = {}
    for source in SOURCES:
        item = loaded[f"topology-{source}"]["result"]
        topology_rows.extend(item["rows"])
        topology_summary[source] = dict(item["summary"])
        topology_summary[source]["source_graph"] = source
    checkpoint_rows = []
    checkpoint_mi = []
    for system_id in ("R00", "R01", "R02", "R04", "R06"):
        for source in SOURCES:
            result = loaded[f"checkpoint-{system_id}-{source}"]["result"]
            checkpoint_rows.extend(result["rows"])
            checkpoint_mi.append(
                {
                    "chain_rule_gap": result["epoch_mi"]["chain_rule_gap"],
                    "class_given_edge_count": result["epoch_mi"]["class_given_edge_count"],
                    "class_information": result["epoch_mi"]["class_information"],
                    "edge_count_information": result["epoch_mi"]["edge_count_information"],
                    "immediate_class_information": result["immediate_mi"]["class_information"],
                    "immediate_class_given_edge_count": result["immediate_mi"]["class_given_edge_count"],
                    "immediate_edge_count_information": result["immediate_mi"]["edge_count_information"],
                    "kernel_row_error": result["kernel_row_error"],
                    "source": source,
                    "system": system_id,
                    "total_variation_epoch_vs_immediate": result["total_variation_epoch_vs_immediate"],
                }
            )
    excursions = []
    memory_rows = []
    for system_id in MEMORY_SYSTEMS:
        for source in SOURCES:
            excursions.append(loaded[f"excursion-{system_id}-{source}"]["result"])
            memory_rows.extend(loaded[f"memory-{system_id}-{source}"]["result"]["curve"])
    contributions = []
    contribution_summary = {}
    projection_summary = {}
    projection_classes = []
    for system_id in [row[0] for row in PALETTE]:
        result = loaded[f"atlas-{system_id}"]["result"]
        contributions.extend(result["contribution"]["rows"])
        contribution_summary[system_id] = {key: value for key, value in result["contribution"].items() if key != "rows"}
        projection = result["projection"]
        projection_summary[system_id] = {key: value for key, value in projection.items() if key != "class_rows"}
        for row in projection["class_rows"]:
            projection_classes.append({"system": system_id, **{key: value for key, value in row.items() if key != "masks"}, "mask_count": row["mask_count"]})
    drift_rows = []
    drift_summary = []
    for system_id in [row[0] for row in PALETTE]:
        result = loaded[f"drift-{system_id}"]["result"]
        drift_rows.extend(result["rows"])
        drift_summary.append({key: value for key, value in result.items() if key != "rows"})
    payload = {
        "action_on_source": [row for system_id in ("R01", "R02", "R04", "R05", "R06") for row in action_on_source(system_id)],
        "analysis_version": ANALYSIS_VERSION,
        "asymmetry": asymmetry_table(),
        "checkpoint_mi": checkpoint_mi,
        "checkpoint_rows": checkpoint_rows,
        "contribution_summary": contribution_summary,
        "counterfactual": loaded["counterfactual"]["result"],
        "drift_rows": drift_rows,
        "drift_summary": drift_summary,
        "excursions": excursions,
        "experiment_id": EXPERIMENT_ID,
        "frozen_analysis_plan_commit": frozen_plan_commit,
        "gate_memory": memory_rows,
        "hierarchy": loaded["hierarchy"]["result"],
        "item_walls": [
            {"item_id": row["item_id"], "wall_seconds": row["wall_seconds"]}
            for row in loaded.values()
        ],
        "local_law": local_rows,
        "mask_contribution": contributions,
        "memory_checkpoints": list(MEMORY_CHECKPOINTS),
        "plan_hash": plan["plan_hash"],
        "projection_classes": projection_classes,
        "projection_summary": projection_summary,
        "round_id": ROUND_ID,
        "schema": SCHEMA,
        "stochastic_trajectories": False,
        "structural_zero_systems": list(ZERO_SYSTEMS),
        "symmetry": loaded["symmetry"]["result"],
        "topology": topology_rows,
        "topology_summary": topology_summary,
        "unit": "nats",
    }
    payload["validation"] = validate_payload(payload, repo)
    return payload


def write_payload(path: Path, payload: dict) -> dict:
    from rs_constraint_lab.gen008b_exec import payload_sha256

    body = dict(payload)
    body["payload_sha256"] = payload_sha256(payload)
    atomic_write_json(path, body)
    return body


def _csv(rows: list[dict], columns: list[str]) -> str:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=columns, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    for row in rows:
        rendered = {}
        for column in columns:
            value = row.get(column)
            if isinstance(value, list):
                value = " ".join(str(item) for item in value)
            rendered[column] = value
        writer.writerow(rendered)
    return buffer.getvalue()


def render_csvs(payload: dict) -> dict[str, str]:
    local_rows = []
    for row in payload["local_law"]:
        local_rows.append(
            {
                "action_direction": row.get("action_direction"),
                "analytic_balanced_CMI": row["analytic_balanced_CMI"],
                "condition_polarity": row.get("condition_polarity"),
                "enumerated_balanced_CMI": row["enumerated_balanced_CMI"],
                "gap": row["gap"],
                "minimal_state_coordinates": row.get("minimal_state_coordinates"),
                "multiplier": row.get("multiplier"),
                "q_active": row.get("q_active"),
                "q_inactive": row.get("q_inactive"),
                "system": row["system"],
            }
        )
    return {
        "generation-008c-local-law.csv": _csv(
            local_rows,
            ["system", "multiplier", "action_direction", "condition_polarity", "minimal_state_coordinates", "q_inactive", "q_active", "analytic_balanced_CMI", "enumerated_balanced_CMI", "gap"],
        ),
        "generation-008c-topology.csv": _csv(
            payload["topology"],
            ["source_graph", "slot", "pair_relation", "event_direction", "result_edge_count", "result_graph_class", "slot_topology_category"],
        ),
        "generation-008c-checkpoint-1.csv": _csv(
            payload["checkpoint_rows"],
            ["system", "source", "initial_gate", "destination_edge_count", "destination_class", "probability"],
        ),
        "generation-008c-checkpoint-1-mi.csv": _csv(
            payload["checkpoint_mi"],
            ["system", "source", "class_information", "edge_count_information", "class_given_edge_count", "immediate_class_information", "chain_rule_gap"],
        ),
        "generation-008c-gate-memory.csv": _csv(
            payload["gate_memory"],
            ["system", "source", "checkpoint", "I_initial_gate_current_gate", "Pr_current_gate_equals_initial_gate", "I_initial_full_triad_current_full_triad", "I_initial_gate_current_pair_mask", "I_initial_full_triad_current_pair_mask"],
        ),
        "generation-008c-mask-contribution.csv": _csv(
            payload["mask_contribution"],
            ["system", "pair_mask", "graph_class", "edge_count", "action_match_state", "balanced_CMI_contribution", "stationary_pair_event_weight", "stationary_CMI_contribution"],
        ),
        "generation-008c-drift.csv": _csv(
            payload["drift_rows"],
            ["system", "pair_mask", "triad_gate", "expected_delta_edges", "rule_induced_delta", "stationary_weight"],
        ),
    }


def publish_tables(payload: dict, reports: Path) -> None:
    from rs_constraint_lab.durable import atomic_write_text

    write_payload(reports / "generation-008c-round-c0-tables.json", payload)
    table_dir = reports / "tables"
    for name, text in render_csvs(payload).items():
        atomic_write_text(table_dir / name, text)
