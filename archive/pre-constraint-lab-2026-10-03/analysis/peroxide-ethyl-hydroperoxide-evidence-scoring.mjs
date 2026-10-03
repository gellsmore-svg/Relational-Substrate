import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { clamp01 } from './molecule-model.mjs';

const outDir = new URL('./out/', import.meta.url);
const extractionUrl = new URL('./out/peroxide-ethyl-hydroperoxide-source-extraction.json', import.meta.url);

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

function round(value, digits = 4) {
  return Number(value.toFixed(digits));
}

function cyclicDifference(value, target, period = 360) {
  const raw = Math.abs(((value - target + period / 2) % period) - period / 2);
  return Math.min(raw, period - raw);
}

function alphaDiagnostic(alpha, equilibriumAlpha, repair) {
  const torsionDeviation = clamp01(cyclicDifference(alpha, equilibriumAlpha) / 90);
  const cisCrowding = clamp01((60 - alpha) / 60);
  const antiPlanarRelease = clamp01((alpha - repair.releaseOnsetDegrees) / repair.releaseSpanDegrees) * clamp01(1 - cisCrowding);
  const effectiveTorsionDeviation = torsionDeviation * (1 - antiPlanarRelease * repair.releaseStrength);
  const predictedPenaltyIndex = clamp01(effectiveTorsionDeviation * 0.42 + cisCrowding * 0.58);

  return {
    alpha,
    torsionDeviation,
    cisCrowding,
    antiPlanarRelease,
    effectiveTorsionDeviation,
    predictedPenaltyIndex,
  };
}

const extraction = JSON.parse(await readFile(extractionUrl, 'utf8'));
const repair = extraction.frozenRule;
const equilibriumAlpha = extraction.extractedGeometry.values.equilibriumDihedralDegrees;
const transBarrier = extraction.extractedBarriers.values.VtransCm1;
const cisBarrier = extraction.extractedBarriers.values.VcisCm1;
const sourceBarrierRatio = extraction.extractedBarriers.values.transCisRatio;
const alphaGrid = [0, 30, 60, 90, 120, 150, 180];
const rows = alphaGrid.map((alpha) => alphaDiagnostic(alpha, equilibriumAlpha, repair));
const cisRow = rows.find((row) => row.alpha === 0);
const transRow = rows.find((row) => row.alpha === 180);
const predictedPenaltyRatio = transRow.predictedPenaltyIndex / cisRow.predictedPenaltyIndex;

const checks = {
  sourceRatioPass: sourceBarrierRatio < 0.2,
  predictedRatioPass: predictedPenaltyRatio < 0.35,
  predictedOrderingPass: transRow.predictedPenaltyIndex < cisRow.predictedPenaltyIndex,
  sourceOrderingPass: transBarrier < cisBarrier,
  releaseActiveAtTrans: transRow.antiPlanarRelease > 0,
  cisCrowdingPreserved: cisRow.cisCrowding > 0.9 && cisRow.antiPlanarRelease === 0,
};

const passed = Object.values(checks).every(Boolean);
const decision = {
  status: passed ? 'computed-comparator-pass' : 'fail',
  evidenceStatus:
    'eligible as computed-comparator evidence only: target, rule, release parameters, and pass/fail thresholds were predeclared before source extraction; not experimental validation',
  reading: passed
    ? 'the frozen substituted-peroxide rule correctly keeps ethyl hydroperoxide trans torsion much less penalized than cis torsion under the source-locked computed barriers'
    : 'the frozen substituted-peroxide rule does not satisfy the predeclared ethyl hydroperoxide checks',
  confidenceEffect:
    'do not raise global confidence automatically; this can support the peroxide repair branch only as a computed-comparator held-out pass after ledger policy review',
};

