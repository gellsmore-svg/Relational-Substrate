import { mkdir, writeFile } from 'node:fs/promises';
import { clamp01 } from './molecule-model.mjs';

const outDir = new URL('./out/', import.meta.url);

const cases = [
  {
    formula: 'SiO2 network',
    type: 'fused-silica proxy',
    targetModifierPerAl: 0,
    expectedModifierRate: 0,
    expectedAlRate: 0,
    routeBase: 0.72,
  },
  {
    formula: 'Na2SiO3 network',
    type: 'modifier silicate proxy',
    targetModifierPerAl: 0,
    expectedModifierRate: 0.25,
    expectedAlRate: 0,
    routeBase: 0.68,
  },
  {
    formula: 'NaAlSi3O8 network',
    type: 'charge-compensated aluminosilicate proxy',
    targetModifierPerAl: 1,
    expectedModifierRate: 0.25,
    expectedAlRate: 0.25,
    routeBase: 0.7,
  },
];

const variants = [
  {
    name: 'continuous compensated network',
    kind: 'reference',
    networkContinuity: 1,
    bridgingRate: 0.92,
    nonbridgingRate: 0.08,
    modifierBalance: 1,
    alCompensation: 1,
    tetrahedralIntegrity: 0.96,
    modifierClustering: 0.1,
    terminalOxygenExcess: 0.08,
  },
  {
    name: 'strained depolymerised network',
    kind: 'strained',
    networkContinuity: 0.72,
    bridgingRate: 0.64,
    nonbridgingRate: 0.28,
    modifierBalance: 0.82,
    alCompensation: 0.84,
    tetrahedralIntegrity: 0.82,
    modifierClustering: 0.22,
    terminalOxygenExcess: 0.26,
  },
  {
    name: 'overlinked edge-sharing network',
    kind: 'strained',
    networkContinuity: 0.86,
    bridgingRate: 0.98,
    nonbridgingRate: 0.02,
    modifierBalance: 0.66,
    alCompensation: 0.74,
    tetrahedralIntegrity: 0.58,
    modifierClustering: 0.18,
    terminalOxygenExcess: 0.04,
  },
  {
    name: 'isolated tetrahedra',
    kind: 'decoy',
    networkContinuity: 0.18,
    bridgingRate: 0.16,
    nonbridgingRate: 0.74,
    modifierBalance: 0.42,
    alCompensation: 0.48,
    tetrahedralIntegrity: 0.74,
    modifierClustering: 0.56,
    terminalOxygenExcess: 0.72,
  },
  {
    name: 'modifier-clustered channels',
    kind: 'decoy',
    networkContinuity: 0.55,
    bridgingRate: 0.5,
    nonbridgingRate: 0.38,
    modifierBalance: 0.38,
    alCompensation: 0.54,
    tetrahedralIntegrity: 0.78,
    modifierClustering: 0.86,
    terminalOxygenExcess: 0.36,
  },
  {
    name: 'uncompensated aluminium substitutions',
    kind: 'decoy',
    networkContinuity: 0.78,
    bridgingRate: 0.82,
    nonbridgingRate: 0.12,
    modifierBalance: 0.34,
    alCompensation: 0.16,
    tetrahedralIntegrity: 0.82,
    modifierClustering: 0.28,
    terminalOxygenExcess: 0.14,
  },
];

