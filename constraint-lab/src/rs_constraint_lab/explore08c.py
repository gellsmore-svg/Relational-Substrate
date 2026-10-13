"""Generation 8C mechanism reading.

The calculations are exact constraint semantics, exact pair-slot weights,
the pair-event epoch kernel, graph classification, and finite enumeration.
They do not sample trajectories and they do not fit a parameter.

A float64 information value is a kernel result. A fraction identity is
stated only where the arithmetic is exact.
"""

from __future__ import annotations

import math
from collections import defaultdict
from fractions import Fraction

import numpy as np

from rs_constraint_lab.constraints import DISSOLVE, FORM, parse_expression
from rs_constraint_lab.explore08 import CLASS_NAMES, CLASS_OF_MASK, PAIR_SLOTS, source_masks
from rs_constraint_lab.explore08a import PALETTE, load_repair_palette
from rs_constraint_lab.explore08b import (
    N_FULL_STATES,
    N_PAIR_STATES,
    N_TRIAD_STATES,
    PAIR_SLOT_COUNT,
    _cmi_from_joint,
    balanced_slot_cmi,
    coarse_class_cmi,
    decompose_class_information,
    epoch_landing,
    kernel_row_error,
    pair_slot_laws,
    stationary_distribution,
    stationary_slot_cmi,
    stationary_state_weight,
    system_kernel,
)
from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.state import edges, relation_slots
from rs_constraint_lab.weights import alphabet_factors

EXPERIMENT_ID = "generation-008c-mechanistic-decomposition"
ANALYSIS_VERSION = "generation-008c-mechanism/v1"
ROUND_ID = "round-c0"
SINGLE_RULE_SYSTEMS = ("R01", "R02", "R04", "R06")
CONDITIONED_SYSTEMS = ("R01", "R02", "R04", "R05", "R06")
ZERO_SYSTEMS = ("R00", "R03", "R07")
MEMORY_SYSTEMS = ("R00", "R01", "R06")
MEMORY_CHECKPOINTS = (0, 1, 2, 4, 8, 16, 32, 64)
SOURCES = ("star", "path", "triangle")
GATE_SLOT_REFERENCE = 6
CLOSED_FORM_TOLERANCE = 1e-12
CMI_TOLERANCE = 1e-12
CHAIN_RULE_TOLERANCE = 1e-12
SYMMETRY_TOLERANCE = 1e-12
GATE_MEMORY_TOLERANCE = 1e-12
DRIFT_TOLERANCE = 1e-12
STATIONARY_DRIFT_TOLERANCE = 1e-9
KERNEL_ROW_TOLERANCE = 1e-12
CHECKPOINT_REPRODUCTION_TOLERANCE = 1e-8
# Published Generation 8B figures, used only as comparison targets.
PUBLISHED_BALANCED_CMI = {
    "suppress": 0.009748566529643855,
    "favour": 0.02336844477204944,
}
PUBLISHED_CHECKPOINT = {
    ("R06", "path"): {
        "class_information": 0.02798,
        "edge_count_information": 0.008801,
        "class_given_edge_count": 0.01918,
    },
    ("R01", "path"): {
        "class_information": 0.01023,
        "edge_count_information": 0.001393,
        "class_given_edge_count": 0.008838,
    },
}


class MechanismError(RuntimeError):
    """An exact identity or a frozen comparison missed its tolerance."""


def load_palette() -> list[dict]:
    systems = load_repair_palette()
    if [row["system_id"] for row in systems] != [item[0] for item in PALETTE]:
        raise MechanismError("A0 palette order drifted")
    return systems


def palette_by_id() -> dict[str, dict]:
    return {row["system_id"]: row for row in load_palette()}


def w4_factors() -> dict[str, Fraction]:
    return alphabet_factors("W4")


def parsed_rules(expressions: list[str]):
    return tuple(parse_expression(expression, 4, order=3) for expression in expressions)


def relation_name(slot: int) -> str:
    slot_tuple = relation_slots(4, 3)[slot]
    return "-".join(str(entity) for entity in slot_tuple)


def _uniform_six() -> tuple[Fraction, ...]:
    return tuple(Fraction(1, 6) for _ in range(PAIR_SLOT_COUNT))


def active_six(multiplier: Fraction, action: int) -> tuple[Fraction, ...]:
    total = multiplier + PAIR_SLOT_COUNT - 1
    return tuple(
        (multiplier if slot == action else Fraction(1)) / total for slot in range(PAIR_SLOT_COUNT)
    )


def js_equal(left: tuple[Fraction, ...] | tuple[float, ...], right: tuple[Fraction, ...] | tuple[float, ...]) -> float:
    """Equal-weight Jensen-Shannon divergence, in nats."""
    paired = [(float(a), float(b)) for a, b in zip(left, right, strict=True)]
    mixture = [(a + b) / 2.0 for a, b in paired]

    def kl(source) -> float:
        value = 0.0
        for probability, mixed in zip(source, mixture, strict=True):
            if probability > 0.0 and mixed > 0.0:
                value += probability * math.log(probability / mixed)
        return value

    return 0.5 * kl([item[0] for item in paired]) + 0.5 * kl([item[1] for item in paired])


def total_variation(left, right) -> float:
    return 0.5 * sum(abs(float(a) - float(b)) for a, b in zip(left, right, strict=True))


def kl_divergence(source, reference) -> float:
    value = 0.0
    for probability, base in zip(source, reference, strict=True):
        if float(probability) > 0.0:
            value += float(probability) * math.log(float(probability) / float(base))
    return value


def analytic_balanced_cmi(multiplier: Fraction) -> float:
    """``(1/2) JS(q_0, q_m)`` for one slot and one binary gate, admissible on half the masks."""
    return 0.5 * js_equal(_uniform_six(), active_six(multiplier, 0))


def _law_floats(law: tuple[Fraction, ...]) -> list[float]:
    return [float(item) for item in law]


def _pair_law_fraction(kernel, state: int) -> tuple[Fraction, ...]:
    weights = kernel.weights[state][:PAIR_SLOT_COUNT]
    total = sum(weights, Fraction(0))
    if total == 0:
        raise MechanismError(f"state {state} has no pair weight")
    return tuple(weight / total for weight in weights)


def _expected_pair_weights(rules, state: int) -> tuple[Fraction, ...]:
    factors = w4_factors()
    weights = [Fraction(1) for _ in range(PAIR_SLOT_COUNT)]
    for rule in rules:
        if rule.action >= PAIR_SLOT_COUNT:
            raise MechanismError("a pair-slot law saw a non-pair action")
        if rule.matches(state, rule.action):
            weights[rule.action] *= factors[rule.weight]
    return tuple(weights)


def rule_is_active(rule, state: int) -> bool:
    return bool(rule.matches(state, rule.action))


def _gate_bit(rule) -> tuple[int, int]:
    if len(rule.conditions) != 1:
        raise MechanismError("a single conditional rule must name one condition slot")
    slot, required = rule.conditions[0]
    if slot < PAIR_SLOTS:
        raise MechanismError("the condition is not a triad slot")
    return slot, required


