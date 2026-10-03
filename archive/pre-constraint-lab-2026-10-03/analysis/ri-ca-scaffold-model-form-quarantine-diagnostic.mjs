import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const evidenceRows = [
  {
    material: 'hardystonite',
    formula: 'Ca2ZnSi2O7',
    familyContext: 'same melilite topology with Zn/d10 T1 buffer',
    status: 'failed split-Ca transfer',
    reading: 'same-topology success is not automatic once T1 cation chemistry changes',
  },
  {
    material: 'rankinite',
    formula: 'Ca3Si2O7',
    familyContext: 'pure Ca-Si-O non-melilite Ca3Si2O7 polymorph',
    status: 'failed split-Ca transfer',
    reading: 'scalar Ca/O uplift overpredicts outside melilite',
  },
  {
    material: 'kilchoanite',
    formula: 'Ca3Si2O7',
    familyContext: 'pure Ca-Si-O paired Ca3Si2O7 polymorph',
    status: 'failed split-Ca transfer',
    reading: 'rankinite miss is not an isolated polymorph anomaly',
  },
  {
    material: 'larnite',
    formula: 'Ca2SiO4',
    familyContext: 'pure Ca-Si-O compact/lower-coordinate orthosilicate',
    status: 'failed split-Ca transfer; baseline passed locally',
    reading: 'baseline pass is local control-row success, not model validation',
  },
  {
    material: 'merwinite',
    formula: 'Ca3Mg(SiO4)2',
    familyContext: 'Mg-bearing Ca-silicate-family density-control contrast',
    status: 'baseline failed; split-Ca and split-Ca/Mg passed',
    reading: 'pass is not promotable because Mg chemistry is confounded',
  },
  {
    material: 'spurrite',
    formula: 'Ca5(SiO4)2(CO3)',
    familyContext: 'Mg-removed but carbonate-introduced Ca-rich control contrast',
    status: 'all frozen families failed',
    reading: 'carbonate prevents clean Ca-Si-O falsification, but merwinite pass remains confounded',
  },
  {
    material: 'wollastonite/pseudowollastonite/hatrurite',
    formula: 'CaSiO3 / Ca3SiO5',
    familyContext: 'candidate pure Ca-Si-O continuation rows',
    status: 'not scored',
    reading: 'source lock is exhausted under current gate; do not use broad/secondary rows',
  },
];

const familyStatus = [
  {
    family: 'baseline density + Al/O + Al-comp response',
    quarantineStatus: 'reference diagnostic only',
    reason:
      'passes silica/sodium/albite-family controls and larnite locally, but misses rankinite, kilchoanite, merwinite, and spurrite in the later chain',
  },
  {
    family: 'split Ca scaffold family',
    quarantineStatus: 'quarantined outside its source domain',
    reason:
      'calibrated as post-failure Ca scaffold response, then failed hardystonite, rankinite, kilchoanite, larnite, and spurrite; merwinite pass is Mg-confounded',
  },
  {
    family: 'split Ca/Mg scaffold family',
    quarantineStatus: 'quarantined outside its source domain',
    reason:
      'inherits split-Ca failures and adds Mg/O calibration debt; merwinite pass cannot promote it and spurrite fails with Mg/O = 0',
  },
];

const allowedUses = [
  {
    use: 'historical reference rows',
    status: 'allowed',
    boundary: 'may be reported to explain how the chain reached the current failure state',
  },
  {
    use: 'fresh held-out prediction',
    status: 'blocked',
    boundary: 'blocked until a new model form is predeclared before a source-locked target is scored',
  },
  {
    use: 'programme-level material RI support',
    status: 'blocked',
    boundary: 'blocked because no active family has cleared a clean source-locked held-out target after the topology failures',
  },
  {
    use: 'descriptor design',
    status: 'allowed',
    boundary: 'may motivate structural descriptors such as Ca coordination, Ca-O distance, T-site field/polarizability, and connectivity class',
  },
];

const reopenConditions = [
  'predeclare a new model form before scoring another target',
  'source-lock a clean held-out target with optical constants, measured density, and paired CIF before prediction',
  'classify the target under frozen CIF/structural gates before optical scoring',
  'do not reuse rankinite, kilchoanite, larnite, merwinite, or spurrite as fresh validation',
  'do not treat Mg-bearing or carbonate-bearing rows as pure Ca-Si-O validation',
  'keep any density/Lorentz-Lorenz comparator labelled as conventional control evidence, not substrate-specific support',
];

const report = {
  source: 'ri-ca-scaffold-model-form-quarantine-diagnostic.mjs',
  date: '2026-05-17',
  status: 'Ca-scaffold RI families quarantined outside source domain; no model promoted',
  evidenceRows,
  familyStatus,
  allowedUses,
  reopenConditions,
  decision:
    'do not score further material-RI targets under baseline, split-Ca, or split-Ca/Mg as candidate repairs; use them only as reference diagnostics until a new source-locked model form is predeclared',
};

const markdown = `# RI Ca-Scaffold Model-Form Quarantine Diagnostic

## Scope

This diagnostic records the model-form boundary after the post-merwinite branch and pure Ca-Si-O source-exhaustion screen. It does not score a target, does not fit a coefficient, and does not promote a new RI repair. Its purpose is to prevent the failed Ca-scaffold families from being reused as active prediction families outside their source domain.

Date: ${report.date}

## Evidence Ledger

${table(
  ['Material', 'Formula', 'Family context', 'Status', 'Reading'],
  evidenceRows.map((row) => [
    row.material,
    row.formula,
    row.familyContext,
    row.status,
    row.reading,
  ]),
)}

## Family Status

${table(
  ['Family', 'Quarantine status', 'Reason'],
  familyStatus.map((row) => [row.family, row.quarantineStatus, row.reason]),
)}

## Allowed Uses

${table(
  ['Use', 'Status', 'Boundary'],
  allowedUses.map((row) => [row.use, row.status, row.boundary]),
)}

## Reopen Conditions

${reopenConditions.map((condition) => `- ${condition}`).join('\n')}

## Decision

${report.decision}

Status: ${report.status}

## Reading

The active Ca-scaffold repair programme is now model-form blocked, not merely target-blocked. The split-Ca and split-Ca/Mg families are useful forensic diagnostics, but they should not be used as candidate repairs for another material-RI score. The baseline density family is also only a reference comparator after the later failures.

The next legitimate RI step is not another score with these families. It is either a predeclared new model form with structural descriptors fixed before target scoring, or a primary-source unlock for a clean held-out target followed by pre-score gate classification.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-ca-scaffold-model-form-quarantine-diagnostic.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('ri-ca-scaffold-model-form-quarantine-diagnostic.md', outDir), markdown);

console.log(markdown);
