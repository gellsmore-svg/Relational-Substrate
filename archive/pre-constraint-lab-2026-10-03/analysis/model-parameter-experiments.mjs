import { mkdir, writeFile } from 'node:fs/promises';
import {
  calculateOutcome,
  closedForms,
  scenarioPresets,
  scenarios,
  transientForms,
} from '../src/model.js';

const outDir = new URL('./out/', import.meta.url);

const knobs = ['boundary', 'route', 'storage', 'scatter', 'reseat', 'phase', 'charge'];
const baseIdentityGate = 0.62;
const baseStressGate = 0.62;

const variations = [
  { label: 'boundary +0.10', knob: 'boundary', delta: 0.10 },
  { label: 'boundary -0.10', knob: 'boundary', delta: -0.10 },
  { label: 'route +0.10', knob: 'route', delta: 0.10 },
  { label: 'route -0.10', knob: 'route', delta: -0.10 },
  { label: 'storage +0.10', knob: 'storage', delta: 0.10 },
  { label: 'storage -0.10', knob: 'storage', delta: -0.10 },
  { label: 'scatter +0.10', knob: 'scatter', delta: 0.10 },
  { label: 'scatter -0.10', knob: 'scatter', delta: -0.10 },
  { label: 'reseat +0.10', knob: 'reseat', delta: 0.10 },
  { label: 'reseat -0.10', knob: 'reseat', delta: -0.10 },
  { label: 'phase toward 0.5', knob: 'phase', toward: 0.5, amount: 0.10 },
  { label: 'phase away from 0.5', knob: 'phase', awayFrom: 0.5, amount: 0.10 },
  { label: '|charge| lower 0.10', knob: 'charge', magnitudeDelta: -0.10 },
  { label: '|charge| higher 0.10', knob: 'charge', magnitudeDelta: 0.10 },
];

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

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

function applyVariation(input, variation) {
  const next = { ...input };
  if (variation.delta !== undefined) {
    const clamp = variation.knob === 'charge' ? clampCharge : clamp01;
    next[variation.knob] = clamp((next[variation.knob] ?? 0) + variation.delta);
  } else if (variation.toward !== undefined) {
    const current = next[variation.knob] ?? variation.toward;
    const direction = variation.toward - current;
    next[variation.knob] = clamp01(current + Math.sign(direction) * Math.min(Math.abs(direction), variation.amount));
  } else if (variation.awayFrom !== undefined) {
    const current = next[variation.knob] ?? variation.awayFrom;
    const direction = current >= variation.awayFrom ? 1 : -1;
    next[variation.knob] = clamp01(current + direction * variation.amount);
  } else if (variation.magnitudeDelta !== undefined) {
    const current = next[variation.knob] ?? 0;
    const sign = current === 0 ? 1 : Math.sign(current);
    const magnitude = clamp01(Math.abs(current) + variation.magnitudeDelta);
    next[variation.knob] = clampCharge(sign * magnitude);
  }
  return next;
}

function compactOutcome(input, outcome) {
  return {
    input: Object.fromEntries(knobs.map((knob) => [knob, round(input[knob] ?? 0)])),
    identityScore: round(outcome.identityScore),
    closureStress: round(outcome.closureStress),
    effectiveIdentityScore: round(outcome.effectiveIdentityScore ?? outcome.identityScore),
    identityPreserved: outcome.identityPreserved,
    admitted: round(outcome.admitted),
    returned: round(outcome.returned),
    stored: round(outcome.stored),
    scattered: round(outcome.scattered),
    grammar: {
      continuity: round(outcome.grammar.continuity),
      phaseMatch: round(outcome.grammar.phaseMatch),
      chargeTension: round(outcome.grammar.chargeTension),
      grammarAlignment: round(outcome.grammar.grammarAlignment),
    },
  };
}

const seeds = [];
for (const scenario of scenarios) {
  seeds.push({
    label: `${scenario} preset / trefoil+sine`,
    closedForm: 'trefoil',
    transientForm: 'sine',
    scenario,
    ...scenarioPresets[scenario],
  });
}

