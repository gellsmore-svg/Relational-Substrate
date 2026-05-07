import { readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const sweepUrl = new URL('t1-coupling-sweep.json', outDir);

const parameterNames = [
  'closureIntegrity',
  'routeCountFit',
  'routeContinuity',
  'tensionBalance',
  'polarityResolution',
  'angularConstraint',
  'torsionTolerance',
  'distributionCoherence',
  'identityPreservation',
  'leakageRisk',
];

function average(values) {
  return values.length ? values.reduce((sum, value) => sum + value, 0) / values.length : 0;
}

function maxAbs(values) {
  return values.length ? Math.max(...values.map((value) => Math.abs(value))) : 0;
}

function format(value) {
  return Number(value.toFixed(4));
}

function stabilityLabel(meanAbsoluteResidual) {
  if (meanAbsoluteResidual <= 0.045) return 'tight';
  if (meanAbsoluteResidual <= 0.075) return 'usable';
  return 'loose';
}

function directionLabel(residual) {
  if (residual > 0.04) return 'candidate high';
  if (residual < -0.04) return 'candidate low';
  return 'aligned';
}

const sweep = JSON.parse(await readFile(sweepUrl, 'utf8'));

const familyResiduals = sweep.families.map((family) => {
  const best = family.best[0];
  const residuals = Object.fromEntries(
    parameterNames.map((parameter) => [parameter, format(best.candidate[parameter] - family.target[parameter])])
  );
  const absoluteResiduals = parameterNames.map((parameter) => Math.abs(residuals[parameter]));
  const meanAbsoluteResidual = average(absoluteResiduals);
  const maxAbsoluteResidual = maxAbs(absoluteResiduals);
  const largestResidualParameter = parameterNames
    .map((parameter) => ({ parameter, residual: residuals[parameter], absoluteResidual: Math.abs(residuals[parameter]) }))
    .sort((a, b) => b.absoluteResidual - a.absoluteResidual)[0];

  return {
    family: family.family,
    patternName: family.patternName,
    bestScore: best.score,
    meanAbsoluteResidual: format(meanAbsoluteResidual),
    maxAbsoluteResidual: format(maxAbsoluteResidual),
    largestResidualParameter,
    stability: stabilityLabel(meanAbsoluteResidual),
    residuals,
    targetDerivation: family.targetDerivation,
  };
});

const parameterResiduals = parameterNames.map((parameter) => {
  const values = familyResiduals.map((family) => family.residuals[parameter]);
  const meanResidual = average(values);
  const meanAbsoluteResidual = average(values.map((value) => Math.abs(value)));
  const maxAbsoluteResidual = maxAbs(values);
  return {
    parameter,
    meanResidual: format(meanResidual),
    meanAbsoluteResidual: format(meanAbsoluteResidual),
    maxAbsoluteResidual: format(maxAbsoluteResidual),
    direction: directionLabel(meanResidual),
  };
});

const json = {
  source: 't1-coupling-sweep.json',
  status: 'derived-target stability report; not proof and not a hidden material layer',
  familyResiduals,
  parameterResiduals,
  weakestFamilies: [...familyResiduals].sort((a, b) => b.meanAbsoluteResidual - a.meanAbsoluteResidual).slice(0, 3),
  weakestParameters: [...parameterResiduals].sort((a, b) => b.meanAbsoluteResidual - a.meanAbsoluteResidual).slice(0, 5),
};

await writeFile(new URL('t1-target-stability.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate T1 Target Stability

## Scope

This report reads \`t1-coupling-sweep.json\` and checks how closely the best admissible candidate in each family matches the T2-derived target envelope.

It does not prove the Relational Substrate theory and does not add any material layer between \`T0\` substrate and T1 vortons. It is a residual report for the current target-derivation formula.

## Family Residuals

| Family | Pattern | Best score | Mean abs residual | Max abs residual | Largest residual | Direction | Stability |
|---|---|---:|---:|---:|---|---|---|
${familyResiduals
  .map(
    (family) =>
      `| ${family.family} | ${family.patternName} | ${family.bestScore} | ${family.meanAbsoluteResidual} | ${family.maxAbsoluteResidual} | ${family.largestResidualParameter.parameter} | ${directionLabel(family.largestResidualParameter.residual)} | ${family.stability} |`
  )
  .join('\n')}

## Parameter Residuals

| Parameter | Mean residual | Mean abs residual | Max abs residual | Direction |
|---|---:|---:|---:|---|
${parameterResiduals
  .map(
    (parameter) =>
      `| ${parameter.parameter} | ${parameter.meanResidual} | ${parameter.meanAbsoluteResidual} | ${parameter.maxAbsoluteResidual} | ${parameter.direction} |`
  )
  .join('\n')}

## Weakest Families

${json.weakestFamilies
  .map(
    (family) =>
      `- ${family.family}: ${family.stability}, mean abs residual ${family.meanAbsoluteResidual}, largest residual ${family.largestResidualParameter.parameter} (${family.largestResidualParameter.residual})`
  )
  .join('\n')}

## Weakest Parameters

${json.weakestParameters
  .map(
    (parameter) =>
      `- ${parameter.parameter}: ${parameter.direction}, mean abs residual ${parameter.meanAbsoluteResidual}, max abs residual ${parameter.maxAbsoluteResidual}`
  )
  .join('\n')}

## Interpretation

Tight residuals mean the current grid can express the T2-derived target without much mismatch. Loose residuals mean either the target formula is over-demanding, the parameter grid is too coarse, or the guardrails are excluding candidates that would otherwise fit.

The next useful step is to run a local refinement sweep around the current best candidates using narrower parameter levels. That will distinguish coarse-grid error from genuine formula weakness.
`;

await writeFile(new URL('t1-target-stability.md', outDir), markdown);

console.log(`Read ${sweepUrl.pathname}`);
console.log(`Wrote ${new URL('t1-target-stability.md', outDir).pathname}`);
