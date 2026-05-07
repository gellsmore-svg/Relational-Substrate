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
  family: 'rotatable covalent',
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
  const routeContinuity = clamp01(reference.routeBase - bondRms * 0.08 - angleRms * 0.08 - effectiveTorsionRms * 0.16 - stericDeviation * 0.08 - cisCrowding * 0.18);
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
      torsionMean,
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

function expectedClass(angle) {
  if (angle === 0 || angle === 180) {
    return 'planar-extreme';
  }
  if (angle === 90 || angle === 120) {
    return 'skew-like';
  }
  return 'intermediate';
}

function round(value, digits = 4) {
  return Number(value.toFixed(digits));
}

const referenceFeatures = coordinateFeatures(peroxideAtoms(reference.torsion));
const referenceCandidate = deriveCandidate(referenceFeatures, referenceFeatures);
const referenceScore = scoreFamilyCandidate(referenceCandidate);
const angles = [0, 30, 60, 90, 111.5, 120, 150, 180];
const nearReferenceWindow = 15;

const rows = angles.map((angle) => {
  const features = coordinateFeatures(peroxideAtoms(angle));
  const candidate = deriveCandidate(features, referenceFeatures);
  const familyScore = scoreFamilyCandidate(candidate);
  const genericScore = scoreCandidate(candidate);
  const penalty = referenceScore - familyScore;
  const referenceDistance = Math.abs(angle - reference.torsion);

  return {
    angle,
    expectedClass: expectedClass(angle),
    referenceDistance: round(referenceDistance, 1),
    referenceBand: angle === reference.torsion ? 'reference' : referenceDistance <= nearReferenceWindow ? 'near-reference' : 'nonlocal',
    familyScore: round(familyScore),
    genericScore: round(genericScore),
    penaltyVsReference: round(penalty),
    torsionMean: round(candidate.coordinateMetrics.torsionMean, 2),
    torsionRms: round(candidate.coordinateMetrics.torsionRms, 3),
    effectiveTorsionRms: round(candidate.coordinateMetrics.effectiveTorsionRms, 3),
    torsionMax: round(candidate.coordinateMetrics.torsionMax, 3),
    stericClearance: round(candidate.coordinateMetrics.stericClearance, 4),
    stericObstruction: round(candidate.coordinateMetrics.steric, 3),
    cisCrowding: round(candidate.coordinateMetrics.cisCrowding, 3),
    antiPlanarRelease: round(candidate.coordinateMetrics.antiPlanarRelease, 3),
    polarityDeviation: round(candidate.coordinateMetrics.polarityDeviation, 3),
    geometryFit: round(candidate.geometryFit, 3),
    angleStrain: round(candidate.angleStrain, 3),
    routeContinuity: round(candidate.routeContinuity, 3),
  };
});

const referenceRow = rows.find((row) => row.angle === reference.torsion);
const nearReferenceRows = rows.filter((row) => row.referenceBand === 'near-reference');
const lowestNearReferencePenalty = nearReferenceRows.length ? Math.min(...nearReferenceRows.map((row) => row.penaltyVsReference)) : null;
const nonLocalRows = rows.filter((row) => row.referenceBand === 'nonlocal');
const lowestNonLocalPenalty = Math.min(...nonLocalRows.map((row) => row.penaltyVsReference));
const planarRows = rows.filter((row) => row.expectedClass === 'planar-extreme');
const skewRows = rows.filter((row) => row.expectedClass === 'skew-like');
const diagnosis =
  lowestNonLocalPenalty < 0.08
    ? 'weak peroxide torsion separation: nonlocal torsions remain too close to the reference'
    : 'peroxide torsion separation is visible once near-reference neighbours are distinguished from real decoys';

const json = {
  source: 'peroxide-torsion-sweep.mjs',
  status: 'focused peroxide torsion diagnostic; not a molecule calibration anchor',
  reference: {
    angle: reference.torsion,
    score: round(referenceScore),
  },
  summary: {
    angles: rows.length,
    referenceScore: referenceRow.familyScore,
    meanPlanarExtremeScore: round(average(planarRows.map((row) => row.familyScore))),
    meanSkewLikeScore: round(average(skewRows.map((row) => row.familyScore))),
    nearReferenceWindow,
    lowestNearReferencePenalty: lowestNearReferencePenalty === null ? null : round(lowestNearReferencePenalty),
    lowestNonLocalPenalty: round(lowestNonLocalPenalty),
    frontierPenalty: round(lowestNonLocalPenalty),
    diagnosis,
  },
  rows,
};

await mkdir(outDir, { recursive: true });
await writeFile(new URL('peroxide-torsion-sweep.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate Peroxide Torsion Sweep

## Scope

This report checks whether the rotatable-group steric feature also behaves sensibly for \`H2O2\`.

It does not change molecule-family weights and does not add a new calibration anchor. It compares planar-extreme, intermediate, and skew-like peroxide torsion angles around the rounded gas-phase reference. It also reports cis-crowding pressure for low-torsion, close-H-H rows.

## Summary

| Metric | Value |
|---|---:|
| Reference angle | ${reference.torsion} |
| Reference score | ${round(referenceScore)} |
| Mean planar-extreme score | ${round(average(planarRows.map((row) => row.familyScore)))} |
| Mean skew-like score | ${round(average(skewRows.map((row) => row.familyScore)))} |
| Near-reference window | ${nearReferenceWindow} degrees |
| Lowest near-reference penalty | ${lowestNearReferencePenalty === null ? 'n/a' : round(lowestNearReferencePenalty)} |
| Lowest nonlocal penalty | ${round(lowestNonLocalPenalty)} |
| Frontier penalty | ${round(lowestNonLocalPenalty)} |

Diagnosis: ${diagnosis}.

## Torsion Rows

| Torsion angle | Expected class | Reference band | Distance from reference | Family score | Generic score | Penalty vs reference | Torsion mean | Torsion RMS | Effective torsion RMS | Steric clearance | Steric obstruction | Cis crowding | Anti-planar release | Polarity deviation | Geometry fit | Angle strain | Route continuity |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
${rows
  .map(
    (row) =>
      `| ${row.angle} | ${row.expectedClass} | ${row.referenceBand} | ${row.referenceDistance} | ${row.familyScore} | ${row.genericScore} | ${row.penaltyVsReference} | ${row.torsionMean} | ${row.torsionRms} | ${row.effectiveTorsionRms} | ${row.stericClearance} | ${row.stericObstruction} | ${row.cisCrowding} | ${row.antiPlanarRelease} | ${row.polarityDeviation} | ${row.geometryFit} | ${row.angleStrain} | ${row.routeContinuity} |`
  )
  .join('\n')}

## Reading

The peroxide case is not an ethane clone: torsion changes also shift polarity and H-H separation. Rows inside the near-reference window should be read as local tolerance neighbours, not hard decoys. The frontier penalty is therefore the lowest nonlocal penalty. Cis crowding prevents planar cis compression from being hidden inside a single saturated steric channel; anti-planar release prevents uncrowded trans-like routes from inheriting the same saturated closure penalty as crowded cis routes.
`;

await writeFile(new URL('peroxide-torsion-sweep.md', outDir), markdown);

console.log(`Angles tested: ${rows.length}`);
console.log(`Lowest nonlocal penalty: ${round(lowestNonLocalPenalty)}`);
console.log(`Wrote ${new URL('peroxide-torsion-sweep.md', outDir).pathname}`);
