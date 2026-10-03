import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const reservation = JSON.parse(
  await readFile(
    new URL('peroxide-substituted-rotor-evidence-predeclaration.json', outDir),
    'utf8',
  ),
);

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const target = {
  molecule: 'ethyl hydroperoxide',
  formula: 'C2H5OOH',
  reservedBy: 'peroxide-substituted-rotor-evidence-predeclaration.mjs',
  predeclarationHash: reservation.predeclaration.hash,
  reservedRole: 'fresh substituted R-OOH terminal hydroxyl torsion target',
  frozenRule: {
    releaseStrength: 0.25,
    releaseOnsetDegrees: 155,
    releaseSpanDegrees: 20,
    passFail:
      'predicted trans/cis penalty ratio < 0.35 and source trans/cis barrier ratio < 0.20, with predicted trans penalty lower than cis penalty',
  },
};

const sourceCandidates = [
  {
    role: 'primary torsional barrier candidate',
    citation:
      'G. S. Maciel, A. C. P. Bitencourt, M. Ragni, and V. Aquilanti, Int. J. Quantum Chem. 107, 2697-2707 (2007)',
    doi: '10.1002/qua.21462',
    url: 'https://onlinelibrary.wiley.com/doi/abs/10.1002/qua.21462',
    sourceType: 'alkyl peroxide torsional potential study',
    usefulBecause:
      'Abstract explicitly includes C2H5OOH among chiral alkyl peroxides and discusses cis/trans barriers and torsional level energies.',
    lockedUse:
      'candidate primary source for ethyl hydroperoxide trans/cis torsion barriers if full text/table can be accessed',
    extractionStatus: 'primary provenance source found; direct full text still not accessible, but follow-up source exposes HOOEt table',
  },
  {
    role: 'torsional dynamics cross-check',
    citation:
      'A. C. P. Bitencourt, M. Ragni, G. S. Maciel, V. Aquilanti, and F. V. Prudente, J. Chem. Phys. 129, 154316 (2008)',
    doi: '10.1063/1.2992554',
    url: 'https://pubs.aip.org/aip/jcp/article/129/15/154316/897855/Level-distributions-partition-functions-and-rates',
    sourceType: 'O-O torsional level distributions / partition functions',
    usefulBecause:
      'Article metadata names HOOEt in the studied derivative set and states that previously determined potential-energy profiles along the dihedral angle are used.',
    lockedUse:
      'candidate cross-check for torsional level distribution and prior-potential provenance, not enough alone unless barrier tables are extractable',
    extractionStatus: 'source-locked via UFBA repository PDF; Table I exposes HOOEt geometry and barriers',
  },
  {
    role: 'experimental spectroscopy context',
    citation:
      'J. P. Kercher, C. A. Blacquiere, M. K. Hazra, J. S. Francisco, and A. Sinha, J. Phys. Chem. A 112, 10215-10221 (2008)',
    doi: '10.1021/jp076803r',
    url: 'https://pubs.acs.org/doi/10.1021/jp076803r',
    sourceType: 'ethyl hydroperoxide OH overtone photodissociation / vibrational-torsional model',
    usefulBecause:
      'Abstract reports ethyl hydroperoxide vibrational-torsional spectra and simulated trans/gauche conformer spectra.',
    lockedUse:
      'spectroscopic identity and conformer-context source; not primary unless it reports paired trans/cis OH torsion barriers',
    extractionStatus: 'source candidate found; full text/table not accessible in current session',
  },
  {
    role: 'experimental spectroscopy context',
    citation: 'O-H Stretch Overtone Excitation of Ethyl Hydroperoxide Conformers, J. Phys. Chem. A (2011)',
    doi: '10.1021/jp208467f',
    url: 'https://pubs.acs.org/doi/abs/10.1021/jp208467f',
    sourceType: 'laser photoacoustic OH-stretch overtone spectra with ab initio spectral simulations',
    usefulBecause:
      'Reports ethyl hydroperoxide conformer spectra for 3-6 OH-stretch quanta and ab initio spectral simulations.',
    lockedUse: 'backup spectroscopy/context source',
    extractionStatus: 'source candidate found; exact barrier suitability not verified',
  },
];

const supersededSearchIndexHints = [
  {
    source: 'web search preview for Bitencourt et al. 2008 AIP PDF',
    url: 'https://pubs.aip.org/aip/jcp/article-pdf/doi/10.1063/1.2992554/14904074/154316_1_online.pdf',
    targetRow: 'HOOH diatom-diatom line, not HOOEt',
    hintedValues: {
      VcisCm1: 2645.33,
      VtransCm1: 396.81,
      transCisRatio: Number((396.81 / 2645.33).toFixed(4)),
    },
    status: 'superseded non-target search-index hint',
    reason:
      'The full PDF extraction shows these values belong to the HOOH diatom-diatom line, not the HOOEt row. The HOOEt source-locked row is Vcis=2270.55 cm-1 and Vtrans=236.46 cm-1.',
  },
];

