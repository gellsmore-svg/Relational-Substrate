"""Exact stationary, projection and temporal diagnostics for historical roles."""

from __future__ import annotations

from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import cache

import numpy as np

from rs_constraint_lab.durable import canonical_json, sha256_bytes
from rs_constraint_lab.exact import _stationary_rational, period_of, strongly_connected_components
from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.history import HistoryError, PRECISION, js, mutual_information
from rs_constraint_lab.history_roles import (
    DIRECTIONS, RELATIONS, RoleController, aggregate_quotient, covariance_gap,
    role_descriptors, role_orbits, slot_relation,
)


def fingerprint(payload) -> str:
    return sha256_bytes(canonical_json(payload).encode())


def serial_rows(rows):
    return [sorted(row.items()) for row in rows]


@cache
def material_partition(n=4):
    structure = role_orbits(n)
    if n == 4:
        canonical = pair_classes().class_of
    else:
        canonical = tuple(min(mapping[p] for mapping in structure.mask_maps) for p in range(1 << structure.slots))
    representatives = tuple(sorted(set(canonical)))
    groups = tuple(tuple(p for p, rep in enumerate(canonical) if rep == key) for key in representatives)
    class_of = tuple(representatives.index(rep) for rep in canonical)
    return representatives, groups, class_of


def stationary(rows):
    successors = [tuple(row.items()) for row in rows]
    components = strongly_connected_components(successors)
    if len(components) != 1:
        raise HistoryError(f"multiple communicating classes require separate interpretation: {components}")
    pi = _stationary_rational(components[0], successors)
    vector = [pi[i] for i in range(len(rows))]
    if min(vector) <= 0:
        raise HistoryError("unique positive stationary law required")
    return vector, len(components), period_of(components[0], successors)


def balance_gap(pi, rows):
    incoming = [Fraction(0)] * len(rows)
    for source, row in enumerate(rows):
        for target, value in row.items():
            incoming[target] += pi[source] * value
    return max(abs(left - right) for left, right in zip(incoming, pi))


def detailed_balance_gap(pi, rows):
    return max(abs(pi[source] * value - pi[target] * rows[target].get(source, 0)) for source, row in enumerate(rows) for target, value in row.items())


def currents(pi, rows):
    result = []
    for source in range(len(rows)):
        for target in range(source + 1, len(rows)):
            value = pi[source] * rows[source].get(target, 0) - pi[target] * rows[target].get(source, 0)
            if value:
                result.append({"source": source, "target": target, "net_flow": value})
    return result


@cache
def _ln(value: Fraction) -> Decimal:
    with localcontext() as context:
        context.prec = PRECISION
        return (Decimal(value.numerator) / Decimal(value.denominator)).ln()


def conditional_model_information(left, right, blocks):
    """Compute conditional model MI directly, allowing unequal block priors."""
    masses = defaultdict(lambda: [Fraction(0), Fraction(0)])
    for a, b, block in zip(left, right, blocks):
        masses[block][0] += a
        masses[block][1] += b
    with localcontext() as context:
        context.prec = PRECISION
        result = Decimal(0)
        for a, b, block in zip(left, right, blocks):
            ma, mb = masses[block]
            for value, mass in ((a, ma), (b, mb)):
                if value:
                    ratio = value * (ma + mb) / ((a + b) * mass)
                    result += Decimal(value.numerator) / Decimal(value.denominator) * _ln(ratio) / 2
        return +result


def project(vector, n=4):
    representatives, groups, _ = material_partition(n)
    slots = role_orbits(n).slots
    classes = [sum(vector[p] for p in group) for group in groups]
    counts = [sum(vector[p] for p in range(len(vector)) if p.bit_count() == k) for k in range(slots + 1)]
    conditional = {
        str(k): [value / counts[k] if rep.bit_count() == k else Fraction(0) for rep, value in zip(representatives, classes)]
        for k in range(slots + 1)
    }
    return {"pair_mask": vector, "graph_class_representatives": representatives, "graph_class": classes, "edge_count": counts, "class_given_edge_count": conditional}


