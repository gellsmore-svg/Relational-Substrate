"""NL: an anchor-relative local/remote traffic-matched comparator (GT-P012, E5D).

A diagnostic comparison process parameterised from a target's stationary generator, not a
relational constraint family. Given a fixed analyst partition of slots into LOCAL (incident on
an anchor vertex) and REMOTE, with l(x), r(x) the present counts in each pool and z = (l, r):

* p_z = sum_{z(x)=z} pi(x), and the ORDERED stationary macro fluxes J_{z->z'} for the four
  neighbouring cells (one local or one remote toggle), as sums of positive terms;
* the lift W_NL: every absent LOCAL slot forms at J_{z->z+eL} / (p_z (L-l)), every present LOCAL
  slot dissolves at J_{z->z-eL} / (p_z l), and likewise for REMOTE. Directed fluxes are used as
  they are; nothing is symmetrised, so projected circulation is preserved;
* stationary law pi_NL(x) = p_z / (C(L,l) C(R,r)) (T16: macro-flux conservation suffices; detailed
  balance is not assumed and holds iff every macro edge carries zero net current).

NL matches p_z and every ordered macro flux, hence the edge-count profile, adjacent edge-count
traffic, mean CT activity and local/remote event traffic. It does not match arrangement within a
cell, completer counts, correlations, local motif hazards, multi-time structure or persistence.
Definitions and proofs: ``gravity-time/docs/e5d-local-traffic-comparator.md``.
"""

from __future__ import annotations

import math

import numpy as np

from rs_constraint_lab import gtpersist as P
from rs_constraint_lab.gte0a import Chain
from rs_constraint_lab.state import edges

LOCALCONTROL_VERSION = "gt-localcontrol/v1"
DIRS = ("L+", "L-", "R+", "R-")


