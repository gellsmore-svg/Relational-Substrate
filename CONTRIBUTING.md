# Contributing

Relational Substrate currently has three active layers:

- `books/` — the manuscripts. Treat the prose as read-only unless the task is explicitly a book edit.
- `constraint-lab/` — the active experimental programme.
- `archive/pre-constraint-lab-2026-10-03/` — the historical modelling programme. Preserve it. Do not delete it, and do not silently import its physical assumptions into the laboratory grammar.

The repository licence is the MIT licence at the root.

## Epistemic rules for the laboratory

The laboratory explores, observes, infers, compares, and updates coherence. It does not certify the ontology.

- Keep observation, inference, and RS interpretation in separate layers.
- Prefer: observed, generated, inferred, suggests, tensions with, coherent with, opens a question.
- A formal proof is meaningful inside a declared formal system. It is not a proof of the ontology of reality.
- Do not encode hoped-for outcomes (construction, repair, sacrificial persistence, self-transformation) as primitive search targets.
- Preserve null results, baseline-equivalent rules, fragile parameters, and failed motif candidates.
- Do not describe a sampled region as exhaustive.

## Laboratory changes

A useful change does one of the following:

- extends the grammar, the state semantics, or the exact analysis with a declared coordinate (`N`, `A`, `O`, `G`, `S`, `H`, `K`, `L`, and the relation semantics);
- adds a test that locks a theorem, a canonicalisation orbit, or a replay;
- records a generation with its coverage manifest, including the regions not searched;
- corrects a methodological defect and reruns the affected cell.

Before opening a pull request that touches the laboratory:

```bash
cd constraint-lab
python -m pip install -e ".[dev]"
python -m pytest -q
python -m rs_constraint_lab run experiments/specs/generation-000.json --out generated/generation-000
```

Generation 1 is exhaustive and is not part of CI. Rerun it when a change can alter its manifest, and say so in the pull request.

## Books

Rebuild the EPUB editions from the repository root:

```bash
npm run books:epub
```

That command needs `pandoc` and `epubcheck`. It reads `books/*.md` and `scripts/epub-cleanup.lua`.

## Archive

Run the historical programme from inside the archive directory. See `archive/pre-constraint-lab-2026-10-03/README.md`.
