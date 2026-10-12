"""Bounded commands for Generation 8B analysis round B0.

Each command is one durable item: one system's kernel results, one system's
initial-context permutations, or one system/source current-context permutation.
Corrected tables are assembled from those items. They are not computed inside
the plan commit.

Execution refuses unless the frozen plan commit is an ancestor of HEAD, the
plan hash matches, and, in production, a remote-tracking branch contains it.
"""

from __future__ import annotations

import hashlib
import sys
import time
from pathlib import Path

import numpy as np

from rs_constraint_lab.durable import atomic_write_json, sha256_file
from rs_constraint_lab.explore08 import CLASS_OF_MASK, FrozenPlanError, plan_hash, remote_contains, require_frozen_plan
from rs_constraint_lab.explore08a import repository_root, triad_config_id
from rs_constraint_lab.explore08b import (
    CHECKPOINTS,
    CURRENT_PERMUTATIONS,
    INITIAL_PERMUTATIONS,
    OCCUPANCY_HORIZON,
    ZERO_INFORMATION_FLOOR,
    ZERO_SYSTEMS,
    CalibrationError,
    analysis_constants,
    assert_zero_floor,
    balanced_slot_cmi,
    class_from_mask,
    coarse_class_cmi,
    decompose_class_information,
    distributions_at_starts,
    absorbing_survival,
    empirical_slot_cmi,
    empirical_state_weight,
    epoch_landing,
    first_destination_laws,
    information_from_conditionals,
    kernel_metadata,
    kernel_row_error,
    layout_guard,
    leading_order_bias,
    load_a0_palette,
    mask_class_decomposition,
    occupancy_shares_from_classes,
    pair_mask_law_span,
    pair_slot_laws,
    permutation_null_conditional,
    permutation_null_initial,
    propagate_pair_marginals,
    reproduce_plugin_tables,
    source_start_states,
    stationary_distribution,
    stationary_slot_cmi,
    stationary_state_weight,
    structural_triad_independence,
    symmetry_destination_gap,
    system_kernel,
    triad_weight_span,
    visits_from_slot_mask_cells,
)

PLAN_RELPATH = "constraint-lab/exploration/generation-008b/round-b0-plan.json"
PARENT_TABLES_RELPATH = "constraint-lab/reports/generation-008a-round-a0-tables.json"
PUBLISHED_RELPATH = "constraint-lab/reports/generation-008b-round-b0-tables.json"
SCHEMA = "rs-constraint-lab.information-calibration-tables/v1"
SOURCES = ("star", "path", "triangle")
CURRENT_ESTIMANDS = (
    ("current_triad_next_pair_slot_given_full_pair_mask", "full_pair_mask", "next_pair_slot"),
    ("current_triad_next_pair_slot_given_pair_class", "pair_graph_class", "next_pair_slot"),
    ("current_triad_next_pair_class_given_pair_class", "pair_graph_class", "next_pair_class"),
)
# Operational measurements from the implementation preflight.
# They justify the frozen floors. They are not B0 information results.
SOLVER_PREFLIGHT = {
    "block_epoch_seconds_baseline": 0.029,
    "chain_rule_gap_magnitude": "below 1e-15",
    "conditional_permutation_2000_seconds_estimate": 11.0,
    "cross_solver_gap_magnitude": "below 1e-15",
    "dense_epoch_seconds_baseline": 0.38,
    "initial_permutation_10000_seconds_estimate": 0.95,
    "kernel_build_seconds_baseline": 0.016,
    "max_unabsorbed_mass_at_512": 2.46e-22,
    "plugin_reproduction_cell_count": 336,
    "plugin_reproduction_max_abs_gap": 2.81e-16,
    "propagation_one_source_512_seconds": 4.58,
    "stationary_seconds_baseline": 0.21,
    "zero_control_identity_magnitude": "below 1e-14",
}


def lab_root() -> Path:
    return repository_root() / "constraint-lab"


def parent_tables_path() -> Path:
    return repository_root() / PARENT_TABLES_RELPATH


def _note(message: str) -> None:
    print(f"generation-008b {time.strftime('%H:%M:%S')} {message}", file=sys.stderr, flush=True)


def _num(value) -> float | None:
    if value is None:
        return None
    return float(value)


