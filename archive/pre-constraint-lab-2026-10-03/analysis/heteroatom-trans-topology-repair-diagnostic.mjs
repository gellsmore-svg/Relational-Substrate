import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const exposedRows = [
  {
    id: 'disulfane',
    label: 'H-S-S-H',
    centralElement: 'S',
    externalTransCm1: 1958,
    exposedSource: 'disulfane-heteroatom-rotor-comparison.json',
    rowsPath: 'disulfane-heteroatom-rotor-prelookup.json',
    getRows: (payload) => payload.frozenRows,
  },
  {
    id: 'selenane-92',
    label: 'H-Se-Se-H / H-Se-Se angle 92',
    centralElement: 'Se',
    externalTransCm1: 1664.2,
    exposedSource: 'selenane-heteroatom-rotor-comparison.json',
    rowsPath: 'selenane-heteroatom-rotor-prelookup.json',
    getRows: (payload) => payload.bracketResults.find((row) => row.sideAngle === 92).frozenRows,
  },
  {
    id: 'selenane-95',
    label: 'H-Se-Se-H / H-Se-Se angle 95',
    centralElement: 'Se',
    externalTransCm1: 1664.2,
    exposedSource: 'selenane-heteroatom-rotor-comparison.json',
    rowsPath: 'selenane-heteroatom-rotor-prelookup.json',
    getRows: (payload) => payload.bracketResults.find((row) => row.sideAngle === 95).frozenRows,
  },
  {
    id: 'selenane-98',
    label: 'H-Se-Se-H / H-Se-Se angle 98',
    centralElement: 'Se',
    externalTransCm1: 1664.2,
    exposedSource: 'selenane-heteroatom-rotor-comparison.json',
    rowsPath: 'selenane-heteroatom-rotor-prelookup.json',
    getRows: (payload) => payload.bracketResults.find((row) => row.sideAngle === 98).frozenRows,
  },
];

const predeclaredCandidate = {
  id: 'trans_planar_topology_penalty',
  status: 'diagnostic-only exposed-failure calibration; not validation',
  formula:
    'additionalCm1 = coefficientCm1 * transWindow(torsionMean)^2 * antiPlanarRelease * heavyAtomFactor(centralElement)',
  coefficientCm1: 1450,
  transWindow: 'clamp01((torsionMean - 150) / 30); 0 at <=150 degrees, 1 at 180 degrees',
  heavyAtomFactor: {
    S: 1,
    Se: 1,
    default: 0,
  },
  allowedInputs: ['torsionMean', 'antiPlanarRelease', 'centralElement'],
  prohibitedInputs: ['external barrier magnitude for fresh targets', 'post-lookup geometry edits', 'target-specific coefficients'],
  interpretation:
    'Represents a missing topology cost for fully anti-planar heavy-atom H2X2 rotors where the current antiPlanarRelease term incorrectly converts the trans barrier pathway into a shallow local minimum.',
};

function clamp01(value) {
  return Math.max(0, Math.min(1, value));
}

function round(value, digits = 4) {
  return Number(value.toFixed(digits));
}

function topology(rows, key = 'modelCm1') {
  return rows.map((row, index) => {
    const previous = index === 0 ? rows[1] : rows[index - 1];
    const next = index === rows.length - 1 ? rows[rows.length - 2] : rows[index + 1];
    let label = 'neither';
    if (row[key] < previous[key] && row[key] < next[key]) label = 'local-minimum';
    if (row[key] > previous[key] && row[key] > next[key]) label = 'local-maximum';
    return { ...row, topology: label };
  });
}

function heavyAtomFactor(element) {
  return predeclaredCandidate.heavyAtomFactor[element] ?? predeclaredCandidate.heavyAtomFactor.default;
}

function transWindow(torsionMean) {
  return clamp01((torsionMean - 150) / 30);
}

function repairPenalty(row, centralElement) {
  return (
    predeclaredCandidate.coefficientCm1 *
    transWindow(row.torsionMean) ** 2 *
    (row.antiPlanarRelease ?? 0) *
    heavyAtomFactor(centralElement)
  );
}

function evaluateLargeBarrier(modelCm1, externalCm1) {
  const errorPct = ((modelCm1 - externalCm1) / externalCm1) * 100;
  return {
    errorPct: round(errorPct, 2),
    pass35Pct: Math.abs(errorPct) <= 35,
  };
}

function rowMarkdown(rows) {
  const header = '| angle | base cm-1 | added penalty | repaired cm-1 | base topology | repaired topology | anti-planar release |';
  const rule = '|---:|---:|---:|---:|---|---|---:|';
  const body = rows.map((row) => `| ${row.angle} | ${row.modelCm1} | ${row.addedTransPlanarPenaltyCm1} | ${row.repairedCm1} | ${row.topology} | ${row.repairedTopology} | ${row.antiPlanarRelease} |`);
  return [header, rule, ...body].join('\n');
}

async function loadRows(config) {
  const payload = JSON.parse(await readFile(new URL(config.rowsPath, outDir), 'utf8'));
  return config.getRows(payload);
}

const results = [];

