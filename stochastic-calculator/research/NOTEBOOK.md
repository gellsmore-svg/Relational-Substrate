# Research notebook continuation

All results below are observed. `programme.json` declared SC-002 through SC-019;
follow-ups SC-020/021 and the holdout SC-022 were declared after inspecting earlier
results. The runner writes the full manifest before the first trial. Each ordinary
cell uses two separate 200-seed batches, unless specified otherwise. Both batches
use the same implementation, not independent research teams. The pooled estimates
below are descriptive; per-replication results remain in each run's `summary.json`.

## SC-002 - Equivalence-class diversity

| Field | Record |
| --- | --- |
| Question | Are distinct configurations observationally equivalent? |
| Hypothesis | H1: identity survives neutral defects with varying incidence. |
| Model | Global signed-relation normalization. |
| Variables | Identities 0, 1, 7, 9; six neutral pairs; 400 trials each. |
| Procedure | Perturb and normalize; hash structural states without instance IDs. |
| Results | 1,600/1,600 correct; 400 trajectory hashes per identity. Zero has one final normal form despite varied transient trajectories. |
| Interpretation | Trajectory diversity and final-state diversity are different measurements. |
| Alternative explanations | Standard multiset equivalence; labels on background regions supply some structural distinctions. |
| RS relevance | Operational example of identity without a preserved microscopic template. |
| Confidence | High within this model; no evidence for ontological primacy of relations. |
| Follow-up experiments | Test unlabelled graph isomorphism and topology-sensitive identities. |

## SC-003 - Identity constraint strength

| Field | Record |
| --- | --- |
| Question | Does fault rejection improve identity reliability? |
| Hypothesis | H2, with the explicit null explanation of simple error filtering. |
| Model | Identity 7 plus six neutral pairs; deletion attempts before active steps. |
| Variables | Nine strengths 0-1; fixed attempted fault probability 0.15; 400 trials/cell. |
| Procedure | Hold the fault law fixed; vary rejection probability; log every terminal class. |
| Results | Accuracy 11.75% at strengths 0 and 0.2, 51% at 0.8, 97.5% at 0.99, 100% at 1. Outcome entropy falls from 2.627 bits to zero. All trials normalize. |
| Interpretation | Structural convergence does not certify original identity. The apparent flat low-strength segment is compatible with sampling noise. |
| Alternative explanations | More rejection means less destructive noise by construction; cancellation can mask balanced losses. |
| RS relevance | Separate admissibility enforcement from correctness and from convergence. |
| Confidence | High for measured curve; no critical point identified. |
| Follow-up experiments | Independent fault channels and stronger topology-dependent constraints. |

## SC-004 - First stochastic addition

| Field | Record |
| --- | --- |
| Question | Can 3 + 4 resolve without computing a numeric target? |
| Hypothesis | H3: conservation plus routing suffices. |
| Model | Two relation populations feed a shared output; stochastic handoff and rewiring. |
| Variables | 400 trials in two 200-seed batches, no faults. |
| Procedure | Only after SC-001, implement redistribution; decode only the output normal form. |
| Results | 400/400 produce 7; mean 16.17 counted events including initial/final observations. |
| Interpretation | Numerical output is fixed by a conserved relational measure. |
| Alternative explanations | This is a designed unary addition realization. The input disjoint union already contains the conserved total. |
| RS relevance | An explicit possible mechanism for a deterministic observable under stochastic rewrites. |
| Confidence | High, conditional on rules and boundary encoding. |
| Follow-up experiments | SC-005 replication and SC-019 fixed-initial-state control. |

## SC-005 - Extensive trajectory replication

| Field | Record |
| --- | --- |
| Question | Do identical arithmetic inputs admit many trajectories? |
| Hypothesis | H6. |
| Model | Same addition apparatus. |
| Variables | 3 + 4 and 17 + 28; two 10,000-seed batches each. |
| Procedure | Compare structural-event hashes, final signatures, event counts and decoded values. |
| Results | 40,000/40,000 correct. Each operand pair has 20,000 unique paths; 20,000 unique final incidence structures. Mean events about 16 and 92 respectively; p95 23 and 108. Each individual 10,000/10,000 batch has Wilson interval [0.999616, 1]. |
| Interpretation | Strong finite evidence of diverse microtrajectories with fixed output. |
| Alternative explanations | These seeds also randomize input incidence; diversity might originate at the boundary. |
| RS relevance | Constructive possibility, already compatible with established stochastic computation. |
| Confidence | High for recorded finite ensembles; hash entropy is a diversity proxy, not a true path-space entropy estimate. |
| Follow-up experiments | SC-019 fixes the entire initial microstate. No 100,000-trial claim is made. |

