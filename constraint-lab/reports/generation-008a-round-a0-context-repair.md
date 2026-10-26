# Generation 008A Round A0 — context-alignment repair

Round A0 is Mode B. A completed trajectory is an observation. Pass and fail in this report are reserved for software tests, replay, and `verify --require-complete`.

The question is what, in the stochastic future of one visible pair organisation, still depends on which of the 16 hidden triad configurations it started from, once every configuration is actually run.

## A. External Review 008

Review 008 accepted the Generation 8 micro-batch platform and the trajectories that were run. It qualified the hidden-context conclusions. It did not erase the edge-count occupancy axis, the finite-grade order, the visible-source routing pattern, or the composite-system occupancy shift.

The review target remains `research/constraint-lab-v0.8-exploration` at `f5c0b6d1c8aae7b467066a4b3b5974ea2a0f59c9`. Generation 8 plans, journey lines, reports, synthesis, and execution provenance are unchanged.

## B. Context-symmetry flaw

Generation 8 reduced the 16 triad configurations under `Aut(visible source graph)` before execution. That reduction preserves the dynamics when the active rule system is invariant under those automorphisms. Baseline dynamics are. A labelled rule such as `dissolve(0-1) | absent(0-1-2) => strong_suppress` is not, because some source-graph automorphisms move the action edge, the conditioning triad, or both.

Two starts can therefore be equivalent under the visible graph and inequivalent under the visible graph plus the active rule system. Generation 8 represented both by one canonical context orbit. The trajectories that were run remain valid. The statements that initial hidden context has only a small effect, that maximum context information is about 0.06 nats, and that hidden context is broadly routing-insensitive are provisional under that graph-only orbit basis.

The trajectory engine, RNG, event logging, replay, and constraint semantics were not the object of the repair.

## C. Corrected execution basis

For each of star, path, and triangle, Round A0 executed all 16 raw triad configurations. That is 48 starts per system. Symmetry is computed after execution. It does not delete a start.

Episode identity and the seed use `experiment_id`, `round_id`, `system_id`, `source_graph_class`, `raw_triad_config`, and `replicate_index`. A graph-only orbit id is analysis metadata. Generation 8 episodes are not counted as Generation 8A replicates.

`Aut(source graph, constraint system)` is the set of vertex permutations that preserve the labelled source pair mask and the multiset of labelled rules. A permutation may reorder rules in a multi-rule system. It may not change action, direction, condition, polarity, weight, or multiplicity.

## D. Rule-aware automorphism groups

These groups were calculated from the frozen expressions and recorded in the plan before any Round A0 trajectory. They are not trajectory results. Orbit sizes sum to 16 in every cell.

| System | Star | Path | Triangle |
| --- | --- | --- | --- |
| R00 baseline | \|G\|=6, 8 orbits, sizes 1,3,3,1,1,3,3,1 | \|G\|=2, 10 orbits, sizes 1,2,1,2,2,2,2,1,2,1 | \|G\|=6, 8 orbits, sizes 1,1,3,3,3,3,1,1 |
| R01, R02, R06 conditional on edge 0-1 and triad 0-1-2 | \|G\|=1, 16 singleton orbits | \|G\|=1, 16 singleton orbits | \|G\|=2, 12 orbits, sizes 1,1,1,1,2,2,2,2,1,1,1,1 |
| R03, R07 unconditional `dissolve(0-1)` | \|G\|=2, 12 orbits, sizes 1,2,1,1,2,1,1,2,1,1,2,1 | \|G\|=2, 10 orbits, same sizes as the full path group | \|G\|=2, 12 orbits, same sizes as the conditional triangle group |
| R04, R05 off-edge conditional, including the two-rule composite | \|G\|=1, 16 singleton orbits | \|G\|=1, 16 singleton orbits | \|G\|=2, 12 orbits, same sizes as the conditional triangle group |

Baseline recovers `Aut(source graph)`. The grade does not change the group when the structural multiset is the same. The triangle subgroup of a labelled rule on edge 0-1 is not the identity. Eighty-six graph-only orbits split into more than one rule-aware orbit: star and triangle contribute 4 splits each for R01–R07, and path contributes 6 splits each for R01, R02, R04, R05, and R06. R00 does not split. R03 and R07 do not split on path, because the path reflection already fixes edge 0-1.

## E. A0 frozen plan

| Item | Value |
| --- | --- |
| Frozen plan commit | `61ed53075238284850e792aff5743f0a8a7b6695` |
| Plan hash | `efbfcf17861878e528e0c359877d65281d695a78e1adaabb105181bd4b68f68d` |
| Plan file | `constraint-lab/exploration/generation-008a/round-a0-plan.json` |
| Decision journey line | journey step 1, commit `439d5545560b62e7e8d4eeea86683c38c3ef0f9a` |
| Tables | `constraint-lab/reports/generation-008a-round-a0-tables.json` |

The plan was pushed before execution. The plan file does not contain its own git SHA.

