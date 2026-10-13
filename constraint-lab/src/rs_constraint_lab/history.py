"""One-step pair-event history, with exact toggle and projection semantics."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction

import numpy as np

from rs_constraint_lab.exact import strongly_connected_components
from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.memory_clocks import _solve_fraction_columns
from rs_constraint_lab.state import edges

ANALYSIS_VERSION = "generation-008h-history/v1"
PRECISION = 160
DECAY_CHECKPOINTS = (0, 1, 2, 4, 8, 16, 32, 64)


class HistoryError(ValueError):
    """Invalid history state or failed exact verification."""


@dataclass(frozen=True, slots=True)
class HistoryState:
    material: int
    recent_pair: int | None


@dataclass(frozen=True)
class RecentReversal:
    multiplier: Fraction
    pair_slots: int = 6
    triad_slots: int = 4

    def __post_init__(self) -> None:
        object.__setattr__(self, "multiplier", Fraction(self.multiplier))
        if self.multiplier <= 0:
            raise HistoryError("recent-reversal multiplier must be positive")
        if type(self.pair_slots) is not int or self.pair_slots < 1:
            raise HistoryError("positive integer pair-slot count required")
        if type(self.triad_slots) is not int or self.triad_slots < 0:
            raise HistoryError("nonnegative integer hidden-slot count required")

    @property
    def width(self) -> int:
        return self.pair_slots + self.triad_slots

    def validate_history(self, history: int | None) -> None:
        if history is not None and (type(history) is not int or not 0 <= history < self.pair_slots):
            raise HistoryError("history must be a pair slot or the start sentinel")

    def validate_state(self, state: HistoryState) -> None:
        self.validate_history(state.recent_pair)
        if type(state.material) is not int or not 0 <= state.material < 1 << self.width:
            raise HistoryError("material state outside the declared relation space")

    def full_index(self, state: HistoryState) -> int:
        self.validate_state(state)
        register = 0 if state.recent_pair is None else state.recent_pair + 1
        return state.material * (self.pair_slots + 1) + register

    def state_from_index(self, index: int) -> HistoryState:
        if type(index) is not int or not 0 <= index < (1 << self.width) * (self.pair_slots + 1):
            raise HistoryError("augmented state index out of range")
        material, register = divmod(index, self.pair_slots + 1)
        return HistoryState(material, None if register == 0 else register - 1)

    def advance(self, state: HistoryState, event: int) -> HistoryState:
        self.validate_state(state)
        if type(event) is not int or not 0 <= event < self.width:
            raise HistoryError("event slot out of range")
        history = event if event < self.pair_slots else state.recent_pair
        return HistoryState(state.material ^ (1 << event), history)

    def weights(self, history: int | None) -> tuple[Fraction, ...]:
        self.validate_history(history)
        return tuple(self.multiplier if slot == history else Fraction(1) for slot in range(self.width))

    def full_probabilities(self, history: int | None) -> tuple[Fraction, ...]:
        weights = self.weights(history)
        total = sum(weights)
        return tuple(weight / total for weight in weights)

    def full_row(self, state: HistoryState) -> dict[HistoryState, Fraction]:
        self.validate_state(state)
        return {self.advance(state, event): probability for event, probability in enumerate(self.full_probabilities(state.recent_pair))}

    def pair_probabilities(self, history: int | None) -> tuple[Fraction, ...]:
        full = self.full_probabilities(history)
        pair_mass = sum(full[:self.pair_slots])
        return tuple(probability / pair_mass for probability in full[:self.pair_slots])

    def epoch_index(self, pair_mask: int, history: int) -> int:
        self.validate_history(history)
        if history is None or type(pair_mask) is not int or not 0 <= pair_mask < 1 << self.pair_slots:
            raise HistoryError("recurrent pair state requires a mask and remembered slot")
        return pair_mask * self.pair_slots + history

    def epoch_state(self, index: int) -> tuple[int, int]:
        if type(index) is not int or not 0 <= index < (1 << self.pair_slots) * self.pair_slots:
            raise HistoryError("pair-epoch index out of range")
        return divmod(index, self.pair_slots)

    def epoch_row(self, pair_mask: int, history: int | None) -> dict[int, Fraction]:
        if type(pair_mask) is not int or not 0 <= pair_mask < 1 << self.pair_slots:
            raise HistoryError("pair mask out of range")
        return {
            self.epoch_index(pair_mask ^ (1 << event), event): probability
            for event, probability in enumerate(self.pair_probabilities(history))
        }

    def epoch_kernel(self) -> list[dict[int, Fraction]]:
        return [self.epoch_row(*self.epoch_state(index)) for index in range((1 << self.pair_slots) * self.pair_slots)]

    def direct_next_pair_slots(self, pair_mask: int, history: int | None) -> list[list[Fraction]]:
        """Resolve hidden-only excursions from full rows, for every raw hidden mask."""
        if type(pair_mask) is not int or not 0 <= pair_mask < 1 << self.pair_slots:
            raise HistoryError("pair mask out of range")
        size = 1 << self.triad_slots
        matrix = [[Fraction(i == j) for j in range(size)] for i in range(size)]
        direct = [[Fraction(0) for _ in range(size)] for _ in range(self.pair_slots)]
        for hidden in range(size):
            state = HistoryState(pair_mask | (hidden << self.pair_slots), history)
            for target, probability in self.full_row(state).items():
                difference = state.material ^ target.material
                event = difference.bit_length() - 1
                if event < self.pair_slots:
                    direct[event][hidden] += probability
                else:
                    matrix[hidden][target.material >> self.pair_slots] -= probability
        columns = _solve_fraction_columns(matrix, direct)
        return [[columns[event][hidden] for event in range(self.pair_slots)] for hidden in range(size)]


def _decimal(value: Fraction) -> Decimal:
    return Decimal(value.numerator) / Decimal(value.denominator)


def js(left, right) -> Decimal:
    left, right = tuple(left), tuple(right)
    if len(left) != len(right) or sum(left) != 1 or sum(right) != 1 or any(v < 0 for v in left + right):
        raise HistoryError("JS requires equal-length normalised nonnegative rational rows")
    with localcontext() as context:
        context.prec = PRECISION
        result = Decimal(0)
        for p, q in zip(left, right):
            average = (p + q) / 2
            for value in (p, q):
                if value:
                    result += _decimal(value) * _decimal(value / average).ln() / 2
        return +result


def mutual_information(joint) -> Decimal:
    size = len(joint)
    width = len(joint[0])
    if any(len(row) != width for row in joint) or sum(map(sum, joint)) != 1:
        raise HistoryError("joint information table must be normalised")
    if any(value < 0 for row in joint for value in row):
        raise HistoryError("negative joint information entry")
    marg_left = [sum(row) for row in joint]
    marg_right = [sum(joint[i][j] for i in range(size)) for j in range(width)]
    with localcontext() as context:
        context.prec = PRECISION
        result = Decimal(0)
        for i, row in enumerate(joint):
            for j, value in enumerate(row):
                if value:
                    result += _decimal(value) * _decimal(value / (marg_left[i] * marg_right[j])).ln()
        return +result


def analytic_row_js(multiplier: Fraction, denominator: Fraction) -> Decimal:
    with localcontext() as context:
        context.prec = PRECISION
        m = multiplier
        return +(_decimal(m) * _decimal(2 * m / (m + 1)).ln() + _decimal(2 / (m + 1)).ln()) / _decimal(denominator)


def analytic_shape_js(multiplier: Fraction) -> Decimal:
    with localcontext() as context:
        context.prec = PRECISION
        m = multiplier
        numerator = (
            2 * _decimal(Fraction(4) / (m + 3)).ln()
            + _decimal(m + 1) * _decimal(2 * (m + 1) / (m + 3)).ln()
            + _decimal(m) * _decimal(2 * m / (m + 1)).ln()
            + _decimal(2 / (m + 1)).ln()
        )
        return +numerator / _decimal(2 * (m + 5))


def entropy_information(diagonal: Fraction, off_diagonal: Fraction, slots: int) -> Decimal:
    with localcontext() as context:
        context.prec = PRECISION
        # Express ln(slots)+sum(q ln q) as KL to avoid neutral cancellation.
        result = Decimal(0)
        for value, count in ((diagonal, 1), (off_diagonal, slots - 1)):
            if value:
                result += count * _decimal(value) * _decimal(slots * value).ln()
        return +result


def _shape_name(mask: int) -> str:
    table = pair_classes()
    canonical = table.class_of[mask]
    descriptor = table.by_mask[canonical]
    if canonical == table.path_mask:
        return "two_edge_path"
    if canonical == table.matching_mask:
        return "two_edge_matching"
    if descriptor["edge_count"] == 4 and descriptor["triangle_count"] == 1:
        return "triangle_pendant"
    if descriptor["edge_count"] == 4 and tuple(descriptor["degree_multiset"]) == (2, 2, 2, 2):
        return "four_cycle"
    return descriptor["name"]


def witness_specification() -> dict:
    pair_slots = edges(4)
    initial = 1 << pair_slots.index((0, 1))
    middle = pair_slots.index((1, 2))
    end = pair_slots.index((2, 3))
    endpoint = initial | (1 << middle) | (1 << end)
    classifier = pair_classes()
    toggles = []
    for event, pair in enumerate(pair_slots):
        target = endpoint ^ (1 << event)
        toggles.append({
            "slot": event, "pair": list(pair), "direction": "dissolve" if endpoint & (1 << event) else "form",
            "target_pair_mask": target, "graph_class": classifier.class_of[target], "shape": _shape_name(target),
        })
    return {
        "start_state": initial, "start_history": None, "endpoint_state": endpoint, "endpoint_triad_mask": 0,
        "middle_slot": middle, "end_slot": end,
        "history_M_events": [end, middle], "history_E_events": [middle, end],
        "canonical_path_class": classifier.class_of[endpoint], "toggles": toggles,
    }


def analyse_witness(multiplier: Fraction) -> dict:
    model = RecentReversal(multiplier)
    spec = witness_specification()
    start = HistoryState(spec["start_state"], None)
    paths = []
    for name in ("M", "E"):
        state, probability = start, Fraction(1)
        states = [model.full_index(state)]
        for event in spec[f"history_{name}_events"]:
            if state.material & (1 << event):
                raise HistoryError("the prescribed witness event must be formation")
            target = model.advance(state, event)
            probability *= model.full_row(state)[target]
            state = target
            states.append(model.full_index(state))
        paths.append({"name": name, "state": state, "probability": probability, "augmented_indices": states})
    if paths[0]["state"].material != paths[1]["state"].material or paths[0]["probability"] != paths[1]["probability"]:
        raise HistoryError("common-start witness lost endpoint or equal-probability control")
    material = paths[0]["state"].material
    full = [model.full_probabilities(path["state"].recent_pair) for path in paths]
    pair = [model.pair_probabilities(path["state"].recent_pair) for path in paths]
    classes, counts, shapes, masks = [], [], [], []
    table = pair_classes()
    for row in pair:
        class_row = {representative: Fraction(0) for representative in table.representatives}
        count_row = [Fraction(0) for _ in range(7)]
        shape_row = defaultdict(Fraction)
        mask_row = [Fraction(0) for _ in range(64)]
        for event, probability in enumerate(row):
            target = material ^ (1 << event)
            class_row[table.class_of[target]] += probability
            count_row[target.bit_count()] += probability
            shape_row[_shape_name(target)] += probability
            mask_row[target] += probability
        classes.append(class_row)
        counts.append(count_row)
        shapes.append(dict(shape_row))
        masks.append(mask_row)
    full_js, pair_js = js(*full), js(*pair)
    graph_js = js(classes[0].values(), classes[1].values())
    edge_js = js(*counts)
    with localcontext() as context:
        context.prec = PRECISION
        gaps = [
            abs(full_js - analytic_row_js(multiplier, multiplier + 9)),
            abs(pair_js - analytic_row_js(multiplier, multiplier + 5)),
            abs(graph_js - analytic_shape_js(multiplier)),
        ]
        label_remainder = pair_js - graph_js
    return {
        "m": multiplier, **spec,
        "history_A_events": spec["history_M_events"], "history_B_events": spec["history_E_events"],
        "endpoint_history_A": paths[0]["state"].recent_pair, "endpoint_history_B": paths[1]["state"].recent_pair,
        "endpoint_material_bytes_A": material.to_bytes(2, "little").hex(),
        "endpoint_material_bytes_B": paths[1]["state"].material.to_bytes(2, "little").hex(),
        "fixed_ordinary_constraints": [], "baseline_weights": [Fraction(1)] * 10, "event_support": list(range(10)),
        "path_probability_A": paths[0]["probability"], "path_probability_B": paths[1]["probability"],
        "path_probability_formula": Fraction(1) / (10 * (multiplier + 9)),
        "augmented_path_A": paths[0]["augmented_indices"], "augmented_path_B": paths[1]["augmented_indices"],
        "full_rows": full, "pair_rows": pair, "edge_count_distributions": counts,
        "graph_class_distributions": classes, "shape_distributions": shapes, "pair_mask_distributions": masks,
        "full_row_JS": str(full_js), "pair_row_JS": str(pair_js), "edge_count_JS": str(edge_js),
        "graph_class_JS": str(graph_js), "shape_given_edgecount_JS": str(graph_js),
        "label_given_class_JS": str(label_remainder),
        "full_row_max_difference": max(abs(a - b) for a, b in zip(*full)),
        "pair_row_max_difference": max(abs(a - b) for a, b in zip(*pair)),
        "edge_count_exact_equality": counts[0] == counts[1],
        "analytic_numeric_gap": str(max(gaps)), "same_program": True, "same_complete_material_state": True,
        "equal_event_multiset": sorted(spec["history_M_events"]) == sorted(spec["history_E_events"]),
    }


def analyse_kernel(model: RecentReversal, quotient_masks=None) -> dict:
    rows = model.epoch_kernel()
    count = len(rows)
    stationary = [Fraction(1, count)] * count
    incoming = [Fraction(0)] * count
    for source, row in enumerate(rows):
        for target, probability in row.items():
            incoming[target] += stationary[source] * probability
    pair_marginal = [sum(stationary[p * model.pair_slots:(p + 1) * model.pair_slots]) for p in range(1 << model.pair_slots)]
    history_marginal = [sum(stationary[model.epoch_index(p, h)] for p in range(1 << model.pair_slots)) for h in range(model.pair_slots)]
    independent_gap = max(abs(stationary[index] - pair_marginal[p] * history_marginal[h]) for index, (p, h) in enumerate(map(model.epoch_state, range(count))))
    components = strongly_connected_components([tuple(row.items()) for row in rows])
    if len(components) != 1:
        raise HistoryError("stationary comparison requires one communicating class")
    parity_ok = all(p.bit_count() % 2 != model.epoch_state(target)[0].bit_count() % 2 for source, row in enumerate(rows) for p in [model.epoch_state(source)[0]] for target in row)
    return_two = all(any(rows[target].get(source, 0) > 0 for target in row) for source, row in enumerate(rows))
    material_rows = []
    lumpability_gap = Fraction(0)
    for p in range(1 << model.pair_slots):
        material_rows.append({
            p ^ (1 << event): sum(model.pair_probabilities(h)[event] * stationary[model.epoch_index(p, h)] / pair_marginal[p] for h in range(model.pair_slots))
            for event in range(model.pair_slots)
        })
        reference = {model.epoch_state(target)[0]: probability for target, probability in rows[model.epoch_index(p, 0)].items()}
        for h in range(1, model.pair_slots):
            projected = {model.epoch_state(target)[0]: probability for target, probability in rows[model.epoch_index(p, h)].items()}
            lumpability_gap = max(lumpability_gap, max(abs(projected[t] - reference[t]) for t in reference))
    quotient_checks, quotient_gap = [], Fraction(0)
    for mask in (quotient_masks if quotient_masks is not None else (0,)):
        for h in (None, *range(model.pair_slots)):
            direct = model.direct_next_pair_slots(mask, h)
            closed = model.pair_probabilities(h)
            gap = max(abs(value - closed[event]) for row in direct for event, value in enumerate(row))
            quotient_gap = max(quotient_gap, gap)
            quotient_checks.append({"pair_mask": mask, "history": h, "raw_hidden_rows": len(direct), "gap": gap})
    return {
        "m": model.multiplier, "state_count": count, "pair_slots": model.pair_slots,
        "stationary_distribution": stationary, "stationary_residual": max(abs(a - b) for a, b in zip(incoming, stationary)),
        "uniform_joint_gap": max(abs(value - Fraction(1, count)) for value in stationary),
        "pair_marginal": pair_marginal, "history_marginal": history_marginal,
        "pair_marginal_gap": max(abs(value - Fraction(1, 1 << model.pair_slots)) for value in pair_marginal),
        "history_pair_independence_gap": independent_gap, "communicating_class_count": len(components),
        "period": 2 if parity_ok and return_two else None, "parity_flip_verified": parity_ok, "two_step_return_verified": return_two,
        "row_sum_gap": max(abs(sum(row.values()) - 1) for row in rows),
        "strong_lumpability": lumpability_gap == 0, "lumpability_gap": lumpability_gap,
        "stationary_one_step_gap_vs_H0": max(abs(v - Fraction(1, model.pair_slots)) for row in material_rows for v in row.values()),
        "stationary_projected_pair_rows": material_rows,
        "full_vs_pair_quotient_gap": quotient_gap, "quotient_checks": quotient_checks,
        "transitions": [list(row.items()) for row in rows],
    }


def _matrix_product(left, right):
    size = len(left)
    return [[sum((left[i][k] * right[k][j] for k in range(size)), Fraction(0)) for j in range(size)] for i in range(size)]


def analyse_temporal(model: RecentReversal) -> dict:
    slots = model.pair_slots
    if slots < 2:
        raise HistoryError("the temporal comparison requires at least two pair slots")
    q = [list(model.pair_probabilities(h)) for h in range(slots)]
    uniform = [Fraction(1, slots)] * slots
    lam = (model.multiplier - 1) / (model.multiplier + slots - 1)
    constant_gap = max(abs(sum(row) - 1) for row in q)
    stationary_gap = max(abs(sum(uniform[i] * q[i][j] for i in range(slots)) - uniform[j]) for j in range(slots))
    symmetry_gap = max(abs(q[i][j] - q[j][i]) for i in range(slots) for j in range(slots))
    eigen_gap = Fraction(0)
    for basis in range(slots - 1):
        vector = [Fraction(i == basis) - Fraction(i == slots - 1) for i in range(slots)]
        eigen_gap = max(eigen_gap, max(abs(sum(q[i][j] * vector[j] for j in range(slots)) - lam * vector[i]) for i in range(slots)))
    float_eigenvalues = np.linalg.eigvalsh(np.array(q, dtype=float))
    expected_eigenvalues = sorted([float(lam)] * (slots - 1) + [1.0])
    float_eigen_gap = float(np.max(np.abs(float_eigenvalues - expected_eigenvalues)))
    joint = [[value / slots for value in row] for row in q]
    information = mutual_information(joint)
    analytic_information = entropy_information(q[0][0], q[0][1], slots)
    power = [[Fraction(i == j) for j in range(slots)] for i in range(slots)]
    decay, power_gap = [], Fraction(0)
    for checkpoint in range(max(DECAY_CHECKPOINTS) + 1):
        if checkpoint in DECAY_CHECKPOINTS:
            predicted = [[Fraction(1, slots) + lam ** checkpoint * (Fraction(i == j) - Fraction(1, slots)) for j in range(slots)] for i in range(slots)]
            power_gap = max(power_gap, max(abs(power[i][j] - predicted[i][j]) for i in range(slots) for j in range(slots)))
            decay.append({
                "checkpoint": checkpoint, "transition_matrix": [row[:] for row in power],
                "TV_to_uniform": sum(abs(v - Fraction(1, slots)) for v in power[0]) / 2,
                "TV_formula": Fraction(slots - 1, slots) * abs(lam) ** checkpoint,
                "initial_history_MI": str(mutual_information([[v / slots for v in row] for row in power])),
            })
        if checkpoint < max(DECAY_CHECKPOINTS):
            power = _matrix_product(power, q)
    rows = model.epoch_kernel()
    size = len(rows)
    pi = Fraction(1, size)
    backtrack = Fraction(0)
    for source, row in enumerate(rows):
        initial_pair = model.epoch_state(source)[0]
        for middle, probability in row.items():
            for target, second in rows[middle].items():
                if model.epoch_state(target)[0] == initial_pair:
                    backtrack += pi * probability * second
    order2_gap = Fraction(0)
    triple_count = 0
    # Enumerate all consistent triples from actual augmented transitions.
    for current in range(1 << slots):
        for last in range(slots):
            middle_pair = current ^ (1 << last)
            target = model.epoch_index(current, last)
            expected = {model.epoch_state(nxt)[0]: value for nxt, value in rows[target].items()}
            for earlier in range(slots):
                first_pair = middle_pair ^ (1 << earlier)
                middle = model.epoch_index(middle_pair, earlier)
                mass = Fraction(0)
                numerators = defaultdict(Fraction)
                for initial_history in range(slots):
                    source = model.epoch_index(first_pair, initial_history)
                    weight = pi * rows[source].get(middle, 0) * rows[middle].get(target, 0)
                    mass += weight
                    for nxt, probability in rows[target].items():
                        numerators[model.epoch_state(nxt)[0]] += weight * probability
                if mass <= 0:
                    raise HistoryError("conditioned material triple must be legal")
                order2_gap = max(order2_gap, max(abs(numerators[nxt] / mass - probability) for nxt, probability in expected.items()))
                triple_count += 1
    order1_gap = max(abs(a - b) for a, b in zip(q[0], q[1]))
    with localcontext() as context:
        context.prec = PRECISION
        information_gap = abs(information - analytic_information)
    return {
        "m": model.multiplier, "transition_matrix": q, "stationary_history": uniform,
        "repeat_probability": q[0][0], "nontrivial_eigenvalue": lam, "multiplicity": slots - 1,
        "float_eigenvalues": float_eigenvalues.tolist(), "exact_eigen_gap": eigen_gap,
        "eigenvalue_gap": float_eigen_gap, "history_row_sum_gap": constant_gap,
        "history_stationary_residual": stationary_gap, "history_symmetry_gap": symmetry_gap,
        "consecutive_event_MI": str(information), "analytic_consecutive_event_MI": str(analytic_information),
        "information_formula_gap": str(information_gap), "initial_history_decay": decay, "matrix_power_gap": power_gap,
        "two_step_backtrack_probability": backtrack, "H0_backtrack_probability": Fraction(1, slots),
        "backtrack_repeat_gap": abs(backtrack - q[0][0]),
        "order1_witness_gap": order1_gap, "order2_sufficiency_gap": order2_gap,
        "consistent_triples_checked": triple_count, "projected_markov_order": 1 if order1_gap == 0 else 2,
        "order1_example": {"current_pair_mask": 0, "previous_mask_A": 1, "previous_mask_B": 2, "future_slot_rows": [q[0], q[1]]},
    }
