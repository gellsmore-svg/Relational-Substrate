"""Generation 8B information calibration.

Three layers stay separate.

Layer A is the Generation 8A plug-in estimate from a finite contingency table.
Layer B compares that plug-in with a deterministic permutation of its labels.
Layer C is a deterministic kernel result from the known transition law.

A float64 kernel result is not a rational identity. Structural controls whose
pair-event law does not read the triad are calibration instruments supplied
by the transition semantics. A permutation percentile is not a scientific verdict.

Negative ``observed - null mean`` values are stored. They are not replaced by zero.
"""

from __future__ import annotations

import math
from collections import Counter

import numpy as np

from rs_constraint_lab.constraints import Choreography, parse_expression
from rs_constraint_lab.durable import canonical_json, sha256_bytes
from rs_constraint_lab.explore08 import (
    CLASS_NAMES,
    CLASS_OF_MASK,
    PAIR_SLOTS,
    _mutual_information,
    _seed_from_identity,
    source_masks,
)
from rs_constraint_lab.explore08a import (
    PALETTE,
    class_edge_counts,
    conditional_mutual_information,
    load_repair_palette,
    mutual_information,
    rule_aware_partition,
)
from rs_constraint_lab.kernel import Kernel, build_kernel, kernel_fingerprint
from rs_constraint_lab.memory_clocks import epoch_kernel_block, epoch_kernel_float, float_stationary, layout
from rs_constraint_lab.state import relation_slots
from rs_constraint_lab.weights import alphabet_factors

EXPERIMENT_ID = "generation-008b-information-calibration"
ANALYSIS_VERSION = "generation-008b-information/v1"
ROUND_ID = "round-b0"
ZERO_SYSTEMS = ("R00", "R03", "R07")
TRIAD_CONDITIONED_SYSTEMS = ("R01", "R02", "R04", "R05", "R06")
CHECKPOINTS = (1, 2, 4, 8, 16, 32, 64, 128, 256, 512)
OCCUPANCY_HORIZON = 512
INITIAL_PERMUTATIONS = 10_000
CURRENT_PERMUTATIONS = 2_000
# Floors are numerical thresholds for float64 kernel results.
# They were chosen from solver scale, before the B0 tables were interpreted.
ZERO_INFORMATION_FLOOR = 1e-10
KERNEL_ROW_TOLERANCE = 1e-9
STATIONARY_RESIDUAL_TOLERANCE = 1e-8
HITTING_RESIDUAL_TOLERANCE = 1e-8
CROSS_SOLVER_TOLERANCE = 1e-8
PLUGIN_REPRODUCTION_TOLERANCE = 1e-9
CHAIN_RULE_TOLERANCE = 1e-9
UNABSORBED_HORIZON_TOLERANCE = 1e-8
N_PAIR_STATES = 64
N_TRIAD_STATES = 16
N_FULL_STATES = 1024
PAIR_SLOT_COUNT = 6
SEED_FUNCTION = "sha256-u64-v1"


class CalibrationError(RuntimeError):
    """A structural identity or a reproduction check missed its frozen tolerance."""


def permutation_seed(estimand_id: str, system_id: str, source_graph: str, index: int) -> int:
    return _seed_from_identity(
        {
            "estimand_id": estimand_id,
            "experiment_id": EXPERIMENT_ID,
            "permutation_index": int(index),
            "source_graph_class": source_graph,
            "system_id": system_id,
        }
    )


def leading_order_bias(n_contexts: int, n_outcomes: int, n_samples: int) -> float:
    """Miller-Madow scale ``((dx-1)(dy-1))/(2N)``. A sanity check, not a correction."""
    return ((n_contexts - 1) * (n_outcomes - 1)) / (2.0 * n_samples)


def system_kernel(expressions: list[str]) -> Kernel:
    rules = tuple(parse_expression(expression, 4, order=3) for expression in expressions)
    factors = alphabet_factors("W4")
    choreography = Choreography(0, 0, rules)
    slots = tuple(relation_slots(4, 3))
    return build_kernel(4, choreography, factors, relation_slots=slots)


def kernel_metadata(kernel: Kernel, expressions: list[str]) -> dict:
    fingerprint = kernel_fingerprint(kernel)
    return {
        "analysis_version": ANALYSIS_VERSION,
        "deadlock_states": int(sum(kernel.deadlock)),
        "expressions": list(expressions),
        "fingerprint_sha256": sha256_bytes(fingerprint.encode("utf-8")),
        "n_states": kernel.n_states,
        "relation_slot_count": len(kernel.relation_slots),
    }


