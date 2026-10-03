"""Baseline-relative reconfiguration of pairwise isomorphism classes.

The free hypercube makes many class-to-class paths reachable. Reachability
is not the observation. The predeclared comparison is the difference of
stationary pair-event fluxes:

    delta_flux(X, Y) = F_constrained(X, Y) - F_baseline(X, Y)

F(X, Y) is the stationary probability that one pair-event step goes from
isomorphism class X to isomorphism class Y. The epoch measure is the landing
distribution of pair-changing transitions. The class-to-class matrix is an
observable of that chain. It is not a lumped Markov model, and states are
not aggregated merely because they share an orbit.

The ranking scalar, fixed before the census, is the maximum absolute
delta_flux over ordered pairs whose classes have the same edge count and
are not isomorphic. The horizon below is not adjusted after results are seen.

Different edge count, same edge count and isomorphic, and same edge count
and non-isomorphic are recorded as separate categories. Only the last is
called structural reconfiguration.
"""

from __future__ import annotations

import numpy as np

from rs_constraint_lab.graphs import PairClassTable, pair_classes
from rs_constraint_lab.memory_clocks import FLOAT_TV_FLOOR, _epoch_flux_float, layout

# Predeclared before any N=4 census maximum is inspected.
RECONFIGURATION_MEASURE = "max_abs_stationary_pair_event_class_flux_delta"
RECONFIGURATION_HORIZON = 16
EFFECT_FLOOR = FLOAT_TV_FLOOR


def _epoch_distribution(kernel, pi, landing: np.ndarray) -> np.ndarray:
    flux = _epoch_flux_float(kernel, pi)
    row_mass = landing.sum(axis=1)
    active = (flux > 0.0) & (row_mass > 0.0)
    total = float(flux[active].sum())
    out = np.zeros(kernel.n_states, dtype=np.float64)
    if total <= 0.0:
        return out
    out[active] = flux[active] / total
    return out


def class_flux(kernel, pi: np.ndarray, landing: np.ndarray, table: PairClassTable | None = None) -> np.ndarray:
    """Stationary pair-event flux between canonical pairwise classes."""
    table = table or pair_classes()
    n_pairs, _n_triads = layout(kernel)
    mask = (1 << n_pairs) - 1
    mu = _epoch_distribution(kernel, pi, landing)
    representatives = table.representatives
    index = {mask_id: position for position, mask_id in enumerate(representatives)}
    width = len(representatives)
    pair = np.arange(kernel.n_states) & mask
    class_index = np.array([index[table.class_of[int(item)]] for item in pair], dtype=np.int32)
    flux = np.zeros((width, width), dtype=np.float64)
    sources = np.flatnonzero(mu)
    for state in sources:
        mass = float(mu[state])
        left = int(class_index[state])
        row = landing[state]
        for target in np.flatnonzero(row):
            flux[left, int(class_index[target])] += mass * float(row[target])
    return flux


def _category(table: PairClassTable, left: int, right: int) -> str:
    if table.by_mask[left]["edge_count"] != table.by_mask[right]["edge_count"]:
        return "different_edge_count"
    if left == right:
        return "same_edge_count_isomorphic"
    return "same_edge_count_nonisomorphic"


def _category_totals(table: PairClassTable, flux: np.ndarray) -> dict[str, float]:
    totals = {
        "different_edge_count": 0.0,
        "same_edge_count_isomorphic": 0.0,
        "same_edge_count_nonisomorphic": 0.0,
    }
    for left_index, left in enumerate(table.representatives):
        for right_index, right in enumerate(table.representatives):
            totals[_category(table, left, right)] += float(flux[left_index, right_index])
    return totals


