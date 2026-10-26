# GT-P008 secondary analyses of published E4 data

*GT-P008, deliverable 3. Written 2026-10-15.*

> **Status.**
> - These are **post hoc, explanatory views** of the exposed E4A and E4B tables (payloads `f050380ac32e` and `169e71c33b38`).
> - They are **not E5 evidence**, not a preregistered test, and not independent confirmation of any E4 finding.
> - No E4 or E5 cell was computed. The only stationary laws evaluated were the uniform NULL product law, an independent recomputation of the CLOSEW Gibbs law used as an extraction check, and synthetic-ε N=4 proof fixtures.
> - Definitions D1–D8 were fixed and pushed (`56ae926`) before any computation.

- **Reproduce:** `constraint-lab/.venv/bin/python -m rs_constraint_lab.gtsort write`, which regenerates `gt-p008-secondary-analyses.json`. `tests/test_gtsort.py::test_committed_secondary_json_is_reproducible` checks that the committed JSON equals a fresh build.
- **Theory:** `docs/e4-sorting-mechanism-derivation.md`.
- **Uncertainty:** values are exact finite-chain quantities, with stationary residual ≤ 1e-12 and no sampling error. Δ is a log-odds contrast between source orbits L and H of one cell.

## 1. Extraction checks (D1, D2)

Every check passes, so the published tables are read correctly and the stationary balance identity (S1) holds in the published laws.

| Check | Largest deviation |
| --- | --- |
| NULL orbit occupancy = 0.5 (both clocks) | 1.7e-16 |
| PCOMP continuous orbit occupancy = 0.5 | 2.2e-14 |
| CLOSEW orbits against an independent Gibbs law, continuous | 2.7e-15 |
| CLOSEW orbits against an independent Gibbs law, per event | 2.7e-15 |
| PATHF: act = 2·occ (S1 with D ≡ 1) | 2.2e-15 |
| PATHH: act = 2·(1 − occ) (S1 with F ≡ 1) | 1.6e-14 |
| per-event act = continuous act / mean rate | 8.6e-16 |
| census held_floor = F1 floor | 1.4e-15 |
| NULL witness means = E_0[w] (S4 closed form) | 2.7e-15 |
| published analytic_floor = F1 (mismatches) | 0 |

Selected GT-F60 values re-extracted, continuous clock:
- P3 N=5 PATHF middle / ends: 0.332 / 0.177;
- star N=6 PATHF centre / leaves: 0.363 / 0.093;
- P4 N=6 PATHH inner / ends: 0.159 / 0.128.

All agree with the GT-P007 record.

## 2. Orbit contrasts: floor term, residue and first order (D4, D6)

- **Floor term** = Δf·ln 2, the exact part of Δ under S2.
- **Floor share** = floor term / Δ (shown only when |Δ| > 0.05 and the two have the same sign).
- **First order** = ln 2·(κ_L − κ_H) (S4 and S6), evaluated at the W4 strength. It is a weak-coupling extrapolation, not a theorem at that strength.
- **Conventions.** L is the lower-floor orbit. In P4, where floors are equal, L is the inner orbit. Δd = held degree of L − held degree of H.

