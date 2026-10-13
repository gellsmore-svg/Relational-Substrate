"""Deterministic Generation 8F matched-control interaction bridge."""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import permutations

import numpy as np

from rs_constraint_lab.constraints import DISSOLVE, FORM, Choreography, Constraint
from rs_constraint_lab.durable import canonical_json, sha256_bytes
from rs_constraint_lab.exact import period_of, strongly_connected_components
from rs_constraint_lab.explore08 import CLASS_NAMES, CLASS_OF_MASK, plan_hash, source_masks
from rs_constraint_lab.explore08b import (
    _cmi_from_joint, epoch_landing, pair_slot_laws, stationary_slot_cmi,
)
from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.kernel import Kernel, build_kernel
from rs_constraint_lab.state import edges, relation_slots

EXPERIMENT_ID = "generation-008f-interaction-to-topology-bridge"
ANALYSIS_VERSION = "generation-008f-bridge/v2"
ROUND_ID = "round-f0"
CHECKPOINTS = (1, 2, 4, 8, 16, 32, 64)
SOURCES = ("star", "path", "triangle")
MOTIFS = ("BOTH", "ONE", "NEITHER")
DIRECTIONS = ("form", "dissolve")
GRADES = {"strong_suppress": Fraction(1, 4), "strong_favour": Fraction(4)}
COMPARATORS = ("ENDPOINT", "PROJECTION", "DRIFT")
DECIMAL_DIGITS = 80
N_PAIR_STATES, N_TRIAD_STATES, N_FULL_STATES = 64, 16, 1024
PAIR_SLOTS = 6
ONTOLOGY = {"G": 0, "H": 0, "L": 0, "N": 4, "O": 3, "S": 0, "hypergraph": "independent"}
TOLERANCES = {
    "rational_local_probability": 1e-15,
    "float_local_probability_gap": 1e-13,
    "kernel_row_sum": 1e-12,
    "epoch_solve_residual": 1e-11,
    "stationary_residual": 1e-11,
    "stationary_nonnegative": 1e-13,
    "information_chain_rule": 1e-12,
    "drift_balanced_action_match": 1e-14,
    "logit_second_difference": 1e-13,
    "conjugacy": 1e-12,
    "information_floor": 1e-12,
}


class BridgeError(RuntimeError):
    """A construction or numerical validation failed."""


@dataclass(frozen=True)
class LawSpec:
    target_id: str
    model: str
    incidence_motif: str
    direction: str
    grade: str
    m: str
    action_pair: int
    condition_triads: tuple[int, int]
    weights: tuple[tuple[str, str], ...]
    literal_polarities: tuple[int, int] = (1, 1)


def slots() -> tuple[tuple[int, ...], ...]:
    return tuple(relation_slots(4, 3))


def relation_name(slot: int) -> str:
    return "-".join(map(str, slots()[slot]))


def path_middle_action() -> int:
    mask = source_masks()["path"]
    pairs = edges(4)
    degrees = [sum((mask >> i) & 1 for i, edge in enumerate(pairs) if v in edge) for v in range(4)]
    choices = [i for i, edge in enumerate(pairs) if (mask >> i) & 1 and all(degrees[v] == 2 for v in edge)]
    if len(choices) != 1:
        raise BridgeError("canonical path has no unique middle edge")
    return choices[0]


def condition_triads(action: int, motif: str) -> tuple[int, int]:
    containing = tuple(i for i in range(6, 10) if set(slots()[action]) <= set(slots()[i]))
    other = tuple(i for i in range(6, 10) if i not in containing)
    if len(containing) != 2 or len(other) != 2:
        raise BridgeError("N=4 incidence changed")
    return {"BOTH": containing, "ONE": (containing[0], other[0]), "NEITHER": other}[motif]


