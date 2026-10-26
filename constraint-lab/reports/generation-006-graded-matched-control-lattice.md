# Generation 006 — graded matched-control lattice

Experiment `generation-006-graded-matched-control-lattice`. Analysis `n4-graded-matched-controls`, version `0.6.0`. Control mapping version `0.6.0`. Specification `experiments/specs/generation-006.json`, sha256 `b9b60e103ab5abdb6f4ab5ab5fc5ae4b59dea234244604cd802ba3f2df3865b4`. Catalogue sha256 `60a80a31dacb92798c2e9f1ed1a846666b21f5eb8ffdf8934c6708689f5cfd7f`.

The run used 10 shards, 10 canonical targets each, and 2 workers. Failed 0. Quarantined 0. Summary `runtime_seconds` is 96.00385372998426. Shard-work is 95.53377 seconds. The summary `git_commit` is `89ad5dd6253b65dda6b3604e389243806e18f3c8`, the commit that contained the runner. Summary sha256 `aee5695d9387396f08c54be10048312153a391e50cee615de96be581210b910b`. Row table sha256 `9f078891f01de14c9c9e2e270ecca3f68f7810af19a811db5172f5b4defd0c33`. Surface sha256 `3b094edc965f78a7fcea76b836e03f94a4ccb0e76b4ce95f174ce6043f12aba0`.

Machine-readable tables:

- `reports/tables/generation-006-graded-matched-control-lattice-singles-n4-k2.csv`
- `reports/tables/generation-006-graded-matched-control-lattice-graded-surface.json`

The grids below are rounded to five decimal places. The JSON and CSV hold the stored values.

## A. Question and competing explanations

The question is whether the strong v0.5 two-rule effect is tied to the higher-order gate, once the action edges and the weights are held fixed, and whether that distinction survives when prohibit is replaced by a finite grade.

Three explanations stay separate:

```text
A. hard deletion / prohibit-specific effect
B. generic nonlinear two-rule composition
C. specifically higher-order-conditioned interaction
```

`I`, `G`, and `Delta_S` keep the v0.5 definitions. The analysis vector is not summed.

## B. External Review 005

Review 005 is `provenance/reviews/005-chatgpt-review-v0.5.md`. It reads v0.5 at `003a7c64a35ce8e781e7208117e09702ce63a715` and records Actions run `37151937623` on that head. The preceding close-out run is `37151793037`. The review is not a line-by-line audit. Its conclusion, which this generation tests, is that a nonzero interaction residual does not by itself establish a uniquely higher-order interaction, and that prohibit may be special because it deletes a transition.

## C. Recursive design Pass 1

Pass 1 is in `docs/generation-006-design-passes.md`. It is unchanged. The selected design was the target motif plus condition erasure plus pair-face controls. Grok's vector for that design was CI 5, CF 4, CB 5, IN 5, IG 5, CR 4, PR 5. The external vector scored the same design 5 on every coordinate. The disagreements are recorded there and are not averaged.

## D. Exact target and control grammar

Ontology: `N = 4`, `O = 3`, `G = S = H = L = 0`, independent hypergraph. Pair-face substitution is a control construction. It is not simplicial semantics.

The target is `dissolve(e_A) => w_P` together with `dissolve(e_B) | L(tau) => w_T`, with `e_A` disjoint from `e_B`. Both v0.5 geometries are kept: `contains_p_companion_edge` and `contains_t_action_edge`. Both polarities are kept. Each rule takes the full W4 grade set, independently, so each structural motif has a 5 by 5 weight lattice.

| Quantity | Count |
| --- | --- |
| Labelled targets | 1,200 |
| Canonical targets | 100 |
| Canonical structural targets | 4 |
| Orbit size | 12 on all 100 |
| Distinct labelled condition-erased controls | 150 |
| Canonical condition-erased controls | 15 |
| Labelled face attempts | 3,600 |
| Distinct labelled live face controls | 1,500 |
| Canonical face controls | 100 |
| Same-as-action present collapses | 300 |
| Same-as-action absent unsatisfiable | 300 |
| Within-target face deduplications | 100 |
| Live face equal to erasure | 0 |
| Invalid structurally simple pairs | 0 |

