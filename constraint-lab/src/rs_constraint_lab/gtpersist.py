"""Motif persistence, within-episode turnover, a density-matched comparator and a lagged hub (GT-P009).

Read-only observables on a finite single-toggle chain (``gte0a.Chain``); no
rule reads a motif, anchor or selected vertex. Definitions and proofs:
``gravity-time/docs/e5-definitions-and-null-construction.md``.

* Predicates: intact motifs (I_TRI, I_STAR, I_2PATH; required edges present,
  others free) and flexible anchored organisations (F_TRI, F_STAR, F_2PATH).
* Episodes by stationary boundary flux: J_A = sum pi W over toggles leaving A
  (equal to the entering flux), L_ct = pi(A)/J_A, L_jump = E_pi[q 1_A]/J_A,
  off-episode and recurrence counterparts, and Omega = eligible internal
  toggle flux / J_A.
* ND: the reversible, exchangeable Metropolis chain with the target's
  continuous-time edge-count profile p_k, scaled to the target's mean rate.
* Lagged hub: a maximum-degree vertex chosen once at a stationary start
  (uniform over ties), followed at declared lags against a uniform vertex.
  Continuous lags use the exact matrix exponential of the chain lumped by the
  permutations fixing vertices 0 and 1; jump lags use full-space propagation.
* Residual (occupation-sampled) lifetimes from the killed jump chain on A
  (BiCGSTAB), which also gives an entrance first-passage check of L_ct.
"""

from __future__ import annotations

import itertools
import math
import time

import numpy as np

from rs_constraint_lab import gtobs
from rs_constraint_lab.gte0a import Chain
from rs_constraint_lab.state import edges

PERSIST_VERSION = "gt-persist/v1"
TIE_RELATIVE = 1e-9
RARE_MASS = 1e-12
KILLED_TOLERANCE = 1e-12
KILLED_CAP = 20_000
KILLED_SECONDS = 60.0
PADE13_THETA = 5.371920351148152

PREDICATES = ("I_TRI", "I_STAR", "I_2PATH", "F_TRI", "F_STAR", "F_2PATH")
INTACT = ("I_TRI", "I_STAR", "I_2PATH")
FLEXIBLE = ("F_TRI", "F_STAR", "F_2PATH")


# --- structure ---------------------------------------------------------------


def slot(n: int, a: int, b: int) -> int:
    return edges(n).index((min(a, b), max(a, b)))


def bits(states: np.ndarray, n: int) -> np.ndarray:
    """(states, slots) boolean presence array."""
    m = len(edges(n))
    return ((states[:, None] >> np.arange(m)) & 1).astype(bool)


def degrees(states: np.ndarray, n: int) -> np.ndarray:
    x = bits(states, n)
    deg = np.zeros((len(states), n), dtype=np.int64)
    for e, (a, b) in enumerate(edges(n)):
        deg[:, a] += x[:, e]
        deg[:, b] += x[:, e]
    return deg


def primary_instance(predicate: str) -> tuple[int, ...]:
    """Declared vertices: I_TRI(0,1,2); I_STAR(0;1,2,3); I_2PATH(1,0,2) (middle 0); F_TRI {0,1}; F_STAR(0); F_2PATH(0)."""
    return {"I_TRI": (0, 1, 2), "I_STAR": (0, 1, 2, 3), "I_2PATH": (1, 0, 2), "F_TRI": (0, 1), "F_STAR": (0,), "F_2PATH": (0,)}[predicate]


def relabelled_instance(predicate: str, n: int) -> tuple[int, ...]:
    """Image of the primary instance under v -> n-1-v (covariance check)."""
    return tuple(n - 1 - v for v in primary_instance(predicate))


def required_slots(predicate: str, n: int, vertices: tuple[int, ...]) -> list[int]:
    """Slots that must be present: every intact edge, and the F_TRI anchor."""
    if predicate == "I_TRI":
        a, b, c = vertices
        return [slot(n, a, b), slot(n, b, c), slot(n, a, c)]
    if predicate == "I_STAR":
        c, *leaves = vertices
        return [slot(n, c, v) for v in leaves]
    if predicate == "I_2PATH":
        a, b, c = vertices
        return [slot(n, a, b), slot(n, b, c)]
    if predicate == "F_TRI":
        a, b = vertices
        return [slot(n, a, b)]
    return []


