import { mkdir, writeFile } from 'node:fs/promises';
import { formatPredeclaration, predeclare } from './predeclaration-gate.mjs';

const outDir = new URL('./out/', import.meta.url);

const candidates = [
  {
    target: 'hydroxymethyl hydroperoxide',
    formula: 'HOCH2OOH',
    sourceSignal:
      'primary spectroscopy metadata explicitly states that the torsional potential is represented as a Fourier series of the torsional angle',
    freshness:
      'previously named only as a backup identity; no numerical HMHP torsion coordinates, Fourier coefficients, or profile energies have been extracted in this project',
    constructRisk:
      'contains coupled internal rotors; usable only if one source-defined O-O torsion profile is isolated under a fixed or explicitly minimized companion-coordinate rule',
    decision: 'reserve',
  },
  {
    target: 'peracetic acid',
    formula: 'CH3C(O)OOH',
    sourceSignal:
      'open-access far-infrared study provides multidimensional torsional surfaces',
    freshness:
      'numerical conformer and barrier values were exposed in search metadata before reservation',
    constructRisk: 'multi-rotor surface',
    decision: 'exclude-from-fresh-validation',
  },
  {
    target: 'isopropyl hydroperoxide',
    formula: '(CH3)2CHOOH',
    sourceSignal:
      'recent isomer survey and thermochemistry sources exist',
    freshness: 'not previously scored',
    constructRisk:
      'metadata does not yet establish a source-defined multi-point O-O torsional profile',
    decision: 'defer',
  },
];

const reservedTarget = candidates.find((candidate) => candidate.decision === 'reserve');
const target =
  'hydroxymethyl hydroperoxide (HOCH2OOH) source-defined O-O torsional profile with equilibrium, intermediate, and nonlocal coordinates under one declared companion-coordinate rule';
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
    'one source-defined potential-energy equilibrium for a named O-O torsion',
    'one intermediate coordinate with cyclic distance 10 to less than 45 degrees from equilibrium',
    'one nonlocal coordinate with cyclic distance at least 45 degrees from equilibrium',
    'all three energies from one electronic state, method, and companion-coordinate treatment',
    'atom order and positive torsion direction explicitly locked before scoring',
  ],
  normalization:
    'subtract equilibrium energy; normalize source and predicted rises by their respective maximum rise over the frozen three-coordinate set',
  passFail: [
    'intermediate selection distance is greater than 0 and less than 1',
    'predicted and source relative-energy ordering agree',
    'Spearman rank correlation is at least 0.8',
    'normalized-rise mean absolute error is at most 0.20',
    'no target-specific direction flip, rescaling, threshold change, or coordinate replacement',
  ],
};

const report = {
  source: 'peroxide-v2-fresh-target-reservation.mjs',
  date: '2026-06-24',
  status: 'HMHP reserved before numerical torsion-profile extraction',
  candidates,
  reservedTarget,
  predeclaration: pre,
  frozenContract,
  blockedActions: [
    'do not use peracetic acid as fresh validation after numerical metadata exposure',
    'do not extract HMHP numerical profile values inside this reservation',
    'do not collapse different companion-coordinate treatments into one profile',
    'record source-lock failure if a clean three-coordinate profile cannot be reconstructed',
  ],
  nextGate:
    'open the primary HMHP spectroscopy source and lock one same-construct O-O torsional profile without changing this contract',
};

const predeclarationBlock = formatPredeclaration(pre)
  .replace(
    '### Predeclaration (gate #1/#2)',
    '### Predeclaration (fresh equilibrium-relative crowding target)',
  )
  .replace(
    '- Conventional comparators (control evidence only): ',
    '- Conventional comparators: not required for this molecule/torsion target',
  );

const markdown = `# Peroxide v2 Fresh Target Reservation

Status: **${report.status}**

${predeclarationBlock}

## Target

${reservedTarget.target} (${reservedTarget.formula}).

Freshness: ${reservedTarget.freshness}.

Construct risk: ${reservedTarget.constructRisk}.

## Frozen Contract

- crowding: \`${frozenContract.relativeCrowding}\`
- energy: \`${frozenContract.energyPenalty}\`
- normalization: ${frozenContract.normalization}

### Required Source Rows

${frozenContract.sourceRequirements.map((item) => `- ${item}`).join('\n')}

### Pass/Fail

${frozenContract.passFail.map((item) => `- ${item}`).join('\n')}

Peracetic acid is explicitly excluded from fresh validation because numerical
values were exposed before reservation.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-v2-fresh-target-reservation.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('peroxide-v2-fresh-target-reservation.md', outDir),
  markdown,
);

console.log(`Peroxide v2 fresh target reservation: ${pre.hash}`);
