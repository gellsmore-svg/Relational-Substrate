# Generation 003c — two clocks for the Generation 3 memory

This is a reanalysis of the kernels Generation 3 already measured. It does not replace `generation-003-independent-triadic-relation` or `generation-003b-k3-singletons`, and it does not edit their reports.

Engine `0.3.0`. Semantic version `0.3.0`. Those identities stay on the N=3 independent-hypergraph kernels. The new analysis name is `memory-clock-reanalysis`. Grammar `independent-hypergraph-v1`. Normalisation `structural-unique-v1`.
Specification hash `b3940305e0c8ed69e9a80faa39d98964893f52563a2f13645c8f338ee22e4020`.
Summary SHA-256 `37c2d96c698f73431ae80d09170eae1b3d84f6e9fbfdcd4f2bbd9b0fd2ae1630`.
Row table SHA-256 `bb5a535b4291e53d07ead37c6a3016e63035c0e66141ffbfd9201ea13ee177a8` (`reports/tables/generation-003c-memory-clock-refinement-singles-n3-k2.csv`, 7,386 lines including the header, 1,768,428 bytes).
Plan git commit `90ad68fc0e55333335412dfa3af5c7081b60c918`. The summary field `git_commit` is that same commit: the completing merge ran before the analysis commit that contains this report.

Workers 2. Shards 11. Quarantined 0. Failed 0.
The invocation that executed the shards ran for 129.27 seconds and then stopped in the merge, because the historical-reducibility check required two zero counts that a counter omits when they are zero. The three nonzero class counts already matched Generation 3. The check was changed to treat a missing class as zero. The completing invocation found every shard already receipted, merged in 0.210 seconds, and wrote `runtime_seconds` 0.210. That field is the completing invocation, not the shard execution. Shard-work across the 11 receipts is 248.268 seconds.

Coordinate, unchanged from Generation 3:

```text
N=3  O=3  G=0  S=0  H=0  L=0
K<=2  cardinalities {1, 2}  structural-simple  W4
independent hypergraph
```

Cardinality 1 contributed 80 canonical sets. Cardinality 2 contributed 7,305. The analysed total is 7,385.

`rho3 = 1` is the primary row. `rho3 = 1/2` and `rho3 = 2` are recomputed inside the same shards for the two clocks, the pair-jump boolean, and the triad-rate boolean. Alphabet sensitivity was not part of this reanalysis.

## A. The two clocks

The full chain on the 16 relational states remains first-order Markov. A positive total variation below is memory of a coarse-graining, not memory of the full relational state.

`FULL_EVENT_CLOCK_MEMORY` is the Generation 3 statistic. The observer sees the pairwise state after every full-system event, including an event that toggles only the triad. A triad-only event while the pairs stay fixed is a visible self-loop. The exact value is `full_event_clock_memory_tv`. On these kernels it equals `emergent_memory_tv`. The census reproduced Generation 3's count: 5,250 of 7,385 sets have positive full-event-clock memory.

`PAIR_EVENT_EPOCH_MEMORY` observes the pairwise state only when a pairwise relation toggles. Stopping times `τ_i` are those toggles. `Q_i` is the pairwise state at `τ_i`, after the toggle. The total variation compares `P(Q_{i+1} | Q_i)` with `P(Q_{i+1} | Q_i, Q_{i-1})` under the stationary flux of pair-changing steps. Triad-only excursions are summed out of the epoch kernel. A missing epoch mass is recorded as a defect and is not called zero memory. In this census every epoch total variation was defined and every defect was zero. Undefined did not occur.

The epoch information quantities are not renames of the full-event quantities. `I(T of Y_i ; Q_{i+1} | Q_i)` and `I(Q_i ; T of Y_{i+1} | T of Y_i)` use the pair-event clock. `Y_i` is the full state at the pair event.

## B. Axes

Generation 3's reducibility label is retained as `historical_reducibility`. It is not the taxonomy. The reanalysis uses separate axes.

| Axis | Question | Values used here |
| --- | --- | --- |
| A | Does the triadic bit change the conditional law of the next pair toggle? | `NO` / `YES`, plus the exact jump total variation |
| B | Does the pair state change the triadic toggle probability? | `NO` / `YES` for the normalised rate, and a separate flag for the un-normalised triad weight |
| C | Full-event-clock memory | `zero` / `positive`, exact total variation |
| D | Pair-event-epoch memory | `zero` / `positive`, exact total variation |
| E | Are the conditional pair-jump kernels in the searched Generation 1b N=3 grammar? | `inside` / `outside` / `unresolved` |

