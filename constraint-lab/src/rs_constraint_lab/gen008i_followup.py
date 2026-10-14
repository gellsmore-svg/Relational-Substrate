"""Two separately frozen I1 mechanism probes selected after the complete I0 atlas."""

from __future__ import annotations

import argparse
from decimal import Decimal
from fractions import Fraction
from math import factorial
from pathlib import Path
import signal
import time

from rs_constraint_lab.durable import atomic_write_json, read_json, sha256_file
from rs_constraint_lab.explore08 import FrozenPlanError, plan_hash, remote_contains, require_frozen_plan
from rs_constraint_lab.gen008i_exec import decode, require_execution as require_i0, repository_root
from rs_constraint_lab.history import HistoryError
from rs_constraint_lab.history_roles import RoleController, slot_relation
from rs_constraint_lab.role_atlas import balance_gap, decomposition, fingerprint

PLAN = "constraint-lab/exploration/generation-008i/round-i1-plan.json"
I0_COMMIT = "035601e215bf6f0c4621d818ffa22b713d0b5d67"
I0_RESULT_COMMIT = "2b001561abba3e21bc6489bcfdca1249b31519aa"
VERSION = "generation-008i-I1-mechanisms/v1"
FEATURES = ("SAME_FORM", "SAME_DISSOLVE", "DISJ_FORM", "DISJ_DISSOLVE")
GRADES = (("m025", "1/4"), ("m4", "4"))
ITEMS = ("I1-COORDINATE-SYMMETRY", "I1-SINGLETON-MATCHED-KU")


def permute_bits(mask, permutation):
    return sum(1 << permutation[e] for e in range(len(permutation)) if mask & (1 << e))


def slot_generators(slots):
    result = []
    for index in range(slots - 1):
        permutation = list(range(slots))
        permutation[index], permutation[index + 1] = permutation[index + 1], permutation[index]
        result.append(tuple(permutation))
    return result


def generated_group_size(slots):
    known = {tuple(range(slots))}
    queue = list(known)
    for permutation in queue:
        for generator in slot_generators(slots):
            image = tuple(generator[e] for e in permutation)
            if image not in known:
                known.add(image)
                queue.append(image)
    return len(known)


def candidate_same_stationary(model):
    if model.feature.relation != "SAME" or model.feature.direction is None:
        raise HistoryError("stationary factorisation is scoped to SAME x direction")
    slots = model.slots
    r = (model.multiplier + slots - 1) / (model.multiplier + 2 * slots - 1)
    if model.feature.direction == "DISSOLVE":
        r = 1 - r
    pi = []
    for p in range(1 << slots):
        for h in range(slots):
            other_present = p.bit_count() - int(bool(p & (1 << h)))
            pi.append(Fraction(1, 2 * slots) * r**other_present * (1 - r)**(slots - 1 - other_present))
    return r, pi


