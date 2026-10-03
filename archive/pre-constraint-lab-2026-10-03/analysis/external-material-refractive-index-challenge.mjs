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
    'source-anchored refractive-index targets for SiO2 fused silica, sodium silicate glass, held-out albite feldspar, fresh-validation anorthite feldspar, and second-generation held-out orthoclase feldspar, checked against the current material grammar outputs',
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
    {
      formula: 'CaAl2Si2O8',
      material: 'anorthite feldspar',
      wavelengthNm: null,
      measuredRefractiveIndex: 1.58167,
      source: 'Mindat anorthite optical data mean of n-alpha/n-beta/n-gamma range midpoints',
      freshCandidateValidation: true,
    },
    {
      formula: 'KAlSi3O8',
      material: 'orthoclase feldspar',
      wavelengthNm: null,
      measuredRefractiveIndex: 1.52183,
      source: 'Mindat orthoclase optical data mean of n-alpha/n-beta/n-gamma range midpoints',
      secondGenerationValidation: true,
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
    {
      label: 'Mindat, Anorthite mineral information',
      url: 'https://www.mindat.org/min-246.html',
      note:
        'Lists anorthite optical RI ranges n-alpha 1.573-1.577, n-beta 1.58-1.585, and n-gamma 1.585-1.59; scalar target uses the mean of range midpoints.',
    },
    {
      label: 'Mindat, Orthoclase mineral information',
      url: 'https://www.mindat.org/min-3026.html',
      note:
        'Lists orthoclase optical RI ranges n-alpha 1.518-1.520, n-beta 1.522-1.524, and n-gamma 1.522-1.525; scalar target uses the mean of range midpoints.',
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

const quarantinedCandidate = {
  name: 'calibration-debt aluminosilicate framework candidate',
  equation: 'n = silicaBaseline + candidateNboTSlope * NBO/T + frameworkAlBoost * chargeBalancedAl',
  silicaBaseline: 1.46,
  candidateNboTSlope: 0.03,
  frameworkAlBoost: 0.075,
  status: 'quarantined calibration candidate; fresh validation failed; not counted as a benchmark pass',
  reason:
    'The NBO/T slope and framework-Al boost are target-implied by the current Na2SiO3 and NaAlSi3O8 rows after the miss was observed.',
  releaseCondition:
    'Do not promote in this form: CaAl2Si2O8 fresh validation misses tolerance without changing coefficients.',
};

const secondGenerationCandidate = {
  name: 'second-generation modifier-identity candidate',
  equation:
    'n = silicaBaseline + candidateNboTSlope * NBO/T + frameworkAlBoost * chargeBalancedAl - divalentModifierPenalty * divalentModifierCharge',
  silicaBaseline: 1.46,
  candidateNboTSlope: 0.03,
  frameworkAlBoost: 0.075,
  divalentModifierPenalty: 0.014,
  status:
    'quarantined second-generation candidate; target-informed after anorthite failure; not counted as a benchmark pass',
  reason:
    'The divalent modifier term is introduced only after observing that the first repair overpredicts CaAl2Si2O8, so current-row agreement is calibration debt.',
  releaseCondition:
    'Do not promote in this form: KAlSi3O8 second-generation held-out validation misses tolerance without changing coefficients.',
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

function predictQuarantinedCandidate(composition) {
  if (!composition) return null;
  return round(
    quarantinedCandidate.silicaBaseline +
      quarantinedCandidate.candidateNboTSlope * composition.nboT +
      quarantinedCandidate.frameworkAlBoost * composition.chargeBalancedAl,
    5
  );
}

function predictSecondGenerationCandidate(composition) {
  if (!composition) return null;
  return round(
    secondGenerationCandidate.silicaBaseline +
      secondGenerationCandidate.candidateNboTSlope * composition.nboT +
      secondGenerationCandidate.frameworkAlBoost * composition.chargeBalancedAl -
      secondGenerationCandidate.divalentModifierPenalty * (composition.divalentModifierCharge ?? 0),
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

const candidateRows = rows.map((row) => {
  const composition = nbo.rows.find((compositionRow) => compositionRow.formula === row.formula);
  const candidatePrediction = predictQuarantinedCandidate(composition);
  const candidateAbsoluteError =
    typeof candidatePrediction === 'number'
      ? round(Math.abs(candidatePrediction - row.measuredRefractiveIndex), 5)
      : null;
  return {
    formula: row.formula,
    freshCandidateValidation: Boolean(row.freshCandidateValidation),
    secondGenerationValidation: Boolean(row.secondGenerationValidation),
    measuredRefractiveIndex: row.measuredRefractiveIndex,
    candidatePrediction,
    candidateAbsoluteError,
    wouldPassTolerance:
      typeof candidateAbsoluteError === 'number' &&
      candidateAbsoluteError <= external.tolerances.refractiveIndexAbsoluteErrorMax,
  };
});
const calibrationCandidateRows = candidateRows.filter(
  (row) => !row.freshCandidateValidation && !row.secondGenerationValidation
);
const freshCandidateValidationRows = candidateRows.filter((row) => row.freshCandidateValidation);

const secondGenerationRows = rows.map((row) => {
  const composition = nbo.rows.find((compositionRow) => compositionRow.formula === row.formula);
  const candidatePrediction = predictSecondGenerationCandidate(composition);
  const candidateAbsoluteError =
    typeof candidatePrediction === 'number'
      ? round(Math.abs(candidatePrediction - row.measuredRefractiveIndex), 5)
      : null;
  return {
    formula: row.formula,
    secondGenerationValidation: Boolean(row.secondGenerationValidation),
    measuredRefractiveIndex: row.measuredRefractiveIndex,
    nboT: row.nboT,
    chargeBalancedAl: row.chargeBalancedAl,
    divalentModifierCharge: composition?.divalentModifierCharge ?? null,
    candidatePrediction,
    candidateAbsoluteError,
    currentRowsOnly: true,
    wouldPassTolerance:
      typeof candidateAbsoluteError === 'number' &&
      candidateAbsoluteError <= external.tolerances.refractiveIndexAbsoluteErrorMax,
  };
});
const secondGenerationCalibrationRows = secondGenerationRows.filter((row) => !row.secondGenerationValidation);
const secondGenerationValidationRows = secondGenerationRows.filter((row) => row.secondGenerationValidation);

const checks = [
  {
    check: 'Source anchors present',
    expectation: 'measured refractive-index targets should have explicit external source anchors',
    modelValue: external.sources.map((source) => source.label).join('; '),
    pass: external.sources.length === external.measuredRows.length,
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
  {
    check: 'Quarantined candidate discipline',
    expectation: 'target-implied coefficient revisions should be reported as calibration debt, not counted as a current pass',
    modelValue: `${quarantinedCandidate.name}: ${candidateRows
      .map((row) => `${row.formula} candidate error ${row.candidateAbsoluteError}`)
      .join('; ')}`,
    pass:
      quarantinedCandidate.status.includes('not counted') &&
      calibrationCandidateRows.every((row) => row.wouldPassTolerance),
    reading:
      'A revised slope/framework-Al candidate can fit the calibration rows, but because it is target-implied after failure it remains quarantined and must survive fresh validation before promotion.',
  },
  {
    check: 'Fresh held-out candidate validation',
    expectation: 'the quarantined candidate should clear a new material composition without changing coefficients before promotion',
    modelValue: freshCandidateValidationRows
      .map(
        (row) =>
          `${row.formula}: measured ${row.measuredRefractiveIndex}, candidate ${row.candidatePrediction}, error ${row.candidateAbsoluteError}`
      )
      .join('; '),
    pass:
      freshCandidateValidationRows.length > 0 &&
      freshCandidateValidationRows.every((row) => row.wouldPassTolerance),
    reading:
      'Anorthite is a fresh validation target for the quarantined candidate; failure here keeps the repair candidate from becoming a measured-property pass.',
  },
  {
    check: 'Second-generation candidate quarantine',
    expectation:
      'a repair introduced after anorthite failure may be reported only as calibration debt until a new held-out material validates it',
    modelValue: `${secondGenerationCandidate.name}: ${secondGenerationRows
      .map((row) => `${row.formula} candidate error ${row.candidateAbsoluteError}`)
      .join('; ')}`,
    pass:
      secondGenerationCandidate.status.includes('not counted') &&
      secondGenerationCalibrationRows.every((row) => row.wouldPassTolerance),
    reading:
      'A modifier-identity term can fit the rows available when it was introduced, but because it was added after seeing anorthite it remains calibration debt.',
  },
  {
    check: 'Second-generation held-out validation',
    expectation:
      'the modifier-identity candidate should clear a new source-anchored material composition without changing coefficients before promotion',
    modelValue: secondGenerationValidationRows
      .map(
        (row) =>
          `${row.formula}: measured ${row.measuredRefractiveIndex}, candidate ${row.candidatePrediction}, error ${row.candidateAbsoluteError}`
      )
      .join('; '),
    pass:
      secondGenerationValidationRows.length > 0 &&
      secondGenerationValidationRows.every((row) => row.wouldPassTolerance),
    reading:
      'Orthoclase is the fresh held-out validation target for the second-generation modifier-identity candidate; failure here keeps the material-property gate unresolved and identifies K/Na framework response as a missing variable.',
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
  quarantinedCandidate,
  secondGenerationCandidate,
  calibrationDiagnostic,
  frameworkPairs,
  candidateRows,
  secondGenerationRows,
  secondGenerationValidationRows,
  grammarVariables,
  rows,
  score,
  checks,
  confidenceEffect:
    status === 'measured material refractive-index pass'
      ? 'would support a material-property confidence increase because NBO/T accounting transfers to measured refractive index without target fitting'
      : 'holds confidence flat and preserves the material-property gate because the first-pass topology-only proxy does not yet satisfy measured refractive-index tolerance; the first repair fails fresh anorthite validation; the second-generation modifier-identity candidate fails fresh orthoclase validation',
};

await writeFile(new URL('external-material-refractive-index-challenge.json', outDir), JSON.stringify(report, null, 2));

const markdown = `# Relational Substrate External Material Refractive-Index Challenge

## Scope

This report turns the material-property gate into an explicit measured refractive-index challenge.

It asks whether the current material grammar can move beyond NBO/T composition accounting and produce a predeclared refractive-index prediction for source-anchored SiO2, Na2SiO3, held-out NaAlSi3O8, fresh-validation CaAl2Si2O8, and second-generation held-out KAlSi3O8 targets. The current answer is still no at pass level: a first-pass topology-only proxy exists, but it does not clear the measured tolerance and collapses distinct zero-NBO frameworks. A target-implied repair candidate also fails fresh anorthite validation. A second-generation modifier-identity candidate fits the rows available when it was introduced, but fails fresh orthoclase validation.

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

## Quarantined Candidate

This candidate is not counted as the benchmark result. It records the shape of the likely repair and the fresh held-out validation failure.

| Measure | Value |
|---|---|
| Name | ${quarantinedCandidate.name} |
| Equation | ${quarantinedCandidate.equation} |
| Coefficients | silicaBaseline ${quarantinedCandidate.silicaBaseline}; candidateNboTSlope ${quarantinedCandidate.candidateNboTSlope}; frameworkAlBoost ${quarantinedCandidate.frameworkAlBoost} |
| Status | ${quarantinedCandidate.status} |
| Reason | ${quarantinedCandidate.reason} |
| Release condition | ${quarantinedCandidate.releaseCondition} |

| Formula | Measured RI | Candidate prediction | Absolute error | Would pass tolerance |
|---|---:|---:|---:|---|
${candidateRows
  .map(
    (row) =>
      `| ${row.formula}${row.freshCandidateValidation ? ' (fresh validation)' : ''} | ${row.measuredRefractiveIndex} | ${row.candidatePrediction} | ${row.candidateAbsoluteError} | ${row.wouldPassTolerance ? 'yes' : 'no'} |`
  )
  .join('\n')}

## Second-Generation Quarantined Candidate

This candidate is also not counted as the benchmark result. It records the next repair hypothesis after the anorthite failure: a divalent-modifier correction distinguishes Na and Ca aluminosilicate frameworks, but current-row agreement is not validation because the term was added after seeing the CaAl2Si2O8 miss. Orthoclase is the first new held-out row after this candidate was fixed, and it fails tolerance.

| Measure | Value |
|---|---|
| Name | ${secondGenerationCandidate.name} |
| Equation | ${secondGenerationCandidate.equation} |
| Coefficients | silicaBaseline ${secondGenerationCandidate.silicaBaseline}; candidateNboTSlope ${secondGenerationCandidate.candidateNboTSlope}; frameworkAlBoost ${secondGenerationCandidate.frameworkAlBoost}; divalentModifierPenalty ${secondGenerationCandidate.divalentModifierPenalty} |
| Status | ${secondGenerationCandidate.status} |
| Reason | ${secondGenerationCandidate.reason} |
| Release condition | ${secondGenerationCandidate.releaseCondition} |

| Formula | Measured RI | Divalent modifier charge | Candidate prediction | Absolute error | Held-out for this candidate | Would pass tolerance |
|---|---:|---:|---:|---:|---|
${secondGenerationRows
  .map(
    (row) =>
      `| ${row.formula} | ${row.measuredRefractiveIndex} | ${row.divalentModifierCharge} | ${row.candidatePrediction} | ${row.candidateAbsoluteError} | ${row.secondGenerationValidation ? 'yes' : 'no'} | ${row.wouldPassTolerance ? 'yes' : 'no'} |`
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

This is an unresolved calibration challenge, not a failed source check. The material grammar has reached exact composition accounting and now has a first-pass topology-only refractive-index proxy, but the proxy does not satisfy measured tolerance across all targets. The held-out albite row shows that NBO/T alone collapses silica and charge-balanced aluminosilicate frameworks that have different measured refractive indices. A target-implied candidate with a stronger NBO/T slope and positive framework-Al contribution fits the calibration rows, but fresh anorthite validation misses tolerance, so this repair candidate remains failed calibration debt rather than a promotable material-property model. A second-generation modifier-identity candidate fits the rows available when it was introduced by adding a divalent-modifier correction, but fresh orthoclase validation misses tolerance, so K/Na framework response remains a missing variable. Orthoclase is structurally meaningful because K+ and Na+ are both monovalent modifiers, but K+ has larger ionic radius and lower field strength than Na+; the current modifier term does not distinguish those cation-response differences, so this is a cation-sensitivity test rather than merely another numerical tolerance row.
`;

await writeFile(new URL('external-material-refractive-index-challenge.md', outDir), markdown);

console.log(`External material refractive-index challenge: ${status}`);
console.log(`Score: ${score}`);
console.log(`Wrote ${new URL('external-material-refractive-index-challenge.md', outDir).pathname}`);
