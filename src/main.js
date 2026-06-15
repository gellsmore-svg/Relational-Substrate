import './styles.css';
import * as THREE from 'three';
import { calculateOutcome, scenarioPresets, simulateSequence, measureResilience, computeCrossRegimeDurability, testRegimeTransition, REGIME_TRANSITION_PROFILES, computeTransitionFragility, computeRegimeStability, findHighStabilitySettings, findBestRegimeForDurability, computeMonteCarloDurability } from './model.js';

const canvas = document.querySelector('#scene');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xf7f6ef);
scene.fog = new THREE.Fog(0xf7f6ef, 12, 36);

const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
camera.position.set(0, 4.2, 10);

const group = new THREE.Group();
scene.add(group);

const lights = [
  new THREE.AmbientLight(0xffffff, 1.1),
  new THREE.DirectionalLight(0xffffff, 1.25),
  new THREE.PointLight(0xffffff, 1.2, 18),
];
lights[1].position.set(4, 7, 5);
lights[2].position.set(-3, 2, 4);
lights.forEach((light) => scene.add(light));

const grid = new THREE.GridHelper(12, 24, 0xbcb7aa, 0xd7d2c4);
grid.position.y = -2.2;
scene.add(grid);

const materials = {
  closed: new THREE.MeshStandardMaterial({
    color: 0x1e6f66,
    emissive: 0x0b211f,
    metalness: 0.12,
    roughness: 0.32,
  }),
  transient: new THREE.MeshStandardMaterial({
    color: 0xb18400,
    emissive: 0x2d2100,
    metalness: 0.05,
    roughness: 0.22,
  }),
  returned: new THREE.MeshStandardMaterial({
    color: 0x9a5f00,
    emissive: 0x291900,
    roughness: 0.28,
  }),
  stored: new THREE.MeshStandardMaterial({
    color: 0x5469a6,
    emissive: 0x111734,
    roughness: 0.28,
    transparent: true,
    opacity: 0.74,
  }),
  scatter: new THREE.MeshStandardMaterial({
    color: 0xa13e51,
    emissive: 0x2d0d14,
    roughness: 0.35,
  }),
  stress: new THREE.MeshStandardMaterial({
    color: 0x263238,
    emissive: 0x111111,
    roughness: 0.45,
    transparent: true,
    opacity: 0.22,
  }),
};

const state = {
  scenario: 'admit',
  closedForm: 'trefoil',
  transientForm: 'straight',
  boundary: 0.82,
  route: 0.78,
  storage: 0.18,
  scatter: 0.12,
  reseat: 0.7,
  phase: 0.5,
  charge: 0.0,
  regime: 'nominal',
};

const els = {
  outcome: document.querySelector('#outcome-name'),
  identity: document.querySelector('#identity-state'),
  stress: document.querySelector('#stress-state'),
  reading: document.querySelector('#reading'),
  closedForm: document.querySelector('#closed-form'),
  transientForm: document.querySelector('#transient-form'),
  boundary: document.querySelector('#boundary'),
  route: document.querySelector('#route'),
  storage: document.querySelector('#storage'),
  scatter: document.querySelector('#scatter'),
  reseat: document.querySelector('#reseat'),
  phase: document.querySelector('#phase'),
  charge: document.querySelector('#charge'),
  regime: document.querySelector('#regime'),
  exportButton: document.querySelector('#export-case'),
  exportOutput: document.querySelector('#export-output'),
  runTraceButton: document.querySelector('#run-trace'),
  suggestStableButton: document.querySelector('#suggest-stable'),
  traceOutput: document.querySelector('#trace-output'),
  grammarHealth: document.querySelector('#grammar-health'),
  resilienceHorizon: document.querySelector('#resilience-horizon'),
  resilienceNote: document.querySelector('#resilience-note'),
  robustnessScore: document.querySelector('#robustness-score'),
  robustnessNote: document.querySelector('#robustness-note'),
  stabilityScore: document.querySelector('#stability-score'),
  stabilityNote: document.querySelector('#stability-note'),
  durabilityIndex: document.querySelector('#durability-index'),
  durabilityNote: document.querySelector('#durability-note'),
};

