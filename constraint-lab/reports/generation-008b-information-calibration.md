# Generation 008B — information calibration

Generation 8B is Mode B. It calibrates the information statistics of the Generation 8A trajectories. It does not replace the context-repair atlas, and it does not run a new stochastic census. Pass and fail in this note are reserved for tests, replay, chronology, and numerical tolerances.

The numerical record is `constraint-lab/reports/generation-008b-round-b0-tables.json`. Schema `rs-constraint-lab.information-calibration-tables/v1`. File sha256 `d7bc06d027eabb62f5f2e5bed312c746ef3f062198a25a35bd5246ce23590e09`. Payload sha256 `b2ecdac74e38b3d53160a43b3319bcb4cc607cab4817c5cb2cfdaa68f4171adf`. The result commit is `dc9f9b9eb6e4a36b4513d10b49e937c43b57b371`. Every table row is labelled by layer: A is the plug-in, B is the permutation calibration, C is the deterministic kernel result. Float64 kernel quantities are deterministic kernel results. Mutual information is in nats. Negative values of plug-in minus null mean are stored as computed.

## A. External Review 008A

Review 008A is `constraint-lab/provenance/reviews/008A-chatgpt-review-v0.8a.md`. It reads branch `research/constraint-lab-v0.8a-context-repair` at `b7b5d848d90b7d1824bcce9740c2faf966cbea54`. The review inspected branch chronology, Round A0 frozen-plan ancestry, the rule-aware symmetry implementation, raw-context execution, trajectory and replay execution, the Round A0 report and synthesis, the mutual-information implementation, the current-context event counters, the CI history, and the final-head run.

The operational record it accepts is 6,144 primary trajectories, 6,759 durable items, 58 batches, 2 workers, 615 of 615 durable replay checks exact, 5,314,418 full events, 3,145,728 pair events, 3,145,728 transition markers, 0 timeouts, 0 retries, 0 quarantines, and every episode at `pair_horizon`. Disk after merge is 678,150,248 bytes. Batch wall times are median 17.716 s, p90 18.063 s, maximum 19.428 s. The A0 frozen plan is `61ed53075238284850e792aff5743f0a8a7b6695`. The atlas result is `4897d9e02b2942670bafc52bc966ef6709167b64`, and it descends from that plan. Final-head Actions run `38312376920` is on `b7b5d848d90b7d1824bcce9740c2faf966cbea54`. The earlier red runs were a shallow checkout. Commit `bf821c771e4ed86e24688ed44ab6035b7e9af785` set full history on the constraint-lab job. The suite after that fix reported 167 passed.

Prompt 008A authored metadata, recorded beside the agent input and not assigned to it: 33,117 bytes, sha256 `0417394f876ad063a48759ef419102b4fde4730f710e228ebba9703209c6b3f6`. The stored agent input is 33,115 bytes, sha256 `1c44d30b086e2e02ace4d0777605267d8f7139c71948beffe058b5c976d25010`. The authored file is not in this working environment. Status `externally_verified_pending_import`. Relationship `unknown`.

## B. Why plug-in mutual information required calibration

Generation 8A computed ordinary plug-in mutual information and conditional mutual information from finite contingency tables. That estimator is the standard functional of the empirical table. The Generation 8A implementation has no finite-sample bias correction, no permutation reference, and no replacement by the transition kernel.

The laboratory has a 1024-state chain and an explicit transition law, so those three layers can be separated. Layer A is the Generation 8A plug-in. Layer B compares it with a deterministic permutation null. Layer C evaluates the same estimand from the kernel. A non-zero plug-in value is a statement about the estimator until a zero-information control or a kernel quantity says otherwise.

The leading independence-bias scale for 16 contexts, 2 destinations, and 256 episodes is `((16-1)*(2-1))/(2*256) = 0.029297` nats. That figure is a sanity check. The primary correction is the permutation null and the kernel value.

## C. Structural zero-information controls

R00, R03, and R07 are calibration instruments supplied by the rule semantics. They are references for the estimator. The programme is not organised as a hypothesis test.

`Constraint.matches` reads the action bit, each condition bit, and, when a count literal is present, the popcount of the full state. The A0 palette has no count literals. R00 has no rules, so every slot weight is 1. R03 is `dissolve(0-1) => strong_suppress`. R07 is `dissolve(0-1) => strong_favour`. In both, the only modified weight is pair slot 0, and it is modified only when pair bit 0 is set. No action, condition, or count reads a triad slot. For a fixed pair mask the six pair-slot weights are therefore the same at all 16 triads. The measured triad weight span on these three systems is 0.

