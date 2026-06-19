---
type: Module
title: Analysis sweeps
description: Batch parameter sweeps over the shared model — the coherence sweep (grammar signatures, region preservation rates, identity-gate flip sensitivity, example sequence traces) and geometry sweeps that perturb explicit fields and derive coherence variables from them.
resource: https://github.com/gellsmore-svg/Relational-Substrate/tree/main/analysis
tags: [relational-substrate, analysis, sweeps, coherence]
timestamp: 2026-06-19T00:00:00Z
---

# Analysis sweeps (`analysis/*.mjs`)

Batch exploration of the [model](model.md)'s parameter space, sharing the same rule
model as the [UI](sandbox-ui.md):

- **Coherence sweep** — records **grammar signatures**, high/low-grammar region
  **preservation rates**, [identity-gate](../concepts/closure-gate-and-identity.md)
  **flip sensitivity** under small perturbations, and example
  [sequence traces](../concepts/resilience-and-regimes.md).
- **Geometry sweeps** (e.g. ethane torsion, boundary-transition) — perturb explicit
  geometry fields (bond length, bond angle, torsion, ring-closure distance,
  polarity vector, steric clearance, valence mismatch); [coherence](../concepts/coherence.md)
  variables are then **derived** from those fields. The geometry fields are inputs,
  not [substrate objects](../concepts/guardrail.md).
- **Supporting data** — `descriptor-registry.json` and `evidence-ledger.mjs` track
  descriptors and an evidence ledger across runs.

Sweeps run via Node (`.mjs`) and feed the [reports](reports.md). The external
calibration comparators are documented separately under [benchmarks](benchmarks.md).
