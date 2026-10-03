"""Exhaustive generation runner.

Every canonical constraint set in a requested cell receives a light exact
analysis (support, classes, period, one-step dissolution shift, closing
probability). Stationary analysis runs for every singleton and for the
first-seen member of every modal-and-support family. The short rise-then-release
path measure runs inside that stationary call when the state space has at most
64 states. Sensitivity across geometric alphabets runs on singletons.
"""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
import platform
import subprocess
import sys
import time
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path

import numpy as np

from rs_constraint_lab.accounting import template_accounting
from rs_constraint_lab.constraints import Choreography, parse_expression
from rs_constraint_lab.grammar import build_grammar, is_canonical_ids
from rs_constraint_lab.kernel import build_kernel
from rs_constraint_lab.observables import (
    equivalent_kernel,
    heavy_observables,
    light_observables,
    neutral_sentence,
)
from rs_constraint_lab.spec import spec_hash
from rs_constraint_lab.state import canonical_states, edge_count, n_states
from rs_constraint_lab.trajectory import sample_trajectory
from rs_constraint_lab.version import ENGINE_VERSION
from rs_constraint_lab.weights import alphabet_factors

FAMILY_INDEX_COMMIT_LIMIT_BYTES = 2_000_000
MEASURE_SCOPE = {
    "search": "every canonical constraint set at the requested cardinalities",
    "light": "every canonical set: support, communicating classes, period, deadlock, dissolve shift, closing bias",
    "heavy": "every cardinality-1 set, and the first-seen member of each modal-and-support family",
    "rise_then_release": "inside every heavy call, from the empty state, only when the labelled state count is at most 64",
    "sensitivity": "every cardinality-1 set, on the declared geometric alphabets",
    "screen_rise_excess": "the family exemplar only; dissolve shift and closing bias use the family range",
    "stationary": "rational when the labelled state count is at most 16; otherwise float64 with a recorded residual, Cesaro if the solve is unstable",
}


def _git_commit() -> str | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return out.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def _set_id(alphabet: str, expressions: list[str]) -> str:
    body = alphabet + "\n" + "\n".join(sorted(expressions))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]


def _json_ready(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_ready(item) for item in value]
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return value
    return value


@dataclass
class Family:
    family_id: str
    count: int = 0
    cardinality: int = 0
    expressions: list[str] = field(default_factory=list)
    k_max: int = 0
    arity: int = 0
    light: dict = field(default_factory=dict)
    heavy: dict | None = None
    shift_min: float = 0.0
    shift_max: float = 0.0
    closing_min: float | None = None
    closing_max: float | None = None
    equivalent_to_baseline: bool = False


def _update_family(families: dict[str, Family], family_id: str, cardinality: int, expressions, k_max, arity, light, equivalent: bool) -> Family:
    shift = light["max_abs_dissolve_shift"]
    closing = light["closing_bias"]
    if family_id not in families:
        families[family_id] = Family(
            family_id=family_id,
            count=1,
            cardinality=cardinality,
            expressions=list(expressions),
            k_max=k_max,
            arity=arity,
            light=light,
            shift_min=shift,
            shift_max=shift,
            closing_min=closing,
            closing_max=closing,
            equivalent_to_baseline=equivalent,
        )
        return families[family_id]
    family = families[family_id]
    family.count += 1
    family.shift_min = min(family.shift_min, shift)
    family.shift_max = max(family.shift_max, shift)
    if closing is not None:
        family.closing_min = closing if family.closing_min is None else min(family.closing_min, closing)
        family.closing_max = closing if family.closing_max is None else max(family.closing_max, closing)
    return family


def _analyse_set(n, expressions, factors, baseline, horizon):
    constraints = tuple(parse_expression(text, n) for text in expressions)
    kernel = build_kernel(n, Choreography(0, 0, constraints), factors)
    light = light_observables(kernel, baseline)
    light.pop("modes", None)
    same = equivalent_kernel(kernel, baseline)
    return kernel, constraints, light, same