Orbit accounting closes: `100 × 12 = 1,200`. Deletion classes: both prohibit 4, exactly one prohibit 32, neither prohibit 64. Every geometry × polarity × weight cell has one canonical system. Ten erased ids are shared by a swapped unequal weight pair. `I` is symmetric in the two rules. The row records `erased_weight_role = assigned_by_weight_not_by_listing_order`.

Live face relations on the canonical records: adjacent 200, disjoint 50. A `contains_t_action_edge` target is matched to erasure plus one adjacent face. Its same-as-action face collapses or is unsatisfiable. The disjoint gate at the same weights is a face of the other geometry and is not attached to those rows.

Control 3 is not added. The pool of 100 canonical targets is below the v0.5 census of 2,304 and below the ceiling of 600.

## E. Recursive design Pass 2

Pass 2 is appended after the catalogue and the two-row benchmark. No coordinate changed. The in-process serial estimate was about 102 to 130 seconds. The completed run took 96.0 seconds of wall clock with 2 workers. That measurement does not revise Pass 2. Control 3 stayed off.

## F. Numerical validation

The effect floor stayed `1e-8`. The preflight rule was: keep `1e-8` when the worst reference gap is below `1e-10`. The worst preflight gap was `3.397282455352979e-14`, on the direct-versus-iterative committor of the condition-erased control. Block-versus-dense landing gaps were at most `1.1102230246251565e-16`. The anchor-versus-published interaction gap was a reproduction check and was not an input to the floor.

After the census, on the ten validation rows, the direct-versus-iterative committor gap is at most `2.930988785010413e-14`. Replay of the primary probe against the shard row has gap 0. The largest stationary or solver residual on a shard row is `2.220446049250313e-15`. The floor was not moved.

Pure pairwise controls, erasure and faces, have triadic committor spread at most `1.3877787807814457e-15`. The count above `1e-8` is 0. The spread was measured. It was not hard-coded.

Support violations, extra positive relational toggles relative to the components and the baseline, are 0 on all 100 systems. Thirty-six systems remove at least one baseline toggle. The v0.5 anchor removes 768, which matches the published v0.5 count.

## G. v0.5 prohibit-anchor reproduction

The stored representative is:

```text
dissolve(0-1) => prohibit
dissolve(2-3) | absent(0-1-2) => prohibit
```

Target id `98969a9f75232bbed2fbab25`. Geometry `contains_p_companion_edge`, polarity absent. On both directions the recomputed `Q0`, `QT`, `QP`, `QTP`, `I`, `G`, and `delta_S` differ from the published v0.5 values by 0 at the stored precision.

Path to matching:

```text
Q0 = 0.18823529411764703
QT = 0.18808717457278007
QP = 0.18765207631874303
QTP = 0.2538772345202259
I = 0.06637327774634985
G = 0.0650587226036749
Delta_S = 0.021431815558849432
```

Matching to path: `I = -0.08059720804185766`, `G = 0.08118968622132561`, `Delta_S = 0.036908902906276686`.

The other three both-prohibit canonical systems, `present(0-1-2)`, `absent(0-2-3)`, and `present(0-2-3)`, agree with this anchor to about `1e-16` on `I`, `G`, and `Delta_S`. Path source-state interaction is positive on all 192 source states. Matching source-state interaction is negative on all 48. That is the v0.5 four-way tie, reproduced inside the new experiment.

Matched controls of the anchor, path to matching:

| Control | Relation | I | G |
| --- | --- | --- | --- |
| erased `95,1045` | unconditional | 0.2705978081468282 | 0.26884815475011614 |
| face `95,1050` | disjoint | 0.013950574675887645 | -0.01336735687698365 |
| face `95,1060` | adjacent | 0.07210165820317929 | 0.0715184404042753 |

`I_abs_margin = -0.20422453040047836`. `G_margin = -0.20378943214644124`. Matching to path: erased `I = -0.3249421007460227`, `G = 0.3272749719416385`, `I_abs_margin = -0.24434489270416504`, `G_margin = -0.2460852857203129`. Control spreads on these rows sit near `1e-16`.

## H. Full target weight lattice