def drift_root(m: Fraction) -> dict:
    """Monotonicity gives a unique positive root, including r=1 at m=1."""
    with localcontext() as context:
        context.prec = DECIMAL_DIGITS
        md = Decimal(m.numerator) / Decimal(m.denominator)

        def p(x):
            return x / (x + 5)

        def f(r):
            return 2 * p(r) + p(r * r) - 2 * p(Decimal(1)) - p(md)

        lo, hi = Decimal(0), max(Decimal(2), md)
        initial = [str(lo), str(hi)]
        while f(hi) < 0:
            hi *= 2
        for _ in range(320):
            mid = (lo + hi) / 2
            if mid == lo or mid == hi:
                break
            if f(mid) < 0:
                lo = mid
            else:
                hi = mid
        root = (lo + hi) / 2
        residual = abs(f(root)) / 4
        return {
            "root_decimal": str(root), "root_float": float(root),
            "initial_bracket": initial, "final_bracket": [str(lo), str(hi)],
            "solver": "monotone Decimal bisection, maximum 320 iterations",
            "precision_digits": DECIMAL_DIGITS, "residual_decimal": str(residual),
            "residual_tolerance": "1e-70",
        }


def reference_weights(m: Fraction, roots: dict, grade: str) -> dict:
    with localcontext() as context:
        context.prec = DECIMAL_DIGITS
        md = Decimal(m.numerator) / Decimal(m.denominator)
        root = roots[grade]["root_decimal"]
        half = md.sqrt()
        return {
            "K3": (("k3", str(md)),),
            "ENDPOINT": (("u1", str(half)), ("u2", str(half))),
            "PROJECTION": (("unconditional", str(1 / half.sqrt())), ("u1", str(half)), ("u2", str(half))),
            "DRIFT": (("u1", root), ("u2", root)),
        }


def all_laws(roots: dict) -> list[LawSpec]:
    laws = []
    action = path_middle_action()
    for motif in MOTIFS:
        for direction in DIRECTIONS:
            for grade, m in GRADES.items():
                target_id = f"F0-{motif}-{direction}-{grade}"
                for model, weights in reference_weights(m, roots, grade).items():
                    laws.append(LawSpec(target_id, model, motif, direction, grade, str(m), action, condition_triads(action, motif), weights))
    return laws


def local_multiplier_fraction(law: LawSpec, u1: int, u2: int) -> Fraction:
    value = Fraction(1)
    active = {"k3": bool(u1 and u2), "u1": bool(u1), "u2": bool(u2), "unconditional": True}
    for role, weight in law.weights:
        if active[role]:
            value *= Fraction(weight)
    return value


def local_table(law: LawSpec) -> dict:
    fractions = [local_multiplier_fraction(law, *corner) for corner in ((0, 0), (1, 0), (0, 1), (1, 1))]
    probabilities = [w / (w + 5) for w in fractions]
    with localcontext() as context:
        context.prec = DECIMAL_DIGITS
        multiplier = [Decimal(w.numerator) / Decimal(w.denominator) for w in fractions]
        logs = [w.ln() for w in multiplier]
        c = (Decimal(Fraction(law.m).numerator) / Decimal(Fraction(law.m).denominator)).ln()
        delta = logs[3] - logs[1] - logs[2] + logs[0]
        expected = c if law.model == "K3" else Decimal(0)
        if abs(delta - expected) > Decimal("1e-70"):
            raise BridgeError("comparator second difference failed")
        log_reference = [str(x) for x in logs]
        delta_reference = str(delta)
    joint = np.zeros((4, 6, 1))
    for corner, w in enumerate(fractions):
        row = np.full(6, float(1 / (w + 5)))
        row[law.action_pair] = float(w / (w + 5))
        joint[corner, :, 0] = row / 4
    probability = sum(probabilities, Fraction(0)) / 4
    # Over all pair masks, only half admit this direction. The other five
    # toggles average zero net edge change; the affected toggle changes sign.
    drift = (probability - Fraction(1, 6)) / 2
    if law.direction == "dissolve":
        drift = -drift
    return {
        "corner_order": ["00", "10", "01", "11"],
        "action_log_multiplier_reference": log_reference,
        "action_log_multiplier": [float(x) for x in log_reference],
        "action_multiplier_reference": [str(x) for x in multiplier],
        "action_multiplier": [float(x) for x in fractions],
        "six_slot_action_probability": [float(x) for x in probabilities],
        "six_slot_action_probability_fraction": [str(x) for x in probabilities],
        "local_delta12": float(delta_reference), "local_delta12_reference": delta_reference,
        "balanced_action_probability": float(probability),
        "balanced_CMI": 0.5 * _cmi_from_joint(joint),
        "balanced_edge_drift": float(drift),
    }