def _require_plan_contract(plan: dict) -> None:
    constants = analysis_constants()
    if plan.get("experiment_id") != "generation-008b-information-calibration":
        raise FrozenPlanError("execution refused: plan experiment id is not Generation 8B")
    if plan.get("round_id") != "round-b0":
        raise FrozenPlanError("execution refused: plan round is not B0")
    if plan.get("tolerances") != constants:
        raise FrozenPlanError("execution refused: frozen tolerances drifted from the analysis module")
    permutations = plan.get("permutations") or {}
    if permutations.get("initial_context") != INITIAL_PERMUTATIONS:
        raise FrozenPlanError("execution refused: initial permutation count drifted")
    if permutations.get("current_context") != CURRENT_PERMUTATIONS:
        raise FrozenPlanError("execution refused: current-context permutation count drifted")
    if plan.get("stochastic_trajectories") is not False:
        raise FrozenPlanError("execution refused: B0 does not add stochastic trajectories")
    if [row["system_id"] for row in plan.get("systems", [])] != [row["system_id"] for row in load_a0_palette()]:
        raise FrozenPlanError("execution refused: B0 system palette drifted")


def require_b0_execution(
    repo: Path,
    commit: str | None,
    relpath: str,
    disk_path: Path | None = None,
    *,
    require_remote: bool = True,
) -> dict:
    """Refuse B0 execution without a frozen, hash-matched, ancestral plan."""
    plan = require_frozen_plan(repo, commit, relpath, disk_path=disk_path)
    if require_remote and not remote_contains(repo, commit or ""):
        raise FrozenPlanError("execution refused: frozen plan commit is not on a remote-tracking branch")
    _require_plan_contract(plan)
    digest = sha256_file(parent_tables_path())
    if digest != plan.get("parent_tables_sha256"):
        raise FrozenPlanError("execution refused: Generation 8A tables drifted from the frozen plan")
    return plan


def prepare_b0_plan() -> dict:
    """Analysis contract. No corrected mutual-information values."""
    systems = []
    for row in load_a0_palette():
        systems.append(
            {
                "expressions": list(row["expressions"]),
                "parent_round_id": row["parent_round_id"],
                "parent_system_id": row["parent_system_id"],
                "role": row.get("role"),
                "system_id": row["system_id"],
            }
        )
    document = {
        "analysis_only": True,
        "analysis_version": "generation-008b-information/v1",
        "checkpoints": list(CHECKPOINTS),
        "epoch_solver": "block",
        "estimators": {
            "layer_a": "Generation 8A plug-in mutual information recomputed from the committed counts",
            "layer_b": "deterministic permutation of those counts; negative excess is stored",
            "layer_c": "deterministic kernel result from the pair-event epoch kernel and the full-event stationary distribution",
        },
        "execution": {
            "commands": [
                "exact --system one of R00-R07",
                "permute-initial --system one of R00-R07",
                "permute-current --system one of R00-R07 --source one of star/path/triangle",
            ],
            "cross_solver_check": "dense epoch kernel compared with the block kernel for every B0 system",
            "heartbeat": "stderr stage lines",
            "horizon_matched_mutual_information": "omitted when unabsorbed mass at pair epoch 512 is below unabsorbed_horizon_tolerance; the validation table stores that mass",
            "target_seconds": "30-60",
            "watchdog_seconds": 120,
            "workers": 2,
        },
        "experiment_id": "generation-008b-information-calibration",
        "first_destination": {
            "definition": "eventual hitting distribution of the other two 3-edge classes; the source class is transient and return to it is allowed",
            "prior": "uniform over the 16 raw triads",
            "route": "route_from_runs",
        },
        "miller_madow_reference": {
            "checkpoint_class": {"contexts": 16, "formula": "((dx-1)*(dy-1))/(2N)", "outcomes": 11, "samples": 256},
            "current_slot_given_full_mask_if_every_mask_is_occupied": {
                "conditioners": 64,
                "contexts": 16,
                "formula": "conditioners * ((dx-1)*(dy-1)) / (2N)",
                "outcomes": 6,
                "samples": 131072,
            },
            "first_destination": {"contexts": 16, "formula": "((dx-1)*(dy-1))/(2N)", "outcomes": 2, "samples": 256},
            "role": "sanity check beside permutation and kernel results",
        },
        "mode": "B",
        "occupancy": {
            "epochs": "1..512 inclusive",
            "excludes_initial_epoch": True,
            "observables": ["11 graph classes", "edge count via the class decomposition", "sparse", "3-edge", "dense"],
        },
        "parent_round_id": "round-a0",
        "parent_tables": PARENT_TABLES_RELPATH,
        "parent_tables_sha256": sha256_file(parent_tables_path()),
        "permutations": {
            "current_context": CURRENT_PERMUTATIONS,
            "current_context_estimands": [item[0] for item in CURRENT_ESTIMANDS],
            "current_context_null": "permute the triad inside each conditioner stratum; finite-table bias calibration, not a trajectory interval",
            "initial_context": INITIAL_PERMUTATIONS,
            "initial_context_estimands": ["first_destination", *[f"checkpoint_class_{step}" for step in CHECKPOINTS]],
            "initial_context_null": "permute raw-triad labels inside system x source; preserve episode outcomes and the 16-label multiset",
            "seed": "sha256-u64-v1 of experiment id, estimand id, system id, source graph, permutation index",
        },
        "round_id": "round-b0",
        "schema": "rs-constraint-lab.information-calibration-plan/v1",
        "solver_preflight": dict(SOLVER_PREFLIGHT),
        "sources": list(SOURCES),
        "stochastic_trajectories": False,
        "structural_zero_controls": list(ZERO_SYSTEMS),
        "structural_zero_reason": "pair-event weight does not read a triad slot or a full-state count literal, so the pair-mask trajectory is independent of the triad",
        "systems": systems,
        "tables": [
            "first_destination",
            "checkpoints",
            "occupancy",
            "occupancy_ranges",
            "current_context",
            "numerical_validation",
        ],
        "tolerances": analysis_constants(),
        "weightings": [
            {
                "id": "balanced_law",
                "question": "does the rule make the next pair-slot law depend on the triad once the pair mask is fixed",
                "state_weight": "uniform over the 1024 full states",
            },
            {
                "id": "a0_empirical_event_source",
                "question": "how much of that dependence was present in the states visited by the 512-pair-event atlas",
                "state_weight": "Generation 8A pre-pair-event state counts; the next slot is the exact local law",
            },
            {
                "id": "stationary_pair_event",
                "question": "how much of that dependence is experienced under the system's own long-run pair-event occupancy",
                "state_weight": "pi(s) times the probability the next full event is a pair event",
            },
        ],
    }
    document["plan_hash"] = plan_hash(document)
    return document


