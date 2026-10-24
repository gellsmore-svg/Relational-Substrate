"""Current-state prohibit and multiply on one carrier.

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
J counts declared features. Declared cardinality counts the list, including
duplicates. An incident-neighbour predicate is still one declared feature.
Its conjunction expansion has a separate J.

The opening condition reads one designated carrier bit. The incident-neighbour
condition reads the current presence of every other carrier edge that shares
an endpoint with the event. Both are current-state weights on one toggle.
"""

from __future__ import annotations

import hashlib
import json
import math
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
INCIDENT_GRAMMAR_ID = "incident-neighbour-v1"
MIXED_GRAMMAR_ID = "opening-plus-incident-v1"
KERNEL_METHOD = "row_gcd_halt_self_loop"
STRUCTURE_METHOD = "present_degree_components_cycle"
EFFECTS = ("prohibit", "multiply")
ACTIONS = ("either", "form", "dissolve")
POLARITIES = ("present", "absent")
CONDITION_KINDS = ("designated_edge", "incident_neighbour")
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
        raise ValueError("a constraint needs a when clause")
    kind = when.get("kind", "designated_edge")
    if kind not in CONDITION_KINDS:
        raise ValueError(f"unknown condition kind {kind}")
    polarity = when.get("polarity")
    if polarity not in POLARITIES:
        raise ValueError(f"unknown polarity {polarity}")
    factor = None
    if effect == "multiply":
        raw_factor = raw.get("factor")
        if isinstance(raw_factor, bool) or not isinstance(raw_factor, int) or raw_factor < 2:
            raise ValueError("a multiply factor must be an integer >= 2")
        factor = raw_factor
    elif "factor" in raw:
        raise ValueError("a prohibit does not take a factor")
    if kind == "incident_neighbour":
        if "edge" in when:
            raise ValueError("an incident-neighbour condition does not name a designated edge")
        return {
            "effect": effect,
            "action": action,
            "event": event,
            "kind": kind,
            "condition": None,
            "polarity": polarity,
            "factor": factor,
        }
    condition = _pair(when.get("edge"), n)
    if condition == event:
        raise ValueError("the condition edge must differ from the event edge")
    return {
        "effect": effect,
        "action": action,
        "event": event,
        "kind": "designated_edge",
        "condition": condition,
        "polarity": polarity,
        "factor": factor,
    }


def _literals(constraint: dict) -> int:
    """Condition, plus the event bit when the action is form or dissolve."""
    return 2 if constraint["action"] in ("form", "dissolve") else 1


def _incident_bits(edges: list[tuple[int, int]], event_bit: int) -> list[int]:
    """Other carrier edges that share an endpoint with the event. Carrier order."""
    left, right = edges[event_bit]
    bits = []
    for bit, pair in enumerate(edges):
        if bit == event_bit:
            continue
        if pair[0] in (left, right) or pair[1] in (left, right):
            bits.append(bit)
    return bits


def _action_holds(state: int, event_bit: int, action: str) -> bool:
    event_on = ((state >> event_bit) & 1) == 1
    if action == "form":
        return not event_on
    if action == "dissolve":
        return event_on
    return True


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


def _incident_guard(state: int, bits: list[int], event_bit: int, polarity: str, action: str) -> bool:
    """True when the current incident neighbourhood has the requested polarity."""
    any_present = any((state >> bit) & 1 for bit in bits)
    if polarity == "present" and not any_present:
        return False
    if polarity == "absent" and any_present:
        return False
    return _action_holds(state, event_bit, action)


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
        if constraint["event"] not in index:
            raise ValueError("a constraint names an edge outside the carrier")
        if constraint["kind"] == "designated_edge" and constraint["condition"] not in index:
            raise ValueError("a constraint names an edge outside the carrier")
        if constraint["kind"] == "incident_neighbour":
            bits = _incident_bits(edges, index[constraint["event"]])
            constraint["incident_bits"] = bits
            constraint["incident_edges"] = len(bits)
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
                if constraint["kind"] == "designated_edge":
                    matched = _guard(
                        state,
                        index[constraint["condition"]],
                        edge,
                        constraint["polarity"],
                        constraint["action"],
                    )
                else:
                    matched = _incident_guard(
                        state,
                        constraint["incident_bits"],
                        edge,
                        constraint["polarity"],
                        constraint["action"],
                    )
                if not matched:
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


