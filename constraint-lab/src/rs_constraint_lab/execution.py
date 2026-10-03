"""Shard coordinator.

A generation is a list of deterministic shards. The coordinator writes
``plan.json`` and ``progress.json``. Workers write only their own shard
directory. A rerun skips a shard whose receipt matches the result hash and
whose identity matches this engine. Wall-clock fields never enter a shard id.
"""

from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import hashlib
import json
import math
import multiprocessing
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures.process import BrokenProcessPool
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from rs_constraint_lab.accounting import template_accounting
from rs_constraint_lab.analysis import (
    consider_extreme,
    execute_shard_task,
    merge_extremes,
    merge_ranges,
)
from rs_constraint_lab.constraints import Choreography, parse_expression
from rs_constraint_lab.durable import atomic_write_json, atomic_write_text, json_ready, read_json, sha256_file
from rs_constraint_lab.dynamics import RelabelTables, canonical_tokens, family_ids
from rs_constraint_lab.generation import (
    FAMILY_INDEX_COMMIT_LIMIT_BYTES,
    _family_histogram,
    _git_commit,
    _not_searched,
    _publish,
    _select_motifs,
    _set_id,
    _write_singles,
)
from rs_constraint_lab.grammar import (
    build_grammar,
    canonical_id_tuple,
    count_canonical_simple_sets,
    grammar_statistics,
    labelled_simple_count,
)
from rs_constraint_lab.kernel import build_kernel
from rs_constraint_lab.observables import equivalent_kernel, heavy_observables, light_observables
from rs_constraint_lab.spec import effective_options, spec_hash, validate_spec
from rs_constraint_lab.higher_order import (
    absorb_higher_order,
    comparison_directory,
    file_sha256,
    higher_order_science,
    orbit_catalogue,
    serialise_higher_order,
)
from rs_constraint_lab.state import canonical_states, n_states
from rs_constraint_lab.trajectory import sample_trajectory
from rs_constraint_lab.version import (
    ANALYSIS_HEAVY_EVERY,
    DEFAULT_SHARD_ITEMS,
    DEFAULT_WORKERS,
    ENGINE_VERSION,
    EXECUTION_PRINCIPLE,
    GRAMMAR_COUNT,
    GRAMMAR_EDGE,
    GRAMMAR_HYPERGRAPH,
    MAX_ATTEMPTS,
    MAX_TASKS_PER_CHILD,
    NORMALISATION_STACKED,
    NORMALISATION_STRUCTURAL,
    PROFILE_NOTE,
    SEMANTIC_VERSION,
    engine_version_for,
    hypergraph_version_for_n,
    semantic_version_for,
)
from rs_constraint_lab.weights import ENUMERATED_WEIGHTS, alphabet_factors

PLAN_SCHEMA = "rs-constraint-lab.run-plan/v1"
PROGRESS_SCHEMA = "rs-constraint-lab.progress/v1"

MEASURE_SCOPE = {
    "search": "every canonical set at the requested cardinalities; structural-simple drops stacked weights before analysis",
    "light": "every analysed set",
    "heavy": "every analysed set, including exact rational observables when the state count is at most 16",
    "exact_kernel": "full rational kernel reduced under S_N before hashing",
    "qualitative_family": "S_N-canonical support token and modal token",
    "observable_signature": "labelling-invariant scalars; not a kernel identity",
    "rise_then_release": "from the empty state when the labelled state count is at most 64",
    "sensitivity": "every analysed cardinality-1 set, on the declared geometric alphabets",
    "shards": "half-open lexicographic combination ranges, atomic result plus receipt",
    "stationary": "Fraction end to end at <=16 states; float64 beyond. Entropy is always float",
}


class IncompatibleGeneration(RuntimeError):
    """The output directory was produced under a different scientific identity."""


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _python_mm() -> str:
    return ".".join(sys.version.split()[0].split(".")[:2])


def _hypergraph_accounting(grammar) -> dict:
    stats = grammar.stats or {}
    return {
        "labelled_states": 1 << len(grammar.relation_slots),
        "relation_slots": len(grammar.relation_slots),
        "raw_structural_templates": stats.get("structural_normal_forms", 0),
        "removed_syntax_invalid": 0,
        "removed_redundant_normalisation": 0,
        "outside_k_bound": stats.get("outside_k_bound", 0),
        "outside_a_bound": stats.get("edge_outside_a", 0),
        "structural_normal_forms": stats.get("structural_normal_forms", 0),
        "weight_alphabet_size": stats.get("weight_alphabet_size", 0),
        "labelled_constraints": stats.get("labelled_constraints", 0),
        "structural_by_class": dict(stats.get("structural_by_class") or {}),
    }


def _grammar_version(predicates, semantics: str = "graph") -> str:
    if semantics == "hypergraph":
        return GRAMMAR_HYPERGRAPH
    if "count" in predicates:
        return GRAMMAR_COUNT
    return GRAMMAR_EDGE


def _normalisation(composition: str) -> str:
    if composition == "stacked-weight":
        return NORMALISATION_STACKED
    return NORMALISATION_STRUCTURAL


def _weights_of(spec: dict) -> list[str]:
    return list(spec.get("weights", ENUMERATED_WEIGHTS))


def _header(spec: dict, shard_items: int) -> dict:
    options = effective_options(spec)
    semantics = spec["semantics"]
    header = {
        "experiment_id": spec["experiment_id"],
        "generation": spec["generation"],
        "spec_hash": spec_hash(spec),
        "engine_version": engine_version_for(semantics),
        "semantic_version": semantic_version_for(semantics),
        "normalisation_version": _normalisation(options["composition"]),
        "grammar_version": _grammar_version(options["predicates"], semantics),
        "analysis": options["analysis"],
        "composition": options["composition"],
        "predicates": list(options["predicates"]),
        "shard_items": int(shard_items),
        "python": sys.version.split()[0],
        "python_mm": _python_mm(),
        "numpy": np.__version__,
        "platform": sys.platform,
        "git_commit": _git_commit(),
        "principle": EXECUTION_PRINCIPLE,
    }
    if semantics == "hypergraph":
        widest = max((int(cell["N"]) for cell in spec["cells"]), default=3)
        engine, semantic = hypergraph_version_for_n(widest)
        header["engine_version"] = engine
        header["semantic_version"] = semantic
        header["rho3"] = "1"
        if widest <= 3:
            index = comparison_directory()
            header["comparison_kernel_index_sha256"] = file_sha256(index / "kernel-ids-n3-k3.txt")
            header["comparison_qualitative_index_sha256"] = file_sha256(index / "qualitative-ids-n3-k3.txt")
            header["comparison_support_index_sha256"] = file_sha256(index / "families-n3-k3.jsonl")
        else:
            catalogue = Path(__file__).resolve().parents[2] / "catalogue" / (
                "generation-001b-structurally-normalised-kernel-ids-n4-k2.txt"
            )
            header["pairwise_n4_index_sha256"] = file_sha256(catalogue)
    return header


def _require_compatible(plan: dict, spec: dict, shard_items: int) -> None:
    current = _header(spec, shard_items)
    stored = plan["header"]
    keys = (
        "spec_hash",
        "engine_version",
        "semantic_version",
        "normalisation_version",
        "grammar_version",
        "analysis",
        "composition",
        "predicates",
        "shard_items",
        "python_mm",
        "numpy",
    )
    for key in keys:
        if stored.get(key) != current[key]:
            raise IncompatibleGeneration(
                f"refusing to resume: {key} is {stored.get(key)!r} in the plan and {current[key]!r} now. "
                "Use a new output directory. Completed shards were not modified."
            )
    for key in (
        "rho3",
        "comparison_kernel_index_sha256",
        "comparison_qualitative_index_sha256",
        "comparison_support_index_sha256",
        "pairwise_n4_index_sha256",
    ):
        if key in stored or key in current:
            if stored.get(key) != current.get(key):
                raise IncompatibleGeneration(
                    f"refusing to resume: {key} is {stored.get(key)!r} in the plan and {current.get(key)!r} now. "
                    "Use a new output directory. Completed shards were not modified."
                )


