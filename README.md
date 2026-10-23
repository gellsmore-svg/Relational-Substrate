# Relational Substrate

**This is a research programme asking whether one relational substrate can
reproduce the *structure* of known physics.** In that substrate a single
topological structure, the **vorton** (a knotted, soliton-like twist, in the
lineage of Kelvin's vortex atom, the Skyrme model and the Hopfion), is the only
structural primitive. Light, electricity and magnetism are downstream
expressions of it, not separate ingredients.

The ontology is set out in the [books](books/README.md). This repository is
where it is tested, by computation and against established physics.

> **Cross-programme research map.** The shared synthesis hub links the
> Constraint Laboratory and Gravity/Time programmes, their contrasts, nulls,
> open questions and metaphors: start at
> [`research-synthesis/generated/index.md`](research-synthesis/generated/index.md).
> How to run and update it:
> [`research-synthesis/docs/runbook.md`](research-synthesis/docs/runbook.md).
> The hub reads pinned programme ledgers; it has no authority over either
> programme's plans, validators or results.

## Where it stands

**Honest ceiling: a coherent, could-fail-tested *structural lens*, not
validated physics.** No number has been reproduced. Every magnitude (α,
masses, binding energies, spectral line positions) is parked as a coupling
and may not be fitted. Confidence is tracked on two separate axes: internal
coherence is high and earned; empirical correctness is low and capped.
([capstone §4](docs/conceptual-phase-completion-2026-07-12.md))

- **Conceptual phase: complete (2026-07-12).** A ladder of rungs T0–T7
  derives, from the substrate's grain and without fitting, the qualitative
  architecture of matter: vorton identity, fermion statistics, charge quantisation,
  emergent electromagnetism, atoms via exclusion shells, and light–vorton
  admissibility.
- **Instantiation phase: under way.** Parameter-free computations that could
  have failed have passed so far: the vorton's identity is an integer Hopf
  number (H = 0.9998, independent of scale); the selection rule `H = p·q`;
  the emergent magnetic sector; and a Dirac-fermion zero-mode mechanism. See
  [instantiation/](instantiation/README.md).
- **Open condition:** the fermion and charge-quantisation results hold only
  if the substrate is in an odd (θ = π) class that is assumed, not generic,
  and could fail. Settling it needs a concrete microscopic model and could
  come out negative.
  ([WP-A](docs/theta-origin-wpa-2026-07-13.md))

## How the work is done

- **Structure over magnitude.** Success means reproducing known physics
  structurally (invariants, signs, discreteness), not finding a novel effect.
- **No fitted parameters, and pre-registered falsifiers.** Each test is
  declared before it is run, and it is allowed to fail.
- **Containment, not fit.** Progress means more of known physics is contained
  by the structure, not that a curve is matched.
- The research method is in [research-methods/](research-methods/README.md).

## Where to start

| If you want… | Read |
|---|---|
| The current model and what it does *not* claim | [Conceptual-phase completion](docs/conceptual-phase-completion-2026-07-12.md) |
| What was decided, and why | [Decision log](docs/decision-log.md) (D1–D9) |
| The computations, with code | [instantiation/](instantiation/README.md) |
| The framework itself | [books/](books/README.md) |
| How the programmes relate | [research-synthesis hub](research-synthesis/generated/index.md) |
| A non-technical account of the *earlier* phase | [Plain-language explainer](docs/plain-language-explainer.md) |

## The earlier phase (archived)

Before the 2026-07 re-anchoring, the programme drifted from physics
unification into a stress-history and order-effect ("coaxing") resilience
programme. [Decision D1](docs/decision-log.md) records this as **objective
drift**. The work is archived, not deleted, and its results stand on their own
terms. A pre-registered order effect was corroborated on open fatigue data,
and the same *directional* law was recorded across four unconnected domains in
the [cross-domain ledger](docs/cross-domain-directional-ledger.md). It
predicted direction but not magnitude, so it was a directional lens, not a
quantitative predictor ([validation status](docs/relational-substrate-validation-status.md)).

## The browser sandbox

```bash
npm install
npm run dev
```

The sandbox and the `analysis/` sweeps and benchmarks belong to the earlier
phase; [decision D4](docs/decision-log.md) retired the `src/model.js` core as
the spine. They still run, and CI builds the full report chain
(`npm run reports`). The command reference is in
[docs/sandbox-and-benchmarks.md](docs/sandbox-and-benchmarks.md).

**Guardrail:** the geometry is a visual grammar only. No mesh, curve, tube,
point or rendered object should be read as a literal substrate cell.

## Books

The framework's primary texts are in [`books/`](books/README.md):

- `books/relational-substrate.md`: the technical ontology volume, *The
  Relational Substrate*.
- `books/coherent-biblical-ontology-bachelors.md`: *Coherent Biblical Ontology*.
- `books/coherent-biblical-ontology-second-edition.md`: *Coherent Biblical
  Ontology*, second edition (October 2026, revision 2.4), with its working
  record in `books/v2/`.

## Also here

- [`okf/`](okf/index.md): a machine- and human-readable concept map in Open
  Knowledge Format.
- [`research/`](research/SOURCES.md): research notes, with a consolidated
  list of the external sources they cite.

[CONTRIBUTING](CONTRIBUTING.md) · MIT, see [LICENSE](LICENSE).
