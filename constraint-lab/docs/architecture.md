# Architecture

## Package

`rs_constraint_lab` is one package. The modules follow the data flow rather than a deep tree.

| Module | Responsibility |
| --- | --- |
| `state` | Bitset states, edge order, exact `S_N` action on states |
| `semantics` | Named graph / hypergraph / simplicial axes; only graph executes |
| `weights` | Grade table and geometric alphabets |
| `constraints` | Normal-form constraint, parser, choreography hook |
| `grammar` | Labelled enumeration, permutation image table, canonical id tuples |
| `accounting` | Coverage identity for one cell, including the arity bound |
| `kernel` | Multiplicative toggle kernel, halt completion, modal and support maps |
| `exact` | SCCs, period, rational and float64 stationary distributions, absorption |
| `observables` | Light and heavy measurements, neutral sentences, exact fraction fields |
| `dynamics` | Canonical support, modal, kernel, and observable-signature identities |
| `combinadic` | Lexicographic combination rank and successor |
| `durable` | Atomic write, fsync, and content hash |
| `analysis` | One shard: canonical sets, exact kernels, family aggregates |
| `execution` | Plan, progress, spawn workers, resume, merge |
| `trajectory` | Event-sourced sampling and replay comparison |
| `spec` | Specification schema `rs-constraint-lab.experiment/v1` |
| `generation` | Generation 1 cell runner, retained for that record's definitions |
| `cli` | `rs-lab` |

## Representations

Pairwise state is an integer bitset. Edge `e` is bit `e`. A toggle is `state XOR (1 << e)`. Permutation maps are tables of edge-index images, built once per `N`. Constraint images are integer ids into the labelled grammar, so an orbit check does not re-parse expressions.

Kernels store, per state, the weight of each toggle as a `Fraction` and the normalised successor list. Sparse rows are implicit: a zero weight is omitted from the successor list. Halt rows store the flagged self-loop.

NumPy is used when the recurrent class has more than 16 states. Smaller classes stay in exact rational arithmetic and do not need a matrix library. NetworkX, SciPy, pandas, igraph, HyperNetX, XGI, and GUDHI are not dependencies. They become candidates when a hypergraph cell, a simplicial cell, or a clustering task needs them.

## Experiment data

```text
SOURCE / SPECS            committed (experiments/specs)
SMALL CANONICAL RESULTS   committed when they fit the size rule
SUMMARY TABLES            committed (reports/tables, manifests)
SELECTED EXEMPLARS        committed (exemplars)
BULK RUN DATA             generated/  (gitignored)
```

The family index is committed when the JSONL file is at most 2 MB. Larger indexes stay in `generated/` and are regenerated from the specification. The summary still carries a histogram, the coverage counts, and the ids of the motif files that were selected. Motif selection is deterministic and capped at 48 families per cell: every baseline-equivalent family, then structural families of small cardinality and large dissolution shift, then extreme closing bias, then extreme rise-then-release excess, then a few measure-only families.

Singleton tables are committed in full. They are the complete heavy record of every canonical one-constraint grammar in the cell.

## Determinism

Canonical enumeration walks combinations in id order and keeps an orbit only when its sorted id tuple is the least image. Stochastic order does not enter the exact census. Exemplar traces use a fixed seed list.

Generation 1, produced by `generation.py`, identifies a family by the 16-hex SHA-256 prefix of `N`, the labelled modal-map hash, and the labelled support-map hash. Heavy analysis in that runner is stored for the first-seen member. That record is historical and is not recomputed in place.

From engine 0.2 the executed family identifiers are full SHA-256 digests of tokens that have already been reduced under `S_N`. Support, mode, the exact rational kernel, and the observable signature are separate identifiers. Qualitative family id is the hash of `N`, the canonical support id, and the canonical modal id. It is the descendant of the Generation 1 family, not the same string. Heavy analysis runs for every canonical set the composition mode keeps. Merged counts, ranges, and example lists do not depend on which worker finishes first.

## Execution

The scientific unit of work must be smaller than the lifetime of the machine or process executing it. Once a valid research shard has been completed, an unrelated crash should never require it to be recomputed.

The operational form is: prefer bounded, independently reproducible, idempotent units of work with durable checkpoints, so completed progress is monotonic and interruption is cheap. No expensive research result may depend on one long-lived process completing successfully.

A generation is a cell, then a cardinality, then a deterministic shard, then a range of canonical constraint-set work items. The shard id is a hash of the engine semantic identity, the specification hash, the cell coordinate, the cardinality, the half-open combination range, and the analysis mode. It does not include the clock, the process id, or the attempt number. The git commit is provenance on the run header only.

Each worker writes a temporary file, flushes and fsyncs it, validates the JSON, and publishes it with `os.replace`. The completion receipt is a second atomic file. A truncated `*.tmp` is not a result. Workers do not append to a shared JSONL file. The coordinator merges completed shard files afterward. `running` without a valid receipt becomes pending on the next resume. A shard that fails three times is quarantined and the rest of the generation continues. The generation status is `COMPLETE`, `PARTIAL`, or `FAILED`. An intentional early stop remains `IN_PROGRESS`.

The default pool has 2 workers. `--workers N` raises that bound. The pool uses the `spawn` start method, including when there is one worker, so Linux and Windows exercise the same process model. Each worker handles one shard and is then replaced (`max_tasks_per_child = 1`). `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, and `MKL_NUM_THREADS` default to 1 so a float64 solve does not also multiply threads inside the worker.

`rs-lab plan` prints the grammar size, the combination count, and the shard count and writes nothing. `rs-lab run` resumes when `plan.json` is already present and the header matches. A changed semantic version, specification hash, grammar, normalisation, item budget, Python minor version, or NumPy version is refused before the progress file is modified.

The item budget is 4000 combinations. On this machine the measured worst window at that budget was an N=4 cardinality-2 block of float64 kernels, 66.7 seconds. The N=3 opening prefix is not that window: weights are generated innermost, so the first combinations stack grades on the first structures and are cheap to skip. Later N=3 windows are dense and still shorter than the N=4 window at the same item count.

Output belongs on the Linux filesystem when the laboratory is running under WSL. `/mnt/c` on this machine is a 9p drvfs mount. Forty small atomic fsync writes took 0.109s under `/tmp` and 0.377s under `/mnt/c/Users/Public`. That is a latency measurement, not a crash-durability result. The launchers are `scripts/run-lab.sh` and `scripts/run-lab.ps1`. Both call `python -m rs_constraint_lab`.

## What is refused

- `H > 0` or `L > 0` raises `NotImplementedError` from the choreography.
- A non-empty history or constraint-state argument does the same.
- `hypergraph` and `simplicial` raise `NotImplementedError` from their slot counters, and the CLI refuses to run them.
- `neutral` in a specification is a validation error.
- A declared `G`, `S`, `H`, `L`, or `O` other than the implemented value (`0, 0, 0, 0, 2`) is a validation error. Absence means that implemented value.
- `A_max`, when present, drops every constraint whose arity exceeds it. Arity counts entities named by the action and the edge conditions. A count literal names no entity.
- An unknown composition, analysis mode, or predicate is a validation error. The executable analysis is `heavy-every-canonical`. Compositions are `structural-simple` (the default) and `stacked-weight`. Predicates are `edge` and `count`.
