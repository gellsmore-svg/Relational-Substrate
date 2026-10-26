"""Memory-clock reanalysis and the N=4 singleton census.

Generation 3 artifacts are not rewritten. This module reads the same grammar
and writes a separate experiment. N=4 uses float64 stationary distributions
and says so. Exact structural facts stay exact.
"""

from __future__ import annotations

import csv
import hashlib
import os
import sys
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np

from rs_constraint_lab.combinadic import next_combination, unrank_combination
from rs_constraint_lab.constraints import Choreography, cross_order_class, set_cross_order_class, structurally_simple
from rs_constraint_lab.durable import atomic_write_json, atomic_write_text, json_ready, read_json, sha256_file
from rs_constraint_lab.dynamics import RelabelTables, canonical_tokens, family_ids
from rs_constraint_lab.exact import long_run
from rs_constraint_lab.grammar import (
    build_grammar,
    count_canonical_simple_sets,
    is_canonical_ids,
    labelled_simple_count,
)
from rs_constraint_lab.kernel import Kernel, build_kernel
from rs_constraint_lab.memory_clocks import (
    epoch_kernel_float,
    epoch_predictive_information,
    epoch_predictive_information_float,
    float_stationary,
    full_event_clock_memory_tv,
    full_event_cmi_triad_to_pair,
    full_event_pair_memory_tv,
    layout,
    memory_status_float,
    observation_memory_tv,
    pair_event_epoch_memory_tv,
    pair_event_epoch_memory_tv_float,
    pair_jump_dependence,
    pair_jump_dependence_float,
    triad_rate_depends_on_pairs,
    triad_weight_depends_on_pairs,
)
from rs_constraint_lab.reconfiguration import (
    RECONFIGURATION_HORIZON,
    RECONFIGURATION_MEASURE,
    class_flux,
    compare_reconfiguration,
    focused_transition,
)
from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.version import hypergraph_version_for_n
from rs_constraint_lab.weights import alphabet_factors

ANALYSIS_CLOCKS = "memory-clock-reanalysis"
ANALYSIS_N4 = "n4-singleton"
N4_INDEX_NAME = "generation-001b-structurally-normalised-kernel-ids-n4-k2.txt"
# Generation 3 measured these. A mismatch means the clock definition drifted.
GEN3_ANALYSED = 7385
GEN3_FULL_EVENT_POSITIVE = 5250
GEN3_CLASS_COUNTS = {"P->P": 1890, "P->T": 380, "T->P": 380, "T->T": 35, "mixed": 4700}
GEN3_REDUCIBILITY = {
    "FULLY_REDUCIBLE": 2295,
    "PAIRWISE_PROJECTION_REDUCIBLE": 2150,
    "IRREDUCIBLE_DYNAMIC_COUPLING": 2940,
    "OUTSIDE_SEARCHED_PAIRWISE_GRAMMAR": 0,
    "UNRESOLVED": 0,
}


def _now() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _fraction_text(value: Fraction | None) -> str | None:
    if value is None:
        return None
    return f"{value.numerator}/{value.denominator}"


def slotted_baselines(slots, rho: Fraction) -> tuple[Fraction, ...]:
    return tuple(Fraction(rho) if len(slot) == 3 else Fraction(1) for slot in slots)


def build_slotted(n: int, constraints, factors, slots, rho: Fraction) -> Kernel:
    return build_kernel(
        n,
        Choreography(0, 0, tuple(constraints)),
        factors,
        relation_slots=slots,
        baseline_weights=slotted_baselines(slots, rho),
    )


def _status_exact(value: Fraction | None) -> str:
    if value is None:
        return "undefined"
    if value > 0:
        return "positive"
    return "zero"


def _axis_e_from_ids(known: set[str] | None, slice_ids: list[str | None]) -> str:
    """Membership of non-halt conditional pair kernels in a searched index.

    ``None`` in ``slice_ids`` is a halt slice and is skipped. Differing jump
    kernels can both sit inside the searched grammar.
    """
    if known is None:
        return "unresolved"
    comparable = [item for item in slice_ids if item is not None]
    if not comparable:
        return "unresolved"
    if any(item not in known for item in comparable):
        return "outside"
    return "inside"


def _slice_halt(kernel: Kernel, triad: int, n_pairs: int) -> bool:
    span = 1 << n_pairs
    shift = triad << n_pairs
    for state in range(shift, shift + span):
        if kernel.deadlock[state]:
            continue
        if sum(kernel.weights[state][:n_pairs], Fraction(0)) > 0:
            return False
    return True


def pair_slice_kernel(kernel: Kernel, triad: int) -> Kernel:
    """Graph kernel of the next pair toggle at one fixed triadic configuration."""
    n_pairs, _n_triads = layout(kernel)
    span = 1 << n_pairs
    successors = []
    weights_out = []
    deadlock = []
    for pair_state in range(span):
        full = pair_state | (triad << n_pairs)
        pair_weights = tuple(kernel.weights[full][:n_pairs])
        total = sum(pair_weights, Fraction(0))
        weights_out.append(pair_weights)
        if kernel.deadlock[full] or total == 0:
            deadlock.append(True)
            successors.append(((pair_state, Fraction(1)),))
            continue
        outgoing = []
        for bit, weight in enumerate(pair_weights):
            if weight:
                outgoing.append((pair_state ^ (1 << bit), weight / total))
        deadlock.append(False)
        successors.append(tuple(outgoing))
    return Kernel(kernel.n, span, n_pairs, tuple(successors), tuple(weights_out), tuple(deadlock))


def _weight_patterns(kernel: Kernel) -> tuple[tuple[tuple[bool, ...], ...], tuple[tuple[bool, ...], ...]]:
    support = []
    modal = []
    for row in kernel.weights:
        support.append(tuple(weight > 0 for weight in row))
        best = max(row) if row else Fraction(0)
        modal.append(tuple(weight == best for weight in row))
    return tuple(support), tuple(modal)


def assess_n3_clocks(kernel: Kernel, indexes: dict, tables: RelabelTables) -> dict:
    """Orthogonal axes for one N=3 independent-hypergraph kernel.

    The historical reducibility label is retained and is not the taxonomy.
    """
    from rs_constraint_lab.higher_order import classify_reducibility

    pi_run = long_run(kernel, 0)
    pi = [pi_run["distribution_exact"].get(state, Fraction(0)) for state in range(kernel.n_states)]
    full = full_event_clock_memory_tv(kernel, pi)
    epoch, defect = pair_event_epoch_memory_tv(kernel, pi)
    jump, jump_tv = pair_jump_dependence(kernel)
    rate = triad_rate_depends_on_pairs(kernel)
    weight = triad_weight_depends_on_pairs(kernel)
    info = epoch_predictive_information(kernel, pi)
    reducibility = classify_reducibility(kernel, indexes, tables)
    n_pairs, n_triads = layout(kernel)
    slice_ids: list[str | None] = []
    for triad in range(1 << n_triads):
        if _slice_halt(kernel, triad, n_pairs):
            slice_ids.append(None)
            continue
        if triad == 0:
            slice_ids.append(reducibility["jump_id_triad_absent"])
        elif triad == 1:
            slice_ids.append(reducibility["jump_id_triad_present"])
        else:
            slice_ids.append(None)
    return {
        "arithmetic": "rational",
        "residual": 0.0,
        "periods": list(pi_run["periods"]),
        "pair_jump": bool(jump),
        "pair_jump_tv": _fraction_text(jump_tv),
        "triad_rate": bool(rate),
        "triad_weight": bool(weight),
        "full_tv": _fraction_text(full),
        "full_status": _status_exact(full),
        "epoch_tv": _fraction_text(epoch),
        "epoch_status": _status_exact(epoch),
        "epoch_defect": _fraction_text(defect),
        "axis_e": _axis_e_from_ids(indexes.get("kernels"), slice_ids),
        "historical_reducibility": reducibility["class"],
        "cmi_epoch_triad_to_pair": info["cmi_triad_to_next_pair_bits"],
        "cmi_epoch_pair_to_triad": info["cmi_pair_to_next_triad_bits"],
        "epoch_defined": bool(info["defined"]),
    }


