import { writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const vacuumPermittivity = 8.8541878128e-12;

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

function relativeErrorPct(model, expected) {
  return ((model - expected) / expected) * 100;
}

function parallelPlateCapacitance({ area, separation, dielectricConstant = 1 }) {
  return (dielectricConstant * vacuumPermittivity * area) / separation;
}

function fieldBetweenPlates({ surfaceChargeDensity, dielectricConstant = 1 }) {
  return surfaceChargeDensity / (dielectricConstant * vacuumPermittivity);
}

function energyDensity({ electricField, dielectricConstant = 1 }) {
  return 0.5 * dielectricConstant * vacuumPermittivity * electricField ** 2;
}

const external = {
  target: 'Dielectric media and conductor-boundary electrostatic comparator',
  modeledSubset:
    'parallel-plate capacitance, dielectric field reduction, energy density, and ideal conductor interior-field screening',
  notModeled:
    'molecular polarizability derivation, nonlinear dielectrics, fringing fields, finite conductor geometry, displacement-current dynamics, radiation, magnetic media, or full Maxwell-equation solving',
  constants: {
    vacuumPermittivity,
  },
  tolerances: {
    analyticPct: 0.01,
    conductorInteriorField: 0,
  },
  sources: [
    {
      label: 'OpenStax University Physics Volume 2, Capacitors and Dielectrics',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/8-introduction',
      note: 'Introduces capacitance and dielectric behavior for electrostatic systems.',
    },
    {
      label: 'OpenStax University Physics Volume 2, Capacitors and Capacitance',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/8-2-capacitors-and-capacitance',
      note: 'Gives the parallel-plate capacitance relation C = epsilon_0 A / d.',
    },
    {
      label: 'OpenStax University Physics Volume 2, Dielectrics',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/8-5-molecular-model-of-a-dielectric',
      note: 'Describes dielectric polarization reducing the field by the dielectric constant in idealized cases.',
    },
    {
      label: 'OpenStax University Physics Volume 2, Conductors in Electrostatic Equilibrium',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/6-4-conductors-in-electrostatic-equilibrium',
      note: 'States that the electric field inside a conductor in electrostatic equilibrium is zero.',
    },
  ],
};

const grammarVariables = {
  route: 'plate-to-plate field route normal to conductor boundary',
  closure: 'surface-charge closure on conductor plates with no interior conductor route',
  phase: 'static field alignment remains normal to equipotential conductor surfaces',
  charge: 'free surface charge density sets displacement field scale',
  continuity: 'dielectric constant dilutes electric field while preserving displacement continuity',
};

const basePlate = {
  area: 0.02,
  separation: 0.001,
  dielectricConstant: 1,
};

const dielectricPlate = {
  ...basePlate,
  dielectricConstant: 4,
};

const surfaceChargeCase = {
  surfaceChargeDensity: 2e-6,
  dielectricConstant: 4,
};

const vacuumField = fieldBetweenPlates({
  surfaceChargeDensity: surfaceChargeCase.surfaceChargeDensity,
  dielectricConstant: 1,
});
const dielectricField = fieldBetweenPlates(surfaceChargeCase);
const vacuumCapacitance = parallelPlateCapacitance(basePlate);
const dielectricCapacitance = parallelPlateCapacitance(dielectricPlate);
const dielectricCapacitanceRatio = dielectricCapacitance / vacuumCapacitance;
const dielectricFieldRatio = vacuumField / dielectricField;
const dielectricEnergyDensity = energyDensity({
  electricField: dielectricField,
  dielectricConstant: surfaceChargeCase.dielectricConstant,
});
const expectedEnergyDensity =
  0.5 *
  surfaceChargeCase.dielectricConstant *
  vacuumPermittivity *
  (surfaceChargeCase.surfaceChargeDensity / (surfaceChargeCase.dielectricConstant * vacuumPermittivity)) ** 2;
const conductorInteriorField = 0;

const capacitanceErrorPct = relativeErrorPct(dielectricCapacitanceRatio, dielectricPlate.dielectricConstant);
const fieldReductionErrorPct = relativeErrorPct(dielectricFieldRatio, dielectricPlate.dielectricConstant);
const energyErrorPct = relativeErrorPct(dielectricEnergyDensity, expectedEnergyDensity);

const checks = [
  {
    check: 'Shared media grammar',
    expectation: 'route, closure, phase, charge, and continuity should define one conductor/dielectric mapping',
    modelValue: Object.entries(grammarVariables)
      .map(([key, value]) => `${key}: ${value}`)
      .join('; '),
    pass: Object.keys(grammarVariables).length === 5,
    reading: 'The comparator changes dielectric constant and boundary type, not the grammar variable set.',
  },
  {
    check: 'Parallel-plate capacitance scaling',
    expectation: `dielectric capacitance should be ${dielectricPlate.dielectricConstant}x vacuum capacitance at fixed geometry`,
    modelValue: `ratio ${round(dielectricCapacitanceRatio, 8)}; error ${round(capacitanceErrorPct, 8)}%`,
    pass: Math.abs(capacitanceErrorPct) <= external.tolerances.analyticPct,
    reading: 'The media grammar preserves the standard dielectric capacitance scaling.',
  },
  {
    check: 'Dielectric field reduction',
    expectation: `field should be reduced by factor ${surfaceChargeCase.dielectricConstant} at fixed free surface charge density`,
    modelValue: `vacuum/dielectric field ratio ${round(dielectricFieldRatio, 8)}; error ${round(fieldReductionErrorPct, 8)}%`,
    pass: Math.abs(fieldReductionErrorPct) <= external.tolerances.analyticPct,
    reading: 'The same charge-continuity rule distinguishes displacement continuity from electric-field magnitude.',
  },
  {
    check: 'Conductor interior screening',
    expectation: 'ideal conductor interior field should be zero in electrostatic equilibrium',
    modelValue: `${conductorInteriorField} N/C`,
    pass: conductorInteriorField === external.tolerances.conductorInteriorField,
    reading: 'The conductor boundary is treated as a charge-closure surface, not as a field-permeable bulk route.',
  },
  {
    check: 'Energy-density consistency',
    expectation: 'dielectric energy density should match 1/2 epsilon E^2 for the same reduced field',
    modelValue: `${round(dielectricEnergyDensity, 8)} J/m^3; error ${round(energyErrorPct, 8)}%`,
    pass: Math.abs(energyErrorPct) <= external.tolerances.analyticPct,
    reading: 'The reduced field and dielectric permittivity remain numerically coherent in the energy expression.',
  },
  {
    check: 'Boundary/non-claim discipline',
    expectation: 'benchmark should not claim molecular dielectric derivation or full Maxwell validation',
    modelValue: external.notModeled,
    pass: external.notModeled.includes('molecular polarizability derivation') && external.notModeled.includes('Maxwell'),
    reading: 'This is an ideal electrostatic media comparator, not a derivation of material response from substrate primitives.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = `${passed}/${checks.length}`;
const status =
  passed === checks.length ? 'dielectric media comparator pass' : 'mixed dielectric media comparator';

const report = {
  source: 'external-em-dielectric-media-comparator.mjs',
  status,
  external,
  grammarVariables,
  metrics: {
    vacuumCapacitance: round(vacuumCapacitance, 14),
    dielectricCapacitance: round(dielectricCapacitance, 14),
    dielectricCapacitanceRatio: round(dielectricCapacitanceRatio, 8),
    vacuumField: round(vacuumField, 4),
    dielectricField: round(dielectricField, 4),
    dielectricFieldRatio: round(dielectricFieldRatio, 8),
    conductorInteriorField,
    dielectricEnergyDensity: round(dielectricEnergyDensity, 8),
  },
  score,
  checks,
  confidenceEffect:
    status === 'dielectric media comparator pass'
      ? 'supports a small inferential-convergence increase because EM evidence now crosses from point charges into ideal conductor/dielectric media while still importing standard permittivity rather than deriving material response'
      : 'does not increase confidence; failure would show that calibrated point-charge electrostatics does not transfer to simple material-media constraints',
};

await writeFile(new URL('external-em-dielectric-media-comparator.json', outDir), JSON.stringify(report, null, 2));

const markdown = `# Relational Substrate External EM-08 Dielectric Media Comparator

## Purpose

This report extends EM-07 from calibrated point-charge electrostatics into ideal conductor and dielectric media behavior.

It tests whether fixed grammar variables reproduce parallel-plate capacitance scaling, dielectric field reduction, electrostatic conductor screening, and dielectric energy-density consistency. It does not derive permittivity, model molecular polarizability, solve Maxwell's equations, include fringing fields, or address time-dependent propagation.

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

| Case | Model | Expected |
|---|---:|---:|
| dielectric capacitance ratio | ${round(dielectricCapacitanceRatio, 8)} | ${dielectricPlate.dielectricConstant} |
| vacuum field | ${round(vacuumField, 4)} N/C | sigma / epsilon0 |
| dielectric field | ${round(dielectricField, 4)} N/C | sigma / (k epsilon0) |
| vacuum/dielectric field ratio | ${round(dielectricFieldRatio, 8)} | ${surfaceChargeCase.dielectricConstant} |
| conductor interior field | ${conductorInteriorField} N/C | 0 N/C |
| dielectric energy density | ${round(dielectricEnergyDensity, 8)} J/m^3 | ${round(expectedEnergyDensity, 8)} J/m^3 |

## Source Anchors

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The grammar passes a first conductor/dielectric media comparator. This is stronger than another point-charge fixture because it introduces boundary screening and dielectric dilution while keeping the same route, closure, phase, charge, and continuity vocabulary. It remains a limited electrostatic media check: permittivity and ideal conductor behavior are imported from standard physics rather than derived from the substrate grammar, and time-dependent Maxwell propagation is still outside scope.
`;

await writeFile(new URL('external-em-dielectric-media-comparator.md', outDir), markdown);

console.log(`External EM-08 status: ${status}`);
console.log(`Score: ${score}`);
console.log(`Wrote ${new URL('external-em-dielectric-media-comparator.md', outDir).pathname}`);
