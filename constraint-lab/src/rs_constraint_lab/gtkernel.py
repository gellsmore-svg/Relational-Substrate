"""Vectorised label-covariant template kernels for the GT programme (E1 machinery).

``build_kernel`` matches every rule instance against every state, which is
O(states x slots x rules) in Python and does not reach N=7 (2^21 states, up to
840 path instances). The templates used by GT are label-covariant and
multiply once per satisfying witness, so a toggle's weight depends only on
witness counts:

  closure    w_T(ab) = #{c : x_ac & x_bc}
  adjacency  w_W(ab) = #{c : x_ac} + #{c : x_bc}           (c not in {a, b})
  path       w_P(ab) = sum over end in {a, b} of
                       #{(c, d) : x_end,c & x_c,d}          (c, d not in {a, b}, c != d)

A form component with factor f contributes f^w when the relation is absent; a
dissolve component with factor g contributes g^w when it is present. A
prohibit factor contributes 0 if w > 0 and 1 otherwise. The HELD scaffold
sets the dissolve weight of the three source relations to 0. W4 factors are
powers of two, so float64 weights are exact and must equal ``build_kernel``'s
Fraction weights exactly; the tests check that bit for bit.

Rates are computed for every state of the candidate space (all states in
FREE; all states containing the source triangle in HELD), then the reachable
class from the declared start is found by breadth-first search over arrays.
"""

from __future__ import annotations

import itertools
import time

import numpy as np

from rs_constraint_lab import gt0
from rs_constraint_lab.gte0a import COMPONENT_K, FACTORS, SOURCE, Chain
from rs_constraint_lab.state import edges

KERNEL_VERSION = "gt-vectorised-kernel/v1"
LAZY_CAP = 2_000_000
LAZY_TOLERANCE = 1e-15
STATIONARY_RESIDUAL_TOLERANCE = 1e-12


def candidate_states(n: int, mode: str) -> np.ndarray:
    slots = len(edges(n))
    if mode == "FREE":
        return np.arange(1 << slots, dtype=np.int64)
    if mode != "HELD":
        raise ValueError(f"unknown mode {mode}")
    source_mask = gt0.start_state(n, "HELD")
    free = [e for e in range(slots) if not (source_mask >> e) & 1]
    codes = np.zeros(1 << len(free), dtype=np.int64)
    pattern = np.arange(1 << len(free), dtype=np.int64)
    for j, e in enumerate(free):
        codes |= ((pattern >> j) & 1) << e
    return codes | source_mask


def witness_counts(states: np.ndarray, n: int, kind: str) -> np.ndarray:
    """Witness count for every (state, slot) for one component kind (int16)."""
    edge_list = edges(n)
    position = {pair: i for i, pair in enumerate(edge_list)}

    def bit(a: int, b: int) -> np.ndarray:
        return ((states >> position[(min(a, b), max(a, b))]) & 1).astype(np.int16)

    cache: dict[tuple[int, int], np.ndarray] = {}

    def x(a: int, b: int) -> np.ndarray:
        key = (min(a, b), max(a, b))
        if key not in cache:
            cache[key] = bit(a, b)
        return cache[key]

    out = np.zeros((len(states), len(edge_list)), dtype=np.int16)
    for e, (a, b) in enumerate(edge_list):
        others = [c for c in range(n) if c not in (a, b)]
        if kind.startswith("close"):
            for c in others:
                out[:, e] += x(a, c) & x(b, c)
        elif kind == "adj_form":
            for c in others:
                out[:, e] += x(a, c) + x(b, c)
        elif kind.startswith("path"):
            for end in (a, b):
                for c in others:
                    reach = np.zeros(len(states), dtype=np.int16)
                    for d in others:
                        if d != c:
                            reach += x(c, d)
                    out[:, e] += x(end, c) * reach
        else:
            raise ValueError(f"unknown component {kind}")
    return out


def weights(states: np.ndarray, n: int, mode: str, components: list[tuple[str, str]], factors: dict | None = None) -> np.ndarray:
    """Event weight of every (state, slot) under the listed components and the mode's scaffold.

    ``factors`` is a grade-to-factor table from ``weights.alphabet_factors``;
    the default is W4, the alphabet of every GT round so far.
    """
    table = FACTORS if factors is None else factors
    slots = len(edges(n))
    present = ((states[:, None] >> np.arange(slots)) & 1).astype(bool)
    W = np.ones((len(states), slots))
    for kind, grade in components:
        if kind not in COMPONENT_K:
            raise ValueError(f"unknown component {kind}")
        factor = float(table[grade])
        count = witness_counts(states, n, kind)
        if factor == 0.0:
            term = np.where(count > 0, 0.0, 1.0)
        else:
            term = np.power(factor, count.astype(np.float64))
        acts_on = ~present if kind.endswith("_form") else present
        W = np.where(acts_on, W * term, W)
    if mode == "HELD":
        source_slots = gt0.held_slot_indices(n)
        for e in source_slots:
            W[present[:, e], e] = 0.0
    return W