| Cell | Orbits L − H | Δf | Δd | Δ log odds, continuous | Floor term | Residue | Floor share | First order, continuous | Δ log odds, per event | First order, per event |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P3 N=5 PATHF | 1 − 0+2 | 1 | 1 | +0.840 | 0.693 | +0.147 | 0.83 | +0.520 | +0.586 | +0.303 |
| P3 N=5 PATHH | 1 − 0+2 | 1 | 1 | +0.911 | 0.693 | +0.218 | 0.76 | +0.520 | +0.784 | +0.607 |
| P3 N=5 CSPH | 1 − 0+2 | 1 | 1 | +0.690 | 0.693 | -0.003 | 1.00 | +0.866 | +0.718 | +0.910 |
| P3 N=5 PCOMP | 1 − 0+2 | 1 | 1 | -0.000 | 0.000 | -0.000 | — | +0.000 | +0.178 | +0.303 |
| P3 N=5 CLOSEW | 1 − 0+2 | 1 | 1 | +0.089 | 0.000 | +0.089 | — | +0.173 | +0.057 | +0.152 |
| P3 N=6 PATHF | 1 − 0+2 | 1 | 1 | +0.859 | 0.693 | +0.166 | 0.81 | +0.347 | +0.672 | +0.213 |
| P3 N=6 PATHH | 1 − 0+2 | 1 | 1 | +0.972 | 0.693 | +0.279 | 0.71 | +0.347 | +0.867 | +0.427 |
| P3 N=6 CSPH | 1 − 0+2 | 1 | 1 | +0.865 | 0.693 | +0.172 | 0.80 | +0.693 | +0.927 | +0.746 |
| P3 N=6 PCOMP | 1 − 0+2 | 1 | 1 | -0.000 | 0.000 | -0.000 | — | +0.000 | +0.087 | +0.213 |
| P3 N=6 CLOSEW | 1 − 0+2 | 1 | 1 | +0.069 | 0.000 | +0.069 | — | +0.173 | +0.043 | +0.160 |
| S4 N=6 PATHF | 0 − 1+2+3 | 2 | 2 | +1.719 | 1.386 | +0.333 | 0.81 | +0.693 | +1.318 | +0.404 |
| S4 N=6 PATHH | 0 − 1+2+3 | 2 | 2 | +1.862 | 1.386 | +0.475 | 0.74 | +0.693 | +1.586 | +0.866 |
| S4 N=6 CSPH | 0 − 1+2+3 | 2 | 2 | +1.788 | 1.386 | +0.402 | 0.78 | +1.386 | +1.788 | +1.502 |
| S4 N=6 PCOMP | 0 − 1+2+3 | 2 | 2 | -0.000 | 0.000 | -0.000 | — | +0.000 | +0.180 | +0.462 |
| S4 N=6 CLOSEW | 0 − 1+2+3 | 2 | 2 | +0.126 | 0.000 | +0.126 | — | +0.347 | +0.075 | +0.318 |
| P4 N=6 PATHF | 1+2 − 0+3 | 0 | 1 | +0.067 | 0.000 | +0.067 | — | +0.173 | -0.053 | +0.058 |
| P4 N=6 PATHH | 1+2 − 0+3 | 0 | 1 | +0.255 | 0.000 | +0.255 | — | +0.173 | +0.259 | +0.260 |
| P4 N=6 CSPH | 1+2 − 0+3 | 0 | 1 | +0.558 | 0.000 | +0.558 | — | +0.520 | +0.573 | +0.578 |
| P4 N=6 PCOMP | 1+2 − 0+3 | 0 | 1 | -0.000 | 0.000 | -0.000 | — | +0.000 | +0.081 | +0.202 |
| P4 N=6 CLOSEW | 1+2 − 0+3 | 0 | 1 | +0.066 | 0.000 | +0.066 | — | +0.173 | +0.039 | +0.159 |

**Reading.**
- The floor term is 71–100% of the continuous-clock Δ for the σ > 0 families in P3 and the star. The residue is positive in 8 of 9, with P3 N=5 CSPH at −0.003.
- The first-order index has the right continuous-clock sign in 16/16 nonzero contrasts and the right per-event sign in 19/20. The miss is P4 PATHF per event: observed −0.053, first order +0.058.
- PCOMP: continuous Δ = 0 exactly (S2b), but per-event Δ = +0.08 to +0.18. **Sorting in the per-event clock only.**
- CLOSEW: Δf = 0, yet Δ = +0.07 to +0.13, from held degree through closure witnesses. The first-order value over-predicts it (S4b).

## 3. Kinetic routes (D3, D5)

Ratios L/H of:
- the conditional formation-rate mean F̄;
- the conditional dissolution-rate mean D̄;
- the mean present sojourn τ+ and the mean absent sojourn τ−.

