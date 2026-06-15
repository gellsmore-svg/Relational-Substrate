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
  Zn: 65.38,
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
    measuredRi: 1.45704,
    chargeBalancedAlO: 0,
    cationDelta: 0,
  },
  {
    formula: 'Na2SiO3',
    material: 'sodium silicate glass',
    composition: { Na: 2, Si: 1, O: 3 },
    density: 2.614,
    measuredRi: 1.52,
    chargeBalancedAlO: 0,
    cationDelta: 0,
  },
  {
    formula: 'NaAlSi3O8',
    material: 'albite',
    composition: { Na: 1, Al: 1, Si: 3, O: 8 },
    density: 2.625,
    measuredRi: 1.53493,
    chargeBalancedAlO: 1 / 8,
    cationDelta: cfs.Na.delta,
  },
  {
    formula: 'CaAl2Si2O8',
    material: 'anorthite',
    composition: { Ca: 1, Al: 2, Si: 2, O: 8 },
    density: 2.75,
    measuredRi: 1.58167,
    chargeBalancedAlO: 2 / 8,
    cationDelta: cfs.Ca.delta,
  },
  {
    formula: 'KAlSi3O8',
    material: 'orthoclase',
    composition: { K: 1, Al: 1, Si: 3, O: 8 },
    density: 2.59,
    measuredRi: 1.52183,
    chargeBalancedAlO: 1 / 8,
    cationDelta: cfs.K.delta,
  },
  {
    formula: 'KAlSiO4',
    material: 'kalsilite',
    composition: { K: 1, Al: 1, Si: 1, O: 4 },
    density: 2.605,
    measuredRi: 1.5375,
    chargeBalancedAlO: 1 / 4,
    cationDelta: cfs.K.delta,
  },
  {
    formula: 'Ca2Al2SiO7',
    material: 'gehlenite',
    composition: { Ca: 2, Al: 2, Si: 1, O: 7 },
    density: 2.97714,
    measuredRi: 1.66217,
    chargeBalancedAlO: 2 / 7,
    cationDelta: cfs.Ca.delta,
  },
  {
    formula: 'Ca2MgSi2O7',
    material: 'akermanite',
    composition: { Ca: 2, Mg: 1, Si: 2, O: 7 },
    density: 2.944,
    measuredRi: 1.63467,
    chargeBalancedAlO: 0,
    cationDelta: cfs.Ca.delta,
  },
];

const target = {
  formula: 'Ca2ZnSi2O7',
  material: 'hardystonite',
  topologyClass: 'melilite sorosilicate',
  composition: { Ca: 2, Zn: 1, Si: 2, O: 7 },
  density: midpoint([3.396, 3.443]),
  chargeBalancedAlO: 0,
  cationDelta: cfs.Ca.delta,
  source: {
    primaryLabel: 'Handbook of Mineralogy, Hardystonite PDF',
    primaryUrl: 'https://www.handbookofmineralogy.org/pdfs/hardystonite.pdf',
    primaryValue:
      'Lists D(meas.) = 3.396-3.443, omega = 1.669, epsilon = 1.657.',
    alternateLabel: 'Webmineral/Mindat hardystonite optical tables',
    alternateValue:
      'Webmineral/Mindat list density about 3.40 and optical data omega = 1.672, epsilon = 1.661.',
  },
  omega: 1.669,
  epsilon: 1.657,
  alternateOmega: 1.672,
  alternateEpsilon: 1.661,
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
    znScaffoldO: count(row, 'Zn') / oxygen,
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
    name: 'split Ca scaffold family',
    status: 'frozen after gehlenite/akermanite failure; validates Ca scaffold transfer without Zn term',
    labels: ['intercept', 'density', 'Al/O', 'alCompResponse/O', 'Ca/O'],
    row: (row) => [1, row.density, row.chargeBalancedAlO, row.alCompensationResponseO, row.caScaffoldO],
  },
  {
    name: 'split Ca/Mg scaffold family',
    status: 'frozen after gehlenite/akermanite failure; no explicit Zn term, Mg/O is zero for hardystonite',
    labels: ['intercept', 'density', 'Al/O', 'alCompResponse/O', 'Ca/O', 'Mg/O'],
    row: (row) => [1, row.density, row.chargeBalancedAlO, row.alCompensationResponseO, row.caScaffoldO, row.mgScaffoldO],
  },
];

