# Execution 008C — mechanistic decomposition

This is the execution record for prompt 008C. It closes that prompt. It does not close prompt 008B.

## Prompt

| Field | Value |
| --- | --- |
| prompt_id | 008C |
| agent_input_path | `constraint-lab/provenance/prompts/008C-v0.8c-agent-input.md` |
| agent_input_sha256 | `dbccad0a983eab3f6f2fa738275fb62c8af9f2beffda005b08b85feb7fc034d9` |
| agent_input_bytes | 57205 |
| authored_prompt_path | null |
| authored_prompt_sha256 | null |
| authored_prompt_bytes | null |
| authored_prompt_status | `pending_verbatim_import` |
| relationship of authored to agent input | `unknown` |
| date | 2026-10-13 |
| authoring source | user instruction to the implementing agent |
| target | Grok 4.7 |
| repository | gellsmore-svg/Relational-Substrate |
| starting_branch | `research/constraint-lab-v0.8b-information-calibration` |
| starting_commit | `66fc7f48ac776aec461553cfac06126ed6566626` |

The stored file is the agent input. It includes one leading newline and one trailing newline. It does not contain its own sha256. No separate authored Markdown was byte-compared. Prompt 008B is not overwritten. The authored hash stays null.

## Result

Branch `research/constraint-lab-v0.8c-mechanism`.

The inclusive commit range produced by prompt 008C, through the mechanism report, is:

```text
3d422467574e979387b5606b7ab4d5996d89837c
479469f7b56277849f75080f5f8478e875d95ec7
```

The parent of the first commit is `66fc7f48ac776aec461553cfac06126ed6566626`. The commit that adds this execution file is outside that range. The ledger line that points at this record is that same close-out commit. It is not inside the analysis range above.

Experiment id:

- `generation-008c-mechanistic-decomposition`

Reports:

- `constraint-lab/reports/generation-008c-mechanistic-decomposition.md`
- `constraint-lab/reports/generation-008c-round-c0-tables.json`
- `constraint-lab/reports/tables/generation-008c-local-law.csv`
- `constraint-lab/reports/tables/generation-008c-topology.csv`
- `constraint-lab/reports/tables/generation-008c-checkpoint-1.csv`
- `constraint-lab/reports/tables/generation-008c-checkpoint-1-mi.csv`
- `constraint-lab/reports/tables/generation-008c-gate-memory.csv`
- `constraint-lab/reports/tables/generation-008c-mask-contribution.csv`
- `constraint-lab/reports/tables/generation-008c-drift.csv`

Journey:

- `constraint-lab/exploration/generation-008c/journey.jsonl`

Charter:

- `constraint-lab/exploration/generation-008c/charter.md`

Frozen analysis plan, pushed before Round C0 executed:

- Round C0: `3e783387cd2c8050559c29bac059beae03555ab7`
- plan hash: `febde3989a8b2f2461440e708897fe78c1fdac436375c0c628b393309932c897`
- plan file: `constraint-lab/exploration/generation-008c/round-c0-plan.json`

The tables commit is `f962000d7c6c750565843426d46bcd3fdbb43026`. Journey step 2 records that sha as `result_commit`. Journey step 1 still has `result_commit` null. That opening line is unchanged.

The report commit is `479469f7b56277849f75080f5f8478e875d95ec7`.

Round C1 was not opened.

Coherence snapshot, written in the report commit:

- path: `constraint-lab/coherence/snapshots/through-generation-008c.md`
- file sha256: `d0e73fd314ad91682e66026de02ea4f2253a05d62e581b3f9270f9809935abf0`
- canonical ledger sha256 recorded in that snapshot: `b0800de29262c13ba7f4af8ce60790b5912698401e39f7ec10dcbcd628f87cb3`

The snapshot hashes the findings and relations ledger. It does not hash this execution file.

## What ran

Mode B. Round C0 only. Exact mechanism reading of the N=4 transition law already used in Generations 8 through 8B. No new stochastic trajectories. No permutation calibration. No parameter fit. No new controls. Root `constraint-lab/generated/generation-008c/round-c0`. The supervisor was not used. Each item is an in-process kernel read under a 120-second watchdog.

The bounded items were local-law, topology, checkpoint, excursion, gate-memory, contribution, projection, drift, and hierarchy reads: 60 items. The longest wall was 1.4129106379996301 seconds. Each stayed inside the watchdog.

`generation008c verify --frozen-plan-commit 3e783387cd2c8050559c29bac059beae03555ab7` on that root returned `complete: true`, `missing_count: 0`, and plan hash `febde3989a8b2f2461440e708897fe78c1fdac436375c0c628b393309932c897`. The published tables record `validation.ok: true` and an empty problem list. Their `frozen_analysis_plan_commit` is `3e783387cd2c8050559c29bac059beae03555ab7`.

`constraint-lab/generated/` is gitignored. CI does not recompute the kernels. The published numerical record is the report and the tables. The tables file is 674,820 bytes, sha256 `6002bc7c817514a3d4576ced8f56d45b5a05409682ef4ab42fc32caf352b0493`. Its payload sha256 is `8c2f6cf73a633ab3addced919931e2c79bfe2d76b6cfa7dc58cde55ce1daccb8`.

## Divergences from the prompt

- Round C1 was not defined. The prompt asks for one frozen analysis round, C0.
- No new stochastic scientific trajectories were run.
- Permutation calibration was not repeated.
- No parameters were fit and no controls were added.
- No separate authored Markdown was imported. The authored hash stays null.
- Actions run `38354878731` on `ffbc19a036eee534be3b893aec7dd100a6d5839d` succeeded before C0 tables were published. That run is the journey-question head. It is not a run of the tables commit or of the report.
- The coherence ledger, generated views, and snapshot are part of the report commit. They are inside the inclusive range. This close-out does not regenerate them.

## Local checks

Before the report head was pushed, the constraint-lab suite reported 207 passed in 118.10 seconds. `generation008c verify` returned complete, with the plan hash above, before this close-out.

## CI

Actions run `38355958689` is the push of `479469f7b56277849f75080f5f8478e875d95ec7`. The URL is `https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/38355958689`.

`gh run view 38355958689` reported conclusion success on `479469f7b56277849f75080f5f8478e875d95ec7`. Jobs `constraint-lab` and `books` both completed. The constraint-lab job reported 207 passed in 88.06 seconds.

This execution file is a later commit. The run id is not a run id for the commit that adds this file.
