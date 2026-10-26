# Execution record — GT-P002 (open-thetical rounds E0A, E0B)

- **Prompt:** `prompts/GT-P002-agent-input.md`. Agent transcription; byte identity with the authored prompt is not established. The OTR 1.0 definition supplied with it is at `research-methods/open-thetical-research.md` (sha256 `2d902395…88dd`), committed alone in `4efcd02`.
- **Implementing agent:** Claude Opus 5.5.
- **Date:** 2026-10-14.
- **Starting point:** `f6b3d24` (GT-P001 close-out), descending from the 8G base `22e252e`. 8H (`e9f8f3b`, open) was not used.

## Commit sequence

| Commit | Content |
| --- | --- |
| `4efcd02` | shared OTR 1.0 method (research-methods/ only) |
| `62d53fa` | GT-P002 provenance; charter adopts OTR |
| `3193c66` | coverage, novelty and E0A selection audit (before any E0A code) |
| `8ee42fe` | E0A analysis code and fixture tests |
| `2e5c97e` | **E0A plan frozen** (hash `c98414e1…9dfa`), pushed before execution |
| (journey) | E0A question recorded before execution |
| `c31ef92` | E0A tables (48/48, payload `18fa301b…98cf`) |
| `679b477` | E0A reflection and E0A→E0B decision note, journey step 6 |
| (feat) | E0B analysis code; backward-compatible `families` parameter in gte0a |
| `50c4b2c` | **E0B plan frozen** (hash `ad28c5b1…2c32`), pushed before execution |
| (journey) | E0B question recorded before execution |
| `d99f972` | E0B tables (36/36, payload `f02c7c95…cb80`) |
| `950eeac` | report, atlas, ledger, register, roadmap, record tests; journey step 8 (E0C not run) |

## Execution decisions

- **No post-freeze change to either round's estimands.**
- **One code change between the rounds.** `gte0a` functions gained an optional `families` parameter, with the E0A families as default. A recomputed E0A item matched to about 1e-15, except a conditional attachment over a 1e-9 mass (2.8e-10) and the reordering of exactly tied top-k entries. E0B's replication cells reproduced E0A within 1e-12 (Y2).
- **Reproducibility.** Results are reproducible to about 1e-15, not bitwise, because of multi-threaded BLAS.
- **Pre-freeze exposure.**
  - E0A: synthetic cycle and N=4 fixtures, timing on N=6 NULL, and a PATHF kernel build with no observable computed.
  - E0B: E0A tables read in full; N=4 fixtures; the single E0A replication check.
- **E0A frozen expectation X4 failed in 4/16 cells** (saturation). It is recorded as computed and not reworded.
- **E0C was not run.** The remaining question needs N ≥ 7 and new kernel machinery.
- **Generated items are untracked, as for G0/G1.** Selected atlas trajectories are tracked in `reports/gt-e0-atlas-trajectories.json`, and every trajectory replays from its seed.
- **No change** to the Constraint Laboratory's records, to CBO, or to the 8H branch. Cross-programme suggestions are proposals only (report §8).
- **PR #6** stays a draft and is not merged.

## Verification

- **Local suite:** 345 tests passed (319 before GT-P002).
- **CI:** run 38534005957 (pull_request, head `950eeac`) succeeded. The run on the provenance close-out commit is recorded in `ledger.jsonl`.
