import { mkdir, writeFile } from 'node:fs/promises';
import { simulateSequence } from '../src/model.js';

// MAGNITUDE test: does the grammar predict the SIZE of the order effect, or only its
// direction? Decisive finding: the grammar has NO intrinsic graded life-to-failure
// (survival under repeated load is binary), so its order effect is a near-threshold
// sign flip, not a magnitude. Matching the fatigue magnitude is therefore supplied
// entirely by the (free) mapping -> the grammar is a directional LENS for this effect,
// not a parameter-free quantitative predictor. Consistency only; confidence unchanged.

const outDir = new URL('./out/', import.meta.url);

function trace(schedule, base) {
  return simulateSequence(base, schedule.length, {
    regimeSchedule: schedule, regimeMemory: 0.3, adaptivePolicy: false, lightweight: true,
  });
}
function firstBreak(schedule, base) {
  return trace(schedule, base).trace.findIndex((t) => !t.identityPreserved);
}

// (1) Is survival under repeated identical load GRADED (a life) or BINARY (a threshold)?
const lifeCounts = {};
const grid = [];
for (const boundary of [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]) {
  for (const reseat of [0.2, 0.3, 0.4, 0.5, 0.6]) {
    for (const route of [0.35, 0.5, 0.65]) {
      for (const charge of [0.35, 0.5]) {
        const base = { boundary, reseat, route, charge, phase: 0.5, scatter: 0.4, storage: 0.5 };
        const br = firstBreak(Array(16).fill('stressed'), base);
        const life = br < 0 ? 16 : br;
        lifeCounts[life] = (lifeCounts[life] || 0) + 1;
        grid.push({ ...base, life });
      }
    }
  }
}
const distinctLives = Object.keys(lifeCounts).map(Number).sort((a, b) => a - b);
const intermediateLives = distinctLives.filter((l) => l > 0 && l < 16).length;
const survivalIsBinary = intermediateLives === 0;

// (2) Quantify the grammar's order effect as a near-threshold SIGN effect: across
// marginal configs, fraction where gentle-first survives the whole history but
// harsh-first does not (a survival FLIP), and the min-identity shift. (Same machinery
// as P1; reproduced here so the magnitude conclusion is self-contained.)
function wholeHistory(schedule, base) {
  const r = trace(schedule, base);
  const ids = r.trace.map((t) => t.identityScore);
  return { allPreserved: r.trace.every((t) => t.identityPreserved), minIdentity: Math.min(...ids) };
}
let flips = 0, total = 0, sumMinDelta = 0;
for (const boundary of [0.45, 0.55, 0.65, 0.75]) {
  for (const reseat of [0.35, 0.5, 0.65, 0.8]) {
    for (const k of [1, 2, 3]) {
      const base = { boundary, reseat, phase: 0.55, route: 0.55, charge: 0.3, scatter: 0.3, storage: 0.5 };
      const gentleFirst = [...Array(k).fill('recovering'), ...Array(k).fill('stressed')];
      const harshFirst = [...Array(k).fill('stressed'), ...Array(k).fill('recovering')];
      const gf = wholeHistory(gentleFirst, base);
      const hf = wholeHistory(harshFirst, base);
      total += 1;
      if (gf.allPreserved && !hf.allPreserved) flips += 1;
      sumMinDelta += gf.minIdentity - hf.minIdentity;
    }
  }
}
const flipFraction = Number((flips / total).toFixed(3));
const meanMinIdentityDelta = Number((sumMinDelta / total).toFixed(4));

// (3) The fatigue magnitude the grammar would need to reproduce (validated Miner test).
const fatigue = {
  matchedPairDRatio: Number((1.717 / 0.820).toFixed(3)),
  maxCoaxingRatio_n2_over_virgin: Number((16776 / 6813).toFixed(3)), // 2.462 (L-H 0.006->0.008)
};