def structural_triad_independence(expressions: list[str]) -> dict:
    """Why a pair-event law does or does not read the triad.

    ``Constraint.matches`` reads the action bit, each condition bit, and,
    when a count literal is present, ``state.bit_count()``. Count literals
    count every set bit, including triad bits. The A0 palette has none.

    If every rule has an empty count list and neither its action nor its
    conditions occupy a triad slot, then for a fixed pair mask the weight
    of every slot is the same at all 16 triads. Triad-only steps keep the
    pair mask fixed, so they do not change that weight vector. The pair
    slot that ends the excursion, and therefore the next pair mask, is
    independent of the current triad. The pair-mask trajectory is then
    independent of the initial triad, and so is every functional of it.
    """
    rules = [parse_expression(expression, 4, order=3) for expression in expressions]
    reasons = []
    reads_triad = False
    for rule in rules:
        if rule.counts:
            reads_triad = True
            reasons.append("count literal reads the full-state popcount")
        if rule.action >= PAIR_SLOTS:
            reads_triad = True
            reasons.append(f"action slot {rule.action} is a triad slot")
        for slot, _required in rule.conditions:
            if slot >= PAIR_SLOTS:
                reads_triad = True
                reasons.append(f"condition slot {slot} is a triad slot")
    return {
        "pair_event_law_reads_triad": reads_triad,
        "reasons": reasons,
        "rule_count": len(rules),
        "structural_zero_control": not reads_triad,
    }


def weight_rows(kernel: Kernel) -> np.ndarray:
    rows = np.zeros((kernel.n_states, kernel.n_edges), dtype=np.float64)
    for state, weights in enumerate(kernel.weights):
        for slot, weight in enumerate(weights):
            rows[state, slot] = float(weight)
    return rows


def pair_slot_laws(kernel: Kernel) -> dict[str, np.ndarray]:
    """Local pair-slot laws at every full state.

    ``conditional`` renormalises the six pair propensities. That is
    ``P(E=e | s, the next full event is a pair event)``.
    ``full_event`` is ``P(the next full event is pair slot e | s)``,
    without conditioning on the event being a pair event.
    """
    weights = weight_rows(kernel)
    pair = weights[:, :PAIR_SLOT_COUNT]
    pair_total = pair.sum(axis=1)
    full_total = weights.sum(axis=1)
    if np.any(pair_total <= 0.0) or np.any(full_total <= 0.0):
        raise CalibrationError("a state has no positive pair-event weight")
    conditional = pair / pair_total[:, None]
    full_event = pair / full_total[:, None]
    return {"conditional": conditional, "full_event": full_event}


def triad_weight_span(kernel: Kernel) -> float:
    """Largest per-slot gap, over pair masks, between the 16 triads."""
    weights = weight_rows(kernel)[:, :PAIR_SLOT_COUNT]
    span = 0.0
    triads = np.arange(N_TRIAD_STATES)
    for mask in range(N_PAIR_STATES):
        block = weights[(triads << PAIR_SLOTS) | mask]
        span = max(span, float(np.max(np.max(block, axis=0) - np.min(block, axis=0))))
    return span


def _state_class() -> np.ndarray:
    pair_class = np.asarray(CLASS_OF_MASK, dtype=np.int32)
    return pair_class[np.arange(N_FULL_STATES) & (N_PAIR_STATES - 1)]


def epoch_landing(kernel: Kernel, *, solver: str = "block") -> tuple[np.ndarray, float]:
    if solver == "block":
        landing, defect = epoch_kernel_block(kernel)
    elif solver == "dense":
        landing, defect = epoch_kernel_float(kernel)
    else:
        raise ValueError(f"unknown epoch solver {solver}")
    if landing is None or defect is None:
        raise CalibrationError(f"{solver} pair-event kernel did not solve")
    if landing.shape != (N_FULL_STATES, N_FULL_STATES):
        raise CalibrationError(f"epoch kernel shape drifted: {landing.shape}")
    return landing, float(defect)


def kernel_row_error(landing: np.ndarray) -> float:
    return float(np.max(np.abs(landing.sum(axis=1) - 1.0)))


def pair_mask_law_span(landing: np.ndarray) -> float:
    """Largest L1 gap, across triads of one pair mask, of the next pair-mask law.

    Structural zero controls have a gap at numerical noise. A triad-conditioned
    rule can have a positive gap, and that gap is not itself an information value.
    """
    span = 0.0
    for mask in range(N_PAIR_STATES):
        rows = np.empty((N_TRIAD_STATES, N_PAIR_STATES), dtype=np.float64)
        for triad in range(N_TRIAD_STATES):
            state = mask | (triad << PAIR_SLOTS)
            rows[triad] = landing[state].reshape(N_TRIAD_STATES, N_PAIR_STATES).sum(axis=0)
        span = max(span, float(np.max(np.abs(rows - rows[:1]).sum(axis=1))))
    return span


def information_from_conditionals(conditional: np.ndarray) -> float:
    """``I(X;Y)`` in nats. Rows are contexts. The prior over rows is uniform."""
    conditional = np.asarray(conditional, dtype=np.float64)
    if conditional.ndim != 2 or conditional.shape[0] < 2:
        raise ValueError("conditional information needs at least two contexts")
    row_sums = conditional.sum(axis=1)
    if np.any(row_sums <= 0.0):
        raise CalibrationError("a context distribution has no mass")
    probabilities = conditional / row_sums[:, None]
    prior = 1.0 / probabilities.shape[0]
    marginal = probabilities.mean(axis=0)
    information = 0.0
    for context in range(probabilities.shape[0]):
        for outcome, probability in enumerate(probabilities[context]):
            joint = prior * probability
            if joint <= 0.0 or marginal[outcome] <= 0.0:
                continue
            information += joint * math.log(joint / (prior * marginal[outcome]))
    return float(information)


