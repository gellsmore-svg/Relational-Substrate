# Relational Substrate Research Task Map

Last updated: 2026-06-13
Current branch: `main`
Latest validation state: see latest RI chain output; this map now reflects the post-orthoclase Ca-scaffold topology-gate sequence through Ca-scaffold model-form quarantine.

## Current Status

| Measure | Value |
|---|---:|
| Overall sandbox/report completion | 99.999% |
| External benchmark completion | 100% |
| Benchmark target coverage | 30/24 |
| Benchmark passes | 29/30 (96.7%) |
| Checks passed | 187/192 (97.4%) |
| Core independent evidence lines | 7 |
| Orientation-only evidence lines | 1 |
| Grammar internal coherence | 8/10 |
| Cross-domain equivalence | 5.2/10 |
| Evidence independence | 4.5/10 |
| Unification thesis support | 4.8/10 |
| Inferential convergence | 5.6/10 |

Read confidence as inferential convergence, not proof. The current posture is deliberately held near 5.6/10 — below the 6.25 cap — because the material-property gate is unresolved, the heteroatom-torsion (disulfane / H-Se-Se-H) trans-side transfer failed under held constants, and EM depth remains mostly scalar analytic evidence inside one electromagnetic evidence line.

> Reconciled 2026-06-13: the /10 confidence metrics above were updated to match the regenerated `analysis/out/external-benchmark-summary.json` (the doc had drifted high — it previously read inferential convergence 6.25, cross-domain 5.7, unification 5.2). 6.25 was the **cap**, not the computed value; the computed inferential convergence stepped down to 5.6 after the heteroatom-torsion trans-side failures. Regenerate with `npm run reports` and audit drift with `npm run evidence:ledger`.

## Current Blocking Gate

The live blocker is still the measured material refractive-index challenge, but the active front has moved beyond the original orthoclase miss. The current RI chain has diagnosed the simple NBO/T, framework-Al, cation-response, and scalar Ca-scaffold repairs as insufficient without topology/structure gates.

Current broad benchmark command:

```bash
npm run benchmark:material-refractive-index
```

Current RI chain command:

```bash
node analysis/ri-refractive-index-chain-runner.mjs
```

Current status:

| Item | State |
|---|---|
| Benchmark status | measured material refractive-index challenge unresolved |
| Benchmark score | 7/11 for the original material-RI challenge |
| RI chain status | 33-step RI diagnostic chain completes |
| Primary proxy | `n = 1.46 + 0.02*NBO/T - 0.004*chargeBalancedAl` |
| First repair candidate | `n = 1.46 + 0.03*NBO/T + 0.075*chargeBalancedAl` |
| First repair status | failed fresh anorthite validation; not promotable |
| Second-generation candidate | `n = 1.46 + 0.03*NBO/T + 0.075*chargeBalancedAl - 0.014*divalentModifierCharge` |
| Second-generation status | failed fresh orthoclase validation; not promotable |
| Later Ca-scaffold status | melilite-local Ca scaffold repair failed transfer to hardystonite, rankinite, kilchoanite, and larnite; topology gate required |
| Current held-out state | larnite classified before scoring and then scored under frozen gates |

Measured targets:

| Formula | Material | Role | Measured RI | Primary prediction | First repair | Second-generation candidate | Reading |
|---|---|---|---:|---:|---:|---:|---|
| SiO2 | fused silica | source-anchored baseline | 1.45704 | 1.46 | 1.46 | 1.46 | baseline clears tolerance |
| Na2SiO3 | sodium silicate glass | modifier/NBO pressure | 1.52 | 1.5 | 1.52 | 1.52 | primary fails; candidates fit |
| NaAlSi3O8 | albite feldspar | held-out framework pressure | 1.53493 | 1.456 | 1.535 | 1.535 | primary collapses framework; candidates fit |
| CaAl2Si2O8 | anorthite feldspar | fresh first-repair validation | 1.58167 | 1.452 | 1.61 | 1.582 | primary fails; first repair fails; second-generation fits current rows but is not validation |
| KAlSi3O8 | orthoclase feldspar | fresh second-generation validation | 1.52183 | 1.456 | 1.535 | 1.535 | second-generation overpredicts by 0.01317; fails 0.01 tolerance |