def _hit_before_return(
    landing: np.ndarray,
    mu: np.ndarray,
    class_index: np.ndarray,
    source: int,
    target: int,
    horizon: int,
) -> dict:
    source_mask = class_index == source
    target_mask = class_index == target
    other_mask = ~(source_mask | target_mask)
    start = np.where(source_mask, mu, 0.0)
    total = float(start.sum())
    if total <= 0.0:
        return {"defined": False}
    dist = start / total
    hit = 0.0
    returned = 0.0
    moment = 0.0
    for step in range(1, horizon + 1):
        nxt = dist @ landing
        hit_mass = float(nxt[target_mask].sum())
        return_mass = float(nxt[source_mask].sum())
        hit += hit_mass
        returned += return_mass
        moment += step * hit_mass
        dist = np.where(other_mask, nxt, 0.0)
    unresolved = float(dist.sum())
    mean = None
    mean_status = "undefined"
    if hit > EFFECT_FLOOR and unresolved <= EFFECT_FLOOR:
        mean = moment / hit
        mean_status = "conditional_on_hit_within_horizon"
    elif hit > EFFECT_FLOOR:
        mean = moment / hit
        mean_status = "truncated_lower_bound_within_horizon"
    return {
        "defined": True,
        "hit_before_return": hit,
        "return_before_hit": returned,
        "unresolved_within_horizon": unresolved,
        "mean_pair_events_given_hit": mean,
        "mean_status": mean_status,
        "horizon": horizon,
    }


def _one_step_by_triad(
    landing: np.ndarray,
    mu: np.ndarray,
    class_index: np.ndarray,
    n_pairs: int,
    source: int,
    width: int,
) -> list[np.ndarray | None]:
    laws: list[np.ndarray | None] = []
    n_t = len(mu) >> n_pairs
    for triad in range(n_t):
        shift = triad << n_pairs
        selected = []
        mass = 0.0
        for state in range(shift, shift + (1 << n_pairs)):
            if class_index[state] == source and mu[state] > 0.0:
                selected.append(state)
                mass += float(mu[state])
        if mass <= 0.0:
            laws.append(None)
            continue
        law = np.zeros(width, dtype=np.float64)
        for state in selected:
            weight = float(mu[state]) / mass
            row = landing[state]
            for target in np.flatnonzero(row):
                law[int(class_index[target])] += weight * float(row[target])
        laws.append(law)
    return laws


def focused_transition(
    kernel,
    pi: np.ndarray,
    landing: np.ndarray,
    source_name: str,
    target_name: str,
    table: PairClassTable | None = None,
    horizon: int = RECONFIGURATION_HORIZON,
) -> dict:
    """One ordered class transition, including the triad-conditioned hit."""
    table = table or pair_classes()
    n_pairs, _n_triads = layout(kernel)
    mask = (1 << n_pairs) - 1
    mu = _epoch_distribution(kernel, pi, landing)
    representatives = table.representatives
    index = {mask_id: position for position, mask_id in enumerate(representatives)}
    name_index = {table.by_mask[mask_id]["name"]: index[mask_id] for mask_id in representatives}
    if source_name not in name_index or target_name not in name_index:
        return {"defined": False, "reason": "class name is not in the N=4 table"}
    source = name_index[source_name]
    target = name_index[target_name]
    pair = np.arange(kernel.n_states) & mask
    class_index = np.array([index[table.class_of[int(item)]] for item in pair], dtype=np.int32)
    passage = _hit_before_return(landing, mu, class_index, source, target, horizon)
    spread = _triad_conditioned_spread(landing, mu, class_index, n_pairs, source, target, horizon)
    laws = _one_step_by_triad(landing, mu, class_index, n_pairs, source, len(representatives))
    defined_laws = [law for law in laws if law is not None]
    one_step_spread = 0.0
    if len(defined_laws) >= 2:
        hits = [float(law[target]) for law in defined_laws]
        one_step_spread = max(hits) - min(hits)
    return {
        "defined": passage.get("defined", False),
        "source": source_name,
        "target": target_name,
        "horizon": horizon,
        "passage": passage,
        "triad_hit_spread": spread["spread"] if spread.get("defined") else None,
        "triad_changes_hit": bool(spread.get("defined") and spread["spread"] > EFFECT_FLOOR),
        "one_step_target_spread_across_triads": one_step_spread,
        "triad_changes_one_step": one_step_spread > EFFECT_FLOOR,
    }