// Add one best-case and one stressed case per scenario so the experiment is not only about a single form/transient pair.
for (const scenario of scenarios) {
  seeds.push({
    label: `${scenario} preset / circle+straight`,
    closedForm: 'circle',
    transientForm: 'straight',
    scenario,
    ...scenarioPresets[scenario],
  });
  seeds.push({
    label: `${scenario} preset / double+ribbon`,
    closedForm: 'double',
    transientForm: 'ribbon',
    scenario,
    ...scenarioPresets[scenario],
  });
}

const seedReports = seeds.map((seed) => {
  const base = calculateOutcome(seed);
  const rows = variations.map((variation) => {
    const variedInput = applyVariation(seed, variation);
    const varied = calculateOutcome(variedInput);
    return {
      label: variation.label,
      knob: variation.knob,
      variedInput,
      identityDelta: round(varied.identityScore - base.identityScore),
      effectiveIdentityDelta: round((varied.effectiveIdentityScore ?? varied.identityScore) - (base.effectiveIdentityScore ?? base.identityScore)),
      stressDelta: round(varied.closureStress - base.closureStress),
      coherenceDelta: round(varied.coherenceMetric - base.coherenceMetric),
      grammarAlignmentDelta: round(varied.grammar.grammarAlignment - base.grammar.grammarAlignment),
      preservedChange:
        base.identityPreserved === varied.identityPreserved
          ? 'unchanged'
          : base.identityPreserved
            ? 'breaks preservation'
            : 'restores preservation',
      outcome: compactOutcome(variedInput, varied),
    };
  });

  return {
    seed: {
      label: seed.label,
      closedForm: seed.closedForm,
      transientForm: seed.transientForm,
      scenario: seed.scenario,
      input: Object.fromEntries(knobs.map((knob) => [knob, seed[knob]])),
    },
    base: compactOutcome(seed, base),
    variationRows: rows,
    bestIdentityMoves: [...rows].sort((a, b) => b.identityDelta - a.identityDelta).slice(0, 5),
    worstIdentityMoves: [...rows].sort((a, b) => a.identityDelta - b.identityDelta).slice(0, 5),
  };
});

const aggregate = variations.map((variation) => {
  const all = seedReports.flatMap((seed) => seed.variationRows.filter((row) => row.label === variation.label));
  return {
    label: variation.label,
    knob: variation.knob,
    meanIdentityDelta: round(mean(all.map((row) => row.identityDelta))),
    meanEffectiveIdentityDelta: round(mean(all.map((row) => row.effectiveIdentityDelta))),
    meanStressDelta: round(mean(all.map((row) => row.stressDelta))),
    meanCoherenceDelta: round(mean(all.map((row) => row.coherenceDelta))),
    meanGrammarAlignmentDelta: round(mean(all.map((row) => row.grammarAlignmentDelta))),
    restoresPreservation: all.filter((row) => row.preservedChange === 'restores preservation').length,
    breaksPreservation: all.filter((row) => row.preservedChange === 'breaks preservation').length,
  };
});

const aggregateRanked = [...aggregate].sort(
  (a, b) => b.meanEffectiveIdentityDelta - a.meanEffectiveIdentityDelta || a.meanStressDelta - b.meanStressDelta,
);

const byKnob = knobs.map((knob) => {
  const rows = aggregate.filter((row) => row.knob === knob);
  return {
    knob,
    bestMove: [...rows].sort((a, b) => b.meanEffectiveIdentityDelta - a.meanEffectiveIdentityDelta)[0]?.label ?? 'n/a',
    bestMeanEffectiveIdentityDelta: rows.length
      ? round(Math.max(...rows.map((row) => row.meanEffectiveIdentityDelta)))
      : 0,
    worstMove: [...rows].sort((a, b) => a.meanEffectiveIdentityDelta - b.meanEffectiveIdentityDelta)[0]?.label ?? 'n/a',
    worstMeanEffectiveIdentityDelta: rows.length
      ? round(Math.min(...rows.map((row) => row.meanEffectiveIdentityDelta)))
      : 0,
  };
});

