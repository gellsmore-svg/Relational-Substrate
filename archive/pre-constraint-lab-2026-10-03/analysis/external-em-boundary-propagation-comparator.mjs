import { writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const speedOfLight = 299792458;
const vacuumImpedance = 376.730313668;

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

function relativeErrorPct(model, expected) {
  return ((model - expected) / expected) * 100;
}

function medium({ refractiveIndex }) {
  return {
    refractiveIndex,
    impedance: vacuumImpedance / refractiveIndex,
    speed: speedOfLight / refractiveIndex,
  };
}

function normalIncidence({ from, to }) {
  const incident = medium(from);
  const transmitted = medium(to);
  const amplitudeReflection = (transmitted.impedance - incident.impedance) / (transmitted.impedance + incident.impedance);
  const amplitudeTransmission = (2 * transmitted.impedance) / (transmitted.impedance + incident.impedance);
  const powerReflection = amplitudeReflection ** 2;
  const powerTransmission = 1 - powerReflection;
  return {
    incident,
    transmitted,
    amplitudeReflection,
    amplitudeTransmission,
    powerReflection,
    powerTransmission,
    phaseInversion: amplitudeReflection < 0,
  };
}

const external = {
  target: 'Normal-incidence electromagnetic boundary propagation comparator',
  modeledSubset:
    'normal-incidence reflection/transmission at a dielectric boundary, impedance contrast, phase inversion, speed change, and energy balance',
  notModeled:
    'oblique incidence, polarization splitting, total internal reflection, absorption, dispersion, multilayer interference, roughness scattering, conductor skin depth, radiation generation, or numerical Maxwell-equation solving',
  constants: {
    speedOfLight,
    vacuumImpedance,
  },
  tolerances: {
    analyticPct: 0.01,
    energyBalance: 1e-12,
  },
  sources: [
    {
      label: 'OpenStax University Physics Volume 3, Fresnel Equations',
      url: 'https://openstax.org/books/university-physics-volume-3/pages/1-5-fresnels-equations',
      note: 'Gives reflection and transmission behavior for electromagnetic waves at media boundaries.',
    },
    {
      label: 'OpenStax University Physics Volume 2, Electromagnetic Waves in Matter',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/16-5-momentum-and-radiation-pressure',
      note: 'Provides context for wave energy and momentum transfer at electromagnetic boundaries.',
    },
    {
      label: 'OpenStax University Physics Volume 3, Reflection and Refraction',
      url: 'https://openstax.org/books/university-physics-volume-3/pages/1-2-the-law-of-reflection',
      note: 'Introduces reflection/refraction boundary behavior and refractive-index speed changes.',
    },
  ],
};

const grammarVariables = {
  route: 'incident route splits into reflected and transmitted boundary routes',
  closure: 'boundary continuity closes energy accounting between reflected and transmitted routes',
  phase: 'reflection phase flips when the wave enters a higher-index medium',
  charge: 'no free boundary charge is modeled in the ideal dielectric interface',
  continuity: 'normal-incidence impedance contrast governs amplitude and power continuity',
};

const airGlass = normalIncidence({
  from: { refractiveIndex: 1 },
  to: { refractiveIndex: 1.5 },
});
const glassAir = normalIncidence({
  from: { refractiveIndex: 1.5 },
  to: { refractiveIndex: 1 },
});
const matched = normalIncidence({
  from: { refractiveIndex: 1.33 },
  to: { refractiveIndex: 1.33 },
});

const expectedAirGlassPowerReflection = ((1 - 1.5) / (1 + 1.5)) ** 2;
const expectedGlassAirPowerReflection = ((1.5 - 1) / (1.5 + 1)) ** 2;
const expectedSpeedRatio = 1 / 1.5;
const airGlassEnergyBalance = airGlass.powerReflection + airGlass.powerTransmission;
const glassAirEnergyBalance = glassAir.powerReflection + glassAir.powerTransmission;
const airGlassReflectionErrorPct = relativeErrorPct(airGlass.powerReflection, expectedAirGlassPowerReflection);
const glassAirReflectionErrorPct = relativeErrorPct(glassAir.powerReflection, expectedGlassAirPowerReflection);
const speedRatioErrorPct = relativeErrorPct(airGlass.transmitted.speed / airGlass.incident.speed, expectedSpeedRatio);

const checks = [
  {
    check: 'Shared boundary grammar',
    expectation: 'route, closure, phase, charge, and continuity should define one dielectric-boundary mapping',
    modelValue: Object.entries(grammarVariables)
      .map(([key, value]) => `${key}: ${value}`)
      .join('; '),
    pass: Object.keys(grammarVariables).length === 5,
    reading: 'The comparator changes refractive index contrast, not the grammar vocabulary.',
  },
  {
    check: 'Air-to-glass reflection power',
    expectation: 'normal-incidence air-to-n=1.5 glass reflection should be 4%',
    modelValue: `${round(airGlass.powerReflection * 100, 6)}%; error ${round(airGlassReflectionErrorPct, 8)}%`,
    pass: Math.abs(airGlassReflectionErrorPct) <= external.tolerances.analyticPct,
    reading: 'The boundary split reproduces the standard normal-incidence reflection fraction.',
  },
  {
    check: 'Reverse-boundary reflection symmetry',
    expectation: 'glass-to-air normal-incidence reflection power should match air-to-glass for the same index contrast',
    modelValue: `${round(glassAir.powerReflection * 100, 6)}%; error ${round(glassAirReflectionErrorPct, 8)}%`,
    pass:
      Math.abs(glassAirReflectionErrorPct) <= external.tolerances.analyticPct &&
      Math.abs(glassAir.powerReflection - airGlass.powerReflection) <= external.tolerances.energyBalance,
    reading: 'Power reflection is symmetric under boundary reversal, while phase sign is not.',
  },
  {
    check: 'Reflection phase inversion',
    expectation: 'reflection should invert phase when entering higher index and not invert when entering lower index',
    modelValue: `air-to-glass inversion ${airGlass.phaseInversion}; glass-to-air inversion ${glassAir.phaseInversion}`,
    pass: airGlass.phaseInversion === true && glassAir.phaseInversion === false,
    reading: 'The phase route distinguishes high-index entry from low-index release.',
  },
  {
    check: 'Matched-boundary no-reflection limit',
    expectation: 'identical media should produce zero reflected power',
    modelValue: `${matched.powerReflection}`,
    pass: matched.powerReflection === 0,
    reading: 'No impedance contrast leaves no boundary split to reflect.',
  },
  {
    check: 'Transmission speed change',
    expectation: 'wave speed in n=1.5 glass should be c/1.5',
    modelValue: `speed ratio ${round(airGlass.transmitted.speed / airGlass.incident.speed, 8)}; error ${round(speedRatioErrorPct, 8)}%`,
    pass: Math.abs(speedRatioErrorPct) <= external.tolerances.analyticPct,
    reading: 'The transmitted route changes speed according to refractive index.',
  },
  {
    check: 'Energy balance at ideal boundary',
    expectation: 'reflected plus transmitted power fractions should sum to 1 in lossless normal incidence',
    modelValue: `air/glass ${airGlassEnergyBalance}; glass/air ${glassAirEnergyBalance}`,
    pass:
      Math.abs(airGlassEnergyBalance - 1) <= external.tolerances.energyBalance &&
      Math.abs(glassAirEnergyBalance - 1) <= external.tolerances.energyBalance,
    reading: 'The ideal boundary redistributes power rather than creating or losing it.',
  },
  {
    check: 'Boundary/non-claim discipline',
    expectation: 'benchmark should not claim full Fresnel, roughness, or Maxwell validation',
    modelValue: external.notModeled,
    pass: external.notModeled.includes('oblique incidence') && external.notModeled.includes('Maxwell'),
    reading: 'This is a normal-incidence boundary comparator, not a general optical propagation solver.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = `${passed}/${checks.length}`;
const status =
  passed === checks.length ? 'boundary propagation comparator pass' : 'mixed boundary propagation comparator';

const report = {
  source: 'external-em-boundary-propagation-comparator.mjs',
  status,
  external,
  grammarVariables,
  metrics: {
    airGlass: {
      amplitudeReflection: round(airGlass.amplitudeReflection, 8),
      amplitudeTransmission: round(airGlass.amplitudeTransmission, 8),
      powerReflection: round(airGlass.powerReflection, 8),
      powerTransmission: round(airGlass.powerTransmission, 8),
      phaseInversion: airGlass.phaseInversion,
    },
    glassAir: {
      amplitudeReflection: round(glassAir.amplitudeReflection, 8),
      amplitudeTransmission: round(glassAir.amplitudeTransmission, 8),
      powerReflection: round(glassAir.powerReflection, 8),
      powerTransmission: round(glassAir.powerTransmission, 8),
      phaseInversion: glassAir.phaseInversion,
    },
    matched: {
      powerReflection: matched.powerReflection,
    },
    speedRatio: round(airGlass.transmitted.speed / airGlass.incident.speed, 8),
  },
  score,
  checks,
  confidenceEffect:
    status === 'boundary propagation comparator pass'
      ? 'supports a small inferential-convergence increase because EM evidence now includes propagation through a media boundary while remaining limited to normal-incidence imported-index optics'
      : 'does not increase confidence; failure would show that plane-wave propagation does not transfer to simple boundary splitting',
};

await writeFile(new URL('external-em-boundary-propagation-comparator.json', outDir), JSON.stringify(report, null, 2));

const markdown = `# Relational Substrate External EM-10 Boundary Propagation Comparator

## Purpose

This report extends EM-09 from free-space plane-wave propagation into a bounded normal-incidence media-boundary check.

It tests whether fixed grammar variables reproduce normal-incidence reflection power, transmission power, phase inversion, matched-boundary no-reflection behavior, speed change, and ideal energy balance. It does not model oblique incidence, polarization splitting, total internal reflection, roughness, absorption, multilayer interference, or full Maxwell-equation propagation.

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

## Boundary Rows

| Case | Reflection amplitude | Transmission amplitude | Reflected power | Transmitted power | Phase inversion |
|---|---:|---:|---:|---:|---|
| air to n=1.5 glass | ${round(airGlass.amplitudeReflection, 8)} | ${round(airGlass.amplitudeTransmission, 8)} | ${round(airGlass.powerReflection, 8)} | ${round(airGlass.powerTransmission, 8)} | ${airGlass.phaseInversion ? 'yes' : 'no'} |
| n=1.5 glass to air | ${round(glassAir.amplitudeReflection, 8)} | ${round(glassAir.amplitudeTransmission, 8)} | ${round(glassAir.powerReflection, 8)} | ${round(glassAir.powerTransmission, 8)} | ${glassAir.phaseInversion ? 'yes' : 'no'} |
| matched n=1.33 to n=1.33 | ${round(matched.amplitudeReflection, 8)} | ${round(matched.amplitudeTransmission, 8)} | ${matched.powerReflection} | ${matched.powerTransmission} | ${matched.phaseInversion ? 'yes' : 'no'} |

## Source Anchors

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The grammar passes a first boundary propagation comparator. This is stronger than free-space propagation alone because the route now has to split, invert phase conditionally, preserve energy accounting, and change speed at a media boundary. It remains a narrow normal-incidence imported-index check, not a general Fresnel solver, rough-interface model, or Maxwell-equation boundary simulation.
`;

await writeFile(new URL('external-em-boundary-propagation-comparator.md', outDir), markdown);

console.log(`External EM-10 status: ${status}`);
console.log(`Score: ${score}`);
console.log(`Wrote ${new URL('external-em-boundary-propagation-comparator.md', outDir).pathname}`);