| System | Parent | Expression |
| --- | --- | --- |
| R00 | S00 | baseline, no rule |
| R01 | S01 | `dissolve(0-1) \| absent(0-1-2) => strong_suppress` |
| R02 | S05 | `form(0-1) \| absent(0-1-2) => strong_suppress` |
| R03 | S10 | `dissolve(0-1) => strong_suppress` |
| R04 | S11 | `dissolve(2-3) \| present(0-1-2) => strong_suppress` |
| R05 | S09 | `dissolve(0-1) => strong_suppress` and `dissolve(2-3) \| present(0-1-2) => strong_suppress` |
| R06 | S12 | `dissolve(0-1) \| absent(0-1-2) => strong_favour` |
| R07 | S16 | `dissolve(0-1) => strong_favour` |

No `prohibit`. Eight systems, 3 source graphs, 16 raw triads, 16 replicates: 6,144 episodes. Pair horizon 512. Full-event cap 16,384. Batch size 120. Smoke replay exact on every episode. Durable replay fraction 0.1, selected by episode-hash.

The predeclared information measures are uniform-raw, uniform rule-aware orbit, and uniform graph-only orbit on this sample, for the first other 3-edge destination; uniform-raw pair class at the checkpoints; and the three current-triad conditionals. The current-triad conditionals were computed for every A0 system. The required subset was R00, R01, R03, R05, R06, and R07. The uniform graph-only figure pools raw members of a Generation 8 orbit on this sample. It is not the Generation 8 published estimate.

## F. Operational record

`verify --require-complete` returned `ok` and `complete` on 6,759 items, 0 problems, spec hash equal to the plan hash. Durable replay: 615 of 615 exact, 0 mismatches. Every stored episode carries `smoke_replay: exact`. A mismatch is refused before the episode item is stored.

| Quantity | Value |
| --- | --- |
| Durable items | 6,759 (6,144 episodes + 615 replays) |
| Batches | 58 |
| Workers | 2 |
| Started | 2026-10-12T21:07:49Z |
| Last activity | 2026-10-12T21:17:21Z |
| Median batch wall | 17.716329 s |
| p90 batch wall | 18.062894 s |
| Maximum batch wall | 19.428333 s |
| Timeouts / retries / quarantines | 0 / 0 / 0 |
| Full events | 5,314,418 |
| Pair events | 3,145,728 |
| Transition markers | 3,145,728 |
| Disk after merge | 678,150,248 bytes |

Median is the wall at index `n // 2` of the 58 sorted batch walls. p90 is nearest-rank index `min(n-1, ceil(0.9 n) - 1)`.

All 6,144 episodes ended at `pair_horizon`. Pair events are 6,144 × 512. No episode was censored.

| Artifact | sha256 |
| --- | --- |
| `merge/atlas.json` | `fe3a71bb3d65f1fb0bf054859356552f75594f6e14eeb5449b7598037bcf2060` |
| `merge/summary.json` | `b95c4862a8513a8dab5cefa056614b15f76e6e7a61691bd5c9ddbf8417b21dd9` |
| `index/transitions.jsonl.gz` | `a98e6fcd0e70b47e07a3aff3c27ef920b334e758cab1508ede136f074c03ecde` |
| `index/class-runs.jsonl.gz` | `6e8182bebbc286f2163e5993d9e0bca907c9173c738bb215cd430d02ddc46155` |

The raw event stream remains the replay source. Episode summaries omit the duplicated marker list. The transition index is streamed once at merge.

## G. Raw-context routing

Raw configuration rows are the primary table. They are in the tables file, 384 rows, each with the 16-replicate destination counts. No symmetry average is applied first. Destination names below are the 3-edge classes: path `e3-deg2211-tri0-comp1`, triangle `e3-deg2220-tri1-comp2`, star `e3-deg3111-tri0-comp1`.

Equal weight on the 16 raw configurations gives these destination shares.

| System | Star to path / triangle | Path to star / triangle | Triangle to path / star |
| --- | --- | --- | --- |
| R00 | 0.68 / 0.32 | 0.52 / 0.48 | 0.69 / 0.31 |
| R01 | 0.68 / 0.32 | 0.53 / 0.47 | 0.67 / 0.33 |
| R02 | 0.68 / 0.32 | 0.49 / 0.51 | 0.67 / 0.33 |
| R03 | 0.71 / 0.29 | 0.45 / 0.55 | 0.67 / 0.33 |
| R04 | 0.74 / 0.26 | 0.52 / 0.48 | 0.70 / 0.30 |
| R05 | 0.75 / 0.25 | 0.56 / 0.44 | 0.75 / 0.25 |
| R06 | 0.70 / 0.30 | 0.50 / 0.50 | 0.71 / 0.29 |
| R07 | 0.66 / 0.34 | 0.50 / 0.50 | 0.72 / 0.28 |

Path continues to split between star and triangle. Star and triangle continue to route mostly through path. The constraint systems move those shares by a few hundredths. They do not replace the route family.

Pairwise Jensen-Shannon divergence among the 16 raw destination distributions, and the occupancy L1, return-rate range, and passage-time range, are below. Median JS is the index `n // 2` of the pairwise values. Return range is the range of the 16 raw-context return-before rates.

