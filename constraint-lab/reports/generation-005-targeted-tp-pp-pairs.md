# Generation 005 — targeted T->P plus P->P pairs

Engine `0.4.0` on this cell. Semantic version `0.4.0`. Analysis version `0.5.0`. Grammar `independent-hypergraph-v1`. Normalisation `structural-unique-v1`.
Specification hash `c0372859f77626cec7af10c22cd35d0518ff3772ad907f7d6b08350fa17708af`.
Catalogue SHA-256 `d2994cead5190422a27ac1a135494fc6a2dd469dc914cb88ee0fed8192e10c57`.
Python 3.12.3, NumPy 2.5.3, platform `linux`.
Summary SHA-256 `5651a656c3404d833c296322216255b8de71ef56a3f046f2f1dfbf8a4220f154`.
Row table SHA-256 `d479775aafacb9bb6b6c5aea7522443f05ab4d581b92864a4cc1a7ff70e12c0e` (`reports/tables/generation-005-targeted-tp-pp-pairs-singles-n4-k2.csv`, 2,305 lines including the header, 1,784,842 bytes).
Plan git commit `1c7726f8d431ea54baeb478bf2171d0703046ea2`. The summary field `git_commit` is that commit. The plan was written before this report.

Stationary distributions, epoch kernels, and committors are float64. The largest residual recorded on a census row is `3.1730260779960773e-15`. These solutions are numerical.

```text
N=4  O=3  G=0  S=0  H=0  L=0
independent hypergraph
one T->P rule and one P->P rule
weights: prohibit, strong_favour
```

## A. Why this targeted pair grammar

Generation 4 showed that a hidden triadic configuration can condition a multi-step passage between the two-edge path and the two-edge matching, and that an ordinary pairwise singleton moves the same passage further. Generation 4a separated source occupancy from future dynamics and replaced the finite horizon with an eventual committor. The singleton conclusions survived. The open question is composition.

The question is whether one higher-order-conditioned pairwise rule and one ordinary pairwise rule, acting together, change that passage beyond the sum of the two singleton effects, and whether the pair increases the dependence on the hidden triadic configuration.

The full cardinality-2 grammar has 85,175 canonical structurally-simple pairs. It was not executed. The label grid `8 × 10 × 2 × 2 = 320` is a grid of singleton orbit names and weight choices. It does not encode the relative alignment of the two rules. It is not the canonical count.

## B. Exact pair enumeration and symmetry

Labelled structural rules were enumerated from the eight `T->P` singleton orbits and the ten `P->P` singleton orbits already present in Generation 4. Each structural rule then received `prohibit` or `strong_favour`. Every set of one weighted `T->P` rule and one weighted `P->P` rule was formed, and the complete set was canonicalised under `S4`. Rules were not canonicalised separately and then multiplied.

| Quantity | Count |
| --- | ---: |
| Labelled `T->P` structural rules | 96 |
| Labelled `T->P` weighted rules | 192 |
| Labelled `P->P` structural rules | 132 |
| Labelled `P->P` weighted rules | 264 |
| Weighted labelled pairs | 50,688 |
| Invalid structurally-simple pairs | 0 |
| Canonical structural pairs before weights | 576 |
| Canonical weighted pairs | 2,304 |
| Orbits of size 12 | 384 |
| Orbits of size 24 | 1,920 |

`384 × 12 + 1,920 × 24 = 50,688`. The mean orbit size is 22, not 24. Weighted canonical pairs are four times the structural canonical pairs, one factor for each independent weight pair. The label grid of 320 is recorded in the coverage block with `weight_grid_is_the_canonical_count` false.

The pool is below the predeclared ceiling of 20,000, so the census is exhaustive for this grammar. It is not a sample, and it is not the 85,175.

## C. Relative-alignment classes

