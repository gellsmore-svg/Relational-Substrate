import './styles.css';
import * as THREE from 'three';
import { calculateOutcome, scenarioPresets } from './model.js';

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
};

const outputs = {
  boundary: document.querySelector('#boundary-value'),
  route: document.querySelector('#route-value'),
  storage: document.querySelector('#storage-value'),
  scatter: document.querySelector('#scatter-value'),
  reseat: document.querySelector('#reseat-value'),
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

function makeTransientPath(kind, scenario) {
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
      return new THREE.Vector3(x, Math.sin(t * Math.PI * 5.5) * 0.28, Math.cos(t * Math.PI * 4) * 0.18);
    });
  }

  if (kind === 'ribbon') {
    return [
      new THREE.Vector3(-5.4, -0.25, -0.2),
      new THREE.Vector3(-2.4, 0.12, 0.35),
      new THREE.Vector3(0, 0.3, -0.15),
      new THREE.Vector3(2.4, 0.12, 0.35),
      new THREE.Vector3(5.4, -0.25, -0.2),
    ];
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
    outputs.metrics[key].textContent = value.toFixed(2);
  });

  const readings = {
    Admitted: 'The transient is admitted with coherent delay. The closed form flexes within tolerance and returns.',
    Returned: 'Boundary compatibility is poor inward but strong enough to return the transient coherently.',
    Stored: 'Part of the transient becomes local stress or lock-up. This is not vorton generation unless invariant closure persists.',
    Scattered: 'Route compatibility is uneven. The open transient fragments into multiple weaker outcomes.',
  };
  const gate = outcome.identityPreserved
    ? 'The closure gate remains above threshold.'
    : 'The closure gate falls below threshold: identity is at risk.';
  els.reading.textContent = `${readings[dominant]} ${gate}`;
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

  const path = makeTransientPath(state.transientForm, state.scenario);
  const transient = makeTube(path, state.transientForm === 'ribbon' ? 0.055 : 0.04, state.scenario === 'return' ? materials.returned : materials.transient);
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
}

function updateStateFromControls() {
  ['boundary', 'route', 'storage', 'scatter', 'reseat'].forEach((key) => {
    state[key] = Number(els[key].value);
    outputs[key].textContent = state[key].toFixed(2);
  });
  state.closedForm = els.closedForm.value;
  state.transientForm = els.transientForm.value;
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

[els.closedForm, els.transientForm, els.boundary, els.route, els.storage, els.scatter, els.reseat].forEach((control) => {
  control.addEventListener('input', updateStateFromControls);
});

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
