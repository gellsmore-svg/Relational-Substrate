# Generation 008 — exploration synthesis

Generation 8 is Mode B, open relational exploration. Rounds 0, 1, and 2 were executed. Round 3 was left unopened after Round 2, because the four finite grades on the inspected dissolve rule were ordered and `strong_favour` reversed both the unconditional dissolve and the off-edge conditional dissolve.

A completed trajectory has no scientific pass or fail. The primary object is the replayable event stream. The numbers below are summaries of those streams. Raw trajectories stay in gitignored `constraint-lab/generated/generation-008/`.

## Rounds

| Round | Frozen plan | Result commit | Episodes | Systems |
| --- | --- | --- | --- | --- |
| 0 | `0a9e74f287b3ecb24efd3981b9562e53086ffee9` | `2b1778306f08e556df195d735e482c8b3533d796` | 4,160 | S00–S09 |
| 1 | `509e80fbb5b472d8da61ba7ba85fcedba15939c1` | `7b7dc28b4631f1d2a675b7a43135da2d6d06ead4` | 1,664 | S10–S13 |
| 2 | `93253e2d249a6f44ace3e7c63ce42306404fa401` | `8bf0b9f13bba194089141c54c10eb9e73084ae1f` | 1,664 | S14–S17 |

The Round 2 result commit is the atlas report. This file does not contain the close-out commit.

Ontology, fixed for the generation: N=4, O=3, G=S=H=L=0, independent hypergraph, 6 pair bits, 4 triad bits, 1024 states, 11 pair-graph classes. Starts: 8 star orbits, 10 path orbits, 8 triangle orbits, 26 hidden-context starts, 16 replicates, horizon 512 pair events, cap 16,384 full events.

## OBSERVATIONS

### What recurred

Every episode in all three rounds ended at `pair_horizon`. Counts: 4,160, then 1,664, then 1,664. There were 0 `full_event_cap` endings and 0 `no_admissible_event` endings. Every episode reached another 3-edge class inside the horizon. Replay samples were exact: 416, 167, and 167.

Every pair toggle changes the edge count by one, and the 11 isomorphism classes are partitioned by edge count, so every pair event changes class. The transition diagonal is 0. Initial source residence is 1. A full episode is 513 pair-class runs of length 1, and 512 transition markers.

The 3-edge layer stays near 0.314 of pair-epochs on every system from S00 through S17. The share that moves is the sparse side (0–2 edges) against the dense side (4–6 edges).

Baseline S00 occupancy is close to the share of the 64 labelled pair masks (L1 0.0098). The small remainder matches the parity of starting on a 3-edge graph and taking 513 epochs.

Mean pair-class entropy stays near 2.10–2.14. `log(11)` is about 2.398. Mean full-state entropy stays near 6.02–6.14. `log(1024)` is about 6.931. Mean distinct pair classes stay near 11. Full route signatures of length 513 did not repeat inside a round, so medoid and rare-route selectors are lexicographic tie-breaks.

Length-2 and length-3 motifs are adjacent edge-count steps. Which boundary is most frequent follows where the occupancy sits. Round 0's pooled top pair was `e4-deg3221` with `e5-deg3322`. Round 2's pooled top pair was `e2-deg2110` with `e1-deg1100`, in a round whose systems sit on the sparse side of the baseline. The systems share those motifs. A system did not keep a private route.

### The edge-count layer

Dense minus sparse, pair-epoch shares:

| System | What it is | Dense − sparse | L1 to S00 |
| --- | --- | --- | --- |
| S09 | both S10 and S11 rules, `strong_suppress` | +0.2399 | 0.2565 |
| S10 | unconditional `dissolve(0-1)`, `strong_suppress` | +0.1684 | 0.1660 |
| S13 | `form(0-1) \| absent(0-1-2)`, `strong_favour` | +0.0890 | 0.0864 |
| S11 | `dissolve(2-3) \| present(0-1-2)`, `strong_suppress` | +0.0697 | 0.0672 |
| S01 | `dissolve(0-1) \| absent(0-1-2)`, `strong_suppress` | +0.0645 | 0.0598 |
| S14 | same expression, `weak_suppress` | +0.0389 | 0.0365 |
| S00 | baseline relational dynamics | +0.0061 | 0 |
| S15 | same expression, `weak_favour` | −0.0429 | 0.0518 |
| S05 | `form(0-1) \| absent(0-1-2)`, `strong_suppress` | −0.0617 | 0.0717 |
| S12 | S01 expression, `strong_favour` | −0.0841 | 0.0926 |
| S17 | S11 expression, `strong_favour` | −0.0851 | 0.0945 |
| S16 | unconditional `dissolve(0-1)`, `strong_favour` | −0.1396 | 0.1492 |

