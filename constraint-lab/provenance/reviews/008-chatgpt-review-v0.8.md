# External review 008 — ChatGPT review of v0.8

This file records the scope and conclusions of an external ChatGPT review of `research/constraint-lab-v0.8-exploration` at `f5c0b6d1c8aae7b467066a4b3b5974ea2a0f59c9`.

The review is external to the v0.8 implementation. It is not a line-by-line audit of every durable item. Generation 8 remains historical evidence for the trajectories that were actually run. This review does not rewrite Generation 8 plans, journey records, trajectory reports, synthesis, or execution provenance. It qualifies one hidden-context conclusion. It does not erase the runs.

## What was inspected

The external review inspected:

- branch history;
- frozen Round 0, Round 1, and Round 2 plan chronology;
- trajectory reports;
- the exploration synthesis;
- the journey ledger;
- the execution record;
- the event and replay implementation;
- hidden-context orbit construction;
- atlas aggregation;
- the test suite;
- final-head CI.

## Operational conclusions

The micro-batch trajectory platform is accepted.

Round 0:

```text
4,160 episodes
4,576 durable items
39 batches
416 exact replay checks
3,623,976 full events
2,129,920 pair events
```

Round 1:

```text
1,664 episodes
1,831 durable items
16 batches
167 exact replay checks
1,425,781 full events
851,968 pair events
```

Round 2:

```text
1,664 episodes
1,831 durable items
16 batches
167 exact replay checks
1,400,613 full events
851,968 pair events
```

Totals:

```text
7,488 trajectories
8,238 durable items
71 batches
750 replay checks
~6.45 million full events
~3.83 million pair events
0 timeouts
0 retries
0 quarantines
```

The three episode counts sum to 7,488. The three item counts sum to 8,238. The three batch counts sum to 71. The three replay counts sum to 750. Full events sum to 6,450,370. Pair events sum to 3,833,856. Execution 008 records the same per-round counts, and `verify --require-complete` returned `ok` and `complete` on each round root.

Every episode ended at the pair horizon. There were 0 `full_event_cap` endings and 0 `no_admissible_event` endings. Replay mismatches were 0.

Final-head GitHub Actions run:

```text
38295390458
```

on:

```text
f5c0b6d1c8aae7b467066a4b3b5974ea2a0f59c9
```

The URL is `https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/38295390458`. Jobs `constraint-lab` and `books` both completed with conclusion `success`. This review is the record of that final-head run. The preceding synthesis commit `a9d35503f86521b4e8046a03b9a6250143594dc3` has Actions run `38294927720`, recorded in Execution 008. That line is not a run id for the close-out commit. Do not add a further commit whose only purpose is to restate `38295390458`.

Local suite, recorded in Execution 008 after the synthesis commit:

```text
148 passed
```

That suite includes the Generation 8 replay, orbit, and frozen-plan tests and the prior platform tests. It does not re-run the trajectory atlas.

Frozen plan commits, each pushed before the round that names it:

```text
Round 0  0a9e74f287b3ecb24efd3981b9562e53086ffee9
Round 1  509e80fbb5b472d8da61ba7ba85fcedba15939c1
Round 2  93253e2d249a6f44ace3e7c63ce42306404fa401
```

Result commits descend from those plans: Round 0 `2b1778306f08e556df195d735e482c8b3533d796`, Round 1 `7b7dc28b4631f1d2a675b7a43135da2d6d06ead4`, Round 2 `8bf0b9f13bba194089141c54c10eb9e73084ae1f`.

## Methodological success

Generation 8 successfully changed inquiry mode. It is Mode B, open relational exploration. A completed trajectory has no scientific pass or fail. The scientific object is the fully replayable stochastic trajectory.

Round 0 did not reveal a large hidden-triad routing split. The atlas exposed an unexpected organising coordinate:

```text
edge-count occupancy
```

with a comparatively stable 3-edge layer near:

```text
0.314
```

while finite constraints shifted occupancy between:

```text
sparse side = 0, 1, 2 edges
dense side = 4, 5, 6 edges
```

Round 1 followed that observation by separating the composite system and reversing finite grades. Round 2 then filled the intermediate grades and observed an ordered progression. Round 3 was left unopened after that progression was visible.

This is a valid example of:

```text
exploration → observation → revised exploration
```

rather than hypothesis rescue. That methodological conclusion stands.

## Reliable trajectory observations

The following remain valid observations about the trajectories that were actually run.

