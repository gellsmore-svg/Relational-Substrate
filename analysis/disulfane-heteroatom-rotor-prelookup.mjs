import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const cm1PerKcalMol = 349.755;

const familyWeights = {
  valenceSatisfaction: 0.16,
  geometryFit: 0.16,
  angleStrain: 0.14,
  bondStrain: 0.13,
  polarityBalance: 0.11,
  routeContinuity: 0.14,
  ringClosure: 0,
  stericObstruction: 0.16,
};

const geometry = {
  molecule: 'H-S-S-H',
  centralBond: 2.1,
  sideBond: 1.36,
  sideAngle: 98,
  routeBase: 0.7,
  sources: [
    'Cordero-style covalent-radius estimate: S = 1.05 A, H = 0.31 A, so S-S = 2.10 A and S-H = 1.36 A.',
    'Second-row bent-valence class angle fixed at H-S-S = 98 degrees before barrier lookup.',
  ],
};

const chargeBands = [
  { min: 0, max: 0.4, magnitude: 0.05 },
  { min: 0.4, max: 0.9, magnitude: 0.2 },
  { min: 0.9, max: 1.4, magnitude: 0.35 },
  { min: 1.4, max: Infinity, magnitude: 0.5 },
];

const electronegativity = {
  H: 2.2,
  S: 2.58,
};

const tolerances = {
  bondLength: 0.2,
  bondAngle: 28,
  torsion: 45,
  polarityVector: 0.85,
  stericClearance: 0.5,
};

const gridAngles = [0, 30, 60, 90, 120, 150, 180];

function clamp01(value) {
  return Math.max(0, Math.min(1, value));
}

function round(value, digits = 4) {
  return Number(value.toFixed(digits));
}

function vec(x, y, z = 0) {
  return { x, y, z };
}

function add(a, b) {
  return vec(a.x + b.x, a.y + b.y, a.z + b.z);
}

function sub(a, b) {
  return vec(a.x - b.x, a.y - b.y, a.z - b.z);
}

function scale(a, factor) {
  return vec(a.x * factor, a.y * factor, a.z * factor);
}

function dot(a, b) {
  return a.x * b.x + a.y * b.y + a.z * b.z;
}

function cross(a, b) {
  return vec(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x);
}

function norm(a) {
  return Math.sqrt(dot(a, a));
}

function distance(a, b) {
  return norm(sub(a, b));
}

function average(values) {
  return values.length ? values.reduce((sum, value) => sum + value, 0) / values.length : 0;
}

function rms(values) {
  return values.length ? Math.sqrt(values.reduce((sum, value) => sum + value * value, 0) / values.length) : 0;
}

function maxOrZero(values) {
  return values.length ? Math.max(...values) : 0;
}

function angleDegrees(a, b, c) {
  const ba = sub(a, b);
  const bc = sub(c, b);
  const denominator = Math.max(norm(ba) * norm(bc), 1e-9);
  const cosine = Math.max(-1, Math.min(1, dot(ba, bc) / denominator));
  return (Math.acos(cosine) * 180) / Math.PI;
}

function torsionDegrees(a, b, c, d) {
  const b1 = sub(b, a);
  const b2 = sub(c, b);
  const b3 = sub(d, c);
  const n1 = cross(b1, b2);
  const n2 = cross(b2, b3);
  const m1 = cross(n1, scale(b2, 1 / Math.max(norm(b2), 1e-9)));
  return (Math.atan2(dot(m1, n2), dot(n1, n2)) * 180) / Math.PI;
}

function cyclicDifference(value, target, period = 360) {
  const raw = Math.abs(((value - target + period / 2) % period) - period / 2);
  return Math.min(raw, period - raw);
}

function chargeMagnitude(elementA, elementB) {
  const delta = Math.abs(electronegativity[elementA] - electronegativity[elementB]);
  const band = chargeBands.find((entry) => delta >= entry.min && delta < entry.max);
  return band.magnitude;
}

