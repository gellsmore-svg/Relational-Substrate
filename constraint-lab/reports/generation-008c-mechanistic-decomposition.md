# Generation 008C — mechanistic decomposition

Generation 8C is Mode B. It reads the transition law that Generations 8, 8A, and 8B already measured. It does not run a new stochastic census, a permutation calibration, a parameter fit, or a new control. Pass and fail in this note are reserved for tests, chronology, numerical tolerances, and CI.

The numerical record is `constraint-lab/reports/generation-008c-round-c0-tables.json`. Schema `rs-constraint-lab.mechanism-tables/v1`. File sha256 `6002bc7c817514a3d4576ced8f56d45b5a05409682ef4ab42fc32caf352b0493`. Payload sha256 `8c2f6cf73a633ab3addced919931e2c79bfe2d76b6cfa7dc58cde55ce1daccb8`. The result commit is `f962000d7c6c750565843426d46bcd3fdbb43026`. Mutual information is in nats. A float64 kernel quantity is a deterministic kernel result. A fraction identity is stated only where the arithmetic is exact.

The compression this round supports is short. A one-bit triad gate reweights one pair slot. Six-slot normalisation turns that weight into a local event law. Graph topology maps the chosen slot onto an edge-count change, and, on the path, onto a shape change at the same edge count. Triad toggles refresh the gate, so the initial value is forgotten, while the gate bit that is present continues to reweight the current slot. The long-run sparse/dense shift has the sign of that persistent bias. It is not a memory of the initial triad.

## A. External Review 008B

Review 008B is `constraint-lab/provenance/reviews/008B-chatgpt-review-v0.8b.md`. It reads branch `research/constraint-lab-v0.8b-information-calibration` at `66fc7f48ac776aec461553cfac06126ed6566626`. The review inspected branch chronology, the frozen B0 plan, the information-calibration report, the exact-kernel results, the permutation calibration, the structural zero-information controls, the numerical validation, the current-context weighting comparisons, commit `7eb63924c4c5484decd1ab5b7bee3a25b440ac68`, and the final-head CI.

The branch is 11 commits ahead of v0.8A. Final head `66fc7f48ac776aec461553cfac06126ed6566626`. Final-head Actions run `38326986030` succeeded. The frozen B0 plan is `466d54339738d315ed621ea4256a239cb026498a`, plan hash `279857bb2ee82eefd430ba56c9fa3758238ebea9e0b652c01b56b97dbc1bf618`. The B0 tables commit is `dc9f9b9eb6e4a36b4513d10b49e937c43b57b371`. No new scientific trajectories were run. B0 used 40 bounded items, `exact`, `permute-initial`, and `permute-current`, two workers, and a 120-second watchdog. Approximate item walls were 3.8 seconds for an exact item, 30–32 seconds for an initial permutation, and 14–16 seconds for a current permutation. The report-head constraint-lab suite reported 182 passed.

The first R03 exact command stopped because the implementation required an empirical class-conditional mutual information to be zero on an unconditional pair rule. That identity is not guaranteed. A finite sample can correlate the triad with which labelled mask inside one graph class was visited, while the slot law varies across those masks. Commit `7eb63924c4c5484decd1ab5b7bee3a25b440ac68` corrected the validation assertion. The structural zero that remains is `I(current triad ; next pair slot | full labelled pair mask) = 0` for R00, R03, and R07. The frozen estimands did not change.

The review's scientific record, which C0 explains, is the following. The 336 Generation 8A plug-in cells reproduce with maximum absolute gap `2.810e-16`. The first-destination permutation-null mean is about 0.03024–0.03127 nats. The largest plug-in cell, R03 star at 0.07021 nats, is a structural-zero system whose exact first-destination information is below `1e-10`. Exact first-destination information is at the floor for R00, R03, R07, and for every path source. On star and triangle the conditioned values are R01 `5.699e-7`, R02 `3.307e-7`, R04 `3.307e-7`, R05 `2.025e-5`, and R06 `1.906e-7` nats. The plug-in checkpoint signal near 0.12–0.14 nats through epoch 512 was estimator bias. The largest exact class information is R06 path at checkpoint 1, 0.02798 nats. By checkpoint 64 every exact class information is below `1e-10`. At checkpoint 1, star and triangle carry edge-count information only. Path carries an additional shape term. Exact 512-epoch dense-minus-sparse context ranges are at most 0.001925 nats of variation, beside grade-driven occupancy shifts of order `10^-1`. Balanced full-mask slot information is 0.009749 nats on R01, R02, and R04, 0.010413 on R05, and 0.023368 on R06. Stationary values are 0.012025, 0.013240, and 0.016895. Class conditioning retains 0.661, 0.710, and 0.443 of those stationary values. Information in the next graph class given the current graph class is about 0.001–0.0026 nats.

Prompt 008B authored metadata, recorded beside the agent input and not assigned to it: 41,183 bytes, sha256 `7bcbfc788747c7280ef514721e0d2620413aa5ba2e8a8744ff75b8d093e7fc0f`. The stored agent input is 41,188 bytes, sha256 `3f77c124b444446a78c3020a838fa65ddc9f2fddc08690ffff082ee94a70b660`. The authored file is not in this working environment. Status `externally_verified_pending_import`. Relationship `unknown`.

## B. Question

The governing question is how a higher-order triadic condition alters the local lower-order event law, how visible graph topology converts that local event bias into an edge-count change or a shape change, and why the influence of the initial triadic context is forgotten on this grammar.

