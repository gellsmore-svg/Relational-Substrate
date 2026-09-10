# RS findings

## Observer and recurrence extension: SC-026/027/027R

### Strong within-model finding: some instability belongs to the readout

Evidence: on the same CG trajectories, pure readout was correct in 50/50 trials at
500/2,000/8,000 proposals. Ready readout was correct in 0/50, 1/50, 1/50 and escaped
393 times over 8,000 steps. For 50+50, pure readout was 50/50 at 2,000 while ready
readout was 0/50; both were 50/50 by 8,000. Identity was never lost.
Experiment IDs: SC-026.
Replications: 50 paired seeds per cell; checkpoints/readouts share trajectories.
Alternative explanations: a supplied readiness flag adds activation delay and flicker.
Confidence: high within this representation; 50/50 Wilson interval [.9287, 1].
Implication: refine the earlier stability finding: R is needed for persistent ready
readout, not for persistent polarity-only numerical readout. Neither observer is
automatically privileged by RS. Constraints remain legitimate programmed rules.

### Supported finding: recurrent readability without permanent cleanup

Evidence: with neutral births continuously admitted at b=.01, pure occupancy was
.954335 and .949245 in separate seed batches. There were respectively 233/231
departures and 227/229 complete returns. No growth or readiness irreversibility
was enforced. All trajectories preserved charge; only readability was lost/restored.
Experiment IDs: SC-027, SC-027R.
Replications: two disjoint 50-seed batches for each nonzero cap32 condition.
Alternative explanations: finite birth-death dynamics with a generic birth bias.
Confidence: supported for 3+4 in the tested regime, not arbitrary operations or faults.
Implication: frequent, reproducible access to a numerical class need not require an
absorbing microscopic state. This is not recovery of destroyed identity, nor proof
of full microscopic Markov reversibility or thermodynamic detailed balance.

### Supported comparator and retained discrepancy

Evidence: predeclared stationary pure-occupancy predictions .950231/.767740/.290238/
.007700 for b=.01/.05/.2/.5 lie within the seed-bootstrap occupancy intervals in
both batches. One primary terminal count, 44/50 at b=.01, marginally excluded its
prediction under Wilson intervals; replication gave 48/50 and included it.
Experiment IDs: SC-027, SC-027R.
Replications: two 50-seed batches; replication was declared after the discrepancy.
Alternative explanations: sampling variation, incomplete mixing, macro approximation.
Confidence: useful quantitative comparator; not complete equilibrium validation.
Implication: a defined statistical potential can describe a well-like distribution,
but ordinary stochastic computation accounts for this evidence. No uniquely RS
mechanism or physical energy landscape was established. Do not erase the first
snapshot discrepancy or treat marginal intervals as simultaneous guarantees.

### Negative findings and next test

Evidence: C-only time-mean population changed from 29.13 to 387.79 when capacity
changed from32 to512. At recurrent b=.5, cap interventions remained substantial.
Paired cap32/cap128 paths were identical at b=.05/.2 where neither cap intervened.
Experiment IDs: SC-026/027.
Replications: 50 paired seeds per capacity/rule; matched duplicates are controls.
Alternative explanations: reflecting boundaries and population drift, not spontaneous
numerical attractor selection. Topology remains unnecessary for the global invariant.
Confidence: high for the measured limits; no broad theorem about RS substrates.
Implication: SC-028 needs an explicit redundancy/surviving-information model before
claiming repair after charge loss. No new multiplication, division, higher-order
coordination or T-C-R capability is established by this stage.

Full protocol and qualifications: [RELAXATION_LAB.md](research/RELAXATION_LAB.md).
Data, uncertainty and plots: [RESULTS.md](research/dynamics-analysis/RESULTS.md).
Earlier findings below retain their original observer and model scope.

## Fixed-proposal extension: SC-023 through SC-025

General programmed constraints are the intended experimental subject. A successful
deterministic scheduler does not invalidate that subject. The audit asks whether
constraints inspect an answer oracle, not whether constraints exist. The new kernel
receives state and general rules, neither operands nor an expected answer.

### Strong within-model finding: distinct forms of stability

Evidence: C alone preserved identity 100/100 but yielded no readable terminal
state. CGR gave 100/100 correct with no escapes. G/GR gave readable wrong zeroes
100/100. CG visited correct readout in 69/100, escaped 162 times, and ended there
in only 1/100. All 100 full-constraint accepted-state trajectories differed.
Experiment IDs: SC-023; full-constraint replication SC-024.
Replications: 100 paired seeds per ablation; 100 independent full-replication seeds.
Alternative explanations: conserved multiset invariant, normalization, chosen observer.
Confidence: high within model; 100/100 Wilson interval [0.9630, 1.0000] per batch.
Implication: identity preservation, readable capture and durable readout are distinct
operational coherence factors. R stabilizes this readout, not the charge observable.

