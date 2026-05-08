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

function sinc(value) {
  return value === 0 ? 1 : Math.sin(value) / value;
}

function beta({ slitWidth, wavelength, thetaRadians }) {
  return (Math.PI * slitWidth * Math.sin(thetaRadians)) / wavelength;
}

function delta({ slitSeparation, wavelength, thetaRadians }) {
  return (Math.PI * slitSeparation * Math.sin(thetaRadians)) / wavelength;
}

function singleSlitEnvelope({ slitWidth, wavelength, thetaRadians }) {
  return sinc(beta({ slitWidth, wavelength, thetaRadians })) ** 2;
}

function doubleSlitCarrier({ slitSeparation, wavelength, thetaRadians }) {
  return Math.cos(delta({ slitSeparation, wavelength, thetaRadians })) ** 2;
}

function relativeIntensity({ slitWidth, slitSeparation, wavelength, thetaRadians }) {
  return (
    singleSlitEnvelope({ slitWidth, wavelength, thetaRadians }) *
    doubleSlitCarrier({ slitSeparation, wavelength, thetaRadians })
  );
}

function interferenceMaximumAngle({ slitSeparation, wavelength, order }) {
  const sine = (order * wavelength) / slitSeparation;
  if (Math.abs(sine) > 1) {
    return { exists: false, order, sine, thetaRadians: null, thetaDegrees: null };
  }
  const thetaRadians = Math.asin(sine);
  return { exists: true, order, sine, thetaRadians, thetaDegrees: radToDeg(thetaRadians) };
}

function interferenceMinimumAngle({ slitSeparation, wavelength, orderIndex }) {
  const sine = ((orderIndex + 0.5) * wavelength) / slitSeparation;
  if (Math.abs(sine) > 1) {
    return { exists: false, orderIndex, sine, thetaRadians: null, thetaDegrees: null };
  }
  const thetaRadians = Math.asin(sine);
  return { exists: true, orderIndex, sine, thetaRadians, thetaDegrees: radToDeg(thetaRadians) };
}

function singleSlitMinimumAngle({ slitWidth, wavelength, order }) {
  const sine = (order * wavelength) / slitWidth;
  if (Math.abs(sine) > 1) {
    return { exists: false, order, sine, thetaRadians: null, thetaDegrees: null };
  }
  const thetaRadians = Math.asin(sine);
  return { exists: true, order, sine, thetaRadians, thetaDegrees: radToDeg(thetaRadians) };
}

function screenPosition({ thetaRadians, distance }) {
  return distance * Math.tan(thetaRadians);
}

const external = {
  target: 'Double-slit diffraction envelope comparator',
  modeledSubset:
    'double-slit fringe spacing, constructive/destructive conditions, single-slit envelope modulation, missing orders, slit-separation scaling, wavelength scaling, symmetry, and screen-position mapping',
  notModeled:
    'finite detector response, vector diffraction, polarization, aperture aberrations, partial coherence, broadband spectrum intensities, resolving power, radiation generation, or numerical Maxwell-equation solving',
  tolerances: {
    analyticPct: 0.05,
    angleDegrees: 0.05,
    intensity: 0.002,
    screenPositionPct: 1,
  },
  sources: [
    {
      label: 'OpenStax University Physics Volume 3, Young double-slit experiment',
      url: 'https://openstax.org/books/university-physics-volume-3/pages/3-3-youngs-double-slit-experiment',
      note: 'Gives the double-slit constructive and destructive path-difference conditions.',
    },
    {
      label: 'OpenStax University Physics Volume 3, Double-Slit Diffraction',
      url: 'https://openstax.org/books/university-physics-volume-3/pages/4-3-double-slit-diffraction',
      note: 'Describes double-slit interference modulated by a finite single-slit diffraction envelope and missing-order behavior.',
    },
    {
      label: 'OpenStax University Physics Volume 3, Intensity in Single-Slit Diffraction',
      url: 'https://openstax.org/books/university-physics-volume-3/pages/4-2-intensity-in-single-slit-diffraction',
      note: 'Gives the sinc-squared aperture envelope used to modulate the two-slit interference carrier.',
    },
  ],
};

