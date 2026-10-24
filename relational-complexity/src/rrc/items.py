"""Execute one frozen item. No item reads another item's output."""

from __future__ import annotations

import time
import traceback

import numpy as np

from rrc import ENGINE_VERSION
from rrc.constraints import (
    KERNEL_METHOD,
    STRUCTURE_METHOD,
    compile_model,
    occupation_report,
    support_report,
    weight_table_hash,
)
from rrc.model import (
    build_weights,
    check_state_independent_identity,
    describe_state,
    edge_list,
    edge_presence,
    HALT_COMPLETION,
    fraction_payload,
    grammar_form,
    lumpability,
    lumpable_closure,
    pair_depth,
    partition_labels,
    recurrent_class_count,
    state_independent_rate_identity,
    stationary_balanced,
    stationary_dense,
    toggle_rates,
)


def _json_ready(report: dict) -> dict:
    witness = report["witness"]
    payload = {
        "exact": report["exact"],
        "defect_l1": fraction_payload(report["defect_l1"]),
        "n_blocks": report["n_blocks"],
        "max_block_size": report["max_block_size"],
        "witness": None,
    }
    if witness is not None:
        payload["witness"] = {
            "block": witness["block"],
            "states": witness["states"],
            "pairwise_l1": fraction_payload(witness["pairwise_l1"]),
        }
    return payload


def execute_lumpability(spec: dict) -> dict:
    started = time.perf_counter()
    n = int(spec["n"])
    weights = build_weights(n, spec["rule"])
    labels, blocks, hidden, visible = partition_labels(n, spec["partition"], "interface")
    if blocks != len(set(labels)):
        raise RuntimeError("block count drifted")
    base = lumpability(weights, labels)
    augmentations = {}
    for name in spec.get("augmentations", []):
        aug_labels, aug_blocks, _hidden, _visible = partition_labels(n, spec["partition"], name)
        if aug_blocks != len(set(aug_labels)):
            raise RuntimeError("augmentation block count drifted")
        report = lumpability(weights, aug_labels)
        packed = _json_ready(report)
        packed["n_blocks"] = aug_blocks
        augmentations[name] = packed
    closure = {"computed": False}
    if spec.get("closure"):
        closure = lumpable_closure(weights, labels)
        if not closure["exact"]:
            raise RuntimeError("lumpable closure did not reach a lumpable partition")
    classes = recurrent_class_count(weights)
    grammar = grammar_form(weights, labels, hidden, visible, base["exact"])
    identity = None
    if spec.get("identity_check"):
        identity = check_state_independent_identity(weights, labels, hidden, visible)
    edges = edge_list(n)
    witness = _json_ready(base)["witness"]
    if witness is not None:
        witness = dict(witness)
        witness["decoded"] = [describe_state(state, edges) for state in witness["states"]]
    status = "complete"
    if identity is not None and not identity["ok"]:
        status = "failed"
    return {
        "status": status,
        "engine_version": ENGINE_VERSION,
        "item_id": spec["id"],
        "round_id": spec["round_id"],
        "type": "lumpability",
        "role": spec.get("role", "unopened"),
        "n": n,
        "rule_family": spec["rule"]["family"],
        "partition": spec["partition"],
        "n_states": int(weights.shape[0]),
        "n_edges": int(weights.shape[1]),
        "n_hidden_edges": len(hidden),
        "n_interface_edges": len(visible),
        "exact": base["exact"],
        "defect_l1": fraction_payload(base["defect_l1"]),
        "n_blocks": base["n_blocks"],
        "max_block_size": base["max_block_size"],
        "witness": witness,
        "augmentations": augmentations,
        "closure": closure,
        "classes": classes,
        "grammar": grammar,
        "identity": identity,
        "method": "exact_rational_enumeration",
        "halt_completion": classes["halt_completion"],
        "elapsed_s": round(time.perf_counter() - started, 6),
    }


def _depth_summary(edges, base_presence, pert_presence, base_rates, pert_rates) -> list[dict]:
    buckets: dict[int, dict] = {}
    for edge, depth in enumerate(pair_depth(edges)):
        bucket = buckets.setdefault(
            depth,
            {"depth": depth, "edges": [], "occupation_abs": [], "rate_abs": []},
        )
        bucket["edges"].append([edges[edge][0], edges[edge][1]])
        bucket["occupation_abs"].append(abs(float(pert_presence[edge] - base_presence[edge])))
        bucket["rate_abs"].append(abs(float(pert_rates[edge] - base_rates[edge])))
    summary = []
    for depth in sorted(buckets):
        bucket = buckets[depth]
        summary.append(
            {
                "depth": depth,
                "edges": bucket["edges"],
                "occupation_abs_mean": float(np.mean(bucket["occupation_abs"])),
                "occupation_abs_max": float(np.max(bucket["occupation_abs"])),
                "rate_abs_mean": float(np.mean(bucket["rate_abs"])),
                "rate_abs_max": float(np.max(bucket["rate_abs"])),
            }
        )
    return summary


