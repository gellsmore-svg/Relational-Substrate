import { mkdir, writeFile } from 'node:fs/promises';
import { formatPredeclaration, predeclare } from './predeclaration-gate.mjs';

const outDir = new URL('./out/', import.meta.url);

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const frozenRule = {
  name: 'substituted peroxide OH-torsion qualitative gate v0',
  targetFamily: 'fresh R-OOH substituted peroxide with terminal hydroxyl torsion source data',
  descriptor: 'peroxide_anti_planar_release',
  releaseStrength: 0.25,
  releaseOnsetDegrees: 155,
  releaseSpanDegrees: 20,
  equilibriumAlphaUse:
    'use source-locked H-Y-X-C or H-O-O-C terminal hydroxyl torsion equilibrium angle when available; otherwise freeze the source-reported minimum alpha convention before scoring',
  scoringFormula:
    'penaltyIndex = 0.42 * effectiveTorsionDeviation + 0.58 * cisCrowding; effectiveTorsionDeviation = torsionDeviation * (1 - antiPlanarRelease * releaseStrength)',
  passFail:
    'pass only if predicted trans/cis penalty ratio is below 0.35 and source trans/cis barrier ratio is below 0.20, with predicted trans penalty lower than cis penalty',
};

const candidates = [
  {
    target: 'ethyl hydroperoxide',
    formula: 'C2H5OOH',
    freshness: 'not used in H2O2 or CH3OOH diagnostics',
    relation: 'same terminal hydroperoxide OH torsion family with larger alkyl substituent',
    sourceRisk: 'medium: likely spectroscopy/photochemistry literature, exact torsional barrier availability unverified',
    decision: 'reserve-for-source-lock',
    reason:
      'Best first evidence-counting target after CH3OOH because it keeps the R-OOH motif while changing alkyl topology beyond methyl.',
  },
  {
    target: 'tert-butyl hydroperoxide',
    formula: '(CH3)3COOH',
    freshness: 'not used',
    relation: 'same terminal hydroperoxide motif with bulky alkyl crowding',
    sourceRisk: 'medium-high: common molecule but conformer/torsion table may be harder to isolate',
    decision: 'backup-if-source-rich',
    reason:
      'Useful stress test of the same rule, but bulky substituent can mix OH torsion with alkyl steric effects.',
  },
  {
    target: 'hydroxymethyl hydroperoxide',
    formula: 'HOCH2OOH',
    freshness: 'not used',
    relation: 'same hydroperoxide motif with additional OH polarity channel',
    sourceRisk: 'high: atmospheric relevance but likely multiple conformers and limited simple torsion data',
    decision: 'defer',
    reason:
      'Chemically relevant but too many extra hydrogen-bond/polarity channels for the first evidence-counting substituted-peroxide gate.',
  },
];

const reserved = candidates.find((candidate) => candidate.decision === 'reserve-for-source-lock');
const target =
  `${reserved.target} (${reserved.formula}) fresh substituted R-OOH terminal hydroxyl torsion; source lock required before any barrier or scoring lookup`;

const pre = predeclare({
  target,
  modelForm: frozenRule.name,
  descriptors: [frozenRule.descriptor],
  heldOut: true,
  requireConventional: false,
});

const sourceLockRequirements = [
  'named source for same molecular identity and conformer family',
  'source-reported or source-derivable terminal OH torsion convention before scoring',
  'paired trans/cis or equivalent high/low OH torsion barrier comparator',
  'frozen alpha grid or explicit mapping from source torsion coordinates to alpha before scoring',
  'no release strength/onset/span changes after source values are read',
  'computed-comparator result must be labelled computed; experimental result may be labelled experimental only if barrier comparator is experimental',
];

const blockedActions = [
  'do not look up ethyl hydroperoxide torsion or barrier values inside this predeclaration artifact',
  'do not reuse CH3OOH extracted values as fresh evidence',
  'do not count a pass if the source lacks paired trans/cis OH torsion comparators',
  'do not promote this gate to evidence if the target changes after source lookup',
];

const report = {
  source: 'peroxide-substituted-rotor-evidence-predeclaration.mjs',
  date: '2026-06-23',
  status: 'evidence-counting substituted-peroxide gate predeclared; target reserved for source lock; no source lookup performed',
  frozenRule,
  reservedTarget: reserved,
  predeclaration: pre,
  candidates,
  sourceLockRequirements,
  blockedActions,
};

const predeclarationBlock = formatPredeclaration(pre)
  .replace('### Predeclaration (gate #1/#2)', '### Predeclaration (evidence-counting substituted-peroxide gate)')
  .replace('- Conventional comparators (control evidence only): ', '- Conventional comparators: not required for this molecule/torsion diagnostic');

const markdown = `# Substituted Peroxide Evidence Gate Predeclaration

## Scope

This freezes a future evidence-counting substituted-peroxide OH-torsion diagnostic before source lookup. It does not read source values, score a molecule, or increase evidence.

Date: ${report.date}

${predeclarationBlock}

## Frozen Rule

${table(
  ['Field', 'Value'],
  [
    ['Name', frozenRule.name],
    ['Target family', frozenRule.targetFamily],
    ['Descriptor', frozenRule.descriptor],
    ['Release parameters', `strength=${frozenRule.releaseStrength}; onset=${frozenRule.releaseOnsetDegrees}; span=${frozenRule.releaseSpanDegrees}`],
    ['Equilibrium alpha use', frozenRule.equilibriumAlphaUse],
    ['Scoring formula', frozenRule.scoringFormula],
    ['Pass/fail', frozenRule.passFail],
  ],
)}

## Candidate Screen

${table(
  ['Target', 'Formula', 'Freshness', 'Relation', 'Source risk', 'Decision', 'Reason'],
  candidates.map((row) => [row.target, row.formula, row.freshness, row.relation, row.sourceRisk, row.decision, row.reason]),
)}

## Reserved Target

${table(
  ['Field', 'Value'],
  [
    ['Target', reserved.target],
    ['Formula', reserved.formula],
    ['Reason', reserved.reason],
  ],
)}

## Source-Lock Requirements

${sourceLockRequirements.map((item) => `- ${item}`).join('\n')}

## Blocked Actions

${blockedActions.map((item) => `- ${item}`).join('\n')}

Status: ${report.status}
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('peroxide-substituted-rotor-evidence-predeclaration.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('peroxide-substituted-rotor-evidence-predeclaration.md', outDir), markdown);

console.log(markdown);