def _shard_identity(spec: dict, header: dict, cell_index: int, cell: dict, cardinality: int, start: int, end: int) -> dict:
    options = effective_options(spec)
    identity = {
        "G": options["G"],
        "H": options["H"],
        "L": options["L"],
        "O": options["O"],
        "S": options["S"],
        "a_max": cell.get("A_max"),
        "alphabet": spec["alphabet"],
        "analysis": options["analysis"],
        "cardinality": cardinality,
        "cell_index": cell_index,
        "composition": options["composition"],
        "end": end,
        "engine_version": ENGINE_VERSION,
        "grammar_version": header["grammar_version"],
        "k_max": int(cell["K_max"]),
        "n": int(cell["N"]),
        "normalisation_version": header["normalisation_version"],
        "predicates": list(options["predicates"]),
        "rise_release_horizon": int(spec.get("rise_release_horizon", 4)),
        "semantic_version": SEMANTIC_VERSION,
        "sensitivity_alphabets": list(spec.get("sensitivity_alphabets", [])),
        "spec_hash": header["spec_hash"],
        "start": start,
        "weights": _weights_of(spec),
    }
    if spec.get("semantics") == "hypergraph":
        identity["engine_version"] = header["engine_version"]
        identity["semantic_version"] = header["semantic_version"]
        identity["semantics"] = "hypergraph"
        identity["rho3"] = header["rho3"]
        for key in (
            "comparison_kernel_index_sha256",
            "comparison_qualitative_index_sha256",
            "comparison_support_index_sha256",
            "pairwise_n4_index_sha256",
        ):
            if key in header:
                identity[key] = header[key]
    if "analysis_version" in spec:
        identity["analysis_version"] = spec["analysis_version"]
    if "effect_floor" in spec:
        identity["effect_floor"] = float(spec["effect_floor"])
    return identity


def _shard_id(identity: dict) -> str:
    payload = json.dumps(identity, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]


def build_plan(spec: dict, shard_items: int | None = None) -> dict:
    validate_spec(spec)
    options = effective_options(spec)
    if options["analysis"] not in {
        ANALYSIS_HEAVY_EVERY,
        "memory-clock-reanalysis",
        "n4-singleton",
        "n4-reconfiguration-sensitivity",
        "n4-targeted-pairs",
    }:
        raise ValueError(f"analysis {options['analysis']!r} is not executable")
    if options["analysis"] in {"n4-singleton", "n4-reconfiguration-sensitivity"}:
        for cell in spec["cells"]:
            if int(cell["N"]) != 4:
                raise ValueError(f"{options['analysis']} requires N=4")
            if any(int(card) != 1 for card in cell["cardinalities"]):
                raise ValueError(f"{options['analysis']} refuses cardinality above 1")
    if options["analysis"] == "n4-targeted-pairs":
        for cell in spec["cells"]:
            if int(cell["N"]) != 4:
                raise ValueError("n4-targeted-pairs requires N=4")
            if list(cell["cardinalities"]) != [2]:
                raise ValueError("n4-targeted-pairs executes cardinality 2 only")
    if options["analysis"] == "memory-clock-reanalysis":
        for cell in spec["cells"]:
            if int(cell["N"]) != 3:
                raise ValueError("memory-clock reanalysis executes N=3")
    items = int(shard_items or DEFAULT_SHARD_ITEMS)
    if items < 1:
        raise ValueError("shard item budget must be at least 1")
    header = _header(spec, items)
    if options["analysis"] == "n4-targeted-pairs":
        from rs_constraint_lab.v05 import build_targeted_plan

        return build_targeted_plan(spec, items, header)
    weights = _weights_of(spec)
    estimates = []
    shards = []
    disk = 0
    for cell_index, cell in enumerate(spec["cells"]):
        n = int(cell["N"])
        k_max = int(cell["K_max"])
        a_max = cell.get("A_max")
        hypergraph_grammar = None
        orbits = None
        if spec["semantics"] == "hypergraph":
            hypergraph_grammar = build_grammar(
                n,
                k_max,
                weights,
                a_max=a_max,
                predicates=options["predicates"],
                order=options["O"],
            )
            stats = hypergraph_grammar.stats
            edge = _hypergraph_accounting(hypergraph_grammar)
            orbits = orbit_catalogue(n) if n == 3 else None
            labelled_state_count = edge["labelled_states"]
            canonical_state_count = orbits["orbit_count"] if orbits else None
        else:
            stats = grammar_statistics(
                n,
                k_max,
                len(weights),
                a_max=a_max,
                predicates=options["predicates"],
                weight_names=tuple(weights),
            )
            edge = template_accounting(n, k_max, len(weights), a_max=a_max)
            labelled_state_count = n_states(n)
            canonical_state_count = len(canonical_states(n))
        labelled = stats["labelled_constraints"]
        structural = stats["structural_normal_forms"]
        card_estimates = {}
        for cardinality in cell["cardinalities"]:
            combinations = math.comb(labelled, cardinality) if labelled >= cardinality else 0
            simple = labelled_simple_count(structural, len(weights), cardinality)
            exact_canonical = None
            if hypergraph_grammar is not None and 0 < combinations <= 2_000_000:
                exact_canonical = count_canonical_simple_sets(hypergraph_grammar, cardinality)
            shard_count = 0 if combinations == 0 else math.ceil(combinations / items)
            upper = simple * 400
            disk += upper
            card_estimates[str(cardinality)] = {
                "labelled_combinations": combinations,
                "labelled_simple": simple,
                "labelled_stacked": combinations - simple,
                "canonicalisation_comparisons": combinations * math.factorial(n),
                "symmetry_estimate_simple_over_factorial": simple / math.factorial(n) if n else 0,
                "canonical_simple_exact": exact_canonical,
                "shards": shard_count,
                "disk_upper_bound_bytes": upper,
            }
            start = 0
            while start < combinations:
                end = min(start + items, combinations)
                identity = _shard_identity(spec, header, cell_index, cell, cardinality, start, end)
                shards.append(
                    {
                        "shard_id": _shard_id(identity),
                        "ordinal": len(shards),
                        "cell_index": cell_index,
                        "n": n,
                        "k_max": k_max,
                        "a_max": a_max,
                        "cardinality": cardinality,
                        "start": start,
                        "end": end,
                        "identity": identity,
                    }
                )
                start = end
        estimates.append(
            {
                "N": n,
                "K_max": k_max,
                "A_max": a_max,
                "labelled_states": labelled_state_count,
                "canonical_states": canonical_state_count,
                "orbits": orbits,
                "grammar": stats,
                "edge_accounting": edge,
                "cardinalities": card_estimates,
            }
        )
    return {
        "schema": PLAN_SCHEMA,
        "header": header,
        "spec": spec,
        "estimates": {
            "cells": estimates,
            "shard_count": len(shards),
            "disk_upper_bound_bytes": disk,
            "shard_items": items,
            "profile_note": PROFILE_NOTE,
            "workers_default": DEFAULT_WORKERS,
        },
        "shards": shards,
    }


