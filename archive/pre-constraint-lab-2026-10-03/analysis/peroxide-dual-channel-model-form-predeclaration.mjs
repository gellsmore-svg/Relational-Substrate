import { mkdir, writeFile } from 'node:fs/promises';
import { formatPredeclaration, predeclare } from './predeclaration-gate.mjs';

const outDir = new URL('./out/', import.meta.url);

const target =
  'future fresh held-out peroxide-like rotor; exact molecule, reference geometry, charge rules, torsion grid, and comparator must be reserved before scoring';
const modelForm = 'peroxide dual-channel route and energy model v0';
const descriptors = ['peroxide_anti_planar_release', 'peroxide_unreleased_route_mismatch'];

const pre = predeclare({
  target,
  modelForm,
  descriptors,
  heldOut: true,
  requireConventional: false,
});

const frozenModelForm = {
  energyChannel: {
    purpose: 'absolute barrier and relative energy prediction',
    descriptor: 'peroxide_anti_planar_release',
    releaseStrength: 0.65,
    releaseOnsetDegrees: 145,
    releaseSpanDegrees: 35,
    conversionRule: 'retain the existing branch energy conversion unchanged',
  },
  selectionChannel: {
    purpose: 'conformer admissibility and nonlocal route discrimination only',
    descriptor: 'peroxide_unreleased_route_mismatch',
    formula:
      'evaluate the existing family score with effectiveTorsionRms=torsionRms and effectiveTorsionMax=torsionMax; selectionPenalty = referenceFamilyScore - candidateFamilyScore',
    newCoefficients: 0,
    prohibitedUses: [
      'conversion to cm-1',
      'addition to the energy-channel barrier',
      'target-specific thresholds or weights',
    ],
  },
  passCriteria: {
    exposedFeasibility:
      'selection nonlocal weakest penalty >= 0.10; selection near-reference weakest penalty <= 0.05; energy-channel H2O2 absolute checks remain bit-for-bit unchanged',
    freshEvidence:
      'same frozen channels pass a target reserved after this predeclaration; exposed H2O2 and substituted-peroxide rows do not count',
  },
};

const report = {
  source: 'peroxide-dual-channel-model-form-predeclaration.mjs',
  date: '2026-06-23',
  status: 'model form frozen before any fresh dual-channel target lookup',
  evidenceStatus: 'none',
  predeclaration: pre,
  frozenModelForm,
  nextGate:
    'run exposed H2O2 feasibility without altering either channel, then reserve a fresh peroxide-like rotor before source lookup',
};

const predeclarationBlock = formatPredeclaration(pre)
  .replace('### Predeclaration (gate #1/#2)', '### Predeclaration (gate #1; molecule/torsion)')
  .replace(
    '- Conventional comparators (control evidence only): ',
    '- Conventional comparators: not required for this molecule/torsion model-form diagnostic',
  );

const markdown = `# Peroxide Dual-Channel Model-Form Predeclaration

Status: **${report.status}**

${predeclarationBlock}

## Frozen Channels

| Channel | Purpose | Rule |
|---|---|---|
| energy | absolute barrier and relative energy prediction | existing anti-planar release at strength 0.65, onset 145 degrees, span 35 degrees |
| selection | conformer admissibility and route discrimination | existing family score with torsion deviation unreleased; no new coefficient |

The selection penalty is dimensionless. It must not be converted to cm-1,
added to a barrier, or fitted with target-specific weights.

## Pass Criteria

- exposed feasibility: ${frozenModelForm.passCriteria.exposedFeasibility}
- fresh evidence: ${frozenModelForm.passCriteria.freshEvidence}

Evidence status: ${report.evidenceStatus}.

Next gate: ${report.nextGate}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-dual-channel-model-form-predeclaration.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(new URL('peroxide-dual-channel-model-form-predeclaration.md', outDir), markdown);

console.log(`Peroxide dual-channel predeclaration: ${report.status}`);
console.log(`Predeclaration hash: ${pre.hash}`);
