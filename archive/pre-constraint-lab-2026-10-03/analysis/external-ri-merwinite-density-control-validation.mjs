import { readFile, mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const reservationReport = JSON.parse(
  await readFile(new URL('./out/ri-density-control-falsifier-reservation-diagnostic.json', import.meta.url))
);

const atomicMass = {
  O: 15.999,
  Mg: 24.305,
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
    topologyClass: 'polymerized glass network',
    composition: { Si: 1, O: 2 },
    density: 2.203,
    measuredRi: 1.45704,
    chargeBalancedAlO: 0,
    cationDelta: 0,
  },
  {
    formula: 'Na2SiO3',
    material: 'sodium silicate glass',
    topologyClass: 'depolymerized metasilicate glass',
    composition: { Na: 2, Si: 1, O: 3 },
    density: 2.614,
    measuredRi: 1.52,
    chargeBalancedAlO: 0,
    cationDelta: 0,
  },
  {
    formula: 'NaAlSi3O8',
    material: 'albite',
    topologyClass: 'feldspar framework',
    composition: { Na: 1, Al: 1, Si: 3, O: 8 },
    density: 2.625,
    measuredRi: 1.53493,
    chargeBalancedAlO: 1 / 8,
    cationDelta: cfs.Na.delta,
  },
  {
    formula: 'CaAl2Si2O8',
    material: 'anorthite',
    topologyClass: 'feldspar framework',
    composition: { Ca: 1, Al: 2, Si: 2, O: 8 },
    density: 2.75,
    measuredRi: 1.58167,
    chargeBalancedAlO: 2 / 8,
    cationDelta: cfs.Ca.delta,
  },
  {
    formula: 'KAlSi3O8',
    material: 'orthoclase',
    topologyClass: 'feldspar framework',
    composition: { K: 1, Al: 1, Si: 3, O: 8 },
    density: 2.59,
    measuredRi: 1.52183,
    chargeBalancedAlO: 1 / 8,
    cationDelta: cfs.K.delta,
  },
  {
    formula: 'KAlSiO4',
    material: 'kalsilite',
    topologyClass: 'feldspathoid framework',
    composition: { K: 1, Al: 1, Si: 1, O: 4 },
    density: 2.605,
    measuredRi: 1.5375,
    chargeBalancedAlO: 1 / 4,
    cationDelta: cfs.K.delta,
  },
  {
    formula: 'Ca2Al2SiO7',
    material: 'gehlenite',
    topologyClass: 'melilite sorosilicate',
    composition: { Ca: 2, Al: 2, Si: 1, O: 7 },
    density: 2.97714,
    measuredRi: 1.66217,
    chargeBalancedAlO: 2 / 7,
    cationDelta: cfs.Ca.delta,
  },
  {
    formula: 'Ca2MgSi2O7',
    material: 'akermanite',
    topologyClass: 'melilite sorosilicate',
    composition: { Ca: 2, Mg: 1, Si: 2, O: 7 },
    density: 2.944,
    measuredRi: 1.63467,
    chargeBalancedAlO: 0,
    cationDelta: cfs.Ca.delta,
  },
];

const reserved = reservationReport.reservedTarget;
const target = {
  formula: 'Ca3Mg(SiO4)2',
  material: 'merwinite',
  topologyClass: reserved.topologyClass,
  compositionClass: reserved.compositionClass,
  composition: { Ca: 3, Mg: 1, Si: 2, O: 8 },
  density: reserved.densityForFutureScoring,
  measuredRi: 1.713666,
  scalarRiRange: reserved.scalarRiRange,
  chargeBalancedAlO: 0,
  cationDelta: cfs.Ca.delta,
  source: {
    primaryLabel: reserved.opticalSource.label,
    primaryUrl: reserved.opticalSource.url,
    primaryValue: reserved.opticalSource.value,
    cifUrl: reserved.cifSource.url,
    limitation: 'Mg-bearing Ca-silicate-family target; not pure Ca-Si-O continuation',
  },
};

function round(value, places = 5) {
  return Number(value.toFixed(places));
}

function llFromN(n) {
  return (n ** 2 - 1) / (n ** 2 + 2);
}

function nFromLl(ll) {
  return Math.sqrt((1 + 2 * ll) / (1 - ll));
}

function count(row, element) {
  return row.composition[element] ?? 0;
}

function molarMass(composition) {
  return Object.entries(composition).reduce((sum, [element, elementCount]) => sum + atomicMass[element] * elementCount, 0);
}

