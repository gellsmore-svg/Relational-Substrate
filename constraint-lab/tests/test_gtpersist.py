"""Proof fixtures for GT-P009 persistence observables (synthetic chains and N <= 4 only; no E5A cell)."""

from __future__ import annotations

import math

import numpy as np
import pytest

from rs_constraint_lab import gt0, gtkernel, gtobs
from rs_constraint_lab import gtpersist as G
from rs_constraint_lab.gte0a import Chain
from rs_constraint_lab.state import edges

PCOMP = [("path_form", "weak_favour"), ("path_dissolve", "weak_favour")]
PATHF = [("path_form", "weak_suppress")]
PATHH = [("path_dissolve", "weak_favour")]
CSPH = [("close_form", "strong_favour"), ("path_dissolve", "weak_favour")]
CLOSEW = [("close_form", "weak_favour")]


def law(chain):
    st = gtkernel.stationary_sparse(chain)
    assert st["resolved"]
    return st["ct"]


def free(n, components, factors=None):
    chain, _ = gtkernel.reachable_chain(n, "FREE", components, factors)
    return chain


def binom_pmf(n, k):
    return math.comb(n, k) / 2**n


# --- two-state chain ------------------------------------------------------------


def test_two_state_episode_lifetimes():
    a, b = 3.0, 0.5
    chain = Chain(1, np.array([0, 1]), np.array([[a], [b]]), np.array([[1], [0]]))
    ct = np.array([b, a]) / (a + b)
    r = G.episode_statistics(chain, ct, np.array([False, True]))
    assert r["lifetime_ct"] == pytest.approx(1 / b)
    assert r["off_lifetime_ct"] == pytest.approx(1 / a)
    assert r["lifetime_jump"] == pytest.approx(1.0)
    assert r["recurrence_entry_to_entry_ct"] == pytest.approx(1 / a + 1 / b)
    assert r["flux_balance_relative"] < 1e-15


# --- NULL closed forms (independent unit-rate bits) ------------------------------------


def null_closed_forms(n):
    m = len(edges(n))
    s = n - 2
    out = {"I_TRI": (1 / 8, 3 / 8, None), "I_STAR": (1 / 8, 3 / 8, None), "I_2PATH": (1 / 4, 2 / 4, None)}
    pi_tri = (1 - 0.75**s) / 2
    out["F_TRI"] = (pi_tri, pi_tri + 0.5 * s * 0.25 * 0.75 ** (s - 1) * 2, 0.5 * s * (1 - 0.75 ** (s - 1)))
    d = [binom_pmf(n - 1, k) for k in range(n)]
    out["F_STAR"] = (sum(d[3:]), 3 * d[3] if n > 3 else 0.0, sum(d[k] * ((n - 1 - k) + k * (k >= 4)) for k in range(3, n)))
    out["F_2PATH"] = (sum(d[2:]), 2 * d[2], sum(d[k] * ((n - 1 - k) + k * (k >= 3)) for k in range(2, n)))
    return m, out


@pytest.mark.parametrize("n", [4])
def test_null_closed_forms(n):
    chain = free(n, [])
    ct = law(chain)
    m, forms = null_closed_forms(n)
    for p in G.PREDICATES:
        r = G.analyse_predicate(chain, ct, n, p, G.primary_instance(p))
        prev, J, omega_flux = forms[p]
        assert r["prevalence_ct"] == pytest.approx(prev, abs=1e-14)
        assert r["entries_per_unit_time"] == pytest.approx(J, abs=1e-14)
        assert r["lifetime_ct"] == pytest.approx(prev / J)
        assert r["lifetime_jump"] == pytest.approx(m * prev / J)  # q = M everywhere
        if omega_flux is not None:
            assert r["omega"] == pytest.approx(omega_flux / J, abs=1e-13)
    e = G.edge_episode(chain, ct, n, 0, 1)
    assert e["lifetime_ct"] == pytest.approx(1.0) and e["lifetime_jump"] == pytest.approx(m)


def test_small_n_degeneracies():
    chain = free(3, [])
    ct = law(chain)
    star = G.analyse_predicate(chain, ct, 3, "F_STAR", (0,))
    assert star["classification"] == "absent"  # degree <= 2 at N=3
    tri = G.analyse_predicate(chain, ct, 3, "F_TRI", (0, 1))
    assert tri["omega"] == 0.0  # one possible completer: no replacement is possible
    chain4 = free(4, PATHF)
    s4 = G.analyse_predicate(chain4, law(chain4), 4, "F_STAR", (0,))
    assert s4["omega"] == 0.0  # degree 3 is the maximum at N=4


# --- intact-motif structural limitation ---------------------------------------------


