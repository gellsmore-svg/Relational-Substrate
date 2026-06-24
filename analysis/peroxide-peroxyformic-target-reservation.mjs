import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { formatPredeclaration, predeclare } from './predeclaration-gate.mjs';

const outDir = new URL('./out/', import.meta.url);
const availability = JSON.parse(
  await readFile(
    new URL('peroxide-intermediate-route-source-availability.json', outDir),
    'utf8',
  ),
);
const selected = availability.selected;

if (selected.target !== 'peroxyformic acid') {
  throw new Error('Intermediate-route screen did not select peroxyformic acid.');
}

const target =
  'peroxyformic acid (HC(O)OOH) source-defined O-O/COOH torsional profile with equilibrium, intermediate, and nonlocal coordinates on one potential-energy surface';
const pre = predeclare({
  target,
  modelForm: 'peroxide observable-torsion selection plus released-energy model v1',
  descriptors: ['peroxide_anti_planar_release', 'peroxide_torsion_route_distance'],
  heldOut: true,
  requireConventional: false,
});

const frozenApplication = {
  selectionFormula:
    'clamp01(cyclicDifference(candidateTorsion, sourceDefinedReferenceTorsion, 360) / 45)',
  energyFormula:
    'clamp01(torsionDeviation * (1 - antiPlanarRelease * 0.65)) * 0.42 + cisCrowding * 0.58',
  releaseParameters: {
    strength: 0.65,
    onsetDegrees: 145,
    spanDegrees: 35,
  },
  sourceRequirements: [
    'one source-defined potential-energy equilibrium coordinate',
    'at least one same-surface intermediate coordinate 10 to less than 45 degrees cyclic distance from equilibrium',
    'at least one same-surface nonlocal coordinate at least 45 degrees from equilibrium',
    'relative energies for all three coordinates under one method and construct',
  ],
  normalization:
    'subtract the source equilibrium energy; divide source and predicted rises by their respective maximum rise across the frozen three-coordinate set',
  passFail: [
    'the intermediate selection distance must be greater than 0 and less than 1',
    'predicted and source relative-energy ordering must agree across equilibrium, intermediate, and nonlocal coordinates',
    'Spearman rank correlation across the frozen coordinates must be at least 0.8',
    'mean absolute error between normalized source and normalized predicted energy rises must be at most 0.20',
    'no target-specific rescaling, coordinate substitution, or post-extraction threshold change',
  ],
};

const blockedActions = [
  'do not extract numerical peroxyformic-acid torsions or energies inside this reservation',
  'do not replace a missing intermediate coordinate with a trans endpoint after source inspection',
  'do not fit the 45-degree tolerance or release parameters to peroxyformic acid',
  'do not mix coordinates from different electronic states, methods, or vibrational constructs',
  'record source-lock failure if the source does not expose the frozen three-coordinate set',
];

const report = {
  source: 'peroxide-peroxyformic-target-reservation.mjs',
  date: '2026-06-24',
  status: 'peroxyformic acid reserved before numerical source extraction',
  target: selected,
  predeclaration: pre,
  frozenApplication,
  blockedActions,
  nextGate:
    'open the primary peroxyformic-acid source and source-lock the frozen three-coordinate same-surface profile without changing this contract',
};

const predeclarationBlock = formatPredeclaration(pre)
  .replace(
    '### Predeclaration (gate #1/#2)',
    '### Predeclaration (fresh intermediate-route target)',
  )
  .replace(
    '- Conventional comparators (control evidence only): ',
    '- Conventional comparators: not required for this molecule/torsion target',
  );

const markdown = `# Peroxyformic-Acid Intermediate-Route Target Reservation

Status: **${report.status}**

No numerical peroxyformic-acid torsion or energy values were consulted in this
reservation.

${predeclarationBlock}

## Frozen Quantitative Contract

- selection: \`${frozenApplication.selectionFormula}\`
- energy: \`${frozenApplication.energyFormula}\`
- normalization: ${frozenApplication.normalization}

### Required Source Rows

${frozenApplication.sourceRequirements.map((item) => `- ${item}`).join('\n')}

### Pass/Fail

${frozenApplication.passFail.map((item) => `- ${item}`).join('\n')}

### Blocked Actions

${blockedActions.map((item) => `- ${item}`).join('\n')}

Next gate: ${report.nextGate}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-peroxyformic-target-reservation.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('peroxide-peroxyformic-target-reservation.md', outDir),
  markdown,
);

console.log(`Peroxyformic target reservation hash: ${pre.hash}`);
