"""Structural identity, exact fractions, count grammar, and combinadic shards."""

from __future__ import annotations

import itertools
import json

import pytest

from rs_constraint_lab.combinadic import next_combination, unrank_combination
from rs_constraint_lab.constraints import (
    parse_expression,
    structurally_simple,
)
from rs_constraint_lab.durable import atomic_write_json, read_json
from rs_constraint_lab.dynamics import (
    RelabelTables,
    canonical_tokens,
    classify_cancellation,
    family_ids,
    observed_post_release_new_edge,
)
from rs_constraint_lab.grammar import (
    build_grammar,
    grammar_statistics,
    labelled_simple_count,
)
from rs_constraint_lab.kernel import build_kernel
from rs_constraint_lab.observables import heavy_observables, light_observables
from rs_constraint_lab.spec import validate_spec
from rs_constraint_lab.weights import ENUMERATED_WEIGHTS, alphabet_factors
from rs_constraint_lab.constraints import Choreography


def _kernel(n, constraints):
    return build_kernel(n, Choreography(0, 0, tuple(constraints)), alphabet_factors("W4"))


def _spec(**overrides):
    data = {
        "schema": "rs-constraint-lab.experiment/v1",
        "experiment_id": "axis-check",
        "generation": 0,
        "semantics": "graph",
        "alphabet": "W4",
        "cells": [{"N": 2, "K_max": 1, "cardinalities": [1]}],
    }
    data.update(overrides)
    return data


def test_structural_identity_excludes_weight():
    favour = parse_expression("form(0-1) => strong_favour", 3)
    suppress = parse_expression("form(0-1) => strong_suppress", 3)
    assert favour.structural_key() == suppress.structural_key()
    assert favour.key() != suppress.key()
    assert structurally_simple((favour, suppress)) is False
    other = parse_expression("form(0-1) | present(0-2) => strong_suppress", 3)
    assert structurally_simple((favour, other)) is True


def test_a_max_filters_the_grammar_and_undeclared_axes_are_refused():
    empty = build_grammar(3, 1, ["prohibit"], a_max=1)
    assert empty.labelled == ()
    bounded = build_grammar(3, 3, ["prohibit"], a_max=2)
    edge_list = list(bounded.edge_list)
    assert bounded.labelled
    assert all(constraint.arity(edge_list) <= 2 for constraint in bounded.labelled)
    assert bounded.stats["edge_outside_a"] > 0
    with pytest.raises(ValueError, match="G=1"):
        validate_spec(_spec(G=1))
    with pytest.raises(ValueError, match="H=1"):
        validate_spec(_spec(H=1))
    with pytest.raises(ValueError, match="O=3"):
        validate_spec(_spec(O=3))
    with pytest.raises(ValueError, match="A_max"):
        validate_spec(_spec(cells=[{"N": 2, "K_max": 1, "A_max": True, "cardinalities": [1]}]))
    with pytest.raises(ValueError, match="composition"):
        validate_spec(_spec(composition="stacked-everywhere"))
    validate_spec(_spec())


def test_wedge_observables_stay_rational():
    wedge = parse_expression("form(0-2) | present(0-1) & present(1-2) => strong_favour", 3)
    kernel = _kernel(3, [wedge])
    heavy = heavy_observables(kernel, 4, 0)
    light = light_observables(kernel, _kernel(3, []))
    assert heavy["stationary_arithmetic"] == "rational"
    assert heavy["triangle_mass_exact"] == "11/64"
    assert heavy["mean_edge_density_exact"] == "13/24"
    assert light["closing_bias_exact"] == "1/9"
    assert isinstance(heavy["entropy_rate_bits"], float)


def test_relabelled_kernels_share_one_exact_family():
    left = parse_expression("form(0-1) | present(0-2) => strong_favour", 3)
    right = parse_expression("form(0-2) | present(0-1) => strong_favour", 3)
    tables = RelabelTables(3)
    left_ids = family_ids(3, canonical_tokens(_kernel(3, [left]), tables))
    right_ids = family_ids(3, canonical_tokens(_kernel(3, [right]), tables))
    assert left_ids["exact_kernel_family"] == right_ids["exact_kernel_family"]
    assert len(left_ids["exact_kernel_family"]) == 64
    assert left_ids["qualitative_family"] == right_ids["qualitative_family"]