`I`, `G`, and `Delta_S` agree across the two geometries and both polarities. The largest absolute difference on any of those three fields, over every weight cell and both directions, is `9.992007221626409e-16`. The tables below are `contains_p_companion_edge`, polarity absent. The other three copies are the same surface at that tolerance. Rows are `w_P`. Columns are `w_T`, in the order prohibit, strong_suppress, weak_suppress, weak_favour, strong_favour.

Path to matching, `I`:

| w_P \ w_T | prohibit | strong_suppress | weak_suppress | weak_favour | strong_favour |
| --- | --- | --- | --- | --- | --- |
| prohibit | +0.06637 | +0.03837 | +0.02062 | -0.01789 | -0.02905 |
| strong_suppress | +0.03306 | +0.01973 | +0.01083 | -0.00994 | -0.01649 |
| weak_suppress | +0.01610 | +0.00979 | +0.00545 | -0.00519 | -0.00875 |
| weak_favour | -0.01076 | -0.00681 | -0.00391 | +0.00411 | +0.00730 |
| strong_favour | -0.01551 | -0.00996 | -0.00578 | +0.00636 | +0.01162 |

Path to matching, `G`:

| w_P \ w_T | prohibit | strong_suppress | weak_suppress | weak_favour | strong_favour |
| --- | --- | --- | --- | --- | --- |
| prohibit | +0.06506 | +0.03717 | +0.01947 | +0.01819 | +0.02963 |
| strong_suppress | +0.03250 | +0.01928 | +0.01043 | +0.01015 | +0.01670 |
| weak_suppress | +0.01578 | +0.00970 | +0.00543 | +0.00520 | +0.00876 |
| weak_favour | +0.01091 | +0.00685 | +0.00389 | +0.00247 | +0.00423 |
| strong_favour | +0.01566 | +0.00999 | +0.00577 | +0.00067 | +0.00503 |

Path to matching, `Delta_S`:

| w_P \ w_T | prohibit | strong_suppress | weak_suppress | weak_favour | strong_favour |
| --- | --- | --- | --- | --- | --- |
| prohibit | +0.02143 | +0.01152 | +0.00581 | +0.00349 | +0.00363 |
| strong_suppress | +0.01186 | +0.00670 | +0.00353 | +0.00247 | +0.00297 |
| weak_suppress | +0.00599 | +0.00352 | +0.00193 | +0.00153 | +0.00200 |
| weak_favour | +0.00624 | +0.00383 | +0.00214 | +0.00142 | +0.00035 |
| strong_favour | +0.01036 | +0.00652 | +0.00372 | +0.00321 | +0.00360 |

Matching to path, `I`:

| w_P \ w_T | prohibit | strong_suppress | weak_suppress | weak_favour | strong_favour |
| --- | --- | --- | --- | --- | --- |
| prohibit | -0.08060 | -0.04671 | -0.02513 | +0.02176 | +0.03494 |
| strong_suppress | -0.04092 | -0.02457 | -0.01355 | +0.01255 | +0.02070 |
| weak_suppress | -0.02019 | -0.01239 | -0.00695 | +0.00674 | +0.01135 |
| weak_favour | +0.01386 | +0.00896 | +0.00523 | -0.00578 | -0.01039 |
| strong_favour | +0.01979 | +0.01303 | +0.00773 | -0.00906 | -0.01687 |

Matching to path, `G`, changes sign inside the favour-against-suppress block. The diagonal stays positive: prohibit 0.08119, strong_suppress 0.02472, weak_suppress 0.00688, weak_favour 0.00697, strong_favour 0.02165. The minimum on this surface is -0.00869. `Delta_S` on the same diagonal is 0.03691, 0.01209, 0.00363, 0.00369, 0.01175. Eight finite cells on matching to path have negative `Delta_S`, all in the block where one weight is a suppress grade and the other is strong_favour.

The sign of `I` follows the two weights. Same-side grades, both on the suppress side of neutral or both on the favour side, keep the anchor sign: path positive, matching negative. Opposite-side grades flip both directions. All 100 systems have `|I| > 1e-8` in both directions. State-sign coherence of the target matches the sign of `I` on every row: 192 path source states of one sign, 48 matching source states of one sign.