def decomposition(left, right, n=4):
    representatives, _, class_of = material_partition(n)
    l, r = project(left, n), project(right, n)
    i_pair = js(left, right)
    i_class = js(l["graph_class"], r["graph_class"])
    i_edge = js(l["edge_count"], r["edge_count"])
    i_shape = conditional_model_information(l["graph_class"], r["graph_class"], [rep.bit_count() for rep in representatives])
    i_label = conditional_model_information(left, right, class_of)
    with localcontext() as context:
        context.prec = PRECISION
        gap = abs(i_pair - i_edge - i_shape - i_label)
    return {
        "pairmask": str(i_pair), "graphclass": str(i_class), "edgecount": str(i_edge),
        "shape_given_edge": str(i_shape), "label_given_class": str(i_label), "chain_gap": str(gap),
    }


def full_crosscheck(rows, lifted, orbit_masses, model):
    size = len(rows)
    transition = np.zeros((size, size))
    for source, row in enumerate(rows):
        for target, probability in row.items():
            transition[source, target] = float(probability)
    matrix = np.vstack((transition.T - np.eye(size), np.ones((1, size)) / np.sqrt(size)))
    rhs = np.zeros(size + 1)
    rhs[-1] = 1 / np.sqrt(size)
    oracle, _, rank, _ = np.linalg.lstsq(matrix, rhs, rcond=None)
    if rank != size:
        raise HistoryError("full-state stationary cross-check lacks unique normalised solution")
    structure = role_orbits(model.n)
    actual_orbits = [sum(oracle[state] for state in group) for group in structure.members]
    actual_pairs = [sum(oracle[p * model.slots:(p + 1) * model.slots]) for p in range(1 << model.slots)]
    predicted_pairs = [sum(lifted[p * model.slots:(p + 1) * model.slots]) for p in range(1 << model.slots)]
    role_gap = 0.0
    for coordinate, width in enumerate((2, 2 * (model.n - 2) + 1, 2, model.n - 1)):
        for value in range(width):
            states = [state for state in range(size) if role_descriptors(*divmod(state, model.slots), model.n)[coordinate] == value]
            role_gap = max(role_gap, abs(sum(oracle[state] for state in states) - float(sum(lifted[state] for state in states))))
    return {
        "performed": True, "method": "independent full-state overdetermined linear balance least-squares solve",
        "joint_gap": float(max(abs(oracle[i] - float(lifted[i])) for i in range(size))),
        "orbit_mass_gap": float(max(abs(a - float(b)) for a, b in zip(actual_orbits, orbit_masses))),
        "pair_marginal_gap": float(max(abs(a - float(b)) for a, b in zip(actual_pairs, predicted_pairs))),
        "role_distribution_gap": float(role_gap),
        "stationary_residual": float(max(abs(oracle @ transition - oracle))),
    }