def law_record(law: LawSpec) -> dict:
    return {
        "target_id": law.target_id, "model": law.model,
        "comparator": None if law.model == "K3" else law.model,
        "incidence_motif": law.incidence_motif, "direction": law.direction,
        "grade": law.grade, "m": law.m, "action_pair": law.action_pair,
        "action_pair_name": relation_name(law.action_pair),
        "condition_triads": list(law.condition_triads),
        "condition_triad_names": [relation_name(x) for x in law.condition_triads],
        "literal_polarities": list(law.literal_polarities),
        "comparator_parameters": dict(law.weights),
    }


def law_identity(law: LawSpec) -> dict:
    return {
        "action": law.action_pair, "direction": law.direction,
        "gates": list(law.condition_triads), "polarities": list(law.literal_polarities),
        "weights": dict(law.weights),
    }


def law_fingerprint(law: LawSpec) -> str:
    return sha256_bytes(canonical_json(law_identity(law)).encode())


def canonical_law(law: LawSpec) -> LawSpec:
    return replace(law, condition_triads=(6, 7))


def canonical_fingerprint(law: LawSpec) -> str:
    return law_fingerprint(canonical_law(law))


def s4_fingerprint(law: LawSpec) -> str:
    index = {slot: i for i, slot in enumerate(slots())}
    images = []
    for permutation in permutations(range(4)):
        mapping = [index[tuple(sorted(permutation[v] for v in slot))] for slot in slots()]
        image = replace(law, action_pair=mapping[law.action_pair], condition_triads=tuple(sorted(mapping[t] for t in law.condition_triads)))
        images.append(canonical_json(law_identity(image)))
    return sha256_bytes(min(images).encode())


def raw_to_canonical(law: LawSpec) -> np.ndarray:
    order = list(law.condition_triads) + [i for i in range(6, 10) if i not in law.condition_triads]
    state = np.arange(1024)
    mapped = state & 63
    for destination, original in enumerate(order, 6):
        mapped |= ((state >> original) & 1) << destination
    return mapped


def source_topology_table() -> list[dict]:
    action = path_middle_action()
    rows = []
    for source, mask in source_masks().items():
        present = bool((mask >> action) & 1)
        category = {"star": "star_spoke", "path": "path_middle_edge", "triangle": "triangle_edge"}[source]
        rows.append({
            "source": source, "pair_mask": mask, "action_pair": action,
            "action_pair_name": relation_name(action), "action_present": present,
            "action_topology_category": category if present else "absent_pair",
            "form_admissible": not present, "dissolve_admissible": present,
        })
    return rows


def polarity_prerequisite() -> dict:
    return {
        "holds_structurally": True,
        "map": "state xor (1 << second_condition_triad)",
        "proof": "Triad toggles have state-independent weight 1. Bit complementation preserves each toggle and every pair bit. Flipping the corresponding required literal preserves all active rule weights, normalisation and successors. Consequently it conjugates the full and pair-event kernels, preserves uniform raw-triad starts and stationary visible marginals.",
        "numeric_checks": "after freeze, PP versus PA on BOTH for both strong grades",
        "pre_freeze_actual_target_kernels": 0,
    }


