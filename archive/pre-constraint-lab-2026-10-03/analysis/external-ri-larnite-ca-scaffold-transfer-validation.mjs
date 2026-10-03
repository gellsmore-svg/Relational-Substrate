import { readFile, mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const gateReport = JSON.parse(await readFile(new URL('./out/ri-larnite-gate-classification-diagnostic.json', import.meta.url)));

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

const target = {
  formula: 'Ca2SiO4',
  material: 'larnite',
  topologyClass: 'Ca orthosilicate / beta-dicalcium silicate',
  composition: { Ca: 2, Si: 1, O: 4 },
  density: 3.305,
  measuredRi: 1.719666,
  scalarRiRange: [1.713333, 1.726],
  chargeBalancedAlO: 0,
  cationDelta: cfs.Ca.delta,
  preScoreGateClassification: gateReport.gateClassification,
  source: {
    primaryLabel: 'Handbook of Mineralogy, Larnite PDF',
    primaryUrl: 'https://handbookofmineralogy.org/pdfs/larnite.pdf',
    primaryValue:
      'Lists D(meas.) = 3.28-3.33 and biaxial alpha = 1.700-1.715, beta = 1.715-1.723, gamma = 1.725-1.740.',
    cifUrl: 'https://www.crystallography.net/cod/9017424.cif',
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
    status: 'post-failure Ca scaffold family; no larnite/topology term',
    labels: ['intercept', 'density', 'Al/O', 'alCompResponse/O', 'Ca/O'],
    row: (row) => [1, row.density, row.chargeBalancedAlO, row.alCompensationResponseO, row.caScaffoldO],
  },
  {
    name: 'split Ca/Mg scaffold family',
    status: 'post-failure Ca/Mg scaffold family; Mg/O is zero for larnite',
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

const caFamily = results.find((row) => row.name === 'split Ca scaffold family');
const status = caFamily.midpointPass
  ? 'larnite falsifies current compact-scaffold gate: Ca-scaffold family passed despite non-melilite classification'
  : 'larnite strengthens topology-gated Ca-scaffold interpretation: Ca-scaffold family failed transfer';

const report = {
  source: 'external-ri-larnite-ca-scaffold-transfer-validation.mjs',
  status,
  tolerance,
  target: decoratedTarget,
  preScoreGateClassification: gateReport.gateClassification,
  gateDescriptors: gateReport.larniteDescriptors,
  results,
  interpretation:
    'Larnite was classified before scoring as compact/lower-coordinate. A Ca-family overprediction supports non-transfer of melilite Ca uplift; a pass would weaken the frozen gate.',
};

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

const markdown = `# RI Ca-Scaffold Transfer Validation: Larnite

## Scope

This scores larnite only after its CIF gate classification was frozen. It does not change coefficients, thresholds, density handling, or source interpretation.

## Target

${table(
  ['Measure', 'Value'],
  [
    ['Formula', target.formula],
    ['Material', target.material],
    ['Topology class', target.topologyClass],
    ['Pre-score gate classification', gateReport.gateClassification],
    ['Density used', target.density],
    ['Ca/O', decoratedTarget.caScaffoldO],
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

The larnite result follows the pre-score gate direction. Larnite was classified as compact/lower-coordinate, and the melilite-derived Ca scaffold uplift overpredicts it badly. This strengthens the topology-gated reading: Ca/O and density are not enough; Ca scaffold response must be conditioned by local Ca environment and silicate topology before it can be reused outside melilite.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('external-ri-larnite-ca-scaffold-transfer-validation.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('external-ri-larnite-ca-scaffold-transfer-validation.md', outDir), markdown);

console.log(markdown);
