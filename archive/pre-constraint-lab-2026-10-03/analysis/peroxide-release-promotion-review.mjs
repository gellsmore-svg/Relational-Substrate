import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

async function readJson(name) {
  return JSON.parse(await readFile(new URL(name, outDir), 'utf8'));
}

function round(value, digits = 4) {
  return Number(value.toFixed(digits));
}

function pctError(model, target) {
  return ((model - target) / target) * 100;
}

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const sensitivity = await readJson('peroxide-anti-planar-release-sensitivity.json');
const releasePredeclaration = await readJson('peroxide-release-repair-predeclaration.json');
const ethylScore = await readJson('peroxide-ethyl-hydroperoxide-evidence-scoring.json');
const h2o2Absolute = await readJson('external-h2o2-absolute-barrier-benchmark.json');

const frozen = releasePredeclaration.frozenCandidate;
const candidateKey = `strength=${frozen.releaseStrength};onset=${frozen.releaseOnsetDegrees};span=${frozen.releaseSpanDegrees}`;
const candidate = sensitivity.summaries.find((row) => row.key === candidateKey);

if (!candidate) {
  throw new Error(`Frozen release candidate ${candidateKey} is missing from the sensitivity grid.`);
}

const scale = h2o2Absolute.scale.cm1PerPenalty;
const externalTrans = h2o2Absolute.external.transBarrierCm1;
const externalCis = h2o2Absolute.external.cisBarrierCm1;
const externalRatio = externalCis / externalTrans;
const candidateTransCm1 = candidate.transPenalty * scale;
const candidateCisCm1 = candidate.cisPenalty * scale;
const candidateRatio = candidateCisCm1 / candidateTransCm1;
const transErrorPct = pctError(candidateTransCm1, externalTrans);
const cisErrorPct = pctError(candidateCisCm1, externalCis);
const ratioErrorPct = pctError(candidateRatio, externalRatio);
const barrierTolerancePct = h2o2Absolute.external.barrierTolerancePct;
const ratioTolerancePct = h2o2Absolute.external.ratioTolerancePct;

const checks = [
  {
    check: 'H2O2 nonlocal shape',
    pass: candidate.passShape,
    value: `nonlocal weakest=${candidate.nonlocalWeakest}; near weakest=${candidate.nearWeakest}`,
    requirement: 'nonlocal weakest >= 0.10 and near weakest <= 0.05',
  },
  {
    check: 'Ethyl hydroperoxide predeclared comparator',
    pass: ethylScore.decision.status === 'computed-comparator-pass',
    value: `source ratio=${ethylScore.sourceComparators.sourceBarrierRatio}; predicted ratio=${ethylScore.checks.predictedPenaltyRatio}`,
    requirement: 'computed-comparator-pass under frozen rule',
  },
  {
    check: 'H2O2 absolute trans barrier regression',
    pass: Math.abs(transErrorPct) <= barrierTolerancePct,
    value: `${round(candidateTransCm1, 2)} cm-1; error=${round(transErrorPct, 2)}%`,
    requirement: `${externalTrans} cm-1 +/- ${barrierTolerancePct}%`,
  },
  {
    check: 'H2O2 absolute cis barrier regression',
    pass: Math.abs(cisErrorPct) <= barrierTolerancePct,
    value: `${round(candidateCisCm1, 2)} cm-1; error=${round(cisErrorPct, 2)}%`,
    requirement: `${externalCis} cm-1 +/- ${barrierTolerancePct}%`,
  },
  {
    check: 'H2O2 cis/trans ratio regression',
    pass: Math.abs(ratioErrorPct) <= ratioTolerancePct,
    value: `${round(candidateRatio, 4)}; error=${round(ratioErrorPct, 2)}%`,
    requirement: `${round(externalRatio, 4)} +/- ${ratioTolerancePct}%`,
  },
];

const failedChecks = checks.filter((check) => !check.pass);
const status = failedChecks.length === 0 ? 'promotion-approved' : 'promotion-blocked-cross-benchmark-regression';
const decision =
  status === 'promotion-approved'
    ? 'promote the frozen release candidate to the live peroxide branch default'
    : 'retain the current live release parameters; do not promote the frozen candidate';
const nextModelRequirement =
  status === 'promotion-approved'
    ? 'rerun the full benchmark suite before confidence accounting'
    : 'introduce a model form that can improve nonlocal discrimination without increasing the H2O2 trans barrier penalty; do not continue tuning only strength/onset/span against exposed targets';

const report = {
  source: 'peroxide-release-promotion-review.mjs',
  date: '2026-06-23',
  status,
  decision,
  currentLiveRelease: sensitivity.current.release,
  candidateRelease: candidate.release,
  candidateKey,
  candidateMetrics: {
    nearWeakest: candidate.nearWeakest,
    shoulderWeakest: candidate.shoulderWeakest,
    nonlocalWeakest: candidate.nonlocalWeakest,
    transPenalty: candidate.transPenalty,
    cisPenalty: candidate.cisPenalty,
    h2o2TransCm1: round(candidateTransCm1, 2),
    h2o2CisCm1: round(candidateCisCm1, 2),
    h2o2CisTransRatio: round(candidateRatio, 4),
    transErrorPct: round(transErrorPct, 2),
    cisErrorPct: round(cisErrorPct, 2),
    ratioErrorPct: round(ratioErrorPct, 2),
  },
  checks,
  failedChecks: failedChecks.map((check) => check.check),
  confidenceAction: 'no global confidence change',
  branchAction:
    status === 'promotion-approved'
      ? 'candidate may become branch default after full-suite verification'
      : 'candidate remains a diagnostic branch alternative, not the live default',
  nextModelRequirement,
};

const markdown = `# Peroxide Release Promotion Review

## Decision

Status: **${status}**

${decision}.

The candidate improves the H2O2 nonlocal shape and passes the predeclared
ethyl hydroperoxide computed comparator. It must also preserve the existing
ethane-scaled H2O2 absolute barrier checks before it can replace the live
release parameters.

## Parameters

${table(
  ['Setting', 'Strength', 'Onset', 'Span'],
  [
    ['current live', sensitivity.current.release.strength, sensitivity.current.release.onset, sensitivity.current.release.span],
    ['promotion candidate', candidate.release.strength, candidate.release.onset, candidate.release.span],
  ],
)}

## Checks

${table(
  ['Check', 'Requirement', 'Candidate value', 'Result'],
  checks.map((check) => [check.check, check.requirement, check.value, check.pass ? 'pass' : 'fail']),
)}

## Reading

The candidate predicts an H2O2 trans barrier of ${round(candidateTransCm1, 2)}
cm-1 instead of ${externalTrans} cm-1, an error of ${round(transErrorPct, 2)}%.
The cis barrier remains near target because the candidate leaves the cis
penalty unchanged, but the resulting cis/trans ratio error is
${round(ratioErrorPct, 2)}%.

Branch action: ${report.branchAction}.

Confidence action: ${report.confidenceAction}.

Next model requirement: ${nextModelRequirement}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('peroxide-release-promotion-review.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('peroxide-release-promotion-review.md', outDir), markdown);

console.log(`Peroxide release promotion review: ${status}`);
console.log(`Failed checks: ${failedChecks.length}/${checks.length}`);
console.log(`Candidate H2O2 trans barrier: ${round(candidateTransCm1, 2)} cm-1`);
console.log(`Wrote ${new URL('peroxide-release-promotion-review.md', outDir).pathname}`);
