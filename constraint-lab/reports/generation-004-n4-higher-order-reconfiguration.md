# Generation 004 — N=4 higher-order reconfiguration

Engine `0.4.0` on this cell. Semantic version `0.4.0`. Grammar `independent-hypergraph-v1`. Normalisation `structural-unique-v1`.
The N=3 reanalysis in this same round stays on engine `0.3.0`. Pairwise Generation 1b shards stay on engine `0.2.0`.
Specification hash `d64a9cccc12ec4a58a886227a52ba3b2b35a9506978a521b3766835de8f4a7f9`.
Python 3.12.3, NumPy 2.5.3, platform `linux`.
Summary SHA-256 `6f941c19ae73ae0caf1157d6e4bdf7ccec2e775f9598e00db8e98765b110ea2a`.
Row table SHA-256 `12ff748721ca076ba922c0c1330ed75ce291157771dcfc7b340378cc81bb4c49` (`reports/tables/generation-004-n4-higher-order-reconfiguration-singles-n4-k2.csv`, 161 lines including the header, 56,979 bytes).
Plan git commit `90ad68fc0e55333335412dfa3af5c7081b60c918`. The summary field `git_commit` is that commit. The plan was written before the analysis commit that contains this report. The plan header is left at the commit that existed when the shards were pinned.

Stationary distributions in this census are float64. A residual is the maximum imbalance of the solved linear system. The largest primary residual is `2.5573076642415593e-15`. Every residual is below `1e-8`. These distributions are numerical. The baseline uniformity argument in section F is a separate, exact symmetry claim.

## A. Why N=4

At `N = 3` every pairwise graph is identified by its edge count. Two graphs on three vertices with the same number of edges are isomorphic. `N = 4` is the first order at which two simple graphs can share an edge count and fail to be isomorphic. The two-edge path and the two-edge matching are the smallest such pair.

The question this cell can actually ask is whether an independent triadic configuration changes the probability of a passage between those two graphs, on a chain that is still a function of the current relational state alone.

```text
N=4  O=3  G=0  S=0  H=0  L=0
K<=2  cardinality 1  structural-simple  W4
independent hypergraph
```

`T` is the full triadic configuration, an element of `{0,1}^4`, not one hidden bit and not the popcount. `P` is the pairwise graph, an element of `{0,1}^6`. The full state is `(P, T)`.

## B. Provenance corrections

Prompt 003's stored execution-time file remains `constraint-lab/provenance/prompts/003-v0.3-higher-order-relations.md` (25,995 bytes, sha256 `9ac0de2c5d4cdd33749fec03a232f2d35fe5f6dbead9b0f572cafce4e23cbccb`). The agent-input file is one leading newline longer. The ChatGPT-authored Markdown reported at 27,580 bytes is not in this working environment. Its status stays `pending_verbatim_import`. The file was not reconstructed.

Prompt 004 is `constraint-lab/provenance/prompts/004-v0.4-n4-higher-order-reconfiguration.md` (32,011 bytes, sha256 `f261527e522cc780f0937097b7de7706f7953f8bf69c59837442bbb7e1cf76ef`). One byte string was available. It is the agent input. `relationship` is `unknown` because no separate authored file was found to compare. Semantic similarity was not recorded as byte identity.

Review 003 is `constraint-lab/provenance/reviews/003-chatgpt-review-v0.3.md`. It reviews `e04e0d4dcf979197b62d8d73fd747a0a2084c2b6`. It is not a line-by-line audit and it is not a review of this generation. Review 004 is pending and is not written here.

## C. Memory-taxonomy refinement from Generation 3

Generation 3's report is unchanged. The reanalysis is `generation-003c-memory-clock-refinement`, engine `0.3.0`, specification hash `b3940305e0c8ed69e9a80faa39d98964893f52563a2f13645c8f338ee22e4020`. It recomputed the 7,385 canonical sets from the same grammar. It did not overwrite Generation 3 or Generation 3b.

`FULL_EVENT_CLOCK_MEMORY` is the Generation 3 statistic. The observer sees the pairwise state after every full-system event. A triad-only toggle is a visible self-loop. On the six reference kernels this total variation equals `emergent_memory_tv`. The census count is 5,250 of 7,385.

`PAIR_EVENT_EPOCH_MEMORY` observes the pairwise state only when a pairwise relation toggles. `Q_i` is the pairwise state after that toggle. The total variation compares `P(Q_{i+1} | Q_i)` with `P(Q_{i+1} | Q_i, Q_{i-1})`. Epoch information uses that clock. It is not a rename of `I(T_t ; P_{t+1} | P_t)`.

