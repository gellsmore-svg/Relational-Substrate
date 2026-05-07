# Relational Substrate

Relational Substrate is a visual and analytical sandbox for the AMS topology grammar: route, closure, phase, charge, and continuity.

It does not simulate `T0` directly and does not treat rendered curves, molecules, lattices, materials, or interfaces as substrate objects. It is a browser-based conceptual model for:

```text
open transient order
meeting
closed stable order
under admissibility conditions
```

## Run

```bash
npm install
npm run dev
```

## Current Scope

Version `0.1` includes:

- light, e-ink-friendly theme
- selectable closed forms
- selectable open transient forms
- A/B/C scenario presets
- sliders for boundary compatibility, route continuity, storage, scattering, and reseating
- outcome fractions: admitted, returned, stored, scattered
- closure stress readout
- closure gate metrics: closure, returnability, boundedness, coherence, reseating, leakage, identity score
- identity preserved / at risk readout
- route-split visualisation for admitted, returned, stored, and scattered portions

## Coherence Sweep

Run the rule-model sweep with:

```bash
npm run sweep
```

Outputs are written under:

```text
analysis/out/
```

The sweep iterates closed forms, transient forms, A/B/C scenarios, and sampled slider settings. It is useful for finding coherent, fragile, and high-stress pattern regions inside the current toy rule model. It is not physical validation.

The browser UI and the sweep share the same rule model from `src/model.js`, so the screen and batch search now use the same closure, route, storage, scattering, reseating, and identity thresholds.

## Molecule Bench

Run the first secondary-regime molecule bench with:

```bash
npm run molecules
```

Outputs are written under:

```text
analysis/out/
```

This bench uses known simple molecular geometries as calibration data. It checks whether a transparent topology-and-constraint score ranks reference candidates above strained or incoherent variants. It does not treat atoms as vorton species.

Run the generated molecule perturbation sweep with:

```bash
npm run molecule:sweep
```

The perturbation sweep reports total iterations tried and change counts by category and severity. This gives a scale marker for how much of the candidate space has actually been tested.

Run the geometry-derived molecule sweep with:

```bash
npm run molecule:geometry
```

This sweep perturbs explicit geometry fields such as bond length, bond angle, torsion, ring closure distance, polarity vector, steric clearance, and valence mismatch. Coherence variables are then derived from those geometry fields.

Run the coordinate-derived molecule sweep with:

```bash
npm run molecule:coordinates
```

This sweep perturbs atom coordinate sets first, derives coordinate-feature distributions, and then derives coherence variables from those distributions. Current coordinate cases are `H2`, `HCl`, `F2`, `H2O`, `H2S`, `SO2`, `CO2`, `HCN`, `OCS`, `CH4`, `SiH4`, `CF4`, `BF3`, `BCl3`, `H2CO`, `H2CS`, `NH3`, `PH3`, `O2`, `N2`, `CO`, `C2H2`, `C2H4`, `C2H6`, `H2O2`, `NO2`, `NaCl`, `LiF`, `benzene`, and `pyridine`.

Coordinate scoring uses the same coherence variables across all cases, with family-aware weights for diatomic covalent, bent polar, trigonal pyramidal covalent, linear triatomic, linear unsaturated covalent, trigonal planar covalent, asymmetric planar covalent, tetrahedral covalent, rotatable covalent, aromatic ring, and ionic-pair cases.

Coordinate references include provenance metadata for the classical geometry anchors. These anchors calibrate the bench; they are not AMS-derived claims.

The coordinate sweep also writes decoy-control results for deliberately wrong or strained geometries such as linear water, bent carbon dioxide, planar ammonia, pyramidal boron trifluoride, eclipsed ethane, and warped benzene. These controls are not calibration anchors; they test whether the current score rejects familiar failure modes.

Run the calibration interpretation report with:

```bash
npm run molecule:calibration
```

This reads the coordinate sweep output and classifies envelope width, failure rate, and dominant constraint character by molecule. It also writes a per-family validation rollup showing whether family weights still rank reference coordinates first without per-molecule tuning.

Run the focused ethane torsion diagnostic with:

```bash
npm run molecule:ethane-torsion
```

This isolates the weak `eclipsed C2H6` decoy by scoring staggered-like, intermediate, and eclipsed-like ethane torsion angles without changing molecule-family weights.

