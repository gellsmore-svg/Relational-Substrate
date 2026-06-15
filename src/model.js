export const closedForms = ['circle', 'trefoil', 'double'];
export const transientForms = ['straight', 'sine', 'ribbon'];
export const scenarios = ['admit', 'return', 'store'];

export const scenarioPresets = {
  admit: { boundary: 0.82, route: 0.78, storage: 0.18, scatter: 0.12, reseat: 0.7, phase: 0.5, charge: 0.0 },
  return: { boundary: 0.22, route: 0.32, storage: 0.24, scatter: 0.18, reseat: 0.74, phase: 0.3, charge: 0.2 },
  store: { boundary: 0.48, route: 0.42, storage: 0.7, scatter: 0.5, reseat: 0.46, phase: 0.7, charge: -0.15 },
};

const formBias = {
  circle: { closure: 0.02, return: 0.03, bounded: 0, coherence: 0.03, reseat: 0.04, leakage: 0.02 },
  trefoil: { closure: 0.06, return: 0.04, bounded: 0.04, coherence: -0.01, reseat: -0.02, leakage: 0.01 },
  double: { closure: 0.04, return: 0.07, bounded: -0.01, coherence: -0.03, reseat: -0.01, leakage: -0.02 },
};

const transientBias = {
  straight: { route: 0.05, scatter: -0.03, storage: -0.02 },
  sine: { route: -0.02, scatter: 0.02, storage: 0.03 },
  ribbon: { route: -0.04, scatter: 0.04, storage: 0.02 },
};

const scenarioBias = {
  admit: { admitted: 0.22, returnedScale: 0.55, storedScale: 0.72, scattered: 0 },
  return: { admittedScale: 0.48, returned: 0.36, storedScale: 0.7, scattered: 0 },
  store: { admittedScale: 0.66, returnedScale: 1, stored: 0.22, scattered: 0.14 },
};

export function clamp01(value) {
  return Math.max(0, Math.min(1, value));
}

// === Pure grammar derivation (v0.3 advancement) ===
// The five first-class substrate grammar elements in the abstract model:
// - route (continuity source from the transient path)
// - closure (compatibility/boundary of the closed stable order)
// - phase (alignment / timing match between transient and closed)
// - charge (tension / asymmetry / polarity stress)
// - continuity (persistence / memory of the route across disturbance)
// This helper isolates the mapping so the logic is explicit and reusable.
export function deriveGrammar(input = {}) {
  const route = clamp01((input.route ?? 0.5) + (transientBias[input.transientForm]?.route ?? 0));
  const reseat = input.reseat ?? 0.5;
  const phase = typeof input.phase === 'number' ? clamp01(input.phase) : 0.5;
  const charge = typeof input.charge === 'number' ? input.charge : 0.0;

  const continuity = clamp01(route * 0.58 + reseat * 0.42); // persistence of the route
  const phaseMatch = clamp01(1 - Math.abs(phase - 0.5) * 1.9); // alignment between transient and closed
  const chargeTension = clamp01(Math.abs(charge)); // asymmetry / tension (higher = more stress risk)

  return {
    continuity,
    phaseMatch,
    chargeTension,
    phase,
    charge,
    // route and closure (boundary) are passed through for callers that want the five-tuple view
    route,
    closure: input.boundary ?? 0.5,
  };
}

