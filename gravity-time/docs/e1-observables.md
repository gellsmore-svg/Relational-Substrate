# E1 observables: scalable implementation and validation matrix

Prompt GT-P003, deliverables 1 and 2. This is engineering, not a scientific round. No E1 plan is frozen, and no N=7 scientific cell has been computed.

| Module | Role |
| --- | --- |
| `constraint-lab/src/rs_constraint_lab/gtobs.py` (`gt-e1-observables/v1`) | Every E0A/E0B channel, from a `gtkernel` chain, in array form, plus labelled additions |
| `gtobs_validate.py` | Opt-in reproduction of all 84 published E0 cells, with independent referees |
| `gtobs_fixtures.py` | N=7 cost fixtures on theorem-fixed cells only |
| `gtscale.py` | Law-free scale census and NULL baselines (`docs/e1-scale-confound-audit.md`) |
| `gtkernel.py` | Unchanged except an optional `factors` argument (alphabet), with W4 as the default |
| `constraint-lab/tests/test_gtobs.py` | 86 tests: equivalence, edge cases, identities, referees |

## 1. Why a faster kernel was not enough

E0's analysis (`gte0a.analyse_item`) rebuilt the kernel through `build_kernel`, found the recurrent classes by Python graph search, ran a breadth-first search per (state, probe) for distance to the source, looked states up in dictionaries, and used dense matrices for the spectrum and autocorrelation. Each of these is impractical at N=7 (262,144 HELD and 2,097,152 FREE states). `gtobs` keeps every definition and replaces only the computation.

## 2. Validation matrix

Status key:
- **S** — already scalable; E0 code reused unchanged.
- **R** — rewritten in array form, same definition, reproduced to tolerance.
- **I** — iterative method with declared tolerance and convergence diagnostics, checked against dense or exact references.
- **O** — omitted at N=7.
- **A** — addition (new channel, not published in E0).

Reproduction tolerance against the committed tables is |Δ| ≤ 1e-10 absolute or ≤ 1e-8 relative.

