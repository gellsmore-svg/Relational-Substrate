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

const target = {
  material: 'larnite',
  formula: 'Ca2SiO4',
  role: 'held-out Ca-only non-melilite silicate target',
  reservationStatus: 'reserved before CIF geometry extraction and before RI scoring',
  topologyClass: 'Ca orthosilicate / beta-dicalcium silicate',
  whyThisTarget:
    'It keeps the chemistry Ca-Si-O but changes polymerization and Ca scaffold away from melilite and Ca3Si2O7.',
  opticalSource: {
    label: 'Handbook of Mineralogy, Larnite, Mineral Data Publishing version 1.2',
    url: 'https://handbookofmineralogy.org/pdfs/larnite.pdf',
    densityMeasuredRange: [3.28, 3.33],
    densityCalculated: 3.326,
    opticalClass: 'biaxial (+)',
    alphaRange: [1.7, 1.715],
    betaRange: [1.715, 1.723],
    gammaRange: [1.725, 1.74],
    sourceNotes:
      'Handbook reports D(meas.) = 3.28-3.33, D(calc.) = 3.326, alpha = 1.700-1.715, beta = 1.715-1.723, gamma = 1.725-1.740.',
  },
  cifSource: {
    codId: '9017424',
    url: 'https://www.crystallography.net/cod/9017424.cif',
    cardUrl: 'https://www.crystallography.net/cod/9017424.html',
    reference:
      'Yamnova et al. 2011, Crystal structure of larnite beta-Ca2SiO4 and specific features of polymorphic transitions in dicalcium orthosilicate',
    sourceMaterial: 'synthetic',
    spaceGroup: 'P 1 21/n 1',
    cell: { a: 5.5051, b: 6.7551, c: 9.3108, alpha: 90, beta: 94.513, gamma: 90 },
    densityCalculated: 3.314,
    hasCoordinates: true,
    hasDisorder: false,
  },
};

const scalarRiRange = [
  biaxialScalar(target.opticalSource.alphaRange[0], target.opticalSource.betaRange[0], target.opticalSource.gammaRange[0]),
  biaxialScalar(target.opticalSource.alphaRange[1], target.opticalSource.betaRange[1], target.opticalSource.gammaRange[1]),
].map((value) => round(value));

const reservation = {
  ...target,
  densityForFutureScoring: round(midpoint(target.opticalSource.densityMeasuredRange)),
  scalarRiRange,
  scalarRiMidpoint: round(midpoint(scalarRiRange)),
};

const rejectedAlternatives = [
  {
    material: 'wollastonite',
    reason:
      'Useful later Ca-chain transfer target, but the prior screen flagged broad Handbook density and optical ranges.',
  },
  {
    material: 'gugiaite / alumoakermanite',
    reason:
      'Useful same-scaffold melilite stress tests, but they require source-qualified RI and CIF pairing before reservation.',
  },
  {
    material: 'additional Ca3Si2O7 polymorph',
    reason:
      'Useful if source-qualified, but rankinite and kilchoanite have already established the first Ca3Si2O7 pair.',
  },
];

const lockedPreScoreExpectations = [
  {
    expectation: 'Do not fit a new coefficient before scoring larnite',
    status: 'locked',
  },
  {
    expectation: 'Use the existing split-Ca family and candidate gate definitions as frozen diagnostics',
    status: 'locked',
  },
  {
    expectation: 'Extract larnite CIF geometry before optical scoring, then classify the gate without changing thresholds',
    status: 'next step',
  },
  {
    expectation:
      'If larnite is lower-coordinate or compact by the fixed extractor, the candidate gate predicts non-transfer of melilite Ca uplift',
    status: 'hypothesis, not yet scored',
  },
];

const report = {
  source: 'ri-heldout-larnite-reservation-diagnostic.mjs',
  status: 'held-out target reserved; no prediction scored',
  reservation,
  rejectedAlternatives,
  lockedPreScoreExpectations,
};

function table(headers, bodyRows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...bodyRows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const markdown = `# RI Held-Out Larnite Reservation Diagnostic

## Scope

This diagnostic reserves larnite as the next held-out Ca-silicate target before CIF geometry extraction and before RI scoring. It does not score a prediction and does not fit a coefficient.

## Reserved Target

${table(
  ['Field', 'Value'],
  [
    ['Material', reservation.material],
    ['Formula', reservation.formula],
    ['Role', reservation.role],
    ['Topology class', reservation.topologyClass],
    ['Reservation status', reservation.reservationStatus],
    ['Why this target', reservation.whyThisTarget],
  ]
)}

## Optical Source

${table(
  ['Field', 'Value'],
  [
    ['Source', reservation.opticalSource.label],
    ['URL', reservation.opticalSource.url],
    ['Measured density range', reservation.opticalSource.densityMeasuredRange.join('-')],
    ['Density for future scoring', reservation.densityForFutureScoring],
    ['Optical class', reservation.opticalSource.opticalClass],
    ['alpha range', reservation.opticalSource.alphaRange.join('-')],
    ['beta range', reservation.opticalSource.betaRange.join('-')],
    ['gamma range', reservation.opticalSource.gammaRange.join('-')],
    ['Scalar RI range', reservation.scalarRiRange.join('-')],
    ['Scalar RI midpoint', reservation.scalarRiMidpoint],
  ]
)}

## CIF Source

${table(
  ['Field', 'Value'],
  [
    ['COD ID', reservation.cifSource.codId],
    ['CIF URL', reservation.cifSource.url],
    ['COD card', reservation.cifSource.cardUrl],
    ['Reference', reservation.cifSource.reference],
    ['Source material', reservation.cifSource.sourceMaterial],
    ['Space group', reservation.cifSource.spaceGroup],
    ['Cell', `a=${reservation.cifSource.cell.a}, b=${reservation.cifSource.cell.b}, c=${reservation.cifSource.cell.c}, beta=${reservation.cifSource.cell.beta}`],
    ['Calculated density', reservation.cifSource.densityCalculated],
    ['Has coordinates', reservation.cifSource.hasCoordinates ? 'yes' : 'no'],
    ['Has disorder', reservation.cifSource.hasDisorder ? 'yes' : 'no'],
  ]
)}

## Rejected Alternatives

${table(
  ['Alternative', 'Reason'],
  rejectedAlternatives.map((row) => [row.material, row.reason])
)}

## Locked Pre-Score Expectations

${table(
  ['Expectation', 'Status'],
  lockedPreScoreExpectations.map((row) => [row.expectation, row.status])
)}

## Reading

Larnite is now reserved as the next held-out target. The next safe step is geometry extraction and gate classification only. Optical scoring should come after that, with the split-Ca family and the candidate gates kept frozen.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-heldout-larnite-reservation-diagnostic.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('ri-heldout-larnite-reservation-diagnostic.md', outDir), markdown);

console.log(markdown);
