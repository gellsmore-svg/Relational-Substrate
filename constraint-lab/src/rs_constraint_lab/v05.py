"""Generation 4a reanalysis and the Generation 5 targeted pair census.

Generation 4's outputs are not rewritten here. 4a recomputes the focused
horizon-16 passage under matched baselines, then separates source occupancy
from future dynamics. Generation 5 canonicalises complete ``T->P`` plus
``P->P`` sets under S4. It does not multiply singleton orbit counts, and it
does not execute the full cardinality-2 grammar.
"""

from __future__ import annotations

import hashlib
import json
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np

from rs_constraint_lab.constraints import cross_order_class, structurally_simple
from rs_constraint_lab.durable import atomic_write_json, json_ready, read_json, sha256_file
from rs_constraint_lab.grammar import build_grammar, canonical_id_tuple
from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.memory_clocks import epoch_kernel_block, float_stationary
from rs_constraint_lab.passage import (
    PATH_CLASS,
    MATCHING_CLASS,
    class_position,
    eventual_committor,
    hit_passage,
    interaction_residual,
    kernel_layout_index,
    prepare_direction,
    reference_source,
    sign_status,
    state_interaction,
    state_summary,
    stationary_source_mu,
    super_singleton_gap,
)
from rs_constraint_lab.reconfiguration import RECONFIGURATION_HORIZON, focused_transition
from rs_constraint_lab.version import HYPERGRAPH_N4_SEMANTIC_VERSION, hypergraph_version_for_n
from rs_constraint_lab.weights import alphabet_factors

ANALYSIS_4A = "n4-reconfiguration-sensitivity"
ANALYSIS_5 = "n4-targeted-pairs"
ANALYSIS_VERSION = "0.5.0"
# A pool above this bound is not executed. The runner must not sample it.
TARGETED_POOL_CEILING = 20000
PRIMARY_ALPHABET = "W4"
PRIMARY_RHO = Fraction(1)


