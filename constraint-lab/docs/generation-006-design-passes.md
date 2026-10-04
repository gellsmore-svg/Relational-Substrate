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
