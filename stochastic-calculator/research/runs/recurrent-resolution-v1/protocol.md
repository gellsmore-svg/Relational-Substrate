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
Pending execution.

### Interpretation
Pending. High occupancy is not permanent correctness or correction of charge loss.

### Alternative explanations
Standard finite birth-death dynamics, population bias and a reflecting cap; the
comparator should be preferred over a novel explanation if it accounts for data.

### RS relevance
Test a fluctuating yet repeatedly readable numerical class under general constraints.
Keep readout recovery distinct from preservation or restoration of information.

### Confidence
Untested; the comparator is an idealized analytic prediction, not measured evidence.

### Follow-up experiments
Independent seed/initialization/horizon replication for apparent wells. Redundancy
and charge-changing damage remain a separate SC-028 project; multiplication is
not revised before understanding this narrower experiment.
