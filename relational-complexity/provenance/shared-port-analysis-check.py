"""Independent exact checks of a declared shared-port product; no RRC imports."""

from fractions import Fraction
from itertools import product
import json


METHOD_ID = "shared-port-analysis-0.1.0"
MAX_STATES = 64
MAX_EVENTS = 4096


def require(condition, message):
    if not condition:
        raise ValueError(message)


def event(label, source, target, weight=1):
    return {"label": label, "source": source, "target": target, "weight": weight}


def component(ports, events, port_count=2, handshake=("h",), coordinates=None):
    result = {"n_states": len(ports), "ports": list(ports), "port_count": port_count,
              "handshake": list(handshake), "events": events,
              "coordinates": list(coordinates) if coordinates is not None else [(i,) for i in range(len(ports))]}
    validate(result)
    return result


def validate(system):
    n, count = system["n_states"], system["port_count"]
    require(type(n) is int and 1 <= n <= MAX_STATES, "invalid state count")
    require(type(count) is int and 1 <= count <= n, "invalid port count")
    ports = system["ports"]
    require(len(ports) == n and all(type(p) is int and 0 <= p < count for p in ports), "invalid port map")
    require(set(ports) == set(range(count)), "port map must be onto")
    shared = system["handshake"]
    require(isinstance(shared, list) and all(isinstance(label, str) and label for label in shared), "invalid handshake")
    require(len(set(shared)) == len(shared), "duplicate handshake label")
    coordinates = system["coordinates"]
    require(len(coordinates) == n and all(isinstance(c, tuple) and c and all(type(x) is int and x >= 0 for x in c) for c in coordinates), "invalid coordinates")
    require(len(set(coordinates)) == n and len({len(c) for c in coordinates}) == 1, "ambiguous coordinates")
    require(isinstance(system["events"], list) and len(system["events"]) <= MAX_EVENTS, "invalid event list")
    for record in system["events"]:
        require(isinstance(record["label"], str) and bool(record["label"]), "invalid event label")
        require(type(record["weight"]) is int and record["weight"] >= 0, "invalid event weight")
        require(all(type(record[k]) is int and 0 <= record[k] < n for k in ("source", "target")), "invalid event state")
        if record["weight"] and record["label"] not in shared:
            require(ports[record["source"]] == ports[record["target"]], "private event changes the port")


def compatible(left, right):
    validate(left)
    validate(right)
    require(left["port_count"] == right["port_count"], "incompatible port types")
    require(set(left["handshake"]) == set(right["handshake"]), "incompatible handshake")
    require(left["n_states"] * right["n_states"] <= MAX_STATES, "Cartesian validation cap exceeded")


def compose(left, right):
    """Sparse matching events, explicitly filtering compatible sources/targets."""
    compatible(left, right)
    pairs = [(s, t) for s in range(left["n_states"]) for t in range(right["n_states"])
             if left["ports"][s] == right["ports"][t]]
    index = {pair: i for i, pair in enumerate(pairs)}
    records = []

    def append(label, source, target, weight):
        if weight and source in index and target in index:
            records.append(event(label, index[source], index[target], weight))

    shared = set(left["handshake"])
    for first in left["events"]:
        if not first["weight"]:
            continue
        if first["label"] in shared:
            for second in right["events"]:
                if first["label"] == second["label"]:
                    append(first["label"], (first["source"], second["source"]),
                           (first["target"], second["target"]), first["weight"] * second["weight"])
        else:
            for passive in range(right["n_states"]):
                append(first["label"], (first["source"], passive), (first["target"], passive), first["weight"])
    for second in right["events"]:
        if second["label"] not in shared:
            for passive in range(left["n_states"]):
                append(second["label"], (passive, second["source"]), (passive, second["target"]), second["weight"])
    return component([left["ports"][s] for s, _ in pairs], records, left["port_count"], sorted(shared),
                     [left["coordinates"][s] + right["coordinates"][t] for s, t in pairs])


def matrices(system):
    validate(system)
    n = system["n_states"]
    result = {}
    for record in system["events"]:
        matrix = result.setdefault(record["label"], [[0] * n for _ in range(n)])
        matrix[record["source"]][record["target"]] += record["weight"]
    return {label: matrix for label, matrix in result.items() if any(any(row) for row in matrix)}


def cartesian_matrices(left, right):
    """Independent dense tensor formula on all Cartesian copies, before guarding."""
    compatible(left, right)
    n, m = left["n_states"], right["n_states"]
    first, second = matrices(left), matrices(right)
    zero_left, zero_right = [[0] * n for _ in range(n)], [[0] * m for _ in range(m)]
    result = {}
    for label in sorted(set(first) | set(second)):
        a, b = first.get(label, zero_left), second.get(label, zero_right)
        matrix = [[0] * (n * m) for _ in range(n * m)]
        for s, t, u, v in product(range(n), range(m), range(n), range(m)):
            matrix[s * m + t][u * m + v] = (a[s][u] * b[t][v] if label in left["handshake"] else
                                           a[s][u] * (t == v) + (s == u) * b[t][v])
        if any(any(row) for row in matrix):
            result[label] = matrix
    return result


