import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const gateRequirements = [
  'pure Ca-Si-O composition with no Mg, carbonate, hydroxyl, alkali, Fe/Mn substitution, or cement-phase ambiguity',
  'source-anchored optical constants, preferably alpha/beta/gamma, with one material/polytype identity',
  'source-anchored measured density for the same material/polytype identity',
  'paired CIF with coordinates for the same material/polytype identity',
  'pre-score CIF gate classification before optical prediction',
  'no use of broad pooled optical ranges or secondary aggregate rows as held-out targets',
];

const candidates = [
  {
    material: 'wollastonite',
    formula: 'CaSiO3',
    class: 'pure Ca-Si-O chain silicate',
    opticalStatus: 'Handbook row is broad and not polytype-specific',
    densityStatus: 'Handbook D(meas.) = 2.86-3.09 is broad and not polytype-specific',
    cifStatus: 'COD rows exist for WO1T/triclinic and Wollastonite-2M/parawollastonite',
    decision: 'defer',
    reason:
      'The CIF side is strong, but optical constants and measured density are not locked to a single polytype.',
    nextUnlock:
      'Find a primary optical/density row that explicitly names Wollastonite-2M/parawollastonite, WO1T, 1A, 3A, 4A, 5A, or 7A.',
  },
  {
    material: 'wollastonite-1A / 2M / 3A-4A-5A-7A secondary rows',
    formula: 'CaSiO3',
    class: 'pure Ca-Si-O wollastonite polytype pages',
    opticalStatus:
      'Webmineral-style rows list alpha = 1.615-1.646, beta = 1.627-1.659, gamma = 1.629-1.662 for multiple polytype pages',
    densityStatus: 'density 2.8-2.9 average 2.84 is broad and repeated across pages',
    cifStatus: 'structure references exist on pages but optical/density rows are not primary-source matched',
    decision: 'reject for scoring',
    reason:
      'The rows are secondary aggregate data and appear repeated across polytype pages, so they do not unlock a held-out prediction target.',
    nextUnlock: 'Trace the listed optical-property source to a primary table and verify polytype identity.',
  },
  {
    material: 'hatrurite',
    formula: 'Ca3SiO5',
    class: 'pure Ca-Si-O high-Ca tricalcium oxy silicate',
    opticalStatus: 'Handbook/RRUFF row reports n = n.d.; only birefringence approximately 0.006',
    densityStatus: 'D(meas.) = n.d. and D(calc.) = n.d. in the Handbook/RRUFF row',
    cifStatus: 'structure rows exist elsewhere, but optical and density fields fail first',
    decision: 'reject for current gate',
    reason: 'Attractive chemistry, but the source row lacks the optical constants and density needed for RI scoring.',
    nextUnlock: 'Find an independent measured optical/density row for a named hatrurite or C3S polymorph.',
  },
  {
    material: 'pseudowollastonite',
    formula: 'CaSiO3',
    class: 'pure Ca-Si-O high-temperature CaSiO3 polymorph',
    opticalStatus: 'no source-grade alpha/beta/gamma row found in the quick screen',
    densityStatus: 'no matched measured-density row found in the quick screen',
    cifStatus: 'not selected',
    decision: 'defer',
    reason:
      'Chemistry is attractive, but the search surfaced high-temperature structural/spectroscopy context rather than a source-locked optical target.',
    nextUnlock: 'Find a primary optical-constants table for pseudowollastonite with density and a paired structure row.',
  },
  {
    material: 'larnite',
    formula: 'Ca2SiO4',
    class: 'pure Ca-Si-O orthosilicate',
    opticalStatus: 'already source-anchored and scored',
    densityStatus: 'already source-anchored and scored',
    cifStatus: 'COD 9017424 already used',
    decision: 'exhausted',
    reason: 'Already classified before scoring and then scored under frozen gates.',
    nextUnlock: 'Do not reuse as a fresh held-out target.',
  },
  {
    material: 'rankinite and kilchoanite',
    formula: 'Ca3Si2O7',
    class: 'pure Ca-Si-O paired polymorphs',
    opticalStatus: 'already source-anchored and scored',
    densityStatus: 'already source-anchored and scored',
    cifStatus: 'already used in topology-transfer sequence',
    decision: 'exhausted',
    reason: 'Already used to expose scalar Ca-scaffold non-transfer outside melilite.',
    nextUnlock: 'Do not reuse as fresh held-out targets.',
  },
];

const viable = candidates.filter((candidate) => candidate.decision === 'reserve');

const report = {
  source: 'ri-pure-ca-si-o-source-exhaustion-screen.mjs',
  date: '2026-05-17',
  status: 'no new pure Ca-Si-O target reserved; source lock exhausted under current gate',
  gateRequirements,
  candidates,
  viable,
  decision:
    'do not score another target until a polytype-specific wollastonite/pseudowollastonite optical-density row or another pure Ca-Si-O source-locked row is found',
};

const markdown = `# RI Pure Ca-Silicate Source Exhaustion Screen

## Scope

This screen records the post-spurrite search state for a clean pure Ca-Si-O held-out target. It does not score a prediction, does not fit or promote a model, and does not relax the source rules after the spurrite carbonate-confounded failure.

Date: ${report.date}

## Gate Requirements

${gateRequirements.map((requirement) => `- ${requirement}`).join('\n')}

## Candidate Screen

${table(
  [
    'Material',
    'Formula',
    'Class',
    'Optical status',
    'Density status',
    'CIF status',
    'Decision',
    'Reason',
  ],
  candidates.map((row) => [
    row.material,
    row.formula,
    row.class,
    row.opticalStatus,
    row.densityStatus,
    row.cifStatus,
    row.decision,
    row.reason,
  ]),
)}

## Unlock Conditions

${table(
  ['Material', 'Next unlock'],
  candidates
    .filter((row) => row.nextUnlock)
    .map((row) => [row.material, row.nextUnlock]),
)}

## Decision

${report.decision}

Status: ${report.status}

## Reading

The clean Ca-Si-O branch is source-blocked, not model-ready. Wollastonite remains the best chemistry target, but the available optical and density rows are too broad or too secondary to serve as a held-out prediction target. Hatrurite remains chemically attractive but lacks usable optical and density fields. Pseudowollastonite needs a source-grade optical/density row before it can enter the chain.

Do not infer that no pure Ca-Si-O target exists in the literature. Infer only that no new target is reserved under the current source-lock rules in this screen. The next productive artifact should either unlock a primary polytype-specific optical/density source or move to a model-form diagnostic that explicitly treats the Ca-scaffold family as failed outside its source domain.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-pure-ca-si-o-source-exhaustion-screen.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('ri-pure-ca-si-o-source-exhaustion-screen.md', outDir), markdown);

console.log(markdown);
