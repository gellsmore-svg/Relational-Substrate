# Observation controls and recurrent stochastic resolution

General constraints are the experimental subject, not evidence of cheating. We
test their sufficiency and observer dependence without passing an answer into
the dynamics. The existing calculator and SC-023/025 mechanism remain unchanged.

## SC-026 - Passive readout, horizon and capacity controls

### Question
Which stability claims depend on the ready marker, finite observation duration,
or the population cap?

### Hypothesis
H16: removing the readiness condition from a passive observer eliminates the
apparent readout instability in CG, without changing identity or trajectories.
H17: longer horizons improve full-constraint completion; unconstrained neutral
growth remains cap-sensitive. Both initially unsupported for this new seed set.

### Model
The unchanged fixed-proposal kernel from SC-023/025. Two passive observers see
every state of the same trajectory: `pure` reads signed cardinality only when all
relations share one polarity; `ready` additionally requires all records ready.
Mixed populations are unreadable for both. Signed charge of mixed populations is
computed only by an independent diagnostic, never reported as a calculator result.
Empty population is readable zero. Neither observer controls transitions or stopping.

### Variables
Three C-only capacities (32/128/512), CG and CGR for 3+4, and CGR for 17+28 and
50+50. Fifty new paired seeds per cell, three initial neutral pairs, eight sites.
Checkpoints 500/2,000/8,000 along each trajectory, no burn-in. Configuration:
`configs/observer-controls.json`. 350 trajectories, 1,050 checkpoint records;
the checkpoints are repeated measurements, NOT 1,050 independent replications.

### Procedure
Archive this protocol, configuration and source before execution. Record both
readouts, trajectory/tape prefix hashes, initial/checkpoint states, charge violations,
population and defect occupancies, cap interventions, captures, escapes, complete
residence/recovery durations and boundary censoring. A defect is one opposite-pair
unit, measured as min(positive count, negative count) outside the kernel.
Time steps and within-trajectory episodes are correlated. Wilson intervals apply
to terminal correctness across seeds; occupancy intervals use a 1,000-resample
seed-level percentile bootstrap, not individual time samples. Cells are paired.
Complete-episode durations exclude boundary-censored episodes and are not unbiased
estimates of all recovery times. No checkpoint is selected after observing success.

### Results
350 trajectories completed, producing 1,050 checkpoint records. In CG, pure readout
was correct in all 50 trials at each checkpoint; ready readout was correct in
0/50, 1/50, 1/50 at 500/2,000/8,000. Over 8,000 steps, CG pure occupancy was
0.98968 with no escapes, while ready occupancy was 0.00788 with 393 escapes.
CG and CGR had the same pure occupancy; the readiness gate changes the supplied
ready observable, not cancellation or charge. Full CGR readouts were 50/50 at
all checkpoints for seven. At 8,000, both larger full-constraint cases were 50/50
under both observers. At 2,000, the 100 case was already 50/50 pure but 0/50 ready.

All C-only cells ended unreadable under both observers. Their time-mean populations
were 29.13, 118.96 and 387.79 at caps 32/128/512, with 26,149/22,488/12,982 cap
rejections across the 50 runs. At cap32 a rare readable visit occurred; do not
interpret zero terminal success as impossibility of transient capture. Odd charge
means the largest reachable populations below these even caps are 31/127/511.

### Interpretation
H16/H17 supported within this model. Readiness-related instability and much of the
large-input delay depend on the supplied observer. This does not make that observer
illegitimate, but its behavior is not an intrinsic instability of numerical identity.
Pure readout still demands actual cancellation of opposite signs. Merely lifting
the growth gate produces cap-sensitive neutral background, not reliable readout.

### Alternative explanations
Readiness-bit activation, sparse matching and growth under a reflecting resource
boundary are explicit conventional alternatives to deepening probability wells.

### RS relevance
Separate preservation of identity from physical/operational accessibility of a
chosen observable. The ready flag is supplied, not an emergent coherence measure.

### Confidence
Fifty seeds per cell; 50/50 terminal success has Wilson interval approximately
[0.9287, 1]. Paired checkpoints are not independent replications. The post-hoc
CG readiness comparator 1/128 is numerically close to 0.00788 occupancy, but this
does not establish the full joint stationary distribution. Protocol was archived
before execution; the archived `protocol.md` retains the unobserved hypotheses.

### Follow-up experiments
Use these findings to select primary/secondary readouts for SC-027. Permit ongoing
neutral birth and cancellation with answer-blind stochastic admission. Do not
claim microscopic detailed balance merely because macro defects can appear/disappear.

