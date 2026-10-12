# Generation 008 Round 0 — trajectory atlas

Round 0 is an atlas of replayable trajectories. It is not a verdict. A completed episode has no scientific pass or fail. Pass and fail below are reserved for execution, replay, and `verify --require-complete`.

The question is what the N=4 independent hypergraph does when a visible 3-edge pair organisation is the start, the hidden triad configuration varies inside that graph's automorphism group, and one finite constraint system runs for a fixed horizon.

## Provenance

| Item | Value |
| --- | --- |
| Branch | `research/constraint-lab-v0.8-exploration` |
| Frozen plan commit | `0a9e74f287b3ecb24efd3981b9562e53086ffee9` |
| Plan hash | `fec52960f5e16706e12e9baf0a45169f49c2414b6e7e3ecc80b1b9d0f97c3b86` |
| Plan file | `constraint-lab/exploration/generation-008/round-000-plan.json` |
| Runner | `generation-008-trajectory/v1` |
| Mode | B |
| Machine-readable tables | `constraint-lab/reports/generation-008-round-000-tables.json` |

`verify --require-complete` returned `ok` with 4,576 items, 0 problems, 0 missing completed items, and 0 quarantines. The spec hash on that report is the plan hash. Replay items: 416 of 416 exact.

Raw trajectories stay in gitignored `constraint-lab/generated/generation-008/round-000/`. The published tables carry these artifact hashes:

| Artifact | sha256 |
| --- | --- |
| `merge/atlas.json` | `12d40feb65ef7bcf4b63cfc4d322dcf4d8132fe0dc25e5a5bbc2e670a80ccce5` |
| `merge/summary.json` | `b8b8db3cf522aa5c910f1c8eb5733fdbe7af0fe8da789c34586b5a88bbad04fd` |
| `index/transitions.jsonl.gz` | `d41b4c128d307165a4c45924ca51fe9175de5227e44f79446b2424e1f8337e1d` |
| `index/class-runs.jsonl.gz` | `90c89e3d10365de39f327d44f51d01ce436d69484ef352c8795975f9f7764c26` |

## What was run

Ontology: N=4, O=3, G=S=H=L=0, independent hypergraph. State: 6 pair bits and 4 triad bits, 1024 full states.

Source organisations, each a canonical labelled representative, with hidden-context orbits under that graph's automorphism group:

| Source | Class | Mask | Aut | Orbits | Sizes |
| --- | --- | --- | --- | --- | --- |
| star | `e3-deg3111-tri0-comp1` | 7 | 6 | 8 | 1, 3, 3, 1, 1, 3, 3, 1 |
| path | `e3-deg2211-tri0-comp1` | 13 | 2 | 10 | 1, 2, 1, 2, 2, 2, 2, 1, 2, 1 |
| triangle | `e3-deg2220-tri1-comp2` | 11 | 6 | 8 | 1, 1, 3, 3, 3, 3, 1, 1 |

Orbit sizes sum to 16 for each source. Hidden-context starts: 26.

| System | Expressions |
| --- | --- |
| S00 | none. Role: baseline relational dynamics |
| S01 | `dissolve(0-1) \| absent(0-1-2) => strong_suppress` |
| S02 | `dissolve(0-1) \| absent(0-2-3) => strong_suppress` |
| S03 | `dissolve(0-1) \| present(0-1-2) => strong_suppress` |
| S04 | `dissolve(0-1) \| present(0-2-3) => strong_suppress` |
| S05 | `form(0-1) \| absent(0-1-2) => strong_suppress` |
| S06 | `form(0-1) \| absent(0-2-3) => strong_suppress` |
| S07 | `form(0-1) \| present(0-1-2) => strong_suppress` |
| S08 | `form(0-1) \| present(0-2-3) => strong_suppress` |
| S09 | `dissolve(0-1) => strong_suppress` and `dissolve(2-3) \| present(0-1-2) => strong_suppress` |

