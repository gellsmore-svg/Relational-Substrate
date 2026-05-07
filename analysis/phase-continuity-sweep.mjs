import { mkdir, writeFile } from 'node:fs/promises';
import { clamp01 } from './molecule-model.mjs';

const outDir = new URL('./out/', import.meta.url);

const cases = [
  {
    name: 'refractive phase carry-through',
    interfaceType: 'air-glass phase proxy',
    routeBase: 0.7,
    phaseDemand: 0.82,
  },
  {
    name: 'release phase preservation',
    interfaceType: 'glass-air release proxy',
    routeBase: 0.68,
    phaseDemand: 0.78,
  },
  {
    name: 'crystal gate phase lock',
    interfaceType: 'glass-crystal gate proxy',
    routeBase: 0.66,
    phaseDemand: 0.9,
  },
];

const variants = [
  {
    name: 'phase-continuous transmission',
    kind: 'reference',
    phaseContinuity: 0.9,
    phaseMemory: 0.88,
    angleCoherence: 0.84,
    gateTiming: 0.82,
    routeSplitFit: 0.86,
    amplitudeOrder: 0.84,
    phaseJitter: 0.08,
    destructiveInterference: 0.1,
    delayedPhaseLock: 0.12,
  },
  {
    name: 'phase-lagged but coherent transmission',
    kind: 'strained',
    phaseContinuity: 0.72,
    phaseMemory: 0.7,
    angleCoherence: 0.78,
    gateTiming: 0.64,
    routeSplitFit: 0.82,
    amplitudeOrder: 0.78,
    phaseJitter: 0.24,
    destructiveInterference: 0.18,
    delayedPhaseLock: 0.34,
  },
  {
    name: 'noisy but recoverable phase lock',
    kind: 'strained',
    phaseContinuity: 0.66,
    phaseMemory: 0.68,
    angleCoherence: 0.62,
    gateTiming: 0.72,
    routeSplitFit: 0.74,
    amplitudeOrder: 0.74,
    phaseJitter: 0.34,
    destructiveInterference: 0.22,
    delayedPhaseLock: 0.24,
  },
  {
    name: 'phase-broken high transmission',
    kind: 'decoy',
    phaseContinuity: 0.2,
    phaseMemory: 0.22,
    angleCoherence: 0.66,
    gateTiming: 0.72,
    routeSplitFit: 0.86,
    amplitudeOrder: 0.78,
    phaseJitter: 0.72,
    destructiveInterference: 0.52,
    delayedPhaseLock: 0.28,
  },
  {
    name: 'amplitude-only passage',
    kind: 'decoy',
    phaseContinuity: 0.32,
    phaseMemory: 0.28,
    angleCoherence: 0.74,
    gateTiming: 0.68,
    routeSplitFit: 0.8,
    amplitudeOrder: 0.9,
    phaseJitter: 0.62,
    destructiveInterference: 0.42,
    delayedPhaseLock: 0.34,
  },
  {
    name: 'delayed phase capture',
    kind: 'decoy',
    phaseContinuity: 0.5,
    phaseMemory: 0.44,
    angleCoherence: 0.7,
    gateTiming: 0.38,
    routeSplitFit: 0.76,
    amplitudeOrder: 0.74,
    phaseJitter: 0.4,
    destructiveInterference: 0.34,
    delayedPhaseLock: 0.78,
  },
  {
    name: 'interference-fragmented output',
    kind: 'decoy',
    phaseContinuity: 0.46,
    phaseMemory: 0.38,
    angleCoherence: 0.5,
    gateTiming: 0.58,
    routeSplitFit: 0.66,
    amplitudeOrder: 0.52,
    phaseJitter: 0.58,
    destructiveInterference: 0.82,
    delayedPhaseLock: 0.42,
  },
];

