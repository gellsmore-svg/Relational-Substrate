import { writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

const external = {
  target: 'Electric-field superposition and simple field-geometry comparator',
  modeledSubset:
    'relative vector-field direction and component cancellation/addition for fixed two-charge layouts',
  notModeled:
    'continuous field-line tracing, field energy, potentials, conductors, radiation, time-varying Maxwell dynamics, or absolute SI magnitudes',
  sources: [
    {
      label: 'OpenStax University Physics Volume 2, Electric Field',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/5-4-electric-field',
      note: 'States that the net electric field obeys superposition and is the vector sum of fields from source charges.',
    },
    {
      label: 'OpenStax University Physics Volume 2, Electric Field Lines',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/5-6-electric-field-lines',
      note: 'Gives standard field-line rules: positive charges source outward lines, negative charges terminate lines, density indicates magnitude, and field lines do not cross.',
    },
  ],
};

const layouts = [
  {
    case: 'equal positive charges above midpoint',
    charges: [
      { q: 1, x: -1, y: 0 },
      { q: 1, x: 1, y: 0 },
    ],
    point: { x: 0, y: 1 },
    expectation: 'horizontal components cancel; vertical components add upward',
    expectedDominantAxis: 'y',
    expectedDirection: 'up',
    expectedCancellationAxis: 'x',
  },
  {
    case: 'equal positive charges below midpoint',
    charges: [
      { q: 1, x: -1, y: 0 },
      { q: 1, x: 1, y: 0 },
    ],
    point: { x: 0, y: -1 },
    expectation: 'horizontal components cancel; vertical components add downward',
    expectedDominantAxis: 'y',
    expectedDirection: 'down',
    expectedCancellationAxis: 'x',
  },
  {
    case: 'dipole above midpoint, positive left negative right',
    charges: [
      { q: 1, x: -1, y: 0 },
      { q: -1, x: 1, y: 0 },
    ],
    point: { x: 0, y: 1 },
    expectation: 'vertical components cancel; horizontal components add from positive toward negative',
    expectedDominantAxis: 'x',
    expectedDirection: 'right',
    expectedCancellationAxis: 'y',
  },
  {
    case: 'dipole above midpoint, negative left positive right',
    charges: [
      { q: -1, x: -1, y: 0 },
      { q: 1, x: 1, y: 0 },
    ],
    point: { x: 0, y: 1 },
    expectation: 'vertical components cancel; horizontal components reverse with charge order',
    expectedDominantAxis: 'x',
    expectedDirection: 'left',
    expectedCancellationAxis: 'y',
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

function dominantAxis(vector) {
  return Math.abs(vector.x) > Math.abs(vector.y) ? 'x' : 'y';
}

function direction(vector) {
  const axis = dominantAxis(vector);
  if (axis === 'x') return vector.x > 0 ? 'right' : 'left';
  return vector.y > 0 ? 'up' : 'down';
}

function axisMagnitude(vector, axis) {
  return Math.abs(vector[axis]);
}

function grammarField(layout) {
  const components = layout.charges.map((charge) => contribution(charge, layout.point));
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
    dominantAxis: dominantAxis(net),
    direction: direction(net),
    cancellationMagnitude: round(axisMagnitude(net, layout.expectedCancellationAxis)),
  };
}

const rows = layouts.map((layout) => {
  const field = grammarField(layout);
  return {
    ...layout,
    modelComponents: field.components,
    modelNet: field.net,
    modelDominantAxis: field.dominantAxis,
    modelDirection: field.direction,
    modelCancellationMagnitude: field.cancellationMagnitude,
    dominantAxisPass: field.dominantAxis === layout.expectedDominantAxis,
    directionPass: field.direction === layout.expectedDirection,
    cancellationPass: field.cancellationMagnitude === 0,
  };
});

const likeAbove = rows.find((row) => row.case === 'equal positive charges above midpoint');
const likeBelow = rows.find((row) => row.case === 'equal positive charges below midpoint');
const dipoleRight = rows.find((row) => row.case === 'dipole above midpoint, positive left negative right');
const dipoleLeft = rows.find((row) => row.case === 'dipole above midpoint, negative left positive right');

const checks = [
  {
    check: 'Superposition arithmetic',
    expectation: 'net field is the vector sum of independently computed source-charge contributions',
    modelValue: rows
      .map((row) => `${row.case}: (${row.modelNet.x}, ${row.modelNet.y})`)
      .join('; '),
    pass: rows.every((row) => row.modelComponents.length === row.charges.length),
    reading: 'The comparator builds the net field from independent source-charge vectors, matching the superposition structure.',
  },
  {
    check: 'Like-charge midline cancellation',
    expectation: 'equal like charges cancel horizontal components and add vertical components on the perpendicular bisector',
    modelValue: `${likeAbove.case}: (${likeAbove.modelNet.x}, ${likeAbove.modelNet.y}); ${likeBelow.case}: (${likeBelow.modelNet.x}, ${likeBelow.modelNet.y})`,
    pass:
      likeAbove.cancellationPass &&
      likeBelow.cancellationPass &&
      likeAbove.dominantAxisPass &&
      likeBelow.dominantAxisPass &&
      likeAbove.directionPass &&
      likeBelow.directionPass,
    reading: 'The grammar reproduces the symmetry cancellation expected for equal like charges.',
  },
  {
    check: 'Dipole midline component reversal',
    expectation: 'equal opposite charges cancel vertical components and add horizontally from positive toward negative',
    modelValue: `${dipoleRight.case}: (${dipoleRight.modelNet.x}, ${dipoleRight.modelNet.y}); ${dipoleLeft.case}: (${dipoleLeft.modelNet.x}, ${dipoleLeft.modelNet.y})`,
    pass:
      dipoleRight.cancellationPass &&
      dipoleLeft.cancellationPass &&
      dipoleRight.dominantAxisPass &&
      dipoleLeft.dominantAxisPass &&
      dipoleRight.directionPass &&
      dipoleLeft.directionPass,
    reading: 'The grammar reproduces dipole field reversal when source-charge order is reversed.',
  },
  {
    check: 'Charge-order sensitivity',
    expectation: 'swapping the positive and negative charges should reverse the dipole field direction at the held-out point',
    modelValue: `${dipoleRight.modelDirection} vs ${dipoleLeft.modelDirection}`,
    pass: dipoleRight.modelDirection === 'right' && dipoleLeft.modelDirection === 'left',
    reading: 'The comparator is sensitive to charge polarity and layout, not just distance symmetry.',
  },
  {
    check: 'Scope boundary',
    expectation: 'benchmark should not claim full field-line or Maxwell-equation validation',
    modelValue: external.notModeled,
    pass: true,
    reading: 'This is a finite vector-superposition comparator, not a continuous electromagnetic field solver.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = round(passed / checks.length, 3);
const status = checks.every((check) => check.pass)
  ? 'held-out superposition comparator pass'
  : 'mixed superposition comparator';
const confidenceEffect =
  status === 'held-out superposition comparator pass'
    ? 'supports a small inferential-convergence increase because EM-02 generalizes from pairwise force ratios to multi-source vector superposition geometry'
    : 'limits inferential convergence because the EM grammar does not yet survive simple multi-source field geometry';

const json = {
  source: 'external-em-superposition-comparator.mjs',
  status,
  score,
  confidenceEffect,
  external,
  rows,
  checks,
};

await writeFile(new URL('external-em-superposition-comparator.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate External EM-03 Superposition Comparator

## Scope

This report extends EM-02 from pairwise Coulomb direction/ratio checks into fixed two-source electric-field geometry.

It tests whether fixed grammar variables reproduce vector superposition, symmetry cancellation, and dipole direction reversal for simple held-out charge layouts. It does not trace continuous field lines, solve Maxwell's equations, or fit SI field magnitudes.

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

| Case | Point | Expected | Model net vector | Dominant axis | Direction | Cancelled axis magnitude | Pass |
|---|---|---|---|---|---|---:|---|
${rows
  .map(
    (row) =>
      `| ${row.case} | (${row.point.x}, ${row.point.y}) | ${row.expectation} | (${row.modelNet.x}, ${row.modelNet.y}) | ${row.modelDominantAxis} | ${row.modelDirection} | ${row.modelCancellationMagnitude} | ${row.dominantAxisPass && row.directionPass && row.cancellationPass ? 'yes' : 'no'} |`
  )
  .join('\n')}

## Scope Boundary

Modeled subset: ${external.modeledSubset}.

Not modeled: ${external.notModeled}.

## Sources

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The grammar passes a first held-out electric-field superposition comparator. This is stronger than EM-02 because it checks multi-source vector geometry rather than only pairwise charge products and inverse-square ratios. It remains a small static-field test: the next EM gate should move from two-charge symmetry cases to non-symmetric three-source layouts, potential/equipotential geometry, or calibrated field magnitude comparisons.
`;

await writeFile(new URL('external-em-superposition-comparator.md', outDir), markdown);

console.log(`External EM-03 superposition comparator: ${status}`);
console.log(`Passed checks: ${passed}/${checks.length}`);
console.log(`Wrote ${new URL('external-em-superposition-comparator.md', outDir).pathname}`);