def _edge_distribution(class_conditional: np.ndarray, edges: list[int]) -> np.ndarray:
    out = np.zeros((class_conditional.shape[0], 7), dtype=np.float64)
    for class_index, edge_count in enumerate(edges):
        out[:, edge_count] += class_conditional[:, class_index]
    return out


def class_given_edge_information(class_conditional: np.ndarray, edges: list[int] | None = None) -> float:
    """``I(T; C | E)`` when ``E`` is the edge count of class ``C``."""
    edges = class_edge_counts() if edges is None else edges
    conditional = np.asarray(class_conditional, dtype=np.float64)
    conditional = conditional / conditional.sum(axis=1, keepdims=True)
    prior = 1.0 / conditional.shape[0]
    information = 0.0
    for edge_count in range(7):
        members = [index for index, edge in enumerate(edges) if edge == edge_count]
        if not members:
            continue
        mass_te = conditional[:, members].sum(axis=1)
        mass_e = float(mass_te.mean())
        if mass_e <= 0.0:
            continue
        class_given_edge = conditional[:, members].mean(axis=0) / mass_e
        for context in range(conditional.shape[0]):
            if mass_te[context] <= 0.0:
                continue
            given_context = conditional[context, members] / mass_te[context]
            for outcome, probability in enumerate(given_context):
                joint = prior * mass_te[context] * probability
                if joint <= 0.0 or class_given_edge[outcome] <= 0.0:
                    continue
                information += joint * math.log(probability / class_given_edge[outcome])
    return float(information)


def decompose_class_information(class_conditional: np.ndarray) -> dict:
    edges = class_edge_counts()
    class_information = information_from_conditionals(class_conditional)
    edge_information = information_from_conditionals(_edge_distribution(class_conditional, edges))
    shape_information = class_given_edge_information(class_conditional, edges)
    return {
        "class_given_edge_count": shape_information,
        "class_information": class_information,
        "edge_count_information": edge_information,
        "chain_rule_gap": class_information - edge_information - shape_information,
    }


def mask_class_decomposition(mask_conditional: np.ndarray) -> dict:
    """``I(T; mask) = I(T; class) + I(T; mask | class)``."""
    pair_class = np.asarray(CLASS_OF_MASK, dtype=np.int32)
    mask_conditional = np.asarray(mask_conditional, dtype=np.float64)
    mask_conditional = mask_conditional / mask_conditional.sum(axis=1, keepdims=True)
    class_conditional = np.zeros((mask_conditional.shape[0], 11), dtype=np.float64)
    for mask, class_index in enumerate(pair_class):
        class_conditional[:, class_index] += mask_conditional[:, mask]
    mask_information = information_from_conditionals(mask_conditional)
    class_information = information_from_conditionals(class_conditional)
    prior = 1.0 / mask_conditional.shape[0]
    residual = 0.0
    for class_index in range(11):
        members = np.flatnonzero(pair_class == class_index)
        mass_tc = mask_conditional[:, members].sum(axis=1)
        mass_c = float(mass_tc.mean())
        if mass_c <= 0.0:
            continue
        within = mask_conditional[:, members].mean(axis=0) / mass_c
        for context in range(mask_conditional.shape[0]):
            if mass_tc[context] <= 0.0:
                continue
            given = mask_conditional[context, members] / mass_tc[context]
            for outcome, probability in enumerate(given):
                joint = prior * mass_tc[context] * probability
                if joint <= 0.0 or within[outcome] <= 0.0:
                    continue
                residual += joint * math.log(probability / within[outcome])
    return {
        "chain_rule_gap": mask_information - class_information - residual,
        "class_information": class_information,
        "mask_given_class": float(residual),
        "mask_information": mask_information,
    }


def first_destination_laws(landing: np.ndarray, source_class: int) -> dict:
    """Eventual hitting law of the other two 3-edge classes.

    Destination states are absorbing only in this calculation. The epoch
    kernel itself is left unchanged. The source class is transient, so the
    start is not scored as a hit.
    """
    state_class = _state_class()
    three = sorted({int(index) for index, name in enumerate(CLASS_NAMES) if name.startswith("e3-")})
    if source_class not in three or len(three) != 3:
        raise CalibrationError("3-edge class index drifted")
    destinations = [index for index in three if index != source_class]
    absorbing = np.isin(state_class, destinations)
    transient = np.flatnonzero(~absorbing)
    factor = np.eye(transient.size, dtype=np.float64) - landing[np.ix_(transient, transient)]
    absorbed = []
    for class_index in destinations:
        members = np.flatnonzero(state_class == class_index)
        absorbed.append(landing[transient][:, members].sum(axis=1))
    rhs = np.column_stack(absorbed)
    try:
        solved = np.linalg.solve(factor, rhs)
    except np.linalg.LinAlgError as exc:
        raise CalibrationError("first-destination linear system did not solve") from exc
    residual = float(np.max(np.abs(factor @ solved - rhs)))
    totals = solved.sum(axis=1)
    height = np.zeros((N_FULL_STATES, 2), dtype=np.float64)
    for column, class_index in enumerate(destinations):
        members = np.flatnonzero(state_class == class_index)
        height[members, column] = 1.0
    height[transient] = solved
    return {
        "destination_classes": [CLASS_NAMES[index] for index in destinations],
        "height": height,
        "hitting_residual": residual,
        "max_abs_total_gap": float(np.max(np.abs(totals - 1.0))),
        "transient_count": int(transient.size),
    }


