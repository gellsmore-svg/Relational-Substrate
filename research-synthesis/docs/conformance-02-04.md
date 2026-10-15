# Conformance pass against the author pack: 02, 03, 04 (2026-10-15)

The infrastructure was first built from `01_AGENT_IMPLEMENTATION_PROMPT.md` alone. The rest of the pack arrived later as `RS_Shared_Coherence_Implementation_Pack_2026-10-15.zip` (sha256 `e1f7d94d…cdbd`). This pass checks every requirement of:
- `02_ARCHITECTURE_CONTRACT.md`;
- `03_DISCOVERY_RUBRIC.md`;
- `04_ACCEPTANCE_AND_REVIEW.md`.

**Status key:**
- **met**: implemented and tested;
- **met (changed)**: required a change in this pass;
- **partial**: met with a stated limitation;
- **n/a**: not applicable.

Tests are in `tests/test_rssynth.py`: 65 in total, of which `Conformance0204` covers this pass. Each test is named in the evidence column.

## 02: architecture contract

| Requirement | Status | Evidence |
| --- | --- | --- |
| Programmes own their ledgers; the shared layer owns only pointers, cross-programme relations, questions, metaphors and views; no copied canonical lines in an independently editable ledger | partial | Ledgers are read at pins. `sources/materialised/` holds byte-identical copies used as a **read-only cache**: each is verified against its sha256 and against the git blob at the pin, and `check` fails on any edit. They are not a ledger; nothing writes to them except `synth pin`. The contract also allows reading at view time, without a committed cache. A committed cache was kept so that CI and offline checks work. Tests: `test_tampered_copy_is_detected`, `test_copies_equal_git_objects_at_the_pins` |
| The shared layer owns **cross-programme** relations only | met (changed) | A ledger connection with both endpoints in one programme is refused. Proposals with both endpoints in one programme must be marked `within_programme`: they are upstream suggestions for that programme's ledger and can never be promoted. Test: `test_within_programme_relations_never_enter_the_shared_ledger` |
| No universal scalar confidence; keep magnitude, robustness, temporal character, layer, role and significance distinct | met | The validator refuses score fields. Upstream dimensions pass through untouched. Review-vector axes are never summed. Tests: `test_scalar_scores_are_refused`, `test_review_vector_has_nine_unsummed_axes` |
| Namespaced ids `CL::`, `GT::`, `SC::`, `HIST::` | met | `core.parse_ref`, resolver and collision checks (`NamespacesAndCommits`) |
| Source refs carry commit, path, schema version and sha256 | met (changed) | Per artifact: path, sha256, git blob. Per source: `reviewed_source_commit` and `source_schema` (validator git blob). Graph nodes carry `source_commit`. Shown in `generated/provenance.md` |
| Distinguish the reviewed source commit from the observed moving branch head | met (changed) | `reviewed_source_commit` in the manifest, and `reviewed_source_commits` on every connection. Moving heads are reported by `audit` and `check` (staleness) and never substituted. A connection reviewed against an older pin raises a re-review warning (`ledger.stale_reviews`) |
| A historical archive is unresolved until its bytes are present and match the intake manifest; a citation in a synthesis is not evidence | met | `HIST` is `pending_intake` with expected archive sha256 (from the seed manifest) recorded as unverified. `EXT` (the synthesis) is `external_stored`, and its references resolve as pending. Tests: `test_historical_claims_cannot_be_accepted_before_intake`, `test_unresolved_sources_stay_blocked` |
| A coherent shared relation schema, with status transitions and **append-only decision history** | met (changed) | `decision_history` on every connection and proposal. Allowed transitions are in `core.STATUS_TRANSITIONS`. The last entry must equal the current state. `check` compares with the committed version and fails if any history was rewritten or deleted. `review` appends and never overwrites. Tests: `test_decision_history_is_append_only_and_transitions_are_checked`, `test_false_positive_seed_is_rejected_and_unresolved_seed_stays_unresolved` |
| Fields such as epistemic basis, counterevidence and dependence notes | met (changed) | `epistemic_basis` (formal, observed, interpretive, methodological, question), `counterevidence_refs`, `independence` + `independence_note`, `alternatives`, `falsifiers`. The field mapping is in `docs/crosswalk.md` |
| Suggested relation labels; do not silently equate same-named upstream words | met (changed) | `refines`, `fails_under_projection` and `requires_scope_alignment` were added. The other labels are mapped in `docs/crosswalk.md`. Shared types are validated separately from upstream relation types and never merged with upstream edges |
| Dimensions must not collapse (proof, exact numerical, stochastic estimate, post hoc, interpretation, metaphor) | met | Upstream epistemic layers are kept. `review_vector.evidence_status.status` takes one of theorem, numerical_exact, monte_carlo_estimate, qualitative_report, post_hoc_exploratory, unexecuted_plan. Metaphors are a separate, non-evidentiary layer |
| Track source review quality, independence, matched controls, projection/clock robustness and physical relevance separately | partial | Source review quality: `unreviewed_generations` caps decisions. Independence, controls, and scope or clock: separate fields and review-vector axes. **Physical relevance is not an axis**: physical claims are excluded outright by the overreach guard (`test_accepted_records_cannot_claim_physics`) |
| Adapter validates each programme's schema; indexes are transient or derived | met | `coherence_ledger_v1` reads each pin's own vocabulary from its validator (via `ast`, never executed) |
| No frozen round changed; isolated branch; no cherry-picks; validator code is not run from active branches | met | `test_branch_changes_only_the_shared_layer`. The validator is parsed, not executed |
| Views: `index.md`, `provenance.md`, `themes/*.md` + `themes/*.mmd`, `contradictions.md`, `nulls.md`, `questions.md`, `metaphor-coverage.md`, `metaphor-links.mmd`, `metaphor-gaps.md`, and a lossless `graph.json` | met (changed) | All are generated. `graph.json` now carries every shared record (with review vectors and histories), the source manifest, and node-level pins and round-review state. Tests: `test_required_view_names`, `test_graph_json_is_lossless` |
| Updating policy: milestone-triggered; auto-detection never approves; maintenance detects staleness only | met | `docs/cadence.md`; `propose-pin`, `apply-pin` (named human); `update-candidates` writes diagnostics only |
| v1 without a graph database, hosted vector store or custom front end | met | Standard-library Python, JSONL, Markdown and Mermaid |

