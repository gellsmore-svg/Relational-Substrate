"""Generation-0 correctness: states, kernels, orbits, replay, and two theorems."""

from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

from rs_constraint_lab.accounting import template_accounting
from rs_constraint_lab.constraints import FORM, Choreography, Constraint, parse_expression
from rs_constraint_lab.exact import long_run, period_of
from rs_constraint_lab.grammar import build_grammar, canonical_id_tuple, is_canonical_ids
from rs_constraint_lab.kernel import build_kernel, modal_map, support_map
from rs_constraint_lab.observables import heavy_observables, light_observables
from rs_constraint_lab.semantics import get_semantics
from rs_constraint_lab.spec import load_spec, validate_spec
from rs_constraint_lab.state import canonical_state, edge_count, n_states, relabel_state, edges, edge_index, permutations
from rs_constraint_lab.trajectory import replay_matches, sample_trajectory
from rs_constraint_lab.weights import alphabet_factors


def _kernel(n, constraints, alphabet="W4"):
    return build_kernel(n, Choreography(0, 0, tuple(constraints)), alphabet_factors(alphabet))


def _baseline(n, alphabet="W4"):
    return _kernel(n, [], alphabet)


def test_state_counts_match_the_hypercube():
    assert [n_states(n) for n in range(2, 8)] == [2, 8, 64, 1024, 32768, 2_097_152]
    assert [edge_count(n) for n in range(2, 7)] == [1, 3, 6, 10, 15]


def test_baseline_is_uniform_and_period_two():
    kernel = _baseline(3)
    for state, row in enumerate(kernel.successors):
        assert sum(prob for _nxt, prob in row) == 1
        assert len(row) == 3
        assert all(prob == pytest.approx(1 / 3) or prob.numerator == 1 for _nxt, prob in row)
        for nxt, prob in row:
            assert prob == __import__("fractions").Fraction(1, 3)
            assert (state ^ nxt).bit_count() == 1
    assert period_of(list(range(8)), kernel.successors) == 2
    ran = long_run(kernel, 0)
    assert ran["stationary_arithmetic"] == "rational"
    assert all(abs(ran["distribution"][state] - 1 / 8) < 1e-12 for state in range(8))
    heavy = heavy_observables(kernel, 4, 0)
    assert heavy["mean_edge_density"] == pytest.approx(0.5)
    assert heavy["entropy_rate_bits"] == pytest.approx(__import__("math").log2(3))
    assert heavy["reversibility_defect"] == pytest.approx(0, abs=1e-12)
    assert heavy["tv_from_uniform"] == pytest.approx(0, abs=1e-12)


def test_toggle_changes_edge_count_parity():
    kernel = _baseline(4)
    for state, row in enumerate(kernel.successors):
        for nxt, _prob in row:
            assert state.bit_count() % 2 != nxt.bit_count() % 2


def test_canonical_state_is_constant_on_orbits():
    n = 4
    edge_list = edges(n)
    index = edge_index(n)
    for state in (0, 1, 7, 18, 33, 63):
        canon = canonical_state(state, n)
        for perm in permutations(n):
            image = relabel_state(state, perm, edge_list, index)
            assert canonical_state(image, n) == canon


def test_constraint_and_set_orbits_agree():
    grammar = build_grammar(3, 3, ["prohibit", "strong_favour"])
    identity = grammar.image[0]
    assert identity == tuple(range(len(grammar.labelled)))
    for row in grammar.image:
        assert sorted(row) == list(range(len(grammar.labelled)))
    for i in range(0, len(grammar.labelled), 17):
        canon = canonical_id_tuple((i,), grammar.image)
        for row in grammar.image:
            assert canonical_id_tuple((row[i],), grammar.image) == canon
    pair = (0, 5)
    canon_pair = canonical_id_tuple(pair, grammar.image)
    for row in grammar.image:
        imaged = tuple(sorted(row[i] for i in pair))
        assert canonical_id_tuple(imaged, grammar.image) == canon_pair
    assert is_canonical_ids(canon_pair, grammar.image)


def test_expression_roundtrip_for_every_n4_pattern():
    grammar = build_grammar(4, 2, ["prohibit", "weak_favour", "strong_suppress"])
    for constraint in grammar.labelled:
        text = constraint.expression(list(grammar.edge_list))
        assert parse_expression(text, 4).key() == constraint.key()


