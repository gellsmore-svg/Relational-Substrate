# Execution 008A — context-alignment repair

This is the execution record for prompt 008A. It closes that prompt. It does not close prompt 008.

## Prompt

| Field | Value |
| --- | --- |
| prompt_id | 008A |
| agent_input_path | `constraint-lab/provenance/prompts/008A-v0.8a-agent-input.md` |
| agent_input_sha256 | `1c44d30b086e2e02ace4d0777605267d8f7139c71948beffe058b5c976d25010` |
| agent_input_bytes | 33115 |
| authored_prompt_path | null |
| authored_prompt_sha256 | null |
| authored_prompt_bytes | null |
| authored_prompt_status | `pending_verbatim_import` |
| relationship of authored to agent input | `unknown` |
| date | 2026-10-12 |
| authoring source | user instruction to the implementing agent |
| target | Grok 4.7 |
| repository | gellsmore-svg/Relational-Substrate |
| starting_branch | `research/constraint-lab-v0.8-exploration` |
| starting_commit | `f5c0b6d1c8aae7b467066a4b3b5974ea2a0f59c9` |

The stored file is the agent input. It includes one leading newline and one trailing newline. It does not contain its own sha256. No separate authored Markdown was byte-compared. Prompt 008 is not overwritten.

## Result

Branch `research/constraint-lab-v0.8a-context-repair`.

The inclusive commit range produced by prompt 008A, through the chronology checkout fix, is:

```text
6293985e8e77645e912b60b281beaf479c3d5939
bf821c771e4ed86e24688ed44ab6035b7e9af785
```

The parent of the first commit is `f5c0b6d1c8aae7b467066a4b3b5974ea2a0f59c9`. The commit that adds this execution file is outside that range. The ledger line that points at this record is that same close-out commit. It is not inside the analysis range above.

Experiment id:

- `generation-008a-context-repair`

Reports:

- `constraint-lab/reports/generation-008a-round-a0-context-repair.md`
- `constraint-lab/reports/generation-008a-round-a0-tables.json`
- `constraint-lab/reports/generation-008a-context-repair-synthesis.md`

Journey:

- `constraint-lab/exploration/generation-008a/journey.jsonl`

Frozen plan commit, pushed before Round A0 executed:

- Round A0: `61ed53075238284850e792aff5743f0a8a7b6695`
- plan hash: `efbfcf17861878e528e0c359877d65281d695a78e1adaabb105181bd4b68f68d`
- plan file: `constraint-lab/exploration/generation-008a/round-a0-plan.json`

The atlas commit is `4897d9e02b2942670bafc52bc966ef6709167b64`. Journey step 2 records that sha as `result_commit`. Journey step 1 still has `result_commit` null. That opening line is unchanged.

Rounds A1 and A2 were not opened.

## What ran

Mode B. Round A0 only. Root `constraint-lab/generated/generation-008a/round-a0`. The supervisor used 2 workers, a 10 second heartbeat, and a 120 second watchdog. The horizon stayed 512 pair events, with a 16,384 full-event cap. The repair palette is eight systems, three source graphs, 16 raw triad configurations, and 16 replicates: 6,144 primary episodes.

Round A0: 6,144 episodes, 6,759 items, 58 batches, 615 of 615 durable replays exact. Every stored episode carries `smoke_replay: exact`. Full events 5,314,418. Pair events 3,145,728. Transition markers 3,145,728. Median batch wall 17.716329 s. p90 18.062894 s. Maximum 19.428333 s. Timeouts 0. Retries 0. Quarantines 0. Disk after merge 678,150,248 bytes. Started 2026-10-12T21:07:49Z. Last activity 2026-10-12T21:17:21Z. All 6,144 episodes ended at `pair_horizon`.

`verify --require-complete` returned `ok` and `complete` on the Round A0 root, with an empty problem list. The spec hash equals the plan hash `efbfcf17861878e528e0c359877d65281d695a78e1adaabb105181bd4b68f68d`.

`constraint-lab/generated/` is gitignored. CI does not re-run the atlas. The published numerical record is the report and the tables file.

## Divergences from the prompt

- Rounds A1 and A2 were left unopened. The prompt allows at most three rounds. After Round A0 the symmetry groups were calculated, every raw context had a trajectory, and the first-destination information stayed small under the uniform raw prior, so the remaining rounds were not used.
- Current-triad conditional information was computed for all eight A0 systems. The prompt requires the subset R00, R01, R03, R05, R06, and R07 unless a preflight adjusts it. The frozen plan computed the whole palette. That choice is in the plan commit, before any A0 trajectory was inspected.
- Three cells with a unanimous 16/16 first destination are a reading of the predeclared destination counts. They are not a new catalogue measure.
- Prohibit was not introduced. Every episode reached the pair horizon.
- A paired random-number design across raw contexts was not used. The prompt reserves that for a later frozen plan.
- No separate authored Markdown was imported. The authored hash stays null.
- Actions run `38308019051` on `439d5545560b62e7e8d4eeea86683c38c3ef0f9a` failed. Actions run `38311458058` on `6a8060b0a336a9a140eee9816c0db68cf72fefd2` failed. In both, job `books` succeeded and job `constraint-lab` failed `test_generation8_frozen_plans_are_ancestors_of_their_results` with `ChronologyError: 0a9e74f287b3ecb24efd3981b9562e53086ffee9 is not an ancestor of 2b1778306f08e556df195d735e482c8b3533d796`. The checkout was shallow, so `merge-base` could not see the Generation 8 plan commits. Those runs are not trajectory mismatches. Commit `bf821c771e4ed86e24688ed44ab6035b7e9af785` sets `fetch-depth: 0` on the constraint-lab job only. That commit is inside the inclusive range.

## Local checks

The published atlas was verified with `generation008a verify --require-complete` before the atlas commit. The suite that includes the Generation 8A tests is the CI result below. This close-out does not re-run the trajectory atlas.

## CI

Actions run `38311563660` is the push of `bf821c771e4ed86e24688ed44ab6035b7e9af785`. The URL is `https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/38311563660`.

`gh run view 38311563660` reported conclusion success on `bf821c771e4ed86e24688ed44ab6035b7e9af785`. Jobs `constraint-lab` and `books` both completed. The constraint-lab job reported 167 passed in 83.31 seconds.

This execution file is a later commit. The run id is not a run id for the commit that adds this file.