@pytest.mark.parametrize("components", [PATHF, PATHH, CSPH, PCOMP, CLOSEW])
def test_intact_required_edges_never_turn_over(components):
    chain = free(4, components)
    ct = law(chain)
    for p in G.INTACT:
        r = G.analyse_predicate(chain, ct, 4, p, G.primary_instance(p))
        assert r["required_edge_internal_flux"] == 0.0
        assert r["omega"] == 0.0
        assert r["required_edge_exit_share"] == pytest.approx(1.0)


def test_flexible_predicates_survive_incident_toggles():
    n = 5
    star = sum(1 << G.slot(n, 0, v) for v in (1, 2, 3))
    plus = star | (1 << G.slot(n, 0, 4))
    states = np.array([star, plus], dtype=np.int64)
    assert G.predicate_mask(states, n, "F_STAR", (0,)).all()
    assert G.predicate_mask(states, n, "F_2PATH", (0,)).all()
    assert G.eligible_toggles(states, n, "F_STAR", (0,))[0, G.slot(n, 0, 4)]
    assert not G.predicate_mask(states, n, "I_STAR", (0, 1, 2, 4))[0]
    # a triangle completer replaced by another while the anchor 01 stays
    t1 = sum(1 << G.slot(n, a, b) for a, b in ((0, 1), (0, 2), (1, 2), (0, 3)))
    t2 = t1 | (1 << G.slot(n, 1, 3))
    t3 = t2 & ~(1 << G.slot(n, 0, 2))
    trio = np.array([t1, t2, t3], dtype=np.int64)
    assert G.predicate_mask(trio, n, "F_TRI", (0, 1)).all()
    elig = G.eligible_toggles(trio, n, "F_TRI", (0, 1))
    assert elig[0, G.slot(n, 1, 3)] and elig[1, G.slot(n, 0, 2)]
    assert not elig[0, G.slot(n, 2, 3)]  # not incident on the anchor


# --- flux identities and clocks -------------------------------------------------------


def random_chain(seed, n=4):
    rng = np.random.default_rng(seed)
    m = len(edges(n))
    states = np.arange(1 << m, dtype=np.int64)
    W = rng.uniform(0.1, 3.0, size=(len(states), m))
    T = states[:, None] ^ (1 << np.arange(m))[None, :]
    return Chain(m, states, W, T)


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_entry_equals_exit_flux_and_first_passage(seed):
    chain = random_chain(seed)
    ct = law(chain)
    A = G.predicate_mask(chain.states, 4, "F_2PATH", (0,))
    r = G.episode_statistics(chain, ct, A)
    assert r["flux_balance_relative"] < 1e-12
    assert r["jump_length_identity_gap"] < 1e-12
    fp = G.residual_lifetimes(chain, ct, A)
    assert fp["resolved"]
    assert fp["entrance_mean_life_ct"] == pytest.approx(r["lifetime_ct"], rel=1e-10)
    assert fp["entrance_mean_life_jump"] == pytest.approx(r["lifetime_jump"], rel=1e-10)
    # occupation-sampled residual life is a different quantity: Palm bounds
    assert fp["occupation_residual_life_ct"] >= 0.5 * r["lifetime_ct"] - 1e-12
    assert fp["occupation_residual_life_jump"] >= 0.5 * (r["lifetime_jump"] + 1) - 1e-12


def test_ct_jump_conversion_uses_rate_weighted_law():
    chain = free(4, PATHH)
    ct = law(chain)
    A = G.predicate_mask(chain.states, 4, "I_2PATH", G.primary_instance("I_2PATH"))
    r = G.episode_statistics(chain, ct, A)
    nu = ct * chain.rates / (ct @ chain.rates)
    assert r["prevalence_jump"] == pytest.approx(float(nu[A].sum()))
    assert r["lifetime_jump"] == pytest.approx(r["prevalence_jump"] / r["entries_per_event"])


def test_uniform_rate_rescaling():
    chain = free(4, CSPH)
    ct = law(chain)
    scaled = Chain(chain.n_slots, chain.states, 7.0 * chain.W, chain.T)
    for p in ("F_TRI", "I_TRI"):
        a = G.analyse_predicate(chain, ct, 4, p, G.primary_instance(p))
        b = G.analyse_predicate(scaled, ct, 4, p, G.primary_instance(p))
        assert b["lifetime_ct"] == pytest.approx(a["lifetime_ct"] / 7.0)
        assert b["lifetime_jump"] == pytest.approx(a["lifetime_jump"])
        assert b["omega"] == pytest.approx(a["omega"])


# --- PCOMP: uniform CT law is not uniform kinetics -------------------------------------


