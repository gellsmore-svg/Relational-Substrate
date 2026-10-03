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
const angles = Array.from(new Set([0, 30, 60, 75, 80, 85, 90, 95, 100, 105, 111.5, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 180])).sort(
  (a, b) => a - b
);

const releaseStrengths = [0, 0.25, 0.45, 0.55, 0.65, 0.75];
const releaseOnsets = [135, 145, 155, 165];
const releaseSpans = [20, 35, 50];

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

function deriveCandidate(features, referenceFeatures, release) {
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
  const antiPlanarRelease = clamp01((torsionMean - release.onset) / release.span) * clamp01(1 - stericDeviation) * clamp01(1 - cisCrowding);
  const effectiveTorsionRms = torsionRms * (1 - antiPlanarRelease * release.strength);
  const effectiveTorsionMax = torsionMax * (1 - antiPlanarRelease * release.strength);

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
      torsionMean,
      torsionRms,
      effectiveTorsionRms,
      steric: stericDeviation,
      cisCrowding,
      antiPlanarRelease,
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

function parameterKey(release) {
  return `strength=${release.strength};onset=${release.onset};span=${release.span}`;
}

function summarizeRelease(release, referenceFeatures) {
  const referenceCandidate = deriveCandidate(referenceFeatures, referenceFeatures, release);
  const referenceScore = scoreFamilyCandidate(referenceCandidate);
  const rows = angles.map((angle) => {
    const features = coordinateFeatures(peroxideAtoms(angle));
    const candidate = deriveCandidate(features, referenceFeatures, release);
    const familyScore = scoreFamilyCandidate(candidate);
    const distanceFromReference = Math.abs(angle - reference.torsion);
    return {
      angle,
      referenceBand: referenceBand(distanceFromReference),
      familyScore,
      genericScore: scoreCandidate(candidate),
      penaltyVsReference: referenceScore - familyScore,
      antiPlanarRelease: candidate.coordinateMetrics.antiPlanarRelease,
      effectiveTorsionRms: candidate.coordinateMetrics.effectiveTorsionRms,
    };
  });
  const bandSummary = ['near-reference', 'transition-shoulder', 'nonlocal'].map((band) => {
    const bandRows = rows.filter((row) => row.referenceBand === band);
    const weakest = bandRows.reduce((best, row) => (row.penaltyVsReference < best.penaltyVsReference ? row : best), bandRows[0]);
    return {
      band,
      rows: bandRows.length,
      weakestAngle: weakest.angle,
      weakestPenalty: weakest.penaltyVsReference,
      meanPenalty: average(bandRows.map((row) => row.penaltyVsReference)),
    };
  });
  const near = bandSummary.find((item) => item.band === 'near-reference');
  const shoulder = bandSummary.find((item) => item.band === 'transition-shoulder');
  const nonlocal = bandSummary.find((item) => item.band === 'nonlocal');
  const trans = rows.find((row) => row.angle === 180);
  const cis = rows.find((row) => row.angle === 0);
  const localDamage = Math.max(0, near.weakestPenalty - 0.05);
  const shoulderDamage = Math.max(0, shoulder.weakestPenalty - 0.08);
  const diagnosticScore = nonlocal.weakestPenalty - localDamage * 2 - shoulderDamage * 0.75;

  return {
    key: parameterKey(release),
    release,
    referenceScore: round(referenceScore),
    nearWeakest: round(near.weakestPenalty),
    shoulderWeakest: round(shoulder.weakestPenalty),
    nonlocalWeakest: round(nonlocal.weakestPenalty),
    nonlocalWeakestAngle: nonlocal.weakestAngle,
    transPenalty: round(trans.penaltyVsReference),
    cisPenalty: round(cis.penaltyVsReference),
    transAntiPlanarRelease: round(trans.antiPlanarRelease),
    transEffectiveTorsionRms: round(trans.effectiveTorsionRms),
    diagnosticScore: round(diagnosticScore),
    passShape: nonlocal.weakestPenalty >= 0.1 && near.weakestPenalty <= 0.05,
    bandSummary: bandSummary.map((item) => ({
      ...item,
      weakestPenalty: round(item.weakestPenalty),
      meanPenalty: round(item.meanPenalty),
    })),
  };
}

const referenceFeatures = coordinateFeatures(peroxideAtoms(reference.torsion));
const currentRelease = { strength: 0.65, onset: 145, span: 35 };
const releaseGrid = [];
for (const strength of releaseStrengths) {
  for (const onset of releaseOnsets) {
    for (const span of releaseSpans) {
      releaseGrid.push({ strength, onset, span });
    }
  }
}

const summaries = releaseGrid.map((release) => summarizeRelease(release, referenceFeatures));
const current = summaries.find((item) => item.key === parameterKey(currentRelease));
const ranked = [...summaries].sort(
  (a, b) =>
    Number(b.passShape) - Number(a.passShape) ||
    b.diagnosticScore - a.diagnosticScore ||
    b.nonlocalWeakest - a.nonlocalWeakest ||
    a.nearWeakest - b.nearWeakest
);
const topCandidates = ranked.slice(0, 12);
const topNonzeroCandidates = ranked.filter((item) => item.release.strength > 0).slice(0, 12);
const directionReading =
  topCandidates[0].release.strength === 0
    ? `removing the anti-planar release entirely gives the strongest separation; among nonzero alternatives, ${topNonzeroCandidates[0].key} is the least-disruptive repair direction`
    : topCandidates[0].release.strength < current.release.strength
      ? 'weaker anti-planar release is the dominant repair direction'
      : topCandidates[0].release.onset > current.release.onset
        ? 'later anti-planar onset is the dominant repair direction'
        : 'the current anti-planar release neighbourhood is not the dominant weakness';

const json = {
  source: 'peroxide-anti-planar-release-sensitivity.mjs',
  status: 'diagnostic-only parameter sensitivity; not a molecule model repair and not evidence',
  reference: {
    formula: reference.formula,
    angle: reference.torsion,
  },
  current,
  directionReading,
  grid: {
    strengths: releaseStrengths,
    onsets: releaseOnsets,
    spans: releaseSpans,
    rows: summaries.length,
  },
  topCandidates,
  topNonzeroCandidates,
  summaries,
};

await mkdir(outDir, { recursive: true });
await writeFile(new URL('peroxide-anti-planar-release-sensitivity.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate Peroxide Anti-Planar Release Sensitivity

## Scope

This is a diagnostic-only sweep over the peroxide torsion anti-planar release term.

It does not change the molecule model, does not alter family weights, and does not add evidence. Its purpose is to identify why the current nonlocal peroxide torsion frontier remains weak: the 180 degree trans-like row is too close to the 111.5 degree reference after anti-planar release reduces the effective torsion penalty.

## Current Setting

| Strength | Onset | Span | Near weakest | Shoulder weakest | Nonlocal weakest | Weakest nonlocal angle | Trans penalty | Trans release | Trans effective torsion RMS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ${current.release.strength} | ${current.release.onset} | ${current.release.span} | ${current.nearWeakest} | ${current.shoulderWeakest} | ${current.nonlocalWeakest} | ${current.nonlocalWeakestAngle} | ${current.transPenalty} | ${current.transAntiPlanarRelease} | ${current.transEffectiveTorsionRms} |

Reading: ${directionReading}.

## Top Diagnostic Candidates

Ranked by: first preserve the local window shape, then increase nonlocal separation, then avoid over-penalising the shoulder.

| Rank | Strength | Onset | Span | Near weakest | Shoulder weakest | Nonlocal weakest | Weakest nonlocal angle | Trans penalty | Trans release | Trans effective torsion RMS | Shape pass | Diagnostic score |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
${topCandidates
  .map(
    (item, index) =>
      `| ${index + 1} | ${item.release.strength} | ${item.release.onset} | ${item.release.span} | ${item.nearWeakest} | ${item.shoulderWeakest} | ${item.nonlocalWeakest} | ${item.nonlocalWeakestAngle} | ${item.transPenalty} | ${item.transAntiPlanarRelease} | ${item.transEffectiveTorsionRms} | ${item.passShape ? 'yes' : 'no'} | ${item.diagnosticScore} |`
  )
  .join('\n')}

## Least-Disruptive Nonzero Candidates

These retain an anti-planar release term but reduce or delay its effect enough to clear the nonlocal separation shape.

| Rank | Strength | Onset | Span | Near weakest | Shoulder weakest | Nonlocal weakest | Weakest nonlocal angle | Trans penalty | Trans release | Trans effective torsion RMS | Shape pass | Diagnostic score |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
${topNonzeroCandidates
  .map(
    (item, index) =>
      `| ${index + 1} | ${item.release.strength} | ${item.release.onset} | ${item.release.span} | ${item.nearWeakest} | ${item.shoulderWeakest} | ${item.nonlocalWeakest} | ${item.nonlocalWeakestAngle} | ${item.transPenalty} | ${item.transAntiPlanarRelease} | ${item.transEffectiveTorsionRms} | ${item.passShape ? 'yes' : 'no'} | ${item.diagnosticScore} |`
  )
  .join('\n')}

## Reading

The current setting preserves a sensible local tolerance window but lets the trans-like 180 degree row recover too much route coherence. Full removal of the release term is the strongest mathematical fix, but that may be too blunt physically because it erases the intended distinction between crowded cis compression and uncrowded trans-like release. The least-disruptive nonzero alternatives point to a smaller release strength and/or later onset, so uncrowded trans-like rows remain nonlocal while near-reference rows remain local.

Any promotion from this diagnostic would require a separate predeclared repair: frozen release formula, coefficient/onset/span, held-out rotor target, and pass/fail criteria before lookup.
`;

await writeFile(new URL('peroxide-anti-planar-release-sensitivity.md', outDir), markdown);

console.log(`Release settings tested: ${summaries.length}`);
console.log(`Current nonlocal weakest: ${current.nonlocalWeakest}`);
console.log(`Top diagnostic candidate: ${topCandidates[0].key}`);
