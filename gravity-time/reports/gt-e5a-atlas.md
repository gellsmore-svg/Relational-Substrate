# GT-E5A FREE persistence atlas

Generated from `gravity-time/reports/round-e5a-tables.json` (payload `6e978571d83e…`), frozen plan `1dc43c6`. Every item, predicate, comparator and diagnostic is listed. **N0** = NULL at the same N; **ND** = the density-matched comparator (CT edge-count profile and CT mean rate only; not jump-density matched). Lifetimes: CT in model time units, jump in jumps. ρ = motif lifetime / edge present-lifetime in the same law and clock. Ω = eligible within-episode toggles per episode (intact motifs: 0 by theorem). Prevalences are re-expressions of published E0B laws.

Frozen identities and checks: **32/34 hold**.

Not holding: Z-FREE-N6-CSPH-strong_favour+weak_favour (['target: propagator not stochastic']); Z-FREE-N6-PATHH-weak_favour (['target: comparison degree not stationary', 'target: propagator not stochastic', 'target: propagator not stationary']).

## Item records

| Item | Role | Status | Wall s | Peak MB | Problems |
| --- | --- | --- | --- | --- | --- |
| FREE-N5-CLOSEW-weak_favour | control_reversible_closure | complete | 0.2 | 48 | none |
| FREE-N5-CSPH-strong_favour+weak_favour | open_scientific | complete | 0.2 | 48 | none |
| FREE-N5-NULL-none | null_control_N0 | complete | 0.2 | 47 | none |
| FREE-N5-PATHF-weak_suppress | open_scientific | complete | 0.4 | 48 | none |
| FREE-N5-PATHH-weak_favour | open_scientific | complete | 0.2 | 48 | none |
| FREE-N5-PCOMP-weak_favour+weak_favour | control_equal_ratio | complete | 0.6 | 48 | none |
| FREE-N6-CLOSEW-weak_favour | control_reversible_closure | complete | 102.5 | 668 | none |
| FREE-N6-CSPH-strong_favour+weak_favour | open_scientific | complete | 72.0 | 668 | target: propagator not stochastic |
| FREE-N6-NULL-none | null_control_N0 | complete | 38.7 | 669 | none |
| FREE-N6-PATHF-weak_suppress | open_scientific | complete | 78.5 | 668 | none |
| FREE-N6-PATHH-weak_favour | open_scientific | complete | 109.8 | 668 | target: comparison degree not stationary; target: propagator not stochastic; target: propagator not stationary |
| FREE-N6-PCOMP-weak_favour+weak_favour | control_equal_ratio | complete | 50.2 | 668 | none |

## ND construction

| Item | scale c | rare bins (p_k < 1e-12) | log φ range | min unscaled rate | CT density L1 | jump density L1 target vs ND | mean jump edges target / ND | iterative cross-check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FREE-N5-CLOSEW-weak_favour | 3.090 | none | 6.9 | 0.125 | 1.76e-15 | 0.450 | 7.53 / 6.58 | resolved (455) |
| FREE-N5-CSPH-strong_favour+weak_favour | 3.720 | none | 15.4 | 0.016 | 1.62e-15 | 0.592 | 4.45 / 3.57 | resolved (160) |
| FREE-N5-NULL-none | 1.000 | none | 3.55e-15 | 1.000 | 3.26e-16 | 2.51e-16 | 5.00 / 5.00 | resolved (1) |
| FREE-N5-PATHF-weak_suppress | 1.000 | {'10': 5.7628985471501864e-15} | 27.2 | 2.44e-04 | 1.73e-15 | 2.03e-15 | 3.14 / 3.14 | resolved (142) |
| FREE-N5-PATHH-weak_favour | 2.095 | {'10': 1.2892858041976536e-15} | 28.7 | 2.44e-04 | 1.86e-15 | 0.415 | 3.58 / 3.04 | resolved (136) |
| FREE-N5-PCOMP-weak_favour+weak_favour | 44.406 | none | 2.06e-13 | 1.000 | 1.97e-15 | 1.287 | 7.74 / 5.00 | resolved (11) |
| FREE-N6-CLOSEW-weak_favour | 7.515 | none | 13.9 | 0.063 | 8.53e-15 | 0.472 | 12.98 / 11.90 | resolved (736) |
| FREE-N6-CSPH-strong_favour+weak_favour | 4.767 | {'12': 1.4144989927805407e-13, '13': 9.537868477232856e-18, '14': 1.000286484461828e-22, '15': 1.017544031231504e-28} | 56.5 | 1.53e-05 | 3.18e-14 | 0.597 | 5.12 / 4.21 | resolved (177) |
| FREE-N6-NULL-none | 1.000 | none | 7.11e-15 | 1.000 | 3.45e-17 | 1.62e-16 | 7.50 / 7.50 | resolved (1) |
| FREE-N6-PATHF-weak_suppress | 1.000 | {'11': 2.6494090091858225e-13, '12': 4.582878247216121e-18, '13': 6.982974648223552e-24, '14': 7.020231350438234e-31, '15': 2.7895893058932186e-39} | 81.2 | 5.96e-08 | 1.50e-14 | 2.25e-14 | 3.97 / 3.97 | resolved (168) |
| FREE-N6-PATHH-weak_favour | 2.734 | {'11': 6.265111613358474e-14, '12': 8.551051318450941e-19, '13': 1.06840599365638e-24, '14': 9.26283050585976e-32, '15': 3.680718146109422e-40} | 83.4 | 5.96e-08 | 3.13e-14 | 0.428 | 4.41 / 3.80 | resolved (160) |
| FREE-N6-PCOMP-weak_favour+weak_favour | 4608.670 | none | 1.41e-12 | 1.000 | 3.18e-14 | 1.740 | 12.85 / 7.50 | resolved (29) |

## Predicates: target, N0, ND

**FREE-N5-CLOSEW-weak_favour**

| Predicate | law | π(A) | ν(A) | L_ct | L_jump | entries/unit t | ρ_ct | ρ_jump | Ω | eligible share | vs N0 | vs ND |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F_2PATH | target | 0.909 | 0.921 | 2.544 | 38.93 | 0.357 | 2.544 | 2.583 | 14.505 | 0.382 | longer_both_clocks|turnover_more | longer_both_clocks|turnover_more |
|  | N0 | 0.687 | 0.688 | 0.917 | 9.17 | 0.750 | 0.917 | 0.917 | 2.667 | 0.327 |  |  |
|  | ND | 0.917 | 0.853 | 1.410 | 19.83 | 0.650 | 1.410 | 1.508 | 6.811 | 0.362 |  |  |
| F_STAR | target | 0.730 | 0.736 | 0.738 | 11.24 | 0.989 | 0.738 | 0.746 | 3.241 | 0.316 | longer_both_clocks|turnover_more | longer_both_clocks|turnover_more |
|  | N0 | 0.312 | 0.312 | 0.417 | 4.17 | 0.750 | 0.417 | 0.417 | 0.667 | 0.211 |  |  |
|  | ND | 0.727 | 0.578 | 0.619 | 7.43 | 1.174 | 0.619 | 0.565 | 1.771 | 0.275 |  |  |
| F_TRI | target | 0.698 | 0.696 | 0.669 | 10.07 | 1.044 | 0.669 | 0.668 | 4.958 | 0.547 | longer_both_clocks|turnover_more | longer_both_clocks|turnover_more |
|  | N0 | 0.289 | 0.289 | 0.407 | 4.07 | 0.711 | 0.407 | 0.407 | 0.923 | 0.301 |  |  |
|  | ND | 0.682 | 0.537 | 0.607 | 7.22 | 1.124 | 0.607 | 0.549 | 2.901 | 0.466 |  |  |
| I_2PATH | target | 0.595 | 0.584 | 0.500 | 7.41 | 1.191 | 0.500 | 0.492 | 0.000 | 0.000 | longer_jump_only|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.250 | 0.250 | 0.500 | 5.00 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 |  |  |
|  | ND | 0.590 | 0.446 | 0.579 | 6.61 | 1.020 | 0.579 | 0.503 | 0.000 | 0.000 |  |  |
| I_STAR | target | 0.483 | 0.462 | 0.333 | 4.82 | 1.449 | 0.333 | 0.320 | 0.000 | 0.000 | longer_jump_only|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 3.33 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.475 | 0.312 | 0.442 | 4.39 | 1.074 | 0.442 | 0.334 | 0.000 | 0.000 |  |  |
| I_TRI | target | 0.489 | 0.465 | 0.333 | 4.79 | 1.467 | 0.333 | 0.318 | 0.000 | 0.000 | longer_jump_only|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 3.33 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.475 | 0.312 | 0.442 | 4.39 | 1.074 | 0.442 | 0.334 | 0.000 | 0.000 |  |  |

**FREE-N5-CSPH-strong_favour+weak_favour**

| Predicate | law | π(A) | ν(A) | L_ct | L_jump | entries/unit t | ρ_ct | ρ_jump | Ω | eligible share | vs N0 | vs ND |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F_2PATH | target | 0.505 | 0.605 | 0.220 | 7.08 | 2.294 | 0.794 | 0.794 | 2.009 | 0.331 | not_longer|turnover_fewer | longer_both_clocks|turnover_more |
|  | N0 | 0.687 | 0.688 | 0.917 | 9.17 | 0.750 | 0.917 | 0.917 | 2.667 | 0.327 |  |  |
|  | ND | 0.482 | 0.453 | 0.185 | 4.67 | 2.602 | 0.668 | 0.654 | 1.054 | 0.287 |  |  |
| F_STAR | target | 0.153 | 0.266 | 0.076 | 3.54 | 2.012 | 0.275 | 0.398 | 0.291 | 0.114 | not_longer|turnover_fewer | longer_jump_only|turnover_more |
|  | N0 | 0.312 | 0.312 | 0.417 | 4.17 | 0.750 | 0.417 | 0.417 | 0.667 | 0.211 |  |  |
|  | ND | 0.121 | 0.110 | 0.098 | 2.39 | 1.230 | 0.355 | 0.335 | 0.229 | 0.165 |  |  |
| F_TRI | target | 0.212 | 0.297 | 0.101 | 3.82 | 2.089 | 0.366 | 0.428 | 0.935 | 0.332 | not_longer|turnover_more | longer_both_clocks|turnover_more |
|  | N0 | 0.289 | 0.289 | 0.407 | 4.07 | 0.711 | 0.407 | 0.407 | 0.923 | 0.301 |  |  |
|  | ND | 0.106 | 0.096 | 0.094 | 2.28 | 1.132 | 0.339 | 0.319 | 0.152 | 0.119 |  |  |
| I_2PATH | target | 0.145 | 0.212 | 0.121 | 4.74 | 1.199 | 0.436 | 0.532 | 0.000 | 0.000 | not_longer|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.250 | 0.250 | 0.500 | 5.00 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 |  |  |
|  | ND | 0.125 | 0.116 | 0.137 | 3.41 | 0.914 | 0.495 | 0.478 | 0.000 | 0.000 |  |  |
| I_STAR | target | 0.053 | 0.100 | 0.073 | 3.71 | 0.722 | 0.264 | 0.417 | 0.000 | 0.000 | longer_jump_only|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 3.33 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.037 | 0.034 | 0.090 | 2.19 | 0.413 | 0.326 | 0.307 | 0.000 | 0.000 |  |  |
| I_TRI | target | 0.076 | 0.120 | 0.071 | 2.98 | 1.076 | 0.256 | 0.335 | 0.000 | 0.000 | not_longer|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 3.33 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.037 | 0.034 | 0.090 | 2.19 | 0.413 | 0.326 | 0.307 | 0.000 | 0.000 |  |  |

**FREE-N5-NULL-none**

