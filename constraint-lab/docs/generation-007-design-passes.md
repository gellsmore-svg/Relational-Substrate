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