## SC-006 - Addition constraint degradation

| Field | Record |
| --- | --- |
| Question | How does destructive admissibility change output reliability? |
| Hypothesis | H2; test H10 skeptically. |
| Model | 3 + 4 with a deletion proposal probability of 0.15 per active step. |
| Variables | Same nine strengths as SC-003, 400 trials each. |
| Procedure | Record all outputs and confidence intervals, including incorrect normal forms. |
| Results | Accuracy 12%, 17.25%, 27.25%, 45%, 63.5%, 83.25%, 89.75%, 97.5%, 100% at strengths 0, .2, .4, .6, .8, .9, .95, .99, 1. Entropy 2.178 to zero. No timeouts. |
| Interpretation | A graded observed reliability curve exists; the parameter itself is a fault filter. |
| Alternative explanations | Geometric survival under repeated independent fault opportunities predicts the curve without fitting. |
| RS relevance | A warning against inferring a probability well from a reliability curve alone. |
| Confidence | High for measurements; criticality unsupported. |
| Follow-up experiments | Lock the survival formula and test new noise rates in SC-022. |

## SC-007 - Conservation and cancellation

| Field | Record |
| --- | --- |
| Question | Can large opposed contributions cancel to exact small outputs? |
| Hypothesis | H3 and the signed extension of H1. |
| Model | Reverse right-operand orientation; annihilate opposite relations. |
| Variables | 100-100, 3-7, 0-0, -7-(-3); 400 trials each. |
| Procedure | Compare output with independent integer subtraction after normalization. |
| Results | All 1,600 correct. 100-100 has mean 286.9 events but exactly zero output. 0-0 has one trajectory, not artificial diversity. |
| Interpretation | Large transient populations need not imply unstable macroscopic charge. |
| Alternative explanations | Exact programmed anti-pair cancellation. |
| RS relevance | Distinguishes component activity from global invariant variation. |
| Confidence | High for mechanism; theoretical novelty absent. |
| Follow-up experiments | SC-017 covariance and unbalanced-damage control. |

## SC-008 - Mid-calculation perturbation

| Field | Record |
| --- | --- |
| Question | Can an active calculation withstand disturbance? |
| Hypothesis | H1 for neutral disturbance; H8 adversarially for erasure. |
| Model | 17 + 28 with intervention at event count 10. |
| Variables | Neutral-pair counts 1, 6, 20; single erasure controls; 400 trials each. |
| Procedure | Intervene inside normalization; record intervention_applied. |
| Results | 1,200/1,200 neutral trials correct; mean events 94.8, 101.8, 128.5 as pair count grows. 0/1,200 erasure controls recover 45; they normalize at 44. |
| Interpretation | Defect relaxation works inside an invariant class; charge loss persists. |
| Alternative explanations | The neutral perturbation is designed to be exactly cancelling. |
| RS relevance | Recovery requires specifying which information survived the disturbance. |
| Confidence | High for this finite range. |
| Follow-up experiments | The three erasure cells all erase one relation: their pair-count labels are redundant replications, not an erasure-magnitude sweep. Test real multi-erasure doses next. |

## SC-009 - Occupancy, escape, and competing classes

| Field | Record |
| --- | --- |
| Question | Does the original identity attract states after cross-class damage? |
| Hypothesis | H10 versus disconnected invariant classes. |
| Model | Start at 7; perform 24 perturbation/normalization cycles. |
| Variables | Neutral pair insertion versus one sign flip; 400 paths each. |
| Procedure | Observe all 25 macrostate checkpoints, not just endpoint accuracy. |
| Results | Neutral control: 10,000/10,000 checkpoints at 7. Sign flips: 400 exits from 7, zero returns, progression 7,5,3,1,-1,1,... . |
| Interpretation | Different classes are not corrected toward the original value. A forced period-two orbit appears. |
| Alternative explanations | Flipping a relation in a one-sign normal form reduces its magnitude by two until parity controls the residual. |
| RS relevance | An attractor must be distinguished from normalization in a disconnected equivalence class. |
| Confidence | High for observed trajectories; no physical energy or well depth defined. |
| Follow-up experiments | Isolate parity in SC-020 before discussing spontaneous oscillation. |

## SC-010 - Relational product versus repeated addition

