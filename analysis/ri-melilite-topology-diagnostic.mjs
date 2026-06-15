import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const atomicMass = {
  O: 15.999,
  Mg: 24.305,
  Al: 26.9815385,
  Si: 28.085,
  Ca: 40.078,
};

const rows = [
  {
    formula: 'Ca2Al2SiO7',
    material: 'gehlenite',
    role: 'fresh RI failure row',
    composition: { Ca: 2, Al: 2, Si: 1, O: 7 },
    density: 2.97714,
    measuredRi: 1.66217,
    topologyClass: 'melilite sorosilicate',
    tetrahedralSitePattern: 'Al at T1; mixed Al/Si at T2',
    nonTetrahedralCations: { Ca: 2 },
    tetrahedralAl: 2,
    tetrahedralMg: 0,
    tetrahedralSi: 1,
    sourceNote:
      'RI from Burshtein, Shimony, and Levy JOSA A 1993; density from CatalystHub/Materials Project structure density.',
  },
  {
    formula: 'Ca2MgSi2O7',
    material: 'akermanite',
    role: 'reserved melilite-family candidate; RI not yet scored',
    composition: { Ca: 2, Mg: 1, Si: 2, O: 7 },
    density: 2.941,
    measuredRi: null,
    topologyClass: 'melilite sorosilicate',
    tetrahedralSitePattern: 'Mg at T1; Si at T2',
    nonTetrahedralCations: { Ca: 2 },
    tetrahedralAl: 0,
    tetrahedralMg: 1,
    tetrahedralSi: 2,
    sourceNote:
      'Density from Mindat/AMCSD-style structure snippet for 100% Ak; RI source remains pending primary/source-table confirmation.',
  },
  {
    formula: 'CaAl2Si2O8',
    material: 'anorthite',
    role: 'feldspar Ca-Al-Si comparison row',
    composition: { Ca: 1, Al: 2, Si: 2, O: 8 },
    density: 2.75,
    measuredRi: 1.58167,
    topologyClass: 'feldspar framework',
    tetrahedralSitePattern: 'Al/Si framework tetrahedra',
    nonTetrahedralCations: { Ca: 1 },
    tetrahedralAl: 2,
    tetrahedralMg: 0,
    tetrahedralSi: 2,
    sourceNote:
      'Existing RI target from Mindat anorthite optical data mean; density from Mindat specific gravity range midpoint.',
  },
];

function round(value, places = 5) {
  return Number(value.toFixed(places));
}

function molarMass(composition) {
  return Object.entries(composition).reduce((sum, [element, count]) => sum + atomicMass[element] * count, 0);
}

function count(row, element) {
  return row.composition[element] ?? 0;
}

function tetrahedralCations(row) {
  return row.tetrahedralAl + row.tetrahedralMg + row.tetrahedralSi;
}

function nonTetrahedralCharge(row) {
  return Object.entries(row.nonTetrahedralCations).reduce((sum, [element, countValue]) => {
    const charge = element === 'Ca' || element === 'Mg' ? 2 : 1;
    return sum + charge * countValue;
  }, 0);
}

function decorate(row) {
  const mass = molarMass(row.composition);
  const molarVolume = mass / row.density;
  const oxygen = count(row, 'O');
  const tCations = tetrahedralCations(row);
  return {
    ...row,
    molarMass: round(mass),
    molarVolume: round(molarVolume),
    oxygenVolume: round(molarVolume / oxygen),
    tetrahedralPackingDensity: round(tCations / molarVolume),
    tetrahedralAlFraction: round(row.tetrahedralAl / tCations),
    tetrahedralMgFraction: round(row.tetrahedralMg / tCations),
    tetrahedralSiFraction: round(row.tetrahedralSi / tCations),
    nonTetrahedralChargePerO: round(nonTetrahedralCharge(row) / oxygen),
    caPerO: round((row.nonTetrahedralCations.Ca ?? 0) / oxygen),
  };
}

const decoratedRows = rows.map(decorate);

const gehlenite = decoratedRows.find((row) => row.formula === 'Ca2Al2SiO7');
const anorthite = decoratedRows.find((row) => row.formula === 'CaAl2Si2O8');
const akermanite = decoratedRows.find((row) => row.formula === 'Ca2MgSi2O7');

