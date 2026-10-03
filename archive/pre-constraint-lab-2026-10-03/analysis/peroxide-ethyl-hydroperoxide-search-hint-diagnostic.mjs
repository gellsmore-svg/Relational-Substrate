import { readFile, mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const sourceLockUrl = new URL('./out/peroxide-ethyl-hydroperoxide-source-lock-screen.json', import.meta.url);

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

const sourceLock = JSON.parse(await readFile(sourceLockUrl, 'utf8'));
const hint = sourceLock.supersededSearchIndexHints?.[0];

if (!hint) {
  throw new Error('missing superseded ethyl hydroperoxide search-index hint');
}

const sourceRatio = hint.hintedValues.VtransCm1 / hint.hintedValues.VcisCm1;
const passThreshold = 0.2;
const margin = passThreshold - sourceRatio;

const decision = {
  status: 'superseded-not-target-row',
  evidenceStatus:
    'not evidence: values came from a search-index preview and full PDF extraction shows they belong to HOOH, not HOOEt',
  reading:
    'the prior search-index hint has been superseded by source-locked HOOEt extraction from the repository-hosted Bitencourt et al. 2008 PDF',
  nextGate: 'use peroxide-ethyl-hydroperoxide-source-extraction.json and peroxide-ethyl-hydroperoxide-evidence-scoring.json',
};

const report = {
  source: 'peroxide-ethyl-hydroperoxide-search-hint-diagnostic.mjs',
  date: '2026-06-23',
  target: sourceLock.target,
  sourceLockArtifact: 'analysis/out/peroxide-ethyl-hydroperoxide-source-lock-screen.json',
  predeclarationHash: sourceLock.target.predeclarationHash,
  hintedValues: {
    VtransCm1: hint.hintedValues.VtransCm1,
    VcisCm1: hint.hintedValues.VcisCm1,
    transCisRatio: round(sourceRatio),
    ratioThreshold: passThreshold,
    margin: round(margin),
  },
  hintStatus: hint.status,
  decision,
};

const markdown = `# Ethyl Hydroperoxide Search-Hint Diagnostic

## Scope

This diagnostic evaluates a search-index preview hint for the predeclared ethyl hydroperoxide gate. It is not source extraction, not scoring, and not evidence.

Date: ${report.date}

## Hint

${table(
  ['Field', 'Value'],
  [
    ['Target', `${report.target.molecule} (${report.target.formula})`],
    ['Predeclaration hash', report.predeclarationHash],
    ['Vtrans hint', `${report.hintedValues.VtransCm1} cm-1`],
    ['Vcis hint', `${report.hintedValues.VcisCm1} cm-1`],
    ['Hinted trans/cis ratio', report.hintedValues.transCisRatio],
    ['Predeclared ratio threshold', report.hintedValues.ratioThreshold],
    ['Margin to threshold', report.hintedValues.margin],
    ['Hint target row', hint.targetRow],
    ['Hint status', report.hintStatus],
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
await writeFile(new URL('peroxide-ethyl-hydroperoxide-search-hint-diagnostic.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('peroxide-ethyl-hydroperoxide-search-hint-diagnostic.md', outDir), markdown);

console.log(markdown);
