import { mkdir, writeFile } from 'node:fs/promises';
import { calculateOutcome, closedForms, transientForms, scenarios, simulateSequence, deriveGrammar, measureResilience, computeCrossRegimeDurability, testRegimeTransition, computeTransitionFragility, computeRegimeStability, findHighStabilitySettings, findBestRegimeForDurability, computeMonteCarloDurability } from '../src/model.js';

const outDir = new URL('./out/', import.meta.url);

const values = [0.15, 0.35, 0.55, 0.75, 0.9];
const phaseValues = [0.2, 0.5, 0.8];
const chargeValues = [-0.6, 0, 0.6];

function compact(row) {
  return {
    closedForm: row.closedForm,
    transientForm: row.transientForm,
    scenario: row.scenario,
    boundary: row.boundary,
    route: row.route,
    storage: row.storage,
    scatter: row.scatter,
    reseat: row.reseat,
    phase: row.phase,
    charge: row.charge,
    continuity: row.grammar ? Number(row.grammar.continuity.toFixed(4)) : null,
    phaseMatch: row.grammar ? Number(row.grammar.phaseMatch.toFixed(4)) : null,
    chargeTension: row.grammar ? Number(row.grammar.chargeTension.toFixed(4)) : null,
    grammarAlignment: row.grammar ? Number(row.grammar.grammarAlignment?.toFixed(4) ?? null) : null,
    identityScore: Number(row.identityScore.toFixed(4)),
    closureStress: Number(row.closureStress.toFixed(4)),
    admitted: Number(row.admitted.toFixed(4)),
    returned: Number(row.returned.toFixed(4)),
    stored: Number(row.stored.toFixed(4)),
    scattered: Number(row.scattered.toFixed(4)),
    identityPreserved: row.identityPreserved,
    coherence: row.coherenceMetric ? Number(row.coherenceMetric.toFixed(4)) : null,
  };
}

