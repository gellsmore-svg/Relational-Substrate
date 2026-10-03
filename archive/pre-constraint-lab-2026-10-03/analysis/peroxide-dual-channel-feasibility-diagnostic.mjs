import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

async function readJson(name) {
  return JSON.parse(await readFile(new URL(name, outDir), 'utf8'));
}

function round(value, digits = 4) {
  return Number(value.toFixed(digits));
}

function pctError(model, target) {
  return ((model - target) / target) * 100;
}

const predeclaration = await readJson('peroxide-dual-channel-model-form-predeclaration.json');
const sensitivity = await readJson('peroxide-anti-planar-release-sensitivity.json');
const h2o2Absolute = await readJson('external-h2o2-absolute-barrier-benchmark.json');

const frozen = predeclaration.frozenModelForm;
const energy = sensitivity.summaries.find(
  (row) =>
    row.release.strength === frozen.energyChannel.releaseStrength &&
    row.release.onset === frozen.energyChannel.releaseOnsetDegrees &&
    row.release.span === frozen.energyChannel.releaseSpanDegrees,
);
const selection = sensitivity.summaries.find(
  (row) =>
    row.release.strength === 0 &&
    row.release.onset === frozen.energyChannel.releaseOnsetDegrees &&
    row.release.span === frozen.energyChannel.releaseSpanDegrees,
);

if (!energy || !selection) {
  throw new Error('Frozen energy or unreleased selection row is missing from the sensitivity grid.');
}

const scale = h2o2Absolute.scale.cm1PerPenalty;
const energyTransCm1 = energy.transPenalty * scale;
const energyCisCm1 = energy.cisPenalty * scale;
const externalTransCm1 = h2o2Absolute.external.transBarrierCm1;
const externalCisCm1 = h2o2Absolute.external.cisBarrierCm1;
const barrierTolerancePct = h2o2Absolute.external.barrierTolerancePct;
const energyTransErrorPct = pctError(energyTransCm1, externalTransCm1);
const energyCisErrorPct = pctError(energyCisCm1, externalCisCm1);

const checks = [
  {
    check: 'selection nonlocal separation',
    pass: selection.nonlocalWeakest >= 0.1,
    value: selection.nonlocalWeakest,
    requirement: '>= 0.10',
  },
  {
    check: 'selection local tolerance',
    pass: selection.nearWeakest <= 0.05,
    value: selection.nearWeakest,
    requirement: '<= 0.05',
  },
  {
    check: 'energy trans barrier remains within existing tolerance',
    pass: Math.abs(energyTransErrorPct) <= barrierTolerancePct,
    value: `${round(energyTransCm1, 2)} cm-1 (${round(energyTransErrorPct, 2)}%)`,
    requirement: `${externalTransCm1} cm-1 +/- ${barrierTolerancePct}%`,
  },
  {
    check: 'energy cis barrier remains within existing tolerance',
    pass: Math.abs(energyCisErrorPct) <= barrierTolerancePct,
    value: `${round(energyCisCm1, 2)} cm-1 (${round(energyCisErrorPct, 2)}%)`,
    requirement: `${externalCisCm1} cm-1 +/- ${barrierTolerancePct}%`,
  },
  {
    check: 'selection channel does not alter energy channel',
    pass: energy.key === sensitivity.current.key,
    value: energy.key,
    requirement: sensitivity.current.key,
  },
];

const passed = checks.every((check) => check.pass);
const report = {
  source: 'peroxide-dual-channel-feasibility-diagnostic.mjs',
  date: '2026-06-23',
  status: passed ? 'exposed-feasibility-pass' : 'exposed-feasibility-fail',
  validationClaim: false,
  evidenceStatus: 'none; H2O2 is already exposed',
  predeclarationHash: predeclaration.predeclaration.hash,
  channels: {
    energy: {
      release: energy.release,
      nonlocalWeakest: energy.nonlocalWeakest,
      transPenalty: energy.transPenalty,
      cisPenalty: energy.cisPenalty,
      transBarrierCm1: round(energyTransCm1, 2),
      cisBarrierCm1: round(energyCisCm1, 2),
    },
    selection: {
      rule: frozen.selectionChannel.formula,
      newCoefficients: frozen.selectionChannel.newCoefficients,
      nearWeakest: selection.nearWeakest,
      shoulderWeakest: selection.shoulderWeakest,
      nonlocalWeakest: selection.nonlocalWeakest,
      nonlocalWeakestAngle: selection.nonlocalWeakestAngle,
      transPenalty: selection.transPenalty,
    },
  },
  checks,
  decision: passed
    ? 'the two-channel form resolves the exposed shape/energy conflict by construction and may proceed to fresh-target reservation'
    : 'do not reserve a fresh target; revise or reject the model form without changing live energy parameters',
  liveParameterAction: 'retain strength=0.65, onset=145, span=35 for the energy channel',
  nextGate: passed
    ? 'reserve one fresh peroxide-like rotor before lookup and test both frozen channels unchanged'
    : 'none until exposed feasibility passes',
};

const markdown = `# Peroxide Dual-Channel Feasibility Diagnostic

Status: **${report.status}**

This uses already-exposed H2O2 rows. It tests model-form feasibility only and
adds no evidence.

## Results

| Channel/check | Requirement | Value | Result |
|---|---|---|---|
${checks
  .map((check) => `| ${check.check} | ${check.requirement} | ${check.value} | ${check.pass ? 'pass' : 'fail'} |`)
  .join('\n')}

## Channel Separation

- Energy channel: live release strength 0.65, onset 145 degrees, span 35 degrees.
- Selection channel: unreleased torsion mismatch through the existing family score.
- New fitted coefficients: ${frozen.selectionChannel.newCoefficients}.
- Selection penalty is not converted to energy.

The selection frontier moves from ${energy.nonlocalWeakest} to
${selection.nonlocalWeakest}, while the energy-channel trans barrier remains
${round(energyTransCm1, 2)} cm-1 and the cis barrier remains
${round(energyCisCm1, 2)} cm-1.

Decision: ${report.decision}.

Live parameter action: ${report.liveParameterAction}.

Next gate: ${report.nextGate}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-dual-channel-feasibility-diagnostic.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(new URL('peroxide-dual-channel-feasibility-diagnostic.md', outDir), markdown);

console.log(`Peroxide dual-channel feasibility: ${report.status}`);
console.log(`Selection nonlocal weakest: ${selection.nonlocalWeakest}`);
console.log(`Energy trans barrier: ${round(energyTransCm1, 2)} cm-1`);
