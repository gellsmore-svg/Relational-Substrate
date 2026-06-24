import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function cyclicDifference(value, target, period = 360) {
  return Math.abs(((value - target + period / 2) % period) - period / 2);
}

function clamp01(value) {
  return Math.max(0, Math.min(1, value));
}

function routeDistance(candidate, reference) {
  return clamp01(cyclicDifference(candidate, reference) / 45);
}

const predeclaration = JSON.parse(
  await readFile(new URL('peroxide-observable-route-model-form-predeclaration.json', outDir), 'utf8'),
);
const sourceLock = JSON.parse(
  await readFile(new URL('peroxide-dimethyl-source-lock-screen.json', outDir), 'utf8'),
);
const promotion = JSON.parse(
  await readFile(new URL('peroxide-release-promotion-review.json', outDir), 'utf8'),
);

const cases = [
  {
    case: 'H2O2 local neighbour',
    construct: 'PES torsion coordinate',
    referenceDegrees: 111.5,
    candidateDegrees: 120,
    expected: 'local',
  },
  {
    case: 'H2O2 trans route',
    construct: 'PES torsion coordinate',
    referenceDegrees: 111.5,
    candidateDegrees: 180,
    expected: 'nonlocal',
  },
  {
    case: 'dimethyl peroxide PES cis route',
    construct: 'potential-energy equilibrium',
    referenceDegrees: sourceLock.extractedPreview.bitencourtComputedPes.equilibriumAngleDegrees,
    candidateDegrees: 0,
    expected: 'nonlocal',
  },
  {
    case: 'dimethyl peroxide dynamical versus PES construct',
    construct: 'cross-construct diagnostic; not a conformer score',
    referenceDegrees: sourceLock.extractedPreview.bitencourtComputedPes.equilibriumAngleDegrees,
    candidateDegrees: sourceLock.extractedPreview.nistEvaluatedDynamicModel.equilibriumAngleDegrees,
    expected: 'different-construct',
  },
].map((row) => ({
  ...row,
  cyclicDifferenceDegrees: cyclicDifference(row.candidateDegrees, row.referenceDegrees),
  selectionDistance: Number(routeDistance(row.candidateDegrees, row.referenceDegrees).toFixed(4)),
}));

const checks = [
  {
    check: 'H2O2 local route remains local',
    pass: cases[0].selectionDistance < 1 / 3,
    value: cases[0].selectionDistance,
  },
  {
    check: 'H2O2 trans route is separated',
    pass: cases[1].selectionDistance === 1,
    value: cases[1].selectionDistance,
  },
  {
    check: 'dimethyl PES cis route is separated from trans minimum',
    pass: cases[2].selectionDistance === 1,
    value: cases[2].selectionDistance,
  },
  {
    check: 'dynamical and PES coordinates are not silently conflated',
    pass: cases[3].selectionDistance === 1 && cases[3].expected === 'different-construct',
    value: cases[3].selectionDistance,
  },
  {
    check: 'live energy channel remains unchanged',
    pass:
      promotion.currentLiveRelease.strength === 0.65 &&
      promotion.currentLiveRelease.onset === 145 &&
      promotion.currentLiveRelease.span === 35,
    value: JSON.stringify(promotion.currentLiveRelease),
  },
];

const status = checks.every((check) => check.pass)
  ? 'exposed-observable-route-feasibility-pass'
  : 'exposed-observable-route-feasibility-fail';

const report = {
  source: 'peroxide-observable-route-feasibility-diagnostic.mjs',
  date: '2026-06-23',
  status,
  validationClaim: false,
  evidenceStatus: 'none; all cases are exposed redesign pressure',
  predeclarationHash: predeclaration.predeclaration.hash,
  cases,
  checks,
  liveEnergyRelease: promotion.currentLiveRelease,
  decision:
    status === 'exposed-observable-route-feasibility-pass'
      ? 'the observable-only route descriptor removes the target-mapping ambiguity and may proceed to a new pre-lookup reservation'
      : 'reject or revise the descriptor before reserving another target',
};

const markdown = `# Peroxide Observable-Route Feasibility Diagnostic

Status: **${status}**

This is exposed-data feasibility only. It adds no evidence.

| Case | Construct | Reference | Candidate | Difference | Selection distance | Expected |
|---|---|---:|---:|---:|---:|---|
${cases
  .map(
    (row) =>
      `| ${row.case} | ${row.construct} | ${row.referenceDegrees} | ${row.candidateDegrees} | ${row.cyclicDifferenceDegrees} | ${row.selectionDistance} | ${row.expected} |`,
  )
  .join('\n')}

The descriptor consumes only a source-defined torsion and construct label. It
does not require charges, pseudo-atoms, steric construction, or family weights.

Live energy release remains strength ${promotion.currentLiveRelease.strength},
onset ${promotion.currentLiveRelease.onset}, span
${promotion.currentLiveRelease.span}.

Decision: ${report.decision}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-observable-route-feasibility-diagnostic.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(new URL('peroxide-observable-route-feasibility-diagnostic.md', outDir), markdown);

console.log(`Peroxide observable-route feasibility: ${status}`);