The useful content is the multiscale structure. A one-bit gate measurably alters a six-way lower-order event law. The influence of that bit's initial value decays to the floor. The bit that is instantiated now continues to alter the present transition. A non-zero conditional mutual information, by itself, is the direct consequence of a rule that reads the bit. The propagation is the result.

Graph classes in this note are descriptors of pair relations. No organisation, repair, routing success, boundary, or preferred graph is encoded or scored.

## C. Frozen C0 plan

The frozen analysis plan is commit `3e783387cd2c8050559c29bac059beae03555ab7`, plan hash `febde3989a8b2f2461440e708897fe78c1fdac436375c0c628b393309932c897`, file `constraint-lab/exploration/generation-008c/round-c0-plan.json`. It was committed and pushed before any C0 quantity was stored. Journey step 1, commit `ffbc19a036eee534be3b893aec7dd100a6d5839d`, still has `result_commit` null. Actions run `38354878731` succeeded on that pre-execution commit. It is not a run of the tables commit or of this report. Journey step 2 names the tables commit `f962000d7c6c750565843426d46bcd3fdbb43026`. That commit descends from the frozen plan.

C0 is the only round. The palette is the Generation 8A repair palette, R00 through R07. The parent tables file is pinned at sha256 `d7bc06d027eabb62f5f2e5bed312c746ef3f062198a25a35bd5246ce23590e09`. The closed-form candidates and the rounded checkpoint-1 figures sit in the plan as comparison targets. The derivation does not read them as inputs. Tolerances frozen before execution: closed form, conditional-mutual-information equality, chain rule, symmetry, gate memory, drift identity, and kernel row at `1e-12`; stationary drift at `1e-9`; checkpoint reproduction against the Generation 8B kernel rows at `1e-8`; rounded prose at `5e-6`; zero-information floor `1e-10`.

Sixty items ran in process. Each item is one deterministic kernel or enumeration. The largest wall was 1.413 seconds. The 120-second watchdog was not approached. The supervisor was not used. Validation of the assembled payload reported no problem. No stochastic trajectory was sampled.

## D. The minimal local rule

The W4 alphabet is base 2. `strong_suppress` is grade −2, factor `1/4`. `strong_favour` is grade +2, factor `4`. The kernel gives every slot baseline weight 1 and multiplies a slot by the factor when a constraint matches that slot. The pair-event law renormalises the six pair weights.

A match requires the action slot to be the toggled slot, the action bit to be in the polarity's admissible state, and each condition bit to agree. For one conditional pair rule the admissible state is one bit, and the condition in this palette is one triad bit. Enumeration over all 1024 states puts the six-slot law into two values. It is uniform when the rule is inactive. It is the one-slot reweight when the action is admissible and the gate matches. The other eight bits do not split either group. The exact weight gap against the implementation is `0/1`. There are 256 active states.

The one-bit conjunction of admissibility and the gate is a sufficient statistic for this local law. The two raw bits are also sufficient, and three of their four pairs share the uniform law, so the conjunction is the smaller statistic. Neither statistic is claimed to determine the future trajectory. Later pair masks depend on which slot was chosen, and the gate continues to move.

R01 is `dissolve(0-1) | absent(0-1-2) => strong_suppress`. R02 is `form(0-1) | absent(0-1-2) => strong_suppress`. R04 is `dissolve(2-3) | present(0-1-2) => strong_suppress`. R06 is `dissolve(0-1) | absent(0-1-2) => strong_favour`. Each names one action slot and one gate.

## E. Closed-form pair-slot law

When the rule is inactive, each of the six pair slots has probability `1/6`. When the rule is active and exactly one slot carries multiplier `m`,

```text
q(action) = m / (m + 5)
q(other)  = 1 / (m + 5)
```

For `m = 1/4` the action probability is `1/21` and each other probability is `4/21`. For `m = 4` the action probability is `4/9` and each other probability is `1/9`. Every relevant state in the 1024-state enumeration matches these rows.

Under the balanced weighting, 32 of 64 pair masks make the action admissible, and on each of those masks 8 of 16 triads match the gate. The remaining masks contribute zero. The balanced conditional mutual information is therefore

```text
I_balanced = (1/2) JS(q_0, q_m)
```

with equal weight on the two gate states inside an admissible mask. This factor is the state count.

| System | Multiplier | Direction | Gate | Analytic | Enumerated | Gap |
| --- | --- | --- | --- | --- | --- | --- |
| R01 | 1/4 | dissolve | absent | 0.009748566529643857 | 0.009748566529643059 | 7.980e-16 |
| R02 | 1/4 | form | absent | 0.009748566529643857 | 0.009748566529643060 | 7.962e-16 |
| R04 | 1/4 | dissolve | present | 0.009748566529643857 | 0.009748566529642743 | 1.114e-15 |
| R06 | 4 | dissolve | absent | 0.023368444772049440 | 0.023368444772049621 | 1.804e-16 |
| R05 | 1/4 and 1/4 | composite | mixed | 0.010413087564076735 | 0.010413087564075357 | 1.377e-15 |

The single-rule rows agree with the Generation 8B balanced kernel values inside `1e-12`. The pre-registered candidates were 0.009748566529643855 and 0.02336844477204944. The analytic values sit on those candidates to `1e-15` or better. The strongest local higher-order information in Generation 8B is the information in reweighting one of six pair slots, averaged over a gate that is on for a quarter of the balanced states.

## F. Why suppress and favour are asymmetric

