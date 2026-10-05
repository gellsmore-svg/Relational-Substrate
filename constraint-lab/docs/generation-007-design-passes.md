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
