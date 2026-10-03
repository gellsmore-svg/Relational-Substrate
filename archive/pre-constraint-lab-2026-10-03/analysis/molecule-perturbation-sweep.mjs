import { mkdir, writeFile } from 'node:fs/promises';
import { clamp01, molecules, scoreCandidate } from './molecule-model.mjs';

const outDir = new URL('./out/', import.meta.url);

const categories = [
  'bond-length',
  'bond-angle',
  'route-continuity',
  'polarity-storage',
  'ring-closure',
  'steric-pressure',
  'valence-coupling',
];

const degradationLevels = [
  { label: 'none', value: 0 },
  { label: 'mild', value: 1 },
  { label: 'moderate', value: 2 },
  { label: 'strong', value: 3 },
  { label: 'extreme', value: 4 },
];

const tradeoffLevels = [
  { label: 'improve-moderate', value: -2 },
  { label: 'improve-mild', value: -1 },
  { label: 'neutral', value: 0 },
  { label: 'degrade-mild', value: 1 },
  { label: 'degrade-moderate', value: 2 },
];

function adjust(candidate, key, delta) {
  candidate[key] = clamp01(candidate[key] + delta);
}

function applyCategoryAdjustment(reference, category, level) {
  const next = { ...reference };
  const amount = Math.abs(level.value);
  const direction = Math.sign(level.value);

  if (direction === 0) {
    return next;
  }

  const degrade = direction > 0;
  const sign = degrade ? 1 : -1;

  if (category === 'bond-length') {
    adjust(next, 'bondStrain', sign * amount * 0.13);
    adjust(next, 'geometryFit', -sign * amount * 0.035);
    adjust(next, 'routeContinuity', -sign * amount * 0.025);
  }

  if (category === 'bond-angle') {
    adjust(next, 'angleStrain', sign * amount * 0.14);
    adjust(next, 'geometryFit', -sign * amount * 0.06);
    adjust(next, 'stericObstruction', sign * amount * 0.025);
  }

  if (category === 'route-continuity') {
    adjust(next, 'routeContinuity', -sign * amount * 0.12);
    adjust(next, 'polarityBalance', -sign * amount * 0.025);
  }

  if (category === 'polarity-storage') {
    adjust(next, 'polarityBalance', -sign * amount * 0.11);
    adjust(next, 'routeContinuity', -sign * amount * 0.018);
  }

  if (category === 'ring-closure') {
    if (reference.ringClosure > 0) {
      adjust(next, 'ringClosure', -sign * amount * 0.17);
      adjust(next, 'routeContinuity', -sign * amount * 0.055);
    } else {
      adjust(next, 'geometryFit', -sign * amount * 0.025);
      adjust(next, 'stericObstruction', sign * amount * 0.02);
    }
  }

  if (category === 'steric-pressure') {
    adjust(next, 'stericObstruction', sign * amount * 0.15);
    adjust(next, 'geometryFit', -sign * amount * 0.035);
    adjust(next, 'angleStrain', sign * amount * 0.035);
  }

  if (category === 'valence-coupling') {
    adjust(next, 'valenceSatisfaction', -sign * amount * 0.11);
    adjust(next, 'routeContinuity', -sign * amount * 0.045);
  }

  return next;
}

function* tuples(levels, length, prefix = []) {
  if (prefix.length === length) {
    yield prefix;
    return;
  }

  for (const level of levels) {
    yield* tuples(levels, length, [...prefix, level]);
  }
}

function compact(row) {
  return {
    name: row.name,
    mode: row.mode,
    score: Number(row.score.toFixed(4)),
    changedCategories: row.changedCategories,
    improvedCategories: row.improvedCategories,
    degradedCategories: row.degradedCategories,
    maxLevel: row.maxLevel,
    valenceSatisfaction: Number(row.valenceSatisfaction.toFixed(3)),
    geometryFit: Number(row.geometryFit.toFixed(3)),
    angleStrain: Number(row.angleStrain.toFixed(3)),
    bondStrain: Number(row.bondStrain.toFixed(3)),
    polarityBalance: Number(row.polarityBalance.toFixed(3)),
    routeContinuity: Number(row.routeContinuity.toFixed(3)),
    ringClosure: Number(row.ringClosure.toFixed(3)),
    stericObstruction: Number(row.stericObstruction.toFixed(3)),
  };
}

function profileKey(row) {
  return [
    row.score.toFixed(4),
    row.changedCategories,
    row.improvedCategories,
    row.degradedCategories,
    row.valenceSatisfaction.toFixed(3),
    row.geometryFit.toFixed(3),
    row.angleStrain.toFixed(3),
    row.bondStrain.toFixed(3),
    row.polarityBalance.toFixed(3),
    row.routeContinuity.toFixed(3),
    row.ringClosure.toFixed(3),
    row.stericObstruction.toFixed(3),
  ].join('|');
}