| Predicate | law | π(A) | ν(A) | L_ct | L_jump | entries/unit t | ρ_ct | ρ_jump | Ω | eligible share | vs N0 | vs ND |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F_2PATH | target | 0.687 | 0.688 | 0.917 | 9.17 | 0.750 | 0.917 | 0.917 | 2.667 | 0.327 | tie_both_clocks|turnover_tie | tie_both_clocks|turnover_tie |
|  | N0 | 0.687 | 0.688 | 0.917 | 9.17 | 0.750 | 0.917 | 0.917 | 2.667 | 0.327 |  |  |
|  | ND | 0.688 | 0.687 | 0.917 | 9.17 | 0.750 | 0.917 | 0.917 | 2.667 | 0.327 |  |  |
| F_STAR | target | 0.312 | 0.312 | 0.417 | 4.17 | 0.750 | 0.417 | 0.417 | 0.667 | 0.211 | tie_both_clocks|turnover_tie | tie_both_clocks|turnover_tie |
|  | N0 | 0.312 | 0.312 | 0.417 | 4.17 | 0.750 | 0.417 | 0.417 | 0.667 | 0.211 |  |  |
|  | ND | 0.312 | 0.312 | 0.417 | 4.17 | 0.750 | 0.417 | 0.417 | 0.667 | 0.211 |  |  |
| F_TRI | target | 0.289 | 0.289 | 0.407 | 4.07 | 0.711 | 0.407 | 0.407 | 0.923 | 0.301 | tie_both_clocks|turnover_tie | tie_both_clocks|turnover_tie |
|  | N0 | 0.289 | 0.289 | 0.407 | 4.07 | 0.711 | 0.407 | 0.407 | 0.923 | 0.301 |  |  |
|  | ND | 0.289 | 0.289 | 0.407 | 4.07 | 0.711 | 0.407 | 0.407 | 0.923 | 0.301 |  |  |
| I_2PATH | target | 0.250 | 0.250 | 0.500 | 5.00 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 | tie_both_clocks|intact_no_turnover | tie_both_clocks|intact_no_turnover |
|  | N0 | 0.250 | 0.250 | 0.500 | 5.00 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 |  |  |
|  | ND | 0.250 | 0.250 | 0.500 | 5.00 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 |  |  |
| I_STAR | target | 0.125 | 0.125 | 0.333 | 3.33 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 | tie_both_clocks|intact_no_turnover | tie_both_clocks|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 3.33 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.125 | 0.125 | 0.333 | 3.33 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
| I_TRI | target | 0.125 | 0.125 | 0.333 | 3.33 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 | tie_both_clocks|intact_no_turnover | tie_both_clocks|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 3.33 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.125 | 0.125 | 0.333 | 3.33 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |

**FREE-N5-PATHF-weak_suppress**

| Predicate | law | π(A) | ν(A) | L_ct | L_jump | entries/unit t | ρ_ct | ρ_jump | Ω | eligible share | vs N0 | vs ND |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F_2PATH | target | 0.392 | 0.360 | 0.669 | 4.07 | 0.586 | 0.669 | 0.649 | 1.055 | 0.343 | not_longer|turnover_fewer | longer_both_clocks|turnover_more |
|  | N0 | 0.687 | 0.688 | 0.917 | 9.17 | 0.750 | 0.917 | 0.917 | 2.667 | 0.327 |  |  |
|  | ND | 0.404 | 0.370 | 0.628 | 3.81 | 0.643 | 0.628 | 0.607 | 0.781 | 0.278 |  |  |
| F_STAR | target | 0.099 | 0.081 | 0.380 | 2.06 | 0.260 | 0.380 | 0.329 | 0.376 | 0.354 | not_longer|turnover_fewer | longer_both_clocks|turnover_more |
|  | N0 | 0.312 | 0.312 | 0.417 | 4.17 | 0.750 | 0.417 | 0.417 | 0.667 | 0.211 |  |  |
|  | ND | 0.082 | 0.071 | 0.354 | 2.04 | 0.232 | 0.354 | 0.325 | 0.163 | 0.157 |  |  |
| F_TRI | target | 0.092 | 0.074 | 0.337 | 1.79 | 0.273 | 0.337 | 0.286 | 0.044 | 0.056 | not_longer|turnover_fewer | not_longer|turnover_fewer |
|  | N0 | 0.289 | 0.289 | 0.407 | 4.07 | 0.711 | 0.407 | 0.407 | 0.923 | 0.301 |  |  |
|  | ND | 0.070 | 0.061 | 0.340 | 1.95 | 0.207 | 0.340 | 0.311 | 0.076 | 0.080 |  |  |
| I_2PATH | target | 0.104 | 0.092 | 0.500 | 2.90 | 0.209 | 0.500 | 0.463 | 0.000 | 0.000 | not_longer|intact_no_turnover | not_longer|intact_no_turnover |
|  | N0 | 0.250 | 0.250 | 0.500 | 5.00 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 |  |  |
|  | ND | 0.097 | 0.087 | 0.500 | 2.99 | 0.194 | 0.500 | 0.476 | 0.000 | 0.000 |  |  |
| I_STAR | target | 0.034 | 0.027 | 0.333 | 1.76 | 0.102 | 0.333 | 0.280 | 0.000 | 0.000 | not_longer|intact_no_turnover | not_longer|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 3.33 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.024 | 0.021 | 0.333 | 1.92 | 0.072 | 0.333 | 0.306 | 0.000 | 0.000 |  |  |
| I_TRI | target | 0.031 | 0.025 | 0.333 | 1.77 | 0.094 | 0.333 | 0.283 | 0.000 | 0.000 | not_longer|intact_no_turnover | not_longer|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 3.33 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.024 | 0.021 | 0.333 | 1.92 | 0.072 | 0.333 | 0.306 | 0.000 | 0.000 |  |  |

**FREE-N5-PATHH-weak_favour**

| Predicate | law | π(A) | ν(A) | L_ct | L_jump | entries/unit t | ρ_ct | ρ_jump | Ω | eligible share | vs N0 | vs ND |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F_2PATH | target | 0.376 | 0.447 | 0.289 | 4.64 | 1.303 | 0.605 | 0.648 | 0.994 | 0.273 | not_longer|turnover_fewer | longer_jump_only|turnover_more |
|  | N0 | 0.687 | 0.688 | 0.917 | 9.17 | 0.750 | 0.917 | 0.917 | 2.667 | 0.327 |  |  |
|  | ND | 0.388 | 0.351 | 0.295 | 3.62 | 1.314 | 0.618 | 0.594 | 0.721 | 0.276 |  |  |
| F_STAR | target | 0.093 | 0.128 | 0.164 | 3.05 | 0.567 | 0.345 | 0.426 | 0.286 | 0.140 | not_longer|turnover_fewer | longer_jump_only|turnover_more |
|  | N0 | 0.312 | 0.312 | 0.417 | 4.17 | 0.750 | 0.417 | 0.417 | 0.667 | 0.211 |  |  |
|  | ND | 0.074 | 0.063 | 0.168 | 1.94 | 0.442 | 0.352 | 0.319 | 0.146 | 0.155 |  |  |
| F_TRI | target | 0.082 | 0.119 | 0.138 | 2.70 | 0.596 | 0.289 | 0.377 | 0.164 | 0.096 | not_longer|turnover_fewer | longer_jump_only|turnover_more |
|  | N0 | 0.289 | 0.289 | 0.407 | 4.07 | 0.711 | 0.407 | 0.407 | 0.923 | 0.301 |  |  |
|  | ND | 0.063 | 0.054 | 0.161 | 1.86 | 0.389 | 0.338 | 0.307 | 0.059 | 0.069 |  |  |
| I_2PATH | target | 0.100 | 0.126 | 0.224 | 3.81 | 0.447 | 0.468 | 0.531 | 0.000 | 0.000 | not_longer|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.250 | 0.250 | 0.500 | 5.00 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 |  |  |
|  | ND | 0.091 | 0.081 | 0.239 | 2.88 | 0.382 | 0.500 | 0.473 | 0.000 | 0.000 |  |  |
| I_STAR | target | 0.032 | 0.045 | 0.160 | 2.99 | 0.202 | 0.335 | 0.418 | 0.000 | 0.000 | not_longer|intact_no_turnover | longer_both_clocks|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 3.33 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.021 | 0.018 | 0.159 | 1.84 | 0.135 | 0.333 | 0.302 | 0.000 | 0.000 |  |  |
| I_TRI | target | 0.028 | 0.041 | 0.128 | 2.58 | 0.216 | 0.269 | 0.360 | 0.000 | 0.000 | not_longer|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 3.33 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.021 | 0.018 | 0.159 | 1.84 | 0.135 | 0.333 | 0.302 | 0.000 | 0.000 |  |  |

**FREE-N5-PCOMP-weak_favour+weak_favour**

| Predicate | law | π(A) | ν(A) | L_ct | L_jump | entries/unit t | ρ_ct | ρ_jump | Ω | eligible share | vs N0 | vs ND |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F_2PATH | target | 0.687 | 0.948 | 0.061 | 37.48 | 11.227 | 2.719 | 2.420 | 13.598 | 0.373 | longer_jump_only|turnover_more | longer_both_clocks|turnover_more |
|  | N0 | 0.687 | 0.688 | 0.917 | 9.17 | 0.750 | 0.917 | 0.917 | 2.667 | 0.327 |  |  |
|  | ND | 0.687 | 0.687 | 0.021 | 9.17 | 33.305 | 0.917 | 0.917 | 2.667 | 0.327 |  |  |
| F_STAR | target | 0.312 | 0.765 | 0.009 | 9.50 | 35.766 | 0.388 | 0.614 | 2.268 | 0.267 | longer_jump_only|turnover_more | longer_jump_only|turnover_more |
|  | N0 | 0.312 | 0.312 | 0.417 | 4.17 | 0.750 | 0.417 | 0.417 | 0.667 | 0.211 |  |  |
|  | ND | 0.312 | 0.312 | 0.009 | 4.17 | 33.305 | 0.417 | 0.417 | 0.667 | 0.211 |  |  |
| F_TRI | target | 0.289 | 0.731 | 0.011 | 12.02 | 27.014 | 0.475 | 0.776 | 5.372 | 0.488 | longer_jump_only|turnover_more | longer_both_clocks|turnover_more |
|  | N0 | 0.289 | 0.289 | 0.407 | 4.07 | 0.711 | 0.407 | 0.407 | 0.923 | 0.301 |  |  |
|  | ND | 0.289 | 0.289 | 0.009 | 4.07 | 31.570 | 0.407 | 0.407 | 0.923 | 0.301 |  |  |
| I_2PATH | target | 0.250 | 0.608 | 0.007 | 7.92 | 34.074 | 0.326 | 0.512 | 0.000 | 0.000 | longer_jump_only|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.250 | 0.250 | 0.500 | 5.00 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 |  |  |
|  | ND | 0.250 | 0.250 | 0.011 | 5.00 | 22.203 | 0.500 | 0.500 | 0.000 | 0.000 |  |  |
| I_STAR | target | 0.125 | 0.483 | 0.003 | 5.45 | 39.363 | 0.141 | 0.352 | 0.000 | 0.000 | longer_jump_only|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 3.33 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.125 | 0.125 | 0.008 | 3.33 | 16.652 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
| I_TRI | target | 0.125 | 0.482 | 0.003 | 5.42 | 39.495 | 0.141 | 0.350 | 0.000 | 0.000 | longer_jump_only|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 3.33 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.125 | 0.125 | 0.008 | 3.33 | 16.652 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |

**FREE-N6-CLOSEW-weak_favour**

| Predicate | law | π(A) | ν(A) | L_ct | L_jump | entries/unit t | ρ_ct | ρ_jump | Ω | eligible share | vs N0 | vs ND |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F_2PATH | target | 0.990 | 0.991 | 16.803 | 445.55 | 0.059 | 16.803 | 17.159 | 147.521 | 0.332 | longer_both_clocks|turnover_more | longer_both_clocks|turnover_more |
|  | N0 | 0.812 | 0.812 | 1.300 | 19.50 | 0.625 | 1.300 | 1.300 | 5.500 | 0.297 |  |  |
|  | ND | 0.994 | 0.981 | 6.091 | 159.10 | 0.163 | 6.091 | 6.684 | 51.809 | 0.328 |  |  |
| F_STAR | target | 0.960 | 0.961 | 3.443 | 91.25 | 0.279 | 3.443 | 3.514 | 29.156 | 0.323 | longer_both_clocks|turnover_more | longer_both_clocks|turnover_more |
|  | N0 | 0.500 | 0.500 | 0.533 | 8.00 | 0.938 | 0.533 | 0.533 | 1.667 | 0.238 |  |  |
|  | ND | 0.967 | 0.910 | 1.584 | 39.49 | 0.610 | 1.584 | 1.659 | 11.853 | 0.308 |  |  |
| F_TRI | target | 0.876 | 0.859 | 0.926 | 24.03 | 0.946 | 0.926 | 0.925 | 11.963 | 0.519 | longer_both_clocks|turnover_more | longer_both_clocks|turnover_more |
|  | N0 | 0.342 | 0.342 | 0.448 | 6.71 | 0.764 | 0.448 | 0.448 | 1.514 | 0.265 |  |  |
|  | ND | 0.874 | 0.768 | 0.821 | 19.12 | 1.064 | 0.821 | 0.803 | 8.565 | 0.473 |  |  |
| I_2PATH | target | 0.790 | 0.757 | 0.500 | 12.68 | 1.580 | 0.500 | 0.488 | 0.000 | 0.000 | longer_jump_only|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.250 | 0.250 | 0.500 | 7.50 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 |  |  |
|  | ND | 0.787 | 0.640 | 0.547 | 11.78 | 1.438 | 0.547 | 0.495 | 0.000 | 0.000 |  |  |
| I_STAR | target | 0.714 | 0.666 | 0.333 | 8.23 | 2.143 | 0.333 | 0.317 | 0.000 | 0.000 | longer_jump_only|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 5.00 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.708 | 0.522 | 0.396 | 7.74 | 1.788 | 0.396 | 0.325 | 0.000 | 0.000 |  |  |
| I_TRI | target | 0.716 | 0.667 | 0.333 | 8.22 | 2.149 | 0.333 | 0.317 | 0.000 | 0.000 | longer_jump_only|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 5.00 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.708 | 0.522 | 0.396 | 7.74 | 1.788 | 0.396 | 0.325 | 0.000 | 0.000 |  |  |

