import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function round(value, places = 5) {
  return Number(value.toFixed(places));
}

function llFromN(n) {
  return (n ** 2 - 1) / (n ** 2 + 2);
}

function nFromLl(ll) {
  return Math.sqrt((1 + 2 * ll) / (1 - ll));
}

function midpoint([low, high]) {
  return (low + high) / 2;
}

const constants = {
  silicaBaseline: 1.46,
  nboSlope: 0.03,
  densityReference: 2.203,
  tolerance: 0.01,
};

const cfs = {
  Na: { delta: 0 },
  K: { delta: -0.2796 },
  Ca: { delta: 0.8762 },
};

const calibrationRows = [
  {
    formula: 'SiO2',
    material: 'fused silica',
    measuredRefractiveIndex: 1.45704,
    density: 2.203,
    densitySource: 'Crystran fused silica material data sheet',
    nboT: 0,
    chargeBalancedAlO: 0,
    deltaCFS: 0,
  },
  {
    formula: 'Na2SiO3',
    material: 'sodium silicate glass',
    measuredRefractiveIndex: 1.52,
    density: 2.614,
    densitySource: 'PubChem sodium silicate HSDB/Merck Index anhydrous density',
    nboT: 2,
    chargeBalancedAlO: 0,
    deltaCFS: 0,
  },
  {
    formula: 'NaAlSi3O8',
    material: 'albite',
    measuredRefractiveIndex: 1.53493,
    density: midpoint([2.6, 2.65]),
    densitySource: 'Mindat albite specific gravity range',
    nboT: 0,
    chargeBalancedAlO: 1 / 8,
    deltaCFS: cfs.Na.delta,
  },
  {
    formula: 'CaAl2Si2O8',
    material: 'anorthite',
    measuredRefractiveIndex: 1.58167,
    density: midpoint([2.74, 2.76]),
    densitySource: 'Mindat anorthite specific gravity range',
    nboT: 0,
    chargeBalancedAlO: 2 / 8,
    deltaCFS: cfs.Ca.delta,
  },
  {
    formula: 'KAlSi3O8',
    material: 'orthoclase',
    measuredRefractiveIndex: 1.52183,
    density: midpoint([2.55, 2.63]),
    densitySource: 'Mindat orthoclase specific gravity range',
    nboT: 0,
    chargeBalancedAlO: 1 / 8,
    deltaCFS: cfs.K.delta,
  },
  {
    formula: 'KAlSiO4',
    material: 'kalsilite',
    measuredRefractiveIndex: 1.5375,
    density: midpoint([2.59, 2.62]),
    densitySource: 'Mindat kalsilite measured density range',
    nboT: 0,
    chargeBalancedAlO: 1 / 4,
    deltaCFS: cfs.K.delta,
  },
];

const heldOutRows = [
  {
    formula: 'Ca2Al2SiO7',
    material: 'gehlenite',
    measuredRefractiveIndex: null,
    density: 2.97714,
    densitySource: 'CatalystHub/Materials Project Ca2Al2SiO7 structure density',
    nboT: 2 / 3,
    chargeBalancedAlO: 2 / 7,
    deltaCFS: cfs.Ca.delta,
    role: 'primary fresh Ca-aluminosilicate sorosilicate structural transfer',
  },
];

function cationResponseO(row) {
  return row.chargeBalancedAlO * row.deltaCFS;
}

function normalizedDensity(row) {
  return row.density / constants.densityReference;
}

function llOffset(row) {
  return llFromN(constants.silicaBaseline + constants.nboSlope * row.nboT) - llFromN(constants.silicaBaseline);
}

function featureRow(row) {
  return [1, normalizedDensity(row), row.chargeBalancedAlO, cationResponseO(row)];
}

const featureSets = {
  full: {
    labels: ['b0', 'b_density', 'b_al', 'b_cfs'],
    row: (row) => [1, normalizedDensity(row), row.chargeBalancedAlO, cationResponseO(row)],
  },
  dropAl: {
    labels: ['b0', 'b_density', 'b_cfs'],
    row: (row) => [1, normalizedDensity(row), cationResponseO(row)],
  },
  dropCfs: {
    labels: ['b0', 'b_density', 'b_al'],
    row: (row) => [1, normalizedDensity(row), row.chargeBalancedAlO],
  },
  densityOnly: {
    labels: ['b0', 'b_density'],
    row: (row) => [1, normalizedDensity(row)],
  },
};

