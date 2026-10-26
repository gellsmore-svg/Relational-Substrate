"""Exact switching-link/compiler/refinement checks; no production-engine imports."""

from collections import Counter, deque
from fractions import Fraction
from itertools import product
from math import prod
import json


METHOD_ID = "switching-link-analysis-0.1.0"
CHANNELS = ("left", "right", "joint", "switch")
MAX_GLOBAL_STATES = 32
MAX_REFINEMENT_BLOCKS = 8


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_actor(matrix):
    require(isinstance(matrix, list) and 1 <= len(matrix) <= 4, "invalid actor size")
    n = len(matrix)
    require(all(isinstance(row, list) and len(row) == n for row in matrix), "invalid actor matrix")
    require(all(type(value) is int and value >= 0 for row in matrix for value in row), "invalid actor weight")
    require(all(matrix[s][s] == 0 for s in range(n)), "actor self-loops are outside this grammar")


def network(left, right, switch=(1, 1)):
    validate_actor(left)
    validate_actor(right)
    require(len(switch) == 2 and all(type(x) is int and x >= 0 for x in switch), "invalid switch weights")
    require(2 * len(left) * len(right) <= MAX_GLOBAL_STATES, "global state cap exceeded")
    return {"left": left, "right": right, "switch": list(switch)}


def index(s, t, mode, right_size):
    return 2 * (s * right_size + t) + mode


def direct_weights(model):
    a, b, switch = model["left"], model["right"], model["switch"]
    size = 2 * len(a) * len(b)
    result = {label: [[0] * size for _ in range(size)] for label in CHANNELS}
    for s, t, mode in product(range(len(a)), range(len(b)), range(2)):
        source = index(s, t, mode, len(b))
        if mode == 0:
            for u, weight in enumerate(a[s]):
                result["left"][source][index(u, t, mode, len(b))] += weight
            for v, weight in enumerate(b[t]):
                result["right"][source][index(s, v, mode, len(b))] += weight
        else:
            for u, v in product(range(len(a)), range(len(b))):
                result["joint"][source][index(u, v, mode, len(b))] += a[s][u] * b[t][v]
        result["switch"][source][source ^ 1] += switch[mode]
    return nonzero_matrices(result)


def nonzero_matrices(matrices):
    return {label: matrix for label, matrix in matrices.items() if any(any(row) for row in matrix)}


def event(label, source, target, weight=1):
    return {"label": label, "source": source, "target": target, "weight": weight}


def compile_protocol(model):
    """Expand actors into four fixed shared channels, with explicit passive events."""
    parts = []
    for matrix, active, passive in ((model["left"], ("left", "joint"), ("right", "switch")),
                                    (model["right"], ("right", "joint"), ("left", "switch"))):
        records = [event(label, s, u, weight) for s, row in enumerate(matrix)
                   for u, weight in enumerate(row) if weight for label in active]
        records.extend(event(label, s, s) for s in range(len(matrix)) for label in passive)
        parts.append({"n_states": len(matrix), "handshake": list(CHANNELS), "events": records})
    records = [event("left", 0, 0), event("right", 0, 0), event("joint", 1, 1),
               event("switch", 0, 1, model["switch"][0]), event("switch", 1, 0, model["switch"][1])]
    parts.append({"n_states": 2, "handshake": list(CHANNELS), "events": records})
    return parts


def flatten(point, sizes):
    result = 0
    for value, size in zip(point, sizes):
        result = result * size + value
    return result