const outputs = {
  boundary: document.querySelector('#boundary-value'),
  route: document.querySelector('#route-value'),
  storage: document.querySelector('#storage-value'),
  scatter: document.querySelector('#scatter-value'),
  reseat: document.querySelector('#reseat-value'),
  phase: document.querySelector('#phase-value'),
  charge: document.querySelector('#charge-value'),
  admitted: document.querySelector('#admitted-value'),
  returned: document.querySelector('#returned-value'),
  stored: document.querySelector('#stored-value'),
  scattered: document.querySelector('#scattered-value'),
  admittedBar: document.querySelector('#admitted-bar'),
  returnedBar: document.querySelector('#returned-bar'),
  storedBar: document.querySelector('#stored-bar'),
  scatteredBar: document.querySelector('#scattered-bar'),
  metrics: {
    closure: document.querySelector('#metric-closure'),
    return: document.querySelector('#metric-return'),
    bounded: document.querySelector('#metric-bounded'),
    coherence: document.querySelector('#metric-coherence'),
    reseat: document.querySelector('#metric-reseat'),
    leakage: document.querySelector('#metric-leakage'),
    identity: document.querySelector('#identity-score'),
  },
};

function makeTube(points, radius, material, tubularSegments = 180) {
  const curve = new THREE.CatmullRomCurve3(points, false, 'catmullrom', 0.45);
  const geometry = new THREE.TubeGeometry(curve, tubularSegments, radius, 12, false);
  return new THREE.Mesh(geometry, material);
}

function torusKnotGeometry(type) {
  if (type === 'circle') {
    return new THREE.TorusGeometry(2, 0.085, 18, 160);
  }
  if (type === 'double') {
    const outer = new THREE.Group();
    const left = new THREE.Mesh(new THREE.TorusGeometry(1.25, 0.075, 16, 110), materials.closed);
    const right = new THREE.Mesh(new THREE.TorusGeometry(1.25, 0.075, 16, 110), materials.closed);
    left.position.x = -1;
    right.position.x = 1;
    right.rotation.y = Math.PI / 2.7;
    outer.add(left, right);
    return outer;
  }
  return new THREE.TorusKnotGeometry(1.55, 0.075, 220, 18, 2, 3);
}

function makeTransientPath(kind, scenario, phase = 0.5) {
  const phaseShift = (phase - 0.5) * Math.PI * 1.6; // map 0-1 phase to a useful shift

  if (scenario === 'return') {
    return [
      new THREE.Vector3(-5.4, 0, 0),
      new THREE.Vector3(-2.1, 0.06, 0),
      new THREE.Vector3(-3.35, 1.05, 0.25),
      new THREE.Vector3(-5.1, 1.35, 0.5),
    ];
  }

  if (kind === 'sine') {
    return Array.from({ length: 44 }, (_, i) => {
      const t = i / 43;
      const x = -5.4 + t * 10.8;
      const y = Math.sin(t * Math.PI * 5.5 + phaseShift) * 0.28;
      const z = Math.cos(t * Math.PI * 4 + phaseShift * 0.6) * 0.18;
      return new THREE.Vector3(x, y, z);
    });
  }

  if (kind === 'ribbon') {
    return [
      new THREE.Vector3(-5.4, -0.25, -0.2),
      new THREE.Vector3(-2.4, 0.12, 0.35),
      new THREE.Vector3(0, 0.3, -0.15),
      new THREE.Vector3(2.4, 0.12, 0.35),
      new THREE.Vector3(5.4, -0.25, -0.2),
    ].map((p, i) => {
      // small phase-driven twist on the ribbon
      const twist = Math.sin(i * 0.8 + phaseShift) * 0.12 * (phase - 0.5);
      return new THREE.Vector3(p.x, p.y + twist, p.z);
    });
  }

  if (scenario === 'store') {
    return [
      new THREE.Vector3(-5.4, 0, 0),
      new THREE.Vector3(-2.2, 0.04, 0),
      new THREE.Vector3(-0.4, 0.22, 0.2),
      new THREE.Vector3(1.2, -0.05, -0.2),
      new THREE.Vector3(3.4, -0.24, 0.1),
    ];
  }

  return [
    new THREE.Vector3(-5.4, 0, 0),
    new THREE.Vector3(-2.5, 0.03, 0),
    new THREE.Vector3(0, 0.12, 0.18),
    new THREE.Vector3(2.5, 0.03, 0),
    new THREE.Vector3(5.4, 0, 0),
  ];
}

