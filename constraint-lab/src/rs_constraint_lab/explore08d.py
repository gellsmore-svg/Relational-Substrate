"""Generation 8D two-gate composition.

The census is exact. A weight is a positive rational multiplier. The W4
grades are evaluation points, not fitted samples. Structural identity does
not include the weight. S4 canonicalisation does not quotient by bit
complement or by weight reciprocity.

Literal duplicate structural rules are rejected by ``structurally_simple``.
The kernel would multiply them. They are not systems in this atlas.
"""

from __future__ import annotations

import hashlib
import itertools
import math
from collections import Counter, defaultdict
from fractions import Fraction

import numpy as np

from rs_constraint_lab.constraints import (
    DISSOLVE,
    FORM,
    Choreography,
    Constraint,
    parse_expression,
    structurally_simple,
)
from rs_constraint_lab.explore08b import _cmi_from_joint
from rs_constraint_lab.explore08c import analytic_balanced_cmi
from rs_constraint_lab.kernel import build_kernel
from rs_constraint_lab.state import permutations, relation_slots, relabel_relation_state, slot_permutation_maps
from rs_constraint_lab.weights import alphabet_factors

EXPERIMENT_ID = "generation-008d-two-gate-composition"
ANALYSIS_VERSION = "generation-008d-composition/v1"
ROUND_ID = "round-d0"
N_FULL_STATES = 1024
N_PAIR_STATES = 64
N_TRIAD_STATES = 16
PAIR_SLOT_COUNT = 6
TRIAD_SLOT_COUNT = 4
STRUCTURAL_PLACEHOLDER = "neutral"
GRADES = ("strong_suppress", "weak_suppress", "weak_favour", "strong_favour")
PROBABILITY_TOLERANCE = 1e-12
CMI_TOLERANCE = 1e-12
KERNEL_TOLERANCE = 1e-12
LOGIT_TOLERANCE = 1e-12
REDUCIBILITY_TOLERANCE = 1e-12
CLASSES = ("R0", "R1U", "R1G", "R1T", "R2S", "R2G")


class CompositionError(RuntimeError):
    """An exact identity missed its tolerance."""


def _slots() -> tuple[tuple[int, ...], ...]:
    return tuple(relation_slots(4, 3))


SLOTS = _slots()
SLOT_MAPS = tuple(slot_permutation_maps(4, SLOTS))
FACTORS = alphabet_factors("W4")
GRADE_FACTOR = {name: FACTORS[name] for name in GRADES}


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def log_fraction(value: Fraction) -> float:
    if value <= 0:
        raise CompositionError("log weight is not defined for a non-positive multiplier")
    return math.log(value.numerator) - math.log(value.denominator)


def rule_key(rule: Constraint) -> tuple[int, int, int, int]:
    if len(rule.conditions) != 1 or rule.counts:
        raise CompositionError("a primary rule must be one triad literal and no count")
    gate, required = rule.conditions[0]
    if rule.action >= PAIR_SLOT_COUNT or gate < PAIR_SLOT_COUNT:
        raise CompositionError("a primary rule must toggle a pair and read a triad")
    return (rule.polarity, rule.action, gate, required)


def constraint_from_key(key: tuple[int, int, int, int], weight: str) -> Constraint:
    polarity, action, gate, required = key
    return Constraint(polarity, action, ((gate, required),), weight, ())


def expression_from_key(key: tuple[int, int, int, int], weight: str) -> str:
    return constraint_from_key(key, weight).expression(list(SLOTS))


def structural_expression(key: tuple[int, int, int, int]) -> str:
    rendered = expression_from_key(key, STRUCTURAL_PLACEHOLDER)
    suffix = f" => {STRUCTURAL_PLACEHOLDER}"
    if not rendered.endswith(suffix):
        raise CompositionError("structural expression did not use the placeholder weight")
    return rendered[: -len(suffix)]


def all_structural_rules() -> tuple[Constraint, ...]:
    rules = []
    for polarity in (FORM, DISSOLVE):
        for action in range(PAIR_SLOT_COUNT):
            for gate in range(PAIR_SLOT_COUNT, PAIR_SLOT_COUNT + TRIAD_SLOT_COUNT):
                for required in (0, 1):
                    rules.append(Constraint(polarity, action, ((gate, required),), STRUCTURAL_PLACEHOLDER, ()))
    if len(rules) != len({rule_key(rule) for rule in rules}):
        raise CompositionError("structural rules are not unique")
    return tuple(rules)


def labelled_pairs(rules: tuple[Constraint, ...]) -> tuple[tuple[Constraint, Constraint], ...]:
    pairs = []
    for left, right in itertools.combinations(rules, 2):
        if rule_key(left) == rule_key(right):
            raise CompositionError("a structural rule was repeated inside combinations")
        if not structurally_simple((left, right)):
            raise CompositionError("an unordered pair of distinct rules was rejected")
        if rule_key(left) <= rule_key(right):
            pairs.append((left, right))
        else:
            pairs.append((right, left))
    return tuple(pairs)


def _relabel_fast(key: tuple[int, int, int, int], edge_map: tuple[int, ...]) -> tuple[int, int, int, int]:
    polarity, action, gate, required = key
    return (polarity, edge_map[action], edge_map[gate], required)


def canonical_structural_key(left: tuple[int, int, int, int], right: tuple[int, int, int, int]) -> tuple:
    best = None
    for edge_map in SLOT_MAPS:
        ordered = tuple(sorted((_relabel_fast(left, edge_map), _relabel_fast(right, edge_map))))
        if best is None or ordered < best:
            best = ordered
    return best


def canonical_weighted_key(
    left: tuple[int, int, int, int],
    left_weight: str,
    right: tuple[int, int, int, int],
    right_weight: str,
) -> tuple:
    best = None
    for edge_map in SLOT_MAPS:
        ordered = tuple(sorted((
            (_relabel_fast(left, edge_map), left_weight),
            (_relabel_fast(right, edge_map), right_weight),
        )))
        if best is None or ordered < best:
            best = ordered
    return best


def _face(action: int, gate: int) -> bool:
    return set(SLOTS[action]).issubset(SLOTS[gate])


def _pair_relation(left_action: int, right_action: int) -> str:
    if left_action == right_action:
        return "same_pair"
    if set(SLOTS[left_action]) & set(SLOTS[right_action]):
        return "adjacent_pairs"
    return "disjoint_pairs"


