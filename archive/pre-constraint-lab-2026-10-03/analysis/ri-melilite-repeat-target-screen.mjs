import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function round(value, places = 6) {
  return Number(value.toFixed(places));
}

function uniaxialScalar(ordinary, extraordinary) {
  return (2 * ordinary + extraordinary) / 3;
}

const candidates = [
  {
    material: 'gugiaite',
    formula: 'Ca2BeSi2O7',
    topologyClass: 'melilite group',
    sourceUrl: 'https://handbookofmineralogy.org/pdfs/gugiaite.pdf',
    density: 3.034,
    opticalClass: 'uniaxial (+)',
    ordinary: 1.664,
    extraordinary: 1.672,
    scalarRi: round(uniaxialScalar(1.664, 1.672)),
    sourceStrength: 'Handbook-backed',
    classFit: 'same melilite topology but introduces Be T1 chemistry',
    screenDecision: 'defer',
    reason:
      'Good source row and same melilite group, but Be adds a new high-field T1 chemistry class outside the frozen Al/Mg/Zn interpretation.',
  },
  {
    material: 'alumoakermanite',
    formula: '(Ca,Na)2(Al,Mg,Fe2+)(Si2O7)',
    topologyClass: 'melilite group',
    sourceUrl: 'https://www.handbookofmineralogy.org/pdfs/alumnoakermanite.pdf',
    density: 2.96,
    opticalClass: 'uniaxial (-)',
    ordinary: 1.635,
    extraordinary: 1.626,
    scalarRi: round(uniaxialScalar(1.635, 1.626)),
    sourceStrength: 'Handbook-backed',
    classFit: 'same melilite topology but mixed Ca/Na and Al/Mg/Fe chemistry',
    screenDecision: 'defer',
    reason:
      'Good source row and same melilite topology, but mixed occupancy prevents a clean same-class Al, Mg, or Zn repeat under the frozen contract.',
  },
  {
    material: 'rankinite',
    formula: 'Ca3Si2O7',
    topologyClass: 'rankinite-like Ca sorosilicate',
    sourceUrl: 'https://handbookofmineralogy.org/pdfs/rankinite.pdf',
    density: 2.98,
    opticalClass: 'biaxial (+)',
    ordinary: null,
    extraordinary: null,
    scalarRi: 1.645667,
    sourceStrength: 'Handbook-backed with Webmineral cross-check',
    classFit: 'not melilite; clean Ca-rich scaffold transfer target with no Mg/Al/Zn T1 chemistry',
    screenDecision: 'prefer for next falsifier if no pure same-class melilite is found',
    reason:
      'Topology changes, but that is exactly the frozen contract falsifier for whether melilite Ca-scaffold uplift transfers outside melilite.',
  },
];

const screen = {
  source: 'ri-melilite-repeat-target-screen.mjs',
  status: 'target screening only; no prediction made',
  decision:
    'No clean same-class Al/Mg/Zn melilite repeat is promoted. Gugiaite and alumoakermanite are source-backed melilite repeats but add new or mixed T1 chemistry. Rankinite remains the cleaner next falsifier for topology-gated Ca scaffold transfer.',
  candidates,
};

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const markdown = `# RI Melilite Repeat Target Screen

## Scope

This screen checks whether a same-class melilite repeat should precede rankinite under the frozen T1-buffer contract. It does not score any candidate and does not change coefficients.

## Candidates

${table(
  ['Material', 'Formula', 'Topology', 'Density', 'Optical class', 'Scalar RI', 'Source strength', 'Class fit', 'Decision'],
  candidates.map((row) => [
    row.material,
    row.formula,
    row.topologyClass,
    row.density,
    row.opticalClass,
    row.scalarRi,
    row.sourceStrength,
    row.classFit,
    row.screenDecision,
  ])
)}

## Candidate Notes

${table(
  ['Material', 'Source', 'Reason'],
  candidates.map((row) => [row.material, row.sourceUrl, row.reason])
)}

## Decision

No clean same-class Al/Mg/Zn melilite repeat is promoted.

Gugiaite is source-backed and in the melilite group, but Be introduces a new T1 chemistry class. Alumoakermanite is source-backed and in the melilite group, but mixed Ca/Na and Al/Mg/Fe occupancy makes it a chemically entangled repeat.

Rankinite remains the cleaner next falsifier if the question is whether the Ca-scaffold uplift is topology-gated rather than generally transferable.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-melilite-repeat-target-screen.json', outDir), JSON.stringify(screen, null, 2));
await writeFile(new URL('ri-melilite-repeat-target-screen.md', outDir), markdown);

console.log(markdown);
