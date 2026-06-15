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
    material: 'gehlenite',
    formula: 'Ca2Al2SiO7',
    topologyClass: 'melilite sorosilicate',
    topologyGateClass: 'melilite sheet scaffold',
    composition: { Ca: 2, Al: 2, Si: 1, O: 7 },
    density: 2.97714,
    measuredRi: 1.66217,
    splitCaPrediction: 1.66054,
    splitCaMgPrediction: 1.66166,
    sourceStatus: 'paper-backed',
  },
  {
    material: 'akermanite',
    formula: 'Ca2MgSi2O7',
    topologyClass: 'melilite sorosilicate',
    topologyGateClass: 'melilite sheet scaffold',
    composition: { Ca: 2, Mg: 1, Si: 2, O: 7 },
    density: 2.944,
    measuredRi: 1.63467,
    splitCaPrediction: 1.63523,
    splitCaMgPrediction: 1.63467,
    sourceStatus: 'source-qualified',
  },
  {
    material: 'rankinite',
    formula: 'Ca3Si2O7',
    topologyClass: 'rankinite-like Ca sorosilicate',
    topologyGateClass: 'Ca3Si2O7 polymorph scaffold',
    composition: { Ca: 3, Si: 2, O: 7 },
    density: 2.98,
    measuredRi: 1.645667,
    splitCaPrediction: 1.67378,
    splitCaMgPrediction: 1.68211,
    sourceStatus: 'Handbook-backed',
  },
  {
    material: 'kilchoanite',
    formula: 'Ca3Si2O7',
    topologyClass: 'kilchoanite Ca sorosilicate polymorph',
    topologyGateClass: 'Ca3Si2O7 polymorph scaffold',
    composition: { Ca: 3, Si: 2, O: 7 },
    density: 2.992,
    measuredRi: 1.648167,
    splitCaPrediction: 1.67592,
    splitCaMgPrediction: 1.68428,
    sourceStatus: 'Handbook-backed',
  },
];

function round(value, places = 6) {
  return Number(value.toFixed(places));
}

function count(row, element) {
  return row.composition[element] ?? 0;
}

function molarMass(composition) {
  return Object.entries(composition).reduce((sum, [element, elementCount]) => sum + atomicMass[element] * elementCount, 0);
}

