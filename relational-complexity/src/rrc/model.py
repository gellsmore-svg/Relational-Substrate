"""Exact single-toggle chains and strong lumpability.

Edge order matches the Constraint Laboratory: pairs ``i < j`` in
lexicographic order. Bit ``e`` is 1 when that pair is present.

A halt state, one whose weights are all zero, is completed by a self-loop.
That self-loop is not a relational event. The name of the convention is
``halt_self_loop``.
"""

from __future__ import annotations

import math
from collections import defaultdict
from fractions import Fraction

import numpy as np

HALT_COMPLETION = "halt_self_loop"
MAX_EDGES = 62


def edge_list(n: int) -> list[tuple[int, int]]:
    if n < 0:
        raise ValueError("N must be non-negative")
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    if len(edges) > MAX_EDGES:
        raise ValueError(f"N={n} has {len(edges)} pairs, above the {MAX_EDGES}-bit builder")
    return edges


def edge_count(n: int) -> int:
    return len(edge_list(n))


def state_count(n: int) -> int:
    return 1 << edge_count(n)


def wedge_pairs(n: int, edges: list[tuple[int, int]]) -> list[tuple[tuple[int, int], ...]]:
    """For each pair, the bit-pairs whose joint presence makes a common neighbour."""
    index = {pair: bit for bit, pair in enumerate(edges)}

    def bit(a: int, b: int) -> int:
        if a > b:
            a, b = b, a
        return index[(a, b)]

    wedges = []
    for a, b in edges:
        pairs = []
        for c in range(n):
            if c == a or c == b:
                continue
            pairs.append((bit(a, c), bit(b, c)))
        wedges.append(tuple(pairs))
    return wedges


def _common_counts(n: int, edges: list[tuple[int, int]]) -> np.ndarray:
    size = 1 << len(edges)
    counts = np.zeros((size, len(edges)), dtype=np.int16)
    states = np.arange(size, dtype=np.int64)
    for edge, pairs in enumerate(wedge_pairs(n, edges)):
        count = np.zeros(size, dtype=np.int16)
        for left, right in pairs:
            count += (((states >> left) & 1) & ((states >> right) & 1)).astype(np.int16)
        counts[:, edge] = count
    return counts


def build_weights(n: int, rule: dict) -> np.ndarray:
    """Integer toggle weights, shape ``(2**C(N,2), C(N,2))``."""
    edges = edge_list(n)
    size = 1 << len(edges)
    width = len(edges)
    family = rule["family"]
    if family == "unconstrained":
        return np.ones((size, width), dtype=np.int32)
    if family == "state_independent_rates":
        incident = int(rule["incident_node"])
        near = int(rule["incident_weight"])
        far = int(rule["other_weight"])
        if near < 0 or far < 0:
            raise ValueError("rates must be non-negative")
        weights = np.empty((size, width), dtype=np.int32)
        for edge, (a, b) in enumerate(edges):
            weights[:, edge] = near if a == incident or b == incident else far
        return weights
    if family == "calibration_weights":
        weights = np.empty((size, width), dtype=np.int32)
        for state in range(size):
            for edge in range(width):
                weights[state, edge] = 1 + ((state * 17 + edge * 13) % 5)
        return weights
    counts = _common_counts(n, edges)
    if family == "hard_wedge_formation":
        states = np.arange(size, dtype=np.int64)
        present = (states[:, None] >> np.arange(width, dtype=np.int64)[None, :]) & 1
        weights = np.ones((size, width), dtype=np.int32)
        weights[(present == 0) & (counts == 0)] = 0
        return weights
    if family == "soft_wedge":
        common = int(rule["common_weight"])
        base = int(rule["base_weight"])
        if common < 0 or base < 0:
            raise ValueError("weights must be non-negative")
        return np.where(counts >= 1, common, base).astype(np.int32)
    if family == "soft_wedge_local_boost":
        common = int(rule["common_weight"])
        base = int(rule["base_weight"])
        boost = int(rule["boost"])
        node = int(rule["boost_node"])
        if min(common, base, boost) < 0:
            raise ValueError("weights must be non-negative")
        weights = np.where(counts >= 1, common, base).astype(np.int32)
        for edge, (a, b) in enumerate(edges):
            if a == node or b == node:
                weights[:, edge] *= boost
        return weights
    raise ValueError(f"unknown rule family {family}")