def run_experiment(spec: dict, out_dir: Path, publish_root: Path | None = None) -> dict:
    started = time.perf_counter()
    out_dir.mkdir(parents=True, exist_ok=True)
    digest = spec_hash(spec)
    factors = alphabet_factors(spec["alphabet"])
    sensitivity = [alphabet_factors(name) for name in spec.get("sensitivity_alphabets", [])]
    sensitivity_names = list(spec.get("sensitivity_alphabets", []))
    screens = spec.get("predeclared_screens", {})
    horizon = int(spec.get("rise_release_horizon", 4))
    cells = []
    for cell in spec["cells"]:
        cells.append(
            _run_cell(spec, cell, factors, sensitivity, sensitivity_names, screens, horizon, digest, out_dir)
        )
    summary = {
        "engine_version": ENGINE_VERSION,
        "git_commit": _git_commit(),
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "platform": platform.platform(),
        "spec_hash": digest,
        "experiment_id": spec["experiment_id"],
        "generation": spec["generation"],
        "runtime_seconds": time.perf_counter() - started,
        "cells": cells,
        "unsearched_declared": list(spec.get("unsearched", [])),
    }
    _write_json(out_dir / "summary.json", summary)
    if publish_root is not None:
        _publish(summary, spec, publish_root, out_dir)
    return summary


def _run_cell(spec, cell, factors, sensitivity, sensitivity_names, screens, horizon, digest, out_dir):
    n = int(cell["N"])
    k_max = int(cell["K_max"])
    cardinalities = list(cell["cardinalities"])
    print(f"[cell] N={n} K<={k_max} cardinalities={cardinalities}", file=sys.stderr)
    t0 = time.perf_counter()
    grammar = build_grammar(n, k_max, spec["weights"])
    accounting = template_accounting(n, k_max, len(spec["weights"]))
    if accounting["labelled_constraints"] != len(grammar.labelled):
        raise RuntimeError(
            f"accounting labelled {accounting['labelled_constraints']} "
            f"!= grammar {len(grammar.labelled)}"
        )
    canon_states = canonical_states(n)
    baseline_kernel = build_kernel(n, Choreography(0, 0, ()), factors)
    baseline_light = light_observables(baseline_kernel, baseline_kernel)
    baseline_light.pop("modes", None)
    baseline_heavy = heavy_observables(baseline_kernel, horizon, 0)
    baseline_rise = baseline_heavy["rise_then_release"]
    families: dict[str, Family] = {}
    singles_rows = []
    coverage_cards = {}
    invariant_checks = 0
    invariant_modal = 0
    invariant_support = 0
    references = []
    for text in spec.get("reference_expressions", []):
        references.append(_locate_reference(grammar, text, n))

    for cardinality in cardinalities:
        seen, row_slice, inv = _enumerate_cardinality(
            grammar,
            cardinality,
            factors,
            sensitivity,
            baseline_kernel,
            baseline_light,
            baseline_heavy,
            baseline_rise,
            families,
            horizon,
            screens,
        )
        coverage_cards[str(cardinality)] = seen
        if cardinality == 1:
            singles_rows.extend(row_slice)
        invariant_checks += inv["checks"]
        invariant_modal += inv["modal"]
        invariant_support += inv["support"]
        print(
            f"[cell] N={n} cardinality={cardinality} canonical={seen['canonical']} "
            f"families_so_far={len(families)}",
            file=sys.stderr,
        )

    for reference in references:
        if reference.get("in_grammar"):
            match = next((row for row in singles_rows if row["expressions"] == reference["canonical_expression"]), None)
            reference["single"] = match

    exemplars = _write_exemplars(
        spec, n, factors, grammar, families, references, baseline_heavy, digest, out_dir, screens, baseline_rise
    )
    family_rows = [_family_row(spec, n, k_max, family, baseline_rise, screens) for family in families.values()]
    family_path = out_dir / f"families-n{n}-k{k_max}.jsonl"
    _write_jsonl(family_path, family_rows)
    _write_singles(out_dir / f"singles-n{n}-k{k_max}.csv", singles_rows)
    motifs = _select_motifs(family_rows)
    for motif in motifs:
        _write_json(out_dir / "motifs" / f"n{n}-k{k_max}-{motif['motif_id']}.json", motif)
    structural = sum(1 for row in family_rows if "structural" in row["tags"])
    screened = sum(1 for row in family_rows if "screened" in row["tags"])
    nulls = sum(1 for row in family_rows if "baseline-equivalent" in row["tags"])
    return {
        "coordinate": _coordinate(spec, n, k_max, cell),
        "runtime_seconds": time.perf_counter() - t0,
        "accounting": accounting,
        "canonical_states": len(canon_states),
        "relation_slots": edge_count(n),
        "labelled_states": n_states(n),
        "cardinalities": coverage_cards,
        "baseline": {"light": _json_ready(baseline_light), "heavy": _json_ready(baseline_heavy)},
        "measure_scope": MEASURE_SCOPE,
        "families": len(family_rows),
        "family_histogram": _family_histogram(family_rows),
        "family_index_bytes": family_path.stat().st_size,
        "family_index_commit_limit_bytes": FAMILY_INDEX_COMMIT_LIMIT_BYTES,
        "motif_ids": [motif["motif_id"] for motif in motifs],
        "structural_families": structural,
        "screened_families": screened,
        "baseline_equivalent_families": nulls,
        "sensitivity": {
            "alphabets": sensitivity_names,
            "checks": invariant_checks,
            "modal_unchanged": invariant_modal,
            "support_unchanged": invariant_support,
        },
        "references": _json_ready(references),
        "exemplars": exemplars,
        "not_searched": _not_searched(n, k_max, cardinalities, accounting),
    }


