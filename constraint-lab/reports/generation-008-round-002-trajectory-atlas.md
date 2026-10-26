# Generation 008 Round 2 — finite-grade order and two reversals

Round 2 follows the Round 1 atlas. A completed episode is an observation. Pass and fail in this report are reserved for replay and `verify --require-complete`.

The Round 1 observations that set this round were: `strong_favour` on a dissolve rule sat near `strong_suppress` on the matched form rule, the unconditional dissolve suppression carried more of the S09 dense shift than the conditional rule, and the 3-edge layer stayed near 0.314 of pair-epochs.

## Provenance

| Item | Value |
| --- | --- |
| Frozen plan commit | `93253e2d249a6f44ace3e7c63ce42306404fa401` |
| Plan hash | `d5141d33f817357cf028ac97de8d7dad486113685f86a0c71734003cfef437a0` |
| Plan file | `constraint-lab/exploration/generation-008/round-002-plan.json` |
| Decision journey line | journey step 5, commit `eb97a564c5391f1658818116406618dc1985616e` |
| Parent Round 1 plan | `509e80fbb5b472d8da61ba7ba85fcedba15939c1` |
| Parent Round 1 report | `7b7dc28b4631f1d2a675b7a43135da2d6d06ead4` |
| Tables | `constraint-lab/reports/generation-008-round-002-tables.json` |

`verify --require-complete` returned `ok` on 1,831 items, 0 problems, spec hash equal to the plan hash. Replay: 167 of 167 exact.

| Artifact | sha256 |
| --- | --- |
| `merge/atlas.json` | `14aaeefcd597eae1ab919e0dbe6a098930fa01b7d5496cc16c00985f28bf2870` |
| `merge/summary.json` | `ecce03ae13a4a0aec5bc17f55dbb4ebeccbd6789739938f41ae0a20639acacf2` |
| `index/transitions.jsonl.gz` | `2e58fd393f9926728b0ca5a3be4deb3277330ee73aa9f1938ed585227efd739a` |
| `index/class-runs.jsonl.gz` | `30bb9a7c60b82ac4ab3fb563bd0878bf789da7afa808ba9dec88401fd34c23c1` |

## What was run

Same ontology, same 26 hidden-context starts, 16 replicates, pair horizon 512, full-event cap 16,384. Episodes: 4 × 26 × 16 = 1,664.

| System | Parent | Expression |
| --- | --- | --- |
| S14 | S01, middle grade | `dissolve(0-1) \| absent(0-1-2) => weak_suppress` |
| S15 | S01, middle grade | `dissolve(0-1) \| absent(0-1-2) => weak_favour` |
| S16 | S10, grade flipped | `dissolve(0-1) => strong_favour` |
| S17 | S11, grade flipped | `dissolve(2-3) \| present(0-1-2) => strong_favour` |

No `prohibit`.

## Operational record

| Quantity | Value |
| --- | --- |
| Durable items | 1,831 (1,664 episodes + 167 replays) |
| Batches | 16 |
| Workers | 2 |
| Started | 2026-10-12T18:51:17Z |
| Last activity | 2026-10-12T18:53:23Z |
| Median batch wall | 14.495715 s |
| p90 batch wall | 15.764156 s |
| Maximum batch wall | 15.799182 s |
| Timeouts / retries / quarantines | 0 / 0 / 0 |
| Events written | 1,400,613 |
| Pair events | 851,968 |
| Disk after merge | 1.2 GB |

Median is the wall at index `n // 2`. p90 is nearest-rank index `min(n-1, ceil(0.9 n) - 1)`.

## OBSERVATIONS

All 1,664 episodes ended at `pair_horizon`. The transition diagonal is 0 on every system. Pair-event support is 212,992 per system.

The coordinate used below is dense minus sparse: the share of pair-epochs on 4, 5, or 6 edges, minus the share on 0, 1, or 2 edges. The 3-edge layer is the remainder.

| System | Sparse | 3-edge | Dense | Dense − sparse | L1 to S00 |
| --- | --- | --- | --- | --- | --- |
| S10 unconditional dissolve suppress | 0.2590 | 0.3136 | 0.4274 | +0.1684 | 0.1660 |
| S01 `strong_suppress` on the S01 rule | 0.3104 | 0.3148 | 0.3749 | +0.0645 | 0.0598 |
| S14 `weak_suppress` on the S01 rule | 0.3236 | 0.3139 | 0.3625 | +0.0389 | 0.0365 |
| S00 baseline | 0.3395 | 0.3150 | 0.3456 | +0.0061 | 0 |
| S15 `weak_favour` on the S01 rule | 0.3641 | 0.3147 | 0.3212 | −0.0429 | 0.0518 |
| S05 `strong_suppress` on the matched form rule | 0.3742 | 0.3134 | 0.3125 | −0.0617 | 0.0717 |
| S12 `strong_favour` on the S01 rule | 0.3853 | 0.3136 | 0.3012 | −0.0841 | 0.0926 |
| S17 `strong_favour` on the off-edge conditional dissolve | 0.3865 | 0.3122 | 0.3014 | −0.0851 | 0.0945 |
| S16 `strong_favour` on the unconditional dissolve | 0.4129 | 0.3139 | 0.2733 | −0.1396 | 0.1492 |

On the S01 expression the four finite grades fall in this order of dense − sparse: S01 `strong_suppress` +0.0645, S14 `weak_suppress` +0.0389, S15 `weak_favour` −0.0429, S12 `strong_favour` −0.0841. Each step is smaller than the one before it. The two weak grades sit on opposite sides of the baseline.

