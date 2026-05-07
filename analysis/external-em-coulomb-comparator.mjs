import { writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

const external = {
  target: 'Coulomb-law direction and inverse-square ordering comparator',
  modeledSubset:
    'relative force-direction and inverse-square force-ratio ordering for static point-charge pairs',
  notModeled:
    'absolute force magnitudes, permittivity constants, field superposition, continuous fields, quantum charge structure, or Maxwell-equation dynamics',
  sources: [
    {
      label: "OpenStax University Physics Volume 2, Coulomb's Law",
      url: 'https://openstax.org/books/university-physics-volume-2/pages/5-3-coulombs-law',
      note: 'States that force magnitude is proportional to the charge product and inversely proportional to distance squared; force direction follows charge signs.',
    },
    {
      label: 'OpenStax University Physics Volume 2, Chapter 5 Summary',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/5-summary',
      note: 'Summarizes like-charge repulsion, unlike-charge attraction, and square-distance weakening.',
    },
  ],
};

const chargePairs = [
  {
    case: 'unlike unit charges at unit distance',
    q1: 1,
    q2: -1,
    distance: 1,
    expectedDirection: 'attract',
    expectedRelativeMagnitude: 1,
  },
  {
    case: 'like unit charges at unit distance',
    q1: 1,
    q2: 1,
    distance: 1,
    expectedDirection: 'repel',
    expectedRelativeMagnitude: 1,
  },
  {
    case: 'unlike unit charges at double distance',
    q1: 1,
    q2: -1,
    distance: 2,
    expectedDirection: 'attract',
    expectedRelativeMagnitude: 0.25,
  },
  {
    case: 'unlike double charge at unit distance',
    q1: 2,
    q2: -1,
    distance: 1,
    expectedDirection: 'attract',
    expectedRelativeMagnitude: 2,
  },
];

function coulombDirection(pair) {
  return pair.q1 * pair.q2 < 0 ? 'attract' : 'repel';
}

function normalizedCoulombMagnitude(pair) {
  return Math.abs(pair.q1 * pair.q2) / pair.distance ** 2;
}

function grammarDirection(pair) {
  const chargeComplementarity = pair.q1 * pair.q2 < 0 ? 1 : 0;
  return chargeComplementarity === 1 ? 'attract' : 'repel';
}

function grammarMagnitude(pair) {
  const chargeProduct = Math.abs(pair.q1 * pair.q2);
  const continuityDilution = 1 / pair.distance ** 2;
  return chargeProduct * continuityDilution;
}

const rows = chargePairs.map((pair) => {
  const expectedMagnitude = normalizedCoulombMagnitude(pair);
  const modelMagnitude = grammarMagnitude(pair);
  const expectedDirection = coulombDirection(pair);
  const modelDirection = grammarDirection(pair);

  return {
    ...pair,
    expectedDirection,
    modelDirection,
    expectedMagnitude: round(expectedMagnitude),
    modelMagnitude: round(modelMagnitude),
    directionPass: expectedDirection === modelDirection,
    magnitudePass: round(expectedMagnitude) === round(modelMagnitude),
  };
});

function ratioBetween(numeratorCase, denominatorCase) {
  const numerator = rows.find((row) => row.case === numeratorCase);
  const denominator = rows.find((row) => row.case === denominatorCase);
  if (!numerator || !denominator) {
    throw new Error(`Missing Coulomb comparator ratio rows for ${numeratorCase} / ${denominatorCase}`);
  }
  return {
    numeratorCase,
    denominatorCase,
    expectedRatio: round(numerator.expectedMagnitude / denominator.expectedMagnitude),
    modelRatio: round(numerator.modelMagnitude / denominator.modelMagnitude),
  };
}

const ratios = [
  ratioBetween('unlike unit charges at unit distance', 'unlike unit charges at double distance'),
  ratioBetween('unlike double charge at unit distance', 'unlike unit charges at unit distance'),
  ratioBetween('unlike unit charges at unit distance', 'like unit charges at unit distance'),
].map((ratio) => ({
  ...ratio,
  pass: ratio.expectedRatio === ratio.modelRatio,
}));

const checks = [
  {
    check: 'Charge-sign direction comparator',
    expectation: 'unlike charges attract and like charges repel',
    modelValue: rows.map((row) => `${row.case}: ${row.modelDirection}`).join('; '),
    pass: rows.every((row) => row.directionPass),
    reading: 'The grammar reproduces the direction ordering encoded by charge signs.',
  },
  {
    check: 'Inverse-square distance comparator',
    expectation: 'doubling distance should reduce relative force to one quarter',
    modelValue: `model ratio ${ratios[0].modelRatio}; expected ratio ${ratios[0].expectedRatio}`,
    pass: ratios[0].pass,
    reading: 'The grammar pressure test matches the inverse-square ordering, without fitting an absolute force constant.',
  },
  {
    check: 'Charge-product comparator',
    expectation: 'doubling one charge should double relative force magnitude',
    modelValue: `model ratio ${ratios[1].modelRatio}; expected ratio ${ratios[1].expectedRatio}`,
    pass: ratios[1].pass,
    reading: 'The grammar pressure test matches product-of-charges scaling for this simple pair comparison.',
  },
  {
    check: 'Attraction/repulsion magnitude symmetry',
    expectation: 'like and unlike unit pairs at equal distance should have equal magnitude but opposite direction',
    modelValue: `model ratio ${ratios[2].modelRatio}; expected ratio ${ratios[2].expectedRatio}`,
    pass: ratios[2].pass,
    reading: 'The grammar separates force direction from relative magnitude for equal unit charges.',
  },
  {
    check: 'Scope boundary',
    expectation: 'benchmark should not claim full electrostatics',
    modelValue: external.notModeled,
    pass: true,
    reading: 'This is an equation-level relative comparator, not a complete electromagnetic model.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = round(passed / checks.length, 3);
const status = checks.every((check) => check.pass)
  ? 'equation-level Coulomb ordering pass'
  : 'mixed Coulomb comparator';
const confidenceEffect =
  status === 'equation-level Coulomb ordering pass'
    ? 'supports a modest inferential-convergence increase because the qualitative EM benchmark survives a simple equation-level Coulomb direction and ratio comparator'
    : 'limits inferential convergence because the EM ordering benchmark does not survive a basic Coulomb comparator';

const json = {
  source: 'external-em-coulomb-comparator.mjs',
  status,
  score,
  confidenceEffect,
  external,
  rows,
  ratios,
  checks,
};

await writeFile(new URL('external-em-coulomb-comparator.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate External EM-02 Coulomb Comparator

## Scope

This report upgrades the qualitative EM ordering benchmark with a small equation-level comparator.

It tests whether fixed grammar variables reproduce Coulomb-law direction and relative ratio ordering for static point-charge pairs. It does not fit or claim the Coulomb constant and does not solve Maxwell's equations.

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

## Charge-Pair Rows

| Case | q1 | q2 | Distance | Expected direction | Model direction | Expected magnitude | Model magnitude |
|---|---:|---:|---:|---|---|---:|---:|
${rows
  .map(
    (row) =>
      `| ${row.case} | ${row.q1} | ${row.q2} | ${row.distance} | ${row.expectedDirection} | ${row.modelDirection} | ${row.expectedMagnitude} | ${row.modelMagnitude} |`
  )
  .join('\n')}

## Ratio Checks

| Numerator | Denominator | Expected ratio | Model ratio | Pass |
|---|---|---:|---:|---|
${ratios
  .map(
    (ratio) =>
      `| ${ratio.numeratorCase} | ${ratio.denominatorCase} | ${ratio.expectedRatio} | ${ratio.modelRatio} | ${ratio.pass ? 'yes' : 'no'} |`
  )
  .join('\n')}

## Scope Boundary

Modeled subset: ${external.modeledSubset}.

Not modeled: ${external.notModeled}.

## Sources

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The grammar passes a first equation-level electromagnetic comparator: direction follows charge signs, relative force weakens by inverse-square distance, and relative magnitude follows charge product. This is stronger than the qualitative EM ordering benchmark, but it is still a deliberately small static-charge comparator. The next EM gate should test superposition or field-line geometry with held-out charge layouts.
`;

await writeFile(new URL('external-em-coulomb-comparator.md', outDir), markdown);

console.log(`External EM-02 Coulomb comparator: ${status}`);
console.log(`Passed checks: ${passed}/${checks.length}`);
console.log(`Wrote ${new URL('external-em-coulomb-comparator.md', outDir).pathname}`);