const sourceLockDecision = {
  status: 'source-locked; extraction available',
  primaryCandidate: sourceCandidates[0].citation,
  crossCheckCandidate: sourceCandidates[1].citation,
  reason:
    'The reserved target has source candidates explicitly tied to ethyl hydroperoxide torsional potentials. A repository-hosted Bitencourt et al. 2008 PDF exposes the required HOOEt geometry and paired trans/cis barrier table.',
};

const extractionPlan = [
  {
    step: 'obtain full text/table for Maciel et al. 2007',
    source: 'Wiley DOI 10.1002/qua.21462',
    block: 'do not score from abstract-only qualitative trends',
  },
  {
    step: 'extract paired ethyl hydroperoxide trans/cis OH torsion barriers',
    source: 'Maciel et al. 2007 first; Bitencourt et al. 2008 as provenance/cross-check',
    block: 'if paired trans/cis barriers are absent, mark source lock failed rather than changing target after lookup',
  },
  {
    step: 'freeze source torsion mapping',
    source: 'use source dihedral convention and map to the predeclared alpha coordinate before scoring',
    block: 'no alpha-grid or formula changes after numeric extraction',
  },
  {
    step: 'score only from extraction artifact',
    source: 'future ethyl hydroperoxide extraction JSON',
    block: 'do not score directly from this source-lock screen',
  },
];

const blockedActions = [
  'do not score ethyl hydroperoxide from abstract-level source text',
  'do not substitute CH3OOH or tert-butyl hydroperoxide after seeing source availability without recording source-lock failure',
  'do not tune the frozen release parameters or pass/fail thresholds',
  'do not count spectroscopy context as barrier validation unless paired trans/cis barrier values are present',
];

const report = {
  source: 'peroxide-ethyl-hydroperoxide-source-lock-screen.mjs',
  date: '2026-06-23',
  target,
  sourceCandidates,
  supersededSearchIndexHints,
  sourceLockDecision,
  extractionPlan,
  blockedActions,
};

const markdown = `# Ethyl Hydroperoxide Source-Lock Screen

## Scope

This report follows the predeclared substituted-peroxide evidence gate and source-locks the reserved ethyl hydroperoxide target as far as current accessible sources allow. It does not extract final scoring values, does not score the target, and does not change the frozen rule.

Date: ${report.date}

## Reserved Target

${table(
  ['Field', 'Value'],
  [
    ['Molecule', target.molecule],
    ['Formula', target.formula],
    ['Reserved by', target.reservedBy],
    ['Predeclaration hash', target.predeclarationHash],
    ['Reserved role', target.reservedRole],
    ['Frozen release', `strength=${target.frozenRule.releaseStrength}; onset=${target.frozenRule.releaseOnsetDegrees}; span=${target.frozenRule.releaseSpanDegrees}`],
    ['Pass/fail', target.frozenRule.passFail],
  ],
)}

## Source Candidates

${table(
  ['Role', 'Citation', 'DOI', 'Source type', 'Useful because', 'Locked use', 'Extraction status'],
  sourceCandidates.map((row) => [
    row.role,
    row.citation,
    row.doi,
    row.sourceType,
    row.usefulBecause,
    row.lockedUse,
    row.extractionStatus,
  ]),
)}

## Source-Lock Decision

${table(
  ['Field', 'Value'],
  [
    ['Status', sourceLockDecision.status],
    ['Primary candidate', sourceLockDecision.primaryCandidate],
    ['Cross-check candidate', sourceLockDecision.crossCheckCandidate],
    ['Reason', sourceLockDecision.reason],
  ],
)}

## Superseded Search-Index Hint

${table(
  ['Source', 'Target row', 'Vtrans', 'Vcis', 'Ratio', 'Status', 'Reason'],
  supersededSearchIndexHints.map((row) => [
    row.source,
    row.targetRow,
    `${row.hintedValues.VtransCm1} cm-1`,
    `${row.hintedValues.VcisCm1} cm-1`,
    row.hintedValues.transCisRatio,
    row.status,
    row.reason,
  ]),
)}

## Extraction Plan

${table(
  ['Step', 'Source', 'Block'],
  extractionPlan.map((row) => [row.step, row.source, row.block]),
)}

## Blocked Actions

${blockedActions.map((item) => `- ${item}`).join('\n')}

## Decision

Ethyl hydroperoxide remains the correctly predeclared evidence target. Source lock is now available through the repository-hosted Bitencourt et al. 2008 PDF; extraction and scoring must consume the dedicated extraction artifact rather than this screen.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('peroxide-ethyl-hydroperoxide-source-lock-screen.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('peroxide-ethyl-hydroperoxide-source-lock-screen.md', outDir), markdown);

console.log(markdown);