def _load_tables() -> dict:
    import json

    return json.loads(parent_tables_path().read_text(encoding="utf-8"))


def _index_tables(tables: dict) -> dict:
    return {
        "checkpoint": {
            (row["system_id"], row["source_graph_class"], int(row["checkpoint"])): row
            for row in tables["checkpoint_pair_class_information"]
        },
        "current": {(row["system_id"], row["source_graph_class"]): row for row in tables["current_context"]},
        "destination": {(row["system_id"], row["source_graph_class"]): row for row in tables["uniform_raw_triad_information"]},
    }


def _system_row(plan: dict, system_id: str) -> dict:
    for row in plan["systems"]:
        if row["system_id"] == system_id:
            return row
    raise CalibrationError(f"unknown B0 system {system_id}")


def _ranges(values: np.ndarray) -> float:
    return float(np.max(values) - np.min(values))


def analyse_exact(system_row: dict, indexed: dict) -> dict:
    """Layer C and numerical validation for one system. The kernel is built once."""
    system_id = system_row["system_id"]
    expressions = list(system_row["expressions"])
    _note(f"{system_id} kernel")
    independence = structural_triad_independence(expressions)
    if independence["structural_zero_control"] != (system_id in ZERO_SYSTEMS):
        raise CalibrationError(f"{system_id} structural classification does not match the B0 control list")
    kernel = system_kernel(expressions)
    layout_guard(kernel)
    metadata = kernel_metadata(kernel, expressions)
    landing, defect = epoch_landing(kernel, solver="block")
    _note(f"{system_id} dense cross-check")
    dense, dense_defect = epoch_landing(kernel, solver="dense")
    cross_gap = float(np.max(np.abs(landing - dense)))
    row_error = kernel_row_error(landing)
    if row_error > analysis_constants()["kernel_row_tolerance"]:
        raise CalibrationError(f"{system_id} epoch rows miss mass by {row_error}")
    if cross_gap > analysis_constants()["cross_solver_tolerance"]:
        raise CalibrationError(f"{system_id} dense and block kernels differ by {cross_gap}")
    laws = pair_slot_laws(kernel)
    slot_gap = float(np.max(np.abs(laws["conditional"].sum(axis=1) - 1.0)))
    if slot_gap > analysis_constants()["kernel_row_tolerance"]:
        raise CalibrationError(f"{system_id} pair-slot laws are not normalised")
    weight_span = triad_weight_span(kernel)
    mask_span = pair_mask_law_span(landing)
    _note(f"{system_id} stationary")
    stationary = stationary_distribution(kernel)
    if stationary["residual"] > analysis_constants()["stationary_residual_tolerance"]:
        raise CalibrationError(f"{system_id} stationary residual is {stationary['residual']}")
    balanced = balanced_slot_cmi(laws["conditional"])
    stationary_cmi = stationary_slot_cmi(kernel, stationary["pi"], laws["full_event"])
    stationary_weight = stationary_state_weight(stationary["pi"], laws["full_event"])
    stationary_coarse = coarse_class_cmi(stationary_weight, laws["conditional"])
    if system_id in ZERO_SYSTEMS:
        assert_zero_floor(weight_span, f"{system_id} triad weight span")
        assert_zero_floor(mask_span, f"{system_id} next pair-mask span")
        assert_zero_floor(balanced, f"{system_id} balanced-law CMI")
        assert_zero_floor(stationary_cmi, f"{system_id} stationary CMI")
        for label, value in stationary_coarse.items():
            assert_zero_floor(value, f"{system_id} stationary {label}")
    starts = source_start_states()
    ordered_starts: list[int] = []
    slices: dict[str, tuple[int, int]] = {}
    for source in SOURCES:
        slices[source] = (len(ordered_starts), len(ordered_starts) + len(starts[source]))
        ordered_starts.extend(starts[source])
    _note(f"{system_id} checkpoint propagation")
    propagated = propagate_pair_marginals(landing, ordered_starts)
    sources = []
    hitting_residual = 0.0
    total_gap = 0.0
    symmetry_gap = 0.0
    unabsorbed = 0.0
    chain_gap = 0.0
    identity_terms: list[float] = []
    for source in SOURCES:
        _note(f"{system_id} {source} route")
        begin, end = slices[source]
        state_list = ordered_starts[begin:end]
        source_class = int(CLASS_OF_MASK[state_list[0] & 63])
        solved = first_destination_laws(landing, source_class)
        hitting_residual = max(hitting_residual, float(solved["hitting_residual"]))
        total_gap = max(total_gap, float(solved["max_abs_total_gap"]))
        if solved["hitting_residual"] > analysis_constants()["hitting_residual_tolerance"]:
            raise CalibrationError(f"{system_id} {source} hitting residual is {solved['hitting_residual']}")
        if solved["max_abs_total_gap"] > analysis_constants()["hitting_residual_tolerance"]:
            raise CalibrationError(f"{system_id} {source} destination probabilities miss 1")
        height = distributions_at_starts(solved["height"], state_list)
        exact_destination = information_from_conditionals(height)
        gap = symmetry_destination_gap(expressions, state_list[0] & 63, height)
        symmetry_gap = max(symmetry_gap, gap)
        if gap > ZERO_INFORMATION_FLOOR:
            raise CalibrationError(f"{system_id} {source} symmetry-equivalent starts differ by L1 {gap}")
        survival = absorbing_survival(landing, state_list, OCCUPANCY_HORIZON, solved["destination_classes"])
        unabsorbed = max(unabsorbed, survival)
        checkpoints = []
        for step in CHECKPOINTS:
            mask = propagated["mask_at_checkpoint"][step][begin:end]
            class_conditional = class_from_mask(mask)
            pieces = decompose_class_information(class_conditional)
            mask_pieces = mask_class_decomposition(mask)
            chain_gap = max(chain_gap, abs(pieces["chain_rule_gap"]), abs(mask_pieces["chain_rule_gap"]))
            if abs(pieces["chain_rule_gap"]) > analysis_constants()["chain_rule_tolerance"]:
                raise CalibrationError(f"{system_id} {source} checkpoint {step} chain rule drifted")
            if abs(mask_pieces["chain_rule_gap"]) > analysis_constants()["chain_rule_tolerance"]:
                raise CalibrationError(f"{system_id} {source} checkpoint {step} mask chain rule drifted")
            checkpoints.append(
                {
                    "checkpoint": step,
                    "exact_class_given_edge_count_MI": pieces["class_given_edge_count"],
                    "exact_class_MI": pieces["class_information"],
                    "exact_edge_count_MI": pieces["edge_count_information"],
                    "exact_pair_mask_MI": mask_pieces["mask_information"],
                    "layer": "C",
                }
            )
            if system_id in ZERO_SYSTEMS:
                identity_terms.extend(
                    [
                        abs(pieces["class_information"]),
                        abs(pieces["edge_count_information"]),
                        abs(pieces["class_given_edge_count"]),
                        abs(mask_pieces["mask_information"]),
                    ]
                )
        class_share = propagated["class_occupancy_epochs_1_to_horizon"][begin:end]
        shares = occupancy_shares_from_classes(class_share)
        occupancy = []
        for triad in range(16):
            occupancy.append(
                {
                    "exact_3edge_share": _num(shares["three_edge_share"][triad]),
                    "exact_dense_minus_sparse": _num(shares["dense_minus_sparse"][triad]),
                    "exact_dense_share": _num(shares["dense_share"][triad]),
                    "exact_sparse_share": _num(shares["sparse_share"][triad]),
                    "raw_triad": triad_config_id(triad),
                }
            )
        ranges = {
            "class_l1": float(np.max(np.abs(class_share[:, None, :] - class_share[None, :, :]).sum(axis=2))),
            "dense_minus_sparse": _ranges(shares["dense_minus_sparse"]),
            "dense_share": _ranges(shares["dense_share"]),
            "sparse_share": _ranges(shares["sparse_share"]),
            "three_edge_share": _ranges(shares["three_edge_share"]),
        }
        if system_id in ZERO_SYSTEMS:
            identity_terms.append(abs(exact_destination))
            identity_terms.extend(abs(value) for value in ranges.values())
            for value in identity_terms:
                assert_zero_floor(value, f"{system_id} {source} zero-information identity")
        per_triad = []
        for triad in range(16):
            per_triad.append(
                {
                    "probabilities": [_num(value) for value in height[triad]],
                    "raw_triad": triad_config_id(triad),
                }
            )
        sources.append(
            {
                "checkpoints": checkpoints,
                "destination_classes": list(solved["destination_classes"]),
                "destination_by_triad": per_triad,
                "exact_destination_MI": exact_destination,
                "hitting_residual": _num(solved["hitting_residual"]),
                "layer": "C",
                "max_abs_total_gap": _num(solved["max_abs_total_gap"]),
                "occupancy": occupancy,
                "occupancy_ranges": ranges,
                "source_graph_class": source,
                "symmetry_gap": gap,
                "unabsorbed_mass_512": survival,
            }
        )
    return {
        "balanced_law_cmi": balanced,
        "chain_rule_gap_max": chain_gap,
        "cross_solver_gap": cross_gap,
        "deadlock_states": metadata["deadlock_states"],
        "dense_defect": dense_defect,
        "epoch_defect": defect,
        "fingerprint_sha256": metadata["fingerprint_sha256"],
        "kernel_row_error": row_error,
        "layer": "C",
        "null_identity_max": max(identity_terms) if identity_terms else None,
        "pair_mask_law_span": mask_span,
        "pair_slot_gap": slot_gap,
        "sources": sources,
        "stationary_arithmetic": stationary["arithmetic"],
        "stationary_coarse": stationary_coarse,
        "stationary_min_entry": stationary["min_entry"],
        "stationary_pair_event_cmi": stationary_cmi,
        "stationary_periods": stationary["periods"],
        "stationary_residual": stationary["residual"],
        "structural": independence,
        "symmetry_gap_max": symmetry_gap,
        "system_id": system_id,
        "triad_weight_span": weight_span,
        "unabsorbed_mass_max": unabsorbed,
        "hitting_residual": hitting_residual,
        "destination_total_gap_max": total_gap,
        "empirical_event_source": _empirical_from_kernel(system_id, laws, indexed),
    }


