"""Proof fixtures for GT-P011 (E5C) durable renewal: synthetic chains, N <= 4 kernels and a synthetic N = 5
rule that is not one of the twelve laws. No E5C scientific cell is evaluated here."""

from __future__ import annotations

import numpy as np
import pytest

from rs_constraint_lab import gtkernel
from rs_constraint_lab import gtdurable as D
from rs_constraint_lab import gtpersist as G
from rs_constraint_lab import gtrenew as RN
from rs_constraint_lab.gte0a import Chain
from rs_constraint_lab.state import edges

PCOMP = [("path_form", "weak_favour"), ("path_dissolve", "weak_favour")]
CLOSEW = [("close_form", "weak_favour")]


def law(chain):
    st = gtkernel.stationary_sparse(chain)
    assert st["resolved"]
    return st["ct"]


def free(n, comps):
    return gtkernel.reachable_chain(n, "FREE", comps)[0]


def full_chain(n, rate_fn):
    m = len(edges(n))
    states = np.arange(1 << m, dtype=np.int64)
    x = G.bits(states, n)
    W = np.array([[rate_fn(x[i], e) for e in range(m)] for i in range(len(states))], dtype=float)
    return Chain(m, states, W, states[:, None] ^ (1 << np.arange(m))[None, :])


def neighbourhood_rate(n):
    pairs = edges(n)
    adj = [[f for f, q in enumerate(pairs) if f != e and set(q) & set(p)] for e, p in enumerate(pairs)]
    return lambda xb, e: 2.0 ** int(sum(xb[f] for f in adj[e]))


def independent_route(chain, ct, n, predicate, vertices, horizons=D.HORIZONS, tol=1e-15, cap=100_000):
    """Propagate (x, phase, local count) through the plain jump chain from every original entry state.
    No canonical frames, no resolvents, no remote/local kernel."""
    A = G.predicate_mask(chain.states, n, predicate, vertices)
    mu = RN.entrance_weights(chain, ct, A)
    J = mu.sum()
    part = RN.participation(chain.states, n, predicate, vertices)
    loc = RN.local_mask(n, predicate, vertices)
    Pj = chain.W / chain.rates[:, None]
    hmax = max(horizons)
    U = np.zeros(hmax + 1)
    for y in np.nonzero(mu > 0)[0]:
        s0 = np.nonzero(part[y])[0]
        if not RN.renewal_feasible(n, predicate, vertices, len(s0)):
            continue
        R = A & ~part[:, s0].any(axis=1)
        pre = np.zeros(len(A))
        pre[y] = 1.0
        post = np.zeros((hmax + 1, len(A)))
        for _ in range(cap):
            new_pre = np.zeros(len(A))
            new_post = np.zeros_like(post)
            # pre-renewal jumps
            for e in range(chain.n_slots):
                tgt = chain.T[:, e]
                mass = pre * Pj[:, e]
                np.add.at(new_pre, tgt, mass)
            entered = np.where(R, new_pre, 0.0)
            U[0] += mu[y] * entered.sum()
            new_post[0] += entered
            new_pre = np.where(A & ~R, new_pre, 0.0)
            # post-renewal jumps
            for c in range(hmax):
                if not post[c].any():
                    continue
                for e in range(chain.n_slots):
                    tgt = chain.T[:, e]
                    mass = post[c] * Pj[:, e]
                    cc = c + 1 if loc[e] else c
                    landed = np.zeros(len(A))
                    np.add.at(landed, tgt, mass)
                    landed = np.where(R, landed, 0.0)
                    if loc[e]:
                        U[cc] += mu[y] * landed.sum()
                        if cc < hmax:
                            new_post[cc] += landed
                    else:
                        new_post[cc] += landed
            new_post[hmax] = 0.0
            pre, post = new_pre, new_post
            if pre.sum() + post.sum() < tol:
                break
    return {h: U[h] / J for h in horizons}


@pytest.mark.parametrize("comps", [[], PCOMP, CLOSEW])
def test_f_tri_n4_matches_independent_route(comps):
    chain = free(4, comps)
    ct = law(chain)
    v = G.primary_instance("F_TRI")
    d = D.durable(chain, ct, 4, "F_TRI", v)
    ref = independent_route(chain, ct, 4, "F_TRI", v)
    for h in D.HORIZONS:
        assert d["U"][str(h)] == pytest.approx(ref[h], rel=1e-8, abs=1e-15)
    assert d["R0"] == pytest.approx(RN.replacement(chain, ct, 4, "F_TRI", v)["renewal_unconditional"], rel=1e-10)


@pytest.mark.parametrize("predicate", ["F_2PATH", "F_TRI"])
def test_synthetic_n5_matches_independent_route(predicate):
    chain = full_chain(5, neighbourhood_rate(5))
    ct = law(chain)
    v = G.primary_instance(predicate)
    d = D.durable(chain, ct, 5, predicate, v)
    ref = independent_route(chain, ct, 5, predicate, v)
    for h in D.HORIZONS:
        assert d["U"][str(h)] == pytest.approx(ref[h], rel=1e-7, abs=1e-14)
    assert d["R0"] == pytest.approx(RN.replacement(chain, ct, 5, predicate, v)["renewal_unconditional"], rel=1e-9)