def action_admissible(rule, state: int) -> bool:
    present = (state >> rule.action) & 1
    if rule.polarity == FORM:
        return not present
    if rule.polarity == DISSOLVE:
        return bool(present)
    raise MechanismError(f"polarity {rule.polarity} is not form or dissolve")


def gate_matches(rule, state: int) -> bool:
    slot, required = _gate_bit(rule)
    return ((state >> slot) & 1) == required


def single_rule_sufficient(expressions: list[str]) -> dict:
    """Minimal coordinates of one conditional pair rule, checked on all 1024 states."""
    rules = parsed_rules(expressions)
    if len(rules) != 1 or not rules[0].conditions:
        raise MechanismError("single-rule sufficiency requires one conditional pair rule")
    rule = rules[0]
    kernel = system_kernel(list(expressions))
    multiplier = w4_factors()[rule.weight]
    gate_slot, gate_required = _gate_bit(rule)
    groups: dict[tuple[int, int], set[tuple[Fraction, ...]]] = defaultdict(set)
    weight_gap = Fraction(0)
    inactive_uniform = True
    active_matches = True
    for state in range(N_FULL_STATES):
        admissible = int(action_admissible(rule, state))
        matched = int(gate_matches(rule, state))
        active = rule_is_active(rule, state)
        if active != (admissible == 1 and matched == 1):
            raise MechanismError("rule activity is not the conjunction of admissibility and the gate")
        expected = _expected_pair_weights(rules, state)
        actual = kernel.weights[state][:PAIR_SLOT_COUNT]
        for left, right in zip(expected, actual, strict=True):
            weight_gap = max(weight_gap, abs(left - right))
        law = _pair_law_fraction(kernel, state)
        groups[(admissible, matched)].add(law)
        if active:
            if law != active_six(multiplier, rule.action):
                active_matches = False
        elif law != _uniform_six():
            inactive_uniform = False
    raw_bit_groups: dict[tuple[int, int], set[tuple[Fraction, ...]]] = defaultdict(set)
    for state in range(N_FULL_STATES):
        action_bit = (state >> rule.action) & 1
        gate_bit = (state >> gate_slot) & 1
        raw_bit_groups[(action_bit, gate_bit)].add(_pair_law_fraction(kernel, state))
    distinct_within_conjunction = max(len(laws) for laws in groups.values())
    distinct_within_raw = max(len(laws) for laws in raw_bit_groups.values())
    other_bits_irrelevant = distinct_within_raw == 1 and distinct_within_conjunction == 1
    conjunction_values = {key: next(iter(laws)) for key, laws in groups.items()}
    active_key = (1, 1)
    inactive_keys = [key for key in conjunction_values if key != active_key]
    minimal_is_conjunction = (
        other_bits_irrelevant
        and conjunction_values[active_key] != _uniform_six()
        and all(conjunction_values[key] == _uniform_six() for key in inactive_keys)
    )
    return {
        "action_relation": relation_name(rule.action),
        "action_slot": rule.action,
        "active_state_count": sum(1 for state in range(N_FULL_STATES) if rule_is_active(rule, state)),
        "admissible_mask_count": sum(
            1 for mask in range(N_PAIR_STATES) if action_admissible(rule, mask)
        ),
        "condition_polarity": "present" if gate_required else "absent",
        "condition_relation": relation_name(gate_slot),
        "condition_slot": gate_slot,
        "direction": "form" if rule.polarity == FORM else "dissolve",
        "exact_weight_gap": f"{weight_gap.numerator}/{weight_gap.denominator}",
        "gate_half_within_admissible_mask": True,
        "inactive_is_uniform": inactive_uniform,
        "active_matches_closed_form": active_matches,
        "minimal_sufficient_coordinates": ["rule_active"] if minimal_is_conjunction else ["action_bit", "gate_bit"],
        "multiplier": f"{multiplier.numerator}/{multiplier.denominator}",
        "other_bits_irrelevant": other_bits_irrelevant,
        "raw_sufficient_coordinates": ["action_edge_bit", "condition_triad_bit"],
        "rule_active_is_conjunction": minimal_is_conjunction,
        "weight_name": rule.weight,
    }


def _count_gate_balance(rule) -> dict:
    gate_slot, required = _gate_bit(rule)
    admissible = [mask for mask in range(N_PAIR_STATES) if action_admissible(rule, mask)]
    if len(admissible) != N_PAIR_STATES // 2:
        raise MechanismError("action admissibility is not half of the pair masks")
    balanced = True
    for mask in admissible:
        matched = 0
        for triad in range(N_TRIAD_STATES):
            state = mask | (triad << PAIR_SLOTS)
            if ((state >> gate_slot) & 1) == required:
                matched += 1
        if matched != N_TRIAD_STATES // 2:
            balanced = False
    return {
        "admissible_masks": len(admissible),
        "gate_matched_triads_per_admissible_mask": N_TRIAD_STATES // 2,
        "gate_weight_is_one_half": balanced,
        "mask_weight_is_one_half": len(admissible) == N_PAIR_STATES // 2,
    }


def single_rule_local_law(system_id: str) -> dict:
    row = palette_by_id()[system_id]
    expressions = list(row["expressions"])
    coordinates = single_rule_sufficient(expressions)
    balance = _count_gate_balance(parsed_rules(expressions)[0])
    multiplier = w4_factors()[parsed_rules(expressions)[0].weight]
    kernel = system_kernel(expressions)
    enumerated = balanced_slot_cmi(pair_slot_laws(kernel)["conditional"])
    analytic = analytic_balanced_cmi(multiplier)
    inactive = _uniform_six()
    active = active_six(multiplier, parsed_rules(expressions)[0].action)
    return {
        "action_direction": coordinates["direction"],
        "analytic_balanced_CMI": analytic,
        "condition_polarity": coordinates["condition_polarity"],
        "enumerated_balanced_CMI": enumerated,
        "gap": abs(analytic - enumerated),
        "minimal_state_coordinates": coordinates["minimal_sufficient_coordinates"],
        "multiplier": coordinates["multiplier"],
        "q_active": _law_floats(active),
        "q_inactive": _law_floats(inactive),
        "raw_sufficient_coordinates": coordinates["raw_sufficient_coordinates"],
        "state_count_proof": {**coordinates, **balance},
        "system": system_id,
        "weighting_identity": "I = (1/2) JS(q_0, q_m), because half the masks are admissible and, on those masks, the gate splits the triads in half",
    }


