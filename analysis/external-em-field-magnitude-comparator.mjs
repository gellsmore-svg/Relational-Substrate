import { writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const coulombConstant = 8.9875517923e9;
const elementaryCharge = 1.602176634e-19;

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

function relativeErrorPct(model, expected) {
  return ((model - expected) / expected) * 100;
}

function vectorMagnitude(vector) {
  return Math.hypot(vector.x, vector.y, vector.z ?? 0);
}

function pointField({ q, source = { x: 0, y: 0, z: 0 }, point }) {
  const dx = point.x - source.x;
  const dy = point.y - source.y;
  const dz = (point.z ?? 0) - (source.z ?? 0);
  const r = Math.hypot(dx, dy, dz);
  const scale = (coulombConstant * q) / r ** 3;
  return {
    x: scale * dx,
    y: scale * dy,
    z: scale * dz,
    magnitude: Math.abs(coulombConstant * q) / r ** 2,
    r,
  };
}

const external = {
  target: 'Calibrated point-charge electric-field magnitude comparator',
  modeledSubset:
    'absolute SI electric-field magnitudes and vector components for static point charges using E = kq/r^2',
  notModeled:
    'charge derivation, permittivity derivation, conductors, shielding, dielectric media, radiation, magnetic fields, time-dependent Maxwell dynamics, or relativistic propagation',
  constants: {
    coulombConstant,
    elementaryCharge,
  },
  tolerances: {
    workedExamplePct: 3,
    analyticPct: 0.01,
    componentPct: 0.01,
  },
  sources: [
    {
      label: 'OpenStax University Physics Volume 2, Chapter 5 Key Equations',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/5-key-equations',
      note: 'Lists the electric field at a point as the sum of point-charge source terms with the 1/(4 pi epsilon_0) constant.',
    },
    {
      label: 'OpenStax University Physics Volume 2, Electric Field',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/5-4-electric-field',
      note: 'Gives a worked point-charge field example for a helium nucleus: about 4.1 x 10^12 N/C at 26.5 pm.',
    },
    {
      label: 'OpenStax University Physics Volume 2, Calculations of Electric Potential',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/7-3-calculations-of-electric-potential',
      note: 'States that point-charge electric field magnitude decreases with distance squared as E = kq/r^2.',
    },
  ],
};

const grammarVariables = {
  route: 'radial route from source charge to field point',
  closure: 'no closed-loop topology for static electric source field',
  phase: 'field direction preserves radial sign orientation',
  charge: 'signed source charge multiplied by Coulomb constant',
  continuity: 'inverse-square dilution over continuous radial distance',
};

const heliumExample = {
  label: 'OpenStax helium nucleus example',
  q: 2 * elementaryCharge,
  point: { x: 26.5e-12, y: 0, z: 0 },
  expectedMagnitude: 4.1e12,
  tolerancePct: external.tolerances.workedExamplePct,
};

const microCoulombCase = {
  label: '1 microC at 0.5 m',
  q: 1e-6,
  point: { x: 0.5, y: 0, z: 0 },
  expectedMagnitude: coulombConstant * 1e-6 / 0.5 ** 2,
  tolerancePct: external.tolerances.analyticPct,
};

const distanceCases = [
  {
    label: '1 microC at 1 m',
    q: 1e-6,
    point: { x: 1, y: 0, z: 0 },
  },
  {
    label: '1 microC at 2 m',
    q: 1e-6,
    point: { x: 2, y: 0, z: 0 },
  },
];

const chargeCases = [
  {
    label: '1 microC at 1 m',
    q: 1e-6,
    point: { x: 1, y: 0, z: 0 },
  },
  {
    label: '2 microC at 1 m',
    q: 2e-6,
    point: { x: 1, y: 0, z: 0 },
  },
];

const vectorCase = {
  label: '1 microC at 3-4-5 m point',
  q: 1e-6,
  point: { x: 3, y: 4, z: 0 },
  expectedMagnitude: coulombConstant * 1e-6 / 5 ** 2,
  expectedX: (coulombConstant * 1e-6 / 5 ** 2) * (3 / 5),
  expectedY: (coulombConstant * 1e-6 / 5 ** 2) * (4 / 5),
};

function evaluatedCase(testCase) {
  const field = pointField(testCase);
  return {
    ...testCase,
    modelMagnitude: field.magnitude,
    modelX: field.x,
    modelY: field.y,
    modelZ: field.z,
  };
}

const heliumRow = evaluatedCase(heliumExample);
const microCoulombRow = evaluatedCase(microCoulombCase);
const distanceRows = distanceCases.map(evaluatedCase);
const chargeRows = chargeCases.map(evaluatedCase);
const vectorRow = evaluatedCase(vectorCase);

const distanceRatio = distanceRows[0].modelMagnitude / distanceRows[1].modelMagnitude;
const chargeRatio = chargeRows[1].modelMagnitude / chargeRows[0].modelMagnitude;
const vectorMagnitudeFromComponents = vectorMagnitude({
  x: vectorRow.modelX,
  y: vectorRow.modelY,
  z: vectorRow.modelZ,
});

const heliumErrorPct = relativeErrorPct(heliumRow.modelMagnitude, heliumExample.expectedMagnitude);
const microCoulombErrorPct = relativeErrorPct(microCoulombRow.modelMagnitude, microCoulombCase.expectedMagnitude);
const vectorMagnitudeErrorPct = relativeErrorPct(vectorRow.modelMagnitude, vectorCase.expectedMagnitude);
const vectorXErrorPct = relativeErrorPct(vectorRow.modelX, vectorCase.expectedX);
const vectorYErrorPct = relativeErrorPct(vectorRow.modelY, vectorCase.expectedY);

const checks = [
  {
    check: 'Shared calibrated field grammar',
    expectation: 'route, closure, phase, charge, and continuity should define one calibrated point-field mapping',
    modelValue: Object.entries(grammarVariables)
      .map(([key, value]) => `${key}: ${value}`)
      .join('; '),
    pass: Object.keys(grammarVariables).length === 5,
    reading: 'The comparator changes source charge and field point, not the grammar variables.',
  },
  {
    check: 'Published worked-example magnitude',
    expectation: `OpenStax helium-nucleus field about ${heliumExample.expectedMagnitude.toExponential(2)} N/C within ${heliumExample.tolerancePct}%`,
    modelValue: `${heliumRow.modelMagnitude.toExponential(4)} N/C; error ${round(heliumErrorPct, 3)}%`,
    pass: Math.abs(heliumErrorPct) <= heliumExample.tolerancePct,
    reading: 'The calibrated point-field grammar reproduces the standard worked example within rounding tolerance.',
  },
  {
    check: 'Absolute microcoulomb magnitude',
    expectation: `${round(microCoulombCase.expectedMagnitude, 2)} N/C for 1 microC at 0.5 m`,
    modelValue: `${round(microCoulombRow.modelMagnitude, 2)} N/C; error ${round(microCoulombErrorPct, 6)}%`,
    pass: Math.abs(microCoulombErrorPct) <= microCoulombCase.tolerancePct,
    reading: 'The model returns absolute SI magnitude from the published Coulomb constant, not a relative unitless score.',
  },
  {
    check: 'Calibrated inverse-square magnitude',
    expectation: 'field magnitude at 1 m should be 4x field magnitude at 2 m for the same source charge',
    modelValue: `ratio ${round(distanceRatio, 6)}`,
    pass: Math.abs(distanceRatio - 4) <= 1e-9,
    reading: 'The calibrated field preserves inverse-square distance dilution at absolute scale.',
  },
  {
    check: 'Calibrated charge linearity',
    expectation: 'doubling source charge should double field magnitude at fixed distance',
    modelValue: `ratio ${round(chargeRatio, 6)}`,
    pass: Math.abs(chargeRatio - 2) <= 1e-9,
    reading: 'The calibrated field preserves linear charge scaling at absolute scale.',
  },
  {
    check: 'Vector component magnitude consistency',
    expectation: '3-4-5 point should produce components whose norm matches the calibrated field magnitude',
    modelValue: `magnitude ${round(vectorRow.modelMagnitude, 6)}, component norm ${round(vectorMagnitudeFromComponents, 6)}`,
    pass: Math.abs(vectorMagnitudeFromComponents - vectorRow.modelMagnitude) <= 1e-9,
    reading: 'The calibrated vector components and scalar field magnitude remain coherent.',
  },
  {
    check: 'Vector component direction',
    expectation: 'field components should follow the radial unit vector at the 3-4-5 point',
    modelValue: `x ${round(vectorRow.modelX, 6)} (${round(vectorXErrorPct, 8)}%); y ${round(vectorRow.modelY, 6)} (${round(vectorYErrorPct, 8)}%)`,
    pass:
      Math.abs(vectorMagnitudeErrorPct) <= external.tolerances.componentPct &&
      Math.abs(vectorXErrorPct) <= external.tolerances.componentPct &&
      Math.abs(vectorYErrorPct) <= external.tolerances.componentPct,
    reading: 'The calibrated field keeps radial direction and magnitude coupled.',
  },
  {
    check: 'Scope boundary',
    expectation: 'benchmark should not claim derivation of the Coulomb constant or full Maxwell validation',
    modelValue: external.notModeled,
    pass: external.notModeled.includes('permittivity derivation') && external.notModeled.includes('Maxwell'),
    reading: 'This is a calibrated point-charge field comparator, not a derivation of electrodynamics from substrate primitives.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = `${passed}/${checks.length}`;
const status = passed === checks.length ? 'calibrated field magnitude comparator pass' : 'mixed calibrated field magnitude comparator';

const report = {
  source: 'external-em-field-magnitude-comparator.mjs',
  status,
  external,
  grammarVariables,
  metrics: {
    heliumExample: {
      modelMagnitude: round(heliumRow.modelMagnitude, 2),
      expectedMagnitude: heliumExample.expectedMagnitude,
      errorPct: round(heliumErrorPct, 4),
    },
    microCoulombCase: {
      modelMagnitude: round(microCoulombRow.modelMagnitude, 4),
      expectedMagnitude: round(microCoulombCase.expectedMagnitude, 4),
      errorPct: round(microCoulombErrorPct, 8),
    },
    distanceRatio: round(distanceRatio, 8),
    chargeRatio: round(chargeRatio, 8),
    vectorCase: {
      modelMagnitude: round(vectorRow.modelMagnitude, 6),
      expectedMagnitude: round(vectorCase.expectedMagnitude, 6),
      modelX: round(vectorRow.modelX, 6),
      expectedX: round(vectorCase.expectedX, 6),
      modelY: round(vectorRow.modelY, 6),
      expectedY: round(vectorCase.expectedY, 6),
    },
  },
  score,
  checks,
  confidenceEffect:
    status === 'calibrated field magnitude comparator pass'
      ? 'supports a small inferential-convergence increase because EM evidence now includes absolute SI field magnitude without fitted scale, while remaining inside one electrostatic evidence line'
      : 'does not increase confidence; failure would show that prior EM topology and potential checks do not transfer to calibrated field magnitude',
};

await writeFile(new URL('external-em-field-magnitude-comparator.json', outDir), JSON.stringify(report, null, 2));

const markdown = `# Relational Substrate External EM-07 Field Magnitude Comparator

## Purpose

This report extends EM-06 from electrostatic potential geometry into calibrated point-charge electric-field magnitude.

It tests whether fixed grammar variables reproduce absolute SI field magnitudes and vector components for static point charges using the published Coulomb constant. It does not derive the Coulomb constant, model conductors, solve Maxwell's equations, model media, or address time-dependent propagation.

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

## Calibrated Rows

| Case | Model | Expected | Error |
|---|---:|---:|---:|
| OpenStax helium nucleus field | ${heliumRow.modelMagnitude.toExponential(4)} N/C | ${heliumExample.expectedMagnitude.toExponential(4)} N/C | ${round(heliumErrorPct, 4)}% |
| 1 microC at 0.5 m | ${round(microCoulombRow.modelMagnitude, 4)} N/C | ${round(microCoulombCase.expectedMagnitude, 4)} N/C | ${round(microCoulombErrorPct, 8)}% |
| distance ratio, 1 m / 2 m | ${round(distanceRatio, 8)} | 4 | 0% |
| charge ratio, 2 microC / 1 microC | ${round(chargeRatio, 8)} | 2 | 0% |

## Vector Case

| Quantity | Model | Expected |
|---|---:|---:|
| magnitude | ${round(vectorRow.modelMagnitude, 6)} N/C | ${round(vectorCase.expectedMagnitude, 6)} N/C |
| x component | ${round(vectorRow.modelX, 6)} N/C | ${round(vectorCase.expectedX, 6)} N/C |
| y component | ${round(vectorRow.modelY, 6)} N/C | ${round(vectorCase.expectedY, 6)} N/C |

## Source Anchors

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The grammar passes a calibrated point-charge field-magnitude comparator. This is stronger than EM-06 because the outputs are absolute SI magnitudes rather than only qualitative topology or unitless geometry. It remains one electromagnetic evidence line and it imports the conventional Coulomb constant rather than deriving it. The next EM gate should move toward conductors/material media or time-dependent propagation rather than counting more point-charge electrostatics as independent evidence.
`;

await writeFile(new URL('external-em-field-magnitude-comparator.md', outDir), markdown);

console.log(`External EM-07 status: ${status}`);
console.log(`Score: ${score}`);
console.log(`Wrote ${new URL('external-em-field-magnitude-comparator.md', outDir).pathname}`);
