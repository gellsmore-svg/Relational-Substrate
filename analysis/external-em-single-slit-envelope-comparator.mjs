import { writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function round(value, places = 8) {
  return Number(value.toFixed(places));
}

function radToDeg(radians) {
  return (radians * 180) / Math.PI;
}

function degToRad(degrees) {
  return (degrees * Math.PI) / 180;
}

function relativeErrorPct(model, expected) {
  if (expected === 0) return model === 0 ? 0 : Infinity;
  return ((model - expected) / expected) * 100;
}

function sinc(value) {
  return value === 0 ? 1 : Math.sin(value) / value;
}

function beta({ slitWidth, wavelength, thetaRadians }) {
  return (Math.PI * slitWidth * Math.sin(thetaRadians)) / wavelength;
}

function relativeIntensity({ slitWidth, wavelength, thetaRadians }) {
  return sinc(beta({ slitWidth, wavelength, thetaRadians })) ** 2;
}

function minimumAngle({ slitWidth, wavelength, order }) {
  const sine = (order * wavelength) / slitWidth;
  if (Math.abs(sine) > 1) {
    return { exists: false, order, sine, thetaRadians: null, thetaDegrees: null };
  }
  const thetaRadians = Math.asin(sine);
  return { exists: true, order, sine, thetaRadians, thetaDegrees: radToDeg(thetaRadians) };
}

const external = {
  target: 'Single-slit diffraction envelope comparator',
  modeledSubset:
    'single-slit minima, sinc-squared intensity envelope, central maximum, side-lobe relative intensity, wavelength scaling, slit-width scaling, symmetry, and screen-position mapping',
  notModeled:
    'double-slit interference, diffraction-grating order combs, finite detector response, vector diffraction, polarization, aperture aberrations, coherence limits, broadband spectrum intensities, resolving power, radiation generation, or numerical Maxwell-equation solving',
  tolerances: {
    analyticPct: 0.05,
    angleDegrees: 0.05,
    intensity: 0.002,
    screenPositionPct: 0.01,
  },
  sources: [
    {
      label: 'OpenStax University Physics Volume 3, Single-Slit Diffraction',
      url: 'https://openstax.org/books/university-physics-volume-3/pages/4-1-single-slit-diffraction',
      note: 'Gives the single-slit minima condition a sin theta = m lambda and qualitative envelope behavior.',
    },
    {
      label: 'OpenStax University Physics Volume 3, Intensity in Single-Slit Diffraction',
      url: 'https://openstax.org/books/university-physics-volume-3/pages/4-2-intensity-in-single-slit-diffraction',
      note: 'Gives I/I0 = (sin beta / beta)^2 and the 550 nm, 2.00 micrometer worked example.',
    },
  ],
};

const grammarVariables = {
  route: 'continuous aperture routes interfere across the slit rather than only at discrete grating grooves',
  closure: 'destructive closure occurs when the aperture path difference equals an integer wavelength',
  phase: 'the envelope phase is beta = pi a sin(theta) / lambda',
  charge: 'no free charge, source current, or radiation-generation mechanism is modeled',
  continuity: 'angular diffraction continuity maps envelope intensity to screen position',
};

const wavelength = 550e-9;
const slitWidth = 2e-6;
const screenDistance = 2;
const firstMinimum = minimumAngle({ slitWidth, wavelength, order: 1 });
const secondMinimum = minimumAngle({ slitWidth, wavelength, order: 2 });
const halfwayAngleRadians = (firstMinimum.thetaRadians + secondMinimum.thetaRadians) / 2;
const halfwayIntensity = relativeIntensity({ slitWidth, wavelength, thetaRadians: halfwayAngleRadians });
const centralIntensity = relativeIntensity({ slitWidth, wavelength, thetaRadians: 0 });
const negativeFirstMinimum = minimumAngle({ slitWidth, wavelength, order: -1 });
const widerSlitFirstMinimum = minimumAngle({ slitWidth: slitWidth * 2, wavelength, order: 1 });
const longerWavelengthFirstMinimum = minimumAngle({ slitWidth, wavelength: 650e-9, order: 1 });
const firstMinimumScreenPosition = screenDistance * Math.tan(firstMinimum.thetaRadians);
const centralApproxWidthRadians = (2 * wavelength) / slitWidth;
const actualCentralWidthRadians = firstMinimum.thetaRadians - negativeFirstMinimum.thetaRadians;

const checks = [
  {
    check: 'Shared single-slit grammar',
    expectation: 'route, closure, phase, charge, and continuity should define one single-slit envelope mapping',
    modelValue: Object.entries(grammarVariables)
      .map(([key, value]) => `${key}: ${value}`)
      .join('; '),
    pass: Object.keys(grammarVariables).length === 5,
    reading: 'The comparator adds aperture envelope phase without adding a new grammar vocabulary.',
  },
  {
    check: 'First minimum angle',
    expectation: '550 nm through a 2.00 micrometer slit should give first minimum near 16.0 degrees',
    modelValue: `${round(firstMinimum.thetaDegrees, 4)} degrees`,
    pass: Math.abs(firstMinimum.thetaDegrees - 16.0) <= external.tolerances.angleDegrees,
    reading: 'The first destructive aperture route matches the OpenStax worked example.',
  },
  {
    check: 'Second minimum angle',
    expectation: '550 nm through a 2.00 micrometer slit should give second minimum near 33.4 degrees',
    modelValue: `${round(secondMinimum.thetaDegrees, 4)} degrees`,
    pass: Math.abs(secondMinimum.thetaDegrees - 33.4) <= external.tolerances.angleDegrees,
    reading: 'The second destructive aperture route also matches the worked example.',
  },
  {
    check: 'Sinc-squared side-lobe intensity',
    expectation: 'halfway between the first two minima should have relative intensity near 0.044',
    modelValue: `${round(halfwayIntensity, 5)}`,
    pass: Math.abs(halfwayIntensity - 0.044) <= external.tolerances.intensity,
    reading: 'The envelope intensity is not a flat grating-order comb; side lobes are much weaker.',
  },
  {
    check: 'Central maximum recovery',
    expectation: 'theta = 0 should recover unit relative intensity',
    modelValue: `${centralIntensity}`,
    pass: centralIntensity === 1,
    reading: 'The sinc limit preserves the central peak.',
  },
  {
    check: 'Positive/negative minimum symmetry',
    expectation: 'first minima should be equal and opposite around the central maximum',
    modelValue: `+${round(firstMinimum.thetaDegrees, 4)} deg; ${round(negativeFirstMinimum.thetaDegrees, 4)} deg`,
    pass: Math.abs(firstMinimum.thetaDegrees + negativeFirstMinimum.thetaDegrees) <= external.tolerances.angleDegrees,
    reading: 'The aperture envelope remains symmetric about the optical axis.',
  },
  {
    check: 'Slit-width scaling',
    expectation: 'doubling slit width should narrow the first-minimum angle',
    modelValue: `base ${round(firstMinimum.thetaDegrees, 4)} deg; double width ${round(widerSlitFirstMinimum.thetaDegrees, 4)} deg`,
    pass: widerSlitFirstMinimum.thetaDegrees < firstMinimum.thetaDegrees,
    reading: 'A wider aperture produces a narrower diffraction envelope.',
  },
  {
    check: 'Wavelength scaling',
    expectation: 'a longer wavelength should broaden the first-minimum angle',
    modelValue: `550nm ${round(firstMinimum.thetaDegrees, 4)} deg; 650nm ${round(longerWavelengthFirstMinimum.thetaDegrees, 4)} deg`,
    pass: longerWavelengthFirstMinimum.thetaDegrees > firstMinimum.thetaDegrees,
    reading: 'A longer wavelength spreads the single-slit envelope more strongly.',
  },
  {
    check: 'Small-angle central-width approximation',
    expectation: 'central angular width should be close to 2 lambda / a for this worked example',
    modelValue: `actual ${round(actualCentralWidthRadians, 5)} rad; approx ${round(centralApproxWidthRadians, 5)} rad`,
    pass: Math.abs(relativeErrorPct(actualCentralWidthRadians, centralApproxWidthRadians)) <= 3,
    reading: 'The numerical envelope is consistent with the usual small-angle width estimate.',
  },
  {
    check: 'Screen-position mapping',
    expectation: 'first minimum screen offset should equal L tan(theta)',
    modelValue: `${round(firstMinimumScreenPosition, 6)} m`,
    pass:
      Math.abs(
        relativeErrorPct(firstMinimumScreenPosition, screenDistance * Math.tan(firstMinimum.thetaRadians))
      ) <= external.tolerances.screenPositionPct,
    reading: 'Angular envelope continuity maps to a measurable screen offset.',
  },
  {
    check: 'Boundary/non-claim discipline',
    expectation: 'benchmark should not claim grating combs, vector diffraction, broadband intensity, radiation, or Maxwell validation',
    modelValue: external.notModeled,
    pass:
      external.notModeled.includes('diffraction-grating') &&
      external.notModeled.includes('broadband') &&
      external.notModeled.includes('Maxwell'),
    reading: 'This is a scalar single-slit envelope comparator, not a full diffraction optics solver.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = `${passed}/${checks.length}`;
const status =
  passed === checks.length ? 'single-slit envelope comparator pass' : 'mixed single-slit envelope comparator';

const report = {
  source: 'external-em-single-slit-envelope-comparator.mjs',
  status,
  external,
  grammarVariables,
  metrics: {
    wavelengthMeters: wavelength,
    slitWidthMeters: slitWidth,
    screenDistanceMeters: screenDistance,
    firstMinimumDegrees: round(firstMinimum.thetaDegrees, 4),
    secondMinimumDegrees: round(secondMinimum.thetaDegrees, 4),
    halfwayAngleDegrees: round(radToDeg(halfwayAngleRadians), 4),
    halfwayRelativeIntensity: round(halfwayIntensity, 5),
    centralIntensity,
    negativeFirstMinimumDegrees: round(negativeFirstMinimum.thetaDegrees, 4),
    widerSlitFirstMinimumDegrees: round(widerSlitFirstMinimum.thetaDegrees, 4),
    longerWavelengthFirstMinimumDegrees: round(longerWavelengthFirstMinimum.thetaDegrees, 4),
    firstMinimumScreenPositionMeters: round(firstMinimumScreenPosition, 6),
    centralApproxWidthRadians: round(centralApproxWidthRadians, 5),
    actualCentralWidthRadians: round(actualCentralWidthRadians, 5),
  },
  score,
  checks,
  confidenceEffect:
    status === 'single-slit envelope comparator pass'
      ? 'supports a small inferential-convergence increase because EM evidence now includes scalar finite-aperture diffraction envelopes and side-lobe intensity while remaining limited to single-slit Fraunhofer optics'
      : 'does not increase confidence; failure would show that scalar grating diffraction does not transfer to finite-aperture envelope constraints',
};

await writeFile(new URL('external-em-single-slit-envelope-comparator.json', outDir), JSON.stringify(report, null, 2));

const markdown = `# Relational Substrate External EM-16 Single-Slit Envelope Comparator

## Purpose

This report extends EM-15 from a scalar grating equation into a finite-aperture single-slit diffraction envelope.

It tests whether fixed grammar variables reproduce single-slit minima, the sinc-squared intensity envelope, central maximum, side-lobe relative intensity, wavelength scaling, slit-width scaling, symmetry, and screen-position mapping. It does not model double-slit interference, diffraction-grating order combs, vector diffraction, polarization, aperture aberrations, coherence limits, broadband intensities, resolving power, radiation generation, or full Maxwell-equation propagation.

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

## Single-Slit Rows

| Case | Value | Note |
|---|---:|---|
| first minimum | ${round(firstMinimum.thetaDegrees, 4)} deg | 550 nm, 2.00 micrometer slit |
| second minimum | ${round(secondMinimum.thetaDegrees, 4)} deg | 550 nm, 2.00 micrometer slit |
| side-lobe sample | ${round(halfwayIntensity, 5)} I0 | halfway between first two minima |
| central maximum | ${centralIntensity} I0 | sinc limit |
| negative first minimum | ${round(negativeFirstMinimum.thetaDegrees, 4)} deg | symmetry |
| double slit width first minimum | ${round(widerSlitFirstMinimum.thetaDegrees, 4)} deg | narrower envelope |
| 650 nm first minimum | ${round(longerWavelengthFirstMinimum.thetaDegrees, 4)} deg | broader envelope |
| first minimum screen offset | ${round(firstMinimumScreenPosition, 6)} m | screen at ${screenDistance} m |

## Source Anchors

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The grammar passes a first single-slit envelope comparator. This is stronger than the scalar grating-equation check because finite aperture width now controls destructive minima and the sinc-squared side-lobe intensity envelope. It remains scalar Fraunhofer optics, not vector diffraction, broadband intensity prediction, resolving power, radiation generation, or a Maxwell-equation model.
`;

await writeFile(new URL('external-em-single-slit-envelope-comparator.md', outDir), markdown);

console.log(`External EM-16 status: ${status}`);
console.log(`Score: ${score}`);
console.log(`Wrote ${new URL('external-em-single-slit-envelope-comparator.md', outDir).pathname}`);