| Channel | What it measures | Clock | Status | Exact equivalence argument / check | Available N |
| --- | --- | --- | --- | --- | --- |
| Regime (`recurrent` / `absorbing` / `mixed`) | Whether the reachable class is one recurrent class | — | R | Reachable set is closed, so irreducible ⇔ every state reaches the start (reverse search; toggles are involutions). A singleton closed class has R=0 because toggles never self-loop. Tested against `gt0.class_structure` on all 36 N=4 family-grade-modes and on synthetic absorbing and mixed chains | all |
| `recurrent_class_sizes` | Sizes of recurrent classes | — | R (partial) | `[size]` when irreducible. For reducible classes, `None` (E0 listed all classes); no E1 candidate cell is reducible at N≤6 | all |
| Stationary law π_jump, π_ct = π_jump/R | Occupancy | both | I | Lazy power iteration by gathers. Stops when L1 change < 1e-15 **and** maximum per-entry relative change < 1e-13. Second run from the point mass on the start; the two limits must agree to 1e-10 L1. Checked against dense LU, GTH elimination and an exact rational solve (section 3) | all |
| `occupancy_ct` (edge-count distribution, expected edges, triangles, wedges, maximum degree, degree variance, full-centre probability) | Shape distribution and means | continuous | S | E0 expressions on `gtobs.structure_arrays` (narrower integer types, same values) | all |
| `edge_count_modes` | Strict local maxima of the edge-count distribution | continuous | S, **tie-sensitive** | Exactly equal neighbouring values (binomial symmetry in NULL, some composites) make the strict-peak test depend on rounding. E0 values in 4 N=5 cells were decided by rounding. The validator accepts a difference only when both lists are inside the tie-aware plateau set | all |
| `held_jump`, `held_continuous` (attachment fraction, by free-edge count, distance distribution, radial drift, escape, capture) | Source-relative occupancy and drift | jump: per event (P = W/R); continuous: per unit time (rate W) | R | Distances from a multi-source breadth-first search on neighbour bitmasks for all states at once (equal to `gt0.distance_to_source`, tested on all N≤5 and sampled N=6 states). Drift, escape and capture use the target's distance by index. Equal to `gt0.held_observables` on design cells | all HELD |
| `shell_activity` (activity by shell, near/far ratio ρ = A(1)/A(2)) | Local event activity | both | R | Same sums grouped by shell; tested against `gte0a.shell_activity` | all HELD; shells 1–4 at N=7 |
| `free_jump`, `free_continuous` (edge-count distribution, triangles given edge count) | Shape occupancy | both | R | Grouped sums; tested against `gt0.free_observables` | all FREE |
| `reversibility` (entropy production per time and per event, irreversible flux fraction, elementary-square affinities, one-sided transitions) | Stationary current and cycle affinity | both (per-event = per-time / mean rate) | S | Array code reused; 153 (HELD) or 210 (FREE) slot pairs at N=7 | all |
| `projected_current` | Net flux between projection bins: (free edges, attachments) for HELD, (edges, triangles) for FREE | — | S, **noise floor** | E0 lists pairs with net > 1e-15 × total flux, which is float noise. Gradient cells sometimes list or omit a noise pair. Ties among top entries are structural (equal currents along one cycle), so order is arbitrary. The validator compares entries by identity and ignores entries below 1e-12 | all |
| `event_order` (pattern asymmetry, immediate reversal, top patterns: the handover) | Time-reversal asymmetry of consecutive event pairs on the stationary jump chain | jump (order is clock-free) | R | Integer type codes and one `bincount` per slot pair instead of string masks; equal to `gte0a.event_order` | all |
| `hub_frame.event_order`, `hub_frame.projected_current` | The same in the emergent-hub frame (hub = every max-degree vertex, ties included) | jump | S | `gte0b` array code reused | all |
| `class_table`, `symmetry_max_abs_difference` | Occupancy by symmetry class (S3×S(N−3) in HELD; S_N in FREE) | both | R | Permutations by 8-bit lookup tables. FREE class counts 11, 34, 156 for N=4, 5, 6 match the number of unlabelled graphs. Table and symmetry check equal to `gte0a.class_table` | all; FREE N=7 has 5,040 permutations |
| `gibbs_projection` (KL to the moment-matched triple-local Gibbs law) | Distance from the gradient family | continuous | S | E0 Newton code reused; non-convergence flagged as in E0 (X-PROJ) | all |
| `predicted_law_l1_gap` | Gap to the analytic Gibbs law of a gradient family | continuous | S | At HELD N7, CLOSE strong_favour (fixture) gives 2.7e-16 | all, W4 |
| `autocorrelation`, `localisation_persistence_index` | Integrated autocorrelation time ∫C(t)/C(0)dt of indicator and count functions | continuous time, also in mean events | I | E0 solved (−G + 1π)x = f̃ densely, only up to 4,096 states. For π-centred f̃ this is −G x = f̃, i.e. (I−P)x = f̃/R on the jump chain. The jump chain has period 2, so the series uses the lazy chain: x = ½ Σ P_Lᵏ (f̃/R), re-centred each term. Stops at relative term 1e-13. Equal to the dense result to 1e-9 relative on design cells; NULL edge indicator gives exactly ½ | all (**new above 4,096 states**: FREE N6 and every N=7 cell) |
| `spectrum` (relaxation gap, complex eigenvalue count, oscillation index) | Full generator spectrum | continuous | **O** | Dense eigen-decomposition. E0 already omitted it above 4,096 states (FREE N6). It is not reproduced at any N by `gtobs`; the E0 values at N≤6 stand. Reason for omission: the full spectrum (and complex-eigenvalue counts) needs dense algebra; a sparse estimate of the gap alone would not reproduce the oscillation channels. The autocorrelation times of the declared functions carry the slow-mode information E1 needs | E0 N≤5, HELD N6 |
| Trajectories (4 × 400 events) | Illustrative Gillespie paths; no table statistic uses them | continuous | S | E0 sampler reused, same seeds; summary by sorted-array lookup, equal to E0 | all |
| `e1_additions.held` (attachment margin, null-density-standardised margin, detached-probe-count distribution) | Density-controlled source selectivity; full detachment distribution | both | A | Margin identity af − r0 checked; both margins exactly 0 under NULL (N=5, 6) | all HELD |
| `e1_additions.hub_structure_ct` (maximum-degree distribution, tied-hub count, hub includes source / probe / probe only) | Hub ties and fluctuating hubs | continuous | A | Fixtures: empty (all tied, degree 0), complete (all tied), star (unique hub) | all |
| `e1_additions.witness_census_jump` | Witness count engaged per executed event of each component; mean log-weight | jump | A | Distribution sums to 1. The measured confound channel of the audit | all |
| `e1_additions.autocorrelation_extra` (hub indicator of vertex 0 in FREE, of the probe in HELD) | Hub persistence | continuous | A | Same series as above | all |