def format_plan(spec: dict, shard_items: int | None = None) -> str:
    plan = build_plan(spec, shard_items)
    header = plan["header"]
    lines = [
        f"experiment {header['experiment_id']}",
        f"spec_hash {header['spec_hash']}",
        f"engine {header['engine_version']}  semantic {header['semantic_version']}",
        f"composition {header['composition']}  normalisation {header['normalisation_version']}",
        f"predicates {', '.join(header['predicates'])}  grammar {header['grammar_version']}",
        f"analysis {header['analysis']}",
        f"shard_items {header['shard_items']}  ({header.get('principle', PROFILE_NOTE)})",
        f"profile {plan['estimates']['profile_note']}",
        f"workers default {DEFAULT_WORKERS}  (override with --workers; steady progress is preferred to filling the machine)",
        f"estimated shards {plan['estimates']['shard_count']}",
        f"disk upper bound {plan['estimates']['disk_upper_bound_bytes']} bytes "
        "(400 bytes times each labelled structurally-simple set; aggregates are smaller)",
        "combination order is lexicographic. Weights are generated innermost, so "
        "the opening range is often stacked grades rather than the slowest range. "
        "The item budget was measured on the slowest window.",
    ]
    for cell in plan["estimates"]["cells"]:
        grammar = cell["grammar"]
        edge = cell["edge_accounting"]
        lines.append(
            f"cell N={cell['N']} K<={cell['K_max']} A_max={cell['A_max']} "
            f"states {cell['labelled_states']} canonical_states {cell['canonical_states']}"
        )
        if "structural_by_class" in edge:
            classes = ", ".join(f"{name} {count}" for name, count in edge["structural_by_class"].items())
            lines.append(
                f"  relation structural {edge['structural_normal_forms']} "
                f"labelled {edge['labelled_constraints']} slots {edge['relation_slots']} "
                f"outside A {edge['outside_a_bound']}"
            )
            lines.append(f"  cross-order structural {classes}")
            if cell.get("orbits"):
                lines.append(
                    f"  orbits {cell['orbits']['orbit_count']} "
                    f"({', '.join(row['name'] + ' x' + str(row['size']) for row in cell['orbits']['orbits'])})"
                )
        else:
            lines.append(
                f"  edge structural {edge['structural_normal_forms']} edge labelled {edge['labelled_constraints']} "
                f"outside A {edge['outside_a_bound']}"
            )
        lines.append(
            f"  grammar structural {grammar['structural_normal_forms']} "
            f"count structural {grammar['count_structural']} "
            f"count tautology {grammar['count_tautology']} "
            f"count unsatisfiable {grammar['count_unsatisfiable']} "
            f"labelled {grammar['labelled_constraints']}"
        )
        for cardinality, info in cell["cardinalities"].items():
            lines.append(
                f"  cardinality {cardinality}: combinations {info['labelled_combinations']} "
                f"labelled-simple {info['labelled_simple']} labelled-stacked {info['labelled_stacked']} "
                f"symmetry-estimate {info['symmetry_estimate_simple_over_factorial']:.1f} "
                f"canonical-simple-exact {info.get('canonical_simple_exact')} "
                f"canonicalisation-comparisons {info['canonicalisation_comparisons']} "
                f"shards {info['shards']}"
            )
    return "\n".join(lines)


def _initial_progress(plan: dict) -> dict:
    shards = {}
    for shard in plan["shards"]:
        shards[shard["shard_id"]] = {"status": "pending", "attempts": 0, "ordinal": shard["ordinal"]}
    progress = {
        "schema": PROGRESS_SCHEMA,
        "experiment_id": plan["header"]["experiment_id"],
        "generation": plan["header"]["generation"],
        "spec_hash": plan["header"]["spec_hash"],
        "engine_version": plan["header"]["engine_version"],
        "semantic_version": plan["header"]["semantic_version"],
        "total_shards": len(plan["shards"]),
        "pending": len(plan["shards"]),
        "running": 0,
        "completed": 0,
        "failed": 0,
        "quarantined": 0,
        "last_completed_shard": None,
        "start_time": _now(),
        "last_heartbeat": _now(),
        "status": "COMPLETE" if not plan["shards"] else "IN_PROGRESS",
        "workers_last": None,
        "worker_history": [],
        "shards": shards,
    }
    return progress


def _recount(progress: dict) -> None:
    counts = {"pending": 0, "running": 0, "completed": 0, "failed": 0, "quarantined": 0}
    for state in progress["shards"].values():
        counts[state["status"]] = counts.get(state["status"], 0) + 1
    progress.update(counts)
    progress["status"] = _status_name(progress)


def _status_name(progress: dict) -> str:
    if progress["total_shards"] == 0:
        return "COMPLETE"
    if (
        progress["completed"] == progress["total_shards"]
        and progress["pending"] == 0
        and progress["running"] == 0
        and progress["failed"] == 0
        and progress["quarantined"] == 0
    ):
        return "COMPLETE"
    if progress["pending"] or progress["running"] or progress["failed"]:
        return "IN_PROGRESS"
    if progress["completed"] == 0:
        return "FAILED"
    return "PARTIAL"


def _receipt_valid(out_dir: Path, shard: dict) -> bool:
    shard_dir = out_dir / "shards" / shard["shard_id"]
    receipt_path = shard_dir / "receipt.json"
    result_path = shard_dir / "result.json"
    if not receipt_path.is_file() or not result_path.is_file():
        return False
    try:
        receipt = read_json(receipt_path)
    except json.JSONDecodeError:
        return False
    if receipt.get("status") != "completed":
        return False
    if receipt.get("identity") != shard["identity"]:
        return False
    if receipt.get("engine_version") != shard["identity"]["engine_version"]:
        return False
    if receipt.get("semantic_version") != shard["identity"]["semantic_version"]:
        return False
    if receipt.get("result_sha256") != sha256_file(result_path):
        return False
    return True


def _reconcile(out_dir: Path, plan: dict) -> dict:
    progress_path = out_dir / "progress.json"
    if progress_path.exists():
        progress = read_json(progress_path)
    else:
        progress = _initial_progress(plan)
    known = {shard["shard_id"] for shard in plan["shards"]}
    if set(progress["shards"]) != known:
        raise IncompatibleGeneration("progress shard ids do not match the plan. The directory was not modified.")
    for shard in plan["shards"]:
        state = progress["shards"][shard["shard_id"]]
        if _receipt_valid(out_dir, shard):
            state["status"] = "completed"
            continue
        if state["status"] == "completed":
            state["status"] = "pending"
            state["attempts"] = 0
        elif state["status"] == "running":
            state["status"] = "pending"
        elif state["status"] == "failed" and state["attempts"] >= MAX_ATTEMPTS:
            state["status"] = "quarantined"
    _recount(progress)
    progress["last_heartbeat"] = _now()
    atomic_write_json(progress_path, progress)
    return progress


def _save_progress(out_dir: Path, progress: dict) -> None:
    progress["last_heartbeat"] = _now()
    _recount(progress)
    atomic_write_json(out_dir / "progress.json", progress)


def _eligible(state: dict) -> bool:
    return state["status"] in {"pending", "failed"} and state["attempts"] < MAX_ATTEMPTS


def _task(plan: dict, shard: dict, attempt: int, out_dir: Path) -> dict:
    return {
        "ordinal": shard["ordinal"],
        "shard_id": shard["shard_id"],
        "identity": shard["identity"],
        "spec": plan["spec"],
        "start": shard["start"],
        "end": shard["end"],
        "n": shard["n"],
        "k_max": shard["k_max"],
        "a_max": shard["a_max"],
        "cardinality": shard["cardinality"],
        "shard_dir": str(out_dir / "shards" / shard["shard_id"]),
        "attempt": attempt,
    }


def _write_failure(out_dir: Path, shard: dict, attempt: int, payload: dict) -> None:
    body = {
        "shard_id": shard["shard_id"],
        "input_identity": shard["identity"],
        "attempt": attempt,
        "exception_type": payload.get("exception_type", "WorkerCrashed"),
        "message": payload.get("message", "worker exited without a receipt"),
        "traceback": payload.get("traceback", ""),
        "timestamp": _now(),
        "engine_version": shard["identity"]["engine_version"],
        "semantic_version": shard["identity"]["semantic_version"],
        "spec_hash": shard["identity"]["spec_hash"],
    }
    atomic_write_json(out_dir / "shards" / shard["shard_id"] / "failure.json", body)