Between pair events only triad bits toggle. On these three systems that excursion leaves the weight vector unchanged. The pair slot that ends the excursion, and the pair mask it writes, are independent of the current triad once the current pair mask is known. By induction the whole pair-mask trajectory is independent of the initial triad. Every functional of that trajectory is independent of the initial triad: the first other 3-edge destination, the graph class at a checkpoint, the edge count, the class given the edge count, the labelled pair mask, and the expected class occupancy. Under a uniform raw-triad prior the exact mutual information of each of those observables with the initial triad is zero.

The same weight identity gives the current-context statement. The local law `P(next pair slot | full pair mask, current triad)` equals `P(next pair slot | full pair mask)`. Conditional mutual information of the triad with the next pair slot, given the full pair mask, is zero under the balanced weighting, under the A0 empirical state weighting with the exact slot law, and under the stationary pair-event weighting. Conditioning only on the isomorphism class is a different estimand. Different masks in one class can carry different slot laws, and a finite sample can put different mask weights on different triads inside that class.

The runtime classification matches this reading. R00, R03, and R07 are the structural zero controls. R01, R02, R04, R05, and R06 each name triad slot 6 in a condition. Their triad weight spans are 0.75, except R06, whose strong-favour grade has span 3.0.

## D. Frozen B0 analysis plan

The frozen analysis plan is commit `466d54339738d315ed621ea4256a239cb026498a`, plan hash `279857bb2ee82eefd430ba56c9fa3758238ebea9e0b652c01b56b97dbc1bf618`, file `constraint-lab/exploration/generation-008b/round-b0-plan.json`. It was pushed before any B0 quantity was computed. Actions run `38319517214` succeeded on that commit. The result commit descends from it. Journey step 1 still has `result_commit` null. Journey step 2 names `dc9f9b9eb6e4a36b4513d10b49e937c43b57b371`.

B0 is the only round. The palette is the Generation 8A repair palette, R00 through R07. No new scientific episodes. Permutation counts were frozen at 10,000 for each initial-context cell and 2,000 for each current-context cell. Seeds are `sha256-u64-v1` of the experiment id, the estimand id, the system, the source graph, and the permutation index. The zero-information floor is `1e-10`. Kernel row tolerance `1e-9`. Stationary and hitting residuals `1e-8`. Cross-solver tolerance `1e-8`. Plug-in reproduction tolerance `1e-9`. Chain-rule tolerance `1e-9`. Unabsorbed-mass tolerance `1e-8`.

Each command is one system, or one system and source. Two workers. Watchdog 120 seconds. The commands that ran were `exact`, `permute-initial`, and `permute-current`. Exact kernels are built once per system and reused. A horizon-matched destination mutual information is omitted when the unabsorbed mass at epoch 512 is below `1e-8`. The validation table stores that mass. The largest mass in B0 is `2.460e-22`, on R05. The episode-block bootstrap was left unused.

The first `exact` command for R03 stopped because an empirical class-conditional value on a zero-information control was above the floor. That value is an occupancy correlation inside a graph class. Commit `7eb6392` keeps the floor on the full-mask identity, which is the identity the semantics give. R03 was rerun. The frozen estimands did not change. The published tables include that rerun.

## E. Plug-in reproduction

The committed Generation 8A cells were recomputed from the committed counts with the same mutual-information functions. The comparison covers 336 cells: 24 first-destination cells, 240 checkpoint class cells, and 72 current-context cells. The maximum absolute gap is `2.810e-16`, inside the tolerance `1e-9`. Contingency order does not enter the functional. The unit remains nats.

The Generation 8A plug-in figures below are therefore the same numbers as the published A0 tables. Calibration starts from that reproduction.

## F. Permutation calibration

Initial-context permutations shuffle the 16 raw-triad labels inside each system and source. Episode outcomes stay put. Each label keeps 16 episodes. Current-context permutations shuffle the triad inside each conditioner stratum and preserve the outcome and conditioner marginals. Pair events inside an episode are serially correlated. The current-context null is a finite-table bias calibration. Its percentile is not a trajectory uncertainty and it is not a causal significance statement. No p-value is published. Plug-in minus null mean is stored with its sign.

### First destination

The permutation-null mean on all 24 cells lies between 0.03024 and 0.03127 nats. The Miller-Madow full-alphabet term is 0.029297 nats on every cell. The plug-in values sit on that bias scale.

