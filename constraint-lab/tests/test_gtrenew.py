"""Proof fixtures for GT-P010 (E5B) observables: synthetic chains and N <= 4 kernels, plus a synthetic
N = 5 rule that is not one of the twelve E5B laws. No E5B scientific cell is evaluated here."""

from __future__ import annotations

import math

import numpy as np
import pytest

from rs_constraint_lab import gtkernel, gtobs
from rs_constraint_lab import gtpersist as G
from rs_constraint_lab import gtrenew as R
from rs_constraint_lab.gte0a import Chain
from rs_constraint_lab.state import edges

PCOMP = [("path_form", "weak_favour"), ("path_dissolve", "weak_favour")]
CLOSEW = [("close_form", "weak_favour")]
PATHF = [("path_form", "weak_suppress")]


def law(chain):
    st = gtkernel.stationary_sparse(chain)
    assert st["resolved"]
    return st["ct"]


def free(n, components):
    chain, _ = gtkernel.reachable_chain(n, "FREE", components)
    return chain


def full_chain(n, rate_fn):
    """Synthetic full-space chain with W(x,e) = rate_fn(bits, e)."""
    m = len(edges(n))
    states = np.arange(1 << m, dtype=np.int64)
    x = G.bits(states, n)
    W = np.array([[rate_fn(x[i], e) for e in range(m)] for i in range(len(states))], dtype=float)
    T = states[:, None] ^ (1 << np.arange(m))[None, :]
    return Chain(m, states, W, T)


def neighbourhood_rate(n):
    """PCOMP-like synthetic control: rate of toggling e is 2^(present slots sharing a vertex with e).

    The rate does not depend on e's own state, so W(x,e) = W(x xor e, e): the uniform law is
    stationary (detailed balance) while rates are heterogeneous within each edge-count layer.
    """
    pairs = edges(n)
    adj = [[f for f, q in enumerate(pairs) if f != e and set(q) & set(p)] for e, p in enumerate(pairs)]
    return lambda xb, e: 2.0 ** int(sum(xb[f] for f in adj[e]))


# --- analytic NULL control --------------------------------------------------------


@pytest.mark.parametrize("n", [3, 4])
def test_null_local_count_is_local_slots_times_ct_lifetime(n):
    chain = free(n, [])
    ct = law(chain)
    for p in R.FLEXIBLE:
        v = G.primary_instance(p)
        if p == "F_TRI" and n < 3:
            continue
        A = G.predicate_mask(chain.states, n, p, v)
        if A.all() or not A.any():
            continue
        lc = R.local_clock(chain, ct, A, R.local_mask(n, p, v))
        ep = G.episode_statistics(chain, ct, A)
        slots = int(R.local_mask(n, p, v).sum())
        assert slots == (2 * n - 3 if p == "F_TRI" else n - 1)
        assert lc["lifetime_local"] == pytest.approx(slots * ep["lifetime_ct"], rel=1e-12)
        assert lc["lifetime_local"] <= lc["lifetime_jump"] + 1e-12
        assert lc["exit_local_share"] == pytest.approx(1.0, abs=1e-15)  # every flexible exit toggles an anchor-incident slot


# --- structural feasibility --------------------------------------------------------


@pytest.mark.parametrize("n", [5, 6])
def test_f_star_complete_renewal_is_structurally_impossible(n):
    v = G.primary_instance("F_STAR")
    assert not R.renewal_feasible(n, "F_STAR", v, 3)
    assert R.max_partial_absent(n, "F_STAR", v, 3) == n - 4


@pytest.mark.parametrize("n", [5, 6])
def test_f_2path_and_f_tri_feasibility(n):
    assert R.renewal_feasible(n, "F_2PATH", G.primary_instance("F_2PATH"), 2)
    v = G.primary_instance("F_TRI")
    for s in range(1, n - 2):
        assert R.renewal_feasible(n, "F_TRI", v, s)
    assert not R.renewal_feasible(n, "F_TRI", v, n - 2)


def test_impossible_renewal_is_labelled_not_estimated():
    chain = free(4, [])
    rep = R.replacement(chain, law(chain), 4, "F_STAR", G.primary_instance("F_STAR"))
    assert rep["renewal_status"] == "STRUCTURALLY_IMPOSSIBLE"
    assert rep["renewal_unconditional"] is None


# --- independent augmented-observer route ------------------------------------------