def _coordinate(spec, n, k_max, cell) -> dict:
    return {
        "N": n,
        "A_max": cell.get("A_max"),
        "O": spec.get("O", 2),
        "G": spec.get("G", 0),
        "S": spec.get("S", 0),
        "H": spec.get("H", 0),
        "K_max": k_max,
        "L": spec.get("L", 0),
        "semantics": spec["semantics"],
        "alphabet": spec["alphabet"],
    }


def _not_searched(n, k_max, cardinalities, accounting) -> list[str]:
    notes = []
    for missing in (1, 2, 3):
        if missing not in cardinalities:
            notes.append(f"cardinality {missing} at N={n} was not searched")
    if accounting["outside_k_bound"]:
        notes.append(
            f"{accounting['outside_k_bound']} structural templates at N={n} have K>{k_max} and were not searched"
        )
    notes.append("multisets that repeat one constraint were not searched; repetition is a weight change")
    if n >= 5 and 2 in cardinalities:
        notes.append("this note should not appear: N>=5 pairs were not expected")
    return notes


def _locate_reference(grammar, text, n) -> dict:
    try:
        constraint = parse_expression(text, n)
    except ValueError as exc:
        return {"expression": text, "in_grammar": False, "reason": str(exc)}
    if constraint.k() > grammar.k_max or constraint.weight not in grammar.weights:
        return {
            "expression": text,
            "in_grammar": False,
            "reason": "outside this cell's K bound or weight list",
        }
    found = next((i for i, item in enumerate(grammar.labelled) if item.key() == constraint.key()), None)
    if found is None:
        return {"expression": text, "in_grammar": False, "reason": "not in the normal-form grammar"}
    from rs_constraint_lab.grammar import canonical_id_tuple

    canon = canonical_id_tuple((found,), grammar.image)
    return {
        "expression": text,
        "in_grammar": True,
        "canonical_expression": grammar.expression(canon[0]),
        "same_labelling": text == grammar.expression(canon[0]),
    }


