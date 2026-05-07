# Contributing

Relational Substrate is a research sandbox. Contributions should preserve the ontology boundaries and evidential discipline of the project.

## Ground Rules

- Do not claim that the sandbox proves a substrate exists.
- Do not describe rendered geometry, molecules, lattices, materials, or interfaces as substrate objects.
- Keep the T0 / T1 / T2 distinction explicit.
- Use inferential convergence language rather than proof-framing.
- Use equivalence-with-unification language rather than displacement or replacement claims.
- Treat conventional domain models as comparators, not enemies.
- Prefer held-out or externally anchored checks over same-layer expansion.
- Quantify limitations when possible.

## Expected Changes

Good contributions usually do one of the following:

- Add a benchmark with a named comparator and clear pass/fail criteria.
- Tighten an existing benchmark tolerance or limitation.
- Improve reproducibility of `npm run reports`.
- Improve review documentation without strengthening claims beyond evidence.
- Add a non-molecular/material validation target that exercises the unification thesis.

## Before Opening a Pull Request

Run:

```bash
npm ci
npm run build
npm run reports
```

Generated files under `analysis/out/`, `dist/`, `node_modules/`, and `verification/` are ignored. If a generated report needs to become part of the public review packet, copy it into `docs/` deliberately and explain why.

