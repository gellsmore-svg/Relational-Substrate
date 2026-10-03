import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const rows = [
  {
    material: 'melilite prototype / akermanite class',
    formula: 'Ca2MgSi2O7',
    gateClass: 'melilite CaO8 tetrahedral-sheet scaffold',
    caCoordination: '8',
    caBondMetric: 'CaO8 polyhedral layer; exact Ca-O distances not extracted in current source pass',
    silicateUnit: 'isolated Si2O7 or related melilite tetrahedral sheet units',
    bridgeAngleMetric: 'not source-extracted; source notes T-O-T bridge-angle relation to spectral bands',
    numericReadiness: 'coordination-class ready; angle not ready',
    sourceStatus: 'source-backed class descriptor, incomplete numeric geometry',
    sourceUrls: [
      'https://aflow.org/p/A2BC7D2_tP24_113_e_a_cef_e-001/A2BC7D2_tP24_113_e_a_cef_e-001.pdf',
      'https://pmc.ncbi.nlm.nih.gov/articles/PMC6644492/',
    ],
  },
  {
    material: 'rankinite',
    formula: 'Ca3Si2O7',
    gateClass: 'Ca-polyhedra sheet plus inserted disilicate',
    caCoordination: '7 in older structure summary; newer abstract gives Ca-polyhedra sheets',
    caBondMetric: 'Ca-O 2.25-2.90 A in older structure summary',
    silicateUnit: 'arrays/inserted Si2O7 groups',
    bridgeAngleMetric: 'not source-extracted; newer abstract says bridge Si-O bonds are longer than nonbridge bonds',
    numericReadiness: 'Ca coordination/bond-range ready; bridge angle not ready',
    sourceStatus: 'source-backed numeric Ca environment, incomplete bridge geometry',
    sourceUrls: [
      'https://pubs.acs.org/doi/10.1021/ic020647f',
      'https://www.jstage.jst.go.jp/article/minerj/8/4/8_4_240/_article',
    ],
  },
  {
    material: 'kilchoanite / manganoan kilchoanite analogue',
    formula: 'Ca3Si2O7 ideal; Ca6(SiO4)(Si3O10) structural formula',
    gateClass: 'mixed silicate-unit scaffold with multiple Ca sites',
    caCoordination: 'manganoan analogue reports four octahedral M sites',
    caBondMetric: '<M1-O> 2.538 A; <M2-O> 2.380 A; <M3-O> 2.307 A; <M4-O> 2.346 A in manganoan analogue',
    silicateUnit: 'SiO4 plus Si3O10; later Birkhin refinement describes strongly folded trisilicate units interwoven with CaO6/CaO8 polyhedra',
    bridgeAngleMetric:
      'not exact for pure kilchoanite in current pass; source says Si-O-Si angles decrease as bridging oxygen coordination increases',
    numericReadiness: 'M-site distance ready for analogue; pure-kilchoanite bridge angle not ready',
    sourceStatus: 'source-backed analogue numeric M-site geometry, incomplete pure-phase bridge geometry',
    sourceUrls: [
      'https://handbookofmineralogy.org/pdfs/kilchoanite.pdf',
      'https://www.cambridge.org/core/journals/mineralogical-magazine/article/abs/crystal-structure-of-manganoan-kilchoanite-ca233mn067si2o7-a-sitepreference-rule-for-the-substitution-of-mn-for-ca/CAB83AF5CCB4A460348E537CF4252C06',
      'https://www.researchgate.net/publication/257654715_Trabzonite_Ca4Si3O9OHOH_Crystal_Structure_Revised_Formula_New_Occurrence_and_Relation_to_Killalaite',
    ],
  },
];

const descriptorReadiness = [
  {
    descriptor: 'Ca coordination class',
    status: 'ready as categorical descriptor',
    reason: 'melilite is source-described with Ca in 8-fold coordination; rankinite has 7-O Ca summary; kilchoanite analogue has multiple octahedral M sites',
  },
  {
    descriptor: 'Ca bond-length range / mean M-O distances',
    status: 'partly ready',
    reason: 'rankinite and manganoan kilchoanite have numeric ranges/means; melilite exact Ca-O distances still need a comparable source extraction',
  },
  {
    descriptor: 'silicate-unit connectivity',
    status: 'ready as categorical descriptor',
    reason: 'melilite sheet units, rankinite inserted Si2O7, and kilchoanite SiO4 + Si3O10 are source-distinguished',
  },
  {
    descriptor: 'Si-O-Si bridge angle',
    status: 'not ready for numeric modelling',
    reason: 'sources support relevance and directionality, but exact comparable angles were not extracted for all three gate classes',
  },
  {
    descriptor: 'bridge oxygen coordination / overbonding',
    status: 'promising but not ready',
    reason: 'kilchoanite analogue source links higher bridge-O coordination to smaller Si-O-Si angle, but comparable values are missing for melilite and rankinite',
  },
];

const modellingBoundary = {
  allowedNow: [
    'categorical Ca coordination class',
    'categorical silicate-unit connectivity class',
    'source-status flags separating exact numeric values from analogue or abstract-level descriptors',
  ],
  blockedNow: [
    'numeric Si-O-Si angle coefficient',
    'numeric bridge oxygen coordination coefficient',
    'continuous Ca bond-length correction across melilite/rankinite/kilchoanite',
  ],
  nextSourceNeed:
    'Extract comparable structure tables or CIF-derived values for melilite, rankinite, and kilchoanite before fitting any numeric topology coefficient.',
};

const report = {
  source: 'ri-structural-numeric-readiness-diagnostic.mjs',
  status: 'numeric structural descriptor readiness; no optical fit',
  rows,
  descriptorReadiness,
  modellingBoundary,
};

function table(headers, bodyRows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...bodyRows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const markdown = `# RI Structural Numeric-Readiness Diagnostic

## Scope

This diagnostic asks which structural-gate descriptors are numeric-ready after the first source pass. It does not score a new optical target and does not fit a repair term.

## Rows

${table(
  ['Material / class', 'Gate class', 'Ca coordination', 'Ca bond metric', 'Silicate unit', 'Bridge-angle metric', 'Numeric readiness'],
  rows.map((row) => [
    row.material,
    row.gateClass,
    row.caCoordination,
    row.caBondMetric,
    row.silicateUnit,
    row.bridgeAngleMetric,
    row.numericReadiness,
  ])
)}

## Descriptor Readiness

${table(
  ['Descriptor', 'Status', 'Reason'],
  descriptorReadiness.map((row) => [row.descriptor, row.status, row.reason])
)}

## Modelling Boundary

${table(
  ['Boundary', 'Items'],
  [
    ['Allowed now', modellingBoundary.allowedNow.join('; ')],
    ['Blocked now', modellingBoundary.blockedNow.join('; ')],
    ['Next source need', modellingBoundary.nextSourceNeed],
  ]
)}

## Sources

${table(
  ['Material / class', 'Source URLs'],
  rows.map((row) => [row.material, row.sourceUrls.join('; ')])
)}

## Reading

The next model may use categorical structural gates, but not numeric bridge-angle terms yet. The available sources support the direction of the structural hypothesis: Ca environment and silicate-unit connectivity differ across melilite, rankinite, and kilchoanite. However, exact comparable Si-O-Si bridge angles and bridge-oxygen coordination values are not yet source-extracted across the full set.

Do not fit a continuous topology coefficient until comparable structure tables or CIF-derived values are available for all gate classes.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-structural-numeric-readiness-diagnostic.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('ri-structural-numeric-readiness-diagnostic.md', outDir), markdown);

console.log(markdown);