`m = 1/4` and `m = 4` are reciprocals of the slot weight. They are different distances from the uniform law, because five slots keep weight 1.

| Grade | Action probability | Other probability | Total variation | JS from uniform | Balanced CMI |
| --- | --- | --- | --- | --- | --- |
| strong_suppress | 1/21 | 4/21 | 5/42 | 0.019497133059 | 0.009748566529643857 |
| strong_favour | 4/9 | 1/9 | 5/18 | 0.046736889544 | 0.023368444772049440 |

The ratio of the total variations is `7/3`. The same ratio appears in the Jensen-Shannon terms and in the closed-form edge drifts below. Favour moves one slot from `1/6` to `4/9`. Suppression moves it from `1/6` to `1/21`. The favour displacement is larger, so the local information is larger. Both informations remain small on the nat scale.

## G. Why R01, R02, and R04 are locally equivalent

The balanced formula depends on there being one active slot, one multiplier, and one binary gate that is on for half of the triads on half of the masks. It does not depend on whether the action is a formation or a dissolution, on which of the six slots is named, or on whether the gate polarity is present or absent. R01, R02, and R04 meet that description with `m = 1/4`. Their enumerated balanced values differ by at most `3.2e-16`.

This is an equivalence of the balanced local law. Two labelled conjugacies make the same point and stop there.

Complementing every relation bit except the gate bit `0-1-2` takes the R02 kernel to the R01 kernel. The largest absolute transition-probability gap is 0. Flipping the gate bit and exchanging pair slots `0-1` and `2-3` takes the R04 kernel to the R01 kernel. That gap is also 0. Both maps send some pair masks to a different isomorphism class. The star mask 7, class `e3-deg3111-tri0-comp1`, is sent by the slot exchange to mask 38, class `e3-deg2220-tri1-comp2`. Labelled slot information is preserved because the map is a bijection of slots. Graph class is not.

A further measured identity sits in the stationary projection atlas. Class masses of R01 and R04 agree to a maximum absolute difference of `1.424e-15`. Their full-mask and class-conditional slot informations agree at the same floor. The slot exchange does not imply that identity, because it is not a class homomorphism. It is reported as measured. R02's stationary masses are not the R01 masses. The largest absolute class-mass difference is 0.02841, and the loss leaders of R02 are the edge-complement of the loss leaders of R01: the R01 loss on `e2-deg2110-tri0-comp2` reappears as the R02 loss on `e4-deg3221-tri1-comp1`, with the same mass 0.1733.

R02 and R04 are also inadmissible on every canonical 3-edge source used below. Edge `0-1` is already present, so a formation of that edge cannot fire. Edge `2-3` is absent, so a dissolution of that edge cannot fire. Their checkpoint-1 class information on those sources is at the floor. Local equivalence does not imply equal source trajectories.

## H. R05 composite normalisation

R05 is `dissolve(0-1) => strong_suppress` together with `dissolve(2-3) | present(0-1-2) => strong_suppress`. The local law depends on three bits: whether edge `0-1` is present, whether edge `2-3` is present, and the gate. Dropping any one of them splits a law. The eight bit patterns produce four distinct laws. The formula gap on those laws is `0/1`.

Edge `2-3` absent contributes no triad dependence, including when edge `0-1` is present and the unconditional rule is on. The gate is unread, and the unconditional weight does not depend on the triad. The two strata that carry information are each 16 of the 64 masks.

On edge `2-3` present and edge `0-1` absent, the gate-off law is uniform and the gate-on law is `q_{1/4}` on slot `2-3`. The equal-weight divergence is 0.019497133059 nats, the single-rule Jensen-Shannon value. On both edges present, the gate-off law is `q_{1/4}` on slot `0-1`, and the gate-on law puts weight `1/4` on both slot `0-1` and slot `2-3`. The total weight is `9/2`. Those two slots each have probability `1/18`, and each of the other four has probability `2/9`. The divergence of that pair of laws is 0.022155217197 nats.

The balanced information is one quarter of the first divergence plus one quarter of the second. The stored analytic value is 0.010413087564076735 nats. The enumerated value is 0.010413087564075357 nats. The gap is `1.377e-15`. The single-rule value is smaller because the both-edges stratum replaces `JS(q_0, q_m)` with a different divergence between two already-biased laws. That difference is a shared denominator. Two weighted slots are normalised together.

This local interaction is not the Generation 5 or Generation 6 committor interaction, and it is not the Generation 8 occupancy residual of the composite. Those are multistep statements about passage and about class share. The denominator identity is one pair event.

## I. One-step topology atlas

The canonical sources are star mask 7, path mask 13, and triangle mask 11. Each row is one pair-slot toggle. The class names are the canonicaliser's.