def augmented_reference(chain, ct, n, predicate, vertices, tol=1e-15, cap=200_000):
    """Propagate (x, S0) directly: for each entry state, iterate the killed jump chain with the
    entry set carried along. No canonical mapping, no BiCGSTAB. Returns (departures/episode, renewal)."""
    A = G.predicate_mask(chain.states, n, predicate, vertices)
    mu = R.entrance_weights(chain, ct, A)
    J = mu.sum()
    part = R.participation(chain.states, n, predicate, vertices)
    Pj = chain.W / chain.rates[:, None]
    dep = 0.0
    ren = 0.0
    for y in np.nonzero(mu > 0)[0]:
        s0 = np.nonzero(part[y])[0]
        # renewal: absorb when no s0 participates (inside A)
        renew_set = A & ~part[:, s0].any(axis=1)
        dist = np.zeros(len(A))
        dist[y] = 1.0
        absorbed = 0.0
        for _ in range(cap):
            nxt = np.zeros(len(A))
            np.add.at(nxt, chain.T.ravel(), (dist[:, None] * Pj).ravel())
            nxt[~A] = 0.0
            absorbed += nxt[renew_set].sum()
            nxt[renew_set] = 0.0
            dist = nxt
            if dist.sum() < tol:
                break
        ren += mu[y] * absorbed
        for s in s0:
            gone = A & ~part[:, s]
            dist = np.zeros(len(A))
            dist[y] = 1.0
            hit = 0.0
            for _ in range(cap):
                nxt = np.zeros(len(A))
                np.add.at(nxt, chain.T.ravel(), (dist[:, None] * Pj).ravel())
                nxt[~A] = 0.0
                hit += nxt[gone].sum()
                nxt[gone] = 0.0
                dist = nxt
                if dist.sum() < tol:
                    break
            dep += mu[y] * hit
    return dep / J, ren / J


@pytest.mark.parametrize("components", [[], PCOMP, CLOSEW])
def test_f_tri_replacement_matches_augmented_reference_n4(components):
    chain = free(4, components)
    ct = law(chain)
    v = G.primary_instance("F_TRI")
    rep = R.replacement(chain, ct, 4, "F_TRI", v)
    dep, ren = augmented_reference(chain, ct, 4, "F_TRI", v)
    assert rep["expected_distinct_departures_per_episode"] == pytest.approx(dep, rel=1e-9)
    assert rep["renewal_unconditional"] == pytest.approx(ren, rel=1e-9)
    assert all(s.get("dense_max_abs_difference", 0.0) < 1e-10 for s in rep["solves"].values())


@pytest.mark.parametrize("predicate", ["F_2PATH", "F_TRI", "F_STAR"])
def test_synthetic_n5_replacement_matches_augmented_reference(predicate):
    chain = full_chain(5, neighbourhood_rate(5))
    ct = law(chain)
    v = G.primary_instance(predicate)
    rep = R.replacement(chain, ct, 5, predicate, v)
    dep, ren = augmented_reference(chain, ct, 5, predicate, v)
    assert rep["expected_distinct_departures_per_episode"] == pytest.approx(dep, rel=1e-8)
    if rep["renewal_status"] == "computed":
        assert rep["renewal_unconditional"] == pytest.approx(ren, rel=1e-8)
    else:
        assert ren == 0.0


# --- Monte Carlo trajectory check (independent of every linear solve) ----------------


def test_monte_carlo_trajectories_agree_n4_null():
    rng = np.random.default_rng(20261015)
    n = 4
    chain = free(n, [])
    ct = law(chain)
    p = "F_TRI"
    v = G.primary_instance(p)
    A = G.predicate_mask(chain.states, n, p, v)
    loc = R.local_mask(n, p, v)
    part = R.participation(chain.states, n, p, v)
    mu = R.entrance_weights(chain, ct, A)
    entries = np.nonzero(mu > 0)[0]
    w = mu[entries] / mu.sum()
    Pj = chain.W / chain.rates[:, None]
    episodes = 40_000
    local_total = 0
    renewed = 0
    for _ in range(episodes):
        x = rng.choice(entries, p=w)
        s0 = part[x].copy()
        while True:
            e = rng.choice(chain.n_slots, p=Pj[x])
            local_total += int(loc[e])
            x = chain.T[x, e]
            if not A[x]:
                break
            if not (part[x] & s0).any():
                renewed += 1
                # continue the episode for the local count; renewal counted once
                while A[x]:
                    e = rng.choice(chain.n_slots, p=Pj[x])
                    local_total += int(loc[e])
                    x = chain.T[x, e]
                break
    lc = R.local_clock(chain, ct, A, loc)
    rep = R.replacement(chain, ct, n, p, v)
    assert local_total / episodes == pytest.approx(lc["lifetime_local"], rel=0.02)
    assert renewed / episodes == pytest.approx(rep["renewal_unconditional"], abs=0.006)


# --- flicker ------------------------------------------------------------------------


def test_flicker_null_closed_form_n4():
    """NULL: after any internal toggle the next event reverses it with probability 1/M."""
    chain = free(4, [])
    ct = law(chain)
    for p in ("F_TRI", "F_2PATH"):
        v = G.primary_instance(p)
        A = G.predicate_mask(chain.states, 4, p, v)
        f = R.flicker(chain, ct, A, G.eligible_toggles(chain.states, 4, p, v), R.local_mask(4, p, v))
        assert f["reversal_next_event"] == pytest.approx(1 / 6, rel=1e-12)
        assert f["reversal_next_local_event"] == pytest.approx(1 / int(R.local_mask(4, p, v).sum()), rel=1e-12)


