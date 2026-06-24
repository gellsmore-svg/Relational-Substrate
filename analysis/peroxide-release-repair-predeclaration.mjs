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

const modelForm = 'peroxide anti-planar release repair candidate v0';
const target =
  'future fresh held-out H2X2-like rotor target; exact molecule, geometry source, charge rules, torsion grid, and measured/computed comparator rows must be reserved before scoring';
const descriptors = ['peroxide_anti_planar_release'];

const pre = predeclare({
  target,
  modelForm,
  descriptors,
  heldOut: true,
  requireConventional: false,
});

const frozenCandidate = {
  releaseStrength: 0.25,
  releaseOnsetDegrees: 155,
  releaseSpanDegrees: 20,
  source: 'least-disruptive nonzero row from peroxide-anti-planar-release-sensitivity.mjs',
};

const blockedEvidence = [
  {
    source: 'current H2O2 torsion grid',
    reason: 'already exposed diagnostic pressure; can tune or reject a candidate but cannot validate it',
  },
  {
    source: 'strength=0 full release removal',
    reason: 'mathematically strongest but physically blunt; erases the intended crowded-cis versus uncrowded-trans distinction',
  },
  {
    source: 'same-topology disulfane/selenane trans failures',
    reason: 'belong to the heavy-atom trans-planar diagnostic and are already exposed calibration pressure',
  },
];

const nextGate = [
  {
    step: 'fresh target reservation',
    passCondition: 'one H2X2-like or adjacent rotor target is reserved before lookup and not already used in the exposed diagnostics',
  },
  {
    step: 'source lock',
    passCondition: 'geometry, charge assignment, torsion reference/comparator, and grid are frozen from named sources',
  },
  {
    step: 'formula lock',
    passCondition: 'release strength/onset/span and equation are frozen before target scoring',
  },
  {
    step: 'scoring gate',
    passCondition: 'candidate improves nonlocal separation without damaging the local tolerance window under the frozen pass/fail criteria',
  },
];

const report = {
  source: 'peroxide-release-repair-predeclaration.mjs',
  date: '2026-06-23',
  status:
    'peroxide anti-planar release repair candidate predeclared as diagnostic shape only; scoring remains blocked until a fresh held-out rotor target is reserved',
  predeclaration: pre,
  frozenCandidate,
  blockedEvidence,
  nextGate,
};
const predeclarationBlock = formatPredeclaration(pre)
  .replace('### Predeclaration (gate #1/#2)', '### Predeclaration (gate #1; molecule/torsion)')
  .replace('- Conventional comparators (control evidence only): ', '- Conventional comparators: not required for this molecule/torsion diagnostic');

const markdown = `# Peroxide Anti-Planar Release Repair Predeclaration

## Scope

This report freezes a candidate repair shape for the weak peroxide nonlocal torsion frontier. It does not change the molecule model, does not score a held-out target, and does not add evidence.

Date: ${report.date}

${predeclarationBlock}

Note: the conventional-baseline requirement is intentionally disabled for this molecule/torsion predeclaration because density/Lorentz-Lorenz controls apply to material refractive-index scoring, not H2X2 rotor topology diagnostics.

## Frozen Candidate Shape

${table(
  ['Parameter', 'Value'],
  [
    ['release strength', frozenCandidate.releaseStrength],
    ['release onset', `${frozenCandidate.releaseOnsetDegrees} degrees`],
    ['release span', `${frozenCandidate.releaseSpanDegrees} degrees`],
    ['source', frozenCandidate.source],
  ],
)}

## Blocked Evidence

${table(
  ['Source', 'Reason it cannot validate the repair'],
  blockedEvidence.map((row) => [row.source, row.reason]),
)}

## Next Scoring Gate

${table(
  ['Step', 'Pass condition'],
  nextGate.map((row) => [row.step, row.passCondition]),
)}

## Decision

The least-disruptive nonzero candidate from the sensitivity sweep may be used as a predeclared repair shape for a future test, but it remains blocked from evidence status. A fresh held-out rotor target must be reserved before lookup, and the formula must remain unchanged through scoring.

Status: ${report.status}
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('peroxide-release-repair-predeclaration.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('peroxide-release-repair-predeclaration.md', outDir), markdown);

console.log(markdown);
