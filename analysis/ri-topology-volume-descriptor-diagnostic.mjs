import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const atomicMass = {
  O: 15.999,
  Na: 22.98976928,
  Mg: 24.305,
  Al: 26.9815385,
  Si: 28.085,
  K: 39.0983,
  Ca: 40.078,
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
    topologyClass: 'polymerized glass network',
    composition: { Si: 1, O: 2 },
    density: 2.203,
    densitySource: 'Crystran fused silica material data sheet',
    measuredRefractiveIndex: 1.45704,
    nboT: 0,
    chargeBalancedAlO: 0,
    cationDelta: 0,
    role: 'exposed baseline',
  },
  {
    formula: 'Na2SiO3',
    material: 'sodium silicate glass',
    topologyClass: 'depolymerized metasilicate glass',
    composition: { Na: 2, Si: 1, O: 3 },
    density: 2.614,
    densitySource: 'PubChem sodium silicate HSDB/Merck Index anhydrous density',
    measuredRefractiveIndex: 1.52,
    nboT: 2,
    chargeBalancedAlO: 0,
    cationDelta: 0,
    role: 'exposed modifier/NBO row',
  },
  {
    formula: 'NaAlSi3O8',
    material: 'albite',
    topologyClass: 'feldspar framework',
    composition: { Na: 1, Al: 1, Si: 3, O: 8 },
    density: midpoint([2.6, 2.65]),
    densitySource: 'Mindat albite specific gravity range',
    measuredRefractiveIndex: 1.53493,
    nboT: 0,
    chargeBalancedAlO: 1 / 8,
    cationDelta: cfs.Na.delta,
    role: 'exposed Na feldspar framework',
  },
  {
    formula: 'CaAl2Si2O8',
    material: 'anorthite',
    topologyClass: 'feldspar framework',
    composition: { Ca: 1, Al: 2, Si: 2, O: 8 },
    density: midpoint([2.74, 2.76]),
    densitySource: 'Mindat anorthite specific gravity range',
    measuredRefractiveIndex: 1.58167,
    nboT: 0,
    chargeBalancedAlO: 2 / 8,
    cationDelta: cfs.Ca.delta,
    role: 'exposed Ca feldspar framework',
  },
  {
    formula: 'KAlSi3O8',
    material: 'orthoclase',
    topologyClass: 'feldspar framework',
    composition: { K: 1, Al: 1, Si: 3, O: 8 },
    density: midpoint([2.55, 2.63]),
    densitySource: 'Mindat orthoclase specific gravity range',
    measuredRefractiveIndex: 1.52183,
    nboT: 0,
    chargeBalancedAlO: 1 / 8,
    cationDelta: cfs.K.delta,
    role: 'prior held-out K feldspar framework',
  },
  {
    formula: 'KAlSiO4',
    material: 'kalsilite',
    topologyClass: 'feldspathoid framework',
    composition: { K: 1, Al: 1, Si: 1, O: 4 },
    density: midpoint([2.59, 2.62]),
    densitySource: 'Mindat kalsilite measured density range',
    measuredRefractiveIndex: 1.5375,
    nboT: 0,
    chargeBalancedAlO: 1 / 4,
    cationDelta: cfs.K.delta,
    role: 'known failed feldspathoid transfer',
  },
  {
    formula: 'Ca2Al2SiO7',
    material: 'gehlenite',
    topologyClass: 'sorosilicate',
    composition: { Ca: 2, Al: 2, Si: 1, O: 7 },
    density: 2.97714,
    densitySource: 'CatalystHub/Materials Project Ca2Al2SiO7 structure density',
    measuredRefractiveIndex: null,
    nboT: 2 / 3,
    chargeBalancedAlO: 2 / 7,
    cationDelta: cfs.Ca.delta,
    role: 'pre-RI descriptor preview only',
  },
];

function midpoint([low, high]) {
  return (low + high) / 2;
}

function round(value, places = 5) {
  return Number(value.toFixed(places));
}