| Cell | Max JS | Median JS | Max occupancy L1 | Return range | Passage-time range |
| --- | --- | --- | --- | --- | --- |
| R00 path | 0.1308 | 0.0080 | 0.0994 | 0.312 | 5.50 |
| R00 star | 0.1124 | 0.0091 | 0.0931 | 0.250 | 1.88 |
| R00 triangle | 0.2158 | 0.0091 | 0.0885 | 0.375 | 3.38 |
| R01 path | 0.0995 | 0.0084 | 0.0775 | 0.500 | 8.25 |
| R01 star | 0.0776 | 0.0091 | 0.0821 | 0.438 | 2.50 |
| R01 triangle | 0.1124 | 0.0084 | 0.0802 | 0.438 | 1.75 |
| R02 path | 0.0734 | 0.0080 | 0.0629 | 0.250 | 3.25 |
| R02 star | 0.0861 | 0.0080 | 0.0719 | 0.375 | 2.50 |
| R02 triangle | 0.1424 | 0.0091 | 0.0714 | 0.312 | 2.88 |
| R03 path | 0.0721 | 0.0080 | 0.0938 | 0.375 | 6.25 |
| R03 star | 0.2903 | 0.0197 | 0.0621 | 0.375 | 2.62 |
| R03 triangle | 0.1124 | 0.0084 | 0.0843 | 0.438 | 3.25 |
| R04 path | 0.1687 | 0.0078 | 0.0807 | 0.375 | 6.38 |
| R04 star | 0.0631 | 0.0084 | 0.0680 | 0.438 | 3.25 |
| R04 triangle | 0.0861 | 0.0105 | 0.0629 | 0.312 | 2.38 |
| R05 path | 0.1034 | 0.0080 | 0.0721 | 0.438 | 7.12 |
| R05 star | 0.1307 | 0.0058 | 0.0802 | 0.438 | 2.12 |
| R05 triangle | 0.2158 | 0.0186 | 0.0789 | 0.312 | 2.12 |
| R06 path | 0.1687 | 0.0178 | 0.0958 | 0.250 | 7.25 |
| R06 star | 0.1028 | 0.0084 | 0.0953 | 0.375 | 2.38 |
| R06 triangle | 0.1307 | 0.0091 | 0.0948 | 0.188 | 2.12 |
| R07 path | 0.0995 | 0.0084 | 0.0877 | 0.375 | 11.00 |
| R07 star | 0.1124 | 0.0105 | 0.0853 | 0.312 | 3.12 |
| R07 triangle | 0.0432 | 0.0024 | 0.0950 | 0.500 | 3.50 |

The typical pair of raw contexts is close: median destination JS is about 0.008 to 0.020. The largest single pair is R03 star `t08` against `t13`, JS 0.2903. Their 16-replicate counts are `t08` 6 path and 10 triangle, and `t13` 16 path. Their dense-minus-sparse values are +0.1809 and +0.1847. The destination tail and the occupancy coordinate do not move together in that pair.

Three raw cells sent all 16 replicates to one destination, in each case the path class: R00 triangle `t00`, R03 star `t13`, and R05 triangle `t02`. This is a reading of the predeclared destination counts. The same kind of 16/16 path cell that Generation 8 recorded for S08 star-o00 recurs on this palette, including on baseline.

Return-before rates range by 0.19 to 0.50 across the 16 contexts of a cell. Passage-time ranges are largest on path. Both are also large inside baseline, so section K compares them with within-orbit sampling before they are read as context effects.

## H. Raw-context occupancy

The coordinate is dense minus sparse: the share of pair-epochs on 4, 5, or 6 edges, minus the share on 0, 1, or 2 edges. The 3-edge layer is the remainder. Each system has 768 episodes and 393,984 pair-epochs, including the initial epoch. Shares use that support. The within-system span is the range of the 48 raw-context means.

| System | Sparse | 3-edge | Dense | Dense − sparse | L1 to R00 | Within-system dense − sparse span |
| --- | --- | --- | --- | --- | --- | --- |
| R05 composite suppress | 0.2275 | 0.3072 | 0.4653 | +0.2378 | 0.2535 | 0.0699 |
| R03 unconditional dissolve suppress | 0.2567 | 0.3138 | 0.4295 | +0.1728 | 0.1729 | 0.0880 |
| R01 conditional dissolve suppress | 0.3072 | 0.3133 | 0.3795 | +0.0723 | 0.0708 | 0.0819 |
| R04 off-edge conditional suppress | 0.3083 | 0.3142 | 0.3774 | +0.0691 | 0.0679 | 0.0647 |
| R00 baseline | 0.3414 | 0.3139 | 0.3447 | +0.0033 | 0 | 0.0911 |
| R02 conditional form suppress | 0.3782 | 0.3148 | 0.3071 | −0.0711 | 0.0762 | 0.0707 |
| R06 conditional dissolve favour | 0.3858 | 0.3139 | 0.3004 | −0.0854 | 0.0899 | 0.0863 |
| R07 unconditional dissolve favour | 0.4159 | 0.3130 | 0.2711 | −0.1448 | 0.1494 | 0.0866 |

