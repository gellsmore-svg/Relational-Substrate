---
type: Concept
title: Substrate grammar
description: The five first-class elements of the model — route (the path order takes), closure (whether it forms a closed stable form), phase (alignment of oscillatory order), charge (tension between orders), and continuity (persistence of the route) — derived from inputs by deriveGrammar.
resource: https://github.com/gellsmore-svg/Relational-Substrate/blob/main/src/model.js
tags: [relational-substrate, grammar, route, closure, phase, charge, continuity]
timestamp: 2026-06-19T00:00:00Z
---

# Substrate grammar

The model treats **five grammar elements** as first-class inputs/factors:

- **route** — the path that transient order takes toward a closed form.
- **closure** — whether order forms a closed, stable configuration.
- **phase** — alignment of oscillatory order (phase match vs mismatch).
- **charge** — tension between orders (charge tension).
- **continuity** — persistence of the route over an encounter.

A helper, `deriveGrammar(input)`, derives this explicit grammar state
(`continuity`, `phaseMatch`, `chargeTension`, …) from the raw sliders/inputs, so
the grammar is **exposed**, not hidden inside the outcome calculation. The grammar
feeds [coherence](coherence.md) (via a named `grammarAlignment` term) and the
[admissibility outcome](admissibility-and-outcomes.md). This is the vocabulary the
whole sandbox and every [sweep](../modules/analysis-sweeps.md) share.
