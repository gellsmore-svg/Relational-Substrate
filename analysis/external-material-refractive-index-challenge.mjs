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
    {
      formula: 'NaAlSi3O8',
      material: 'albite feldspar',
      wavelengthNm: null,
      measuredRefractiveIndex: 1.53493,
      source: 'Mindat albite optical data mean of n-alpha/n-beta/n-gamma range midpoints',
      heldOut: true,
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
    {
      label: 'Mindat, Albite mineral information',
      url: 'https://www.mindat.org/min-96.html',
      note:
        'Lists albite optical RI ranges n-alpha 1.528-1.533, n-beta 1.5317-1.53685, and n-gamma 1.538-1.542; scalar target uses the mean of range midpoints.',
    },
  ],
};

const grammarVariables = {
  route: 'material network route is represented by topology continuity, NBO/T accounting, and a first-pass modifier-route index proxy',
  closure: 'charge-balance closure accounts for Al compensation and excess modifier charge',
  phase: 'optical phase is represented only by a scalar refractive-index proxy; no wavelength-dispersion curve is present',
  charge: 'modifier charge and aluminium charge balance are represented, but electronic polarizability is not',
  continuity: 'network continuity contributes through a silica baseline plus modifier depolymerization penalty/boost',
};

const predictor = {
  name: 'topology-only NBO/T refractive-index proxy',
  equation: 'n = silicaBaseline + nboTModifierSlope * NBO/T - chargeBalancedAlPenalty * chargeBalancedAl',
  silicaBaseline: 1.46,
  nboTModifierSlope: 0.02,
  chargeBalancedAlPenalty: 0.004,
  calibrationDiscipline:
    'coefficients are fixed before the measured-target comparison in this script; no target-specific endpoint solve is performed',
  limitations:
    'does not use density, molar refraction, electronic polarizability, Sellmeier dispersion, glass relaxation, temperature, or wavelength-dependent composition response',
};

function predictRefractiveIndex(composition) {
  if (!composition) return null;
  return round(
    predictor.silicaBaseline +
      predictor.nboTModifierSlope * composition.nboT -
      predictor.chargeBalancedAlPenalty * composition.chargeBalancedAl,
    5
  );
}

function slopeForTarget(row, baseline = predictor.silicaBaseline) {
  if (!row || row.nboT === 0) return null;
  return round((row.measuredRefractiveIndex - baseline + predictor.chargeBalancedAlPenalty * row.chargeBalancedAl) / row.nboT, 5);
}

const rows = external.measuredRows.map((target) => {
  const composition = nbo.rows.find((row) => row.formula === target.formula);
  const predictedRefractiveIndex = predictRefractiveIndex(composition);
  const absoluteError =
    typeof predictedRefractiveIndex === 'number'
      ? round(Math.abs(predictedRefractiveIndex - target.measuredRefractiveIndex), 5)
      : null;
  return {
    ...target,
    nboT: composition?.nboT ?? null,
    chargeBalancedAl: composition?.chargeBalancedAl ?? null,
    predictedRefractiveIndex,
    absoluteError,
    pass:
      typeof absoluteError === 'number' &&
      absoluteError <= external.tolerances.refractiveIndexAbsoluteErrorMax,
  };
});

const modifierRows = rows.filter((row) => row.nboT > 0);
const tolerance = external.tolerances.refractiveIndexAbsoluteErrorMax;
const slopeDiagnostics = modifierRows.map((row) => {
  const lowerSlope = round(
    (row.measuredRefractiveIndex -
      tolerance -
      predictor.silicaBaseline +
      predictor.chargeBalancedAlPenalty * row.chargeBalancedAl) /
      row.nboT,
    5
  );
  const upperSlope = round(
    (row.measuredRefractiveIndex +
      tolerance -
      predictor.silicaBaseline +
      predictor.chargeBalancedAlPenalty * row.chargeBalancedAl) /
      row.nboT,
    5
  );
  const targetImpliedSlope = slopeForTarget(row);
  return {
    formula: row.formula,
    targetImpliedSlope,
    toleranceSlopeWindow: [lowerSlope, upperSlope],
    currentSlope: predictor.nboTModifierSlope,
    currentSlopeWithinToleranceWindow:
      predictor.nboTModifierSlope >= lowerSlope && predictor.nboTModifierSlope <= upperSlope,
  };
});

const calibrationDiagnostic = {
  purpose: 'show the modifier slope required by measured targets without converting that target-implied value into a pass',
  currentSlope: predictor.nboTModifierSlope,
  slopeDiagnostics,
  endpointFitPolicy:
    'A slope changed after seeing these targets is treated as calibration debt unless it is validated on a new held-out composition.',
};

const frameworkRows = rows.filter((row) => row.nboT === 0);
const frameworkPairs = frameworkRows.flatMap((left, leftIndex) =>
  frameworkRows.slice(leftIndex + 1).map((right) => {
    const measuredSeparation = round(Math.abs(left.measuredRefractiveIndex - right.measuredRefractiveIndex), 5);
    const predictedSeparation = round(Math.abs(left.predictedRefractiveIndex - right.predictedRefractiveIndex), 5);
    return {
      formulas: [left.formula, right.formula],
      measuredSeparation,
      predictedSeparation,
      pass: Math.abs(measuredSeparation - predictedSeparation) <= tolerance,
    };
  })
);

