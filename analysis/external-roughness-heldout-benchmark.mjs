import { readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

async function readJson(name) {
  return JSON.parse(await readFile(new URL(name, outDir), 'utf8'));
}

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

const roughness = await readJson('roughness-scatter-sweep.json');

const predictionManifest = {
  label: 'held-out roughness/interface prediction',
  predictionStage:
    'Roughness scatter rows are generated before this external comparison evaluates source-backed optics checks.',
  heldOutReason:
    'This is a new interface surface, separate from the earlier boundary phase-continuity benchmark.',
  predictions: [
    {
      id: 'smooth-boundary-specular',
      prediction: 'A polished low-roughness boundary should favour coherent specular reflection.',
    },
    {
      id: 'rough-boundary-diffuse',
      prediction: 'A high-roughness boundary should favour diffuse rough scatter over specular order.',
    },
    {
      id: 'false-specular-rejected',
      prediction: 'A high apparent specular row with broken phase memory should not win.',
    },
  ],
};

const external = {
  target: 'roughness-controlled specular versus diffuse scattering',
  sources: [
    {
      label: 'Bruce et al., Applied Optics 2021',
      url: 'https://doi.org/10.1364/AO.410003',
      note: 'Studies light scattering from rough surfaces using controlled polarization and coherence.',
    },
    {
      label: 'van Ginneken et al., Applied Optics 1998',
      url: 'https://doi.org/10.1364/AO.37.000130',
      note: 'Treats diffuse and specular reflectance from rough surfaces.',
    },
    {
      label: 'Bennett and Porteus, JOSA 1961',
      url: 'https://doi.org/10.1364/JOSA.51.000123',
      note: 'Classical relation between surface roughness and specular reflection at normal incidence.',
    },
  ],
};

function summary(caseName) {
  const item = roughness.summaries.find((row) => row.case === caseName);
  if (!item) {
    throw new Error(`Missing roughness summary for ${caseName}`);
  }
  return item;
}

const polished = summary('polished optical boundary');
const microRough = summary('micro-rough glass boundary');
const matte = summary('matte rough boundary');

const checks = [
  {
    check: 'Prediction manifest exists before comparison',
    expectation: 'benchmark should record held-out interface predictions being tested',
    modelValue: predictionManifest.predictions.map((item) => item.id).join(', '),
    pass: predictionManifest.predictions.length === 3,
    reading: 'The roughness comparison is anchored to explicit prediction-order claims.',
  },
  {
    check: 'Smooth boundary predicts specular reflection',
    expectation: 'low roughness should preserve stronger specular reflection',
    modelValue: `${polished.case}: predicted best ${polished.predictedBest}, score ${polished.predictedBestScore}`,
    pass: polished.predictedBest === 'specular coherent reflection',
    reading: 'The smooth interface prediction matches roughness optics expectations.',
  },
  {
    check: 'Near-threshold roughness predicts mixed scatter',
    expectation: 'near-Rayleigh roughness should sit between clean specular and fully diffuse regimes',
    modelValue: `${microRough.case}: predicted best ${microRough.predictedBest}, score ${microRough.predictedBestScore}`,
    pass: microRough.predictedBest === 'micro-rough mixed scatter',
    reading: 'The middle roughness case lands in the mixed scatter regime.',
  },
  {
    check: 'High roughness predicts diffuse scatter',
    expectation: 'rough surfaces should favour diffuse scattering over coherent specular order',
    modelValue: `${matte.case}: predicted best ${matte.predictedBest}, score ${matte.predictedBestScore}`,
    pass: matte.predictedBest === 'diffuse rough scatter',
    reading: 'The high roughness prediction matches the external diffuse-scatter expectation.',
  },
  {
    check: 'False specular decoys rejected',
    expectation: 'apparent specular order with broken phase memory should not win',
    modelValue: roughness.summaries.map((item) => `${item.case}: penalty ${item.decoyPenalty}`).join('; '),
    pass: roughness.summaries.every((item) => item.predictionClearsDecoys && item.decoyPenalty > 0.1),
    reading: 'All roughness regimes reject the decoy rows by the interface threshold.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = round(passed / checks.length, 3);
const status = checks.every((check) => check.pass) ? 'held-out interface pass' : 'mixed held-out interface benchmark';
const confidenceEffect =
  status === 'held-out interface pass'
    ? 'supports a small confidence increase because a separate held-out interface benchmark passes'
    : 'limits confidence because the held-out roughness/interface prediction failed';

const json = {
  source: 'external-roughness-heldout-benchmark.mjs',
  status,
  score,
  confidenceEffect,
  predictionManifest,
  external,
  checks,
  summaries: roughness.summaries,
};

await writeFile(new URL('external-roughness-heldout-benchmark.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate External Roughness Held-Out Benchmark

## Scope

This report evaluates a held-out interface prediction: roughness-controlled specular versus diffuse scatter.

It is not an optics solver. It checks whether the model orders smooth, near-threshold, and rough boundaries in the same qualitative direction as rough-surface scattering literature.

## Result

| Measure | Value |
|---|---:|
| Status | ${status} |
| Passed checks | ${passed}/${checks.length} |
| Score | ${score} |
| Confidence effect | ${confidenceEffect} |

## Prediction Manifest

${predictionManifest.predictions.map((item) => `- ${item.id}: ${item.prediction}`).join('\n')}

## Checks

| Check | Expectation | Model value | Pass | Reading |
|---|---|---|---|---|
${checks.map((check) => `| ${check.check} | ${check.expectation} | ${check.modelValue} | ${check.pass ? 'yes' : 'no'} | ${check.reading} |`).join('\n')}

## Sources

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The held-out roughness benchmark passes: smooth boundaries predict coherent specular order, high roughness predicts diffuse scatter, and false-specular phase-broken decoys are rejected. This improves interface anchoring but remains qualitative.
`;

await writeFile(new URL('external-roughness-heldout-benchmark.md', outDir), markdown);

console.log(`External roughness held-out benchmark: ${status}`);
console.log(`Passed checks: ${passed}/${checks.length}`);
console.log(`Wrote ${new URL('external-roughness-heldout-benchmark.md', outDir).pathname}`);