def _solve_pair(weights: np.ndarray, spec: dict) -> dict:
    tolerance = float(spec["tolerance"])
    cross = float(spec["cross_tolerance"])
    maximum = int(spec["max_iter"])
    uniform = stationary_balanced(weights, "uniform", tolerance, maximum)
    empty = stationary_balanced(weights, "empty", tolerance, maximum)
    gap = float(np.abs(uniform["distribution"] - empty["distribution"]).sum())
    if max(uniform["image_gap"], empty["image_gap"]) > cross:
        uniform["converged"] = False
    dense_gap = None
    if weights.shape[0] <= int(spec.get("dense_max_states", 1024)):
        dense = stationary_dense(weights)
        dense_gap = float(np.abs(dense - uniform["distribution"]).sum())
    converged = bool(uniform["converged"] and empty["converged"] and gap <= cross)
    if dense_gap is not None:
        converged = converged and dense_gap <= cross
    return {
        "distribution": uniform["distribution"],
        "uniform_iterations": uniform["iterations"],
        "uniform_residual": uniform["residual"],
        "empty_iterations": empty["iterations"],
        "empty_residual": empty["residual"],
        "start_l1": gap,
        "dense_l1": dense_gap,
        "converged": converged,
    }


def execute_propagation(spec: dict) -> dict:
    started = time.perf_counter()
    n = int(spec["n"])
    base_weights = build_weights(n, spec["base_rule"])
    pert_weights = build_weights(n, spec["perturbed_rule"])
    base = _solve_pair(base_weights, spec)
    pert = _solve_pair(pert_weights, spec)
    status = "complete" if base["converged"] and pert["converged"] else "unresolved"
    edges = edge_list(n)
    identity_gap = None
    if spec.get("identity_check"):
        law = state_independent_rate_identity(base_weights)
        pert_law = state_independent_rate_identity(pert_weights)
        if law is None or pert_law is None:
            status = "failed"
            identity_gap = {"ok": False, "reason": "identity requested for a state-dependent rule"}
        else:
            base_presence = edge_presence(base["distribution"])
            pert_presence = edge_presence(pert["distribution"])
            base_rates = toggle_rates(base["distribution"], base_weights)
            pert_rates = toggle_rates(pert["distribution"], pert_weights)
            occupation_gap = max(
                float(np.max(np.abs(base_presence - law["occupation"]))),
                float(np.max(np.abs(pert_presence - pert_law["occupation"]))),
            )
            rate_gap = max(
                float(np.max(np.abs(base_rates - np.array(law["toggle_rate"])))),
                float(np.max(np.abs(pert_rates - np.array(pert_law["toggle_rate"])))),
            )
            identity_gap = {
                "ok": occupation_gap <= float(spec["cross_tolerance"]) and rate_gap <= float(spec["cross_tolerance"]),
                "occupation_gap": occupation_gap,
                "rate_gap": rate_gap,
            }
            if not identity_gap["ok"]:
                status = "failed"
    base_presence = edge_presence(base["distribution"])
    pert_presence = edge_presence(pert["distribution"])
    base_rates = toggle_rates(base["distribution"], base_weights)
    pert_rates = toggle_rates(pert["distribution"], pert_weights)
    return {
        "status": status,
        "engine_version": ENGINE_VERSION,
        "item_id": spec["id"],
        "round_id": spec["round_id"],
        "type": "propagation",
        "role": spec.get("role", "unopened"),
        "n": n,
        "base_family": spec["base_rule"]["family"],
        "perturbed_family": spec["perturbed_rule"]["family"],
        "scaffold": "path_index_min_endpoint",
        "n_states": int(base_weights.shape[0]),
        "stationary_tv": float(0.5 * np.abs(base["distribution"] - pert["distribution"]).sum()),
        "depths": _depth_summary(edges, base_presence, pert_presence, base_rates, pert_rates),
        "edge_occupation_base": base_presence.tolist(),
        "edge_occupation_perturbed": pert_presence.tolist(),
        "edge_rate_base": base_rates.tolist(),
        "edge_rate_perturbed": pert_rates.tolist(),
        "solver": {
            "base": {key: value for key, value in base.items() if key != "distribution"},
            "perturbed": {key: value for key, value in pert.items() if key != "distribution"},
            "method": "parity_balanced_iteration",
            "cross_check": "second_start_and_dense_solve_when_states_fit",
        },
        "identity": identity_gap,
        "tolerance": spec["tolerance"],
        "cross_tolerance": spec["cross_tolerance"],
        "elapsed_s": round(time.perf_counter() - started, 6),
    }


