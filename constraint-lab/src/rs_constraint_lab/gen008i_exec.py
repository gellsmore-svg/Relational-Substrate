"""Frozen, resumable OpenThetical I0 execution and independent output verification."""

from __future__ import annotations

import argparse
import json
import platform
import re
import signal
import sys
import time
from collections import defaultdict
from dataclasses import asdict
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import numpy as np

from rs_constraint_lab.coherence import canonical_ledger_bytes
from rs_constraint_lab.durable import atomic_write_json, read_json, sha256_bytes, sha256_file
from rs_constraint_lab.explore08 import FrozenPlanError, plan_hash, remote_contains, require_frozen_plan
from rs_constraint_lab.history import PRECISION, HistoryError
from rs_constraint_lab.history_roles import FEATURES, FEATURE_BY_NAME, RoleController, role_orbits, structural_record
from rs_constraint_lab.role_atlas import (
    aggregate_quotient, analyse_controller, balance_gap, decomposition, fingerprint,
    material_partition, project, serial_rows,
)

VERSION = "generation-008i-historical-roles/v1"
PLAN = "constraint-lab/exploration/generation-008i/round-i0-plan.json"
EXPERIMENT = "generation-008i-history-role-grammar"
GRADES = (("m025", "1/4"), ("m4", "4"))
FULL_CHECK_FEATURES = ("ADJ_ANY", "FORM_ANY", "ADJ_FORM")
SOURCE_PATHS = tuple("constraint-lab/src/rs_constraint_lab/" + name for name in (
    "gen008i_exec.py", "history_roles.py", "role_atlas.py", "history.py", "exact.py",
    "memory_clocks.py", "state.py", "graphs.py", "durable.py", "explore08.py", "coherence.py",
))
INPUT_PATHS = (
    "research-methods/open-thetical-research.md",
    "constraint-lab/methodology/open-thetical-application.md",
    "constraint-lab/exploration/generation-008i/charter.md",
    "constraint-lab/exploration/generation-008i/open-thetical-possibilities.md",
    "constraint-lab/exploration/generation-008i/structural-orbits.json",
)
TOLERANCES = {
    "rational_identities": "exact", "quotient_aggregation": "exact", "S4_covariance": "exact",
    "stationary_residual": "exact", "stationary_normalisation": "exact", "KU_stationary_residual": "exact",
    "information_chain_gap": "1e-25", "labelled_remainder": "1e-25",
    "full_quotient_crosscheck": 1e-14, "Markov_order_conditional_gap": "exact",
}


def repository_root():
    return Path(__file__).resolve().parents[3]


def decode(value):
    if isinstance(value, str) and re.fullmatch(r"-?[0-9]+/[0-9]+", value):
        return Fraction(value)
    if isinstance(value, list):
        return [decode(item) for item in value]
    if isinstance(value, dict):
        return {key: decode(item) for key, item in value.items()}
    return value


def items():
    return [{"item_id": "I0-NEUTRAL", "kind": "neutral", "feature": "SAME_ANY", "m": "1"}] + [
        {"item_id": f"I0-{feature.name}-{label}", "kind": "controller", "feature": feature.name, "m": m}
        for feature in FEATURES for label, m in GRADES
    ] + [{"item_id": "I0-EQUIVALENCE-SYMMETRY", "kind": "equivalence"}]