const practicalRecipes = [
  {
    recipe: 'preservation lift',
    changes: ['reseat +0.10', 'route +0.10', 'scatter -0.10', 'phase toward 0.5', '|charge| lower 0.10'],
    use: 'quickest way to explore stronger identity preservation without changing model internals',
  },
  {
    recipe: 'stress/failure probe',
    changes: ['reseat -0.10', 'route -0.10', 'scatter +0.10', 'phase away from 0.5', '|charge| higher 0.10'],
    use: 'tests whether a configuration is only barely above the identity gate',
  },
  {
    recipe: 'storage lock-up probe',
    changes: ['storage +0.10', 'scatter +0.10', 'reseat -0.10'],
    use: 'checks whether apparent preservation is vulnerable to stored/scattered closure stress',
  },
  {
    recipe: 'route boost probe',
    changes: ['route +0.10'],
    use: 'isolates positive continuity sensitivity without deliberately altering phase or charge',
  },
  {
    recipe: 'route suppression probe',
    changes: ['route -0.10'],
    use: 'isolates negative continuity sensitivity without deliberately altering phase or charge',
  },
];

const variationByLabel = new Map(variations.map((variation) => [variation.label, variation]));

function applyRecipe(input, recipe) {
  return recipe.changes.reduce((current, change) => {
    const variation = variationByLabel.get(change);
    if (!variation) {
      throw new Error(`Unknown recipe variation: ${change}`);
    }
    return applyVariation(current, variation);
  }, { ...input });
}

const recipeReports = practicalRecipes.map((recipe) => {
  const rows = seedReports.map((seedReport) => {
    const seed = seeds.find((candidate) => candidate.label === seedReport.seed.label);
    const base = calculateOutcome(seed);
    const recipeInput = applyRecipe(seed, recipe);
    const outcome = calculateOutcome(recipeInput);
    return {
      seed: seed.label,
      base: compactOutcome(seed, base),
      outcome: compactOutcome(recipeInput, outcome),
      identityDelta: round(outcome.identityScore - base.identityScore),
      effectiveIdentityDelta: round((outcome.effectiveIdentityScore ?? outcome.identityScore) - (base.effectiveIdentityScore ?? base.identityScore)),
      stressDelta: round(outcome.closureStress - base.closureStress),
      coherenceDelta: round(outcome.coherenceMetric - base.coherenceMetric),
      preservedChange:
        base.identityPreserved === outcome.identityPreserved
          ? 'unchanged'
          : base.identityPreserved
            ? 'breaks preservation'
            : 'restores preservation',
    };
  });

  return {
    recipe: recipe.recipe,
    changes: recipe.changes,
    use: recipe.use,
    meanIdentityDelta: round(mean(rows.map((row) => row.identityDelta))),
    meanEffectiveIdentityDelta: round(mean(rows.map((row) => row.effectiveIdentityDelta))),
    meanStressDelta: round(mean(rows.map((row) => row.stressDelta))),
    meanCoherenceDelta: round(mean(rows.map((row) => row.coherenceDelta))),
    restoresPreservation: rows.filter((row) => row.preservedChange === 'restores preservation').length,
    breaksPreservation: rows.filter((row) => row.preservedChange === 'breaks preservation').length,
    rows,
  };
});

const result = {
  scope:
    'One-at-a-time parameter experiments around current scenario presets. Exploratory only; not validation and not a model change.',
  gates: {
    identityScore: baseIdentityGate,
    closureStress: baseStressGate,
  },
  seedCount: seeds.length,
  variations,
  aggregateRanked,
  byKnob,
  seedReports,
  practicalRecipes,
  recipeReports,
};

await mkdir(outDir, { recursive: true });
await writeFile(new URL('model-parameter-experiments.json', outDir), `${JSON.stringify(result, null, 2)}\n`);

const topAggregate = aggregateRanked.slice(0, 8);
const bottomAggregate = [...aggregateRanked].reverse().slice(0, 8);

