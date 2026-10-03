"""Instantiation phase — test 1: compute the Hopf invariant of an explicit vorton.

The conceptual phase asserted that a vorton's identity is an integer Hopf/linking
number (π₃). This is the first touch of computation and the sharpest could-fail
test of that claim: build an *explicit* charge-1 Hopfion director field and
compute its Hopf number numerically — it must come out to a clean integer, and,
because a topological invariant cannot depend on the configuration's size, it
must be **the same at two different scales** (parameter-free; no calibration).

Construction (all standard, no free/tuned parameters):
  R³ --(inverse stereographic)--> S³ --(Hopf map)--> S²
so n: R³ → S² is the elementary Hopfion, n → (0,0,-1) at infinity, Hopf charge 1.

Invariant (Whitehead):  F_i = (1/8π) ε_ijk n·(∂_j n × ∂_k n),  ∇×A = F,
                        H = ∫ A·F d³x   (an integer for the Hopf class).
The ∇×A = F solve is done spectrally: A(k) = i (k×F(k))/k².
"""

from __future__ import annotations

import numpy as np


def build_hopfion(N: int, L: float, scale: float) -> tuple[np.ndarray, float]:
    """Elementary (charge-1) Hopfion on an N³ periodic box of side L, size `scale`."""
    xs = (np.arange(N) - N // 2) * (L / N)
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    X, Y, Z = X / scale, Y / scale, Z / scale
    r2 = X**2 + Y**2 + Z**2
    denom = r2 + 1.0
    # inverse stereographic projection R³ → S³ ⊂ R⁴
    X1, X2, X3, X4 = 2 * X / denom, 2 * Y / denom, 2 * Z / denom, (r2 - 1.0) / denom
    # Hopf map S³ → S²: n = Z† σ Z, with Z = (X1+iX2, X3+iX4) (already unit on S³)
    Z1, Z2 = X1 + 1j * X2, X3 + 1j * X4
    nx = 2 * np.real(np.conj(Z1) * Z2)
    ny = 2 * np.imag(np.conj(Z1) * Z2)
    nz = np.abs(Z1) ** 2 - np.abs(Z2) ** 2
    n = np.stack([nx, ny, nz], axis=0)
    n /= np.sqrt((n**2).sum(axis=0))  # enforce |n| = 1
    return n, L / N


def hopf_invariant(n: np.ndarray, dx: float) -> float:
    """Whitehead integral H = ∫ A·F, with F the pullback flux and ∇×A = F."""
    N = n.shape[1]
    k = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij")
    Kv = [KX, KY, KZ]
    K2 = KX**2 + KY**2 + KZ**2
    K2[0, 0, 0] = 1.0  # k=0 handled explicitly below

    n_hat = [np.fft.fftn(n[a]) for a in range(3)]

    def d(a: int, j: int) -> np.ndarray:  # ∂_j n^a via spectral derivative
        return np.real(np.fft.ifftn(1j * Kv[j] * n_hat[a]))

    dn = [[d(a, j) for j in range(3)] for a in range(3)]

    def djn(j: int) -> np.ndarray:  # the vector ∂_j n
        return np.stack([dn[0][j], dn[1][j], dn[2][j]], axis=0)

    def cross(u: np.ndarray, v: np.ndarray) -> np.ndarray:
        return np.stack([u[1] * v[2] - u[2] * v[1],
                         u[2] * v[0] - u[0] * v[2],
                         u[0] * v[1] - u[1] * v[0]], axis=0)

    def ndot(u: np.ndarray) -> np.ndarray:
        return (n * u).sum(axis=0)

    # F_i = (1/8π) ε_ijk n·(∂_j n × ∂_k n); the ε-sum gives the factor 2
    F = np.stack([
        2 * ndot(cross(djn(1), djn(2))),
        2 * ndot(cross(djn(2), djn(0))),
        2 * ndot(cross(djn(0), djn(1))),
    ], axis=0) / (8 * np.pi)

    # solve ∇×A = F spectrally: A(k) = i (k × F(k)) / k²  (Coulomb gauge)
    F_hat = [np.fft.fftn(F[i]) for i in range(3)]
    kxF = [Kv[1] * F_hat[2] - Kv[2] * F_hat[1],
           Kv[2] * F_hat[0] - Kv[0] * F_hat[2],
           Kv[0] * F_hat[1] - Kv[1] * F_hat[0]]
    A = []
    for i in range(3):
        A_hat = 1j * kxF[i] / K2
        A_hat[0, 0, 0] = 0.0
        A.append(np.real(np.fft.ifftn(A_hat)))
    A = np.stack(A, axis=0)

    return float((A * F).sum() * dx**3)


def measure(N: int, L: float, scale: float) -> float:
    n, dx = build_hopfion(N, L, scale)
    return hopf_invariant(n, dx)


def main() -> int:
    print("Elementary Hopfion (inverse-stereographic ∘ Hopf map).")
    print("Claim under test: its Hopf number is the integer 1, parameter-free.\n")

    # (1) The integer is real: H converges to 1 as the discretisation improves
    #     (fixed physical structure, well contained in box L=16; finer grid).
    print("Convergence to the integer (scale=1.0, box L=16, refining the grid):")
    best = None
    for N in (64, 96, 128):
        H = measure(N, 16.0, 1.0)
        best = H
        print(f"  grid {N:>3}³   dx={16.0/N:.3f}    H = {H:+.5f}   (→ {round(H)})")

    # (2) Parameter-free: at the finest grid, vary the Hopfion's physical size
    #     (all well contained + resolved). A topological invariant must not move.
    print("\nScale-independence (grid 128³, box L=16, varying structure size):")
    Hs = []
    for scale in (0.8, 1.0, 1.25):
        H = measure(128, 16.0, scale)
        Hs.append(H)
        print(f"  size={scale:<5}  H = {H:+.5f}")
    spread = max(Hs) - min(Hs)

    print(f"\n  finest-grid H = {best:+.5f}  (nearest integer {round(best)})")
    print(f"  scale-spread  = {spread:.5f}")
    ok_int = abs(best - 1.0) < 0.02
    ok_scale = spread < 0.02
    print(f"  integer 1?              {'PASS' if ok_int else 'FAIL'}")
    print(f"  parameter-free (scale)? {'PASS' if ok_scale else 'FAIL'}")
    return 0 if (ok_int and ok_scale) else 1


if __name__ == "__main__":
    raise SystemExit(main())