The old word `FULLY_REDUCIBLE` is retained as `historical_reducibility` and is not the taxonomy. The axes are pair-jump dependence, triad-rate dependence, the two clocks, and membership of the conditional pair-jump kernels in the searched Generation 1b grammar.

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

Epoch memory is 2,886. All 2,886 also have full-event memory and pair-jump dependence. Of the 5,250 full-event-positive sets, 2,364 have epoch memory zero. Undefined epoch rows: 0. Defects: 0.

| Class | Sets | Full-event positive | Epoch positive |
| --- | ---: | ---: | ---: |
| `P->P` | 1,890 | 0 | 0 |
| `P->T` | 380 | 368 | 0 |
| `T->P` | 380 | 370 | 370 |
| `T->T` | 35 | 20 | 0 |
| mixed | 4,700 | 4,492 | 2,516 |

Pure `T->P` keeps epoch memory on 370 of 380. The other 10 put the same weight on both triadic literals, so the jump total variation is zero. Pure `P->T` and pure `T->T` keep epoch memory on 0 sets. No set has jump dependence absent and epoch memory present. 64 sets have jump dependence and both clocks zero; on each of them the two jump laws are not both charged by the stationary distribution reached from state 0.

The reference split at `rho3 = 1` is exact. `form(0-1-2) => strong_favour` has full-event memory `81/1288` and epoch memory 0. `form(0-1) | present(0-1-2) => strong_favour` has jump total variation `1/3`, full-event memory `27/616`, and epoch memory `34/1485`. The two `P->T` references have epoch memory 0. Across `rho3 ∈ {1/2, 1, 2}` the jump, rate, and full-event status are unchanged on all 7,385 sets. Epoch status moves on 6 sets at `rho3 = 1/2` and on 6 other sets at `rho3 = 2`. The reference rules do not move.

Axis E is `inside` for all 7,385 sets. The rate flag and the un-normalised weight flag disagree on 4,339 sets. The full table is in `reports/generation-003c-memory-clock-refinement.md`.

## D. N=4 state and symmetry structure

Slots, pairs first:

```text
(0,1) (0,2) (0,3) (1,2) (1,3) (2,3)
(0,1,2) (0,1,3) (0,2,3) (1,2,3)
```

Ten binary slots. `2^10 = 1,024` labelled states. `S4` has 24 permutations. The four triads move under `S4`. The triple that contained every entity at `N = 3` was fixed; that accident does not hold here.

The independent-hypergraph action has 90 orbits on the 1,024 states. The count is exact: every labelled state was visited through the 24 images. The 64 pairwise graphs fall into 11 isomorphism classes. Edge count is one descriptor of a class. The class is the canonical mask under `S4`.

| Class | Edges | Degrees | Triangles | Components | Automorphisms | Orbit |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| `e0-deg0000-tri0-comp4` | 0 | 0,0,0,0 | 0 | 4 | 24 | 1 |
| `e1-deg1100-tri0-comp3` | 1 | 1,1,0,0 | 0 | 3 | 4 | 6 |
| `e2-deg2110-tri0-comp2` | 2 | 2,1,1,0 | 0 | 2 | 2 | 12 |
| `e2-deg1111-tri0-comp2` | 2 | 1,1,1,1 | 0 | 2 | 8 | 3 |
| `e3-deg3111-tri0-comp1` | 3 | 3,1,1,1 | 0 | 1 | 6 | 4 |
| `e3-deg2220-tri1-comp2` | 3 | 2,2,2,0 | 1 | 2 | 6 | 4 |
| `e3-deg2211-tri0-comp1` | 3 | 2,2,1,1 | 0 | 1 | 2 | 12 |
| `e4-deg3221-tri1-comp1` | 4 | 3,2,2,1 | 1 | 1 | 2 | 12 |
| `e4-deg2222-tri0-comp1` | 4 | 2,2,2,2 | 0 | 1 | 8 | 3 |
| `e5-deg3322-tri2-comp1` | 5 | 3,3,2,2 | 2 | 1 | 4 | 6 |
| `e6-deg3333-tri4-comp1` | 6 | 3,3,3,3 | 4 | 1 | 24 | 1 |

Same edge count, more than one class:

- 2 edges: the path `e2-deg2110-tri0-comp2` (canonical mask 3) and the matching `e2-deg1111-tri0-comp2` (canonical mask 12).
- 3 edges: the star, the triangle plus an isolated vertex, and the three-edge path.
- 4 edges: two classes, the complements of the two two-edge classes.

No scalar combines these descriptors. The predeclared focused passage is the two-edge pair only. The three-edge and four-edge distinctions were classified and were not given their own first-passage runs.

