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
| `accounting` | Coverage identity for one cell |
| `kernel` | Multiplicative toggle kernel, halt completion, modal and support maps |
| `exact` | SCCs, period, rational and float64 stationary distributions, absorption |
| `observables` | Light and heavy measurements, neutral sentences |
| `trajectory` | Event-sourced sampling and replay comparison |
| `spec` | Specification schema `rs-constraint-lab.experiment/v1` |
| `generation` | Exhaustive cell runner, family index, motif selection |
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

Canonical enumeration walks combinations in id order and keeps an orbit only when its sorted id tuple is the least image. Family identity is the SHA-256 prefix of `N`, the modal-map hash, and the support-map hash. The first-seen member of a family is the one with smallest cardinality, then the earliest combination in that enumeration. Stochastic order does not enter the exact census. Exemplar traces use a fixed seed list.

## What is refused

- `H > 0` or `L > 0` raises `NotImplementedError` from the choreography.
- A non-empty history or constraint-state argument does the same.
- `hypergraph` and `simplicial` raise `NotImplementedError` from their slot counters, and the CLI refuses to run them.
- `neutral` in a specification is a validation error.

## Profiling

Cell runtime is stored on the summary. Multiprocessing is not used. A later generation that needs it should record the profile that justified the split, and should keep semantic results independent of worker order.