## 03: discovery rubric

| Requirement | Status | Evidence |
| --- | --- | --- |
| Similarity is a discovery aid; record tokens, normalisation, model, documents, filtering, duplicate handling and seed | met (changed) | `proposals/discovery-diagnostics.json` records the method, declared synonym table, document selection, duplicate handling, `seed: null` and `deterministic: true`. No embedding model is used |
| Synonym or terminology mapping without assuming a shared ontology | met (changed) | `discover.SYNONYMS`, labelled as retrieval normalisation only |
| A review vector with nine independent axes per candidate pair, not summed | met (changed) | `review_vector` on every reviewed record. Candidates carry the vector with only `semantic_resemblance` filled; the other axes stay `unknown` |
| Low similarity must not veto, high similarity must not promote | met | Calibration in diagnostics: 3 of 9 reviewed links have zero similarity, and the top candidate is a rejected boilerplate false positive (P::0008). Tests: `test_reviewed_links_can_have_zero_similarity`, `test_discovery_never_writes_the_ledger_or_raises_status` |
| Decision categories `accepted_formal`, `accepted_bounded`, `qualified`, `candidate`, `rejected`, `blocked_missing_source` | met (changed) | `decision_category` on every record, kept separate from review authority (`review_status`). Current agent recommendations: X::0003, X::0004 and X::0005 are `accepted_bounded`; the others are `qualified`, because they rest on unreviewed rounds or are limited |
| Keep decision history and counterevidence; rejections are valuable | met | Append-only history. Rejected proposals keep their rationale (`test_rejected_and_undetermined_keep_rationale`) |
| False-attractor controls (six named pairs) | met (changed) | P::FA-01 (basin vs gravity), FA-02 (retention vs reconstruction), FA-03 (stationary match vs path law), FA-04 (graph class vs higher-order role) and FA-05 (current-history efficacy vs initial memory) are rejected with counterevidence. The sixth (metaphor coverage vs corroboration) is enforced structurally. Tests: `test_false_attractors_are_recorded_rejected_and_cannot_be_promoted`, `test_metaphor_coverage_is_not_corroboration` |
| Prefer about 15 auditable proposals with counterexamples over many unreviewed edges | met | 21 proposals: 8 agent, 5 false-attractor, 8 author seeds. 9 reviewed connections |

## 04: acceptance list

