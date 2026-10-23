# RRC-001 interpretation

Round `rrc-001` is closed. The plan file was not edited after the cells ran. Execution commit `cdc1de55c3e6e2f4e1b646d33d78859101a3348a`. Plan hash `172ff5ce99e0fca96ce3c5cb94e6fc1d9518f0352007740a174935488fe95382`. Engine `rrc-0.1.0`. Definitions commit `2053b8bddc94b3a9b1d5db712f4c91c6518a681b`. Verify: 29 complete, 0 failed, 0 timeout, 0 unresolved.

The atlas lists every cell. This note says what those cells mean. Layers stay separate.

| Layer | What it is allowed to say |
| --- | --- |
| Exact mathematics | A proof from the rule, or a rational identity checked in integer arithmetic on the weight table |
| Model observation | A number written by a frozen cell |
| Numerical residual | A gap at the size of the solver tolerance |
| Representation | A consequence of a designated subset, a named statistic, or the path-index scaffold |
| Inference | A reading that the cells support and that is narrower than a theorem for every N |
| Ontological reading | None are recorded |

Six constituent nodes, six edges along a path, six levels of composition, and six units of context remain four different claims. The round varied the first. It constructed one level of composition. It did not build a path of six edges, which would need seven nodes, and it did not store six units of context.

## 1. Exact mathematics

### 1.1 Unconstrained and state-independent weights

These identities were proved before the round and used as checks. The frozen R0 cells replicate them at every size in the plan, including sizes the test suite had not executed.

If every pair has the same positive weight, the next law of any fixed set of visible pairs is the same from every hidden pattern. A hidden flip holds the interface still. The stationary presence of every pair is 1/2. The grammar form on an exact interface is `unconstrained_lazy`.

If the weights are positive and depend only on which pair is flipping, the same lumpability holds, the toggle probability of pair e is r_e / R from every state, and the form is `reweighted_single_toggle` when the r_e are not all equal.

### 1.2 Balance when a weight ignores its own bit

For the soft wedge, and for the soft wedge multiplied by a constant on the star of a node, the weight of toggling pair e does not depend on whether e is currently present. A common neighbour is made of other pairs. The boost is a constant multiplier.

Let W(G) be the sum of the toggle weights at graph G, and let Z be the sum of W over all graphs. The probability π(G) = W(G) / Z satisfies detailed balance. The two directions of a flip contribute w(e, G) / Z on each side, and those weights agree by the bit condition. All weights in these two rules are positive, so the chain on the hypercube of graphs is irreducible. π is therefore the stationary law. It is already balanced across the two parity classes, which is why it is a fixed point of a period-2 chain.

The stationary rate at which e flips is the average of w(e, ·):

sum_G w(e, G) / Z.

The unboosted soft wedge is symmetric across pairs, the rates sum to 1, and each rate is exactly 1/E.

The frozen boost multiplies star weights by 5. The unboosted averages are equal, so the boosted averages stand in the ratio 5 : 1. With I = N − 1 star pairs and E − I other pairs,

R = 5 I + (E − I),

the star rate is 5/R and every other rate is 1/R. Those are the state-independent rates with incident weight 5 and other weight 1.

`test_soft_wedge_balance_gives_orbit_rates` checks stationarity of π on N=3 and N=4, and checks the orbit rates on N=3, 4 and 6. The stored propagation solvers agree with these rates to within 2×10⁻¹². The match is this identity, confirmed by the cells, rather than a numerical coincidence.

Presence is a different functional of π. It is the W-weighted fraction of graphs in which the pair is on. It is not 1/2, because W is not constant.

### 1.3 The hard wedge absorbs at the empty graph

A present pair has weight 1 under the hard wedge: the zero applies only to an absent pair with no common neighbour. The empty graph has no present pair and no common neighbour, so every weight is 0 and the chain halts there. Any nonempty graph can delete a present pair. Repeating deletions reaches the empty graph, which has no exit. The only deadlock is the empty graph, and the only recurrent class is that one state.

`test_hard_wedge_empty_graph_is_the_only_deadlock` checks N=3 and N=4. Every frozen hard-wedge cell reports the same counts: one deadlock, one recurrent class. The counts are the rule, confirmed by the enumeration. The hard wedge does not stabilise a nonempty structure.

## 2. Model observations

State counts: N=3 has 8 graphs, N=4 has 64, N=5 has 1,024, N=6 has 32,768. Every cell finished by exact enumeration. The event shape in every cell is `single_toggle_or_hold`. No cell produced `outside_grammar`.

### 2.1 Interface exactness

Defects are rational L1 defects of the next interface-block law. Exact means numerator 0.

| Cell family | Exact cells | Form | Closure against the full state count |
| --- | --- | --- | --- |
| R0 unconstrained, all seven partitions | 7 of 7, defect 0/1 | `unconstrained_lazy` | Closure equals the interface block count |
| R1 hard wedge, all seven | 0 of 7 | `not_markovian_on_interface` | Full count minus 1, 1, 7, 11, 79, 35, 72 |
| R2 soft wedge, all seven | 0 of 7 | `not_markovian_on_interface` | Closure equals the full count in every cell |

