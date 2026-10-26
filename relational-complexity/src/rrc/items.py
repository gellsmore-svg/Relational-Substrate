"""Execute one frozen item. No item reads another item's output."""

from __future__ import annotations

import time
import traceback
from fractions import Fraction

import numpy as np

from rrc import ENGINE_VERSION
from rrc.composition import (
    active_intersection_labels,
    constant_labels,
    cover_count_labels,
    labelled_active_block_labels,
    labelled_realised_block_labels,
    realised_intersection_labels,
    realised_overlap_count_labels,
    observation_law,
    present_canonical_line_graph_labels,
    present_carrier_orbit_labels,
    present_degree_labels,
    present_edge_count_labels,
    present_labelled_line_graph_labels,
    present_line_graph_labels,
    rational_lumpability,
    successive_observations,
)
from rrc.constraints import (
    KERNEL_METHOD,
    STRUCTURE_METHOD,
    compile_model,
    occupation_report,
    support_report,
    weight_table_hash,
)
from rrc.coupled_models import correspondence
from rrc.event_kernel import CLOCK, STRICT_METHOD_ID, kernel, single_toggle_catalogue, strict_kernel
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


OBSERVATION_LABELS = {
    "present_line_graph": lambda n, edges, cover: present_line_graph_labels(edges),
    "present_edge_count": lambda n, edges, cover: present_edge_count_labels(edges),
    "constant_label": lambda n, edges, cover: constant_labels(edges),
    "present_degree_sequence": lambda n, edges, cover: present_degree_labels(n, edges),
    "labelled_line_graph": lambda n, edges, cover: present_labelled_line_graph_labels(edges),
    "canonical_line_graph": lambda n, edges, cover: present_canonical_line_graph_labels(edges),
    "carrier_orbit": lambda n, edges, cover: present_carrier_orbit_labels(n, edges),
    "cover_count": lambda n, edges, cover: cover_count_labels(edges, cover),
    "active_intersection": lambda n, edges, cover: active_intersection_labels(edges, cover),
    "labelled_active_blocks": lambda n, edges, cover: labelled_active_block_labels(edges, cover),
    "realised_intersection": lambda n, edges, cover: realised_intersection_labels(edges, cover),
    "labelled_realised_blocks": lambda n, edges, cover: labelled_realised_block_labels(edges, cover),
    "realised_overlap_count": lambda n, edges, cover: realised_overlap_count_labels(edges, cover),
}

COVER_OBSERVATIONS = (
    "cover_count",
    "active_intersection",
    "labelled_active_blocks",
    "realised_intersection",
    "labelled_realised_blocks",
    "realised_overlap_count",
)


