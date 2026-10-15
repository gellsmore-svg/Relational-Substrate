# Crosswalk: relation labels and fields

Labels from the architecture contract (02) and the author seeds, set against the shared vocabulary in `rssynth/core.py`.
- **Meanings are not equated by name.** Each row states the semantics the validator enforces.
- **Shared types are never merged with upstream programme relation types.** Upstream types (for example `qualifies` or `refines` inside a CL or GT ledger) relate findings within one programme, under that programme's validator. The shared types relate records across programmes.

## Relation labels

| 02 / seed label | Shared type | Semantics enforced here |
| --- | --- | --- |
| `compatible_with` | `epistemic_compatibility` | Both claims can hold; no shared mechanism asserted |
| `shares_formal_mechanism_with` | `exact_theorem_correspondence` or `tested_structural_analogy` | Split by verification: the same statement under explicit maps, or a declared map checked on both sides. Both need eight-dimension verdicts when promoted |
| `contrasts_with` | `explicit_contrast` | The claims differ in a stated, checkable way |
| `depends_on_same_kernel` | `shared_implementation_assumption` | Common code, kernel or validator lineage. Never independent |
| `refines` | `refines` | One claim narrows or sharpens the other within the same scope |
| `qualifies` | `qualifies` | One claim limits the scope of the other (directed) |
| `fails_under_projection` | `fails_under_projection` | Holds on the full state but not under a declared projection |
| `requires_scope_alignment` | `requires_scope_alignment` | Not comparable until state, clock, projection and horizon are aligned |
| `raises_shared_question`, `shared_question` | none: a shared question (`XQ::`) | Questions are not connections |
| `candidate_mechanism_analogy` (seed) | `untested_hypothesis` | No formal comparison has been reviewed yet |

## Relation fields (02 example against the shared schema)

| 02 field | Shared field |
| --- | --- |
| `relation_id` | `connection_id` (`X::NNNN`); proposals use `proposal_id` (`P::…`) |
| `from_ref`, `to_ref` | `from`, `to` (namespaced; seed claims keep multi-source `sources`) |
| `relation_type` | `connection_type` |
| `proposition` | `rationale` (seed claims: `claim`) |
| `scope{state, clock, observations, interventions, horizon}` | `scope` (text) plus `comparison` with verdicts on state, transition_law, support, clock, projection, intervention, horizon and conditioning |
| `status` | `review_status` (who reviewed) plus `decision_category` (rubric 03) |
| `epistemic_basis` | `epistemic_basis` |
| `evidence_refs`, `counterevidence_refs` | same names |
| `dependence_notes` | `independence` + `independence_note` |
| `alternatives` | `alternatives` |
| `falsifier` | `falsifiers` (a list) |
| `review{decision, reviewed_at, rationale}` | `review` (reviewer, date, record) plus append-only `decision_history` |
