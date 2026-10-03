---
type: Concept
title: Resilience & regimes
description: Beyond single snapshots, simulateSequence runs multi-step traces with simple memory carry (accumulated continuity + stress) to ask whether identity survives a history of encounters; resilience, cross-regime durability, regime stability/transition, and Monte-Carlo durability quantify that survival across regimes.
resource: https://github.com/gellsmore-svg/Relational-Substrate/blob/main/src/model.js
tags: [relational-substrate, resilience, durability, regimes, sequence]
timestamp: 2026-06-19T00:00:00Z
---

# Resilience & regimes

The model has moved from single-interaction snapshots toward **"does identity
survive a short history of encounters?"** — while staying strictly
[abstract](guardrail.md):

- **`simulateSequence(base, n)`** — multi-step traces with simple **memory carry**
  (accumulated continuity + stress) and consumption, so an
  [identity](closure-gate-and-identity.md) is tested over a sequence, not one event.
- **`measureResilience` / `computeMonteCarloDurability`** — how robustly identity
  persists under perturbation / random sampling.
- **`computeCrossRegimeDurability` / `computeRegimeStability` / `testRegimeTransition`
  / `computeTransitionFragility`** (+ `REGIME_TRANSITION_PROFILES`) — how durable
  order is *across regimes* and how fragile the transitions between them are.
- **`findHighStabilitySettings` / `findBestRegimeForDurability`** — search for the
  [grammar](substrate-grammar.md) settings/regimes where identity is most durable.

These turn the model into a study of **persistence**: which grammars hold identity
through change. Reported by the [analysis sweeps](../modules/analysis-sweeps.md).
