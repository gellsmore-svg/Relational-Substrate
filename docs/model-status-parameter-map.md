# RS Modelling Status And Parameter Map

Last updated: 2026-06-22

## Purpose

This note answers four practical questions:

- what is currently modelled successfully
- which parameters or descriptors those successes depend on
- what is not yet modelled successfully
- which parameters can be varied for experiments without turning exploration into validation

It is a working map, not a confidence upgrade. The external benchmark summary still holds inferential convergence at 5.6/10 while the measured material refractive-index gate and heavy-heteroatom torsion transfer remain unresolved.

## Core Toy-Model Parameters

The browser sandbox and abstract sweeps use the same pure model in `src/model.js`.

| Parameter | Meaning in the toy model | Current role |
|---|---|---|
| `boundary` | compatibility of encountered boundary/closure | raises admission and boundedness; low values favour return |
| `route` | continuity of the transient route | major positive driver of identity preservation |
| `storage` | tendency to lock/store disturbance | raises closure stress when excessive |
| `scatter` | incoherent loss/dispersal | reduces coherence and raises closure stress |
| `reseat` | ability of the closed order to settle after encounter | strongest positive input in sensitivity analysis |
| `phase` | alignment/timing state around neutral `0.5` | contributes through `phaseMatch = 1 - abs(phase - 0.5) * 1.9` |
| `charge` | asymmetry/tension | contributes through `chargeTension = abs(charge)` |

Current scenario presets:

| Scenario | boundary | route | storage | scatter | reseat | phase | charge |
|---|---:|---:|---:|---:|---:|---:|---:|
| `admit` | 0.82 | 0.78 | 0.18 | 0.12 | 0.70 | 0.50 | 0.00 |
| `return` | 0.22 | 0.32 | 0.24 | 0.18 | 0.74 | 0.30 | 0.20 |
| `store` | 0.48 | 0.42 | 0.70 | 0.50 | 0.46 | 0.70 | -0.15 |

Current identity gate:

| Gate | Value | Reading |
|---|---:|---|
| `identityScore >=` | 0.62 | active binding constraint |
| `closureStress <` | 0.62 | near-inert in the current sensitivity sweep |

Sensitivity result: raising the identity cutoff by `+0.01` changes coherent rate by about `-0.0308`; raising the closure-stress cutoff by `+0.01` changes coherent rate by only about `+0.0002`. If experimenting with the toy model, identity weighting and reseat/route/scatter matter much more than the closure-stress cutoff.

## Successfully Modelled Or Passed Comparators

These are successful within their declared scope, not proofs of the ontology.

| Area | Status | Parameters/descriptors that matter | Boundary of the success |
|---|---|---|---|
| H2O2 torsion | passes qualitative, equilibrium-angle, and ethane-scale absolute-barrier checks | torsion penalty profile, anti-planar release revision, ethane-derived scale; no H2O2 endpoint fitting in the absolute transfer check | not a full quantum torsional energy surface |
| Ethane torsion | passes qualitative and broad quantitative tolerance | normalized threefold torsion reference; experimental barrier `2.875 kcal/mol`; model penalty scaled to that endpoint | endpoint scaling is a caveat; intermediate points remain high |
| Hydrazine cation torsion | qualitative/ratiometric held-out pass with magnitude miss | held ethane/H2O2 torsion architecture and scale transfer | absolute barrier magnitudes are low |
| Ionic lattice ordering | qualitative pass | alternating charge, closure, continuity; separates unlike-neighbour order from same-charge/collapse decoys | not a lattice-energy or full crystal-physics model |
| Silicate network order | qualitative held-out pass | graph continuity, charge compensation, non-bridging oxygen / tetrahedral network logic | not a glass-structure or measured-property simulator |
| Material NBO/T accounting | quantitative pass | exact composition accounting for NBO/T and charge balance | composition accounting only; does not predict RI by itself |
| Mixed-modifier route order | diagnostic pass | distributed modifier paths, route continuity, charge compensation, field-trap avoidance | not diffusion, durability, or conductivity simulation |
| Boundary / phase continuity | qualitative pass | route, phase memory, continuity, ordered splitting versus phase-broken decoys | orientation/route-memory evidence only |
| Roughness/interface ordering | qualitative and calibrated smooth-TIS passes | roughness, wavelength, incidence-angle, specular fraction, Bennett-Porteus total integrated scatter | imports smooth-surface TIS; not BRDF/PSD/deep roughness |
| EM comparators EM-02 through EM-17 | 131/131 checks pass | charge/source geometry, vector superposition, field-line topology, imported constants, Fresnel/thin-film/absorbing/scalar diffraction equations | one electromagnetic evidence line; many are analytic comparators, not Maxwell solvers |
| T1 sweep/refinement | internally coherent search | 10 scalar T1 parameters, 14,417,920 broad candidates tried, 6,348,375 accepted; 33,125 local refinement candidates accepted | fit to current T2-derived envelopes, not direct evidence of T1 primitives |