| System | Source | Plug-in | Null mean | Excess | Null percentile | Exact |
| --- | --- | --- | --- | --- | --- | --- |
| R00 | star | 0.03206 | 0.03070 | +0.00136 | 59.6 | floor |
| R00 | path | 0.03071 | 0.03052 | +0.00019 | 55.8 | floor |
| R00 | triangle | 0.04342 | 0.03093 | +0.01249 | 86.8 | floor |
| R01 | star | 0.02912 | 0.03063 | −0.00151 | 49.8 | 5.699e-7 |
| R01 | path | 0.03102 | 0.03040 | +0.00063 | 56.4 | floor |
| R01 | triangle | 0.02468 | 0.03058 | −0.00591 | 33.2 | 5.699e-7 |
| R02 | star | 0.02121 | 0.03075 | −0.00954 | 20.4 | 3.307e-7 |
| R02 | path | 0.02614 | 0.03039 | −0.00425 | 38.8 | floor |
| R02 | triangle | 0.03523 | 0.03064 | +0.00460 | 69.8 | 3.307e-7 |
| R03 | star | 0.07021 | 0.03102 | +0.03919 | 99.6 | floor |
| R03 | path | 0.02324 | 0.03039 | −0.00715 | 27.9 | floor |
| R03 | triangle | 0.02827 | 0.03069 | −0.00241 | 45.9 | floor |
| R04 | star | 0.02087 | 0.03127 | −0.01040 | 18.6 | 3.307e-7 |
| R04 | path | 0.03261 | 0.03049 | +0.00212 | 61.9 | floor |
| R04 | triangle | 0.03169 | 0.03106 | +0.00063 | 57.5 | 3.307e-7 |
| R05 | star | 0.02774 | 0.03122 | −0.00347 | 43.0 | 2.025e-5 |
| R05 | path | 0.02884 | 0.03036 | −0.00152 | 49.9 | floor |
| R05 | triangle | 0.05674 | 0.03121 | +0.02553 | 97.2 | 2.025e-5 |
| R06 | star | 0.02750 | 0.03062 | −0.00312 | 43.5 | 1.906e-7 |
| R06 | path | 0.04674 | 0.03037 | +0.01637 | 91.0 | floor |
| R06 | triangle | 0.03078 | 0.03089 | −0.00011 | 54.8 | 1.906e-7 |
| R07 | star | 0.03819 | 0.03060 | +0.00759 | 77.5 | floor |
| R07 | path | 0.03249 | 0.03024 | +0.00225 | 61.6 | floor |
| R07 | triangle | 0.01273 | 0.03113 | −0.01841 | 2.7 | floor |

"Floor" means the absolute exact-kernel value is below `1e-10`. The signed kernel values on those cells have magnitude at most about `2e-16`. R03 star is the largest plug-in cell, 0.07021 nats. Its null 95th percentile is 0.0525 and its null 99th is 0.0642. The cell is in the far tail of its own null, and its exact-kernel value is at the floor. R07 triangle is the low tail of the same family of controls: plug-in 0.01273, excess −0.01841, percentile 2.7, exact value at the floor. The controls track the bias, including both tails.

### Checkpoints

From checkpoint 2 through 512 the median plug-in class mutual information of the 24 system/source cells lies between 0.1209 and 0.1398 nats. The median permutation-null mean on those same cells lies between 0.1315 and 0.1328 nats. The full-alphabet Miller-Madow term is 0.29297 nats, which counts 11 classes. The realised support is smaller, and the permutation null is the calibration that matches the plug-in. Excess at checkpoint 512 runs in both directions. R00 path is 0.1243 against a null mean of 0.1320. R01 star is 0.1798 against 0.1332. Both exact-kernel values at that checkpoint are at the floor.

At checkpoint 1 the null mean is about 0.030 on star and triangle and about 0.097 on path, because one pair toggle from a 3-edge source reaches a smaller set of classes, and the path source reaches more than one class at the neighbouring edge counts.

### Current context

For `I(current triad; next pair slot | full pair mask)` the permutation-null mean is 0.01850 to 0.01868 nats on every system and source. The plug-in on R00, R03, and R07 is 0.01782 to 0.01919. Excess on those controls is a few ten-thousandths of a nat, positive and negative. R07 star is percentile 1.7. R00 star is percentile 96.5. The plug-in on the five triad-conditioned systems is 0.02939 to 0.03624. Every one of those 15 cells sits at the top of its 2,000-draw null. The largest plug-in is R06 star, 0.03624, against a null mean of 0.01855.

The class-conditional plug-in nulls are smaller, because the conditioner is coarser: about 0.00316 nats for the next slot, and about 0.00097 nats for the next class. Those floors are the right comparison for the Generation 8A class-conditional plug-in figures.

## G. Exact first-destination information

The route definition is unchanged. The source 3-edge class is transient. The other two 3-edge classes compete. Return to the source is allowed. The quantity is the eventual hitting distribution. The two destination probabilities sum to 1. The largest gap in that sum, on R00, is `3.33e-15`. Unabsorbed mass at epoch 512 is at most `2.460e-22`.

Under the uniform raw-triad prior the exact-kernel mutual information is at the floor for R00, R03, and R07 on every source. It is at the floor on the path source for every system, including the triad-conditioned ones. On star and triangle it is non-zero for the triad-conditioned systems, and the star value agrees with the triangle value to about `1e-16`.

