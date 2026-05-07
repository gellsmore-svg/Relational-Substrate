import { readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

async function readJson(name) {
  return JSON.parse(await readFile(new URL(name, outDir), 'utf8'));
}

async function readOptionalJson(name) {
  try {
    return await readJson(name);
  } catch {
    return null;
  }
}

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

function penaltyBand(value) {
  if (value < 0.1) {
    return 'weak';
  }
  if (value < 0.2) {
    return 'watch';
  }
  return 'clear';
}

function residualBand(value) {
  const magnitude = Math.abs(value);
  if (magnitude > 0.12) {
    return 'weak';
  }
  if (magnitude > 0.08) {
    return 'watch';
  }
  return 'clear';
}

function addPenaltyFrontier(items, source, summary, labelKey = 'case') {
  items.push({
    source,
    label: summary[labelKey] ?? summary.formula ?? summary.label,
    challenger: summary.bestDecoy ?? summary.decoy ?? 'nearest decoy',
    metric: 'decoy penalty',
    value: summary.decoyPenalty,
    band: penaltyBand(summary.decoyPenalty),
  });
}

const calibration = await readJson('molecule-calibration-summary.json');
const stability = await readJson('t1-target-stability.json');
const ethaneTorsion = await readOptionalJson('ethane-torsion-sweep.json');
const peroxideTorsion = await readOptionalJson('peroxide-torsion-sweep.json');
const peroxideRefinement = await readOptionalJson('peroxide-nonlocal-refinement.json');
const ionicLattice = await readOptionalJson('ionic-lattice-sweep.json');
const silicateNetwork = await readOptionalJson('silicate-network-sweep.json');
const mixedModifier = await readOptionalJson('mixed-modifier-sweep.json');
const boundaryTransition = await readOptionalJson('boundary-transition-sweep.json');
const phaseContinuity = await readOptionalJson('phase-continuity-sweep.json');

const frontiers = [];
const localToleranceFrontiers = [];

for (const control of calibration.controls) {
  frontiers.push({
    source: 'molecule decoy control',
    label: control.label,
    challenger: control.expectedFailure ?? control.candidate?.name ?? 'explicit decoy control',
    metric: 'decoy penalty',
    value: control.decoyPenalty,
    band: penaltyBand(control.decoyPenalty),
  });
}

if (ethaneTorsion) {
  frontiers.push({
    source: 'ethane torsion',
    label: 'weakest eclipsed conformer',
    challenger: 'eclipsed-like phase',
    metric: 'torsion penalty',
    value: ethaneTorsion.summary.weakestEclipsedPenalty,
    band: penaltyBand(ethaneTorsion.summary.weakestEclipsedPenalty),
  });
}

if (peroxideTorsion) {
  if (typeof peroxideTorsion.summary.lowestNearReferencePenalty === 'number') {
    localToleranceFrontiers.push({
      source: 'peroxide torsion tolerance',
      label: 'nearest local torsion neighbour',
      challenger: `${peroxideTorsion.summary.nearReferenceWindow} degree near-reference window`,
      metric: 'local tolerance penalty',
      value: peroxideTorsion.summary.lowestNearReferencePenalty,
      band: 'local',
    });
  }
  frontiers.push({
    source: 'peroxide torsion',
    label: 'nonlocal torsion challenger',
    challenger: 'nonlocal torsion decoy',
    metric: 'torsion penalty',
    value: peroxideRefinement?.summary.frontierPenalty ?? peroxideTorsion.summary.frontierPenalty ?? peroxideTorsion.summary.lowestNonLocalPenalty,
    band: penaltyBand(peroxideRefinement?.summary.frontierPenalty ?? peroxideTorsion.summary.frontierPenalty ?? peroxideTorsion.summary.lowestNonLocalPenalty),
  });
}

if (peroxideRefinement) {
  for (const item of peroxideRefinement.summary.byBand.filter((band) => band.band !== 'nonlocal')) {
    localToleranceFrontiers.push({
      source: 'peroxide torsion refinement',
      label: item.band,
      challenger: `${item.rows} refined torsion rows`,
      metric: 'weakest penalty',
      value: item.weakestPenalty,
      band: item.band === 'near-reference' ? 'local' : 'shoulder',
    });
  }
}

for (const report of [
  ['ionic lattice', ionicLattice, 'formula'],
  ['silicate network', silicateNetwork, 'formula'],
  ['mixed modifier', mixedModifier, 'formula'],
  ['boundary transition', boundaryTransition, 'case'],
  ['phase continuity', phaseContinuity, 'case'],
]) {
  const [source, data, labelKey] = report;
  if (!data) {
    continue;
  }
  for (const summary of data.summaries) {
    addPenaltyFrontier(frontiers, source, summary, labelKey);
  }
}

const residualFrontiers = [
  ...stability.weakestFamilies.slice(0, 6).map((family) => ({
    source: 'T1 family residual',
    label: family.family,
    challenger: 'best admissible T1 candidate',
    metric: 'residual',
    value: family.residual,
    magnitude: Math.abs(family.residual),
    band: residualBand(family.residual),
  })),
  ...stability.weakestParameters.slice(0, 6).map((parameter) => ({
    source: 'T1 parameter residual',
    label: parameter.parameter,
    challenger: 'derived target envelope',
    metric: 'mean residual',
    value: parameter.meanResidual,
    magnitude: Math.abs(parameter.meanResidual),
    band: residualBand(parameter.meanResidual),
  })),
];

const rankedPenaltyFrontiers = frontiers
  .filter((item) => typeof item.value === 'number')
  .sort((a, b) => a.value - b.value)
  .map((item) => ({ ...item, value: round(item.value) }));
const rankedResidualFrontiers = residualFrontiers
  .filter((item) => typeof item.value === 'number')
  .sort((a, b) => b.magnitude - a.magnitude)
  .map((item) => ({ ...item, value: round(item.value), magnitude: round(item.magnitude) }));

const weakestPenalty = rankedPenaltyFrontiers[0];
const weakestResidual = rankedResidualFrontiers[0];
const nextTarget =
  weakestPenalty?.band === 'weak'
    ? `tighten ${weakestPenalty.source}: ${weakestPenalty.label}`
    : weakestPenalty?.band === 'watch'
      ? `watch and refine ${weakestPenalty.source}: ${weakestPenalty.label}`
    : weakestResidual?.band === 'weak'
      ? `tighten ${weakestResidual.source}: ${weakestResidual.label}`
      : 'add an independent external benchmark case rather than tuning existing diagnostics';

const json = {
  source: 'model-frontier-report.mjs',
  status: 'frontier report over current topology sandbox diagnostics',
  nextTarget,
  weakestPenalty,
  weakestResidual,
  localToleranceFrontiers,
  rankedPenaltyFrontiers,
  rankedResidualFrontiers,
};

await writeFile(new URL('model-frontier-report.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate Sandbox Frontier Report

## Scope

This report ranks the current sandbox pressure points across molecule controls, focused torsion diagnostics, material/interface diagnostics, and T1 residual reports.

It does not add a new model. It prevents the next step from being chosen by habit when an existing weak separation or residual already points to a better target.

## Next Target

${nextTarget}.

## Weakest Decoy / Challenger Separations

| Rank | Source | Label | Challenger | Metric | Value | Band |
|---:|---|---|---|---|---:|---|
${rankedPenaltyFrontiers
  .slice(0, 14)
  .map(
    (item, index) =>
      `| ${index + 1} | ${item.source} | ${item.label} | ${item.challenger} | ${item.metric} | ${item.value} | ${item.band} |`
  )
  .join('\n')}

## Local Tolerance Context

| Source | Label | Context | Metric | Value | Band |
|---|---|---|---|---:|---|
${localToleranceFrontiers
  .map((item) => `| ${item.source} | ${item.label} | ${item.challenger} | ${item.metric} | ${round(item.value)} | ${item.band} |`)
  .join('\n')}

## Weakest T1 Residuals

| Rank | Source | Label | Comparator | Metric | Value | Magnitude | Band |
|---:|---|---|---|---|---:|---:|---|
${rankedResidualFrontiers
  .slice(0, 12)
  .map(
    (item, index) =>
      `| ${index + 1} | ${item.source} | ${item.label} | ${item.challenger} | ${item.metric} | ${item.value} | ${item.magnitude} | ${item.band} |`
  )
  .join('\n')}

## Reading

Weak decoy penalties mean a diagnostic can still rank the reference first while failing to create enough clearance against a plausible wrong arrangement. Local tolerance rows are reported for context but should not be treated as hard decoy failures. High residuals mean the T1 target formula or admissible grid still does not match a T2-derived envelope cleanly.
`;

await writeFile(new URL('model-frontier-report.md', outDir), markdown);

console.log(`Next target: ${nextTarget}`);
console.log(`Wrote ${new URL('model-frontier-report.md', outDir).pathname}`);