function disulfaneCharges() {
  const magnitude = chargeMagnitude('S', 'H');
  return {
    H: magnitude,
    S: -magnitude,
    note: 'S-H Delta EN is in the <0.4 band; S-S has no polarity contribution.',
  };
}

function disulfaneAtoms(torsionDegreesValue) {
  const ss = geometry.centralBond;
  const sh = geometry.sideBond;
  const angle = (geometry.sideAngle * Math.PI) / 180;
  const torsion = (torsionDegreesValue * Math.PI) / 180;
  const xOffset = Math.cos(angle) * sh;
  const radial = Math.sin(angle) * sh;
  const charges = disulfaneCharges();

  return [
    { element: 'S', partialCharge: charges.S, position: vec(-ss / 2, 0, 0) },
    { element: 'S', partialCharge: charges.S, position: vec(ss / 2, 0, 0) },
    { element: 'H', partialCharge: charges.H, position: vec(-ss / 2 - xOffset, radial, 0) },
    { element: 'H', partialCharge: charges.H, position: vec(ss / 2 + xOffset, Math.cos(torsion) * radial, Math.sin(torsion) * radial) },
  ];
}

function coordinateFeatures(atoms) {
  const bonds = [
    [0, 1],
    [0, 2],
    [1, 3],
  ];
  const angles = [
    [2, 0, 1],
    [0, 1, 3],
  ];
  const torsions = [[2, 0, 1, 3]];
  const bondLengths = bonds.map(([a, b]) => distance(atoms[a].position, atoms[b].position));
  const angleValues = angles.map(([a, b, c]) => angleDegrees(atoms[a].position, atoms[b].position, atoms[c].position));
  const torsionValues = torsions.map(([a, b, c, d]) => Math.abs(torsionDegrees(atoms[a].position, atoms[b].position, atoms[c].position, atoms[d].position)));
  const crossSideDistances = [distance(atoms[2].position, atoms[3].position)];
  const chargeCentre = atoms.reduce(
    (sum, atom) => add(sum, scale(atom.position, atom.partialCharge)),
    vec(0, 0, 0)
  );

  return {
    bondLengths,
    angles: angleValues,
    torsions: torsionValues,
    polarityVector: norm(chargeCentre),
    stericClearance: Math.min(...crossSideDistances),
    stericMean: average(crossSideDistances),
  };
}

function deriveCandidate(features, referenceFeatures, referenceTorsion) {
  const bondDeviations = features.bondLengths.map((length, index) => clamp01(Math.abs(length - referenceFeatures.bondLengths[index]) / tolerances.bondLength));
  const angleDeviations = features.angles.map((angle, index) => clamp01(Math.abs(angle - referenceFeatures.angles[index]) / tolerances.bondAngle));
  const torsionDeviations = features.torsions.map((torsion) => clamp01(cyclicDifference(torsion, referenceTorsion) / tolerances.torsion));
  const stericDeviation = clamp01((referenceFeatures.stericClearance - features.stericClearance) / tolerances.stericClearance);
  const polarityDeviation = clamp01(Math.abs(features.polarityVector - referenceFeatures.polarityVector) / tolerances.polarityVector);

  const bondRms = rms(bondDeviations);
  const bondMax = maxOrZero(bondDeviations);
  const angleRms = rms(angleDeviations);
  const angleMax = maxOrZero(angleDeviations);
  const torsionRms = rms(torsionDeviations);
  const torsionMax = maxOrZero(torsionDeviations);
  const torsionMean = average(features.torsions);
  const cisCrowding = clamp01(stericDeviation * clamp01((60 - torsionMean) / 60));
  const antiPlanarRelease = clamp01((torsionMean - 145) / 35) * clamp01(1 - stericDeviation) * clamp01(1 - cisCrowding);
  const effectiveTorsionRms = torsionRms * (1 - antiPlanarRelease * 0.65);
  const effectiveTorsionMax = torsionMax * (1 - antiPlanarRelease * 0.65);

  const bondStrain = clamp01(bondRms * 0.65 + bondMax * 0.2);
  const angleStrain = clamp01(
    angleRms * 0.42 + angleMax * 0.16 + effectiveTorsionRms * 0.3 + effectiveTorsionMax * 0.08 + stericDeviation * 0.04 + cisCrowding * 0.48
  );
  const geometryFit = clamp01(
    1 - (bondRms * 0.18 + bondMax * 0.08 + angleRms * 0.18 + angleMax * 0.07 + effectiveTorsionRms * 0.24 + stericDeviation * 0.18 + cisCrowding * 0.36)
  );
  const routeContinuity = clamp01(geometry.routeBase - bondRms * 0.08 - angleRms * 0.08 - effectiveTorsionRms * 0.16 - stericDeviation * 0.08 - cisCrowding * 0.18);
  const polarityBalance = clamp01(1 - polarityDeviation * 0.72);

  return {
    valenceSatisfaction: clamp01(1 - bondMax * 0.08),
    geometryFit,
    angleStrain,
    bondStrain,
    polarityBalance,
    routeContinuity,
    ringClosure: 0,
    stericObstruction: stericDeviation,
    coordinateMetrics: {
      bondRms,
      angleRms,
      torsionRms,
      effectiveTorsionRms,
      torsionMax,
      steric: stericDeviation,
      cisCrowding,
      antiPlanarRelease,
      stericClearance: features.stericClearance,
      stericMean: features.stericMean,
      torsionMean,
      polarityDeviation,
    },
  };
}

