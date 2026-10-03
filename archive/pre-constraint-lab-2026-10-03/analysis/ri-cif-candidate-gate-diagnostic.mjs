import { readFile, mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const residualReport = JSON.parse(await readFile(new URL('./out/ri-cif-residual-separation-diagnostic.json', import.meta.url)));

function round(value, places = 6) {
  return Number(value.toFixed(places));
}

function mean(values) {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function absolute(value) {
  return Math.abs(value);
}

const rows = residualReport.joinedRows;
const meliliteRows = rows.filter((row) => row.topologyGateClass === 'melilite sheet scaffold');
const ca3si2o7Rows = rows.filter((row) => row.topologyGateClass === 'Ca3Si2O7 polymorph scaffold');

const candidateGates = [
  {
    gate: 'coordination-only Ca scaffold gate',
    descriptor: 'scaffoldCoordinationMean',
    candidateRule: 'melilite-like if mean Ca coordination is 8',
    observedGap: `${Math.max(...ca3si2o7Rows.map((row) => row.scaffoldCoordinationMean))} to ${Math.min(
      ...meliliteRows.map((row) => row.scaffoldCoordinationMean)
    )}`,
    promotedStatus: 'diagnostic candidate only',
    reason:
      'It cleanly separates the two melilite rows from the Ca3Si2O7 pair, but is cutoff-sensitive and should not be promoted from four rows.',
    classify: (row) => row.scaffoldCoordinationMean === 8,
  },
  {
    gate: 'mean Ca-O scaffold-distance gate',
    descriptor: 'scaffoldDistanceMean',
    candidateRule: 'melilite-like if mean Ca-O is at least 2.53 A',
    observedGap: `${round(Math.max(...ca3si2o7Rows.map((row) => row.scaffoldDistanceMean)))} to ${round(
      Math.min(...meliliteRows.map((row) => row.scaffoldDistanceMean))
    )} A`,
    promotedStatus: 'diagnostic candidate only',
    reason:
      'It separates the current rows and describes scaffold compaction, but the 2.53 A boundary is chosen inside the observed gap.',
    classify: (row) => row.scaffoldDistanceMean >= 2.53,
  },
  {
    gate: 'bridge-angle mean gate',
    descriptor: 'bridgeAngleMean',
    candidateRule: 'no stable one-dimensional rule from current rows',
    observedGap: 'rankinite high-angle and kilchoanite low-angle both have nearly identical negative residuals',
    promotedStatus: 'reject as first scalar gate',
    reason:
      'The class means are similar and the within-class Ca3Si2O7 spread crosses the melilite values, so angle is topology detail rather than first gate.',
    classify: () => null,
  },
  {
    gate: 'Ca/O scalar gate',
    descriptor: 'caO',
    candidateRule: 'reject as transferable scaffold gate',
    observedGap: 'Ca3Si2O7 has higher Ca/O but lower measured response than the melilite-derived Ca uplift predicts',
    promotedStatus: 'reject as transferable gate',
    reason:
      'It separates formulas but gives the wrong physical transfer reading: more Ca does not mean the melilite Ca uplift transfers.',
    classify: () => null,
  },
];

const gateResults = candidateGates.map((gate) => {
  const applicableRows = rows.map((row) => {
    const meliliteLike = gate.classify(row);
    return {
      material: row.material,
      topologyGateClass: row.topologyGateClass,
      descriptorValue: row[gate.descriptor],
      splitCaResidual: row.splitCaResidual,
      meliliteLike,
      expectedResidualBand: meliliteLike === null ? 'not classified' : meliliteLike ? 'near zero' : 'negative overprediction',
      matchesResidualBand:
        meliliteLike === null
          ? null
          : meliliteLike
            ? absolute(row.splitCaResidual) <= 0.003
            : row.splitCaResidual <= -0.02,
    };
  });

  const classified = applicableRows.filter((row) => row.matchesResidualBand !== null);
  return {
    ...gate,
    classify: undefined,
    rows: applicableRows,
    classifiedCount: classified.length,
    matchedCount: classified.filter((row) => row.matchesResidualBand).length,
    observedDiagnosticPass:
      classified.length > 0 && classified.every((row) => row.matchesResidualBand) ? 'yes on current rows' : 'not applicable / no',
  };
});

const groupCentres = [
  {
    group: 'melilite sheet scaffold',
    materials: meliliteRows.map((row) => row.material),
    meanResidual: round(mean(meliliteRows.map((row) => row.splitCaResidual))),
    meanCoordination: round(mean(meliliteRows.map((row) => row.scaffoldCoordinationMean))),
    meanCaODistance: round(mean(meliliteRows.map((row) => row.scaffoldDistanceMean))),
    meanBridgeAngle: round(mean(meliliteRows.map((row) => row.bridgeAngleMean))),
  },
  {
    group: 'Ca3Si2O7 polymorph scaffold',
    materials: ca3si2o7Rows.map((row) => row.material),
    meanResidual: round(mean(ca3si2o7Rows.map((row) => row.splitCaResidual))),
    meanCoordination: round(mean(ca3si2o7Rows.map((row) => row.scaffoldCoordinationMean))),
    meanCaODistance: round(mean(ca3si2o7Rows.map((row) => row.scaffoldDistanceMean))),
    meanBridgeAngle: round(mean(ca3si2o7Rows.map((row) => row.bridgeAngleMean))),
  },
];

const nextHeldOutTargets = [
  {
    targetClass: 'same melilite scaffold, different T1 cation',
    purpose: 'stress-test whether CaO8 scaffold gate remains near-zero residual while T1 chemistry changes',
    examples: 'gugiaite / alumoakermanite only if source-qualified RI and CIF are available',
  },
  {
    targetClass: 'Ca-only non-melilite silicate with known CIF and RI',
    purpose: 'test whether compact/lower-coordinate Ca scaffold predicts non-transfer of melilite Ca uplift',
    examples: 'larnite or wollastonite only after optical source uncertainty is handled',
  },
  {
    targetClass: 'additional Ca3Si2O7 or closely related polymorph',
    purpose: 'separate Ca3Si2O7 formula effects from local Ca coordination and scaffold distance',
    examples: 'prefer a source with explicit ambient-pressure structure and optical constants',
  },
];

const report = {
  source: 'ri-cif-candidate-gate-diagnostic.mjs',
  status: 'candidate gate diagnostic only; no coefficient or threshold promoted',
  groupCentres,
  candidateGates: gateResults,
  nextHeldOutTargets,
  boundary:
    'The coordination and Ca-O distance gates are allowed as hypotheses for the next held-out target, not as fitted model terms.',
};

function table(headers, bodyRows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...bodyRows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

function format(value) {
  if (value === null || value === undefined) return 'n/a';
  if (typeof value === 'boolean') return value ? 'yes' : 'no';
  return value;
}

const markdown = `# RI CIF Candidate-Gate Diagnostic

## Scope

This diagnostic turns the four-row CIF residual separation into explicit candidate gate tests. It does not fit a coefficient and does not promote a threshold. A gate can only be used as a held-out validation hypothesis.

## Group Centres

${table(
  ['Group', 'Materials', 'Mean residual', 'Mean Ca coordination', 'Mean Ca-O', 'Mean bridge angle'],
  groupCentres.map((row) => [
    row.group,
    row.materials.join(', '),
    row.meanResidual,
    row.meanCoordination,
    row.meanCaODistance,
    row.meanBridgeAngle,
  ])
)}

## Candidate Gates

${table(
  ['Gate', 'Candidate rule', 'Observed gap', 'Status', 'Current-row result', 'Reason'],
  gateResults.map((row) => [
    row.gate,
    row.candidateRule,
    row.observedGap,
    row.promotedStatus,
    row.observedDiagnosticPass,
    row.reason,
  ])
)}

## Row-Level Gate Checks

${gateResults
  .map(
    (gate) => `### ${gate.gate}

${table(
  ['Material', 'Descriptor value', 'Residual', 'Melilite-like?', 'Expected residual band', 'Matches?'],
  gate.rows.map((row) => [
    row.material,
    format(row.descriptorValue),
    row.splitCaResidual,
    format(row.meliliteLike),
    row.expectedResidualBand,
    format(row.matchesResidualBand),
  ])
)}
`
  )
  .join('\n')}

## Held-Out Target Need

${table(
  ['Target class', 'Purpose', 'Examples'],
  nextHeldOutTargets.map((row) => [row.targetClass, row.purpose, row.examples])
)}

## Reading

The candidate gate is now concrete enough to falsify: melilite-like Ca scaffold means Ca coordination 8 and long mean Ca-O distance near 2.57 A under the fixed extraction method. The Ca3Si2O7 rows are more compact and lower-coordinate, so the melilite-derived Ca uplift should not transfer.

Do not turn either numeric boundary into a model coefficient yet. The next target should be chosen before scoring, and should have both optical constants and an ambient-pressure CIF.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-cif-candidate-gate-diagnostic.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('ri-cif-candidate-gate-diagnostic.md', outDir), markdown);

console.log(markdown);