### Moderate finding: reliability depends on duration and enforcement

Evidence: at 2,000 proposals, .9/.99/.999/.9999/1 enforcement gave 0/0/48/95/100
correct answers out of 100 each. At .99, 59 visited correct readout but none retained
it at the horizon. The predeclared survival bound is consistent with these samples.
Experiment IDs: SC-024.
Replications: 100 new paired seeds per strength; one horizon only.
Alternative explanations: cumulative death/flip/cancellation hazards. With no growth
and any imperfect conservation enforcement, eventual zero follows almost surely
under ideal independent draws; this is analytic, not an infinite-duration experiment.
Confidence: high for sample counts; limited generality of one horizon.
Implication: report observation duration with degrees of determinism. A steep curve
alone establishes neither a physical probability well nor an unexplained transition.

### Moderate finding: reusable constraints need not complete promptly

Evidence: unchanged C/G/R preserved charge in all 800 transfer trials. 17+28 became
readable in 87/100 global and 19/100 local trials; 50+50 in 0/100 in either mode.
Zero and negative inputs used the same rules. No full-constraint cap hits occurred.
Experiment IDs: SC-025.
Replications: 100 paired seeds per input/locality cell.
Alternative explanations: sparse matching and random activation of supplied readiness.
Confidence: high within this size/horizon range; no universal complexity law.
Implication: separate arithmetic invariant, readout cost and coordination cost.
Local cancellation with global rewiring/selection is not full decentralization.

### Negative findings and limits

Evidence: C/CR each incurred 7,124 capacity rejections. Incidence remains inessential
to global charge. Input joining explicitly establishes additive composition.
No multiplication, division, higher-order or T-C-R extension was tested here.
Experiment IDs: SC-023 through SC-025.
Replications: counts above; no cap-sweep or alternate-observer replication yet.
Alternative explanations: ordinary constrained stochastic computation is sufficient.
Confidence: high about implementation boundaries, not all possible RS models.
Implication: test cap sensitivity, reversible relaxation and alternative readouts;
then audit multiplication's pair registry. No ontological amendment is warranted.

Notebook: [CONSTRAINT_LAB.md](research/CONSTRAINT_LAB.md).
Data and uncertainty: [RESULTS.md](research/constraint-analysis/RESULTS.md).
The historical findings below retain their original scope.

This report is suitable for transfer into the RS/Nexology programme. It distinguishes
observations from interpretation and makes no physical-substrate claim. See the
[notebook](RESEARCH.md), [mechanism audit](MECHANISMS.md), and
[measured tables](research/analysis/RESULTS.md) for reproducible support.

## Strong findings

**Exact observables can coexist with stochastic relational trajectories.**

Evidence: 40,000/40,000 SC-005 additions correct; SC-019 fixes the entire initial
microstate and yields 4,000/4,000 correct with 4,000 distinct structural paths.
Experiment IDs: SC-004, SC-005, SC-019.
Replications: two 10,000-run batches per operation in SC-005; two 1,000-run batches
per operation in SC-019.
Alternative explanations: designed invariant-preserving stochastic rewriting,
already familiar in population protocols and chemical reaction computation.
Confidence: high within this apparatus, no claim of theoretical novelty.
Implication: deterministic macro-description does not logically require identical
microtrajectories. This is a constructive example, not evidence about nature.

## Moderate findings

**Local cancellation can preserve arithmetic at increased convergence cost.**

Evidence: all 2,400 SC-013 trials correct; increasing regions from 2 to 32 increases
local mean events from 30.1 to 355.6, while global remains about 30.
Experiment IDs: SC-013, SC-018.
Replications: two 200-run batches per cell, with additional censored repeats.
Alternative explanations: random-walk encounter times and a global scheduler.
Confidence: high for local cancellation; limited for broader decentralization.
Implication: local admissibility and global orchestration must be separately stated.

## Tentative findings

**Coordination carriers are an operational interpretation of bundle certificates.**

Evidence: 2,000/2,000 decimal carry/borrow trials correct; gates relate ten members
and authorize fresh receiver instances.
Experiment IDs: SC-012, SC-014.
Replications: two 200-run batches per decimal case.
Alternative explanations: ordinary radix rewriting and transaction certificates.
Confidence: high as an implementation, tentative as RS interpretation.
Implication: provides a controllable T-C-R test object; not a discovery of its necessity.

## Negative findings

**No unique RS explanation is required by the results.**