Each canonical set stores a categorical signature: the `P->P` action edge against the `T->P` action edge (`same`, `adjacent`, `disjoint`); the `T->P` condition triad against its action edge (`contains_acted_edge`, `intersects_one_vertex`); and the `P->P` vertices against the `T->P` condition triad (`contained`, `partial_overlap`). No scalar alignment score is used.

There are 1,280 distinct signatures across the 2,304 canonical systems. The 320 groups that share a `T->P` orbit, a `P->P` orbit, and a weight pair all split. Every such group has more than one signature, and the largest split is 5. Two systems with the same singleton orbit labels can be inequivalent as a combined set.

Across the census the action-edge relation is `adjacent` on 1,408 systems, `same` on 448, and `disjoint` on 448. The condition-versus-action split is even, 1,152 and 1,152. The vertex-versus-triad split is `partial_overlap` on 1,792 and `contained` on 512.

At the effect floor, the path-to-matching interaction residual takes 304 distinct values, and the matching-to-path residual takes 304. Relative alignment distinguishes more systems than this one observable does.

## D. Block epoch solver validation

The pair-event landing used here is the block solver. Between pair events the pairwise state is fixed and only the 16 triadic configurations move. The solver keeps the semantics of the dense epoch kernel: the same conditioning on the next pair event, and the same treatment of a missing future pair event.

Before this census, the block landing was compared with the dense landing on the N=3 baseline, an N=3 `T->P` reference, the N=4 baseline, an N=4 `T->P` `strong_favour` reference, an N=4 `P->T` reference, and an N=4 prohibit rule. The largest absolute landing gap on those kernels was `5.55e-17`. Row sums, defects, pair-event memory, the horizon-16 passage, and the eventual committor were part of that comparison. The dense implementation remains in the tree. Generation 4's historical `assess_n4` path was not switched onto the block solver.

The plan-time sample on this machine timed one cold kernel at `0.06974976797937416` seconds and the following committor work at `0.03279972600284964` seconds. The first eight sorted canonical pairs took `2.362076071993215` seconds, `0.2952595089991519` seconds per pair, with later pairs reusing singleton committors. The plan estimated `340.13895436702296` seconds at two workers. A landing matrix is `8.388608` megabytes. The plan's per-worker memory figure multiplies that size by the shard length and overstates what a worker retains: each pair landing is released after the row is stored. Shard length 384 was taken from that sample. Workers stayed at 2.

## E. Eventual committor definition

The primary observable is the eventual hit-before-return committor on the pair-event epoch kernel, in both directions, between

```text
e2-deg2110-tri0-comp2    two-edge path
e2-deg1111-tri0-comp2    two-edge matching
```

For a start in the source class, it is the probability of reaching the target class before returning to the source class, after at least one pair event. The transient block is solved by `numpy.linalg.solve`. Float64 values are not called exact.

Horizon 16 is stored for every pair as `horizon16_controlled_delta`, against the matched baseline. It is a comparator. The horizon was not changed after the census.

The effect floor is `1e-8`, declared in the specification before either the Generation 4a census or this one. The reason is the reference-kernel residuals named in Generation 4a: landing gap `5.55e-17`, stationary residual `8.40e-16`, committor residual `1.78e-15`, statewise committor gap `4.44e-16`, condition numbers between 10 and 14. The largest residual observed in this census is `3.1730260779960773e-15`. A value inside the floor is classified zero. The interaction residual subtracts four committors, and the floor sits about four orders of magnitude above a pessimistic thousand-fold amplification of the measured committor residual.

## F. Controlled versus stationary source

`mu_ref` is the unconstrained baseline pair-event stationary distribution conditioned on the source class. The same array is used for the baseline, the `T->P` singleton, the `P->P` singleton, and the pair. The controlled baseline committor is identical on all 2,304 rows: path to matching `0.18823529411764703`, matching to path `0.752941176470588`.

`Q_stationary` uses each kernel's own source distribution. The occupancy contribution on a pair is `Q_stationary(TP) - Q_controlled(TP)`. It is a descriptive difference. It is not a unique causal split.

