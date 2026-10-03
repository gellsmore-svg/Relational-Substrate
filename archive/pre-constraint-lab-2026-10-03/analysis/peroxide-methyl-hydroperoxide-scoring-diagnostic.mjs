import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { clamp01 } from './molecule-model.mjs';

const outDir = new URL('./out/', import.meta.url);
const extractionUrl = new URL('./out/peroxide-methyl-hydroperoxide-source-extraction.json', import.meta.url);

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

function extractedValue(extraction, key) {
  const row = extraction.extractedValues.find((item) => item.key === key);
  if (!row) {
    throw new Error(`missing extracted value: ${key}`);
  }
  return row.valueCm1;
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
const repair = extraction.frozenRepair;
const equilibriumAlpha = extraction.extractedGeometry.values.H4O2O1C3Degrees;
const transBarrier = extractedValue(extraction, 'Vtrans_YH');
const cisBarrier = extractedValue(extraction, 'Vcis_YH');
const sourceBarrierRatio = transBarrier / cisBarrier;
const alphaGrid = extraction.torsionGrid.alphaDegrees;
const rows = alphaGrid.map((alpha) => alphaDiagnostic(alpha, equilibriumAlpha, repair));
const cisRow = rows.find((row) => row.alpha === 0);
const transRow = rows.find((row) => row.alpha === 180);
const predictedPenaltyRatio = transRow.predictedPenaltyIndex / cisRow.predictedPenaltyIndex;
const qualitativeOrderingPass = transRow.predictedPenaltyIndex < cisRow.predictedPenaltyIndex && transBarrier < cisBarrier;
const releaseActiveAtTrans = transRow.antiPlanarRelease > 0;
const cisCrowdingPreserved = cisRow.cisCrowding > 0.9 && cisRow.antiPlanarRelease === 0;

const decision = {
  status: qualitativeOrderingPass && releaseActiveAtTrans && cisCrowdingPreserved ? 'diagnostic-compatible' : 'diagnostic-fail',
  evidenceStatus:
    'diagnostic only: CH3OOH coordinate-consumption rule was created after source extraction, so this must not raise the evidence ledger or confidence score',
  reading:
    qualitativeOrderingPass
      ? 'the frozen anti-planar release direction is qualitatively compatible with the source ordering: trans OH rotation remains much less penalized than cis OH rotation'
      : 'the frozen anti-planar release direction does not reproduce the source ordering',
  nextGate:
    'a future evidence-counting target must freeze this CH3OOH diagnostic rule, or a more general substituted-peroxide rule, before extracting a new held-out molecule',
};

const report = {
  source: 'peroxide-methyl-hydroperoxide-scoring-diagnostic.mjs',
  date: '2026-06-23',
  target: extraction.reservedTarget,
  extractionArtifact: 'analysis/out/peroxide-methyl-hydroperoxide-source-extraction.json',
  frozenRepair: repair,
  sourceComparators: {
    transBarrierCm1: transBarrier,
    cisBarrierCm1: cisBarrier,
    sourceBarrierRatio: round(sourceBarrierRatio, 4),
  },
  diagnosticModel: {
    equilibriumAlphaDegrees: equilibriumAlpha,
    alphaGrid,
    formula:
      'penaltyIndex = 0.42 * effectiveTorsionDeviation + 0.58 * cisCrowding; effectiveTorsionDeviation = torsionDeviation * (1 - antiPlanarRelease * releaseStrength)',
    caveat: 'diagnostic rule introduced after source extraction; use only as compatibility/readiness check',
  },
  diagnosticChecks: {
    qualitativeOrderingPass,
    releaseActiveAtTrans,
    cisCrowdingPreserved,
    predictedPenaltyRatio: round(predictedPenaltyRatio, 4),
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

const markdown = `# Methyl Hydroperoxide Scoring Diagnostic

## Scope

This diagnostic consumes the CH3OOH source extraction and checks whether the frozen peroxide anti-planar release direction is qualitatively compatible with the extracted source ordering. It is not evidence-counting because the CH3OOH coordinate-consumption rule was not frozen before source extraction.

Date: ${report.date}

## Inputs

${table(
  ['Field', 'Value'],
  [
    ['Target', `${report.target.molecule} (${report.target.formula}; ${report.target.alias})`],
    ['Extraction artifact', report.extractionArtifact],
    ['Frozen release', `strength=${repair.releaseStrength}; onset=${repair.releaseOnsetDegrees}; span=${repair.releaseSpanDegrees}`],
    ['Equilibrium alpha', `${equilibriumAlpha} deg`],
    ['Trans OH barrier', `${transBarrier} cm-1`],
    ['Cis OH barrier', `${cisBarrier} cm-1`],
    ['Source trans/cis barrier ratio', report.sourceComparators.sourceBarrierRatio],
  ],
)}

## Diagnostic Formula

${table(
  ['Field', 'Value'],
  [
    ['Formula', report.diagnosticModel.formula],
    ['Caveat', report.diagnosticModel.caveat],
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
    ['Qualitative source ordering pass', report.diagnosticChecks.qualitativeOrderingPass ? 'yes' : 'no'],
    ['Release active at trans', report.diagnosticChecks.releaseActiveAtTrans ? 'yes' : 'no'],
    ['Cis crowding preserved', report.diagnosticChecks.cisCrowdingPreserved ? 'yes' : 'no'],
    ['Predicted trans/cis penalty ratio', report.diagnosticChecks.predictedPenaltyRatio],
  ],
)}

## Decision

${table(
  ['Field', 'Value'],
  [
    ['Status', decision.status],
    ['Evidence status', decision.evidenceStatus],
    ['Reading', decision.reading],
    ['Next gate', decision.nextGate],
  ],
)}
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('peroxide-methyl-hydroperoxide-scoring-diagnostic.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('peroxide-methyl-hydroperoxide-scoring-diagnostic.md', outDir), markdown);

console.log(markdown);