function targetLl(row) {
  return llFromN(row.measuredRefractiveIndex) - llOffset(row);
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

function correlation(left, right) {
  const meanLeft = left.reduce((sum, value) => sum + value, 0) / left.length;
  const meanRight = right.reduce((sum, value) => sum + value, 0) / right.length;
  const centeredLeft = left.map((value) => value - meanLeft);
  const centeredRight = right.map((value) => value - meanRight);
  const numerator = centeredLeft.reduce((sum, value, i) => sum + value * centeredRight[i], 0);
  const denominator = Math.sqrt(
    centeredLeft.reduce((sum, value) => sum + value ** 2, 0) *
      centeredRight.reduce((sum, value) => sum + value ** 2, 0)
  );
  return denominator === 0 ? null : numerator / denominator;
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

function conditionNumber(x) {
  const xtx = multiply(transpose(x), x);
  const eigenvalues = jacobiEigenvaluesSymmetric(xtx).filter((value) => value > 1e-12);
  return Math.sqrt(eigenvalues[eigenvalues.length - 1] / eigenvalues[0]);
}

const x = calibrationRows.map(featureRow);
const y = calibrationRows.map(targetLl);

const descriptorColumns = {
  normalizedDensity: calibrationRows.map(normalizedDensity),
  chargeBalancedAlO: calibrationRows.map((row) => row.chargeBalancedAlO),
  cationResponseO: calibrationRows.map(cationResponseO),
};

const descriptorCorrelations = {
  densityVsAl: round(correlation(descriptorColumns.normalizedDensity, descriptorColumns.chargeBalancedAlO), 6),
  densityVsCationResponse: round(correlation(descriptorColumns.normalizedDensity, descriptorColumns.cationResponseO), 6),
  alVsCationResponse: round(correlation(descriptorColumns.chargeBalancedAlO, descriptorColumns.cationResponseO), 6),
};

const condition = round(conditionNumber(x), 4);
const coefficients = leastSquares(x, y);
const coefficientMap = {
  b0: coefficients[0],
  bDensity: coefficients[1],
  bAl: coefficients[2],
  bCfs: coefficients[3],
};

function predictLl(row, options = {}) {
  const densityCoefficient = options.densityOff ? 0 : coefficientMap.bDensity;
  return (
    coefficientMap.b0 +
    densityCoefficient * normalizedDensity(row) +
    coefficientMap.bAl * row.chargeBalancedAlO +
    coefficientMap.bCfs * cationResponseO(row) +
    llOffset(row)
  );
}

function predictN(row, options = {}) {
  return round(nFromLl(predictLl(row, options)), 5);
}

const calibrationResults = calibrationRows.map((row) => {
  const predicted = predictN(row);
  return {
    ...row,
    normalizedDensity: round(normalizedDensity(row), 6),
    cationResponseO: round(cationResponseO(row), 6),
    predicted,
    residual: round(predicted - row.measuredRefractiveIndex, 6),
  };
});

const guardrailFailures = [
  Math.abs(descriptorCorrelations.densityVsAl) > 0.9 &&
    `density/Al correlation ${descriptorCorrelations.densityVsAl} exceeds 0.9`,
  Math.abs(descriptorCorrelations.densityVsCationResponse) > 0.95 &&
    `density/cation-response correlation ${descriptorCorrelations.densityVsCationResponse} exceeds 0.95`,
  Math.abs(descriptorCorrelations.alVsCationResponse) > 0.95 &&
    `Al/cation-response correlation ${descriptorCorrelations.alVsCationResponse} exceeds 0.95`,
  condition > 30 && `design matrix condition number ${condition} exceeds 30`,
  coefficientMap.bDensity <= 0 && `b_density ${coefficientMap.bDensity} is non-positive`,
  coefficientMap.bCfs <= 0 && `b_cfs ${coefficientMap.bCfs} is non-positive`,
  calibrationResults.every((row) => Math.abs(row.residual) < 1e-9) &&
    'all exposed calibration residuals are exactly zero',
].filter(Boolean);

const heldOutDescriptorPreview = heldOutRows.map((row) => ({
  formula: row.formula,
  material: row.material,
  normalizedDensity: round(normalizedDensity(row), 6),
  chargeBalancedAlO: round(row.chargeBalancedAlO, 6),
  cationResponseO: round(cationResponseO(row), 6),
  priorPerOxygenPrediction: round(
    1.46 + 0.03 * row.nboT + 0.59944 * row.chargeBalancedAlO + 0.37482117 * cationResponseO(row),
    5
  ),
  densityModelPredictionBeforeRiLookup: guardrailFailures.length ? null : predictN(row),
  densityOffPredictionBeforeRiLookup: guardrailFailures.length ? null : predictN(row, { densityOff: true }),
}));

function diagnosticsForFeatureSet([name, spec]) {
  const variantX = calibrationRows.map(spec.row);
  const variantCoefficients = leastSquares(variantX, y);
  const variantCondition = round(conditionNumber(variantX), 4);
  const predictions = calibrationRows.map((row) => {
    const ll = spec.row(row).reduce((sum, value, index) => sum + value * variantCoefficients[index], 0) + llOffset(row);
    return nFromLl(ll);
  });
  const maxAbsResidual = Math.max(
    ...predictions.map((predicted, index) => Math.abs(predicted - calibrationRows[index].measuredRefractiveIndex))
  );
  return {
    name,
    labels: spec.labels,
    condition: variantCondition,
    coefficients: Object.fromEntries(
      spec.labels.map((label, index) => [label, round(variantCoefficients[index], 8)])
    ),
    maxAbsCalibrationResidual: round(maxAbsResidual, 6),
    bDensityPositive: variantCoefficients[spec.labels.indexOf('b_density')] > 0,
    bCfsPositive: spec.labels.includes('b_cfs')
      ? variantCoefficients[spec.labels.indexOf('b_cfs')] > 0
      : null,
  };
}

const reducedModelDiagnostics = Object.entries(featureSets).map(diagnosticsForFeatureSet);

const report = `# RI Structural Descriptor Validation: Pre-Lookup Guardrails

## Status

| Measure | Value |
|---|---|
| Phase | pre-held-out-RI lookup |
| Held-out RI included | no |
| Guardrail status | ${guardrailFailures.length ? 'BLOCKED' : 'PASSED'} |

${guardrailFailures.length ? `Guardrail failures:\n\n${guardrailFailures.map((failure) => `- ${failure}`).join('\n')}` : 'All hard pre-lookup guardrails passed. Coefficients are frozen before held-out RI lookup.'}

## Descriptor Correlations

| Pair | Correlation |
|---|---:|
| normalizedDensity vs chargeBalancedAlO | ${descriptorCorrelations.densityVsAl} |
| normalizedDensity vs cationResponseO | ${descriptorCorrelations.densityVsCationResponse} |
| chargeBalancedAlO vs cationResponseO | ${descriptorCorrelations.alVsCationResponse} |
| design matrix condition number | ${condition} |

## Coefficients

| Coefficient | Value |
|---|---:|
| b0 | ${round(coefficientMap.b0, 8)} |
| b_density | ${round(coefficientMap.bDensity, 8)} |
| b_al | ${round(coefficientMap.bAl, 8)} |
| b_cfs | ${round(coefficientMap.bCfs, 8)} |

## Calibration Residuals

| Formula | Material | Density | Normalized density | Al/O | Cation response | Measured RI | Predicted RI | Residual |
|---|---|---:|---:|---:|---:|---:|---:|---:|
${calibrationResults
  .map((row) =>
    `| ${row.formula} | ${row.material} | ${row.density} | ${row.normalizedDensity} | ${round(row.chargeBalancedAlO, 6)} | ${row.cationResponseO} | ${row.measuredRefractiveIndex} | ${row.predicted} | ${row.residual} |`
  )
  .join('\n')}

## Held-Out Descriptor Preview

No held-out RI has been looked up or included.

| Formula | Material | Normalized density | Al/O | Cation response | Prior per-oxygen prediction | Density model prediction before RI lookup | Density-off prediction before RI lookup |
|---|---|---:|---:|---:|---:|---:|---:|
${heldOutDescriptorPreview
  .map((row) =>
    `| ${row.formula} | ${row.material} | ${row.normalizedDensity} | ${row.chargeBalancedAlO} | ${row.cationResponseO} | ${row.priorPerOxygenPrediction} | ${row.densityModelPredictionBeforeRiLookup ?? 'blocked'} | ${row.densityOffPredictionBeforeRiLookup ?? 'blocked'} |`
  )
  .join('\n')}

## Reduced Model Diagnostics

These diagnostics use only exposed calibration rows and do not include held-out RI.

| Variant | Coefficients | Condition number | Max exposed residual | b_density positive | b_cfs positive |
|---|---|---:|---:|---|---|
${reducedModelDiagnostics
  .map((variant) =>
    `| ${variant.name} | ${variant.labels.join(', ')} | ${variant.condition} | ${variant.maxAbsCalibrationResidual} | ${variant.bDensityPositive ? 'yes' : 'no'} | ${variant.bCfsPositive === null ? 'n/a' : variant.bCfsPositive ? 'yes' : 'no'} |`
  )
  .join('\n')}

## Descriptor Sources

- SiO2 density: Crystran fused silica material data sheet, density 2.203 g/cc.
- Na2SiO3 density: PubChem sodium silicate HSDB/Merck Index, anhydrous density 2.614.
- Albite density: Mindat specific gravity 2.6-2.65.
- Anorthite density: Mindat specific gravity 2.74-2.76.
- Orthoclase density: Mindat specific gravity 2.55-2.63.
- Kalsilite density: Mindat measured density 2.59-2.62 g/cm3.
- Gehlenite density: CatalystHub/Materials Project Ca2Al2SiO7 structure density 2.97714 g/cm3.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-structural-descriptor-validation-prelookup.json', outDir), JSON.stringify({
  constants,
  coefficients: coefficientMap,
  descriptorCorrelations,
  condition,
  guardrailFailures,
  calibrationResults,
  heldOutDescriptorPreview,
  reducedModelDiagnostics,
}, null, 2));
await writeFile(new URL('ri-structural-descriptor-validation-prelookup.md', outDir), report);
console.log(report);
