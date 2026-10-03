import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function round(value, places = 6) {
  return Number(value.toFixed(places));
}

function midpoint([low, high]) {
  return (low + high) / 2;
}

function biaxialScalar(alpha, beta, gamma) {
  return (alpha + beta + gamma) / 3;
}

function scalarRange(alphaRange, betaRange, gammaRange) {
  return [
    biaxialScalar(alphaRange[0], betaRange[0], gammaRange[0]),
    biaxialScalar(alphaRange[1], betaRange[1], gammaRange[1]),
  ].map((value) => round(value));
}

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const opticalSource = {
  label: 'Handbook of Mineralogy, Wollastonite PDF',
  url: 'https://handbookofmineralogy.org/pdfs/wollastonite.pdf',
  value:
    'Reports broad D(meas.) = 2.86-3.09, D(calc.) = 2.90, alpha = 1.616-1.640, beta = 1.628-1.650, gamma = 1.631-1.653, and lists multiple polytypes.',
  polytypeSpecific: false,
  densityRange: [2.86, 3.09],
  densityCalculated: 2.9,
  alphaRange: [1.616, 1.64],
  betaRange: [1.628, 1.65],
  gammaRange: [1.631, 1.653],
};

const cifCandidates = [
  {
    codId: '9005777',
    mineralName: 'Wollastonite',
    polytype: 'WO1T / triclinic wollastonite-like row',
    formula: 'CaSiO3',
    reference: 'Ohashi 1984, Polysynthetically-twinned structures of enstatite and wollastonite',
    sourceMaterial: 'not stated in fetched CIF header',
    spaceGroup: 'P -1',
    cell: 'a=7.9258, b=7.3202, c=7.0653, alpha=90.055, beta=95.217, gamma=103.426',
    densityCalculated: 2.916,
    hasCoordinates: true,
    hasDisorder: false,
    url: 'https://www.crystallography.net/cod/9005777.cif',
    cardUrl: 'https://www.crystallography.net/cod/9005777.html',
  },
  {
    codId: '9008151',
    mineralName: 'Wollastonite-2M',
    polytype: 'parawollastonite / Wollastonite-2M',
    formula: 'CaSiO3',
    reference: 'Trojer 1968, The crystal structure of parawollastonite',
    sourceMaterial: 'Crestmore, California, USA',
    spaceGroup: 'P 1 21/a 1',
    cell: 'a=15.426, b=7.320, c=7.066, beta=95.404',
    densityCalculated: 2.914,
    hasCoordinates: true,
    hasDisorder: false,
    url: 'https://www.crystallography.net/cod/9008151.cif',
    cardUrl: 'https://www.crystallography.net/cod/9008151.html',
  },
  {
    codId: '9011913',
    mineralName: 'Wollastonite-2M',
    polytype: 'Wollastonite-2M',
    formula: 'CaSiO3',
    reference: 'Mamedov and Belov 1956, The crystal structure of wollastonite',
    sourceMaterial: 'not stated in fetched CIF header',
    spaceGroup: 'P 1 21/a 1',
    cell: 'a=15.36, b=7.285, c=7.084, beta=95.4',
    densityCalculated: 2.933,
    hasCoordinates: true,
    hasDisorder: false,
    url: 'https://www.crystallography.net/cod/9011913.cif',
    cardUrl: 'https://www.crystallography.net/cod/9011913.html',
  },
];

const lockRequirements = [
  {
    field: 'single polytype identity',
    required: 'explicit Wo-1A/WO1T, Wollastonite-2M/parawollastonite, or other singular polytype',
    currentState: 'CIF candidates are polytype-specific, but the available Handbook optical row is pooled/broad',
    locked: false,
  },
  {
    field: 'polytype-specific optical constants',
    required: 'alpha, beta, gamma for the same polytype, with source citation and wavelength if reported',
    currentState: 'not locked; Handbook optical constants are broad and not assigned to a selected polytype',
    locked: false,
  },
  {
    field: 'polytype-specific measured density',
    required: 'measured density for the same polytype/source row',
    currentState: 'not locked; Handbook reports broad measured density 2.86-3.09',
    locked: false,
  },
  {
    field: 'paired CIF',
    required: 'COD or equivalent coordinates for the same polytype',
    currentState: 'available for multiple candidate polytypes',
    locked: true,
  },
  {
    field: 'composition hygiene',
    required: 'pure Ca-Si-O, excluding Mn/Fe-substituted bustamite/pectolite-adjacent rows',
    currentState: 'candidate COD rows are formula CaSiO3; optical sample composition remains not source-locked',
    locked: false,
  },
  {
    field: 'pre-score gate classification',
    required: 'CIF-derived Ca coordination and mean Ca-O under the fixed extractor before optical scoring',
    currentState: 'deferred until a single source-locked polytype is selected',
    locked: false,
  },
];