def describe_pair(left: tuple[int, int, int, int], right: tuple[int, int, int, int]) -> dict:
    left_polarity, left_action, left_gate, left_required = left
    right_polarity, right_action, right_gate, right_required = right
    if left_required == right_required:
        polarity_relation = "same_polarity"
    elif left_gate == right_gate:
        polarity_relation = "opposite_polarity"
    else:
        polarity_relation = "mixed_literal_polarity"
    action_relation = _pair_relation(left_action, right_action)
    direction_relation = "same_direction" if left_polarity == right_polarity else "opposite_direction"
    gate_relation = "same_triad" if left_gate == right_gate else "different_triads"
    incidence = [
        [bool(_face(left_action, left_gate)), bool(_face(left_action, right_gate))],
        [bool(_face(right_action, left_gate)), bool(_face(right_action, right_gate))],
    ]
    if (
        action_relation == "same_pair"
        and gate_relation == "same_triad"
        and polarity_relation == "opposite_polarity"
        and direction_relation == "same_direction"
    ):
        family = "complementary_gate"
    elif action_relation == "same_pair" and gate_relation == "different_triads" and direction_relation == "same_direction":
        family = "same_action_different_gates"
    elif action_relation != "same_pair" and gate_relation == "same_triad":
        family = "different_actions_same_gate"
    elif action_relation != "same_pair" and gate_relation == "different_triads":
        family = "different_actions_different_gates"
    elif action_relation == "same_pair" and direction_relation == "opposite_direction":
        family = "same_slot_opposite_directions"
    else:
        family = "other"
    return {
        "action_relation": action_relation,
        "composition_family": family,
        "cross_incidence": [incidence[0][1], incidence[1][0]],
        "direction_relation": direction_relation,
        "gate_relation": gate_relation,
        "incidence_matrix": incidence,
        "own_incidence": [incidence[0][0], incidence[1][1]],
        "polarity_relation": polarity_relation,
    }


def build_universe() -> dict:
    rules = all_structural_rules()
    pairs = labelled_pairs(rules)
    grouped: dict[tuple, list[tuple]] = defaultdict(list)
    for left, right in pairs:
        grouped[canonical_structural_key(rule_key(left), rule_key(right))].append((rule_key(left), rule_key(right)))
    orbits = []
    weighted_count = 0
    for index, canonical in enumerate(sorted(grouped)):
        members = grouped[canonical]
        if canonical_structural_key(canonical[0], canonical[1]) != canonical:
            raise CompositionError("structural canonicalisation is not idempotent")
        weighted = []
        seen = set()
        for left_weight in GRADES:
            for right_weight in GRADES:
                key = canonical_weighted_key(canonical[0], left_weight, canonical[1], right_weight)
                if canonical_weighted_key(key[0][0], key[0][1], key[1][0], key[1][1]) != key:
                    raise CompositionError("weighted canonicalisation is not idempotent")
                if key in seen:
                    continue
                seen.add(key)
                weighted.append(key)
        weighted = tuple(sorted(weighted))
        orbit_id = f"ORB-{index:04d}"
        systems = []
        for weight_index, key in enumerate(weighted):
            systems.append(
                {
                    "canonical_weighted_rules": [
                        expression_from_key(key[0][0], key[0][1]),
                        expression_from_key(key[1][0], key[1][1]),
                    ],
                    "structural_orbit_id": orbit_id,
                    "system_id": f"{orbit_id}-W{weight_index:02d}",
                    "weighted_key": key,
                    "weights": [key[0][1], key[1][1]],
                }
            )
        weighted_count += len(systems)
        orbits.append(
            {
                "canonical_rules": [structural_expression(canonical[0]), structural_expression(canonical[1])],
                "canonical_structural_key": canonical,
                "descriptors": describe_pair(canonical[0], canonical[1]),
                "orbit_id": orbit_id,
                "orbit_size": len(members),
                "systems": systems,
            }
        )
    if sum(orbit["orbit_size"] for orbit in orbits) != len(pairs):
        raise CompositionError("orbit sizes do not sum to the labelled-pair count")
    return {
        "duplicate_structural_rules_allowed": False,
        "labelled_pair_count": len(pairs),
        "labelled_rule_count": len(rules),
        "orbits": orbits,
        "structural_orbit_count": len(orbits),
        "weighted_canonical_count": weighted_count,
    }


_UNIVERSE: dict | None = None


def load_universe() -> dict:
    global _UNIVERSE
    if _UNIVERSE is None:
        _UNIVERSE = build_universe()
    return _UNIVERSE


def implementation_weights(constraints: tuple[Constraint, ...]) -> tuple[tuple[Fraction, ...], ...]:
    kernel = build_kernel(
        4,
        Choreography(0, 0, constraints),
        FACTORS,
        relation_slots=SLOTS,
    )
    if any(kernel.deadlock):
        raise CompositionError("a two-gate state has an empty admissible set")
    return kernel.weights


def product_weights(constraints: tuple[Constraint, ...]) -> tuple[tuple[Fraction, ...], ...]:
    rows = []
    for state in range(N_FULL_STATES):
        weights = [Fraction(1) for _ in range(len(SLOTS))]
        for constraint in constraints:
            if constraint.matches(state, constraint.action):
                weights[constraint.action] *= FACTORS[constraint.weight]
        rows.append(tuple(weights))
    return tuple(rows)


def _check_kernel_agreement(constraints: tuple[Constraint, ...], product: tuple[tuple[Fraction, ...], ...]) -> float:
    kernel_rows = implementation_weights(constraints)
    gap = 0.0
    for state in range(N_FULL_STATES):
        if kernel_rows[state] != product[state]:
            for left, right in zip(kernel_rows[state], product[state], strict=True):
                gap = max(gap, abs(float(left - right)))
            if kernel_rows[state] != product[state]:
                raise CompositionError("kernel weights and the product formula disagree")
    return gap


