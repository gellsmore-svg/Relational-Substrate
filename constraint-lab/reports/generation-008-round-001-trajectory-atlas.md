# Generation 008 Round 1 — component split and grade sign

Round 1 follows the Round 0 atlas. It is still an exploration record. A completed episode has no scientific pass or fail.

The Round 0 observations that set this round were: dissolve-suppression moved pair-epoch mass toward higher edge counts, form-suppression moved it toward lower edge counts, and the two-rule anchor S09 moved much further (occupancy L1 to the baseline 0.2565) than any singleton. Initial-orbit information on the first 3-edge destination stayed below 0.07 nats.

## Provenance

| Item | Value |
| --- | --- |
| Frozen plan commit | `509e80fbb5b472d8da61ba7ba85fcedba15939c1` |
| Plan hash | `6f19f8d9ad374792eae970b7691f3eca63699a9d743c13016550e266a9de8354` |
| Plan file | `constraint-lab/exploration/generation-008/round-001-plan.json` |
| Parent Round 0 plan | `0a9e74f287b3ecb24efd3981b9562e53086ffee9` |
| Parent Round 0 report | `2b1778306f08e556df195d735e482c8b3533d796` |
| Tables | `constraint-lab/reports/generation-008-round-001-tables.json` |

`verify --require-complete` returned `ok` on 1,831 items, 0 problems, spec hash equal to the plan hash. Replay: 167 of 167 exact.

| Artifact | sha256 |
| --- | --- |
| `merge/atlas.json` | `66977f3435fe3beccec6519a13f917ab4a4e22c5de891c57fe1f610764b05eb3` |
| `merge/summary.json` | `a337ed64c76d601f64f9f331a37a4c2b66dedbd682aed8569f070b04fac52b30` |
| `index/transitions.jsonl.gz` | `b821e28c19eba7d6f986e0a0161790e127b4b46d1f2a4b0ccc52cf0948e867ee` |
| `index/class-runs.jsonl.gz` | `7bed0770731df02980cff0a30942c8a95da2d8849400deefe1a3eec6d546ad63` |

## What was run

Same ontology, same 26 hidden-context starts, 16 replicates, pair horizon 512, full-event cap 16,384. Episodes: 4 × 26 × 16 = 1,664.

| System | Parent | Expression |
| --- | --- | --- |
| S10 | S09 without the conditional rule | `dissolve(0-1) => strong_suppress` |
| S11 | S09 without the unconditional rule | `dissolve(2-3) \| present(0-1-2) => strong_suppress` |
| S12 | S01, grade flipped | `dissolve(0-1) \| absent(0-1-2) => strong_favour` |
| S13 | S05, grade flipped | `form(0-1) \| absent(0-1-2) => strong_favour` |

No `prohibit`.

## Operational record

| Quantity | Value |
| --- | --- |
| Durable items | 1,831 (1,664 episodes + 167 replays) |
| Batches | 16 |
| Workers | 2 |
| Median batch wall | 14.597432 s |
| p90 batch wall | 15.761986 s |
| Maximum batch wall | 15.95338 s |
| Timeouts / retries / quarantines | 0 / 0 / 0 |
| Events written | 1,425,781 |
| Pair events | 851,968 |
| Disk after merge | 1.2 GB |

## OBSERVATIONS

All 1,664 episodes ended at `pair_horizon`.

The 3-edge layer stays near 0.314 of pair-epochs in every Round 0 and Round 1 system below. The movement is between the sparse side (0, 1, and 2 edges) and the dense side (4, 5, and 6 edges).

| System | Sparse | 3-edge | Dense | L1 to S00 |
| --- | --- | --- | --- | --- |
| S00 baseline | 0.339 | 0.315 | 0.346 | 0 |
| S12 favour dissolve | 0.385 | 0.314 | 0.301 | 0.0926 |
| S05 suppress form | 0.374 | 0.313 | 0.313 | 0.0717 |
| S01 suppress dissolve | 0.310 | 0.315 | 0.375 | 0.0598 |
| S11 conditional dissolve on edge 2-3 | 0.308 | 0.315 | 0.378 | 0.0672 |
| S13 favour form | 0.298 | 0.315 | 0.387 | 0.0864 |
| S10 unconditional dissolve suppress | 0.259 | 0.314 | 0.427 | 0.1660 |
| S09 both S10 and S11 rules | 0.227 | 0.307 | 0.466 | 0.2565 |