function scoreCandidate(candidate) {
  const score =
    candidate.valenceSatisfaction * familyWeights.valenceSatisfaction +
    candidate.geometryFit * familyWeights.geometryFit +
    (1 - candidate.angleStrain) * familyWeights.angleStrain +
    (1 - candidate.bondStrain) * familyWeights.bondStrain +
    candidate.polarityBalance * familyWeights.polarityBalance +
    candidate.routeContinuity * familyWeights.routeContinuity +
    candidate.ringClosure * familyWeights.ringClosure +
    (1 - candidate.stericObstruction) * familyWeights.stericObstruction;

  return clamp01(score);
}

function rowsForReference(referenceAngle, scaleTransfer) {
  const referenceFeatures = coordinateFeatures(disulfaneAtoms(referenceAngle));
  const referenceCandidate = deriveCandidate(referenceFeatures, referenceFeatures, referenceAngle);
  const referenceScore = scoreCandidate(referenceCandidate);

  return gridAngles.map((angle) => {
    const features = coordinateFeatures(disulfaneAtoms(angle));
    const candidate = deriveCandidate(features, referenceFeatures, referenceAngle);
    const score = scoreCandidate(candidate);
    const penalty = Math.max(0, referenceScore - score);

    return {
      angle,
      score: round(score),
      penalty: round(penalty),
      modelCm1: round(penalty * scaleTransfer.cm1PerPenalty, 2),
      torsionMean: round(candidate.coordinateMetrics.torsionMean, 2),
      effectiveTorsionRms: round(candidate.coordinateMetrics.effectiveTorsionRms, 4),
      stericClearance: round(candidate.coordinateMetrics.stericClearance, 4),
      stericDeviation: round(candidate.coordinateMetrics.steric, 4),
      cisCrowding: round(candidate.coordinateMetrics.cisCrowding, 4),
      antiPlanarRelease: round(candidate.coordinateMetrics.antiPlanarRelease, 4),
      polarityDeviation: round(candidate.coordinateMetrics.polarityDeviation, 4),
      geometryFit: round(candidate.geometryFit, 4),
      angleStrain: round(candidate.angleStrain, 4),
      routeContinuity: round(candidate.routeContinuity, 4),
    };
  });
}

function bestAngle(rows) {
  return rows.reduce((best, row) => (row.score > best.score ? row : best), rows[0]).angle;
}

