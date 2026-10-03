import { mkdir, writeFile } from 'node:fs/promises';
import { clamp01, scoreCandidate } from './molecule-model.mjs';

const outDir = new URL('./out/', import.meta.url);

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

const reference = {
  formula: 'C2H6',
  family: 'rotatable covalent',
  bondLength: 1.535,
  bondAngle: 109.5,
  torsion: 60,
  routeBase: 0.78,
  valenceCapacity: 4,
};

const tolerances = {
  bondLength: 0.22,
  bondAngle: 30,
  torsion: 50,
  polarityVector: 0.65,
  stericClearance: 0.55,
  valenceMismatch: 1,
};

function vec(x, y, z = 0) {
  return { x, y, z };
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
  return values.length ? values.reduce((sum, value) => sum + value, 0) / values.length : null;
}

function rms(values) {
  return values.length ? Math.sqrt(values.reduce((sum, value) => sum + value * value, 0) / values.length) : 0;
}

function maxOrZero(values) {
  return values.length ? Math.max(...values) : 0;
}

function pairKey(a, b) {
  return [Math.min(a, b), Math.max(a, b)].join('-');
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

function ethaneAtoms(torsionDegreesValue) {
  const cc = reference.bondLength;
  const ch = 1.095;
  const axial = ch / 3;
  const radius = Math.sqrt(Math.max(ch * ch - axial * axial, 0));
  const atoms = [
    { element: 'C', partialCharge: -0.12, position: vec(-cc / 2, 0, 0) },
    { element: 'C', partialCharge: -0.12, position: vec(cc / 2, 0, 0) },
  ];

  for (let i = 0; i < 3; i += 1) {
    const theta = (i / 3) * Math.PI * 2;
    atoms.push({ element: 'H', partialCharge: 0.04, position: vec(-cc / 2 - axial, Math.cos(theta) * radius, Math.sin(theta) * radius) });
  }

  const offset = (torsionDegreesValue * Math.PI) / 180;
  for (let i = 0; i < 3; i += 1) {
    const theta = (i / 3) * Math.PI * 2 + offset;
    atoms.push({ element: 'H', partialCharge: 0.04, position: vec(cc / 2 + axial, Math.cos(theta) * radius, Math.sin(theta) * radius) });
  }

  return atoms;
}

const definition = {
  bonds: [
    [0, 1],
    [0, 2],
    [0, 3],
    [0, 4],
    [1, 5],
    [1, 6],
    [1, 7],
  ],
  angles: [
    [2, 0, 1],
    [3, 0, 1],
    [4, 0, 1],
    [5, 1, 0],
    [6, 1, 0],
    [7, 1, 0],
  ],
  torsions: [
    [2, 0, 1, 5],
    [3, 0, 1, 6],
    [4, 0, 1, 7],
  ],
};

function coordinateFeatures(atoms) {
  const bonded = new Set(definition.bonds.map(([a, b]) => pairKey(a, b)));
  const bondLengths = definition.bonds.map(([a, b]) => distance(atoms[a].position, atoms[b].position));
  const angles = definition.angles.map(([a, b, c]) => angleDegrees(atoms[a].position, atoms[b].position, atoms[c].position));
  const torsions = definition.torsions.map(([a, b, c, d]) => {
    const raw = Math.abs(torsionDegrees(atoms[a].position, atoms[b].position, atoms[c].position, atoms[d].position));
    return raw > 180 ? 360 - raw : raw;
  });
  const chargeCentre = atoms.reduce(
    (sum, atom) => vec(sum.x + atom.position.x * atom.partialCharge, sum.y + atom.position.y * atom.partialCharge, sum.z + atom.position.z * atom.partialCharge),
    vec(0, 0, 0)
  );
  const rotatableDistances = [];
  for (const left of [2, 3, 4]) {
    for (const right of [5, 6, 7]) {
      if (!bonded.has(pairKey(left, right))) {
        rotatableDistances.push(distance(atoms[left].position, atoms[right].position));
      }
    }
  }

  return {
    bondLengths,
    angles,
    torsions,
    polarityVector: norm(chargeCentre),
    stericClearance: Math.min(...rotatableDistances),
  };
}

function cyclicDifference(value, target, period = 120) {
  const raw = Math.abs(((value - target + period / 2) % period) - period / 2);
  return Math.min(raw, period - raw);
}

function deriveCandidate(features, referenceFeatures) {
  const bondDeviations = features.bondLengths.map((length, index) => clamp01(Math.abs(length - referenceFeatures.bondLengths[index]) / tolerances.bondLength));
  const angleDeviations = features.angles.map((angle, index) => clamp01(Math.abs(angle - referenceFeatures.angles[index]) / tolerances.bondAngle));
  const torsionDeviations = features.torsions.map((torsion) => clamp01(cyclicDifference(torsion, reference.torsion, 120) / tolerances.torsion));
  const stericDeviation = clamp01((referenceFeatures.stericClearance - features.stericClearance) / tolerances.stericClearance);
  const polarityDeviation = clamp01(Math.abs(features.polarityVector - referenceFeatures.polarityVector) / tolerances.polarityVector);

  const bondRms = rms(bondDeviations);
  const bondMax = maxOrZero(bondDeviations);
  const angleRms = rms(angleDeviations);
  const angleMax = maxOrZero(angleDeviations);
  const torsionRms = rms(torsionDeviations);
  const torsionMax = maxOrZero(torsionDeviations);

  const bondStrain = clamp01(bondRms * 0.65 + bondMax * 0.2);
  const angleStrain = clamp01(angleRms * 0.44 + angleMax * 0.16 + torsionRms * 0.28 + torsionMax * 0.08 + stericDeviation * 0.04);
  const geometryFit = clamp01(1 - (bondRms * 0.18 + bondMax * 0.08 + angleRms * 0.18 + angleMax * 0.07 + torsionRms * 0.24 + stericDeviation * 0.18));
  const routeContinuity = clamp01(reference.routeBase - bondRms * 0.08 - angleRms * 0.08 - torsionRms * 0.16 - stericDeviation * 0.08);
  const polarityBalance = clamp01(1 - polarityDeviation * 0.72);
  const stericObstruction = stericDeviation;

  return {
    valenceSatisfaction: clamp01(1 - bondMax * 0.08),
    geometryFit,
    angleStrain,
    bondStrain,
    polarityBalance,
    routeContinuity,
    ringClosure: 0,
    stericObstruction,
    coordinateMetrics: {
      bondRms,
      bondMax,
      angleRms,
      angleMax,
      torsionRms,
      torsionMax,
      steric: stericDeviation,
      stericClearance: features.stericClearance,
      torsionMean: average(features.torsions),
    },
  };
}

function scoreFamilyCandidate(candidate) {
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

function expectedClass(angle) {
  return [60, 180, 300].includes(angle) ? 'staggered-like' : [0, 120, 240].includes(angle) ? 'eclipsed-like' : 'intermediate';
}

function round(value, digits = 4) {
  return Number(value.toFixed(digits));
}

const referenceFeatures = coordinateFeatures(ethaneAtoms(reference.torsion));
const referenceCandidate = deriveCandidate(referenceFeatures, referenceFeatures);
const referenceScore = scoreFamilyCandidate(referenceCandidate);
const angles = [0, 30, 60, 90, 120, 180, 240, 300];

const rows = angles.map((angle) => {
  const features = coordinateFeatures(ethaneAtoms(angle));
  const candidate = deriveCandidate(features, referenceFeatures);
  const familyScore = scoreFamilyCandidate(candidate);
  const genericScore = scoreCandidate(candidate);
  const penalty = referenceScore - familyScore;

  return {
    angle,
    expectedClass: expectedClass(angle),
    familyScore: round(familyScore),
    genericScore: round(genericScore),
    penaltyVsReference: round(penalty),
    torsionMean: round(candidate.coordinateMetrics.torsionMean, 2),
    torsionRms: round(candidate.coordinateMetrics.torsionRms, 3),
    torsionMax: round(candidate.coordinateMetrics.torsionMax, 3),
    stericClearance: round(candidate.coordinateMetrics.stericClearance, 4),
    stericObstruction: round(candidate.coordinateMetrics.steric, 3),
    geometryFit: round(candidate.geometryFit, 3),
    angleStrain: round(candidate.angleStrain, 3),
    routeContinuity: round(candidate.routeContinuity, 3),
  };
});

const eclipsedRows = rows.filter((row) => row.expectedClass === 'eclipsed-like');
const staggeredRows = rows.filter((row) => row.expectedClass === 'staggered-like');
const intermediateRows = rows.filter((row) => row.expectedClass === 'intermediate');
const weakestPenalty = Math.min(...eclipsedRows.map((row) => row.penaltyVsReference));
const meanEclipsedPenalty = average(eclipsedRows.map((row) => row.penaltyVsReference));
const meanStaggeredScore = average(staggeredRows.map((row) => row.familyScore));
const meanIntermediateScore = average(intermediateRows.map((row) => row.familyScore));
const meanEclipsedScore = average(eclipsedRows.map((row) => row.familyScore));

const diagnosis =
  weakestPenalty < 0.1
    ? 'weak torsion-phase separation: feature extraction sees the torsion change, but scoring still keeps eclipsed conformers close to the staggered reference'
    : 'torsion-phase separation is strong enough for the current control threshold';
const stericReading = rows.every((row) => row.stericObstruction === rows[0].stericObstruction)
  ? 'steric obstruction is flat across this torsion sweep, so H-H crowding is not yet being expressed by the current steric feature'
  : 'steric obstruction changes across this torsion sweep';
const nextReading = rows.every((row) => row.stericObstruction === rows[0].stericObstruction)
  ? 'The feature layer does detect torsion phase: eclipsed-like angles carry high torsion RMS relative to the staggered reference. The steric feature does not yet detect the expected H-H crowding difference across ethane conformers. That means the next modelling improvement should be feature extraction for rotatable non-bonded proximity before changing rotatable-covalent weights.'
  : 'The feature layer now detects both torsion phase and rotatable-group H-H proximity. Eclipsed-like angles carry high torsion RMS and higher steric obstruction relative to the staggered reference, so the weak generic ethane decoy was a feature-extraction issue rather than a reason to tune rotatable-covalent weights.';

const json = {
  source: 'ethane-torsion-sweep.mjs',
  status: 'focused ethane torsion diagnostic; not a molecule calibration anchor',
  reference: {
    angle: reference.torsion,
    score: round(referenceScore),
  },
  summary: {
    angles: rows.length,
    meanStaggeredScore: round(meanStaggeredScore),
    meanIntermediateScore: round(meanIntermediateScore),
    meanEclipsedScore: round(meanEclipsedScore),
    meanEclipsedPenalty: round(meanEclipsedPenalty),
    weakestEclipsedPenalty: round(weakestPenalty),
    diagnosis,
    stericReading,
  },
  rows,
};

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ethane-torsion-sweep.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate Ethane Torsion Sweep

## Scope

This report isolates the weak \`eclipsed C2H6\` decoy found by the coordinate bench.

It does not change molecule-family weights and does not add a new calibration anchor. It checks whether the current features and rotatable-covalent score separate staggered-like and eclipsed-like ethane conformers.

## Summary

| Metric | Value |
|---|---:|
| Reference angle | ${reference.torsion} |
| Reference score | ${round(referenceScore)} |
| Mean staggered-like score | ${round(meanStaggeredScore)} |
| Mean intermediate score | ${round(meanIntermediateScore)} |
| Mean eclipsed-like score | ${round(meanEclipsedScore)} |
| Mean eclipsed penalty | ${round(meanEclipsedPenalty)} |
| Weakest eclipsed penalty | ${round(weakestPenalty)} |

Diagnosis: ${diagnosis}.

Steric reading: ${stericReading}.

## Torsion Rows

| Torsion angle | Expected class | Family score | Generic score | Penalty vs reference | Torsion mean | Torsion RMS | Torsion max | Steric clearance | Steric obstruction | Geometry fit | Angle strain | Route continuity |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
${rows
  .map(
    (row) =>
      `| ${row.angle} | ${row.expectedClass} | ${row.familyScore} | ${row.genericScore} | ${row.penaltyVsReference} | ${row.torsionMean} | ${row.torsionRms} | ${row.torsionMax} | ${row.stericClearance} | ${row.stericObstruction} | ${row.geometryFit} | ${row.angleStrain} | ${row.routeContinuity} |`
  )
  .join('\n')}

## Reading

${nextReading}
`;

await writeFile(new URL('ethane-torsion-sweep.md', outDir), markdown);

console.log(`Angles tested: ${rows.length}`);
console.log(`Weakest eclipsed penalty: ${round(weakestPenalty)}`);
console.log(`Wrote ${new URL('ethane-torsion-sweep.md', outDir).pathname}`);
