import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const sourceLock = JSON.parse(
  await readFile(
    new URL('peroxide-peroxyformic-source-lock-screen.json', outDir),
    'utf8',
  ),
);

function clamp01(value) {
  return Math.max(0, Math.min(1, value));
}

function cyclicDifference(value, target, period = 360) {
  return Math.abs(((value - target + period / 2) % period) - period / 2);
}

function selectionDistance(candidate, reference) {
  return clamp01(cyclicDifference(candidate, reference) / 45);
}

function energyPenalty(alpha, equilibrium) {
  const torsionDeviation = clamp01(cyclicDifference(alpha, equilibrium) / 45);
  const cisCrowding = clamp01((60 - alpha) / 60);
  const antiPlanarRelease =
    clamp01((alpha - 145) / 35) * clamp01(1 - cisCrowding);
  const effectiveTorsionDeviation =
    torsionDeviation * (1 - antiPlanarRelease * 0.65);
  return clamp01(effectiveTorsionDeviation * 0.42 + cisCrowding * 0.58);
}

function ranks(values) {
  return values.map(
    (value) =>
      1 +
      values.filter((candidate) => candidate < value).length +
      (values.filter((candidate) => candidate === value).length - 1) / 2,
  );
}

function pearson(left, right) {
  const leftMean = left.reduce((sum, value) => sum + value, 0) / left.length;
  const rightMean = right.reduce((sum, value) => sum + value, 0) / right.length;
  const numerator = left.reduce(
    (sum, value, index) =>
      sum + (value - leftMean) * (right[index] - rightMean),
    0,
  );
  const leftScale = Math.sqrt(
    left.reduce((sum, value) => sum + (value - leftMean) ** 2, 0),
  );
  const rightScale = Math.sqrt(
    right.reduce((sum, value) => sum + (value - rightMean) ** 2, 0),
  );
  return numerator / (leftScale * rightScale);
}

const coordinates = sourceLock.lockedConstruct.coordinates;
const equilibrium = coordinates.find((row) => row.role === 'equilibrium');
const rows = coordinates.map((row) => ({
  ...row,
  selectionDistance: selectionDistance(
    row.torsionDegrees,
    equilibrium.torsionDegrees,
  ),
  predictedPenalty: energyPenalty(
    row.torsionDegrees,
    equilibrium.torsionDegrees,
  ),
}));

const sourceRises = rows.map(
  (row) => row.relativeEnergyEv - equilibrium.relativeEnergyEv,
);
const predictedEquilibrium = rows.find(
  (row) => row.role === 'equilibrium',
).predictedPenalty;
const predictedRises = rows.map(
  (row) => row.predictedPenalty - predictedEquilibrium,
);
const sourceMax = Math.max(...sourceRises);
const predictedMax = Math.max(...predictedRises);
const normalizationValid = sourceMax > 0 && predictedMax > 0;
const normalizedSource = sourceRises.map((value) => value / sourceMax);
const normalizedPredicted = normalizationValid
  ? predictedRises.map((value) => value / predictedMax)
  : null;
const mae = normalizedPredicted
  ? normalizedSource.reduce(
      (sum, value, index) =>
        sum + Math.abs(value - normalizedPredicted[index]),
      0,
    ) / normalizedSource.length
  : null;
const spearman = pearson(ranks(sourceRises), ranks(predictedRises));
const intermediate = rows.find((row) => row.role === 'intermediate');
const sourceOrdering = [...rows]
  .sort((left, right) => left.relativeEnergyEv - right.relativeEnergyEv)
  .map((row) => row.role);
const predictedOrdering = [...rows]
  .sort((left, right) => left.predictedPenalty - right.predictedPenalty)
  .map((row) => row.role);
const orderingMatches =
  JSON.stringify(sourceOrdering) === JSON.stringify(predictedOrdering);

const checks = [
  {
    check: 'intermediate selection distance is unsaturated',
    pass:
      intermediate.selectionDistance > 0 &&
      intermediate.selectionDistance < 1,
    value: intermediate.selectionDistance.toFixed(4),
  },
  {
    check: 'source and predicted energy ordering agree',
    pass: orderingMatches,
    value: `${sourceOrdering.join(' < ')} versus ${predictedOrdering.join(' < ')}`,
  },
  {
    check: 'Spearman rank correlation is at least 0.8',
    pass: spearman >= 0.8,
    value: spearman.toFixed(4),
  },
  {
    check: 'normalized energy-rise MAE is at most 0.20',
    pass: normalizationValid && mae <= 0.2,
    value: normalizationValid ? mae.toFixed(4) : 'undefined: predicted maximum rise is not positive',
  },
];

const passed = checks.every((check) => check.pass);
const report = {
  source: 'peroxide-peroxyformic-profile-scoring.mjs',
  date: '2026-06-24',
  status: passed
    ? 'heldout-intermediate-profile-pass'
    : 'heldout-intermediate-profile-fail',
  predeclarationHash: sourceLock.sourceLockDecision.predeclarationHash,
  sourceReference: sourceLock.sourceReference,
  frozenParameters: {
    selectionToleranceDegrees: 45,
    releaseStrength: 0.65,
    releaseOnsetDegrees: 145,
    releaseSpanDegrees: 35,
  },
  rows: rows.map((row, index) => ({
    ...row,
    sourceNormalizedRise: normalizedSource[index],
    predictedRise: predictedRises[index],
    predictedNormalizedRise: normalizedPredicted?.[index] ?? null,
  })),
  metrics: {
    sourceOrdering,
    predictedOrdering,
    orderingMatches,
    spearman,
    normalizationValid,
    normalizedMae: mae,
  },
  checks,
  diagnosis:
    'the absolute-angle cis-crowding term assigns the source equilibrium at 0 degrees the largest penalty and predicts decreasing penalty toward 90 degrees, reversing the held-out ground-state energy profile',
  decision:
    'block promotion of the current observable-route plus released-energy model form; redesign cis-crowding so source-defined equilibrium topology is not penalized solely because its absolute torsion is near 0 degrees',
  confidenceAction:
    'no global confidence increase; record a held-out model-form failure',
};

const markdown = `# Peroxyformic-Acid Intermediate-Profile Scoring

Status: **${report.status}**

| Role | Torsion | Source energy | Selection distance | Predicted penalty | Predicted rise |
|---|---:|---:|---:|---:|---:|
${report.rows
  .map(
    (row) =>
      `| ${row.role} | ${row.torsionDegrees} degrees | ${row.relativeEnergyEv} eV | ${row.selectionDistance.toFixed(4)} | ${row.predictedPenalty.toFixed(4)} | ${row.predictedRise.toFixed(4)} |`,
  )
  .join('\n')}

## Frozen Checks

| Check | Value | Result |
|---|---|---|
${checks
  .map(
    (row) =>
      `| ${row.check} | ${row.value} | ${row.pass ? 'pass' : 'fail'} |`,
  )
  .join('\n')}

Diagnosis: ${report.diagnosis}.

Decision: ${report.decision}.

Confidence action: ${report.confidenceAction}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-peroxyformic-profile-scoring.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('peroxide-peroxyformic-profile-scoring.md', outDir),
  markdown,
);

console.log(`Peroxyformic profile scoring: ${report.status}`);