def _execute(out_dir: Path, plan: dict, progress: dict, workers: int, max_shards: int | None) -> None:
    if workers < 1:
        raise ValueError("workers must be at least 1")
    progress["workers_last"] = workers
    progress["worker_history"].append({"workers": workers, "at": _now()})
    _save_progress(out_dir, progress)
    if not any(_eligible(progress["shards"][shard["shard_id"]]) for shard in plan["shards"]):
        return
    ctx = multiprocessing.get_context("spawn")
    pool = None
    in_flight: dict = {}
    completed_now = 0
    by_id = {shard["shard_id"]: shard for shard in plan["shards"]}

    def ensure_pool():
        nonlocal pool
        if pool is None:
            pool = ProcessPoolExecutor(
                max_workers=workers,
                mp_context=ctx,
                max_tasks_per_child=MAX_TASKS_PER_CHILD,
            )
        return pool

    def mark_failure(shard_id: str, payload: dict) -> None:
        shard = by_id[shard_id]
        state = progress["shards"][shard_id]
        _write_failure(out_dir, shard, state["attempts"], payload)
        if state["attempts"] >= MAX_ATTEMPTS:
            state["status"] = "quarantined"
        else:
            state["status"] = "failed"

    try:
        while True:
            if max_shards is not None and completed_now >= max_shards:
                break
            running_ids = set(in_flight.values())
            eligible = [
                shard
                for shard in plan["shards"]
                if shard["shard_id"] not in running_ids and _eligible(progress["shards"][shard["shard_id"]])
            ]
            while eligible and len(in_flight) < workers:
                if max_shards is not None and completed_now + len(in_flight) >= max_shards:
                    break
                shard = eligible.pop(0)
                state = progress["shards"][shard["shard_id"]]
                state["attempts"] += 1
                state["status"] = "running"
                _save_progress(out_dir, progress)
                future = ensure_pool().submit(execute_shard_task, _task(plan, shard, state["attempts"], out_dir))
                in_flight[future] = shard["shard_id"]
            if not in_flight:
                break
            done = None
            waited = 0.0
            while done is None:
                for future in list(in_flight):
                    if future.done():
                        done = future
                        break
                if done is None:
                    time.sleep(0.05)
                    waited += 0.05
                    if waited >= 1.0:
                        progress["last_heartbeat"] = _now()
                        atomic_write_json(out_dir / "progress.json", progress)
                        waited = 0.0
            shard_id = in_flight.pop(done)
            try:
                payload = done.result()
            except BrokenProcessPool as exc:
                payload = {
                    "ok": False,
                    "exception_type": "BrokenProcessPool",
                    "message": str(exc),
                    "traceback": traceback.format_exc(),
                }
                mark_failure(shard_id, payload)
                for future, other_id in list(in_flight.items()):
                    mark_failure(
                        other_id,
                        {"exception_type": "BrokenProcessPool", "message": "pool restarted after a worker crash", "traceback": ""},
                    )
                in_flight.clear()
                if pool is not None:
                    pool.shutdown(wait=False, cancel_futures=True)
                    pool = None
                _save_progress(out_dir, progress)
                continue
            if payload.get("ok") and _receipt_valid(out_dir, by_id[shard_id]):
                progress["shards"][shard_id]["status"] = "completed"
                progress["last_completed_shard"] = shard_id
                completed_now += 1
                print(
                    f"[shard] completed {progress['completed'] + 1}/{progress['total_shards']} {shard_id}",
                    file=sys.stderr,
                )
            else:
                mark_failure(shard_id, payload if isinstance(payload, dict) else {"message": repr(payload)})
                print(
                    f"[shard] {progress['shards'][shard_id]['status']} {shard_id} "
                    f"attempt {progress['shards'][shard_id]['attempts']}",
                    file=sys.stderr,
                )
            _save_progress(out_dir, progress)
    finally:
        if pool is not None:
            pool.shutdown(wait=True, cancel_futures=False)


