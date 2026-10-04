# Generation 006 design passes

These vectors are ordinal design-selection scores on a `0–5` scale. Higher is better. They are not empirical facts, probabilities, or a confidence score. They are not summed.

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

The question being designed for is whether the strong v0.5 two-rule effect is a hard deletion, a generic nonlinear composition of two constraints, or a specifically higher-order-conditioned interaction. Those three explanations stay separate.

## Pass 1 — before implementation

Written before the Generation 6 catalogue and before the experiment runner. Counts and runtimes below are expectations, not measurements.

### External vector

| Candidate | CI | CF | CB | IN | IG | CR | PR |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Full 85,175 pair census | 2 | 2 | 1 | 2 | 3 | 2 | 4 |
| Only weaken the v0.5 prohibit motif | 4 | 3 | 5 | 5 | 4 | 3 | 5 |
| Target motif + condition-erasure + pair-face controls | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| Broad matched P->P + P->P control census | 4 | 4 | 4 | 4 | 5 | 4 | 5 |
| T->P + T->P control family | 4 | 3 | 4 | 4 | 4 | 3 | 5 |
| Add a second graph-class passage now | 3 | 4 | 4 | 4 | 4 | 3 | 5 |
| Switch to simplicial semantics now | 2 | 2 | 3 | 3 | 5 | 1 | 5 |

### Grok vector

Assigned independently. Disagreements are explained under the table. They are not averaged with the external vector.

| Candidate | CI | CF | CB | IN | IG | CR | PR |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Full 85,175 pair census | 2 | 1 | 2 | 2 | 3 | 2 | 4 |
| Only weaken the v0.5 prohibit motif | 3 | 2 | 5 | 5 | 3 | 2 | 5 |
| Target motif + condition-erasure + pair-face controls | 5 | 4 | 5 | 5 | 5 | 4 | 5 |
| Broad matched P->P + P->P control census | 3 | 3 | 3 | 3 | 4 | 3 | 5 |
| T->P + T->P control family | 3 | 2 | 4 | 4 | 3 | 3 | 5 |
| Add a second graph-class passage now | 3 | 4 | 4 | 4 | 3 | 2 | 5 |
| Switch to simplicial semantics now | 2 | 1 | 3 | 2 | 4 | 1 | 4 |

### Disagreements

The full census is computable with the block solver. v0.5 analysed 2,304 pairs in about five minutes. A thirty-fold increase is heavy and still bounded, so CB is 2 rather than 1. It has no matched control for the motif, so CF is 1 rather than 2.

Weakening the prohibit motif without a lower-order control answers deletion versus finite grade. It does not answer whether a finite-grade residual is higher-order-specific. Review 005 is explicit that `I != 0` is not unique to a triadic gate. CI, CF, IG, and CR are therefore one step lower than the external vector.

The selected design still isolates the gate while holding action edges and weights fixed. CF is 4 rather than 5 because the grammar excludes a condition on a rule's own action slot. A pair-face that is the acted edge cannot be a live gate: `present` on that edge collapses toward the unconditional rule, and `absent` on that edge is contradictory with dissolution. That is a fairness fact about one face, not a reason to abandon the design. CR is 4 rather than 5 because the passage is still only path versus matching. A result that is special to that pair of graphs would not be visible inside this round.

A broad pairwise census is not locally matched to the target edges and weights unless it is built that way. Doing it now spends interpretability on a population the matched faces may already cover. A `T->P` plus `T->P` family answers a later ambiguity, whether any second higher-order rule would do this, and it is not a lower-order control. A second passage reuses kernels but changes the question being isolated. Simplicial semantics changes the event model, so its committor is not the v0.5 observable. CF is 1 for that reason.

### What drove the selection

The selected primary design is the target motif plus condition erasure plus pair-face controls.

The coordinates that carry the choice are CI and IG. No other candidate holds the actions and the weights fixed while removing only the gate, and no other candidate can separate deletion, generic composition, and higher-order selectivity in one lattice. CB, IN, and PR are also at the top of the scale. CF and CR are not perfect, and those limits are part of the design record rather than a reason to switch.

Rejected for this round, and not because they are uninteresting:

- The full cardinality-2 census does not match controls to the motif.
- Weakening the prohibit weights alone leaves the nonlinear-composition confound in place.
- A broad pairwise census and a two-triad family answer questions that are not yet the live ambiguity.
- A second passage and simplicial semantics each change a variable this round is trying to hold still.

