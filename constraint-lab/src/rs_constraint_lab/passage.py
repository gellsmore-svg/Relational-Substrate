"""Controlled-source passage and the eventual hit-before-return committor.

STATIONARY_SOURCE_PASSAGE is the Generation 4 quantity. It starts from the
kernel's own pair-event stationary distribution, conditioned on the source
graph class. That definition is unchanged and lives in
``reconfiguration.focused_transition``.

CONTROLLED_SOURCE_PASSAGE uses one reference distribution, ``mu_ref``, taken
from the unconstrained baseline and conditioned on the source class. The same
array is the start for the baseline, a singleton, and a two-rule kernel.
It is not renormalised onto a constrained stationary source.

The eventual committor is horizon-independent. On the pair-event epoch
kernel, for a start ``s`` in source class A, ``q(s)`` is the probability of
reaching target class B before returning to A, after at least one pair event.
Horizon 16 remains a comparator. It is not the primary mechanistic quantity.
"""

from __future__ import annotations

import numpy as np

from rs_constraint_lab.graphs import PairClassTable, pair_classes
from rs_constraint_lab.memory_clocks import layout
from rs_constraint_lab.reconfiguration import (
    EFFECT_FLOOR,
    RECONFIGURATION_HORIZON,
    _epoch_distribution,
    _hit_before_return,
)

PATH_CLASS = "e2-deg2110-tri0-comp2"
MATCHING_CLASS = "e2-deg1111-tri0-comp2"
DIRECT_SOLVER = "numpy.linalg.solve"
ITERATIVE_SOLVER = "fixed-point"


def class_index_array(n_states: int, n_pairs: int, table: PairClassTable | None = None) -> np.ndarray:
    table = table or pair_classes()
    mask = (1 << n_pairs) - 1
    index = {mask_id: position for position, mask_id in enumerate(table.representatives)}
    pair = np.arange(n_states) & mask
    return np.array([index[table.class_of[int(item)]] for item in pair], dtype=np.int32)


def class_position(table: PairClassTable, name: str) -> int:
    for position, mask_id in enumerate(table.representatives):
        if table.by_mask[mask_id]["name"] == name:
            return position
    raise KeyError(name)


def reference_source(mu: np.ndarray, class_index: np.ndarray, source: int) -> np.ndarray:
    """Baseline epoch mass conditioned on one source class.

    The returned array is a new object. Callers that compare kernels must
    pass that same object through; this function is the only place that
    builds it.
    """
    out = np.zeros(mu.shape[0], dtype=np.float64)
    chosen = class_index == source
    total = float(mu[chosen].sum())
    if total <= 0.0:
        return out
    out[chosen] = mu[chosen] / total
    return out


def stationary_source_mu(kernel, pi: np.ndarray, landing: np.ndarray) -> np.ndarray:
    """Pair-event stationary distribution of this kernel. Not a controlled start."""
    return _epoch_distribution(kernel, pi, landing)


def hit_passage(
    landing: np.ndarray,
    mu: np.ndarray,
    class_index: np.ndarray,
    source: int,
    target: int,
    horizon: int = RECONFIGURATION_HORIZON,
) -> dict:
    """Finite-horizon hit-before-return under an explicit start ``mu``.

    ``mu`` is used as given. A constrained kernel does not replace it with
    its own stationary source.
    """
    return _hit_before_return(landing, mu, class_index, source, target, horizon)


def _absorbing_blocks(landing: np.ndarray, class_index: np.ndarray, source: int, target: int):
    source_states = np.flatnonzero(class_index == source)
    target_states = np.flatnonzero(class_index == target)
    other = np.flatnonzero((class_index != source) & (class_index != target))
    rhs = landing[np.ix_(other, target_states)].sum(axis=1) if other.size and target_states.size else np.zeros(other.size)
    block = landing[np.ix_(other, other)] if other.size else np.zeros((0, 0), dtype=np.float64)
    return source_states, target_states, other, block, rhs


def _values_from_transient(n_states: int, other: np.ndarray, target_states: np.ndarray, transient: np.ndarray) -> np.ndarray:
    value = np.zeros(n_states, dtype=np.float64)
    if target_states.size:
        value[target_states] = 1.0
    if other.size:
        value[other] = transient
    return value


