---
type: Concept
title: Closure gate & identity
description: A closure gate reads out closure, returnability, boundedness, coherence, reseating, and leakage, and combines them into an identity score — a measure of whether a stable, self-consistent order has formed. Small perturbations can flip the gate, which the sweeps probe for sensitivity.
resource: https://github.com/gellsmore-svg/Relational-Substrate/blob/main/src/model.js
tags: [relational-substrate, closure-gate, identity, metrics]
timestamp: 2026-06-19T00:00:00Z
---

# Closure gate & identity

Beyond the [outcome fractions](admissibility-and-outcomes.md), each interaction is
read through a **closure gate** — a set of metrics describing the *quality* of the
closure:

- **closure**, **returnability**, **boundedness**, **coherence**, **reseating**,
  **leakage**, and a composite **identity score**.

The **identity score** is the headline: does a stable, self-consistent order
actually form and hold? The gate is sensitive — small perturbations can **flip**
it — which is why the [sweeps](../modules/analysis-sweeps.md) measure identity-gate
**flip sensitivity** under small perturbations and the high/low-grammar region
**preservation rate**. Whether identity survives not just one encounter but a short
**history** of them is the [resilience](resilience-and-regimes.md) question.
[Coherence](coherence.md) is one of the gate's inputs and its richest term.