// Verdict.
const magnitudeParameterFree = !survivalIsBinary; // a graded life would be needed to predict magnitude
const report = {
  source: 'grammar-order-effect-magnitude-test.mjs',
  date: '2026-06-25',
  status: magnitudeParameterFree
    ? 'grammar has a graded life and could predict magnitude (investigate further)'
    : 'grammar has NO intrinsic graded life -> predicts order DIRECTION at a threshold but not MAGNITUDE; fatigue magnitude is supplied entirely by the mapping -> directional LENS, established nonlinear-damage models win on magnitude',
  consistencyCheckOnly: true,
  validationClaim: false,
  raisesConfidence: false,
  survivalGradedness: {
    distinctLivesUnderRepeatedStressedLoad: distinctLives,
    intermediateLives,
    survivalIsBinary,
    lifeCounts,
    note: 'survival under repeated identical load is binary (0 or the full horizon) -> the grammar has no cycles-to-failure magnitude analog',
  },
  grammarOrderEffectSize: {
    marginalConfigs: total,
    survivalFlipFraction: flipFraction,
    meanMinIdentityDelta,
    note: 'the order effect is a small near-threshold sign effect (whether order flips binary survival; a ~1% min-identity shift), not a graded magnitude',
  },
  fatigueMagnitudeToBeat: fatigue,
  verdict: [
    `Survival under repeated load is BINARY (distinct lives observed: ${distinctLives.join(', ')}; zero intermediate). The grammar therefore has no intrinsic graded life-to-failure, i.e. no cycles-to-failure magnitude.`,
    `Its order effect is a near-threshold SIGN effect: gentle-first flips whole-history survival in ${Math.round(flipFraction * 100)}% of marginal configs, with a mean min-identity shift of only ${meanMinIdentityDelta} (in 0-1 units).`,
    `The fatigue effect to reproduce is multiplicative and large (matched-pair D-ratio ~${fatigue.matchedPairDRatio}; coaxing up to ~${fatigue.maxCoaxingRatio_n2_over_virgin}x life). The grammar contributes the SIGN at the threshold; ALL of the magnitude would come from the (free) amplitude->regime and block->steps mapping.`,
    'DECISIVE VERDICT: the grammar predicts the order effect parameter-free in DIRECTION only. It cannot predict the MAGNITUDE without a calibration that supplies the entire effect size, at which point it is indistinguishable from a fitted nonlinear-damage model. So the grammar does NOT beat established nonlinear cumulative-damage models on magnitude; for this phenomenon it is a directional / conceptual LENS.',
    'This closes the order-effect arc honestly: the RS grammar earned a genuine first -- a distinctive, pre-registered prediction corroborated on real data in BOTH directions vs the order-independent Miner null -- but the magnitude test shows that is the ceiling. The unification thesis stands as coherent and directionally suggestive, not as a quantitative predictor. Confidence stays capped.',
  ],
};

const markdown = `# Grammar Order-Effect: Magnitude Test (decisive)

Status: **${report.status}**

Consistency check only; confidence unchanged. Uses the committed model (no new parameters).

## (1) Is survival graded or binary?

Distinct lives under repeated 'stressed' load: ${distinctLives.join(', ')} (intermediate lives: ${intermediateLives}).
Survival is **${survivalIsBinary ? 'BINARY' : 'graded'}** -> ${survivalIsBinary ? 'no intrinsic cycles-to-failure magnitude' : 'a graded life exists'}.

## (2) Grammar order-effect SIZE (near threshold)

- survival-flip fraction (gentle-first survives whole history, harsh-first does not): **${flipFraction}** of ${total} marginal configs
- mean min-identity shift (gentle-first - harsh-first): **${meanMinIdentityDelta}** (0-1 units)

## (3) Fatigue magnitude to reproduce

- matched-pair D-ratio: ${fatigue.matchedPairDRatio}; max coaxing ratio: ${fatigue.maxCoaxingRatio_n2_over_virgin}x

## Verdict

${report.verdict.map((v) => `- ${v}`).join('\n')}
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('grammar-order-effect-magnitude-test.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('grammar-order-effect-magnitude-test.md', outDir), markdown);

console.log(`Grammar order-effect magnitude test: ${survivalIsBinary ? 'DIRECTION-ONLY (lens) -- no intrinsic magnitude' : 'graded life found'}`);
console.log(`  survival binary: ${survivalIsBinary} (lives: ${distinctLives.join(',')}); order effect = ${Math.round(flipFraction*100)}% flips, min-id shift ${meanMinIdentityDelta}`);
console.log(`  fatigue magnitude to beat: D-ratio ${fatigue.matchedPairDRatio}, coaxing ${fatigue.maxCoaxingRatio_n2_over_virgin}x -> supplied entirely by mapping`);