def reachable_chain(n: int, mode: str, components: list[tuple[str, str]], factors: dict | None = None) -> tuple[Chain, dict]:
    """The reachable class from the declared start as a Chain, plus timings."""
    started = time.perf_counter()
    space = candidate_states(n, mode)
    W_all = weights(space, n, mode, components, factors)
    slots = W_all.shape[1]
    index = np.full(1 << slots, -1, dtype=np.int64)
    index[space] = np.arange(len(space))
    T_all = np.empty(W_all.shape, dtype=np.int64)
    for e in range(slots):
        T_all[:, e] = index[space ^ (1 << e)]
    if ((T_all < 0) & (W_all > 0)).any():
        raise ValueError("a positive rate leaves the candidate space")
    built = time.perf_counter()
    start = int(index[gt0.start_state(n, mode)])
    seen = np.zeros(len(space), dtype=bool)
    seen[start] = True
    frontier = np.array([start])
    while frontier.size:
        targets = T_all[frontier][W_all[frontier] > 0]
        fresh = np.unique(targets[~seen[targets]])
        seen[fresh] = True
        frontier = fresh
    keep = np.nonzero(seen)[0]
    remap = np.full(len(space), -1, dtype=np.int64)
    remap[keep] = np.arange(len(keep))
    T = np.where(T_all[keep] >= 0, remap[np.maximum(T_all[keep], 0)], -1)
    chain = Chain(slots, space[keep], W_all[keep], T)
    if ((chain.T < 0) & (chain.W > 0)).any():
        raise ValueError("a positive rate leaves the reachable class")
    return chain, {"build_seconds": built - started, "reach_seconds": time.perf_counter() - built}


def stationary_sparse(chain: Chain, *, start: np.ndarray | None = None, tolerance: float = LAZY_TOLERANCE, cap: int = LAZY_CAP) -> dict:
    """Jump-chain stationary law by lazy power iteration on arrays, then pi_ct = pi / R.

    Same convention as G0/E0 (``gte0a.stationary``); no dense matrix is formed.
    """
    R = chain.rates
    if (R <= 0).any():
        return {"resolved": False, "reason": "zero total rate in the class"}
    P = chain.W / R[:, None]
    valid = (chain.T >= 0) & (P > 0)
    rows = np.broadcast_to(np.arange(len(R))[:, None], P.shape)[valid]
    cols = chain.T[valid]
    vals = P[valid]
    size = len(R)
    pi = np.full(size, 1.0 / size) if start is None else start / start.sum()
    iterations = 0
    started = time.perf_counter()
    for iterations in range(1, cap + 1):
        moved = np.bincount(cols, weights=pi[rows] * vals, minlength=size)
        nxt = 0.5 * (pi + moved)
        delta = float(np.abs(nxt - pi).sum())
        pi = nxt
        if delta < tolerance:
            break
    moved = np.bincount(cols, weights=pi[rows] * vals, minlength=size)
    residual = float(np.abs(moved - pi).sum())
    out = {"iterations": iterations, "method": "lazy_iteration_sparse", "residual": residual, "seconds": time.perf_counter() - started}
    if residual > STATIONARY_RESIDUAL_TOLERANCE or (pi < -1e-15).any():
        out.update({"reason": "residual above tolerance", "resolved": False})
        return out
    pi = np.clip(pi, 0.0, None)
    pi /= pi.sum()
    ct = pi / R
    ct /= ct.sum()
    out.update({"ct": ct, "jump": pi, "mean_rate_ct": float(ct @ R), "resolved": True})
    return out


def all_e0_components() -> dict[str, dict[str, list[tuple[str, str]]]]:
    """Every family-grade executed in E0A and E0B, keyed as in their tables."""
    from rs_constraint_lab import gte0a, gte0b

    merged: dict[str, dict[str, list[tuple[str, str]]]] = {}
    for families in (gte0a.FAMILIES, gte0b.FAMILIES):
        for family, grades in families.items():
            for grade, components in grades.items():
                merged.setdefault(family, {})[grade] = components
    return merged


def compare_with_build_kernel(family: str, grade: str, n: int, mode: str, families: dict) -> dict:
    """Exact comparison of reachable class, targets and weights against the reference path."""
    from rs_constraint_lab import gte0a

    reference = gte0a.chain_from_kernel(gte0a.build(family, grade, n, mode, families), gt0.start_state(n, mode))
    fast, _ = reachable_chain(n, mode, families[family][grade])
    same_states = np.array_equal(reference.states, fast.states)
    return {
        "max_weight_difference": float(np.abs(reference.W - fast.W).max()) if same_states else None,
        "same_states": bool(same_states),
        "same_targets": bool(same_states and np.array_equal(reference.T, fast.T)),
        "weights_identical": bool(same_states and np.array_equal(reference.W, fast.W)),
    }


def path_witness_total(n: int) -> int:
    return len(list(itertools.combinations(range(n), 2))) * 2 * (n - 2) * (n - 3)