function markdownTable(rows) {
  const header = '| angle | score | penalty | model cm-1 | torsion | steric clearance | cis crowding | anti-planar release |';
  const rule = '|---:|---:|---:|---:|---:|---:|---:|---:|';
  const body = rows.map((row) => `| ${row.angle} | ${row.score} | ${row.penalty} | ${row.modelCm1} | ${row.torsionMean} | ${row.stericClearance} | ${row.cisCrowding} | ${row.antiPlanarRelease} |`);
  return [header, rule, ...body].join('\n');
}

async function main() {
  const ethane = JSON.parse(await readFile(new URL('external-ethane-quantitative-benchmark.json', outDir), 'utf8'));
  const scaleTransfer = {
    source: 'external-ethane-quantitative-benchmark.json',
    kcalPerPenalty: ethane.scale.kcalPerPenalty,
    cm1PerPenalty: ethane.scale.kcalPerPenalty * cm1PerKcalMol,
  };
  const firstPassRows = rowsForReference(90, scaleTransfer);
  const modelPredictedMinimum = bestAngle(firstPassRows);
  const frozenRows = rowsForReference(modelPredictedMinimum, scaleTransfer);
  const charges = disulfaneCharges();

  const payload = {
    status: 'prelookup-model-output',
    target: 'disulfane H-S-S-H',
    targetBarrierLookupPerformed: false,
    geometry,
    chargeRule: {
      electronegativity,
      chargeBands,
      assigned: charges,
    },
    transferConstants: {
      routeBase: geometry.routeBase,
      cisCrowdingThreshold: 60,
      antiPlanarStart: 145,
      antiPlanarSpan: 35,
      scaleTransfer,
    },
    gridAngles,
    referenceStateRule: {
      temporaryReferenceAngle: 90,
      modelPredictedMinimum,
      frozenReferenceAngle: modelPredictedMinimum,
    },
    firstPassRows,
    frozenRows,
    passFailRules: {
      freeRotorDiagnostic: 'external barrier < 250 cm-1',
      smallBarrier: '250-700 cm-1 requires predicted barrier within [0.5x, 2x] external',
      largeBarrier: '>700 cm-1 requires <=35 percent absolute error',
      minimumLocation: 'within 30 degrees of external minimum',
      noRetune: 'failure is recorded; no constants altered before a different-topology fresh target',
    },
  };

  const md = `# Disulfane Heteroatom Rotor Prelookup Output

Status: prelookup model output. No disulfane barrier value has been consulted in this script.

## Locked Inputs

- molecule: ${geometry.molecule}
- S-S: ${geometry.centralBond} A
- S-H: ${geometry.sideBond} A
- H-S-S angle: ${geometry.sideAngle} degrees
- routeBase: ${geometry.routeBase}
- assigned charges: S ${charges.S}, H ${charges.H}
- scale: ${round(scaleTransfer.cm1PerPenalty, 2)} cm-1 per penalty unit

## Reference-State Rule

The temporary reference is 90 degrees. The highest-score first-pass row selects the model-predicted minimum, then the reference features are rebuilt and frozen at that angle.

- model-predicted minimum: ${modelPredictedMinimum} degrees

## First Pass Rows

${markdownTable(firstPassRows)}

## Frozen Reference Rows

${markdownTable(frozenRows)}

## Locked Comparison Rules

- external barrier < 250 cm-1: diagnostic free-rotor regime
- external barrier 250-700 cm-1: predicted barrier must be within [0.5x, 2x] external
- external barrier > 700 cm-1: absolute percent error must be <= 35 percent
- model-predicted minimum must be within 30 degrees of the external minimum
- no geometry, coefficients, angle grid, source tables, or scoring terms may change after lookup
- if the target fails, record the failure; do not retune before selecting a different-topology fresh target
`;

  await mkdir(outDir, { recursive: true });
  await writeFile(new URL('disulfane-heteroatom-rotor-prelookup.json', outDir), `${JSON.stringify(payload, null, 2)}\n`);
  await writeFile(new URL('disulfane-heteroatom-rotor-prelookup.md', outDir), md);
  console.log(md);
}

await main();