## 3. Numerical findings about the published E0 values

The reproduction found three kinds of fragility in published E0 numbers. None changes a published finding's statement. All are recorded in the ledger as GT-F35. The published tables are unchanged.

1. **Dense LU loses accuracy on improbable states.**
   - **HELD N5 PATHF weak_favour (128 states).** Stationary probabilities reach 1e-12. Measured against an exact rational GTH solve, E0's dense solve had relative errors up to 2.9e-6 there; the new iteration has 6.6e-16.
   - **HELD N6 non-gradient cells.** Probabilities reach 1e-38. The dense solve returned tiny negative values, and E0 clipped them to exactly zero, for 13–136 states per cell.
   - Two consequences:
     - `one_sided_transitions`, published as 120–2,136 in five cells (PATHF, PATHH, CSPF, CWPF, CWPH), is an artefact. Forward flux was positive, but reverse flux from a clipped state was zero. The true value is 0.
     - `attachment_fraction_by_free_edge_count` at densities of stationary mass 1e-14 to 1e-35 is wrong by up to 0.56. Mostly this is k = 9–11; in the saturated cells it is k = 1–8.
   - Wherever `gtobs` and E0 disagree in a cell of ≤4,096 states, a float GTH referee (subtraction-free, positive by construction) decides. In all 15 such cells it agrees with `gtobs`.
   - No published report sentence, finding or hypothesis uses either channel at the affected densities. In particular, the CSPH a/k profile used in the confound audit (k = 1–6) is unaffected; CSPH differs only at k = 11.
2. **L1-stopped iteration leaves rare states unconverged.** E0's FREE N6 cells used lazy iteration stopped on L1 change alone. In the two saturated FREE N6 cells (PATHF weak_favour, PATHH weak_suppress), edge counts 3–10 carry stationary mass from 1e-33 to 1e-17. E0's values of `triangles_given_edge_count` there differ from converged values by up to 67%; E0's law at those states is off by up to 10¹⁵ relative. A strict two-start run (relative change 1e-15 from uniform and from a point mass, agreeing to 1e-15) is the referee for classes above the dense limit, and agrees with `gtobs`. The affected values describe practically unvisited densities and carry no weight in any aggregate.
3. **Tie- and threshold-dependent definitions.** `edge_count_modes` (strict peaks, equal neighbours) and the inclusion threshold of `top_net_currents` (1e-15 × total flux) depend on rounding in E0. `gtobs` keeps the definitions for comparability. The E1 draft proposes reading modes with the tie-aware plateau rule and treating currents below 1e-12 of total flux as zero.

## 4. Reproduction of all published E0 cells

Run (opt-in, about 13 minutes; not in CI):

