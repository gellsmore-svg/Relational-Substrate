# Acceptance list and test coverage

`04_ACCEPTANCE_AND_REVIEW.md` was **not supplied**. This list is the Stage H list of the 01 prompt, plus the requirements stated in its Stages B–G. Tests are in `tests/test_rssynth.py`: 49 tests, standard library only.

| Requirement (01 prompt) | Tests | Status |
| --- | --- | --- |
| Source lock and hash verification | `SourceLockAndHashes`: copies match sha256 and git blob ids; copies equal git objects at the pins; a tampered copy is detected; an edited manifest digest is detected | Implemented |
| Dangling and colliding namespaces; missing commits | `NamespacesAndCommits`: two default revisions collide; abbreviated commit rejected; reserved namespace rejected; same local id in two namespaces stays distinct; dangling and malformed references fail | Implemented |
| Forbidden implications (a metaphor cannot prove a finding; cosine cannot raise an epistemic level) | `ForbiddenImplications`: metaphor as evidence or endpoint refused; disjoint vocabularies; evidence fields refused on metaphor links; `evidentiary: false`; no scalar scores; discovery output not citable; smuggled force/pull needs a disclaimer; metaphors never change node status; discovery never writes the ledger or changes the graph | Implemented |
| Differing ancestry and stale sources | `AncestryStalenessAndRevisions`: shared lineage needs an independence note; a shared implementation assumption is never independent; the inherited CL copy on the GT branch is not counted; a moved branch is reported, not followed | Implemented |
| Alternate revisions, parallel branches, in-flight protection | A lineage-only revision is not ingested; `propose-pin` against an older or parallel CL commit (8M `9b2f857`) flags non-descent and removed rows; `apply-pin` requires a named human; an incompatible upstream schema stops; undeclared upstream fields are reported | Implemented |
| Idempotent regeneration and tamper detection | `RegenerationAndSnapshots`: two builds are equal and match the committed views; a hand-edited view is detected; snapshots are immutable and tamper-evident | Implemented |
| Negative, null and contradictory relations preserved | `NegativeAndContradictoryPreservation`: rejected and undetermined proposals keep their rationale; contrasts, rejections and programme negative findings appear in the contradictions view | Implemented |
| Graph view coverage, scale and readability | `ViewsCoverageAndReadability`: a theme page per concept; the front page links every view; statuses in text; Mermaid edge counts bounded; absent sources marked absent from the local tree; separate edge families in `graph.json` | Implemented |
| Frozen experiment, book and ledger non-mutation | `NonMutationOfResearchRecords`: the branch diff against `origin/main` touches only `research-synthesis/` and its workflow; generation writes only under `generated/` | Implemented |
| Review workflow; no unreviewed promotion | `ReviewAndHistoricalIntake`: promotion refused for an incomplete evidential comparison; human acceptance needs a named human | Implemented |
| Historical intake | Historical claims cannot be accepted before intake; pending pointers are allowed only in unresolved records | Implemented as a guard; **intake itself pending** (archives and procedure not supplied) |
| Seed intake | Author seeds are staged as unapproved proposals only | Implemented; **author seeds not supplied** |
| Discovery: reproducible, dominance-controlled, false positives in tests | `DiscoveryBehaviour`: a boilerplate false positive ranks first and is not promoted; per-node and near-duplicate caps hold; reviewed links can have zero similarity | Implemented (TF-IDF baseline; no embedding model) |

## Not covered, or only partly covered

- **The `03_DISCOVERY_RUBRIC.md` dimensions.** These are unknown, because the file was not supplied. Discovery tags only the eight comparison dimensions of the 01 prompt, as `mentioned_both`, `mentioned_one_side` or `unknown`.
- **Requirements unique to `02_ARCHITECTURE_CONTRACT.md` or `04_ACCEPTANCE_AND_REVIEW.md`** cannot be checked until those files are supplied.
