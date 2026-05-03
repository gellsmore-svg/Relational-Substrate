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
  formula: 'H2O2',
  bondLength: 1.475,
  bondAngle: 94.8,
  torsion: 111.5,
  routeBase: 0.7,
};

const tolerances = {
  bondLength: 0.2,
  bondAngle: 28,
  torsion: 45,
  polarityVector: 0.85,
  stericClearance: 0.5,
};

const nearReferenceWindow = 15;
const shoulderWindow = 35;

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

function peroxideAtoms(torsionDegreesValue) {
  const oo = reference.bondLength;
  const oh = 0.967;
  const angle = (reference.bondAngle * Math.PI) / 180;
  const torsion = (torsionDegreesValue * Math.PI) / 180;
  const xOffset = Math.cos(angle) * oh;
  const radial = Math.sin(angle) * oh;

  return [
    { element: 'O', partialCharge: -0.35, position: vec(-oo / 2, 0, 0) },
    { element: 'O', partialCharge: -0.35, position: vec(oo / 2, 0, 0) },
    { element: 'H', partialCharge: 0.35, position: vec(-oo / 2 - xOffset, radial, 0) },
    { element: 'H', partialCharge: 0.35, position: vec(oo / 2 + xOffset, Math.cos(torsion) * radial, Math.sin(torsion) * radial) },
  ];
}

function cyclicDifference(value, target, period = 360) {
  const raw = Math.abs(((value - target + period / 2) % period) - period / 2);
  return Math.min(raw, period - raw);
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
  const chargeCentre = atoms.reduce(
    (sum, atom) => vec(sum.x + atom.position.x * atom.partialCharge, sum.y + atom.position.y * atom.partialCharge, sum.z + atom.position.z * atom.partialCharge),
    vec(0, 0, 0)
  );

  return {
    bondLengths,
    angles: angleValues,
    torsions: torsionValues,
    polarityVector: norm(chargeCentre),
    stericClearance: distance(atoms[2].position, atoms[3].position),
  };
}