def eventual_committor(
    landing: np.ndarray,
    class_index: np.ndarray,
    source: int,
    target: int,
    *,
    method: str = "direct",
    iterative_tolerance: float = 1e-14,
    iterative_limit: int = 100000,
    record_condition: bool = False,
) -> dict:
    """Eventual source-to-target-before-return committor on an epoch kernel.

    For ``u`` outside A and B, ``h(u)`` solves the absorbing equation. For
    ``s`` in A, ``q(s)`` is one epoch step from ``s``. States outside A have
    no ``q`` and are stored as NaN. The solve is float64.
    """
    n_states = landing.shape[0]
    source_states, target_states, other, block, rhs = _absorbing_blocks(landing, class_index, source, target)
    q = np.full(n_states, np.nan, dtype=np.float64)
    record = {
        "solver": DIRECT_SOLVER if method == "direct" else ITERATIVE_SOLVER,
        "method": method,
        "matrix_dimension": int(other.size),
        "residual": None,
        "condition_number": None,
        "conditioning_warning": None,
        "precision": "float64",
        "failure": False,
        "iterations": None,
    }
    if source_states.size == 0:
        record["failure"] = True
        record["failure_reason"] = "source class is empty"
        return {"q": q, "solver": record}
    if other.size == 0:
        value = _values_from_transient(n_states, other, target_states, np.zeros(0, dtype=np.float64))
        q[source_states] = landing[source_states] @ value
        record["residual"] = 0.0
        return {"q": q, "solver": record}
    if method == "iterative":
        transient = np.zeros(other.size, dtype=np.float64)
        iterations = 0
        for iterations in range(1, iterative_limit + 1):
            nxt = block @ transient + rhs
            if float(np.max(np.abs(nxt - transient))) <= iterative_tolerance:
                transient = nxt
                break
            transient = nxt
        else:
            record["failure"] = True
            record["failure_reason"] = "iterative committor did not meet the tolerance"
        record["iterations"] = iterations
    else:
        system = np.eye(other.size, dtype=np.float64) - block
        try:
            transient = np.linalg.solve(system, rhs)
        except np.linalg.LinAlgError:
            record["failure"] = True
            record["failure_reason"] = "direct committor solve failed"
            return {"q": q, "solver": record}
        if record_condition:
            condition = float(np.linalg.cond(system))
            record["condition_number"] = condition
            if condition > 1e12:
                record["conditioning_warning"] = "condition number above 1e12"
        residual_vector = (np.eye(other.size, dtype=np.float64) - block) @ transient - rhs
        record["residual"] = float(np.max(np.abs(residual_vector)))
    if method == "iterative":
        residual_vector = (np.eye(other.size, dtype=np.float64) - block) @ transient - rhs
        record["residual"] = float(np.max(np.abs(residual_vector)))
    value = _values_from_transient(n_states, other, target_states, transient)
    q[source_states] = landing[source_states] @ value
    return {"q": q, "solver": record}


def weighted_mean(q: np.ndarray, mu: np.ndarray) -> float | None:
    """Mean of ``q`` under ``mu`` on the states where ``q`` is defined."""
    defined = np.isfinite(q) & (mu > 0.0)
    total = float(mu[defined].sum())
    if total <= 0.0:
        return None
    return float(mu[defined] @ q[defined] / total)


def triad_conditioned_committor(
    q: np.ndarray,
    mu: np.ndarray,
    n_pairs: int,
    *,
    mass_floor: float = 0.0,
) -> dict:
    """Eventual committor by the full triadic configuration, not its popcount.

    ``mu`` is the fixed source weighting. A configuration with no source mass
    is uncharged and is omitted. The spread is max minus min over charged
    configurations.
    """
    n_t = mu.shape[0] >> n_pairs
    span = 1 << n_pairs
    charged = []
    for triad in range(n_t):
        window = slice(triad << n_pairs, (triad << n_pairs) + span)
        mass = float(mu[window].sum())
        if mass <= mass_floor:
            continue
        defined = np.isfinite(q[window])
        if not np.any(defined):
            continue
        local_mu = np.where(defined, mu[window], 0.0)
        local_total = float(local_mu.sum())
        if local_total <= mass_floor:
            continue
        value = float(local_mu @ np.where(defined, q[window], 0.0) / local_total)
        charged.append({"triad": triad, "mass": mass, "committor": value})
    if not charged:
        return {"defined": False, "spread": None, "min": None, "max": None, "configurations": []}
    values = [row["committor"] for row in charged]
    lowest = min(values)
    highest = max(values)
    return {
        "defined": len(charged) >= 1,
        "spread": float(highest - lowest),
        "min": float(lowest),
        "max": float(highest),
        "min_configurations": [row["triad"] for row in charged if row["committor"] == lowest],
        "max_configurations": [row["triad"] for row in charged if row["committor"] == highest],
        "charged_count": len(charged),
        "configurations": charged,
    }


