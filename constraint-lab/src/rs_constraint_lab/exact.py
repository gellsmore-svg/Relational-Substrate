"""Exact finite-state analysis of a toggle kernel.

Structural facts (support, communicating classes, period, deadlocks) are
exact. On state spaces of size at most 16 the stationary distribution and
absorption probabilities are rational. Larger spaces use float64 with a
recorded residual, and a Cesaro average if the linear solve is unstable.
"""

from __future__ import annotations

import math
from collections import deque
from fractions import Fraction

import numpy as np

from rs_constraint_lab.kernel import Kernel


def strongly_connected_components(successors) -> list[list[int]]:
    """Iterative Kosaraju.

    The toggle hypercube has a Hamiltonian path, so a recursive depth-first
    search exceeds the interpreter stack once the state space reaches 1,024.
    """
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
                nxt = row[cursor][0]
                if not seen[nxt]:
                    seen[nxt] = True
                    stack.append((nxt, 0))
            else:
                stack.pop()
                finish.append(vertex)
    transpose: list[list[int]] = [[] for _ in range(size)]
    for vertex, row in enumerate(successors):
        for nxt, _prob in row:
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


def recurrent_components(kernel: Kernel) -> list[list[int]]:
    recurrent = []
    for component in strongly_connected_components(kernel.successors):
        members = set(component)
        leaves = False
        for state in component:
            for nxt, prob in kernel.successors[state]:
                if prob > 0 and nxt not in members:
                    leaves = True
                    break
            if leaves:
                break
        if not leaves:
            recurrent.append(component)
    return recurrent


def period_of(component: list[int], successors) -> int:
    if len(component) == 1:
        return 1
    members = set(component)
    start = component[0]
    level = {start: 0}
    queue: deque[int] = deque([start])
    divisor = 0
    while queue:
        state = queue.popleft()
        for nxt, prob in successors[state]:
            if prob == 0 or nxt not in members:
                continue
            if nxt not in level:
                level[nxt] = level[state] + 1
                queue.append(nxt)
            else:
                divisor = math.gcd(divisor, abs(level[state] + 1 - level[nxt]))
    return divisor or 1


