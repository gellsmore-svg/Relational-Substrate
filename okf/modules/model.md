---
type: Module
title: The model (src/model.js)
description: The shared pure-logic core — deriveGrammar and calculateOutcome, the closed/transient forms and scenario presets, simulateSequence for multi-step traces, and the resilience/durability/regime-stability functions. The single source of truth driving both the UI and the sweeps.
resource: https://github.com/gellsmore-svg/Relational-Substrate/blob/main/src/model.js
tags: [relational-substrate, model, pure-logic]
timestamp: 2026-06-19T00:00:00Z
---

# The model (`src/model.js`)

The **single pure-logic core** — deterministic functions with no UI or I/O — that
both the [sandbox](sandbox-ui.md) and the [sweeps](analysis-sweeps.md) import:

- **`deriveGrammar(input)`** — derive the explicit [grammar](../concepts/substrate-grammar.md)
  state from inputs.
- **`calculateOutcome(input, options)`** — the central calculation:
  [outcome fractions](../concepts/admissibility-and-outcomes.md),
  [closure-gate metrics + identity](../concepts/closure-gate-and-identity.md), and
  [coherence](../concepts/coherence.md).
- **`closedForms` / `transientForms` / `scenarios` / `scenarioPresets`** — the
  selectable forms and A/B/C presets.
- **`simulateSequence(base, n)`** — [multi-step traces](../concepts/resilience-and-regimes.md)
  with memory carry.
- **`measureResilience`, `computeMonteCarloDurability`, `computeCrossRegimeDurability`,
  `computeRegimeStability`, `testRegimeTransition`, `computeTransitionFragility`,
  `findHighStabilitySettings`, `findBestRegimeForDurability`** (+
  `REGIME_TRANSITION_PROFILES`) — the [resilience & regime](../concepts/resilience-and-regimes.md)
  analysis.

Keeping the rules here, pure and shared, is what makes the screen and the batch
search provably consistent.