The 3-edge layer stays near 0.314 except on R05, where it is 0.3072. Finite suppress moves mass toward the dense side. Finite favour moves mass toward the sparse side. The within-system span across raw contexts is about 0.06 to 0.09, smaller than the unconditional system shift and comparable to the conditional system shift.

For conditional systems the frozen crosswalk records whether the conditioning triad is present in the initial state. Grouping the 16 raw contexts by that bit, with equal context weight, moves mean dense-minus-sparse by at most 0.0144 (R01 path, absent +0.0819 against present +0.0675). Baseline and the unconditional rules have no condition bit, so that coordinate does not distinguish their 16 starts. The initial condition bit is not the organiser of the edge-count axis.

Triad-only fractions stay inside about 0.37 to 0.44. R05 sits highest, about 0.428 to 0.445. R07 sits lowest, about 0.368 to 0.385. The within-system range of that fraction is about 0.02.

## I. Initial-context information

All figures are in nats. The uniform raw prior gives each of the 16 triad configurations equal weight. The uniform rule-aware and uniform graph-only figures give each orbit equal weight and mix raw members inside an orbit equally. When the rule-aware partition is 16 singletons, the rule-aware number equals the raw number. That equality is present for R01, R02, R04, R05, and R06 on star and on path. When the rule-aware group equals the source-graph group, the rule-aware number equals the graph-only number. That equality is present for all three R00 sources and for R03 path and R07 path.

`I(raw initial triad; first other 3-edge destination)`:

| Cell | Uniform raw | Uniform rule-aware orbit | Uniform graph-only orbit on this sample | Raw minus graph-only |
| --- | --- | --- | --- | --- |
| R00 star | 0.0321 | 0.0111 | 0.0111 | +0.0210 |
| R00 path | 0.0307 | 0.0238 | 0.0238 | +0.0069 |
| R00 triangle | 0.0434 | 0.0552 | 0.0552 | −0.0118 |
| R01 star | 0.0291 | 0.0291 | 0.0215 | +0.0076 |
| R01 path | 0.0310 | 0.0310 | 0.0181 | +0.0129 |
| R01 triangle | 0.0247 | 0.0273 | 0.0203 | +0.0044 |
| R02 star | 0.0212 | 0.0212 | 0.0093 | +0.0119 |
| R02 path | 0.0261 | 0.0261 | 0.0236 | +0.0025 |
| R02 triangle | 0.0352 | 0.0189 | 0.0093 | +0.0259 |
| R03 star | 0.0702 | 0.0605 | 0.0544 | +0.0158 |
| R03 path | 0.0232 | 0.0155 | 0.0155 | +0.0078 |
| R03 triangle | 0.0283 | 0.0244 | 0.0140 | +0.0143 |
| R04 star | 0.0209 | 0.0209 | 0.0135 | +0.0073 |
| R04 path | 0.0326 | 0.0326 | 0.0101 | +0.0225 |
| R04 triangle | 0.0317 | 0.0245 | 0.0173 | +0.0144 |
| R05 star | 0.0277 | 0.0277 | 0.0369 | −0.0091 |
| R05 path | 0.0288 | 0.0288 | 0.0133 | +0.0155 |
| R05 triangle | 0.0567 | 0.0487 | 0.0232 | +0.0335 |
| R06 star | 0.0275 | 0.0275 | 0.0080 | +0.0195 |
| R06 path | 0.0467 | 0.0467 | 0.0394 | +0.0073 |
| R06 triangle | 0.0308 | 0.0204 | 0.0095 | +0.0213 |
| R07 star | 0.0382 | 0.0439 | 0.0279 | +0.0103 |
| R07 path | 0.0325 | 0.0219 | 0.0219 | +0.0106 |
| R07 triangle | 0.0127 | 0.0089 | 0.0041 | +0.0086 |

The largest uniform-raw value is 0.0702 nats, R03 star. The largest raw-minus-graph-only gap on this sample is +0.0335 nats, R05 triangle. Two gaps are negative, because equal orbit weight is a different prior from equal raw-config weight. Raw contingency counts for these three estimands are in the tables file.

`I(raw initial triad; pair class at checkpoint)`, same uniform raw prior:

| Checkpoint | Minimum | Median | Maximum | Maximum cell |
| --- | --- | --- | --- | --- |
| 1 | 0.0165 | 0.0347 | 0.1444 | R06 path |
| 2 | 0.0950 | 0.1247 | 0.1866 | R01 path |
| 32 | 0.0941 | 0.1254 | 0.1695 | R02 star |
| 64 | 0.0916 | 0.1415 | 0.1599 | R03 path |
| 512 | 0.0968 | 0.1228 | 0.1798 | R01 star |

From checkpoint 2 through 512 the median stays between 0.1228 and 0.1415. It does not fall away by checkpoint 32 or 64.

