import { mkdir, writeFile } from 'node:fs/promises';
import { clamp01 } from './molecule-model.mjs';

const outDir = new URL('./out/', import.meta.url);

const cases = [
  {
    formula: 'Na-K silicate',
    materialType: 'mixed alkali modifier proxy',
    routeBase: 0.69,
    targetMixBalance: 0.5,
    fieldMismatch: 0.18,
  },
  {
    formula: 'Na-Mg aluminosilicate',
    materialType: 'mixed monovalent/divalent modifier proxy',
    routeBase: 0.67,
    targetMixBalance: 0.58,
    fieldMismatch: 0.32,
  },
  {
    formula: 'Ca-Na phosphate glass',
    materialType: 'cross-linked phosphate modifier proxy',
    routeBase: 0.66,
    targetMixBalance: 0.46,
    fieldMismatch: 0.27,
  },
];

const variants = [
  {
    name: 'distributed compensated modifiers',
    kind: 'reference',
    networkAccess: 0.9,
    modifierMixBalance: 0.92,
    chargeCompensation: 0.94,
    channelContinuity: 0.86,
    localFieldSmoothing: 0.88,
    clustering: 0.12,
    depletionZones: 0.08,
    blockedRoutes: 0.1,
  },
  {
    name: 'mild field-mismatch segregation',
    kind: 'strained',
    networkAccess: 0.76,
    modifierMixBalance: 0.72,
    chargeCompensation: 0.79,
    channelContinuity: 0.7,
    localFieldSmoothing: 0.65,
    clustering: 0.28,
    depletionZones: 0.2,
    blockedRoutes: 0.22,
  },
  {
    name: 'partly blocked modifier channels',
    kind: 'strained',
    networkAccess: 0.64,
    modifierMixBalance: 0.78,
    chargeCompensation: 0.8,
    channelContinuity: 0.52,
    localFieldSmoothing: 0.72,
    clustering: 0.2,
    depletionZones: 0.18,
    blockedRoutes: 0.42,
  },
  {
    name: 'single-modifier dominance',
    kind: 'decoy',
    networkAccess: 0.62,
    modifierMixBalance: 0.18,
    chargeCompensation: 0.54,
    channelContinuity: 0.58,
    localFieldSmoothing: 0.46,
    clustering: 0.36,
    depletionZones: 0.34,
    blockedRoutes: 0.3,
  },
  {
    name: 'clustered modifier islands',
    kind: 'decoy',
    networkAccess: 0.5,
    modifierMixBalance: 0.48,
    chargeCompensation: 0.56,
    channelContinuity: 0.4,
    localFieldSmoothing: 0.32,
    clustering: 0.84,
    depletionZones: 0.5,
    blockedRoutes: 0.44,
  },
  {
    name: 'depleted transport corridors',
    kind: 'decoy',
    networkAccess: 0.42,
    modifierMixBalance: 0.62,
    chargeCompensation: 0.5,
    channelContinuity: 0.22,
    localFieldSmoothing: 0.44,
    clustering: 0.3,
    depletionZones: 0.82,
    blockedRoutes: 0.68,
  },
  {
    name: 'overcompensated field traps',
    kind: 'decoy',
    networkAccess: 0.58,
    modifierMixBalance: 0.56,
    chargeCompensation: 0.22,
    channelContinuity: 0.5,
    localFieldSmoothing: 0.2,
    clustering: 0.62,
    depletionZones: 0.36,
    blockedRoutes: 0.5,
  },
];

function scoreVariant(testCase, variant) {
  const mixDistance = Math.abs(variant.modifierMixBalance - testCase.targetMixBalance);
  const mixCoherence = clamp01(1 - mixDistance / 0.58);
  const mismatchPenalty = clamp01(testCase.fieldMismatch * (1 - variant.localFieldSmoothing) + variant.clustering * 0.2);
  const transportContinuity = clamp01(
    variant.networkAccess * 0.32 +
      variant.channelContinuity * 0.36 +
      (1 - variant.blockedRoutes) * 0.2 +
      (1 - variant.depletionZones) * 0.12
  );
  const modifierDistribution = clamp01(
    mixCoherence * 0.35 +
      variant.modifierMixBalance * 0.2 +
      (1 - variant.clustering) * 0.25 +
      (1 - variant.depletionZones) * 0.2
  );
  const chargeFieldOrder = clamp01(
    variant.chargeCompensation * 0.42 +
      variant.localFieldSmoothing * 0.28 +
      modifierDistribution * 0.18 +
      (1 - mismatchPenalty) * 0.12
  );
  const routeContinuity = clamp01(
    testCase.routeBase +
      transportContinuity * 0.13 +
      chargeFieldOrder * 0.09 -
      variant.blockedRoutes * 0.15 -
      mismatchPenalty * 0.1
  );
  const percolationRisk = clamp01(
    (1 - transportContinuity) * 0.34 +
      variant.blockedRoutes * 0.24 +
      variant.depletionZones * 0.18 +
      variant.clustering * 0.16 +
      mismatchPenalty * 0.08
  );
  const score = clamp01(
    transportContinuity * 0.26 +
      modifierDistribution * 0.22 +
      chargeFieldOrder * 0.2 +
      routeContinuity * 0.12 +
      (1 - percolationRisk) * 0.12 +
      (1 - mismatchPenalty) * 0.08
  );

  return {
    formula: testCase.formula,
    materialType: testCase.materialType,
    variant: variant.name,
    kind: variant.kind,
    score: Number(score.toFixed(4)),
    transportContinuity: Number(transportContinuity.toFixed(3)),
    modifierDistribution: Number(modifierDistribution.toFixed(3)),
    chargeFieldOrder: Number(chargeFieldOrder.toFixed(3)),
    routeContinuity: Number(routeContinuity.toFixed(3)),
    percolationRisk: Number(percolationRisk.toFixed(3)),
    mismatchPenalty: Number(mismatchPenalty.toFixed(3)),
    clustering: Number(variant.clustering.toFixed(3)),
    depletionZones: Number(variant.depletionZones.toFixed(3)),
    blockedRoutes: Number(variant.blockedRoutes.toFixed(3)),
  };
}