def distributions_at_starts(height: np.ndarray, starts: list[int]) -> np.ndarray:
    return np.vstack([height[start] for start in starts])


def absorbing_kernel(landing: np.ndarray, destination_classes: list[str]) -> tuple[np.ndarray, np.ndarray]:
    """Copy of the epoch kernel with the destination classes made absorbing.

    Integer index pairs set the diagonal. A boolean-boolean assignment would
    fill the destination block instead of the self-loops.
    """
    state_class = _state_class()
    name_to_index = {name: index for index, name in enumerate(CLASS_NAMES)}
    destination_ids = [name_to_index[name] for name in destination_classes]
    absorbing = np.isin(state_class, destination_ids)
    modified = np.array(landing, copy=True)
    indices = np.flatnonzero(absorbing)
    modified[indices, :] = 0.0
    modified[indices, indices] = 1.0
    return modified, absorbing


def absorbing_survival(
    landing: np.ndarray,
    starts: list[int],
    horizon: int,
    destination_classes: list[str],
) -> float:
    """Largest mass, over starts, still outside the two destinations after ``horizon`` pair events."""
    modified, absorbing = absorbing_kernel(landing, destination_classes)
    current = np.zeros((len(starts), N_FULL_STATES), dtype=np.float64)
    for row, start in enumerate(starts):
        current[row, start] = 1.0
    for _ in range(horizon):
        current = current @ modified
    return float(np.max(current[:, ~absorbing].sum(axis=1)))


def propagate_pair_marginals(
    landing: np.ndarray,
    starts: list[int],
    checkpoints: tuple[int, ...] = CHECKPOINTS,
    horizon: int = OCCUPANCY_HORIZON,
) -> dict:
    """Pair-mask, class, and edge-count laws at each checkpoint, plus mean occupancy on epochs 1..horizon."""
    current = np.zeros((len(starts), N_FULL_STATES), dtype=np.float64)
    for row, start in enumerate(starts):
        current[row, start] = 1.0
    pair_class = np.asarray(CLASS_OF_MASK, dtype=np.int32)
    edges = class_edge_counts()
    class_of_mask_rows = []
    wanted = set(checkpoints)
    stored_masks: dict[int, np.ndarray] = {}
    occupancy = np.zeros((len(starts), 11), dtype=np.float64)
    last = 0
    for step in range(1, horizon + 1):
        current = current @ landing
        pair_mass = current.reshape(len(starts), N_TRIAD_STATES, N_PAIR_STATES).sum(axis=1)
        class_mass = np.zeros((len(starts), 11), dtype=np.float64)
        for mask, class_index in enumerate(pair_class):
            class_mass[:, class_index] += pair_mass[:, mask]
        occupancy += class_mass
        if step in wanted:
            stored_masks[step] = pair_mass
        last = step
    if last != horizon:
        raise CalibrationError("checkpoint propagation stopped early")
    return {
        "class_occupancy_epochs_1_to_horizon": occupancy / float(horizon),
        "mask_at_checkpoint": stored_masks,
    }


def class_from_mask(mask_conditional: np.ndarray) -> np.ndarray:
    pair_class = np.asarray(CLASS_OF_MASK, dtype=np.int32)
    out = np.zeros((mask_conditional.shape[0], 11), dtype=np.float64)
    for mask, class_index in enumerate(pair_class):
        out[:, class_index] += mask_conditional[:, mask]
    return out


def occupancy_shares_from_classes(class_share: np.ndarray) -> dict[str, np.ndarray]:
    edges = class_edge_counts()
    sparse = np.zeros(class_share.shape[0], dtype=np.float64)
    three = np.zeros(class_share.shape[0], dtype=np.float64)
    dense = np.zeros(class_share.shape[0], dtype=np.float64)
    for index, edge_count in enumerate(edges):
        if edge_count <= 2:
            sparse += class_share[:, index]
        elif edge_count == 3:
            three += class_share[:, index]
        else:
            dense += class_share[:, index]
    return {
        "dense_minus_sparse": dense - sparse,
        "dense_share": dense,
        "sparse_share": sparse,
        "three_edge_share": three,
    }


def stationary_distribution(kernel: Kernel) -> dict:
    pi, residual, arithmetic, periods = float_stationary(kernel)
    if pi.shape != (kernel.n_states,):
        raise CalibrationError("stationary vector has the wrong length")
    total = float(pi.sum())
    if abs(total - 1.0) > 1e-8:
        raise CalibrationError(f"stationary mass is {total}")
    negative = float(np.min(pi))
    return {
        "arithmetic": arithmetic,
        "mass": total,
        "min_entry": negative,
        "periods": [int(period) for period in periods],
        "pi": pi / total,
        "residual": float(residual),
    }


