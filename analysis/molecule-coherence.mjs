import { mkdir, writeFile } from 'node:fs/promises';
import { molecules, scoreCandidate } from './molecule-model.mjs';

const outDir = new URL('./out/', import.meta.url);

const results = molecules.map((molecule) => {
  const ranked = [molecule.reference, ...molecule.manualVariants]
    .map((item) => ({ ...item, score: scoreCandidate(item) }))
    .sort((a, b) => b.score - a.score);
  return {
    formula: molecule.formula,
    reading: molecule.reading,
    passed: ranked[0].type === 'reference',
    ranked,
  };
});

const passed = results.filter((result) => result.passed).length;
const failed = results.length - passed;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('molecule-coherence.json', outDir), JSON.stringify({ passed, failed, results }, null, 2));

const markdown = `# AMS Molecule Coherence Bench

## Scope

This is a secondary-regime coherence bench. It does not claim that atoms are vorton species, and it does not place material components between the continuous substrate and vorton formation.

The bench asks whether a simple topology-and-constraint score ranks known-good molecular geometries above nearby strained or incoherent alternatives.

Molecules tested: ${results.length}

Reference geometries ranked first: ${passed}

Failures: ${failed}

## Results

${results
  .map(
    (result) => `### ${result.formula}

${result.reading}

Pass: ${result.passed ? 'yes' : 'no'}

| Rank | Candidate | Type | Score | Valence | Geometry | Angle strain | Bond strain | Polarity | Route | Ring | Steric |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
${result.ranked
  .map(
    (row, index) =>
      `| ${index + 1} | ${row.name} | ${row.type} | ${row.score.toFixed(3)} | ${row.valenceSatisfaction.toFixed(2)} | ${row.geometryFit.toFixed(2)} | ${row.angleStrain.toFixed(2)} | ${row.bondStrain.toFixed(2)} | ${row.polarityBalance.toFixed(2)} | ${row.routeContinuity.toFixed(2)} | ${row.ringClosure.toFixed(2)} | ${row.stericObstruction.toFixed(2)} |`
  )
  .join('\n')}`
  )
  .join('\n\n')}

## First Reading

This first bench passes only because the input variables are hand-calibrated from known chemistry. That is acceptable at this stage. The value is that the scoring language is now explicit and executable.

The next hard test is to move from hand-scored candidates to generated perturbations of bond length, angle, polarity balance, ring closure, and route continuity. If generated known-good candidates do not remain near the top, the weights or variables need correction before any stronger AMS claim is made.
`;

await writeFile(new URL('molecule-coherence-summary.md', outDir), markdown);

console.log(`Molecules tested: ${results.length}`);
console.log(`Reference geometries ranked first: ${passed}`);
console.log(`Failures: ${failed}`);
console.log(`Wrote ${new URL('molecule-coherence-summary.md', outDir).pathname}`);