def _clock_only_n3(kernel: Kernel) -> dict:
    pi_run = long_run(kernel, 0)
    pi = [pi_run["distribution_exact"].get(state, Fraction(0)) for state in range(kernel.n_states)]
    full = full_event_clock_memory_tv(kernel, pi)
    epoch, _defect = pair_event_epoch_memory_tv(kernel, pi)
    jump, _jump_tv = pair_jump_dependence(kernel)
    return {
        "pair_jump": bool(jump),
        "triad_rate": bool(triad_rate_depends_on_pairs(kernel)),
        "full_status": _status_exact(full),
        "epoch_status": _status_exact(epoch),
        "axis_e_relevant": False,
    }


def load_n4_pairwise_index() -> dict:
    """Generation 1b N=4 K<=2 pairwise kernel ids from the committed catalogue.

    The comparison is not against the N=3 index and not against a 1,024-state
    hypergraph id. A halt slice is omitted by the caller.
    """
    path = Path(__file__).resolve().parents[2] / "catalogue" / N4_INDEX_NAME
    if not path.is_file():
        return {"present": False, "kernels": None, "sha256": "missing", "baseline_id": None, "baseline_was_added": False}
    found = {line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    tables = RelabelTables(4)
    baseline = build_kernel(4, Choreography(0, 0, ()), {})
    baseline_id = family_ids(4, canonical_tokens(baseline, tables))["exact_kernel_family"]
    added = baseline_id not in found
    found.add(baseline_id)
    return {
        "present": True,
        "kernels": found,
        "sha256": digest,
        "baseline_id": baseline_id,
        "baseline_was_added": added,
        "path": str(path),
        "domain": (
            "Generation 1b N=4 K<=2 cardinalities {1,2} structural-simple "
            "pairwise-edge exact kernel ids, plus the unconstrained O=2 baseline"
        ),
    }


def _axis_e_n4(kernel: Kernel, known: set[str] | None, tables: RelabelTables, cache: dict) -> str:
    if known is None:
        return "unresolved"
    n_pairs, n_triads = layout(kernel)
    slice_ids: list[str | None] = []
    for triad in range(1 << n_triads):
        if _slice_halt(kernel, triad, n_pairs):
            slice_ids.append(None)
            continue
        sliced = pair_slice_kernel(kernel, triad)
        key = sliced.weights
        cached = cache.get(key)
        if cached is None:
            cached = family_ids(kernel.n, canonical_tokens(sliced, tables))["exact_kernel_family"]
            cache[key] = cached
        slice_ids.append(cached)
    return _axis_e_from_ids(known, slice_ids)


def _pair_observation(n_states: int, n_pairs: int) -> np.ndarray:
    mask = (1 << n_pairs) - 1
    return np.array([state & mask for state in range(n_states)], dtype=np.int32)


def _count_observation(n_states: int, n_pairs: int) -> np.ndarray:
    mask = (1 << n_pairs) - 1
    span = 1 << n_pairs
    return np.array(
        [(state & mask) + span * ((state >> n_pairs).bit_count()) for state in range(n_states)],
        dtype=np.int32,
    )


def _sign(value: float | None) -> int | None:
    if value is None:
        return None
    if abs(value) <= 1e-8:
        return 0
    return 1 if value > 0 else -1


def assess_n4(
    kernel: Kernel,
    baseline_pack: dict,
    index_kernels: set[str] | None,
    tables: RelabelTables,
    cache: dict,
    *,
    probe: bool = False,
) -> dict:
    """One N=4 singleton. Numerical stationary fields are not called exact.

    A probe omits projection B, epoch information, axis E, and the
    horizon-16 passage. It keeps the predeclared flux comparison, both
    memory clocks, and the pair-jump law. Sensitivity passes use probes.
    """
    pi, residual, arithmetic, periods = float_stationary(kernel)
    landing, defect = epoch_kernel_float(kernel)
    n_pairs, _n_triads = layout(kernel)
    full_tv = float(full_event_pair_memory_tv(kernel, pi))
    full_status = memory_status_float(full_tv, residual)
    if probe:
        count_tv = None
        count_status = None
    else:
        count_tv = float(observation_memory_tv(kernel, pi, _count_observation(kernel.n_states, n_pairs)))
        count_status = memory_status_float(count_tv, residual)
    if landing is None:
        epoch_tv, epoch_defect = None, None
        epoch_info = {"cmi_triad_to_next_pair_bits": None, "cmi_pair_to_next_triad_bits": None}
        epoch_status = "unresolved"
        reconfig = {"max_abs_delta_flux": None, "argmax": None, "effect": None, "category_flux_delta": None}
    else:
        epoch_tv, epoch_defect = pair_event_epoch_memory_tv_float(kernel, pi, landing, defect)
        epoch_status = memory_status_float(epoch_tv, residual)
        if probe:
            epoch_info = {"cmi_triad_to_next_pair_bits": None, "cmi_pair_to_next_triad_bits": None}
            reconfig = _reconfig_against(kernel, pi, landing, baseline_pack, focused=False)
        else:
            epoch_info = epoch_predictive_information_float(kernel, pi, landing, defect)
            reconfig = _reconfig_against(kernel, pi, landing, baseline_pack, focused=True)
    if kernel.n_states <= 16:
        jump, jump_tv_exact = pair_jump_dependence(kernel)
        jump_tv = _fraction_text(jump_tv_exact)
    else:
        jump, jump_distance = pair_jump_dependence_float(kernel)
        jump_tv = jump_distance
    return {
        "arithmetic": arithmetic,
        "residual": residual,
        "periods": list(periods),
        "pair_jump": bool(jump),
        "pair_jump_tv": jump_tv,
        "triad_rate": bool(triad_rate_depends_on_pairs(kernel)),
        "triad_weight": bool(triad_weight_depends_on_pairs(kernel)),
        "full_tv": full_tv,
        "full_status": full_status,
        "epoch_tv": epoch_tv,
        "epoch_status": epoch_status,
        "epoch_defect": epoch_defect,
        "cmi_full_triad_to_pair": None if probe else full_event_cmi_triad_to_pair(kernel, pi),
        "cmi_epoch_triad_to_pair": epoch_info.get("cmi_triad_to_next_pair_bits"),
        "cmi_epoch_pair_to_triad": epoch_info.get("cmi_pair_to_next_triad_bits"),
        "projection_b_tv": count_tv,
        "projection_b_status": count_status,
        "restores_markov": bool(full_status == "positive" and count_status == "zero"),
        "axis_e": None if probe else _axis_e_n4(kernel, index_kernels, tables, cache),
        "reconfig_max_abs_delta": reconfig.get("max_abs_delta_flux"),
        "reconfig_argmax": reconfig.get("argmax"),
        "reconfig_effect": reconfig.get("effect"),
        "category_flux_delta": reconfig.get("category_flux_delta"),
        "focused_path_to_matching": reconfig.get("focused_path_to_matching"),
        "focused_matching_to_path": reconfig.get("focused_matching_to_path"),
    }


def prepare_baseline_pack(kernel: Kernel) -> dict:
    pi, residual, arithmetic, periods = float_stationary(kernel)
    landing, defect = epoch_kernel_float(kernel)
    if landing is None:
        raise RuntimeError("unconstrained N=4 epoch kernel did not solve")
    table = pair_classes()
    flux = class_flux(kernel, pi, landing, table)
    forward = focused_transition(kernel, pi, landing, table.path_name, table.matching_name, table)
    backward = focused_transition(kernel, pi, landing, table.matching_name, table.path_name, table)
    return {
        "pi": pi,
        "residual": residual,
        "arithmetic": arithmetic,
        "periods": list(periods),
        "landing": landing,
        "defect": defect,
        "flux": flux,
        "forward": forward,
        "backward": backward,
        "kernel": kernel,
    }


def _reconfig_against(
    kernel: Kernel,
    pi: np.ndarray,
    landing: np.ndarray,
    baseline_pack: dict,
    *,
    focused: bool = True,
) -> dict:
    table = pair_classes()
    constrained = class_flux(kernel, pi, landing, table)
    delta = constrained - baseline_pack["flux"]
    best_abs = 0.0
    best = None
    for left_index, left in enumerate(table.representatives):
        for right_index, right in enumerate(table.representatives):
            if table.by_mask[left]["edge_count"] != table.by_mask[right]["edge_count"]:
                continue
            if left == right:
                continue
            value = float(delta[left_index, right_index])
            if best is None or abs(value) > best_abs:
                base = float(baseline_pack["flux"][left_index, right_index])
                best_abs = abs(value)
                best = {
                    "source": table.by_mask[left]["name"],
                    "target": table.by_mask[right]["name"],
                    "edge_count": table.by_mask[left]["edge_count"],
                    "delta_flux": value,
                    "constrained_flux": float(constrained[left_index, right_index]),
                    "baseline_flux": base,
                    "ratio": None if base <= 1e-8 else float(constrained[left_index, right_index]) / base,
                }
    if focused:
        forward = focused_transition(kernel, pi, landing, table.path_name, table.matching_name, table)
        backward = focused_transition(kernel, pi, landing, table.matching_name, table.path_name, table)
        forward_row = _delta_hit(forward, baseline_pack["forward"])
        backward_row = _delta_hit(backward, baseline_pack["backward"])
    else:
        forward_row = None
        backward_row = None
    return {
        "measure": RECONFIGURATION_MEASURE,
        "horizon": RECONFIGURATION_HORIZON,
        "max_abs_delta_flux": best_abs,
        "argmax": best,
        "effect": best_abs > 1e-8,
        "category_flux_delta": _category_delta(table, constrained, baseline_pack["flux"]),
        "focused_path_to_matching": forward_row,
        "focused_matching_to_path": backward_row,
    }


def _category_delta(table, constrained, baseline) -> dict[str, float]:
    totals = {"different_edge_count": 0.0, "same_edge_count_isomorphic": 0.0, "same_edge_count_nonisomorphic": 0.0}
    base = dict(totals)
    for left_index, left in enumerate(table.representatives):
        for right_index, right in enumerate(table.representatives):
            if table.by_mask[left]["edge_count"] != table.by_mask[right]["edge_count"]:
                key = "different_edge_count"
            elif left == right:
                key = "same_edge_count_isomorphic"
            else:
                key = "same_edge_count_nonisomorphic"
            totals[key] += float(constrained[left_index, right_index])
            base[key] += float(baseline[left_index, right_index])
    return {key: totals[key] - base[key] for key in totals}


def _delta_hit(constrained: dict, baseline: dict) -> dict:
    hit = (constrained.get("passage") or {}).get("hit_before_return")
    base_hit = (baseline.get("passage") or {}).get("hit_before_return")
    delta = None if hit is None or base_hit is None else hit - base_hit
    return {
        "hit_before_return": hit,
        "baseline_hit_before_return": base_hit,
        "delta_hit_before_return": delta,
        "triad_changes_hit": constrained.get("triad_changes_hit"),
        "triad_hit_spread": constrained.get("triad_hit_spread"),
        "triad_changes_one_step": constrained.get("triad_changes_one_step"),
        "mean_status": (constrained.get("passage") or {}).get("mean_status"),
        "mean_pair_events_given_hit": (constrained.get("passage") or {}).get("mean_pair_events_given_hit"),
        "unresolved_within_horizon": (constrained.get("passage") or {}).get("unresolved_within_horizon"),
    }


def independent_hypergraph_orbits(n: int) -> dict:
    """S_N orbits of the full independent-hypergraph state.

    The count is exact. It is the number of distinct labelled states up to
    entity relabeling, not the number of pairwise graphs.
    """
    from rs_constraint_lab.state import permutations, relabel_relation_state, relation_slots

    slots = tuple(relation_slots(n, 3))
    perms = permutations(n)
    n_states = 1 << len(slots)
    seen = [False] * n_states
    orbits = 0
    for state in range(n_states):
        if seen[state]:
            continue
        for perm in perms:
            seen[relabel_relation_state(state, perm, slots)] = True
        orbits += 1
    if not all(seen):
        raise RuntimeError("hypergraph orbits do not cover the labelled states")
    return {"labelled_states": n_states, "orbit_count": orbits, "slots": len(slots)}


def n4_baseline_certificate(kernel: Kernel) -> dict:
    """Structural and numerical checks for the unconstrained N=4, O=3 chain.

    Uniformity is exact when every state has the same ten successors of
    probability 1/10 and every transition has its reverse. The numerical
    solve is recorded beside that fact and is not called an exact distribution.
    """
    n_pairs, n_triads = layout(kernel)
    symmetric = True
    toggles = []
    for state, row in enumerate(kernel.successors):
        if kernel.deadlock[state] or len(row) != n_pairs + n_triads:
            toggles.append(len(row))
            symmetric = False
            continue
        toggles.append(len(row))
        for nxt, prob in row:
            if prob != Fraction(1, n_pairs + n_triads):
                symmetric = False
            reverse = kernel.probability(nxt, state)
            if reverse != prob:
                symmetric = False
    ran = long_run(kernel, 0)
    pi = np.zeros(kernel.n_states, dtype=np.float64)
    for state, prob in ran["distribution"].items():
        pi[state] = prob
    uniform = np.full(kernel.n_states, 1.0 / kernel.n_states)
    tv_uniform = 0.5 * float(np.abs(pi - uniform).sum())
    landing, defect = epoch_kernel_float(kernel)
    full_tv = float(full_event_pair_memory_tv(kernel, pi))
    count_tv = float(observation_memory_tv(kernel, pi, _count_observation(kernel.n_states, n_pairs)))
    epoch_tv = None
    if landing is not None:
        epoch_tv, _epoch_defect = pair_event_epoch_memory_tv_float(kernel, pi, landing, defect)
    cmi = full_event_cmi_triad_to_pair(kernel, pi)
    jump, jump_tv = pair_jump_dependence(kernel)
    classes = pair_classes()
    orbits = independent_hypergraph_orbits(kernel.n)
    bit_means = []
    for bit in range(n_pairs + n_triads):
        bit_means.append(float(sum(pi[state] for state in range(kernel.n_states) if (state >> bit) & 1)))
    pair_triad_joint_gap = 0.0
    for pair_bit in range(n_pairs):
        for triad_bit in range(n_pairs, n_pairs + n_triads):
            joint = float(
                sum(
                    pi[state]
                    for state in range(kernel.n_states)
                    if (state >> pair_bit) & 1 and (state >> triad_bit) & 1
                )
            )
            pair_triad_joint_gap = max(pair_triad_joint_gap, abs(joint - 0.25))
    return {
        "states": kernel.n_states,
        "slots": n_pairs + n_triads,
        "pair_slots": n_pairs,
        "triad_slots": n_triads,
        "toggles_per_state_min": min(toggles) if toggles else 0,
        "toggles_per_state_max": max(toggles) if toggles else 0,
        "symmetric_regular": symmetric,
        "uniform_stationary_by_symmetry": symmetric,
        "periods": list(ran["periods"]),
        "stationary_arithmetic": ran["stationary_arithmetic"],
        "stationary_residual": float(ran["stationary_residual"]),
        "tv_from_uniform_numerical": tv_uniform,
        "pair_bit_means": bit_means[:n_pairs],
        "triad_bit_means": bit_means[n_pairs:],
        "expected_pair_density": float(sum(bit_means[:n_pairs]) / n_pairs) if n_pairs else None,
        "expected_triad_occupancy": float(sum(bit_means[n_pairs:])),
        "pair_triad_joint_gap": pair_triad_joint_gap,
        "hypergraph_orbit_count": orbits["orbit_count"],
        "pair_jump_dependence": bool(jump),
        "pair_jump_tv": _fraction_text(jump_tv),
        "triad_rate_dependence": bool(triad_rate_depends_on_pairs(kernel)),
        "full_event_clock_tv": full_tv,
        "full_event_clock_status": memory_status_float(full_tv, float(ran["stationary_residual"])),
        "pair_event_epoch_tv": epoch_tv,
        "pair_event_epoch_status": memory_status_float(epoch_tv, float(ran["stationary_residual"])),
        "projection_b_tv": count_tv,
        "cmi_triad_to_next_pair": cmi,
        "pairwise_class_count": len(classes.representatives),
        "focused_classes": {"path": classes.path_name, "matching": classes.matching_name},
        "epoch_defect": defect,
    }


def _finish_receipt(task: dict, shard_dir: Path, result: dict, started: float, counts: dict) -> None:
    identity = task["identity"]
    result_path = shard_dir / "result.json"
    atomic_write_json(result_path, result)
    digest = sha256_file(result_path)
    receipt = {
        "status": "completed",
        "shard_id": task["shard_id"],
        "identity": identity,
        "result_sha256": digest,
        "attempt": task["attempt"],
        "engine_version": identity["engine_version"],
        "semantic_version": identity["semantic_version"],
        "spec_hash": identity["spec_hash"],
        "grammar_version": identity["grammar_version"],
        "normalisation_version": identity["normalisation_version"],
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "counts": counts,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "finished_at": _now(),
    }
    atomic_write_json(shard_dir / "receipt.json", receipt)
    (shard_dir / "running.json").unlink(missing_ok=True)


def _require_version(task: dict) -> None:
    identity = task["identity"]
    engine, semantic = hypergraph_version_for_n(int(task["n"]))
    if identity.get("engine_version") != engine or identity.get("semantic_version") != semantic:
        raise RuntimeError("shard identity does not match this independent-hypergraph version")


def _walk(task: dict, grammar, on_set) -> dict:
    counts = {
        "scanned": 0,
        "symmetry_removed": 0,
        "stacked_canonical": 0,
        "stacked_analysed": 0,
        "analysed": 0,
    }
    start = int(task["start"])
    end = int(task["end"])
    cardinality = int(task["cardinality"])
    labelled_n = len(grammar.labelled)
    if labelled_n < cardinality or end <= start:
        counts["canonical_including_stacked"] = 0
        counts["canonical_simple"] = 0
        return counts
    combo = unrank_combination(start, labelled_n, cardinality)
    for index in range(start, end):
        ids = combo
        counts["scanned"] += 1
        constraints = tuple(grammar.labelled[i] for i in ids)
        simple = structurally_simple(constraints)
        if not is_canonical_ids(ids, grammar.image):
            counts["symmetry_removed"] += 1
        elif not simple:
            counts["stacked_canonical"] += 1
        else:
            on_set(constraints)
            counts["analysed"] += 1
        combo = next_combination(combo, labelled_n)
        if combo is None and index + 1 < end:
            raise RuntimeError("combination index ended before the shard boundary")
    counts["canonical_including_stacked"] = counts["stacked_canonical"] + counts["analysed"]
    counts["canonical_simple"] = counts["analysed"]
    return counts


def execute_memory_clock_shard(task: dict) -> None:
    """Rebuild Generation 3 kernels and record the two clocks. No family census."""
    from rs_constraint_lab.higher_order import load_comparison_indexes
    from rs_constraint_lab.spec import effective_options

    _require_version(task)
    if int(task["n"]) != 3 or task["spec"].get("analysis") != ANALYSIS_CLOCKS:
        raise RuntimeError("memory-clock reanalysis executes independent hypergraph only at N=3")
    shard_dir = Path(task["shard_dir"])
    shard_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(
        shard_dir / "running.json",
        {"shard_id": task["shard_id"], "attempt": task["attempt"], "started_at": _now(), "pid": os.getpid()},
    )
    started = time.perf_counter()
    spec = task["spec"]
    options = effective_options(spec)
    grammar = build_grammar(
        int(task["n"]),
        int(task["k_max"]),
        spec.get("weights"),
        a_max=task["a_max"],
        predicates=tuple(options["predicates"]),
        order=3,
    )
    factors = alphabet_factors(spec["alphabet"])
    indexes = load_comparison_indexes()
    tables = RelabelTables(3)
    slots = grammar.relation_slots
    rows = []
    slot_list = grammar.slot_list()

    def on_set(constraints) -> None:
        expressions = tuple(sorted(constraint.expression(slot_list) for constraint in constraints))
        primary = build_slotted(3, constraints, factors, slots, Fraction(1))
        report = assess_n3_clocks(primary, indexes, tables)
        sensitivity = {}
        for label, rho in (("1/2", Fraction(1, 2)), ("2", Fraction(2))):
            other = build_slotted(3, constraints, factors, slots, rho)
            sensitivity[label] = _clock_only_n3(other)
        rows.append(
            {
                "expressions": list(expressions),
                "cardinality": int(task["cardinality"]),
                "k": max(constraint.k() for constraint in constraints),
                "cross_order_class": set_cross_order_class(constraints, 3),
                "primary": report,
                "sensitivity": sensitivity,
            }
        )

    counts = _walk(task, grammar, on_set)
    result = {
        "identity": task["identity"],
        "counts": counts,
        "families": {},
        "singles": [],
        "extremes": {},
        "cancellations": {},
        "sensitivity": {"checks": 0, "modal_unchanged": 0, "support_unchanged": 0},
        "threshold_motifs": [],
        "clock_rows": rows,
    }
    _finish_receipt(task, shard_dir, result, started, counts)


def execute_n4_shard(task: dict) -> None:
    from rs_constraint_lab.spec import effective_options

    _require_version(task)
    if int(task["n"]) != 4 or int(task["cardinality"]) != 1 or task["spec"].get("analysis") != ANALYSIS_N4:
        raise RuntimeError("the N=4 census executes K<=2 cardinality 1 only")
    declared = task["spec"].get("reconfiguration_measure")
    if declared is not None and declared != RECONFIGURATION_MEASURE:
        raise RuntimeError("refusing to run: the spec measure is not the predeclared flux delta")
    declared_horizon = task["spec"].get("reconfiguration_horizon")
    if declared_horizon is not None and int(declared_horizon) != RECONFIGURATION_HORIZON:
        raise RuntimeError("refusing to run: the spec horizon is not the predeclared pair-event horizon")
    shard_dir = Path(task["shard_dir"])
    shard_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(
        shard_dir / "running.json",
        {"shard_id": task["shard_id"], "attempt": task["attempt"], "started_at": _now(), "pid": os.getpid()},
    )
    started = time.perf_counter()
    spec = task["spec"]
    options = effective_options(spec)
    grammar = build_grammar(
        4,
        int(task["k_max"]),
        spec.get("weights"),
        a_max=task["a_max"],
        predicates=tuple(options["predicates"]),
        order=3,
    )
    factors = alphabet_factors(spec["alphabet"])
    slots = grammar.relation_slots
    slot_list = grammar.slot_list()
    index = load_n4_pairwise_index()
    tables = RelabelTables(4)
    cache: dict = {}
    baseline_packs = {
        "1": prepare_baseline_pack(build_slotted(4, (), factors, slots, Fraction(1))),
        "1/2": prepare_baseline_pack(build_slotted(4, (), factors, slots, Fraction(1, 2))),
        "2": prepare_baseline_pack(build_slotted(4, (), factors, slots, Fraction(2))),
    }
    # Unconstrained weights do not use the alphabet, so alphabet variants
    # share the rho=1 baseline.
    sensitivity_factors = [(name, alphabet_factors(name)) for name in spec.get("sensitivity_alphabets", [])]
    rows = []

    def on_set(constraints) -> None:
        expression = constraints[0].expression(slot_list)
        kernel = build_slotted(4, constraints, factors, slots, Fraction(1))
        report = assess_n4(kernel, baseline_packs["1"], index["kernels"], tables, cache)
        primary_support, primary_modal = _weight_patterns(kernel)
        chosen = (report.get("reconfig_argmax") or {})
        sensitivity = {}
        for label, rho in (("1/2", Fraction(1, 2)), ("2", Fraction(2))):
            other = build_slotted(4, constraints, factors, slots, rho)
            probed = assess_n4(other, baseline_packs[label], index["kernels"], tables, cache, probe=True)
            # Pair-slice weights do not include the triad baseline, so rho3
            # cannot move the searched-grammar membership of those slices.
            probed["axis_e"] = report["axis_e"]
            sensitivity[label] = _sensitivity_flags(report, probed, chosen, primary_support, primary_modal, other)
        for name, extra_factors in sensitivity_factors:
            other = build_slotted(4, constraints, extra_factors, slots, Fraction(1))
            probed = assess_n4(other, baseline_packs["1"], index["kernels"], tables, cache, probe=True)
            probed["axis_e"] = _axis_e_n4(other, index["kernels"], tables, cache)
            sensitivity[name] = _sensitivity_flags(report, probed, chosen, primary_support, primary_modal, other)
        rows.append(
            {
                "expression": expression,
                "k": constraints[0].k(),
                "cross_order_class": cross_order_class(constraints[0], 6),
                "weight": constraints[0].weight,
                "primary": _public_n4(report),
                "sensitivity": sensitivity,
            }
        )

    counts = _walk(task, grammar, on_set)
    result = {
        "identity": task["identity"],
        "counts": counts,
        "families": {},
        "singles": [],
        "extremes": {},
        "cancellations": {},
        "sensitivity": {"checks": len(rows) * (2 + len(sensitivity_factors)), "modal_unchanged": 0, "support_unchanged": 0},
        "threshold_motifs": [],
        "n4_rows": rows,
        "index": {
            "sha256": index["sha256"],
            "baseline_was_added": index["baseline_was_added"],
            "domain": index.get("domain"),
        },
    }
    _finish_receipt(task, shard_dir, result, started, counts)


def _public_n4(report: dict) -> dict:
    hidden = {"support_pattern", "modal_pattern"}
    return {key: value for key, value in report.items() if key not in hidden}


def _sensitivity_flags(primary: dict, other: dict, chosen: dict, support, modal, other_kernel: Kernel) -> dict:
    other_support, other_modal = _weight_patterns(other_kernel)
    delta = None
    if chosen:
        # The variant's own argmax may differ. Robustness of the primary pair
        # is read from the variant row's argmax only when it names the same
        # classes; otherwise the sign comparison is unresolved and recorded
        # from the variant's maximum absolute delta sign as a separate field.
        delta = (other.get("reconfig_argmax") or {}).get("delta_flux")
        same_pair = (
            (other.get("reconfig_argmax") or {}).get("source") == chosen.get("source")
            and (other.get("reconfig_argmax") or {}).get("target") == chosen.get("target")
        )
    else:
        same_pair = False
    return {
        "pair_jump": other["pair_jump"],
        "full_status": other["full_status"],
        "epoch_status": other["epoch_status"],
        "axis_e": other["axis_e"],
        "reconfig_effect": other["reconfig_effect"],
        "reconfig_delta_sign": _sign(delta),
        "primary_pair_still_argmax": same_pair,
        "jump_unchanged": other["pair_jump"] == primary["pair_jump"],
        "full_unchanged": other["full_status"] == primary["full_status"],
        "epoch_unchanged": other["epoch_status"] == primary["epoch_status"],
        "axis_e_unchanged": other["axis_e"] == primary["axis_e"],
        "reconfig_effect_unchanged": other["reconfig_effect"] == primary["reconfig_effect"],
        "support_unchanged": other_support == support,
        "modal_unchanged": other_modal == modal,
    }


def _invariant(primary: dict, sensitivity: dict, key: str) -> bool:
    return all(row.get(key) == primary.get(key) for row in sensitivity.values())


def summarise_clock_rows(rows: list[dict]) -> dict:
    """Answer the Generation 3 reanalysis questions from stored rows."""
    classes = Counter()
    reducibility = Counter()
    cross = Counter()
    full_by_class = {name: Counter() for name in ("P->P", "P->T", "T->P", "T->T", "mixed")}
    epoch_by_class = {name: Counter() for name in full_by_class}
    full_positive = 0
    epoch_positive = 0
    both = 0
    full_positive_epoch_zero = 0
    full_positive_epoch_undefined = 0
    jump_no_epoch_yes = 0
    jump_yes_epoch_zero = 0
    max_epoch = None
    rho_changed = Counter()
    for row in rows:
        label = row["cross_order_class"]
        classes[label] += 1
        primary = row["primary"]
        reducibility[primary["historical_reducibility"]] += 1
        key = (
            "YES" if primary["pair_jump"] else "NO",
            primary["full_status"],
            primary["epoch_status"],
            "YES" if primary["triad_rate"] else "NO",
        )
        cross[key] += 1
        full_by_class[label][primary["full_status"]] += 1
        epoch_by_class[label][primary["epoch_status"]] += 1
        epoch_by_class[label]["n"] += 1
        if primary["full_status"] == "positive":
            full_positive += 1
            if primary["epoch_status"] == "positive":
                both += 1
            elif primary["epoch_status"] == "zero":
                full_positive_epoch_zero += 1
            else:
                full_positive_epoch_undefined += 1
        if primary["epoch_status"] == "positive":
            epoch_positive += 1
            if not primary["pair_jump"]:
                jump_no_epoch_yes += 1
            value = Fraction(primary["epoch_tv"])
            if max_epoch is None or value > max_epoch[0]:
                max_epoch = (value, row["expressions"], label, primary["pair_jump"], primary["triad_rate"])
        if primary["pair_jump"] and primary["epoch_status"] == "zero":
            jump_yes_epoch_zero += 1
        for rho, probed in row["sensitivity"].items():
            for field in ("pair_jump", "triad_rate", "full_status", "epoch_status"):
                if probed[field] != primary[field]:
                    rho_changed[f"{rho}:{field}"] += 1
    mechanism = None
    if max_epoch is not None:
        mechanism = {
            "epoch_tv": _fraction_text(max_epoch[0]),
            "expressions": list(max_epoch[1]),
            "cross_order_class": max_epoch[2],
            "pair_jump": max_epoch[3],
            "triad_rate": max_epoch[4],
        }
    pure = {}
    for label in ("T->P", "P->T", "T->T", "P->P", "mixed"):
        pure[label] = {
            "n": epoch_by_class[label]["n"],
            "full_positive": full_by_class[label]["positive"],
            "full_zero": full_by_class[label]["zero"],
            "epoch_positive": epoch_by_class[label]["positive"],
            "epoch_zero": epoch_by_class[label]["zero"],
            "epoch_undefined": epoch_by_class[label]["undefined"],
        }
    return {
        "analysed": len(rows),
        "class_counts": dict(classes),
        "historical_reducibility": dict(reducibility),
        "full_event_positive": full_positive,
        "epoch_positive": epoch_positive,
        "both_positive": both,
        "full_positive_epoch_zero": full_positive_epoch_zero,
        "full_positive_epoch_undefined": full_positive_epoch_undefined,
        "jump_no_epoch_positive": jump_no_epoch_yes,
        "jump_yes_epoch_zero": jump_yes_epoch_zero,
        "largest_epoch": mechanism,
        "pure": pure,
        "rho_status_changes": dict(rho_changed),
        "cross_tab": [
            {
                "pair_jump": key[0],
                "full_event": key[1],
                "pair_event_epoch": key[2],
                "triad_rate": key[3],
                "count": count,
            }
            for key, count in sorted(cross.items())
        ],
    }


def _check_gen3_reproduction(summary_counts: dict) -> None:
    if summary_counts["analysed"] != GEN3_ANALYSED:
        raise RuntimeError(
            f"memory reanalysis analysed {summary_counts['analysed']} sets; Generation 3 analysed {GEN3_ANALYSED}"
        )
    if summary_counts["full_event_positive"] != GEN3_FULL_EVENT_POSITIVE:
        raise RuntimeError(
            "full-event clock does not reproduce Generation 3's "
            f"{GEN3_FULL_EVENT_POSITIVE} positive sets "
            f"(got {summary_counts['full_event_positive']})"
        )
    if summary_counts["class_counts"] != GEN3_CLASS_COUNTS:
        raise RuntimeError(f"class counts drifted from Generation 3: {summary_counts['class_counts']}")
    reducibility = {key: 0 for key in GEN3_REDUCIBILITY}
    reducibility.update(summary_counts["historical_reducibility"])
    if reducibility != GEN3_REDUCIBILITY:
        raise RuntimeError(
            f"historical reducibility drifted from Generation 3: {reducibility}"
        )
    summary_counts["historical_reducibility"] = reducibility


def _write_clock_csv(path: Path, rows: list[dict]) -> None:
    fields = [
        "expressions", "cardinality", "k", "cross_order_class", "historical_reducibility",
        "pair_jump", "pair_jump_tv", "triad_rate", "triad_weight", "full_tv", "full_status",
        "epoch_tv", "epoch_status", "epoch_defect", "axis_e",
        "cmi_epoch_triad_to_pair", "cmi_epoch_pair_to_triad",
        "rho_half_full", "rho_half_epoch", "rho_half_jump", "rho_half_rate",
        "rho_2_full", "rho_2_epoch", "rho_2_jump", "rho_2_rate",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            primary = row["primary"]
            half = row["sensitivity"]["1/2"]
            double = row["sensitivity"]["2"]
            writer.writerow(
                {
                    "expressions": " && ".join(row["expressions"]),
                    "cardinality": row["cardinality"],
                    "k": row["k"],
                    "cross_order_class": row["cross_order_class"],
                    "historical_reducibility": primary["historical_reducibility"],
                    "pair_jump": int(primary["pair_jump"]),
                    "pair_jump_tv": primary["pair_jump_tv"],
                    "triad_rate": int(primary["triad_rate"]),
                    "triad_weight": int(primary["triad_weight"]),
                    "full_tv": primary["full_tv"],
                    "full_status": primary["full_status"],
                    "epoch_tv": primary["epoch_tv"] or "",
                    "epoch_status": primary["epoch_status"],
                    "epoch_defect": primary["epoch_defect"],
                    "axis_e": primary["axis_e"],
                    "cmi_epoch_triad_to_pair": primary["cmi_epoch_triad_to_pair"],
                    "cmi_epoch_pair_to_triad": primary["cmi_epoch_pair_to_triad"],
                    "rho_half_full": half["full_status"],
                    "rho_half_epoch": half["epoch_status"],
                    "rho_half_jump": int(half["pair_jump"]),
                    "rho_half_rate": int(half["triad_rate"]),
                    "rho_2_full": double["full_status"],
                    "rho_2_epoch": double["epoch_status"],
                    "rho_2_jump": int(double["pair_jump"]),
                    "rho_2_rate": int(double["triad_rate"]),
                }
            )


def _write_n4_csv(path: Path, rows: list[dict]) -> None:
    fields = [
        "expression", "k", "cross_order_class", "weight", "residual", "arithmetic", "periods",
        "pair_jump", "pair_jump_tv", "triad_rate", "triad_weight", "full_tv", "full_status",
        "epoch_tv", "epoch_status", "epoch_defect", "cmi_full_triad_to_pair",
        "cmi_epoch_triad_to_pair", "cmi_epoch_pair_to_triad", "projection_b_tv",
        "projection_b_status", "restores_markov", "axis_e", "reconfig_max_abs_delta",
        "reconfig_source", "reconfig_target", "reconfig_delta", "reconfig_ratio",
        "reconfig_effect", "focused_delta_hit_path_to_matching", "focused_triad_changes_hit",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            primary = row["primary"]
            argmax = primary.get("reconfig_argmax") or {}
            focused = primary.get("focused_path_to_matching") or {}
            writer.writerow(
                {
                    "expression": row["expression"],
                    "k": row["k"],
                    "cross_order_class": row["cross_order_class"],
                    "weight": row["weight"],
                    "residual": primary["residual"],
                    "arithmetic": primary["arithmetic"],
                    "periods": " ".join(str(item) for item in primary["periods"]),
                    "pair_jump": int(primary["pair_jump"]),
                    "pair_jump_tv": primary["pair_jump_tv"],
                    "triad_rate": int(primary["triad_rate"]),
                    "triad_weight": int(primary["triad_weight"]),
                    "full_tv": primary["full_tv"],
                    "full_status": primary["full_status"],
                    "epoch_tv": "" if primary["epoch_tv"] is None else primary["epoch_tv"],
                    "epoch_status": primary["epoch_status"],
                    "epoch_defect": primary["epoch_defect"],
                    "cmi_full_triad_to_pair": primary["cmi_full_triad_to_pair"],
                    "cmi_epoch_triad_to_pair": primary["cmi_epoch_triad_to_pair"],
                    "cmi_epoch_pair_to_triad": primary["cmi_epoch_pair_to_triad"],
                    "projection_b_tv": primary["projection_b_tv"],
                    "projection_b_status": primary["projection_b_status"],
                    "restores_markov": int(bool(primary["restores_markov"])),
                    "axis_e": primary["axis_e"],
                    "reconfig_max_abs_delta": primary["reconfig_max_abs_delta"],
                    "reconfig_source": argmax.get("source", ""),
                    "reconfig_target": argmax.get("target", ""),
                    "reconfig_delta": argmax.get("delta_flux", ""),
                    "reconfig_ratio": argmax.get("ratio", ""),
                    "reconfig_effect": "" if primary["reconfig_effect"] is None else int(bool(primary["reconfig_effect"])),
                    "focused_delta_hit_path_to_matching": focused.get("delta_hit_before_return", ""),
                    "focused_triad_changes_hit": "" if focused.get("triad_changes_hit") is None else int(bool(focused.get("triad_changes_hit"))),
                }
            )


def _empty_hashes(out_dir: Path, n: int, k_max: int) -> dict[str, str]:
    names = {
        "family_index_sha256": out_dir / f"families-n{n}-k{k_max}.jsonl",
        "singles_sha256": out_dir / f"singles-n{n}-k{k_max}.csv",
        "kernel_index_sha256": out_dir / f"kernel-ids-n{n}-k{k_max}.txt",
        "qualitative_index_sha256": out_dir / f"qualitative-ids-n{n}-k{k_max}.txt",
        "observable_index_sha256": out_dir / f"observable-ids-n{n}-k{k_max}.txt",
    }
    written = {}
    for key, path in names.items():
        if not path.exists():
            path.write_text("", encoding="utf-8")
        written[key] = sha256_file(path)
    return written


def merge_census(out_dir: Path, plan: dict, publish: Path | None = None) -> dict:
    """Merge a clock or N=4 census without the Generation 3 heavy path."""
    from rs_constraint_lab.execution import _fingerprint, _reconcile
    from rs_constraint_lab.generation import _git_commit, _publish
    from rs_constraint_lab.version import EXECUTION_PRINCIPLE, MAX_ATTEMPTS, PROFILE_NOTE

    out_dir = Path(out_dir)
    progress = _reconcile(out_dir, plan)
    spec = plan["spec"]
    analysis = spec.get("analysis")
    rows: list[dict] = []
    counts: dict[str, dict] = {}
    work = 0.0
    index_meta = None
    for shard in plan["shards"]:
        state = progress["shards"][shard["shard_id"]]
        card = str(shard["cardinality"])
        bucket = counts.setdefault(
            card,
            {"scanned": 0, "symmetry_removed": 0, "stacked_canonical": 0, "analysed": 0, "canonical_including_stacked": 0, "canonical_simple": 0},
        )
        if state["status"] != "completed":
            continue
        result = read_json(out_dir / "shards" / shard["shard_id"] / "result.json")
        for name, value in result["counts"].items():
            bucket[name] = bucket.get(name, 0) + value
        rows.extend(result.get("clock_rows") or result.get("n4_rows") or [])
        if result.get("index"):
            index_meta = result["index"]
        receipt = read_json(out_dir / "shards" / shard["shard_id"] / "receipt.json")
        work += float(receipt.get("elapsed_seconds") or 0.0)
    cell = spec["cells"][0]
    n = int(cell["N"])
    k_max = int(cell["K_max"])
    estimate = plan["estimates"]["cells"][0]
    if progress["status"] == "COMPLETE":
        for cardinality, info in estimate["cardinalities"].items():
            got = counts.get(cardinality, {}).get("canonical_simple", 0)
            planned = info.get("canonical_simple_exact")
            scanned = counts.get(cardinality, {})
            pieces = (
                scanned.get("analysed", 0)
                + scanned.get("stacked_canonical", 0)
                + scanned.get("symmetry_removed", 0)
            )
            if pieces != info["labelled_combinations"]:
                raise RuntimeError(f"coverage gap at cardinality {cardinality}")
            if planned is not None and got != planned:
                raise RuntimeError(f"canonical coverage {got} != planned {planned}")
    clock_summary = None
    n4_summary = None
    if analysis == ANALYSIS_CLOCKS and progress["status"] == "COMPLETE":
        clock_summary = summarise_clock_rows(rows)
        if spec["experiment_id"] == "generation-003c-memory-clock-refinement":
            _check_gen3_reproduction(clock_summary)
        csv_path = out_dir / f"singles-n{n}-k{k_max}.csv"
        _write_clock_csv(csv_path, rows)
    if analysis == ANALYSIS_N4 and progress["status"] == "COMPLETE":
        n4_summary = summarise_n4_rows(rows, spec)
        csv_path = out_dir / f"singles-n{n}-k{k_max}.csv"
        _write_n4_csv(csv_path, rows)
    hashes = _empty_hashes(out_dir, n, k_max) if progress["status"] == "COMPLETE" else {
        "family_index_sha256": "",
        "singles_sha256": "",
        "kernel_index_sha256": "",
        "qualitative_index_sha256": "",
        "observable_index_sha256": "",
    }
    if progress["status"] == "COMPLETE" and (out_dir / f"singles-n{n}-k{k_max}.csv").exists():
        hashes["singles_sha256"] = sha256_file(out_dir / f"singles-n{n}-k{k_max}.csv")
    cardinalities = {}
    for cardinality, info in estimate["cardinalities"].items():
        scanned = counts.get(cardinality, {})
        cardinalities[cardinality] = {
            "labelled_combinations": info["labelled_combinations"],
            "labelled_simple": info["labelled_simple"],
            "labelled_stacked": info["labelled_stacked"],
            "canonical": scanned.get("canonical_simple", 0),
            "canonical_including_stacked": scanned.get("canonical_including_stacked", 0),
            "stacked_canonical": scanned.get("stacked_canonical", 0),
            "removed_by_symmetry": scanned.get("symmetry_removed", 0),
            "analysed": scanned.get("analysed", 0),
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
        "canonical_states": estimate["canonical_states"],
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
        "kernel_index_count": 0,
        **hashes,
        "clock_census": clock_summary,
        "n4_census": n4_summary,
        "pairwise_index": index_meta,
    }
    summary = {
        "status": progress["status"],
        "engine_version": plan["header"]["engine_version"],
        "semantic_version": plan["header"]["semantic_version"],
        "git_commit": _git_commit(),
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "platform": sys.platform,
        "spec_hash": plan["header"]["spec_hash"],
        "experiment_id": spec["experiment_id"],
        "generation": spec["generation"],
        "composition": spec.get("composition", "structural-simple"),
        "predicates": list(spec.get("predicates", [])),
        "analysis": analysis,
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
        "reconfiguration_measure": RECONFIGURATION_MEASURE if analysis == ANALYSIS_N4 else None,
        "reconfiguration_horizon": RECONFIGURATION_HORIZON if analysis == ANALYSIS_N4 else None,
    }
    summary["science"] = {
        "status": summary["status"],
        "spec_hash": summary["spec_hash"],
        "semantic_version": summary["semantic_version"],
        "composition": summary["composition"],
        "predicates": summary["predicates"],
        "analysis": analysis,
        "cells": [
            {
                "N": n,
                "K_max": k_max,
                "families": 0,
                "cardinalities": cardinalities,
                "clock_census": clock_summary,
                "n4_census": n4_summary,
            }
        ],
    }
    atomic_write_json(out_dir / "summary.json", json_ready(summary))
    if publish is not None and summary["status"] == "COMPLETE":
        _publish(summary, spec, Path(publish), out_dir)
    return summary


def summarise_n4_rows(rows: list[dict], spec: dict) -> dict:
    by_class = Counter(row["cross_order_class"] for row in rows)
    by_k = Counter(row["k"] for row in rows)
    jump = Counter()
    full = Counter()
    epoch = Counter()
    axis = Counter()
    restores = 0
    effects = []
    for row in rows:
        primary = row["primary"]
        label = row["cross_order_class"]
        jump[f"{label}:{'YES' if primary['pair_jump'] else 'NO'}"] += 1
        full[f"{label}:{primary['full_status']}"] += 1
        epoch[f"{label}:{primary['epoch_status']}"] += 1
        axis[f"{label}:{primary['axis_e']}"] += 1
        if primary["restores_markov"]:
            restores += 1
        if primary.get("reconfig_effect"):
            effects.append(
                {
                    "expression": row["expression"],
                    "class": label,
                    "k": row["k"],
                    "weight": row["weight"],
                    "max_abs_delta": primary["reconfig_max_abs_delta"],
                    "argmax": primary["reconfig_argmax"],
                    "pair_jump": primary["pair_jump"],
                    "epoch_status": primary["epoch_status"],
                    "full_status": primary["full_status"],
                }
            )
    effects.sort(key=lambda item: -float(item["max_abs_delta"] or 0.0))
    grammar = build_grammar(
        4,
        int(spec["cells"][0]["K_max"]),
        spec.get("weights"),
        a_max=spec["cells"][0].get("A_max"),
        predicates=tuple(spec.get("predicates", ["pair", "triad"])),
        order=3,
    )
    structural_orbits, orbit_class, orbit_k = _structural_orbits(grammar)
    card2_labelled = 0
    labelled = grammar.stats["labelled_constraints"]
    if labelled >= 2:
        from math import comb

        card2_labelled = comb(labelled, 2)
    card2_canonical = count_canonical_simple_sets(grammar, 2)
    return {
        "analysed": len(rows),
        "by_class": dict(by_class),
        "by_k": {str(key): value for key, value in by_k.items()},
        "pair_jump": dict(jump),
        "full_event": dict(full),
        "pair_event_epoch": dict(epoch),
        "axis_e": dict(axis),
        "projection_b_restores_markov": restores,
        "reconfig_effects": len(effects),
        "reconfig_top": effects[:12],
        "grammar": {
            "structural_normal_forms": grammar.stats["structural_normal_forms"],
            "labelled_constraints": labelled,
            "structural_by_class": dict(grammar.stats["structural_by_class"]),
            "canonical_weighted_singletons": len(rows),
            "canonical_structural_orbits": structural_orbits,
            "structural_orbits_by_class": dict(orbit_class),
            "structural_orbits_by_k": {str(key): value for key, value in orbit_k.items()},
            "cardinality_2_labelled_combinations": card2_labelled,
            "cardinality_2_labelled_simple": labelled_simple_count(
                grammar.stats["structural_normal_forms"], len(grammar.weights), 2
            ),
            "cardinality_2_canonical_simple": card2_canonical,
            "cardinality_2_executed": False,
        },
        "measure": RECONFIGURATION_MEASURE,
        "horizon": RECONFIGURATION_HORIZON,
    }


def _structural_orbits(grammar) -> tuple[int, Counter, Counter]:
    weight = grammar.weights[0]
    n_pairs = sum(1 for slot in grammar.relation_slots if len(slot) == 2)
    count = 0
    by_class: Counter = Counter()
    by_k: Counter = Counter()
    for index, constraint in enumerate(grammar.labelled):
        if constraint.weight != weight:
            continue
        if not is_canonical_ids((index,), grammar.image):
            continue
        count += 1
        by_class[cross_order_class(constraint, n_pairs)] += 1
        by_k[constraint.k()] += 1
    return count, by_class, by_k


def reference_clock_table(expressions: list[str], rho_values: tuple[Fraction, ...] = (Fraction(1),)) -> list[dict]:
    """Exact clocks for the Generation 3 reference rules. Used by the report."""
    from rs_constraint_lab.constraints import parse_expression
    from rs_constraint_lab.higher_order import load_comparison_indexes
    from rs_constraint_lab.state import relation_slots

    factors = alphabet_factors("W4")
    slots = tuple(relation_slots(3, 3))
    indexes = load_comparison_indexes()
    tables = RelabelTables(3)
    rows = []
    for text in expressions:
        constraint = parse_expression(text, 3, order=3)
        by_rho = {}
        for rho in rho_values:
            kernel = build_slotted(3, (constraint,), factors, slots, rho)
            if rho == Fraction(1):
                by_rho[str(rho)] = assess_n3_clocks(kernel, indexes, tables)
            else:
                by_rho[str(rho)] = _clock_only_n3(kernel)
        rows.append(
            {
                "expression": text,
                "cross_order_class": cross_order_class(constraint, 3),
                "rho": by_rho,
            }
        )
    return rows