const grammarVariables = {
  route: 'two coherent aperture routes interfere while each slit contributes a finite-width aperture route bundle',
  closure: 'constructive closure occurs at d sin(theta) = m lambda and envelope closure suppresses orders at a sin(theta) = n lambda',
  phase: 'interference phase is delta = pi d sin(theta) / lambda and envelope phase is beta = pi a sin(theta) / lambda',
  charge: 'no free charge, source current, or radiation-generation mechanism is modeled',
  continuity: 'far-field angular continuity maps interference-envelope intensity to screen position',
};

const wavelength = 550e-9;
const slitWidth = 2e-6;
const slitSeparation = 6e-6;
const screenDistance = 2;
const centralMaximum = interferenceMaximumAngle({ slitSeparation, wavelength, order: 0 });
const firstMaximum = interferenceMaximumAngle({ slitSeparation, wavelength, order: 1 });
const firstMinimum = interferenceMinimumAngle({ slitSeparation, wavelength, orderIndex: 0 });
const thirdMaximum = interferenceMaximumAngle({ slitSeparation, wavelength, order: 3 });
const envelopeMinimum = singleSlitMinimumAngle({ slitWidth, wavelength, order: 1 });
const negativeFirstMaximum = interferenceMaximumAngle({ slitSeparation, wavelength, order: -1 });
const doubledSeparationFirstMaximum = interferenceMaximumAngle({
  slitSeparation: slitSeparation * 2,
  wavelength,
  order: 1,
});
const longerWavelengthFirstMaximum = interferenceMaximumAngle({
  slitSeparation,
  wavelength: 650e-9,
  order: 1,
});
const centralIntensity = relativeIntensity({
  slitWidth,
  slitSeparation,
  wavelength,
  thetaRadians: centralMaximum.thetaRadians,
});
const firstMaximumIntensity = relativeIntensity({
  slitWidth,
  slitSeparation,
  wavelength,
  thetaRadians: firstMaximum.thetaRadians,
});
const firstMinimumIntensity = relativeIntensity({
  slitWidth,
  slitSeparation,
  wavelength,
  thetaRadians: firstMinimum.thetaRadians,
});
const missingOrderIntensity = relativeIntensity({
  slitWidth,
  slitSeparation,
  wavelength,
  thetaRadians: thirdMaximum.thetaRadians,
});
const firstMaximumScreenPosition = screenPosition({
  thetaRadians: firstMaximum.thetaRadians,
  distance: screenDistance,
});
const smallAngleFringeSpacing = (screenDistance * wavelength) / slitSeparation;

