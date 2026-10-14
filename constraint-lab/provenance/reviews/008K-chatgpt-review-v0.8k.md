# External Review 008K: predictive-state synthesis

Supplied external review, recorded first for Prompt 008L.
Target branch: research/constraint-lab-v0.8k-predictive-state-synthesis.
Reviewed head: e81e7d5f67fa00f1d629f8bd4b365352d25c9eb1.

## Scope inspected

- Additive eleven-commit chronology and non-experimental synthesis discipline.
- Exact final-head CI.
- State taxonomy and coarsest strong predictive refinement.
- Observation-coarsening monotonicity and induced quotient commutation.
- Strong versus trace equivalence and weak/stationary distinctions.
- Synchronization versus Markov order.
- Finite-history augmentation and finite constraint-state flattening.
- Support-preserving grammar obstruction, compiler classes and novelty taxonomy.
- H/L boundary and branch reconciliation.
- Recorded H-question status correction and H2 recommendation.

## Verdict

**Generation 8K passes formal, technical, provenance, and coherence review.
No rerun required.**

Eleven commits ahead of predictive-state Generation 8I.
Final-head Actions run 38622307127 succeeded on exact closing head
e81e7d5f67fa00f1d629f8bd4b365352d25c9eb1, both constraint-lab and books.
Local full suite: 395 passed.
No 8K scientific experiment was opened. No 8K scientific freeze was required.

## Preserved formal results

CL-T60: strong predictive refinement is monotone under deterministic observation
coarsening. CL-T61: nested strong partitions induce commuting quotients.
CL-T62: strong-block equality implies observed future-word equality; converse
fails generally. CL-T63: finite worst-case synchronization bounds observed order.
CL-T64/T65: closed finite history/constraint state admits an augmented Markov
kernel. CL-T66: flattening does not remove preserved support obstructions.
CL-T67: stationary one/two-time matching does not imply path equivalence.
CL-M04: axis novelty is compiler-relative. CL-M05: explanatory compression is
prediction/equivalence scoped.

Finite closed H and eta both flatten at raw kernel level; novelty must declare
represented state, support, clock, observation, compiler class, K/J/alphabet,
equivalence and initial-law quantifier. H2 is recommended because same X and
same h1 can be held fixed while h2 differs. This is not absolute non-Markovianity.

## Canonicality and coherence

Canonical ancestry: 8H -> predictive-state 8I -> 8K -> 8L.
Alternate role-grammar 8I and coarse-process 8J remain separate, not merged or
cherry-picked. No actual shared namespace collision was found at pinned heads.

8K closes with 160 findings and 235 relations.
Q-H-MINIMAL-STATE and Q-H-COARSE-GRAINING were changed unresolved->qualified
with explicit transition records, without closing broad questions.
Q-H2-LAST-PAIR-COMPILER asks about structural usefulness beyond an engineered
record after the fixed-(X,h1) boundary is met. 8L addresses that capability
boundary, not necessarily the broader utility question.

## Review testimony versus verification

This file records the supplied external verdict; it does not impersonate a new
independent review. Historical 8I exposure and its literal pre-freeze regression
exception remain preserved in the reviewed 8K record.