function caseAdjustedVariant(testCase, variant) {
  const modifierNeed = testCase.expectedModifierRate;
  const alNeed = testCase.expectedAlRate;
  const modifierBalance =
    modifierNeed === 0
      ? clamp01(variant.kind === 'reference' ? 1 - variant.modifierClustering * 0.25 : variant.modifierBalance + 0.18)
      : variant.modifierBalance;
  const alCompensation =
    alNeed === 0
      ? clamp01(variant.kind === 'reference' ? 1 : variant.alCompensation + 0.16)
      : variant.alCompensation;
  const modifierDistribution = clamp01(1 - variant.modifierClustering * (modifierNeed > 0 ? 1 : 0.45));
  const chargeBalance = clamp01(modifierBalance * 0.45 + alCompensation * 0.45 + modifierDistribution * 0.1);
  const topologyContinuity = clamp01(
    variant.networkContinuity * 0.45 + variant.bridgingRate * 0.32 + (1 - variant.terminalOxygenExcess) * 0.23
  );
  const tetrahedralNetwork = clamp01(
    variant.tetrahedralIntegrity * 0.45 + topologyContinuity * 0.35 + (1 - Math.abs(variant.bridgingRate - 0.9)) * 0.2
  );
  const modifierOrdering = clamp01(
    modifierNeed === 0
      ? 1 - variant.nonbridgingRate * 0.6 - variant.modifierClustering * 0.2
      : modifierBalance * 0.45 + modifierDistribution * 0.35 + (1 - Math.abs(variant.nonbridgingRate - 0.25)) * 0.2
  );
  const alOrdering = clamp01(alNeed === 0 ? alCompensation : alCompensation * 0.75 + modifierDistribution * 0.25);
  const routeContinuity = clamp01(
    testCase.routeBase + topologyContinuity * 0.15 + chargeBalance * 0.1 - variant.terminalOxygenExcess * 0.18
  );
  const collapseRisk = clamp01(
    (1 - topologyContinuity) * 0.34 +
      (1 - chargeBalance) * 0.26 +
      variant.modifierClustering * 0.22 +
      variant.terminalOxygenExcess * 0.18
  );
  const score = clamp01(
    topologyContinuity * 0.25 +
      tetrahedralNetwork * 0.2 +
      chargeBalance * 0.18 +
      modifierOrdering * 0.14 +
      alOrdering * 0.1 +
      routeContinuity * 0.08 +
      (1 - collapseRisk) * 0.05
  );

  return {
    formula: testCase.formula,
    materialType: testCase.type,
    variant: variant.name,
    kind: variant.kind,
    score: Number(score.toFixed(4)),
    topologyContinuity: Number(topologyContinuity.toFixed(3)),
    tetrahedralNetwork: Number(tetrahedralNetwork.toFixed(3)),
    chargeBalance: Number(chargeBalance.toFixed(3)),
    modifierOrdering: Number(modifierOrdering.toFixed(3)),
    alOrdering: Number(alOrdering.toFixed(3)),
    routeContinuity: Number(routeContinuity.toFixed(3)),
    collapseRisk: Number(collapseRisk.toFixed(3)),
    bridgingRate: Number(variant.bridgingRate.toFixed(3)),
    nonbridgingRate: Number(variant.nonbridgingRate.toFixed(3)),
    modifierClustering: Number(variant.modifierClustering.toFixed(3)),
  };
}

const rows = cases.flatMap((testCase) => variants.map((variant) => caseAdjustedVariant(testCase, variant)));
const summaries = cases.map((testCase) => {
  const caseRows = rows.filter((row) => row.formula === testCase.formula);
  const reference = caseRows.find((row) => row.kind === 'reference');
  const decoys = caseRows.filter((row) => row.kind === 'decoy');
  const strained = caseRows.filter((row) => row.kind === 'strained');
  const bestDecoy = decoys.reduce((best, row) => (row.score > best.score ? row : best), decoys[0]);
  const bestStrained = strained.reduce((best, row) => (row.score > best.score ? row : best), strained[0]);

  return {
    formula: testCase.formula,
    materialType: testCase.type,
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
  ? `weak silicate network separation for ${weak.map((item) => item.formula).join(', ')}`
  : 'silicate network controls separate continuous compensated networks from fragmented, clustered, or uncompensated decoys';

const json = {
  source: 'silicate-network-sweep.mjs',
  status: 'focused silicate/aluminosilicate network diagnostic; not part of molecule calibration',
  diagnosis,
  summaries,
  rows,
};

await mkdir(outDir, { recursive: true });
await writeFile(new URL('silicate-network-sweep.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate Silicate Network Sweep

## Scope

This diagnostic addresses a material-structure gap that sits beyond molecule geometry: small silicate and aluminosilicate network order.

It does not simulate glass physics, crystals, melt dynamics, or real material properties. It tests a graph-level route grammar: continuous tetrahedral networks with plausible modifier placement and aluminium charge compensation should outrank fragmented, modifier-clustered, or uncompensated decoys.

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

| Formula | Variant | Kind | Score | Topology continuity | Tetrahedral network | Charge balance | Modifier ordering | Al ordering | Route continuity | Collapse risk | Bridging rate | Nonbridging rate | Modifier clustering |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
${rows
  .map(
    (row) =>
      `| ${row.formula} | ${row.variant} | ${row.kind} | ${row.score} | ${row.topologyContinuity} | ${row.tetrahedralNetwork} | ${row.chargeBalance} | ${row.modifierOrdering} | ${row.alOrdering} | ${row.routeContinuity} | ${row.collapseRisk} | ${row.bridgingRate} | ${row.nonbridgingRate} | ${row.modifierClustering} |`
  )
  .join('\n')}

## Reading

This is a topology/control diagnostic. The useful question is whether the route grammar can reject obvious network failures before attempting richer bulk-material modelling.
`;

await writeFile(new URL('silicate-network-sweep.md', outDir), markdown);

console.log(`Cases tested: ${cases.length}`);
console.log(`Diagnosis: ${diagnosis}`);
console.log(`Wrote ${new URL('silicate-network-sweep.md', outDir).pathname}`);
