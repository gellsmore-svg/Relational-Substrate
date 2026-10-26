"""Scalable GT observables (gtobs), scale census (gtscale) and the gtkernel alphabet parameter."""

from __future__ import annotations

import math

import numpy as np
import pytest

from rs_constraint_lab import gt0, gte0a, gte0b, gtkernel, gtobs, gtscale
from rs_constraint_lab.gte0a import SOURCE, Chain
from rs_constraint_lab.gtobs_validate import compare, gth_stationary, plateau_modes
from rs_constraint_lab.state import edges
from rs_constraint_lab.weights import alphabet_factors

FAMILIES = gtkernel.all_e0_components()
DESIGN_CELLS = [
    ("NULL", "none"),
    ("CSPH", "strong_favour+weak_favour"),
    ("CSPF", "strong_favour+weak_suppress"),
    ("PATHF", "weak_favour"),
    ("PATHH", "weak_favour"),
    ("CLOSEW", "weak_favour"),
    ("COMPETE", "strong_favour+strong_favour"),
]


def reference_chain(family, grade, n, mode):
    return gte0a.chain_from_kernel(gte0a.build(family, grade, n, mode, FAMILIES), gt0.start_state(n, mode))


def fast_chain(family, grade, n, mode, factors=None):
    chain, _ = gtkernel.reachable_chain(n, mode, FAMILIES[family][grade], factors)
    return chain


# --- distances -----------------------------------------------------------------


@pytest.mark.parametrize("n,mode", [(4, "FREE"), (5, "FREE"), (5, "HELD"), (6, "HELD")])
def test_source_distances_match_breadth_first_search(n, mode):
    states = gtkernel.candidate_states(n, mode)
    D = gtobs.source_distances(states, n)
    edge_list = edges(n)
    for i in range(0, len(states), max(1, len(states) // 700)):
        for p in range(n):
            ref = gt0.distance_to_source(int(states[i]), n, edge_list, p)
            assert (D[i, p] < 0) == math.isinf(ref)
            if not math.isinf(ref):
                assert D[i, p] == ref


def test_source_distances_edge_cases():
    n = 6
    slots = len(edges(n))
    empty, complete = np.array([0], dtype=np.int64), np.array([(1 << slots) - 1], dtype=np.int64)
    assert gtobs.source_distances(empty, n)[0].tolist() == [0, 0, 0, -1, -1, -1]
    assert gtobs.source_distances(complete, n)[0].tolist() == [0, 0, 0, 1, 1, 1]
    index = {pair: i for i, pair in enumerate(edges(n))}
    chain_state = (1 << index[(2, 3)]) | (1 << index[(3, 4)]) | (1 << index[(4, 5)])
    assert gtobs.source_distances(np.array([chain_state], dtype=np.int64), n)[0].tolist() == [0, 0, 0, 1, 2, 3]


# --- class regime -----------------------------------------------------------------


def test_class_regime_on_synthetic_chains():
    # 0 <-> 1 -> 2 (absorbing): reducible with an absorbing state
    W = np.array([[1.0, 0.0], [1.0, 1.0], [0.0, 0.0]])
    T = np.array([[1, -1], [0, 2], [-1, 1]])
    r = gtobs.class_regime(Chain(2, np.array([0, 1, 2]), W, T), 0)
    assert r["regime"] == "absorbing" and r["absorbing_state_count"] == 1 and r["recurrent_class_sizes"] is None
    # 0 -> 1 <-> 2 with no zero-rate state: transient start, mixed
    W = np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 1.0]])
    T = np.array([[1, -1], [-1, 2], [-1, 1]])
    r = gtobs.class_regime(Chain(2, np.array([0, 1, 2]), W, T), 0)
    assert r["regime"] == "mixed" and r["absorbing_state_count"] == 0
    # 0 <-> 1: irreducible
    W = np.array([[1.0], [2.0]])
    T = np.array([[1], [0]])
    r = gtobs.class_regime(Chain(1, np.array([0, 1]), W, T), 0)
    assert r == {"absorbing_state_count": 0, "irreducible": True, "recurrent_class_sizes": [2], "regime": "recurrent"}


@pytest.mark.parametrize("mode", ["HELD", "FREE"])
def test_class_regime_matches_class_structure(mode):
    for family, grades in FAMILIES.items():
        for grade in grades:
            kernel = gte0a.build(family, grade, 4, mode, FAMILIES)
            states = gt0.reachable(kernel, gt0.start_state(4, mode))
            structure = gt0.class_structure(kernel, states)
            chain = fast_chain(family, grade, 4, mode)
            r = gtobs.class_regime(chain, gtobs.start_index(chain, 4, mode))
            single = len(structure["recurrent_classes"]) == 1 and len(structure["recurrent_classes"][0]) == len(states)
            assert r["irreducible"] == single
            assert r["absorbing_state_count"] == len(structure["absorbing_states"])


