import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const atomicMass = {
  O: 15.999,
  Al: 26.9815385,
  Si: 28.085,
  Ca: 40.078,
  Na: 22.98976928,
  K: 39.0983,
};

const cfs = {
  Na: { delta: 0 },
  K: { delta: -0.2796 },
  Ca: { delta: 0.8762 },
};

const tolerance = 0.01;

const trainingRows = [
  {
    formula: 'SiO2',
    material: 'fused silica',
    composition: { Si: 1, O: 2 },
    density: 2.203,
    measuredRefractiveIndex: 1.45704,
    nboT: 0,
    chargeBalancedAlO: 0,
    cationDelta: 0,
  },
  {
    formula: 'Na2SiO3',
    material: 'sodium silicate glass',
    composition: { Na: 2, Si: 1, O: 3 },
    density: 2.614,
    measuredRefractiveIndex: 1.52,
    nboT: 2,
    chargeBalancedAlO: 0,
    cationDelta: 0,
  },
  {
    formula: 'NaAlSi3O8',
    material: 'albite',
    composition: { Na: 1, Al: 1, Si: 3, O: 8 },
    density: midpoint([2.6, 2.65]),
    measuredRefractiveIndex: 1.53493,
    nboT: 0,
    chargeBalancedAlO: 1 / 8,
    cationDelta: cfs.Na.delta,
  },
  {
    formula: 'CaAl2Si2O8',
    material: 'anorthite',
    composition: { Ca: 1, Al: 2, Si: 2, O: 8 },
    density: midpoint([2.74, 2.76]),
    measuredRefractiveIndex: 1.58167,
    nboT: 0,
    chargeBalancedAlO: 2 / 8,
    cationDelta: cfs.Ca.delta,
  },
  {
    formula: 'KAlSi3O8',
    material: 'orthoclase',
    composition: { K: 1, Al: 1, Si: 3, O: 8 },
    density: midpoint([2.55, 2.63]),
    measuredRefractiveIndex: 1.52183,
    nboT: 0,
    chargeBalancedAlO: 1 / 8,
    cationDelta: cfs.K.delta,
  },
  {
    formula: 'KAlSiO4',
    material: 'kalsilite',
    composition: { K: 1, Al: 1, Si: 1, O: 4 },
    density: midpoint([2.59, 2.62]),
    measuredRefractiveIndex: 1.5375,
    nboT: 0,
    chargeBalancedAlO: 1 / 4,
    cationDelta: cfs.K.delta,
  },
];

const target = {
  formula: 'Ca2Al2SiO7',
  material: 'gehlenite',
  topologyClass: 'sorosilicate',
  composition: { Ca: 2, Al: 2, Si: 1, O: 7 },
  density: 2.97714,
  densitySource: 'CatalystHub/Materials Project Ca2Al2SiO7 structure density',
  nboT: 2 / 3,
  chargeBalancedAlO: 2 / 7,
  cationDelta: cfs.Ca.delta,
  refractiveIndexSource: {
    label: 'Burshtein, Shimony, and Levy, JOSA A 10, 2246-2247 (1993)',
    url: 'https://opg.optica.org/josaa/abstract.cfm?uri=josaa-10-10-2246',
    sourceValue:
      'Table 1 reports n_o = 1.665 +/- 0.003 and n_e - n_o = -0.0085 +/- 0.0003 at 632.8 nm.',
    scalarPolicy:
      'Use principal-axis scalar mean (2*n_o + n_e)/3 for uniaxial tetragonal gehlenite.',
  },
  ordinaryIndex: 1.665,
  extraordinaryMinusOrdinary: -0.0085,
};

function midpoint([low, high]) {
  return (low + high) / 2;
}

function round(value, places = 5) {
  return Number(value.toFixed(places));
}

function llFromN(n) {
  return (n ** 2 - 1) / (n ** 2 + 2);
}

function nFromLl(ll) {
  return Math.sqrt((1 + 2 * ll) / (1 - ll));
}

function molarMass(composition) {
  return Object.entries(composition).reduce((sum, [element, count]) => sum + atomicMass[element] * count, 0);
}

function count(row, element) {
  return row.composition[element] ?? 0;
}

function tetrahedralCations(row) {
  return count(row, 'Si') + count(row, 'Al');
}

function cationResponseO(row) {
  return row.chargeBalancedAlO * row.cationDelta;
}

