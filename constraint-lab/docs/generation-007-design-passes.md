# Generation 007 design passes

These vectors are ordinal design-selection scores on a `0–5` scale. Higher is better. They are not empirical facts, probabilities, or a confidence score. They are not summed. The external vector and the Grok vector are not averaged.

Dimensions:

```text
CI  causal isolation
CF  control fairness / comparability
CB  computational boundedness
IN  interpretability
IG  expected information gain
CR  resistance to confounding
PR  provenance / reproducibility clarity
```

The question being designed for is the confound left by Review 006. v0.6 matched action geometry, nominal weight, and polarity. A gated rule is active in fewer states than its condition erasure, so the same nominal weight is not the same singleton perturbation. The question is whether a lower-order control, calibrated to the higher-order singleton's controlled-committor effect, still produces a composed interaction at least as large, and whether higher-order gating still contributes hidden-state selectivity after that calibration.

Ontology stays fixed: `N = 4`, `O = 3`, `G = S = H = L = 0`, independent hypergraph. No second passage, no simplicial semantics, and no larger system in this round.

## Pass 1 — before implementation

Written before the calibration engine and before any composed-system margin is read. Costs, monotonicity, and root counts below are expectations, not measurements.

### External vector

The externally selected primary design is to effect-match the lower-order singleton control to the higher-order singleton before comparing the corresponding two-rule compositions. Its vector is CI 5, CF 5, CB 4, IN 5, IG 5, CR 5, PR 5. CB is the weaker coordinate because continuous calibration adds root finding and more kernel evaluations.

| Candidate | CI | CF | CB | IN | IG | CR | PR |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Effect-matched erased control | 5 | 5 | 4 | 5 | 5 | 5 | 5 |
| Effect-matched pair-face control | 5 | 5 | 4 | 5 | 5 | 5 | 5 |
| Broader P->P + P->P census | 2 | 2 | 3 | 2 | 2 | 2 | 5 |
| Second graph-class passage now | 3 | 4 | 4 | 4 | 4 | 3 | 5 |
| T->P + T->P family | 3 | 2 | 4 | 3 | 3 | 3 | 5 |
| Simplicial semantics | 1 | 1 | 3 | 2 | 2 | 1 | 5 |
| Add H/S/G/L or larger N | 1 | 1 | 2 | 2 | 1 | 1 | 4 |

The external note is that the two effect-matched controls may both be needed. Erasure alone is not assumed to be sufficient.

### Grok vector

Assigned independently, before implementation. Disagreements are explained under the table. They are not averaged with the external vector.

| Candidate | CI | CF | CB | IN | IG | CR | PR |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Effect-matched erased control | 5 | 4 | 4 | 5 | 5 | 4 | 5 |
| Effect-matched pair-face control | 5 | 5 | 4 | 5 | 5 | 4 | 5 |
| Broader P->P + P->P census | 2 | 2 | 3 | 2 | 1 | 2 | 5 |
| Second graph-class passage now | 2 | 3 | 4 | 4 | 3 | 2 | 5 |
| T->P + T->P family | 2 | 2 | 4 | 3 | 2 | 2 | 5 |
| Simplicial semantics | 1 | 1 | 3 | 2 | 1 | 1 | 4 |
| Add H/S/G/L or larger N | 1 | 1 | 2 | 1 | 1 | 1 | 4 |

### Disagreements

Effect-matched erasure isolates the duty-cycle confound: the control keeps the action edge, the action direction, and the event, and a continuous multiplier is chosen so the singleton controlled committor matches. CI, IN, IG, and PR agree with the external vector. CF is 4 rather than 5 because equal aggregate `Delta` is not equal state-resolved effect, and an ungated rule fires on a different set of states than the triad gate. CR is 4 for the same reason. A later negative margin could still be a difference of hidden-state shape. The design has to classify that. It does not make erasure's fairness perfect in advance.

Effect-matched pair-face control is the stricter comparison. It keeps a gate and replaces order-3 dependence with order-2 dependence, then calibrates the multiplier. CF stays 5. CR is 4 rather than 5 because v0.6 already showed that `contains_t_action_edge` has no disjoint live face, and because one scalar multiplier may fail to match both passage directions. Those are limits to measure, not reasons to drop the control. CB stays 4. Root finding is extra work, and the predeclared cell set is still far smaller than the v0.6 lattice.

