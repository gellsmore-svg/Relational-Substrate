# Relational Substrate Research Task Map

Last updated: 2026-05-08
Current branch: `main`
Latest committed validation state: `a64ba99`

## Current Status

| Measure | Value |
|---|---:|
| Overall sandbox/report completion | 99.999% |
| External benchmark completion | 100% |
| Benchmark target coverage | 30/24 |
| Benchmark passes | 29/30 (96.7%) |
| Checks passed | 186/190 (97.9%) |
| Core independent evidence lines | 7 |
| Orientation-only evidence lines | 1 |
| Grammar internal coherence | 8/10 |
| Cross-domain equivalence | 5.7/10 |
| Evidence independence | 4.5/10 |
| Unification thesis support | 5.2/10 |
| Inferential convergence | 6.25/10 |

Read confidence as inferential convergence, not proof. The current posture is deliberately held near 6/10 because the material-property gate is unresolved and EM depth remains mostly scalar analytic evidence inside one electromagnetic evidence line.

## Current Blocking Gate

The live blocker is the measured material refractive-index challenge.

Current command:

```bash
npm run benchmark:material-refractive-index
```

Current status:

| Item | State |
|---|---|
| Benchmark status | measured material refractive-index challenge unresolved |
| Benchmark score | 6/9 |
| Primary proxy | `n = 1.46 + 0.02*NBO/T - 0.004*chargeBalancedAl` |
| Repair candidate | `n = 1.46 + 0.03*NBO/T + 0.075*chargeBalancedAl` |
| Repair status | failed fresh anorthite validation; not promotable |

Measured targets:

| Formula | Material | Role | Measured RI | Primary prediction | Repair prediction | Reading |
|---|---|---|---:|---:|---:|---|
| SiO2 | fused silica | source-anchored baseline | 1.45704 | 1.46 | 1.46 | baseline clears tolerance |
| Na2SiO3 | sodium silicate glass | modifier/NBO pressure | 1.52 | 1.5 | 1.52 | primary fails; repair fits |
| NaAlSi3O8 | albite feldspar | held-out framework pressure | 1.53493 | 1.456 | 1.535 | primary collapses framework; repair fits |
| CaAl2Si2O8 | anorthite feldspar | fresh repair validation | 1.58167 | 1.452 | 1.61 | primary fails; repair also fails |

Source anchors:

- SiO2: KLA/Filmetrics refractive-index database, citing Malitson JOSA 1965.
- Na2SiO3: PubChem sodium silicate HSDB/Merck Index property record.
- NaAlSi3O8: Mindat albite optical RI ranges.
- CaAl2Si2O8: Mindat anorthite optical RI ranges.

## Why The Current Repair Failed

The first proxy only uses NBO/T and charge-balanced Al, so it cannot distinguish zero-NBO framework materials well enough. Albite exposed the missing framework term. A target-implied positive framework-Al term then fit silica, sodium metasilicate, and albite, but failed anorthite by overpredicting RI:

| Formula | Repair prediction | Measured RI | Error | Tolerance |
|---|---:|---:|---:|---:|
| CaAl2Si2O8 | 1.61 | 1.58167 | 0.02833 | 0.01 |

This means a simple linear framework-Al boost is still structurally incomplete. The next model likely needs a variable that distinguishes Na-aluminosilicate and Ca-aluminosilicate frameworks.

## Next Tasks

1. Replace the failed refractive-index repair candidate.
   - Candidate variables to test: cation field strength, density, molar refraction, cation polarizability, Ca/Na modifier identity, or a normalized framework-charge-density term.
   - Do not promote a target-fitted equation without a fresh held-out material.

2. Add one new held-out refractive-index material only after choosing the next predictor form.
   - Recommended class: another feldspar or silicate with simple stoichiometry that the NBO/T model can represent.
   - Avoid choosing the validation row after inspecting whether the revised equation passes it.

3. Keep current confidence capped.
   - Do not raise inferential convergence above 6.25/10 until a measured material-property prediction passes without endpoint fitting.
   - If a revised predictor fits current rows but fails a fresh target, keep the material benchmark unresolved.

4. Secondary validation track: held-out torsion absolute magnitudes.
   - Hydrazine cation remains a qualitative/ratiometric pass with absolute-magnitude miss.
   - Next useful task is calibrated absolute barrier transfer on a new torsion system without endpoint fitting.

5. Secondary validation track: roughness/interface beyond smooth-surface TIS.
   - Current roughness calibrated scatter is a smooth-surface TIS comparator.
   - Next useful task is measured BRDF/PSD/broadband scatter, not more scalar EM depth.

6. Lower priority EM track.
   - EM-17 completed scalar double-slit envelope coupling.
   - Do not prioritize further scalar EM comparators until material-property or held-out absolute torsion improves.

## Working Commands

Use these before committing substantive updates:

```bash
node --check analysis/material-nbo-stoichiometry.mjs
node --check analysis/external-material-refractive-index-challenge.mjs
node --check analysis/external-benchmark-summary.mjs
node --check analysis/milestone-external-review-summary.mjs
node --check analysis/claude-drift-completeness-review.mjs
npm run reports
npm run build
```

After reports regenerate, inspect:

```bash
sed -n '1,170p' analysis/out/external-benchmark-summary.md
sed -n '1,180p' analysis/out/external-material-refractive-index-challenge.md
sed -n '1,120p' docs/claude-drift-completeness-review.md
```

## Files To Check First Next Session

- `analysis/external-material-refractive-index-challenge.mjs`
- `analysis/material-nbo-stoichiometry.mjs`
- `analysis/external-benchmark-summary.mjs`
- `analysis/milestone-external-review-summary.mjs`
- `docs/claude-drift-completeness-review.md`

## Guardrails

- Treat `analysis/out/` as generated output.
- Keep source-of-truth report logic in `analysis/*.mjs`.
- Keep `docs/claude-drift-completeness-review.md` as the tracked review copy.
- Do not count EM-02 through EM-17 as independent domains; they are one electromagnetic evidence line.
- Do not count boundary phase as core evidence; it is orientation-only.
- Do not count target-implied material-property coefficients as validation until they clear a fresh held-out target.