Evidence: ordered scheduling is exact; charge erasure is not repaired; a no-fit
survival formula explains new-rate constraint data within all six pointwise intervals.
Experiment IDs: SC-001, SC-008, SC-016, SC-022.
Replications: 1,800 foundational nonzero erasures, 1,200 active erasures, 400 ordered
trials and six holdout cells of 800 trials.
Alternative explanations: conventional conservation, rewrite normalization,
exactly-once enforcement, parity and geometric survival suffice.
Confidence: high that no additional explanation is needed for these observations;
this does not falsify every possible RS model.
Implication: do not promote this apparatus into evidence for a physical substrate
or a new theory of computation. Global incidence is partly representational overhead.

## Unexpected phenomena

**A parity-controlled forced cycle defeats endpoint-only assessment.**

Evidence: start 7 evolves through 5,3,1,-1,1,... after repeated single flips.
Even starting identities reach absorbing zero. Starting at 1 is correct at the
24th kick despite repeated departure from its initial identity.
Experiment IDs: SC-009, SC-020.
Replications: 400 initial flip trajectories plus 200 per follow-up starting value.
Alternative explanations: flipping changes signed charge by two; periodic external
forcing and cancellation completely explain the cycle.
Confidence: high for parity, no support for spontaneous oscillation.
Implication: measure trajectory occupancy and durability, not only endpoints.

## Constraint behaviour

**Reliability rises with explicit fault rejection; criticality is unestablished.**

Evidence: SC-006 accuracy spans .12 to 1 as rejection rises 0 to 1. Held-out rates
in SC-022 agree with `((1-d)/(1+d))^7`, where `d=fault_rate*(1-strength)`.
Experiment IDs: SC-003, SC-006, SC-022.
Replications: 400 per sweep cell; 800 per holdout cell.
Alternative explanations: analytically predicted survival of seven required handoffs.
Confidence: high for the measured curve and comparator compatibility.
Implication: do not equate a parameter called constraint with a deepening attractor.
Full enforcement guarantees rejection of this specified damage channel by design.

## Identity findings

**Equivalence-class preservation is not reconstruction of destroyed information.**

Evidence: 4,000/4,000 SC-001 preserving perturbations succeed; 0/1,800 nonzero
single erasures recover the original identity. Mid-calculation erasure likewise fails.
Experiment IDs: SC-001, SC-002, SC-008.
Replications: 200 trials per foundational cell plus independent follow-up cells;
the final SC-001 rerun reuses seeds and is a reproducibility check, not new evidence.
Alternative explanations: signed cardinality is a programmed invariant; arbitrary
incidence changes do not alter it, but unpaired deletion does.
Confidence: high within this representation.
Implication: any RS identity-recovery claim should state where sufficient surviving
information resides and which perturbations remain inside its identity class.

## Relationships-of-relationships findings

**Coordination over relation families is useful, but its ontological necessity is untested.**

Evidence: product obligations reference relation pairs; division commits complete
matching families; replay exclusion restores carry correctness under injected replay.
Experiment IDs: SC-010, SC-011, SC-014.
Replications: 2,400 product comparisons, 2,800 partition trials, 2,400 carry ablations.
Alternative explanations: ordinary registries, matching constraints and a consumed
flag. No information-matched first-order implementation was tested.
Confidence: high for operational behavior, inconclusive for stronger H5.
Implication: treat higher-order modelling as a useful language until its independent
explanatory or predictive value is isolated.

## Coordination carrier findings

**Carry replay exclusion prevents a specific duplicate-instantiation failure.**

Evidence: protected 37+48 is correct in every SC-014 cell; unprotected accuracy is
.8275 at replay rate .15 and .48 at .5, with errors at 95.
Experiment IDs: SC-012, SC-014, SC-021.
Replications: 400 trials per ablation cell and per amplification case.
Alternative explanations: exactly-once delivery, explicitly programmed.
Confidence: high for this fault channel, not general noise resilience.
Implication: coordination experiments should separately vary duplication, erasure,
delay, and exclusivity. One protected channel is not universal coherence.

## T-C-R findings

**A computational handoff can preserve identity while changing instance identity.**

Evidence: source relations and gate records are consumed/replaced, and receiver
relations are freshly instantiated. Numeric conservation includes in-flight gates.
Experiment IDs: SC-004, SC-012.
Replications: carried across all relevant trial traces; phase-count checks automated.
Alternative explanations: ordinary message reconstruction retaining a certificate;
the information is preserved in software records.
Confidence: high for record replacement, tentative for RS interpretation.
Implication: distinguish persistence of an entity from persistence of relational
information. A matched persistent-carrier comparator and asynchronous clocks remain open.

## Conservation findings