def test_pcomp_uniform_ct_law_but_different_jump_law_and_lifetimes():
    pc = free(4, PCOMP)
    nl = free(4, [])
    ct_pc, ct_nl = law(pc), law(nl)
    assert np.abs(ct_pc - ct_nl).max() < 1e-13
    nu_pc = ct_pc * pc.rates / (ct_pc @ pc.rates)
    assert np.abs(nu_pc - ct_nl).max() > 1e-3
    a = G.analyse_predicate(pc, ct_pc, 4, "I_2PATH", G.primary_instance("I_2PATH"))
    b = G.analyse_predicate(nl, ct_nl, 4, "I_2PATH", G.primary_instance("I_2PATH"))
    assert a["prevalence_ct"] == pytest.approx(b["prevalence_ct"], abs=1e-13)
    assert abs(a["prevalence_jump"] - b["prevalence_jump"]) > 1e-4
    assert abs(a["lifetime_ct"] - b["lifetime_ct"]) > 1e-4


# --- ND comparator ----------------------------------------------------------------


def test_nd_null_fixed_point():
    chain = free(4, [])
    ct = law(chain)
    p = G.density_profile(chain.states, ct, 6)
    nd, pi, info = G.nd_chain(4, p, float(ct @ chain.rates))
    assert info["activity_scale"] == pytest.approx(1.0)
    assert np.abs(nd.W - 1.0).max() < 1e-12
    assert np.abs(pi - ct).max() < 1e-15


def test_nd_nonuniform_profile():
    m = 6
    p = np.array([0.30, 0.02, 0.004, 0.08, 0.25, 0.05, 0.30])
    p /= p.sum()
    nd, pi, info = G.nd_chain(4, p, 9.5)
    assert info["detailed_balance_max_relative"] < 1e-12
    assert info["global_balance_relative"] < 1e-12
    assert info["density_l1_vs_target"] < 1e-12
    assert info["mean_rate_relative_gap"] < 1e-12
    st = gtkernel.stationary_sparse(nd)
    assert st["resolved"] and np.abs(st["ct"] - pi).sum() < 1e-9
    # uniform within each edge count
    k = np.array([int(s).bit_count() for s in nd.states])
    for j in range(m + 1):
        assert np.ptp(pi[k == j]) < 1e-15 * max(pi.max(), 1)
    # rates read only the edge count: label-covariant
    perm = (2, 0, 3, 1)
    codes = gtobs.permute_codes(nd.states, gtobs.permutation_tables(4, perm))
    assert np.array_equal(np.sort(nd.W[codes], axis=1), np.sort(nd.W, axis=1))


def test_nd_rare_interior_bin_is_flagged_and_analytic():
    p = np.array([0.30, 0.02, 1e-13, 0.08, 0.25, 0.05, 0.30])
    p /= p.sum()
    nd, pi, info = G.nd_chain(4, p, 9.5)
    assert "2" in info["rare_bins"]
    assert info["min_unscaled_transition_rate"] < 1e-11  # near-bottleneck: iterative solvers cannot confirm the law
    assert info["detailed_balance_max_relative"] < 1e-12 and info["global_balance_relative"] < 1e-12
    assert info["density_l1_vs_target"] < 1e-12


def test_nd_zero_bin_is_unresolved():
    r = G.nd_rates(np.array([0.5, 0.0, 0.5]))
    assert not r["resolved"] and r["zero_bins"] == [1]


def test_nd_jump_density_differs_from_target_jump_density():
    chain = free(4, PATHH)
    ct = law(chain)
    p = G.density_profile(chain.states, ct, 6)
    nd, pi, _ = G.nd_chain(4, p, float(ct @ chain.rates))
    assert np.abs(G.density_profile(nd.states, pi, 6) - p).sum() < 1e-12
    assert np.abs(G.jump_density(nd, pi, 4) - G.jump_density(chain, ct, 4)).sum() > 1e-6


# --- covariance ------------------------------------------------------------------


@pytest.mark.parametrize("components", [PATHF, CSPH])
def test_relabelled_instances_agree(components):
    chain = free(4, components)
    ct = law(chain)
    for p in G.PREDICATES:
        a = G.analyse_predicate(chain, ct, 4, p, G.primary_instance(p))
        b = G.analyse_predicate(chain, ct, 4, p, G.relabelled_instance(p, 4))
        for key in ("prevalence_ct", "lifetime_ct", "lifetime_jump", "omega"):
            assert b[key] == pytest.approx(a[key], rel=1e-10, abs=1e-15)


def test_hub_tie_rule_is_covariant():
    n = 4
    states = np.arange(1 << len(edges(n)), dtype=np.int64)
    h, _ = G.hub_weights(states, n)
    perm = (3, 1, 0, 2)
    codes = gtobs.permute_codes(states, gtobs.permutation_tables(n, perm))
    for v in range(n):
        assert np.array_equal(h[codes, perm[v]], h[:, v])
    assert np.allclose(h.sum(axis=1), 1.0)