# --- invariances ------------------------------------------------------------------------


def test_event_count_statistics_are_scale_free():
    chain = free(4, PCOMP)
    ct = law(chain)
    fast = Chain(chain.n_slots, chain.states, 3.0 * chain.W, chain.T)
    a = R.analyse_law(chain, ct, 4, relabelled=False)
    b = R.analyse_law(fast, ct, 4, relabelled=False)
    for p in R.FLEXIBLE:
        for key in ("lifetime_local", "local_share_of_events_in_A"):
            assert a["predicates"][p]["local"][key] == pytest.approx(b["predicates"][p]["local"][key], rel=1e-12)
        assert a["predicates"][p]["flicker"]["reversal_next_event"] == b["predicates"][p]["flicker"]["reversal_next_event"] or a["predicates"][p]["flicker"]["reversal_next_event"] == pytest.approx(b["predicates"][p]["flicker"]["reversal_next_event"], rel=1e-12)
        ra, rb = a["predicates"][p]["replacement"], b["predicates"][p]["replacement"]
        assert ra["expected_distinct_departures_per_episode"] == pytest.approx(rb["expected_distinct_departures_per_episode"], rel=1e-10)


def test_relabelled_anchor_agrees_synthetic_n5():
    chain = full_chain(5, neighbourhood_rate(5))
    ct = law(chain)
    out = R.analyse_law(chain, ct, 5)
    for p in R.FLEXIBLE:
        a, b = out["predicates"][p], out["relabelled"][p]
        assert a["local"]["lifetime_local"] == pytest.approx(b["local"]["lifetime_local"], rel=1e-9)
        assert a["replacement"]["expected_distinct_departures_per_episode"] == pytest.approx(b["replacement"]["expected_distinct_departures_per_episode"], rel=1e-9)
        if a["replacement"]["renewal_status"] == "computed":
            assert a["replacement"]["renewal_unconditional"] == pytest.approx(b["replacement"]["renewal_unconditional"], rel=1e-9)


# --- NK -------------------------------------------------------------------------------------


def test_nk_null_fixed_point():
    n = 4
    chain = free(n, [])
    ct = law(chain)
    lf = R.layer_fluxes(chain, ct, n)
    rates = R.nk_rates(lf["p"], lf["up"])
    assert np.allclose(rates["birth"][:-1], 1.0, rtol=1e-12) and np.allclose(rates["death"][1:], 1.0, rtol=1e-12)


@pytest.mark.parametrize("n", [4, 5])
def test_nk_propositions_on_heterogeneous_uniform_law(n):
    chain = full_chain(n, neighbourhood_rate(n))
    ct = law(chain)
    m = len(edges(n))
    assert np.allclose(ct, 1.0 / (1 << m), rtol=1e-9)  # uniform law despite heterogeneous rates
    lf = R.layer_fluxes(chain, ct, n)
    assert np.allclose(lf["up"], lf["down"], rtol=1e-10)  # stationary layer flux balance
    assert max(lf["q_range_given_k"]) > 0  # heterogeneous within layers
    nk, pi_nk, info = R.nk_chain(n, lf["p"], lf["up"])
    assert info["detailed_balance_max_relative"] < 1e-12
    assert info["global_balance_relative"] < 1e-10
    solved = law(nk)
    assert np.abs(solved - pi_nk).sum() < 1e-9  # analytic law agrees with an independent solve
    lnk = R.layer_fluxes(nk, pi_nk, n)
    ids = R.nk_identities(lf, lnk)
    assert ids["p_relative"] < 1e-10 and ids["up_flux_relative"] < 1e-10 and ids["mean_q_given_k_relative"] < 1e-10
    assert ids["nk_within_layer_sd_max"] < 1e-9
    # mean rate and jump-clock density profile follow
    assert float(pi_nk @ nk.rates) == pytest.approx(float(ct @ chain.rates), rel=1e-10)
    assert np.allclose(G.jump_density(nk, pi_nk, n), G.jump_density(chain, ct, n), atol=1e-12)
    # unlike ND, which matches only the CT profile and mean rate
    nd, pi_nd, _ = G.nd_chain(n, lf["p"], float(ct @ chain.rates))
    assert np.abs(G.jump_density(nd, pi_nd, n) - G.jump_density(chain, ct, n)).sum() > 1e-6 or n < 5


def test_nk_zero_bin_is_unresolved():
    rates = R.nk_rates(np.array([0.5, 0.0, 0.5]), np.array([0.1, 0.1]))
    assert rates["resolved"] is False