function uniqueProfiles(rows, limit) {
  const seen = new Set();
  const unique = [];

  for (const row of rows) {
    const key = profileKey(row);
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

function emptyCounts(keys) {
  return Object.fromEntries(keys.map((key) => [key, 0]));
}

const globalCategoryCounts = emptyCounts(categories);
const globalLevelCounts = emptyCounts([...degradationLevels.map((level) => level.label), ...tradeoffLevels.map((level) => level.label)]);
const globalDirectionCounts = { neutral: 0, improve: 0, degrade: 0 };
const globalModeCounts = { degradation: 0, tradeoff: 0 };
let skippedPureTradeoffRows = 0;

let totalIterations = 0;
const results = [];

function addLevelCounts(level, category, counts) {
  const direction = Math.sign(level.value);
  counts.levelCounts[level.label] += 1;
  globalLevelCounts[level.label] += 1;

  if (direction === 0) {
    counts.directionCounts.neutral += 1;
    globalDirectionCounts.neutral += 1;
    return;
  }

  globalCategoryCounts[category] += 1;
  counts.categoryCounts[category] += 1;

  if (direction < 0) {
    counts.directionCounts.improve += 1;
    globalDirectionCounts.improve += 1;
  } else {
    counts.directionCounts.degrade += 1;
    globalDirectionCounts.degrade += 1;
  }
}

function buildRowsForMode(molecule, mode, levels, counts) {
  const rows = [];

  for (const tuple of tuples(levels, categories.length)) {
    const directions = tuple.map((level) => Math.sign(level.value));
    const preliminaryChanged = directions.filter((direction) => direction !== 0).length;
    const preliminaryImproved = directions.filter((direction) => direction < 0).length;
    const preliminaryDegraded = directions.filter((direction) => direction > 0).length;
    const isGenuineTradeoff =
      mode !== 'tradeoff' || preliminaryChanged === 0 || (preliminaryImproved > 0 && preliminaryDegraded > 0);

    if (!isGenuineTradeoff) {
      skippedPureTradeoffRows += 1;
      continue;
    }

    let candidate = { ...molecule.reference };
    const changes = {};
    let changedCategories = 0;
    let improvedCategories = 0;
    let degradedCategories = 0;
    let maxLevelValue = 0;
    let maxLevel = 'none';

    tuple.forEach((level, index) => {
      const category = categories[index];
      const direction = Math.sign(level.value);
      changes[category] = level.label;
      addLevelCounts(level, category, counts);

      if (direction !== 0) {
        changedCategories += 1;
      }
      if (direction < 0) {
        improvedCategories += 1;
      }
      if (direction > 0) {
        degradedCategories += 1;
      }
      if (Math.abs(level.value) > maxLevelValue) {
        maxLevelValue = Math.abs(level.value);
        maxLevel = level.label;
      }

      candidate = applyCategoryAdjustment(candidate, category, level);
    });

    const name = changedCategories === 0 ? 'reference envelope' : `${changedCategories}-category ${mode}`;
    rows.push({
      ...candidate,
      name,
      type: changedCategories === 0 ? 'reference' : 'generated',
      mode,
      score: scoreCandidate(candidate),
      changes,
      changedCategories,
      improvedCategories,
      degradedCategories,
      maxLevel,
    });

    totalIterations += 1;
    globalModeCounts[mode] += 1;
  }

  return rows;
}

for (const molecule of molecules) {
  const levelLabels = [...degradationLevels.map((level) => level.label), ...tradeoffLevels.map((level) => level.label)];
  const counts = {
    categoryCounts: emptyCounts(categories),
    levelCounts: emptyCounts(levelLabels),
    directionCounts: { neutral: 0, improve: 0, degrade: 0 },
  };

  const degradationRows = buildRowsForMode(molecule, 'degradation', degradationLevels, counts);
  const tradeoffRows = buildRowsForMode(molecule, 'tradeoff', tradeoffLevels, counts);
  const rows = [...degradationRows, ...tradeoffRows];

  const ranked = rows.sort(
    (a, b) => b.score - a.score || a.changedCategories - b.changedCategories || a.degradedCategories - b.degradedCategories
  );
  const referenceRows = ranked.filter((row) => row.type === 'reference');
  const referenceScore = scoreCandidate(molecule.reference);
  const referenceRank = ranked.findIndex((row) => row.type === 'reference') + 1;
  const aboveReference = ranked.filter((row) => row.score > referenceScore).length;
  const withinFivePercent = ranked.filter((row) => row.score >= referenceScore * 0.95).length;
  const strongFailures = ranked.filter((row) => row.score < 0.55).length;
  const tradeoffAboveReference = ranked.filter((row) => row.mode === 'tradeoff' && row.score > referenceScore).length;
  const topScore = ranked[0].score;
  const saturatedTopProfiles = ranked.filter(
    (row) =>
      row.score === topScore &&
      row.valenceSatisfaction === 1 &&
      row.geometryFit === 1 &&
      row.polarityBalance === 1 &&
      row.routeContinuity === 1
  ).length;

  results.push({
    formula: molecule.formula,
    iterations: rows.length,
    degradationIterations: degradationRows.length,
    tradeoffIterations: tradeoffRows.length,
    referenceRank,
    referenceScore,
    referenceRows: referenceRows.length,
    aboveReference,
    tradeoffAboveReference,
    withinFivePercent,
    strongFailures,
    topScore,
    saturatedTopProfiles,
    categoryCounts: counts.categoryCounts,
    levelCounts: counts.levelCounts,
    directionCounts: counts.directionCounts,
    top: uniqueProfiles(ranked, 12).map(compact),
    bottom: ranked.slice(-12).reverse().map(compact),
  });
}

const summary = {
  totalIterations,
  molecules: molecules.length,
  categories,
  degradationLevels: degradationLevels.map((level) => level.label),
  tradeoffLevels: tradeoffLevels.map((level) => level.label),
  globalCategoryCounts,
  globalLevelCounts,
  globalDirectionCounts,
  globalModeCounts,
  skippedPureTradeoffRows,
  results,
};

await mkdir(outDir, { recursive: true });
await writeFile(new URL('molecule-perturbation-sweep.json', outDir), JSON.stringify(summary, null, 2));

const markdown = `# Relational Substrate Molecule Perturbation Sweep

## Scope

This sweep generates candidate variants from reference molecular constraint profiles. It is a secondary-regime coherence bench, not a claim that atoms are vorton species.

Two modes are now run:

- degradation: every non-neutral category moves away from the reference profile.
- tradeoff: categories can improve or degrade, allowing compensation between constraints.

Each iteration applies a level across these change categories:

${categories.map((category) => `- ${category}`).join('\n')}

## Scale

Molecules tested: ${molecules.length}

Total iterations tried: ${totalIterations}

Degradation iterations: ${globalModeCounts.degradation}

Tradeoff iterations: ${globalModeCounts.tradeoff}

Pure improve/degrade tradeoff rows skipped: ${skippedPureTradeoffRows}

Categories per iteration: ${categories.length}

## Global Direction Counts

This counts every category assignment across every iteration.

| Direction | Count |
|---|---:|
${Object.entries(globalDirectionCounts)
  .map(([direction, count]) => `| ${direction} | ${count} |`)
  .join('\n')}

## Global Category Counts

This counts non-neutral applications by category.

| Category | Non-neutral applications |
|---|---:|
${Object.entries(globalCategoryCounts)
  .map(([category, count]) => `| ${category} | ${count} |`)
  .join('\n')}

## Global Level Counts

| Level | Count |
|---|---:|
${Object.entries(globalLevelCounts)
  .map(([level, count]) => `| ${level} | ${count} |`)
  .join('\n')}

## Molecule Results

| Molecule | Iterations | Reference rank | Reference score | Top score | Above reference | Tradeoff above reference | Within 95% | Strong failures | Saturated top profiles |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
${results
  .map(
    (result) =>
      `| ${result.formula} | ${result.iterations} | ${result.referenceRank} | ${result.referenceScore.toFixed(4)} | ${result.topScore.toFixed(4)} | ${result.aboveReference} | ${result.tradeoffAboveReference} | ${result.withinFivePercent} | ${result.strongFailures} | ${result.saturatedTopProfiles} |`
  )
  .join('\n')}

## Top Candidates By Molecule

${results
  .map(
    (result) => `### ${result.formula}

| Rank | Candidate | Mode | Score | Changed | Improved | Degraded | Max level | Valence | Geometry | Angle strain | Bond strain | Polarity | Route | Ring | Steric |
|---:|---|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
${result.top
  .map(
    (row, index) =>
      `| ${index + 1} | ${row.name} | ${row.mode} | ${row.score} | ${row.changedCategories} | ${row.improvedCategories} | ${row.degradedCategories} | ${row.maxLevel} | ${row.valenceSatisfaction} | ${row.geometryFit} | ${row.angleStrain} | ${row.bondStrain} | ${row.polarityBalance} | ${row.routeContinuity} | ${row.ringClosure} | ${row.stericObstruction} |`
  )
  .join('\n')}`
  )
  .join('\n\n')}

## First Reading

The mixed tradeoff mode now excludes pure improvement and pure degradation rows. A tradeoff candidate must either be the neutral reference envelope or contain at least one improved category and at least one degraded category.

When a tradeoff candidate outranks the reference, that is not a discovery. It is a useful diagnostic: under the current scoring assumptions, some loss in one constraint can be more than compensated by gains elsewhere.

The top table is deduplicated by score and constraint profile. Remaining saturated top profiles are a modelling limitation: abstract improvements can push several variables to 1 without specifying the actual geometry that achieved that state.

The next stronger version should replace abstract score adjustments with explicit geometry perturbations: bond lengths, bond angles, torsions, ring closure distances, and polarity vectors. Then the bench can report not only which profile scores best, but which actual geometric candidate produced it.
`;

await writeFile(new URL('molecule-perturbation-sweep-summary.md', outDir), markdown);

console.log(`Molecules tested: ${molecules.length}`);
console.log(`Total iterations tried: ${totalIterations}`);
console.log(`Degradation iterations: ${globalModeCounts.degradation}`);
console.log(`Tradeoff iterations: ${globalModeCounts.tradeoff}`);
console.log(`Wrote ${new URL('molecule-perturbation-sweep-summary.md', outDir).pathname}`);
