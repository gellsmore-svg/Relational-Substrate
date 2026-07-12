"""Instantiation phase — test 3: the emergent magnetic sector (Mermin–Ho).

The EM tier (D9 / the crux) rests on one identification: the emergent magnetic
field is the skyrmion density,  b_i = (1/8π) ε_ijk n·(∂_j n × ∂_k n),  whose flux
through a closed surface equals the enclosed topological charge (π₂). Two
consequences are tested here, both parameter-free:

  (a) a **hedgehog** (singular, degree q) is an **emergent magnetic monopole**:
      the box flux ∮ b·dS = q  — "π₂ density integrates to the charge";
  (b) a **smooth Hopfion** (no singularity) carries **no net monopole**:
      ∮ b·dS ≈ 0  — the crux's "no magnetic monopole for smooth textures".

The field is not periodic (n = r̂ points radially), so derivatives use central
finite differences and the flux is summed over the six faces of the box.
"""

from __future__ import annotations

import numpy as np

from hopf_invariant import build_hopfion


def build_hedgehog(N: int, L: float, q: int):
    """Degree-q hedgehog: n = (sinθ cos qφ, sinθ sin qφ, cosθ). q=1 is n = r̂."""
    xs = (np.arange(N) - (N - 1) / 2) * (L / N)  # offset so no grid point sits at r=0
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    r = np.sqrt(X**2 + Y**2 + Z**2)
    cth = Z / r
    sth = np.sqrt(X**2 + Y**2) / r
    phi = np.arctan2(Y, X)
    n = np.stack([sth * np.cos(q * phi), sth * np.sin(q * phi), cth], axis=0)
    n /= np.sqrt((n**2).sum(axis=0))
    return n, L / N


def emergent_b(n: np.ndarray, dx: float) -> np.ndarray:
    """b_i = (1/4π) n·(∂_j n × ∂_k n) (cyclic) — the emergent magnetic field."""
    dn = [[np.gradient(n[a], dx, axis=j, edge_order=2) for j in range(3)] for a in range(3)]

    def djn(j: int) -> np.ndarray:
        return np.stack([dn[0][j], dn[1][j], dn[2][j]], axis=0)

    def cross(u: np.ndarray, v: np.ndarray) -> np.ndarray:
        return np.stack([u[1] * v[2] - u[2] * v[1],
                         u[2] * v[0] - u[0] * v[2],
                         u[0] * v[1] - u[1] * v[0]], axis=0)

    def ndot(u: np.ndarray) -> np.ndarray:
        return (n * u).sum(axis=0)

    bx = ndot(cross(djn(1), djn(2)))
    by = ndot(cross(djn(2), djn(0)))
    bz = ndot(cross(djn(0), djn(1)))
    return np.stack([bx, by, bz], axis=0) / (4 * np.pi)


def box_flux(n: np.ndarray, dx: float) -> float:
    """∮ b·dS over the six faces of the cubic box (outward normals)."""
    b = emergent_b(n, dx)
    da = dx * dx
    flux = (
        b[0][-1, :, :].sum() - b[0][0, :, :].sum()
        + b[1][:, -1, :].sum() - b[1][:, 0, :].sum()
        + b[2][:, :, -1].sum() - b[2][:, :, 0].sum()
    ) * da
    return float(flux)


def main() -> int:
    N = 64
    print(f"Emergent magnetic sector (grid {N}³), parameter-free.\n")
    print("(a) hedgehog (singular) = emergent monopole: flux ∮b·dS should equal its charge q")
    ok = True
    for q in (1, 2, 3):
        n, dx = build_hedgehog(N, 2.0, q)
        f = box_flux(n, dx)
        good = abs(f - q) < 0.1
        ok &= good
        print(f"    degree q={q}   flux = {f:+.4f}   (expect {q})   {'PASS' if good else 'FAIL'}")

    print("\n(b) smooth Hopfion (no singularity) = no net monopole: flux should be ≈ 0")
    n, dx = build_hopfion(N, 16.0, 1.0)
    f = box_flux(n, dx)
    good = abs(f) < 0.05
    ok &= good
    print(f"    smooth H=1 texture   flux = {f:+.5f}   (expect 0)   {'PASS' if good else 'FAIL'}")

    print("\n  RESULT:", "PASS — π₂ density = emergent magnetic flux; monopole ⇔ singular"
          if ok else "FAIL — see values")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
