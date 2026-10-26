# Generation 007B execution

Generation 007B uses the Generation 007R supervisor. It does not run as one shard. A worker process owns one batch and exits. Completed items and batch receipts stay on disk, so a killed terminal does not discard finished work.

Scientific root: `constraint-lab/generated/generation-007b/`.

Preflight root: `constraint-lab/generated/generation-007b-preflight/`.

Smoke root: `constraint-lab/generated/generation-007b-smoke/`.

All three are gitignored. The frozen counts are in `constraint-lab/docs/generation-007b-work-count.md`.

`python -m rs_constraint_lab run` on this analysis is refused. The command to use is `generation007b`.

## Commands

From `constraint-lab/`:

```bash
python -m rs_constraint_lab generation007b plan
python -m rs_constraint_lab generation007b benchmark
python -m rs_constraint_lab generation007b smoke
python -m rs_constraint_lab generation007b preflight
python -m rs_constraint_lab generation007b start
python -m rs_constraint_lab generation007b status
python -m rs_constraint_lab generation007b status --watch 5
python -m rs_constraint_lab generation007b stop
python -m rs_constraint_lab generation007b restart
python -m rs_constraint_lab generation007b verify --require-complete
python -m rs_constraint_lab generation007b merge
```

`restart` is `start` on the same root. Completed items are not solved again.

`run-next` executes one batch and returns, with `--max-wall` defaulting to 60 seconds. `run-batches --count 5` executes five batches and returns. `supervise` runs until the plan is complete or stopped. Start that through `scripts/start-generation-007b.sh`, which returns after the supervisor has its own session.

`benchmark` measures the two-level pair-point item and writes `plan/batch-policy.json`. Until that file exists, each batch contains one item. The count is `floor(45 / p90)`, reduced while `count * p90 > 60` or `count * max > 100`. The watchdog stays 120 seconds. Smoke and preflight use their own roots. Copy `plan/batch-policy.json` into those roots after their plans exist. The measurement below is the copy source.

Measured on this machine on 2026-10-12, nine pair-point samples, numeric threads pinned to 1.

| Kind | p50 | p90 | max | items per batch |
| --- | --- | --- | --- | --- |
| pair point | 0.290s | 0.315s | 0.315s | 142 |
| target singleton | 0.290s | 0.315s | 0.315s | 142 |
| target composition | not timed | not timed | not timed | 1 |
| control composition | not timed | not timed | not timed | 1 |

The target-singleton row uses the pair-point samples. It was not timed as its own kind. Composition stays at one item per batch.

The two-level reference gap on that run was 0, below `1e-10`. The match tolerance stays `1e-8`.

An atomic item is one canonical two-level control at one `(m_off, m_on)`, one rho, and one alphabet. It returns both singleton passage directions. The planner reads stored points and requests the next stencil. It does not call the kernel.

## Watching another terminal

Linux / WSL:

```bash
python -m rs_constraint_lab generation007b status --watch 5
tail -n 30 -f constraint-lab/generated/generation-007b/progress/progress.log
```

`status.json` is `constraint-lab/generated/generation-007b/progress/status.json`. The supervisor writes it when it starts, before the first heartbeat interval, and rewrites it on every heartbeat. `running_batches` has one row for each live worker: `batch_id`, `worker_pid`, `items`, `started_at`, `elapsed_seconds`, `watchdog_seconds`. `current_batch_id` remains the first live worker.

PowerShell, not executed on this Linux host:

```powershell
Get-Content .\constraint-lab\generated\generation-007b\progress\progress.log -Tail 30 -Wait
```

## Background start and stop

```bash
constraint-lab/scripts/start-generation-007b.sh
constraint-lab/scripts/stop-generation-007b.sh
constraint-lab/scripts/watch-generation-007b.sh
```

PowerShell equivalents are `start-generation-007b.ps1`, `stop-generation-007b.ps1`, and `watch-generation-007b.ps1` in the same directory. They were written for Windows. They were not executed on this Linux host. Native PowerShell validation is not claimed. That is not a blocker for the Linux scientific run.

`stop` asks the supervisor to finish the current batch, write `STOPPED`, and release the lock. A hard kill is recovered by the next start: valid items remain, and a batch without a receipt is scheduled again for the items that were not published.

A second live supervisor is refused. A lock whose process is gone is recovered and logged.

## What a batch is allowed to do

A normal batch targets 30–60 seconds. The watchdog is 120 seconds. The supervisor heartbeats at least every 10 seconds, including while a worker is still inside a solve. Two workers is the default. Each worker sets the numeric libraries to one thread.

On timeout the supervisor kills the worker process group, keeps published items, and splits the unfinished items. A single item that times out twice after the first attempt is quarantined. Other items continue.

Profiles:

```text
smoke       one logical problem, its coarse grid, adaptive cap 250, no composition
preflight   15 logical problems, representation and cost only
census      42 problems, then composition, then the robustness probes
```

Smoke and preflight do not schedule composition. The census schedules composition only for calibrations whose status is `represented`. `unresolved_at_cap` and unrepresented calibrations stay in the merge and do not receive composition or robustness items.

## Planner corrections before the census

Three corrections were made after the first smoke and the first preflight. They do not change the frozen selection rule or the tolerance.

- A named nominal of zero uses Generation 7 `log_distance`. The selector does not divide by that nominal.
- Newton starts only after both log10 widths are at most 0.05. A subdivision stencil that is already stored does not promote a wide basin to Newton.
- A missing Jacobian sample requests a durable point. It does not mark the basin exhausted.

An uncaught supervisor exception is written to `last_error` before the process exits. The state name remains `STOPPED`.

The corrected preflight is the one recorded in Pass 2 of `docs/generation-007b-design-passes.md`.

## Census close

The census root is `generated/generation-007b`. Its scientific reading is `reports/generation-007b-two-level-pair-face-control.md`. The machine-readable rows are `reports/generation-007b-tables.json`, rendered from `generated/generation-007b/merge/summary.json`. `generated/` stays gitignored.

`verify --require-complete` accepts a Generation 007B calibration whose `status` is `represented`, `unrepresented`, or `unresolved_at_cap`. Generation 7 still requires `convergence_status`. Merge rows for 007B are keyed by `calibration_id`, because one target can have more than one live face. The scalar-erasure state-shape join reads `generated/generation-007/merge/summary.json` and does not refit that control.

The census supervisor started at `2026-10-12T12:45:38Z` and its last activity is `2026-10-12T14:19:04Z`. Status is `COMPLETE`. Items are 4,539 / 4,539. Calibrations are 42 / 42. Unresolved calibrations, timeouts, retries, quarantines, and `last_error` are 0. Receipts are 196. There was no resume and no stale-lock event on this root. `cache_hits` and `cache_misses` in the status file are 0 because the 007B counter returns those fields as zero. They are not a kernel-cache measurement.