def _empirical_from_kernel(system_id: str, laws: dict, indexed: dict) -> list[dict]:
    rows = []
    for source in SOURCES:
        current = indexed["current"][(system_id, source)]
        mask_cells = current["cells"]["current_triad_next_pair_slot_given_full_pair_mask"]
        visits = visits_from_slot_mask_cells(mask_cells)
        if abs(float(visits.sum()) - 131072.0) > 1e-6:
            raise CalibrationError(f"{system_id} {source} visit total is {visits.sum()}")
        weight = empirical_state_weight(visits)
        exact_mask = empirical_slot_cmi(visits, laws["conditional"])
        coarse = coarse_class_cmi(weight, laws["conditional"])
        if system_id in ZERO_SYSTEMS:
            assert_zero_floor(exact_mask, f"{system_id} {source} empirical-source CMI")
            for label, value in coarse.items():
                assert_zero_floor(value, f"{system_id} {source} empirical {label}")
        rows.append(
            {
                "exact_next_pair_class_given_pair_class": coarse["next_pair_class_given_pair_class"],
                "exact_next_pair_slot_given_full_pair_mask": exact_mask,
                "exact_next_pair_slot_given_pair_class": coarse["next_pair_slot_given_pair_class"],
                "source_graph_class": source,
            }
        )
    return rows


