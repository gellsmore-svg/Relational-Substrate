// Cross-track evidence ledger (process recommendation #7).
//
// Consolidates the project's evidence accounting into one queryable place and
// makes it auditable: it reads the authoritative computed accounting from the
// regenerated benchmark summary (analysis/out/external-benchmark-summary.json),
// reads the DECLARED headline metrics from docs/research-task-map.md, and then
//   1. lists every evidence line (core vs orientation-only) with its checks,
//      grammar variables, and conventional comparator coverage;
//   2. mechanically enforces the standing guardrails (EM-02..EM-17 collapse to
//      one electromagnetic line; boundary phase is orientation-only and never
//      core; the declared independent-line count matches the itemized lines);
//   3. flags DRIFT between the declared doc numbers and the freshly computed
//      numbers, so reviewers reconcile rather than trust a stale figure.
//
// This invents no evidence and computes no new confidence score. It only
// structures and cross-checks numbers the project already produces/declares.
// Source of truth remains external-benchmark-summary.mjs and the task map;
// run `npm run reports` first so the summary JSON is current.

import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const docsDir = new URL('../docs/', import.meta.url);

const r2 = (v) => (v == null ? null : Number(Number(v).toFixed(2)));

async function loadSummary() {
  const url = new URL('external-benchmark-summary.json', outDir);
  try {
    return JSON.parse(await readFile(url, 'utf8'));
  } catch {
    throw new Error('analysis/out/external-benchmark-summary.json missing — run `npm run reports` first.');
  }
}

// Parse the "Current Status" metric table out of the task map (the declared,
// human-curated headline numbers). Returns a map of normalized label -> number.
async function loadDeclared() {
  const text = await readFile(new URL('research-task-map.md', docsDir), 'utf8');
  const declared = {};
  for (const line of text.split('\n')) {
    const m = line.match(/^\|\s*([^|]+?)\s*\|\s*([0-9.]+)(?:\/10)?\s*\|\s*$/);
    if (!m) continue;
    const key = m[1].trim().toLowerCase();
    const val = Number(m[2]);
    if (!Number.isNaN(val)) declared[key] = val;
  }
  return declared;
}

const summary = await loadSummary();
const declared = await loadDeclared();
const conf = summary.confidence || {};

// --- evidence lines --------------------------------------------------------
const lines = (summary.evidenceLineSummaries || []).map((l) => ({
  evidenceLine: l.evidenceLine,
  core: !l.orientationOnly,
  orientationOnly: !!l.orientationOnly,
  benchmarkCount: l.benchmarkCount,
  checks: `${l.checksPassed}/${l.checksTotal}`,
  checksComplete: l.checksPassed === l.checksTotal,
  grammarVariables: l.variables,
  benchmarks: l.benchmarks,
  limitation: l.limitation,
}));
const coreLines = lines.filter((l) => l.core);
const orientationLines = lines.filter((l) => l.orientationOnly);

// --- declared vs computed headline metrics (drift check) -------------------
// declared-doc label -> computed field in the summary confidence object
const metricMap = [
  ['inferential convergence', 'updatedInferentialConvergenceOutOf10'],
  ['cross-domain equivalence', 'crossDomainEquivalenceOutOf10'],
  ['evidence independence', 'evidenceIndependenceOutOf10'],
  ['unification thesis support', 'unificationThesisSupportOutOf10'],
  ['grammar internal coherence', 'updatedInternalCoherenceOutOf10'],
];
const metrics = metricMap.map(([docKey, confKey]) => {
  const declaredVal = declared[docKey] ?? null;
  const computedVal = conf[confKey] ?? null;
  const drift = declaredVal != null && computedVal != null ? r2(declaredVal - computedVal) : null;
  return { metric: docKey, declaredDoc: declaredVal, computed: computedVal, drift };
});
const drifted = metrics.filter((m) => m.drift != null && m.drift !== 0);

// counts
const declaredCore = declared['core independent evidence lines'] ?? null;
const declaredOrientation = declared['orientation-only evidence lines'] ?? null;

// --- guardrail checks (mechanical) -----------------------------------------
const warnings = [];
const checks = [];
const record = (name, ok, detail) => {
  checks.push({ check: name, ok, detail });
  if (!ok) warnings.push(`${name}: ${detail}`);
};

record(
  'independent-line count matches summary',
  summary.independentEvidenceLines === coreLines.length,
  `summary.independentEvidenceLines=${summary.independentEvidenceLines}, itemized core lines=${coreLines.length}`,
);
record(
  'declared core-line count matches computed',
  declaredCore == null || declaredCore === summary.independentEvidenceLines,
  `task-map declares ${declaredCore}, summary computes ${summary.independentEvidenceLines}`,
);
record(
  'orientation line count matches',
  (declaredOrientation == null || declaredOrientation === orientationLines.length) &&
    summary.orientationEvidenceLines === orientationLines.length,
  `declared=${declaredOrientation}, summary=${summary.orientationEvidenceLines}, itemized=${orientationLines.length}`,
);
const emLines = coreLines.filter((l) => /electromagnetic|electrostatic|\bEM\b/i.test(l.evidenceLine));
record(
  'EM collapses to a single core line (EM-02..EM-17 not double-counted)',
  emLines.length <= 1,
  `found ${emLines.length} EM core lines: ${emLines.map((l) => l.evidenceLine).join(', ')}`,
);
const boundaryAsCore = coreLines.find((l) => /boundary/i.test(l.evidenceLine));
record(
  'boundary phase is orientation-only, never core',
  !boundaryAsCore,
  boundaryAsCore ? `boundary line counted as core: ${boundaryAsCore.evidenceLine}` : 'ok',
);

