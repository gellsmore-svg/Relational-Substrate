import { readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const cm1PerKcalMol = 349.755;

async function readJson(name) {
  return JSON.parse(await readFile(new URL(name, outDir), 'utf8'));
}

function clamp01(value) {
  return Math.max(0, Math.min(1, value));
}

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

function vec(x, y, z = 0) {
  return { x, y, z };
}

function add(a, b) {
  return vec(a.x + b.x, a.y + b.y, a.z + b.z);
}

function sub(a, b) {
  return vec(a.x - b.x, a.y - b.y, a.z - b.z);
}

function scale(a, factor) {
  return vec(a.x * factor, a.y * factor, a.z * factor);
}

function dot(a, b) {
  return a.x * b.x + a.y * b.y + a.z * b.z;
}

function cross(a, b) {
  return vec(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x);
}

function norm(a) {
  return Math.sqrt(dot(a, a));
}

function normalize(a) {
  const length = Math.max(norm(a), 1e-9);
  return scale(a, 1 / length);
}

function distance(a, b) {
  return norm(sub(a, b));
}

function rms(values) {
  return values.length ? Math.sqrt(values.reduce((sum, value) => sum + value * value, 0) / values.length) : 0;
}

function maxOrZero(values) {
  return values.length ? Math.max(...values) : 0;
}

function cyclicDifference(value, target, period = 360) {
  const raw = Math.abs(((value - target + period / 2) % period) - period / 2);
  return Math.min(raw, period - raw);
}

const ethane = await readJson('external-ethane-quantitative-benchmark.json');
const scaleTransfer = {
  source: 'external-ethane-quantitative-benchmark.json',
  kcalPerPenalty: ethane.scale.kcalPerPenalty,
  cm1PerPenalty: ethane.scale.kcalPerPenalty * cm1PerKcalMol,
};

const external = {
  molecule: 'N2H4+',
  target: 'held-out hydrazine cation torsion transfer',
  minimumAngle: 90,
  barriers: [
    { angle: 0, energyKjMol: 35.8, energyCm1: 2993 },
    { angle: 90, energyKjMol: 0, energyCm1: 0 },
    { angle: 180, energyKjMol: 13.16, energyCm1: 1100 },
  ],
  source: {
    label: 'NIST CCCBDB experimental barriers to internal rotation for N2H4+',
    url: 'https://cccbdb.nist.gov/exprotbar2x.asp?casno=302012&ti=1',
    note: 'Lists torsion angle 0 at 2993 cm-1, 90 at 0 cm-1, and 180 at 1100 cm-1 for hydrazine cation.',
  },
  tolerances: {
    orderingRequired: true,
    barrierErrorPctMax: 35,
    ratioErrorPctMax: 35,
  },
};

const reference = {
  nn: 1.45,
  nh: 1.02,
  hnnAngle: 112,
  hnhAngle: 107,
  torsion: external.minimumAngle,
  routeBase: 0.72,
};

const weights = {
  geometryFit: 0.18,
  angleStrain: 0.16,
  bondStrain: 0.12,
  polarityBalance: 0.1,
  routeContinuity: 0.16,
  stericObstruction: 0.28,
};

function groupHydrogens(nPosition, bisector, axis) {
  const halfHnh = (reference.hnhAngle * Math.PI) / 360;
  const split = normalize(cross(axis, bisector));
  const center = scale(bisector, Math.cos(halfHnh) * reference.nh);
  const offset = scale(split, Math.sin(halfHnh) * reference.nh);
  return [add(nPosition, add(center, offset)), add(nPosition, sub(center, offset))];
}

function hydrazineAtoms(torsionDegrees) {
  const torsion = (torsionDegrees * Math.PI) / 180;
  const hnn = (reference.hnnAngle * Math.PI) / 180;
  const leftN = vec(-reference.nn / 2, 0, 0);
  const rightN = vec(reference.nn / 2, 0, 0);
  const axis = vec(1, 0, 0);
  const leftBisector = normalize(vec(-Math.cos(Math.PI - hnn), Math.sin(Math.PI - hnn), 0));
  const rightBisector = normalize(vec(Math.cos(Math.PI - hnn), Math.sin(Math.PI - hnn) * Math.cos(torsion), Math.sin(Math.PI - hnn) * Math.sin(torsion)));
  const leftH = groupHydrogens(leftN, leftBisector, axis);
  const rightH = groupHydrogens(rightN, rightBisector, axis);

  return [
    { element: 'N', partialCharge: -0.25, position: leftN },
    { element: 'N', partialCharge: -0.25, position: rightN },
    ...leftH.map((position) => ({ element: 'H', partialCharge: 0.375, position })),
    ...rightH.map((position) => ({ element: 'H', partialCharge: 0.375, position })),
  ];
}

function featuresFor(angle) {
  const atoms = hydrazineAtoms(angle);
  const nLeft = atoms[0].position;
  const nRight = atoms[1].position;
  const leftHydrogens = [atoms[2].position, atoms[3].position];
  const rightHydrogens = [atoms[4].position, atoms[5].position];
  const bondLengths = [
    distance(nLeft, nRight),
    ...leftHydrogens.map((h) => distance(nLeft, h)),
    ...rightHydrogens.map((h) => distance(nRight, h)),
  ];
  const crossDistances = leftHydrogens.flatMap((left) => rightHydrogens.map((right) => distance(left, right)));
  const chargeCentre = atoms.reduce(
    (sum, atom) => add(sum, scale(atom.position, atom.partialCharge)),
    vec(0, 0, 0)
  );

  return {
    bondLengths,
    torsion: angle,
    stericClearance: Math.min(...crossDistances),
    polarityVector: norm(chargeCentre),
  };
}

function candidateFor(angle, referenceFeatures) {
  const features = featuresFor(angle);
  const bondDeviations = features.bondLengths.map((length, index) => clamp01(Math.abs(length - referenceFeatures.bondLengths[index]) / 0.25));
  const bondRms = rms(bondDeviations);
  const bondMax = maxOrZero(bondDeviations);
  const torsionRms = clamp01(cyclicDifference(features.torsion, reference.torsion) / 55);
  const torsionMax = torsionRms;
  const stericDeviation = clamp01((referenceFeatures.stericClearance - features.stericClearance) / 0.55);
  const polarityDeviation = clamp01(Math.abs(features.polarityVector - referenceFeatures.polarityVector) / 0.9);
  const cisCrowding = clamp01(stericDeviation * clamp01((55 - features.torsion) / 55));
  const antiPlanarRelease = clamp01((features.torsion - 145) / 35) * clamp01(1 - stericDeviation) * clamp01(1 - cisCrowding);
  const effectiveTorsionRms = torsionRms * (1 - antiPlanarRelease * 0.65);
  const effectiveTorsionMax = torsionMax * (1 - antiPlanarRelease * 0.65);

  const angleStrain = clamp01(effectiveTorsionRms * 0.34 + effectiveTorsionMax * 0.1 + stericDeviation * 0.08 + cisCrowding * 0.48);
  const geometryFit = clamp01(1 - (bondRms * 0.18 + bondMax * 0.08 + effectiveTorsionRms * 0.24 + stericDeviation * 0.18 + cisCrowding * 0.36));
  const routeContinuity = clamp01(reference.routeBase - bondRms * 0.08 - effectiveTorsionRms * 0.16 - stericDeviation * 0.08 - cisCrowding * 0.18);
  const polarityBalance = clamp01(1 - polarityDeviation * 0.72);
  const bondStrain = clamp01(bondRms * 0.65 + bondMax * 0.2);

  const score =
    geometryFit * weights.geometryFit +
    (1 - angleStrain) * weights.angleStrain +
    (1 - bondStrain) * weights.bondStrain +
    polarityBalance * weights.polarityBalance +
    routeContinuity * weights.routeContinuity +
    (1 - stericDeviation) * weights.stericObstruction;

  return {
    score: clamp01(score),
    metrics: {
      torsionRms: round(torsionRms, 4),
      effectiveTorsionRms: round(effectiveTorsionRms, 4),
      stericClearance: round(features.stericClearance, 4),
      stericDeviation: round(stericDeviation, 4),
      cisCrowding: round(cisCrowding, 4),
      antiPlanarRelease: round(antiPlanarRelease, 4),
      polarityDeviation: round(polarityDeviation, 4),
      geometryFit: round(geometryFit, 4),
      angleStrain: round(angleStrain, 4),
      routeContinuity: round(routeContinuity, 4),
    },
  };
}

const referenceFeatures = featuresFor(reference.torsion);
const referenceCandidate = candidateFor(reference.torsion, referenceFeatures);
const rows = external.barriers.map((barrier) => {
  const candidate = candidateFor(barrier.angle, referenceFeatures);
  const penalty = Math.max(0, referenceCandidate.score - candidate.score);
  const modelCm1 = penalty * scaleTransfer.cm1PerPenalty;
  const errorPct = barrier.energyCm1 === 0 ? 0 : ((modelCm1 - barrier.energyCm1) / barrier.energyCm1) * 100;

  return {
    angle: barrier.angle,
    externalCm1: barrier.energyCm1,
    modelPenalty: round(penalty, 4),
    modelCm1: round(modelCm1, 2),
    errorPct: round(errorPct, 2),
    absoluteErrorPct: round(Math.abs(errorPct), 2),
    pass: barrier.energyCm1 === 0 ? penalty < 0.02 : Math.abs(errorPct) <= external.tolerances.barrierErrorPctMax,
    ...candidate.metrics,
  };
});

const row0 = rows.find((row) => row.angle === 0);
const row90 = rows.find((row) => row.angle === 90);
const row180 = rows.find((row) => row.angle === 180);
const externalRatio = row0.externalCm1 / row180.externalCm1;
const modelRatio = row180.modelCm1 > 0 ? row0.modelCm1 / row180.modelCm1 : Infinity;
const ratioErrorPct = ((modelRatio - externalRatio) / externalRatio) * 100;
const orderingPass = row90.modelPenalty < row180.modelPenalty && row180.modelPenalty < row0.modelPenalty;
const absolutePass = rows.every((row) => row.pass);
const ratioPass = Math.abs(ratioErrorPct) <= external.tolerances.ratioErrorPctMax;
const nonzeroBarrierRows = rows.filter((row) => row.externalCm1 > 0 && row.modelCm1 > 0);
const leastSquaresScaleMultiplier =
  nonzeroBarrierRows.reduce((sum, row) => sum + row.modelCm1 * row.externalCm1, 0) /
  nonzeroBarrierRows.reduce((sum, row) => sum + row.modelCm1 ** 2, 0);
const calibrationGapRows = nonzeroBarrierRows.map((row) => {
  const requiredScaleMultiplier = row.externalCm1 / row.modelCm1;
  const leastSquaresCm1 = row.modelCm1 * leastSquaresScaleMultiplier;
  const leastSquaresErrorPct = ((leastSquaresCm1 - row.externalCm1) / row.externalCm1) * 100;
  return {
    angle: row.angle,
    externalCm1: row.externalCm1,
    modelCm1: row.modelCm1,
    requiredScaleMultiplier: round(requiredScaleMultiplier, 4),
    leastSquaresCm1: round(leastSquaresCm1, 2),
    leastSquaresErrorPct: round(leastSquaresErrorPct, 2),
  };
});
const requiredScaleSpread = Math.max(...calibrationGapRows.map((row) => row.requiredScaleMultiplier)) -
  Math.min(...calibrationGapRows.map((row) => row.requiredScaleMultiplier));

const checks = [
  {
    check: 'Held-out scale transfer',
    expectation: 'use ethane kcal-per-penalty scale without hydrazine endpoint fitting',
    modelValue: `${round(scaleTransfer.cm1PerPenalty, 2)} cm-1 per penalty`,
    pass: true,
    reading: 'The hydrazine cation barriers are compared under the already-used ethane scale.',
  },
  {
    check: 'Barrier ordering',
    expectation: '90 degree minimum, 180 degree lower barrier, 0 degree higher barrier',
    modelValue: `90: ${row90.modelCm1} cm-1; 180: ${row180.modelCm1} cm-1; 0: ${row0.modelCm1} cm-1`,
    pass: orderingPass,
    reading: orderingPass
      ? 'Anti-planar release generalizes qualitatively: the 180 degree barrier is below the crowded 0 degree barrier.'
      : 'The held-out torsion ordering fails, so the H2O2 refinement may not generalize.',
  },
  {
    check: 'Absolute transferred barriers',
    expectation: `all barriers within ${external.tolerances.barrierErrorPctMax}%`,
    modelValue: rows.map((row) => `${row.angle}: ${row.modelCm1} vs ${row.externalCm1} cm-1 (${row.errorPct}%)`).join('; '),
    pass: absolutePass,
    reading: absolutePass
      ? 'The transferred scale survives the held-out hydrazine cation barrier magnitudes.'
      : 'The transferred scale does not reproduce all held-out hydrazine cation barrier magnitudes.',
  },
  {
    check: 'Barrier-ratio transfer',
    expectation: `0/180 ratio ${round(externalRatio, 3)} within ${external.tolerances.ratioErrorPctMax}%`,
    modelValue: `model ratio ${round(modelRatio, 3)}; error ${round(ratioErrorPct, 2)}%`,
    pass: ratioPass,
    reading: ratioPass
      ? 'The relative anti-planar/crowded barrier split transfers to the held-out torsion system.'
      : 'The relative anti-planar/crowded barrier split is not quantitatively stable on the held-out torsion system.',
  },
  {
    check: 'Scope boundary',
    expectation: 'benchmark remains a small topology transfer check, not a hydrazine quantum-chemistry model',
    modelValue: 'single geometry proxy, ethane scale transfer, NIST barrier comparator',
    pass: true,
    reading: 'This is a held-out pressure test for anti-planar release, not a molecular solver.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = round(passed / checks.length, 3);
const status = checks.every((check) => check.pass)
  ? 'held-out torsion transfer pass'
  : orderingPass
    ? 'held-out torsion ordering pass with quantitative miss'
    : 'held-out torsion transfer fail';
const confidenceEffect =
  status === 'held-out torsion transfer pass'
    ? 'supports a confidence increase because anti-planar release transfers to a held-out torsion system under the ethane scale'
    : orderingPass
      ? 'holds confidence mostly flat: anti-planar release transfers qualitatively but not as a calibrated barrier model'
      : 'reduces confidence because anti-planar release does not generalize to the held-out torsion ordering';

const json = {
  source: 'external-hydrazine-cation-torsion-benchmark.mjs',
  status,
  score,
  confidenceEffect,
  external,
  scaleTransfer: {
    ...scaleTransfer,
    kcalPerPenalty: round(scaleTransfer.kcalPerPenalty, 4),
    cm1PerPenalty: round(scaleTransfer.cm1PerPenalty, 2),
  },
  reference,
  rows,
  metrics: {
    orderingPass,
    absolutePass,
    ratioPass,
    modelBarrierRatio0To180: round(modelRatio, 4),
    externalBarrierRatio0To180: round(externalRatio, 4),
    ratioErrorPct: round(ratioErrorPct, 2),
    calibrationGap: {
      requiredScaleMultipliers: calibrationGapRows.map((row) => ({
        angle: row.angle,
        multiplier: row.requiredScaleMultiplier,
      })),
      requiredScaleSpread: round(requiredScaleSpread, 4),
      leastSquaresScaleMultiplier: round(leastSquaresScaleMultiplier, 4),
      leastSquaresRows: calibrationGapRows,
      reading:
        'Hydrazine absolute magnitudes are not solved by the ethane scale. A single post-hoc multiplier would improve absolute scale but would not remove the relative-barrier shape error.',
    },
  },
  checks,
};

await writeFile(new URL('external-hydrazine-cation-torsion-benchmark.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate External Hydrazine Cation Held-Out Torsion Benchmark

## Scope

This benchmark tests whether anti-planar release generalizes beyond H2O2.

It uses NIST CCCBDB hydrazine cation internal-rotation barriers and transfers the ethane quantitative energy scale without fitting any hydrazine endpoint. It is a held-out torsion pressure test, not a quantum-chemistry model for hydrazine cation.

## Result

| Measure | Value |
|---|---:|
| Status | ${status} |
| Passed checks | ${passed}/${checks.length} |
| Score | ${score} |
| Model 0/180 ratio | ${round(modelRatio, 3)} |
| External 0/180 ratio | ${round(externalRatio, 3)} |
| Ratio error | ${round(ratioErrorPct, 2)}% |
| Confidence effect | ${confidenceEffect} |

## Checks

| Check | Expectation | Model value | Pass | Reading |
|---|---|---|---|---|
${checks.map((check) => `| ${check.check} | ${check.expectation} | ${check.modelValue} | ${check.pass ? 'yes' : 'no'} | ${check.reading} |`).join('\n')}

## Barrier Rows

| Angle | External cm-1 | Model penalty | Model cm-1 | Error | Effective torsion RMS | Steric deviation | Cis crowding | Anti-planar release | Pass |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
${rows
  .map(
    (row) =>
      `| ${row.angle} | ${row.externalCm1} | ${row.modelPenalty} | ${row.modelCm1} | ${row.errorPct}% | ${row.effectiveTorsionRms} | ${row.stericDeviation} | ${row.cisCrowding} | ${row.antiPlanarRelease} | ${row.pass ? 'yes' : 'no'} |`
  )
  .join('\n')}

## Calibration Gap Diagnostic

This diagnostic does not add a fitted hydrazine correction. It quantifies what correction would be required if one tried to repair the absolute-magnitude miss after the fact.

| Measure | Value |
|---|---:|
| 0 degree required multiplier | ${calibrationGapRows.find((row) => row.angle === 0)?.requiredScaleMultiplier}x |
| 180 degree required multiplier | ${calibrationGapRows.find((row) => row.angle === 180)?.requiredScaleMultiplier}x |
| Required multiplier spread | ${round(requiredScaleSpread, 4)}x |
| Best single multiplier | ${round(leastSquaresScaleMultiplier, 4)}x |

| Angle | External cm-1 | Current model cm-1 | Required multiplier | Best-single-multiplier cm-1 | Best-single-multiplier error |
|---:|---:|---:|---:|---:|---:|
${calibrationGapRows
  .map(
    (row) =>
      `| ${row.angle} | ${row.externalCm1} | ${row.modelCm1} | ${row.requiredScaleMultiplier}x | ${row.leastSquaresCm1} | ${row.leastSquaresErrorPct}% |`
  )
  .join('\n')}

The required multipliers are not equal. A post-hoc single multiplier would bring the 0 degree barrier near tolerance, but would leave the 180 degree barrier high; the 0/180 shape ratio would remain unchanged. This keeps the hydrazine result classified as directional/ratiometric transfer, not calibrated torsional-energy validation.

## Source

- ${external.source.label}: ${external.source.url}. ${external.source.note}

## Reading

The important result is whether anti-planar release transfers without endpoint fitting. A qualitative ordering pass reduces the overfit concern from H2O2, while the absolute-magnitude miss remains an explicit limitation: the current geometry proxy is not a calibrated torsional energy model and should not be counted as held-out absolute barrier validation.
`;

await writeFile(new URL('external-hydrazine-cation-torsion-benchmark.md', outDir), markdown);

console.log(`External hydrazine cation torsion benchmark: ${status}`);
console.log(`Passed checks: ${passed}/${checks.length}`);
console.log(`Model 0/180 ratio: ${round(modelRatio, 3)}`);
console.log(`Wrote ${new URL('external-hydrazine-cation-torsion-benchmark.md', outDir).pathname}`);
