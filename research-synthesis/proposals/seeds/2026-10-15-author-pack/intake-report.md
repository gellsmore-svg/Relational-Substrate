# Seed intake report: author pack of 2026-10-15

*Intake by an AI research assistant (Claude Opus 5.5) on 2026-10-15, at the author's request. **Nothing here is reviewed or adopted.** All records are staged as `proposed` (claims) or `draft` (metaphors). No ledger file was changed by the intake.*

## Receipt

- **Archive:** `RS_Shared_Coherence_Implementation_Pack_2026-10-15.zip` (36,323 bytes; sha256 `e1f7d94d1666d834393d49dda3ebde96f4578ea8bd6e180a891f5f5edfcccdbd`; 13 files), from the author's Downloads folder.
  - Extracted into an isolated scratch directory with a path-traversal check.
  - Only the three seed files are stored here.
- **Stored verbatim in this directory**, byte-identical to the archive members:

| File | Bytes | sha256 |
| --- | --- | --- |
| `candidate-relations.jsonl` | 5,096 | `2a8784fe92a8970205852286c496dece45a4eca8b1d5936fbce093e8aaa45b4b` |
| `metaphors.jsonl` | 5,833 | `4a5bd422a3bde6e846398a67a758b7a3657afb917a86c6f5fa698f85c2eda6c7` |
| `source-manifest.json` | 4,138 | `1d0fa94b1d622aea1712bf134ef9012b65d91a60fd395e0744bd2cfd135d4f42` |

- **Machine receipt:** `receipt.json`.
- **Staged records:**
  - 8 seed claims in `proposals/candidate-relations.jsonl` (`kind: seed_claim`, ids `P::SYN-C001` to `P::SYN-C008`);
  - 7 draft metaphors in `proposals/metaphor-drafts.jsonl` (`M::META-…`).

  Each keeps its original record under `seed_record`.
- **Re-running the intake** adds nothing: the 15 ids are skipped.

## The seed source manifest against the current pins

| Source | Seed pin | Current pin | Reading |
| --- | --- | --- | --- |
| CL | `9b2f857` (8M closed; "8N status recheck required") | `e650d71` (8N closed) | The current pin is the later completed head the seed asked to recheck. **Not changed** |
| GT | `a73cd02` (GT-P008; "E5A/GT-P009 recheck required") | `79fa6b0` (GT-P009 closed) | Same. **Not changed** |
| SC | `aa06213` | `aa06213` | Identical |
| METHOD / OTR | `05b15b0` | `05b15b0` | Identical |
| HIST | 2 archives, 6 primary paths | pending | Archive names, sha256 and primary paths were recorded in `sources/pin-spec.json` as **expected, unverified** pointers. Neither archive was found locally (name search, 2026-10-15) |

**No drift in cited findings.** Every CL and GT finding cited by a seed claim (22 distinct ids) resolves at **both** pin sets. Each row is **byte-identical** between the seed pins and the current pins, so assessing the seeds at the current pins introduces no drift.

## Seed claims

**Relation-type mapping** (declared in `rssynth/ledger.py`, `SEED_RELATION_MAP`):

| Seed type | Shared connection type |
| --- | --- |
| `compatible_with` | `epistemic_compatibility` |
| `contrasts_with` | `explicit_contrast` |
| `qualifies` | `qualifies` |
| `candidate_mechanism_analogy` | `untested_hypothesis` (no formal comparison reviewed yet) |
| `shared_question`, `raises_shared_question` | none: these are questions, not connections |

