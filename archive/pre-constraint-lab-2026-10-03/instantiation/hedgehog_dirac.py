"""Instantiation phase — WP-B: a Dirac fermion in a hedgehog → Jackiw–Rebbi zero mode.

Test of the θ=π-generation claim (scope: docs/theta-generation-scope-2026-07-13.md).
Abanov–Wiegmann: integrating out N Dirac fermions gapped by the order parameter
gives Θ = Nπ, so a *single* Dirac cone ⇒ θ=π. Jackiw–Rebbi: a Dirac fermion whose
mass is a degree-1 hedgehog binds **exactly one zero mode**, so the soliton carries
induced charge ±½ — the θ=π Witten half-charge. This is the concrete, could-fail
signature.

Minimal faithful model: a genuine 3D hedgehog mass (a 3-vector order parameter)
coupled to a 3D Dirac fermion needs 3 kinetic + 3 mass + 1 Wilson = 7 mutually
anticommuting matrices → an **8-band** lattice model. The Wilson term isolates a
single Dirac cone (removes doublers); in the topological window it leaves one
effective cone, so a degree-1 hedgehog should bind one mid-gap state localized at
the core, with a charge-conjugation-symmetric spectrum ⇒ induced charge ½.

We diagonalise (sparse, shift-invert near E=0) and report: the low-|E| spectrum,
whether there is an isolated near-zero mode, and where it lives (core vs surface).
Honest test — it can be clean (PASS) or messy (STALL), per the scope.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def k3(a, b, c):
    return np.kron(np.kron(a, b), c)


# 7 mutually anticommuting 8×8 matrices (Jordan–Wigner):
# kinetic g[0..2], hedgehog mass g[3..5], Wilson g[6].
g = [k3(X, I2, I2), k3(Y, I2, I2), k3(Z, X, I2), k3(Z, Y, I2),
     k3(Z, Z, X), k3(Z, Z, Y), k3(Z, Z, Z)]


def build_hamiltonian(N: int, m: float, M: float) -> sp.csr_matrix:
    """8-band Wilson–Dirac fermion with a degree-1 hedgehog mass, open boundaries."""
    xs = (np.arange(N) - (N - 1) / 2)  # half-integers: no site at r=0

    def idx(i, j, k):
        return i * N * N + j * N + k

    rr, cc = np.meshgrid(np.arange(8), np.arange(8), indexing="ij")
    rows, cols, vals = [], [], []

    def add(r0, c0, B):
        rows.append((r0 + rr).ravel())
        cols.append((c0 + cc).ravel())
        vals.append(B.ravel())

    hop = [(-0.5j) * g[l] - 0.5 * g[6] for l in range(3)]  # kinetic + Wilson hop
    dirs = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]

    for i in range(N):
        for j in range(N):
            for k in range(N):
                b = 8 * idx(i, j, k)
                x, y, z = xs[i], xs[j], xs[k]
                r = np.sqrt(x * x + y * y + z * z)
                nx, ny, nz = x / r, y / r, z / r  # hedgehog n = r̂
                onsite = m * (nx * g[3] + ny * g[4] + nz * g[5]) + M * g[6]
                add(b, b, onsite)
                for l, (di, dj, dk) in enumerate(dirs):
                    ii, jj, kk = i + di, j + dj, k + dk
                    if ii < N and jj < N and kk < N:  # open BC
                        b2 = 8 * idx(ii, jj, kk)
                        add(b, b2, hop[l])
                        add(b2, b, hop[l].conj().T)

    n = 8 * N ** 3
    H = sp.coo_matrix((np.concatenate(vals),
                       (np.concatenate(rows), np.concatenate(cols))),
                      shape=(n, n)).tocsr()
    return H


def analyse(N: int, m: float, M: float) -> tuple[np.ndarray, tuple[float, float]]:
    H = build_hamiltonian(N, m, M)
    # dense full spectrum (fast at small N; shows the whole gap + ±E symmetry)
    vals, vecs = np.linalg.eigh(H.toarray())
    order = np.argsort(np.abs(vals))
    vals, vecs = vals[order], vecs[:, order]
    # localisation of the mode nearest E=0
    psi = vecs[:, 0].reshape(N, N, N, 8)
    dens = (np.abs(psi) ** 2).sum(axis=3)
    c = (N - 1) / 2
    ii, jj, kk = np.unravel_index(np.argmax(dens), dens.shape)
    core_R = N / 4.0
    Xg, Yg, Zg = np.meshgrid(np.arange(N) - c, np.arange(N) - c, np.arange(N) - c, indexing="ij")
    Rg = np.sqrt(Xg ** 2 + Yg ** 2 + Zg ** 2)
    core_frac = dens[Rg <= core_R].sum() / dens.sum()
    peak_r = np.sqrt((ii - c) ** 2 + (jj - c) ** 2 + (kk - c) ** 2)
    return vals, (core_frac, peak_r)


def main() -> int:
    N, m = 8, 1.0
    print(f"Hedgehog–Dirac (8-band Wilson–Dirac), grid {N}³ dense, hedgehog mass m={m}.\n")
    print("Jackiw–Rebbi expectation: ONE isolated mid-gap mode at the core, spectrum ±E symmetric.\n")
    ok = False
    for M in (1.0, 1.5, 2.0, 2.5, 3.0):
        vals, (core_frac, peak_r) = analyse(N, m, M)
        near = np.sort(np.abs(vals))
        gap = near[near > 0.05][0] if (near > 0.05).any() else float("nan")
        n_zero = int((np.abs(vals) < 0.05).sum())
        print(f"  Wilson M={M}:")
        print(f"    |E| nearest 0: {', '.join(f'{v:.4f}' for v in near[:6])}")
        print(f"    zero modes (|E|<0.05): {n_zero};  next state |E|≈{gap:.3f} (bulk gap)")
        print(f"    mode-0 core-localised fraction: {core_frac:.2f};  peak radius: {peak_r:.1f} (0=centre)")
        clean = (n_zero == 1 and gap > 0.15 and core_frac > 0.3)
        print(f"    → {'clean single core zero mode (JR ½)' if clean else 'not clean here'}\n")
        ok = ok or clean
    print("  RESULT:", "PASS — single Dirac cone binds one hedgehog zero mode ⇒ induced charge ½ ⇒ θ=π"
          if ok else "INCONCLUSIVE — no clean single core zero mode in this window (see scope §6)")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
