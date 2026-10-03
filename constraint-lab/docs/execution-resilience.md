# Execution resilience

The scientific unit of work must be smaller than the lifetime of the machine or process executing it. Once a valid research shard has been completed, an unrelated crash should never require it to be recomputed.

## Item budget

Measured on this development machine on 2026-10-03, one worker, with `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, and `MKL_NUM_THREADS` set to 1.

The opening prefix is not the expensive region of the N=3 triple grammar. Ranks `0:1000` of N=3, `K ≤ 3`, cardinality 3 analysed nothing (0.006s). Weights are generated innermost, so those combinations stack grades on the first structures and the structural-simple filter skips them.

The dense N=3 window at ranks `180000:190000` analysed 9399 rational kernels in 13.6s.

The binding window is N=4, `K ≤ 2`, cardinality 2, ranks `4000:8000`: 3262 canonical-simple float64 kernels in 66.7s. `DEFAULT_SHARD_ITEMS` is 4000 so that window stays inside 60–90 seconds and under 120 seconds. A single 1000-combination slice of the same region (ranks `4000:5000`, 898 kernels) took 18.4s, which is the same rate.

## Miniature interruption

`tests/test_resilience.py` runs an N=2 grammar with two weights, two combinations per shard, and two workers. It stops after two successful shards, plants a stale `running` mark and a truncated `result.json.tmp`, resumes, and compares the merged scientific projection with a one-worker uninterrupted run of the same specification. The projections match, and the receipts written before the stop are unchanged. A permanent injected failure quarantines that shard after three attempts and leaves the generation `PARTIAL`. A one-shot failure completes on the next attempt and matches a clean run. A changed semantic version, specification hash, or NumPy version is refused before `progress.json` is modified.

## Filesystem placement

Under WSL, `/mnt/c` is a 9p drvfs mount. Forty small atomic fsync writes took 0.109s under `/tmp` and 0.377s under `/mnt/c/Users/Public`. That comparison is latency only. Generation output goes on the Linux filesystem.

## Generation 2 interruption

The occupation-threshold generation was stopped on purpose with `--max-shards 4` and then resumed. This was not a killed process. The miniature test above is a separate check.

Interrupted invocation, from `constraint-lab/`:

```bash
.venv/bin/python -m rs_constraint_lab run experiments/specs/generation-002.json \
  --out generated/generation-002-interrupted \
  --workers 2 --max-shards 4 \
  --compare-to generated/generation-001b-structurally-normalised
```

Exit 0. The plan has 18 shards. Four completed, in this order, and their receipt SHA-256 values were recorded before the resume:

```text
f331be5730dca47a8ae15636  47979beb68f1308a016e0844f4037d0ebd1a2ff4b26184a7bb48b6b7dcad6165
b706904d6bd67334fcb5628e  1e15a75e0056f19c59e7b0049d8a167e7453ed451f06d2bdb0b8ebe12a86b1f1
75133b4248ed554cb6019bc1  b1a10d9fbb7afcbdc3b59ed2301785afa75f0f94c9ee322848c794d0825e2ec1
cd7d5cb0882fc09adad9acdf  57fb936cacae9bee865a9f22b372a504e94e3dbd3d44474547117a75f0b8ff37
```

Resume:

```bash
.venv/bin/python -m rs_constraint_lab resume generated/generation-002-interrupted \
  --workers 2 \
  --compare-to generated/generation-001b-structurally-normalised
```

Exit 0. Status `COMPLETE`: 18 completed, 0 failed, 0 quarantined. The four receipts above were byte-identical after the resume. Workers were 2 on both invocations.

Clean invocation, a new directory:

```bash
.venv/bin/python -m rs_constraint_lab run experiments/specs/generation-002.json \
  --out generated/generation-002-occupation-threshold \
  --workers 2 \
  --compare-to generated/generation-001b-structurally-normalised \
  --publish .
```

Exit 0. Wall clock 13.169 seconds. Shard-work sum 20.220 seconds. Shard completion order differed from the resumed run.

`scientific_projection` of the resumed summary and the clean summary is equal. The cited census is the clean directory. The interrupted directory is the resilience evidence and is not published. Receipt bytes differ between the two directories because a receipt carries timestamps; the scientific projection does not.