function addRouteSplit(outcome) {
  const base = new THREE.Vector3(-0.15, 0.05, 0);
  const admittedEnd = new THREE.Vector3(2.7 + outcome.admitted * 2, 0.12, 0.1);
  const returnedEnd = new THREE.Vector3(-2.4 - outcome.returned * 2, 1.0, 0.45);
  const storedEnd = new THREE.Vector3(0.1, -0.85 - outcome.stored * 0.65, 0.15);

  if (outcome.admitted > 0.18) {
    group.add(makeTube([base, new THREE.Vector3(1.1, 0.22, 0.16), admittedEnd], 0.024, materials.transient, 42));
  }

  if (outcome.returned > 0.16) {
    group.add(makeTube([base, new THREE.Vector3(-1.2, 0.5, 0.25), returnedEnd], 0.024, materials.returned, 42));
  }

  if (outcome.stored > 0.16) {
    group.add(makeTube([base, new THREE.Vector3(0, -0.35, 0.08), storedEnd], 0.022, materials.stored, 32));
  }
}

function addScatter() {
  const count = Math.round(4 + state.scatter * 10);
  for (let i = 0; i < count; i += 1) {
    const angle = (i / count) * Math.PI * 2;
    const start = new THREE.Vector3(0.35, 0.05, 0);
    const end = new THREE.Vector3(
      Math.cos(angle) * (1.4 + state.scatter),
      Math.sin(angle * 1.7) * 0.85,
      Math.sin(angle) * (1.4 + state.scatter)
    );
    const ray = makeTube([start, end], 0.018, materials.scatter, 20);
    group.add(ray);
  }
}

function addStoredGlow() {
  const geometry = new THREE.SphereGeometry(0.62 + state.storage * 0.5, 32, 18);
  const mesh = new THREE.Mesh(geometry, materials.stored);
  mesh.scale.set(1.25, 0.7, 1.25);
  group.add(mesh);
}

function addStressShell(outcome) {
  const geometry = new THREE.TorusGeometry(2.18 + outcome.closureStress * 0.34, 0.018, 8, 160);
  const shell = new THREE.Mesh(geometry, materials.stress);
  shell.rotation.x = Math.PI / 2.5;
  group.add(shell);
}

function setMeter(name, value) {
  const percent = Math.round(value * 100);
  outputs[`${name}Bar`].style.width = `${percent}%`;
  outputs[name].textContent = `${percent}%`;
}