| Source | Slot | Relation | Direction | Category | Edges | Class |
| --- | --- | --- | --- | --- | --- | --- |
| star | 0 | 0-1 | dissolve | spoke | 2 | e2-deg2110-tri0-comp2 |
| star | 1 | 0-2 | dissolve | spoke | 2 | e2-deg2110-tri0-comp2 |
| star | 2 | 0-3 | dissolve | spoke | 2 | e2-deg2110-tri0-comp2 |
| star | 3 | 1-2 | form | rim | 4 | e4-deg3221-tri1-comp1 |
| star | 4 | 1-3 | form | rim | 4 | e4-deg3221-tri1-comp1 |
| star | 5 | 2-3 | form | rim | 4 | e4-deg3221-tri1-comp1 |
| triangle | 0 | 0-1 | dissolve | triangle_edge | 2 | e2-deg2110-tri0-comp2 |
| triangle | 1 | 0-2 | dissolve | triangle_edge | 2 | e2-deg2110-tri0-comp2 |
| triangle | 2 | 0-3 | form | pendant | 4 | e4-deg3221-tri1-comp1 |
| triangle | 3 | 1-2 | dissolve | triangle_edge | 2 | e2-deg2110-tri0-comp2 |
| triangle | 4 | 1-3 | form | pendant | 4 | e4-deg3221-tri1-comp1 |
| triangle | 5 | 2-3 | form | pendant | 4 | e4-deg3221-tri1-comp1 |
| path | 0 | 0-1 | dissolve | path_middle | 2 | e2-deg1111-tri0-comp2 |
| path | 1 | 0-2 | form | path_short_chord | 4 | e4-deg3221-tri1-comp1 |
| path | 2 | 0-3 | dissolve | path_end | 2 | e2-deg2110-tri0-comp2 |
| path | 3 | 1-2 | dissolve | path_end | 2 | e2-deg2110-tri0-comp2 |
| path | 4 | 1-3 | form | path_short_chord | 4 | e4-deg3221-tri1-comp1 |
| path | 5 | 2-3 | form | path_long_chord | 4 | e4-deg2222-tri0-comp1 |

The path categories are one middle edge, two ends, two short chords, and one long chord. `e2-deg1111-tri0-comp2` is the 2-edge matching. `e2-deg2110-tri0-comp2` is the 2-edge path. `e4-deg2222-tri0-comp1` is the 4-cycle. `e4-deg3221-tri1-comp1` is the triangle with a pendant edge.

## J. Why path carries shape information

From the star, every dissolution leads to `e2-deg2110-tri0-comp2` and every formation leads to `e4-deg3221-tri1-comp1`. From the triangle, the same two classes exhaust the two edge counts. Inside either edge-count direction there is one isomorphism class. A gate that reweights one slot can change the probability of losing an edge or gaining an edge. It cannot change the shape given that edge count. At the first pair event, `I(initial triad ; class | edge count) = 0` on star and on triangle for that structural reason.

From the path, edge count 2 contains both the matching and the 2-edge path. Edge count 4 contains both the 4-cycle and the triangle-plus-pendant. The partition is

```text
dissolve an end     -> 2 edges, 2-edge path
dissolve the middle -> 2 edges, 2-edge matching
form a short chord  -> 4 edges, triangle plus pendant
form the long chord -> 4 edges, 4-cycle
```

R01 and R06 act on edge `0-1`. On the canonical path that edge is the middle. The gate changes the probability of the unique dissolution that produces the matching. The other two dissolutions produce the 2-edge path. Shape given edge count can be nonzero at the first pair event because the biased slot has a private class inside its edge count.

On the star the same action is one of three spokes, and all three spokes share a class. On the triangle it is one of three triangle edges, and those three share a class. R02's formation of `0-1` is inadmissible on all three sources, because the edge is present. R04's dissolution of `2-3` is inadmissible because that edge is a missing rim, a missing pendant, or the missing long chord.

## K. Reconstructing checkpoint 1

Checkpoint 1 is the first pair-event epoch. The initial distribution is the canonical source mask with a uniform raw triad. The landing kernel sums every path that toggles only triad bits and then takes one pair slot. The class information is computed from that landing. It is not the slot law of the initial state.

| System | Source | Class | Edge count | Shape given edge | Immediate class | Epoch-versus-immediate TV |
| --- | --- | --- | --- | --- | --- | --- |
| R01 | path | 0.010230532737 | 0.001392555411 | 0.008837977327 | 0.019497133059 | 1.044e-3 |
| R01 | star | 0.001392555411 | 0.001392555411 | 0 | 0.002566343847 | 6.266e-4 |
| R06 | path | 0.027980335340 | 0.008801031906 | 0.019179303434 | 0.046736889544 | 6.039e-3 |
| R06 | star | 0.008801031906 | 0.008801031906 | 0 | 0.014362591564 | 3.623e-3 |
| R00 | path | 3.3e-16 | 0 | floor | floor | floor |
| R02 | path | 3.3e-16 | 0 | floor | floor | floor |
| R04 | path | 3.3e-16 | 0 | floor | floor | floor |

Triangle agrees with star to the printed floor. The chain rule `class = edge + shape` closes to `2e-16`. These epoch rows reproduce the Generation 8B checkpoint-1 kernel values inside `1e-12`. The edge term of the path equals the edge term of the star. On the path, the class information is larger by the shape term. On the star, the three spokes are one class, so the class sees only the edge-count part of the same slot bias.

The immediate column forces the first full event to be a pair event at the initial mask. On the path that mask is admissible, so the gate splits the triads in half and the immediate class information is the full Jensen-Shannon divergence, 0.019497 nats for R01 and 0.046737 nats for R06. The epoch values are smaller. The difference is the triad-only excursion.

## L. Triad-only excursions before the first pair event

Before the pair event the chain may toggle triad bits any number of times. On a fixed pair mask the baseline has six pair slots and four triad slots, each of weight 1, so the probability that the pair event is immediate is `6/10 = 0.6`. The probability that the pre-pair gate still equals the initial gate is 0.875. The probability that the gate flips at least once is `1/7`. The mean excursion length is `2/3`.

A reweighted pair slot changes those figures, because it changes the probability of leaving by a pair event.