No system has a stationary interaction residual outside the floor and a controlled interaction residual inside it. Controlling the source does not erase the interaction. It does change it. The sign of the stationary residual and the sign of the controlled residual disagree on 256 rows for path to matching and on 568 rows for matching to path. Among rows with absolute controlled residual above `1e-4`, the median of `|I_stationary - I| / |I|` is `0.6749201768336786` on path to matching and `1.4577340129134928` on matching to path. A ranking that used only the stationary source would move magnitudes, and on those rows it would move signs.

## G. Singleton reference effects

On the controlled eventual committor the component effects in this pool are the Generation 4a singletons at `prohibit` and `strong_favour`. The largest controlled eventual singleton movements in the full Generation 4a table, which includes the other grades, are `0.03065683868166208` (`P->P`, path to matching) and `0.041220483357880866` (`P->P`, matching to path). The largest `T->P` movements there are `0.0011971123165731568` and `0.004788449266292405`.

Inside this pair census the median absolute component effects are smaller than the median pair effect. Path to matching: median `|Delta_T|` `0.00041847769980563054`, median `|Delta_P|` `0.0063462469496579355`, median `|Delta_TP|` `0.007931857526577796`. Matching to path: `0.0016739107992224667`, `0.009505027290441115`, and `0.010033478384281813`.

The extreme family below uses a `P->P` prohibit whose own controlled eventual deltas are `-0.0005832177989039955` and `-0.002332871195615871`, and a `T->P` prohibit whose own deltas are about `-0.000148` and `-0.000592`. Both components are above the floor. Both are far smaller than the pair.

## H. Two-rule controlled committor census

Analysis `n4-targeted-pairs`. Six shards, 384 items each. Workers 2. Failed 0. Quarantined 0. Status COMPLETE. Wall `305.6155730149767` seconds. Shard work `554.452213` seconds. All 2,304 canonical systems were analysed. Resume state at the end is complete: every shard receipt is present, and a second invocation is not required.

Support violations are 0. No pair introduces a positive one-step relational toggle that is absent from the baseline and from each component. Support removals are a different count: 1,728 systems delete at least one baseline toggle, median 256 deleted toggles, maximum 768. A prohibit weight is a deletion. The total of those counts is 614,400. That is not a new support.

| Direction | Nonzero I | Positive I | Negative I | G > 0 | Delta_S > 0 | Sign reversal of the stronger singleton | Pair dominates both components by 10× |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| path to matching | 2,304 | 1,164 | 1,140 | 1,232 | 1,948 | 344 | 76 |
| matching to path | 2,304 | 1,124 | 1,180 | 1,264 | 1,576 | 312 | 12 |

Zero within the floor: 0 and 0. The coded cancellation class, a nonzero residual with a pair delta inside the floor, is 0 and 0. The class in which both singleton deltas are inside the floor and the pair is not is also 0 and 0. Twelve systems have `G` inside the floor in each direction. `G` is negative on 1,060 and 1,028 systems.

Median absolute interaction residual: path to matching `0.003966107013885001`, matching to path `0.004368503087999187`. The 10th percentiles are `0.00048166050961367946` and `0.0005432165551277901`. The 90th percentiles are `0.012163160196803996` and `0.014311276017299202`. The smallest absolute residuals are `2.62123887301291e-06` and `5.878327874464517e-07`, still above the floor. Systems with absolute residual above `0.01`: 352 and 432. Systems above `0.001`: 1,816 and 1,996.

The median of `|I| / max(|Delta_T|, |Delta_P|)` is `0.526792088663445` on path to matching and `0.4850427079922347` on matching to path. On a typical row the interaction residual is about half the stronger singleton component, not a rounding correction to it.

Of the 352 path-to-matching rows with absolute residual above `0.01`, 264 have disjoint action edges. Disjoint edges are 448 of 2,304 systems in the whole census. The same threshold on matching to path has 220 disjoint, 156 same-edge, and 56 adjacent.

## I. Interaction residual