S01 through S04, four placements of conditional dissolve suppression, have occupancy L1 0.0108 between the extremes of that group. S05 through S08 move the other way. S11 against S01 is L1 0.0083. S17 against S12 is L1 0.0060.

S09 against the sum of the separate S10 and S11 deviations from S00 has L1 0.0698.

The four grades on the S01 expression are strictly ordered: +0.0645, +0.0389, −0.0429, −0.0841.

### Routing

From a path start the first other 3-edge class splits between star and triangle. From a star or a triangle the first other 3-edge class is usually the path. Round 0 pooled baseline: path 82 star / 78 triangle, star 90 path / 38 triangle, triangle 86 path / 42 star. Later rounds stay in that shape. The loosest star split in Round 1 was S13, 78 path / 50 triangle, still path-majority. Round 2 path splits stay between 73 and 87 on each side.

Return before another 3-edge class is common from a path start (about 0.54 to 0.68 in Round 0, and 0.863 under S16) and uncommon from a star or triangle start (about 0.15 to 0.30). Mean waits are about 9 to 11 pair events from a path and about 4 from a star or triangle. Path source-return counts are about 95 to 103 per episode in Round 0. Star and triangle returns are about 26 to 34. Round 2 mean source returns, pooled over sources, sit near 57.

### Hidden context

Episode-equal information of the initial hidden-context orbit about the first 3-edge destination:

| Round | Largest cell |
| --- | --- |
| 0 | 0.0631 nats (S08 triangle); weighted maximum 0.0710 |
| 1 | 0.0485 nats (S13 path); weighted 0.0536 |
| 2 | 0.0437 nats (S17 path); weighted 0.0523 |

`log 2` is about 0.693 nats. The largest Jensen-Shannon divergence between two orbits was 0.1687 in Round 0 (S08 path) and 0.1308 in Round 2 (S15 path and S17 path). Mean divergences are near 0.02 to 0.04.

One Round 0 cell, S08 `star-o00`, sent 16 of 16 episodes to the path. Other S08 star orbits sent 10 to 12. Baseline star orbits sent 9 to 13. That cell was not re-sampled.

The checkpoint series of first-destination information is 0 at 1 pair event, because one pair toggle cannot land on another 3-edge class. It reaches the horizon value by epoch 32 to 64, once every episode has a destination. Early checkpoints still include `censored_at_horizon` as an outcome, and the largest Round 2 cell at epoch 2 is 0.110 nats.

In Round 0, conditional on the current pair class and weighted by pair events, mutual information of the current triad configuration with the next pair class is 0.00049 nats on S00 and 0.00519 nats on S09. Mutual information of the initial orbit, given only the current pair class, stays near 0.001 nat on every Round 0 system. Rounds 1 and 2 did not recompute that conditional. Given the full state, the initial orbit has no further effect on the next draw. These conditionals are given only the pair class.

## INFERENCES

The atlas is organised by an edge-count oscillation whose stationary weight is close to the number of labelled graphs in each class. A finite constraint weight shifts mass between the sparse side and the dense side and leaves the 3-edge layer in place.

On one structural dissolve rule the four finite grades are ordered along that shift. The sign of a strong grade reverses the direction. `strong_favour` on dissolve sits near `strong_suppress` on the matched form rule (S12 against S05, L1 0.0239), and `strong_favour` on form sits near `strong_suppress` on dissolve (S13 against S01, L1 0.0266). The weak grades are shorter steps on the same line, one on each side of the baseline.

An unconditional pair rule moves the layer more than one conditional triad-to-pair rule. Putting both of S09's rules together moves it further, in the same direction as the sum of the separate deviations, and the residual L1 is 0.0698, so the combination is not that sum.

Which edge the condition names, and whether the condition is present or absent, is a finer occupancy difference than the grade. That fineness appears at both ends: S11 against S01, and S17 against S12.

The initial hidden triad, reduced under the source graph's automorphism group, does not choose the next 3-edge class at a large information scale in these samples. The visible source class does organise that first step: the path splits, and the star and the triangle go to the path. That source pattern is stable across the palettes that were run.

S08 `star-o00` remains a 16-episode observation at the edge of the baseline band. It is not a settled dependence, and it was not used as a reason to add systems.

## Context-sensitive and context-insensitive

