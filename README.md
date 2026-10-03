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

The Constraint Laboratory is the active experimental programme on `research/constraint-lab-v0.1`. Its charter, engine, and generation records live under `constraint-lab/`.

## Licence

[MIT](LICENSE). Copyright (c) 2026 gellsmore-svg.
