import { readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const sweepUrl = new URL('t1-coupling-sweep.json', outDir);
const stabilityUrl = new URL('t1-target-stability.json', outDir);

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

const weights = {
  closureIntegrity: 0.14,
  routeCountFit: 0.1,
  routeContinuity: 0.13,
  tensionBalance: 0.12,
  polarityResolution: 0.1,
  angularConstraint: 0.11,
  torsionTolerance: 0.07,
  distributionCoherence: 0.11,
  identityPreservation: 0.14,
  leakageRisk: 0.08,
};

const totalWeight = Object.values(weights).reduce((sum, value) => sum + value, 0);
const offsets = [-0.04, -0.02, 0, 0.02, 0.04];

function clamp(value, minValue, maxValue) {
  return Math.max(minValue, Math.min(maxValue, value));
}

function format(value) {
  return Number(value.toFixed(4));
}

function boundsFor(parameter) {
  return parameter === 'leakageRisk' ? [0.03, 0.35] : [0.42, 0.96];
}

function scoreCandidate(candidate, target) {
  const rawScore = parameterNames.reduce((sum, parameter) => {
    const distance = Math.abs(candidate[parameter] - target[parameter]);
    return sum + Math.max(0, 1 - distance / 0.55) * weights[parameter];
  }, 0);
  return rawScore / totalWeight;
}

function rejectReason(candidate) {
  if (candidate.closureIntegrity < 0.6) return 'closure integrity below stable-coupling floor';
  if (candidate.identityPreservation < 0.6) return 'identity preservation below stable-coupling floor';
  if (candidate.routeContinuity < 0.6 && candidate.routeCountFit > 0.75) return 'many routes without route continuity';
  if (candidate.distributionCoherence > 0.75 && candidate.leakageRisk > 0.45) return 'distributed route with high leakage';
  if (candidate.polarityResolution > 0.75 && candidate.tensionBalance < 0.6) return 'polarity lock without tension balance';
  if (candidate.angularConstraint > 0.75 && candidate.torsionTolerance < 0.6) return 'strong angle constraint with poor torsion tolerance';
  if (candidate.leakageRisk > 0.6) return 'leakage risk too high for persistent coupling';
  return null;
}

function* localCandidates(base, refinedParameters, index = 0, current = { ...base }) {
  if (index === refinedParameters.length) {
    yield { ...current };
    return;
  }

  const parameter = refinedParameters[index];
  const [minValue, maxValue] = boundsFor(parameter);
  const seen = new Set();

  for (const offset of offsets) {
    const value = format(clamp(base[parameter] + offset, minValue, maxValue));
    if (seen.has(value)) continue;
    seen.add(value);
    yield* localCandidates(base, refinedParameters, index + 1, { ...current, [parameter]: value });
  }
}

function residualSummary(candidate, target) {
  const residuals = Object.fromEntries(parameterNames.map((parameter) => [parameter, format(candidate[parameter] - target[parameter])]));
  const absoluteResiduals = parameterNames.map((parameter) => Math.abs(residuals[parameter]));
  const meanAbsoluteResidual = absoluteResiduals.reduce((sum, value) => sum + value, 0) / absoluteResiduals.length;
  const largestResidual = parameterNames
    .map((parameter) => ({ parameter, residual: residuals[parameter], absoluteResidual: Math.abs(residuals[parameter]) }))
    .sort((a, b) => b.absoluteResidual - a.absoluteResidual)[0];

  return {
    residuals,
    meanAbsoluteResidual: format(meanAbsoluteResidual),
    maxAbsoluteResidual: format(largestResidual.absoluteResidual),
    largestResidual,
  };
}

function compact(row) {
  return {
    score: format(row.score),
    meanAbsoluteResidual: row.summary.meanAbsoluteResidual,
    maxAbsoluteResidual: row.summary.maxAbsoluteResidual,
    largestResidual: row.summary.largestResidual,
    candidate: row.candidate,
  };
}

function insertTop(rows, row, limit = 12) {
  rows.push(row);
  rows.sort((a, b) => b.score - a.score || a.summary.meanAbsoluteResidual - b.summary.meanAbsoluteResidual);
  if (rows.length > limit) {
    rows.pop();
  }
}

const sweep = JSON.parse(await readFile(sweepUrl, 'utf8'));
const stability = JSON.parse(await readFile(stabilityUrl, 'utf8'));
const refinedParameters = stability.weakestParameters.slice(0, 5).map((parameter) => parameter.parameter);
const families = [];
let totalIterations = 0;
let acceptedIterations = 0;
let rejectedIterations = 0;
const globalRejected = {};

for (const family of sweep.families) {
  const base = family.best[0].candidate;
  const baseSummary = residualSummary(base, family.target);
  const topRows = [];
  const rejected = {};
  let familyIterations = 0;
  let familyAccepted = 0;
  let familyRejected = 0;

  for (const candidate of localCandidates(base, refinedParameters)) {
    familyIterations += 1;
    totalIterations += 1;
    const reason = rejectReason(candidate);
    if (reason) {
      rejected[reason] = (rejected[reason] ?? 0) + 1;
      globalRejected[reason] = (globalRejected[reason] ?? 0) + 1;
      familyRejected += 1;
      rejectedIterations += 1;
      continue;
    }

    const summary = residualSummary(candidate, family.target);
    insertTop(topRows, {
      score: scoreCandidate(candidate, family.target),
      candidate,
      summary,
    });
    familyAccepted += 1;
    acceptedIterations += 1;
  }

  const best = topRows[0];

  families.push({
    family: family.family,
    patternName: family.patternName,
    target: family.target,
    base: {
      score: family.best[0].score,
      candidate: base,
      summary: baseSummary,
    },
    refined: compact(best),
    improvement: {
      score: format(best.score - family.best[0].score),
      meanAbsoluteResidual: format(baseSummary.meanAbsoluteResidual - best.summary.meanAbsoluteResidual),
      maxAbsoluteResidual: format(baseSummary.maxAbsoluteResidual - best.summary.maxAbsoluteResidual),
    },
    iterations: familyIterations,
    accepted: familyAccepted,
    rejected: familyRejected,
    rejectionReasons: rejected,
    top: topRows.map(compact),
  });
}

const json = {
  source: 't1-coupling-sweep.json',
  status: 'local T1 refinement around best candidates; not proof and not a hidden material layer',
  offsets,
  refinedParameters,
  totalIterations,
  acceptedIterations,
  rejectedIterations,
  globalRejected,
  families,
};

await writeFile(new URL('t1-local-refinement.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate T1 Local Refinement

## Scope

This report performs a local refinement sweep around the best T1 candidate for each family from \`t1-coupling-sweep.json\`.

It does not prove the Relational Substrate theory and does not add a material layer between \`T0\` substrate and T1 vortons. Its purpose is to distinguish coarse-grid error from weakness in the target formula or guardrails.

Offsets tested around each best candidate: ${offsets.join(', ')}

Refined parameters: ${refinedParameters.join(', ')}

## Scale

Total local candidates tried: ${totalIterations}

Accepted after guardrails: ${acceptedIterations}

Rejected by guardrails: ${rejectedIterations}

## Family Improvements

| Family | Base score | Refined score | Score gain | Base mean abs residual | Refined mean abs residual | Residual improvement | Largest refined residual |
|---|---:|---:|---:|---:|---:|---:|---|
${families
  .map(
    (family) =>
      `| ${family.family} | ${family.base.score} | ${family.refined.score} | ${family.improvement.score} | ${family.base.summary.meanAbsoluteResidual} | ${family.refined.meanAbsoluteResidual} | ${family.improvement.meanAbsoluteResidual} | ${family.refined.largestResidual.parameter} (${family.refined.largestResidual.residual}) |`
  )
  .join('\n')}

## Refined Candidates

${families
  .map(
    (family) => `### ${family.family}

Candidate pattern: ${family.patternName}

| Parameter | Target | Base | Refined |
|---|---:|---:|---:|
${parameterNames
  .map((parameter) => `| ${parameter} | ${family.target[parameter]} | ${family.base.candidate[parameter]} | ${family.refined.candidate[parameter]} |`)
  .join('\n')}
`
  )
  .join('\n')}

## Interpretation

If refinement sharply improves residuals, the coarse global grid was the main limitation. If refinement barely moves a family, the current target formula or guardrails are more likely responsible.

The next step is to feed the refined candidates back into the stability report and decide whether the target formula needs adjustment or whether the current formula is stable enough for more molecule families.
`;

await writeFile(new URL('t1-local-refinement.md', outDir), markdown);

console.log(`Total local candidates tried: ${totalIterations}`);
console.log(`Accepted after guardrails: ${acceptedIterations}`);
console.log(`Rejected by guardrails: ${rejectedIterations}`);
console.log(`Wrote ${new URL('t1-local-refinement.md', outDir).pathname}`);
