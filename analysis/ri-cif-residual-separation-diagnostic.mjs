import { readFile, mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const geometryReport = JSON.parse(await readFile(new URL('./out/ri-cif-geometry-extraction-diagnostic.json', import.meta.url)));
const topologyReport = JSON.parse(await readFile(new URL('./out/ri-ca-scaffold-topology-gate-diagnostic.json', import.meta.url)));

function round(value, places = 6) {
  return Number(value.toFixed(places));
}

function mean(values) {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function summarize(values) {
  if (values.length === 0) return null;
  return {
    count: values.length,
    min: round(Math.min(...values)),
    max: round(Math.max(...values)),
    mean: round(mean(values)),
  };
}

const geometryByMaterial = new Map(
  geometryReport.analyses.map((row) => [
    row.material,
    {
      codId: row.codId,
      gateClass: row.gateClass,
      bridgeAngleMean: row.bridgeAngleSummary?.mean ?? null,
      bridgeAngleMin: row.bridgeAngleSummary?.min ?? null,
      bridgeAngleMax: row.bridgeAngleSummary?.max ?? null,
      bridgeAngleCount: row.bridgeAngleSummary?.count ?? 0,
      scaffoldCoordinationMean: row.scaffoldCoordinationSummary?.mean ?? null,
      scaffoldCoordinationMin: row.scaffoldCoordinationSummary?.min ?? null,
      scaffoldCoordinationMax: row.scaffoldCoordinationSummary?.max ?? null,
      scaffoldDistanceMean: row.scaffoldDistanceSummary?.mean ?? null,
      scaffoldDistanceMin: row.scaffoldDistanceSummary?.min ?? null,
      scaffoldDistanceMax: row.scaffoldDistanceSummary?.max ?? null,
    },
  ])
);

const joinedRows = topologyReport.rows.map((row) => {
  const geometry = geometryByMaterial.get(row.material) ?? null;
  return {
    material: row.material,
    topologyGateClass: row.topologyGateClass,
    measuredRi: row.measuredRi,
    splitCaPrediction: row.splitCaPrediction,
    splitCaResidual: row.measuredMinusSplitCa,
    caO: row.caO,
    oxygenVolume: row.oxygenVolume,
    geometryStatus: geometry ? 'available' : 'missing from current CIF extraction',
    ...geometry,
  };
});

const rowsWithGeometry = joinedRows.filter((row) => row.geometryStatus === 'available');
const rowsMissingGeometry = joinedRows.filter((row) => row.geometryStatus !== 'available');

const groupSummary = Object.values(
  rowsWithGeometry.reduce((groups, row) => {
    groups[row.topologyGateClass] ??= { topologyGateClass: row.topologyGateClass, rows: [] };
    groups[row.topologyGateClass].rows.push(row);
    return groups;
  }, {})
).map((group) => ({
  topologyGateClass: group.topologyGateClass,
  materials: group.rows.map((row) => row.material),
  meanSplitCaResidual: round(mean(group.rows.map((row) => row.splitCaResidual))),
  meanCaO: round(mean(group.rows.map((row) => row.caO))),
  meanOxygenVolume: round(mean(group.rows.map((row) => row.oxygenVolume))),
  meanBridgeAngle: round(mean(group.rows.map((row) => row.bridgeAngleMean))),
  meanScaffoldCoordination: round(mean(group.rows.map((row) => row.scaffoldCoordinationMean))),
  meanScaffoldDistance: round(mean(group.rows.map((row) => row.scaffoldDistanceMean))),
}));

const descriptorContrasts = [
  {
    descriptor: 'Ca/O',
    meliliteValue: groupSummary.find((row) => row.topologyGateClass === 'melilite sheet scaffold')?.meanCaO ?? null,
    ca3si2o7Value:
      groupSummary.find((row) => row.topologyGateClass === 'Ca3Si2O7 polymorph scaffold')?.meanCaO ?? null,
    reading: 'changes by formula class, but earlier rankinite/kilchoanite failures show it is not transferable by itself',
  },
  {
    descriptor: 'oxygen volume',
    meliliteValue: groupSummary.find((row) => row.topologyGateClass === 'melilite sheet scaffold')?.meanOxygenVolume ?? null,
    ca3si2o7Value:
      groupSummary.find((row) => row.topologyGateClass === 'Ca3Si2O7 polymorph scaffold')?.meanOxygenVolume ?? null,
    reading: 'available but still composition/packing level; does not encode local Ca scaffold geometry',
  },
  {
    descriptor: 'mean T-O-T bridge angle',
    meliliteValue: groupSummary.find((row) => row.topologyGateClass === 'melilite sheet scaffold')?.meanBridgeAngle ?? null,
    ca3si2o7Value:
      groupSummary.find((row) => row.topologyGateClass === 'Ca3Si2O7 polymorph scaffold')?.meanBridgeAngle ?? null,
    reading:
      'not clean as a single scalar here: rankinite is high-angle while kilchoanite is low-angle; useful as topology detail, not the first gate',
  },
  {
    descriptor: 'mean Ca scaffold coordination',
    meliliteValue:
      groupSummary.find((row) => row.topologyGateClass === 'melilite sheet scaffold')?.meanScaffoldCoordination ?? null,
    ca3si2o7Value:
      groupSummary.find((row) => row.topologyGateClass === 'Ca3Si2O7 polymorph scaffold')?.meanScaffoldCoordination ?? null,
    reading:
      'cleanest current physical discriminator: Ca3Si2O7 rows have lower effective Ca coordination and large negative split-Ca residuals',
  },
  {
    descriptor: 'mean Ca-O scaffold distance',
    meliliteValue:
      groupSummary.find((row) => row.topologyGateClass === 'melilite sheet scaffold')?.meanScaffoldDistance ?? null,
    ca3si2o7Value:
      groupSummary.find((row) => row.topologyGateClass === 'Ca3Si2O7 polymorph scaffold')?.meanScaffoldDistance ?? null,
    reading:
      'also physically instructive: Ca3Si2O7 rows have shorter mean Ca-O distances despite the melilite-derived Ca term overpredicting RI',
  },
];

const residualByScaffoldDistance = rowsWithGeometry.map((row) => ({
  material: row.material,
  scaffoldDistanceMean: row.scaffoldDistanceMean,
  scaffoldCoordinationMean: row.scaffoldCoordinationMean,
  splitCaResidual: row.splitCaResidual,
}));

const readings = [
  {
    finding: 'Ca scaffold geometry is more instructive than bridge angle as the first quantitative gate',
    evidence:
      'Gehlenite and akermanite have Ca coordination 8 and near-zero split-Ca residuals, while rankinite/kilchoanite have lower coordination means and roughly -0.028 split-Ca residuals.',
  },
  {
    finding: 'Bridge angle is topology-specific but not monotone against the residual in this small set',
    evidence:
      'Rankinite bridge angle is 136.232 deg and kilchoanite is 117.474 deg, yet both have nearly identical negative residuals.',
  },
  {
    finding: 'The current physical motif is Ca scaffold compaction / coordination change',
    evidence:
      'Ca3Si2O7 rows show shorter mean Ca-O distances and lower effective coordination than the melilite rows; this matches the failure of scalar Ca/O uplift.',
  },
];

const report = {
  source: 'ri-cif-residual-separation-diagnostic.mjs',
  status: 'diagnostic only; no optical coefficient fit',
  caveat:
    rowsMissingGeometry.length === 0
      ? 'All current topology-gate rows have CIF-derived geometry in this join.'
      : `${rowsMissingGeometry.map((row) => row.material).join(', ')} remain optical rows without CIF-derived geometry.`,
  joinedRows,
  rowsMissingGeometry,
  groupSummary,
  descriptorContrasts,
  residualByScaffoldDistance,
  bridgeAngleSummary: summarize(rowsWithGeometry.map((row) => row.bridgeAngleMean)),
  scaffoldCoordinationSummary: summarize(rowsWithGeometry.map((row) => row.scaffoldCoordinationMean)),
  scaffoldDistanceSummary: summarize(rowsWithGeometry.map((row) => row.scaffoldDistanceMean)),
  readings,
};

function table(headers, bodyRows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...bodyRows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

function format(value) {
  return value === null || value === undefined ? 'n/a' : value;
}

const markdown = `# RI CIF Residual-Separation Diagnostic

## Scope

This diagnostic joins CIF-derived local geometry to the frozen split-Ca residuals. It does not fit a new optical coefficient. It asks whether geometry descriptors give a sharper physical gate than Ca/O or oxygen volume.

Important caveat: this is still a four-row diagnostic, not a model fit. The geometry values depend on the source CIF, symmetry expansion, and fixed cutoffs.

## Joined Rows

${table(
  [
    'Material',
    'Topology gate class',
    'Split-Ca residual',
    'Ca/O',
    'O volume',
    'Bridge angle mean',
    'Ca coord mean',
    'Mean Ca-O',
    'Geometry status',
  ],
  joinedRows.map((row) => [
    row.material,
    row.topologyGateClass,
    row.splitCaResidual,
    row.caO,
    row.oxygenVolume,
    format(row.bridgeAngleMean),
    format(row.scaffoldCoordinationMean),
    format(row.scaffoldDistanceMean),
    row.geometryStatus,
  ])
)}

## Geometry Group Summary

${table(
  [
    'Topology gate class',
    'Materials',
    'Mean residual',
    'Mean bridge angle',
    'Mean Ca coord',
    'Mean Ca-O',
  ],
  groupSummary.map((row) => [
    row.topologyGateClass,
    row.materials.join(', '),
    row.meanSplitCaResidual,
    row.meanBridgeAngle,
    row.meanScaffoldCoordination,
    row.meanScaffoldDistance,
  ])
)}

## Descriptor Contrasts

${table(
  ['Descriptor', 'Melilite value', 'Ca3Si2O7 value', 'Reading'],
  descriptorContrasts.map((row) => [row.descriptor, format(row.meliliteValue), format(row.ca3si2o7Value), row.reading])
)}

## Readings

${table(
  ['Finding', 'Evidence'],
  readings.map((row) => [row.finding, row.evidence])
)}

## Boundary

The current physical pattern is not simply "more Ca raises RI." It is closer to: a melilite Ca scaffold term only transfers when the Ca environment stays melilite-like. In the Ca3Si2O7 pair, the Ca scaffold is more compact and lower-coordinate, and the melilite-derived Ca uplift overpredicts RI by nearly the same amount in both polymorphs.

Next safe step: use the now-paired melilite geometry rows to define candidate gate tests, then reserve a new held-out Ca-silicate target before any coefficient or threshold is proposed.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-cif-residual-separation-diagnostic.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('ri-cif-residual-separation-diagnostic.md', outDir), markdown);

console.log(markdown);