def _cmi_from_joint(joint: np.ndarray) -> float:
    """``I(T; E | Z)`` from a joint array shaped ``(triad, outcome, conditioner)``."""
    total = float(joint.sum())
    if total <= 0.0:
        raise CalibrationError("conditional information received no mass")
    probability = joint / total
    conditioner = probability.sum(axis=(0, 1))
    triad_conditioner = probability.sum(axis=1)
    outcome_conditioner = probability.sum(axis=0)
    information = 0.0
    triad_count, outcome_count, conditioner_count = probability.shape
    for triad in range(triad_count):
        for outcome in range(outcome_count):
            for condition in range(conditioner_count):
                cell = probability[triad, outcome, condition]
                if cell <= 0.0:
                    continue
                information += cell * math.log(
                    (cell * conditioner[condition])
                    / (triad_conditioner[triad, condition] * outcome_conditioner[outcome, condition])
                )
    return float(information)


def balanced_slot_cmi(law: np.ndarray) -> float:
    """``I(T; slot | pair mask)`` with every full state weighted equally."""
    joint = np.zeros((N_TRIAD_STATES, PAIR_SLOT_COUNT, N_PAIR_STATES), dtype=np.float64)
    for triad in range(N_TRIAD_STATES):
        for mask in range(N_PAIR_STATES):
            state = mask | (triad << PAIR_SLOTS)
            joint[triad, :, mask] = law[state]
    return _cmi_from_joint(joint)


def stationary_slot_cmi(kernel: Kernel, pi: np.ndarray, full_event: np.ndarray) -> float:
    """Long-run pair-event weighting ``pi(s) P(next full event is slot e | s)``."""
    joint = np.zeros((N_TRIAD_STATES, PAIR_SLOT_COUNT, N_PAIR_STATES), dtype=np.float64)
    for state in range(kernel.n_states):
        mask = state & (N_PAIR_STATES - 1)
        triad = state >> PAIR_SLOTS
        joint[triad, :, mask] += pi[state] * full_event[state]
    return _cmi_from_joint(joint)


def empirical_slot_cmi(visit_counts: np.ndarray, law: np.ndarray) -> float:
    """Visit counts of pre-pair-event states, with the exact slot law at each state."""
    joint = np.zeros((N_TRIAD_STATES, PAIR_SLOT_COUNT, N_PAIR_STATES), dtype=np.float64)
    for triad in range(N_TRIAD_STATES):
        for mask in range(N_PAIR_STATES):
            state = mask | (triad << PAIR_SLOTS)
            count = visit_counts[triad, mask]
            if count:
                joint[triad, :, mask] = count * law[state]
    return _cmi_from_joint(joint)


def _next_class_law(law: np.ndarray) -> np.ndarray:
    """``P(next pair class | s)`` from a pair-slot law. Slot ``e`` toggles pair bit ``e``."""
    pair_class = np.asarray(CLASS_OF_MASK, dtype=np.int32)
    out = np.zeros((N_FULL_STATES, 11), dtype=np.float64)
    for state in range(N_FULL_STATES):
        mask = state & (N_PAIR_STATES - 1)
        for slot in range(PAIR_SLOT_COUNT):
            nxt = mask ^ (1 << slot)
            out[state, pair_class[nxt]] += law[state, slot]
    return out


def _joint_from_state_outcome(weights: np.ndarray, outcome_law: np.ndarray, conditioner: np.ndarray) -> np.ndarray:
    n_outcomes = outcome_law.shape[1]
    n_conditions = int(conditioner.max()) + 1
    joint = np.zeros((N_TRIAD_STATES, n_outcomes, n_conditions), dtype=np.float64)
    for state in range(N_FULL_STATES):
        if weights[state] == 0.0:
            continue
        mask = state & (N_PAIR_STATES - 1)
        triad = state >> PAIR_SLOTS
        joint[triad, :, conditioner[mask]] += weights[state] * outcome_law[state]
    return joint


def coarse_class_cmi(state_weight: np.ndarray, slot_law: np.ndarray) -> dict:
    """Exact-law information when the conditioner is the 11-class label."""
    pair_class = np.asarray(CLASS_OF_MASK, dtype=np.int32)
    class_law = _next_class_law(slot_law)
    slot_joint = _joint_from_state_outcome(state_weight, slot_law, pair_class)
    class_joint = _joint_from_state_outcome(state_weight, class_law, pair_class)
    return {
        "next_pair_class_given_pair_class": _cmi_from_joint(class_joint),
        "next_pair_slot_given_pair_class": _cmi_from_joint(slot_joint),
    }


def visits_from_slot_mask_cells(cells: list[dict]) -> np.ndarray:
    """Pre-pair-event visit counts. Summing the sampled slot recovers the state occupancy."""
    visits = np.zeros((N_TRIAD_STATES, N_PAIR_STATES), dtype=np.float64)
    for item in cells:
        visits[int(item["x"]), int(item["z"])] += float(item["count"])
    return visits


