# Generation 008A — context-repair synthesis

Generation 8A is Mode B. It repaired the hidden-context execution basis and ran one round, A0. Rounds A1 and A2 were not opened. Pass and fail in this note are reserved for tests, replay, and verification.

The numerical record is `constraint-lab/reports/generation-008a-round-a0-context-repair.md` and `constraint-lab/reports/generation-008a-round-a0-tables.json`. The frozen plan is `61ed53075238284850e792aff5743f0a8a7b6695`, plan hash `efbfcf17861878e528e0c359877d65281d695a78e1adaabb105181bd4b68f68d`. The atlas commit is `4897d9e02b2942670bafc52bc966ef6709167b64`.

## WHAT GENERATION 8 GOT RIGHT

The trajectories that were run are intact. The micro-batch platform, exact replay, and the event semantics were not the flaw.

The organising coordinate that Round 0 found, and Rounds 1 and 2 followed, is still there under exhaustive context starts. Dense minus sparse on the copied expressions is R03 +0.1728, R01 +0.0723, R04 +0.0691, R00 +0.0033, R02 −0.0711, R06 −0.0854, R07 −0.1448, and the composite R05 +0.2378. The 3-edge layer stays near 0.314, and at 0.3072 on R05. Strong favour reverses strong suppress on both the conditional dissolve and the unconditional dissolve.

Visible-source routing survives. Path splits between star and triangle. Star and triangle route mostly through path. The shares move by a few hundredths across the eight systems. They do not change family.

The composite still shifts occupancy more than either component. The 11-class residual against R03 + R04 − R00 has L1 0.0640, near Generation 8's 0.0698. It still does not create a private route family. On the single dense-minus-sparse coordinate the same residual is −0.0008.

The methodological sequence of Generation 8, exploration then observation then a revised exploration, stands. Generation 8A is a further revision of the context basis, not a rescue of a routing hypothesis.

## WHAT GENERATION 8'S CONTEXT QUOTIENT MISSED

Generation 8 executed one representative of each orbit under `Aut(visible source graph)`. That group preserves baseline dynamics. It does not preserve a labelled rule whose action edge or conditioning triad moves. Eighty-six graph-only orbits on this palette split once the rule is required to be invariant.

The missed distinction is formal and is now calculated. The numerical miss on the first other 3-edge destination is small once it is measured on one sample. Uniform-raw mutual information is at most 0.0702 nats. Pooling the same raw trajectories into graph-only orbits changes that figure by at most +0.0335 nats, and sometimes downward, because equal orbit weight is a different prior. Generation 8's published orbit-equal numbers are a third estimand: one representative, a different seed. They are not subtracted from the raw figure as if they were the same quantity.

## RULE-AWARE SYMMETRY

`Aut(source graph, constraint system)` preserves the labelled source pair mask and the multiset of labelled rules. Baseline recovers the source-graph group: order 6 on star and triangle, order 2 on path. A conditional or off-edge rule reduces star and path to the identity, 16 singleton orbits, and leaves a order-2 subgroup on triangle, 12 orbits. An unconditional `dissolve(0-1)` leaves order 2 on every source; on path that is already the full source group, so path does not split. The grade does not change the group. These groups were frozen in the plan before execution. They describe the 16 raw starts. They did not choose them.

## RAW-CONTEXT OBSERVATIONS

6,144 episodes, 16 replicates of each of 48 starts, horizon 512. All ended at the horizon. Durable replay 615/615 exact. No timeout, retry, or quarantine.

Median pairwise destination JS among the 16 raw contexts of a system and source is about 0.008 to 0.020. The maximum is 0.2903, R03 star `t08` (6 path, 10 triangle) against `t13` (16 path). Those two contexts agree on dense minus sparse, +0.1809 and +0.1847. Three cells are 16/16 path, including baseline triangle `t00`.

Maximum occupancy L1 between two raw contexts is 0.0994, on baseline path. Within a system, dense minus sparse spans about 0.06 to 0.09. Grouping conditional starts by whether the conditioning triad is initially present moves that mean by at most 0.0144.

## INITIAL-CONTEXT EFFECTS

Under the uniform raw prior, information about the first other 3-edge destination is 0.0127 to 0.0702 nats. At checkpoint 1 that route-outcome information is 0, because one pair toggle cannot reach another 3-edge class. It locks by checkpoint 32 to 64 at the full-horizon value.

Information about the pair class at a checkpoint is a different estimand. From checkpoint 2 through 512 its median stays between 0.1228 and 0.1415 nats. Initial context is not forgotten on that coordinate. It is also not a large controller of the first route label.

For the 208 raw states that Generation 8 executed as canonical representatives, the destination JS between the old 16-replicate sample and the new one has median 0.0084 and maximum 0.1827. The maximum is a baseline cell. The seed change alone moves the tail.