function updateReadout(outcome) {
  setMeter('admitted', outcome.admitted);
  setMeter('returned', outcome.returned);
  setMeter('stored', outcome.stored);
  setMeter('scattered', outcome.scattered);

  const dominant = [
    ['Admitted', outcome.admitted],
    ['Returned', outcome.returned],
    ['Stored', outcome.stored],
    ['Scattered', outcome.scattered],
  ].sort((a, b) => b[1] - a[1])[0][0];

  els.outcome.textContent = dominant;
  els.identity.textContent = outcome.identityPreserved ? 'Preserved' : 'At Risk';
  els.stress.textContent = outcome.closureStress < 0.28 ? 'Low' : outcome.closureStress < 0.52 ? 'Moderate' : 'High';

  Object.entries(outcome.metrics).forEach(([key, value]) => {
    if (outputs.metrics[key]) outputs.metrics[key].textContent = value.toFixed(2);
  });

  // Show grammar factors if available (the five elements: route, closure, phase, charge, continuity)
  if (outcome.grammar) {
    const g = outcome.grammar;
    // We can repurpose some metric outputs or just log; for now extend the reading
    const grammarLine = ` | cont:${g.continuity.toFixed(2)} phaseM:${g.phaseMatch.toFixed(2)} chT:${g.chargeTension.toFixed(2)}`;
    // append to reading later
    window._lastGrammar = grammarLine; // tiny hack for the reading
  }

  const readings = {
    Admitted: 'The transient is admitted with coherent delay. The closed form flexes within tolerance and returns.',
    Returned: 'Boundary compatibility is poor inward but strong enough to return the transient coherently.',
    Stored: 'Part of the transient becomes local stress or lock-up. This is not vorton generation unless invariant closure persists.',
    Scattered: 'Route compatibility is uneven. The open transient fragments into multiple weaker outcomes.',
  };
  const gate = outcome.identityPreserved
    ? 'The closure gate remains above threshold.'
    : 'The closure gate falls below threshold: identity is at risk.';
  let text = `${readings[dominant]} ${gate}`;
  if (window._lastGrammar) text += window._lastGrammar;
  els.reading.textContent = text;

  // Expose grammar factors in dedicated outputs if present in the DOM
  if (outcome.grammar) {
    const g = outcome.grammar;
    const contEl = document.getElementById('grammar-continuity');
    const pmEl = document.getElementById('grammar-phaseMatch');
    const ctEl = document.getElementById('grammar-chargeTension');
    if (contEl) contEl.textContent = g.continuity.toFixed(2);
    if (pmEl) pmEl.textContent = g.phaseMatch.toFixed(2);
    if (ctEl) ctEl.textContent = g.chargeTension.toFixed(2);

    // Grammar health composite (simple average of the three core normalized grammar signals)
    const health = (g.continuity + g.phaseMatch + (1 - g.chargeTension)) / 3;
    if (els.grammarHealth) els.grammarHealth.textContent = health.toFixed(2);
  }
}