S01–S08 are the eight Generation 4 structural T→P forms at `strong_suppress`. S09 is the Generation 5 disjoint anchor `07f18bb89362ae4ea6606830`, both rules regraded to `strong_suppress`. Round 0 uses no `prohibit`.

Replicates: 16 per system, source, and orbit. Episodes: 10 × 26 × 16 = 4,160. Pair horizon: 512. Full-event cap: 16,384. Seeds: `sha256-u64-v1` over the six identity fields.

## Operational record

| Quantity | Value |
| --- | --- |
| Durable items | 4,576 (4,160 episodes + 416 replays) |
| Batches | 39 |
| Workers | 2 |
| Batch item cap | 120 |
| Median batch wall | 15.49511 s |
| p90 batch wall | 16.694902 s |
| Maximum batch wall | 17.335057 s |
| Batches over 30 s / 60 s / 120 s | 0 / 0 / 0 |
| Timeouts | 0 |
| Retries | 0 |
| Quarantines | 0 |
| Failed items | 0 |
| Events written | 3,623,976 |
| Pair events | 2,129,920 |
| Transition markers | 2,129,920 |
| Replay sample | 416 / 4,160, every one `exact` |
| Disk after merge | 3.0 GB |

The preflight estimate was about 138 s of episode compute and about 119 MB of gzip event streams. The event streams are that order of size. The directory is about 3.0 GB because each episode item stores its summary, including one marker per pair event, and the merge copies those items. The horizon stayed at 512. It was not revised after the trajectories existed.

Median and p90 use the same rank convention as Generation 007B: median index `n//2`, p90 index `min(n-1, ceil(0.9n)-1)`, here 19 and 35.

## OBSERVATIONS

### Termination and clocks

All 4,160 episodes ended with `termination_reason = pair_horizon`. The full-event cap was not hit. No episode reached a state with no admissible event.

Mean full-event counts run from 851.3 on S00 to 909.2 on S09. Mean triad-only fraction is 0.3980 on S00, 0.409–0.411 on S01–S08, and 0.4364 on S09. Triad toggles remain in the full trajectory. They are about two fifths of the full clock on the baseline and a larger share on S09.

Every episode recorded 512 pair events. Pair-epoch occupancy, including the initial epoch, is 513 per episode and 213,408 per system.

### Every pair event changes isomorphism class

The eleven class names are partitioned by edge count. A pair event toggles one pair bit, so the edge count changes by one. The class therefore changes on every pair event.

Observed consequences, in every system:

- The 11×11 pair-event transition diagonal is 0. Support per system is 212,992, equal to 416 × 512.
- The initial source residence is 1 in every episode. The first pair event leaves the source class.
- A visit to a pair class lasts one pair-epoch. Occupancy counts visits, including the start.
- The change-compressed class path has length 513.
- All 4,160 full-length route signatures are distinct.

The predeclared medoid and rare-route selectors therefore meet a sample in which every signature occurs once. Under the tie break, the global medoid id is `e5e320c67f70d4d1d1940298` and the global rare-route id is `b2e41a29904b602092877ae1`. Longest source residence is 1 for every episode, so that selector returns the smallest episode id in scope. Highest source returns is the selector that still varies: global and S09 both select `c6316c8553bb3bbf2624a347` with 129 returns. S00 selects `61a35131a7c3f987e1ca70af` with 122 returns. Replay of `c6316c8553bb3bbf2624a347` is `exact` on 951 events.

The opening of that S09 path episode, orbit `path-o07`, is a dissolve of a pair (`4/37`, rules empty on the chosen slot), then a form into the triangle class, then several triad toggles, then a return to the path class at pair epoch 5. The baseline episode with the most source returns opens at probability `1/10` on every slot. Later S09 steps use normaliser 34 when two slots are down-weighted, which is the integer-weight image of two `strong_suppress` factors.

### Where the pair clock spent time

Class index order used below:

```text
0 e0-deg0000-tri0-comp4          1 mask
1 e1-deg1100-tri0-comp3          6
2 e2-deg1111-tri0-comp2          3
3 e2-deg2110-tri0-comp2         12
4 e3-deg2211-tri0-comp1         12   path source
5 e3-deg2220-tri1-comp2          4   triangle source
6 e3-deg3111-tri0-comp1          4   star source
7 e4-deg2222-tri0-comp1          3
8 e4-deg3221-tri1-comp1         12
9 e5-deg3322-tri2-comp1          6
10 e6-deg3333-tri4-comp1         1
```

S00 pair-epoch counts: 3270, 19663, 9990, 39522, 40446, 13491, 13278, 10038, 40416, 20034, 3260.

Those counts sit close to the share of the 64 labelled pair graphs. The L1 distance from S00 occupancy to that mask share is 0.0098. The three 3-edge sources are not a preferred destination set. The path class and `e4-deg3221-tri1-comp1` each hold about 0.190 of S00 epochs, and each is 12 of the 64 labelled graphs. The star and the triangle each hold about 0.063, and each is 4 of the 64 graphs.

Mean pair-class entropy is 2.134 nats on S00 (the uniform 11-class entropy is log 11 ≈ 2.398). Mean full-state entropy is 6.137 nats on S00 (log 1024 ≈ 6.931). Mean distinct pair classes visited is 10.998 on S00. Episodes commonly touch all eleven classes. S09 is the low end, at 10.923.

### The eight T→P archetypes

Occupancy L1 distance to S00:

| System | Action | L1 |
| --- | --- | --- |
| S01 | dissolve, absent(0-1-2) | 0.0598 |
| S02 | dissolve, absent(0-2-3) | 0.0674 |
| S03 | dissolve, present(0-1-2) | 0.0723 |
| S04 | dissolve, present(0-2-3) | 0.0690 |
| S05 | form, absent(0-1-2) | 0.0717 |
| S06 | form, absent(0-2-3) | 0.0830 |
| S07 | form, present(0-1-2) | 0.0798 |
| S08 | form, present(0-2-3) | 0.0791 |
| S09 | two-rule anchor | 0.2565 |

S01–S04, the dissolve suppressions, move counts toward higher edge numbers. On S01 the 5-edge class has 22,624 epochs against 20,034 on S00, and the 1-edge class has 17,116 against 19,663. S05–S08, the form suppressions, move the other way. On S05 the 1-edge class has 22,659 and the 5-edge class has 17,374.

Inside one action polarity the four condition placements stay near one another. The occupancy L1 from S01 to S04 is 0.0108, smaller than either system's L1 to S00. The form-side systems show the same pattern. Exact counts are in the tables.

Pair-class entropy stays near 2.13 on S01–S08. Full-state entropy stays near 6.12–6.13. Triad-only fraction stays near 0.410.

### The composite anchor

S09 is the occupancy outlier. Counts: 1146, 10448, 8483, 28254, 42026, 11545, 11973, 14017, 48427, 30920, 6169.

Relative to the mask share, empty and 1-edge classes are low, and the 5-edge and 6-edge classes are high. The 5-edge class has 30,920 epochs against 20,034 on S00. The complete graph has 6,169 against 3,260. Mean pair-class entropy falls to 2.096. Mean full-state entropy falls to 6.039. Mean full events rise to 909.2, and the triad-only fraction rises to 0.4364.

The leading transition cells on S09 are `e4-deg3221-tri1-comp1 → e5-deg3322-tri2-comp1` (19,111) and the reverse (19,010). On S00 those two cells are 13,327 and 13,498.

### Routing among the three 3-edge classes

No episode is `censored_at_horizon`. No episode remains in its source class.

Pooled first other 3-edge class, episode counts:

| System | From path (n=160) | From star (n=128) | From triangle (n=128) |
| --- | --- | --- | --- |
| S00 | star 82, triangle 78 | path 90, triangle 38 | path 86, star 42 |
| S01 | star 81, triangle 79 | path 88, triangle 40 | path 88, star 40 |
| S02 | triangle 82, star 78 | path 91, triangle 37 | path 95, star 33 |
| S03 | star 82, triangle 78 | path 90, triangle 38 | path 95, star 33 |
| S04 | triangle 82, star 78 | path 93, triangle 35 | path 92, star 36 |
| S05 | triangle 84, star 76 | path 91, triangle 37 | path 84, star 44 |
| S06 | triangle 82, star 78 | path 85, triangle 43 | path 96, star 32 |
| S07 | star 82, triangle 78 | path 89, triangle 39 | path 93, star 35 |
| S08 | triangle 83, star 77 | path 95, triangle 33 | path 93, star 35 |
| S09 | star 86, triangle 74 | path 85, triangle 43 | path 93, star 35 |

The path class is the usual next 3-edge class after a star start or a triangle start. A path start splits between star and triangle, close to even. Mean pair-epoch at which that next class begins is about 9.2–9.5 from a path start and about 3.6–4.7 from a star or triangle start.

Return to the source class before any other 3-edge class, pooled:

- Path starts: 0.544–0.681
- Star starts: 0.148–0.242
- Triangle starts: 0.195–0.297

Mean source returns over the whole horizon follow the same split. On S00, path orbits average about 95–101 returns and star or triangle orbits average about 29–34. S09 path orbits average about 97–103. The horizon contains 513 class positions, so a path-started episode is in the path class on roughly a fifth of the pair clock and returns many times.

### Hidden-context information on the first 3-edge destination

`I(initial hidden-context orbit ; first other 3-edge class | source, system)`, in nats, episode-equal:

- S00: path 0.0155, star 0.0134, triangle 0.0153
- The thirty constrained cells run from 0.0098 (S04 star) to 0.0631 (S08 triangle)
- Configuration-weighted values sit in the same band. The largest weighted value is 0.0710 on S08 triangle

Max Jensen-Shannon divergence between orbit destination distributions:

- S00: 0.0316–0.0371
- Largest constrained value: 0.1687 on S08 path. S08 triangle is 0.1615 and S08 star is 0.1518

Orbit tables for the high cells, 16 episodes each:

- S00 star orbits send 9–13 episodes to the path class
- S08 `star-o00` sends 16 of 16 to the path class. The other S08 star orbits send 10–12
- S08 `triangle-o02` sends 9 to the star class and 7 to the path class. The other S08 triangle orbits are path-majority, from 9–15 of 16
- S02 `star-o00` sends 15 to the path class and 1 to the triangle class
- S01 `path-o04` sends 13 to the triangle class and 3 to the star class. S00 path orbits sit between 6 and 10 on each side

These are the sample counts. log 2 ≈ 0.693 nats would be a deterministic split between two destinations. The observed information is below 0.07 nats.

### Checkpoints of that same first-destination statistic

At pair epoch 1 the information is 0 in every cell. One pair toggle changes the edge count by one, so it cannot land on another 3-edge class. Every episode is still unresolved, and the unresolved label is shared.

The value then moves while some episodes have arrived and some have not. It locks to the horizon value once every episode has a destination. On these data that lock is in place by epoch 32 or 64. The series in the tables is flat from that checkpoint through 512. The flat tail is the definition of a first-arrival label.

### Current class at a checkpoint

A second descriptor, computed from the class-run index for this report, is `I(initial orbit ; pair class occupied at the checkpoint | source, system)`.

On S00 this ranges from about 0.007 at epoch 1 on the triangle to about 0.164 at epoch 16 on the path, and it is still about 0.09–0.12 at epoch 512. Constrained cells occupy a similar band. The high readings include 0.260 on S01 star at epoch 4 and 0.202 on S07 star at epoch 64. The baseline itself moves by about 0.16 across checkpoints, with 16 episodes, 11 classes, and 8 or 10 orbits. The full series is in the narrative above and can be recomputed from `index/class-runs.jsonl.gz`. It is not a second experiment.

### Conditional information given the current pair class

