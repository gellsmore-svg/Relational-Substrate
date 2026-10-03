"""Analysis of one deterministic shard.

``execute_shard_task`` is a module-level function so a spawn-context worker
can import it. A worker builds the grammar it needs, writes one shard
directory, and returns. It does not append to a shared file.
"""

from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import sys
import time
import traceback
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

from rs_constraint_lab.combinadic import next_combination, unrank_combination
from rs_constraint_lab.constraints import Choreography, structurally_simple
from rs_constraint_lab.durable import atomic_write_json, sha256_file
from rs_constraint_lab.dynamics import (
    RelabelTables,
    canonical_tokens,
    classify_cancellation,
    family_ids,
    observable_signature,
    observed_post_release_new_edge,
)
from rs_constraint_lab.generation import _set_id
from rs_constraint_lab.grammar import build_grammar, is_canonical_ids
from rs_constraint_lab.kernel import build_kernel
from rs_constraint_lab.observables import equivalent_kernel, heavy_observables, light_observables, neutral_sentence
from rs_constraint_lab.spec import effective_options
from rs_constraint_lab.version import ENGINE_VERSION, SEMANTIC_VERSION
from rs_constraint_lab.weights import ENUMERATED_WEIGHTS, alphabet_factors


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _fraction(value):
    if value is None:
        return None
    if isinstance(value, Fraction):
        return value
    if isinstance(value, str):
        return Fraction(value)
    return None


def consider_range(ranges: dict, name: str, exact, numeric) -> None:
    slot = ranges.setdefault(name, {"min_exact": None, "max_exact": None, "min": None, "max": None})
    parsed = _fraction(exact)
    if parsed is not None:
        text = f"{parsed.numerator}/{parsed.denominator}"
        if slot["min_exact"] is None or parsed < Fraction(slot["min_exact"]):
            slot["min_exact"] = text
        if slot["max_exact"] is None or parsed > Fraction(slot["max_exact"]):
            slot["max_exact"] = text
    if numeric is not None:
        number = float(numeric)
        slot["min"] = number if slot["min"] is None else min(slot["min"], number)
        slot["max"] = number if slot["max"] is None else max(slot["max"], number)


def merge_ranges(left: dict, right: dict) -> dict:
    merged: dict = {}
    for name in set(left) | set(right):
        consider_range(merged, name, None, None)
        for source in (left.get(name), right.get(name)):
            if not source:
                continue
            consider_range(merged, name, source.get("min_exact"), None)
            consider_range(merged, name, source.get("max_exact"), None)
            consider_range(merged, name, None, source.get("min"))
            consider_range(merged, name, None, source.get("max"))
    return merged


def consider_extreme(box: dict, name: str, value, expressions, kernel_id: str, *, higher: bool) -> None:
    if value is None:
        return
    if isinstance(value, Fraction):
        kind = "fraction"
        stored = f"{value.numerator}/{value.denominator}"
        comparable = value
    else:
        kind = "float"
        stored = float(value)
        comparable = stored
    payload = {"value": stored, "kind": kind, "expressions": list(expressions), "kernel": kernel_id}

    def as_comparable(item):
        if item["kind"] == "fraction":
            return Fraction(item["value"])
        return float(item["value"])

    current = box.get(name)
    if current is None:
        box[name] = payload
        return
    old = as_comparable(current)
    better = comparable > old if higher else comparable < old
    tie = comparable == old and tuple(expressions) < tuple(current["expressions"])
    if better or tie:
        box[name] = payload


def merge_extremes(left: dict, right: dict) -> dict:
    merged = dict(left)
    for name, payload in right.items():
        value = Fraction(payload["value"]) if payload["kind"] == "fraction" else float(payload["value"])
        consider_extreme(merged, name, value, payload["expressions"], payload["kernel"], higher=name.endswith("_max"))
    return merged


def _keep_examples(bucket: list, expressions, limit: int = 8) -> None:
    row = list(expressions)
    if row in bucket:
        return
    bucket.append(row)
    bucket.sort()
    del bucket[limit:]


