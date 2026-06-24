import { mkdir, writeFile } from 'node:fs/promises';
import { formatPredeclaration, predeclare } from './predeclaration-gate.mjs';

const outDir = new URL('./out/', import.meta.url);

const candidates = [
  {
    target: 'dimethyl peroxide',
    formula: 'CH3OOCH3',
    rotorClass: 'dialkyl peroxide central O-O rotor',
    freshness: 'not used or scored in the existing H2O2, CH3OOH, or C2H5OOH diagnostics',
    diagnosticValue:
      'changes both terminal groups and removes the hydroperoxide H-H cis-crowding shortcut while retaining the central O-O route',
    sourceRisk: 'medium; exact paired geometry and torsional comparator availability is not yet checked',
    decision: 'reserve',
  },
  {
    target: 'tert-butyl hydroperoxide',
    formula: '(CH3)3COOH',
    rotorClass: 'bulky substituted hydroperoxide rotor',
    freshness: 'not scored, but previously listed as a backup candidate',
    diagnosticValue: 'strong crowding stress but less cleanly separates route mismatch from substituent sterics',
    sourceRisk: 'medium-high',
    decision: 'defer',
  },
  {
    target: 'hydroxymethyl hydroperoxide',
    formula: 'HOCH2OOH',
    rotorClass: 'polar substituted hydroperoxide rotor',
    freshness: 'not scored, but previously listed as a deferred candidate',
    diagnosticValue: 'adds hydrogen-bond and polarity channels that complicate the first dual-channel test',
    sourceRisk: 'high',
    decision: 'defer',
  },
];

const reservedTarget = candidates.find((candidate) => candidate.decision === 'reserve');
const target =
  `${reservedTarget.target} (${reservedTarget.formula}) central O-O torsion; paired equilibrium geometry and torsional energy comparator required before scoring`;

const pre = predeclare({
  target,
  modelForm: 'peroxide dual-channel route and energy model v0',
  descriptors: ['peroxide_anti_planar_release', 'peroxide_unreleased_route_mismatch'],
  heldOut: true,
  requireConventional: false,
});

const frozenApplication = {
  energyChannel:
    'use the existing peroxide anti-planar release energy channel unchanged: strength=0.65, onset=145 degrees, span=35 degrees',
  selectionChannel:
    'use the existing family score with torsion deviation unreleased; no conversion to cm-1 and no new coefficient',
  geometryMapping:
    'map the source-defined C-O-O-C torsion to the model torsion coordinate; freeze atom ordering and angular convention during source lock',
  passFail: [
    'source provides or supports a defensible equilibrium C-O-O-C torsion and at least one nonlocal torsional comparator',
    'selection channel ranks the source equilibrium route above the named nonlocal comparator',
    'energy channel preserves the source barrier ordering without target-specific rescaling',
    'record failure if paired geometry and energy data cannot be source-locked',
  ],
};

const blockedActions = [
  'do not look up dimethyl peroxide geometry or torsional values inside this reservation',
  'do not change the live energy release parameters after source lookup',
  'do not add a dimethyl-peroxide-specific selection coefficient or threshold',
  'do not substitute another molecule after seeing source values without first recording source-lock failure',
  'do not count computed-comparator agreement as experimental validation',
];

const report = {
  source: 'peroxide-dual-channel-target-reservation.mjs',
  date: '2026-06-23',
  status: 'fresh dual-channel target reserved before source lookup',
  reservedTarget,
  candidates,
  predeclaration: pre,
  frozenApplication,
  blockedActions,
  nextGate:
    'search for a primary or source-grade dimethyl peroxide equilibrium-geometry and torsional-energy source, then record a source-lock pass or failure before extraction',
};

const predeclarationBlock = formatPredeclaration(pre)
  .replace('### Predeclaration (gate #1/#2)', '### Predeclaration (fresh dual-channel target)')
  .replace(
    '- Conventional comparators (control evidence only): ',
    '- Conventional comparators: not required for this molecule/torsion target',
  );

const markdown = `# Peroxide Dual-Channel Fresh Target Reservation

Status: **${report.status}**

This artifact reserves the target identity before source lookup. It contains no
dimethyl peroxide geometry, barrier, or conformer values.

${predeclarationBlock}

## Reserved Target

| Field | Value |
|---|---|
| molecule | ${reservedTarget.target} |
| formula | ${reservedTarget.formula} |
| rotor class | ${reservedTarget.rotorClass} |
| diagnostic value | ${reservedTarget.diagnosticValue} |
| source risk | ${reservedTarget.sourceRisk} |

## Frozen Application

- Energy channel: ${frozenApplication.energyChannel}.
- Selection channel: ${frozenApplication.selectionChannel}.
- Geometry mapping: ${frozenApplication.geometryMapping}.

## Pass/Fail

${frozenApplication.passFail.map((item) => `- ${item}`).join('\n')}

## Blocked Actions

${blockedActions.map((item) => `- ${item}`).join('\n')}

Next gate: ${report.nextGate}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-dual-channel-target-reservation.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(new URL('peroxide-dual-channel-target-reservation.md', outDir), markdown);

console.log(`Peroxide dual-channel target reservation: ${reservedTarget.target} (${reservedTarget.formula})`);
console.log(`Predeclaration hash: ${pre.hash}`);