def hidden_edges(n: int, partition: dict) -> list[int]:
    edges = edge_list(n)
    kind = partition["kind"]
    if kind == "hide_subset":
        members = set(partition["members"])
        if any(node < 0 or node >= n for node in members):
            raise ValueError("subset node outside 0..N-1")
        return [bit for bit, (a, b) in enumerate(edges) if a in members and b in members]
    if kind == "hide_two_subsets":
        left = set(partition["left"])
        right = set(partition["right"])
        if left & right:
            raise ValueError("composed subsets overlap")
        if any(node < 0 or node >= n for node in left | right):
            raise ValueError("subset node outside 0..N-1")
        return [
            bit
            for bit, (a, b) in enumerate(edges)
            if (a in left and b in left) or (a in right and b in right)
        ]
    raise ValueError(f"unknown partition {kind}")


def visible_edges(n: int, hidden: list[int]) -> list[int]:
    hidden_set = set(hidden)
    return [bit for bit in range(edge_count(n)) if bit not in hidden_set]


def _pack_array(states: np.ndarray, bits: list[int]) -> np.ndarray:
    packed = np.zeros(states.shape, dtype=np.int64)
    for place, bit in enumerate(bits):
        packed |= ((states >> bit) & 1) << place
    return packed


def _popcount_bits(states: np.ndarray, bits: list[int]) -> np.ndarray:
    count = np.zeros(states.shape, dtype=np.int16)
    for bit in bits:
        count += ((states >> bit) & 1).astype(np.int16)
    return count


def _wedge_profiles(
    n: int,
    edges: list[tuple[int, int]],
    visible: list[int],
) -> list[tuple[int, ...]]:
    wedges = wedge_pairs(n, edges)
    size = 1 << len(edges)
    profiles = []
    for state in range(size):
        counts = []
        for edge in visible:
            count = 0
            for left, right in wedges[edge]:
                if (state >> left) & 1 and (state >> right) & 1:
                    count += 1
            counts.append(count)
        profiles.append(tuple(counts))
    return profiles


def _compact(keys: list) -> tuple[list[int], int]:
    index: dict = {}
    labels = []
    for key in keys:
        if key not in index:
            index[key] = len(index)
        labels.append(index[key])
    return labels, len(index)


def partition_labels(
    n: int,
    partition: dict,
    augmentation: str,
) -> tuple[list[int], int, list[int], list[int]]:
    """Return compact labels, block count, hidden bits, visible bits.

    ``augmentation`` is ``interface``, ``edge_count``, ``parity`` or
    ``interface_wedge_counts``. The first groups only by interface bits.
    """
    edges = edge_list(n)
    hidden = hidden_edges(n, partition)
    visible = visible_edges(n, hidden)
    size = 1 << len(edges)
    states = np.arange(size, dtype=np.int64)
    packed = _pack_array(states, visible)
    if augmentation == "interface":
        keys = [int(value) for value in packed]
    elif augmentation == "edge_count":
        counts = _popcount_bits(states, hidden)
        keys = [(int(packed[state]), int(counts[state])) for state in range(size)]
    elif augmentation == "parity":
        counts = _popcount_bits(states, hidden)
        keys = [(int(packed[state]), int(counts[state]) & 1) for state in range(size)]
    elif augmentation == "interface_wedge_counts":
        profiles = _wedge_profiles(n, edges, visible)
        keys = [(int(packed[state]), profiles[state]) for state in range(size)]
    else:
        raise ValueError(f"unknown augmentation {augmentation}")
    labels, blocks = _compact(keys)
    return labels, blocks, hidden, visible


def _masses(state: int, weights: np.ndarray, sums: np.ndarray, labels: list[int]) -> tuple[int, dict[int, int]]:
    total = int(sums[state])
    if total == 0:
        return 1, {int(labels[state]): 1}
    accumulated: dict[int, int] = {}
    row = weights[state]
    for edge, weight in enumerate(row):
        weight = int(weight)
        if weight == 0:
            continue
        block = int(labels[state ^ (1 << edge)])
        accumulated[block] = accumulated.get(block, 0) + weight
    return total, accumulated