The largest exact value is R05, `2.025e-5` nats, on star and on triangle. R01 is `5.699e-7`. R02 and R04 are `3.307e-7`. R06 is `1.906e-7`. Each of these is above the floor `1e-10` and small relative to the plug-in, which is about 0.02 to 0.07, and small relative to the permutation-null mean, which is about 0.031.

The Generation 8A maximum, R03 star at 0.0702 nats, is one of the cells whose exact value is at the floor. R05 triangle, plug-in 0.0567 and null percentile 97.2, has exact value `2.025e-5`. The plug-in excess there is 0.0255. The kernel value is three orders of magnitude smaller.

Sampling frequencies from the A0 episodes sit at the scale expected from 16 replicates. Pooled L1 distances from the exact destination law run up to about 0.125. That comparison is a compatibility check at the sampling scale. The information result is the kernel value.

## H. Exact checkpoint information

The pair-class distribution at checkpoints 1, 2, 4, 8, 16, 32, 64, 128, 256, and 512 is the epoch-0 start propagated by the pair-event kernel. Sampled trajectories are not the source of these distributions.

On R00, R03, and R07 the exact class mutual information, the edge-count mutual information, the class-given-edge mutual information, and the labelled pair-mask mutual information are at the floor at every sampled checkpoint. Magnitudes are at most a few `1e-16`, and the stored signs include both.

On the triad-conditioned systems the exact class information is largest at checkpoint 1 or 2 and is at the floor from checkpoint 64 through 512. Nothing in the exact class curve persists to checkpoint 512. The plug-in median near 0.12 nats through checkpoint 512 sits on the permutation-null median near 0.132. Persistence of the plug-in number is the bias of the estimator.

The largest exact class value in the grid is R06 path at checkpoint 1, 0.02798 nats. R06 star and triangle at checkpoint 1 are 0.008801 nats. R01 path at checkpoint 1 is 0.01023 nats. R01 star and triangle peak at checkpoint 2, at 0.002113 nats. R02 and R04 peak at 0.0001206 nats on star and triangle at checkpoint 2, and their curves agree with each other to `1.2e-16`. R05 peaks at 0.0001640 nats on star and triangle at checkpoint 4. By checkpoint 32 the largest exact class value among the conditioned systems is `1.29e-9`, on R01. By checkpoint 64 every exact class value is at the floor.

Star and triangle agree with each other to about `1e-16` at every system and checkpoint. The labelled pair-mask mutual information agrees across all three sources to about `1e-16`. It is larger than the class information at the early checkpoints: 0.02798 on R06 and 0.01023 on R01 at checkpoint 1, and 0.02986 on R06 at checkpoint 2. It is at the floor by checkpoint 64 as well.

## I. Edge-count versus shape decomposition

Edge count is a function of graph class, so the chain rule `I(T0; C) = I(T0; E) + I(T0; C | E)` is an identity of the joint distribution. The numerical gap is at most `5.94e-16`.

At checkpoint 1 on star and triangle, the exact class information equals the exact edge-count information, and the shape term is 0. One pair toggle changes the edge count by exactly one, and from those sources that determines the class. At checkpoint 1 on path the shape term is present. For R06 path it is 0.01918 of the 0.02798 class nats, and the edge term is 0.008801. For R01 path it is 0.008838 of the 0.01023 class nats, and the edge term is 0.001393. The edge term itself agrees between path and star to about `1e-16`. The extra path information is shape given edge count.

At checkpoint 2 the shape term is a real piece of the remaining class information. On star and triangle it is the larger piece for R02, R04, and R05: R02 and R04 have edge 0.0000177 and shape 0.000103; R05 has edge 0.0000287 and shape 0.000131. R01 and R06 at checkpoint 2 are still mostly edge count, with a shape piece of 0.000121 on R01 and 0.000269 on R06.

The labelled mask decomposes the same way: mask information equals class information plus mask-given-class. At the early checkpoints the mask term is the larger one. The additional information is the labelled alignment inside a class. By checkpoint 64 the mask term is at the floor with the class term.

The deferred Generation 8A question, whether a persistent 0.12 nats is edge count or residual shape, has this answer in the kernel. There is no persistent 0.12 nats. The early exact information is both coordinates, in proportions that depend on the checkpoint and the source, and both coordinates have decayed below the floor by checkpoint 64.

## J. Exact finite-horizon occupancy

Expected occupancy is the mean of the class distribution over pair epochs 1 through 512 inclusive. Epoch 0, the initial source, is excluded. Generation 8A occupancy included the initial epoch. The context range is the maximum minus the minimum across the 16 raw triads.

On R00, R03, and R07 the exact dense-minus-sparse range is at most `5.6e-16`, and the 11-class L1 range is at most `1.8e-15`. The exact context range on the controls is at the floor.