## I. Condition-erasure controls

On the 64 finite systems, the absolute interaction of the erased control has median 0.01469 and maximum 0.05427 on path to matching, and median 0.01885 and maximum 0.06667 on matching to path. The target medians on the same rows are 0.00802 and 0.01087. At the prohibit anchor the erased absolute values are 0.27060 and 0.32494.

The erased control is a purely pairwise two-rule system. Its triadic spread is below the floor.

## J. Pair-face controls

On the same 64 finite systems the face-control absolute interaction, counting each live matched face, has median 0.00785 and maximum 0.04191 on path to matching, and median 0.01012 and maximum 0.05765 on matching to path. At the prohibit anchor the adjacent face is slightly above the target on path to matching (0.07210 against 0.06637). The disjoint face is smaller (0.01395). The present-polarity disjoint face at prohibit reaches 0.21447 on path to matching and -0.29164 on matching to path, still below the erased control and above the higher-order target.

Every live face spread is below the floor.

## K. Target versus matched-control envelope

`I_abs_margin` is negative on all 100 targets in both directions. The least negative finite value is -0.003097154503193811, on path to matching, at weak_favour / weak_favour, `contains_p_companion_edge`, present, target `9ea012b4adc2caa40ace4a2c`. The target does not meet the strongest matched control within the floor on any row.

`G_margin` is negative on all 100 path-to-matching rows and on 98 matching-to-path rows. Two finite matching-to-path rows are positive:

| Target | Weights | G | G_margin | I | I_abs_margin | Delta_S |
| --- | --- | --- | --- | --- | --- | --- |
| `4339adc7cee052575bee7a14` | weak_suppress, strong_favour, contains_t, present | 0.0016968154894350107 | 0.006676875155676942 | 0.011345223497018608 | -0.005324003063608362 | -0.004141241219820069 |
| `38bc280346bd567b780a78e5` | strong_suppress, strong_favour, contains_t, present | 0.010291427747881499 | 0.0030627945891027464 | 0.02069768567510799 | -0.008938083630182558 | -0.004565708335584118 |

Both have a negative `I_abs_margin` and a negative `Delta_S`. The positive `G_margin` is the super-singleton gap of a small target against a control whose `G` is smaller, while the control still has the larger absolute interaction. Those two rows are `contains_t_action_edge` rows, whose matched set has no disjoint face. The same weights on `contains_p_companion_edge` keep a negative `G_margin`. The largest geometry gap in `G_margin` is 0.021055861296393252, at that weak_suppress / strong_favour cell.

Margins are not a copy of the target surface. Target `I`, `G`, and `Delta_S` tie across geometry and polarity. The control sets do not. `contains_t_action_edge` is matched to fewer live faces.

## L. Hard deletion versus finite grade

Continuity ratios use the same geometry and polarity prohibit/prohibit anchor. Bins are descriptive. There is no `>= 1.00` bin.

Neither prohibit, 64 rows in each direction:

| Ratio | Path to matching | Matching to path |
| --- | --- | --- |
| R_I median (min, max) | 0.1209 (0.0589, 0.2973) | 0.1349 (0.0649, 0.3049) |
| R_G median (min, max) | 0.0970 (0.0103, 0.2963) | 0.1004 (0, 0.3044) |
| R_S median (min, max) | 0.1442 (0.0165, 0.3128) | 0.1342 (0, 0.3275) |

Path `R_I` bins: 24 below 0.10, 36 in 0.10 to 0.25, 4 in 0.25 to 0.50. Matching `R_I` bins: 20, 36, and 8 in those same bins. No finite row keeps half the anchor absolute interaction.

Exactly one prohibit sits higher. Path `R_I` bins: 12 in 0.10 to 0.25, 16 in 0.25 to 0.50, 4 in 0.50 to 1.00. Matching `R_I` bins: 8, 16, and 8.

The surface does not fall through the floor when prohibit becomes strong_suppress. On the diagonal, path `I` goes 0.06637, 0.01973, 0.00545, 0.00411, 0.01162. The step off prohibit is the largest step. The finite grades remain ordered by how far the weights sit from hard zero, and the sign flips when the two weights sit on opposite sides of neutral. That is a graded response with a deletion peak, and it is also a sign change away from the same-side quadrant.

