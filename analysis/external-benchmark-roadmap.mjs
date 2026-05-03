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
  substrateTruthConfidenceOutOf10: 2.5,
  reason:
    'The sandbox now has broad internal coherence checks, but confidence in substrate truth remains low because external prediction and comparison are not yet implemented.',
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
    current: currentStatus.substrateTruthConfidenceOutOf10,
    nextThreshold: 4,
    requirement: 'At least three independent external comparisons pass without per-case tuning.',
  },
  {
    gate: 'Substrate-theory claim strength',
    current: currentStatus.substrateTruthConfidenceOutOf10,
    nextThreshold: 6,
    requirement: 'The model makes at least one nontrivial prediction before fitting and survives external comparison.',
  },
];

const immediatePlan = [
  'Implement a small external-data ingestion shape for benchmark rows without embedding source-specific assumptions in the scoring code.',
  'Start with peroxide torsion because it is the current weakest true frontier and has a clear external analogue.',
  'Record pass/fail criteria before any score adjustment.',
  'Only raise substrate-theory confidence after an external comparison passes without special tuning.',
];

const json = {
  source: 'external-benchmark-roadmap.mjs',
  status: 'external anchoring roadmap for AMS topology sandbox',
  currentStatus,
  currentFrontier: frontier.nextTarget,
  benchmarkTargets,
  confidenceGates,
  immediatePlan,
  sourceMetrics: assumptions.metrics,
};

await writeFile(new URL('external-benchmark-roadmap.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# AMS External Benchmark Roadmap

## Current Status

| Measure | Value |
|---|---:|
| Sandbox completion | ${currentStatus.sandboxCompletionPct}% |
| Internal coherence confidence | ${currentStatus.internalCoherenceConfidenceOutOf10}/10 |
| Substrate truth confidence | ${currentStatus.substrateTruthConfidenceOutOf10}/10 |

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

The sandbox has earned confidence as an internal coherence machine. It has not earned strong confidence as a substrate theory. The next confidence gain must come from external comparisons defined before tuning.
`;

await writeFile(new URL('external-benchmark-roadmap.md', outDir), markdown);

console.log(`Current frontier: ${frontier.nextTarget}`);
console.log(`Substrate truth confidence: ${currentStatus.substrateTruthConfidenceOutOf10}/10`);
console.log(`Wrote ${new URL('external-benchmark-roadmap.md', outDir).pathname}`);
