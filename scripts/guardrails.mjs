#!/usr/bin/env node
/**
 * Basic guardrails checker for Relational Substrate.
 * Run via: node scripts/guardrails.mjs
 *
 * Enforces:
 * - Syntax checks on key analysis and report scripts
 * - Presence and basic validity of descriptor-registry.json (when present)
 * - Reminder of predeclaration and conventional baseline rules
 *
 * This is intentionally lightweight. It strengthens existing hygiene without
 * adding heavy dependencies.
 */

import { readFile } from 'node:fs/promises';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { runGateSelfTest } from '../analysis/predeclaration-gate.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, '..');

const checks = [
  'analysis/ri-refractive-index-chain-runner.mjs',
  'analysis/ri-ca-scaffold-model-form-quarantine-diagnostic.mjs',
  'analysis/ri-structural-model-form-predeclaration.mjs',
  'analysis/ri-pure-ca-si-o-source-exhaustion-screen.mjs',
  'analysis/external-material-refractive-index-challenge.mjs',
  'analysis/material-nbo-stoichiometry.mjs',
  'analysis/peroxide-anti-planar-release-sensitivity.mjs',
  'analysis/peroxide-release-repair-predeclaration.mjs',
  'analysis/peroxide-fresh-rotor-target-reservation.mjs',
  'analysis/peroxide-methyl-hydroperoxide-source-lock-screen.mjs',
  'analysis/peroxide-methyl-hydroperoxide-source-extraction.mjs',
  'analysis/peroxide-methyl-hydroperoxide-scoring-diagnostic.mjs',
  'analysis/peroxide-substituted-rotor-evidence-predeclaration.mjs',
  'analysis/peroxide-ethyl-hydroperoxide-source-lock-screen.mjs',
  'analysis/peroxide-ethyl-hydroperoxide-search-hint-diagnostic.mjs',
  'analysis/peroxide-ethyl-hydroperoxide-source-extraction.mjs',
  'analysis/peroxide-ethyl-hydroperoxide-evidence-scoring.mjs',
  'analysis/peroxide-evidence-ledger-policy.mjs',
  'analysis/peroxide-release-promotion-review.mjs',
  'analysis/peroxide-dual-channel-model-form-predeclaration.mjs',
  'analysis/peroxide-dual-channel-feasibility-diagnostic.mjs',
  'analysis/peroxide-dual-channel-target-reservation.mjs',
  'analysis/peroxide-dimethyl-source-lock-screen.mjs',
  'analysis/peroxide-observable-route-model-form-predeclaration.mjs',
  'analysis/peroxide-observable-route-feasibility-diagnostic.mjs',
  'analysis/peroxide-observable-route-target-reservation.mjs',
  'analysis/peroxide-diethyl-source-lock-screen.mjs',
  'analysis/peroxide-source-availability-screen.mjs',
  'analysis/peroxide-tbhp-target-reservation.mjs',
  'analysis/peroxide-tbhp-source-lock-screen.mjs',
  'analysis/peroxide-tbhp-source-extraction.mjs',
  'analysis/peroxide-tbhp-observable-route-scoring.mjs',
  'analysis/peroxide-intermediate-route-source-availability.mjs',
  'analysis/peroxide-peroxyformic-target-reservation.mjs',
  'analysis/peroxide-peroxyformic-source-lock-screen.mjs',
  'analysis/peroxide-peroxyformic-profile-scoring.mjs',
  'analysis/peroxide-equilibrium-relative-crowding-predeclaration.mjs',
  'analysis/peroxide-equilibrium-relative-crowding-diagnostic.mjs',
  'analysis/peroxide-v2-fresh-target-reservation.mjs',
  'analysis/peroxide-hmhp-source-lock-screen.mjs',
  'analysis/peroxide-v2-source-availability-screen.mjs',
  'analysis/peroxide-methyl-chloroperoxide-reservation.mjs',
  'analysis/peroxide-methyl-chloroperoxide-source-lock-screen.mjs',
  'analysis/heteroatom-trans-topology-repair-diagnostic.mjs',
  'analysis/neutral-hydrazine-torsion-target-reservation.mjs',
  'analysis/neutral-hydrazine-torsion-source-lock-screen.mjs',
  'analysis/roughness-psd-brdf-model-form-predeclaration.mjs',
  'analysis/roughness-tungsten-brdf-target-reservation.mjs',
  'analysis/roughness-tungsten-brdf-source-lock-screen.mjs',
  'analysis/roughness-psd-brdf-source-availability-screen.mjs',
  'analysis/roughness-tayabaly-brdf-target-reservation.mjs',
  'analysis/roughness-tayabaly-brdf-source-lock-screen.mjs',
  'analysis/roughness-profile-psd-scatter-psd-predeclaration.mjs',
  'analysis/roughness-psd-brdf-model.mjs',
  'analysis/roughness-psd-brdf-feasibility-diagnostic.mjs',
  'analysis/run-roughness-psd-brdf-case.mjs',
  'analysis/model-sensitivity-analysis.mjs',
  'analysis/model-parameter-experiments.mjs',
  'analysis/run-parameter-recipe.mjs',
  'analysis/evidence-ledger.mjs',
  'analysis/predeclaration-gate.mjs',
  'analysis/run-exported-case.mjs',
  'scripts/generate-reports.mjs',
];