def empirical_state_weight(visits: np.ndarray) -> np.ndarray:
    weight = np.zeros(N_FULL_STATES, dtype=np.float64)
    for triad in range(N_TRIAD_STATES):
        for mask in range(N_PAIR_STATES):
            weight[mask | (triad << PAIR_SLOTS)] = visits[triad, mask]
    return weight


def stationary_state_weight(pi: np.ndarray, full_event: np.ndarray) -> np.ndarray:
    """Weight of ``s`` among pair events: ``pi(s) P(next event is a pair event | s)``."""
    return pi * full_event.sum(axis=1)


def plugin_from_contingency(contingency: dict) -> float | None:
    return mutual_information({str(key): {str(outcome): float(count) for outcome, count in counts.items()} for key, counts in contingency.items()})


def plugin_cmi_from_cells(cells: list[dict]) -> dict:
    counted: dict[tuple, int] = {}
    for item in cells:
        counted[(item["x"], item["y"], item["z"])] = int(item["count"])
    return conditional_mutual_information(counted)


def reproduce_plugin_tables(tables: dict) -> dict:
    """Layer A. Recompute committed Generation 8A plug-in values from their counts."""
    gaps = []

    def check(layer: str, system: str, source: str, label: str, published, recomputed) -> None:
        if published is None or recomputed is None:
            gaps.append(
                {
                    "gap": None,
                    "label": label,
                    "layer": layer,
                    "recomputed": recomputed,
                    "published": published,
                    "source_graph_class": source,
                    "system_id": system,
                }
            )
            return
        gaps.append(
            {
                "gap": float(recomputed) - float(published),
                "label": label,
                "layer": layer,
                "recomputed": float(recomputed),
                "published": float(published),
                "source_graph_class": source,
                "system_id": system,
            }
        )

    for row in tables["uniform_raw_triad_information"]:
        check(
            "plugin_first_destination",
            row["system_id"],
            row["source_graph_class"],
            "uniform_raw",
            row["nats"],
            plugin_from_contingency(row["contingency"]),
        )
    for row in tables["checkpoint_pair_class_information"]:
        check(
            "plugin_checkpoint_class",
            row["system_id"],
            row["source_graph_class"],
            f"checkpoint_{row['checkpoint']}",
            row["nats"],
            plugin_from_contingency(row["contingency"]),
        )
    for row in tables["current_context"]:
        for key in (
            "current_triad_next_pair_class_given_pair_class",
            "current_triad_next_pair_slot_given_pair_class",
            "current_triad_next_pair_slot_given_full_pair_mask",
        ):
            recomputed = plugin_cmi_from_cells(row["cells"][key])
            check(
                "plugin_current_context",
                row["system_id"],
                row["source_graph_class"],
                key,
                row[key]["nats"],
                recomputed["nats"],
            )
    worst = max((abs(item["gap"]) for item in gaps if item["gap"] is not None), default=0.0)
    return {
        "cells": gaps,
        "max_abs_gap": worst,
        "tolerance": PLUGIN_REPRODUCTION_TOLERANCE,
        "within_tolerance": worst <= PLUGIN_REPRODUCTION_TOLERANCE,
    }


def _codes(values: list[str]) -> tuple[np.ndarray, list[str]]:
    index = {value: position for position, value in enumerate(sorted(set(values)))}
    return np.fromiter((index[value] for value in values), dtype=np.int32, count=len(values)), sorted(index)


def mutual_information_codes(contexts: np.ndarray, outcomes: np.ndarray) -> float:
    n_contexts = int(contexts.max()) + 1
    n_outcomes = int(outcomes.max()) + 1
    joint = np.bincount(contexts * n_outcomes + outcomes, minlength=n_contexts * n_outcomes).astype(np.float64)
    joint = joint.reshape(n_contexts, n_outcomes)
    total = float(joint.sum())
    if total <= 0.0:
        return 0.0
    probability = joint / total
    context_marginal = probability.sum(axis=1)
    outcome_marginal = probability.sum(axis=0)
    information = 0.0
    for context in range(n_contexts):
        if context_marginal[context] <= 0.0:
            continue
        for outcome in range(n_outcomes):
            cell = probability[context, outcome]
            if cell <= 0.0:
                continue
            information += cell * math.log(cell / (context_marginal[context] * outcome_marginal[outcome]))
    return float(information)


def expand_contingency(contingency: dict[str, dict[str, float]]) -> tuple[np.ndarray, np.ndarray]:
    contexts: list[str] = []
    outcomes: list[str] = []
    for context in sorted(contingency):
        for outcome, count in sorted(contingency[context].items()):
            copies = int(round(float(count)))
            if abs(copies - float(count)) > 1e-6:
                raise CalibrationError(f"contingency count {count} is not an integer episode count")
            contexts.extend([str(context)] * copies)
            outcomes.extend([str(outcome)] * copies)
    context_codes, _names = _codes(contexts)
    outcome_codes, _outcomes = _codes(outcomes)
    return context_codes, outcome_codes