def agreement_indices(left, right):
    return [s * right["n_states"] + t for s in range(left["n_states"]) for t in range(right["n_states"])
            if left["ports"][s] == right["ports"][t]]


def restriction_oracle(left, right):
    indices = agreement_indices(left, right)
    result = {label: [[matrix[s][t] for t in indices] for s in indices]
              for label, matrix in cartesian_matrices(left, right).items()}
    return {label: matrix for label, matrix in result.items() if any(any(row) for row in matrix)}


def normalise(label_matrices, size):
    result = []
    for source in range(size):
        row = [sum(matrix[source][target] for matrix in label_matrices.values()) for target in range(size)]
        total = sum(row)
        result.append([Fraction(value, total) for value in row] if total else
                      [Fraction(source == target) for target in range(size)])
    return result


def kernel(system):
    return normalise(matrices(system), system["n_states"])


def canonical_weights(system, coordinate_map=lambda c: c):
    points = [coordinate_map(c) for c in system["coordinates"]]
    require(len(set(points)) == len(points), "noninjective coordinate map")
    weights = {(label, points[s], points[t]): value for label, matrix in matrices(system).items()
               for s, row in enumerate(matrix) for t, value in enumerate(row) if value}
    ports = {points[s]: p for s, p in enumerate(system["ports"])}
    return {"port_count": system["port_count"], "handshake": sorted(system["handshake"]),
            "ports": ports, "weights": weights}


def unit(port_count, handshake=("h",)):
    return component(list(range(port_count)),
                     [event(label, source, target) for label in handshake
                      for source, target in product(range(port_count), repeat=2)], port_count, handshake)


def support_invariant(left, right):
    compatible(left, right)
    for a in left["events"]:
        for b in right["events"]:
            if (a["weight"] and b["weight"] and a["label"] in left["handshake"] and a["label"] == b["label"]
                    and left["ports"][a["source"]] == right["ports"][b["source"]]
                    and left["ports"][a["target"]] != right["ports"][b["target"]]):
                return {"invariant": False, "witness": {"label": a["label"],
                        "source_pair": [a["source"], b["source"]], "target_pair": [a["target"], b["target"]],
                        "positive_product_weight": a["weight"] * b["weight"]}}
    return {"invariant": True, "witness": None}


def agreement_report(left, right):
    compatible(left, right)
    indices = agreement_indices(left, right)
    full = normalise(cartesian_matrices(left, right), left["n_states"] * right["n_states"])
    retained = [[full[source][target] for target in indices] for source in indices]
    leaks = [1 - sum(row) for row in retained]
    invariant = all(value == 0 for value in leaks)
    conditionals = [[value / sum(row) for value in row] if sum(row) else None for row in retained]
    attempts = [[value + (leaks[source] if source == target else 0) for target, value in enumerate(row)]
                for source, row in enumerate(retained)]
    require(invariant == support_invariant(left, right)["invariant"], "support/kernel invariance disagreement")
    identified = compose(left, right)
    require(matrices(identified) == restriction_oracle(left, right), "sparse/restriction disagreement")
    return {"invariant": invariant, "leakage": leaks, "agreement_image": indices,
            "restricted_rows": retained if invariant else None, "conditional_rows": conditionals,
            "rejected_attempts_hold_control": attempts,
            "identified_rows": kernel(identified), "support": support_invariant(left, right)}


def observation_count(size, observation):
    require(len(observation) == size and all(type(x) is int and x >= 0 for x in observation), "invalid observation")
    count = len(set(observation))
    require(set(observation) == set(range(count)), "noncontiguous observation")
    return count


def observed_kernel(matrix, observation):
    count = observation_count(len(matrix), observation)
    first = {}
    for source, block in enumerate(observation):
        row = [sum(matrix[source][target] for target in range(len(matrix)) if observation[target] == destination)
               for destination in range(count)]
        if block in first and first[block][1] != row:
            return {"exact": False, "rows": None, "witness": {"states": [first[block][0], source],
                    "first_row": first[block][1], "second_row": row}}
        first[block] = (source, row)
    return {"exact": True, "rows": [first[k][1] for k in range(count)], "witness": None}


def boundary_factor(system, observation):
    observation_count(system["n_states"], observation)
    first = {}
    for source, block in enumerate(observation):
        port = system["ports"][source]
        if block in first and first[block][1] != port:
            return {"defined": False, "port_map": None, "witness": [first[block][0], source]}
        first[block] = (source, port)
    return {"defined": True, "port_map": [first[k][1] for k in range(len(first))], "witness": None}


def lift(system, mode):
    require(mode in {"hold", "flip", "reset"}, "invalid internal update")
    records = []
    for record in system["events"]:
        for hidden in range(2):
            updated = hidden if mode == "hold" else 1 - hidden if mode == "flip" else 0
            records.append(event(record["label"], 2 * record["source"] + hidden,
                                 2 * record["target"] + updated, record["weight"]))
    return component([p for p in system["ports"] for _ in range(2)], records,
                     system["port_count"], system["handshake"])


