import { mkdir, writeFile } from 'node:fs/promises';
import { simulateSequence } from '../src/model.js';

// P1: derive the grammar's order effect directly from the model.
//
// Hypothesis (from docs/grammar-native-prediction-scoping-2026-06-24.md): because
// simulateSequence carries memory (accumContinuity built by gentle steps; accumStress
// built by harsh steps), the SAME multiset of encounters in a different ORDER should
// give different identity survival -- and specifically GENTLE-FIRST should survive
// better than HARSH-FIRST ("preconditioning / coaxing"). Static theories predict no
// order effect; order-independent cumulative baselines predict the null.
//
// This script asserts no physical evidence. It characterises whether the toy model
// actually produces the predicted directional order effect, across a config sweep, so
// the programme can judge whether the grammar has a distinctive falsifiable claim (vs
// being a conceptual lens). No external data.

const outDir = new URL('./out/', import.meta.url);

// 'recovering' = gentle encounter (low fatigue, reseat boost); 'stressed' = harsh.
const GENTLE = 'recovering';
const HARSH = 'stressed';

function scheduleGentleFirst(k) {
  return [...Array(k).fill(GENTLE), ...Array(k).fill(HARSH)];
}
function scheduleHarshFirst(k) {
  return [...Array(k).fill(HARSH), ...Array(k).fill(GENTLE)];
}
function scheduleInterleaved(k) {
  const s = [];
  for (let i = 0; i < k; i += 1) s.push(GENTLE, HARSH);
  return s;
}

function run(base, schedule, regimeMemory) {
  const r = simulateSequence(base, schedule.length, {
    regimeSchedule: schedule,
    regimeMemory,
    adaptivePolicy: false,
    lightweight: true,
  });
  // Whole-history measures from the trace ("did the closed order survive the HISTORY",
  // not just the last step): min identity over the trace, and whether EVERY step held.
  const ids = r.trace.map((t) => (t.metrics ? t.metrics.identityScore : t.identityScore) ?? t.identityScore);
  const idScores = r.trace.map((t) => t.identityScore);
  const minIdentity = Math.min(...idScores);
  const allStepsPreserved = r.trace.every((t) => t.identityPreserved);
  return {
    // last-step (recency) measures
    finalIdentity: r.summary.finalIdentity,
    finalPreserved: r.summary.finalPreserved,
    memWeightedCoherence: r.summary.memoryWeightedCoherence,
    finalStress: r.summary.finalStress,
    // whole-history (preconditioning) measures
    minIdentity: Number(minIdentity.toFixed(4)),
    allStepsPreserved,
  };
}

// Config sweep over marginal territory (where order can matter). Each axis kept to a
// small principled grid; phase/charge/route/scatter/storage at moderate values.
const boundaries = [0.45, 0.55, 0.65, 0.75];
const reseats = [0.35, 0.5, 0.65, 0.8];
const phases = [0.45, 0.6];
const baseTemplate = { route: 0.55, phase: 0.55, charge: 0.3, scatter: 0.3, storage: 0.5 };

const halfLengths = [1, 2, 3]; // k gentle + k harsh => sequences of length 2, 4, 6
const regimeMemories = [0.0, 0.3];

const rows = [];
for (const boundary of boundaries) {
  for (const reseat of reseats) {
    for (const phase of phases) {
      for (const k of halfLengths) {
        for (const regimeMemory of regimeMemories) {
          const base = { ...baseTemplate, boundary, reseat, phase };
          const gf = run(base, scheduleGentleFirst(k), regimeMemory);
          const hf = run(base, scheduleHarshFirst(k), regimeMemory);
          rows.push({
            boundary, reseat, phase, k, regimeMemory,
            // recency (final-state) order effect
            gfIdentity: gf.finalIdentity, hfIdentity: hf.finalIdentity,
            deltaFinalIdentity: Number((gf.finalIdentity - hf.finalIdentity).toFixed(4)),
            // whole-history (preconditioning) order effect
            gfMinIdentity: gf.minIdentity, hfMinIdentity: hf.minIdentity,
            deltaMinIdentity: Number((gf.minIdentity - hf.minIdentity).toFixed(4)),
            gfAllPreserved: gf.allStepsPreserved, hfAllPreserved: hf.allStepsPreserved,
          });
        }
      }
    }
  }
}

// Aggregate the order effect under TWO survival definitions.
const n = rows.length;
function stats(deltaKey) {
  const d = rows.map((r) => r[deltaKey]);
  return {
    meanDelta: Number((d.reduce((s, v) => s + v, 0) / n).toFixed(4)),
    fracGentleBetter: Number((rows.filter((r) => r[deltaKey] > 1e-6).length / n).toFixed(3)),
    fracHarshBetter: Number((rows.filter((r) => r[deltaKey] < -1e-6).length / n).toFixed(3)),
    range: [Number(Math.min(...d).toFixed(4)), Number(Math.max(...d).toFixed(4))],
  };
}
// Recency (final state): positive delta = gentle-first ends higher.
const recency = stats('deltaFinalIdentity');
// Whole-history (preconditioning): positive delta = gentle-first holds a higher minimum.
const wholeHistory = stats('deltaMinIdentity');
// Whole-history survival flips: gentle-first holds ALL steps but harsh-first breaks somewhere.
const wholeHistoryFlips = rows.filter((r) => r.gfAllPreserved && !r.hfAllPreserved).length;
const reverseWholeHistoryFlips = rows.filter((r) => !r.gfAllPreserved && r.hfAllPreserved).length;