const rows = cases.flatMap((testCase) => variants.map((variant) => scoreVariant(testCase, variant)));
const summaries = cases.map((testCase) => {
  const caseRows = rows.filter((row) => row.formula === testCase.formula);
  const reference = caseRows.find((row) => row.kind === 'reference');
  const decoys = caseRows.filter((row) => row.kind === 'decoy');
  const strained = caseRows.filter((row) => row.kind === 'strained');
  const bestDecoy = decoys.reduce((best, row) => (row.score > best.score ? row : best), decoys[0]);
  const bestStrained = strained.reduce((best, row) => (row.score > best.score ? row : best), strained[0]);

  return {
    formula: testCase.formula,
    materialType: testCase.materialType,
    referenceScore: reference.score,
    bestStrained: bestStrained.variant,
    bestStrainedScore: bestStrained.score,
    bestDecoy: bestDecoy.variant,
    bestDecoyScore: bestDecoy.score,
    decoyPenalty: Number((reference.score - bestDecoy.score).toFixed(4)),
    referenceBeatsDecoys: decoys.every((row) => reference.score > row.score),
  };
});

const weak = summaries.filter((summary) => summary.decoyPenalty < 0.1 || !summary.referenceBeatsDecoys);
const diagnosis = weak.length
  ? `weak mixed-modifier separation for ${weak.map((item) => item.formula).join(', ')}`
  : 'mixed-modifier controls separate distributed transport order from clustered, depleted, or field-trapped decoys';

const json = {
  source: 'mixed-modifier-sweep.mjs',
  status: 'focused mixed-modifier transport diagnostic; not part of molecule calibration',
  diagnosis,
  summaries,
  rows,
};

await mkdir(outDir, { recursive: true });
await writeFile(new URL('mixed-modifier-sweep.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate Mixed-Modifier Sweep

## Scope

This diagnostic extends the material-structure reports from static silicate network order into mixed-modifier transport order.

It does not simulate diffusion, glass transition behaviour, conductivity, or measured durability. It tests a route grammar: distributed compensated modifiers with continuous transport access should outrank single-modifier dominance, clustered islands, depleted corridors, and overcompensated field traps.

## Summary

Diagnosis: ${diagnosis}.

| Formula | Material type | Reference score | Best strained | Best strained score | Best decoy | Best decoy score | Decoy penalty | Reference beats decoys |
|---|---|---:|---|---:|---|---:|---:|---|
${summaries
  .map(
    (summary) =>
      `| ${summary.formula} | ${summary.materialType} | ${summary.referenceScore} | ${summary.bestStrained} | ${summary.bestStrainedScore} | ${summary.bestDecoy} | ${summary.bestDecoyScore} | ${summary.decoyPenalty} | ${summary.referenceBeatsDecoys ? 'yes' : 'no'} |`
  )
  .join('\n')}

## Variant Rows

| Formula | Variant | Kind | Score | Transport continuity | Modifier distribution | Charge-field order | Route continuity | Percolation risk | Mismatch penalty | Clustering | Depletion zones | Blocked routes |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
${rows
  .map(
    (row) =>
      `| ${row.formula} | ${row.variant} | ${row.kind} | ${row.score} | ${row.transportContinuity} | ${row.modifierDistribution} | ${row.chargeFieldOrder} | ${row.routeContinuity} | ${row.percolationRisk} | ${row.mismatchPenalty} | ${row.clustering} | ${row.depletionZones} | ${row.blockedRoutes} |`
  )
  .join('\n')}

## Reading

This is a topology/control diagnostic. The useful question is whether mixed modifier order can be treated as route continuity plus local charge-field balance before attempting physically calibrated transport models.
`;

await writeFile(new URL('mixed-modifier-sweep.md', outDir), markdown);

console.log(`Cases tested: ${cases.length}`);
console.log(`Diagnosis: ${diagnosis}`);
console.log(`Wrote ${new URL('mixed-modifier-sweep.md', outDir).pathname}`);