The seven partitions are: hide {0,1} at N=3 and N=4; hide {0,1,2} at N=4, 5 and 6; hide {0,1,2,3} at N=5; and the two triangles {0,1,2} and {3,4,5} at N=6.

Selected defects, copied from the result rationals:

| Cells | Defect |
| --- | --- |
| R1, one hidden pair (N=3 and N=4) | 2/3 |
| R1, hidden triangle at N=4, N=5 and N=6 | 51/40 |
| R1, hide four nodes at N=5 | 4373/2688 |
| R1, two triangles at N=6 | 180449/110880 |
| R2, one hidden pair (N=3 and N=4) | 1/3 |
| R2, hidden triangle at N=4 | 1207/2520 |
| R2, hidden triangle at N=5 and N=6 | 486/935 |
| R2, hide four nodes at N=5 | 33912142353/69807337600 |
| R2, two triangles at N=6 | 11106/17765 |

The repeated fractions are part of the observation. A proof that they hold for every larger N is open.

One witness, from `L-N4-hide3-R2`: masks 20 and 21, edges {(0,3),(1,3)} and those edges plus the hidden pair (0,1), pairwise L1 28/45. The two graphs share the interface and disagree about its next law. The hard-wedge triangle cells from N=4 through the two-triangle cell share a witness shape of the same kind, masks that differ by one hidden pair, with pairwise L1 4/3.

### 2.2 Repairs

| Situation | Edge count | Parity | Wedge-count profile |
| --- | --- | --- | --- |
| R0, every partition | exact | exact | inexact in all seven cells |
| R1 or R2, one hidden pair | exact | exact | exact only for R1 at N=3 (7 blocks of 8); inexact for R1 at N=4 and for R2 at N=3 and N=4 |
| R1 or R2, three or six hidden pairs | inexact | inexact | inexact |

R0 wedge-count defects include 2/3, 3/4, 9/10, 16/15 and 9/8. The profile is a refinement of an interface that was itself exact. Strong lumpability is not inherited by a refinement, and this refinement loses it.

With one hidden pair, count and parity are exact because each statistic is that bit. That is the full hidden state, recovered under another name. It is not an intermediate summary.

For the soft wedge, closure equal to the full state count means something stronger than the failure of these three statistics. Any exact aggregation that still reports the interface has to separate every pair of graphs. No proper function of the hidden graph restores strong lumpability on these cells.

The hard-wedge gaps are real and small. They are not a stable bound: the omitted counts are 1, 1, 7, 11, 79, 35, 72. The largest gap in the round, 79 graphs at N=5 with four nodes hidden, still leaves 945 blocks out of 1,024.

### 2.3 Stationary profiles

R0 against the state-independent boost (weights 5 on the star of node 0, weight 1 elsewhere):

- Stationary total variation is 0 at N=3, 4, 5 and 6.
- Presence stays 1/2 on every pair. The occupation gaps in the files are 0.
- Signed rate changes are the identity of section 1.1. Star pairs move to 5/R and the other pairs move to 1/R, from a base rate 1/E.
- The absolute rate gaps are 4/33 and 8/33 at N=3, 1/9 and 1/9 at N=4, 6/65 and 4/65 at N=5, 8/105 and 4/105 at N=6. At N=4 the two absolute gaps agree because 5 and 1 sit equally far from the mean weight 3. The signed changes are opposite. The depth table stores absolute gaps, so a flat absolute row at N=4 is this arithmetic, while the signed rates remain two different numbers.

R2 against the soft-wedge boost (the same multiplier 5 on the same star):

| N | Total variation | Soft presence | Boosted star presence | Boosted complement | Star shift | Complement shift |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 4/77 | 9/14 | 95/154 | 107/154 | −2/77 | +4/77 |
| 4 | 3/74 | 43/74 | 43/74 | 43/74 | 0 | 0 |
| 5 | 927/22750 | 478/875 | 1259/2275 | 176/325 | +81/11375 | −54/11375 |
| 6 | 743/21868 | 4121/7810 | 29279/54670 | 28631/54670 | +216/27335 | −108/27335 |

These rationals are π ∝ W, evaluated in integers. The stored solver figures differ from them by at most about 2×10⁻¹². At N=4 the file's occupation gaps, about 10⁻¹², are that residual. The presence shift is 0. The total variation is not 0: the law over the 64 graphs does move, by 3/74, while every single-pair marginal stays at 43/74.

The mean number of present pairs is invariant under the frozen boost: 27/14, 129/37, 956/175 and 12363/1562 at N=3, 4, 5 and 6. The complement shift is the star shift scaled by the ratio of the two orbit sizes, with the opposite sign.

Soft presence is above 1/2 at every computed N and moves toward 1/2 as N grows through this range. W(empty) = E and W(complete) = 4E for N≥3, so the weight that defines π is larger on the complete graph than on the empty graph. The occupation figures are the resulting density.

### 2.4 Composition

`L-N6-triads-*` hides the inside of each of two triangles and keeps the nine pairs that run between them. This is a constructed cut, designated in the plan.