Axis A is a property of the kernel at every non-deadlock state with a positive pair weight. It is not restricted to states charged by the stationary distribution. Axis E skips a slice that has halted. Every comparable slice in this census was inside the searched grammar. Outside was 0. Unresolved was 0.

Axis B's rate flag is the broader one. A change in pair weights at a fixed triad weight changes the probability of the triad toggle by competition, even when the un-normalised triad weight is constant. The two flags disagree on 4,339 sets:

| Triad rate | Triad weight | Sets |
| --- | --- | ---: |
| yes | no | 4,331 |
| yes | yes | 2,942 |
| no | no | 104 |
| no | yes | 8 |

The historical label was reproduced exactly: `FULLY_REDUCIBLE` 2,295, `PAIRWISE_PROJECTION_REDUCIBLE` 2,150, `IRREDUCIBLE_DYNAMIC_COUPLING` 2,940, outside 0, unresolved 0. Class counts were reproduced exactly: `P->P` 1,890, `P->T` 380, `T->P` 380, `T->T` 35, mixed 4,700.

## C. Cross-tabulation

All 7,385 sets. No cell with epoch memory and a negative jump flag exists. No cell with positive full-event memory, positive jump dependence, and zero epoch memory exists.

| Pair jump | Full-event clock | Pair-event epoch | Triad rate | Sets |
| --- | --- | --- | --- | ---: |
| no | positive | zero | no | 28 |
| no | positive | zero | yes | 2,336 |
| no | zero | zero | no | 46 |
| no | zero | zero | yes | 2,025 |
| yes | positive | positive | no | 18 |
| yes | positive | positive | yes | 2,868 |
| yes | zero | zero | no | 20 |
| yes | zero | zero | yes | 44 |

By pure cross-order class. A cardinality-2 set is pure when both constraints have that class. Mixed means the two constraints have different classes.

| Class | Sets | Full-event positive | Epoch positive | Epoch zero |
| --- | ---: | ---: | ---: | ---: |
| `P->P` | 1,890 | 0 | 0 | 1,890 |
| `P->T` | 380 | 368 | 0 | 380 |
| `T->P` | 380 | 370 | 370 | 10 |
| `T->T` | 35 | 20 | 0 | 35 |
| mixed | 4,700 | 4,492 | 2,516 | 2,184 |

The 10 pure `T->P` sets with zero epoch memory are cardinality-2 pairs that put the same weight on `present(0-1-2)` and on `absent(0-1-2)`. Their jump total variation is zero. The rate flag can still be true. They also have zero full-event memory.

## D. Answers

1. Of the 5,250 full-event-memory sets, 2,886 retain positive memory at pair-event epochs.
2. 2,364 lose all of that memory when triad-only events are skipped. None became undefined.
3. Pure `T->P`: 370 of 380 retain pair-event-epoch memory. The other 10 have jump total variation zero, as above.
4. Pure `P->T`: 0 of 380 retain pair-event-epoch memory. 368 of them have positive full-event memory.
5. Pure `T->T`: 0 of 35 retain pair-event-epoch memory. 20 of them have positive full-event memory.
6. No set in this census has zero pair-jump dependence and positive pair-event-epoch memory.
7. Yes. 64 sets have pair-jump dependence and zero pair-event-epoch memory. All 64 also have zero full-event memory. On each of them, the distinct jump laws are not both charged by the stationary distribution reached from state 0. Twenty of the 64 differ only on states of stationary mass zero. The other 44 put positive mass on a pair state where the laws differ, but only one of the two triadic slices at that pair state is charged. A visited difference between two charged slices does not occur among these 64. Under the kernel definition of axis A, jump dependence without epoch memory occurs. Under the restriction to slices the stationary chain actually charges, it does not occur in this census.
8. The largest pair-event-epoch total variation is `464/4305`, on a mixed cardinality-2 set: `form(0-1) | absent(0-1-2) => prohibit` and `form(0-1-2) | absent(0-1) => strong_suppress`. Pair jump is true. Triad rate is true.
9. The six Generation 3 reference rules separate on these axes. Values at `rho3 = 1`:

