# Execution GT-P001 — programme establishment and Rounds G0 and G1

**Prompt:** `gravity-time/provenance/prompts/GT-P001-agent-input.md`, 7,693 bytes, sha256 `66fd93e36e93910ae30efdad5857d1b45abcdf92c00b8e10bfe67fcc44572793`. An agent transcription, not a byte capture; relationship to the authored prompt unknown.

**Branch** `research/gravity-time-admissibility` from `22e252e560cc711d337b6ae506b0fb76728247d6` (8G). The inclusive range is `38e9201` through `d7f7f79`. This close-out commit is outside it.

| Round | Frozen plan | Plan hash | Result |
| --- | --- | --- | --- |
| G0 | `b45f10b148fe7df1f54ffb7db35d4ea828b170ef` | `30fba33af15509f6e46458532490f5e34a928487b09863592fb438a6d344e92a` | `97c2daa5d445e57110fa64baa690e64934a6373a` |
| G1 | `331d5197dc5332aaf14b57c8661eb7004b54e259` | `1707f1783acb3509d33f39177ff76e501be7406e5c9ae6fc8470cc88882d67c4` | `3dccd0a` |

## Divergences

- **Post-freeze solver change.** G0's first run was killed out of memory after 39 of 40 items. The dense absorption matrix for `FREE-N6-LOCK` (32,767 transient states) did not fit. Commit `226abe1` changed the solver for sets above 4,096 states, not any estimand. The dense and iterative paths agree to about 1e-12 on sets small enough for both. The 39 completed items were not recomputed.
- **Frozen G0 drift criterion confounded.** It was reported as computed and qualified in the report and the ledger.
- **G1 P3 replaced before freezing.** The originally drafted P3 (DENS leaves inward share at null) was found false by derivation before the freeze, and was replaced by a derivable clock prediction. The replacement is in the frozen plan.
- **Gibbs identity read after G0.** It was verified on fresh kernels and is recorded as a post-hoc reading.
- **No G2 or later round** was opened.

## Coherence

Snapshot `gravity-time/coherence/snapshots/through-gt-g1.md`, sha256 `73919597964af207bf45984e027609cd719a0c32bf0d8c883580494dc5bb88ef`. Canonical ledger sha256 `b63c186b68f9d723ececf1c2e661479bb193d15167381ad751c95496cb178eee`.

## CI

Actions run `38474755842` on `d7f7f797f76af69a6580d3e03a3f5918e9852e21`: success, with both jobs `constraint-lab` and `books`. That run id is not a run of this close-out commit.