def reduce_weight_table(weights: np.ndarray) -> np.ndarray:
    """Divide each positive row by its gcd. A zero row stays zero.

    This is the exact fingerprint of ``halt_self_loop`` probabilities.
    It is not a continuous-time rate, and it does not compare different shapes.
    """
    if weights.size and int(weights.min()) < 0:
        raise ValueError("weights must be non-negative")
    reduced = np.zeros_like(weights)
    for state in range(weights.shape[0]):
        row = [int(value) for value in weights[state].tolist()]
        if not any(value > 0 for value in row):
            continue
        divisor = 0
        for value in row:
            divisor = math.gcd(divisor, value)
        if divisor <= 0:
            raise RuntimeError("a positive row had no positive divisor")
        reduced[state] = [value // divisor for value in row]
    return reduced


def kernel_fingerprint(weights: np.ndarray) -> str:
    return weight_table_hash(reduce_weight_table(weights))


def kernels_equal(left: np.ndarray, right: np.ndarray) -> bool:
    if left.shape != right.shape:
        return False
    return bool(np.array_equal(reduce_weight_table(left), reduce_weight_table(right)))


def _expansion(constraint: dict) -> dict:
    """Conjunction cost of one incident predicate. Not the declared J.

    A present-polarity disjunction expands to one exact minterm for each
    nonempty subset of the incident edges, because a product of overlapping
    features would multiply the factor more than once. An absent-polarity
    condition is one conjunction of negative literals. A prohibit expansion
    is the existing hard zero, not the positive CL-T12 construction.
    """
    width = int(constraint["incident_edges"])
    action_literals = 1 if constraint["action"] in ("form", "dissolve") else 0
    if constraint["effect"] == "prohibit":
        family = "prohibit features, not the positive CL-T12 construction"
    else:
        family = "positive conjunction features inside CL-T12"
    if width == 0 and constraint["polarity"] == "present":
        return {
            "expansion_j": 0,
            "expansion_k": 0,
            "expansion_note": "empty neighbourhood; the present polarity never matches. " + family,
        }
    if width == 0 and constraint["polarity"] == "absent":
        return {
            "expansion_j": 1,
            "expansion_k": 1 + action_literals,
            "expansion_note": "empty neighbourhood; the absent polarity matches in every state. " + family,
        }
    if constraint["polarity"] == "present":
        return {
            "expansion_j": (1 << width) - 1,
            "expansion_k": 1 + width + action_literals,
            "expansion_note": "exact minterms of the disjunction. Declared J stays 1. " + family,
        }
    return {
        "expansion_j": 1,
        "expansion_k": 1 + width + action_literals,
        "expansion_note": "one conjunction of the absent incident literals. " + family,
    }


def grammar_of(parsed: list) -> str:
    kinds = {item["kind"] for item in parsed}
    if kinds <= {"designated_edge"}:
        return GRAMMAR_ID
    if kinds == {"incident_neighbour"}:
        return INCIDENT_GRAMMAR_ID
    return MIXED_GRAMMAR_ID


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


def present_graph(n: int, edges: list[tuple[int, int]], state: int) -> dict:
    """Degree sequence, component sizes, and a cycle flag of the present graph.

    Degree sequences and component sizes are non-increasing. Isolated nodes
    are included. A forest state has ``components == n - present edges``.
    """
    count = int(n)
    degree = [0] * count
    parent = list(range(count))

    def find(node: int) -> int:
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def union(left: int, right: int) -> None:
        root_left = find(left)
        root_right = find(right)
        if root_left != root_right:
            parent[root_right] = root_left

    present = 0
    for bit, (left, right) in enumerate(edges):
        if (state >> bit) & 1:
            present += 1
            degree[left] += 1
            degree[right] += 1
            union(left, right)
    node_tally: dict[int, int] = {}
    edge_tally: dict[int, int] = {}
    for node in range(count):
        root = find(node)
        node_tally[root] = node_tally.get(root, 0) + 1
    for bit, (left, _right) in enumerate(edges):
        if (state >> bit) & 1:
            root = find(left)
            edge_tally[root] = edge_tally.get(root, 0) + 1
    has_cycle = any(edge_tally.get(root, 0) > nodes - 1 for root, nodes in node_tally.items())
    return {
        "component_sizes": sorted(node_tally.values(), reverse=True),
        "components": len(node_tally),
        "degree_sequence": sorted(degree, reverse=True),
        "has_cycle": has_cycle,
        "present_edges": present,
    }


def structure_hash(n: int, edges: list[tuple[int, int]]) -> str:
    rows = [present_graph(n, edges, state) for state in range(1 << len(edges))]
    blob = json.dumps(rows, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")
    return hashlib.sha256(blob).hexdigest()


def _bookkeeping(edges, parsed, active, weights) -> dict:
    positive_k = [
        1 + _literals(item)
        for item in parsed
        if item["effect"] == "multiply" and item["kind"] == "designated_edge"
    ]
    prohibit_literals = [
        _literals(item)
        for item in parsed
        if item["effect"] == "prohibit" and item["kind"] == "designated_edge"
    ]
    j_positive = sum(item["effect"] == "multiply" for item in parsed)
    j_prohibit = sum(item["effect"] == "prohibit" for item in parsed)
    size = int(weights.shape[0])
    zero_active = int(np.count_nonzero(active == 0))
    per_event: dict[tuple[int, int], int] = {}
    for item in parsed:
        per_event[item["event"]] = per_event.get(item["event"], 0) + 1
    features = []
    expansion_j_total = 0
    expansion_ks = []
    incident_widths = []
    for item in parsed:
        feature = {
            "action": item["action"],
            "condition_kind": item["kind"],
            "effect": item["effect"],
            "event": [item["event"][0], item["event"][1]],
            "polarity": item["polarity"],
        }
        if item["kind"] == "designated_edge":
            literals = _literals(item)
            feature["condition"] = [item["condition"][0], item["condition"][1]]
            feature["literals"] = literals
            if item["effect"] == "multiply":
                feature["factor"] = item["factor"]
                feature["positive_k"] = 1 + literals
        else:
            expansion = _expansion(item)
            incident_widths.append(item["incident_edges"])
            expansion_j_total += expansion["expansion_j"]
            if expansion["expansion_k"]:
                expansion_ks.append(expansion["expansion_k"])
            feature["incident_edges"] = item["incident_edges"]
            feature.update(expansion)
            if item["effect"] == "multiply":
                feature["factor"] = item["factor"]
        features.append(feature)
    return {
        "declared_cardinality": len(parsed),
        "distinct_events": len(per_event),
        "features": features,
        "j_positive": j_positive,
        "j_prohibit": j_prohibit,
        "max_active_in_state": int(active.max()) if size else 0,
        "max_constraints_on_one_event": max(per_event.values()) if per_event else 0,
        "expansion_j_total": expansion_j_total,
        "max_expansion_k": max(expansion_ks) if expansion_ks else 0,
        "max_incident_edges": max(incident_widths) if incident_widths else 0,
        "max_positive_k": max(positive_k) if positive_k else 0,
        "max_prohibit_literals": max(prohibit_literals) if prohibit_literals else 0,
        "states_with_zero_active": zero_active,
        "zero_active_fraction": fraction_payload(Fraction(zero_active, size)),
    }


def _ablate(n, carrier, constraints, baseline, target: np.ndarray):
    """Smallest sublists for the raw table and for the halt_self_loop kernel.

    ``effective_cardinality`` is the size of a smallest sublist that reproduces
    the integer table. ``kernel_effective_cardinality`` is the same search for
    the row-gcd kernel. A sublist can match the kernel and miss the raw table.
    ``removal_sensitive_count`` counts entries whose deletion changes the raw
    table. ``kernel_removal_sensitive_count`` counts entries whose deletion
    changes the kernel. Above 16 declared constraints neither search is run.
    """
    count = len(constraints)
    empty = {
        "effective_cardinality": None,
        "kernel_effective_cardinality": None,
        "kernel_removal_sensitive_count": None,
        "removal_sensitive_count": None,
    }
    if count > MAX_EXACT_ABLATION:
        return empty
    target_kernel = reduce_weight_table(target)
    effective = None
    kernel_effective = None
    for width in range(count + 1):
        if effective is not None and kernel_effective is not None:
            break
        for chosen in combinations(range(count), width):
            if effective is not None and kernel_effective is not None:
                break
            subset = [constraints[index] for index in chosen]
            weights = compile_weight_table(n, carrier, subset, baseline)
            if effective is None and np.array_equal(weights, target):
                effective = width
            if kernel_effective is None and np.array_equal(reduce_weight_table(weights), target_kernel):
                kernel_effective = width
    if effective is None or kernel_effective is None:
        raise RuntimeError("the full constraint list did not reproduce its table")
    sensitive = 0
    kernel_sensitive = 0
    for index in range(count):
        subset = [item for position, item in enumerate(constraints) if position != index]
        weights = compile_weight_table(n, carrier, subset, baseline)
        if not np.array_equal(weights, target):
            sensitive += 1
        if not np.array_equal(reduce_weight_table(weights), target_kernel):
            kernel_sensitive += 1
    return {
        "effective_cardinality": effective,
        "kernel_effective_cardinality": kernel_effective,
        "kernel_removal_sensitive_count": kernel_sensitive,
        "removal_sensitive_count": sensitive,
    }


def _dependency(edges, parsed) -> dict:
    """Syntax of the rule list. Not a cascade observed in the chain."""
    index = {pair: bit for bit, pair in enumerate(edges)}
    adjacency: dict[int, set[int]] = {bit: set() for bit in range(len(edges))}
    involved: set[int] = set()
    for item in parsed:
        target = index[item["event"]]
        if item["kind"] == "designated_edge":
            sources = [index[item["condition"]]]
        else:
            sources = list(item["incident_bits"])
        involved.add(target)
        for source in sources:
            adjacency[source].add(target)
            involved.add(source)
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
    ablation = _ablate(n, carrier, constraints, baseline, weights)
    book.update(ablation)
    book["effective_method"] = (
        EFFECTIVE_METHOD if ablation["effective_cardinality"] is not None else "not_computed_above_16"
    )
    book["kernel_ablation_method"] = (
        EFFECTIVE_METHOD if ablation["kernel_effective_cardinality"] is not None else "not_computed_above_16"
    )
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
        "grammar_id": grammar_of(parsed),
        "imposed_rule_dependency": _dependency(edges, parsed),
        "kernel_sha256": kernel_fingerprint(weights),
        "n": int(n),
        "structure_sha256": structure_hash(int(n), edges),
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
