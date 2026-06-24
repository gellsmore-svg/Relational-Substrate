import { mkdir, writeFile } from 'node:fs/promises';
import { formatPredeclaration, predeclare } from './predeclaration-gate.mjs';

const outDir = new URL('./out/', import.meta.url);

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const candidates = [
  {
    target: 'methyl hydroperoxide',
    formula: 'CH3OOH',
    rotorClass: 'substituted peroxide O-O rotor',
    relationToRepair: 'same O-O torsion family as H2O2, but with asymmetric methyl substitution',
    freshness: 'not used in the current H2O2, ethane, hydrazine, disulfane, or selenane diagnostics',
    sourceRisk: 'medium: likely richer spectroscopy/quantum literature than rarer mixed H-X-Y-H rotors, but exact barrier/geometry source still unverified',
    decision: 'reserve-for-source-lock',
    reason:
      'Best first source-lock target because it keeps peroxide O-O torsion while changing substituent topology enough to test whether the anti-planar release repair generalizes beyond exposed H2O2 rows.',
  },
  {
    target: 'ditellane',
    formula: 'H2Te2',
    rotorClass: 'same-topology heavy H2X2 rotor',
    relationToRepair: 'same H-X-X-H topology as disulfane and selenane, but heavier central atoms',
    freshness: 'not used in the current exposed rows',
    sourceRisk: 'high: data availability and stable geometry/barrier sources may be poor',
    decision: 'defer',
    reason:
      'Good topology purity but too likely to collapse into source scarcity or heavy-atom effects tied to the separate trans-planar topology penalty.',
  },
  {
    target: 'hydroxylamine',
    formula: 'NH2OH',
    rotorClass: 'adjacent N-O heteroatom rotor',
    relationToRepair: 'adjacent heteroatom torsion with asymmetric H-bearing ends',
    freshness: 'neutral target distinct from exposed hydrazine cation',
    sourceRisk: 'medium: likely sourceable, but less directly peroxide-family than CH3OOH',
    decision: 'backup-source-lock',
    reason:
      'Useful backup if peroxide-family source lock fails; tests adjacent heteroatom torsion but not the O-O release term as directly.',
  },
  {
    target: 'dioxygen difluoride',
    formula: 'FOOF',
    rotorClass: 'O-O rotor without terminal hydrogens',
    relationToRepair: 'same central O-O bond but lacks the H-H cis-crowding channel',
    freshness: 'not used',
    sourceRisk: 'medium-high: sourceable but chemically hazardous and not H-bearing',
    decision: 'reject-current-gate',
    reason:
      'It removes the H-H crowding channel that motivated the release term, so it is a poor first test of the candidate repair.',
  },
];

const reserved = candidates.find((candidate) => candidate.decision === 'reserve-for-source-lock');
const target =
  `${reserved.target} (${reserved.formula}) ${reserved.rotorClass}; source lock required before any barrier, geometry, or torsion scoring lookup`;

const pre = predeclare({
  target,
  modelForm: 'peroxide anti-planar release repair candidate v0',
  descriptors: ['peroxide_anti_planar_release'],
  heldOut: true,
  requireConventional: false,
});

const sourceLockRequirements = [
  'named primary or source-grade computational/spectroscopic reference for the same molecular identity',
  'frozen equilibrium geometry or reference torsion convention before extracting a target value',
  'frozen charge/partial-charge assignment rule or explicit no-charge simplification before scoring',
  'frozen torsion grid and reference/nonlocal/local-window definitions before target scoring',
  'measured or source-grade computed barrier/order comparator, recorded without changing release strength/onset/span',
  'explicit failure rule if no paired geometry and torsion comparator can be found',
];

const blockedActions = [
  'do not look up CH3OOH barrier or geometry values inside this reservation artifact',
  'do not tune release strength/onset/span from CH3OOH after lookup',
  'do not count a pass unless the exact predeclared formula remains unchanged',
  'do not reuse H2O2, hydrazine cation, disulfane, or selenane exposed rows as fresh evidence',
];

const report = {
  source: 'peroxide-fresh-rotor-target-reservation.mjs',
  date: '2026-06-23',
  status: 'fresh rotor target identity reserved for source lock; no source lookup and no scoring performed',
  reservedTarget: reserved,
  predeclaration: pre,
  candidates,
  sourceLockRequirements,
  blockedActions,
};

const predeclarationBlock = formatPredeclaration(pre)
  .replace('### Predeclaration (gate #1/#2)', '### Predeclaration (target reservation; molecule/torsion)')
  .replace('- Conventional comparators (control evidence only): ', '- Conventional comparators: not required for this molecule/torsion diagnostic');

const markdown = `# Peroxide Fresh Rotor Target Reservation

## Scope

This report reserves a fresh rotor target identity before source lookup. It does not look up target values, does not score a target, and does not change the peroxide anti-planar release repair candidate.

Date: ${report.date}

${predeclarationBlock}

## Candidate Screen

${table(
  ['Target', 'Formula', 'Rotor class', 'Relation to repair', 'Freshness', 'Source risk', 'Decision', 'Reason'],
  candidates.map((row) => [
    row.target,
    row.formula,
    row.rotorClass,
    row.relationToRepair,
    row.freshness,
    row.sourceRisk,
    row.decision,
    row.reason,
  ]),
)}

## Reserved Target

${table(
  ['Field', 'Value'],
  [
    ['Target', reserved.target],
    ['Formula', reserved.formula],
    ['Rotor class', reserved.rotorClass],
    ['Reason', reserved.reason],
  ],
)}

## Source-Lock Requirements

${sourceLockRequirements.map((item) => `- ${item}`).join('\n')}

## Blocked Actions

${blockedActions.map((item) => `- ${item}`).join('\n')}

## Decision

Methyl hydroperoxide is reserved as the first source-lock target for the peroxide anti-planar release repair candidate. The next step may search for source-grade CH3OOH torsion/geometry data, but the repair formula remains frozen at strength 0.25, onset 155 degrees, span 20 degrees. If source lock fails, the reservation must record failure before selecting the backup target.

Status: ${report.status}
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('peroxide-fresh-rotor-target-reservation.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('peroxide-fresh-rotor-target-reservation.md', outDir), markdown);

console.log(markdown);
