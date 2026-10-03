"""Neutral observables.

Names in this module describe the transition kernel and the trajectories it
generates. They do not name interpretive outcomes.
"""

from __future__ import annotations

import hashlib
import math
from fractions import Fraction

from rs_constraint_lab.exact import long_run, period_of, recurrent_components, reachable_from
from rs_constraint_lab.kernel import Kernel, modal_map, support_map
from rs_constraint_lab.state import component_count, edges


def _sha(payload: tuple) -> str:
    return hashlib.sha256(repr(payload).encode("utf-8")).hexdigest()[:16]


def _fraction_text(value: Fraction | None) -> str | None:
    if value is None:
        return None
    return f"{value.numerator}/{value.denominator}"


def light_observables(kernel: Kernel, baseline: Kernel) -> dict:
    deadlocks = [state for state, halted in enumerate(kernel.deadlock) if halted]
    recurrent = recurrent_components(kernel)
    periods = sorted({period_of(component, kernel.successors) for component in recurrent})
    reachable = reachable_from(kernel, 0)
    reachable_recurrent = sum(
        1 for component in recurrent if any(state in reachable for state in component)
    )
    max_shift = Fraction(0)
    sum_shift = Fraction(0)
    counted = 0
    for state in range(kernel.n_states):
        if kernel.deadlock[state]:
            continue
        occupied = state.bit_count()
        dissolve = Fraction(0)
        for nxt, prob in kernel.successors[state]:
            if nxt.bit_count() < occupied:
                dissolve += prob
        baseline_dissolve = Fraction(occupied, kernel.n_edges)
        shift = abs(dissolve - baseline_dissolve)
        if shift > max_shift:
            max_shift = shift
        sum_shift += shift
        counted += 1
    closing = _closing_bias_exact(kernel)
    mean_shift = (sum_shift / counted) if counted else Fraction(0)
    modes = modal_map(kernel)
    support = support_map(kernel)
    base_support = support_map(baseline)
    return {
        "n_deadlock": len(deadlocks),
        "deadlock_states": deadlocks,
        "n_recurrent": len(recurrent),
        "n_recurrent_reachable_from_empty": reachable_recurrent,
        "periods": periods,
        "reachable_from_empty": len(reachable),
        "max_abs_dissolve_shift": float(max_shift),
        "max_abs_dissolve_shift_exact": _fraction_text(max_shift),
        "mean_abs_dissolve_shift": float(mean_shift),
        "mean_abs_dissolve_shift_exact": _fraction_text(mean_shift),
        "closing_bias": None if closing is None else float(closing),
        "closing_bias_exact": _fraction_text(closing),
        "support_matches_baseline": support == base_support,
        "modal_family": _sha((kernel.n, modes)),
        "support_family": _sha((kernel.n, support)),
        "modes": modes,
    }


def _closing_bias_exact(kernel: Kernel) -> Fraction | None:
    """Mean P(form the missing edge | exactly two edges are present), minus 1/3.

    Defined only for the three-edge system. The baseline probability on each
    such state is 1/3, so the baseline bias is 0. A two-edge deadlock
    contributes probability 0. Deadlock counts are recorded separately.
    The value is a rational function of the kernel rows at every N for which
    the predicate is defined; it does not go through the stationary solve.
    """
    if kernel.n_edges != 3:
        return None
    values = []
    for state in range(kernel.n_states):
        if state.bit_count() != 2:
            continue
        if kernel.deadlock[state]:
            values.append(Fraction(0))
            continue
        missing = next(bit for bit in range(3) if ((state >> bit) & 1) == 0)
        target = state | (1 << missing)
        probability = Fraction(0)
        for nxt, prob in kernel.successors[state]:
            if nxt == target:
                probability += prob
        values.append(probability)
    if not values:
        return None
    return sum(values, Fraction(0)) / len(values) - Fraction(1, 3)


