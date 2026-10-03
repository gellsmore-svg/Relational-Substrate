---
type: Concept
title: Guardrail — strictly abstract
description: The model's honesty constraint — it does not simulate T0 directly and does not treat rendered curves, molecules, lattices, materials, or interfaces as substrate objects. The external benchmarks calibrate the abstract grammar against classical reference order; they are diagnostics, not physical claims.
resource: https://github.com/gellsmore-svg/Relational-Substrate/blob/main/README.md
tags: [relational-substrate, guardrail, abstraction, honesty]
timestamp: 2026-06-19T00:00:00Z
---

# Guardrail — strictly abstract

The project is deliberate about what it is **not**. The model:

- does **not** simulate `T0` directly;
- does **not** treat rendered curves, molecules, lattices, materials, or interfaces
  as substrate objects — they are conceptual illustrations of the
  [grammar](substrate-grammar.md), not physics.

The [external benchmarks](../modules/benchmarks.md) (EM, molecular geometry,
lattice, glass network, transport) **calibrate** the abstract grammar against
classical reference order — checking whether the grammar *separates* reference
order from decoys — and are explicitly **topology/control diagnostics, not
simulators**. Classical geometry anchors carry provenance metadata; they calibrate
the bench, they are **not claims derived from the grammar**. Coordinate/geometry
fields are inputs from which coherence variables are *derived*, not substrate
objects themselves.

This guardrail is what keeps the model honest: a relational, abstract grammar with
diagnostics, not a physical theory dressed as software.
