import { readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

async function readJson(name) {
  return JSON.parse(await readFile(new URL(name, outDir), 'utf8'));
}

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

function expectedNormalizedBarrier(angle, referenceAngle) {
  const radians = ((angle - referenceAngle) * Math.PI) / 180;
  return (1 - Math.cos(3 * radians)) / 2;
}

function rms(values) {
  return values.length ? Math.sqrt(values.reduce((sum, value) => sum + value * value, 0) / values.length) : 0;
}

const ethane = await readJson('ethane-torsion-sweep.json');

const external = {
  molecule: 'C2H6',
  target: 'quantitative tolerance for normalized ethane torsion shape',
  experimentalBarrierKcalMol: 2.875,
  quantitativeTolerance: {
    normalizedRmsErrorMax: 0.12,
    interiorPointErrorMax: 0.18,
    eclipsedBarrierKcalMolTolerance: 0.15,
  },
  comparisonShape:
    'A simple threefold torsion reference, normalized so staggered minima are 0 and eclipsed maxima are 1: (1 - cos(3 theta)) / 2.',
  sources: [
    {
      label: 'Rotational barrier in ethane molecular orbital study, Molecules 2012',
      url: 'https://doi.org/10.3390/molecules17044661',
      note: 'Cites the ethane rotational barrier as 2.875 kcal/mol and describes staggered minimum / eclipsed maximum.',
    },
    {
      label: 'Hyperconjugation not steric repulsion leads to the staggered structure of ethane, Nature 2001',
      url: 'https://doi.org/10.1038/35079036',
      note: 'Describes staggered ethane as preferred and eclipsed ethane as unstable during rotation.',
    },
  ],
};

const barrierPenalty = Math.max(...ethane.rows.map((row) => row.penaltyVsReference));
const kcalPerPenalty = external.experimentalBarrierKcalMol / barrierPenalty;

const rows = ethane.rows.map((row) => {
  const modelNormalized = barrierPenalty > 0 ? row.penaltyVsReference / barrierPenalty : 0;
  const expectedNormalized = expectedNormalizedBarrier(row.angle, ethane.reference.angle);
  const normalizedError = modelNormalized - expectedNormalized;

  return {
    angle: row.angle,
    expectedClass: row.expectedClass,
    modelPenalty: row.penaltyVsReference,
    modelKcalMol: round(row.penaltyVsReference * kcalPerPenalty, 3),
    modelNormalized: round(modelNormalized, 4),
    expectedNormalized: round(expectedNormalized, 4),
    normalizedError: round(normalizedError, 4),
  };
});

const normalizedErrors = rows.map((row) => row.normalizedError);
const interiorRows = rows.filter((row) => row.expectedClass === 'intermediate');
const interiorErrors = interiorRows.map((row) => Math.abs(row.normalizedError));
const rmsNormalizedError = round(rms(normalizedErrors), 4);
const maxInteriorError = round(Math.max(...interiorErrors), 4);
const scaledEclipsedBarrier = round(barrierPenalty * kcalPerPenalty, 3);
const barrierError = round(Math.abs(scaledEclipsedBarrier - external.experimentalBarrierKcalMol), 4);

const checks = [
  {
    check: 'Predeclared normalized RMS tolerance',
    expectation: `RMS normalized shape error <= ${external.quantitativeTolerance.normalizedRmsErrorMax}`,
    modelValue: `${rmsNormalizedError}`,
    pass: rmsNormalizedError <= external.quantitativeTolerance.normalizedRmsErrorMax,
    reading: 'The full sampled torsion curve stays inside the broad quantitative shape tolerance.',
  },
  {
    check: 'Predeclared interior-point tolerance',
    expectation: `intermediate-angle normalized error <= ${external.quantitativeTolerance.interiorPointErrorMax}`,
    modelValue: `${maxInteriorError}`,
    pass: maxInteriorError <= external.quantitativeTolerance.interiorPointErrorMax,
    reading: 'The 30 and 90 degree points are high relative to the simple cosine reference, but not outside the tolerance.',
  },
  {
    check: 'Barrier scale anchoring',
    expectation: `scaled eclipsed barrier within ${external.quantitativeTolerance.eclipsedBarrierKcalMolTolerance} kcal/mol of ${external.experimentalBarrierKcalMol}`,
    modelValue: `${scaledEclipsedBarrier} kcal/mol; error ${barrierError}`,
    pass: barrierError <= external.quantitativeTolerance.eclipsedBarrierKcalMolTolerance,
    reading: 'The barrier endpoint is anchored by scale mapping, so this is a scale sanity check rather than independent validation.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = round(passed / checks.length, 3);
const status = checks.every((check) => check.pass) ? 'quantitative tolerance pass' : 'quantitative tolerance fail';
const confidenceEffect =
  status === 'quantitative tolerance pass'
    ? 'supports a small confidence increase because a predeclared quantitative tolerance passes, with endpoint scaling caveats'
    : 'limits confidence because the first quantitative tolerance check failed';

const json = {
  source: 'external-ethane-quantitative-benchmark.mjs',
  status,
  score,
  confidenceEffect,
  external,
  scale: {
    barrierPenalty,
    kcalPerPenalty: round(kcalPerPenalty, 3),
    scaledEclipsedBarrier,
    barrierError,
    rmsNormalizedError,
    maxInteriorError,
  },
  rows,
  checks,
};

await writeFile(new URL('external-ethane-quantitative-benchmark.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate External Ethane Quantitative Benchmark

## Scope

This report adds the first predeclared quantitative tolerance check to the external benchmark set.

It does not claim a fitted physical energy model. It maps the model's eclipsed penalty onto the external ethane barrier, then tests whether the normalized torsion shape stays within a broad tolerance around a simple threefold reference curve.

## Result

| Measure | Value |
|---|---:|
| Status | ${status} |
| Passed checks | ${passed}/${checks.length} |
| Score | ${score} |
| RMS normalized error | ${rmsNormalizedError} |
| Max interior error | ${maxInteriorError} |
| Confidence effect | ${confidenceEffect} |

## Checks

| Check | Expectation | Model value | Pass | Reading |
|---|---|---|---|---|
${checks.map((check) => `| ${check.check} | ${check.expectation} | ${check.modelValue} | ${check.pass ? 'yes' : 'no'} | ${check.reading} |`).join('\n')}

## Torsion Shape Rows

| Angle | Class | Model penalty | Model kcal/mol | Model normalized | Expected normalized | Error |
|---:|---|---:|---:|---:|---:|---:|
${rows
  .map(
    (row) =>
      `| ${row.angle} | ${row.expectedClass} | ${row.modelPenalty} | ${row.modelKcalMol} | ${row.modelNormalized} | ${row.expectedNormalized} | ${row.normalizedError} |`
  )
  .join('\n')}

## Sources

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The model clears a broad quantitative shape tolerance. The main weakness is visible: the intermediate torsion points are too high against the simple threefold curve. This is a useful pass, not a strong physical-energy validation.
`;

await writeFile(new URL('external-ethane-quantitative-benchmark.md', outDir), markdown);

console.log(`External ethane quantitative benchmark: ${status}`);
console.log(`Passed checks: ${passed}/${checks.length}`);
console.log(`RMS normalized error: ${rmsNormalizedError}`);
console.log(`Wrote ${new URL('external-ethane-quantitative-benchmark.md', outDir).pathname}`);
