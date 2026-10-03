import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const predeclaration = JSON.parse(
  await readFile(
    new URL(
      'peroxide-equilibrium-relative-crowding-predeclaration.json',
      outDir,
    ),
    'utf8',
  ),
);
const h2o2 = JSON.parse(
  await readFile(
    new URL('external-h2o2-quantitative-benchmark.json', outDir),
    'utf8',
  ),
);
const tbhp = JSON.parse(
  await readFile(new URL('peroxide-tbhp-source-extraction.json', outDir), 'utf8'),
);
const peroxyformic = JSON.parse(
  await readFile(
    new URL('peroxide-peroxyformic-source-lock-screen.json', outDir),
    'utf8',
  ),
);

function clamp01(value) {
  return Math.max(0, Math.min(1, value));
}

function signedDifference(value, reference) {
  return ((value - reference + 540) % 360) - 180;
}

function cyclicDifference(value, reference) {
  return Math.abs(signedDifference(value, reference));
}

function score(candidate, reference) {
  const signedDisplacement = signedDifference(candidate, reference);
  const torsionDeviation = clamp01(cyclicDifference(candidate, reference) / 45);
  const relativeCrowding = clamp01(-signedDisplacement / 60);
  const antiPlanarRelease =
    clamp01((candidate - 145) / 35) * clamp01(1 - relativeCrowding);
  const effectiveTorsionDeviation =
    torsionDeviation * (1 - antiPlanarRelease * 0.65);
  const penalty = clamp01(
    effectiveTorsionDeviation * 0.42 + relativeCrowding * 0.58,
  );
  return {
    candidate,
    reference,
    signedDisplacement,
    torsionDeviation,
    relativeCrowding,
    antiPlanarRelease,
    effectiveTorsionDeviation,
    penalty,
  };
}

function ranks(values) {
  return values.map(
    (value) =>
      1 +
      values.filter((candidate) => candidate < value).length +
      (values.filter((candidate) => candidate === value).length - 1) / 2,
  );
}

function pearson(left, right) {
  const leftMean = left.reduce((sum, value) => sum + value, 0) / left.length;
  const rightMean = right.reduce((sum, value) => sum + value, 0) / right.length;
  const numerator = left.reduce(
    (sum, value, index) =>
      sum + (value - leftMean) * (right[index] - rightMean),
    0,
  );
  const leftScale = Math.sqrt(
    left.reduce((sum, value) => sum + (value - leftMean) ** 2, 0),
  );
  const rightScale = Math.sqrt(
    right.reduce((sum, value) => sum + (value - rightMean) ** 2, 0),
  );
  return numerator / (leftScale * rightScale);
}

const h2o2Reference = h2o2.metrics.referenceAngle;
const h2o2Rows = {
  equilibrium: score(h2o2Reference, h2o2Reference),
  trans: score(180, h2o2Reference),
  cis: score(0, h2o2Reference),
};
const h2o2Ratio = h2o2Rows.cis.penalty / h2o2Rows.trans.penalty;
const externalH2o2Ratio =
  h2o2.external.cisBarrierCm1 / h2o2.external.transBarrierCm1;
const h2o2RatioFactor = Math.max(
  h2o2Ratio / externalH2o2Ratio,
  externalH2o2Ratio / h2o2Ratio,
);

const tbhpReference = tbhp.torsionConstruct.equilibriumDegrees;
const tbhpRows = {
  equilibrium: score(tbhpReference, tbhpReference),
  trans: score(
    tbhp.torsionConstruct.transBarrierCoordinateDegrees,
    tbhpReference,
  ),
};

const peroxyReference = peroxyformic.lockedConstruct.coordinates.find(
  (row) => row.role === 'equilibrium',
);
const peroxyRows = peroxyformic.lockedConstruct.coordinates.map((row) => ({
  ...row,
  ...score(row.torsionDegrees, peroxyReference.torsionDegrees),
}));
const sourceRises = peroxyRows.map(
  (row) => row.relativeEnergyEv - peroxyReference.relativeEnergyEv,
);
const predictedReference = peroxyRows.find(
  (row) => row.role === 'equilibrium',
).penalty;
const predictedRises = peroxyRows.map(
  (row) => row.penalty - predictedReference,
);
const sourceMax = Math.max(...sourceRises);
const predictedMax = Math.max(...predictedRises);
const normalizedSource = sourceRises.map((value) => value / sourceMax);
const normalizedPredicted = predictedRises.map(
  (value) => value / predictedMax,
);
const peroxyMae =
  normalizedSource.reduce(
    (sum, value, index) =>
      sum + Math.abs(value - normalizedPredicted[index]),
    0,
  ) / normalizedSource.length;
