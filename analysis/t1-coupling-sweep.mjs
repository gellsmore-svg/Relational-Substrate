import { readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const descriptorUrl = new URL('t1-coupling-patterns.json', outDir);
const calibrationUrl = new URL('molecule-calibration-summary.json', outDir);

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

const parameterLevelSets = {
  closureIntegrity: [0.45, 0.6, 0.75, 0.9],
  routeCountFit: [0.45, 0.6, 0.75, 0.9],
  routeContinuity: [0.45, 0.6, 0.75, 0.9],
  tensionBalance: [0.45, 0.6, 0.75, 0.9],
  polarityResolution: [0.45, 0.6, 0.75, 0.9],
  angularConstraint: [0.45, 0.6, 0.75, 0.9],
  torsionTolerance: [0.45, 0.6, 0.75, 0.9],
  distributionCoherence: [0.45, 0.6, 0.75, 0.9],
  identityPreservation: [0.45, 0.6, 0.75, 0.9],
  leakageRisk: [0.05, 0.15, 0.3, 0.45, 0.6],
};

const descriptorPriors = {
  'diatomic covalent': {
    routeDemand: 0.92,
    polarityDemand: 0.42,
    angularDemand: 0.18,
    torsionDemand: 0.32,
    distributionDemand: 0.22,
  },
  'bent polar': {
    routeDemand: 0.74,
    polarityDemand: 0.86,
    angularDemand: 0.82,
    torsionDemand: 0.42,
    distributionDemand: 0.42,
  },
  'trigonal pyramidal covalent': {
    routeDemand: 0.8,
    polarityDemand: 0.86,
    angularDemand: 0.84,
    torsionDemand: 0.7,
    distributionDemand: 0.58,
  },
  'linear triatomic': {
    routeDemand: 0.82,
    polarityDemand: 0.68,
    angularDemand: 0.94,
    torsionDemand: 0.54,
    distributionDemand: 0.58,
  },
  'linear unsaturated covalent': {
    routeDemand: 0.9,
    polarityDemand: 0.42,
    angularDemand: 0.96,
    torsionDemand: 0.62,
    distributionDemand: 0.72,
  },
  'tetrahedral covalent': {
    routeDemand: 0.9,
    polarityDemand: 0.42,
    angularDemand: 0.88,
    torsionDemand: 0.62,
    distributionDemand: 0.82,
  },
  'rotatable covalent': {
    routeDemand: 0.82,
    polarityDemand: 0.55,
    angularDemand: 0.68,
    torsionDemand: 0.86,
    distributionDemand: 0.64,
  },
  'trigonal planar covalent': {
    routeDemand: 0.86,
    polarityDemand: 0.42,
    angularDemand: 0.9,
    torsionDemand: 0.86,
    distributionDemand: 0.72,
  },
  'asymmetric planar covalent': {
    routeDemand: 0.84,
    polarityDemand: 0.82,
    angularDemand: 0.88,
    torsionDemand: 0.86,
    distributionDemand: 0.7,
  },
  'aromatic ring': {
    routeDemand: 0.96,
    polarityDemand: 0.58,
    angularDemand: 0.86,
    torsionDemand: 0.92,
    distributionDemand: 0.98,
  },
  'ionic pair': {
    routeDemand: 0.68,
    polarityDemand: 0.98,
    angularDemand: 0.12,
    torsionDemand: 0.32,
    distributionDemand: 0.18,
  },
};

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

function percent(value) {
  return `${(value * 100).toFixed(2)}%`;
}

function clamp(value, minValue = 0.05, maxValue = 0.96) {
  return Math.max(minValue, Math.min(maxValue, value));
}

function targetValue(value) {
  return Number(clamp(value).toFixed(3));
}

function deriveTarget(family) {
  const prior = descriptorPriors[family.family];
  const dominant = family.dominantConstraints;
  const constraintIntensity = clamp(1 - family.averageNearRate / 0.08, 0, 1);
  const failureIntensity = clamp(family.averageFailureRate / 0.65, 0, 1);
  const polarityDominant = dominant.includes('polarity') ? 1 : 0;
  const bondDominant = dominant.includes('bond') ? 1 : 0;
  const angularFamily = Math.max(prior.angularDemand, dominant.includes('angle') ? 0.9 : 0);
  const distributionFamily = Math.max(prior.distributionDemand, dominant.includes('ring') ? 0.95 : 0);

  return {
    target: {
      closureIntegrity: targetValue(0.7 + constraintIntensity * 0.16 + failureIntensity * 0.08),
      routeCountFit: targetValue(0.52 + prior.routeDemand * 0.42),
      routeContinuity: targetValue(0.58 + constraintIntensity * 0.18 + prior.routeDemand * 0.16),
      tensionBalance: targetValue(0.56 + failureIntensity * 0.18 + bondDominant * 0.08 + prior.routeDemand * 0.08),
      polarityResolution: targetValue(0.42 + prior.polarityDemand * 0.34 + polarityDominant * 0.14 + failureIntensity * 0.06),
      angularConstraint: targetValue(0.36 + angularFamily * 0.4 + constraintIntensity * 0.14),
      torsionTolerance: targetValue(0.44 + prior.torsionDemand * 0.34 + constraintIntensity * 0.1),
      distributionCoherence: targetValue(0.38 + distributionFamily * 0.42 + constraintIntensity * 0.12),
      identityPreservation: targetValue(0.66 + constraintIntensity * 0.18 + failureIntensity * 0.08),
      leakageRisk: targetValue(0.26 - constraintIntensity * 0.12 - failureIntensity * 0.04, 0.05, 0.32),
    },
    derivation: {
      constraintIntensity: Number(constraintIntensity.toFixed(4)),
      failureIntensity: Number(failureIntensity.toFixed(4)),
      polarityDominant: Boolean(polarityDominant),
      bondDominant: Boolean(bondDominant),
      descriptorPrior: prior,
    },
  };
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

function candidateFromIndexes(indexes) {
  return Object.fromEntries(parameterNames.map((parameter, index) => [parameter, parameterLevelSets[parameter][indexes[index]]]));
}

function* indexTuples(index = 0, prefix = []) {
  if (index === parameterNames.length) {
    yield prefix;
    return;
  }

  const parameter = parameterNames[index];
  for (let levelIndex = 0; levelIndex < parameterLevelSets[parameter].length; levelIndex += 1) {
    yield* indexTuples(index + 1, [...prefix, levelIndex]);
  }
}

function compactCandidate(row) {
  return {
    score: Number(row.score.toFixed(4)),
    distance: Number((1 - row.score).toFixed(4)),
    candidate: row.candidate,
  };
}

const descriptors = JSON.parse(await readFile(descriptorUrl, 'utf8'));
const calibration = JSON.parse(await readFile(calibrationUrl, 'utf8'));

const families = [];
const globalRejected = {};
let totalIterations = 0;
let acceptedIterations = 0;
let rejectedIterations = 0;

for (const family of descriptors.families) {
  const calibrationFamily = calibration.families.find((item) => item.family === family.family);
  const { target, derivation } = deriveTarget(calibrationFamily);
  const rows = [];
  const rejected = {};
  let familyIterations = 0;
  let familyAccepted = 0;
  let familyRejected = 0;

  for (const indexes of indexTuples()) {
    const candidate = candidateFromIndexes(indexes);
    const reason = rejectReason(candidate);
    familyIterations += 1;
    totalIterations += 1;

    if (reason) {
      rejected[reason] = (rejected[reason] ?? 0) + 1;
      globalRejected[reason] = (globalRejected[reason] ?? 0) + 1;
      familyRejected += 1;
      rejectedIterations += 1;
      continue;
    }

    familyAccepted += 1;
    acceptedIterations += 1;
    rows.push({
      score: scoreCandidate(candidate, target),
      candidate,
    });
  }

  rows.sort((a, b) => b.score - a.score);
  const best = rows.slice(0, 12).map(compactCandidate);
  const worst = rows.slice(-12).reverse().map(compactCandidate);
  families.push({
    family: family.family,
    patternName: family.descriptor.patternName,
    target,
    targetDerivation: derivation,
    calibration: {
      cases: calibrationFamily.cases,
      averageNearRate: calibrationFamily.averageNearRate,
      averageFailureRate: calibrationFamily.averageFailureRate,
      dominantConstraints: calibrationFamily.dominantConstraints,
    },
    iterations: familyIterations,
    accepted: familyAccepted,
    rejected: familyRejected,
    rejectionReasons: rejected,
    best,
    worst,
  });
}

const json = {
  source: ['t1-coupling-patterns.json', 'molecule-calibration-summary.json'],
  status: 'candidate numeric T1 coupling sweep with T2-derived targets; not proof and not a hidden material layer',
  parameters: parameterNames,
  parameterLevelSets,
  totalIterations,
  acceptedIterations,
  rejectedIterations,
  globalRejected,
  families,
};

await writeFile(new URL('t1-coupling-sweep.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# AMS T1 Coupling Parameter Sweep

## Scope

This report turns the qualitative T1 coupling descriptors into bounded numeric parameter candidates.

It does not prove AMS and does not introduce a hidden material layer. The sweep tests whether a candidate coupling grammar can produce the right constraint shape for the already-calibrated T2 molecule families.

The target envelopes in this version are derived from T2 calibration metrics, with descriptor priors used only for broad family features that the T2 metrics do not directly contain, such as route count demand and distribution mode.

## Parameters

${parameterNames.map((parameter) => `- ${parameter}`).join('\n')}

Parameter levels tested:

${parameterNames.map((parameter) => `- ${parameter}: ${parameterLevelSets[parameter].join(', ')}`).join('\n')}

## Scale

Total T1 candidates tried: ${totalIterations}

Accepted after guardrails: ${acceptedIterations}

Rejected by guardrails: ${rejectedIterations}

## Global Rejection Reasons

| Reason | Count |
|---|---:|
${Object.entries(globalRejected)
  .sort((a, b) => b[1] - a[1])
  .map(([reason, count]) => `| ${reason} | ${count} |`)
  .join('\n')}

## Family Results

${families
  .map(
    (family) => `### ${family.family}

Candidate pattern: ${family.patternName}

T2 calibration: ${family.calibration.cases} cases, ${percent(family.calibration.averageNearRate)} average near-reference rate, ${percent(family.calibration.averageFailureRate)} average strong-failure rate.

Dominant T2 constraints: ${family.calibration.dominantConstraints}

| Iterations | Accepted | Rejected |
|---:|---:|---:|
| ${family.iterations} | ${family.accepted} | ${family.rejected} |

Target envelope:

| Parameter | Target |
|---|---:|
${Object.entries(family.target)
  .map(([parameter, value]) => `| ${parameter} | ${value} |`)
  .join('\n')}

Target derivation:

| Metric | Value |
|---|---:|
| constraintIntensity | ${family.targetDerivation.constraintIntensity} |
| failureIntensity | ${family.targetDerivation.failureIntensity} |
| polarityDominant | ${family.targetDerivation.polarityDominant ? 'yes' : 'no'} |
| bondDominant | ${family.targetDerivation.bondDominant ? 'yes' : 'no'} |

Top candidates:

| Rank | Score | Closure | Routes | Continuity | Tension | Polarity | Angle | Torsion | Distribution | Identity | Leakage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
${family.best
  .map(
    (row, index) =>
      `| ${index + 1} | ${row.score} | ${row.candidate.closureIntegrity} | ${row.candidate.routeCountFit} | ${row.candidate.routeContinuity} | ${row.candidate.tensionBalance} | ${row.candidate.polarityResolution} | ${row.candidate.angularConstraint} | ${row.candidate.torsionTolerance} | ${row.candidate.distributionCoherence} | ${row.candidate.identityPreservation} | ${row.candidate.leakageRisk} |`
  )
  .join('\n')}
`
  )
  .join('\n')}

## Interpretation

The first sweep is coarse. Its job is not to find final T1 geometries, but to expose the shape of the parameter space and make incoherent candidates rejectable.

The useful result is that each T2 family now has a bounded T1 target envelope and a ranked set of admissible candidates, while the target values are no longer hand-set per family. The next step is to test whether one shared target-derivation formula remains stable as more molecule families and reference cases are added.
`;

await writeFile(new URL('t1-coupling-sweep.md', outDir), markdown);

console.log(`Total T1 candidates tried: ${totalIterations}`);
console.log(`Accepted after guardrails: ${acceptedIterations}`);
console.log(`Rejected by guardrails: ${rejectedIterations}`);
console.log(`Wrote ${new URL('t1-coupling-sweep.md', outDir).pathname}`);
