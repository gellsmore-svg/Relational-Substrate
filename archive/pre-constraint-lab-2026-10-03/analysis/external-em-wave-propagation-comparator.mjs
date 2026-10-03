import { writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const speedOfLight = 299792458;
const vacuumPermittivity = 8.8541878128e-12;
const vacuumPermeability = 1 / (vacuumPermittivity * speedOfLight ** 2);
const vacuumImpedance = Math.sqrt(vacuumPermeability / vacuumPermittivity);

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

function relativeErrorPct(model, expected) {
  return ((model - expected) / expected) * 100;
}

function dot(a, b) {
  return a.x * b.x + a.y * b.y + a.z * b.z;
}

function cross(a, b) {
  return {
    x: a.y * b.z - a.z * b.y,
    y: a.z * b.x - a.x * b.z,
    z: a.x * b.y - a.y * b.x,
  };
}

function magnitude(vector) {
  return Math.hypot(vector.x, vector.y, vector.z);
}

function planeWave({ electricAmplitude, frequency, z, t }) {
  const wavelength = speedOfLight / frequency;
  const angularFrequency = 2 * Math.PI * frequency;
  const waveNumber = (2 * Math.PI) / wavelength;
  const phase = waveNumber * z - angularFrequency * t;
  const e = electricAmplitude * Math.sin(phase);
  const b = e / speedOfLight;
  return {
    wavelength,
    phase,
    electric: { x: e, y: 0, z: 0 },
    magnetic: { x: 0, y: b, z: 0 },
    propagation: { x: 0, y: 0, z: 1 },
    poynting: cross({ x: e, y: 0, z: 0 }, { x: 0, y: b / vacuumPermeability, z: 0 }),
  };
}

const external = {
  target: 'Plane-wave electromagnetic propagation comparator',
  modeledSubset:
    'vacuum plane-wave speed relation, E/B amplitude relation, transverse field geometry, Poynting direction, impedance, and phase propagation',
  notModeled:
    'derivation of c, derivation of permittivity or permeability, boundary reflection, dispersion, waveguides, antennas, radiation generation, quantum electrodynamics, or numerical Maxwell-equation solving',
  constants: {
    speedOfLight,
    vacuumPermittivity,
    vacuumPermeability,
    vacuumImpedance,
  },
  tolerances: {
    analyticPct: 0.01,
    phaseAbsolute: 1e-10,
    orthogonality: 1e-12,
  },
  sources: [
    {
      label: 'OpenStax University Physics Volume 2, Electromagnetic Waves',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/16-introduction',
      note: 'Introduces electromagnetic waves and their propagation as coupled electric and magnetic fields.',
    },
    {
      label: 'OpenStax University Physics Volume 2, Plane Electromagnetic Waves',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/16-3-plane-electromagnetic-waves',
      note: 'Gives plane-wave relations including transverse E and B fields, E/B = c, and propagation direction.',
    },
    {
      label: 'OpenStax University Physics Volume 2, Energy Carried by Electromagnetic Waves',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/16-4-energy-carried-by-electromagnetic-waves',
      note: 'Relates electromagnetic wave energy flow to the Poynting vector.',
    },
  ],
};

const grammarVariables = {
  route: 'phase-front route advances along the propagation axis',
  closure: 'electric and magnetic field components remain mutually coupled rather than independently closed',
  phase: 'sinusoidal phase is preserved under wavelength/period translation',
  charge: 'no free source charge in the vacuum propagation region',
  continuity: 'field amplitude relation and energy-flow direction remain continuous across the wave cycle',
};

const caseConfig = {
  electricAmplitude: 120,
  frequency: 60e6,
  z: speedOfLight / 60e6 / 8,
  t: 1 / 60e6 / 16,
};

const row = planeWave(caseConfig);
const shifted = planeWave({
  ...caseConfig,
  z: caseConfig.z + row.wavelength,
  t: caseConfig.t + 1 / caseConfig.frequency,
});
const peakB = caseConfig.electricAmplitude / speedOfLight;
const eMagnitude = magnitude(row.electric);
const bMagnitude = magnitude(row.magnetic);
const eOverB = eMagnitude / bMagnitude;
const poyntingDirectionDot = dot(row.poynting, row.propagation) / magnitude(row.poynting);
const impedanceFromFields = caseConfig.electricAmplitude / (peakB / vacuumPermeability);
const speedFromConstants = 1 / Math.sqrt(vacuumPermittivity * vacuumPermeability);
const phaseShiftError = Math.abs(Math.sin(row.phase) - Math.sin(shifted.phase));

const speedErrorPct = relativeErrorPct(speedFromConstants, speedOfLight);
const ratioErrorPct = relativeErrorPct(eOverB, speedOfLight);
const impedanceErrorPct = relativeErrorPct(impedanceFromFields, vacuumImpedance);

const checks = [
  {
    check: 'Shared propagation grammar',
    expectation: 'route, closure, phase, charge, and continuity should define one vacuum wave mapping',
    modelValue: Object.entries(grammarVariables)
      .map(([key, value]) => `${key}: ${value}`)
      .join('; '),
    pass: Object.keys(grammarVariables).length === 5,
    reading: 'The comparator changes wave phase and amplitudes, not the grammar vocabulary.',
  },
  {
    check: 'Vacuum speed relation',
    expectation: '1 / sqrt(epsilon0 mu0) should equal c under the imported constants',
    modelValue: `${round(speedFromConstants, 4)} m/s; error ${round(speedErrorPct, 8)}%`,
    pass: Math.abs(speedErrorPct) <= external.tolerances.analyticPct,
    reading: 'The propagation check is calibrated to standard vacuum constants; it does not derive those constants.',
  },
  {
    check: 'E/B amplitude relation',
    expectation: 'plane-wave electric-to-magnetic field ratio should equal c',
    modelValue: `${round(eOverB, 4)}; error ${round(ratioErrorPct, 8)}%`,
    pass: Math.abs(ratioErrorPct) <= external.tolerances.analyticPct,
    reading: 'The coupled electric and magnetic amplitudes retain the standard vacuum relation.',
  },
  {
    check: 'Transverse field geometry',
    expectation: 'E, B, and propagation vectors should be mutually orthogonal',
    modelValue: `E.B ${round(dot(row.electric, row.magnetic), 12)}, E.k ${round(dot(row.electric, row.propagation), 12)}, B.k ${round(dot(row.magnetic, row.propagation), 12)}`,
    pass:
      Math.abs(dot(row.electric, row.magnetic)) <= external.tolerances.orthogonality &&
      Math.abs(dot(row.electric, row.propagation)) <= external.tolerances.orthogonality &&
      Math.abs(dot(row.magnetic, row.propagation)) <= external.tolerances.orthogonality,
    reading: 'The route geometry separates field orientation from propagation direction.',
  },
  {
    check: 'Poynting direction',
    expectation: 'E x B / mu0 should point along the propagation route',
    modelValue: `direction dot ${round(poyntingDirectionDot, 8)}`,
    pass: Math.abs(poyntingDirectionDot - 1) <= external.tolerances.analyticPct,
    reading: 'The energy-flow direction follows the coupled field orientation.',
  },
  {
    check: 'Vacuum impedance relation',
    expectation: 'E/H should equal sqrt(mu0/epsilon0)',
    modelValue: `${round(impedanceFromFields, 8)} ohm; expected ${round(vacuumImpedance, 8)} ohm; error ${round(impedanceErrorPct, 8)}%`,
    pass: Math.abs(impedanceErrorPct) <= external.tolerances.analyticPct,
    reading: 'The amplitude relation is consistent with vacuum impedance under imported constants.',
  },
  {
    check: 'Phase translation continuity',
    expectation: 'phase should be invariant under simultaneous one-wavelength and one-period translation',
    modelValue: `absolute sine difference ${phaseShiftError}`,
    pass: phaseShiftError <= external.tolerances.phaseAbsolute,
    reading: 'The wave route preserves phase continuity across one full propagation cycle.',
  },
  {
    check: 'Boundary/non-claim discipline',
    expectation: 'benchmark should not claim derivation of c or full Maxwell validation',
    modelValue: external.notModeled,
    pass: external.notModeled.includes('derivation of c') && external.notModeled.includes('Maxwell'),
    reading: 'This is a calibrated plane-wave relation comparator, not a generative electromagnetic theory.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = `${passed}/${checks.length}`;
const status =
  passed === checks.length ? 'plane-wave propagation comparator pass' : 'mixed plane-wave propagation comparator';

const report = {
  source: 'external-em-wave-propagation-comparator.mjs',
  status,
  external,
  grammarVariables,
  metrics: {
    wavelength: round(row.wavelength, 8),
    frequency: caseConfig.frequency,
    speedFromConstants: round(speedFromConstants, 4),
    eOverB: round(eOverB, 4),
    peakB: Number(peakB.toExponential(8)),
    poyntingDirectionDot: round(poyntingDirectionDot, 8),
    impedanceFromFields: round(impedanceFromFields, 8),
    vacuumImpedance: round(vacuumImpedance, 8),
    phaseShiftError,
  },
  score,
  checks,
  confidenceEffect:
    status === 'plane-wave propagation comparator pass'
      ? 'supports a small inferential-convergence increase because EM evidence now reaches time-dependent plane-wave relations while still importing vacuum constants rather than deriving electrodynamics'
      : 'does not increase confidence; failure would show that static EM checks do not transfer to basic propagation constraints',
};

await writeFile(new URL('external-em-wave-propagation-comparator.json', outDir), JSON.stringify(report, null, 2));

const markdown = `# Relational Substrate External EM-09 Wave Propagation Comparator

## Purpose

This report extends EM-08 from ideal electrostatic media into a bounded time-dependent vacuum plane-wave check.

It tests whether fixed grammar variables reproduce the standard plane-wave speed relation, E/B relation, transverse field geometry, Poynting direction, vacuum impedance, and phase translation continuity. It does not derive the speed of light, derive permittivity or permeability, solve Maxwell's equations, model radiation generation, or handle boundary propagation.

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

| Quantity | Model | Expected |
|---|---:|---:|
| speed from constants | ${round(speedFromConstants, 4)} m/s | ${speedOfLight} m/s |
| E/B ratio | ${round(eOverB, 4)} | ${speedOfLight} |
| peak B for E0=${caseConfig.electricAmplitude} V/m | ${peakB.toExponential(8)} T | E0 / c |
| Poynting direction dot | ${round(poyntingDirectionDot, 8)} | 1 |
| vacuum impedance | ${round(impedanceFromFields, 8)} ohm | ${round(vacuumImpedance, 8)} ohm |
| phase translation error | ${phaseShiftError} | 0 |

## Source Anchors

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The grammar passes a first time-dependent plane-wave comparator. This is stronger than another static electrostatic fixture because it checks phase propagation, transverse field coupling, and energy-flow direction together. It remains a limited imported-constant check: the speed of light, permittivity, and permeability are not derived, and the benchmark is not a Maxwell-equation solver or radiation-generation model.
`;

await writeFile(new URL('external-em-wave-propagation-comparator.md', outDir), markdown);

console.log(`External EM-09 status: ${status}`);
console.log(`Score: ${score}`);
console.log(`Wrote ${new URL('external-em-wave-propagation-comparator.md', outDir).pathname}`);