def predicate_mask(states: np.ndarray, n: int, predicate: str, vertices: tuple[int, ...]) -> np.ndarray:
    x = bits(states, n)
    if predicate in INTACT:
        return x[:, required_slots(predicate, n, vertices)].all(axis=1)
    if predicate == "F_TRI":
        a, b = vertices
        completers = np.zeros(len(states), dtype=np.int64)
        for c in range(n):
            if c not in (a, b):
                completers += x[:, slot(n, a, c)] & x[:, slot(n, b, c)]
        return x[:, slot(n, a, b)] & (completers >= 1)
    (c,) = vertices
    deg = degrees(states, n)[:, c]
    if predicate == "F_STAR":
        return deg >= 3
    if predicate == "F_2PATH":
        return deg >= 2
    raise ValueError(f"unknown predicate {predicate}")


def eligible_toggles(states: np.ndarray, n: int, predicate: str, vertices: tuple[int, ...]) -> np.ndarray:
    """(states, slots) mask of toggles that change the participating edge set (before A/A' membership is imposed).

    Intact predicates: the required slots (their internal flux is identically
    zero; the analyser checks it). F_TRI: slot ac or bc (c not in the anchor)
    whose other leg is present. F_STAR / F_2PATH: slots incident on the centre.
    """
    m = len(edges(n))
    out = np.zeros((len(states), m), dtype=bool)
    if predicate in INTACT:
        out[:, required_slots(predicate, n, vertices)] = True
        return out
    x = bits(states, n)
    if predicate == "F_TRI":
        a, b = vertices
        for c in range(n):
            if c in (a, b):
                continue
            ac, bc = slot(n, a, c), slot(n, b, c)
            out[:, ac] = x[:, bc]
            out[:, bc] = x[:, ac]
        return out
    (c,) = vertices
    for e, pair in enumerate(edges(n)):
        if c in pair:
            out[:, e] = True
    return out


# --- episodes ----------------------------------------------------------------