def _published_plugin(row: dict) -> float:
    published = row.get("nats")
    if published is None:
        raise CalibrationError("a Generation 8A information cell has no nats value")
    return float(published)


def _flatten_null(summary: dict) -> dict:
    return {
        "null_median": summary["null_median"],
        "null_percentile_of_observed": summary["null_percentile_of_observed"],
        "permutation_05": summary["null_p05"],
        "permutation_50": summary["null_p50"],
        "permutation_95": summary["null_p95"],
        "permutation_99": summary["null_p99"],
        "permutation_null_mean": summary["null_mean"],
        "permutation_null_sd": summary["null_sd"],
        "plugin_minus_null": summary["plugin_minus_null_mean"],
        "plugin_MI": summary["observed_plugin"],
        "standardised_excess": summary["standardised_excess"],
    }


def permute_initial(system_row: dict, indexed: dict) -> dict:
    """Layer B for initial-context plug-in cells of one system."""
    system_id = system_row["system_id"]
    cells = []
    for source in SOURCES:
        destination = indexed["destination"][(system_id, source)]
        _note(f"{system_id} {source} first-destination permutations")
        summary = permutation_null_initial(
            destination["contingency"],
            estimand_id="first_destination",
            system_id=system_id,
            source_graph=source,
            count=INITIAL_PERMUTATIONS,
        )
        if abs(summary["observed_plugin"] - _published_plugin(destination)) > analysis_constants()["plugin_reproduction_tolerance"]:
            raise CalibrationError(f"{system_id} {source} first-destination plug-in drifted")
        cells.append({"estimand_id": "first_destination", "source_graph_class": source, **_flatten_null(summary), "layer": "B"})
        for step in CHECKPOINTS:
            published = indexed["checkpoint"][(system_id, source, step)]
            _note(f"{system_id} {source} checkpoint {step} permutations")
            summary = permutation_null_initial(
                published["contingency"],
                estimand_id=f"checkpoint_class_{step}",
                system_id=system_id,
                source_graph=source,
                count=INITIAL_PERMUTATIONS,
            )
            if abs(summary["observed_plugin"] - _published_plugin(published)) > analysis_constants()["plugin_reproduction_tolerance"]:
                raise CalibrationError(f"{system_id} {source} checkpoint {step} plug-in drifted")
            cells.append(
                {
                    "checkpoint": step,
                    "estimand_id": f"checkpoint_class_{step}",
                    "layer": "B",
                    "source_graph_class": source,
                    **_flatten_null(summary),
                }
            )
    return {"cells": cells, "layer": "B", "system_id": system_id}


