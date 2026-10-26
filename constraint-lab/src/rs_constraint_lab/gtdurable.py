"""Durable renewal: first-renewal distributions and post-renewal survival over anchor-local events (GT-P011, E5C).

Read-only observer functionals of a finite single-toggle chain and its CT stationary law.
No rule reads the anchor, the original-partner set S0 or any quantity here (8G gate not
engaged). Definitions and proofs: ``gravity-time/docs/e5c-durable-renewal-definitions.md``.

For a flexible predicate A (F_2PATH, F_TRI) and an entry-set size s:

* entry states are mapped by permutations fixing the anchor into a canonical frame in which
  S0 = the first s candidates; their Palm entrance weights form a row vector mu_s;
* R = {x in A : no member of S0 participates}, B = A minus R;
* phi = mu_s|B (I - P_BB)^-1 P_B->R is the exact (unnormalised) first-renewal distribution;
* between anchor-local events the chain moves by remote jumps, which never leave R (T13);
  the local-event kernel on R is K = (I - P_rem,RR)^-1 P_loc, and survival through h local
  events with the original partners absent is phi K_RR^h 1;
* after first renewal the chain leaves R almost surely, either by an original partner
  returning (into A minus R) or by exit (out of A): exclusive and exhaustive causes.
"""

from __future__ import annotations

import numpy as np

from rs_constraint_lab import gtobs
from rs_constraint_lab import gtpersist as P
from rs_constraint_lab import gtrenew as RN
from rs_constraint_lab.gte0a import Chain

DURABLE_VERSION = "gt-durable/v1"
PREDICATES = ("F_2PATH", "F_TRI")
HORIZONS = (0, 1, 2, 4, 8)
SOLVE_TOLERANCE = 1e-12
SOLVE_CAP = 20_000
SOLVE_SECONDS = 600.0
DENSE_LIMIT = 4096


# --- row solves on a killed sub-chain ----------------------------------------------


def _sub(chain: Chain, mask: np.ndarray, cols: np.ndarray | None = None):
    """Jump-chain transitions from mask-states that stay in mask (optionally only through slots in cols)."""
    idx = np.nonzero(mask)[0]
    local = np.full(len(mask), -1, dtype=np.int64)
    local[idx] = np.arange(len(idx))
    Pj = chain.W[idx] / chain.rates[idx, None]
    T = chain.T[idx]
    keep = (T >= 0) & np.where(T >= 0, mask[np.maximum(T, 0)], False)
    if cols is not None:
        keep &= cols[None, :]
    rows, slots = np.nonzero(keep)
    return idx, local, rows, local[T[rows, slots]], Pj[rows, slots]


def row_solve(chain: Chain, mask: np.ndarray, rhs: np.ndarray, *, cols: np.ndarray | None = None, dense: bool | None = None) -> dict:
    """x (I - P_mm) = rhs on the states in mask (P restricted to transitions within mask, optionally via cols).

    rhs and x are full-length row vectors (zero outside mask). BiCGSTAB on the transposed operator;
    a dense direct solve as an independent route when the system is small.
    """
    idx, local, r, c, v = _sub(chain, mask, cols)
    b = rhs[idx]
    out = {"size": int(len(idx))}
    x = np.zeros(len(mask))
    if len(idx) == 0 or not b.any():
        out.update({"x": x, "resolved": True, "relative_residual": 0.0, "iterations": 0})
        return out

    def apply(y):  # y (I - P_mm), as a column operation on y
        z = y.copy()
        np.subtract.at(z, c, y[r] * v)
        return z

    sol = P.bicgstab(apply, b, tolerance=SOLVE_TOLERANCE, cap=SOLVE_CAP, seconds=SOLVE_SECONDS)
    out.update({"iterations": sol["iterations"], "relative_residual": sol["relative_residual"], "resolved": bool(sol["resolved"])})
    use_dense = dense if dense is not None else len(idx) <= DENSE_LIMIT
    if use_dense:
        M = np.eye(len(idx))
        np.add.at(M, (r, c), -v)
        xd = np.linalg.solve(M.T, b)
        out["dense_max_abs_difference"] = float(np.abs(xd - sol["x"]).max())
    x[idx] = sol["x"]
    out["x"] = x
    return out