const markdown = `# Model Parameter Experiments

## Scope

This report varies one parameter at a time around the current scenario presets. It is designed for interactive experimentation: "if this knob moves, what changes?" It does not change the model, fit a target, or validate the substrate theory.

Identity gate used for interpretation: \`identityScore >= ${baseIdentityGate}\` and \`closureStress < ${baseStressGate}\`.

Seeds tested: ${seeds.length} scenario/form/transient combinations.

## Aggregate Effects

Positive identity deltas mean the move usually strengthens identity preservation around the current presets. Negative deltas mean it usually weakens preservation.

### Strongest Average Lifts

${table(
  ['Move', 'Mean identity Δ', 'Mean effective identity Δ', 'Mean stress Δ', 'Mean coherence Δ', 'Restores', 'Breaks'],
  topAggregate.map((row) => [
    row.label,
    row.meanIdentityDelta,
    row.meanEffectiveIdentityDelta,
    row.meanStressDelta,
    row.meanCoherenceDelta,
    row.restoresPreservation,
    row.breaksPreservation,
  ]),
)}

### Strongest Average Breaks

${table(
  ['Move', 'Mean identity Δ', 'Mean effective identity Δ', 'Mean stress Δ', 'Mean coherence Δ', 'Restores', 'Breaks'],
  bottomAggregate.map((row) => [
    row.label,
    row.meanIdentityDelta,
    row.meanEffectiveIdentityDelta,
    row.meanStressDelta,
    row.meanCoherenceDelta,
    row.restoresPreservation,
    row.breaksPreservation,
  ]),
)}

## Knob Summary

${table(
  ['Knob', 'Best move', 'Best effective identity Δ', 'Worst move', 'Worst effective identity Δ'],
  byKnob.map((row) => [
    row.knob,
    row.bestMove,
    row.bestMeanEffectiveIdentityDelta,
    row.worstMove,
    row.worstMeanEffectiveIdentityDelta,
  ]),
)}

## Practical Recipes

${table(
  ['Recipe', 'Changes', 'Use'],
  practicalRecipes.map((row) => [row.recipe, row.changes.join('; '), row.use]),
)}

## Recipe Results

These apply each recipe as a combined multi-parameter move around every seed. This is more realistic than the one-at-a-time table, but still exploratory.

${table(
  ['Recipe', 'Mean identity Δ', 'Mean effective identity Δ', 'Mean stress Δ', 'Mean coherence Δ', 'Restores', 'Breaks'],
  recipeReports.map((row) => [
    row.recipe,
    row.meanIdentityDelta,
    row.meanEffectiveIdentityDelta,
    row.meanStressDelta,
    row.meanCoherenceDelta,
    row.restoresPreservation,
    row.breaksPreservation,
  ]),
)}

### Recipe Seed Outcomes

${recipeReports
  .map((recipe) => {
    const rows = recipe.rows
      .map(
        (row) =>
          `| ${row.seed} | ${row.identityDelta} | ${row.effectiveIdentityDelta} | ${row.stressDelta} | ${row.preservedChange} |`,
      )
      .join('\n');
    return `#### ${recipe.recipe}

Changes: ${recipe.changes.join('; ')}

| Seed | Identity Δ | Effective identity Δ | Stress Δ | Preservation |
|---|---:|---:|---:|---|
${rows}`;
  })
  .join('\n\n')}

## Seed Details

${seedReports
  .map((seed) => {
    const bestRows = seed.bestIdentityMoves
      .map(
        (row) =>
          `| ${row.label} | ${row.identityDelta} | ${row.effectiveIdentityDelta} | ${row.stressDelta} | ${row.preservedChange} |`,
      )
      .join('\n');
    const worstRows = seed.worstIdentityMoves
      .map(
        (row) =>
          `| ${row.label} | ${row.identityDelta} | ${row.effectiveIdentityDelta} | ${row.stressDelta} | ${row.preservedChange} |`,
      )
      .join('\n');
    return `### ${seed.seed.label}

Base: identity ${seed.base.identityScore}, effective identity ${seed.base.effectiveIdentityScore}, stress ${seed.base.closureStress}, preserved ${seed.base.identityPreserved ? 'yes' : 'no'}.

Best moves:

| Move | Identity Δ | Effective identity Δ | Stress Δ | Preservation |
|---|---:|---:|---:|---|
${bestRows}

Worst moves:

| Move | Identity Δ | Effective identity Δ | Stress Δ | Preservation |
|---|---:|---:|---:|---|
${worstRows}`;
  })
  .join('\n\n')}

## Reading

This one-at-a-time experiment agrees with the broader sensitivity analysis: \`reseat\`, \`route\`, and \`scatter\` are the most useful practical knobs. \`phase\` matters when it moves away from the neutral alignment point, and \`charge\` matters through absolute tension. \`storage\` is useful for stress tests because too much storage can look like retention while raising closure stress.

Use this report to guide sandbox exploration. Do not use it to tune evidence-bearing material RI or torsion coefficients after seeing a target.
`;

await writeFile(new URL('model-parameter-experiments.md', outDir), markdown);

console.log(markdown);
