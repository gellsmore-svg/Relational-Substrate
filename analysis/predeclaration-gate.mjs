// Predeclaration + conventional-baseline gate (process recommendations #1 and #2).
//
// A HARD, throwing contract that scoring work must pass BEFORE any target is
// scored. It enforces, mechanically:
//   #1 every descriptor used is registered in descriptor-registry.json (no
//      post-hoc / unregistered descriptors), a model form is named, and a
//      target identity is declared — yielding a frozen, hashable predeclaration
//      record that a scored result can be tied back to;
//   #2 the declared descriptor set includes at least one CONVENTIONAL
//      comparator (e.g. density / lorentz_lorenz) so every material/optical
//      score carries a non-fitted baseline side-by-side, and conventional vs
//      substrate descriptors are separated in the record (conventional terms
//      are never counted as substrate support).
//
// Usage in a scoring step:
//   import { predeclare, requireScoringGate, formatPredeclaration } from './predeclaration-gate.mjs';
//   const pre = predeclare({ target: 'larnite Ca2SiO4 COD 9017424', modelForm: 'split-Ca topology gate',
//                            descriptors: ['ca_coordination','silicate_connectivity','lorentz_lorenz'], heldOut: true });
//   requireScoringGate(pre, { target: 'larnite Ca2SiO4 COD 9017424' }); // throws if not predeclared
//   // ...score only after this passes; emit formatPredeclaration(pre) into the report.
//
// Adoption note (per process-recommendations.md): this is the required path
// for NEW model-form / target-scoring work. Retrofitting the existing 33-step
// RI chain is a separate, reviewed change and is intentionally not done here.
//
// Run `node analysis/predeclaration-gate.mjs` (or `npm run gate:check`) to
// execute the self-test that proves the gate accepts a valid predeclaration
// and rejects unregistered descriptors, a missing conventional baseline, and
// scoring without a predeclaration.

import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';

const registry = JSON.parse(readFileSync(new URL('./descriptor-registry.json', import.meta.url), 'utf8'));
const REGISTRY_IDS = new Set(registry.descriptors.map((d) => d.id));
const CONVENTIONAL_IDS = new Set(registry.descriptors.filter((d) => d.conventional).map((d) => d.id));

export class PredeclarationError extends Error {
  constructor(message) {
    super(message);
    this.name = 'PredeclarationError';
  }
}

export function predeclare({ target, modelForm, descriptors, heldOut = null, requireConventional = true } = {}) {
  if (!target || typeof target !== 'string') {
    throw new PredeclarationError('predeclaration requires a target identity string (material + source lock).');
  }
  if (!modelForm || typeof modelForm !== 'string') {
    throw new PredeclarationError('predeclaration requires a named model form.');
  }
  if (!Array.isArray(descriptors) || descriptors.length === 0) {
    throw new PredeclarationError('predeclaration requires a non-empty descriptor set drawn from the registry.');
  }
  const unknown = descriptors.filter((id) => !REGISTRY_IDS.has(id));
  if (unknown.length) {
    throw new PredeclarationError(
      `descriptors not in registry (add a registry entry/PR before scoring): ${unknown.join(', ')}`,
    );
  }
  const conventionalComparators = descriptors.filter((id) => CONVENTIONAL_IDS.has(id));
  if (requireConventional && conventionalComparators.length === 0) {
    throw new PredeclarationError(
      'no conventional comparator declared (#2): include a non-fitted baseline such as density or lorentz_lorenz.',
    );
  }
  const substrateDescriptors = descriptors.filter((id) => !CONVENTIONAL_IDS.has(id));
  const hash = createHash('sha256')
    .update(JSON.stringify({ target, modelForm, descriptors: [...descriptors].sort(), registry: registry.version }))
    .digest('hex')
    .slice(0, 16);
  return Object.freeze({
    predeclaredAt: new Date().toISOString(),
    target,
    modelForm,
    descriptors: Object.freeze([...descriptors]),
    conventionalComparators: Object.freeze(conventionalComparators),
    substrateDescriptors: Object.freeze(substrateDescriptors),
    heldOut,
    registryVersion: registry.version,
    hash,
  });
}