function updateResilience() {
  // Live 8-step durability horizon using the current full state (forms + sliders + selected regime)
  const input = currentCase();
  const regime = state.regime || 'nominal';
  const res = measureResilience(input, { maxSteps: 8, regime });
  if (els.resilienceHorizon) {
    els.resilienceHorizon.textContent = `${res.survivedSteps}/8`;
  }
  if (els.resilienceNote) {
    const regimeLabel = regime === 'nominal' ? '' : ` (${regime})`;
    els.resilienceNote.textContent = (res.finalPreserved ? 'full horizon' : `failed at step ${res.failedAtStep}`) + regimeLabel;
    els.resilienceNote.style.color = res.finalPreserved ? '#2a5' : '#a33';
  }

  // Cross-regime robustness (new): how well does this survive *regardless of condition*?
  // Uses computeCrossRegimeDurability for the pure-logic "condition-independent" score.
  const robust = computeCrossRegimeDurability(input, { maxSteps: 8 });
  if (els.robustnessScore) {
    els.robustnessScore.textContent = robust.robustness.toFixed(2);
  }
  if (els.robustnessNote) {
    const note = robust.fullRobust
      ? 'fully robust across regimes'
      : `min ${robust.minSurvival}/8 (drop stressed: ${robust.dropStressed})`;
    els.robustnessNote.textContent = note;
    els.robustnessNote.style.color = robust.fullRobust ? '#2a5' : '#a33';
  }

  // Regime stability (live): composite across all transition profiles using the new primitive.
  const stab = computeRegimeStability(input, { maxSteps: 8 });
  if (els.stabilityScore) {
    els.stabilityScore.textContent = stab.stability.toFixed(2);
  }
  if (els.stabilityNote) {
    const note = stab.fullStable
      ? 'stable across all profiles'
      : `max frag ${stab.maxFragility} (avg ${stab.avgFragility})`;
    els.stabilityNote.textContent = note;
    els.stabilityNote.style.color = stab.fullStable ? '#2a5' : '#a33';
  }

  // Durability Index (live): unified 0-1 score for long-term coherence under varying conditions.
  if (els.durabilityIndex) {
    els.durabilityIndex.textContent = stab.durabilityIndex.toFixed(2);
  }
  if (els.durabilityNote) {
    const note = stab.durabilityIndex > 0.9 ? 'highly durable' : stab.durabilityIndex > 0.7 ? 'moderately durable' : 'fragile to variation';
    els.durabilityNote.textContent = note;
    els.durabilityNote.style.color = stab.durabilityIndex > 0.7 ? '#2a5' : '#a33';
  }

  // Path Inertia / Memory (live): short nominal trace on current static state to show what memoryMod (coherence inertia from accum carry * (1-stress)) this grammar would build.
  // High inertia means history has created momentum that feeds forward and now also modulates core coherence/identity in snapshots.
  const memTrace = simulateSequence(input, 3);  // default nominal, exercises feed-forward + core memory mod
  const pathInertia = memTrace.trace && memTrace.trace.length ? (memTrace.trace[memTrace.trace.length - 1].memoryMod || 0) : 0;
  if (els.durabilityNote) {
    const current = els.durabilityNote.textContent || '';
    els.durabilityNote.textContent = current + ` | inertia ${pathInertia.toFixed(2)}`;
  }
}

function rebuildScene() {
  group.clear();

  const closed = torusKnotGeometry(state.closedForm);
  if (closed.isGroup) {
    group.add(closed);
  } else {
    const mesh = new THREE.Mesh(closed, materials.closed);
    mesh.rotation.x = Math.PI / 2.5;
    group.add(mesh);
  }

  const path = makeTransientPath(state.transientForm, state.scenario, state.phase);
  const baseRadius = state.transientForm === 'ribbon' ? 0.055 : 0.04;
  const radius = baseRadius * (1 + Math.abs(state.charge) * 0.3);
  const transientMat = state.scenario === 'return' ? materials.returned : materials.transient;
  // Grammar viz: phase shifts the wave/ribbon, charge affects tension (emissive + slight roughness)
  const transient = makeTube(path, radius, transientMat);
  if (state.charge !== 0 || state.phase !== 0.5) {
    transient.material = transientMat.clone();
    transient.material.emissive = transientMat.emissive.clone();
    const tension = Math.abs(state.charge);
    transient.material.emissive.r = Math.min(1, transient.material.emissive.r + tension * 0.45);
    transient.material.roughness = 0.22 + tension * 0.28;
  }
  group.add(transient);

  if (state.scenario === 'store' || state.storage > 0.55) {
    addStoredGlow();
  }
  if (state.scenario === 'store' || state.scatter > 0.38) {
    addScatter();
  }

  const outcome = calculateOutcome(state);
  addRouteSplit(outcome);
  addStressShell(outcome);
  updateReadout(outcome);
  updateResilience();   // live durability horizon (v0.3+)
}

function updateStateFromControls() {
  ['boundary', 'route', 'storage', 'scatter', 'reseat', 'phase', 'charge'].forEach((key) => {
    state[key] = Number(els[key].value);
    if (outputs[key]) outputs[key].textContent = state[key].toFixed(2);
  });
  state.closedForm = els.closedForm.value;
  state.transientForm = els.transientForm.value;
  if (els.regime) state.regime = els.regime.value;
  rebuildScene();
}