def _num(value):
    if isinstance(value, np.ndarray):
        return [_num(item) for item in value.tolist()]
    if isinstance(value, np.floating):
        number = float(value)
        if number != number or number in {float("inf"), float("-inf")}:
            return None
        return number
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, float):
        if value != value or value in {float("inf"), float("-inf")}:
            return None
        return value
    if isinstance(value, dict):
        return {str(key): _num(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_num(item) for item in value]
    return value


def _factors_key(factors: dict) -> tuple:
    return tuple((name, str(value)) for name, value in sorted(factors.items()))


def _grammar(weights, a_max=4):
    return build_grammar(4, 2, tuple(weights), a_max=a_max, predicates=("pair", "triad"), order=3)


def _stem(constraint, grammar, index: int, slots) -> str:
    best = None
    for row in grammar.image:
        text = grammar.labelled[row[index]].expression(slots).split(" => ", 1)[0]
        if best is None or text < best:
            best = text
    return best


def _edge_relation(left: tuple[int, ...], right: tuple[int, ...]) -> str:
    if left == right:
        return "same"
    if set(left) & set(right):
        return "adjacent"
    return "disjoint"


def _triad_vs_edge(triad: tuple[int, ...], edge: tuple[int, ...]) -> str:
    shared = set(edge) & set(triad)
    if set(edge) <= set(triad):
        return "contains_acted_edge"
    if len(shared) == 1:
        return "intersects_one_vertex"
    if not shared:
        return "disjoint"
    return "other_overlap"


def _vertices_vs_triad(vertices: set[int], triad: tuple[int, ...]) -> str:
    if not vertices & set(triad):
        return "disjoint"
    if vertices <= set(triad):
        return "contained"
    return "partial_overlap"


def alignment_signature(tp, pp, grammar, tp_index: int, pp_index: int, slots) -> dict:
    """Categorical relative alignment of one canonical two-rule representative."""
    tp_action = slots[tp.action]
    pp_action = slots[pp.action]
    tp_condition = slots[tp.conditions[0][0]] if tp.conditions else None
    pp_conditions = [slots[slot] for slot, _bit in pp.conditions]
    pp_vertices = set(pp_action)
    for slot in pp_conditions:
        pp_vertices.update(slot)
    return {
        "tp_orbit": _stem(tp, grammar, tp_index, slots),
        "pp_orbit": _stem(pp, grammar, pp_index, slots),
        "tp_weight": tp.weight,
        "pp_weight": pp.weight,
        "tp_k": tp.k(),
        "pp_k": pp.k(),
        "action_edge_relation": _edge_relation(pp_action, tp_action),
        "tp_condition_vs_action": None if tp_condition is None else _triad_vs_edge(tp_condition, tp_action),
        "pp_vertices_vs_tp_triad": None if tp_condition is None else _vertices_vs_triad(pp_vertices, tp_condition),
        "pp_condition_count": len(pp_conditions),
    }


def targeted_catalogue(spec: dict) -> dict:
    """Exact S4 census of weighted ``T->P`` plus ``P->P`` sets.

    Rules are labelled first. Weights are assigned independently. The
    complete two-rule set is then canonicalised. Component orbits are not
    multiplied.
    """
    weights = tuple(spec.get("weights", ("prohibit", "strong_favour")))
    grammar = _grammar(weights, spec["cells"][0].get("A_max", 4))
    slots = grammar.slot_list()
    n_pairs = sum(1 for slot in grammar.relation_slots if len(slot) == 2)
    tp_ids = [index for index, constraint in enumerate(grammar.labelled) if cross_order_class(constraint, n_pairs) == "T->P"]
    pp_ids = [index for index, constraint in enumerate(grammar.labelled) if cross_order_class(constraint, n_pairs) == "P->P"]
    tp_structural = {grammar.labelled[index].structural_key() for index in tp_ids}
    pp_structural = {grammar.labelled[index].structural_key() for index in pp_ids}
    orbit_sizes: Counter = Counter()
    invalid = 0
    labelled_pairs = 0
    for left in tp_ids:
        for right in pp_ids:
            labelled_pairs += 1
            pair = (grammar.labelled[left], grammar.labelled[right])
            if not structurally_simple(pair):
                invalid += 1
                continue
            canon = canonical_id_tuple((left, right), grammar.image)
            orbit_sizes[canon] += 1
    representatives = tuple(sorted(orbit_sizes))
    for canon in representatives:
        classes = {cross_order_class(grammar.labelled[index], n_pairs) for index in canon}
        if classes != {"T->P", "P->P"}:
            raise RuntimeError(f"canonical pair {canon} is not one T->P rule and one P->P rule")
    structural = _grammar((weights[0],), spec["cells"][0].get("A_max", 4))
    structural_index = {constraint.structural_key(): index for index, constraint in enumerate(structural.labelled)}
    structural_canons = set()
    alignments = []
    expressions = []
    for canon in representatives:
        by_class = {}
        for index in canon:
            constraint = grammar.labelled[index]
            by_class[cross_order_class(constraint, n_pairs)] = (index, constraint)
        pp_index, pp = by_class["P->P"]
        tp_index, tp = by_class["T->P"]
        alignments.append(alignment_signature(tp, pp, grammar, tp_index, pp_index, slots))
        expressions.append([pp.expression(slots), tp.expression(slots)])
        structural_ids = tuple(
            structural_index[grammar.labelled[index].structural_key()] for index in canon
        )
        structural_canons.add(canonical_id_tuple(structural_ids, structural.image))
    payload = json.dumps([list(item) for item in representatives], separators=(",", ":"))
    coverage = {
        "labelled_tp_structural": len(tp_structural),
        "labelled_pp_structural": len(pp_structural),
        "labelled_tp_weighted": len(tp_ids),
        "labelled_pp_weighted": len(pp_ids),
        "weighted_labelled_pairs": labelled_pairs,
        "invalid_pairs": invalid,
        "canonical_weighted_pairs": len(representatives),
        "canonical_structural_pairs": len(structural_canons),
        "weight_grid_8x10x2x2": 320,
        "weight_grid_is_the_canonical_count": False,
        "orbit_size_distribution": {
            str(size): count for size, count in sorted(Counter(orbit_sizes.values()).items())
        },
        "labelled_pairs_accounted": int(sum(orbit_sizes.values()) + invalid),
    }
    return {
        "grammar_weights": list(weights),
        "representatives": representatives,
        "expressions": expressions,
        "alignments": alignments,
        "coverage": coverage,
        "sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
    }


def require_effect_floor(spec: dict) -> float:
    if "effect_floor" not in spec:
        raise ValueError("effect_floor must be declared before a v0.5 census runs")
    floor = float(spec["effect_floor"])
    if floor <= 0.0:
        raise ValueError("effect_floor must be positive")
    return floor


def _baseline_pack(factors, rho: Fraction, slots, cache: dict) -> dict:
    key = ("baseline", _factors_key(factors), str(rho))
    if key in cache:
        return cache[key]
    from rs_constraint_lab.census import build_slotted

    kernel = build_slotted(4, (), factors, slots, rho)
    pi, residual, arithmetic, periods = float_stationary(kernel)
    landing, defect = epoch_kernel_block(kernel)
    if landing is None or defect is None:
        raise RuntimeError("baseline block epoch solver failed")
    n_pairs, class_index, table = kernel_layout_index(kernel)
    own = stationary_source_mu(kernel, pi, landing)
    refs = {}
    positions = {}
    for name in (PATH_CLASS, MATCHING_CLASS):
        position = class_position(table, name)
        positions[name] = position
        refs[name] = reference_source(own, class_index, position)
    cache[key] = {
        "kernel": kernel,
        "pi": pi,
        "residual": float(residual),
        "arithmetic": arithmetic,
        "periods": list(periods),
        "landing": landing,
        "defect": float(defect),
        "n_pairs": n_pairs,
        "class_index": class_index,
        "table": table,
        "mu_ref": refs,
        "positions": positions,
    }
    return cache[key]


def _constrained_pack(constraints, factors, rho: Fraction, slots, cache: dict) -> dict:
    key = (tuple(constraint.key() for constraint in constraints), _factors_key(factors), str(rho))
    if key in cache:
        return cache[key]
    from rs_constraint_lab.census import build_slotted

    kernel = build_slotted(4, constraints, factors, slots, rho)
    pi, residual, arithmetic, periods = float_stationary(kernel)
    landing, defect = epoch_kernel_block(kernel)
    if landing is None or defect is None:
        raise RuntimeError("block epoch solver failed")
    cache[key] = {
        "kernel": kernel,
        "pi": pi,
        "residual": float(residual),
        "arithmetic": arithmetic,
        "periods": list(periods),
        "landing": landing,
        "defect": float(defect),
    }
    return cache[key]


def _hit_fields(focused: dict, baseline: dict, floor: float) -> dict:
    hit = (focused.get("passage") or {}).get("hit_before_return")
    base_hit = (baseline.get("passage") or {}).get("hit_before_return")
    delta = None if hit is None or base_hit is None else float(hit - base_hit)
    unresolved = (focused.get("passage") or {}).get("unresolved_within_horizon")
    spread_value = focused.get("triad_hit_spread")
    spread = None if spread_value is None else float(spread_value)
    return {
        "hit_before_return": None if hit is None else float(hit),
        "baseline_hit_before_return": None if base_hit is None else float(base_hit),
        "delta_hit_before_return": delta,
        "triad_hit_spread": spread,
        "triad_changes_hit": bool(spread is not None and spread > floor),
        "unresolved_within_horizon": None if unresolved is None else float(unresolved),
        "mean_status": (focused.get("passage") or {}).get("mean_status"),
        "sign": sign_status(delta, floor),
    }


def _direction_names(table):
    return (
        ("path_to_matching", table.path_name, table.matching_name),
        ("matching_to_path", table.matching_name, table.path_name),
    )


def assess_singleton_row(constraint, spec: dict, slots, cache: dict) -> dict:
    """Horizon-16 sensitivity plus the primary controlled eventual committor."""
    floor = require_effect_floor(spec)
    from rs_constraint_lab.census import build_slotted

    probes = [("primary", PRIMARY_ALPHABET, PRIMARY_RHO)]
    for label in spec.get("rho3_sensitivity", ["1/2", "1", "2"]):
        if label in {"1", "1/1"}:
            continue
        probes.append((f"rho{label}", PRIMARY_ALPHABET, Fraction(label)))
    for name in spec.get("sensitivity_alphabets", ["W3", "W16"]):
        probes.append((name, name, PRIMARY_RHO))
    horizon = int(spec.get("reconfiguration_horizon", RECONFIGURATION_HORIZON))
    if horizon != RECONFIGURATION_HORIZON:
        raise RuntimeError("refusing to run: the horizon is not the predeclared value 16")
    directions = {}
    residuals = []
    for probe_name, alphabet, rho in probes:
        factors = alphabet_factors(alphabet)
        baseline = _baseline_pack(factors, rho, slots, cache)
        kernel = build_slotted(4, (constraint,), factors, slots, rho)
        pi, residual, _arithmetic, _periods = float_stationary(kernel)
        landing, defect = epoch_kernel_block(kernel)
        if landing is None or defect is None:
            raise RuntimeError(f"block epoch solver failed for {probe_name}")
        residuals.append(float(residual))
        table = baseline["table"]
        probe_directions = {}
        for key, source_name, target_name in _direction_names(table):
            focused = focused_transition(kernel, pi, landing, source_name, target_name, table, horizon)
            base_focused = focused_transition(
                baseline["kernel"], baseline["pi"], baseline["landing"], source_name, target_name, table, horizon
            )
            fields = _hit_fields(focused, base_focused, floor)
            controlled = hit_passage(
                landing,
                baseline["mu_ref"][source_name],
                baseline["class_index"],
                baseline["positions"][source_name],
                baseline["positions"][target_name],
                horizon,
            )
            base_controlled = hit_passage(
                baseline["landing"],
                baseline["mu_ref"][source_name],
                baseline["class_index"],
                baseline["positions"][source_name],
                baseline["positions"][target_name],
                horizon,
            )
            controlled_hit = controlled.get("hit_before_return")
            base_controlled_hit = base_controlled.get("hit_before_return")
            controlled_delta = None
            if controlled_hit is not None and base_controlled_hit is not None:
                controlled_delta = float(controlled_hit - base_controlled_hit)
            fields["controlled_hit_before_return"] = None if controlled_hit is None else float(controlled_hit)
            fields["controlled_baseline_hit_before_return"] = None if base_controlled_hit is None else float(base_controlled_hit)
            fields["controlled_delta_hit_before_return"] = controlled_delta
            fields["controlled_sign"] = sign_status(controlled_delta, floor)
            fields["baseline_alphabet"] = alphabet
            fields["baseline_rho"] = str(rho)
            fields["source_distribution"] = "STATIONARY_SOURCE_PASSAGE"
            fields["controlled_source_distribution"] = "CONTROLLED_SOURCE_PASSAGE"
            if probe_name == "primary":
                solved = prepare_direction(
                    kernel,
                    pi,
                    landing,
                    baseline["class_index"],
                    baseline["n_pairs"],
                    baseline["positions"][source_name],
                    baseline["positions"][target_name],
                    baseline["mu_ref"][source_name],
                    horizon=horizon,
                )
                base_solved = prepare_direction(
                    baseline["kernel"],
                    baseline["pi"],
                    baseline["landing"],
                    baseline["class_index"],
                    baseline["n_pairs"],
                    baseline["positions"][source_name],
                    baseline["positions"][target_name],
                    baseline["mu_ref"][source_name],
                    horizon=horizon,
                )
                if solved["mu_ref"] is not baseline["mu_ref"][source_name]:
                    raise RuntimeError("controlled source was replaced")
                if base_solved["mu_ref"] is not baseline["mu_ref"][source_name]:
                    raise RuntimeError("baseline controlled source was replaced")
                q_delta = solved["q"] - base_solved["q"]
                summary = state_summary(q_delta, baseline["mu_ref"][source_name], baseline["n_pairs"])
                stat_delta = None
                ctrl_delta = None
                if solved["q_stationary"] is not None and base_solved["q_stationary"] is not None:
                    stat_delta = float(solved["q_stationary"] - base_solved["q_stationary"])
                if solved["q_controlled"] is not None and base_solved["q_controlled"] is not None:
                    ctrl_delta = float(solved["q_controlled"] - base_solved["q_controlled"])
                occupancy = None if stat_delta is None or ctrl_delta is None else float(stat_delta - ctrl_delta)
                h16_occupancy = None
                if fields["delta_hit_before_return"] is not None and controlled_delta is not None:
                    h16_occupancy = float(fields["delta_hit_before_return"] - controlled_delta)
                spread = solved["triad"].get("spread")
                fields["eventual"] = {
                    "q_stationary": solved["q_stationary"],
                    "q_controlled": solved["q_controlled"],
                    "baseline_q_stationary": base_solved["q_stationary"],
                    "baseline_q_controlled": base_solved["q_controlled"],
                    "delta_stationary": stat_delta,
                    "delta_controlled": ctrl_delta,
                    "occupancy_contribution": occupancy,
                    "horizon16_occupancy_contribution": h16_occupancy,
                    "triad_spread": None if spread is None else float(spread),
                    "triad_min": solved["triad"].get("min"),
                    "triad_max": solved["triad"].get("max"),
                    "triad_min_configurations": solved["triad"].get("min_configurations"),
                    "triad_max_configurations": solved["triad"].get("max_configurations"),
                    "triad_changes": bool(spread is not None and spread > floor),
                    "sign_controlled": sign_status(ctrl_delta, floor),
                    "solver": solved["solver"],
                    "baseline_solver": base_solved["solver"],
                    "state": summary,
                }
                residuals.append(float(solved["solver"]["residual"] or 0.0))
            probe_directions[key] = fields
        directions[probe_name] = probe_directions
    expression = constraint.expression(slots)
    return _num(
        {
            "expression": expression,
            "k": constraint.k(),
            "cross_order_class": cross_order_class(constraint, 6),
            "weight": constraint.weight,
            "probes": directions,
            "max_stationary_residual": max(residuals) if residuals else None,
            "epoch_solver": "block",
        }
    )


def _support_violations(smaller, larger) -> int:
    """Relational toggles present in ``smaller`` and absent from ``larger``.

    Deadlock self-loops are not relational events and are not counted.
    """
    violations = 0
    for source, row in enumerate(smaller.successors):
        if smaller.deadlock[source]:
            continue
        allowed = {
            target
            for target, prob in larger.successors[source]
            if prob and target != source and not larger.deadlock[source]
        }
        for target, prob in row:
            if prob and target != source and target not in allowed:
                violations += 1
    return violations


def _pack_key(constraints, factors, rho: Fraction):
    return (tuple(constraint.key() for constraint in constraints), _factors_key(factors), str(rho))


def _evict_pack(cache: dict, constraints, factors, rho: Fraction) -> None:
    """Drop a pair landing after its compact row is stored.

    Singleton packs stay. A shard must not retain one 1024-by-1024 landing
    for every pair it analyses.
    """
    cache.pop(_pack_key(constraints, factors, rho), None)


def _pair_identifier(spec: dict, expressions: list[str]) -> str:
    payload = json.dumps(
        {
            "analysis_version": spec.get("analysis_version", ANALYSIS_VERSION),
            "expressions": list(expressions),
            "semantic_version": HYPERGRAPH_N4_SEMANTIC_VERSION,
            "spec_hash": spec.get("_spec_hash"),
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]


def _cached_direction(pack: dict, baseline: dict, source_name: str, target_name: str, horizon: int) -> dict:
    """Solve one direction once per kernel. Later pairs reuse the same ``mu_ref``."""
    key = (source_name, target_name, int(horizon))
    store = pack.setdefault("directions_cache", {})
    if key not in store:
        if pack.get("landing") is None or pack.get("kernel") is None or pack.get("pi") is None:
            raise RuntimeError("pair-event landing was released before this direction was solved")
        store[key] = prepare_direction(
            pack["kernel"],
            pack["pi"],
            pack["landing"],
            baseline["class_index"],
            baseline["n_pairs"],
            baseline["positions"][source_name],
            baseline["positions"][target_name],
            baseline["mu_ref"][source_name],
            horizon=horizon,
        )
    solved = store[key]
    if solved["mu_ref"] is not baseline["mu_ref"][source_name]:
        raise RuntimeError("controlled source diverged between kernels")
    return solved


def _release_landings(cache: dict) -> None:
    """Drop dense landings once both focused directions are stored.

    The kernel stays. Support checks read its toggles. The direction cache
    holds the committor, which is the expensive object to recompute.
    """
    for pack in cache.values():
        if not isinstance(pack, dict):
            continue
        cached = pack.get("directions_cache") or {}
        if len(cached) >= 2 and pack.get("landing") is not None:
            pack["landing"] = None


def assess_pair_row(tp, pp, spec: dict, slots, cache: dict, alignment: dict) -> dict:
    """Controlled eventual committor of a two-rule set and of each member."""
    floor = require_effect_floor(spec)
    factors = alphabet_factors(spec["alphabet"])
    rho = PRIMARY_RHO
    horizon = int(spec.get("reconfiguration_horizon", RECONFIGURATION_HORIZON))
    if horizon != RECONFIGURATION_HORIZON:
        raise RuntimeError("refusing to run: the horizon is not the predeclared value 16")
    baseline = _baseline_pack(factors, rho, slots, cache)
    packs = {
        "0": baseline,
        "T": _constrained_pack((tp,), factors, rho, slots, cache),
        "P": _constrained_pack((pp,), factors, rho, slots, cache),
        "TP": _constrained_pack((tp, pp), factors, rho, slots, cache),
    }
    violations = _support_violations(packs["TP"]["kernel"], packs["T"]["kernel"])
    violations += _support_violations(packs["TP"]["kernel"], packs["P"]["kernel"])
    violations += _support_violations(packs["TP"]["kernel"], packs["0"]["kernel"])
    removed = _support_violations(packs["0"]["kernel"], packs["TP"]["kernel"])
    table = baseline["table"]
    directions = {}
    vectors = {}
    residuals = [baseline["residual"], packs["T"]["residual"], packs["P"]["residual"], packs["TP"]["residual"]]
    for key, source_name, target_name in _direction_names(table):
        solved = {}
        for label, pack in packs.items():
            solved[label] = _cached_direction(pack, baseline, source_name, target_name, horizon)
            residual = solved[label]["solver"]["residual"]
            residuals.append(0.0 if residual is None else float(residual))
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
        gap = None
        if None not in {delta_t, delta_p, delta_tp}:
            gap = super_singleton_gap(delta_tp, delta_t, delta_p)
        spread_t = solved["T"]["triad"].get("spread")
        spread_tp = solved["TP"]["triad"].get("spread")
        delta_s = None if spread_t is None or spread_tp is None else float(spread_tp - spread_t)
        stat_values = {label: solved[label]["q_stationary"] for label in packs}
        stat_i = None
        if None not in stat_values.values():
            stat_i = interaction_residual(stat_values["TP"], stat_values["T"], stat_values["P"], stat_values["0"])
        occupancy = None
        if solved["TP"]["q_stationary"] is not None and qtp is not None:
            occupancy = float(solved["TP"]["q_stationary"] - qtp)
        h16_tp = solved["TP"]["controlled_hit"].get("hit_before_return")
        h16_0 = solved["0"]["controlled_hit"].get("hit_before_return")
        h16_delta = None if h16_tp is None or h16_0 is None else float(h16_tp - h16_0)
        i_state = state_interaction(solved["TP"]["q"], solved["T"]["q"], solved["P"]["q"], solved["0"]["q"])
        i_summary = state_summary(i_state, baseline["mu_ref"][source_name], baseline["n_pairs"])
        defined = np.isfinite(i_state)
        states = [int(state) for state in np.flatnonzero(defined)]
        vectors[key] = {
            "states": states,
            "i_state": [float(i_state[state]) for state in states],
            "q_tp": [float(solved["TP"]["q"][state]) for state in states],
            "q_t": [float(solved["T"]["q"][state]) for state in states],
            "q_p": [float(solved["P"]["q"][state]) for state in states],
            "q_0": [float(solved["0"]["q"][state]) for state in states],
        }
        pos_state = i_summary.get("max_positive_state")
        neg_state = i_summary.get("max_negative_state")

        def _at(state):
            if state is None:
                return None
            return {
                "state": int(state),
                "triad": int(state) >> baseline["n_pairs"],
                "i_state": float(i_state[state]),
                "q_tp": float(solved["TP"]["q"][state]),
                "q_t": float(solved["T"]["q"][state]),
                "q_p": float(solved["P"]["q"][state]),
                "q_0": float(solved["0"]["q"][state]),
            }

        directions[key] = {
            "Q0": q0,
            "QT": qt,
            "QP": qp,
            "QTP": qtp,
            "delta_T": delta_t,
            "delta_P": delta_p,
            "delta_TP": delta_tp,
            "I_interaction": residual_i,
            "I_sign": sign_status(residual_i, floor),
            "G": gap,
            "G_sign": sign_status(gap, floor),
            "S_T": None if spread_t is None else float(spread_t),
            "S_TP": None if spread_tp is None else float(spread_tp),
            "delta_S": delta_s,
            "delta_S_sign": sign_status(delta_s, floor),
            "triad_min_configurations": solved["TP"]["triad"].get("min_configurations"),
            "triad_max_configurations": solved["TP"]["triad"].get("max_configurations"),
            "I_stationary": stat_i,
            "I_stationary_sign": sign_status(stat_i, floor),
            "occupancy_contribution": occupancy,
            "horizon16_controlled_hit": None if h16_tp is None else float(h16_tp),
            "horizon16_controlled_baseline": None if h16_0 is None else float(h16_0),
            "horizon16_controlled_delta": h16_delta,
            "solver_residual": max(float(solved[label]["solver"]["residual"] or 0.0) for label in packs),
            "state_interaction": i_summary,
            "max_positive_interaction_state": _at(pos_state),
            "max_negative_interaction_state": _at(neg_state),
        }
    expressions = [pp.expression(slots), tp.expression(slots)]
    return _num(
        {
            "pair_id": _pair_identifier(spec, expressions),
            "expressions": expressions,
            "alignment": alignment,
            "directions": directions,
            "support_violations": violations,
            "support_removed": removed,
            "max_residual": max(residuals) if residuals else None,
            "vectors": vectors,
        }
    )


def benchmark_pair_cost(spec: dict) -> dict:
    """Time one two-rule kernel with the block epoch solver. Float64, not exact."""
    catalogue = targeted_catalogue(spec)
    if not catalogue["representatives"]:
        return {
            "kernel_seconds": None,
            "committor_seconds": None,
            "seconds_per_kernel": None,
            "sample_pairs": 0,
            "sample_seconds": 0.0,
            "seconds_per_pair_sample": None,
            "sample_note": "catalogue is empty",
            "stationary_residual": None,
            "epoch_defect": None,
            "landing_megabytes": None,
            "catalogue": catalogue,
        }
    grammar = _grammar(tuple(spec["weights"]), spec["cells"][0].get("A_max", 4))
    slots = grammar.relation_slots
    canon = catalogue["representatives"][0]
    constraints = tuple(grammar.labelled[index] for index in canon)
    cache: dict = {}
    factors = alphabet_factors(spec["alphabet"])
    started = time.perf_counter()
    pack = _constrained_pack(constraints, factors, PRIMARY_RHO, slots, cache)
    elapsed = time.perf_counter() - started
    baseline = _baseline_pack(factors, PRIMARY_RHO, slots, cache)
    started_q = time.perf_counter()
    for source_name, target_name in (
        (baseline["table"].path_name, baseline["table"].matching_name),
        (baseline["table"].matching_name, baseline["table"].path_name),
    ):
        eventual_committor(
            pack["landing"],
            baseline["class_index"],
            baseline["positions"][source_name],
            baseline["positions"][target_name],
        )
    committor_seconds = time.perf_counter() - started_q
    sample = 8 if len(catalogue["representatives"]) >= 8 else len(catalogue["representatives"])
    sample_cache: dict = {}
    sample_started = time.perf_counter()
    for index, canon in enumerate(catalogue["representatives"][:sample]):
        members = sorted(
            (cross_order_class(grammar.labelled[item], 6), item) for item in canon
        )
        sample_pp = grammar.labelled[members[0][1]]
        sample_tp = grammar.labelled[members[1][1]]
        assess_pair_row(
            sample_tp,
            sample_pp,
            spec,
            grammar.slot_list(),
            sample_cache,
            catalogue["alignments"][index],
        )
        _evict_pack(sample_cache, (sample_tp, sample_pp), factors, PRIMARY_RHO)
        _release_landings(sample_cache)
    sample_seconds = time.perf_counter() - sample_started
    per_pair = None if sample == 0 else sample_seconds / sample
    return {
        "kernel_seconds": elapsed,
        "committor_seconds": committor_seconds,
        "seconds_per_kernel": elapsed + committor_seconds,
        "sample_pairs": sample,
        "sample_seconds": sample_seconds,
        "seconds_per_pair_sample": per_pair,
        "sample_note": "first sorted canonical pairs; early pairs build singleton committors and later pairs reuse them",
        "stationary_residual": pack["residual"],
        "epoch_defect": pack["defect"],
        "landing_megabytes": pack["landing"].nbytes / 1e6 if pack.get("landing") is not None else None,
        "catalogue": catalogue,
    }


def execute_4a_shard(task: dict) -> None:
    from rs_constraint_lab.census import _finish_receipt, _require_version, _walk
    from rs_constraint_lab.spec import effective_options

    _require_version(task)
    if task["spec"].get("analysis") != ANALYSIS_4A:
        raise RuntimeError("generation 4a shard received a different analysis")
    if int(task["n"]) != 4 or int(task["cardinality"]) != 1:
        raise RuntimeError("generation 4a recomputes N=4 cardinality-1 singletons only")
    spec = dict(task["spec"])
    require_effect_floor(spec)
    if list(spec.get("sensitivity_alphabets", [])) != ["W3", "W16"]:
        raise RuntimeError("generation 4a sensitivity alphabets are W3 and W16")
    if [str(item) for item in spec.get("rho3_sensitivity", [])] != ["1/2", "1", "2"]:
        raise RuntimeError("generation 4a rho3 probes are 1/2, 1, and 2")
    shard_dir = Path(task["shard_dir"])
    shard_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(
        shard_dir / "running.json",
        {"shard_id": task["shard_id"], "attempt": task["attempt"], "started_at": _now(), "pid": _pid()},
    )
    started = time.perf_counter()
    options = effective_options(spec)
    grammar = _grammar(spec.get("weights"), task["a_max"])
    slots = grammar.relation_slots
    slot_list = grammar.slot_list()
    cache: dict = {}
    rows = []

    def on_set(constraints) -> None:
        rows.append(assess_singleton_row(constraints[0], spec, slot_list, cache))

    counts = _walk(task, grammar, on_set)
    result = {"identity": task["identity"], "counts": counts, "sensitivity_rows": rows}
    _finish_receipt(task, shard_dir, result, started, counts)


def execute_5_shard(task: dict) -> None:
    from rs_constraint_lab.census import _finish_receipt, _require_version

    _require_version(task)
    spec = dict(task["spec"])
    if spec.get("analysis") != ANALYSIS_5:
        raise RuntimeError("generation 5 shard received a different analysis")
    require_effect_floor(spec)
    if int(spec.get("reconfiguration_horizon", RECONFIGURATION_HORIZON)) != RECONFIGURATION_HORIZON:
        raise RuntimeError("refusing to run: the horizon is not the predeclared value 16")
    spec["_spec_hash"] = task["identity"]["spec_hash"]
    catalogue = targeted_catalogue(spec)
    if catalogue["sha256"] != task["identity"].get("catalogue_sha256"):
        raise RuntimeError("targeted catalogue does not match the shard identity")
    if catalogue["coverage"]["canonical_weighted_pairs"] > TARGETED_POOL_CEILING:
        raise RuntimeError("targeted pool exceeds the predeclared ceiling")
    shard_dir = Path(task["shard_dir"])
    shard_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(
        shard_dir / "running.json",
        {"shard_id": task["shard_id"], "attempt": task["attempt"], "started_at": _now(), "pid": _pid()},
    )
    started = time.perf_counter()
    grammar = _grammar(tuple(spec["weights"]), task["a_max"])
    slots = grammar.slot_list()
    factors = alphabet_factors(spec["alphabet"])
    cache: dict = {}
    rows = []
    start = int(task["start"])
    end = int(task["end"])
    for offset, canon in enumerate(catalogue["representatives"][start:end]):
        index = start + offset
        members = sorted(
            ((cross_order_class(grammar.labelled[item], 6), item) for item in canon),
        )
        pp = grammar.labelled[members[0][1]]
        tp = grammar.labelled[members[1][1]]
        rows.append(assess_pair_row(tp, pp, spec, slots, cache, catalogue["alignments"][index]))
        _evict_pack(cache, (tp, pp), factors, PRIMARY_RHO)
        _release_landings(cache)
    counts = {"analysed": len(rows), "solver_failures": 0, "start": start, "end": end}
    result = {"identity": task["identity"], "counts": counts, "pair_rows": rows}
    _finish_receipt(task, shard_dir, result, started, counts)


def _now() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _pid() -> int:
    import os

    return os.getpid()


def _question_counts(rows: list[dict], floor: float) -> dict:
    """Predeclared Generation 5 questions. Classification uses ``floor`` as given."""
    directions = ("path_to_matching", "matching_to_path")
    out = {"effect_floor": floor, "systems": len(rows), "directions": {}}
    alignments = Counter(json.dumps(row["alignment"], sort_keys=True) for row in rows)
    out["relative_alignment_classes"] = len(alignments)
    out["support_violation_systems"] = sum(1 for row in rows if row.get("support_violations"))
    out["support_removed_systems"] = sum(1 for row in rows if row.get("support_removed"))
    out["support_removed_total"] = int(sum(row.get("support_removed") or 0 for row in rows))
    for name in directions:
        nonzero = positive = negative = 0
        g_positive = 0
        delta_s_positive = 0
        sign_reversals = 0
        both_small = 0
        stationary_only = 0
        best_pos = None
        best_neg = None
        best_g = None
        best_s = None
        additive = super_add = sub_add = cancel = dominated = 0
        for row in rows:
            direction = row["directions"][name]
            status = direction["I_sign"]
            if status == "positive":
                positive += 1
                nonzero += 1
            elif status == "negative":
                negative += 1
                nonzero += 1
            if direction["G_sign"] == "positive":
                g_positive += 1
            if direction["delta_S_sign"] == "positive":
                delta_s_positive += 1
            delta_t = direction["delta_T"]
            delta_p = direction["delta_P"]
            delta_tp = direction["delta_TP"]
            strongest = max(abs(delta_t or 0.0), abs(delta_p or 0.0))
            strongest_sign = 0
            if abs(delta_t or 0.0) >= abs(delta_p or 0.0) and abs(delta_t or 0.0) > floor:
                strongest_sign = 1 if delta_t > 0 else -1
            elif abs(delta_p or 0.0) > floor:
                strongest_sign = 1 if delta_p > 0 else -1
            pair_sign = 0 if abs(delta_tp or 0.0) <= floor else (1 if delta_tp > 0 else -1)
            if strongest_sign and pair_sign and strongest_sign != pair_sign:
                sign_reversals += 1
            if abs(delta_t or 0.0) <= floor and abs(delta_p or 0.0) <= floor and abs(delta_tp or 0.0) > floor:
                both_small += 1
            pair_abs = abs(delta_tp or 0.0)
            if pair_abs > floor and abs(delta_t or 0.0) < 0.1 * pair_abs and abs(delta_p or 0.0) < 0.1 * pair_abs:
                dominated += 1
            if direction["I_stationary_sign"] != "zero" and status == "zero":
                stationary_only += 1
            interaction = direction["I_interaction"]
            if status == "zero":
                additive += 1
            elif interaction is not None and delta_tp is not None and abs(delta_tp) <= floor and abs(interaction) > floor:
                cancel += 1
            elif status == "positive":
                super_add += 1
            elif status == "negative":
                sub_add += 1
            marker = (direction["I_interaction"], row["pair_id"], row["expressions"], row["alignment"])
            if direction["I_interaction"] is not None and (best_pos is None or direction["I_interaction"] > best_pos[0]):
                best_pos = marker
            if direction["I_interaction"] is not None and (best_neg is None or direction["I_interaction"] < best_neg[0]):
                best_neg = marker
            if direction["G"] is not None and (best_g is None or direction["G"] > best_g[0]):
                best_g = (direction["G"], row["pair_id"], row["expressions"], row["alignment"])
            if direction["delta_S"] is not None and (best_s is None or direction["delta_S"] > best_s[0]):
                best_s = (direction["delta_S"], row["pair_id"], row["expressions"], row["alignment"])
        out["directions"][name] = {
            "nonzero_interaction": nonzero,
            "positive_interaction": positive,
            "negative_interaction": negative,
            "zero_within_tolerance": len(rows) - nonzero,
            "G_positive": g_positive,
            "delta_S_positive": delta_s_positive,
            "sign_reversals_of_strongest_singleton": sign_reversals,
            "pair_moves_when_both_singletons_are_within_floor": both_small,
            "pair_effect_dominates_both_components_by_10x": dominated,
            "stationary_interaction_lost_under_control": stationary_only,
            "additive": additive,
            "positive_interaction_residual": super_add,
            "negative_interaction_residual": sub_add,
            "cancellation_with_small_pair_delta": cancel,
            "largest_positive_I": _extreme(best_pos),
            "largest_negative_I": _extreme(best_neg),
            "largest_positive_G": _extreme(best_g),
            "largest_positive_delta_S": _extreme(best_s),
        }
    return out


def _extreme(marker):
    if marker is None:
        return None
    value, pair_id, expressions, alignment = marker
    return {
        "value": value,
        "pair_id": pair_id,
        "expressions": expressions,
        "alignment": alignment,
    }


def summarise_4a(rows: list[dict], floor: float) -> dict:
    by_class = Counter(row["cross_order_class"] for row in rows)
    probes = ("primary", "rho1/2", "rho2", "W3", "W16")
    directions = ("path_to_matching", "matching_to_path")
    survival = {probe: {direction: {} for direction in directions} for probe in probes}
    for probe in probes:
        for direction in directions:
            for kind in ("T->P", "P->P", "P->T", "T->T"):
                selected = [row for row in rows if row["cross_order_class"] == kind]
                moved = 0
                triad = 0
                controlled_moved = 0
                for row in selected:
                    fields = row["probes"][probe][direction]
                    if fields["sign"] != "zero":
                        moved += 1
                    if fields["triad_changes_hit"]:
                        triad += 1
                    if fields["controlled_sign"] != "zero":
                        controlled_moved += 1
                survival[probe][direction][kind] = {
                    "rows": len(selected),
                    "stationary_passage_nonzero": moved,
                    "triad_changes_hit": triad,
                    "controlled_passage_nonzero": controlled_moved,
                }
    eventual = {direction: {} for direction in directions}
    for direction in directions:
        for kind in ("T->P", "P->P", "P->T", "T->T"):
            selected = [row for row in rows if row["cross_order_class"] == kind]
            altered = 0
            triad = 0
            occupancy = []
            controlled_abs = []
            stationary_abs = []
            for row in selected:
                event = row["probes"]["primary"][direction]["eventual"]
                if event["sign_controlled"] != "zero":
                    altered += 1
                if event["triad_changes"]:
                    triad += 1
                if event["occupancy_contribution"] is not None:
                    occupancy.append(abs(event["occupancy_contribution"]))
                if event["delta_controlled"] is not None:
                    controlled_abs.append(abs(event["delta_controlled"]))
                if event["delta_stationary"] is not None:
                    stationary_abs.append(abs(event["delta_stationary"]))
            eventual[direction][kind] = {
                "rows": len(selected),
                "controlled_eventual_nonzero": altered,
                "triad_changes_eventual": triad,
                "max_abs_controlled_delta": max(controlled_abs) if controlled_abs else None,
                "max_abs_stationary_delta": max(stationary_abs) if stationary_abs else None,
                "max_abs_occupancy_contribution": max(occupancy) if occupancy else None,
                "median_abs_occupancy_contribution": _median(occupancy),
            }
    ranking = {}
    for direction in directions:
        ranking[direction] = {
            "P->P_max_abs_controlled": eventual[direction]["P->P"]["max_abs_controlled_delta"],
            "T->P_max_abs_controlled": eventual[direction]["T->P"]["max_abs_controlled_delta"],
            "P->P_max_abs_stationary_eventual": eventual[direction]["P->P"]["max_abs_stationary_delta"],
            "T->P_max_abs_stationary_eventual": eventual[direction]["T->P"]["max_abs_stationary_delta"],
        }
    return {
        "rows": len(rows),
        "by_class": dict(by_class),
        "effect_floor": floor,
        "horizon": RECONFIGURATION_HORIZON,
        "primary_quantity_for_sensitivity": "STATIONARY_SOURCE_PASSAGE",
        "sensitivity": survival,
        "eventual_primary": eventual,
        "ranking": ranking,
        "max_stationary_residual": max((row["max_stationary_residual"] or 0.0) for row in rows) if rows else None,
    }


def _median(values: list[float]) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return float(ordered[mid])
    return float(0.5 * (ordered[mid - 1] + ordered[mid]))


def _write_csv(path: Path, header: list[str], rows: list[list]) -> None:
    import csv

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def _4a_csv(path: Path, rows: list[dict]) -> None:
    header = ["expression", "class", "weight", "k"]
    probes = ("primary", "rho1/2", "rho2", "W3", "W16")
    directions = ("path_to_matching", "matching_to_path")
    for probe in probes:
        for direction in directions:
            for name in ("hit", "baseline", "delta", "spread", "unresolved", "sign", "controlled_delta", "triad"):
                header.append(f"{probe}.{direction}.{name}")
    for direction in directions:
        for name in (
            "q_controlled",
            "delta_controlled",
            "delta_stationary",
            "occupancy",
            "triad_spread",
            "sign",
        ):
            header.append(f"eventual.{direction}.{name}")
    body = []
    for row in rows:
        line = [row["expression"], row["cross_order_class"], row["weight"], row["k"]]
        for probe in probes:
            for direction in directions:
                fields = row["probes"][probe][direction]
                line.extend(
                    [
                        fields["hit_before_return"],
                        fields["baseline_hit_before_return"],
                        fields["delta_hit_before_return"],
                        fields["triad_hit_spread"],
                        fields["unresolved_within_horizon"],
                        fields["sign"],
                        fields["controlled_delta_hit_before_return"],
                        fields["triad_changes_hit"],
                    ]
                )
        for direction in directions:
            event = row["probes"]["primary"][direction]["eventual"]
            line.extend(
                [
                    event["q_controlled"],
                    event["delta_controlled"],
                    event["delta_stationary"],
                    event["occupancy_contribution"],
                    event["triad_spread"],
                    event["sign_controlled"],
                ]
            )
        body.append(line)
    _write_csv(path, header, body)


def _5_csv(path: Path, rows: list[dict]) -> None:
    header = [
        "pair_id",
        "pp",
        "tp",
        "tp_orbit",
        "pp_orbit",
        "action_edge_relation",
        "tp_condition_vs_action",
        "pp_vertices_vs_tp_triad",
        "support_violations",
        "support_removed",
    ]
    for direction in ("path_to_matching", "matching_to_path"):
        for name in (
            "Q0",
            "QT",
            "QP",
            "QTP",
            "delta_T",
            "delta_P",
            "delta_TP",
            "I_interaction",
            "I_sign",
            "G",
            "delta_S",
            "I_stationary",
            "occupancy_contribution",
            "horizon16_controlled_delta",
        ):
            header.append(f"{direction}.{name}")
    body = []
    for row in rows:
        alignment = row["alignment"]
        line = [
            row["pair_id"],
            row["expressions"][0],
            row["expressions"][1],
            alignment["tp_orbit"],
            alignment["pp_orbit"],
            alignment["action_edge_relation"],
            alignment["tp_condition_vs_action"],
            alignment["pp_vertices_vs_tp_triad"],
            row["support_violations"],
            row["support_removed"],
        ]
        for direction in ("path_to_matching", "matching_to_path"):
            fields = row["directions"][direction]
            for name in (
                "Q0",
                "QT",
                "QP",
                "QTP",
                "delta_T",
                "delta_P",
                "delta_TP",
                "I_interaction",
                "I_sign",
                "G",
                "delta_S",
                "I_stationary",
                "occupancy_contribution",
                "horizon16_controlled_delta",
            ):
                line.append(fields[name])
        body.append(line)
    _write_csv(path, header, body)


def validate_selected_extrema(spec: dict, rows: list[dict], questions: dict) -> dict:
    """Recompute the predeclared extrema. Does not change their ranking."""
    grammar = _grammar(tuple(spec["weights"]), spec["cells"][0].get("A_max", 4))
    slots = grammar.slot_list()
    index = {constraint.expression(slots): constraint for constraint in grammar.labelled}
    quantity_field = {
        "largest_positive_I": "I_interaction",
        "largest_negative_I": "I_interaction",
        "largest_positive_G": "G",
        "largest_positive_delta_S": "delta_S",
    }
    selected = []
    seen = set()
    for direction, payload in questions["directions"].items():
        for quantity in quantity_field:
            extreme = payload[quantity]
            if extreme is None:
                continue
            key = (extreme["pair_id"], direction, quantity)
            if key in seen:
                continue
            seen.add(key)
            selected.append((direction, quantity, extreme))
    systems = []
    known = set()
    checks: dict[str, list] = {}
    for direction, quantity, extreme in selected:
        checks.setdefault(extreme["pair_id"], []).append((direction, quantity, extreme["value"]))
        if extreme["pair_id"] in known:
            continue
        known.add(extreme["pair_id"])
        systems.append(extreme)
    results = []
    cache: dict = {}
    factors = alphabet_factors(spec["alphabet"])
    floor = require_effect_floor(spec)
    any_changed = False
    for extreme in systems:
        pp = index[extreme["expressions"][0]]
        tp = index[extreme["expressions"][1]]
        direct = assess_pair_row(tp, pp, spec, slots, cache, extreme["alignment"])
        iterative_gap = _iterative_gap(tp, pp, factors, slots, cache)
        relabel_gap = _relabel_gap(tp, pp, spec, grammar, slots, direct)
        rho = {}
        for label, value in (("1/2", Fraction(1, 2)), ("2", Fraction(2))):
            rho[label] = _rho_variant(tp, pp, spec, slots, value)
        alphabets = {}
        if tp.weight != "prohibit" or pp.weight != "prohibit":
            for name in ("W3", "W16"):
                alphabets[name] = _alphabet_variant(tp, pp, spec, slots, name)
        gaps = []
        changed = False
        for direction, quantity, stored in checks[extreme["pair_id"]]:
            recomputed = direct["directions"][direction][quantity_field[quantity]]
            gap = None if recomputed is None or stored is None else abs(float(recomputed) - float(stored))
            if gap is not None and gap > floor:
                changed = True
            gaps.append(
                {
                    "direction": direction,
                    "quantity": quantity,
                    "discovery_value": stored,
                    "recomputed_value": recomputed,
                    "abs_gap": gap,
                }
            )
        any_changed = any_changed or changed
        results.append(
            {
                "pair_id": extreme["pair_id"],
                "expressions": extreme["expressions"],
                "alignment": extreme["alignment"],
                "direct": {key: value for key, value in direct.items() if key != "vectors"},
                "iterative_max_abs_gap": iterative_gap,
                "relabel_max_abs_gap": relabel_gap,
                "rho": rho,
                "alphabets": alphabets,
                "discovery_recompute_gaps": gaps,
                "ranking_changed": changed,
            }
        )
    return {
        "ranking_policy": "discovery order is retained; a recompute gap above the effect floor is recorded and does not reorder the census",
        "ranking_changed": any_changed,
        "systems": results,
        "selected_quantities": [
            {"direction": direction, "quantity": quantity, "pair_id": extreme["pair_id"], "value": extreme["value"]}
            for direction, quantity, extreme in selected
        ],
    }


def _iterative_gap(tp, pp, factors, slots, cache: dict) -> float:
    from rs_constraint_lab.census import build_slotted

    baseline = _baseline_pack(factors, PRIMARY_RHO, slots, cache)
    pack = _constrained_pack((tp, pp), factors, PRIMARY_RHO, slots, cache)
    gap = 0.0
    for source_name, target_name in (
        (PATH_CLASS, MATCHING_CLASS),
        (MATCHING_CLASS, PATH_CLASS),
    ):
        direct = eventual_committor(
            pack["landing"],
            baseline["class_index"],
            baseline["positions"][source_name],
            baseline["positions"][target_name],
            record_condition=True,
        )
        iterative = eventual_committor(
            pack["landing"],
            baseline["class_index"],
            baseline["positions"][source_name],
            baseline["positions"][target_name],
            method="iterative",
            iterative_tolerance=1e-12,
            iterative_limit=20000,
        )
        both = np.isfinite(direct["q"]) & np.isfinite(iterative["q"])
        if np.any(both):
            gap = max(gap, float(np.max(np.abs(direct["q"][both] - iterative["q"][both]))))
    return gap


def _relabel_gap(tp, pp, spec, grammar, slots, direct: dict) -> float:
    """Kernel check on three images. The full orbit is checked by canonical id."""
    from rs_constraint_lab.constraints import relabel_constraint
    from rs_constraint_lab.grammar import canonical_id_tuple
    from rs_constraint_lab.state import slot_permutation_maps

    labelled_index = {constraint.key(): index for index, constraint in enumerate(grammar.labelled)}
    origin = tuple(sorted(labelled_index[constraint.key()] for constraint in (tp, pp)))
    canonical = canonical_id_tuple(origin, grammar.image)
    maps = slot_permutation_maps(4, tuple(slots))
    for slot_map in maps:
        image_ids = tuple(
            sorted(labelled_index[relabel_constraint(constraint, slot_map).key()] for constraint in (tp, pp))
        )
        if canonical_id_tuple(image_ids, grammar.image) != canonical:
            raise RuntimeError("relabelled pair left its canonical orbit")
    gap = 0.0
    cache: dict = {}
    for slot_map in (maps[1], maps[len(maps) // 2], maps[-1]):
        image_tp = relabel_constraint(tp, slot_map)
        image_pp = relabel_constraint(pp, slot_map)
        recomputed = assess_pair_row(image_tp, image_pp, spec, slots, cache, direct["alignment"])
        for name in ("path_to_matching", "matching_to_path"):
            left = direct["directions"][name]["I_interaction"]
            right = recomputed["directions"][name]["I_interaction"]
            if left is not None and right is not None:
                gap = max(gap, abs(float(left) - float(right)))
    return gap


def _rho_variant(tp, pp, spec, slots, rho: Fraction) -> dict:
    variant = dict(spec)
    cache: dict = {}
    factors = alphabet_factors(spec["alphabet"])
    baseline = _baseline_pack(factors, rho, slots, cache)
    packs = {
        "0": baseline,
        "T": _constrained_pack((tp,), factors, rho, slots, cache),
        "P": _constrained_pack((pp,), factors, rho, slots, cache),
        "TP": _constrained_pack((tp, pp), factors, rho, slots, cache),
    }
    out = {}
    for source_name, target_name, key in (
        (PATH_CLASS, MATCHING_CLASS, "path_to_matching"),
        (MATCHING_CLASS, PATH_CLASS, "matching_to_path"),
    ):
        solved = {
            label: prepare_direction(
                pack["kernel"],
                pack["pi"],
                pack["landing"],
                baseline["class_index"],
                baseline["n_pairs"],
                baseline["positions"][source_name],
                baseline["positions"][target_name],
                baseline["mu_ref"][source_name],
            )
            for label, pack in packs.items()
        }
        q0 = solved["0"]["q_controlled"]
        qt = solved["T"]["q_controlled"]
        qp = solved["P"]["q_controlled"]
        qtp = solved["TP"]["q_controlled"]
        out[key] = _num(
            {
                "I_interaction": None if None in {q0, qt, qp, qtp} else interaction_residual(qtp, qt, qp, q0),
                "delta_TP": None if qtp is None or q0 is None else float(qtp - q0),
                "delta_S": _spread_delta(solved["T"], solved["TP"]),
                "S_TP": solved["TP"]["triad"].get("spread"),
            }
        )
    return out


def _alphabet_variant(tp, pp, spec, slots, alphabet: str) -> dict:
    """Strong-favour scales with the alphabet. Prohibit stays zero."""
    renamed = dict(spec)
    renamed["alphabet"] = alphabet
    return _rho_variant(tp, pp, renamed, slots, PRIMARY_RHO)


def _spread_delta(left: dict, right: dict):
    a = left["triad"].get("spread")
    b = right["triad"].get("spread")
    if a is None or b is None:
        return None
    return float(b - a)


def build_targeted_plan(spec: dict, items: int, header: dict) -> dict:
    """Plan the targeted census. The catalogue count is fixed before any shard runs."""
    from rs_constraint_lab.execution import PLAN_SCHEMA, _hypergraph_accounting, _shard_id, _shard_identity
    from rs_constraint_lab.version import DEFAULT_WORKERS, PROFILE_NOTE

    floor = require_effect_floor(spec)
    if [int(cell["N"]) for cell in spec["cells"]] != [4]:
        raise ValueError("targeted pairs require N=4")
    if any(int(card) != 2 for cell in spec["cells"] for card in cell["cardinalities"]):
        raise ValueError("targeted pairs are cardinality 2")
    timed = benchmark_pair_cost(spec)
    catalogue = timed["catalogue"]
    coverage = catalogue["coverage"]
    count = coverage["canonical_weighted_pairs"]
    if count > TARGETED_POOL_CEILING:
        raise RuntimeError(
            "targeted canonical pool is "
            f"{count}, above the ceiling {TARGETED_POOL_CEILING}. "
            "No sample was drawn. Record the count and choose a symmetry-respecting subdesign before running."
        )
    cell = spec["cells"][0]
    grammar = _grammar(tuple(spec["weights"]), cell.get("A_max", 4))
    per_kernel = float(timed["seconds_per_kernel"] or 0.0)
    per_pair = timed.get("seconds_per_pair_sample") or per_kernel
    # ids are not ordered by class. Unique members are the singleton packs a
    # process-wide cache would build. Pair landings are evicted after each row,
    # so this kernel count is an upper bound on work, not on retained memory.
    unique_members = len({index for canon in catalogue["representatives"] for index in canon})
    estimated_kernels = unique_members + count
    # The pair sample includes cold singleton solves. Scaling it by the pair
    # count is an upper bound once singleton committors are reused.
    estimated_seconds = count * float(per_pair)
    shard_count = 0 if count == 0 else (count + items - 1) // items
    disk = count * 20000
    shards = []
    start = 0
    while start < count:
        end = min(start + items, count)
        identity = _shard_identity(spec, header, 0, cell, 2, start, end)
        identity["catalogue_sha256"] = catalogue["sha256"]
        identity["analysis_version"] = spec.get("analysis_version", ANALYSIS_VERSION)
        identity["effect_floor"] = floor
        shards.append(
            {
                "shard_id": _shard_id(identity),
                "ordinal": len(shards),
                "cell_index": 0,
                "n": 4,
                "k_max": int(cell["K_max"]),
                "a_max": cell.get("A_max"),
                "cardinality": 2,
                "start": start,
                "end": end,
                "identity": identity,
            }
        )
        start = end
    header = dict(header)
    header["catalogue_sha256"] = catalogue["sha256"]
    header["analysis_version"] = spec.get("analysis_version", ANALYSIS_VERSION)
    return {
        "schema": PLAN_SCHEMA,
        "header": header,
        "spec": spec,
        "estimates": {
            "cells": [
                {
                    "N": 4,
                    "K_max": int(cell["K_max"]),
                    "A_max": cell.get("A_max"),
                    "labelled_states": 1024,
                    "canonical_states": None,
                    "grammar": grammar.stats,
                    "edge_accounting": _hypergraph_accounting(grammar),
                    "cardinalities": {
                        "2": {
                            "labelled_combinations": coverage["weighted_labelled_pairs"],
                            "labelled_simple": coverage["weighted_labelled_pairs"] - coverage["invalid_pairs"],
                            "labelled_stacked": coverage["invalid_pairs"],
                            "canonical_simple_exact": count,
                            "shards": shard_count,
                            "disk_upper_bound_bytes": disk,
                        }
                    },
                    "targeted_coverage": coverage,
                }
            ],
            "shard_count": len(shards),
            "disk_upper_bound_bytes": disk,
            "shard_items": items,
            "profile_note": PROFILE_NOTE,
            "workers_default": DEFAULT_WORKERS,
            "benchmark": {
                "kernel_seconds": timed["kernel_seconds"],
                "committor_seconds": timed["committor_seconds"],
                "seconds_per_kernel": per_kernel,
                "sample_pairs": timed["sample_pairs"],
                "sample_seconds": timed["sample_seconds"],
                "seconds_per_pair_sample": per_pair,
                "sample_note": timed["sample_note"],
                "estimated_kernels_with_singleton_cache": estimated_kernels,
                "estimated_serial_seconds": estimated_seconds,
                "estimated_seconds_at_default_workers": estimated_seconds / DEFAULT_WORKERS,
                "landing_megabytes": timed["landing_megabytes"],
                "pair_landings_retained": "evicted after each row",
                "solver_memory_megabytes_per_worker": timed["landing_megabytes"] * min(items, count) + 5.0,
                "stationary_residual_sample": timed["stationary_residual"],
                "epoch_defect_sample": timed["epoch_defect"],
            },
            "effect_floor": floor,
        },
        "shards": shards,
    }


def merge_v05(out_dir: Path, plan: dict, publish: Path | None = None) -> dict:
    from rs_constraint_lab.execution import _fingerprint, _reconcile
    from rs_constraint_lab.generation import _git_commit, _publish
    from rs_constraint_lab.version import EXECUTION_PRINCIPLE, MAX_ATTEMPTS, PROFILE_NOTE

    out_dir = Path(out_dir)
    progress = _reconcile(out_dir, plan)
    spec = plan["spec"]
    analysis = spec.get("analysis")
    floor = require_effect_floor(spec)
    rows: list[dict] = []
    work = 0.0
    analysed = 0
    for shard in plan["shards"]:
        state = progress["shards"][shard["shard_id"]]
        if state["status"] != "completed":
            continue
        result = read_json(out_dir / "shards" / shard["shard_id"] / "result.json")
        incoming = result.get("sensitivity_rows") or result.get("pair_rows") or []
        for row in incoming:
            row.pop("vectors", None)
            rows.append(row)
        analysed += int(result["counts"].get("analysed", 0))
        receipt = read_json(out_dir / "shards" / shard["shard_id"] / "receipt.json")
        work += float(receipt.get("elapsed_seconds") or 0.0)
    cell = spec["cells"][0]
    n = int(cell["N"])
    k_max = int(cell["K_max"])
    v05_summary = None
    if progress["status"] == "COMPLETE" and analysis == ANALYSIS_4A:
        expected = plan["estimates"]["cells"][0]["cardinalities"]["1"]["canonical_simple_exact"]
        if analysed != expected:
            raise RuntimeError(f"generation 4a analysed {analysed}, planned {expected}")
        v05_summary = summarise_4a(rows, floor)
        _4a_csv(out_dir / f"singles-n{n}-k{k_max}.csv", rows)
    if progress["status"] == "COMPLETE" and analysis == ANALYSIS_5:
        expected = plan["estimates"]["cells"][0]["cardinalities"]["2"]["canonical_simple_exact"]
        if analysed != expected:
            raise RuntimeError(f"generation 5 analysed {analysed}, planned {expected}")
        questions = _question_counts(rows, floor)
        questions["max_observed_residual"] = max((row["max_residual"] or 0.0) for row in rows) if rows else None
        questions["effect_floor_reason"] = spec.get("effect_floor_reason")
        validation = validate_selected_extrema(spec, rows, questions)
        v05_summary = {
            "coverage": plan["estimates"]["cells"][0]["targeted_coverage"],
            "questions": questions,
            "validation": validation,
            "benchmark": plan["estimates"].get("benchmark"),
        }
        _5_csv(out_dir / f"singles-n{n}-k{k_max}.csv", rows)
    hashes = {
        "family_index_sha256": "",
        "singles_sha256": sha256_file(out_dir / f"singles-n{n}-k{k_max}.csv") if (out_dir / f"singles-n{n}-k{k_max}.csv").exists() else "",
        "kernel_index_sha256": "",
        "kernel_index_count": 0,
        "qualitative_index_sha256": "",
        "observable_index_sha256": "",
    }
    estimate = plan["estimates"]["cells"][0]
    cardinalities = {}
    for cardinality, info in estimate["cardinalities"].items():
        cardinalities[cardinality] = {
            "labelled_combinations": info.get("labelled_combinations"),
            "labelled_simple": info.get("labelled_simple"),
            "labelled_stacked": info.get("labelled_stacked"),
            "canonical": analysed,
            "analysed": analysed,
        }
    cell_summary = {
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
            "analysis": analysis,
        },
        "runtime_seconds": work,
        "accounting": {"edge": estimate["edge_accounting"], "grammar": estimate["grammar"]},
        "canonical_states": estimate.get("canonical_states"),
        "relation_slots": estimate["edge_accounting"]["relation_slots"],
        "labelled_states": estimate["labelled_states"],
        "cardinalities": cardinalities,
        "families": 0,
        "family_histogram": {},
        "structural_families": 0,
        "screened_families": 0,
        "baseline_equivalent_families": 0,
        "cancellations": {},
        "extremes": {},
        **hashes,
        "v05_census": v05_summary,
    }
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
        "analysis": analysis,
        "analysis_version": spec.get("analysis_version", ANALYSIS_VERSION),
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
        "cells": [cell_summary],
        "unsearched_declared": list(spec.get("unsearched", [])),
        "territory": None,
        "effect_floor": floor,
        "effect_floor_reason": spec.get("effect_floor_reason"),
        "v05": v05_summary,
    }
    atomic_write_json(out_dir / "summary.json", json_ready(summary))
    if publish is not None and summary["status"] == "COMPLETE":
        _publish(summary, spec, Path(publish), out_dir)
    return summary
