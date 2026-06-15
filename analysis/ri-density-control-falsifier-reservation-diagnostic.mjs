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

const candidates = [
  {
    material: 'merwinite',
    formula: 'Ca3Mg(SiO4)2',
    role: 'high-density Mg-bearing Ca-silicate density-control falsifier',
    topologyClass: 'dense Ca-Mg orthosilicate / merwinite structure',
    compositionClass: 'Ca-Mg-Si-O; not pure Ca-Si-O',
    densityRange: [3.15, 3.32],
    densityForFutureScoring: round(midpoint([3.15, 3.32])),
    densityCalculated: 3.33,
    opticalClass: 'biaxial (+)',
    alphaRange: [1.702, 1.71],
    betaRange: [1.71, 1.714],
    gammaRange: [1.718, 1.728],
    opticalSource: {
      label: 'Handbook of Mineralogy, Merwinite PDF',
      url: 'https://handbookofmineralogy.org/pdfs/merwinite.pdf',
      value:
        'Reports D(meas.) = 3.15-3.32, D(calc.) = 3.33, alpha = 1.702-1.710, beta = 1.710-1.714, gamma = 1.718-1.728.',
    },
    cifSource: {
      codId: '9000285',
      url: 'https://www.crystallography.net/cod/9000285.cif',
      cardUrl: 'https://www.crystallography.net/cod/9000285.html',
      reference:
        'Moore and Araki 1972, Atomic arrangement of merwinite, Ca3Mg[SiO4]2, an unusual dense-packed structure of geophysical interest',
      sourceMaterial: 'mineral / AMCSD-derived COD row',
      spaceGroup: 'P 1 21/a 1',
      cell: { a: 13.254, b: 5.293, c: 9.328, alpha: 90, beta: 91.9, gamma: 90 },
      densityCalculated: 3.338,
      hasCoordinates: true,
      hasDisorder: false,
    },
    decision: 'reserve',
    reason:
      'Best available next density-control falsifier: high density, high RI, Handbook optical constants, and a COD CIF with coordinates. Caveat: Mg chemistry is introduced.',
  },
  {
    material: 'spurrite',
    formula: 'Ca5(SiO4)2(CO3)',
    role: 'Ca-rich silicate-carbonate control candidate',
    topologyClass: 'Ca silicate-carbonate with isolated SiO4 and carbonate groups',
    compositionClass: 'Ca-Si-C-O; adds carbonate',
    densityRange: [3.02, 3.02],
    densityForFutureScoring: 3.02,
    densityCalculated: 3.025,
    opticalClass: 'biaxial (-)',
    alphaRange: [1.637, 1.641],
    betaRange: [1.672, 1.676],
    gammaRange: [1.676, 1.681],
    opticalSource: {
      label: 'Handbook of Mineralogy, Spurrite PDF',
      url: 'https://handbookofmineralogy.org/pdfs/spurrite.pdf',
      value:
        'Reports D(meas.) = 3.02, D(calc.) = 3.025, alpha = 1.637-1.641, beta = 1.672-1.676, gamma = 1.676-1.681.',
    },
    cifSource: {
      codId: 'pending',
      url: 'pending source-qualified CIF selection',
      cardUrl: 'pending',
      reference: 'Smith, Karle, Hauptman, and Karle 1960 spurrite structure is source-known, but a COD row was not selected in this step.',
      sourceMaterial: 'not yet selected',
      spaceGroup: 'P 21/a per Handbook/source descriptions',
      cell: { a: 10.49, b: 6.705, c: 14.16, alpha: 90, beta: 101.316667, gamma: 90 },
      densityCalculated: 3.025,
      hasCoordinates: false,
      hasDisorder: null,
    },
    decision: 'defer',
    reason:
      'Useful pure-Ca-heavy control but adds carbonate and needs a source-qualified CIF row before reservation.',
  },
  {
    material: 'wollastonite',
    formula: 'CaSiO3',
    role: 'Ca chain-silicate broad transfer candidate',
    topologyClass: 'Ca chain silicate / pyroxenoid',
    compositionClass: 'Ca-Si-O',
    densityRange: [2.86, 3.09],
    densityForFutureScoring: round(midpoint([2.86, 3.09])),
    densityCalculated: 2.9,
    opticalClass: 'biaxial (-)',
    alphaRange: [1.616, 1.64],
    betaRange: [1.628, 1.65],
    gammaRange: [1.631, 1.653],
    opticalSource: {
      label: 'Handbook of Mineralogy, Wollastonite PDF',
      url: 'https://handbookofmineralogy.org/pdfs/wollastonite.pdf',
      value:
        'Reports broad D(meas.) = 2.86-3.09 and broad alpha/beta/gamma ranges.',
    },
    cifSource: {
      codId: 'not selected here',
      url: 'not selected here',
      cardUrl: 'not selected here',
      reference: 'multiple polytypes; defer until polytype-specific optical/source row is selected',
      sourceMaterial: 'not selected',
      spaceGroup: 'polytype-dependent',
      cell: null,
      densityCalculated: 2.9,
      hasCoordinates: false,
      hasDisorder: null,
    },
    decision: 'defer',
    reason:
      'Useful Ca-Si-O chain silicate, but density/optical ranges are broad and polytype choice must be controlled before scoring.',
  },
  {
    material: 'hatrurite',
    formula: 'Ca3SiO5',
    role: 'pure Ca-Si-O high-Ca candidate',
    topologyClass: 'tricalcium silicate / hatrurite',
    compositionClass: 'Ca-Si-O',
    densityRange: null,
    densityForFutureScoring: null,
    densityCalculated: null,
    opticalClass: 'biaxial',
    alphaRange: null,
    betaRange: null,
    gammaRange: null,
    opticalSource: {
      label: 'Handbook of Mineralogy, Hatrurite PDF',
      url: 'https://handbookofmineralogy.org/pdfs/hatrurite.pdf',
      value:
        'Reports D(meas.) = n.d., D(calc.) = n.d., and n = n.d.; only birefringence approximately 0.006 is listed.',
    },
    cifSource: {
      codId: 'not selected',
      url: 'not selected',
      cardUrl: 'not selected',
      reference: 'structure rows exist elsewhere, but optical/density source is insufficient for this benchmark',
      sourceMaterial: 'not selected',
      spaceGroup: 'not selected',
      cell: null,
      densityCalculated: null,
      hasCoordinates: null,
      hasDisorder: null,
    },
    decision: 'reject for current gate',
    reason:
      'Attractive pure Ca-Si-O chemistry, but the Handbook optical and density fields are not usable for RI scoring.',
  },
];