The route-outcome information, which is the first other 3-edge destination on the prefix and which includes `censored_at_horizon` while episodes have not yet arrived, is 0 at checkpoint 1. One pair toggle cannot land on another 3-edge class. By checkpoint 32 the maximum is 0.0783 nats. At checkpoints 64, 128, and 512 the maximum is 0.0702 nats, on R03 star, matching the full-horizon uniform-raw destination information. That quantity locks. It does not wash out, and it does not grow after the first destination has been reached. The checkpoint pair-class information is a different estimand, and it persists.

## J. Current-context information

The next pair event in the slot estimands is the pair-slot index 0..5. Direction is the pre-state bit of that slot. Weights are pair events. These are not the uniform raw-triad prior.

| Cell | I(current triad; next pair class \| pair class) | I(current triad; next slot \| pair class) | I(current triad; next slot \| full pair mask) |
| --- | --- | --- | --- |
| R00 path | 0.00092 | 0.00311 | 0.01818 |
| R00 star | 0.00120 | 0.00311 | 0.01919 |
| R00 triangle | 0.00100 | 0.00327 | 0.01889 |
| R01 path | 0.00179 | 0.01148 | 0.03110 |
| R01 star | 0.00212 | 0.01017 | 0.03010 |
| R01 triangle | 0.00190 | 0.01180 | 0.03139 |
| R02 path | 0.00191 | 0.01087 | 0.03047 |
| R02 star | 0.00206 | 0.01087 | 0.03049 |
| R02 triangle | 0.00189 | 0.01168 | 0.03176 |
| R03 path | 0.00101 | 0.00327 | 0.01883 |
| R03 star | 0.00085 | 0.00331 | 0.01812 |
| R03 triangle | 0.00087 | 0.00308 | 0.01843 |
| R04 path | 0.00198 | 0.01072 | 0.02966 |
| R04 star | 0.00171 | 0.01030 | 0.02939 |
| R04 triangle | 0.00195 | 0.01071 | 0.03061 |
| R05 path | 0.00351 | 0.01311 | 0.03325 |
| R05 star | 0.00354 | 0.01328 | 0.03284 |
| R05 triangle | 0.00323 | 0.01257 | 0.03126 |
| R06 path | 0.00225 | 0.01075 | 0.03555 |
| R06 star | 0.00197 | 0.01044 | 0.03624 |
| R06 triangle | 0.00223 | 0.01061 | 0.03515 |
| R07 path | 0.00123 | 0.00313 | 0.01915 |
| R07 star | 0.00078 | 0.00310 | 0.01781 |
| R07 triangle | 0.00091 | 0.00318 | 0.01825 |

Conditioning on the isomorphism class gives very small information about the next pair class, 0.00078 to 0.00354 nats. The same current triad carries more information about the next pair slot when the conditioner is the full 6-bit pair mask: about 0.018 nats on baseline and on the unconditional dissolves, and about 0.030 to 0.036 nats on the five systems whose rule has a triad condition. The class-conditional slot figure sits between them, near 0.003 without a triad condition and near 0.011 to 0.013 with one. Small information given only the isomorphism class is not the same statement as dynamic irrelevance. The mask figure is larger, and it is still small beside `log(6)` for a six-way slot. Raw cell counts for all three counters are in the tables file.

Compared with section I, the current triad's information about the next pair class is smaller than the initial triad's information about the first destination. The current triad's information about the next slot given the full mask is similar in size to the typical initial-destination information, and smaller than the persistent checkpoint pair-class information.

## K. Rule-aware orbit consistency

For each rule-aware orbit with more than one raw context, the tables record the within-orbit maximum destination JS, occupancy L1, and return-rate range. The source-level within-orbit figures below are the maxima of those orbit figures. Split figures are the maximum pairwise destination JS and occupancy L1 among raw contexts that share a Generation 8 graph-only orbit and do not share a rule-aware orbit. A blank within-orbit cell means every rule-aware orbit is a singleton. A blank split cell means the graph-only partition was not refined.