**FREE-N6-CSPH-strong_favour+weak_favour**

| Predicate | law | π(A) | ν(A) | L_ct | L_jump | entries/unit t | ρ_ct | ρ_jump | Ω | eligible share | vs N0 | vs ND |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F_2PATH | target | 0.472 | 0.547 | 0.158 | 7.70 | 2.982 | 0.753 | 0.752 | 2.020 | 0.301 | not_longer|turnover_fewer | longer_both_clocks|turnover_more |
|  | N0 | 0.812 | 0.812 | 1.300 | 19.50 | 0.625 | 1.300 | 1.300 | 5.500 | 0.297 |  |  |
|  | ND | 0.469 | 0.437 | 0.146 | 5.71 | 3.213 | 0.694 | 0.678 | 1.213 | 0.258 |  |  |
| F_STAR | target | 0.162 | 0.244 | 0.068 | 4.30 | 2.391 | 0.323 | 0.419 | 0.520 | 0.158 | not_longer|turnover_fewer | longer_jump_only|turnover_more |
|  | N0 | 0.500 | 0.500 | 0.533 | 8.00 | 0.938 | 0.533 | 0.533 | 1.667 | 0.238 |  |  |
|  | ND | 0.131 | 0.116 | 0.079 | 2.96 | 1.649 | 0.378 | 0.351 | 0.364 | 0.186 |  |  |
| F_TRI | target | 0.151 | 0.203 | 0.071 | 4.01 | 2.128 | 0.337 | 0.392 | 0.778 | 0.258 | not_longer|turnover_fewer | longer_jump_only|turnover_more |
|  | N0 | 0.342 | 0.342 | 0.448 | 6.71 | 0.764 | 0.448 | 0.448 | 1.514 | 0.265 |  |  |
|  | ND | 0.069 | 0.061 | 0.072 | 2.67 | 0.955 | 0.344 | 0.317 | 0.136 | 0.082 |  |  |
| I_2PATH | target | 0.092 | 0.128 | 0.095 | 5.53 | 0.969 | 0.452 | 0.540 | 0.000 | 0.000 | not_longer|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.250 | 0.250 | 0.500 | 7.50 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 |  |  |
|  | ND | 0.078 | 0.071 | 0.105 | 4.02 | 0.742 | 0.499 | 0.478 | 0.000 | 0.000 |  |  |
| I_STAR | target | 0.030 | 0.051 | 0.067 | 4.80 | 0.443 | 0.317 | 0.469 | 0.000 | 0.000 | not_longer|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 5.00 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.018 | 0.016 | 0.070 | 2.58 | 0.259 | 0.333 | 0.306 | 0.000 | 0.000 |  |  |
| I_TRI | target | 0.041 | 0.060 | 0.053 | 3.26 | 0.772 | 0.250 | 0.318 | 0.000 | 0.000 | not_longer|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 5.00 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.018 | 0.016 | 0.070 | 2.58 | 0.259 | 0.333 | 0.306 | 0.000 | 0.000 |  |  |

**FREE-N6-NULL-none**

| Predicate | law | π(A) | ν(A) | L_ct | L_jump | entries/unit t | ρ_ct | ρ_jump | Ω | eligible share | vs N0 | vs ND |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F_2PATH | target | 0.812 | 0.812 | 1.300 | 19.50 | 0.625 | 1.300 | 1.300 | 5.500 | 0.297 | tie_both_clocks|turnover_tie | tie_both_clocks|turnover_tie |
|  | N0 | 0.812 | 0.812 | 1.300 | 19.50 | 0.625 | 1.300 | 1.300 | 5.500 | 0.297 |  |  |
|  | ND | 0.812 | 0.812 | 1.300 | 19.50 | 0.625 | 1.300 | 1.300 | 5.500 | 0.297 |  |  |
| F_STAR | target | 0.500 | 0.500 | 0.533 | 8.00 | 0.938 | 0.533 | 0.533 | 1.667 | 0.238 | tie_both_clocks|turnover_tie | tie_both_clocks|turnover_tie |
|  | N0 | 0.500 | 0.500 | 0.533 | 8.00 | 0.938 | 0.533 | 0.533 | 1.667 | 0.238 |  |  |
|  | ND | 0.500 | 0.500 | 0.533 | 8.00 | 0.937 | 0.533 | 0.533 | 1.667 | 0.238 |  |  |
| F_TRI | target | 0.342 | 0.342 | 0.448 | 6.71 | 0.764 | 0.448 | 0.448 | 1.514 | 0.265 | tie_both_clocks|turnover_tie | tie_both_clocks|turnover_tie |
|  | N0 | 0.342 | 0.342 | 0.448 | 6.71 | 0.764 | 0.448 | 0.448 | 1.514 | 0.265 |  |  |
|  | ND | 0.342 | 0.342 | 0.448 | 6.71 | 0.764 | 0.448 | 0.448 | 1.514 | 0.265 |  |  |
| I_2PATH | target | 0.250 | 0.250 | 0.500 | 7.50 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 | tie_both_clocks|intact_no_turnover | tie_both_clocks|intact_no_turnover |
|  | N0 | 0.250 | 0.250 | 0.500 | 7.50 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 |  |  |
|  | ND | 0.250 | 0.250 | 0.500 | 7.50 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 |  |  |
| I_STAR | target | 0.125 | 0.125 | 0.333 | 5.00 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 | tie_both_clocks|intact_no_turnover | tie_both_clocks|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 5.00 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.125 | 0.125 | 0.333 | 5.00 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
| I_TRI | target | 0.125 | 0.125 | 0.333 | 5.00 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 | tie_both_clocks|intact_no_turnover | tie_both_clocks|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 5.00 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.125 | 0.125 | 0.333 | 5.00 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |

**FREE-N6-PATHF-weak_suppress**

| Predicate | law | π(A) | ν(A) | L_ct | L_jump | entries/unit t | ρ_ct | ρ_jump | Ω | eligible share | vs N0 | vs ND |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F_2PATH | target | 0.413 | 0.384 | 0.700 | 5.44 | 0.590 | 0.700 | 0.685 | 1.281 | 0.289 | not_longer|turnover_fewer | longer_both_clocks|turnover_more |
|  | N0 | 0.812 | 0.812 | 1.300 | 19.50 | 0.625 | 1.300 | 1.300 | 5.500 | 0.297 |  |  |
|  | ND | 0.433 | 0.400 | 0.671 | 5.18 | 0.644 | 0.671 | 0.654 | 1.065 | 0.255 |  |  |
| F_STAR | target | 0.118 | 0.098 | 0.411 | 2.86 | 0.287 | 0.411 | 0.361 | 0.636 | 0.341 | not_longer|turnover_fewer | longer_both_clocks|turnover_more |
|  | N0 | 0.500 | 0.500 | 0.533 | 8.00 | 0.938 | 0.533 | 0.533 | 1.667 | 0.238 |  |  |
|  | ND | 0.110 | 0.097 | 0.372 | 2.72 | 0.297 | 0.372 | 0.343 | 0.314 | 0.183 |  |  |
| F_TRI | target | 0.071 | 0.058 | 0.338 | 2.30 | 0.209 | 0.338 | 0.290 | 0.046 | 0.035 | not_longer|turnover_fewer | not_longer|turnover_fewer |
|  | N0 | 0.342 | 0.342 | 0.448 | 6.71 | 0.764 | 0.448 | 0.448 | 1.514 | 0.265 |  |  |
|  | ND | 0.057 | 0.049 | 0.342 | 2.48 | 0.166 | 0.342 | 0.312 | 0.102 | 0.069 |  |  |
| I_2PATH | target | 0.072 | 0.064 | 0.500 | 3.67 | 0.145 | 0.500 | 0.462 | 0.000 | 0.000 | not_longer|intact_no_turnover | not_longer|intact_no_turnover |
|  | N0 | 0.250 | 0.250 | 0.500 | 7.50 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 |  |  |
|  | ND | 0.069 | 0.062 | 0.500 | 3.78 | 0.138 | 0.500 | 0.476 | 0.000 | 0.000 |  |  |
| I_STAR | target | 0.020 | 0.016 | 0.333 | 2.20 | 0.059 | 0.333 | 0.277 | 0.000 | 0.000 | not_longer|intact_no_turnover | not_longer|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 5.00 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.015 | 0.013 | 0.333 | 2.41 | 0.044 | 0.333 | 0.304 | 0.000 | 0.000 |  |  |
| I_TRI | target | 0.018 | 0.015 | 0.333 | 2.27 | 0.054 | 0.333 | 0.286 | 0.000 | 0.000 | not_longer|intact_no_turnover | not_longer|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 5.00 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.015 | 0.013 | 0.333 | 2.41 | 0.044 | 0.333 | 0.304 | 0.000 | 0.000 |  |  |

**FREE-N6-PATHH-weak_favour**

| Predicate | law | π(A) | ν(A) | L_ct | L_jump | entries/unit t | ρ_ct | ρ_jump | Ω | eligible share | vs N0 | vs ND |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F_2PATH | target | 0.386 | 0.449 | 0.224 | 5.71 | 1.725 | 0.611 | 0.647 | 1.184 | 0.251 | not_longer|turnover_fewer | longer_jump_only|turnover_more |
|  | N0 | 0.812 | 0.812 | 1.300 | 19.50 | 0.625 | 1.300 | 1.300 | 5.500 | 0.297 |  |  |
|  | ND | 0.408 | 0.374 | 0.240 | 4.83 | 1.699 | 0.656 | 0.636 | 0.968 | 0.253 |  |  |
| F_STAR | target | 0.111 | 0.146 | 0.134 | 3.87 | 0.826 | 0.366 | 0.439 | 0.474 | 0.165 | not_longer|turnover_fewer | longer_jump_only|turnover_more |
|  | N0 | 0.500 | 0.500 | 0.533 | 8.00 | 0.938 | 0.533 | 0.533 | 1.667 | 0.238 |  |  |
|  | ND | 0.097 | 0.084 | 0.135 | 2.56 | 0.721 | 0.368 | 0.337 | 0.283 | 0.181 |  |  |
| F_TRI | target | 0.059 | 0.084 | 0.100 | 3.12 | 0.595 | 0.272 | 0.353 | 0.153 | 0.072 | not_longer|turnover_fewer | longer_jump_only|turnover_more |
|  | N0 | 0.342 | 0.342 | 0.448 | 6.71 | 0.764 | 0.448 | 0.448 | 1.514 | 0.265 |  |  |
|  | ND | 0.049 | 0.042 | 0.124 | 2.35 | 0.394 | 0.340 | 0.309 | 0.083 | 0.062 |  |  |
| I_2PATH | target | 0.069 | 0.085 | 0.172 | 4.68 | 0.398 | 0.471 | 0.530 | 0.000 | 0.000 | not_longer|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.250 | 0.250 | 0.500 | 7.50 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 |  |  |
|  | ND | 0.063 | 0.057 | 0.183 | 3.60 | 0.345 | 0.500 | 0.474 | 0.000 | 0.000 |  |  |
| I_STAR | target | 0.020 | 0.026 | 0.133 | 3.90 | 0.147 | 0.364 | 0.441 | 0.000 | 0.000 | not_longer|intact_no_turnover | longer_both_clocks|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 5.00 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.013 | 0.011 | 0.122 | 2.30 | 0.104 | 0.333 | 0.303 | 0.000 | 0.000 |  |  |
| I_TRI | target | 0.015 | 0.022 | 0.093 | 2.99 | 0.161 | 0.255 | 0.338 | 0.000 | 0.000 | not_longer|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 5.00 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.013 | 0.011 | 0.122 | 2.30 | 0.104 | 0.333 | 0.303 | 0.000 | 0.000 |  |  |

**FREE-N6-PCOMP-weak_favour+weak_favour**

