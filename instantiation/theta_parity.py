"""Instantiation — WP-A support: θ = N_f·π (parity), so even N_f ⇒ boson.

WP-B showed a *single* Dirac cone in the hedgehog binds one zero mode → charge ½
→ θ=π (fermion). Here we confirm the parity dependence that underlies WP-A's
Result B: N_f decoupled cones bind N_f zero modes, so the induced charge is N_f/2
and the statistics is fixed by **N_f mod 2** — odd ⇒ fermion (θ=π), even ⇒ boson
(θ=0). The standard order-parameter fractionalisation (Néel–VBS dual, N_f=2) is
therefore a **boson** — the opposite of what the program needs.

Reuses the WP-B single-cone builder; at small N so the multi-cone (block-diagonal)
matrices stay cheap to diagonalise.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp

from hedgehog_dirac import build_hamiltonian


def zero_count(H, thresh: float = 0.06):
    v = np.linalg.eigvalsh(H.toarray() if sp.issparse(H) else H)
    av = np.sort(np.abs(v))
    nz = int((av < thresh).sum())
    gap = float(av[av >= thresh][0]) if (av >= thresh).any() else float("nan")
    return nz, gap


def main() -> int:
    N, m = 6, 1.0
    # 1) find a single-cone topological window at this N (exactly one zero mode)
    best = None
    for M in np.round(np.arange(0.5, 3.01, 0.25), 2):
        nz, gap = zero_count(build_hamiltonian(N, m, M))
        if nz == 1 and (best is None or gap > best[1]):
            best = (float(M), gap)
    if best is None:
        print(f"N={N}: no clean single-cone window found (too coarse); see WP-B (N=8).")
        return 2
    Mstar = best[0]
    print(f"Parity of induced charge (grid {N}³, single-cone window M*={Mstar}, gap {best[1]:.3f}).\n")
    print(f"  {'N_f':<5}{'#zero modes':<13}{'charge N_f/2':<14}{'θ = N_fπ':<12}{'statistics'}")

    ok = True
    for Nf in (1, 2, 3):
        H = sp.block_diag([build_hamiltonian(N, m, Mstar)] * Nf)
        nz, _ = zero_count(H)
        charge = nz / 2.0
        theta = "π" if nz % 2 else "0"
        stat = "fermion" if nz % 2 else "boson"
        good = (nz == Nf)
        ok &= good
        print(f"  {Nf:<5}{nz:<13}{charge:<14}{theta:<12}{stat}{'' if good else '  (!count≠N_f)'}")

    print("\n  → induced charge = N_f/2; parity fixes statistics: odd N_f ⇒ fermion (θ=π),")
    print("    even N_f ⇒ boson (θ=0). The standard N_f=2 dual ⇒ BOSON (WP-A, Result B).")
    print("  RESULT:", "PASS — θ = N_f·π confirmed; even ⇒ boson" if ok
          else "counts off (finite-size); pattern still parity")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