def rise_then_release_probability(kernel: Kernel, horizon: int = 4, start: int = 0) -> Fraction:
    """Probability that some length-``horizon`` path from ``start`` rises by 2 then falls by 1."""
    total = Fraction(0)

    def matches(counts: list[int]) -> bool:
        for i, left in enumerate(counts):
            for j in range(i + 1, len(counts)):
                if counts[j] < left + 2:
                    continue
                for right in counts[j + 1 :]:
                    if right <= counts[j] - 1:
                        return True
        return False

    def walk(state: int, prob: Fraction, counts: list[int]) -> None:
        nonlocal total
        if len(counts) == horizon + 1:
            if matches(counts):
                total += prob
            return
        for nxt, step in kernel.successors[state]:
            if step == 0:
                continue
            counts.append(nxt.bit_count())
            walk(nxt, prob * step, counts)
            counts.pop()

    walk(start, Fraction(1), [start.bit_count()])
    return total


def _text(value: Fraction | None) -> str | None:
    if value is None:
        return None
    return f"{value.numerator}/{value.denominator}"


def heavy_observables(kernel: Kernel, horizon: int = 4, start: int = 0) -> dict:
    ran = long_run(kernel, start)
    pi_exact = ran["distribution_exact"]
    pi = ran["distribution"]
    entropy = 0.0
    edge_list = edges(kernel.n)
    rise_exact = None
    if kernel.n_states <= 64:
        rise_exact = rise_then_release_probability(kernel, horizon, start)
    if pi_exact is not None:
        density_sum = sum((mass * state.bit_count() for state, mass in pi_exact.items()), Fraction(0))
        component_sum = sum(
            (mass * component_count(state, kernel.n, edge_list) for state, mass in pi_exact.items()),
            Fraction(0),
        )
        occupancy = [Fraction(0) for _ in range(kernel.n_edges + 1)]
        halt_mass = Fraction(0)
        for state, mass in pi_exact.items():
            occupancy[state.bit_count()] += mass
            if kernel.deadlock[state]:
                halt_mass += mass
            mass_float = float(mass)
            for _nxt, prob in kernel.successors[state]:
                probability = float(prob)
                if probability > 0.0 and mass_float > 0.0:
                    entropy -= mass_float * probability * math.log(probability)
        uniform = Fraction(1, kernel.n_states)
        tv = Fraction(1, 2) * sum(
            (abs(pi_exact.get(state, Fraction(0)) - uniform) for state in range(kernel.n_states)),
            Fraction(0),
        )
        defect = _reversibility_defect_exact(kernel, pi_exact)
        density = density_sum / kernel.n_edges
        triangle = pi_exact.get(kernel.n_states - 1, Fraction(0)) if kernel.n == 3 else None
        disjoint = None
        occupancy_out = [float(item) for item in occupancy]
        occupancy_exact = [_text(item) for item in occupancy]
        density_exact = _text(density)
        tv_exact = _text(tv)
        defect_exact = _text(defect)
        halt_exact = _text(halt_mass)
        triangle_exact = _text(triangle) if triangle is not None else None
        disjoint_exact = None
        density_float = float(density)
        tv_float = float(tv)
        defect_float = float(defect)
        halt_float = float(halt_mass)
        triangle_float = None if triangle is None else float(triangle)
        component_float = float(component_sum)
    else:
        density_sum = 0.0
        component_sum_float = 0.0
        occupancy_out = [0.0 for _ in range(kernel.n_edges + 1)]
        halt_float = 0.0
        for state, mass in pi.items():
            occupied = state.bit_count()
            density_sum += mass * occupied
            occupancy_out[occupied] += mass
            component_sum_float += mass * component_count(state, kernel.n, edge_list)
            if kernel.deadlock[state]:
                halt_float += mass
            for _nxt, prob in kernel.successors[state]:
                probability = float(prob)
                if probability > 0.0 and mass > 0.0:
                    entropy -= mass * probability * math.log(probability)
        uniform = 1.0 / kernel.n_states
        tv_float = 0.5 * sum(abs(pi.get(state, 0.0) - uniform) for state in range(kernel.n_states))
        defect_float = _reversibility_defect(kernel, pi)
        density_float = density_sum / kernel.n_edges
        triangle_float = pi.get(kernel.n_states - 1, 0.0) if kernel.n == 3 else None
        disjoint = None
        if kernel.n == 4:
            # The three perfect matchings on four labelled vertices:
            # edges (01,23), (02,13), (03,12) in the lexicographic edge order.
            disjoint = pi.get(33, 0.0) + pi.get(18, 0.0) + pi.get(12, 0.0)
        occupancy_exact = None
        density_exact = None
        tv_exact = None
        defect_exact = None
        halt_exact = None
        triangle_exact = None
        disjoint_exact = None
        component_float = component_sum_float
    return {
        "mean_edge_density": density_float,
        "mean_edge_density_exact": density_exact,
        "edge_count_occupancy": occupancy_out,
        "edge_count_occupancy_exact": occupancy_exact,
        "mean_component_count": component_float,
        "entropy_rate_nats": entropy,
        "entropy_rate_bits": entropy / math.log(2),
        "tv_from_uniform": tv_float,
        "tv_from_uniform_exact": tv_exact,
        "reversibility_defect": defect_float,
        "reversibility_defect_exact": defect_exact,
        "halt_mass": halt_float,
        "halt_mass_exact": halt_exact,
        "triangle_mass": triangle_float,
        "triangle_mass_exact": triangle_exact,
        "disjoint_pair_mass": disjoint,
        "disjoint_pair_mass_exact": disjoint_exact,
        "rise_then_release": None if rise_exact is None else float(rise_exact),
        "rise_then_release_exact": _text(rise_exact),
        "stationary_arithmetic": ran["stationary_arithmetic"],
        "stationary_residual": ran["stationary_residual"],
        "n_recurrent": ran["n_recurrent"],
        "periods": ran["periods"],
        "reachable_count": ran["reachable_count"],
    }