## M. Polarity comparison

Present and absent agree on target `I`, `G`, and `Delta_S` within the floor on all 100 weight cells and both directions. Sign changes of those three fields: 0. The largest absolute target difference found while scanning polarity and geometry together is the `9.99e-16` figure above.

The control envelope is not polarity-blind. Present and absent select different face controls. The largest `G_margin` gap between present and absent is 0.017726592097540683, on `contains_t_action_edge`, matching to path, weak_suppress / strong_favour.

## N. Geometry comparison

The separation order was the Chebyshev grade index from prohibit, then `w_P`, then `w_T`. No weight cell separates the two geometries on `I`, `G`, or `Delta_S` above the floor, in either polarity or either direction. `first_separation` is null on all three fields.

The geometries separate on the margins, because their matched face sets differ. Section K records that gap. The v0.5 tie at prohibit is the same tie at every finite grade on the target observable.

## O. State-resolved specificity

Validation used the predeclared criteria, then the four both-prohibit anchors. Ten target ids. Ties kept the earliest target id at the exact maximum. A later row inside the floor was not added.

`D_state` against the erased control keeps one sign across the source class on every validated row and both directions. The top-three L1 share is about 0.02 on path to matching and about 0.13 to 0.20 on matching to path. The descriptive cut of 0.5 is not met. The difference from erasure is spread through the source class.

`D_state` against the adjacent face is mixed, and the triad-bucket means change sign, on the validated rows. The top-three share stays below 0.5, about 0.04 to 0.06 on path and about 0.25 to 0.27 on matching. The aggregate comparison with that face hides a triad-dependent sign pattern.

`D_state` against the disjoint face, where that face is matched, keeps one sign and is not concentrated on three states.

## P. Robustness validation

Probes: `rho3 = 1/2`, `rho3 = 2`, alphabet `W3`, alphabet `W16`, each compared with `W4` at `rho3 = 1`. `W3` and `W16` keep the grade names and change the base from 2 to 3 and 4. Prohibit stays 0. `rho3` rescales the baseline triad-slot weight and does not rename a grade.

On all ten rows and both directions, the sign of `I`, the sign of `I_abs_margin`, and the boolean `I_abs_margin > 1e-8` agree on every probe. The target stays below the matched envelope in absolute interaction.

The sign of `G_margin` and the sign of `Delta_S` agree on every probe for nine of the ten rows. The exception is `cabbf5e671d6f78d036341fe`, path to matching, weak_favour / strong_favour, `contains_t_action_edge`, absent. That row was selected as the largest finite path `G_margin`, and the value is negative: -0.0010281685991569145, with `Delta_S = 0.0003531889848947811`. At `W3` those become `G_margin = 0.001389091255457442` and `Delta_S = -0.0020650283179073636`. At `W16` they become 0.003467111842779008 and -0.004565960120780033. At `rho3 = 2`, `Delta_S` becomes -0.00023818801335095952 while `G_margin` stays negative. The strong_suppress diagonal and the prohibit anchors do not flip these signs. Sign stability of a margin near `1e-3` is not magnitude invariance, and it is not stability of the large cells.

## Q. Recursive design Pass 3

Asked after the lattice. A secondary family would have been one of: a broader matched `P->P` plus `P->P` census, a small `T->P` plus `T->P` family, or a second graph-class passage.

Ambiguity A does not survive. Finite-grade target interaction is above the floor and is distinguishable from the matched controls: `I_abs_margin` is negative on every row, and `Delta_S` is carried by the target while the controls are triad-flat.

Ambiguity B does not block the classification of this motif. The higher-order gate is distinct in `Delta_S`. It is not distinct by having a larger interaction than its matched pairwise controls. A second higher-order rule would ask a new question.

Ambiguity C does not materially survive. Both directions agree on the negative interaction margin, the deletion peak, the polarity and geometry tie of the target observable, and positive `Delta_S` on most finite rows. The two positive `G_margin` rows are small, matching-only, and have negative `Delta_S`.

No secondary family was run. Scores are in `docs/generation-006-design-passes.md`. They are not summed.