def coordinate_case(model, published_pi):
    rows = model.kernel()
    slots = model.slots
    gap, joint_gap, witness = Fraction(0), Fraction(0), None
    for mapping in slot_generators(slots):
        mask_map = [permute_bits(p, mapping) for p in range(1 << slots)]
        for source, row in enumerate(rows):
            image_source = mask_map[source // slots] * slots + mapping[source % slots]
            joint_gap = max(joint_gap, abs(published_pi[source] - published_pi[image_source]))
            for target, value in row.items():
                image_target = mask_map[target // slots] * slots + mapping[target % slots]
                image_value = rows[image_source].get(image_target, 0)
                difference = abs(value - image_value)
                gap = max(gap, difference)
                if difference and witness is None:
                    witness = {"generator": mapping, "source": source, "target": target, "probability": value, "mapped_probability": image_value}
    material = [sum(published_pi[p * slots:(p + 1) * slots]) for p in range(1 << slots)]
    layer_gap = max(
        max(material[p] for p in range(1 << slots) if p.bit_count() == k) -
        min(material[p] for p in range(1 << slots) if p.bit_count() == k)
        for k in range(slots + 1)
    )
    result = {
        "feature": model.feature_name, "m": model.multiplier, "generator_kernel_gap": gap,
        "generator_stationary_gap": joint_gap, "generator_witness": witness,
        "within_edge_layer_material_gap": layer_gap,
        "kernel_comparisons": (slots - 1) * len(rows) * slots,
    }
    if model.feature.relation == "SAME":
        r, candidate = candidate_same_stationary(model)
        result.update({
            "other_bit_probability": r, "candidate_normalisation_gap": abs(sum(candidate) - 1),
            "candidate_stationary_balance_gap": balance_gap(candidate, rows),
            "candidate_vs_I0_gap": max(abs(a - b) for a, b in zip(candidate, published_pi)),
        })
    return result


def load_inputs(root):
    results = {}
    for feature in FEATURES:
        for label, m in GRADES:
            path = root / "constraint-lab/reports/items/generation-008i" / f"I0-{feature}-{label}.json"
            results[feature, Fraction(m)] = decode(read_json(path)["result"])
    return results


def singleton_pair(same, disjoint, m):
    direction = same["catalog"]["feature"].split("_", 1)[1]
    models = (RoleController("SAME_" + direction, m), RoleController("DISJ_" + direction, m))
    opposite = [next(e for e in range(6) if slot_relation(4, e, h) == "DISJOINT") for h in range(6)]
    row_bijection_gap = max(
        abs(models[1].pair_probabilities(p, h)[e] - models[0].pair_probabilities(p, opposite[h])[e])
        for p in range(64) for h in range(6) for e in range(6)
    )
    ku = [[dict(row) for row in result["KU_kernel"]] for result in (same, disjoint)]
    kpi = [[dict(row) for row in result["K_pi"]] for result in (same, disjoint)]
    ku_gap = max(abs(ku[0][p][p ^ (1 << e)] - ku[1][p][p ^ (1 << e)]) for p in range(64) for e in range(6))
    identity_gap = Fraction(0)
    deltas = []
    for model, result, averaged, experienced in zip(models, (same, disjoint), ku, kpi):
        table = []
        for p in range(64):
            row = []
            for e in range(6):
                target = p ^ (1 << e)
                delta = sum(
                    (result["stationary_joint"][p * 6 + h] / result["material"]["pair_mask"][p] - Fraction(1, 6))
                    * model.pair_probabilities(p, h)[e] for h in range(6)
                )
                identity_gap = max(identity_gap, abs(delta - experienced[p][target] + averaged[p][target]))
                row.append(delta)
            table.append(row)
        deltas.append(table)
    matched_gap = max(
        abs(kpi[0][p][p ^ (1 << e)] - kpi[1][p][p ^ (1 << e)] - deltas[0][p][e] + deltas[1][p][e])
        for p in range(64) for e in range(6)
    )
    material_left, material_right = (result["material"]["pair_mask"] for result in (same, disjoint))
    return {
        "direction": direction, "m": m, "history_slot_bijection": opposite,
        "row_history_bijection_gap": row_bijection_gap, "matched_KU_gap": ku_gap,
        "conditional_feedback_identity_gap": identity_gap, "matched_experienced_kernel_identity_gap": matched_gap,
        "stationary_material_comparison": decomposition(material_left, material_right),
        "stationary_pair_max_gap": max(abs(a - b) for a, b in zip(material_left, material_right)),
        "Kpi_row_max_gap": max(abs(kpi[0][p][p ^ (1 << e)] - kpi[1][p][p ^ (1 << e)]) for p in range(64) for e in range(6)),
        "same_feedback_rows": deltas[0], "disjoint_feedback_rows": deltas[1],
        "scope": "same declared uniform-history comparator; not all possible current-state representations",
    }


def prepare_plan():
    document = {
        "round_id": "I1", "analysis_version": VERSION, "method": "OTR recursive mechanism probes after complete I0",
        "I0_frozen_commit": I0_COMMIT, "I0_result_commit": I0_RESULT_COMMIT,
        "decision_path": "constraint-lab/exploration/generation-008i/open-thetical-decision.md",
        "decision_commit": "8688e86af6c0412381a0e3130547b3e181f496ea", "items": list(ITEMS),
        "inputs": "eight already observed SAME/DISJ direction x grade I0 cells; no new stationary solve",
        "probe1": {
            "target": "SAME coordinate symmetry and stationary factorisation, DISJ boundary",
            "features": list(FEATURES), "grades": list(GRADES),
            "generators": slot_generators(6), "group_closure_expected": factorial(6),
            "candidate": "SAME_FORM: h uniform; p_h uniform bit; other bits iid r=(m+5)/(m+11); DISSOLVE complement",
            "estimands": "exact generator kernel/joint invariance, within-edge material uniformity, formula normalisation/balance/I0 agreement; retain DISJ counterexamples",
        },
        "probe2": {
            "target": "SAME/DISJ matched-KU feedback for both directions and grades",
            "estimands": "row bijection h->opposite(h), identical KU, paired material JS edge/shape/label decomposition, Kpi-KU conditional-history identity",
        },
        "exposure": {
            "I0_inputs": "fully observed and declared; probes selected post-I0",
            "new_I1_non_neutral_checks_or_contrasts_before_freeze": 0,
            "analytic_expectations": "post-I0 symbolic expectations in the decision; exact target verification unopened",
            "allowed_fixtures": "neutral or smaller synthetic SAME x direction only",
        },
        "arithmetic": "exact Fraction identities, 160-digit information, no Monte Carlo",
        "tolerances": {"rational_gaps": "exact", "information_chain_gap": "1e-25"},
        "work_counts": {
            "atomic_items": 2, "reused_I0_cells": 8, "new_stationary_solves": 0,
            "symmetry_generator_kernel_comparisons": 8 * 5 * 384 * 6,
            "symmetry_generator_joint_comparisons": 8 * 5 * 384,
            "candidate_stationary_laws": 4, "matched_pairs": 4, "history_bijection_slot_comparisons": 4 * 64 * 6 * 6,
        },
        "execution": {"workers": 1, "item_watchdog_seconds": 120, "expected_wall_seconds": 30, "disk_budget_bytes": 5_000_000},
        "non_claims": "No new controller family/grade, H2, L, N5, causality score, irreducible history or physical ontology claim.",
    }
    document["plan_hash"] = plan_hash(document)
    return document


def write_plan(root):
    plan = prepare_plan()
    sources = ("gen008i_followup.py", "gen008i_exec.py", "history_roles.py", "role_atlas.py", "history.py", "durable.py", "exact.py")
    plan["source_sha256"] = {"constraint-lab/src/rs_constraint_lab/" + path: sha256_file(root / "constraint-lab/src/rs_constraint_lab" / path) for path in sources}
    paths = [
        "constraint-lab/reports/generation-008i-round-i0-tables.json",
        "constraint-lab/exploration/generation-008i/open-thetical-decision.md",
    ] + [f"constraint-lab/reports/items/generation-008i/I0-{feature}-{label}.json" for feature in FEATURES for label, _ in GRADES]
    plan["input_sha256"] = {path: sha256_file(root / path) for path in paths}
    plan["plan_hash"] = plan_hash(plan)
    atomic_write_json(root / PLAN, plan)
    return plan


def require_execution(root, commit):
    plan = require_frozen_plan(root, commit, PLAN, disk_path=root / PLAN)
    if not remote_contains(root, commit or ""):
        raise FrozenPlanError("I1 plan must be pushed")
    require_i0(root, I0_COMMIT)
    for field in ("source_sha256", "input_sha256"):
        for path, digest in plan[field].items():
            if sha256_file(root / path) != digest:
                raise FrozenPlanError(f"I1 input/source drift: {path}")
    return plan


def validate(item, result):
    if item == ITEMS[0]:
        if result["generated_group_size"] != 720:
            raise HistoryError("slot generators do not generate S6")
        for row in result["cases"]:
            if row["feature"].startswith("SAME"):
                for field in ("generator_kernel_gap", "generator_stationary_gap", "within_edge_layer_material_gap", "candidate_normalisation_gap", "candidate_stationary_balance_gap", "candidate_vs_I0_gap"):
                    if Fraction(row[field]):
                        raise HistoryError(f"SAME mechanism identity failed: {field}")
    else:
        for row in result["pairs"]:
            for field in ("row_history_bijection_gap", "matched_KU_gap", "conditional_feedback_identity_gap", "matched_experienced_kernel_identity_gap"):
                if Fraction(row[field]):
                    raise HistoryError(f"singleton comparator identity failed: {field}")
            if abs(Decimal(row["stationary_material_comparison"]["chain_gap"])) > Decimal("1e-25"):
                raise HistoryError("I1 information chain gap")


def execute(root, commit):
    plan = require_execution(root, commit)
    inputs = load_inputs(root)
    hashes = {}
    for item in plan["items"]:
        path = root / "constraint-lab/reports/items/generation-008i-i1" / (item + ".json")
        print(f"[I1] active {item}", flush=True)
        if path.exists():
            envelope = read_json(path)
            if envelope["plan_hash"] != plan["plan_hash"] or envelope.get("frozen_analysis_plan_commit") != commit or envelope.get("analysis_version") != VERSION or envelope.get("item_id") != item or fingerprint(envelope["result"]) != envelope["result_sha256"]:
                raise HistoryError("I1 cached payload identity mismatch")
            validate(item, decode(envelope["result"]))
        else:
            started = time.monotonic()
            def timeout_handler(*_args):
                raise TimeoutError("I1 item watchdog; completed item retained")
            previous = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(plan["execution"]["item_watchdog_seconds"])
            try:
                if item == ITEMS[0]:
                    result = {
                        "generated_group_size": generated_group_size(6), "slot_generators": slot_generators(6),
                        "cases": [coordinate_case(RoleController(feature, m), row["stationary_joint"]) for (feature, m), row in inputs.items()],
                    }
                else:
                    result = {"pairs": [singleton_pair(inputs["SAME_" + direction, Fraction(m)], inputs["DISJ_" + direction, Fraction(m)], Fraction(m)) for direction in ("FORM", "DISSOLVE") for _, m in GRADES]}
                validate(item, result)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, previous)
            envelope = {
                "item_id": item, "plan_hash": plan["plan_hash"], "frozen_analysis_plan_commit": commit,
                "analysis_version": VERSION, "wall_seconds": time.monotonic() - started,
                "result_sha256": fingerprint(result), "result": result,
            }
            atomic_write_json(path, envelope)
        hashes[str(path.relative_to(root))] = sha256_file(path)
        print(f"[I1] completed {item}", flush=True)
    summary = {"round_id": "I1", "status": "COMPLETE", "frozen_analysis_plan_commit": commit, "plan_hash": plan["plan_hash"], "plan_file_sha256": sha256_file(root / PLAN), "item_sha256": hashes, "work_counts": plan["work_counts"], "new_stationary_solves": 0}
    atomic_write_json(root / "constraint-lab/reports/generation-008i-round-i1-tables.json", summary)
    return summary


def verify(root, commit):
    plan = require_execution(root, commit)
    summary = read_json(root / "constraint-lab/reports/generation-008i-round-i1-tables.json")
    if summary["plan_hash"] != plan["plan_hash"] or summary["status"] != "COMPLETE":
        raise HistoryError("I1 summary identity mismatch")
    for path, digest in summary["item_sha256"].items():
        if sha256_file(root / path) != digest:
            raise HistoryError("I1 published item digest mismatch")
        envelope = read_json(root / path)
        if fingerprint(envelope["result"]) != envelope["result_sha256"]:
            raise HistoryError("I1 scientific payload digest mismatch")
        validate(envelope["item_id"], decode(envelope["result"]))
    return {"status": "VERIFIED", "items": 2, "plan_hash": plan["plan_hash"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("plan", "execute", "verify"))
    parser.add_argument("--frozen-plan-commit")
    args = parser.parse_args()
    root = repository_root()
    print(write_plan(root) if args.command == "plan" else execute(root, args.frozen_plan_commit) if args.command == "execute" else verify(root, args.frozen_plan_commit))


if __name__ == "__main__":
    main()