const report = {
  source: 'peroxide-ethyl-hydroperoxide-evidence-scoring.mjs',
  date: '2026-06-23',
  target: extraction.target,
  extractionArtifact: 'analysis/out/peroxide-ethyl-hydroperoxide-source-extraction.json',
  predeclarationHash: extraction.target.predeclarationHash,
  frozenRule: repair,
  sourceComparators: {
    transBarrierCm1: transBarrier,
    cisBarrierCm1: cisBarrier,
    sourceBarrierRatio,
  },
  diagnosticModel: {
    equilibriumAlphaDegrees: equilibriumAlpha,
    alphaGrid,
    formula:
      'penaltyIndex = 0.42 * effectiveTorsionDeviation + 0.58 * cisCrowding; effectiveTorsionDeviation = torsionDeviation * (1 - antiPlanarRelease * releaseStrength)',
  },
  checks: {
    ...checks,
    predictedPenaltyRatio: round(predictedPenaltyRatio),
  },
  rows: rows.map((row) => ({
    alpha: row.alpha,
    torsionDeviation: round(row.torsionDeviation),
    cisCrowding: round(row.cisCrowding),
    antiPlanarRelease: round(row.antiPlanarRelease),
    effectiveTorsionDeviation: round(row.effectiveTorsionDeviation),
    predictedPenaltyIndex: round(row.predictedPenaltyIndex),
  })),
  decision,
};

const markdown = `# Ethyl Hydroperoxide Evidence Scoring

## Scope

This consumes the source-locked ethyl hydroperoxide extraction under the predeclared substituted-peroxide gate. It is eligible only as computed-comparator evidence, not experimental validation.

Date: ${report.date}

## Inputs

${table(
  ['Field', 'Value'],
  [
    ['Target', `${report.target.molecule} (${report.target.formula}; ${report.target.sourceLabel})`],
    ['Predeclaration hash', report.predeclarationHash],
    ['Extraction artifact', report.extractionArtifact],
    ['Frozen release', `strength=${repair.releaseStrength}; onset=${repair.releaseOnsetDegrees}; span=${repair.releaseSpanDegrees}`],
    ['Equilibrium dihedral', `${equilibriumAlpha} deg`],
    ['Trans barrier', `${transBarrier} cm-1`],
    ['Cis barrier', `${cisBarrier} cm-1`],
    ['Source trans/cis ratio', sourceBarrierRatio],
  ],
)}

## Alpha Rows

${table(
  ['Alpha', 'Torsion deviation', 'Cis crowding', 'Anti-planar release', 'Effective torsion deviation', 'Predicted penalty index'],
  report.rows.map((row) => [
    row.alpha,
    row.torsionDeviation,
    row.cisCrowding,
    row.antiPlanarRelease,
    row.effectiveTorsionDeviation,
    row.predictedPenaltyIndex,
  ]),
)}

## Checks

${table(
  ['Check', 'Result'],
  [
    ['Source ratio < 0.20', checks.sourceRatioPass ? 'pass' : 'fail'],
    ['Predicted ratio < 0.35', checks.predictedRatioPass ? 'pass' : 'fail'],
    ['Predicted trans penalty lower than cis', checks.predictedOrderingPass ? 'pass' : 'fail'],
    ['Source trans barrier lower than cis', checks.sourceOrderingPass ? 'pass' : 'fail'],
    ['Release active at trans', checks.releaseActiveAtTrans ? 'pass' : 'fail'],
    ['Cis crowding preserved', checks.cisCrowdingPreserved ? 'pass' : 'fail'],
    ['Predicted trans/cis penalty ratio', report.checks.predictedPenaltyRatio],
  ],
)}

## Decision

${table(
  ['Field', 'Value'],
  [
    ['Status', decision.status],
    ['Evidence status', decision.evidenceStatus],
    ['Reading', decision.reading],
    ['Confidence effect', decision.confidenceEffect],
  ],
)}
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('peroxide-ethyl-hydroperoxide-evidence-scoring.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('peroxide-ethyl-hydroperoxide-evidence-scoring.md', outDir), markdown);

console.log(markdown);