| System | Immediate | Gate still equal | Flipped at least once | Mean length |
| --- | --- | --- | --- | --- |
| R00 | 0.600000 | 0.875000 | 0.142857 | 0.6667 |
| R01 | 0.583784 | 0.868421 | 0.151429 | 0.7135 |
| R06 | 0.646154 | 0.891304 | 0.121429 | 0.5507 |

The overlap of "still equal" and "flipped at least once" is a flip that returned. It is about 0.020 on R01 and about 0.013 on R06.

The selected slot, conditional on the initial gate, is diluted relative to the pure active law. For R01, gate 0 is the active polarity. Slot `0-1` is selected with probability 0.064327, against the pure active value `1/21 = 0.047619`. Each other slot has probability 0.187135, against `4/21 = 0.190476`. For R06 the active slot has probability 0.42029, against `4/9 = 0.444444`. Favour makes the pair event more probable while the gate is active, so there is less time for the gate to flip, and more of the initial bias survives to checkpoint 1. Suppression does the opposite. That is why the R06 checkpoint-1 informations are larger than a rescaling of the R01 informations by the local Jensen-Shannon ratio alone would suggest. The excursion length depends on the grade.

On R02 and R04 the action is inadmissible on the source mask. Triad toggles do not change the pair mask, so the action stays inadmissible until the first pair event. The first pair event is the uniform six-slot law. Checkpoint-1 information of the initial triad is at the floor. Later checkpoints can become nonzero once the pair mask has moved onto a mask where the action is admissible. The path memory curves of R02 and R04 are not part of the C0 memory item set. Their checkpoint-1 agreement with R00 is structural.

## M. Gate-memory decay

The joint of the initial triad and the current full state was propagated by the pair-event landing kernel at checkpoints 0, 1, 2, 4, 8, 16, 32, and 64. The curves below are the path source. Star and triangle give the same mutual informations to the printed digits. Every distribution has mass 1 within `1e-12`.

R00, with the coordinate `0-1-2` tracked even though no rule reads it:

| Checkpoint | I(gate; gate) | Pr(equal) | I(triad; triad) | I(gate; mask) | I(triad; mask) |
| --- | --- | --- | --- | --- | --- |
| 0 | 0.693147 | 1 | 2.772589 | 0 | 0 |
| 1 | 0.316377 | 0.875000 | 1.283515 | floor | floor |
| 4 | 0.050927 | 0.658203 | 0.206835 | floor | floor |
| 16 | 5.023e-5 | 0.505011 | 2.010e-4 | floor | floor |
| 64 | floor | 0.500000 | floor | floor | floor |

R01 path:

| Checkpoint | I(gate; gate) | Pr(equal) | I(triad; triad) | I(gate; mask) | I(triad; mask) |
| --- | --- | --- | --- | --- | --- |
| 1 | 0.303953 | 0.868421 | 1.235816 | 0.01023053 | 0.01023053 |
| 2 | 0.155996 | 0.771603 | 0.637079 | 0.01257941 | 0.01257941 |
| 4 | 0.044314 | 0.647604 | 0.182410 | 0.00907686 | 0.00907686 |
| 8 | 0.003769 | 0.543331 | 0.016017 | 0.00209163 | 0.00209163 |
| 16 | 2.565e-5 | 0.503578 | 1.280e-4 | 4.715e-5 | 4.715e-5 |
| 32 | 7.119e-10 | 0.500019 | 8.052e-9 | 7.977e-9 | 7.977e-9 |
| 64 | floor | 0.500000 | floor | floor | floor |

R06 path:

| Checkpoint | I(gate; gate) | Pr(equal) | I(triad; triad) | I(gate; mask) | I(triad; mask) |
| --- | --- | --- | --- | --- | --- |
| 1 | 0.350876 | 0.891304 | 1.424510 | 0.02798034 | 0.02798034 |
| 2 | 0.193698 | 0.799976 | 0.796506 | 0.02986329 | 0.02986329 |
| 4 | 0.061101 | 0.672589 | 0.258312 | 0.01390642 | 0.01390642 |
| 8 | 0.006357 | 0.556215 | 0.028309 | 0.00132870 | 0.00132870 |
| 16 | 7.113e-5 | 0.505954 | 3.516e-4 | 1.311e-5 | 1.311e-5 |
| 32 | 8.987e-9 | 0.500067 | 5.546e-8 | 1.603e-9 | 1.603e-9 |
| 64 | floor | 0.500000 | floor | floor | floor |

The gap between `I(initial full triad ; pair mask)` and `I(initial gate bit ; pair mask)` is about `1e-16` on R01 and on R06 at every stored checkpoint. The other three triad bits retain memory of themselves, visible in `I(triad ; triad)` above `I(gate ; gate)`, and they carry no additional pair-mask information. The decay of the pair projection is the decay of the gate bit.

At checkpoint 1, `I(gate ; pair mask)` equals the path class information. It is larger than the star class information by the path's shape term, 0.008838 nats on R01 and 0.019179 nats on R06. The star's three spokes are one class, so isomorphism discards which spoke moved. The path's middle edge has a private class, so the class keeps the mask information.

The pair-mask information rises slightly from checkpoint 1 to checkpoint 2 and then falls. By checkpoint 32 it is below `1e-8`. By checkpoint 64 it is below the `1e-10` floor on every stored system and source. The Generation 8B statement that exact class information is gone by epoch 64 is this mixing.

## N. Current context after initial memory is lost