for (const config of exposedRows) {
  const baseRows = topology(await loadRows(config));
  const repairedRowsWithoutTopology = baseRows.map((row) => {
    const added = repairPenalty(row, config.centralElement);
    return {
      ...row,
      addedTransPlanarPenaltyCm1: round(added, 2),
      repairedCm1: round(row.modelCm1 + added, 2),
    };
  });
  const repairedRows = topology(repairedRowsWithoutTopology, 'repairedCm1').map((row) => ({
    ...row,
    repairedTopology: row.topology,
    topology: baseRows.find((base) => base.angle === row.angle).topology,
  }));
  const baseTrans = baseRows.find((row) => row.angle === 180);
  const repairedTrans = repairedRows.find((row) => row.angle === 180);
  const baseEval = evaluateLargeBarrier(baseTrans.modelCm1, config.externalTransCm1);
  const repairedEval = evaluateLargeBarrier(repairedTrans.repairedCm1, config.externalTransCm1);

  results.push({
    ...config,
    baseTrans: {
      modelCm1: baseTrans.modelCm1,
      topology: baseTrans.topology,
      ...baseEval,
    },
    repairedTrans: {
      modelCm1: repairedTrans.repairedCm1,
      addedTransPlanarPenaltyCm1: repairedTrans.addedTransPlanarPenaltyCm1,
      topology: repairedTrans.repairedTopology,
      ...repairedEval,
    },
    topologyRepaired: baseTrans.topology === 'local-minimum' && repairedTrans.repairedTopology === 'local-maximum',
    magnitudeRepaired: repairedEval.pass35Pct,
    rows: repairedRows.map((row) => ({
      angle: row.angle,
      modelCm1: row.modelCm1,
      addedTransPlanarPenaltyCm1: row.addedTransPlanarPenaltyCm1,
      repairedCm1: row.repairedCm1,
      topology: row.topology,
      repairedTopology: row.repairedTopology,
      antiPlanarRelease: row.antiPlanarRelease,
    })),
  });
}

const allExposedTopologyRepaired = results.every((result) => result.topologyRepaired);
const allExposedMagnitudeRepaired = results.every((result) => result.magnitudeRepaired);

const payload = {
  status: 'diagnostic-only',
  source: 'heteroatom-trans-topology-repair-diagnostic.mjs',
  predeclaredCandidate,
  exposedFailuresOnly: true,
  validationClaim: false,
  freshTargetRequiredBeforeEvidence: true,
  summary: {
    exposedRows: results.length,
    allExposedTopologyRepaired,
    allExposedMagnitudeRepaired,
    reading:
      'The single trans-planar topology penalty is sufficient on already-exposed failure rows. This is calibration pressure only; it does not recover torsion evidence until a fresh held-out post-redesign target passes unchanged.',
  },
  results,
};

function resultSection(result) {
  return `## ${result.label}

- exposed source: ${result.exposedSource}
- external trans barrier: ${result.externalTransCm1} cm-1
- base trans: ${result.baseTrans.modelCm1} cm-1, ${result.baseTrans.topology}, error ${result.baseTrans.errorPct}%
- repaired trans: ${result.repairedTrans.modelCm1} cm-1, ${result.repairedTrans.topology}, error ${result.repairedTrans.errorPct}%
- topology repaired on exposed row: ${result.topologyRepaired ? 'yes' : 'no'}
- magnitude repaired on exposed row: ${result.magnitudeRepaired ? 'yes' : 'no'}

${rowMarkdown(result.rows)}
`;
}

const md = `# Heteroatom Trans Topology Repair Diagnostic

Status: diagnostic only. This is not a validation pass and does not alter the locked disulfane or H-Se-Se-H comparison results.

## Predeclared Candidate

- descriptor: \`${predeclaredCandidate.id}\`
- formula: \`${predeclaredCandidate.formula}\`
- coefficient: ${predeclaredCandidate.coefficientCm1} cm-1
- trans window: ${predeclaredCandidate.transWindow}
- allowed inputs: ${predeclaredCandidate.allowedInputs.join(', ')}
- prohibited inputs: ${predeclaredCandidate.prohibitedInputs.join(', ')}

Interpretation: ${predeclaredCandidate.interpretation}

## Summary

- exposed rows checked: ${results.length}
- all exposed trans topologies repaired: ${allExposedTopologyRepaired ? 'yes' : 'no'}
- all exposed trans magnitudes within large-barrier tolerance: ${allExposedMagnitudeRepaired ? 'yes' : 'no'}
- evidence status: none; a fresh held-out post-redesign target is required before this can count.

${results.map(resultSection).join('\n')}

## Required Next Gate

Reserve one fresh H2X2-like or adjacent heavy-atom rotor target before lookup. Freeze this exact formula, coefficient, geometry rules, charge rules, grid, and pass/fail criteria before consulting the target. If the fresh target fails, record the failure without adding a second repair term.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('heteroatom-trans-topology-repair-diagnostic.json', outDir), `${JSON.stringify(payload, null, 2)}\n`);
await writeFile(new URL('heteroatom-trans-topology-repair-diagnostic.md', outDir), md);

console.log(md);