def _load_id_set(directory: Path, prefix: str, n: int) -> set[str]:
    found: set[str] = set()
    for path in sorted(directory.glob(f"{prefix}-n{n}-k*.txt")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line:
                found.add(line)
    return found


def _require_comparison_index(directory: Path, spec: dict) -> None:
    if not directory.is_dir():
        raise IncompatibleGeneration(f"comparison index {directory} does not exist")
    for cell in spec["cells"]:
        found = list(directory.glob(f"kernel-ids-n{cell['N']}-k*.txt"))
        if not found:
            raise IncompatibleGeneration(
                f"comparison index {directory} has no kernel-ids for N={cell['N']}. "
                "Generation 2 was not started."
            )


def _fingerprint(out_dir: Path, plan: dict) -> str:
    parts = []
    for shard in plan["shards"]:
        receipt_path = out_dir / "shards" / shard["shard_id"] / "receipt.json"
        if not receipt_path.is_file():
            return ""
        try:
            receipt = read_json(receipt_path)
        except json.JSONDecodeError:
            return ""
        parts.append(receipt.get("result_sha256", ""))
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()


def _absorb_family(dest: dict, src: dict) -> None:
    key = src["qualitative_family"]
    incoming = dict(src)
    incoming["kernel_ids"] = set(src["kernel_ids"])
    incoming["observable_ids"] = set(src["observable_ids"])
    if key not in dest:
        dest[key] = incoming
        return
    family = dest[key]
    if family["support_family"] != incoming["support_family"] or family["modal_family"] != incoming["modal_family"]:
        raise RuntimeError(f"qualitative family {key} collided across different canonical tokens")
    family["count"] += incoming["count"]
    family["equivalent_members"] += incoming["equivalent_members"]
    family["count_literal_members"] += incoming["count_literal_members"]
    family["kernel_ids"].update(incoming["kernel_ids"])
    family["observable_ids"].update(incoming["observable_ids"])
    family["ranges"] = merge_ranges(family["ranges"], incoming["ranges"])
    if (incoming["cardinality"], tuple(incoming["expressions"])) < (family["cardinality"], tuple(family["expressions"])):
        family["cardinality"] = incoming["cardinality"]
        family["expressions"] = list(incoming["expressions"])
        family["k_max"] = incoming["k_max"]
        family["arity"] = incoming["arity"]
        family["observed"] = incoming["observed"]


def _absorb_cancellations(dest: dict, src: dict) -> None:
    for name in ("genuine_global", "local", "inherited_baseline"):
        dest[name] = dest.get(name, 0) + src.get(name, 0)
        bucket = f"{name}_examples"
        rows = list(dest.get(bucket, []))
        for row in src.get(bucket, []):
            if row not in rows:
                rows.append(list(row))
        rows.sort()
        dest[bucket] = rows[:8]


def _range_float(ranges: dict, name: str, end: str):
    slot = ranges.get(name) or {}
    return slot.get(end)


def _tags(family: dict, screens: dict) -> list[str]:
    tags = []
    baseline = family["equivalent_members"] == family["count"] and family["support_matches_baseline"]
    if baseline:
        tags.append("baseline-equivalent")
    if not family["support_matches_baseline"]:
        tags.append("structural")
    shift_bar = float(screens.get("max_abs_dissolve_shift_notable", 0.1))
    close_bar = float(screens.get("closing_bias_abs_notable", 0.1))
    rise_bar = float(screens.get("rise_release_excess_notable", 0.05))
    screened = False
    shift_max = _range_float(family["ranges"], "max_abs_dissolve_shift", "max")
    if shift_max is not None and shift_max >= shift_bar:
        screened = True
    for end in ("min", "max"):
        closing = _range_float(family["ranges"], "closing_bias", end)
        if closing is not None and abs(closing) >= close_bar:
            screened = True
    for end in ("min", "max"):
        excess = _range_float(family["ranges"], "rise_then_release_excess", end)
        if excess is not None and abs(excess) >= rise_bar:
            screened = True
    if screened and not baseline:
        tags.append("screened")
    if "structural" not in tags and "baseline-equivalent" not in tags:
        tags.append("measure")
    return tags


def _excess_endpoint(ranges: dict):
    left = _range_float(ranges, "rise_then_release_excess", "min")
    right = _range_float(ranges, "rise_then_release_excess", "max")
    if left is None:
        return right
    if right is None:
        return left
    return right if abs(right) >= abs(left) else left


def _family_row(spec: dict, family: dict, screens: dict) -> dict:
    expressions = list(family["expressions"])
    return {
        "motif_id": family["qualitative_family"],
        "tags": _tags(family, screens),
        "count": family["count"],
        "expressions": expressions,
        "coordinate": {
            "N": family.get("n"),
            "A": family["arity"],
            "O": spec.get("O", 2),
            "G": spec.get("G", 0),
            "S": spec.get("S", 0),
            "H": spec.get("H", 0),
            "K": family["k_max"],
            "L": spec.get("L", 0),
            "semantics": spec["semantics"],
            "alphabet": spec["alphabet"],
            "cardinality": family["cardinality"],
        },
        "observed": family["observed"],
        "support_matches_baseline": family["support_matches_baseline"],
        "support_family": family["support_family"],
        "modal_family": family["modal_family"],
        "n_deadlock": family["n_deadlock"],
        "n_recurrent": family["n_recurrent"],
        "periods": family["periods"],
        "shift_min": _range_float(family["ranges"], "max_abs_dissolve_shift", "min"),
        "shift_max": _range_float(family["ranges"], "max_abs_dissolve_shift", "max"),
        "closing_min": _range_float(family["ranges"], "closing_bias", "min"),
        "closing_max": _range_float(family["ranges"], "closing_bias", "max"),
        "mean_edge_density": _range_float(family["ranges"], "mean_edge_density", "max"),
        "entropy_rate_bits": _range_float(family["ranges"], "entropy_rate_bits", "max"),
        "tv_from_uniform": _range_float(family["ranges"], "tv_from_uniform", "max"),
        "halt_mass": _range_float(family["ranges"], "halt_mass", "max"),
        "rise_then_release": _range_float(family["ranges"], "rise_then_release", "max"),
        "rise_then_release_excess": _excess_endpoint(family["ranges"]),
        "reversibility_defect": _range_float(family["ranges"], "reversibility_defect", "max"),
        "triangle_mass": _range_float(family["ranges"], "triangle_mass", "max"),
        "disjoint_pair_mass": _range_float(family["ranges"], "disjoint_pair_mass", "max"),
        "stationary_arithmetic": "rational" if int(family.get("n") or 0) <= 3 else "float64",
        "stationary_residual": 0.0 if int(family.get("n") or 0) <= 3 else None,
        "equivalent_to_baseline": family["equivalent_members"] == family["count"] and family["support_matches_baseline"],
        "exact_kernel_count": len(family["kernel_ids"]),
        "observable_signature_count": len(family["observable_ids"]),
        "equivalent_members": family["equivalent_members"],
        "count_literal_members": family["count_literal_members"],
        "ranges": family["ranges"],
        "within_family": {
            "exact_kernel_count": len(family["kernel_ids"]),
            "observable_signature_count": len(family["observable_ids"]),
            "ranges": family["ranges"],
            "equivalent_members": family["equivalent_members"],
            "count_literal_members": family["count_literal_members"],
        },
    }


def _write_lines(path: Path, values: list[str]) -> str:
    atomic_write_text(path, "".join(f"{value}\n" for value in values))
    return sha256_file(path)


def _classify_territory(motifs: list[dict], index_dir: Path, n: int) -> dict:
    kernels = _load_id_set(index_dir, "kernel-ids", n)
    qualitative = _load_id_set(index_dir, "qualitative-ids", n)
    observable = _load_id_set(index_dir, "observable-ids", n)
    classes = {
        "threshold_motifs": len(motifs),
        "syntactically_new_dynamically_equivalent": 0,
        "new_kernel_same_qualitative_family": 0,
        "qualitatively_new": 0,
        "exact_kernel_new": 0,
        "observable_signature_new": 0,
        "kernel_in_index_but_qualitative_missing": 0,
    }
    examples = {name: [] for name in (
        "syntactically_new_dynamically_equivalent",
        "new_kernel_same_qualitative_family",
        "qualitatively_new",
        "exact_kernel_new",
        "observable_signature_new",
    )}
    for motif in motifs:
        in_kernel = motif["kernel"] in kernels
        in_qual = motif["qualitative"] in qualitative
        in_obs = motif["observable"] in observable
        if in_kernel and not in_qual:
            classes["kernel_in_index_but_qualitative_missing"] += 1
        if in_kernel:
            classes["syntactically_new_dynamically_equivalent"] += 1
            _keep(examples["syntactically_new_dynamically_equivalent"], motif["expressions"])
        else:
            classes["exact_kernel_new"] += 1
            _keep(examples["exact_kernel_new"], motif["expressions"])
            if in_qual:
                classes["new_kernel_same_qualitative_family"] += 1
                _keep(examples["new_kernel_same_qualitative_family"], motif["expressions"])
        if not in_qual:
            classes["qualitatively_new"] += 1
            _keep(examples["qualitatively_new"], motif["expressions"])
        if not in_obs:
            classes["observable_signature_new"] += 1
            _keep(examples["observable_signature_new"], motif["expressions"])
    classes["examples"] = examples
    classes["post_release_new_edge"] = sum(1 for motif in motifs if motif.get("post_release_new_edge"))
    return classes


def _keep(bucket: list, expressions, limit: int = 8) -> None:
    row = list(expressions)
    if row in bucket:
        return
    bucket.append(row)
    bucket.sort()
    del bucket[limit:]


def _kernel_args(grammar) -> dict:
    if grammar.relation_slots:
        return {
            "relation_slots": grammar.relation_slots,
            "baseline_weights": grammar.baseline_weights,
        }
    return {}


def _slim_higher_order(box: dict, science: dict) -> dict:
    serial = serialise_higher_order(box)
    for kind in ("kernel_ids_by_class", "support_ids_by_class", "qualitative_ids_by_class"):
        serial[kind] = {name: len(values) for name, values in serial.get(kind, {}).items()}
    serial["qualitative_family_count"] = len(serial.get("qualitative_ids") or [])
    serial.pop("qualitative_ids", None)
    for row in serial.get("sensitivity", {}).values():
        row["qualitative_family_count"] = len(row.get("qualitative_ids") or [])
        row.pop("qualitative_ids", None)
    serial["id_digest"] = {
        "qualitative_ids_sha256": science["qualitative_ids_sha256"],
        "kernel_ids_sha256": science["kernel_ids_sha256"],
    }
    return serial


def _reference_block(spec: dict, grammar, factors, tables, horizon: int) -> list[dict]:
    blocks = []
    alphabet = spec["alphabet"]
    for text in spec.get("reference_expressions", []):
        slot_list = grammar.slot_list()
        try:
            constraint = parse_expression(text, grammar.n, order=grammar.order)
        except ValueError as exc:
            blocks.append({"expression": text, "in_grammar": False, "reason": str(exc)})
            continue
        if constraint.k() > grammar.k_max or constraint.weight not in grammar.weights:
            blocks.append({"expression": text, "in_grammar": False, "reason": "outside this cell's K bound or weight list"})
            continue
        if grammar.a_max is not None and constraint.arity(slot_list) > grammar.a_max:
            blocks.append({"expression": text, "in_grammar": False, "reason": "arity exceeds A_max"})
            continue
        found = next((i for i, item in enumerate(grammar.labelled) if item.key() == constraint.key()), None)
        if found is None:
            blocks.append({"expression": text, "in_grammar": False, "reason": "not in the normal-form grammar"})
            continue
        canon = canonical_id_tuple((found,), grammar.image)
        canonical_expression = grammar.expression(canon[0])
        constraints = (grammar.labelled[canon[0]],)
        kernel_args = _kernel_args(grammar)
        kernel = build_kernel(grammar.n, Choreography(0, 0, constraints), factors, **kernel_args)
        baseline = build_kernel(grammar.n, Choreography(0, 0, ()), factors, **kernel_args)
        light = light_observables(kernel, baseline)
        light.pop("modes", None)
        light["equivalent_to_baseline"] = equivalent_kernel(kernel, baseline)
        heavy = heavy_observables(kernel, horizon, 0)
        ids = family_ids(grammar.n, canonical_tokens(kernel, tables))
        expressions = [canonical_expression]
        blocks.append(
            {
                "expression": text,
                "in_grammar": True,
                "canonical_expression": canonical_expression,
                "same_labelling": text == canonical_expression,
                "single": {
                    "set_id": _set_id(alphabet, expressions),
                    "family_id": ids["qualitative_family"],
                    "modal_family": ids["modal_family"],
                    "exact_kernel_family": ids["exact_kernel_family"],
                    "expressions": expressions,
                    "mean_edge_density_exact": heavy.get("mean_edge_density_exact"),
                    "triangle_mass_exact": heavy.get("triangle_mass_exact"),
                    "closing_bias_exact": light.get("closing_bias_exact"),
                    "max_abs_dissolve_shift_exact": light.get("max_abs_dissolve_shift_exact"),
                    "equivalent_to_baseline": light["equivalent_to_baseline"],
                },
            }
        )
    return blocks


def _write_exemplars(spec, grammar, factors, digest, families, cancellations, out_dir: Path) -> list[dict]:
    written = []
    edge_list = grammar.slot_list()
    seeds = list(spec.get("trajectory", {}).get("seeds", [0]))
    kernel_args = _kernel_args(grammar)
    recorded_engine = engine_version_for(spec["semantics"]) if spec["semantics"] == "hypergraph" else None
    horizon = int(spec.get("trajectory", {}).get("horizon", 32))
    targets = [("baseline", [], [0])]
    for reference in spec.get("reference_expressions", [])[:6]:
        try:
            constraint = parse_expression(reference, grammar.n, order=grammar.order)
        except ValueError:
            continue
        if any(item.key() == constraint.key() for item in grammar.labelled):
            targets.append(("reference", [constraint.expression(edge_list)], seeds if grammar.n == 3 else [0]))
    ranked = sorted(families.values(), key=lambda family: (family["cardinality"], tuple(family["expressions"])))
    added = 0
    for family in ranked:
        if family["equivalent_members"] == family["count"] and family["support_matches_baseline"]:
            continue
        targets.append(("family", list(family["expressions"]), [0]))
        added += 1
        if added >= 4:
            break
    for kind, label in (("genuine_global", "cancellation"), ("local", "cancellation")):
        examples = cancellations.get(f"{kind}_examples") or []
        if examples:
            targets.append((label, list(examples[0]), [0]))
    for family in ranked:
        if family.get("count_literal_members"):
            targets.append(("threshold", list(family["expressions"]), [0]))
            break
    complete = (1 << grammar.n_edges) - 1 if False else (1 << len(edge_list)) - 1
    for label, expressions, seed_list in targets:
        constraints = tuple(parse_expression(text, grammar.n, order=grammar.order) for text in expressions)
        kernel = build_kernel(grammar.n, Choreography(0, 0, constraints), factors, **kernel_args)
        set_id = _set_id(spec["alphabet"], expressions) if expressions else _set_id(spec["alphabet"], ["baseline"])
        for seed in seed_list:
            for initial, initial_name in ((0, "empty"), (complete, "complete")):
                record = sample_trajectory(
                    kernel,
                    constraints,
                    factors,
                    edge_list,
                    initial,
                    seed,
                    horizon,
                    digest,
                    set_id,
                    engine_version=recorded_engine,
                )
                record["n"] = grammar.n
                record["alphabet"] = spec["alphabet"]
                record["expressions"] = list(expressions)
                record["label"] = label
                record["initial_name"] = initial_name
                path = out_dir / "exemplars" / f"{record['run_id']}.json"
                atomic_write_json(path, record)
                written.append(
                    {
                        "run_id": record["run_id"],
                        "label": label,
                        "initial": initial_name,
                        "seed": seed,
                        "expressions": expressions,
                    }
                )
    return written


def _publish_run(summary: dict, spec: dict, publish: Path, out_dir: Path) -> None:
    """Copy a finished summary. The caller must already have set the wall clock."""
    if summary.get("status") != "COMPLETE":
        return
    _publish(summary, spec, Path(publish), out_dir)
    catalogue = Path(publish) / "catalogue"
    catalogue.mkdir(parents=True, exist_ok=True)
    for path in out_dir.glob("kernel-ids-*.txt"):
        if path.stat().st_size <= FAMILY_INDEX_COMMIT_LIMIT_BYTES:
            target = catalogue / f"{spec['experiment_id']}-{path.name}"
            target.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")


def merge_directory(out_dir: Path, publish: Path | None = None, compare_to: Path | None = None) -> dict:
    out_dir = Path(out_dir)
    plan = read_json(out_dir / "plan.json")
    progress = _reconcile(out_dir, plan)
    spec = plan["spec"]
    fingerprint = _fingerprint(out_dir, plan)
    existing_path = out_dir / "summary.json"
    if existing_path.exists() and fingerprint:
        existing = read_json(existing_path)
        if (
            existing.get("receipt_fingerprint") == fingerprint
            and existing.get("status") == "COMPLETE"
            and progress["status"] == "COMPLETE"
            and (compare_to is None or existing.get("territory") is not None)
        ):
            if publish is not None:
                _publish_run(existing, spec, publish, out_dir)
            return existing
    if spec.get("analysis") in {"memory-clock-reanalysis", "n4-singleton"}:
        from rs_constraint_lab.census import merge_census

        return merge_census(out_dir, plan, publish)
    if spec.get("analysis") in {"n4-reconfiguration-sensitivity", "n4-targeted-pairs"}:
        from rs_constraint_lab.v05 import merge_v05

        return merge_v05(out_dir, plan, publish)
    options = effective_options(spec)
    screens = spec.get("predeclared_screens", {})
    horizon = int(spec.get("rise_release_horizon", 4))
    weights = _weights_of(spec)
    factors = alphabet_factors(spec["alphabet"])
    by_cell: dict[int, dict] = {}
    for shard in plan["shards"]:
        cell_index = shard["cell_index"]
        bucket = by_cell.setdefault(
            cell_index,
            {
                "families": {},
                "singles": [],
                "extremes": {},
                "cancellations": {},
                "sensitivity": {"checks": 0, "modal_unchanged": 0, "support_unchanged": 0},
                "threshold_motifs": [],
                "counts": {},
                "work_seconds": 0.0,
                "higher_order": {},
            },
        )
        card = str(shard["cardinality"])
        card_counts = bucket["counts"].setdefault(
            card,
            {
                "scanned": 0,
                "symmetry_removed": 0,
                "stacked_canonical": 0,
                "stacked_analysed": 0,
                "analysed": 0,
                "canonical_including_stacked": 0,
                "canonical_simple": 0,
            },
        )
        state = progress["shards"][shard["shard_id"]]
        if state["status"] != "completed":
            continue
        result = read_json(out_dir / "shards" / shard["shard_id"] / "result.json")
        for name, value in result["counts"].items():
            card_counts[name] = card_counts.get(name, 0) + value
        for family in result["families"].values():
            family["n"] = shard["n"]
            _absorb_family(bucket["families"], family)
        bucket["singles"].extend(result["singles"])
        bucket["extremes"] = merge_extremes(bucket["extremes"], result["extremes"])
        _absorb_cancellations(bucket["cancellations"], result["cancellations"])
        for name in ("checks", "modal_unchanged", "support_unchanged"):
            bucket["sensitivity"][name] += result["sensitivity"][name]
        bucket["threshold_motifs"].extend(result["threshold_motifs"])
        if result.get("higher_order"):
            absorb_higher_order(bucket["higher_order"], result["higher_order"])
        receipt = read_json(out_dir / "shards" / shard["shard_id"] / "receipt.json")
        bucket["work_seconds"] += float(receipt.get("elapsed_seconds") or 0.0)

    cells = []
    territory_cells = []
    for cell_index, cell in enumerate(spec["cells"]):
        bucket = by_cell.get(cell_index) or {
            "families": {},
            "singles": [],
            "extremes": {},
            "cancellations": {},
            "sensitivity": {"checks": 0, "modal_unchanged": 0, "support_unchanged": 0},
            "threshold_motifs": [],
            "counts": {},
            "work_seconds": 0.0,
            "higher_order": {},
        }
        n = int(cell["N"])
        k_max = int(cell["K_max"])
        grammar_order = 3 if spec["semantics"] == "hypergraph" else 2
        grammar = build_grammar(
            n,
            k_max,
            weights,
            a_max=cell.get("A_max"),
            predicates=tuple(options["predicates"]),
            order=grammar_order,
        )
        tables = RelabelTables(n, grammar.relation_slots or None)
        kernel_args = _kernel_args(grammar)
        baseline_kernel = build_kernel(n, Choreography(0, 0, ()), factors, **kernel_args)
        baseline_light = light_observables(baseline_kernel, baseline_kernel)
        baseline_light.pop("modes", None)
        baseline_heavy = heavy_observables(baseline_kernel, horizon, 0)
        rows = []
        for family in bucket["families"].values():
            family["n"] = n
            rows.append(_family_row(spec, family, screens))
        rows.sort(key=lambda row: row["motif_id"])
        family_path = out_dir / f"families-n{n}-k{k_max}.jsonl"
        atomic_write_text(
            family_path,
            "".join(json.dumps(json_ready(row), sort_keys=True) + "\n" for row in rows),
        )
        singles = sorted(bucket["singles"], key=lambda row: row["set_id"])
        singles_path = out_dir / f"singles-n{n}-k{k_max}.csv"
        _write_singles(singles_path, singles)
        kernel_ids = sorted({kernel_id for family in bucket["families"].values() for kernel_id in family["kernel_ids"]})
        qualitative_ids = sorted(bucket["families"])
        observable_ids = sorted({obs for family in bucket["families"].values() for obs in family["observable_ids"]})
        kernel_sha = _write_lines(out_dir / f"kernel-ids-n{n}-k{k_max}.txt", kernel_ids)
        qualitative_sha = _write_lines(out_dir / f"qualitative-ids-n{n}-k{k_max}.txt", qualitative_ids)
        observable_sha = _write_lines(out_dir / f"observable-ids-n{n}-k{k_max}.txt", observable_ids)
        motifs = _select_motifs(rows)
        for motif in motifs:
            atomic_write_json(out_dir / "motifs" / f"n{n}-k{k_max}-{motif['motif_id'][:16]}.json", motif)
        estimate = plan["estimates"]["cells"][cell_index]
        cardinalities = {}
        for cardinality, info in estimate["cardinalities"].items():
            counts = bucket["counts"].get(
                cardinality,
                {
                    "scanned": 0,
                    "symmetry_removed": 0,
                    "stacked_canonical": 0,
                    "analysed": 0,
                    "canonical_including_stacked": 0,
                    "canonical_simple": 0,
                },
            )
            cardinalities[cardinality] = {
                "labelled_combinations": info["labelled_combinations"],
                "labelled_simple": info["labelled_simple"],
                "labelled_stacked": info["labelled_stacked"],
                "canonical": counts.get("canonical_simple", 0),
                "canonical_including_stacked": counts.get("canonical_including_stacked", 0),
                "stacked_canonical": counts.get("stacked_canonical", 0),
                "removed_by_symmetry": counts.get("symmetry_removed", 0),
                "analysed": counts.get("analysed", 0),
            }
        references = _reference_block(spec, grammar, factors, tables, horizon)
        exemplars = []
        if progress["status"] == "COMPLETE":
            exemplars = _write_exemplars(
                spec, grammar, factors, plan["header"]["spec_hash"], bucket["families"], bucket["cancellations"], out_dir
            )
        structural = sum(1 for row in rows if "structural" in row["tags"])
        screened = sum(1 for row in rows if "screened" in row["tags"])
        nulls = sum(1 for row in rows if "baseline-equivalent" in row["tags"])
        cell_summary = {
            "coordinate": {
                "N": n,
                "A_max": cell.get("A_max"),
                "O": options["O"],
                "G": options["G"],
                "S": options["S"],
                "H": options["H"],
                "K_max": k_max,
                "L": options["L"],
                "semantics": spec["semantics"],
                "alphabet": spec["alphabet"],
                "composition": options["composition"],
                "predicates": list(options["predicates"]),
            },
            "runtime_seconds": bucket["work_seconds"],
            "accounting": {"edge": estimate["edge_accounting"], "grammar": estimate["grammar"]},
            "canonical_states": estimate["canonical_states"],
            "relation_slots": estimate["edge_accounting"]["relation_slots"],
            "labelled_states": estimate["labelled_states"],
            "cardinalities": cardinalities,
            "baseline": {"light": baseline_light, "heavy": baseline_heavy},
            "measure_scope": MEASURE_SCOPE,
            "families": len(rows),
            "family_histogram": _family_histogram(rows),
            "family_index_bytes": family_path.stat().st_size,
            "family_index_sha256": sha256_file(family_path),
            "singles_sha256": sha256_file(singles_path),
            "kernel_index_sha256": kernel_sha,
            "kernel_index_count": len(kernel_ids),
            "qualitative_index_sha256": qualitative_sha,
            "observable_index_sha256": observable_sha,
            "observable_signature_count": len(observable_ids),
            "family_index_commit_limit_bytes": FAMILY_INDEX_COMMIT_LIMIT_BYTES,
            "motif_ids": [motif["motif_id"] for motif in motifs],
            "structural_families": structural,
            "screened_families": screened,
            "baseline_equivalent_families": nulls,
            "sensitivity": {
                "alphabets": list(spec.get("sensitivity_alphabets", [])),
                "checks": bucket["sensitivity"]["checks"],
                "modal_unchanged": bucket["sensitivity"]["modal_unchanged"],
                "support_unchanged": bucket["sensitivity"]["support_unchanged"],
            },
            "references": references,
            "exemplars": exemplars,
            "cancellations": bucket["cancellations"],
            "extremes": bucket["extremes"],
            "not_searched": _not_searched(n, k_max, list(cell["cardinalities"]), estimate["edge_accounting"]),
        }
        if bucket.get("higher_order") and bucket["higher_order"].get("sets_by_class"):
            cell_summary["higher_order_science"] = higher_order_science(bucket["higher_order"])
            cell_summary["higher_order"] = _slim_higher_order(bucket["higher_order"], cell_summary["higher_order_science"])
        if compare_to is not None:
            cell_summary["territory"] = _classify_territory(bucket["threshold_motifs"], Path(compare_to), n)
            territory_cells.append({"N": n, "K_max": k_max, "territory": cell_summary["territory"]})
        cells.append(cell_summary)
        if progress["status"] == "COMPLETE":
            for cardinality, counts in cardinalities.items():
                if counts["analysed"] + counts["stacked_canonical"] + counts["removed_by_symmetry"] != counts["labelled_combinations"]:
                    raise RuntimeError(
                        f"coverage gap at N={n} cardinality {cardinality}: "
                        f"scanned pieces do not sum to {counts['labelled_combinations']}"
                    )
                planned = estimate["cardinalities"][cardinality].get("canonical_simple_exact")
                if planned is not None and counts["canonical"] != planned:
                    raise RuntimeError(
                        f"canonical coverage at N={n} cardinality {cardinality} is "
                        f"{counts['canonical']} and the exact plan count is {planned}"
                    )
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
        "composition": options["composition"],
        "predicates": list(options["predicates"]),
        "normalisation_version": plan["header"]["normalisation_version"],
        "grammar_version": plan["header"]["grammar_version"],
        "runtime_seconds": 0.0,
        "shard_work_seconds": sum(cell["runtime_seconds"] for cell in cells),
        "receipt_fingerprint": fingerprint,
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
        "cells": cells,
        "unsearched_declared": list(spec.get("unsearched", [])),
        "territory": territory_cells or None,
    }
    # runtime_seconds is the coordinator wall clock. run_spec sets it. A merge
    # keeps the value already stored on a completed summary and does not time
    # its own assembly.
    summary["science"] = _science(summary)
    atomic_write_json(out_dir / "summary.json", summary)
    if publish is not None:
        _publish_run(summary, spec, publish, out_dir)
    return summary


