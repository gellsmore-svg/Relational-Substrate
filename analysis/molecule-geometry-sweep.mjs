import { mkdir, writeFile } from 'node:fs/promises';
import { deriveCandidateFromGeometry, geometryMolecules, scoreCandidate } from './molecule-model.mjs';

const outDir = new URL('./out/', import.meta.url);

const perturbations = [
  { key: 'bondLength', label: 'bond-length', unit: 'angstrom' },
  { key: 'bondAngle', label: 'bond-angle', unit: 'degree' },
  { key: 'torsion', label: 'torsion', unit: 'degree' },
  { key: 'ringClosureDistance', label: 'ring-closure-distance', unit: 'angstrom' },
  { key: 'polarityVector', label: 'polarity-vector', unit: 'relative' },
  { key: 'stericClearance', label: 'steric-clearance', unit: 'angstrom' },
  { key: 'valenceMismatch', label: 'valence-mismatch', unit: 'relative' },
];

const levels = [
  { label: 'minus-strong', value: -2 },
  { label: 'minus-mild', value: -1 },
  { label: 'reference', value: 0 },
  { label: 'plus-mild', value: 1 },
  { label: 'plus-strong', value: 2 },
];

function* tuples(length, prefix = []) {
  if (prefix.length === length) {
    yield prefix;
    return;
  }

  for (const level of levels) {
    yield* tuples(length, [...prefix, level]);
  }
}

function applyGeometryLevel(molecule, geometry, perturbation, level) {
  const expected = molecule.reference[perturbation.key];
  if (expected === null) {
    return geometry;
  }

  const next = { ...geometry };
  const tolerance = molecule.tolerances[perturbation.key];
  const signedStep = level.value * tolerance * 0.5;

  if (perturbation.key === 'stericClearance') {
    next[perturbation.key] = Math.max(0, expected + signedStep);
    return next;
  }

  if (perturbation.key === 'valenceMismatch') {
    next[perturbation.key] = Math.max(0, expected + Math.abs(level.value) * 0.5);
    return next;
  }

  if (perturbation.key === 'polarityVector') {
    next[perturbation.key] = Math.max(0, expected + signedStep);
    return next;
  }

  next[perturbation.key] = expected + signedStep;
  return next;
}

function geometryKey(row) {
  return [
    row.score.toFixed(4),
    row.geometry.bondLength?.toFixed(3) ?? 'na',
    row.geometry.bondAngle?.toFixed(2) ?? 'na',
    row.geometry.torsion?.toFixed(2) ?? 'na',
    row.geometry.ringClosureDistance?.toFixed(3) ?? 'na',
    row.geometry.polarityVector?.toFixed(3) ?? 'na',
    row.geometry.stericClearance?.toFixed(3) ?? 'na',
    row.geometry.valenceMismatch?.toFixed(3) ?? 'na',
  ].join('|');
}

function uniqueRows(rows, limit) {
  const seen = new Set();
  const unique = [];

  for (const row of rows) {
    const key = geometryKey(row);
    if (seen.has(key)) {
      continue;
    }
    seen.add(key);
    unique.push(row);
    if (unique.length === limit) {
      break;
    }
  }

  return unique;
}

function compact(row) {
  return {
    name: row.name,
    score: Number(row.score.toFixed(4)),
    changedGeometryFields: row.changedGeometryFields,
    maxLevel: row.maxLevel,
    geometry: {
      bondLength: row.geometry.bondLength,
      bondAngle: row.geometry.bondAngle,
      torsion: row.geometry.torsion,
      ringClosureDistance: row.geometry.ringClosureDistance,
      polarityVector: row.geometry.polarityVector,
      stericClearance: row.geometry.stericClearance,
      valenceMismatch: row.geometry.valenceMismatch,
    },
    derived: {
      valenceSatisfaction: Number(row.valenceSatisfaction.toFixed(3)),
      geometryFit: Number(row.geometryFit.toFixed(3)),
      angleStrain: Number(row.angleStrain.toFixed(3)),
      bondStrain: Number(row.bondStrain.toFixed(3)),
      polarityBalance: Number(row.polarityBalance.toFixed(3)),
      routeContinuity: Number(row.routeContinuity.toFixed(3)),
      ringClosure: Number(row.ringClosure.toFixed(3)),
      stericObstruction: Number(row.stericObstruction.toFixed(3)),
    },
  };
}

const globalFieldCounts = Object.fromEntries(perturbations.map((item) => [item.label, 0]));
const globalLevelCounts = Object.fromEntries(levels.map((level) => [level.label, 0]));
let totalIterations = 0;
const results = [];