// rec #2 tie-in: material/optical benchmarks should carry a conventional comparator
const materialish = (summary.benchmarks || []).filter((b) =>
  /material|optical|refractive|silicate|roughness|interface/i.test(`${b.domain} ${b.label} ${b.evidenceLine}`),
);
const missingComparator = materialish.filter((b) => !b.conventionalComparator || b.conventionalComparator === 'n/a');
record(
  'material/optical benchmarks declare a conventional comparator',
  missingComparator.length === 0,
  `${missingComparator.length} of ${materialish.length} material/optical benchmarks lack a conventional comparator: ${missingComparator
    .map((b) => b.label)
    .slice(0, 6)
    .join('; ')}`,
);

// --- assemble + write ------------------------------------------------------
const ledger = {
  generated: new Date().toISOString(),
  scope: 'Consolidated, auditable cross-track evidence accounting. Invents nothing; structures + cross-checks the existing computed and declared numbers. Not physics validation.',
  sources: {
    computed: 'analysis/out/external-benchmark-summary.json (regenerate via `npm run reports`)',
    declared: 'docs/research-task-map.md Current Status table',
    guardrails: '.restart.md / research-task-map.md Guardrails',
  },
  programmeStatus: summary.status,
  blockingGate: 'measured material refractive-index challenge unresolved (see research-task-map.md)',
  evidenceLineCounts: {
    coreComputed: summary.independentEvidenceLines,
    orientationComputed: summary.orientationEvidenceLines,
    coreDeclaredDoc: declaredCore,
    orientationDeclaredDoc: declaredOrientation,
  },
  headlineMetrics: metrics,
  drift: drifted,
  evidenceLines: lines,
  guardrailChecks: checks,
  warnings,
};

await mkdir(outDir, { recursive: true });
await writeFile(new URL('evidence-ledger.json', outDir), JSON.stringify(ledger, null, 2));

const tbl = (rows, cols) => rows.map((r) => `| ${cols.map((c) => (r[c] == null ? '' : r[c])).join(' | ')} |`).join('\n');

const markdown = `# Cross-Track Evidence Ledger

**Scope.** One consolidated, auditable view of the evidence accounting. It
**invents no evidence and computes no new confidence score** — it structures
and cross-checks the numbers the project already produces (the regenerated
benchmark summary) and declares (the task map). Not physics validation.

Generated: ${ledger.generated}
Computed source: \`analysis/out/external-benchmark-summary.json\` · Declared source: \`docs/research-task-map.md\`

Programme status: ${summary.status}
Blocking gate: ${ledger.blockingGate}

## Headline metrics — declared (doc) vs computed (regenerated)

${drifted.length ? `> ⚠️ **${drifted.length} metric(s) drift between the task map and the freshly computed summary.** Reconcile before citing a headline number.` : '> No drift between declared and computed headline metrics.'}

| Metric | Declared (task map) | Computed (summary) | Drift (declared − computed) |
|---|---:|---:|---:|
${tbl(metrics, ['metric', 'declaredDoc', 'computed', 'drift'])}

Evidence lines: core computed **${summary.independentEvidenceLines}** (declared ${declaredCore}); orientation-only **${summary.orientationEvidenceLines}** (declared ${declaredOrientation}).

## Evidence lines

| Evidence line | Role | Benchmarks | Checks | Grammar variables | Limitation |
|---|---|---:|---:|---|---|
${tbl(
  lines.map((l) => ({ ...l, role: l.orientationOnly ? 'orientation-only' : 'core' })),
  ['evidenceLine', 'role', 'benchmarkCount', 'checks', 'grammarVariables', 'limitation'],
)}

## Guardrail checks

${checks.map((c) => `- ${c.ok ? '✓' : '✗'} ${c.check}${c.ok ? '' : ` — ${c.detail}`}`).join('\n')}

${warnings.length ? `## Warnings\n\n${warnings.map((w) => `- ⚠️ ${w}`).join('\n')}\n` : ''}
## Reading

This ledger is for defending or challenging the headline numbers during
review. Drift rows mean a cited number is stale somewhere and must be
reconciled — it does **not** itself change any number. The guardrail checks
mechanically enforce the standing rules (one electromagnetic line; boundary
phase orientation-only; declared counts match computed). It deliberately makes
no claim about the substrate.
`;

await writeFile(new URL('evidence-ledger-summary.md', outDir), markdown);

console.log('Cross-track evidence ledger');
console.log(`Core lines: ${summary.independentEvidenceLines} | orientation: ${summary.orientationEvidenceLines}`);
console.log(`Guardrail checks: ${checks.filter((c) => c.ok).length}/${checks.length} ok`);
if (drifted.length) {
  console.log(`DRIFT (declared vs computed):`);
  for (const d of drifted) console.log(`  - ${d.metric}: doc ${d.declaredDoc} vs computed ${d.computed} (Δ ${d.drift})`);
}
if (warnings.length) {
  console.log('WARNINGS:');
  for (const w of warnings) console.log(`  - ${w}`);
}
console.log(`Wrote ${new URL('evidence-ledger-summary.md', outDir).pathname}`);