| Cell | F̄ L/H | D̄ L/H | τ+ L/H | τ− L/H |
| --- | --- | --- | --- | --- |
| P3 N=5 PATHF | 2.316 | 1.000 | 1.000 | 0.432 |
| P3 N=5 PATHH | 1.000 | 0.402 | 2.487 | 1.000 |
| P3 N=5 CSPH | 0.966 | 0.485 | 2.064 | 1.035 |
| P3 N=5 PCOMP | 0.857 | 0.857 | 1.167 | 1.167 |
| P3 N=5 CLOSEW | 1.094 | 1.000 | 1.000 | 0.914 |
| P3 N=6 PATHF | 2.361 | 1.000 | 1.000 | 0.424 |
| P3 N=6 PATHH | 1.000 | 0.378 | 2.642 | 1.000 |
| P3 N=6 CSPH | 0.951 | 0.401 | 2.497 | 1.051 |
| P3 N=6 PCOMP | 0.942 | 0.942 | 1.062 | 1.062 |
| P3 N=6 CLOSEW | 1.071 | 1.000 | 1.000 | 0.934 |
| S4 N=6 PATHF | 5.579 | 1.000 | 1.000 | 0.179 |
| S4 N=6 PATHH | 1.000 | 0.155 | 6.434 | 1.000 |
| S4 N=6 CSPH | 0.843 | 0.141 | 7.088 | 1.186 |
| S4 N=6 PCOMP | 0.887 | 0.887 | 1.127 | 1.127 |
| S4 N=6 CLOSEW | 1.134 | 1.000 | 1.000 | 0.882 |
| P4 N=6 PATHF | 1.070 | 1.000 | 1.000 | 0.935 |
| P4 N=6 PATHH | 1.000 | 0.775 | 1.290 | 1.000 |
| P4 N=6 CSPH | 1.084 | 0.621 | 1.611 | 0.922 |
| P4 N=6 PCOMP | 0.950 | 0.950 | 1.052 | 1.052 |
| P4 N=6 CLOSEW | 1.068 | 1.000 | 1.000 | 0.936 |

**Reading.**
- **PATHF** sorts only through formation (τ+ ratio 1.000 exactly, because D ≡ 1).
- **PATHH** sorts only through lifetime (τ− ratio 1.000 exactly, because F ≡ 1).
- **CSPH** sorts mostly through lifetime.
- **PCOMP** has F̄ and D̄ ratios equal, hence equal odds: low-floor slots turn over *more slowly* in both directions.

## 4. P3 chord strata (D7; association only)

| Cell | Clock | Chord occupancy | Absent: middle / ends (Δ) | Present: middle / ends (Δ) |
| --- | --- | --- | --- | --- |
| P3 N=5 PATHF | continuous | 0.289 | 0.411 / 0.179 (+1.161) | 0.138 / 0.170 (-0.249) |
| P3 N=5 PATHF | jump | 0.254 | 0.333 / 0.184 (+0.796) | 0.138 / 0.170 (-0.248) |
| P3 N=5 PATHH | continuous | 0.289 | 0.416 / 0.175 (+1.210) | 0.143 / 0.156 (-0.105) |
| P3 N=5 PATHH | jump | 0.339 | 0.457 / 0.228 (+1.050) | 0.240 / 0.209 (+0.179) |
| P3 N=5 CSPH | continuous | 0.533 | 0.539 / 0.233 (+1.347) | 0.213 / 0.216 (-0.017) |
| P3 N=5 CSPH | jump | 0.559 | 0.648 / 0.297 (+1.471) | 0.365 / 0.336 (+0.128) |
| P3 N=5 PCOMP | continuous | 0.500 | 0.500 / 0.500 (-0.000) | 0.500 / 0.500 (-0.000) |
| P3 N=5 PCOMP | jump | 0.797 | 0.840 / 0.731 (+0.657) | 0.789 / 0.779 (+0.059) |
| P3 N=5 CLOSEW | continuous | 0.822 | 0.786 / 0.708 (+0.420) | 0.817 / 0.817 (+0.000) |
| P3 N=5 CLOSEW | jump | 0.793 | 0.781 / 0.734 (+0.253) | 0.790 / 0.790 (+0.000) |
| P3 N=6 PATHF | continuous | 0.234 | 0.342 / 0.147 (+1.101) | 0.112 / 0.143 (-0.279) |
| P3 N=6 PATHF | jump | 0.215 | 0.285 / 0.146 (+0.849) | 0.105 / 0.133 (-0.267) |
| P3 N=6 PATHH | continuous | 0.230 | 0.357 / 0.143 (+1.202) | 0.120 / 0.134 (-0.127) |
| P3 N=6 PATHH | jump | 0.264 | 0.390 / 0.178 (+1.085) | 0.188 / 0.171 (+0.120) |
| P3 N=6 CSPH | continuous | 0.448 | 0.457 / 0.168 (+1.426) | 0.171 / 0.174 (-0.026) |
| P3 N=6 CSPH | jump | 0.458 | 0.550 / 0.205 (+1.556) | 0.270 / 0.247 (+0.124) |
| P3 N=6 PCOMP | continuous | 0.500 | 0.500 / 0.500 (-0.000) | 0.500 / 0.500 (+0.000) |
| P3 N=6 PCOMP | jump | 0.866 | 0.888 / 0.828 (+0.502) | 0.864 / 0.861 (+0.022) |
| P3 N=6 CLOSEW | continuous | 0.907 | 0.887 / 0.822 (+0.535) | 0.906 / 0.906 (+0.000) |
| P3 N=6 CLOSEW | jump | 0.880 | 0.876 / 0.838 (+0.317) | 0.878 / 0.878 (+0.000) |

