import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const rows = [
  {
    formula: 'CaAl2Si2O8',
    material: 'anorthite',
    topologyClass: 'feldspar framework',
    measuredRi: 1.58167,
    predictedDensityFamily: 1.58412,
    composition: { Ca: 1, Al: 2, Si: 2, O: 8 },
    chargeBalancedAlO: 2 / 8,
    currentCationResponseO: 0.21905,
    role: 'current Ca-Al feldspar row fit reasonably by density-family diagnostics',
  },
  {
    formula: 'Ca2Al2SiO7',
    material: 'gehlenite',
    topologyClass: 'melilite sorosilicate',
    measuredRi: 1.66217,
    predictedDensityFamily: 1.62573,
    composition: { Ca: 2, Al: 2, Si: 1, O: 7 },
    chargeBalancedAlO: 2 / 7,
    currentCationResponseO: 0.250343,
    role: 'paper-backed fresh melilite failure',
  },
  {
    formula: 'Ca2MgSi2O7',
    material: 'akermanite',
    topologyClass: 'melilite sorosilicate',
    measuredRi: 1.63467,
    predictedDensityFamily: 1.57197,
    composition: { Ca: 2, Mg: 1, Si: 2, O: 7 },
    chargeBalancedAlO: 0,
    currentCationResponseO: 0,
    role: 'source-qualified melilite failure; no Al charge balance so current cation-response vanishes',
  },
];

function round(value, places = 5) {
  return Number(value.toFixed(places));
}

function count(row, element) {
  return row.composition[element] ?? 0;
}

function caScaffoldO(row) {
  return count(row, 'Ca') / count(row, 'O');
}

function nonTetrahedralChargeO(row) {
  return (2 * count(row, 'Ca')) / count(row, 'O');
}

function tetrahedralAlFraction(row) {
  const tCations = count(row, 'Al') + count(row, 'Si') + count(row, 'Mg');
  return count(row, 'Al') / tCations;
}

function decorate(row) {
  const residual = row.measuredRi - row.predictedDensityFamily;
  return {
    ...row,
    caScaffoldO: round(caScaffoldO(row)),
    nonTetrahedralChargeO: round(nonTetrahedralChargeO(row)),
    tetrahedralAlFraction: round(tetrahedralAlFraction(row)),
    residual: round(residual),
    residualPerCaO: round(residual / caScaffoldO(row)),
    currentResponseBlindSpot:
      caScaffoldO(row) > 0 && row.currentCationResponseO === 0
        ? 'yes: Ca scaffold present but current cation-response is zero'
        : 'no',
  };
}

const decoratedRows = rows.map(decorate);

const contrasts = [
  {
    contrast: 'akermanite current-response blind spot',
    evidence:
      'akermanite has Ca/O 0.28571 and non-T charge/O 0.57143, but current cation-response/O is 0 because it is tied to charge-balanced Al/O',
    reading:
      'The current response term conflates charge compensation with Ca scaffold; it cannot represent Ca-rich non-Al melilites.',
  },
  {
    contrast: 'melilite residuals share sign',
    evidence:
      'gehlenite residual +0.03644; akermanite residual +0.0627 under the frozen density family',
    reading:
      'Both melilites are underpredicted, so the missing term likely raises RI for Ca-rich melilite scaffolds rather than correcting only Al chemistry.',
  },
  {
    contrast: 'anorthite is not enough',
    evidence:
      'anorthite is Ca-bearing and fits reasonably, but Ca/O is 0.125 versus 0.28571 in both melilites',
    reading:
      'A single Ca feldspar row does not calibrate the high-Ca melilite scaffold regime.',
  },
];

const report = {
  source: 'ri-ca-scaffold-response-diagnostic.mjs',
  status: 'diagnostic only; no repair promoted',
  rows: decoratedRows,
  contrasts,
  nextHypothesis:
    'Separate modifier charge compensation from non-tetrahedral Ca scaffold density/polarizability before any further RI validation.',
};

function table(headers, bodyRows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...bodyRows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const markdown = `# RI Ca-Scaffold Response Diagnostic

## Scope

This diagnostic follows the gehlenite and akermanite melilite failures. It does not promote a repair term. It asks whether the current cation-response variable is blind to Ca-rich scaffold response because it is tied to charge-balanced Al/O.

## Rows

${table(
  [
    'Formula',
    'Material',
    'Topology',
    'Measured RI',
    'Density-family prediction',
    'Residual',
    'Ca/O',
    'Non-T charge/O',
    'Al/O',
    'T Al fraction',
    'Current cation-response/O',
    'Blind spot',
  ],
  decoratedRows.map((row) => [
    row.formula,
    row.material,
    row.topologyClass,
    row.measuredRi,
    row.predictedDensityFamily,
    row.residual,
    row.caScaffoldO,
    row.nonTetrahedralChargeO,
    round(row.chargeBalancedAlO),
    row.tetrahedralAlFraction,
    round(row.currentCationResponseO),
    row.currentResponseBlindSpot,
  ])
)}

## Contrasts

${table(
  ['Contrast', 'Evidence', 'Reading'],
  contrasts.map((row) => [row.contrast, row.evidence, row.reading])
)}

## Reading

The melilite failures expose a variable-type error. The current cation-response term is useful for charge-balanced aluminosilicate frameworks, but it disappears for akermanite because there is no Al charge-compensation demand. That is physically wrong for RI: Ca remains a dense, polarizable non-tetrahedral scaffold even when it is not compensating Al.

The next repair candidate should not simply add "more Ca" as a fitted scalar. It should separate:

1. charge-compensation role: modifier charge used to balance Al;
2. scaffold role: non-tetrahedral Ca/Mg content per oxygen or per volume;
3. topology role: feldspar framework versus melilite sorosilicate.

Until that separation exists, the RI model should remain failed across melilite transfer.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-ca-scaffold-response-diagnostic.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('ri-ca-scaffold-response-diagnostic.md', outDir), markdown);

console.log(markdown);