```text
I = Q_TP - Q_T - Q_P + Q_0
  = Delta_TP - Delta_T - Delta_P
```

`I = 0` would mean the combined committor effect is additive on this observable. `I > 0` is a positive interaction residual. `I < 0` is a negative one. The word for the quantity is interaction residual.

No row is additive at the floor. Positive and negative residuals are nearly balanced: 1,164 against 1,140, and 1,124 against 1,180.

The largest positive path-to-matching residual is `0.06637327774634985`. The largest negative matching-to-path residual is `-0.08059720804185777`. Four canonical systems share both values to within `1e-8`. They are the same motif under four condition polarities:

```text
dissolve(0-1) => prohibit
dissolve(2-3) | absent(0-1-2)  => prohibit
dissolve(2-3) | present(0-1-2) => prohibit
dissolve(2-3) | absent(0-2-3)  => prohibit
dissolve(2-3) | present(0-2-3) => prohibit
```

The action edges are disjoint. For the triad `0-1-2` the condition intersects the acted edge `2-3` in one vertex and the `P->P` vertices are contained in the triad. For the triad `0-2-3` the condition contains the acted edge and the vertex overlap is partial. The discovery ranking retains one pair id per predeclared quantity. The ids `600141626a884b274e29285f` and `07f18bb89362ae4ea6606830` differ in the last stored digit of the matching residual, by about `1e-16`. That gap is below the floor. The four systems are one observable value. Discovery order was not rewritten to collapse the tie.

On `600141626a884b274e29285f` the controlled values are:

| Quantity | Path to matching | Matching to path |
| --- | ---: | ---: |
| Q0 | 0.18823529411764703 | 0.752941176470588 |
| QT | 0.18808717457278007 | 0.75234869829112 |
| QP | 0.18765207631874303 | 0.7506083052749721 |
| QTP | 0.2538772345202259 | 0.6694186190536465 |
| Delta_T | −0.00014811954486695922 | −0.0005924781794679479 |
| Delta_P | −0.0005832177989039955 | −0.002332871195615871 |
| Delta_TP | 0.0656419404025789 | −0.08352255741694148 |
| I | 0.06637327774634985 | −0.08059720804185766 |
| G | 0.0650587226036749 | 0.08118968622132561 |
| Delta_S | 0.021431815558849432 | 0.036908902906276686 |
| I stationary | 0.08748920875794805 | −0.1769123557424147 |
| Occupancy contribution | 0.001325029761030383 | −0.1754787527028282 |
| Horizon-16 controlled delta | 0.027888704769459288 | −0.12749628797139034 |

The path-to-matching pair delta is positive while both singleton deltas are small and negative. The matching-to-path pair delta is much more negative than either singleton. The two directions agree in a passage sense: the controlled probability of hitting the matching before returning to the path goes up, and the controlled probability of hitting the path before returning to the matching goes down. Horizon 16 has the same signs and different magnitudes. The matching-to-path occupancy contribution, `-0.1754787527028282`, is larger than the controlled pair delta. The path-to-matching occupancy contribution is `0.001325029761030383`, much smaller than the controlled pair delta. One direction of this motif is mostly future dynamics. The other mixes a large occupancy shift with a still-large controlled shift.

The largest negative path-to-matching residual is `-0.029049739457073953`. The largest positive matching-to-path residual is `0.03494167205552434`. Four canonical systems share both values to within `1e-8`. Each is `dissolve(0-1) => prohibit` together with `dissolve(2-3) => strong_favour` conditioned on one of `absent(0-1-2)`, `present(0-1-2)`, `absent(0-2-3)`, or `present(0-2-3)`. The action edges are disjoint. The four signatures are not the same: two contain the acted edge and two intersect it in one vertex. This observable does not separate them. The discovery ids are `c78ab9dd545fe3e2125c7d31` and `a05d086daba5893e9e95791c`. The path residual is negative and the matching residual is positive, the opposite pattern from the prohibit-prohibit motif, and smaller.