**Reading.**
- With the chord absent, the middle has no internal witness and the ends have one; the middle is strongly favoured (Δ +1.10 to +1.43 continuous, +0.80 to +1.56 per event).
- With the chord present, both have exactly two internal witnesses. The middle's continuous-clock advantage disappears or reverses (Δ −0.28 to −0.02).
- Per event, PATHH and CSPH keep a small positive Δ: the sign depends on the clock.
- Chord occupancy is suppressed under PATHF and PATHH (0.23–0.29) but **not under CSPH (0.45–0.53)**, where closure rewards the chord. This clarifies the GT-P007 phrasing "the chord is rare" (audit, qualification Q-4).
- These are strata of one stationary law. They do not show what toggling the chord would do (Q-2).
- The star and P4 tables condition on only one of their chords, so they are not shown.

## 5. Gathering margins and composition (D6, D8)

- **Collation.** The published margins and overlap diagnostics are shown as published; no new standardisation was computed.
- **First-order slope.** This is S7, multiplied by ln 2 for scale.

| Cell | Raw, continuous / per event | Standardised, continuous / per event | Free density | NULL weight low-k / rare-k | First-order slope × ln 2 | Sign agreement (raw, continuous) |
| --- | --- | --- | --- | --- | --- | --- |
| K2 N=5 PATHF | +0.048 / +0.026 | +0.001 / -0.004 | 0.292 | 0.018 / 0.002 | +0.039 | yes |
| K2 N=5 PATHH | +0.073 / +0.068 | +0.005 / +0.021 | 0.283 | 0.088 / 0.002 | +0.039 | yes |
| K2 N=5 CSPH | +0.115 / +0.099 | +0.055 / +0.068 | 0.337 | 0.020 / 0.000 | +0.077 | yes |
| K2 N=5 PCOMP | -0.000 / +0.007 | -0.000 / +0.026 | 0.500 | 0.000 / 0.000 | +0.000 | slope 0 |
| K2 N=5 CLOSEW | +0.006 / +0.004 | +0.020 / +0.016 | 0.782 | 0.000 / 0.000 | +0.019 | yes |
| K2 N=6 PATHF | +0.026 / +0.008 | -0.023 / -0.025 | 0.247 | 0.122 / 0.090 | +0.021 | yes |
| K2 N=6 PATHH | +0.065 / +0.064 | -0.030 / -0.016 | 0.235 | 0.122 / 0.090 | +0.021 | yes |
| K2 N=6 CSPH | +0.124 / +0.124 | +0.009 / +0.031 | 0.263 | 0.183 / 0.029 | +0.064 | yes |
| K2 N=6 PCOMP | -0.000 / +0.003 | -0.000 / +0.025 | 0.500 | 0.000 / 0.000 | +0.000 | slope 0 |
| K2 N=6 CLOSEW | +0.002 / +0.002 | +0.024 / +0.021 | 0.892 | 0.000 / 0.000 | +0.021 | yes |
| P3 N=5 PATHF | -0.026 / -0.033 | -0.021 / -0.022 | 0.236 | 0.031 / 0.004 | +0.000 | slope 0 |
| P3 N=5 PATHH | -0.007 / -0.001 | -0.015 / -0.007 | 0.227 | 0.031 / 0.004 | +0.000 | slope 0 |
| P3 N=5 CSPH | -0.043 / +0.002 | -0.008 / +0.002 | 0.288 | 0.004 / 0.000 | -0.005 | yes |
| P3 N=5 PCOMP | +0.000 / +0.002 | +0.000 / +0.007 | 0.500 | 0.000 / 0.000 | +0.000 | slope 0 |
| P3 N=5 CLOSEW | +0.000 / +0.000 | -0.002 / +0.000 | 0.802 | 0.000 / 0.000 | -0.003 | **no** |
| P3 N=6 PATHF | -0.039 / -0.059 | -0.050 / -0.051 | 0.205 | 0.244 / 0.046 | +0.003 | **no** |
| P3 N=6 PATHH | +0.008 / +0.015 | -0.060 / -0.045 | 0.193 | 0.157 / 0.133 | +0.003 | yes |
| P3 N=6 CSPH | +0.004 / +0.041 | -0.037 / -0.011 | 0.222 | 0.244 / 0.046 | +0.025 | yes |
| P3 N=6 PCOMP | -0.000 / +0.002 | +0.000 / +0.017 | 0.500 | 0.000 / 0.000 | +0.000 | slope 0 |
| P3 N=6 CLOSEW | +0.001 / +0.001 | +0.013 / +0.012 | 0.898 | 0.000 / 0.000 | +0.011 | yes |
| K3 N=5 PATHF | -0.107 / -0.131 | -0.067 / -0.070 | 0.167 | 0.055 / 0.008 | +0.021 | **no** |
| K3 N=5 PATHH | -0.044 / -0.008 | -0.039 / -0.022 | 0.155 | 0.055 / 0.008 | +0.021 | **no** |
| K3 N=5 CSPH | +0.046 / +0.073 | +0.023 / +0.038 | 0.201 | 0.008 / 0.000 | +0.064 | yes |
| K3 N=5 PCOMP | -0.000 / +0.009 | -0.000 / +0.024 | 0.500 | 0.000 / 0.000 | +0.000 | slope 0 |
| K3 N=5 CLOSEW | +0.005 / +0.003 | +0.022 / +0.015 | 0.813 | 0.000 / 0.000 | +0.021 | yes |
| K3 N=6 PATHF | -0.206 / -0.237 | -0.120 / -0.121 | 0.165 | 0.314 / 0.073 | +0.000 | slope 0 |
| K3 N=6 PATHH | -0.112 / -0.061 | -0.129 / -0.104 | 0.147 | 0.314 / 0.073 | +0.000 | slope 0 |
| K3 N=6 CSPH | +0.009 / +0.065 | -0.073 / -0.034 | 0.167 | 0.175 / 0.019 | +0.065 | yes |
| K3 N=6 PCOMP | +0.000 / +0.004 | -0.000 / +0.032 | 0.500 | 0.000 / 0.000 | +0.000 | slope 0 |
| K3 N=6 CLOSEW | +0.003 / +0.002 | +0.034 / +0.028 | 0.903 | 0.000 / 0.000 | +0.032 | yes |
| S4 N=6 PATHF | +0.059 / +0.032 | -0.004 / -0.004 | 0.147 | 0.314 / 0.073 | +0.000 | slope 0 |
| S4 N=6 PATHH | +0.085 / +0.066 | -0.031 / -0.021 | 0.139 | 0.193 / 0.194 | +0.000 | slope 0 |
| S4 N=6 CSPH | -0.060 / -0.020 | -0.056 / -0.037 | 0.176 | 0.175 / 0.019 | -0.029 | yes |
| S4 N=6 PCOMP | +0.000 / +0.000 | +0.000 / +0.004 | 0.500 | 0.000 / 0.000 | +0.000 | slope 0 |
| S4 N=6 CLOSEW | -0.000 / -0.000 | -0.017 / -0.012 | 0.904 | 0.000 / 0.000 | -0.014 | yes |
| P4 N=6 PATHF | -0.088 / -0.078 | -0.019 / -0.018 | 0.173 | 0.314 / 0.073 | -0.019 | yes |
| P4 N=6 PATHH | -0.077 / -0.060 | -0.013 / -0.015 | 0.163 | 0.314 / 0.073 | -0.019 | yes |
| P4 N=6 CSPH | -0.251 / -0.192 | -0.069 / -0.064 | 0.195 | 0.175 / 0.019 | -0.058 | yes |
| P4 N=6 PCOMP | +0.000 / -0.001 | +0.000 / -0.009 | 0.500 | 0.000 / 0.000 | +0.000 | slope 0 |
| P4 N=6 CLOSEW | -0.001 / -0.001 | -0.023 / -0.017 | 0.905 | 0.000 / 0.000 | -0.019 | yes |

