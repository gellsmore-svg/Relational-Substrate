# Fixed-proposal constraint laboratory

## Framing correction

The experiment is about **constraints acting on stochastic possibilities**.
Writing those constraints is legitimate. Neither deterministic acceptance rules
nor a successful deterministic scheduler disqualifies the experiment. What would
disqualify it is concealing an answer-valued target or a conventional expression
solver in the dynamics. Conversely, random event hashes alone do not establish
that constraints cause stable arithmetic. That requires interventions on the rules.

The historical calculator remains unchanged. This separate experimental kernel
extends its addition/signed-cancellation investigation, not multiplication or division.

## SC-023: predeclared design

### Question
Which general constraints preserve identity, make it readable, and stabilize that
readout under continuing random perturbations?

### Hypothesis
H11-H13 in `HYPOTHESES.md`, declared before this run. Conservation alone will not
guarantee a stable normal form; normalizing rules alone need not preserve identity.

### Model
A state is an ordered microconfiguration of oriented, signed incidence records.
The observer identifies a number with positive count minus negative count. The
kernel never computes that difference. Readable states have one polarity and all
records ready; empty is readable zero. Incidence varies, but global-mode arithmetic
does not require topology. This limitation is explicit, not concealed by naming.

Each step selects uniformly from eight proposals: single birth, death, polarity
flip, neutral-pair birth, arbitrary-pair cancellation, rewire, mark ready, mark
unready. Addresses, endpoints, polarity and enforcement draw are always generated,
whether needed or not. A shared seed gives exactly the same proposal tape across
ablations. State-dependent addressing/applicability can still differ. Modulo indexing
has negligible finite-word bias; this is not an exact uniform finite-state sampler.

Three independent constraints:

- **C, conservation:** reject single birth/death/flip and same-polarity cancellation.
  Opposite-polarity cancellation and neutral-pair birth remain allowed. The predicate
  inspects the proposed local rewrite, not a global numeric target.
- **G, no growth:** reject births, including neutral pairs. This is a supplied
  normalization direction, not a property discovered or a conservation law.
- **R, readiness:** reject ready-to-unready transitions. This makes handoff completion
  persistent but is not needed to preserve the signed identity.

Constraints are identical for every number; only input populations differ. All
configurations retain a 128-record cap, fixed grammar, boundary encoding, discrete
clock and observer. Thus `none` means none of C/G/R, not absence of every assumption.
This is broad bounded randomness, not mathematically undefined unrestricted randomness.

### Variables
All eight C/G/R combinations, input populations 3 and 4 plus three neutral pairs,
100 paired seeds, eight sites, fixed 2,000-step horizon. No stopping on success.
Configuration: `configs/constraint-ablation.json`.

### Procedure
Run `python -m rs_calc.constraint_lab --config configs/constraint-ablation.json
--output research/runs/constraint-ablation-v1` from the project directory (one line).
Archive source and manifest before trials. Log initial/final states, proposal and
accepted-state path hashes, charge occupancy, first capture, escape, terminal
readability, correctness, constraint rejections and cap interventions.

Correctness and signed charge are measured outside the kernel. Counts of steps
are not independent samples: intervals use trial-level terminal correctness.
Cells share random tapes, so between-cell comparisons are paired, not independent.
The apparatus does not call finite-horizon readability proof of convergence.

### Results
SC-023 completed: 800 trials, 100 per cell. Full C/G/R: 100/100 correct,
95% Wilson interval [0.9630, 1.0000], 100 distinct accepted-state trajectories,
mean first capture 189.57 proposals, zero observed escapes. C alone preserved
identity 100/100 but yielded zero readable terminal states. G and GR each produced
readable zero in 100/100 trials, always incorrect. CG preserved identity 100/100;
69 trials visited a readable correct state, but only one ended there, with 162
total escapes. C and CR each incurred 7,124 capacity rejections, so their behavior
is explicitly influenced by the resource boundary. These are not unbounded results.

Engineering pilot before SC-023: a test requiring every seeded `17 + 28` trial
to be readable within 2,000 proposals failed. That assertion confused invariance
with bounded-time completion. The corrected software test requires preserved
identity, correct readout whenever readable, and no escape after capture. The
SC-023 horizon and cells remain unchanged; larger-input censoring is a follow-up.

