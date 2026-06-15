import { readFile, mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

async function readJson(name) {
  return JSON.parse(await readFile(new URL(`./out/${name}`, import.meta.url), 'utf8'));
}

function round(value, places = 6) {
  return Number(value.toFixed(places));
}

function mean(values) {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function resultByName(report, name) {
  const result = report.results.find((row) => row.name === name);
  if (!result) throw new Error(`Missing result family: ${name}`);
  return result;
}

function format(value) {
  if (value === null || value === undefined) return 'n/a';
  if (typeof value === 'boolean') return value ? 'yes' : 'no';
  return value;
}

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const rankinite = await readJson('external-ri-rankinite-ca-scaffold-transfer-validation.json');
const kilchoanite = await readJson('external-ri-kilchoanite-ca-scaffold-transfer-validation.json');
const larnite = await readJson('external-ri-larnite-ca-scaffold-transfer-validation.json');
const larniteGate = await readJson('ri-larnite-gate-classification-diagnostic.json');

const targets = [rankinite, kilchoanite, larnite].map((report) => {
  const baseline = resultByName(report, 'baseline density + Al/O + Al-comp response');
  const splitCa = resultByName(report, 'split Ca scaffold family');
  const splitCaMg = resultByName(report, 'split Ca/Mg scaffold family');
  return {
    material: report.target.material,
    formula: report.target.formula,
    topologyClass: report.target.topologyClass,
    density: report.target.density,
    caO: report.target.caScaffoldO,
    oxygenVolume: report.target.oxygenVolume,
    measuredRi: report.target.measuredRi,
    baselinePrediction: baseline.predictedRi,
    baselineResidual: baseline.residual,
    baselinePass: baseline.midpointPass,
    splitCaPrediction: splitCa.predictedRi,
    splitCaResidual: splitCa.residual,
    splitCaPass: splitCa.midpointPass,
    splitCaMgPrediction: splitCaMg.predictedRi,
    splitCaMgResidual: splitCaMg.residual,
    splitCaMgPass: splitCaMg.midpointPass,
  };
});

const nonMeliliteSummary = {
  rows: targets.map((row) => row.material),
  meanDensity: round(mean(targets.map((row) => row.density))),
  meanCaO: round(mean(targets.map((row) => row.caO))),
  meanMeasuredRi: round(mean(targets.map((row) => row.measuredRi))),
  meanBaselineResidual: round(mean(targets.map((row) => row.baselineResidual))),
  meanSplitCaResidual: round(mean(targets.map((row) => row.splitCaResidual))),
  meanSplitCaMgResidual: round(mean(targets.map((row) => row.splitCaMgResidual))),
};

const contrastFindings = [
  {
    finding: 'The larnite baseline pass is a control-row success, not a repair validation',
    evidence:
      'The baseline family passes larnite but misses rankinite and kilchoanite, so one high-density orthosilicate row is not enough to promote it as a material-property model.',
  },
  {
    finding: 'The split-Ca term is consistently too large outside melilite',
    evidence:
      `Split-Ca residuals are ${targets.map((row) => `${row.material} ${row.splitCaResidual}`).join(', ')}; all are negative overpredictions.`,
  },
  {
    finding: 'Larnite shows that topology-gated non-transfer does not mean low RI',
    evidence:
      'Larnite has the highest measured RI in this non-melilite set, but the melilite-derived Ca uplift still overshoots it by 0.03067.',
  },
  {
    finding: 'The next variable is suppression/gating of Ca scaffold response, not another scalar Ca coefficient',
    evidence:
      'Ca/O rises from 0.42857 in Ca3Si2O7 rows to 0.5 in larnite, while split-Ca overprediction remains large; raw Ca/O has the wrong transfer shape.',
  },
];

const nextTests = [
  {
    task: 'Density-control falsifier',
    purpose:
      'Reserve another high-density Ca-silicate with optical constants and CIF geometry to test whether the baseline density-family larnite pass repeats.',
    boundary:
      'Do not choose the target by estimated fit; source the optical and CIF rows first, then score the frozen baseline and split-Ca families.',
  },
  {
    task: 'Gate-suppressed Ca diagnostic',
    purpose:
      'State a diagnostic version of Ca scaffold response that is active in melilite-like CaO8 environments and suppressed in compact/lower-coordinate non-melilite environments.',
    boundary:
      'Treat this as a model-form hypothesis only until a fresh target is reserved; do not fit a coefficient from rankinite, kilchoanite, and larnite.',
  },
  {
    task: 'Control-family audit',
    purpose:
      'Ask whether the baseline density + Al/O + Al-comp response is functioning as a crude Lorentz-Lorenz density proxy rather than a substrate-specific topology term.',
    boundary:
      'Acknowledge conventional density/polarizability explanations as the comparator; do not count a density-only success as substrate-specific evidence.',
  },
];

const report = {
  source: 'ri-larnite-density-control-contrast-diagnostic.mjs',
  status: 'diagnostic only; larnite contrast explains control pass versus split-Ca failure',
  larnitePreScoreGate: {
    classification: larniteGate.gateClassification,
    descriptors: larniteGate.larniteDescriptors,
  },
  targets,
  nonMeliliteSummary,
  contrastFindings,
  nextTests,
};

const markdown = `# RI Larnite Density-Control Contrast Diagnostic

## Scope

This diagnostic explains the larnite contrast after scoring: the older density-dominant baseline passes larnite, while the post-failure split-Ca repair fails. It does not fit a new coefficient and does not promote either family.

## Target Rows

${table(
  [
    'Material',
    'Formula',
    'Topology',
    'Density',
    'Ca/O',
    'O volume',
    'Measured RI',
    'Baseline pred',
    'Baseline residual',
    'Baseline pass',
    'Split-Ca pred',
    'Split-Ca residual',
    'Split-Ca pass',
  ],
  targets.map((row) => [
    row.material,
    row.formula,
    row.topologyClass,
    row.density,
    round(row.caO),
    round(row.oxygenVolume),
    row.measuredRi,
    row.baselinePrediction,
    row.baselineResidual,
    row.baselinePass ? 'yes' : 'no',
    row.splitCaPrediction,
    row.splitCaResidual,
    row.splitCaPass ? 'yes' : 'no',
  ])
)}

## Non-Melilite Summary

${table(
  ['Rows', 'Mean density', 'Mean Ca/O', 'Mean measured RI', 'Mean baseline residual', 'Mean split-Ca residual', 'Mean split-Ca/Mg residual'],
  [
    [
      nonMeliliteSummary.rows.join(', '),
      nonMeliliteSummary.meanDensity,
      nonMeliliteSummary.meanCaO,
      nonMeliliteSummary.meanMeasuredRi,
      nonMeliliteSummary.meanBaselineResidual,
      nonMeliliteSummary.meanSplitCaResidual,
      nonMeliliteSummary.meanSplitCaMgResidual,
    ],
  ]
)}

## Larnite Gate State Before Scoring

${table(
  ['Descriptor', 'Value'],
  [
    ['Gate classification', larniteGate.gateClassification],
    ['Mean Ca coordination', format(larniteGate.larniteDescriptors.scaffoldCoordinationMean)],
    ['Mean Ca-O', format(larniteGate.larniteDescriptors.scaffoldDistanceMean)],
    ['Bridge angle mean', format(larniteGate.larniteDescriptors.bridgeAngleMean)],
  ]
)}

## Contrast Findings

${table(
  ['Finding', 'Evidence'],
  contrastFindings.map((row) => [row.finding, row.evidence])
)}

## Next Tests

${table(
  ['Task', 'Purpose', 'Boundary'],
  nextTests.map((row) => [row.task, row.purpose, row.boundary])
)}

## Reading

The larnite row sharpens the diagnosis. The failure is not "non-melilite Ca silicates have low RI"; larnite has high RI and the baseline density-family predictor fits it. The failure is that the melilite-derived Ca scaffold uplift is not transferable as a scalar Ca/O term. Outside melilite, Ca scaffold response needs a topology/environment gate or suppression term, and the density-family control must remain visible as the conventional comparator.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-larnite-density-control-contrast-diagnostic.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('ri-larnite-density-control-contrast-diagnostic.md', outDir), markdown);

console.log(markdown);