A state with triad `ABC` present and no edges is a legal state. From it the chain can toggle that triad off, or toggle a pair on. Face closure was not applied. `docs/simplicial-design.md` is unchanged.

## E. Grammar planning and exact coverage

The external review said the `K ≤ 2` singleton scope should stay small after symmetry reduction. It did not publish an integer. The exact counts:

| Object | Count |
| --- | ---: |
| Structural normal forms | 380 |
| Labelled constraints, five weights | 1,900 |
| `S4` canonical weighted singletons | 160 |
| Structural orbits at one weight | 32 |

Structural forms by class: `P->P` 132, `P->T` 96, `T->P` 96, `T->T` 56, mixed 0. A single constraint has one class, so mixed is empty at cardinality 1.

By `K`, still unweighted forms:

| `K` | `P->P` | `P->T` | `T->P` | `T->T` |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 12 | 0 | 0 | 8 |
| 2 | 120 | 96 | 96 | 48 |

`K = 1` has no `T->P` and no `P->T` form. A triadic condition on a pairwise action has `K = 2`. The Generation 3 report had named a `K ≤ 1` probe as the next cell. Review 003 rejected that bound for this reason. This census follows Review 003. The 20 canonical `K = 1` rows are the subset of the same run.

Orbits at one weight: `P->P` 10, `P->T` 8, `T->P` 8, `T->T` 6, and by `K` the split is 4 plus 28. The four `K = 1` orbits are form an edge, dissolve an edge, form a triad, and dissolve a triad. Five weights give `32 × 5 = 160` canonical weighted singletons.

The plan's symmetry estimate was `1900/24 = 79.17`. The exact canonical count is 160. The estimate divides by `|S4|` as if every orbit had 24 distinct images. Constraints with a nontrivial stabiliser have smaller orbits, so the number of orbits is larger. The gap is that stabiliser, not a second grammar.

Cardinality 2, counted and not executed: 1,804,050 labelled combinations, 1,800,250 labelled structurally-simple pairs, 85,175 canonical structurally-simple pairs. `cardinality_2_executed` is false.

The plan used shard size 100 because an N=4 assessment is a 1,024-state kernel, not because 100 matches the older pairwise item window. Nineteen shards. Workers 2. Disk upper bound recorded in the plan: 760,000 bytes. The published row table is 56,979 bytes.

## F. Baseline validation

The unconstrained chain at `rho2 = rho3 = 1` was certified before the census maxima were read, and the certificate was recomputed while this report was written.

Every state has ten successors, each of probability `1/10`, and every transition has its reverse. The chain is the 10-bit hypercube under single-bit flips. That graph is connected and bipartite by Hamming parity, so the unconstrained chain is one recurrent class of period 2, and the uniform measure `1/1024` is its unique stationary distribution. This uniformity is the symmetry. The float64 solve is a check beside it: arithmetic `float64`, residual `2.7462841029057827e-16`, total variation from uniform `1.9881557337952938e-15`.

Each of the six pair bits and each of the four triad bits has numerical mean `0.5`. Expected pair density `0.4999999999999996`. Expected triadic occupancy `1.9999999999999996`, against the exact occupancy 2 from four fair bits. The largest gap between a pair-triad joint mean and `1/4` is `6.38378239159465e-16`.

Pair-jump dependence is false, jump total variation `0/1`. Triad-rate dependence is false. Full-event-clock total variation `2.7755575615628914e-16`, status zero. Pair-event-epoch total variation `2.498001805406602e-16`, status zero, defect 0. Projection B total variation is on the same scale. `I(T_t ; P_{t+1} | P_t)` is `-1.5183428258071694e-15` bits. Eleven pairwise classes. 90 hypergraph orbits. The focused names are the path and the matching above.

The baseline hit-before-return at horizon 16, the comparator stored on every primary row, is `0.18311749702578972` from the path to the matching and `0.7324699881031586` from the matching to the path. Unresolved mass within the horizon remains about `0.0256` on rows whose kernel does not move this passage. The means in section L are truncated lower bounds for that reason.

## G. Singleton cross-order census

Status `COMPLETE`. Canonical coverage `{"1": 160}` against the plan count 160. Quarantined 0. Failed 0. Workers 2 on both invocations. Shard items 100. Nineteen receipts. Shard-work, the sum of receipt elapsed times, is 313.631 seconds. The longest receipt is 90.221 seconds (50 canonical sets). Four receipts exceed 30 seconds. Fourteen shards scan 100 labelled rows and analyse 0, because symmetry removes them; those receipts are about one second.

