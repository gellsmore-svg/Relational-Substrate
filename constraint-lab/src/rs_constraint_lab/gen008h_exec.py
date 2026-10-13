"""Frozen, atomic H0 execution. No non-neutral calculations occur in planning."""

from __future__ import annotations

import argparse
import platform
import sys
import time
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import numpy as np

from rs_constraint_lab.coherence import canonical_ledger_bytes
from rs_constraint_lab.durable import atomic_write_json, read_json, sha256_bytes, sha256_file
from rs_constraint_lab.explore08 import FrozenPlanError, plan_hash, remote_contains, require_frozen_plan
from rs_constraint_lab.history import (
    ANALYSIS_VERSION, DECAY_CHECKPOINTS, PRECISION, HistoryState, RecentReversal,
    analyse_kernel, analyse_temporal, analyse_witness, witness_specification,
)

PLAN_RELPATH = "constraint-lab/exploration/generation-008h/round-h0-plan.json"
SCHEMA = "rs-constraint-lab.history-tables/v1"
PALETTE = (("m025", "1/4"), ("m1", "1"), ("m4", "4"))
TOLERANCES = {
    "rational_identities": "exact", "row_sums": "exact", "stationary_residual": "exact",
    "uniform_joint_gap": "exact", "history_pair_independence_gap": "exact",
    "neutral_lumpability_gap": "exact", "information_formula_gap": "1e-13", "eigenvalue_gap": "1e-13",
}
SOURCE_PATHS = (
    "constraint-lab/src/rs_constraint_lab/history.py",
    "constraint-lab/src/rs_constraint_lab/gen008h_exec.py",
    "constraint-lab/src/rs_constraint_lab/graphs.py",
    "constraint-lab/src/rs_constraint_lab/state.py",
    "constraint-lab/src/rs_constraint_lab/exact.py",
    "constraint-lab/src/rs_constraint_lab/memory_clocks.py",
    "constraint-lab/src/rs_constraint_lab/durable.py",
    "constraint-lab/src/rs_constraint_lab/explore08.py",
)


class HistoryRunError(RuntimeError):
    """An execution, cache or exact result violates the frozen contract."""


def repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def h0_items() -> list[dict]:
    items = [{"item_id": f"H-{kind.upper()}-{label}", "kind": kind, "m": m} for label, m in PALETTE for kind in ("witness", "kernel", "temporal")]
    return items + [
        {"item_id": "H-FORMAL-NONLUMPABILITY", "kind": "nonlumpability", "m": None},
        {"item_id": "H-STATE-AUGMENTATION", "kind": "augmentation", "m": None},
    ]


