---
type: Project
title: Relational Substrate
description: A visual and analytical sandbox for the substrate grammar — route, closure, phase, charge, and continuity. A strictly abstract, browser-based conceptual model of "open transient order meeting closed stable order under admissibility conditions," with a pure-logic core, an interactive UI, and a battery of diagnostic sweeps and benchmarks.
resource: https://github.com/gellsmore-svg/Relational-Substrate
tags: [relational-substrate, substrate-grammar, coherence, conceptual-model, sandbox]
timestamp: 2026-06-19T00:00:00Z
---

# Relational Substrate

Relational Substrate is a visual and analytical **sandbox for the substrate
grammar**: route, closure, phase, charge, and continuity. It is a strictly
abstract, browser-based conceptual model of:

```text
open transient order
meeting
closed stable order
under admissibility conditions
```

It does **not** simulate physics directly and does **not** treat rendered curves,
molecules, lattices, or materials as substrate objects — see the
[guardrail](concepts/guardrail.md). This bundle is an
[Open Knowledge Format](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)
description of the model's concepts and components.

## Map

- **[Concepts](concepts/index.md)** — the substrate grammar, admissibility &
  outcomes, the closure gate & identity, coherence, resilience across regimes, and
  the abstraction guardrail.
- **[Modules](modules/index.md)** — the pure-logic model, the browser sandbox UI,
  the analysis sweeps, the external benchmarks, and the reports.

## At a glance

- One shared **pure-logic core** (`src/model.js`) drives both the screen and the
  batch sweeps — see [the model](modules/model.md).
- The five grammar elements are first-class factors; **coherence** rewards
  alignment and penalises tension/scatter — see [coherence](concepts/coherence.md).
- Outcomes split into **admitted / returned / stored / scattered**; a **closure
  gate** yields an **identity score**.
- License: see LICENSE. JS / Vite (`npm run dev`).
