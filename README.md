# Relational Substrate

Relational Substrate is a research repository. As of the constraint-laboratory boundary (2026-10-03) it has three roles:

```text
books/            active manuscripts
constraint-lab/   active experiment (this branch)
archive/          historical modelling programme, preserved
```

The books remain at the repository root:

- `books/relational-substrate.md`
- `books/coherent-biblical-ontology-bachelors.md`
- `books/epub/` — validated EPUB 2 editions

Rebuild and validate both EPUBs with:

```bash
npm run books:epub
```

`pandoc` and `epubcheck` are required. See `books/README.md`.

The pre-2026-10-03 modelling programme — browser sandbox, analysis bench, research notes, topological instantiation, and the legacy npm surface — is preserved in:

```text
archive/pre-constraint-lab-2026-10-03/
```

The immutable source commit is tag `pre-constraint-lab-2026-10-03` (`06cb0dc0be6aa952639a3337cf95606f1feaa4c4`). Archival does not repudiate that work. Run instructions and the locations of the old root README, package definition, restart notes, and CI workflow are in the archive README.

The Constraint Laboratory lives under `constraint-lab/`. Generation 1 was produced on `research/constraint-lab-v0.1`. Engine 0.2, on `research/constraint-lab-v0.2`, keeps that record and runs later generations as resumable shards.

Generation 1 searched the memoryless pairwise grammar at `N = 2, 3, 4` and the singletons at `N = 5`, with no geometry. The report is `constraint-lab/reports/generation-001-pregeometric-pairwise.md`. Generation 1b, on `research/constraint-lab-v0.2`, reanalyses that search under structural constraint identity. Generation 2 adds an occupation-count predicate at `N = 3`. Neither rewrites the Generation 1 record. From `constraint-lab/`:

```bash
python -m pip install -e ".[dev]"
python -m rs_constraint_lab inspect-space experiments/specs/generation-001.json
python -m rs_constraint_lab run experiments/specs/generation-001.json --out generated/generation-001 --publish .
python -m rs_constraint_lab replay exemplars/01fce7a65bc87c75.json
```

`npm run books:epub` still rebuilds the books. The laboratory does not rewrite them.

## Licence

[MIT](LICENSE). Copyright (c) 2026 gellsmore-svg.