def prepare_h0_plan() -> dict:
    spec = witness_specification()
    document = {
        "experiment_id": "generation-008h-history-as-state", "round_id": "H0", "mode": "A",
        "analysis_version": ANALYSIS_VERSION, "schema": SCHEMA,
        "parent_commit": "22e252e560cc711d337b6ae506b0fb76728247d6",
        "ontology": {"N": 4, "O": 3, "G": 0, "S": 0, "L": 0, "H_pair": 1, "hypergraph": "independent"},
        "controller": {
            "name": "RECENT-REVERSAL", "positive_multiplier": True, "ordinary_constraints": [],
            "baseline_weights": [1] * 10, "pair_update": "history := event slot", "triad_update": "history unchanged",
            "start_sentinel": None, "full_state_index": "7*x + (0 if h is None else h+1)",
            "recurrent_pair_index": "6*pair_mask+h", "history_depth_clock": "pair event",
        },
        "targets": [{"label": label, "m": m} for label, m in PALETTE],
        "witness": spec, "quotient_pair_masks": [0, spec["endpoint_state"], 63],
        "decay_checkpoints": list(DECAY_CHECKPOINTS), "decimal_precision": PRECISION,
        "tolerances": TOLERANCES, "items": h0_items(),
        "work_counts": {
            "atomic_items": 11, "target_models": 3, "full_witness_rows": 6, "pair_witness_rows": 6,
            "witness_paths": 6, "pair_epoch_kernels": 3, "pair_epoch_states_per_kernel": 384,
            "pair_epoch_transition_entries": 3 * 384 * 6,
            "direct_full_to_pair_block_solves": 3 * 3 * 7,
            "direct_raw_triad_rows": 3 * 3 * 7 * 16,
            "direct_slot_probability_checks": 3 * 3 * 7 * 16 * 6,
            "event_history_matrices": 3, "initial_history_checkpoint_cells": 3 * len(DECAY_CHECKPOINTS),
            "consistent_material_triples": 3 * 64 * 6 * 6,
            "two_step_augmented_paths": 3 * 384 * 6 * 6,
            "deterministic_full_state_updates": 1024 * 7 * 10,
        },
        "estimands": [
            "common-start equal-probability full-event histories with byte-identical ten-bit material endpoint",
            "full/pair row JS, exact row differences, and same edge-count/different graph-class laws",
            "strong lumpability of history erasure and fixed-state non-compilability",
            "exact next-pair closure against full-event absorption on all 16 raw triads",
            "384-state rational kernel, communicating structure, period and stationary joint balance",
            "pair/history independence, stationary material occupancy and history-averaged one-step pair law",
            "six-slot eigenstructure, repeat probability, consecutive-event MI and initial-history decay",
            "two-step material backtracking and order-two sufficiency against all consistent triples",
            "deterministic augmented-state update semantics and first-order Markov restoration",
        ],
        "coherence_inputs": [
            "F018-LOCAL-VERSUS-INITIAL", "F8C-CURRENT-SURVIVES",
            "F8G-FORMAL-CURRENT-STATE-EXPRESSIVITY", "F8G-FORMAL-EQUIVALENCE-HIERARCHY",
            "F8G-FORMAL-H-L-DISTINCTION", "F8G-FORMAL-COMPILATION-TEST",
            "Q-H-POSITIVE", "F011-QUOTIENT-INVALID",
        ],
        "pre_freeze_exposure": {
            "actual_non_neutral_H0_rows_kernels_cells": 0,
            "neutral_six_slot_plumbing": "declared; the neutral law is pre-observed, not claimed unopened",
            "synthetic_fixture": "three pair slots, one hidden slot, multiplier 2",
            "analytic_expectations": "externally predeclared symbolic derivations; no target-grade numerical verification",
        },
        "execution": {
            "workers": 1, "stochastic_trajectories": 0, "inline_atomic_items": True,
            "expected_total_wall_seconds": 60, "disk_estimate_bytes": 10_000_000,
            "item_opacity_limit_seconds": 60,
            "overrun_policy": "stop; freeze a supervised amendment before further items",
            "resume": "atomic item envelopes validated against plan hash, source version and exact invariants",
        },
        "non_claims": [
            "No absolute non-Markovianity or irreducible time claim.",
            "Order two and one-step H0 agreement refer to the pair-event clock.",
            "State augmentation changes representation and joint update support; it is not unchanged-state K/J compilation.",
            "No purpose, repair, fragility, adaptation, design or theology inferred.",
        ],
    }
    document["plan_hash"] = plan_hash(document)
    return document


def write_plan(root: Path | None = None) -> dict:
    root = root or repository_root()
    document = prepare_h0_plan()
    document["analysis_source_sha256"] = {path: sha256_file(root / path) for path in SOURCE_PATHS}
    document["planning_coherence_ledger_sha256"] = sha256_bytes(canonical_ledger_bytes(root / "constraint-lab/coherence"))
    calibration = root / "constraint-lab/exploration/generation-008h/calibration.json"
    document["calibration_sha256"] = sha256_file(calibration)
    document["plan_hash"] = plan_hash(document)
    atomic_write_json(root / PLAN_RELPATH, document)
    return document


def require_h0_execution(root: Path, commit: str | None, *, require_remote: bool = True) -> dict:
    plan = require_frozen_plan(root, commit, PLAN_RELPATH, disk_path=root / PLAN_RELPATH)
    if require_remote and not remote_contains(root, commit or ""):
        raise FrozenPlanError("H0 refused: frozen plan must be pushed before scientific execution")
    expected = prepare_h0_plan()
    for key, value in expected.items():
        if key != "plan_hash" and plan.get(key) != value:
            raise FrozenPlanError(f"H0 refused: frozen field {key} drifted")
    for path, digest in plan["analysis_source_sha256"].items():
        if sha256_file(root / path) != digest:
            raise FrozenPlanError(f"H0 refused: analysis source {path} drifted")
    if sha256_file(root / "constraint-lab/exploration/generation-008h/calibration.json") != plan["calibration_sha256"]:
        raise FrozenPlanError("H0 refused: pre-freeze calibration record drifted")
    return plan