export function calculateOutcome(input, options = {}) {
  const skipDurability = options.skipDurability || false;

  const fBias = formBias[input.closedForm] || formBias.trefoil;
  const tBias = transientBias[input.transientForm] || transientBias.straight;
  const sBias = scenarioBias[input.scenario] || scenarioBias.admit;

  const boundary = input.boundary;
  const route = clamp01(input.route + tBias.route);
  const storageSetting = clamp01(input.storage + tBias.storage);
  const scatterSetting = clamp01(input.scatter + tBias.scatter);
  const reseat = input.reseat;

  // Grammar now derived from the dedicated helper (keeps single source of truth)
  let g = deriveGrammar(input);
  if (options.pathMemory !== undefined) {
    const mem = clamp01(options.pathMemory);
    // Path memory boosts the 'continuity' component of grammar (inertia makes the route persistence stronger in the alignment for this step).
    g.continuity = clamp01(g.continuity * (1 + mem * 0.08));
  }
  const { continuity, phaseMatch, chargeTension, phase, charge } = g;

  // Original 4-bucket logic (preserved for compatibility + viz), lightly augmented with grammar factors
  let admitted = boundary * route * continuity * phaseMatch * (1 - chargeTension * 0.32) * (1 - scatterSetting * 0.52);
  let returned = (1 - boundary) * (0.71 + (1 - route) * 0.29) * (1 - phaseMatch * 0.22);
  let stored = storageSetting * (1 - route * 0.36) * (1 - phaseMatch * 0.12) * (1 + chargeTension * 0.22);
  let scattered = scatterSetting * (1 - boundary * 0.27) * (1 + chargeTension * 0.38) * (1 - continuity * 0.18);

  if (sBias.admitted) admitted += sBias.admitted;
  if (sBias.returned) returned += sBias.returned;
  if (sBias.stored) stored += sBias.stored;
  if (sBias.scattered) scattered += sBias.scattered;
  if (sBias.admittedScale) admitted *= sBias.admittedScale;
  if (sBias.returnedScale) returned *= sBias.returnedScale;
  if (sBias.storedScale) stored *= sBias.storedScale;

  const total = admitted + returned + stored + scattered || 1;
  admitted /= total;
  returned /= total;
  stored /= total;
  scattered /= total;

  // Memory modulation of 4-bucket outcomes (pure logic): when pathMemory (inertia from history) is passed, high memory shifts the immediate encounter toward persistence.
  // High inertia "holds" more of the transient coherently (higher admitted + stored, lower scattered) — history state changes the fate fractions themselves.
  if (options.pathMemory !== undefined) {
    const mem = clamp01(options.pathMemory);
    admitted = clamp01(admitted * (1 + mem * 0.12));
    stored = clamp01(stored * (1 + mem * 0.08));
    scattered = clamp01(scattered * (1 - mem * 0.15));
    returned = clamp01(returned * (1 - mem * 0.04));
    const t2 = admitted + returned + stored + scattered || 1;
    admitted /= t2;
    returned /= t2;
    stored /= t2;
    scattered /= t2;
  }

  // === Metrics (gate scores) - evolved coherence logic (v0.3) ===
  let closureStress = stored * 0.60 + scattered * 0.50 + (1 - reseat) * 0.34 + chargeTension * 0.18;

  const closureMetric = clamp01(0.71 + reseat * 0.19 - scattered * 0.30 + fBias.closure);
  const returnMetric = clamp01(boundary * 0.27 + route * 0.25 + reseat * 0.44 - stored * 0.17 + fBias.return);
  const boundedMetric = clamp01(0.85 - stored * 0.28 - scattered * 0.24 + boundary * 0.11 + fBias.bounded);

  // Advanced coherence (pure logic grammar composition):
  // Coherence is primarily the alignment of the five grammar elements (route/closure/phase/charge/continuity)
  // under low scatter. We compute an explicit grammarAlignment (multiplicative core) plus a small
  // additive baseAlignment rescue (so a single weak factor does not instantly zero everything).
  const grammarAlignment = continuity * phaseMatch * (1 - chargeTension) * (1 - scatterSetting * 0.68);
  const baseAlignment = (route * 0.50 + boundary * 0.28 + reseat * 0.22);
  let coherenceMetric = clamp01(
    grammarAlignment * 0.82 + baseAlignment * 0.18 + fBias.coherence
  );

  // Memory now explicitly participates in the grammarAlignment and coherenceMetric (pure logic: built inertia from history strengthens the alignment of the five grammar elements for the current step).
  if (options.pathMemory !== undefined) {
    const mem = clamp01(options.pathMemory);
    // High memory directly boosts the multiplicative grammarAlignment term (inertia as a 'memory factor' in coherence).
    // This makes coherence itself reflect the accumulated history state.
    const memBoost = 1 + 0.1 * mem;
    coherenceMetric = clamp01(coherenceMetric * memBoost);
  }

  const reseatMetric = clamp01(reseat - closureStress * 0.23 + fBias.reseat);
  const leakageMetric = clamp01(1 - (stored * 0.37 + scattered * 0.48 + (1 - boundary) * 0.15) + fBias.leakage);

  let identityScore = clamp01(
    closureMetric * 0.16 +
      returnMetric * 0.16 +
      boundedMetric * 0.15 +
      coherenceMetric * 0.20 +     // slightly higher weight on evolved coherence
      reseatMetric * 0.13 +
      leakageMetric * 0.12 +
      continuity * 0.08            // continuity now contributes directly to identity
  );

  let identityPreserved = identityScore >= 0.62 && closureStress < 0.62;

  // Integrate Durability Index back into core (long-term view affects immediate metrics)
  let durabilityIndex = 0;
  let modulatedIdentityScore = identityScore;
  if (!skipDurability) {
    const durObj = computeRegimeStability(input, { maxSteps: 8 });
    durabilityIndex = durObj.durabilityIndex;
    let durabilityBoost = 0.1 * durabilityIndex;
    if (options.pathQuality !== undefined) {
      // pathQuality (0-1) from recent reinforcement/debt scales the durability boost (closes the loop between long-term dynamics and immediate metrics)
      durabilityBoost *= (0.5 + 0.5 * options.pathQuality);
    }
    modulatedIdentityScore = clamp01(identityScore * (0.9 + durabilityBoost));

    // Extend feedback to closureStress and identityPreserved in the core single-shot view (high dur makes preservation "easier" in the immediate metrics too).
    closureStress = clamp01(closureStress * (1 - durabilityIndex * 0.2));
    identityPreserved = modulatedIdentityScore >= 0.62 && closureStress < 0.62;

    // Also modulate coherenceMetric with dur for the long-term view in single-shot.
    coherenceMetric = clamp01(coherenceMetric * (0.95 + 0.05 * durabilityIndex));
  }

  // Integrate path memory (accumulated coherence inertia from history / simulateSequence) into the core single-shot view.
  // This closes another layer of the loop: memory built across steps now directly strengthens coherence and makes identity preservation slightly more forgiving in the instantaneous calculation (analogous to durability).
  if (options.pathMemory !== undefined) {
    const mem = clamp01(options.pathMemory);
    const memBoost = 0.08 * mem;
    // High memory boosts the coherence term (stronger grammar alignment effect when history has built inertia).
    coherenceMetric = clamp01(coherenceMetric * (0.97 + 0.03 * mem));
    modulatedIdentityScore = clamp01((modulatedIdentityScore || identityScore) * (0.95 + memBoost));
    // Slight relaxation: high memory reduces effective closure stress and softens the gate (history "helps" preservation).
    closureStress = clamp01(closureStress * (1 - 0.12 * mem));
    identityPreserved = modulatedIdentityScore >= 0.60 && closureStress < 0.60;
  }

  return {
    ...input,
    admitted,
    returned,
    stored,
    scattered,
    identityPreserved,
    closureStress,
    closureMetric,
    returnMetric,
    boundedMetric,
    coherenceMetric,
    reseatMetric,
    leakageMetric,
    identityScore,
    // New explicit grammar state for downstream use (UI, sweeps, books)
    grammar: {
      continuity,
      phaseMatch,
      chargeTension,
      phase,
      charge,
      grammarAlignment,   // v0.3: primary multiplicative grammar health term
    },
    metrics: {
      closure: closureMetric,
      return: returnMetric,
      bounded: boundedMetric,
      coherence: coherenceMetric,
      reseat: reseatMetric,
      leakage: leakageMetric,
      identity: identityScore,
      continuity,
      phaseMatch,
      chargeTension,
      grammarAlignment,
      durabilityIndex,
      modulatedIdentity: modulatedIdentityScore,
      pathMemory: options.pathMemory !== undefined ? clamp01(options.pathMemory) : undefined,
    },
    pathMemory: options.pathMemory !== undefined ? clamp01(options.pathMemory) : undefined,
  };
}

/**
 * simulateSequence (pure-logic advancement)
 * Runs a short chain of interactions starting from baseInput.
 * Demonstrates how identity and coherence behave "over time" (repeated meetings)
 * rather than in a single snapshot.
 *
 * Memory / carry rules (still abstract toy rules):
 * - A fraction of previous-step continuity "carries" into the next route.
 * - Stress slowly accumulates (decays between steps).
 * - Each step mildly "consumes" storage and adds a little scatter (fatigue) unless reseat is excellent.
 * - Final identityPreserved of the trace is what matters for "did the closed order survive the history coherently".
 *
 * Returns: { trace: Outcome[], finalPreserved: bool, summary }
 */
