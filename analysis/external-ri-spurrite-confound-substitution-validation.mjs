import { readFile, mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const reservationReport = JSON.parse(
  await readFile(new URL('./out/ri-post-merwinite-target-reservation-diagnostic.json', import.meta.url))
);

const atomicMass = {
  C: 12.011,
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
  formula: 'Ca5(SiO4)2(CO3)',
  material: 'spurrite',
  topologyClass: reserved.topologyClass,
  compositionClass: reserved.compositionClass,
  composition: { Ca: 5, Si: 2, C: 1, O: 11 },
  density: reserved.densityForFutureScoring,
  measuredRi: 1.663833,
  scalarRiRange: reserved.scalarRiRange,
  chargeBalancedAlO: 0,
  cationDelta: cfs.Ca.delta,
  source: {
    primaryLabel: reserved.opticalSource.label,
    primaryUrl: reserved.opticalSource.url,
    primaryValue: reserved.opticalSource.value,
    cifUrl: reserved.cifSource.url,
    limitation: 'Mg-removed but carbonate-introduced Ca-rich silicate-carbonate control contrast',
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
    carbonateO: count(row, 'C') / oxygen,
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
    status: 'reference family before scaffold split; no carbonate descriptor',
    labels: ['intercept', 'density', 'Al/O', 'alCompResponse/O'],
    row: (row) => [1, row.density, row.chargeBalancedAlO, row.alCompensationResponseO],
  },
  {
    name: 'split Ca scaffold family',
    status: 'post-failure Ca scaffold family; no spurrite/carbonate term',
    labels: ['intercept', 'density', 'Al/O', 'alCompResponse/O', 'Ca/O'],
    row: (row) => [1, row.density, row.chargeBalancedAlO, row.alCompensationResponseO, row.caScaffoldO],
  },
  {
    name: 'split Ca/Mg scaffold family',
    status: 'post-failure Ca/Mg scaffold family; Mg/O is zero for spurrite',
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

const status = splitCa.midpointPass
  ? 'spurrite split-Ca passes under carbonate limitation; not promotable'
  : 'spurrite split-Ca fails under carbonate limitation; merwinite pass remains Mg/topology-confounded';

const report = {
  source: 'external-ri-spurrite-confound-substitution-validation.mjs',
  status,
  tolerance,
  target: decoratedTarget,
  reservationBoundary: reservationReport.lockedPreScoreExpectations,
  results,
  interpretation:
    'Spurrite removes Mg but introduces carbonate. Pass/fail results are control-contrast evidence only and cannot promote split-Ca or split-Ca/Mg as clean Ca-Si-O material-property validation.',
};

const reading = splitCa.midpointPass
  ? 'Spurrite passes the split-Ca family with Mg/O equal to zero, but carbonate has been introduced. This weakens the claim that merwinite was only an Mg artifact, yet still cannot promote the model as pure Ca-Si-O validation.'
  : 'Spurrite fails the split-Ca family, so the merwinite split-Ca pass remains Mg/topology-confounded. Carbonate prevents treating the failure as a clean Ca-Si-O falsifier.';

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

const markdown = `# RI Spurrite Confound-Substitution Validation

## Scope

This validation scores reserved spurrite after the post-merwinite reservation and wollastonite source-lock screen. It uses the same frozen baseline, split-Ca, and split-Ca/Mg families. No coefficient, threshold, density handling, or carbonate descriptor is added.

Spurrite removes the merwinite Mg confound but introduces carbonate, so this is a Mg-removed/carbonate-introduced control contrast rather than clean Ca-Si-O validation.

## Target

${table(
  ['Field', 'Value'],
  [
    ['Formula', target.formula],
    ['Material', target.material],
    ['Topology class', target.topologyClass],
    ['Composition class', target.compositionClass],
    ['Density used', target.density],
    ['Ca/O', round(decoratedTarget.caScaffoldO)],
    ['Mg/O', round(decoratedTarget.mgScaffoldO)],
    ['C/O', round(decoratedTarget.carbonateO)],
    ['Oxygen volume', round(decoratedTarget.oxygenVolume)],
    ['Scalar RI range', target.scalarRiRange.join('-')],
    ['Scalar RI midpoint', target.measuredRi],
    ['Optical source', target.source.primaryLabel],
    ['CIF URL', target.source.cifUrl],
    ['Limitation', target.source.limitation],
  ],
)}

## Frozen Candidate Results

${table(
  ['Candidate family', 'Status', 'Predicted RI', 'Measured midpoint', 'Scalar RI range', 'Error', 'Midpoint pass', 'Range pass', 'Residual', 'Coefficients'],
  results.map((row) => [
    row.name,
    row.status,
    row.predictedRi,
    row.measuredRi,
    row.scalarRiRange.join('-'),
    row.primaryError,
    row.midpointPass ? 'yes' : 'no',
    row.rangePass ? 'yes' : 'no',
    row.residual,
    coefficients(row),
  ]),
)}

## Result Contrast

${table(
  ['Family', 'Predicted RI', 'Error', 'Pass', 'Reading'],
  [
    [
      baseline.name,
      baseline.predictedRi,
      baseline.primaryError,
      baseline.midpointPass ? 'yes' : 'no',
      baseline.midpointPass ? 'density baseline passes this carbonate row' : 'density baseline misses this carbonate row',
    ],
    [
      splitCa.name,
      splitCa.predictedRi,
      splitCa.primaryError,
      splitCa.midpointPass ? 'yes' : 'no',
      splitCa.midpointPass ? 'Ca scaffold family passes despite carbonate confound' : 'Ca scaffold family still fails after Mg removal',
    ],
    [
      splitCaMg.name,
      splitCaMg.predictedRi,
      splitCaMg.primaryError,
      splitCaMg.midpointPass ? 'yes' : 'no',
      splitCaMg.midpointPass ? 'Mg/O is zero, so this collapses to Ca-family behavior under the fitted Mg coefficient' : 'Mg/O is zero and family still misses',
    ],
  ],
)}

Status:

\`\`\`text
${status}
\`\`\`

Reading:

${reading}

Important boundary:

- do not call this pure Ca-Si-O validation;
- do not promote split-Ca or split-Ca/Mg from this row;
- use the result only as a control contrast after merwinite;
- the clean Ca-Si-O path remains blocked until a polytype-specific wollastonite optical/density row is source-locked.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('external-ri-spurrite-confound-substitution-validation.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('external-ri-spurrite-confound-substitution-validation.md', outDir), markdown);

console.log(markdown);