def projected_order_and_lags(model, pi, rows):
    slots = model.slots
    pairs = 1 << slots
    pair_end = defaultdict(lambda: defaultdict(Fraction))
    triple_end = defaultdict(lambda: defaultdict(Fraction))
    backtrack = lag1 = lag2 = Fraction(0)
    for source, row in enumerate(rows):
        p0 = source // slots
        for middle, first in row.items():
            p1 = middle // slots
            mass1 = pi[source] * first
            pair_end[p0, p1][middle] += mass1
            lag1 += mass1 * p0.bit_count() * p1.bit_count()
            for target, second in rows[middle].items():
                p2 = target // slots
                mass2 = mass1 * second
                triple_end[p0, p1, p2][target] += mass2
                lag2 += mass2 * p0.bit_count() * p2.bit_count()
                if p2 == p0:
                    backtrack += mass2

    def conditional(endpoints):
        normaliser = sum(endpoints.values())
        if normaliser <= 0:
            raise HistoryError("conditioned path must have positive probability")
        result = defaultdict(Fraction)
        for endpoint, mass in endpoints.items():
            for target, probability in rows[endpoint].items():
                result[target // slots] += mass * probability / normaliser
        return dict(result)

    pair_rows = {key: conditional(value) for key, value in pair_end.items()}
    order2_gap = Fraction(0)
    for (p0, p1, p2), endpoints in triple_end.items():
        observed, expected = conditional(endpoints), pair_rows[p1, p2]
        order2_gap = max(order2_gap, max(abs(observed.get(target, 0) - expected.get(target, 0)) for target in observed.keys() | expected.keys()))
    gap, witness = Fraction(0), None
    for p in range(pairs):
        for a in range(slots):
            for b in range(a + 1, slots):
                left, right = pair_rows[p ^ (1 << a), p], pair_rows[p ^ (1 << b), p]
                for target in left.keys() | right.keys():
                    difference = abs(left.get(target, 0) - right.get(target, 0))
                    gap = max(gap, difference)
                    if difference and witness is None:
                        witness = {
                            "current_pair_mask": p, "previous_mask_A": p ^ (1 << a), "previous_mask_B": p ^ (1 << b),
                            "next_mask": target, "probability_A": left.get(target, 0), "probability_B": right.get(target, 0),
                            "positive_past_mass_A": sum(pair_end[p ^ (1 << a), p].values()),
                            "positive_past_mass_B": sum(pair_end[p ^ (1 << b), p].values()),
                        }
    mean = sum(pi[state] * (state // slots).bit_count() for state in range(len(pi)))
    variance = sum(pi[state] * ((state // slots).bit_count() - mean) ** 2 for state in range(len(pi)))
    return {
        "projected_markov_order": 1 if gap == 0 else 2,
        "order1_witness_gap": gap, "order1_witness": witness, "order2_sufficiency_gap": order2_gap,
        "consistent_material_triples": len(triple_end), "positive_material_pairs": len(pair_end),
        "two_step_paths_enumerated": len(rows) * slots * slots,
        "two_step_backtrack_probability": backtrack,
        "edge_count_mean": mean, "edge_count_variance": variance,
        "edge_count_lag1_correlation": (lag1 - mean * mean) / variance,
        "edge_count_lag2_correlation": (lag2 - mean * mean) / variance,
    }


def analyse_controller(model: RoleController, *, independent_full=False, raw_triad_checks=True):
    with localcontext() as context:
        context.prec = PRECISION
        return _analyse_controller(model, independent_full, raw_triad_checks)


def _analyse_controller(model, independent_full, raw_triad_checks):
    slots, size = model.slots, model.state_count
    mask_count = 1 << slots
    rows = model.kernel()
    structure = role_orbits(model.n)
    quotient, quotient_gap = aggregate_quotient(rows, structure.members, structure.orbit_of)
    if quotient_gap:
        raise HistoryError("invalid dynamical S4 quotient")
    orbit_pi, quotient_classes, quotient_period = stationary(quotient)
    pi = [orbit_pi[structure.orbit_of[state]] / len(structure.members[structure.orbit_of[state]]) for state in range(size)]
    successors = [tuple(row.items()) for row in rows]
    full_components = strongly_connected_components(successors)
    full_periods = [period_of(component, successors) for component in full_components]
    if len(full_components) != 1:
        raise HistoryError(f"full chain has multiple communicating classes: {full_components}")
    marginal = [sum(pi[p * slots:(p + 1) * slots]) for p in range(mask_count)]
    history = [sum(pi[p * slots + h] for p in range(mask_count)) for h in range(slots)]
    representatives, material_groups, class_of = material_partition(model.n)
    material = project(marginal, model.n)
    uniform = [Fraction(1, mask_count)] * mask_count

    ku, kpi = [], []
    for p in range(mask_count):
        ku.append({p ^ (1 << e): sum(model.pair_probabilities(p, h)[e] for h in range(slots)) / slots for e in range(slots)})
        kpi.append({p ^ (1 << e): sum(pi[p * slots + h] * model.pair_probabilities(p, h)[e] for h in range(slots)) / marginal[p] for e in range(slots)})
    ku_quotient, ku_quotient_gap = aggregate_quotient(ku, material_groups, class_of)
    if ku_quotient_gap:
        raise HistoryError("uniform-history material class quotient invalid")
    ku_class_pi, ku_classes, ku_period = stationary(ku_quotient)
    ku_pi = [ku_class_pi[class_of[p]] / len(material_groups[class_of[p]]) for p in range(mask_count)]
    neutral_comparison = decomposition(marginal, uniform, model.n)
    ku_comparison = decomposition(marginal, ku_pi, model.n)

    pair_history = [pi[p * slots:(p + 1) * slots] for p in range(mask_count)]
    edge_history = [[Fraction(0)] * slots for _ in range(slots + 1)]
    class_history = [[Fraction(0)] * slots for _ in representatives]
    roles = {
        "P_R": [Fraction(0)] * 2, "P_A_h": [Fraction(0)] * (2 * (model.n - 2) + 1),
        "P_D_h": [Fraction(0)] * 2, "P_C_h": [Fraction(0)] * (model.n - 1),
        "P_R_A_h": [[Fraction(0)] * (2 * (model.n - 2) + 1) for _ in range(2)],
        "P_R_C_h": [[Fraction(0)] * (model.n - 1) for _ in range(2)],
        "P_D_h_C_h": [[Fraction(0)] * (model.n - 1) for _ in range(2)],
    }
    event_joint = [[Fraction(0)] * slots for _ in range(slots)]
    relation_direction = [[Fraction(0)] * 2 for _ in RELATIONS]
    for p in range(mask_count):
        for h in range(slots):
            mass = pi[p * slots + h]
            edge_history[p.bit_count()][h] += mass
            class_history[class_of[p]][h] += mass
            r, a, d, c = role_descriptors(p, h, model.n)
            for key, value in (("P_R", r), ("P_A_h", a), ("P_D_h", d), ("P_C_h", c)):
                roles[key][value] += mass
            roles["P_R_A_h"][r][a] += mass
            roles["P_R_C_h"][r][c] += mass
            roles["P_D_h_C_h"][d][c] += mass
            for e, probability in enumerate(model.pair_probabilities(p, h)):
                flow = mass * probability
                event_joint[h][e] += flow
                relation_direction[RELATIONS.index(slot_relation(model.n, e, h))][int(bool(p & (1 << e)))] += flow
    relation_probabilities = [sum(row) for row in relation_direction]
    temporal = projected_order_and_lags(model, pi, rows)
    temporal.update({
        "clock": "pair-event epoch", "repeat_probability": relation_probabilities[0],
        "adjacent_probability": relation_probabilities[1], "disjoint_probability": relation_probabilities[2],
        "consecutive_slot_MI": str(mutual_information(event_joint)), "consecutive_slot_joint": event_joint,
    })
    roles.update({
        "next_relation_order": RELATIONS, "next_direction_order": DIRECTIONS,
        "next_relation_probabilities": relation_probabilities, "next_relation_by_direction": relation_direction,
    })
    lumpability_gap = Fraction(0)
    for p in range(mask_count):
        for a in range(slots):
            for b in range(a + 1, slots):
                lumpability_gap = max(lumpability_gap, max(abs(x - y) for x, y in zip(model.pair_probabilities(p, a), model.pair_probabilities(p, b))))
    quotient_checks, closure_gap = [], Fraction(0)
    if raw_triad_checks:
        for p in ((0, 41, 63) if model.n == 4 else (0, mask_count - 1)):
            for h in (None, *range(slots)):
                direct = model.direct_next_pair_slots(p, h)
                expected = model.pair_probabilities(p, h)
                gap = max(abs(value - expected[e]) for row in direct for e, value in enumerate(row))
                closure_gap = max(closure_gap, gap)
                quotient_checks.append({"pair_mask": p, "history": h, "raw_triad_rows": len(direct), "gap": gap})
    full_db_gap = detailed_balance_gap(pi, rows)
    quotient_db_gap = detailed_balance_gap(orbit_pi, quotient)
    catalog = {
        "family": model.feature.family, "feature": model.feature_name, "m": model.multiplier,
        "history_dependent": model.feature.relation is not None,
        "current_state_dependent": model.feature.direction is not None,
        "S4_covariant": covariance_gap(model) == 0, "quotient_valid": quotient_gap == 0,
        "kernel_fingerprint": fingerprint(serial_rows(quotient)),
        "stationary_fingerprint": fingerprint(pi),
        "material_fingerprint": fingerprint(marginal),
        "projected_kernel_fingerprint": fingerprint(serial_rows(kpi)),
        "KU_kernel_fingerprint": fingerprint(serial_rows(ku)),
    }
    atlas = {
        "communicating_classes": len(full_components), "period": full_periods[0], "unique_stationary": len(full_components) == 1,
        "reversible": full_db_gap == 0, "quotient_reversible": quotient_db_gap == 0,
        "material_markov_projection_reversible": detailed_balance_gap(marginal, kpi) == 0,
        "I_pair_history": str(mutual_information(pair_history)),
        "I_edge_history": str(mutual_information(edge_history)), "I_class_history": str(mutual_information(class_history)),
        "neutral_JS_pairmask": neutral_comparison["pairmask"], "neutral_JS_graphclass": neutral_comparison["graphclass"],
        "neutral_JS_edgecount": neutral_comparison["edgecount"], "neutral_JS_shape_given_edge": neutral_comparison["shape_given_edge"],
        "neutral_JS_label_given_class": neutral_comparison["label_given_class"],
        "KU_JS_pairmask": ku_comparison["pairmask"], "KU_JS_graphclass": ku_comparison["graphclass"],
        "KU_JS_edgecount": ku_comparison["edgecount"], "KU_JS_shape": ku_comparison["shape_given_edge"],
        "projected_markov_order": temporal["projected_markov_order"], "strong_lumpability": lumpability_gap == 0,
    }
    validation = {
        "row_sum_gap": max(abs(sum(row.values()) - 1) for row in rows),
        "quotient_aggregation_gap": quotient_gap, "quotient_stationary_residual": balance_gap(orbit_pi, quotient),
        "stationary_residual": balance_gap(pi, rows), "stationary_normalisation_gap": abs(sum(pi) - 1),
        "stationary_S4_gap": max(abs(marginal[p] - marginal[group[0]]) for group in material_groups for p in group),
        "history_uniform_gap": max(abs(value - Fraction(1, slots)) for value in history),
        "edge_history_independence_gap": max(abs(edge_history[k][h] - material["edge_count"][k] * history[h]) for k in range(slots + 1) for h in range(slots)),
        "class_history_independence_gap": max(abs(class_history[k][h] - material["graph_class"][k] * history[h]) for k in range(len(representatives)) for h in range(slots)),
        "KU_quotient_gap": ku_quotient_gap, "KU_row_sum_gap": max(abs(sum(row.values()) - 1) for row in ku),
        "KU_stationary_residual": balance_gap(ku_pi, ku), "Kpi_stationary_residual": balance_gap(marginal, kpi),
        "Kpi_row_sum_gap": max(abs(sum(row.values()) - 1) for row in kpi),
        "full_vs_pair_quotient_gap": closure_gap,
        "neutral_information_chain_gap": neutral_comparison["chain_gap"], "KU_information_chain_gap": ku_comparison["chain_gap"],
        "labelled_remainder": neutral_comparison["label_given_class"],
        "order2_sufficiency_gap": temporal["order2_sufficiency_gap"],
        "order_lumpability_gap": abs(temporal["order1_witness_gap"] - lumpability_gap),
        "backtrack_repeat_gap": abs(temporal["two_step_backtrack_probability"] - temporal["repeat_probability"]),
        "stationary_form_dissolve_balance_gap": abs(sum(row[0] for row in relation_direction) - Fraction(1, 2)),
    }
    return {
        "catalog": catalog, "atlas": atlas, "roles": roles, "temporal": temporal, "validation": validation,
        "state_count": size, "orbit_count": len(structure.members), "quotient_classes": quotient_classes, "quotient_period": quotient_period,
        "quotient_kernel": serial_rows(quotient), "stationary_orbit_masses": orbit_pi, "stationary_joint": pi,
        "stationary_history": history, "material": material, "KU_kernel": serial_rows(ku), "KU_stationary_pair": ku_pi,
        "KU_classes": ku_classes, "KU_period": ku_period, "K_pi": serial_rows(kpi),
        "neutral_comparison": neutral_comparison, "KU_comparison": ku_comparison,
        "lumpability_gap": lumpability_gap, "full_augmented_detailed_balance_gap": full_db_gap,
        "quotient_detailed_balance_gap": quotient_db_gap,
        "quotient_currents": currents(orbit_pi, quotient) if quotient_db_gap else [],
        "one_way_augmented_transitions": sum(rows[target].get(source, 0) == 0 for source, row in enumerate(rows) for target in row),
        "raw_triad_checks": quotient_checks,
        "full_crosscheck": full_crosscheck(rows, pi, orbit_pi, model) if independent_full else {"performed": False},
        "precision_decimal_digits": PRECISION,
    }
