import { mkdir, writeFile } from 'node:fs/promises';
import { formatPredeclaration, predeclare } from './predeclaration-gate.mjs';

const outDir = new URL('./out/', import.meta.url);

const target =
  'exposed peroxide pressure set only: H2O2, tert-butyl hydroperoxide, and peroxyformic acid; no fresh evidence claim';
const pre = predeclare({
  target,
  modelForm:
    'peroxide observable-route plus equilibrium-relative crowding energy model v2',
  descriptors: [
    'peroxide_anti_planar_release',
    'peroxide_torsion_route_distance',
    'peroxide_equilibrium_relative_crowding',
  ],
  heldOut: false,
  requireConventional: false,
});

const frozenModelForm = {
  signedDisplacement:
    '((candidateTorsion - sourceDefinedReferenceTorsion + 540) % 360) - 180',
  relativeCrowding: 'clamp01(-signedDisplacement / 60)',
  torsionDeviation:
    'clamp01(cyclicDifference(candidateTorsion, sourceDefinedReferenceTorsion, 360) / 45)',
  antiPlanarRelease:
    'clamp01((candidateTorsion - 145) / 35) * clamp01(1 - relativeCrowding)',
  energyPenalty:
    'clamp01(torsionDeviation * (1 - antiPlanarRelease * 0.65)) * 0.42 + relativeCrowding * 0.58',
  inheritedConstants: {
    crowdingSpanDegrees: 60,
    torsionToleranceDegrees: 45,
    releaseStrength: 0.65,
    releaseOnsetDegrees: 145,
    releaseSpanDegrees: 35,
    torsionWeight: 0.42,
    crowdingWeight: 0.58,
  },
  newFittedCoefficients: 0,
  directionRule:
    'the source atom order fixes the signed direction before scoring; positive displacement is release-facing and negative displacement is compressed/cis-facing',
  exposedChecks: [
    'H2O2: equilibrium < trans < cis penalty and cis/trans penalty ratio within factor 2 of 6.621',
    'TBHP: equilibrium penalty below trans penalty',
    'peroxyformic acid: equilibrium < 30 degree < 90 degree penalty, Spearman at least 0.8, normalized-rise MAE at most 0.20',
  ],
};

const report = {
  source: 'peroxide-equilibrium-relative-crowding-predeclaration.mjs',
  date: '2026-06-24',
  status:
    'equilibrium-relative crowding model form frozen for exposed feasibility only',
  validationClaim: false,
  predeclaration: pre,
  frozenModelForm,
  blockedActions: [
    'do not count exposed pressure-case agreement as new evidence',
    'do not alter direction, spans, weights, release parameters, or thresholds during feasibility scoring',
    'do not reserve a fresh target unless every exposed check passes',
  ],
  nextGate:
    'run the unchanged formula on exposed H2O2, TBHP, and peroxyformic-acid pressure cases',
};

const predeclarationBlock = formatPredeclaration(pre)
  .replace(
    '### Predeclaration (gate #1/#2)',
    '### Predeclaration (equilibrium-relative crowding redesign)',
  )
  .replace(
    '- Conventional comparators (control evidence only): ',
    '- Conventional comparators: not required for this molecule/torsion diagnostic',
  );

const markdown = `# Peroxide Equilibrium-Relative Crowding Predeclaration

Status: **${report.status}**

${predeclarationBlock}

## Frozen Formula

- signed displacement: \`${frozenModelForm.signedDisplacement}\`
- crowding: \`${frozenModelForm.relativeCrowding}\`
- energy penalty: \`${frozenModelForm.energyPenalty}\`
- new fitted coefficients: ${frozenModelForm.newFittedCoefficients}

Direction rule: ${frozenModelForm.directionRule}.

## Exposed Checks

${frozenModelForm.exposedChecks.map((item) => `- ${item}`).join('\n')}

No exposed pass may be counted as fresh evidence.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-equilibrium-relative-crowding-predeclaration.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('peroxide-equilibrium-relative-crowding-predeclaration.md', outDir),
  markdown,
);

console.log(`Equilibrium-relative crowding predeclaration: ${pre.hash}`);