def interaction_residual(q_tp: float, q_t: float, q_p: float, q_0: float) -> float:
    """``Q_TP - Q_T - Q_P + Q_0``. Zero is additive on this observable."""
    return float(q_tp - q_t - q_p + q_0)


def super_singleton_gap(delta_tp: float, delta_t: float, delta_p: float) -> float:
    """``|Delta_TP| - max(|Delta_T|, |Delta_P|)``. Kept separate from the residual."""
    return float(abs(delta_tp) - max(abs(delta_t), abs(delta_p)))


def state_interaction(q_tp: np.ndarray, q_t: np.ndarray, q_p: np.ndarray, q_0: np.ndarray) -> np.ndarray:
    """``q_TP(s) - q_T(s) - q_P(s) + q_0(s)`` where every factor is defined."""
    out = np.full(q_tp.shape, np.nan, dtype=np.float64)
    defined = np.isfinite(q_tp) & np.isfinite(q_t) & np.isfinite(q_p) & np.isfinite(q_0)
    out[defined] = q_tp[defined] - q_t[defined] - q_p[defined] + q_0[defined]
    return out


def state_summary(delta: np.ndarray, mu: np.ndarray, n_pairs: int) -> dict:
    """Source-resolved passage change. The mean does not replace the extrema."""
    defined = np.isfinite(delta)
    if not np.any(defined):
        return {"defined": False}
    values = delta[defined]
    states = np.flatnonzero(defined)
    positive = float(np.max(values))
    negative = float(np.min(values))
    pos_state = int(states[int(np.argmax(values))])
    neg_state = int(states[int(np.argmin(values))])
    weighted = weighted_mean(np.where(defined, delta, np.nan), mu)
    by_triad = triad_conditioned_committor(np.where(defined, delta, np.nan), mu, n_pairs)
    return {
        "defined": True,
        "baseline_source_weighted_mean": weighted,
        "max_positive": positive,
        "max_negative": negative,
        "max_absolute": float(max(abs(positive), abs(negative))),
        "max_positive_state": pos_state,
        "max_negative_state": neg_state,
        "max_positive_triad": int(pos_state >> n_pairs),
        "max_negative_triad": int(neg_state >> n_pairs),
        "triad_range": by_triad.get("spread"),
        "triad_min_configurations": by_triad.get("min_configurations"),
        "triad_max_configurations": by_triad.get("max_configurations"),
    }


def sign_status(value: float | None, floor: float = EFFECT_FLOOR) -> str:
    if value is None:
        return "undefined"
    if abs(value) <= floor:
        return "zero"
    return "positive" if value > 0.0 else "negative"


def prepare_direction(
    kernel,
    pi: np.ndarray,
    landing: np.ndarray,
    class_index: np.ndarray,
    n_pairs: int,
    source: int,
    target: int,
    mu_ref: np.ndarray,
    *,
    horizon: int = RECONFIGURATION_HORIZON,
    record_condition: bool = False,
) -> dict:
    """Stationary and controlled passage, plus the eventual committor, one direction."""
    own = stationary_source_mu(kernel, pi, landing)
    own_source = reference_source(own, class_index, source)
    stationary_hit = hit_passage(landing, own_source, class_index, source, target, horizon)
    controlled_hit = hit_passage(landing, mu_ref, class_index, source, target, horizon)
    solved = eventual_committor(landing, class_index, source, target, record_condition=record_condition)
    q = solved["q"]
    q_stationary = weighted_mean(q, own_source)
    q_controlled = weighted_mean(q, mu_ref)
    spread = triad_conditioned_committor(q, mu_ref, n_pairs)
    return {
        "q": q,
        "stationary_hit": stationary_hit,
        "controlled_hit": controlled_hit,
        "q_stationary": q_stationary,
        "q_controlled": q_controlled,
        "triad": spread,
        "solver": solved["solver"],
        "mu_ref": mu_ref,
    }


def kernel_layout_index(kernel, table: PairClassTable | None = None):
    table = table or pair_classes()
    n_pairs, _n_triads = layout(kernel)
    return n_pairs, class_index_array(kernel.n_states, n_pairs, table), table