def _require_zero(payload: dict, fields) -> None:
    for field in fields:
        if Fraction(payload[field]) != 0:
            raise HistoryRunError(f"exact identity failed: {field}")


def validate_result(kind: str, result: dict) -> None:
    if kind == "witness":
        if Fraction(result["path_probability_A"]) != Fraction(result["path_probability_B"]) or Fraction(result["path_probability_A"]) <= 0:
            raise HistoryRunError("common-start paths must have equal positive probability")
        if result["endpoint_material_bytes_A"] != result["endpoint_material_bytes_B"] or not result["edge_count_exact_equality"]:
            raise HistoryRunError("material/edge-count control failed")
        if Decimal(result["analytic_numeric_gap"]) > Decimal(TOLERANCES["information_formula_gap"]):
            raise HistoryRunError("witness information formula gap")
    elif kind == "kernel":
        _require_zero(result, ("stationary_residual", "uniform_joint_gap", "pair_marginal_gap", "history_pair_independence_gap", "row_sum_gap", "stationary_one_step_gap_vs_H0", "full_vs_pair_quotient_gap"))
        if result["communicating_class_count"] != 1 or result["period"] != 2:
            raise HistoryRunError("epoch communicating/period structure unexpected")
        if result["strong_lumpability"] != (Fraction(result["m"]) == 1):
            raise HistoryRunError("history-erasure lumpability mismatch")
    elif kind == "temporal":
        _require_zero(result, ("exact_eigen_gap", "history_row_sum_gap", "history_stationary_residual", "history_symmetry_gap", "matrix_power_gap", "backtrack_repeat_gap", "order2_sufficiency_gap"))
        if result["eigenvalue_gap"] > float(TOLERANCES["eigenvalue_gap"]) or Decimal(result["information_formula_gap"]) > Decimal(TOLERANCES["information_formula_gap"]):
            raise HistoryRunError("temporal analytic/numeric gap")
        expected = 1 if Fraction(result["m"]) == 1 else 2
        if result["projected_markov_order"] != expected:
            raise HistoryRunError("projected order mismatch")
    elif not result.get("verified"):
        raise HistoryRunError("formal verification item incomplete")


def _augmentation_check() -> dict:
    model = RecentReversal(Fraction(1))
    checked = 0
    for index in range(1024 * 7):
        state = model.state_from_index(index)
        if model.full_index(state) != index:
            raise HistoryRunError("augmented index does not invert")
        for event in range(10):
            target = model.advance(state, event)
            expected = event if event < 6 else state.recent_pair
            if target.material != state.material ^ (1 << event) or target.recent_pair != expected:
                raise HistoryRunError("deterministic history update failed")
            checked += 1
    return {"verified": True, "updates_checked": checked, "H_pair": 1, "material_bits": 10, "sentinel": None, "scope": "Markov on (x,h), not unchanged-state H0 compilation"}


def _evaluate(item: dict, directory: Path, plan: dict) -> dict:
    kind = item["kind"]
    if kind == "witness":
        return analyse_witness(Fraction(item["m"]))
    if kind == "kernel":
        return analyse_kernel(RecentReversal(Fraction(item["m"])), plan["quotient_pair_masks"])
    if kind == "temporal":
        return analyse_temporal(RecentReversal(Fraction(item["m"])))
    if kind == "augmentation":
        return _augmentation_check()
    witnesses = [read_json(directory / f"H-WITNESS-{label}.json")["result"] for label, _m in PALETTE]
    for result in witnesses:
        neutral = Fraction(result["m"]) == 1
        if (Fraction(result["full_row_max_difference"]) == 0) != neutral or (Fraction(result["pair_row_max_difference"]) == 0) != neutral:
            raise HistoryRunError("same-state divergent-row witness failed")
    return {
        "verified": True, "same_complete_x": True,
        "full_and_pair_rows_diverge_iff_non_neutral": True,
        "fixed_state_non_compilability": "one H0 row cannot equal two unequal history-conditioned rows",
        "scope": "unchanged ordinary x; finite state augmentation remains possible",
    }