def execute_probe(spec: dict) -> dict:
    mode = spec["mode"]
    if mode == "ok":
        return {
            "status": "complete",
            "engine_version": ENGINE_VERSION,
            "item_id": spec["id"],
            "round_id": spec["round_id"],
            "type": "probe",
            "value": spec.get("value"),
        }
    if mode == "sleep":
        time.sleep(float(spec["seconds"]))
        return {
            "status": "complete",
            "engine_version": ENGINE_VERSION,
            "item_id": spec["id"],
            "round_id": spec["round_id"],
            "type": "probe",
            "value": "slept",
        }
    if mode == "raise":
        raise RuntimeError("probe raised")
    raise ValueError(f"unknown probe mode {mode}")


def execute_atlas_core(spec: dict) -> dict:
    """Common-core atlas cell. Does not decide which outcome would be interesting."""
    started = time.perf_counter()
    baseline = spec.get("baseline", 1)
    model = compile_model(spec["n"], spec["carrier"], spec["constraints"], baseline)
    tolerance = float(spec["tolerance"])
    cross = float(spec["cross_tolerance"])
    maximum = int(spec["max_iter"])
    dense_max = int(spec["dense_max_states"])
    occupied = occupation_report(model, tolerance, cross, maximum, dense_max)
    support = support_report(model["weights"])
    status = "complete"
    if support["classes"] != occupied["classes"]:
        status = "failed"
    if occupied["occupation"]["status"] == "unresolved":
        status = "unresolved"
    if model["action_bit_independent"] and not model["empirical_bit_independent"]:
        status = "failed"
    weights = model["weights"]
    return {
        "status": status,
        "engine_version": ENGINE_VERSION,
        "grammar_id": model["grammar_id"],
        "item_id": spec["id"],
        "round_id": spec["round_id"],
        "type": "atlas_core",
        "role": spec.get("role", "unopened"),
        "idea_ids": list(spec.get("idea_ids", [])),
        "n": model["n"],
        "n_states": int(weights.shape[0]),
        "n_edges": int(weights.shape[1]),
        "carrier": {
            "kind": model["carrier_kind"],
            "edges": [[left, right] for left, right in model["carrier_edges"]],
            "components": model["carrier_components"],
            "components_note": "components of the carrier graph, isolated nodes included; an instrument",
        },
        "baseline": model["baseline"],
        "composer": {
            "name": "prohibit_then_product",
            "order_independent": True,
        },
        "clock": {
            "name": HALT_COMPLETION,
            "step": "one carrier pair, probability proportional to its current weight",
        },
        "compilation": {
            "all_weights_positive": bool(np.all(weights > 0)),
            "gate": "current-state single-toggle weights",
            "history": False,
            "hyperedge": False,
            "multi_pair_event": False,
            "new_primitive": False,
        },
        "bookkeeping": model["bookkeeping"],
        "imposed_rule_dependency": model["imposed_rule_dependency"],
        "action_bit_independent": bool(model["action_bit_independent"]),
        "empirical_bit_independent": bool(model["empirical_bit_independent"]),
        "weight_sha256": weight_table_hash(weights),
        "kernel_sha256": model["kernel_sha256"],
        "kernel_method": KERNEL_METHOD,
        "structure_sha256": model["structure_sha256"],
        "structure_method": STRUCTURE_METHOD,
        "weights": [[int(value) for value in row] for row in weights.tolist()],
        "positive_transitions": support["positive_transitions"],
        "zero_cells": support["zero_cells"],
        "classes": support["classes"],
        "occupation": occupied["occupation"],
        "solver_budget": {
            "cross_tolerance": cross,
            "dense_max_states": dense_max,
            "max_iter": maximum,
            "tolerance": tolerance,
            "used": occupied["occupation"].get("method") == "stationary_balanced",
        },
        "method": "exact_weight_table",
        "elapsed_s": round(time.perf_counter() - started, 6),
    }


def execute_spec(spec: dict) -> dict:
    kind = spec["type"]
    if kind == "lumpability":
        return execute_lumpability(spec)
    if kind == "propagation":
        return execute_propagation(spec)
    if kind == "probe":
        return execute_probe(spec)
    if kind == "atlas_core":
        return execute_atlas_core(spec)
    raise ValueError(f"unknown item type {kind}")


def execute_spec_catching(spec: dict) -> dict:
    try:
        return execute_spec(spec)
    except Exception:
        return {
            "status": "failed",
            "engine_version": ENGINE_VERSION,
            "item_id": spec.get("id"),
            "round_id": spec.get("round_id"),
            "type": spec.get("type"),
            "error": traceback.format_exc(),
        }