def matched_protocol_weights(parts):
    """Independent n-ary event matching, without reading the original link policy."""
    require(parts and all(set(p["handshake"]) == set(CHANNELS) for p in parts), "incompatible protocol")
    sizes = [p["n_states"] for p in parts]
    require(all(type(n) is int and n > 0 for n in sizes) and prod(sizes) <= MAX_GLOBAL_STATES,
            "invalid protocol size")
    size = prod(sizes)
    result = {label: [[0] * size for _ in range(size)] for label in CHANNELS}
    for source in product(*(range(n) for n in sizes)):
        for label in CHANNELS:
            choices = [[e for e in part["events"] if e["label"] == label and e["source"] == state and e["weight"]]
                       for part, state in zip(parts, source)]
            for records in product(*choices):
                target = tuple(e["target"] for e in records)
                result[label][flatten(source, sizes)][flatten(target, sizes)] += prod(e["weight"] for e in records)
    return nonzero_matrices(result)


def normalise(matrices, size):
    result = []
    for source in range(size):
        row = [sum(matrix[source][target] for matrix in matrices.values()) for target in range(size)]
        total = sum(row)
        result.append([Fraction(value, total) for value in row] if total else
                      [Fraction(source == target) for target in range(size)])
    return result


def observation_count(size, labels):
    require(len(labels) == size and all(type(x) is int and x >= 0 for x in labels), "invalid observation")
    count = len(set(labels))
    require(set(labels) == set(range(count)), "noncontiguous observation")
    return count


def block_report(matrix, labels):
    count = observation_count(len(matrix), labels)
    first = {}
    for source, block in enumerate(labels):
        row = [Fraction(0)] * count
        for target, value in enumerate(matrix[source]):
            row[labels[target]] += value
        if block in first and first[block][1] != row:
            return {"exact": False, "rows": None, "witness": {"states": [first[block][0], source],
                    "first_row": first[block][1], "second_row": row}}
        first[block] = (source, row)
    return {"exact": True, "rows": [first[k][1] for k in range(count)], "witness": None}


def active_mask(model):
    return sum(1 << (s * len(model["right"]) + t) for s in range(len(model["left"]))
               for t in range(len(model["right"])) if sum(model["left"][s]) + sum(model["right"][t]) > 0)


def refinement_labels(blocks, mask):
    require(type(blocks) is int and blocks > 0 and type(mask) is int and 0 <= mask < 1 << blocks, "invalid refinement")
    labels, next_label = [], 0
    for block in range(blocks):
        split = bool(mask & (1 << block))
        labels.extend([next_label, next_label + int(split)])
        next_label += 1 + int(split)
    return labels


def exhaustive_refinements(matrix, blocks):
    require(blocks <= MAX_REFINEMENT_BLOCKS, "refinement enumeration cap exceeded")
    exact = [mask for mask in range(1 << blocks) if block_report(matrix, refinement_labels(blocks, mask))["exact"]]
    minimal = [mask for mask in exact if not any(other != mask and other & mask == other for other in exact)]
    return {"checks": 1 << blocks, "exact_mask_count": len(exact), "minimal_masks": minimal}


def bipartite_support(matrix):
    adjacency = [set() for _ in matrix]
    for s, row in enumerate(matrix):
        for t, weight in enumerate(row):
            if s != t and weight:
                adjacency[s].add(t)
                adjacency[t].add(s)
    colour = {}
    for start in range(len(matrix)):
        if start in colour:
            continue
        colour[start] = 0
        queue = deque([start])
        while queue:
            source = queue.popleft()
            for target in adjacency[source]:
                if target in colour and colour[target] == colour[source]:
                    return False
                if target not in colour:
                    colour[target] = 1 - colour[source]
                    queue.append(target)
    return True


def frozen_binary_controls(model):
    require(len(model["left"]) == len(model["right"]) == 2 and model["switch"] == [0, 0], "not a frozen binary model")
    full = normalise(direct_weights(model), 8)
    result = []
    for mode in range(2):
        points = [index(s, t, mode, 2) for s, t in product(range(2), repeat=2)]
        require(all(sum(full[source][target] for target in points) == 1 for source in points), "frozen mode leaks")
        encoded = [2 * s + (t if mode == 0 else s ^ t) for s, t in product(range(2), repeat=2)]
        require(len(set(encoded)) == 4, "frozen encoding not injective")
        require(all((encoded[s] ^ encoded[t]).bit_count() == 1 for s in range(4) for t in range(4)
                    if s != t and full[points[s]][points[t]]), "frozen mode is not one-bit support")
        result.append({"mode": mode, "encoded_actor_states": encoded, "invariant": True, "one_bit_support": True})
    return result