def prepare_f0_plan() -> dict:
    roots = {grade: drift_root(m) for grade, m in GRADES.items()}
    laws = all_laws(roots)
    local = [{**law_record(law), **local_table(law)} for law in laws]
    document = {
        "schema": "rs-constraint-lab.bridge-plan/v2", "experiment_id": EXPERIMENT_ID,
        "analysis_version": ANALYSIS_VERSION, "round_id": ROUND_ID, "mode": "B",
        "ontology": ONTOLOGY, "stochastic_trajectories": False,
        "decimal_digits": DECIMAL_DIGITS, "drift_roots": roots,
        "source_topology": source_topology_table(), "checkpoints": list(CHECKPOINTS),
        "laws": [law_record(law) for law in laws], "local_matching": local,
        "fingerprints": [
            {"target_id": law.target_id, "model": law.model,
             "labelled": law_fingerprint(law), "s4": s4_fingerprint(law),
             "hidden_permutation_canonical": canonical_fingerprint(law),
             "raw_to_canonical_triad_order": list(law.condition_triads) + [i for i in range(6, 10) if i not in law.condition_triads]}
            for law in laws
        ],
        "polarity_conjugacy": polarity_prerequisite(),
        "pre_freeze_exposure": {
            "actual_scientific_target_kernels": [], "actual_scientific_cells": [],
            "allowed": ["symbolic local tables", "80-digit root and multiplier construction", "law specification fingerprints", "structural conjugacy proof", "historical/synthetic propagation and timing"],
            "prompt_storage_deviation": "unexecuted preliminary draft preceded prompt transcription; see Execution 008F",
        },
        "tolerances": TOLERANCES,
        "estimands": ["binary model JS at pair-mask, class and edge-count projections", "conditional shape and label CMI", "stationary pair-event occupancy", "secondary full-event stationary pair-weighted slot CMI"],
        "numeric_method": {
            "weights": "exact Fractions for W4; exact rational representations of frozen 80-digit Decimal approximations for continuous comparators",
            "kernel_analysis": "float64, cross-checked against frozen high-precision local reference",
            "epoch": "existing Generation 8B block landing solve; residual (I-T)E-R checked independently",
            "stationary": "normalised linear solve after communicating-structure and period checks, no arbitrary class weighting",
            "symmetry": "16 hidden-bit-permutation canonical laws; pairs fixed, raw 16-state prior retained. 48 labelled laws and S4 classes remain separately recorded.",
            "cache": ["law fingerprint", "analysis version", "80-digit weights/float64 matrices"],
        },
        "execution": {
            "worker_count": 1, "atomic_item": "one canonical law and its three source propagation blocks",
            "watchdog_seconds": 120, "heartbeat_seconds": 5, "resume": True,
            "expected_wall_seconds": [30, 120], "expected_disk_bytes": 160000000,
            "calibration": "historical R01, with single BLAS thread; actual timing stored separately before freeze",
        },
        "work_count": {
            "targets": 12, "comparators_per_target": 3, "labelled_laws": len({law_fingerprint(x) for x in laws}),
            "s4_laws": len({s4_fingerprint(x) for x in laws}),
            "unique_law_count": len({canonical_fingerprint(x) for x in laws}),
            "unique_full_kernels": len({canonical_fingerprint(x) for x in laws}),
            "unique_pair_event_kernels": len({canonical_fingerprint(x) for x in laws}),
            "labelled_kernel_materialisations": len(laws), "source_law_blocks": 16 * 3,
            "source_checkpoint_distribution_cells": 16 * 3 * len(CHECKPOINTS),
            "labelled_source_checkpoint_distribution_cells": len(laws) * 3 * len(CHECKPOINTS),
            "source_comparison_blocks": 12 * 3 * 3,
            "source_checkpoint_comparison_cells": 12 * 3 * 3 * len(CHECKPOINTS),
            "stationary_comparison_cells": 12 * 3,
            "conjugacy_prerequisite_checks": 2,
        },
    }
    document["plan_hash"] = plan_hash(document)
    return document


def rule_constraints(law: LawSpec) -> tuple[Constraint, ...]:
    requirements = dict(zip(("u1", "u2"), zip(law.condition_triads, law.literal_polarities), strict=True))
    output = []
    for role, _ in law.weights:
        conditions = tuple(requirements.values()) if role == "k3" else () if role == "unconditional" else (requirements[role],)
        output.append(Constraint(FORM if law.direction == "form" else DISSOLVE, law.action_pair, conditions, role, ()))
    return tuple(output)


def build_law_kernel(law: LawSpec) -> Kernel:
    return build_kernel(4, Choreography(0, 0, rule_constraints(law)), {role: Fraction(value) for role, value in law.weights}, relation_slots=slots())


def full_transition_matrix(kernel: Kernel) -> np.ndarray:
    matrix = np.zeros((kernel.n_states, kernel.n_states))
    for state, row in enumerate(kernel.successors):
        for target, probability in row:
            matrix[state, target] = float(probability)
    return matrix