const enrichedCandidates = candidates.map((candidate) => ({
  ...candidate,
  scalarRiRange:
    candidate.alphaRange && candidate.betaRange && candidate.gammaRange
      ? scalarRange(candidate.alphaRange, candidate.betaRange, candidate.gammaRange)
      : null,
}));

const reservedTarget = enrichedCandidates.find((candidate) => candidate.decision === 'reserve');

const lockedPreScoreExpectations = [
  {
    expectation: 'Do not score merwinite in this artifact',
    status: 'locked',
  },
  {
    expectation: 'Use the frozen baseline, split-Ca, and split-Ca/Mg families when merwinite is scored later',
    status: 'locked',
  },
  {
    expectation: 'Treat Mg chemistry as a limitation, not a hidden continuation of pure Ca-Si-O testing',
    status: 'locked',
  },
  {
    expectation:
      'If the density-family pass repeats while split-Ca/Mg fails or overpredicts, baseline density/polarizability pressure increases',
    status: 'pre-score interpretation',
  },
  {
    expectation:
      'If the density-family fails too, larnite was likely a local control-row accident',
    status: 'pre-score interpretation',
  },
];

const report = {
  source: 'ri-density-control-falsifier-reservation-diagnostic.mjs',
  date: '2026-05-17',
  status: 'merwinite reserved as next density-control falsifier; no prediction scored',
  reservedTarget,
  candidates: enrichedCandidates,
  lockedPreScoreExpectations,
};

