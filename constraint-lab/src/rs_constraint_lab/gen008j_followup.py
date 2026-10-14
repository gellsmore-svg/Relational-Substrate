"""Separately frozen J1 projection mechanisms, selected after complete J0."""

from __future__ import annotations

import argparse
import json
import time
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

from rs_constraint_lab.coarse_process import (
    CLOCK, ORIENTATION, ObservedChain, chains_for, edge_chain, published_models, sparse_words,
)
from rs_constraint_lab.durable import atomic_write_json, canonical_json, read_json, sha256_bytes, sha256_file
from rs_constraint_lab.explore08 import FrozenPlanError, plan_hash, remote_contains, require_frozen_plan
from rs_constraint_lab.gen008j_exec import BASE, MANIFEST, OUTPUT, load_word_file, repository_root
from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.history import HistoryError
from rs_constraint_lab.history_roles import aggregate_quotient, role_orbits

VERSION = "generation-008j-projection-mechanisms/v1"
PLAN = "constraint-lab/exploration/generation-008j/round-j1-plan.json"
SUMMARY = "constraint-lab/reports/generation-008j-round-j1-tables.json"
ITEMS = ("J1-CLASS-PAIR-ROLE", "J1-SAME-EDGE-ROLE")


def partition_labels(labels):
    keys = tuple(sorted(set(labels)))
    groups = tuple(tuple(i for i, label in enumerate(labels) if label == key) for key in keys)
    return keys, groups, tuple(keys.index(label) for label in labels)


def reconstruction_record(groups, state_pairs):
    pairs = []
    constant = True
    for group in groups:
        values = {state_pairs[state] for state in group}
        constant &= len(values) == 1
        pairs.append(tuple(sorted(values)))
    buckets = defaultdict(list)
    for orbit, values in enumerate(pairs):
        if len(values) == 1:
            buckets[values[0]].append(orbit)
    collisions = [{"class_pair": key, "role_orbits": members}
                  for key, members in sorted(buckets.items()) if len(members) > 1]
    return {"constant_on_orbits": constant, "role_orbit_count": len(groups),
            "class_pair_count": len(buckets), "collisions": collisions,
            "bijection": constant and not collisions and len(buckets) == len(groups),
            "role_to_class_pair": [values[0] if len(values) == 1 else None for values in pairs]}


def same_edge_formula(feature, multiplier, count, remembered_present, slots=6):
    m, k, r = Fraction(multiplier), count, remembered_present
    if feature not in ("SAME_ANY", "SAME_FORM", "SAME_DISSOLVE"):
        raise HistoryError("formula scoped to SAME features")
    if r not in (0, 1) or not 0 <= k <= slots or k < r or k > slots - 1 + r:
        raise HistoryError("infeasible remembered-bit/count role")
    formation = Fraction(slots - k)
    dissolution = Fraction(k)
    if feature in ("SAME_ANY", "SAME_FORM"):
        formation += (m - 1) * (1 - r)
    if feature in ("SAME_ANY", "SAME_DISSOLVE"):
        dissolution += (m - 1) * r
    total = formation + dissolution
    row = {}
    if formation:
        row[k + 1, 1] = formation / total
    if dissolution:
        row[k - 1, 0] = dissolution / total
    return row


def class_pair_probe(root):
    structure, table = role_orbits(), pair_classes()
    state_pairs = tuple((table.name_of[p ^ (1 << h)], table.name_of[p]) for p in range(64) for h in range(6))
    result = reconstruction_record(structure.members, state_pairs)
    result.update(clock=CLOCK, orientation=ORIENTATION, item_id=ITEMS[0], systems=[])
    if not result["bijection"]:
        return result
    pairs = result["role_to_class_pair"]
    for key, model in sorted(published_models(root).items()):
        h, _, _ = chains_for(model)
        compiled = []
        for source, row in enumerate(h.rows):
            projected = defaultdict(Fraction)
            for target, value in row.items():
                projected[h.observations[target]] += value
            compiled.append(projected)
        # Independently condition the published J0 triples on each class pair.
        envelope = read_json(root / OUTPUT / (key.replace("I0-", "J0-") + ".json"))
        triples = envelope["result"]["triples"]["graph_class"]
        normalisers, conditional = defaultdict(Fraction), defaultdict(lambda: defaultdict(Fraction))
        for row in triples:
            a, b, c = row["word"]
            mass = Fraction(row["P_H"])
            normalisers[a, b] += mass
            conditional[a, b][c] += mass
        gap = Fraction(0)
        for orbit, pair in enumerate(pairs):
            normaliser = normalisers[pair]
            if normaliser <= 0:
                raise HistoryError("class-pair witness must have positive stationary probability")
            for target in set(compiled[orbit]) | set(conditional[pair]):
                gap = max(gap, abs(compiled[orbit].get(target, 0) - conditional[pair].get(target, 0) / normaliser))
        if gap:
            raise HistoryError("reconstructed role/class triple law mismatch")
        result["systems"].append({
            "controller_id": key, "compiled_class_rows": [sorted(row.items()) for row in compiled],
            "triple_conditional_gap": gap, "positive_class_pairs": len(normalisers),
            "order1_gap": envelope["result"]["diagnostics"]["H"]["finite_depth"]["graph_class"][0]["conditional_row_gap"],
            "projected_class_order": 1 if Fraction(envelope["result"]["diagnostics"]["H"]["finite_depth"]["graph_class"][0]["conditional_row_gap"]) == 0 else 2,
        })
    return result