## SC-027 - Recurrent resolution under continuing neutral disturbance

### Question
Can a readable equivalence class be highly occupied and repeatedly recovered while
neutral structures continue appearing and disappearing?

### Hypothesis
H18: a generic birth-admission bias can yield high pure-readout occupancy with
measurable escapes and returns, without a hard ban on growth or reverse readiness.
H19: a conventional birth-death comparator accounts for defect occupancy; no
unexplained well or uniquely RS law is needed. Both initially unsupported.

### Model
Same proposal tape and exact local conservation. No irreversible readiness gate
and no no-growth gate. Neutral-pair birth is admitted with fixed probability b;
opposite-pair cancellation remains allowed. The same state-independent b applies
to every population. The proposal's existing independent enforcement draw supplies
this admission, so there is no new state-dependent RNG consumption. At b=0, birth
is prohibited only as the absorbing comparison condition. At b>0, defect count can
increase and decrease. This is bidirectional macro-defect dynamics, not an assertion
of full microscopic Markov reversibility or thermodynamic detailed balance.

The pure observer is primary, selected after SC-026. Ready remains a secondary
diagnostic. Charge-changing damage is still forbidden, so this tests repeated
readout recovery *within* an identity class, not reconstruction of destroyed identity.

### Variables
b = 0, .01, .05, .2, .5 at capacity32; .05 and .2 also at capacity128. Eight initial
neutral pairs, input3+4, 50 new paired seeds per cell. Fixed8,000-step horizon,
4,000-step burn-in, no success-based stopping. Seven cells, 350 trajectories.
Configuration: `configs/recurrent-resolution.json`. No cell-dependent number rule.

### Procedure
Archive protocol and sources, run dynamics, measure both observers and recurrence.
The following no-fit comparator is specified before the run. Let q be absolute
conserved charge and k the number of neutral defects, used ONLY in analysis.
With ideal uniform addresses, macro birth probability per proposal is b/8 below
the cap; death probability is `[2*k*(q+k)/(q+2*k)^2]/8`. The factor follows from
choosing two opposite signs with replacement. The stationary probability weights
obey `pi(k+1)/pi(k) = b / [2*(k+1)*(q+k+1)/(q+2*k+2)^2]`, then normalization.
The kernel never computes q, k, this ratio, or pi. `defect_prediction.py` is solely
a measuring instrument. Finite-word modulo addressing differs negligibly from this
idealization. Burn-in does not prove equilibration; compare observed histograms and
seed-level uncertainty with the predicted distribution and retain disagreements.

`-log(pi(k))` is a defined dimensionless statistical potential when probabilities
are positive, not physical energy. No potential is assigned to the microscopic
graph and no numerical target is supplied to transition acceptance.

### Results
350 trajectories completed. Charge was preserved throughout all of them. In the
4,000-step measurement window at cap32, pure occupancy was 1.00000, 0.954335,
0.775690, 0.291410 and 0.009475 for b = 0, .01, .05, .2, .5. Corresponding no-fit
stationary predictions were 1, .950231, .767740, .290238 and .007700. Every predicted
pure occupancy lies within its seed-bootstrap interval. At b=.01, 233 escapes and
227 complete recovery episodes occurred, with at least one complete return in
49/50 trajectories. At b=.05 there were 943 escapes and 928 complete returns;
at b=.2, 1,429 escapes and 1,395 complete returns. Counts exclude left-censored
recovery starts; unfinished terminal episodes remain logged, not discarded.

No capacity rejection occurred at b<=.2. The cap32/cap128 cells for b=.05 and .2
have identical paired trajectories, so these are capacity controls, not independent
replications. At b=.5 there were 1,553 capacity rejections during measurement;
its stationary distribution is explicitly cap-dependent.

Endpoint caveat: b=.01 ended pure/readable in only 44/50 runs (Wilson interval
[.76195, .94382]), slightly excluding the stationary prediction .95023 despite
good time-occupancy agreement. This discrepancy is retained. Other nonzero cap32
endpoint counts were 35/50, 16/50 and 1/50. These are marginal intervals among
several paired comparisons, not a predeclared omnibus rejection test.

### Interpretation
H18 supported in this bounded model: readable states can be frequently occupied
and repeatedly recovered without hard growth or readiness irreversibility. H19
is supported for time occupancy, but one terminal comparison disagrees marginally.
High occupancy is not permanent correctness, charge-loss repair or a proof of
stationarity. The statistical potential is model-derived and reference-class
dependent; the b=.5 cap-favored region is not a well around correct readout.