## J. Super-singleton magnitude

```text
G = |Delta_TP| - max(|Delta_T|, |Delta_P|)
```

`G` is not `I`. A system can have `G > 0` with a small residual, or a large residual with `G < 0`.

`G > 0` on 1,232 path-to-matching rows and 1,264 matching-to-path rows. The median `G` is slightly positive (`0.0003199220222700472` and `0.0007712705668620479`). The median absolute `G` is `0.0034416194165916847` and `0.003818908052108272`.

The largest positive path-to-matching `G` in the discovery ranking is `0.0650587226036749`, on the same prohibit-prohibit row as the largest positive `I`. The largest positive matching-to-path `G` is `0.08118968622132583`, on `83e30a0d85355dd29a222456`, which is one of the four rows in that same tie. The discovery file keeps both ids. The values match the other members of the tie to `1e-16`.

On the strong-favour same-edge row in section K, path-to-matching `G` is `0.010113068453687396` while `I` is `-0.009689473509634255`. The pair moves the committor by more than either component, and the residual is negative because the pair overshoots the sum of two negative component deltas.

## K. Higher-order selectivity increment

`S_T` is the triad-conditioned spread of the eventual committor for the `T->P` singleton. `S_TP` is the same spread for the pair. `Delta_S = S_TP - S_T`. The spread is over the 16 configurations in `{0,1}^4`, not over the popcount.

`Delta_S > 0` on 1,948 path-to-matching rows and 1,576 matching-to-path rows. `Delta_S < 0` on 356 and 728. No row has `Delta_S` inside the floor. The median is `0.002802229464498665` and `0.0016484715846504239`. The minima are `-0.0013548922071160985` and `-0.005419568828464172`.

The largest positive path-to-matching `Delta_S` is `0.02143181555884946`, again inside the prohibit-prohibit tie (`83e30a0d85355dd29a222456` in the discovery file; the other three members match the aggregate). The largest positive matching-to-path `Delta_S` is `0.05468011300288589`. Four canonical systems share it to within `1e-8`: `dissolve(0-1) => strong_favour` with `form(0-1) => strong_favour` conditioned on `absent(0-1-2)`, `present(0-1-2)`, `absent(0-2-3)`, or `present(0-2-3)`. The discovery representative is:

```text
dissolve(0-1) => strong_favour
form(0-1) | present(0-2-3) => strong_favour
```

Pair id `a242054905a5b0245e08de79`. The action edges are the same edge. The condition triad intersects that edge in one vertex. The `P->P` vertices overlap the triad partially. Support removed is 0. On matching to path, `Delta_T` is `-0.0016943797762123403`, `Delta_P` is `-0.010788888375934835`, `Delta_TP` is `-0.05124116219068453`, `I` is `-0.038757894038537355`, and `G` is `0.040452273814749695`. Adding the pairwise strong favour increases the triad spread by `0.05468011300288589` and makes the passage change about five times the stronger singleton. The residual is negative. Selectivity amplification and a negative interaction residual occur together on this row.

## L. State-resolved interaction

For each source state, `I_state(s) = q_TP(s) - q_T(s) - q_P(s) + q_0(s)`. The full vectors are in the gitignored shard results and are removed from the published summary. The published validation block keeps the weighted mean, both extrema, and the attaining states for the predeclared extrema.

On the prohibit-prohibit representative `600141626a884b274e29285f`, path to matching, every stored source-state residual is positive. The baseline-weighted mean is `0.06637327774634989`. The maximum is `0.0943232027103007` at full state 521, triadic configuration 8. The minimum is `0.039744603249193294` at state 340, configuration 5. The aggregate does not conceal an opposite state.

On matching to path for that same row, every stored source-state residual is negative. The mean is `-0.08059720804185755`. The least negative value is `-0.040725992871065264` at state 76, configuration 1. The most negative is `-0.19574497898313614` at state 289, configuration 4. The triad range of the state residual is `0.03690890290627721`.

