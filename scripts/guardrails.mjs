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

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, '..');

const checks = [
  'analysis/ri-refractive-index-chain-runner.mjs',
  'analysis/ri-ca-scaffold-model-form-quarantine-diagnostic.mjs',
  'analysis/ri-pure-ca-si-o-source-exhaustion-screen.mjs',
  'analysis/external-material-refractive-index-challenge.mjs',
  'analysis/material-nbo-stoichiometry.mjs',
  'analysis/model-sensitivity-analysis.mjs',
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