### Interpretation
The measured roles differ: C protects numeric identity, G removes ongoing birth
of neutral background, R stabilizes the supplied ready-state readout. Readability
is not truth: G/GR reliably settle on the wrong answer. Conversely unreadability
is not identity destruction: C preserves charge throughout. Predeclared
mathematical expectation: full C/G/R preserves
charge and makes `(population size, pending count)` lexicographically nonincreasing.
Opposite pairs or pending records always have a positive-probability reducing move
in global mode. In a bounded state space this implies almost-sure eventual normal
form, not a deterministic finite runtime bound. Rewiring can continue afterwards.

### Alternative explanations
Classical constrained Markov dynamics and terminating multiset rewriting are
sufficient candidate explanations. Union of the input populations supplies the
additive composition boundary; this experiment does not discover the meaning of +.

### RS relevance
Tests the sufficiency and distinct roles of general relational constraints. It does
not establish unique RS mechanisms, physical randomness, or physical ontology.

### Confidence
H11-H13 supported within this grammar and observer. Finite-sample rates are not
universal guarantees. Conditional invariant argument is separate from measured
finite-horizon capture rates. Analysis verified all 100 matched proposal tapes;
distinct accepted-state paths exclude noops and rejected RNG. Predeclaration here
means recorded locally before execution, not external registered preregistration.

### Follow-up experiments
The identity/readout separation motivates SC-024/025 below. Retain the cap-sensitive
C/CR results as data; do not treat removing a growth restriction as a matched
stationary-noise experiment. A subsequent cap sweep is still needed.

## SC-024: predeclared enforcement follow-up

### Question
Does rare violation of conservation destabilize otherwise persistent readouts?

### Hypothesis
H14: under ongoing proposals and G/R, a sharp-looking finite-horizon reliability
curve can arise from accumulated leakage rather than a phase transition. Initial
status: unsupported. Near-perfect rejection may still permit incorrect outcomes.

### Model
Same kernel, G/R enforced; each locally charge-changing proposal is rejected with
probability s. No target-dependent repair is available after a violation.

### Variables
s = 0.9, 0.99, 0.999, 0.9999, 1; 100 new paired seeds per cell, 2,000 proposals,
3 + 4 plus three neutral pairs. Selected after SC-023, before SC-024 results.

### Procedure
Run `configs/constraint-followups.json`; preserve successes, escapes and corruptions.
Correctness intervals use trials, not the correlated time samples. A prospective
upper bound on probability of *never losing charge*, not terminal correctness:
on a charge-preserving history with initial charge seven, state cannot be empty,
and death or flip changes charge. Thus survival is at most
`(1 - (1-s)/4)^2000`; same-sign cancellation adds additional failure opportunities.
This is an observer-side bound, not a kernel objective. Terminal correctness can
exceed survival because corruption may accidentally cancel later.

### Results
SC-024 completed: 500 trials. Correct terminal answers for s = 0.9, 0.99, 0.999,
0.9999, 1 were respectively 0, 0, 48, 95, 100 out of 100. At 0.999 the Wilson
interval is [0.3846, 0.5768]; at 0.9999 it is [0.8882, 0.9785]. Identity-surviving
counts happened to equal correct terminal counts in these samples. At 0.99,
59 trials visited a correct readable state but none retained it at the horizon;
74 ended as zero. Full enforcement independently replicated SC-023: 100 distinct
accepted-state paths, 100 correct answers, no escapes, mean capture 171.57 steps.
The predeclared survival upper bounds are approximately 1.02e-22, 0.00670, 0.60649,
0.95123 and 1. Observed survival fractions do not exceed these bounds; this is a
consistency check, not a fitted model or proof from finite samples.

### Interpretation
Ongoing rare violations accumulate; nearly complete enforcement need not imply
durable correctness. No empirical critical point is inferred from this horizon.
Post-result analytic deduction: with G enforced, population size cannot increase;
for every s < 1 a nonempty state has a fixed positive chance `(1-s)/8` of losing
a record to death on each proposal. Under ideal independent random draws it
therefore reaches empty zero almost surely eventually. Thus this model has a
precise long-time absorbing-state distinction at perfect enforcement, not evidence
of an unidentified physical phase transition. No target-aware repair restores
the original class. Finite-PRNG samples are evidence about the implementation;
the almost-sure statement belongs to its ideal stochastic model.

### Alternative explanations
Repeated independent proposal hazards plus state-dependent same-sign cancellation;
no new RS mechanism is needed to explain a steep curve.