The balanced current-context informations stay at the closed form after epoch 64: 0.009748566529643857 nats for R01, R02, and R04, and 0.023368444772049440 nats for R06. The stationary values stay at 0.01202466 and 0.01689541 nats. R00, R03, and R07 stay at the floor.

There is no paradox in the pair of limits. `I(T_0 ; P_k)` is information about which initial triad was drawn. Triad toggles replace that bit. `I(T_k ; next slot | P_k)` is information about the bit that is present when the weight is computed. The rule multiplies a slot by `m` when that current bit matches. Forgetting the initial value leaves the current multiplication in place.

The same separation is visible on R00. The unused gate coordinate mixes from probability 1 to probability 1/2, and the pair mask carries no information about the initial triad at any checkpoint. Mixing of a bit is ordinary Markov refresh. Pair-mask information appears only when a rule reads the bit.

## O. Full-mask contribution atlas

Each of the 64 labelled masks has a balanced contribution and a stationary contribution. The contributions sum to the enumerated conditional mutual informations. The sum gaps are at most `1.6e-15`.

For R01, R02, R04, and R06, every mask on which the action is inadmissible contributes zero within `2e-17`. Every admissible mask contributes the same balanced amount. For R01 that amount is `JS/64 = 0.0003046427` nats, and 32 masks sum to the closed form. For R06 every admissible mask contributes 0.0007302639 nats. The active-mask span is zero to `1e-15`. Stationary differences among those masks come from the stationary pair-event weight of the mask, not from a different local law.

R05 does not have one active value. Admissible masks, those with edge `2-3` present, split into the companion-absent contribution and the both-edges contribution. The span of those balanced contributions is `4.153e-5` nats. Thirty-two masks still contribute zero. R00, R03, and R07 have 64 zero-contribution masks, and their balanced totals sit at the signed floor around `1e-15`.

## P. Why graph-class projection loses information

Replacing the full labelled mask by the isomorphism class mixes masks whose slot laws differ. The stationary account is

| System | Full-mask CMI | Class CMI | Retained fraction | Discarded | Next class given class |
| --- | --- | --- | --- | --- | --- |
| R01 | 0.01202466 | 0.00794553 | 0.66077 | 0.00407913 | 0.0009723 |
| R02 | 0.01202466 | 0.00794553 | 0.66077 | 0.00407913 | 0.0009723 |
| R04 | 0.01202466 | 0.00794553 | 0.66077 | 0.00407913 | 0.0009723 |
| R05 | 0.01324043 | 0.00939972 | 0.70993 | 0.00384070 | 0.0025706 |
| R06 | 0.01689541 | 0.00749224 | 0.44345 | 0.00940317 | 0.0011959 |

The loss summed over classes matches `full − class` to `1e-15`. R00, R03, and R07 have full-mask values at the signed floor. Their retained fraction is left undefined. Dividing two floors is not a statement.

The information in the next graph class given the current graph class is a coarser observable still. It is about 0.001–0.0026 nats on the conditioned systems, in line with Generation 8B. Most of the local slot information does not survive as a change of isomorphism class. It is information about which labelled slot moves inside a class, or about an edge-count change that several classes share only in part.

## Q. R06 projection-loss mechanism

The largest R01 losses, in nats of stationary contribution, are the 3-edge path class `e3-deg2211-tri0-comp1` at `9.115e-4` (labelled 0.012025 against class 0.007163, mass 0.1875, 12 masks), `e2-deg2110-tri0-comp2` at `8.567e-4`, and `e4-deg3221-tri1-comp1` at `7.748e-4`. The 3-edge path class contains the action edge as a middle edge, as an end edge, or not at all. Those masks do not share a slot law. Isomorphism identifies them.

R06's largest losses are `e4-deg3221-tri1-comp1` at `2.091e-3`, the same 3-edge path class at `2.083e-3` (labelled 0.01690 against class 0.00579, mass 0.1875), and `e2-deg2110-tri0-comp2` at `1.669e-3`. The absolute discarded information is 0.009403 nats, against 0.004079 for R01.

The fraction moves the other way when occupancy is removed. Under the balanced weight, R01 retains 0.48472 of its full-mask information and R06 retains 0.64704. Favour's law is farther from uniform, and a larger share of that stronger bias remains visible after masks in a class are mixed. The absolute discarded amount is still larger for favour, 0.008248 against 0.005023.

Swapping the stationary occupancies separates the two effects. The R06 law on the R01 occupancy retains 0.82306. The R01 law on the R06 occupancy retains 0.30836. The stationary fraction 0.443 for R06 is the favour law sitting on the sparser occupancy that favour-dissolution produces. It is an occupancy effect on top of the normalisation. The same labelled geometry loses a different fraction because the multiplier changes which masks are occupied, not because the masks change their membership in a class.

## R. Local edge-count drift

For a pair event, formation changes the edge count by `+1` and dissolution by `−1`. The expected change is the six-slot law contracted with those signs. The baseline, with uniform slots, depends only on how many edges are present. The rule-induced part is the difference between the gated law and that baseline.

On an active rule the induced part has a closed form in the edge count `k`. Strong-suppress dissolution contributes `(6−k)/21`. Strong-favour dissolution contributes `(k−6)/9`. Strong-suppress formation contributes `−k/21`. The gate must match and the action must be admissible. Every other stratum contributes 0, including a dissolution rule on the complete graph, where every slot already removes an edge, and a formation rule on the empty graph. The formula matches the enumerated induced drift to `3.3e-16` on every mask and gate of R01, R02, R03, R04, R06, and R07.

