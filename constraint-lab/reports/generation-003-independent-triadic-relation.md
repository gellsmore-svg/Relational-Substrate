# Generation 003 — an independent triadic relation

Engine `0.3.0` on this cell. Semantic version `0.3.0`. Normalisation `structural-unique-v1`. Grammar `independent-hypergraph-v1`.
Pairwise shards elsewhere still record engine `0.2.0`. That identity was not moved.
Specification hash `26bc5fcafd9dd868171659f20f132bb27965e63c0bf26659414d42fd228ada17`.
Python 3.12.3, NumPy 2.5.3, platform `linux`.
The completing resume recorded wall clock 162.102 seconds and shard-work 293.272 seconds. Workers 2. Shards 11. Quarantined 0.
An earlier invocation completed shard `9a6439ef6d1573d3b107d03d` and stopped. Its receipt SHA-256 stayed `2f20d5ec38faf042a6893a91a88b5a58ce797341ebc674be70596cb5b85b5f47` after resume. That opening invocation's own wall clock was 4.237 seconds and is not included in the 162.102 second field.
Summary SHA-256 `f90a84da22cdf9dc0d447ed08c75084b2023b9987033c92f3f2e0b14bb6bd9fe`.
Census commit at execution: `ca679de546a50ad75928101d43920b2cd50ba4e0`.

The bounded `K ≤ 3` singleton extension is a separate experiment, `generation-003b-k3-singletons`, specification hash `3107a2f57cf8c56f8ca56cc40da8e451dfd9bd97407874305e3a7cc7c3f5da99`. Wall clock 8.204 seconds. One shard. Summary SHA-256 `7a925a1eeb28bfca6bb1934a69409f8e51c5ea439035f95fd0db1bfcc96cc526`.

## A. Formal higher-order ontology

The entities are `0`, `1`, and `2`. The slots are the three pairs and one triple:

```text
bit 0    (0, 1)
bit 1    (0, 2)
bit 2    (1, 2)
bit 3    (0, 1, 2)
```

`ABC` present does not imply `AB`, `AC`, or `BC`. The three pairs present do not imply `ABC`. The semantics are independent hypergraph. They are not simplicial. Face-closure is scoped in `docs/simplicial-design.md` and was not executed.

Relation order `O` is the largest cardinality of an independently existing relation. Here `O = 3`.

Constraint arity `A` is the number of distinct entities named by the constraint. `form(0-1-2)` has `A = 3` and `K = 1`.

`G = 0`. There is no embedding.

`S` keeps its existing meaning: channels other than the binary incidence of a named relation. The triadic bit is relational incidence. It is not an entity-state channel and not a history register. `S = 0`, `H = 0`, `L = 0`.

The primary baseline gives every slot, including the triad, toggle weight 1. Formation and dissolution are symmetric. `rho3` is the baseline weight of the triadic toggle. The census uses `rho3 = 1`. The values `1/2` and `2` are recomputed inside the same shards. They are not a second experiment.

## B. State-space and orbit structure

OBSERVATION. There are 16 labelled states and 4 toggles from every non-halting state of the unconstrained walk. The walk has period 2. The stationary distribution is uniform, `1/16` on each state. The stationary triadic occupancy is `1/2`. The pair density is `1/2` both when the triad is absent and when it is present. Both formation and dissolution fluxes of the triad are `1/8`. The mean sojourn of the present triad is 4. Mutual information between the triad bit and the pairwise edge count is 0. `I(T; P'|P) = 0` and `I(P; T'|T) = 0`. The total variation between `P(P'|P)` and `P(P'|P, P_prev)` after hiding the triad is 0.

`S_3` fixes bit 3 and permutes bits 0, 1, and 2. The coarse classes are the pairwise edge count crossed with the triadic bit. There are 8 orbits, and they cover 16 states:

| Class | Size |
| --- | ---: |
| empty pairs, triad absent | 1 |
| empty pairs, triad present | 1 |
| one pair, triad absent | 3 |
| one pair, triad present | 3 |
| wedge, triad absent | 3 |
| wedge, triad present | 3 |
| triangle, triad absent | 1 |
| triangle, triad present | 1 |

Empty pairs plus the triad is not the same class as one pair and no triad. At `N = 3` the pairwise isomorphism type is the edge count. A relabelled wedge is the same class. Same-cardinality non-isomorphic reconfiguration is impossible in this cell.

## C. Grammar and coverage

The `K ≤ 2` grammar was counted exactly before the run. The symmetry estimate is not the coverage figure.

| Piece | Count |
| --- | ---: |
| Slots | 4 |
| Structural normal forms | 56 |
| of which `P->P` | 30 |
| of which `P->T` | 12 |
| of which `T->P` | 12 |
| of which `T->T` | 2 |
| of which mixed, as one constraint | 0 |
| Labelled constraints, five weights | 280 |
| Cardinality 1 labelled combinations | 280 |
| Cardinality 1 canonical structurally-simple sets | 80 |
| Cardinality 2 labelled combinations | 39,060 |
| Cardinality 2 labelled structurally-simple sets | 38,500 |
| Cardinality 2 labelled stacked-weight sets | 560 |
| Cardinality 2 canonical structurally-simple sets | 7,305 |
| Canonical structurally-simple sets analysed | 7,385 |
| Shards at 4,000 combinations | 11 |

The plan's upper disk bound was 15,512,000 bytes. The merged summary is 62,538 bytes. The family JSONL is about 12 MB and stays under `generated/`.

A mixed constraint, one rule that reads both a pair and the triad, has at least two conditions, so `K ≥ 3`. Mixed *sets* already occur at cardinality 2 when the two rules have different classes. Those sets are in the primary census. The single-rule mixed forms are not.

Coverage of the completed run matches the plan: 80 and 7,305 canonical simple sets. Stacked canonical sets at cardinality 2 were 160 and were not analysed under structural-simple composition.

## D. Baseline and sensitivity

OBSERVATION. The edge-only rule `form(0-1) => strong_favour` has identical conditional pairwise jump kernels on the two triadic slices. Both equal the Generation 1b kernel of the same expression. Its jump total variation is 0. Its coarse-grained memory total variation is 0. `I(T; P'|P) = 0`. `I(P; T'|T)` is about 0.011 bits, because the pair weights change the chance that the next event is the triad. That is rate competition. It is not a change of the pairwise jump law.

The same edge-only wedge rule used in earlier generations, `form(0-2) | present(0-1) & present(1-2) => strong_favour`, has conditional closing bias `1/9` on the hypergraph kernel, matching the pairwise kernel.

Under `rho3 = 1/2` and `rho3 = 2`, across all 7,385 primary sets:

| Change | `rho3 = 1/2` | `rho3 = 2` |
| --- | ---: | ---: |
| Exact kernel id | 7,384 | 7,384 |
| Modal family | 7,365 | 7,368 |
| Qualitative family | 7,365 | 7,368 |
| Support family | 0 | 0 |
| Reducibility class | 0 | 0 |
| Irreducible-coupling boolean | 0 | 0 |
| Emergent-memory boolean | 0 | 0 |

The one set whose exact kernel id did not change was not identified. Qualitative family counts under the two rates were 2,612 and 2,418, against 2,789 at `rho3 = 1`.

INFERENCE. The exact kernel and the modal family depend on treating the triad as having the same primitive rate as a pair. The support, the reducibility class, and the presence or absence of coarse-grained memory do not, inside this pair of rates.

## E. Cross-order constraint classes

A rule is classified by what it reads and what it toggles. `P->P` reads and toggles pairs. `P->T` reads a pair and toggles the triad. `T->P` reads the triad and toggles a pair. `T->T` reads and toggles the triad. A set whose members are not all the same class is `mixed`. The stored label uses ASCII `->`.

