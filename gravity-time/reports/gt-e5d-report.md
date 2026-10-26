# Is it just where the traffic sits? Durability against a local/remote traffic match (GT-E5D)

*A plain-English report for the human researcher on prompt GT-P012, 15 October 2026.*
- *One frozen round, executed once:*
  - frozen plan `c74d896`, plan_hash `6a83dbb7…1fe7`;
  - results `6749346`, payload `228b7bb9d313…`;
  - consulted hub commit `38c2501` (read only).
- *Numbers are exact finite-model computations. Tables: `round-e5d-tables.json`; per-row view: `gt-e5d-atlas.md`; construction and proofs (T16–T19): `docs/e5d-local-traffic-comparator.md`.*
- *Nothing here is a body, a place, a time or a force. The anchor is chosen by the analyst; NL is a comparison process, not a new rule.*

## Headlines

1. **Strongest positive: PATHH's triangle durability is not explained by local/remote traffic.**
   - The new stand-in NL matches how many links sit at the anchor and elsewhere, and every directed transition between those counts. Against it, PATHH's renewed triangle still survives much better.
   - Four anchor changes after renewal: C_4 is ×1.99 at N=5 (0.055 against 0.028) and ×1.44 at N=6 (0.077 against 0.053). At eight changes the factors are ×3.7 and ×2.0.
   - This holds in both entry classes, with original partners returning no more often than under NL.
2. **Strongest negative (an explanation found): PATHF's centre advantage *is* local/remote traffic.**
   - PATHF "≥2 links" at N=6 reached renewal 1.32 times as often as NK and survived the first anchor change 1.27 times as well. Against NL both disappear (×1.00 and ×1.01).
   - The small PATHF effect seen since E5A is explained by how its activity divides between the anchor and the rest of the graph.
3. **Surprise: PCOMP's within-class effect survives NL too, and PCOMP shows no circulation at all.**
   - PCOMP triangle episodes that start with two or more completers survive four changes about 2.2–2.4 times as well as NL within those classes (0.024 against 0.011 at N=5, size 2; 0.019 against 0.008 at N=6, size 3).
   - PCOMP's projected traffic is perfectly reversible, but its rates vary widely *within* each local/remote cell (CV up to 0.67). What remains is about arrangement within a cell, which no stand-in here matches.

## What NL is, and what the mathematics showed

- **Partition:** NL splits the links into those touching the anchor (local) and the rest (remote). It records how much stationary probability sits at each pair of counts (local, remote), and the stationary rate of each one-step move between pairs, *in each direction separately*.
- **Rates:** it then gives every local slot, and every remote slot, the same rate within its count cell, chosen to reproduce those directed flows exactly.
- **Proof on fixtures:**
  - NL's long-run picture is stationary even when traffic circulates around the (local, remote) grid (T16). Detailed balance is not needed.
  - It reproduces every directed flow (T17), and among stand-ins of this exchangeable kind it is the only one that does (T18).
  - It is reversible exactly when no circulation exists (T19).
  - Every identity held in every science cell, to 10⁻¹⁰ or better.
- **Circulation was real in the PATH and CSPH families.** Their projected net currents reach 40–98% of the larger directed flow, so NL is **not** reversible for them. CLOSEW and PCOMP have none (to 10⁻¹³), so NL is reversible for them. This is a property of the projection of a finite process, not an arrow of time.
- **What NL does not match:** which particular local links are present (so the triangle completers), correlations, multi-step structure, the first-renewal law, or persistence itself.

## Family by family (C_h = survival given renewal; ratios target ÷ comparator)

| Family, pattern | Against NK (E5C) | Against NL (new) | Reading |
| --- | --- | --- | --- |
| PATHH triangle | C_4 ×2.10 (N5), ×1.61 (N6) | C_4 ×1.99, ×1.44 | residual not traffic (D1 or D3) |
| PCOMP triangle, size ≥ 2 | C_4 ×2.2 (N5, s=2), ×1.5 pooled (N6) | about the same (×2.2; ×1.45) | within-cell arrangement (D3) |
| PCOMP pooled | C_4 ×1.19 (N5), ×0.99 (N6) | ×1.17, ×0.95 | near control |
| PATHF "≥2 links", N6 | R0 ×1.32, C_1 ×1.27 | R0 ×1.00, C_1 ×1.01 | **explained by traffic (D2)** |
| PATHF triangle | below (C_4 ×0.55, ×0.50) | below (×0.51, ×0.46) | negative, unchanged |
| CSPH triangle | R0 ×2.2–2.6; C_1 ×0.84–0.86; returns about 2.5× | R0 ×2.0–2.1; C_1 ×0.81–0.82; returns 2.1–2.4× | still flicker-assisted (D4); NL removes part of the renewal excess |
| CSPH "≥2 links", N6 | C_1 ×0.93, C_4 ×1.45 | C_1 ×0.91, C_4 ×1.26 | horizon-dependent sign, small values (D5) |
| PATHH "≥2 links", N6 | below NK (R0 ×0.83) | ≈ NL (×0.97–1.05) | near control |
| CLOSEW | ≈ or below | ≈ or below (×0.88–1.12 up to h = 4; larger only at h = 8, on values near 10⁻⁵) | control |
| NULL | — | NL = NK = ND = N0 exactly | fixed point |

**Horizon dependence.** Ratios at h = 8 are larger but rest on probabilities of 10⁻⁴–10⁻². CSPH "≥2 links" changes sign between h = 2 and h = 4 against both stand-ins.

## Answers

- **GT-Q25:** for PATHF, yes: traffic explains it. For PATHH and PCOMP, no: residuals remain beyond the local/remote traffic match. Both point to arrangement within a count cell (D3), or to organisation (D1). E5D cannot separate those two.
- **NL against NK:** NL removes only a small part of PATHH's excess (×2.10 → ×1.99; ×1.61 → ×1.44), but all of PATHF's.

## What this does not show

- No self-maintaining organisation: all renewal still decays within a few anchor changes (E5C).
- **A residual beyond NL means "not explained by this projection".** It is not proof of an organisational mechanism.
- The same exposed laws were used, so this is not independent confirmation.
- Nothing about identity of a moving structure, interaction, displacement, acceleration or gravity.

## Files

`plans/round-e5d-plan.json`, `reports/round-e5d-tables.json`, `reports/gt-e5d-atlas.md`, `reports/gt-e5d-reflection.md`, `docs/e5d-local-traffic-comparator.md`, `docs/gt-p012-starting-audit.md`, `docs/gt-p012-coverage-and-integrity-audit.md`, `docs/gt-e5d-cross-programme-transfer.md`, `docs/gt-p012-shared-synthesis-handoff.md`, `provenance/execution-GT-P012.md`.
