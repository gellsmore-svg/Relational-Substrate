# RS Constraint Laboratory

The Constraint Laboratory explores the grammar of constraints acting on a stochastic relational possibility space. It begins pre-geometrically, at small entity counts, and exhausts each bounded grammar cell before the next increase in expressive depth.

The governing question is:

> Given a stochastic space of relational possibility, what is the smallest grammar of constraints capable of producing the families of organisation, persistence, dissolution, transformation and higher-order structure that emerge from it?

Under the working premises in [docs/research-charter.md](docs/research-charter.md), a later question is whether those grammars begin to reveal a coherent reusable architecture of the designed creaturely runtime. The laboratory does not treat a simulation result as a certificate of that ontology.

## Layout

```text
docs/            charter, formalism, literature map, roadmap
src/             engine
experiments/     specifications and published manifests
catalogue/       motif records and family indexes small enough to commit
reports/         generation reports and summary tables
exemplars/       selected replayable trajectories
tests/
generated/       bulk run output (gitignored)
```

`books/` stays at the repository root. The pre-2026-10-03 modelling programme stays in `archive/pre-constraint-lab-2026-10-03/`.

## Install

Python 3.11 or newer. From this directory:

```bash
python -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
```

The only runtime dependency is NumPy, used for stationary solves on state spaces larger than 16. Canonical labelling for `N ≤ 5` uses the standard-library symmetric group. The pinned environment used for Generation 1 is `requirements.lock`.

## Commands

```bash
rs-lab inspect-space experiments/specs/generation-001.json
rs-lab enumerate states experiments/specs/generation-001.json --n 3
rs-lab enumerate constraints experiments/specs/generation-001.json --n 3
rs-lab exact experiments/specs/generation-000.json --out generated/generation-000
rs-lab run experiments/specs/generation-001.json --out generated/generation-001 --publish .
rs-lab replay exemplars/<run-id>.json
rs-lab analyze experiments/manifests/generation-001-pregeometric-pairwise-summary.json
rs-lab compare experiments/manifests/generation-001-pregeometric-pairwise-summary.json <id>
rs-lab catalogue build experiments/manifests/generation-001-pregeometric-pairwise-summary.json
rs-lab report experiments/manifests/generation-001-pregeometric-pairwise-summary.json
```

`exact` and `run` both execute the exhaustive cell, including the selected stochastic replays. `run --publish` copies the summary, the singleton tables, family indexes at most 2 MB, selected motif files, and the seed-0 exemplars (plus every N=3 reference seed) into this directory. Bulk output remains under `generated/`.

Generation 0 is the correctness cell and is what CI runs. Generation 1 is the first research census and is too large for CI.

## Reading order

1. [docs/research-charter.md](docs/research-charter.md)
2. [docs/formalism.md](docs/formalism.md)
3. [docs/dimension-model.md](docs/dimension-model.md)
4. [docs/constraint-dsl.md](docs/constraint-dsl.md)
5. [docs/architecture.md](docs/architecture.md)
6. [docs/observables.md](docs/observables.md)
7. [docs/literature-map.md](docs/literature-map.md)
8. [docs/experiment-roadmap.md](docs/experiment-roadmap.md)
9. [docs/interpretation-boundaries.md](docs/interpretation-boundaries.md)
10. The generation report under `reports/`, once that generation has been run.

## Reproducibility

A published summary records the engine version, the git commit of the engine, the Python version, the NumPy version, the platform, the specification hash, the coverage counts, and the runtime. A stochastic run replays from the specification hash, the engine version, the constraint-set id, the initial state, the PRNG name (`python-random-MT19937`), and the seed. Selection uses integer weights and `randrange`.