def permute_current(system_row: dict, indexed: dict, source: str) -> dict:
    """Layer B finite-table calibration for one system and source."""
    system_id = system_row["system_id"]
    row = indexed["current"][(system_id, source)]
    cells = []
    for key, conditioner, outcome in CURRENT_ESTIMANDS:
        _note(f"{system_id} {source} {key}")
        summary = permutation_null_conditional(
            row["cells"][key],
            estimand_id=key,
            system_id=system_id,
            source_graph=source,
            count=CURRENT_PERMUTATIONS,
        )
        published = float(row[key]["nats"])
        if abs(summary["observed_plugin"] - published) > analysis_constants()["plugin_reproduction_tolerance"]:
            raise CalibrationError(f"{system_id} {source} {key} plug-in drifted")
        cells.append(
            {
                "calibration": summary["calibration"],
                "conditioner": conditioner,
                "estimand_id": key,
                "layer": "B",
                "outcome": outcome,
                "serial_dependence": summary["serial_dependence"],
                "source_graph_class": source,
                **_flatten_null(summary),
            }
        )
    return {"cells": cells, "layer": "B", "source_graph_class": source, "system_id": system_id}


def _compatibility(source_payload: dict, contingency: dict) -> dict:
    names = source_payload["destination_classes"]
    exact = np.array([row["probabilities"] for row in source_payload["destination_by_triad"]], dtype=np.float64)
    worst = 0.0
    pooled_counts = np.zeros(len(names), dtype=np.float64)
    for triad, row in enumerate(source_payload["destination_by_triad"]):
        counts = contingency[row["raw_triad"]]
        total = float(sum(counts.values()))
        for index, name in enumerate(names):
            empirical = float(counts.get(name, 0.0)) / total if total else 0.0
            worst = max(worst, abs(empirical - exact[triad, index]))
            pooled_counts[index] += float(counts.get(name, 0.0))
    pooled = pooled_counts / pooled_counts.sum()
    return {
        "max_abs_context": worst,
        "pooled_l1": float(np.abs(pooled - exact.mean(axis=0)).sum()),
    }