The coordinator field `runtime_seconds` is 217.686. The resume path adds the new elapsed time to the previous summary when shards are still unfinished. The first invocation finished shard `011ccc9fe91e` at `2026-10-03T17:46:16Z`. The second invocation's worker stamp is `2026-10-03T17:47:36Z`, and the last receipt is `2026-10-03T17:49:36Z`. The stored 217.686 seconds is the sum of the two coordinator walls.

| Class | Canonical | `K = 1` | `K = 2` |
| --- | ---: | ---: | ---: |
| `P->P` | 50 | 10 | 40 |
| `P->T` | 40 | 0 | 40 |
| `T->P` | 40 | 0 | 40 |
| `T->T` | 30 | 10 | 20 |

Every primary row uses arithmetic `float64`. Every stored period set is `{2}`: every recurrent component the solver found has period 2. The number of recurrent components was not stored on the row. Epoch defect is 0 on all 160 rows.

The eight `T->P` orbits, each times five weights:

```text
form(0-1) | present(0-1-2)
form(0-1) | absent(0-1-2)
form(0-1) | present(0-2-3)
form(0-1) | absent(0-2-3)
dissolve(0-1) | present(0-1-2)
dissolve(0-1) | absent(0-1-2)
dissolve(0-1) | present(0-2-3)
dissolve(0-1) | absent(0-2-3)
```

`0-1-2` contains the acted edge. `0-2-3` meets that edge in one vertex. Present and absent are opposite literals. These eight are the structural catalogue. The forty weighted rows are their `W4` grades.

## H. Pair-jump dependence on hidden triads

Axis A asks whether the triadic configuration changes the law of the next pair toggle, at states where a pair toggle has positive weight. It is a property of the kernel. It is not restricted to the stationary support.

| Class | Pair jump | Sets |
| --- | --- | ---: |
| `P->P` | no | 50 |
| `P->T` | no | 40 |
| `T->P` | yes | 40 |
| `T->T` | no | 30 |

The 40 yes-rows are exactly the `T->P` singletons. At each fixed weight the eight orbits store one common jump total variation. The float is bit-identical across those eight rows:

| Weight | Jump total variation |
| --- | ---: |
| `strong_favour` | 0.2777777777777778 |
| `prohibit` | 0.16666666666666669 |
| `strong_suppress` | 0.11904761904761904 |
| `weak_favour` | 0.11904761904761904 |
| `weak_suppress` | 0.07575757575757579 |

These are float64 values. `strong_suppress` and `weak_favour` landed on the same stored value. The census did not reduce them to rationals.

`K = 1` contributes none of the yes-rows. An unconditional action does not read a triad, so it cannot put two different pair-jump laws on two triadic slices.

Axis E compares each non-halt pair-slice kernel with the committed Generation 1b `N = 4`, `K ≤ 2` catalogue `catalogue/generation-001b-structurally-normalised-kernel-ids-n4-k2.txt`, sha256 `59ccc85b0293ff41f68cc64a1268e1bd2209f5dca03eecfc56e38b740a2581a0`. At `W4`, all 160 rows are `inside`. Differing jump laws can both sit inside that catalogue. `inside` is not a claim of dynamical independence, and it is not a claim about grammars outside the catalogue.

## I. Full-event-clock memory

Projection A hides all four triads. The observer's state is the pairwise graph, 64 values, read after every full-system event.

| Class | Full-event clock | Sets |
| --- | --- | ---: |
| `P->P` | zero | 50 |
| `P->T` | positive | 40 |
| `T->P` | positive | 40 |
| `T->T` | positive | 28 |
| `T->T` | zero | 2 |

Positive: 108 of 160. The two zeros are `form(0-1-2) => prohibit` and `dissolve(0-1-2) => prohibit`. The other eight `K = 1` triadic rows are positive, and every `K = 2` triadic row is positive. Every `P->P` row is zero. The largest stored full-event total variation is `0.02886671418389814`, on `dissolve(0-1) | absent(0-2-3) => strong_favour`.

The same written rule at `N = 3` is an exact fraction, and the `N = 4` value is a different state space. `form(0-1-2) => strong_favour` has full-event total variation `81/1288` at `N = 3` and `0.00817820407648577` here. `form(0-1) | present(0-1-2) => strong_favour` has `27/616` at `N = 3` and `0.028866714183895116` here, with epoch total variation `0.030900101788571624` beside the `N = 3` value `34/1485`. Hiding four triads does not multiply the `N = 3` total variation by a constant.

## J. Pair-event-epoch memory

| Class | Pair-event epoch | Sets |
| --- | --- | ---: |
| `P->P` | zero | 50 |
| `P->T` | zero | 40 |
| `T->P` | positive | 40 |
| `T->T` | zero | 30 |