def execute_composition_observation(spec: dict) -> dict:
    """Lumpability of one label map. The map is not a new coordinate."""
    started = time.perf_counter()
    observation = spec.get("observation")
    if observation not in OBSERVATION_LABELS:
        raise ValueError(f"unknown observation {observation}")
    baseline = spec.get("baseline", 1)
    model = compile_model(spec["n"], spec["carrier"], list(spec.get("constraints", [])), baseline)
    edges = [list(edge) for edge in model["carrier_edges"]]
    cover = spec.get("cover")
    if observation in COVER_OBSERVATIONS and not isinstance(cover, list):
        raise ValueError(f"{observation} requires a cover")
    labels = OBSERVATION_LABELS[observation](model["n"], edges, cover)
    law = observation_law(model["weights"], labels)
    weights = model["weights"]
    witness = law["witness"]
    witness_payload = None
    if witness is not None:
        witness_payload = {
            "block": witness["block"],
            "states": witness["states"],
            "pairwise_l1": fraction_payload(witness["pairwise_l1"]),
        }
    return {
        "status": "complete",
        "engine_version": ENGINE_VERSION,
        "item_id": spec["id"],
        "round_id": spec.get("round_id"),
        "type": "composition_observation",
        "role": spec.get("role", "observation"),
        "idea_ids": list(spec.get("idea_ids", [])),
        "observation": observation,
        "cover": cover if observation in COVER_OBSERVATIONS else None,
        "n": model["n"],
        "n_states": int(weights.shape[0]),
        "n_edges": int(weights.shape[1]),
        "n_blocks": law["n_blocks"],
        "n_distinct_labels": law["n_distinct_labels"],
        "injective": law["injective"],
        "new_state": False,
        "exact": law["exact"],
        "defect_l1": fraction_payload(law["defect_l1"]),
        "quotient": law["quotient"],
        "further_label": "undefined",
        "further_label_reason": "no second label map is declared",
        "dynamics": "halt_self_loop projection; Markov only when exact",
        "witness": witness_payload,
        "baseline": model["baseline"],
        "grammar_id": model["grammar_id"],
        "carrier": {
            "kind": model["carrier_kind"],
            "edges": edges,
        },
        "weight_sha256": weight_table_hash(weights),
        "kernel_sha256": model["kernel_sha256"],
        "kernel_method": KERNEL_METHOD,
        "structure_sha256": model["structure_sha256"],
        "structure_method": STRUCTURE_METHOD,
        "weights": [[int(value) for value in row] for row in weights.tolist()],
        "clock": {
            "name": HALT_COMPLETION,
            "step": "one carrier pair, probability proportional to its current weight",
        },
        "elapsed_s": round(time.perf_counter() - started, 6),
    }


def _fraction_ready(value):
    if value is None:
        return None
    if isinstance(value, Fraction):
        return fraction_payload(value)
    if isinstance(value, dict) and "num" in value and "den" in value:
        return {
            "num": str(value["num"]),
            "den": str(value["den"]),
            "float": float(Fraction(int(value["num"]), int(value["den"]))),
        }
    raise TypeError("a defect must be a fraction or undefined")


def _stage_ready(stage: dict) -> dict:
    exact = stage["exact"]
    rows = stage["quotient_rows"]
    if exact is True and not isinstance(rows, list):
        raise RuntimeError("an exact stage has no quotient rows")
    if exact is not True and rows is not None:
        raise RuntimeError("an undefined stage stores quotient rows")
    return {
        "depth": stage["depth"],
        "typed": stage["typed"],
        "factors_through_previous": stage["factors_through_previous"],
        "n_distinct_labels": stage["n_distinct_labels"],
        "exact": exact,
        "defect_l1": _fraction_ready(stage["defect_l1"]),
        "quotient_defined": stage["quotient_defined"],
        "quotient_rows": rows,
        "undefined_reason": stage["undefined_reason"],
        "new_state": False,
    }


def _direct_ready(law: dict) -> dict:
    exact = law["exact"]
    rows = law["quotient_rows"]
    if exact is True and not isinstance(rows, list):
        raise RuntimeError("an exact direct law has no quotient rows")
    if exact is not True and rows is not None:
        raise RuntimeError("an inexact direct law stores quotient rows")
    return {
        "exact": exact,
        "defect_l1": _fraction_ready(law["defect_l1"]),
        "n_distinct_labels": law["n_distinct_labels"],
        "quotient_defined": law["quotient_defined"],
        "quotient_rows": rows,
    }


