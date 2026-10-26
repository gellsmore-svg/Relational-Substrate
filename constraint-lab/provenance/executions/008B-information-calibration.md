# Execution 008B — information calibration

This is the execution record for prompt 008B. It closes that prompt. It does not close prompt 008A.

## Prompt

| Field | Value |
| --- | --- |
| prompt_id | 008B |
| agent_input_path | `constraint-lab/provenance/prompts/008B-v0.8b-agent-input.md` |
| agent_input_sha256 | `3f77c124b444446a78c3020a838fa65ddc9f2fddc08690ffff082ee94a70b660` |
| agent_input_bytes | 41188 |
| authored_prompt_path | null |
| authored_prompt_sha256 | null |
| authored_prompt_bytes | null |
| authored_prompt_status | `pending_verbatim_import` |
| relationship of authored to agent input | `unknown` |
| date | 2026-10-13 |
| authoring source | user instruction to the implementing agent |
| target | Grok 4.7 |
| repository | gellsmore-svg/Relational-Substrate |
| starting_branch | `research/constraint-lab-v0.8a-context-repair` |
| starting_commit | `b7b5d848d90b7d1824bcce9740c2faf966cbea54` |

The stored file is the agent input. It includes one leading newline and one trailing newline. It does not contain its own sha256. No separate authored Markdown was byte-compared. Prompt 008A is not overwritten.

## Result

Branch `research/constraint-lab-v0.8b-information-calibration`.

The inclusive commit range produced by prompt 008B, through the information-calibration report, is:

```text
331a4c43ea6f7c0fec7f89b33d2d4cc6b1661d73
72f77430352ab6fa76dfe314992ed4494c1e1a1c
```

The parent of the first commit is `b7b5d848d90b7d1824bcce9740c2faf966cbea54`. The commit that adds this execution file is outside that range. The ledger line that points at this record is that same close-out commit. It is not inside the analysis range above.

Experiment id:

- `generation-008b-information-calibration`

Reports:

- `constraint-lab/reports/generation-008b-information-calibration.md`
- `constraint-lab/reports/generation-008b-round-b0-tables.json`

Journey:

- `constraint-lab/exploration/generation-008b/journey.jsonl`

Frozen analysis plan, pushed before Round B0 executed:

- Round B0: `466d54339738d315ed621ea4256a239cb026498a`
- plan hash: `279857bb2ee82eefd430ba56c9fa3758238ebea9e0b652c01b56b97dbc1bf618`
- plan file: `constraint-lab/exploration/generation-008b/round-b0-plan.json`

The tables commit is `dc9f9b9eb6e4a36b4513d10b49e937c43b57b371`. Journey step 2 records that sha as `result_commit`. Journey step 1 still has `result_commit` null. That opening line is unchanged.

Round B1 was not opened.

## What ran

Mode B. Round B0 only. Analysis of the Generation 8A Round A0 counts and the exact N=4 transition law. No new stochastic trajectories. Root `constraint-lab/generated/generation-008b/round-b0`. Two workers. Heartbeat on stderr. Watchdog 120 seconds. The palette is R00 through R07. Permutation counts are 10,000 initial-context draws per cell and 2,000 current-context draws per cell.

The bounded commands were `exact` for each system, `permute-initial` for each system, and `permute-current` for each system and source: 40 items. Exact commands finished in about 3.8 seconds. Initial-context permutations finished in about 30 to 32 seconds. Current-context permutations finished in about 14 to 16 seconds. Each stayed inside the watchdog. The supervisor was not used.

`generation008b verify` on that root returned `complete: true` with an empty missing list. The same command checked that `466d54339738d315ed621ea4256a239cb026498a` is an ancestor of `dc9f9b9eb6e4a36b4513d10b49e937c43b57b371` and that the plan hash matches.

`constraint-lab/generated/` is gitignored. CI does not recompute the kernels. The published numerical record is the report and the tables file. The tables file is 480,377 bytes, sha256 `d7bc06d027eabb62f5f2e5bed312c746ef3f062198a25a35bd5246ce23590e09`. Its payload sha256 is `b2ecdac74e38b3d53160a43b3319bcb4cc607cab4817c5cb2cfdaa68f4171adf`.

## Divergences from the prompt

- Round B1 was not defined. The prompt asks for one frozen analysis round, B0.
- No new stochastic scientific episodes were run. Permutation draws are analysis of the committed counts.
- The optional episode-block bootstrap was not run.
- A separate horizon-matched first-destination mutual information was omitted. The frozen plan omits it when unabsorbed mass at epoch 512 is below `1e-8`. The largest such mass is `2.460e-22`, on R05. The validation table stores the mass.
- The first `exact` command for R03 stopped because an empirical class-conditional value on a zero-information control was above the floor `1e-10`. That quantity is an occupancy correlation inside a graph class. Commit `7eb63924c4c5484decd1ab5b7bee3a25b440ac68` keeps the floor on the full-mask identity. R03 was rerun after that commit. The frozen estimands did not change. The published tables include the rerun. That commit is inside the inclusive range.
- The optional labelled pair-mask checkpoint mutual information was computed and stored.
- No separate authored Markdown was imported. The authored hash stays null.
- Actions run `38319517214` on `466d54339738d315ed621ea4256a239cb026498a` succeeded before B0 execution. That run is the frozen-plan head. It is not the report-head run below.

## Local checks

Before the report head was pushed, the constraint-lab suite reported 182 passed in 220.53 seconds. `generation008b verify` returned complete, with the plan-result chronology above, before this close-out.

## CI

Actions run `38321798042` is the push of `72f77430352ab6fa76dfe314992ed4494c1e1a1c`. The URL is `https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/38321798042`.

`gh run view 38321798042` reported conclusion success on `72f77430352ab6fa76dfe314992ed4494c1e1a1c`. Jobs `constraint-lab` and `books` both completed. The constraint-lab job reported 182 passed in 105.48 seconds.

This execution file is a later commit. The run id is not a run id for the commit that adds this file.