| Cell | Within-orbit max JS | Within-orbit max L1 | Within-orbit return range | Split max JS | Split max L1 | Split return range |
| --- | --- | --- | --- | --- | --- | --- |
| R00 path | 0.0516 | 0.0538 | 0.250 |  |  |  |
| R00 star | 0.1124 | 0.0770 | 0.250 |  |  |  |
| R00 triangle | 0.0221 | 0.0643 | 0.375 |  |  |  |
| R01 path |  |  |  | 0.0499 | 0.0704 | 0.438 |
| R01 star |  |  |  | 0.0556 | 0.0799 | 0.438 |
| R01 triangle | 0.0197 | 0.0716 | 0.250 | 0.0321 | 0.0770 | 0.438 |
| R02 path |  |  |  | 0.0316 | 0.0524 | 0.250 |
| R02 star |  |  |  | 0.0631 | 0.0592 | 0.375 |
| R02 triangle | 0.1034 | 0.0456 | 0.250 | 0.0631 | 0.0551 | 0.312 |
| R03 path | 0.0183 | 0.0541 | 0.312 |  |  |  |
| R03 star | 0.1229 | 0.0365 | 0.250 | 0.1827 | 0.0482 | 0.375 |
| R03 triangle | 0.0178 | 0.0560 | 0.188 | 0.0516 | 0.0565 | 0.438 |
| R04 path |  |  |  | 0.1335 | 0.0592 | 0.375 |
| R04 star |  |  |  | 0.0432 | 0.0573 | 0.438 |
| R04 triangle | 0.0338 | 0.0509 | 0.188 | 0.0861 | 0.0402 | 0.250 |
| R05 path |  |  |  | 0.0516 | 0.0677 | 0.438 |
| R05 star |  |  |  | 0.0264 | 0.0604 | 0.438 |
| R05 triangle | 0.0556 | 0.0582 | 0.188 | 0.2158 | 0.0789 | 0.312 |
| R06 path |  |  |  | 0.0371 | 0.0575 | 0.250 |
| R06 star |  |  |  | 0.0776 | 0.0921 | 0.375 |
| R06 triangle | 0.0353 | 0.0463 | 0.188 | 0.0861 | 0.0655 | 0.188 |
| R07 path | 0.0499 | 0.0763 | 0.250 |  |  |  |
| R07 star | 0.0029 | 0.0631 | 0.250 | 0.0861 | 0.0485 | 0.312 |
| R07 triangle | 0.0264 | 0.0409 | 0.188 | 0.0264 | 0.0858 | 0.375 |

Baseline star, whose rule-aware group is the full source group, already has within-orbit destination JS 0.1124. That is sampling variation among raw contexts that the symmetry says are equivalent, at 16 replicates. R03 star's split JS of 0.1827 sits above that floor. R05 triangle's split JS of 0.2158 sits well above its within-orbit JS of 0.0556. R02 triangle's within-orbit JS of 0.1034 is larger than its split JS. Return ranges inside true baseline orbits are already 0.25 to 0.375, so a split return range of similar size is not, by itself, evidence that the old quotient hid a stable return effect.

The clearest split excesses are R05 triangle on destination and R03 star on destination. Their median pairwise JS values remain 0.0186 and 0.0197. The excess is a tail, not the typical pair.

## L. Generation 8 graph-only versus 8A raw comparison

Generation 8 `episode_equal` gives equal weight to each graph-only orbit and uses only that orbit's canonical representative. Generation 8 `configuration_weighted` weights those same representative samples by orbit size. Neither is the uniform raw estimand, and neither is the uniform graph-only pooling of this sample. The numerical difference is recorded with those labels. It is not one effect.

| Cell | Gen 8 orbit-equal | Gen 8 configuration-weighted | 8A uniform raw | 8A rule-aware | 8A graph-only on this sample |
| --- | --- | --- | --- | --- | --- |
| R00 / S00 star | 0.0134 | 0.0107 | 0.0321 | 0.0111 | 0.0111 |
| R00 / S00 path | 0.0155 | 0.0163 | 0.0307 | 0.0238 | 0.0238 |
| R00 / S00 triangle | 0.0153 | 0.0178 | 0.0434 | 0.0552 | 0.0552 |
| R01 / S01 star | 0.0209 | 0.0207 | 0.0291 | 0.0291 | 0.0215 |
| R01 / S01 path | 0.0448 | 0.0524 | 0.0310 | 0.0310 | 0.0181 |
| R01 / S01 triangle | 0.0298 | 0.0252 | 0.0247 | 0.0273 | 0.0203 |
| R02 / S05 star | 0.0197 | 0.0168 | 0.0212 | 0.0212 | 0.0093 |
| R02 / S05 path | 0.0356 | 0.0393 | 0.0261 | 0.0261 | 0.0236 |
| R02 / S05 triangle | 0.0179 | 0.0192 | 0.0352 | 0.0189 | 0.0093 |
| R03 / S10 star | 0.0053 | 0.0053 | 0.0702 | 0.0605 | 0.0544 |
| R03 / S10 path | 0.0218 | 0.0272 | 0.0232 | 0.0155 | 0.0155 |
| R03 / S10 triangle | 0.0192 | 0.0110 | 0.0283 | 0.0244 | 0.0140 |
| R04 / S11 star | 0.0079 | 0.0086 | 0.0209 | 0.0209 | 0.0135 |
| R04 / S11 path | 0.0158 | 0.0168 | 0.0326 | 0.0326 | 0.0101 |
| R04 / S11 triangle | 0.0256 | 0.0206 | 0.0317 | 0.0245 | 0.0173 |
| R05 / S09 star | 0.0237 | 0.0145 | 0.0277 | 0.0277 | 0.0369 |
| R05 / S09 path | 0.0408 | 0.0389 | 0.0288 | 0.0288 | 0.0133 |
| R05 / S09 triangle | 0.0451 | 0.0314 | 0.0567 | 0.0487 | 0.0232 |
| R06 / S12 star | 0.0309 | 0.0377 | 0.0275 | 0.0275 | 0.0080 |
| R06 / S12 path | 0.0368 | 0.0375 | 0.0467 | 0.0467 | 0.0394 |
| R06 / S12 triangle | 0.0242 | 0.0208 | 0.0308 | 0.0204 | 0.0095 |
| R07 / S16 star | 0.0271 | 0.0374 | 0.0382 | 0.0439 | 0.0279 |
| R07 / S16 path | 0.0298 | 0.0347 | 0.0325 | 0.0219 | 0.0219 |
| R07 / S16 triangle | 0.0328 | 0.0326 | 0.0127 | 0.0089 | 0.0041 |