def execute_successive_observation(spec: dict) -> dict:
    """Store a typed sequence of label maps. The maps add no state.

    A later sequential kernel exists only when ``successive_observations``
    defines it. This item does not manufacture a kernel for a non-exact
    or untyped stage. The transition law remains the carrier weight table.
    """
    started = time.perf_counter()
    names = spec.get("observations")
    if not isinstance(names, list) or len(names) < 2:
        raise ValueError("a successive observation names at least two maps")
    if any(not isinstance(name, str) or name not in OBSERVATION_LABELS for name in names):
        raise ValueError("unknown observation")
    baseline = spec.get("baseline", 1)
    model = compile_model(spec["n"], spec["carrier"], list(spec.get("constraints", [])), baseline)
    edges = [list(edge) for edge in model["carrier_edges"]]
    cover = spec.get("cover")
    if any(name in COVER_OBSERVATIONS for name in names) and not isinstance(cover, list):
        raise ValueError("a cover observation requires a cover")
    stages = [OBSERVATION_LABELS[name](model["n"], edges, cover) for name in names]
    report = successive_observations(model["weights"], stages)
    weights = model["weights"]
    return {
        "status": "complete",
        "engine_version": ENGINE_VERSION,
        "item_id": spec["id"],
        "round_id": spec.get("round_id"),
        "type": "successive_observation",
        "role": spec.get("role", "successive"),
        "idea_ids": list(spec.get("idea_ids", [])),
        "observations": list(names),
        "cover": cover if any(name in COVER_OBSERVATIONS for name in names) else None,
        "n": model["n"],
        "n_states": int(weights.shape[0]),
        "n_edges": int(weights.shape[1]),
        "new_state": False,
        "stages": [_stage_ready(stage) for stage in report["stages"]],
        "direct": [_direct_ready(law) for law in report["direct"]],
        "exact_prefix": report["exact_prefix"],
        "kernels_agree": report["kernels_agree"],
        "agreement": report["agreement"],
        "conditional_exactness": report["conditional_exactness"],
        "history_dependent": report["history_dependent"],
        "label_counts": report["label_counts"],
        "baseline": model["baseline"],
        "grammar_id": model["grammar_id"],
        "carrier": {
            "kind": model["carrier_kind"],
            "edges": edges,
        },
        "weight_sha256": weight_table_hash(weights),
        "kernel_sha256": model["kernel_sha256"],
        "kernel_method": KERNEL_METHOD,
        "structure_sha256": model["structure_sha256"],
        "structure_method": STRUCTURE_METHOD,
        "weights": [[int(value) for value in row] for row in weights.tolist()],
        "clock": {
            "name": HALT_COMPLETION,
            "step": "one carrier pair, probability proportional to its current weight",
        },
        "elapsed_s": round(time.perf_counter() - started, 6),
    }


def execute_event_kernel(spec: dict) -> dict:
    """Normalise one declared event list. This does not compile a weight table.

    The state is the integer named by the spec. The item adds no coordinate.
    The call is ``kernel``, so the stored method is event-kernel-0.1.0.
    That method does not check Hamming distance.
    """
    started = time.perf_counter()
    family = spec.get("family")
    if not isinstance(family, str) or family == "":
        raise ValueError("an event kernel names a family")
    catalogue = spec.get("catalogue")
    events = spec.get("events")
    if catalogue is not None and events is not None:
        raise ValueError("an event kernel names a catalogue or an event list")
    n_states = spec.get("n_states")
    if "bit_width" in spec:
        width = spec["bit_width"]
        if isinstance(width, bool) or not isinstance(width, int) or width < 1:
            raise ValueError("bit_width must be a positive integer")
        if isinstance(n_states, bool) or n_states != (1 << width):
            raise ValueError("n_states must be 2 to the bit width")
    if catalogue == "single_toggle":
        rows = spec.get("rows")
        if not isinstance(rows, list) or n_states != len(rows):
            raise ValueError("n_states must match the single-toggle catalogue")
        events = single_toggle_catalogue(rows)
    elif catalogue is not None:
        raise ValueError("unknown catalogue")
    elif not isinstance(events, list):
        raise ValueError("an event kernel names a catalogue or an event list")
    report = kernel(n_states, events)
    payload = {
        "status": "complete",
        "engine_version": ENGINE_VERSION,
        "item_id": spec["id"],
        "round_id": spec.get("round_id"),
        "type": "event_kernel",
        "role": spec.get("role"),
        "family": family,
        "method": report["method"],
        "clock": report["clock"],
        "n_states": report["n_states"],
        "halt_self_loop_is_event": False,
        "new_primitive": False,
        "catalogue": catalogue,
        "event_count": len(events),
        "aggregated_weights": report["aggregated_weights"],
        "row_sums": report["row_sums"],
        "enabled_event_counts": report["enabled_event_counts"],
        "completions": report["completions"],
        "probabilities": [
            [fraction_payload(cell) for cell in row] for row in report["probabilities"]
        ],
        "elapsed_s": round(time.perf_counter() - started, 6),
    }
    if "bit_width" in spec:
        payload["bit_width"] = spec["bit_width"]
    return payload