def _boundary(chain: Chain, A: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    valid = chain.T >= 0
    target_in = np.where(valid, A[np.maximum(chain.T, 0)], False)
    return valid, target_in


def episode_statistics(chain: Chain, ct: np.ndarray, A: np.ndarray, *, eligible: np.ndarray | None = None, required: list[int] | None = None, anchor: int | None = None) -> dict:
    """Stationary entrance-episode quantities of the set A, both clocks.

    ``ct`` is the normalised continuous-time stationary law. Fluxes are
    stationary probability flows per unit time.
    """
    R = chain.rates
    mean_rate = float(ct @ R)
    valid, target_in = _boundary(chain, A)
    flow = ct[:, None] * chain.W
    leaving = valid & A[:, None] & ~target_in
    entering = valid & ~A[:, None] & target_in
    internal = valid & A[:, None] & target_in
    exit_flux = float(flow[leaving].sum())
    entry_flux = float(flow[entering].sum())
    prevalence_ct = float(ct[A].sum())
    rate_mass = ct * R
    in_rate_mass = float(rate_mass[A].sum())
    out = {
        "entry_flux": entry_flux,
        "exit_flux": exit_flux,
        "flux_balance_relative": abs(entry_flux - exit_flux) / max(entry_flux, exit_flux) if max(entry_flux, exit_flux) > 0 else 0.0,
        "mean_rate_ct": mean_rate,
        "prevalence_ct": prevalence_ct,
        "prevalence_jump": in_rate_mass / mean_rate if mean_rate > 0 else None,
        "state_count": int(A.sum()),
    }
    if not A.any():
        out["classification"] = "absent"
        return out
    if A.all():
        out["classification"] = "whole_space"
        return out
    J = 0.5 * (entry_flux + exit_flux)
    if J <= 0.0:
        out["classification"] = "closed_or_absorbing"
        return out
    internal_flux = float(flow[internal].sum())
    out.update(
        {
            "classification": "ergodic_episodes",
            "entries_per_event": J / mean_rate,
            "entries_per_unit_time": J,
            "internal_events_per_episode": internal_flux / J,
            "lifetime_ct": prevalence_ct / J,
            "lifetime_jump": in_rate_mass / J,
            "off_lifetime_ct": (1.0 - prevalence_ct) / J,
            "off_lifetime_jump": (mean_rate - in_rate_mass) / J,
            "recurrence_entry_to_entry_ct": 1.0 / J,
            "recurrence_entry_to_entry_jump": mean_rate / J,
        }
    )
    out["jump_length_identity_gap"] = abs(out["lifetime_jump"] - 1.0 - out["internal_events_per_episode"]) / out["lifetime_jump"]
    if eligible is not None:
        omega_flux = float(flow[internal & eligible].sum())
        out["omega"] = omega_flux / J
        out["eligible_share_of_internal_events"] = out["omega"] / out["internal_events_per_episode"] if out["internal_events_per_episode"] > 0 else None
    if required is not None:
        req = np.zeros(chain.W.shape[1], dtype=bool)
        req[required] = True
        out["required_edge_internal_flux"] = float(flow[internal & req[None, :]].sum())
        out["required_edge_exit_share"] = float(flow[leaving & req[None, :]].sum()) / exit_flux
    if anchor is not None:
        anc = np.zeros(chain.W.shape[1], dtype=bool)
        anc[anchor] = True
        out["exit_share_anchor"] = float(flow[leaving & anc[None, :]].sum()) / exit_flux
        out["exit_share_last_completer"] = float(flow[leaving & ~anc[None, :]].sum()) / exit_flux
    return out


def analyse_predicate(chain: Chain, ct: np.ndarray, n: int, predicate: str, vertices: tuple[int, ...]) -> dict:
    A = predicate_mask(chain.states, n, predicate, vertices)
    eligible = eligible_toggles(chain.states, n, predicate, vertices)
    req = required_slots(predicate, n, vertices) if predicate in INTACT else None
    anchor = slot(n, *vertices) if predicate == "F_TRI" else None
    out = episode_statistics(chain, ct, A, eligible=eligible, required=req, anchor=anchor)
    out.update({"predicate": predicate, "vertices": list(vertices)})
    return out


def edge_episode(chain: Chain, ct: np.ndarray, n: int, a: int, b: int) -> dict:
    A = bits(chain.states, n)[:, slot(n, a, b)]
    out = episode_statistics(chain, ct, A)
    out["slot"] = [a, b]
    return out


# --- residual life and entrance first passage --------------------------------


def _killed_operator(chain: Chain, A: np.ndarray):
    idx = np.nonzero(A)[0]
    local = np.full(len(A), -1, dtype=np.int64)
    local[idx] = np.arange(len(idx))
    P = chain.W[idx] / chain.rates[idx, None]
    T = chain.T[idx]
    keep = (T >= 0) & np.where(T >= 0, A[np.maximum(T, 0)], False)
    tgt = np.where(keep, local[np.maximum(T, 0)], 0)
    Pk = np.where(keep, P, 0.0)

    def apply(v: np.ndarray) -> np.ndarray:  # (I - P_AA) v
        return v - (Pk * v[tgt]).sum(axis=1)

    return idx, apply


def bicgstab(apply, b: np.ndarray, *, tolerance: float = KILLED_TOLERANCE, cap: int = KILLED_CAP, seconds: float = KILLED_SECONDS) -> dict:
    """Unpreconditioned BiCGSTAB for apply(x) = b; returns x and convergence diagnostics."""
    started = time.perf_counter()
    x = np.zeros_like(b)
    r = b - apply(x)
    r_hat = r.copy()
    rho = alpha = omega = 1.0
    v = np.zeros_like(b)
    p = np.zeros_like(b)
    norm_b = float(np.linalg.norm(b))
    relative = float(np.linalg.norm(r)) / norm_b
    it = 0
    for it in range(1, cap + 1):
        rho_new = float(r_hat @ r)
        if rho_new == 0.0:
            break
        beta = (rho_new / rho) * (alpha / omega) if it > 1 else 0.0
        p = r + beta * (p - omega * v) if it > 1 else r.copy()
        v = apply(p)
        alpha = rho_new / float(r_hat @ v)
        s = r - alpha * v
        if float(np.linalg.norm(s)) / norm_b < tolerance:
            x = x + alpha * p
            r = s
            relative = float(np.linalg.norm(b - apply(x))) / norm_b
            break
        t = apply(s)
        omega = float(t @ s) / float(t @ t)
        x = x + alpha * p + omega * s
        r = s - omega * t
        rho = rho_new
        relative = float(np.linalg.norm(r)) / norm_b
        if relative < tolerance or time.perf_counter() - started > seconds:
            break
    true_relative = float(np.linalg.norm(b - apply(x))) / norm_b
    return {"x": x, "iterations": it, "relative_residual": true_relative, "resolved": true_relative < 10 * tolerance, "seconds": time.perf_counter() - started}


def residual_lifetimes(chain: Chain, ct: np.ndarray, A: np.ndarray) -> dict:
    """Killed jump chain on A: occupation-sampled residual life and entrance mean life, both clocks."""
    if not A.any() or A.all():
        return {"resolved": False, "reason": "A empty or whole space"}
    R = chain.rates
    idx, apply = _killed_operator(chain, A)
    solve_ct = bicgstab(apply, 1.0 / R[idx])
    solve_jump = bicgstab(apply, np.ones(len(idx)))
    out = {"iterations_ct": solve_ct["iterations"], "iterations_jump": solve_jump["iterations"], "relative_residual_ct": solve_ct["relative_residual"], "relative_residual_jump": solve_jump["relative_residual"], "seconds": solve_ct["seconds"] + solve_jump["seconds"]}
    if not (solve_ct["resolved"] and solve_jump["resolved"]):
        out.update({"resolved": False, "reason": "killed-chain solve did not reach tolerance"})
        return out
    h_ct = np.zeros(len(A))
    h_jump = np.zeros(len(A))
    h_ct[idx] = solve_ct["x"]
    h_jump[idx] = solve_jump["x"]
    valid, target_in = _boundary(chain, A)
    entering = valid & ~A[:, None] & target_in
    entrance = np.bincount(chain.T[entering], weights=(ct[:, None] * chain.W)[entering], minlength=len(A))
    entrance /= entrance.sum()
    rate_mass = ct * R
    out.update(
        {
            "entrance_mean_life_ct": float(entrance @ h_ct),
            "entrance_mean_life_jump": float(entrance @ h_jump),
            "occupation_residual_life_ct": float(ct[A] @ h_ct[A]) / float(ct[A].sum()),
            "occupation_residual_life_jump": float(rate_mass[A] @ h_jump[A]) / float(rate_mass[A].sum()),
            "resolved": True,
        }
    )
    return out


# --- ND: density-matched exchangeable comparator ------------------------------


def density_profile(states: np.ndarray, law: np.ndarray, m: int) -> np.ndarray:
    k = np.array([int(s).bit_count() for s in states]) if len(states) < 64 else _popcount(states)
    return np.bincount(k, weights=law, minlength=m + 1)


def _popcount(states: np.ndarray) -> np.ndarray:
    v = states.copy()
    c = np.zeros(len(v), dtype=np.int64)
    while v.any():
        c += v & 1
        v >>= 1
    return c


def nd_rates(p: np.ndarray) -> dict:
    """Metropolis birth/death rates for target weight phi_k = p_k / C(M, k) on every labelled k-edge graph.

    birth[k] = min(1, phi_{k+1}/phi_k) (k = 0..M-1); death[k] = min(1, phi_{k-1}/phi_k) (k = 1..M).
    Ratios are formed in logarithms.
    """
    m = len(p) - 1
    if (p <= 0).any():
        return {"resolved": False, "reason": "a density bin has zero mass", "zero_bins": [int(k) for k in np.nonzero(p <= 0)[0]]}
    log_phi = np.log(p) - np.array([math.lgamma(m + 1) - math.lgamma(k + 1) - math.lgamma(m - k + 1) for k in range(m + 1)])
    up = np.exp(np.minimum(0.0, log_phi[1:] - log_phi[:-1]))
    down = np.exp(np.minimum(0.0, log_phi[:-1] - log_phi[1:]))
    birth = np.concatenate([up, [0.0]])
    death = np.concatenate([[0.0], down])
    return {"birth": birth, "death": death, "log_phi": log_phi, "log_phi_range": float(log_phi.max() - log_phi.min()), "rare_bins": {str(k): float(p[k]) for k in range(m + 1) if p[k] < RARE_MASS}, "resolved": True}


def nd_chain(n: int, p: np.ndarray, target_mean_rate: float) -> tuple[Chain, np.ndarray, dict]:
    """The scaled ND chain on the full FREE space, its analytic CT law, and construction diagnostics."""
    m = len(edges(n))
    rates = nd_rates(p)
    if not rates["resolved"]:
        raise ValueError(rates["reason"])
    states = np.arange(1 << m, dtype=np.int64)
    x = bits(states, n)
    k = x.sum(axis=1)
    W_unscaled = np.where(x, rates["death"][k][:, None], rates["birth"][k][:, None])
    log_pi = rates["log_phi"][k]
    pi = np.exp(log_pi - log_pi.max())
    pi /= pi.sum()
    unscaled_mean = float(pi @ W_unscaled.sum(axis=1))
    c = target_mean_rate / unscaled_mean
    T = states[:, None] ^ (1 << np.arange(m))[None, :]
    chain = Chain(m, states, c * W_unscaled, T)
    phi = np.exp(rates["log_phi"] - rates["log_phi"].max())
    db = max(abs(phi[j] * rates["birth"][j] - phi[j + 1] * rates["death"][j + 1]) / max(phi[j] * rates["birth"][j], phi[j + 1] * rates["death"][j + 1]) for j in range(m))
    flow_in = np.zeros(len(states))
    for e in range(m):
        flow_in += pi[T[:, e]] * chain.W[T[:, e], e]
    global_balance = float(np.abs(flow_in - pi * chain.rates).sum() / (pi * chain.rates).sum())
    p_nd = np.bincount(k, weights=pi, minlength=m + 1)
    info = {
        "activity_scale": c,
        "birth": [float(v) for v in rates["birth"]],
        "death": [float(v) for v in rates["death"]],
        "density_l1_vs_target": float(np.abs(p_nd - p).sum()),
        "detailed_balance_max_relative": float(db),
        "global_balance_relative": global_balance,
        "log_phi_range": rates["log_phi_range"],
        "min_unscaled_transition_rate": float(min(rates["birth"][:m].min(), rates["death"][1:].min())),
        "mean_rate_ct": float(pi @ chain.rates),
        "mean_rate_relative_gap": abs(float(pi @ chain.rates) - target_mean_rate) / target_mean_rate,
        "rare_bins": rates["rare_bins"],
        "unscaled_mean_rate_ct": unscaled_mean,
    }
    return chain, pi, info


def jump_density(chain: Chain, ct: np.ndarray, n: int) -> np.ndarray:
    nu = ct * chain.rates
    nu /= nu.sum()
    return density_profile(chain.states, nu, len(edges(n)))


# --- lagged hub --------------------------------------------------------------


def lump_index(states: np.ndarray, n: int) -> tuple[np.ndarray, np.ndarray]:
    """Lump label (0..L-1) of every state under the permutations fixing 0 and 1, and one representative per lump."""
    best = states.copy()
    for rest in itertools.permutations(range(2, n)):
        best = np.minimum(best, gtobs.permute_codes(states, gtobs.permutation_tables(n, (0, 1) + rest)))
    labels, lump = np.unique(best, return_inverse=True)
    position = np.searchsorted(states, labels)
    return lump.astype(np.int64), position


def lumped_generator(chain: Chain, lump: np.ndarray, reps: np.ndarray) -> tuple[np.ndarray, float]:
    """Dense lumped generator from representatives, and the strong-lumpability defect over all states."""
    size = len(reps)
    valid = chain.T >= 0
    Q = np.zeros((size, size))
    for i, r in enumerate(reps):
        sel = valid[r]
        np.add.at(Q[i], lump[chain.T[r][sel]], chain.W[r][sel])
    # every state's aggregated rate into each lump must equal its representative's (strong lumpability)
    rows = np.broadcast_to(np.arange(len(lump))[:, None], chain.W.shape)[valid]
    dest = lump[chain.T[valid]]
    keys, inverse = np.unique(rows * size + dest, return_inverse=True)
    agg = np.bincount(inverse, weights=chain.W[valid])
    src, dst = keys // size, keys % size
    entry_defect = float(np.abs(agg - Q[lump[src], dst]).max())
    total_defect = float(np.abs(chain.rates - Q[lump].sum(axis=1)).max())
    defect = max(entry_defect, total_defect) / float(chain.rates.max())
    Q[np.diag_indices(size)] -= Q.sum(axis=1)
    return Q, defect


_PADE13 = (64764752532480000.0, 32382376266240000.0, 7771770303897600.0, 1187353796428800.0, 129060195264000.0, 10559470521600.0, 670442572800.0, 33522128640.0, 1323241920.0, 40840800.0, 960960.0, 16380.0, 182.0, 1.0)


def expm(A: np.ndarray) -> tuple[np.ndarray, int]:
    """Matrix exponential by Pade-13 scaling and squaring (Higham 2005); returns (exp(A), squarings)."""
    norm = float(np.abs(A).sum(axis=0).max())
    s = max(0, int(math.ceil(math.log2(norm / PADE13_THETA)))) if norm > PADE13_THETA else 0
    A = A / (2.0**s)
    b = _PADE13
    eye = np.eye(len(A))
    A2 = A @ A
    A4 = A2 @ A2
    A6 = A4 @ A2
    U = A @ (A6 @ (b[13] * A6 + b[11] * A4 + b[9] * A2) + b[7] * A6 + b[5] * A4 + b[3] * A2 + b[1] * eye)
    V = A6 @ (b[12] * A6 + b[10] * A4 + b[8] * A2) + b[6] * A6 + b[4] * A4 + b[2] * A2 + b[0] * eye
    E = np.linalg.solve(V - U, V + U)
    for _ in range(s):
        E = E @ E
    return E, s


def uniformised_expm_action(Q: np.ndarray, t: float, f: np.ndarray, *, tail: float = 1e-15, cap: int = 20_000) -> np.ndarray | None:
    """exp(tQ) f by uniformisation (cross-check only; None when it needs more than ``cap`` terms)."""
    lam = float(-np.diag(Q).min())
    if lam == 0.0 or t == 0.0:
        return f.copy()
    if lam * t > cap / 2:
        return None
    P = np.eye(len(Q)) + Q / lam
    term = f.copy()
    log_w = -lam * t
    out = math.exp(log_w) * term
    total = math.exp(log_w)
    k = 0
    while 1.0 - total > tail and k < cap:
        k += 1
        term = P @ term
        log_w += math.log(lam * t) - math.log(k)
        w = math.exp(log_w)
        out += w * term
        total += w
    return out


def pair_permutation_index(states: np.ndarray, n: int, v: int, u: int, *, alternative: bool = False) -> np.ndarray:
    """Index (= code, full FREE space) of sigma(x) for a permutation with sigma(v)=0, sigma(u)=1.

    The other vertices go to 2..n-1 in increasing order, or in decreasing order
    with ``alternative`` (a covariance check: both must give the same value of a
    Stab(0,1)-invariant function).
    """
    rest = [w for w in range(n) if w not in (v, u)]
    if alternative:
        rest = rest[::-1]
    perm = [0] * n
    perm[v], perm[u] = 0, 1
    for j, w in enumerate(rest):
        perm[w] = 2 + j
    return gtobs.permute_codes(states, gtobs.permutation_tables(n, tuple(perm)))


def hub_weights(states: np.ndarray, n: int) -> tuple[np.ndarray, np.ndarray]:
    """h(x, v) = 1/|argmax deg| on maximum-degree vertices (S_N-covariant ties), and the degree array."""
    deg = degrees(states, n)
    top = deg == deg.max(axis=1, keepdims=True)
    return top / top.sum(axis=1, keepdims=True), deg


def hub_lag_summary(states: np.ndarray, n: int, start_law: np.ndarray, G: np.ndarray, pair_index: dict) -> dict:
    """Hub and comparison-vertex degree and neighbour retention, given G(x) = E_x[X_01 at the lag]."""
    h, deg = hub_weights(states, n)
    x = bits(states, n)
    hub_deg = np.zeros(len(states))
    cmp_deg = np.zeros(len(states))
    hub_ret = np.zeros(len(states))
    cmp_ret = np.zeros(len(states))
    for v in range(n):
        for u in range(n):
            if u == v:
                continue
            g = G[pair_index[(v, u)]]
            present = x[:, slot(n, v, u)]
            hub_deg += h[:, v] * g
            cmp_deg += g / n
            hub_ret += h[:, v] * g * present
            cmp_ret += g * present / n
    hub0 = float(start_law @ (h * deg).sum(axis=1))
    cmp0 = float(start_law @ deg.mean(axis=1))
    out = {"comparison_degree": float(start_law @ cmp_deg), "comparison_retained_neighbours": float(start_law @ cmp_ret), "hub_degree": float(start_law @ hub_deg), "hub_retained_neighbours": float(start_law @ hub_ret)}
    out["gap"] = out["hub_degree"] - out["comparison_degree"]
    out["hub_retention_fraction"] = out["hub_retained_neighbours"] / hub0 if hub0 > 0 else None
    out["comparison_retention_fraction"] = out["comparison_retained_neighbours"] / cmp0 if cmp0 > 0 else None
    return out


def jump_propagate(chain: Chain, f: np.ndarray, steps: int) -> list[np.ndarray]:
    """[f, Pf, P^2 f, ..., P^steps f] for the jump chain (full space)."""
    P = chain.W / chain.rates[:, None]
    T = np.maximum(chain.T, 0)
    P = np.where(chain.T >= 0, P, 0.0)
    out = [f.copy()]
    for _ in range(steps):
        out.append((P * out[-1][T]).sum(axis=1))
    return out


def lagged_hub(chain: Chain, ct: np.ndarray, n: int, lags: tuple[int, ...], *, lumped: tuple | None = None) -> dict:
    """Lagged hub control in both clocks (D-2, D-7, D-9 of the E5 audit)."""
    started = time.perf_counter()
    states = chain.states
    if len(states) != 1 << len(edges(n)) or not np.array_equal(states, np.arange(len(states))):
        raise ValueError("lagged hub expects the full FREE space indexed by code")
    R = chain.rates
    mean_rate = float(ct @ R)
    nu = ct * R / mean_rate
    f = bits(states, n)[:, slot(n, 0, 1)].astype(float)
    pair_index = {(v, u): pair_permutation_index(states, n, v, u) for v in range(n) for u in range(n) if u != v}
    alt_index = {(v, u): pair_permutation_index(states, n, v, u, alternative=True) for v in range(n) for u in range(n) if u != v}
    # jump clock, full space
    jump_values = jump_propagate(chain, f, max(lags))
    jump = {str(d): hub_lag_summary(states, n, nu, jump_values[d], pair_index) for d in lags}
    # continuous clock, lumped exact exponential
    lump, reps = lumped if lumped is not None else lump_index(states, n)
    Q, defect = lumped_generator(chain, lump, reps)
    f_bar = f[reps]
    pi_bar = np.bincount(lump, weights=ct, minlength=len(reps))
    positive = sorted(d for d in lags if d > 0)
    times = {d: d / mean_rate for d in positive}
    checks = {"lumpability_defect_relative": defect}
    props = {}
    base, squarings = expm(times[positive[0]] * Q)
    props[positive[0]] = base
    for prev, d in zip(positive[:-1], positive[1:]):
        if d == 2 * prev:
            props[d] = props[prev] @ props[prev]
        else:
            props[d], _ = expm(times[d] * Q)
    # non-dyadic semigroup check: P(t_last) against P(3/4 t_last) P(1/4 t_last)
    three_quarter, squarings_check = expm(0.75 * times[positive[-1]] * Q)
    quarter, _ = expm(0.25 * times[positive[-1]] * Q)
    checks["squarings_first_lag"] = squarings
    checks["squarings_semigroup_check"] = squarings_check
    checks["row_sum_max_error"] = max(float(np.abs(Pm.sum(axis=1) - 1.0).max()) for Pm in props.values())
    checks["min_entry"] = min(float(Pm.min()) for Pm in props.values())
    checks["stationarity_l1"] = max(float(np.abs(pi_bar @ Pm - pi_bar).sum()) for Pm in props.values())
    checks["semigroup_max"] = float(np.abs(three_quarter @ quarter - props[positive[-1]]).max())
    uni = uniformised_expm_action(Q, times[positive[-1]], f_bar)
    checks["uniformisation_vs_expm_max"] = float(np.abs(uni - props[positive[-1]] @ f_bar).max()) if uni is not None else None
    # lumped jump chain against the full-space propagation (lumping cross-check)
    lam_rates = -np.diag(Q)
    Pbar = Q / lam_rates[:, None]
    Pbar[np.diag_indices(len(Q))] = 0.0
    lumped_jump = np.linalg.matrix_power(Pbar, max(lags)) @ f_bar
    checks["lumped_vs_full_jump_max"] = float(np.abs(lumped_jump[lump] - jump_values[max(lags)]).max())
    ct_rows = {"0": hub_lag_summary(states, n, ct, f, pair_index)}
    for d in positive:
        G = (props[d] @ f_bar)[lump]
        ct_rows[str(d)] = hub_lag_summary(states, n, ct, G, pair_index)
        ct_rows[str(d)]["time"] = times[d]
    G_last = (props[positive[-1]] @ f_bar)[lump]
    alt = hub_lag_summary(states, n, ct, G_last, alt_index)
    checks["pair_permutation_covariance_max"] = max(abs(alt[k] - ct_rows[str(positive[-1])][k]) for k in ("hub_degree", "comparison_degree", "hub_retained_neighbours"))
    for rows in (ct_rows, jump):
        g0 = rows["0"]["gap"]
        for row in rows.values():
            row["normalised_gap"] = row["gap"] / g0 if g0 != 0 else None
    return {"checks": checks, "continuous": ct_rows, "jump": jump, "lag_time_unit": 1.0 / mean_rate, "lumped_states": int(len(reps)), "seconds": time.perf_counter() - started}


# --- NULL closed forms (independent unit-rate bits; definitions note section 6) ----------


def null_closed_forms(n: int) -> dict:
    """Prevalence, boundary flux J and eligible internal flux (Omega * J) of each primary predicate under NULL.

    Every slot is an independent unit-rate bit, so pi is uniform, q = M, and
    the centre degree is Binomial(n-1, 1/2). Lifetimes: L_ct = prevalence/J,
    L_jump = M * L_ct.
    """
    s = n - 2
    d = [math.comb(n - 1, k) / 2 ** (n - 1) for k in range(n)]
    pi_tri = (1 - 0.75**s) / 2
    out = {
        "I_TRI": {"prevalence": 1 / 8, "flux": 3 / 8, "omega_flux": 0.0},
        "I_STAR": {"prevalence": 1 / 8, "flux": 3 / 8, "omega_flux": 0.0},
        "I_2PATH": {"prevalence": 1 / 4, "flux": 1 / 2, "omega_flux": 0.0},
        "F_TRI": {"prevalence": pi_tri, "flux": pi_tri + s * 0.25 * 0.75 ** (s - 1), "omega_flux": 0.5 * s * (1 - 0.75 ** (s - 1))},
        "F_STAR": {"prevalence": sum(d[3:]), "flux": 3 * d[3] if n > 3 else 0.0, "omega_flux": sum(d[k] * ((n - 1 - k) + k * (k >= 4)) for k in range(3, n))},
        "F_2PATH": {"prevalence": sum(d[2:]), "flux": 2 * d[2], "omega_flux": sum(d[k] * ((n - 1 - k) + k * (k >= 3)) for k in range(2, n))},
    }
    return out


def null_lag_closed_forms(n: int, lags: tuple[int, ...]) -> dict:
    """NULL lagged hub: normalised gap and neighbour retention in both clocks (t = lag / M in continuous time)."""
    m = len(edges(n))
    return {
        "continuous": {str(d): {"normalised_gap": math.exp(-2 * d / m), "retention": 0.5 + 0.5 * math.exp(-2 * d / m)} for d in lags},
        "jump": {str(d): {"normalised_gap": (1 - 2 / m) ** d, "retention": 0.5 + 0.5 * (1 - 2 / m) ** d} for d in lags},
    }