# --- stationary law ------------------------------------------------------------------


@pytest.mark.parametrize("family,grade", DESIGN_CELLS)
@pytest.mark.parametrize("mode", ["HELD", "FREE"])
def test_iterative_stationary_matches_dense(family, grade, mode):
    chain = fast_chain(family, grade, 5, mode)
    dense = gte0a.stationary(chain)
    it = gtobs.stationary(chain, gtobs.start_index(chain, 5, mode))
    assert it["resolved"] and it["cross_check_l1"] < 1e-12
    assert np.abs(it["ct"] - dense["ct"]).sum() < 1e-12


def test_iterative_stationary_has_high_relative_accuracy_on_rare_states():
    chain = fast_chain("PATHF", "weak_favour", 5, "HELD")
    referee = gth_stationary(chain)["jump"]
    it = gtobs.stationary(chain, gtobs.start_index(chain, 5, "HELD"))["jump"]
    assert referee.min() < 1e-11
    assert float((np.abs(it - referee) / referee).max()) < 1e-12


def test_gth_referee_matches_dense_on_ordinary_cell():
    chain = fast_chain("CSPH", "strong_favour+weak_favour", 5, "HELD")
    assert np.abs(gth_stationary(chain)["ct"] - gte0a.stationary(chain)["ct"]).max() < 1e-14


def test_stationary_reports_unresolved_on_zero_rate():
    W = np.array([[1.0], [0.0]])
    T = np.array([[1], [0]])
    out = gtobs.stationary(Chain(1, np.array([0, 1]), W, T), 0)
    assert out["resolved"] is False


# --- channel equivalence with the E0 implementation --------------------------------------


@pytest.mark.parametrize("family,grade", DESIGN_CELLS)
def test_held_channels_match_e0(family, grade):
    n, mode = 5, "HELD"
    kernel = gte0a.build(family, grade, n, mode, FAMILIES)
    states = gt0.reachable(kernel, gt0.start_state(n, mode))
    chain = gte0a.chain_from_kernel(kernel, gt0.start_state(n, mode))
    stat = gte0a.stationary(chain)
    D = gtobs.source_distances(chain.states, n)
    for law, unit in ((stat["jump"], False), (stat["ct"], True)):
        ref = gt0.held_observables(kernel, states, law, n, per_unit_time=unit)
        assert compare(ref, gtobs.held_observables(chain, law, n, D, per_unit_time=unit)) == []
    ref = gte0a.shell_activity(chain, stat["ct"], stat["jump"], n)
    assert compare(ref, gtobs.shell_activity(chain, stat["ct"], stat["jump"], n, D)) == []


@pytest.mark.parametrize("family,grade", DESIGN_CELLS)
@pytest.mark.parametrize("mode", ["HELD", "FREE"])
def test_event_order_class_table_and_free_channels_match_e0(family, grade, mode):
    n = 5
    chain = reference_chain(family, grade, n, mode)
    stat = gte0a.stationary(chain)
    ref = gte0a.event_order(chain, stat["jump"], n, mode)
    assert compare({"e": ref}, {"e": gtobs.event_order(chain, stat["jump"], n, mode)}) == []
    arrays = gte0a.structure_arrays(chain, n)
    table, sym = gtobs.class_table(chain, stat["ct"], stat["jump"], n, mode, gtobs.structure_arrays(chain, n))
    ref_table, ref_sym = gte0a.class_table(chain, stat["ct"], stat["jump"], n, mode, arrays)
    assert compare(ref_table, table) == []
    assert abs(sym - ref_sym) < 1e-15
    if mode == "FREE":
        states = [int(s) for s in chain.states]
        assert compare(gt0.free_observables(states, stat["ct"], n), gtobs.free_observables(chain, stat["ct"], gtobs.structure_arrays(chain, n))) == []


@pytest.mark.parametrize("family,grade", DESIGN_CELLS)
@pytest.mark.parametrize("mode", ["HELD", "FREE"])
def test_autocorrelation_series_matches_dense(family, grade, mode):
    n = 5
    chain = reference_chain(family, grade, n, mode)
    stat = gte0a.stationary(chain)
    arrays = gte0a.structure_arrays(chain, n)
    functions = {"edges": arrays["edges"].astype(float), "triangles": arrays["triangles"].astype(float), "degree_v3": arrays["degree"][:, 3].astype(float)}
    ref = gte0a.autocorrelation_times(chain, stat["ct"], stat["mean_rate_ct"], functions)
    new = gtobs.autocorrelation_times(chain, stat["ct"], stat["jump"], stat["mean_rate_ct"], functions)
    assert not new["diagnostics"]["cap_reached"]
    assert compare(ref, new["taus"], rel_tol=1e-9) == []


