---
type: Module
title: External benchmarks
description: Calibration comparators that check whether the abstract grammar separates classical reference order from decoys — across electromagnetism, molecular geometry, ionic lattices, glass networks, and transport. They are topology/control diagnostics, not physics simulators.
resource: https://github.com/gellsmore-svg/Relational-Substrate/tree/main/analysis
tags: [relational-substrate, benchmarks, calibration, diagnostics]
timestamp: 2026-06-19T00:00:00Z
---

# External benchmarks (`analysis/external-*.mjs`)

A battery of **calibration comparators** that test the abstract
[grammar](../concepts/substrate-grammar.md) against **classical reference order** —
checking whether the grammar *separates* reference order from decoys, never
claiming to reproduce the physics ([guardrail](../concepts/guardrail.md)):

- **Electromagnetism** — Coulomb, equipotentials, field-line topology, dielectric
  and absorbing media, boundary propagation, diffraction grating, double-slit
  envelope, and more (`external-em-*.mjs`).
- **Molecular geometry** — e.g. disulfane / heteroatom rotor comparisons against
  geometry anchors.
- **Ionic lattice** — does an alternating-charge lattice grammar separate `NaCl` /
  `LiF` order from same-charge, clustered, and pair-collapse decoys.
- **Glass network** — does a tetrahedral-network grammar separate fused-silica /
  sodium-silicate / aluminosilicate order from fragmented / modifier-clustered /
  charge-uncompensated decoys.
- **Transport** — does mixed-modifier route order separate compensated transport
  paths from dominance / clustering / depletion / field-trap decoys.

Each is explicitly a **topology/control diagnostic only** — not a simulator of EM,
chemistry, crystals, glass, or diffusion. Geometry anchors carry provenance and
**calibrate the bench**; they are not claims of the grammar. Summaries and roadmaps
(`external-benchmark-summary.mjs`, `external-benchmark-roadmap.mjs`) collate them
into the [reports](reports.md).