S11 against S01, two conditional dissolve suppressions on different edges, has occupancy L1 0.0083. S10 against S09 has L1 0.1011. The sum of the separate S10 and S11 deviations from S00 differs from S09 by L1 0.0698.

S12 against its `strong_suppress` parent S01 has L1 0.1504. S12 against the form-suppression system S05 has L1 0.0239. S13 against its parent S05 has L1 0.1523. S13 against the dissolve-suppression system S01 has L1 0.0266.

Five-edge share of pair-epochs: S12 0.0768, S05 0.0814, S00 0.0939, S01 0.1060, S11 0.1073, S13 0.1107, S10 0.1277, S09 0.1449.

Triad-only fraction: S12 0.3860, S13 0.3861, S00 0.3980, S11 0.4094, S10 0.4245, S09 0.4364.

Pooled first other 3-edge class:

| System | Path (n=160) | Star (n=128) | Triangle (n=128) |
| --- | --- | --- | --- |
| S10 | triangle 89, star 71 | path 96, triangle 32 | path 90, star 38 |
| S11 | triangle 80, star 80 | path 89, triangle 39 | path 86, star 42 |
| S12 | triangle 87, star 73 | path 95, triangle 33 | path 85, star 43 |
| S13 | triangle 80, star 80 | path 78, triangle 50 | path 83, star 45 |

The largest first-destination information is 0.0485 nats, on S13 path. S10 star is 0.0053 nats. No episode was censored. Route signatures of length 513 did not need a new census to see that the class still changes on every pair event: the transition diagonal remains a property of the edge-count partition.

The highest source-return selector picks `e1e034a87e4af26b9ddfd50d` (S11, 125 returns).

## INFERENCES

The grade sign reverses the layer shift of the matched absent-adjacent pair. `strong_favour` on a dissolve rule lands near `strong_suppress` on the corresponding form rule, and `strong_favour` on a form rule lands near `strong_suppress` on the corresponding dissolve rule. The 3-edge layer is the part that stays put.

S09's dense shift is larger than either component. The unconditional dissolve suppression carries more of it than the conditional rule. The conditional rule, on its own, is close to the Round 0 conditional dissolve suppressions, including one that names a different edge. The two components in combination are in the same direction as the sum of their separate deviations, and the residual L1 is 0.0698, so the combination is not that sum.

The first 3-edge route stays a source-class pattern: stars and triangles go to the path class, and a path start splits. S13's star starts are the loosest of these splits (78 path, 50 triangle) and still path-majority.

## RS / GLOBAL-COHERENCE INTERPRETATION

The new descriptive distinction is the direction in which a finite weight pushes the edge-count layer, together with whether that weight is conditional. Hidden-context orbit information stays in the small band already seen in Round 0. This round does not establish a Designer, a Christian ontology, or an ultimate receiver.

## NEXT EXPLORATION OPTIONS

| Id | Perturbation | CN | RD | RC | EC | CG | CB |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | S01 to `weak_suppress` | 1 | 2 | 1 | 4 | 2 | 4 |
| B | S01 to `weak_favour` | 1 | 2 | 1 | 4 | 2 | 4 |
| C | S10 to `strong_favour` | 3 | 3 | 2 | 5 | 3 | 4 |
| D | S11 to `strong_favour` | 2 | 2 | 2 | 4 | 3 | 4 |
| E | 64 replicates of S08 `star-o00` | 1 | 1 | 1 | 2 | 3 | 2 |
| F | `prohibit` on the unconditional dissolve | 2 | 2 | 1 | 2 | 2 | 3 |

Chosen for Round 2: A, B, C, D.

A and B place the two middle finite grades on the same structural rule as S01 and S12, so the four grades can be read in one order. C asks whether the larger unconditional shift reverses under `strong_favour`, as the conditional shift did. D asks the same of the off-edge conditional rule.

Deferred: E resamples a 16-episode cell. F would introduce a hard-support boundary. Round 1 still reached the pair horizon with admissible events on every episode, including the unconditional suppression. `prohibit` still lacks a concrete support-boundary observation.

Round 2 executes only after its plan commit is on the remote. This report does not contain that commit's hash.
