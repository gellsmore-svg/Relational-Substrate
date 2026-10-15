# Candidate bridges (proposals)

Staged in `proposals/`; none is in the ledger. Status is shown in text.

| Id | Type | From | To | Status | Origin |
| --- | --- | --- | --- | --- | --- |
| P::0001 | exact_theorem_correspondence | `CL::F003-CLOCK-SPLIT` | `GT::GT-F69-CLOCK-SEPARATED-SORTING` | REJECTED | agent_drafted |
| P::0002 | explicit_contrast | `CL::F001-PAIRWISE-RISE` | `GT::GT-F12-SINGLE-WITNESS-REVERSIBLE` | REJECTED | agent_drafted |
| P::0003 | untested_hypothesis | `GT::GT-F67-FLOOR-IS-AN-EXACT-ODDS-LEVER` | `CL::CL-T18` | PROPOSED (unreviewed) | agent_drafted |
| P::0004 | tested_structural_analogy | `GT::GT-F68-FIRST-ORDER-SORTING-INDEX` | `CL::F016-CURRENT-SLOT-INFORMATION` | UNDETERMINED | agent_drafted |
| P::0005 | untested_hypothesis | `HIST::505-507` | `C::occupancy-vs-process` | PROPOSED (unreviewed) | agent_drafted |
| P::0006 | untested_hypothesis | `EXT::2026-10-15-cross-research-synthesis` | `C::predictive-sufficiency` | PROPOSED (unreviewed) | agent_drafted |
| P::0007 | untested_hypothesis | `GT::GT-F80-CLOSEW-CLOSURE-RECOVERY` | `CL::Q-H2-CONTROLLED-PASSAGE` | UNDETERMINED | agent_drafted |
| P::0008 | common_definition | `CL::CL-F05` | `GT::GT-F82-E5A-COMPARATOR-AND-NUMERICAL-QUALIFICATIONS` | REJECTED | discovery_candidate |

## Retrieval diagnostics (not evidence)

TF-IDF cosine between statement texts. A ranking aid for human review: not a probability, not a confidence in correctness, not evidence of structural convergence; a low value is not evidence against it.

Calibration: similarity and rank of reviewed connections among all cross-programme pairs:

- X::0001 (tested_structural_analogy): similarity 0.000, rank unranked (no shared terms) of 11725
- X::0002 (epistemic_compatibility): similarity 0.060, rank 876 of 11725
- X::0003 (explicit_contrast): similarity 0.023, rank 5516 of 11725
- X::0004 (explicit_contrast): similarity 0.015, rank 8061 of 11725
- X::0005 (shared_implementation_assumption): similarity 0.000, rank unranked (no shared terms) of 11725
- X::0006 (qualifies): similarity 0.000, rank unranked (no shared terms) of 11725
- X::0007 (epistemic_compatibility): similarity 0.029, rank 4014 of 11725
- X::0008 (qualifies): similarity 0.050, rank 1489 of 11725
- X::0009 (tested_structural_analogy): similarity 0.102, rank 111 of 11725

Top 10 unreviewed retrieval candidates:

- 0.190 `CL::CL-F05` ↔ `GT::GT-F82-E5A-COMPARATOR-AND-NUMERICAL-QUALIFICATIONS` (shared terms: checks, items, controls, frozen) [already_reviewed]
- 0.170 `CL::F8E-K3-DRIFT-SURFACE` ↔ `GT::GT-F25-KINETICS-SETS-OCCUPANCY-UNDER-IRREVERSIBILITY` (shared terms: formation, dissolution, ratio, exactly)
- 0.170 `CL::CL-T20` ↔ `GT::GT-Q01-KINETIC-CONVENTION` (shared terms: justify, alone)
- 0.167 `CL::F8E-K3-DRIFT-SURFACE` ↔ `GT::GT-F04-RETENTION-NOT-APPROACH` (shared terms: drift, exactly)
- 0.165 `CL::F8D-WEAK-GRADE-SURFACE` ↔ `GT::GT-F04-RETENTION-NOT-APPROACH` (shared terms: drift, exactly)
- 0.162 `CL::F8C-TOPOLOGY-ATLAS` ↔ `GT::GT-F64-CHORD-SWITCHES-SITE-OFF` (shared terms: chord, middle, path)
- 0.159 `CL::F8M-HISTORY-ONLY-STRUCTURAL-SILENCE` ↔ `GT::GT-F69-CLOCK-SEPARATED-SORTING` (shared terms: first, law, differ, any, uniform)
- 0.156 `CL::F8C-PATH-CONVERTS-SLOT` ↔ `GT::GT-F05-RELATIONAL-POTENTIAL` (shared terms: count, edge, share, triangle)
- 0.155 `CL::CL-T58` ↔ `GT::GT-F07-SHARED-BASIN-DIFFERENT-CLOCKS` (shared terms: masses)
- 0.152 `CL::F008-COMPOSITION-REPRESENTATION` ↔ `GT::GT-Q18-REVERSAL-AT-W4` (shared terms: discriminator, depends, graph)