def _generator(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(np.uint64(seed)))


def initial_null_values(
    contingency: dict[str, dict[str, float]],
    *,
    estimand_id: str,
    system_id: str,
    source_graph: str,
    count: int,
    start: int = 0,
) -> np.ndarray:
    """Plug-in values for permutation indexes ``start .. start+count-1``.

    Each index has its own seed, so a later block continues the earlier one.
    """
    contexts, outcomes = expand_contingency(contingency)
    null = np.empty(count, dtype=np.float64)
    for offset in range(count):
        generator = _generator(permutation_seed(estimand_id, system_id, source_graph, start + offset))
        shuffled = generator.permutation(contexts)
        null[offset] = mutual_information_codes(shuffled, outcomes)
    return null


def permutation_null_initial(
    contingency: dict[str, dict[str, float]],
    *,
    estimand_id: str,
    system_id: str,
    source_graph: str,
    count: int,
    start: int = 0,
) -> dict:
    """Shuffle context labels. Outcome values and the label multiset stay fixed.

    This is finite-table bias calibration. It is not a trajectory-level interval.
    """
    contexts, outcomes = expand_contingency(contingency)
    observed = mutual_information_codes(contexts, outcomes)
    null = initial_null_values(
        contingency,
        estimand_id=estimand_id,
        system_id=system_id,
        source_graph=source_graph,
        count=count,
        start=start,
    )
    return _null_summary(observed, null)


