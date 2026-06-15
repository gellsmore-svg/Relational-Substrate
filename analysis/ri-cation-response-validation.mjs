import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function round(value, places = 5) {
  return Number(value.toFixed(places));
}

function midpoint([low, high]) {
  return (low + high) / 2;
}

const cfs = {
  Na: { radiusAngstrom: 1.18, value: 0.7182, delta: 0 },
  K: { radiusAngstrom: 1.51, value: 0.4386, delta: -0.2796 },
  Ca: { radiusAngstrom: 1.12, value: 1.5944, delta: 0.8762 },
};

const constants = {
  silicaBaseline: 1.46,
  nboSlope: 0.03,
  tolerance: 0.01,
};

const exposedRows = [
  {
    formula: 'SiO2',
    material: 'fused silica',
    measuredRefractiveIndex: 1.45704,
    oxygenCount: 2,
    nboT: 0,
    chargeBalancedAlO: 0,
    divalentModifierChargeO: 0,
    deltaCFS: 0,
  },
  {
    formula: 'Na2SiO3',
    material: 'sodium silicate glass',
    measuredRefractiveIndex: 1.52,
    oxygenCount: 3,
    nboT: 2,
    chargeBalancedAlO: 0,
    divalentModifierChargeO: 0,
    deltaCFS: 0,
  },
  {
    formula: 'NaAlSi3O8',
    material: 'albite feldspar',
    measuredRefractiveIndex: 1.53493,
    oxygenCount: 8,
    nboT: 0,
    chargeBalancedAlO: 0.125,
    divalentModifierChargeO: 0,
    deltaCFS: cfs.Na.delta,
    fitRole: 'exposed Na framework',
  },
  {
    formula: 'CaAl2Si2O8',
    material: 'anorthite feldspar',
    measuredRefractiveIndex: 1.58167,
    oxygenCount: 8,
    nboT: 0,
    chargeBalancedAlO: 0.25,
    divalentModifierChargeO: 0.25,
    deltaCFS: cfs.Ca.delta,
    fitRole: 'exposed Ca framework',
  },
  {
    formula: 'KAlSi3O8',
    material: 'orthoclase feldspar',
    measuredRefractiveIndex: 1.52183,
    oxygenCount: 8,
    nboT: 0,
    chargeBalancedAlO: 0.125,
    divalentModifierChargeO: 0,
    deltaCFS: cfs.K.delta,
    fitRole: 'exposed K framework / prior held-out failure',
  },
];

const heldOutRows = [
  {
    formula: 'KAlSiO4',
    material: 'kalsilite feldspathoid',
    measuredRefractiveIndex: round(
      (midpoint([1.538, 1.543]) + midpoint([1.532, 1.537])) / 2,
      5
    ),
    sourceValue: 'Mindat optical data: n_omega = 1.538-1.543; n_epsilon = 1.532-1.537',
    sourceUrl: 'https://www.mindat.org/min-2142.html',
    oxygenCount: 4,
    nboT: 0,
    chargeBalancedAlO: 0.25,
    divalentModifierChargeO: 0,
    deltaCFS: cfs.K.delta,
    role: 'primary K-bearing fresh validation',
  },
  {
    formula: 'NaAlSiO4',
    material: 'nepheline feldspathoid',
    measuredRefractiveIndex: round(
      (midpoint([1.529, 1.546]) + midpoint([1.526, 1.542])) / 2,
      5
    ),
    sourceValue:
      'Mindat optical data: n_omega = 1.529-1.546; n_epsilon = 1.526-1.542; current Mindat formula is Na3K(Al4Si4O16), not pure NaAlSiO4',
    sourceUrl: 'https://www.mindat.org/min-2880.html',
    oxygenCount: 4,
    nboT: 0,
    chargeBalancedAlO: 0.25,
    divalentModifierChargeO: 0,
    deltaCFS: cfs.Na.delta,
    role: 'secondary transfer check; source formula mismatch means not counted as clean Na-only validation',
    compromised: true,
  },
];

