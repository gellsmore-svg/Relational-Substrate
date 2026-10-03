import { readFile, mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const geometryReport = JSON.parse(await readFile(new URL('./out/ri-cif-geometry-extraction-diagnostic.json', import.meta.url)));
const reservationReport = JSON.parse(await readFile(new URL('./out/ri-heldout-larnite-reservation-diagnostic.json', import.meta.url)));

function round(value, places = 6) {
  return Number(value.toFixed(places));
}

function format(value) {
  if (value === null || value === undefined) return 'n/a';
  if (typeof value === 'boolean') return value ? 'yes' : 'no';
  return value;
}

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const larnite = geometryReport.analyses.find((row) => row.material === 'larnite');

if (!larnite) {
  throw new Error('larnite geometry row missing; run ri-cif-geometry-extraction-diagnostic.mjs first');
}

const larniteDescriptors = {
  material: larnite.material,
  codId: larnite.codId,
  gateClass: larnite.gateClass,
  bridgeAngleMean: larnite.bridgeAngleSummary?.mean ?? null,
  bridgeAngleRange:
    larnite.bridgeAngleSummary === null
      ? null
      : `${larnite.bridgeAngleSummary.min}-${larnite.bridgeAngleSummary.max}`,
  scaffoldCoordinationMean: larnite.scaffoldCoordinationSummary?.mean ?? null,
  scaffoldCoordinationRange:
    larnite.scaffoldCoordinationSummary === null
      ? null
      : `${larnite.scaffoldCoordinationSummary.min}-${larnite.scaffoldCoordinationSummary.max}`,
  scaffoldDistanceMean: larnite.scaffoldDistanceSummary?.mean ?? null,
  scaffoldDistanceRange:
    larnite.scaffoldDistanceSummary === null
      ? null
      : `${larnite.scaffoldDistanceSummary.min}-${larnite.scaffoldDistanceSummary.max}`,
};

const frozenGateChecks = [
  {
    gate: 'coordination-only Ca scaffold gate',
    frozenRule: 'melilite-like if mean Ca coordination is 8',
    descriptorValue: larniteDescriptors.scaffoldCoordinationMean,
    meliliteLike: larniteDescriptors.scaffoldCoordinationMean === 8,
    preScorePrediction: 'non-transfer of melilite Ca uplift',
  },
  {
    gate: 'mean Ca-O scaffold-distance gate',
    frozenRule: 'melilite-like if mean Ca-O is at least 2.53 A',
    descriptorValue: larniteDescriptors.scaffoldDistanceMean,
    meliliteLike:
      typeof larniteDescriptors.scaffoldDistanceMean === 'number' &&
      larniteDescriptors.scaffoldDistanceMean >= 2.53,
    preScorePrediction: 'non-transfer of melilite Ca uplift',
  },
  {
    gate: 'bridge-angle mean gate',
    frozenRule: 'rejected as first scalar gate before larnite reservation',
    descriptorValue: larniteDescriptors.bridgeAngleMean,
    meliliteLike: null,
    preScorePrediction: 'not used for pre-score classification',
  },
];

const classifiedChecks = frozenGateChecks.filter((row) => row.meliliteLike !== null);
const gateClassification =
  classifiedChecks.every((row) => row.meliliteLike === false)
    ? 'compact/lower-coordinate non-melilite Ca scaffold'
    : classifiedChecks.every((row) => row.meliliteLike === true)
      ? 'melilite-like Ca scaffold'
      : 'mixed gate classification';

const lockedBoundary = [
  {
    boundary: 'No optical score',
    status: 'locked',
    reading:
      'The larnite RI midpoint remains reserved in the prior diagnostic but is not compared to any prediction here.',
  },
  {
    boundary: 'No coefficient update',
    status: 'locked',
    reading: 'The split-Ca families and candidate gate thresholds remain unchanged.',
  },
  {
    boundary: 'Gate before score',
    status: 'satisfied',
    reading:
      'Larnite is classified by CIF geometry before any RI scoring, preserving the held-out test order.',
  },
];

const report = {
  source: 'ri-larnite-gate-classification-diagnostic.mjs',
  status: 'larnite CIF gate classified before optical scoring',
  reservation: {
    material: reservationReport.reservation.material,
    formula: reservationReport.reservation.formula,
    role: reservationReport.reservation.role,
    opticalSource: reservationReport.reservation.opticalSource,
    cifSource: reservationReport.reservation.cifSource,
  },
  larniteDescriptors,
  frozenGateChecks,
  gateClassification,
  lockedBoundary,
  nextAllowedStep:
    'Score larnite only after this gate classification is kept frozen; expected diagnostic outcome is non-transfer of the melilite Ca uplift.',
};

const markdown = `# RI Larnite Gate-Classification Diagnostic

## Scope

This diagnostic performs the reserved pre-score larnite step: extract CIF-derived local geometry, classify the frozen Ca-scaffold gate, and stop before optical scoring. It does not fit a coefficient and does not compare larnite RI to any model prediction.

## Reserved Target

${table(
  ['Field', 'Value'],
  [
    ['Material', report.reservation.material],
    ['Formula', report.reservation.formula],
    ['Role', report.reservation.role],
    ['CIF source', report.reservation.cifSource.url],
    ['Optical source held in reserve', report.reservation.opticalSource.url],
  ]
)}

## CIF Geometry

${table(
  ['Descriptor', 'Value'],
  [
    ['COD ID', larniteDescriptors.codId],
    ['Gate class', larniteDescriptors.gateClass],
    ['Bridge angle range', format(larniteDescriptors.bridgeAngleRange)],
    ['Bridge angle mean', format(larniteDescriptors.bridgeAngleMean)],
    ['Ca coordination range', format(larniteDescriptors.scaffoldCoordinationRange)],
    ['Mean Ca coordination', format(larniteDescriptors.scaffoldCoordinationMean)],
    ['Mean Ca-O range', format(larniteDescriptors.scaffoldDistanceRange)],
    ['Mean Ca-O', format(larniteDescriptors.scaffoldDistanceMean)],
  ]
)}

## Frozen Gate Checks

${table(
  ['Gate', 'Frozen rule', 'Descriptor value', 'Melilite-like?', 'Pre-score prediction'],
  frozenGateChecks.map((row) => [
    row.gate,
    row.frozenRule,
    format(typeof row.descriptorValue === 'number' ? round(row.descriptorValue) : row.descriptorValue),
    format(row.meliliteLike),
    row.preScorePrediction,
  ])
)}

## Boundary Locks

${table(
  ['Boundary', 'Status', 'Reading'],
  lockedBoundary.map((row) => [row.boundary, row.status, row.reading])
)}

## Reading

Gate classification: ${gateClassification}.

Larnite classifies as a compact/lower-coordinate non-melilite Ca scaffold under the frozen coordination and Ca-O distance gates. This is the required pre-score state: if larnite is scored next, the expected diagnostic outcome is non-transfer of the melilite Ca uplift. A pass would mean the gate generalizes; an overprediction similar to rankinite/kilchoanite would strengthen the topology-gated Ca-scaffold reading.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-larnite-gate-classification-diagnostic.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('ri-larnite-gate-classification-diagnostic.md', outDir), markdown);

console.log(markdown);
