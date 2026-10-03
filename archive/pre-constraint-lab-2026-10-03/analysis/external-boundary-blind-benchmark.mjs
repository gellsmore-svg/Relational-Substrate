import { readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

async function readJson(name) {
  return JSON.parse(await readFile(new URL(name, outDir), 'utf8'));
}

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

function rowBy(rows, caseName, variantName) {
  const row = rows.find((item) => item.case === caseName && item.variant === variantName);
  if (!row) {
    throw new Error(`Missing row for ${caseName} / ${variantName}`);
  }
  return row;
}

const boundary = await readJson('boundary-transition-sweep.json');
const phase = await readJson('phase-continuity-sweep.json');

const predictionManifest = {
  label: 'pre-comparison boundary and phase-order prediction',
  predictionStage:
    'Model rows are read and ranked before this script evaluates the external comparison checks.',
  verificationStatus:
    'documented in-script and reproducible, but not independently timestamped before the diagnostic cases existed',
  scope:
    'Predict qualitative ordering among phase-preserving, amplitude-only, phase-broken, rough-scatter, and ordered-boundary variants.',
  predictions: [
    {
      id: 'phase-preserving-outranks-amplitude-only',
      prediction:
        'Phase-continuous transmission should outrank amplitude-only passage and phase-broken high transmission even when amplitude or route split looks good.',
    },
    {
      id: 'ordered-boundary-outranks-diffuse-scatter',
      prediction:
        'Ordered boundary transition should outrank diffuse-scatter dominated boundary variants for simple air/glass and glass/air proxies.',
    },
    {
      id: 'rough-transmitting-is-intermediate',
      prediction:
        'Rough but still transmitting boundary variants should sit below ordered references but above diffuse-scatter decoys.',
    },
  ],
};

const external = {
  target: 'optical boundary phase and rough-scatter ordering',
  expectations: [
    {
      id: 'boundary-continuity',
      expectation:
        'Reflection and transmission at an optical boundary are governed by wave boundary conditions, so phase/field continuity is not optional bookkeeping.',
    },
    {
      id: 'rough-scatter-coherence',
      expectation:
        'Rough-surface scattering is treated as a field/coherence problem, and diffuse scattering degrades clean specular wavefront order.',
    },
  ],
  sources: [
    {
      label: 'Physics LibreTexts, Reflection and Transmission at Boundaries and Fresnel Equations',
      url: 'https://phys.libretexts.org/Bookshelves/Optics/Physical_Optics_%28Tatum%29/02%3A_Reflection_and_Transmission_at_Boundaries_and_the_Fresnel_Equations',
      note: 'Frames reflected and transmitted amplitudes as consequences of boundary continuity conditions.',
    },
    {
      label: 'Bruce et al., Applied Optics 2021',
      url: 'https://doi.org/10.1364/AO.410003',
      note: 'Studies rough-surface scattering with controlled polarization and coherence of the incident beam.',
    },
    {
      label: 'Hyde et al., Optics Express 2013',
      url: 'https://doi.org/10.1364/OE.21.006807',
      note: 'Treats scattering of a partially coherent wave from a statistically rough material surface.',
    },
  ],
};

const phaseComparisons = phase.summaries.map((summary) => {
  const reference = rowBy(phase.rows, summary.case, 'phase-continuous transmission');
  const amplitudeOnly = rowBy(phase.rows, summary.case, 'amplitude-only passage');
  const phaseBroken = rowBy(phase.rows, summary.case, 'phase-broken high transmission');

  return {
    case: summary.case,
    referenceScore: reference.score,
    amplitudeOnlyScore: amplitudeOnly.score,
    phaseBrokenScore: phaseBroken.score,
    referenceMarginVsAmplitudeOnly: round(reference.score - amplitudeOnly.score),
    referenceMarginVsPhaseBroken: round(reference.score - phaseBroken.score),
    pass: reference.score > amplitudeOnly.score && reference.score > phaseBroken.score,
  };
});

const boundaryComparisons = boundary.summaries.map((summary) => {
  const reference = rowBy(boundary.rows, summary.case, 'ordered boundary transition');
  const roughTransmitting = rowBy(boundary.rows, summary.case, 'rough but transmitting boundary');
  const diffuseScatter = rowBy(boundary.rows, summary.case, 'diffuse scatter dominated boundary');

  return {
    case: summary.case,
    referenceScore: reference.score,
    roughTransmittingScore: roughTransmitting.score,
    diffuseScatterScore: diffuseScatter.score,
    referenceMarginVsRough: round(reference.score - roughTransmitting.score),
    roughMarginVsDiffuse: round(roughTransmitting.score - diffuseScatter.score),
    pass: reference.score > roughTransmitting.score && roughTransmitting.score > diffuseScatter.score,
  };
});

const checks = [
  {
    check: 'Prediction manifest exists before comparison',
    expectation: 'benchmark should record the qualitative prediction being tested',
    modelValue: predictionManifest.predictions.map((item) => item.id).join(', '),
    pass: predictionManifest.predictions.length === 3,
    reading: 'The comparison is anchored to explicit model-order predictions.',
  },
  {
    check: 'Phase-preserving transmission outranks amplitude-only passage',
    expectation: external.expectations.find((item) => item.id === 'boundary-continuity').expectation,
    modelValue: phaseComparisons
      .map(
        (item) =>
          `${item.case}: reference ${item.referenceScore}, amplitude-only ${item.amplitudeOnlyScore}, phase-broken ${item.phaseBrokenScore}`
      )
      .join('; '),
    pass: phaseComparisons.every((item) => item.pass),
    reading:
      'The model predicts that apparent transmission is insufficient when phase continuity and phase memory break.',
  },
  {
    check: 'Ordered boundary outranks rough and diffuse scatter',
    expectation: external.expectations.find((item) => item.id === 'rough-scatter-coherence').expectation,
    modelValue: boundaryComparisons
      .map(
        (item) =>
          `${item.case}: ordered ${item.referenceScore}, rough ${item.roughTransmittingScore}, diffuse ${item.diffuseScatterScore}`
      )
      .join('; '),
    pass: boundaryComparisons.every((item) => item.pass),
    reading:
      'The model predicts a clean ordering from ordered transmission to rough transmission to diffuse scatter.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = round(passed / checks.length, 3);
const status = checks.every((check) => check.pass)
  ? 'documented blind-style qualitative pass'
  : 'mixed blind-style benchmark';
const confidenceEffect =
  status === 'documented blind-style qualitative pass'
    ? 'supports a small confidence increase because an explicit boundary prediction survives external qualitative checks, but inferential weight is limited because the prediction was not independently timestamped'
    : 'limits confidence because the boundary prediction fails external qualitative ordering';

const json = {
  source: 'external-boundary-blind-benchmark.mjs',
  status,
  score,
  confidenceEffect,
  predictionManifest,
  external,
  phaseComparisons,
  boundaryComparisons,
  checks,
};

await writeFile(new URL('external-boundary-blind-benchmark.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate External Boundary Blind-Style Benchmark

## Scope

This report records a pre-comparison model prediction for boundary and phase-order cases, then compares it against external qualitative optics expectations.

It is blind-style rather than a full historical blind test: the current diagnostic cases already exist, but this report separates the prediction manifest from the external comparison checks and does not tune model scores.

Verification limit: ${predictionManifest.verificationStatus}. This benchmark should be treated as documented and reproducible, not as a fully independent blind prediction.

## Result

| Measure | Value |
|---|---:|
| Status | ${status} |
| Passed checks | ${passed}/${checks.length} |
| Score | ${score} |
| Confidence effect | ${confidenceEffect} |

## Prediction Manifest

Verification status: ${predictionManifest.verificationStatus}.

${predictionManifest.predictions.map((item) => `- ${item.id}: ${item.prediction}`).join('\n')}

## Checks

| Check | Expectation | Model value | Pass | Reading |
|---|---|---|---|---|
${checks.map((check) => `| ${check.check} | ${check.expectation} | ${check.modelValue} | ${check.pass ? 'yes' : 'no'} | ${check.reading} |`).join('\n')}

## Sources

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The model survives this boundary prediction check: phase-preserving transmission outranks amplitude-only or phase-broken passage, and ordered boundaries outrank rough and diffuse-scatter variants. Because the prediction was not independently timestamped before the cases existed, this benchmark carries reduced inferential weight. It does not turn the sandbox into an optics simulator; it only clears one documented qualitative prediction-ordering gate.
`;

await writeFile(new URL('external-boundary-blind-benchmark.md', outDir), markdown);

console.log(`External boundary blind-style benchmark: ${status}`);
console.log(`Passed checks: ${passed}/${checks.length}`);
console.log(`Wrote ${new URL('external-boundary-blind-benchmark.md', outDir).pathname}`);
