# Generation 7 execution

Generation 7 does not run as one shard. The supervisor schedules bounded batches. A worker process owns one batch and exits. Completed items and batch receipts stay on disk, so a killed terminal does not discard finished work.

The scientific root is `constraint-lab/generated/generation-007/`. The smoke root is `constraint-lab/generated/generation-007-smoke/`. Both are gitignored.

## Commands

From `constraint-lab/`:

```bash
python -m rs_constraint_lab generation007 plan
python -m rs_constraint_lab generation007 benchmark
python -m rs_constraint_lab generation007 smoke
scripts/start-generation-007.sh
python -m rs_constraint_lab generation007 status
python -m rs_constraint_lab generation007 status --watch 5
python -m rs_constraint_lab generation007 stop
python -m rs_constraint_lab generation007 verify
python -m rs_constraint_lab generation007 merge
```

`run-next` executes one batch and returns. `run-batches --count 5` executes five batches and returns. `supervise` runs until the plan is complete or stopped. Start that through `scripts/start-generation-007.sh`, which returns after the supervisor has its own session.

The same start command resumes a stopped or killed run. Completed items are not solved again.

`benchmark` measures representative items and writes `plan/batch-policy.json`. Until that file exists, each batch contains one item.

Measured on this machine on 2026-10-12, three repeats, numeric threads pinned to 1. The count is `floor(45 / p90)`, reduced while `count * p90 > 60` or `count * max > 100`. The watchdog stays 120 seconds.

| Kind | p50 | p90 | max | items per batch |
| --- | --- | --- | --- | --- |
| multiplier | 0.301s | 0.315s | 0.316s | 142 |
| target singleton | 0.307s | 0.307s | 0.307s | 146 |
| target composition | 0.531s | 0.533s | 0.533s | 84 |
| control composition | 0.532s | 0.545s | 0.545s | 82 |

A multiplier batch of 142 items is about 45 seconds of kernel time before process startup and the atomic item write. The smoke run is the check that the wall time, including those writes, stays inside the watchdog.

## Watching another terminal

Linux / WSL:

```bash
tail -n 30 -f constraint-lab/generated/generation-007/progress/progress.log
```

PowerShell:

```powershell
Get-Content .\constraint-lab\generated\generation-007\progress\progress.log -Tail 30 -Wait
```

Status:

```bash
python -m rs_constraint_lab generation007 status --watch 5
```

`status.json` is `constraint-lab/generated/generation-007/progress/status.json`. The ETA line is the ETA for the current plan. Adaptive calibration can add points after that plan.

## Background start and stop

```bash
constraint-lab/scripts/start-generation-007.sh
constraint-lab/scripts/stop-generation-007.sh
constraint-lab/scripts/watch-generation-007.sh
```

PowerShell equivalents are `start-generation-007.ps1`, `stop-generation-007.ps1`, and `watch-generation-007.ps1` in the same directory. They were written for Windows and were not executed on this Linux host.

`stop` asks the supervisor to finish the current batch, write `STOPPED`, and release the lock. A hard kill is recovered by the next start: valid items remain, and a batch without a receipt is scheduled again for the items that were not published.

A second live supervisor is refused. A lock whose process is gone is recovered and logged.

## What a batch is allowed to do

A normal batch targets 30–60 seconds. The watchdog is 120 seconds. The supervisor heartbeats at least every 10 seconds, including while a worker is still inside a solve. Two workers is the default. Each worker sets the numeric libraries to one thread.

On timeout the supervisor kills the worker process group, keeps published items, and splits the unfinished items. A single item that times out twice after the first attempt is quarantined. Other items continue.

## Sensitivity divergence

The frozen specification lists alphabets `W3` and `W16`. Prompt 007R asks for `rho3 = 1/2` and `rho3 = 2` on the selected robustness rows. Alphabet recalibration is not scheduled. Rho robustness is.