### Finite-grade ordering

For the S01 conditional dissolve rule, dense minus sparse:

```text
strong_suppress  dense-sparse ≈ +0.0645
weak_suppress                    +0.0389
baseline                         +0.0061
weak_favour                      -0.0429
strong_favour                    -0.0841
```

The published synthesis records the same four grades on the S01 expression as +0.0645, +0.0389, −0.0429, −0.0841, with baseline S00 at +0.0061.

### Unconditional reversal

The unconditional dissolve rule moved approximately:

```text
strong_suppress  +0.1684
strong_favour    -0.1396
```

on the same dense-minus-sparse coordinate. Those are S10 and S16 in the published atlas.

### Visible-source routing

Within the sampled starts:

```text
path tends to split between star and triangle
star tends to route through path
triangle tends to route through path
```

This is consistent with labelled-graph multiplicities:

```text
3-edge path: 12 labelled realisations
star:         4
triangle:     4
```

That multiplicity is an important structural comparator. It is not asserted as the only explanation.

### Composite system

S09 shifted occupancy more strongly than either component. The published residual of S09 against the sum of the separate S10 and S11 deviations from S00 is L1 0.0698. The residual against simple addition was non-zero. S09 did not create a qualitatively private route family in Generation 8.

## Context-construction flaw

Generation 8 reduced the 16 triad configurations under:

```text
Aut(visible source graph)
```

before trajectory execution.

`enumerate_hidden_contexts` builds orbits with `pair_automorphisms` of the labelled source pair mask, then executes the canonical member of each orbit. The resulting execution basis is 8 star orbits, 10 path orbits, and 8 triangle orbits: 26 starts, not 48 raw starts. The start state is the source mask with the orbit's canonical triad in the high four bits.

That reduction is valid only when the active dynamics are invariant under those same automorphisms.

For baseline dynamics, the unconstrained toggle kernel has no labelled rule, so the source-graph automorphisms preserve the dynamics.

For a labelled constraint such as:

```text
dissolve(0-1) | absent(0-1-2) => strong_suppress
```

some automorphisms of the visible graph move the action edge, the conditioning triad, or both. Those permutations do not preserve the constraint system.

Thus two starts can be equivalent under the visible graph and inequivalent under the visible graph together with the active rule system. Generation 8 nevertheless represented both by one canonical context orbit. That is a genuine sampling flaw for hidden-context analysis.

## Consequence of the flaw

The trajectories are not discarded. The edge-count occupancy axis, the finite-grade ordering, the suppress/favour reversals, the composite-system occupancy observation, and the source-class routing patterns remain observations about the trajectories that were run.

Generation 8 statements such as:

```text
initial hidden context has only a small effect
maximum context information is ~0.06 nats
hidden context is broadly routing-insensitive
```

are provisional under the Generation 8 graph-only orbit basis. The published largest episode-equal figures are 0.0631 nats in Round 0, 0.0485 nats in Round 1, and 0.0437 nats in Round 2. Those numbers describe the orbits that were executed. Some dynamically distinct raw triad starts were not separately executed, so those numbers do not yet describe the uniform raw-triad measure.

The trajectory engine, the RNG, event logging, replay, and the constraint semantics were not shown to be wrong. The flaw is in which initial contexts were treated as symmetry-equivalent.

## What this review does not withdraw

The platform, the frozen-plan chronology, the replay checks, and the occupancy and routing observations listed above stay in force. Generation 8 did change the question from coefficient fitting to replayable trajectories, and the atlas did find the edge-count coordinate by following the data. Those are not undone by the context-sampling qualification.

## Prompt 008 authored metadata

The following metadata is externally verified and is not assigned to the stored agent input. The two byte strings are distinct. The authored file is not in this working environment, so no byte comparison was performed.

```text
authored bytes: 41,865
authored sha256: 4cc6f5597a3d26ec3378a14af72e8d9efee25d26c7646839228f02edade1af98
authored_prompt_status: externally_verified_pending_import
relationship: unknown

stored Grok agent input:
  path: constraint-lab/provenance/prompts/008-v0.8-agent-input.md
  bytes: 41,862
  sha256: b4e73a9b3f43d80dbe3f9e1d8b63ae28107dd7a1928ed172a391eb1036cba065
```

The original Prompt 008 ledger line is left unchanged, including its null authored hash. A later ledger line records this external verification. Prompt 007, Prompt 007R, and Prompt 007B are not overwritten.