def test_monte_carlo_n4_null_f_tri():
    rng = np.random.default_rng(11)
    n, p = 4, "F_TRI"
    chain = free(n, [])
    ct = law(chain)
    v = G.primary_instance(p)
    A = G.predicate_mask(chain.states, n, p, v)
    mu = RN.entrance_weights(chain, ct, A)
    part = RN.participation(chain.states, n, p, v)
    loc = RN.local_mask(n, p, v)
    Pj = chain.W / chain.rates[:, None]
    entries = np.nonzero(mu > 0)[0]
    w = mu[entries] / mu.sum()
    hits = np.zeros(3)
    trials = 60_000
    for _ in range(trials):
        x = rng.choice(entries, p=w)
        s0 = part[x].copy()
        if s0.sum() > 1:
            continue
        renewed, count = False, 0
        while True:
            e = rng.choice(chain.n_slots, p=Pj[x])
            x = chain.T[x, e]
            if not A[x]:
                break
            if not renewed:
                if not (part[x] & s0).any():
                    renewed = True
                    hits[0] += 1
                continue
            if (part[x] & s0).any():
                break
            if loc[e]:
                count += 1
                if count <= 2:
                    hits[count] += 1
                if count == 2:
                    break
    d = D.durable(chain, ct, n, p, v)
    for h in (0, 1, 2):
        assert hits[h] / trials == pytest.approx(d["U"][str(h)], abs=0.004)


def test_identities_monotonicity_and_causes():
    chain = full_chain(5, neighbourhood_rate(5))
    ct = law(chain)
    for p in D.PREDICATES:
        d = D.durable(chain, ct, 5, p, G.primary_instance(p))
        U = [d["U"][str(h)] for h in D.HORIZONS]
        assert all(a >= b - 1e-15 for a, b in zip(U, U[1:]))
        for c in d["classes"].values():
            if c.get("status") != "computed":
                continue
            assert c["remote_closure_violations"] == 0  # T13
            assert c["return_before_exit"] + c["exit_before_return"] == pytest.approx(1.0, abs=1e-10)
            assert c["first_local_split_sum"] == pytest.approx(1.0, abs=1e-10)
            for h in D.HORIZONS:
                assert c["U"][str(h)] == pytest.approx(c["R0"] * c["C"][str(h)], rel=1e-12)
            assert c["C"]["0"] == pytest.approx(1.0)


def test_first_hit_law_differs_from_stationary_restriction():
    chain = full_chain(5, neighbourhood_rate(5))
    ct = law(chain)
    d = D.durable(chain, ct, 5, "F_2PATH", G.primary_instance("F_2PATH"))
    assert d["classes"]["2"]["first_hit_vs_stationary_l1"] > 1e-3  # the result follows the first-hit law (matched by the independent route)


def test_uniform_rescaling_invariant_and_remote_change_matters():
    chain = full_chain(5, neighbourhood_rate(5))
    ct = law(chain)
    v = G.primary_instance("F_2PATH")
    base = D.durable(chain, ct, 5, "F_2PATH", v)
    fast = D.durable(Chain(chain.n_slots, chain.states, 4.0 * chain.W, chain.T), ct, 5, "F_2PATH", v)
    for h in D.HORIZONS:
        assert base["U"][str(h)] == pytest.approx(fast["U"][str(h)], rel=1e-10)
    # F_2PATH at N=5 is structurally zero after renewal (T14); use F_TRI for the remote-rate effect
    assert base["classes"]["2"]["post_renewal_status"] == "STRUCTURALLY_ZERO_FOR_H_GE_1" and base["classes"]["2"]["C"]["1"] == 0.0
    vt = G.primary_instance("F_TRI")
    bt = D.durable(chain, ct, 5, "F_TRI", vt)
    remote = ~RN.local_mask(5, "F_TRI", vt)
    W2 = chain.W * np.where(remote, 5.0, 1.0)[None, :]
    ch2 = Chain(chain.n_slots, chain.states, W2, chain.T)
    alt = D.durable(ch2, law(ch2), 5, "F_TRI", vt)
    assert abs(alt["classes"]["1"]["C"]["2"] - bt["classes"]["1"]["C"]["2"]) > 1e-6  # remote rates matter through the local kernel


def test_t14_post_renewal_feasibility_for_vertex_predicates():
    """F_2PATH (k=2): survival past h=0 needs K-s > k; N=5 (K=4,s=2) no, N=6 (K=5,s=2) yes."""
    for n, expected in ((5, "STRUCTURALLY_ZERO_FOR_H_GE_1"), (6, "computed")):
        chain = full_chain(n, neighbourhood_rate(n))  # synthetic rule at both sizes (no E5C cell)
        ct = law(chain)
        d = D.durable(chain, ct, n, "F_2PATH", G.primary_instance("F_2PATH"), horizons=(0, 1))
        assert d["classes"]["2"]["post_renewal_status"] == expected


def test_relabelled_anchor_and_structural_impossibility():
    chain = full_chain(5, neighbourhood_rate(5))
    ct = law(chain)
    out = D.analyse_law(chain, ct, 5)
    for p in D.PREDICATES:
        for h in D.HORIZONS:
            a, b = out["predicates"][p]["U"][str(h)], out["relabelled"][p]["U"][str(h)]
            assert a == pytest.approx(b, rel=1e-9, abs=1e-15)
    assert out["predicates"]["F_TRI"]["classes"]["3"]["status"] == "STRUCTURALLY_IMPOSSIBLE"
    n4 = D.durable(free(4, []), law(free(4, [])), 4, "F_2PATH", G.primary_instance("F_2PATH"))
    assert n4["status"] == "STRUCTURALLY_IMPOSSIBLE" and n4["R0"] is None


def test_observer_does_not_touch_rules():
    import inspect

    src = inspect.getsource(D)
    assert "gtkernel" not in src and "reachable_chain" not in src