def _science(summary: dict) -> dict:
    cells = []
    for cell in summary["cells"]:
        cells.append(
            {
                "N": cell["coordinate"]["N"],
                "K_max": cell["coordinate"]["K_max"],
                "families": cell["families"],
                "structural_families": cell["structural_families"],
                "screened_families": cell["screened_families"],
                "baseline_equivalent_families": cell["baseline_equivalent_families"],
                "cardinalities": cell["cardinalities"],
                "cancellations": {
                    key: value
                    for key, value in cell.get("cancellations", {}).items()
                },
                "extremes": cell.get("extremes", {}),
                "family_index_sha256": cell["family_index_sha256"],
                "singles_sha256": cell["singles_sha256"],
                "kernel_index_sha256": cell["kernel_index_sha256"],
                "kernel_index_count": cell["kernel_index_count"],
                "qualitative_index_sha256": cell["qualitative_index_sha256"],
                "observable_index_sha256": cell["observable_index_sha256"],
                "histogram": cell["family_histogram"],
                "territory": cell.get("territory"),
            }
        )
        if cell.get("higher_order_science"):
            cells[-1]["higher_order"] = cell["higher_order_science"]
        if cell.get("clock_census") is not None:
            cells[-1]["clock_census"] = cell["clock_census"]
        if cell.get("n4_census") is not None:
            cells[-1]["n4_census"] = cell["n4_census"]
        if cell.get("v05_census") is not None:
            cells[-1]["v05_census"] = cell["v05_census"]
    return {
        "status": summary["status"],
        "spec_hash": summary["spec_hash"],
        "semantic_version": summary["semantic_version"],
        "composition": summary["composition"],
        "predicates": summary["predicates"],
        "cells": cells,
    }


