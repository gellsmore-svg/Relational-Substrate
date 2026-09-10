# Research notebook

SC-001 below was recorded before arithmetic implementation. Subsequent experiments
and revisions are recorded in [the continuation notebook](research/NOTEBOOK.md).
All measured tables, intervals and figures are in [RESULTS.md](research/analysis/RESULTS.md).

## SC-001 - Stable stochastic number identity

### Question
Can identities 0-9 survive microscopic reorganisation without retaining a template?

### Hypothesis
H1 predicts preservation under charge-preserving perturbations. H8 tests the
stronger, adversarial claim that conservation also repairs actual information loss.

### Model
Oriented relation populations; random incidence replacement, stochastic routing
and opposite-polarity cancellation. Number identity is signed excess. Decoder
requires a single-polarity output normal form. No target enters the dynamics.

### Variables
Ten identities, three perturbation modes, 200 independent seeded trials per cell;
8 regions, 6 neutral pairs, full enforcement, 10,000-transition budget.

### Procedure
Declared in `configs/foundation.json` before execution. Ran
`python3 -m rs_calc.foundation --output research/runs/sc001-foundation` before
implementing arithmetic. Every trial has initial/final states and its seed.

### Results
6,000 trials completed. Rewiring: 2,000/2,000 correct. Neutral injection:
2,000/2,000 correct. Single-relation erasure: 0/1,800 correct for identities 1-9;
200/200 for zero, where nothing was erased. Every trial reached a normal form.
For each 200/200 cell the 95% Wilson interval is approximately [0.9812, 1].
For each 0/200 cell it is approximately [0, 0.0188]. These are per-cell intervals,
not simultaneous confidence bounds or universal probabilities.

Identity 1 produced 63 distinct final incidence structures after rewiring and 62
after neutral disturbance; identities 3-9 produced 200/200 distinct structures in
both conditions. Instance IDs and list order are excluded from these hashes.
Zero always has one final normal form; its disturbed pre-normal states can differ.

### Interpretation
There is real microscopic diversity within preserved classes, conditional on an
imposed signed invariant. Normalization removes neutral defects. Information loss
moves the state into another class and cannot be repaired by these rules.

### Alternative explanations
This is standard signed-multiset conservation and cancellation. The graph's
incidence is not necessary for the global numerical invariant. It does not establish
a relations-first ontology or a novel error-correction principle.

### RS relevance
An inspectable example of identity independent of a microscopic template. The
negative control requires separating identity preservation from identity recovery
after invariant destruction. This sharpens terminology, not physical theory.

### Confidence
High for these finite trials; the invariant also supplies a conditional proof.
No confidence claim about physical substrates follows.

### Follow-up experiments
Proceed with conservation-based addition (SC-004), trajectory replication (SC-005),
and fault-admission sweeps (SC-003/006). Retain erasure failure. Introduce product
and partition coordination only after the addition mechanism passes its audit.
