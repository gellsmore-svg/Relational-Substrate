import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { basename } from 'node:path';
import { createHash } from 'node:crypto';
import { calculateOutcome, scenarioPresets } from '../src/model.js';

const outDir = new URL('./out/', import.meta.url);
const allowedKnobs = new Set(['boundary', 'route', 'storage', 'scatter', 'reseat', 'phase', 'charge']);
const inputPath = process.argv[2] || new URL('./parameter-recipe.example.json', import.meta.url).pathname;

function clamp01(value) {
  return Math.max(0, Math.min(1, value));
}

function clampCharge(value) {
  return Math.max(-1, Math.min(1, value));
}

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

function mean(values) {
  return values.length ? values.reduce((sum, value) => sum + value, 0) / values.length : 0;
}

function stableStringify(value) {
  if (Array.isArray(value)) {
    return `[${value.map((item) => stableStringify(item)).join(',')}]`;
  }
  if (value && typeof value === 'object') {
    return `{${Object.keys(value)
      .sort()
      .map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`)
      .join(',')}}`;
  }
  return JSON.stringify(value);
}

function hashRecord(value) {
  return createHash('sha256').update(stableStringify(value)).digest('hex').slice(0, 16);
}

function slug(value) {
  return String(value)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 80) || 'parameter-recipe';
}

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

function normalizeSeed(seed) {
  const preset = seed.preset ? scenarioPresets[seed.preset] : {};
  if (seed.preset && !preset) {
    throw new Error(`Unknown scenario preset: ${seed.preset}`);
  }
  const scenario = seed.scenario || seed.preset || 'admit';
  const directKnobs = Object.fromEntries(
    [...allowedKnobs]
      .filter((knob) => seed[knob] !== undefined)
      .map((knob) => [knob, seed[knob]]),
  );
  return {
    label: seed.label || `${scenario} / ${seed.closedForm || 'trefoil'}+${seed.transientForm || 'sine'}`,
    closedForm: seed.closedForm || 'trefoil',
    transientForm: seed.transientForm || 'sine',
    scenario,
    ...preset,
    ...directKnobs,
    ...seed.overrides,
  };
}

function moveLabel(move) {
  if (move.label) return move.label;
  if (move.delta !== undefined) return `${move.knob} ${move.delta >= 0 ? '+' : ''}${move.delta}`;
  if (move.toward !== undefined) return `${move.knob} toward ${move.toward}`;
  if (move.awayFrom !== undefined) return `${move.knob} away from ${move.awayFrom}`;
  if (move.magnitudeDelta !== undefined) return `|${move.knob}| ${move.magnitudeDelta >= 0 ? '+' : ''}${move.magnitudeDelta}`;
  return `${move.knob} move`;
}

function applyMove(input, move) {
  if (!allowedKnobs.has(move.knob)) {
    throw new Error(`Unknown knob "${move.knob}". Allowed: ${[...allowedKnobs].join(', ')}`);
  }
  const next = { ...input };
  if (move.delta !== undefined) {
    const clamp = move.knob === 'charge' ? clampCharge : clamp01;
    next[move.knob] = clamp((next[move.knob] ?? 0) + move.delta);
  } else if (move.toward !== undefined) {
    const current = next[move.knob] ?? move.toward;
    const direction = move.toward - current;
    next[move.knob] = clamp01(current + Math.sign(direction) * Math.min(Math.abs(direction), move.amount ?? 0.1));
  } else if (move.awayFrom !== undefined) {
    const current = next[move.knob] ?? move.awayFrom;
    const direction = current >= move.awayFrom ? 1 : -1;
    next[move.knob] = clamp01(current + direction * (move.amount ?? 0.1));
  } else if (move.magnitudeDelta !== undefined) {
    const current = next[move.knob] ?? 0;
    const sign = current === 0 ? 1 : Math.sign(current);
    const magnitude = clamp01(Math.abs(current) + move.magnitudeDelta);
    next[move.knob] = clampCharge(sign * magnitude);
  } else {
    throw new Error(`Move for ${move.knob} must include delta, toward, awayFrom, or magnitudeDelta.`);
  }
  return next;
}

function applyRecipe(seed, recipe) {
  return recipe.moves.reduce((current, move) => applyMove(current, move), { ...seed });
}

function compact(input, outcome) {
  return {
    input: {
      boundary: round(input.boundary ?? 0),
      route: round(input.route ?? 0),
      storage: round(input.storage ?? 0),
      scatter: round(input.scatter ?? 0),
      reseat: round(input.reseat ?? 0),
      phase: round(input.phase ?? 0),
      charge: round(input.charge ?? 0),
    },
    identityScore: round(outcome.identityScore),
    effectiveIdentityScore: round(outcome.effectiveIdentityScore ?? outcome.identityScore),
    closureStress: round(outcome.closureStress),
    coherence: round(outcome.coherenceMetric),
    identityPreserved: outcome.identityPreserved,
    admitted: round(outcome.admitted),
    returned: round(outcome.returned),
    stored: round(outcome.stored),
    scattered: round(outcome.scattered),
    continuity: round(outcome.grammar.continuity),
    phaseMatch: round(outcome.grammar.phaseMatch),
    chargeTension: round(outcome.grammar.chargeTension),
  };
}

const config = JSON.parse(await readFile(inputPath, 'utf8'));
const seeds = (config.seeds || []).map(normalizeSeed);
if (!seeds.length) {
  throw new Error('Recipe file must include at least one seed.');
}
if (!Array.isArray(config.recipes) || !config.recipes.length) {
  throw new Error('Recipe file must include at least one recipe.');
}

const recipeReports = config.recipes.map((recipe) => {
  if (!Array.isArray(recipe.moves) || !recipe.moves.length) {
    throw new Error(`Recipe "${recipe.name || 'unnamed'}" must include moves.`);
  }
  const rows = seeds.map((seed) => {
    const baseOutcome = calculateOutcome(seed);
    const recipeInput = applyRecipe(seed, recipe);
    const recipeOutcome = calculateOutcome(recipeInput);
    return {
      seed: seed.label,
      base: compact(seed, baseOutcome),
      outcome: compact(recipeInput, recipeOutcome),
      identityDelta: round(recipeOutcome.identityScore - baseOutcome.identityScore),
      effectiveIdentityDelta: round(
        (recipeOutcome.effectiveIdentityScore ?? recipeOutcome.identityScore) -
          (baseOutcome.effectiveIdentityScore ?? baseOutcome.identityScore),
      ),
      stressDelta: round(recipeOutcome.closureStress - baseOutcome.closureStress),
      coherenceDelta: round(recipeOutcome.coherenceMetric - baseOutcome.coherenceMetric),
      preservedChange:
        baseOutcome.identityPreserved === recipeOutcome.identityPreserved
          ? 'unchanged'
          : baseOutcome.identityPreserved
            ? 'breaks preservation'
            : 'restores preservation',
    };
  });
  return {
    name: recipe.name || 'unnamed recipe',
    description: recipe.description || '',
    moves: recipe.moves.map(moveLabel),
    meanIdentityDelta: round(mean(rows.map((row) => row.identityDelta))),
    meanEffectiveIdentityDelta: round(mean(rows.map((row) => row.effectiveIdentityDelta))),
    meanStressDelta: round(mean(rows.map((row) => row.stressDelta))),
    meanCoherenceDelta: round(mean(rows.map((row) => row.coherenceDelta))),
    restoresPreservation: rows.filter((row) => row.preservedChange === 'restores preservation').length,
    breaksPreservation: rows.filter((row) => row.preservedChange === 'breaks preservation').length,
    rows,
  };
});

const reportName = config.name || basename(inputPath).replace(/\.[^.]+$/, '');
const normalizedLock = {
  name: reportName,
  description: config.description || '',
  seeds: seeds.map((seed) => ({
    label: seed.label,
    closedForm: seed.closedForm,
    transientForm: seed.transientForm,
    scenario: seed.scenario,
    boundary: seed.boundary,
    route: seed.route,
    storage: seed.storage,
    scatter: seed.scatter,
    reseat: seed.reseat,
    phase: seed.phase,
    charge: seed.charge,
  })),
  recipes: config.recipes.map((recipe) => ({
    name: recipe.name || 'unnamed recipe',
    description: recipe.description || '',
    moves: recipe.moves,
  })),
};
const recipeHash = hashRecord(normalizedLock);
const inputHashStatus = config.recipeHash
  ? {
      providedRecipeHash: config.recipeHash,
      recomputedRecipeHash: recipeHash,
      matches: config.recipeHash === recipeHash,
    }
  : null;
if (inputHashStatus && !inputHashStatus.matches) {
  throw new Error(
    `Recipe lock hash mismatch: provided ${inputHashStatus.providedRecipeHash}, recomputed ${inputHashStatus.recomputedRecipeHash}`,
  );
}
const result = {
  source: 'run-parameter-recipe.mjs',
  inputPath,
  name: reportName,
  description: config.description || '',
  status: 'exploratory parameter recipe report; not validation',
  recipeHash,
  inputHashStatus,
  seeds: seeds.map((seed) => ({
    label: seed.label,
    closedForm: seed.closedForm,
    transientForm: seed.transientForm,
    scenario: seed.scenario,
  })),
  recipeReports,
};

await mkdir(outDir, { recursive: true });
const outBase = `parameter-recipe-${slug(reportName)}`;
await writeFile(new URL(`${outBase}.json`, outDir), `${JSON.stringify(result, null, 2)}\n`);
await writeFile(new URL(`${outBase}.lock.json`, outDir), `${JSON.stringify({ recipeHash, ...normalizedLock }, null, 2)}\n`);

const markdown = `# Parameter Recipe Report: ${reportName}