def _pair_laws(full_rows: tuple[tuple[Fraction, ...], ...]) -> tuple[tuple[Fraction, ...], ...]:
    laws = []
    for row in full_rows:
        pair = row[:PAIR_SLOT_COUNT]
        total = sum(pair, Fraction(0))
        if any(weight <= 0 for weight in pair):
            raise CompositionError("a pair weight is not positive")
        law = tuple(weight / total for weight in pair)
        if sum(law, Fraction(0)) != 1:
            raise CompositionError("a six-slot law does not sum to 1")
        laws.append(law)
    return tuple(laws)


def _pattern(state: int, bits: tuple[int, ...]) -> int:
    value = 0
    for shift, bit in enumerate(bits):
        value |= ((state >> bit) & 1) << shift
    return value


def _minimal_coordinates(laws: tuple[tuple[Fraction, ...], ...], bits: tuple[int, ...]) -> dict:
    def determines(chosen: tuple[int, ...]) -> bool:
        seen: dict[int, tuple[Fraction, ...]] = {}
        for state, law in enumerate(laws):
            key = _pattern(state, chosen)
            previous = seen.get(key)
            if previous is None:
                seen[key] = law
            elif previous != law:
                return False
        return True

    if not determines(bits):
        raise CompositionError("the candidate bits do not determine the six-slot law")
    smallest = len(bits)
    winners = []
    for size in range(len(bits) + 1):
        found = [tuple(sorted(chosen)) for chosen in itertools.combinations(bits, size) if determines(tuple(sorted(chosen)))]
        if found:
            smallest = size
            winners = found
            break
    for chosen in winners:
        for dropped in itertools.combinations(chosen, len(chosen) - 1):
            if determines(tuple(dropped)):
                raise CompositionError("a declared minimal coordinate set has a smaller determining subset")
    return {
        "all_minimal_coordinate_sets": [list(item) for item in winners],
        "candidate_bits": list(bits),
        "minimal_coordinate_count": smallest,
    }


def _effective_gate_dimension(laws: tuple[tuple[Fraction, ...], ...]) -> int:
    triad_bits = tuple(range(PAIR_SLOT_COUNT, PAIR_SLOT_COUNT + TRIAD_SLOT_COUNT))

    def determines(chosen: tuple[int, ...]) -> bool:
        seen: dict[tuple[int, int], tuple[Fraction, ...]] = {}
        for state, law in enumerate(laws):
            key = (state & (N_PAIR_STATES - 1), _pattern(state, chosen))
            previous = seen.get(key)
            if previous is None:
                seen[key] = law
            elif previous != law:
                return False
        return True

    for size in range(len(triad_bits) + 1):
        for chosen in itertools.combinations(triad_bits, size):
            if determines(chosen):
                if size > 2:
                    raise CompositionError("effective gate dimension exceeds two")
                return size
    raise CompositionError("no triad-bit set determines the law")


def _cmi_numpy(joint: np.ndarray) -> float:
    total = float(joint.sum())
    if total <= 0.0:
        raise CompositionError("conditional information received no mass")
    probability = joint / total
    conditioner = probability.sum(axis=(0, 1))
    left = probability.sum(axis=1)
    right = probability.sum(axis=0)
    denominator = left[:, None, :] * right[None, :, :]
    mask = probability > 0.0
    ratio = np.ones_like(probability)
    np.divide(probability * conditioner[None, None, :], denominator, out=ratio, where=mask)
    return float(np.sum(np.where(mask, probability * np.log(ratio), 0.0)))


def _float_laws(laws: tuple[tuple[Fraction, ...], ...]) -> np.ndarray:
    array = np.empty((N_FULL_STATES, PAIR_SLOT_COUNT), dtype=np.float64)
    for state, law in enumerate(laws):
        array[state] = [float(item) for item in law]
    return array


def _balanced_cmi(array: np.ndarray, conditioner_bits: tuple[int, ...] | None = None) -> float:
    if conditioner_bits is None:
        joint = np.zeros((N_TRIAD_STATES, PAIR_SLOT_COUNT, N_PAIR_STATES), dtype=np.float64)
        for state in range(N_FULL_STATES):
            joint[state >> PAIR_SLOT_COUNT, :, state & (N_PAIR_STATES - 1)] = array[state]
        return _cmi_numpy(joint)
    width = 1 << len(conditioner_bits)
    joint = np.zeros((width, PAIR_SLOT_COUNT, N_PAIR_STATES), dtype=np.float64)
    for state in range(N_FULL_STATES):
        joint[_pattern(state, conditioner_bits), :, state & (N_PAIR_STATES - 1)] += array[state]
    return _cmi_numpy(joint)


def _conditional_cmi(array: np.ndarray, target_bit: int, given_bit: int) -> float:
    joint = np.zeros((2, PAIR_SLOT_COUNT, N_PAIR_STATES * 2), dtype=np.float64)
    for state in range(N_FULL_STATES):
        mask = state & (N_PAIR_STATES - 1)
        given = (state >> given_bit) & 1
        target = (state >> target_bit) & 1
        joint[target, :, mask + N_PAIR_STATES * given] += array[state]
    return _cmi_numpy(joint)


def _literal(key: tuple[int, int, int, int], state: int) -> int:
    _polarity, _action, gate, required = key
    return int(((state >> gate) & 1) == required)


def _admissible(key: tuple[int, int, int, int], state: int) -> int:
    polarity, action, _gate, _required = key
    present = (state >> action) & 1
    if polarity == FORM:
        return int(present == 0)
    return int(present == 1)


def _matches(key: tuple[int, int, int, int], state: int) -> bool:
    return _admissible(key, state) == 1 and _literal(key, state) == 1