def _fraction_rows(rows):
    if rows is None:
        return None
    return [[fraction_payload(cell) for cell in row] for row in rows]


def _declared_events(spec: dict) -> tuple[int, list]:
    """Resolve one catalogue or one event list. The two keys are not combined."""
    catalogue = spec.get("catalogue")
    events = spec.get("events")
    if catalogue is not None and events is not None:
        raise ValueError("an event list names a catalogue or an event list")
    n_states = spec.get("n_states")
    if isinstance(n_states, bool) or not isinstance(n_states, int):
        raise ValueError("n_states must be a positive integer")
    if catalogue == "single_toggle":
        rows = spec.get("rows")
        if not isinstance(rows, list) or n_states != len(rows):
            raise ValueError("n_states must match the single-toggle catalogue")
        events = single_toggle_catalogue(rows)
    elif catalogue is not None:
        raise ValueError("unknown catalogue")
    elif not isinstance(events, list):
        raise ValueError("an event list names a catalogue or an event list")
    return n_states, events


def _bit_width_of(spec: dict):
    if "bit_width" not in spec:
        return None
    width = spec["bit_width"]
    if isinstance(width, bool) or not isinstance(width, int) or width < 1:
        raise ValueError("bit_width must be a positive integer")
    return width


def execute_strict_event_comparison(spec: dict) -> dict:
    """One strict event law, and a declared image when the spec names one.

    The reference law is inside this spec. This item does not read another
    item. A missing image stores no correspondence. A leaking image stores
    no restricted rows. No occupation is stored.
    """
    started = time.perf_counter()
    family = spec.get("family")
    if not isinstance(family, str) or family == "":
        raise ValueError("a strict event comparison names a family")
    n_states, events = _declared_events(spec)
    width = _bit_width_of(spec)
    report = strict_kernel(n_states, events, bit_width=width)
    image_map = spec.get("image_map")
    reference = spec.get("reference")
    compared = None
    if image_map is not None:
        if not isinstance(reference, dict):
            raise ValueError("an image map names a reference law")
        if not isinstance(image_map, list) or not image_map:
            raise ValueError("an image map lists the image of each reference state")
        ref_states, ref_events = _declared_events(reference)
        if len(image_map) != ref_states:
            raise ValueError("an image map covers the reference state space")
        ref_report = strict_kernel(ref_states, ref_events, bit_width=_bit_width_of(reference))
        checked = correspondence(
            ref_report["probabilities"],
            report["probabilities"],
            dict(enumerate(image_map)),
        )
        compared = {
            "image": checked["image"],
            "image_invariant": checked["image_invariant"],
            "conjugate": checked["conjugate"],
            "restricted_rows": _fraction_rows(checked["restricted_rows"]),
        }
    payload = {
        "status": "complete",
        "engine_version": ENGINE_VERSION,
        "item_id": spec["id"],
        "round_id": spec.get("round_id"),
        "type": "strict_event_comparison",
        "role": spec.get("role"),
        "family": family,
        "method": STRICT_METHOD_ID,
        "clock": CLOCK,
        "semantics": report["semantics"],
        "n_states": report["n_states"],
        "halt_self_loop_is_event": False,
        "new_primitive": False,
        "catalogue": spec.get("catalogue"),
        "event_count": len(report["events"]),
        "events": report["events"],
        "aggregated_weights": report["aggregated_weights"],
        "row_sums": report["row_sums"],
        "enabled_event_counts": report["enabled_event_counts"],
        "completions": report["completions"],
        "probabilities": _fraction_rows(report["probabilities"]),
        "correspondence": compared,
        "elapsed_s": round(time.perf_counter() - started, 6),
    }
    if width is not None:
        payload["bit_width"] = width
    return payload