def _null_summary(observed: float, null: np.ndarray) -> dict:
    ordered = np.sort(null)
    count = ordered.size
    mean = float(ordered.mean()) if count else 0.0
    variance = float(np.mean((ordered - mean) ** 2)) if count else 0.0
    deviation = math.sqrt(variance)
    if count == 0:
        percentile = None
    else:
        percentile = 100.0 * float(np.searchsorted(ordered, observed, side="right")) / count
    excess = float(observed - mean)

    def _at(fraction: float) -> float | None:
        if count == 0:
            return None
        return float(ordered[percentile_rank(count, fraction)])

    return {
        "null_count": int(count),
        "null_mean": mean,
        "null_median": float(ordered[count // 2]) if count else None,
        "null_p05": _at(0.05),
        "null_p50": _at(0.50),
        "null_p95": _at(0.95),
        "null_p99": _at(0.99),
        "null_percentile_of_observed": percentile,
        "null_sd": deviation,
        "observed_plugin": float(observed),
        "plugin_minus_null_mean": excess,
        "standardised_excess": None if deviation == 0.0 else excess / deviation,
    }


def _strata_from_cells(cells: list[dict]) -> dict:
    strata: dict = {}
    for item in cells:
        strata.setdefault(item["z"], []).append((item["x"], item["y"], int(item["count"])))
    return strata


def cmi_codes_from_cells(cells: list[dict]) -> float:
    return float(plugin_cmi_from_cells(cells)["nats"])


def cmi_from_count_tables(tables: list[np.ndarray]) -> float:
    """``I(X;Y|Z)`` in nats. Each array is one conditioner stratum, shaped ``(x, y)``."""
    total = float(sum(float(table.sum()) for table in tables))
    if total <= 0.0:
        raise CalibrationError("conditional information received no mass")
    information = 0.0
    for table in tables:
        mass = np.asarray(table, dtype=np.float64)
        zone = float(mass.sum())
        if zone <= 0.0:
            continue
        probability = mass / total
        positive = probability > 0.0
        if not np.any(positive):
            continue
        zone_probability = zone / total
        context = mass.sum(axis=1) / total
        outcome = mass.sum(axis=0) / total
        denominator = context[:, None] * outcome[None, :]
        ratio = np.ones_like(probability)
        np.divide(probability * zone_probability, denominator, out=ratio, where=positive)
        information += float(np.sum(probability * np.log(ratio), where=positive))
    return float(information)


def _prepared_conditional_tables(cells: list[dict]) -> list[np.ndarray]:
    prepared = []
    for _condition, triples in _strata_from_cells(cells).items():
        outcomes = sorted({item[1] for item in triples}, key=str)
        triads = sorted({item[0] for item in triples}, key=str)
        outcome_index = {value: position for position, value in enumerate(outcomes)}
        triad_index = {value: position for position, value in enumerate(triads)}
        table = np.zeros((len(triads), len(outcomes)), dtype=np.int64)
        for triad, outcome, copies in triples:
            table[triad_index[triad], outcome_index[outcome]] += copies
        prepared.append(table)
    return prepared


def conditional_null_values(
    cells: list[dict],
    *,
    estimand_id: str,
    system_id: str,
    source_graph: str,
    count: int,
    start: int = 0,
) -> np.ndarray:
    """Plug-in values for within-stratum permutations ``start .. start+count-1``."""
    prepared = _prepared_conditional_tables(cells)
    null = np.empty(count, dtype=np.float64)
    for offset in range(count):
        generator = _generator(permutation_seed(estimand_id, system_id, source_graph, start + offset))
        drawn = []
        for table in prepared:
            remaining = table.sum(axis=1).astype(np.int64)
            resampled = np.zeros_like(table)
            for column in range(table.shape[1]):
                need = int(table[:, column].sum())
                if need == 0:
                    continue
                take = generator.multivariate_hypergeometric(remaining, need)
                remaining -= take
                resampled[:, column] = take
            drawn.append(resampled)
        null[offset] = cmi_from_count_tables(drawn)
    return null


def permutation_null_conditional(
    cells: list[dict],
    *,
    estimand_id: str,
    system_id: str,
    source_graph: str,
    count: int,
    start: int = 0,
) -> dict:
    """Permute ``T`` inside each conditioner stratum.

    The observed outcome and conditioner marginals stay fixed. Serial
    dependence inside an episode is not preserved, so the null describes
    finite-table plug-in bias rather than a complete trajectory interval.
    """
    observed = cmi_codes_from_cells(cells)
    null = conditional_null_values(
        cells,
        estimand_id=estimand_id,
        system_id=system_id,
        source_graph=source_graph,
        count=count,
        start=start,
    )
    summary = _null_summary(observed, null)
    summary["calibration"] = "finite_table_plugin_bias"
    summary["serial_dependence"] = "not preserved; episode order is outside this null"
    return summary


def identity_permutation_matches(contingency: dict[str, dict[str, float]]) -> bool:
    contexts, outcomes = expand_contingency(contingency)
    return mutual_information_codes(contexts, outcomes) == mutual_information_codes(contexts.copy(), outcomes)


def percentile_rank(ordered_count: int, fraction: float) -> int:
    """Nearest-rank index ``min(n-1, max(0, ceil(fraction * n) - 1))``."""
    if ordered_count <= 0:
        raise ValueError("a percentile needs a non-empty sample")
    return min(ordered_count - 1, max(0, math.ceil(fraction * ordered_count) - 1))


def assert_zero_floor(value: float, label: str, floor: float = ZERO_INFORMATION_FLOOR) -> None:
    if abs(value) > floor:
        raise CalibrationError(f"{label} is {value}, above the numerical floor {floor}")


def source_start_states() -> dict[str, list[int]]:
    masks = source_masks()
    return {
        key: [masks[key] | (triad << PAIR_SLOTS) for triad in range(N_TRIAD_STATES)]
        for key in ("star", "path", "triangle")
    }


def symmetry_destination_gap(expressions: list[str], pair_mask: int, distributions: np.ndarray) -> float:
    """Largest L1 gap inside a rule-aware orbit. ``distributions`` is ordered by raw triad 0..15."""
    partition = rule_aware_partition(pair_mask, expressions)
    gap = 0.0
    for orbit in partition["orbits"]:
        members = orbit["members"]
        base = distributions[members[0]]
        for triad in members[1:]:
            gap = max(gap, float(np.abs(distributions[triad] - base).sum()))
    return gap


def destination_compatibility(exact: np.ndarray, counts: dict[str, float], names: list[str]) -> float:
    total = sum(counts.values()) or 1.0
    empirical = np.array([float(counts.get(name, 0.0)) / total for name in names], dtype=np.float64)
    return float(np.max(np.abs(empirical - exact)))


def load_a0_palette() -> list[dict]:
    systems = load_repair_palette()
    if [row["system_id"] for row in systems] != [item[0] for item in PALETTE]:
        raise CalibrationError("A0 palette order drifted")
    return systems


def analysis_constants() -> dict:
    return {
        "chain_rule_tolerance": CHAIN_RULE_TOLERANCE,
        "checkpoints": list(CHECKPOINTS),
        "cross_solver_tolerance": CROSS_SOLVER_TOLERANCE,
        "current_permutations": CURRENT_PERMUTATIONS,
        "hitting_residual_tolerance": HITTING_RESIDUAL_TOLERANCE,
        "initial_permutations": INITIAL_PERMUTATIONS,
        "kernel_row_tolerance": KERNEL_ROW_TOLERANCE,
        "occupancy_epochs": "1..512 inclusive",
        "occupancy_horizon": OCCUPANCY_HORIZON,
        "plugin_reproduction_tolerance": PLUGIN_REPRODUCTION_TOLERANCE,
        "stationary_residual_tolerance": STATIONARY_RESIDUAL_TOLERANCE,
        "unabsorbed_horizon_tolerance": UNABSORBED_HORIZON_TOLERANCE,
        "zero_information_floor": ZERO_INFORMATION_FLOOR,
        "zero_systems": list(ZERO_SYSTEMS),
    }


def layout_guard(kernel: Kernel) -> None:
    n_pairs, n_triads = layout(kernel)
    if n_pairs != PAIR_SLOT_COUNT or n_triads != 4 or kernel.n_states != N_FULL_STATES:
        raise CalibrationError(f"layout drifted: pairs {n_pairs} triads {n_triads} states {kernel.n_states}")


def plugin_mutual_information_reference(by_context: dict[str, dict[str, float]]) -> float | None:
    """The Generation 8A function, used so Layer A cannot drift onto another formula."""
    return _mutual_information(by_context)