function decorate(row) {
  const oxygen = count(row, 'O');
  const molarVolume = molarMass(row.composition) / row.density;
  return {
    ...row,
    oxygenVolume: molarVolume / oxygen,
    caScaffoldO: count(row, 'Ca') / oxygen,
    mgScaffoldO: count(row, 'Mg') / oxygen,
    alCompensationResponseO: row.chargeBalancedAlO * row.cationDelta,
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

const families = [
  {
    name: 'baseline density + Al/O + Al-comp response',
    status: 'reference family before scaffold split',
    labels: ['intercept', 'density', 'Al/O', 'alCompResponse/O'],
    row: (row) => [1, row.density, row.chargeBalancedAlO, row.alCompensationResponseO],
  },
  {
    name: 'split Ca scaffold family',
    status: 'post-failure Ca scaffold family; no merwinite/topology term',
    labels: ['intercept', 'density', 'Al/O', 'alCompResponse/O', 'Ca/O'],
    row: (row) => [1, row.density, row.chargeBalancedAlO, row.alCompensationResponseO, row.caScaffoldO],
  },
  {
    name: 'split Ca/Mg scaffold family',
    status: 'post-failure Ca/Mg scaffold family; includes Mg/O but no merwinite/topology term',
    labels: ['intercept', 'density', 'Al/O', 'alCompResponse/O', 'Ca/O', 'Mg/O'],
    row: (row) => [1, row.density, row.chargeBalancedAlO, row.alCompensationResponseO, row.caScaffoldO, row.mgScaffoldO],
  },
];

const training = trainingRows.map(decorate);
const decoratedTarget = decorate(target);

const results = families.map((family) => {
  const coefficients = leastSquares(
    training.map(family.row),
    training.map((row) => llFromN(row.measuredRi))
  );
  const predictedLl = family
    .row(decoratedTarget)
    .reduce((sum, value, index) => sum + value * coefficients[index], 0);
  const predictedRi = round(nFromLl(predictedLl));
  const primaryError = round(Math.abs(predictedRi - target.measuredRi));
  const rangePass = predictedRi >= target.scalarRiRange[0] - tolerance && predictedRi <= target.scalarRiRange[1] + tolerance;
  return {
    name: family.name,
    status: family.status,
    coefficients: Object.fromEntries(family.labels.map((label, index) => [label, round(coefficients[index], 8)])),
    predictedRi,
    measuredRi: target.measuredRi,
    scalarRiRange: target.scalarRiRange,
    primaryError,
    midpointPass: primaryError <= tolerance,
    rangePass,
    residual: round(target.measuredRi - predictedRi),
  };
});

const baseline = results.find((row) => row.name === 'baseline density + Al/O + Al-comp response');
const splitCa = results.find((row) => row.name === 'split Ca scaffold family');
const splitCaMg = results.find((row) => row.name === 'split Ca/Mg scaffold family');

const status = baseline.midpointPass
  ? 'merwinite repeats density-control pass under Mg-bearing limitation'
  : 'merwinite breaks density-control pass; larnite baseline success remains local';

const report = {
  source: 'external-ri-merwinite-density-control-validation.mjs',
  status,
  tolerance,
  target: decoratedTarget,
  reservationBoundary: reservationReport.lockedPreScoreExpectations,
  results,
  interpretation:
    baseline.midpointPass && !splitCa.midpointPass
      ? 'The density-family pass repeats while scalar Ca scaffold still overpredicts. This increases pressure to treat density/polarizability as a conventional control rather than substrate-specific validation.'
      : 'The merwinite result should be read against the frozen reservation boundary; Mg chemistry prevents pure Ca-Si-O transfer claims.',
};

const reading =
  baseline.midpointPass && !splitCa.midpointPass
    ? 'Merwinite repeats the baseline density-family pass while scalar Ca scaffold fails. This would increase pressure to treat density/polarizability as the main control.'
    : !baseline.midpointPass && splitCa.midpointPass
      ? 'Merwinite breaks the baseline density-family pass while the split-Ca and split-Ca/Mg families pass. This means larnite baseline success was local, and the Ca/Mg-bearing row cannot be used as pure Ca-Si-O validation.'
      : baseline.midpointPass && splitCa.midpointPass
        ? 'Both baseline and split-Ca families pass merwinite, so this row does not discriminate density control from scaffold terms.'
        : 'Both baseline and split-Ca families fail merwinite, so this row weakens both current control families.';

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

function coefficients(row) {
  return Object.entries(row.coefficients)
    .map(([label, value]) => `${label}: ${value}`)
    .join('; ');
}

const markdown = `# RI Density-Control Validation: Merwinite

## Scope

This scores merwinite only after it was reserved as a density-control falsifier. It does not change coefficients, thresholds, density handling, or source interpretation. Because merwinite contains Mg, it is not a pure Ca-Si-O continuation.

## Target

${table(
  ['Measure', 'Value'],
  [
    ['Formula', target.formula],
    ['Material', target.material],
    ['Topology class', target.topologyClass],
    ['Composition class', target.compositionClass],
    ['Density used', target.density],
    ['Ca/O', round(decoratedTarget.caScaffoldO)],
    ['Mg/O', round(decoratedTarget.mgScaffoldO)],
    ['Oxygen volume', round(decoratedTarget.oxygenVolume)],
    ['Primary source', target.source.primaryLabel],
    ['Primary source value', target.source.primaryValue],
    ['Scalar RI range', target.scalarRiRange.join('-')],
    ['Scalar RI midpoint', target.measuredRi],
    ['Tolerance', tolerance],
  ]
)}

Primary source URL: ${target.source.primaryUrl}

CIF source URL: ${target.source.cifUrl}

## Frozen Candidate Results

${table(
  ['Candidate family', 'Status', 'Predicted RI', 'Measured midpoint', 'Error', 'Midpoint pass', 'Range pass', 'Residual'],
  results.map((row) => [
    row.name,
    row.status,
    row.predictedRi,
    row.measuredRi,
    row.primaryError,
    row.midpointPass ? 'yes' : 'no',
    row.rangePass ? 'yes' : 'no',
    row.residual,
  ])
)}

## Coefficients

${table(['Candidate family', 'Coefficients'], results.map((row) => [row.name, coefficients(row)]))}

## Status

${status}.

## Reading

${reading} The split-Ca/Mg family should not be promoted from this result because Mg/O was introduced after akermanite and is being tested here in a Mg-bearing row. The disciplined reading is that merwinite is a useful control contrast, not a material-property validation pass.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('external-ri-merwinite-density-control-validation.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('external-ri-merwinite-density-control-validation.md', outDir), markdown);

console.log(markdown);