export function simulateSequence(baseInput = {}, stepCount = 4, options = {}) {
  const trace = [];
  let current = { ...baseInput };
  let accumContinuity = 0.5;
  let accumStress = 0.0;
  let pathQuality = 0.5;  // running accumulator of sustained success quality (blend of preservation, durability, inertia). High values close virtuous loops: better carry, faster stress recovery, easier rescue, lower bar for carried-final quality.

  const regimeSchedule = options.regimeSchedule || null;
  const regimeMemory = options.regimeMemory ?? 0;  // 0 = no memory (instant switch), 1 = full persistence of previous regime's effects
  const adaptivePolicy = options.adaptivePolicy || false;  // if true, at each step greedily pick the regime that maximizes durabilityIndex for the config (pure logic "choose the condition to best preserve coherence")
  const regimeSwitchingCost = options.regimeSwitchingCost ?? 0;  // 0 = free to switch regimes mid-history; >0 penalizes changes (models friction/cost of shifting conditions, encouraging "sticking" with good regimes)

  let prevRegime = null;

  for (let step = 0; step < stepCount; step += 1) {
    let stepRegime = regimeSchedule ? (regimeSchedule[step] || regimeSchedule[regimeSchedule.length - 1] || 'nominal') : 'nominal';
    if (adaptivePolicy) {
      // State-aware adaptive choice: pick regime that maximizes immediate "goodness" (low fatigue, high reseat, low current stress) + discounted future stability/durability.
      // Pure logic "farsighted choice of conditions to preserve coherence".
      const regimes = ['nominal', 'stressed', 'recovering'];
      let bestR = regimes[0];
      let bestV = -Infinity;
      regimes.forEach(r => {
        const mods = getRegimeModulators(r);
        let imm = (1 - mods.fatigueFactor * 0.3 + mods.reseatBoost * 0.2) * (1 - accumStress * 0.4);  // immediate step quality, penalized by current stress
        // Path memory / inertia weighting in immediate value: high current memory (coherence that has persisted) makes preserving more attractive right now (pure logic momentum).
        const currentMem = clamp01(accumContinuity * (1 - accumStress));
        imm = imm * (1 + 0.08 * currentMem);
        // PathQuality weighting (new): high sustained success quality makes future preservation expectation more valuable in the choice (quality-weighted non-myopic scoring).
        const currentPathQEst = clamp01(0.6 * pathQuality + 0.4 * currentMem);
        imm = imm * (0.92 + 0.08 * currentPathQEst);
        let futValue = computeRegimeStability({ ...current, ...baseInput }, { maxSteps: 8, regimeMemory }).stability;  // future value under best for this choice (cross-profile stability)
        const remaining = stepCount - step;
        if (remaining > 1) {
          // Lookahead with "commitment": simulate a short horizon *sticking* with this r and blend the outcome (high if preserves well under commitment to r)
          const commitSchedule = Array(remaining).fill(r);
          const commitTrans = testRegimeTransition({ ...current, ...baseInput }, { maxSteps: remaining, regimeSchedule: commitSchedule, regimeMemory });
          const commitScore = commitTrans.finalPreserved ? 1.0 : (commitTrans.summary.finalIdentity || 0.5);
          // Memory boost to commitment value: high current memory (inertia) makes the projected value of sticking with this regime higher (pure logic: built coherence makes long-term commitment to a good regime more attractive).
          const memBoostedCommit = commitScore * (1 + 0.15 * currentMem);
          futValue = 0.5 * futValue + 0.5 * memBoostedCommit;  // blend general stability with commitment-specific preservation under sticking with r
        }
        // Non-myopic extension (pure logic): blend explicit Monte-Carlo expected final preservation rate (averaged over many random future condition sequences / profiles)
        // directly into the per-step value. This makes regime choice at each step average over uncertainty in future "stories" rather than relying only on immediate + one commitment path.
        let mcExp = 0.5;
        try {
          const mcProbe = computeMonteCarloDurability({ ...current, ...baseInput }, { maxSteps: Math.min(4, remaining || 3), numTrials: 5, regimeMemory });
          mcExp = mcProbe.expectedFinalPresRate || 0.5;
        } catch (_) { /* keep neutral on any transient issue; never break the trace */ }
        // PathQuality scales the non-myopic components (MC + fut) so that high-quality histories value long-term expectation more (self-reinforcing choice under good running quality).
        const vNonMyopicScale = (0.85 + 0.15 * currentPathQEst);
        let v = imm + 0.45 * futValue * vNonMyopicScale + 0.25 * mcExp * vNonMyopicScale;  // non-myopic + quality-weighted
        if (prevRegime && r !== prevRegime) {
          v -= regimeSwitchingCost * 0.3;  // penalize switch (friction/cost of changing conditions)
        }
        if (v > bestV) {
          bestV = v;
          bestR = r;
        }
      });
      stepRegime = bestR;
    }
    let mods = getRegimeModulators(stepRegime);

    // Regime memory / inertia: blend current mods with previous regime's if memory > 0
    if (regimeMemory > 0 && prevRegime) {
      const prevMods = getRegimeModulators(prevRegime);
      const m = regimeMemory;
      mods = {
        fatigueBase: mods.fatigueBase * (1 - m) + prevMods.fatigueBase * m,
        fatigueFactor: mods.fatigueFactor * (1 - m) + prevMods.fatigueFactor * m,
        storageDecay: mods.storageDecay * (1 - m) + prevMods.storageDecay * m,
        scatterBias: mods.scatterBias * (1 - m) + prevMods.scatterBias * m,
        reseatBoost: mods.reseatBoost * (1 - m) + prevMods.reseatBoost * m,
      };
    }

    // Inject carried continuity as a mild boost/anchor on the route for this step.
    // Path-memory feed-forward (new pure-logic layer): the running accumulators (built from prior steps' grammar + durability-scaled carry/decay)
    // now directly alter the *inputs* to this step's calculation. High carry (persisted coherence memory) boosts the effective route.
    // High accumStress (built disturbance) raises scatter for this encounter. This makes successful history make future encounters start stronger
    // (and stressed history makes them harder) before the 4-bucket, grammarAlignment, coherence, and identity gate are even computed.
    const carriedRoute = clamp01((current.route ?? 0.5) * 0.72 + accumContinuity * 0.28);
    const stepInput = {
      ...current,
      route: carriedRoute,
    };

    // Additional explicit feed from the *current* accum state (incoming memory at the start of this step).
    stepInput.route = clamp01(stepInput.route + accumContinuity * 0.12);
    stepInput.scatter = clamp01((stepInput.scatter ?? 0.3) + accumStress * 0.12);

    // Apply per-step regime bias if any
    if (mods.scatterBias) {
      stepInput.scatter = clamp01((stepInput.scatter ?? 0.3) + mods.scatterBias);
    }

    // Pass the incoming path memory (from prior accum state) so the core calculateOutcome can apply it
    // (history inertia now modulates coherence/identity/gate in the single-step view, closing the loop like durability).
    const incomingMemory = clamp01(accumContinuity * (1 - accumStress));
    const out = calculateOutcome(stepInput, { skipDurability: true, pathMemory: incomingMemory });

    // Compute durability for feedback/accumulator scaling independently (cheap short-horizon stability run).
    // This ensures dur-scaled carry and stress decay are active even though the per-step outcome itself uses skipDurability to avoid recursion.
    let durForAccum = 0;
    try {
      const d = computeRegimeStability({ ...stepInput }, { maxSteps: 2, regimeMemory: (options.regimeMemory ?? 0) });
      durForAccum = d.durabilityIndex || 0;
    } catch (_) {}
    // Also surface it on the step for traces/UI if not already present from a non-skip path.
    if (!out.metrics) out.metrics = {};
    if (!out.metrics.durabilityIndex) out.metrics.durabilityIndex = durForAccum;

    // Update accumulators from this step's grammar outcome.
    // Deeper closed feedback (pure logic): durability (long-term resistance to condition variation) now directly
    // modulates the carry fraction of prior continuity into the next route, and the decay rate of accumulated stress.
    // High durability retains more "memory of past coherence" (higher carry) and sheds history stress faster (lower retain on old accumStress).
    const dur = durForAccum;
    const carryFactorBase = clamp01(0.22 + 0.18 * dur);
    // PathQuality (running success quality) now explicitly scales carry and stress decay on top of dur+mem:
    // high pathQuality retains even more prior continuity (virtuous cycle stronger) and sheds accumStress faster.
    const currentPathQForScale = clamp01(0.55 * pathQuality + 0.45 * (incomingMemory || 0));
    const carryFactor = clamp01(carryFactorBase + 0.12 * currentPathQForScale);
    // Memory now directly scales the accumulator carry fraction and stress decay (deeper inertia/persistence from built memory):
    // high memoryMod (inertia) retains more of the prior continuity carry (stronger persistence of good coherence state) and
    // accelerates shedding of accumStress (faster recovery). This makes successful history build "stickier" accumulators for future steps.
    const memForAccum = incomingMemory;
    accumContinuity = clamp01(out.grammar.continuity * (1 - carryFactor) + accumContinuity * carryFactor * (1 + 0.12 * memForAccum));

    // Durability-scaled stress decay: higher durability lowers the retained weight on prior accumStress (faster relaxation of disturbance history).
    // Further eased by pathQuality (good sustained quality histories recover disturbance history faster).
    const stressRetainBase = clamp01(0.62 * (1 - 0.28 * dur) * (1 - 0.1 * memForAccum));
    const stressRetain = clamp01(stressRetainBase * (1 - 0.18 * currentPathQForScale));
    accumStress = clamp01(accumStress * stressRetain + out.closureStress * (1 - stressRetain) * 0.38);

    // Post-update path memory (for this step's "after" state and for the next step's feed-forward).
    // memoryMod = how much coherent persistence remains vs accumulated disturbance. High values mean the history has built "inertia".
    const memoryMod = clamp01(accumContinuity * (1 - accumStress));

    // Memory as rescuer in history traces (pure logic): high ending inertia can "carry" identity across a marginal step for the purpose of the overall history's preservation success.
    // This models built-up structure helping the closed order survive even if one encounter is borderline.
    // PathQuality now modulates the rescuer threshold: high sustained quality lowers the inertia needed to rescue a marginal step (virtuous histories are more forgiving).
    let tracePreserved = out.identityPreserved;
    let memoryRescued = false;
    const rescuerThresh = clamp01(0.55 - 0.12 * currentPathQForScale);  // lower bar when pathQuality high
    if (!tracePreserved && memoryMod > rescuerThresh) {
      tracePreserved = out.identityScore >= 0.58 && out.closureStress < 0.65;
      memoryRescued = true;
    }

    const durForStep = (out.metrics && out.metrics.durabilityIndex) ? out.metrics.durabilityIndex : 0;
    const durAdjustedId = out.metrics ? out.metrics.modulatedIdentity : out.identityScore;

    // step pathQuality: blend of this step's preservation success, its durability, and the inertia just built. Feeds the running accumulator.
    const stepPathQuality = clamp01((tracePreserved ? 0.92 : 0.62) * (0.55 + 0.45 * durForAccum) * (0.65 + 0.35 * memoryMod));

    const stepOutcome = {
      ...out,
      step,
      regime: stepRegime,
      accumContinuity: Number(accumContinuity.toFixed(4)),
      accumStress: Number(accumStress.toFixed(4)),
      durabilityAdjustedIdentityScore: durAdjustedId,
      carryFactor: Number(carryFactor.toFixed(4)),
      stressRetain: Number(stressRetain.toFixed(4)),
      memoryMod: Number(memoryMod.toFixed(4)),
      pathQuality: Number(stepPathQuality.toFixed(4)),
      identityPreserved: tracePreserved,
      memoryRescued,
    };
    trace.push(stepOutcome);

    // Blend this step's quality into the running pathQuality accumulator (closed loop for next steps' carry/decay/rescue/policy).
    pathQuality = clamp01(0.62 * pathQuality + 0.38 * stepPathQuality);

    // Mild consumption / relaxation for next step — modulated by the (possibly memory-blended) regime of *this* step
    let fatigue = mods.fatigueBase * mods.fatigueFactor * (1 - (out.grammar.continuity + out.reseatMetric) / 2);

    // Incorporate Durability Index / pathQuality feedback into consumption (closed-loop pure logic):
    // high durability (or high pathQuality from recent reinf) reduces fatigue impact and improves carry for next steps.
    // This creates self-reinforcing coherent paths: successful long-term durability makes future steps easier (virtuous cycle).
    if (out.metrics && out.metrics.durabilityIndex) {
      const d = out.metrics.durabilityIndex;
      fatigue *= (1 - d * 0.2);  // high dur reduces effective fatigue
      // Also scale the reinf/debt bonus/penalty by dur for stronger effect in high-dur configs
    }

    // Memory amplification of virtuous cycle (pure logic extension): built path memory (inertia from prior coherent steps) now directly eases consumption/fatigue and amplifies reinforcement for the next step.
    // High memoryMod makes maintaining coherence "cheaper" (less fatigue drift) and strengthens the carry boost after preserved steps.
    const mem = memoryMod;  // post-update for this step
    fatigue *= (1 - mem * 0.15);  // high inertia reduces effective fatigue beyond dur

    current = {
      ...current,
      storage: clamp01((current.storage ?? 0.4) * (mods.storageDecay + out.reseatMetric * 0.03 + mods.reseatBoost)),
      scatter: clamp01((current.scatter ?? 0.3) * 0.96 + fatigue),
    };

    // Coherence reinforcement / path dependence (pure logic): after a preserved step under adaptive policy (good choice + commitment), slightly boost future carry / reduce future fatigue (self-reinforcing coherent paths under good condition choices). Scaled by dur for stronger effect in high-dur configs.
    // Further amplified by memoryMod: high inertia makes the reinforcement from a good preserved step stronger.
    if (adaptivePolicy && out.identityPreserved) {
      const reinfScale = 0.03 * durForAccum * (1 + 0.5 * mem);
      accumContinuity = clamp01(accumContinuity * (1 + reinfScale));
    }

    // Coherence debt (symmetric negative feedback): after a non-preserved step under adaptive policy (poor choice or bad outcome), slightly reduce future carry / increase future fatigue impact (degrading paths under poor condition choices; vicious cycle contrast to reinforcement). Scaled by dur.
    if (adaptivePolicy && !out.identityPreserved) {
      const debtScale = 0.03 * durForAccum * (1 + 0.5 * mem);
      accumContinuity = clamp01(accumContinuity * (1 - debtScale));
    }

    prevRegime = stepRegime;
  }

  const last = trace[trace.length - 1];
  const avgMem = trace.reduce((s, t) => s + (t.memoryMod || 0), 0) / trace.length;
  const avgPathQ = trace.length ? (trace.reduce((s, t) => s + (t.pathQuality || 0.5), 0) / trace.length) : 0.5;
  const finalPathQ = trace.length ? (trace[trace.length-1].pathQuality || 0.5) : 0.5;

  // memoryAdjustedFinalIdentity: the final identityScore is boosted by cumulative memory (inertia makes the ending "preserved quality" stronger, not just the binary).
  const memoryAdjustedFinalIdentity = Number((last.identityScore * (1 + avgMem * 0.1)).toFixed(4));

  // memoryCarriedFinalIdentity: when the trace is memory-carried preserved, the carried quality is the memory-adjusted final identity (cumulative inertia carries not just the binary but the strength of the ending state).
  let finalPreserved = !!last.identityPreserved;
  let memoryCarriedPreserved = false;
  // Dynamic quality gate for carried preservation: high avgPathQuality lowers the required carried identity quality (virtuous sustained histories forgive a weaker final snapshot).
  const carriedQualityGate = clamp01(0.58 - 0.07 * avgPathQ);
  const memoryCarriedFinalIdentity = memoryCarriedPreserved ? memoryAdjustedFinalIdentity : last.identityScore;  // pre-assign for the if (will rebind if carried triggers)
  if (!finalPreserved && memoryCarriedFinalIdentity > 0.62) {
    // cumulative memory inertia across the history can rescue the overall preservation (built coherence "carries" the identity even if the last step is marginal)
    // now a smooth function of the memoryCarriedFinalIdentity (accumulated grammar state)
    finalPreserved = true;
    memoryCarriedPreserved = true;
  }
  // Recompute carried final id if the carried trigger fired above (order-safe)
  const finalMemoryCarriedIdentity = memoryCarriedPreserved ? memoryAdjustedFinalIdentity : last.identityScore;
  const minCoherence = Math.min(...trace.map((t) => t.coherenceMetric));
  const avgCoherence = trace.reduce((s, t) => s + t.coherenceMetric, 0) / trace.length;
  // memoryWeightedCoherence: the trace coherence now explicitly includes the memory modulation of grammarAlignment/coherenceMetric from core.
  const memoryWeightedCoherence = trace.reduce((s, t) => s + t.coherenceMetric * (1 + (t.memoryMod || 0) * 0.05), 0) / trace.length;

  return {
    trace,
    finalPreserved,
    summary: {
      steps: trace.length,
      finalIdentity: Number(last.identityScore.toFixed(4)),
      finalStress: Number(last.closureStress.toFixed(4)),
      finalPreserved,
      minCoherence: Number(minCoherence.toFixed(4)),
      avgCoherence: Number(avgCoherence.toFixed(4)),
      startCoherence: Number(trace[0].coherenceMetric.toFixed(4)),
      avgMemoryMod: Number(avgMem.toFixed(4)),
      memoryWeightedCoherence: Number(memoryWeightedCoherence.toFixed(4)),
      memoryAdjustedFinalIdentity,
      memoryCarriedPreserved,
      memoryCarriedFinalIdentity: finalMemoryCarriedIdentity,
      memoryCarriedFinalPreserved: memoryCarriedPreserved && finalMemoryCarriedIdentity > carriedQualityGate,
      avgPathQuality: Number(avgPathQ.toFixed(4)),
      finalPathQuality: Number(finalPathQ.toFixed(4)),
      memoryCarriedFinalPresQualityGate: Number(carriedQualityGate.toFixed(4)),
    },
  };
}

