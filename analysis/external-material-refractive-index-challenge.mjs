import { readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

async function readJson(name) {
  return JSON.parse(await readFile(new URL(name, outDir), 'utf8'));
}

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

const nbo = await readJson('material-nbo-stoichiometry.json');

const external = {
  target: 'measured refractive-index material-property challenge',
  modeledSubset:
    'source-anchored refractive-index targets for SiO2 fused silica and sodium silicate glass, checked against the current material grammar outputs',
  notModeled:
    'Sellmeier coefficient derivation, density prediction, molar refraction, glass relaxation, temperature dependence, wavelength-dependent dispersion beyond cited target values, molecular polarizability, or ab initio optical-property prediction',
  tolerances: {
    refractiveIndexAbsoluteErrorMax: 0.01,
  },
  measuredRows: [
    {
      formula: 'SiO2',
      material: 'fused silica',
      wavelengthNm: 632.8,
      measuredRefractiveIndex: 1.45704,
      source: 'KLA/Filmetrics refractive-index database citing Malitson JOSA 1965',
    },
    {
      formula: 'Na2SiO3',
      material: 'sodium silicate glass',
      wavelengthNm: null,
      measuredRefractiveIndex: 1.52,
      source: 'PubChem sodium silicate HSDB/Merck Index property record',
    },
  ],
  sources: [
    {
      label: 'KLA/Filmetrics, Refractive Index of SiO2 Fused Silica',
      url: 'https://www.kla.com/products/instruments/refractive-index-database/SiO2/Fused-Silica',
      note: 'Lists n = 1.45704 at 632.8 nm for SiO2 and cites I. H. Malitson, JOSA 1965.',
    },
    {
      label: 'PubChem Sodium Silicate, CID 23266',
      url: 'https://pubchem.ncbi.nlm.nih.gov/compound/23266',
      note: 'Lists index of refraction 1.520 for sodium silicate glass from HSDB/Merck Index.',
    },
  ],
};

const grammarVariables = {
  route: 'material network route is represented by topology continuity and NBO/T accounting only',
  closure: 'charge-balance closure accounts for Al compensation and excess modifier charge',
  phase: 'no optical phase-dispersion model is present for material refractive index',
  charge: 'modifier charge and aluminium charge balance are represented, but electronic polarizability is not',
  continuity: 'network continuity exists as a topology score, not as a calibrated optical-property equation',
};

const rows = external.measuredRows.map((target) => {
  const composition = nbo.rows.find((row) => row.formula === target.formula);
  return {
    ...target,
    nboT: composition?.nboT ?? null,
    chargeBalancedAl: composition?.chargeBalancedAl ?? null,
    predictedRefractiveIndex: null,
    absoluteError: null,
    pass: false,
  };
});

const checks = [
  {
    check: 'Source anchors present',
    expectation: 'measured refractive-index targets should have explicit external source anchors',
    modelValue: external.sources.map((source) => source.label).join('; '),
    pass: external.sources.length === 2,
    reading: 'The challenge uses concrete measured-property targets rather than qualitative material language.',
  },
  {
    check: 'Composition prerequisites present',
    expectation: 'material NBO/T accounting rows should exist for all refractive-index targets',
    modelValue: rows.map((row) => `${row.formula}: NBO/T ${row.nboT}`).join('; '),
    pass: rows.every((row) => row.nboT !== null),
    reading: 'The current grammar reaches the composition-accounting prerequisite for this property challenge.',
  },
  {
    check: 'Measured-property predictor exists',
    expectation: 'the grammar should provide a predeclared refractive-index prediction before comparison',
    modelValue: rows.map((row) => `${row.formula}: ${row.predictedRefractiveIndex ?? 'no prediction'}`).join('; '),
    pass: rows.every((row) => typeof row.predictedRefractiveIndex === 'number'),
    reading: 'This is the live gap: NBO/T accounting has not yet become a refractive-index predictor.',
  },
  {
    check: 'Refractive-index tolerance',
    expectation: `absolute index error should be <= ${external.tolerances.refractiveIndexAbsoluteErrorMax}`,
    modelValue: rows
      .map((row) => `${row.formula}: measured ${row.measuredRefractiveIndex}, predicted ${row.predictedRefractiveIndex ?? 'none'}`)
      .join('; '),
    pass: rows.every(
      (row) =>
        typeof row.predictedRefractiveIndex === 'number' &&
        Math.abs(row.predictedRefractiveIndex - row.measuredRefractiveIndex) <=
          external.tolerances.refractiveIndexAbsoluteErrorMax
    ),
    reading: 'The current sandbox cannot claim a calibrated material-property pass until this numeric comparison exists.',
  },
  {
    check: 'Boundary/non-claim discipline',
    expectation: 'benchmark should not claim optical-property derivation, density, dispersion, or polarizability modelling',
    modelValue: external.notModeled,
    pass:
      external.notModeled.includes('density') &&
      external.notModeled.includes('dispersion') &&
      external.notModeled.includes('polarizability'),
    reading: 'The challenge is a deliberately hard gate, not a hidden refractive-index model.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = `${passed}/${checks.length}`;
const status =
  passed === checks.length
    ? 'measured material refractive-index pass'
    : 'measured material refractive-index challenge unresolved';

const report = {
  source: 'external-material-refractive-index-challenge.mjs',
  status,
  external,
  grammarVariables,
  rows,
  score,
  checks,
  confidenceEffect:
    status === 'measured material refractive-index pass'
      ? 'would support a material-property confidence increase because NBO/T accounting transfers to measured refractive index without target fitting'
      : 'holds confidence flat and preserves the material-property gate because current composition accounting does not yet predict measured refractive index',
};

await writeFile(new URL('external-material-refractive-index-challenge.json', outDir), JSON.stringify(report, null, 2));

const markdown = `# Relational Substrate External Material Refractive-Index Challenge

## Scope

This report turns the material-property gate into an explicit measured refractive-index challenge.

It asks whether the current material grammar can move beyond NBO/T composition accounting and produce a predeclared refractive-index prediction for source-anchored SiO2 and Na2SiO3 targets. The current answer is no: the composition prerequisite exists, but no refractive-index predictor has been implemented.

## Result

| Measure | Value |
|---|---:|
| Status | ${status} |
| Score | ${score} |
| Confidence effect | ${report.confidenceEffect} |

## Checks

| Check | Expectation | Model value | Pass | Reading |
|---|---|---|---|---|
${checks
  .map(
    (check) =>
      `| ${check.check} | ${check.expectation} | ${check.modelValue} | ${check.pass ? 'yes' : 'no'} | ${check.reading} |`
  )
  .join('\n')}

## Measured Targets

| Formula | Material | Wavelength | Measured refractive index | NBO/T | Charge-balanced Al | Predicted refractive index | Pass |
|---|---|---:|---:|---:|---:|---:|---|
${rows
  .map(
    (row) =>
      `| ${row.formula} | ${row.material} | ${row.wavelengthNm ?? 'not specified'} | ${row.measuredRefractiveIndex} | ${row.nboT} | ${row.chargeBalancedAl} | ${row.predictedRefractiveIndex ?? 'none'} | ${row.pass ? 'yes' : 'no'} |`
  )
  .join('\n')}

## Source Anchors

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

This is an unresolved calibration challenge, not a failed source check. The material grammar has reached exact composition accounting, but it has not yet produced a measured refractive-index model. A future pass requires a predeclared optical-property equation or grammar-derived proxy before comparing against the measured targets.
`;

await writeFile(new URL('external-material-refractive-index-challenge.md', outDir), markdown);

console.log(`External material refractive-index challenge: ${status}`);
console.log(`Score: ${score}`);
console.log(`Wrote ${new URL('external-material-refractive-index-challenge.md', outDir).pathname}`);
