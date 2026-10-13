"""Generation 8E conjunctive gate grammar.

The census is exact. One rule reads one pair action and two distinct
triad literals, so its expression complexity is K=3 and its rule
cardinality is 1. The W4 grades are evaluation points, not fitted samples.
Structural identity does not include the weight. S4 canonicalisation does
not quotient by bit complement or by weight reciprocity.

Gate coordinates come in two forms. A literal coordinate U is the truth
of the written literal: U = G for ``present`` and U = 1 - G for
``absent``. A raw coordinate G is the triad bit. A discrete difference
in literal coordinates and one in raw coordinates differ by the product
of the literal signs.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

from rs_constraint_lab.constraints import DISSOLVE, FORM, Constraint, parse_expression, structurally_simple
from rs_constraint_lab.explore08d import (
    FACTORS,
    GRADE_FACTOR,
    GRADES,
    N_FULL_STATES,
    N_PAIR_STATES,
    PAIR_SLOT_COUNT,
    SLOT_MAPS,
    SLOTS,
    TRIAD_SLOT_COUNT,
    _balanced_cmi,
    _check_kernel_agreement,
    _effective_gate_dimension,
    _float_laws,
    _law_hash,
    _minimal_coordinates,
    _pair_laws,
    _row_fingerprint,
    fraction_text,
    local_law_class,
    one_rule_catalogue,
    product_weights,
)

EXPERIMENT_ID = "generation-008e-conjunctive-gates"
ANALYSIS_VERSION = "generation-008e-conjunction/v1"
ROUND_ID = "round-e0"
STRUCTURAL_PLACEHOLDER = "neutral"
PROBABILITY_TOLERANCE = 1e-12
CMI_TOLERANCE = 1e-12
INTERACTION_TOLERANCE = 1e-12
COMPARISON_TOLERANCE = 1e-12
BASIS_TOLERANCE = 1e-12
TRIAD_SLOTS = tuple(range(PAIR_SLOT_COUNT, PAIR_SLOT_COUNT + TRIAD_SLOT_COUNT))
D8_SYSTEMS_RELPATH = "constraint-lab/reports/tables/generation-008d-weighted-systems.json"
D8_SYSTEMS_SHA256 = "e5acbf8b02c75bc732d79f9444f820044a7c53a0a4a8ef8191de8d039b238e07"


class ConjunctionError(ValueError):
    """A K3 census invariant did not hold."""


# --- structural universe -------------------------------------------------

Key = tuple  # (polarity, action, ((gate, required), (gate, required)))


def rule_key(rule: Constraint) -> Key:
    return (rule.polarity, rule.action, tuple(rule.conditions))


def constraint_from_key(key: Key, weight: str) -> Constraint:
    polarity, action, conditions = key
    return Constraint(polarity, action, tuple(conditions), weight, ())


def expression_from_key(key: Key, weight: str) -> str:
    return constraint_from_key(key, weight).expression(list(SLOTS))


def structural_expression(key: Key) -> str:
    rendered = expression_from_key(key, STRUCTURAL_PLACEHOLDER)
    suffix = f" => {STRUCTURAL_PLACEHOLDER}"
    if not rendered.endswith(suffix):
        raise ConjunctionError("structural expression did not use the placeholder weight")
    return rendered[: -len(suffix)]


def all_k3_rules() -> tuple[Constraint, ...]:
    rules = []
    for polarity in (FORM, DISSOLVE):
        for action in range(PAIR_SLOT_COUNT):
            for first, second in itertools.combinations(TRIAD_SLOTS, 2):
                for left_required in (0, 1):
                    for right_required in (0, 1):
                        conditions = tuple(sorted(((first, left_required), (second, right_required))))
                        rule = Constraint(polarity, action, conditions, STRUCTURAL_PLACEHOLDER, ())
                        check_k3_rule(rule)
                        rules.append(rule)
    if len(rules) != len({rule_key(rule) for rule in rules}):
        raise ConjunctionError("K3 rules are not unique")
    return tuple(rules)


def check_k3_rule(rule: Constraint) -> None:
    if rule.action >= PAIR_SLOT_COUNT:
        raise ConjunctionError("the action is not a pair slot")
    if rule.counts:
        raise ConjunctionError("a count predicate is present")
    if len(rule.conditions) != 2:
        raise ConjunctionError("the rule does not have two conditions")
    gates = [gate for gate, _required in rule.conditions]
    if any(gate not in TRIAD_SLOTS for gate in gates):
        raise ConjunctionError("a condition is not a triad slot")
    if gates[0] == gates[1]:
        raise ConjunctionError("the two conditions read one triad")
    if list(rule.conditions) != sorted(rule.conditions):
        raise ConjunctionError("the conditions are not in canonical order")
    if rule.k() != 3:
        raise ConjunctionError(f"K is {rule.k()}, not 3")


def _relabel(key: Key, edge_map: tuple[int, ...]) -> Key:
    polarity, action, conditions = key
    return (polarity, edge_map[action], tuple(sorted((edge_map[gate], required) for gate, required in conditions)))


def canonical_key(key: Key) -> Key:
    return min(_relabel(key, edge_map) for edge_map in SLOT_MAPS)


def _face(action: int, gate: int) -> bool:
    return set(SLOTS[action]).issubset(SLOTS[gate])


def describe_rule(key: Key) -> dict:
    polarity, action, conditions = key
    (first, first_required), (second, second_required) = conditions
    faces = [_face(action, first), _face(action, second)]
    shared = tuple(sorted(set(SLOTS[first]) & set(SLOTS[second])))
    if len(shared) != 2:
        raise ConjunctionError("two distinct triads at N=4 do not share a pair")
    face_count = sum(faces)
    incidence = {2: "face_of_both", 1: "face_of_exactly_one", 0: "face_of_neither"}[face_count]
    polarity_relation = "same" if first_required == second_required else "mixed"
    if polarity_relation == "same":
        pattern = "present_present" if first_required else "absent_absent"
    elif face_count == 1:
        face_literal = first_required if faces[0] else second_required
        pattern = "face_present_other_absent" if face_literal else "face_absent_other_present"
    else:
        pattern = "present_absent"
    return {
        "action_direction": "form" if polarity == FORM else "dissolve",
        "action_equals_shared_pair": tuple(SLOTS[action]) == shared,
        "condition_polarities": ["present" if first_required else "absent", "present" if second_required else "absent"],
        "face_flags": faces,
        "incidence_class": incidence,
        "literal_pattern": pattern,
        "literal_polarity_relation": polarity_relation,
    }


def build_universe() -> dict:
    rules = all_k3_rules()
    grouped: dict[Key, list[Key]] = defaultdict(list)
    for rule in rules:
        grouped[canonical_key(rule_key(rule))].append(rule_key(rule))
    orbits = []
    for index, canonical in enumerate(sorted(grouped)):
        if canonical_key(canonical) != canonical:
            raise ConjunctionError("canonicalisation is not idempotent")
        orbit_id = f"K3-{index:02d}"
        systems = [
            {
                "canonical_weighted_rule": expression_from_key(canonical, grade),
                "grade": grade,
                "multiplier": fraction_text(GRADE_FACTOR[grade]),
                "structural_orbit_id": orbit_id,
                "system_id": f"{orbit_id}-{grade}",
            }
            for grade in GRADES
        ]
        orbits.append(
            {
                "canonical_key": canonical,
                "canonical_rule": structural_expression(canonical),
                "descriptors": describe_rule(canonical),
                "orbit_id": orbit_id,
                "orbit_size": len(grouped[canonical]),
                "systems": systems,
            }
        )
    if sum(orbit["orbit_size"] for orbit in orbits) != len(rules):
        raise ConjunctionError("orbit sizes do not sum to the labelled rule count")
    return {
        "labelled_rule_count": len(rules),
        "orbits": orbits,
        "structural_orbit_count": len(orbits),
        "weighted_system_count": sum(len(orbit["systems"]) for orbit in orbits),
    }


_UNIVERSE: dict | None = None


def load_universe() -> dict:
    global _UNIVERSE
    if _UNIVERSE is None:
        _UNIVERSE = build_universe()
    return _UNIVERSE


def universe_public() -> dict:
    universe = load_universe()
    return {
        "labelled_rule_count": universe["labelled_rule_count"],
        "orbits": [
            {
                "canonical_rule": orbit["canonical_rule"],
                "descriptors": orbit["descriptors"],
                "orbit_id": orbit["orbit_id"],
                "orbit_size": orbit["orbit_size"],
            }
            for orbit in universe["orbits"]
        ],
        "structural_orbit_count": universe["structural_orbit_count"],
        "weighted_system_count": universe["weighted_system_count"],
    }


# --- local law -----------------------------------------------------------


def _admissible(key: Key, state: int) -> bool:
    polarity, action, _conditions = key
    present = (state >> action) & 1
    return (polarity == FORM and not present) or (polarity == DISSOLVE and bool(present))


def _literals(key: Key, state: int) -> tuple[int, int]:
    return tuple(int(((state >> gate) & 1) == required) for gate, required in key[2])


def _raw(key: Key, state: int) -> tuple[int, int]:
    return tuple((state >> gate) & 1 for gate, _required in key[2])


def corner_table(key: Key, full_rows, coordinates: str) -> dict[tuple[int, int], Fraction]:
    """Action multiplier on admissible states, keyed by literal or raw gate corner."""
    table: dict[tuple[int, int], Fraction] = {}
    reader = _literals if coordinates == "literal" else _raw
    action = key[1]
    for state, row in enumerate(full_rows):
        if not _admissible(key, state):
            if row[action] != 1:
                raise ConjunctionError("an inadmissible action carries a multiplier")
            continue
        corner = reader(key, state)
        previous = table.get(corner)
        if previous is None:
            table[corner] = row[action]
        elif previous != row[action]:
            raise ConjunctionError("one gate corner carries two multipliers")
    if len(table) != 4:
        raise ConjunctionError("an admissible gate corner is missing")
    return table


def mobius(values: dict[tuple[int, int], float]) -> dict[str, float]:
    """Raw polynomial coefficients of a four-corner table: c + a G1 + b G2 + d G1 G2."""
    c = values[(0, 0)]
    a = values[(1, 0)] - values[(0, 0)]
    b = values[(0, 1)] - values[(0, 0)]
    d = values[(1, 1)] - values[(1, 0)] - values[(0, 1)] + values[(0, 0)]
    return {"a": a, "b": b, "c": c, "d": d}


def reconstruct(coefficients: dict[str, float]) -> dict[tuple[int, int], float]:
    c, a, b, d = coefficients["c"], coefficients["a"], coefficients["b"], coefficients["d"]
    return {(g1, g2): c + a * g1 + b * g2 + d * g1 * g2 for g1 in (0, 1) for g2 in (0, 1)}


def interaction_order(coefficients: dict[str, float], tolerance: float = INTERACTION_TOLERANCE) -> int:
    if abs(coefficients["d"]) > tolerance:
        return 2
    if abs(coefficients["a"]) > tolerance or abs(coefficients["b"]) > tolerance:
        return 1
    return 0


def _log_table(table: dict[tuple[int, int], Fraction]) -> dict[tuple[int, int], float]:
    return {corner: math.log(value.numerator) - math.log(value.denominator) for corner, value in table.items()}


def literal_signs(key: Key) -> tuple[int, int]:
    return tuple(1 if required else -1 for _gate, required in key[2])


def _truth_rows(key: Key, full_rows, laws) -> list[dict]:
    grouped: dict[tuple[int, int, int], list[int]] = defaultdict(list)
    for state in range(N_FULL_STATES):
        u1, u2 = _literals(key, state)
        grouped[(int(_admissible(key, state)), u1, u2)].append(state)
    rows = []
    action = key[1]
    for admissible in (0, 1):
        for u1 in (0, 1):
            for u2 in (0, 1):
                states = grouped[(admissible, u1, u2)]
                law = laws[states[0]]
                multiplier = full_rows[states[0]][action]
                for state in states[1:]:
                    if laws[state] != law or full_rows[state][action] != multiplier:
                        raise ConjunctionError("a truth-table cell contains two laws")
                rows.append(
                    {
                        "action_admissible": bool(admissible),
                        "action_multiplier": fraction_text(multiplier),
                        "active": bool(admissible and u1 and u2),
                        "literal_1_truth": u1,
                        "literal_2_truth": u2,
                        "normalised_slot_law": [fraction_text(item) for item in law],
                        "state_count": len(states),
                    }
                )
    return rows


def k3_law(multiplier: Fraction) -> tuple[Fraction, ...]:
    total = multiplier + PAIR_SLOT_COUNT - 1
    return tuple((multiplier if slot == 0 else Fraction(1)) / total for slot in range(PAIR_SLOT_COUNT))


def _uniform() -> tuple[Fraction, ...]:
    return tuple(Fraction(1, PAIR_SLOT_COUNT) for _ in range(PAIR_SLOT_COUNT))


def _entropy(law) -> float:
    return -sum(p * math.log(p) for p in law if p > 0)


def analytic_balanced_cmi(multiplier: Fraction) -> float:
    """(1/2) JS_(1/4, 3/4)(q_m, q_0): admissible on half the masks, conjunction true on a quarter of triads."""
    active = [float(p) for p in k3_law(multiplier)]
    uniform = [float(p) for p in _uniform()]
    mixture = [0.25 * a + 0.75 * u for a, u in zip(active, uniform, strict=True)]
    weighted_js = _entropy(mixture) - 0.25 * _entropy(active) - 0.75 * _entropy(uniform)
    return 0.5 * weighted_js


def analytic_balanced_drift(multiplier: Fraction, polarity: int) -> Fraction:
    if polarity == DISSOLVE:
        return Fraction(5) * (1 - multiplier) / (Fraction(48) * (multiplier + 5))
    if polarity == FORM:
        return Fraction(5) * (multiplier - 1) / (Fraction(48) * (multiplier + 5))
    raise ConjunctionError("polarity is not form or dissolve")


def enumerated_balanced_drift(laws) -> Fraction:
    """Mean rule-induced change in expected edge count over all 1024 states, against the uniform law."""
    induced = Fraction(0)
    uniform = _uniform()
    for state, law in enumerate(laws):
        mask = state & (N_PAIR_STATES - 1)
        for slot in range(PAIR_SLOT_COUNT):
            sign = -1 if (mask >> slot) & 1 else 1
            induced += (law[slot] - uniform[slot]) * sign
    return induced / N_FULL_STATES


def analyse_system(orbit: dict, system: dict, *, d8_index: dict | None = None) -> dict:
    key = orbit["canonical_key"]
    grade = system["grade"]
    multiplier = GRADE_FACTOR[grade]
    rule = constraint_from_key(key, grade)
    check_k3_rule(rule)
    if not structurally_simple((rule,)):
        raise ConjunctionError("a single rule was rejected as structurally repeated")
    full_rows = product_weights((rule,))
    kernel_gap = _check_kernel_agreement((rule,), full_rows)
    laws = _pair_laws(full_rows)
    action, gates = key[1], tuple(gate for gate, _required in key[2])
    coordinates = _minimal_coordinates(laws, tuple(sorted((action, *gates))))
    dimension = _effective_gate_dimension(laws)
    fingerprints = _row_fingerprint(laws)
    literal_table = corner_table(key, full_rows, "literal")
    raw_table = corner_table(key, full_rows, "raw")
    literal_coefficients = mobius(_log_table(literal_table))
    raw_coefficients = mobius(_log_table(raw_table))
    signs = literal_signs(key)
    log_m = math.log(multiplier.numerator) - math.log(multiplier.denominator)
    expected_raw = log_m * signs[0] * signs[1]
    order = interaction_order(raw_coefficients)
    if interaction_order(literal_coefficients) != order:
        raise ConjunctionError("literal and raw interaction orders disagree")
    for corner, value in literal_table.items():
        expected = multiplier if corner == (1, 1) else Fraction(1)
        if value != expected:
            raise ConjunctionError("the literal truth table is not the single-corner conjunction")
    enumerated_cmi = _balanced_cmi(_float_laws(laws))
    analytic_cmi = analytic_balanced_cmi(multiplier)
    enumerated_drift = enumerated_balanced_drift(laws)
    analytic_drift = analytic_balanced_drift(multiplier, key[0])
    active_states = sum(1 for state in range(N_FULL_STATES) if rule.matches(state, action))
    labelled = _law_hash(full_rows)
    s4_class = local_law_class(full_rows)
    one_rule = one_rule_catalogue().get(labelled)
    comparison = {
        "d8_exact_labelled_match_count": None,
        "d8_exact_s4_match_count": None,
        "one_rule_k2_or_k1_labelled_match": one_rule is not None,
        "symbolic_additive_representable": abs(literal_coefficients["d"]) <= INTERACTION_TOLERANCE,
    }
    if d8_index is not None:
        comparison["d8_exact_labelled_match_count"] = len(d8_index["labelled"].get(labelled, []))
        comparison["d8_exact_s4_match_count"] = len(d8_index["s4"].get(s4_class, []))
    return {
        "active_state_count": active_states,
        "balanced_cmi": enumerated_cmi,
        "balanced_cmi_analytic": analytic_cmi,
        "balanced_cmi_gap": abs(enumerated_cmi - analytic_cmi),
        "balanced_edge_drift": fraction_text(enumerated_drift),
        "balanced_edge_drift_analytic": fraction_text(analytic_drift),
        "canonical_weighted_rule": system["canonical_weighted_rule"],
        "comparison": comparison,
        "distinct_local_law_rows": len(fingerprints),
        "effective_gate_dimension": dimension,
        "gate_interaction_order": order,
        "grade": grade,
        "interaction": {
            "expected_literal_delta12": log_m,
            "expected_raw_delta12": expected_raw,
            "literal_delta12": literal_coefficients["d"],
            "literal_gap": abs(literal_coefficients["d"] - log_m),
            "raw_delta12": raw_coefficients["d"],
            "raw_gap": abs(raw_coefficients["d"] - expected_raw),
            "raw_mobius": raw_coefficients,
        },
        "K": rule.k(),
        "kernel_max_abs_gap": kernel_gap,
        "labelled_law_sha256": labelled,
        "local_law_class": s4_class,
        "minimal_coordinate_count": coordinates["minimal_coordinate_count"],
        "minimal_coordinate_sets": coordinates["all_minimal_coordinate_sets"],
        "multiplier": fraction_text(multiplier),
        "row_fingerprints": fingerprints,
        "rule_cardinality": 1,
        "structural_orbit_id": orbit["orbit_id"],
        "system_id": system["system_id"],
        "truth_table": _truth_rows(key, full_rows, laws),
    }


def load_d8_index(repo: Path) -> dict:
    """Labelled and S4 law hashes of every Generation 8D weighted system, from the committed table."""
    import hashlib

    path = repo / D8_SYSTEMS_RELPATH
    rows = json.loads(path.read_text(encoding="utf-8"))
    from rs_constraint_lab.durable import canonical_json

    digest = hashlib.sha256(canonical_json(rows).encode("utf-8")).hexdigest()
    if digest != D8_SYSTEMS_SHA256:
        raise ConjunctionError("the committed Generation 8D weighted-system table does not match its recorded hash")
    labelled: dict[str, list[str]] = defaultdict(list)
    s4: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        labelled[row["labelled_law_sha256"]].append(row["system_id"])
        s4[row["local_law_class"]].append(row["system_id"])
    return {"labelled": dict(labelled), "s4": dict(s4), "system_count": len(rows), "table_sha256": digest}


def analyse_orbit(orbit_id: str, *, d8_index: dict | None = None) -> dict:
    universe = load_universe()
    orbit = next(item for item in universe["orbits"] if item["orbit_id"] == orbit_id)
    return {
        "canonical_rule": orbit["canonical_rule"],
        "descriptors": orbit["descriptors"],
        "orbit_id": orbit_id,
        "orbit_size": orbit["orbit_size"],
        "systems": [analyse_system(orbit, system, d8_index=d8_index) for system in orbit["systems"]],
    }


# --- algebra items -------------------------------------------------------

CORNERS = ((0, 0), (1, 0), (0, 1), (1, 1))


def _rank(rows: list[list[Fraction]]) -> int:
    matrix = [list(row) for row in rows]
    rank = 0
    columns = len(matrix[0]) if matrix else 0
    for column in range(columns):
        pivot = next((r for r in range(rank, len(matrix)) if matrix[r][column] != 0), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        for r in range(len(matrix)):
            if r != rank and matrix[r][column] != 0:
                factor = matrix[r][column] / matrix[rank][column]
                matrix[r] = [x - factor * y for x, y in zip(matrix[r], matrix[rank], strict=True)]
        rank += 1
    return rank


def symbolic_additive_comparison() -> dict:
    """Exact rank argument over the rationals.

    Over the four literal corners, the additive one-literal features span
    {1, U1, U2}. The conjunction U1 U2 is outside that span, so
    c U1 U2 = c0 + a U1 + b U2 on all four corners forces c = 0. The
    argument holds for every real c, a, b and c0, not only W4 values.
    """
    def features(u1, u2):
        return [Fraction(1), Fraction(u1), Fraction(u2)]

    design = [features(u1, u2) for u1, u2 in CORNERS]
    with_conjunction = [features(u1, u2) + [Fraction(u1 * u2)] for u1, u2 in CORNERS]
    without_constant = [[Fraction(u1), Fraction(u2)] for u1, u2 in CORNERS]
    without_constant_aug = [[Fraction(u1), Fraction(u2), Fraction(u1 * u2)] for u1, u2 in CORNERS]
    result = {
        "additive_with_constant_rank": _rank(design),
        "additive_with_constant_plus_conjunction_rank": _rank(with_conjunction),
        "additive_without_constant_rank": _rank(without_constant),
        "additive_without_constant_plus_conjunction_rank": _rank(without_constant_aug),
        "delta12_of_additive_features": [
            fraction_text(f[3] - f[1] - f[2] + f[0])
            for f in zip(*[features(u1, u2) for u1, u2 in CORNERS], strict=True)
        ],
        "delta12_of_conjunction": fraction_text(Fraction(1 * 1) - 0 - 0 + 0),
        "statement": "c U1 U2 = c0 + a U1 + b U2 on all four literal corners implies c = 0",
    }
    if result["additive_with_constant_plus_conjunction_rank"] != result["additive_with_constant_rank"] + 1:
        raise ConjunctionError("the conjunction lies in the additive span")
    if result["additive_without_constant_plus_conjunction_rank"] != result["additive_without_constant_rank"] + 1:
        raise ConjunctionError("the conjunction lies in the span of two one-literal features")
    if any(value != "0/1" for value in result["delta12_of_additive_features"]):
        raise ConjunctionError("an additive feature has a non-zero second difference")
    return result


BASIS_EXAMPLES = (
    {"name": "conjunction", "table": {(0, 0): "0", (1, 0): "0", (0, 1): "0", (1, 1): "1"}},
    {"name": "xor", "table": {(0, 0): "0", (1, 0): "1", (0, 1): "1", (1, 1): "0"}},
    {"name": "xnor", "table": {(0, 0): "1", (1, 0): "0", (0, 1): "0", (1, 1): "1"}},
    {"name": "additive", "table": {(0, 0): "1/3", (1, 0): "5/6", (0, 1): "-2/3", (1, 1): "-1/6"}},
    {"name": "generic", "table": {(0, 0): "2", (1, 0): "-7/5", (0, 1): "3/11", (1, 1): "19/4"}},
)

# Corner indicators as raw polynomials: coefficients of (1, G1, G2, G1G2).
CORNER_POLYNOMIALS = {
    (0, 0): (1, -1, -1, 1),
    (1, 0): (0, 1, 0, -1),
    (0, 1): (0, 0, 1, -1),
    (1, 1): (0, 0, 0, 1),
}


def _det4(matrix: list[list[Fraction]]) -> Fraction:
    if len(matrix) == 1:
        return matrix[0][0]
    total = Fraction(0)
    for column in range(len(matrix)):
        minor = [row[:column] + row[column + 1:] for row in matrix[1:]]
        total += (-1) ** column * matrix[0][column] * _det4(minor)
    return total


def basis_items() -> dict:
    rows = []
    for example in BASIS_EXAMPLES:
        table = {corner: Fraction(value) for corner, value in example["table"].items()}
        coefficients = mobius(table)
        rebuilt = reconstruct(coefficients)
        polynomial_from_corners = [Fraction(0)] * 4
        for corner, value in table.items():
            for index, weight in enumerate(CORNER_POLYNOMIALS[corner]):
                polynomial_from_corners[index] += value * weight
        corners_from_polynomial = {
            corner: sum(
                (Fraction(coefficient) * term(corner) for coefficient, term in zip(
                    (coefficients["c"], coefficients["a"], coefficients["b"], coefficients["d"]),
                    (lambda k: 1, lambda k: k[0], lambda k: k[1], lambda k: k[0] * k[1]),
                    strict=True,
                )),
                Fraction(0),
            )
            for corner in CORNERS
        }
        gap = max(abs(rebuilt[corner] - table[corner]) for corner in CORNERS)
        rows.append(
            {
                "corner_coefficients": {f"{g1}{g2}": fraction_text(table[(g1, g2)]) for g1, g2 in CORNERS},
                "corner_to_polynomial": [fraction_text(item) for item in polynomial_from_corners],
                "interaction_order": interaction_order({k: float(v) for k, v in coefficients.items()}),
                "mobius_coefficients": {k: fraction_text(v) for k, v in coefficients.items()},
                "name": example["name"],
                "polynomial_to_corner_gap": fraction_text(max(abs(corners_from_polynomial[c] - table[c]) for c in CORNERS)),
                "reconstruction_gap": fraction_text(gap),
                "truth_table": {f"{g1}{g2}": fraction_text(table[(g1, g2)]) for g1, g2 in CORNERS},
            }
        )
        if gap != 0 or polynomial_from_corners != [coefficients["c"], coefficients["a"], coefficients["b"], coefficients["d"]]:
            raise ConjunctionError(f"basis reconstruction failed on {example['name']}")
    matrix = [[Fraction(x) for x in CORNER_POLYNOMIALS[corner]] for corner in CORNERS]
    determinant = _det4(matrix)
    if determinant == 0:
        raise ConjunctionError("the corner indicators are not a basis")
    return {"corner_polynomial_determinant": fraction_text(determinant), "corner_polynomials": {f"{g1}{g2}": list(CORNER_POLYNOMIALS[(g1, g2)]) for g1, g2 in CORNERS}, "examples": rows}


def w4_coverage() -> dict:
    """Four-corner tables reachable with at most one W4 rule per basis element, in log2 units."""
    levels = (0, -2, -1, 1, 2)  # absent rule, then the W4 grades as powers of 2
    corner = {(l00, l10, l01, l11) for l00 in levels for l10 in levels for l01 in levels for l11 in levels}
    polynomial = set()
    for c in levels:
        for a in levels:
            for b in levels:
                for d in levels:
                    polynomial.add((c, c + a, c + b, c + a + b + d))
    return {
        "corner_basis_tables": len(corner),
        "intersection_tables": len(corner & polynomial),
        "note": "Each basis element carries no rule or one W4 rule. Values are log2 action multipliers at corners (00, 10, 01, 11).",
        "polynomial_basis_tables": len(polynomial),
        "polynomial_only_tables": len(polynomial - corner),
        "corner_only_tables": len(corner - polynomial),
        "polynomial_max_abs_log2_corner": max(max(abs(x) for x in table) for table in polynomial),
    }


def _two_rule_gate_table(rules: tuple[Constraint, ...], action: int, gates: tuple[int, int]) -> dict:
    full_rows = product_weights(rules)
    gap = _check_kernel_agreement(rules, full_rows)
    table: dict[tuple[int, int], Fraction] = {}
    polarity = rules[0].polarity
    for state, row in enumerate(full_rows):
        present = (state >> action) & 1
        admissible = (polarity == FORM and not present) or (polarity == DISSOLVE and present)
        if not admissible:
            if any(weight != 1 for weight in row):
                raise ConjunctionError("an inadmissible state carries a multiplier")
            continue
        if any(weight != 1 for slot, weight in enumerate(row) if slot != action):
            raise ConjunctionError("a non-action slot carries a multiplier")
        corner = ((state >> gates[0]) & 1, (state >> gates[1]) & 1)
        if table.setdefault(corner, row[action]) != row[action]:
            raise ConjunctionError("one gate corner carries two multipliers")
    return {"kernel_gap": gap, "table": table}


def boolean_constructions() -> dict:
    """Targeted two-rule and four-rule K3 constructions on one action. Not a census."""
    action, gates = 0, (TRIAD_SLOTS[0], TRIAD_SLOTS[1])
    results = []
    for polarity in (FORM, DISSOLVE):
        for grade in GRADES:
            m = GRADE_FACTOR[grade]
            xor = (
                Constraint(polarity, action, ((gates[0], 1), (gates[1], 0)), grade, ()),
                Constraint(polarity, action, ((gates[0], 0), (gates[1], 1)), grade, ()),
            )
            xnor = (
                Constraint(polarity, action, ((gates[0], 1), (gates[1], 1)), grade, ()),
                Constraint(polarity, action, ((gates[0], 0), (gates[1], 0)), grade, ()),
            )
            for name, rules, expected in (
                ("xor", xor, {(0, 0): Fraction(1), (1, 0): m, (0, 1): m, (1, 1): Fraction(1)}),
                ("xnor", xnor, {(0, 0): m, (1, 0): Fraction(1), (0, 1): Fraction(1), (1, 1): m}),
            ):
                if not structurally_simple(rules):
                    raise ConjunctionError(f"{name} rules were rejected as repeated")
                measured = _two_rule_gate_table(rules, action, gates)
                if measured["table"] != expected:
                    raise ConjunctionError(f"{name} construction does not select the expected corners")
                logs = _log_table(measured["table"])
                coefficients = mobius(logs)
                results.append(
                    {
                        "action_direction": "form" if polarity == FORM else "dissolve",
                        "construction": name,
                        "gate_table": {f"{g1}{g2}": fraction_text(v) for (g1, g2), v in sorted(measured["table"].items())},
                        "grade": grade,
                        "interaction_order": interaction_order(coefficients),
                        "kernel_gap": measured["kernel_gap"],
                        "raw_mobius": coefficients,
                        "rules": [rule.expression(list(SLOTS)) for rule in rules],
                    }
                )
    corner_grades = {(0, 0): "strong_suppress", (0, 1): "weak_suppress", (1, 0): "weak_favour", (1, 1): "strong_favour"}
    four = tuple(
        Constraint(DISSOLVE, action, ((gates[0], g1), (gates[1], g2)), grade, ())
        for (g1, g2), grade in corner_grades.items()
    )
    if not structurally_simple(four):
        raise ConjunctionError("four corner rules were rejected as repeated")
    measured = _two_rule_gate_table(four, action, gates)
    expected = {corner: GRADE_FACTOR[grade] for corner, grade in corner_grades.items()}
    if measured["table"] != expected:
        raise ConjunctionError("the four corner rules do not assign independent multipliers")
    return {
        "constructions": results,
        "four_corner": {
            "gate_table": {f"{g1}{g2}": fraction_text(v) for (g1, g2), v in sorted(measured["table"].items())},
            "kernel_gap": measured["kernel_gap"],
            "rules": [rule.expression(list(SLOTS)) for rule in four],
        },
        "placement": {"action": "-".join(map(str, SLOTS[action])), "gates": ["-".join(map(str, SLOTS[g])) for g in gates]},
    }


def general_conjunction_check() -> dict:
    """Targeted check of the r-literal monomial law for r = 1..4 on one placement. Not a census."""
    action = 0
    rows = []
    for r in range(1, TRIAD_SLOT_COUNT + 1):
        gates = TRIAD_SLOTS[:r]
        for literals in itertools.product((0, 1), repeat=r):
            conditions = tuple(sorted(zip(gates, literals)))
            rule = Constraint(DISSOLVE, action, conditions, "strong_favour", ())
            full_rows = product_weights((rule,))
            _check_kernel_agreement((rule,), full_rows)
            table: dict[tuple[int, ...], float] = {}
            for state, row in enumerate(full_rows):
                if not (state >> action) & 1:
                    continue
                corner = tuple((state >> gate) & 1 for gate in gates)
                value = math.log(row[action].numerator) - math.log(row[action].denominator)
                if table.setdefault(corner, value) != value:
                    raise ConjunctionError("one raw corner carries two values")
            # Top Moebius coefficient: sum over corners of (-1)^(r - |S|) L(S).
            top = sum((-1) ** (r - sum(corner)) * value for corner, value in table.items())
            signs = 1
            for required in literals:
                signs *= 1 if required else -1
            expected = math.log(4) * signs
            rows.append(
                {
                    "K": rule.k(),
                    "literals": ["present" if x else "absent" for x in literals],
                    "r": r,
                    "top_coefficient": top,
                    "top_coefficient_expected": expected,
                    "gap": abs(top - expected),
                }
            )
            if abs(top - expected) > INTERACTION_TOLERANCE or rule.k() != r + 1:
                raise ConjunctionError("the r-literal monomial law did not hold")
    return {"grade": "strong_favour", "rows": rows}


def k3_surface() -> dict:
    """Analytic K3 balanced information and drift at the four W4 grades, beside the K2 one-gate values."""
    from rs_constraint_lab.explore08c import analytic_balanced_cmi as k2_cmi
    from rs_constraint_lab.explore08d import balanced_drift_formula as k2_drift

    predicted = {
        "strong_suppress": 0.006761384413735834,
        "weak_suppress": 0.002333270369315642,
        "weak_favour": 0.003961514536995468,
        "strong_favour": 0.018447186631125900,
    }
    rows = []
    for grade in GRADES:
        m = GRADE_FACTOR[grade]
        k3 = analytic_balanced_cmi(m)
        rows.append(
            {
                "grade": grade,
                "k2_balanced_cmi": k2_cmi(m),
                "k2_dissolve_drift": fraction_text(k2_drift(m, DISSOLVE)),
                "k3_balanced_cmi": k3,
                "k3_dissolve_drift": fraction_text(analytic_balanced_drift(m, DISSOLVE)),
                "k3_form_drift": fraction_text(analytic_balanced_drift(m, FORM)),
                "k3_over_k2_cmi": k3 / k2_cmi(m),
                "k3_over_k2_drift": fraction_text(analytic_balanced_drift(m, DISSOLVE) / k2_drift(m, DISSOLVE)),
                "multiplier": fraction_text(m),
                "review_prediction_cmi": predicted[grade],
                "review_prediction_gap": abs(k3 - predicted[grade]),
            }
        )
    return {"rows": rows}


def parser_semantics() -> dict:
    """What the order-3 parser does with two triad conditions."""
    two = parse_expression("dissolve(0-1) | present(0-1-3) & present(0-1-2) => strong_favour", 4, order=3)
    out = {
        "conditions": [list(c) for c in two.conditions],
        "conditions_sorted": list(two.conditions) == sorted(two.conditions),
        "counts": list(two.counts),
        "k": two.k(),
    }
    try:
        parse_expression("dissolve(0-1) | present(0-1-2) & present(0-1-2) => strong_favour", 4, order=3)
        out["repeated_literal_rejected"] = False
    except ValueError:
        out["repeated_literal_rejected"] = True
    contradictory = parse_expression("dissolve(0-1) | present(0-1-2) & absent(0-1-2) => strong_favour", 4, order=3)
    out["contradictory_same_triad_accepted"] = True
    out["contradictory_same_triad_matches"] = sum(1 for s in range(N_FULL_STATES) if contradictory.matches(s, contradictory.action))
    try:
        parse_expression("dissolve(0-1) | present(0-1) => strong_favour", 4, order=3)
        out["action_slot_condition_rejected"] = False
    except ValueError:
        out["action_slot_condition_rejected"] = True
    try:
        parse_expression("dissolve(0-1) | present(0-1-2) & count>=2 => strong_favour", 4, order=3)
        out["count_predicate_rejected"] = False
    except ValueError:
        out["count_predicate_rejected"] = True
    return out


def census_summary(systems: list[dict], orbits: list[dict]) -> dict:
    cmi_groups: dict[tuple, set] = defaultdict(set)
    for system in systems:
        orbit = next(o for o in orbits if o["orbit_id"] == system["structural_orbit_id"])
        key = (system["grade"], orbit["descriptors"]["literal_polarity_relation"], orbit["descriptors"]["incidence_class"])
        cmi_groups[key].add(round(system["balanced_cmi"], 11))
    by_grade: dict[str, set] = defaultdict(set)
    for system in systems:
        by_grade[system["grade"]].add(round(system["balanced_cmi"], 11))
    return {
        "active_state_counts": dict(Counter(s["active_state_count"] for s in systems)),
        "distinct_cmi_values_by_grade": {g: len(v) for g, v in by_grade.items()},
        "distinct_local_law_rows": dict(Counter(s["distinct_local_law_rows"] for s in systems)),
        "effective_gate_dimension": dict(Counter(s["effective_gate_dimension"] for s in systems)),
        "gate_interaction_order": dict(Counter(s["gate_interaction_order"] for s in systems)),
        "max_balanced_cmi_gap": max(s["balanced_cmi_gap"] for s in systems),
        "max_kernel_gap": max(s["kernel_max_abs_gap"] for s in systems),
        "max_literal_delta12_gap": max(s["interaction"]["literal_gap"] for s in systems),
        "max_raw_delta12_gap": max(s["interaction"]["raw_gap"] for s in systems),
        "minimal_coordinate_count": dict(Counter(s["minimal_coordinate_count"] for s in systems)),
        "drift_formula_matches": all(s["balanced_edge_drift"] == s["balanced_edge_drift_analytic"] for s in systems),
        "d8_labelled_matches": sum(s["comparison"]["d8_exact_labelled_match_count"] or 0 for s in systems),
        "d8_s4_matches": sum(s["comparison"]["d8_exact_s4_match_count"] or 0 for s in systems),
        "one_rule_matches": sum(1 for s in systems if s["comparison"]["one_rule_k2_or_k1_labelled_match"]),
        "symbolic_additive_representable": sum(1 for s in systems if s["comparison"]["symbolic_additive_representable"]),
        "placement_groups_with_one_cmi": sum(1 for v in cmi_groups.values() if len(v) == 1),
        "placement_groups": len(cmi_groups),
        "local_law_classes": len({s["local_law_class"] for s in systems}),
        "labelled_law_classes": len({s["labelled_law_sha256"] for s in systems}),
        "system_count": len(systems),
    }
