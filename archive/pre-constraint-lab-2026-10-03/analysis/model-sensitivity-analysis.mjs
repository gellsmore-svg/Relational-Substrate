// Model-form sensitivity analysis (process recommendation #5).
//
// Characterizes how the sandbox's "coherent region" (identityPreserved)
// depends on modelling choices, rather than on the inputs alone:
//   - the identityScore cutoff (currently 0.62)
//   - the closureStress cutoff (currently 0.62)
//   - the six metric weights inside identityScore
//   - which of the five continuous inputs move identity the most
//
// This is a robustness/stability characterization of the TOY MODEL. It is
// not physics validation and makes no claim about the substrate. It reads
// only the values calculateOutcome already returns (the component metrics
// closureMetric…leakageMetric and identityScore/closureStress), so it never
// modifies or re-implements the model. Bias-table robustness (formBias etc.)
// is out of scope here because those live inside calculateOutcome and would
// require parameterizing the model — a separate, non-additive change.

import { mkdir, writeFile } from 'node:fs/promises';
import { calculateOutcome, closedForms, transientForms, scenarios } from '../src/model.js';

const outDir = new URL('./out/', import.meta.url);

const BASE_IDENTITY = 0.62; // src/model.js: identityScore >= 0.62
const BASE_STRESS = 0.62; // src/model.js: closureStress < 0.62

// identityScore weights as declared in src/model.js calculateOutcome (sum 1.0)
const baseWeights = {
  closure: 0.18,
  return: 0.18,
  bounded: 0.17,
  coherence: 0.18,
  reseat: 0.14,
  leakage: 0.15,
};

const values = [0.1, 0.3, 0.5, 0.7, 0.9];
const inputs = ['boundary', 'route', 'storage', 'scatter', 'reseat'];

const clamp01 = (v) => Math.max(0, Math.min(1, v));
const mean = (xs) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : 0);
const r4 = (v) => Number(v.toFixed(4));

// --- full sweep over the sandbox input space -------------------------------
const rows = [];
for (const closedForm of closedForms) {
  for (const transientForm of transientForms) {
    for (const scenario of scenarios) {
      for (const boundary of values) {
        for (const route of values) {
          for (const storage of values) {
            for (const scatter of values) {
              for (const reseat of values) {
                rows.push(
                  calculateOutcome({ closedForm, transientForm, scenario, boundary, route, storage, scatter, reseat }),
                );
              }
            }
          }
        }
      }
    }
  }
}

const N = rows.length;
const coherentRate = (arr, idCut, stCut) =>
  arr.filter((r) => r.identityScore >= idCut && r.closureStress < stCut).length / (arr.length || 1);

const baseRate = coherentRate(rows, BASE_IDENTITY, BASE_STRESS);

// --- 1. threshold sensitivity (one knob at a time) -------------------------
const cuts = [];
for (let c = 0.5; c <= 0.7401; c += 0.02) cuts.push(r4(c));

const identityCutSweep = cuts.map((c) => ({ cut: c, rate: r4(coherentRate(rows, c, BASE_STRESS)) }));
const stressCutSweep = cuts.map((c) => ({ cut: c, rate: r4(coherentRate(rows, BASE_IDENTITY, c)) }));

// local slope near the base gate, expressed as Δ(coherent rate) per +0.01 cutoff
const d = 0.02;
const identitySlopePer01 = r4(
  ((coherentRate(rows, BASE_IDENTITY + d, BASE_STRESS) - coherentRate(rows, BASE_IDENTITY - d, BASE_STRESS)) / (2 * d)) *
    0.01,
);
const stressSlopePer01 = r4(
  ((coherentRate(rows, BASE_IDENTITY, BASE_STRESS + d) - coherentRate(rows, BASE_IDENTITY, BASE_STRESS - d)) / (2 * d)) *
    0.01,
);

// joint nudge: tighten both vs loosen both
const jointNudges = [0.02, 0.05].map((eps) => ({
  eps,
  tighter: r4(coherentRate(rows, BASE_IDENTITY + eps, BASE_STRESS - eps)),
  looser: r4(coherentRate(rows, BASE_IDENTITY - eps, BASE_STRESS + eps)),
}));