| Predicate | law | π(A) | ν(A) | L_ct | L_jump | entries/unit t | ρ_ct | ρ_jump | Ω | eligible share | vs N0 | vs ND |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F_2PATH | target | 0.812 | 0.996 | 0.007 | 601.97 | 114.347 | 32.747 | 23.418 | 199.428 | 0.332 | longer_jump_only|turnover_more | longer_both_clocks|turnover_more |
|  | N0 | 0.812 | 0.812 | 1.300 | 19.50 | 0.625 | 1.300 | 1.300 | 5.500 | 0.297 |  |  |
|  | ND | 0.812 | 0.812 | 2.82e-04 | 19.50 | 2880.419 | 1.300 | 1.300 | 5.500 | 0.297 |  |  |
| F_STAR | target | 0.500 | 0.966 | 5.09e-04 | 68.06 | 981.372 | 2.348 | 2.648 | 21.237 | 0.317 | longer_jump_only|turnover_more | longer_both_clocks|turnover_more |
|  | N0 | 0.500 | 0.500 | 0.533 | 8.00 | 0.938 | 0.533 | 0.533 | 1.667 | 0.238 |  |  |
|  | ND | 0.500 | 0.500 | 1.16e-04 | 8.00 | 4320.629 | 0.533 | 0.533 | 1.667 | 0.238 |  |  |
| F_TRI | target | 0.342 | 0.852 | 1.43e-04 | 24.59 | 2396.607 | 0.657 | 0.957 | 11.412 | 0.484 | longer_jump_only|turnover_more | longer_both_clocks|turnover_more |
|  | N0 | 0.342 | 0.342 | 0.448 | 6.71 | 0.764 | 0.448 | 0.448 | 1.514 | 0.265 |  |  |
|  | ND | 0.342 | 0.342 | 9.71e-05 | 6.71 | 3519.512 | 0.448 | 0.448 | 1.514 | 0.265 |  |  |
| I_2PATH | target | 0.250 | 0.739 | 6.29e-05 | 12.84 | 3977.668 | 0.290 | 0.499 | 0.000 | 0.000 | longer_jump_only|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.250 | 0.250 | 0.500 | 7.50 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 |  |  |
|  | ND | 0.250 | 0.250 | 1.08e-04 | 7.50 | 2304.335 | 0.500 | 0.500 | 0.000 | 0.000 |  |  |
| I_STAR | target | 0.125 | 0.640 | 2.42e-05 | 8.58 | 5155.636 | 0.112 | 0.334 | 0.000 | 0.000 | longer_jump_only|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 5.00 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.125 | 0.125 | 7.23e-05 | 5.00 | 1728.251 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
| I_TRI | target | 0.125 | 0.640 | 2.42e-05 | 8.56 | 5167.024 | 0.111 | 0.333 | 0.000 | 0.000 | longer_jump_only|intact_no_turnover | longer_jump_only|intact_no_turnover |
|  | N0 | 0.125 | 0.125 | 0.333 | 5.00 | 0.375 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |
|  | ND | 0.125 | 0.125 | 7.23e-05 | 5.00 | 1728.251 | 0.333 | 0.333 | 0.000 | 0.000 |  |  |

## Lifetime and ρ ratios (target / comparator)

| Item | Predicate | L_ct/N0 | L_jump/N0 | L_ct/ND | L_jump/ND | ρ_ct/ND | ρ_jump/ND | Ω − Ω_ND | π/π_ND |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FREE-N5-CLOSEW-weak_favour | F_2PATH | 2.775 | 4.246 | 1.804 | 1.963 | 1.804 | 1.713 | 7.694 | 0.991 |
| FREE-N5-CLOSEW-weak_favour | F_STAR | 1.772 | 2.699 | 1.193 | 1.513 | 1.193 | 1.321 | 1.470 | 1.005 |
| FREE-N5-CLOSEW-weak_favour | F_TRI | 1.645 | 2.476 | 1.102 | 1.393 | 1.102 | 1.216 | 2.057 | 1.023 |
| FREE-N5-CLOSEW-weak_favour | I_2PATH | 1.000 | 1.483 | 0.864 | 1.121 | 0.864 | 0.978 | 0.000 | 1.008 |
| FREE-N5-CLOSEW-weak_favour | I_STAR | 1.000 | 1.445 | 0.754 | 1.097 | 0.754 | 0.958 | 0.000 | 1.018 |
| FREE-N5-CLOSEW-weak_favour | I_TRI | 1.000 | 1.438 | 0.754 | 1.092 | 0.754 | 0.953 | 0.000 | 1.031 |
| FREE-N5-CSPH-strong_favour+weak_favour | F_2PATH | 0.240 | 0.772 | 1.188 | 1.517 | 1.188 | 1.215 | 0.955 | 1.048 |
| FREE-N5-CSPH-strong_favour+weak_favour | F_STAR | 0.183 | 0.850 | 0.776 | 1.481 | 0.776 | 1.186 | 0.062 | 1.269 |
| FREE-N5-CSPH-strong_favour+weak_favour | F_TRI | 0.250 | 0.939 | 1.082 | 1.676 | 1.082 | 1.342 | 0.782 | 1.997 |
| FREE-N5-CSPH-strong_favour+weak_favour | I_2PATH | 0.242 | 0.947 | 0.882 | 1.389 | 0.882 | 1.112 | 0.000 | 1.156 |
| FREE-N5-CSPH-strong_favour+weak_favour | I_STAR | 0.219 | 1.114 | 0.810 | 1.692 | 0.810 | 1.355 | 0.000 | 1.415 |
| FREE-N5-CSPH-strong_favour+weak_favour | I_TRI | 0.212 | 0.895 | 0.784 | 1.361 | 0.784 | 1.090 | 0.000 | 2.040 |
| FREE-N5-NULL-none | F_2PATH | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 8.88e-16 | 1.000 |
| FREE-N5-NULL-none | F_STAR | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 5.55e-16 | 1.000 |
| FREE-N5-NULL-none | F_TRI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 8.88e-16 | 1.000 |
| FREE-N5-NULL-none | I_2PATH | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| FREE-N5-NULL-none | I_STAR | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| FREE-N5-NULL-none | I_TRI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| FREE-N5-PATHF-weak_suppress | F_2PATH | 0.730 | 0.444 | 1.066 | 1.069 | 1.066 | 1.069 | 0.274 | 0.971 |
| FREE-N5-PATHF-weak_suppress | F_STAR | 0.913 | 0.495 | 1.075 | 1.012 | 1.075 | 1.012 | 0.214 | 1.204 |
| FREE-N5-PATHF-weak_suppress | F_TRI | 0.830 | 0.441 | 0.993 | 0.918 | 0.993 | 0.918 | -0.031 | 1.311 |
| FREE-N5-PATHF-weak_suppress | I_2PATH | 1.000 | 0.581 | 1.000 | 0.973 | 1.000 | 0.973 | 0.000 | 1.076 |
| FREE-N5-PATHF-weak_suppress | I_STAR | 1.000 | 0.527 | 1.000 | 0.917 | 1.000 | 0.917 | 0.000 | 1.408 |
| FREE-N5-PATHF-weak_suppress | I_TRI | 1.000 | 0.532 | 1.000 | 0.925 | 1.000 | 0.925 | 0.000 | 1.299 |
| FREE-N5-PATHH-weak_favour | F_2PATH | 0.315 | 0.506 | 0.979 | 1.283 | 0.979 | 1.089 | 0.273 | 0.971 |
| FREE-N5-PATHH-weak_favour | F_STAR | 0.395 | 0.732 | 0.980 | 1.570 | 0.980 | 1.333 | 0.140 | 1.257 |
| FREE-N5-PATHH-weak_favour | F_TRI | 0.339 | 0.664 | 0.854 | 1.448 | 0.854 | 1.230 | 0.104 | 1.307 |
| FREE-N5-PATHH-weak_favour | I_2PATH | 0.447 | 0.761 | 0.937 | 1.323 | 0.937 | 1.123 | 0.000 | 1.094 |
| FREE-N5-PATHH-weak_favour | I_STAR | 0.479 | 0.898 | 1.004 | 1.628 | 1.004 | 1.383 | 0.000 | 1.511 |
| FREE-N5-PATHH-weak_favour | I_TRI | 0.385 | 0.775 | 0.807 | 1.405 | 0.807 | 1.193 | 0.000 | 1.297 |
| FREE-N5-PCOMP-weak_favour+weak_favour | F_2PATH | 0.067 | 4.089 | 2.967 | 4.089 | 2.967 | 2.640 | 10.931 | 1.000 |
| FREE-N5-PCOMP-weak_favour+weak_favour | F_STAR | 0.021 | 2.281 | 0.931 | 2.281 | 0.931 | 1.473 | 1.602 | 1.000 |
| FREE-N5-PCOMP-weak_favour+weak_favour | F_TRI | 0.026 | 2.956 | 1.169 | 2.956 | 1.169 | 1.909 | 4.449 | 1.000 |
| FREE-N5-PCOMP-weak_favour+weak_favour | I_2PATH | 0.015 | 1.584 | 0.652 | 1.584 | 0.652 | 1.023 | 0.000 | 1.000 |
| FREE-N5-PCOMP-weak_favour+weak_favour | I_STAR | 0.010 | 1.636 | 0.423 | 1.636 | 0.423 | 1.057 | 0.000 | 1.000 |
| FREE-N5-PCOMP-weak_favour+weak_favour | I_TRI | 0.009 | 1.627 | 0.422 | 1.627 | 0.422 | 1.051 | 0.000 | 1.000 |
| FREE-N6-CLOSEW-weak_favour | F_2PATH | 12.925 | 22.849 | 2.759 | 2.800 | 2.759 | 2.567 | 95.712 | 0.996 |
| FREE-N6-CLOSEW-weak_favour | F_STAR | 6.456 | 11.406 | 2.173 | 2.311 | 2.173 | 2.118 | 17.303 | 0.993 |
| FREE-N6-CLOSEW-weak_favour | F_TRI | 2.068 | 3.579 | 1.127 | 1.257 | 1.127 | 1.152 | 3.398 | 1.002 |
| FREE-N6-CLOSEW-weak_favour | I_2PATH | 1.000 | 1.691 | 0.913 | 1.076 | 0.913 | 0.987 | 0.000 | 1.004 |
| FREE-N6-CLOSEW-weak_favour | I_STAR | 1.000 | 1.646 | 0.842 | 1.064 | 0.842 | 0.975 | 0.000 | 1.009 |
| FREE-N6-CLOSEW-weak_favour | I_TRI | 1.000 | 1.644 | 0.842 | 1.063 | 0.842 | 0.974 | 0.000 | 1.012 |
| FREE-N6-CSPH-strong_favour+weak_favour | F_2PATH | 0.122 | 0.395 | 1.085 | 1.349 | 1.085 | 1.109 | 0.807 | 1.007 |
| FREE-N6-CSPH-strong_favour+weak_favour | F_STAR | 0.127 | 0.537 | 0.855 | 1.451 | 0.855 | 1.194 | 0.155 | 1.241 |
| FREE-N6-CSPH-strong_favour+weak_favour | F_TRI | 0.158 | 0.598 | 0.979 | 1.500 | 0.979 | 1.234 | 0.642 | 2.183 |
| FREE-N6-CSPH-strong_favour+weak_favour | I_2PATH | 0.190 | 0.738 | 0.905 | 1.375 | 0.905 | 1.131 | 0.000 | 1.181 |
| FREE-N6-CSPH-strong_favour+weak_favour | I_STAR | 0.200 | 0.960 | 0.954 | 1.859 | 0.954 | 1.529 | 0.000 | 1.633 |
| FREE-N6-CSPH-strong_favour+weak_favour | I_TRI | 0.158 | 0.651 | 0.751 | 1.262 | 0.751 | 1.038 | 0.000 | 2.238 |
| FREE-N6-NULL-none | F_2PATH | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | -2.66e-15 | 1.000 |
| FREE-N6-NULL-none | F_STAR | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | -2.22e-16 | 1.000 |
| FREE-N6-NULL-none | F_TRI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| FREE-N6-NULL-none | I_2PATH | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| FREE-N6-NULL-none | I_STAR | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| FREE-N6-NULL-none | I_TRI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| FREE-N6-PATHF-weak_suppress | F_2PATH | 0.538 | 0.279 | 1.042 | 1.049 | 1.042 | 1.049 | 0.216 | 0.954 |
| FREE-N6-PATHF-weak_suppress | F_STAR | 0.770 | 0.358 | 1.103 | 1.052 | 1.103 | 1.052 | 0.321 | 1.067 |
| FREE-N6-PATHF-weak_suppress | F_TRI | 0.754 | 0.342 | 0.988 | 0.928 | 0.988 | 0.928 | -0.056 | 1.245 |
| FREE-N6-PATHF-weak_suppress | I_2PATH | 1.000 | 0.489 | 1.000 | 0.971 | 1.000 | 0.971 | 0.000 | 1.050 |
| FREE-N6-PATHF-weak_suppress | I_STAR | 1.000 | 0.440 | 1.000 | 0.913 | 1.000 | 0.913 | 0.000 | 1.347 |
| FREE-N6-PATHF-weak_suppress | I_TRI | 1.000 | 0.454 | 1.000 | 0.941 | 1.000 | 0.941 | 0.000 | 1.223 |
| FREE-N6-PATHH-weak_favour | F_2PATH | 0.172 | 0.293 | 0.932 | 1.182 | 0.932 | 1.017 | 0.216 | 0.946 |
| FREE-N6-PATHH-weak_favour | F_STAR | 0.251 | 0.484 | 0.994 | 1.512 | 0.994 | 1.300 | 0.191 | 1.139 |
| FREE-N6-PATHH-weak_favour | F_TRI | 0.223 | 0.465 | 0.800 | 1.329 | 0.800 | 1.143 | 0.070 | 1.207 |
| FREE-N6-PATHH-weak_favour | I_2PATH | 0.345 | 0.624 | 0.943 | 1.297 | 0.943 | 1.116 | 0.000 | 1.088 |
| FREE-N6-PATHH-weak_favour | I_STAR | 0.400 | 0.779 | 1.093 | 1.695 | 1.093 | 1.458 | 0.000 | 1.552 |
| FREE-N6-PATHH-weak_favour | I_TRI | 0.280 | 0.597 | 0.765 | 1.300 | 0.765 | 1.118 | 0.000 | 1.188 |
| FREE-N6-PCOMP-weak_favour+weak_favour | F_2PATH | 0.005 | 30.870 | 25.190 | 30.870 | 25.190 | 18.014 | 193.928 | 1.000 |
| FREE-N6-PCOMP-weak_favour+weak_favour | F_STAR | 9.55e-04 | 8.508 | 4.403 | 8.508 | 4.403 | 4.965 | 19.570 | 1.000 |
| FREE-N6-PCOMP-weak_favour+weak_favour | F_TRI | 3.19e-04 | 3.662 | 1.469 | 3.662 | 1.469 | 2.137 | 9.898 | 1.000 |
| FREE-N6-PCOMP-weak_favour+weak_favour | I_2PATH | 1.26e-04 | 1.711 | 0.579 | 1.711 | 0.579 | 0.999 | 0.000 | 1.000 |
| FREE-N6-PCOMP-weak_favour+weak_favour | I_STAR | 7.27e-05 | 1.717 | 0.335 | 1.717 | 0.335 | 1.002 | 0.000 | 1.000 |
| FREE-N6-PCOMP-weak_favour+weak_favour | I_TRI | 7.26e-05 | 1.712 | 0.334 | 1.712 | 0.334 | 0.999 | 0.000 | 1.000 |