def prepare_plan():
    structure = role_orbits()
    quotient_entries = sum(len({structure.orbit_of[((state // 6) ^ (1 << event)) * 6 + event] for event in range(6)}) for state in (group[0] for group in structure.members))
    document = {
        "experiment_id": EXPERIMENT, "round_id": "I0", "mode": "B / OTR", "analysis_version": VERSION,
        "parent_commit": "ad5b656e26fe66610b583aedccdd34593e13791a",
        "ontology": {"N": 4, "O": 3, "G": 0, "S": 0, "L": 0, "H_pair": 1, "hypergraph": "independent"},
        "method_source": {
            "path": INPUT_PATHS[0], "resolved_ref": "05b15b0d903d46070b99ac84f9cab1bd898046ba",
            "source_commit": "3840a7c2d566a520b2c7f98b2e699f81fb409675", "source_blob": "669754b54e4374d7f8c9a606b1faf4811b7b8569",
            "sha256": "2d9023955ddfaf269131033589c547cea7090c72caf2577ab28f7138dfb388dd",
            "authored_byte_status": "source itself is agent_transcription_pending_byte_comparison",
        },
        "features": [asdict(feature) for feature in FEATURES], "grades": list(GRADES), "items": items(),
        "semantics": {
            "weight": "m**BooleanFeature", "history_update": "pair e -> h=e; triad -> preserve h",
            "sentinel": "relation predicates inactive; current-only direction predicates remain active",
            "triads": "four unit-weight toggles, unread by controller",
            "pair_clock_closure": "w_e/(sum_pair_weights+4) geometric triad excursions -> w_e/sum_pair_weights",
            "S4_action": "simultaneous vertex relabelling of pair mask, h and event; every member's block row checked",
            "orbit_count": len(structure.members), "state_count": 384,
            "descriptor_use": "diagnostic only; collision orbits retained separately",
        },
        "probe_complementarity": {
            "A": "history relation without current direction, complements B/C; does not isolate conjunction",
            "B": "current direction without historical efficacy, complements A/C; not an H discovery",
            "C": "conjunction, contrasted with both controls; not a unique causal decomposition",
        },
        "estimands": [
            "exact augmented/orbit stationarity, irreducibility and period",
            "material mask/class/count/class-given-count laws",
            "equal-model neutral JS: pairmask, class, edge, conditional shape, conditional label",
            "pair/history, edge/history and class/history MI",
            "R,A_h,D_h,C_h marginal and RA,RC,DC joint role distributions",
            "SAME/ADJACENT/DISJOINT next-event mass, split FORM/DISSOLVE",
            "consecutive-slot joint/MI, repeat, adjacent, disjoint and two-step backtracking",
            "exact edge-count means, variance and lag-1/lag-2 correlation",
            "history-erasure strong lumpability and positive-past order-one witness",
            "all consistent triple-conditioned rows for order-two sufficiency",
            "KU uniform-history rows, exact material stationary law and JS decomposition",
            "Kpi stationary-history rows and exact marginal stationary balance",
            "augmented, quotient and material-projection reversibility kept separate",
            "nonzero quotient probability currents if present",
            "exact kernel/joint/material/Kpi/KU equivalence fingerprints",
            "explicit graph-complement feature conjugacy and grade reciprocity under identity/complement",
        ],
        "arithmetic": {
            "transition": "Fraction", "stationary": "exact rational balance on 28 role orbits and 11 material classes for KU",
            "information_decimal_digits": PRECISION, "full_oracle": "independent 384-state float overdetermined balance least-squares; no power iteration",
        },
        "independent_full_check_features": list(FULL_CHECK_FEATURES),
        "raw_triad_pair_masks": [0, 41, 63], "raw_triad_histories": [None, 0, 1, 2, 3, 4, 5],
        "reciprocity_scope": "identity or graph-complement maps among the declared palette; not proof of absence of every possible transformation",
        "tolerances": TOLERANCES,
        "work_counts": {
            "primary_cells": 22, "neutral_items": 1, "equivalence_symmetry_items": 1, "atomic_items": 24,
            "full_states_per_cell": 384, "role_orbits": len(structure.members),
            "primary_full_transition_entries": 22 * 384 * 6,
            "quotient_supported_entries_per_cell": quotient_entries,
            "primary_quotient_supported_entries": 22 * quotient_entries,
            "primary_exact_stationary_solves": 44,
            "primary_transition_covariance_comparisons": 22 * 24 * 384 * 6,
            "primary_consistent_material_triples": 22 * 64 * 6 * 6,
            "primary_two_step_augmented_paths": 22 * 384 * 6 * 6,
            "primary_raw_triad_block_solves": 22 * 3 * 7,
            "primary_raw_triad_rows": 22 * 3 * 7 * 16,
            "primary_raw_slot_checks": 22 * 3 * 7 * 16 * 6,
            "primary_independent_full_solves": 6, "directed_complement_checks": 22,
        },
        "pre_freeze_exposure": {
            "actual_non_neutral_I0_cells": 0, "neutral_production": "pre-observed and calibrated",
            "synthetic": "N=3 ADJ_FORM m=2; not a primary I0 cell",
            "structural": "all state orbits, descriptor collisions and Boolean covariance observed before freeze as authorised",
            "historical_8H": "available control; no new role-atlas grade used as a smoke test",
        },
        "execution": {
            "workers": 1, "expected_wall_seconds": 240, "disk_budget_bytes": 50_000_000,
            "item_watchdog_seconds": 120, "resume": "reuse only hash-valid item matching frozen plan/version/identity",
            "overrun": "stop and freeze an amendment before continuing; retain completed items",
            "stochastic_scientific_trajectories": 0,
        },
        "OTR_stop": "complete I0 first; retain all findings; >=5 next probes; at most two complementary frozen I1 probes or justified stop",
    }
    document["plan_hash"] = plan_hash(document)
    return document


def require_execution(root, commit, require_remote=True):
    plan = require_frozen_plan(root, commit, PLAN, disk_path=root / PLAN)
    if require_remote and not remote_contains(root, commit or ""):
        raise FrozenPlanError("I0 plan must be pushed before any scientific execution")
    expected = prepare_plan()
    for key, value in expected.items():
        if key != "plan_hash" and plan.get(key) != json.loads(json.dumps(value)):
            raise FrozenPlanError(f"I0 frozen field drift: {key}")
    for key in ("analysis_source_sha256", "frozen_input_sha256"):
        for path, digest in plan[key].items():
            if sha256_file(root / path) != digest:
                raise FrozenPlanError(f"I0 frozen file drift: {path}")
    if sha256_file(root / "constraint-lab/exploration/generation-008i/calibration.json") != plan["calibration_sha256"]:
        raise FrozenPlanError("I0 pre-freeze calibration drifted")
    return plan


def validate_result(result):
    if result.get("kind") == "equivalence":
        if any(Fraction(row["kernel_gap"]) or Fraction(row["stationary_gap"]) for row in result["complement_checks"]):
            raise HistoryError("declared FORM/DISSOLVE complement identity failed")
        return
    for key, value in result["validation"].items():
        limit = Decimal("1e-25") if "information" in key or key == "labelled_remainder" else Decimal(0)
        invalid = abs(value) > Fraction(limit) if isinstance(value, Fraction) else abs(Decimal(str(value))) > limit
        if invalid:
            raise HistoryError(f"frozen diagnostic failed: {key}={value}")
    if not result["catalog"]["S4_covariant"] or not result["catalog"]["quotient_valid"]:
        raise HistoryError("covariance or quotient invalid")
    if result["atlas"]["communicating_classes"] != 1 or result["atlas"]["period"] != 2:
        raise HistoryError("unexpected communicating structure: separate interpretation required")
    check = result["full_crosscheck"]
    if check["performed"]:
        for key, value in check.items():
            if key not in ("performed", "method") and value > TOLERANCES["full_quotient_crosscheck"]:
                raise HistoryError(f"full-state cross-check failed: {key}={value}")


def calibrate(root):
    if (root / PLAN).exists():
        raise HistoryError("calibration precedes the frozen plan")
    measurements = []
    for name, model in (
        ("neutral-production", RoleController("SAME_ANY", Fraction(1))),
        ("synthetic-three-slot", RoleController("ADJ_FORM", Fraction(2), 3)),
    ):
        started = time.monotonic()
        result = analyse_controller(model, independent_full=True)
        validate_result(result)
        measurements.append({"fixture": name, "N": model.n, "m": model.multiplier, "wall_seconds": time.monotonic() - started, "full_crosscheck": result["full_crosscheck"]})
    record = {"actual_non_neutral_I0_cells": 0, "measurements": measurements, "execution": "direct durable items, 120-second per-item signal watchdog"}
    atomic_write_json(root / "constraint-lab/exploration/generation-008i/calibration.json", record)
    return record


def write_plan(root):
    plan = prepare_plan()
    plan["analysis_source_sha256"] = {path: sha256_file(root / path) for path in SOURCE_PATHS}
    plan["frozen_input_sha256"] = {path: sha256_file(root / path) for path in INPUT_PATHS}
    plan["calibration_sha256"] = sha256_file(root / "constraint-lab/exploration/generation-008i/calibration.json")
    plan["planning_coherence_sha256"] = sha256_bytes(canonical_ledger_bytes(root / "constraint-lab/coherence"))
    plan["plan_hash"] = plan_hash(plan)
    atomic_write_json(root / PLAN, plan)
    return plan


def equivalence_atlas(records, neutral):
    groups = {}
    for field in ("kernel_fingerprint", "full_kernel_fingerprint", "stationary_fingerprint", "material_fingerprint", "projected_kernel_fingerprint", "KU_kernel_fingerprint"):
        table = defaultdict(list)
        for row in [neutral, *records]:
            table[row["catalog"][field]].append(row["controller_id"])
        groups[field] = [{"fingerprint": key, "controller_ids": value} for key, value in sorted(table.items())]
    by_key = {(row["catalog"]["feature"], Fraction(row["catalog"]["m"])): row for row in records}
    models = {key: RoleController(*key) for key in by_key}

    def mapped_gap(left, right, complement):
        mask = 63 if complement else 0
        target_rows = right.kernel()
        return max(
            abs(probability - target_rows[((source // 6) ^ mask) * 6 + source % 6].get(((target // 6) ^ mask) * 6 + target % 6, 0))
            for source, row in enumerate(left.kernel()) for target, probability in row.items()
        )

    complement_checks = []
    for key, row in by_key.items():
        feature, m = key
        spec = FEATURE_BY_NAME[feature]
        partner = feature.replace("_FORM", "_DISSOLVE") if spec.direction == "FORM" and spec.relation else (
            feature.replace("_DISSOLVE", "_FORM") if spec.direction == "DISSOLVE" and spec.relation else
            ("DISSOLVE_ANY" if feature == "FORM_ANY" else "FORM_ANY" if feature == "DISSOLVE_ANY" else feature)
        )
        other = by_key[partner, m]
        complement_checks.append({
            "source": row["controller_id"], "target": other["controller_id"],
            "map": "p xor 63; history unchanged",
            "kernel_gap": mapped_gap(models[key], models[partner, m], True),
            "stationary_gap": max(abs(row["stationary_joint"][state] - other["stationary_joint"][((state // 6) ^ 63) * 6 + state % 6]) for state in range(384)),
        })
    reciprocity = []
    for key, row in by_key.items():
        for feature in FEATURES:
            target_key = feature.name, 1 / key[1]
            for complement in (False, True):
                gap = mapped_gap(models[key], models[target_key], complement)
                reciprocity.append({
                    "source": row["controller_id"], "target": by_key[target_key]["controller_id"],
                    "map": "graph complement" if complement else "identity",
                    "kernel_gap": gap, "equivalent": gap == 0,
                })
    return {
        "kind": "equivalence", "groups": groups, "complement_checks": complement_checks,
        "reciprocity_checks": reciprocity, "reciprocity_matches": [row for row in reciprocity if row["equivalent"]],
        "scope": "fingerprints keep law/statistic levels separate; reciprocity tests identity/complement only",
    }


def _load_envelope(path, item, plan, commit):
    envelope = read_json(path)
    if envelope.get("analysis_version") != VERSION or envelope.get("plan_hash") != plan["plan_hash"] or envelope.get("item") != item or envelope.get("frozen_analysis_plan_commit") != commit:
        raise HistoryError("cached item identity or frozen analysis does not match")
    if fingerprint(envelope["result"]) != envelope["result_sha256"]:
        raise HistoryError("cached scientific payload digest mismatch")
    validate_result(decode(envelope["result"]))
    return envelope


def execute(root, output, commit):
    plan = require_execution(root, commit)
    directory = output / "items"
    directory.mkdir(parents=True, exist_ok=True)
    timings = []
    for position, item in enumerate(plan["items"], 1):
        path = directory / (item["item_id"] + ".json")
        atomic_write_json(output / "status.json", {"status": "RUNNING", "active_item": item["item_id"], "completed": position - 1, "total": len(plan["items"]), "plan_hash": plan["plan_hash"]})
        print(f"[I0] {position}/{len(plan['items'])} active {item['item_id']}", flush=True)
        if path.exists():
            envelope = _load_envelope(path, item, plan, commit)
        else:
            started = time.monotonic()

            def timeout_handler(*_args):
                raise TimeoutError("120-second I0 item watchdog; retain completed items and freeze amendment")

            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(plan["execution"]["item_watchdog_seconds"])
            try:
                if item["kind"] == "equivalence":
                    primary = [decode(read_json(directory / (previous["item_id"] + ".json"))["result"]) for previous in plan["items"] if previous["kind"] == "controller"]
                    neutral = decode(read_json(directory / "I0-NEUTRAL.json")["result"])
                    result = equivalence_atlas(primary, neutral)
                else:
                    model = RoleController(item["feature"], Fraction(item["m"]))
                    result = analyse_controller(model, independent_full=item["kind"] == "neutral" or item["feature"] in FULL_CHECK_FEATURES)
                    result["controller_id"] = item["item_id"]
                    result["catalog"]["controller_id"] = item["item_id"]
                validate_result(result)
            except Exception as exc:
                atomic_write_json(output / "status.json", {"status": "STOPPED", "active_item": item, "error": str(exc), "completed": position - 1})
                raise
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
            wall = time.monotonic() - started
            envelope = {
                "schema": "rs-constraint-lab.role-atlas/v1", "analysis_version": VERSION,
                "item": item, "plan_hash": plan["plan_hash"], "frozen_analysis_plan_commit": commit,
                "wall_seconds": wall, "result_sha256": fingerprint(result), "result": result,
            }
            atomic_write_json(path, envelope)
        timings.append({"item_id": item["item_id"], "wall_seconds": envelope["wall_seconds"]})
        print(f"[I0] completed {item['item_id']} ({envelope['wall_seconds']:.3f}s)", flush=True)
    atomic_write_json(output / "status.json", {"status": "COMPLETE", "completed": len(timings), "timings": timings, "plan_hash": plan["plan_hash"]})
    return assemble(root, output, commit)


def assemble(root, output, commit):
    plan = require_execution(root, commit)
    records, item_hashes, timings = [], {}, []
    neutral = equivalence = None
    for item in plan["items"]:
        envelope = _load_envelope(output / "items" / (item["item_id"] + ".json"), item, plan, commit)
        published = "constraint-lab/reports/items/generation-008i/" + item["item_id"] + ".json"
        atomic_write_json(root / published, envelope)
        item_hashes[published] = sha256_file(root / published)
        timings.append({"item_id": item["item_id"], "wall_seconds": envelope["wall_seconds"]})
        result = decode(envelope["result"])
        if item["kind"] == "neutral":
            neutral = result
        elif item["kind"] == "equivalence":
            equivalence = result
        else:
            records.append(result)
    details = {
        "controller-catalog": [row["catalog"] for row in records],
        "stationary-atlas": [{"controller_id": row["controller_id"], **row["atlas"]} for row in records],
        "role-atlas": [{"controller_id": row["controller_id"], **row["roles"]} for row in records],
        "temporal-atlas": [{"controller_id": row["controller_id"], **row["temporal"]} for row in records],
        "validation": [{"controller_id": row["controller_id"], **row["validation"], "full_crosscheck": row["full_crosscheck"]} for row in records],
        "stationary-distributions": [{key: row[key] for key in ("controller_id", "stationary_joint", "stationary_orbit_masses", "stationary_history", "material", "KU_stationary_pair", "uniform_joint_gap")} for row in records],
        "kernels": [{key: row[key] for key in ("controller_id", "quotient_kernel", "KU_kernel", "K_pi")} for row in records],
        "currents": [{key: row[key] for key in ("controller_id", "full_augmented_detailed_balance_gap", "quotient_detailed_balance_gap", "quotient_currents", "one_way_augmented_transitions")} for row in records],
        "equivalence": equivalence, "neutral": neutral,
    }
    detail_hashes = {}
    for name, rows in details.items():
        path = "constraint-lab/reports/tables/generation-008i-" + name + ".json"
        atomic_write_json(root / path, rows)
        detail_hashes[path] = sha256_file(root / path)
    summary = {
        "experiment_id": EXPERIMENT, "round_id": "I0", "status": "COMPLETE", "analysis_version": VERSION,
        "frozen_analysis_plan_commit": commit, "plan_hash": plan["plan_hash"], "plan_file_sha256": sha256_file(root / PLAN),
        "primary_cells": len(records), "work_counts": plan["work_counts"], "timings": timings,
        "item_sha256": item_hashes, "detail_sha256": detail_hashes, "tolerances": TOLERANCES,
        "precision_decimal_digits": PRECISION, "stochastic_scientific_trajectories": 0,
        "python": sys.version, "numpy": np.__version__, "platform": platform.platform(),
    }
    atomic_write_json(root / "constraint-lab/reports/generation-008i-round-i0-tables.json", summary)
    return summary


def verify(root, commit):
    plan = require_execution(root, commit)
    summary = read_json(root / "constraint-lab/reports/generation-008i-round-i0-tables.json")
    if summary["status"] != "COMPLETE" or summary["plan_hash"] != plan["plan_hash"] or summary["primary_cells"] != 22:
        raise HistoryError("incomplete or mismatched I0 publication")
    for path, digest in {**summary["item_sha256"], **summary["detail_sha256"]}.items():
        if sha256_file(root / path) != digest:
            raise HistoryError(f"published file digest mismatch: {path}")
    for item in plan["items"]:
        path = root / "constraint-lab/reports/items/generation-008i" / (item["item_id"] + ".json")
        result = decode(_load_envelope(path, item, plan, commit)["result"])
        if item["kind"] == "equivalence":
            continue
        model = RoleController(item["feature"], Fraction(item["m"]))
        rows = model.kernel()
        if balance_gap(result["stationary_joint"], rows):
            raise HistoryError("independent full-state exact stationary balance failed")
        marginal = [sum(result["stationary_joint"][p * 6:(p + 1) * 6]) for p in range(64)]
        if marginal != result["material"]["pair_mask"]:
            raise HistoryError("stationary material projection mismatch")
        for key, vector in (("KU_kernel", result["KU_stationary_pair"]), ("K_pi", marginal)):
            kernel = [dict(row) for row in result[key]]
            if balance_gap(vector, kernel):
                raise HistoryError(f"{key} independent balance failed")
        if fingerprint(serial_rows(rows)) != result["catalog"]["full_kernel_fingerprint"]:
            raise HistoryError("published full kernel fingerprint mismatch")
        independently_decomposed = decomposition(marginal, [Fraction(1, 64)] * 64)
        if independently_decomposed != result["neutral_comparison"]:
            raise HistoryError("independent information decomposition mismatch")
    return {"status": "VERIFIED", "items": len(plan["items"]), "primary_cells": 22, "details": len(summary["detail_sha256"]), "plan_hash": plan["plan_hash"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("calibrate", "plan", "execute", "verify"))
    parser.add_argument("--frozen-plan-commit")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = repository_root()
    output = args.output or root / "constraint-lab/generated/generation-008i/round-i0"
    if args.command == "calibrate":
        print(calibrate(root))
    elif args.command == "plan":
        plan = write_plan(root)
        print({"plan_hash": plan["plan_hash"], "work_counts": plan["work_counts"]})
    elif args.command == "execute":
        result = execute(root, output, args.frozen_plan_commit)
        print({"status": result["status"], "primary_cells": result["primary_cells"]})
    else:
        print(verify(root, args.frozen_plan_commit))


if __name__ == "__main__":
    main()
