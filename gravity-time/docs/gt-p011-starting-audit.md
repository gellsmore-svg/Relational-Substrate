# GT-P011 starting audit

*15 October 2026. Written before any E5C computation. No E5C observable of any N=5 or N=6 cell has been evaluated.*

## 1. Live heads (verified by `git fetch`)

| Ref | Expected | Observed |
| --- | --- | --- |
| GT `research/gravity-time-admissibility` | `4aaf04c0601b4232fc9fa24f6aa5d5ce6390c7e2` | same; clean worktree; CI green (run 38787488394) |
| GT PR #6 | open, draft | open, draft |
| Hub `main` | `38c2501bbab22ca1eb2288ea76a962ac0170d5e6` | same |
| CL (for context only) | 8N `e650d71` | 8N `e650d71`; a later CL 8O close exists at `99565d1` (tag `constraint-lab-008o-close`) |
| E5C artefacts | none | none: no `round-e5c` plan, table, report or branch |

No concurrent E5C or hub-update branch exists on the remote. The Downloads folder also contains other prompts (CL 8P, a "repository-native federated cycle" prompt) that other agents may be executing. The hub head is therefore re-checked immediately before the hub milestone step (§7 of the prompt), and any movement is reconciled rather than overwritten.

## 2. Prior GT results carried forward unchanged

- **GT-P010 / E5B:**
  - close `4aaf04c`, frozen plan `fc3ec7d` (plan_hash `c35bc3bb…d944`), results `fcb17ae` (payload `0d307350d1ac…`);
  - 12/12 laws, 36/36 analyses, every frozen check passing, 865 tests, CI green.
- **E5A intact-count correction:** 2/30 rather than 1/30, recorded append-only as GT-F90; GT-P009's files are unedited.
- **E5B claims preserved:**
  - PCOMP's vertex patterns fall below NK;
  - PATHF F_STAR/F_2PATH have small, consistent advantages against NK (= ND for PATHF);
  - PATHH F_TRI/F_STAR and CSPH F_TRI exceed NK, CSPH with high flicker;
  - CLOSEW attenuates, and F_2PATH reverses at N=6;
  - complete renewal is defined relative to the post-entrance participants and says nothing about durability;
  - F_STAR complete renewal is structurally impossible at N ≤ 6 (T10);
  - size-1 F_TRI renewal equals a departure.
- **Not run in E5B:** the durable-renewal filter and the anchor-local sensitivity analysis. E5C starts from new definitions.

## 3. Hub consulted (read-only)

- **Commit `38c2501`.** Read with `git show`; nothing merged.
- **Pins:** GT `79fa6b0` (GT-P009, unreviewed); CL `e650d71` (008N; the hub manifest still lists it unreviewed, though CL 8O has since recorded an external review of 008N on its own branch); SC `aa06213` catalogued only.
- **Records:** 9 connections (all human_accepted at their categories through RT-0001), 50 proposals, round trips RT-0001 to RT-0003 all ratified (none open).
- **The GT pin is stale.** It predates GT-P010 and GT-P011; the milestone in §7 addresses both rounds.
- **Shared questions used as discriminating questions:**
  - XQ::01: what NK does not control, namely within-layer and anchor-local rate arrangement;
  - XQ::04: durable reconstruction against flicker;
  - XQ::07: whether durability is a generator/stopping-set functional, a kind of quantity CL also uses;
  - XQ::03: local event counts are counts within one process, not a new time.
- **CL scope.** CL-T85, CL-T88 and CL-T89 were compared in GT-P010's audit §4. E5C performs no CL computation.

## 4. Exposure and adaptivity

E5C was chosen because of E5B, and the twelve laws and their E5A/E5B values are exposed. E5C is therefore an adaptive follow-up with new estimands (first-renewal distribution, post-renewal survival over anchor-local events, return against exit), not a blind confirmation.

All six families at both sizes are covered, including the negative and control rows. Nothing is selected by E5B sign.

## 5. Scope decisions to settle before the freeze

1. **Predicates.** F_2PATH and F_TRI, the latter stratified by entry size. F_STAR partial-renewal durability is **not** included: E5B's partial channel would need its own durability definition, and the prompt marks it optional.
2. **Horizons.** h ∈ {0, 1, 2, 4, 8} anchor-local events, unless fixture costs force fewer (they do not; see the definitions note).
3. **Continuous-time channel.** No optional continuous-time post-renewal channel. Event counts only, with the anchor-local hazard reported as a diagnostic.
4. **Comparators.** N0, ND and NK, unchanged.
5. **Exact computation:** forward (row) solves in canonical frames; no simulation.
