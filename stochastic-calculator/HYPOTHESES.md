# Hypothesis register

Declared before SC-001. Status here is the initial status; dated updates follow
the initial table, preserving the distinction between expectation and observation.

| ID | Hypothesis | Initial status | Falsifier / discriminating test |
| --- | --- | --- | --- |
| H1 | Number identity can survive multiple relational microstates. | unsupported | Charge-preserving rewrites change the decoded result. |
| H2 | Stronger admissibility enforcement raises reliability under fixed noise. | unsupported | Replicated sweeps show no improvement; separate longer runtime from stronger enforcement. |
| H3 | Addition can resolve by conserved redistribution without a target oracle. | unsupported | An answer-valued helper or nonconserving rewrite is required. |
| H4 | Decimal carry can be implemented by transient coordination of relations. | unsupported | Receiver needs a precomputed carry or result. |
| H5 | Higher-order constraints improve coherence beyond first-order transport. | unsupported | Removing coordination has no material effect under matched faults. |
| H6 | Exact outputs coexist with distinct stochastic trajectories. | unsupported | Structural trajectories are identical after excluding random identifiers. |
| H7 | Structured covariance can stabilize a fluctuating aggregate. | unsupported | Neutral perturbations create net variance. |
| H8 | Conserved identity implies recovery from arbitrary damage. | unsupported | An erased unpaired relation changes the stable output. |
| H9 | A fully local architecture suffices for every operation. | unsupported | Product/partition/termination still require nonlocal information. |
| H10 | Constraint sweeps reveal a phase transition or physical probability well. | unsupported | Smooth fault filtering and absorbing rewrite classes explain the observations. |

No hypothesis is an ontological claim. Classical multiset rewriting, population
protocols and error-control mechanisms are explicit competing explanations.

## Update after SC-001

- H1: supported within the signed-population model (4,000 preserving trials).
- H8: contradicted in this model (0/1,800 recovery after nonzero single erasure).
- All other hypotheses remain at their initial status pending further experiments.

## Update after SC-022

| ID | Current status | Evidence and qualification |
| --- | --- | --- |
| H1 | strongly supported within model | SC-001/002/008; conservation class only, not arbitrary damage. |
| H2 | supported under explicit fault filtering | SC-003/006/022; conventional survival suffices. |
| H3 | supported within model | SC-004/007; addition implemented by redistribution of a conserved population. |
| H4 | supported as a constructed protocol | SC-012; radix ten and the T-C-R rule are supplied, not spontaneously learned. |
| H5 | inconclusive broadly | SC-014 shows replay-exclusion benefit; no matched first-order comparator. |
| H6 | strongly supported within model | SC-005 and fixed-initial SC-019. |
| H7 | strongly supported for designed covariance | SC-017; cancellation imposed by neutral pairing. |
| H8 | contradicted within model | SC-001/008: charge destruction not repaired. |
| H9 | inconclusive | SC-013 local cancellation works; multiplication, partition and completion remain globally orchestrated. |
| H10 | unsupported | SC-009/020/022: invariant classes, forced parity and survival explain results; no physical potential defined. |

These statuses do not increase confidence in the empirical correctness of RS.