Positive: 40 of 160, exactly the `T->P` rows. The largest stored epoch total variation is `0.03090010178857225`, on `form(0-1) | absent(0-1-2) => strong_favour`. At that weight the other seven orbits lie between `0.03090010178857094` and that value. The span is about `1.3e-15`. The jump total variation is bit-identical across the eight orbits. The epoch and full-event totals are not: they agree to well under the floor `1e-8` and differ in the last stored bits. The same pattern holds at the other four weights. The spans stay below `6e-15`.

`P->T` and `T->T` reproduce the Generation 3 pure-class split on this singleton grammar. They can show full-event memory, and the epoch total variation stays under the floor `1e-8`. The bare triadic favour is again a timing split: full-event total variation `0.00817820407648577`, epoch total variation on the numerical floor, pair jump false.

No row has pair-jump dependence and epoch memory zero. No row has epoch memory and pair-jump dependence absent. Both statements are counts over these 160 kernels.

## K. Information carried by hidden triadic configuration

`I(T_t ; P_{t+1} | P_t)` uses the full-event clock and the 16-valued triadic configuration. The largest stored value is `0.03683980611793161` bits, on `form(0-1) | absent(0-2-3) => prohibit`. The smallest stored values are about `-1e-15` and sit on kernels whose status is zero. Those negatives are numerical noise around zero.

The epoch quantity `I(T at the pair event ; Q_{i+1} | Q_i)` has largest stored value `0.026020337851306984` bits, on `form(0-1) | present(0-2-3) => prohibit`. The other epoch quantity, `I(Q_i ; T at the next pair event | T at this pair event)`, has largest stored value `0.04786763321174155` bits, on `form(0-1-2) | absent(0-3) => prohibit`, which is `P->T`. On that class the pair event predicts the hidden triad, and section J says the next pair event does not remember the previous pair event once triad-only steps are removed.

Projection B exposes the pairwise graph and the number of triads present: 64 graphs times counts `{0,1,2,3,4}`, so 320 observation labels. "Restores Markovity" means the pair-only full-event total variation is positive and the Projection B total variation is zero.

Restorations: 0 of 160. Wherever the pair-only clock is positive, Projection B is positive too. On the 40 `T->P` rows the two total variations agree to `1e-12`. On the 40 `P->T` rows and the 28 positive `T->T` rows, the Projection B total variation is larger. The largest Projection B value is `0.031622325043410816`, on `form(0-1-2) => strong_favour`, against a pair-only value of `0.00817820407648577` for that same rule. Adding the count changes the statistic. It does not remove the memory.

The triad-conditioned hit in section L is computed across the 16 configurations, not across the count. A positive spread there means two triadic configurations disagree. The count was not tested as a sufficient statistic for that spread.

## L. Non-isomorphic same-cardinality reconfiguration

The ranking scalar was fixed before any census maximum was inspected:

```text
max_abs_stationary_pair_event_class_flux_delta
```

It is the maximum of `|F_constrained(X, Y) - F_baseline(X, Y)|` over ordered pairs of isomorphism classes with the same edge count and different canonical masks. `F` is the stationary flux of one pair-event step. The class matrix is an observable of the 1,024-state epoch chain. States were not lumped because they share an orbit. Lumpability was not assumed.

A pair event toggles exactly one pair bit, so the edge count changes by exactly one. Two classes of equal edge count are not neighbours under one pair event. Their one-step flux is identically zero on the constrained kernel and on the baseline. The ranking scalar is identically zero on every kernel in this semantics, at every cardinality and every `K`.

The census confirms the consequence. `reconfig_effects` is 0. The stored argmax on all 160 rows is the path to the matching, with `delta_flux` 0. The same-edge-count category totals, isomorphic and non-isomorphic, are 0.0. The different-edge-count category total differs from the baseline by at most `8.271161533457416e-14`, the size of a conservation residual: both flux matrices sum to 1, so the three category totals cannot all move. Individual different-edge-count cells were not stored. They were not promoted into a replacement ranking after the scalar came out zero. The horizon was not changed. The measure was not changed.

The predeclared multi-step observable is separate. Horizon `h = 16` pair events, fixed in the specification. For the focused ordered pair, the quantity is the probability of hitting the target class before returning to the source class, starting from the stationary pair-event distribution conditioned on the source. The mean pair-event count given a hit is a truncated lower bound on every row: unresolved mass at horizon 16 stays above `1e-8`, so no row is reported as a finite mean first-passage time. `mean_status` is `truncated_lower_bound_within_horizon` on all 160 rows, in both directions.

Path to matching, `|delta| > 1e-8`:

| Class | Rows | Rows above the floor | Largest delta |
| --- | ---: | ---: | ---: |
| `P->P` | 50 | 50 | −0.03593449303098292 |
| `T->P` | 40 | 40 | −0.006258155390793857 |
| `P->T` | 40 | 0 | numerical floor |
| `T->T` | 30 | 0 | numerical floor |

Matching to path, same floor:

| Class | Rows above the floor | Largest delta |
| --- | ---: | ---: |
| `P->P` | 50 | −0.11970449038888031 |
| `T->P` | 40 | −0.025032621563174984 |
| `P->T` | 0 | numerical floor |
| `T->T` | 0 | numerical floor |

The largest path-to-matching change is `dissolve(0-1) | absent(2-3) => prohibit`, class `P->P`. Baseline hit `0.18311749702578972`, constrained hit `0.1471830039948068`, unresolved mass `0.04437356050199857`, truncated mean `4.014144444225485`. `triad_changes_hit` is false.

The largest matching-to-path change is `dissolve(0-1) => prohibit`, class `P->P`, `K = 1`. Baseline hit `0.7324699881031586`, constrained hit `0.6127654977142782`, unresolved mass `0.0873800593047553`, truncated mean `4.970856238685318`. `triad_changes_hit` is false.

The largest `T->P` path-to-matching change is `dissolve(0-1) | present(0-2-3) => prohibit`. Baseline hit `0.18311749702578972`, constrained hit `0.17685934163499586`, delta `−0.006258155390793857`, triad spread `0.008995800253034203`. The matching-to-path delta on that same row is `−0.025032621563174984`, triad spread `0.035983201012137256`.

Signs are not uniform. Path to matching: `P->P` has 29 decreases and 21 increases; `T->P` has 24 decreases and 16 increases. Matching to path: `P->P` has 31 decreases and 19 increases; `T->P` has 24 decreases and 16 increases.

`triad_changes_hit` is true on both directions for all 40 `T->P` rows, and false on both directions for the other 120. `triad_changes_one_step` is false on all 160 rows in both directions. The one-step probability of the other same-count class is zero from every triadic slice, so the one-step spread across triads is zero. The multi-step spread is where a triadic configuration changes this passage.

## M. Baseline-relative transition effects

Every delta in section L subtracts the unconstrained kernel at the same `rho3`. Reachability on the free hypercube is not the observation.

On the focused passage the pairwise singletons move the hit probability, and they move it by more than the `T->P` singletons. The largest `T->P` path-to-matching decrease is about one sixth of the largest `P->P` decrease (`0.00626` beside `0.03593`). The largest `T->P` matching-to-path decrease is about one fifth of the largest `P->P` decrease (`0.02503` beside `0.11970`). The `P->P` rows have `triad_changes_hit` false. A nonzero delta, by itself, is a pairwise fact on 50 of these kernels.

What the `T->P` rows add is the spread across the 16 triadic configurations. The hidden configuration changes the hit probability. The one-step class-to-class flux of equal edge count does not move.

`P->T` and `T->T` leave both focused deltas on the numerical floor. A constraint that writes on a triad and only reads a pair, or that only reweights triads, does not move this two-edge passage under the horizon and the floor used here.

## N. Weight and rate sensitivity

Primary rows use `W4` and `rho3 = 1`. The same shards recompute `rho3 ∈ {1/2, 2}` and the alphabets `W3` and `W16`. Probes recompute the two clocks, the jump boolean, the support, the modal toggle pattern, and the one-step flux delta. They do not recompute Projection B, the epoch informations, or the horizon-16 passage. Survival of the multi-step hit delta under `rho3` and under the alphabets was not measured.

`rho3` cannot move axis E. Pair-slice weights do not include the triadic baseline, so the rho probes copy the primary axis E value. Alphabet probes recompute axis E.

On all 160 rows, at both alternate rates and at both alphabets:

- the jump boolean is unchanged;
- both clock statuses are unchanged;
- the one-step reconfiguration effect stays false;
- the support of strictly positive toggle weights is unchanged;
- `primary_pair_still_argmax` stays true.

The argmax flag is true because every kernel, primary and probed, stores the same zero-delta pair as its argmax: the path to the matching. The flag does not say a nonzero structural transition survived.

The modal pattern is the per-state set of maximal-weight toggles. It changes on all 160 rows at `rho3 = 1/2` and at `rho3 = 2`. Changing the baseline weight of every triadic toggle changes which toggle is heaviest. It does not change the memory statuses. At `W3` and `W16` the modal pattern is unchanged on all 160 rows: for a fixed grade assignment the ordering of the positive weights does not depend on the base.

