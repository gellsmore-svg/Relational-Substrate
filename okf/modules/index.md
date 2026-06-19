---
type: Module Index
title: Relational Substrate Modules
description: The components — the shared pure-logic model, the browser sandbox UI, the analysis sweeps, the external calibration benchmarks, and the report generation.
resource: https://github.com/gellsmore-svg/Relational-Substrate/tree/main/src
tags: [relational-substrate, modules, components]
timestamp: 2026-06-19T00:00:00Z
---

# Modules

- **[Model](model.md)** (`src/model.js`) — the shared pure-logic core: grammar,
  outcomes, coherence, sequences, and resilience/regime analysis.
- **[Sandbox UI](sandbox-ui.md)** (`src/main.js`, `index.html`, `src/styles.css`) —
  the interactive browser sandbox.
- **[Analysis sweeps](analysis-sweeps.md)** (`analysis/*.mjs`) — batch parameter
  sweeps over the model (coherence, geometry, resilience).
- **[Benchmarks](benchmarks.md)** (`analysis/external-*.mjs`) — calibration
  comparators against classical reference order.
- **[Reports](reports.md)** (`scripts/generate-reports.mjs`, `verification/`) —
  report generation and the build/test pipeline.

The browser UI and the sweeps **share the same rule model** from `src/model.js`, so
the screen and batch search use the same thresholds.