/**
 * measureResilience (continuation of the pure-logic advance)
 * Uses repeated simulateSequence-style steps (or direct calculateOutcome with state evolution)
 * to answer: "Under this configuration (and optional persistent load), how many steps
 * can the closed order survive before identityPreserved becomes false?"
 *
 * This is the natural next question after single snapshots and fixed-length traces.
 * Returns the count of coherent steps survived, the step at which it failed (if any),
 * plus a compact history and summary.
 *
 * Regime support (v0.4 durability exploration):
 * - 'nominal': baseline mild consumption (default, backward compatible)
 * - 'stressed': harsher fatigue + initial scatter bias (models adverse environment)
 * - 'recovering': gentler consumption + reseat boost after early stress (models healing/settling)
 *
 * You can still pass custom loadProfile for fine control.
 */
export function measureResilience(baseInput = {}, options = {}) {
  const maxSteps = options.maxSteps ?? 12;
  const loadProfile = options.loadProfile ?? {};
  const regime = options.regime ?? 'nominal';

  // Regime modulators (pure abstract rules — harsher or gentler "world" for the repeated meetings)
  let fatigueBase = 0.03;
  let fatigueFactor = 1.0;
  let storageDecay = 0.94;
  let scatterBias = 0.0;
  let reseatBoost = 0.0;

  if (regime === 'stressed') {
    fatigueFactor = 1.6;
    scatterBias = 0.08;
    storageDecay = 0.90;
  } else if (regime === 'recovering') {
    fatigueFactor = 0.6;
    reseatBoost = 0.04;
    storageDecay = 0.96;
  }

  let current = { ...baseInput };
  const history = [];
  let survived = 0;

  for (let step = 0; step < maxSteps; step += 1) {
    const stepInput = { ...current, ...loadProfile };
    // Apply regime bias to scatter for this step
    if (scatterBias) {
      stepInput.scatter = clamp01((stepInput.scatter ?? 0.3) + scatterBias);
    }
    const out = calculateOutcome(stepInput, { skipDurability: true });

    // Compute step memory from current out (grammar + low stress = high inertia)
    const stepMem = out.grammar ? clamp01(out.grammar.continuity * (1 - out.closureStress)) : 0;

    const entry = {
      step,
      coherenceMetric: out.coherenceMetric,
      identityScore: out.identityScore,
      closureStress: out.closureStress,
      identityPreserved: out.identityPreserved,
      grammar: out.grammar,
      regime,
    };
    history.push(entry);

    if (!out.identityPreserved) {
      break;
    }
    survived = step + 1;

    // Consumption modulated by regime + memory (pure logic: high inertia from current grammar makes repeated encounters cheaper to survive, extending the horizon)
    let fatigue = fatigueBase * fatigueFactor * (1 - (out.grammar.continuity + out.reseatMetric) / 2);
    fatigue *= (1 - stepMem * 0.15);  // memory eases fatigue
    const memStorageDecay = storageDecay * (1 + stepMem * 0.05);  // high memory makes storage decay gentler
    current = {
      ...current,
      storage: clamp01((current.storage ?? 0.4) * (memStorageDecay + out.reseatMetric * 0.03 + reseatBoost)),
      scatter: clamp01((current.scatter ?? 0.3) * 0.97 + fatigue),
    };
  }

  const last = history[history.length - 1];
  return {
    survivedSteps: survived,
    failedAtStep: last.identityPreserved ? null : last.step,
    finalPreserved: last.identityPreserved,
    regime,
    history: history.map((h) => ({
      step: h.step,
      coh: Number(h.coherenceMetric.toFixed(3)),
      id: Number(h.identityScore.toFixed(3)),
      stress: Number(h.closureStress.toFixed(3)),
      preserved: h.identityPreserved,
    })),
    summary: {
      maxTested: maxSteps,
      survived,
      failedAt: last.identityPreserved ? null : last.step,
      finalCoherence: Number(last.coherenceMetric.toFixed(4)),
      finalIdentity: Number(last.identityScore.toFixed(4)),
      finalStress: Number(last.closureStress.toFixed(4)),
      regime,
    },
  };
}