const rows = [];
for (const closedForm of closedForms) {
  for (const transientForm of transientForms) {
    for (const scenario of scenarios) {
      for (const boundary of values) {
        for (const route of values) {
          for (const storage of values) {
            for (const scatter of values) {
              for (const reseat of values) {
                for (const phase of phaseValues) {
                  for (const charge of chargeValues) {
                    rows.push(calculateOutcome({ closedForm, transientForm, scenario, boundary, route, storage, scatter, reseat, phase, charge }));
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}

const preserved = rows.filter((row) => row.identityPreserved);
const topCoherent = [...rows]
  .filter((row) => row.identityPreserved)
  .sort((a, b) => b.identityScore - a.identityScore || a.closureStress - b.closureStress)
  .slice(0, 25)
  .map(compact);

const fragile = [...rows]
  .filter((row) => row.identityScore > 0.58 && row.identityScore < 0.68)
  .sort((a, b) => Math.abs(a.identityScore - 0.62) - Math.abs(b.identityScore - 0.62))
  .slice(0, 25)
  .map(compact);

const failure = [...rows]
  .filter((row) => !row.identityPreserved)
  .sort((a, b) => b.closureStress - a.closureStress || a.identityScore - b.identityScore)
  .slice(0, 25)
  .map(compact);

const byPattern = new Map();
for (const row of rows) {
  const key = `${row.closedForm}/${row.transientForm}/${row.scenario}`;
  const current = byPattern.get(key) || { key, count: 0, preserved: 0, avgIdentity: 0, avgStress: 0, bestRow: null, bestId: -1 };
  current.count += 1;
  current.preserved += row.identityPreserved ? 1 : 0;
  current.avgIdentity += row.identityScore;
  current.avgStress += row.closureStress;
  if (row.identityScore > current.bestId) {
    current.bestId = row.identityScore;
    current.bestRow = row;
  }
  byPattern.set(key, current);
}

const patternSummary = [...byPattern.values()]
  .map((item) => ({
    pattern: item.key,
    preservedRate: Number((item.preserved / item.count).toFixed(4)),
    avgIdentity: Number((item.avgIdentity / item.count).toFixed(4)),
    avgStress: Number((item.avgStress / item.count).toFixed(4)),
  }))
  .sort((a, b) => b.preservedRate - a.preservedRate || b.avgIdentity - a.avgIdentity);

// Family-level resilience stats (cheap: one representative "best" case per pattern family)
const resilienceByPattern = [];
for (const [key, item] of byPattern.entries()) {
  if (item.bestRow) {
    const rNom = measureResilience(item.bestRow, { maxSteps: 8, regime: 'nominal' });
    const rStress = measureResilience(item.bestRow, { maxSteps: 8, regime: 'stressed' });
    const robust = computeCrossRegimeDurability(item.bestRow, { maxSteps: 8 });
    resilienceByPattern.push({
      pattern: key,
      avgSurvivedNominal: Number(rNom.survivedSteps.toFixed(2)),
      fullHorizonNominal: rNom.survivedSteps >= 8,
      survivedStressed: rStress.survivedSteps,
      fullHorizonStressed: rStress.survivedSteps >= 8,
      crossRegimeRobustness: robust.robustness,
      minSurvivalAcrossRegimes: robust.minSurvival,
      fullRobustAcrossRegimes: robust.fullRobust,
      dropStressed: robust.dropStressed,
    });
  }
}
resilienceByPattern.sort((a, b) => b.crossRegimeRobustness - a.crossRegimeRobustness || b.avgSurvivedNominal - a.avgSurvivedNominal);

// === v0.3 grammar-centric analysis (pick up & advance the pure logic model) ===
const preservedRows = rows.filter((r) => r.identityPreserved);
const nonPreservedRows = rows.filter((r) => !r.identityPreserved);

function avg(arr) { return arr.length ? arr.reduce((s, v) => s + v, 0) / arr.length : 0; }

const grammarSignature = {
  preserved: {
    avgContinuity: Number(avg(preservedRows.map((r) => r.grammar?.continuity ?? 0)).toFixed(4)),
    avgPhaseMatch: Number(avg(preservedRows.map((r) => r.grammar?.phaseMatch ?? 0)).toFixed(4)),
    avgChargeTension: Number(avg(preservedRows.map((r) => r.grammar?.chargeTension ?? 0)).toFixed(4)),
    avgGrammarAlignment: Number(avg(preservedRows.map((r) => r.grammar?.grammarAlignment ?? 0)).toFixed(4)),
    count: preservedRows.length,
  },
  all: {
    avgContinuity: Number(avg(rows.map((r) => r.grammar?.continuity ?? 0)).toFixed(4)),
    avgPhaseMatch: Number(avg(rows.map((r) => r.grammar?.phaseMatch ?? 0)).toFixed(4)),
    avgChargeTension: Number(avg(rows.map((r) => r.grammar?.chargeTension ?? 0)).toFixed(4)),
    avgGrammarAlignment: Number(avg(rows.map((r) => r.grammar?.grammarAlignment ?? 0)).toFixed(4)),
    count: rows.length,
  },
};

// Grammar region rates (simple signatures that the coherence logic says should matter)
const highGrammar = rows.filter((r) => (r.grammar?.continuity ?? 0) > 0.72 && (r.grammar?.phaseMatch ?? 0) > 0.68 && (r.grammar?.chargeTension ?? 0) < 0.35);
const highGrammarPreservedRate = highGrammar.length ? (highGrammar.filter((r) => r.identityPreserved).length / highGrammar.length) : 0;

const lowGrammar = rows.filter((r) => (r.grammar?.continuity ?? 0) < 0.45 || (r.grammar?.phaseMatch ?? 0) < 0.42 || (r.grammar?.chargeTension ?? 0) > 0.55);
const lowGrammarPreservedRate = lowGrammar.length ? (lowGrammar.filter((r) => r.identityPreserved).length / lowGrammar.length) : 0;

// Threshold flip sensitivity (how fragile is the identityPreserved decision under small grammar changes?)
// Sample the fragile band + some randoms to keep runtime reasonable.
const flipCandidates = [...fragile];
if (flipCandidates.length < 60) {
  // top up with a few borderline identityScore cases
  const extra = [...rows]
    .filter((r) => r.identityScore > 0.55 && r.identityScore < 0.72 && !fragile.includes(r))
    .slice(0, 40);
  flipCandidates.push(...extra);
}
let flipsTested = 0;
let flips = 0;
const deltas = [
  { phase: 0.12 }, { phase: -0.12 },
  { charge: 0.18 }, { charge: -0.18 },
  { route: 0.08, reseat: -0.05 },
];
for (const base of flipCandidates.slice(0, 90)) {
  const baseOutcome = calculateOutcome(base);
  const basePres = baseOutcome.identityPreserved;
  for (const d of deltas) {
    const perturbed = calculateOutcome({ ...base, ...d });
    if (perturbed.identityPreserved !== basePres) {
      flips += 1;
    }
    flipsTested += 1;
  }
}
const flipRate = flipsTested ? Number((flips / flipsTested).toFixed(4)) : 0;

// A few representative traces on high-coherence seeds (to exercise the new sequence simulator)
const topSeeds = topCoherent.slice(0, 3);
const traceExamples = topSeeds.map((seed) => {
  const res = simulateSequence(seed, 4);
  return {
    seed: { closedForm: seed.closedForm, transientForm: seed.transientForm, scenario: seed.scenario },
    summary: res.summary,
    finalStepGrammar: res.trace[res.trace.length - 1].grammar ? {
      continuity: res.trace[res.trace.length - 1].grammar.continuity,
      phaseMatch: res.trace[res.trace.length - 1].grammar.phaseMatch,
    } : null,
  };
});

// Regime transition test on interesting subsets (new: durability under changing conditions)
const defaultTransition = ['nominal', 'nominal', 'stressed', 'stressed', 'recovering', 'recovering', 'recovering', 'recovering'];
const transitionTop = topCoherent.slice(0, 6).map((seed) => {
  const t = testRegimeTransition(seed, { maxSteps: 8, regimeSchedule: defaultTransition });
  return {
    pattern: `${seed.closedForm}/${seed.transientForm}/${seed.scenario}`,
    finalPreserved: t.finalPreserved,
    survivedStressedPhase: t.transitionSummary.survivedThroughStressed,
    stressedInSchedule: t.transitionSummary.stressedStepsInSchedule,
  };
});

const transitionFragile = fragile.slice(0, 6).map((seed) => {
  const t = testRegimeTransition(seed, { maxSteps: 8, regimeSchedule: defaultTransition });
  return {
    pattern: `${seed.closedForm}/${seed.transientForm}/${seed.scenario}`,
    finalPreserved: t.finalPreserved,
    survivedStressedPhase: t.transitionSummary.survivedThroughStressed,
    stressedInSchedule: t.transitionSummary.stressedStepsInSchedule,
  };
});

// Profile fragility (damage caused by specific transition patterns) on interesting subsets
const profileFragTop = topCoherent.slice(0, 4).map((seed) => ({
  pattern: `${seed.closedForm}/${seed.transientForm}/${seed.scenario}`,
  spike: computeTransitionFragility(seed, { maxSteps: 8, profile: 'stress-spike' }).fragility,
  osc: computeTransitionFragility(seed, { maxSteps: 8, profile: 'oscillation' }).fragility,
  degradation: computeTransitionFragility(seed, { maxSteps: 8, profile: 'gradual-degradation' }).fragility,
}));
const profileFragFragile = fragile.slice(0, 3).map((seed) => ({
  pattern: `${seed.closedForm}/${seed.transientForm}/${seed.scenario}`,
  spike: computeTransitionFragility(seed, { maxSteps: 8, profile: 'stress-spike' }).fragility,
}));

// Regime stability (1 - max fragility across profiles) for top/fragile
const stabilityTop = topCoherent.slice(0, 4).map((seed) => {
  const s = computeRegimeStability(seed, { maxSteps: 8 });
  return { pattern: `${seed.closedForm}/${seed.transientForm}/${seed.scenario}`, stability: s.stability, maxFrag: s.maxFragility };
});
const stabilityFragile = fragile.slice(0, 3).map((seed) => {
  const s = computeRegimeStability(seed, { maxSteps: 8 });
  return { pattern: `${seed.closedForm}/${seed.transientForm}/${seed.scenario}`, stability: s.stability, maxFrag: s.maxFragility };
});

// Small "explorer" pass: use findHighStabilitySettings on top cases to show improvement potential
const stabilitySearch = topCoherent.slice(0, 3).map((seed) => {
  const baseSt = computeRegimeStability(seed, { maxSteps: 8 }).stability;
  const search = findHighStabilitySettings(seed, { maxSteps: 8, samples: 15, stepSize: 0.06 });
  const searchWithMemory = findHighStabilitySettings(seed, { maxSteps: 8, samples: 15, stepSize: 0.06, regimeMemory: 0.5 });
  const policy = findBestRegimeForDurability(seed, { maxSteps: 8 });
  const mc = computeMonteCarloDurability(seed, { maxSteps: 8, numTrials: 30 });
  const adaptive = simulateSequence(seed, 8, { adaptivePolicy: true, regimeMemory: 0.5 });
  const adaptiveWithSwitch = simulateSequence(seed, 8, { adaptivePolicy: true, regimeMemory: 0.5, regimeSwitchingCost: 0.2 });
  const avgMem = adaptive.trace && adaptive.trace.length ? (adaptive.trace.reduce((s, t) => s + (t.memoryMod || 0), 0) / adaptive.trace.length) : 0;
  const finalMem = adaptive.trace && adaptive.trace.length ? adaptive.trace[adaptive.trace.length-1].memoryMod : null;
  const presMems = adaptive.trace.filter(t => t.identityPreserved).map(t => t.memoryMod || 0);
  const avgMemPres = presMems.length ? presMems.reduce((s, v) => s + v, 0) / presMems.length : 0;
  const memRescues = adaptive.trace.filter(t => t.memoryRescued).length;
  const highMemAdmitted = adaptive.trace.filter(t => (t.memoryMod || 0) > 0.5).map(t => t.admitted || 0);
  const avgAdmittedHighMem = highMemAdmitted.length ? highMemAdmitted.reduce((s, v) => s + v, 0) / highMemAdmitted.length : 0;
  const highMemCoh = adaptive.trace.filter(t => (t.memoryMod || 0) > 0.5).map(t => t.coherenceMetric || 0);
  const avgCoherenceHighMem = highMemCoh.length ? highMemCoh.reduce((s, v) => s + v, 0) / highMemCoh.length : 0;
  const highMemCarry = adaptive.trace.filter(t => (t.memoryMod || 0) > 0.5).map(t => t.accumContinuity || 0);
  const avgCarryHighMem = highMemCarry.length ? highMemCarry.reduce((s, v) => s + v, 0) / highMemCarry.length : 0;
  const memAdjFinalId = adaptive.summary.memoryAdjustedFinalIdentity || (adaptive.summary.finalIdentity * (1 + avgMem * 0.1));
  const memoryCarriedPres = adaptive.summary.memoryCarriedPreserved || false;
  const memoryCarriedFinalId = memoryCarriedPres ? (adaptive.summary.memoryAdjustedFinalIdentity || (adaptive.summary.finalIdentity * (1 + avgMem * 0.1))) : adaptive.summary.finalIdentity;
  const memoryCarriedFinalPres = adaptive.summary.memoryCarriedFinalPreserved || false;
  const avgPathQ = adaptive.summary.avgPathQuality || (adaptive.trace && adaptive.trace.length ? (adaptive.trace.reduce((s,t)=>s+(t.pathQuality||0.5),0)/adaptive.trace.length) : 0);
  const finalPathQ = adaptive.summary.finalPathQuality || (adaptive.trace && adaptive.trace.length ? (adaptive.trace[adaptive.trace.length-1].pathQuality || 0.5) : 0);
  const carriedQGate = adaptive.summary.memoryCarriedFinalPresQualityGate || 0.58;
  const pathQBoostedFinalId = adaptive.summary.pathQBoostedFinalIdentity || null;
  return {
    pattern: `${seed.closedForm}/${seed.transientForm}/${seed.scenario}`,
    baseStability: baseSt,
    bestFound: search.bestStability,
    improvement: search.improvement,
    withMemoryImprovement: searchWithMemory.improvement,
    baseDurabilityIndex: computeRegimeStability(seed, { maxSteps: 8 }).durabilityIndex,
    projectedDurabilityIndex: search.projectedDurabilityIndex,
    bestRegimeForDurability: policy.bestRegime,
    policyEffectiveDurIdx: policy.bestEffectiveDurabilityIndex,
    mcExpectedFinalPresRate: mc.expectedFinalPresRate,
    mcAvgFinalIdentity: mc.avgFinalIdentity,
    adaptiveFinalPres: adaptive.finalPreserved,
    adaptiveAvgId: adaptive.summary.finalIdentity,
    adaptiveWithSwitchFinalPres: adaptiveWithSwitch.finalPreserved,
    adaptiveWithSwitchAvgId: adaptiveWithSwitch.summary.finalIdentity,
    avgPathMemory: Number(avgMem.toFixed(4)),
    finalPathMemory: finalMem,
    avgMemoryOnPreserved: Number(avgMemPres.toFixed(4)),
    memoryRescues: memRescues,
    avgAdmittedHighMem: Number(avgAdmittedHighMem.toFixed(4)),
    avgCoherenceHighMem: Number(avgCoherenceHighMem.toFixed(4)),
    avgCarryHighMem: Number(avgCarryHighMem.toFixed(4)),
    memoryAdjustedFinalId: memAdjFinalId,
    memoryCarriedPres: memoryCarriedPres,
    memoryCarriedFinalId: memoryCarriedFinalId,
    memoryCarriedFinalPres: memoryCarriedFinalPres,
    avgPathQuality: Number(avgPathQ.toFixed(4)),
    finalPathQuality: Number(finalPathQ.toFixed(4)),
    carriedQualityGate: Number(carriedQGate.toFixed(4)),
    pathQBoostedFinalId,
  };
});

// PathQuality effect on adaptive durability (re-uses the adaptive traces already computed for stabilitySearch).
// High pathQuality histories should show stronger finalPres / carriedPres rates under the model's own consumption rules.
const pathQOnAdaptive = stabilitySearch.map(s => ({
  pattern: s.pattern,
  avgPathQ: s.avgPathQuality,
  finalPathQ: s.finalPathQuality,
  adaptiveFinalPres: s.adaptiveFinalPres,
  memoryCarriedFinalPres: s.memoryCarriedFinalPres,
  carriedQualityGate: s.carriedQualityGate,
}));

// === Resilience / durability on interesting subsets (v0.3+ continuation) ===
// Compute cheaply only on the already-selected top coherent, fragile, and a tiny stratified grammar sample.
// This turns the sweep into a durability explorer without re-running the full grid.
const resilienceTop = topCoherent.slice(0, 10).map((seed) => {
  const r = measureResilience(seed, { maxSteps: 8 });
  return {
    ...compact(seed),
    resilience: {
      survived: r.survivedSteps,
      finalPreserved: r.finalPreserved,
      finalIdentity: Number(r.summary.finalIdentity.toFixed(3)),
      avgPathQ: r.summary.avgPathQuality || null,
      finalPathQ: r.summary.finalPathQuality || null,
      qualityAdjustedSurvived: r.summary.qualityAdjustedSurvived || r.survivedSteps,
    }
  };
});

const resilienceFragile = fragile.slice(0, 10).map((seed) => {
  const r = measureResilience(seed, { maxSteps: 8 });
  return {
    ...compact(seed),
    resilience: {
      survived: r.survivedSteps,
      finalPreserved: r.finalPreserved,
      finalIdentity: Number(r.summary.finalIdentity.toFixed(3)),
      avgPathQ: r.summary.avgPathQuality || null,
      finalPathQ: r.summary.finalPathQuality || null,
      qualityAdjustedSurvived: r.summary.qualityAdjustedSurvived || r.survivedSteps,
    }
  };
});

// Small stratified sample: 2 from high-grammar preserved, 2 from low-grammar
const highSample = highGrammar.filter(r => r.identityPreserved).slice(0, 2).map((seed) => {
  const r = measureResilience(seed, { maxSteps: 8 });
  return { pattern: `${seed.closedForm}/${seed.transientForm}/${seed.scenario}`, survived: r.survivedSteps, finalPres: r.finalPreserved, qualityAdj: r.summary.qualityAdjustedSurvived || r.survivedSteps };
});
const lowSample = lowGrammar.slice(0, 2).map((seed) => {
  const r = measureResilience(seed, { maxSteps: 8 });
  return { pattern: `${seed.closedForm}/${seed.transientForm}/${seed.scenario}`, survived: r.survivedSteps, finalPres: r.finalPreserved, qualityAdj: r.summary.qualityAdjustedSurvived || r.survivedSteps };
});

await mkdir(outDir, { recursive: true });
await writeFile(new URL('coherence-sweep.json', outDir), JSON.stringify({
  total: rows.length,
  preserved: preserved.length,
  preservedRate: Number((preserved.length / rows.length).toFixed(4)),
  patternSummary,
  grammarSignature,
  grammarRegionRates: {
    highGrammarCount: highGrammar.length,
    highGrammarPreservedRate: Number(highGrammarPreservedRate.toFixed(4)),
    lowGrammarCount: lowGrammar.length,
    lowGrammarPreservedRate: Number(lowGrammarPreservedRate.toFixed(4)),
  },
  flipSensitivity: {
    candidatesSampled: flipCandidates.length,
    perturbationsTested: flipsTested,
    flipsDetected: flips,
    flipRate,
  },
  traceExamples,
  resilience: {
    topCoherent: resilienceTop,
    fragile: resilienceFragile,
    highGrammarSample: highSample,
    lowGrammarSample: lowSample,
    byPattern: resilienceByPattern,
  },
  transitions: {
    top: transitionTop,
    fragile: transitionFragile,
  },
  profileFragility: {
    top: profileFragTop,
    fragile: profileFragFragile,
  },
  stability: {
    top: stabilityTop,
    fragile: stabilityFragile,
  },
  stabilitySearch,
  pathQOnAdaptive,
  topCoherent,
  fragile,
  failure,
  note: 'This sweep includes deeper closed feedback: durability now explicitly scales carryFactor (continuity memory retention) and stressRetain (accumStress decay) inside simulateSequence accumulators; adaptive per-step regime choice blends explicit MC expectedFinalPresRate (non-myopic expectation over random future sequences) into scoring. PathQuality (running accumulator blending per-step preservation success * dur * inertia) now further explicitly scales carry and stress decay (beyond dur+mem), lowers rescuer threshold (high quality histories forgive marginal steps more easily), and dynamically lowers the quality gate for memoryCarriedFinalPreserved. Adaptive policy scoring quality-weights its non-myopic (MC+fut) terms. Summaries now expose avgPathQuality, finalPathQuality, memoryCarriedFinalPresQualityGate. NEW: pathQuality now also directly eases consumption/fatigue and amplifies reinf/debt scales in the simulate loop (high sustained quality makes coherence cheaper to maintain and good policy steps self-reinforce more strongly). pathQOnAdaptive shows the correlation of avg/final pathQ with adaptive finalPres + memoryCarriedFinalPres on the explorer traces.',
}, null, 2));

const markdown = `# Relational Substrate Sandbox Coherence Sweep

## Scope

This sweep is a conceptual search over the sandbox rule model. It is not physics validation.

Total combinations: ${rows.length}

Identity preserved: ${preserved.length}

Preserved rate: ${(preserved.length / rows.length).toFixed(4)}

## Best Pattern Families

| Pattern | Preserved rate | Avg identity | Avg stress |
|---|---:|---:|---:|
${patternSummary
  .slice(0, 12)
  .map((row) => `| ${row.pattern} | ${row.preservedRate} | ${row.avgIdentity} | ${row.avgStress} |`)
  .join('\n')}

## Top Coherent Cases

| Closed | Transient | Scenario | Boundary | Route | Storage | Scatter | Reseat | Identity | Stress |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
${topCoherent
  .slice(0, 12)
  .map((row) => `| ${row.closedForm} | ${row.transientForm} | ${row.scenario} | ${row.boundary} | ${row.route} | ${row.storage} | ${row.scatter} | ${row.reseat} | ${row.identityScore} | ${row.closureStress} |`)
  .join('\n')}

## Fragile Boundary Cases

These sit near the preservation threshold and are useful for testing the model language.

| Closed | Transient | Scenario | Boundary | Route | Storage | Scatter | Reseat | Identity | Stress | Preserved |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
${fragile
  .slice(0, 12)
  .map((row) => `| ${row.closedForm} | ${row.transientForm} | ${row.scenario} | ${row.boundary} | ${row.route} | ${row.storage} | ${row.scatter} | ${row.reseat} | ${row.identityScore} | ${row.closureStress} | ${row.identityPreserved} |`)
  .join('\n')}

## High-Stress Failures

| Closed | Transient | Scenario | Boundary | Route | Storage | Scatter | Reseat | Identity | Stress |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
${failure
  .slice(0, 12)
  .map((row) => `| ${row.closedForm} | ${row.transientForm} | ${row.scenario} | ${row.boundary} | ${row.route} | ${row.storage} | ${row.scatter} | ${row.reseat} | ${row.identityScore} | ${row.closureStress} |`)
  .join('\n')}

## First Reading

The current toy model favours high boundary compatibility, high route continuity, low scattering, and high reseating tolerance. That is expected and not yet a discovery. The useful part is the fragile boundary set: those cases show where small changes in storage, scattering, or reseating move a candidate from identity-preserved to identity-at-risk.

## Grammar Signature (v0.3 advance)

Grammar factors are now first-class (via deriveGrammar). Population averages:

- Preserved population: continuity=${grammarSignature.preserved.avgContinuity}, phaseMatch=${grammarSignature.preserved.avgPhaseMatch}, chargeTension=${grammarSignature.preserved.avgChargeTension}, grammarAlignment=${grammarSignature.preserved.avgGrammarAlignment}
- Overall: continuity=${grammarSignature.all.avgContinuity}, phaseMatch=${grammarSignature.all.avgPhaseMatch}, chargeTension=${grammarSignature.all.avgChargeTension}, grammarAlignment=${grammarSignature.all.avgGrammarAlignment}

High-grammar region (cont>0.72, phaseM>0.68, chT<0.35): ${highGrammar.length} cases, preserved rate ${(highGrammarPreservedRate*100).toFixed(1)}%
Low-grammar region (weak on any axis): ${lowGrammar.length} cases, preserved rate ${(lowGrammarPreservedRate*100).toFixed(1)}%

## Identity Threshold Sensitivity (flip rate under small grammar perturbations)

Sampled ${flipCandidates.length} borderline candidates, ${flipsTested} phase/charge/route-reseat perturbations.
Flips observed: ${flips} → flip rate ${ (flipRate*100).toFixed(2) }%

This quantifies how "sharp" the 0.62 / stress<0.62 identity gate is when the underlying grammar elements (phase alignment, charge tension, continuity) are nudged.

## Sequence Trace Examples (simulateSequence)

Three high-coherence seeds were run for 4-step histories with simple memory carry + mild consumption. Each reports finalPreserved + avg/min coherence across the trace:

${traceExamples.map((ex, i) => `- ${ex.seed.closedForm}/${ex.seed.transientForm}/${ex.seed.scenario}: finalPres=${ex.summary.finalPreserved}, startCoh=${ex.summary.startCoherence}, avgCoh=${ex.summary.avgCoherence}, minCoh=${ex.summary.minCoherence}, finalId=${ex.summary.finalIdentity}`).join('\n')}

This begins to move the model from single-interaction snapshots toward "does identity survive a short history of encounters?"

## Resilience & Durability (measureResilience, 8-step horizon)

Resilience measures how many sequential interactions (with memory carry + consumption) a configuration can survive before identity is lost. Computed on the interesting subsets only.

**Top coherent cases (best single-shot) durability:**
${resilienceTop.slice(0,6).map(r => `- ${r.closedForm}/${r.transientForm}/${r.scenario}: survived ${r.resilience.survived}/8 (qa ${r.resilience.qualityAdjustedSurvived}), finalId=${r.resilience.finalIdentity}, fullPres=${r.resilience.finalPreserved}`).join('\n')}

**Fragile/borderline cases durability:**
${resilienceFragile.slice(0,6).map(r => `- ${r.closedForm}/${r.transientForm}/${r.scenario}: survived ${r.resilience.survived}/8 (qa ${r.resilience.qualityAdjustedSurvived}), finalId=${r.resilience.finalIdentity}, fullPres=${r.resilience.finalPreserved}`).join('\n')}

**Stratified grammar samples:**
- High-grammar preserved examples: ${highSample.map(s => `${s.pattern} survived ${s.survived} (qa ${s.qualityAdj})`).join('; ')}
- Low-grammar examples: ${lowSample.map(s => `${s.pattern} survived ${s.survived} (qa ${s.qualityAdj})`).join('; ')}

Key observation from this run: strong grammar alignment (high continuity + phase match, low charge tension) not only raises the chance of identityPreserved on a single interaction but also dramatically extends the number of repeated encounters the configuration can withstand before coherence/identity collapses under the model's consumption rules. High ending pathQuality in a resilience run now provides an additional 'quality-adjusted' lift to the effective survival horizon (the consumption, core gate, and policy quality effects make the order predictably last longer under the abstract rules).

## Resilience by Pattern Family (durability across meeting types)

For each closed/transient/scenario family we took the single best (highest identity) case and measured 8-step survival under regimes + cross-regime robustness (new primitive: min survival across nominal/stressed/recovering, normalized 0-1; 1.0 = fully robust no matter the condition).

| Pattern | Survived (nom) | Full (nom) | Survived (str) | Full (str) | Robustness | Min across | Full robust |
|---|---:|---:|---:|---:|---:|---:|---:|
${resilienceByPattern
  .slice(0, 12)
  .map((r) => `| ${r.pattern} | ${r.avgSurvivedNominal} | ${r.fullHorizonNominal} | ${r.survivedStressed} | ${r.fullHorizonStressed} | ${r.crossRegimeRobustness} | ${r.minSurvivalAcrossRegimes} | ${r.fullRobustAcrossRegimes} |`)
  .join('\n')}

This shows which meeting types produce the most *condition-independent* durable coherent states. Robustness = 1.0 means the grammar alignment survives the full horizon under all tested regimes.

## Regime Transitions (durability under changing conditions)

Using ${'`'}testRegimeTransition${'`'} with a canonical "stress spike then recovery" schedule on the same top and fragile cases. This tests survival when conditions worsen mid-history and then improve.

**Top coherent cases under transition:**
${transitionTop.map((t) => `- ${t.pattern}: finalPres=${t.finalPreserved}, survived stressed phase ${t.survivedStressedPhase}/${t.stressedInSchedule}`).join('\n')}

**Fragile cases under transition:**
${transitionFragile.map((t) => `- ${t.pattern}: finalPres=${t.finalPreserved}, survived stressed phase ${t.survivedStressedPhase}/${t.stressedInSchedule}`).join('\n')}

High-grammar alignments continue to show strong tolerance even when the "environment" (regime) changes during the sequence of meetings.

## Transition Profile Fragility

Fragility = drop in survival steps caused by a specific transition pattern vs pure nominal (0 = no damage).

**On top coherent samples:**
${profileFragTop.map(p => `- ${p.pattern}: spike=${p.spike} osc=${p.osc} degradation=${p.degradation}`).join('\n')}

**On fragile samples (stress-spike):**
${profileFragFragile.map(p => `- ${p.pattern}: spike=${p.spike}`).join('\n')}

## Regime Stability

Stability = 1 - max fragility across all profiles (1.0 = zero damage from any tested transition pattern).

**On top coherent samples:**
${stabilityTop.map(s => `- ${s.pattern}: stability=${s.stability} (maxFrag=${s.maxFrag})`).join('\n')}

**On fragile samples:**
${stabilityFragile.map(s => `- ${s.pattern}: stability=${s.stability} (maxFrag=${s.maxFrag})`).join('\n')}

## Stability Search (local exploration)

Using findHighStabilitySettings (small random perturbations on grammar factors) on a few top cases to estimate how much local improvement in regime stability is still available. Also shown with moderate regimeMemory (inertia from previous regime). Includes Durability Index (composite robustness * stability * low-fragility). Also shows best regime policy (which fixed regime maximizes the durabilityIndex). Adaptive policy (state-aware lookahead choice per step using the policy function).

${stabilitySearch.map(s => `- ${s.pattern}: base stab=${s.baseStability} durIdx=${s.baseDurabilityIndex} → best stab=${s.bestFound} durIdx=${s.projectedDurabilityIndex} (imp ${s.improvement}, mem ${s.withMemoryImprovement}, bestRegime=${s.bestRegimeForDurability} eff=${s.policyEffectiveDurIdx}, MC presRate=${s.mcExpectedFinalPresRate}, adaptive pres=${s.adaptiveFinalPres} avgId=${s.adaptiveAvgId}, adaptive+switch pres=${s.adaptiveWithSwitchFinalPres} avgId=${s.adaptiveWithSwitchAvgId}, avgPathMem=${s.avgPathMemory}, finalMem=${s.finalPathMemory}, memOnPres=${s.avgMemoryOnPreserved}, memRescues=${s.memoryRescues}, avgAdmitHighMem=${s.avgAdmittedHighMem}, avgCohHighMem=${s.avgCoherenceHighMem}, avgCarryHighMem=${s.avgCarryHighMem}, memAdjFinalId=${s.memoryAdjustedFinalId}, memCarriedPres=${s.memoryCarriedPres}, memCarriedFinalId=${s.memoryCarriedFinalId}, memCarriedFinalPres=${s.memoryCarriedFinalPres}, avgPathQ=${s.avgPathQuality}, finalPathQ=${s.finalPathQuality}, carriedQGate=${s.carriedQualityGate}, pathQBoostedFinalId=${s.pathQBoostedFinalId})`).join('\n')}

## PathQuality consumption & reinforcement modulation (latest advance)
PathQuality (running) now directly reduces fatigue in the consumption step and multiplies the reinfScale / debtScale (high pathQ makes good preserved adaptive steps boost carry *more* and bad steps hurt carry *more*). This is the explicit "sustained quality makes coherence cheaper and streaks self-reinforcing" layer.

pathQOnAdaptive (from the same explorer adaptive 8-step traces):
${pathQOnAdaptive.slice(0,6).map(p => `- ${p.pattern}: avgPathQ=${p.avgPathQ} finalPathQ=${p.finalPathQ} pres=${p.adaptiveFinalPres} carriedPres=${p.memoryCarriedFinalPres} gate=${p.carriedQualityGate}`).join('\n')}

This begins to move the model from measurement of durability to active search for more stable regions in the abstract parameter space. The policy helps "choose the best condition" for the config. MC adds average-case expectation over random sequences. Adaptive adds per-step dynamic choice with commitment lookahead (evaluates value of sticking with the regime for the remaining horizon, blended with cross stability; reacts to current accum stress). Switching cost adds friction to changing regimes mid-history (encourages sticking). Reinforcement (small carry boost after preserved policy steps) creates self-reinforcing coherent paths under good choices; debt (carry penalty after poor steps) creates degrading paths under bad choices (balanced virtuous/vicious cycles). Deeper closed-loop: durability now explicitly scales the carry fraction (how much prior continuity memory is retained into the next route) and the accumStress decay rate (how quickly history disturbance is shed) inside the accumulators themselves; adaptive choice directly blends MC expected preservation (non-myopic averaging over many possible future condition stories) into its per-step value scoring. Path memory (the running accumContinuity * (1 - accumStress) after each step) now feeds forward explicitly: before each calculateOutcome the incoming carry boosts the effective route fed to the 4-bucket/grammar/coherence calc, while incoming accumStress raises scatter (history state changes the actual inputs and therefore the coherence/identity numbers on subsequent encounters). The live sandbox now shows "Path Inertia" (memoryMod after short nominal trace on current sliders) next to durability. Adaptive policy imm value now weights by current memory (high inertia makes immediate preservation more attractive). Consumption and accum updates therefore reflect both immediate dur and the explicit carry/decay modulators; the next step's outcome reflects the memoryMod; memory also modulates core coherence/identity/gate when passed -- full cross-scale path-dependent feedback in the pure abstract grammar. Memory now further amplifies reinf and eases fatigue in simulate (stronger self-reinforcing cycles once inertia builds); adaptive commitment value boosted by current memory (high inertia makes sticking with a regime more attractive in lookahead). Memory can rescue marginal identityPreserved in traces (high ending inertia carries the structure across the gate for history success). Memory now also directly modulates the 4-bucket outcomes in the core (high pathMemory/inertia shifts admitted+stored up, scattered down -- history changes the immediate fate fractions). Memory now explicitly modulates grammarAlignment and coherenceMetric in the core too (inertia as a direct 'grammar factor' strengthening alignment for the current step). Memory now directly scales the accumulator carry fraction (higher memory retains more prior continuity carry for deeper persistence) and stress decay rate (faster recovery). This makes built inertia "stickier" for future accumulators. Memory now also scales consumption in resilience measures (measureResilience, cross-regime): high memory eases fatigue and makes storage decay gentler, extending the number of steps a config can survive before identity fails (the "survival horizon" benefits directly from inertia). The trace summary now has explicit memoryAdjustedFinalIdentity (final identity boosted by avgMem, so preservation is not just binary but quality-enhanced by cumulative inertia). Sweep reports avg memory on preserved steps (memOnPres), memoryRescues, avg admitted under high-memory steps (avgAdmitHighMem), avg coherence under high-memory steps (avgCohHighMem), avg carry under high-memory steps (avgCarryHighMem), memoryAdjustedFinalId, and the resilience numbers now reflect memory-extended horizons for high-inertia cases. The memoryWeightedCoherence in trace summaries explicitly reflects the core memory modulation of coherence. UI resilience meters now note inertia est. boost to survived steps. Trace feedback notes memory carried preservation for the whole history (memoryCarriedPres flag). Sweep now reports memoryCarriedPres and memoryCarriedFinalId for adaptive traces in the explorer, quantifying how often high cumulative inertia carries the preservation (and the carried quality of the final identity) for the entire sequence even when the last step is marginal. The trace summary now includes memoryCarriedFinalIdentity as the carried quality when the flag is true. The explorer also reports memoryCarriedFinalPres (the carried preserved with quality threshold) for adaptive, showing when memory carries a high-quality final state. The whole trace can now be "memory-carried preserved" if avgMem high even if the literal last step is marginal (memoryCarriedPres flag). Sweep now reports memoryCarriedPres for adaptive traces in the explorer, quantifying how often high cumulative inertia carries the preservation for the entire sequence even when the last step is marginal. Trace feedback notes memory carried preservation for the whole history. The policy helps "choose the best condition" for the config. MC adds average-case expectation over random sequences. Adaptive adds per-step dynamic choice with commitment lookahead (evaluates value of sticking with the regime for the remaining horizon, blended with cross stability; reacts to current accum stress). Switching cost adds friction to changing regimes mid-history (encourages sticking). Reinforcement (small carry boost after preserved policy steps) creates self-reinforcing coherent paths under good choices; debt (carry penalty after poor steps) creates degrading paths under bad choices (balanced virtuous/vicious cycles). Deeper closed-loop: durability now explicitly scales the carry fraction (how much prior continuity memory is retained into the next route) and the accumStress decay rate (how quickly history disturbance is shed) inside the accumulators themselves; adaptive choice directly blends MC expected preservation (non-myopic averaging over many possible future condition stories) into its per-step value scoring. Path memory (the running accumContinuity * (1 - accumStress) after each step) now feeds forward explicitly: before each calculateOutcome the incoming carry boosts the effective route fed to the 4-bucket/grammar/coherence calc, while incoming accumStress raises scatter (history state changes the actual inputs and therefore the coherence/identity numbers on subsequent encounters). The live sandbox now shows "Path Inertia" (memoryMod after short nominal trace on current sliders) next to durability. Adaptive policy imm value now weights by current memory (high inertia makes immediate preservation more attractive). Consumption and accum updates therefore reflect both immediate dur and the explicit carry/decay modulators; the next step's outcome reflects the memoryMod; memory also modulates core coherence/identity/gate when passed -- full cross-scale path-dependent feedback in the pure abstract grammar. Memory now further amplifies reinf and eases fatigue in simulate (stronger self-reinforcing cycles once inertia builds); adaptive commitment lookahead value is boosted by current memory (high inertia makes "sticking" with a regime more valuable in the farsighted score). Sweep reports avg memory on preserved steps (memOnPres) to quantify the benefit.
`;

await writeFile(new URL('coherence-sweep-summary.md', outDir), markdown);

console.log(`Swept ${rows.length} combinations.`);
console.log(`Identity preserved in ${preserved.length} combinations (${(preserved.length / rows.length).toFixed(4)}).`);
console.log(`Wrote ${new URL('coherence-sweep-summary.md', outDir).pathname}`);
