"""Frozen deterministic I0 execution for the predictive-state 8I variant."""

from __future__ import annotations

import argparse
import json
import re
import signal
import time
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

from rs_constraint_lab.coherence import canonical_ledger_bytes
from rs_constraint_lab.durable import atomic_write_json, canonical_json, read_json, sha256_bytes, sha256_file
from rs_constraint_lab.explore08 import FrozenPlanError, plan_hash, remote_contains, require_frozen_plan
from rs_constraint_lab.history import HistoryError, PRECISION, RecentReversal
from rs_constraint_lab.predictive_state import (
    CLOCK, PROJECTIONS, analyse_projection, balance_gap, commute, covariance, geometry, orbit_atlas,
)
from rs_constraint_lab.refinement import lumpability

BASE = "ad5b656e26fe66610b583aedccdd34593e13791a"
VERSION = "generation-008i-predictive-state/v1"
DIRECTORY = "constraint-lab/exploration/generation-008i"
PLAN = DIRECTORY + "/round-i0-plan.json"
CALIBRATION = DIRECTORY + "/calibration.json"
OUTPUT = "constraint-lab/reports/items/generation-008i-predictive"
MANIFEST = "constraint-lab/reports/generation-008i-predictive-round-i0-tables.json"
TABLE = "constraint-lab/reports/tables/generation-008i-predictive-"
GRADES = (("m025", "1/4"), ("m1", "1"), ("m4", "4"))
SHORT = dict(zip(PROJECTIONS, ("MASK", "CLASS", "COUNT", "PARITY")))
EXPECTED = {"non_neutral": dict(zip(PROJECTIONS, (384, 28, 12, 2))),
            "neutral": dict(zip(PROJECTIONS, (64, 11, 7, 2)))}
SOURCES = tuple("constraint-lab/src/rs_constraint_lab/" + name for name in (
    "refinement.py", "predictive_state.py", "gen008i_predictive_exec.py",
    "history.py", "graphs.py", "state.py", "exact.py", "memory_clocks.py",
    "durable.py", "explore08.py", "coherence.py",
))
INPUTS = (
    DIRECTORY + "/charter.md",
    "constraint-lab/provenance/prompts/008I-v0.8i-predictive-state-agent-input.md",
    "constraint-lab/reports/generation-008h-round-h0-tables.json",
)


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


def digest(value):
    return sha256_bytes(canonical_json(value).encode())


def items():
    return [{"item_id": f"I-REFINE-{SHORT[projection]}-{label}", "kind": "refine",
             "projection": projection, "grade": label, "m": m}
            for projection in PROJECTIONS for label, m in GRADES] + [
        {"item_id": "I-ORBIT-ATLAS", "kind": "orbits"},
        {"item_id": "I-SYNCHRONIZATION", "kind": "synchronization"},
        {"item_id": "I-QUOTIENT-COMMUTATION", "kind": "commutation"},
    ]


def validate_result(item, result):
    if item["kind"] != "refine":
        return
    target = EXPECTED["neutral" if Fraction(item["m"]) == 1 else "non_neutral"][item["projection"]]
    if result["stable_block_count"] != target:
        raise HistoryError("external count expectation differs: stop and diagnose without forcing partition")
    for name in ("strong_lumpability_gap", "full_stationary_gap", "quotient_stationary_gap",
                 "independent_route_membership_gap", "state_reordering_gap", "one_step_H0_gap"):
        if Fraction(result[name]):
            raise HistoryError(f"exact predictive check failed: {name}")
    if Decimal(result["temporal_information"]["formula_enumeration_gap"]) > Decimal("1e-25"):
        raise HistoryError("independent CMI identity exceeds frozen tolerance")
    if not result["distinct_next_observation_rows_within_current_observation"]:
        raise HistoryError("particular-process word-equivalence minimality not established")


