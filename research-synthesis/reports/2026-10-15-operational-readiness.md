# Operational readiness (2026-10-15)

**Epistemic status:** a dated report by an AI research assistant (Claude Opus 5.5) on the state of the synthesis infrastructure. Not experiment evidence; changes no programme record.

**Verdict:** **infrastructure-ready** (GO for a merge review); **not historically complete** (historical findings await the author's publication consent).

## Release gates

| Gate | Status | Evidence |
| --- | --- | --- |
| No change to CL/GT branches or frozen results | Pass | CL `e650d71`, GT `79fa6b0`, SC `aa06213` heads unchanged; the hub only reads pinned commits |
| Committed changes limited to the synthesis layer, root README and CI | Pass | `git diff origin/main...HEAD` outside `research-synthesis/`: `README.md`, `.github/workflows/research-synthesis.yml`; enforced by the scope guard |
| No historical bytes, code, recovered conversations or private inventories committed | Pass | Archives, inventories and the review packet stay outside the repository; only archive names, whole-file hashes, inventory digests and the ten already-public landmark paths appear |
| Accurate hashes and source anchors | Pass | Whole-file sha256 and member counts match; every file member matches the bundle's integrity manifest; `synth hist-verify` re-hashes cited members |
| All tests green | Pass | 97 standard-library tests; `synth check` OK; generation byte-identical across two runs; `synth smoke-cycle` 9/9 |
| Human publication policy applied without retroactive inference | Pass | No `publication_consent` decision exists, so nothing historical is published; AD-0002 is explicitly not consent (AD-0004) |
| Operational runbook and root link | Pass | `docs/runbook.md`, `docs/branch-integration.md`; root README links `generated/index.md` |
| No physics or ontology overclaim | Pass | Validator blocks physical terms in accepted records; the 508 plan is recorded as a plan |

## Counts

| Item | Count |
| --- | ---: |
| Source nodes read (CL, GT at pins) | 433 |
| Shared concepts | 13 |
| Cross-programme connections | 9 (all `human_accepted` through RT-0001/AD-0002: 3 `accepted_bounded`, 6 `qualified`) |
| Proposals | 50 (24 proposed, 16 under review, 8 rejected, 2 undetermined; 12 blocked on missing or unpublished sources) |
| Shared questions | 7 (6 open, 1 pending a source: XQ::05) |
| Metaphors | 6 `human_accepted` (non-evidentiary), 8 drafts, 19 links |
| Author decisions | AD-0001 (relation type), AD-0002 and AD-0003 (round-trip ratifications), AD-0004 (policy amendment) |
| Snapshots | 3 (all verified byte-for-byte) |
| Generated views | 43 files (themes in Markdown and Mermaid, `graph.json`) |

## Tested commands

`audit`, `validate`, `generate` (twice, identical), `check` (with and without `RS_HIST_ARCHIVE_DIR`), `snapshot`, `review`, `intake-seeds`, `round-close`, `ratify`, `hist-inventory`, `hist-verify`, `smoke-cycle`. `propose-pin` and `apply-pin` are covered by the test suite.

## Historical archives

| | `RS_Work_Research.zip` | `RS_Work_Round46_Supplement.zip` |
| --- | --- | --- |
| sha256 | `3ecfd22f…1e46` (match) | `630da2d9…4b5e` (match) |
| Members | 403 (match) | 9 (match) |
| File members matching the integrity manifest | 390 of 390 | 9 of 9 |
| Unsafe members | 0 | 0 |
| Inventory digest | `5773c58a…7c84` | `e522c13f…2a2d` |

- Ten landmark sources read; further priority sources read where the landmarks depend on them.
- Derived findings drafted and source-verified **privately** (member hashes and line anchors); **0 public** `HIST::` findings; HIST stays `pending_intake`.
- The 11 historically blocked records and XQ::05 stay blocked, each with a dated re-evaluation entry. Their privately staged assessments are with the author.
- Historical source verification is not numerical reproduction: nothing was recomputed.

## Scientific limits

- No derived physical gravity, time or quantum model.
- No established complete 600-plus experiment corpus.
- CL 008N and GT-P009 remain unreviewed rounds; links resting on them stay `qualified`.
- SC remains `catalogued_only` (no structured ledger).
- No ontology is promoted by metaphor or by historical interpretation.

## Branch integration contract (summary)

CL and GT remain authoritative. They may read a pinned hub commit as planning context and record which commit they consulted; they propose back through seeds after a closed round. The hub never writes to their branches, never cherry-picks into them and never follows a moved head without a reviewed pin. Full text: [`docs/branch-integration.md`](../docs/branch-integration.md).

## Known issues

- Materialised source copies are committed rather than read at view time (a partial conformance item, `docs/conformance-02-04.md`).
- Physical relevance is not tracked as a review axis (partial conformance item).
- RT-0001 was assembled retrospectively when the implicit-acceptance rule was introduced (audit note in AD-0004; AD-0002 not rewritten).
- Some proposal scripts serialise JSONL with different separators from the shared writer; content is identical (cosmetic).
- Commit `b08cf9a` failed the synthesis workflow (a test fixture clash), fixed in `1bfe179`.

## GO / NO-GO for merging into `main`

**GO for a merge review** if the author accepts:
1. the hub as context-only infrastructure, with CL/GT authority unchanged;
2. that historical content stays private until a `publication_consent` decision;
3. the known issues above.

**NO-GO** (do not merge) if any of these is required first: published historical findings; reviewed CL 008N or GT-P009 rounds; an SC structured ledger; closing the two partial conformance items.

Historical completeness is a separate milestone: it starts with the author's publication decision and a follow-up intake round.
