import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { formatPredeclaration, predeclare } from './predeclaration-gate.mjs';

const outDir = new URL('./out/', import.meta.url);
const availability = JSON.parse(
  await readFile(
    new URL('peroxide-v2-source-availability-screen.json', outDir),
    'utf8',
  ),
);
const selected = availability.selected;

if (selected.target !== 'methyl chloroperoxide') {
  throw new Error('Availability screen did not select methyl chloroperoxide.');
}

const target =
  'methyl chloroperoxide (CH3OOCl) source-defined C-O-O-Cl torsional profile with equilibrium, intermediate, and nonlocal coordinates under one electronic-structure method';
const pre = predeclare({
  target,
  modelForm:
    'peroxide observable-route plus equilibrium-relative crowding energy model v2',
  descriptors: [
    'peroxide_anti_planar_release',
    'peroxide_torsion_route_distance',
    'peroxide_equilibrium_relative_crowding',
  ],
  heldOut: true,
  requireConventional: false,
});

const frozenContract = {
  signedDisplacement:
    '((candidateTorsion - sourceDefinedReferenceTorsion + 540) % 360) - 180',
  relativeCrowding: 'clamp01(-signedDisplacement / 60)',
  torsionDeviation:
    'clamp01(cyclicDifference(candidateTorsion, sourceDefinedReferenceTorsion, 360) / 45)',
  antiPlanarRelease:
    'clamp01((candidateTorsion - 145) / 35) * clamp01(1 - relativeCrowding)',
  energyPenalty:
    'clamp01(torsionDeviation * (1 - antiPlanarRelease * 0.65)) * 0.42 + relativeCrowding * 0.58',
  sourceRequirements: [
    'one source-defined ground-state C-O-O-Cl equilibrium torsion',
    'one same-profile intermediate coordinate 10 to less than 45 degrees from equilibrium',
    'one same-profile nonlocal coordinate at least 45 degrees from equilibrium',
    'relative energies for all rows under one method and relaxation rule',
    'positive torsion direction fixed from source atom order before scoring',
  ],
  passFail: [
    'intermediate selection distance is greater than 0 and less than 1',
    'source and predicted energy ordering agree',
    'Spearman rank correlation is at least 0.8',
    'normalized-rise mean absolute error is at most 0.20',
    'no target-specific direction flip, rescaling, or profile-row replacement',
  ],
  interpretationBoundary:
    'a pass supports adjacent peroxide-family transfer only; a fail may reflect halogen-specific electronic structure and must not be generalized as a hydroperoxide failure without a hydroperoxide target',
};

const report = {
  source: 'peroxide-methyl-chloroperoxide-reservation.mjs',
  date: '2026-06-24',
  status:
    'methyl chloroperoxide reserved before numerical torsion-profile extraction',
  target: selected,
  predeclaration: pre,
  frozenContract,
  blockedActions: [
    'do not inspect numerical CH3OOCl profile values inside this reservation',
    'do not reinterpret isomerization barriers as torsional scan rows',
    'do not mix methods or relaxation rules',
    'record source-lock failure if the full profile cannot be accessed or reconstructed directly',
  ],
  nextGate:
    'open the primary CH3OOCl paper and source-lock its torsional profile without changing this contract',
};

const predeclarationBlock = formatPredeclaration(pre)
  .replace(
    '### Predeclaration (gate #1/#2)',
    '### Predeclaration (fresh adjacent peroxide-family target)',
  )
  .replace(
    '- Conventional comparators (control evidence only): ',
    '- Conventional comparators: not required for this molecule/torsion target',
  );

const markdown = `# Methyl Chloroperoxide Target Reservation

Status: **${report.status}**

${predeclarationBlock}

The frozen v2 formula and profile thresholds are unchanged.

Boundary: ${frozenContract.interpretationBoundary}.

No numerical CH3OOCl torsion or energy values were inspected before this
reservation.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-methyl-chloroperoxide-reservation.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('peroxide-methyl-chloroperoxide-reservation.md', outDir),
  markdown,
);

console.log(`Methyl chloroperoxide reservation: ${pre.hash}`);