The recomputed members of the tie match these magnitudes and do not match the state indices. The fourth member shares the published aggregate residual and was not given a separate state recomputation. The condition polarity moves which full state attains the extremum. The aggregate residual does not move above the floor.

On `a242054905a5b0245e08de79`, matching to path, the state residuals run from `-0.06764765019978247` at state 786, configuration 12, to `-0.010452287634129864` at state 722, configuration 11. Again the source class does not change sign inside the validated row. The committor itself is smallest at triadic configuration 14 and largest at configuration 11.

## M. Horizon-16 comparison

The horizon-16 controlled delta was stored for every pair. On the prohibit-prohibit motif it has the same sign as the eventual pair delta in both directions, with magnitudes `0.027888704769459288` and `-0.12749628797139034` against eventual pair deltas `0.0656419404025789` and `-0.08352255741694148`. The finite horizon is the smaller figure on the path-to-matching side and the larger figure on the matching-to-path side. The eventual committor stays the primary quantity. The census was not re-ranked by the horizon-16 column.

Median absolute horizon-16 controlled delta: `0.008578217217492107` and `0.013769909688258475`, beside median absolute eventual residuals `0.003966107013885001` and `0.004368503087999187`. The two scales are related and they are not substitutes.

## N. Robustness validation

This section is post-selection. It covers the discovery extrema only. It is not a sensitivity census of the 2,304.

Direct recomputation reproduced every selected discovery value with absolute gap 0. The iterative fixed-point committor, tolerance `1e-12`, differs from the direct solve by at most `2.8542168628575837e-12` on these rows. Three `S4` images of each selected pair reproduce the interaction residual to at most `2.220446049250313e-16`, and every image of the pair stays in the same canonical orbit. `ranking_changed` is false. Discovery order is unchanged. A tie inside the floor was not collapsed.

`rho3 = 1/2` and `rho3 = 2` were recomputed for each selected pair, against the baseline at that same rate.

On the prohibit-prohibit motif the path-to-matching residual stays positive and the matching-to-path residual stays negative. At `rho3 = 1/2` the residuals are `0.07599633051003743` and `-0.09213189040380465`. At `rho3 = 2` they are `0.05977539321576758` and `-0.07263579969293799`. `Delta_S` stays positive in both directions at both rates: at one half, `0.046322349049654654` and `0.06948871341185447`; at two, `0.008904594293291795` and `0.01823278456949573`. Alphabet variants were not run, because both weights are prohibit and prohibit is zero in `W3`, `W4`, and `W16`. `G` was not recomputed at the alternate rates. The recorded robust quantities are the interaction residual, the pair delta, and `Delta_S`.

On the strong-favour dissolution that carries the opposite-sign residual (`c78ab9dd545fe3e2125c7d31` and its tied partner), the path residual stays negative and the matching residual stays positive at both rates and at `W3` and `W16`. Magnitudes move. At `W16` the path residual is `-0.03596931898491437` and the matching residual is `0.04169603284607426`. Matching-to-path `Delta_S` is already negative on the primary row (`-0.002911392405975155`) and stays negative at `rho3 = 2`, `W3`, and `W16`. Path-to-matching `Delta_S` stays positive and small. Interaction-residual sign is robust on this row. The selectivity increment is not robust in both directions.

On `a242054905a5b0245e08de79` the matching residual stays negative and `Delta_S` stays positive at both rates and at both alphabets. The alphabet changes the magnitude a lot, as a strong-favour grade should. At `W16` the matching residual is `-0.17986979065643494` and `Delta_S` is `0.26284325632543953`. At `W3` they are `-0.11439170471124871` and `0.16479138362407253`. Sign robustness is not magnitude robustness. The whole census was not repeated at these alphabets.

## O. Negative findings

