"""Proof fixtures for the NL comparator (GT-P012, E5D): synthetic chains and N <= 4 kernels only."""

from __future__ import annotations

import inspect

import numpy as np
import pytest

from rs_constraint_lab import gtkernel
from rs_constraint_lab import gtdurable as D
from rs_constraint_lab import gtlocalcontrol as NLm
from rs_constraint_lab import gtpersist as G
from rs_constraint_lab import gtrenew as RN
from rs_constraint_lab.gte0a import Chain
from rs_constraint_lab.state import edges


def law(chain):
    st = gtkernel.stationary_sparse(chain, cap=200_000)
    assert st["resolved"]
    return st["ct"]


def full_chain(n, rate_fn):
    m = len(edges(n))
    states = np.arange(1 << m, dtype=np.int64)
    x = G.bits(states, n)
    W = np.array([[rate_fn(x[i], e) for e in range(m)] for i in range(len(states))], dtype=float)
    return Chain(m, states, W, states[:, None] ^ (1 << np.arange(m))[None, :])


def circulating_rate(local):
    """Positive, deliberately non-reversible: local forms fast when remote is sparse, remote forms fast
    when local is dense, local dissolves fast when remote is dense, remote dissolves fast when local is sparse."""
    def f(xb, e):
        l, r = int(xb[local].sum()), int(xb[~local].sum())
        if local[e]:
            return (3.0 if r <= 1 else 0.5) if not xb[e] else (2.5 if r >= 2 else 0.4)
        return (3.0 if l >= 3 else 0.5) if not xb[e] else (2.5 if l <= 2 else 0.4)
    return f


MASKS = {"F_TRI": lambda n: RN.local_mask(n, "F_TRI", G.primary_instance("F_TRI")), "F_2PATH": lambda n: RN.local_mask(n, "F_2PATH", G.primary_instance("F_2PATH"))}


@pytest.mark.parametrize("pred", ["F_TRI", "F_2PATH"])
def test_null_fixed_point(pred):
    n = 4
    chain = gtkernel.reachable_chain(n, "FREE", [])[0]
    ct = law(chain)
    mf = NLm.macro_fluxes(chain, ct, n, MASKS[pred](n))
    nl, pi, info = NLm.nl_chain(n, MASKS[pred](n), mf)
    assert np.allclose(nl.W, 1.0, rtol=1e-10)
    assert info["reversible"]


@pytest.mark.parametrize("pred", ["F_TRI", "F_2PATH"])
def test_nonreversible_projection_preserved(pred):
    n = 4
    local = MASKS[pred](n)
    chain = full_chain(n, circulating_rate(local))
    ct = law(chain)
    mf = NLm.macro_fluxes(chain, ct, n, local)
    diag = NLm.macro_diagnostics(mf)
    assert diag["conservation_max_relative"] < 1e-9  # T16 premise: macro-flux conservation
    assert diag["net_current_max_relative"] > 1e-3  # a genuine projected circulation exists
    nl, pi, info = NLm.nl_chain(n, local, mf)
    assert info["global_balance_relative"] < 1e-10  # pi_NL stationary without detailed balance
    assert not info["reversible"]  # detailed balance is not imposed
    assert max(info["identities"].values()) < 1e-10  # p and every ORDERED macro flux matched
    assert np.abs(law(nl) - pi).sum() < 1e-8  # independent stationary solve
    # NL's own projection carries the same net currents
    d2 = NLm.macro_diagnostics(NLm.macro_fluxes(nl, pi, n, local))
    assert d2["net_current_max_relative"] == pytest.approx(diag["net_current_max_relative"], rel=1e-8)


def test_count_dependent_target_is_its_own_nl_and_nk():
    n = 4
    chain = full_chain(n, lambda xb, e: (1.0 + 0.7 * xb.sum()) if not xb[e] else (2.0 + 0.3 * xb.sum()))
    ct = law(chain)
    local = MASKS["F_TRI"](n)
    nl, pi, _ = NLm.nl_chain(n, local, NLm.macro_fluxes(chain, ct, n, local))
    assert np.allclose(nl.W, chain.W, rtol=1e-9)
    lf = RN.layer_fluxes(chain, ct, n)
    nk, _, _ = RN.nk_chain(n, lf["p"], lf["up"])
    assert np.allclose(nk.W, chain.W, rtol=1e-9)


def test_relabelled_anchor_gives_identical_durability():
    n = 4
    chain = gtkernel.reachable_chain(n, "FREE", [("path_form", "weak_favour"), ("path_dissolve", "weak_favour")])[0]
    ct = law(chain)
    out = []
    for inst in (G.primary_instance("F_TRI"), G.relabelled_instance("F_TRI", n)):
        local = RN.local_mask(n, "F_TRI", inst)
        nl, pi, _ = NLm.nl_chain(n, local, NLm.macro_fluxes(chain, ct, n, local))
        out.append(D.durable(nl, pi, n, "F_TRI", inst))
    for h in D.HORIZONS:
        assert out[0]["U"][str(h)] == pytest.approx(out[1]["U"][str(h)], rel=1e-9, abs=1e-15)


def test_zero_cell_is_unresolved_not_smoothed():
    mf = {"L": 1, "R": 1, "p": np.array([[0.5, 0.0], [0.25, 0.25]]), "J": {d: np.full((2, 2), 0.1) for d in NLm.DIRS}}
    assert NLm.nl_rates(mf)["resolved"] is False


def test_nl_never_sees_the_predicate_or_durability():
    sig = inspect.signature(NLm.nl_chain)
    assert list(sig.parameters) == ["n", "local", "mf"]
    src = inspect.getsource(NLm)
    for word in ("participation", "renew", "durable", "S0", "F_TRI", "completer"):
        assert word not in src.split('"""', 2)[2], word