def test_count_grammar_size_and_wedge_equivalence():
    stats = grammar_statistics(
        3,
        2,
        len(ENUMERATED_WEIGHTS),
        predicates=("edge", "count"),
        weight_names=ENUMERATED_WEIGHTS,
    )
    assert stats["edge_structural"] == 30
    assert stats["count_structural"] == 42
    assert stats["structural_normal_forms"] == 72
    assert stats["labelled_constraints"] == 360
    assert stats["count_tautology"] > 0
    assert stats["count_unsatisfiable"] > 0
    assert labelled_simple_count(72, 5, 1) == 360
    assert labelled_simple_count(72, 5, 2) == 63900
    grammar = build_grammar(
        3, 2, ENUMERATED_WEIGHTS, predicates=("edge", "count")
    )
    assert len(grammar.labelled) == 360
    texts = [grammar.expression(i) for i in range(len(grammar.labelled))]
    assert "form(0-1) | count>=3 => strong_favour" not in texts
    assert "form(0-1) | count<=2 => strong_favour" not in texts
    assert "dissolve(0-1) | count>=1 => strong_favour" not in texts
    assert "form(0-1) | count>=2 => strong_favour" in texts
    counted = parse_expression("form(0-1) | count>=2 => strong_favour", 3)
    wedge = parse_expression("form(0-1) | present(0-2) & present(1-2) => strong_favour", 3)
    assert _kernel(3, [counted]).successors == _kernel(3, [wedge]).successors
    parsed = parse_expression(counted.expression(list(grammar.edge_list)), 3)
    assert parsed.key() == counted.key()
    with pytest.raises(ValueError, match="at most one count"):
        parse_expression("form(0-1) | count>=1 & count<=2 => strong_favour", 3)


def test_cancellation_classes_and_post_release_flag():
    factors = alphabet_factors("W4")
    baseline = _kernel(3, [])
    global_set = (
        parse_expression("form(0-1) => strong_favour", 3),
        parse_expression("form(0-1) | present(0-2) => strong_suppress", 3),
        parse_expression("form(0-1) | absent(0-2) => strong_suppress", 3),
    )
    global_kernel = _kernel(3, global_set)
    assert classify_cancellation(3, global_set, factors, global_kernel, baseline) == "genuine_global"
    local_set = global_set[:2]
    local_kernel = _kernel(3, local_set)
    assert classify_cancellation(3, local_set, factors, local_kernel, baseline) == "local"
    inherited = (
        parse_expression("form(0-1) => strong_favour", 2),
        parse_expression("dissolve(0-1) => weak_favour", 2),
    )
    inherited_kernel = _kernel(2, inherited)
    assert classify_cancellation(2, inherited, factors, inherited_kernel, _kernel(2, [])) == "inherited_baseline"
    release = (parse_expression("dissolve(0-1) | count>=2 => strong_favour", 3),)
    assert observed_post_release_new_edge(_kernel(3, release), release, factors) is True
    formed = (parse_expression("form(0-1) | count>=1 => strong_favour", 3),)
    assert observed_post_release_new_edge(_kernel(3, formed), formed, factors) is False
    assert observed_post_release_new_edge(baseline, (), factors) is False


def test_combinadic_matches_itertools():
    for n, k in ((5, 2), (6, 3), (3, 1), (4, 0)):
        combos = list(itertools.combinations(range(n), k))
        for rank, combo in enumerate(combos):
            assert unrank_combination(rank, n, k) == combo
        if not combos:
            continue
        cursor = combos[0]
        for expected in combos[1:]:
            cursor = next_combination(cursor, n)
            assert cursor == expected
        assert next_combination(combos[-1], n) is None
    assert unrank_combination(0, 5, 2) == (0, 1)
    assert unrank_combination(4, 5, 2) == (1, 2)
    assert unrank_combination(9, 5, 2) == (3, 4)


def test_truncated_temporary_is_not_the_result(tmp_path):
    target = tmp_path / "result.json"
    atomic_write_json(target, {"ok": True})
    temporary = target.with_name("result.json.tmp")
    temporary.write_text("{truncated", encoding="utf-8")
    assert read_json(target) == {"ok": True}
    with pytest.raises(json.JSONDecodeError):
        read_json(temporary)
