"""Check a declared weighted synchronization product; no RRC worker imports."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
import json


METHOD_ID = "label-sync-analysis-0.1.0"
MAX_STATES = 32
MAX_EVENTS = 2048


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def component(size: int, events: list[dict], handshake=("sync",)) -> dict:
    result = {"n_states": size, "handshake": list(handshake), "events": events}
    validate(result)
    return result


def event(label: str, source: int, target: int, weight: int = 1) -> dict:
    return {"label": label, "source": source, "target": target, "weight": weight}


def validate(system: dict) -> None:
    size = system["n_states"]
    require(type(size) is int and 1 <= size <= MAX_STATES, "invalid state count")
    shared = system["handshake"]
    require(isinstance(shared, list) and all(isinstance(label, str) and label for label in shared), "invalid handshake alphabet")
    require(len(set(shared)) == len(shared), "duplicate handshake label")
    require(isinstance(system["events"], list) and len(system["events"]) <= MAX_EVENTS, "invalid event list")
    for record in system["events"]:
        require(isinstance(record["label"], str) and bool(record["label"]), "invalid event label")
        require(all(type(record[key]) is int and 0 <= record[key] < size for key in ("source", "target")), "invalid event state")
        require(type(record["weight"]) is int and record["weight"] >= 0, "invalid event weight")


def compatible(left: dict, right: dict) -> None:
    validate(left)
    validate(right)
    require(set(left["handshake"]) == set(right["handshake"]), "incompatible handshake alphabets")
    require(left["n_states"] * right["n_states"] <= MAX_STATES, "composite state cap exceeded")


def compose(left: dict, right: dict) -> dict:
    compatible(left, right)
    left_size, right_size = left["n_states"], right["n_states"]
    shared = set(left["handshake"])
    records = []
    for first in left["events"]:
        if first["weight"] == 0:
            continue
        if first["label"] in shared:
            for second in right["events"]:
                if second["label"] == first["label"] and second["weight"]:
                    records.append(event(first["label"], first["source"] * right_size + second["source"],
                                         first["target"] * right_size + second["target"],
                                         first["weight"] * second["weight"]))
        else:
            for passive in range(right_size):
                records.append(event(first["label"], first["source"] * right_size + passive,
                                     first["target"] * right_size + passive, first["weight"]))
    for second in right["events"]:
        if second["label"] not in shared and second["weight"]:
            for passive in range(left_size):
                records.append(event(second["label"], passive * right_size + second["source"],
                                     passive * right_size + second["target"], second["weight"]))
    return component(left_size * right_size, records, sorted(shared))


def labelled_weights(system: dict) -> dict:
    validate(system)
    size = system["n_states"]
    labels = set(system["handshake"]) | {record["label"] for record in system["events"]}
    matrices = {label: [[0] * size for _ in range(size)] for label in sorted(labels)}
    for record in system["events"]:
        matrices[record["label"]][record["source"]][record["target"]] += record["weight"]
    return {label: matrix for label, matrix in matrices.items() if any(any(row) for row in matrix)}


def matrix_product_oracle(left: dict, right: dict) -> dict:
    compatible(left, right)
    left_weights, right_weights = labelled_weights(left), labelled_weights(right)
    left_size, right_size = left["n_states"], right["n_states"]
    shared = set(left["handshake"])
    result = {}
    for label in sorted(set(left_weights) | set(right_weights) | shared):
        first = left_weights.get(label, [[0] * left_size for _ in range(left_size)])
        second = right_weights.get(label, [[0] * right_size for _ in range(right_size)])
        matrix = []
        for source_left, source_right in product(range(left_size), range(right_size)):
            row = []
            for target_left, target_right in product(range(left_size), range(right_size)):
                if label in shared:
                    value = first[source_left][target_left] * second[source_right][target_right]
                else:
                    value = (first[source_left][target_left] * (source_right == target_right)
                             + (source_left == target_left) * second[source_right][target_right])
                row.append(value)
            matrix.append(row)
        if any(any(row) for row in matrix):
            result[label] = matrix
    return result


def weighted_equal(left: dict, right: dict) -> bool:
    return (left["n_states"] == right["n_states"]
            and set(left["handshake"]) == set(right["handshake"])
            and labelled_weights(left) == labelled_weights(right))


def kernel(system: dict) -> list[list[Fraction]]:
    matrices = labelled_weights(system)
    size = system["n_states"]
    result = []
    for source in range(size):
        row = [sum(matrix[source][target] for matrix in matrices.values()) for target in range(size)]
        total = sum(row)
        result.append([Fraction(weight, total) for weight in row] if total
                      else [Fraction(source == target) for target in range(size)])
    return result


def partition(system: dict, labels: list[int]) -> int:
    require(len(labels) == system["n_states"] and all(type(label) is int and label >= 0 for label in labels), "invalid observation")
    count = len(set(labels))
    require(set(labels) == set(range(count)), "observation labels must be contiguous")
    return count


def observed_kernel(system: dict, labels: list[int]) -> dict:
    count = partition(system, labels)
    matrix = kernel(system)
    first = {}
    for source, label in enumerate(labels):
        row = [sum(matrix[source][target] for target, observed in enumerate(labels) if observed == block)
               for block in range(count)]
        if label in first and first[label][1] != row:
            return {"exact": False, "rows": None,
                    "witness": {"states": [first[label][0], source], "source_block": label,
                                "first_row": first[label][1], "second_row": row}}
        first[label] = (source, row)
    return {"exact": True, "rows": [first[label][1] for label in range(count)], "witness": None}


def weighted_quotient(system: dict, labels: list[int]) -> dict:
    count = partition(system, labels)
    matrices = labelled_weights(system)
    first = {}
    for source, block in enumerate(labels):
        row = {label: [sum(matrix[source][target] for target, observed in enumerate(labels) if observed == destination)
                       for destination in range(count)] for label, matrix in matrices.items()}
        if block in first and first[block][1] != row:
            return {"exact": False, "component": None, "witness": {"states": [first[block][0], source], "source_block": block}}
        first[block] = (source, row)
    records = [event(label, source, target, weight)
               for source in range(count) for label, row in first[source][1].items()
               for target, weight in enumerate(row) if weight]
    return {"exact": True, "component": component(count, records, system["handshake"]), "witness": None}


def unit(handshake=("sync",)) -> dict:
    return component(1, [event(label, 0, 0) for label in handshake], handshake)


def lift(system: dict, mode: str) -> dict:
    validate(system)
    require(mode in {"hold", "flip", "reset"}, "unknown hidden-state update")
    records = []
    for record in system["events"]:
        for hidden in range(2):
            updated = hidden if mode == "hold" else 1 - hidden if mode == "flip" else 0
            records.append(event(record["label"], 2 * record["source"] + hidden,
                                 2 * record["target"] + updated, record["weight"]))
    return component(2 * system["n_states"], records, system["handshake"])


def product_observation(left_labels: list[int], right_labels: list[int]) -> list[int]:
    right_count = len(set(right_labels))
    return [first * right_count + second for first in left_labels for second in right_labels]


def hidden_component(labels_by_hidden: tuple[str, str], rates=(1, 1), handshake=("a", "b")) -> dict:
    return component(4, [event(labels_by_hidden[hidden], 2 * observed + hidden,
                               2 * (1 - observed) + hidden, rates[hidden])
                         for observed in range(2) for hidden in range(2)], handshake)


def serialise(value):
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, dict):
        return {key: serialise(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialise(item) for item in value]
    return value


def run_checks() -> dict:
    menu = [component(2, [])] + [component(2, [event(label, source, target)])
                               for label, source, target in product(("sync", "private"), range(2), range(2))]
    pair_checks = 0
    for left, right in product(menu, repeat=2):
        require(labelled_weights(compose(left, right)) == matrix_product_oracle(left, right), "sparse/dense composition disagreement")
        pair_checks += 1
    triple_checks = 0
    for first, second, third in product(menu, repeat=3):
        require(weighted_equal(compose(compose(first, second), third), compose(first, compose(second, third))), "associativity failure")
        triple_checks += 1
    for system in menu:
        require(weighted_equal(compose(system, unit()), system) and weighted_equal(compose(unit(), system), system), "unit failure")
    quotient_checks = 0
    for macro, mode, partner in product(menu, ("hold", "flip", "reset"), menu):
        micro = lift(macro, mode)
        labels = [state // 2 for state in range(micro["n_states"])]
        reduced = weighted_quotient(micro, labels)
        require(reduced["exact"] and weighted_equal(reduced["component"], macro), "lift does not preserve label weights")
        observed = observed_kernel(compose(micro, partner), product_observation(labels, list(range(partner["n_states"]))))
        require(observed["exact"] and observed["rows"] == kernel(compose(macro, partner)), "quotient/composition does not commute")
        quotient_checks += 1
    nonbinary = component(3, [event("sync", 0, 1), event("sync", 0, 1, 2),
                              event("sync", 1, 2, 2), event("sync", 2, 0),
                              event("private", 0, 0), event("private", 2, 1)])
    partner = component(2, [event("sync", 0, 1, 2), event("sync", 1, 0), event("private", 1, 1)])
    require(labelled_weights(compose(nonbinary, partner)) == matrix_product_oracle(nonbinary, partner), "nonbinary duplicate aggregation failure")
    left_micro, right_micro = lift(nonbinary, "flip"), lift(partner, "reset")
    labels = product_observation([state // 2 for state in range(6)], [state // 2 for state in range(4)])
    reduced = weighted_quotient(compose(left_micro, right_micro), labels)
    require(reduced["exact"] and weighted_equal(reduced["component"], compose(nonbinary, partner)), "two-factor weighted reduction failure")
    require(observed_kernel(compose(left_micro, right_micro), labels)["rows"] == kernel(compose(nonbinary, partner)), "two-factor normalisation failure")
    shared_partner = component(2, [event("a", 0, 1), event("a", 1, 0)], ("a", "b"))
    hidden = hidden_component(("a", "b"))
    observed = [0, 0, 1, 1]
    hidden_before = observed_kernel(hidden, observed)
    hidden_after = observed_kernel(compose(hidden, shared_partner), product_observation(observed, [0, 1]))
    require(hidden_before["exact"] and not hidden_after["exact"], "hidden-label counterexample missing")
    require(weighted_quotient(hidden, observed)["component"] is None, "invalid labelled quotient was manufactured")
    scaled = hidden_component(("a", "a"), (1, 2))
    shared_only = observed_kernel(compose(scaled, shared_partner), product_observation(observed, [0, 1]))
    private_partner = component(2, shared_partner["events"] + [event("tick", 0, 0), event("tick", 1, 1)], ("a", "b"))
    with_clock = observed_kernel(compose(scaled, private_partner), product_observation(observed, [0, 1]))
    require(shared_only["exact"] and not with_clock["exact"], "private-clock scaling contrast missing")
    require(not weighted_quotient(scaled, observed)["exact"], "sufficient condition unexpectedly necessary")
    neutral, dead = unit(("a", "b")), component(1, [], ("a", "b"))
    require(kernel(neutral) == kernel(dead), "one-state aggregate control drift")
    require(kernel(compose(shared_partner, neutral)) != kernel(compose(shared_partner, dead)), "halt completion was incorrectly promoted to an event")
    return serialise({"method": METHOD_ID, "evidence_type": "analytic proof and independent software validation",
                      "scientific_worker_invocations": 0, "new_atlas_cells": 0,
                      "basis_component_count": len(menu), "pair_oracle_checks": pair_checks,
                      "associative_triples_checked": triple_checks, "unit_controls_checked": len(menu),
                      "weighted_quotient_contexts_checked": quotient_checks,
                      "hidden_update_modes": ["hold", "flip", "reset"],
                      "nonbinary_and_two_factor_controls": "verified",
                      "unit_and_halt_same_standalone_kernel": True,
                      "unit_and_halt_different_composed_kernel": True,
                      "hidden_label_standalone_exact": hidden_before,
                      "hidden_label_composed_nonexact": hidden_after,
                      "scaling_shared_only_exact": shared_only,
                      "scaling_with_private_clock_nonexact": with_clock,
                      "status": "verified"})


if __name__ == "__main__":
    print(json.dumps(run_checks(), indent=2))