def reference_probability_gap(law: LawSpec, kernel: Kernel) -> dict:
    full_gap, pair_gap = 0.0, 0.0
    for state, weights in enumerate(kernel.weights):
        literals = [int(((state >> bit) & 1) == polarity) for bit, polarity in zip(law.condition_triads, law.literal_polarities, strict=True)]
        admissible = bool((state >> law.action_pair) & 1) == (law.direction == "dissolve")
        w = local_multiplier_fraction(law, *literals) if admissible else Fraction(1)
        if weights[law.action_pair] != w:
            raise BridgeError("exact reference weight disagrees with kernel")
        for slot in range(10):
            expected = (w if slot == law.action_pair else Fraction(1)) / (w + 9)
            rounded = Fraction.from_float(float(kernel.probability(state, state ^ (1 << slot))))
            full_gap = max(full_gap, float(abs(expected - rounded)))
            if slot < 6:
                expected_pair = (w if slot == law.action_pair else Fraction(1)) / (w + 5)
                actual = float(weights[slot]) / sum(map(float, weights[:6]))
                pair_gap = max(pair_gap, float(abs(expected_pair - Fraction.from_float(actual))))
    return {"reference_probability_gap": max(full_gap, pair_gap), "full_reference_probability_gap": full_gap, "pair_reference_probability_gap": pair_gap}


def epoch_residual(full: np.ndarray, epoch: np.ndarray) -> float:
    states = np.arange(len(full))
    residual = epoch.copy()
    direct = np.zeros_like(full)
    for bit in range(10):
        targets = states ^ (1 << bit)
        probability = full[states, targets]
        if bit < 6:
            direct[states, targets] = probability
        else:
            residual -= probability[:, None] * epoch[targets]
    return float(np.max(np.abs(residual - direct)))


def stationary_distribution(matrix: np.ndarray) -> dict:
    successors = tuple(tuple((int(t), float(matrix[s, t])) for t in np.flatnonzero(matrix[s] > 0)) for s in range(len(matrix)))
    components = strongly_connected_components(successors)
    if len(components) != 1:
        raise BridgeError(f"stationary interpretation requires an amendment: {len(components)} communicating classes")
    period = period_of(components[0], successors)
    system = np.eye(len(matrix)) - matrix.T
    system[-1] = 1
    rhs = np.zeros(len(matrix))
    rhs[-1] = 1
    pi = np.linalg.solve(system, rhs)
    minimum = float(pi.min())
    if minimum < -TOLERANCES["stationary_nonnegative"]:
        raise BridgeError("negative stationary solution")
    pi = np.maximum(pi, 0)
    pi /= pi.sum()
    residual = float(np.max(np.abs(pi @ matrix - pi)))
    if residual > TOLERANCES["stationary_residual"]:
        raise BridgeError("stationary residual exceeds frozen tolerance")
    return {"pi": pi, "residual": residual, "normalisation_error": abs(float(pi.sum()) - 1), "min_entry": minimum, "communicating_classes": len(components), "period": period, "method": "float64 normalised linear solve"}


def project(distribution: np.ndarray) -> dict:
    pair = distribution.reshape(16, 64).sum(axis=0)
    graph = np.bincount(CLASS_OF_MASK, weights=pair, minlength=11)
    edge = np.bincount([i.bit_count() for i in range(64)], weights=pair, minlength=7)
    return {"pair_mask": pair.tolist(), "graph_class": graph.tolist(), "edge_count": edge.tolist()}


def js_equal(left, right) -> float:
    p = np.asarray(left, dtype=float)
    q = np.asarray(right, dtype=float)
    if np.any(p < -1e-13) or np.any(q < -1e-13) or abs(p.sum()-1) > 1e-10 or abs(q.sum()-1) > 1e-10:
        raise BridgeError("invalid information distribution")
    p, q = np.maximum(p, 0), np.maximum(q, 0)
    p, q = p / p.sum(), q / q.sum()
    mix = (p + q) / 2
    result = 0.0
    for row in (p, q):
        positive = row > 0
        result += 0.5 * float(np.sum(row[positive] * np.log(row[positive] / mix[positive])))
    return result