const peroxySpearman = pearson(ranks(sourceRises), ranks(predictedRises));
const peroxyOrdering = [...peroxyRows]
  .sort((left, right) => left.penalty - right.penalty)
  .map((row) => row.role);

const checks = [
  {
    check: 'H2O2 equilibrium < trans < cis',
    pass:
      h2o2Rows.equilibrium.penalty < h2o2Rows.trans.penalty &&
      h2o2Rows.trans.penalty < h2o2Rows.cis.penalty,
    value: `${h2o2Rows.equilibrium.penalty.toFixed(4)} < ${h2o2Rows.trans.penalty.toFixed(4)} < ${h2o2Rows.cis.penalty.toFixed(4)}`,
  },
  {
    check: 'H2O2 cis/trans ratio within factor 2',
    pass: h2o2RatioFactor <= 2,
    value: `model=${h2o2Ratio.toFixed(4)}; source=${externalH2o2Ratio.toFixed(4)}; factor=${h2o2RatioFactor.toFixed(4)}`,
  },
  {
    check: 'TBHP equilibrium below trans',
    pass: tbhpRows.equilibrium.penalty < tbhpRows.trans.penalty,
    value: `${tbhpRows.equilibrium.penalty.toFixed(4)} < ${tbhpRows.trans.penalty.toFixed(4)}`,
  },
  {
    check: 'peroxyformic ordering restored',
    pass:
      JSON.stringify(peroxyOrdering) ===
      JSON.stringify(['equilibrium', 'intermediate', 'nonlocal']),
    value: peroxyOrdering.join(' < '),
  },
  {
    check: 'peroxyformic Spearman at least 0.8',
    pass: peroxySpearman >= 0.8,
    value: peroxySpearman.toFixed(4),
  },
  {
    check: 'peroxyformic normalized-rise MAE at most 0.20',
    pass: peroxyMae <= 0.2,
    value: peroxyMae.toFixed(4),
  },
];

const passed = checks.every((check) => check.pass);
const report = {
  source: 'peroxide-equilibrium-relative-crowding-diagnostic.mjs',
  date: '2026-06-24',
  status: passed
    ? 'exposed-equilibrium-relative-crowding-feasibility-pass'
    : 'exposed-equilibrium-relative-crowding-feasibility-fail',
  validationClaim: false,
  evidenceStatus: 'none; H2O2, TBHP, and peroxyformic acid are exposed',
  predeclarationHash: predeclaration.predeclaration.hash,
  formula: predeclaration.frozenModelForm,
  cases: {
    h2o2: {
      rows: h2o2Rows,
      modelCisTransRatio: h2o2Ratio,
      externalCisTransRatio: externalH2o2Ratio,
      ratioFactor: h2o2RatioFactor,
    },
    tbhp: { rows: tbhpRows },
    peroxyformic: {
      rows: peroxyRows,
      sourceRises,
      predictedRises,
      normalizedSource,
      normalizedPredicted,
      ordering: peroxyOrdering,
      spearman: peroxySpearman,
      normalizedMae: peroxyMae,
    },
  },
  checks,
  decision: passed
    ? 'the equilibrium-relative crowding descriptor clears exposed feasibility without fitted coefficients; it may proceed to a fresh target reservation under a separately frozen validation contract'
    : 'reject or revise the descriptor before any fresh target reservation',
  confidenceAction: 'none; exposed redesign feasibility only',
};

const markdown = `# Peroxide Equilibrium-Relative Crowding Diagnostic

Status: **${report.status}**

This diagnostic uses exposed cases only and adds no evidence.

| Check | Value | Result |
|---|---|---|
${checks
  .map(
    (row) =>
      `| ${row.check} | ${row.value} | ${row.pass ? 'pass' : 'fail'} |`,
  )
  .join('\n')}

## Peroxyformic Profile

| Role | Torsion | Relative crowding | Penalty | Source normalized rise | Predicted normalized rise |
|---|---:|---:|---:|---:|---:|
${peroxyRows
  .map(
    (row, index) =>
      `| ${row.role} | ${row.torsionDegrees} | ${row.relativeCrowding.toFixed(4)} | ${row.penalty.toFixed(4)} | ${normalizedSource[index].toFixed(4)} | ${normalizedPredicted[index].toFixed(4)} |`,
  )
  .join('\n')}

Decision: ${report.decision}.

Confidence action: ${report.confidenceAction}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-equilibrium-relative-crowding-diagnostic.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('peroxide-equilibrium-relative-crowding-diagnostic.md', outDir),
  markdown,
);

console.log(`Equilibrium-relative crowding diagnostic: ${report.status}`);