### Alternative explanations
Standard finite birth-death dynamics, population bias and a reflecting cap; the
comparator should be preferred over a novel explanation if it accounts for data.

### RS relevance
Test a fluctuating yet repeatedly readable numerical class under general constraints.
Keep readout recovery distinct from preservation or restoration of information.

### Confidence
Fifty seeds per cell. At b=.01 the occupancy bootstrap interval is
[.94636, .96184]; b=.05 [.76042, .79067]; b=.2 [.272315, .310675]; b=.5 [.00686,
.01254]. Time steps are not independent observations. Independent replication
below was specified after observing the terminal discrepancy, with no tuning of b,
the dynamics, horizon, burn-in or initial conditions.

### Follow-up experiments
Independent seed/initialization/horizon replication for apparent wells. Redundancy
and charge-changing damage remain a separate SC-028 project; multiplication is
not revised before understanding this narrower experiment.

## SC-027R - Fresh-seed recurrence replication

### Question
Does recurrent occupancy replicate, and does the low b=.01 terminal count recur?

### Hypothesis
H19 remains provisional for terminal occupancy. A finite-sample fluctuation is
plausible, but do not assume it away. Preserve the first batch regardless of outcome.

### Model
Unchanged SC-027 kernel and predeclared stationary comparator.

### Variables
New seeds 271000-271049; b=.01/.05/.2/.5, capacity32, input3+4, eight neutral
pairs, horizon8,000, burn-in4,000. Four paired cells, 200 new trajectories.

### Procedure
Archive `configs/recurrent-replication.json` and this protocol before execution.
Compare terminal counts, seed-level occupancy intervals and departures/returns.
Do not relabel this post-result replication as part of the original predeclaration.

### Results
200 fresh trajectories completed. At b=.01/.05/.2/.5, pure time occupancies were
.949245/.770425/.292230/.009300, with terminal correct counts 48/50, 42/50, 14/50
and 0/50. Every predeclared stationary pure-occupancy prediction lies inside its
replication seed-bootstrap interval. At b=.01, 231 departures and 229 complete
returns occurred, with a complete return in every one of the 50 trajectories.
The b=.01 occupancy interval was [.94167, .956295]. All trajectories preserved
charge. The first batch's 44/50 endpoint result remains unchanged in its archive.

### Interpretation
High recurrent readout occupancy replicated without tuning. The low b=.01 endpoint
count did not repeat; its replication Wilson interval [.86540, .98896] contains
the stationary prediction. This is consistent with sampling variation, not proof
that the original discrepancy has a unique explanation. H19 is supported as a
useful conventional comparator, not fully validated microscopic equilibrium.

### Alternative explanations
Finite-sample variation, serial dependence within trajectories, incomplete mixing,
or inadequacy of the idealized macro-chain comparator.

### RS relevance
Reliability claims require replication and separate instantaneous availability
from time-averaged accessibility of the preserved identity class.

### Confidence
Supported across two disjoint 50-seed batches for the nonzero cap32 cells. Marginal
occupancy intervals are not simultaneous guarantees. The first batch's capacity
controls are paired duplicates where no cap intervened, not further replications.

### Follow-up experiments
Vary initial defect count and horizon before claiming full equilibrium validation.

## Stage conclusion and audit

SC-026/027/027R contain 900 trial trajectories and 1,600 checkpoint records. There
are three disjoint seed batches; cells within each batch share tapes and checkpoints
are repeated observations. Every trial preserved charge. No result was generated
by the comparator: `recurrent_kernel.py` imports only the original proposal kernel
and dataclasses. `defect_prediction.py`, both decoders, episode statistics and
expected arithmetic live exclusively in the measuring layer. The only new kernel
parameter is a population-independent probability of admitting neutral birth.

The numbers remain unary signed populations and their joining is an explicit
composition boundary. This stage does not discover addition ex nihilo, establish
a relations-first ontology, repair an erased net unit, or extend multiplication,
division, T-C-R or higher-order coordination. It does demonstrate recurrent access
to readable arithmetic under bidirectional defect dynamics rather than requiring
permanent cleanup. Ordinary constrained stochastic computation accounts for the
observations; no uniquely RS explanatory principle was isolated.

Next: SC-028 must make surviving redundant information explicit before attempting
charge-loss repair. A new cap/initialization/horizon study can further test the
stationary comparator. Neither task is silently counted as completed here.