const training = trainingRows.map(decorate);
const decoratedTarget = decorate(target);
const measuredRi = round((2 * target.omega + target.epsilon) / 3);
const alternateMeasuredRi = round((2 * target.alternateOmega + target.alternateEpsilon) / 3);

const results = families.map((family) => {
  const coefficients = leastSquares(
    training.map(family.row),
    training.map((row) => llFromN(row.measuredRi))
  );
  const predictedLl = family
    .row(decoratedTarget)
    .reduce((sum, value, index) => sum + value * coefficients[index], 0);
  const predictedRi = round(nFromLl(predictedLl));
  const primaryError = round(Math.abs(predictedRi - measuredRi));
  const alternateError = round(Math.abs(predictedRi - alternateMeasuredRi));
  return {
    name: family.name,
    status: family.status,
    coefficients: Object.fromEntries(family.labels.map((label, index) => [label, round(coefficients[index], 8)])),
    predictedRi,
    measuredRi,
    alternateMeasuredRi,
    primaryError,
    alternateError,
    primaryPass: primaryError <= tolerance,
    alternatePass: alternateError <= tolerance,
  };
});

const status = results.some((row) => row.primaryPass)
  ? 'hardystonite Ca-scaffold validation has at least one primary-source pass'
  : 'hardystonite Ca-scaffold validation failed primary-source tolerance';

const report = {
  source: 'external-ri-hardystonite-ca-scaffold-validation.mjs',
  status,
  tolerance,
  target: {
    ...decoratedTarget,
    measuredRi,
    alternateMeasuredRi,
  },
  results,
};

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const markdown = `# RI Ca-Scaffold Validation: Hardystonite

## Scope

This report scores hardystonite as a fresh Ca-scaffold validation after the post-failure Ca scaffold split was frozen on gehlenite and akermanite. It tests whether the Ca scaffold term transfers to a same-topology Ca-Zn melilite without adding a Zn-specific term.

## Target

| Measure | Value |
|---|---|
| Formula | ${target.formula} |
| Material | ${target.material} |
| Topology class | ${target.topologyClass} |
| Density used | ${target.density} |
| Primary source | ${target.source.primaryLabel} |
| Primary source value | ${target.source.primaryValue} |
| Primary scalar RI | ${measuredRi} |
| Alternate source note | ${target.source.alternateValue} |
| Alternate scalar RI | ${alternateMeasuredRi} |
| Tolerance | ${tolerance} |

Primary source URL: ${target.source.primaryUrl}

## Frozen Candidate Results

${table(
  [
    'Candidate family',
    'Status',
    'Predicted RI',
    'Primary measured RI',
    'Primary error',
    'Primary pass',
    'Alternate measured RI',
    'Alternate error',
    'Alternate pass',
  ],
  results.map((row) => [
    row.name,
    row.status,
    row.predictedRi,
    row.measuredRi,
    row.primaryError,
    row.primaryPass ? 'yes' : 'no',
    row.alternateMeasuredRi,
    row.alternateError,
    row.alternatePass ? 'yes' : 'no',
  ])
)}

## Status

${status}.

## Reading

Hardystonite is a strong next test because it keeps the melilite Ca scaffold and removes both tetrahedral Al and Mg. If a frozen Ca-scaffold family passes without a Zn term, the Ca scaffold split has real transfer value inside the melilite family. If it fails, the repair remains local to gehlenite/akermanite and probably needs explicit T1 cation polarizability or topology-class handling.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('external-ri-hardystonite-ca-scaffold-validation.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('external-ri-hardystonite-ca-scaffold-validation.md', outDir), markdown);

console.log(markdown);