| Claim | Theme | Proposed → mapped | Seed status | Sources | Relation to agent-drafted records |
| --- | --- | --- | --- | --- | --- |
| SYN-C001 | predictive sufficiency under projection | shared_question → none | blocked (historical primary) | CL F8H-NONLUMPABLE-MATERIAL-PROJECTION, CL F8M-H2-STATIONARY-H1-RESIDUAL, `HIST::rs_work_round11/findings.md` (pending) | New. Overlaps concept `C::predictive-sufficiency`; no agent connection |
| SYN-C002 | occupancy vs passage | compatible_with → epistemic_compatibility | candidate | CL F004, CL F8M-H2-STATIONARY-H1-RESIDUAL, GT F04-RETENTION-NOT-APPROACH | Same theme as X::0001 and X::0009, but **different evidence**. The agent links use CL F8N / CL-T88 against GT-F78 / GT-F79 (E5A); the seed uses GT-F04 (G0), which predates E5A |
| SYN-C003 | clock dependence | compatible_with → epistemic_compatibility | candidate | CL F003, GT F07, GT F69 | **Disagreement to resolve.** Agent review X::0003 classifies CL F003 against GT clock effects as an **explicit contrast**: CL's epoch hides events, while GT's clocks share one event sequence. The seed proposes compatibility. The two readings can coexist (compatible as a theme, different as operations), but the author should decide which relation type the ledger carries |
| SYN-C004 | relational topology and context | candidate_mechanism_analogy → untested_hypothesis | candidate | CL F8F-FIRST-PATH-SHAPE, CL F8C-PROJECTION-GEOMETRY, GT F64, GT F67 | Close to P::0004 (undetermined), which compared GT-F68 with CL F016. Both await a declared map between witness counts and gate literals |
| SYN-C005 | higher-order influence, not scalar strength | shared_question → none | blocked (historical primary) | CL F005, CL F007, GT F63, `HIST::…/RS_507_Integrated_Ledger.md` (pending) | New. Overlaps `C::higher-order-context` |
| SYN-C006 | historical memory vs initial memory | contrasts_with → explicit_contrast | candidate | CL F018, CL F8H-CURRENT-VS-INITIAL-MEMORY, CL F8M-HISTORY-ONLY-STRUCTURAL-SILENCE | **All three sources are CL**: a within-programme contrast, not a cross-programme one. Related to X::0007 (CL F018 with GT-F81) |
| SYN-C007 | evidence against attraction inference | qualifies → qualifies | candidate | GT F61, GT F62, GT F01 | **All three sources are GT**: a within-programme qualification. The point stands (raw gathering is density composition) |
| SYN-C008 | endogenous persistence not yet proven | raises_shared_question → none | blocked (historical primary) | GT Q19, GT F23, `HIST::…/RS_507_Integrated_Ledger.md` (pending) | The seed predates E5A and asks that E5A be reviewed against matched lifetime and turnover nulls. **E5A has since run:** GT-F74 to GT-F82 partly answer GT-Q19, and the agent's X::0007 and XQ::04 bear on it |

**Things to notice:**
- Three claims are blocked on historical primary sources that are not available. They are kept as proposals with their pending `HIST::` pointers.
- Two claims (SYN-C006, SYN-C007) cite a single programme. The shared layer can hold them, but they are not cross-programme bridges.

## Seed metaphors

Converted into the shared metaphor schema, with the original kept under `seed_record`:
- `maps` → mapping rows;
- `boundary` → "does not mean";
- `misleading_if` → misleading readings;
- `name` → title.

**Concept targets** map to shared concepts only where the meaning is the same (`SEED_CONCEPT_MAP` in `rssynth/workflow.py`).

| Metaphor | Mapped concepts | Unmapped seed targets | Nearest agent-drafted metaphor |
| --- | --- | --- | --- |
| META-MUSIC-SCORE | — | stochastic_actualisation, stable_macro_readout, microtrajectory_diversity | none (new territory) |
| META-MAP-JOURNEYS | C::occupancy-vs-process, C::predictive-sufficiency | process_words | M::two-towns (same concept) |
| META-SCAFFOLD-ARCH | — | externally_held_reference, endogenous_metastability, identity_through_turnover | none. It fits GT's held-vs-free distinction (E4/E5A) |
| META-BRAID | C::higher-order-context | structural_arrangement, interactions_not_just_scalar | none: the first metaphor for higher-order context |
| META-LOOKING-GLASS | — | observation_projection, observer_readout, information_loss | none |
| META-RIVER-DELTA | — | pattern_persistence, route_turnover, metastability | M::rotating-committee (persistence through turnover) |
| META-TWO-CLOCKS | C::clock-readout-dependence | event_rate_vs_occupation | M::minutes-and-moves (same concept) |

**Validation:**
- No metaphor raised a smuggling flag: each seed's `boundary` already disclaims metric, force or agency where its image suggests them.
- The 16 unmapped targets are listed in `generated/metaphor-gaps.md` as candidates for new concepts. **None was created.**

## Not done in this intake (needs review or a separate request)

- **No claim or metaphor was reviewed, promoted or merged** with agent records, including the SYN-C003 / X::0003 disagreement.
- **The other pack files are not applied yet:** `02_ARCHITECTURE_CONTRACT.md`, `03_DISCOVERY_RUBRIC.md`, `04_ACCEPTANCE_AND_REVIEW.md`, `05_HISTORICAL_INTAKE.md`, the background synthesis and the diagrams. The infrastructure was built from the 01 prompt alone. A conformance pass against 02–04, and registration of the background synthesis's claims, are the natural next steps.