def assemble_tables(exact_payloads: list[dict], initial_payloads: list[dict], current_payloads: list[dict], indexed: dict) -> dict:
    """Join the three layers. Plug-in values come from the committed Generation 8A counts."""
    reproduction = reproduce_plugin_tables(_load_tables())
    if not reproduction["within_tolerance"]:
        raise CalibrationError(f"Generation 8A plug-in reproduction gap is {reproduction['max_abs_gap']}")
    exact_by = {row["system_id"]: row for row in exact_payloads}
    initial_by = {row["system_id"]: row for row in initial_payloads}
    current_by = {(row["system_id"], row["source_graph_class"]): row for row in current_payloads}
    first_rows = []
    checkpoint_rows = []
    occupancy_rows = []
    range_rows = []
    validation = []
    current_rows = []
    bias_destination = leading_order_bias(16, 2, 256)
    bias_checkpoint = leading_order_bias(16, 11, 256)
    for system_id in [row["system_id"] for row in load_a0_palette()]:
        exact = exact_by[system_id]
        initial = {(row["estimand_id"], row["source_graph_class"]): row for row in initial_by[system_id]["cells"]}
        validation.append(
            {
                "chain_rule_gap_max": exact["chain_rule_gap_max"],
                "cross_solver_gap": exact["cross_solver_gap"],
                "destination_total_gap_max": exact["destination_total_gap_max"],
                "fingerprint_sha256": exact["fingerprint_sha256"],
                "hitting_residual": exact["hitting_residual"],
                "kernel_row_error": exact["kernel_row_error"],
                "null_identity_max": exact["null_identity_max"],
                "pair_mask_law_span": exact["pair_mask_law_span"],
                "stationary_arithmetic": exact["stationary_arithmetic"],
                "stationary_periods": exact["stationary_periods"],
                "stationary_residual": exact["stationary_residual"],
                "structural_zero_control": exact["structural"]["structural_zero_control"],
                "symmetry_gap_max": exact["symmetry_gap_max"],
                "system_id": system_id,
                "triad_weight_span": exact["triad_weight_span"],
                "unabsorbed_mass_max": exact["unabsorbed_mass_max"],
            }
        )
        current_rows.append(
            {
                "conditioner": "full_pair_mask",
                "exact_law_CMI": exact["balanced_law_cmi"],
                "layer_exact": "C",
                "outcome": "next_pair_slot",
                "permutation_null_mean": None,
                "plugin_CMI": None,
                "source_or_weighting": "balanced_law",
                "system_id": system_id,
                "unit": "nats",
                "weighting": "balanced_law",
            }
        )
        current_rows.append(
            {
                "conditioner": "full_pair_mask",
                "exact_law_CMI": exact["stationary_pair_event_cmi"],
                "layer_exact": "C",
                "outcome": "next_pair_slot",
                "permutation_null_mean": None,
                "plugin_CMI": None,
                "source_or_weighting": "stationary_pair_event",
                "system_id": system_id,
                "unit": "nats",
                "weighting": "stationary_pair_event",
            }
        )
        for key, value in exact["stationary_coarse"].items():
            current_rows.append(
                {
                    "conditioner": "pair_graph_class",
                    "exact_law_CMI": value,
                    "layer_exact": "C",
                    "outcome": "next_pair_slot" if "slot" in key else "next_pair_class",
                    "permutation_null_mean": None,
                    "plugin_CMI": None,
                    "source_or_weighting": "stationary_pair_event",
                    "system_id": system_id,
                    "unit": "nats",
                    "weighting": "stationary_pair_event",
                }
            )
        empirical_by = {row["source_graph_class"]: row for row in exact["empirical_event_source"]}
        for source in SOURCES:
            source_exact = next(row for row in exact["sources"] if row["source_graph_class"] == source)
            plugin = initial[("first_destination", source)]
            contingency = indexed["destination"][(system_id, source)]["contingency"]
            compatibility = _compatibility(source_exact, contingency)
            first_rows.append(
                {
                    "destination_classes": source_exact["destination_classes"],
                    "exact_MI": source_exact["exact_destination_MI"],
                    "layer_exact": "C",
                    "layer_permutation": "B",
                    "layer_plugin": "A",
                    "miller_madow_full_alphabet": bias_destination,
                    "plugin_minus_exact": plugin["plugin_MI"] - source_exact["exact_destination_MI"],
                    "sampling_max_abs_context": compatibility["max_abs_context"],
                    "sampling_pooled_l1": compatibility["pooled_l1"],
                    "source_graph_class": source,
                    "system_id": system_id,
                    "unabsorbed_mass_512": source_exact["unabsorbed_mass_512"],
                    "unit": "nats",
                    **{key: plugin[key] for key in plugin if key not in {"estimand_id", "layer", "source_graph_class"}},
                }
            )
            for checkpoint in source_exact["checkpoints"]:
                step = checkpoint["checkpoint"]
                calibrated = initial[(f"checkpoint_class_{step}", source)]
                checkpoint_rows.append(
                    {
                        "checkpoint": step,
                        "exact_class_MI": checkpoint["exact_class_MI"],
                        "exact_class_given_edge_count_MI": checkpoint["exact_class_given_edge_count_MI"],
                        "exact_edge_count_MI": checkpoint["exact_edge_count_MI"],
                        "layer_exact": "C",
                        "layer_permutation": "B",
                        "layer_plugin": "A",
                        "miller_madow_full_alphabet": bias_checkpoint,
                        "null_median": calibrated["null_median"],
                        "null_percentile_of_observed": calibrated["null_percentile_of_observed"],
                        "optional_exact_pair_mask_MI": checkpoint["exact_pair_mask_MI"],
                        "permutation_05": calibrated["permutation_05"],
                        "permutation_50": calibrated["permutation_50"],
                        "permutation_95": calibrated["permutation_95"],
                        "permutation_99": calibrated["permutation_99"],
                        "permutation_null_mean": calibrated["permutation_null_mean"],
                        "permutation_null_sd": calibrated["permutation_null_sd"],
                        "plugin_class_MI": calibrated["plugin_MI"],
                        "plugin_minus_null": calibrated["plugin_minus_null"],
                        "source_graph_class": source,
                        "standardised_excess": calibrated["standardised_excess"],
                        "system_id": system_id,
                        "unit": "nats",
                    }
                )
            for occupancy in source_exact["occupancy"]:
                occupancy_rows.append({"layer": "C", "source_graph_class": source, "system_id": system_id, **occupancy})
            range_rows.append(
                {"layer": "C", "source_graph_class": source, "system_id": system_id, **source_exact["occupancy_ranges"]}
            )
            empirical = empirical_by[source]
            current_lookup = {
                row["estimand_id"]: row for row in current_by[(system_id, source)]["cells"]
            }
            mapping = {
                "current_triad_next_pair_slot_given_full_pair_mask": empirical["exact_next_pair_slot_given_full_pair_mask"],
                "current_triad_next_pair_slot_given_pair_class": empirical["exact_next_pair_slot_given_pair_class"],
                "current_triad_next_pair_class_given_pair_class": empirical["exact_next_pair_class_given_pair_class"],
            }
            for key, conditioner, outcome in CURRENT_ESTIMANDS:
                calibrated = current_lookup[key]
                current_rows.append(
                    {
                        "conditioner": conditioner,
                        "exact_law_CMI": mapping[key],
                        "layer_exact": "C",
                        "layer_permutation": "B",
                        "layer_plugin": "A",
                        "null_median": calibrated["null_median"],
                        "null_percentile_of_observed": calibrated["null_percentile_of_observed"],
                        "outcome": outcome,
                        "permutation_05": calibrated["permutation_05"],
                        "permutation_50": calibrated["permutation_50"],
                        "permutation_95": calibrated["permutation_95"],
                        "permutation_99": calibrated["permutation_99"],
                        "permutation_null_mean": calibrated["permutation_null_mean"],
                        "permutation_null_sd": calibrated["permutation_null_sd"],
                        "plugin_CMI": calibrated["plugin_MI"],
                        "plugin_minus_null": calibrated["plugin_minus_null"],
                        "serial_dependence": calibrated["serial_dependence"],
                        "source_or_weighting": source,
                        "standardised_excess": calibrated["standardised_excess"],
                        "system_id": system_id,
                        "unit": "nats",
                        "weighting": "a0_empirical_event_source",
                    }
                )
    return {
        "analysis_version": "generation-008b-information/v1",
        "checkpoints": checkpoint_rows,
        "current_context": current_rows,
        "experiment_id": "generation-008b-information-calibration",
        "first_destination": first_rows,
        "numerical_validation": validation,
        "occupancy": occupancy_rows,
        "occupancy_ranges": range_rows,
        "plugin_reproduction": {
            "cell_count": len(reproduction["cells"]),
            "max_abs_gap": reproduction["max_abs_gap"],
            "tolerance": reproduction["tolerance"],
            "within_tolerance": reproduction["within_tolerance"],
        },
        "round_id": "round-b0",
        "schema": SCHEMA,
        "unit": "nats",
    }


def file_sha256(path: Path) -> str:
    return sha256_file(path)


def payload_sha256(payload: dict) -> str:
    from rs_constraint_lab.durable import canonical_json

    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def write_payload(path: Path, payload: dict) -> dict:
    body = dict(payload)
    body["payload_sha256"] = payload_sha256(payload)
    atomic_write_json(path, body)
    return body



