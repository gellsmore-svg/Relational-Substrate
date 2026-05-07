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