```
python -m rs_constraint_lab.gtobs_validate --n 5 --n 6 --out report.json
```

Result: see `provenance/e1-observables-validation.log` (final code) and the summary table below.

Final run at code commit `8414d7c` (12 minutes, 347 MB peak). Each published cell falls in exactly one row:

| Outcome | N=5 cells | N=6 cells | Total |
| --- | --- | --- | --- |
| Agrees with the published table on every compared channel | 40 | 27 | 67 |
| Differs only where the GTH referee shows E0's dense solve wrong (item 1) | 2 | 13 | 15 |
| Differs only where the strict two-start referee shows E0's L1-stopped iteration wrong (item 2) | 0 | 2 | 2 |
| Unexplained difference | 0 | 0 | **0** |
| Total | 42 | 42 | 84 |

Also:
- **Tie-sensitive E0 value** (`edge_count_modes`, item 3) in 4 cells (N=5), within the tie-aware plateau.
- **New capability.** E0 published `None` for autocorrelation in all 21 FREE N6 cells (above its dense limit). `gtobs` computes it with the declared tolerance.

Not compared: the spectrum (omitted), timings, solver diagnostics and the additions.

## 5. Cost at N=7 (theorem-fixed fixtures only)

Measured on theorem-fixed cells (`provenance/e1-fixtures/`). Full pipeline, no trajectories. Extrapolations for scientific cells are in `docs/e1-held-free-feasibility.md`.

| Fixture | States | Wall | Peak RSS | Stationary | Autocorrelation | Classes | Check |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HELD N7 NULL | 262,144 | 136 s | 450 MB | 31 s (point start: 577 iterations) | 90 s (467 terms) | 1.1 s (144 permutations) | two starts agree to 1.0e-13 relative |
| HELD N7 CLOSE strong_favour | 262,144 | 136 s | 452 MB | 59 s (537 + 575 iterations) | 62 s (320 terms) | 1.1 s | analytic Gibbs law to 2.7e-16 L1 |
| FREE N7 NULL | 2,097,152 | 1,512 s | 3.2 GB | 332 s (point start: 673 iterations) | 855 s (542 terms) | 178 s (5,040 permutations) | two starts agree to 1.3e-13 relative; symmetry 0 |

The autocorrelation loop was then made allocation-free: HELD N7 NULL went from 90 s to 73 s, and the results are unchanged (tests). The fixture rows keep the earlier, conservative times.

## 6. Edge cases covered by tests

- Empty graph, complete graph and a probe chain at distance 3 (distances).
- Disconnected probes (distance −1, "inf").
- Synthetic absorbing, mixed and irreducible chains (regime).
- A zero-rate state (stationary reported unresolved).
- A class not closed under the symmetry group (raises).
- Constant function (autocorrelation `None`, the zero-variance denominator).
- Tied hubs: empty, complete and star.
- NULL identities: uniform law, zero margins, edge indicator τ = ½.
- Gradient and non-gradient pairs (CLOSEW against CSPH and PATHF/PATHH) in every equivalence test.
- W3 and W16 kernels against `build_kernel` (relative 1e-14; 1/3 is not exact in binary). W4 stays bit-exact.

## 7. Limitations

- **Spectrum omitted** (section 2).
- **Recurrent class list for reducible cells** is not computed. If a frozen E1 cell turned out reducible, its regime would still be classified correctly, but the class sizes would be `None`.
- **Solver cost** depends on the slowest mode of each chain. Iteration counts are measured at N≤6 and on fixtures at N=7; for scientific N=7 cells they are extrapolations (`docs/e1-held-free-feasibility.md`). The iteration cap is 2,000,000. A cell that reaches it, or whose two starts disagree, is reported unresolved, not estimated.
- **Rare-state conditionals.** The new solver resolves them to about 1e-13 relative. Conditionals on sets of mass below about 1e-15 should still be read as describing unvisited configurations.
