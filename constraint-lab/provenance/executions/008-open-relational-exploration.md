# Execution 008 — open relational exploration

This is the execution record for prompt 008. It closes that prompt. It does not close prompt 007, prompt 007R, or prompt 007B.

## Prompt

| Field | Value |
| --- | --- |
| prompt_id | 008 |
| agent_input_path | `constraint-lab/provenance/prompts/008-v0.8-agent-input.md` |
| agent_input_sha256 | `b4e73a9b3f43d80dbe3f9e1d8b63ae28107dd7a1928ed172a391eb1036cba065` |
| agent_input_bytes | 41862 |
| authored_prompt_path | null |
| authored_prompt_sha256 | null |
| authored_prompt_bytes | null |
| authored_prompt_status | `pending_verbatim_import` |
| relationship of authored to agent input | `unknown` |
| date | 2026-10-12 |
| authoring source | user instruction to the implementing agent |
| target | Grok 4.7 |
| repository | gellsmore-svg/Relational-Substrate |
| starting_branch | `research/constraint-lab-v0.7b` |
| starting_commit | `8f47bae7f773ec3b706b2c603667a31b9c69285b` |

The stored file is the agent input. It includes one leading newline and one trailing newline. It does not contain its own sha256. No separate authored Markdown was byte-compared. Prompt 007, Prompt 007R, and Prompt 007B are not overwritten.

## Result

Branch `research/constraint-lab-v0.8-exploration`.

The inclusive commit range produced by prompt 008, through the synthesis, is:

```text
0d8b4064e922157c4b715a0e815d17e00836e4da
a9d35503f86521b4e8046a03b9a6250143594dc3
```

The parent of the first commit is `8f47bae7f773ec3b706b2c603667a31b9c69285b`. The commit that adds this execution file is outside that range. The ledger line that points at this record is that same close-out commit. It is not inside the analysis range above.

Experiment id:

- `generation-008-open-relational-exploration`

Reports:

- `constraint-lab/reports/generation-008-round-000-trajectory-atlas.md`
- `constraint-lab/reports/generation-008-round-001-trajectory-atlas.md`
- `constraint-lab/reports/generation-008-round-002-trajectory-atlas.md`
- `constraint-lab/reports/generation-008-exploration-synthesis.md`

Frozen plan commits, each pushed before its round executed:

- Round 0: `0a9e74f287b3ecb24efd3981b9562e53086ffee9`
- Round 1: `509e80fbb5b472d8da61ba7ba85fcedba15939c1`
- Round 2: `93253e2d249a6f44ace3e7c63ce42306404fa401`

Round 3 was not opened.

## What ran

Mode B. Rounds 0, 1, and 2. Roots under `constraint-lab/generated/generation-008/`. The supervisor used 2 workers, a 10 second heartbeat, and a 120 second watchdog.

Round 0: 4,160 episodes, 4,576 items, 39 batches, 416 of 416 replays exact. Events written 3,623,976. Pair events 2,129,920. Median batch wall 15.49511 s. p90 16.694902 s. Maximum 17.335057 s. Timeouts 0. Retries 0. Quarantines 0. Disk after merge 3.0 GB.

Round 1: 1,664 episodes, 1,831 items, 16 batches, 167 of 167 replays exact. Events written 1,425,781. Pair events 851,968. Median batch wall 14.597432 s. p90 15.761986 s. Maximum 15.95338 s. Timeouts 0. Retries 0. Quarantines 0. Disk after merge 1.2 GB.

Round 2: 1,664 episodes, 1,831 items, 16 batches, 167 of 167 replays exact. Events written 1,400,613. Pair events 851,968. Median batch wall 14.495715 s. p90 15.764156 s. Maximum 15.799182 s. Timeouts 0. Retries 0. Quarantines 0. Disk after merge 1.2 GB. Started 2026-10-12T18:51:17Z. Last activity 2026-10-12T18:53:23Z.

`verify --require-complete` returned `ok` and `complete` on each round root, with an empty problem list. Spec hashes equal the plan hashes:

- Round 0 `fec52960f5e16706e12e9baf0a45169f49c2414b6e7e3ecc80b1b9d0f97c3b86`
- Round 1 `6f19f8d9ad374792eae970b7691f3eca63699a9d743c13016550e266a9de8354`
- Round 2 `d5141d33f817357cf028ac97de8d7dad486113685f86a0c71734003cfef437a0`

`constraint-lab/generated/` is gitignored. CI does not re-run the atlas. The published numerical record is the reports and the tables files.

## Divergences from the prompt

- Round 3 was left unopened. The prompt allows at most four rounds. After Round 2 the four finite grades on the S01 rule were ordered and `strong_favour` reversed the unconditional dissolve and the off-edge conditional dissolve, so the remaining round was not used.
- Optional trajectory clustering was not built.
- Conditional mutual information of the current triad, given the pair class, was computed for Round 0 only.
- Episodes ran as one process. The 64-epoch segment path is implemented and covered by tests. The batches did not need it.
- Every full route signature inside a round was unique, so the medoid and rare-route selectors resolved by lexicographic tie-break. The reports say so.
- No separate authored Markdown was imported. The authored hash stays null.
- The PowerShell start, stop, and watch scripts were not executed on this Linux host.

## Local checks

After the synthesis commit, `python -m pytest -q` in `constraint-lab` reported 148 passed in 209.28 seconds. That suite includes the Generation 8 replay, orbit, and frozen-plan tests and the prior platform tests. It does not re-run the trajectory atlas.

## CI

Actions run `38294927720` is the push of `a9d35503f86521b4e8046a03b9a6250143594dc3`. The URL is `https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/38294927720`.

`gh run view 38294927720` reported conclusion success on `a9d35503f86521b4e8046a03b9a6250143594dc3`. Jobs `constraint-lab` and `books` both completed.

This execution file is a later commit. The run id is not a run id for the commit that adds this file.