On the triad-conditioned systems the dense-minus-sparse range is non-zero and small beside the Generation 8A raw spans of about 0.06 to 0.09:

| System | Dense minus sparse | Sparse share | 3-edge share | Dense share | Class L1, star and triangle | Class L1, path |
| --- | --- | --- | --- | --- | --- | --- |
| R01 | 0.001423 | 0.000720 | 0.000017 | 0.000703 | 0.001476 | 0.001626 |
| R02 | 0.000395 | 0.000205 | 0.000015 | 0.000190 | 0.000441 | 0.000410 |
| R04 | 0.000395 | 0.000190 | 0.000015 | 0.000205 | 0.000441 | 0.000410 |
| R05 | 0.000347 | 0.000146 | 0.000054 | 0.000201 | 0.000546 | 0.000487 |
| R06 | 0.001925 | 0.000974 | 0.000024 | 0.000950 | 0.002000 | 0.002345 |

R06 is the largest. The per-triad dense-minus-sparse values agree across star, path, and triangle to about `1e-15`. The scalar edge-count range is source-invariant at that precision. The 11-class L1 range is larger on path for R01 and R06, and larger on star and triangle for R02, R04, and R05. R02 and R04 exchange the sparse-share range and the dense-share range and otherwise agree. Their per-triad dense-minus-sparse vectors are not negations of each other.

Checkpoint 512 itself carries no exact initial-triad information. The occupancy range is the average of a transient difference over 512 epochs. It is a finite-horizon integral. It is a genuine context dependence of the path average, and it is about 0.002 at its largest.

## K. Current-context exact transition-law information

The estimand is the one Generation 8A counted: the triad in the pre-pair-event state, and the pair slot of the next pair event. Triad-event slots are outside the outcome. At each full state the exact conditional slot law is the six pair propensities renormalised among themselves. That is the local law of the pair-event records. For a triad-conditioned rule it differs from the epoch-kernel next-slot law, because triad flips during the excursion can change the weights before the pair event.

Three weightings stay separate.

Balanced-law weighting gives every pair-mask and triad state equal weight before the exact slot law is applied. It is one number per system. It asks whether the rule itself makes the next slot depend on the triad once the mask is fixed.

A0 empirical-source weighting uses the visited pre-pair-event states in the Generation 8A streams, 131,072 pair events per system and source, and replaces the sampled slot with the exact slot distribution at that state. It asks what the finite atlas experienced, with the next-event sampling noise removed.

Stationary pair-event weighting uses the stationary distribution of the full-event chain. The joint weight of a state and a pair slot is stationary mass times the full-event probability of that pair slot. It asks what the long-run pair-event clock experiences.

Full pair mask, next pair slot, exact-kernel conditional mutual information:

| System | Balanced | A0 empirical, three sources | Stationary |
| --- | --- | --- | --- |
| R00 | floor | floor | floor |
| R01 | 0.009749 | 0.012064 to 0.012180 | 0.012025 |
| R02 | 0.009749 | 0.011894 to 0.011974 | 0.012025 |
| R03 | floor | floor | floor |
| R04 | 0.009749 | 0.011882 to 0.011950 | 0.012025 |
| R05 | 0.010413 | 0.012953 to 0.013164 | 0.013240 |
| R06 | 0.023368 | 0.016842 to 0.017076 | 0.016895 |
| R07 | floor | floor | floor |

R00, R03, and R07 are at the floor on all three weightings. The signed balanced values have magnitude about `1e-15`. The identity holds. R01, R02, and R04 agree with one another through about `1e-15` on the balanced value and on the stationary value.

R06 is the largest balanced value, 0.02337 nats, and its stationary and empirical values are smaller, about 0.0169. The long-run occupancy experiences less of that rule's intrinsic dependence than the balanced weighting measures. R01, R02, R04, and R05 go the other way by a smaller amount: the stationary value is a little above the balanced value, and the A0 empirical exact-law value sits on the stationary value.

The plug-in excess over the permutation null tracks these exact-law values. R06 star has plug-in 0.03624, null mean 0.01855, excess 0.01769, and exact empirical-source value 0.01691. The Generation 8A interval of about 0.030 to 0.036 nats is the exact-law value plus a bias of about 0.0185 nats. Subtracting 0.018 by hand is not the calculation. The kernel value is.

## L. Balanced versus empirical versus stationary weighting

The three numbers answer three questions.

The balanced value is law dependence. Once the labelled pair mask is fixed, the next pair-slot distribution depends on the current triad exactly on the five systems whose rule names a triad, and it is independent of the triad on R00, R03, and R07.

The stationary value is the same law, weighted by the pair events the chain produces in the long run. For the strong-suppress conditionals it is about 0.012 to 0.013 nats. For the strong-favour conditional it is 0.0169 nats, below that rule's balanced value of 0.0234.

