import { readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const cm1PerKcalMol = 349.755;

async function readJson(name) {
  return JSON.parse(await readFile(new URL(name, outDir), 'utf8'));
}

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

function pctError(model, external) {
  return ((model - external) / external) * 100;
}

const h2o2 = await readJson('external-h2o2-quantitative-benchmark.json');
const ethane = await readJson('external-ethane-quantitative-benchmark.json');

const external = {
  molecule: 'H2O2',
  target: 'absolute peroxide torsional barrier transfer check',
  scaleSource: 'ethane quantitative benchmark kcal-per-penalty scale; no H2O2 endpoint fitting',
  transBarrierCm1: h2o2.external.transBarrierCm1,
  cisBarrierCm1: h2o2.external.cisBarrierCm1,
  barrierTolerancePct: 15,
  ratioTolerancePct: 15,
  sources: h2o2.external.sources,
};

const scale = {
  ethaneBarrierPenalty: ethane.scale.barrierPenalty,
  kcalPerPenalty: ethane.scale.kcalPerPenalty,
  cm1PerPenalty: ethane.scale.kcalPerPenalty * cm1PerKcalMol,
};

function barrierRow(label, penalty, externalCm1) {
  const modelKcalMol = penalty * scale.kcalPerPenalty;
  const modelCm1 = modelKcalMol * cm1PerKcalMol;
  const errorPct = pctError(modelCm1, externalCm1);

  return {
    label,
    modelPenalty: penalty,
    modelKcalMol: round(modelKcalMol, 4),
    modelCm1: round(modelCm1, 2),
    externalCm1,
    errorPct: round(errorPct, 2),
    absoluteErrorPct: round(Math.abs(errorPct), 2),
    pass: Math.abs(errorPct) <= external.barrierTolerancePct,
  };
}

const trans = barrierRow('trans barrier', h2o2.metrics.transPenalty, external.transBarrierCm1);
const cis = barrierRow('cis barrier', h2o2.metrics.cisPenalty, external.cisBarrierCm1);
const modelRatio = trans.modelCm1 > 0 ? cis.modelCm1 / trans.modelCm1 : 0;
const externalRatio = external.cisBarrierCm1 / external.transBarrierCm1;
const ratioErrorPct = pctError(modelRatio, externalRatio);

const checks = [
  {
    check: 'No H2O2 endpoint fitting',
    expectation: 'energy scale should transfer from ethane rather than using trans or cis H2O2 as an anchor',
    modelValue: `${round(scale.kcalPerPenalty, 3)} kcal/mol per penalty from ethane; ${round(scale.cm1PerPenalty, 1)} cm-1 per penalty`,
    pass: true,
    reading: 'This is a transfer-scale falsification check, not a fitted peroxide energy surface.',
  },
  {
    check: 'Transferred trans barrier',
    expectation: `${external.transBarrierCm1} cm-1 +/- ${external.barrierTolerancePct}%`,
    modelValue: `${trans.modelCm1} cm-1; error ${trans.errorPct}%`,
    pass: trans.pass,
    reading:
      'The transferred scale overpredicts the low trans barrier, so the current grammar does not recover the shallow peroxide barrier floor.',
  },
  {
    check: 'Transferred cis barrier',
    expectation: `${external.cisBarrierCm1} cm-1 +/- ${external.barrierTolerancePct}%`,
    modelValue: `${cis.modelCm1} cm-1; error ${cis.errorPct}%`,
    pass: cis.pass,
    reading:
      'The same transferred scale lands close to the high cis barrier, which localizes the discrepancy to relative barrier structure rather than complete energy-scale failure.',
  },
  {
    check: 'Transferred cis/trans ratio',
    expectation: `${round(externalRatio, 3)} +/- ${external.ratioTolerancePct}%`,
    modelValue: `${round(modelRatio, 3)}; error ${round(ratioErrorPct, 2)}%`,
    pass: Math.abs(ratioErrorPct) <= external.ratioTolerancePct,
    reading:
      'The ratio remains compressed because the trans barrier is too high relative to cis under a scale not fitted to peroxide.',
  },
  {
    check: 'Limitation promoted',
    expectation: 'a mixed result should reduce confidence or hold it flat rather than be counted as a new convergence pass',
    modelValue: 'status is absolute barrier mixed diagnostic',
    pass: true,
    reading:
      'This benchmark converts the H2O2 caveat into an explicit falsification pressure point for the next grammar revision.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = round(passed / checks.length, 3);
const status = checks.every((check) => check.pass) ? 'absolute barrier pass' : 'absolute barrier mixed diagnostic';
const confidenceEffect =
  status === 'absolute barrier pass'
    ? 'would support a material confidence increase because an ethane-derived energy scale transfers to both H2O2 barriers'
    : 'limits confidence because the ethane-derived scale overpredicts the H2O2 trans barrier while matching the cis barrier, preserving the ratio-compression limitation';

const json = {
  source: 'external-h2o2-absolute-barrier-benchmark.mjs',
  status,
  score,
  confidenceEffect,
  external,
  scale: {
    ...scale,
    kcalPerPenalty: round(scale.kcalPerPenalty, 4),
    cm1PerPenalty: round(scale.cm1PerPenalty, 2),
  },
  metrics: {
    trans,
    cis,
    modelCisToTransRatio: round(modelRatio, 4),
    externalCisToTransRatio: round(externalRatio, 4),
    ratioErrorPct: round(ratioErrorPct, 2),
  },
  checks,
};

await writeFile(new URL('external-h2o2-absolute-barrier-benchmark.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate External H2O2 Absolute Barrier Benchmark

## Scope

This report promotes the H2O2 compression caveat into an explicit transfer-scale falsification check.

It uses the kcal-per-penalty scale already exposed by the ethane quantitative benchmark and applies that scale to the H2O2 trans and cis penalties. It does not fit either H2O2 endpoint. It is therefore stricter than the earlier H2O2 ratio-shape benchmark.

## Result

| Measure | Value |
|---|---:|
| Status | ${status} |
| Passed checks | ${passed}/${checks.length} |
| Score | ${score} |
| Trans model barrier | ${trans.modelCm1} cm-1 |
| Trans external barrier | ${trans.externalCm1} cm-1 |
| Trans error | ${trans.errorPct}% |
| Cis model barrier | ${cis.modelCm1} cm-1 |
| Cis external barrier | ${cis.externalCm1} cm-1 |
| Cis error | ${cis.errorPct}% |
| Model cis/trans ratio | ${round(modelRatio, 3)} |
| External cis/trans ratio | ${round(externalRatio, 3)} |
| Ratio error | ${round(ratioErrorPct, 2)}% |
| Confidence effect | ${confidenceEffect} |

## Checks

| Check | Expectation | Model value | Pass | Reading |
|---|---|---|---|---|
${checks.map((check) => `| ${check.check} | ${check.expectation} | ${check.modelValue} | ${check.pass ? 'yes' : 'no'} | ${check.reading} |`).join('\n')}

## Barrier Rows

| Barrier | Model penalty | Model kcal/mol | Model cm-1 | External cm-1 | Error | Pass |
|---|---:|---:|---:|---:|---:|---|
| ${trans.label} | ${trans.modelPenalty} | ${trans.modelKcalMol} | ${trans.modelCm1} | ${trans.externalCm1} | ${trans.errorPct}% | ${trans.pass ? 'yes' : 'no'} |
| ${cis.label} | ${cis.modelPenalty} | ${cis.modelKcalMol} | ${cis.modelCm1} | ${cis.externalCm1} | ${cis.errorPct}% | ${cis.pass ? 'yes' : 'no'} |

## Sources

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

This is not a new pass. The transferred ethane scale predicts the H2O2 cis barrier closely but overpredicts the trans barrier by ${trans.errorPct}%. That preserves the known cis/trans compression and makes it more specific: the current grammar produces a high-strain cis closure cost on roughly the right absolute scale, but it does not recover the shallow trans barrier floor. The next peroxide revision should therefore target relative closure/phase scaling near planar trans, not broad energy rescaling.
`;

await writeFile(new URL('external-h2o2-absolute-barrier-benchmark.md', outDir), markdown);

console.log(`External H2O2 absolute barrier benchmark: ${status}`);
console.log(`Passed checks: ${passed}/${checks.length}`);
console.log(`Trans error: ${trans.errorPct}%`);
console.log(`Cis error: ${cis.errorPct}%`);
console.log(`Wrote ${new URL('external-h2o2-absolute-barrier-benchmark.md', outDir).pathname}`);