def _reversibility_defect_exact(kernel: Kernel, pi: dict[int, Fraction]) -> Fraction:
    defect = Fraction(0)
    for state, row in enumerate(kernel.successors):
        mass = pi.get(state, Fraction(0))
        for nxt, prob in row:
            reverse = Fraction(0)
            for back, back_prob in kernel.successors[nxt]:
                if back == state:
                    reverse += back_prob
            gap = abs(mass * prob - pi.get(nxt, Fraction(0)) * reverse)
            if gap > defect:
                defect = gap
    return defect


def _reversibility_defect(kernel: Kernel, pi: dict[int, float]) -> float:
    defect = 0.0
    for state, row in enumerate(kernel.successors):
        mass = pi.get(state, 0.0)
        for nxt, prob in row:
            reverse = 0.0
            for back, back_prob in kernel.successors[nxt]:
                if back == state:
                    reverse += float(back_prob)
            flow_gap = abs(mass * float(prob) - pi.get(nxt, 0.0) * reverse)
            if flow_gap > defect:
                defect = flow_gap
    return defect


def equivalent_kernel(kernel: Kernel, baseline: Kernel) -> bool:
    return kernel.successors == baseline.successors


def neutral_sentence(light: dict) -> str:
    sentences = []
    if light["n_deadlock"]:
        sentences.append(
            f"{light['n_deadlock']} states have an empty admissible set and halt"
        )
    else:
        sentences.append("every state has at least one admissible toggle")
    sentences.append(f"{light['n_recurrent']} recurrent class(es) with periods {light['periods']}")
    if light["support_matches_baseline"]:
        sentences.append("the admissible transition graph is the full toggle hypercube")
    else:
        sentences.append("the admissible transition graph is a proper subgraph of the toggle hypercube")
    shift = light["max_abs_dissolve_shift"]
    sentences.append(f"the largest one-step dissolution-probability deviation from m/M is {shift:.6f}")
    if light["closing_bias"] is not None:
        sentences.append(
            f"the two-edge closing probability differs from 1/3 by {light['closing_bias']:.6f}"
        )
    return "; ".join(sentences) + "."