**Conservation supplies exactness only relative to a designed encoding and rule set.**

Evidence: addition/subtraction output agrees with an independent oracle; neutral
defects cancel; decimal bundles preserve weighted signed multiplicity.
Experiment IDs: SC-001, SC-004, SC-007, SC-012.
Replications: multiple seeded batches plus signed operand-grid and radix tests.
Alternative explanations: designed stoichiometry and confluent normal forms.
Confidence: high and supported by a conditional invariant argument.
Implication: computation may be located in admissible transformations, but the
initialization, conservation law and observer map remain substantive assumptions.

## Determinism/stochasticity findings

**Random scheduling is compatible with, but unnecessary for, the exact outputs.**

Evidence: random and ordered schedules both yield correct subtraction; fixed-input
random runs differ in path and length without output variation.
Experiment IDs: SC-005, SC-016, SC-019.
Replications: two batches per setting; ordered incidence remains seeded.
Alternative explanations: schedule independence of the designed rewrite system.
Confidence: high; no assertion that the ordered control removes every random choice.
Implication: microstochasticity and deterministic macrodescription are compatible;
the apparatus establishes no computational advantage from randomness.

## Coherence findings

**Conservation, convergence, correctness, and durability are noninterchangeable.**

Evidence: wrong erased states converge; full-constraint local states time out;
components with variance 77.19697 have covariance -77.19697 and zero net variance;
endpoint-correct parity paths leave their identity repeatedly.
Experiment IDs: SC-008, SC-017, SC-018, SC-020.
Replications: two batches per condition and multiple starting identities.
Alternative explanations: standard statistical dependence and temporal logic.
Confidence: high for distinctions; factor independence and latent coherence are untested.
Implication: use separate operational metrics. Do not collapse them into an
unvalidated scalar coherence factor or impose a final coherence ontology.

## Scaling findings

**A compact number notation can mask expensive unary work and weighted failures.**

Evidence: population 1,000 takes about 2,000 addition events, with scanning overhead;
unprotected carry accuracy falls .7725, .5675, .4525 across one/two/three boundaries.
Experiment IDs: SC-015, SC-021.
Replications: 100 trials per scale, 400 per carry cascade.
Alternative explanations: list scans, independent fault opportunities and imposed radix weights.
Confidence: high for this implementation; no general substrate scaling law.
Implication: record representation cost, controller cost and numerical error scale separately.

## Questions generated

The following are research questions, not established findings. Their evidence is
the limitations above (SC-008, SC-013, SC-014, SC-022); replications and alternatives
are those of the associated entries; confidence in any answer is currently low.

- Can a topology-defined invariant retain identity under damage that changes edge count?
- Which minimal redundant relations permit bounded erasure correction without retaining a numeric target?
- Can distributed completion detection support compositional multiplication and division?
- Does an information-matched first-order protocol perform differently from the bundle representation?
- Can an RS-defined constraint yield a predeclared prediction not captured by a conventional comparator?

## Proposed RS experiments

These proposals have no trial evidence yet; confidence is untested, and conventional
error-correcting codes, population protocols and matching algorithms are required
comparators. Their implication is a test programme, not a theoretical amendment.

1. Topology candidate: compare cycle/component identities against signed cardinality
   under matched rewiring, deletion and incidence-blind controls.
2. Redundancy candidate: distribute relation witnesses, erase components, and measure
   the information boundary for recovery without a stored answer.
3. Carrier comparison: persistent message versus local reconstruction, matched for
   state information, asynchronous delay, duplication and erasure.
4. Decentralization: eliminate global empty checks and pair registries; record which
   arithmetic/composition guarantees survive.
5. Coherence discrimination: predeclare nonredundant metrics and predict a reserved
   perturbation regime before measuring it.

## Proposed theoretical amendments

No change to RS ontology is justified by this experiment. The following are proposed
terminology refinements, with high confidence in their utility inside this apparatus
and untested applicability elsewhere. Evidence and replications are SC-001/008/018/020;
alternative explanations are ordinary invariants, recovery and temporal behavior.

- Require an explicit surviving-information account for identity recovery.
- State the permitted perturbation class and observation timescale with any stability claim.
- Distinguish local rewrite admissibility from global scheduling and completion knowledge.
- Reserve 'attractor' for a defined dynamical property; do not infer it from successful normalization.
- Treat second-order structure as an operational claim until a matched comparator distinguishes it.

**Answer to the principal research question:** this model supplies a reproducible
construction of deterministic arithmetic under stochastic trajectories. Its behavior
is explained by ordinary computer science and probability. The RS contribution at
this stage is a concrete experimental vocabulary and test bench, not independent
confirmation of RS or an advance in physical theory.