def calibrate(root):
    if (root / PLAN).exists():
        raise HistoryError("neutral calibration must precede freeze")
    records = []
    for projection in PROJECTIONS:
        start = time.monotonic()
        result = analyse_projection(RecentReversal(Fraction(1)), projection)
        validate_result({"kind": "refine", "projection": projection, "m": "1"}, result)
        records.append({"projection": projection, "wall_seconds": time.monotonic() - start,
                        "result_bytes": len(canonical_json(result).encode()),
                        "initial_blocks": result["initial_block_count"],
                        "stable_blocks": result["stable_block_count"]})
    output = {
        "fixture": "neutral m=1 only", "measurements": records,
        "new_non_neutral_variant_target_executions": 0, "prior_related_non_neutral_exposure": True,
        "notes": "Prior role-grammar 8I and coarse-process 8J quotient/CMI/order results already known; not a blind round.",
    }
    atomic_write_json(root / CALIBRATION, output)
    return output


def write_plan(root):
    if (root / PLAN).exists():
        raise HistoryError("refusing to replace existing I0 plan")
    calibration = read_json(root / CALIBRATION)
    document = {
        "experiment_id": "generation-008i-predictive-state", "prompt_id": "008I",
        "prompt_variant": "predictive-state", "round_id": "I0", "mode": "A",
        "analysis_version": VERSION, "parent_commit": BASE, "clock": CLOCK,
        "ontology": {"N": 4, "O": 3, "G": 0, "S": 0, "L": 0, "H_pair": 1, "hypergraph": "independent"},
        "controller": "unchanged RECENT-REVERSAL", "grades": GRADES,
        "observation_chain": PROJECTIONS,
        "refinement_semantics": "coarsest strongly lumpable refinement on fixed recurrent states, preserving current observation; arbitrary augmented initial laws",
        "word_equivalence_scope": "not generally equated with strong lumpability; direct next-observation-row separation checked in this process",
        "synchronization": "shortest consecutive observation count determining the current stable block; neutral may need only one",
        "externally_predeclared_counts_not_algorithm_inputs": EXPECTED,
        "estimands": [
            "generic exact fixed point, all block memberships, chronology, sparse signatures, merge obstructions",
            "independent S4 and fixed-graph automorphism pair orbits, membership equivalence with non-neutral class refinement",
            "analytic (k,r) count quotient/formula/binomial stationary law versus generic refinement",
            "parity all-order deterministic alternation, checked through finite length six as plumbing",
            "stationary quotient pushforwards, exact one-step H0 equality at all four resolutions",
            "past/current/next triples from current state and independent two-forward-event enumeration",
            "160-digit temporal CMI versus independently aggregated quotient KL, and labelled event-MI formula",
            "positive-past first-order failures, exact two-observation synchronization and all-past order-two sufficiency",
            "deterministic and strong-lumpable arrows between consecutive stable partitions; stationary commutation",
            "block membership stability across non-neutral grades and reverse state enumeration",
        ],
        "items": items(),
        "work_counts": {
            "atomic_items": 15, "primary_projection_grade_items": 12, "cross_items": 3,
            "distinct_existing_kernels": 3, "recurrent_states": 384, "supported_transitions_per_kernel": 2304,
            "primary_refinement_runs_with_reverse_enumeration": 24,
            "current_state_triple_terms": 12 * 384 * 6,
            "independent_forward_triple_terms": 12 * 384 * 6 * 6,
            "S4_transition_comparisons": 3 * 24 * 384 * 6,
            "commuting_adjacent_arrows": 3 * 3,
            "initial_observation_counts": dict(zip(PROJECTIONS, (64, 11, 7, 2))),
            "worst_case_strict_split_rounds_per_item": "384 minus initial block count",
            "expected_same_observation_merge_certificates_non_neutral": 2 * (960 + 28 + 5),
        },
        "precision_decimal_digits": PRECISION,
        "tolerances": {"rational_identities": "exact", "partitions": "exact", "stationary_residual": "exact",
                       "one_step_H0_gap": "exact", "synchronization_and_sufficiency": "exact",
                       "information_formula_enumeration_gap": "1e-25"},
        "pre_freeze_exposure": {
            "new_non_neutral_variant_target_executions": 0, "blind_round": False,
            "prior_related_exposure": {
                "role_grammar_head": "6615c9f03a1fa30558f8cf519a125e610d393f31",
                "coarse_process_head": "64a4fe67e585e5be03f6afb2a0613e147c509b63",
                "known": "28 roles, SAME 12-state quotient, class-pair synchronization, SAME class/count CMI and order results",
            },
            "new_targets": "generic minimal-refinement fixed points, merge certificates, partition memberships and commutation",
            "allowed": ["neutral production plumbing", "small synthetic refinement", "structural graph audit", "user-predeclared analytic expectations"],
        },
        "engineering": {
            "workers": 1, "per_item_watchdog_seconds": 120, "disk_budget_bytes": 64_000_000,
            "neutral_total_seconds": sum(row["wall_seconds"] for row in calibration["measurements"]),
            "estimated_total_seconds": max(60, 30 * sum(row["wall_seconds"] for row in calibration["measurements"])),
            "resume": "retain only complete hash-valid matching frozen envelopes",
            "on_unexpected_count_or_budget": "stop and diagnose; no hidden changes to counts/tolerances/scope",
        },
        "source_sha256": {path: sha256_file(root / path) for path in SOURCES},
        "input_sha256": {path: sha256_file(root / path) for path in INPUTS},
        "calibration_sha256": sha256_file(root / CALIBRATION),
        "planning_coherence_sha256": sha256_bytes(canonical_ledger_bytes(root / "constraint-lab/coherence")),
    }
    document["plan_hash"] = plan_hash(document)
    atomic_write_json(root / PLAN, document)
    return document