def _enumerate_cardinality(grammar, cardinality, factors, sensitivity, baseline_kernel, baseline_light, baseline_heavy, baseline_rise, families, horizon, screens):
    labelled_n = len(grammar.labelled)
    total = math.comb(labelled_n, cardinality)
    canonical = 0
    rows = []
    inv = {"checks": 0, "modal": 0, "support": 0}
    edge_list = list(grammar.edge_list)
    iterator = itertools.combinations(range(labelled_n), cardinality)
    report_every = 200_000
    for offset, ids in enumerate(iterator, start=1):
        if offset % report_every == 0:
            print(f"  scanned {offset}/{total} cardinality={cardinality}", file=sys.stderr)
        if not is_canonical_ids(ids, grammar.image):
            continue
        canonical += 1
        expressions = [grammar.expression(i) for i in ids]
        k_here = max(grammar.labelled[i].k() for i in ids)
        named: set[int] = set()
        for i in ids:
            constraint = grammar.labelled[i]
            named.update(edge_list[constraint.action])
            for edge, _bit in constraint.conditions:
                named.update(edge_list[edge])
        arity = len(named)
        kernel, _constraints, light, same = _analyse_set(grammar.n, expressions, factors, baseline_kernel, horizon)
        family_id = hashlib.sha256(
            f"{grammar.n}|{light['modal_family']}|{light['support_family']}".encode()
        ).hexdigest()[:16]
        family = _update_family(families, family_id, cardinality, expressions, k_here, arity, light, same)
        heavy = None
        if cardinality == 1 or family.heavy is None:
            heavy = heavy_observables(kernel, horizon, 0)
            if baseline_rise is not None and heavy["rise_then_release"] is not None:
                heavy["rise_then_release_excess"] = heavy["rise_then_release"] - baseline_rise
            if family.heavy is None:
                family.heavy = heavy
        if cardinality == 1:
            rows.append(
                _single_row(
                    grammar.n,
                    expressions,
                    k_here,
                    arity,
                    light,
                    heavy,
                    same,
                    family_id,
                    spec_alphabet_placeholder(factors),
                )
            )
            inv_one = _sensitivity(grammar.n, expressions, sensitivity, light)
            inv["checks"] += inv_one["checks"]
            inv["modal"] += inv_one["modal"]
            inv["support"] += inv_one["support"]
    coverage = {
        "labelled_combinations": total,
        "canonical": canonical,
        "removed_by_symmetry": total - canonical,
    }
    return coverage, rows, inv


def spec_alphabet_placeholder(factors) -> str:
    from rs_constraint_lab.weights import ALPHABET_BASE, alphabet_factors as build

    for name in ALPHABET_BASE:
        if build(name) == factors:
            return name
    return "custom"


def _single_row(n, expressions, k_here, arity, light, heavy, same, family_id, alphabet) -> dict:
    heavy = heavy or {}
    return {
        "N": n,
        "alphabet": alphabet,
        "set_id": _set_id(alphabet, expressions),
        "expressions": " && ".join(sorted(expressions)),
        "K": k_here,
        "A": arity,
        "equivalent_to_baseline": same,
        "family_id": family_id,
        "support_matches_baseline": light["support_matches_baseline"],
        "n_deadlock": light["n_deadlock"],
        "n_recurrent": light["n_recurrent"],
        "periods": " ".join(str(item) for item in light["periods"]),
        "max_abs_dissolve_shift": light["max_abs_dissolve_shift"],
        "closing_bias": light["closing_bias"],
        "mean_edge_density": heavy.get("mean_edge_density"),
        "entropy_rate_bits": heavy.get("entropy_rate_bits"),
        "tv_from_uniform": heavy.get("tv_from_uniform"),
        "halt_mass": heavy.get("halt_mass"),
        "rise_then_release": heavy.get("rise_then_release"),
        "rise_then_release_excess": heavy.get("rise_then_release_excess"),
        "reversibility_defect": heavy.get("reversibility_defect"),
        "triangle_mass": heavy.get("triangle_mass"),
        "disjoint_pair_mass": heavy.get("disjoint_pair_mass"),
        "stationary_arithmetic": heavy.get("stationary_arithmetic"),
        "stationary_residual": heavy.get("stationary_residual"),
    }