| System | Sign when active | Balanced induced drift | Stationary expected drift | Closed form |
| --- | --- | --- | --- | --- |
| R00 | none | 0 | floor | undefined |
| R01 | positive | +5/168 | floor | yes |
| R02 | negative | −5/168 | floor | yes |
| R03 | positive | +5/84 | floor | yes |
| R04 | positive | +5/168 | floor | yes |
| R05 | composite | +0.09325397 | floor | undefined |
| R06 | negative | −5/72 | floor | yes |
| R07 | negative | −5/36 | floor | yes |

`5/168` is 0.02976190. `5/72` is 0.06944444. The favour-to-suppress magnitude ratio on the one-gate rules is `7/3`, the same ratio as the total-variation asymmetry. The unconditional rules R03 and R07 are twice the corresponding one-gate rules, because the gate no longer turns the weight off on half the triads. R05's balanced induced drift, 0.093254, is larger than R03's 0.059524. Both weighted slots, when they are admissible together, push the edge count in the same direction. The stationary expected drift is at most `3.3e-15` in absolute value. That zero is the stationarity identity. Edge count is a function of state, and the pair-event-weighted average of its expected change is zero when the weighting is the stationary pair-event distribution. It does not say the rule is idle.

## S. From local drift to the Generation 8 occupancy axis

Generation 8 measured dense-minus-sparse pair-epoch shares. The strong-grade entries that match this palette are S09 `+0.2399`, S10 `+0.1684`, S11 `+0.0697`, S01 `+0.0645`, S00 `+0.0061`, S05 `−0.0617`, S12 `−0.0841`, and S16 `−0.1396`. Generation 8A's exhaustive repair of the same expressions gave R05 `+0.2378`, R03 `+0.1728`, R01 `+0.0723`, R04 `+0.0691`, R00 `+0.0033`, R02 `−0.0711`, R06 `−0.0854`, and R07 `−0.1448`.

The signs agree with the induced drift. Suppressing dissolution raises expected edge count, and those systems sit on the dense side of baseline. Favouring dissolution lowers expected edge count, and those systems sit on the sparse side. Suppressing formation lowers expected edge count, and R02 sits on the sparse side. The unconditional grade moves the balanced drift by twice the one-gate amount, and the occupancy shift of R03 is larger than that of R01, and the shift of R07 is larger than that of R06, in the same direction. R05's local drift is larger than R03's, and R05's occupancy shift is the largest dense shift in the palette.

The mean drift does not determine those occupancy numbers. A positive drift at a mask says the next pair event tends to add an edge from that mask. The stationary distribution is the balance of that tendency across all masks, including masks where the rule is off and the baseline drift points the other way. The 3-edge layer near 0.314 is not derived here. The local mechanism fixes the direction of the grade effect and the reason an unconditional rule outruns a one-gate rule of the same grade. It leaves the layer masses to the global balance.

## T. Mechanism hierarchy

Each arrow was checked by a kernel quantity in the hierarchy item.

The gate bit and the action bit determine the local law. The closed-form gap is `8e-16` on R01 and `2e-16` on R06.

One slot is reweighted. The resulting law is `m/(m+5)` and `1/(m+5)`, and the balanced information is half the Jensen-Shannon divergence. Favour's total variation is `5/18` and suppression's is `5/42`.

Topology maps the slot. The path has more than one class at edge counts 2 and 4. The star has one. The epoch shape term is 0.008838 nats on R01 path and 0 on R01 star.

Repeated pair epochs erase the initial gate's information in the pair mask, from 0.010231 nats at checkpoint 1 to below `1e-10` at checkpoint 64 on R01. R00's pair-mask information stays at the floor throughout. The current balanced information stays at 0.009749 nats.

The rule-induced drift has the sign of the occupancy axis, and the stationary average of expected edge change is numerical zero.

The hierarchy that survives those checks is:

```text
triad gate state
→ one pair slot reweighted
→ six-slot law changes by normalisation
→ topology maps that slot to an edge-count change, and on the path to a shape
→ the current pair state changes
→ mixing refreshes the gate and erases the initial value
→ the current gate still modifies the local law
→ long-run occupancy follows the persistent bias of the rule
```

The last arrow is a sign and a comparison of magnitudes across rule families. It is not an equality between mean drift and stationary share.

## U. Observations

The observations are the identities, enumerations, and kernel values above. In short:

The W4 factors are `1/4` and `4`. The single-rule law is uniform or the one-slot formula, with weight gap `0/1`. Balanced informations are 0.009748566529643857 and 0.023368444772049440 nats. R05's mixture is 0.010413087564075357 nats. Star and triangle have one class per edge count at the first toggle. The path has two classes at edge count 2 and two at edge count 4. The epoch kernel reproduces the Generation 8B checkpoint-1 split. Excursions dilute the gate, and favour shortens them. Gate-bit information in the pair mask equals full-triad information in the pair mask, and both are below the floor by epoch 64. Admissible masks share one balanced contribution on a single-rule system. Class projection retains 0.66077 or 0.44345 of the stationary slot information, and the fraction reversal is occupancy. Induced drift has the closed forms `(6−k)/21`, `(k−6)/9`, and `−k/21`, with balanced means `+5/168`, `−5/168`, and `−5/72`. Stationary expected drift is numerical zero.

## V. Inferences

Path topology converts a one-slot bias into shape-given-edge information, because the biased slot is the middle edge and that edge has a private class inside its edge count. Star and triangle convert the same kind of bias into edge count only, because every toggle at a given edge count shares a class.