The A0 empirical-source value is the finite 512-epoch atlas with the exact slot law. On every triad-conditioned system it agrees with the stationary value to about 0.001 nats or closer. The exploratory trajectories already sat on the long-run state weighting for this local estimand. The gap between the plug-in and this value is the finite-table bias, whose null mean is about 0.0185 nats.

## M. Full pair mask versus graph class

The full-mask quantity stays primary. The class-conditional exact-law quantities are the continuity comparison with Generation 8A.

Stationary pair-event weighting, exact-kernel conditional mutual information:

| System | Slot given full mask | Slot given class | Fraction retained | Next class given class |
| --- | --- | --- | --- | --- |
| R00 | floor | floor |  | floor |
| R01 | 0.012025 | 0.007946 | 0.661 | 0.000972 |
| R02 | 0.012025 | 0.007946 | 0.661 | 0.000972 |
| R03 | floor | floor |  | floor |
| R04 | 0.012025 | 0.007946 | 0.661 | 0.000972 |
| R05 | 0.013240 | 0.009400 | 0.710 | 0.002571 |
| R06 | 0.016895 | 0.007492 | 0.443 | 0.001196 |
| R07 | floor | floor |  | floor |

Collapsing the labelled mask to the 11-class label keeps about two thirds of the stationary slot information for R01, R02, R04, and R05, and keeps 0.443 of it for R06. The discarded fraction is labelled alignment. The next graph class, given the current class, carries still less: at most 0.00257 nats, on R05.

On the zero-information controls the stationary class-conditional values are at the floor. The pair-mask chain does not depend on the triad, so the long-run mix of masks inside a class does not either. The A0 empirical-source class-conditional values are different. R00 remains at the floor, because every slot weight is 1. R03 and R07 are about `1e-5` to `5e-5`: R03 star next-class-given-class is `1.372e-5`, and R07 path next-slot-given-class is `4.921e-5`. The slot law of an unconditional dissolve depends on whether pair bit 0 is set. A finite atlas can correlate the triad with which masks inside a class were visited. That residual is an occupancy correlation in the sample. It is above the floor, it is far below the 0.018 plug-in, and it is not a failure of the full-mask identity.

The Generation 8A plug-in comparison, about 0.003 nats given the class and about 0.018 nats given the mask on the controls, compares two bias floors. The exact law on the controls is at the floor for the full mask under every weighting, and at the floor for the class under the stationary weighting. On the triad-conditioned systems the exact class-conditional slot information is about 0.0075 to 0.0094 nats. The plug-in of about 0.010 to 0.013 sits above its own null mean of about 0.00316 by that same amount.

## N. Numerical validation

The published validation rows, one per system:

Kernel row error is between `1.1e-16` and `4.4e-16`. Stationary residual is between `1.5e-16` and `1.1e-15`, inside the `1e-8` threshold of the float64 solver. Arithmetic is float64. Every system reports period 2, and the stationary distribution is still unique under that period when the chain is irreducible. Hitting residual is between `7.8e-16` and `1.7e-15`. Dense and block epoch kernels agree to between `1.4e-17` and `1.1e-16`. Rule-aware symmetry gaps on the destination laws are at most `1.6e-15`. Destination probabilities sum to 1 within `3.3e-15`. Chain-rule gaps are at most `5.9e-16`. Unabsorbed mass at epoch 512 is at most `2.460e-22`.

The zero-information identity maximum, taken over the exact initial-context functionals and the three full-mask current-context weightings, is `3.3e-16` on R00, `1.8e-15` on R03, and `3.2e-16` on R07. All are inside the predeclared floor `1e-10`. Deadlock is absent. Triad weight span is 0 on the controls, 0.75 on R01, R02, R04, and R05, and 3.0 on R06. The span of the next pair-mask law across triads is at the floor on the controls, 0.175 on R01, R02, and R04, 0.191 on R05, and 0.435 on R06. Those spans are diagnostics of the kernel. The information figures are the mutual informations above.

Plug-in reproduction: 336 cells, maximum absolute gap `2.810e-16`.

## O. What Generation 8A information claims change

The Generation 8A report and synthesis are unchanged. The following sentences in `constraint-lab/reports/generation-008a-context-repair-synthesis.md` are plug-in observations. The kernel reading replaces them as descriptions of the transition law.

"Uniform-raw mutual information is at most 0.0702 nats." The plug-in maximum remains 0.0702 nats, on R03 star, and that cell reproduces. The exact-kernel maximum on the same estimand is `2.025e-5` nats, on R05 star and R05 triangle. The 0.0702 cell is a structural zero.