### Factual uncertainties that can change a coordinate

- The exact canonical counts, and therefore CB, are not yet measured.
- If face substitution collapses so far that adjacent and disjoint pair gates are not both populated, CF and CR fall.
- If condition erasure identifies `(w_P, w_T)` with `(w_T, w_P)` under `S4`, several targets share one control. That is a deduplication to record. It lowers CF only if the shared control is then compared as though the weight assignment were still ordered.
- State-resolved storage could change CB if it is attached to every row rather than to the predeclared validation rows.
- The effect floor is not re-litigated in this pass. A later numerical preflight can keep or replace `1e-8` before the census. It does not by itself change the design choice.

Pass 1 is not rewritten by later passes.

## Pass 2 — after exact preflight

Written after the exact catalogue and a two-row in-process benchmark. Pass 1 above is unchanged.

### Measurements

Catalogue sha256:

```text
60a80a31dacb92798c2e9f1ed1a846666b21f5eb8ffdf8934c6708689f5cfd7f
```

Labelled targets are 1,200. That is 3 matchings × 2 orientations × 4 triads × 2 polarities × 25 weight cells. Orbit accounting closes: 100 canonical targets × orbit size 12 = 1,200. Canonical structural targets are 4. Every canonical target has orbit size 12. The stabilizer has order 2. Equal weights do not enlarge the orbit, because the two rules stay structurally distinct.

Distinct labelled condition-erased controls, counted before `S4` as constraint-key pairs, are 150. Canonical erased controls are 15. Ten erased ids are shared by a swapped unequal weight pair. `I` is symmetric in the two rules, so that swap does not change `I` or `G`. The row records `erased_weight_role = assigned_by_weight_not_by_listing_order` and whether the id is shared. The shared control is not compared as if the listing order had stayed fixed.

Labelled face attempts are 3,600. Labelled live faces are 3,000. Distinct labelled live face controls are 1,500. Canonical face controls are 100. Same-as-action `present` collapses number 300. Same-as-action `absent` unsatisfiable literals number 300. Within-target face deduplications number 100. A live face equal to its erasure control numbers 0. Invalid structurally simple pairs number 0.

Deletion classes on the 100 canonical targets: both prohibit 4, exactly one prohibit 32, neither prohibit 64. Missing geometry × polarity × weight cells: 0. Each of the 100 cells has exactly one canonical system.

Live face relations on those canonical records: adjacent 200, disjoint 50. Non-live statuses: `redundant_collapse_to_erasure` 25, `unsatisfiable_absent_on_action` 25.

Control 3 is not added. The face catalogue spans adjacent and disjoint as relation categories. Same-as-action appears only as a recorded collapse or an unsatisfiable literal.

One matching limit is recorded and is not repaired by a wider grammar. A `contains_t_action_edge` target is matched to condition erasure plus one adjacent face. Its same-as-action face collapses or is unsatisfiable. A triad that contains the acted edge has no face disjoint from that edge. The disjoint gate at the same weights is a face control of the other geometry. It is not attached to the `contains_t_action_edge` rows.

The canonical target pool is 100. That is below the v0.5 census of 2,304 and below the execution ceiling of 600.

Numerical preflight kept `1e-8`. The worst reference gap is `3.397282455352979e-14`, below `1e-10`. The floor rule does not use scientific magnitudes. The six reference systems and the gap list are in `experiments/specs/generation-006.json`. The anchor-versus-published interaction gap is a reproduction check and is not an input to the floor.

The in-process benchmark times the anchor and the next catalogue row on one cache and discards the science values. Cold row: 1.296 seconds. Warm row: 1.023 seconds. Sample solver residual: `1.6653345369377348e-15`. The serial estimate from the warm row is about 102 seconds. The serial upper bound from the cold row is about 130 seconds. The shard budget is 10 items, so the plan has 10 shards. Workers stay at 2. Each worker rebuilds the catalogue, so wall time can exceed half of the serial estimate. The pool is still a small targeted run.

### Vectors

Old vector for the selected design, from Pass 1:

```text
CI 5, CF 4, CB 5, IN 5, IG 5, CR 4, PR 5
```

New vector:

```text
CI 5, CF 4, CB 5, IN 5, IG 5, CR 4, PR 5
```

### Why each checked coordinate stays

CB stays 5. One hundred canonical targets and a serial estimate near two minutes, with two workers, is a small bounded experiment. It is not the 2,304-pair census and not the full cardinality-2 grammar.