const handbookScalarRange = scalarRange(
  opticalSource.alphaRange,
  opticalSource.betaRange,
  opticalSource.gammaRange,
);

const report = {
  source: 'ri-wollastonite-polytype-source-lock-screen.mjs',
  date: '2026-05-17',
  status: 'wollastonite deferred; no polytype-specific optical/density/CIF source lock established',
  opticalSource: {
    ...opticalSource,
    scalarRiRange: handbookScalarRange,
    scalarRiMidpoint: round(midpoint(handbookScalarRange)),
  },
  cifCandidates,
  lockRequirements,
  decision:
    'defer wollastonite; fall back to spurrite scoring only as a Mg-removed/carbonate-introduced control contrast unless a polytype-specific optical row is found',
};

const markdown = `# RI Wollastonite Polytype Source-Lock Screen

## Scope

This screen checks whether wollastonite can become the next clean Ca-Si-O target after spurrite reservation. It does not score a prediction, does not compute a gate classification, and does not fit or promote a model. Wollastonite can only be reserved for RI scoring if optical constants, density, and CIF coordinates are source-locked to one polytype.

Date: ${report.date}

## Decision

${report.decision}

Status: ${report.status}

## Broad Optical Source

${table(
  ['Field', 'Value'],
  [
    ['Source', opticalSource.label],
    ['URL', opticalSource.url],
    ['Source value', opticalSource.value],
    ['Polytype-specific', opticalSource.polytypeSpecific ? 'yes' : 'no'],
    ['Scalar RI range from broad row', report.opticalSource.scalarRiRange.join('-')],
    ['Scalar RI midpoint from broad row', report.opticalSource.scalarRiMidpoint],
  ],
)}

## CIF Candidates

${table(
  [
    'COD ID',
    'Mineral name',
    'Polytype/read',
    'Density calc.',
    'Space group',
    'Coordinates',
    'Disorder',
    'Reference',
  ],
  cifCandidates.map((row) => [
    row.codId,
    row.mineralName,
    row.polytype,
    row.densityCalculated,
    row.spaceGroup,
    row.hasCoordinates ? 'yes' : 'no',
    row.hasDisorder ? 'yes' : 'no',
    row.reference,
  ]),
)}

## Lock Requirements

${table(
  ['Field', 'Required', 'Current state', 'Locked'],
  lockRequirements.map((row) => [
    row.field,
    row.required,
    row.currentState,
    row.locked ? 'yes' : 'no',
  ]),
)}

## Wording Boundaries

- Do not call wollastonite source-qualified until one polytype has matching optical constants, measured density, and CIF coordinates.
- Do not average Wo-1A/WO1T and Wollastonite-2M/parawollastonite optical rows.
- Do not use the broad Handbook scalar RI range as a held-out target.
- Do not treat this screen as model evidence; it is only a source-control gate.
- If no polytype-specific optical row is found, score spurrite next only as Mg-removed/carbonate-introduced control contrast.

## Reading

Wollastonite remains the higher-value chemistry target because it is pure Ca-Si-O, but it is not ready for prediction. The CIF side is usable for several polytype-specific candidates; the blocking field is a source-anchored optical and measured-density row for the same polytype. Until that row is found, the disciplined path is to defer wollastonite rather than relax the source lock.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-wollastonite-polytype-source-lock-screen.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('ri-wollastonite-polytype-source-lock-screen.md', outDir), markdown);

console.log(markdown);