## Lagged hub (hub chosen once at a stationary start)

Normalised gap = (hub degree − comparison degree at lag) / (same at lag 0). Retention = expected initial neighbours still adjacent / expected initial degree.

**FREE-N5-CLOSEW-weak_favour**

| clock | lag | gap target / N0 / ND | normalised gap target / N0 / ND | hub retention target / N0 / ND | comparison retention target | decay vs ND | decay vs N0 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| continuous | 0 | 0.694 / 0.977 / 0.664 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| continuous | 1 | 0.524 / 0.800 / 0.491 | 0.754 / 0.819 / 0.740 | 0.944 / 0.909 / 0.938 | 0.944 | slower | faster |
| continuous | 16 | 0.020 / 0.040 / 0.006 | 0.029 / 0.041 / 0.009 | 0.766 / 0.520 / 0.760 | 0.768 | slower | faster |
| continuous | 2 | 0.403 / 0.655 / 0.364 | 0.580 / 0.670 / 0.548 | 0.904 / 0.835 / 0.893 | 0.904 | slower | faster |
| continuous | 4 | 0.248 / 0.439 / 0.200 | 0.357 / 0.449 / 0.302 | 0.851 / 0.725 / 0.834 | 0.852 | slower | faster |
| continuous | 8 | 0.102 / 0.197 / 0.061 | 0.147 / 0.202 / 0.092 | 0.798 / 0.601 / 0.783 | 0.800 | slower | faster |
| jump | 0 | 0.723 / 0.977 / 0.838 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| jump | 1 | 0.518 / 0.781 / 0.638 | 0.717 / 0.800 / 0.761 | 0.934 / 0.900 / 0.924 | 0.934 | faster | faster |
| jump | 16 | 0.011 / 0.027 / 0.013 | 0.015 / 0.028 / 0.016 | 0.759 / 0.514 / 0.666 | 0.760 | faster | faster |
| jump | 2 | 0.383 / 0.625 / 0.488 | 0.530 / 0.640 / 0.583 | 0.889 / 0.820 / 0.865 | 0.890 | faster | faster |
| jump | 4 | 0.220 / 0.400 / 0.289 | 0.304 / 0.410 / 0.345 | 0.834 / 0.705 / 0.785 | 0.834 | faster | faster |
| jump | 8 | 0.078 / 0.164 / 0.103 | 0.108 / 0.168 / 0.122 | 0.784 / 0.584 / 0.707 | 0.785 | faster | faster |

**FREE-N5-CSPH-strong_favour+weak_favour**

| clock | lag | gap target / N0 / ND | normalised gap target / N0 / ND | hub retention target / N0 / ND | comparison retention target | decay vs ND | decay vs N0 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| continuous | 0 | 1.163 / 0.977 / 0.985 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| continuous | 1 | 1.003 / 0.800 / 0.803 | 0.862 / 0.819 / 0.815 | 0.912 / 0.909 / 0.880 | 0.891 | slower | slower |
| continuous | 16 | 0.159 / 0.040 / 0.039 | 0.137 / 0.041 / 0.040 | 0.450 / 0.520 / 0.395 | 0.442 | slower | slower |
| continuous | 2 | 0.869 / 0.655 / 0.655 | 0.747 / 0.670 / 0.665 | 0.838 / 0.835 / 0.784 | 0.811 | slower | slower |
| continuous | 4 | 0.662 / 0.439 / 0.437 | 0.569 / 0.449 / 0.444 | 0.724 / 0.725 / 0.644 | 0.696 | slower | slower |
| continuous | 8 | 0.400 / 0.197 / 0.195 | 0.344 / 0.202 / 0.198 | 0.579 / 0.601 / 0.492 | 0.560 | slower | slower |
| jump | 0 | 1.225 / 0.977 / 0.973 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| jump | 1 | 1.050 / 0.781 / 0.771 | 0.857 / 0.800 / 0.792 | 0.916 / 0.900 / 0.862 | 0.888 | slower | slower |
| jump | 16 | 0.157 / 0.027 / 0.023 | 0.128 / 0.028 / 0.024 | 0.506 / 0.514 / 0.372 | 0.494 | slower | slower |
| jump | 2 | 0.910 / 0.625 / 0.611 | 0.743 / 0.640 / 0.628 | 0.847 / 0.820 / 0.754 | 0.808 | slower | slower |
| jump | 4 | 0.696 / 0.400 / 0.383 | 0.568 / 0.410 / 0.394 | 0.742 / 0.705 / 0.604 | 0.700 | slower | slower |
| jump | 8 | 0.419 / 0.164 / 0.151 | 0.342 / 0.168 / 0.155 | 0.614 / 0.584 / 0.453 | 0.584 | slower | slower |

**FREE-N5-NULL-none**

| clock | lag | gap target / N0 / ND | normalised gap target / N0 / ND | hub retention target / N0 / ND | comparison retention target | decay vs ND | decay vs N0 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| continuous | 0 | 0.977 / 0.977 / 0.977 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| continuous | 1 | 0.800 / 0.800 / 0.800 | 0.819 / 0.819 / 0.819 | 0.909 / 0.909 / 0.909 | 0.909 | tie | tie |
| continuous | 16 | 0.040 / 0.040 / 0.040 | 0.041 / 0.041 / 0.041 | 0.520 / 0.520 / 0.520 | 0.520 | tie | tie |
| continuous | 2 | 0.655 / 0.655 / 0.655 | 0.670 / 0.670 / 0.670 | 0.835 / 0.835 / 0.835 | 0.835 | tie | tie |
| continuous | 4 | 0.439 / 0.439 / 0.439 | 0.449 / 0.449 / 0.449 | 0.725 / 0.725 / 0.725 | 0.725 | tie | tie |
| continuous | 8 | 0.197 / 0.197 / 0.197 | 0.202 / 0.202 / 0.202 | 0.601 / 0.601 / 0.601 | 0.601 | tie | tie |
| jump | 0 | 0.977 / 0.977 / 0.977 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| jump | 1 | 0.781 / 0.781 / 0.781 | 0.800 / 0.800 / 0.800 | 0.900 / 0.900 / 0.900 | 0.900 | tie | tie |
| jump | 16 | 0.027 / 0.027 / 0.027 | 0.028 / 0.028 / 0.028 | 0.514 / 0.514 / 0.514 | 0.514 | tie | tie |
| jump | 2 | 0.625 / 0.625 / 0.625 | 0.640 / 0.640 / 0.640 | 0.820 / 0.820 / 0.820 | 0.820 | tie | tie |
| jump | 4 | 0.400 / 0.400 / 0.400 | 0.410 / 0.410 / 0.410 | 0.705 / 0.705 / 0.705 | 0.705 | tie | tie |
| jump | 8 | 0.164 / 0.164 / 0.164 | 0.168 / 0.168 / 0.168 | 0.584 / 0.584 / 0.584 | 0.584 | tie | tie |

**FREE-N5-PATHF-weak_suppress**

| clock | lag | gap target / N0 / ND | normalised gap target / N0 / ND | hub retention target / N0 / ND | comparison retention target | decay vs ND | decay vs N0 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| continuous | 0 | 1.102 / 0.977 / 0.961 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| continuous | 1 | 0.929 / 0.800 / 0.775 | 0.843 / 0.819 / 0.806 | 0.867 / 0.909 / 0.866 | 0.867 | slower | slower |
| continuous | 16 | 0.064 / 0.040 / 0.032 | 0.058 / 0.041 / 0.034 | 0.359 / 0.520 / 0.353 | 0.356 | slower | slower |
| continuous | 2 | 0.781 / 0.655 / 0.625 | 0.709 / 0.670 / 0.651 | 0.764 / 0.835 / 0.760 | 0.762 | slower | slower |
| continuous | 4 | 0.551 / 0.439 / 0.409 | 0.500 / 0.449 / 0.426 | 0.618 / 0.725 / 0.609 | 0.613 | slower | slower |
| continuous | 8 | 0.270 / 0.197 / 0.176 | 0.245 / 0.202 / 0.183 | 0.461 / 0.601 / 0.450 | 0.455 | slower | slower |
| jump | 0 | 1.031 / 0.977 / 0.943 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| jump | 1 | 0.845 / 0.781 / 0.735 | 0.819 / 0.800 / 0.779 | 0.840 / 0.900 / 0.843 | 0.841 | slower | slower |
| jump | 16 | 0.031 / 0.027 / 0.017 | 0.030 / 0.028 / 0.018 | 0.328 / 0.514 / 0.326 | 0.327 | slower | slower |
| jump | 2 | 0.685 / 0.625 / 0.573 | 0.665 / 0.640 / 0.607 | 0.721 / 0.820 / 0.723 | 0.722 | slower | slower |
| jump | 4 | 0.445 / 0.400 / 0.348 | 0.431 / 0.410 / 0.369 | 0.563 / 0.705 / 0.560 | 0.561 | slower | slower |
| jump | 8 | 0.184 / 0.164 / 0.128 | 0.178 / 0.168 / 0.136 | 0.410 / 0.584 / 0.404 | 0.407 | slower | slower |

**FREE-N5-PATHH-weak_favour**

| clock | lag | gap target / N0 / ND | normalised gap target / N0 / ND | hub retention target / N0 / ND | comparison retention target | decay vs ND | decay vs N0 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| continuous | 0 | 1.117 / 0.977 / 0.956 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| continuous | 1 | 0.953 / 0.800 / 0.769 | 0.853 / 0.819 / 0.804 | 0.888 / 0.909 / 0.863 | 0.868 | slower | slower |
| continuous | 16 | 0.081 / 0.040 / 0.031 | 0.072 / 0.041 / 0.033 | 0.361 / 0.520 / 0.345 | 0.355 | slower | slower |
| continuous | 2 | 0.811 / 0.655 / 0.620 | 0.726 / 0.670 / 0.648 | 0.794 / 0.835 / 0.756 | 0.767 | slower | slower |
| continuous | 4 | 0.585 / 0.439 / 0.404 | 0.524 / 0.449 / 0.422 | 0.650 / 0.725 / 0.602 | 0.622 | slower | slower |
| continuous | 8 | 0.303 / 0.197 / 0.172 | 0.271 / 0.202 / 0.180 | 0.481 / 0.601 / 0.441 | 0.463 | slower | slower |
| jump | 0 | 1.125 / 0.977 / 0.936 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| jump | 1 | 0.950 / 0.781 / 0.727 | 0.844 / 0.800 / 0.776 | 0.886 / 0.900 / 0.838 | 0.860 | slower | slower |
| jump | 16 | 0.067 / 0.027 / 0.016 | 0.060 / 0.028 / 0.017 | 0.386 / 0.514 / 0.316 | 0.381 | slower | slower |
| jump | 2 | 0.799 / 0.625 / 0.564 | 0.710 / 0.640 / 0.602 | 0.790 / 0.820 / 0.716 | 0.757 | slower | slower |
| jump | 4 | 0.563 / 0.400 / 0.340 | 0.500 / 0.410 / 0.363 | 0.648 / 0.705 / 0.550 | 0.614 | slower | slower |
| jump | 8 | 0.278 / 0.164 / 0.123 | 0.247 / 0.168 / 0.131 | 0.489 / 0.584 / 0.392 | 0.468 | slower | slower |