| Class | Canonical simple sets | Share of 7,385 |
| --- | ---: | ---: |
| `P->P` | 1,890 | 0.256 |
| `P->T` | 380 | 0.051 |
| `T->P` | 380 | 0.051 |
| `T->T` | 35 | 0.005 |
| mixed | 4,700 | 0.636 |

## F. New support, modal, and kernel territory

The comparison does not hash a 16-state kernel against an 8-state kernel.

For each analysed set the two conditional pairwise jump kernels are the 8-state kernels obtained by restricting to one triadic bit and renormalising the three pair weights. Those kernels are canonicalised with the same `S_3` action as Generation 1b.

Comparison domain, stated exactly: Generation 1b, `N = 3`, `K ≤ 3`, cardinalities `{1, 2, 3}`, structural-simple, pairwise-edge grammar, plus the unconstrained pairwise baseline. Count predicates, stacked weights, other `N`, and `K > 3` are outside that domain. Generation 2 is outside it.

OBSERVATION. Every conditional jump support id and every conditional jump qualitative id fell inside that index. The outside-index counts are 0 and 0. No searched set was `OUTSIDE_SEARCHED_PAIRWISE_GRAMMAR` or `UNRESOLVED`.

There were 0 genuine global cancellations and 0 inherited-baseline cancellations. There were 112 local cancellations. The primary cell produced 2,789 qualitative families of the 16-state process. Those families are not a count of new pairwise supports.

INFERENCE. Relative to the searched pairwise grammar, the new object is not a new pairwise transition support. The conditional pair supports were already in Generation 1b.

## G. Reducibility to pairwise dynamics

Reducibility is defined only inside the domain above.

- `FULLY_REDUCIBLE`: the two jump kernels are the same searched O=2 kernel, and the unnormalised triad weight does not depend on the pair configuration. The triad weight may still differ between the absent slice and the present slice.
- `PAIRWISE_PROJECTION_REDUCIBLE`: the two jump kernels are the same searched O=2 kernel, and the triad weight depends on the pairs.
- `IRREDUCIBLE_DYNAMIC_COUPLING`: the two jump kernels differ. The triadic bit changes the law of the next pair event.
- `OUTSIDE_SEARCHED_PAIRWISE_GRAMMAR`: the jump kernels agree, but that kernel is not in the index. This is not absolute irreducibility. The count here was 0.
- `UNRESOLVED`: the index was missing. It was present for this run.

| Class | Sets |
| --- | ---: |
| `FULLY_REDUCIBLE` | 2,295 |
| `PAIRWISE_PROJECTION_REDUCIBLE` | 2,150 |
| `IRREDUCIBLE_DYNAMIC_COUPLING` | 2,940 |
| `OUTSIDE_SEARCHED_PAIRWISE_GRAMMAR` | 0 |
| `UNRESOLVED` | 0 |

By cross-order class:

| | Fully | Projection | Irreducible |
| --- | ---: | ---: | ---: |
| `P->P` | 1,890 | 0 | 0 |
| `P->T` | 10 | 370 | 0 |
| `T->P` | 20 | 0 | 360 |
| `T->T` | 35 | 0 | 0 |
| mixed | 340 | 1,780 | 2,580 |

OBSERVATION. Every pure `P->P` set is fully reducible on the conditional jump kernels. No pure `P->T` or `T->T` set makes the two jump kernels differ. The sets that do are `T->P` (360 of 380) and mixed sets (2,580 of 4,700).

Reference rows, all inside the grammar:

| Expression | Class | Jump TV | Memory TV | `I(T;P'|P)` | `I(P;T'|T)` |
| --- | --- | ---: | ---: | ---: | ---: |
| `form(0-1) => strong_favour` | fully reducible, `P->P` | 0 | 0 | 0 | 0.011 |
| `form(0-1-2) => strong_favour` | fully reducible, `T->T` | 0 | 81/1288 | 0.068 | 0 |
| `form(0-1-2) \| present(0-1) => strong_favour` | projection, `P->T` | 0 | 351/9520 | 0.039 | 0.030 |
| `dissolve(0-1-2) \| present(0-1) => prohibit` | projection, `P->T` | 0 | 1/16 | 0.060 | 0.092 |
| `form(0-1) \| present(0-1-2) => strong_favour` | irreducible, `T->P` | 1/3 | 27/616 | 0.030 | 0.006 |
| `dissolve(0-1) \| present(0-1-2) => strong_favour` | irreducible, `T->P` | 1/3 | 27/616 | 0.030 | 0.006 |