// Hard gate. Call immediately before scoring; throws unless a valid
// predeclaration is present and (optionally) matches the scoring target.
export function requireScoringGate(predeclaration, { target } = {}) {
  if (!predeclaration || typeof predeclaration !== 'object' || !predeclaration.hash) {
    throw new PredeclarationError('scoring attempted without a valid predeclaration record.');
  }
  if (target && predeclaration.target !== target) {
    throw new PredeclarationError(
      `predeclaration target "${predeclaration.target}" does not match scoring target "${target}".`,
    );
  }
  if (!predeclaration.conventionalComparators || predeclaration.conventionalComparators.length === 0) {
    throw new PredeclarationError('scoring gate: predeclaration is missing a conventional baseline (#2).');
  }
  return true;
}

// Markdown block for a report, so the predeclaration is visible alongside the score.
export function formatPredeclaration(pre) {
  return [
    '### Predeclaration (gate #1/#2)',
    '',
    `- Target: ${pre.target}`,
    `- Model form: ${pre.modelForm}`,
    `- Held-out: ${pre.heldOut === null ? 'unspecified' : pre.heldOut}`,
    `- Substrate descriptors: ${pre.substrateDescriptors.join(', ') || '(none)'}`,
    `- Conventional comparators (control evidence only): ${pre.conventionalComparators.join(', ')}`,
    `- Registry: v${pre.registryVersion} · predeclaration hash: ${pre.hash}`,
  ].join('\n');
}

// --- self-test (proves the gate is actually hard) --------------------------
export function runGateSelfTest() {
  const results = [];
  const expectPass = (name, fn) => {
    try {
      fn();
      results.push({ name, ok: true });
    } catch (e) {
      results.push({ name, ok: false, detail: `unexpected throw: ${e.message}` });
    }
  };
  const expectThrow = (name, fn) => {
    try {
      fn();
      results.push({ name, ok: false, detail: 'expected a PredeclarationError but none was thrown' });
    } catch (e) {
      results.push({ name, ok: e instanceof PredeclarationError, detail: e instanceof PredeclarationError ? undefined : `wrong error type: ${e.name}` });
    }
  };

  const valid = ['ca_coordination', 'silicate_connectivity', 'lorentz_lorenz'];
  expectPass('valid predeclaration accepted', () => {
    const pre = predeclare({ target: 'selftest material', modelForm: 'selftest form', descriptors: valid, heldOut: true });
    requireScoringGate(pre, { target: 'selftest material' });
  });
  expectThrow('unregistered descriptor rejected', () =>
    predeclare({ target: 't', modelForm: 'f', descriptors: ['ca_coordination', 'not_a_registered_descriptor'] }),
  );
  expectThrow('missing conventional baseline rejected', () =>
    predeclare({ target: 't', modelForm: 'f', descriptors: ['ca_coordination', 'silicate_connectivity'] }),
  );
  expectThrow('empty descriptor set rejected', () =>
    predeclare({ target: 't', modelForm: 'f', descriptors: [] }),
  );
  expectThrow('scoring without predeclaration rejected', () => requireScoringGate(null, { target: 't' }));
  expectThrow('target mismatch rejected', () => {
    const pre = predeclare({ target: 'a', modelForm: 'f', descriptors: valid });
    requireScoringGate(pre, { target: 'b' });
  });

  return { passed: results.every((r) => r.ok), results };
}

// run as main → execute the self-test
if (import.meta.url === `file://${process.argv[1]}`) {
  const { passed, results } = runGateSelfTest();
  console.log('Predeclaration gate self-test:');
  for (const r of results) console.log(`  ${r.ok ? '✓' : '✗'} ${r.name}${r.ok ? '' : ` — ${r.detail}`}`);
  console.log(passed ? '\nGate self-test passed (the gate is hard).' : '\nGate self-test FAILED.');
  process.exit(passed ? 0 : 1);
}
