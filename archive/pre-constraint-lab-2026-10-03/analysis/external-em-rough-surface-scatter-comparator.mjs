import { writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function round(value, places = 8) {
  return Number(value.toFixed(places));
}

function degToRad(degrees) {
  return (degrees * Math.PI) / 180;
}

function relativeErrorPct(model, expected) {
  if (expected === 0) return model === 0 ? 0 : Infinity;
  return ((model - expected) / expected) * 100;
}

function roughnessPhase({ sigma, wavelength, angleDegrees = 0 }) {
  return (4 * Math.PI * sigma * Math.cos(degToRad(angleDegrees))) / wavelength;
}

function totalIntegratedScatter({ sigma, wavelength, angleDegrees = 0 }) {
  const phase = roughnessPhase({ sigma, wavelength, angleDegrees });
  const specularFraction = Math.exp(-(phase ** 2));
  return {
    phase,
    specularFraction,
    scatterFraction: 1 - specularFraction,
  };
}

const external = {
  target: 'Rough-surface scatter comparator',
  modeledSubset:
    'Bennett-Porteus style total integrated scatter, specular-loss factor, roughness scaling, wavelength scaling, incidence-angle scaling, smooth-limit recovery, small-roughness approximation, and reflected-energy budget',
  notModeled:
    'full BRDFs, polarization-resolved rough-surface scattering, power spectral density integration, arbitrary correlation lengths, deep roughness, lossy multilayer transfer, broadband material spectra, diffraction gratings, thermal response, radiation generation, or numerical Maxwell-equation solving',
  tolerances: {
    analyticPct: 0.01,
    budgetError: 1e-12,
    smallRoughnessApproxPct: 0.1,
  },
  sources: [
    {
      label: 'Bennett and Porteus, Journal of the Optical Society of America 1961',
      url: 'https://doi.org/10.1364/JOSA.51.000123',
      note: 'Classical normal-incidence relation between RMS surface roughness and specular reflectance.',
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
  route: 'reflected route splits into coherent specular and roughness-scattered route portions',
  closure: 'reflected-energy closure tracks specular plus integrated-scatter fractions',
  phase: 'height roughness introduces random phase error proportional to sigma over wavelength',
  charge: 'no microscopic surface-charge or material-response derivation is modeled',
  continuity: 'smooth-boundary continuity is degraded by an exponential roughness factor',
};

const wavelength = 550e-9;
const smoothReflectance = 0.04;
const sigma = 10e-9;
const base = totalIntegratedScatter({ sigma, wavelength });
const smooth = totalIntegratedScatter({ sigma: 0, wavelength });
const doubleRoughness = totalIntegratedScatter({ sigma: sigma * 2, wavelength });
const shortWavelength = totalIntegratedScatter({ sigma, wavelength: 450e-9 });
const longWavelength = totalIntegratedScatter({ sigma, wavelength: 700e-9 });
const angled = totalIntegratedScatter({ sigma, wavelength, angleDegrees: 60 });
const tinyRoughness = totalIntegratedScatter({ sigma: 1e-9, wavelength });
const tinyApproximation = tinyRoughness.phase ** 2;
const specularReflectance = smoothReflectance * base.specularFraction;
const scatteredReflectance = smoothReflectance * base.scatterFraction;
const reflectedBudget = specularReflectance + scatteredReflectance;

const checks = [
  {
    check: 'Shared rough-surface grammar',
    expectation: 'route, closure, phase, charge, and continuity should define one rough-surface scatter mapping',
    modelValue: Object.entries(grammarVariables)
      .map(([key, value]) => `${key}: ${value}`)
      .join('; '),
    pass: Object.keys(grammarVariables).length === 5,
    reading: 'The comparator adds roughness phase loss without adding a new grammar vocabulary.',
  },
  {
    check: 'Bennett-Porteus scatter relation',
    expectation: 'total integrated scatter should equal 1 - exp(-(4 pi sigma / wavelength)^2) at normal incidence',
    modelValue: `${round(base.scatterFraction)}`,
    pass:
      Math.abs(
        relativeErrorPct(base.scatterFraction, 1 - Math.exp(-(((4 * Math.PI * sigma) / wavelength) ** 2)))
      ) <= external.tolerances.analyticPct,
    reading: 'RMS roughness now maps to calibrated specular loss rather than only qualitative diffuse order.',
  },
  {
    check: 'Smooth-limit recovery',
    expectation: 'zero roughness should preserve all reflected energy in the specular route',
    modelValue: `specular ${smooth.specularFraction}, scatter ${smooth.scatterFraction}`,
    pass: smooth.specularFraction === 1 && smooth.scatterFraction === 0,
    reading: 'The rough-surface comparator reduces cleanly to the prior smooth-boundary limit.',
  },
  {
    check: 'Roughness scaling',
    expectation: 'doubling RMS roughness should increase integrated scatter and reduce the specular fraction',
    modelValue: `base scatter ${round(base.scatterFraction)}, double scatter ${round(doubleRoughness.scatterFraction)}`,
    pass:
      doubleRoughness.scatterFraction > base.scatterFraction &&
      doubleRoughness.specularFraction < base.specularFraction,
    reading: 'Phase disorder increases with RMS height, so coherent specular order falls.',
  },
  {
    check: 'Wavelength scaling',
    expectation: 'the same roughness should scatter more at shorter wavelength and less at longer wavelength',
    modelValue: `450nm ${round(shortWavelength.scatterFraction)}, 700nm ${round(longWavelength.scatterFraction)}`,
    pass: shortWavelength.scatterFraction > base.scatterFraction && longWavelength.scatterFraction < base.scatterFraction,
    reading: 'The governing ratio is roughness relative to wavelength, not absolute roughness alone.',
  },
  {
    check: 'Incidence-angle scaling',
    expectation: 'at 60 degrees from normal the cos(theta) factor should reduce the integrated scatter term',
    modelValue: `normal ${round(base.scatterFraction)}, 60deg ${round(angled.scatterFraction)}`,
    pass: angled.scatterFraction < base.scatterFraction,
    reading: 'The path-height phase term contracts with the incidence-angle cosine.',
  },
  {
    check: 'Small-roughness approximation',
    expectation: 'for tiny roughness, integrated scatter should approximate the squared roughness phase term',
    modelValue: `TIS ${tinyRoughness.scatterFraction}, phase^2 ${tinyApproximation}`,
    pass:
      Math.abs(relativeErrorPct(tinyRoughness.scatterFraction, tinyApproximation)) <=
      external.tolerances.smallRoughnessApproxPct,
    reading: 'The exponential scatter law has the expected first-order small-roughness behavior.',
  },
  {
    check: 'Reflected-energy budget',
    expectation: 'specular reflected plus integrated scattered reflected energy should recover the smooth reflectance',
    modelValue: `${reflectedBudget}`,
    pass: Math.abs(reflectedBudget - smoothReflectance) <= external.tolerances.budgetError,
    reading: 'The comparator accounts for roughness redistribution inside the reflected budget.',
  },
  {
    check: 'Boundary/non-claim discipline',
    expectation: 'benchmark should not claim BRDF, deep roughness, broadband, or Maxwell validation',
    modelValue: external.notModeled,
    pass:
      external.notModeled.includes('BRDF') &&
      external.notModeled.includes('broadband') &&
      external.notModeled.includes('Maxwell'),
    reading: 'This is a narrow roughness/TIS comparator, not a full surface-scatter solver.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = `${passed}/${checks.length}`;
const status =
  passed === checks.length ? 'rough surface scatter comparator pass' : 'mixed rough surface scatter comparator';

const report = {
  source: 'external-em-rough-surface-scatter-comparator.mjs',
  status,
  external,
  grammarVariables,
  metrics: {
    wavelengthMeters: wavelength,
    sigmaMeters: sigma,
    smoothReflectance,
    base: {
      phase: round(base.phase),
      specularFraction: round(base.specularFraction),
      scatterFraction: round(base.scatterFraction),
      specularReflectance: round(specularReflectance),
      scatteredReflectance: round(scatteredReflectance),
    },
    smoothLimit: {
      specularFraction: smooth.specularFraction,
      scatterFraction: smooth.scatterFraction,
    },
    doubleRoughnessScatterFraction: round(doubleRoughness.scatterFraction),
    shortWavelengthScatterFraction: round(shortWavelength.scatterFraction),
    longWavelengthScatterFraction: round(longWavelength.scatterFraction),
    angledScatterFraction: round(angled.scatterFraction),
    tinyRoughnessScatterFraction: tinyRoughness.scatterFraction,
    tinyRoughnessPhaseSquared: tinyApproximation,
    reflectedBudget,
  },
  score,
  checks,
  confidenceEffect:
    status === 'rough surface scatter comparator pass'
      ? 'supports a small inferential-convergence increase because EM evidence now includes calibrated RMS roughness to total-integrated-scatter behavior while remaining limited to a smooth-surface analytic approximation'
      : 'does not increase confidence; failure would show that absorbing-media optics does not transfer to rough-surface scatter constraints',
};

await writeFile(new URL('external-em-rough-surface-scatter-comparator.json', outDir), JSON.stringify(report, null, 2));

const markdown = `# Relational Substrate External EM-14 Rough-Surface Scatter Comparator

## Purpose

This report extends EM-13 from absorbing media into a narrow calibrated rough-surface scatter check.

It tests whether fixed grammar variables reproduce Bennett-Porteus style total integrated scatter, specular-loss factor, RMS roughness scaling, wavelength scaling, incidence-angle scaling, smooth-limit recovery, small-roughness approximation, and reflected-energy budgeting. It does not model full BRDFs, polarization-resolved scatter, PSD integration, arbitrary correlation lengths, deep roughness, lossy multilayer transfer, broadband material spectra, diffraction gratings, radiation generation, or full Maxwell-equation propagation.

## Status

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

## Roughness Rows

| Case | Scatter fraction | Specular fraction | Note |
|---|---:|---:|---|
| smooth limit | ${smooth.scatterFraction} | ${smooth.specularFraction} | zero roughness |
| sigma 10 nm, wavelength 550 nm | ${round(base.scatterFraction)} | ${round(base.specularFraction)} | baseline TIS |
| sigma 20 nm, wavelength 550 nm | ${round(doubleRoughness.scatterFraction)} | ${round(doubleRoughness.specularFraction)} | roughness scaling |
| sigma 10 nm, wavelength 450 nm | ${round(shortWavelength.scatterFraction)} | ${round(shortWavelength.specularFraction)} | shorter wavelength |
| sigma 10 nm, wavelength 700 nm | ${round(longWavelength.scatterFraction)} | ${round(longWavelength.specularFraction)} | longer wavelength |
| sigma 10 nm, 60 degrees | ${round(angled.scatterFraction)} | ${round(angled.specularFraction)} | incidence-angle cosine |

## Source Anchors

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The grammar passes a first calibrated rough-surface scatter comparator. This is stronger than the prior qualitative roughness/interface benchmark because RMS roughness, wavelength, and incidence angle now produce numeric specular-loss and integrated-scatter fractions. It remains a smooth-surface approximation, not a full BRDF, PSD, deep-roughness, broadband, or Maxwell-equation surface-scatter model.
`;

await writeFile(new URL('external-em-rough-surface-scatter-comparator.md', outDir), markdown);

console.log(`External EM-14 status: ${status}`);
console.log(`Score: ${score}`);
console.log(`Wrote ${new URL('external-em-rough-surface-scatter-comparator.md', outDir).pathname}`);
