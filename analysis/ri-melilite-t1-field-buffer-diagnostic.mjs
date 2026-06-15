import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const rows = [
  {
    material: 'gehlenite',
    formula: 'Ca2Al2SiO7',
    t1Cation: 'Al',
    t1Class: 'trivalent high-field network former',
    t1Charge: 3,
    t1RadiusCn4A: 0.39,
    mlrCn4PolarizabilityA3: 1.5649,
    d10Flag: 0,
    measuredRi: 1.66217,
    caScaffoldPrediction: 1.66054,
  },
  {
    material: 'akermanite',
    formula: 'Ca2MgSi2O7',
    t1Cation: 'Mg',
    t1Class: 'divalent s-block tetrahedral cation',
    t1Charge: 2,
    t1RadiusCn4A: 0.57,
    mlrCn4PolarizabilityA3: 2.07,
    d10Flag: 0,
    measuredRi: 1.63467,
    caScaffoldPrediction: 1.63523,
  },
  {
    material: 'hardystonite',
    formula: 'Ca2ZnSi2O7',
    t1Cation: 'Zn',
    t1Class: 'divalent d10 tetrahedral cation',
    t1Charge: 2,
    t1RadiusCn4A: 0.6,
    mlrCn4PolarizabilityA3: 2.7618,
    d10Flag: 1,
    measuredRi: 1.665,
    caScaffoldPrediction: 1.72018,
  },
];

function round(value, places = 6) {
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
  return denominator === 0 ? null : round(numerator / denominator);
}

const enrichedRows = rows.map((row) => ({
  ...row,
  chargePerRadius: round(row.t1Charge / row.t1RadiusCn4A),
  fieldStrength: round(row.t1Charge / row.t1RadiusCn4A ** 2),
  polarizabilityPerCharge: round(row.mlrCn4PolarizabilityA3 / row.t1Charge),
  polarizabilityPerRadius3: round(row.mlrCn4PolarizabilityA3 / row.t1RadiusCn4A ** 3),
  caScaffoldResidual: round(row.measuredRi - row.caScaffoldPrediction),
}));

const descriptorKeys = [
  'chargePerRadius',
  'fieldStrength',
  'mlrCn4PolarizabilityA3',
  'polarizabilityPerCharge',
  'polarizabilityPerRadius3',
  'd10Flag',
];

const descriptorDiagnostics = descriptorKeys.map((key) => ({
  descriptor: key,
  order: [...enrichedRows].sort((a, b) => a[key] - b[key]).map((row) => `${row.t1Cation}:${row[key]}`),
  correlationVsMeasuredRi: correlation(
    enrichedRows.map((row) => row[key]),
    enrichedRows.map((row) => row.measuredRi)
  ),
  correlationVsCaScaffoldResidual: correlation(
    enrichedRows.map((row) => row[key]),
    enrichedRows.map((row) => row.caScaffoldResidual)
  ),
}));

const proposedFreezeOptions = [
  {
    option: 'T1 identity class',
    rule: 'Use categorical classes Al-high-field, Mg-divalent-s, Zn-divalent-d10; do not interpolate by raw polarizability.',
    status: 'most honest with three melilite rows; highest calibration debt if converted to coefficients',
  },
  {
    option: 'Field plus d10 gate',
    rule: 'Use fieldStrength for Al-vs-divalent contrast and d10Flag for Zn; keep Ca scaffold as baseline covariate.',
    status: 'best physical diagnostic form to freeze before a new target, but needs a target outside Al/Mg/Zn to validate',
  },
  {
    option: 'Raw polarizability',
    rule: 'Use MLR CN4 polarizability directly.',
    status: 'rejected for validation: the Al < Mg < Zn order conflicts with measured Mg < Al < Zn behavior',
  },
];

const report = {
  source: 'ri-melilite-t1-field-buffer-diagnostic.mjs',
  status: 'diagnostic only; candidate model form selection before future validation',
  sourceNotes: [
    'CN4 ionic radii follow Shannon-style tetrahedral radii used in the companion T1 diagnostic.',
    'CN4 polarizabilities use the Qin et al. 2023 public ion dielectric polarizability database MLR-optimized scale.',
    'The Zn d10 flag represents the pseudo-noble-gas / filled-d-shell cation class; use as a physical class marker, not a fitted optical coefficient yet.',
  ],
  rows: enrichedRows,
  descriptorDiagnostics,
  proposedFreezeOptions,
};

function table(headers, bodyRows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...bodyRows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const markdown = `# RI Melilite T1 Field-Buffer Diagnostic

## Scope

This diagnostic follows source-anchoring of the T1 dielectric polarizability table. It does not score a new material and does not promote a predictor. It asks which physical descriptor family should be frozen before the next held-out melilite or Ca-silicate test.

## Rows

${table(
  [
    'Material',
    'Formula',
    'T1',
    'T1 class',
    'Charge/r',
    'Field z/r2',
    'MLR CN4 polarizability',
    'Polarizability/charge',
    'Polarizability/r3',
    'd10',
    'Measured RI',
    'Ca residual',
  ],
  enrichedRows.map((row) => [
    row.material,
    row.formula,
    row.t1Cation,
    row.t1Class,
    row.chargePerRadius,
    row.fieldStrength,
    row.mlrCn4PolarizabilityA3,
    row.polarizabilityPerCharge,
    row.polarizabilityPerRadius3,
    row.d10Flag,
    row.measuredRi,
    row.caScaffoldResidual,
  ])
)}

## Descriptor Diagnostics

${table(
  ['Descriptor', 'Order', 'Corr vs measured RI', 'Corr vs Ca-scaffold residual'],
  descriptorDiagnostics.map((row) => [
    row.descriptor,
    row.order.join(' < '),
    row.correlationVsMeasuredRi,
    row.correlationVsCaScaffoldResidual,
  ])
)}

## Freeze Options

${table(
  ['Option', 'Rule', 'Status'],
  proposedFreezeOptions.map((row) => [row.option, row.rule, row.status])
)}

## Reading

Raw T1 polarizability remains the wrong validation descriptor by itself. It orders Al < Mg < Zn, while the measured RI order is Mg < Al < Zn. Field strength separates Al from the divalent T1 cations, while the d10 class separates Zn from Mg despite their similar charge and radius.

The most useful next frozen form is therefore not a scalar polarizability pass-through. It is a Ca-scaffold baseline plus a T1 buffer term with two parts:

1. a high-field T1 term for trivalent Al-like occupancy;
2. a d10 / covalency class marker for Zn-like occupancy.

This is still calibration debt. With only Al, Mg, and Zn melilites in hand, the honest next validation target should test one of those classes without adding a new class, or else move outside melilite to test whether the Ca-scaffold baseline transfers independently of T1 chemistry.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-melilite-t1-field-buffer-diagnostic.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('ri-melilite-t1-field-buffer-diagnostic.md', outDir), markdown);

console.log(markdown);
