import { mkdir, writeFile } from 'node:fs/promises';
import { clamp01 } from './molecule-model.mjs';

const outDir = new URL('./out/', import.meta.url);

const cases = [
  {
    name: 'polished optical boundary',
    interfaceType: 'low roughness visible-light proxy',
    roughnessRatio: 0.025,
    expectedSpecular: 0.94,
    expectedDiffuse: 0.06,
    routeBase: 0.72,
  },
  {
    name: 'micro-rough glass boundary',
    interfaceType: 'near-Rayleigh roughness proxy',
    roughnessRatio: 0.14,
    expectedSpecular: 0.58,
    expectedDiffuse: 0.42,
    routeBase: 0.68,
  },
  {
    name: 'matte rough boundary',
    interfaceType: 'high roughness scattering proxy',
    roughnessRatio: 0.42,
    expectedSpecular: 0.16,
    expectedDiffuse: 0.84,
    routeBase: 0.64,
  },
];

const variants = [
  {
    name: 'specular coherent reflection',
    kind: 'candidate',
    specularOrder: 0.94,
    diffuseOrder: 0.08,
    phaseMemory: 0.9,
    angleCoherence: 0.88,
    scatterWidth: 0.1,
    surfaceRandomness: 0.08,
  },
  {
    name: 'micro-rough mixed scatter',
    kind: 'candidate',
    specularOrder: 0.58,
    diffuseOrder: 0.42,
    phaseMemory: 0.58,
    angleCoherence: 0.62,
    scatterWidth: 0.44,
    surfaceRandomness: 0.36,
  },
  {
    name: 'diffuse rough scatter',
    kind: 'candidate',
    specularOrder: 0.16,
    diffuseOrder: 0.86,
    phaseMemory: 0.22,
    angleCoherence: 0.28,
    scatterWidth: 0.82,
    surfaceRandomness: 0.78,
  },
  {
    name: 'phase-randomized false specular',
    kind: 'decoy',
    specularOrder: 0.72,
    diffuseOrder: 0.22,
    phaseMemory: 0.18,
    angleCoherence: 0.7,
    scatterWidth: 0.46,
    surfaceRandomness: 0.68,
  },
  {
    name: 'overdiffuse polished surface',
    kind: 'decoy',
    specularOrder: 0.28,
    diffuseOrder: 0.78,
    phaseMemory: 0.32,
    angleCoherence: 0.24,
    scatterWidth: 0.78,
    surfaceRandomness: 0.24,
  },
];

function scoreVariant(testCase, variant) {
  const specularError = Math.abs(variant.specularOrder - testCase.expectedSpecular);
  const diffuseError = Math.abs(variant.diffuseOrder - testCase.expectedDiffuse);
  const splitFit = clamp01(1 - (specularError * 0.52 + diffuseError * 0.48));
  const roughnessFit = clamp01(
    1 - Math.abs(variant.surfaceRandomness - clamp01(testCase.roughnessRatio / 0.42)) * 0.82
  );
  const coherenceFit = clamp01(
    variant.phaseMemory * (1 - testCase.roughnessRatio) +
      variant.diffuseOrder * clamp01(testCase.roughnessRatio / 0.42) -
      variant.surfaceRandomness * Math.max(0, 0.18 - testCase.roughnessRatio)
  );
  const angularDiscipline = clamp01(
    variant.angleCoherence * testCase.expectedSpecular +
      variant.scatterWidth * testCase.expectedDiffuse +
      splitFit * 0.18
  );
  const routeContinuity = clamp01(
    testCase.routeBase + splitFit * 0.13 + roughnessFit * 0.1 + coherenceFit * 0.08 - specularError * 0.18
  );
  const falseOrderRisk = clamp01(
    (1 - splitFit) * 0.34 +
      (1 - roughnessFit) * 0.24 +
      Math.max(0, variant.specularOrder - variant.phaseMemory) * 0.24 +
      specularError * 0.18
  );
  const score = clamp01(
    splitFit * 0.26 +
      roughnessFit * 0.2 +
      coherenceFit * 0.18 +
      angularDiscipline * 0.16 +
      routeContinuity * 0.12 +
      (1 - falseOrderRisk) * 0.08
  );

  return {
    case: testCase.name,
    interfaceType: testCase.interfaceType,
    variant: variant.name,
    kind: variant.kind,
    score: Number(score.toFixed(4)),
    roughnessRatio: testCase.roughnessRatio,
    splitFit: Number(splitFit.toFixed(3)),
    roughnessFit: Number(roughnessFit.toFixed(3)),
    coherenceFit: Number(coherenceFit.toFixed(3)),
    angularDiscipline: Number(angularDiscipline.toFixed(3)),
    routeContinuity: Number(routeContinuity.toFixed(3)),
    falseOrderRisk: Number(falseOrderRisk.toFixed(3)),
    specularOrder: Number(variant.specularOrder.toFixed(3)),
    diffuseOrder: Number(variant.diffuseOrder.toFixed(3)),
    phaseMemory: Number(variant.phaseMemory.toFixed(3)),
  };
}