def reachable_from(kernel: Kernel, start: int) -> set[int]:
    seen = {start}
    queue = [start]
    while queue:
        state = queue.pop()
        for nxt, prob in kernel.successors[state]:
            if prob > 0 and nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def _solve_fraction(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    size = len(vector)
    augmented = [row[:] + [vector[i]] for i, row in enumerate(matrix)]
    for col in range(size):
        pivot = next((row for row in range(col, size) if augmented[row][col] != 0), None)
        if pivot is None:
            raise ZeroDivisionError("singular stationary system")
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        scale = augmented[col][col]
        for column in range(col, size + 1):
            augmented[col][column] /= scale
        for row in range(size):
            if row == col or augmented[row][col] == 0:
                continue
            factor = augmented[row][col]
            for column in range(col, size + 1):
                augmented[row][column] -= factor * augmented[col][column]
    return [augmented[i][size] for i in range(size)]


def _stationary_rational(component: list[int], successors) -> dict[int, Fraction]:
    if len(component) == 1:
        return {component[0]: Fraction(1)}
    position = {state: i for i, state in enumerate(component)}
    size = len(component)
    transition = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    for state in component:
        for nxt, prob in successors[state]:
            transition[position[state]][position[nxt]] += prob
    matrix = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    vector = [Fraction(0) for _ in range(size)]
    for column in range(size - 1):
        for row in range(size):
            matrix[column][row] = transition[row][column]
        matrix[column][column] -= 1
    for row in range(size):
        matrix[size - 1][row] = 1
    vector[size - 1] = 1
    solution = _solve_fraction(matrix, vector)
    return {state: solution[position[state]] for state in component}


def _stationary_float(component: list[int], successors) -> tuple[dict[int, float], float, str]:
    if len(component) == 1:
        return {component[0]: 1.0}, 0.0, "float64"
    position = {state: i for i, state in enumerate(component)}
    size = len(component)
    transition = np.zeros((size, size))
    for state in component:
        for nxt, prob in successors[state]:
            transition[position[state], position[nxt]] += float(prob)
    matrix = np.eye(size) - transition.T
    matrix[-1, :] = 1.0
    vector = np.zeros(size)
    vector[-1] = 1.0
    method = "float64"
    try:
        solution = np.linalg.solve(matrix, vector)
        residual = float(np.max(np.abs(solution @ transition - solution)))
        if residual > 1e-8 or float(np.min(solution)) < -1e-8:
            raise np.linalg.LinAlgError("unstable solve")
    except np.linalg.LinAlgError:
        method = "cesaro"
        current = np.ones(size) / size
        accumulator = np.zeros(size)
        steps = max(400, 8 * size)
        for _ in range(steps):
            current = current @ transition
            accumulator += current
        solution = accumulator / steps
        residual = float(np.max(np.abs(solution @ transition - solution)))
    solution = np.clip(solution, 0.0, None)
    total = float(solution.sum())
    solution = solution / total
    return {state: float(solution[position[state]]) for state in component}, residual, method


def _absorption_weights(
    kernel: Kernel,
    start: int,
    recurrent: list[list[int]],
    rational: bool,
):
    """Absorption probabilities. Rational when requested, otherwise float64.

    The rational branch stays in ``Fraction`` so callers can keep exact
    stationary mixtures. The float list returned for the historical
    ``absorption`` field is derived from those fractions at the boundary.
    """
    member_class: dict[int, int] = {}
    for index, component in enumerate(recurrent):
        for state in component:
            member_class[state] = index
    if start in member_class:
        if rational:
            weights = [Fraction(0) for _ in recurrent]
            weights[member_class[start]] = Fraction(1)
            return weights
        weights_float = [0.0] * len(recurrent)
        weights_float[member_class[start]] = 1.0
        return weights_float
    transient = [state for state in range(kernel.n_states) if state not in member_class]
    position = {state: i for i, state in enumerate(transient)}
    size = len(transient)
    if rational:
        base = [[Fraction(0) for _ in range(size)] for _ in range(size)]
        for state in transient:
            for nxt, prob in kernel.successors[state]:
                if nxt in position:
                    base[position[state]][position[nxt]] += prob
        matrix = [[Fraction(1 if i == j else 0) - base[i][j] for j in range(size)] for i in range(size)]
        heights = []
        for component in recurrent:
            members = set(component)
            vector = [Fraction(0) for _ in range(size)]
            for state in transient:
                for nxt, prob in kernel.successors[state]:
                    if nxt in members:
                        vector[position[state]] += prob
            heights.append(_solve_fraction(matrix, vector))
        raw = [height[position[start]] for height in heights]
    else:
        base = np.zeros((size, size))
        for state in transient:
            for nxt, prob in kernel.successors[state]:
                if nxt in position:
                    base[position[state], position[nxt]] += float(prob)
        matrix = np.eye(size) - base
        raw = []
        for component in recurrent:
            members = set(component)
            vector = np.zeros(size)
            for state in transient:
                for nxt, prob in kernel.successors[state]:
                    if nxt in members:
                        vector[position[state]] += float(prob)
            raw.append(float(np.linalg.solve(matrix, vector)[position[start]]))
    total = sum(raw)
    if total <= 0:
        raise RuntimeError(f"no recurrent class is reachable from state {start}")
    return [value / total for value in raw]


def long_run(kernel: Kernel, start: int = 0) -> dict:
    recurrent = recurrent_components(kernel)
    rational = kernel.n_states <= 16
    exact_classes = []
    float_classes = []
    residual = 0.0
    method = "rational" if rational else "float64"
    for component in recurrent:
        if rational:
            exact = _stationary_rational(component, kernel.successors)
            exact_classes.append(exact)
            float_classes.append({state: float(value) for state, value in exact.items()})
        else:
            dist, class_residual, class_method = _stationary_float(component, kernel.successors)
            exact_classes.append(None)
            float_classes.append(dist)
            residual = max(residual, class_residual)
            if class_method != "float64":
                method = class_method
    weights = _absorption_weights(kernel, start, recurrent, rational)
    pi: dict[int, float] = {}
    pi_exact: dict[int, Fraction] | None
    if rational:
        pi_exact = {}
        for weight, dist in zip(weights, exact_classes):
            for state, prob in dist.items():
                pi_exact[state] = pi_exact.get(state, Fraction(0)) + weight * prob
        for state, prob in pi_exact.items():
            pi[state] = float(prob)
        weights_float = [float(weight) for weight in weights]
    else:
        pi_exact = None
        weights_float = list(weights)
        for weight, dist in zip(weights_float, float_classes):
            for state, prob in dist.items():
                pi[state] = pi.get(state, 0.0) + weight * prob
    reachable = reachable_from(kernel, start)
    reachable_recurrent = []
    for index, component in enumerate(recurrent):
        if any(state in reachable for state in component):
            reachable_recurrent.append(index)
    periods = sorted({period_of(component, kernel.successors) for component in recurrent})
    return {
        "distribution": pi,
        "distribution_exact": pi_exact,
        "absorption": weights_float,
        "absorption_exact": list(weights) if rational else None,
        "n_recurrent": len(recurrent),
        "n_recurrent_reachable_from_start": len(reachable_recurrent),
        "periods": periods,
        "stationary_arithmetic": method,
        "stationary_residual": residual,
        "reachable_count": len(reachable),
    }