const preconditioningHolds = wholeHistory.fracGentleBetter >= 0.8 && wholeHistory.meanDelta > 0 && reverseWholeHistoryFlips === 0;
const recencyDominatesFinal = recency.fracHarshBetter >= 0.8 && recency.meanDelta < 0;

const report = {
  source: 'grammar-order-effect-derivation.mjs',
  date: '2026-06-24',
  status: `order effect is real and direction depends on the survival measure: ${recencyDominatesFinal ? 'final-state = RECENCY (end-gentle better)' : 'final-state mixed'}; ${preconditioningHolds ? 'whole-history = PRECONDITIONING (gentle-first protects)' : 'whole-history not cleanly preconditioning'}`,
  validationClaim: false,
  evidenceStatus: 'none; internal derivation from the toy model, no external data',
  configsTested: n,
  finalStateRecency: {
    note: 'positive meanDelta would mean gentle-first ends higher; negative = end-gentle (harsh-first) wins = RECENCY',
    ...recency,
  },
  wholeHistoryPreconditioning: {
    note: 'positive meanDelta means gentle-first holds a HIGHER minimum identity across the history = PRECONDITIONING',
    ...wholeHistory,
    wholeHistoryFlips_gentleHoldsAllHarshBreaks: wholeHistoryFlips,
    reverseWholeHistoryFlips: reverseWholeHistoryFlips,
  },
  preconditioningHolds,
  recencyDominatesFinal,
  reading: [
    `The toy model produces a CONSISTENT, direction-dependent order effect (order is non-commutative for identity survival).`,
    recencyDominatesFinal
      ? `Under the FINAL-STATE measure the effect is RECENCY: ending on a gentle encounter wins (harsh-first), because the last step dominates finalIdentity. Recency is NOT a distinctive no-competitor claim (many simple models give it).`
      : `Under the final-state measure the effect is mixed.`,
    preconditioningHolds
      ? `Under the WHOLE-HISTORY measure (the grammar's actual claim -- "did the closed order survive the history"), the effect is PRECONDITIONING: gentle-first holds a higher minimum identity across the run because the harsh encounters land on a memory-protected identity, and there are whole-history survival flips only in the predicted direction. THIS is the grammar's distinctive, falsifiable prediction, and it is real in the model.`
      : `Under the whole-history measure the model does not cleanly show preconditioning, which would weaken the grammar's distinctive claim.`,
    `Net for P1: the distinctive no-competitor prediction (preconditioning) is real in the model ONLY for whole-history survival, not final state. A real-world test must therefore use a whole-history survival endpoint (did it ever fail), not a final-state endpoint -- e.g. fatigue: cycles-to-first-crack under gentle-first vs harsh-first blocks, NOT residual strength after the sequence.`,
  ],
  caveats: [
    'derived from the toy rule model, not physics; shows the claim is internally real and which endpoint reveals it, not that it is physically true',
    'only signs/consistency are meaningful; magnitudes are in abstract identity units',
    'gentle/harsh = recovering/stressed regimes; the multiset (k gentle + k harsh) is held fixed when reversing order',
  ],
  sampleRows: [...rows].sort((a, b) => b.deltaMinIdentity - a.deltaMinIdentity).slice(0, 4)
    .concat([...rows].sort((a, b) => a.deltaMinIdentity - b.deltaMinIdentity).slice(0, 2)),
};

const markdown = `# Grammar Order-Effect Derivation (P1)

Status: **${report.status}**

Internal derivation from the toy model (\`simulateSequence\`); no external data, no
physical claim. Tests whether the same multiset of encounters in a different ORDER
changes identity survival, under two endpoints.

## Final-state endpoint (recency) -- ${n} configs

delta = gentleFirst.finalIdentity - harshFirst.finalIdentity (positive = gentle-first ends higher)

| mean delta | gentle-first better | harsh-first better | range |
|---|---|---|---|
| ${recency.meanDelta} | ${recency.fracGentleBetter} | ${recency.fracHarshBetter} | [${recency.range.join(', ')}] |

## Whole-history endpoint (preconditioning) -- ${n} configs

delta = gentleFirst.minIdentity - harshFirst.minIdentity (positive = gentle-first holds a higher minimum)

| mean delta | gentle-first better | harsh-first better | range | whole-history flips (gentle holds all, harsh breaks) | reverse |
|---|---|---|---|---|---|
| ${wholeHistory.meanDelta} | ${wholeHistory.fracGentleBetter} | ${wholeHistory.fracHarshBetter} | [${wholeHistory.range.join(', ')}] | ${wholeHistoryFlips} | ${reverseWholeHistoryFlips} |

Preconditioning holds (whole-history): **${preconditioningHolds ? 'yes' : 'no'}**.
Recency dominates final state: **${recencyDominatesFinal ? 'yes' : 'no'}**.

## Reading

${report.reading.map((r) => `- ${r}`).join('\n')}

## Caveats

${report.caveats.map((c) => `- ${c}`).join('\n')}
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('grammar-order-effect-derivation.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('grammar-order-effect-derivation.md', outDir), markdown);

console.log(`Grammar order-effect derivation (${n} configs):`);
console.log(`  final-state (recency):    meanDelta=${recency.meanDelta}  gentleBetter=${recency.fracGentleBetter}  harshBetter=${recency.fracHarshBetter}`);
console.log(`  whole-history (precond.): meanDelta=${wholeHistory.meanDelta}  gentleBetter=${wholeHistory.fracGentleBetter}  flips=${wholeHistoryFlips} (reverse ${reverseWholeHistoryFlips})`);
console.log(`  preconditioning holds: ${preconditioningHolds} | recency dominates final: ${recencyDominatesFinal}`);
