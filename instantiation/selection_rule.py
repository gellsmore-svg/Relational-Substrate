"""Instantiation phase — test 2: the π₂–π₃ selection rule  H = p·q.

The conceptual phase claimed the vorton's Hopf identity is a quadratic form on the
constituent windings — for a single twisted tube, `H = n·m` (skyrmion winding ×
internal twist). Here that is put to an explicit, parameter-free numerical test.

Construction: the **type-(p,q) Hopfion**. From the same inverse-stereographic map
R³ → S³ (two complex coordinates Z₁, Z₂), take the meromorphic map to the Riemann
sphere `w = Z₁ᵖ / Z₂q` and read off the director by inverse stereographic
projection. Its two winding numbers (p, q) play the roles of the two circulations
(skyrmion charge and twist); the standard result is **Hopf charge H = p·q**.

The invariant is computed by the same Whitehead routine verified in test 1
(`hopf_invariant`), so this test isolates the *selection-rule arithmetic*.
"""

from __future__ import annotations

import numpy as np

from hopf_invariant import hopf_invariant


def build_pq_hopfion(N: int, L: float, p: int, q: int, scale: float = 1.0):
    """Type-(p,q) Hopfion: w = Z₁ᵖ / Z₂q, director by inverse stereographic proj."""
    xs = (np.arange(N) - N // 2) * (L / N)
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    X, Y, Z = X / scale, Y / scale, Z / scale
    r2 = X**2 + Y**2 + Z**2
    den = r2 + 1.0
    X1, X2, X3, X4 = 2 * X / den, 2 * Y / den, 2 * Z / den, (r2 - 1.0) / den
    Z1, Z2 = X1 + 1j * X2, X3 + 1j * X4
    # w = Z1^p / Z2^q, taken as u/v with |u|,|v| <= 1 (no overflow); n = inv-stereo(w).
    # Written to avoid dividing by zero: |u|²+|v|² > 0 everywhere on S³.
    u, v = Z1**p, Z2**q
    d = np.abs(u) ** 2 + np.abs(v) ** 2
    uvb = u * np.conj(v)
    nx = 2 * np.real(uvb) / d
    ny = 2 * np.imag(uvb) / d
    nz = (np.abs(v) ** 2 - np.abs(u) ** 2) / d
    n = np.stack([nx, ny, nz], axis=0)
    n /= np.sqrt((n**2).sum(axis=0))
    return n, L / N


def main() -> int:
    N, L = 128, 16.0
    print(f"Selection rule  H = p·q  (grid {N}³, box L={L}), parameter-free.\n")
    print(f"  {'(p,q)':<8}{'p·q':<6}{'computed H':<14}{'ok?'}")
    cases = [(1, 1), (2, 1), (1, 2), (2, 2), (3, 1), (2, 3)]
    all_ok = True
    for p, q in cases:
        n, dx = build_pq_hopfion(N, L, p, q)
        H = hopf_invariant(n, dx)
        expected = p * q
        ok = abs(abs(H) - expected) < 0.25  # rounds to the correct integer
        all_ok &= ok
        print(f"  {str((p, q)):<8}{expected:<6}{H:+.4f}       {'PASS' if ok else 'FAIL'}")
    print("\n  RESULT:", "PASS — H = p·q holds parameter-free" if all_ok else "FAIL — see values")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