Source anchors:

- SiO2: KLA/Filmetrics refractive-index database, citing Malitson JOSA 1965.
- Na2SiO3: PubChem sodium silicate HSDB/Merck Index property record.
- NaAlSi3O8: Mindat albite optical RI ranges.
- CaAl2Si2O8: Mindat anorthite optical RI ranges.
- KAlSi3O8: Mindat orthoclase optical RI ranges.

## Why The Current Repair Failed

The first proxy only uses NBO/T and charge-balanced Al, so it cannot distinguish zero-NBO framework materials well enough. Albite exposed the missing framework term. A target-implied positive framework-Al term then fit silica, sodium metasilicate, and albite, but failed anorthite by overpredicting RI:

| Formula | Repair prediction | Measured RI | Error | Tolerance |
|---|---:|---:|---:|---:|
| CaAl2Si2O8 | 1.61 | 1.58167 | 0.02833 | 0.01 |

This means a simple linear framework-Al boost is still structurally incomplete. The current second-generation candidate tests one such variable: modifier identity via divalent modifier charge.

## Current Second-Generation Candidate

The current second-generation candidate adds a crude divalent-modifier correction:

```text
n = 1.46 + 0.03*NBO/T + 0.075*chargeBalancedAl - 0.014*divalentModifierCharge
```

This fit the measured rows available when it was introduced, including CaAl2Si2O8, but it failed the fresh orthoclase held-out row:

| Formula | Candidate prediction | Measured RI | Error | Tolerance |
|---|---:|---:|---:|---:|
| KAlSi3O8 | 1.535 | 1.52183 | 0.01317 | 0.01 |

The failure is narrow but real under the predeclared tolerance. Treat it as a structural K/Na framework-response miss, not as a source problem.

## Current Latest RI State

The latest safe state is:

| Item | State |
|---|---|
| Gate hypothesis | melilite-like Ca scaffold requires Ca coordination 8 and mean Ca-O at least 2.53 A under the fixed extractor |
| Reserved target | larnite, Ca2SiO4, COD 9017424 |
| Pre-score classification | compact/lower-coordinate non-melilite Ca scaffold |
| Larnite descriptors | mean Ca coordination 7.5; mean Ca-O 2.506367 A; no T-O-T bridge angle under isolated SiO4 orthosilicate rule |
| Scored result | split-Ca family predicted 1.75034 versus measured midpoint 1.719666; error 0.03067; fail |
| Control result | baseline density + Al/O + Al-comp response predicted 1.71769; error 0.00198; pass |
| Contrast diagnostic | baseline family misses rankinite and kilchoanite but passes larnite; split-Ca overpredicts all three non-melilite Ca-silicate rows |
| Reserved next target | merwinite, Ca3Mg(SiO4)2, reserved as high-density Mg-bearing Ca-silicate density-control falsifier |
| Merwinite result | baseline predicted 1.69837 versus measured 1.713666; error 0.0153; fail. Split-Ca and split-Ca/Mg pass, but Mg is confounded |
| Reading | larnite baseline success is local; merwinite does not validate a new model because Mg chemistry prevents pure Ca-Si-O transfer claims |
| Boundary | do not promote split-Ca or split-Ca/Mg from merwinite; treat it as a control contrast |
| Post-merwinite reservation | spurrite, Ca5(SiO4)2(CO3), reserved as Mg-removed/carbonate-introduced control contrast; no prediction scored |
| Wollastonite screen | deferred; COD polytype-specific CIF rows exist, but no polytype-specific optical/density row is locked |
| Spurrite result | baseline predicted 1.64084; split-Ca predicted 1.68693; split-Ca/Mg predicted 1.69584 versus measured midpoint 1.663833. All fail 0.01 tolerance |
| Pure Ca-Si-O source screen | no new held-out target reserved; wollastonite/pseudowollastonite remain source-blocked and hatrurite lacks usable optical/density fields |
| Model-form boundary | baseline, split-Ca, and split-Ca/Mg families are quarantined as reference diagnostics only; do not score further targets under them as candidate repairs |