def _truth_table(
    keys: tuple[tuple[int, int, int, int], tuple[int, int, int, int]],
    full_rows: tuple[tuple[Fraction, ...], ...],
    laws: tuple[tuple[Fraction, ...], ...],
) -> list[dict]:
    grouped: dict[tuple[int, int, int, int], list[int]] = defaultdict(list)
    for state in range(N_FULL_STATES):
        grouped[(
            _admissible(keys[0], state),
            _admissible(keys[1], state),
            _literal(keys[0], state),
            _literal(keys[1], state),
        )].append(state)
    rows = []
    for admissibility_left in (0, 1):
        for admissibility_right in (0, 1):
            for literal_left in (0, 1):
                for literal_right in (0, 1):
                    signature = (admissibility_left, admissibility_right, literal_left, literal_right)
                    states = grouped.get(signature, [])
                    if not states:
                        rows.append(
                            {
                                "active_rules": [],
                                "gate_literal_state": [literal_left, literal_right],
                                "normalised_slot_law": None,
                                "pair_admissibility_state": [admissibility_left, admissibility_right],
                                "pre_normalisation_weights": None,
                                "realised": False,
                                "state_count": 0,
                            }
                        )
                        continue
                    sample = states[0]
                    law = laws[sample]
                    weights = full_rows[sample][:PAIR_SLOT_COUNT]
                    for state in states[1:]:
                        if laws[state] != law or full_rows[state][:PAIR_SLOT_COUNT] != weights:
                            raise CompositionError("a truth-table cell contains two laws")
                    active = []
                    if _matches(keys[0], sample):
                        active.append("rule_1")
                    if _matches(keys[1], sample):
                        active.append("rule_2")
                    rows.append(
                        {
                            "active_rules": active,
                            "gate_literal_state": [literal_left, literal_right],
                            "normalised_slot_law": [fraction_text(item) for item in law],
                            "pair_admissibility_state": [admissibility_left, admissibility_right],
                            "pre_normalisation_weights": [fraction_text(item) for item in weights],
                            "realised": True,
                            "state_count": len(states),
                        }
                    )
    if sum(row["state_count"] for row in rows) != N_FULL_STATES:
        raise CompositionError("truth-table state counts do not cover the state space")
    return rows


def _row_fingerprint(laws: tuple[tuple[Fraction, ...], ...]) -> list[dict]:
    counts: Counter[tuple[Fraction, ...]] = Counter(laws)
    rows = []
    for index, (law, count) in enumerate(sorted(counts.items(), key=lambda item: (-item[1], item[0]))):
        rows.append(
            {
                "row_index": index,
                "slot_law": [fraction_text(item) for item in law],
                "state_count": count,
            }
        )
    return rows


def _pack_weight_table(full_rows: tuple[tuple[Fraction, ...], ...]) -> tuple[np.ndarray, np.ndarray]:
    """Little-endian numerator and denominator arrays.

    A non-negative numerator has the same eight bytes as signed little-endian
    ``to_bytes``. Every weight in this census is positive.
    """
    numerators = np.empty((N_FULL_STATES, len(SLOTS)), dtype="<u8")
    denominators = np.empty((N_FULL_STATES, len(SLOTS)), dtype="<u8")
    for state, row in enumerate(full_rows):
        for slot, weight in enumerate(row):
            if weight.numerator < 0:
                raise CompositionError("a weight numerator is negative")
            numerators[state, slot] = weight.numerator
            denominators[state, slot] = weight.denominator
    return numerators, denominators


def _hash_packed(numerators: np.ndarray, denominators: np.ndarray) -> str:
    packed = np.empty((numerators.shape[0], numerators.shape[1], 2), dtype="<u8")
    packed[:, :, 0] = numerators
    packed[:, :, 1] = denominators
    return hashlib.sha256(np.ascontiguousarray(packed).tobytes()).hexdigest()


def _law_hash(full_rows: tuple[tuple[Fraction, ...], ...]) -> str:
    numerators, denominators = _pack_weight_table(full_rows)
    return _hash_packed(numerators, denominators)


_PERMUTATION_INVERSES: list[tuple[np.ndarray, np.ndarray]] | None = None


def _permutation_inverses() -> list[tuple[np.ndarray, np.ndarray]]:
    global _PERMUTATION_INVERSES
    if _PERMUTATION_INVERSES is None:
        prepared = []
        for perm, edge_map in zip(permutations(4), SLOT_MAPS, strict=True):
            inverse_state = [0] * N_FULL_STATES
            for state in range(N_FULL_STATES):
                inverse_state[relabel_relation_state(state, perm, SLOTS)] = state
            inverse_slot = [0] * len(SLOTS)
            for slot, image in enumerate(edge_map):
                inverse_slot[image] = slot
            prepared.append((np.asarray(inverse_state, dtype=np.int64), np.asarray(inverse_slot, dtype=np.int64)))
        _PERMUTATION_INVERSES = prepared
    return _PERMUTATION_INVERSES


def local_law_class(full_rows: tuple[tuple[Fraction, ...], ...]) -> str:
    """Minimum SHA-256 of the full weight table over S4.

    The hash is an identity for the equivalence class. It is not a score.
    The identity permutation reproduces ``_law_hash``.
    """
    numerators, denominators = _pack_weight_table(full_rows)
    best = None
    for inverse_state, inverse_slot in _permutation_inverses():
        token = _hash_packed(numerators[inverse_state][:, inverse_slot], denominators[inverse_state][:, inverse_slot])
        if best is None or token < best:
            best = token
    if best is None:
        raise CompositionError("S4 produced no law image")
    return best


def _varying_slots(full_rows: tuple[tuple[Fraction, ...], ...]) -> tuple[int, ...]:
    found = []
    for slot in range(PAIR_SLOT_COUNT):
        if any(row[slot] != 1 for row in full_rows):
            found.append(slot)
    return tuple(found)


def _one_rule_hashes() -> dict[str, tuple[Constraint, ...]]:
    catalogue: dict[str, tuple[Constraint, ...]] = {}
    empty_rows = product_weights(())
    catalogue[_law_hash(empty_rows)] = ()
    for action in range(PAIR_SLOT_COUNT):
        for polarity in (FORM, DISSOLVE):
            for weight in GRADES:
                constraints = (Constraint(polarity, action, (), weight, ()),)
                catalogue[_law_hash(product_weights(constraints))] = constraints
                for gate in range(PAIR_SLOT_COUNT, PAIR_SLOT_COUNT + TRIAD_SLOT_COUNT):
                    for required in (0, 1):
                        conditional = (Constraint(polarity, action, ((gate, required),), weight, ()),)
                        catalogue[_law_hash(product_weights(conditional))] = conditional
    return catalogue


_ONE_RULE_HASHES: dict[str, tuple[Constraint, ...]] | None = None


def one_rule_catalogue() -> dict[str, tuple[Constraint, ...]]:
    global _ONE_RULE_HASHES
    if _ONE_RULE_HASHES is None:
        _ONE_RULE_HASHES = _one_rule_hashes()
    return _ONE_RULE_HASHES