def _sensitivity(n, expressions, sensitivity_factors, light) -> dict:
    checks = modal_hits = support_hits = 0
    constraints = tuple(parse_expression(text, n) for text in expressions)
    from rs_constraint_lab.kernel import modal_map, support_map

    for factors in sensitivity_factors:
        kernel = build_kernel(n, Choreography(0, 0, constraints), factors)
        mode_id = hashlib.sha256(repr((n, modal_map(kernel))).encode()).hexdigest()[:16]
        support_id = hashlib.sha256(repr((n, support_map(kernel))).encode()).hexdigest()[:16]
        checks += 1
        if mode_id == light["modal_family"]:
            modal_hits += 1
        if support_id == light["support_family"]:
            support_hits += 1
    return {"checks": checks, "modal": modal_hits, "support": support_hits}


def _family_tags(family: Family, screens) -> list[str]:
    light = family.light
    heavy = family.heavy or {}
    tags = []
    if family.equivalent_to_baseline:
        tags.append("baseline-equivalent")
    if not light["support_matches_baseline"]:
        tags.append("structural")
    shift_bar = float(screens.get("max_abs_dissolve_shift_notable", 0.1))
    close_bar = float(screens.get("closing_bias_abs_notable", 0.1))
    rise_bar = float(screens.get("rise_release_excess_notable", 0.05))
    excess = heavy.get("rise_then_release_excess")
    screened = family.shift_max >= shift_bar
    for closing in (family.closing_min, family.closing_max):
        if closing is not None and abs(closing) >= close_bar:
            screened = True
    if excess is not None and abs(excess) >= rise_bar:
        screened = True
    if screened and not family.equivalent_to_baseline:
        tags.append("screened")
    if "structural" not in tags and "baseline-equivalent" not in tags:
        tags.append("measure")
    return tags


def _family_row(spec, n, k_max, family: Family, baseline_rise, screens) -> dict:
    del k_max, baseline_rise
    light = family.light
    heavy = family.heavy or {}
    return {
        "motif_id": family.family_id,
        "tags": _family_tags(family, screens),
        "count": family.count,
        "expressions": sorted(family.expressions),
        "coordinate": {
            "N": n,
            "A": family.arity,
            "O": spec.get("O", 2),
            "G": spec.get("G", 0),
            "S": spec.get("S", 0),
            "H": spec.get("H", 0),
            "K": family.k_max,
            "L": spec.get("L", 0),
            "semantics": spec["semantics"],
            "alphabet": spec["alphabet"],
            "cardinality": family.cardinality,
        },
        "observed": neutral_sentence(light),
        "support_matches_baseline": light["support_matches_baseline"],
        "n_deadlock": light["n_deadlock"],
        "n_recurrent": light["n_recurrent"],
        "periods": light["periods"],
        "shift_min": family.shift_min,
        "shift_max": family.shift_max,
        "closing_min": family.closing_min,
        "closing_max": family.closing_max,
        "mean_edge_density": heavy.get("mean_edge_density"),
        "entropy_rate_bits": heavy.get("entropy_rate_bits"),
        "tv_from_uniform": heavy.get("tv_from_uniform"),
        "halt_mass": heavy.get("halt_mass"),
        "rise_then_release": heavy.get("rise_then_release"),
        "rise_then_release_excess": heavy.get("rise_then_release_excess"),
        "reversibility_defect": heavy.get("reversibility_defect"),
        "triangle_mass": heavy.get("triangle_mass"),
        "disjoint_pair_mass": heavy.get("disjoint_pair_mass"),
        "stationary_arithmetic": heavy.get("stationary_arithmetic"),
        "stationary_residual": heavy.get("stationary_residual"),
        "equivalent_to_baseline": family.equivalent_to_baseline,
    }


def _quantiles(values: list[float]) -> dict[str, float]:
    if not values:
        return {}
    ordered = sorted(values)

    def at(probability: float) -> float:
        if len(ordered) == 1:
            return ordered[0]
        position = probability * (len(ordered) - 1)
        lower = int(position)
        upper = min(lower + 1, len(ordered) - 1)
        fraction = position - lower
        return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction

    return {str(probability): at(probability) for probability in (0, 0.25, 0.5, 0.75, 0.9, 0.99, 1)}


