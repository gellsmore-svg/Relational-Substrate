import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const structuralRows = [
  {
    material: 'akermanite / melilite prototype',
    formula: 'Ca2MgSi2O7 / melilite group',
    opticalRole: 'melilite scaffold calibration class',
    sourcedStructure:
      'Melilite-type tetragonal P-421m structure; akermanite represents the prototype class; contains isolated Si2O7 or related groups and interleaved tetrahedral and CaO8 polyhedral layers.',
    sourceUrl: 'https://aflow.org/p/A2BC7D2_tP24_113_e_a_cef_e-001/A2BC7D2_tP24_113_e_a_cef_e-001.pdf',
    sourceStatus: 'prototype/source-backed descriptor',
    caEnvironment: 'CaO8 polyhedral layer between tetrahedral layers',
    silicateUnit: 'isolated Si2O7 or related melilite tetrahedral sheet units',
    gateClass: 'melilite sheet scaffold',
  },
  {
    material: 'rankinite',
    formula: 'Ca3Si2O7',
    opticalRole: 'Ca3Si2O7 transfer failure',
    sourcedStructure:
      'Monoclinic P21/a rankinite; Ca coordination polyhedra form sheets parallel to (010), with Si2O7 groups inserted between them.',
    sourceUrl: 'https://www.jstage.jst.go.jp/article/minerj/8/4/8_4_240/_article',
    sourceStatus: 'primary abstract-backed descriptor',
    caEnvironment: 'Ca coordination-polyhedra sheets',
    silicateUnit: 'inserted Si2O7 groups',
    gateClass: 'Ca-polyhedra sheet plus inserted disilicate',
  },
  {
    material: 'kilchoanite',
    formula: 'Ca3Si2O7 ideal; Ca6(SiO4)(Si3O10) structural description',
    opticalRole: 'Ca3Si2O7 paired-polymorph transfer failure',
    sourcedStructure:
      'Handbook lists kilchoanite as dimorphous with rankinite and cites the crystal structure as Ca6(SiO4)(Si3O10); later single-crystal work on manganoan kilchoanite is isostructural with kilchoanite and reports multiple Ca/Mn sites plus Si-O-Si angle systematics.',
    sourceUrl:
      'https://handbookofmineralogy.org/pdfs/kilchoanite.pdf; https://www.cambridge.org/core/journals/mineralogical-magazine/article/abs/crystal-structure-of-manganoan-kilchoanite-ca233mn067si2o7-a-sitepreference-rule-for-the-substitution-of-mn-for-ca/CAB83AF5CCB4A460348E537CF4252C06',
    sourceStatus: 'Handbook plus primary abstract-backed descriptor',
    caEnvironment: 'multiple Ca sites; Ca/Mn site-preference work reports four octahedral sites in manganoan analogue',
    silicateUnit: 'SiO4 plus Si3O10 structural description, not a simple rankinite-like inserted Si2O7 label',
    gateClass: 'Ca3Si2O7 polymorph / mixed silicate-unit scaffold',
  },
];

const opticalFindings = [
  {
    finding: 'melilite Ca scaffold succeeds locally',
    evidence: 'gehlenite and akermanite split-Ca residuals are near zero after post-failure repair',
    structuralReading: 'CaO8 layer embedded in melilite tetrahedral sheet scaffold is a local context, not a transferable scalar',
  },
  {
    finding: 'rankinite and kilchoanite reject melilite Ca uplift',
    evidence: 'rankinite and kilchoanite split-Ca residuals are both about -0.028 RI units',
    structuralReading: 'Ca3Si2O7 polymorphs need their own gate even when Ca/O and formula are close',
  },
  {
    finding: 'formula is too coarse as topology',
    evidence: 'rankinite and kilchoanite have the same ideal formula and similar RI, but sourced structural descriptions differ',
    structuralReading: 'use silicate-unit connectivity and Ca-polyhedra environment rather than formula labels alone',
  },
];