## R. Optional secondary control

Not run. There is no secondary experiment id.

## S. Negative findings

- No target row exceeds every matched lower-order control in `|I|`.
- Path to matching has no positive `G_margin`. The two positive matching rows do not carry a positive `Delta_S`.
- Finite grades keep less than half of the prohibit-anchor `|I|`, `G`, and positive `Delta_S`. None exceed the anchor.
- Pairwise controls are triad-independent to the floor. They do not reproduce `Delta_S`.
- The condition-erased double prohibit produces a larger `|I|` and a larger `G` than the v0.5 higher-order anchor.
- Present and absent, and the two geometries, do not separate the target observable at any finite grade.
- The small path `G_margin` and `Delta_S` on `cabbf5e671d6f78d036341fe` change sign under `W3`, `W16`, and, for `Delta_S`, under `rho3 = 2`.
- `rho` and alphabet probes cover the ten validation rows, not the whole lattice.
- Full state vectors for non-validation rows are not in the published summary.
- Cardinality 3, simplicial semantics, a second passage, a `T->P` plus `T->P` family, the broad pairwise census, and `H`, `S`, `G`, `L` above 0 were not run.

## T. Inferences

OBSERVED. The v0.5 prohibit anchor reproduces, including the four-way tie, the signs of the source-state residuals, and the support-removed count 768.

OBSERVED. All 64 finite systems have `|I| > 1e-8` in both directions. Median absolute interaction is about 0.008 on path to matching and about 0.011 on matching to path. Median continuity against the prohibit anchor is about 0.12 and 0.13. The diagonal falls from the prohibit cell through strong_suppress and weak_suppress, and it rises again on the favour diagonal without returning to the prohibit magnitude.

OBSERVED. `I_abs_margin` is negative on every system and both directions. Erasure is the larger interaction at matched weights. On the finite rows its median absolute interaction is about twice the target median. At the prohibit anchor it is about four times the target.

OBSERVED. `Delta_S` is positive on all 64 finite path rows and on 56 of 64 finite matching rows. Every matched pairwise control has triadic spread below `1e-8`. The median finite `Delta_S` is about 0.14 of the prohibit anchor.

OBSERVED. The difference from the erased control keeps one sign across the source class and is not concentrated on three states. The difference from the adjacent face changes sign with the hidden triad.

INFERRED. The three explanations split across different observables. Hard deletion accounts for the peak magnitude: the prohibit cell is the extreme of the same-side quadrant, and finite grades hold a fraction of it. Generic composition accounts for `I` and `G`: a matched system with the gate removed, or with the gate replaced by a pair face, produces an interaction at least as large. Higher-order conditioning accounts for `Delta_S`: the hidden triadic configuration moves the controlled committor only when a rule reads a triad. The higher-order gate does not add a larger non-additivity than the matched pairwise composition. It adds triad selectivity, and it reduces the interaction relative to deleting the gate.

The two positive `G_margin` rows do not pull that inference back. They are small, they have negative `Delta_S`, and they still lose on `|I|`.

## U. RS / global-coherence interpretation

This cell does not establish a globally coherent architecture, and it does not assign a meaning to a triad.

What it supports is narrower. On this passage, composing two dissolution weights is a non-additive operation whether or not one of the rules is gated by a triad. Removing the triad gate, and leaving the same two actions and the same two weights, increases the absolute interaction. Keeping the gate makes the passage depend on which of the 16 triadic configurations is hidden. That split is coherent with treating ordinary constraint composition and higher-order selectivity as different pieces of work. It tensions with reading the v0.5 prohibit motif as evidence that a higher-order condition creates a new kind of non-additivity. The larger non-additivity, at these matched weights, is the pairwise deletion. A calculated split of this kind is not a design conclusion.

## V. Recursive design Pass 4 and next experiment

Pass 4 is in the design-pass note. The chosen next step is to stop this motif. The coordinates that carry that choice are CI, IN, and CB: the three explanations are already separated on this passage, the lattice is readable, and another family would change the question. A second graph-class passage remains the deferred fork with the best remaining resistance to the passage confound. It is not run in this branch. `H`, `S`, `G`, `L`, a larger `N`, and simplicial semantics stay unused.