def feedback_pair(feedback):
    left_events, right_events = [], []
    for x, p in product(range(2), repeat=2):
        left_events.extend([event("h", 2 * x + p, 2 * x + 1 - p),
                            event("left", 2 * x + p, 2 * (1 - x) + p, 1 + p if feedback else 1)])
    for p, y in product(range(2), repeat=2):
        right_events.extend([event("h", 2 * p + y, 2 * (1 - p) + y),
                             event("right", 2 * p + y, 2 * p + 1 - y)])
    return component([0, 1, 0, 1], left_events), component([0, 0, 1, 1], right_events)


def bit_kernel(feedback):
    matrix = [[0] * 8 for _ in range(8)]
    for source in range(8):
        matrix[source][source ^ 4] = 1 + ((source >> 1) & 1) if feedback else 1
        matrix[source][source ^ 2] = 1
        matrix[source][source ^ 1] = 1
    return normalise({"aggregate": matrix}, 8)


def serialise(value):
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, dict):
        return {key: serialise(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialise(item) for item in value]
    return value


def run_checks():
    menu = [component([0, 1], [])]
    menu += [component([0, 1], [event("h", source, target)]) for source, target in product(range(2), repeat=2)]
    menu += [component([0, 1], [event("private", source, source)]) for source in range(2)]
    for left, right in product(menu, repeat=2):
        agreement_report(left, right)
    for left, middle, right in product(menu, repeat=3):
        require(canonical_weights(compose(compose(left, middle), right)) ==
                canonical_weights(compose(left, compose(middle, right))), "associativity failure")
    for system in menu:
        neutral = unit(system["port_count"], system["handshake"])
        require(canonical_weights(compose(neutral, system), lambda c: c[1:]) == canonical_weights(system), "left identity failure")
        require(canonical_weights(compose(system, neutral), lambda c: c[:-1]) == canonical_weights(system), "right identity failure")
    for system, mode, partner in product(menu, ("hold", "flip", "reset"), menu):
        agreement_report(lift(system, mode), partner)
    three = component([0, 1, 2], [event("h", 0, 1), event("h", 0, 1, 2), event("h", 1, 2, 2),
                                 event("h", 2, 0), event("g", 0, 0), event("p", 1, 1, 2)], 3, ("h", "g"))
    agreement_report(three, three)
    require(canonical_weights(compose(compose(three, three), three)) ==
            canonical_weights(compose(three, compose(three, three))), "three-port iteration failure")
    reports = {}
    for feedback in (False, True):
        left, right = feedback_pair(feedback)
        identified = compose(left, right)
        require(kernel(identified) == bit_kernel(feedback), "listed-bit reduction disagreement")
        require(agreement_report(left, right)["invariant"], "compatible feedback copies leak")
        observation = [2 * (c[0] // 2) + c[1] % 2 for c in identified["coordinates"]]
        reports["feedback" if feedback else "no_feedback"] = {
            "observation": observed_kernel(kernel(identified), observation), "boundary": boundary_factor(identified, observation)}
    require(reports["no_feedback"]["observation"]["exact"] and not reports["feedback"]["observation"]["exact"], "feedback/null separation missing")
    require(not reports["no_feedback"]["boundary"]["defined"], "predictive observation incorrectly inherits the port")
    left, right = feedback_pair(True)
    third = lift(menu[2], "flip")
    require(canonical_weights(compose(compose(left, right), third)) ==
            canonical_weights(compose(left, compose(right, third))), "internal-state iteration failure")
    random_port = component([0, 1], [event("h", source, target, target + 1) for source, target in product(range(2), repeat=2)])
    mismatch_left = component([0, 1], [event("h", 0, 1, 2), event("tick", 0, 0)])
    mismatch_right = component([0, 1], [event("h", 0, 0, 3)])
    mismatch = agreement_report(mismatch_left, mismatch_right)
    rejected = agreement_report(component([0, 1], [event("h", 0, 1, 2)]), mismatch_right)
    require(mismatch["leakage"][0] == Fraction(6, 7) and rejected["conditional_rows"][0] is None,
            "constraint/conditioning boundary missing")
    return serialise({"method": METHOD_ID, "evidence_type": "analytic proof and independent software validation",
                      "scientific_worker_invocations": 0, "new_atlas_cells": 0,
                      "basis_components": len(menu), "pair_oracle_checks": len(menu) ** 2,
                      "associativity_triples": len(menu) ** 3, "two_sided_unit_controls": len(menu),
                      "lifted_pair_oracle_checks": len(menu) ** 2 * 3,
                      "extra_three_port_and_internal_iteration": "verified",
                      "eight_state_identification_and_bit_reduction": reports,
                      "equal_marginals_copy_comparison": agreement_report(random_port, random_port),
                      "mismatched_targets_with_private_competitor": mismatch,
                      "all_shared_targets_rejected": rejected, "status": "verified"})


if __name__ == "__main__":
    print(json.dumps(run_checks(), indent=2))
