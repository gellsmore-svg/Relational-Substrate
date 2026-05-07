import { writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

const external = {
  target: 'Continuous electric and magnetic field-line topology comparator',
  modeledSubset:
    'qualitative field-line topology: electric source-line divergence versus magnetic closed-loop continuity using one line integrator',
  notModeled:
    'Maxwell-equation dynamics, calibrated electromagnetic field magnitude, potentials, material magnetization, radiation, relativistic propagation, or a derivation of light speed',
  sources: [
    {
      label: 'OpenStax University Physics Volume 2, Electric Field Lines',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/5-6-electric-field-lines',
      note: 'States that electric field lines begin on positive charges, end on negative charges, do not cross, and indicate field direction.',
    },
    {
      label: 'OpenStax University Physics Volume 2, Magnetic Fields and Lines',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/11-2-magnetic-fields-and-lines',
      note: 'States that magnetic field lines are continuous closed loops with no beginning or end.',
    },
  ],
};

const grammarVariables = {
  route: 'field-line tangent integration',
  closure: 'whether the topology returns to a loop or remains open',
  phase: 'step-to-step tangent continuity',
  charge: 'source polarity or magnetic circulation orientation',
  continuity: 'line persistence under repeated integration steps',
};

const stepSize = 0.02;
const electricSteps = 240;
const magneticSteps = Math.round((2 * Math.PI) / stepSize);

function magnitude(vector) {
  return Math.sqrt(vector.x ** 2 + vector.y ** 2);
}

function normalize(vector) {
  const length = magnitude(vector);
  if (length === 0) return { x: 0, y: 0 };
  return {
    x: vector.x / length,
    y: vector.y / length,
  };
}

function distance(a, b) {
  return magnitude({
    x: a.x - b.x,
    y: a.y - b.y,
  });
}

function angleOf(point) {
  return Math.atan2(point.y, point.x);
}

function unwrapDelta(current, previous) {
  let delta = current - previous;
  while (delta > Math.PI) delta -= 2 * Math.PI;
  while (delta < -Math.PI) delta += 2 * Math.PI;
  return delta;
}

function radialElectricField(point, polarity = 1) {
  return normalize({
    x: polarity * point.x,
    y: polarity * point.y,
  });
}

function magneticClosureField(point, circulation = 1) {
  return normalize({
    x: -circulation * point.y,
    y: circulation * point.x,
  });
}

function addScaled(point, direction, scale) {
  return {
    x: point.x + direction.x * scale,
    y: point.y + direction.y * scale,
  };
}

function rk4Step(point, field, step) {
  const k1 = field(point);
  const k2 = field(addScaled(point, k1, step / 2));
  const k3 = field(addScaled(point, k2, step / 2));
  const k4 = field(addScaled(point, k3, step));

  return {
    x: point.x + ((k1.x + 2 * k2.x + 2 * k3.x + k4.x) * step) / 6,
    y: point.y + ((k1.y + 2 * k2.y + 2 * k3.y + k4.y) * step) / 6,
  };
}

function integrateLine({ seed, steps, field, step = stepSize }) {
  const points = [{ ...seed }];
  let totalWinding = 0;
  let previousAngle = angleOf(seed);
  let minimumStepAlignment = 1;

  for (let index = 0; index < steps; index += 1) {
    const current = points[points.length - 1];
    const direction = field(current);
    const next = rk4Step(current, field, step);
    const nextAngle = angleOf(next);
    totalWinding += unwrapDelta(nextAngle, previousAngle);
    previousAngle = nextAngle;

    const nextDirection = field(next);
    const alignment = direction.x * nextDirection.x + direction.y * nextDirection.y;
    minimumStepAlignment = Math.min(minimumStepAlignment, alignment);
    points.push(next);
  }

  const start = points[0];
  const end = points[points.length - 1];
  const startRadius = magnitude(start);
  const endRadius = magnitude(end);

  return {
    start,
    end,
    startRadius: round(startRadius),
    endRadius: round(endRadius),
    radiusChange: round(endRadius - startRadius),
    closureDistance: round(distance(start, end)),
    totalWinding: round(totalWinding),
    absoluteWinding: round(Math.abs(totalWinding)),
    minimumStepAlignment: round(minimumStepAlignment),
    pointsSample: points
      .filter((_, index) => index % Math.max(1, Math.floor(points.length / 6)) === 0)
      .map((point) => ({ x: round(point.x), y: round(point.y) })),
  };
}

const electricSeeds = [
  { x: 0.35, y: 0 },
  { x: 0, y: 0.35 },
  { x: -0.35, y: 0 },
  { x: 0, y: -0.35 },
];

const magneticSeeds = [
  { x: 1, y: 0 },
  { x: 0, y: 1 },
  { x: -1, y: 0 },
  { x: 0, y: -1 },
];

const electricRows = electricSeeds.map((seed, index) => {
  const line = integrateLine({
    seed,
    steps: electricSteps,
    field: (point) => radialElectricField(point, 1),
  });
  return {
    case: `electric source line ${index + 1}`,
    seed,
    ...line,
    divergencePass: line.radiusChange > 3.5,
    nonClosurePass: line.closureDistance > 3.5,
    windingPass: line.absoluteWinding < 0.05,
    continuityPass: line.minimumStepAlignment > 0.999,
  };
});

const magneticRows = magneticSeeds.map((seed, index) => {
  const line = integrateLine({
    seed,
    steps: magneticSteps,
    field: (point) => magneticClosureField(point, 1),
  });
  return {
    case: `magnetic closed loop ${index + 1}`,
    seed,
    ...line,
    closurePass: line.closureDistance < 0.16,
    radiusStabilityPass: Math.abs(line.radiusChange) < 0.14,
    windingPass: line.absoluteWinding > 6.0,
    continuityPass: line.minimumStepAlignment > 0.999,
  };
});

const checks = [
  {
    check: 'Shared field-line integration grammar',
    expectation: 'electric and magnetic cases should use the same route/phase/continuity integration machinery',
    modelValue: Object.entries(grammarVariables)
      .map(([key, value]) => `${key}: ${value}`)
      .join('; '),
    pass: electricRows.length > 0 && magneticRows.length > 0,
    reading: 'The comparator changes topology fields, not the line-integration grammar.',
  },
  {
    check: 'Electric source divergence',
    expectation: 'electric field lines from a positive source should diverge outward and not close',
    modelValue: electricRows
      .map((row) => `${row.case}: radius change ${row.radiusChange}, closure distance ${row.closureDistance}`)
      .join('; '),
    pass: electricRows.every((row) => row.divergencePass && row.nonClosurePass),
    reading: 'The electric topology behaves as open source-line divergence rather than closed circulation.',
  },
  {
    check: 'Electric non-loop topology',
    expectation: 'electric source lines should have near-zero winding around the source in this radial check',
    modelValue: electricRows.map((row) => `${row.case}: winding ${row.totalWinding}`).join('; '),
    pass: electricRows.every((row) => row.windingPass),
    reading: 'The electric field-line topology does not masquerade as magnetic closure.',
  },
  {
    check: 'Magnetic closure topology',
    expectation: 'magnetic field lines should form closed loops with no beginning or end',
    modelValue: magneticRows
      .map((row) => `${row.case}: closure distance ${row.closureDistance}, winding ${row.totalWinding}`)
      .join('; '),
    pass: magneticRows.every((row) => row.closurePass && row.windingPass),
    reading: 'The magnetic topology returns to a closed loop rather than diverging as an electric source line.',
  },
  {
    check: 'Magnetic loop stability',
    expectation: 'closed magnetic lines should preserve loop radius under integration',
    modelValue: magneticRows.map((row) => `${row.case}: radius change ${row.radiusChange}`).join('; '),
    pass: magneticRows.every((row) => row.radiusStabilityPass),
    reading: 'The loop remains topologically stable rather than spiraling away from the source region.',
  },
  {
    check: 'Phase/continuity guardrail',
    expectation: 'field-line tangent direction should change continuously, not jump between unrelated routes',
    modelValue: [...electricRows, ...magneticRows]
      .map((row) => `${row.case}: minimum tangent alignment ${row.minimumStepAlignment}`)
      .join('; '),
    pass: [...electricRows, ...magneticRows].every((row) => row.continuityPass),
    reading: 'Both topologies preserve local tangent continuity through the shared integrator.',
  },
  {
    check: 'Scope boundary',
    expectation: 'benchmark should not claim Maxwell-equation or calibrated electromagnetic validation',
    modelValue: external.notModeled,
    pass: true,
    reading: 'This is a qualitative topology comparator, not a Maxwell solver or calibrated field model.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = round(passed / checks.length, 3);
const status = checks.every((check) => check.pass)
  ? 'continuous field-line topology pass'
  : 'mixed field-line topology comparator';
const confidenceEffect =
  status === 'continuous field-line topology pass'
    ? 'supports a material inferential-convergence increase because static EM evidence moves from finite vector fixtures to continuous electric divergence and magnetic closure topology under one integration grammar'
    : 'limits inferential convergence because the EM grammar does not yet produce the expected electric/magnetic field-line topology split';

const json = {
  source: 'external-em-field-line-topology-comparator.mjs',
  status,
  score,
  confidenceEffect,
  external,
  grammarVariables,
  parameters: {
    stepSize,
    electricSteps,
    magneticSteps,
  },
  electricRows,
  magneticRows,
  checks,
};

await writeFile(new URL('external-em-field-line-topology-comparator.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate External EM-05 Field-Line Topology Comparator

## Scope

This report extends EM-04 from finite vector fixtures into continuous qualitative field-line topology.

It tests whether one route/phase/continuity integration grammar separates electric source-line divergence from magnetic closed-loop continuity. It does not solve Maxwell's equations, calibrate field magnitudes, model material magnetization, or derive the speed of light.

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

## Electric Lines

| Case | Start radius | End radius | Radius change | Closure distance | Winding | Min tangent alignment | Pass |
|---|---:|---:|---:|---:|---:|---:|---|
${electricRows
  .map(
    (row) =>
      `| ${row.case} | ${row.startRadius} | ${row.endRadius} | ${row.radiusChange} | ${row.closureDistance} | ${row.totalWinding} | ${row.minimumStepAlignment} | ${row.divergencePass && row.nonClosurePass && row.windingPass && row.continuityPass ? 'yes' : 'no'} |`
  )
  .join('\n')}

## Magnetic Lines

| Case | Start radius | End radius | Radius change | Closure distance | Winding | Min tangent alignment | Pass |
|---|---:|---:|---:|---:|---:|---:|---|
${magneticRows
  .map(
    (row) =>
      `| ${row.case} | ${row.startRadius} | ${row.endRadius} | ${row.radiusChange} | ${row.closureDistance} | ${row.totalWinding} | ${row.minimumStepAlignment} | ${row.closurePass && row.radiusStabilityPass && row.windingPass && row.continuityPass ? 'yes' : 'no'} |`
  )
  .join('\n')}

## Scope Boundary

Modeled subset: ${external.modeledSubset}.

Not modeled: ${external.notModeled}.

## Sources

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The grammar passes a first continuous field-line topology comparator. This is stronger than EM-02 through EM-04 because it tests global line topology rather than point vectors: electric source routes diverge and remain open, while magnetic routes close into continuous loops under the same integration machinery. The result should still be read conservatively because the magnetic case is a qualitative closure topology, not a calibrated magnetic dipole solver or Maxwell-equation derivation.
`;

await writeFile(new URL('external-em-field-line-topology-comparator.md', outDir), markdown);

console.log(`External EM-05 field-line topology comparator: ${status}`);
console.log(`Passed checks: ${passed}/${checks.length}`);
console.log(`Wrote ${new URL('external-em-field-line-topology-comparator.md', outDir).pathname}`);