def test_accounting_matches_the_generator():
    for n, k_max in ((2, 3), (3, 3), (4, 2)):
        weights = ["prohibit", "weak_suppress", "strong_favour"]
        grammar = build_grammar(n, k_max, weights)
        accounting = template_accounting(n, k_max, len(weights))
        assert accounting["labelled_constraints"] == len(grammar.labelled)
        assert accounting["raw_structural_templates"] == (
            accounting["removed_syntax_invalid"]
            + accounting["removed_redundant_normalisation"]
            + accounting["outside_k_bound"]
            + accounting["outside_a_bound"]
            + accounting["structural_normal_forms"]
        )
        assert accounting["outside_a_bound"] == 0


def test_n5_baseline_uses_iterative_components_and_stays_uniform():
    kernel = _baseline(5)
    light = light_observables(kernel, kernel)
    assert kernel.n_states == 1024
    assert light["n_recurrent"] == 1
    assert light["periods"] == [2]
    assert light["reachable_from_empty"] == 1024
    heavy = heavy_observables(kernel, 4, 0)
    assert heavy["stationary_arithmetic"] == "float64"
    assert heavy["stationary_residual"] < 1e-8
    assert heavy["mean_edge_density"] == pytest.approx(0.5, abs=1e-6)
    assert heavy["entropy_rate_bits"] == pytest.approx(math.log2(10), rel=1e-6)
    assert heavy["rise_then_release"] is None


def test_n2_positive_weights_match_the_baseline_and_prohibit_halts():
    baseline = _baseline(2)
    grammar = build_grammar(2, 3, ["strong_suppress", "weak_suppress", "weak_favour", "strong_favour", "prohibit"])
    for constraint in grammar.labelled:
        kernel = _kernel(2, [constraint])
        if constraint.weight == "prohibit":
            assert any(kernel.deadlock)
            assert kernel.successors != baseline.successors
        else:
            assert kernel.successors == baseline.successors
            assert not any(kernel.deadlock)


def test_closing_bias_counts_a_deadlocked_two_edge_state_as_zero():
    texts = []
    for a, b in ((0, 1), (0, 2), (1, 2)):
        texts.append(f"form({a}-{b}) => prohibit")
        texts.append(f"dissolve({a}-{b}) => prohibit")
    kernel = _kernel(3, [parse_expression(text, 3) for text in texts])
    light = light_observables(kernel, _baseline(3))
    assert light["n_deadlock"] == 8
    assert light["closing_bias"] == pytest.approx(-1 / 3)


def test_hand_computed_n3_prohibit_and_path_rule():
    # Edges: (0,1)=0, (0,2)=1, (1,2)=2.
    one_edge = Constraint(FORM, 0, (), "prohibit")
    kernel = _kernel(3, [one_edge])
    # From empty, AB cannot form. AC and BC form with equal weight.
    empty = dict(kernel.successors[0])
    assert 1 not in empty or empty.get(1, 0) == 0
    assert empty[2] == __import__("fractions").Fraction(1, 2)  # form edge 1 -> state 2
    assert empty[4] == __import__("fractions").Fraction(1, 2)  # form edge 2 -> state 4

    path = parse_expression("form(0-2) | present(0-1) & present(1-2) => prohibit", 3)
    kernel = _kernel(3, [path])
    # State with edges 0 and 2 present is 1+4=5. Closing edge 1 is forbidden.
    outgoing = dict(kernel.successors[5])
    assert outgoing.get(7, 0) == 0
    assert outgoing[5 ^ 1] == __import__("fractions").Fraction(1, 2)
    assert outgoing[5 ^ 4] == __import__("fractions").Fraction(1, 2)
    light = light_observables(kernel, _baseline(3))
    assert light["closing_bias"] < -0.1
    favour = parse_expression("form(0-2) | present(0-1) & present(1-2) => strong_favour", 3)
    favoured = _kernel(3, [favour])
    assert dict(favoured.successors[5])[7] == __import__("fractions").Fraction(4, 6)
    heavy = heavy_observables(favoured, 4, 0)
    assert heavy["reversibility_defect"] > 0
    assert heavy["triangle_mass"] != pytest.approx(1 / 8)


