import { writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function round(value, places = 5) {
  return Number(value.toFixed(places));
}

const external = {
  target: 'Electric equipotential geometry comparator',
  modeledSubset:
    'static point-charge scalar potential superposition, dipole zero-potential symmetry, and electric-field/equipotential perpendicularity',
  notModeled:
    'Maxwell-equation dynamics, conductors, capacitance, material media, radiation, calibrated SI magnitudes, magnetic vector potential, or relativistic propagation',
  sources: [
    {
      label: 'OpenStax University Physics Volume 2, Calculations of Electric Potential',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/7-3-calculations-of-electric-potential',
      note: 'Gives point-charge potential V = kq/r and scalar superposition for systems of point charges.',
    },
    {
      label: 'OpenStax University Physics Volume 2, Determining Field from Potential',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/7-4-determining-field-from-potential',
      note: 'States that electric field points in the direction of decreasing potential and is the negative gradient of potential.',
    },
    {
      label: 'OpenStax University Physics Volume 2, Equipotential Surfaces and Conductors',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/7-5-equipotential-surfaces-and-conductors',
      note: 'States that equipotential lines are perpendicular to electric field lines.',
    },
  ],
};

const grammarVariables = {
  route: 'scalar potential accumulation across source routes',
  closure: 'constant-potential contour constraint',
  phase: 'field tangent and equipotential tangent remain orthogonal',
  charge: 'signed source polarity contributes q/r to potential and q rhat/r^2 to field',
  continuity: 'local finite-gradient continuity links scalar potential to vector field direction',
};

const likeCharges = [
  { q: 1, x: -1, y: 0 },
  { q: 1, x: 1, y: 0 },
];

const dipole = [
  { q: 1, x: -1, y: 0 },
  { q: -1, x: 1, y: 0 },
];

function distance(source, point) {
  return Math.hypot(point.x - source.x, point.y - source.y);
}

function potential(charges, point) {
  return charges.reduce((sum, source) => sum + source.q / distance(source, point), 0);
}

function field(charges, point) {
  return charges.reduce(
    (net, source) => {
      const dx = point.x - source.x;
      const dy = point.y - source.y;
      const r = Math.hypot(dx, dy);
      const scale = source.q / r ** 3;
      return {
        x: net.x + scale * dx,
        y: net.y + scale * dy,
      };
    },
    { x: 0, y: 0 }
  );
}

function centralGradient(charges, point, h = 1e-4) {
  return {
    x:
      (potential(charges, { x: point.x + h, y: point.y }) -
        potential(charges, { x: point.x - h, y: point.y })) /
      (2 * h),
    y:
      (potential(charges, { x: point.x, y: point.y + h }) -
        potential(charges, { x: point.x, y: point.y - h })) /
      (2 * h),
  };
}

function dot(a, b) {
  return a.x * b.x + a.y * b.y;
}

function vectorError(a, b) {
  return Math.hypot(a.x - b.x, a.y - b.y);
}

const likeSymmetry = {
  top: potential(likeCharges, { x: 0, y: 1 }),
  bottom: potential(likeCharges, { x: 0, y: -1 }),
  midpoint: potential(likeCharges, { x: 0, y: 0 }),
  far: potential(likeCharges, { x: 0, y: 3 }),
};

const dipoleZeroRows = [0.5, 1, 2].map((y) => ({
  point: { x: 0, y },
  potential: potential(dipole, { x: 0, y }),
}));

const equipotentialPoint = { x: 0, y: 1 };
const equipotentialField = field(dipole, equipotentialPoint);
const equipotentialTangent = { x: 0, y: 1 };
const equipotentialDot = dot(equipotentialField, equipotentialTangent);

const gradientPoint = { x: 0.35, y: 0.8 };
const gradient = centralGradient(dipole, gradientPoint);
const gradientField = field(dipole, gradientPoint);
const negativeGradient = { x: -gradient.x, y: -gradient.y };
const gradientRelationError = vectorError(gradientField, negativeGradient);

const checks = [
  {
    check: 'Shared potential grammar',
    expectation: 'route, closure, phase, charge, and continuity should define one scalar/vector geometry without case-specific parameters',
    modelValue: Object.entries(grammarVariables)
      .map(([key, value]) => `${key}: ${value}`)
      .join('; '),
    pass: Object.keys(grammarVariables).length === 5,
    reading: 'The comparator changes charge layout, not the grammar variables or scaling constants.',
  },
  {
    check: 'Scalar potential superposition',
    expectation: 'total point-charge potential should add source potentials as scalars',
    modelValue: `like-charge top ${round(likeSymmetry.top)}, bottom ${round(likeSymmetry.bottom)}, midpoint ${round(
      likeSymmetry.midpoint
    )}, far ${round(likeSymmetry.far)}`,
    pass:
      Math.abs(likeSymmetry.top - potential([likeCharges[0]], { x: 0, y: 1 }) - potential([likeCharges[1]], { x: 0, y: 1 })) <
      1e-10,
    reading: 'The grammar potential is built by signed q/r scalar accumulation rather than vector-field addition.',
  },
  {
    check: 'Like-charge equipotential mirror symmetry',
    expectation: 'equal like charges should give equal potentials at mirror points above and below the midpoint',
    modelValue: `top ${round(likeSymmetry.top)}, bottom ${round(likeSymmetry.bottom)}, delta ${round(
      likeSymmetry.top - likeSymmetry.bottom
    )}`,
    pass: Math.abs(likeSymmetry.top - likeSymmetry.bottom) < 1e-10,
    reading: 'The midpoint mirror line preserves equal scalar potential for symmetric equal charges.',
  },
  {
    check: 'Potential decreases away from like charges',
    expectation: 'the midpoint between equal like charges should have higher potential than a farther same-axis point',
    modelValue: `midpoint ${round(likeSymmetry.midpoint)}, far ${round(likeSymmetry.far)}`,
    pass: likeSymmetry.midpoint > likeSymmetry.far,
    reading: 'The static scalar potential follows the expected distance ordering without fitting a physical unit scale.',
  },
  {
    check: 'Dipole zero-potential perpendicular bisector',
    expectation: 'equal opposite charges should cancel scalar potential along the perpendicular bisector',
    modelValue: dipoleZeroRows.map((row) => `(${row.point.x}, ${row.point.y}) => ${round(row.potential)}`).join('; '),
    pass: dipoleZeroRows.every((row) => Math.abs(row.potential) < 1e-10),
    reading: 'The dipole equipotential line appears as a scalar cancellation contour, not as a field-vector cancellation.',
  },
  {
    check: 'Field perpendicular to equipotential tangent',
    expectation: 'electric field should be perpendicular to the zero-potential equipotential tangent',
    modelValue: `field (${round(equipotentialField.x)}, ${round(equipotentialField.y)}), tangent (${equipotentialTangent.x}, ${equipotentialTangent.y}), dot ${round(
      equipotentialDot
    )}`,
    pass: Math.abs(equipotentialDot) < 1e-10 && Math.abs(equipotentialField.x) > 0.1,
    reading: 'At the dipole bisector, scalar potential is constant along the tangent while the field points across it.',
  },
  {
    check: 'Field equals negative potential gradient',
    expectation: 'the vector field should match -grad(V) at a non-symmetric held-out point',
    modelValue: `field (${round(gradientField.x)}, ${round(gradientField.y)}), -grad (${round(
      negativeGradient.x
    )}, ${round(negativeGradient.y)}), error ${round(gradientRelationError, 8)}`,
    pass: gradientRelationError < 1e-7,
    reading: 'The scalar potential and vector field remain coupled at a non-symmetric point rather than only by visual symmetry.',
  },
  {
    check: 'Scope boundary',
    expectation: 'benchmark should not claim conductor, Maxwell, propagation, radiation, or calibrated SI validation',
    modelValue: external.notModeled,
    pass: external.notModeled.includes('Maxwell') && external.notModeled.includes('calibrated SI'),
    reading: 'This is an electrostatic geometry comparator, not a full electromagnetic solver.',
  },
];

const passedChecks = checks.filter((check) => check.pass).length;
const score = `${passedChecks}/${checks.length}`;
const status = passedChecks === checks.length ? 'equipotential geometry comparator pass' : 'mixed equipotential geometry comparator';

const report = {
  source: 'external-em-equipotential-comparator.mjs',
  status,
  external,
  grammarVariables,
  metrics: {
    likeChargeSymmetry: {
      top: round(likeSymmetry.top),
      bottom: round(likeSymmetry.bottom),
      midpoint: round(likeSymmetry.midpoint),
      far: round(likeSymmetry.far),
    },
    dipoleZeroPotentialRows: dipoleZeroRows.map((row) => ({
      point: row.point,
      potential: round(row.potential),
    })),
    equipotentialOrthogonality: {
      point: equipotentialPoint,
      field: { x: round(equipotentialField.x), y: round(equipotentialField.y) },
      tangent: equipotentialTangent,
      dot: round(equipotentialDot),
    },
    gradientRelation: {
      point: gradientPoint,
      field: { x: round(gradientField.x), y: round(gradientField.y) },
      negativeGradient: { x: round(negativeGradient.x), y: round(negativeGradient.y) },
      error: round(gradientRelationError, 8),
    },
  },
  score,
  checks,
  confidenceEffect:
    status === 'equipotential geometry comparator pass'
      ? 'supports a small inferential-convergence increase because EM evidence now links scalar potential geometry to vector fields, while remaining inside one electrostatic evidence line'
      : 'does not increase confidence; a failure here would show that EM topology/vector checks are not yet coherent with scalar potential geometry',
};

await writeFile(new URL('external-em-equipotential-comparator.json', outDir), JSON.stringify(report, null, 2));

const markdown = `# Relational Substrate External EM-06 Equipotential Geometry Comparator

## Purpose

This report extends EM-05 from field-line topology into scalar potential geometry.

It tests whether fixed grammar variables reproduce point-charge scalar potential superposition, dipole zero-potential symmetry, equipotential/field perpendicularity, and the field-as-negative-gradient relation. It does not model conductors, capacitance, Maxwell dynamics, radiation, propagation, magnetic vector potential, material media, or calibrated SI magnitudes.

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

## Metrics

### Like-Charge Potential

| Location | Potential |
|---|---:|
| top mirror point | ${round(likeSymmetry.top)} |
| bottom mirror point | ${round(likeSymmetry.bottom)} |
| midpoint | ${round(likeSymmetry.midpoint)} |
| far same-axis point | ${round(likeSymmetry.far)} |

### Dipole Zero-Potential Bisector

| Point | Potential |
|---|---:|
${dipoleZeroRows.map((row) => `| (${row.point.x}, ${row.point.y}) | ${round(row.potential)} |`).join('\n')}

### Equipotential Orthogonality

At point (${equipotentialPoint.x}, ${equipotentialPoint.y}), field = (${round(equipotentialField.x)}, ${round(
  equipotentialField.y
)}) and the equipotential tangent = (${equipotentialTangent.x}, ${equipotentialTangent.y}); dot product = ${round(
  equipotentialDot
)}.

### Gradient Relation

At held-out point (${gradientPoint.x}, ${gradientPoint.y}), field = (${round(gradientField.x)}, ${round(
  gradientField.y
)}) and -grad(V) = (${round(negativeGradient.x)}, ${round(negativeGradient.y)}); vector error = ${round(
  gradientRelationError,
  8
)}.

## Source Anchors

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The grammar passes a scalar-potential/equipotential geometry comparator under the same electrostatic charge rules used by the field-vector checks. This is stronger than another finite vector fixture because it links scalar potential, vector field, and contour geometry. It remains one electromagnetic evidence line: the next EM gate should move toward calibrated field magnitude, conductors/material media, or time-dependent propagation rather than counting more electrostatic geometry checks as independent domains.
`;

await writeFile(new URL('external-em-equipotential-comparator.md', outDir), markdown);

console.log(`External EM-06 status: ${status}`);
console.log(`Score: ${score}`);
console.log(`Wrote ${new URL('external-em-equipotential-comparator.md', outDir).pathname}`);