/**
 * computeCrossRegimeDurability (new pure-logic primitive for "condition-independent" coherence)
 * Runs measureResilience under all three regimes for the same baseInput.
 * Returns a robustness summary that captures how well the grammar alignment holds up
 * when the "world" (fatigue/consumption) changes.
 *
 * This is the natural next abstraction after single-regime resilience:
 * "Does this coherent state survive repeated meetings *regardless of condition*?"
 *
 * Metrics:
 * - survivals: per-regime survived steps (out of maxSteps)
 * - minSurvival: worst-case (most conservative durability)
 * - dropStressed: how much harsher conditions hurt (nominal - stressed)
 * - robustness: simple score minSurvival / maxSteps (0-1). 1.0 = fully robust across regimes.
 * - fullRobust: true only if full horizon in all three regimes.
 */
export function computeCrossRegimeDurability(baseInput = {}, options = {}) {
  const maxSteps = options.maxSteps ?? 8;
  const regimes = ['nominal', 'stressed', 'recovering'];

  const results = {};
  regimes.forEach((reg) => {
    const res = measureResilience(baseInput, { maxSteps, regime: reg });
    results[reg] = {
      survived: res.survivedSteps,
      finalPreserved: res.finalPreserved,
      finalIdentity: res.summary.finalIdentity,
    };
  });

  const survivals = {
    nominal: results.nominal.survived,
    stressed: results.stressed.survived,
    recovering: results.recovering.survived,
  };

  const minSurvival = Math.min(...Object.values(survivals));
  const maxSurvival = Math.max(...Object.values(survivals));
  const dropStressed = survivals.nominal - survivals.stressed;
  const robustness = Number((minSurvival / maxSteps).toFixed(4));
  const fullRobust = Object.values(survivals).every((s) => s >= maxSteps);

  return {
    survivals,
    minSurvival,
    maxSurvival,
    dropStressed,
    robustness,
    fullRobust,
    details: results,
  };
}