const checks = [
  {
    check: 'Source anchors present',
    expectation: 'measured refractive-index targets should have explicit external source anchors',
    modelValue: external.sources.map((source) => source.label).join('; '),
    pass: external.sources.length === 3,
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
    modelValue: `${predictor.name}: ${rows
      .map((row) => `${row.formula}: ${row.predictedRefractiveIndex ?? 'no prediction'}`)
      .join('; ')}`,
    pass: rows.every((row) => typeof row.predictedRefractiveIndex === 'number'),
    reading: 'A first-pass topology-only predictor now exists, so the gate moves from missing predictor to measured tolerance.',
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
    reading: 'The current proxy must clear all measured targets before this becomes a calibrated material-property pass.',
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
  {
    check: 'Endpoint-fit guard',
    expectation: 'target-implied slope diagnostics should be reported without converting a two-target fit into an independent pass',
    modelValue: slopeDiagnostics
      .map(
        (row) =>
          `${row.formula}: implied slope ${row.targetImpliedSlope}; tolerance window ${row.toleranceSlopeWindow.join('..')}; current ${row.currentSlope}`
      )
      .join('; '),
    pass: slopeDiagnostics.every((row) => !row.currentSlopeWithinToleranceWindow),
    reading:
      'The diagnostic exposes the slope needed for tolerance while preserving the unresolved status until a new held-out composition validates any revised coefficient.',
  },
  {
    check: 'Held-out framework distinction',
    expectation: 'zero-NBO framework compositions with different measured RI should not collapse to nearly identical predictions',
    modelValue: frameworkPairs
      .map(
        (pair) =>
          `${pair.formulas.join(' vs ')}: measured separation ${pair.measuredSeparation}; predicted separation ${pair.predictedSeparation}`
      )
      .join('; '),
    pass: frameworkPairs.every((pair) => pair.pass),
    reading:
      'Albite exposes a structural limitation of the topology-only proxy: NBO/T alone cannot distinguish silica from a charge-balanced aluminosilicate framework.',
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
  predictor,
  calibrationDiagnostic,
  frameworkPairs,
  grammarVariables,
  rows,
  score,
  checks,
  confidenceEffect:
    status === 'measured material refractive-index pass'
      ? 'would support a material-property confidence increase because NBO/T accounting transfers to measured refractive index without target fitting'
      : 'holds confidence flat and preserves the material-property gate because the first-pass topology-only proxy does not yet satisfy measured refractive-index tolerance',
};

await writeFile(new URL('external-material-refractive-index-challenge.json', outDir), JSON.stringify(report, null, 2));

const markdown = `# Relational Substrate External Material Refractive-Index Challenge

## Scope

This report turns the material-property gate into an explicit measured refractive-index challenge.

It asks whether the current material grammar can move beyond NBO/T composition accounting and produce a predeclared refractive-index prediction for source-anchored SiO2, Na2SiO3, and held-out NaAlSi3O8 targets. The current answer is still no at pass level: a first-pass topology-only proxy exists, but it does not clear the measured tolerance and collapses distinct zero-NBO frameworks.

## Result

| Measure | Value |
|---|---:|
| Status | ${status} |
| Score | ${score} |
| Confidence effect | ${report.confidenceEffect} |

## Predictor

| Measure | Value |
|---|---|
| Name | ${predictor.name} |
| Equation | ${predictor.equation} |
| Coefficients | silicaBaseline ${predictor.silicaBaseline}; nboTModifierSlope ${predictor.nboTModifierSlope}; chargeBalancedAlPenalty ${predictor.chargeBalancedAlPenalty} |
| Calibration discipline | ${predictor.calibrationDiscipline} |
| Limitations | ${predictor.limitations} |

## Calibration Diagnostic

| Formula | Target-implied modifier slope | Tolerance slope window | Current slope | Current slope in window |
|---|---:|---:|---:|---|
${slopeDiagnostics
  .map(
    (row) =>
      `| ${row.formula} | ${row.targetImpliedSlope} | ${row.toleranceSlopeWindow.join(' to ')} | ${row.currentSlope} | ${row.currentSlopeWithinToleranceWindow ? 'yes' : 'no'} |`
  )
  .join('\n')}

Endpoint-fit policy: ${calibrationDiagnostic.endpointFitPolicy}

## Held-Out Framework Diagnostic

| Pair | Measured RI separation | Predicted RI separation | Pass |
|---|---:|---:|---|
${frameworkPairs
  .map(
    (pair) =>
      `| ${pair.formulas.join(' vs ')} | ${pair.measuredSeparation} | ${pair.predictedSeparation} | ${pair.pass ? 'yes' : 'no'} |`
  )
  .join('\n')}

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

| Formula | Material | Wavelength | Measured refractive index | NBO/T | Charge-balanced Al | Predicted refractive index | Absolute error | Pass |
|---|---|---:|---:|---:|---:|---:|---:|---|
${rows
  .map(
    (row) =>
      `| ${row.formula} | ${row.material} | ${row.wavelengthNm ?? 'not specified'} | ${row.measuredRefractiveIndex} | ${row.nboT} | ${row.chargeBalancedAl} | ${row.predictedRefractiveIndex ?? 'none'} | ${row.absoluteError ?? 'none'} | ${row.pass ? 'yes' : 'no'} |`
  )
  .join('\n')}

## Source Anchors

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

This is an unresolved calibration challenge, not a failed source check. The material grammar has reached exact composition accounting and now has a first-pass topology-only refractive-index proxy, but the proxy does not yet satisfy measured tolerance across all targets. The held-out albite row shows that NBO/T alone collapses silica and charge-balanced aluminosilicate frameworks that have different measured refractive indices. A future pass requires improving the predeclared optical-property equation or grammar-derived proxy before comparing against measured targets.
`;

await writeFile(new URL('external-material-refractive-index-challenge.md', outDir), markdown);

console.log(`External material refractive-index challenge: ${status}`);
console.log(`Score: ${score}`);
console.log(`Wrote ${new URL('external-material-refractive-index-challenge.md', outDir).pathname}`);