def _family_histogram(rows: list[dict]) -> dict:
    periods: dict[str, int] = {}
    deadlocks: dict[str, int] = {}
    for row in rows:
        key = " ".join(str(item) for item in row["periods"])
        periods[key] = periods.get(key, 0) + 1
        dead = str(row["n_deadlock"])
        deadlocks[dead] = deadlocks.get(dead, 0) + 1
    excesses = [
        row["rise_then_release_excess"]
        for row in rows
        if row.get("rise_then_release_excess") is not None
    ]
    closings = [row["closing_max"] for row in rows if row.get("closing_max") is not None]
    return {
        "families": len(rows),
        "support_matches_baseline": sum(1 for row in rows if row["support_matches_baseline"]),
        "shift_max": _quantiles([row["shift_max"] for row in rows]),
        "closing_max": _quantiles(closings),
        "rise_then_release_excess": _quantiles(excesses),
        "periods": periods,
        "n_deadlock": deadlocks,
    }


EVALUATION_VECTOR = {
    "reproducibility": "exact kernel; stochastic runs are seeded replays",
    "coverage": "exhaustive inside the cell coordinate",
    "parameter_robustness": "geometric bases preserve the modal map and the support; magnitudes change",
    "symmetry_robustness": "orbit representative under the full symmetric group",
    "cross_substrate_recurrence": "not tested in this generation",
    "trajectory_distinctiveness": "rise_then_release_excess and reversibility_defect, where computed",
    "interpretability": "the observed sentence is structural; naming is left to the report",
    "global_coherence_relevance": "open; not scored",
}


def _motif_record(row: dict) -> dict:
    return {
        "motif_id": row["motif_id"],
        "canonical_constraint_set": row["expressions"],
        "coordinate": row["coordinate"],
        "count_in_family": row["count"],
        "tags": row["tags"],
        "parameter_regime": row["coordinate"]["alphabet"],
        "observed": row["observed"],
        "trajectory_signature": {
            "rise_then_release": row.get("rise_then_release"),
            "rise_then_release_excess": row.get("rise_then_release_excess"),
            "entropy_rate_bits": row.get("entropy_rate_bits"),
            "halt_mass": row.get("halt_mass"),
            "mean_edge_density": row.get("mean_edge_density"),
        },
        "robustness_region": {
            "shift_min": row["shift_min"],
            "shift_max": row["shift_max"],
            "closing_min": row["closing_min"],
            "closing_max": row["closing_max"],
        },
        "symmetry_class": "lexicographically least labelling under S_N",
        "known_equivalent_grammars": row["count"],
        "notes": {
            "observed": row["observed"],
            "inferred": "not stored on the motif; inferences are written in the generation report",
            "speculative": "not stored on the motif",
        },
        "evaluation_vector": EVALUATION_VECTOR,
    }


def _select_motifs(rows: list[dict]) -> list[dict]:
    """Deterministic cap. The full family index remains in the generated jsonl."""
    chosen: list[dict] = []
    seen: set[str] = set()

    def add(row: dict) -> None:
        if row["motif_id"] in seen or len(chosen) >= 48:
            return
        seen.add(row["motif_id"])
        chosen.append(_motif_record(row))

    for row in rows:
        if "baseline-equivalent" in row["tags"]:
            add(row)
    structural = [row for row in rows if "structural" in row["tags"]]
    structural.sort(key=lambda row: (row["coordinate"]["cardinality"], -row["shift_max"], row["expressions"]))
    for row in structural[:12]:
        add(row)
    by_closing = sorted(
        rows,
        key=lambda row: abs(row["closing_max"] if row["closing_max"] is not None else 0.0),
        reverse=True,
    )
    for row in by_closing[:8]:
        add(row)
    with_excess = [row for row in rows if row.get("rise_then_release_excess") is not None]
    with_excess.sort(key=lambda row: abs(row["rise_then_release_excess"]), reverse=True)
    for row in with_excess[:8]:
        add(row)
    measure = [row for row in rows if "measure" in row["tags"]]
    measure.sort(key=lambda row: row["shift_max"], reverse=True)
    for row in measure[:4]:
        add(row)
    return chosen


