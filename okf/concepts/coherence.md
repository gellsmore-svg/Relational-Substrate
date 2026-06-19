---
type: Concept
title: Coherence
description: Coherence is computed as a richer combination of the five grammar elements that rewards alignment across the grammar (a named grammarAlignment term) while penalising charge tension and scatter — the model's measure of how well an order holds together.
resource: https://github.com/gellsmore-svg/Relational-Substrate/blob/main/src/model.js
tags: [relational-substrate, coherence, grammar-alignment]
timestamp: 2026-06-19T00:00:00Z
---

# Coherence

**Coherence** is the model's measure of how well an order holds together. As of the
v0.2 grammar advance it is computed as a **richer combination of the five
[grammar elements](substrate-grammar.md)** rather than a single slider: it
**rewards alignment** across the grammar — captured in a named **`grammarAlignment`**
term — while **penalising charge tension and scatter**.

Coherence is a primary input to the [closure gate and identity
score](closure-gate-and-identity.md): an order with high grammar alignment and low
tension coheres and is more likely to be [admitted](admissibility-and-outcomes.md)
and to hold its identity. The browser [sandbox](../modules/sandbox-ui.md) exposes a
**grammar-health composite**, and the coherence [sweep](../modules/analysis-sweeps.md)
records grammar signatures and how coherence behaves across the parameter space.
The pure-logic explanation lives alongside the model.