## Not Yet Modelled Successfully

| Area | Current failure/block | Parameters involved | What must change before validation |
|---|---|---|---|
| Measured material refractive index | unresolved: original material-RI challenge remains `7/11` | baseline equation `n = 1.46 + 0.02*NBO/T - 0.004*chargeBalancedAl` fails framework RI separation | source-lock a held-out target and use the predeclared structural descriptor set before scoring |
| RI first repair | failed fresh anorthite | `n = 1.46 + 0.03*NBO/T + 0.075*chargeBalancedAl`; anorthite error `0.02833` | do not promote; target-implied framework-Al boost is calibration debt |
| RI second-generation repair | failed fresh orthoclase | `n = 1.46 + 0.03*NBO/T + 0.075*chargeBalancedAl - 0.014*divalentModifierCharge`; orthoclase error `0.01317` | do not promote; K/Na framework-response variable is missing |
| Ca-scaffold RI families | quarantined | baseline density + Al/O + Al-comp; split-Ca; split-Ca/Mg | no further target scoring under these families as candidate repairs |
| Clean Ca-Si-O RI continuation | source-blocked | wollastonite/pseudowollastonite/hatrurite need optical constants, density, and CIF tied to one identity | find a primary polytype-specific optical/density row plus paired CIF |
| Heavy H2X2 torsion transfer | disulfane and H-Se-Se-H fail trans-side topology/magnitude | current anti-planar release predicts a spurious shallow 180-degree local minimum | reserve a fresh post-redesign target before using `trans_planar_topology_penalty` as evidence |
| Proposed heavy-heteroatom trans repair | diagnostic only, repairs exposed rows | `additionalCm1 = 1450 * transWindow(torsionMean)^2 * antiPlanarRelease * heavyAtomFactor(centralElement)` | must pass a fresh held-out target unchanged |
| Peroxide frontier | weakest internal challenger remains nonlocal torsion | nonlocal torsion penalty `0.0753`; near-reference penalty `0.0255` | useful for refinement, but do not tune solely to exposed peroxide rows |
| Rough optical/interface depth | not yet BRDF/PSD/broadband | current calibrated comparator is smooth-surface TIS | move to measured scatter curves or PSD-backed BRDF data |
| EM depth | scalar analytic depth, not dynamics | imported `c`, permittivity, permeability, Fresnel indices, grating equations | do not add more confidence from similar scalar EM comparators alone |

## Current RI Predeclaration Boundary

The next allowed RI model-form artifact is now predeclared, but no target has been scored under it.

| Descriptor | Status | Use |
|---|---|---|
| `ca_coordination` | substrate-facing | classify Ca scaffold environment from paired CIF |
| `mean_ca_o_distance` | substrate-facing | freeze Ca-O polyhedral distance extraction before scoring |
| `t_site_polarizability` | substrate-facing | replace ad hoc Al/O boosts with a versioned T-site response descriptor |
| `silicate_connectivity` | substrate-facing | classify orthosilicate/sorosilicate/chain/framework/ring topology |
| `density` | conventional control | comparator only; not substrate evidence |
| `lorentz_lorenz` | conventional control | comparator only; substrate terms must add held-out value beyond it |

Do not use this predeclaration to score a target by itself. A specific material/polytype still needs its own source lock, frozen extraction rules, equation, coefficients, and pass/fail tolerance before scoring.

## Parameters Worth Varying For Exploration

These are useful sandbox experiments. They should be labelled exploratory unless predeclared against a fresh held-out target.