document.querySelectorAll('.scenario').forEach((button) => {
  button.addEventListener('click', () => {
    document.querySelectorAll('.scenario').forEach((item) => item.classList.remove('active'));
    button.classList.add('active');
    state.scenario = button.dataset.scenario;
    Object.entries(scenarioPresets[state.scenario]).forEach(([key, value]) => {
      els[key].value = value;
    });
    updateStateFromControls();
  });
});

[els.closedForm, els.transientForm, els.boundary, els.route, els.storage, els.scatter, els.reseat, els.phase, els.charge, els.regime].forEach((control) => {
  if (control) control.addEventListener(control.tagName === 'SELECT' ? 'change' : 'input', updateStateFromControls);
});

// #8 UI->analysis round-trip: export the exact current case as JSON in the
// same shape analysis scripts/the chain runner consume (calculateOutcome
// input). Replay with `npm run case:run -- case.json`.
function currentCase() {
  return {
    schema: 'rs-sandbox-case/v2',
    scenario: state.scenario,
    closedForm: state.closedForm,
    transientForm: state.transientForm,
    boundary: state.boundary,
    route: state.route,
    storage: state.storage,
    scatter: state.scatter,
    reseat: state.reseat,
    phase: state.phase,
    charge: state.charge,
    regime: state.regime,
  };
}

if (els.exportButton && els.exportOutput) {
  els.exportButton.addEventListener('click', () => {
    const json = JSON.stringify(currentCase(), null, 2);
    els.exportOutput.value = json;
    els.exportOutput.hidden = false;
    els.exportOutput.focus();
    els.exportOutput.select();
    if (navigator.clipboard?.writeText) {
      navigator.clipboard.writeText(json).catch(() => {});
    }
  });
}

