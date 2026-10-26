# Execution 007 attempt 1 — aborted

This record does not close Prompt 007. It does not accept a Generation 7 result.

Prompt 007 was executed on branch `research/constraint-lab-v0.7`. The useful committed implementation on that branch is `d0abedfd382396deecf4a1ffff1e0a0fe331920a` through `5787f2c0f2664d2daa3125997aaa5267a3059ac0`. Those commits are preserved. They are not a completed generation.

## Known facts

- Prompt 007 was executed.
- The run continued for many hours.
- The foreground terminal stopped providing useful visible progress.
- The machine remained computationally active.
- The user could not tell whether the experiment was progressing or hung.
- The run was manually terminated.
- Completion was not established.
- Partial outputs are not accepted as a completed generation without validation.

The established failure is lack of bounded execution and observability. A root cause inside the solver is not claimed here.

## Files observed when this recovery was assessed

Observed on 2026-10-12. No `rs_constraint_lab` process was running. `constraint-lab/generated/` is gitignored, so these files were never a commit.

The directory is kept as a forensic artifact at:

```text
constraint-lab/generated/forensic/generation-007-attempt-1/
```

`progress.json` recorded:

```text
status: IN_PROGRESS
start_time: 2026-10-05T10:02:35+00:00
last_heartbeat: 2026-10-05T16:50:14+00:00
completed: 1
running: 1
failed: 0
quarantined: 0
total_shards: 2
workers_last: 2
spec_hash: 3bd1164efde699e57784d22ea24c9026e724e134939ff9d4743566cb23e6cf0d
```

Shard `aca9c6ed43cdbb71cb432732` (ordinal 0) had only `running.json`. That file records `pid` 2034290 and `started_at` `2026-10-05T10:02:35+00:00`. It has no result file and no receipt.

Shard `40f54eebb0d913327d887418` (ordinal 1, combination range 14:28) has a receipt. The receipt records `finished_at` `2026-10-05T10:07:29+00:00`, `elapsed_seconds` 294.282878, and `analysed` 14. That receipt is not a generation result. The shard result has no per-evaluation item id, so it is not imported into Generation 7.

## What is reused

The calibration mathematics, the Generation 7 specification, the v0.7 tests, Review 006, and Prompt 007's stored agent input are reused on `research/constraint-lab-v0.7-resumable` only as code and provenance. The forensic shard is not a cache of completed items.

Prompt 007 is not overwritten. Prompt 007R is a different instruction.