def _classify(
    keys: tuple[tuple[int, int, int, int], tuple[int, int, int, int]],
    multipliers: tuple[Fraction, Fraction],
    full_rows: tuple[tuple[Fraction, ...], ...],
    dimension: int,
) -> dict:
    digest = _law_hash(full_rows)
    catalogue = one_rule_catalogue()
    comparator = catalogue.get(digest)
    varying = _varying_slots(full_rows)
    syntactic = comparator is not None
    if not varying:
        reducibility = "R0"
    elif comparator is not None and len(comparator) == 1 and not comparator[0].conditions:
        reducibility = "R1U"
    elif comparator is not None and len(comparator) == 1 and comparator[0].conditions:
        reducibility = "R1G"
    elif _is_two_level(keys, multipliers, full_rows, varying):
        reducibility = "R1T"
        syntactic = False
    elif dimension <= 1:
        reducibility = "R2S"
    else:
        reducibility = "R2G"
    if reducibility == "R2G" and syntactic:
        raise CompositionError("a two-gate law matched a one-rule comparator")
    if reducibility in {"R0", "R1U", "R1G"} and comparator is None:
        raise CompositionError(f"{reducibility} has no comparator in the one-rule grammar")
    if reducibility in {"R0", "R1U", "R1G"}:
        if product_weights(comparator) != full_rows:
            raise CompositionError(f"{reducibility} comparator does not reproduce the weight table")
    return {
        "comparator_expressions": [constraint.expression(list(SLOTS)) for constraint in comparator] if comparator else [],
        "reducibility_class": reducibility,
        "syntactic_one_rule": syntactic,
        "varying_slots": list(varying),
    }


def _is_two_level(keys, multipliers, full_rows, varying) -> bool:
    if len(varying) != 1:
        return False
    if keys[0][1] != keys[1][1] or keys[0][0] != keys[1][0] or keys[0][2] != keys[1][2]:
        return False
    if keys[0][3] == keys[1][3]:
        return False
    if multipliers[0] == multipliers[1]:
        return False
    slot = varying[0]
    if slot != keys[0][1]:
        return False
    for state, row in enumerate(full_rows):
        for other in range(PAIR_SLOT_COUNT):
            if other != slot and row[other] != 1:
                return False
        if not _admissible(keys[0], state):
            if row[slot] != 1:
                return False
            continue
        literal = _literal(keys[0], state)
        expected = multipliers[0] if literal else multipliers[1]
        if row[slot] != expected:
            return False
    return True


def _logit_checks(keys, multipliers, full_rows) -> dict:
    same_action = keys[0][1] == keys[1][1] and keys[0][0] == keys[1][0]
    different_gates = keys[0][2] != keys[1][2]
    max_same = 0.0
    max_different = 0.0
    same_checked = 0
    different_checked = 0
    delta_gap = 0.0
    delta_checked = 0
    for state in range(N_FULL_STATES):
        both = _matches(keys[0], state) and _matches(keys[1], state)
        if not both:
            continue
        row = full_rows[state]
        pair = row[:PAIR_SLOT_COUNT]
        total = sum(pair, Fraction(0))
        if same_action:
            expected_action = multipliers[0] * multipliers[1]
            expected_total = expected_action + PAIR_SLOT_COUNT - 1
            action = keys[0][1]
            if pair[action] != expected_action or total != expected_total:
                max_same = max(max_same, abs(float(pair[action] - expected_action)), abs(float(total - expected_total)))
            same_checked += 1
        elif keys[0][1] != keys[1][1]:
            expected_total = multipliers[0] + multipliers[1] + PAIR_SLOT_COUNT - 2
            if pair[keys[0][1]] != multipliers[0] or pair[keys[1][1]] != multipliers[1] or total != expected_total:
                max_different = max(
                    max_different,
                    abs(float(pair[keys[0][1]] - multipliers[0])),
                    abs(float(pair[keys[1][1]] - multipliers[1])),
                    abs(float(total - expected_total)),
                )
            different_checked += 1
    if same_action and different_gates:
        levels = {}
        for state in range(N_FULL_STATES):
            if not (_admissible(keys[0], state) and _admissible(keys[1], state)):
                continue
            signature = (_literal(keys[0], state), _literal(keys[1], state))
            levels[signature] = full_rows[state][keys[0][1]]
        if set(levels) == {(0, 0), (0, 1), (1, 0), (1, 1)}:
            identity = levels[(1, 1)] * levels[(0, 0)] - levels[(1, 0)] * levels[(0, 1)]
            delta_gap = abs(float(identity))
            delta_checked = 1
            if identity != 0:
                raise CompositionError("same-action logit interaction is not zero")
    if max_same > REDUCIBILITY_TOLERANCE or max_different > REDUCIBILITY_TOLERANCE:
        raise CompositionError("normalisation formula missed its tolerance")
    return {
        "different_action_both_active_checks": different_checked,
        "different_action_gap": max_different,
        "logit_interaction_checks": delta_checked,
        "logit_interaction_gap": delta_gap,
        "same_action_both_active_checks": same_checked,
        "same_action_gap": max_same,
    }


def _log_additivity(keys, multipliers, full_rows) -> float:
    """Exact product check, then the float log residual on slots a rule touches.

    A slot that neither rule touches stays at weight 1. Its log residual is
    identically zero, so it is not sent through ``math.log``.
    """
    gap = 0.0
    for state, row in enumerate(full_rows):
        left_match = _matches(keys[0], state)
        right_match = _matches(keys[1], state)
        for slot, weight in enumerate(row):
            left = multipliers[0] if left_match and slot == keys[0][1] else Fraction(1)
            right = multipliers[1] if right_match and slot == keys[1][1] else Fraction(1)
            if weight != left * right:
                raise CompositionError("pre-normalisation weights are not the product of the rule weights")
            if left == 1 and right == 1:
                continue
            residual = log_fraction(weight) - log_fraction(left) - log_fraction(right)
            gap = max(gap, abs(residual))
    if gap > LOGIT_TOLERANCE:
        raise CompositionError(f"log-weight residual {gap} exceeds {LOGIT_TOLERANCE}")
    return gap