function mean(values) {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

const enrichedRows = rows.map((row) => {
  const oxygen = count(row, 'O');
  const tAtoms = count(row, 'Si') + count(row, 'Al') + count(row, 'Mg');
  const molarVolume = molarMass(row.composition) / row.density;
  return {
    ...row,
    caO: round(count(row, 'Ca') / oxygen),
    tO: round(tAtoms / oxygen),
    siO: round(count(row, 'Si') / oxygen),
    alMgO: round((count(row, 'Al') + count(row, 'Mg')) / oxygen),
    oxygenVolume: round(molarVolume / oxygen),
    measuredMinusSplitCa: round(row.measuredRi - row.splitCaPrediction),
    measuredMinusSplitCaMg: round(row.measuredRi - row.splitCaMgPrediction),
  };
});

const groupSummary = Object.values(
  enrichedRows.reduce((groups, row) => {
    groups[row.topologyGateClass] ??= {
      topologyGateClass: row.topologyGateClass,
      rows: [],
    };
    groups[row.topologyGateClass].rows.push(row);
    return groups;
  }, {})
).map((group) => ({
  topologyGateClass: group.topologyGateClass,
  materials: group.rows.map((row) => row.material),
  meanCaO: round(mean(group.rows.map((row) => row.caO))),
  meanOxygenVolume: round(mean(group.rows.map((row) => row.oxygenVolume))),
  meanMeasuredRi: round(mean(group.rows.map((row) => row.measuredRi))),
  meanSplitCaResidual: round(mean(group.rows.map((row) => row.measuredMinusSplitCa))),
  meanSplitCaMgResidual: round(mean(group.rows.map((row) => row.measuredMinusSplitCaMg))),
}));

const gateRules = [
  {
    rule: 'Ca/O is not transferable by itself',
    evidence:
      'Ca3Si2O7 polymorphs have higher Ca/O than melilites but are overpredicted by the melilite-derived Ca scaffold term.',
  },
  {
    rule: 'oxygen volume is not sufficient by itself',
    evidence:
      'Melilite and Ca3Si2O7 rows have overlapping oxygen volumes around 13.7-13.8 A3/O while residual signs differ by topology class.',
  },
  {
    rule: 'topology gate must be categorical until a structural descriptor is sourced',
    evidence:
      'Rankinite and kilchoanite share formula and similar RI, so the gate separates melilite sheet scaffold from Ca3Si2O7 polymorph scaffold rather than rankinite alone.',
  },
];

const nextDescriptorNeeds = [
  'source structural descriptors for melilite vs Ca3Si2O7 topology: Si2O7 linkage geometry, Ca coordination/polyhedral connectivity, and bridge oxygen environment',
  'test larnite only after the gate is stated, because it changes formula to Ca2SiO4 and will probe broader Ca-only topology transfer',
  'do not fit a topology coefficient from two melilites plus two Ca3Si2O7 polymorphs; use this as a gate-selection diagnostic',
];

const report = {
  source: 'ri-ca-scaffold-topology-gate-diagnostic.mjs',
  status: 'diagnostic only; no repair coefficient promoted',
  rows: enrichedRows,
  groupSummary,
  gateRules,
  nextDescriptorNeeds,
};

function table(headers, bodyRows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...bodyRows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const markdown = `# RI Ca-Scaffold Topology-Gate Diagnostic

## Scope

This diagnostic consolidates the melilite, rankinite, and kilchoanite Ca-scaffold results. It does not fit a repair term. It asks what kind of gate is required before Ca scaffold is reused outside melilite.

## Rows

${table(
  [
    'Material',
    'Formula',
    'Topology gate class',
    'Ca/O',
    'O volume',
    'Measured RI',
    'Split Ca prediction',
    'Split Ca residual',
    'Split Ca/Mg residual',
    'Source status',
  ],
  enrichedRows.map((row) => [
    row.material,
    row.formula,
    row.topologyGateClass,
    row.caO,
    row.oxygenVolume,
    row.measuredRi,
    row.splitCaPrediction,
    row.measuredMinusSplitCa,
    row.measuredMinusSplitCaMg,
    row.sourceStatus,
  ])
)}

## Group Summary

${table(
  ['Topology gate class', 'Rows', 'Mean Ca/O', 'Mean O volume', 'Mean measured RI', 'Mean split-Ca residual'],
  groupSummary.map((row) => [
    row.topologyGateClass,
    row.materials.join(', '),
    row.meanCaO,
    row.meanOxygenVolume,
    row.meanMeasuredRi,
    row.meanSplitCaResidual,
  ])
)}

## Gate Rules

${table(
  ['Rule', 'Evidence'],
  gateRules.map((row) => [row.rule, row.evidence])
)}

## Next Descriptor Needs

${nextDescriptorNeeds.map((item) => `- ${item}`).join('\n')}

## Reading

The Ca-scaffold term is not a transferable scalar. It behaves locally inside melilite rows, then overpredicts both Ca3Si2O7 polymorphs by nearly the same amount. Since rankinite and kilchoanite have similar scalar RI, density, Ca/O, and oxygen volume, this is not a rankinite-specific anomaly.

The immediate gate should be categorical: melilite sheet scaffold versus Ca3Si2O7 polymorph scaffold. A later quantitative gate should be sourced from structural descriptors rather than inferred from four optical rows.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-ca-scaffold-topology-gate-diagnostic.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('ri-ca-scaffold-topology-gate-diagnostic.md', outDir), markdown);

console.log(markdown);
