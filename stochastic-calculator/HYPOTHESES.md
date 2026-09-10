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

## Predeclared SC-023 hypotheses

Programming general constraints is legitimate in this research programme. Neither
that fact nor correctness under deterministic scheduling is evidence of cheating.
The prohibited shortcut is an answer oracle or hidden conventional expression
solver. The new proposal kernel does not receive operands or an expected answer.

| ID | Hypothesis | Initial status | Discriminating test |
| --- | --- | --- | --- |
| H11 | Conservation alone preserves identity but does not ensure stable readable output under ongoing proposals. | unsupported | Fixed-horizon C versus CGR ablation; observe charge and readability separately. |
| H12 | Conservation, non-growth, and irreversible readiness together yield stable normal forms under a fixed broad proposal grammar. | unsupported | All eight constraint combinations, same random tape, 100 seeds, 2,000 steps. |
| H13 | Removing conservation while retaining normalizing constraints can produce stable but incorrect outputs. | unsupported | GR ablation; log full terminal outcome distribution and charge violations. |

These tests use bounded, grammar-defined randomness, not literally unrestricted
randomness. The same constraints apply to every population. No per-number rule
or comparison with an expected sum occurs in proposal acceptance. Neutral pairs
are added at initialization to make cancellation and identity/readout separation
observable. The horizon is fixed in advance; first capture is not a stopping rule.

## SC-023 result and predeclared follow-ups

H11-H13: supported within the new grammar/observer (800 trials). See
`research/CONSTRAINT_LAB.md` for measurements and limitations.

- H14 (unsupported): accumulated conservation leakage can create a steep
  finite-horizon reliability curve without a phase transition. SC-024 tests five
  enforcement strengths, selected after SC-023 but before the follow-up run.
- H15 (unsupported): unchanged full constraints preserve identity across signed
  inputs and scale; timely readability degrades with size/local matching. SC-025
  uses fresh seeds; the earlier 17+28 engineering pilot is disclosed.

## Update after SC-025

- H11-H13 remain supported within the defined proposal grammar and readout.
  Conservation alone preserved charge, while GR alone settled incorrectly at zero.
- H14: supported for finite-horizon cumulative leakage; 0%, 0%, 48%, 95%, 100%
  accuracy at enforcement .9, .99, .999, .9999, 1 (100 seeds each). No empirical
  phase transition is established. A conditional eventual-zero argument is given
  separately from observations.
- H15: supported for the tested inputs. All 800 trials preserved identity; correct
  readable completion varied from 0 to 100/100 with scale and locality. The larger
  cases are horizon-censored, not successful calculations with an unreadable output.

Generalization to other proposal distributions, alternative readouts, topology-led
identities or the full operator suite remains untested by this extension.
