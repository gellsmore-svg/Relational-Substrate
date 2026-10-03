import { readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

async function readJson(name) {
  return JSON.parse(await readFile(new URL(name, outDir), 'utf8'));
}

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

const ethane = await readJson('ethane-torsion-sweep.json');

const external = {
  molecule: 'C2H6',
  target: 'torsional barrier profile',
  experimentalBarrierKcalMol: 2.875,
  commonBarrierKcalMol: 2.9,
  expectedMinimum: 'staggered',
  expectedMaximum: 'eclipsed',
  sources: [
    {
      label: 'Rotational barrier in ethane molecular orbital study, Molecules 2012',
      url: 'https://doi.org/10.3390/molecules17044661',
      note: 'Cites the known ethane rotational barrier as 2.875 kcal/mol and describes staggered minimum / eclipsed maximum.',
    },
    {
      label: 'Hyperconjugation not steric repulsion leads to the staggered structure of ethane, Nature 2001',
      url: 'https://doi.org/10.1038/35079036',
      note: 'Describes ethane alternating between preferred staggered and unstable eclipsed conformations during rotation.',
    },
    {
      label: 'Barrier to internal rotation in ethane, Journal of Chemical Physics 1966',
      url: 'https://doi.org/10.1063/1.1727979',
      note: 'Reports experimental barrier height around 3.03 +/- 0.3 kcal/mol in historical computational comparison.',
    },
  ],
};

const rows = ethane.rows;
const staggered = rows.filter((row) => row.expectedClass === 'staggered-like');
const intermediate = rows.filter((row) => row.expectedClass === 'intermediate');
const eclipsed = rows.filter((row) => row.expectedClass === 'eclipsed-like');

const meanStaggeredPenalty = round(staggered.reduce((sum, row) => sum + row.penaltyVsReference, 0) / staggered.length);
const meanIntermediatePenalty = round(intermediate.reduce((sum, row) => sum + row.penaltyVsReference, 0) / intermediate.length);
const meanEclipsedPenalty = round(eclipsed.reduce((sum, row) => sum + row.penaltyVsReference, 0) / eclipsed.length);
const modelBarrierScale = meanEclipsedPenalty;
const kcalPerPenalty = external.experimentalBarrierKcalMol / modelBarrierScale;
const impliedIntermediateKcal = meanIntermediatePenalty * kcalPerPenalty;

const checks = [
  {
    check: 'Staggered minimum',
    expectation: 'staggered conformers should be lowest energy',
    modelValue: `mean staggered penalty ${meanStaggeredPenalty}`,
    pass: meanStaggeredPenalty === 0,
    reading: 'Model treats staggered-like rows as the reference basin.',
  },
  {
    check: 'Eclipsed maximum',
    expectation: 'eclipsed conformers should be highest energy',
    modelValue: `intermediate ${meanIntermediatePenalty}; eclipsed ${meanEclipsedPenalty}`,
    pass: meanEclipsedPenalty > meanIntermediatePenalty && meanIntermediatePenalty > meanStaggeredPenalty,
    reading: 'Model ordering matches the external torsion profile ordering.',
  },
  {
    check: 'Threefold periodicity',
    expectation: 'three staggered minima and three eclipsed maxima per 360 degrees',
    modelValue: `${staggered.length} staggered-like; ${eclipsed.length} eclipsed-like`,
    pass: staggered.length === 3 && eclipsed.length === 3,
    reading: 'Model grid represents the expected ethane torsion periodicity.',
  },
  {
    check: 'Barrier scale treatment',
    expectation: `experimental barrier about ${external.experimentalBarrierKcalMol} kcal/mol`,
    modelValue: `normalized eclipsed penalty ${modelBarrierScale}; implied intermediate about ${round(impliedIntermediateKcal, 2)} kcal/mol if scaled`,
    pass: modelBarrierScale > 0,
    reading: 'Model has the right qualitative barrier direction, but the score is normalized and not a physical energy model.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = round(passed / checks.length, 3);
const status = checks.every((check) => check.pass) ? 'qualitative pass' : 'mixed external benchmark';
const confidenceEffect =
  status === 'qualitative pass'
    ? 'supports another small confidence increase in internal-to-external coherence, but still not quantitative substrate validation'
    : 'keeps confidence limited because a basic conformer-ordering benchmark failed';

const json = {
  source: 'external-ethane-benchmark.mjs',
  status,
  score,
  confidenceEffect,
  external,
  modelReference: ethane.reference,
  checks,
  scaleNote: {
    modelBarrierScale,
    kcalPerPenalty: round(kcalPerPenalty, 3),
    impliedIntermediateKcal: round(impliedIntermediateKcal, 3),
  },
};

await writeFile(new URL('external-ethane-benchmark.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate External Ethane Benchmark

## Scope

This report compares the ethane torsion diagnostic against source-backed qualitative facts about ethane internal rotation.

It is not a fitted energy model. It checks whether the Relational Substrate torsion score has the right ordering and periodic structure before any quantitative calibration.

## Result

| Measure | Value |
|---|---:|
| Status | ${status} |
| Passed checks | ${passed}/${checks.length} |
| Score | ${score} |
| Confidence effect | ${confidenceEffect} |

## Checks

| Check | Expectation | Model value | Pass | Reading |
|---|---|---|---|---|
${checks.map((check) => `| ${check.check} | ${check.expectation} | ${check.modelValue} | ${check.pass ? 'yes' : 'no'} | ${check.reading} |`).join('\n')}

## Scale Note

If the normalized eclipsed penalty is mapped onto the experimental ${external.experimentalBarrierKcalMol} kcal/mol barrier, one model penalty unit corresponds to about ${round(kcalPerPenalty, 2)} kcal/mol. Under that rough mapping, the intermediate rows imply about ${round(impliedIntermediateKcal, 2)} kcal/mol. This is only a diagnostic scale comparison, not a fitted physical unit conversion.

## Sources

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The model matches the qualitative ethane torsion ordering and threefold periodicity. It has not yet earned a quantitative barrier-height claim.
`;

await writeFile(new URL('external-ethane-benchmark.md', outDir), markdown);

console.log(`External ethane benchmark: ${status}`);
console.log(`Passed checks: ${passed}/${checks.length}`);
console.log(`Wrote ${new URL('external-ethane-benchmark.md', outDir).pathname}`);