A broader pairwise census does not calibrate singleton strength, so it repeats the v0.6 confound on a larger set. IG is 1 rather than 2. The other coordinates agree.

A second graph-class passage is a real later question. Running it now changes the passage before the strength confound on the current passage is removed. CI is 2 rather than 3, CF is 3 rather than 4, IG is 3 rather than 4, and CR is 2 rather than 3.

A `T->P` plus `T->P` family asks whether two higher-order rules interact. It is not a lower-order control for this singleton. CI is 2 rather than 3, IG is 2 rather than 3, and CR is 2 rather than 3.

Simplicial semantics replaces the event model. The resulting committor would not be the v0.5 observable. IG is 1 rather than 2, and PR is 4 rather than 5, because no translation back to the stored committor is part of the proposal.

Adding `H`, `S`, `G`, `L`, or a larger `N` makes the same confound harder to read. IN is 1 rather than 2. The other coordinates agree.

### What drove the selection

The selected design is both effect-matched controls, used in this order:

```text
1. effect-matched condition erasure
2. effect-matched adjacent pair-face gate
3. effect-matched disjoint pair-face gate where v0.6 already marks that face live
```

Same-as-action faces stay redundant or unsatisfiable. They are not invented as live controls.

Erasure is required because it is the control that produced the v0.6 negative margin. Pair-face is required because erasure removes the gate entirely, so it cannot by itself say whether an order-2 gate, once strength-matched, still falls short of the order-3 gate. Dropping either control would leave the Review 006 confound only partly asked.

The Grok vector for that combined design, not an average of the rows above, is:

```text
CI 5
CF 4
CB 4
IN 5
IG 5
CR 4
PR 5
```

CI and IG carry the choice. No other candidate holds the action fixed and removes the nominal-weight confound before the composition comparison. CF is 4 because the primary match is an aggregate singleton scalar, with state-shape reported beside it rather than assumed away. CR is 4 because forward and reverse multipliers may differ, and because one geometry has no disjoint face. CB is 4 for the same reason as the external vector. IN and PR are at the top of the scale if cells, tolerances, scales, the root-selection rule, and the search domain are frozen before composed margins are read.

Rejected for this round:

- A broader pairwise census does not effect-match.
- A second passage, a two-triad family, simplicial semantics, and a larger ontology each change a variable this round is trying to hold still.

### Both control types

Both are necessary. The decision is not deferred to the data. Pass 2 may narrow duplicated calibration problems. It may not drop pair-face or erasure because one of them is cheaper.

### Factual uncertainties that can change a coordinate

- Monotonicity and root multiplicity are not yet measured. Non-monotone branches, or several roots, would lower IN and CR. All roots stay recorded. The predeclared selection rule is the root with smallest absolute log-distance from the target's nominal multiplier.
- A prohibit singleton may have no finite multiplier. That is a result to classify as `finite solution`, `zero-boundary solution`, `no finite solution`, or `unresolved`. It lowers the coverage of the finite comparison. It does not justify moving `m` off zero to force a finite match.
- If one scalar cannot jointly match both directions, composition claims on that cell are not fair. The design already separates singleton representability from composition difference.
- Severe state-shape mismatch after a good aggregate match would lower CR of any magnitude claim and would be the input to Pass 3. It is not a reason to start with two free parameters.
- v0.6 target symmetry across geometry and polarity does not automatically extend to control effect functions. Reuse requires a numerical cross-check. Skipping it would lower CR and PR.
- Calibration cost is unknown. A large log grid over many repeated systems could lower CB. Caching by constraint structure, multiplier, and `rho3` is part of the design so that repeated systems are not solved again.
- The matching tolerance is not the scientific effect floor. Preflight may keep or replace a suggested absolute tolerance of `1e-8` before margins are read. The floor used for scientific effects stays separate.

Pass 1 is not rewritten by later passes.

## Pass 2 — after calibration preflight

Written after the numerical reference and a five-cell singleton calibration. Composed margins were not read. Pass 1 above is unchanged.

### Measurements

The numerical reference keeps both `1e-8` declarations. The worst gap is `1.5237811012980274e-14`, on the direct-versus-iterative committor of the `m = 0` kernel. Named W4 factors reproduced by the continuous multiplier differ by `0`. The anchor singleton differs from the published Generation 6 `Delta_T` by `0`. Unconditional controls stay triad-flat below `1e-8`. The match tolerance and the effect floor stay separate fields. A weak-suppress joint residual that once sat just above `1e-8` was a golden-section stop at log10 width `1e-4`. Tightening that stop to `1e-7` brought the residual under the tolerance. The tolerance was not loosened.

