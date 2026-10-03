import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const melilites = [
  {
    formula: 'Ca2Al2SiO7',
    material: 'gehlenite',
    t1Cation: 'Al',
    t1Charge: 3,
    t1IonicRadiusTetraAngstrom: 0.39,
    shannonNoCnPolarizabilityA3: 0.79,
    mlrCn4PolarizabilityA3: 1.5649,
    mlExtendedCn4PolarizabilityA3: 1.2527,
    measuredRi: 1.66217,
    caScaffoldPrediction: 1.66054,
    frozenPreSplitPrediction: 1.62573,
    sourceClass: 'paper-backed',
  },
  {
    formula: 'Ca2MgSi2O7',
    material: 'akermanite',
    t1Cation: 'Mg',
    t1Charge: 2,
    t1IonicRadiusTetraAngstrom: 0.57,
    shannonNoCnPolarizabilityA3: 1.32,
    mlrCn4PolarizabilityA3: 2.07,
    mlExtendedCn4PolarizabilityA3: 1.9571,
    measuredRi: 1.63467,
    caScaffoldPrediction: 1.63523,
    frozenPreSplitPrediction: 1.57197,
    sourceClass: 'source-qualified',
  },
  {
    formula: 'Ca2ZnSi2O7',
    material: 'hardystonite',
    t1Cation: 'Zn',
    t1Charge: 2,
    t1IonicRadiusTetraAngstrom: 0.6,
    shannonNoCnPolarizabilityA3: 2.04,
    mlrCn4PolarizabilityA3: 2.7618,
    mlExtendedCn4PolarizabilityA3: 2.4089,
    measuredRi: 1.665,
    caScaffoldPrediction: 1.72018,
    frozenPreSplitPrediction: null,
    sourceClass: 'handbook-backed',
  },
];

const t1PropertySources = [
  {
    property: 'tetrahedral ionic radius',
    source: 'Shannon effective ionic radii, as reproduced in Nagra NTB 23-03 table excerpt and general Shannon-radius references',
    values: 'Al3+ IV 0.39 A; Mg2+ IV 0.57 A; Zn2+ IV 0.60 A',
    status: 'source-anchored enough for descriptor diagnosis',
  },
  {
    property: 'cation polarizability',
    source:
      'Qin et al. 2023 public ion dielectric polarizability database, derived from Shannon-style dielectric polarizability data and expanded by MLR/ML methods',
    values:
      'Shannon no-CN: Al3+ 0.7900, Mg2+ 1.3200, Zn2+ 2.0400 A3; MLR CN4: Al3+ 1.5649, Mg2+ 2.0700, Zn2+ 2.7618 A3; ML-extended CN4: Al3+ 1.2527, Mg2+ 1.9571, Zn2+ 2.4089 A3',
    status: 'source-anchored for descriptor diagnosis; not an optical validation predictor',
  },
];

function round(value, places = 5) {
  return Number(value.toFixed(places));
}