const contrasts = [
  {
    contrast: 'gehlenite vs anorthite',
    question: 'same Ca-Al-Si-O broad chemistry, different topology class',
    oxygenVolumeDelta: round(gehlenite.oxygenVolume - anorthite.oxygenVolume),
    tetrahedralAlFractionDelta: round(gehlenite.tetrahedralAlFraction - anorthite.tetrahedralAlFraction),
    nonTetrahedralChargePerODelta: round(
      gehlenite.nonTetrahedralChargePerO - anorthite.nonTetrahedralChargePerO
    ),
    measuredRiDelta: round(gehlenite.measuredRi - anorthite.measuredRi),
    reading:
      'Gehlenite has higher RI despite similar oxygen volume and lower tetrahedral packing than anorthite, pointing beyond generic density/Al/O.',
  },
  {
    contrast: 'gehlenite vs akermanite reserved',
    question: 'same melilite topology and Ca scaffold, T-site Al replaced by Mg/Si',
    oxygenVolumeDelta: round(gehlenite.oxygenVolume - akermanite.oxygenVolume),
    tetrahedralAlFractionDelta: round(gehlenite.tetrahedralAlFraction - akermanite.tetrahedralAlFraction),
    nonTetrahedralChargePerODelta: round(
      gehlenite.nonTetrahedralChargePerO - akermanite.nonTetrahedralChargePerO
    ),
    measuredRiDelta: 'pending akermanite RI source',
    reading:
      'Akermanite would isolate melilite T-site chemistry from topology class if a strong RI source is confirmed.',
  },
];

const report = {
  source: 'ri-melilite-topology-diagnostic.mjs',
  status: 'diagnostic only; no validation target scored',
  rows: decoratedRows,
  contrasts,
  nextTargetPolicy:
    'Reserve akermanite only after confirming a source-table RI value, preferably ordinary/extraordinary indices with wavelength or a reputable handbook/mineral database value.',
};

function table(headers, bodyRows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...bodyRows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const markdown = `# RI Melilite Topology Diagnostic

## Scope

This diagnostic follows the gehlenite RI failure. It does not score a new target or promote a repair. It separates melilite/sorosilicate topology, Ca scaffold, and tetrahedral-site chemistry from generic density, Al/O, and cation-response descriptors.

## Rows

${table(
  [
    'Formula',
    'Material',
    'Role',
    'Topology',
    'T-site pattern',
    'Density',
    'O volume',
    'T packing',
    'T Al fraction',
    'T Mg fraction',
    'Ca/O',
    'Non-T charge/O',
    'Measured RI',
  ],
  decoratedRows.map((row) => [
    row.formula,
    row.material,
    row.role,
    row.topologyClass,
    row.tetrahedralSitePattern,
    row.density,
    row.oxygenVolume,
    row.tetrahedralPackingDensity,
    row.tetrahedralAlFraction,
    row.tetrahedralMgFraction,
    row.caPerO,
    row.nonTetrahedralChargePerO,
    row.measuredRi ?? 'pending',
  ])
)}

## Contrasts

${table(
  ['Contrast', 'Question', 'O volume delta', 'T Al fraction delta', 'Non-T charge/O delta', 'Measured RI delta', 'Reading'],
  contrasts.map((row) => [
    row.contrast,
    row.question,
    row.oxygenVolumeDelta,
    row.tetrahedralAlFractionDelta,
    row.nonTetrahedralChargePerODelta,
    row.measuredRiDelta,
    row.reading,
  ])
)}

## Reading

The gehlenite miss is not repaired by generic bridge-oxygen fraction. This diagnostic points to a more specific gap: melilite topology and T-site chemistry. Gehlenite differs from anorthite not simply by density or Al/O, but by a Ca-rich melilite scaffold with tetrahedral Al occupying a different structural role.

Akermanite is the natural next target because it keeps the melilite/Ca scaffold while replacing tetrahedral Al with Mg/Si. It should remain reserved until a strong RI source is confirmed.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-melilite-topology-diagnostic.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('ri-melilite-topology-diagnostic.md', outDir), markdown);

console.log(markdown);
