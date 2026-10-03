import { mkdir, writeFile } from 'node:fs/promises';
import { formatPredeclaration, predeclare } from './predeclaration-gate.mjs';

const outDir = new URL('./out/', import.meta.url);

const target =
  'future fresh held-out peroxide-like rotor with source-defined torsion construct; exact molecule and source must be reserved after this model-form freeze';
const pre = predeclare({
  target,
  modelForm: 'peroxide observable-torsion selection plus released-energy model v1',
  descriptors: ['peroxide_anti_planar_release', 'peroxide_torsion_route_distance'],
  heldOut: true,
  requireConventional: false,
});

const frozenModelForm = {
  energyChannel: {
    descriptor: 'peroxide_anti_planar_release',
    releaseStrength: 0.65,
    releaseOnsetDegrees: 145,
    releaseSpanDegrees: 35,
    action: 'unchanged from the live peroxide energy branch',
  },
  selectionChannel: {
    descriptor: 'peroxide_torsion_route_distance',
    formula:
      'clamp01(cyclicDifference(candidateTorsion, sourceDefinedReferenceTorsion, 360) / 45)',
    toleranceDegrees: 45,
    newCoefficients: 0,
    requiredConstructLabel: ['potential-energy equilibrium', 'dynamical/vibrationally averaged'],
    prohibitedInputs: [
      'partial charges',
      'invented terminal-group coordinates',
      'steric pseudo-atoms',
      'family-score weights',
      'target-specific thresholds',
      'conversion to cm-1',
    ],
  },
  interpretation:
    'The selection channel answers whether two source-defined torsion routes are locally equivalent. It does not predict an energy barrier or assert that a dynamical average is a PES minimum.',
  evidenceStatus:
    'model form frozen after exposed H2O2 and dimethyl-peroxide pressure; neither target can validate this redesign',
};

const report = {
  source: 'peroxide-observable-route-model-form-predeclaration.mjs',
  date: '2026-06-23',
  status: 'observable-only selection model form frozen before another fresh target reservation',
  predeclaration: pre,
  frozenModelForm,
  nextGate:
    'run exposed feasibility on H2O2 and both dimethyl-peroxide constructs, then reserve a new target only if construct separation is coherent',
};

const predeclarationBlock = formatPredeclaration(pre)
  .replace('### Predeclaration (gate #1/#2)', '### Predeclaration (molecule/torsion model form)')
  .replace(
    '- Conventional comparators (control evidence only): ',
    '- Conventional comparators: not required for this molecule/torsion model form',
  );

const markdown = `# Peroxide Observable-Torsion Model-Form Predeclaration

Status: **${report.status}**

${predeclarationBlock}

## Frozen Selection Rule

\`${frozenModelForm.selectionChannel.formula}\`

- tolerance: ${frozenModelForm.selectionChannel.toleranceDegrees} degrees
- new coefficients: ${frozenModelForm.selectionChannel.newCoefficients}
- construct label required: ${frozenModelForm.selectionChannel.requiredConstructLabel.join(' or ')}
- energy conversion: prohibited

The live energy channel remains strength 0.65, onset 145 degrees, span 35
degrees.

Evidence status: ${frozenModelForm.evidenceStatus}.

Next gate: ${report.nextGate}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-observable-route-model-form-predeclaration.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(new URL('peroxide-observable-route-model-form-predeclaration.md', outDir), markdown);

console.log(`Peroxide observable-route predeclaration: ${report.status}`);
console.log(`Predeclaration hash: ${pre.hash}`);
