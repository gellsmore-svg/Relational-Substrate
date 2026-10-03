import { readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

async function readJson(name) {
  return JSON.parse(await readFile(new URL(name, outDir), 'utf8'));
}

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

function findAngle(rows, angle) {
  return rows.find((row) => row.angle === angle);
}

const peroxide = await readJson('peroxide-nonlocal-refinement.json');

const external = {
  molecule: 'H2O2',
  target: 'torsional profile',
  expectedEquilibriumAngle: 111.9,
  expectedEquilibriumTolerance: 1,
  transBarrierCm1: 387.07,
  cisBarrierCm1: 2562.8,
  sources: [
    {
      label: 'Roto-torsional H2O2 study, Spectrochimica Acta A 2000',
      url: 'https://doi.org/10.1016/S1386-1425(99)00267-X',
      note: 'Reports trans-gauche structure at 111.9 +/- 0.4 degrees, trans barrier 387.07 cm-1, cis barrier 2562.8 cm-1.',
    },
    {
      label: 'Diffusion quantum Monte Carlo H2O2 torsional barriers, Chemical Physics Letters 2004',
      url: 'https://doi.org/10.1016/j.cplett.2004.06.142',
      note: 'Reports calculated trans and cis barriers in good agreement with experimental values around 385/387 and 2488/2563 cm-1.',
    },
  ],
};

const referenceAngle = peroxide.reference.angle;
const referenceDelta = Math.abs(referenceAngle - external.expectedEquilibriumAngle);
const cisRow = findAngle(peroxide.rows, 0);
const transRow = findAngle(peroxide.rows, 180);
const modelCisToTransRatio = cisRow.penaltyVsReference / transRow.penaltyVsReference;
const externalCisToTransRatio = external.cisBarrierCm1 / external.transBarrierCm1;

const checks = [
  {
    check: 'Equilibrium torsion angle',
    expectation: `${external.expectedEquilibriumAngle} +/- ${external.expectedEquilibriumTolerance} degrees`,
    modelValue: referenceAngle,
    pass: referenceDelta <= external.expectedEquilibriumTolerance,
    reading: `Model reference is ${round(referenceDelta, 2)} degrees from the external equilibrium angle.`,
  },
  {
    check: 'Cis barrier higher than trans barrier',
    expectation: 'cis barrier should be much higher than trans barrier',
    modelValue: `cis penalty ${cisRow.penaltyVsReference}; trans penalty ${transRow.penaltyVsReference}`,
    pass: cisRow.penaltyVsReference > transRow.penaltyVsReference,
    reading: 'Model penalty ordering matches the external barrier ordering.',
  },
  {
    check: 'Barrier ratio rough shape',
    expectation: `external cis/trans barrier ratio about ${round(externalCisToTransRatio, 2)}`,
    modelValue: `model cis/trans penalty ratio ${round(modelCisToTransRatio, 2)}`,
    pass: modelCisToTransRatio > 1 && modelCisToTransRatio < externalCisToTransRatio,
    reading:
      'Model gets the direction right but compresses the cis/trans contrast, so this is a partial qualitative pass rather than a quantitative validation.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = round(passed / checks.length, 3);
const status = checks.every((check) => check.pass) ? 'qualitative pass' : 'mixed external benchmark';
const confidenceEffect =
  status === 'qualitative pass'
    ? 'supports a small confidence increase in internal-to-external coherence, not in theory confidence by itself'
    : 'keeps inferential-convergence confidence low until quantitative mismatch is resolved';

const json = {
  source: 'external-h2o2-benchmark.mjs',
  status,
  score,
  confidenceEffect,
  external,
  modelReference: peroxide.reference,
  checks,
};

await writeFile(new URL('external-h2o2-benchmark.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate External H2O2 Benchmark

## Scope

This report is the first external anchor for the topology sandbox. It compares the peroxide torsion diagnostic against source-backed qualitative facts about hydrogen peroxide internal rotation.

It is not a fitted quantum chemistry model. It checks whether the Relational Substrate torsion score has the right qualitative shape before any tuning against external data.

## Result

| Measure | Value |
|---|---:|
| Status | ${status} |
| Passed checks | ${passed}/${checks.length} |
| Score | ${score} |
| Confidence effect | ${confidenceEffect} |

## Checks

| Check | Expectation | Model value | Pass | Reading |
|---|---|---|---|---|
${checks.map((check) => `| ${check.check} | ${check.expectation} | ${check.modelValue} | ${check.pass ? 'yes' : 'no'} | ${check.reading} |`).join('\n')}

## Sources

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

This benchmark moves the work from internal coherence toward external comparison. The model matches the qualitative minimum and cis/trans ordering, but it is not yet quantitatively calibrated to barrier heights.
`;

await writeFile(new URL('external-h2o2-benchmark.md', outDir), markdown);

console.log(`External H2O2 benchmark: ${status}`);
console.log(`Passed checks: ${passed}/${checks.length}`);
console.log(`Wrote ${new URL('external-h2o2-benchmark.md', outDir).pathname}`);