def serialise(value):
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, dict):
        return {key: serialise(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialise(item) for item in value]
    return value


def run_checks():
    systems = refinement_checks = exact_refinements = actor_exact = 0
    histogram = Counter()
    for a01, a10, b01, b10, gamma0, gamma1 in product(range(3), repeat=6):
        model = network([[0, a01], [a10, 0]], [[0, b01], [b10, 0]], (gamma0, gamma1))
        weights = direct_weights(model)
        require(weights == matched_protocol_weights(compile_protocol(model)), "guarded/compiler raw weights differ")
        matrix = normalise(weights, 8)
        proposed = active_mask(model)
        brute = exhaustive_refinements(matrix, 4)
        require(brute["minimal_masks"] == [proposed], "coarsest exact refinement disagreement")
        labels = refinement_labels(4, proposed)
        require(block_report(matrix, labels)["exact"], "proposed refinement is not exact")
        actor_view = block_report(matrix, [i // 2 for i in range(8)])
        require(actor_view["exact"] == (proposed == 0), "actor-only closure criterion disagreement")
        systems += 1
        refinement_checks += brute["checks"]
        exact_refinements += brute["exact_mask_count"]
        actor_exact += int(actor_view["exact"])
        histogram[len(set(labels))] += 1
    nonbinary = network([[0, 1, 0], [0, 0, 2], [1, 0, 0]], [[0, 2], [1, 0]], (1, 2))
    require(direct_weights(nonbinary) == matched_protocol_weights(compile_protocol(nonbinary)), "nonbinary compiler failure")
    require(exhaustive_refinements(normalise(direct_weights(nonbinary), 12), 6)["minimal_masks"] == [63], "nonbinary refinement failure")
    active = network([[0, 1], [1, 0]], [[0, 1], [1, 0]])
    active_kernel = normalise(direct_weights(active), 8)
    cycle = [0, 4, 6, 7, 1, 0]
    require(all(active_kernel[s][t] > 0 for s, t in zip(cycle, cycle[1:])), "five-cycle edge missing")
    require(not bipartite_support(active_kernel), "switching odd-cycle control is bipartite")
    frozen = network(active["left"], active["right"], (0, 0))
    partial = network([[0, 1], [0, 0]], [[0, 1], [0, 0]])
    partial_labels = refinement_labels(4, active_mask(partial))
    null = network([[0, 0], [0, 0]], [[0, 0], [0, 0]], (1, 2))
    return serialise({"method": METHOD_ID, "evidence_type": "analytic proof and independent software validation",
                      "scientific_worker_invocations": 0, "new_atlas_cells": 0,
                      "binary_networks": systems, "raw_compiler_checks": systems,
                      "refinement_checks": refinement_checks, "exact_refinement_masks": exact_refinements,
                      "actor_only_exact_cases": actor_exact, "coarsest_block_count_histogram": dict(sorted(histogram.items())),
                      "nonbinary_compiler_and_refinement": "verified",
                      "active_actor_view": block_report(active_kernel, [i // 2 for i in range(8)]),
                      "partial_activity": {"labels": partial_labels, "coarsest_blocks": len(set(partial_labels)),
                                           "observation": block_report(normalise(direct_weights(partial), 8), partial_labels)},
                      "inactive_actors": block_report(normalise(direct_weights(null), 8), [i // 2 for i in range(8)]),
                      "directed_five_cycle": cycle, "switching_support_bipartite": False,
                      "frozen_binary_controls": frozen_binary_controls(frozen), "status": "verified"})


if __name__ == "__main__":
    print(json.dumps(run_checks(), indent=2))