def edge_role_probe(root):
    structure = role_orbits()
    labels = tuple((group[0] // 6).bit_count() for group in structure.members)
    remembered = tuple(((group[0] // 6) >> (group[0] % 6)) & 1 for group in structure.members)
    keys, groups, group_of = partition_labels(tuple(zip(labels, remembered)))
    result = {"clock": CLOCK, "orientation": ORIENTATION, "item_id": ITEMS[1],
              "edge_role_count": len(keys), "roles": keys, "systems": []}
    for key, model in sorted(published_models(root).items()):
        h, _, _ = chains_for(model)
        quotient, gap = aggregate_quotient(h.rows, groups, group_of)
        record = {"controller_id": key, "edge_role_lumpability_gap": gap, "strongly_lumpable": gap == 0}
        feature = model.get("feature")
        if key == "I0-NEUTRAL":
            feature = "SAME_ANY"
        if feature in ("SAME_ANY", "SAME_FORM", "SAME_DISSOLVE"):
            m = Fraction(model["m"])
            formula_gap = Fraction(0)
            for source, row in enumerate(quotient):
                expected = same_edge_formula(feature, m, *keys[source])
                actual = {keys[target]: value for target, value in row.items()}
                formula_gap = max(formula_gap, max(abs(expected.get(target, 0) - actual.get(target, 0))
                                                    for target in expected.keys() | actual.keys()))
            pi = tuple(sum(h.pi[state] for state in group) for group in groups)
            reduced = ObservedChain(quotient, pi, tuple(k for k, r in keys))
            words, _ = sparse_words(reduced)
            envelope = read_json(root / OUTPUT / (key.replace("I0-", "J0-") + ".json"))
            original = load_word_file(root, envelope)
            word_gap = Fraction(0)
            for block in original["words"]:
                if block["projection"] != "edge_count":
                    continue
                actual = {tuple(row["word"]): Fraction(row["P_H"]) for row in block["rows"]}
                law = words[block["word_length"]]
                word_gap = max(word_gap, max(abs(actual.get(word, 0) - law.get(word, 0))
                                             for word in actual.keys() | law.keys()))
            if gap or formula_gap or word_gap:
                raise HistoryError("SAME reduced edge-role identity failed")
            record.update(formula_gap=formula_gap, J0_word_gap=word_gap,
                          quotient_rows=[sorted(row.items()) for row in quotient], stationary_role=pi)
        result["systems"].append(record)
    return result


def write_plan(root):
    if (root / PLAN).exists():
        raise HistoryError("refusing to replace J1 plan")
    j0 = read_json(root / MANIFEST)
    inputs = [
        "constraint-lab/exploration/generation-008j/open-thetical-decision.md",
        MANIFEST, *j0["item_sha256"], *j0["table_sha256"],
        "constraint-lab/reports/tables/generation-008i-controller-catalog.json",
        "constraint-lab/reports/tables/generation-008i-kernels.json",
        "constraint-lab/reports/tables/generation-008i-stationary-distributions.json",
        "constraint-lab/reports/tables/generation-008i-neutral.json",
    ]
    sources = [
        "constraint-lab/src/rs_constraint_lab/gen008j_followup.py",
        *read_json(root / "constraint-lab/exploration/generation-008j/round-j0-plan.json")["source_sha256"],
    ]
    plan = {
        "round_id": "J1", "analysis_version": VERSION, "clock": CLOCK, "orientation": ORIENTATION,
        "parent_reviewed_commit": BASE, "decision_commit": "3998b4f",
        "items": ITEMS, "new_controllers": 0, "new_grades": 0, "new_stationary_solves": 0,
        "new_word_lengths": 0, "stochastic_scientific_trajectories": 0,
        "pre_freeze_exposure": {"J0_inputs_preobserved": True, "new_J1_target_checks": 0,
                               "symbolic_candidates": "post-J0 class-pair bijection and SAME (k,R) counting; pre-J0 generic SAME simplification already declared"},
        "estimands": [
            "384 states: class pair constant/injective on 28 S4 roles; preserve collisions if present",
            "all 23 role laws compiled to class-pair rows and checked against J0 stationary triples",
            "all 23 exact (k,R) role block gaps; retain ADJ/DISJ boundaries",
            "seven SAME/neutral reduced-role laws versus symbolic count formula and J0 edge words L1..6",
        ],
        "work_counts": {"atomic_items": 2, "augmented_state_pair_labels": 384,
                        "role_states_per_system": 28, "class_row_systems": 23, "edge_block_systems": 23,
                        "SAME_formula_systems": 7, "SAME_formula_rows": 7 * 12,
                        "reused_word_lengths": [1, 2, 3, 4, 5, 6]},
        "candidate_formula": {
            "F": "6-k + (m-1)*(1-R) for SAME_ANY/FORM; otherwise 6-k",
            "D": "k + (m-1)*R for SAME_ANY/DISSOLVE; otherwise k",
            "transition": "(k,R)->(k+1,1) with F/(F+D), (k-1,0) with D/(F+D)",
            "scope": "positive m, feasible remembered bit/count, no new controller"},
        "tolerances": {"rational_identities": "exact", "word_comparison": "exact"},
        "engineering": {"workers": 1, "estimated_seconds": 5, "per_item_budget_seconds": 120, "disk_budget_bytes": 5_000_000},
        "source_sha256": {path: sha256_file(root / path) for path in sources},
        "input_sha256": {path: sha256_file(root / path) for path in inputs},
    }
    plan["plan_hash"] = plan_hash(plan)
    atomic_write_json(root / PLAN, plan)
    return plan


def require_execution(root, commit):
    plan = require_frozen_plan(root, commit, PLAN, root / PLAN)
    if not remote_contains(root, commit):
        raise FrozenPlanError("J1 plan must be pushed")
    if plan["analysis_version"] != VERSION:
        raise FrozenPlanError("J1 analysis version drift")
    for field in ("source_sha256", "input_sha256"):
        for path, value in plan[field].items():
            if sha256_file(root / path) != value:
                raise FrozenPlanError(f"J1 frozen artifact drift: {path}")
    return plan


def execute(root, commit):
    plan = require_execution(root, commit)
    hashes, times = {}, {}
    for item, function in zip(ITEMS, (class_pair_probe, edge_role_probe)):
        path = root / "constraint-lab/reports/items/generation-008j-j1" / (item + ".json")
        started = time.monotonic()
        if path.exists():
            value = read_json(path)
            if value["plan_hash"] != plan["plan_hash"] or value["result_sha256"] != sha256_bytes(canonical_json(value["result"]).encode()):
                raise HistoryError("invalid resumed J1 item")
        else:
            result = function(root)
            value = {"item_id": item, "clock": CLOCK, "frozen_analysis_plan_commit": commit,
                     "plan_hash": plan["plan_hash"], "result": result,
                     "result_sha256": sha256_bytes(canonical_json(result).encode()),
                     "wall_seconds": time.monotonic() - started}
            atomic_write_json(path, value)
        if value["wall_seconds"] > plan["engineering"]["per_item_budget_seconds"]:
            raise HistoryError("J1 budget overrun: preserve result and amend before continuing")
        hashes[str(path.relative_to(root))] = sha256_file(path)
        times[item] = value["wall_seconds"]
    result = {"round_id": "J1", "status": "COMPLETE", "clock": CLOCK,
              "frozen_analysis_plan_commit": commit, "plan_hash": plan["plan_hash"],
              "plan_file_sha256": sha256_file(root / PLAN), "item_sha256": hashes,
              "timings": times, "new_stationary_solves": 0, "new_controllers": 0, "new_word_lengths": 0}
    atomic_write_json(root / SUMMARY, result)
    return result


def verify(root, commit):
    plan = require_execution(root, commit)
    summary = read_json(root / SUMMARY)
    if summary["plan_hash"] != plan["plan_hash"] or summary["status"] != "COMPLETE":
        raise HistoryError("J1 summary mismatch")
    for path, value in summary["item_sha256"].items():
        if sha256_file(root / path) != value:
            raise HistoryError("J1 item digest mismatch")
        item = read_json(root / path)
        if item["result_sha256"] != sha256_bytes(canonical_json(item["result"]).encode()):
            raise HistoryError("J1 result mismatch")
    return {"status": "VERIFIED", "items": 2, "plan_hash": plan["plan_hash"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("plan", "execute", "verify"))
    parser.add_argument("--frozen-plan-commit")
    args = parser.parse_args()
    root = repository_root()
    if args.command == "plan":
        result = write_plan(root)
    elif args.command == "execute":
        result = execute(root, args.frozen_plan_commit)
    else:
        result = verify(root, args.frozen_plan_commit)
    print(json.dumps(result, default=str, sort_keys=True))


if __name__ == "__main__":
    main()
