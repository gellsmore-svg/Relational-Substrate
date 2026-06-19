---
type: Module
title: Sandbox UI
description: The interactive browser sandbox — selectable closed and open transient forms, A/B/C scenario presets, sliders for the admissibility controls, live readouts of the grammar state, closure-gate metrics, grammar-health composite, the route-split visualisation, and a "Run 3-step trace" demo.
resource: https://github.com/gellsmore-svg/Relational-Substrate/blob/main/src/main.js
tags: [relational-substrate, ui, sandbox, browser]
timestamp: 2026-06-19T00:00:00Z
---

# Sandbox UI (`src/main.js`, `index.html`, `src/styles.css`)

The interactive front-end over the shared [model](model.md) (`npm run dev`, a
light, e-ink-friendly theme):

- **Inputs** — selectable [closed forms](../concepts/admissibility-and-outcomes.md)
  (circle / trefoil / double) and open transient forms (straight / sine / ribbon),
  A/B/C scenario presets, and sliders for the admissibility controls: boundary
  compatibility, route continuity, storage, scattering, reseating, **phase
  alignment**, and **charge tension**.
- **Readouts** — the explicit [grammar state](../concepts/substrate-grammar.md)
  (continuity, phaseMatch, chargeTension), the
  [closure-gate metrics](../concepts/closure-gate-and-identity.md) and identity
  score, a closure stress readout, and a **grammar-health composite**
  ([coherence](../concepts/coherence.md)).
- **Visualisation** — the **route-split** view for admitted / returned / stored /
  scattered portions, and a live **"Run 3-step trace"** demo
  ([sequences](../concepts/resilience-and-regimes.md)).

Because it imports the same `src/model.js`, the screen and the batch
[sweeps](analysis-sweeps.md) compute identical results. `verification/` holds
desktop/mobile screenshots of the UI.