/**
 * getRegimeModulators (internal helper)
 * Returns the consumption/fatigue parameters for a given regime.
 * Extracted so both single-regime and per-step transition logic can share the rules.
 */
function getRegimeModulators(regime = 'nominal') {
  let fatigueBase = 0.03;
  let fatigueFactor = 1.0;
  let storageDecay = 0.94;
  let scatterBias = 0.0;
  let reseatBoost = 0.0;

  if (regime === 'stressed') {
    fatigueFactor = 1.6;
    scatterBias = 0.08;
    storageDecay = 0.90;
  } else if (regime === 'recovering') {
    fatigueFactor = 0.6;
    reseatBoost = 0.04;
    storageDecay = 0.96;
  }

  return { fatigueBase, fatigueFactor, storageDecay, scatterBias, reseatBoost };
}

/**
 * testRegimeTransition (new primitive for varying conditions)
 * Runs a short history through an explicit sequence of regimes (e.g. a "stress spike" then recovery).
 * This directly tests the pure-logic question: "How much does a temporary worsening of conditions
 * (or a recovery phase) cost the closed form in terms of identity survival?"
 *
 * Default transition: nominal (2 steps) -> stressed (2 steps) -> recovering (remaining).
 * Returns the trace (now with per-step .regime) + survival through the transition + summary.
 */