**FREE-N5-PCOMP-weak_favour+weak_favour**

| clock | lag | gap target / N0 / ND | normalised gap target / N0 / ND | hub retention target / N0 / ND | comparison retention target | decay vs ND | decay vs N0 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| continuous | 0 | 0.977 / 0.977 / 0.977 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| continuous | 1 | 0.862 / 0.800 / 0.800 | 0.883 / 0.819 / 0.819 | 0.956 / 0.909 / 0.909 | 0.943 | slower | slower |
| continuous | 16 | 0.377 / 0.040 / 0.040 | 0.386 / 0.041 / 0.041 | 0.738 / 0.520 / 0.520 | 0.722 | slower | slower |
| continuous | 2 | 0.786 / 0.655 / 0.655 | 0.805 / 0.670 / 0.670 | 0.926 / 0.835 / 0.835 | 0.908 | slower | slower |
| continuous | 4 | 0.677 / 0.439 / 0.439 | 0.693 / 0.449 / 0.449 | 0.879 / 0.725 / 0.725 | 0.860 | slower | slower |
| continuous | 8 | 0.536 / 0.197 / 0.197 | 0.549 / 0.202 / 0.202 | 0.816 / 0.601 / 0.601 | 0.796 | slower | slower |
| jump | 0 | 0.747 / 0.977 / 0.977 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| jump | 1 | 0.575 / 0.781 / 0.781 | 0.770 / 0.800 / 0.800 | 0.952 / 0.900 / 0.900 | 0.935 | faster | faster |
| jump | 16 | 0.012 / 0.027 / 0.027 | 0.016 / 0.028 / 0.028 | 0.779 / 0.514 / 0.514 | 0.779 | faster | faster |
| jump | 2 | 0.442 / 0.625 / 0.625 | 0.592 / 0.640 / 0.640 | 0.913 / 0.820 / 0.820 | 0.893 | faster | faster |
| jump | 4 | 0.263 / 0.400 / 0.400 | 0.352 / 0.410 / 0.410 | 0.860 / 0.705 / 0.705 | 0.842 | faster | faster |
| jump | 8 | 0.094 / 0.164 / 0.164 | 0.125 / 0.168 / 0.168 | 0.807 / 0.584 / 0.584 | 0.799 | faster | faster |

**FREE-N6-CLOSEW-weak_favour**

| clock | lag | gap target / N0 / ND | normalised gap target / N0 / ND | hub retention target / N0 / ND | comparison retention target | decay vs ND | decay vs N0 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| continuous | 0 | 0.521 / 1.235 / 0.499 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| continuous | 1 | 0.380 / 1.081 / 0.352 | 0.730 / 0.875 / 0.707 | 0.970 / 0.938 / 0.966 | 0.969 | slower | faster |
| continuous | 16 | 0.018 / 0.146 / 0.002 | 0.035 / 0.118 / 0.004 | 0.888 / 0.559 / 0.883 | 0.889 | slower | faster |
| continuous | 2 | 0.287 / 0.946 / 0.249 | 0.551 / 0.766 / 0.500 | 0.949 / 0.883 / 0.942 | 0.949 | slower | faster |
| continuous | 4 | 0.175 / 0.724 / 0.125 | 0.336 / 0.587 / 0.251 | 0.924 / 0.793 / 0.913 | 0.924 | slower | faster |
| continuous | 8 | 0.075 / 0.425 / 0.032 | 0.144 / 0.344 / 0.063 | 0.902 / 0.672 / 0.891 | 0.902 | slower | faster |
| jump | 0 | 0.601 / 1.235 / 0.794 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| jump | 1 | 0.426 / 1.070 / 0.621 | 0.709 / 0.867 / 0.782 | 0.962 / 0.933 / 0.958 | 0.961 | faster | faster |
| jump | 16 | 0.016 / 0.125 / 0.026 | 0.026 / 0.101 / 0.033 | 0.870 / 0.551 / 0.803 | 0.870 | faster | faster |
| jump | 2 | 0.317 / 0.928 / 0.491 | 0.527 / 0.751 / 0.618 | 0.938 / 0.876 / 0.926 | 0.938 | faster | faster |
| jump | 4 | 0.188 / 0.697 / 0.313 | 0.313 / 0.564 / 0.394 | 0.910 / 0.782 / 0.881 | 0.909 | faster | faster |
| jump | 8 | 0.076 / 0.393 / 0.133 | 0.127 / 0.318 / 0.168 | 0.884 / 0.659 / 0.834 | 0.884 | faster | faster |

**FREE-N6-CSPH-strong_favour+weak_favour**

| clock | lag | gap target / N0 / ND | normalised gap target / N0 / ND | hub retention target / N0 / ND | comparison retention target | decay vs ND | decay vs N0 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| continuous | 0 | 1.477 / 1.235 / 1.185 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| continuous | 1 | 1.341 / 1.081 / 1.015 | 0.908 / 0.875 / 0.856 | 0.928 / 0.938 / 0.896 | 0.906 | slower | slower |
| continuous | 16 | 0.351 / 0.146 / 0.102 | 0.238 / 0.118 / 0.086 | 0.440 / 0.559 / 0.354 | 0.422 | slower | slower |
| continuous | 2 | 1.219 / 0.946 / 0.870 | 0.825 / 0.766 / 0.734 | 0.865 / 0.883 / 0.808 | 0.833 | slower | slower |
| continuous | 4 | 1.010 / 0.724 / 0.639 | 0.684 / 0.587 / 0.540 | 0.758 / 0.793 / 0.671 | 0.721 | slower | slower |
| continuous | 8 | 0.703 / 0.425 / 0.347 | 0.476 / 0.344 / 0.293 | 0.605 / 0.672 / 0.498 | 0.574 | slower | slower |
| jump | 0 | 1.608 / 1.235 / 1.167 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| jump | 1 | 1.467 / 1.070 / 0.982 | 0.912 / 0.867 / 0.842 | 0.933 / 0.933 / 0.883 | 0.902 | slower | slower |
| jump | 16 | 0.427 / 0.125 / 0.073 | 0.266 / 0.101 / 0.063 | 0.482 / 0.551 / 0.325 | 0.449 | slower | slower |
| jump | 2 | 1.343 / 0.928 / 0.826 | 0.835 / 0.751 / 0.708 | 0.874 / 0.876 / 0.786 | 0.828 | slower | slower |
| jump | 4 | 1.130 / 0.697 / 0.585 | 0.703 / 0.564 / 0.501 | 0.774 / 0.782 / 0.636 | 0.718 | slower | slower |
| jump | 8 | 0.811 / 0.393 / 0.293 | 0.505 / 0.318 / 0.251 | 0.633 / 0.659 / 0.458 | 0.581 | slower | slower |

**FREE-N6-NULL-none**

| clock | lag | gap target / N0 / ND | normalised gap target / N0 / ND | hub retention target / N0 / ND | comparison retention target | decay vs ND | decay vs N0 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| continuous | 0 | 1.235 / 1.235 / 1.235 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| continuous | 1 | 1.081 / 1.081 / 1.081 | 0.875 / 0.875 / 0.875 | 0.938 / 0.938 / 0.938 | 0.938 | tie | tie |
| continuous | 16 | 0.146 / 0.146 / 0.146 | 0.118 / 0.118 / 0.118 | 0.559 / 0.559 / 0.559 | 0.559 | tie | tie |
| continuous | 2 | 0.946 / 0.946 / 0.946 | 0.766 / 0.766 / 0.766 | 0.883 / 0.883 / 0.883 | 0.883 | tie | tie |
| continuous | 4 | 0.724 / 0.724 / 0.724 | 0.587 / 0.587 / 0.587 | 0.793 / 0.793 / 0.793 | 0.793 | tie | tie |
| continuous | 8 | 0.425 / 0.425 / 0.425 | 0.344 / 0.344 / 0.344 | 0.672 / 0.672 / 0.672 | 0.672 | tie | tie |
| jump | 0 | 1.235 / 1.235 / 1.235 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| jump | 1 | 1.070 / 1.070 / 1.070 | 0.867 / 0.867 / 0.867 | 0.933 / 0.933 / 0.933 | 0.933 | tie | tie |
| jump | 16 | 0.125 / 0.125 / 0.125 | 0.101 / 0.101 / 0.101 | 0.551 / 0.551 / 0.551 | 0.551 | tie | tie |
| jump | 2 | 0.928 / 0.928 / 0.928 | 0.751 / 0.751 / 0.751 | 0.876 / 0.876 / 0.876 | 0.876 | tie | tie |
| jump | 4 | 0.697 / 0.697 / 0.697 | 0.564 / 0.564 / 0.564 | 0.782 / 0.782 / 0.782 | 0.782 | tie | tie |
| jump | 8 | 0.393 / 0.393 / 0.393 | 0.318 / 0.318 / 0.318 | 0.659 / 0.659 / 0.659 | 0.659 | tie | tie |

**FREE-N6-PATHF-weak_suppress**

| clock | lag | gap target / N0 / ND | normalised gap target / N0 / ND | hub retention target / N0 / ND | comparison retention target | decay vs ND | decay vs N0 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| continuous | 0 | 1.321 / 1.235 / 1.167 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| continuous | 1 | 1.166 / 1.081 / 0.994 | 0.883 / 0.875 / 0.852 | 0.891 / 0.938 / 0.890 | 0.891 | slower | slower |
| continuous | 16 | 0.158 / 0.146 / 0.093 | 0.120 / 0.118 / 0.079 | 0.343 / 0.559 / 0.335 | 0.340 | slower | slower |
| continuous | 2 | 1.027 / 0.946 / 0.847 | 0.778 / 0.766 / 0.726 | 0.801 / 0.883 / 0.799 | 0.800 | slower | slower |
| continuous | 4 | 0.793 / 0.724 / 0.617 | 0.600 / 0.587 / 0.528 | 0.662 / 0.793 / 0.655 | 0.659 | slower | slower |
| continuous | 8 | 0.467 / 0.425 / 0.328 | 0.354 / 0.344 / 0.281 | 0.488 / 0.672 / 0.478 | 0.484 | slower | slower |
| jump | 0 | 1.235 / 1.235 / 1.147 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| jump | 1 | 1.072 / 1.070 / 0.958 | 0.868 / 0.867 / 0.836 | 0.873 / 0.933 / 0.876 | 0.874 | slower | slower |
| jump | 16 | 0.097 / 0.125 / 0.064 | 0.078 / 0.101 / 0.056 | 0.309 / 0.551 / 0.305 | 0.308 | slower | faster |
| jump | 2 | 0.925 / 0.928 / 0.801 | 0.749 / 0.751 / 0.698 | 0.771 / 0.876 / 0.773 | 0.772 | slower | faster |
| jump | 4 | 0.679 / 0.697 / 0.559 | 0.550 / 0.564 / 0.487 | 0.618 / 0.782 / 0.618 | 0.619 | slower | faster |
| jump | 8 | 0.358 / 0.393 / 0.272 | 0.290 / 0.318 / 0.237 | 0.441 / 0.659 / 0.436 | 0.439 | slower | faster |

**FREE-N6-PATHH-weak_favour**

| clock | lag | gap target / N0 / ND | normalised gap target / N0 / ND | hub retention target / N0 / ND | comparison retention target | decay vs ND | decay vs N0 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| continuous | 0 | 1.371 / 1.235 / 1.155 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| continuous | 1 | 1.227 / 1.081 / 0.980 | 0.895 / 0.875 / 0.848 | 0.912 / 0.938 / 0.886 | 0.891 | slower | slower |
| continuous | 16 | 0.220 / 0.146 / 0.086 | 0.160 / 0.118 / 0.075 | 0.360 / 0.559 / 0.322 | 0.346 | slower | slower |
| continuous | 2 | 1.097 / 0.946 / 0.832 | 0.800 / 0.766 / 0.720 | 0.833 / 0.883 / 0.792 | 0.804 | slower | slower |
| continuous | 4 | 0.874 / 0.724 / 0.601 | 0.638 / 0.587 / 0.521 | 0.704 / 0.793 / 0.645 | 0.669 | slower | slower |
| continuous | 8 | 0.552 / 0.425 / 0.315 | 0.403 / 0.344 / 0.272 | 0.527 / 0.672 / 0.464 | 0.497 | slower | slower |
| jump | 0 | 1.400 / 1.235 / 1.132 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| jump | 1 | 1.250 / 1.070 / 0.941 | 0.893 / 0.867 / 0.831 | 0.912 / 0.933 / 0.871 | 0.887 | slower | slower |
| jump | 16 | 0.212 / 0.125 / 0.058 | 0.151 / 0.101 / 0.051 | 0.374 / 0.551 / 0.291 | 0.358 | slower | slower |
| jump | 2 | 1.114 / 0.928 / 0.782 | 0.796 / 0.751 / 0.691 | 0.833 / 0.876 / 0.764 | 0.797 | slower | slower |
| jump | 4 | 0.880 / 0.697 / 0.540 | 0.629 / 0.564 / 0.477 | 0.703 / 0.782 / 0.604 | 0.660 | slower | slower |
| jump | 8 | 0.547 / 0.393 / 0.257 | 0.391 / 0.318 / 0.227 | 0.530 / 0.659 / 0.420 | 0.494 | slower | slower |

