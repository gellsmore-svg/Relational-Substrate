import { mkdir, writeFile } from 'node:fs/promises';
import { calculateOutcome, closedForms, transientForms, scenarios } from '../src/model.js';

const outDir = new URL('./out/', import.meta.url);

const values = [0.15, 0.35, 0.55, 0.75, 0.9];

function compact(row) {
  return {
    closedForm: row.closedForm,
    transientForm: row.transientForm,
    scenario: row.scenario,
    boundary: row.boundary,
    route: row.route,
    storage: row.storage,
    scatter: row.scatter,
    reseat: row.reseat,
    identityScore: Number(row.identityScore.toFixed(4)),
    closureStress: Number(row.closureStress.toFixed(4)),
    admitted: Number(row.admitted.toFixed(4)),
    returned: Number(row.returned.toFixed(4)),
    stored: Number(row.stored.toFixed(4)),
    scattered: Number(row.scattered.toFixed(4)),
    identityPreserved: row.identityPreserved,
  };
}

const rows = [];
for (const closedForm of closedForms) {
  for (const transientForm of transientForms) {
    for (const scenario of scenarios) {
      for (const boundary of values) {
        for (const route of values) {
          for (const storage of values) {
            for (const scatter of values) {
              for (const reseat of values) {
                rows.push(calculateOutcome({ closedForm, transientForm, scenario, boundary, route, storage, scatter, reseat }));
              }
            }
          }
        }
      }
    }
  }
}

const preserved = rows.filter((row) => row.identityPreserved);
const topCoherent = [...rows]
  .filter((row) => row.identityPreserved)
  .sort((a, b) => b.identityScore - a.identityScore || a.closureStress - b.closureStress)
  .slice(0, 25)
  .map(compact);

const fragile = [...rows]
  .filter((row) => row.identityScore > 0.58 && row.identityScore < 0.68)
  .sort((a, b) => Math.abs(a.identityScore - 0.62) - Math.abs(b.identityScore - 0.62))
  .slice(0, 25)
  .map(compact);

const failure = [...rows]
  .filter((row) => !row.identityPreserved)
  .sort((a, b) => b.closureStress - a.closureStress || a.identityScore - b.identityScore)
  .slice(0, 25)
  .map(compact);

const byPattern = new Map();
for (const row of rows) {
  const key = `${row.closedForm}/${row.transientForm}/${row.scenario}`;
  const current = byPattern.get(key) || { key, count: 0, preserved: 0, avgIdentity: 0, avgStress: 0 };
  current.count += 1;
  current.preserved += row.identityPreserved ? 1 : 0;
  current.avgIdentity += row.identityScore;
  current.avgStress += row.closureStress;
  byPattern.set(key, current);
}

const patternSummary = [...byPattern.values()]
  .map((item) => ({
    pattern: item.key,
    preservedRate: Number((item.preserved / item.count).toFixed(4)),
    avgIdentity: Number((item.avgIdentity / item.count).toFixed(4)),
    avgStress: Number((item.avgStress / item.count).toFixed(4)),
  }))
  .sort((a, b) => b.preservedRate - a.preservedRate || b.avgIdentity - a.avgIdentity);

await mkdir(outDir, { recursive: true });
await writeFile(new URL('coherence-sweep.json', outDir), JSON.stringify({ total: rows.length, preserved: preserved.length, patternSummary, topCoherent, fragile, failure }, null, 2));

const markdown = `# AMS Topology Sandbox Coherence Sweep

## Scope

This sweep is a conceptual search over the sandbox rule model. It is not physics validation.

Total combinations: ${rows.length}

Identity preserved: ${preserved.length}

Preserved rate: ${(preserved.length / rows.length).toFixed(4)}

## Best Pattern Families

| Pattern | Preserved rate | Avg identity | Avg stress |
|---|---:|---:|---:|
${patternSummary
  .slice(0, 12)
  .map((row) => `| ${row.pattern} | ${row.preservedRate} | ${row.avgIdentity} | ${row.avgStress} |`)
  .join('\n')}

## Top Coherent Cases

| Closed | Transient | Scenario | Boundary | Route | Storage | Scatter | Reseat | Identity | Stress |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
${topCoherent
  .slice(0, 12)
  .map((row) => `| ${row.closedForm} | ${row.transientForm} | ${row.scenario} | ${row.boundary} | ${row.route} | ${row.storage} | ${row.scatter} | ${row.reseat} | ${row.identityScore} | ${row.closureStress} |`)
  .join('\n')}

## Fragile Boundary Cases

These sit near the preservation threshold and are useful for testing the model language.

| Closed | Transient | Scenario | Boundary | Route | Storage | Scatter | Reseat | Identity | Stress | Preserved |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
${fragile
  .slice(0, 12)
  .map((row) => `| ${row.closedForm} | ${row.transientForm} | ${row.scenario} | ${row.boundary} | ${row.route} | ${row.storage} | ${row.scatter} | ${row.reseat} | ${row.identityScore} | ${row.closureStress} | ${row.identityPreserved} |`)
  .join('\n')}

## High-Stress Failures

| Closed | Transient | Scenario | Boundary | Route | Storage | Scatter | Reseat | Identity | Stress |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
${failure
  .slice(0, 12)
  .map((row) => `| ${row.closedForm} | ${row.transientForm} | ${row.scenario} | ${row.boundary} | ${row.route} | ${row.storage} | ${row.scatter} | ${row.reseat} | ${row.identityScore} | ${row.closureStress} |`)
  .join('\n')}

## First Reading

The current toy model favours high boundary compatibility, high route continuity, low scattering, and high reseating tolerance. That is expected and not yet a discovery. The useful part is the fragile boundary set: those cases show where small changes in storage, scattering, or reseating move a candidate from identity-preserved to identity-at-risk.
`;

await writeFile(new URL('coherence-sweep-summary.md', outDir), markdown);

console.log(`Swept ${rows.length} combinations.`);
console.log(`Identity preserved in ${preserved.length} combinations (${(preserved.length / rows.length).toFixed(4)}).`);
console.log(`Wrote ${new URL('coherence-sweep-summary.md', outDir).pathname}`);