def scientific_projection(summary: dict) -> dict:
    return json_ready(summary.get("science") or _science(summary))


def status_text(out_dir: Path) -> str:
    out_dir = Path(out_dir)
    progress_path = out_dir / "progress.json"
    if not progress_path.exists():
        return f"no progress manifest in {out_dir}"
    progress = read_json(progress_path)
    lines = [
        f"{progress.get('experiment_id', out_dir.name)}",
        f"status: {progress.get('status')}",
        f"engine: {progress.get('engine_version')}  semantic: {progress.get('semantic_version')}  spec: {progress.get('spec_hash')}",
        (
            f"shards: total {progress.get('total_shards')}  pending {progress.get('pending')}  "
            f"running {progress.get('running')}  completed {progress.get('completed')}  "
            f"failed {progress.get('failed')}  quarantined {progress.get('quarantined')}"
        ),
        f"last completed: {progress.get('last_completed_shard')}",
        f"start: {progress.get('start_time')}",
        f"last heartbeat: {progress.get('last_heartbeat')}",
    ]
    if progress.get("running"):
        lines.append("note: a running shard has no durable result until its receipt is written; resume reconciles a stale running mark")
    return "\n".join(lines)


def verify_directory(out_dir: Path) -> dict:
    out_dir = Path(out_dir)
    plan = read_json(out_dir / "plan.json")
    progress = read_json(out_dir / "progress.json")
    errors = []
    try:
        _require_compatible(plan, plan["spec"], plan["header"]["shard_items"])
    except IncompatibleGeneration as exc:
        errors.append(str(exc))
    for shard in plan["shards"]:
        state = progress["shards"][shard["shard_id"]]
        valid = _receipt_valid(out_dir, shard)
        temporary = out_dir / "shards" / shard["shard_id"] / "result.json.tmp"
        if temporary.exists():
            errors.append(f"{shard['shard_id']} has a temporary result; it is not complete")
        if state["status"] == "completed" and not valid:
            errors.append(f"{shard['shard_id']} is marked completed without a valid receipt")
        if valid and state["status"] != "completed":
            errors.append(f"{shard['shard_id']} has a valid receipt but progress says {state['status']}")
    reported = progress.get("status")
    derived = _status_name(progress)
    if reported != derived:
        errors.append(f"progress status {reported} does not match the shard counts ({derived})")
    return {
        "ok": not errors and derived == "COMPLETE",
        "status": derived,
        "errors": errors,
        "completed": progress.get("completed"),
        "total": progress.get("total_shards"),
        "quarantined": progress.get("quarantined"),
    }