// --- 2. which gate clause binds among non-coherent samples -----------------
let failIdentityOnly = 0;
let failStressOnly = 0;
let failBoth = 0;
let nonCoherent = 0;
for (const r of rows) {
  const idOk = r.identityScore >= BASE_IDENTITY;
  const stOk = r.closureStress < BASE_STRESS;
  if (idOk && stOk) continue;
  nonCoherent += 1;
  if (!idOk && !stOk) failBoth += 1;
  else if (!idOk) failIdentityOnly += 1;
  else failStressOnly += 1;
}
const bindingClause = {
  nonCoherent,
  failIdentityOnly,
  failStressOnly,
  failBoth,
  identityShare: r4(failIdentityOnly / (nonCoherent || 1)),
  stressShare: r4(failStressOnly / (nonCoherent || 1)),
  bothShare: r4(failBoth / (nonCoherent || 1)),
};

// --- 3. per-input marginal influence ---------------------------------------
const inputSensitivity = inputs
  .map((name) => {
    const byLevel = values.map((v) => {
      const sub = rows.filter((r) => r[name] === v);
      return {
        level: v,
        meanIdentity: r4(mean(sub.map((r) => r.identityScore))),
        rate: r4(coherentRate(sub, BASE_IDENTITY, BASE_STRESS)),
      };
    });
    const rates = byLevel.map((b) => b.rate);
    const ids = byLevel.map((b) => b.meanIdentity);
    return {
      input: name,
      byLevel,
      identityDelta: r4(ids[ids.length - 1] - ids[0]), // mean identity at hi level minus lo level
      coherentRateSpread: r4(Math.max(...rates) - Math.min(...rates)),
    };
  })
  .sort((a, b) => Math.abs(b.identityDelta) - Math.abs(a.identityDelta));

// --- 4. stability across categorical forms / scenarios ---------------------
const byForm = closedForms.map((f) => ({
  closedForm: f,
  rate: r4(coherentRate(rows.filter((r) => r.closedForm === f), BASE_IDENTITY, BASE_STRESS)),
}));
const byScenario = scenarios.map((s) => ({
  scenario: s,
  rate: r4(coherentRate(rows.filter((r) => r.scenario === s), BASE_IDENTITY, BASE_STRESS)),
}));

// --- 5. metric-weight robustness (recomputed from returned component metrics)
const identityFromWeights = (r, w) => {
  const sum = w.closure + w.return + w.bounded + w.coherence + w.reseat + w.leakage;
  return clamp01(
    (r.closureMetric * w.closure +
      r.returnMetric * w.return +
      r.boundedMetric * w.bounded +
      r.coherenceMetric * w.coherence +
      r.reseatMetric * w.reseat +
      r.leakageMetric * w.leakage) /
      sum,
  );
};
// sanity: reproduce identityScore under base weights
const reproMaxErr = r4(Math.max(...rows.map((r) => Math.abs(identityFromWeights(r, baseWeights) - r.identityScore))));

const weightPerturb = Object.keys(baseWeights)
  .map((k) => {
    const up = { ...baseWeights, [k]: baseWeights[k] * 1.1 };
    const down = { ...baseWeights, [k]: baseWeights[k] * 0.9 };
    const rateUp = rows.filter((r) => identityFromWeights(r, up) >= BASE_IDENTITY && r.closureStress < BASE_STRESS).length / N;
    const rateDown =
      rows.filter((r) => identityFromWeights(r, down) >= BASE_IDENTITY && r.closureStress < BASE_STRESS).length / N;
    return {
      weight: k,
      base: baseWeights[k],
      rateAtMinus10pct: r4(rateDown),
      rateAtPlus10pct: r4(rateUp),
      maxShiftVsBase: r4(Math.max(Math.abs(rateUp - baseRate), Math.abs(rateDown - baseRate))),
    };
  })
  .sort((a, b) => b.maxShiftVsBase - a.maxShiftVsBase);

// --- assemble + write ------------------------------------------------------
const result = {
  scope: 'Toy-model sensitivity/robustness characterization. Not physics validation; no substrate claim.',
  totalSamples: N,
  grid: { levels: values, forms: closedForms, transients: transientForms, scenarios },
  baseGate: { identityCut: BASE_IDENTITY, stressCut: BASE_STRESS, coherentRate: r4(baseRate) },
  thresholdSensitivity: {
    identityCutSweep,
    stressCutSweep,
    identitySlopePerPlus01: identitySlopePer01,
    stressSlopePerPlus01: stressSlopePer01,
    jointNudges,
  },
  bindingClause,
  inputSensitivity,
  categoryStability: { byForm, byScenario },
  weightRobustness: { baseWeights, reproMaxErr, weightPerturb },
};

await mkdir(outDir, { recursive: true });
await writeFile(new URL('model-sensitivity-analysis.json', outDir), JSON.stringify(result, null, 2));