| Field | Record |
| --- | --- |
| Question | Does pair composition offer a distinct transparent multiplication model? |
| Hypothesis | Relating operand relations can generate the product count. |
| Model | Cartesian pair obligations versus repeated population replication and normalization. |
| Variables | 3*4, -7*6, 12*13; both models; 400 trials/cell. |
| Procedure | Consume each pair/anchor exactly once; independent multiplication oracle after output. |
| Results | All 2,400 trials correct. 12*13: product mean 524.3 events, repeated model 2,119.6. |
| Interpretation | Pair structure exposes multiplication directly and avoids repeated normalization. |
| Alternative explanations | Explicit Cartesian construction performs substantial designed work; not fixed-species local emergence. |
| RS relevance | A concrete relation-over-relations representation, not evidence that such ontology is necessary. |
| Confidence | High for implementation; speed difference is algorithm-specific. |
| Follow-up experiments | Remove the global pair registry and test duplicate/exclusion failures. |

## SC-011 - Division and residuals

| Field | Record |
| --- | --- |
| Question | Can complete matching produce quotient and residual structure? |
| Hypothesis | Complete divisor-slot groups define quotient units; incomplete group defines remainder. |
| Model | Random injective matching with group commit. |
| Variables | Seven exact, non-exact, signed and zero-dividend cases; 400 trials each. |
| Procedure | Commit only full groups; observe quotient and residual separately. |
| Results | All 2,800 correct. 13/3 gives quotient 4, remainder 1; -13/3 gives -4 and -1. |
| Interpretation | Remainder is an incomplete matching, not an externally computed residual. |
| Alternative explanations | Sequential partitioning and global empty checks are explicitly designed algorithms. |
| RS relevance | A useful structural interpretation of residual admissibility. |
| Confidence | High for tested rules; no fully distributed division result. |
| Follow-up experiments | Distributed completion detection and delayed/duplicate slot claims. |

## SC-012 - Decimal coordination and borrow

| Field | Record |
| --- | --- |
| Question | Can radix coordination use relations over relations and fresh instances? |
| Hypothesis | H4 in a deliberately constructed protocol. |
| Model | Ten-relation transmit bundle, gate re-instantiation, receive in adjacent column; weighted-conserving borrow split. |
| Variables | 37+48, 999+1, 100-1, 1-100, -37-48; 400 trials each. |
| Procedure | Encode decimal columns directly; normalize without unary conversion. |
| Results | All 2,000 correct. 37+48 has one T-C-R cycle, five counted events including boundaries. 999+1 has three cycles, eleven events. |
| Interpretation | Carry can be represented without an ordinary precomputed Boolean carry bit. |
| Alternative explanations | Ten-to-one radix rewriting and certificates are programmed; the certificate preserves information. |
| RS relevance | A testable coordination-carrier analogy. It does not establish nonpersistent physical transport. |
| Confidence | High for protocol, tentative for RS interpretation. |
| Follow-up experiments | SC-014 replay ablation; asynchronous clocks and persistent-carrier comparator remain unimplemented. |

## SC-013 - Locality

| Field | Record |
| --- | --- |
| Question | Is local collision-based cancellation sufficient? |
| Hypothesis | Restricted part of H9, limited to subtraction. |
| Model | Random ring-neighbour handoffs; cancellation only at shared region. |
| Variables | Global/local; 2, 8, 32 regions; 12-9; 400 trials per cell. |
| Procedure | Same 10,000-event budget; measure accuracy and passage time. |
| Results | All 2,400 correct. Global means about 30 events at every size; local means 30.1, 45.5, 355.6. Local 32-region p95 is 830. |
| Interpretation | Local admissibility suffices here but adds a growing encounter cost. |
| Alternative explanations | Ordinary random-walk meeting times; enabled-event search and completion remain global. |
| RS relevance | Separate locality of transitions from locality of orchestration. |
| Confidence | High for this cancellation kernel; H9 for all arithmetic remains unsupported. |
| Follow-up experiments | SC-018 budget sensitivity, then genuinely distributed termination. |

## SC-014 - Higher-order coordination ablation

| Field | Record |
| --- | --- |
| Question | Does bundle replay exclusion matter under duplicate delivery? |
| Hypothesis | H5, narrowly operationalized. |
| Model | Decimal 37+48; retain/remove replay exclusion while preserving all other gates. |
| Variables | Attempted replay probabilities 0, .15, .5; two variants; 400 trials/cell. |
| Procedure | A replay would instantiate another tens relation; compare exact output. |
| Results | Protected variant: 400/400 at every rate. Unprotected: 100%, 82.75%, 48%. Wrong output is 95. |
| Interpretation | Exactly-once coordination prevents this injected failure. |
| Alternative explanations | A conventional consumed marker is sufficient; the test does not remove all higher-order structure. |
| RS relevance | Concrete mechanism for relations constraining other relations, without demonstrated unique benefit of higher-order ontology. |
| Confidence | High for the ablation, low for broad H5. |
| Follow-up experiments | Implement an information-matched first-order protocol and lost-message faults. |