def _write_exemplars(spec, n, factors, grammar, families, references, baseline_heavy, digest, out_dir, screens, baseline_rise):
    written = []
    edge_list = list(grammar.edge_list)
    seeds = list(spec.get("trajectory", {}).get("seeds", [0]))
    horizon = int(spec.get("trajectory", {}).get("horizon", 32))
    targets = []
    targets.append(("baseline", [], 0, [0]))
    if n == 3:
        for reference in references:
            if reference.get("in_grammar"):
                targets.append(("reference", [reference["canonical_expression"]], 0, seeds))
    # A few non-baseline minimal families.
    ranked = sorted(families.values(), key=lambda family: (family.cardinality, family.k_max, family.expressions))
    added = 0
    for family in ranked:
        if family.equivalent_to_baseline:
            continue
        if added >= 4:
            break
        targets.append(("family", list(family.expressions), 0, [0]))
        added += 1
    complete = (1 << edge_count(n)) - 1
    for label, expressions, _seed, seed_list in targets:
        constraints = tuple(parse_expression(text, n) for text in expressions)
        kernel = build_kernel(n, Choreography(0, 0, constraints), factors)
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
                )
                record["n"] = n
                record["alphabet"] = spec["alphabet"]
                record["expressions"] = list(expressions)
                record["label"] = label
                record["initial_name"] = initial_name
                path = out_dir / "exemplars" / f"{record['run_id']}.json"
                _write_json(path, record)
                written.append(
                    {
                        "run_id": record["run_id"],
                        "label": label,
                        "initial": initial_name,
                        "seed": seed,
                        "expressions": expressions,
                        "path": str(path),
                    }
                )
    return written


def _publish(summary, spec, publish_root: Path, out_dir: Path) -> None:
    manifest = publish_root / "experiments" / "manifests"
    manifest.mkdir(parents=True, exist_ok=True)
    experiment = spec["experiment_id"]
    _write_json(manifest / f"{experiment}-summary.json", summary)
    tables = publish_root / "reports" / "tables"
    tables.mkdir(parents=True, exist_ok=True)
    catalogue = publish_root / "catalogue"
    catalogue.mkdir(parents=True, exist_ok=True)
    exemplars = publish_root / "exemplars"
    exemplars.mkdir(parents=True, exist_ok=True)
    for path in out_dir.glob("singles-*.csv"):
        target = tables / f"{experiment}-{path.name}"
        target.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    for path in out_dir.glob("families-*.jsonl"):
        if path.stat().st_size <= FAMILY_INDEX_COMMIT_LIMIT_BYTES:
            target = catalogue / f"{experiment}-{path.name}"
            target.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    motif_dir = out_dir / "motifs"
    if motif_dir.exists():
        published_motifs = catalogue / "motifs"
        published_motifs.mkdir(parents=True, exist_ok=True)
        for path in motif_dir.glob("*.json"):
            target = published_motifs / f"{experiment}-{path.name}"
            target.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    # Pedagogical and baseline exemplars are small enough to keep.
    for path in (out_dir / "exemplars").glob("*.json"):
        record = json.loads(path.read_text(encoding="utf-8"))
        if record.get("label") in {"baseline", "reference", "family"} and record.get("seed") == 0:
            target = exemplars / path.name
            target.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        elif record.get("label") == "reference" and record.get("n") == 3:
            target = exemplars / path.name
            target.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")


def _write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_json_ready(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(_json_ready(row), sort_keys=True) + "\n")


def _write_singles(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    # Drop the internal coverage leak if a row was nested. Rows are flat dicts.
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _json_ready(row[key]) for key in fieldnames})