def require_execution(root, commit):
    plan = require_frozen_plan(root, commit, PLAN, root / PLAN)
    if not remote_contains(root, commit):
        raise FrozenPlanError("I0 plan must be pushed before new non-neutral verification")
    if plan["analysis_version"] != VERSION:
        raise FrozenPlanError("predictive analysis version drift")
    for field in ("source_sha256", "input_sha256"):
        for path, value in plan[field].items():
            if sha256_file(root / path) != value:
                raise FrozenPlanError(f"frozen predictive artifact drift: {path}")
    if sha256_file(root / CALIBRATION) != plan["calibration_sha256"]:
        raise FrozenPlanError("calibration drift")
    return plan


def orbit_result():
    result = orbit_atlas()
    result["covariance"] = [covariance(RecentReversal(Fraction(m))) for _, m in GRADES]
    result["role_kernels"] = []
    blocks = geometry()[2]
    for grade, m in GRADES:
        quotient, gap = lumpability(RecentReversal(Fraction(m)).epoch_kernel(), blocks)
        pi = [Fraction(len(block), 384) for block in blocks]
        residual = balance_gap(pi, quotient)
        if gap or residual:
            raise HistoryError("S4 orbit law or stationary pushforward invalid")
        result["role_kernels"].append({"grade": grade, "m": Fraction(m), "rows": [sorted(row.items()) for row in quotient],
                                       "stationary_mass": pi, "strong_lumpability_gap": gap, "stationary_gap": residual})
    return result