## SC-015 - Scaling

| Field | Record |
| --- | --- |
| Question | How do population size and runtime scale? |
| Hypothesis | Unary population work grows with magnitude. |
| Model | Global addition. |
| Variables | Total populations 12, 85, 285, 1000; two 50-seed batches each. |
| Procedure | Record event counts and wall time including hashing. |
| Results | 400/400 correct; mean events 26.4, 173.0, 570.1, 2000.4. Per-cell Wilson lower bound for 100/100 is about .9630. |
| Interpretation | Event count is near linear in population; scans make runtime grow more quickly. |
| Alternative explanations | Data structures and observer overhead, not substrate complexity laws. |
| RS relevance | No meaningful RS implication detected beyond a representation-cost constraint. |
| Confidence | High for events, machine/load-dependent for wall time. |
| Follow-up experiments | Profile list scans; compare a fully integrated radix mechanism and larger product spaces. |

## SC-016 - Ordered scheduler control

| Field | Record |
| --- | --- |
| Question | Is randomness necessary for correctness? |
| Hypothesis | Exactness arises from invariants, not stochasticity itself. |
| Model | 17-9 under random versus first-enabled event/record selection. |
| Variables | 400 trials each; boundary incidence and replacement endpoints still seeded. |
| Procedure | Keep rewrite rules fixed and change scheduling. |
| Results | 800/800 correct. Ordered schedule always 37 events; random mean 35.7 and p95 45. |
| Interpretation | Random scheduling is not necessary for correct arithmetic. |
| Alternative explanations | These are two implementations of a confluent normal-form computation. |
| RS relevance | Supports compatibility of stochastic microdynamics with exact output, not superiority of noise. |
| Confidence | High; ordered scheduling is not a fully randomness-free engine. |
| Follow-up experiments | Fully fixed incidence and a deterministic replacement rule, plus adversarial unfair schedules. |

## SC-017 - Covariance and cancellation

| Field | Record |
| --- | --- |
| Question | Can highly variable components have an invariant sum? |
| Hypothesis | H7. |
| Model | Identity 7 with a uniformly sampled 0-29 neutral pairs; optional 0-7 erasures. |
| Variables | Balanced versus damaged populations; 400 independent microstates per variant. |
| Procedure | Measure signed contributions before normalization and output afterward. |
| Results | Balanced: both variances 77.19697, covariance -77.19697, net variance zero; 400/400 correct. Damaged: net variance 4.12055, 92/400 correct. |
| Interpretation | Exact covariance cancellation stabilizes a noisy aggregate. |
| Alternative explanations | Correlation is built into pair creation; the variance identity predicts the result exactly. |
| RS relevance | Coherence should not be identified with low component variance. |
| Confidence | High for observations; no newly discovered statistical law. |
| Follow-up experiments | Allow correlated faults with a tunable, independently specified covariance. |

## SC-018 - Finite-budget failure

| Field | Record |
| --- | --- |
| Question | Does invariant correctness imply prompt convergence? |
| Hypothesis | No; finite runtime can prevent observable output. |
| Model | Local 12-9 on 32 regions. |
| Variables | Budgets 10, 50, 200; 400 trials each. |
| Procedure | Count incomplete trials as failures; never decode partial state. |
| Results | Initial programme: 0/400, 2/400, 125/400 finish correctly; timeout fractions 1, .995, .6875. No completed trial is wrong. |
| Interpretation | Finite-time reliability and conditional correctness are distinct. |
| Alternative explanations | Random-walk latency plus externally imposed deadlines. |
| RS relevance | Operational durability requires a timescale as well as a conserved identity. |
| Confidence | High for these budgets. |
| Follow-up experiments | `censoring-v2` repeats these cells after adding incomplete-state snapshots. Original v1 timeout logs have no terminal population; replay from the archived source preserves that limitation. |

## SC-019 - Fixed initial-state trajectory diversity