CF stays 4. Adjacent and disjoint live gates are both populated. Same-as-action collapses as the grammar requires. Swapped-weight erasure is recorded, and roles are assigned by weight. `contains_t_action_edge` rows do not receive a disjoint matched control, because that relation is not a face of their triad. That limit is the reason CF remains 4.

CR stays 4. The passage is still path versus matching. The counts do not add a second passage.

CI, IN, IG, and PR were not claims about counts or runtime. They stay as written in Pass 1.

### Decision

The selected design is unchanged: the target motif, condition erasure, and pair-face controls. Control 3 is not added. No coordinate changed.

## Pass 3 — after the primary lattice

Written after the 100-target run. Passes 1 and 2 are unchanged. The run finished in 96.0 seconds of wall clock, with 0 failed shards and 0 quarantined shards. That clock is a measurement. It is not a reason to start another family.

The primary result splits the three explanations. Finite-grade `|I|` stays above the floor and stays below every row's matched control envelope. `Delta_S` stays on the target. Pairwise controls are triad-flat. The prohibit cell is the magnitude peak and is smaller than its own condition-erased control.

### Ambiguities

Ambiguity A does not survive. The finite-grade target is distinguishable from its face gates and from erasure: the interaction margin is negative on every row, and the triad spread is carried by the target.

Ambiguity B does not block this classification. The higher-order gate is distinct where `Delta_S` is concerned. It is not distinct by producing a larger interaction than the matched pairwise systems. A second higher-order rule would open a new question.

Ambiguity C does not materially survive. Both passage directions agree on the negative interaction margin, the deletion peak, and positive `Delta_S` on most finite rows. Two small matching-to-path `G_margin` values are positive and have negative `Delta_S`.

### Scores for the candidate secondary families

| Candidate | CI | CF | CB | IN | IG | CR | PR |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Broader matched P->P + P->P census | 2 | 2 | 3 | 2 | 2 | 2 | 5 |
| Small T->P + T->P family | 3 | 2 | 4 | 3 | 3 | 3 | 5 |
| Second graph-class passage | 4 | 4 | 4 | 4 | 3 | 4 | 5 |

The broader census loses IG because the matched erasure and the matched faces already show that ordinary composition produces the interaction. A second higher-order family would ask whether any other triad gate also carries `Delta_S`. That is a new isolation, and CF is 2 because it is not the same action pair. The second passage holds the motif still and changes the graphs. Its IG is 3 because the two directions of the present passage already agree, so the passage confound is not what the result is hanging on.

### Decision

No secondary family is executed. There is no second experiment id.

## Pass 4 — final next-step selection

Written after Pass 3. The candidates are ways to continue, or to stop. Interesting structure is not a reason to add a channel.

| Candidate | CI | CF | CB | IN | IG | CR | PR |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Stop this motif | 5 | 5 | 5 | 5 | 4 | 4 | 5 |
| Second graph-class passage, later | 4 | 4 | 4 | 4 | 3 | 4 | 5 |
| Small T->P + T->P family, later | 3 | 2 | 4 | 3 | 3 | 3 | 5 |
| Broad P->P + P->P census | 2 | 2 | 3 | 2 | 2 | 2 | 5 |
| Simplicial semantics | 1 | 1 | 3 | 2 | 2 | 1 | 5 |
| Add H, S, G, L, or a larger N | 1 | 1 | 2 | 2 | 1 | 1 | 4 |

### What drove the choice

The chosen next step is to stop this motif.

CI, IN, and CB carry that choice. The lattice already separates deletion, generic composition, and higher-order selectivity on this passage, the split is readable without a new grammar, and another run would spend a bounded budget on a question this one has answered. IG of stopping is 4 rather than 5 because a second passage could still move the passage confound. CR of stopping is 4 because the claim is about path versus matching. That limit is stated in the report. It is not repaired by adding history, geometry, entity state, meta-constraints, simplicial face closure, or a larger `N`.

### Why the other forks stay deferred

The second passage is the strongest deferred fork. It would keep the graded motif and the matched controls, and it would change the graphs. Both directions of the present passage already agree, so the fork does not have to run in order to classify this result.

A `T->P` plus `T->P` family would ask whether triad selectivity appears for a second higher-order rule. The present evidence already locates selectivity on the one gate that reads a triad. A broad pairwise census would leave the matched edges. Simplicial semantics would change the event. Extra channels and a larger `N` would change the ontology in response to a weak interaction margin, which is the move this round refuses.