"Under the uniform raw prior, information about the first other 3-edge destination is 0.0127 to 0.0702 nats. It locks by checkpoint 32 to 64." That interval is the plug-in interval. It matches the permutation null, whose mean is about 0.031 and whose tails reach about 0.013 and about 0.070. The exact-kernel values are at the floor on the controls and on every path cell, and at most `2.025e-5` elsewhere. Unabsorbed mass at epoch 512 is below `1e-21`, so the horizon hitting distribution and the eventual hitting distribution agree at the scale of this information. There is no exact destination information of size 0.07 waiting to lock.

"From checkpoint 2 through 512 its median stays between 0.1228 and 0.1415 nats. Initial context is not forgotten on that coordinate." The recomputed plug-in median of the 24 cells stays near 0.12 to 0.14 nats, beside a permutation-null median near 0.132. The exact class mutual information is at the floor on the controls at every checkpoint, and on the conditioned systems it is at the floor from checkpoint 64 through 512. Initial context is forgotten on that coordinate by checkpoint 64. The early exact information, at most 0.02798 nats, is transient.

"I(current triad; next pair slot | full labelled pair mask) is about 0.018 nats on baseline and on the unconditional dissolves, and about 0.030 to 0.036 nats on the five systems whose rule names a triad." Both plug-in bands reproduce. The exact-kernel value on the controls is at the floor under all three weightings, and the 0.018 band is the permutation-null mean. The exact-kernel value on the conditioned systems is 0.00975 to 0.02337 nats under balanced weighting and 0.0119 to 0.0171 nats under the A0 state weighting. The higher plug-in band is that law dependence plus the same bias.

"The class projection drops a real, still small, dependence." The plug-in comparison mixed a 0.018 mask floor with a 0.003 class floor. The exact stationary law keeps a substantial fraction of a small dependence, 0.44 to 0.71 of the full-mask slot information, and discards the labelled remainder. On the controls the stationary class-conditional value is at the floor.

"Generation 8's sentence that maximum context information is about 0.06 nats remains a fair description of first-destination information under a uniform raw prior, where the maximum is 0.0702." That sentence describes the plug-in. The exact-kernel first-destination information on this palette is at most `2.025e-5` nats.

The short list in the Generation 8A observations names "a persistent checkpoint pair-class information near 0.12 nats" and "mask-conditional current-triad information about 0.018 or about 0.03." The first of those is the plug-in bias. The second splits into a bias of about 0.0185 and an exact-law value of about 0.010 to 0.023 on the rules that name a triad.

The open question, whether the persistent 0.12 nats is the edge-count coordinate or a residual class distinction, is answered by the decomposition in section I. The 0.12 nats is the bias. The early exact information is both coordinates, and it has left both by checkpoint 64.

The inference that the raw sample makes visible "a modest persistent occupancy difference" describes the 16-replicate spans of about 0.06 to 0.09. The exact context range of expected occupancy is at the floor on the controls and at most 0.00192 on R06. The state at checkpoint 512 does not carry the initial triad. The path average still differs by that small amount because the early epochs differed.

## P. What survives

The context repair stands. All 16 raw triads were executed for each source and system. The analysis group is `Aut(source graph, constraint system)`. Eighty-six graph-only orbits split on this palette once the labelled rules are required to stay invariant. Rule-aware symmetry was calculated after the starts were defined.

The edge-count axis stands. Generation 8A dense minus sparse remains R05 +0.2378, R03 +0.1728, R01 +0.0723, R04 +0.0691, R00 +0.0033, R02 −0.0711, R06 −0.0854, R07 −0.1448. The 3-edge layer remains near 0.314, and 0.3072 on R05. Visible routing remains the same skeleton: path splits toward star and triangle, and star and triangle route mostly through path. The composite residual on the 11-class occupancy vector remains L1 0.0640, and the same residual on dense minus sparse remains about −0.0008. These are facts about the trajectories that were run. This round does not recompute them and does not replace them.

What also survives calibration, as exact-kernel structure, is local. Where a rule names the triad, the current triad carries exact predictive information about the next pair slot given the full pair mask. The balanced values are 0.00975 to 0.02337 nats. A transient initial-context effect of at most 0.02798 nats is present in the first pair events, and a finite-horizon occupancy range of at most 0.00192 remains after averaging 512 epochs. Both are small beside the grade-driven dense-minus-sparse shifts.

## Q. Observations

The observations are the layer labels and the numbers in the Round B0 tables. The short list is:

The 336 Generation 8A plug-in cells reproduce, with maximum absolute gap `2.810e-16`.

First-destination plug-in values lie around a permutation-null mean of about 0.031 nats. The exact-kernel value is at the floor for R00, R03, and R07, at the floor for every path cell, and at most `2.025e-5` nats on R05 star and R05 triangle.

Checkpoint plug-in class information from epoch 2 onward has median about 0.12 to 0.14 nats, beside a null median of about 0.132. Exact class information is at most 0.02798 nats, at R06 path, checkpoint 1, and is at the floor from checkpoint 64 through 512.