const markdown = `# RI Density-Control Falsifier Reservation Diagnostic

## Scope

This diagnostic reserves the next target after the larnite density-control contrast. It does not score a prediction and does not fit or promote a model. The purpose is to test, later, whether the larnite baseline density-family pass repeats on another high-density Ca-silicate-family material with optical constants and CIF geometry.

Date: ${report.date}

## Candidate Screen

${table(
  [
    'Material',
    'Formula',
    'Composition class',
    'Density for future scoring',
    'Scalar RI range',
    'CIF status',
    'Decision',
    'Reason',
  ],
  enrichedCandidates.map((row) => [
    row.material,
    row.formula,
    row.compositionClass,
    row.densityForFutureScoring ?? 'n/a',
    row.scalarRiRange ? row.scalarRiRange.join('-') : 'n/a',
    row.cifSource.hasCoordinates ? `${row.cifSource.codId}; coordinates yes` : row.cifSource.codId,
    row.decision,
    row.reason,
  ])
)}

## Reserved Target

${table(
  ['Field', 'Value'],
  [
    ['Material', reservedTarget.material],
    ['Formula', reservedTarget.formula],
    ['Role', reservedTarget.role],
    ['Topology class', reservedTarget.topologyClass],
    ['Composition class', reservedTarget.compositionClass],
    ['Density range', reservedTarget.densityRange.join('-')],
    ['Density for future scoring', `${reservedTarget.densityForFutureScoring} (midpoint of measured density range)`],
    ['Calculated density', reservedTarget.densityCalculated],
    ['Optical class', reservedTarget.opticalClass],
    ['Scalar RI range', reservedTarget.scalarRiRange.join('-')],
    ['Scalar RI midpoint', round(midpoint(reservedTarget.scalarRiRange))],
  ]
)}

## Optical Source

${table(
  ['Field', 'Value'],
  [
    ['Source', reservedTarget.opticalSource.label],
    ['URL', reservedTarget.opticalSource.url],
    ['Source value', reservedTarget.opticalSource.value],
  ]
)}

## CIF Source

${table(
  ['Field', 'Value'],
  [
    ['COD ID', reservedTarget.cifSource.codId],
    ['CIF URL', reservedTarget.cifSource.url],
    ['COD card', reservedTarget.cifSource.cardUrl],
    ['Reference', reservedTarget.cifSource.reference],
    ['Source material', reservedTarget.cifSource.sourceMaterial],
    ['Space group', reservedTarget.cifSource.spaceGroup],
    [
      'Cell',
      `a=${reservedTarget.cifSource.cell.a}, b=${reservedTarget.cifSource.cell.b}, c=${reservedTarget.cifSource.cell.c}, beta=${reservedTarget.cifSource.cell.beta}`,
    ],
    ['Calculated density', reservedTarget.cifSource.densityCalculated],
    ['Has coordinates', reservedTarget.cifSource.hasCoordinates ? 'yes' : 'no'],
    ['Has disorder', reservedTarget.cifSource.hasDisorder ? 'yes' : 'no'],
  ]
)}

## Locked Pre-Score Expectations

${table(
  ['Expectation', 'Status'],
  lockedPreScoreExpectations.map((row) => [row.expectation, row.status])
)}

## Reading

Merwinite is the best available next density-control falsifier found in this screen because it combines high density, high refractive index, a Handbook optical row, and a COD CIF with coordinates. It is not chemically clean: Mg is present. That limitation must stay visible. The value of the test is not "pure Ca-Si-O transfer"; it is whether the larnite density-family pass repeats in another dense Ca-silicate-family structure while the split-Ca or split-Ca/Mg scaffold terms remain overbroad.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-density-control-falsifier-reservation-diagnostic.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('ri-density-control-falsifier-reservation-diagnostic.md', outDir), markdown);

console.log(markdown);