| Rule | Class | Historical label | Jump | Rate | Weight | Full-event | Epoch |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `form(0-1) => strong_favour` | `P->P` | `FULLY_REDUCIBLE` | no, `0/1` | yes | no | `0/1` | `0/1` |
| `form(0-1-2) => strong_favour` | `T->T` | `FULLY_REDUCIBLE` | no, `0/1` | no | no | `81/1288` | `0/1` |
| `form(0-1-2) \| present(0-1) => strong_favour` | `P->T` | `PAIRWISE_PROJECTION_REDUCIBLE` | no, `0/1` | yes | yes | `351/9520` | `0/1` |
| `dissolve(0-1-2) \| present(0-1) => prohibit` | `P->T` | `PAIRWISE_PROJECTION_REDUCIBLE` | no, `0/1` | yes | yes | `1/16` | `0/1` |
| `form(0-1) \| present(0-1-2) => strong_favour` | `T->P` | `IRREDUCIBLE_DYNAMIC_COUPLING` | yes, `1/3` | yes | no | `27/616` | `34/1485` |
| `dissolve(0-1) \| present(0-1-2) => strong_favour` | `T->P` | `IRREDUCIBLE_DYNAMIC_COUPLING` | yes, `1/3` | yes | no | `27/616` | `34/1485` |

The bare triadic favour is the clean split between the clocks: full-event memory `81/1288`, epoch memory 0, jump false, rate false, weight false. The two `T->P` references keep both clocks positive. The two `P->T` references keep full-event memory and lose epoch memory. The unconditional pair favour has neither memory; its rate flag is the competition effect, and its un-normalised triad weight does not depend on the pairs.

Epoch-clock information at `rho3 = 1`, in bits, is a different pair of numbers from the full-event information in the Generation 3 report. For `form(0-1) | present(0-1-2) => strong_favour`, `I(T at the pair event ; Q_{i+1} | Q_i)` is about 0.01413 bits and `I(Q_i ; T at the next pair event | T at this pair event)` is about 0.00550 bits. For the bare triadic favour both epoch informations are 0. For `form(0-1-2) | present(0-1) => strong_favour` the triad-to-next-pair epoch information is 0 and the pair-to-next-triad epoch information is about 0.02869 bits: the pair event predicts the hidden triad, and the next pair event does not depend on it.

10. Across `rho3 ∈ {1/2, 1, 2}`, the pair-jump boolean, the triad-rate boolean, and the full-event zero/positive status do not change on any of the 7,385 sets. The epoch zero/positive status changes on 6 sets at `rho3 = 1/2` and on 6 other sets at `rho3 = 2`. Those 12 sets are cardinality 2, jump-positive, and full-event-positive. Their epoch total variation at `rho3 = 1` is `3/308` or `4/351`. The reference rules above do not change status at either alternate rate. This says the sign of a small epoch total variation can move when the triad is slowed or sped. It does not say the fraction itself is invariant, because the alternate rates were stored as statuses.

## E. What the split is

OBSERVED. Positive full-event memory without pair-jump dependence is 2,364 sets, and every one of them has zero pair-event-epoch memory. That block contains every pure `P->T` and pure `T->T` set that has full-event memory, plus 1,976 mixed sets. Positive epoch memory is 2,886 sets, and every one of them has pair-jump dependence and positive full-event memory. Inside that block, 370 are pure `T->P` and 2,516 are mixed.

INFERRED. For this grammar, the full-event clock is sensitive to hidden event timing. A triad event that does not change the pairs is a self-loop on the visible process, so a hidden change in how often those events arrive can make `P(P_{t+1} | P_t, P_{t-1})` differ from `P(P_{t+1} | P_t)` even when the law of the next real pair toggle does not depend on the triad. Skipping those events removes that memory. The epoch clock is the one that asks whether the hidden triad changes the sequence of lower-order organisations. In this census that happens together with a kernel difference in the pair-jump law, and the pure `P->T` and pure `T->T` mechanisms do not produce it.

The coincidence is a count over these 7,385 sets. It is not a proof that every kernel with a charged jump-law difference has epoch memory, and it is not a proof that epoch memory can occur without a jump-law difference outside this grammar.

## F. Scope

Not recomputed here: alphabet sensitivity, `K > 2`, cardinality 3, any `N` other than 3, simplicial face closure, geometry, explicit history. Generation 3b's 180 `K ≤ 3` singletons were not reanalysed. The Generation 3 report's trajectory detector remains what that report says it is. This reanalysis does not use it.

## G. Interpretation

The full relational process measured here is still first-order Markov. What changed is the description of the hidden variable's effect on the pairs. Some of Generation 3's coarse-grained memory is hidden timing: the triad changes how long a pairwise state persists, and the sequence of pairwise transitions does not remember the triad. Some of it is a hidden transition law: after a real pair event, the next pair event still depends on the triad that rode along. Those are different facts. Neither is a confirmation of a global-coherence doctrine. The narrower claim they support is the one Generation 4 then tests at `N = 4`: whether a higher-order bit can also change which pairwise graph appears, among graphs that have the same number of edges and are not isomorphic.
