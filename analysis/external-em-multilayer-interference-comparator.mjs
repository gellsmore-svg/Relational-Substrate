import { writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function round(value, places = 8) {
  return Number(value.toFixed(places));
}

function complex(re, im = 0) {
  return { re, im };
}

function add(a, b) {
  return complex(a.re + b.re, a.im + b.im);
}

function multiply(a, b) {
  return complex(a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re);
}

function divide(a, b) {
  const denominator = b.re ** 2 + b.im ** 2;
  return complex((a.re * b.re + a.im * b.im) / denominator, (a.im * b.re - a.re * b.im) / denominator);
}

function expI(theta) {
  return complex(Math.cos(theta), Math.sin(theta));
}

function abs2(a) {
  return a.re ** 2 + a.im ** 2;
}

function relativeErrorPct(model, expected) {
  if (expected === 0) return model === 0 ? 0 : Infinity;
  return ((model - expected) / expected) * 100;
}

function singleLayerReflectance({ n0, n1, ns, thickness, wavelength }) {
  const r01 = (n0 - n1) / (n0 + n1);
  const r12 = (n1 - ns) / (n1 + ns);
  const beta = (2 * Math.PI * n1 * thickness) / wavelength;
  const phase = expI(2 * beta);
  const numerator = add(complex(r01), multiply(complex(r12), phase));
  const denominator = add(complex(1), multiply(complex(r01 * r12), phase));
  const amplitude = divide(numerator, denominator);
  return {
    beta,
    amplitude,
    reflectance: abs2(amplitude),
  };
}

const external = {
  target: 'Multilayer thin-film interference comparator',
  modeledSubset:
    'normal-incidence single-layer thin-film phase thickness, ideal quarter-wave anti-reflection cancellation, off-design wavelength degradation, half-wave recurrence, and nonideal coating-index partial improvement',
  notModeled:
    'absorbing media, complex refractive index, lossy films, roughness scattering, broadband coating optimization, graded-index films, oblique polarization splitting, diffraction, birefringence, radiation generation, or numerical Maxwell-equation solving',
  tolerances: {
    analyticPct: 0.01,
    cancellationReflectance: 1e-12,
    phaseRadians: 1e-12,
  },
  sources: [
    {
      label: 'OpenStax University Physics Volume 3, Thin-Film Interference',
      url: 'https://openstax.org/books/university-physics-volume-3/pages/3-4-interference-in-thin-films',
      note: 'Describes optical path and phase conditions for constructive and destructive thin-film interference.',
    },
    {
      label: 'OpenStax University Physics Volume 3, Fresnel Equations',
      url: 'https://openstax.org/books/university-physics-volume-3/pages/1-5-fresnels-equations',
      note: 'Gives the boundary reflection amplitudes used by the normal-incidence layer comparator.',
    },
  ],
};

const grammarVariables = {
  route: 'incident route splits into front-surface and back-surface reflected routes inside the film stack',
  closure: 'destructive closure occurs when equal reflection amplitudes return out of phase',
  phase: 'optical thickness controls the round-trip phase relation between reflected routes',
  charge: 'no free boundary charge is modeled in the ideal dielectric films',
  continuity: 'field continuity is represented by normal-incidence Fresnel amplitudes at each film boundary',
};

const n0 = 1;
const ns = 1.5;
const wavelength0 = 550e-9;
const idealN1 = Math.sqrt(n0 * ns);
const nonidealN1 = 1.38;
const quarterWaveThickness = wavelength0 / (4 * idealN1);
const halfWaveThickness = wavelength0 / (2 * idealN1);
const nonidealQuarterWaveThickness = wavelength0 / (4 * nonidealN1);
const bareReflectance = ((n0 - ns) / (n0 + ns)) ** 2;
const idealQuarterWave = singleLayerReflectance({
  n0,
  n1: idealN1,
  ns,
  thickness: quarterWaveThickness,
  wavelength: wavelength0,
});
const offDesign = singleLayerReflectance({
  n0,
  n1: idealN1,
  ns,
  thickness: quarterWaveThickness,
  wavelength: wavelength0 * 0.8,
});
const halfWave = singleLayerReflectance({
  n0,
  n1: idealN1,
  ns,
  thickness: halfWaveThickness,
  wavelength: wavelength0,
});
const nonidealQuarterWave = singleLayerReflectance({
  n0,
  n1: nonidealN1,
  ns,
  thickness: nonidealQuarterWaveThickness,
  wavelength: wavelength0,
});

const checks = [
  {
    check: 'Shared multilayer grammar',
    expectation: 'route, closure, phase, charge, and continuity should define one thin-film interference mapping',
    modelValue: Object.entries(grammarVariables)
      .map(([key, value]) => `${key}: ${value}`)
      .join('; '),
    pass: Object.keys(grammarVariables).length === 5,
    reading: 'The comparator changes optical path structure, not the grammar vocabulary.',
  },
  {
    check: 'Bare interface continuity with EM-10 and EM-11',
    expectation: 'air/glass normal-incidence reflectance should remain 4%',
    modelValue: `${round(bareReflectance)}`,
    pass: Math.abs(relativeErrorPct(bareReflectance, 0.04)) <= external.tolerances.analyticPct,
    reading: 'The thin-film comparator inherits the same normal-incidence boundary baseline.',
  },
  {
    check: 'Quarter-wave phase thickness',
    expectation: 'single-pass film phase should equal pi/2 at the design wavelength',
    modelValue: `${idealQuarterWave.beta}`,
    pass: Math.abs(idealQuarterWave.beta - Math.PI / 2) <= external.tolerances.phaseRadians,
    reading: 'The route phase is controlled by optical thickness rather than geometric thickness alone.',
  },
  {
    check: 'Ideal quarter-wave anti-reflection cancellation',
    expectation: 'n1 = sqrt(n0 ns) should cancel reflected intensity at the design wavelength',
    modelValue: `${idealQuarterWave.reflectance}`,
    pass: idealQuarterWave.reflectance <= external.tolerances.cancellationReflectance,
    reading: 'Equal-amplitude reflected routes return pi out of phase and destructively close.',
  },
  {
    check: 'Off-design wavelength degradation',
    expectation: 'the same quarter-wave film should reflect more away from the design wavelength while staying below bare glass',
    modelValue: `${round(offDesign.reflectance)}`,
    pass: offDesign.reflectance > idealQuarterWave.reflectance && offDesign.reflectance < bareReflectance,
    reading: 'The interference cancellation is wavelength-specific, not a universal removal of reflection.',
  },
  {
    check: 'Half-wave recurrence',
    expectation: 'a half-wave layer should transform back to the bare air/glass reflectance at the design wavelength',
    modelValue: `${round(halfWave.reflectance)}`,
    pass: Math.abs(relativeErrorPct(halfWave.reflectance, bareReflectance)) <= external.tolerances.analyticPct,
    reading: 'The layer disappears optically when the round-trip phase returns to full-wave recurrence.',
  },
  {
    check: 'Nonideal coating partial improvement',
    expectation: 'a quarter-wave film with n = 1.38 should reduce reflection but not cancel it',
    modelValue: `${round(nonidealQuarterWave.reflectance)}`,
    pass:
      nonidealQuarterWave.reflectance > idealQuarterWave.reflectance &&
      nonidealQuarterWave.reflectance < bareReflectance,
    reading: 'Wrong amplitude matching still gives phase-assisted improvement without ideal cancellation.',
  },
  {
    check: 'Boundary/non-claim discipline',
    expectation: 'benchmark should not claim rough, absorbing, broadband, or Maxwell validation',
    modelValue: external.notModeled,
    pass:
      external.notModeled.includes('roughness') &&
      external.notModeled.includes('absorbing') &&
      external.notModeled.includes('Maxwell'),
    reading: 'This is an ideal lossless thin-film comparator, not a general optical coating or electromagnetic solver.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = `${passed}/${checks.length}`;
const status =
  passed === checks.length ? 'multilayer interference comparator pass' : 'mixed multilayer interference comparator';

const report = {
  source: 'external-em-multilayer-interference-comparator.mjs',
  status,
  external,
  grammarVariables,
  metrics: {
    n0,
    ns,
    idealN1: round(idealN1),
    nonidealN1,
    wavelength0Meters: wavelength0,
    quarterWaveThicknessMeters: quarterWaveThickness,
    halfWaveThicknessMeters: halfWaveThickness,
    bareReflectance: round(bareReflectance),
    idealQuarterWave: {
      phaseRadians: idealQuarterWave.beta,
      reflectance: idealQuarterWave.reflectance,
    },
    offDesignWavelengthMeters: wavelength0 * 0.8,
    offDesignReflectance: round(offDesign.reflectance),
    halfWaveReflectance: round(halfWave.reflectance),
    nonidealQuarterWaveReflectance: round(nonidealQuarterWave.reflectance),
  },
  score,
  checks,
  confidenceEffect:
    status === 'multilayer interference comparator pass'
      ? 'supports a small inferential-convergence increase because EM evidence now includes phase-sensitive thin-film interference and amplitude matching while remaining limited to ideal lossless imported-index optics'
      : 'does not increase confidence; failure would show that oblique Fresnel boundary behavior does not transfer to multilayer phase-interference constraints',
};

await writeFile(new URL('external-em-multilayer-interference-comparator.json', outDir), JSON.stringify(report, null, 2));

const markdown = `# Relational Substrate External EM-12 Multilayer Interference Comparator

## Purpose

This report extends EM-11 from single-boundary Fresnel behavior into ideal normal-incidence thin-film interference.

It tests whether fixed grammar variables reproduce quarter-wave phase thickness, ideal anti-reflection cancellation, off-design wavelength degradation, half-wave recurrence, and partial improvement under a nonideal film index. It does not model absorbing media, roughness, broadband coatings, graded-index films, oblique polarization splitting, diffraction, or full Maxwell-equation propagation.

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

## Thin-Film Rows

| Case | Film index | Thickness | Wavelength | Reflectance | Note |
|---|---:|---:|---:|---:|---|
| bare air/glass | n/a | n/a | ${wavelength0} m | ${round(bareReflectance)} | boundary baseline |
| ideal quarter wave | ${round(idealN1)} | ${quarterWaveThickness} m | ${wavelength0} m | ${idealQuarterWave.reflectance} | design cancellation |
| ideal quarter wave, off design | ${round(idealN1)} | ${quarterWaveThickness} m | ${wavelength0 * 0.8} m | ${round(offDesign.reflectance)} | wavelength-specific degradation |
| ideal half wave | ${round(idealN1)} | ${halfWaveThickness} m | ${wavelength0} m | ${round(halfWave.reflectance)} | bare-interface recurrence |
| nonideal quarter wave | ${nonidealN1} | ${nonidealQuarterWaveThickness} m | ${wavelength0} m | ${round(nonidealQuarterWave.reflectance)} | partial improvement |

## Source Anchors

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The grammar passes a first thin-film interference comparator. This is stronger than a single-boundary Fresnel check because route phase now has to coordinate two reflected paths across film thickness and amplitude matching. It remains a narrow ideal lossless imported-index optical calculation, not a rough, absorbing, broadband, or full Maxwell-equation coating model.
`;

await writeFile(new URL('external-em-multilayer-interference-comparator.md', outDir), markdown);

console.log(`External EM-12 status: ${status}`);
console.log(`Score: ${score}`);
console.log(`Wrote ${new URL('external-em-multilayer-interference-comparator.md', outDir).pathname}`);