Run the focused peroxide torsion diagnostic with:

```bash
npm run molecule:peroxide-torsion
```

This checks whether the same rotatable-group steric feature behaves sensibly for peroxide, where torsion also shifts polarity and H-H separation.

Run the focused peroxide nonlocal refinement with:

```bash
npm run molecule:peroxide-refine
```

This uses a denser torsion grid to separate near-reference tolerance, transition shoulder, and true nonlocal peroxide torsions. It is still a diagnostic report, not a calibration anchor.

Run the focused ionic lattice diagnostic with:

```bash
npm run molecule:ionic-lattice
```

This checks whether a tiny alternating-charge lattice grammar separates `NaCl` and `LiF` reference order from same-charge layers, clustered charges, and pair-collapse decoys. It is a topology/control diagnostic only; it does not add bulk crystal physics to the molecule calibration.

Run the focused silicate network diagnostic with:

```bash
npm run material:silicate-network
```

This checks whether a graph-level tetrahedral network grammar separates fused-silica, sodium-silicate, and aluminosilicate reference order from fragmented, modifier-clustered, and charge-uncompensated decoys. It is not a glass, crystal, or melt simulator.

Run the focused mixed-modifier diagnostic with:

```bash
npm run material:mixed-modifier
```

This checks whether route-level mixed modifier order separates distributed compensated transport paths from single-modifier dominance, clustered modifier islands, depleted corridors, and overcompensated field traps. It is not a diffusion, conductivity, or durability simulator.

Run the material NBO/T stoichiometry diagnostic with:

```bash
npm run material:nbo-stoichiometry
```

This checks exact non-bridging-oxygen-per-tetrahedron accounting for simple silicate and aluminosilicate compositions. It is a quantitative composition diagnostic, not a material-property simulator.

Run the focused boundary transition diagnostic with:

```bash
npm run interface:boundary-transition
```

This checks whether route-level boundary order separates ordered entry/release transitions from diffuse scattering, trapped release loops, wrong-way return dominance, and phase-broken transmission. It is not an optics, roughness, or crystallography simulator.

Run the focused phase-continuity diagnostic with:

```bash
npm run interface:phase-continuity
```

This isolates the tight `phase-broken transmission` decoy by testing whether route continuity carries phase memory, not merely apparent transmitted amplitude. It is not a wave-optics simulator.

Run the held-out roughness scatter diagnostic with:

```bash
npm run interface:roughness-scatter
```

This checks whether interface route order changes with roughness regime: smooth boundaries should preserve coherent specular order, high roughness should favour diffuse scatter, and false-specular rows with broken phase memory should not win. It is not an optics solver.

Run the T1 coupling descriptor report with:

```bash
npm run t1:coupling
```

This reads the coordinate and calibration outputs, then writes candidate T1 coupling-pattern descriptors for each T2 molecule family. These descriptors are mechanism-facing hypotheses only: they do not prove AMS and do not introduce cells, particles, lattices, or material components between `T0` substrate and T1 vortons.

Run the T1 coupling parameter sweep with:

```bash
npm run t1:sweep
```

This turns the qualitative T1 coupling descriptors into bounded numeric candidates, derives target envelopes from the current T2 family calibration, rejects incoherent candidates by guardrail rules, and ranks admissible candidates. Descriptor priors are still used for broad family features that the T2 metrics do not directly contain.

Run the T1 target stability report with:

```bash
npm run t1:stability
```

This reads the latest T1 sweep output and reports residuals between each T2-derived target envelope and the best admissible T1 candidate. Use it to see whether mismatch is likely coming from the target formula, the parameter grid, or the guardrails.

Run the T1 local refinement sweep with:

```bash
npm run t1:refine
```

This searches a narrower local parameter grid around each current best T1 candidate and reports whether residuals improve. Use it to distinguish coarse-grid error from a genuine weakness in the target formula or guardrails.

Run the assumptions report with:

```bash
npm run model:assumptions
```

This writes the current modelling assumptions, risks, and limitations across ontology boundaries, reference data, T2 scoring, T1 descriptors, numeric parameters, and sweep mechanics.

Run the frontier report with:

```bash
npm run model:frontier
```

This ranks the weakest current decoy separations and T1 residuals across the molecule, material, interface, and focused diagnostic reports. Use it to choose the next modelling target without tuning blindly.