## Scope

${config.description || 'Exploratory sandbox parameter recipes.'}

This report applies configured parameter moves to selected seeds. It does not change the model, fit a target, or validate the substrate theory.

Input file: \`${inputPath}\`

Recipe hash: \`${recipeHash}\`
${inputHashStatus ? `\nInput lock hash verified: ${inputHashStatus.matches ? 'yes' : 'no'}\n` : ''}

Normalized lock file: \`analysis/out/${outBase}.lock.json\`

## Seeds

${table(
  ['Seed', 'Closed form', 'Transient', 'Scenario'],
  result.seeds.map((seed) => [seed.label, seed.closedForm, seed.transientForm, seed.scenario]),
)}

## Recipe Summary

${table(
  ['Recipe', 'Moves', 'Mean effective identity Δ', 'Mean stress Δ', 'Restores', 'Breaks'],
  recipeReports.map((recipe) => [
    recipe.name,
    recipe.moves.join('; '),
    recipe.meanEffectiveIdentityDelta,
    recipe.meanStressDelta,
    recipe.restoresPreservation,
    recipe.breaksPreservation,
  ]),
)}

## Recipe Details

${recipeReports
  .map((recipe) => {
    const rows = recipe.rows
      .map(
        (row) =>
          `| ${row.seed} | ${row.base.effectiveIdentityScore} | ${row.outcome.effectiveIdentityScore} | ${row.effectiveIdentityDelta} | ${row.stressDelta} | ${row.preservedChange} |`,
      )
      .join('\n');
    return `### ${recipe.name}

${recipe.description}

Moves: ${recipe.moves.join('; ')}

| Seed | Base effective identity | Recipe effective identity | Effective identity Δ | Stress Δ | Preservation |
|---|---:|---:|---:|---:|---|
${rows}`;
  })
  .join('\n\n')}

## Reading

Use this for exploration and sensitivity checking. For evidence-bearing work, freeze the recipe before target lookup and keep conventional comparators separate where relevant.
`;

await writeFile(new URL(`${outBase}.md`, outDir), markdown);

console.log(markdown);