const promotedDescriptorCandidates = [
  {
    descriptor: 'Ca polyhedral environment class',
    sourceBasis: 'melilite CaO8 layer vs rankinite Ca-polyhedra sheets vs kilchoanite multiple Ca sites',
    status: 'promote as categorical gate candidate',
  },
  {
    descriptor: 'silicate-unit connectivity class',
    sourceBasis: 'melilite Si2O7/related tetrahedral sheet units; rankinite inserted Si2O7; kilchoanite SiO4 + Si3O10 structural description',
    status: 'promote as categorical gate candidate',
  },
  {
    descriptor: 'bridge oxygen overbonding / Si-O-Si angle class',
    sourceBasis: 'kilchoanite structural work reports Si-O-Si angle systematics with bridging oxygen coordination',
    status: 'source more exact values before numeric use',
  },
];

const rejectedDescriptorCandidates = [
  {
    descriptor: 'ideal formula class',
    reason: 'rankinite and kilchoanite share Ca3Si2O7 but have distinct structural descriptions and similar optical response',
  },
  {
    descriptor: 'Ca/O scalar',
    reason: 'Ca3Si2O7 rows have higher Ca/O yet are overpredicted by melilite-derived Ca scaffold',
  },
  {
    descriptor: 'oxygen-volume scalar alone',
    reason: 'oxygen volume does not distinguish residual sign cleanly across melilite and Ca3Si2O7 rows',
  },
];

const report = {
  source: 'ri-structural-gate-source-diagnostic.mjs',
  status: 'source-backed structural-gate diagnostic; no optical fitting',
  structuralRows,
  opticalFindings,
  promotedDescriptorCandidates,
  rejectedDescriptorCandidates,
};

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const markdown = `# RI Structural Gate Source Diagnostic

## Scope

This diagnostic sources the structural side of the Ca-scaffold gate after the rankinite/kilchoanite transfer failures. It does not score a new optical target and does not fit a repair term.

## Structural Rows

${table(
  ['Material / class', 'Formula', 'Gate class', 'Ca environment', 'Silicate unit', 'Source status'],
  structuralRows.map((row) => [
    row.material,
    row.formula,
    row.gateClass,
    row.caEnvironment,
    row.silicateUnit,
    row.sourceStatus,
  ])
)}

## Sources

${table(
  ['Material / class', 'Source URL'],
  structuralRows.map((row) => [row.material, row.sourceUrl])
)}

## Optical Findings Re-read Structurally

${table(
  ['Finding', 'Evidence', 'Structural reading'],
  opticalFindings.map((row) => [row.finding, row.evidence, row.structuralReading])
)}

## Promoted Descriptor Candidates

${table(
  ['Descriptor', 'Source basis', 'Status'],
  promotedDescriptorCandidates.map((row) => [row.descriptor, row.sourceBasis, row.status])
)}

## Rejected Descriptor Candidates

${table(
  ['Descriptor', 'Reason'],
  rejectedDescriptorCandidates.map((row) => [row.descriptor, row.reason])
)}

## Reading

The structural gate should not be written as a formula label. Rankinite and kilchoanite share the ideal formula Ca3Si2O7 and have similar optical response, but the sourced structural descriptions are not equivalent: rankinite is described as Si2O7 groups inserted between Ca-polyhedra sheets, while kilchoanite is structurally cited as Ca6(SiO4)(Si3O10).

The immediate safe gate is categorical and structural:

1. melilite CaO8 / tetrahedral-sheet scaffold;
2. rankinite Ca-polyhedra sheet plus inserted disilicate scaffold;
3. kilchoanite mixed silicate-unit scaffold.

For the next quantitative step, source exact Si-O-Si bridge angles, bridge oxygen coordination, and Ca coordination/site multiplicity before attempting a numeric topology coefficient.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-structural-gate-source-diagnostic.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('ri-structural-gate-source-diagnostic.md', outDir), markdown);

console.log(markdown);