| Experiment | Parameters to vary | What to watch |
|---|---|---|
| Toy-model coherence robustness | `reseat`, `route`, `scatter`, `boundary`; identity cutoff around `0.58..0.66` | coherent-rate cliff near identity threshold; reseat is strongest driver |
| Phase/charge sensitivity | `phase` around `0.5`; `charge` magnitude | loss of `phaseMatch`; rise in `chargeTension`; whether identity fails through coherence or stress |
| Scenario behaviour | switch `admit`, `return`, `store`; alter preset values in small increments | whether fate fractions change without breaking identity gate discipline |
| Durability/history | regime `nominal/stressed/recovering`, `regimeMemory`, `regimeSwitchingCost`, adaptive policy | whether memory/path-quality rescues marginal histories too easily |
| Peroxide torsion refinement | nonlocal torsion shoulder, anti-planar release shape, polarity/H-H separation weighting | avoid making peroxide the new hidden endpoint fit |
| Heavy H2X2 repair | `trans_planar_topology_penalty` coefficient, trans window start/end, heavy-atom factor | only counts after fresh target reservation; exposed-row repair has no evidence weight |
| RI structural model | Ca coordination cutoff, mean Ca-O extractor, T-site radii/polarizability table, connectivity encoding | freeze all choices before target scoring; always include density/Lorentz-Lorenz side-by-side |
| Roughness/interface | roughness amplitude, wavelength, incidence angle, PSD/BRDF if sourced | move beyond smooth TIS; avoid reusing analytic scalar formulas as new independent evidence |

## Parameters That Should Not Be Tuned For Evidence

| Parameter/action | Why blocked |
|---|---|
| Changing RI coefficients after seeing a target row | creates target-implied calibration debt |
| Reusing rankinite, kilchoanite, larnite, merwinite, or spurrite as fresh RI validation | all are already exposed in the RI chain |
| Promoting split-Ca or split-Ca/Mg after merwinite | merwinite is Mg-confounded and spurrite later failed |
| Counting density/Lorentz-Lorenz as substrate support | they are conventional comparators |
| Tuning `trans_planar_topology_penalty` to disulfane/H-Se-Se-H and calling it validation | both are exposed failure rows |
| Adding more scalar EM comparators and treating them as new independent domains | EM-02 through EM-17 are one evidence line |

## Practical Next Moves

1. For RI: source-lock one clean material/polytype with measured optical constants, measured density, and paired CIF, then emit a target-specific predeclaration before scoring.
2. For torsion: reserve a fresh heavy-atom rotor target before applying the trans-planar topology repair unchanged.
3. For roughness/interface: find measured BRDF/PSD/broadband scatter data and make that the next calibrated surface-response target.
4. For the toy model: run parameter sweeps around `reseat`, `route`, `scatter`, and identity cutoff; these are the most informative knobs for internal robustness.

## Executable Experiment Report

Run:

```bash
npm run model:parameter-experiments
```

This writes:

```text
analysis/out/model-parameter-experiments.md
analysis/out/model-parameter-experiments.json
```

Current one-at-a-time result around the scenario presets:

| Move | Mean effective identity delta | Reading |
|---|---:|---|
| `reseat +0.10` | `+0.0448` | strongest practical preservation lift |
| `route +0.10` | `+0.0231` | second strongest lift; tests continuity sensitivity |
| `scatter -0.10` | `+0.0157` | useful cleanup knob; lowers stress |
| `phase toward 0.5` | `+0.0105` | alignment repair, especially near marginal cases |
| `reseat -0.10` | `-0.0375` | strongest failure probe |
| `route -0.10` | `-0.0231` | clean route-continuity failure probe |
| `phase away from 0.5` | `-0.0134` | phase-mismatch probe |

Use these moves for sandbox exploration only. They are not valid retuning moves for material RI or torsion validation after a target has been observed.

For custom recipe experiments, edit or copy:

```text
analysis/parameter-recipe.example.json
```

Then run:

```bash
npm run model:recipe -- analysis/parameter-recipe.example.json
```

This writes a named `parameter-recipe-*.md/json` report under `analysis/out/`.
It also writes `parameter-recipe-*.lock.json` with a deterministic recipe hash. Use that hash if a recipe must be frozen before looking up a fresh target.

Current combined-recipe result:

| Recipe | Combined moves | Mean effective identity delta | Mean stress delta | Reading |
|---|---|---:|---:|---|
| preservation lift | `reseat +0.10`; `route +0.10`; `scatter -0.10`; `phase toward 0.5`; `|charge| lower 0.10` | `+0.0857` | `-0.0757` | strongest practical way to explore a more coherent region |
| stress/failure probe | `reseat -0.10`; `route -0.10`; `scatter +0.10`; `phase away from 0.5`; `|charge| higher 0.10` | `-0.0791` | `+0.0828` | strongest practical way to expose marginal preservation |
| storage lock-up probe | `storage +0.10`; `scatter +0.10`; `reseat -0.10` | `-0.0508` | `+0.0703` | tests whether retention is actually stress accumulation |
| route boost probe | `route +0.10` | `+0.0231` | `-0.0103` | isolates positive route-continuity sensitivity |
| route suppression probe | `route -0.10` | `-0.0231` | `+0.0100` | isolates negative route-continuity sensitivity |