S14 against S01 has occupancy L1 0.0279. S15 against S12 has L1 0.0423. S15 against S05 has L1 0.0214. S16 against S10 has L1 0.3094. S16 against S00 has L1 0.1492, and S16 against S12 has L1 0.0570. S17 against S11 has L1 0.1573. S17 against S12 has L1 0.0060.

Five-edge share: S16 0.0657, S12 0.0768, S17 0.0778, S15 0.0846, S00 0.0939, S14 0.1013, S01 0.1060, S10 0.1277.

Mean full events, with the pair count fixed at 512: S14 863.4, S15 845.4, S17 835.4, S16 822.6. Triad-only fraction is the complement of 512 over that mean: S14 0.4065, S15 0.3939, S17 0.3867, S16 0.3771.

Mean pair-class entropy: S14 2.136, S15 2.133, S17 2.131, S16 2.117. Mean full-state entropy: S14 6.138, S15 6.125, S17 6.085, S16 6.021. Mean distinct pair classes: S14 11.000, S15 10.998, S17 10.990, S16 10.971. Mean source returns sit between 56.3 and 57.2.

Pooled first other 3-edge class. No episode was censored.

| System | Path (n=160) | Star (n=128) | Triangle (n=128) | Path return-before | Path mean time |
| --- | --- | --- | --- | --- | --- |
| S14 | star 81, triangle 79 | path 86, triangle 42 | path 89, star 39 | 0.594 | 8.71 |
| S15 | star 82, triangle 78 | path 92, triangle 36 | path 84, star 44 | 0.700 | 9.46 |
| S16 | star 87, triangle 73 | path 87, triangle 41 | path 92, star 36 | 0.863 | 10.96 |
| S17 | star 83, triangle 77 | path 80, triangle 48 | path 90, star 38 | 0.719 | 10.83 |

Star and triangle return-before-other-3-edge stays between 0.172 and 0.281. Mean time from those sources stays between 4.09 and 4.48 pair events.

Largest episode-equal information of hidden-context orbit about the first 3-edge destination is 0.0437 nats, on S17 path. The largest configuration-weighted value is 0.0523 nats, on S17 triangle. The largest pairwise Jensen-Shannon divergence between orbits is 0.1308, on S15 path and on S17 path. Mean divergences sit near 0.02.

The checkpoint series of that same first-destination information is 0 at 1 pair event. The largest cell at 2 pair events is 0.110 nats, and that cell still counts episodes whose outcome is `censored_at_horizon`. By 64 pair events every cell equals its value at 512, and the maximum is the 0.0437 nats above.

Pooled motifs of length 2, on the pair-class-change clock, are adjacent in edge count. The most common are `e2-deg2110` → `e1-deg1100` (59,306) and the reverse (58,952), then the path class with `e2-deg2110` (55,239 and 55,204). Sixty motifs were retained and 296 omitted. All four systems appear on the frequent pairs.

Route signatures of length 513 remain unique inside this round, so the medoid and rare-route selectors are lexicographic tie-breaks. Initial source residence is 1 on every episode. The highest-source-return selector picks `e588401bed2b4e452549f2eb` (S15, path orbit `path-o08`, 122 returns, seed 16539540120205479493).

## INFERENCES

The four finite grades on the S01 dissolve rule are ordered along the edge-count layer. `weak_suppress` is a shorter step in the dense direction of `strong_suppress`. `weak_favour` is a shorter step in the sparse direction of `strong_favour`. The baseline sits between the two weak grades.

`strong_favour` reverses the unconditional dissolve. S16 is on the sparse side of the baseline by about as much as S10 is on the dense side (L1 0.149 and 0.166). The unconditional rule remains a larger move than the conditional `strong_favour` (S16 against S12, L1 0.057).

`strong_favour` reverses the off-edge conditional dissolve. S17 lands on S12 (L1 0.0060). At `strong_favour`, naming a different edge and a present-condition is as fine a distinction as S11 against S01 was at `strong_suppress` (L1 0.0083).

The first 3-edge route stays the source-class pattern of Rounds 0 and 1. The timing of path return moves with the sparse shift: S16 path starts return before another 3-edge class in 0.863 of episodes, and the mean wait is 11.0 pair events. The destination split itself stays near even. Hidden-context information on that destination stays inside the small band of the earlier rounds.

## RS / GLOBAL-COHERENCE INTERPRETATION

The descriptive distinction that this round sharpens is the order of the four finite grades, and the reversal of both the unconditional rule and the off-edge conditional rule under `strong_favour`. Initial hidden-context information stays small. This round does not establish a Designer, a Christian ontology, or an ultimate receiver.

## NEXT EXPLORATION OPTIONS

Round 3 stays unopened. The question this round was built to read — whether the four grades are ordered, and whether `strong_favour` reverses the unconditional dissolve and the off-edge conditional dissolve — is answered by the order and the two reversals above.

| Id | Perturbation left unopened | CN | RD | RC | EC | CG | CB |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E | 64 replicates of S08 `star-o00` | 1 | 1 | 1 | 2 | 3 | 2 |
| F | `prohibit` on the unconditional dissolve | 2 | 2 | 1 | 2 | 2 | 3 |
| G | current-triad information at the favour grades | 2 | 1 | 1 | 3 | 2 | 3 |
| H | a later Mode A test of within-polarity placement | 1 | 1 | 1 | 3 | 3 | 3 |

E still resamples a 16-episode cell. F still has no episode in which admissible events ran out: 1,664 of 1,664 Round 2 episodes, and every earlier Generation 8 episode, ended at the pair horizon. G and H are questions the synthesis can name. They are not a further Generation 8 round. The coordinates are an attention vector. They are not summed, and they are not a score.