function llFromN(n) {
  return (n ** 2 - 1) / (n ** 2 + 2);
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

function descriptors(row) {
  const mass = molarMass(row.composition);
  const molarVolume = mass / row.density;
  const oxygen = count(row, 'O');
  const tCations = tetrahedralCations(row);
  const ll = row.measuredRefractiveIndex ? llFromN(row.measuredRefractiveIndex) : null;
  return {
    ...row,
    molarMass: round(mass, 5),
    molarVolume: round(molarVolume, 5),
    oxygenVolume: round(molarVolume / oxygen, 5),
    tetrahedralVolume: round(molarVolume / tCations, 5),
    oxygenPackingDensity: round(oxygen / molarVolume, 5),
    tetrahedralPackingDensity: round(tCations / molarVolume, 5),
    cationResponseO: round(cationResponseO(row), 6),
    lorentzLorenz: ll === null ? null : round(ll, 6),
    molarRefraction: ll === null ? null : round(ll * molarVolume, 5),
    oxygenRefraction: ll === null ? null : round((ll * molarVolume) / oxygen, 5),
  };
}

function mean(values) {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function correlation(left, right) {
  const pairs = left.map((value, index) => [value, right[index]]).filter(([a, b]) => a !== null && b !== null);
  const leftValues = pairs.map(([value]) => value);
  const rightValues = pairs.map(([, value]) => value);
  const leftMean = mean(leftValues);
  const rightMean = mean(rightValues);
  const numerator = leftValues.reduce((sum, value, index) => sum + (value - leftMean) * (rightValues[index] - rightMean), 0);
  const denominator = Math.sqrt(
    leftValues.reduce((sum, value) => sum + (value - leftMean) ** 2, 0) *
      rightValues.reduce((sum, value) => sum + (value - rightMean) ** 2, 0)
  );
  return denominator === 0 ? null : round(numerator / denominator, 6);
}

function transpose(matrix) {
  return matrix[0].map((_, columnIndex) => matrix.map((row) => row[columnIndex]));
}

function multiply(a, b) {
  return a.map((row) => b[0].map((_, j) => row.reduce((sum, value, k) => sum + value * b[k][j], 0)));
}

function jacobiEigenvaluesSymmetric(input) {
  const matrix = input.map((row) => [...row]);
  const n = matrix.length;
  for (let sweep = 0; sweep < 100; sweep += 1) {
    let p = 0;
    let q = 1;
    let max = Math.abs(matrix[p][q]);
    for (let i = 0; i < n; i += 1) {
      for (let j = i + 1; j < n; j += 1) {
        const value = Math.abs(matrix[i][j]);
        if (value > max) {
          max = value;
          p = i;
          q = j;
        }
      }
    }
    if (max < 1e-12) break;
    const theta = (matrix[q][q] - matrix[p][p]) / (2 * matrix[p][q]);
    const t = Math.sign(theta || 1) / (Math.abs(theta) + Math.sqrt(theta ** 2 + 1));
    const c = 1 / Math.sqrt(t ** 2 + 1);
    const s = t * c;
    const app = matrix[p][p];
    const aqq = matrix[q][q];
    const apq = matrix[p][q];
    matrix[p][p] = c ** 2 * app - 2 * s * c * apq + s ** 2 * aqq;
    matrix[q][q] = s ** 2 * app + 2 * s * c * apq + c ** 2 * aqq;
    matrix[p][q] = 0;
    matrix[q][p] = 0;
    for (let r = 0; r < n; r += 1) {
      if (r === p || r === q) continue;
      const arp = matrix[r][p];
      const arq = matrix[r][q];
      matrix[r][p] = c * arp - s * arq;
      matrix[p][r] = matrix[r][p];
      matrix[r][q] = s * arp + c * arq;
      matrix[q][r] = matrix[r][q];
    }
  }
  return matrix.map((row, i) => row[i]).sort((a, b) => a - b);
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

function conditionNumber(x) {
  const xtx = multiply(transpose(x), x);
  const eigenvalues = jacobiEigenvaluesSymmetric(xtx).filter((value) => value > 1e-12);
  return Math.sqrt(eigenvalues[eigenvalues.length - 1] / eigenvalues[0]);
}

function standardizedMatrix(matrix) {
  const columns = transpose(matrix);
  const standardizedColumns = columns.map((column, index) => {
    if (index === 0 && column.every((value) => value === 1)) return column;
    const columnMean = mean(column);
    const variance = mean(column.map((value) => (value - columnMean) ** 2));
    const sd = Math.sqrt(variance);
    if (sd === 0) return column.map(() => 0);
    return column.map((value) => (value - columnMean) / sd);
  });
  return transpose(standardizedColumns);
}

const descriptorRows = rows.map(descriptors);
const measuredRows = descriptorRows.filter((row) => row.measuredRefractiveIndex !== null);

const descriptorCorrelations = {
  molarVolumeVsRi: correlation(
    measuredRows.map((row) => row.molarVolume),
    measuredRows.map((row) => row.measuredRefractiveIndex)
  ),
  oxygenVolumeVsRi: correlation(
    measuredRows.map((row) => row.oxygenVolume),
    measuredRows.map((row) => row.measuredRefractiveIndex)
  ),
  tetrahedralPackingDensityVsRi: correlation(
    measuredRows.map((row) => row.tetrahedralPackingDensity),
    measuredRows.map((row) => row.measuredRefractiveIndex)
  ),
  chargeBalancedAlOVsRi: correlation(
    measuredRows.map((row) => row.chargeBalancedAlO),
    measuredRows.map((row) => row.measuredRefractiveIndex)
  ),
  cationResponseOVsRi: correlation(
    measuredRows.map((row) => row.cationResponseO),
    measuredRows.map((row) => row.measuredRefractiveIndex)
  ),
  molarVolumeVsAlO: correlation(
    measuredRows.map((row) => row.molarVolume),
    measuredRows.map((row) => row.chargeBalancedAlO)
  ),
  oxygenVolumeVsCationResponseO: correlation(
    measuredRows.map((row) => row.oxygenVolume),
    measuredRows.map((row) => row.cationResponseO)
  ),
};

function groupByTopology() {
  const groups = new Map();
  for (const row of descriptorRows) {
    if (!groups.has(row.topologyClass)) groups.set(row.topologyClass, []);
    groups.get(row.topologyClass).push(row);
  }
  return [...groups.entries()].map(([topologyClass, groupRows]) => ({
    topologyClass,
    formulas: groupRows.map((row) => row.formula),
    measuredCount: groupRows.filter((row) => row.measuredRefractiveIndex !== null).length,
    meanOxygenVolume: round(mean(groupRows.map((row) => row.oxygenVolume))),
    meanTetrahedralPackingDensity: round(mean(groupRows.map((row) => row.tetrahedralPackingDensity))),
    meanOxygenRefraction:
      groupRows.some((row) => row.oxygenRefraction !== null)
        ? round(mean(groupRows.filter((row) => row.oxygenRefraction !== null).map((row) => row.oxygenRefraction)))
        : null,
  }));
}

const topologyGroups = groupByTopology();

const featureSets = [
  {
    name: 'current density/Al/cation-response family',
    labels: ['intercept', 'density', 'Al/O', 'cationResponse/O'],
    row: (row) => [1, row.density, row.chargeBalancedAlO, row.cationResponseO],
  },
  {
    name: 'oxygen-volume/Al/cation-response family',
    labels: ['intercept', 'oxygenVolume', 'Al/O', 'cationResponse/O'],
    row: (row) => [1, row.oxygenVolume, row.chargeBalancedAlO, row.cationResponseO],
  },
  {
    name: 'T-packing/Al/cation-response family',
    labels: ['intercept', 'tetrahedralPackingDensity', 'Al/O', 'cationResponse/O'],
    row: (row) => [1, row.tetrahedralPackingDensity, row.chargeBalancedAlO, row.cationResponseO],
  },
  {
    name: 'oxygen-volume plus topology flags',
    labels: ['intercept', 'oxygenVolume', 'Al/O', 'cationResponse/O', 'isFeldspar', 'isGlass'],
    row: (row) => [
      1,
      row.oxygenVolume,
      row.chargeBalancedAlO,
      row.cationResponseO,
      row.topologyClass === 'feldspar framework' ? 1 : 0,
      row.topologyClass.includes('glass') ? 1 : 0,
    ],
  },
  {
    name: 'minimal packing family',
    labels: ['intercept', 'oxygenVolume', 'cationResponse/O'],
    row: (row) => [1, row.oxygenVolume, row.cationResponseO],
  },
  {
    name: 'minimal charge-packing family',
    labels: ['intercept', 'oxygenVolume', 'Al/O'],
    row: (row) => [1, row.oxygenVolume, row.chargeBalancedAlO],
  },
];

const featureSetDiagnostics = featureSets.map((featureSet) => {
  const matrix = measuredRows.map(featureSet.row);
  const condition =
    matrix.length > featureSet.labels.length
      ? round(conditionNumber(matrix), 4)
      : null;
  const standardizedCondition =
    matrix.length > featureSet.labels.length
      ? round(conditionNumber(standardizedMatrix(matrix)), 4)
      : null;
  return {
    name: featureSet.name,
    labels: featureSet.labels,
    measuredRows: matrix.length,
    featureCount: featureSet.labels.length,
    condition,
    standardizedCondition,
    guardrail:
      standardizedCondition === null
        ? 'blocked: not enough measured rows for feature count'
        : standardizedCondition <= 30
          ? 'passes condition guardrail'
          : 'blocked: condition guardrail',
  };
});

const coefficientDiagnostics = featureSets.map((featureSet) => {
  const matrix = measuredRows.map(featureSet.row);
  if (matrix.length <= featureSet.labels.length) {
    return {
      name: featureSet.name,
      status: 'not fit: not enough measured rows for feature count',
      coefficients: null,
      maxAbsResidualLl: null,
      signPattern: null,
    };
  }
  const target = measuredRows.map((row) => row.lorentzLorenz);
  const coefficients = leastSquares(matrix, target);
  const predictions = matrix.map((featureRow) =>
    featureRow.reduce((sum, value, index) => sum + value * coefficients[index], 0)
  );
  const residuals = predictions.map((prediction, index) => prediction - target[index]);
  const coefficientMap = Object.fromEntries(
    featureSet.labels.map((label, index) => [label, round(coefficients[index], 8)])
  );
  return {
    name: featureSet.name,
    status: 'fit on current measured corpus only; not validation',
    coefficients: coefficientMap,
    maxAbsResidualLl: round(Math.max(...residuals.map((value) => Math.abs(value))), 8),
    signPattern: Object.fromEntries(
      Object.entries(coefficientMap).map(([label, value]) => [
        label,
        value > 0 ? 'positive' : value < 0 ? 'negative' : 'zero',
      ])
    ),
  };
});

const descriptorWarnings = [
  'Topology class is categorical and under-sampled; do not fit one coefficient per class from this table.',
  'Molar refraction and oxygen refraction use measured RI and are diagnostic only, not predictor inputs before a fresh target.',
  'Gehlenite is descriptor-preview only; no RI target is included in this diagnostic.',
  'The feldspathoid row remains a known failed transfer, not a clean validation row for a feldspar-fit term.',
];

const json = {
  source: 'ri-topology-volume-descriptor-diagnostic.mjs',
  status: 'descriptor diagnostic only; no benchmark score changed',
  descriptorRows,
  descriptorCorrelations,
  topologyGroups,
  featureSetDiagnostics,
  coefficientDiagnostics,
  descriptorWarnings,
};

function table(headers, bodyRows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...bodyRows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const markdown = `# RI Topology/Volume Descriptor Diagnostic

## Scope

This is a diagnostic companion to the measured refractive-index blocker. It does not promote a new predictor, change benchmark status, or score a fresh held-out RI target.

It translates the lateral "invisible origami" pattern into scientific descriptors:

- folded compactness -> density, molar volume, oxygen volume, tetrahedral packing density
- polarizable packing -> Lorentz-Lorenz value, molar refraction, oxygen refraction
- framework crease density -> charge-balanced Al/O
- modifier response -> cation field-strength response per oxygen
- fold family -> topology class

## Descriptor Table

${table(
  [
    'Formula',
    'Topology class',
    'Role',
    'Density',
    'Molar volume',
    'O volume',
    'T packing density',
    'Al/O',
    'Cation response/O',
    'Measured RI',
    'Molar refraction',
    'O refraction',
  ],
  descriptorRows.map((row) => [
    row.formula,
    row.topologyClass,
    row.role,
    row.density,
    row.molarVolume,
    row.oxygenVolume,
    row.tetrahedralPackingDensity,
    round(row.chargeBalancedAlO, 6),
    row.cationResponseO,
    row.measuredRefractiveIndex ?? 'not looked up',
    row.molarRefraction ?? 'n/a',
    row.oxygenRefraction ?? 'n/a',
  ])
)}

## Descriptor Correlations

These correlations are exploratory and use only rows with measured RI already present in the current corpus.

${table(
  ['Descriptor pair', 'Correlation'],
  Object.entries(descriptorCorrelations).map(([key, value]) => [key, value])
)}

## Topology Groups

${table(
  ['Topology class', 'Rows', 'Measured rows', 'Mean O volume', 'Mean T packing density', 'Mean O refraction'],
  topologyGroups.map((group) => [
    group.topologyClass,
    group.formulas.join(', '),
    group.measuredCount,
    group.meanOxygenVolume,
    group.meanTetrahedralPackingDensity,
    group.meanOxygenRefraction ?? 'n/a',
  ])
)}

## Feature-Set Guardrails

These are design diagnostics only. They ask whether candidate descriptor families are numerically separable enough to consider before any new RI target is scored.

${table(
  ['Feature set', 'Features', 'Measured rows', 'Feature count', 'Raw condition', 'Standardized condition', 'Guardrail'],
  featureSetDiagnostics.map((row) => [
    row.name,
    row.labels.join(', '),
    row.measuredRows,
    row.featureCount,
    row.condition ?? 'n/a',
    row.standardizedCondition ?? 'n/a',
    row.guardrail,
  ])
)}

## Current-Corpus Coefficient Diagnostics

These coefficients are fit only to the currently exposed measured corpus and are not validation. They are recorded before any future fresh RI target is selected so coefficient signs and magnitudes cannot be silently adjusted after lookup.

${table(
  ['Feature set', 'Status', 'Coefficients', 'Max abs LL residual', 'Sign pattern'],
  coefficientDiagnostics.map((row) => [
    row.name,
    row.status,
    row.coefficients
      ? Object.entries(row.coefficients)
          .map(([key, value]) => `${key}: ${value}`)
          .join('; ')
      : 'n/a',
    row.maxAbsResidualLl ?? 'n/a',
    row.signPattern
      ? Object.entries(row.signPattern)
          .map(([key, value]) => `${key}: ${value}`)
          .join('; ')
      : 'n/a',
  ])
)}

## Warnings

${descriptorWarnings.map((warning) => `- ${warning}`).join('\n')}

## Reading

The current RI failures are consistent with a missing packed-framework descriptor. NBO/T and Al charge balance describe crease count and charge closure, but not how the framework is folded into volume or how modifier cations alter polarizable packing. Molar volume and oxygen-volume descriptors make that missing physical embedding explicit.

The table also warns against premature fitting: topology classes are sparse, and molar refraction is target-derived wherever measured RI is already known. The next valid use is to choose exposed calibration rows that reduce descriptor degeneracy before freezing any new equation. A fresh RI target should be scored only after the descriptor design is well-conditioned and the topology class is declared.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-topology-volume-descriptor-diagnostic.json', outDir), JSON.stringify(json, null, 2));
await writeFile(new URL('ri-topology-volume-descriptor-diagnostic.md', outDir), markdown);

console.log(markdown);