# --- lagged hub --------------------------------------------------------------------


def test_lagged_hub_null_closed_forms():
    n, m = 4, 6
    chain = free(n, [])
    ct = law(chain)
    out = G.lagged_hub(chain, ct, n, (0, 1, 2, 4, 8, 16))
    for d in (1, 2, 4, 8, 16):
        assert out["continuous"][str(d)]["normalised_gap"] == pytest.approx(math.exp(-2 * d / m), rel=1e-12)
        assert out["jump"][str(d)]["normalised_gap"] == pytest.approx((1 - 2 / m) ** d, rel=1e-12)
        # NULL retention of an initially present edge: 1/2 + 1/2 e^{-2t}
        assert out["continuous"][str(d)]["hub_retention_fraction"] == pytest.approx(0.5 + 0.5 * math.exp(-2 * d / m), rel=1e-12)
    c = out["checks"]
    assert c["lumpability_defect_relative"] == 0.0 and c["row_sum_max_error"] < 1e-12 and c["lumped_vs_full_jump_max"] < 1e-12


@pytest.mark.parametrize("components", [PATHH, CSPH, PCOMP])
def test_lumpability_and_expm_checks_on_nonreversible_chains(components):
    chain = free(4, components)
    ct = law(chain)
    out = G.lagged_hub(chain, ct, 4, (0, 1, 2, 4, 8, 16))
    c = out["checks"]
    assert c["lumpability_defect_relative"] < 1e-14
    assert c["row_sum_max_error"] < 1e-10 and c["min_entry"] > -1e-12
    assert c["stationarity_l1"] < 1e-10 and c["semigroup_max"] < 1e-10
    assert c["lumped_vs_full_jump_max"] < 1e-12 and c["pair_permutation_covariance_max"] < 1e-12
    # comparison vertex degree is stationary-constant
    degs = [row["comparison_degree"] for row in out["continuous"].values()]
    assert np.ptp(degs) < 1e-10


def test_stiff_expm_matches_symmetrised_eigendecomposition():
    factors = {**{k: float(v) for k, v in gt0.FACTORS.items()}, "weak_favour": 2.0**6}
    chain = free(4, CLOSEW, factors)  # reversible (Gibbs), rates up to 2^12
    ct = law(chain)
    lump, reps = G.lump_index(chain.states, 4)
    Q, defect = G.lumped_generator(chain, lump, reps)
    assert defect < 1e-14
    pi_bar = np.bincount(lump, weights=ct)
    d = np.sqrt(pi_bar)
    S = (d[:, None] * Q) / d[None, :]
    S = 0.5 * (S + S.T)
    vals, vecs = np.linalg.eigh(S)
    t = 3.0 / float(ct @ chain.rates)
    exact = (vecs * np.exp(t * vals)) @ vecs.T
    exact = exact / d[:, None] * d[None, :]
    E, squarings = G.expm(t * Q)
    assert squarings > 0
    assert np.abs(E - exact).max() < 1e-9


def test_deterministic_reproduction():
    chain = free(4, PATHH)
    ct = law(chain)
    a = G.lagged_hub(chain, ct, 4, (0, 1, 2, 4, 8, 16))
    b = G.lagged_hub(chain, ct, 4, (0, 1, 2, 4, 8, 16))
    assert a["continuous"] == b["continuous"] and a["jump"] == b["jump"]
    r1 = G.analyse_predicate(chain, ct, 4, "F_TRI", (0, 1))
    r2 = G.analyse_predicate(chain, ct, 4, "F_TRI", (0, 1))
    assert r1 == r2


def test_closed_set_and_whole_space_classification():
    chain = Chain(1, np.array([0, 1]), np.array([[0.0], [0.0]]), np.array([[-1], [-1]]))
    ct = np.array([0.5, 0.5])
    assert G.episode_statistics(chain, ct, np.array([False, True]))["classification"] == "closed_or_absorbing"
    assert G.episode_statistics(chain, ct, np.array([True, True]))["classification"] == "whole_space"
    assert G.episode_statistics(chain, ct, np.array([False, False]))["classification"] == "absent"


def test_module_null_closed_forms_match_independent_derivation():
    for n in (4, 5, 6, 7):
        _, forms = null_closed_forms(n)
        mod = G.null_closed_forms(n)
        for p in G.PREDICATES:
            prev, J, omega_flux = forms[p]
            assert mod[p]["prevalence"] == pytest.approx(prev)
            assert mod[p]["flux"] == pytest.approx(J)
            if omega_flux is not None:
                assert mod[p]["omega_flux"] == pytest.approx(omega_flux)