def asymmetry_table() -> list[dict]:
    rows = []
    uniform = _uniform_six()
    for name, multiplier in (("strong_suppress", Fraction(1, 4)), ("strong_favour", Fraction(4))):
        active = active_six(multiplier, 0)
        rows.append(
            {
                "action_slot_probability": float(active[0]),
                "balanced_CMI": analytic_balanced_cmi(multiplier),
                "grade": name,
                "js_from_uniform": js_equal(uniform, active),
                "kl_active_from_uniform": kl_divergence(active, uniform),
                "kl_uniform_from_active": kl_divergence(uniform, active),
                "multiplier": f"{multiplier.numerator}/{multiplier.denominator}",
                "other_slot_probability": float(active[1]),
                "total_variation_from_uniform": total_variation(uniform, active),
            }
        )
    return rows


def r05_stratum_laws() -> dict:
    """Exact slot laws on the R05 mask strata. Slots 0 and 5, gate slot 6."""
    multiplier = w4_factors()["strong_suppress"]
    both_total = 2 * multiplier + 4
    both = []
    for slot in range(PAIR_SLOT_COUNT):
        weight = multiplier if slot in (0, 5) else Fraction(1)
        both.append(weight / both_total)
    return {
        "both_edges_gate_off": active_six(multiplier, 0),
        "both_edges_gate_on": tuple(both),
        "companion_absent_gate_off": _uniform_six(),
        "companion_absent_gate_on": active_six(multiplier, 5),
        "multiplier": multiplier,
    }


def r05_analytic_balanced_cmi() -> dict:
    laws = r05_stratum_laws()
    js_companion_absent = js_equal(laws["companion_absent_gate_off"], laws["companion_absent_gate_on"])
    js_both = js_equal(laws["both_edges_gate_off"], laws["both_edges_gate_on"])
    # 16/64 of masks are edge5-present and edge0-absent; 16/64 are both present.
    value = 0.25 * js_companion_absent + 0.25 * js_both
    return {
        "formula": "(1/4) JS(q_0, q_m on slot 5) + (1/4) JS(q_m on slot 0, q_both)",
        "js_both_edges": js_both,
        "js_companion_absent": js_companion_absent,
        "value": value,
    }


def r05_local_law() -> dict:
    row = palette_by_id()["R05"]
    expressions = list(row["expressions"])
    rules = parsed_rules(expressions)
    if len(rules) != 2:
        raise MechanismError("R05 is the two-rule composite")
    kernel = system_kernel(expressions)
    groups: dict[tuple[int, int, int], set[tuple[Fraction, ...]]] = defaultdict(set)
    weight_gap = Fraction(0)
    for state in range(N_FULL_STATES):
        edge0 = (state >> 0) & 1
        edge5 = (state >> 5) & 1
        gate = (state >> GATE_SLOT_REFERENCE) & 1
        expected = _expected_pair_weights(rules, state)
        actual = kernel.weights[state][:PAIR_SLOT_COUNT]
        for left, right in zip(expected, actual, strict=True):
            weight_gap = max(weight_gap, abs(left - right))
        groups[(edge0, edge5, gate)].add(_pair_law_fraction(kernel, state))
    constant = all(len(laws) == 1 for laws in groups.values())
    catalog = r05_stratum_laws()
    expected_groups = {
        (0, 0, 0): _uniform_six(),
        (0, 0, 1): _uniform_six(),
        (0, 1, 0): catalog["companion_absent_gate_off"],
        (0, 1, 1): catalog["companion_absent_gate_on"],
        (1, 0, 0): active_six(catalog["multiplier"], 0),
        (1, 0, 1): active_six(catalog["multiplier"], 0),
        (1, 1, 0): catalog["both_edges_gate_off"],
        (1, 1, 1): catalog["both_edges_gate_on"],
    }
    formula_gap = Fraction(0)
    for key, law in expected_groups.items():
        got = next(iter(groups[key]))
        for left, right in zip(law, got, strict=True):
            formula_gap = max(formula_gap, abs(left - right))
    enumerated = balanced_slot_cmi(pair_slot_laws(kernel)["conditional"])
    analytic = r05_analytic_balanced_cmi()
    return {
        "action_direction": "dissolve",
        "analytic_balanced_CMI": analytic["value"],
        "condition_polarity": "unconditional and present",
        "enumerated_balanced_CMI": enumerated,
        "formula": analytic["formula"],
        "formula_fraction_gap": f"{formula_gap.numerator}/{formula_gap.denominator}",
        "gap": abs(analytic["value"] - enumerated),
        "groups_constant": constant,
        "js_both_edges": analytic["js_both_edges"],
        "js_companion_absent": analytic["js_companion_absent"],
        "minimal_state_coordinates": [
            "unconditional_action_edge_0_1",
            "conditional_action_edge_2_3",
            "condition_triad_0_1_2",
        ],
        "multiplier": "1/4;1/4",
        "stratum_count": len(groups),
        "system": "R05",
        "weight_fraction_gap": f"{weight_gap.numerator}/{weight_gap.denominator}",
    }


def _degrees(mask: int) -> list[int]:
    degree = [0, 0, 0, 0]
    for slot, (left, right) in enumerate(edges(4)):
        if (mask >> slot) & 1:
            degree[left] += 1
            degree[right] += 1
    return degree


def _distance(mask: int, start: int, end: int) -> int | None:
    if start == end:
        return 0
    seen = {start}
    queue = [(start, 0)]
    while queue:
        vertex, depth = queue.pop(0)
        for slot, (left, right) in enumerate(edges(4)):
            if not ((mask >> slot) & 1):
                continue
            nxt = right if vertex == left else left if vertex == right else None
            if nxt is None or nxt in seen:
                continue
            if nxt == end:
                return depth + 1
            seen.add(nxt)
            queue.append((nxt, depth + 1))
    return None


def slot_topology(source: str, mask: int, slot: int) -> str:
    present = (mask >> slot) & 1
    left, right = edges(4)[slot]
    degree = _degrees(mask)
    if source == "star":
        return "spoke" if present else "rim"
    if source == "triangle":
        return "triangle_edge" if present else "pendant"
    if source != "path":
        raise MechanismError(f"unknown source {source}")
    if present:
        if degree[left] == 1 or degree[right] == 1:
            return "path_end"
        return "path_middle"
    distance = _distance(mask, left, right)
    if distance == 2:
        return "path_short_chord"
    if distance == 3:
        return "path_long_chord"
    raise MechanismError(f"path slot {slot} has distance {distance}")


def topology_atlas() -> list[dict]:
    masks = source_masks()
    table = pair_classes()
    rows = []
    for source in SOURCES:
        mask = masks[source]
        for slot in range(PAIR_SLOT_COUNT):
            present = (mask >> slot) & 1
            result = mask ^ (1 << slot)
            canonical = table.class_of[result]
            rows.append(
                {
                    "event_direction": "dissolve" if present else "form",
                    "pair_relation": relation_name(slot),
                    "pre_event_bit": int(present),
                    "result_edge_count": int(result.bit_count()),
                    "result_graph_class": table.name_of[result],
                    "result_mask": result,
                    "slot": slot,
                    "slot_topology_category": slot_topology(source, mask, slot),
                    "source_graph": source,
                    "source_mask": mask,
                    "canonical_result_mask": int(canonical),
                }
            )
    return rows