def _max_probability_gap(full_pair, other) -> float:
    if full_pair == other:
        return 0.0
    left = np.empty((N_FULL_STATES, PAIR_SLOT_COUNT), dtype=np.float64)
    right = np.empty((N_FULL_STATES, PAIR_SLOT_COUNT), dtype=np.float64)
    for state in range(N_FULL_STATES):
        left[state] = [float(item) for item in full_pair[state]]
        right[state] = [float(item) for item in other[state]]
    left /= left.sum(axis=1, keepdims=True)
    right /= right.sum(axis=1, keepdims=True)
    return float(np.max(np.abs(left - right)))


def _ablation(keys, weights: tuple[str, str], full_rows) -> list[dict]:
    specs = (
        ("full", (constraint_from_key(keys[0], weights[0]), constraint_from_key(keys[1], weights[1]))),
        ("rule_1_only", (constraint_from_key(keys[0], weights[0]),)),
        ("rule_2_only", (constraint_from_key(keys[1], weights[1]),)),
        ("neither", ()),
    )
    rows = []
    full_pair = tuple(row[:PAIR_SLOT_COUNT] for row in full_rows)
    for name, constraints in specs:
        other = tuple(row[:PAIR_SLOT_COUNT] for row in product_weights(constraints))
        rows.append(
            {
                "ablation": name,
                "law_equal_to_full": other == full_pair,
                "max_probability_gap": _max_probability_gap(full_pair, other),
            }
        )
    return rows


def _match_count(key: tuple[int, int, int, int]) -> int:
    return sum(1 for state in range(N_FULL_STATES) if _matches(key, state))


def _gate_roles(keys, ablation_rows: list[dict], descriptors: dict, weights: tuple[str, str]) -> list[dict]:
    by_name = {row["ablation"]: row for row in ablation_rows}
    roles = []
    masked = descriptors["composition_family"] == "complementary_gate" and weights[0] == weights[1]
    for index, _name in enumerate(("rule_1_only", "rule_2_only")):
        other = "rule_2_only" if index == 0 else "rule_1_only"
        removed_equal = by_name[other]["law_equal_to_full"]
        matches = _match_count(keys[index])
        roles.append(
            {
                "active_on_a_proper_subset": 0 < matches < N_FULL_STATES,
                "gate_index": index + 1,
                "masked_by_equal_weights": masked,
                "necessary_for_a_local_law_distinction": not removed_equal,
                "redundant": removed_equal,
            }
        )
    return roles


def _information(keys, laws, array: np.ndarray) -> dict:
    full = _balanced_cmi(array)
    reference = _cmi_from_joint(_reference_joint(array))
    if abs(full - reference) > CMI_TOLERANCE:
        raise CompositionError("numpy CMI and the Generation 8B enumerator disagree")
    gate_bits = tuple(dict.fromkeys((keys[0][2], keys[1][2])))
    from_gates = _balanced_cmi(array, gate_bits)
    if abs(full - from_gates) > CMI_TOLERANCE:
        raise CompositionError("truth-table gate weighting does not reproduce the full-triad CMI")
    result = {
        "balanced_full_triad_cmi": full,
        "conditional_gate_1_given_2": None,
        "conditional_gate_2_given_1": None,
        "gate_1_marginal_information": None,
        "gate_2_marginal_information": None,
        "truth_table_cmi_gap": abs(full - from_gates),
    }
    if len(gate_bits) == 2:
        result["gate_1_marginal_information"] = _balanced_cmi(array, (keys[0][2],))
        result["gate_2_marginal_information"] = _balanced_cmi(array, (keys[1][2],))
        result["conditional_gate_1_given_2"] = _conditional_cmi(array, keys[0][2], keys[1][2])
        result["conditional_gate_2_given_1"] = _conditional_cmi(array, keys[1][2], keys[0][2])
    elif len(gate_bits) == 1:
        marginal = _balanced_cmi(array, gate_bits)
        result["gate_1_marginal_information"] = marginal
        result["gate_2_marginal_information"] = marginal
    return result


def _reference_joint(array: np.ndarray) -> np.ndarray:
    joint = np.zeros((N_TRIAD_STATES, PAIR_SLOT_COUNT, N_PAIR_STATES), dtype=np.float64)
    for state in range(N_FULL_STATES):
        joint[state >> PAIR_SLOT_COUNT, :, state & (N_PAIR_STATES - 1)] = array[state]
    return joint


def analyse_system(orbit: dict, system: dict, *, with_class: bool = True) -> dict:
    key = system["weighted_key"]
    keys = (key[0][0], key[1][0])
    weights = (key[0][1], key[1][1])
    multipliers = (GRADE_FACTOR[weights[0]], GRADE_FACTOR[weights[1]])
    constraints = (constraint_from_key(keys[0], weights[0]), constraint_from_key(keys[1], weights[1]))
    if not structurally_simple(constraints):
        raise CompositionError("a weighted system repeats a structural rule")
    product = product_weights(constraints)
    kernel_gap = _check_kernel_agreement(constraints, product)
    laws = _pair_laws(product)
    bits = tuple(sorted({keys[0][1], keys[1][1], keys[0][2], keys[1][2]}))
    coordinates = _minimal_coordinates(laws, bits)
    dimension = _effective_gate_dimension(laws)
    classification = _classify(keys, multipliers, product, dimension)
    if classification["reducibility_class"] in {"R0", "R1U"} and dimension != 0:
        raise CompositionError("a zero-gate class retained a triad coordinate")
    if classification["reducibility_class"] in {"R1G", "R1T", "R2S"} and dimension != 1:
        raise CompositionError("a one-gate class does not have effective dimension 1")
    if classification["reducibility_class"] == "R2G" and dimension != 2:
        raise CompositionError("R2G does not have effective dimension 2")
    information = _information(keys, laws, _float_laws(laws))
    ablation = _ablation(keys, weights, product)
    roles = _gate_roles(keys, ablation, orbit["descriptors"], weights)
    identities = _logit_checks(keys, multipliers, product)
    log_gap = _log_additivity(keys, multipliers, product)
    fingerprints = _row_fingerprint(laws)
    return {
        "ablations": ablation,
        "canonical_weighted_rules": system["canonical_weighted_rules"],
        "comparator_expressions": classification["comparator_expressions"],
        "distinct_local_law_rows": len(fingerprints),
        "effective_gate_dimension": dimension,
        "gate_roles": roles,
        "identities": identities,
        "information": information,
        "kernel_max_abs_gap": kernel_gap,
        "labelled_law_sha256": _law_hash(product),
        "local_law_class": local_law_class(product) if with_class else None,
        "log_weight_gap": log_gap,
        "minimal_coordinate_count": coordinates["minimal_coordinate_count"],
        "minimal_coordinate_sets": coordinates["all_minimal_coordinate_sets"],
        "reducibility_class": classification["reducibility_class"],
        "row_fingerprints": fingerprints,
        "structural_orbit_id": orbit["orbit_id"],
        "syntactic_one_rule": classification["syntactic_one_rule"],
        "system_id": system["system_id"],
        "truth_table": _truth_table(keys, product, laws),
        "varying_slots": classification["varying_slots"],
        "weights": list(weights),
    }