`FULLY_REDUCIBLE` does not mean the triad is invisible once it is hidden. The bare triadic favour leaves the conditional pair kernel equal to the pairwise baseline and still makes the probability of a pair event depend on whether the triad is present. That is recorded as coarse-grained memory, not as a new pairwise jump kernel.

## H. Coarse-grained emergent memory

The test hides bit 3 and compares the stationary laws `P(P'|P)` and `P(P'|P, P_prev)` by total variation. A positive value is emergent memory under coarse-graining. The chain on the 16-state space remains first-order Markov. `H` is still 0.

OBSERVATION. 5,250 of 7,385 sets have positive total variation. The maximum is `2025/10738`, from `dissolve(0-1-2) => strong_favour` together with `form(0-1-2) => strong_suppress`. By class the positive counts are: `P->P` 0 of 1,890; `P->T` 368 of 380; `T->P` 370 of 380; `T->T` 20 of 35; mixed 4,492 of 4,700. Of the positive sets, 278 are still `FULLY_REDUCIBLE` on the jump kernels. Of the irreducible sets, 64 have total variation 0: the jump kernels differ, and the stationary pair marginal is still first-order Markov.

INFERENCE. Hiding the triad can make the pair process non-Markov. It does so for most sets that let the triad read or write a pair, and also for some sets whose only higher-order rule changes the triad's own rate. It does not do so for a pure pairwise rule. The effect is not automatic for every irreducible jump kernel.

## I. Information flow

Both quantities are conditional mutual informations of the stationary kernel, in bits. They are measures of predictive coupling. They are not read as purpose or integration.

OBSERVATION. The triad bit improves the prediction of the next pair state, beyond the current pair state, for 5,250 sets. The largest value seen in the reanalysis of those sets is about 0.215 bits. The pair state improves the prediction of the next triad bit, beyond the current triad bit, for 6,989 sets. The largest value seen is about 0.173 bits. Rate competition without a changed jump law accounts for part of the second direction: 4,421 sets have a state-dependent chance that the next event is the triad, and 2,041 of those are outside the irreducible class and still predict the next triad from the pairs.

On the baseline both informations are 0. On `form(0-1) => strong_favour` only the pair-to-triad direction is positive. On `form(0-1) | present(0-1-2) => strong_favour` both directions are positive, and the jump kernels differ.

## J. Trajectory families

The detector walks the positive-probability support. It records a triad toggle, then a later loss of a pair edge, then the pair-edge counts before the toggle and after the loss. At `N = 3` those counts are the isomorphism classes.

OBSERVATION. The unconstrained baseline already has such a path, including the formation-then-loss shape, and the later edge count differs from the earlier one. So do 7,384 of the 7,385 analysed sets. The one exception forbids both formation and dissolution of the triad, so the triad cannot toggle. `same_cardinality_nonisomorphic` is 0 on every set, which is the `N = 3` fact rather than a search result. `isomorphic_only` is 0 because whenever the loose detector fires, some later state also has a different edge count.

INFERENCE. The detector does not separate a constraint-caused reconfiguration from the free 4-cube. An edge-count change is not a new organisation here.

## K. Transformation-related observations

OBSERVATION. No searched grammar is reported as the sequence "pairwise organisation, then a higher-order relation, then a selective release, then a pairwise organisation that is not isomorphic to the first." The laboratory cannot see that sequence at `N = 3`, because two pairwise graphs with the same edge count are isomorphic.

