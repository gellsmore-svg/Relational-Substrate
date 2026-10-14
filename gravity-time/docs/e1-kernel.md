# E1 machinery — vectorised label-covariant template kernel

Step 1 of the E1 recommendation (`docs/roadmap.md`). This is engineering, not a scientific round. No E1 cell has been run, and no E1 plan has been frozen yet.

**Module:** `constraint-lab/src/rs_constraint_lab/gtkernel.py`, version `gt-vectorised-kernel/v1`.
**Tests:** `constraint-lab/tests/test_gtkernel.py`.

## Method

GT templates are label-covariant and multiply once per satisfying witness. So a toggle's weight depends only on witness counts, which are computed for all states at once with bit arithmetic:

| Component | Witness count for pair ab |
| --- | --- |
| closure (form or dissolve) | #{c : x_ac ∧ x_bc} |
| adjacency (form) | #{c : x_ac} + #{c : x_bc} |
| path (form or dissolve) | Σ over end ∈ {a, b} of #{(c, d) : x_end,c ∧ x_c,d}, with c, d ∉ {a, b} and c ≠ d |

- A form component contributes f^w when the relation is absent. A dissolve component contributes g^w when it is present. `prohibit` contributes 0 if w > 0 and 1 otherwise.
- The HELD scaffold zeroes the dissolve weight of the three source relations.
- Rates are computed on the candidate space: all states in FREE, all states containing the source triangle in HELD. The reachable class from the declared start is then found by array breadth-first search.
- The stationary law follows the G0/E0 convention: the jump-chain law by lazy power iteration, then π_ct = π_jump / R. It uses index arrays, with no dense matrix.

## Validation

- **Exact equivalence with `build_kernel`.** Reachable states, transition targets and the full weight array were compared bit for bit, with tolerance 0. W4 weights are powers of two and exact in float64.

  | N | Cells | Mismatches |
  | --- | --- | --- |
  | 4 | 36 | 0 |
  | 5 | 36 | 0 |
  | 6 | 36 | 0 (319 s, run once, not in CI) |

  Each N covers all 18 E0A/E0B family-grades in both modes. N=4 and N=5 run in CI. N=6 was run once; its log is `provenance/e1-kernel-n6-validation.log`.
- **Sparse against dense stationary law.** On published E0 cells (CLOSE, PATHF weak_suppress, CSPH and EXCL, HELD N5 and N6), the maximum |Δπ_ct| is at most 4.3e-15 and the residual at most 2.0e-15.

## Scale (timing on theorem-fixed cells only)

| Cell | States | Build + reach | Stationary solve | Check |
| --- | --- | --- | --- | --- |
| HELD N7 NULL, non-uniform start | 262,144 | 0.5 s | 10.9 s (448 iterations) | max \|π − uniform\| 2.5e-19 |
| FREE N7 NULL, non-uniform start | 2,097,152 | 10.9 s | 148.5 s (497 iterations) | 4.8e-20 |
| HELD N7 PATHF weak_suppress | 262,144 | 0.7 s, **build only** | not computed | — |

Peak memory was 2.6 GB.

**Pre-freeze exposure for the E1 plan:** the HELD N7 PATHF weak_suppress chain was built for timing. Its reachable class has 262,144 states. No stationary law or observable was computed.

## What the E1 round still needs before it can be frozen

Several E0 observables use dense algebra or brute-force symmetry and do not scale to N=7. Each needs a scalable replacement, or must be declared as omitted at N=7:

- **Spectrum and autocorrelation.** Dense up to 4,096 states. At N=7, omit them, or use a declared sparse estimate (power iteration for the gap; iterative solves for τ).
- **Class tables.** HELD N7 has 144 permutations, which is feasible. FREE N7 has 5,040 permutations over 2M states, which needs the canonical labels computed in chunks.
- **G0 held observables and shell activity.** Per-state Python breadth-first search over 262,144 states × 4 probes is slow. These need a vectorised distance-to-source.
- **Event-order patterns.** These are already array-based, at slots² passes over the class. They are feasible for HELD N7 (18² × 262k); FREE N7 should be timed.

**Status (GT-P003).** Each item above now has a scalable replacement or a declared omission. The spectrum is omitted; autocorrelation is iterative; class tables use lookup tables; distances are vectorised; event order was timed at FREE N7 (17 s). See `docs/e1-observables.md`. The E1 plan is still not frozen.