def analyse_orbit(orbit_id: str, *, with_class: bool = True) -> dict:
    universe = load_universe()
    orbit = next(item for item in universe["orbits"] if item["orbit_id"] == orbit_id)
    systems = [analyse_system(orbit, system, with_class=with_class) for system in orbit["systems"]]
    return {
        "orbit_id": orbit_id,
        "orbit_size": orbit["orbit_size"],
        "systems": systems,
    }


def duplicate_kernel_product() -> dict:
    """The kernel multiplies a repeated structural rule. The grammar rejects it."""
    left = Constraint(FORM, 0, ((PAIR_SLOT_COUNT, 1),), "strong_favour", ())
    right = Constraint(FORM, 0, ((PAIR_SLOT_COUNT, 1),), "weak_suppress", ())
    if structurally_simple((left, right)):
        raise CompositionError("duplicate structural rules were accepted")
    state = 1 << PAIR_SLOT_COUNT
    rows = implementation_weights((left, right))
    expected = FACTORS["strong_favour"] * FACTORS["weak_suppress"]
    if rows[state][0] != expected:
        raise CompositionError("a forced duplicate did not multiply weights")
    return {
        "accepted_in_atlas": False,
        "expected_product": fraction_text(expected),
        "kernel_weight": fraction_text(rows[state][0]),
        "structural_predicate": "structurally_simple",
    }


def _uniform_law() -> tuple[Fraction, ...]:
    return tuple(Fraction(1, 6) for _ in range(PAIR_SLOT_COUNT))


def _active_law(multiplier: Fraction, action: int = 0) -> tuple[Fraction, ...]:
    total = multiplier + PAIR_SLOT_COUNT - 1
    return tuple((multiplier if slot == action else Fraction(1)) / total for slot in range(PAIR_SLOT_COUNT))


def _expected_delta(mask: int, law: tuple[Fraction, ...]) -> Fraction:
    total = Fraction(0)
    for slot, probability in enumerate(law):
        sign = -1 if (mask >> slot) & 1 else 1
        total += probability * sign
    return total


def enumerated_balanced_drift(multiplier: Fraction, polarity: int) -> Fraction:
    induced = Fraction(0)
    groups = 0
    for mask in range(N_PAIR_STATES):
        for gate in (0, 1):
            groups += 1
            present = (mask >> 0) & 1
            admissible = (polarity == FORM and not present) or (polarity == DISSOLVE and present)
            if gate == 1 and admissible:
                law = _active_law(multiplier, 0)
            else:
                law = _uniform_law()
            baseline = _expected_delta(mask, _uniform_law())
            induced += _expected_delta(mask, law) - baseline
    if groups != 128:
        raise CompositionError("drift enumeration did not cover 64 masks and 2 gate values")
    return induced / groups


def balanced_drift_formula(multiplier: Fraction, polarity: int) -> Fraction:
    if polarity == DISSOLVE:
        return Fraction(5) * (1 - multiplier) / (Fraction(24) * (multiplier + 5))
    if polarity == FORM:
        return Fraction(5) * (multiplier - 1) / (Fraction(24) * (multiplier + 5))
    raise CompositionError("polarity is not form or dissolve")


def one_gate_surface() -> dict:
    """One-gate formulas at the four W4 grades, including the weak grades."""
    rows = []
    for name in GRADES:
        multiplier = GRADE_FACTOR[name]
        for polarity, label in ((DISSOLVE, "dissolve"), (FORM, "form")):
            formula = balanced_drift_formula(multiplier, polarity)
            enumerated = enumerated_balanced_drift(multiplier, polarity)
            if formula != enumerated:
                raise CompositionError(f"{name} {label} drift formula disagrees with enumeration")
        constraint = Constraint(FORM, 0, ((PAIR_SLOT_COUNT, 1),), name, ())
        rows_full = product_weights((constraint,))
        _check_kernel_agreement((constraint,), rows_full)
        laws = _pair_laws(rows_full)
        enumerated_cmi = _balanced_cmi(_float_laws(laws))
        analytic = analytic_balanced_cmi(multiplier)
        if abs(enumerated_cmi - analytic) > CMI_TOLERANCE:
            raise CompositionError(f"{name} one-gate CMI missed the closed form")
        rows.append(
            {
                "analytic_balanced_cmi": analytic,
                "balanced_form_drift": fraction_text(balanced_drift_formula(multiplier, FORM)),
                "balanced_dissolve_drift": fraction_text(balanced_drift_formula(multiplier, DISSOLVE)),
                "enumerated_balanced_cmi": enumerated_cmi,
                "grade": name,
                "multiplier": fraction_text(multiplier),
            }
        )
    unconditional = enumerated_balanced_drift(GRADE_FACTOR["strong_suppress"], DISSOLVE)
    # Gate-off half of the groups contributes 0, so dropping the gate doubles the mean.
    always = Fraction(0)
    groups = 0
    multiplier = GRADE_FACTOR["strong_suppress"]
    for mask in range(N_PAIR_STATES):
        groups += 1
        present = mask & 1
        law = _active_law(multiplier, 0) if present else _uniform_law()
        always += _expected_delta(mask, law) - _expected_delta(mask, _uniform_law())
    always /= groups
    if always != 2 * unconditional:
        raise CompositionError("unconditional drift is not twice the one-gate balanced mean")
    return {
        "drift_formula_dissolve": "5(1-m)/(24(m+5))",
        "drift_formula_form": "5(m-1)/(24(m+5))",
        "grades": rows,
        "unconditional_doubles_conditional": True,
    }


