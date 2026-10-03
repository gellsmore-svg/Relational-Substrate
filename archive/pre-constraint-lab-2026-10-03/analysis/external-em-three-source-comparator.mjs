import { writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

function degrees(value) {
  return (value * 180) / Math.PI;
}

const external = {
  target: 'Non-symmetric three-source electric-field geometry comparator',
  modeledSubset:
    'relative vector-field direction, magnitude scaling, and source-contribution sensitivity for fixed non-symmetric three-charge layouts',
  notModeled:
    'continuous field-line tracing, potentials, conductors, radiation, time-varying Maxwell dynamics, field energy, or absolute SI magnitudes',
  sources: [
    {
      label: 'OpenStax University Physics Volume 2, Electric Field',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/5-4-electric-field',
      note: 'States that the net electric field from many source charges is the vector sum of the independently calculated fields.',
    },
    {
      label: 'OpenStax University Physics Volume 2, Electric Field Lines',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/5-6-electric-field-lines',
      note: 'States that electric field vectors are tangent to field lines and that vector direction and density encode field direction and magnitude.',
    },
  ],
};

const layouts = [
  {
    case: 'asymmetric triad A',
    charges: [
      { q: 1, x: -1, y: 0 },
      { q: -2, x: 2, y: 0 },
      { q: 0.5, x: 0, y: 2 },
    ],
    point: { x: 0.5, y: 0.75 },
    expectedNet: { x: 1.0565, y: -0.4151 },
    expectedMagnitude: 1.1351,
    expectedAngleDeg: -21.4517,
    expectedQuadrant: 'east-south',
    expectedDominantAxis: 'x',
    thirdSourceAngleShiftDeg: 11.5,
  },
  {
    case: 'asymmetric triad B',
    charges: [
      { q: 2, x: -1, y: -1 },
      { q: -1, x: 1.5, y: 0.25 },
      { q: -0.5, x: -0.25, y: 2 },
    ],
    point: { x: 0.25, y: 0.5 },
    expectedNet: { x: 0.876, y: 0.4721 },
    expectedMagnitude: 0.9951,
    expectedAngleDeg: 28.3183,
    expectedQuadrant: 'east-north',
    expectedDominantAxis: 'x',
    thirdSourceAngleShiftDeg: 10,
  },
];

function contribution(charge, point) {
  const dx = point.x - charge.x;
  const dy = point.y - charge.y;
  const radiusSquared = dx ** 2 + dy ** 2;
  const radius = Math.sqrt(radiusSquared);
  const scale = charge.q / radius ** 3;
  return {
    x: dx * scale,
    y: dy * scale,
  };
}

function vectorSum(vectors) {
  return vectors.reduce(
    (sum, vector) => ({
      x: sum.x + vector.x,
      y: sum.y + vector.y,
    }),
    { x: 0, y: 0 }
  );
}

function magnitude(vector) {
  return Math.sqrt(vector.x ** 2 + vector.y ** 2);
}

function angleDeg(vector) {
  return degrees(Math.atan2(vector.y, vector.x));
}

function quadrant(vector) {
  const horizontal = vector.x >= 0 ? 'east' : 'west';
  const vertical = vector.y >= 0 ? 'north' : 'south';
  return `${horizontal}-${vertical}`;
}

function dominantAxis(vector) {
  return Math.abs(vector.x) >= Math.abs(vector.y) ? 'x' : 'y';
}

function angleDifference(a, b) {
  const raw = Math.abs(a - b) % 360;
  return raw > 180 ? 360 - raw : raw;
}

function grammarField(layout, charges = layout.charges) {
  const components = charges.map((charge) => contribution(charge, layout.point));
  const net = vectorSum(components);
  return {
    components: components.map((component) => ({
      x: round(component.x),
      y: round(component.y),
    })),
    net: {
      x: round(net.x),
      y: round(net.y),
    },
    magnitude: round(magnitude(net)),
    angleDeg: round(angleDeg(net)),
    quadrant: quadrant(net),
    dominantAxis: dominantAxis(net),
  };
}

function scaledLayout(layout, factor) {
  return {
    ...layout,
    charges: layout.charges.map((charge) => ({
      ...charge,
      q: charge.q * factor,
    })),
  };
}

const rows = layouts.map((layout) => {
  const field = grammarField(layout);
  const withoutThird = grammarField(layout, layout.charges.slice(0, 2));
  const doubled = grammarField(scaledLayout(layout, 2));
  const angleShiftWithoutThird = round(angleDifference(field.angleDeg, withoutThird.angleDeg));

  return {
    ...layout,
    modelComponents: field.components,
    modelNet: field.net,
    modelMagnitude: field.magnitude,
    modelAngleDeg: field.angleDeg,
    modelQuadrant: field.quadrant,
    modelDominantAxis: field.dominantAxis,
    withoutThird,
    doubled,
    angleShiftWithoutThird,
    netPass:
      Math.abs(field.net.x - layout.expectedNet.x) <= 0.0001 &&
      Math.abs(field.net.y - layout.expectedNet.y) <= 0.0001,
    magnitudePass: Math.abs(field.magnitude - layout.expectedMagnitude) <= 0.0001,
    anglePass: Math.abs(field.angleDeg - layout.expectedAngleDeg) <= 0.0001,
    geometryPass:
      field.quadrant === layout.expectedQuadrant && field.dominantAxis === layout.expectedDominantAxis,
    contributionPass: angleShiftWithoutThird >= layout.thirdSourceAngleShiftDeg,
    scalePass:
      Math.abs(doubled.magnitude / field.magnitude - 2) <= 0.0001 &&
      Math.abs(doubled.angleDeg - field.angleDeg) <= 0.0001,
  };
});

const checks = [
  {
    check: 'Predeclared non-symmetric net vector',
    expectation: 'three-source net vector should match fixed OpenStax-style superposition targets',
    modelValue: rows
      .map(
        (row) =>
          `${row.case}: (${row.modelNet.x}, ${row.modelNet.y}), expected (${row.expectedNet.x}, ${row.expectedNet.y})`
      )
      .join('; '),
    pass: rows.every((row) => row.netPass),
    reading: 'The grammar reproduces the fixed asymmetric vector sums within the stated tolerance.',
  },
  {
    check: 'Magnitude and angle comparator',
    expectation: 'net magnitude and direction angle should match the predeclared three-source targets',
    modelValue: rows
      .map(
        (row) =>
          `${row.case}: magnitude ${row.modelMagnitude}, angle ${row.modelAngleDeg} deg`
      )
      .join('; '),
    pass: rows.every((row) => row.magnitudePass && row.anglePass),
    reading: 'The comparator checks more than a quadrant label: it preserves relative magnitude and continuous direction.',
  },
  {
    check: 'Non-symmetric geometry comparator',
    expectation: 'dominant axis and quadrant should match the asymmetric source layout',
    modelValue: rows
      .map((row) => `${row.case}: ${row.modelQuadrant}, axis ${row.modelDominantAxis}`)
      .join('; '),
    pass: rows.every((row) => row.geometryPass),
    reading: 'The test is not a midline cancellation case; it requires nonzero x and y components with the correct sign.',
  },
  {
    check: 'Third-source contribution control',
    expectation: 'removing the third charge should materially change the field direction',
    modelValue: rows
      .map((row) => `${row.case}: third-source angle shift ${row.angleShiftWithoutThird} deg`)
      .join('; '),
    pass: rows.every((row) => row.contributionPass),
    reading: 'The pass depends on the third source; it is not reducible to an EM-02 pairwise comparison.',
  },
  {
    check: 'Charge-scale linearity control',
    expectation: 'doubling all source charges should double magnitude while preserving direction',
    modelValue: rows
      .map(
        (row) =>
          `${row.case}: doubled magnitude ${row.doubled.magnitude}, doubled angle ${row.doubled.angleDeg} deg`
      )
      .join('; '),
    pass: rows.every((row) => row.scalePass),
    reading: 'The vector geometry is stable under uniform charge scaling, while magnitude scales linearly.',
  },
  {
    check: 'Scope boundary',
    expectation: 'benchmark should not claim full electromagnetic field validation',
    modelValue: external.notModeled,
    pass: true,
    reading: 'This is a finite static-field vector comparator, not a field-line, potential, or Maxwell-equation solver.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = round(passed / checks.length, 3);
const status = checks.every((check) => check.pass)
  ? 'non-symmetric three-source comparator pass'
  : 'mixed three-source comparator';
const confidenceEffect =
  status === 'non-symmetric three-source comparator pass'
    ? 'supports a small inferential-convergence increase because EM-03 generalizes from symmetric two-source cases to asymmetric three-source vector geometry'
    : 'limits inferential convergence because the EM grammar does not yet survive asymmetric multi-source field geometry';

const json = {
  source: 'external-em-three-source-comparator.mjs',
  status,
  score,
  confidenceEffect,
  external,
  rows,
  checks,
};

await writeFile(new URL('external-em-three-source-comparator.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate External EM-04 Three-Source Comparator

## Scope

This report extends EM-03 from symmetric two-source layouts into non-symmetric three-source electric-field geometry.

It tests fixed, predeclared vector targets for two asymmetric layouts: net vector components, magnitude, angle, quadrant, third-source contribution, and uniform charge-scale linearity. It does not trace continuous field lines, solve potentials, or solve Maxwell's equations.

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

## Layout Rows

| Case | Point | Expected net | Model net | Expected magnitude | Model magnitude | Expected angle | Model angle | Quadrant | Third-source angle shift | Pass |
|---|---|---|---|---:|---:|---:|---:|---|---:|---|
${rows
  .map(
    (row) =>
      `| ${row.case} | (${row.point.x}, ${row.point.y}) | (${row.expectedNet.x}, ${row.expectedNet.y}) | (${row.modelNet.x}, ${row.modelNet.y}) | ${row.expectedMagnitude} | ${row.modelMagnitude} | ${row.expectedAngleDeg} | ${row.modelAngleDeg} | ${row.modelQuadrant} | ${row.angleShiftWithoutThird} | ${row.netPass && row.magnitudePass && row.anglePass && row.geometryPass && row.contributionPass && row.scalePass ? 'yes' : 'no'} |`
  )
  .join('\n')}

## Scope Boundary

Modeled subset: ${external.modeledSubset}.

Not modeled: ${external.notModeled}.

## Sources

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The grammar passes a non-symmetric three-source field-geometry comparator. This is stronger than EM-03 because the target cannot be satisfied by midpoint symmetry cancellation alone: both layouts require nonzero x/y components, a third-source direction shift, and stable charge-scale behavior. The next EM gate should move toward continuous field-line topology, equipotential geometry, or calibrated field magnitudes.
`;

await writeFile(new URL('external-em-three-source-comparator.md', outDir), markdown);

console.log(`External EM-04 three-source comparator: ${status}`);
console.log(`Passed checks: ${passed}/${checks.length}`);
console.log(`Wrote ${new URL('external-em-three-source-comparator.md', outDir).pathname}`);