function decorate(row) {
  const mass = molarMass(row.composition);
  const molarVolume = mass / row.density;
  const nboOxygen = row.nboT * tetrahedralCations(row);
  const bridgingOxygen = count(row, 'O') - nboOxygen;
  return {
    ...row,
    oxygenVolume: molarVolume / count(row, 'O'),
    tetrahedralPackingDensity: tetrahedralCations(row) / molarVolume,
    cationResponseO: cationResponseO(row),
    bridgeOxygenFraction: bridgingOxygen / count(row, 'O'),
  };
}

function transpose(matrix) {
  return matrix[0].map((_, columnIndex) => matrix.map((row) => row[columnIndex]));
}

function multiply(a, b) {
  return a.map((row) => b[0].map((_, j) => row.reduce((sum, value, k) => sum + value * b[k][j], 0)));
}

function invert(matrix) {
  const n = matrix.length;
  const augmented = matrix.map((row, i) => [
    ...row,
    ...Array.from({ length: n }, (_, j) => (i === j ? 1 : 0)),
  ]);
  for (let col = 0; col < n; col += 1) {
    let pivot = col;
    for (let row = col + 1; row < n; row += 1) {
      if (Math.abs(augmented[row][col]) > Math.abs(augmented[pivot][col])) pivot = row;
    }
    if (Math.abs(augmented[pivot][col]) < 1e-12) throw new Error('Singular design matrix');
    [augmented[col], augmented[pivot]] = [augmented[pivot], augmented[col]];
    const divisor = augmented[col][col];
    augmented[col] = augmented[col].map((value) => value / divisor);
    for (let row = 0; row < n; row += 1) {
      if (row === col) continue;
      const factor = augmented[row][col];
      augmented[row] = augmented[row].map((value, j) => value - factor * augmented[col][j]);
    }
  }
  return augmented.map((row) => row.slice(n));
}

function leastSquares(x, y) {
  const xt = transpose(x);
  const xtx = multiply(xt, x);
  const xty = multiply(xt, y.map((value) => [value]));
  return multiply(invert(xtx), xty).map(([value]) => value);
}

const featureFamilies = [
  {
    name: 'density + Al/O + cation-response/O',
    labels: ['intercept', 'density', 'Al/O', 'cationResponse/O'],
    reason:
      'best current-corpus Lorentz-Lorenz residual among separable candidates; physically straightforward positive coefficient signs before target scoring',
    row: (row) => [1, row.density, row.chargeBalancedAlO, row.cationResponseO],
  },
  {
    name: 'minimal oxygen-volume + Al/O',
    labels: ['intercept', 'oxygenVolume', 'Al/O'],
    reason:
      'cleanest standardized conditioning and an interpretable packing term, retained as the simpler lateral-pattern candidate',
    row: (row) => [1, row.oxygenVolume, row.chargeBalancedAlO],
  },
];

const training = trainingRows.map(decorate);
const decoratedTarget = decorate(target);
const measuredTargetRi = round((2 * target.ordinaryIndex + target.ordinaryIndex + target.extraordinaryMinusOrdinary) / 3, 5);
const targetLl = llFromN(measuredTargetRi);

const familyResults = featureFamilies.map((family) => {
  const coefficients = leastSquares(
    training.map(family.row),
    training.map((row) => llFromN(row.measuredRefractiveIndex))
  );
  const targetLlPrediction = family
    .row(decoratedTarget)
    .reduce((sum, value, index) => sum + value * coefficients[index], 0);
  const predictedRi = round(nFromLl(targetLlPrediction), 5);
  const absoluteError = round(Math.abs(predictedRi - measuredTargetRi), 5);
  return {
    name: family.name,
    reason: family.reason,
    labels: family.labels,
    coefficients: Object.fromEntries(family.labels.map((label, index) => [label, round(coefficients[index], 8)])),
    predictedRi,
    measuredTargetRi,
    absoluteError,
    pass: absoluteError <= tolerance,
  };
});

const postFailureBridgeFamily = {
  name: 'post-failure density + Al/O + cation-response/O + bridge-O fraction',
  labels: ['intercept', 'density', 'Al/O', 'cationResponse/O', 'bridgeOxygenFraction'],
  status: 'post-failure diagnostic only; descriptor chosen after seeing gehlenite miss',
  row: (row) => [1, row.density, row.chargeBalancedAlO, row.cationResponseO, row.bridgeOxygenFraction],
};

const postFailureCoefficients = leastSquares(
  training.map(postFailureBridgeFamily.row),
  training.map((row) => llFromN(row.measuredRefractiveIndex))
);
const postFailurePredictionLl = postFailureBridgeFamily
  .row(decoratedTarget)
  .reduce((sum, value, index) => sum + value * postFailureCoefficients[index], 0);