- The interaction residual is outside the floor on every analysed pair. Approximate additivity is not the result.
- No pair creates a positive one-step toggle that the baseline and the components lack. The large committor changes are reweightings and, where a weight is prohibit, deletions.
- No pair moves the passage while both singleton deltas sit inside the floor. The pairs that dominate their components by a factor of ten still have singleton deltas above the floor, sometimes only by two orders of magnitude less than the pair.
- `Delta_S` is negative on hundreds of rows. Adding a pairwise rule does not uniformly amplify the hidden-triad spread.
- `G` is negative on nearly half the rows. A nonzero residual is not the same thing as a larger-than-either-component effect.
- Stationary and controlled residuals disagree in sign on hundreds of rows. Several Generation 4 stationary magnitudes would not survive as controlled magnitudes.
- Four canonical alignments share the strongest residual to within the floor. The observable does not distinguish those alignments. The discovery pair id is one representative.
- Horizon-16 magnitudes are not the eventual magnitudes.
- `rho3` and alphabet checks cover the selected extrema only.
- The 85,175, the other three grades, cardinality 3, simplicial semantics, and `H`, `S`, `G`, `L` above 0 were not run.
- The full state-resolved vectors are not in the published summary. They are in the shard files, which are gitignored.

## P. Inferences

OBSERVED. All 2,304 canonical systems in this targeted grammar have a controlled eventual interaction residual outside `1e-8`, in both directions. The median absolute residual is about `0.004`. About half the residual signs are positive.

OBSERVED. On a typical row that residual is about half as large as the stronger singleton component. On 76 path-to-matching rows and 12 matching-to-path rows the pair delta exceeds both component deltas by a factor of ten.

OBSERVED. The strongest value is shared by four canonical prohibit-prohibit systems: an unconditional dissolution prohibit on one edge, and a triad-conditioned dissolution prohibit on the complementary edge. Both component deltas on that motif are near `1e-4` to `2e-3`. The pair deltas are `0.0656` and `-0.0835`. `Delta_S` is positive. `G` is positive. The signs survive `rho3 = 1/2` and `rho3 = 2`. The source-state residuals on the validated representative do not change sign inside the source class.

OBSERVED. `Delta_S` is positive on a majority of rows and negative on the rest. The largest selectivity increase on matching to path is a same-edge strong-favour pair, and its interaction residual is negative.

OBSERVED. Controlling the source removes no interaction at the floor. It changes the sign of the residual on 256 and 568 rows, and it changes the matching-to-path magnitude by a median factor larger than one.

INFERRED. Constraint composition is doing something on this observable that the two singleton deltas do not add up to. Part of that something increases the influence of the hidden triadic configuration, and part of it does not. The strongest robust case is a small deletion motif on two disjoint edges, not a broad amplification by every `P->P` rule. Hidden timing, hidden transition-law information, and hidden topology-conditioned passage information were earlier distinctions. This census is evidence about a fourth: a two-rule interaction beyond the additive singleton effects. The evidence says that interaction is present, common, and alignment-dependent, and that its strongest instance is also higher-order-conditioned.

The predeclared outcome list is not a single bin. Outcome A, approximate additivity, does not fit. Outcome B does not fit the majority, because `Delta_S` is positive more often than not, and it does fit the 356 and 728 rows where the spread falls. Outcome C fits the majority counts and the prohibit-prohibit motif. Outcome D fits the sign reversals and the negative residuals, and it does not fit the coded cancellation class, which is empty. Outcome E fits the size and sign gaps between stationary and controlled residuals, and it does not fit a claim that the controlled effects vanish. Outcome F fits the disjoint prohibit motif: nonzero controlled interaction, positive triad spread, positive super-singleton gap, and rate robustness, with alphabet invariance because the weights are prohibit.

## Q. RS / global-coherence interpretation

This cell does not establish a globally coherent architecture, and it does not assign a meaning to a triad.

What it supports is narrower. Once a pairwise rule and a triad-conditioned pairwise rule act on the same independent hypergraph, the eventual passage between two non-isomorphic two-edge graphs is not the sum of the passages each rule produces alone. On the strongest motif, each rule by itself barely moves the controlled committor, and the pair moves it by several hundredths in a direction that depends on which graph is the source. The hidden triadic configuration still changes that probability, and on that motif it changes it by more than the `T->P` rule changed it alone.