function cationResponseO(row) {
  return row.chargeBalancedAlO * row.deltaCFS;
}

const albite = exposedRows.find((row) => row.formula === 'NaAlSi3O8');
const anorthite = exposedRows.find((row) => row.formula === 'CaAl2Si2O8');
const orthoclase = exposedRows.find((row) => row.formula === 'KAlSi3O8');

const frameworkAlOBoost = round(
  (albite.measuredRefractiveIndex - constants.silicaBaseline) / albite.chargeBalancedAlO,
  8
);
const kCfsO = round(
  (orthoclase.measuredRefractiveIndex -
    constants.silicaBaseline -
    frameworkAlOBoost * orthoclase.chargeBalancedAlO) /
    cationResponseO(orthoclase),
  8
);
const divalentOChargePenalty = round(
  (constants.silicaBaseline +
    frameworkAlOBoost * anorthite.chargeBalancedAlO +
    kCfsO * cationResponseO(anorthite) -
    anorthite.measuredRefractiveIndex) /
    anorthite.divalentModifierChargeO,
  8
);

const coefficients = {
  frameworkAlOBoost,
  divalentOChargePenalty,
  kCfsO,
};

function predict(row, includeCfs = true) {
  const cfsTerm = includeCfs ? coefficients.kCfsO * cationResponseO(row) : 0;
  return round(
    constants.silicaBaseline +
      constants.nboSlope * row.nboT +
      coefficients.frameworkAlOBoost * row.chargeBalancedAlO -
      coefficients.divalentOChargePenalty * row.divalentModifierChargeO +
      cfsTerm,
    5
  );
}

function descriptorKey(row) {
  return [
    row.nboT,
    row.chargeBalancedAlO,
    row.divalentModifierChargeO,
    row.deltaCFS,
  ].join('|');
}

function rowResult(row) {
  const basePrediction = predict(row, false);
  const fullPrediction = predict(row, true);
  const baseError = round(Math.abs(basePrediction - row.measuredRefractiveIndex), 5);
  const fullError = round(Math.abs(fullPrediction - row.measuredRefractiveIndex), 5);
  const degenerateWith = exposedRows
    .filter((exposed) => descriptorKey(exposed) === descriptorKey(row))
    .map((exposed) => exposed.formula);
  return {
    ...row,
    cationResponseO: round(cationResponseO(row), 6),
    basePrediction,
    fullPrediction,
    baseError,
    fullError,
    improvesOnBase: fullError < baseError,
    passTolerance: fullError <= constants.tolerance,
    degenerateWith,
  };
}

const fitRows = [albite, anorthite, orthoclase].map(rowResult);
const heldOutResults = heldOutRows.map(rowResult);

const kalsilite = heldOutResults.find((row) => row.formula === 'KAlSiO4');
const nepheline = heldOutResults.find((row) => row.formula === 'NaAlSiO4');
const measuredSeparation = round(
  Math.abs(kalsilite.measuredRefractiveIndex - nepheline.measuredRefractiveIndex),
  5
);
const predictedSeparation = round(Math.abs(kalsilite.fullPrediction - nepheline.fullPrediction), 5);

const classification = kalsilite.passTolerance
  ? nepheline.passTolerance && !nepheline.compromised
    ? 'narrow scalar material-property validation'
    : 'partial cation-response evidence'
  : kalsilite.improvesOnBase
    ? 'framework-Al extrapolation falsified'
    : 'cation-response axis falsified';