The local cancellations and the triadic occupancy extremes are real stationary facts. Triadic occupancy reaches 0 and 1 on some sets, by prohibiting formation or by prohibiting dissolution together with a pair halt. Those are traps and hard restrictions. They are not the stronger transformation sequence.

## L. Negative results

- No conditional pairwise support, and no conditional pairwise qualitative family, fell outside the Generation 1b index.
- No genuine global cancellation appeared.
- Pure pairwise grammars contributed no irreducible jump coupling and no coarse-grained memory.
- The support trajectory detector fires on the baseline. It is not evidence that a constraint discovered a cross-order reconfiguration.
- Same-cardinality non-isomorphic pairwise change did not occur. It cannot occur at `N = 3`.
- Changing `rho3` from 1 to `1/2` or 2 does not change the reducibility class, the support id, or the emergent-memory boolean. It does change almost every exact kernel id.
- `K ≤ 3` pairs and triples were not run. `N = 4` was not run. Simplicial semantics were not run. Count predicates were not added to this grammar.

## M. Inferences

The independent triad is dynamically productive, and the productivity is specific.

The smallest irreducible contribution inside the searched grammar is a triadic condition on a pairwise action. That one literal makes the two conditional pair kernels differ. For the reference `form(0-1) | present(0-1-2) => strong_favour` the jump total variation is `1/3`, and hiding the triad leaves a pair process whose one-step law depends on the previous pair state, with total variation `27/616`.

A pair condition on the triad does not, by itself, change the conditional pair kernel. It does change the triad's rate, and the hidden bit can still make the marginal pair process non-Markov. That is a weaker coupling. It remains representable, on the jump kernels, by a searched O=2 grammar.

A pure pairwise rule does neither. The fourth toggle is still there, so the raw 16-state kernel is not the Generation 1b kernel. Conditioning on a pair event removes that trivial difference.

The new capacity is not a new pairwise support. It is a dependence between the pair law and a bit that a pair-only observer does not see.

## N. RS and global-coherence interpretation

This cell does not establish a globally coherent architecture, and it does not assign meaning to the triad.

What it does is narrower. An independently existing three-way relation can carry information about the next pairwise transition that the current pairwise state does not carry, and a pairwise observer who cannot see that relation can face a process that is not first-order Markov. The relation that does this is still one binary incidence. `S` and `H` stay 0. The apparent memory is produced by coarse-graining, not by writing a history variable into the kernel.

That is coherent with treating higher-order relation as its own primitive of relational possibility. It tensions with reading Generation 2's failure to find organisation, dissolution, and a genuinely different organisation as a reason to add history, geometry, and state channels together. The missing sequence is not available as a pairwise isomorphism distinction at `N = 3`. The coupling that did appear does not require those extra axes.

## O. Next smallest justified experiment

`K ≤ 3` singletons were run because a single mixed-read constraint is absent from the primary grammar and the cost is one shard. See below. They reproduced the same pattern: the 40 mixed singletons are all irreducible, and no jump support left the Generation 1b index.

`K ≤ 3` pairs were not run. The exact canonical count is 50,365, from 288,420 labelled combinations. The primary census already contains 4,700 mixed sets built from `K ≤ 2` rules. Another factor of about seven in the same language is tractable on this machine and is not the smallest remaining question.

Triples at `K ≤ 3` were not run. There are 72,874,120 labelled combinations. Resumability is not a reason to walk them.

The next experiment this evidence supports is a bounded probe at `N = 4`, `O = 3`, independent hypergraph, `K ≤ 1`, cardinalities `{1}` only. Pairwise graphs on four entities can share an edge count and fail to be isomorphic, so the reconfiguration question can be asked. The state space has `2^(6+4) = 1,024` points, so the stationary analysis leaves exact rationals. That probe is not a census, and it was not executed here.

`H = 1` is not the next primitive. The non-Markov pair marginal already appears at `H = 0` by hiding the triad.

`S > 0` is not indicated. The internal bit that carries the predictive information is the relation itself.