def topology_shape_summary(rows: list[dict] | None = None) -> dict:
    rows = topology_atlas() if rows is None else rows
    summary = {}
    for source in SOURCES:
        by_count: dict[int, set[str]] = defaultdict(set)
        categories: dict[str, int] = defaultdict(int)
        for row in rows:
            if row["source_graph"] != source:
                continue
            by_count[row["result_edge_count"]].add(row["result_graph_class"])
            categories[row["slot_topology_category"]] += 1
        summary[source] = {
            "categories": dict(categories),
            "classes_by_edge_count": {str(count): sorted(names) for count, names in sorted(by_count.items())},
            "one_class_per_edge_count": bool(by_count) and all(len(names) == 1 for names in by_count.values()),
        }
    return summary


def _system_expressions(system_id: str) -> list[str]:
    return list(palette_by_id()[system_id]["expressions"])


def _kernel(system_id: str):
    return system_kernel(_system_expressions(system_id))


def action_on_source(system_id: str) -> list[dict]:
    """Where each conditional action slot sits on each canonical source."""
    expressions = _system_expressions(system_id)
    rules = [rule for rule in parsed_rules(expressions) if rule.conditions and rule.action < PAIR_SLOT_COUNT]
    masks = source_masks()
    rows = []
    for rule in rules:
        for source, mask in masks.items():
            present = (mask >> rule.action) & 1
            active_possible = action_admissible(rule, mask)
            rows.append(
                {
                    "action_admissible_on_source": active_possible,
                    "action_relation": relation_name(rule.action),
                    "event_direction_if_selected": "dissolve" if present else "form",
                    "pre_event_bit": int(present),
                    "rule_polarity": "form" if rule.polarity == FORM else "dissolve",
                    "slot_topology_category": slot_topology(source, mask, rule.action),
                    "source_graph": source,
                    "system": system_id,
                }
            )
    return rows


def _class_conditional_from_landing(landing: np.ndarray, mask: int) -> np.ndarray:
    conditional = np.zeros((N_TRIAD_STATES, 11), dtype=np.float64)
    pair_class = np.asarray(CLASS_OF_MASK, dtype=np.int32)
    for triad in range(N_TRIAD_STATES):
        state = mask | (triad << PAIR_SLOTS)
        row = landing[state]
        for slot_class, mass in zip(pair_class, _mask_mass(row), strict=True):
            conditional[triad, slot_class] += mass
    return conditional


def _mask_mass(row: np.ndarray) -> np.ndarray:
    reshaped = row.reshape(N_TRIAD_STATES, N_PAIR_STATES)
    return reshaped.sum(axis=0)


def _immediate_class_conditional(kernel, mask: int) -> np.ndarray:
    """Class law if the first full event were forced to be a pair event at the initial state."""
    laws = pair_slot_laws(kernel)["conditional"]
    pair_class = np.asarray(CLASS_OF_MASK, dtype=np.int32)
    conditional = np.zeros((N_TRIAD_STATES, 11), dtype=np.float64)
    for triad in range(N_TRIAD_STATES):
        state = mask | (triad << PAIR_SLOTS)
        for slot in range(PAIR_SLOT_COUNT):
            nxt = mask ^ (1 << slot)
            conditional[triad, pair_class[nxt]] += laws[state, slot]
    return conditional


def checkpoint_source(system_id: str, source: str, landing: np.ndarray | None = None) -> dict:
    kernel = _kernel(system_id)
    if landing is None:
        landing, defect = epoch_landing(kernel, solver="block")
    else:
        defect = None
    mask = source_masks()[source]
    epoch = _class_conditional_from_landing(landing, mask)
    immediate = _immediate_class_conditional(kernel, mask)
    epoch_parts = decompose_class_information(epoch)
    immediate_parts = decompose_class_information(immediate)
    gate_slot = _primary_gate_slot(system_id)
    rows = []
    pair_class = np.asarray(CLASS_OF_MASK, dtype=np.int32)
    edge_of_class = []
    for name in CLASS_NAMES:
        edge_of_class.append(int(name.split("-")[0][1:]))
    for gate in (0, 1):
        members = [triad for triad in range(N_TRIAD_STATES) if ((triad >> (gate_slot - PAIR_SLOTS)) & 1) == gate]
        mixed = epoch[members].mean(axis=0)
        for class_index, probability in enumerate(mixed):
            if probability <= 0.0:
                continue
            rows.append(
                {
                    "destination_class": CLASS_NAMES[class_index],
                    "destination_edge_count": edge_of_class[class_index],
                    "initial_gate": gate,
                    "probability": float(probability),
                    "source": source,
                    "system": system_id,
                }
            )
    return {
        "epoch_defect": defect,
        "epoch_mi": epoch_parts,
        "immediate_mi": immediate_parts,
        "kernel_row_error": kernel_row_error(landing),
        "rows": rows,
        "source": source,
        "system": system_id,
        "total_variation_epoch_vs_immediate": 0.5 * float(np.abs(epoch.mean(axis=0) - immediate.mean(axis=0)).sum()),
    }


def _primary_gate_slot(system_id: str) -> int:
    rules = parsed_rules(_system_expressions(system_id))
    for rule in rules:
        if rule.conditions:
            slot, _required = rule.conditions[0]
            if slot >= PAIR_SLOTS:
                return slot
    return GATE_SLOT_REFERENCE