function table(headers, rows) {
  const align = headers.map(() => '---');
  return [
    `| ${headers.join(' | ')} |`,
    `| ${align.join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const report = `# RI Cation-Response Validation: Per-Oxygen Design

## Status

| Measure | Value |
|---|---|
| Design reviewed by Claude | cleared for execution with advisory notes |
| Coefficients frozen before held-out lookup | yes |
| Held-out RI lookup order | kalsilite first, nepheline second |
| Closing classification | ${classification} |

## Coefficients

${table(
  ['Coefficient', 'Value'],
  [
    ['silicaBaseline', constants.silicaBaseline],
    ['nboSlope', constants.nboSlope],
    ['frameworkAlOBoost', coefficients.frameworkAlOBoost],
    ['divalentOChargePenalty', coefficients.divalentOChargePenalty],
    ['k_cfsO', coefficients.kCfsO],
  ]
)}

Sign-band check: ${coefficients.kCfsO > 0 && coefficients.kCfsO <= 1 ? 'PASS' : 'WARNING/FAIL'} against predeclared \`0 < k_cfsO <= 1.0\`.

## Calibration Rows

These rows are exposed calibration debt, not validation passes. Orthoclase is included because it is already a prior failed held-out check.

${table(
  [
    'Formula',
    'Measured RI',
    'chargeBalancedAlO',
    'divalentModifierChargeO',
    'deltaCFS',
    'cationResponseO',
    'Full prediction',
    'Residual',
  ],
  fitRows.map((row) => [
    row.formula,
    row.measuredRefractiveIndex,
    row.chargeBalancedAlO,
    row.divalentModifierChargeO,
    row.deltaCFS,
    row.cationResponseO,
    row.fullPrediction,
    round(row.fullPrediction - row.measuredRefractiveIndex, 5),
  ])
)}

## Held-Out Results

${table(
  [
    'Formula',
    'Role',
    'Measured RI',
    'BaseO prediction',
    'FullO prediction',
    'Base error',
    'Full error',
    'Improves on base',
    'Tolerance pass',
    'Descriptor-degenerate with exposed row',
  ],
  heldOutResults.map((row) => [
    row.formula,
    row.role,
    row.measuredRefractiveIndex,
    row.basePrediction,
    row.fullPrediction,
    row.baseError,
    row.fullError,
    row.improvesOnBase ? 'yes' : 'no',
    row.passTolerance ? 'yes' : 'no',
    row.degenerateWith.length ? row.degenerateWith.join(', ') : 'no',
  ])
)}

## K/Na Separation

| Measure | Value |
|---|---:|
| Measured kalsilite/nepheline scalar RI separation | ${measuredSeparation} |
| Predicted kalsilite/nepheline scalar RI separation | ${predictedSeparation} |

## Source Anchors

- Kalsilite: ${heldOutRows[0].sourceUrl}. ${heldOutRows[0].sourceValue}. Scalar target uses the mean of the omega and epsilon range midpoints: ${heldOutRows[0].measuredRefractiveIndex}.
- Nepheline: ${heldOutRows[1].sourceUrl}. ${heldOutRows[1].sourceValue}. Scalar target uses the mean of the omega and epsilon range midpoints: ${heldOutRows[1].measuredRefractiveIndex}.

## Reading

The per-oxygen design breaks the descriptor degeneracy that blocked the prior design, and the fitted cation-response term moves kalsilite in the correct direction relative to the \`k_cfsO = 0\` baseline. It does not clear the measured-property tolerance: kalsilite remains outside the predeclared absolute RI error threshold by ${kalsilite.fullError}, so this is not a material-property validation pass.

The primary failure is framework-Al extrapolation: oxygen-normalised Al density pushes the feldspathoid predictions too high. Nepheline is additionally compromised as a clean Na-only transfer check because the current Mindat formula is mixed Na/K rather than pure NaAlSiO4.

No descriptor, coordination number, normalisation, target, or coefficient was changed after held-out lookup.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-cation-response-validation.json', outDir), JSON.stringify({
  constants,
  cfs,
  coefficients,
  fitRows,
  heldOutResults,
  measuredSeparation,
  predictedSeparation,
  classification,
}, null, 2));
await writeFile(new URL('ri-cation-response-validation.md', outDir), report);

console.log(report);