Each of the 212,992 pair events in a system carries the current triad-orbit label of the labelled pair graph. Averaged over the current pair class, with weight equal to the number of pair events:

| System | I(current triad ; next class \| current class) | I(initial orbit ; next class \| current class) |
| --- | --- | --- |
| S00 | 0.00049 | 0.00097 |
| S01 | 0.00244 | 0.00103 |
| S02 | 0.00134 | 0.00097 |
| S03 | 0.00137 | 0.00112 |
| S04 | 0.00210 | 0.00086 |
| S05 | 0.00220 | 0.00106 |
| S06 | 0.00157 | 0.00095 |
| S07 | 0.00121 | 0.00106 |
| S08 | 0.00213 | 0.00101 |
| S09 | 0.00519 | 0.00099 |

Given the current pair class, the initial orbit stays near 0.001 nat in every system. The current triad orbit is 0.00049 nat on the baseline and rises to 0.00519 nat on S09. The singleton T→P systems sit between 0.0012 and 0.0024. These quantities use every pair event. They are a different scale from the first-destination information, which is estimated from 128 or 160 episodes.

### Motifs

Motifs are counted on the change-compressed class path, which here is the class of every pair-epoch. The top motifs are two-step reversals between classes whose edge counts differ by one, and they occur in all ten systems. The largest are:

| Count | Motif |
| --- | --- |
| 139,697 | `e4-deg3221-tri1-comp1 → e5-deg3322-tri2-comp1` |
| 139,143 | the reverse |
| 136,201 | `e4-deg3221-tri1-comp1 → e3-deg2211-tri0-comp1` |
| 136,106 | the reverse |
| 130,197 | `e2-deg2110-tri0-comp2 → e3-deg2211-tri0-comp1` |
| 130,140 | the reverse |
| 92,239 | `e4-deg3221 → e5-deg3322 → e4-deg3221` |

Sixty motifs are retained and 296 further motif keys were omitted. The retained list is dominated by this shared oscillation. A system-specific difference shows up in the rate, not in a private motif: S05–S08 put `e2-deg2110-tri0-comp2 ↔ e1-deg1100-tri0-comp3` at the top of their own transition matrices (about 15,000 in each direction), while S01–S04 and S09 put `e4-deg3221-tri1-comp1 ↔ e5-deg3322-tri2-comp1` at the top.

### Absences in the sample

- No episode failed to leave its source class.
- No episode failed to reach another 3-edge class inside 512 pair events.
- No full-length route signature recurred.
- No system produced a transition diagonal.
- No condition placement among S01–S04, or among S05–S08, produced an occupancy L1 to baseline as large as S09's.
- The baseline route splits and the constrained route splits occupy one band of a few episodes per orbit, with the individual cells listed above at the edge of that band.

## INFERENCES

The pair-class atlas is organised first by edge count. Because the class name includes the edge count, the pair clock is an oscillation between adjacent layers. The baseline layer weights are close to the number of labelled graphs in each class. That is what a well-mixed uniform toggle on the six edges looks like when it is read through these eleven names.

The eight T→P archetypes add a smaller shift along that same axis. Dissolve-suppression systems spend more pair-epochs in the higher edge counts. Form-suppression systems spend more in the lower edge counts. Which triad is named, and whether the literal is `present` or `absent`, is a finer occupancy difference than the form/dissolve split at this grade.

S09 moves further toward the dense graphs than any singleton. It is the only Round 0 system with an unconditional pair rule. The two components have not been run separately, so the atlas does not yet say how much of that shift each rule carries.

Hidden-context orbits change the first 3-edge destination by a small amount of information on top of a source-class pattern that is already visible on the baseline: stars and triangles go to the path class, and the path class splits. A few 16-episode cells, notably S08 `star-o00` at 16/16 path, sit outside the baseline orbit range. The same system's other orbits do not repeat that extreme. The generation leaves that cell as a sample observation.

The first-destination checkpoint curve flattens because the label is a first-arrival label. It is weak evidence about forgetting. The class occupied at a late checkpoint still varies with the initial orbit inside a band the baseline also occupies.

