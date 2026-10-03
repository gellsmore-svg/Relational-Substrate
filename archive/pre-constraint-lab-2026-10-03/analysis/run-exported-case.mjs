// Replay a sandbox-exported case through the model (process recommendation #8).
//
// Closes the UI->analysis loop: the browser sandbox's "Export case (JSON)"
// button emits the exact form/scenario/slider state; this reads that JSON
// (single object or array) and runs it through calculateOutcome, so a case
// found visually is reproduced exactly in batch.
//
// Usage:
//   npm run case:run -- analysis/exported-case.example.json
//   node analysis/run-exported-case.mjs path/to/case.json
//   pbpaste | node analysis/run-exported-case.mjs        # read from stdin
//
// Exits non-zero on malformed input or out-of-range / unknown fields.

import { readFileSync } from 'node:fs';
import { calculateOutcome, closedForms, transientForms, scenarios } from '../src/model.js';

const REQUIRED_NUMBERS = ['boundary', 'route', 'storage', 'scatter', 'reseat'];

function readInput() {
  const path = process.argv[2];
  if (path) return readFileSync(path, 'utf8');
  try {
    return readFileSync(0, 'utf8'); // stdin
  } catch {
    return '';
  }
}

function validateCase(c, i) {
  const where = `case[${i}]`;
  if (!c || typeof c !== 'object') throw new Error(`${where}: not an object`);
  if (!closedForms.includes(c.closedForm)) throw new Error(`${where}: closedForm must be one of ${closedForms.join(', ')}`);
  if (!transientForms.includes(c.transientForm)) throw new Error(`${where}: transientForm must be one of ${transientForms.join(', ')}`);
  if (!scenarios.includes(c.scenario)) throw new Error(`${where}: scenario must be one of ${scenarios.join(', ')}`);
  for (const k of REQUIRED_NUMBERS) {
    const v = c[k];
    if (typeof v !== 'number' || Number.isNaN(v) || v < 0 || v > 1) {
      throw new Error(`${where}: ${k} must be a number in [0,1] (got ${JSON.stringify(v)})`);
    }
  }
}

const raw = readInput().trim();
if (!raw) {
  console.error('No input. Pass a JSON file path or pipe JSON on stdin.');
  process.exit(2);
}

let parsed;
try {
  parsed = JSON.parse(raw);
} catch (e) {
  console.error(`Invalid JSON: ${e.message}`);
  process.exit(2);
}

const cases = Array.isArray(parsed) ? parsed : [parsed];
try {
  cases.forEach(validateCase);
} catch (e) {
  console.error(`Invalid case: ${e.message}`);
  process.exit(2);
}

const r4 = (v) => Number(v.toFixed(4));
const results = cases.map((c) => {
  const o = calculateOutcome({
    closedForm: c.closedForm,
    transientForm: c.transientForm,
    scenario: c.scenario,
    boundary: c.boundary,
    route: c.route,
    storage: c.storage,
    scatter: c.scatter,
    reseat: c.reseat,
  });
  return {
    input: { closedForm: c.closedForm, transientForm: c.transientForm, scenario: c.scenario,
      boundary: c.boundary, route: c.route, storage: c.storage, scatter: c.scatter, reseat: c.reseat },
    identityScore: r4(o.identityScore),
    closureStress: r4(o.closureStress),
    identityPreserved: o.identityPreserved,
    fractions: { admitted: r4(o.admitted), returned: r4(o.returned), stored: r4(o.stored), scattered: r4(o.scattered) },
    metrics: Object.fromEntries(Object.entries(o.metrics).map(([k, v]) => [k, r4(v)])),
  };
});

for (const [i, res] of results.entries()) {
  const c = res.input;
  console.log(`case ${i}: ${c.closedForm}/${c.transientForm}/${c.scenario} ` +
    `b=${c.boundary} r=${c.route} st=${c.storage} sc=${c.scatter} rs=${c.reseat}`);
  console.log(`  identityScore=${res.identityScore} closureStress=${res.closureStress} identityPreserved=${res.identityPreserved}`);
  console.log(`  fractions: ${JSON.stringify(res.fractions)}`);
  console.log(`  metrics: ${JSON.stringify(res.metrics)}`);
}

// Machine-readable line for piping into other tools.
console.log(JSON.stringify(results.length === 1 ? results[0] : results));