Axis E at `W3` is `outside` on 72 rows: every nonzero grade of every `P->P` and `T->P` orbit (`10 × 4` and `8 × 4`). Axis E at `W16` is `outside` on 36 rows: `strong_favour` and `strong_suppress` of those same orbits. `W16` weak grades use base 4, and `4^1 = 2^2`, `4^{-1} = 2^{-2}`, so those numerical kernels already occur in the `W4` catalogue under the strong grade names. `P->T` and `T->T` stay `inside` at both alphabets, because their pair-slice weights stay at the baseline. Prohibit stays `inside`, because prohibit is zero in every alphabet. `outside` here is an exact kernel-id mismatch against the `W4` catalogue. The support flag says the set of positive-weight toggles did not change.

## O. Negative findings

- The predeclared one-step same-edge-count flux delta is zero on all 160 constrained kernels, and the reason is the single-bit toggle. Cardinality 2 would not turn it on.
- `triad_changes_one_step` is false on all 160 rows.
- Projection B restores Markovity on 0 rows.
- No `P->P`, `P->T`, or `T->T` row has pair-event-epoch memory.
- No `K = 1` row has pair-jump dependence or epoch memory.
- No analysed kernel left the `W4` pair-slice catalogue.
- The horizon-16 means are truncated. Unresolved mass remains on the baseline passage.
- The three-edge and four-edge non-isomorphic families were not given first-passage statistics.
- Cardinality 2 was counted (85,175 canonical) and not executed.
- Simplicial face closure, geometry, explicit history, `S > 0`, and `L > 0` were not introduced.
- Alphabet and `rho3` probes did not include the horizon-16 hit, so that passage has no recorded sensitivity certificate.

## P. Inferences

OBSERVED. On these 160 kernels the two clocks separate by cross-order class. Full-event memory occurs for every `P->T` singleton, every `T->P` singleton, and 28 of 30 `T->T` singletons. Epoch memory occurs for every `T->P` singleton and for no other row. Pair-jump dependence occurs for every `T->P` singleton and for no other row. At each weight the eight `T->P` orbits store one bit-identical jump total variation. Their epoch and full-event totals agree to about `1e-15` and are not bit-identical.

OBSERVED. The one-step flux between non-isomorphic classes of equal edge count is zero. The horizon-16 hit probability between the two-edge path and the two-edge matching moves for every `P->P` singleton and every `T->P` singleton. The largest movements are `P->P`. The triadic configuration changes that hit probability on the `T->P` rows and not on the others. `P->T` and `T->T` move neither the epoch memory nor this passage.

INFERRED. Three kinds of information stay distinct in this grammar. Hidden timing is the full-event memory that disappears when triad-only events are skipped: the `P->T` rows, the positive `T->T` rows, and the Generation 3 block of 2,364. Hidden transition-law information is the pair-jump dependence that survives into the epoch clock: the `T->P` rows here, and 2,886 of the Generation 3 sets. Hidden topological-reconfiguration information, in the narrow sense of a same-edge-count non-isomorphic passage, shows up at horizon 16 as a triad-conditioned change in hit probability. On this singleton grammar that change is smaller than the change produced by a constraint that never reads a triad.

The coincidence of jump dependence with epoch memory is a count over these kernels and over the 7,385 Generation 3 kernels. It is not a theorem that every charged jump-law difference has epoch memory outside this grammar. The 64 Generation 3 rows with jump dependence and zero epoch memory already show that an uncharged difference in the kernel does not produce epoch memory.

The full relational kernel is a time-homogeneous function of `(P, T)`. The coarse-grained memory is a property of an observation of that chain. The period set `{2}` says the recurrent components the solver found are periodic. It does not add a history register. `H` stays 0.

## Q. RS / global-coherence interpretation

This cell does not establish a globally coherent architecture, and it does not assign a meaning to a triad.

What it supports is narrower. An independently existing higher-order relation can carry information about later pairwise events that the current pairwise graph does not carry. Some of that information is about how long a pairwise graph persists. Some of it is about which pair toggles next. Some of it, at `N = 4`, reaches a passage between two graphs that have the same number of edges and are not isomorphic, and that part is conditioned on the triadic configuration. A pairwise constraint, with no triadic literal, moves the same passage further. The higher-order literal is not the strongest singleton influence on this particular passage.

That is coherent with keeping higher-order relation as its own primitive, because the timing split and the jump split both survive the move from one hidden bit to four, with `H`, `S`, `G`, and `L` still 0. It tensions with treating the horizon-16 path/matching delta as evidence that a single triadic condition has become the selector of lower-order organisation. On the numbers in section L, the selector that moves the passage most is still a pairwise prohibit.

## R. Next smallest justified experiment