def sync_result(primary, atlas):
    pair_roles = {(row["predecessor_class"], row["graph_class"]): row for row in atlas["orbit_atlas"]}
    records = []
    for (grade, projection), result in sorted(primary.items()):
        record = dict(result["synchronization"], grade=grade, m=result["m"], clock=CLOCK)
        if projection == "graph_class":
            for pair in record["ordered_pair_atlas"]:
                role = pair_roles[pair["previous"], pair["current"]]
                pair.update(history_orbit_id=role["history_orbit_id"], present=role["present"])
                if Fraction(pair["stationary_probability"]) != Fraction(role["stationary_mass"]):
                    raise HistoryError("class-pair/orbit stationary mass mismatch")
        elif projection == "edge_count":
            for pair in record["ordered_pair_atlas"]:
                pair["r"] = int(pair["current"] > pair["previous"])
        records.append(record)
    for projection in PROJECTIONS:
        if primary["m025", projection]["stable_blocks"] != primary["m4", projection]["stable_blocks"]:
            raise HistoryError("non-neutral partition memberships differ across grades")
    parity_words = [{"length": length, "word": [initial ^ (t % 2) for t in range(length)], "stationary_probability": Fraction(1, 2)}
                    for length in range(1, 7) for initial in (0, 1)]
    return {"clock": CLOCK, "records": records, "non_neutral_membership_equal": True,
            "parity_all_order_proof": "R_t=R_0 xor (t mod 2), independent of m/history given initial parity",
            "parity_finite_null_words": parity_words}


def load_envelope(root, item, plan, commit):
    value = read_json(root / OUTPUT / (item["item_id"] + ".json"))
    if value["item"] != item or value["plan_hash"] != plan["plan_hash"] or value["frozen_analysis_plan_commit"] != commit:
        raise HistoryError("cached item freeze mismatch")
    if value["analysis_version"] != VERSION or value["result_sha256"] != digest(value["result"]):
        raise HistoryError("cached item content hash mismatch")
    validate_result(item, value["result"])
    return value


def publish(root, envelopes, plan, commit):
    primary = [e for e in envelopes if e["item"]["kind"] == "refine"]
    summary_rows, info, triples = [], [], []
    for envelope in primary:
        r = envelope["result"]
        common = {"projection": r["projection"], "m": r["m"], "clock": CLOCK}
        summary_rows.append(dict(common, **{key: r[key] for key in (
            "initial_block_count", "stable_block_count", "refinement_rounds", "strong_lumpability_verified",
            "initial_strong_lumpability", "one_step_H0_gap", "distinct_next_observation_rows_within_current_observation")}))
        info.append(dict(common, **r["temporal_information"]))
        triples.append(dict(common, triples=r["stationary_triples"]))
    tables = {"refinement-summary": summary_rows, "temporal-information": info, "stationary-triples": triples}
    for envelope in envelopes:
        if envelope["item"]["kind"] != "refine":
            tables[envelope["item"]["kind"]] = envelope["result"]
    hashes = {}
    for name, value in tables.items():
        path = TABLE + name + ".json"
        atomic_write_json(root / path, {"clock": CLOCK, "data": value})
        hashes[path] = sha256_file(root / path)
    files = {OUTPUT + "/" + e["item"]["item_id"] + ".json": sha256_file(root / OUTPUT / (e["item"]["item_id"] + ".json")) for e in envelopes}
    summary = {
        "experiment_id": "generation-008i-predictive-state", "prompt_variant": "predictive-state", "round_id": "I0",
        "analysis_version": VERSION, "clock": CLOCK, "status": "COMPLETE", "frozen_analysis_plan_commit": commit,
        "plan_hash": plan["plan_hash"], "plan_file_sha256": sha256_file(root / PLAN),
        "item_sha256": files, "table_sha256": hashes,
        "timings": {e["item"]["item_id"]: e["wall_seconds"] for e in envelopes},
        "primary_items": 12, "cross_items": 3, "stochastic_scientific_trajectories": 0,
        "precision_decimal_digits": PRECISION, "new_targets_unopened_before_freeze": True,
        "prior_related_exposure": True, "blind_round": False,
    }
    atomic_write_json(root / MANIFEST, summary)
    return summary