def test_geometric_alphabets_preserve_modes_and_change_magnitudes():
    text = "form(0-2) | present(0-1) & present(1-2) => strong_favour"
    constraint = parse_expression(text, 3)
    maps = {}
    supports = {}
    closing = {}
    for name in ("W4", "W3", "W16"):
        kernel = _kernel(3, [constraint], name)
        maps[name] = modal_map(kernel)
        supports[name] = support_map(kernel)
        closing[name] = dict(kernel.successors[5])[7]
    assert maps["W4"] == maps["W3"] == maps["W16"]
    assert supports["W4"] == supports["W3"] == supports["W16"]
    assert closing["W4"] != closing["W16"]
    assert closing["W4"] > __import__("fractions").Fraction(1, 3)
    assert closing["W16"] > closing["W4"]


def test_replay_is_deterministic_and_records_the_draw():
    constraint = parse_expression("form(0-2) | present(0-1) => strong_suppress", 3)
    kernel = _kernel(3, [constraint])
    kwargs = dict(
        kernel=kernel,
        constraints=(constraint,),
        factors=alphabet_factors("W4"),
        edge_list=edges(3),
        initial_state=0,
        seed=7,
        horizon=12,
        spec_hash="abc",
        constraint_set_id="def",
    )
    first = sample_trajectory(**kwargs)
    second = sample_trajectory(**kwargs)
    assert replay_matches(first, second)
    assert first["events"][0]["draw"] is not None
    assert first["prng"] == "python-random-MT19937"
    # A different seed diverges on this biased kernel, or is at least a different run id.
    other = sample_trajectory(**{**kwargs, "seed": 8})
    assert other["run_id"] != first["run_id"]


def test_halt_completion_is_marked_and_not_a_silent_toggle():
    constraints = [Constraint(FORM, edge, (), "prohibit") for edge in range(3)]
    kernel = _kernel(3, constraints)
    assert kernel.deadlock[0]
    assert kernel.completion == "self_loop_marked_kernel_undefined"
    assert kernel.successors[0] == ((0, __import__("fractions").Fraction(1)),)
    ran = long_run(kernel, 7)
    assert ran["distribution"][0] == pytest.approx(1)
    assert ran["periods"] == [1]


def test_hypergraph_is_not_compiled_into_pairs():
    semantics = get_semantics("hypergraph")
    with pytest.raises(NotImplementedError, match="not reduced to a collection of pairwise"):
        semantics.relation_slots(3)
    simplicial = get_semantics("simplicial")
    with pytest.raises(NotImplementedError, match="not identified with a hyperedge"):
        simplicial.relation_slots(3)


def test_spec_rejects_neutral_and_unknown_semantics(tmp_path):
    good = {
        "schema": "rs-constraint-lab.experiment/v1",
        "experiment_id": "tiny",
        "generation": 0,
        "semantics": "graph",
        "alphabet": "W4",
        "cells": [{"N": 2, "K_max": 1, "cardinalities": [1]}],
    }
    validate_spec(good)
    bad = dict(good)
    bad["weights"] = ["neutral"]
    with pytest.raises(ValueError, match="neutral"):
        validate_spec(bad)
    bad = dict(good)
    bad["semantics"] = "lattice"
    with pytest.raises(ValueError, match="unknown semantics"):
        validate_spec(bad)
    path = tmp_path / "spec.json"
    path.write_text(json.dumps(good), encoding="utf-8")
    assert load_spec(path)["experiment_id"] == "tiny"


def test_choreography_refuses_history():
    choreography = Choreography(1, 0, ())
    with pytest.raises(NotImplementedError):
        choreography.active(0, (), {})


def test_generation_000_spec_loads():
    spec = load_spec(Path(__file__).resolve().parents[1] / "experiments" / "specs" / "generation-000.json")
    assert spec["generation"] == 0
    assert spec["cells"][0]["N"] == 2


def test_relabelled_rules_share_a_canonical_id_and_polarity_does_not():
    grammar = build_grammar(3, 2, ["strong_suppress"])
    left = parse_expression("form(0-1) | present(0-2) => strong_suppress", 3)
    right = parse_expression("form(0-1) | present(1-2) => strong_suppress", 3)
    dissolve = parse_expression("dissolve(0-1) | present(0-2) => strong_suppress", 3)

    def locate(constraint):
        return next(i for i, item in enumerate(grammar.labelled) if item.key() == constraint.key())

    assert canonical_id_tuple((locate(left),), grammar.image) == canonical_id_tuple((locate(right),), grammar.image)
    assert canonical_id_tuple((locate(left),), grammar.image) != canonical_id_tuple((locate(dissolve),), grammar.image)
