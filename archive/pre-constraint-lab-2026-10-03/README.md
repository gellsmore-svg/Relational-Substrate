# Archive: pre-constraint-lab programme

**Archival date:** 2026-10-03

**Source commit:** `06cb0dc0be6aa952639a3337cf95606f1feaa4c4`

**Immutable reference:** Git tag `pre-constraint-lab-2026-10-03` (annotated), pointing at that commit. The tag is the safety point taken before this directory was assembled. The branch `research/constraint-lab-v0.1` starts from the same commit.

## Why this archive exists

On 2026-10-03 the Relational Substrate repository opened a new primary research avenue: the Constraint Laboratory, a pre-geometric study of constraint grammars on a stochastic relational possibility space.

The modelling programme that was active before that boundary remains in this directory. Archival is a historical boundary. It is not a repudiation, a retraction, or a claim that the earlier results were worthless. Those results stay available for comparison, audit, and reuse.

The books were not archived. They remain the active manuscripts at the repository root (`books/`).

## What this directory contains

The pre-laboratory programme accumulated several phases. They share one checkout here because that is how they were developed.

| Path | Phase |
| --- | --- |
| `src/`, `index.html` | Browser sandbox for route, closure, phase, charge, and continuity. Version 0.1 UI and the later grammar-state model. |
| `analysis/` | Analysis bench: molecule, material, interface, and electromagnetic comparators; stress-history and order-effect studies; cross-domain directional checks; predeclaration gates and evidence ledgers. |
| `docs/` | Modelling and review documents: validation status, task map, vorton / topological-substrate proposal, theta-term scope, coherence notes. |
| `research/` | Research notes and case studies from those phases. |
| `instantiation/` | Numerical topology: Hopf number, the `H = p·q` selection rule, emergent magnetic sector, hedgehog Dirac zero mode, theta parity. |
| `okf/` | Concept and module cards for the sandbox grammar. |
| `scripts/` | Legacy report, guardrail, and canvas-verification scripts. EPUB scripts were **not** moved; they stay at the repository root. |
| `github-workflows/ci.yml` | The Node CI workflow that built the sandbox and regenerated reports. |
| `package.json`, `package-lock.json` | The legacy npm command surface (`vite`, `three`, the `analysis/` scripts). |
| `legacy-root-README.md` | The root README as it stood at the source commit. |
| `CONTRIBUTING.md` | Contribution rules for the sandbox and benchmark bench. |
| `.restart.md` | Chronological restart notes through 2026-06-24. |

Local, untracked build products (`node_modules/`, `dist/`, `verification/`, `analysis/out/`, `analysis/source-cache/`, `instantiation/.venv/`) were moved here with the programme when they were present on the machine that performed the archive. They are gitignored. A fresh clone does not contain them.

## How to run the legacy programme

Work from **this directory**, not from the repository root. The root `package.json` now only rebuilds the books.

```bash
cd archive/pre-constraint-lab-2026-10-03
npm ci
npm run dev          # browser sandbox
npm test             # reports + production build
npm run sweep        # coherence sweep
npm run guardrails
```

Instantiation numerics use the Python files and `requirements.txt` in `instantiation/`. From the source commit's own notes, the checked entry points include:

```bash
cd archive/pre-constraint-lab-2026-10-03/instantiation
python3 hopf_invariant.py
python3 selection_rule.py
python3 emergent_magnetic.py
python3 hedgehog_dirac.py
python3 theta_parity.py
```

Those runs are heavy (spectral integrals on 3D grids) and are not part of the Constraint Laboratory CI.

The old report generator writes under `analysis/out/`, which remains gitignored:

```bash
npm run reports
```

## Where the old root files live

| Former root path | Location in this archive |
| --- | --- |
| `README.md` | `legacy-root-README.md` |
| `CONTRIBUTING.md` | `CONTRIBUTING.md` |
| `package.json` | `package.json` |
| `package-lock.json` | `package-lock.json` |
| `.restart.md` | `.restart.md` |
| `.github/workflows/ci.yml` | `github-workflows/ci.yml` |

## Relationship to the Constraint Laboratory

The laboratory does not import this programme's geometric, nematic, vorton, particle, or closure-score assumptions into its primitive grammar. This archive is the comparison record those later questions can be set against. Interpretation, when it happens, belongs in the laboratory's interpretation layer.
