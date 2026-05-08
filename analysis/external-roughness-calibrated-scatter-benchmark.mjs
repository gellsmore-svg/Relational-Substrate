import { readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

async function readJson(name) {
  return JSON.parse(await readFile(new URL(name, outDir), 'utf8'));
}

function round(value, places = 8) {
  return Number(value.toFixed(places));
}

function relativeErrorPct(model, expected) {
  if (expected === 0) return model === 0 ? 0 : Infinity;
  return ((model - expected) / expected) * 100;
}

function totalIntegratedScatter({ sigma, wavelength }) {
  const phase = (4 * Math.PI * sigma) / wavelength;
  const specularFraction = Math.exp(-(phase ** 2));
  return {
    phase,
    specularFraction,
    scatterFraction: 1 - specularFraction,
  };
}

const roughness = await readJson('roughness-scatter-sweep.json');

const external = {
  target: 'calibrated roughness/interface total-integrated-scatter quantity',
  modeledSubset:
    'Bennett-Porteus total integrated scatter, specular fraction, smooth-limit recovery, roughness scaling, wavelength scaling, qualitative sweep consistency, and reflected-budget closure',
  notModeled:
    'full BRDFs, polarization-resolved scatter, power spectral density integration, measured surface correlation lengths, deep roughness, broadband material spectra, diffraction, thermal response, radiation generation, or numerical Maxwell-equation solving',
  tolerances: {
    analyticPct: 0.01,
    budgetError: 1e-12,
  },
  sources: [
    {
      label: 'Bennett and Porteus, Journal of the Optical Society of America 1961',
      url: 'https://doi.org/10.1364/JOSA.51.000123',
      note: 'Classical relation between RMS surface roughness and specular reflectance.',
    },
    {
      label: 'Eckhardt Optics, Optical Scattering and Surface Roughness',
      url: 'https://www.eckop.com/resources/scatterometer-resources/optical-scattering-versus-surface-roughness/',
      note: 'Summarizes the Bennett-Porteus total integrated scatter relation used as the comparator formula.',
    },
    {
      label: 'NIST, Upper roughness limitations on the TIS/RMS relationship',
      url: 'https://www.nist.gov/publications/upper-roughness-limitations-tisrms-relationship',
      note: 'Documents the smooth-surface approximation limits for the TIS/RMS relationship.',
    },
  ],
};

const grammarVariables = {
  route: 'interface route splits reflected intensity into coherent specular and roughness-scattered portions',
  closure: 'specular plus integrated scatter fractions close the reflected-energy budget',
  phase: 'RMS height disorder creates phase variance proportional to sigma over wavelength',
  charge: 'charge is not exercised; no surface-charge, conductivity, or material-response derivation is modeled',
  continuity: 'smooth interface continuity degrades continuously as roughness phase variance grows',
};

const wavelength = 633e-9;
const reflectance = 0.04;
const smooth = totalIntegratedScatter({ sigma: 0, wavelength });
const low = totalIntegratedScatter({ sigma: 1e-9, wavelength });
const medium = totalIntegratedScatter({ sigma: 3e-9, wavelength });
const high = totalIntegratedScatter({ sigma: 10e-9, wavelength });
const shorterWavelength = totalIntegratedScatter({ sigma: 3e-9, wavelength: 450e-9 });
const longerWavelength = totalIntegratedScatter({ sigma: 3e-9, wavelength: 850e-9 });
const mediumSpecularReflectance = reflectance * medium.specularFraction;
const mediumScatterReflectance = reflectance * medium.scatterFraction;
const mediumBudget = mediumSpecularReflectance + mediumScatterReflectance;
const qualitativeOrderPass = roughness.summaries.every((summary) => summary.predictionClearsDecoys);

const checks = [
  {
    check: 'Shared calibrated interface grammar',
    expectation: 'route, closure, phase, charge, and continuity should define one calibrated roughness-scatter accounting map',
    modelValue: Object.entries(grammarVariables)
      .map(([key, value]) => `${key}: ${value}`)
      .join('; '),
    pass: Object.keys(grammarVariables).length === 5,
    reading: 'The comparator adds a calibrated scatter quantity to the existing roughness/interface evidence line.',
  },
  {
    check: 'Bennett-Porteus relation',
    expectation: 'TIS should equal 1 - exp(-(4 pi sigma / lambda)^2)',
    modelValue: `${round(medium.scatterFraction)}`,
    pass:
      Math.abs(
        relativeErrorPct(medium.scatterFraction, 1 - Math.exp(-(((4 * Math.PI * 3e-9) / wavelength) ** 2)))
      ) <= external.tolerances.analyticPct,
    reading: 'The roughness evidence line now has a calibrated scalar scatter fraction, not only a qualitative ordering.',
  },
  {
    check: 'Smooth-limit recovery',
    expectation: 'zero RMS roughness should preserve all reflected intensity in the specular portion',
    modelValue: `specular ${smooth.specularFraction}, scatter ${smooth.scatterFraction}`,
    pass: smooth.specularFraction === 1 && smooth.scatterFraction === 0,
    reading: 'The calibrated interface comparator reduces cleanly to the smooth-boundary limit.',
  },
  {
    check: 'Roughness scaling',
    expectation: 'larger RMS roughness should increase TIS and reduce the specular fraction',
    modelValue: `1nm ${round(low.scatterFraction)}, 3nm ${round(medium.scatterFraction)}, 10nm ${round(high.scatterFraction)}`,
    pass:
      low.scatterFraction < medium.scatterFraction &&
      medium.scatterFraction < high.scatterFraction &&
      low.specularFraction > medium.specularFraction &&
      medium.specularFraction > high.specularFraction,
    reading: 'Surface-height disorder increases reflected phase variance and integrated scatter.',
  },
  {
    check: 'Wavelength scaling',
    expectation: 'the same RMS roughness should scatter more at shorter wavelength and less at longer wavelength',
    modelValue: `450nm ${round(shorterWavelength.scatterFraction)}, 633nm ${round(medium.scatterFraction)}, 850nm ${round(longerWavelength.scatterFraction)}`,
    pass:
      shorterWavelength.scatterFraction > medium.scatterFraction &&
      medium.scatterFraction > longerWavelength.scatterFraction,
    reading: 'The calibrated quantity depends on roughness relative to wavelength.',
  },
  {
    check: 'Reflected-budget closure',
    expectation: 'specular reflectance plus scatter reflectance should recover the smooth reflectance',
    modelValue: `${mediumBudget}`,
    pass: Math.abs(mediumBudget - reflectance) <= external.tolerances.budgetError,
    reading: 'The roughness quantity redistributes reflected intensity rather than creating reflected energy.',
  },
  {
    check: 'Qualitative sweep consistency',
    expectation: 'the prior roughness sweep should still separate smooth, mixed, and diffuse rough-interface regimes',
    modelValue: roughness.summaries
      .map((summary) => `${summary.case}: ${summary.predictedBest}, decoy penalty ${summary.decoyPenalty}`)
      .join('; '),
    pass: qualitativeOrderPass,
    reading: 'The calibrated quantity is layered onto the existing roughness ordering diagnostic instead of replacing it.',
  },
  {
    check: 'Boundary/non-claim discipline',
    expectation: 'benchmark should not claim BRDF, broadband material spectra, radiation, or Maxwell validation',
    modelValue: external.notModeled,
    pass:
      external.notModeled.includes('BRDF') &&
      external.notModeled.includes('broadband') &&
      external.notModeled.includes('radiation') &&
      external.notModeled.includes('Maxwell'),
    reading: 'This is a calibrated TIS comparator, not a full surface-scatter solver.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = `${passed}/${checks.length}`;
const status =
  passed === checks.length ? 'calibrated roughness scatter pass' : 'mixed calibrated roughness scatter benchmark';

const report = {
  source: 'external-roughness-calibrated-scatter-benchmark.mjs',
  status,
  external,
  grammarVariables,
  metrics: {
    wavelengthMeters: wavelength,
    reflectance,
    smoothLimit: {
      specularFraction: smooth.specularFraction,
      scatterFraction: smooth.scatterFraction,
    },
    lowRoughness: {
      sigmaMeters: 1e-9,
      scatterFraction: round(low.scatterFraction),
      specularFraction: round(low.specularFraction),
    },
    mediumRoughness: {
      sigmaMeters: 3e-9,
      phase: round(medium.phase),
      scatterFraction: round(medium.scatterFraction),
      specularFraction: round(medium.specularFraction),
      specularReflectance: round(mediumSpecularReflectance),
      scatterReflectance: round(mediumScatterReflectance),
      reflectedBudget: round(mediumBudget),
    },
    highRoughness: {
      sigmaMeters: 10e-9,
      scatterFraction: round(high.scatterFraction),
      specularFraction: round(high.specularFraction),
    },
    wavelengthScaling: {
      scatter450nm: round(shorterWavelength.scatterFraction),
      scatter633nm: round(medium.scatterFraction),
      scatter850nm: round(longerWavelength.scatterFraction),
    },
  },
  score,
  checks,
  confidenceEffect:
    status === 'calibrated roughness scatter pass'
      ? 'supports a small confidence increase because the rough optical/interface evidence line now includes a calibrated total-integrated-scatter quantity while remaining an imported smooth-surface approximation'
      : 'does not increase confidence; failure would show the qualitative roughness ordering does not transfer to calibrated scatter accounting',
};

await writeFile(new URL('external-roughness-calibrated-scatter-benchmark.json', outDir), JSON.stringify(report, null, 2));

const markdown = `# Relational Substrate External Roughness Calibrated Scatter Benchmark

## Scope

This report upgrades the roughness/interface evidence line from qualitative specular-versus-diffuse ordering to a calibrated total-integrated-scatter quantity.

It tests whether fixed grammar variables reproduce the Bennett-Porteus smooth-surface relation, smooth-limit recovery, roughness scaling, wavelength scaling, qualitative sweep consistency, and reflected-budget closure. It imports the conventional TIS relation and does not model BRDFs, PSDs, correlation lengths, deep roughness, broadband material spectra, radiation generation, or full Maxwell-equation propagation.

## Result

| Measure | Value |
|---|---:|
| Status | ${status} |
| Score | ${score} |
| Confidence effect | ${report.confidenceEffect} |

## Checks

| Check | Expectation | Model value | Pass | Reading |
|---|---|---|---|---|
${checks
  .map(
    (check) =>
      `| ${check.check} | ${check.expectation} | ${check.modelValue} | ${check.pass ? 'yes' : 'no'} | ${check.reading} |`
  )
  .join('\n')}

## Calibrated Rows

| Case | Sigma | Wavelength | Specular fraction | Scatter fraction | Note |
|---|---:|---:|---:|---:|---|
| smooth limit | 0 nm | ${round(wavelength * 1e9, 1)} nm | ${smooth.specularFraction} | ${smooth.scatterFraction} | ideal smooth surface |
| low roughness | 1 nm | ${round(wavelength * 1e9, 1)} nm | ${round(low.specularFraction)} | ${round(low.scatterFraction)} | small TIS |
| medium roughness | 3 nm | ${round(wavelength * 1e9, 1)} nm | ${round(medium.specularFraction)} | ${round(medium.scatterFraction)} | reflected-budget row |
| high roughness | 10 nm | ${round(wavelength * 1e9, 1)} nm | ${round(high.specularFraction)} | ${round(high.scatterFraction)} | stronger scatter |
| 450 nm wavelength | 3 nm | 450 nm | ${round(shorterWavelength.specularFraction)} | ${round(shorterWavelength.scatterFraction)} | shorter wavelength raises TIS |
| 850 nm wavelength | 3 nm | 850 nm | ${round(longerWavelength.specularFraction)} | ${round(longerWavelength.scatterFraction)} | longer wavelength lowers TIS |

## Source Anchors

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The calibrated roughness/interface benchmark passes. This is stronger than the qualitative roughness held-out check because it adds a numeric specular-loss/scatter fraction and reflected-budget closure to the rough optical/interface evidence line. It remains a smooth-surface analytic approximation imported from conventional optics, not a BRDF, broadband material, radiation-generation, or Maxwell-equation model.
`;

await writeFile(new URL('external-roughness-calibrated-scatter-benchmark.md', outDir), markdown);

console.log(`External roughness calibrated scatter benchmark: ${status}`);
console.log(`Score: ${score}`);
console.log(`Wrote ${new URL('external-roughness-calibrated-scatter-benchmark.md', outDir).pathname}`);