def test_autocorrelation_null_is_one_half():
    """NULL: each slot toggles at rate 1, so an edge indicator decorrelates as exp(-2t)."""
    chain = fast_chain("NULL", "none", 5, "FREE")
    stat = gtobs.stationary(chain, 0)
    bit = ((chain.states >> 0) & 1).astype(float)
    out = gtobs.autocorrelation_times(chain, stat["ct"], stat["jump"], stat["mean_rate_ct"], {"bit0": bit})
    assert abs(out["taus"]["bit0"]["time"] - 0.5) < 1e-12


def test_constant_function_has_no_autocorrelation_time():
    chain = fast_chain("CSPH", "strong_favour+weak_favour", 5, "HELD")
    stat = gtobs.stationary(chain, gtobs.start_index(chain, 5, "HELD"))
    out = gtobs.autocorrelation_times(chain, stat["ct"], stat["jump"], stat["mean_rate_ct"], {"one": np.ones(len(chain.states))})
    assert out["taus"]["one"] is None


# --- symmetry classes ----------------------------------------------------------------------


@pytest.mark.parametrize("n,expected", [(4, 11), (5, 34), (6, 156)])
def test_free_isomorphism_class_counts(n, expected):
    """Unlabelled graphs on n vertices (OEIS A000088): 11, 34, 156."""
    states = gtkernel.candidate_states(n, "FREE")
    canonical, _ = gtobs.canonical_labels(states, n, "FREE")
    assert len(np.unique(canonical)) == expected


def test_permutation_tables_match_reference():
    n = 6
    states = gtkernel.candidate_states(n, "FREE")[::37]
    for perm in gte0a.group_permutations(n, "FREE")[::53]:
        assert np.array_equal(gtobs.permute_codes(states, gtobs.permutation_tables(n, perm)), gte0a.permuted_codes(states, n, perm))


def test_canonical_labels_reject_unclosed_class():
    states = np.array([0, 1], dtype=np.int64)
    with pytest.raises(gte0a.E0AError):
        gtobs.canonical_labels(states, 4, "FREE", np.array([0.5, 0.5]))


# --- additions --------------------------------------------------------------------------------


def test_hub_structure_ties():
    n = 5
    slots = len(edges(n))
    index = {pair: i for i, pair in enumerate(edges(n))}
    star = sum(1 << index[(0, v)] for v in range(1, n))
    states = np.array([0, (1 << slots) - 1, star], dtype=np.int64)
    chain = Chain(slots, states, np.ones((3, slots)), np.zeros((3, slots), dtype=np.int64))
    deg = gtobs.structure_arrays(chain, n)["degree"]
    for i, (top, tied) in enumerate([(0, n), (n - 1, n), (n - 1, 1)]):
        law = np.zeros(3)
        law[i] = 1.0
        out = gtobs.hub_structure(deg, law, n, "HELD")
        assert out["max_degree_distribution"][str(top)] == 1.0
        assert out["tied_hub_count_distribution"][str(tied)] == 1.0
    law = np.array([0.0, 0.0, 1.0])
    out = gtobs.hub_structure(deg, law, n, "HELD")
    assert out["hub_includes_source"] == 1.0 and out["hub_probe_only"] == 0.0


@pytest.mark.parametrize("n", [5, 6])
def test_null_attachment_margins_are_zero(n):
    """Uniform law: E[a | k] = r0 k exactly, so both margins vanish."""
    chain = fast_chain("NULL", "none", n, "HELD")
    stat = gtobs.stationary(chain, gtobs.start_index(chain, n, "HELD"))
    D = gtobs.source_distances(chain.states, n)
    out = gtobs.held_additions(chain, stat["ct"], stat["jump"], n, D, gtobs.structure_arrays(chain, n))
    for clock in ("continuous", "jump"):
        assert abs(out[clock]["attachment_margin"]) < 1e-12
        assert abs(out[clock]["attachment_margin_null_density_standardised"]) < 1e-12
        assert abs(sum(out[clock]["detached_probe_count_distribution"].values()) - 1.0) < 1e-12


def test_attachment_margin_identity_on_published_cell():
    n = 6
    chain = fast_chain("CSPH", "strong_favour+weak_favour", n, "HELD")
    r, _ = gtobs.analyse(chain, family="CSPH", grade="strong_favour+weak_favour", n=n, mode="HELD", families=FAMILIES, with_trajectories=False, with_autocorrelation=False, hub_frame=False)
    held = r["held_continuous"]
    assert abs(r["e1_additions"]["held"]["continuous"]["attachment_margin"] - (held["attachment_fraction"] - held["null_attachment_fraction"])) < 1e-14


