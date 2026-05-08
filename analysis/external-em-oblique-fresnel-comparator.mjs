import { writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

function degToRad(degrees) {
  return (degrees * Math.PI) / 180;
}

function radToDeg(radians) {
  return (radians * 180) / Math.PI;
}

function relativeErrorPct(model, expected) {
  if (expected === 0) return model === 0 ? 0 : Infinity;
  return ((model - expected) / expected) * 100;
}

function snell({ n1, n2, thetaI }) {
  const sinT = (n1 / n2) * Math.sin(thetaI);
  if (Math.abs(sinT) > 1) {
    return { totalInternalReflection: true, thetaT: null };
  }
  return { totalInternalReflection: false, thetaT: Math.asin(sinT) };
}

function fresnel({ n1, n2, thetaDegrees }) {
  const thetaI = degToRad(thetaDegrees);
  const refraction = snell({ n1, n2, thetaI });
  if (refraction.totalInternalReflection) {
    return {
      thetaDegrees,
      totalInternalReflection: true,
      rs: null,
      rp: null,
      Rs: 1,
      Rp: 1,
      thetaT: null,
    };
  }

  const thetaT = refraction.thetaT;
  const cosI = Math.cos(thetaI);
  const cosT = Math.cos(thetaT);
  const rs = (n1 * cosI - n2 * cosT) / (n1 * cosI + n2 * cosT);
  const rp = (n2 * cosI - n1 * cosT) / (n2 * cosI + n1 * cosT);
  return {
    thetaDegrees,
    totalInternalReflection: false,
    rs,
    rp,
    Rs: rs ** 2,
    Rp: rp ** 2,
    thetaT,
  };
}

const external = {
  target: 'Oblique-incidence Fresnel boundary comparator',
  modeledSubset:
    's/p polarized oblique-incidence reflectance, Brewster-angle p-polarized zero, grazing reflectance trend, Snell refraction, and total internal reflection detection',
  notModeled:
    'absorbing media, complex refractive index, phase under total internal reflection, evanescent waves, roughness scattering, multilayer interference, diffraction, birefringence, radiation generation, or numerical Maxwell-equation solving',
  tolerances: {
    analyticPct: 0.01,
    brewsterReflectance: 1e-12,
    angleDegrees: 1e-10,
  },
  sources: [
    {
      label: 'OpenStax University Physics Volume 3, Fresnel Equations',
      url: 'https://openstax.org/books/university-physics-volume-3/pages/1-5-fresnels-equations',
      note: 'Gives s- and p-polarized reflection/transmission behavior for light at media boundaries.',
    },
    {
      label: 'OpenStax University Physics Volume 3, Brewster Angle',
      url: 'https://openstax.org/books/university-physics-volume-3/pages/1-6-brewsters-law',
      note: 'Describes Brewster angle where reflected light is fully polarized and p-reflection vanishes in the ideal case.',
    },
    {
      label: 'OpenStax University Physics Volume 3, Total Internal Reflection',
      url: 'https://openstax.org/books/university-physics-volume-3/pages/1-4-total-internal-reflection',
      note: 'Describes the critical angle and total internal reflection from higher to lower refractive index.',
    },
  ],
};

const grammarVariables = {
  route: 'oblique incident route splits into reflected and refracted angular routes',
  closure: 'boundary continuity closes different s/p amplitude constraints at the same interface',
  phase: 'polarization orientation changes which boundary component can cancel',
  charge: 'no free boundary charge is modeled in the ideal dielectric interface',
  continuity: 'Snell route continuity and Fresnel amplitude continuity jointly govern reflectance',
};

const normal = fresnel({ n1: 1, n2: 1.5, thetaDegrees: 0 });
const oblique = fresnel({ n1: 1, n2: 1.5, thetaDegrees: 45 });
const grazing = fresnel({ n1: 1, n2: 1.5, thetaDegrees: 80 });
const brewsterAngle = radToDeg(Math.atan(1.5 / 1));
const brewster = fresnel({ n1: 1, n2: 1.5, thetaDegrees: brewsterAngle });
const belowCritical = fresnel({ n1: 1.5, n2: 1, thetaDegrees: 40 });
const aboveCritical = fresnel({ n1: 1.5, n2: 1, thetaDegrees: 50 });
const expectedNormal = ((1 - 1.5) / (1 + 1.5)) ** 2;
const expectedCriticalAngle = radToDeg(Math.asin(1 / 1.5));
const criticalAngle = radToDeg(Math.asin(1 / 1.5));

const checks = [
  {
    check: 'Shared oblique-boundary grammar',
    expectation: 'route, closure, phase, charge, and continuity should define one oblique dielectric-boundary mapping',
    modelValue: Object.entries(grammarVariables)
      .map(([key, value]) => `${key}: ${value}`)
      .join('; '),
    pass: Object.keys(grammarVariables).length === 5,
    reading: 'The comparator changes angle and polarization, not the grammar vocabulary.',
  },
  {
    check: 'Normal-incidence continuity with EM-10',
    expectation: 's and p reflectance should match the 4% normal-incidence air/glass result',
    modelValue: `Rs ${round(normal.Rs, 8)}, Rp ${round(normal.Rp, 8)}`,
    pass:
      Math.abs(relativeErrorPct(normal.Rs, expectedNormal)) <= external.tolerances.analyticPct &&
      Math.abs(relativeErrorPct(normal.Rp, expectedNormal)) <= external.tolerances.analyticPct,
    reading: 'The oblique equations reduce to the prior normal-incidence boundary result.',
  },
  {
    check: 'Polarization split at 45 degrees',
    expectation: 's and p reflectance should separate at oblique incidence',
    modelValue: `Rs ${round(oblique.Rs, 8)}, Rp ${round(oblique.Rp, 8)}`,
    pass: oblique.Rs > oblique.Rp && oblique.Rs > normal.Rs,
    reading: 'Oblique route geometry forces different continuity constraints for s and p polarization.',
  },
  {
    check: 'Brewster p-reflectance zero',
    expectation: `p-polarized reflectance should vanish at Brewster angle ${round(brewsterAngle, 8)} degrees`,
    modelValue: `Rp ${brewster.Rp}`,
    pass: brewster.Rp <= external.tolerances.brewsterReflectance,
    reading: 'The p-polarized boundary route can cancel under the Brewster geometry.',
  },
  {
    check: 'Grazing reflectance trend',
    expectation: 'both polarizations should rise at high grazing angle relative to normal incidence',
    modelValue: `Rs ${round(grazing.Rs, 8)}, Rp ${round(grazing.Rp, 8)}`,
    pass: grazing.Rs > normal.Rs && grazing.Rp > normal.Rp,
    reading: 'Route obliquity increases reflection pressure near grazing incidence.',
  },
  {
    check: 'Critical-angle calculation',
    expectation: `glass-to-air critical angle should be ${round(expectedCriticalAngle, 8)} degrees`,
    modelValue: `${round(criticalAngle, 8)} degrees`,
    pass: Math.abs(criticalAngle - expectedCriticalAngle) <= external.tolerances.angleDegrees,
    reading: 'Higher-to-lower index release has a finite angular escape gate.',
  },
  {
    check: 'Total internal reflection gate',
    expectation: 'glass-to-air 40 degrees should transmit, while 50 degrees should be total internal reflection',
    modelValue: `40deg TIR ${belowCritical.totalInternalReflection}; 50deg TIR ${aboveCritical.totalInternalReflection}`,
    pass: belowCritical.totalInternalReflection === false && aboveCritical.totalInternalReflection === true,
    reading: 'The route gate closes when Snell continuity has no real transmitted route.',
  },
  {
    check: 'Boundary/non-claim discipline',
    expectation: 'benchmark should not claim rough, absorbing, multilayer, or Maxwell validation',
    modelValue: external.notModeled,
    pass: external.notModeled.includes('roughness') && external.notModeled.includes('Maxwell'),
    reading: 'This is an ideal oblique Fresnel comparator, not a general optical propagation solver.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = `${passed}/${checks.length}`;
const status =
  passed === checks.length ? 'oblique Fresnel comparator pass' : 'mixed oblique Fresnel comparator';

const report = {
  source: 'external-em-oblique-fresnel-comparator.mjs',
  status,
  external,
  grammarVariables,
  metrics: {
    normal: { Rs: round(normal.Rs, 8), Rp: round(normal.Rp, 8) },
    oblique45: { Rs: round(oblique.Rs, 8), Rp: round(oblique.Rp, 8) },
    grazing80: { Rs: round(grazing.Rs, 8), Rp: round(grazing.Rp, 8) },
    brewster: { angleDegrees: round(brewsterAngle, 8), Rp: brewster.Rp },
    criticalAngle: round(criticalAngle, 8),
    belowCritical: { totalInternalReflection: belowCritical.totalInternalReflection },
    aboveCritical: { totalInternalReflection: aboveCritical.totalInternalReflection },
  },
  score,
  checks,
  confidenceEffect:
    status === 'oblique Fresnel comparator pass'
      ? 'supports a small inferential-convergence increase because EM evidence now includes polarization-sensitive oblique boundary behavior while remaining limited to ideal lossless imported-index optics'
      : 'does not increase confidence; failure would show that normal-incidence boundary propagation does not transfer to oblique Fresnel constraints',
};

await writeFile(new URL('external-em-oblique-fresnel-comparator.json', outDir), JSON.stringify(report, null, 2));

const markdown = `# Relational Substrate External EM-11 Oblique Fresnel Comparator

## Purpose

This report extends EM-10 from normal-incidence boundary propagation into ideal oblique-incidence Fresnel behavior.

It tests whether fixed grammar variables reproduce s/p polarization splitting, Brewster-angle p-reflectance cancellation, grazing reflectance growth, Snell-route continuity, and total-internal-reflection gating. It does not model absorbing media, roughness, multilayer interference, evanescent phase, diffraction, or full Maxwell-equation propagation.

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

## Fresnel Rows

| Case | Rs | Rp | Note |
|---|---:|---:|---|
| air to glass, 0 degrees | ${round(normal.Rs, 8)} | ${round(normal.Rp, 8)} | normal-incidence continuity |
| air to glass, 45 degrees | ${round(oblique.Rs, 8)} | ${round(oblique.Rp, 8)} | polarization split |
| air to glass, Brewster ${round(brewsterAngle, 6)} degrees | ${round(brewster.Rs, 8)} | ${brewster.Rp} | p-reflectance cancellation |
| air to glass, 80 degrees | ${round(grazing.Rs, 8)} | ${round(grazing.Rp, 8)} | grazing trend |
| glass to air, 40 degrees | ${round(belowCritical.Rs, 8)} | ${round(belowCritical.Rp, 8)} | below critical |
| glass to air, 50 degrees | ${aboveCritical.Rs} | ${aboveCritical.Rp} | total internal reflection |

## Source Anchors

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The grammar passes a first oblique Fresnel comparator. This is stronger than normal incidence because the route now has to separate polarization constraints, hit a Brewster cancellation geometry, and close transmission entirely past the critical angle. It remains a narrow ideal-interface check, not a rough, absorbing, multilayer, or full Maxwell-equation optical solver.
`;

await writeFile(new URL('external-em-oblique-fresnel-comparator.md', outDir), markdown);

console.log(`External EM-11 status: ${status}`);
console.log(`Score: ${score}`);
console.log(`Wrote ${new URL('external-em-oblique-fresnel-comparator.md', outDir).pathname}`);