def _apply_fault(task: dict, shard_dir: Path) -> None:
    spec = os.environ.get("RS_LAB_FAULT", "")
    if not spec:
        return
    kind, _, rest = spec.partition(":")
    if not rest or int(rest) != int(task["ordinal"]):
        return
    if kind == "always":
        raise RuntimeError("injected permanent shard failure")
    if kind == "once":
        marker = shard_dir / "fault-once"
        if not marker.exists():
            marker.write_text("consumed\n", encoding="utf-8")
            raise RuntimeError("injected one-shot shard failure")


def _fresh_family(qualitative: str, cardinality: int, expressions, k_here: int, arity: int, light: dict, ids: dict, n: int) -> dict:
    return {
        "count": 0,
        "n": n,
        "cardinality": cardinality,
        "expressions": list(expressions),
        "k_max": k_here,
        "arity": arity,
        "support_family": ids["support_family"],
        "modal_family": ids["modal_family"],
        "qualitative_family": qualitative,
        "support_matches_baseline": light["support_matches_baseline"],
        "n_deadlock": light["n_deadlock"],
        "n_recurrent": light["n_recurrent"],
        "periods": list(light["periods"]),
        "equivalent_members": 0,
        "count_literal_members": 0,
        "kernel_ids": set(),
        "observable_ids": set(),
        "ranges": {},
        "observed": neutral_sentence(light),
    }


def _note_family(family: dict, cardinality: int, expressions, k_here: int, arity: int, light: dict, same: bool, has_count: bool, ids: dict, signature: str) -> None:
    family["count"] += 1
    if (cardinality, tuple(expressions)) < (family["cardinality"], tuple(family["expressions"])):
        family["cardinality"] = cardinality
        family["expressions"] = list(expressions)
        family["k_max"] = k_here
        family["arity"] = arity
        family["observed"] = neutral_sentence(light)
    if same:
        family["equivalent_members"] += 1
    if has_count:
        family["count_literal_members"] += 1
    family["kernel_ids"].add(ids["exact_kernel_family"])
    family["observable_ids"].add(signature)


def _record_ranges(family: dict, light: dict, heavy: dict, excess_exact, excess_float) -> None:
    pairs = (
        ("mean_edge_density", heavy.get("mean_edge_density_exact"), heavy.get("mean_edge_density")),
        ("entropy_rate_bits", None, heavy.get("entropy_rate_bits")),
        ("tv_from_uniform", heavy.get("tv_from_uniform_exact"), heavy.get("tv_from_uniform")),
        ("reversibility_defect", heavy.get("reversibility_defect_exact"), heavy.get("reversibility_defect")),
        ("halt_mass", heavy.get("halt_mass_exact"), heavy.get("halt_mass")),
        ("rise_then_release", heavy.get("rise_then_release_exact"), heavy.get("rise_then_release")),
        ("rise_then_release_excess", excess_exact, excess_float),
        ("triangle_mass", heavy.get("triangle_mass_exact"), heavy.get("triangle_mass")),
        ("max_abs_dissolve_shift", light.get("max_abs_dissolve_shift_exact"), light.get("max_abs_dissolve_shift")),
        ("closing_bias", light.get("closing_bias_exact"), light.get("closing_bias")),
        ("disjoint_pair_mass", heavy.get("disjoint_pair_mass_exact"), heavy.get("disjoint_pair_mass")),
    )
    for name, exact, numeric in pairs:
        if exact is None and numeric is None:
            continue
        consider_range(family["ranges"], name, exact, numeric)


def _serialise_families(families: dict) -> dict:
    serialised = {}
    for key in sorted(families):
        family = dict(families[key])
        family["kernel_ids"] = sorted(family["kernel_ids"])
        family["observable_ids"] = sorted(family["observable_ids"])
        serialised[key] = family
    return serialised


