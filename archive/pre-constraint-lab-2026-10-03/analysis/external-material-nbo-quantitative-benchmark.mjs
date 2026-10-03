import { readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

async function readJson(name) {
  return JSON.parse(await readFile(new URL(name, outDir), 'utf8'));
}

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

const nbo = await readJson('material-nbo-stoichiometry.json');

const external = {
  target: 'quantitative NBO/T charge-balance accounting',
  tolerance: {
    nboTAbsoluteErrorMax: 0,
    chargeBalancedAlErrorMax: 0,
  },
  sources: [
    {
      label: 'Stebbins and Xu, Nature 1997',
      url: 'https://www.nature.com/articles/36312',
      note: 'Defines BO/NBO roles, modifier cations, and aluminium charge compensation in aluminosilicate networks.',
    },
    {
      label: 'Walkley et al., PLOS One 2021',
      url: 'https://doi.org/10.1371/journal.pone.0244621',
      note: 'Uses NBO/T as a composition-derived parameter for aluminosilicate glass reactivity.',
    },
    {
      label: 'Mysen and Richet, Nature 1997',
      url: 'https://www.nature.com/articles/36199',
      note: 'Describes charge-balancing cations near aluminium and excess modifier charge forming NBOs that depolymerize the network.',
    },
  ],
};

const checks = [
  {
    check: 'NBO/T exact composition tolerance',
    expectation: `absolute NBO/T error <= ${external.tolerance.nboTAbsoluteErrorMax}`,
    modelValue: nbo.rows.map((row) => `${row.formula}: error ${row.nboTError}`).join('; '),
    pass: nbo.rows.every((row) => row.nboTError <= external.tolerance.nboTAbsoluteErrorMax),
    reading: 'The model matches the integer charge-balance NBO/T targets for all held-out compositions.',
  },
  {
    check: 'Aluminium charge compensation exact tolerance',
    expectation: `charge-balanced Al error <= ${external.tolerance.chargeBalancedAlErrorMax}`,
    modelValue: nbo.rows.map((row) => `${row.formula}: error ${row.chargeBalancedAlError}`).join('; '),
    pass: nbo.rows.every((row) => row.chargeBalancedAlError <= external.tolerance.chargeBalancedAlErrorMax),
    reading: 'The aluminosilicate case assigns modifier charge to aluminium before creating NBO excess.',
  },
  {
    check: 'Diagnostic checks pass',
    expectation: 'all internal NBO/T accounting checks pass',
    modelValue: `${nbo.checks.filter((check) => check.pass).length}/${nbo.checks.length}`,
    pass: nbo.checks.every((check) => check.pass),
    reading: 'The quantitative composition diagnostic agrees with the external benchmark checks.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = round(passed / checks.length, 3);
const status = checks.every((check) => check.pass) ? 'quantitative material pass' : 'mixed quantitative material benchmark';
const confidenceEffect =
  status === 'quantitative material pass'
    ? 'supports a small confidence increase because material accounting now includes an exact quantitative NBO/T target'
    : 'limits confidence because quantitative material charge-balance accounting failed';

const json = {
  source: 'external-material-nbo-quantitative-benchmark.mjs',
  status,
  score,
  confidenceEffect,
  external,
  rows: nbo.rows,
  checks,
};

await writeFile(new URL('external-material-nbo-quantitative-benchmark.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate External Material NBO/T Quantitative Benchmark

## Scope

This report adds a quantitative material benchmark beyond graph-level ordering: exact NBO/T charge-balance accounting for simple silicate and aluminosilicate compositions.

It does not predict measured glass properties. It verifies that the model's composition accounting can represent the structural variable often used before property correlations are attempted.

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

## Composition Rows

| Formula | NBO/T | Expected NBO/T | NBO/T error | Charge-balanced Al | Charge-balanced Al error |
|---|---:|---:|---:|---:|---:|
${nbo.rows
  .map(
    (row) =>
      `| ${row.formula} | ${row.nboT} | ${row.expectedNboT} | ${row.nboTError} | ${row.chargeBalancedAl} | ${row.chargeBalancedAlError} |`
  )
  .join('\n')}

## Sources

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The material benchmark now includes one exact quantitative composition target. This improves material anchoring, but it is still upstream of actual viscosity, durability, conductivity, or density prediction.
`;

await writeFile(new URL('external-material-nbo-quantitative-benchmark.md', outDir), markdown);

console.log(`External material NBO/T benchmark: ${status}`);
console.log(`Passed checks: ${passed}/${checks.length}`);
console.log(`Wrote ${new URL('external-material-nbo-quantitative-benchmark.md', outDir).pathname}`);