// v0.4: live trace demo using simulateSequence (pure logic multi-step with memory)
// Surfaces measureResilience: primary = currently selected regime, plus full comparison across regimes.
// Shows compact per-step history mask for the primary regime.
if (els.runTraceButton && els.traceOutput) {
  els.runTraceButton.addEventListener('click', () => {
    const input = currentCase();
    const primaryRegime = state.regime || 'nominal';

    // run a short 3-step trace (use 3 so output is compact)
    const { trace, summary } = simulateSequence(input, 3);
    const lines = trace.map((t, i) =>
      `step${i}: coh=${t.coherenceMetric.toFixed(2)} id=${(t.durabilityAdjustedIdentityScore || t.identityScore).toFixed(2)} stress=${t.closureStress.toFixed(2)} pres=${t.identityPreserved}${t.memoryRescued ? ' (mem-rescued)' : ''} | cont=${t.grammar.continuity.toFixed(2)} pm=${t.grammar.phaseMatch.toFixed(2)} (dur-adj id in trace from feedback)`
    );

    // Primary resilience under the UI-selected regime
    const resPrimary = measureResilience(input, { maxSteps: 8, regime: primaryRegime });
    const hist = resPrimary.history.map(h => h.preserved ? 'P' : 'F').join('');

    // Cross-regime robustness using the new helper (condition-independent durability)
    const robust = computeCrossRegimeDurability(input, { maxSteps: 8 });

    // Always show the other two for comparison (pure logic exploration of conditions)
    const others = ['nominal', 'stressed', 'recovering'].filter(r => r !== primaryRegime);
    const resOther1 = measureResilience(input, { maxSteps: 8, regime: others[0] });
    const resOther2 = measureResilience(input, { maxSteps: 8, regime: others[1] });

    const regimeLine = `${primaryRegime}:${resPrimary.survivedSteps}/8  ${others[0]}:${resOther1.survivedSteps}/8  ${others[1]}:${resOther2.survivedSteps}/8`;

    // Regime transition test + standard profiles with fragility (new)
    const trans = testRegimeTransition(input, { maxSteps: 8 });
    const transLine = `transition survival: ${trans.finalPreserved ? 'full' : 'at risk'} (stressed phase: ${trans.transitionSummary.survivedThroughStressed}/${trans.transitionSummary.stressedStepsInSchedule})`;

    const spikeFrag = computeTransitionFragility(input, { maxSteps: 8, profile: 'stress-spike' });
    const oscFrag = computeTransitionFragility(input, { maxSteps: 8, profile: 'oscillation' });
    const degFrag = computeTransitionFragility(input, { maxSteps: 8, profile: 'gradual-degradation' });
    const profileLine = `fragility: spike=${spikeFrag.fragility} osc=${oscFrag.fragility} deg=${degFrag.fragility}`;

    const stability = computeRegimeStability(input, { maxSteps: 8 });
    const stabilityLine = `stability: ${stability.stability} (maxFrag=${stability.maxFragility}, fullStable=${stability.fullStable})`;

    // Quick regime memory demo (inertia from previous step's regime affects consumption)
    const withMem = testRegimeTransition(input, { maxSteps: 8, regimeMemory: 0.6 });
    const memLine = `with memory (0.6): finalPres=${withMem.finalPreserved}`;

    // Core integration demo: durabilityIndex now in calculateOutcome, with pathQuality scaling the boost (from recent reinf/debt in history)
    const sampleOutcome = calculateOutcome(input, { pathQuality: 0.8 });  // e.g. recent reinforcement
    const coreModLine = `core: durIdx=${sampleOutcome.metrics.durabilityIndex} modulatedId (pathQ 0.8)=${sampleOutcome.metrics.modulatedIdentity}`;

    // Optimal regime policy: which single regime maximizes the durabilityIndex for this config (pure logic "choose the best condition")
    const policy = findBestRegimeForDurability(input, { maxSteps: 8 });
    const policyLine = `best regime for durability: ${policy.bestRegime} (effIdx=${policy.bestEffectiveDurabilityIndex} vs cross=${policy.crossDurabilityIndex})`;

    // Monte Carlo expected durability: average over random transition sequences (probabilistic average-case under unpredictable changes)
    const mc = computeMonteCarloDurability(input, { maxSteps: 8, numTrials: 30 });
    const mcLine = `MC expected finalPres rate: ${mc.expectedFinalPresRate} (avgId=${mc.avgFinalIdentity} over ${mc.numTrials} trials)`;

    // Adaptive policy (state-aware with commitment lookahead): at each step, choose regime maximizing immediate quality (modulated by current stress) + discounted future (blended cross-stability + simulated preservation under *committing/sticking* with that regime for remaining horizon). Active "choosing + committing to conditions to preserve coherence". After preserved policy steps: small carry reinforcement (self-reinforcing paths); after poor steps: debt (degrading paths under bad choices).
    const adaptive = simulateSequence(input, 8, { adaptivePolicy: true, regimeMemory: 0.5 });
    const adaptiveLine = `adaptive policy (state-aware commitment lookahead + MC non-myopic + mem 0.5): finalPres=${adaptive.finalPreserved} avgId=${adaptive.summary.finalIdentity} (+ reinf on preserved, debt on poor steps; carry/stress-decay dur-scaled)`;

    // With switching cost: penalizes changing regimes mid-history (models friction of shifting conditions; encourages sticking with good regimes)
    const adaptiveWithSwitch = simulateSequence(input, 8, { adaptivePolicy: true, regimeMemory: 0.5, regimeSwitchingCost: 0.2 });
    const switchLine = `adaptive + switching cost 0.2: finalPres=${adaptiveWithSwitch.finalPreserved} avgId=${adaptiveWithSwitch.summary.finalIdentity}`;

    els.traceOutput.textContent =
      lines.join('\n') +
      `\n\ntrace summary: finalPres=${summary.finalPreserved}  avgCoh=${summary.avgCoherence}  minCoh=${summary.minCoherence}  finalId=${summary.finalIdentity}` +
      `\nresilience (8-step, primary=${primaryRegime}): ${regimeLine}` +
      `\nrobustness: ${robust.robustness} (min ${robust.minSurvival}/8, fullRobust=${robust.fullRobust})` +
      `\n${transLine}` +
      `\n${profileLine}` +
      `\n${stabilityLine}` +
      `\n${memLine}` +
      `\n${policyLine}` +
      `\n${mcLine}` +
      `\n${adaptiveLine}` +
      `\n${switchLine}` +
      `\n${coreModLine}` +
      `\nfeedback: consumption (fatigue) modulated by step durIdx; carry fraction of prior continuity + stress decay rate now explicitly scaled by durability (high-dur retains more coherence memory / sheds history stress faster); reinf/debt amplified (closed full-loop at accumulator level); path memory (accum carry * (1-stress)) now feeds forward to boost next-step route and raise next scatter (history state changes the inputs to the 4-bucket + grammar + coherence calc); memoryMod passed to core calculateOutcome (history inertia now also directly boosts coherence/identity and relaxes the preservation gate in the single-step view, like durability); memory now further eases fatigue and amplifies reinf/debt (stronger virtuous cycles when inertia high); adaptive commitment value boosted by current memory (high inertia makes sticking with a regime more attractive in lookahead); memory now modulates the 4-bucket outcomes in core (high inertia shifts admitted+stored up, scattered down — history changes the immediate fate fractions); memory now explicitly modulates grammarAlignment and coherenceMetric in core (inertia as a direct grammar factor strengthening alignment); adaptive choice now blends MC expected preservation (non-myopic averaging over random future condition sequences)` +
      `\ndur-adjusted id (last adaptive step): ${ (adaptive && adaptive.trace && adaptive.trace.length > 0) ? (adaptive.trace[adaptive.trace.length-1].durabilityAdjustedIdentityScore || 'N/A').toFixed ? (adaptive.trace[adaptive.trace.length-1].durabilityAdjustedIdentityScore || 'N/A').toFixed(3) : (adaptive.trace[adaptive.trace.length-1].durabilityAdjustedIdentityScore || 'N/A') : 'N/A' } (higher in high-dur paths)` +
      `\nhistory (${primaryRegime}): ${hist}  (P=preserved, F=failed)`;
  });
}