def general_normalisation_identities() -> dict:
    """Closed forms for arbitrary positive multipliers, checked outside W4 too."""
    samples = (
        (Fraction(1, 4), Fraction(4)),
        (Fraction(1, 2), Fraction(2)),
        (Fraction(3), Fraction(5)),
        (Fraction(1, 3), Fraction(7)),
        (Fraction(4), Fraction(4)),
    )
    gaps = []
    for left, right in samples:
        same = _numeric_same_action(left, right)
        different = _numeric_different_actions(left, right)
        gaps.append({"different_action_gap": different, "m1": fraction_text(left), "m2": fraction_text(right), "same_action_gap": same})
        if same != 0 or different != 0:
            raise CompositionError("a general multiplier missed the normalisation formula")
    return {"samples": gaps}


def _numeric_same_action(left: Fraction, right: Fraction) -> Fraction:
    both = left * right
    total = both + 5
    formula = (both / total, tuple(Fraction(1, total) for _ in range(5)))
    weights = [Fraction(1) for _ in range(6)]
    weights[0] = both
    actual_total = sum(weights, Fraction(0))
    actual = tuple(weight / actual_total for weight in weights)
    gap = abs(actual[0] - formula[0])
    for slot in range(1, 6):
        gap = max(gap, abs(actual[slot] - formula[1][slot - 1]))
    return gap


def _numeric_different_actions(left: Fraction, right: Fraction) -> Fraction:
    total = left + right + 4
    weights = [Fraction(1) for _ in range(6)]
    weights[0] = left
    weights[1] = right
    actual_total = sum(weights, Fraction(0))
    actual = tuple(weight / actual_total for weight in weights)
    expected = [Fraction(1, total) for _ in range(6)]
    expected[0] = left / total
    expected[1] = right / total
    return max(abs(left_item - right_item) for left_item, right_item in zip(actual, expected, strict=True))


def expressivity_bound() -> dict:
    """Two primitive literals have no free conjunction coefficient."""
    return {
        "both_active_determined_by_the_other_three": True,
        "independent_conjunction_term": False,
        "logit_interaction": "L11 - L10 - L01 + L00 = 0",
        "representation": "L = c + λ1 l1(G1) + λ2 l2(G2)",
        "xor_isolated_by_two_primitive_literals": False,
    }


def universe_public() -> dict:
    """JSON-ready orbit catalogue. Weighted keys stay out of the plan body."""
    universe = load_universe()
    orbits = []
    for orbit in universe["orbits"]:
        orbits.append(
            {
                "canonical_rules": orbit["canonical_rules"],
                "descriptors": orbit["descriptors"],
                "orbit_id": orbit["orbit_id"],
                "orbit_size": orbit["orbit_size"],
                "weighted_system_count": len(orbit["systems"]),
                "weighted_system_ids": [system["system_id"] for system in orbit["systems"]],
            }
        )
    return {
        "duplicate_structural_rules_allowed": False,
        "labelled_pair_count": universe["labelled_pair_count"],
        "labelled_rule_count": universe["labelled_rule_count"],
        "orbits": orbits,
        "structural_orbit_count": universe["structural_orbit_count"],
        "weighted_canonical_count": universe["weighted_canonical_count"],
    }


def census_summary(system_rows: list[dict], orbits: list[dict] | None = None) -> dict:
    by_class = Counter(row["reducibility_class"] for row in system_rows)
    by_dimension = Counter(row["effective_gate_dimension"] for row in system_rows)
    classes_of_dimension = {
        str(dimension): sorted({row["reducibility_class"] for row in system_rows if row["effective_gate_dimension"] == dimension})
        for dimension in sorted(by_dimension)
    }
    information_by_dimension = {}
    for dimension in sorted(by_dimension):
        values = [row["information"]["balanced_full_triad_cmi"] for row in system_rows if row["effective_gate_dimension"] == dimension]
        information_by_dimension[str(dimension)] = {
            "max": max(values) if values else None,
            "min": min(values) if values else None,
        }
    higher_dimension_not_more_information = False
    if "1" in information_by_dimension and "2" in information_by_dimension:
        higher_dimension_not_more_information = (
            information_by_dimension["2"]["min"] < information_by_dimension["1"]["max"]
        )
    labelled_groups = defaultdict(set)
    class_groups = defaultdict(set)
    for row in system_rows:
        labelled_groups[row["labelled_law_sha256"]].add(row["structural_orbit_id"])
        if row["local_law_class"] is not None:
            class_groups[row["local_law_class"]].add(row["structural_orbit_id"])
    redundant = [
        row["system_id"]
        for row in system_rows
        if any(role["redundant"] for role in row["gate_roles"])
    ]
    families = Counter()
    if orbits is not None:
        for orbit in orbits:
            families[orbit["descriptors"]["composition_family"]] += 1
    simplest = None
    for row in system_rows:
        if row["effective_gate_dimension"] != 2:
            continue
        rank = (row["distinct_local_law_rows"], row["minimal_coordinate_count"], row["system_id"])
        if simplest is None or rank < simplest[0]:
            simplest = (rank, row["system_id"])
    return {
        "effective_gate_dimension_counts": {str(key): value for key, value in sorted(by_dimension.items())},
        "families": dict(sorted(families.items())),
        "higher_effective_dimension_can_carry_less_information": higher_dimension_not_more_information,
        "information_by_dimension": information_by_dimension,
        "labelled_law_classes": len(labelled_groups),
        "labelled_law_classes_with_several_orbits": sum(1 for orbits_in_class in labelled_groups.values() if len(orbits_in_class) > 1),
        "local_law_classes": len(class_groups),
        "local_law_classes_with_several_orbits": sum(1 for orbits_in_class in class_groups.values() if len(orbits_in_class) > 1),
        "max_kernel_gap": max(row["kernel_max_abs_gap"] for row in system_rows),
        "max_log_weight_gap": max(row["log_weight_gap"] for row in system_rows),
        "reducibility_counts": {name: by_class.get(name, 0) for name in CLASSES},
        "reducibility_compatible_with_dimension": classes_of_dimension,
        "redundant_rule_systems": redundant,
        "simplest_effective_dimension_2": None if simplest is None else simplest[1],
        "system_count": len(system_rows),
    }