That is coherent with treating constraint composition as its own layer, on top of the higher-order relation, with `H`, `S`, `G`, and `L` still 0. It tensions with two smaller readings. One is that a higher-order condition is only a weak singleton perturbation of a passage that pairwise rules already dominate. On this motif the pairwise singleton is also weak, and the composition is not. The other is that any two-rule effect is evidence of a designed global arrangement. The census is a calculation on a declared grammar. A successful stochastic mechanism is not a design conclusion.

## R. Next smallest justified experiment

Do not start it in this branch.

Simplicial face closure is not the next run. This census did find a two-rule interaction beyond the singleton parts, which was the condition under which that fork would have become the immediate candidate. A new event model would mix a different question into a motif that is not yet graded.

`H`, `S`, `G`, and `L` are not indicated. The interaction appears with all four at 0. Cardinality 3 is not indicated. The effect is already present at two rules. A second graph-class passage would ask whether the motif is special to the path and the matching. That is a real question, and it is larger than the check below.

The smallest next experiment is the same disjoint-edge dissolution motif, still one `T->P` rule and one `P->P` rule, at the three grades this census excluded: `weak_favour`, `weak_suppress`, and `strong_suppress`. The question is whether the interaction residual, `G`, and `Delta_S` survive when the prohibit deletions become finite weights. The canonicalisation should again be of the complete set. The count should be computed before the run. If those grades do not interact, the prohibit result is a deletion phenomenon and the following decision can return to a second passage or to simplicial semantics. If they do interact, the motif is a graded choreography and still does not require a new channel.

## Questions this generation was asked

1. Canonical two-rule systems analysed: 2,304. The run was exhaustive for the declared pool.
2. Relative-alignment classes: 1,280.
3. Nonzero interaction residual above `1e-8`: 2,304 in each direction.
4. Largest positive residual: path to matching `0.06637327774634985`, matching to path `0.03494167205552434`. Largest negative: path to matching `-0.029049739457073953`, matching to path `-0.08059720804185777`.
5. `G > 0`: 1,232 and 1,264.
6. `Delta_S > 0`: 1,948 and 1,576.
7. The residual extrema sit on disjoint action edges. The selectivity extremum on matching to path sits on one shared action edge. Four condition polarities share the strongest residual.
8. The pair reverses the sign of the stronger singleton effect on 344 and 312 rows. The extreme prohibit motif reverses two small negative singleton deltas on the path-to-matching side.
9. No pair moves the passage when both singleton deltas are inside the floor. Seventy-six path-to-matching pairs, including the extreme motif, exceed both components by a factor of ten. The components are small and above the floor.
10. Strong pair effects are not one class. The census splits into positive residuals, negative residuals, positive and negative `G`, and positive and negative `Delta_S`. The empty classes are additivity at the floor, and cancellation defined as a nonzero residual with a pair delta inside the floor.
11. The hidden triad becomes more influential on a majority of rows and less influential on the rest. The extreme prohibit motif increases the spread. The increase survives the two `rho3` probes on that motif.
12. Controlled and stationary residuals differ in sign on 256 and 568 rows, and they differ in magnitude by a median relative factor of about `0.67` and `1.46` where the controlled residual exceeds `1e-4`.
13. No apparent interaction falls inside the floor when the source is controlled. Some signs do not survive that control.
14. No pair adds a positive one-step toggle. 1,728 pairs remove baseline toggles. The passage change reweights existing events, and prohibit deletes some of them.
15. The strongest robust interaction is the four-member tie: `dissolve` prohibit on one edge, plus `dissolve` prohibit on the disjoint edge conditioned on one triad, either polarity. It is `K = 1` plus `K = 2`. Several alignments share the value. The discovery id is a representative, not a unique dynamical winner.
