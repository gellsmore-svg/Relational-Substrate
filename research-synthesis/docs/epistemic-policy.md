# Epistemic policy

## Layers are kept apart

| Layer | Example | May support a scientific claim? |
| --- | --- | --- |
| Source finding (`OBSERVATION`, `INFERENCE`, `METHODOLOGICAL`) | `GT::GT-F78-…` | Within its programme's scope, as that programme states it |
| Formal claim | `CL::CL-T88` | Under its stated assumptions |
| Source interpretation (`RS_GLOBAL_COHERENCE_INTERPRETATION`) | `CL::F-RS-SEPARATION` | No. It is a model interpretation, not a physical finding |
| Cross-programme connection | `X::0001` | Only as typed, scoped and reviewed; never beyond its endpoints' scopes |
| Open question | `XQ::01`, `GT::GT-Q21-…` | No |
| Metaphor | `M::two-towns` | **Never** |
| Retrieval similarity | `proposals/discovery-diagnostics.json` | **Never** |

## Rules enforced by the validator

1. **Endpoints must resolve** in a pinned, ingested source (or in the shared records). Missing or pending sources (`EXT`, `HIST`) may appear only in unresolved records: proposals that are proposed, under review or undetermined, and questions marked `pending_source`.
2. **Evidential types need full comparisons.** An evidential type (`exact_theorem_correspondence`, `tested_structural_analogy`, `common_definition`), once promoted, needs a definite verdict on all eight comparison dimensions. It cannot rest on a catalogued-only document.
3. **Independence must be stated.**
   - Endpoints from sources that share lineage cannot be declared `independent` without an `independence_note`.
   - `shared_implementation_assumption` is never independent.
4. **Promotion needs a written review.** `agent_reviewed` and `human_accepted` need a review record that exists. `human_accepted` needs a named human. Historical claims cannot be accepted before intake.
5. **No scalar scores.** Shared records carry no score fields (score, confidence, probability, similarity, cosine, …).
6. **Metaphors are not evidence.**
   - A metaphor cannot be cited as evidence or used as a connection endpoint.
   - Metaphor links use their own vocabulary and cannot carry evidence fields.
   - Metaphors must set `evidentiary: false`.
   - Words implying metric, place, agency or force (distance, space, force, push, pull, wants, decides, travels, attracts, gravity, …) must be disclaimed in `does_not_mean` if used.
7. **Rejections keep their rationale.** Rejected and undetermined proposals keep a `decision_rationale`; silence is not evidence.
8. **Status is not upgraded by association.** The graph projection derives every node's status from its source or review record only. Adding metaphors or similarity scores never changes a status (tested).

## What a connection does and does not say

- **A `tested_structural_analogy`** says:
  - a declared map takes one programme's formal objects to the other's;
  - the corresponding statements were checked on each side, within the stated scope.

  It does not say the mechanisms are the same.
- **An `epistemic_compatibility`** says the claims can both hold. It asserts no shared mechanism.
- **An `explicit_contrast`** says the claims differ in a stated, checkable way. Several apparent contradictions dissolve into contrasts once their scopes are compared (X::0004).

## Interpretation boundary

None of these records is evidence about physical space, time, gravity or theology. Both programmes keep those layers separate, and this layer inherits that separation.