## CURRENT-CONTEXT EFFECTS

`I(current triad; next pair class | current pair class)` is 0.00078 to 0.00354 nats. That is smaller than the initial triad's information about the first destination.

`I(current triad; next pair slot | full labelled pair mask)` is about 0.018 nats on baseline and on the unconditional dissolves, and about 0.030 to 0.036 nats on the five systems whose rule names a triad. The current triad is alignment-specific in that weak sense. It does not outrun the persistent checkpoint class information.

## FULL-PAIR-MASK VS ISOMORPHISM-CLASS CONDITIONING

The next pair event in this comparison is the pair-slot index 0..5. Direction is implied by the pre-state bit.

Given only the 11-class label, current-triad information about that slot is about 0.003 nats without a triad condition and about 0.011 to 0.013 nats with one. Given the 6-bit pair mask, the same information is about 0.018 and about 0.030 to 0.036. The class projection drops a real, still small, dependence. A small class-conditional number is not evidence that the triad is dynamically irrelevant. The mask-conditional number is the more careful one, and it remains small beside a six-way slot.

## EDGE-COUNT AXIS

The axis Generation 8 found does not depend on having quotiented the hidden triad. Suppress moves pair-epochs toward 4–6 edges. Favour moves them toward 0–2. The unconditional grade moves them further than the conditional grade. The off-edge conditional stays near the matched conditional, not near the unconditional rule. Hidden context moves the same coordinate inside one system by less than the unconditional shift.

## COMPOSITE S09

R05, the copied two-rule system, remains the strongest dense shift, +0.2378, L1 0.2535 from baseline. The residual against adding the unconditional piece and the off-edge piece is non-zero on the 11 classes and nearly zero on dense minus sparse. The largest class pieces are about 0.009 in absolute share. Source routing under R05 is the same two-way split, nudged toward path, not a new family.

## WHAT CHANGED AFTER THE REPAIR

Execution identity is the raw triad configuration `t00`–`t15`. All 48 starts per system were run. Rule-aware orbits are published as analysis, including where they are singletons. Graph-only labels remain a crosswalk, not a seed.

The class-only conditional is no longer the only current-context figure. The full pair mask is reported beside it. Checkpoint pair-class information is reported beside first-destination information, and the two do not tell the same story.

Generation 8's sentence that maximum context information is about 0.06 nats remains a fair description of first-destination information under a uniform raw prior on this palette, where the maximum is 0.0702. It does not describe the checkpoint pair-class estimand, and it does not license the graph-only orbit as an execution basis.

## WHAT DID NOT CHANGE

Ontology, horizon, finite grades, replay, and the absence of a hard support boundary. No episode lacked an admissible event. The visible route skeleton did not reorganise. The edge-count order did not reverse. The composite did not become a private route. Generation 8's historical atlas was not rewritten.

## OBSERVATIONS

The observations are the counts, shares, divergences, and information figures in the Round A0 report. The short list is: 6,144 completed trajectories; first-destination information at most 0.0702 nats; median destination JS near 0.01 and a maximum of 0.2903; a persistent checkpoint pair-class information near 0.12 nats; mask-conditional current-triad information about 0.018 or about 0.03; dense-minus-sparse ordered as in Generation 8; class-share residual L1 0.0640.

## INFERENCES

The wrong symmetry was real. On this palette it did not hide a large first-destination effect. What it did hide, and what the raw sample makes visible, is a modest persistent occupancy difference and a small labelled dependence of the next pair slot on the current triad. Both are smaller than the shift produced by changing the finite grade. The extreme destination cells are sampling-sensitive at 16 replicates, because a true symmetry orbit on baseline already reaches JS 0.11 and an identical raw state can move by JS 0.18 across seed schedules.

## RS / GLOBAL-COHERENCE INTERPRETATION

These are statements about one finite relational grammar. Hidden triad context, once every configuration is allowed to run, does not determine the first 3-edge destination. The law and the visible source graph do most of that work, and they do it along an edge-count coordinate that was found by following the trajectories rather than by confirming a routing hypothesis. A labelled condition makes the current triad a little more informative when the pair state is not collapsed to an isomorphism class.

That is not a claim that physical reality implements the grammar. A small effect on this observable does not refute a higher-order relational ontology. Nothing in the sample identifies a designer or an ultimate receiver.

## NEXT OPEN QUESTIONS

Round A1 was considered and not opened. The candidates, with unsummed attention vectors, are in the Round A0 report and in journey step 2.

The questions left open are whether the destination tail at R03 star and R05 triangle is stable under a paired random stream, and whether the persistent 0.12 nats of checkpoint pair-class information is the edge-count coordinate or a residual class distinction. Both can be declared before they are computed. Prohibit still has no concrete support-boundary observation.