const rows = cases.flatMap((testCase) => variants.map((variant) => scoreVariant(testCase, variant)));
const summaries = cases.map((testCase) => {
  const caseRows = rows.filter((row) => row.case === testCase.name);
  const best = caseRows.reduce((current, row) => (row.score > current.score ? row : current), caseRows[0]);
  const decoys = caseRows.filter((row) => row.kind === 'decoy');
  const bestDecoy = decoys.reduce((current, row) => (row.score > current.score ? row : current), decoys[0]);

  return {
    case: testCase.name,
    interfaceType: testCase.interfaceType,
    roughnessRatio: testCase.roughnessRatio,
    expectedSpecular: testCase.expectedSpecular,
    expectedDiffuse: testCase.expectedDiffuse,
    predictedBest: best.variant,
    predictedBestScore: best.score,
    bestDecoy: bestDecoy.variant,
    bestDecoyScore: bestDecoy.score,
    decoyPenalty: Number((best.score - bestDecoy.score).toFixed(4)),
    predictionClearsDecoys: best.score > bestDecoy.score,
  };
});

const weak = summaries.filter((summary) => summary.decoyPenalty < 0.1 || !summary.predictionClearsDecoys);
const diagnosis = weak.length
  ? `weak roughness scatter separation for ${weak.map((item) => item.case).join(', ')}`
  : 'roughness scatter controls separate smooth specular, mixed, and diffuse rough-interface regimes';

const json = {
  source: 'roughness-scatter-sweep.mjs',
  status: 'held-out roughness/interface scatter diagnostic; not an optics simulator',
  diagnosis,
  summaries,
  rows,
};

await mkdir(outDir, { recursive: true });
await writeFile(new URL('roughness-scatter-sweep.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate Roughness Scatter Sweep

## Scope

This diagnostic tests a held-out interface surface: roughness-controlled specular versus diffuse scatter.

It does not simulate Maxwell optics, BRDFs, or measured scatter curves. It checks whether route order follows roughness-relative-to-wavelength expectations before attempting calibrated optics.

## Summary

Diagnosis: ${diagnosis}.

| Case | Interface type | Roughness ratio | Expected specular | Expected diffuse | Predicted best | Best score | Best decoy | Best decoy score | Decoy penalty |
|---|---|---:|---:|---:|---|---:|---|---:|---:|
${summaries
  .map(
    (summary) =>
      `| ${summary.case} | ${summary.interfaceType} | ${summary.roughnessRatio} | ${summary.expectedSpecular} | ${summary.expectedDiffuse} | ${summary.predictedBest} | ${summary.predictedBestScore} | ${summary.bestDecoy} | ${summary.bestDecoyScore} | ${summary.decoyPenalty} |`
  )
  .join('\n')}

## Variant Rows

| Case | Variant | Kind | Score | Split fit | Roughness fit | Coherence fit | Angular discipline | Route continuity | False-order risk | Specular order | Diffuse order | Phase memory |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
${rows
  .map(
    (row) =>
      `| ${row.case} | ${row.variant} | ${row.kind} | ${row.score} | ${row.splitFit} | ${row.roughnessFit} | ${row.coherenceFit} | ${row.angularDiscipline} | ${row.routeContinuity} | ${row.falseOrderRisk} | ${row.specularOrder} | ${row.diffuseOrder} | ${row.phaseMemory} |`
  )
  .join('\n')}

## Reading

The useful question is whether boundary route order changes with roughness regime: smooth boundaries should preserve coherent specular order; high roughness should favour diffuse scatter; false specular rows with broken phase memory should not win.
`;

await writeFile(new URL('roughness-scatter-sweep.md', outDir), markdown);

console.log(`Cases tested: ${cases.length}`);
console.log(`Diagnosis: ${diagnosis}`);
console.log(`Wrote ${new URL('roughness-scatter-sweep.md', outDir).pathname}`);