def retry_failed(out_dir: Path, workers: int = DEFAULT_WORKERS) -> dict:
    out_dir = Path(out_dir)
    plan = read_json(out_dir / "plan.json")
    _require_compatible(plan, plan["spec"], plan["header"]["shard_items"])
    progress = read_json(out_dir / "progress.json")
    for state in progress["shards"].values():
        if state["status"] in {"failed", "quarantined"}:
            state["status"] = "pending"
            state["attempts"] = 0
    _save_progress(out_dir, progress)
    return resume_directory(out_dir, workers=workers)


def resume_directory(
    out_dir: Path,
    workers: int = DEFAULT_WORKERS,
    max_shards: int | None = None,
    publish: Path | None = None,
    compare_to: Path | None = None,
) -> dict:
    plan = read_json(Path(out_dir) / "plan.json")
    validate_spec(plan["spec"])
    return run_spec(
        plan["spec"],
        out_dir,
        workers=workers,
        max_shards=max_shards,
        publish=publish,
        compare_to=compare_to,
    )


def run_spec(
    spec: dict,
    out_dir: Path,
    *,
    workers: int = DEFAULT_WORKERS,
    shard_items: int | None = None,
    max_shards: int | None = None,
    publish: Path | None = None,
    compare_to: Path | None = None,
) -> dict:
    validate_spec(spec)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    plan_path = out_dir / "plan.json"
    if plan_path.exists():
        plan = read_json(plan_path)
        items = int(plan["header"]["shard_items"])
        if shard_items is not None and int(shard_items) != items:
            raise IncompatibleGeneration(
                f"refusing to resume: shard_items is {items} in the plan and {shard_items} was requested. "
                "Use a new output directory."
            )
        _require_compatible(plan, spec, items)
    else:
        extras = [path for path in out_dir.iterdir() if path.name != "plan.json"]
        if extras:
            raise IncompatibleGeneration(f"{out_dir} is not empty and has no plan.json")
        plan = build_plan(spec, shard_items)
        atomic_write_json(plan_path, plan)
        atomic_write_json(out_dir / "progress.json", _initial_progress(plan))
    if compare_to is not None:
        _require_comparison_index(Path(compare_to), spec)
    progress = _reconcile(out_dir, plan)
    previous_runtime = 0.0
    summary_path = out_dir / "summary.json"
    if summary_path.exists():
        try:
            previous_runtime = float(read_json(summary_path).get("runtime_seconds") or 0.0)
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            previous_runtime = 0.0
    unfinished = any(state.get("status") != "completed" for state in progress.get("shards", {}).values())
    wall = time.perf_counter()
    _execute(out_dir, plan, progress, workers, max_shards)
    summary = merge_directory(out_dir, publish=None, compare_to=compare_to)
    elapsed = time.perf_counter() - wall
    if unfinished:
        summary["runtime_seconds"] = previous_runtime + elapsed
    elif previous_runtime:
        summary["runtime_seconds"] = previous_runtime
    else:
        summary["runtime_seconds"] = elapsed
    summary["science"] = _science(summary)
    atomic_write_json(summary_path, summary)
    if publish is not None:
        _publish_run(summary, plan["spec"], publish, out_dir)
    return summary
