# Execution 007R — resumable effect-matched controls

This is the execution record for prompt 007R. It closes that prompt. It does not close prompt 007. Prompt 007 remains the aborted attempt in `provenance/executions/007-attempt-1-aborted.md`.

## Prompt

| Field | Value |
| --- | --- |
| prompt_id | 007R |
| agent_input_path | `constraint-lab/provenance/prompts/007R-v0.7-resumable-agent-input.md` |
| agent_input_sha256 | `10e893b0734f74b55adf94e070aa713329d79c1cc4f3ae01d7e61c5e72f34c61` |
| agent_input_bytes | 33191 |
| authored_prompt_path | null |
| authored_prompt_sha256 | null |
| authored_prompt_bytes | null |
| authored_prompt_status | `pending_verbatim_import` |
| relationship of authored to agent input | `unknown` |
| date | 2026-10-12 |
| authoring source | user instruction to the implementing agent |
| target | Grok 4.7 |
| repository | gellsmore-svg/Relational-Substrate |
| starting_branch | `research/constraint-lab-v0.6` |
| starting_commit | `4deef3aa272a3ceadb5c610fcc95eaa24fde3901` |

The stored file is the agent input. It includes one leading newline and one trailing newline. It does not contain its own sha256. No separate authored Markdown was byte-compared. Prompt 007 is not overwritten. Prompt 007's authored metadata stays 36,891 bytes, sha256 `70da6a8f307c4044186f1c9e464f5b343f08e48e8bbe515f6bb336e5079b3f31`, and that hash is not assigned to the stored 007 agent-input file.

## Result

Branch `research/constraint-lab-v0.7-resumable`.

The inclusive commit range produced by prompt 007R, through the analysis report, is:

```text
cd17cb275e194970e4334556edfa0569de1b656e
2e1c22c75b22ab11b76cfa77f6b927cd7f7b2d72
b3449d97a2ed3b139d4aa8bbdded40c32bcbcc8e
47203d3189bebce7c82da302b4a7edd613e337f2
751cc7163dbc418d5235de15a325fce980b2ba69
37134fc4366adbda284960d536b9ebde7838a8db
32bf3652d78d97ef441dfad1dd264e0d0b5b4867
107c7ab30fb0a36ed992e78b637ba3fda7ec5d16
```

The commit that adds this execution file is outside that range. The ledger line that points at this record is that same close-out commit. It is not inside the analysis range above.

The parent of `cd17cb275e194970e4334556edfa0569de1b656e` is `64f851c34489a0497fe74a2562a7bd469462c1dc`. That commit and its ancestors back to `4deef3aa272a3ceadb5c610fcc95eaa24fde3901` are the preserved prompt 007 implementation. They are not a completed Generation 7 result. Branch `research/constraint-lab-v0.7` remains at `5787f2c0f2664d2daa3125997aaa5267a3059ac0` and was not moved.

Experiment id:

- `generation-007-effect-matched-controls`

There is no secondary experiment id. 007B was not run.

Report:

- `constraint-lab/reports/generation-007-effect-matched-controls.md`

Design passes:

- `constraint-lab/docs/generation-007-design-passes.md`

## What ran

The census supervisor was pid 45223, a session leader, started by `scripts/start-generation-007.sh` at `2026-10-12T09:08:33Z`. It wrote `COMPLETE` at `2026-10-12T09:34:28Z` and exited. Workers 2. Heartbeat 10 seconds. Watchdog 120 seconds. Initial items 218. Closed plan 3,880. Completed batches 238. Timeouts 0. Splits 0. Retries 0. Quarantines 0. Resume events 0. Median batch wall 4.303464 seconds. p90 5.600972 seconds. Maximum 27.500368 seconds. Cache hits 3,346. Cache misses 3,936. Calibrations 104, all `converged`.

Merge wrote 28 rows. Local verify `--require-complete` on the census root: `ok` true, `complete` true, items 3,880, receipts 238, `missing_completed` empty, orphans empty, quarantined empty, problems empty, spec hash `3bd1164efde699e57784d22ea24c9026e724e134939ff9d4743566cb23e6cf0d`.

`constraint-lab/generated/` is gitignored. The item files, receipts, and summary are local. CI does not re-run the census. The published numerical record is the report.

The smoke root reached `COMPLETE` at `2026-10-12T08:51:48Z`, pid 35071, 76 items, 5 receipts, both calibrations `smoke_capped`. Its merge summary was written at close-out from those items. Every smoke strategy has `used_as_matched` false. The joint text `m = 1` is a cap marker.

## Divergences from the prompt

- The frozen specification lists sensitivity alphabets `W3` and `W16`. Prompt 007R schedules `rho3 = 1/2` and `rho3 = 2` on the selected rows. Alphabet recalibration was not scheduled.
- The progress log writes `phase=` at start and at completion. Phase during the run is on `status.json`.
- The summary's median batch wall is the upper of the two central receipt walls.
- The smoke run finished with an empty merge directory. The smoke merge file used by verify was written afterwards from the completed items. No smoke kernel was rerun for that merge.
- The census itself did not kill and restart. Resumability is the platform test result, plus durable files. `resume_events` is 0.
- PowerShell start, stop, and watch scripts were written and were not executed on this Linux host.
- The forensic shard was not imported.
- 007B was not run. Graph-class routing was not run.
- Review of this generation is not written here.

## Local checks

Before the report commit, `python -m pytest -q` in `constraint-lab` reported 109 passed in 72.74 seconds. That suite includes the fault-injection tests. It does not include the Generation 7 census.

## CI

Actions run `38233390592` is the push of `107c7ab30fb0a36ed992e78b637ba3fda7ec5d16`. The URL is `https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/38233390592`.

`gh run view 38233390592` reported conclusion success on `107c7ab30fb0a36ed992e78b637ba3fda7ec5d16`. Jobs `constraint-lab` and `books` both completed. The URL is `https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/38233390592`.

This execution file is a later commit. The run id is not a run id for the commit that adds this file.
