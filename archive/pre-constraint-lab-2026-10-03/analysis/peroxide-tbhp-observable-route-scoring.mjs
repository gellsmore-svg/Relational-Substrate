import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const extraction = JSON.parse(
  await readFile(new URL('peroxide-tbhp-source-extraction.json', outDir), 'utf8'),
);

function clamp01(value) {
  return Math.max(0, Math.min(1, value));
}

function cyclicDifference(value, target, period = 360) {
  return Math.abs(((value - target + period / 2) % period) - period / 2);
}

function selectionDistance(candidate, reference) {
  return clamp01(cyclicDifference(candidate, reference) / 45);
}

function energyPenalty(alpha, equilibrium) {
  const torsionDeviation = clamp01(cyclicDifference(alpha, equilibrium) / 45);
  const cisCrowding = clamp01((60 - alpha) / 60);
  const antiPlanarRelease =
    clamp01((alpha - 145) / 35) * clamp01(1 - cisCrowding);
  const effectiveTorsionDeviation =
    torsionDeviation * (1 - antiPlanarRelease * 0.65);
  return clamp01(effectiveTorsionDeviation * 0.42 + cisCrowding * 0.58);
}

const equilibrium = extraction.torsionConstruct.equilibriumDegrees;
const trans = extraction.torsionConstruct.transBarrierCoordinateDegrees;
const equilibriumSelection = selectionDistance(equilibrium, equilibrium);
const transSelection = selectionDistance(trans, equilibrium);
const equilibriumEnergyPenalty = energyPenalty(equilibrium, equilibrium);
const transEnergyPenalty = energyPenalty(trans, equilibrium);

const checks = [
  {
    check: 'selection ranks equilibrium above trans route',
    pass: equilibriumSelection < transSelection,
    value: `${equilibriumSelection} < ${transSelection}`,
  },
  {
    check: 'trans route clears nonlocal threshold',
    pass: transSelection === 1,
    value: transSelection,
  },
  {
    check: 'energy channel preserves source ordering',
    pass: equilibriumEnergyPenalty < transEnergyPenalty,
    value: `${equilibriumEnergyPenalty.toFixed(4)} < ${transEnergyPenalty.toFixed(4)}`,
  },
  {
    check: 'source models agree on positive trans barrier',
    pass:
      extraction.barrierComparators.groundStateLmCm1 > 0 &&
      extraction.barrierComparators.groundStateRpCm1 > 0,
    value: `${extraction.barrierComparators.groundStateLmCm1}, ${extraction.barrierComparators.groundStateRpCm1} cm-1`,
  },
];

const passed = checks.every((check) => check.pass);
const report = {
  source: 'peroxide-tbhp-observable-route-scoring.mjs',
  date: '2026-06-23',
  status: passed ? 'heldout-observable-route-comparator-pass' : 'heldout-observable-route-comparator-fail',
  predeclarationHash: extraction.target.predeclarationHash,
  frozenParameters: {
    selectionToleranceDegrees: 45,
    releaseStrength: 0.65,
    releaseOnsetDegrees: 145,
    releaseSpanDegrees: 35,
  },
  sourceComparators: {
    equilibriumDegrees: equilibrium,
    transDegrees: trans,
    groundStateLmCm1: extraction.barrierComparators.groundStateLmCm1,
    groundStateRpCm1: extraction.barrierComparators.groundStateRpCm1,
  },
  predictions: {
    equilibriumSelection,
    transSelection,
    equilibriumEnergyPenalty: Number(equilibriumEnergyPenalty.toFixed(4)),
    transEnergyPenalty: Number(transEnergyPenalty.toFixed(4)),
  },
  checks,
  evidenceStatus:
    'held-out computed-comparator pass with experimental torsional-construct support; not experimental absolute-barrier validation',
  confidenceAction: 'branch-level support only; no automatic global confidence change',
};

const markdown = `# TBHP Observable-Route Scoring

Status: **${report.status}**

| Check | Value | Result |
|---|---|---|
${checks.map((row) => `| ${row.check} | ${row.value} | ${row.pass ? 'pass' : 'fail'} |`).join('\n')}

The frozen selection distance is ${transSelection} for the source trans route.
The unchanged energy channel assigns a larger penalty to the trans route than
to the source equilibrium.

Evidence status: ${report.evidenceStatus}.

Confidence action: ${report.confidenceAction}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-tbhp-observable-route-scoring.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(new URL('peroxide-tbhp-observable-route-scoring.md', outDir), markdown);

console.log(`TBHP observable-route scoring: ${report.status}`);