The positive grid is 33 points, `log10(m) = -4 + i/4`, endpoints `1/10000` and `10000`. Grid sha256:

```text
076d0ad2498359546e350433f089fa37e25f04a1ef1f12266c2bd135d62a04d4
```

Coverage, counted before the census:

```text
target cells                         28
unique target singletons             20
unique erased calibration problems   20
unique face calibration problems     30
unique control structures             5
one-direction root solves           140
joint minimisations                  70
expected grid kernel evaluations    170
expected target singleton solves     20
```

One full curve, 34 kernels, took `5.002034981996985` seconds. That is `0.1471186759410878` seconds per grid point, and about `25.01` seconds for the 170 grid evaluations if each structure is solved once. Root polishing is extra. The five-cell singleton sample below used 977 kernel evaluations in `162.47` seconds on one process. It is 5 of the 28 cells. It does not include composed packs or the robustness probes. The census wall clock is not measured here. With five cached structures, two workers, and shard length 14, the run is a bounded calibration, not a second lattice.

The five cells are `contains_p_companion_edge` / `absent` for prohibit/prohibit, weak_suppress/weak_suppress, and strong_favour/strong_favour; `contains_p_companion_edge` / `present` for strong_suppress/strong_suppress; and `contains_t_action_edge` / `absent` for strong_favour/strong_favour. They were chosen as the anchor, the two finite grade extremes, the other polarity, and one geometry cross-check. They were not chosen by a margin.

Singleton effect functions on this sample are non-monotone and sign-changing for every erasure curve. Pair-face curves are mixed: one direction often monotone, the other often non-monotone, and both sign-changing. Accepted root counts are 1 or 2. A sign-change bracket misses a turning point. The weak_suppress erasure has no sign change inside tolerance and is recorded as `residual_minimum` at `m = 5.912836006187e-1` in both directions, with mismatches `4.251432539348343e-12` and `1.7005730157393373e-11`.

Condition erasure jointly matches every cell in the sample:

| Cell | Delta_T path | Delta_T matching | m joint | joint distance | class |
| --- | --- | --- | --- | --- | --- |
| absent prohibit/prohibit | -0.00014811954486695922 | -0.0005924781794679479 | 3.090231902056e-1 | 4.899531398618103e-09 | finite solution |
| absent weak_suppress/weak_suppress | 1.5943155207420734e-05 | 6.377262082979396e-05 | 5.912836006187e-1 | 3.7711691810269747e-07 | finite solution |
| absent strong_favour/strong_favour | -0.0011971123165731012 | -0.004788449266292405 | 2.539632711361e+0 | 1.9486550679900846e-08 | finite solution |
| present strong_suppress/strong_suppress | -3.684071450540949e-05 | -0.00014736285802174898 | 1.102086401766e+0 | 1.2939426947399198e-07 | finite solution |

The prohibit anchor's erasure match is finite. `only_exact_solution_is_zero` is false. Two sign-change roots exist, and the selected root is the one closest in log-distance to the nominal deletion. Deletion is not the only exact match on this cell. That does not reclassify the other cells.

On the present strong_suppress erasure, the one-direction roots are both `4.623069417062e-1` and also meet the tolerance, while the joint minimiser is `1.102086401766e+0`. Both multipliers jointly match. The predeclared rule keeps the minimiser. The census must not treat those two multipliers as the same control.

Pair-face controls match one direction at a time on every sampled face, and jointly match none of them. Joint distances sit between `1.2806645580317706` and `1.3418969097226727`. The absolute mismatches are orders of magnitude above `1e-8`. Forward and reverse multipliers can differ sharply: the absent strong_favour adjacent face is `1.355519025646e+0` forward and `1.188637321371e+1` reverse. A single scalar does not reproduce that pair-face singleton in both directions on this sample.

The geometry cross-check does not justify collapsing cells. Absent strong_favour path `Delta_T` is `-0.0011971123165731012` on `contains_p_companion_edge` and `-0.0011971123165730457` on `contains_t_action_edge`. The erasure and adjacent multipliers agree at the printed precision. Present strong_suppress is a different singleton, path `Delta_T` `-3.684071450540949e-05`. Polarity is not collapsed. `contains_t_action_edge` still has no disjoint face. All 28 cells stay in the census. Shared control structures are cached. They are not dropped.