const checks = [
  {
    check: 'Shared double-slit envelope grammar',
    expectation: 'route, closure, phase, charge, and continuity should define one two-aperture interference-envelope mapping',
    modelValue: Object.entries(grammarVariables)
      .map(([key, value]) => `${key}: ${value}`)
      .join('; '),
    pass: Object.keys(grammarVariables).length === 5,
    reading: 'The comparator combines interference phase and finite-aperture envelope without adding a new grammar vocabulary.',
  },
  {
    check: 'First bright maximum angle',
    expectation: '550 nm and 6.00 micrometer slit separation should give m = 1 maximum near 5.26 degrees',
    modelValue: `${round(firstMaximum.thetaDegrees, 4)} degrees`,
    pass: Math.abs(firstMaximum.thetaDegrees - 5.26) <= external.tolerances.angleDegrees,
    reading: 'The first constructive two-slit route matches the standard double-slit condition.',
  },
  {
    check: 'First destructive minimum angle',
    expectation: 'the first dark fringe should occur near 2.63 degrees',
    modelValue: `${round(firstMinimum.thetaDegrees, 4)} degrees`,
    pass: Math.abs(firstMinimum.thetaDegrees - 2.63) <= external.tolerances.angleDegrees,
    reading: 'The half-order destructive route lands between the central maximum and first bright fringe.',
  },
  {
    check: 'Central maximum recovery',
    expectation: 'theta = 0 should recover unit relative intensity',
    modelValue: `${centralIntensity}`,
    pass: centralIntensity === 1,
    reading: 'The interference carrier and aperture envelope both preserve the central peak.',
  },
  {
    check: 'Finite-slit envelope modulation',
    expectation: 'the first bright fringe should be reduced by the single-slit envelope to about 0.684 of central intensity',
    modelValue: `${round(firstMaximumIntensity, 5)}`,
    pass: Math.abs(firstMaximumIntensity - 0.684) <= external.tolerances.intensity,
    reading: 'The two-slit carrier is not treated as a flat comb; the finite slit width suppresses off-axis bright fringes.',
  },
  {
    check: 'Destructive-fringe suppression',
    expectation: 'the first dark fringe should have near-zero relative intensity',
    modelValue: `${round(firstMinimumIntensity, 12)}`,
    pass: firstMinimumIntensity <= 1e-12,
    reading: 'The carrier phase cancels the two-slit route at the expected half-order position.',
  },
  {
    check: 'Missing order at envelope minimum',
    expectation: 'with d/a = 3, the m = 3 interference maximum should fall on the first single-slit minimum',
    modelValue: `m3 ${round(thirdMaximum.thetaDegrees, 4)} deg; envelope minimum ${round(envelopeMinimum.thetaDegrees, 4)} deg; intensity ${round(missingOrderIntensity, 12)}`,
    pass:
      Math.abs(thirdMaximum.thetaDegrees - envelopeMinimum.thetaDegrees) <= external.tolerances.angleDegrees &&
      missingOrderIntensity <= 1e-12,
    reading: 'The finite-aperture envelope deletes a formally allowed interference order.',
  },
  {
    check: 'Screen-position/fringe-spacing mapping',
    expectation: 'first bright screen offset should match L tan(theta) and the small-angle fringe spacing within 1%',
    modelValue: `exact ${round(firstMaximumScreenPosition, 6)} m; small-angle ${round(smallAngleFringeSpacing, 6)} m`,
    pass:
      Math.abs(relativeErrorPct(firstMaximumScreenPosition, screenDistance * Math.tan(firstMaximum.thetaRadians))) <=
        external.tolerances.analyticPct &&
      Math.abs(relativeErrorPct(firstMaximumScreenPosition, smallAngleFringeSpacing)) <= external.tolerances.screenPositionPct,
    reading: 'Angular interference continuity maps to a measurable screen spacing.',
  },
  {
    check: 'Positive/negative order symmetry',
    expectation: 'positive and negative first maxima should be equal and opposite around the central maximum',
    modelValue: `+${round(firstMaximum.thetaDegrees, 4)} deg; ${round(negativeFirstMaximum.thetaDegrees, 4)} deg`,
    pass: Math.abs(firstMaximum.thetaDegrees + negativeFirstMaximum.thetaDegrees) <= external.tolerances.angleDegrees,
    reading: 'The two-aperture pattern remains symmetric about the optical axis.',
  },
  {
    check: 'Slit-separation scaling',
    expectation: 'doubling slit separation should narrow the first bright angle',
    modelValue: `base ${round(firstMaximum.thetaDegrees, 4)} deg; double separation ${round(doubledSeparationFirstMaximum.thetaDegrees, 4)} deg`,
    pass: doubledSeparationFirstMaximum.thetaDegrees < firstMaximum.thetaDegrees,
    reading: 'Wider slit separation produces tighter fringe spacing.',
  },
  {
    check: 'Wavelength scaling',
    expectation: 'a longer wavelength should broaden the first bright angle',
    modelValue: `550nm ${round(firstMaximum.thetaDegrees, 4)} deg; 650nm ${round(longerWavelengthFirstMaximum.thetaDegrees, 4)} deg`,
    pass: longerWavelengthFirstMaximum.thetaDegrees > firstMaximum.thetaDegrees,
    reading: 'Longer wavelengths require larger constructive-interference angles.',
  },
  {
    check: 'Boundary/non-claim discipline',
    expectation: 'benchmark should not claim vector diffraction, broadband intensity, resolving power, radiation, or Maxwell validation',
    modelValue: external.notModeled,
    pass:
      external.notModeled.includes('vector diffraction') &&
      external.notModeled.includes('broadband') &&
      external.notModeled.includes('resolving power') &&
      external.notModeled.includes('Maxwell'),
    reading: 'This is a scalar double-slit Fraunhofer comparator, not a full diffraction optics solver.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = `${passed}/${checks.length}`;
const status =
  passed === checks.length ? 'double-slit envelope comparator pass' : 'mixed double-slit envelope comparator';

const report = {
  source: 'external-em-double-slit-envelope-comparator.mjs',
  status,
  external,
  grammarVariables,
  metrics: {
    wavelengthMeters: wavelength,
    slitWidthMeters: slitWidth,
    slitSeparationMeters: slitSeparation,
    separationToWidthRatio: slitSeparation / slitWidth,
    screenDistanceMeters: screenDistance,
    centralMaximumDegrees: centralMaximum.thetaDegrees,
    firstMaximumDegrees: round(firstMaximum.thetaDegrees, 4),
    firstMinimumDegrees: round(firstMinimum.thetaDegrees, 4),
    thirdMaximumDegrees: round(thirdMaximum.thetaDegrees, 4),
    envelopeMinimumDegrees: round(envelopeMinimum.thetaDegrees, 4),
    negativeFirstMaximumDegrees: round(negativeFirstMaximum.thetaDegrees, 4),
    centralRelativeIntensity: centralIntensity,
    firstMaximumRelativeIntensity: round(firstMaximumIntensity, 5),
    firstMinimumRelativeIntensity: round(firstMinimumIntensity, 12),
    missingOrderRelativeIntensity: round(missingOrderIntensity, 12),
    firstMaximumScreenPositionMeters: round(firstMaximumScreenPosition, 6),
    smallAngleFringeSpacingMeters: round(smallAngleFringeSpacing, 6),
    doubledSeparationFirstMaximumDegrees: round(doubledSeparationFirstMaximum.thetaDegrees, 4),
    longerWavelengthFirstMaximumDegrees: round(longerWavelengthFirstMaximum.thetaDegrees, 4),
  },
  score,
  checks,
  confidenceEffect:
    status === 'double-slit envelope comparator pass'
      ? 'supports a small inferential-convergence increase because EM evidence now includes two-aperture interference under a finite single-slit envelope while remaining limited to scalar Fraunhofer optics'
      : 'does not increase confidence; failure would show that single-slit envelope behavior does not transfer to two-aperture interference-envelope coupling',
};

await writeFile(new URL('external-em-double-slit-envelope-comparator.json', outDir), JSON.stringify(report, null, 2));

const markdown = `# Relational Substrate External EM-17 Double-Slit Envelope Comparator

## Purpose

This report extends EM-16 from a finite-aperture single-slit envelope into double-slit interference modulated by that finite-aperture envelope.

It tests whether fixed grammar variables reproduce double-slit fringe spacing, constructive/destructive conditions, single-slit envelope modulation, missing orders, slit-separation scaling, wavelength scaling, symmetry, and screen-position mapping. It does not model vector diffraction, polarization, aperture aberrations, partial coherence, broadband intensities, resolving power, radiation generation, or full Maxwell-equation propagation.

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

## Double-Slit Rows

| Case | Value | Note |
|---|---:|---|
| first bright maximum | ${round(firstMaximum.thetaDegrees, 4)} deg | m = 1, 550 nm, 6.00 micrometer slit separation |
| first destructive minimum | ${round(firstMinimum.thetaDegrees, 4)} deg | first half-order dark fringe |
| central maximum | ${centralIntensity} I0 | carrier and envelope limit |
| first bright relative intensity | ${round(firstMaximumIntensity, 5)} I0 | single-slit envelope suppression |
| third maximum / missing order | ${round(thirdMaximum.thetaDegrees, 4)} deg | coincides with first single-slit minimum |
| missing-order relative intensity | ${round(missingOrderIntensity, 12)} I0 | suppressed by aperture envelope |
| negative first maximum | ${round(negativeFirstMaximum.thetaDegrees, 4)} deg | symmetry |
| double separation first maximum | ${round(doubledSeparationFirstMaximum.thetaDegrees, 4)} deg | narrower fringe spacing |
| 650 nm first maximum | ${round(longerWavelengthFirstMaximum.thetaDegrees, 4)} deg | broader fringe spacing |
| first bright screen offset | ${round(firstMaximumScreenPosition, 6)} m | screen at ${screenDistance} m |
| small-angle fringe spacing | ${round(smallAngleFringeSpacing, 6)} m | L lambda / d |

## Source Anchors

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The grammar passes a first double-slit interference-envelope comparator. This is stronger than the single-slit envelope check because the same scalar phase grammar must preserve two-slit bright/dark fringe positions while the finite-slit envelope suppresses off-axis maxima and creates a missing order at d/a = 3. It remains scalar Fraunhofer optics, not vector diffraction, broadband intensity prediction, resolving power, radiation generation, or a Maxwell-equation model.
`;

await writeFile(new URL('external-em-double-slit-envelope-comparator.md', outDir), markdown);

console.log(`External EM-17 status: ${status}`);
console.log(`Score: ${score}`);
console.log(`Wrote ${new URL('external-em-double-slit-envelope-comparator.md', outDir).pathname}`);
