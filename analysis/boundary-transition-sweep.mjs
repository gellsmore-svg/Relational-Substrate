import { mkdir, writeFile } from 'node:fs/promises';
import { clamp01 } from './molecule-model.mjs';

const outDir = new URL('./out/', import.meta.url);

const cases = [
  {
    name: 'air-to-glass ordered entry',
    interfaceType: 'refractive boundary proxy',
    routeBase: 0.7,
    preferredReturn: 0.18,
    preferredTransmission: 0.76,
  },
  {
    name: 'glass-to-air ordered release',
    interfaceType: 'release boundary proxy',
    routeBase: 0.68,
    preferredReturn: 0.12,
    preferredTransmission: 0.82,
  },
  {
    name: 'glass-to-crystal late gate',
    interfaceType: 'phase-order boundary proxy',
    routeBase: 0.66,
    preferredReturn: 0.34,
    preferredTransmission: 0.54,
  },
];

const variants = [
  {
    name: 'ordered boundary transition',
    kind: 'reference',
    boundaryCompatibility: 0.9,
    angleCoherence: 0.86,
    phaseContinuity: 0.88,
    gateTiming: 0.84,
    returnOrdering: 0.82,
    transmissionOrdering: 0.88,
    trappedRelease: 0.08,
    diffuseScatter: 0.1,
    lateGateDelay: 0.12,
  },
  {
    name: 'rough but transmitting boundary',
    kind: 'strained',
    boundaryCompatibility: 0.68,
    angleCoherence: 0.58,
    phaseContinuity: 0.7,
    gateTiming: 0.72,
    returnOrdering: 0.62,
    transmissionOrdering: 0.72,
    trappedRelease: 0.18,
    diffuseScatter: 0.28,
    lateGateDelay: 0.2,
  },
  {
    name: 'late-gated ordered release',
    kind: 'strained',
    boundaryCompatibility: 0.74,
    angleCoherence: 0.72,
    phaseContinuity: 0.78,
    gateTiming: 0.48,
    returnOrdering: 0.72,
    transmissionOrdering: 0.64,
    trappedRelease: 0.28,
    diffuseScatter: 0.16,
    lateGateDelay: 0.48,
  },
  {
    name: 'diffuse scatter dominated boundary',
    kind: 'decoy',
    boundaryCompatibility: 0.42,
    angleCoherence: 0.24,
    phaseContinuity: 0.38,
    gateTiming: 0.58,
    returnOrdering: 0.38,
    transmissionOrdering: 0.34,
    trappedRelease: 0.22,
    diffuseScatter: 0.78,
    lateGateDelay: 0.26,
  },
  {
    name: 'trapped release loop',
    kind: 'decoy',
    boundaryCompatibility: 0.58,
    angleCoherence: 0.54,
    phaseContinuity: 0.44,
    gateTiming: 0.3,
    returnOrdering: 0.68,
    transmissionOrdering: 0.24,
    trappedRelease: 0.82,
    diffuseScatter: 0.24,
    lateGateDelay: 0.62,
  },
  {
    name: 'wrong-way return dominance',
    kind: 'decoy',
    boundaryCompatibility: 0.64,
    angleCoherence: 0.66,
    phaseContinuity: 0.6,
    gateTiming: 0.58,
    returnOrdering: 0.92,
    transmissionOrdering: 0.28,
    trappedRelease: 0.34,
    diffuseScatter: 0.22,
    lateGateDelay: 0.32,
  },
  {
    name: 'phase-broken transmission',
    kind: 'decoy',
    boundaryCompatibility: 0.7,
    angleCoherence: 0.62,
    phaseContinuity: 0.18,
    gateTiming: 0.68,
    returnOrdering: 0.42,
    transmissionOrdering: 0.66,
    trappedRelease: 0.2,
    diffuseScatter: 0.34,
    lateGateDelay: 0.18,
  },
];

function scoreVariant(testCase, variant) {
  const returnError = Math.abs(variant.returnOrdering - testCase.preferredReturn);
  const transmissionError = Math.abs(variant.transmissionOrdering - testCase.preferredTransmission);
  const splitCoherence = clamp01(1 - (returnError * 0.45 + transmissionError * 0.55));
  const boundaryOrder = clamp01(
    variant.boundaryCompatibility * 0.3 +
      variant.angleCoherence * 0.22 +
      variant.phaseContinuity * 0.26 +
      variant.gateTiming * 0.22
  );
  const routeSplitOrder = clamp01(
    splitCoherence * 0.44 +
      variant.transmissionOrdering * 0.22 +
      (1 - variant.trappedRelease) * 0.18 +
      (1 - variant.diffuseScatter) * 0.16
  );
  const releaseDiscipline = clamp01(
    variant.gateTiming * 0.3 +
      (1 - variant.trappedRelease) * 0.32 +
      (1 - variant.lateGateDelay) * 0.22 +
      variant.phaseContinuity * 0.16
  );
  const routeContinuity = clamp01(
    testCase.routeBase +
      boundaryOrder * 0.12 +
      routeSplitOrder * 0.1 -
      variant.diffuseScatter * 0.14 -
      variant.trappedRelease * 0.1
  );
  const failureRisk = clamp01(
    (1 - boundaryOrder) * 0.24 +
      (1 - routeSplitOrder) * 0.24 +
      variant.diffuseScatter * 0.22 +
      variant.trappedRelease * 0.18 +
      variant.lateGateDelay * 0.12
  );
  const score = clamp01(
    boundaryOrder * 0.25 +
      routeSplitOrder * 0.22 +
      releaseDiscipline * 0.2 +
      routeContinuity * 0.15 +
      (1 - failureRisk) * 0.12 +
      splitCoherence * 0.06
  );

  return {
    case: testCase.name,
    interfaceType: testCase.interfaceType,
    variant: variant.name,
    kind: variant.kind,
    score: Number(score.toFixed(4)),
    boundaryOrder: Number(boundaryOrder.toFixed(3)),
    routeSplitOrder: Number(routeSplitOrder.toFixed(3)),
    releaseDiscipline: Number(releaseDiscipline.toFixed(3)),
    routeContinuity: Number(routeContinuity.toFixed(3)),
    failureRisk: Number(failureRisk.toFixed(3)),
    splitCoherence: Number(splitCoherence.toFixed(3)),
    trappedRelease: Number(variant.trappedRelease.toFixed(3)),
    diffuseScatter: Number(variant.diffuseScatter.toFixed(3)),
    lateGateDelay: Number(variant.lateGateDelay.toFixed(3)),
  };
}