**FREE-N6-PCOMP-weak_favour+weak_favour**

| clock | lag | gap target / N0 / ND | normalised gap target / N0 / ND | hub retention target / N0 / ND | comparison retention target | decay vs ND | decay vs N0 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| continuous | 0 | 1.235 / 1.235 / 1.235 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| continuous | 1 | 1.181 / 1.081 / 1.081 | 0.956 / 0.875 / 0.875 | 0.984 / 0.938 / 0.938 | 0.979 | slower | slower |
| continuous | 16 | 0.964 / 0.146 / 0.146 | 0.781 / 0.118 / 0.118 | 0.912 / 0.559 / 0.559 | 0.899 | slower | slower |
| continuous | 2 | 1.150 / 0.946 / 0.946 | 0.931 / 0.766 / 0.766 | 0.974 / 0.883 / 0.883 | 0.968 | slower | slower |
| continuous | 4 | 1.105 / 0.724 / 0.724 | 0.895 / 0.587 / 0.587 | 0.960 / 0.793 / 0.793 | 0.952 | slower | slower |
| continuous | 8 | 1.044 / 0.425 / 0.425 | 0.846 / 0.344 / 0.344 | 0.939 / 0.672 / 0.672 | 0.929 | slower | slower |
| jump | 0 | 0.668 / 1.235 / 1.235 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 1.000 | — | — |
| jump | 1 | 0.517 / 1.070 / 1.070 | 0.774 / 0.867 / 0.867 | 0.969 / 0.933 / 0.933 | 0.961 | faster | faster |
| jump | 16 | 0.015 / 0.125 / 0.125 | 0.023 / 0.101 / 0.101 | 0.860 / 0.551 / 0.551 | 0.859 | faster | faster |
| jump | 2 | 0.403 / 0.928 / 0.928 | 0.603 / 0.751 / 0.751 | 0.945 / 0.876 / 0.876 | 0.935 | faster | faster |
| jump | 4 | 0.247 / 0.697 / 0.697 | 0.370 / 0.564 / 0.564 | 0.911 / 0.782 / 0.782 | 0.902 | faster | faster |
| jump | 8 | 0.096 / 0.393 / 0.393 | 0.143 / 0.318 / 0.318 | 0.878 / 0.659 / 0.659 | 0.873 | faster | faster |

## Secondary: residual life and entrance first passage

Occupation-sampled residual life is a different quantity from the entrance mean life L (Palm: R_ct = E[L²]/(2E[L]) ≥ L/2).