Source-return counts are high for path starts because the path class is large and is visited often, and lower for star and triangle starts because those classes are small. The return counts track that occupancy. They are a revisit structure in the record.

## RS / GLOBAL-COHERENCE INTERPRETATION

The trajectories are a bounded stochastic history of states, admissible toggles, constraint weights, and integer-weight draws. Recurrent structures in that history are the edge-count oscillation, the path class as the common 3-edge waypoint, and a polarity-sized shift when a single T→P rule is `strong_suppress`.

Higher-order context is present in two places that this round can separate. It is the initial orbit under the source graph, and it is the current triad orbit of whatever pair graph the walk has reached. The initial orbit is a weak descriptor of the next 3-edge class. Conditional on the current pair class, the current triad orbit shifts the next-class distribution by a few thousandths of a nat, most on S09. Rules whose conditions read a triad are able to change a weight when that triad matches, and the aggregate occupancy does move with the action polarity. This round does not treat that movement as a demonstration that a higher-order relation is ontologically basic. The small conditional information is the measured size of the next-class association, and the occupancy shift is the measured size of the layer bias.

Simulation of these trajectories does not establish a Designer, a Christian ontology, or an ultimate receiver. Those remain upstream or broader premises. What this round adds to a coherence reading is a description: at this grade and horizon, visible pair organisation and the form/dissolve axis sort the atlas more strongly than the initial hidden-context orbit does.

## NEXT EXPLORATION OPTIONS

Candidates, each with an attention vector. The coordinates are CN contextual novelty, RD routing diversity, RC recurrence, EC explanatory compression, CG coherence relevance, CB computational boundedness. They are ordinals from 0 to 5. They are not summed, and they are not a score the trajectory maximises.

| Id | Perturbation | CN | RD | RC | EC | CG | CB |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | Remove the T→P rule from S09. Keep `dissolve(0-1) => strong_suppress` | 2 | 2 | 2 | 5 | 3 | 4 |
| B | Remove the unconditional rule from S09. Keep `dissolve(2-3) \| present(0-1-2) => strong_suppress` | 3 | 2 | 2 | 5 | 3 | 4 |
| C | Weight-shift S01 from `strong_suppress` to `strong_favour` | 2 | 3 | 2 | 4 | 3 | 4 |
| D | Weight-shift S05 from `strong_suppress` to `strong_favour` | 2 | 3 | 2 | 4 | 3 | 4 |
| E | Weight-shift S08 from `strong_suppress` to `strong_favour` | 3 | 3 | 2 | 3 | 4 | 4 |
| F | Repeat S00 and S08 at 64 replicates on the same orbits | 1 | 1 | 1 | 2 | 4 | 2 |

Chosen for Round 1: A, B, C, D. Four new systems, the Round 0 context basis, 16 replicates, horizon 512.

A and B split the only system whose occupancy moved far from the mask share, one component at a time. C and D put the opposite finite grade on one dissolve archetype and the matching form archetype (`absent(0-1-2)` on edge `0-1`). If the layer shift reverses with the grade, the sign of the weight is the occupancy axis. If it does not, the `strong_suppress` shift is specific to that grade.

Deferred:

- E stacks a grade change onto the system with the largest sample divergence. The matched pair C and D asks the grade question with less confounding. S08 `star-o00` stays recorded.
- F resamples laws Round 0 already ran. It becomes useful if a later round still has an orbit cell outside the baseline range and the question is trajectory resolution.
- Condition polarity flips of S01 and S08 land on S03 and S06, which Round 0 already contains.
- The eight structural T→P forms are already in the atlas, so a neighbour step inside that set repeats a Round 0 system.
- `prohibit` stays out. Every Round 0 episode had admissible events through the pair horizon. No hard-support boundary showed up in the sample.

Round 1 executes only after its plan file is committed and pushed. That commit is the frozen plan for the round. This report does not contain that commit's hash.