| Field | Record |
| --- | --- |
| Question | Does diversity persist when initial incidence is exactly fixed? |
| Hypothesis | H6 survives removal of the SC-005 boundary-randomness confound. |
| Model | Same exact initial relations encoded with seed 20260910; independent transition PRNG. |
| Variables | 3+4 and 17+28; two 1,000-trial batches each. |
| Procedure | Record identical initial populations, excluding seed from path hash. |
| Results | 4,000/4,000 correct; 2,000 distinct trajectories for each operation. |
| Interpretation | Structural trajectories genuinely differ after a common initial condition. |
| Alternative explanations | Designed stochastic scheduling of an invariant-preserving algorithm. |
| RS relevance | The strongest apparatus-level evidence for the requested micro/macro distinction. |
| Confidence | High, conditional on this model. |
| Follow-up experiments | Quotient trajectories by background-region permutations; compare adversarial schedules. |

## SC-020 - Parity-specific oscillation follow-up

| Field | Record |
| --- | --- |
| Question | Is the SC-009 oscillation spontaneous or forced by parity? |
| Hypothesis | After repeated single flips, even identities reach absorbing zero; odd identities alternate at +/-1. |
| Model | 24 flip/normalization cycles, declared after SC-009. |
| Variables | Starts 0,1,2,6,7,8,9; 200 trials each. |
| Procedure | Inspect every checkpoint rather than endpoint correctness. |
| Results | All 1,400 paths follow the parity rule. Starting at 1 gives 2,400 departures and 2,400 returns across 200 paths, ending correctly at 1 after an even number of kicks. |
| Interpretation | Endpoint accuracy can conceal complete intermediate instability. |
| Alternative explanations | Each flip changes charge by two; pair cancellation and periodic forcing explain the orbit. |
| RS relevance | Useful falsification of an attractive 'spontaneous oscillation' interpretation. |
| Confidence | High for parity; not evidence for spontaneous synchronization. |
| Follow-up experiments | Random kick timing and genuinely autonomous transition cycles. |

## SC-021 - Carry-error amplification

| Field | Record |
| --- | --- |
| Question | Do downstream coordination faults magnify numerical error? |
| Hypothesis | More carry boundaries create more fault opportunities and higher-weight defects. |
| Model | Unprotected receive replay, attempted probability .25. |
| Variables | 9+1, 99+1, 999+1; 400 trials each. |
| Procedure | Record all outcomes and their digit-scale error distribution. |
| Results | Correct fractions .7725, .5675, .4525; outcome entropy .774, 1.622, 2.380 bits. |
| Interpretation | Additional boundaries lower reliability and can create larger numerical defects. |
| Alternative explanations | Multiple independent replay opportunities and imposed decimal weights; not nonlinear fluid-like instability. |
| RS relevance | Coordination cost depends on represented scale; evidence is specific to this fault model. |
| Confidence | High for measurements, no physical scaling inference. |
| Follow-up experiments | Matched protected cascades and feedback damping under repeated faults. |

## SC-022 - Held-out survival comparator

| Field | Record |
| --- | --- |
| Question | Is the constraint curve explained by ordinary survival probability? |
| Hypothesis | P(correct) = ((1-d)/(1+d))^7, d = fault_rate*(1-strength). |
| Model | 3+4; formula derived after SC-006 but locked before these trials, with no fitted parameter. |
| Variables | Previously untested attempted fault rates .05 and .3; strengths 0,.5,.9; 800 trials/cell in two batches. |
| Procedure | Compare predictions to all six pointwise Wilson intervals. |
| Results | Observed .4775,.70375,.94625 and .01625,.13125,.66375; predictions .49630,.70464,.93239 and .01312,.12052,.65696. All six predictions lie inside their intervals. |
| Interpretation | The no-fit conventional model is compatible with held-out measurements. No phase-transition explanation is required. |
| Alternative explanations | Interval overlap is not an equivalence test and does not exclude all other models. The comparator applies specifically to positive addition under this scheduler. |
| RS relevance | A strong restraint on interpreting constraint curves as new RS evidence. |
| Confidence | High for comparator compatibility; generalization to other mechanisms untested. |
| Follow-up experiments | Predict a topology-sensitive mechanism where conventional survival alone fails, then reserve new inputs before testing. |

## Milestone answer

Stable arithmetic can arise under genuinely varied stochastic rewrite trajectories
when the chosen rules preserve an invariant and normalize its representation.
This is an implemented constructive example, not a novel theorem. The strongest
results are already explained by conventional rewriting, conservation, exactly-once
protocols, random-walk encounters and elementary probability. No new physical law,
unique RS prediction, spontaneous hierarchy, independent coherence factor, or
physically defined attractor depth was established.

The useful RS contribution is an auditable apparatus and sharper distinctions:
invariant preservation versus damage repair; microscopic activity versus aggregate
variance; normalization versus original-target attraction; transition locality
versus controller locality; and endpoint correctness versus temporal durability.