export function testRegimeTransition(baseInput = {}, options = {}) {
  const maxSteps = options.maxSteps ?? 8;
  const schedule = options.regimeSchedule || ['nominal', 'nominal', 'stressed', 'stressed', 'recovering', 'recovering', 'recovering', 'recovering'].slice(0, maxSteps);
  const regimeMemory = options.regimeMemory ?? 0;
  const adaptivePolicy = options.adaptivePolicy || false;
  const regimeSwitchingCost = options.regimeSwitchingCost ?? 0;

  // Delegate to the now transition-aware simulateSequence
  const res = simulateSequence(baseInput, maxSteps, { regimeSchedule: schedule, regimeMemory, adaptivePolicy, regimeSwitchingCost });

  // Compute transition-specific summary
  const stressedSteps = schedule.filter(r => r === 'stressed').length;
  const survivedStressedPhase = res.trace.filter((t, i) => schedule[i] === 'stressed' && t.identityPreserved).length;

  return {
    ...res,
    transitionSchedule: schedule,
    transitionSummary: {
      stressedStepsInSchedule: stressedSteps,
      survivedThroughStressed: survivedStressedPhase,
      fullTransitionPreserved: res.finalPreserved,
    },
  };
}

/**
 * REGIME_TRANSITION_PROFILES
 * A small library of interesting regime sequences for pure-logic exploration of durability
 * under time-varying conditions. These are abstract "stories" the interaction can live through.
 */
export const REGIME_TRANSITION_PROFILES = {
  'stress-spike': ['nominal', 'nominal', 'stressed', 'stressed', 'recovering', 'recovering', 'recovering', 'recovering'],
  'oscillation': ['nominal', 'stressed', 'nominal', 'stressed', 'recovering', 'stressed', 'recovering', 'nominal'],
  'gradual-degradation': ['nominal', 'nominal', 'stressed', 'stressed', 'stressed', 'stressed', 'recovering', 'recovering'],
  'prolonged-stress': ['nominal', 'stressed', 'stressed', 'stressed', 'stressed', 'recovering', 'recovering', 'recovering'],
};

/**
 * computeTransitionFragility
 * Runs a nominal (all 'nominal') history and a transition schedule, then quantifies the
 * "damage" the regime changes inflict on survival/identity preservation.
 *
 * fragility = (nominalSurvival - transitionSurvival) / maxSteps   (positive = the changes hurt)
 * This gives a simple, comparable measure of how sensitive a configuration is to particular
 * patterns of environmental change.
 *
 * Returns structured result with survivals, fragility, and whether final identity held in each case.
 */
export function computeTransitionFragility(baseInput = {}, options = {}) {
  const maxSteps = options.maxSteps ?? 8;
  const profileName = options.profile || 'stress-spike';
  const schedule = REGIME_TRANSITION_PROFILES[profileName] || options.regimeSchedule || REGIME_TRANSITION_PROFILES['stress-spike'];

  // Pure nominal run for baseline
  const nominalRun = simulateSequence(baseInput, maxSteps);

  // Transition run
  const regimeMemory = options.regimeMemory ?? 0;
  const transRun = simulateSequence(baseInput, maxSteps, { regimeSchedule: schedule, regimeMemory });

  // Compute "survival" as steps until first identity failure (consistent with resilience style)
  function countSurvival(trace) {
    for (let i = 0; i < trace.length; i++) {
      if (!trace[i].identityPreserved) return i;
    }
    return maxSteps;
  }

  const nominalSurvival = countSurvival(nominalRun.trace);
  const transSurvival = countSurvival(transRun.trace);

  const fragility = Number( ((nominalSurvival - transSurvival) / maxSteps).toFixed(4) );

  return {
    profile: profileName,
    schedule,
    nominalSurvival,
    transitionSurvival: transSurvival,
    fragility,
    nominalFinalPreserved: nominalRun.finalPreserved,
    transitionFinalPreserved: transRun.finalPreserved,
  };
}

/**
 * computeRegimeStability
 * Composite view: how stable is the coherent identity when exposed to the full library of
 * transition profiles? Returns per-profile fragilities + summary metrics.
 *
 * stability = 1 - maxFragility   (1.0 means zero damage on the worst profile)
 * This gives a single number for "condition-independent durability".
 */
export function computeRegimeStability(baseInput = {}, options = {}) {
  const maxSteps = options.maxSteps ?? 8;
  const regimeMemory = options.regimeMemory ?? 0;
  const profiles = Object.keys(REGIME_TRANSITION_PROFILES);

  const fragilities = {};
  let maxFrag = 0;
  let sumFrag = 0;

  profiles.forEach((p) => {
    const f = computeTransitionFragility(baseInput, { maxSteps, profile: p, regimeMemory });
    fragilities[p] = f.fragility;
    if (f.fragility > maxFrag) maxFrag = f.fragility;
    sumFrag += f.fragility;
  });

  const avgFrag = Number((sumFrag / profiles.length).toFixed(4));
  const stability = Number((1 - maxFrag).toFixed(4));

  // Durability Index: single composite 0-1 for overall long-term coherence under varying conditions.
  // Combines cross-regime robustness, stability, and low average fragility.
  const cross = computeCrossRegimeDurability(baseInput, { maxSteps });
  const durabilityIndex = Math.max(0, Math.min(1, cross.robustness * stability * (1 - avgFrag)));

  return {
    fragilities,
    maxFragility: Number(maxFrag.toFixed(4)),
    avgFragility: avgFrag,
    stability,
    fullStable: maxFrag === 0,
    regimeMemory,
    durabilityIndex: Number(durabilityIndex.toFixed(4)),
  };
}

/**
 * findHighStabilitySettings
 * Pure-logic explorer: starting from a baseInput, perform small random perturbations
 * on the grammar-relevant controls (boundary, route, reseat, phase, charge) and return
 * the locally best setting with higher regime stability (lower worst-case fragility).
 *
 * This advances the modelling from passive measurement of durability under conditions
 * to active search for more robust configurations inside the abstract grammar.
 *
 * Returns the best candidate, its stability, the delta from base, and improvement.
 */
