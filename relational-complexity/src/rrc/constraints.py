"""Opening grammar: current-state prohibit and multiply on one carrier.

A carrier is the set of undirected pairs that are allowed to be events.
The state is the subset of that carrier which is present. A chain is a
smaller bit set, not a drawing of the complete graph and not a complete
graph with frozen pairs.

Composition does not depend on list order. A matching prohibit sets the
weight to 0. Otherwise the baseline is multiplied by every matching factor.
A multiply does not revive a zero. Factors are integers of at least 2, so
this composer has no inverse and two multiplies cannot cancel back to the
baseline.

K is computed per feature. It is not the sum of literals across features.
J counts features. Declared cardinality counts the list, including duplicates.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import combinations

import numpy as np

from rrc.model import (
    HALT_COMPLETION,
    MAX_EDGES,
    edge_list,
    fraction_payload,
    recurrent_class_count,
    stationary_balanced,
    stationary_dense,
)

GRAMMAR_ID = "opening-prohibit-multiply-v1"
EFFECTS = ("prohibit", "multiply")
ACTIONS = ("either", "form", "dissolve")
POLARITIES = ("present", "absent")
EFFECTIVE_METHOD = "minimum_equivalent_subset"
MAX_EXACT_ABLATION = 16
MAX_EXACT_DEPENDENCY_NODES = 12


def _pair(raw, n: int) -> tuple[int, int]:
    if not isinstance(raw, (list, tuple)) or len(raw) != 2:
        raise ValueError("a pair must be two node labels")
    if isinstance(raw[0], bool) or isinstance(raw[1], bool):
        raise ValueError("node labels must be integers")
    try:
        left = int(raw[0])
        right = int(raw[1])
    except (TypeError, ValueError) as exc:
        raise ValueError("node labels must be integers") from exc
    if left > right:
        left, right = right, left
    if left == right or left < 0 or right >= n:
        raise ValueError(f"pair {(left, right)} is not an undirected pair on 0..{n - 1}")
    return (left, right)


def resolve_carrier(n: int, carrier) -> tuple[list[tuple[int, int]], str]:
    """Return carrier edges in declared order, and the kind name."""
    count = int(n)
    if count < 0:
        raise ValueError("N must be non-negative")
    if carrier is None or carrier == "complete":
        return edge_list(count), "complete"
    if not isinstance(carrier, dict) or "kind" not in carrier:
        raise ValueError("carrier must be complete or a listed edge set")
    kind = carrier["kind"]
    if kind == "complete":
        return edge_list(count), "complete"
    if kind != "listed":
        raise ValueError(f"unknown carrier kind {kind}")
    raw_edges = carrier.get("edges")
    if not isinstance(raw_edges, list) or not raw_edges:
        raise ValueError("a listed carrier needs at least one edge")
    edges: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    for raw in raw_edges:
        pair = _pair(raw, count)
        if pair in seen:
            raise ValueError(f"duplicate carrier edge {pair}")
        seen.add(pair)
        edges.append(pair)
    if len(edges) > MAX_EDGES:
        raise ValueError(f"carrier has {len(edges)} edges, above the {MAX_EDGES}-bit builder")
    return edges, "listed"


def _constraint(raw: dict, n: int) -> dict:
    if not isinstance(raw, dict):
        raise ValueError("a constraint must be an object")
    effect = raw.get("effect")
    if effect not in EFFECTS:
        raise ValueError(f"unknown effect {effect}")
    action = raw.get("action")
    if action not in ACTIONS:
        raise ValueError(f"unknown action {action}")
    event = _pair(raw.get("event"), n)
    when = raw.get("when")
    if not isinstance(when, dict):
        raise ValueError("a constraint needs a when clause on a different edge")
    condition = _pair(when.get("edge"), n)
    polarity = when.get("polarity")
    if polarity not in POLARITIES:
        raise ValueError(f"unknown polarity {polarity}")
    if condition == event:
        raise ValueError("the condition edge must differ from the event edge")
    factor = None
    if effect == "multiply":
        raw_factor = raw.get("factor")
        if isinstance(raw_factor, bool) or not isinstance(raw_factor, int) or raw_factor < 2:
            raise ValueError("a multiply factor must be an integer >= 2")
        factor = raw_factor
    elif "factor" in raw:
        raise ValueError("a prohibit does not take a factor")
    return {
        "effect": effect,
        "action": action,
        "event": event,
        "condition": condition,
        "polarity": polarity,
        "factor": factor,
    }


def _literals(constraint: dict) -> int:
    """Condition, plus the event bit when the action is form or dissolve."""
    return 2 if constraint["action"] in ("form", "dissolve") else 1


def _guard(state: int, condition_bit: int, event_bit: int, polarity: str, action: str) -> bool:
    condition_on = ((state >> condition_bit) & 1) == 1
    if polarity == "present" and not condition_on:
        return False
    if polarity == "absent" and condition_on:
        return False
    event_on = ((state >> event_bit) & 1) == 1
    if action == "form":
        return not event_on
    if action == "dissolve":
        return event_on
    return True


def compile_weight_table(n: int, carrier, constraints: list, baseline: int = 1) -> np.ndarray:
    """Integer weights, shape ``(2**|carrier|, |carrier|)``, columns in carrier order."""
    weights, _edges, _parsed, _active = _compile(n, carrier, constraints, baseline)
    return weights


def _compile(n: int, carrier, constraints: list, baseline: int):
    if isinstance(baseline, bool) or not isinstance(baseline, int) or baseline < 1:
        raise ValueError("baseline must be a positive integer")
    if not isinstance(constraints, list):
        raise ValueError("constraints must be a list")
    edges, _kind = resolve_carrier(n, carrier)
    index = {pair: bit for bit, pair in enumerate(edges)}
    parsed = []
    for raw in constraints:
        constraint = _constraint(raw, int(n))
        if constraint["event"] not in index or constraint["condition"] not in index:
            raise ValueError("a constraint names an edge outside the carrier")
        parsed.append(constraint)
    size = 1 << len(edges)
    width = len(edges)
    limit = int(np.iinfo(np.int64).max)
    weights = np.zeros((size, width), dtype=np.int64)
    active = np.zeros(size, dtype=np.int32)
    for state in range(size):
        for edge in range(width):
            prohibited = False
            factor = 1
            for constraint in parsed:
                if index[constraint["event"]] != edge:
                    continue
                if not _guard(
                    state,
                    index[constraint["condition"]],
                    edge,
                    constraint["polarity"],
                    constraint["action"],
                ):
                    continue
                active[state] += 1
                if constraint["effect"] == "prohibit":
                    prohibited = True
                else:
                    factor *= int(constraint["factor"])
            value = 0 if prohibited else baseline * factor
            if value > limit:
                raise OverflowError("weight product does not fit in int64")
            weights[state, edge] = value
    return weights, edges, parsed, active


def weight_table_hash(weights: np.ndarray) -> str:
    """sha256 of a canonical JSON integer table. Not a NumPy byte dump."""
    rows = [[int(value) for value in row] for row in weights.tolist()]
    blob = json.dumps(rows, separators=(",", ":"), ensure_ascii=True).encode("ascii")
    return hashlib.sha256(blob).hexdigest()


def empirical_bit_independent(weights: np.ndarray) -> bool:
    """True when each column ignores the bit that column toggles."""
    size, width = weights.shape
    states = np.arange(size)
    for edge in range(width):
        flipped = states ^ (1 << edge)
        if not np.array_equal(weights[:, edge], weights[flipped, edge]):
            return False
    return True


def present_component_count(n: int, edges: list[tuple[int, int]], state: int) -> int:
    """Components of the present edges. Isolated nodes count. Instrument plus state."""
    parent = list(range(int(n)))

    def find(node: int) -> int:
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    for bit, (left, right) in enumerate(edges):
        if (state >> bit) & 1:
            root_left = find(left)
            root_right = find(right)
            if root_left != root_right:
                parent[root_right] = root_left
    return len({find(node) for node in range(int(n))})


def _bookkeeping(edges, parsed, active, weights) -> dict:
    positive_k = [1 + _literals(item) for item in parsed if item["effect"] == "multiply"]
    prohibit_literals = [_literals(item) for item in parsed if item["effect"] == "prohibit"]
    j_positive = sum(item["effect"] == "multiply" for item in parsed)
    j_prohibit = sum(item["effect"] == "prohibit" for item in parsed)
    size = int(weights.shape[0])
    zero_active = int(np.count_nonzero(active == 0))
    per_event: dict[tuple[int, int], int] = {}
    for item in parsed:
        per_event[item["event"]] = per_event.get(item["event"], 0) + 1
    features = []
    for item in parsed:
        literals = _literals(item)
        feature = {
            "action": item["action"],
            "condition": [item["condition"][0], item["condition"][1]],
            "effect": item["effect"],
            "event": [item["event"][0], item["event"][1]],
            "literals": literals,
            "polarity": item["polarity"],
        }
        if item["effect"] == "multiply":
            feature["factor"] = item["factor"]
            feature["positive_k"] = 1 + literals
        features.append(feature)
    return {
        "declared_cardinality": len(parsed),
        "distinct_events": len(per_event),
        "features": features,
        "j_positive": j_positive,
        "j_prohibit": j_prohibit,
        "max_active_in_state": int(active.max()) if size else 0,
        "max_constraints_on_one_event": max(per_event.values()) if per_event else 0,
        "max_positive_k": max(positive_k) if positive_k else 0,
        "max_prohibit_literals": max(prohibit_literals) if prohibit_literals else 0,
        "states_with_zero_active": zero_active,
        "zero_active_fraction": fraction_payload(Fraction(zero_active, size)),
    }


def _ablate(n, carrier, constraints, baseline, target: np.ndarray):
    """Smallest sublist with the same table, and how many singletons matter.

    ``effective_cardinality`` is the size of a smallest sublist that reproduces
    the table. Two copies of one prohibit therefore have effective cardinality 1.
    ``removal_sensitive_count`` is how many entries change the table when that
    one entry is deleted. Both copies are individually redundant, so that count
    is 0. Above 16 declared constraints the exact search is not run.
    """
    count = len(constraints)
    if count > MAX_EXACT_ABLATION:
        return None, None
    effective = None
    for width in range(count + 1):
        for chosen in combinations(range(count), width):
            subset = [constraints[index] for index in chosen]
            weights = compile_weight_table(n, carrier, subset, baseline)
            if np.array_equal(weights, target):
                effective = width
                break
        if effective is not None:
            break
    if effective is None:
        raise RuntimeError("the full constraint list did not reproduce its table")
    sensitive = 0
    for index in range(count):
        subset = [item for position, item in enumerate(constraints) if position != index]
        weights = compile_weight_table(n, carrier, subset, baseline)
        if not np.array_equal(weights, target):
            sensitive += 1
    return effective, sensitive


def _dependency(edges, parsed) -> dict:
    """Syntax of the rule list. Not a cascade observed in the chain."""
    index = {pair: bit for bit, pair in enumerate(edges)}
    adjacency: dict[int, set[int]] = {bit: set() for bit in range(len(edges))}
    involved: set[int] = set()
    for item in parsed:
        source = index[item["condition"]]
        target = index[item["event"]]
        adjacency[source].add(target)
        involved.add(source)
        involved.add(target)
    color = [0] * len(edges)
    has_cycle = False

    def paint(node: int) -> None:
        nonlocal has_cycle
        color[node] = 1
        for nxt in adjacency[node]:
            if color[nxt] == 1:
                has_cycle = True
            elif color[nxt] == 0:
                paint(nxt)
        color[node] = 2

    for node in range(len(edges)):
        if color[node] == 0:
            paint(node)
    payload = {
        "has_cycle": has_cycle,
        "longest_simple_path_edges": None,
        "method": "not_computed",
        "note": "imposed rule text, not an observed dynamical cascade",
    }
    if len(involved) > MAX_EXACT_DEPENDENCY_NODES:
        return payload
    best = 0

    def walk(node: int, seen: set[int]) -> None:
        nonlocal best
        best = max(best, len(seen) - 1)
        for nxt in adjacency[node]:
            if nxt not in seen:
                seen.add(nxt)
                walk(nxt, seen)
                seen.remove(nxt)

    for node in involved:
        walk(node, {node})
    payload["longest_simple_path_edges"] = best
    payload["method"] = "exact_simple_path"
    return payload


def compile_model(n: int, carrier, constraints: list, baseline: int = 1) -> dict:
    weights, edges, parsed, active = _compile(n, carrier, constraints, baseline)
    _kind_edges, kind = resolve_carrier(n, carrier)
    if _kind_edges != edges:
        raise RuntimeError("carrier resolution drifted")
    book = _bookkeeping(edges, parsed, active, weights)
    effective, sensitive = _ablate(n, carrier, constraints, baseline, weights)
    book["effective_cardinality"] = effective
    book["removal_sensitive_count"] = sensitive
    book["effective_method"] = EFFECTIVE_METHOD if effective is not None else "not_computed_above_16"
    full = (1 << len(edges)) - 1
    return {
        "action_bit_independent": all(item["action"] == "either" for item in parsed),
        "active": active,
        "baseline": baseline,
        "bookkeeping": book,
        "carrier_components": present_component_count(int(n), edges, full),
        "carrier_edges": edges,
        "carrier_kind": kind,
        "empirical_bit_independent": empirical_bit_independent(weights),
        "imposed_rule_dependency": _dependency(edges, parsed),
        "n": int(n),
        "weights": weights,
    }


def _means_from_mass(n, edges, mass: np.ndarray) -> dict:
    size, width = mass.shape[0], len(edges)
    total = sum(int(value) for value in mass.tolist())
    if total <= 0:
        raise RuntimeError("occupation mass is zero")
    present = [sum((state >> edge) & 1 for edge in range(width)) for state in range(size)]
    components = [present_component_count(n, edges, state) for state in range(size)]
    present_num = sum(present[state] * int(mass[state]) for state in range(size))
    component_num = sum(components[state] * int(mass[state]) for state in range(size))
    presence = []
    for edge in range(width):
        presence_num = sum(int(mass[state]) for state in range(size) if (state >> edge) & 1)
        presence.append(fraction_payload(Fraction(presence_num, total)))
    return {
        "edge_presence": presence,
        "mean_components": fraction_payload(Fraction(component_num, total)),
        "mean_present_edges": fraction_payload(Fraction(present_num, total)),
    }


def solve_stationary(weights: np.ndarray, tolerance: float, cross: float, max_iter: int, dense_max: int) -> dict:
    """Two parity-balanced starts, plus a dense solve when the state count fits."""
    uniform = stationary_balanced(weights, "uniform", tolerance, max_iter)
    empty = stationary_balanced(weights, "empty", tolerance, max_iter)
    gap = float(np.abs(uniform["distribution"] - empty["distribution"]).sum())
    if max(uniform["image_gap"], empty["image_gap"]) > cross:
        uniform["converged"] = False
        empty["converged"] = False
    dense_gap = None
    if weights.shape[0] <= dense_max:
        dense = stationary_dense(weights)
        dense_gap = float(np.abs(dense - uniform["distribution"]).sum())
    converged = bool(uniform["converged"] and empty["converged"] and gap <= cross)
    if dense_gap is not None:
        converged = converged and dense_gap <= cross
    return {
        "converged": converged,
        "cross_check": "second_start_and_dense_solve_when_states_fit",
        "dense_l1": dense_gap,
        "distribution": uniform["distribution"] if converged else None,
        "empty_iterations": empty["iterations"],
        "empty_residual": empty["residual"],
        "method": "stationary_balanced",
        "start_l1": gap,
        "uniform_iterations": uniform["iterations"],
        "uniform_residual": uniform["residual"],
    }


def occupation_report(model: dict, tolerance: float, cross: float, max_iter: int, dense_max: int) -> dict:
    """Unique occupation only. Several recurrent classes are a result, not a failure."""
    weights = model["weights"]
    classes = recurrent_class_count(weights)
    if classes["recurrent_classes"] != 1:
        return {
            "classes": classes,
            "occupation": {
                "method": None,
                "reason": "recurrent_classes",
                "recurrent_classes": classes["recurrent_classes"],
                "status": "not_unique",
            },
        }
    totals = weights.sum(axis=1)
    minimum = int(totals.min()) if totals.size else 0
    if model["empirical_bit_independent"] and minimum > 0:
        means = _means_from_mass(model["n"], model["carrier_edges"], totals)
        means["method"] = "integer_pi_proportional_to_total_weight"
        means["reason"] = "bit_independent_positive_total_weight_one_recurrent_class"
        means["status"] = "unique"
        means["unnormalized_total_weight"] = [int(value) for value in totals.tolist()]
        return {"classes": classes, "occupation": means}
    solved = solve_stationary(weights, tolerance, cross, max_iter, dense_max)
    if not solved["converged"] or solved["distribution"] is None:
        return {
            "classes": classes,
            "occupation": {
                "dense_l1": solved["dense_l1"],
                "empty_iterations": solved["empty_iterations"],
                "empty_residual": solved["empty_residual"],
                "method": solved["method"],
                "reason": "solver_disagreement_or_residual",
                "start_l1": solved["start_l1"],
                "status": "unresolved",
                "uniform_iterations": solved["uniform_iterations"],
                "uniform_residual": solved["uniform_residual"],
            },
        }
    distribution = solved["distribution"]
    size = distribution.shape[0]
    width = len(model["carrier_edges"])
    states = np.arange(size)
    present = np.zeros(size, dtype=np.float64)
    for edge in range(width):
        present += ((states >> edge) & 1).astype(np.float64)
    components = np.array(
        [present_component_count(model["n"], model["carrier_edges"], int(state)) for state in states],
        dtype=np.float64,
    )
    presence = []
    for edge in range(width):
        mask = ((states >> edge) & 1) == 1
        presence.append(float(distribution[mask].sum()))
    return {
        "classes": classes,
        "occupation": {
            "cross_check": solved["cross_check"],
            "dense_l1": solved["dense_l1"],
            "distribution": [float(value) for value in distribution.tolist()],
            "edge_presence": presence,
            "empty_iterations": solved["empty_iterations"],
            "empty_residual": solved["empty_residual"],
            "mean_components": float(np.dot(components, distribution)),
            "mean_present_edges": float(np.dot(present, distribution)),
            "method": solved["method"],
            "numerical_limitation": "float64 stationary_balanced, cross-checked",
            "reason": "state_dependent_weights_unique_class",
            "start_l1": solved["start_l1"],
            "status": "unique",
            "uniform_iterations": solved["uniform_iterations"],
            "uniform_residual": solved["uniform_residual"],
        },
    }


def support_report(weights: np.ndarray) -> dict:
    classes = recurrent_class_count(weights)
    positive = int(np.count_nonzero(weights > 0))
    zeros = int(np.count_nonzero(weights == 0))
    return {
        "classes": classes,
        "deadlock_states": classes["deadlock_states"],
        "halt_completion": HALT_COMPLETION,
        "positive_transitions": positive,
        "recurrent_classes": classes["recurrent_classes"],
        "zero_cells": zeros,
    }