Context-insensitive, across these rounds and this horizon: termination at the pair horizon, a zero transition diagonal, visitation of essentially all 11 pair classes, a 3-edge layer near 0.314, and a first 3-edge destination that follows the source class.

Sensitive to the constraint: the sparse/dense balance, the five-edge share, the number of triad events before the 512th pair event, and the path-start return-before rate, which rose to 0.863 under unconditional `strong_favour`.

Sensitive to hidden context only as a small distributional difference. The information figures above are the record. They do not by themselves identify a cause.

## Route families and motifs

The recurrent route is an edge-count step: the pair graph moves to a neighbouring edge count, and the class name is whichever isomorphism class sits at that count. The path class is the large 3-edge class (12 labelled graphs). The star and the triangle are the small ones (4 each). Returns to the source class are common from the path and less common from the star and the triangle. Those returns are stored as return counts. The trajectory engine does not label them as repair.

## Structural equivalences, as descriptions

These are readings of the L1 figures, not proved identities.

- Opposite strong grades on a matched dissolve/form pair point the layer in opposite directions and land near each other across that match.
- The four conditional placements inside one polarity are closer to each other than any of them is to the baseline.
- An off-edge present-conditioned dissolve tracks the absent-adjacent dissolve at `strong_suppress` and at `strong_favour`.
- `weak_favour` on the S01 rule is near `strong_suppress` on the matched form rule (L1 0.0214) and is also between the baseline and `strong_favour` on the layer coordinate.

## Surprising absences

The hidden-triad orbits did not split the next 3-edge destination into a large, repeatable difference. The largest information in three rounds is 0.063 nats on 16 replicates.

No episode lost its admissible events, including the unconditional `strong_suppress` and the unconditional `strong_favour`. The hard-support boundary was not observed, so `prohibit` was not introduced.

The 3-edge layer did not follow the sparse/dense shift.

Full route signatures did not recur. There is no repeated long itinerary to treat as a motif beyond the short adjacent steps.

S09's two rules do not add. The residual is an occupancy fact. It did not produce a separate route family.

The extra pairwise coefficient in Generation 007B was unused by every stored fit. Generation 8 did not replace that result with a large routing divergence carried by the initial triad orbit.

## Questions that became clearer

The descriptive axis at this horizon is the edge-count layer. Finite grade orders it. An unconditional weight moves it more than a conditional weight. The visible source class organises the first step among the three 3-edge organisations. The initial hidden orbit, at 16 replicates, does not.

Aggregate passage matching, which Generations 7 and 7B studied, and the trajectory atlas are different records. A one-rule scalar can match two aggregate passage numbers while the state-resolved selectivity stays elsewhere. In this generation that selectivity does not reappear as a large difference in the next 3-edge class.

## Questions that became less well posed

"Does hidden context matter?" needs the observable and the horizon. For the first 3-edge destination, the information is small and it saturates once arrival is complete. For the next class given the current pair class, the Round 0 conditional informations are about a thousandth of a nat. A different observable could still move. The question as asked of this atlas has a small answer.

Interaction magnitude is a poor higher-order signature. The largest layer shifts here belong to an unconditional pair rule, S10 and S16, which read no triad bit.

## Candidate distinctions worth a later Mode A design

These were not executed. Generation 8 stops at Round 2.

- Whether S08 `star-o00`'s 16/16 path split is stable under more replicates.
- Whether the four T→P placements inside one polarity are equivalent for occupancy and for 3-edge routing, under a tolerance declared before the sample.
- Whether the S09 residual L1 of 0.0698 has a state-resolved description that is more than the sum of two layer shifts.

## Questions worth further exploration, outside this generation

- Current-triad conditional information at the favour grades. Round 0's maximum was 0.00519 nats, on S09. It was not recomputed later.
- A hard-support boundary, only after an observation in which admissible events disappear. No Generation 8 episode supplied that observation.
- Return-time distributions beyond the first 3-edge arrival, if the question becomes how long a source class keeps being revisited. The return counts already differ by source class inside 512 pair events.

## RS / GLOBAL-COHERENCE INTERPRETATION

What was observed is a replayable history: edge-count oscillation, a stable 3-edge layer, grade-ordered layer shifts, a larger unconditional shift, a non-additive two-rule anchor, source-class routing, and small initial-orbit information.

What is inferred is that, in this ontology and at this horizon, the finite weight and its support organise the layer, and the initial hidden triad does not organise the next 3-edge class at a large scale.

That inference can sit inside a broader coherence assessment as a description of this dynamics. It does not establish a Designer, a Christian ontology, or an ultimate receiver. Those remain upstream of the simulation.