def conditional_model_information(left, right, group_of_child) -> float:
    joint = 0.5 * np.asarray([left, right], dtype=float)
    joint /= joint.sum()
    group = np.asarray(group_of_child, dtype=int)
    parent = np.array([np.bincount(group, weights=row) for row in joint])
    child = joint.sum(axis=0)
    total_parent = parent.sum(axis=0)
    result = 0.0
    for model in range(2):
        positive = joint[model] > 0
        values = joint[model, positive]
        ratio = values * total_parent[group[positive]] / (parent[model, group[positive]] * child[positive])
        result += float(np.sum(values * np.log(ratio)))
    return result


def decomposition(left_pair, right_pair) -> dict:
    left, right = np.asarray(left_pair), np.asarray(right_pair)
    class_left = np.bincount(CLASS_OF_MASK, weights=left, minlength=11)
    class_right = np.bincount(CLASS_OF_MASK, weights=right, minlength=11)
    edge_of = [i.bit_count() for i in range(64)]
    edge_left = np.bincount(edge_of, weights=left, minlength=7)
    edge_right = np.bincount(edge_of, weights=right, minlength=7)
    class_edge = [next(mask.bit_count() for mask in range(64) if CLASS_OF_MASK[mask] == c) for c in range(11)]
    pair_info = js_equal(left, right)
    class_info = js_equal(class_left, class_right)
    edge_info = js_equal(edge_left, edge_right)
    shape = conditional_model_information(class_left, class_right, class_edge)
    label = conditional_model_information(left, right, CLASS_OF_MASK)
    return {
        "I_model_pairmask": pair_info, "I_model_graph_class": class_info,
        "I_model_edgecount": edge_info, "I_model_shape_given_edgecount": shape,
        "I_model_label_given_class": label,
        "pairmask_chain_gap": pair_info - edge_info - shape - label,
        "class_chain_gap": class_info - edge_info - shape,
    }


def source_initial(source: str) -> np.ndarray:
    vector = np.zeros(1024)
    vector[(np.arange(16) << 6) | source_masks()[source]] = 1 / 16
    return vector


def source_propagation(epoch: np.ndarray, source: str) -> list[dict]:
    distribution = source_initial(source)
    output = []
    for step in range(1, 65):
        distribution = distribution @ epoch
        if step in CHECKPOINTS:
            if abs(float(distribution.sum()) - 1) > TOLERANCES["kernel_row_sum"]:
                raise BridgeError("propagation mass error")
            output.append({"source": source, "checkpoint": step, **project(distribution)})
    return output


def path_event_categories(distribution: dict) -> dict:
    initial = source_masks()["path"]
    pairs = edges(4)
    adjacency = {v: set() for v in range(4)}
    for bit, (a, b) in enumerate(pairs):
        if (initial >> bit) & 1:
            adjacency[a].add(b)
            adjacency[b].add(a)
    mass = {}
    for bit, (a, b) in enumerate(pairs):
        if (initial >> bit) & 1:
            category = "middle_edge_dissolution" if bit == path_middle_action() else "end_edge_dissolution"
        else:
            category = "short_chord_formation" if adjacency[a] & adjacency[b] else "long_chord_formation"
        mass[category] = mass.get(category, 0) + distribution["pair_mask"][initial ^ (1 << bit)]
    return mass


