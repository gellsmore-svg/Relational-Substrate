import { mkdir, writeFile } from 'node:fs/promises';
import { formatPredeclaration, predeclare, requireScoringGate } from './predeclaration-gate.mjs';

const outDir = new URL('./out/', import.meta.url);

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const modelForm = 'source-locked structural RI model form v0';
const target =
  'future source-locked material RI target; exact material, optical constants, density, and paired CIF must be reserved before scoring';
const descriptors = [
  'ca_coordination',
  'mean_ca_o_distance',
  't_site_polarizability',
  'silicate_connectivity',
  'density',
  'lorentz_lorenz',
];

const pre = predeclare({
  target,
  modelForm,
  descriptors,
  heldOut: true,
});

// Prove the declared descriptor set clears the hard gate, while still leaving
// target-specific scoring blocked until a concrete source lock exists.
requireScoringGate(pre, { target });

const descriptorRoles = [
  {
    id: 'ca_coordination',
    role: 'substrate-facing structural gate',
    extraction: 'mean Ca coordination from the paired CIF using one documented cutoff/extractor',
    boundary: 'not a coefficient by itself; classifies Ca scaffold environment before scoring',
  },
  {
    id: 'mean_ca_o_distance',
    role: 'substrate-facing structural gate',
    extraction: 'mean Ca-O distance from the same Ca coordination polyhedra',
    boundary: 'thresholds must be frozen from source rows before any optical target score',
  },
  {
    id: 't_site_polarizability',
    role: 'substrate-facing T-site response descriptor',
    extraction: 'field-strength-weighted T-site occupant response with a versioned radii/polarizability table',
    boundary: 'replaces ad hoc Al/O boosts; no target-implied coefficient is allowed',
  },
  {
    id: 'silicate_connectivity',
    role: 'substrate-facing topology class',
    extraction: 'CIF-derived connectivity class such as orthosilicate, sorosilicate, chain, framework, or ring',
    boundary: 'must be categorical or frozen-encoded before scoring; no post-score relabelling',
  },
  {
    id: 'density',
    role: 'conventional comparator',
    extraction: 'measured density preferred; calculated density allowed only with explicit provenance',
    boundary: 'control evidence only; never counted as substrate support',
  },
  {
    id: 'lorentz_lorenz',
    role: 'conventional comparator',
    extraction: 'Lorentz-Lorenz control from paired optical constants and density',
    boundary: 'baseline comparator; substrate terms must add held-out value beyond this',
  },
];

const freezeRules = [
  'do not score another material RI target under baseline, split-Ca, or split-Ca/Mg families',
  'do not score any target until its material identity, optical constants, measured density, and paired CIF are source-locked',
  'do not reuse rankinite, kilchoanite, larnite, merwinite, or spurrite as fresh held-out validation',
  'freeze descriptor extraction code, thresholds, model equation, coefficients, and pass/fail tolerance before target optical scoring',
  'report density and Lorentz-Lorenz as conventional control evidence only',
  'report value added only on held-out rows, not on calibration rows or already-exposed failures',
];

const blockedShortcuts = [
  {
    shortcut: 'target-implied coefficient repair',
    reason: 'previous framework-Al and cation-response coefficients failed fresh validation pressure',
  },
  {
    shortcut: 'scalar Ca/O uplift',
    reason: 'split-Ca and split-Ca/Mg families are quarantined after hardystonite, rankinite, kilchoanite, larnite, and spurrite failures',
  },
  {
    shortcut: 'broad mineral-page optical rows',
    reason: 'wollastonite remains blocked because optical/density rows are not polytype-locked to a paired CIF',
  },
  {
    shortcut: 'conventional density pass as substrate evidence',
    reason: 'density and Lorentz-Lorenz are comparator controls and cannot raise unification confidence by themselves',
  },
];

const nextGate = [
  {
    step: 'target source lock',
    passCondition: 'one material/polytype has optical constants, density, and CIF tied to the same identity',
  },
  {
    step: 'pre-score classification',
    passCondition: 'the target is classified under the frozen descriptor extractors before RI prediction is computed',
  },
  {
    step: 'conventional comparator',
    passCondition: 'density/Lorentz-Lorenz baseline is reported side-by-side before any substrate-facing claim',
  },
  {
    step: 'held-out score',
    passCondition: 'prediction clears the frozen tolerance without changing descriptor extraction, equation, or coefficients',
  },
];

const report = {
  source: 'ri-structural-model-form-predeclaration.mjs',
  date: '2026-06-22',
  status:
    'structural RI model form predeclared; target-specific scoring remains blocked until a clean source-locked held-out target is reserved',
  predeclaration: pre,
  descriptorRoles,
  freezeRules,
  blockedShortcuts,
  nextGate,
};

const markdown = `# RI Structural Model-Form Predeclaration

## Scope

This diagnostic records the next allowed material refractive-index model form after the Ca-scaffold quarantine. It does not score a target, does not fit a coefficient, and does not promote a new RI repair. Its purpose is to freeze the descriptor boundary for the next source-locked RI attempt before any held-out optical target is scored.

Date: ${report.date}

${formatPredeclaration(pre)}

## Descriptor Roles

${table(
  ['Descriptor', 'Role', 'Extraction freeze', 'Boundary'],
  descriptorRoles.map((row) => [row.id, row.role, row.extraction, row.boundary]),
)}

## Freeze Rules

${freezeRules.map((rule) => `- ${rule}`).join('\n')}

## Blocked Shortcuts

${table(
  ['Shortcut', 'Reason blocked'],
  blockedShortcuts.map((row) => [row.shortcut, row.reason]),
)}

## Next Scoring Gate

${table(
  ['Step', 'Pass condition'],
  nextGate.map((row) => [row.step, row.passCondition]),
)}

## Decision

The next RI work may design a source-locked structural predictor using the declared descriptor set, but it may not score another target until a concrete material/polytype source lock exists and a target-specific predeclaration is emitted. This model-form predeclaration is necessary but not sufficient for validation.

Status: ${report.status}

## Reading

The RI front has moved from "which Ca-scaffold repair works?" to "can a structurally source-locked predictor beat a conventional optical comparator on a fresh held-out material?" That is the right pressure point. The declared substrate-facing descriptors are structural and topological; the declared conventional descriptors are controls. Any future pass has to show value beyond density/Lorentz-Lorenz without reusing already-exposed rows as fresh evidence.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-structural-model-form-predeclaration.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('ri-structural-model-form-predeclaration.md', outDir), markdown);

console.log(markdown);