const tbl = (rowsArr, cols) => rowsArr.map((r) => `| ${cols.map((c) => r[c]).join(' | ')} |`).join('\n');

const markdown = `# Toy-Model Sensitivity Analysis

**Scope.** This characterizes how the sandbox's coherent region (\`identityPreserved\`)
depends on **modelling choices** — the two gate thresholds, the six identity-metric
weights, and which inputs dominate. It is a robustness study of the toy model
(process recommendation #5). **It is not physics validation and makes no claim
about the substrate.**

Samples: ${N} (grid of ${values.length} levels over 5 inputs × ${closedForms.length}×${transientForms.length}×${scenarios.length} form/scenario combinations).

Base gate: \`identityScore ≥ ${BASE_IDENTITY}\` and \`closureStress < ${BASE_STRESS}\` → coherent rate **${r4(baseRate)}**.

## 1. Threshold sensitivity

Local slope near the base gate (change in coherent rate per **+0.01** to the cutoff):
- identity cutoff: **${identitySlopePer01}** per +0.01
- closureStress cutoff: **${stressSlopePer01}** per +0.01

Joint nudge of both gates:

| ± | tighten both | loosen both |
|---:|---:|---:|
${jointNudges.map((j) => `| ${j.eps} | ${j.tighter} | ${j.looser} |`).join('\n')}

Coherent rate vs identity cutoff (closureStress fixed at ${BASE_STRESS}):

| identity cutoff | coherent rate |
|---:|---:|
${tbl(identityCutSweep, ['cut', 'rate'])}

Coherent rate vs closureStress cutoff (identity fixed at ${BASE_IDENTITY}):

| stress cutoff | coherent rate |
|---:|---:|
${tbl(stressCutSweep, ['cut', 'rate'])}

## 2. Which gate clause binds

Of ${bindingClause.nonCoherent} non-coherent samples:
- fail identity clause only: ${bindingClause.failIdentityOnly} (${bindingClause.identityShare})
- fail closureStress clause only: ${bindingClause.failStressOnly} (${bindingClause.stressShare})
- fail both: ${bindingClause.failBoth} (${bindingClause.bothShare})

## 3. Input influence on identity (ranked)

\`identityDelta\` = mean identityScore at the highest input level minus the lowest.

| input | identityDelta | coherent-rate spread |
|---|---:|---:|
${tbl(inputSensitivity, ['input', 'identityDelta', 'coherentRateSpread'])}

## 4. Stability across categories

| closed form | coherent rate |
|---|---:|
${tbl(byForm, ['closedForm', 'rate'])}

| scenario | coherent rate |
|---|---:|
${tbl(byScenario, ['scenario', 'rate'])}

## 5. Metric-weight robustness

Each identityScore weight perturbed ±10% (others held), recomputed from the
component metrics the model returns (reproduction error vs the model's own
identityScore: ${reproMaxErr}). Ranked by largest coherent-rate shift.

| weight | base | rate −10% | rate +10% | max shift vs base (${r4(baseRate)}) |
|---|---:|---:|---:|---:|
${tbl(weightPerturb, ['weight', 'base', 'rateAtMinus10pct', 'rateAtPlus10pct', 'maxShiftVsBase'])}

## Reading

These numbers describe the **model form**, not the world. They are useful for
defending or challenging the sandbox's coherent region during review: a small
local slope and small weight-shift numbers mean the coherent region is a
plateau (robust to the exact 0.62 choices); large numbers mean it sits on a
cliff and the threshold/weight choices are load-bearing. The binding-clause
split shows whether the identity cutoff or the closureStress cutoff is the
active constraint. None of this raises or supports any substrate claim.
`;

await writeFile(new URL('model-sensitivity-analysis-summary.md', outDir), markdown);

console.log(`Sensitivity analysis over ${N} samples.`);
console.log(`Base coherent rate: ${r4(baseRate)} (identity≥${BASE_IDENTITY}, stress<${BASE_STRESS}).`);
console.log(`Identity-cut slope: ${identitySlopePer01}/+0.01 | stress-cut slope: ${stressSlopePer01}/+0.01.`);
console.log(
  `Binding among non-coherent: identity-only ${bindingClause.identityShare}, stress-only ${bindingClause.stressShare}, both ${bindingClause.bothShare}.`,
);
console.log(`Top input influence: ${inputSensitivity[0].input} (Δidentity ${inputSensitivity[0].identityDelta}).`);
console.log(`Wrote ${new URL('model-sensitivity-analysis-summary.md', outDir).pathname}`);
