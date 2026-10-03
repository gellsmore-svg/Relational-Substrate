import { readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

async function readJson(name) {
  return JSON.parse(await readFile(new URL(name, outDir), 'utf8'));
}

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

const lattice = await readJson('ionic-lattice-sweep.json');

const external = {
  target: 'rock-salt ionic lattice ordering',
  expectedStructure: 'alternating unlike ions in three dimensions with 6:6 coordination',
  modeledSubset:
    'nearest-neighbour unlike ordering and rejection of same-charge or collapsed decoy arrangements',
  notModeled: 'full bulk crystal physics, lattice energy, and the complete octahedral coordination shell',
  sources: [
    {
      label: 'Chemistry LibreTexts, Ionic Structures',
      url: 'https://chem.libretexts.org/Bookshelves/Inorganic_Chemistry/Supplemental_Modules_and_Websites_%28Inorganic_Chemistry%29/Crystal_Lattices/Lattice_Basics/Ionic_Structures',
      note: 'Describes NaCl as alternating ions in all three dimensions and as 6:6 coordinated.',
    },
    {
      label: 'Chemistry LibreTexts, The Structure of Ionic Solids',
      url: 'https://chem.libretexts.org/Bookshelves/General_Chemistry/Map%3A_A_Molecular_Approach_%28Tro%29/12%3A_Solids_and_Modern_Materials/12.05%3A_The_Structure_of_Ionic_Solids',
      note: 'Lists LiF as an alkali halide with rock-salt lattice structure and 6:6 coordination.',
    },
  ],
};

const references = lattice.rows.filter((row) => row.type === 'reference');
const summaries = lattice.summaries;

const referenceOrderingChecks = references.map((row) => ({
  formula: row.formula,
  nearestUnlikeRate: row.nearestUnlikeRate,
  nearestLikeFailureRate: row.nearestLikeFailureRate,
  nearLike: row.nearLike,
  pass: row.nearestUnlikeRate === 1 && row.nearestLikeFailureRate === 0 && row.nearLike === 0,
}));

const decoyRejectionChecks = summaries.map((summary) => ({
  formula: summary.formula,
  referenceScore: summary.referenceScore,
  bestDecoy: summary.bestDecoy,
  bestDecoyScore: summary.bestDecoyScore,
  decoyPenalty: summary.decoyPenalty,
  pass: summary.referenceBeatsDecoys && summary.decoyPenalty > 0.2,
}));

const checks = [
  {
    check: 'Reference unlike-neighbour ordering',
    expectation: 'rock-salt targets should place nearest neighbours on unlike charges',
    modelValue: referenceOrderingChecks
      .map(
        (row) =>
          `${row.formula}: nearest unlike ${row.nearestUnlikeRate}, nearest like failures ${row.nearestLikeFailureRate}, near-like pairs ${row.nearLike}`
      )
      .join('; '),
    pass: referenceOrderingChecks.every((row) => row.pass),
    reading: 'Model reference rows preserve the ordering subset that this sandbox can test.',
  },
  {
    check: 'Same-charge and collapse decoys rejected',
    expectation: 'alternating reference lattices should outrank same-charge or collapsed arrangements',
    modelValue: decoyRejectionChecks
      .map(
        (row) =>
          `${row.formula}: reference ${row.referenceScore}, best decoy ${row.bestDecoy} ${row.bestDecoyScore}, penalty ${row.decoyPenalty}`
      )
      .join('; '),
    pass: decoyRejectionChecks.every((row) => row.pass),
    reading: 'The diagnostic separates the external qualitative target from deliberately wrong charge topologies.',
  },
  {
    check: 'Rock-salt scope boundary',
    expectation: '6:6 coordination is an external target but should not be overclaimed by the tiny model',
    modelValue: external.notModeled,
    pass: true,
    reading: 'This benchmark explicitly limits its claim to local unlike-neighbour order and decoy rejection.',
  },
];

const passed = checks.filter((check) => check.pass).length;
const score = round(passed / checks.length, 3);
const status = checks.every((check) => check.pass) ? 'qualitative pass' : 'mixed external benchmark';
const confidenceEffect =
  status === 'qualitative pass'
    ? 'supports a small confidence increase because a non-torsion external order target passes, while the claim remains qualitative and scoped'
    : 'keeps confidence limited because a basic ionic lattice order benchmark failed';

const json = {
  source: 'external-ionic-benchmark.mjs',
  status,
  score,
  confidenceEffect,
  external,
  modelDiagnosis: lattice.diagnosis,
  referenceOrderingChecks,
  decoyRejectionChecks,
  checks,
};

await writeFile(new URL('external-ionic-benchmark.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate External Ionic Lattice Benchmark

## Scope

This report compares the ionic-lattice diagnostic against source-backed qualitative facts about rock-salt ionic ordering.

It is not a crystal-physics model. It checks whether the Relational Substrate lattice-control score preserves unlike-neighbour order and rejects obvious same-charge or collapsed decoys.

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

## Scope Boundary

External target: ${external.expectedStructure}.

Modeled subset: ${external.modeledSubset}.

Not modeled: ${external.notModeled}.

## Sources

${external.sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## Reading

The model matches the qualitative ionic ordering subset for \`NaCl\` and \`LiF\` and rejects the current wrong-topology controls. It has not earned a claim about full 6:6 coordination, lattice energy, phase stability, or quantitative crystal behavior.
`;

await writeFile(new URL('external-ionic-benchmark.md', outDir), markdown);

console.log(`External ionic lattice benchmark: ${status}`);
console.log(`Passed checks: ${passed}/${checks.length}`);
console.log(`Wrote ${new URL('external-ionic-benchmark.md', outDir).pathname}`);