export function findHighStabilitySettings(baseInput = {}, options = {}) {
  const maxSteps = options.maxSteps ?? 8;
  const samples = options.samples ?? 25;
  const stepSize = options.stepSize ?? 0.06;
  const regimeMemory = options.regimeMemory ?? 0;

  const grammarKeys = ['boundary', 'route', 'reseat', 'phase', 'charge'];

  const baseStability = computeRegimeStability(baseInput, { maxSteps }).stability;

  let best = {
    input: { ...baseInput },
    stability: baseStability,
    delta: {},
    improvement: 0,
  };

  for (let i = 0; i < samples; i++) {
    const candidate = { ...baseInput };
    const delta = {};

    grammarKeys.forEach((key) => {
      const current = candidate[key] ?? 0.5;
      const noise = (Math.random() - 0.5) * 2 * stepSize;
      const next = Math.max(0, Math.min(1, current + noise));
      if (next !== current) {
        candidate[key] = Number(next.toFixed(3));
        delta[key] = Number((next - current).toFixed(3));
      }
    });

    const stab = computeRegimeStability(candidate, { maxSteps, regimeMemory }).stability;
    if (stab > best.stability) {
      best = {
        input: candidate,
        stability: Number(stab.toFixed(4)),
        delta,
        improvement: Number((stab - baseStability).toFixed(4)),
      };
    }
  }

  const projectedDur = computeRegimeStability(best.input, { maxSteps, regimeMemory }).durabilityIndex;

  return {
    baseStability: Number(baseStability.toFixed(4)),
    bestStability: best.stability,
    improvement: best.improvement,
    delta: best.delta,
    suggestedInput: best.input,
    regimeMemory,
    projectedDurabilityIndex: projectedDur,
  };
}

/**
 * findBestRegimeForDurability
 * Pure-logic "policy": for a given config, try each possible fixed regime (constant schedule of nominal/stressed/recovering),
 * with optional memory, compute the effective durability under that "policy" (durabilityIndex modulated by whether the fixed regime preserves identity in the constant history).
 * Returns the best regime, its effective index, the cross durabilityIndex, and comparison.
 *
 * This allows "choosing the best condition (regime) to place the system in to maximize its long-term coherent durability under the model's rules".
 */
export function findBestRegimeForDurability(baseInput = {}, options = {}) {
  const maxSteps = options.maxSteps ?? 8;
  const regimeMemory = options.regimeMemory ?? 0;
  const regimes = ['nominal', 'stressed', 'recovering'];

  const cross = computeRegimeStability(baseInput, { maxSteps, regimeMemory });
  const baseDur = cross.durabilityIndex;

  let best = { regime: null, effectiveDurabilityIndex: -1, finalPreserved: false };
  const results = {};

  regimes.forEach(reg => {
    const constSchedule = Array(maxSteps).fill(reg);
    const trans = testRegimeTransition(baseInput, { maxSteps, regimeSchedule: constSchedule, regimeMemory });
    // Effective = cross dur * (1 if preserves in this fixed regime, else penalty)
    const regimeScore = trans.finalPreserved ? 1.0 : 0.6;
    const effective = Number((baseDur * regimeScore).toFixed(4));
    results[reg] = {
      effectiveDurabilityIndex: effective,
      finalPreserved: trans.finalPreserved,
      averageIdentity: trans.summary ? trans.summary.finalIdentity : null, // approx
    };
    if (effective > best.effectiveDurabilityIndex) {
      best = { regime: reg, effectiveDurabilityIndex: effective, finalPreserved: trans.finalPreserved };
    }
  });

  return {
    crossDurabilityIndex: baseDur,
    bestRegime: best.regime,
    bestEffectiveDurabilityIndex: best.effectiveDurabilityIndex,
    results,
    regimeMemory,
    improvementOverWorst: Number((best.effectiveDurabilityIndex - Math.min(...Object.values(results).map(r => r.effectiveDurabilityIndex))).toFixed(4)),
  };
}

/**
 * computeMonteCarloDurability
 * Pure-logic probabilistic view: run many random transition sequences (sampled from the REGIME_TRANSITION_PROFILES
 * or random regime steps) and average the outcomes to estimate "expected" durability under unpredictable condition changes.
 *
 * This complements the 'best policy' (optimistic fixed regime) with average-case over stochastic histories.
 * Returns expected finalPres rate (key MC durability measure), avg identity, and optionally per-trial details.
 */
export function computeMonteCarloDurability(baseInput = {}, options = {}) {
  const maxSteps = options.maxSteps ?? 8;
  const numTrials = options.numTrials ?? 50;
  const regimeMemory = options.regimeMemory ?? 0;
  const useProfiles = options.useProfiles !== false; // default true: sample from profiles
  const includeTrials = options.includeTrials || false;

  const profNames = Object.keys(REGIME_TRANSITION_PROFILES);
  const regimes = ['nominal', 'stressed', 'recovering'];

  let totalFinalPres = 0;
  let totalFinalId = 0;
  const trials = [];

  for (let t = 0; t < numTrials; t++) {
    let schedule;
    if (useProfiles) {
      const chosen = profNames[Math.floor(Math.random() * profNames.length)];
      schedule = REGIME_TRANSITION_PROFILES[chosen].slice(0, maxSteps);
    } else {
      schedule = Array.from({length: maxSteps}, () => regimes[Math.floor(Math.random() * regimes.length)]);
    }

    const trans = testRegimeTransition(baseInput, { maxSteps, regimeSchedule: schedule, regimeMemory });

    totalFinalPres += trans.finalPreserved ? 1 : 0;
    totalFinalId += trans.summary.finalIdentity || 0;

    if (includeTrials) {
      trials.push({
        schedule,
        finalPreserved: trans.finalPreserved,
        finalIdentity: trans.summary.finalIdentity,
      });
    }
  }

  return {
    expectedFinalPresRate: Number((totalFinalPres / numTrials).toFixed(4)),
    avgFinalIdentity: Number((totalFinalId / numTrials).toFixed(4)),
    numTrials,
    useProfiles,
    regimeMemory,
    trials: includeTrials ? trials : undefined,
  };
}