### Vectors

External vector, unchanged from Pass 1:

```text
CI 5, CF 5, CB 4, IN 5, IG 5, CR 5, PR 5
```

Old Grok vector for the combined design, from Pass 1:

```text
CI 5, CF 4, CB 4, IN 5, IG 5, CR 4, PR 5
```

New Grok vector:

```text
CI 5, CF 4, CB 4, IN 4, IG 5, CR 4, PR 5
```

### Why the coordinates move or stay

IN moves from 5 to 4. The sampled curves are non-monotone, several have two accepted roots, and one finite match is a residual minimum rather than a sign change. The selected multiplier is still readable, because every accepted root is stored and the selection rule was frozen before this measurement. It is no longer a picture of one monotone branch.

CR stays 4. The threat in Pass 1 was a silent choice among branches. The run records every accepted root and applies the predeclared closest-log rule, or the joint minimiser, and it records when those two multipliers differ. Forward and reverse pair-face multipliers differ on the sample. That was already the reason CR was 4. It is now measured, not only expected.

CB stays 4. Five structures and a five-cell sample of 162.47 seconds keep the calibration bounded. Root finding is real work. It is not a reason to drop cells that share a cached curve.

CF stays 4. Erasure can match the aggregate singleton on this sample, including jointly. Pair-face gates match one direction and miss the joint vector by a relative distance near 1.3. Equal aggregate `Delta` is still not a state-resolved match. State shape is not read in this pass.

CI, IG, and PR stay. The action edge is still the isolated variable. The sample separates singleton representability from composition, which has not been read. Tolerances, scales, the grid hash, and the selection rule are in the specification.

### Decision

Both control types stay, in the Pass 1 order: effect-matched erasure, then the adjacent face, then the disjoint face where v0.6 marks it live. The sample says erasure and pair-face are not interchangeable. Pair-face joint failure on these cells is a representability observation. It is not yet a reason to add a second lower-order parameter. That decision waits for the census and Pass 3.

The full 28-cell set stays. No cell is dropped for cost, for a duplicated structure, or for a boundary solution. The prohibit anchor is not forced onto `m = 0`. No second passage, no simplicial semantics, and no richer control is started in this pass.

## 007R Pass 1 — before the resumable executor

Written after the aborted attempt and before the micro-batch supervisor. Pass 1 and Pass 2 above are unchanged. No composed margin is read in this section. Costs below are expectations.

The scientific design stays the combined effect-matched design already selected. This pass asks how that design is allowed to run.

### External requirement

Prompt 007R requires that no expensive computation depend on one long-lived process, that the largest unit of work be a loss the laboratory is willing to repeat, and that another terminal be able to tell running, progressing, stalled, failed, stopped, complete, and safely resumable apart. A process that consumes CPU for hours without useful progress is a failed design.

### Grok vector — execution architectures

Assigned before the supervisor was written. Not averaged with the scientific vectors above.

| Candidate | CI | CF | CB | IN | IG | CR | PR |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Resume the two-shard Generation 7 process | 4 | 4 | 1 | 2 | 4 | 3 | 1 |
| Micro-batch supervisor over persisted multiplier evaluations | 5 | 4 | 5 | 4 | 5 | 4 | 5 |
| Two-parameter lower-order control before the scalar census | 3 | 4 | 3 | 3 | 3 | 3 | 4 |

### Disagreements with resuming the shard

The shard runner isolates the same scientific objects, so CI and CF do not fall to the floor. CB is 1 because one shard of fourteen cells held calibration, composition, and robustness inside one process, and the forensic record shows that process still marked running many hours after it started, with no item file. IN is 2 because an observer could not tell a slow kernel from a hang. PR is 1 because a partial shard result has no per-evaluation identity and cannot be validated as a completed item. That architecture is rejected.

The micro-batch design keeps the action fixed and the calibration rule unchanged, so CI stays 5. CF stays 4 for the same reason as the scientific Pass 1: an aggregate singleton match is not a state-shape match. CB moves to 5 because each worker owns one batch with a 120-second watchdog, and a batch is sized from a measurement rather than from a cell count. IN is 4 rather than 5 because adaptive refinement means the final number of evaluations is not known at the start; the status line has to say "current plan" or it will overclaim. IG stays 5. CR stays 4 because forward and reverse multipliers may still differ. PR is 5 when item hashes, receipts, and the prompt identity are on disk before the census.