R0 remains exact, defect 0/1, form `unconstrained_lazy`, closure equal to the 512 interface blocks. R1 has defect 180449/110880 and closure 32,696 of 32,768. R2 has defect 11106/17765 and closure equal to all 32,768 graphs. The qualitative split matches a single hidden subset. The fractions do not match the single-triangle fractions. One composition level was built. A hierarchy of six levels was not.

## 3. Challenge

### 3.1 Residuals

Every propagation solver converged under the frozen tolerances. Where a dense check was allowed (N≤5, at most 1,024 states), the dense gap is about 10⁻¹² or smaller. N=6 has no dense matrix, by the frozen rule, and the two-start gap is about 10⁻¹². Rate and presence figures in section 2.3 that sit at 10⁻¹² in the files are residuals against the integer identities. They are not small scientific effects.

### 3.2 The path index

The scaffold labels a pair by the smaller endpoint. For a rule that is symmetric under every relabeling of {1, …, N−1}, the pairs fall into two orbits: the star of node 0, which is depth 0, and every remaining pair, which occupies every depth from 1 upward. Equal numbers at those greater depths are the orbit, written out once per depth. They are not a signal that travelled and then stopped.

The instrument answered the propagation question it can answer. A local multiplier changes the two orbits and does not create a further depth gradient. It does not measure successive transmission along a path of relations, because the underlying carrier is the complete set of potential pairs and the perturbation does not distinguish those pairs.

### 3.3 The N=4 cancellation

The zero presence shift at N=4 is exact for the frozen weights, at multiplier 5. After the round, the same weight table was checked at multipliers 2 and 7, and at a few other positive (common, base) pairs. Presence stayed uniform across pairs in those checks. The same multiplier 5 moves presence at N=3, N=5 and N=6, and the direction changes: the star loses presence at N=3 and gains it at N=5 and N=6.

This is a property of four nodes under this family, observed beyond the single frozen multiplier and not proved for every positive pair. It is not a solver accident, and it is not a six-node effect. The general proof is the open analytic question.

### 3.4 What would have been a different result

The pre-round feasibility note named five separations. They are scored in `docs/feasibility.md`. In short: exactness tracks whether the weights depend on the hidden pairs; the failure begins at N=3; the three named statistics do not supply a general exact repair; six nodes is not the first change; the local boost rescales the two symmetry orbits and, for the soft wedge, redistributes presence between those orbits.

A representation in which the subsets were discovered by a dynamical criterion, rather than designated, was not run. Weak lumpability, history, and hyperedges were excluded by the plan. Those exclusions bound the claim. They do not soften the exact failures inside the plan.

## 4. What the questions can now say

The opening question rows are unchanged. These sentences are the round's partial answers.

- RRC-Q01. On this grammar the qualitative behaviours are already present at N=3: exact interfaces for weights that ignore the hidden pairs, inexact interfaces for both wedge rules, and a unique absorbing empty graph for the hard wedge. Larger N in the round changes fractions and closure gaps. It does not introduce a new verdict.
- RRC-Q02. For the soft wedge, the exact interface-respecting description is the full current graph on every frozen cell. For the hard wedge the exact closure is the full graph minus a thin set whose size depends on N and on the cut. Neither is a finite bound that stays fixed while N grows.
- RRC-Q03. Six nodes repeats the verdicts of three, four and five, including two defect fractions that agree with a neighbour. The round gives no exact property that singles six out.
- RRC-Q04. The outside can ignore the inside when the weights do not depend on hidden pairs. When they do, hidden current state changes the next outside law, from N=3 upward on these cuts.
- RRC-Q05. An exact unconstrained interface stays `unconstrained_lazy`, including the two-triangle cut. A failed wedge reduction is recorded as `not_markovian_on_interface`. The round produced no transformed grammar and no new event shape.
- RRC-Q06. The local change shows up as two orbits. Graph connectivity of the complete carrier is not a record of transmission. The path index, on this perturbation, coincides with the orbits.
- RRC-Q07. Witness pairs give concrete graphs with the same outside pattern and different next laws. Restoring exactness required the whole hidden state for the soft wedge. Count and parity sufficed only as names for a single hidden bit. The wedge profile did not suffice, and on the unconstrained rule it destroyed an exact interface.
- RRC-Q08. All 29 items were exact enumerations inside the 120-second watchdog. N=6 stationary work stayed iterative. Nothing was sampled.
- RRC-Q09. One constructed composition preserved the qualitative split and did not preserve the defect fractions. No cross-scale numerical invariant, other than the unconstrained form, was found.
- RRC-Q10. Two organisations were not in the opening list. Refining an exact interface by wedge counts can destroy exactness. At four nodes the soft-wedge boost can move the law over graphs while leaving every pair's presence exactly where it was.

## 5. What is not claimed

There is no Relational Substrate ontological reading of these cells. There is no identified bound of six constituent nodes, no result about six edges along a path, no result about six levels of composition, and no result about six units of context. There is no claim that every relational grammar has a finite interface, and no claim that none does. The next proposal is `docs/rrc-002-proposal.md`. It is not a frozen plan.