if (els.suggestStableButton && els.traceOutput) {
  els.suggestStableButton.addEventListener('click', () => {
    const input = currentCase();
    const suggestion = findHighStabilitySettings(input, { maxSteps: 8, samples: 30, stepSize: 0.07 });
    const currentStabObj = computeRegimeStability(input, { maxSteps: 8 });
    const currentDur = currentStabObj.durabilityIndex;

    let text = `Current: stability=${currentStabObj.stability} durabilityIndex=${currentDur}\n`;
    if (suggestion.improvement > 0.001) {
      const projDur = suggestion.projectedDurabilityIndex;
      text += `Found better: stability=${suggestion.bestStability} (+${suggestion.improvement}) durabilityIndex=${projDur}\n`;
      text += `Deltas: ${JSON.stringify(suggestion.delta)}\n`;
      text += `Try: boundary≈${suggestion.suggestedInput.boundary} route≈${suggestion.suggestedInput.route} reseat≈${suggestion.suggestedInput.reseat} phase≈${suggestion.suggestedInput.phase} charge≈${suggestion.suggestedInput.charge}`;
    } else {
      text += `No significantly better local setting found (already near local peak).`;
    }
    els.traceOutput.textContent = text;
  });
}

function resize() {
  const rect = canvas.getBoundingClientRect();
  renderer.setSize(rect.width, rect.height, false);
  camera.aspect = rect.width / Math.max(rect.height, 1);
  camera.updateProjectionMatrix();
}

window.addEventListener('resize', resize);

function animate(time = 0) {
  resize();
  const t = time * 0.001;
  group.rotation.y = Math.sin(t * 0.28) * 0.22 + t * 0.08;
  group.rotation.x = Math.sin(t * 0.2) * 0.08;
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}

updateStateFromControls();
animate();