def test_witness_census_is_a_distribution():
    chain = fast_chain("CSPH", "strong_favour+weak_favour", 5, "HELD")
    stat = gtobs.stationary(chain, gtobs.start_index(chain, 5, "HELD"))
    census = gtobs.witness_census(chain, stat["jump"], 5, FAMILIES["CSPH"]["strong_favour+weak_favour"])
    for row in census.values():
        assert abs(sum(row["witness_distribution"].values()) - 1.0) < 1e-12
        assert 0.0 < row["event_share"] <= 1.0


def test_tie_aware_modes():
    assert plateau_modes({"0": 0.25, "1": 0.25, "2": 0.1}) == {0, 1}
    assert plateau_modes({"0": 0.1, "1": 0.3, "2": 0.1}) == {1}


# --- full analysis -----------------------------------------------------------------------------


def test_analyse_reproduces_published_held_n5_cell():
    import json
    from pathlib import Path

    tables = json.loads((Path(__file__).resolve().parents[2] / "gravity-time/reports/round-e0b-tables.json").read_text())
    item_id = "HELD-N5-CSPH-strong_favour+weak_favour"
    ref = tables["results"][item_id]
    chain = fast_chain("CSPH", "strong_favour+weak_favour", 5, "HELD")
    new, trajectories = gtobs.analyse(chain, family="CSPH", grade="strong_favour+weak_favour", n=5, mode="HELD", families=gte0b.FAMILIES, item_id=item_id, round_id=gte0b.ROUND_ID)
    assert compare(ref, new) == []
    assert len(trajectories["trajectories"]) == gte0a.TRAJECTORIES_PER_CELL


def test_trajectory_summary_matches_e0():
    chain = reference_chain("CSPH", "strong_favour+weak_favour", 5, "HELD")
    arrays = gte0a.structure_arrays(chain, 5)
    start = gtobs.start_index(chain, 5, "HELD")
    path = gte0a.sample_trajectory(chain, start, 12345, 300)
    assert gtobs.trajectory_summary(chain, path, arrays, start) == gte0a.trajectory_summary(chain, path, arrays, start)


# --- gtkernel alphabet ---------------------------------------------------------------------------


@pytest.mark.parametrize("alphabet", ["W3", "W16"])
@pytest.mark.parametrize("family,grade", [("CSPH", "strong_favour+weak_favour"), ("PATHF", "weak_suppress"), ("CLOSEW", "weak_favour")])
def test_alphabet_parameter_matches_build_kernel(alphabet, family, grade):
    from rs_constraint_lab.kernel import Choreography, build_kernel

    factors = alphabet_factors(alphabet)
    n, mode = 5, "HELD"
    ref = gte0a.chain_from_kernel(build_kernel(n, Choreography(0, 0, gte0a.rules_for(family, grade, n, mode, FAMILIES)), factors), gt0.start_state(n, mode))
    fast = fast_chain(family, grade, n, mode, factors)
    assert np.array_equal(ref.states, fast.states) and np.array_equal(ref.T, fast.T)
    assert np.allclose(ref.W, fast.W, rtol=1e-14, atol=0)


def test_default_alphabet_is_w4():
    a = fast_chain("CSPH", "strong_favour+weak_favour", 5, "HELD")
    b = fast_chain("CSPH", "strong_favour+weak_favour", 5, "HELD", alphabet_factors("W4"))
    assert np.array_equal(a.W, b.W)


# --- scale census ---------------------------------------------------------------------------------


@pytest.mark.parametrize("n", [5, 6])
def test_scale_census_matches_analytic_free_means(n):
    expected = {"close_form": (n - 2) / 4, "adj_form": n - 2, "path_form": (n - 2) * (n - 3) / 2}
    for kind, mean in expected.items():
        dist = gtscale.witness_distribution(n, "FREE", kind)
        assert abs(dist["mean"] - mean) < 1e-12
        assert dist["max_observed"] == dist["max_possible"] == gtscale.max_witnesses(kind, n)


def test_path_max_witnesses():
    assert [gtscale.max_witnesses("path_form", n) for n in (5, 6, 7)] == [12, 24, 40]


def test_null_baselines_held_n5():
    out = gtscale.null_baselines(5, "HELD")
    assert out["null_attachment_fraction"] == 6 / 7
    assert abs(sum(out["probe_distance_distribution"].values()) - 1.0) < 1e-12
    assert out["max_finite_distance"] == 2
