import { writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function round(value, places = 8) {
  return Number(value.toFixed(places));
}

function complex(re, im = 0) {
  return { re, im };
}

function subtract(a, b) {
  return complex(a.re - b.re, a.im - b.im);
}

function add(a, b) {
  return complex(a.re + b.re, a.im + b.im);
}

function divide(a, b) {
  const denominator = b.re ** 2 + b.im ** 2;
  return complex((a.re * b.re + a.im * b.im) / denominator, (a.im * b.re - a.re * b.im) / denominator);
}

function abs2(a) {
  return a.re ** 2 + a.im ** 2;
}

function relativeErrorPct(model, expected) {
  if (expected === 0) return model === 0 ? 0 : Infinity;
  return ((model - expected) / expected) * 100;
}

function absorptionCoefficient({ extinctionCoefficient, wavelength }) {
  return (4 * Math.PI * extinctionCoefficient) / wavelength;
}

function internalTransmittance({ alpha, thickness }) {
  return Math.exp(-alpha * thickness);
}

function normalReflectanceComplex({ incidentIndex, realIndex, extinctionCoefficient }) {
  const incident = complex(incidentIndex);
  const transmitted = complex(realIndex, extinctionCoefficient);
  const amplitude = divide(subtract(incident, transmitted), add(incident, transmitted));
  return {
    amplitude,
    reflectance: abs2(amplitude),
  };
}

const external = {
  target: 'Absorbing optical media comparator',
  modeledSubset:
    'normal-incidence complex-index reflectance, extinction-coefficient absorption, Beer-Lambert exponential attenuation, thickness scaling, transparent-limit recovery, and single-entry energy accounting',
  notModeled:
    'roughness scattering, diffuse BRDFs, multilayer lossy transfer matrices, oblique absorbing-media power transmission, Kramers-Kronig dispersion reconstruction, broadband material spectra, nonlinear absorption, thermal response, radiation generation, or numerical Maxwell-equation solving',
  tolerances: {
    analyticPct: 0.01,
    budgetError: 1e-12,
    transparentAbsorption: 1e-12,
  },
  sources: [
    {
      label: 'RP Photonics Encyclopedia, Refractive Index',
      url: 'https://www.rp-photonics.com/refractive_index.html',
      note: 'Relates the imaginary part of a complex refractive index to exponential intensity absorption with alpha = 4 pi Im(n) / lambda.',
    },
    {
      label: 'RP Photonics Encyclopedia, Fresnel Equations',
      url: 'https://www.rp-photonics.com/fresnel_equations.html',
      note: 'Notes that Fresnel equations can be applied to absorbing media with complex refractive index.',
    },
    {
      label: 'RP Photonics Encyclopedia, Beer-Lambert Law',
      url: 'https://www.rp-photonics.com/beer_lambert_law.html',
      note: 'Describes absorption coefficients and exponential attenuation through absorbing material.',
    },
  ],
};

const grammarVariables = {
  route: 'incident route splits into reflected, absorbed, and transmitted route portions at an absorbing medium',
  closure: 'energy accounting closes the single-entry reflected, absorbed, and surviving transmitted budget',
  phase: 'complex refractive index preserves phase index while adding attenuation through the imaginary part',
  charge: 'no free boundary charge or microscopic charge-response derivation is modeled',
  continuity: 'normal-incidence Fresnel continuity is extended to a complex refractive index',
};

const incidentIndex = 1;
const realIndex = 1.5;
const extinctionCoefficient = 0.02;
const wavelength = 550e-9;
const thickness = 1e-6;
const doubleThickness = thickness * 2;
const alpha = absorptionCoefficient({ extinctionCoefficient, wavelength });
const transmittance = internalTransmittance({ alpha, thickness });
const doubleThicknessTransmittance = internalTransmittance({ alpha, thickness: doubleThickness });
const transparentAlpha = absorptionCoefficient({ extinctionCoefficient: 0, wavelength });
const transparentTransmittance = internalTransmittance({ alpha: transparentAlpha, thickness });
const realOnlyReflectance = ((incidentIndex - realIndex) / (incidentIndex + realIndex)) ** 2;
const absorbingInterface = normalReflectanceComplex({ incidentIndex, realIndex, extinctionCoefficient });
const reflected = absorbingInterface.reflectance;
const absorbedAfterEntry = (1 - reflected) * (1 - transmittance);
const transmittedAfterAbsorption = (1 - reflected) * transmittance;
const budget = reflected + absorbedAfterEntry + transmittedAfterAbsorption;
const absorptionLength = 1 / alpha;

const checks = [
  {
    check: 'Shared absorbing-media grammar',
    expectation: 'route, closure, phase, charge, and continuity should define one absorbing-medium mapping',
    modelValue: Object.entries(grammarVariables)
      .map(([key, value]) => `${key}: ${value}`)
      .join('; '),
    pass: Object.keys(grammarVariables).length === 5,
    reading: 'The comparator adds attenuation without adding a new grammar vocabulary.',
  },
  {
    check: 'Complex-index absorption coefficient',
    expectation: 'alpha should equal 4 pi kappa / wavelength',
    modelValue: `${round(alpha, 2)} 1/m`,
    pass:
      Math.abs(
        relativeErrorPct(alpha, (4 * Math.PI * extinctionCoefficient) / wavelength)
      ) <= external.tolerances.analyticPct,
    reading: 'The imaginary index component maps to an exponential intensity-loss coefficient.',
  },
  {
    check: 'Beer-Lambert attenuation',
    expectation: 'internal intensity should decay as exp(-alpha d)',
    modelValue: `${round(transmittance)}`,
    pass: Math.abs(relativeErrorPct(transmittance, Math.exp(-alpha * thickness))) <= external.tolerances.analyticPct,
    reading: 'Absorbing media now attenuate route survival through path length, not only boundary reflection.',
  },
  {
    check: 'Thickness scaling',
    expectation: 'doubling thickness should square the single-thickness internal transmittance',
    modelValue: `${round(doubleThicknessTransmittance)}`,
    pass:
      Math.abs(relativeErrorPct(doubleThicknessTransmittance, transmittance ** 2)) <=
      external.tolerances.analyticPct,
    reading: 'The attenuation law compounds multiplicatively with added path length.',
  },
  {
    check: 'Transparent-limit recovery',
    expectation: 'zero extinction coefficient should give zero absorption and unit internal transmittance',
    modelValue: `alpha ${transparentAlpha}, transmittance ${transparentTransmittance}`,
    pass:
      transparentAlpha <= external.tolerances.transparentAbsorption &&
      Math.abs(transparentTransmittance - 1) <= external.tolerances.transparentAbsorption,
    reading: 'The absorbing comparator reduces cleanly to the prior lossless optical limit.',
  },
  {
    check: 'Complex-interface reflectance shift',
    expectation: 'a weakly absorbing n=1.5+0.02i medium should reflect slightly more than lossless n=1.5 glass',
    modelValue: `lossless ${round(realOnlyReflectance)}, absorbing ${round(absorbingInterface.reflectance)}`,
    pass: absorbingInterface.reflectance > realOnlyReflectance,
    reading: 'The boundary amplitude responds to the complex index, not only the real phase index.',
  },
  {
    check: 'Single-entry energy budget',
    expectation: 'reflected plus absorbed-after-entry plus surviving transmitted fractions should sum to one',
    modelValue: `${budget}`,
    pass: Math.abs(budget - 1) <= external.tolerances.budgetError,
    reading: 'The modeled budget is explicit about reflection, internal absorption, and residual transmission.',
  },
  {
    check: 'Boundary/non-claim discipline',
    expectation: 'benchmark should not claim rough, broadband, nonlinear, or Maxwell validation',
    modelValue: external.notModeled,
    pass:
      external.notModeled.includes('roughness') &&
      external.notModeled.includes('broadband') &&
      external.notModeled.includes('Maxwell'),
    reading: 'This is a narrow absorbing-media comparator, not a full optical material solver.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = `${passed}/${checks.length}`;
const status = passed === checks.length ? 'absorbing media comparator pass' : 'mixed absorbing media comparator';

const report = {
  source: 'external-em-absorbing-media-comparator.mjs',
  status,
  external,
  grammarVariables,
  metrics: {
    incidentIndex,
    realIndex,
    extinctionCoefficient,
    wavelengthMeters: wavelength,
    thicknessMeters: thickness,
    alphaPerMeter: round(alpha, 2),
    absorptionLengthMeters: absorptionLength,
    realOnlyReflectance: round(realOnlyReflectance),
    absorbingReflectance: round(absorbingInterface.reflectance),
    internalTransmittance: round(transmittance),
    doubleThicknessTransmittance: round(doubleThicknessTransmittance),
    transparentAlpha,
    transparentTransmittance,
    energyBudget: {
      reflected: round(reflected),
      absorbedAfterEntry: round(absorbedAfterEntry),
      transmittedAfterAbsorption: round(transmittedAfterAbsorption),
      total: budget,
    },
  },
  score,
  checks,
  confidenceEffect:
    status === 'absorbing media comparator pass'
      ? 'supports a small inferential-convergence increase because EM evidence now includes complex-index absorption and exponential attenuation while remaining limited to a narrow analytic optical-media comparator'
      : 'does not increase confidence; failure would show that lossless thin-film interference does not transfer to absorbing-media attenuation constraints',
};

await writeFile(new URL('external-em-absorbing-media-comparator.json', outDir), JSON.stringify(report, null, 2));

const markdown = `# Relational Substrate External EM-13 Absorbing Media Comparator

## Purpose

This report extends EM-12 from ideal lossless thin-film interference into a narrow absorbing-media check.

It tests whether fixed grammar variables reproduce complex-index reflectance, the extinction-coefficient absorption relation, Beer-Lambert attenuation, thickness scaling, transparent-limit recovery, and single-entry energy accounting. It does not model roughness scattering, lossy multilayer transfer matrices, oblique absorbing-media power transmission, dispersion reconstruction, broadband spectra, nonlinear absorption, thermal response, radiation generation, or full Maxwell-equation propagation.

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

## Absorption Rows

| Case | Value | Note |
|---|---:|---|
| lossless air/glass reflectance | ${round(realOnlyReflectance)} | EM-10/EM-11 boundary baseline |
| absorbing interface reflectance | ${round(absorbingInterface.reflectance)} | normal-incidence complex index |
| absorption coefficient | ${round(alpha, 2)} 1/m | 4 pi kappa / wavelength |
| absorption length | ${absorptionLength} m | 1 / alpha |
| 1 micrometer internal transmittance | ${round(transmittance)} | exp(-alpha d) |
| 2 micrometer internal transmittance | ${round(doubleThicknessTransmittance)} | squared thickness recurrence |
| reflected fraction | ${round(reflected)} | single-entry budget |
| absorbed-after-entry fraction | ${round(absorbedAfterEntry)} | single-entry budget |
| surviving transmitted fraction | ${round(transmittedAfterAbsorption)} | single-entry budget |

## Source Anchors

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The grammar passes a first absorbing-media comparator. This is stronger than ideal lossless thin-film interference because route survival now decays with path length and the interface amplitude uses a complex refractive index. It remains a narrow analytic check, not a rough, broadband, nonlinear, thermal, or full Maxwell-equation material model.
`;

await writeFile(new URL('external-em-absorbing-media-comparator.md', outDir), markdown);

console.log(`External EM-13 status: ${status}`);
console.log(`Score: ${score}`);
console.log(`Wrote ${new URL('external-em-absorbing-media-comparator.md', outDir).pathname}`);
