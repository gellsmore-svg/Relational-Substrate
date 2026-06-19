---
type: Concept
title: Admissibility & outcomes
description: When open transient order meets closed stable order, admissibility conditions (boundary compatibility, route continuity, phase alignment, charge tension, storage, scattering, reseating) determine an outcome split into four fractions — admitted, returned, stored, and scattered.
resource: https://github.com/gellsmore-svg/Relational-Substrate/blob/main/src/model.js
tags: [relational-substrate, admissibility, outcomes, calculateOutcome]
timestamp: 2026-06-19T00:00:00Z
---

# Admissibility & outcomes

The central event the model describes: **open transient order meets closed stable
order under admissibility conditions**. `calculateOutcome(input)` takes the
[grammar](substrate-grammar.md) plus admissibility controls — boundary
compatibility, route continuity, storage, scattering, reseating, phase alignment,
and charge tension — and produces an **outcome split** into four fractions:

- **admitted** — order that is accepted into the closed form;
- **returned** — order turned back at the boundary;
- **stored** — order held in a transient/buffered state;
- **scattered** — order dispersed (lost coherence).

The same call yields the [closure gate metrics](closure-gate-and-identity.md) and
the [coherence](coherence.md) value. Because the rule model is shared, the browser
[sandbox](../modules/sandbox-ui.md) and the batch [sweeps](../modules/analysis-sweeps.md)
compute the same outcome from the same thresholds. This is a relational
admissibility model, not a transport or reaction simulation — see the
[guardrail](guardrail.md).