**Reading.**
- **Composition.** Wherever raw margins are positive for σ > 0 families (K2, star PATHF/PATHH, P3 N=6 PATHH/CSPH), the standardised margins are near zero or negative. The only exception is CSPH under K2 (+0.055 / +0.068 at N=5; +0.009 / +0.031 at N=6).
- **Overlap.** At N=6, 12–31% of the NULL weight lies on low-mass free-edge counts, and up to 19% on rare ones. Standardised values there rest partly on reweighting rarely visited strata. **No standardised value in this table supports density-independent gathering.**
- **First-order slopes.** They have the right sign in 22/26 nonzero cases.
  - The misses are K3 N=5 PATHF (slope > 0, raw −0.107), K3 N=5 PATHH (−0.044), P3 N=6 PATHF (−0.039) and P3 N=5 CLOSEW (raw +0.0004).
  - The first three imply a sign change of the margin between weak and W4 strength (S7b).
  - Exact zero slopes (P3 N=5, K3 N=6 and star N=6 under PATHF/PATHH) leave the sign to second order.

## 6. First-order reversals (pure algebra; S4c)

These are the connected held graphs on ≤ 5 vertices, at N = 6, in which PATHF/PATHH's first-order index favours the **higher-floor** vertex. There are 7 strict reversals among 48 floor-order disagreements; the rest are ties.

