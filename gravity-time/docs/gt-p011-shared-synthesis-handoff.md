# GT-P011 handoff to the shared synthesis hub

*This file is not the hub update. GT-P011 also prepared a **staged hub milestone** covering GT-P010 and GT-P011 on a separate hub branch (see the PR #6 description and `provenance/execution-GT-P011.md` for the branch, PR and status). Nothing here is accepted; all candidates are `proposed`.*

## Provenance

| Item | Value |
| --- | --- |
| GT-P011 close | the provenance-close commit after this file (recorded in `provenance/ledger.jsonl`) |
| E5C frozen plan | `469ee28017cc797be23ab0c71826930ea3784d02`, plan_hash `bab7a59d5faf0ce31a20f5b9fe1bb42ff2f308d94df84bfa34a602c7e7416e47` |
| E5C results | `5080199`, payload `582e845ba338cdc543cb7231d375c6afb594b065ecc0f4407e53fe3ca095e5f1` |
| Snapshot | `coherence/snapshots/through-gt-e5c.md` |
| New GT records | GT-F91 to GT-F97, GT-Q25, GT-R156 to GT-R166 |
| GT-P010 anchor | close `4aaf04c`; GT-F83 to GT-F90, GT-Q23/Q24; handoff `docs/gt-p010-shared-synthesis-handoff.md` (candidates C-1, C-2) |
| Hub consulted | `38c2501` (read-only); GT pin `79fa6b0` (GT-P009) is stale by two rounds |
| Review status | GT-P009, GT-P010 and GT-P011 are closed and scientifically unreviewed |

## Shared questions

| Question | GT-P011 report |
| --- | --- |
| XQ::04 | Durability with a return/exit split separates reconstruction from flicker: CSPH triangle renewal is flicker-assisted, while PATHH triangle survival exceeds NK. The observer has no history axis. Mobile or unlabelled identity is still undefined. |
| XQ::07 | E5C quantities are resolvent and stopping-set functionals: a first-hit law, then powers of a local-event kernel. Both programmes use this vocabulary. No common theorem is shown. |
| XQ::01 | The effects remaining beyond NK lie in within-layer and anchor-local arrangement, which NK does not match (GT-Q25). |
| XQ::03 | Anchor-local counts integrate inert remote events exactly (T13); this is not a time change hiding events. |

## Candidate (proposed only)

**C-3.** `GT::GT-F97-FIRST-HIT-SAMPLING-MATTERS` ↔ `CL::F8N-MATCHED-SOURCE-PASSAGE`, type `epistemic_compatibility`.
- **Claim.** Both programmes condition post-event functionals on an explicit source law: CL on stationary class-conditioned sources, GT on the exact first-hit law.
- **Eight dimensions.**

  | Dimension | Verdict |
  | --- | --- |
  | State | differs |
  | Transition law | differs |
  | Support | differs |
  | Clock | differs: event epochs versus anchor-local counts |
  | Projection | differs |
  | Intervention | not applicable |
  | Horizon | differs: first return versus post-renewal survival |
  | Conditioning | same role: an explicit source law |

- **Lineage:** shared 8G.
- **Falsifier:** a CL post-event functional whose value is invariant to replacing the source law (it would weaken the methodological point).
- **Recommended category:** `candidate`.

## Hub intake

Run the staged hub milestone (see the PR #6 description). Adoption needs a named human reviewer for `apply-pin`.