A two-parameter control is not started in this pass. The scalar census has not been completed under a trustworthy executor. Opening it now would change the control before the representability failure is measured.

### Execution-health expectation

These scores are operational, not scientific, and they are not summed.

```text
B batch boundedness        5
O observability            5
R resumability             5
F fault isolation          5
D durability               5
T token efficiency         4
```

T is 4 because status and the tail of the progress log are concise, while a later report still has to read the merged summary. O, R, and F below 4 would reject the executor even if the arithmetic succeeded.

### What this pass does not do

It does not drop a control, a cell, or a passage direction. It does not import the forensic shard. It does not treat the in-process Pass 2 sample as a generation result. That sample remains a preflight note. The batch measurement and the census still have to be produced by the new executor.

## 007R Pass 2 — after the batch measurement and the smoke

Written after the measured batch policy and the smoke run, and before the census margins were read. Pass 1, the scientific Pass 2, and 007R Pass 1 are unchanged. No composed census margin is an input to this section.

### What was measured

The batch count is `floor(45 / p90)`, reduced while `count * p90 > 60` or `count * max > 100`, with the watchdog left at 120 seconds. On this machine, with numeric threads pinned to 1:

```text
multiplier            p90 0.315s    142 items
target singleton      p90 0.307s    146 items
target composition    p90 0.533s     84 items
control composition   p90 0.545s     82 items
```

The smoke supervisor started in its own session, pid 35071, at `2026-10-12T08:51:31Z`, and reached `COMPLETE` at `08:51:48Z`. The plan opened at 72 items and closed at 76. Five receipts. The slowest batch was 68 items in 13.386 seconds. Timeouts, splits, retries, and quarantines were 0. Both calibrations are `smoke_capped`. The smoke merge, checked at close-out, has `used_as_matched` false on every strategy. The joint text `m = 1` is the cap marker. Smoke verify `--require-complete` accepted 76 items and 5 receipts.

The platform fault tests had already passed in the suite at the executor commit: partial writes, reuse, receipts, process-tree kill, batch split, quarantine, killed-worker reschedule, heartbeat, status before the first interval, status watch, graceful stop, duplicate-supervisor refusal, stale-lock recovery, restartable merge, and a deliberate missing item.

### Grok vector

The micro-batch design, scored again after those measurements. Not averaged with the scientific vectors.

```text
CI 5, CF 4, CB 5, IN 4, IG 5, CR 4, PR 5
```

No coordinate moves. CB stays 5 because the measured batches sit inside a minute and the smoke's slowest batch was 13.4 seconds, with the 120-second watchdog unused. IN stays 4 because the smoke plan grew from 72 to 76, so a status line during adaptive work has to say "current plan". CF stays 4 because the smoke did not turn an aggregate evaluation into a state-shape result, and the cap marker is not a match. CR stays 4 because forward and reverse multipliers have not yet been compared on the census. PR stays 5 because the smoke items, receipts, and verify report are on disk.

The execution-health expectation from 007R Pass 1 is not re-scored here. The census had not run. A process that finishes the smoke and then hides the census inside one foreground command would drop O and T. The census is required to start detached.

### Decision

Run the 28-cell census through the detached supervisor. Keep both control types. Keep both directions. Do not open a two-parameter control. Do not import the forensic shard. Do not treat the smoke `m = 1` texts as matches. Do not retune the `1e-8` floors. The in-process Pass 2 sample stays a preflight note.

## 007R Pass 3 — after the primary census

Written after the detached census reached `COMPLETE`, the merge wrote 28 rows, and verify accepted 3,880 items, 238 receipts, and 104 converged calibrations. The report is `reports/generation-007-effect-matched-controls.md`. No earlier pass is edited. The floors, the grid, and the Pass 1 scores are not retuned.

### What the census changed in the picture

Condition-erased controls match all 28 cells in each direction and jointly. Pair-face controls match each named direction and miss the joint vector on all 42 problems, with distances from about 1.28 to 1.34. One-direction erasure margins `M_I` and `M_G` are negative on all 24 finite cells. The joint erasure match keeps that sign on 16 of 24 and reverses `M_I` on 8, because the joint root is about `m = 1.102` where the one-direction roots are about `m = 0.462`. All 48 finite erasure joint state-shape reports are poorly state-shape matched. Target `delta_S` remains, and the controls stay triad-flat. `m = 0` is not selected. Recalibration at `rho3 = 2` can flip the prohibit sign; the held primary multiplier does not.