const postFailurePrediction = round(nFromLl(postFailurePredictionLl), 5);
const postFailureDiagnostic = {
  name: postFailureBridgeFamily.name,
  status: postFailureBridgeFamily.status,
  coefficients: Object.fromEntries(
    postFailureBridgeFamily.labels.map((label, index) => [label, round(postFailureCoefficients[index], 8)])
  ),
  targetBridgeOxygenFraction: round(decoratedTarget.bridgeOxygenFraction, 6),
  predictedRi: postFailurePrediction,
  measuredTargetRi,
  absoluteError: round(Math.abs(postFailurePrediction - measuredTargetRi), 5),
};

const status = familyResults.some((row) => row.pass)
  ? 'fresh gehlenite RI validation has at least one candidate pass'
  : 'fresh gehlenite RI validation failed both frozen candidate families';

const report = {
  source: 'external-ri-gehlenite-fresh-validation.mjs',
  status,
  tolerance,
  trainingRows: training,
  target: {
    ...decoratedTarget,
    extraordinaryIndex: round(target.ordinaryIndex + target.extraordinaryMinusOrdinary, 5),
    measuredTargetRi,
    targetLl: round(targetLl, 8),
  },
  featureFamilies,
  familyResults,
  postFailureDiagnostic,
};

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const markdown = `# Fresh RI Validation: Gehlenite

## Scope

This report scores a fresh gehlenite refractive-index target after freezing two descriptor families from the current measured corpus. It does not change the main material-property benchmark score by itself.

## Target

| Measure | Value |
|---|---|
| Formula | ${target.formula} |
| Material | ${target.material} |
| Topology class | ${target.topologyClass} |
| Density | ${target.density} |
| Density source | ${target.densitySource} |
| RI source | ${target.refractiveIndexSource.label} |
| RI source value | ${target.refractiveIndexSource.sourceValue} |
| Scalar policy | ${target.refractiveIndexSource.scalarPolicy} |
| Scalar measured RI | ${measuredTargetRi} |
| Tolerance | ${tolerance} |

Source URL: ${target.refractiveIndexSource.url}

## Frozen Candidate Results

${table(
  ['Candidate family', 'Reason frozen', 'Coefficients', 'Predicted RI', 'Measured RI', 'Absolute error', 'Pass'],
  familyResults.map((row) => [
    row.name,
    row.reason,
    Object.entries(row.coefficients)
      .map(([key, value]) => `${key}: ${value}`)
      .join('; '),
    row.predictedRi,
    row.measuredTargetRi,
    row.absoluteError,
    row.pass ? 'yes' : 'no',
  ])
)}

## Status

${status}.

## Post-Failure Bridge-Oxygen Diagnostic

This diagnostic is not validation. The bridge-oxygen fraction term was introduced after the gehlenite miss, following the interpretation that sorosilicate topology may not be represented by density, Al/O, and cation response alone.

${table(
  ['Diagnostic family', 'Status', 'Coefficients', 'Target bridge-O fraction', 'Predicted RI', 'Measured RI', 'Absolute error'],
  [
    [
      postFailureDiagnostic.name,
      postFailureDiagnostic.status,
      Object.entries(postFailureDiagnostic.coefficients)
        .map(([key, value]) => `${key}: ${value}`)
        .join('; '),
      postFailureDiagnostic.targetBridgeOxygenFraction,
      postFailureDiagnostic.predictedRi,
      postFailureDiagnostic.measuredTargetRi,
      postFailureDiagnostic.absoluteError,
    ],
  ]
)}

## Reading

Gehlenite is a sharper test than another feldspar because it keeps Ca-Al-Si-O chemistry but changes topology class to sorosilicate. The result tests whether the packed-framework descriptor families are transferring physical embedding or only fitting feldspar/glass rows.

If both frozen families fail, the reading is not that packing is irrelevant. It is that the current scalar descriptor families do not yet bridge topology class strongly enough for measured RI. If one family passes, it should still be treated as first fresh evidence only, not as a promoted RI model, because topology-class coverage remains sparse.

The post-failure bridge-oxygen diagnostic tests a candidate explanation for the miss. Any improvement is calibration debt until a new target is reserved and scored without changing the descriptor.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('external-ri-gehlenite-fresh-validation.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('external-ri-gehlenite-fresh-validation.md', outDir), markdown);

console.log(markdown);