def _signature_key(total: int, masses: dict[int, int]) -> tuple:
    items = []
    for block, mass in sorted(masses.items()):
        divisor = math.gcd(mass, total)
        items.append((block, mass // divisor, total // divisor))
    return tuple(items)


def _l1(left_total: int, left: dict[int, int], right_total: int, right: dict[int, int]) -> Fraction:
    blocks = set(left) | set(right)
    distance = Fraction(0)
    for block in blocks:
        distance += abs(
            Fraction(left.get(block, 0), left_total) - Fraction(right.get(block, 0), right_total)
        )
    return distance


def lumpability(weights: np.ndarray, labels: list[int]) -> dict:
    """Strong-lumpability defect of ``labels``.

    ``exact`` is true only when every state in a block has the same
    next-block law. ``defect_l1`` is the maximum L1 distance from a state's
    law to the mean law of its block. That distance is zero exactly when the
    partition is strongly lumpable. It is not a stationary distance.
    """
    size, _width = weights.shape
    if len(labels) != size:
        raise ValueError("labels must cover every state")
    sums = weights.sum(axis=1)
    groups: dict[int, list[int]] = defaultdict(list)
    for state, label in enumerate(labels):
        groups[int(label)].append(state)
    defect = Fraction(0)
    witness = None
    for block, members in groups.items():
        rows = [_masses(state, weights, sums, labels) for state in members]
        mean_mass: dict[int, Fraction] = defaultdict(lambda: Fraction(0))
        for total, masses in rows:
            for target, mass in masses.items():
                mean_mass[target] += Fraction(mass, total)
        count = len(members)
        mean = {target: mass / count for target, mass in mean_mass.items()}
        # Compare each row with the mean. The mean is stored as a fake integer
        # row only through Fraction arithmetic below.
        for state, (total, masses) in zip(members, rows):
            keys = set(masses) | set(mean)
            distance = Fraction(0)
            for target in keys:
                distance += abs(Fraction(masses.get(target, 0), total) - mean.get(target, Fraction(0)))
            if distance > defect:
                defect = distance
                partner = members[0]
                partner_row = rows[0]
                for other, other_row in zip(members, rows):
                    if _signature_key(*other_row) != _signature_key(total, masses):
                        partner = other
                        partner_row = other_row
                        break
                pair = _l1(total, masses, partner_row[0], partner_row[1])
                witness = {
                    "block": int(block),
                    "states": sorted((int(state), int(partner))),
                    "pairwise_l1": pair,
                }
    return {
        "exact": defect == 0,
        "defect_l1": defect,
        "n_blocks": len(groups),
        "max_block_size": max(len(members) for members in groups.values()),
        "witness": witness,
    }


def quotient_kernel(weights: np.ndarray, labels: list[int]) -> dict:
    """The common next-block law when ``labels`` is strongly lumpable.

    Rows follow the sorted block ids. A zero weight row is the self-loop
    already used by ``lumpability``. No row is invented when the defect is
    positive: the states in a block need not share a next-block law.
    """
    report = lumpability(weights, labels)
    blocks = sorted({int(label) for label in labels})
    if not report["exact"]:
        return {
            "defined": False,
            "reason": "not strongly lumpable",
            "blocks": blocks,
            "rows": None,
        }
    sums = weights.sum(axis=1)
    representative: dict[int, int] = {}
    for state, label in enumerate(labels):
        representative.setdefault(int(label), state)
    rows = []
    for block in blocks:
        total, masses = _masses(representative[block], weights, sums, labels)
        rows.append([
            fraction_payload(Fraction(masses.get(target, 0), total))
            for target in blocks
        ])
    return {
        "defined": True,
        "reason": "strong lumpability",
        "blocks": blocks,
        "rows": rows,
    }


def fraction_payload(value: Fraction) -> dict:
    return {
        "num": str(value.numerator),
        "den": str(value.denominator),
        "float": float(value),
    }


def event_shape_holds(weights: np.ndarray, visible: list[int]) -> bool:
    """One toggle changes the packed interface by at most one bit."""
    size, width = weights.shape
    bits = visible

    def pack(state: int) -> int:
        packed = 0
        for place, bit in enumerate(bits):
            if (state >> bit) & 1:
                packed |= 1 << place
        return packed

    for state in range(size):
        for edge in range(width):
            if int(weights[state, edge]) == 0:
                continue
            before = pack(state)
            after = pack(state ^ (1 << edge))
            if (before ^ after).bit_count() > 1:
                return False
    return True


def grammar_form(weights: np.ndarray, labels: list[int], hidden: list[int], visible: list[int], exact: bool) -> dict:
    shape = event_shape_holds(weights, visible)
    if not shape:
        return {"event_shape": "not_single_toggle", "form": "outside_grammar", "interface_markov": False}
    if not exact:
        return {
            "event_shape": "single_toggle_or_hold",
            "form": "not_markovian_on_interface",
            "interface_markov": False,
        }
    sums = weights.sum(axis=1)
    representatives: dict[int, int] = {}
    for state, label in enumerate(labels):
        representatives.setdefault(int(label), state)
    holds = []
    flips = []
    for state in representatives.values():
        total = int(sums[state])
        if total == 0:
            holds.append(Fraction(1))
            flips.append(tuple(Fraction(0) for _ in visible))
            continue
        hold = Fraction(sum(int(weights[state, bit]) for bit in hidden), total)
        flip = tuple(Fraction(int(weights[state, bit]), total) for bit in visible)
        if hold + sum(flip) != 1:
            raise RuntimeError("interface probabilities do not sum to 1")
        holds.append(hold)
        flips.append(flip)
    flat = [value for row in flips for value in row]
    if len(set(holds)) == 1 and len(set(flat)) == 1:
        form = "unconstrained_lazy"
    else:
        form = "reweighted_single_toggle"
    return {
        "event_shape": "single_toggle_or_hold",
        "form": form,
        "interface_markov": True,
        "hold": fraction_payload(holds[0]) if holds else None,
        "n_interface_rows": len(representatives),
    }


def lumpable_closure(weights: np.ndarray, labels: list[int]) -> dict:
    """Split blocks until the partition is strongly lumpable.

    The returned block count is exact: termination means each current block
    has one next-block signature, which is strong lumpability.
    """
    size, _width = weights.shape
    current = [int(label) for label in labels]
    sums = weights.sum(axis=1)
    iterations = 0
    while True:
        keys = []
        for state in range(size):
            total, masses = _masses(state, weights, sums, current)
            keys.append((current[state], _signature_key(total, masses)))
        by_label: dict[int, set] = defaultdict(set)
        for label, signature in keys:
            by_label[label].add(signature)
        if all(len(signatures) == 1 for signatures in by_label.values()):
            return {
                "computed": True,
                "exact": True,
                "n_blocks": len(by_label),
                "iterations": iterations,
            }
        renumber: dict = {}
        successor = [0] * size
        for state, key in enumerate(keys):
            if key not in renumber:
                renumber[key] = len(renumber)
            successor[state] = renumber[key]
        current = successor
        iterations += 1
        if iterations > size:
            return {"computed": True, "exact": False, "n_blocks": None, "iterations": iterations}


def support_successors(weights: np.ndarray) -> tuple[list[list[int]], int]:
    size, width = weights.shape
    successors: list[list[int]] = []
    deadlocks = 0
    for state in range(size):
        targets = []
        for edge in range(width):
            if int(weights[state, edge]) != 0:
                targets.append(state ^ (1 << edge))
        if not targets:
            deadlocks += 1
            targets = [state]
        successors.append(targets)
    return successors, deadlocks


def strongly_connected_components(successors: list[list[int]]) -> list[list[int]]:
    """Iterative Kosaraju. The hypercube is deep enough to break recursion."""
    size = len(successors)
    seen = [False] * size
    finish: list[int] = []
    for start in range(size):
        if seen[start]:
            continue
        stack = [(start, 0)]
        seen[start] = True
        while stack:
            vertex, cursor = stack[-1]
            row = successors[vertex]
            if cursor < len(row):
                stack[-1] = (vertex, cursor + 1)
                nxt = row[cursor]
                if not seen[nxt]:
                    seen[nxt] = True
                    stack.append((nxt, 0))
            else:
                stack.pop()
                finish.append(vertex)
    transpose: list[list[int]] = [[] for _ in range(size)]
    for vertex, row in enumerate(successors):
        for nxt in row:
            transpose[nxt].append(vertex)
    seen = [False] * size
    components: list[list[int]] = []
    for start in reversed(finish):
        if seen[start]:
            continue
        stack = [start]
        seen[start] = True
        component: list[int] = []
        while stack:
            vertex = stack.pop()
            component.append(vertex)
            for nxt in transpose[vertex]:
                if not seen[nxt]:
                    seen[nxt] = True
                    stack.append(nxt)
        components.append(component)
    return components


def recurrent_class_count(weights: np.ndarray) -> dict:
    successors, deadlocks = support_successors(weights)
    recurrent = 0
    for component in strongly_connected_components(successors):
        members = set(component)
        leaves = False
        for state in component:
            for nxt in successors[state]:
                if nxt not in members:
                    leaves = True
                    break
            if leaves:
                break
        if not leaves:
            recurrent += 1
    return {
        "deadlock_states": deadlocks,
        "recurrent_classes": recurrent,
        "halt_completion": HALT_COMPLETION,
    }


def describe_state(state: int, edges: list[tuple[int, int]]) -> dict:
    present = [[a, b] for bit, (a, b) in enumerate(edges) if (state >> bit) & 1]
    return {"mask": int(state), "edges": present}


def check_state_independent_identity(
    weights: np.ndarray,
    labels: list[int],
    hidden: list[int],
    visible: list[int],
) -> dict:
    """Positive state-independent rates are strongly lumpable on every edge subset.

    The row check is that state 0 toggles edge ``e`` with probability ``r_e / R``
    and that every other row has the same rates. The lumpability check is that
    those rates induce one next-interface law per interface block. A packing
    bug fails the second check even when the rates themselves are constant.
    """
    prototype = [int(value) for value in weights[0]]
    if not bool(np.all(weights == weights[0])):
        return {"ok": False, "reason": "weights depend on the state"}
    total = sum(prototype)
    if total <= 0 or any(rate <= 0 for rate in prototype):
        return {"ok": False, "reason": "identity requires every rate positive"}
    report = lumpability(weights, labels)
    if not report["exact"]:
        return {"ok": False, "reason": "interface partition is not strongly lumpable", "defect": fraction_payload(report["defect_l1"])}
    sums = weights.sum(axis=1)
    total_0, masses = _masses(0, weights, sums, labels)
    expected_hold = Fraction(sum(prototype[bit] for bit in hidden), total)
    # Reconstruct hold from the self-block mass only when every hidden toggle
    # stays in the block and no visible toggle does. That is the event shape.
    self_block = int(labels[0])
    if Fraction(masses.get(self_block, 0), total_0) != expected_hold:
        return {"ok": False, "reason": "hold mass does not match the hidden rates"}
    for bit in visible:
        if Fraction(prototype[bit], total) != Fraction(int(weights[0, bit]), total):
            return {"ok": False, "reason": "flip rate does not match the row"}
    return {
        "ok": True,
        "hold": fraction_payload(expected_hold),
        "total_rate": total,
        "checked_states": int(weights.shape[0]),
    }


def _transition_probabilities(weights: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    floats = weights.astype(np.float64)
    sums = floats.sum(axis=1)
    dead = sums <= 0
    safe = np.where(dead, 1.0, sums)
    probabilities = floats / safe[:, None]
    probabilities[dead] = 0.0
    return probabilities, dead


def step_distribution(probabilities: np.ndarray, dead: np.ndarray, distribution: np.ndarray) -> np.ndarray:
    size, width = probabilities.shape
    states = np.arange(size, dtype=np.int64)
    nxt = np.zeros(size, dtype=np.float64)
    for edge in range(width):
        np.add.at(nxt, states ^ (1 << edge), distribution * probabilities[:, edge])
    if dead.any():
        nxt[dead] += distribution[dead]
    total = nxt.sum()
    if total <= 0:
        raise RuntimeError("transition destroyed probability mass")
    nxt /= total
    return nxt


def stationary_balanced(
    weights: np.ndarray,
    start: str,
    tolerance: float,
    max_iter: int,
) -> dict:
    """Stationary law by averaging a distribution with its one-step image.

    A positive single-toggle chain with no self-loop is periodic of period 2:
    every event flips the parity of the edge count, so plain power iteration
    oscillates and a Cesaro mean from step 0 keeps a 1/t bias. The average of
    a law and its image cancels the eigenvalue -1. Successive averages then
    converge geometrically to the unique stationary law when every weight is
    positive. A self-loop removes the periodicity; the same iteration still
    converges when the stationary law is unique. Callers cross-check two
    starts and, where the state count fits, a dense linear solve.
    """
    probabilities, dead = _transition_probabilities(weights)
    size = probabilities.shape[0]
    if start == "uniform":
        current = np.full(size, 1.0 / size)
    elif start == "empty":
        current = np.zeros(size)
        current[0] = 1.0
    else:
        raise ValueError(f"unknown start {start}")
    previous = None
    residual = float("inf")
    estimate = current
    for iteration in range(1, max_iter + 1):
        nxt = step_distribution(probabilities, dead, current)
        estimate = 0.5 * (current + nxt)
        if previous is not None:
            residual = float(np.abs(estimate - previous).sum())
            if residual < tolerance:
                image_gap = float(
                    np.abs(estimate - step_distribution(probabilities, dead, estimate)).sum()
                )
                return {
                    "distribution": estimate,
                    "iterations": iteration,
                    "residual": residual,
                    "image_gap": image_gap,
                    "converged": True,
                    "start": start,
                }
        previous = estimate.copy()
        current = nxt
    image_gap = float(np.abs(estimate - step_distribution(probabilities, dead, estimate)).sum())
    return {
        "distribution": estimate,
        "iterations": max_iter,
        "residual": residual,
        "image_gap": image_gap,
        "converged": False,
        "start": start,
    }


def stationary_dense(weights: np.ndarray) -> np.ndarray:
    """Solve ``pi P = pi`` by replacing one dependent equation with the sum."""
    probabilities, dead = _transition_probabilities(weights)
    size, width = probabilities.shape
    states = np.arange(size, dtype=np.int64)
    matrix = np.zeros((size, size), dtype=np.float64)
    for state in range(size):
        if dead[state]:
            matrix[state, state] = 1.0
            continue
        for edge in range(width):
            matrix[state, int(states[state] ^ (1 << edge))] += probabilities[state, edge]
    system = np.eye(size) - matrix.T
    system[-1, :] = 1.0
    target = np.zeros(size)
    target[-1] = 1.0
    solution = np.linalg.solve(system, target)
    solution = np.real(solution)
    solution[solution < 0] = 0.0
    total = solution.sum()
    if total <= 0:
        raise RuntimeError("dense stationary solve returned no mass")
    return solution / total


def edge_presence(distribution: np.ndarray) -> np.ndarray:
    size = distribution.shape[0]
    width = int(math.log2(size))
    if 1 << width != size:
        raise ValueError("distribution length is not a power of two")
    states = np.arange(size)
    presence = np.zeros(width)
    for edge in range(width):
        presence[edge] = float(distribution[(states >> edge) & 1 == 1].sum())
    return presence


def toggle_rates(distribution: np.ndarray, weights: np.ndarray) -> np.ndarray:
    probabilities, _dead = _transition_probabilities(weights)
    return (distribution[:, None] * probabilities).sum(axis=0)


def pair_depth(edges: list[tuple[int, int]]) -> list[int]:
    """Declared path-index depth: the smaller endpoint label.

    This is not hop distance in the complete graph of potential pairs, and
    it is not a discovered geometry.
    """
    return [min(a, b) for a, b in edges]


def state_independent_rate_identity(weights: np.ndarray) -> dict | None:
    prototype = weights[0]
    if not np.array_equal(weights, np.broadcast_to(prototype, weights.shape)):
        return None
    rates = np.array([int(value) for value in prototype], dtype=np.float64)
    total = float(rates.sum())
    if total <= 0 or np.any(rates <= 0):
        return None
    return {"occupation": 0.5, "toggle_rate": (rates / total).tolist(), "total_rate": total}