function mean(values) {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function correlation(left, right) {
  const leftMean = mean(left);
  const rightMean = mean(right);
  const numerator = left.reduce((sum, value, index) => sum + (value - leftMean) * (right[index] - rightMean), 0);
  const denominator = Math.sqrt(
    left.reduce((sum, value) => sum + (value - leftMean) ** 2, 0) *
      right.reduce((sum, value) => sum + (value - rightMean) ** 2, 0)
  );
  return denominator === 0 ? null : round(numerator / denominator, 6);
}

const rows = melilites.map((row) => ({
  ...row,
  caScaffoldResidual: round(row.measuredRi - row.caScaffoldPrediction),
  preSplitResidual:
    row.frozenPreSplitPrediction === null ? null : round(row.measuredRi - row.frozenPreSplitPrediction),
}));

const polarizabilityScales = [
  {
    key: 'shannonNoCnPolarizabilityA3',
    label: 'Shannon no-CN',
    status: 'legacy no-coordination ion dielectric polarizability',
  },
  {
    key: 'mlrCn4PolarizabilityA3',
    label: 'MLR CN4',
    status: 'coordination-specific optimized ion dielectric polarizability',
  },
  {
    key: 'mlExtendedCn4PolarizabilityA3',
    label: 'ML-extended CN4',
    status: 'coordination-specific machine-learning extended ion dielectric polarizability',
  },
];

const polarizabilityScaleDiagnostics = polarizabilityScales.map((scale) => ({
  ...scale,
  values: rows.map((row) => `${row.t1Cation}:${row[scale.key]}`),
  correlationVsMeasuredRi: correlation(
    rows.map((row) => row[scale.key]),
    rows.map((row) => row.measuredRi)
  ),
  correlationVsCaScaffoldResidual: correlation(
    rows.map((row) => row[scale.key]),
    rows.map((row) => row.caScaffoldResidual)
  ),
  order: [...rows].sort((a, b) => a[scale.key] - b[scale.key]).map((row) => `${row.t1Cation}:${row[scale.key]}`),
}));

const correlations = {
  t1RadiusVsMeasuredRi: correlation(
    rows.map((row) => row.t1IonicRadiusTetraAngstrom),
    rows.map((row) => row.measuredRi)
  ),
};

const orderings = {
  measuredRiOrder: [...rows]
    .sort((a, b) => a.measuredRi - b.measuredRi)
    .map((row) => `${row.t1Cation}:${row.measuredRi}`),
  caScaffoldResidualOrder: [...rows]
    .sort((a, b) => a.caScaffoldResidual - b.caScaffoldResidual)
    .map((row) => `${row.t1Cation}:${row.caScaffoldResidual}`),
};

const report = {
  source: 'ri-melilite-t1-cation-diagnostic.mjs',
  status: 'diagnostic only; no predictor promoted',
  rows,
  t1PropertySources,
  polarizabilityScaleDiagnostics,
  correlations,
  orderings,
  sourceCaveat:
    'T1 ionic radii are source-anchored. T1 polarizability now has source-anchored dielectric scales, but those scales are not promoted as optical-RI validation predictors without a frozen conversion or calibration rule.',
};

function table(headers, bodyRows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...bodyRows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const markdown = `# RI Melilite T1-Cation Diagnostic

## Scope

This diagnostic follows the hardystonite failure. It does not promote a predictor. It asks whether the melilite RI behavior is better read through T1 cation identity than through a generic Ca scaffold term.

The T1 radius values are source-anchored. The T1 polarizability values now include source-anchored dielectric scales, but those scales are not promoted as optical-RI validation predictors without a frozen conversion or calibration rule.

## T1 Property Source Status

${table(
  ['Property', 'Source', 'Values', 'Status'],
  t1PropertySources.map((row) => [row.property, row.source, row.values, row.status])
)}

## Rows

${table(
  [
    'Formula',
    'Material',
    'T1 cation',
    'T1 charge',
    'T1 radius',
    'Shannon no-CN polarizability',
    'MLR CN4 polarizability',
    'ML-extended CN4 polarizability',
    'Measured RI',
    'Ca-scaffold prediction',
    'Ca-scaffold residual',
    'Source class',
  ],
  rows.map((row) => [
    row.formula,
    row.material,
    row.t1Cation,
    row.t1Charge,
    row.t1IonicRadiusTetraAngstrom,
    row.shannonNoCnPolarizabilityA3,
    row.mlrCn4PolarizabilityA3,
    row.mlExtendedCn4PolarizabilityA3,
    row.measuredRi,
    row.caScaffoldPrediction,
    row.caScaffoldResidual,
    row.sourceClass,
  ])
)}

## Orderings

| Ordering | Value |
|---|---|
| Measured RI | ${orderings.measuredRiOrder.join(' < ')} |
| Ca-scaffold residual | ${orderings.caScaffoldResidualOrder.join(' < ')} |

## Polarizability Scale Diagnostics

${table(
  ['Scale', 'Values', 'Order', 'Corr vs measured RI', 'Corr vs Ca-scaffold residual', 'Status'],
  polarizabilityScaleDiagnostics.map((row) => [
    row.label,
    row.values.join('; '),
    row.order.join(' < '),
    row.correlationVsMeasuredRi,
    row.correlationVsCaScaffoldResidual,
    row.status,
  ])
)}

## Correlations

${table(
  ['Pair', 'Correlation'],
  Object.entries(correlations).map(([key, value]) => [key, value])
)}

## Reading

All three source-anchored dielectric polarizability scales preserve the same T1 ordering: Al < Mg < Zn. The measured RI ordering remains Mg < Al < Zn, and hardystonite remains far below the Ca-scaffold prediction. That supports the Opus interpretation: T1-site topology buffers or gates cation polarizability rather than adding it directly.

The next model should separate:

1. Ca scaffold baseline for the melilite topology;
2. T1 cation identity or source-anchored polarizability;
3. a topology-buffer term that prevents high-polarizability Zn from being passed through additively.

Do not use these dielectric polarizabilities directly for optical validation. The next step is to freeze a melilite-only diagnostic model that can use polarizability as an ordered or scaled descriptor only with an explicit conversion/calibration rule before any additional melilite target is scored.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-melilite-t1-cation-diagnostic.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('ri-melilite-t1-cation-diagnostic.md', outDir), markdown);

console.log(markdown);