function scoreVariant(testCase, variant) {
  const phaseDemandFit = clamp01(1 - Math.abs(variant.phaseContinuity - testCase.phaseDemand) / 0.82);
  const phaseOrder = clamp01(
    variant.phaseContinuity * 0.34 +
      variant.phaseMemory * 0.26 +
      (1 - variant.phaseJitter) * 0.2 +
      (1 - variant.destructiveInterference) * 0.2
  );
  const gatePhaseCoupling = clamp01(
    variant.gateTiming * 0.32 +
      phaseOrder * 0.3 +
      variant.angleCoherence * 0.2 +
      (1 - variant.delayedPhaseLock) * 0.18
  );
  const transmissionIntegrity = clamp01(
    phaseOrder * 0.36 +
      variant.routeSplitFit * 0.24 +
      variant.amplitudeOrder * 0.18 +
      gatePhaseCoupling * 0.14 +
      phaseDemandFit * 0.08
  );
  const routeContinuity = clamp01(
    testCase.routeBase +
      transmissionIntegrity * 0.13 +
      gatePhaseCoupling * 0.1 -
      variant.phaseJitter * 0.13 -
      variant.destructiveInterference * 0.11
  );
  const phaseFailureRisk = clamp01(
    (1 - phaseOrder) * 0.32 +
      (1 - gatePhaseCoupling) * 0.2 +
      variant.phaseJitter * 0.18 +
      variant.destructiveInterference * 0.18 +
      variant.delayedPhaseLock * 0.12
  );
  const score = clamp01(
    phaseOrder * 0.28 +
      transmissionIntegrity * 0.24 +
      gatePhaseCoupling * 0.18 +
      routeContinuity * 0.14 +
      (1 - phaseFailureRisk) * 0.1 +
      phaseDemandFit * 0.06
  );

  return {
    case: testCase.name,
    interfaceType: testCase.interfaceType,
    variant: variant.name,
    kind: variant.kind,
    score: Number(score.toFixed(4)),
    phaseOrder: Number(phaseOrder.toFixed(3)),
    gatePhaseCoupling: Number(gatePhaseCoupling.toFixed(3)),
    transmissionIntegrity: Number(transmissionIntegrity.toFixed(3)),
    routeContinuity: Number(routeContinuity.toFixed(3)),
    phaseFailureRisk: Number(phaseFailureRisk.toFixed(3)),
    phaseDemandFit: Number(phaseDemandFit.toFixed(3)),
    phaseJitter: Number(variant.phaseJitter.toFixed(3)),
    destructiveInterference: Number(variant.destructiveInterference.toFixed(3)),
    delayedPhaseLock: Number(variant.delayedPhaseLock.toFixed(3)),
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
  ? `weak phase-continuity separation for ${weak.map((item) => item.case).join(', ')}`
  : 'phase-continuity controls separate coherent transmission from amplitude-only, delayed-lock, and interference-fragmented decoys';

const json = {
  source: 'phase-continuity-sweep.mjs',
  status: 'focused phase-continuity diagnostic; not part of boundary calibration',
  diagnosis,
  summaries,
  rows,
};

await mkdir(outDir, { recursive: true });
await writeFile(new URL('phase-continuity-sweep.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate Phase Continuity Sweep

## Scope

This diagnostic isolates the tightest boundary-transition decoy: high apparent transmission with broken phase continuity.

It does not simulate optics or wave equations. It tests whether phase order, phase memory, gate timing, and interference discipline reject outputs that preserve amplitude or route split while losing phase continuity.

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

| Case | Variant | Kind | Score | Phase order | Gate-phase coupling | Transmission integrity | Route continuity | Phase failure risk | Phase-demand fit | Phase jitter | Destructive interference | Delayed phase lock |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
${rows
  .map(
    (row) =>
      `| ${row.case} | ${row.variant} | ${row.kind} | ${row.score} | ${row.phaseOrder} | ${row.gatePhaseCoupling} | ${row.transmissionIntegrity} | ${row.routeContinuity} | ${row.phaseFailureRisk} | ${row.phaseDemandFit} | ${row.phaseJitter} | ${row.destructiveInterference} | ${row.delayedPhaseLock} |`
  )
  .join('\n')}

## Reading

This is a topology/control diagnostic. The useful question is whether route continuity must carry phase memory, not merely transmitted amplitude.
`;

await writeFile(new URL('phase-continuity-sweep.md', outDir), markdown);

console.log(`Cases tested: ${cases.length}`);
console.log(`Diagnosis: ${diagnosis}`);
console.log(`Wrote ${new URL('phase-continuity-sweep.md', outDir).pathname}`);