### Grok vector

```text
CI 5, CF 4, CB 5, IN 4, IG 5, CR 4, PR 5
```

No coordinate moves. The reasons are now measured.

CI stays 5. The action edge is still the isolated variable. Rho robustness does not add a second action.

CF stays 4. Erasure can match the aggregate singleton, including jointly, and the statewise residual is still mixed. Median `max_abs` on the finite joint reports is about 0.011, and the largest is about 0.039. Pair-face is not a fair two-direction control: using its one-direction margins as a joint comparison would drop CF further, and the census does not do that.

CB stays 5. The slowest batch was 27.5 seconds. The watchdog did not fire. The closed plan is 3,880 items, of which 3,662 were requested after the initial 218.

IN stays 4. The final count is now known, which removes the execution-time reason for this score. The scientific reason remains. Sixteen erasure curves in each direction have two roots, and the sign of `M_I` on eight finite cells depends on which root the strategy selects. A single quoted multiplier would overclaim.

IG stays 5. The census separates scalar representability from composition magnitude, and it separates both from selectivity and from state shape.

CR stays 4. Erasure forward and reverse roots agree to a relative gap of about `3e-6`. Pair-face ratios run from about 0.114 to 1.34. The joint selector and the one-direction selector disagree on the sign of eight finite erasure cells. That disagreement is recorded. It is not removed.

PR stays 5. Item hashes, receipts, the spec hash, and verify are on disk. The forensic shard stayed out.

### Execution-health vector, scored from the run

```text
B batch boundedness        5
O observability            5
R resumability             5
F fault isolation          5
D durability               5
T token efficiency         4
```

These are not summed and not averaged into the design vector. R is the fault-test result. The census operational block records `resume_events` 0. T stays 4 because the report reads the merged summary. O, R, and F are all above the rejection line.

### What this pass does not do

It does not drop the eight sign-flip cells. It does not prefer the strategy with the larger higher-order margin. It does not start 007B. It does not schedule `W3` or `W16`. It does not move the `1e-8` floors.

## 007R Pass 4 — next step

Written after Pass 3. The question is which single next experiment the census justifies. None of these candidates is run in this branch.

### Candidates

| Candidate | CI | CF | CB | IN | IG | CR | PR |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Stop, and leave the pair-face joint gap untested | 5 | 4 | 5 | 4 | 2 | 4 | 5 |
| 007B, a frozen two-parameter pair-face control, scored and counted before any run, executed later by this supervisor | 4 | 4 | 4 | 3 | 5 | 3 | 4 |
| Graph-class routing now, among the 3-edge star, the triangle plus an isolated vertex, and the 3-edge path | 2 | 3 | 3 | 3 | 3 | 2 | 4 |

### Why these coordinates

Stopping keeps the erasure result readable and adds no new confound. IG is 2 because the census isolated a concrete representability failure and then declined to test the obvious next control. That is a completed finding only if the face question is closed. It is not closed.

007B aims at the failure the census measured: 42 pair-face joints, one valley each, distance about 1.28 to 1.34. CI is 4 rather than 5 because a second free weight can become a second exposure unless the parameterisation is frozen before the run and the erasure scalar remains the comparison. IN is 3 because two parameters are harder to read than one multiplier. CR is 3 because a richer control can fit more, and a fit is not by itself evidence of higher-order magnitude. PR is 4 until the control, the work count, and the spec hash exist before execution. CB is 4 because the same supervisor can bound the run, and the work count is still uncalculated. IG is 5 because this is the gap in hand.

Graph-class routing now changes the graph while the face control is still a one-direction object and while the erasure magnitude sign still depends on the selector. CI is 2 and CR is 2 for that reason. The fork stays in the report as a later experiment. It is not the smallest next step.

### Decision

The next experiment is 007B. It is not started. Before any run the laboratory has to name the two parameters, freeze them in a specification, score that specification against the erasure scalar, and calculate the item count under the same batch policy. The scientific question it is allowed to answer is whether a second lower-order parameter can represent the pair-face singleton in both directions, and what `M_I` and `M_G` do after that representation. It is not allowed to replace the erasure result, and it is not allowed to run as one opaque process.