def execute_shard_task(task: dict) -> dict:
    shard_id = task["shard_id"]
    try:
        _execute(task)
        return {"ok": True, "shard_id": shard_id}
    except Exception as exc:
        running = Path(task["shard_dir"]) / "running.json"
        running.unlink(missing_ok=True)
        return {
            "ok": False,
            "shard_id": shard_id,
            "exception_type": type(exc).__name__,
            "message": str(exc),
            "traceback": traceback.format_exc(),
        }


def _execute(task: dict) -> None:
    identity = task["identity"]
    if identity["semantic_version"] != SEMANTIC_VERSION or identity["engine_version"] != ENGINE_VERSION:
        raise RuntimeError("shard identity does not match this engine")
    shard_dir = Path(task["shard_dir"])
    shard_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(
        shard_dir / "running.json",
        {"shard_id": task["shard_id"], "attempt": task["attempt"], "started_at": _now(), "pid": os.getpid()},
    )
    _apply_fault(task, shard_dir)
    started = time.perf_counter()
    spec = task["spec"]
    options = effective_options(spec)
    n = int(task["n"])
    k_max = int(task["k_max"])
    cardinality = int(task["cardinality"])
    a_max = task["a_max"]
    grammar = build_grammar(
        n,
        k_max,
        spec.get("weights", list(ENUMERATED_WEIGHTS)),
        a_max=a_max,
        predicates=tuple(options["predicates"]),
    )
    labelled_n = len(grammar.labelled)
    factors = alphabet_factors(spec["alphabet"])
    horizon = int(spec.get("rise_release_horizon", 4))
    baseline_kernel = build_kernel(n, Choreography(0, 0, ()), factors)
    baseline_heavy = heavy_observables(baseline_kernel, horizon, 0)
    baseline_rise = baseline_heavy.get("rise_then_release_exact")
    baseline_rise_float = baseline_heavy.get("rise_then_release")
    tables = RelabelTables(n) if labelled_n else None
    sensitivity_factors = [alphabet_factors(name) for name in spec.get("sensitivity_alphabets", [])]
    edge_list = list(grammar.edge_list)
    families: dict = {}
    singles = []
    extremes: dict = {}
    cancellations = {
        "genuine_global": 0,
        "local": 0,
        "inherited_baseline": 0,
        "genuine_global_examples": [],
        "local_examples": [],
        "inherited_baseline_examples": [],
    }
    sensitivity = {"checks": 0, "modal_unchanged": 0, "support_unchanged": 0}
    threshold_motifs = []
    counts = {
        "scanned": 0,
        "symmetry_removed": 0,
        "stacked_canonical": 0,
        "stacked_analysed": 0,
        "analysed": 0,
    }
    start = int(task["start"])
    end = int(task["end"])
    if labelled_n >= cardinality and end > start:
        combo = unrank_combination(start, labelled_n, cardinality)
        for _index in range(start, end):
            ids = combo
            counts["scanned"] += 1
            simple = structurally_simple(grammar.labelled[i] for i in ids)
            if not is_canonical_ids(ids, grammar.image):
                counts["symmetry_removed"] += 1
            elif options["composition"] == "structural-simple" and not simple:
                counts["stacked_canonical"] += 1
            else:
                if not simple:
                    counts["stacked_analysed"] += 1
                _analyse_one(
                    grammar,
                    ids,
                    factors,
                    baseline_kernel,
                    baseline_rise,
                    baseline_rise_float,
                    tables,
                    horizon,
                    sensitivity_factors,
                    edge_list,
                    spec["alphabet"],
                    cardinality,
                    families,
                    singles,
                    extremes,
                    cancellations,
                    sensitivity,
                    threshold_motifs,
                    n,
                )
                counts["analysed"] += 1
            combo = next_combination(combo, labelled_n)
            if combo is None and _index + 1 < end:
                raise RuntimeError("combination index ended before the shard boundary")
    counts["canonical_including_stacked"] = counts["stacked_canonical"] + counts["analysed"]
    counts["canonical_simple"] = counts["analysed"] - counts["stacked_analysed"]
    result = {
        "identity": identity,
        "counts": counts,
        "families": _serialise_families(families),
        "singles": singles,
        "extremes": extremes,
        "cancellations": cancellations,
        "sensitivity": sensitivity,
        "threshold_motifs": sorted(threshold_motifs, key=lambda row: row["expressions"]),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    # Timing is not part of the scientific result. It stays on the receipt.
    elapsed = result.pop("elapsed_seconds")
    result_path = shard_dir / "result.json"
    atomic_write_json(result_path, result)
    digest = sha256_file(result_path)
    receipt = {
        "status": "completed",
        "shard_id": task["shard_id"],
        "identity": identity,
        "result_sha256": digest,
        "attempt": task["attempt"],
        "engine_version": ENGINE_VERSION,
        "semantic_version": SEMANTIC_VERSION,
        "spec_hash": identity["spec_hash"],
        "grammar_version": identity["grammar_version"],
        "normalisation_version": identity["normalisation_version"],
        "python": sys.version.split()[0],
        "numpy": __import__("numpy").__version__,
        "counts": counts,
        "elapsed_seconds": elapsed,
        "finished_at": _now(),
    }
    atomic_write_json(shard_dir / "receipt.json", receipt)
    (shard_dir / "running.json").unlink(missing_ok=True)


def _analyse_one(
    grammar,
    ids,
    factors,
    baseline_kernel,
    baseline_rise,
    baseline_rise_float,
    tables,
    horizon,
    sensitivity_factors,
    edge_list,
    alphabet,
    cardinality,
    families,
    singles,
    extremes,
    cancellations,
    sensitivity,
    threshold_motifs,
    n,
) -> None:
    constraints = tuple(grammar.labelled[i] for i in ids)
    expressions = tuple(sorted(grammar.expression(i) for i in ids))
    kernel = build_kernel(n, Choreography(0, 0, constraints), factors)
    light = light_observables(kernel, baseline_kernel)
    light.pop("modes", None)
    light.pop("deadlock_states", None)
    same = equivalent_kernel(kernel, baseline_kernel)
    light["equivalent_to_baseline"] = same
    heavy = heavy_observables(kernel, horizon, 0)
    excess_exact = None
    excess_float = None
    if baseline_rise and heavy.get("rise_then_release_exact"):
        excess = Fraction(heavy["rise_then_release_exact"]) - Fraction(baseline_rise)
        excess_exact = f"{excess.numerator}/{excess.denominator}"
        excess_float = float(excess)
    elif baseline_rise_float is not None and heavy.get("rise_then_release") is not None:
        excess_float = heavy["rise_then_release"] - baseline_rise_float
    tokens = canonical_tokens(kernel, tables)
    ids_map = family_ids(n, tokens)
    signature = observable_signature(n, light, heavy)
    named: set[int] = set()
    for constraint in constraints:
        named.update(edge_list[constraint.action])
        for edge, _bit in constraint.conditions:
            named.update(edge_list[edge])
    arity = len(named)
    k_here = max(constraint.k() for constraint in constraints)
    qualitative = ids_map["qualitative_family"]
    family = families.get(qualitative)
    if family is None:
        family = _fresh_family(qualitative, cardinality, expressions, k_here, arity, light, ids_map, n)
        families[qualitative] = family
    has_count = any(constraint.has_count_literal() for constraint in constraints)
    _note_family(family, cardinality, expressions, k_here, arity, light, same, has_count, ids_map, signature)
    _record_ranges(family, light, heavy, excess_exact, excess_float)
    kind = classify_cancellation(n, constraints, factors, kernel, baseline_kernel)
    if kind is not None:
        cancellations[kind] += 1
        _keep_examples(cancellations[f"{kind}_examples"], expressions)
    kernel_id = ids_map["exact_kernel_family"]
    consider_extreme(extremes, "rise_excess_max", _fraction(excess_exact) if excess_exact else excess_float, expressions, kernel_id, higher=True)
    consider_extreme(extremes, "rise_excess_min", _fraction(excess_exact) if excess_exact else excess_float, expressions, kernel_id, higher=False)
    consider_extreme(extremes, "closing_max", _fraction(light.get("closing_bias_exact")), expressions, kernel_id, higher=True)
    consider_extreme(extremes, "closing_min", _fraction(light.get("closing_bias_exact")), expressions, kernel_id, higher=False)
    consider_extreme(extremes, "shift_max", _fraction(light.get("max_abs_dissolve_shift_exact")), expressions, kernel_id, higher=True)
    consider_extreme(extremes, "entropy_max", heavy.get("entropy_rate_bits"), expressions, kernel_id, higher=True)
    consider_extreme(extremes, "entropy_min", heavy.get("entropy_rate_bits"), expressions, kernel_id, higher=False)
    if cardinality == 1:
        singles.append(
            {
                "N": n,
                "alphabet": alphabet,
                "set_id": _set_id(alphabet, list(expressions)),
                "expressions": " && ".join(expressions),
                "K": k_here,
                "A": arity,
                "equivalent_to_baseline": same,
                "family_id": qualitative,
                "exact_kernel_family": kernel_id,
                "support_matches_baseline": light["support_matches_baseline"],
                "n_deadlock": light["n_deadlock"],
                "n_recurrent": light["n_recurrent"],
                "periods": " ".join(str(item) for item in light["periods"]),
                "max_abs_dissolve_shift": light["max_abs_dissolve_shift"],
                "max_abs_dissolve_shift_exact": light["max_abs_dissolve_shift_exact"],
                "closing_bias": light["closing_bias"],
                "closing_bias_exact": light["closing_bias_exact"],
                "mean_edge_density": heavy.get("mean_edge_density"),
                "mean_edge_density_exact": heavy.get("mean_edge_density_exact"),
                "entropy_rate_bits": heavy.get("entropy_rate_bits"),
                "tv_from_uniform": heavy.get("tv_from_uniform"),
                "tv_from_uniform_exact": heavy.get("tv_from_uniform_exact"),
                "halt_mass": heavy.get("halt_mass"),
                "halt_mass_exact": heavy.get("halt_mass_exact"),
                "rise_then_release": heavy.get("rise_then_release"),
                "rise_then_release_exact": heavy.get("rise_then_release_exact"),
                "rise_then_release_excess": excess_float,
                "rise_then_release_excess_exact": excess_exact,
                "reversibility_defect": heavy.get("reversibility_defect"),
                "reversibility_defect_exact": heavy.get("reversibility_defect_exact"),
                "triangle_mass": heavy.get("triangle_mass"),
                "triangle_mass_exact": heavy.get("triangle_mass_exact"),
                "disjoint_pair_mass": heavy.get("disjoint_pair_mass"),
                "stationary_arithmetic": heavy.get("stationary_arithmetic"),
                "stationary_residual": heavy.get("stationary_residual"),
            }
        )
        for extra in sensitivity_factors:
            extra_kernel = build_kernel(n, Choreography(0, 0, constraints), extra)
            extra_ids = family_ids(n, canonical_tokens(extra_kernel, tables))
            sensitivity["checks"] += 1
            if extra_ids["modal_family"] == ids_map["modal_family"]:
                sensitivity["modal_unchanged"] += 1
            if extra_ids["support_family"] == ids_map["support_family"]:
                sensitivity["support_unchanged"] += 1
    if has_count:
        threshold_motifs.append(
            {
                "expressions": list(expressions),
                "kernel": kernel_id,
                "qualitative": qualitative,
                "observable": signature,
                "support": ids_map["support_family"],
                "modal": ids_map["modal_family"],
                "cardinality": cardinality,
                "post_release_new_edge": observed_post_release_new_edge(kernel, constraints, factors)
                if n <= 4
                else False,
            }
        )