def step(chain: Chain, row: np.ndarray, *, cols: np.ndarray | None = None) -> np.ndarray:
    """One jump-chain step of a row vector (optionally only through slots in cols); full-length result."""
    Pj = chain.W / chain.rates[:, None]
    if cols is not None:
        Pj = np.where(cols[None, :], Pj, 0.0)
    out = np.zeros(len(row))
    nz = np.nonzero(row)[0]
    np.add.at(out, chain.T[nz].ravel(), (row[nz, None] * Pj[nz]).ravel())
    return out


# --- canonical entry distributions ---------------------------------------------------


def canonical_entries(chain: Chain, ct: np.ndarray, n: int, predicate: str, vertices: tuple[int, ...]) -> dict:
    """Palm entrance weights mapped to the canonical frame, by entry-set size."""
    A = P.predicate_mask(chain.states, n, predicate, vertices)
    mu = RN.entrance_weights(chain, ct, A)
    part = RN.participation(chain.states, n, predicate, vertices)
    anc = RN.anchor_vertices(predicate, vertices)
    cand = RN.candidates(n, predicate, vertices)
    index = RN._index_of(chain)
    entries = np.nonzero(mu > 0)[0]
    sizes = part[entries].sum(axis=1)
    by_size = {}
    for s in sorted({int(v) for v in sizes}):
        can = cand[:s]
        row = np.zeros(len(A))
        for i in entries[sizes == s]:
            s0 = [v for v in cand if part[i, v]]
            perm = RN._perm_map(n, {**{a: a for a in anc}, **dict(zip(s0, can))})
            j = index[gtobs.permute_codes(chain.states[i : i + 1], gtobs.permutation_tables(n, perm))[0]]
            row[j] += mu[i]
        by_size[s] = row
    return {"A": A, "part": part, "candidates": cand, "J": float(mu.sum()), "by_size": by_size}


# --- durable renewal for one predicate --------------------------------------------------


