# Reports

Dated syntheses, each with its epistemic status.

| Report | Status |
| --- | --- |
| [2026-10-15-initial-federation.md](2026-10-15-initial-federation.md) | Agent interpretation; not human-accepted; not evidence |
| [external-2026-10-15-cross-research-synthesis.md](external-2026-10-15-cross-research-synthesis.md) | **External, exploratory.** Stored verbatim from the author pack (sha256 `1c817747…bc09`). In its own words it is an "exploratory evidence synthesis, not an independent physical validation". **Its cosine scores are lexical retrieval measures, not evidence.** Its historical claims point into private archives that are not available (`HIST`, pending), so they are secondary and unverified here. It is a dated interpretation, not independent experiment evidence |

The external synthesis is registered as source `EXT-SYNTH-20261015` (`external_stored`).
- **Claims.** Its 22 substantive claims are registered as unapproved proposals `P::EXT-C01` to `P::EXT-C22` (`kind: external_claim`), by `proposals/register_external_claims.py`. Each keeps a verbatim quote (validated against the stored file), its section, what it cites and its own assessment.
- **Mapping.** The mapping of citations to pinned ids is the agent's (`source_mapping: agent`).
- **Blocked claims.** 7 claims rest on private historical archives and are `blocked_missing_source`.
- **Unresolved citations.** Two kinds are recorded rather than forced: the CL "Generation 2 census" has no pinned ledger record, and Work 45 and the 508A/B records have no primary paths.
- **Drift.** Every cited finding that existed when the synthesis was written (CL 8M `9b2f857`, GT `2bd18c6`) is byte-identical at the current pins.
- **Not registered.** The study priorities (§11) and the narrative recommendation (§12) are recommendations, not claims.
- **Review.** Question XQ::06 tracks the review of these claims.
- **Restatement** (`proposals/restate_external_claims.py`). The 15 claims not blocked on archives were each checked against pinned records:
  - outcomes: 11 verified, 1 partially verified (EXT-C09: no CL Generation 2 record), 2 consistent, and 1 superseded in context (EXT-C22, written before E5A);
  - each check is recorded as an appended `under_review` history entry; one claim (EXT-C19, an interpretive map) has no pairwise form;
  - 3 cross-programme pairwise proposals were created: `P::EXT-C08-R1` (SC-026 as an instance of readout dependence), `P::EXT-C09-R1` (CL-T01 with GT-F51) and `P::EXT-C20-R1` (CL-T59 strong lumpings refine the prospective equivalence; untested, with a proof sketch);
  - 4 within-programme relations are recorded as upstream suggestions, which can never enter the shared ledger: `P::EXT-C06-U1`, `P::EXT-C10-U1`, `P::EXT-C16-U1` and `P::EXT-C16-U2`;
  - 6 claims were already related in the programmes' own ledgers (CL R8M-011, R8M-013, R-8H-HISTORY-19; GT R86, R127, R128, R129), and those relations are cited, not duplicated.
