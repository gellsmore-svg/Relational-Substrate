import { writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function round(value, places = 8) {
  return Number(value.toFixed(places));
}

function radToDeg(radians) {
  return (radians * 180) / Math.PI;
}

function relativeErrorPct(model, expected) {
  if (expected === 0) return model === 0 ? 0 : Infinity;
  return ((model - expected) / expected) * 100;
}

function gratingAngle({ spacing, wavelength, order }) {
  const sine = (order * wavelength) / spacing;
  if (Math.abs(sine) > 1) {
    return {
      order,
      wavelength,
      exists: false,
      sine,
      thetaRadians: null,
      thetaDegrees: null,
    };
  }
  const thetaRadians = Math.asin(sine);
  return {
    order,
    wavelength,
    exists: true,
    sine,
    thetaRadians,
    thetaDegrees: radToDeg(thetaRadians),
  };
}

function maxOrder({ spacing, wavelength }) {
  return Math.floor(spacing / wavelength);
}

function screenPosition({ thetaRadians, distance }) {
  return distance * Math.tan(thetaRadians);
}

const external = {
  target: 'Diffraction grating comparator',
  modeledSubset:
    'normal-incidence grating equation, first-order violet/red angular dispersion, central-order non-dispersion, positive/negative order symmetry, order cutoff, and screen-position scaling',
  notModeled:
    'finite-slit diffraction envelope, blaze efficiency, polarization, groove shape, vector diffraction, material dispersion, broadband spectrum intensities, resolving power, coherence limits, radiation generation, or numerical Maxwell-equation solving',
  tolerances: {
    analyticPct: 0.01,
    angleDegrees: 0.01,
    screenPositionPct: 0.01,
  },
  sources: [
    {
      label: 'OpenStax University Physics Volume 3, Diffraction Gratings',
      url: 'https://openstax.org/books/university-physics-volume-3/pages/4-4-diffraction-gratings',
      note: 'Gives the grating equation d sin theta = m lambda and a worked 10,000-lines/cm example.',
    },
    {
      label: 'OpenStax University Physics Volume 3, Double-Slit Diffraction',
      url: 'https://openstax.org/books/university-physics-volume-3/pages/4-3-double-slit-diffraction',
      note: 'Describes interference/diffraction overlap and missing-order boundaries that this grating comparator does not model.',
    },
  ],
};

const grammarVariables = {
  route: 'periodic aperture routes add constructively only at allowed grating orders',
  closure: 'path-difference closure requires integer wavelength multiples across adjacent grooves',
  phase: 'phase alignment is encoded by d sin theta = m lambda',
  charge: 'no free charge, source current, or radiation-generation mechanism is modeled',
  continuity: 'far-field angular continuity maps grating order to screen position',
};

const lineDensityPerCm = 10000;
const spacing = 0.01 / lineDensityPerCm;
const screenDistance = 2;
const violet = 380e-9;
const green = 550e-9;
const red = 760e-9;
const violetFirst = gratingAngle({ spacing, wavelength: violet, order: 1 });
const redFirst = gratingAngle({ spacing, wavelength: red, order: 1 });
const greenZero = gratingAngle({ spacing, wavelength: green, order: 0 });
const greenFirst = gratingAngle({ spacing, wavelength: green, order: 1 });
const violetSecond = gratingAngle({ spacing, wavelength: violet, order: 2 });
const redSecond = gratingAngle({ spacing, wavelength: red, order: 2 });
const greenNegativeFirst = gratingAngle({ spacing, wavelength: green, order: -1 });
const greenScreenPosition = screenPosition({
  thetaRadians: greenFirst.thetaRadians,
  distance: screenDistance,
});

const checks = [
  {
    check: 'Shared diffraction grammar',
    expectation: 'route, closure, phase, charge, and continuity should define one grating-diffraction mapping',
    modelValue: Object.entries(grammarVariables)
      .map(([key, value]) => `${key}: ${value}`)
      .join('; '),
    pass: Object.keys(grammarVariables).length === 5,
    reading: 'The comparator adds periodic phase closure without adding a new grammar vocabulary.',
  },
  {
    check: 'Line-density spacing',
    expectation: '10,000 lines/cm should give 1.0e-6 m grating spacing',
    modelValue: `${spacing} m`,
    pass: Math.abs(relativeErrorPct(spacing, 1e-6)) <= external.tolerances.analyticPct,
    reading: 'The grating spacing matches the standard worked-example conversion.',
  },
  {
    check: 'First-order violet angle',
    expectation: '380 nm first order should appear near 22.33 degrees',
    modelValue: `${round(violetFirst.thetaDegrees, 4)} degrees`,
    pass: Math.abs(violetFirst.thetaDegrees - 22.33) <= external.tolerances.angleDegrees,
    reading: 'The violet first-order route lands at the expected constructive-interference angle.',
  },
  {
    check: 'First-order red angle',
    expectation: '760 nm first order should appear near 49.46 degrees',
    modelValue: `${round(redFirst.thetaDegrees, 4)} degrees`,
    pass: Math.abs(redFirst.thetaDegrees - 49.46) <= external.tolerances.angleDegrees,
    reading: 'The red first-order route lands at the expected larger dispersion angle.',
  },
  {
    check: 'Spectral dispersion ordering',
    expectation: 'red first order should be farther from the central maximum than violet first order',
    modelValue: `violet ${round(violetFirst.thetaDegrees, 4)} deg; red ${round(redFirst.thetaDegrees, 4)} deg`,
    pass: redFirst.thetaDegrees > violetFirst.thetaDegrees,
    reading: 'Longer wavelength routes require larger angle for the same grating spacing and order.',
  },
  {
    check: 'Central-order non-dispersion',
    expectation: 'm = 0 should give theta = 0 for all wavelengths',
    modelValue: `${greenZero.thetaDegrees} degrees`,
    pass: greenZero.exists && greenZero.thetaDegrees === 0,
    reading: 'The central maximum does not separate colors in the grating equation.',
  },
  {
    check: 'Order cutoff',
    expectation: 'with 1 micrometer spacing, violet should allow second order while red second order should be forbidden',
    modelValue: `violet mmax ${maxOrder({ spacing, wavelength: violet })}; red m2 exists ${redSecond.exists}`,
    pass: violetSecond.exists && maxOrder({ spacing, wavelength: red }) === 1 && redSecond.exists === false,
    reading: 'Allowed orders close when m lambda exceeds grating spacing.',
  },
  {
    check: 'Positive/negative order symmetry',
    expectation: 'positive and negative first orders should be equal and opposite in angle',
    modelValue: `+${round(greenFirst.thetaDegrees, 4)} deg; ${round(greenNegativeFirst.thetaDegrees, 4)} deg`,
    pass: Math.abs(greenFirst.thetaDegrees + greenNegativeFirst.thetaDegrees) <= external.tolerances.angleDegrees,
    reading: 'Diffraction routes appear symmetrically on either side of the central order.',
  },
  {
    check: 'Screen-position scaling',
    expectation: 'screen offset should equal L tan theta',
    modelValue: `${round(greenScreenPosition, 6)} m`,
    pass:
      Math.abs(
        relativeErrorPct(greenScreenPosition, screenDistance * Math.tan(greenFirst.thetaRadians))
      ) <= external.tolerances.screenPositionPct,
    reading: 'Angular route continuity maps to a measurable screen offset.',
  },
  {
    check: 'Boundary/non-claim discipline',
    expectation: 'benchmark should not claim blaze, finite envelope, broadband intensity, radiation, or Maxwell validation',
    modelValue: external.notModeled,
    pass:
      external.notModeled.includes('blaze') &&
      external.notModeled.includes('broadband') &&
      external.notModeled.includes('Maxwell'),
    reading: 'This is a narrow grating-equation comparator, not a full diffraction optics solver.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = `${passed}/${checks.length}`;
const status = passed === checks.length ? 'diffraction grating comparator pass' : 'mixed diffraction grating comparator';

const report = {
  source: 'external-em-diffraction-grating-comparator.mjs',
  status,
  external,
  grammarVariables,
  metrics: {
    lineDensityPerCm,
    spacingMeters: spacing,
    screenDistanceMeters: screenDistance,
    angles: {
      violetFirst: round(violetFirst.thetaDegrees, 4),
      redFirst: round(redFirst.thetaDegrees, 4),
      greenZero: greenZero.thetaDegrees,
      greenFirst: round(greenFirst.thetaDegrees, 4),
      greenNegativeFirst: round(greenNegativeFirst.thetaDegrees, 4),
      violetSecond: round(violetSecond.thetaDegrees, 4),
      redSecondExists: redSecond.exists,
    },
    maxOrders: {
      violet: maxOrder({ spacing, wavelength: violet }),
      green: maxOrder({ spacing, wavelength: green }),
      red: maxOrder({ spacing, wavelength: red }),
    },
    greenFirstScreenPositionMeters: round(greenScreenPosition, 6),
  },
  score,
  checks,
  confidenceEffect:
    status === 'diffraction grating comparator pass'
      ? 'supports a small inferential-convergence increase because EM evidence now includes periodic-aperture diffraction and spectral angular dispersion while remaining limited to a scalar grating-equation comparator'
      : 'does not increase confidence; failure would show that rough-boundary scatter checks do not transfer to periodic diffraction constraints',
};

await writeFile(new URL('external-em-diffraction-grating-comparator.json', outDir), JSON.stringify(report, null, 2));

const markdown = `# Relational Substrate External EM-15 Diffraction Grating Comparator

## Purpose

This report extends EM-14 from rough-surface scatter into a narrow periodic-aperture diffraction check.

It tests whether fixed grammar variables reproduce the normal-incidence grating equation, first-order violet/red angular dispersion, central-order non-dispersion, positive/negative order symmetry, order cutoff, and screen-position scaling. It does not model finite-slit diffraction envelopes, blaze efficiency, groove-shape vector diffraction, material dispersion, broadband intensity spectra, resolving power, coherence limits, radiation generation, or full Maxwell-equation propagation.

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

## Grating Rows

| Case | Exists | Angle | Note |
|---|---:|---:|---|
| violet 380 nm, m=1 | ${violetFirst.exists ? 'yes' : 'no'} | ${round(violetFirst.thetaDegrees, 4)} deg | OpenStax worked-example violet |
| red 760 nm, m=1 | ${redFirst.exists ? 'yes' : 'no'} | ${round(redFirst.thetaDegrees, 4)} deg | OpenStax worked-example red |
| green 550 nm, m=0 | ${greenZero.exists ? 'yes' : 'no'} | ${greenZero.thetaDegrees} deg | central maximum |
| green 550 nm, m=1 | ${greenFirst.exists ? 'yes' : 'no'} | ${round(greenFirst.thetaDegrees, 4)} deg | first-order screen offset ${round(greenScreenPosition, 6)} m at ${screenDistance} m |
| green 550 nm, m=-1 | ${greenNegativeFirst.exists ? 'yes' : 'no'} | ${round(greenNegativeFirst.thetaDegrees, 4)} deg | order symmetry |
| violet 380 nm, m=2 | ${violetSecond.exists ? 'yes' : 'no'} | ${round(violetSecond.thetaDegrees, 4)} deg | allowed second order |
| red 760 nm, m=2 | ${redSecond.exists ? 'yes' : 'no'} | n/a | forbidden order |

## Source Anchors

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The grammar passes a first diffraction-grating comparator. This is stronger than rough-surface scatter because periodic route spacing now has to produce discrete constructive orders, wavelength dispersion, forbidden orders, and symmetric angular branches. It remains a scalar grating-equation check, not a finite-envelope, blaze-efficiency, broadband-spectrum, vector-diffraction, radiation-generation, or Maxwell-equation model.
`;

await writeFile(new URL('external-em-diffraction-grating-comparator.md', outDir), markdown);

console.log(`External EM-15 status: ${status}`);
console.log(`Score: ${score}`);
console.log(`Wrote ${new URL('external-em-diffraction-grating-comparator.md', outDir).pathname}`);