## Questions this generation was asked

1. The v0.5 prohibit/prohibit anchor reproduces. Stored gaps on `Q0`, `QT`, `QP`, `QTP`, `I`, `G`, and `Delta_S` are 0. The four-way tie survives.
2. Canonical target systems in the 5 by 5 lattice: 100. Labelled targets: 1,200.
3. Unique canonical condition-erased controls: 15. Distinct labelled erased controls: 150.
4. Unique canonical pair-face controls: 100. Distinct labelled live face controls: 1,500.
5. Rows with neither weight prohibit: 64.
6. Among those 64, `|I| > 1e-8` on 64 path-to-matching rows and 64 matching-to-path rows.
7. `G > 1e-8` on 64 and 52.
8. `Delta_S > 1e-8` on 64 and 56.
9. Finite continuity against the same-geometry, same-polarity anchor has median `R_I` 0.121 and 0.135, median `R_G` 0.097 and 0.100, median `R_S` 0.144 and 0.134. Maxima are about 0.30 to 0.33. No finite row is at or above half of the anchor on `R_I`.
10. The interaction falls as the grades leave prohibit, stays above the floor, changes sign when the two weights are on opposite sides of neutral, and does not jump from the prohibit value to numerical zero at the first finite grade.
11. Present and absent stay equivalent on target `I`, `G`, and `Delta_S` at every weight, within the floor. Their control margins do not.
12. The two geometries stay equivalent on those same three target fields at every weight. Their control margins do not. No target-field separation exceeds the floor, so there is no first separating weight.
13. Finite erased `|I|` has median 0.01469 and 0.01885, and maximum 0.05427 and 0.06667. The prohibit erased values are 0.27060 and 0.32494.
14. Finite face `|I|` has median 0.00785 and 0.01012, and maximum 0.04191 and 0.05765.
15. Rows on which the target exceeds every matched control in `|I|`: 0 in each direction, out of 100.
16. Rows on which it exceeds every matched control in `G`: 0 path to matching, 2 matching to path. Both of those have negative `I_abs_margin` and negative `Delta_S`.
17. Pure pairwise controls are triad-independent to the floor. The maximum measured spread is `1.3877787807814457e-15`. The count above `1e-8` is 0.
18. The largest finite `I_abs_margin` is still negative: -0.003097154503193811, path to matching, `9ea012b4adc2caa40ace4a2c`, weak_favour / weak_favour, present, `contains_p_companion_edge`. Matching to path: -0.004542725497151734, `72fb0dd6436edb2c4dec3589`, weak_favour / weak_favour, absent, `contains_t_action_edge`.
19. The largest finite `G_margin` on path to matching is negative: -0.0010281685991569145, `cabbf5e671d6f78d036341fe`. On matching to path the largest is 0.006676875155676942, `4339adc7cee052575bee7a14`.
20. The largest finite `Delta_S` is 0.006704429091300035 on path to matching, `0c3a06c23760029b1ebfe901`, and 0.012088104816016632 on matching to path, `9800da07eb2f1d48cdbc5a17`. Both are strong_suppress / strong_suppress. The two geometries at that weight agree to numerical noise, so each direction's winner is the earliest target id.
21. `I` sign, `I_abs_margin` sign, and the failure to exceed the controls survive every rho and alphabet probe on the ten validation rows. `G_margin` sign and `Delta_S` sign survive on nine rows. They flip on the small path cell named in question 19.
22. Target-versus-erasure differences keep one sign across the source class and are not concentrated on three states. Target-versus-adjacent-face differences change sign by hidden triad and are also not concentrated on three states.
23. The condition-erased double prohibit reproduces, and exceeds, the v0.5 absolute interaction and the super-singleton gap without a higher-order gate. It does not reproduce `Delta_S`. No matched lower-order control carries a triadic spread above the floor.
24. The evidence is a mixture. Deletion accounts for the peak. Generic composition accounts for `I` and `G`. Higher-order gating accounts for `Delta_S`. No one of the three accounts for all three observables.
25. A secondary control family is not required.
26. The smallest justified next step is to stop this motif. A second graph-class passage is the deferred fork. It is not part of this branch.