def durable(chain: Chain, ct: np.ndarray, n: int, predicate: str, vertices: tuple[int, ...], horizons: tuple[int, ...] = HORIZONS) -> dict:
    ce = canonical_entries(chain, ct, n, predicate, vertices)
    A, part, cand, J = ce["A"], ce["part"], ce["candidates"], ce["J"]
    local = RN.local_mask(n, predicate, vertices)
    remote = ~local
    q_loc = chain.W[:, local].sum(axis=1)
    out: dict = {"entry_flux": J, "classes": {}, "unresolved": []}
    totals = {"phi": 0.0, "surv": {h: 0.0 for h in horizons}, "mass_feasible": 0.0}
    for s, mu_s in ce["by_size"].items():
        w = float(mu_s.sum())
        cls: dict = {"entry_weight": w / J, "feasible": RN.renewal_feasible(n, predicate, vertices, s), "solves": {}}
        out["classes"][str(s)] = cls
        if not cls["feasible"]:
            cls["status"] = "STRUCTURALLY_IMPOSSIBLE"
            continue
        can = cand[:s]
        R = A & ~part[:, can].any(axis=1)
        Bm = A & ~R
        cls["renewed_states"] = int(R.sum())
        # T13 frozen check: no remote transition from R leaves R
        TR = chain.T[R]
        tgt_in_R = np.where(TR >= 0, R[np.maximum(TR, 0)], False)
        cls["remote_closure_violations"] = int((~tgt_in_R & remote[None, :] & (chain.W[R] > 0)).sum())
        # T14: is any local transition from R back into R possible at all?
        cls["local_RR_transitions"] = int((tgt_in_R & local[None, :] & (chain.W[R] > 0)).sum())
        cls["post_renewal_status"] = "computed" if cls["local_RR_transitions"] > 0 else "STRUCTURALLY_ZERO_FOR_H_GE_1"
        # first-renewal distribution
        sol_b = row_solve(chain, Bm, np.where(Bm, mu_s, 0.0))
        cls["solves"]["first_renewal"] = {k: v for k, v in sol_b.items() if k != "x"}
        nxt = step(chain, sol_b["x"])
        phi = np.where(R, nxt, 0.0)
        m_phi = float(phi.sum())
        cls["R0"] = m_phi / w
        totals["phi"] += m_phi
        totals["mass_feasible"] += w
        if m_phi == 0.0:
            cls["status"] = "renewal_probability_zero"
            continue
        cls["status"] = "computed"
        # diagnostic: first-renewal law versus the stationary law restricted to R
        piR = np.where(R, ct, 0.0)
        cls["first_hit_vs_stationary_l1"] = float(np.abs(phi / m_phi - piR / piR.sum()).sum())
        cls["local_share_at_first_renewal"] = float((phi * q_loc / chain.rates).sum() / m_phi)
        # survival through local events
        surv = {0: phi.copy()}
        cur = phi.copy()
        first_split = None
        for h in range(1, max(horizons) + 1):
            sol_r = row_solve(chain, R, cur, cols=remote)
            cls["solves"][f"remote_h{h}"] = {k: v for k, v in sol_r.items() if k != "x"}
            after = step(chain, sol_r["x"], cols=local)
            if h == 1:
                first_split = {"stay": float(after[R].sum()), "return": float(after[A & ~R].sum()), "exit": float(after[~A].sum())}
            cur = np.where(R, after, 0.0)
            if h in horizons:
                surv[h] = cur.copy()
        cls["U"] = {str(h): float(surv[h].sum()) / w for h in horizons}
        cls["C"] = {str(h): float(surv[h].sum()) / m_phi for h in horizons}
        for h in horizons:
            totals["surv"][h] += float(surv[h].sum())
        cls["immediate_original_return"] = first_split["return"] / m_phi
        cls["immediate_exit"] = first_split["exit"] / m_phi
        cls["first_local_split_sum"] = (first_split["stay"] + first_split["return"] + first_split["exit"]) / m_phi
        # eventual cause of leaving R
        sol_e = row_solve(chain, R, phi)
        cls["solves"]["leave_R"] = {k: v for k, v in sol_e.items() if k != "x"}
        lv = step(chain, sol_e["x"])
        cls["return_before_exit"] = float(lv[A & ~R].sum()) / m_phi
        cls["exit_before_return"] = float(lv[~A].sum()) / m_phi
        for name, sv in cls["solves"].items():
            if not sv.get("resolved"):
                out["unresolved"].append(f"size{s}:{name}")
    if totals["mass_feasible"] == 0.0:
        out.update({"status": "STRUCTURALLY_IMPOSSIBLE", "R0": None, "U": {str(h): None for h in horizons}, "C": {str(h): None for h in horizons}, "feasible_entry_fraction": 0.0, "resolved": True})
        return out
    out["status"] = "computed"
    out["R0"] = totals["phi"] / J
    out["U"] = {str(h): totals["surv"][h] / J for h in horizons}
    out["C"] = {str(h): (totals["surv"][h] / totals["phi"]) if totals["phi"] > 0 else None for h in horizons}
    out["feasible_entry_fraction"] = totals["mass_feasible"] / J
    if predicate == "F_TRI":
        big = [s for s in ce["by_size"] if s >= 2 and out["classes"][str(s)].get("status") == "computed"]
        mass = sum(float(ce["by_size"][s].sum()) for s in big)
        phi_big = sum(out["classes"][str(s)]["R0"] * float(ce["by_size"][s].sum()) for s in big)
        out["size_ge2"] = {"entry_weight": mass / J, "R0": phi_big / mass if mass else None,
                           "U": {str(h): (sum(out["classes"][str(s)]["U"][str(h)] * float(ce["by_size"][s].sum()) for s in big) / mass) if mass else None for h in horizons},
                           "C": {str(h): (sum(out["classes"][str(s)]["U"][str(h)] * float(ce["by_size"][s].sum()) for s in big) / phi_big) if phi_big else None for h in horizons}}
    out["resolved"] = not out["unresolved"]
    return out


def analyse_law(chain: Chain, ct: np.ndarray, n: int, *, relabelled: bool = True) -> dict:
    out: dict = {"predicates": {}, "relabelled": {}}
    for p in PREDICATES:
        out["predicates"][p] = durable(chain, ct, n, p, P.primary_instance(p))
        if relabelled:
            out["relabelled"][p] = durable(chain, ct, n, p, P.relabelled_instance(p, n))
    return out