def execute(root: Path, output: Path, commit: str | None) -> dict:
    plan = require_h0_execution(root, commit)
    directory = output / "items"
    directory.mkdir(parents=True, exist_ok=True)
    timings = []
    for position, item in enumerate(plan["items"], 1):
        path = directory / f"{item['item_id']}.json"
        print(f"[H0] {position}/{len(plan['items'])} active {item['item_id']}", flush=True)
        atomic_write_json(output / "status.json", {"active_item": item["item_id"], "completed": position - 1, "total": len(plan["items"]), "plan_hash": plan["plan_hash"]})
        if path.exists():
            envelope = read_json(path)
            if envelope.get("plan_hash") != plan["plan_hash"] or envelope.get("item") != item or envelope.get("analysis_version") != ANALYSIS_VERSION:
                raise HistoryRunError("cached item belongs to a different frozen analysis")
            validate_result(item["kind"], envelope["result"])
        else:
            started = time.monotonic()
            result = _evaluate(item, directory, plan)
            wall = time.monotonic() - started
            validate_result(item["kind"], result)
            if wall > plan["execution"]["item_opacity_limit_seconds"]:
                atomic_write_json(output / "status.json", {"status": "OVERRUN_STOP", "item": item, "wall_seconds": wall})
                raise HistoryRunError("H0 item exceeded 60 s; supervised frozen amendment required")
            envelope = {
                "schema": SCHEMA, "analysis_version": ANALYSIS_VERSION, "item": item,
                "plan_hash": plan["plan_hash"], "frozen_analysis_plan_commit": commit,
                "wall_seconds": wall, "result": result,
            }
            atomic_write_json(path, envelope)
        timings.append({"item_id": item["item_id"], "wall_seconds": envelope["wall_seconds"], "sha256": sha256_file(path)})
        print(f"[H0] complete {item['item_id']} ({envelope['wall_seconds']:.3f} s)", flush=True)
    atomic_write_json(output / "status.json", {"status": "COMPLETE", "completed": len(timings), "plan_hash": plan["plan_hash"], "timings": timings})
    return assemble(root, output, commit)