async function checkSyntax(file) {
  return new Promise((resolve) => {
    const proc = spawn(process.execPath, ['--check', file], { stdio: 'inherit' });
    proc.on('close', (code) => resolve(code === 0));
  });
}

async function main() {
  console.log('Running Relational Substrate guardrails...\n');

  let allGood = true;

  // Syntax checks
  console.log('Syntax checks:');
  for (const rel of checks) {
    const full = resolve(root, rel);
    const ok = await checkSyntax(full);
    console.log(`  ${ok ? '✓' : '✗'} ${rel}`);
    if (!ok) allGood = false;
  }

  // Descriptor registry (if present)
  console.log('\nDescriptor registry:');
  try {
    const regPath = resolve(root, 'analysis/descriptor-registry.json');
    const reg = JSON.parse(await readFile(regPath, 'utf8'));
    const hasDescriptors = Array.isArray(reg.descriptors) && reg.descriptors.length > 0;
    const hasRules = reg.rules && typeof reg.rules === 'object';
    console.log(`  ✓ Found and parsed (v${reg.version || 'unknown'})`);
    console.log(`    descriptors: ${reg.descriptors?.length || 0}`);
    if (!hasDescriptors || !hasRules) {
      console.log('  ! Registry is missing expected structure (descriptors + rules)');
      allGood = false;
    } else {
      console.log('  ✓ Basic structure present (predeclaration and conventional rules expected)');
    }
  } catch (e) {
    console.log('  ! No analysis/descriptor-registry.json found or unreadable. Consider creating one for new model forms.');
    // Not fatal — registry is a new recommendation
  }

  // Predeclaration + conventional-baseline gate self-test (#1/#2): prove the
  // hard gate still rejects unregistered descriptors and a missing baseline.
  console.log('\nPredeclaration gate (#1/#2) self-test:');
  try {
    const { passed, results } = runGateSelfTest();
    for (const r of results) {
      console.log(`  ${r.ok ? '✓' : '✗'} ${r.name}${r.ok ? '' : ` — ${r.detail}`}`);
    }
    if (!passed) allGood = false;
  } catch (e) {
    console.log(`  ! gate self-test could not run: ${e.message}`);
    allGood = false;
  }

  console.log('\nProcess reminders (from review):');
  console.log('  - Predeclare any new model form / descriptor set before scoring targets.');
  console.log('  - Always surface a clean conventional baseline (density/Lorentz-Lorenz) side-by-side.');
  console.log('  - Label all conventional terms explicitly; never count them as substrate evidence.');
  console.log('  - Use only source-locked primary data (CIF + measured n + density).');

  console.log('\n' + (allGood ? 'Guardrails passed (basic checks).' : 'Some checks failed — see above.'));
  process.exit(allGood ? 0 : 1);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