def _step_distribution(probabilities, initial: int, horizon: int) -> list[Fraction]:
    size = len(probabilities)
    dist = [Fraction(0) for _ in range(size)]
    dist[initial] = Fraction(1)
    for _ in range(horizon):
        nxt = [Fraction(0) for _ in range(size)]
        for source, mass in enumerate(dist):
            if mass == 0:
                continue
            for target, prob in enumerate(probabilities[source]):
                nxt[target] += mass * prob
        dist = nxt
    return dist


def execute_event_horizon(spec: dict) -> dict:
    """A declared horizon of one strict event law, plus one label partition.

    The horizon is a power of the one-step kernel. It is not an intervention.
    A partition that is not strongly lumpable stores no quotient rows.
    No stationary distribution is stored.
    """
    started = time.perf_counter()
    family = spec.get("family")
    if not isinstance(family, str) or family == "":
        raise ValueError("an event horizon names a family")
    horizon = spec.get("horizon")
    if isinstance(horizon, bool) or not isinstance(horizon, int) or horizon < 1 or horizon > 4:
        raise ValueError("horizon must be an integer from 1 to 4")
    n_states, events = _declared_events(spec)
    width = _bit_width_of(spec)
    report = strict_kernel(n_states, events, bit_width=width)
    initial = spec.get("initial_state")
    if isinstance(initial, bool) or not isinstance(initial, int) or initial < 0 or initial >= n_states:
        raise ValueError("initial_state must be an integer state")
    labels = spec.get("labels")
    if not isinstance(labels, list) or len(labels) != n_states:
        raise ValueError("labels must cover every state")
    subset = spec.get("subset")
    if not isinstance(subset, list) or not subset or len(set(subset)) != len(subset):
        raise ValueError("subset lists distinct states")
    if any(isinstance(state, bool) or not isinstance(state, int) or state < 0 or state >= n_states for state in subset):
        raise ValueError("subset lists states of this law")
    lump = rational_lumpability(report["probabilities"], labels)
    dist = _step_distribution(report["probabilities"], initial, horizon)
    payload = {
        "status": "complete",
        "engine_version": ENGINE_VERSION,
        "item_id": spec["id"],
        "round_id": spec.get("round_id"),
        "type": "event_horizon",
        "role": spec.get("role"),
        "family": family,
        "method": STRICT_METHOD_ID,
        "clock": CLOCK,
        "semantics": report["semantics"],
        "n_states": report["n_states"],
        "halt_self_loop_is_event": False,
        "new_primitive": False,
        "intervention": None,
        "horizon": horizon,
        "initial_state": initial,
        "catalogue": spec.get("catalogue"),
        "event_count": len(report["events"]),
        "completions": report["completions"],
        "probabilities": _fraction_rows(report["probabilities"]),
        "horizon_distribution": [fraction_payload(cell) for cell in dist],
        "subset": list(subset),
        "subset_probability": fraction_payload(sum((dist[state] for state in subset), Fraction(0))),
        "lumpability": {
            "exact": lump["exact"],
            "defined": lump["defined"],
            "defect_l1": fraction_payload(lump["defect_l1"]),
            "rows": _fraction_rows(lump["rows"]),
            "reason": lump["reason"],
        },
        "elapsed_s": round(time.perf_counter() - started, 6),
    }
    if width is not None:
        payload["bit_width"] = width
    return payload


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
    if kind == "composition_observation":
        return execute_composition_observation(spec)
    if kind == "successive_observation":
        return execute_successive_observation(spec)
    if kind == "event_kernel":
        return execute_event_kernel(spec)
    if kind == "strict_event_comparison":
        return execute_strict_event_comparison(spec)
    if kind == "event_horizon":
        return execute_event_horizon(spec)
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
