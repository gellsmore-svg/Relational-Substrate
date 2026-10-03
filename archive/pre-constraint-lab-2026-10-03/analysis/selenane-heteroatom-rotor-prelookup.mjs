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

const geometryBase = {
  molecule: 'H-Se-Se-H',
  centralBond: 2.4,
  sideBond: 1.51,
  routeBase: 0.7,
  sideAngleBracket: [92, 95, 98],
  sources: [
    'Cordero-style covalent-radius estimate: Se = 1.20 A, H = 0.31 A, so Se-Se = 2.40 A and Se-H = 1.51 A.',
    'Bent-valence sensitivity bracket locked before lookup: H-Se-Se = 92, 95, 98 degrees.',
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
  Se: 2.55,
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

function selenaneCharges() {
  const magnitude = chargeMagnitude('Se', 'H');
  return {
    H: magnitude,
    Se: -magnitude,
    note: 'Se-H Delta EN is locked at 0.35 in the <0.4 band; Se-Se has no polarity contribution.',
  };
}

function selenaneAtoms(torsionDegreesValue, sideAngle) {
  const central = geometryBase.centralBond;
  const side = geometryBase.sideBond;
  const angle = (sideAngle * Math.PI) / 180;
  const torsion = (torsionDegreesValue * Math.PI) / 180;
  const xOffset = Math.cos(angle) * side;
  const radial = Math.sin(angle) * side;
  const charges = selenaneCharges();

  return [
    { element: 'Se', partialCharge: charges.Se, position: vec(-central / 2, 0, 0) },
    { element: 'Se', partialCharge: charges.Se, position: vec(central / 2, 0, 0) },
    { element: 'H', partialCharge: charges.H, position: vec(-central / 2 - xOffset, radial, 0) },
    { element: 'H', partialCharge: charges.H, position: vec(central / 2 + xOffset, Math.cos(torsion) * radial, Math.sin(torsion) * radial) },
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
  const routeContinuity = clamp01(geometryBase.routeBase - bondRms * 0.08 - angleRms * 0.08 - effectiveTorsionRms * 0.16 - stericDeviation * 0.08 - cisCrowding * 0.18);
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

function classifyTopology(rows) {
  return rows.map((row, index) => {
    const previous = index === 0 ? rows[1] : rows[index - 1];
    const next = index === rows.length - 1 ? rows[rows.length - 2] : rows[index + 1];
    let topology = 'neither';
    if (row.modelCm1 < previous.modelCm1 && row.modelCm1 < next.modelCm1) topology = 'local-minimum';
    if (row.modelCm1 > previous.modelCm1 && row.modelCm1 > next.modelCm1) topology = 'local-maximum';
    return { ...row, topology };
  });
}

function rowsForReference(referenceAngle, sideAngle, scaleTransfer) {
  const referenceFeatures = coordinateFeatures(selenaneAtoms(referenceAngle, sideAngle));
  const referenceCandidate = deriveCandidate(referenceFeatures, referenceFeatures, referenceAngle);
  const referenceScore = scoreCandidate(referenceCandidate);

  const rows = gridAngles.map((angle) => {
    const features = coordinateFeatures(selenaneAtoms(angle, sideAngle));
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

  return classifyTopology(rows);
}

function bestAngle(rows) {
  return rows.reduce((best, row) => (row.score > best.score ? row : best), rows[0]).angle;
}

function topologyDiagnosis(rows) {
  const transRow = rows.find((row) => row.angle === 180);
  const transPathRows = rows.filter((row) => row.angle >= 90 && row.angle <= 180);
  const nearestMaximum = transPathRows.reduce((best, row) => (row.modelCm1 > best.modelCm1 ? row : best), transPathRows[0]);
  return {
    transTopology: transRow.topology,
    spuriousTransLocalMinimum: transRow.topology === 'local-minimum',
    nearestTransPathMaximum: {
      angle: nearestMaximum.angle,
      modelCm1: nearestMaximum.modelCm1,
    },
  };
}

function runBracket(sideAngle, scaleTransfer) {
  const firstPassRows = rowsForReference(90, sideAngle, scaleTransfer);
  const modelPredictedMinimum = bestAngle(firstPassRows);
  const frozenRows = rowsForReference(modelPredictedMinimum, sideAngle, scaleTransfer);
  return {
    sideAngle,
    firstPassRows,
    modelPredictedMinimum,
    frozenRows,
    topology: topologyDiagnosis(frozenRows),
  };
}

function markdownTable(rows) {
  const header = '| angle | score | penalty | model cm-1 | topology | torsion | steric clearance | cis crowding | anti-planar release |';
  const rule = '|---:|---:|---:|---:|---|---:|---:|---:|---:|';
  const body = rows.map((row) => `| ${row.angle} | ${row.score} | ${row.penalty} | ${row.modelCm1} | ${row.topology} | ${row.torsionMean} | ${row.stericClearance} | ${row.cisCrowding} | ${row.antiPlanarRelease} |`);
  return [header, rule, ...body].join('\n');
}

function bracketMarkdown(result) {
  return `## Bracket Angle ${result.sideAngle} Degrees

- model-predicted minimum: ${result.modelPredictedMinimum} degrees
- trans topology: ${result.topology.transTopology}
- spurious trans local minimum: ${result.topology.spuriousTransLocalMinimum ? 'yes' : 'no'}
- nearest skew-to-trans path maximum: ${result.topology.nearestTransPathMaximum.modelCm1} cm-1 at ${result.topology.nearestTransPathMaximum.angle} degrees

### First Pass Rows

${markdownTable(result.firstPassRows)}

### Frozen Reference Rows

${markdownTable(result.frozenRows)}
`;
}

async function main() {
  const ethane = JSON.parse(await readFile(new URL('external-ethane-quantitative-benchmark.json', outDir), 'utf8'));
  const scaleTransfer = {
    source: 'external-ethane-quantitative-benchmark.json',
    kcalPerPenalty: ethane.scale.kcalPerPenalty,
    cm1PerPenalty: ethane.scale.kcalPerPenalty * cm1PerKcalMol,
  };
  const charges = selenaneCharges();
  const bracketResults = geometryBase.sideAngleBracket.map((sideAngle) => runBracket(sideAngle, scaleTransfer));
  const anySpuriousTransMinimum = bracketResults.some((result) => result.topology.spuriousTransLocalMinimum);

  const payload = {
    status: 'prelookup-model-output',
    target: 'selenane H-Se-Se-H',
    targetBarrierLookupPerformed: false,
    geometry: geometryBase,
    chargeRule: {
      electronegativity,
      chargeBands,
      assigned: charges,
    },
    transferConstants: {
      routeBase: geometryBase.routeBase,
      cisCrowdingThreshold: 60,
      antiPlanarStart: 145,
      antiPlanarSpan: 35,
      scaleTransfer,
    },
    gridAngles,
    topologyRule:
      'Classify each frozen-reference grid row by neighbouring model barrier values on the 0..180 half-scan; a local minimum at 180 degrees is a spurious trans local minimum.',
    anySpuriousTransMinimum,
    bracketResults,
    passFailRules: {
      freeRotorDiagnostic: 'external barrier < 250 cm-1',
      smallBarrier: '250-700 cm-1 requires predicted barrier within [0.5x, 2x] external',
      largeBarrier: '>700 cm-1 requires <=35 percent absolute error',
      minimumLocation: 'within 30 degrees of external minimum',
      topology: 'if external source reports trans maximum, any model local minimum at 180 degrees is topology failure',
      noRetune: 'failure is recorded; no constants altered before an explicitly declared redesign track',
    },
  };

  const md = `# H-Se-Se-H Heteroatom Rotor Prelookup Output

Status: prelookup model output. No H-Se-Se-H barrier or minimum-angle value has been consulted in this script.

## Locked Inputs

- molecule: ${geometryBase.molecule}
- Se-Se: ${geometryBase.centralBond} A
- Se-H: ${geometryBase.sideBond} A
- H-Se-Se angle bracket: ${geometryBase.sideAngleBracket.join(', ')} degrees
- routeBase: ${geometryBase.routeBase}
- assigned charges: Se ${charges.Se}, H ${charges.H}
- scale: ${round(scaleTransfer.cm1PerPenalty, 2)} cm-1 per penalty unit

Geometry inputs are load-bearing model inputs because they set steric clearance and therefore cisCrowding.

## Topology Summary

- any spurious trans local minimum across bracket: ${anySpuriousTransMinimum ? 'yes' : 'no'}

${bracketResults.map(bracketMarkdown).join('\n')}

## Locked Comparison Rules

- external barrier < 250 cm-1: diagnostic free-rotor regime
- external barrier 250-700 cm-1: predicted barrier must be within [0.5x, 2x] external
- external barrier > 700 cm-1: absolute percent error must be <= 35 percent
- model-predicted minimum must be within 30 degrees of the external minimum
- trans-side topology must not be softened into a grid-point ordering pass
- model[0 degrees] > model[180 degrees] is not evidence-bearing on its own
- no rolled-up status may use "partial pass" or "mixed result"
- no geometry, coefficients, angle grid, source tables, scoring terms, or reference-state rule may change after lookup
`;

  await mkdir(outDir, { recursive: true });
  await writeFile(new URL('selenane-heteroatom-rotor-prelookup.json', outDir), `${JSON.stringify(payload, null, 2)}\n`);
  await writeFile(new URL('selenane-heteroatom-rotor-prelookup.md', outDir), md);
  console.log(md);
}

await main();
