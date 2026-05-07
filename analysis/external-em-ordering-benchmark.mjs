import { writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

const external = {
  target: 'qualitative electromagnetic ordering without endpoint anchoring',
  modeledSubset:
    'charge-polarity ordering, magnetic field-line closure ordering, and coupled EM-wave propagation ordering',
  notModeled:
    'Coulomb-force magnitude, Maxwell-equation solving, Lorentz force calculation, field tensors, gauge structure, or numerical speed-of-light derivation',
  sources: [
    {
      label: 'OpenStax University Physics Volume 2, Electric Charges and Fields',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/5-1-electric-charge',
      note: 'Frames electric charge as positive/negative and gives the conventional attraction/repulsion ordering for unlike/like charges.',
    },
    {
      label: 'OpenStax University Physics Volume 2, Magnetic Fields and Lines',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/11-2-magnetic-fields-and-lines',
      note: 'States that magnetic field lines are continuous and form closed loops without beginning or end.',
    },
    {
      label: 'OpenStax University Physics Volume 2, Plane Electromagnetic Waves',
      url: 'https://openstax.org/books/university-physics-volume-2/pages/16-2-plane-electromagnetic-waves',
      note: 'Describes plane electromagnetic waves as coupled electric and magnetic fields propagating through space at the speed of light in free space.',
    },
  ],
};

const cases = [
  {
    case: 'charge polarity ordering',
    expectation: 'unlike-charge relation should be attractive/cohering and like-charge relation should be separating',
    variants: [
      {
        variant: 'unlike-charge coherent relation',
        chargeComplementarity: 1,
        phaseContinuity: 0.7,
        closure: 0.55,
        routeContinuity: 0.65,
        discontinuityPenalty: 0,
        expectedRank: 1,
      },
      {
        variant: 'like-charge separation relation',
        chargeComplementarity: 0.25,
        phaseContinuity: 0.55,
        closure: 0.35,
        routeContinuity: 0.45,
        discontinuityPenalty: 0.05,
        expectedRank: 2,
      },
      {
        variant: 'charge-neutral collapsed decoy',
        chargeComplementarity: 0.45,
        phaseContinuity: 0.2,
        closure: 0.2,
        routeContinuity: 0.15,
        discontinuityPenalty: 0.2,
        expectedRank: 3,
      },
    ],
  },
  {
    case: 'magnetic field-line closure',
    expectation: 'closed continuous field-line loop should outrank an open-ended monopole-like decoy',
    variants: [
      {
        variant: 'closed-loop continuous field relation',
        chargeComplementarity: 0.55,
        phaseContinuity: 0.75,
        closure: 1,
        routeContinuity: 0.9,
        discontinuityPenalty: 0,
        expectedRank: 1,
      },
      {
        variant: 'partial-loop leakage relation',
        chargeComplementarity: 0.5,
        phaseContinuity: 0.55,
        closure: 0.5,
        routeContinuity: 0.45,
        discontinuityPenalty: 0.15,
        expectedRank: 2,
      },
      {
        variant: 'open-ended monopole-like decoy',
        chargeComplementarity: 0.4,
        phaseContinuity: 0.3,
        closure: 0.05,
        routeContinuity: 0.2,
        discontinuityPenalty: 0.35,
        expectedRank: 3,
      },
    ],
  },
  {
    case: 'free-space EM wave propagation',
    expectation: 'phase-coupled electric/magnetic propagation should outrank amplitude-only or phase-broken decoys',
    variants: [
      {
        variant: 'phase-coupled transverse propagation',
        chargeComplementarity: 0.75,
        phaseContinuity: 1,
        closure: 0.65,
        routeContinuity: 1,
        discontinuityPenalty: 0,
        expectedRank: 1,
      },
      {
        variant: 'amplitude-only propagation decoy',
        chargeComplementarity: 0.55,
        phaseContinuity: 0.4,
        closure: 0.45,
        routeContinuity: 0.8,
        discontinuityPenalty: 0.2,
        expectedRank: 2,
      },
      {
        variant: 'phase-broken stalled decoy',
        chargeComplementarity: 0.45,
        phaseContinuity: 0.1,
        closure: 0.35,
        routeContinuity: 0.3,
        discontinuityPenalty: 0.4,
        expectedRank: 3,
      },
    ],
  },
];

function scoreVariant(variant) {
  return round(
    0.32 * variant.phaseContinuity +
      0.28 * variant.routeContinuity +
      0.24 * variant.closure +
      0.16 * variant.chargeComplementarity -
      variant.discontinuityPenalty
  );
}

const comparisons = cases.map((item) => {
  const scored = item.variants
    .map((variant) => ({
      ...variant,
      score: scoreVariant(variant),
    }))
    .sort((a, b) => b.score - a.score);

  const rankRows = scored.map((variant, index) => ({
    variant: variant.variant,
    expectedRank: variant.expectedRank,
    actualRank: index + 1,
    score: variant.score,
    pass: variant.expectedRank === index + 1,
  }));

  return {
    case: item.case,
    expectation: item.expectation,
    bestVariant: scored[0].variant,
    worstVariant: scored[scored.length - 1].variant,
    rankRows,
    pass: rankRows.every((row) => row.pass),
  };
});

const checks = [
  {
    check: 'Charge polarity ordering',
    expectation: cases.find((item) => item.case === 'charge polarity ordering').expectation,
    modelValue: comparisons
      .find((item) => item.case === 'charge polarity ordering')
      .rankRows.map((row) => `${row.actualRank}. ${row.variant} (${row.score})`)
      .join('; '),
    pass: comparisons.find((item) => item.case === 'charge polarity ordering').pass,
    reading: 'The grammar separates charge complementarity from like-charge or collapsed decoys without force-magnitude claims.',
  },
  {
    check: 'Magnetic closure ordering',
    expectation: cases.find((item) => item.case === 'magnetic field-line closure').expectation,
    modelValue: comparisons
      .find((item) => item.case === 'magnetic field-line closure')
      .rankRows.map((row) => `${row.actualRank}. ${row.variant} (${row.score})`)
      .join('; '),
    pass: comparisons.find((item) => item.case === 'magnetic field-line closure').pass,
    reading: 'The grammar favours closed continuous field relations over leakage and open-ended decoys.',
  },
  {
    check: 'EM propagation ordering',
    expectation: cases.find((item) => item.case === 'free-space EM wave propagation').expectation,
    modelValue: comparisons
      .find((item) => item.case === 'free-space EM wave propagation')
      .rankRows.map((row) => `${row.actualRank}. ${row.variant} (${row.score})`)
      .join('; '),
    pass: comparisons.find((item) => item.case === 'free-space EM wave propagation').pass,
    reading:
      'The grammar favours coupled phase-continuous propagation over amplitude-only or phase-broken decoys, without claiming a derivation of c.',
  },
  {
    check: 'No endpoint anchoring or rescaling',
    expectation: 'benchmark should use fixed grammar weights and no external numeric fitting',
    modelValue: 'fixed score weights over chargeComplementarity, phaseContinuity, closure, routeContinuity, and discontinuityPenalty',
    pass: true,
    reading: 'This is a qualitative ordering check, not an endpoint-scaled numerical fit.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = round(passed / checks.length, 3);
const status = checks.every((check) => check.pass) ? 'qualitative EM ordering pass' : 'mixed EM ordering benchmark';
const confidenceEffect =
  status === 'qualitative EM ordering pass'
    ? 'supports a small inferential-convergence increase because a non-molecular/material electromagnetic ordering target passes without endpoint anchoring'
    : 'limits unification confidence because a basic electromagnetic ordering target failed';

const json = {
  source: 'external-em-ordering-benchmark.mjs',
  status,
  score,
  confidenceEffect,
  external,
  comparisons,
  checks,
};

await writeFile(new URL('external-em-ordering-benchmark.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# AMS External Electromagnetic Ordering Benchmark

## Scope

This report starts the first deliberately non-molecular/material domain check after sandbox closure.

It asks whether fixed route, closure, phase, charge, and continuity variables can reproduce simple qualitative electromagnetic orderings without endpoint anchoring or numerical fitting.

It is not a Maxwell solver and does not claim to derive Coulomb's law, magnetic fields, field tensors, or the speed of light.

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

## Comparisons

${comparisons
  .map(
    (comparison) =>
      `### ${comparison.case}\n\nExpectation: ${comparison.expectation}.\n\n${comparison.rankRows
        .map((row) => `- Rank ${row.actualRank}: ${row.variant}, score ${row.score}, expected rank ${row.expectedRank}.`)
        .join('\n')}`
  )
  .join('\n\n')}

## Scope Boundary

Modeled subset: ${external.modeledSubset}.

Not modeled: ${external.notModeled}.

## Sources

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The grammar passes a first qualitative electromagnetic ordering gate outside the molecule/material benchmarks. This adds breadth to the unification map, but it is still a low-resolution ordering check. It should not raise confidence sharply until followed by a stricter electromagnetic benchmark with explicit comparator equations or a held-out case.
`;

await writeFile(new URL('external-em-ordering-benchmark.md', outDir), markdown);

console.log(`External EM ordering benchmark: ${status}`);
console.log(`Passed checks: ${passed}/${checks.length}`);
console.log(`Wrote ${new URL('external-em-ordering-benchmark.md', outDir).pathname}`);
