"""Two clocks for coarse-grained pairwise memory.

FULL_EVENT_CLOCK observes the pairwise projection after every full-system
event. A triadic toggle that leaves the pairs unchanged is a visible self-loop.

PAIR_EVENT_EPOCH observes the pairwise state only when a pairwise relation
toggles. Triad-only events are skipped. Q_i is the pairwise state immediately
after the i-th such toggle.

The full chain stays first-order Markov. A positive total variation is
emergent memory under that coarse-graining, not a fundamental history variable.
Rational arithmetic is used when the state space has at most 16 points.
Larger spaces use float64 and are not described as exact.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

from rs_constraint_lab.exact import long_run
from rs_constraint_lab.kernel import Kernel

# Float total variation at or below this floor is recorded as zero.
# It is a numerical threshold, not an exact identity.
FLOAT_TV_FLOOR = 1e-8
FLOAT_RESIDUAL_LIMIT = 1e-6


def layout(kernel: Kernel) -> tuple[int, int]:
    """Pair slots occupy the low bits. Triad slots occupy the bits above them."""
    slots = kernel.relation_slots
    if not slots:
        raise ValueError("memory clocks require an explicit relation-slot layout")
    n_pairs = 0
    n_triads = 0
    for slot in slots:
        if len(slot) == 2 and n_triads == 0:
            n_pairs += 1
        elif len(slot) == 3:
            n_triads += 1
        else:
            raise ValueError("relation slots must be all pairs, then all triads")
    if n_pairs < 1 or n_triads < 1:
        raise ValueError("memory clocks require at least one pair slot and one triad slot")
    if (1 << (n_pairs + n_triads)) != kernel.n_states:
        raise ValueError("state count does not match the slot layout")
    return n_pairs, n_triads


def _table(kernel: Kernel) -> list[dict[int, Fraction]]:
    return [{nxt: prob for nxt, prob in row} for row in kernel.successors]


def _pair_mask(n_pairs: int) -> int:
    return (1 << n_pairs) - 1


def _is_pair_move(source: int, target: int, mask: int) -> bool:
    return (source ^ target) & mask != 0


def _stationary_exact(kernel: Kernel) -> list[Fraction]:
    ran = long_run(kernel, 0)
    exact = ran["distribution_exact"]
    if exact is None:
        raise RuntimeError("rational stationary distribution is required")
    return [exact.get(state, Fraction(0)) for state in range(kernel.n_states)]


def _tv_dicts(left: dict[int, Fraction], right: dict[int, Fraction]) -> Fraction:
    keys = set(left) | set(right)
    total = sum((abs(left.get(key, Fraction(0)) - right.get(key, Fraction(0))) for key in keys), Fraction(0))
    return total / 2


def full_event_clock_memory_tv(kernel: Kernel, pi: list[Fraction] | None = None) -> Fraction:
    """Max TV between P(P'|P) and P(P'|P, P_prev) on the full-event clock.

    This is the Generation 3 memory statistic when there is one triadic bit.
    """
    n_pairs, n_triads = layout(kernel)
    n_p = 1 << n_pairs
    n_t = 1 << n_triads
    if pi is None:
        pi = _stationary_exact(kernel)
    table = _table(kernel)
    maximum = Fraction(0)
    for previous in range(n_p):
        for current in range(n_p):
            joint = Fraction(0)
            history = [Fraction(0) for _ in range(n_p)]
            for triad_prev in range(n_t):
                source = previous | (triad_prev << n_pairs)
                mass = pi[source]
                if mass == 0:
                    continue
                for triad_now in range(n_t):
                    middle = current | (triad_now << n_pairs)
                    step = table[source].get(middle, Fraction(0))
                    if step == 0:
                        continue
                    weight = mass * step
                    joint += weight
                    for triad_next in range(n_t):
                        for nxt in range(n_p):
                            follow = table[middle].get(nxt | (triad_next << n_pairs), Fraction(0))
                            if follow:
                                history[nxt] += weight * follow
            if joint == 0:
                continue
            current_mass = sum(
                (pi[current | (triad << n_pairs)] for triad in range(n_t)),
                Fraction(0),
            )
            if current_mass == 0:
                continue
            marginal = [Fraction(0) for _ in range(n_p)]
            for triad_now in range(n_t):
                middle = current | (triad_now << n_pairs)
                mass = pi[middle]
                if mass == 0:
                    continue
                for triad_next in range(n_t):
                    for nxt in range(n_p):
                        follow = table[middle].get(nxt | (triad_next << n_pairs), Fraction(0))
                        if follow:
                            marginal[nxt] += mass * follow
            tv = sum(
                (abs(history[nxt] / joint - marginal[nxt] / current_mass) for nxt in range(n_p)),
                Fraction(0),
            ) / 2
            if tv > maximum:
                maximum = tv
    return maximum


def _eventual_pair_states(table: list[dict[int, Fraction]], mask: int, deadlock: tuple[bool, ...]) -> list[int]:
    size = len(table)
    pair_exit = [False] * size
    predecessors: list[list[int]] = [[] for _ in range(size)]
    for source in range(size):
        if deadlock[source]:
            continue
        for target, prob in table[source].items():
            if prob == 0 or target == source:
                continue
            if _is_pair_move(source, target, mask):
                pair_exit[source] = True
            else:
                predecessors[target].append(source)
    seen = {state for state, flag in enumerate(pair_exit) if flag}
    queue = list(seen)
    while queue:
        target = queue.pop()
        for source in predecessors[target]:
            if source not in seen:
                seen.add(source)
                queue.append(source)
    return sorted(seen)


def _solve_fraction_columns(matrix: list[list[Fraction]], columns: list[list[Fraction]]) -> list[list[Fraction]]:
    """Solve one matrix against several right-hand sides.

    ``columns`` is a list of column vectors. The result is the same list of
    solution columns. One elimination keeps the exact Fraction arithmetic of
    solving each column alone.
    """
    size = len(matrix)
    width = len(columns)
    augmented = [row[:] + [columns[col][i] for col in range(width)] for i, row in enumerate(matrix)]
    for col in range(size):
        pivot = next((row for row in range(col, size) if augmented[row][col] != 0), None)
        if pivot is None:
            raise ZeroDivisionError("singular stationary system")
        if pivot != col:
            augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        scale = augmented[col][col]
        for column in range(col, size + width):
            augmented[col][column] /= scale
        for row in range(size):
            factor = augmented[row][col]
            if row == col or factor == 0:
                continue
            for column in range(col, size + width):
                augmented[row][column] -= factor * augmented[col][column]
    return [[augmented[i][size + col] for i in range(size)] for col in range(width)]


def _epoch_kernel_exact(kernel: Kernel) -> tuple[list[dict[int, Fraction]], Fraction]:
    """Landing kernel of the next pair toggle, and the largest missing mass.

    K[y][z] is the probability that the next pair-changing state is z when
    the chain is now at y. Triad-only moves are summed out. A missing mass
    is the probability that no further pair toggle occurs. Rows with a
    missing mass are renormalised so the kernel conditions on a next pair
    event existing. The defect records that missing mass before renormalisation.
    """
    n_pairs, _n_triads = layout(kernel)
    mask = _pair_mask(n_pairs)
    table = _table(kernel)
    seen = _eventual_pair_states(table, mask, kernel.deadlock)
    size = kernel.n_states
    empty: list[dict[int, Fraction]] = [{} for _ in range(size)]
    if not seen:
        return empty, Fraction(1)
    index = {state: row for row, state in enumerate(seen)}
    width = len(seen)
    matrix = [[Fraction(1 if i == j else 0) for j in range(width)] for i in range(width)]
    direct = [[Fraction(0) for _ in range(size)] for _ in range(width)]
    for state in seen:
        row = index[state]
        for target, prob in table[state].items():
            if prob == 0 or target == state:
                continue
            if _is_pair_move(state, target, mask):
                direct[row][target] += prob
            elif target in index:
                matrix[row][index[target]] -= prob
    active_targets = [
        target for target in range(size) if any(direct[row][target] != 0 for row in range(width))
    ]
    solved = {target: [Fraction(0) for _ in range(width)] for target in range(size)}
    if active_targets:
        columns = _solve_fraction_columns(
            matrix,
            [[direct[row][target] for row in range(width)] for target in active_targets],
        )
        for target, column in zip(active_targets, columns):
            solved[target] = column
    kernel_rows: list[dict[int, Fraction]] = [{} for _ in range(size)]
    defect = Fraction(0)
    for state in seen:
        row = index[state]
        masses: dict[int, Fraction] = {}
        total = Fraction(0)
        for target_state in active_targets:
            value = solved[target_state][row]
            if value:
                masses[target_state] = value
                total += value
        missing = Fraction(1) - total
        if missing < 0 and abs(missing) < Fraction(1, 10**12):
            missing = Fraction(0)
        if missing > defect:
            defect = missing
        if total > 0 and missing != 0:
            masses = {key: value / total for key, value in masses.items()}
        kernel_rows[state] = masses
    return kernel_rows, defect


def _epoch_flux(kernel: Kernel, pi: list[Fraction]) -> list[Fraction]:
    n_pairs, _n_triads = layout(kernel)
    mask = _pair_mask(n_pairs)
    table = _table(kernel)
    flux = [Fraction(0) for _ in range(kernel.n_states)]
    for source, mass in enumerate(pi):
        if mass == 0 or kernel.deadlock[source]:
            continue
        for target, prob in table[source].items():
            if prob and _is_pair_move(source, target, mask):
                flux[target] += mass * prob
    total = sum(flux, Fraction(0))
    if total == 0:
        return flux
    return [value / total for value in flux]


def pair_event_epoch_memory_tv(kernel: Kernel, pi: list[Fraction] | None = None) -> tuple[Fraction | None, Fraction]:
    """Max TV between P(Q'|Q) and P(Q'|Q, Q_prev), and the epoch defect.

    None means the stationary chain has no pair-toggle to continue, so the
    epoch process is undefined. Zero is a defined process with no memory.
    """
    n_pairs, _n_triads = layout(kernel)
    n_p = 1 << n_pairs
    mask = _pair_mask(n_pairs)
    if pi is None:
        pi = _stationary_exact(kernel)
    try:
        jump, defect = _epoch_kernel_exact(kernel)
    except ZeroDivisionError:
        return None, Fraction(1)
    flux = _epoch_flux(kernel, pi)
    if sum(flux, Fraction(0)) == 0:
        return None, defect
    active = [state for state, mass in enumerate(flux) if mass > 0 and jump[state]]
    if not active:
        return None, defect
    active_mass = sum((flux[state] for state in active), Fraction(0))
    pi_epoch = [Fraction(0) for _ in range(kernel.n_states)]
    for state in active:
        pi_epoch[state] = flux[state] / active_mass

    def pair_of(state: int) -> int:
        return state & mask

    joint_two = [Fraction(0) for _ in range(n_p * n_p)]
    joint_three = [Fraction(0) for _ in range(n_p * n_p * n_p)]
    marginal = [Fraction(0) for _ in range(n_p)]
    for state, mass in enumerate(pi_epoch):
        if mass == 0:
            continue
        current = pair_of(state)
        marginal[current] += mass
        for nxt, prob in jump[state].items():
            if prob == 0:
                continue
            weight = mass * prob
            follow = pair_of(nxt)
            joint_two[current * n_p + follow] += weight
            for nxt2, prob2 in jump[nxt].items():
                if prob2 == 0:
                    continue
                joint_three[(current * n_p + follow) * n_p + pair_of(nxt2)] += weight * prob2
    maximum = Fraction(0)
    defined = False
    for previous in range(n_p):
        for current in range(n_p):
            joint = sum((joint_three[(previous * n_p + current) * n_p + nxt] for nxt in range(n_p)), Fraction(0))
            current_mass = marginal[current]
            if joint == 0 or current_mass == 0:
                continue
            defined = True
            tv = Fraction(0)
            for nxt in range(n_p):
                conditional = joint_three[(previous * n_p + current) * n_p + nxt] / joint
                one_step = joint_two[current * n_p + nxt] / current_mass
                tv += abs(conditional - one_step)
            tv /= 2
            if tv > maximum:
                maximum = tv
    if not defined:
        return None, defect
    return maximum, defect


def pair_jump_dependence(kernel: Kernel) -> tuple[bool, Fraction]:
    """Whether the triadic configuration changes the next pair-toggle law.

    The law is the distribution of the next pairwise state given that the
    next event toggles a pair. The total variation is the maximum over the
    current pair state and over pairs of triadic configurations.
    """
    n_pairs, n_triads = layout(kernel)
    n_p = 1 << n_pairs
    n_t = 1 << n_triads
    laws: list[list[dict[int, Fraction] | None]] = []
    for triad in range(n_t):
        row: list[dict[int, Fraction] | None] = []
        for pair_state in range(n_p):
            state = pair_state | (triad << n_pairs)
            weights = kernel.weights[state]
            pair_weights = weights[:n_pairs]
            total = sum(pair_weights, Fraction(0))
            if kernel.deadlock[state] or total == 0:
                row.append(None)
                continue
            dist = {}
            for bit, weight in enumerate(pair_weights):
                if weight:
                    dist[pair_state ^ (1 << bit)] = weight / total
            row.append(dist)
        laws.append(row)
    maximum = Fraction(0)
    depends = False
    for pair_state in range(n_p):
        defined = [laws[triad][pair_state] for triad in range(n_t) if laws[triad][pair_state] is not None]
        for left_index, left in enumerate(defined):
            for right in defined[left_index + 1 :]:
                assert left is not None and right is not None
                distance = _tv_dicts(left, right)
                if distance > 0:
                    depends = True
                if distance > maximum:
                    maximum = distance
    return depends, maximum


def triad_rate_depends_on_pairs(kernel: Kernel) -> bool:
    """Whether, inside one triadic configuration, the pair state changes
    the probability of each triadic toggle.

    The probability uses the full event weight, so a change in pair weights
    at a fixed triadic weight is included. That is rate competition.
    """
    n_pairs, n_triads = layout(kernel)
    n_p = 1 << n_pairs
    n_t = 1 << n_triads
    for triad in range(n_t):
        signatures = []
        for pair_state in range(n_p):
            state = pair_state | (triad << n_pairs)
            if kernel.deadlock[state]:
                continue
            weights = kernel.weights[state]
            total = sum(weights, Fraction(0))
            if total == 0:
                continue
            signatures.append(tuple(weights[n_pairs + index] / total for index in range(n_triads)))
        if len(set(signatures)) > 1:
            return True
    return False


def triad_weight_depends_on_pairs(kernel: Kernel) -> bool:
    """Unnormalised triadic weights, within one triadic configuration."""
    n_pairs, n_triads = layout(kernel)
    n_p = 1 << n_pairs
    n_t = 1 << n_triads
    for triad in range(n_t):
        signatures = []
        for pair_state in range(n_p):
            state = pair_state | (triad << n_pairs)
            weights = kernel.weights[state]
            signatures.append(tuple(weights[n_pairs + index] for index in range(n_triads)))
        if len(set(signatures)) > 1:
            return True
    return False


def _cmi_from_joint(joint: dict[tuple[int, int, int], Fraction], *, hidden: int, current: int, nxt: int) -> float:
    """I(H; N | C) from a joint on (H, C, N). Zero-mass terms are skipped."""
    mass_current: dict[int, Fraction] = {}
    mass_hidden: dict[tuple[int, int], Fraction] = {}
    mass_next: dict[tuple[int, int], Fraction] = {}
    for key, mass in joint.items():
        if mass == 0:
            continue
        values = (key[0], key[1], key[2])
        cur = values[current]
        hid = values[hidden]
        following = values[nxt]
        mass_current[cur] = mass_current.get(cur, Fraction(0)) + mass
        mass_hidden[(hid, cur)] = mass_hidden.get((hid, cur), Fraction(0)) + mass
        mass_next[(cur, following)] = mass_next.get((cur, following), Fraction(0)) + mass
    bits = 0.0
    for key, mass in joint.items():
        if mass == 0:
            continue
        values = (key[0], key[1], key[2])
        cur = values[current]
        hid = values[hidden]
        following = values[nxt]
        conditional = mass_hidden[(hid, cur)] and mass / mass_hidden[(hid, cur)]
        marginal = mass_next[(cur, following)] / mass_current[cur]
        if conditional == 0 or marginal == 0:
            continue
        bits += float(mass) * math.log2(float(conditional / marginal))
    return bits


def epoch_predictive_information(kernel: Kernel, pi: list[Fraction] | None = None) -> dict:
    """Predictive information on the pair-event-epoch clock.

    ``I(T_at_epoch ; Q_next | Q)`` uses the triadic configuration of the
    state immediately after a pair toggle. It is not the full-event-clock
    conditional mutual information.
    """
    n_pairs, _n_triads = layout(kernel)
    mask = _pair_mask(n_pairs)
    if pi is None:
        pi = _stationary_exact(kernel)
    try:
        jump, defect = _epoch_kernel_exact(kernel)
    except ZeroDivisionError:
        return {
            "clock": "pair_event_epoch",
            "defined": False,
            "defect": "undefined",
            "cmi_triad_to_next_pair_bits": None,
            "cmi_pair_to_next_triad_bits": None,
            "triad_predicts_next_pair": None,
            "pair_predicts_next_triad": None,
        }
    flux = _epoch_flux(kernel, pi)
    active = [state for state, mass in enumerate(flux) if mass > 0 and jump[state]]
    if not active or sum(flux, Fraction(0)) == 0:
        return {
            "clock": "pair_event_epoch",
            "defined": False,
            "defect": f"{defect.numerator}/{defect.denominator}",
            "cmi_triad_to_next_pair_bits": None,
            "cmi_pair_to_next_triad_bits": None,
            "triad_predicts_next_pair": None,
            "pair_predicts_next_triad": None,
        }
    active_mass = sum((flux[state] for state in active), Fraction(0))
    triad_joint: dict[tuple[int, int, int], Fraction] = {}
    pair_joint: dict[tuple[int, int, int], Fraction] = {}
    for state in active:
        mass = flux[state] / active_mass
        triad = state >> n_pairs
        pair_state = state & mask
        for nxt, prob in jump[state].items():
            if prob == 0:
                continue
            weight = mass * prob
            triad_joint[(triad, pair_state, nxt & mask)] = (
                triad_joint.get((triad, pair_state, nxt & mask), Fraction(0)) + weight
            )
            pair_joint[(pair_state, triad, nxt >> n_pairs)] = (
                pair_joint.get((pair_state, triad, nxt >> n_pairs), Fraction(0)) + weight
            )
    triad_to_pair = _cmi_from_joint(triad_joint, hidden=0, current=1, nxt=2)
    pair_to_triad = _cmi_from_joint(pair_joint, hidden=0, current=1, nxt=2)
    return {
        "clock": "pair_event_epoch",
        "defined": True,
        "defect": f"{defect.numerator}/{defect.denominator}",
        "cmi_triad_to_next_pair_bits": triad_to_pair,
        "cmi_pair_to_next_triad_bits": pair_to_triad,
        "triad_predicts_next_pair": triad_to_pair > 0.0,
        "pair_predicts_next_triad": pair_to_triad > 0.0,
    }


def float_stationary(kernel: Kernel) -> tuple[np.ndarray, float, str, list[int]]:
    """Stationary distribution from state 0, with residual and periods."""
    ran = long_run(kernel, 0)
    pi = np.zeros(kernel.n_states, dtype=np.float64)
    for state, prob in ran["distribution"].items():
        pi[state] = prob
    return pi, float(ran["stationary_residual"]), str(ran["stationary_arithmetic"]), list(ran["periods"])


def _dense_transition(kernel: Kernel) -> np.ndarray:
    matrix = np.zeros((kernel.n_states, kernel.n_states), dtype=np.float64)
    for source, row in enumerate(kernel.successors):
        for target, prob in row:
            matrix[source, target] += float(prob)
    return matrix


def full_event_clock_memory_tv_float(kernel: Kernel, pi: np.ndarray, transition: np.ndarray) -> float:
    n_pairs, n_triads = layout(kernel)
    n_p = 1 << n_pairs
    n_t = 1 << n_triads
    # state = pair + n_p * triad
    shaped = pi.reshape(n_t, n_p)
    trans = transition.reshape(n_t, n_p, n_t, n_p)
    maximum = 0.0
    for previous in range(n_p):
        for current in range(n_p):
            joint = 0.0
            history = np.zeros(n_p, dtype=np.float64)
            for triad_prev in range(n_t):
                mass = shaped[triad_prev, previous]
                if mass == 0.0:
                    continue
                for triad_now in range(n_t):
                    step = trans[triad_prev, previous, triad_now, current]
                    if step == 0.0:
                        continue
                    weight = mass * step
                    joint += weight
                    history += weight * trans[triad_now, current].sum(axis=0)
            if joint == 0.0:
                continue
            current_mass = float(shaped[:, current].sum())
            if current_mass == 0.0:
                continue
            marginal = np.zeros(n_p, dtype=np.float64)
            for triad_now in range(n_t):
                mass = shaped[triad_now, current]
                if mass == 0.0:
                    continue
                marginal += mass * trans[triad_now, current].sum(axis=0)
            maximum = max(maximum, 0.5 * float(np.abs(history / joint - marginal / current_mass).sum()))
    return maximum


def memory_status_float(tv: float | None, residual: float) -> str:
    """Status of a float total variation. ``None`` is undefined, not zero."""
    if tv is None:
        return "undefined"
    if residual > FLOAT_RESIDUAL_LIMIT and tv < 10 * residual:
        return "unresolved"
    if tv > FLOAT_TV_FLOOR:
        return "positive"
    return "zero"


def _successor_float(kernel: Kernel) -> list[list[tuple[int, float]]]:
    rows = []
    for row in kernel.successors:
        rows.append([(target, float(prob)) for target, prob in row if prob])
    return rows


def epoch_kernel_float(kernel: Kernel) -> tuple[np.ndarray | None, float | None]:
    """Dense pair-event kernel. ``None`` means the linear system did not solve.

    The result is float64. It is not an exact kernel. Rows with missing mass
    are renormalised, and the returned defect is the largest missing mass
    before that renormalisation.
    """
    n_pairs, _n_triads = layout(kernel)
    mask = _pair_mask(n_pairs)
    size = kernel.n_states
    succ = _successor_float(kernel)
    pair_exit = [False] * size
    predecessors: list[list[int]] = [[] for _ in range(size)]
    for source in range(size):
        if kernel.deadlock[source]:
            continue
        for target, prob in succ[source]:
            if target == source:
                continue
            if _is_pair_move(source, target, mask):
                pair_exit[source] = True
            else:
                predecessors[target].append(source)
    seen_set = {state for state, flag in enumerate(pair_exit) if flag}
    queue = list(seen_set)
    while queue:
        target = queue.pop()
        for source in predecessors[target]:
            if source not in seen_set:
                seen_set.add(source)
                queue.append(source)
    if not seen_set:
        return np.zeros((size, size), dtype=np.float64), 1.0
    seen = sorted(seen_set)
    index = {state: row for row, state in enumerate(seen)}
    width = len(seen)
    system = np.eye(width, dtype=np.float64)
    direct = np.zeros((width, size), dtype=np.float64)
    for state in seen:
        row = index[state]
        for target, prob in succ[state]:
            if target == state:
                continue
            if _is_pair_move(state, target, mask):
                direct[row, target] += prob
            elif target in index:
                system[row, index[target]] -= prob
    try:
        absorbed = np.linalg.solve(system, direct)
    except np.linalg.LinAlgError:
        return None, None
    raw_totals = absorbed.sum(axis=1)
    missing = 1.0 - raw_totals
    missing[np.abs(missing) < 1e-10] = 0.0
    defect = float(max(0.0, float(np.max(missing)))) if width else 1.0
    # Entries below this floor are linear-algebra noise. Keeping them makes
    # later sparse walks quadratic in the state count.
    absorbed[np.abs(absorbed) < 1e-12] = 0.0
    totals = absorbed.sum(axis=1)
    landing = np.zeros((size, size), dtype=np.float64)
    positive = totals > 1e-15
    for state in seen:
        row = index[state]
        if not positive[row]:
            continue
        landing[state] = absorbed[row] / totals[row]
    return landing, defect


def _epoch_flux_float(kernel: Kernel, pi: np.ndarray) -> np.ndarray:
    n_pairs, _n_triads = layout(kernel)
    mask = _pair_mask(n_pairs)
    flux = np.zeros(kernel.n_states, dtype=np.float64)
    for source, row in enumerate(kernel.successors):
        mass = float(pi[source])
        if mass == 0.0 or kernel.deadlock[source]:
            continue
        for target, prob in row:
            if prob and _is_pair_move(source, target, mask):
                flux[target] += mass * float(prob)
    total = float(flux.sum())
    if total == 0.0:
        return flux
    return flux / total


def pair_event_epoch_memory_tv_float(
    kernel: Kernel,
    pi: np.ndarray,
    landing: np.ndarray | None = None,
    defect: float | None = None,
) -> tuple[float | None, float | None]:
    """Float pair-event-epoch total variation. ``None`` is undefined."""
    n_pairs, _n_triads = layout(kernel)
    n_p = 1 << n_pairs
    mask = _pair_mask(n_pairs)
    if landing is None:
        landing, defect = epoch_kernel_float(kernel)
    if landing is None or defect is None:
        return None, None
    flux = _epoch_flux_float(kernel, pi)
    if float(flux.sum()) == 0.0:
        return None, defect
    row_mass = landing.sum(axis=1)
    active = (flux > 0.0) & (row_mass > 0.0)
    active_mass = float(flux[active].sum())
    if active_mass == 0.0:
        return None, defect
    pi_epoch = np.zeros(kernel.n_states, dtype=np.float64)
    pi_epoch[active] = flux[active] / active_mass
    pair = np.arange(kernel.n_states) & mask
    landing_pair = np.zeros((kernel.n_states, n_p), dtype=np.float64)
    for target_pair in range(n_p):
        chosen = pair == target_pair
        if np.any(chosen):
            landing_pair[:, target_pair] = landing[:, chosen].sum(axis=1)
    incoming = np.zeros((n_p, kernel.n_states), dtype=np.float64)
    joint_two = np.zeros((n_p, n_p), dtype=np.float64)
    marginal = np.zeros(n_p, dtype=np.float64)
    joint_three = np.zeros((n_p, n_p, n_p), dtype=np.float64)
    for current in range(n_p):
        chosen = pair == current
        if not np.any(chosen):
            continue
        marginal[current] = float(pi_epoch[chosen].sum())
        incoming[current] = pi_epoch[chosen] @ landing[chosen]
        joint_two[current] = pi_epoch[chosen] @ landing_pair[chosen]
    for current in range(n_p):
        chosen = np.flatnonzero(pair == current)
        if chosen.size == 0:
            continue
        joint_three[:, current, :] = incoming[:, chosen] @ landing_pair[chosen]
    maximum = 0.0
    defined = False
    for previous in range(n_p):
        for current in range(n_p):
            joint = float(joint_three[previous, current].sum())
            current_mass = float(marginal[current])
            if joint <= 0.0 or current_mass <= 0.0:
                continue
            defined = True
            conditional = joint_three[previous, current] / joint
            one_step = joint_two[current] / current_mass
            maximum = max(maximum, 0.5 * float(np.abs(conditional - one_step).sum()))
    if not defined:
        return None, defect
    return maximum, defect


def observation_memory_tv(kernel: Kernel, pi: np.ndarray, observation: np.ndarray) -> float:
    """Max TV between P(O'|O) and P(O'|O, O_prev) on the full-event clock.

    ``observation`` maps each state to a nonnegative integer label. A
    self-loop is an ordinary event. The sum is the dense image of the
    successor walk: labels may have gaps, and an empty label is skipped.
    """
    labels = np.asarray(observation, dtype=np.int64)
    n_states = kernel.n_states
    if n_states == 0:
        return 0.0
    n_obs = int(labels.max()) + 1
    transition = _dense_transition(kernel)
    indicator = np.zeros((n_states, n_obs), dtype=np.float64)
    indicator[np.arange(n_states), labels] = 1.0
    stationary = np.asarray(pi, dtype=np.float64)
    incoming = indicator.T @ (stationary[:, None] * transition)
    next_obs = transition @ indicator
    maximum = 0.0
    for current in range(n_obs):
        chosen = np.flatnonzero(labels == current)
        if chosen.size == 0:
            continue
        margin = float(stationary[chosen].sum())
        if margin <= 0.0:
            continue
        block = incoming[:, chosen] @ next_obs[chosen]
        one = stationary[chosen] @ next_obs[chosen]
        joint = block.sum(axis=1)
        positive = joint > 0.0
        if not np.any(positive):
            continue
        conditional = block[positive] / joint[positive, None]
        distance = 0.5 * np.abs(conditional - (one / margin)).sum(axis=1)
        maximum = max(maximum, float(distance.max()))
    return maximum


def full_event_cmi_triad_to_pair(kernel: Kernel, pi: np.ndarray) -> float:
    """I(T_t ; P_{t+1} | P_t) on the full-event clock, in bits.

    T_t is the whole triadic configuration, not its population count.
    """
    n_pairs, _n_triads = layout(kernel)
    mask = _pair_mask(n_pairs)
    joint: dict[tuple[int, int, int], float] = {}
    for state, mass in enumerate(pi):
        mass = float(mass)
        if mass == 0.0:
            continue
        triad = state >> n_pairs
        pair_state = state & mask
        for nxt, prob in kernel.successors[state]:
            weight = mass * float(prob)
            if weight == 0.0:
                continue
            key = (triad, pair_state, nxt & mask)
            joint[key] = joint.get(key, 0.0) + weight
    return _cmi_from_float_joint(joint)


def _cmi_from_float_joint(joint: dict[tuple[int, int, int], float]) -> float:
    """I(H; N | C) for a joint on (H, C, N)."""
    mass_current: dict[int, float] = {}
    mass_hidden: dict[tuple[int, int], float] = {}
    mass_next: dict[tuple[int, int], float] = {}
    for (hidden, current, nxt), mass in joint.items():
        if mass == 0.0:
            continue
        mass_current[current] = mass_current.get(current, 0.0) + mass
        mass_hidden[(hidden, current)] = mass_hidden.get((hidden, current), 0.0) + mass
        mass_next[(current, nxt)] = mass_next.get((current, nxt), 0.0) + mass
    bits = 0.0
    for (hidden, current, nxt), mass in joint.items():
        if mass == 0.0:
            continue
        hidden_mass = mass_hidden[(hidden, current)]
        next_mass = mass_next[(current, nxt)]
        current_mass = mass_current[current]
        if hidden_mass <= 0.0 or next_mass <= 0.0 or current_mass <= 0.0:
            continue
        conditional = mass / hidden_mass
        marginal = next_mass / current_mass
        if conditional <= 0.0 or marginal <= 0.0:
            continue
        bits += mass * math.log2(conditional / marginal)
    return bits


def full_event_pair_memory_tv(kernel: Kernel, pi: np.ndarray) -> float:
    """Vectorised full-event-clock memory of the pairwise projection.

    This is the same statistic as ``full_event_clock_memory_tv`` when the
    stationary distribution is the float image of the rational one.
    """
    n_pairs, n_triads = layout(kernel)
    n_p = 1 << n_pairs
    n_t = 1 << n_triads
    transition = _dense_transition(kernel).reshape(n_t, n_p, n_t, n_p)
    shaped = np.asarray(pi, dtype=np.float64).reshape(n_t, n_p)
    # Axes: t source triad, c source pair, n next triad, k next pair.
    # The next triad is summed. The retained last axis is the next pair.
    one = np.einsum("tc,tcnk->ck", shaped, transition, optimize=True)
    current = shaped.sum(axis=0)
    middle = np.einsum("tp,tpuc->puc", shaped, transition, optimize=True)
    history = np.einsum("puc,ucnk->pck", middle, transition, optimize=True)
    maximum = 0.0
    for previous in range(n_p):
        for current_pair in range(n_p):
            joint = float(history[previous, current_pair].sum())
            current_mass = float(current[current_pair])
            if joint <= 0.0 or current_mass <= 0.0:
                continue
            distance = 0.5 * float(
                np.abs(history[previous, current_pair] / joint - one[current_pair] / current_mass).sum()
            )
            if distance > maximum:
                maximum = distance
    return maximum


def pair_jump_dependence_float(kernel: Kernel) -> tuple[bool, float]:
    """Float form of ``pair_jump_dependence`` for state spaces above 16.

    The boolean uses ``FLOAT_TV_FLOOR``. The distance is not an exact fraction.
    """
    n_pairs, n_triads = layout(kernel)
    n_p = 1 << n_pairs
    n_t = 1 << n_triads
    weights = np.zeros((n_t, n_p, n_pairs), dtype=np.float64)
    alive = np.zeros((n_t, n_p), dtype=bool)
    for triad in range(n_t):
        for pair_state in range(n_p):
            state = pair_state | (triad << n_pairs)
            if kernel.deadlock[state]:
                continue
            row = kernel.weights[state]
            weights[triad, pair_state] = [float(row[bit]) for bit in range(n_pairs)]
            alive[triad, pair_state] = True
    totals = weights.sum(axis=2)
    alive &= totals > 0.0
    maximum = 0.0
    for pair_state in range(n_p):
        laws = []
        for triad in range(n_t):
            if not alive[triad, pair_state]:
                continue
            law = np.zeros(n_p, dtype=np.float64)
            scale = totals[triad, pair_state]
            for bit in range(n_pairs):
                weight = weights[triad, pair_state, bit]
                if weight:
                    law[pair_state ^ (1 << bit)] = weight / scale
            laws.append(law)
        for left in range(len(laws)):
            for right in range(left + 1, len(laws)):
                distance = 0.5 * float(np.abs(laws[left] - laws[right]).sum())
                if distance > maximum:
                    maximum = distance
    return maximum > FLOAT_TV_FLOOR, maximum


def epoch_predictive_information_float(
    kernel: Kernel,
    pi: np.ndarray,
    landing: np.ndarray | None = None,
    defect: float | None = None,
) -> dict:
    """Epoch-clock information. Not a rename of the full-event quantities."""
    n_pairs, _n_triads = layout(kernel)
    mask = _pair_mask(n_pairs)
    if landing is None:
        landing, defect = epoch_kernel_float(kernel)
    if landing is None:
        return {
            "clock": "pair_event_epoch",
            "defined": False,
            "defect": None,
            "cmi_triad_to_next_pair_bits": None,
            "cmi_pair_to_next_triad_bits": None,
            "triad_predicts_next_pair": None,
            "pair_predicts_next_triad": None,
        }
    flux = _epoch_flux_float(kernel, pi)
    row_mass = landing.sum(axis=1)
    active = (flux > 0.0) & (row_mass > 0.0)
    active_mass = float(flux[active].sum())
    if active_mass == 0.0 or float(flux.sum()) == 0.0:
        return {
            "clock": "pair_event_epoch",
            "defined": False,
            "defect": defect,
            "cmi_triad_to_next_pair_bits": None,
            "cmi_pair_to_next_triad_bits": None,
            "triad_predicts_next_pair": None,
            "pair_predicts_next_triad": None,
        }
    triad_joint: dict[tuple[int, int, int], float] = {}
    pair_joint: dict[tuple[int, int, int], float] = {}
    for state in np.flatnonzero(active):
        mass = float(flux[state]) / active_mass
        triad = int(state >> n_pairs)
        pair_state = int(state & mask)
        row = landing[state]
        for nxt in np.flatnonzero(row):
            weight = mass * float(row[nxt])
            if weight == 0.0:
                continue
            triad_key = (triad, pair_state, int(nxt & mask))
            pair_key = (pair_state, triad, int(nxt >> n_pairs))
            triad_joint[triad_key] = triad_joint.get(triad_key, 0.0) + weight
            pair_joint[pair_key] = pair_joint.get(pair_key, 0.0) + weight
    triad_to_pair = _cmi_from_float_joint(triad_joint)
    pair_to_triad = _cmi_from_float_joint(pair_joint)
    return {
        "clock": "pair_event_epoch",
        "defined": True,
        "defect": defect,
        "cmi_triad_to_next_pair_bits": triad_to_pair,
        "cmi_pair_to_next_triad_bits": pair_to_triad,
        "triad_predicts_next_pair": triad_to_pair > FLOAT_TV_FLOOR,
        "pair_predicts_next_triad": pair_to_triad > FLOAT_TV_FLOOR,
    }
