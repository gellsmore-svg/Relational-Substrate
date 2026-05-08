import { readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

async function readJson(name) {
  return JSON.parse(await readFile(new URL(name, outDir), 'utf8'));
}

function round(value, places = 2) {
  return Number(value.toFixed(places));
}

const assumptions = await readJson('model-assumptions.json');
const frontier = await readJson('model-frontier-report.json');

const currentStatus = {
  sandboxCompletionPct: 72,
  internalCoherenceConfidenceOutOf10: 7,
  inferentialConvergenceConfidenceOutOf10: 2.5,
  reason:
    'The sandbox now has broad internal coherence checks, but inferential convergence remains low because external prediction and comparison are not yet implemented.',
};

const benchmarkTargets = [
  {
    area: 'Peroxide torsion profile',
    currentFrontier: 'weakest true internal challenger',
    externalAnchor: 'Compare the model torsion ordering against an external H2O2 torsional energy or conformer preference profile.',
    passSignal: 'Reference/skew basin remains preferred and nonlocal torsions have a monotonic or physically interpretable penalty trend.',
    failSignal: 'Model ranks a known high-energy torsion region as too coherent, or misses the observed skew preference.',
    confidenceImpact: '+0.6 if passed, -0.8 if failed',
    priority: 1,
  },
  {
    area: 'Ethane torsion barrier',
    currentFrontier: 'rotatable-route crowding watch item',
    externalAnchor: 'Compare staggered/intermediate/eclipsed score ordering against the known ethane torsion barrier ordering.',
    passSignal: 'Staggered is best, eclipsed is worst, and intermediate angles form a smooth bridge.',
    failSignal: 'Eclipsed-like conformers remain too close to staggered or the curve shape is nonmonotonic for no model reason.',
    confidenceImpact: '+0.4 if passed, -0.5 if failed',
    priority: 2,
  },
  {
    area: 'Boundary phase transition',
    currentFrontier: 'phase-broken transmission watch item',
    externalAnchor: 'Compare route-split/phase-order predictions against simple optical boundary cases before using richer interface claims.',
    passSignal: 'Phase-preserving transmission, diffuse scattering, and trapped/released routes separate in the expected ordering.',
    failSignal: 'The model cannot distinguish apparent transmission from phase-preserving transmission.',
    confidenceImpact: '+0.5 if passed, -0.7 if failed',
    priority: 3,
  },
  {
    area: 'Ionic lattice order',
    currentFrontier: 'clear internal separation',
    externalAnchor: 'Compare alternating unlike-neighbour preference against simple ionic lattice coordination examples.',
    passSignal: 'Alternating unlike-neighbour order stays favoured over like-charge clusters without special fitting.',
    failSignal: 'The grammar cannot generalise from NaCl/LiF proxies to other simple ionic lattices.',
    confidenceImpact: '+0.3 if passed, -0.4 if failed',
    priority: 4,
  },
  {
    area: 'Silicate and modifier networks',
    currentFrontier: 'clear internal separation but physically shallow',
    externalAnchor: 'Compare network-connectivity and modifier-distribution predictions against known qualitative trends in silicate/aluminosilicate glasses.',
    passSignal: 'Network continuity, charge compensation, and modifier clustering map to known qualitative durability/mobility trends.',
    failSignal: 'The model predicts the wrong direction for modifier clustering, charge compensation, or network fragmentation.',
    confidenceImpact: '+0.5 if passed, -0.8 if failed',
    priority: 5,
  },
  {
    area: 'Electromagnetic ordering',
    currentFrontier: 'post-closure domain broadening',
    externalAnchor:
      'Compare fixed grammar ordering against conventional qualitative facts about charge polarity, magnetic field closure, and free-space EM-wave propagation.',
    passSignal:
      'Charge complementarity, closed magnetic continuity, and phase-coupled propagation outrank deliberately wrong decoys without endpoint anchoring.',
    failSignal:
      'The grammar cannot distinguish charge polarity, magnetic closure, or phase-coupled propagation from simple decoys.',
    confidenceImpact: '+0.2 if passed, -0.5 if failed',
    priority: 6,
  },
  {
    area: 'Electromagnetic equation comparator',
    currentFrontier: 'post-closure EM-02 pressure test',
    externalAnchor:
      'Compare grammar direction and relative magnitude ordering against Coulomb-law sign, product-of-charge, and inverse-square distance expectations.',
    passSignal:
      'Direction, inverse-square distance ratio, charge-product ratio, and equal-magnitude/opposite-direction symmetry pass without fitting a force constant.',
    failSignal:
      'The grammar cannot reproduce charge-sign direction or simple Coulomb relative scaling.',
    confidenceImpact: '+0.3 if passed, -0.7 if failed',
    priority: 7,
  },
  {
    area: 'Electromagnetic superposition geometry',
    currentFrontier: 'post-closure EM-03 pressure test',
    externalAnchor:
      'Compare grammar vector addition and symmetry cancellation against electric-field superposition expectations for fixed two-charge layouts.',
    passSignal:
      'Like-charge midline components cancel/add correctly, dipole components reverse with charge order, and the check remains bounded to static field geometry.',
    failSignal:
      'The grammar cannot reproduce simple multi-source vector cancellation or dipole direction reversal.',
    confidenceImpact: '+0.2 if passed, -0.6 if failed',
    priority: 8,
  },
  {
    area: 'Electromagnetic asymmetric multi-source geometry',
    currentFrontier: 'post-closure EM-04 pressure test',
    externalAnchor:
      'Compare grammar vector addition against predeclared non-symmetric three-source electric-field targets.',
    passSignal:
      'Net vector components, magnitude, angle, third-source contribution, and uniform charge-scale linearity pass for asymmetric layouts.',
    failSignal:
      'The grammar only survives symmetric two-source cases and fails asymmetric multi-source field geometry.',
    confidenceImpact: '+0.2 if passed, -0.6 if failed',
    priority: 9,
  },
  {
    area: 'Electromagnetic continuous field-line topology',
    currentFrontier: 'post-closure EM-05 topology pressure test',
    externalAnchor:
      'Compare one grammar integration rule against electric source-line divergence and magnetic closed-loop field-line topology.',
    passSignal:
      'Electric field-line routes diverge and remain open, magnetic routes close into loops, and both use the same route/phase/continuity integrator without domain-specific tuning.',
    failSignal:
      'Electric routes close like magnetic loops, magnetic routes fail to close, or the two cases require separate integration grammars.',
    confidenceImpact: '+0.5 if passed, -0.8 if failed',
    priority: 10,
  },
  {
    area: 'H2O2 absolute torsional barrier transfer',
    currentFrontier: 'post-EM-05 falsification pressure test',
    externalAnchor:
      'Apply an energy scale derived from ethane to H2O2 trans and cis torsional barriers without fitting either H2O2 endpoint.',
    passSignal:
      'Both transferred H2O2 barriers and the cis/trans ratio land within predeclared tolerance under the same scale.',
    failSignal:
      'One barrier or the cis/trans ratio fails materially, showing that the peroxide limitation is not only a unit-conversion issue.',
    confidenceImpact: '+0.3 if passed, -0.2 if mixed, -0.6 if failed',
    priority: 11,
  },
  {
    area: 'Electromagnetic equipotential geometry',
    currentFrontier: 'post-hydrazine EM-06 electrostatic pressure test',
    externalAnchor:
      'Compare scalar potential superposition, dipole zero-potential symmetry, equipotential perpendicularity, and field-as-negative-gradient behavior against conventional electrostatics.',
    passSignal:
      'The same charge/route/closure/phase/continuity grammar links scalar potential, vector field, and equipotential geometry without a new scale parameter.',
    failSignal:
      'The grammar can trace field lines or vector fixtures but cannot reproduce scalar potential/equipotential geometry from the same charge layout.',
    confidenceImpact: '+0.1 if passed, -0.5 if failed',
    priority: 12,
  },
  {
    area: 'Electromagnetic calibrated field magnitude',
    currentFrontier: 'post-EM-06 calibrated electrostatic pressure test',
    externalAnchor:
      'Compare absolute SI electric-field magnitudes and vector components against point-charge E = kq/r^2 examples using the published Coulomb constant.',
    passSignal:
      'Published worked example, microcoulomb magnitude, inverse-square scaling, charge linearity, and vector components pass without fitting a new field scale.',
    failSignal:
      'The grammar survives relative electrostatic geometry but cannot reproduce calibrated point-charge field magnitudes under the same charge/continuity rules.',
    confidenceImpact: '+0.1 if passed, -0.5 if failed',
    priority: 13,
  },
  {
    area: 'Electromagnetic conductor/dielectric media',
    currentFrontier: 'post-EM-07 material-media electrostatic pressure test',
    externalAnchor:
      'Compare ideal parallel-plate capacitance, dielectric field reduction, conductor interior screening, and dielectric energy-density consistency against standard electrostatics.',
    passSignal:
      'The same route/closure/phase/charge/continuity grammar handles dielectric dilution and conductor screening without adding a new electromagnetic vocabulary.',
    failSignal:
      'The grammar survives point-charge electrostatics but cannot reproduce simple conductor or dielectric media constraints.',
    confidenceImpact: '+0.1 if passed, -0.5 if failed',
    priority: 14,
  },
  {
    area: 'Electromagnetic plane-wave propagation',
    currentFrontier: 'post-EM-08 time-dependent propagation pressure test',
    externalAnchor:
      'Compare vacuum plane-wave speed relation, E/B relation, transverse field geometry, Poynting direction, impedance, and phase propagation against standard electromagnetic-wave relations.',
    passSignal:
      'The same route/closure/phase/charge/continuity grammar handles coupled time-dependent propagation without adding a new electromagnetic vocabulary.',
    failSignal:
      'The grammar survives static field and ideal media checks but cannot reproduce basic vacuum propagation constraints.',
    confidenceImpact: '+0.1 if passed, -0.6 if failed',
    priority: 15,
  },
  {
    area: 'Electromagnetic boundary propagation',
    currentFrontier: 'post-EM-09 normal-incidence boundary pressure test',
    externalAnchor:
      'Compare normal-incidence reflection/transmission, impedance contrast, phase inversion, speed change, and lossless energy balance against standard dielectric-boundary optics.',
    passSignal:
      'The same route/closure/phase/charge/continuity grammar handles boundary splitting and conditional phase inversion without adding a new electromagnetic vocabulary.',
    failSignal:
      'The grammar survives free-space propagation but cannot reproduce basic boundary reflection/transmission constraints.',
    confidenceImpact: '+0.1 if passed, -0.6 if failed',
    priority: 16,
  },
  {
    area: 'Electromagnetic oblique Fresnel behavior',
    currentFrontier: 'post-EM-10 oblique boundary pressure test',
    externalAnchor:
      'Compare s/p reflectance split, Brewster-angle p-reflectance zero, grazing trend, critical angle, and total internal reflection against ideal Fresnel optics.',
    passSignal:
      'The same route/closure/phase/charge/continuity grammar handles polarization-sensitive oblique boundary constraints without adding a new electromagnetic vocabulary.',
    failSignal:
      'The grammar survives normal incidence but cannot reproduce oblique Fresnel polarization and total-internal-reflection constraints.',
    confidenceImpact: '+0.1 if passed, -0.6 if failed',
    priority: 17,
  },
  {
    area: 'Electromagnetic multilayer interference',
    currentFrontier: 'post-EM-11 thin-film interference pressure test',
    externalAnchor:
      'Compare quarter-wave anti-reflection cancellation, off-design wavelength degradation, half-wave recurrence, and nonideal coating-index behavior against standard thin-film optics.',
    passSignal:
      'The same route/closure/phase/charge/continuity grammar handles phase-sensitive multilayer interference and amplitude matching without adding a new electromagnetic vocabulary.',
    failSignal:
      'The grammar survives single-boundary Fresnel optics but cannot reproduce thin-film interference constraints.',
    confidenceImpact: '+0.1 if passed, -0.6 if failed',
    priority: 18,
  },
  {
    area: 'Electromagnetic absorbing media',
    currentFrontier: 'post-EM-12 lossy optical-media pressure test',
    externalAnchor:
      'Compare complex-index reflectance, extinction-coefficient absorption, Beer-Lambert attenuation, thickness scaling, transparent-limit recovery, and single-entry energy accounting against standard absorbing-media optics.',
    passSignal:
      'The same route/closure/phase/charge/continuity grammar handles path-length absorption and complex-index boundary response without adding a new electromagnetic vocabulary.',
    failSignal:
      'The grammar survives lossless boundary and thin-film optics but cannot reproduce absorbing-media attenuation constraints.',
    confidenceImpact: '+0.1 if passed, -0.6 if failed',
    priority: 19,
  },
  {
    area: 'Electromagnetic rough-surface scatter',
    currentFrontier: 'post-EM-13 calibrated rough-boundary pressure test',
    externalAnchor:
      'Compare Bennett-Porteus style total integrated scatter, specular-loss factor, roughness scaling, wavelength scaling, incidence-angle scaling, smooth-limit recovery, and reflected-energy budget against standard optical roughness relations.',
    passSignal:
      'The same route/closure/phase/charge/continuity grammar handles RMS roughness as a quantitative phase-disorder loss without adding a new electromagnetic vocabulary.',
    failSignal:
      'The grammar survives absorbing-media optics but cannot reproduce calibrated rough-surface specular-loss constraints.',
    confidenceImpact: '+0.1 if passed, -0.6 if failed',
    priority: 20,
  },
  {
    area: 'Electromagnetic diffraction grating',
    currentFrontier: 'post-EM-14 periodic-aperture diffraction pressure test',
    externalAnchor:
      'Compare normal-incidence grating-equation order angles, spectral angular dispersion, central-order non-dispersion, positive/negative order symmetry, order cutoff, and screen-position scaling against standard diffraction-grating optics.',
    passSignal:
      'The same route/closure/phase/charge/continuity grammar handles periodic phase closure and wavelength-dependent diffraction orders without adding a new electromagnetic vocabulary.',
    failSignal:
      'The grammar survives rough-surface scatter but cannot reproduce periodic-aperture diffraction constraints.',
    confidenceImpact: '+0.1 if passed, -0.6 if failed',
    priority: 21,
  },
  {
    area: 'Electromagnetic single-slit envelope',
    currentFrontier: 'post-EM-15 finite-aperture diffraction-envelope pressure test',
    externalAnchor:
      'Compare single-slit minima, sinc-squared intensity envelope, central maximum, side-lobe relative intensity, wavelength scaling, slit-width scaling, symmetry, and screen-position mapping against standard single-slit Fraunhofer optics.',
    passSignal:
      'The same route/closure/phase/charge/continuity grammar handles finite-aperture envelope intensity without adding a new electromagnetic vocabulary.',
    failSignal:
      'The grammar survives grating order positions but cannot reproduce finite-aperture diffraction-envelope constraints.',
    confidenceImpact: '+0.1 if passed, -0.6 if failed',
    priority: 22,
  },
  {
    area: 'Electromagnetic double-slit envelope coupling',
    currentFrontier: 'post-EM-16 two-aperture interference-envelope pressure test',
    externalAnchor:
      'Compare double-slit fringe spacing, constructive/destructive conditions, single-slit envelope modulation, missing orders, slit-separation scaling, wavelength scaling, symmetry, and screen-position mapping against standard double-slit diffraction optics.',
    passSignal:
      'The same route/closure/phase/charge/continuity grammar handles two-aperture interference under a finite-aperture envelope without adding a new electromagnetic vocabulary.',
    failSignal:
      'The grammar survives single-slit envelopes but cannot reproduce double-slit interference-envelope coupling.',
    confidenceImpact: '+0.1 if passed, -0.6 if failed',
    priority: 23,
  },
  {
    area: 'Material refractive-index property calibration',
    currentFrontier: 'post-NBO/T measured-property pressure test',
    externalAnchor:
      'Compare source-anchored SiO2 and Na2SiO3 refractive-index targets against a predeclared material grammar property predictor.',
    passSignal:
      'The material grammar produces refractive-index values within tolerance without using the target values as fitted endpoints.',
    failSignal:
      'The grammar remains composition accounting only and cannot predict measured material optical properties.',
    confidenceImpact: '+0.3 if passed, -0.2 if unresolved or failed',
    priority: 24,
  },
];

const confidenceGates = [
  {
    gate: 'Internal coherence',
    current: currentStatus.internalCoherenceConfidenceOutOf10,
    nextThreshold: 8,
    requirement: 'At least two watch-band frontiers move to clear without weakening existing clear diagnostics.',
  },
  {
    gate: 'External anchoring',
    current: currentStatus.inferentialConvergenceConfidenceOutOf10,
    nextThreshold: 4,
    requirement: 'At least three independent external comparisons pass without per-case tuning.',
  },
  {
    gate: 'Relational Substrate theory claim strength',
    current: currentStatus.inferentialConvergenceConfidenceOutOf10,
    nextThreshold: 6,
    requirement: 'The model makes at least one nontrivial prediction before fitting and survives external comparison.',
  },
];

const immediatePlan = [
  'Implement a small external-data ingestion shape for benchmark rows without embedding source-specific assumptions in the scoring code.',
  'Start with peroxide torsion because it is the current weakest true frontier and has a clear external analogue.',
  'Record pass/fail criteria before any score adjustment.',
  'Only raise inferential-convergence confidence after an external comparison passes without special tuning.',
];

const json = {
  source: 'external-benchmark-roadmap.mjs',
  status: 'external anchoring roadmap for Relational Substrate sandbox',
  currentStatus,
  currentFrontier: frontier.nextTarget,
  benchmarkTargets,
  confidenceGates,
  immediatePlan,
  sourceMetrics: assumptions.metrics,
};

await writeFile(new URL('external-benchmark-roadmap.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate External Benchmark Roadmap

## Current Status

| Measure | Value |
|---|---:|
| Sandbox completion | ${currentStatus.sandboxCompletionPct}% |
| Internal coherence confidence | ${currentStatus.internalCoherenceConfidenceOutOf10}/10 |
| Inferential convergence confidence | ${currentStatus.inferentialConvergenceConfidenceOutOf10}/10 |

${currentStatus.reason}

Current frontier: ${frontier.nextTarget}.

## Benchmark Targets

| Priority | Area | Current frontier | External anchor | Pass signal | Fail signal | Confidence impact |
|---:|---|---|---|---|---|---|
${benchmarkTargets
  .sort((a, b) => a.priority - b.priority)
  .map(
    (target) =>
      `| ${target.priority} | ${target.area} | ${target.currentFrontier} | ${target.externalAnchor} | ${target.passSignal} | ${target.failSignal} | ${target.confidenceImpact} |`
  )
  .join('\n')}

## Confidence Gates

| Gate | Current | Next threshold | Requirement |
|---|---:|---:|---|
${confidenceGates.map((gate) => `| ${gate.gate} | ${round(gate.current)} | ${gate.nextThreshold} | ${gate.requirement} |`).join('\n')}

## Immediate Plan

${immediatePlan.map((item) => `- ${item}`).join('\n')}

## Reading

The sandbox has earned confidence as an internal coherence machine. It has not earned strong inferential convergence as a Relational Substrate theory. The next confidence gain must come from external comparisons defined before tuning.
`;

await writeFile(new URL('external-benchmark-roadmap.md', outDir), markdown);

console.log(`Current frontier: ${frontier.nextTarget}`);
console.log(`Inferential convergence confidence: ${currentStatus.inferentialConvergenceConfidenceOutOf10}/10`);
console.log(`Wrote ${new URL('external-benchmark-roadmap.md', outDir).pathname}`);
