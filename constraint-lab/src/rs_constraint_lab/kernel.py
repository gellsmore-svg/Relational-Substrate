"""Constrained toggle kernels.

The unconstrained kernel gives every edge toggle weight 1. A constraint
multiplies the weight of a toggle it matches. The resulting weights are
normalised per state. If every weight is 0, the admissible set is empty.
That state halts. The Markov completion used for class and stationary
analysis is a self-loop, recorded as ``HALT_COMPLETION`` and not counted
as a relational event.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from rs_constraint_lab.constraints import Choreography
from rs_constraint_lab.state import edge_count

HALT_COMPLETION = "self_loop_marked_kernel_undefined"


@dataclass(frozen=True)
class Kernel:
    n: int
    n_states: int
    n_edges: int
    successors: tuple[tuple[tuple[int, Fraction], ...], ...]
    weights: tuple[tuple[Fraction, ...], ...]
    deadlock: tuple[bool, ...]
    completion: str = HALT_COMPLETION

    def probability(self, state: int, nxt: int) -> Fraction:
        for target, prob in self.successors[state]:
            if target == nxt:
                return prob
        return Fraction(0)


def build_kernel(n: int, choreography: Choreography, factors: dict[str, Fraction]) -> Kernel:
    slots = edge_count(n)
    size = 1 << slots
    successors: list[tuple[tuple[int, Fraction], ...]] = []
    weights: list[tuple[Fraction, ...]] = []
    deadlock: list[bool] = []
    for state in range(size):
        active = choreography.active(state, (), {})
        row_weights: list[Fraction] = []
        for edge in range(slots):
            weight = Fraction(1)
            for constraint in active:
                if constraint.matches(state, edge):
                    weight *= factors[constraint.weight]
            row_weights.append(weight)
        weights.append(tuple(row_weights))
        total = sum(row_weights)
        if total == 0:
            deadlock.append(True)
            successors.append(((state, Fraction(1)),))
            continue
        deadlock.append(False)
        outgoing = []
        for edge, weight in enumerate(row_weights):
            if weight != 0:
                outgoing.append((state ^ (1 << edge), weight / total))
        successors.append(tuple(outgoing))
    return Kernel(n, size, slots, tuple(successors), tuple(weights), tuple(deadlock))


def kernel_fingerprint(kernel: Kernel) -> str:
    parts = []
    for state, row in enumerate(kernel.successors):
        rendered = ",".join(f"{nxt}:{prob.numerator}/{prob.denominator}" for nxt, prob in row)
        parts.append(f"{state}:{rendered}")
    return "\n".join(parts)


def modal_map(kernel: Kernel) -> tuple[tuple[str, ...], ...]:
    """Per state, the toggles of maximal weight, or ``halt`` when the kernel is empty."""
    rows: list[tuple[str, ...]] = []
    for state, row_weights in enumerate(kernel.weights):
        if kernel.deadlock[state]:
            rows.append(("halt",))
            continue
        best = max(row_weights)
        chosen = tuple(str(edge) for edge, weight in enumerate(row_weights) if weight == best)
        rows.append(chosen)
    return tuple(rows)


def support_map(kernel: Kernel) -> tuple[tuple[str, ...], ...]:
    rows: list[tuple[str, ...]] = []
    for state, row in enumerate(kernel.successors):
        if kernel.deadlock[state]:
            rows.append(("halt",))
        else:
            rows.append(tuple(str(nxt) for nxt, _prob in row))
    return tuple(rows)