def assemble(root: Path, output: Path, commit: str | None) -> dict:
    plan = require_h0_execution(root, commit)
    by_kind = {"witness": [], "kernel": [], "temporal": [], "formal": []}
    hashes = {}
    for item in plan["items"]:
        path = output / "items" / f"{item['item_id']}.json"
        envelope = read_json(path)
        if envelope.get("plan_hash") != plan["plan_hash"] or envelope.get("item") != item:
            raise HistoryRunError("assembly found a mismatched item")
        validate_result(item["kind"], envelope["result"])
        by_kind[item["kind"] if item["kind"] in by_kind else "formal"].append(envelope["result"])
        hashes[item["item_id"]] = sha256_file(path)
    temporal = by_kind["temporal"]
    kernels = by_kind["kernel"]
    projected_fields = ("m", "two_step_backtrack_probability", "H0_backtrack_probability", "order1_witness_gap", "order2_sufficiency_gap", "projected_markov_order", "consistent_triples_checked", "order1_example")
    history_fields = ("m", "transition_matrix", "stationary_history", "repeat_probability", "nontrivial_eigenvalue", "multiplicity", "float_eigenvalues", "consecutive_event_MI", "analytic_consecutive_event_MI")
    details = {
        "witness": by_kind["witness"],
        "history-chain": [{key: value for key, value in row.items() if key in history_fields} for row in temporal],
        "pair-epoch": [{key: value for key, value in row.items() if key != "transitions"} for row in kernels],
        "kernels": [{"m": row["m"], "state_count": row["state_count"], "transitions": row["transitions"]} for row in kernels],
        "projected-process": [{**{key: row[key] for key in projected_fields}, "stationary_one_step_gap_vs_H0": kernels[i]["stationary_one_step_gap_vs_H0"]} for i, row in enumerate(temporal)],
        "initial-history-decay": [{**cell, "m": row["m"]} for row in temporal for cell in row["initial_history_decay"]],
        "formal-checks": by_kind["formal"], "validation": [],
    }
    for witness, kernel, temporal_row in zip(by_kind["witness"], kernels, temporal):
        details["validation"].append({
            "m": witness["m"], "precision_decimal_digits": PRECISION,
            "row_sum_gap": kernel["row_sum_gap"], "stationary_residual": kernel["stationary_residual"],
            "uniform_joint_gap": kernel["uniform_joint_gap"], "full_vs_pair_quotient_gap": kernel["full_vs_pair_quotient_gap"],
            "analytic_numeric_gap": witness["analytic_numeric_gap"], "eigenvalue_gap": temporal_row["eigenvalue_gap"],
            "information_formula_gap": temporal_row["information_formula_gap"], "matrix_power_gap": temporal_row["matrix_power_gap"],
            "order2_sufficiency_gap": temporal_row["order2_sufficiency_gap"],
        })
    detail_hashes = {}
    for name, rows in details.items():
        relpath = f"constraint-lab/reports/tables/generation-008h-{name}.json"
        atomic_write_json(root / relpath, rows)
        detail_hashes[relpath] = sha256_file(root / relpath)
    summary = {
        "schema": SCHEMA, "experiment_id": plan["experiment_id"], "round_id": "H0", "status": "COMPLETE",
        "analysis_version": ANALYSIS_VERSION, "plan_hash": plan["plan_hash"],
        "frozen_analysis_plan_commit": commit, "plan_file_sha256": sha256_file(root / PLAN_RELPATH),
        "work_counts": plan["work_counts"], "item_sha256": hashes, "detail_sha256": detail_hashes,
        "precision_decimal_digits": PRECISION, "tolerances": plan["tolerances"],
        "stochastic_trajectories": 0, "python": sys.version, "numpy": np.__version__, "platform": platform.platform(),
        "timings": read_json(output / "status.json")["timings"],
    }
    atomic_write_json(root / "constraint-lab/reports/generation-008h-round-h0-tables.json", summary)
    return summary


def verify(root: Path, output: Path, commit: str | None) -> dict:
    plan = require_h0_execution(root, commit)
    summary = read_json(root / "constraint-lab/reports/generation-008h-round-h0-tables.json")
    if summary["plan_hash"] != plan["plan_hash"] or summary["status"] != "COMPLETE":
        raise HistoryRunError("published summary does not match the frozen plan")
    for item in plan["items"]:
        path = output / "items" / f"{item['item_id']}.json"
        if sha256_file(path) != summary["item_sha256"][item["item_id"]]:
            raise HistoryRunError("atomic item digest mismatch")
        envelope = read_json(path)
        if envelope["plan_hash"] != plan["plan_hash"] or envelope["item"] != item:
            raise HistoryRunError("atomic item identity mismatch")
        validate_result(item["kind"], envelope["result"])
    for path, digest in summary["detail_sha256"].items():
        if sha256_file(root / path) != digest:
            raise HistoryRunError("published detail digest mismatch")
    return {"status": "VERIFIED", "items": len(plan["items"]), "details": len(summary["detail_sha256"]), "plan_hash": plan["plan_hash"]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("plan", "execute", "verify"))
    parser.add_argument("--frozen-plan-commit")
    parser.add_argument("--output", type=Path, default=repository_root() / "constraint-lab/generated/generation-008h/round-h0")
    args = parser.parse_args()
    root = repository_root()
    if args.command == "plan":
        plan = write_plan(root)
        print({"plan": PLAN_RELPATH, "plan_hash": plan["plan_hash"], "work_counts": plan["work_counts"]})
    elif args.command == "execute":
        result = execute(root, args.output, args.frozen_plan_commit)
        print({"status": result["status"], "plan_hash": result["plan_hash"]})
    else:
        print(verify(root, args.output, args.frozen_plan_commit))


if __name__ == "__main__":
    main()