for (const molecule of geometryMolecules) {
  const rows = [];
  const fieldCounts = Object.fromEntries(perturbations.map((item) => [item.label, 0]));
  const levelCounts = Object.fromEntries(levels.map((level) => [level.label, 0]));

  for (const tuple of tuples(perturbations.length)) {
    let geometry = { ...molecule.reference };
    let changedGeometryFields = 0;
    let maxLevelMagnitude = 0;
    let maxLevel = 'reference';
    const changes = {};

    tuple.forEach((level, index) => {
      const perturbation = perturbations[index];
      const isApplicable = molecule.reference[perturbation.key] !== null;
      changes[perturbation.label] = isApplicable ? level.label : 'not-applicable';

      if (!isApplicable) {
        return;
      }

      levelCounts[level.label] += 1;
      globalLevelCounts[level.label] += 1;

      if (level.value !== 0) {
        changedGeometryFields += 1;
        fieldCounts[perturbation.label] += 1;
        globalFieldCounts[perturbation.label] += 1;
      }

      if (Math.abs(level.value) > maxLevelMagnitude) {
        maxLevelMagnitude = Math.abs(level.value);
        maxLevel = level.label;
      }

      geometry = applyGeometryLevel(molecule, geometry, perturbation, level);
    });

    const candidate = deriveCandidateFromGeometry(molecule, geometry, {
      name: changedGeometryFields === 0 ? 'reference geometry' : `${changedGeometryFields}-field geometry`,
      type: changedGeometryFields === 0 ? 'reference' : 'generated',
      mode: 'geometry',
    });

    rows.push({
      ...candidate,
      score: scoreCandidate(candidate),
      changes,
      changedGeometryFields,
      maxLevel,
    });
    totalIterations += 1;
  }

  const ranked = rows.sort((a, b) => b.score - a.score || a.changedGeometryFields - b.changedGeometryFields);
  const referenceScore = scoreCandidate(deriveCandidateFromGeometry(molecule, molecule.reference, { type: 'reference' }));
  const referenceRank = ranked.findIndex((row) => row.type === 'reference') + 1;
  const aboveReference = ranked.filter((row) => row.score > referenceScore).length;
  const withinFivePercent = ranked.filter((row) => row.score >= referenceScore * 0.95).length;
  const strongFailures = ranked.filter((row) => row.score < 0.55).length;

  results.push({
    formula: molecule.formula,
    iterations: rows.length,
    referenceScore,
    referenceRank,
    aboveReference,
    withinFivePercent,
    strongFailures,
    fieldCounts,
    levelCounts,
    top: uniqueRows(ranked, 12).map(compact),
    bottom: uniqueRows([...ranked].reverse(), 12).map(compact),
  });
}

const summary = {
  totalIterations,
  molecules: geometryMolecules.length,
  fields: perturbations.map((item) => item.label),
  levels: levels.map((level) => level.label),
  globalFieldCounts,
  globalLevelCounts,
  results,
};

await mkdir(outDir, { recursive: true });
await writeFile(new URL('molecule-geometry-sweep.json', outDir), JSON.stringify(summary, null, 2));

const markdown = `# AMS Molecule Geometry Sweep

## Scope

This sweep perturbs explicit geometry fields and derives coherence variables from the resulting geometry. It is still a secondary-regime coherence bench, not a claim that atoms are vorton species.

Perturbed geometry fields:

${perturbations.map((item) => `- ${item.label} (${item.unit})`).join('\n')}

## Scale

Molecules tested: ${geometryMolecules.length}

Total geometry iterations tried: ${totalIterations}

Levels per field: ${levels.map((level) => level.label).join(', ')}

## Global Field Counts

This counts non-reference perturbations for applicable fields.

| Field | Non-reference applications |
|---|---:|
${Object.entries(globalFieldCounts)
  .map(([field, count]) => `| ${field} | ${count} |`)
  .join('\n')}

## Global Level Counts

This counts applicable field assignments.

| Level | Count |
|---|---:|
${Object.entries(globalLevelCounts)
  .map(([level, count]) => `| ${level} | ${count} |`)
  .join('\n')}

## Molecule Results

| Molecule | Iterations | Reference rank | Reference score | Above reference | Within 95% | Strong failures |
|---|---:|---:|---:|---:|---:|---:|
${results
  .map(
    (result) =>
      `| ${result.formula} | ${result.iterations} | ${result.referenceRank} | ${result.referenceScore.toFixed(4)} | ${result.aboveReference} | ${result.withinFivePercent} | ${result.strongFailures} |`
  )
  .join('\n')}

## Top Geometry Candidates

${results
  .map(
    (result) => `### ${result.formula}

| Rank | Candidate | Score | Changed fields | Max level | Bond length | Bond angle | Torsion | Ring closure dist | Polarity | Steric clearance | Valence mismatch | Geometry fit | Route | Bond strain | Angle strain |
|---:|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
${result.top
  .map(
    (row, index) =>
      `| ${index + 1} | ${row.name} | ${row.score} | ${row.changedGeometryFields} | ${row.maxLevel} | ${row.geometry.bondLength ?? 'n/a'} | ${row.geometry.bondAngle ?? 'n/a'} | ${row.geometry.torsion ?? 'n/a'} | ${row.geometry.ringClosureDistance ?? 'n/a'} | ${row.geometry.polarityVector ?? 'n/a'} | ${row.geometry.stericClearance ?? 'n/a'} | ${row.geometry.valenceMismatch ?? 'n/a'} | ${row.derived.geometryFit} | ${row.derived.routeContinuity} | ${row.derived.bondStrain} | ${row.derived.angleStrain} |`
  )
  .join('\n')}`
  )
  .join('\n\n')}

## First Reading

This is a stronger bench than the abstract perturbation sweep because coherence variables are now derived from candidate geometry fields.

The current geometry model is still coarse. It uses averaged bond length and representative angles rather than full atomic coordinates. The next step is to introduce actual coordinate sets and derive bond lengths, angles, torsions, closure distances, polarity vectors, and steric clearances from coordinates.
`;

await writeFile(new URL('molecule-geometry-sweep-summary.md', outDir), markdown);

console.log(`Molecules tested: ${geometryMolecules.length}`);
console.log(`Total geometry iterations tried: ${totalIterations}`);
console.log(`Wrote ${new URL('molecule-geometry-sweep-summary.md', outDir).pathname}`);