Do not run the 85,175 canonical cardinality-2 sets.

The one-step ranking will stay zero on any further independent-hypergraph census, because a pair event still changes one edge. It should stay in the record as a structurally blind detector. It should not be the success test of the next run, and it should not be replaced after the fact.

The smallest continuation that this census actually leaves open is a targeted cardinality-2 grid, still at `N = 4`, `O = 3`, `G = S = H = L = 0`, independent hypergraph, `K ≤ 2`. Take the 8 `T->P` orbits and the 10 `P->P` orbits, at the two weights `prohibit` and `strong_favour` only. That pool has `8 × 10 × 2 × 2 = 320` labelled pairs before symmetry. The exact canonical count of that pool was not computed here. The question to fix before running it: does the pair move the horizon-16 triad-conditioned path/matching hit, or the baseline-relative hit delta, beyond what the `T->P` member and the `P->P` member produce as singletons? Horizon 16 and the two class names stay as they are.

`H = 1` is not indicated. The non-Markov pair marginal is already present at `H = 0`. `S > 0` and `G > 0` are not indicated. The internal variable that changes the jump law is the triadic relation.

Simplicial face closure remains the fork that could make one relational event change more than one pair, and therefore the fork that could put two same-edge-count graphs a single event apart. That comparison is specified in `docs/simplicial-design.md`. It is not the next run. Starting it now would mix a new event model with the cardinality question this census left open. If the targeted grid does not move the triad-conditioned passage beyond its singleton parts, that design note becomes the following decision, and it should be taken as its own branch.

## Questions this generation was asked

1. Generation 3 full-event-clock memory: 5,250 of 7,385.
2. Generation 3 pair-event-epoch memory: 2,886. Undefined: 0.
3. Both: 2,886. Full-event positive and epoch zero: 2,364.
4. Epoch memory is the 370 pure `T->P` sets plus 2,516 mixed sets. Full-event memory without epoch memory is 368 pure `P->T`, 20 pure `T->T`, and 1,976 mixed sets. Pure `P->P` has neither (1,890).
5. `T->P` survives the epoch test on 370 of 380 Generation 3 sets, and on 40 of 40 `N = 4` singletons.
6. No pure `P->T` Generation 3 set has epoch memory (0 of 380). No `N = 4` `P->T` singleton has it (0 of 40).
7. Of the 5,250 Generation 3 full-event-positive sets, 2,364 lose the memory when triad-only events are skipped, and 2,886 keep epoch memory. Every set in the first block has jump dependence absent. Every set in the second has jump dependence present.
8. The `N = 4`, `O = 3`, `K ≤ 2` singleton grammar has 380 structural forms, 1,900 labelled constraints, and 160 canonical weighted singletons.
9. All 160 canonical weighted singletons were analysed, in 32 structural orbits.
10. Hidden-triad-dependent pair-jump laws: the 40 `T->P` singletons, eight orbits times five weights. No other class.
11. Pair-event-epoch memory: those same 40.
12. Hiding four triads reproduces the same class split as hiding one, on the singleton grammar. It does not scale the `N = 3` total variations by one factor. The bare triadic favour drops from `81/1288` to `0.00817820407648577`. `form(0-1) | present(0-1-2) => strong_favour` moves from `27/616` to `0.028866714183895116` on the full-event clock and from `34/1485` to `0.030900101788571624` on the epoch clock.
13. Exposing the triad count restores Markovity in 0 of 160 systems. On 68 systems the count-augmented total variation is larger than the pair-only total variation.
14. Same-edge-count non-isomorphic one-step flux does not move, for the structural reason in section L. The horizon-16 hit between the two-edge path and the two-edge matching does move, for every `P->P` and every `T->P` singleton.
15. Those horizon-16 movements are deltas against the unconstrained kernel. The baseline hits are `0.18311749702578972` and `0.7324699881031586`. The one-step structural delta is zero on the baseline as well.
16. A single `T->P` constraint does change the horizon-16 passage in a way that depends on the triadic configuration. The largest such path-to-matching delta has absolute value `0.006258155390793857`. A single `P->P` constraint changes the same passage by more, up to `0.03593449303098292`, without a triadic condition. The one-step detector does not see either effect.
17. Jump booleans and both clock statuses survive `rho3 ∈ {1/2, 2}` and the alphabets `W3` and `W16` on all 160 rows. Support survives. The modal toggle pattern moves at both alternate rates and survives both alphabets. Exact kernel identity against the `W4` catalogue does not survive the nonzero grades, as section N records. The horizon-16 hit was not inside the sensitivity probes.
18. The next experiment is the 320-label grid in section R. It is a recommendation. It was not started.