Initial-context information decays because the gate bit is refreshed by triad toggles. The other triad bits are not what the pair mask remembers. After the initial bit is forgotten, the current bit still gates the transition. The two statements are readings of one rule at two times.

The Generation 8 occupancy axis has the sign of the local edge drift. Unconditional rules produce a larger balanced drift than one-gate rules of the same grade, and their occupancy shifts are larger in that direction. The stationary distribution is not given by the drift mean.

R01, R02, and R04 are the same balanced local mechanism. Their source trajectories differ where the named action is inadmissible. R05's extra local information is a shared denominator, which is a different fact from its multistep composition residual.

## W. RS / global-coherence interpretation

Inside this model, a higher-order bit can be locally effective and globally forgotten as an initial condition. The effect that persists is the bias of the rule that reads whatever bit is present, and that bias is visible as an occupancy shift that unconditional pair rules can also produce, often more strongly. Local higher-order dependence is therefore a real feature of the transition law and a weak diagnostic of a higher-order ontology. The large occupancy axis is robust and, on this palette, mostly a grade effect.

Nothing here shows that a physical or biological system uses this grammar. Nothing here infers a designer. The H=0 forgetting is a property of a state that stores the current relations and not a history. It is an observation about that state. A small exact gate can still be the mechanism of a larger coordinate, as the drift sign shows, without the gate's information being large and without its initial value lasting.

The coherence ledger keeps those dimensions apart. The local information is small, exact, and local. The occupancy shift is large, robust, and stationary, and its higher-order specificity is limited by the unconditional rules. The initial-context footprint is very small and transient.

## X. Next exploration options

No option is selected.

A. Study the same mechanism at the weak grades and as a surface in the multiplier `m`. The closed form is already written for general `m`. Attention: CN 3, RD 1, RC 2, EC 5, CG 3, CB 5.

B. Move from one triad gate to two higher-order gates and ask how the local coordinates compose. R05 shows a denominator interaction with one gate. Attention: CN 4, RD 2, RC 2, EC 4, CG 4, CB 4.

C. Introduce explicit history `H>0` and ask whether a local higher-order context can leave a lower-order memory that this grammar forgets. Rapid forgetting at `H=0` is not treated as a defect. Attention: CN 5, RD 3, RC 4, EC 3, CG 5, CB 2.

D. Expand to `N=5` while keeping the local-rule grammar. The state space leaves the 1024-state enumeration. Attention: CN 3, RD 3, RC 2, EC 2, CG 3, CB 1.

E. Explore meta-constraints, constraints on constraints. No geometry is defined yet. Attention: CN 4, RD 1, RC 1, EC 2, CG 3, CB 2.

F. Return to open trajectory exploration with a palette informed by this mechanism. Attention: CN 2, RD 4, RC 4, EC 2, CG 3, CB 3.

G. Stop this line and integrate the mechanism into the broader RS formalism. Attention: CN 1, RD 1, RC 1, EC 4, CG 5, CB 5.

The coordinates are contextual novelty, routing diversity, recurrence, explanatory compression, coherence relevance, and computational boundedness. They are ordinals from 0 to 5. They are not summed.

## Y. Coherence-map update

The ledger is `constraint-lab/coherence/findings.jsonl` and `constraint-lab/coherence/relations.jsonl`. The generated views are `current-map.md` and `current-map.mmd`. The snapshot is `constraint-lab/coherence/snapshots/through-generation-008c.md`. Its sha256 is `d0e73fd314ad91682e66026de02ea4f2253a05d62e581b3f9270f9809935abf0`. The canonical ledger sha256 recorded inside the snapshot is `b0800de29262c13ba7f4af8ce60790b5912698401e39f7ec10dcbcd628f87cb3`.

New findings: `F8C-TWO-COORDINATES`, `F8C-CLOSED-FORM-CMI`, `F8C-GRADE-ASYMMETRY`, `F8C-LOCAL-EQUIVALENCE`, `F8C-R05-DENOMINATOR`, `F8C-TOPOLOGY-ATLAS`, `F8C-PATH-CONVERTS-SLOT`, `F8C-CHECKPOINT-EPOCH`, `F8C-GATE-REFRESH`, `F8C-CURRENT-SURVIVES`, `F8C-PROJECTION-GEOMETRY`, `F8C-EDGE-DRIFT`, `F8C-DRIFT-DIRECTION`, and the method notes `F8C-METHOD-GEOMETRY` and `F8C-METHOD-DIMENSIONS`.

Qualified, with statements left as published: `Q-LOCAL-SLOT`, `Q-PATH-SHAPE`, and `Q-CLASS-REMAINDER`. Each is linked by `partially_answered_by` to the finding that answers the part C0 derived.

No interpretation node was deleted. `F008A-PLUGIN-INITIAL-MI` remains a historical observation. Generation 8B's supersession of its interpretation stands.

New open questions: `Q-WEAK-GRADE` and `Q-GATE-COMPOSITION`. `Q-H-POSITIVE`, `Q-SCALE-N`, and `Q-THREE-EDGE-LAYER` stay unresolved. The drift finding qualifies `F010-OCCUPANCY-AXIS` on the sign and leaves the 3-edge layer open.

The new mechanism edges run from the closed form to the Generation 8B slot information, from the path atlas to the checkpoint-1 shape split, from the gate refresh to the transient class memory, from the projection geometry to the class-loss fractions, and from the drift sign to the occupancy axis. The current-survives inference refines `F018-LOCAL-VERSUS-INITIAL`.
