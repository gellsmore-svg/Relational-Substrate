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
Pending execution.

### Interpretation
Pending. Expected implication is observer relativity, not that supplying a readout
is illegitimate. Pure readout still demands actual cancellation of opposite signs.

### Alternative explanations
Readiness-bit activation, sparse matching and growth under a reflecting resource
boundary are explicit conventional alternatives to deepening probability wells.

### RS relevance
Separate preservation of identity from physical/operational accessibility of a
chosen observable. The ready flag is supplied, not an emergent coherence measure.

### Confidence
No empirical claim yet. Predeclaration is local and archived, not externally registered.

### Follow-up experiments
Use these findings to select primary/secondary readouts for SC-027. Permit ongoing
neutral birth and cancellation with answer-blind stochastic admission. Do not
claim microscopic detailed balance merely because macro defects can appear/disappear.