def execute(root, commit):
    plan = require_execution(root, commit)
    primary, envelopes, atlas = {}, [], None
    output = root / OUTPUT
    output.mkdir(parents=True, exist_ok=True)

    def alarm(signum, frame):
        raise TimeoutError("I0 predictive item watchdog: stop, preserve earlier valid items and diagnose")

    previous = signal.signal(signal.SIGALRM, alarm)
    try:
        for position, item in enumerate(plan["items"]):
            path = output / (item["item_id"] + ".json")
            if path.exists():
                envelope = load_envelope(root, item, plan, commit)
            else:
                atomic_write_json(root / DIRECTORY / "status.json", {"status": "RUNNING", "item": item["item_id"], "completed": position, "total": 15})
                start = time.monotonic()
                signal.alarm(plan["engineering"]["per_item_watchdog_seconds"])
                if item["kind"] == "refine":
                    result = analyse_projection(RecentReversal(Fraction(item["m"])), item["projection"])
                elif item["kind"] == "orbits":
                    result = orbit_result()
                elif item["kind"] == "synchronization":
                    result = sync_result(primary, atlas)
                else:
                    result = {"clock": CLOCK, "arrows": commute(primary)}
                validate_result(item, result)
                signal.alarm(0)
                envelope = {"item": item, "analysis_version": VERSION, "plan_hash": plan["plan_hash"],
                            "frozen_analysis_plan_commit": commit, "result": result, "result_sha256": digest(result),
                            "wall_seconds": time.monotonic() - start}
                atomic_write_json(path, envelope)
                envelope = read_json(path)
            result = decode(envelope["result"])
            if item["kind"] == "refine":
                primary[item["grade"], item["projection"]] = result
            elif item["kind"] == "orbits":
                atlas = result
            envelopes.append(envelope)
            if sum(p.stat().st_size for p in output.iterdir()) > plan["engineering"]["disk_budget_bytes"]:
                raise HistoryError("predictive publication exceeds frozen disk budget")
            print("COMPLETE", item["item_id"], f"{envelope['wall_seconds']:.3f}s", flush=True)
        summary = publish(root, envelopes, plan, commit)
        atomic_write_json(root / DIRECTORY / "status.json", {"status": "COMPLETE", "completed": 15})
        return summary
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)


def verify(root, commit):
    plan = require_execution(root, commit)
    summary = read_json(root / MANIFEST)
    if summary["status"] != "COMPLETE" or summary["plan_hash"] != plan["plan_hash"]:
        raise HistoryError("incomplete or mismatched publication")
    for path, value in {**summary["item_sha256"], **summary["table_sha256"]}.items():
        if sha256_file(root / path) != value:
            raise HistoryError(f"published digest mismatch: {path}")
    primary = {}
    for item in plan["items"]:
        envelope = load_envelope(root, item, plan, commit)
        r = decode(envelope["result"])
        if item["kind"] == "refine":
            rows = RecentReversal(Fraction(item["m"])).epoch_kernel()
            q, gap = lumpability(rows, r["stable_blocks"])
            if gap or [sorted(row.items()) for row in q] != [list(map(tuple, row)) for row in r["quotient_kernel"]]:
                raise HistoryError("independent quotient certificate replay failed")
            if sum(r["stationary_mass"]) != 1 or balance_gap(r["stationary_mass"], q):
                raise HistoryError("independent stationary replay failed")
            if sum(row["probability"] for row in r["stationary_triples"]) != 1:
                raise HistoryError("triple table normalisation failed")
            primary[item["grade"], item["projection"]] = r
    if commute(primary) != decode(read_json(root / (TABLE + "commutation.json")))["data"]["arrows"]:
        raise HistoryError("independent quotient reassembly mismatch")
    return {"status": "VERIFIED", "primary_items": 12, "cross_items": 3, "plan_hash": plan["plan_hash"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("calibrate", "plan", "execute", "verify"))
    parser.add_argument("--frozen-plan-commit")
    args = parser.parse_args()
    root = repository_root()
    if args.command == "calibrate":
        result = calibrate(root)
    elif args.command == "plan":
        result = write_plan(root)
    elif args.command == "execute":
        result = execute(root, args.frozen_plan_commit)
    else:
        result = verify(root, args.frozen_plan_commit)
    print(json.dumps(result, default=str, sort_keys=True))


if __name__ == "__main__":
    main()