### RS relevance
Separates durable identity from temporary readable capture under weakened constraint.

### Confidence
H14 supported for a horizon-specific leakage interpretation. Survival bound and
eventual-zero argument are conditional mathematics, not additional trial results.

### Follow-up experiments
Change horizon and proposal weights before claiming a universal strength threshold.

## SC-025: predeclared transfer and locality follow-up

### Question
Do the same constraints transfer to zero, negative and larger populations?

### Hypothesis
H15: full constraints preserve identity across inputs, but finite-time readability
degrades with population size and local cancellation restrictions. Initial status:
unsupported; informed by the documented engineering pilot, not a blind prediction.

### Model
Same full C/G/R kernel. Local variant permits cancellation only at a common target;
rewiring can still jump to any site, and selection/completion observation are global.
It is a local cancellation condition, NOT a wholly local architecture.

### Variables
Inputs [0,0], [3,-7], [17,28], [50,50]; global/local cancellation, 100 new paired
seeds per cell; unchanged 2,000-step horizon and capacity. Same seeds as SC-024,
independent of SC-023. Eight cells, not eight independent replications of one cell.

### Procedure
Run in `constraint-followups.json`; compare terminal charge, readability and censored
first-capture counts. No horizon extension for trials that fail to finish.

### Results
SC-025 completed: 800 trials. Every full-constraint trial preserved charge and
none escaped after correct capture. Terminal readable/correct counts:

| Inputs | Global cancellation | Local cancellation |
| --- | --- | --- |
| 0 + 0 | 100/100 | 100/100 |
| 3 + (-7) | 100/100 | 98/100 |
| 17 + 28 | 87/100 | 19/100 |
| 50 + 50 | 0/100 | 0/100 |

The 45 case has Wilson intervals [0.7902, 0.9224] global and [0.1251, 0.2778]
local. All incomplete cases retain the expected charge; they are not reported as
successful calculations. Zero still begins with three neutral pairs, so its
completion is not trivial empty-input observation. No capacity rejection occurred
in these full-constraint cells.

### Interpretation
H15 supported under these conditions. Same constraints transfer across number
classes, but random activation and sparse matching impose finite-time costs.
A correct charge without a readable result is not a completed calculation.
Conditional means of first capture exclude censored trials and must not be used
as unbiased mean completion-time estimates. The ready marker is a supplied readout
requirement; its random activation cost is partly a design choice, not an intrinsic
complexity bound for every relational arithmetic representation.

### Alternative explanations
Sparse matching and random activation costs are conventional explanations for delay.

### RS relevance
Tests population-independent constraints and locality costs without per-number rules.

### Confidence
Supported within the measured inputs/horizon. The pilot already showed larger-input
censoring; this was a fresh seed set, not an independent blind prediction of scaling.

### Follow-up experiments
Vary horizon, region count and cancellation proposal allocation; investigate local
completion detection separately from local rewrite admissibility.

## Audit and unresolved questions

The kernel imports only standard-library dataclasses, PRNG and iterator types. Its
transition function receives state, a proposal, general constraints and capacity;
not operands, an expected value, or an answer-valued objective. Conventional sums
in `constraint_lab.py` are explicitly the observer, never feedback to acceptance.
The source lint and exhaustive local predicate tests are checks, not a formal
proof of arbitrary future source versions. Seed replay checks reproducibility,
not physical randomness or theoretical independence of pseudorandom outputs.

The outcome is not hidden in a per-number constraint. It *is* implicit in the
input populations and supplied conservation law, as intended. Deterministic input
joining establishes additive composition; cancellation/readiness resolution occurs
through the random constrained proposals. This is not a discovery of addition
without a representation or a composition rule. R is needed for stable readability
under this observer, not for stability of the charge observable itself.

A post-hoc conventional explanation for CG: once opposite pairs disappear, the
seven readiness bits have symmetric ready/unready updates. Their ideal stationary
uniform distribution predicts all-ready occupancy `2^-7 = 1/128`. Observed
occupancy 0.005755 and terminal 1/100 do not establish that limit; a long-run,
initialization-matched test is still needed. No new RS implication is claimed
for this familiar finite-state mechanism.

Next priority: distinguish defect suppression from broader reversible stochastic
relaxation, sweep the population cap, vary readout maps and observation horizons,
then apply the same audit to multiplication's explicitly constructed pair registry.
No multiplication/division, higher-order, or T-C-R result is added by SC-023/025.
