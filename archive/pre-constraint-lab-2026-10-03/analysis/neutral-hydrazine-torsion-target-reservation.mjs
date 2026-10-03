import { mkdir, writeFile } from 'node:fs/promises';
import { formatPredeclaration, predeclare } from './predeclaration-gate.mjs';

const outDir = new URL('./out/', import.meta.url);

const target =
  'neutral hydrazine (N2H4) same-topology N-N internal-rotation profile with source-defined equilibrium and at least two barrier coordinates';
const pre = predeclare({
  target,
  modelForm:
    'hydrazine-family geometry penalty with unchanged ethane absolute scale v0',
  descriptors: ['hydrazine_family_torsion_penalty'],
  heldOut: true,
  requireConventional: false,
});

const frozenModel = {
  topology:
    'reuse the exact two-ended N-N hydrazine geometry builder and candidate scoring implementation from external-hydrazine-cation-torsion-benchmark.mjs',
  geometryConstants: {
    nnAngstrom: 1.45,
    nhAngstrom: 1.02,
    hnnDegrees: 112,
    hnhDegrees: 107,
    routeBase: 0.72,
  },
  featureConstants: {
    torsionToleranceDegrees: 55,
    bondToleranceAngstrom: 0.25,
    stericClearanceSpanAngstrom: 0.55,
    polaritySpan: 0.9,
    cisCrowdingSpanDegrees: 55,
    releaseStrength: 0.65,
    releaseOnsetDegrees: 145,
    releaseSpanDegrees: 35,
  },
  weights: {
    geometryFit: 0.18,
    angleStrain: 0.16,
    bondStrain: 0.12,
    polarityBalance: 0.1,
    routeContinuity: 0.16,
    stericObstruction: 0.28,
  },
  scale:
    'reuse external-ethane-quantitative-benchmark kcal-per-penalty and convert with 349.755 cm-1 per kcal mol-1',
  sourceRequirements: [
    'neutral hydrazine identity, not hydrazine cation',
    'source-defined equilibrium torsion',
    'at least two barrier coordinates and barrier magnitudes on one internal-rotation construct',
    'all barrier angles expressed in one atom-order convention',
  ],
  passFail: [
    'predicted barrier ordering matches the source',
    'every nonzero barrier magnitude is within 35 percent',
    'the ratio of the two nonzero barriers is within 35 percent when two are available',
    'no endpoint fitting, scale multiplier, charge correction, or geometry-constant change',
  ],
};

const report = {
  source: 'neutral-hydrazine-torsion-target-reservation.mjs',
  date: '2026-06-24',
  status: 'neutral hydrazine reserved before numerical barrier lookup',
  predeclaration: pre,
  frozenModel,
  rejectedTarget: {
    target: 'hydroxylamine (NH2OH)',
    reason:
      'the current two-ended N-N geometry proxy cannot transfer unchanged to a one-ended N-O rotor; using it would require a new geometry model before validation',
  },
  blockedActions: [
    'do not inspect neutral-hydrazine barrier numbers inside this reservation',
    'do not reuse hydrazine-cation endpoint multipliers',
    'do not alter charges, geometry constants, weights, or the ethane scale',
    'record source-lock failure if two source-grade barrier rows are unavailable',
  ],
  nextGate:
    'source-lock neutral hydrazine equilibrium and barrier rows, then execute the unchanged cation architecture and scale',
};

const predeclarationBlock = formatPredeclaration(pre)
  .replace(
    '### Predeclaration (gate #1/#2)',
    '### Predeclaration (neutral hydrazine absolute transfer)',
  )
  .replace(
    '- Conventional comparators (control evidence only): ',
    '- Conventional comparators: not required for this molecule/torsion target',
  );

const markdown = `# Neutral Hydrazine Torsion Target Reservation

Status: **${report.status}**

${predeclarationBlock}

The existing hydrazine-cation topology, geometry constants, weights, release
parameters, and ethane-derived absolute scale are frozen unchanged.

## Pass/Fail

${frozenModel.passFail.map((item) => `- ${item}`).join('\n')}

Hydroxylamine is rejected for this gate because it would require a new N-O
geometry model rather than an unchanged topology transfer.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('neutral-hydrazine-torsion-target-reservation.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('neutral-hydrazine-torsion-target-reservation.md', outDir),
  markdown,
);

console.log(`Neutral hydrazine reservation: ${pre.hash}`);