At checkpoint 1 on star and triangle the exact class information is entirely edge count. At checkpoint 1 on path, for R01 and R06, most of it is shape given edge count. The labelled mask carries more than the class at the early checkpoints, and it decays on the same schedule.

Exact dense-minus-sparse context range over epochs 1..512 is at the floor for R00, R03, and R07, and is 0.000347 to 0.001925 for the triad-conditioned systems. The per-triad edge-count values agree across the three sources to about `1e-15`.

Exact full-mask slot information is at the floor for R00, R03, and R07 under balanced, empirical-source, and stationary weightings. On the triad-conditioned systems the balanced values are 0.009749 to 0.023368, and the stationary values are 0.012025 to 0.016895. The A0 empirical exact-law values sit on the stationary values. The plug-in null mean is about 0.0185.

Class conditioning retains 0.44 to 0.71 of the stationary slot information. Stationary class-conditional information on the controls is at the floor. The finite-atlas class-conditional exact-law value on R03 and R07 is about `1e-5` to `5e-5`.

R02 and R04 agree on the exact checkpoint curve to `1.2e-16`. Star and triangle agree on exact class information to about `1e-16`.

Zero-information identities and solver residuals are inside the floors frozen in the plan.

## R. Inferences

The small Generation 8A first-destination plug-in, including the largest cell, is the finite-sample bias of that estimator. A genuine initial-context routing dependence remains on star and triangle for the rules that name a triad. Its size is `1.9e-7` to `2.0e-5` nats. That is above the numerical floor and small relative to the plug-in and to the null mean.

The apparent persistence of about 0.12 nats of checkpoint class information is the same kind of bias, on a larger table. Genuine initial-context information in the class is transient. It is gone, to the floor, by checkpoint 64. While it is present it occupies both the edge-count coordinate and the shape coordinate, and the split depends on the source and the checkpoint. The labelled mask carries a further early component, and that component decays with the class component.

The exact occupancy range is a small integral of that transient difference. It replaces the raw 16-replicate spans of about 0.06 to 0.09 as the description of context dependence in the 512-epoch average. It does not restore a claim that the state at epoch 512 remembers the initial triad.

The current triad changes the next pair-slot law, given the full pair mask, on the rules that name the triad, and on those rules only. The dependence is about 0.010 to 0.023 nats of a six-way slot. The long-run pair-event clock and the finite A0 atlas experience nearly the same amount. The balanced weighting is higher than the stationary weighting for the strong-favour rule and slightly lower for the strong-suppress rules. Class projection keeps a large fraction of this small dependence and discards a labelled remainder, a larger remainder for R06 than for the suppress rules.

The estimator was the observation apparatus. On every structural zero it reported a stable positive number, and that number matched its permutation null. The kernel value on those controls is at the floor.

## S. RS / global-coherence interpretation

These are statements about one finite relational grammar, with N=4 and O=3.

In this grammar, a higher-order relational variable carries exact predictive information about a lower-order event law when the rule explicitly conditions on that higher-order relation. The information is local, it is a few hundredths of a nat, and it is absent from the three systems whose pair-event rule does not read the triad. The exploratory trajectories also looked as though the initial triad was remembered for hundreds of pair events. The exact transition analysis shows that the persistent plug-in figure was sampling bias, and that the genuine initial-context effect is transient and small.

The grade of a pair rule still moves the edge-count coordinate by tenths of a share. The calibrated triad effect does not reorganise that axis, the route skeleton, or the composite residual.

This is not a claim that physical reality implements the grammar. A local dependence of this size does not establish a higher-order ontology, and it does not identify a designer or an ultimate receiver. The collapse of the persistent plug-in figure is informative in the same register: the finite sample produced a stable-looking number, and the known transition law accounts for that number as bias. Both readings stay inside the grammar that was explored. Exact calculation does not turn the question into a test of the programme. The question remains what structure the explored dynamics contain.

## T. Next exploration options

No option is chosen. No further round is opened. A new stochastic census is not required in order to see the quantities B0 computed. The kernel already returns them. The candidates, with unsummed attention vectors, are in journey step 2.

The live candidates are mechanism readings of the kernel: which masks and which triad bits move which slots, especially under R06, where the balanced value is largest; why the path source at checkpoint 1 carries shape information that star and triangle do not; which early epochs accumulate the 512-epoch occupancy range of about 0.002; and which labelled alignments the isomorphism class discards, the discard being largest in fraction on R06. A paired random-number resample of an effect the kernel already gives, a return to a Mode A discriminator, and an expansion past N=4 and O=3 are on the list with lower attention. The split between rules that name a triad and rules that do not is already visible in the semantics and in the kernel values.
