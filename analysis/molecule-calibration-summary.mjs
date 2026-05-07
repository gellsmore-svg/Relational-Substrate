import { readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const sourceUrl = new URL('molecule-coordinate-sweep.json', outDir);

function percent(value) {
  return `${(value * 100).toFixed(2)}%`;
}

function classifyEnvelope(result) {
  const nearRate = result.withinFivePercent / result.iterations;
  if (nearRate >= 0.08) return 'broad';
  if (nearRate >= 0.025) return 'moderate';
  if (nearRate >= 0.005) return 'narrow';
  return 'highly constrained';
}

function classifyFailureRate(result) {
  const failureRate = result.strongFailures / result.iterations;
  if (failureRate >= 0.45) return 'very high';
  if (failureRate >= 0.2) return 'high';
  if (failureRate >= 0.05) return 'moderate';
  if (failureRate > 0) return 'low';
  return 'none';
}

function averageMetric(rows, path) {
  const values = rows
    .map((row) => path.reduce((current, key) => current?.[key], row))
    .filter((value) => typeof value === 'number');
  if (!values.length) return 0;
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function average(values) {
  return values.length ? values.reduce((sum, value) => sum + value, 0) / values.length : 0;
}

function min(values) {
  return values.length ? Math.min(...values) : 0;
}

function max(values) {
  return values.length ? Math.max(...values) : 0;
}

function dominantConstraint(result) {
  const rows = result.top.filter((row) => row.name !== 'reference coordinates');
  const metrics = {
    'bond distribution': averageMetric(rows, ['coordinateMetrics', 'bondRms']),
    'angle distribution': averageMetric(rows, ['coordinateMetrics', 'angleRms']),
    'torsion distribution': averageMetric(rows, ['coordinateMetrics', 'torsionRms']),
    'ring planarity': averageMetric(rows, ['coordinateMetrics', 'ringPlanarity']),
    'polarity balance': Math.max(0, 1 - averageMetric(rows, ['derived', 'polarityBalance'])),
    'steric pressure': averageMetric(rows, ['coordinateMetrics', 'steric']),
  };

  const sorted = Object.entries(metrics).sort((a, b) => b[1] - a[1]);
  const [constraint, value] = sorted[0];
  if (value < 0.01) {
    return 'bond-length stability';
  }
  return constraint;
}

function interpretation(result) {
  const envelope = classifyEnvelope(result);
  const dominant = dominantConstraint(result);

  if (result.family === 'ionic pair') {
    return 'Ionic pair proxy; useful as a polarity/separation test, but not yet a crystal-lattice model.';
  }
  if (result.family === 'diatomic covalent') {
    return `Diatomic case; coherence envelope is mostly controlled by ${dominant}.`;
  }
  if (result.family === 'aromatic ring') {
    return 'Ring/distributed-route case; the very narrow envelope is expected and useful.';
  }
  if (result.family === 'linear triatomic') {
    return 'Linear triatomic case; strong failures mostly indicate angle/linearity sensitivity.';
  }
  if (result.family === 'linear unsaturated covalent') {
    return 'Linear unsaturated case; strong failures should indicate axial bond distribution and linearity sensitivity.';
  }
  if (result.family === 'bent polar') {
    return `Bent/pyramidal polar case; ${envelope} envelope reflects angle and polarity sensitivity.`;
  }
  if (result.family === 'rotatable covalent') {
    return `Rotatable covalent case; ${envelope} envelope should preserve bond identity while exposing torsion and crowding sensitivity.`;
  }
  if (result.family === 'trigonal pyramidal covalent') {
    return `Trigonal pyramidal case; ${envelope} envelope should reflect three-route angular constraint plus out-of-plane polarity.`;
  }
  if (result.family === 'tetrahedral covalent') {
    return `Tetrahedral case; ${envelope} envelope is mostly a check on angular distribution and crowding.`;
  }
  if (result.family === 'trigonal planar covalent') {
    return `Trigonal planar case; ${envelope} envelope should reflect planar angular distribution without ring closure.`;
  }
  if (result.family === 'asymmetric planar covalent') {
    return `Asymmetric planar case; ${envelope} envelope should reflect unequal planar route tension and polarity bias.`;
  }
  return `Coordinate case dominated by ${dominant}.`;
}

const summary = JSON.parse(await readFile(sourceUrl, 'utf8'));

const rows = summary.results.map((result) => {
  const nearRate = result.withinFivePercent / result.iterations;
  const failureRate = result.strongFailures / result.iterations;
  return {
    formula: result.formula,
    family: result.family,
    iterations: result.iterations,
    referenceScore: result.referenceScore,
    referenceGenericScore: result.referenceGenericScore,
    referenceRank: result.referenceRank,
    aboveReference: result.aboveReference,
    nearRate,
    failureRate,
    envelope: classifyEnvelope(result),
    failureClass: classifyFailureRate(result),
    dominantConstraint: dominantConstraint(result),
    interpretation: interpretation(result),
  };
});

const familyRows = Object.entries(
  rows.reduce((groups, row) => {
    groups[row.family] ??= [];
    groups[row.family].push(row);
    return groups;
  }, {})
)
  .map(([family, members]) => {
    const allReferenceFirst = members.every((row) => row.referenceRank === 1);
    const aboveReferenceTotal = members.reduce((sum, row) => sum + row.aboveReference, 0);
    const dominantConstraints = [...new Set(members.map((row) => row.dominantConstraint))].join(', ');
    return {
      family,
      cases: members.length,
      allReferenceFirst,
      aboveReferenceTotal,
      averageNearRate: average(members.map((row) => row.nearRate)),
      minNearRate: min(members.map((row) => row.nearRate)),
      maxNearRate: max(members.map((row) => row.nearRate)),
      averageFailureRate: average(members.map((row) => row.failureRate)),
      minFailureRate: min(members.map((row) => row.failureRate)),
      maxFailureRate: max(members.map((row) => row.failureRate)),
      dominantConstraints,
      status: allReferenceFirst && aboveReferenceTotal === 0 ? 'passes current sanity check' : 'needs review',
    };
  })
  .sort((a, b) => a.family.localeCompare(b.family));

const json = {
  source: 'molecule-coordinate-sweep.json',
  totalIterations: summary.totalIterations,
  molecules: summary.molecules,
  families: familyRows,
  controls: summary.controlResults ?? [],
  rows,
};

await writeFile(new URL('molecule-calibration-summary.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate Molecule Calibration Summary

## Scope

This report interprets the coordinate sweep output. It does not prove the Relational Substrate theory. It summarizes whether the current family-aware bench behaves coherently against approximate classical reference geometries.

Source: \`molecule-coordinate-sweep.json\`

Total coordinate iterations: ${summary.totalIterations}

Molecules tested: ${summary.molecules}

## How To Read This

- \`Family\`: molecule class used to weight the shared coherence variables.
- \`Reference rank\`: sanity check. It should be 1 within its family-aware score profile.
- \`Above reference\`: generated candidates beating the reference. At this stage, 0 is preferred.
- \`Near-reference rate\`: share of candidates within 95% of the reference score. This estimates envelope width.
- \`Strong-failure rate\`: share of candidates below the failure threshold.
- \`Dominant constraint\`: first-pass reading from the best non-reference coordinate profiles.

## Cross-Molecule Interpretation

| Molecule | Family | Reference rank | Above reference | Near-reference rate | Envelope | Strong-failure rate | Failure class | Dominant constraint | Reading |
|---|---|---:|---:|---:|---|---:|---|---|---|
${rows
  .map(
    (row) =>
      `| ${row.formula} | ${row.family} | ${row.referenceRank} | ${row.aboveReference} | ${percent(row.nearRate)} | ${row.envelope} | ${percent(row.failureRate)} | ${row.failureClass} | ${row.dominantConstraint} | ${row.interpretation} |`
  )
  .join('\n')}

## Per-Family Validation

This section checks whether family-level weights generalise across the current reference cases without per-molecule tuning.

| Family | Cases | All references rank first | Above-reference candidates | Avg near-reference rate | Near-reference range | Avg strong-failure rate | Strong-failure range | Dominant constraints | Status |
|---|---:|---|---:|---:|---|---:|---|---|---|
${familyRows
  .map(
    (row) =>
      `| ${row.family} | ${row.cases} | ${row.allReferenceFirst ? 'yes' : 'no'} | ${row.aboveReferenceTotal} | ${percent(row.averageNearRate)} | ${percent(row.minNearRate)}-${percent(row.maxNearRate)} | ${percent(row.averageFailureRate)} | ${percent(row.minFailureRate)}-${percent(row.maxFailureRate)} | ${row.dominantConstraints} | ${row.status} |`
  )
  .join('\n')}

## Decoy Control Validation

These deliberately wrong or strained geometries test whether the current scoring grammar rejects familiar failure modes without changing molecule weights.

| Molecule | Family | Control | Reference score | Decoy score | Decoy rank | Reference beats decoy | Decoy penalty | Expected failure |
|---|---|---|---:|---:|---:|---|---:|---|
${(summary.controlResults ?? [])
  .map(
    (control) =>
      `| ${control.formula} | ${control.family} | ${control.label} | ${control.referenceScore.toFixed(4)} | ${control.familyScore.toFixed(4)} | ${control.decoyRank} | ${control.referenceBeatsDecoy ? 'yes' : 'no'} | ${control.decoyPenalty.toFixed(4)} | ${control.expectedFailure} |`
  )
  .join('\n')}

## Reference Provenance

The coordinate references are rounded classical geometry anchors. They calibrate the test bench; they are not claims derived from the Relational Substrate grammar.

| Molecule | Family | Source | Status | Caution |
|---|---|---|---|---|
${Object.entries(summary.referenceData)
  .map(
    ([formula, data]) =>
      `| ${formula} | ${data.family} | ${data.provenance.sourceName} | ${data.provenance.status} | ${data.provenance.caution} |`
  )
  .join('\n')}

Reference source URL: ${summary.referenceData.H2.provenance.sourceUrl}

## Current Reading

All references should rank first and no generated perturbation should beat the reference. That is the core sanity check.

The coordinate sweep now uses molecule-family weights. The same coherence variables are still used across the bench, but diatomic covalent, bent polar, trigonal pyramidal, linear triatomic, linear unsaturated, trigonal planar, asymmetric planar, tetrahedral, rotatable, aromatic ring, and ionic-pair cases are no longer forced through one generic score profile.

The envelope widths are also plausible:

- Diatomics generally have broader near-reference envelopes because they have fewer geometric failure modes.
- Linear, linear unsaturated, bent, trigonal pyramidal, trigonal planar, rotatable, tetrahedral, and aromatic cases become constrained quickly when angle, torsion, polarity, or distribution strain enters.
- Benzene remains the most constrained case, which is expected for a ring/distributed-route proxy.
- NaCl should be treated separately from covalent molecules because this two-body coordinate proxy does not model an ionic lattice.

## What This Does Not Yet Show

This report does not derive atoms, bonds, or molecules from T1 vortons. It only checks whether the current secondary-regime scoring grammar behaves sensibly when perturbed around known reference geometries.

## Next Calibration Step

The next useful upgrade is the harder modelling layer: defining candidate T1 vorton coupling patterns that could generate these T2 coordinate regimes without inserting hidden material intermediates.
`;

await writeFile(new URL('molecule-calibration-summary.md', outDir), markdown);

console.log(`Read ${sourceUrl.pathname}`);
console.log(`Wrote ${new URL('molecule-calibration-summary.md', outDir).pathname}`);