def _triad_block(kernel, mask: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return Q, absorption probability, and conditional slot law for one pair mask."""
    q_matrix = np.zeros((N_TRIAD_STATES, N_TRIAD_STATES), dtype=np.float64)
    absorb = np.zeros(N_TRIAD_STATES, dtype=np.float64)
    slots = np.zeros((N_TRIAD_STATES, PAIR_SLOT_COUNT), dtype=np.float64)
    for triad in range(N_TRIAD_STATES):
        state = mask | (triad << PAIR_SLOTS)
        weights = [float(weight) for weight in kernel.weights[state]]
        total = sum(weights)
        pair = weights[:PAIR_SLOT_COUNT]
        pair_total = sum(pair)
        absorb[triad] = pair_total / total
        slots[triad] = [weight / pair_total for weight in pair]
        for bit in range(4):
            probability = weights[PAIR_SLOTS + bit] / total
            q_matrix[triad, triad ^ (1 << bit)] += probability
    return q_matrix, absorb, slots


def excursion_report(system_id: str, source: str) -> dict:
    kernel = _kernel(system_id)
    mask = source_masks()[source]
    q_matrix, absorb, slots = _triad_block(kernel, mask)
    gate_shift = _primary_gate_slot(system_id) - PAIR_SLOTS
    length_counts = np.zeros(64, dtype=np.float64)
    pre_equal = 0.0
    ever_flipped = 0.0
    slot_by_gate = np.zeros((2, PAIR_SLOT_COUNT), dtype=np.float64)
    gate_mass = np.zeros(2, dtype=np.float64)
    residual = 0.0
    for triad0 in range(N_TRIAD_STATES):
        remaining = np.zeros((N_TRIAD_STATES, 2), dtype=np.float64)
        remaining[triad0, 0] = 1.0
        initial_gate = (triad0 >> gate_shift) & 1
        for length in range(64):
            flat = remaining.sum(axis=1)
            taken = flat * absorb
            length_counts[length] += taken.sum() / N_TRIAD_STATES
            for triad in range(N_TRIAD_STATES):
                if taken[triad] == 0.0:
                    continue
                current_gate = (triad >> gate_shift) & 1
                if current_gate == initial_gate:
                    pre_equal += taken[triad] / N_TRIAD_STATES
                ever_flipped += remaining[triad, 1] * absorb[triad] / N_TRIAD_STATES
                slot_by_gate[initial_gate] += (taken[triad] / N_TRIAD_STATES) * slots[triad]
                gate_mass[initial_gate] += taken[triad] / N_TRIAD_STATES
            nxt = np.zeros_like(remaining)
            for triad in range(N_TRIAD_STATES):
                for flag in range(2):
                    mass = remaining[triad, flag]
                    if mass == 0.0:
                        continue
                    for bit in range(4):
                        probability = q_matrix[triad, triad ^ (1 << bit)]
                        if probability == 0.0:
                            continue
                        new_flag = 1 if flag or bit == gate_shift else 0
                        nxt[triad ^ (1 << bit), new_flag] += mass * probability
            remaining = nxt
            if float(remaining.sum()) < 1e-18:
                break
        residual += float(remaining.sum()) / N_TRIAD_STATES
    for gate in range(2):
        if gate_mass[gate] > 0.0:
            slot_by_gate[gate] /= gate_mass[gate]
    return {
        "excursion_length": [float(value) for value in length_counts],
        "excursion_length_mass": float(length_counts.sum()),
        "mean_excursion_length": float(sum(index * value for index, value in enumerate(length_counts))),
        "probability_gate_flips_at_least_once": float(ever_flipped),
        "probability_pre_pair_gate_equals_initial": float(pre_equal),
        "probability_pair_event_is_immediate": float(length_counts[0]),
        "residual_unabsorbed": residual,
        "selected_slot_given_initial_gate": {
            "0": [float(value) for value in slot_by_gate[0]],
            "1": [float(value) for value in slot_by_gate[1]],
        },
        "source": source,
        "system": system_id,
    }


def _mutual_from_joint(joint: np.ndarray) -> float:
    total = float(joint.sum())
    if total <= 0.0:
        return 0.0
    probability = joint / total
    left = probability.sum(axis=1)
    right = probability.sum(axis=0)
    information = 0.0
    for i in range(probability.shape[0]):
        for j in range(probability.shape[1]):
            cell = probability[i, j]
            if cell <= 0.0 or left[i] <= 0.0 or right[j] <= 0.0:
                continue
            information += cell * math.log(cell / (left[i] * right[j]))
    return float(information)


def gate_memory_curve(system_id: str, source: str, landing: np.ndarray | None = None) -> list[dict]:
    kernel = _kernel(system_id)
    if landing is None:
        landing, _defect = epoch_landing(kernel, solver="block")
    mask = source_masks()[source]
    gate_shift = _primary_gate_slot(system_id) - PAIR_SLOTS
    rows = np.zeros((N_TRIAD_STATES, N_FULL_STATES), dtype=np.float64)
    for triad in range(N_TRIAD_STATES):
        rows[triad, mask | (triad << PAIR_SLOTS)] = 1.0
    wanted = set(MEMORY_CHECKPOINTS)
    records = []
    for step in range(0, max(MEMORY_CHECKPOINTS) + 1):
        if step in wanted:
            records.append(_memory_record(system_id, source, step, rows, gate_shift))
        if step != max(MEMORY_CHECKPOINTS):
            rows = rows @ landing
    return records


def _memory_record(system_id: str, source: str, step: int, rows: np.ndarray, gate_shift: int) -> dict:
    gate_joint = np.zeros((2, 2), dtype=np.float64)
    triad_joint = np.zeros((N_TRIAD_STATES, N_TRIAD_STATES), dtype=np.float64)
    gate_mask = np.zeros((2, N_PAIR_STATES), dtype=np.float64)
    triad_mask = np.zeros((N_TRIAD_STATES, N_PAIR_STATES), dtype=np.float64)
    states = np.arange(N_FULL_STATES)
    current_gate = (states >> (PAIR_SLOTS + gate_shift)) & 1
    current_triad = states >> PAIR_SLOTS
    current_mask = states & (N_PAIR_STATES - 1)
    for triad in range(N_TRIAD_STATES):
        weight = rows[triad] / N_TRIAD_STATES
        initial_gate = (triad >> gate_shift) & 1
        gate_joint[initial_gate] += np.bincount(current_gate, weights=weight, minlength=2)
        triad_joint[triad] += np.bincount(current_triad, weights=weight, minlength=N_TRIAD_STATES)
        gate_mask[initial_gate] += np.bincount(current_mask, weights=weight, minlength=N_PAIR_STATES)
        triad_mask[triad] += np.bincount(current_mask, weights=weight, minlength=N_PAIR_STATES)
    equal = float(gate_joint[0, 0] + gate_joint[1, 1])
    return {
        "I_initial_full_triad_current_full_triad": _mutual_from_joint(triad_joint),
        "I_initial_full_triad_current_pair_mask": _mutual_from_joint(triad_mask),
        "I_initial_gate_current_gate": _mutual_from_joint(gate_joint),
        "I_initial_gate_current_pair_mask": _mutual_from_joint(gate_mask),
        "checkpoint": step,
        "distribution_mass": float(rows.sum() / N_TRIAD_STATES),
        "gate_pair_gap": _mutual_from_joint(triad_mask) - _mutual_from_joint(gate_mask),
        "Pr_current_gate_equals_initial_gate": equal,
        "source": source,
        "system": system_id,
    }


def _balanced_joint(law: np.ndarray) -> np.ndarray:
    joint = np.zeros((N_TRIAD_STATES, PAIR_SLOT_COUNT, N_PAIR_STATES), dtype=np.float64)
    for triad in range(N_TRIAD_STATES):
        for mask in range(N_PAIR_STATES):
            state = mask | (triad << PAIR_SLOTS)
            joint[triad, :, mask] = law[state] / N_FULL_STATES
    return joint


def _stationary_joint(pi: np.ndarray, full_event: np.ndarray) -> np.ndarray:
    joint = np.zeros((N_TRIAD_STATES, PAIR_SLOT_COUNT, N_PAIR_STATES), dtype=np.float64)
    for state in range(N_FULL_STATES):
        mask = state & (N_PAIR_STATES - 1)
        triad = state >> PAIR_SLOTS
        joint[triad, :, mask] += pi[state] * full_event[state]
    return joint


def _cmi_contribution_by_mask(joint: np.ndarray) -> np.ndarray:
    total = float(joint.sum())
    probability = joint / total
    conditioner = probability.sum(axis=(0, 1))
    triad_conditioner = probability.sum(axis=1)
    outcome_conditioner = probability.sum(axis=0)
    contribution = np.zeros(joint.shape[2], dtype=np.float64)
    for triad in range(probability.shape[0]):
        for outcome in range(probability.shape[1]):
            for mask in range(probability.shape[2]):
                cell = probability[triad, outcome, mask]
                if cell <= 0.0:
                    continue
                contribution[mask] += cell * math.log(
                    (cell * conditioner[mask])
                    / (triad_conditioner[triad, mask] * outcome_conditioner[outcome, mask])
                )
    return contribution


def contribution_atlas(system_id: str) -> dict:
    expressions = _system_expressions(system_id)
    rules = parsed_rules(expressions)
    kernel = _kernel(system_id)
    laws = pair_slot_laws(kernel)
    stationary = stationary_distribution(kernel)
    balanced_joint = _balanced_joint(laws["conditional"])
    stationary_joint = _stationary_joint(stationary["pi"], laws["full_event"])
    balanced_parts = _cmi_contribution_by_mask(balanced_joint)
    stationary_parts = _cmi_contribution_by_mask(stationary_joint)
    weight = stationary_state_weight(stationary["pi"], laws["full_event"])
    mask_weight = np.zeros(N_PAIR_STATES, dtype=np.float64)
    for state in range(N_FULL_STATES):
        mask_weight[state & (N_PAIR_STATES - 1)] += weight[state]
    mask_weight /= mask_weight.sum()
    conditional_rules = [rule for rule in rules if rule.conditions]
    rows = []
    for mask in range(N_PAIR_STATES):
        action_state = None
        active_mask = False
        if len(conditional_rules) == 1:
            rule = conditional_rules[0]
            action_state = int(action_admissible(rule, mask))
            active_mask = bool(action_state)
        elif system_id == "R05":
            action_state = (mask >> 5) & 1
            active_mask = bool(action_state)
        rows.append(
            {
                "action_match_state": action_state,
                "balanced_CMI_contribution": float(balanced_parts[mask]),
                "edge_count": int(mask.bit_count()),
                "graph_class": CLASS_NAMES[CLASS_OF_MASK[mask]],
                "pair_mask": mask,
                "rule_active_mask": active_mask,
                "stationary_CMI_contribution": float(stationary_parts[mask]),
                "stationary_pair_event_weight": float(mask_weight[mask]),
                "system": system_id,
            }
        )
    enumerated_balanced = balanced_slot_cmi(laws["conditional"])
    enumerated_stationary = stationary_slot_cmi(kernel, stationary["pi"], laws["full_event"])
    active_values = [row["balanced_CMI_contribution"] for row in rows if row["rule_active_mask"]]
    inactive_values = [row["balanced_CMI_contribution"] for row in rows if not row["rule_active_mask"]]
    return {
        "active_balanced_contribution_span": (
            max(active_values) - min(active_values) if active_values else 0.0
        ),
        "balanced_cmi": float(balanced_parts.sum()),
        "enumerated_balanced_cmi": enumerated_balanced,
        "inactive_balanced_abs_max": max((abs(value) for value in inactive_values), default=0.0),
        "rows": rows,
        "stationary_cmi": float(stationary_parts.sum()),
        "stationary_enumerated_cmi": enumerated_stationary,
        "stationary_residual": stationary["residual"],
        "sum_gap_balanced": abs(float(balanced_parts.sum()) - enumerated_balanced),
        "sum_gap_stationary": abs(float(stationary_parts.sum()) - enumerated_stationary),
        "system": system_id,
        "zero_contribution_mask_count": sum(1 for row in rows if abs(row["balanced_CMI_contribution"]) <= 1e-15),
    }


def projection_report(system_id: str) -> dict:
    kernel = _kernel(system_id)
    laws = pair_slot_laws(kernel)
    stationary = stationary_distribution(kernel)
    full = stationary_slot_cmi(kernel, stationary["pi"], laws["full_event"])
    weight = stationary_state_weight(stationary["pi"], laws["full_event"])
    coarse = coarse_class_cmi(weight, laws["conditional"])
    retained = coarse["next_pair_slot_given_pair_class"]
    joint = _stationary_joint(stationary["pi"], laws["full_event"])
    pair_class = np.asarray(CLASS_OF_MASK, dtype=np.int32)
    class_rows = []
    loss_sum = 0.0
    for class_index, name in enumerate(CLASS_NAMES):
        members = np.flatnonzero(pair_class == class_index)
        member_joint = joint[:, :, members]
        mass = float(member_joint.sum())
        if mass <= 0.0:
            continue
        within = _cmi_from_joint(member_joint)
        collapsed = member_joint.sum(axis=2, keepdims=True)
        # One conditioner, so the conditional MI is ordinary MI of triad and slot.
        flat = np.zeros((N_TRIAD_STATES, PAIR_SLOT_COUNT), dtype=np.float64)
        flat[:, :] = collapsed[:, :, 0]
        at_class = _mutual_from_joint(flat)
        loss = mass * (within - at_class) / float(joint.sum())
        # within is already computed on the conditional distribution of this class,
        # so mass * within / total is the weighted piece. _cmi_from_joint renormalises,
        # and _mutual_from_joint renormalises, so both are conditional informations.
        weighted_within = (mass / float(joint.sum())) * within
        weighted_class = (mass / float(joint.sum())) * at_class
        loss = weighted_within - weighted_class
        loss_sum += loss
        class_rows.append(
            {
                "class_index": class_index,
                "graph_class": name,
                "labelled_cmi": float(within),
                "class_cmi": float(at_class),
                "loss": float(loss),
                "mask_count": int(len(members)),
                "masks": [int(mask) for mask in members],
                "stationary_mass": mass / float(joint.sum()),
            }
        )
    fraction = retained / full if full > 1e-15 else None
    return {
        "class_cmi": retained,
        "class_rows": class_rows,
        "discarded": full - retained,
        "full_mask_cmi": full,
        "loss_sum": loss_sum,
        "loss_sum_gap": loss_sum - (full - retained),
        "next_class_given_class": coarse["next_pair_class_given_pair_class"],
        "retained_fraction": fraction,
        "system": system_id,
    }


def _delta(mask: int, law: tuple[Fraction, ...] | np.ndarray) -> float:
    total = 0.0
    for slot in range(PAIR_SLOT_COUNT):
        sign = -1.0 if (mask >> slot) & 1 else 1.0
        total += float(law[slot]) * sign
    return total


def closed_form_induced(mask: int, rules, gate: int) -> Fraction | None:
    """One-slot rule-induced edge drift. None when more than one rule is present.

    On an admissible dissolve, suppress contributes ``(6-k)/21`` and favour
    contributes ``(k-6)/9``. On an admissible form, suppress contributes
    ``-k/21``. The gate must match. Every other stratum is zero.
    """
    if len(rules) != 1:
        return None
    rule = rules[0]
    if rule.conditions:
        _slot, required = _gate_bit(rule)
        if gate != required or not action_admissible(rule, mask):
            return Fraction(0)
    elif not action_admissible(rule, mask):
        return Fraction(0)
    edge_count = mask.bit_count()
    if rule.polarity == DISSOLVE and rule.weight == "strong_suppress":
        return Fraction(6 - edge_count, 21)
    if rule.polarity == DISSOLVE and rule.weight == "strong_favour":
        return Fraction(edge_count - 6, 9)
    if rule.polarity == FORM and rule.weight == "strong_suppress":
        return Fraction(-edge_count, 21)
    if rule.polarity == FORM and rule.weight == "strong_favour":
        return Fraction(edge_count, 9)
    return None


def drift_report(system_id: str) -> dict:
    expressions = _system_expressions(system_id)
    rules = parsed_rules(expressions)
    kernel = _kernel(system_id)
    laws = pair_slot_laws(kernel)
    stationary = stationary_distribution(kernel)
    weight = stationary_state_weight(stationary["pi"], laws["full_event"])
    gate_slot = _primary_gate_slot(system_id)
    rows = []
    stationary_drift = 0.0
    weight_total = float(weight.sum())
    direct_gap = 0.0
    closed_form_gap = 0.0
    closed_form_defined = True
    balanced_baseline = 0.0
    balanced_induced = 0.0
    balanced_actual = 0.0
    group_count = 0
    for mask in range(N_PAIR_STATES):
        for gate in (0, 1):
            triad = 0 if gate == 0 else (1 << (gate_slot - PAIR_SLOTS))
            state = mask | (triad << PAIR_SLOTS)
            conditional = laws["conditional"][state]
            baseline = _delta(mask, _uniform_six())
            actual = _delta(mask, conditional)
            induced = actual - baseline
            formula = closed_form_induced(mask, rules, gate)
            if formula is None:
                closed_form_defined = False
            else:
                closed_form_gap = max(closed_form_gap, abs(float(formula) - induced))
            slot_mass = 0.0
            for slot in range(PAIR_SLOT_COUNT):
                sign = -1.0 if (mask >> slot) & 1 else 1.0
                slot_mass += float(conditional[slot]) * sign
            direct_gap = max(direct_gap, abs(slot_mass - actual))
            gate_weight = 0.0
            for triad_index in range(N_TRIAD_STATES):
                if ((triad_index >> (gate_slot - PAIR_SLOTS)) & 1) != gate:
                    continue
                gate_weight += float(weight[mask | (triad_index << PAIR_SLOTS)])
            stationary_drift += (gate_weight / weight_total) * actual
            balanced_baseline += baseline
            balanced_induced += induced
            balanced_actual += actual
            group_count += 1
            rows.append(
                {
                    "baseline_delta_edges": baseline,
                    "closed_form_induced": None if formula is None else float(formula),
                    "edge_count": int(mask.bit_count()),
                    "expected_delta_edges": actual,
                    "pair_mask": mask,
                    "rule_induced_delta": induced,
                    "stationary_weight": gate_weight / weight_total,
                    "system": system_id,
                    "triad_gate": gate,
                }
            )
    per_state = 0.0
    for state in range(N_FULL_STATES):
        mask = state & (N_PAIR_STATES - 1)
        per_state += (float(weight[state]) / weight_total) * _delta(mask, laws["conditional"][state])
    active_sign = _active_drift_sign(rules)
    return {
        "active_rule_induced_sign": active_sign,
        "balanced_baseline_drift": balanced_baseline / group_count,
        "balanced_expected_drift": balanced_actual / group_count,
        "balanced_rule_induced_drift": balanced_induced / group_count,
        "closed_form_defined": closed_form_defined,
        "closed_form_gap": closed_form_gap,
        "direct_identity_gap": direct_gap,
        "per_state_drift_gap": abs(per_state - stationary_drift),
        "rows": rows,
        "stationary_expected_drift": stationary_drift,
        "stationary_residual": stationary["residual"],
        "system": system_id,
    }


def _active_drift_sign(rules) -> str | None:
    """Sign of the rule-induced drift when a dissolve or form rule is the only active weight."""
    if not rules:
        return None
    if len(rules) == 1 and not rules[0].conditions:
        if rules[0].polarity == DISSOLVE and rules[0].weight == "strong_suppress":
            return "positive"
        if rules[0].polarity == DISSOLVE and rules[0].weight == "strong_favour":
            return "negative"
    if len(rules) == 1 and rules[0].conditions:
        if rules[0].polarity == DISSOLVE and rules[0].weight == "strong_suppress":
            return "positive"
        if rules[0].polarity == DISSOLVE and rules[0].weight == "strong_favour":
            return "negative"
        if rules[0].polarity == FORM and rules[0].weight == "strong_suppress":
            return "negative"
    return None


def conjugate_probability_gap(source_id: str, image_id: str, images: list[int]) -> float:
    """Largest absolute probability gap after relabelling source states by ``images``."""
    left = _kernel(source_id)
    right = _kernel(image_id)
    gap = 0.0
    for state in range(N_FULL_STATES):
        image = images[state]
        left_row = {target: float(prob) for target, prob in left.successors[state]}
        right_row = {target: float(prob) for target, prob in right.successors[image]}
        keys = set(left_row) | {pre for pre in range(N_FULL_STATES) if images[pre] in right_row}
        for target, probability in left_row.items():
            mapped = images[target]
            gap = max(gap, abs(probability - right_row.get(mapped, 0.0)))
        for target, probability in right_row.items():
            # every right edge should be the image of a left edge
            if probability > 0.0 and target not in {images[item] for item in left_row}:
                gap = max(gap, probability)
    return gap


def r02_to_r01_images() -> list[int]:
    """Flip every bit except the gate bit. This conjugates form|absent to dissolve|absent on the same slots."""
    mask = ((1 << 10) - 1) ^ (1 << GATE_SLOT_REFERENCE)
    return [state ^ mask for state in range(N_FULL_STATES)]


def r04_to_r01_images() -> list[int]:
    """Flip the gate bit, then swap pair slots 0 and 5."""
    images = []
    for state in range(N_FULL_STATES):
        flipped = state ^ (1 << GATE_SLOT_REFERENCE)
        bit0 = (flipped >> 0) & 1
        bit5 = (flipped >> 5) & 1
        cleared = flipped & ~((1 << 0) | (1 << 5))
        images.append(cleared | (bit5 << 0) | (bit0 << 5))
    return images


def _map_preserves_pair_class(images: list[int]) -> bool:
    for state in range(N_FULL_STATES):
        mask = state & (N_PAIR_STATES - 1)
        image_mask = images[state] & (N_PAIR_STATES - 1)
        if CLASS_OF_MASK[mask] != CLASS_OF_MASK[image_mask]:
            return False
    return True


def _class_image_example(images: list[int]) -> dict:
    """One pair mask whose image is a different isomorphism class."""
    for mask in range(N_PAIR_STATES):
        image_mask = images[mask] & (N_PAIR_STATES - 1)
        if CLASS_OF_MASK[mask] != CLASS_OF_MASK[image_mask]:
            return {
                "image_class": CLASS_NAMES[CLASS_OF_MASK[image_mask]],
                "image_mask": image_mask,
                "source_class": CLASS_NAMES[CLASS_OF_MASK[mask]],
                "source_mask": mask,
            }
    return {}


def symmetry_report() -> dict:
    r02_images = r02_to_r01_images()
    r04_images = r04_to_r01_images()
    r02_gap = conjugate_probability_gap("R02", "R01", r02_images)
    r04_gap = conjugate_probability_gap("R04", "R01", r04_images)
    r02_preserves = _map_preserves_pair_class(r02_images)
    r04_preserves = _map_preserves_pair_class(r04_images)
    return {
        "preserves_graph_class": r02_preserves and r04_preserves,
        "preserves_labelled_slot_cmi": r02_gap <= SYMMETRY_TOLERANCE and r04_gap <= SYMMETRY_TOLERANCE,
        "r02_class_image_example": _class_image_example(r02_images),
        "r02_map": "complement every relation bit except the condition triad 0-1-2",
        "r02_preserves_pair_class": r02_preserves,
        "r02_to_r01_transition_gap": r02_gap,
        "r04_class_image_example": _class_image_example(r04_images),
        "r04_map": "flip condition-triad bit 0-1-2, then exchange pair slots 0-1 and 2-3",
        "r04_preserves_pair_class": r04_preserves,
        "r04_to_r01_transition_gap": r04_gap,
    }


def local_law_table() -> list[dict]:
    rows = [single_rule_local_law(system_id) for system_id in SINGLE_RULE_SYSTEMS]
    rows.append(r05_local_law())
    return rows


def published_checkpoint_targets() -> dict:
    """Rounded Generation 8B comparison targets. Not inputs to the epoch calculation."""
    return PUBLISHED_CHECKPOINT


def _weighted_slot_cmi(state_weight: np.ndarray, conditional: np.ndarray) -> tuple[float, float]:
    joint = np.zeros((N_TRIAD_STATES, PAIR_SLOT_COUNT, N_PAIR_STATES), dtype=np.float64)
    for state in range(N_FULL_STATES):
        if state_weight[state] == 0.0:
            continue
        mask = state & (N_PAIR_STATES - 1)
        triad = state >> PAIR_SLOTS
        joint[triad, :, mask] += state_weight[state] * conditional[state]
    full = _cmi_from_joint(joint)
    retained = coarse_class_cmi(state_weight, conditional)["next_pair_slot_given_pair_class"]
    return full, retained


def projection_counterfactual() -> dict:
    """Separate multiplier shape from stationary occupancy.

    ``balanced`` uses a uniform full-state weight. ``stationary`` uses one
    system's pair-event occupancy with another system's conditional slot law.
    """
    rows = []
    laws = {}
    weights = {"balanced": np.ones(N_FULL_STATES, dtype=np.float64)}
    for system_id in ("R01", "R06"):
        kernel = _kernel(system_id)
        pair = pair_slot_laws(kernel)
        laws[system_id] = pair["conditional"]
        stationary = stationary_distribution(kernel)
        weights[system_id] = stationary_state_weight(stationary["pi"], pair["full_event"])
    for weight_name in ("balanced", "R01", "R06"):
        for law_name in ("R01", "R06"):
            full, retained = _weighted_slot_cmi(weights[weight_name], laws[law_name])
            rows.append(
                {
                    "discarded": full - retained,
                    "full_mask_cmi": full,
                    "law_system": law_name,
                    "retained_class_cmi": retained,
                    "retained_fraction": retained / full if full > 1e-15 else None,
                    "weighting": weight_name,
                }
            )
    return {"rows": rows}


def hierarchy_report() -> dict:
    """Numerical checks of the mechanism chain. Each arrow is a measured gap."""
    suppress = single_rule_local_law("R01")
    favour = single_rule_local_law("R06")
    shapes = topology_shape_summary()
    r01_path = checkpoint_source("R01", "path")
    r06_path = checkpoint_source("R06", "path")
    r01_star = checkpoint_source("R01", "star")
    memory = {system_id: gate_memory_curve(system_id, "path") for system_id in ("R00", "R01", "R06")}
    drift = {system_id: drift_report(system_id) for system_id in ("R01", "R02", "R03", "R06", "R07")}
    current = {system_id: contribution_atlas(system_id)["balanced_cmi"] for system_id in ("R00", "R01", "R06")}

    def at(curve: list[dict], step: int, key: str) -> float:
        return next(row[key] for row in curve if row["checkpoint"] == step)

    r01_late = at(memory["R01"], 64, "I_initial_gate_current_pair_mask")
    r01_early = at(memory["R01"], 1, "I_initial_gate_current_pair_mask")
    r00_mask = max(abs(at(memory["R00"], step, "I_initial_full_triad_current_pair_mask")) for step in MEMORY_CHECKPOINTS)
    return {
        "arrows": {
            "current_gate_still_biases_the_slot_law": {
                "r00_balanced_cmi": current["R00"],
                "r01_balanced_cmi": current["R01"],
                "r01_initial_pair_mask_mi_at_64": r01_late,
            },
            "favour_and_suppress_are_different_distances": {
                "favour_cmi": favour["analytic_balanced_CMI"],
                "favour_total_variation": asymmetry_table()[1]["total_variation_from_uniform"],
                "suppress_cmi": suppress["analytic_balanced_CMI"],
                "suppress_total_variation": asymmetry_table()[0]["total_variation_from_uniform"],
            },
            "gate_refresh_erases_initial_pair_information": {
                "r00_pair_mask_mi_max_abs": r00_mask,
                "r01_pair_mask_mi_at_1": r01_early,
                "r01_pair_mask_mi_at_64": r01_late,
            },
            "one_slot_reweight_matches_the_closed_form": {
                "r01_gap": suppress["gap"],
                "r06_gap": favour["gap"],
            },
            "path_splits_shape_and_star_does_not": {
                "path_one_class_per_edge_count": shapes["path"]["one_class_per_edge_count"],
                "r01_path_shape": r01_path["epoch_mi"]["class_given_edge_count"],
                "r01_star_shape": r01_star["epoch_mi"]["class_given_edge_count"],
                "r06_path_shape": r06_path["epoch_mi"]["class_given_edge_count"],
                "star_one_class_per_edge_count": shapes["star"]["one_class_per_edge_count"],
            },
            "rule_induced_drift_sign": {
                system_id: {
                    "balanced_rule_induced_drift": row["balanced_rule_induced_drift"],
                    "sign": row["active_rule_induced_sign"],
                    "stationary_expected_drift": row["stationary_expected_drift"],
                }
                for system_id, row in drift.items()
            },
        }
    }