def pool_counts(states: np.ndarray, n: int, local: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    x = P.bits(states, n)
    return x[:, local].sum(axis=1), x[:, ~local].sum(axis=1)


def macro_fluxes(chain: Chain, ct: np.ndarray, n: int, local: np.ndarray) -> dict:
    """p[l, r] and ordered fluxes J[dir][l, r] out of cell (l, r), from positive terms only."""
    L, R = int(local.sum()), int((~local).sum())
    x = P.bits(chain.states, n)
    l, r = x[:, local].sum(axis=1), x[:, ~local].sum(axis=1)
    p = np.zeros((L + 1, R + 1))
    np.add.at(p, (l, r), ct)
    J = {}
    for d, pool, form in (("L+", local, True), ("L-", local, False), ("R+", ~local, True), ("R-", ~local, False)):
        mask = pool[None, :] & (~x if form else x)
        rate = np.where(mask, chain.W, 0.0).sum(axis=1)
        a = np.zeros((L + 1, R + 1))
        np.add.at(a, (l, r), ct * rate)
        J[d] = a
    q_loc = chain.W[:, local].sum(axis=1)
    mean_loc = np.zeros((L + 1, R + 1))
    np.add.at(mean_loc, (l, r), ct * q_loc)
    mean_loc = np.divide(mean_loc, p, out=np.zeros_like(p), where=p > 0)
    var_loc = np.zeros((L + 1, R + 1))
    np.add.at(var_loc, (l, r), ct * (q_loc - mean_loc[l, r]) ** 2)  # two-pass: no cancellation
    var_loc = np.divide(var_loc, p, out=np.zeros_like(p), where=p > 0)
    return {"L": L, "R": R, "p": p, "J": J, "local_rate_mean": mean_loc, "local_rate_sd": np.sqrt(var_loc)}


def macro_diagnostics(mf: dict) -> dict:
    """Conservation (outflow = inflow per cell), net currents on macro edges, and their size."""
    L, R, p, J = mf["L"], mf["R"], mf["p"], mf["J"]
    out = J["L+"] + J["L-"] + J["R+"] + J["R-"]
    inflow = np.zeros_like(p)
    inflow[1:, :] += J["L+"][:-1, :]
    inflow[:-1, :] += J["L-"][1:, :]
    inflow[:, 1:] += J["R+"][:, :-1]
    inflow[:, :-1] += J["R-"][:, 1:]
    cons = float(np.max(np.abs(out - inflow) / np.maximum(np.maximum(out, inflow), 1e-300)))
    # net current on each macro edge, relative to the larger direction
    curL = J["L+"][:-1, :] - J["L-"][1:, :]
    curR = J["R+"][:, :-1] - J["R-"][:, 1:]
    relL = np.abs(curL) / np.maximum(np.maximum(J["L+"][:-1, :], J["L-"][1:, :]), 1e-300)
    relR = np.abs(curR) / np.maximum(np.maximum(J["R+"][:, :-1], J["R-"][:, 1:]), 1e-300)
    total = float(sum(J[d].sum() for d in DIRS))
    return {
        "conservation_max_relative": cons,
        "net_current_max_relative": float(max(relL.max() if relL.size else 0.0, relR.max() if relR.size else 0.0)),
        "net_current_abs_sum_over_total_flux": float((np.abs(curL).sum() + np.abs(curR).sum()) / total) if total > 0 else 0.0,
        "zero_cells": [[int(a), int(b)] for a, b in zip(*np.nonzero(p <= 0))],
        "rare_cells": [[int(a), int(b), float(p[a, b])] for a, b in zip(*np.nonzero((p > 0) & (p < P.RARE_MASS)))],
        "p_min": float(p.min()),
    }


def nl_rates(mf: dict) -> dict:
    """Per-slot rates by cell and pool; unresolved on any zero cell or zero interior flux."""
    L, R, p, J = mf["L"], mf["R"], mf["p"], mf["J"]
    if (p <= 0).any():
        return {"resolved": False, "reason": "a macro cell has zero stationary mass"}
    ls = np.arange(L + 1)[:, None] * np.ones((1, R + 1))
    rs = np.ones((L + 1, 1)) * np.arange(R + 1)[None, :]
    with np.errstate(divide="ignore", invalid="ignore"):
        bL = np.where(ls < L, J["L+"] / (p * (L - ls)), 0.0)
        dL = np.where(ls > 0, J["L-"] / (p * ls), 0.0)
        bR = np.where(rs < R, J["R+"] / (p * (R - rs)), 0.0)
        dR = np.where(rs > 0, J["R-"] / (p * rs), 0.0)
    interior = [(bL, ls < L), (dL, ls > 0), (bR, rs < R), (dR, rs > 0)]
    if any(((a <= 0) & m).any() for a, m in interior):
        return {"resolved": False, "reason": "a zero ordered flux on an admissible macro edge"}
    return {"resolved": True, "bL": bL, "dL": dL, "bR": bR, "dR": dR}


def nl_chain(n: int, local: np.ndarray, mf: dict) -> tuple[Chain, np.ndarray, dict]:
    """The NL lift on the full FREE space, its analytic stationary law and identity diagnostics."""
    m = len(edges(n))
    rates = nl_rates(mf)
    if not rates["resolved"]:
        raise ValueError(rates["reason"])
    L, R, p = mf["L"], mf["R"], mf["p"]
    states = np.arange(1 << m, dtype=np.int64)
    x = P.bits(states, n)
    l, r = x[:, local].sum(axis=1), x[:, ~local].sum(axis=1)
    W = np.where(local[None, :], np.where(x, rates["dL"][l, r][:, None], rates["bL"][l, r][:, None]),
                 np.where(x, rates["dR"][l, r][:, None], rates["bR"][l, r][:, None]))
    log_binom = lambda N, k: math.lgamma(N + 1) - math.lgamma(k + 1) - math.lgamma(N - k + 1)  # noqa: E731
    cl = np.array([log_binom(L, k) for k in range(L + 1)])
    cr = np.array([log_binom(R, k) for k in range(R + 1)])
    log_pi = np.log(p)[l, r] - cl[l] - cr[r]
    pi = np.exp(log_pi - log_pi.max())
    pi /= pi.sum()
    T = states[:, None] ^ (1 << np.arange(m))[None, :]
    chain = Chain(m, states, W, T)
    flow_in = np.zeros(len(states))
    for e in range(m):
        flow_in += pi[T[:, e]] * W[T[:, e], e]
    db = 0.0
    for e in range(m):
        a = pi * W[:, e]
        b = pi[T[:, e]] * W[T[:, e], e]
        db = max(db, float((np.abs(a - b) / np.maximum(np.maximum(a, b), 1e-300)).max()))
    mf_nl = macro_fluxes(chain, pi, n, local)
    gaps = {"p_relative": float(np.max(np.abs(mf_nl["p"] - p) / np.maximum(np.maximum(mf_nl["p"], p), 1e-300)))}
    for d in DIRS:
        a, b = mf_nl["J"][d], mf["J"][d]
        mask = (a > 0) | (b > 0)
        gaps[f"J_{d}_relative"] = float(np.max(np.abs(a - b)[mask] / np.maximum(np.maximum(a, b), 1e-300)[mask])) if mask.any() else 0.0
    info = {
        "global_balance_relative": float(np.abs(flow_in - pi * chain.rates).sum() / (pi * chain.rates).sum()),
        "detailed_balance_max_relative": db,
        "reversible": bool(db < 1e-9),
        "identities": gaps,
        "min_rate": float(W.min()),
        "max_rate": float(W.max()),
        "within_cell_sd_local_rate_max": float(mf_nl["local_rate_sd"].max()),
    }
    return chain, pi, info