Run the external benchmark roadmap with:

```bash
npm run model:external-roadmap
```

This records the current completion/confidence status and converts the frontier into external benchmark targets with pass/fail criteria. Use it before raising confidence in the substrate theory itself.

Run the first external peroxide benchmark with:

```bash
npm run benchmark:h2o2
```

This compares the peroxide torsion diagnostic against source-backed qualitative facts about the H2O2 equilibrium angle and cis/trans torsional barrier ordering. It is an external anchor, not a fitted quantum chemistry model.

Run the external peroxide quantitative benchmark with:

```bash
npm run benchmark:h2o2-quant
```

This checks the H2O2 equilibrium torsion angle as a non-scaled numeric target and reports cis/trans barrier-ratio compression as a quantitative caveat.

Run the external ethane benchmark with:

```bash
npm run benchmark:ethane
```

This compares the ethane torsion diagnostic against source-backed qualitative facts about staggered/eclipsed ordering, threefold periodicity, and the roughly 2.9 kcal/mol torsional barrier. It is an ordering benchmark, not an energy fit.

Run the external ethane quantitative tolerance benchmark with:

```bash
npm run benchmark:ethane-quant
```

This maps the model's eclipsed penalty onto the external ethane barrier, then tests the normalized torsion shape against a predeclared broad tolerance around a simple threefold reference curve. It is a quantitative tolerance check, not a fitted energy model.

Run the external ionic lattice benchmark with:

```bash
npm run benchmark:ionic
```

This compares the ionic lattice diagnostic against source-backed qualitative facts about rock-salt unlike-neighbour ordering for `NaCl` and `LiF`. It is an ordering benchmark, not a lattice-energy or crystal-physics model.

Run the external boundary blind-style benchmark with:

```bash
npm run benchmark:boundary-blind
```

This records a pre-comparison boundary/phase ordering prediction, then compares it against source-backed qualitative optics expectations about boundary continuity and rough-surface scattering. It is not a full historical blind test.

Run the external electromagnetic ordering benchmark with:

```bash
npm run benchmark:em-ordering
```

This tests qualitative charge-polarity, magnetic closure, and EM-wave propagation ordering outside the molecular/material benchmarks. It is not a Maxwell solver, Coulomb-force calculation, or derivation of `c`.

Run the external EM-02 Coulomb comparator with:

```bash
npm run benchmark:em-coulomb
```

This compares charge-sign direction and relative inverse-square/product-of-charge ordering against Coulomb-law expectations. It is an equation-level relative comparator, not an absolute electrostatics solver.

Run the external silicate held-out benchmark with:

```bash
npm run benchmark:silicate-heldout
```

This evaluates a held-out material-family prediction against source-backed qualitative facts about silicate network continuity, non-bridging oxygen/modifier structure, and aluminium charge compensation. It is a graph-level ordering benchmark, not a glass-property simulator.

Run the external roughness held-out benchmark with:

```bash
npm run benchmark:roughness-heldout
```

This evaluates a held-out interface prediction against source-backed qualitative facts about roughness-controlled specular and diffuse scattering. It is an ordering benchmark, not a calibrated scatter model.

Run the external material NBO/T quantitative benchmark with:

```bash
npm run benchmark:material-nbo
```

This compares exact NBO/T charge-balance accounting against source-backed material-structure expectations for simple silicate and aluminosilicate compositions. It is quantitative composition accounting, not measured property prediction.

Run the external benchmark summary with:

```bash
npm run benchmark:summary
```

This rolls up external benchmark coverage and updates the confidence posture after generated benchmark reports exist. It keeps inferential convergence separate from internal model coherence.

Run the external review milestone summary with:

```bash
npm run milestone:external-review
```

This generates a detailed milestone report for outside review, including the sandbox intent, ontology boundaries, evidence, confidence posture, non-claims, remaining gates, source anchors, and reviewer questions. It should be regenerated before any next-stage modelling work.

For a fresh clone, regenerate the full report chain with:

```bash
npm run reports
```

This rebuilds the ignored `analysis/out/` artifacts in dependency order, ending with the benchmark summary, milestone summary, and AI review prompt.

## Guardrail

The geometry is a visual grammar only.

No mesh, curve, tube, point, or rendered object should be read as a literal substrate cell.