const rows = cases.flatMap((testCase) => variants.map((variant) => scoreVariant(testCase, variant)));
const summaries = cases.map((testCase) => {
  const caseRows = rows.filter((row) => row.case === testCase.name);
  const reference = caseRows.find((row) => row.kind === 'reference');
  const decoys = caseRows.filter((row) => row.kind === 'decoy');
  const strained = caseRows.filter((row) => row.kind === 'strained');
  const bestDecoy = decoys.reduce((best, row) => (row.score > best.score ? row : best), decoys[0]);
  const bestStrained = strained.reduce((best, row) => (row.score > best.score ? row : best), strained[0]);

  return {
    case: testCase.name,
    interfaceType: testCase.interfaceType,
    referenceScore: reference.score,
    bestStrained: bestStrained.variant,
    bestStrainedScore: bestStrained.score,
    bestDecoy: bestDecoy.variant,
    bestDecoyScore: bestDecoy.score,
    decoyPenalty: Number((reference.score - bestDecoy.score).toFixed(4)),
    referenceBeatsDecoys: decoys.every((row) => reference.score > row.score),
  };
});

const weak = summaries.filter((summary) => summary.decoyPenalty < 0.1 || !summary.referenceBeatsDecoys);
const diagnosis = weak.length
  ? `weak boundary transition separation for ${weak.map((item) => item.case).join(', ')}`
  : 'boundary transition controls separate ordered route splitting from diffuse scatter, trapped release, and phase-broken decoys';

const json = {
  source: 'boundary-transition-sweep.mjs',
  status: 'focused boundary/interface route diagnostic; not part of molecule or material calibration',
  diagnosis,
  summaries,
  rows,
};

await mkdir(outDir, { recursive: true });
await writeFile(new URL('boundary-transition-sweep.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# AMS Boundary Transition Sweep

## Scope

This diagnostic tests interface route behaviour: ordered transition, return, release, and scattering across simple boundary proxies.

It does not simulate optics, Fresnel physics, crystallography, or surface roughness. It tests whether route grammar can distinguish ordered boundary transitions from diffuse scatter, trapped release loops, wrong-way return dominance, and phase-broken transmission.

## Summary

Diagnosis: ${diagnosis}.

| Case | Interface type | Reference score | Best strained | Best strained score | Best decoy | Best decoy score | Decoy penalty | Reference beats decoys |
|---|---|---:|---|---:|---|---:|---:|---|
${summaries
  .map(
    (summary) =>
      `| ${summary.case} | ${summary.interfaceType} | ${summary.referenceScore} | ${summary.bestStrained} | ${summary.bestStrainedScore} | ${summary.bestDecoy} | ${summary.bestDecoyScore} | ${summary.decoyPenalty} | ${summary.referenceBeatsDecoys ? 'yes' : 'no'} |`
  )
  .join('\n')}

## Variant Rows

| Case | Variant | Kind | Score | Boundary order | Route split order | Release discipline | Route continuity | Failure risk | Split coherence | Trapped release | Diffuse scatter | Late gate delay |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
${rows
  .map(
    (row) =>
      `| ${row.case} | ${row.variant} | ${row.kind} | ${row.score} | ${row.boundaryOrder} | ${row.routeSplitOrder} | ${row.releaseDiscipline} | ${row.routeContinuity} | ${row.failureRisk} | ${row.splitCoherence} | ${row.trappedRelease} | ${row.diffuseScatter} | ${row.lateGateDelay} |`
  )
  .join('\n')}

## Reading

This is a topology/control diagnostic. The useful question is whether boundary outcomes can be modelled as route splitting plus release discipline before adding physically calibrated optical or interface equations.
`;

await writeFile(new URL('boundary-transition-sweep.md', outDir), markdown);

console.log(`Cases tested: ${cases.length}`);
console.log(`Diagnosis: ${diagnosis}`);
console.log(`Wrote ${new URL('boundary-transition-sweep.md', outDir).pathname}`);