On this palette the Generation 8 orbit-equal maximum is 0.0451 nats, S09 triangle. The Generation 8 generation-wide maximum of 0.0631 nats was S08 triangle, which is not in the repair palette. The largest 8A uniform-raw value, 0.0702 on R03 star, is the cell whose Generation 8 orbit-equal value was 0.0053. The same cell's graph-only pooling on the 8A sample is 0.0544. Most of that rise relative to 0.0053 is already present after graph-only pooling of the new sample, so it is not only the further split into rule-aware orbits. Seed schedule and which raw states were executed both changed. Section K's within-orbit floor says a 16-replicate destination distribution is sampling-sensitive.

For the 208 Generation 8 canonical representatives, the destination JS between the Generation 8 16-replicate sample and the Round A0 16-replicate sample of the same raw state has median 0.0084 and maximum 0.1827. The maximum is R00 triangle `t00`, the baseline cell that was 16/16 path in Round A0. Exact equality was not expected. The bulk of the paired representatives agree closely. The tail moves.

## M. Edge-count axis under corrected sampling

The finite-grade order on the copied expressions remains visible under exhaustive context starts.

| Expression family | Generation 8 dense − sparse | Round A0 dense − sparse |
| --- | --- | --- |
| Baseline | S00 +0.0061 | R00 +0.0033 |
| Conditional dissolve, strong suppress | S01 +0.0645 | R01 +0.0723 |
| Conditional form, strong suppress | S05 −0.0617 | R02 −0.0711 |
| Unconditional dissolve, strong suppress | S10 +0.1684 | R03 +0.1728 |
| Off-edge conditional dissolve, strong suppress | S11 +0.0697 | R04 +0.0691 |
| Two-rule composite, strong suppress | S09 +0.2399 | R05 +0.2378 |
| Conditional dissolve, strong favour | S12 −0.0841 | R06 −0.0854 |
| Unconditional dissolve, strong favour | S16 −0.1396 | R07 −0.1448 |

Strong suppress and strong favour sit on opposite sides of baseline for both the conditional dissolve and the unconditional dissolve. The off-edge conditional suppress remains near the conditional dissolve suppress, not near the unconditional suppress. The 3-edge layer remains the stable middle. These are independent samples. The order matches.

The predeclared residual is the R05 11-class share minus (R03 share + R04 share − R00 share). Its L1 is 0.0640. Generation 8 reported 0.0698 for the parent systems. The one-dimensional dense-minus-sparse residual on the Round A0 shares is −0.0008: 0.2378 − (0.1728 + 0.0691 − 0.0033). The class-share residual is spread across the 11 classes, with absolute pieces from about 0.0016 to 0.0089. The largest pieces are the path class, +0.0089, and `e4-deg3221-tri1-comp1`, −0.0088. No class carries a private route-sized residual. The source-routing table in section G does not show a route family that appears only under R05.

## N. Unexpected observations

The largest destination disagreement is an occupancy agreement. R03 star `t08` and `t13` differ by JS 0.2903 and by dense-minus-sparse of only 0.0038.

Initial-triad information about the pair class at a late checkpoint stays near 0.12 nats, while initial-triad information about the first destination stays at or below 0.0702 nats. The context signal that persists is not the first route label.

Full-mask conditioning and isomorphism-class conditioning separate cleanly, and they separate by whether the rule has a triad condition. That gap was not visible in a class-only conditional.

A 16/16 path cell occurs on baseline. It is not special to a labelled constraint.

Rule-aware orbits are not uniformly tighter than the 16-replicate floor. R00 star inside a true symmetry orbit already reaches JS 0.1124.

## O. Inferences

These readings stay inside the sampled family: N=4, O=3, horizon 512, the eight copied systems, and 16 replicates.

Graph-only quotienting was the wrong symmetry for every labelled system in the palette. On star and path the conditional and off-edge rules reduce the group to the identity. Executing all 16 raw starts was the correction. After those starts exist, the additional first-destination information in the raw prior, beyond equal weight on the graph-only orbits of this same sample, is at most 0.0335 nats and is sometimes negative. The formal flaw is observed in the groups. A large numerical suppression of first-destination information is not observed on this palette.

The edge-count coordinate remains the strong organiser across systems. Hidden context moves it inside a system by about 0.06 to 0.09, which is real on these replicate counts and smaller than the unconditional grade shift. The initial condition-present bit does not account for that within-system span.

