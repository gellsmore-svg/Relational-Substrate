"""Exact context-probe validation; independent of the RRC and sparse-event engines."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import json


METHOD_ID = "context-probe-analysis-0.1.0"
MAX_STATES = 16
MAX_PRODUCT_STATES = 64


def require(condition, message):
    if not condition:
        raise ValueError(message)


def event(label, source, target, weight=1):
    return {"label": label, "source": source, "target": target, "weight": weight}


def component(size, events, handshake=("a", "b")):
    result = {"n_states": size, "events": events, "handshake": list(handshake)}
    validate(result)
    return result


def validate(system):
    size = system["n_states"]
    require(type(size) is int and 1 <= size <= MAX_STATES, "invalid state count")
    shared = system["handshake"]
    require(isinstance(shared, list) and all(isinstance(x, str) and x for x in shared), "invalid handshake alphabet")
    require(len(set(shared)) == len(shared), "duplicate handshake label")
    require(isinstance(system["events"], list) and len(system["events"]) <= 2048, "invalid event list")
    for record in system["events"]:
        require(isinstance(record["label"], str) and bool(record["label"]), "invalid label")
        require(type(record["weight"]) is int and record["weight"] >= 0, "invalid weight")
        require(all(type(record[k]) is int and 0 <= record[k] < size for k in ("source", "target")), "invalid event state")


def observation_count(system, observation):
    validate(system)
    require(len(observation) == system["n_states"] and all(type(x) is int and x >= 0 for x in observation), "invalid observation")
    count = len(set(observation))
    require(set(observation) == set(range(count)), "noncontiguous observation")
    return count


def signatures(system, observation):
    """Raw event scan, with a separate namespace for the private aggregate."""
    count = observation_count(system, observation)
    shared = set(system["handshake"])
    rows = [{"shared": {label: [0] * count for label in sorted(shared)}, "private": [0] * count}
            for _ in range(system["n_states"])]
    for record in system["events"]:
        row = rows[record["source"]]
        target = row["shared"][record["label"]] if record["label"] in shared else row["private"]
        target[observation[record["target"]]] += record["weight"]
    return rows


def stable(rows, observation):
    first = {}
    for state, block in enumerate(observation):
        if block in first and first[block][1] != rows[state]:
            return {"exact": False, "rows": None,
                    "witness": {"states": [first[block][0], state], "source_block": block,
                                "first_row": first[block][1], "second_row": rows[state]}}
        first[block] = (state, rows[state])
    return {"exact": True, "rows": [first[k][1] for k in range(len(first))], "witness": None}


def label_matrices(system):
    validate(system)
    size = system["n_states"]
    matrices = {}
    for record in system["events"]:
        matrix = matrices.setdefault(record["label"], [[0] * size for _ in range(size)])
        matrix[record["source"]][record["target"]] += record["weight"]
    return matrices


def composed_kernel(left, right):
    """Dense per-label tensor formula, not a scan of matching event pairs."""
    validate(left)
    validate(right)
    require(set(left["handshake"]) == set(right["handshake"]), "incompatible handshake alphabets")
    n, m = left["n_states"], right["n_states"]
    require(n * m <= MAX_PRODUCT_STATES, "product state cap exceeded")
    shared = set(left["handshake"])
    first, second = label_matrices(left), label_matrices(right)
    zero_left, zero_right = [[0] * n for _ in range(n)], [[0] * m for _ in range(m)]
    weights = [[0] * (n * m) for _ in range(n * m)]
    for label in set(first) | set(second):
        a, b = first.get(label, zero_left), second.get(label, zero_right)
        for s, t, u, v in product(range(n), range(m), range(n), range(m)):
            value = (a[s][u] * b[t][v] if label in shared else
                     a[s][u] * (t == v) + (s == u) * b[t][v])
            weights[s * m + t][u * m + v] += value
    result = []
    for source, row in enumerate(weights):
        total = sum(row)
        result.append([Fraction(x, total) for x in row] if total else
                      [Fraction(source == target) for target in range(n * m)])
    return result


def aggregate_rows(matrix, observation):
    count = len(set(observation))
    rows = []
    for row in matrix:
        totals = [Fraction(0)] * count
        for target, value in enumerate(row):
            totals[observation[target]] += value
        rows.append(totals)
    return rows


def product_observation(observation, partner_size):
    return [label * partner_size + state for label in observation for state in range(partner_size)]


def probe_family(handshake):
    """One private-only calibration probe, plus one per shared label."""
    shared = sorted(handshake)
    private_label = "_probe"
    while private_label in shared:
        private_label += "_"
    probes = [{"kind": "private", "label": None, "anchor": 1,
               "component": component(2, [event(private_label, 0, 1)], shared)}]
    for label in shared:
        probes.append({"kind": "shared", "label": label, "anchor": 2,
                       "component": component(3, [event(label, 0, 1), event(private_label, 0, 2)], shared)})
    return probes


def inspect_context(system, observation, partner):
    observation_count(system, observation)
    labels = product_observation(observation, partner["n_states"])
    rows = aggregate_rows(composed_kernel(system, partner), labels)
    return rows, stable(rows, labels)


def assess(system, observation):
    """Compare raw signatures to probe laws; recover raw values from probabilities."""
    expected = signatures(system, observation)
    count = len(set(observation))
    recovered = [{"shared": {}, "private": None} for _ in observation]
    reports = []
    for probe in probe_family(system["handshake"]):
        partner = probe["component"]
        size = partner["n_states"]
        rows, report = inspect_context(system, observation, partner)
        reports.append({"kind": probe["kind"], "label": probe["label"], **report})
        for source, block in enumerate(observation):
            row = rows[source * size]
            anchor = row[block * size + probe["anchor"]]
            require(anchor > 0, "calibration branch absent")
            private = [row[target * size] / anchor for target in range(count)]
            if recovered[source]["private"] is None:
                recovered[source]["private"] = private
            require(recovered[source]["private"] == private, "private reconstruction disagreement")
            if probe["kind"] == "shared":
                recovered[source]["shared"][probe["label"]] = [row[target * size + 1] / anchor for target in range(count)]
    require(recovered == expected, "probability/raw signature reconstruction disagreement")
    verdict = stable(expected, observation)
    require(verdict["exact"] == all(report["exact"] for report in reports), "finite-probe characterization disagreement")
    return {"signature": verdict, "probes": reports, "reconstructed": recovered}


def full_label_stable(system, observation):
    count = observation_count(system, observation)
    labels = sorted({e["label"] for e in system["events"]} | set(system["handshake"]))
    rows = [{label: [0] * count for label in labels} for _ in observation]
    for record in system["events"]:
        rows[record["source"]][record["label"]][observation[record["target"]]] += record["weight"]
    return stable(rows, observation)["exact"]


def template_system(first, second, mode):
    require(mode in {"hold", "flip", "reset"}, "invalid hidden update")
    positions = list(product(("a", "b", "p"), (0, 1)))
    records = []
    for observed, hidden in product(range(2), repeat=2):
        updated = hidden if mode == "hold" else 1 - hidden if mode == "flip" else 0
        for index in (first if hidden == 0 else second):
            label, delta = positions[index]
            records.append(event(label, 2 * observed + hidden, 2 * (observed ^ delta) + updated))
    return component(4, records)


def private_redistribution(handshake=("a", "b")):
    return component(4, [event("p" if hidden == 0 else "q", 2 * observed + hidden,
                               2 * (1 - observed) + 1 - hidden)
                         for observed, hidden in product(range(2), repeat=2)], handshake)


def collapse_private(system, private_label="_private"):
    validate(system)
    require(isinstance(private_label, str) and bool(private_label) and private_label not in system["handshake"],
            "collapsed private label must lie outside handshake")
    shared = set(system["handshake"])
    return component(system["n_states"],
                     [event(record["label"] if record["label"] in shared else private_label,
                            record["source"], record["target"], record["weight"])
                      for record in system["events"]], system["handshake"])


def serialise(value):
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, dict):
        return {key: serialise(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialise(item) for item in value]
    return value


def run_checks():
    templates = [()] + [(i,) for i in range(6)] + list(combinations(range(6), 2))
    counts = {"systems": 0, "stable": 0, "unstable": 0, "probe_laws": 0, "reconstructed_signatures": 0}
    for first, second, mode in product(templates, templates, ("hold", "flip", "reset")):
        system = template_system(first, second, mode)
        result = assess(system, [0, 0, 1, 1])
        counts["systems"] += 1
        counts["stable" if result["signature"]["exact"] else "unstable"] += 1
        counts["probe_laws"] += len(result["probes"])
        counts["reconstructed_signatures"] += len(result["reconstructed"])
    redistributed = private_redistribution()
    positive = assess(redistributed, [0, 0, 1, 1])
    require(positive["signature"]["exact"] and not full_label_stable(redistributed, [0, 0, 1, 1]), "private aggregation boundary missing")
    changed = private_redistribution(("p", "q"))
    require(not assess(changed, [0, 0, 1, 1])["signature"]["exact"], "changed-H control missing")
    internal = component(2, [event("p", 0, 0)])
    private_probe = probe_family(internal["handshake"])[0]["component"]
    _, internal_report = inspect_context(internal, [0, 0], private_probe)
    require(not internal_report["exact"], "internal-loop calibration counterexample missing")
    scaled = component(4, [event("a", 2 * observed + hidden, 2 * (1 - observed) + hidden, hidden + 1)
                           for observed, hidden in product(range(2), repeat=2)])
    partner = component(2, [event("a", 0, 1), event("a", 1, 0)])
    _, shared_only = inspect_context(scaled, [0, 0, 1, 1], partner)
    require(shared_only["exact"] and not assess(scaled, [0, 0, 1, 1])["signature"]["exact"], "restricted-context scaling boundary missing")
    empty_h = component(2, [event("p", 0, 1, 2), event("q", 1, 0, 2)], ())
    require(assess(empty_h, [0, 0])["signature"]["exact"], "empty-H control failure")
    duplicates = component(2, [event("a", 0, 1), event("a", 0, 1, 2), event("q", 0, 0, 0)])
    assess(duplicates, [0, 1])
    return serialise({"method": METHOD_ID, "evidence_type": "analytic proof and independent software validation",
                      "scientific_worker_invocations": 0, "new_atlas_cells": 0,
                      "template_count": len(templates), "hidden_update_modes": ["hold", "flip", "reset"],
                      "validation": counts,
                      "full_label_condition_not_necessary_for_all_declared_contexts": True,
                      "private_redistribution_signatures": positive["reconstructed"],
                      "changed_handshake_fails": True,
                      "internal_loop_vs_halt_calibration": internal_report,
                      "scaling_exact_in_shared_only_context": shared_only["exact"],
                      "scaling_not_uniformly_preserved": True,
                      "empty_handshake_and_duplicate_nonunit_controls": "verified",
                      "status": "verified"})


if __name__ == "__main__":
    print(json.dumps(run_checks(), indent=2))