def analyse_law(law: LawSpec) -> tuple[dict, dict[str, np.ndarray]]:
    kernel = build_law_kernel(law)
    full = full_transition_matrix(kernel)
    epoch, defect = epoch_landing(kernel)
    stationary = stationary_distribution(epoch)
    stationary_full = stationary_distribution(full)
    reference = reference_probability_gap(law, kernel)
    validation = {
        **reference, "row_sum_error": float(np.max(np.abs(full.sum(axis=1) - 1))),
        "epoch_row_sum_error": float(np.max(np.abs(epoch.sum(axis=1) - 1))),
        "epoch_kernel_residual": epoch_residual(full, epoch), "epoch_missing_mass": defect,
        "stationary_residual": stationary["residual"],
        "full_stationary_residual": stationary_full["residual"],
        "stationary_min_entry": stationary["min_entry"],
        "stationary_normalisation_error": stationary["normalisation_error"],
        "communicating_classes": stationary["communicating_classes"], "epoch_period": stationary["period"],
        "weight_precision": "exact W4 rational" if law.model in ("K3", "ENDPOINT") else "frozen 80-digit Decimal approximation, rational represented, float64 analysis",
    }
    for field, tolerance in (
        ("row_sum_error", "kernel_row_sum"), ("epoch_row_sum_error", "kernel_row_sum"),
        ("epoch_kernel_residual", "epoch_solve_residual"), ("epoch_missing_mass", "epoch_solve_residual"),
        ("reference_probability_gap", "float_local_probability_gap"),
    ):
        if validation[field] > TOLERANCES[tolerance]:
            raise BridgeError(f"{field} exceeds frozen tolerance")
    local_laws = pair_slot_laws(kernel)
    context = stationary_slot_cmi(kernel, stationary_full["pi"], local_laws["full_event"])
    post_epoch_context = stationary_slot_cmi(kernel, stationary["pi"], local_laws["conditional"])
    parity = np.array([(i & 63).bit_count() % 2 for i in range(1024)])
    parity_stationary = {}
    for value in (0, 1):
        selected = stationary["pi"] * (parity == value)
        selected /= selected.sum()
        parity_stationary[str(value)] = project(selected)
    result = {
        "law": law_record(law), "canonical_fingerprint": canonical_fingerprint(law),
        "numeric_validation": validation, "stationary": project(stationary["pi"]),
        "stationary_by_parity": parity_stationary,
        "stationary_pair_event_CMI": context,
        "stationary_post_epoch_conditional_CMI": post_epoch_context,
        "context_weighting": "full-event stationary pi(s) times full-event pair-slot probability, then normalised over pair events",
        "source_distributions": [row for source in SOURCES for row in source_propagation(epoch, source)],
    }
    return result, {"full": full, "epoch": epoch, "stationary": stationary["pi"], "stationary_full": stationary_full["pi"]}


def polarity_conjugacy_check(laws: list[LawSpec], cache: dict) -> dict:
    checks = []
    for law in laws:
        if law.incidence_motif != "BOTH" or law.model != "K3" or law.direction != "form":
            continue
        base = canonical_law(law)
        changed = replace(base, literal_polarities=(1, 0))
        kernel = build_law_kernel(base)
        flipped = build_law_kernel(changed)
        mapping = np.arange(1024) ^ (1 << 7)
        exact = all(kernel.weights[s] == flipped.weights[int(mapping[s])] for s in range(1024))
        if not exact:
            raise BridgeError("exact polarity weight conjugacy failed")
        full = full_transition_matrix(flipped)
        epoch, _ = epoch_landing(flipped)
        original = cache[canonical_fingerprint(law)]
        full_gap = float(np.max(np.abs(original["full"] - full[np.ix_(mapping, mapping)])))
        epoch_gap = float(np.max(np.abs(original["epoch"] - epoch[np.ix_(mapping, mapping)])))
        pi = stationary_distribution(epoch)["pi"]
        stationary_gap = float(np.max(np.abs(np.asarray(project(pi)["pair_mask"]) - np.asarray(project(original["stationary"])["pair_mask"]))))
        uniform_gap = max(float(np.max(np.abs(source_initial(s)[mapping] - source_initial(s)))) for s in SOURCES)
        checks.append({"grade": law.grade, "exact_weight_gap": "0", "full_kernel_gap": full_gap, "pair_epoch_gap": epoch_gap, "stationary_visible_gap": stationary_gap, "uniform_raw_triad_map_gap": uniform_gap})
    holds = len(checks) == 2 and all(max(r["full_kernel_gap"], r["pair_epoch_gap"], r["stationary_visible_gap"], r["uniform_raw_triad_map_gap"]) <= TOLERANCES["conjugacy"] for r in checks)
    if not holds:
        raise BridgeError("polarity conjugacy failed; primary bridge stopped")
    return {"holds": holds, "state_map": "s xor (1 << 7) in canonical hidden coordinates", "checks": checks}

