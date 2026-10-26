"""Generation 6 graded lattice with matched lower-order controls.

The target is one unconditional dissolution and one triad-conditioned
dissolution on a disjoint edge. Each structural target is weighted on the
full W4 grade lattice. Condition erasure and the three pair faces of the
conditioning triad are the matched controls. A pair face is a control
construction. It is not a simplicial identification.

``I`` keeps the v0.5 definition. Pairwise controls have their triadic
committor spread measured. It is not hard-coded to zero.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import statistics
import time
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

import numpy as np

from rs_constraint_lab.constraints import DISSOLVE, Constraint, parse_expression
from rs_constraint_lab.durable import atomic_write_json, canonical_json, json_ready, read_json, sha256_file
from rs_constraint_lab.grammar import canonical_id_tuple
from rs_constraint_lab.memory_clocks import epoch_kernel_block, epoch_kernel_float
from rs_constraint_lab.passage import (
    eventual_committor,
    interaction_residual,
    kernel_layout_index,
    state_interaction,
    super_singleton_gap,
)
from rs_constraint_lab.reconfiguration import RECONFIGURATION_HORIZON
from rs_constraint_lab.v05 import (
    PRIMARY_RHO,
    _baseline_pack,
    _cached_direction,
    _constrained_pack,
    _direction_names,
    _grammar,
    _num,
    _release_landings,
    _support_violations,
    require_effect_floor,
)
from rs_constraint_lab.version import HYPERGRAPH_N4_SEMANTIC_VERSION
from rs_constraint_lab.weights import ENUMERATED_WEIGHTS, alphabet_factors

ANALYSIS_6 = "n4-graded-matched-controls"
ANALYSIS_VERSION = "0.6.0"
CONTROL_MAPPING_VERSION = "0.6.0"
# Far below the v0.5 census of 2,304. A larger pool is not sampled.
GRADED_POOL_CEILING = 600
WEIGHT_ORDER = tuple(ENUMERATED_WEIGHTS)
WEIGHT_INDEX = {name: index for index, name in enumerate(WEIGHT_ORDER)}
CONTINUITY_BINS = (
    (0.0, 0.10, "< 0.10"),
    (0.10, 0.25, "0.10 to < 0.25"),
    (0.25, 0.50, "0.25 to < 0.50"),
    (0.50, 1.00, "0.50 to < 1.00"),
    (1.00, float("inf"), ">= 1.00"),
)
# Selection is fixed before the rankings are read. Ties keep the earliest row.
VALIDATION_CRITERIA = (
    "largest_finite_abs_I",
    "largest_finite_I_abs_margin",
    "largest_finite_G_margin",
    "largest_finite_delta_S",
    "largest_negative_I_abs_margin",
)
# Descriptive cut for "a few source states". Not a success threshold.
CONCENTRATION_TOP_STATES = 3
CONCENTRATION_SHARE = 0.5
ANCHOR_EXPRESSIONS = (
    "dissolve(0-1) => prohibit",
    "dissolve(2-3) | absent(0-1-2) => prohibit",
)
PUBLISHED_ANCHOR = {
    "path_to_matching": {
        "Q0": 0.18823529411764703,
        "QT": 0.18808717457278007,
        "QP": 0.18765207631874303,
        "QTP": 0.2538772345202259,
        "delta_T": -0.00014811954486695922,
        "delta_P": -0.0005832177989039955,
        "delta_TP": 0.0656419404025789,
        "I": 0.06637327774634985,
        "G": 0.0650587226036749,
        "delta_S": 0.021431815558849432,
    },
    "matching_to_path": {
        "Q0": 0.752941176470588,
        "QT": 0.75234869829112,
        "QP": 0.7506083052749721,
        "QTP": 0.6694186190536465,
        "delta_T": -0.0005924781794679479,
        "delta_P": -0.002332871195615871,
        "delta_TP": -0.08352255741694148,
        "I": -0.08059720804185766,
        "G": 0.08118968622132561,
        "delta_S": 0.036908902906276686,
    },
}


def _slot_text(slot: tuple[int, ...]) -> str:
    return "-".join(str(entity) for entity in slot)


def _edge_relation(left: tuple[int, ...], right: tuple[int, ...]) -> str:
    if tuple(left) == tuple(right):
        return "same"
    if set(left) & set(right):
        return "adjacent"
    return "disjoint"


def _faces(triad: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(face) for face in itertools.combinations(triad, 2))


def _geometry(triad: tuple[int, ...], t_edge: tuple[int, ...], p_edge: tuple[int, ...]) -> str:
    contains_t = set(t_edge) <= set(triad)
    contains_p = set(p_edge) <= set(triad)
    if contains_t and not contains_p:
        return "contains_t_action_edge"
    if contains_p and len(set(t_edge) & set(triad)) == 1:
        return "contains_p_companion_edge"
    return "other"


def _deletion_class(w_p: str, w_t: str) -> str:
    prohibited = int(w_p == "prohibit") + int(w_t == "prohibit")
    if prohibited == 2:
        return "both_prohibit"
    if prohibited == 1:
        return "exactly_one_prohibit"
    return "neither_prohibit"


def _id_text(ids: tuple[int, ...] | list[int]) -> str:
    return ",".join(str(item) for item in ids)


def _item_key(canonical_ids, w_p: str, w_t: str, spec_hash: str | None = None) -> str:
    payload = {
        "analysis_version": ANALYSIS_VERSION,
        "canonical_complete_system": [int(item) for item in canonical_ids],
        "control_mapping_version": CONTROL_MAPPING_VERSION,
        "semantic_version": HYPERGRAPH_N4_SEMANTIC_VERSION,
        "weight_cell": {"w_P": w_p, "w_T": w_t},
    }
    if spec_hash is not None:
        payload["spec_hash"] = spec_hash
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def _require_lattice_spec(spec: dict) -> None:
    if spec.get("semantics") != "hypergraph":
        raise ValueError("generation 6 executes independent hypergraph semantics")
    if spec.get("analysis") not in {None, ANALYSIS_6}:
        raise ValueError("generation 6 catalogue received a different analysis")
    for axis in ("G", "S", "H", "L"):
        if int(spec.get(axis, 0)) != 0:
            raise ValueError(f"{axis} must stay 0")
    if int(spec.get("O", 3)) != 3:
        raise ValueError("O must stay 3")
    cell = spec["cells"][0]
    if int(cell["N"]) != 4 or int(cell["K_max"]) != 2 or list(cell["cardinalities"]) != [2]:
        raise ValueError("generation 6 is N=4, K<=2, cardinality 2")
    if int(cell.get("A_max", 4)) != 4:
        raise ValueError("generation 6 keeps A_max 4")
    if tuple(spec.get("weights", ())) != WEIGHT_ORDER:
        raise ValueError("generation 6 requires the full W4 grade lattice on each rule")


def _lookup(index: dict, constraint: Constraint) -> int:
    try:
        return index[constraint.key()]
    except KeyError as exc:
        raise RuntimeError(f"constraint is outside the grammar: {constraint.key()!r}") from exc


def _roles(constraints: list[Constraint], slots) -> tuple[Constraint, Constraint]:
    gated = [item for item in constraints if item.conditions]
    plain = [item for item in constraints if not item.conditions]
    if len(gated) == 1 and len(plain) == 1:
        return gated[0], plain[0]
    if len(plain) == 2 and len(gated) == 0:
        raise RuntimeError("two unconditional rules have no gated role; assign them by weight")
    raise RuntimeError("a matched system must be one gated rule and one unconditional rule, or two unconditional rules")


def _assign_erased(constraints: list[Constraint], w_p: str, w_t: str) -> tuple[Constraint, Constraint]:
    """T is the erased action weight. Listing order is not the role."""
    if len(constraints) != 2 or any(item.conditions for item in constraints):
        raise RuntimeError("an erased control is two unconditional dissolutions")
    if w_p == w_t:
        return constraints[0], constraints[1]
    by_weight = {item.weight: item for item in constraints}
    if set(by_weight) != {w_p, w_t}:
        raise RuntimeError("erased control weights do not match the target cell")
    return by_weight[w_t], by_weight[w_p]


def _control_from_rules(grammar, index, image, first: Constraint, second: Constraint) -> tuple[int, ...]:
    return canonical_id_tuple((_lookup(index, first), _lookup(index, second)), image)


def _face_records(grammar, index, image, slots, t_rule: Constraint, p_rule: Constraint, erased_ids) -> list[dict]:
    if len(t_rule.conditions) != 1:
        raise RuntimeError("the target gate is one literal")
    cond_slot, bit = t_rule.conditions[0]
    triad = tuple(slots[cond_slot])
    action = tuple(slots[t_rule.action])
    companion = tuple(slots[p_rule.action])
    polarity = "present" if bit else "absent"
    if _faces(triad) != tuple(sorted(_faces(triad))):
        raise RuntimeError("pair faces were not the three pair subsets")
    faces = []
    seen = set()
    for face in _faces(triad):
        relation_action = _edge_relation(face, action)
        relation_companion = _edge_relation(face, companion)
        record = {
            "face": _slot_text(face),
            "relation_to_action": relation_action,
            "relation_to_companion": relation_companion,
            "polarity": polarity,
            "status": None,
            "control_ids": None,
            "control_id": None,
            "expressions": None,
            "duplicate_of_earlier_face": False,
        }
        if relation_action == "same":
            if bit == 1:
                record["status"] = "redundant_collapse_to_erasure"
                record["control_ids"] = [int(item) for item in erased_ids]
                record["control_id"] = _id_text(erased_ids)
                record["expressions"] = [grammar.expression(item) for item in erased_ids]
            else:
                record["status"] = "unsatisfiable_absent_on_action"
            faces.append(record)
            continue
        face_slot = slots.index(face)
        if face_slot == t_rule.action:
            raise RuntimeError("a face equal to the action was not classified as same")
        gated = Constraint(DISSOLVE, t_rule.action, ((face_slot, bit),), t_rule.weight, ())
        ids = _control_from_rules(grammar, index, image, gated, p_rule)
        record["status"] = "live"
        record["control_ids"] = [int(item) for item in ids]
        record["control_id"] = _id_text(ids)
        record["expressions"] = [grammar.expression(item) for item in ids]
        if record["control_id"] in seen or record["control_id"] == _id_text(erased_ids):
            record["duplicate_of_earlier_face"] = True
        seen.add(record["control_id"])
        faces.append(record)
    if len(faces) != 3:
        raise RuntimeError("a triad must contribute three pair faces")
    named = {_relation_entities(row["face"]) for row in faces}
    if named != set(_faces(triad)):
        raise RuntimeError("face records are not the three pair subsets of the triad")
    return faces


def _relation_entities(text: str) -> tuple[int, ...]:
    return tuple(int(part) for part in text.split("-"))


def _build_record(grammar, index, image, slots, canon: tuple[int, ...]) -> dict:
    members = [grammar.labelled[item] for item in canon]
    t_rule, p_rule = _roles(members, slots)
    if t_rule.polarity != DISSOLVE or p_rule.polarity != DISSOLVE:
        raise RuntimeError("the target family is dissolution on both actions")
    if len(t_rule.conditions) != 1:
        raise RuntimeError("the target gate is one triadic literal")
    cond_slot, bit = t_rule.conditions[0]
    triad = tuple(slots[cond_slot])
    if len(triad) != 3:
        raise RuntimeError("the target condition is not a triad")
    t_edge = tuple(slots[t_rule.action])
    p_edge = tuple(slots[p_rule.action])
    if not set(t_edge).isdisjoint(p_edge):
        raise RuntimeError("target action edges are not disjoint")
    geometry = _geometry(triad, t_edge, p_edge)
    erased_rule = Constraint(DISSOLVE, t_rule.action, (), t_rule.weight, ())
    erased_ids = _control_from_rules(grammar, index, image, erased_rule, p_rule)
    faces = _face_records(grammar, index, image, slots, t_rule, p_rule, erased_ids)
    live_ids = []
    for face in faces:
        if face["status"] == "live" and not face["duplicate_of_earlier_face"]:
            if face["control_id"] != _id_text(erased_ids):
                live_ids.append(face["control_id"])
    matched = [_id_text(erased_ids), *live_ids]
    if len(matched) != len(set(matched)):
        raise RuntimeError("matched control ids are not deduplicated")
    expressions = [p_rule.expression(slots), t_rule.expression(slots)]
    return {
        "canonical_ids": [int(item) for item in canon],
        "target_id": _item_key(canon, p_rule.weight, t_rule.weight)[:24],
        "item_key": _item_key(canon, p_rule.weight, t_rule.weight),
        "expressions": expressions,
        "geometry": geometry,
        "polarity": "present" if bit else "absent",
        "w_P": p_rule.weight,
        "w_T": t_rule.weight,
        "deletion_class": _deletion_class(p_rule.weight, t_rule.weight),
        "action_edges": {"P": _slot_text(p_edge), "T": _slot_text(t_edge)},
        "triad": _slot_text(triad),
        "condition_polarity_bit": int(bit),
        "erased_ids": [int(item) for item in erased_ids],
        "erased_control_id": _id_text(erased_ids),
        "erased_expressions": [grammar.expression(item) for item in erased_ids],
        "faces": faces,
        "face_control_ids": live_ids,
        "matched_control_ids": matched,
        "control_mapping_version": CONTROL_MAPPING_VERSION,
    }


def _face_signature(faces: list[dict]) -> frozenset:
    """Relation, status, and canonical control. Face labels are not part of the match."""
    return frozenset(
        (row["relation_to_action"], row["status"], row["control_id"], row["polarity"])
        for row in faces
    )


def _labelled_signature(grammar, index, image, slots, t_rule: Constraint, p_rule: Constraint) -> tuple:
    erased_ids = _control_from_rules(
        grammar,
        index,
        image,
        Constraint(DISSOLVE, t_rule.action, (), t_rule.weight, ()),
        p_rule,
    )
    faces = _face_records(grammar, index, image, slots, t_rule, p_rule, erased_ids)
    return (_id_text(erased_ids), _face_signature(faces))


def graded_catalogue(spec: dict) -> dict:
    """Exact S4 catalogue of the target lattice and its matched controls.

    Labelled systems are enumerated from the motif, then canonicalised as
    complete two-rule sets. Counts are not products of singleton orbits.
    """
    _require_lattice_spec(spec)
    grammar = _grammar(WEIGHT_ORDER, 4)
    slots = grammar.slot_list()
    index = {constraint.key(): position for position, constraint in enumerate(grammar.labelled)}
    image = grammar.image
    pair_slots = [slot for slot in slots if len(slot) == 2]
    triad_slots = [slot for slot in slots if len(slot) == 3]
    orbits: Counter = Counter()
    records: dict[tuple[int, ...], dict] = {}
    labelled = 0
    labelled_erased_keys = set()
    labelled_live_face_keys = set()
    canonical_erased = set()
    canonical_live_faces = set()
    labelled_face_attempts = 0
    collapsed = 0
    unsatisfiable = 0
    live_faces = 0
    within_target_face_dedup = 0
    unexpected_live_equals_erased = 0
    for left in pair_slots:
        for right in pair_slots:
            if not set(left).isdisjoint(right):
                continue
            for triad in triad_slots:
                for bit in (0, 1):
                    for w_p in WEIGHT_ORDER:
                        for w_t in WEIGHT_ORDER:
                            labelled += 1
                            companion = Constraint(DISSOLVE, slots.index(left), (), w_p, ())
                            gated = Constraint(
                                DISSOLVE,
                                slots.index(right),
                                ((slots.index(triad), bit),),
                                w_t,
                                (),
                            )
                            canon = canonical_id_tuple(
                                (_lookup(index, companion), _lookup(index, gated)),
                                image,
                            )
                            orbits[canon] += 1
                            erased_rule = Constraint(DISSOLVE, slots.index(right), (), w_t, ())
                            labelled_erased_keys.add((companion.key(), erased_rule.key()))
                            erased_ids = _control_from_rules(grammar, index, image, erased_rule, companion)
                            canonical_erased.add(erased_ids)
                            for face in _faces(triad):
                                labelled_face_attempts += 1
                                if face == tuple(right):
                                    if bit == 0:
                                        unsatisfiable += 1
                                    else:
                                        collapsed += 1
                                    continue
                                live_faces += 1
                                face_rule = Constraint(
                                    DISSOLVE,
                                    slots.index(right),
                                    ((slots.index(face), bit),),
                                    w_t,
                                    (),
                                )
                                labelled_live_face_keys.add((companion.key(), face_rule.key()))
                                canonical_live_faces.add(
                                    _control_from_rules(grammar, index, image, face_rule, companion)
                                )
                            signature = _labelled_signature(grammar, index, image, slots, gated, companion)
                            if canon not in records:
                                records[canon] = _build_record(grammar, index, image, slots, canon)
                            stored_faces = _face_signature(records[canon]["faces"])
                            stored = (records[canon]["erased_control_id"], stored_faces)
                            if signature != stored:
                                raise RuntimeError("control mapping is not a function of the canonical target")
    representatives = tuple(sorted(records))
    if len(representatives) != len(orbits):
        raise RuntimeError("orbit keys and records diverged")
    structural = _grammar((WEIGHT_ORDER[0],), 4)
    structural_index = {constraint.structural_key(): position for position, constraint in enumerate(structural.labelled)}
    structural_canons = set()
    relation_live = Counter()
    relation_other = Counter()
    swapped_groups = defaultdict(set)
    for canon in representatives:
        record = records[canon]
        record["orbit_size"] = int(orbits[canon])
        members = [grammar.labelled[item] for item in canon]
        structural_ids = tuple(
            structural_index[item.structural_key()] for item in members
        )
        structural_canons.add(canonical_id_tuple(structural_ids, structural.image))
        swapped_groups[record["erased_control_id"]].add((record["w_P"], record["w_T"]))
        for face in record["faces"]:
            if face["status"] == "live":
                relation_live[face["relation_to_action"]] += 1
                if face["duplicate_of_earlier_face"]:
                    within_target_face_dedup += 1
                if face["control_id"] == record["erased_control_id"]:
                    unexpected_live_equals_erased += 1
            else:
                relation_other[face["status"]] += 1
    for record in records.values():
        mates = swapped_groups[record["erased_control_id"]]
        record["erased_shared_with_swapped_weights"] = (record["w_T"], record["w_P"]) in mates and record["w_P"] != record["w_T"]
        record["erased_weight_role"] = "assigned_by_weight_not_by_listing_order"
    cells = Counter((row["geometry"], row["polarity"], row["w_P"], row["w_T"]) for row in records.values())
    geometries = sorted({row["geometry"] for row in records.values()})
    polarities = sorted({row["polarity"] for row in records.values()})
    missing_cells = [
        {"geometry": geometry, "polarity": polarity, "w_P": w_p, "w_T": w_t}
        for geometry in geometries
        for polarity in polarities
        for w_p in WEIGHT_ORDER
        for w_t in WEIGHT_ORDER
        if cells[(geometry, polarity, w_p, w_t)] != 1
    ]
    live_relations = set(relation_live)
    spans_relevant = {"adjacent", "disjoint"} <= live_relations and "same" not in live_relations
    control_3 = {
        "added": False,
        "spans_same_adjacent_and_disjoint": spans_relevant,
        "live_relations_to_action": dict(sorted(relation_live.items())),
        "non_live_face_statuses": dict(sorted(relation_other.items())),
        "reason": (
            "Pair-face substitution produces live adjacent gates and live disjoint gates. "
            "The same-as-action face is present as a recorded collapse when the literal is "
            "redundant, and as an unsatisfiable literal when it contradicts dissolution. "
            "At N=4 the only edge disjoint from the acted edge is the companion edge, so "
            "that disjoint gate is the missing relation and it is already in the face set. "
            "No wider pairwise family is added."
            if spans_relevant
            else "A relevant pair-gate relation is missing. Do not run until that gap is documented."
        ),
    }
    if not spans_relevant:
        control_3["added"] = False
    payload = []
    for canon in representatives:
        row = records[canon]
        payload.append(
            {
                "canonical_ids": row["canonical_ids"],
                "geometry": row["geometry"],
                "polarity": row["polarity"],
                "w_P": row["w_P"],
                "w_T": row["w_T"],
                "erased_control_id": row["erased_control_id"],
                "faces": [
                    {
                        "face": face["face"],
                        "relation_to_action": face["relation_to_action"],
                        "status": face["status"],
                        "control_id": face["control_id"],
                    }
                    for face in row["faces"]
                ],
                "matched_control_ids": row["matched_control_ids"],
            }
        )
    digest = hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()
    coverage = {
        "labelled_target_systems": labelled,
        "canonical_target_systems": len(representatives),
        "canonical_structural_targets": len(structural_canons),
        "labelled_condition_erased_controls": labelled,
        "distinct_labelled_condition_erased_controls": len(labelled_erased_keys),
        "canonical_condition_erased_controls": len(canonical_erased),
        "labelled_face_control_attempts": labelled_face_attempts,
        "labelled_live_face_controls": live_faces,
        "distinct_labelled_live_face_controls": len(labelled_live_face_keys),
        "canonical_face_controls": len(canonical_live_faces),
        "collapsed_same_as_action_present": collapsed,
        "unsatisfiable_same_as_action_absent": unsatisfiable,
        "within_target_face_deduplications": within_target_face_dedup,
        "live_face_equal_to_erasure": unexpected_live_equals_erased,
        "invalid_structurally_simple_pairs": 0,
        "orbit_size_distribution": {
            str(size): count for size, count in sorted(Counter(orbits.values()).items())
        },
        "labelled_targets_accounted": int(sum(orbits.values())),
        "weight_cells_per_geometry_polarity": len(WEIGHT_ORDER) ** 2,
        "geometry_polarity_weight_cells_not_exactly_one": missing_cells,
        "geometries": geometries,
        "polarities": polarities,
        "deletion_class_counts": dict(sorted(Counter(row["deletion_class"] for row in records.values()).items())),
        "erased_ids_shared_by_swapped_weights": sum(
            1 for mates in swapped_groups.values() if any(left != right and (right, left) in mates for left, right in mates)
        ),
        "below_v05_pair_census": len(representatives) < 2304,
        "v05_pair_census": 2304,
    }
    if coverage["labelled_targets_accounted"] != labelled:
        raise RuntimeError("labelled target orbit accounting does not close")
    return {
        "control_mapping_version": CONTROL_MAPPING_VERSION,
        "analysis_version": ANALYSIS_VERSION,
        "semantic_version": HYPERGRAPH_N4_SEMANTIC_VERSION,
        "grammar_weights": list(WEIGHT_ORDER),
        "records": [records[canon] for canon in representatives],
        "coverage": coverage,
        "control_3": control_3,
        "sha256": digest,
    }


def _record_by_expressions(catalogue: dict, expressions: tuple[str, str] | list[str]) -> dict:
    grammar = _grammar(WEIGHT_ORDER, 4)
    slots = grammar.slot_list()
    index = {constraint.key(): position for position, constraint in enumerate(grammar.labelled)}
    parsed = [parse_expression(text, 4, order=3) for text in expressions]
    canon = canonical_id_tuple(tuple(_lookup(index, item) for item in parsed), grammar.image)
    text = _id_text(canon)
    for record in catalogue["records"]:
        if _id_text(record["canonical_ids"]) == text:
            return record
    raise KeyError(f"expressions are not in the graded catalogue: {expressions}")


def _constraints_of(grammar, ids: list[int]) -> list[Constraint]:
    return [grammar.labelled[int(item)] for item in ids]


def _state_sign(i_state: np.ndarray, mu: np.ndarray, floor: float) -> dict:
    defined = np.isfinite(i_state) & (mu > 0.0)
    if not np.any(defined):
        return {"defined": False, "coherence": "undefined", "n_positive": 0, "n_negative": 0, "n_within_floor": 0}
    values = i_state[defined]
    n_positive = int(np.sum(values > floor))
    n_negative = int(np.sum(values < -floor))
    n_within = int(values.size - n_positive - n_negative)
    if n_positive and n_negative:
        coherence = "mixed"
    elif n_positive:
        coherence = "positive"
    elif n_negative:
        coherence = "negative"
    else:
        coherence = "within_floor"
    return {
        "defined": True,
        "coherence": coherence,
        "n_source_states": int(values.size),
        "n_positive": n_positive,
        "n_negative": n_negative,
        "n_within_floor": n_within,
    }


def _system_directions(t_rule, p_rule, baseline, factors, rho, slots, cache, floor: float, store_states: bool) -> dict:
    packs = {
        "0": baseline,
        "T": _constrained_pack((t_rule,), factors, rho, slots, cache),
        "P": _constrained_pack((p_rule,), factors, rho, slots, cache),
        "TP": _constrained_pack((t_rule, p_rule), factors, rho, slots, cache),
    }
    table = baseline["table"]
    horizon = RECONFIGURATION_HORIZON
    out = {}
    residuals = []
    for key, source_name, target_name in _direction_names(table):
        solved = {
            label: _cached_direction(pack, baseline, source_name, target_name, horizon)
            for label, pack in packs.items()
        }
        for label in packs:
            residual = solved[label]["solver"]["residual"]
            residuals.append(0.0 if residual is None else float(residual))
            if solved[label]["mu_ref"] is not baseline["mu_ref"][source_name]:
                raise RuntimeError("controlled source diverged between a target and its controls")
        q0 = solved["0"]["q_controlled"]
        qt = solved["T"]["q_controlled"]
        qp = solved["P"]["q_controlled"]
        qtp = solved["TP"]["q_controlled"]
        delta_t = None if qt is None or q0 is None else float(qt - q0)
        delta_p = None if qp is None or q0 is None else float(qp - q0)
        delta_tp = None if qtp is None or q0 is None else float(qtp - q0)
        residual_i = None
        if None not in {q0, qt, qp, qtp}:
            residual_i = interaction_residual(qtp, qt, qp, q0)
        gap = None if None in {delta_t, delta_p, delta_tp} else super_singleton_gap(delta_tp, delta_t, delta_p)
        spread_t = solved["T"]["triad"].get("spread")
        spread_tp = solved["TP"]["triad"].get("spread")
        delta_s = None if spread_t is None or spread_tp is None else float(spread_tp - spread_t)
        i_state = state_interaction(solved["TP"]["q"], solved["T"]["q"], solved["P"]["q"], solved["0"]["q"])
        direction = {
            "Q0": q0,
            "QT": qt,
            "QP": qp,
            "QTP": qtp,
            "delta_T": delta_t,
            "delta_P": delta_p,
            "delta_TP": delta_tp,
            "I": residual_i,
            "G": gap,
            "S_T": None if spread_t is None else float(spread_t),
            "S_TP": None if spread_tp is None else float(spread_tp),
            "delta_S": delta_s,
            "state_sign": _state_sign(i_state, solved["0"]["mu_ref"], floor),
            "solver_residual": max(float(solved[label]["solver"]["residual"] or 0.0) for label in packs),
        }
        if store_states:
            mu = solved["0"]["mu_ref"]
            defined = np.isfinite(i_state) & (mu > 0.0)
            states = [int(state) for state in np.flatnonzero(defined)]
            direction["states"] = states
            direction["i_state"] = [float(i_state[state]) for state in states]
            direction["triad"] = [int(state) >> int(baseline["n_pairs"]) for state in states]
        out[key] = direction
    _release_landings(cache)
    return {"directions": out, "max_solver_residual": max(residuals) if residuals else None, "packs": packs}


def _unique_controls(record: dict, grammar, slots) -> list[dict]:
    systems = []
    erased_members = _constraints_of(grammar, record["erased_ids"])
    t_rule, p_rule = _assign_erased(erased_members, record["w_P"], record["w_T"])
    systems.append(
        {
            "role": "erased",
            "control_id": record["erased_control_id"],
            "relation_to_action": "unconditional",
            "status": "live",
            "t": t_rule,
            "p": p_rule,
        }
    )
    seen = {record["erased_control_id"]}
    for face in record["faces"]:
        if face["status"] != "live" or face["control_id"] in seen:
            continue
        members = _constraints_of(grammar, face["control_ids"])
        gated, companion = _roles(members, slots)
        if gated.weight != record["w_T"] or companion.weight != record["w_P"]:
            raise RuntimeError("a face control does not preserve the target weights")
        bit = gated.conditions[0][1]
        if ("present" if bit else "absent") != record["polarity"]:
            raise RuntimeError("a face control changed polarity")
        systems.append(
            {
                "role": "face",
                "control_id": face["control_id"],
                "relation_to_action": face["relation_to_action"],
                "relation_to_companion": face["relation_to_companion"],
                "face": face["face"],
                "status": "live",
                "t": gated,
                "p": companion,
            }
        )
        seen.add(face["control_id"])
    return systems


def _safe_ratio(numerator: float | None, denominator: float | None, floor: float) -> float | None:
    if numerator is None or denominator is None or abs(denominator) <= floor:
        return None
    return float(numerator / denominator)


def _margins(target: dict, controls: list[dict], floor: float) -> dict:
    finite = [row for row in controls if row.get("I") is not None]
    if not finite or target.get("I") is None:
        return {
            "control_abs_I_max": None,
            "I_abs_margin": None,
            "I_ratio": None,
            "attaining_abs_I_control_id": None,
            "control_G_max": None,
            "G_margin": None,
            "G_ratio": None,
            "attaining_G_control_id": None,
        }
    abs_winner = max(finite, key=lambda row: (abs(row["I"]), row["control_id"]))
    # The earliest id wins an exact tie so the attaining control is stable.
    abs_candidates = [row for row in finite if abs(abs(row["I"]) - abs(abs_winner["I"])) <= 0.0]
    abs_winner = sorted(abs_candidates, key=lambda row: row["control_id"])[0]
    g_finite = [row for row in finite if row.get("G") is not None]
    g_winner = max(g_finite, key=lambda row: (row["G"], row["control_id"]))
    g_candidates = [row for row in g_finite if g_winner["G"] - row["G"] == 0.0]
    g_winner = sorted(g_candidates, key=lambda row: row["control_id"])[0]
    control_abs = abs(abs_winner["I"])
    return {
        "control_abs_I_max": control_abs,
        "I_abs_margin": float(abs(target["I"]) - control_abs),
        "I_ratio": _safe_ratio(abs(target["I"]), control_abs, floor),
        "attaining_abs_I_control_id": abs_winner["control_id"],
        "control_G_max": g_winner["G"],
        "G_margin": float(target["G"] - g_winner["G"]),
        "G_ratio": _safe_ratio(target["G"], g_winner["G"], floor),
        "attaining_G_control_id": g_winner["control_id"],
    }


def assess_target_row(record: dict, spec: dict, grammar, cache: dict, *, factors=None, rho: Fraction | None = None, store_states: bool = False) -> dict:
    """Controlled committor of one target and of each deduplicated matched control."""
    floor = require_effect_floor(spec)
    factors = alphabet_factors(spec["alphabet"]) if factors is None else factors
    rho = PRIMARY_RHO if rho is None else rho
    if int(spec.get("reconfiguration_horizon", RECONFIGURATION_HORIZON)) != RECONFIGURATION_HORIZON:
        raise RuntimeError("refusing to run: the horizon is not the predeclared value 16")
    slots = grammar.slot_list()
    members = _constraints_of(grammar, record["canonical_ids"])
    t_rule, p_rule = _roles(members, slots)
    if [p_rule.expression(slots), t_rule.expression(slots)] != record["expressions"]:
        raise RuntimeError("canonical representative expressions drifted from the catalogue")
    baseline = _baseline_pack(factors, rho, slots, cache)
    target = _system_directions(t_rule, p_rule, baseline, factors, rho, slots, cache, floor, store_states)
    violations = 0
    tp_kernel = target["packs"]["TP"]["kernel"]
    for label in ("T", "P", "0"):
        violations += _support_violations(tp_kernel, target["packs"][label]["kernel"])
    removed = _support_violations(target["packs"]["0"]["kernel"], tp_kernel)
    control_systems = _unique_controls(record, grammar, slots)
    solved_controls = []
    for system in control_systems:
        solved = _system_directions(system["t"], system["p"], baseline, factors, rho, slots, cache, floor, store_states)
        solved_controls.append((system, solved))
        if solved["directions"]["path_to_matching"]["Q0"] != target["directions"]["path_to_matching"]["Q0"]:
            raise RuntimeError("baseline committor differed between a target and a matched control")
    directions = {}
    for key in target["directions"]:
        control_rows = []
        for system, solved in solved_controls:
            direction = solved["directions"][key]
            control_rows.append(
                {
                    "role": system["role"],
                    "control_id": system["control_id"],
                    "relation_to_action": system["relation_to_action"],
                    "relation_to_companion": system.get("relation_to_companion"),
                    "face": system.get("face"),
                    "status": system["status"],
                    "I": direction["I"],
                    "G": direction["G"],
                    "delta_S": direction["delta_S"],
                    "delta_TP": direction["delta_TP"],
                    "S_T": direction["S_T"],
                    "S_TP": direction["S_TP"],
                    "state_sign": direction["state_sign"],
                    "states": direction.get("states"),
                    "i_state": direction.get("i_state"),
                    "triad": direction.get("triad"),
                }
            )
        target_direction = dict(target["directions"][key])
        margin = _margins(target_direction, control_rows, floor)
        published_controls = []
        for row in control_rows:
            published = dict(row)
            if not store_states:
                published.pop("states", None)
                published.pop("i_state", None)
                published.pop("triad", None)
            published_controls.append(published)
        if not store_states:
            target_direction.pop("states", None)
            target_direction.pop("i_state", None)
            target_direction.pop("triad", None)
        directions[key] = {
            "target": target_direction,
            "controls": published_controls,
            **margin,
        }
    residuals = [target["max_solver_residual"]]
    residuals.extend(solved["max_solver_residual"] for _system, solved in solved_controls)
    return _num(
        {
            "target_id": record["target_id"],
            "work_item_key": _item_key(
                record["canonical_ids"],
                record["w_P"],
                record["w_T"],
                spec.get("_spec_hash"),
            ),
            "item_key": record["item_key"],
            "canonical_ids": record["canonical_ids"],
            "expressions": record["expressions"],
            "geometry": record["geometry"],
            "polarity": record["polarity"],
            "w_P": record["w_P"],
            "w_T": record["w_T"],
            "deletion_class": record["deletion_class"],
            "action_edges": record["action_edges"],
            "triad": record["triad"],
            "orbit_size": record.get("orbit_size"),
            "control_mapping_version": CONTROL_MAPPING_VERSION,
            "erased_control_id": record["erased_control_id"],
            "erased_ids": record["erased_ids"],
            "erased_expressions": record["erased_expressions"],
            "erased_shared_with_swapped_weights": record.get("erased_shared_with_swapped_weights"),
            "erased_weight_role": record.get("erased_weight_role"),
            "face_control_ids": list(record["face_control_ids"]),
            "faces": record["faces"],
            "matched_control_ids": list(record["matched_control_ids"]),
            "directions": directions,
            "support_violations": violations,
            "support_removed": removed,
            "max_residual": max(residual for residual in residuals if residual is not None),
            "analysis_version": ANALYSIS_VERSION,
            "semantic_version": HYPERGRAPH_N4_SEMANTIC_VERSION,
        }
    )


def _minimal_spec(**overrides) -> dict:
    spec = {
        "schema": "rs-constraint-lab.experiment/v1",
        "experiment_id": "generation-006-graded-matched-control-lattice",
        "generation": 6,
        "semantics": "hypergraph",
        "G": 0,
        "S": 0,
        "H": 0,
        "L": 0,
        "O": 3,
        "alphabet": "W4",
        "composition": "structural-simple",
        "analysis": ANALYSIS_6,
        "analysis_version": ANALYSIS_VERSION,
        "predicates": ["pair", "triad"],
        "weights": list(WEIGHT_ORDER),
        "cells": [{"N": 4, "K_max": 2, "A_max": 4, "cardinalities": [2]}],
        "reconfiguration_horizon": 16,
        "effect_floor": 1e-8,
        "sensitivity_alphabets": ["W3", "W16"],
        "rho3_sensitivity": ["1/2", "1", "2"],
        "focused_transition": ["e2-deg2110-tri0-comp2", "e2-deg1111-tri0-comp2"],
    }
    spec.update(overrides)
    return spec


def numerical_preflight(spec: dict | None = None) -> dict:
    """Numerical gaps on predeclared reference systems.

    The systems are the baseline, the v0.5 prohibit anchor, one finite
    suppress target, one finite favour target, the anchor's erased control,
    and one live pair-face of the anchor. They are not chosen by extremum.
    Magnitudes of ``I`` are not a reason to move the effect floor.
    """
    spec = _minimal_spec() if spec is None else spec
    floor = require_effect_floor(spec)
    catalogue = graded_catalogue(spec)
    anchor = _record_by_expressions(catalogue, ANCHOR_EXPRESSIONS)
    same_structure = [
        row
        for row in catalogue["records"]
        if row["geometry"] == anchor["geometry"] and row["polarity"] == anchor["polarity"]
    ]
    suppress = next(row for row in same_structure if row["w_P"] == "strong_suppress" and row["w_T"] == "strong_suppress")
    favour = next(row for row in same_structure if row["w_P"] == "strong_favour" and row["w_T"] == "strong_favour")
    grammar = _grammar(WEIGHT_ORDER, 4)
    slots = grammar.slot_list()
    factors = alphabet_factors("W4")
    cache: dict = {}
    named = {
        "baseline": None,
        "v05_prohibit_anchor": anchor,
        "finite_suppress_target": suppress,
        "finite_favour_target": favour,
    }
    landing_gaps = {}
    committor_gaps = {}
    direct_iterative = {}
    baseline = _baseline_pack(factors, PRIMARY_RHO, slots, cache)
    kernels = {"baseline": baseline["kernel"]}
    for name, record in named.items():
        if record is None:
            continue
        members = _constraints_of(grammar, record["canonical_ids"])
        t_rule, p_rule = _roles(members, slots)
        pack = _constrained_pack((t_rule, p_rule), factors, PRIMARY_RHO, slots, cache)
        kernels[name] = pack["kernel"]
    erased_members = _constraints_of(grammar, anchor["erased_ids"])
    erased_t, erased_p = _assign_erased(erased_members, anchor["w_P"], anchor["w_T"])
    kernels["condition_erased_control"] = _constrained_pack(
        (erased_t, erased_p), factors, PRIMARY_RHO, slots, cache
    )["kernel"]
    live_face = next(face for face in anchor["faces"] if face["status"] == "live")
    face_members = _constraints_of(grammar, live_face["control_ids"])
    kernels["pair_face_control"] = _constrained_pack(tuple(face_members), factors, PRIMARY_RHO, slots, cache)["kernel"]
    for name, kernel in kernels.items():
        dense, _dense_defect = epoch_kernel_float(kernel)
        block, _block_defect = epoch_kernel_block(kernel)
        if dense is None or block is None:
            raise RuntimeError(f"{name} epoch solver failed")
        landing_gaps[name] = float(np.max(np.abs(dense - block)))
        _n_pairs, class_index, table = kernel_layout_index(kernel)
        gaps = []
        iterative_gaps = []
        for source_name, target_name in (
            (table.path_name, table.matching_name),
            (table.matching_name, table.path_name),
        ):
            source = baseline["positions"][source_name]
            target = baseline["positions"][target_name]
            left = eventual_committor(dense, class_index, source, target)
            right = eventual_committor(block, class_index, source, target)
            both = np.isfinite(left["q"]) & np.isfinite(right["q"])
            gaps.append(float(np.max(np.abs(left["q"][both] - right["q"][both]))))
            iterated = eventual_committor(block, class_index, source, target, method="iterative")
            both_i = np.isfinite(right["q"]) & np.isfinite(iterated["q"])
            iterative_gaps.append(float(np.max(np.abs(right["q"][both_i] - iterated["q"][both_i]))))
        committor_gaps[name] = max(gaps)
        direct_iterative[name] = max(iterative_gaps)
    assessed = assess_target_row(anchor, spec, grammar, {})
    identity_gap = 0.0
    state_gap = 0.0
    for key, published in PUBLISHED_ANCHOR.items():
        got = assessed["directions"][key]["target"]["I"]
        recomputed = interaction_residual(
            assessed["directions"][key]["target"]["QTP"],
            assessed["directions"][key]["target"]["QT"],
            assessed["directions"][key]["target"]["QP"],
            assessed["directions"][key]["target"]["Q0"],
        )
        identity_gap = max(identity_gap, abs(got - recomputed))
        state_gap = max(state_gap, abs(got - published["I"]))
    # State-resolved subtraction noise on the anchor, direct versus iterative.
    anchor_pack = _constrained_pack(
        tuple(_roles(_constraints_of(grammar, anchor["canonical_ids"]), slots)),
        factors,
        PRIMARY_RHO,
        slots,
        cache,
    )
    _n_pairs, class_index, table = kernel_layout_index(anchor_pack["kernel"])
    source_name, target_name = table.path_name, table.matching_name
    direct_q = eventual_committor(
        anchor_pack["landing"], class_index, baseline["positions"][source_name], baseline["positions"][target_name]
    )["q"]
    iterative_q = eventual_committor(
        anchor_pack["landing"],
        class_index,
        baseline["positions"][source_name],
        baseline["positions"][target_name],
        method="iterative",
    )["q"]
    both_q = np.isfinite(direct_q) & np.isfinite(iterative_q)
    state_subtraction = float(np.max(np.abs(direct_q[both_q] - iterative_q[both_q])))
    worst = max([*landing_gaps.values(), *committor_gaps.values(), *direct_iterative.values(), identity_gap, state_subtraction])
    decision = "keep_1e-8" if worst < 1e-10 else "stop_and_document_before_census"
    return {
        "effect_floor_input": floor,
        "landing_block_vs_dense": landing_gaps,
        "committor_block_vs_dense": committor_gaps,
        "committor_direct_vs_iterative": direct_iterative,
        "interaction_identity_gap": identity_gap,
        "anchor_versus_published_I_gap": state_gap,
        "anchor_state_direct_vs_iterative": state_subtraction,
        "worst_numerical_gap": worst,
        "floor_decision": decision,
        "floor_rule": "Keep 1e-8 when the worst reference gap is below 1e-10. Do not use scientific magnitudes.",
        "reference_face_control_id": live_face["control_id"],
        "anchor_target_id": anchor["target_id"],
        "catalogue_sha256": catalogue["sha256"],
        "coverage": catalogue["coverage"],
        "control_3": catalogue["control_3"],
    }


def benchmark_graded_cost(spec: dict, catalogue: dict | None = None) -> dict:
    """Time the anchor and the next catalogue row. The estimate is an upper bound, not a ranking."""
    catalogue = catalogue or graded_catalogue(spec)
    grammar = _grammar(WEIGHT_ORDER, 4)
    anchor = _record_by_expressions(catalogue, ANCHOR_EXPRESSIONS)
    sample_ids = [anchor["target_id"]]
    for record in catalogue["records"]:
        if record["target_id"] not in sample_ids:
            sample_ids.append(record["target_id"])
        if len(sample_ids) == 2:
            break
    cache: dict = {}
    elapsed = []
    residual = 0.0
    for target_id in sample_ids:
        record = next(row for row in catalogue["records"] if row["target_id"] == target_id)
        started = time.perf_counter()
        row = assess_target_row(record, spec, grammar, cache)
        elapsed.append(time.perf_counter() - started)
        residual = max(residual, float(row["max_residual"] or 0.0))
    count = catalogue["coverage"]["canonical_target_systems"]
    per_cold = elapsed[0]
    per_warm = sum(elapsed[1:]) / max(1, len(elapsed) - 1)
    return {
        "sample_targets": len(sample_ids),
        "cold_target_seconds": per_cold,
        "warm_target_seconds": per_warm,
        "sample_seconds": sum(elapsed),
        "estimated_serial_seconds_from_warm": count * per_warm,
        "estimated_serial_seconds_upper": count * per_cold,
        "stationary_or_solver_residual_sample": residual,
        "sample_note": "anchor plus the next catalogue row; science values are not retained",
    }


def build_graded_plan(spec: dict, items: int, header: dict) -> dict:
    from rs_constraint_lab.execution import PLAN_SCHEMA, _hypergraph_accounting, _shard_id, _shard_identity
    from rs_constraint_lab.version import DEFAULT_WORKERS, PROFILE_NOTE

    _require_lattice_spec(spec)
    if list(spec.get("sensitivity_alphabets", [])) != ["W3", "W16"]:
        raise ValueError("generation 6 sensitivity alphabets are W3 and W16")
    if [str(item) for item in spec.get("rho3_sensitivity", [])] != ["1/2", "1", "2"]:
        raise ValueError("generation 6 rho3 probes are 1/2, 1, and 2")
    floor = require_effect_floor(spec)
    catalogue = graded_catalogue(spec)
    count = catalogue["coverage"]["canonical_target_systems"]
    if count > GRADED_POOL_CEILING:
        raise RuntimeError(
            f"graded canonical pool is {count}, above the ceiling {GRADED_POOL_CEILING}. "
            "No sample was drawn."
        )
    if not catalogue["coverage"]["below_v05_pair_census"]:
        raise RuntimeError("the graded pool is not smaller than the v0.5 census; stop and explain it")
    if catalogue["coverage"]["geometry_polarity_weight_cells_not_exactly_one"]:
        raise RuntimeError("the weight lattice is not exactly one canonical system per cell")
    if catalogue["control_3"]["added"]:
        raise RuntimeError("control 3 was marked added without a separate frozen extension")
    if not catalogue["control_3"]["spans_same_adjacent_and_disjoint"]:
        raise RuntimeError("matched faces do not span the relevant pair-gate relations")
    timed = benchmark_graded_cost(spec, catalogue)
    cell = spec["cells"][0]
    grammar = _grammar(WEIGHT_ORDER, 4)
    shard_count = 0 if count == 0 else (count + items - 1) // items
    shards = []
    start = 0
    while start < count:
        end = min(start + items, count)
        identity = _shard_identity(spec, header, 0, cell, 2, start, end)
        identity["catalogue_sha256"] = catalogue["sha256"]
        identity["analysis_version"] = ANALYSIS_VERSION
        identity["control_mapping_version"] = CONTROL_MAPPING_VERSION
        identity["effect_floor"] = floor
        identity["semantic_version"] = header["semantic_version"]
        shards.append(
            {
                "shard_id": _shard_id(identity),
                "ordinal": len(shards),
                "cell_index": 0,
                "n": 4,
                "k_max": 2,
                "a_max": 4,
                "cardinality": 2,
                "start": start,
                "end": end,
                "identity": identity,
            }
        )
        start = end
    header = dict(header)
    header["catalogue_sha256"] = catalogue["sha256"]
    header["analysis_version"] = ANALYSIS_VERSION
    header["control_mapping_version"] = CONTROL_MAPPING_VERSION
    coverage = catalogue["coverage"]
    return {
        "schema": PLAN_SCHEMA,
        "header": header,
        "spec": spec,
        "estimates": {
            "cells": [
                {
                    "N": 4,
                    "K_max": 2,
                    "A_max": 4,
                    "labelled_states": 1024,
                    "canonical_states": None,
                    "grammar": grammar.stats,
                    "edge_accounting": _hypergraph_accounting(grammar),
                    "cardinalities": {
                        "2": {
                            "labelled_combinations": coverage["labelled_target_systems"],
                            "labelled_simple": coverage["labelled_target_systems"],
                            "labelled_stacked": 0,
                            "canonical_simple_exact": count,
                            "shards": shard_count,
                            "disk_upper_bound_bytes": count * 20000,
                            "symmetry_estimate_simple_over_factorial": coverage["labelled_target_systems"] / 24,
                            "canonicalisation_comparisons": coverage["labelled_target_systems"] * 24,
                        }
                    },
                    "graded_coverage": coverage,
                    "control_3": catalogue["control_3"],
                }
            ],
            "shard_count": len(shards),
            "disk_upper_bound_bytes": count * 20000,
            "shard_items": items,
            "profile_note": PROFILE_NOTE,
            "workers_default": DEFAULT_WORKERS,
            "benchmark": timed,
            "effect_floor": floor,
            "catalogue_sha256": catalogue["sha256"],
        },
        "shards": shards,
    }


def execute_6_shard(task: dict) -> None:
    from rs_constraint_lab.census import _finish_receipt, _require_version

    _require_version(task)
    spec = dict(task["spec"])
    if spec.get("analysis") != ANALYSIS_6:
        raise RuntimeError("generation 6 shard received a different analysis")
    _require_lattice_spec(spec)
    require_effect_floor(spec)
    if int(spec.get("reconfiguration_horizon", RECONFIGURATION_HORIZON)) != RECONFIGURATION_HORIZON:
        raise RuntimeError("refusing to run: the horizon is not the predeclared value 16")
    spec["_spec_hash"] = task["identity"]["spec_hash"]
    catalogue = graded_catalogue(spec)
    if catalogue["sha256"] != task["identity"].get("catalogue_sha256"):
        raise RuntimeError("graded catalogue does not match the shard identity")
    if task["identity"].get("control_mapping_version") != CONTROL_MAPPING_VERSION:
        raise RuntimeError("control mapping version does not match the shard identity")
    if catalogue["coverage"]["canonical_target_systems"] > GRADED_POOL_CEILING:
        raise RuntimeError("graded pool exceeds the predeclared ceiling")
    shard_dir = Path(task["shard_dir"])
    shard_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(
        shard_dir / "running.json",
        {"shard_id": task["shard_id"], "attempt": task["attempt"], "started_at": _now(), "pid": _pid()},
    )
    started = time.perf_counter()
    grammar = _grammar(WEIGHT_ORDER, 4)
    cache: dict = {}
    rows = []
    start = int(task["start"])
    end = int(task["end"])
    for record in catalogue["records"][start:end]:
        rows.append(assess_target_row(record, spec, grammar, cache))
        _release_landings(cache)
    counts = {"analysed": len(rows), "solver_failures": 0, "start": start, "end": end}
    result = {"identity": task["identity"], "counts": counts, "graded_rows": rows}
    _finish_receipt(task, shard_dir, result, started, counts)


def _now() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _pid() -> int:
    import os

    return os.getpid()


def _direction_value(row: dict, direction: str, name: str):
    return row["directions"][direction]["target"].get(name)


def _margin_value(row: dict, direction: str, name: str):
    return row["directions"][direction].get(name)


def _select_one(rows: list[dict], direction: str, criterion: str) -> dict:
    finite = [row for row in rows if row["deletion_class"] == "neither_prohibit"]
    if criterion == "largest_finite_abs_I":
        ranked = sorted(finite, key=lambda row: (-abs(_direction_value(row, direction, "I")), row["target_id"]))
    elif criterion == "largest_finite_I_abs_margin":
        ranked = sorted(finite, key=lambda row: (-_margin_value(row, direction, "I_abs_margin"), row["target_id"]))
    elif criterion == "largest_finite_G_margin":
        ranked = sorted(finite, key=lambda row: (-_margin_value(row, direction, "G_margin"), row["target_id"]))
    elif criterion == "largest_finite_delta_S":
        ranked = sorted(finite, key=lambda row: (-_direction_value(row, direction, "delta_S"), row["target_id"]))
    elif criterion == "largest_negative_I_abs_margin":
        ranked = sorted(finite, key=lambda row: (_margin_value(row, direction, "I_abs_margin"), row["target_id"]))
    else:
        raise RuntimeError(f"unknown validation criterion {criterion}")
    if not ranked:
        raise RuntimeError("no finite-grade row is available for validation")
    return ranked[0]


def select_validation_rows(rows: list[dict]) -> dict:
    """Predeclared validation set. Criteria are not revised after the sort."""
    chosen = {}
    for direction in ("path_to_matching", "matching_to_path"):
        picks = {}
        for criterion in VALIDATION_CRITERIA:
            picks[criterion] = _select_one(rows, direction, criterion)["target_id"]
        chosen[direction] = picks
    anchors = [row["target_id"] for row in rows if row["deletion_class"] == "both_prohibit"]
    face_for_anchor = {}
    for row in rows:
        if row["deletion_class"] != "both_prohibit":
            continue
        face_for_anchor[row["target_id"]] = {}
        for direction in ("path_to_matching", "matching_to_path"):
            faces = [
                control
                for control in row["directions"][direction]["controls"]
                if control["role"] == "face" and control["I"] is not None
            ]
            winner = sorted(faces, key=lambda control: (-abs(control["I"]), control["control_id"]))[0]
            face_for_anchor[row["target_id"]][direction] = winner["control_id"]
    target_ids = []
    for direction_picks in chosen.values():
        for target_id in direction_picks.values():
            if target_id not in target_ids:
                target_ids.append(target_id)
    for target_id in anchors:
        if target_id not in target_ids:
            target_ids.append(target_id)
    return {
        "criteria": list(VALIDATION_CRITERIA),
        "by_direction": chosen,
        "anchor_target_ids": anchors,
        "strongest_anchor_face_by_direction": face_for_anchor,
        "target_ids": target_ids,
        "tie_rule": "earliest target_id at the exact maximum; a later row inside the effect floor is not added",
    }


def _continuity_bin(value: float | None) -> str | None:
    if value is None:
        return None
    for lower, upper, label in CONTINUITY_BINS:
        if lower <= value < upper or (upper == float("inf") and value >= lower):
            return label
    return None


def _distribution(values: list[float]) -> dict:
    xs = sorted(value for value in values if value is not None)
    if not xs:
        return {"count": 0}
    return {
        "count": len(xs),
        "min": xs[0],
        "median": float(statistics.median(xs)),
        "max": xs[-1],
    }


def _anchor_lookup(rows: list[dict]) -> dict:
    found = {}
    for row in rows:
        if row["deletion_class"] != "both_prohibit":
            continue
        found[(row["geometry"], row["polarity"])] = row
    return found


def _ratio_block(row: dict, anchor: dict, direction: str, floor: float) -> dict:
    target = row["directions"][direction]["target"]
    base = anchor["directions"][direction]["target"]
    i_den = abs(base["I"])
    r_i = None if i_den <= floor else abs(target["I"]) / i_den
    g_den = max(base["G"], floor)
    r_g = max(target["G"], 0.0) / g_den
    s_den = max(base["delta_S"], floor)
    r_s = max(target["delta_S"], 0.0) / s_den
    return {
        "R_I": r_i,
        "R_G": r_g,
        "R_S": r_s,
        "R_I_bin": _continuity_bin(r_i),
        "R_G_bin": _continuity_bin(r_g),
        "R_S_bin": _continuity_bin(r_s),
        "G_denominator_is_floor": base["G"] <= floor,
        "delta_S_denominator_is_floor": base["delta_S"] <= floor,
    }


def _surface(rows: list[dict]) -> dict:
    surface = {}
    for row in rows:
        for direction in ("path_to_matching", "matching_to_path"):
            key = f"{row['geometry']}|{row['polarity']}|{direction}"
            grid = surface.setdefault(key, {})
            cell = f"{row['w_P']}|{row['w_T']}"
            target = row["directions"][direction]["target"]
            grid[cell] = {
                "I": target["I"],
                "G": target["G"],
                "delta_S": target["delta_S"],
                "I_abs_margin": row["directions"][direction]["I_abs_margin"],
                "G_margin": row["directions"][direction]["G_margin"],
            }
    return surface


def _polarity_and_geometry(rows: list[dict], floor: float) -> dict:
    by_cell = {}
    for row in rows:
        for direction in ("path_to_matching", "matching_to_path"):
            target = row["directions"][direction]["target"]
            by_cell[(row["geometry"], row["polarity"], row["w_P"], row["w_T"], direction)] = target
    polarity = []
    geometries = sorted({row["geometry"] for row in rows})
    for geometry in geometries:
        for w_p in WEIGHT_ORDER:
            for w_t in WEIGHT_ORDER:
                for direction in ("path_to_matching", "matching_to_path"):
                    present = by_cell[(geometry, "present", w_p, w_t, direction)]
                    absent = by_cell[(geometry, "absent", w_p, w_t, direction)]
                    entry = {"geometry": geometry, "w_P": w_p, "w_T": w_t, "direction": direction}
                    for name in ("I", "G", "delta_S"):
                        difference = float(present[name] - absent[name])
                        entry[name] = {
                            "difference": difference,
                            "equal_within_floor": abs(difference) <= floor,
                            "sign_change": (present[name] > floor and absent[name] < -floor)
                            or (present[name] < -floor and absent[name] > floor),
                        }
                    polarity.append(entry)
    geometry_rows = []
    names = [name for name in geometries if name != "other"]
    if len(names) >= 2:
        left_name, right_name = names[0], names[1]
        for polarity_name in ("present", "absent"):
            for direction in ("path_to_matching", "matching_to_path"):
                separating = {quantity: None for quantity in ("I", "G", "delta_S")}
                ordered = sorted(
                    ((w_p, w_t) for w_p in WEIGHT_ORDER for w_t in WEIGHT_ORDER),
                    key=lambda item: (max(WEIGHT_INDEX[item[0]], WEIGHT_INDEX[item[1]]), WEIGHT_INDEX[item[0]], WEIGHT_INDEX[item[1]]),
                )
                for w_p, w_t in ordered:
                    left = by_cell[(left_name, polarity_name, w_p, w_t, direction)]
                    right = by_cell[(right_name, polarity_name, w_p, w_t, direction)]
                    for quantity in ("I", "G", "delta_S"):
                        difference = abs(float(left[quantity] - right[quantity]))
                        if separating[quantity] is None and difference > floor:
                            separating[quantity] = {
                                "w_P": w_p,
                                "w_T": w_t,
                                "absolute_difference": difference,
                            }
                geometry_rows.append(
                    {
                        "polarity": polarity_name,
                        "direction": direction,
                        "left_geometry": left_name,
                        "right_geometry": right_name,
                        "order": "chebyshev grade index from prohibit, then w_P, then w_T",
                        "first_separation": separating,
                    }
                )
    return {"polarity_cells": polarity, "geometry_separation": geometry_rows}


def _d_state_summary(target_states, target_values, control_states, control_values, floor: float) -> dict:
    target_map = {int(state): float(value) for state, value in zip(target_states, target_values)}
    control_map = {int(state): float(value) for state, value in zip(control_states, control_values)}
    states = sorted(set(target_map) & set(control_map))
    if not states:
        return {"defined": False}
    differences = [target_map[state] - control_map[state] for state in states]
    n_positive = sum(1 for value in differences if value > floor)
    n_negative = sum(1 for value in differences if value < -floor)
    if n_positive and n_negative:
        coherence = "mixed"
    elif n_positive:
        coherence = "positive"
    elif n_negative:
        coherence = "negative"
    else:
        coherence = "within_floor"
    order = sorted(range(len(states)), key=lambda index: abs(differences[index]), reverse=True)
    total = sum(abs(differences[index]) for index in order)
    top = order[:CONCENTRATION_TOP_STATES]
    top_share = None if total <= floor else sum(abs(differences[index]) for index in top) / total
    return {
        "defined": True,
        "coherence": coherence,
        "n_source_states": len(states),
        "n_positive": n_positive,
        "n_negative": n_negative,
        "top3_l1_share": top_share,
        "concentrated_on_top3": bool(top_share is not None and top_share >= CONCENTRATION_SHARE),
        "max_abs": max(abs(value) for value in differences),
    }


def _triad_sign_change(states, values, triads, floor: float) -> bool:
    buckets = defaultdict(list)
    for state, value, triad in zip(states, values, triads):
        buckets[int(triad)].append(float(value))
    signs = set()
    for bucket in buckets.values():
        mean = sum(bucket) / len(bucket)
        if mean > floor:
            signs.add(1)
        elif mean < -floor:
            signs.add(-1)
    return signs == {1, -1}


def validate_selected(spec: dict, rows: list[dict], selection: dict) -> dict:
    """State-resolved differences and rho/alphabet probes for the selected rows only."""
    floor = require_effect_floor(spec)
    grammar = _grammar(WEIGHT_ORDER, 4)
    catalogue = {row["target_id"]: row for row in graded_catalogue(spec)["records"]}
    by_id = {row["target_id"]: row for row in rows}
    probes = [
        ("W4_rho1", alphabet_factors("W4"), Fraction(1)),
        ("W4_rho1/2", alphabet_factors("W4"), Fraction(1, 2)),
        ("W4_rho2", alphabet_factors("W4"), Fraction(2)),
        ("W3_rho1", alphabet_factors("W3"), Fraction(1)),
        ("W16_rho1", alphabet_factors("W16"), Fraction(1)),
    ]
    validated = []
    probe_caches = {name: {} for name, _factors, _rho in probes}
    for target_id in selection["target_ids"]:
        record = catalogue[target_id]
        primary = by_id[target_id]
        probe_rows = {}
        for name, factors, rho in probes:
            store = name == "W4_rho1"
            probe_rows[name] = assess_target_row(
                record,
                spec,
                grammar,
                probe_caches[name],
                factors=factors,
                rho=rho,
                store_states=store,
            )
        replay_gap = 0.0
        for direction in ("path_to_matching", "matching_to_path"):
            for field in ("I", "G", "delta_S"):
                replay_gap = max(
                    replay_gap,
                    abs(
                        probe_rows["W4_rho1"]["directions"][direction]["target"][field]
                        - primary["directions"][direction]["target"][field]
                    ),
                )
            replay_gap = max(
                replay_gap,
                abs(
                    probe_rows["W4_rho1"]["directions"][direction]["I_abs_margin"]
                    - primary["directions"][direction]["I_abs_margin"]
                ),
            )
        state_reports = {}
        stored = probe_rows["W4_rho1"]
        for direction in ("path_to_matching", "matching_to_path"):
            target_direction = stored["directions"][direction]["target"]
            control_reports = []
            target_map = {
                int(state): float(value)
                for state, value in zip(target_direction["states"], target_direction["i_state"])
            }
            triad_of = {
                int(state): int(triad)
                for state, triad in zip(target_direction["states"], target_direction["triad"])
            }
            for control in stored["directions"][direction]["controls"]:
                summary = _d_state_summary(
                    target_direction["states"],
                    target_direction["i_state"],
                    control["states"],
                    control["i_state"],
                    floor,
                )
                control_map = {
                    int(state): float(value)
                    for state, value in zip(control["states"], control["i_state"])
                }
                shared = sorted(set(target_map) & set(control_map))
                summary["sign_changes_by_triad"] = _triad_sign_change(
                    shared,
                    [target_map[state] - control_map[state] for state in shared],
                    [triad_of[state] for state in shared],
                    floor,
                )
                summary["control_id"] = control["control_id"]
                summary["role"] = control["role"]
                control_reports.append(summary)
            state_reports[direction] = control_reports
        robustness = {}
        primary_probe = probe_rows["W4_rho1"]
        for name, _factors, _rho in probes:
            if name == "W4_rho1":
                continue
            other = probe_rows[name]
            direction_report = {}
            for direction in ("path_to_matching", "matching_to_path"):
                left = primary_probe["directions"][direction]
                right = other["directions"][direction]
                direction_report[direction] = {
                    "I_sign_same": _sign(left["target"]["I"], floor) == _sign(right["target"]["I"], floor),
                    "I_abs_margin_sign_same": _sign(left["I_abs_margin"], floor) == _sign(right["I_abs_margin"], floor),
                    "G_margin_sign_same": _sign(left["G_margin"], floor) == _sign(right["G_margin"], floor),
                    "delta_S_sign_same": _sign(left["target"]["delta_S"], floor) == _sign(right["target"]["delta_S"], floor),
                    "target_exceeds_controls_abs_I_same": (left["I_abs_margin"] > floor) == (right["I_abs_margin"] > floor),
                    "I": right["target"]["I"],
                    "I_abs_margin": right["I_abs_margin"],
                    "G_margin": right["G_margin"],
                    "delta_S": right["target"]["delta_S"],
                }
            robustness[name] = direction_report
        direct_gap = _direct_iterative_gap(record, spec, grammar)
        validated.append(
            {
                "target_id": target_id,
                "expressions": record["expressions"],
                "geometry": record["geometry"],
                "polarity": record["polarity"],
                "w_P": record["w_P"],
                "w_T": record["w_T"],
                "deletion_class": record["deletion_class"],
                "replay_gap": replay_gap,
                "direct_vs_iterative_committor": direct_gap,
                "state_resolved": state_reports,
                "robustness": robustness,
                "alphabet_note": (
                    "W3 and W16 keep the grade names and change the base from 2 to 3 and 4. "
                    "prohibit remains the multiplicative zero. rho3 rescales the baseline weight "
                    "of triad slots and does not rename a grade."
                ),
            }
        )
    return _num(
        {
            "selection": selection,
            "rows": validated,
            "concentration_rule": {
                "top_states": CONCENTRATION_TOP_STATES,
                "share": CONCENTRATION_SHARE,
                "meaning": "descriptive cut, not a success threshold",
            },
        }
    )


def _sign(value, floor: float) -> str:
    if value is None:
        return "undefined"
    if abs(value) <= floor:
        return "zero"
    return "positive" if value > 0.0 else "negative"


def _direct_iterative_gap(record: dict, spec: dict, grammar) -> float:
    floor = require_effect_floor(spec)
    slots = grammar.slot_list()
    factors = alphabet_factors(spec["alphabet"])
    cache: dict = {}
    baseline = _baseline_pack(factors, PRIMARY_RHO, slots, cache)
    members = _constraints_of(grammar, record["canonical_ids"])
    t_rule, p_rule = _roles(members, slots)
    pack = _constrained_pack((t_rule, p_rule), factors, PRIMARY_RHO, slots, cache)
    _n_pairs, class_index, table = kernel_layout_index(pack["kernel"])
    worst = 0.0
    for source_name, target_name in (
        (table.path_name, table.matching_name),
        (table.matching_name, table.path_name),
    ):
        source = baseline["positions"][source_name]
        target = baseline["positions"][target_name]
        direct = eventual_committor(pack["landing"], class_index, source, target)
        iterated = eventual_committor(pack["landing"], class_index, source, target, method="iterative")
        both = np.isfinite(direct["q"]) & np.isfinite(iterated["q"])
        worst = max(worst, float(np.max(np.abs(direct["q"][both] - iterated["q"][both]))))
    if worst > floor:
        return worst
    return worst


def summarise_graded(rows: list[dict], floor: float) -> dict:
    anchors = _anchor_lookup(rows)
    grouped = {name: [] for name in ("both_prohibit", "exactly_one_prohibit", "neither_prohibit")}
    control_spreads = []
    ratios = []
    for row in rows:
        for direction in ("path_to_matching", "matching_to_path"):
            target = row["directions"][direction]["target"]
            margin = row["directions"][direction]
            bucket = grouped[row["deletion_class"]]
            bucket.append(
                {
                    "direction": direction,
                    "abs_I": abs(target["I"]),
                    "G": target["G"],
                    "delta_S": target["delta_S"],
                    "I_abs_margin": margin["I_abs_margin"],
                    "G_margin": margin["G_margin"],
                }
            )
            for control in margin["controls"]:
                for field in ("S_T", "S_TP", "delta_S"):
                    if control.get(field) is not None:
                        control_spreads.append(abs(control[field]))
            if row["deletion_class"] != "both_prohibit":
                ratios.append(
                    {
                        "target_id": row["target_id"],
                        "deletion_class": row["deletion_class"],
                        "geometry": row["geometry"],
                        "polarity": row["polarity"],
                        "w_P": row["w_P"],
                        "w_T": row["w_T"],
                        "direction": direction,
                        **_ratio_block(row, anchors[(row["geometry"], row["polarity"])], direction, floor),
                    }
                )
    def _count(predicate) -> int:
        return sum(1 for row in rows if predicate(row))

    finite = [row for row in rows if row["deletion_class"] == "neither_prohibit"]
    questions = {}
    for direction in ("path_to_matching", "matching_to_path"):
        finite_dir = []
        for row in finite:
            target = row["directions"][direction]["target"]
            margin = row["directions"][direction]
            finite_dir.append((row, target, margin))
        questions[direction] = {
            "finite_rows": len(finite_dir),
            "abs_I_above_floor": sum(1 for _row, target, _margin in finite_dir if abs(target["I"]) > floor),
            "G_positive_above_floor": sum(1 for _row, target, _margin in finite_dir if target["G"] > floor),
            "delta_S_positive_above_floor": sum(1 for _row, target, _margin in finite_dir if target["delta_S"] > floor),
            "I_abs_margin_positive": sum(1 for _row, _target, margin in finite_dir if margin["I_abs_margin"] > floor),
            "G_margin_positive": sum(1 for _row, _target, margin in finite_dir if margin["G_margin"] > floor),
            "target_I_distribution": _distribution([abs(target["I"]) for _row, target, _margin in finite_dir]),
            "erased_abs_I_distribution": _distribution(
                [
                    abs(control["I"])
                    for _row, _target, margin in finite_dir
                    for control in margin["controls"]
                    if control["role"] == "erased"
                ]
            ),
            "face_abs_I_distribution": _distribution(
                [
                    abs(control["I"])
                    for _row, _target, margin in finite_dir
                    for control in margin["controls"]
                    if control["role"] == "face"
                ]
            ),
        }
    group_summary = {}
    for name, bucket in grouped.items():
        group_summary[name] = {
            "rows_times_directions": len(bucket),
            "abs_I": _distribution([item["abs_I"] for item in bucket]),
            "G": _distribution([item["G"] for item in bucket]),
            "delta_S": _distribution([item["delta_S"] for item in bucket]),
            "I_abs_margin": _distribution([item["I_abs_margin"] for item in bucket]),
            "G_margin": _distribution([item["G_margin"] for item in bucket]),
        }
    ratio_bins = {}
    for deletion in ("neither_prohibit", "exactly_one_prohibit"):
        ratio_bins[deletion] = {}
        for field in ("R_I_bin", "R_G_bin", "R_S_bin"):
            ratio_bins[deletion][field] = dict(Counter(item[field] for item in ratios if item["deletion_class"] == deletion))
    return {
        "effect_floor": floor,
        "systems": len(rows),
        "support_violation_systems": _count(lambda row: row.get("support_violations")),
        "support_removed_systems": _count(lambda row: row.get("support_removed")),
        "max_residual": max((row["max_residual"] or 0.0) for row in rows) if rows else None,
        "pairwise_control_spread_max": max(control_spreads) if control_spreads else None,
        "pairwise_control_spread_above_floor": sum(1 for value in control_spreads if value > floor),
        "group_distributions": group_summary,
        "continuity_bins": ratio_bins,
        "by_direction": questions,
        "surface": _surface(rows),
        "symmetry": _polarity_and_geometry(rows, floor),
        "ratios": ratios,
    }


def _write_csv(path: Path, rows: list[dict], floor: float) -> None:
    import csv

    anchors = _anchor_lookup(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "target_id",
        "geometry",
        "polarity",
        "w_P",
        "w_T",
        "deletion_class",
        "direction",
        "I",
        "G",
        "delta_S",
        "delta_TP",
        "state_sign",
        "I_erased",
        "G_erased",
        "face_control_ids",
        "face_I",
        "face_G",
        "control_abs_I_max",
        "I_abs_margin",
        "control_G_max",
        "G_margin",
        "I_ratio",
        "R_I",
        "R_G",
        "R_S",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            ratios = None
            if row["deletion_class"] != "both_prohibit":
                ratios = {
                    direction: _ratio_block(row, anchors[(row["geometry"], row["polarity"])], direction, floor)
                    for direction in ("path_to_matching", "matching_to_path")
                }
            for direction in ("path_to_matching", "matching_to_path"):
                block = row["directions"][direction]
                target = block["target"]
                erased = next(control for control in block["controls"] if control["role"] == "erased")
                faces = [control for control in block["controls"] if control["role"] == "face"]
                ratio = None if ratios is None else ratios[direction]
                writer.writerow(
                    {
                        "target_id": row["target_id"],
                        "geometry": row["geometry"],
                        "polarity": row["polarity"],
                        "w_P": row["w_P"],
                        "w_T": row["w_T"],
                        "deletion_class": row["deletion_class"],
                        "direction": direction,
                        "I": target["I"],
                        "G": target["G"],
                        "delta_S": target["delta_S"],
                        "delta_TP": target["delta_TP"],
                        "state_sign": target["state_sign"]["coherence"],
                        "I_erased": erased["I"],
                        "G_erased": erased["G"],
                        "face_control_ids": ";".join(control["control_id"] for control in faces),
                        "face_I": ";".join(str(control["I"]) for control in faces),
                        "face_G": ";".join(str(control["G"]) for control in faces),
                        "control_abs_I_max": block["control_abs_I_max"],
                        "I_abs_margin": block["I_abs_margin"],
                        "control_G_max": block["control_G_max"],
                        "G_margin": block["G_margin"],
                        "I_ratio": block["I_ratio"],
                        "R_I": None if ratio is None else ratio["R_I"],
                        "R_G": None if ratio is None else ratio["R_G"],
                        "R_S": None if ratio is None else ratio["R_S"],
                    }
                )


def merge_v06(out_dir: Path, plan: dict, publish: Path | None = None) -> dict:
    from rs_constraint_lab.execution import _fingerprint, _reconcile
    from rs_constraint_lab.generation import _git_commit, _publish
    from rs_constraint_lab.version import EXECUTION_PRINCIPLE, MAX_ATTEMPTS, PROFILE_NOTE

    out_dir = Path(out_dir)
    progress = _reconcile(out_dir, plan)
    spec = plan["spec"]
    floor = require_effect_floor(spec)
    rows: list[dict] = []
    work = 0.0
    analysed = 0
    for shard in plan["shards"]:
        state = progress["shards"][shard["shard_id"]]
        if state["status"] != "completed":
            continue
        result = read_json(out_dir / "shards" / shard["shard_id"] / "result.json")
        rows.extend(result.get("graded_rows") or [])
        analysed += int(result["counts"].get("analysed", 0))
        receipt = read_json(out_dir / "shards" / shard["shard_id"] / "receipt.json")
        work += float(receipt.get("elapsed_seconds") or 0.0)
    cell = spec["cells"][0]
    n = int(cell["N"])
    k_max = int(cell["K_max"])
    v06_summary = None
    if progress["status"] == "COMPLETE":
        expected = plan["estimates"]["cells"][0]["cardinalities"]["2"]["canonical_simple_exact"]
        if analysed != expected:
            raise RuntimeError(f"generation 6 analysed {analysed}, planned {expected}")
        summary_numbers = summarise_graded(rows, floor)
        selection = select_validation_rows(rows)
        validation = validate_selected(spec, rows, selection)
        v06_summary = {
            "coverage": plan["estimates"]["cells"][0]["graded_coverage"],
            "control_3": plan["estimates"]["cells"][0]["control_3"],
            "questions": summary_numbers,
            "validation": validation,
            "benchmark": plan["estimates"].get("benchmark"),
        }
        _write_csv(out_dir / f"singles-n{n}-k{k_max}.csv", rows, floor)
        atomic_write_json(out_dir / "graded-surface.json", json_ready(summary_numbers["surface"]))
    estimate = plan["estimates"]["cells"][0]
    summary = {
        "status": progress["status"],
        "engine_version": plan["header"]["engine_version"],
        "semantic_version": plan["header"]["semantic_version"],
        "git_commit": _git_commit(),
        "python": __import__("sys").version.split()[0],
        "numpy": np.__version__,
        "platform": __import__("sys").platform,
        "spec_hash": plan["header"]["spec_hash"],
        "experiment_id": spec["experiment_id"],
        "generation": spec["generation"],
        "composition": spec.get("composition", "structural-simple"),
        "predicates": list(spec.get("predicates", [])),
        "analysis": spec.get("analysis"),
        "analysis_version": spec.get("analysis_version", ANALYSIS_VERSION),
        "control_mapping_version": CONTROL_MAPPING_VERSION,
        "normalisation_version": plan["header"]["normalisation_version"],
        "grammar_version": plan["header"]["grammar_version"],
        "runtime_seconds": 0.0,
        "shard_work_seconds": work,
        "receipt_fingerprint": _fingerprint(out_dir, plan),
        "execution": {
            "workers_last": progress.get("workers_last"),
            "worker_history": progress.get("worker_history", []),
            "shard_items": plan["header"]["shard_items"],
            "shard_count": plan["estimates"]["shard_count"],
            "max_attempts": MAX_ATTEMPTS,
            "multiprocessing": "spawn",
            "principle": EXECUTION_PRINCIPLE,
            "profile_note": PROFILE_NOTE,
        },
        "cells": [
            {
                "coordinate": {
                    "N": n,
                    "A_max": cell.get("A_max"),
                    "O": 3,
                    "G": 0,
                    "S": 0,
                    "H": 0,
                    "K_max": k_max,
                    "L": 0,
                    "semantics": "hypergraph",
                    "alphabet": spec["alphabet"],
                    "composition": spec.get("composition", "structural-simple"),
                    "predicates": list(spec.get("predicates", ["pair", "triad"])),
                    "analysis": spec.get("analysis"),
                },
                "runtime_seconds": work,
                "accounting": {"edge": estimate["edge_accounting"], "grammar": estimate["grammar"]},
                "canonical_states": estimate.get("canonical_states"),
                "relation_slots": estimate["edge_accounting"]["relation_slots"],
                "labelled_states": estimate["labelled_states"],
                "cardinalities": {
                    "2": {
                        "labelled_combinations": estimate["cardinalities"]["2"].get("labelled_combinations"),
                        "labelled_simple": estimate["cardinalities"]["2"].get("labelled_simple"),
                        "labelled_stacked": estimate["cardinalities"]["2"].get("labelled_stacked"),
                        "canonical": analysed,
                        "analysed": analysed,
                    }
                },
                "families": 0,
                "family_histogram": {},
                "structural_families": 0,
                "screened_families": 0,
                "baseline_equivalent_families": 0,
                "cancellations": {},
                "extremes": {},
                "family_index_sha256": "",
                "singles_sha256": sha256_file(out_dir / f"singles-n{n}-k{k_max}.csv")
                if (out_dir / f"singles-n{n}-k{k_max}.csv").exists()
                else "",
                "kernel_index_sha256": "",
                "kernel_index_count": 0,
                "qualitative_index_sha256": "",
                "observable_index_sha256": "",
                "v06_census": v06_summary,
            }
        ],
        "unsearched_declared": list(spec.get("unsearched", [])),
        "territory": None,
        "effect_floor": floor,
        "effect_floor_reason": spec.get("effect_floor_reason"),
        "v06": v06_summary,
    }
    atomic_write_json(out_dir / "summary.json", json_ready(_num(summary)))
    if publish is not None and summary["status"] == "COMPLETE":
        _publish(summary, spec, Path(publish), out_dir)
        tables = Path(publish) / "reports" / "tables"
        tables.mkdir(parents=True, exist_ok=True)
        surface = out_dir / "graded-surface.json"
        if surface.exists():
            target = tables / f"{spec['experiment_id']}-graded-surface.json"
            target.write_text(surface.read_text(encoding="utf-8"), encoding="utf-8")
    return summary
