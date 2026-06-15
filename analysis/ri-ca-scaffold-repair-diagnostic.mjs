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

const rows = [
  {
    formula: 'SiO2',
    material: 'fused silica',
    role: 'baseline training row',
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
    role: 'modifier/NBO training row',
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
    role: 'Na feldspar training row',
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
    role: 'Ca feldspar training row',
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
    role: 'K feldspar prior held-out row',
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
    role: 'feldspathoid prior failed row',
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
    role: 'paper-backed melilite failure row',
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
    role: 'source-qualified melilite failure row',
    topologyClass: 'melilite sorosilicate',
    composition: { Ca: 2, Mg: 1, Si: 2, O: 7 },
    density: 2.944,
    measuredRi: 1.63467,
    chargeBalancedAlO: 0,
    cationDelta: cfs.Ca.delta,
  },
];

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
    isMelilite: row.topologyClass === 'melilite sorosilicate' ? 1 : 0,
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

const decoratedRows = rows.map(decorate);

const diagnosticFamilies = [
  {
    name: 'baseline density + Al/O + Al-comp response',
    status: 'reference family before scaffold split',
    labels: ['intercept', 'density', 'Al/O', 'alCompResponse/O'],
    row: (row) => [1, row.density, row.chargeBalancedAlO, row.alCompensationResponseO],
  },
  {
    name: 'split Ca scaffold family',
    status: 'post-failure diagnostic; includes Ca scaffold after melilite failures',
    labels: ['intercept', 'density', 'Al/O', 'alCompResponse/O', 'Ca/O'],
    row: (row) => [1, row.density, row.chargeBalancedAlO, row.alCompensationResponseO, row.caScaffoldO],
  },
  {
    name: 'split Ca/Mg scaffold family',
    status: 'post-failure diagnostic; tests whether Mg-bearing akermanite needs separate scaffold role',
    labels: ['intercept', 'density', 'Al/O', 'alCompResponse/O', 'Ca/O', 'Mg/O'],
    row: (row) => [1, row.density, row.chargeBalancedAlO, row.alCompensationResponseO, row.caScaffoldO, row.mgScaffoldO],
  },
];

const familyResults = diagnosticFamilies.map((family) => {
  const coefficients = leastSquares(
    decoratedRows.map(family.row),
    decoratedRows.map((row) => llFromN(row.measuredRi))
  );
  const rowResults = decoratedRows.map((row) => {
    const predictedLl = family.row(row).reduce((sum, value, index) => sum + value * coefficients[index], 0);
    const predictedRi = round(nFromLl(predictedLl));
    return {
      formula: row.formula,
      material: row.material,
      role: row.role,
      measuredRi: row.measuredRi,
      predictedRi,
      residual: round(row.measuredRi - predictedRi),
    };
  });
  return {
    name: family.name,
    status: family.status,
    coefficients: Object.fromEntries(family.labels.map((label, index) => [label, round(coefficients[index], 8)])),
    maxAbsResidual: round(Math.max(...rowResults.map((row) => Math.abs(row.residual)))),
    meliliteResiduals: rowResults.filter((row) => ['Ca2Al2SiO7', 'Ca2MgSi2O7'].includes(row.formula)),
    rowResults,
  };
});

const report = {
  source: 'ri-ca-scaffold-repair-diagnostic.mjs',
  status: 'post-failure repair diagnostic only; no validation promoted',
  rows: decoratedRows,
  familyResults,
  nextValidationNeed:
    'If a scaffold split is adopted, reserve a new Ca-rich non-melilite or melilite-series target before scoring. Do not treat gehlenite/akermanite improvements as validation.',
};

function table(headers, bodyRows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...bodyRows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const markdown = `# RI Ca-Scaffold Repair Diagnostic

## Scope

This is a post-failure diagnostic only. It tests whether splitting Al charge-compensation response from non-tetrahedral Ca/Mg scaffold response can account for the melilite failures. Because the split is introduced after gehlenite and akermanite failures, any improvement is calibration debt, not validation.

## Family Summary

${table(
  ['Family', 'Status', 'Coefficients', 'Max abs residual', 'Gehlenite residual', 'Akermanite residual'],
  familyResults.map((family) => [
    family.name,
    family.status,
    Object.entries(family.coefficients)
      .map(([key, value]) => `${key}: ${value}`)
      .join('; '),
    family.maxAbsResidual,
    family.meliliteResiduals.find((row) => row.formula === 'Ca2Al2SiO7').residual,
    family.meliliteResiduals.find((row) => row.formula === 'Ca2MgSi2O7').residual,
  ])
)}

## Row Results

${familyResults
  .map(
    (family) => `### ${family.name}

${table(
  ['Formula', 'Material', 'Measured RI', 'Predicted RI', 'Residual', 'Role'],
  family.rowResults.map((row) => [
    row.formula,
    row.material,
    row.measuredRi,
    row.predictedRi,
    row.residual,
    row.role,
  ])
)}
`
  )
  .join('\n')}

## Reading

If adding Ca/O sharply reduces melilite residuals while preserving older rows, the failure diagnosis is coherent: the old cation-response variable was typed too narrowly as Al charge compensation. If Ca/O improves gehlenite but not akermanite, Mg-bearing scaffold role remains separate. If Ca/O and Mg/O both improve current rows, the next validation must be a new reserved target because the diagnostic used the failures it explains.

Do not promote this repair without a fresh target. The strongest next target would isolate scaffold role from topology, for example a Ca-rich non-melilite silicate or another melilite-series member with a stronger source than Webmineral snippets.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-ca-scaffold-repair-diagnostic.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('ri-ca-scaffold-repair-diagnostic.md', outDir), markdown);

console.log(markdown);