def _triad_conditioned_spread(landing, mu, class_index, n_pairs, source, target, horizon) -> dict:
    """Spread of hit-before-return across triadic configurations.

    The configurations are advanced together. This does not lump the pair
    classes into a quotient chain.
    """
    n_t = len(mu) >> n_pairs
    span = 1 << n_pairs
    source_mask = class_index == source
    target_mask = class_index == target
    other_mask = ~(source_mask | target_mask)
    starts = []
    for triad in range(n_t):
        shift = triad << n_pairs
        selected = np.zeros(len(mu), dtype=np.float64)
        window = slice(shift, shift + span)
        selected[window] = np.where(source_mask[window], mu[window], 0.0)
        total = float(selected.sum())
        if total <= EFFECT_FLOOR:
            continue
        starts.append(selected / total)
    if len(starts) < 2:
        return {"defined": False, "spread": 0.0}
    dist = np.stack(starts)
    hit = np.zeros(len(starts), dtype=np.float64)
    for _step in range(1, horizon + 1):
        nxt = dist @ landing
        hit += nxt[:, target_mask].sum(axis=1)
        dist = np.where(other_mask, nxt, 0.0)
    return {"defined": True, "spread": float(hit.max() - hit.min())}


def compare_reconfiguration(kernel, baseline_kernel, pi, baseline_pi, landing, baseline_landing) -> dict:
    """Primary census observable for one constrained kernel against its baseline."""
    table = pair_classes()
    constrained = class_flux(kernel, pi, landing, table)
    baseline = class_flux(baseline_kernel, baseline_pi, baseline_landing, table)
    delta = constrained - baseline
    best_abs = 0.0
    best = None
    structural_pairs = 0
    for left_index, left in enumerate(table.representatives):
        for right_index, right in enumerate(table.representatives):
            if _category(table, left, right) != "same_edge_count_nonisomorphic":
                continue
            structural_pairs += 1
            value = float(delta[left_index, right_index])
            if best is None or abs(value) > best_abs:
                base = float(baseline[left_index, right_index])
                best_abs = abs(value)
                best = {
                    "source": table.by_mask[left]["name"],
                    "target": table.by_mask[right]["name"],
                    "edge_count": table.by_mask[left]["edge_count"],
                    "delta_flux": value,
                    "constrained_flux": float(constrained[left_index, right_index]),
                    "baseline_flux": base,
                    "ratio": None if base <= EFFECT_FLOOR else float(constrained[left_index, right_index]) / base,
                }
    constrained_totals = _category_totals(table, constrained)
    baseline_totals = _category_totals(table, baseline)
    path = table.path_name
    matching = table.matching_name
    forward = focused_transition(kernel, pi, landing, path, matching, table)
    backward = focused_transition(kernel, pi, landing, matching, path, table)
    base_forward = focused_transition(baseline_kernel, baseline_pi, baseline_landing, path, matching, table)
    base_backward = focused_transition(baseline_kernel, baseline_pi, baseline_landing, matching, path, table)
    return {
        "measure": RECONFIGURATION_MEASURE,
        "horizon": RECONFIGURATION_HORIZON,
        "lumpability_assumed": False,
        "structural_class_pairs": structural_pairs,
        "max_abs_delta_flux": best_abs,
        "argmax": best,
        "effect": best_abs > EFFECT_FLOOR,
        "category_flux_constrained": constrained_totals,
        "category_flux_baseline": baseline_totals,
        "category_flux_delta": {
            key: constrained_totals[key] - baseline_totals[key] for key in constrained_totals
        },
        "focused_path_to_matching": _with_baseline(forward, base_forward),
        "focused_matching_to_path": _with_baseline(backward, base_backward),
        "focused_classes": {"path": path, "matching": matching},
    }


def _with_baseline(constrained: dict, baseline: dict) -> dict:
    constrained_hit = (constrained.get("passage") or {}).get("hit_before_return")
    baseline_hit = (baseline.get("passage") or {}).get("hit_before_return")
    delta_hit = None
    if constrained_hit is not None and baseline_hit is not None:
        delta_hit = constrained_hit - baseline_hit
    return {
        "constrained": constrained,
        "baseline_hit_before_return": baseline_hit,
        "delta_hit_before_return": delta_hit,
    }
