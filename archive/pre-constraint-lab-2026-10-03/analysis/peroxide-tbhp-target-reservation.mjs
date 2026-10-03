import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { formatPredeclaration, predeclare } from './predeclaration-gate.mjs';

const outDir = new URL('./out/', import.meta.url);
const availability = JSON.parse(
  await readFile(new URL('peroxide-source-availability-screen.json', outDir), 'utf8'),
);
const selected = availability.selected;

if (selected.target !== 'tert-butyl hydroperoxide') {
  throw new Error('Availability screen did not select tert-butyl hydroperoxide.');
}

const target =
  `${selected.target} (${selected.formula}) source-defined O-O/COOH torsion; potential-energy equilibrium and same-surface nonlocal comparator required`;
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
  toleranceDegrees: 45,
  torsionMapping:
    'use the source COOH/O-O torsion convention; freeze atom ordering and angle range during source lock',
  constructRule:
    'score only same-surface potential-energy torsion coordinates; spectroscopy may validate construct identity but dynamical averages are not PES minima',
  energyRule:
    'retain live release strength=0.65, onset=145 degrees, span=35 degrees; no target-specific scaling',
  passFail: [
    'source-lock equilibrium torsion and at least one nonlocal torsion coordinate with energy ordering',
    'selection distance ranks the equilibrium route closer than the nonlocal route',
    'energy channel preserves source ordering without target-specific rescaling',
    'label computed and experimental support separately',
  ],
};

const blockedActions = [
  'do not extract numeric TBHP torsion or barrier values inside this reservation',
  'do not tune the 45-degree tolerance or live release parameters',
  'do not use OH-stretch frequencies as direct torsional barrier values',
  'do not count the previous metadata availability screen as validation',
];

const report = {
  source: 'peroxide-tbhp-target-reservation.mjs',
  date: '2026-06-23',
  status: 'tert-butyl hydroperoxide reserved before numerical source extraction',
  target: selected,
  predeclaration: pre,
  frozenApplication,
  blockedActions,
  nextGate:
    'obtain the 2021 TBHP torsion papers or author/repository versions, then source-lock numerical torsion constructs before extraction',
};

const predeclarationBlock = formatPredeclaration(pre)
  .replace('### Predeclaration (gate #1/#2)', '### Predeclaration (fresh TBHP target)')
  .replace(
    '- Conventional comparators (control evidence only): ',
    '- Conventional comparators: not required for this molecule/torsion target',
  );

const markdown = `# Tert-Butyl Hydroperoxide Target Reservation

Status: **${report.status}**

The identity was selected by a metadata-only availability screen. No numerical
TBHP torsion or barrier values were read before this reservation.

${predeclarationBlock}

## Frozen Contract

- selection: \`${frozenApplication.selectionFormula}\`
- mapping: ${frozenApplication.torsionMapping}
- construct rule: ${frozenApplication.constructRule}
- energy rule: ${frozenApplication.energyRule}

## Blocked Actions

${blockedActions.map((item) => `- ${item}`).join('\n')}

Next gate: ${report.nextGate}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-tbhp-target-reservation.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(new URL('peroxide-tbhp-target-reservation.md', outDir), markdown);

console.log(`TBHP target reservation hash: ${pre.hash}`);