| Item | law | Predicate | resolved | entrance mean ct / L_ct | entrance mean jump / L_jump | residual ct | residual jump |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FREE-N5-CLOSEW-weak_favour | target | F_2PATH | yes | 1.000000000 | 1.000000000 | 3.348 | 51.18 |
| FREE-N5-CLOSEW-weak_favour | target | F_STAR | yes | 1.000000000 | 1.000000000 | 0.900 | 13.49 |
| FREE-N5-CLOSEW-weak_favour | target | F_TRI | yes | 1.000000000 | 1.000000000 | 0.711 | 10.63 |
| FREE-N5-CLOSEW-weak_favour | target | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.500 | 7.49 |
| FREE-N5-CLOSEW-weak_favour | target | I_STAR | yes | 1.000000000 | 1.000000000 | 0.333 | 4.89 |
| FREE-N5-CLOSEW-weak_favour | target | I_TRI | yes | 1.000000000 | 1.000000000 | 0.333 | 4.86 |
| FREE-N5-CLOSEW-weak_favour | nd | F_2PATH | yes | 1.000000000 | 1.000000000 | 2.251 | 26.31 |
| FREE-N5-CLOSEW-weak_favour | nd | F_STAR | yes | 1.000000000 | 1.000000000 | 0.918 | 8.78 |
| FREE-N5-CLOSEW-weak_favour | nd | F_TRI | yes | 1.000000000 | 1.000000000 | 0.810 | 7.80 |
| FREE-N5-CLOSEW-weak_favour | nd | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.653 | 6.63 |
| FREE-N5-CLOSEW-weak_favour | nd | I_STAR | yes | 1.000000000 | 1.000000000 | 0.498 | 4.41 |
| FREE-N5-CLOSEW-weak_favour | nd | I_TRI | yes | 1.000000000 | 1.000000000 | 0.498 | 4.41 |
| FREE-N5-CSPH-strong_favour+weak_favour | target | F_2PATH | yes | 1.000000000 | 1.000000000 | 0.322 | 9.38 |
| FREE-N5-CSPH-strong_favour+weak_favour | target | F_STAR | yes | 1.000000000 | 1.000000000 | 0.122 | 4.49 |
| FREE-N5-CSPH-strong_favour+weak_favour | target | F_TRI | yes | 1.000000000 | 1.000000000 | 0.136 | 3.99 |
| FREE-N5-CSPH-strong_favour+weak_favour | target | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.169 | 5.14 |
| FREE-N5-CSPH-strong_favour+weak_favour | target | I_STAR | yes | 1.000000000 | 1.000000000 | 0.104 | 4.13 |
| FREE-N5-CSPH-strong_favour+weak_favour | target | I_TRI | yes | 1.000000000 | 1.000000000 | 0.112 | 3.04 |
| FREE-N5-CSPH-strong_favour+weak_favour | nd | F_2PATH | yes | 1.000000000 | 1.000000000 | 0.213 | 5.37 |
| FREE-N5-CSPH-strong_favour+weak_favour | nd | F_STAR | yes | 1.000000000 | 1.000000000 | 0.104 | 2.53 |
| FREE-N5-CSPH-strong_favour+weak_favour | nd | F_TRI | yes | 1.000000000 | 1.000000000 | 0.095 | 2.31 |
| FREE-N5-CSPH-strong_favour+weak_favour | nd | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.137 | 3.43 |
| FREE-N5-CSPH-strong_favour+weak_favour | nd | I_STAR | yes | 1.000000000 | 1.000000000 | 0.090 | 2.20 |
| FREE-N5-CSPH-strong_favour+weak_favour | nd | I_TRI | yes | 1.000000000 | 1.000000000 | 0.090 | 2.20 |
| FREE-N5-NULL-none | target | F_2PATH | yes | 1.000000000 | 1.000000000 | 1.129 | 11.29 |
| FREE-N5-NULL-none | target | F_STAR | yes | 1.000000000 | 1.000000000 | 0.467 | 4.67 |
| FREE-N5-NULL-none | target | F_TRI | yes | 1.000000000 | 1.000000000 | 0.430 | 4.30 |
| FREE-N5-NULL-none | target | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.500 | 5.00 |
| FREE-N5-NULL-none | target | I_STAR | yes | 1.000000000 | 1.000000000 | 0.333 | 3.33 |
| FREE-N5-NULL-none | target | I_TRI | yes | 1.000000000 | 1.000000000 | 0.333 | 3.33 |
| FREE-N5-NULL-none | nd | F_2PATH | yes | 1.000000000 | 1.000000000 | 1.129 | 11.29 |
| FREE-N5-NULL-none | nd | F_STAR | yes | 1.000000000 | 1.000000000 | 0.467 | 4.67 |
| FREE-N5-NULL-none | nd | F_TRI | yes | 1.000000000 | 1.000000000 | 0.430 | 4.30 |
| FREE-N5-NULL-none | nd | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.500 | 5.00 |
| FREE-N5-NULL-none | nd | I_STAR | yes | 1.000000000 | 1.000000000 | 0.333 | 3.33 |
| FREE-N5-NULL-none | nd | I_TRI | yes | 1.000000000 | 1.000000000 | 0.333 | 3.33 |
| FREE-N5-PATHF-weak_suppress | target | F_2PATH | yes | 1.000000000 | 1.000000000 | 0.783 | 4.70 |
| FREE-N5-PATHF-weak_suppress | target | F_STAR | yes | 1.000000000 | 1.000000000 | 0.414 | 2.21 |
| FREE-N5-PATHF-weak_suppress | target | F_TRI | yes | 1.000000000 | 1.000000000 | 0.338 | 1.80 |
| FREE-N5-PATHF-weak_suppress | target | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.500 | 2.93 |
| FREE-N5-PATHF-weak_suppress | target | I_STAR | yes | 1.000000000 | 1.000000000 | 0.333 | 1.76 |
| FREE-N5-PATHF-weak_suppress | target | I_TRI | yes | 1.000000000 | 1.000000000 | 0.333 | 1.78 |
| FREE-N5-PATHF-weak_suppress | nd | F_2PATH | yes | 1.000000000 | 1.000000000 | 0.706 | 4.29 |
| FREE-N5-PATHF-weak_suppress | nd | F_STAR | yes | 1.000000000 | 1.000000000 | 0.368 | 2.13 |
| FREE-N5-PATHF-weak_suppress | nd | F_TRI | yes | 1.000000000 | 1.000000000 | 0.342 | 1.97 |
| FREE-N5-PATHF-weak_suppress | nd | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.500 | 3.00 |
| FREE-N5-PATHF-weak_suppress | nd | I_STAR | yes | 1.000000000 | 1.000000000 | 0.333 | 1.92 |
| FREE-N5-PATHF-weak_suppress | nd | I_TRI | yes | 1.000000000 | 1.000000000 | 0.333 | 1.92 |
| FREE-N5-PATHH-weak_favour | target | F_2PATH | yes | 1.000000000 | 1.000000000 | 0.414 | 6.01 |
| FREE-N5-PATHH-weak_favour | target | F_STAR | yes | 1.000000000 | 1.000000000 | 0.228 | 3.53 |
| FREE-N5-PATHH-weak_favour | target | F_TRI | yes | 1.000000000 | 1.000000000 | 0.168 | 2.79 |
| FREE-N5-PATHH-weak_favour | target | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.268 | 4.00 |
| FREE-N5-PATHH-weak_favour | target | I_STAR | yes | 1.000000000 | 1.000000000 | 0.194 | 3.09 |
| FREE-N5-PATHH-weak_favour | target | I_TRI | yes | 1.000000000 | 1.000000000 | 0.161 | 2.63 |
| FREE-N5-PATHH-weak_favour | nd | F_2PATH | yes | 1.000000000 | 1.000000000 | 0.330 | 4.06 |
| FREE-N5-PATHH-weak_favour | nd | F_STAR | yes | 1.000000000 | 1.000000000 | 0.174 | 2.02 |
| FREE-N5-PATHH-weak_favour | nd | F_TRI | yes | 1.000000000 | 1.000000000 | 0.162 | 1.88 |
| FREE-N5-PATHH-weak_favour | nd | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.239 | 2.89 |
| FREE-N5-PATHH-weak_favour | nd | I_STAR | yes | 1.000000000 | 1.000000000 | 0.159 | 1.84 |
| FREE-N5-PATHH-weak_favour | nd | I_TRI | yes | 1.000000000 | 1.000000000 | 0.159 | 1.84 |
| FREE-N5-PCOMP-weak_favour+weak_favour | target | F_2PATH | yes | 1.000000000 | 1.000000000 | 0.096 | 49.66 |
| FREE-N5-PCOMP-weak_favour+weak_favour | target | F_STAR | yes | 1.000000000 | 1.000000000 | 0.024 | 12.28 |
| FREE-N5-PCOMP-weak_favour+weak_favour | target | F_TRI | yes | 1.000000000 | 1.000000000 | 0.024 | 12.84 |
| FREE-N5-PCOMP-weak_favour+weak_favour | target | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.033 | 8.37 |
| FREE-N5-PCOMP-weak_favour+weak_favour | target | I_STAR | yes | 1.000000000 | 1.000000000 | 0.015 | 5.81 |
| FREE-N5-PCOMP-weak_favour+weak_favour | target | I_TRI | yes | 1.000000000 | 1.000000000 | 0.015 | 5.68 |
| FREE-N5-PCOMP-weak_favour+weak_favour | nd | F_2PATH | yes | 1.000000000 | 1.000000000 | 0.025 | 11.29 |
| FREE-N5-PCOMP-weak_favour+weak_favour | nd | F_STAR | yes | 1.000000000 | 1.000000000 | 0.011 | 4.67 |
| FREE-N5-PCOMP-weak_favour+weak_favour | nd | F_TRI | yes | 1.000000000 | 1.000000000 | 0.010 | 4.30 |
| FREE-N5-PCOMP-weak_favour+weak_favour | nd | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.011 | 5.00 |
| FREE-N5-PCOMP-weak_favour+weak_favour | nd | I_STAR | yes | 1.000000000 | 1.000000000 | 0.008 | 3.33 |
| FREE-N5-PCOMP-weak_favour+weak_favour | nd | I_TRI | yes | 1.000000000 | 1.000000000 | 0.008 | 3.33 |
| FREE-N6-CLOSEW-weak_favour | target | F_2PATH | yes | 1.000000000 | 1.000000000 | 21.441 | 567.17 |
| FREE-N6-CLOSEW-weak_favour | target | F_STAR | yes | 1.000000000 | 1.000000000 | 4.442 | 116.30 |
| FREE-N6-CLOSEW-weak_favour | target | F_TRI | yes | 1.000000000 | 1.000000000 | 0.937 | 24.39 |
| FREE-N6-CLOSEW-weak_favour | target | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.500 | 12.86 |
| FREE-N6-CLOSEW-weak_favour | target | I_STAR | yes | 1.000000000 | 1.000000000 | 0.333 | 8.40 |
| FREE-N6-CLOSEW-weak_favour | target | I_TRI | yes | 1.000000000 | 1.000000000 | 0.333 | 8.39 |
| FREE-N6-CLOSEW-weak_favour | nd | F_2PATH | yes | 1.000000000 | 1.000000000 | 8.958 | 216.53 |
| FREE-N6-CLOSEW-weak_favour | nd | F_STAR | yes | 1.000000000 | 1.000000000 | 2.527 | 53.53 |
| FREE-N6-CLOSEW-weak_favour | nd | F_TRI | yes | 1.000000000 | 1.000000000 | 0.972 | 19.90 |
| FREE-N6-CLOSEW-weak_favour | nd | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.599 | 11.85 |
| FREE-N6-CLOSEW-weak_favour | nd | I_STAR | yes | 1.000000000 | 1.000000000 | 0.434 | 7.81 |
| FREE-N6-CLOSEW-weak_favour | nd | I_TRI | yes | 1.000000000 | 1.000000000 | 0.434 | 7.81 |
| FREE-N6-CSPH-strong_favour+weak_favour | target | F_2PATH | yes | 1.000000000 | 1.000000000 | 0.269 | 11.57 |
| FREE-N6-CSPH-strong_favour+weak_favour | target | F_STAR | yes | 1.000000000 | 1.000000000 | 0.126 | 6.58 |
| FREE-N6-CSPH-strong_favour+weak_favour | target | F_TRI | yes | 1.000000000 | 1.000000000 | 0.103 | 4.29 |
| FREE-N6-CSPH-strong_favour+weak_favour | target | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.137 | 6.58 |
| FREE-N6-CSPH-strong_favour+weak_favour | target | I_STAR | yes | 1.000000000 | 1.000000000 | 0.100 | 6.07 |
| FREE-N6-CSPH-strong_favour+weak_favour | target | I_TRI | yes | 1.000000000 | 1.000000000 | 0.085 | 3.37 |
| FREE-N6-CSPH-strong_favour+weak_favour | nd | F_2PATH | yes | 1.000000000 | 1.000000000 | 0.171 | 6.73 |
| FREE-N6-CSPH-strong_favour+weak_favour | nd | F_STAR | yes | 1.000000000 | 1.000000000 | 0.086 | 3.23 |
| FREE-N6-CSPH-strong_favour+weak_favour | nd | F_TRI | yes | 1.000000000 | 1.000000000 | 0.073 | 2.71 |
| FREE-N6-CSPH-strong_favour+weak_favour | nd | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.105 | 4.05 |
| FREE-N6-CSPH-strong_favour+weak_favour | nd | I_STAR | yes | 1.000000000 | 1.000000000 | 0.070 | 2.59 |
| FREE-N6-CSPH-strong_favour+weak_favour | nd | I_TRI | yes | 1.000000000 | 1.000000000 | 0.070 | 2.59 |
| FREE-N6-NULL-none | target | F_2PATH | yes | 1.000000000 | 1.000000000 | 1.705 | 25.58 |
| FREE-N6-NULL-none | target | F_STAR | yes | 1.000000000 | 1.000000000 | 0.658 | 9.88 |
| FREE-N6-NULL-none | target | F_TRI | yes | 1.000000000 | 1.000000000 | 0.480 | 7.20 |
| FREE-N6-NULL-none | target | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.500 | 7.50 |
| FREE-N6-NULL-none | target | I_STAR | yes | 1.000000000 | 1.000000000 | 0.333 | 5.00 |
| FREE-N6-NULL-none | target | I_TRI | yes | 1.000000000 | 1.000000000 | 0.333 | 5.00 |
| FREE-N6-NULL-none | nd | F_2PATH | yes | 1.000000000 | 1.000000000 | 1.705 | 25.58 |
| FREE-N6-NULL-none | nd | F_STAR | yes | 1.000000000 | 1.000000000 | 0.658 | 9.88 |
| FREE-N6-NULL-none | nd | F_TRI | yes | 1.000000000 | 1.000000000 | 0.480 | 7.20 |
| FREE-N6-NULL-none | nd | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.500 | 7.50 |
| FREE-N6-NULL-none | nd | I_STAR | yes | 1.000000000 | 1.000000000 | 0.333 | 5.00 |
| FREE-N6-NULL-none | nd | I_TRI | yes | 1.000000000 | 1.000000000 | 0.333 | 5.00 |
| FREE-N6-PATHF-weak_suppress | target | F_2PATH | yes | 1.000000000 | 1.000000000 | 0.851 | 6.54 |
| FREE-N6-PATHF-weak_suppress | target | F_STAR | yes | 1.000000000 | 1.000000000 | 0.478 | 3.27 |
| FREE-N6-PATHF-weak_suppress | target | F_TRI | yes | 1.000000000 | 1.000000000 | 0.339 | 2.33 |
| FREE-N6-PATHF-weak_suppress | target | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.500 | 3.71 |
| FREE-N6-PATHF-weak_suppress | target | I_STAR | yes | 1.000000000 | 1.000000000 | 0.333 | 2.22 |
| FREE-N6-PATHF-weak_suppress | target | I_TRI | yes | 1.000000000 | 1.000000000 | 0.333 | 2.29 |
| FREE-N6-PATHF-weak_suppress | nd | F_2PATH | yes | 1.000000000 | 1.000000000 | 0.779 | 6.04 |
| FREE-N6-PATHF-weak_suppress | nd | F_STAR | yes | 1.000000000 | 1.000000000 | 0.401 | 2.94 |
| FREE-N6-PATHF-weak_suppress | nd | F_TRI | yes | 1.000000000 | 1.000000000 | 0.345 | 2.51 |
| FREE-N6-PATHF-weak_suppress | nd | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.500 | 3.80 |
| FREE-N6-PATHF-weak_suppress | nd | I_STAR | yes | 1.000000000 | 1.000000000 | 0.333 | 2.42 |
| FREE-N6-PATHF-weak_suppress | nd | I_TRI | yes | 1.000000000 | 1.000000000 | 0.333 | 2.42 |
| FREE-N6-PATHH-weak_favour | target | F_2PATH | yes | 1.000000000 | 1.000000000 | 0.354 | 8.08 |
| FREE-N6-PATHH-weak_favour | target | F_STAR | yes | 1.000000000 | 1.000000000 | 0.218 | 5.16 |
| FREE-N6-PATHH-weak_favour | target | F_TRI | yes | 1.000000000 | 1.000000000 | 0.131 | 3.30 |
| FREE-N6-PATHH-weak_favour | target | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.217 | 5.11 |
| FREE-N6-PATHH-weak_favour | target | I_STAR | yes | 1.000000000 | 1.000000000 | 0.173 | 4.24 |
| FREE-N6-PATHH-weak_favour | target | I_TRI | yes | 1.000000000 | 1.000000000 | 0.125 | 3.12 |
| FREE-N6-PATHH-weak_favour | nd | F_2PATH | yes | 1.000000000 | 1.000000000 | 0.276 | 5.59 |
| FREE-N6-PATHH-weak_favour | nd | F_STAR | yes | 1.000000000 | 1.000000000 | 0.144 | 2.75 |
| FREE-N6-PATHH-weak_favour | nd | F_TRI | yes | 1.000000000 | 1.000000000 | 0.125 | 2.37 |
| FREE-N6-PATHH-weak_favour | nd | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.183 | 3.63 |
| FREE-N6-PATHH-weak_favour | nd | I_STAR | yes | 1.000000000 | 1.000000000 | 0.122 | 2.31 |
| FREE-N6-PATHH-weak_favour | nd | I_TRI | yes | 1.000000000 | 1.000000000 | 0.122 | 2.31 |
| FREE-N6-PCOMP-weak_favour+weak_favour | target | F_2PATH | yes | 1.000000000 | 1.000000000 | 0.016 | 700.48 |
| FREE-N6-PCOMP-weak_favour+weak_favour | target | F_STAR | yes | 1.000000000 | 1.000000000 | 0.004 | 85.43 |
| FREE-N6-PCOMP-weak_favour+weak_favour | target | F_TRI | yes | 1.000000000 | 1.000000000 | 0.003 | 25.19 |
| FREE-N6-PCOMP-weak_favour+weak_favour | target | I_2PATH | yes | 1.000000000 | 1.000000000 | 0.005 | 13.23 |
| FREE-N6-PCOMP-weak_favour+weak_favour | target | I_STAR | yes | 1.000000000 | 1.000000000 | 0.002 | 8.94 |
| FREE-N6-PCOMP-weak_favour+weak_favour | target | I_TRI | yes | 1.000000000 | 1.000000000 | 0.002 | 8.87 |
| FREE-N6-PCOMP-weak_favour+weak_favour | nd | F_2PATH | yes | 1.000000000 | 1.000000000 | 3.70e-04 | 25.58 |
| FREE-N6-PCOMP-weak_favour+weak_favour | nd | F_STAR | yes | 1.000000000 | 1.000000000 | 1.43e-04 | 9.87 |
| FREE-N6-PCOMP-weak_favour+weak_favour | nd | F_TRI | yes | 1.000000000 | 1.000000000 | 1.04e-04 | 7.20 |
| FREE-N6-PCOMP-weak_favour+weak_favour | nd | I_2PATH | yes | 1.000000000 | 1.000000000 | 1.08e-04 | 7.50 |
| FREE-N6-PCOMP-weak_favour+weak_favour | nd | I_STAR | yes | 1.000000000 | 1.000000000 | 7.23e-05 | 5.00 |
| FREE-N6-PCOMP-weak_favour+weak_favour | nd | I_TRI | yes | 1.000000000 | 1.000000000 | 7.23e-05 | 5.00 |

## Replication of published E0B laws

| Item | holds | max |Δct| | max |Δjump| | mean-rate gap |
| --- | --- | --- | --- | --- |
| FREE-N5-CLOSEW-weak_favour | True | 2.22e-15 | 2.39e-15 | 5.33e-15 |
| FREE-N5-CSPH-strong_favour+weak_favour | True | 8.74e-16 | 1.33e-15 | 7.11e-14 |
| FREE-N5-NULL-none | True | 1.92e-15 | 1.93e-15 | 1.78e-15 |
| FREE-N5-PATHF-weak_suppress | True | 4.86e-16 | 5.00e-16 | 1.78e-15 |
| FREE-N5-PATHH-weak_favour | True | 5.76e-16 | 4.65e-16 | 1.07e-14 |
| FREE-N5-PCOMP-weak_favour+weak_favour | True | 1.01e-14 | 3.30e-15 | 1.97e-11 |
| FREE-N6-CLOSEW-weak_favour | True | 1.67e-16 | 1.11e-16 | 7.11e-15 |
| FREE-N6-CSPH-strong_favour+weak_favour | True | 8.33e-17 | 6.94e-18 | 7.11e-15 |
| FREE-N6-NULL-none | True | 0.000 | 0.000 | 0.000 |
| FREE-N6-PATHF-weak_suppress | True | 5.27e-16 | 6.94e-17 | 1.78e-15 |
| FREE-N6-PATHH-weak_favour | True | 1.25e-16 | 4.16e-17 | 0.000 |
| FREE-N6-PCOMP-weak_favour+weak_favour | True | 1.63e-15 | 6.66e-16 | 5.03e-09 |
