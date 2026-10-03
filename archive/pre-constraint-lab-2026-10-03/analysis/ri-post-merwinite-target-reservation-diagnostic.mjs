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
    material: 'spurrite',
    formula: 'Ca5(SiO4)2(CO3)',
    role: 'Ca-rich silicate-carbonate post-merwinite confound-substitution target',
    topologyClass: 'Ca silicate-carbonate with isolated SiO4 and carbonate groups',
    compositionClass: 'Ca-Si-C-O; adds carbonate but removes Mg',
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
      codId: '9004961',
      url: 'https://www.crystallography.net/cod/9004961.cif',
      cardUrl: 'https://www.crystallography.net/cod/9004961.html',
      reference:
        'Grice 2005, The structure of spurrite, tilleyite and scawtite, and relationships to other silicate-carbonate minerals',
      sourceMaterial: 'Cornet Hill, Apuseni Mountains, Romania',
      spaceGroup: 'P 1 21/a 1',
      cell: { a: 10.484, b: 6.712, c: 14.156, alpha: 90, beta: 101.27, gamma: 90 },
      densityCalculated: 3.023,
      hasCoordinates: true,
      hasDisorder: false,
    },
    decision: 'reserve',
    reason:
      'Best source-qualified post-merwinite target found in this screen: removes Mg while keeping Ca-rich chemistry, has Handbook optical constants, and has COD coordinates. Caveat: carbonate is introduced, so this substitutes one confound for another.',
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
      codId: 'not selected',
      url: 'not selected',
      cardUrl: 'not selected',
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
      'Chemically cleaner Ca-Si-O target than spurrite, but optical/density ranges are broad and polytype choice remains uncontrolled.',
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
      reference: 'optical/density source is insufficient for this benchmark',
      sourceMaterial: 'not selected',
      spaceGroup: 'not selected',
      cell: null,
      densityCalculated: null,
      hasCoordinates: null,
      hasDisorder: null,
    },
    decision: 'reject for current gate',
    reason:
      'Attractive pure Ca-Si-O chemistry, but the available Handbook optical and density fields are not usable for RI scoring.',
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
    expectation: 'Do not score spurrite in this artifact',
    status: 'locked',
  },
  {
    expectation: 'Use the frozen baseline, split-Ca, and split-Ca/Mg families when spurrite is scored later',
    status: 'locked',
  },
  {
    expectation: 'Treat carbonate chemistry as a limitation, not as pure Ca-Si-O continuation',
    status: 'locked',
  },
  {
    expectation:
      'If split-Ca passes spurrite while Mg/O is zero, the merwinite split-Ca pass is less likely to be only an Mg artifact',
    status: 'pre-score interpretation',
  },
  {
    expectation:
      'If split-Ca fails spurrite, the merwinite split-Ca pass remains Mg/topology-confounded',
    status: 'pre-score interpretation',
  },
];

const report = {
  source: 'ri-post-merwinite-target-reservation-diagnostic.mjs',
  date: '2026-05-17',
  status: 'spurrite reserved as post-merwinite confound-substitution target; no prediction scored',
  reservedTarget,
  candidates: enrichedCandidates,
  lockedPreScoreExpectations,
};

const markdown = `# RI Post-Merwinite Target Reservation Diagnostic

## Scope

This diagnostic reserves the next target after merwinite. It does not score a prediction and does not fit or promote a model. The purpose is to remove the Mg confound introduced by merwinite while keeping source quality visible. Spurrite substitutes a carbonate confound, so it is a control contrast rather than a clean Ca-Si-O validation row.

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
    ['Density for future scoring', reservedTarget.densityForFutureScoring],
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

Spurrite is not a clean Ca-Si-O target because carbonate is introduced. It is the best source-qualified target found in this screen for removing the merwinite Mg confound while preserving usable optical and CIF sources: Ca-rich, no Mg, Handbook optical constants, and COD coordinates. Score it only after this reservation state is preserved, and read it as confound substitution rather than pure confound reduction.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-post-merwinite-target-reservation-diagnostic.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('ri-post-merwinite-target-reservation-diagnostic.md', outDir), markdown);

console.log(markdown);