function deriveCandidate(features, referenceFeatures) {
  const bondDeviations = features.bondLengths.map((length, index) => clamp01(Math.abs(length - referenceFeatures.bondLengths[index]) / tolerances.bondLength));
  const angleDeviations = features.angles.map((angle, index) => clamp01(Math.abs(angle - referenceFeatures.angles[index]) / tolerances.bondAngle));
  const torsionDeviations = features.torsions.map((torsion) => clamp01(cyclicDifference(torsion, reference.torsion) / tolerances.torsion));
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

  const bondStrain = clamp01(bondRms * 0.65 + bondMax * 0.2);
  const angleStrain = clamp01(angleRms * 0.42 + angleMax * 0.16 + torsionRms * 0.3 + torsionMax * 0.08 + stericDeviation * 0.04 + cisCrowding * 0.48);
  const geometryFit = clamp01(1 - (bondRms * 0.18 + bondMax * 0.08 + angleRms * 0.18 + angleMax * 0.07 + torsionRms * 0.24 + stericDeviation * 0.18 + cisCrowding * 0.36));
  const routeContinuity = clamp01(reference.routeBase - bondRms * 0.08 - angleRms * 0.08 - torsionRms * 0.16 - stericDeviation * 0.08 - cisCrowding * 0.18);
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
      angleRms,
      torsionRms,
      torsionMean,
      steric: stericDeviation,
      cisCrowding,
      stericClearance: features.stericClearance,
      polarityDeviation,
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

function referenceBand(distanceFromReference) {
  if (distanceFromReference === 0) {
    return 'reference';
  }
  if (distanceFromReference <= nearReferenceWindow) {
    return 'near-reference';
  }
  if (distanceFromReference <= shoulderWindow) {
    return 'transition-shoulder';
  }
  return 'nonlocal';
}

function round(value, digits = 4) {
  return Number(value.toFixed(digits));
}

const referenceFeatures = coordinateFeatures(peroxideAtoms(reference.torsion));
const referenceCandidate = deriveCandidate(referenceFeatures, referenceFeatures);
const referenceScore = scoreFamilyCandidate(referenceCandidate);
const angles = Array.from(new Set([0, 30, 60, 75, 80, 85, 90, 95, 100, 105, 111.5, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 180])).sort(
  (a, b) => a - b
);

const rows = angles.map((angle) => {
  const features = coordinateFeatures(peroxideAtoms(angle));
  const candidate = deriveCandidate(features, referenceFeatures);
  const familyScore = scoreFamilyCandidate(candidate);
  const distanceFromReference = Math.abs(angle - reference.torsion);

  return {
    angle,
    referenceDistance: round(distanceFromReference, 1),
    referenceBand: referenceBand(distanceFromReference),
    familyScore: round(familyScore),
    genericScore: round(scoreCandidate(candidate)),
    penaltyVsReference: round(referenceScore - familyScore),
    torsionMean: round(candidate.coordinateMetrics.torsionMean, 2),
    torsionRms: round(candidate.coordinateMetrics.torsionRms, 3),
    stericClearance: round(candidate.coordinateMetrics.stericClearance, 4),
    stericObstruction: round(candidate.coordinateMetrics.steric, 3),
    cisCrowding: round(candidate.coordinateMetrics.cisCrowding, 3),
    polarityDeviation: round(candidate.coordinateMetrics.polarityDeviation, 3),
    geometryFit: round(candidate.geometryFit, 3),
    angleStrain: round(candidate.angleStrain, 3),
    routeContinuity: round(candidate.routeContinuity, 3),
  };
});

const byBand = ['near-reference', 'transition-shoulder', 'nonlocal'].map((band) => {
  const bandRows = rows.filter((row) => row.referenceBand === band);
  const weakest = bandRows.reduce((best, row) => (row.penaltyVsReference < best.penaltyVsReference ? row : best), bandRows[0]);

  return {
    band,
    rows: bandRows.length,
    weakestAngle: weakest.angle,
    weakestPenalty: weakest.penaltyVsReference,
    meanPenalty: round(average(bandRows.map((row) => row.penaltyVsReference))),
  };
});

const nonlocal = byBand.find((item) => item.band === 'nonlocal');
const shoulder = byBand.find((item) => item.band === 'transition-shoulder');
const diagnosis =
  nonlocal.weakestPenalty < 0.1
    ? 'weak peroxide nonlocal separation: true nonlocal torsions remain too close to the reference'
    : shoulder.weakestPenalty < 0.08
      ? 'peroxide has a narrow transition shoulder near the reference but true nonlocal torsions separate'
      : 'peroxide nonlocal torsions separate once the transition shoulder is not treated as a hard decoy';

const json = {
  source: 'peroxide-nonlocal-refinement.mjs',
  status: 'focused peroxide nonlocal torsion refinement; not a molecule calibration anchor',
  reference: {
    angle: reference.torsion,
    score: round(referenceScore),
  },
  summary: {
    angles: rows.length,
    nearReferenceWindow,
    shoulderWindow,
    byBand,
    frontierPenalty: nonlocal.weakestPenalty,
    diagnosis,
  },
  rows,
};

await mkdir(outDir, { recursive: true });
await writeFile(new URL('peroxide-nonlocal-refinement.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# AMS Peroxide Nonlocal Refinement

## Scope

This report refines the weakest current molecule frontier: peroxide torsion outside the near-reference window.

It does not change molecule-family weights and does not add a new calibration anchor. It separates local tolerance neighbours, a transition shoulder, and true nonlocal torsions on a denser torsion grid. It also reports cis-crowding pressure for low-torsion, close-H-H peroxide rows.

## Summary

Diagnosis: ${diagnosis}.

| Band | Rows | Weakest angle | Weakest penalty | Mean penalty |
|---|---:|---:|---:|---:|
${byBand.map((item) => `| ${item.band} | ${item.rows} | ${item.weakestAngle} | ${item.weakestPenalty} | ${item.meanPenalty} |`).join('\n')}

## Torsion Rows

| Torsion angle | Reference band | Distance from reference | Family score | Generic score | Penalty vs reference | Torsion RMS | Steric clearance | Steric obstruction | Cis crowding | Polarity deviation | Geometry fit | Angle strain | Route continuity |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
${rows
  .map(
    (row) =>
      `| ${row.angle} | ${row.referenceBand} | ${row.referenceDistance} | ${row.familyScore} | ${row.genericScore} | ${row.penaltyVsReference} | ${row.torsionRms} | ${row.stericClearance} | ${row.stericObstruction} | ${row.cisCrowding} | ${row.polarityDeviation} | ${row.geometryFit} | ${row.angleStrain} | ${row.routeContinuity} |`
  )
  .join('\n')}

## Reading

The useful distinction is not reference versus every other angle. Peroxide has a local tolerance zone near 111.5 degrees, a transition shoulder where route memory is still partially coherent, and true nonlocal torsions that should carry a clearer penalty. The cis-crowding term prevents planar cis compression from being hidden inside a single saturated steric channel.
`;

await writeFile(new URL('peroxide-nonlocal-refinement.md', outDir), markdown);

console.log(`Angles tested: ${rows.length}`);
console.log(`Frontier penalty: ${nonlocal.weakestPenalty}`);
console.log(`Diagnosis: ${diagnosis}`);