First destination remains context-insensitive in the bulk. Median JS near 0.01, and uniform-raw mutual information at most 0.0702 nats, are the bulk description. The maximum JS values are sampling-sensitive: the baseline within-orbit floor is already 0.11, and the same raw state can move by JS 0.18 between the Generation 8 seed and the Round A0 seed. R03 star and R05 triangle are the tails most worth a later paired resample if a later round is opened. They are not, on this sample, a reorganisation of the route family.

Current triad context is alignment-specific and small. It is larger for rules that name a triad, and larger when the conditioner keeps the labelled pair mask. It is not larger than the persistent initial-triad information about the late pair class. Initial context is not forgotten by pair event 32 or 64 on that class coordinate. The first-destination coordinate has already locked by then.

The composite remains non-additive on the 11-class share and nearly additive on dense-minus-sparse. That is the same pattern Generation 8 reported, restated with the scalar and the class vector separated.

The seventeen repair questions, answered from the observations above:

1. The groups are the table in section D.
2. Rule-aware orbit counts are 8 or 10 where the group is the full source group, 16 where the group is trivial, and 12 where the group has order 2 and is not the full source group.
3. Eighty-six graph-only orbits split. R00 does not. R03 and R07 do not split on path.
4. Maximum destination JS is 0.2903. Median JS is about 0.008 to 0.020.
5. Maximum occupancy L1 between raw contexts is 0.0994, on baseline path.
6. Return-before ranges are 0.188 to 0.500, and baseline within-orbit ranges are already 0.250 to 0.375.
7. Uniform-raw mutual information is at most 0.0702 nats. The largest gap versus graph-only pooling of this sample is +0.0335 nats. The Generation 8 orbit-equal numbers are a different estimand and are tabulated in section L.
8. A 16/16 path cell recurs, three times, including on baseline.
9. First-destination information locks by checkpoint 32 to 64. Pair-class information at the checkpoint does not wash out.
10. Current-triad information about the next pair class is smaller than initial-triad information about the first destination. Current-triad information about the next slot given the full mask is similar to the typical initial-destination information and smaller than the persistent checkpoint class information.
11. Full-mask conditioning reveals more current-triad dependence than isomorphism-class conditioning, for the slot variable.
12. The extra mask-conditional information concentrates on rules that name a triad. The initial condition-present bit does not concentrate the edge-count shift.
13. The finite-grade edge-count order remains visible.
14. The S09-type class-share residual remains non-zero, L1 0.0640. The dense-minus-sparse residual is −0.0008.
15. Visible-source routing, the 3-edge layer, the grade order, the unconditional reversal, and the absence of a private composite route survive.
16. The graph-only orbit basis does not survive as an execution basis. The numerical claim that first-destination context information is small does survive, with the measure labelled, and the class-only conditional does not survive as a sufficient description of current-triad dependence.
17. The observation that should drive a later round, if one is opened, is the persistent checkpoint pair-class information near 0.12 nats, together with the sampling-sensitive destination tails. Section Q records that choice as deferred.

## P. RS / global-coherence interpretation

The repair says something about this toy relational dynamics. Exhaustive hidden triad starts do not hand the first route to the hidden triad. They leave a modest, persistent shift in which pair classes are occupied, organised more strongly by the finite grade and the visible source graph than by the initial triad label. A labelled rule does make the current triad slightly more informative about the next pair slot once the labelled pair mask is kept in view. That is evidence about this grammar, this horizon, and these observables.

It is not evidence that a physical system implements the grammar. A small context effect here does not refute a higher-order relational ontology. It says this observable, on this family, is not strongly controlled by the initial hidden triad. No designer and no ultimate receiver is inferred from the trajectories.

## Q. Next exploration options

Round A1 is not opened. The methodological repair is coherent: the symmetry groups are calculated, every raw context was executed, and the first-destination information stayed small under the corrected prior. The edge-count axis did not depend on the graph-only quotient. A further round is permitted and is not required.

Five candidates were considered. Attention vectors are ordinals from 0 to 5. They are not summed.

| Candidate | CN | RD | RC | EC | CG | CB |
| --- | --- | --- | --- | --- | --- | --- |
| Paired-RNG resample, 64 replicates, of the largest destination-JS pairs, with R00 triangle as the sampling floor | 3 | 4 | 2 | 3 | 2 | 4 |
| Analysis only, on the stored A0 streams: separate checkpoint pair-class information into edge count and class given edge count | 4 | 1 | 2 | 5 | 4 | 5 |
| Raw-context rerun of the weak grades on the conditional dissolve | 2 | 1 | 1 | 4 | 4 | 3 |
| Raw-context rerun of the opposite condition polarity on the same structural dissolve | 2 | 2 | 1 | 3 | 3 | 3 |
| A hard `prohibit` on the unconditional dissolve | 1 | 1 | 1 | 1 | 2 | 2 |

None is chosen. The paired resample would test a tail that the median and the mutual information already bound. The checkpoint decomposition is the most informative unused reading, and it can wait, because the report already separates first destination from late pair class without that extra cut. The weak grades and the polarity flip ask questions the grade order and the condition-bit grouping have already narrowed. Prohibit has no support-boundary observation: every episode reached the pair horizon with admissible events. Round A2 is not opened.
