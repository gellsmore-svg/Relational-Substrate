---
type: Module
title: Reports & build
description: Report generation that runs the sweeps and benchmarks and writes their results, plus the build/test pipeline — npm run reports generates the reports, npm run build is the Vite build, and npm test runs reports then build.
resource: https://github.com/gellsmore-svg/Relational-Substrate/blob/main/scripts/generate-reports.mjs
tags: [relational-substrate, reports, build, vite]
timestamp: 2026-06-19T00:00:00Z
---

# Reports & build (`scripts/generate-reports.mjs`)

The pipeline that turns the [sweeps](analysis-sweeps.md) and
[benchmarks](benchmarks.md) into recorded output:

- **`npm run reports`** → `node scripts/generate-reports.mjs` — runs the analyses
  and writes their results (the durable record of how the
  [grammar](../concepts/substrate-grammar.md) behaves and how it scores against the
  calibration benches).
- **`npm run build`** → `vite build` — builds the browser [sandbox](sandbox-ui.md)
  into `dist/`.
- **`npm test`** → `npm run reports && npm run build` — the combined check (reports
  must generate and the app must build), which CI runs.

`verification/` holds UI screenshots (desktop/mobile). The `analysis/`,
`verification/`, and `dist/` outputs together with the reports are the project's
evidence that the abstract model is exercised and recorded — within the
[guardrail](../concepts/guardrail.md).
