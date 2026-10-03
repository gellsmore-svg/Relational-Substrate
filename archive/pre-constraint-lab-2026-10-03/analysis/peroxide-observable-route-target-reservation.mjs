import { mkdir, writeFile } from 'node:fs/promises';
import { formatPredeclaration, predeclare } from './predeclaration-gate.mjs';

const outDir = new URL('./out/', import.meta.url);

const candidates = [
  {
    target: 'diethyl peroxide',
    formula: 'C2H5OOC2H5',
    rotorClass: 'symmetric dialkyl peroxide central O-O rotor',
    freshness:
      'not named, sourced, extracted, or scored in the existing project artifacts or cached peroxide source',
    diagnosticValue:
      'tests transfer from dimethyl to a larger symmetric dialkyl peroxide without returning to the terminal O-H torsion used for hydroperoxides',
    sourceRisk: 'unknown until post-reservation source search',
    decision: 'reserve',
  },
  {
    target: 'tert-butyl hydroperoxide',
    formula: '(CH3)3COOH',
    rotorClass: 'bulky hydroperoxide terminal O-H/O-O coupled rotor',
    freshness: 'previously named as a backup candidate but not scored',
    diagnosticValue: 'strong steric stress but less clean central O-O transfer',
    sourceRisk: 'previously assessed medium-high',
    decision: 'defer',
  },
  {
    target: 'di-tert-butyl peroxide',
    formula: '(CH3)3COOC(CH3)3',
    rotorClass: 'bulky symmetric dialkyl peroxide',
    freshness: 'not used',
    diagnosticValue: 'likely dominated by substituent crowding and coupled rotations',
    sourceRisk: 'likely high for a simple source-defined O-O torsional comparator',
    decision: 'defer',
  },
];

const reservedTarget = candidates.find((candidate) => candidate.decision === 'reserve');
const target =
  `${reservedTarget.target} (${reservedTarget.formula}) central C-O-O-C torsion; source-defined equilibrium construct and at least one nonlocal torsion comparator required`;

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
  constructRule:
    'the reference torsion must be labelled potential-energy equilibrium or dynamical/vibrationally averaged; cross-construct comparisons are diagnostic only',
  energyRule:
    'retain live release strength=0.65, onset=145 degrees, span=35 degrees; no target-specific rescaling',
  passFail: [
    'source-lock a C-O-O-C torsion convention and reference construct before numeric extraction',
    'source-lock at least one named nonlocal torsion route or barrier coordinate in the same convention',
    'selection distance must rank the reference route closer than the nonlocal route',
    'energy ordering must agree with the source without target-specific scaling',
    'record source-lock failure if paired geometry and torsional-energy information cannot be obtained',
  ],
};

const blockedActions = [
  'do not search for diethyl peroxide geometry or barriers inside this reservation step',
  'do not substitute a different target after seeing source availability without recording failure',
  'do not introduce charges, steric pseudo-atoms, or target-specific selection thresholds',
  'do not convert the selection distance to cm-1',
  'do not count a computed-only comparator as experimental validation',
];

const report = {
  source: 'peroxide-observable-route-target-reservation.mjs',
  date: '2026-06-23',
  status: 'fresh observable-route target reserved before source lookup',
  reservedTarget,
  candidates,
  predeclaration: pre,
  frozenApplication,
  blockedActions,
  nextGate:
    'search primary and repository sources for diethyl peroxide C-O-O-C equilibrium geometry and torsional-energy data; record source-lock pass or failure',
};

const predeclarationBlock = formatPredeclaration(pre)
  .replace('### Predeclaration (gate #1/#2)', '### Predeclaration (fresh observable-route target)')
  .replace(
    '- Conventional comparators (control evidence only): ',
    '- Conventional comparators: not required for this molecule/torsion target',
  );

const markdown = `# Peroxide Observable-Route Fresh Target Reservation

Status: **${report.status}**

No diethyl peroxide source values were consulted in this reservation.

${predeclarationBlock}

## Reserved Target

| Field | Value |
|---|---|
| target | ${reservedTarget.target} |
| formula | ${reservedTarget.formula} |
| rotor class | ${reservedTarget.rotorClass} |
| freshness | ${reservedTarget.freshness} |
| diagnostic value | ${reservedTarget.diagnosticValue} |

## Frozen Contract

- selection: \`${frozenApplication.selectionFormula}\`
- construct rule: ${frozenApplication.constructRule}
- energy rule: ${frozenApplication.energyRule}

## Pass/Fail

${frozenApplication.passFail.map((item) => `- ${item}`).join('\n')}

## Blocked Actions

${blockedActions.map((item) => `- ${item}`).join('\n')}

Next gate: ${report.nextGate}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-observable-route-target-reservation.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(new URL('peroxide-observable-route-target-reservation.md', outDir), markdown);

console.log(`Observable-route target reserved: ${reservedTarget.target} (${reservedTarget.formula})`);
console.log(`Predeclaration hash: ${pre.hash}`);