Simplicial face-closure is a real comparison and a different semantics. It is specified as questions in `docs/simplicial-design.md`. It is not the next run: the open behavioural gap is non-isomorphic pairwise change, and that gap is about `N`, not about face-closure.

## Generation 3B — why this extension, and why it stopped

OBSERVATION. At `K ≤ 3` the structural grammar has 152 forms: `P->P` 54, `P->T` 36, `T->P` 12, `T->T` 2, mixed 48. Labelled constraints: 760. Canonical singletons: 180, of which 20 have `K = 1`, 60 have `K = 2`, and 100 have `K = 3`. The run analysed 180. Families of the 16-state process: 108. Wall clock 8.204 seconds. One shard. Workers 2, so the second worker was idle.

All 40 mixed singletons are `IRREDUCIBLE_DYNAMIC_COUPLING`. All 20 `T->P` singletons are irreducible. All 50 `P->T` singletons are projection-reducible. All 60 `P->P` and all 10 `T->T` singletons are fully reducible. Emergent memory is positive for 118 of 180, including 70 of the 100 `K = 3` rules. Jump supports and jump qualitative families outside the Generation 1b index: 0. Reducibility class and the memory boolean are unchanged at `rho3 = 1/2` and `rho3 = 2`. Exact kernel ids all change. Genuine global cancellations: 0. `same_cardinality_nonisomorphic`: 0.

INFERENCE. Allowing one constraint to read both orders does not create a new kind of result. It puts the irreducible pattern into a single rule. The pairwise supports remain inside the grammar already searched at `O = 2`.

## Questions this generation was asked

How many exact O=3 states and symmetry classes are there? 16 labelled states, 8 orbits.

How large is the bounded higher-order grammar? At `K ≤ 2`, 56 structural forms and 280 labelled constraints. At `K ≤ 3`, 152 structural forms and 760 labelled constraints.

How many canonical simple sets were searched? 7,385 in the primary cell (80 + 7,305). The extension searched 180 singletons at `K ≤ 3`, which include the lower-`K` singletons again.

What proportion is `P->P`, `P->T`, `T->P`, `T->T`, or mixed? Of the 7,385: 1,890, 380, 380, 35, and 4,700.

Which grammars reduce to pairwise behaviour? All 1,890 pure `P->P` sets, on the conditional jump kernels. Most `P->T` and all `T->T` sets do too, in the fully reducible or projection-reducible sense defined above. Some of those still have coarse-grained memory.

Which are irreducible inside the searched comparison? 2,940 primary sets, concentrated in `T->P` and mixed sets. All 40 mixed `K = 3` singletons. None of this is a claim beyond the Generation 1b pairwise index.

Does hiding the triad make the pair process non-Markov? For 5,250 of 7,385 primary sets, yes, as a positive total variation. For the baseline and for pure `P->P` sets, no.

Does the triad carry predictive information about the next pair transition? For 5,250 sets, `I(T; P'|P) > 0`. The baseline value is 0.

Does the pair state carry predictive information about the next triad transition? For 6,989 sets, `I(P; T'|T) > 0`. Part of that is rate competition with an unchanged jump law.

Do any new transition supports appear that the Generation 1b comparison cannot represent? Not in the conditional pairwise jump kernels. The outside-index count is 0. Generation 2's count predicates were not the comparison domain.

Do any neutral trajectory classes resemble cross-order reconfiguration? The schematic path occurs, including on the unconstrained baseline. It is not distinctive.

Does anything satisfy the stronger self-transformation criterion? No. At `N = 3` that criterion would require a non-isomorphic pairwise change, which the state space cannot express.

Which findings survive the triad baseline rate? Support, reducibility class, and the emergent-memory boolean survive `rho3 ∈ {1/2, 1, 2}`. Exact kernel ids and modal families do not.

What is the smallest justified next increase? A singleton probe at `N = 4`, `O = 3`, independent hypergraph, `K ≤ 1`. Not `H = 1`, not `S > 0`, and not a simplicial execution.
