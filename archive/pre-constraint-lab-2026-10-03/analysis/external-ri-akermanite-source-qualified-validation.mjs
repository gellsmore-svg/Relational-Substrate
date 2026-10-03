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
    composition: { Si: 1, O: 2 },
    density: 2.203,
    measuredRefractiveIndex: 1.45704,
    chargeBalancedAlO: 0,
    cationDelta: 0,
  },
  {
    formula: 'Na2SiO3',
    material: 'sodium silicate glass',
    composition: { Na: 2, Si: 1, O: 3 },
    density: 2.614,
    measuredRefractiveIndex: 1.52,
    chargeBalancedAlO: 0,
    cationDelta: 0,
  },
  {
    formula: 'NaAlSi3O8',
    material: 'albite',
    composition: { Na: 1, Al: 1, Si: 3, O: 8 },
    density: 2.625,
    measuredRefractiveIndex: 1.53493,
    chargeBalancedAlO: 1 / 8,
    cationDelta: cfs.Na.delta,
  },
  {
    formula: 'CaAl2Si2O8',
    material: 'anorthite',
    composition: { Ca: 1, Al: 2, Si: 2, O: 8 },
    density: 2.75,
    measuredRefractiveIndex: 1.58167,
    chargeBalancedAlO: 2 / 8,
    cationDelta: cfs.Ca.delta,
  },
  {
    formula: 'KAlSi3O8',
    material: 'orthoclase',
    composition: { K: 1, Al: 1, Si: 3, O: 8 },
    density: 2.59,
    measuredRefractiveIndex: 1.52183,
    chargeBalancedAlO: 1 / 8,
    cationDelta: cfs.K.delta,
  },
  {
    formula: 'KAlSiO4',
    material: 'kalsilite',
    composition: { K: 1, Al: 1, Si: 1, O: 4 },
    density: 2.605,
    measuredRefractiveIndex: 1.5375,
    chargeBalancedAlO: 1 / 4,
    cationDelta: cfs.K.delta,
  },
];

const target = {
  formula: 'Ca2MgSi2O7',
  material: 'akermanite',
  topologyClass: 'melilite sorosilicate',
  composition: { Ca: 2, Mg: 1, Si: 2, O: 7 },
  density: 2.944,
  chargeBalancedAlO: 0,
  cationDelta: cfs.Ca.delta,
  source: {
    label: 'Webmineral, Akermanite Mineral Data',
    url: 'https://webmineral.com/data/Akermanite.shtml',
    sourceValue: 'Lists density 2.944 and optical data w = 1.632, e = 1.64.',
    sourceLimit:
      'Mineral database source; wavelength and uncertainty are not specified, so this is source-qualified rather than primary dispersion-grade validation.',
  },
  ordinaryIndex: 1.632,
  extraordinaryIndex: 1.64,
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

function molarMass(composition) {
  return Object.entries(composition).reduce((sum, [element, count]) => sum + atomicMass[element] * count, 0);
}

function count(row, element) {
  return row.composition[element] ?? 0;
}

function tetrahedralCations(row) {
  return count(row, 'Si') + count(row, 'Al') + count(row, 'Mg');
}

function cationResponseO(row) {
  return row.chargeBalancedAlO * row.cationDelta;
}

function decorate(row) {
  const molarVolume = molarMass(row.composition) / row.density;
  return {
    ...row,
    oxygenVolume: molarVolume / count(row, 'O'),
    tetrahedralPackingDensity: tetrahedralCations(row) / molarVolume,
    cationResponseO: cationResponseO(row),
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
    row: (row) => [1, row.density, row.chargeBalancedAlO, row.cationResponseO],
  },
  {
    name: 'minimal oxygen-volume + Al/O',
    labels: ['intercept', 'oxygenVolume', 'Al/O'],
    row: (row) => [1, row.oxygenVolume, row.chargeBalancedAlO],
  },
];

const training = trainingRows.map(decorate);
const decoratedTarget = decorate(target);
const measuredTargetRi = round((2 * target.ordinaryIndex + target.extraordinaryIndex) / 3, 5);

const results = featureFamilies.map((family) => {
  const coefficients = leastSquares(
    training.map(family.row),
    training.map((row) => llFromN(row.measuredRefractiveIndex))
  );
  const predictedLl = family
    .row(decoratedTarget)
    .reduce((sum, value, index) => sum + value * coefficients[index], 0);
  const predictedRi = round(nFromLl(predictedLl), 5);
  const absoluteError = round(Math.abs(predictedRi - measuredTargetRi), 5);
  return {
    name: family.name,
    coefficients: Object.fromEntries(family.labels.map((label, index) => [label, round(coefficients[index], 8)])),
    predictedRi,
    measuredTargetRi,
    absoluteError,
    pass: absoluteError <= tolerance,
  };
});

const status = results.some((row) => row.pass)
  ? 'source-qualified akermanite validation has at least one candidate pass'
  : 'source-qualified akermanite validation failed both frozen candidate families';

const report = {
  source: 'external-ri-akermanite-source-qualified-validation.mjs',
  status,
  tolerance,
  sourceQualification: target.source.sourceLimit,
  target: {
    ...decoratedTarget,
    measuredTargetRi,
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

const markdown = `# Source-Qualified RI Validation: Akermanite

## Scope

This report scores akermanite as a source-qualified melilite-family target using a mineral database RI table. It is not as strong as the gehlenite paper-backed validation because wavelength and uncertainty are not specified.

## Target

| Measure | Value |
|---|---|
| Formula | ${target.formula} |
| Material | ${target.material} |
| Topology class | ${target.topologyClass} |
| Density | ${target.density} |
| Source | ${target.source.label} |
| Source value | ${target.source.sourceValue} |
| Source limit | ${target.source.sourceLimit} |
| Scalar measured RI | ${measuredTargetRi} |
| Tolerance | ${tolerance} |

Source URL: ${target.source.url}

## Frozen Candidate Results

${table(
  ['Candidate family', 'Coefficients', 'Predicted RI', 'Measured RI', 'Absolute error', 'Pass'],
  results.map((row) => [
    row.name,
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

## Reading

Akermanite keeps the melilite/Ca scaffold while replacing gehlenite's tetrahedral Al-rich chemistry with Mg/Si. If the frozen families miss akermanite too, the problem is broader melilite/sorosilicate transfer. If they pass akermanite while missing gehlenite, the missing descriptor is probably T-site Al role or Al-specific polarizability in the melilite scaffold.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('external-ri-akermanite-source-qualified-validation.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('external-ri-akermanite-source-qualified-validation.md', outDir), markdown);

console.log(markdown);