| Held graph (N=6) | Lower-floor vertex (floor, degree) | Higher-floor vertex (floor, degree) | κ_lower − κ_higher |
| --- | --- | --- | --- |
| 01 02 03 12 14 | 3 (2, 1) | 0 (3, 3) | -0.25 |
| 01 02 03 12 14 | 4 (2, 1) | 0 (3, 3) | -0.25 |
| 01 02 03 12 14 | 3 (2, 1) | 1 (3, 3) | -0.25 |
| 01 02 03 12 14 | 4 (2, 1) | 1 (3, 3) | -0.25 |
| 01 02 03 04 12 13 | 4 (3, 1) | 0 (4, 4) | -0.50 |
| 01 02 03 04 12 13 24 | 3 (5, 2) | 0 (6, 4) | -0.25 |
| 01 02 03 04 12 13 24 | 4 (5, 2) | 0 (6, 4) | -0.25 |

At W4 strength, none of these has been computed. Testing them would be a new scientific enumeration, proposed in `docs/gt-p008-next-round-options.md` (candidate B).

## 7. Analyses considered and not done

| Analysis | Why not |
| --- | --- |
| Per-density-stratum orbit occupancy | Not in the published tables; would need new cell computations |
| Conditional witness laws (to test the feedback mechanism directly) | Not in the tables; only unconditional means were published |
| Star and P4 strata over all chords | Only the first chord was tabulated |
| Re-standardising margins with a different reference density | Would be a new estimator chosen after seeing the data; nothing would justify it |
| First-order theory of per-event margins | Possible from S6, but not needed for any question here |
