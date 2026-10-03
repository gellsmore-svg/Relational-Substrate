import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

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
  formula: 'Ca3Si2O7',
  material: 'rankinite',
  topologyClass: 'rankinite-like Ca sorosilicate',
  composition: { Ca: 3, Si: 2, O: 7 },
  density: 2.98,
  measuredRi: 1.645667,
  scalarRiRange: [1.644333, 1.647],
  chargeBalancedAlO: 0,
  cationDelta: cfs.Ca.delta,
  source: {
    primaryLabel: 'Handbook of Mineralogy, Rankinite PDF',
    primaryUrl: 'https://handbookofmineralogy.org/pdfs/rankinite.pdf',
    primaryValue:
      'Lists D(meas.) = 2.96-3.00 and biaxial alpha = 1.640-1.643, beta = 1.643-1.646, gamma = 1.650-1.652.',
    secondaryUrl: 'https://webmineral.com/data/Rankinite.shtml',
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
    status: 'post-failure Ca scaffold family; no rankinite/topology term',
    labels: ['intercept', 'density', 'Al/O', 'alCompResponse/O', 'Ca/O'],
    row: (row) => [1, row.density, row.chargeBalancedAlO, row.alCompensationResponseO, row.caScaffoldO],
  },
  {
    name: 'split Ca/Mg scaffold family',
    status: 'post-failure Ca/Mg scaffold family; Mg/O is zero for rankinite',
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
  ? 'rankinite weakens topology-gated Ca-scaffold interpretation: Ca-scaffold family passed'
  : 'rankinite supports topology-gated Ca-scaffold interpretation: Ca-scaffold family failed transfer';

const report = {
  source: 'external-ri-rankinite-ca-scaffold-transfer-validation.mjs',
  status,
  tolerance,
  target: decoratedTarget,
  results,
  interpretation:
    'Rankinite is a non-melilite Ca-rich sorosilicate. A pass would imply the melilite Ca-scaffold uplift transfers without topology gating. A failure supports topology gating but does not calibrate the corrected model.',
};

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const markdown = `# RI Ca-Scaffold Transfer Validation: Rankinite

## Scope

This scores rankinite as a non-melilite Ca-scaffold transfer test under the frozen T1-buffer contract. It does not validate the melilite T1-buffer model. It asks whether the Ca-scaffold uplift that repaired gehlenite/akermanite transfers to a Ca-rich sorosilicate with different topology and no Mg/Al/Zn T1 chemistry.

## Target

| Measure | Value |
|---|---|
| Formula | ${target.formula} |
| Material | ${target.material} |
| Topology class | ${target.topologyClass} |
| Density used | ${target.density} |
| Ca/O | ${round(decoratedTarget.caScaffoldO)} |
| Oxygen volume | ${round(decoratedTarget.oxygenVolume)} |
| Primary source | ${target.source.primaryLabel} |
| Primary source value | ${target.source.primaryValue} |
| Scalar RI range | ${target.scalarRiRange.join('-')} |
| Scalar RI midpoint | ${target.measuredRi} |
| Tolerance | ${tolerance} |

Primary source URL: ${target.source.primaryUrl}

Secondary source URL: ${target.source.secondaryUrl}

## Frozen Candidate Results

${table(
  [
    'Candidate family',
    'Status',
    'Predicted RI',
    'Measured midpoint',
    'Error',
    'Midpoint pass',
    'Range pass',
    'Residual',
  ],
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

## Status

${status}.

## Reading

Rankinite does not carry Mg/Al/Zn T1 chemistry, so this is a cleaner test of Ca-scaffold transfer than gugiaite or alumoakermanite. If the Ca scaffold family passes, the melilite topology gate weakens. If it fails, the hardystonite lesson generalizes: Ca scaffold cannot be used as a transferable scalar without topology.

The result should not be used to fit a new topology term yet. It only decides whether the next model needs explicit topology gating before Ca scaffold is reused.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('external-ri-rankinite-ca-scaffold-transfer-validation.json', outDir),
  JSON.stringify(report, null, 2)
);
await writeFile(new URL('external-ri-rankinite-ca-scaffold-transfer-validation.md', outDir), markdown);

console.log(markdown);