| Item | Status | Evidence |
| --- | --- | --- |
| Isolated branch from verified `main`; no writes to CL/GT branches | met | `audits/2026-10-15-starting-audit.md`; `test_branch_changes_only_the_shared_layer` |
| Changes confined to `research-synthesis/` plus justified CI | met | One added workflow, `.github/workflows/research-synthesis.yml`; `audits/2026-10-15-change-record.md` |
| Pins include SHA, path, namespace and read status; moving heads refreshed but not substituted | met | Manifest; staleness (`test_stale_branch_is_reported_not_followed`) |
| Mismatch, missing commit, missing file, missing digest or changed schema fail with an actionable diagnostic | met (changed) | An unreachable commit is now an **error** that names the fix (`test_unreachable_pin_fails_with_actionable_diagnostic`). Also covered: tamper, path missing at pin, missing digest, incompatible schema (`test_incompatible_upstream_schema_stops`), undeclared fields |
| GT's ancestry from CL 8G handled without fabricating CL 8M/N on that branch | met | Lineage edges. The GT branch's CL copy is excluded (`test_inherited_cl_copy_on_gt_branch_is_not_counted`) |
| Adopted closed-round evidence distinguished from unreviewed 8N/E5 results | met (changed) | `unreviewed_generations`: CL `008N` (no review recorded after External Review 008M) and GT `GT-P009`. Graph nodes carry `unreviewed_round`. `links.md` marks affected links. Such links cannot be `accepted_*` (`test_unreviewed_rounds_cap_the_decision`) |
| Deterministic, byte-identical regeneration | met | `test_regeneration_is_idempotent_and_matches_committed_views` |
| No id collisions after namespacing | met | `NamespacesAndCommits` |
| No dangling edges in the accepted view; unresolved proposal references staged and visible in diagnostics | met (changed) | The validator resolves every ledger reference. `candidate-bridges.md` has a "Review diagnostics: unresolved references" section (`test_required_view_names`) |
| Observation, theorem, interpretation, question and metaphor distinctly typed | met | Node kinds and layers; separate edge families in `graph.json` |
| Proof or review links need named evidence and scope; analogues cannot silently become equivalences | met | Evidential types need eight-dimension verdicts, a review record, a reviewer, scope and rationale. The seed `candidate_mechanism_analogy` maps to `untested_hypothesis` |
| Shared ancestry represented, so common-kernel findings are not independent confirmations | met | `lineage_shared`, the independence rule, and X::0005 (`shared_implementation_assumption`) |
| Negative, null, superseded and qualified findings navigable | met | `nulls.md`, `contradictions.md` |
| A false-positive seed is rejected; an unresolved seed stays unresolved | met (changed) | `test_false_positive_seed_is_rejected_and_unresolved_seed_stays_unresolved`. The real author seeds are staged unreviewed; three are `blocked_missing_source` |
| No overall score fields; no promotion from cosine or metaphor coverage | met | `ForbiddenImplications`, `Conformance0204` |
| Metaphors state audience, coverage, mapping, useful scope and failed implications | met (changed) | `useful_scope` is now required for reviewed metaphors (`test_metaphors_need_useful_scope`). Author seed drafts lack it and are flagged in `metaphor-gaps.md` |
| One-to-many and many-to-many coverage; complement, bridge and conflict edges | met | Metaphor links (`metaphor-overlap.md`) |
| A metaphor-origin relation never counts as support | met | `test_metaphor_cannot_be_cited_as_evidence`, `…_endpoint`, `…_link_cannot_carry_evidence_fields` |
| Multiple metaphors do not increase evidence counts | met (changed) | `test_metaphor_coverage_is_not_corroboration`. No evidence counts exist on nodes |
| Reports show concepts lacking metaphors, and metaphors that overreach | met (changed) | `metaphor-gaps.md`: concepts without coverage, unmapped seed targets, draft flags, and an overreach section |
| Historical archives not copied; historical claims need verified bytes, otherwise `blocked_missing_source` | met | `HIST` pending; seed claims citing HIST are `blocked_missing_source` |
| Earlier synthesis labelled exploratory; its cosines labelled retrieval measures | met (changed) | Stored verbatim as `reports/external-2026-10-15-cross-research-synthesis.md`, and labelled in `reports/README.md` and in the manifest note |
| At least one prominent unresolved question and one contradiction or limitation in the views | met (changed) | "Headlines" on `index.md`: XQ::01; X::0004; author decisions (AD-0001 settled SYN-C003 as an explicit contrast); the unreviewed-round limitation |
| No derived physics or ontology extension shown as a confirmed record | met (changed) | The overreach guard on accepted records. FA-01 records the gravity reading as rejected |
| Commands documented; fast CI; diff and provenance; draft PR left unmerged; completion report; no new experiments or book edits | met | README; workflow; change record; PR #8 (draft) |

## Remaining limitations

- **Committed cache.** The materialised copies are committed. They are a verified read-only cache, but a committed one; see the first 02 row.
- **Physical relevance.** It is excluded rather than tracked as an axis.
- **Agent recommendations only.** Every decision category is an agent recommendation (`agent_reviewed`). None is human-accepted.