## Next Tasks

1. Treat the post-merwinite branch as model-form blocked and avoid model promotion.
   - Spurrite removes Mg but introduces carbonate; all frozen families failed, so merwinite's split-Ca pass remains Mg/topology-confounded.
   - Wollastonite remains deferred: CIF candidates exist for WO1T/triclinic and Wollastonite-2M/parawollastonite, but the available optical/density row is broad and not polytype-locked.
   - The pure Ca-Si-O screen found no new source-locked target; the quarantine diagnostic now blocks baseline, split-Ca, and split-Ca/Mg from further candidate-repair scoring.
   - The next clean RI path is a predeclared new structural model form before target scoring, or a primary-source unlock for a clean held-out target followed by pre-score gate classification.

2. Keep the topology-gated Ca-scaffold diagnosis separate from material-property validation.
   - Larnite is not a programme-level RI pass because the active post-failure repair failed.
   - The baseline pass is a control-row success only; the baseline family still misses rankinite and kilchoanite.
   - Treat density/polarizability as the conventional comparator, not as substrate-specific evidence.

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
npm run guardrails
```

After reports regenerate, inspect:

```bash
sed -n '1,170p' analysis/out/external-benchmark-summary.md
sed -n '1,180p' analysis/out/external-material-refractive-index-challenge.md
sed -n '1,120p' docs/claude-drift-completeness-review.md
```

## Process and Tooling Recommendations (adopted 2026-06-13)

A detailed review recommended the following process improvements to strengthen guardrails, predeclaration, conventional baselines, and reproducibility. These are now expected for new model-form or descriptor work. Full rationale is in `docs/process-recommendations.md`.

- **Predeclaration**: Explicitly declare the descriptor set (see `analysis/descriptor-registry.json`) and extraction rules *before* scoring any target. Treat as a hard gate.
- **Conventional baselines**: Surface a clean, non-fitted conventional predictor (density + Lorentz-Lorenz) side-by-side in every material/RI report. Report value added on held-out rows only; label conventional terms explicitly.
- **Descriptor registry**: Use the registry for new descriptors (with units, extraction, source requirements, conventional flag). Started in `analysis/descriptor-registry.json`.
- **Guardrails script**: Run `npm run guardrails` for syntax + registry checks (`node scripts/guardrails.mjs`).
- **Provenance**: Lock primary data rows (CIF + measured n + density) before prediction. Prefer a dedicated calibration data area (future).
- **Toy model characterization**: Add sensitivity analysis on `identityPreserved` thresholds and bias tables.
- **Cross-track ledger**: Improve queryable summary of evidence lines, independence, and conventional vs. grammar contribution.
- **UI/analysis roundtrip**: Add export of exact sandbox parameters as JSON for exact reproduction in analysis scripts.

See `CONTRIBUTING.md` (Expected Changes and Process Improvements section) and `.restart.md` for integration notes. Run the guardrails script as part of pre-update hygiene.

## Files To Check First Next Session

- `analysis/external-material-refractive-index-challenge.mjs`
- `analysis/material-nbo-stoichiometry.mjs`
- `analysis/ri-refractive-index-chain-runner.mjs`
- `analysis/ri-larnite-gate-classification-diagnostic.mjs`
- `analysis/external-ri-larnite-ca-scaffold-transfer-validation.mjs`
- `analysis/ri-larnite-density-control-contrast-diagnostic.mjs`
- `analysis/ri-density-control-falsifier-reservation-diagnostic.mjs`
- `analysis/external-ri-merwinite-density-control-validation.mjs`
- `analysis/ri-post-merwinite-target-reservation-diagnostic.mjs`
- `analysis/ri-wollastonite-polytype-source-lock-screen.mjs`
- `analysis/external-ri-spurrite-confound-substitution-validation.mjs`
- `analysis/ri-pure-ca-si-o-source-exhaustion-screen.mjs`
- `analysis/ri-ca-scaffold-model-form-quarantine-diagnostic.mjs`
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
