import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const target = {
  molecule: 'methyl hydroperoxide',
  formula: 'CH3OOH',
  reservedBy: 'peroxide-fresh-rotor-target-reservation.mjs',
  reservedRole: 'fresh substituted peroxide O-O rotor target for peroxide anti-planar release repair candidate',
  frozenRepair: {
    releaseStrength: 0.25,
    releaseOnsetDegrees: 155,
    releaseSpanDegrees: 20,
  },
};

const sourceCandidates = [
  {
    role: 'experimental spectroscopy / source-grade molecular identity',
    citation:
      'M. Tyblewski, T.-K. Ha, R. Meyer, A. Bauder, and C. E. Blom, J. Chem. Phys. 97, 6168-6180 (1992)',
    doi: '10.1063/1.463725',
    url: 'https://pubs.aip.org/aip/jcp/article-pdf/97/9/6168/19306060/6168_1_online.pdf',
    sourceType: 'microwave and millimeter-wave spectroscopy with ab initio support',
    usefulBecause:
      'Investigates CH3OOH from 12-307 GHz; assigns rotational and torsional-rotational transitions; reports gauche equilibrium configuration and internal-rotation analysis.',
    lockedUse:
      'candidate source for equilibrium geometry convention, internal-rotation state structure, and spectroscopic identity',
    extractionStatus: 'source candidate found; full table extraction still pending',
  },
  {
    role: 'theoretical torsion/barrier source',
    citation:
      'S. Dalbouha, M. L. Senent, and N. Komiha, J. Chem. Phys. 142, 074304 (2015)',
    doi: '10.1063/1.4907941',
    url: 'https://pubs.aip.org/aip/jcp/article/142/7/074304/900501/Theoretical-spectroscopic-characterization-at-low',
    sourceType: 'high-level ab initio spectroscopic prediction',
    usefulBecause:
      'Uses CCSD(T) and CCSD(T)-F12 methods for CH3OOH and sulfur analogs; provides rotational parameters, anharmonic frequencies, torsional barriers, torsional levels, and splittings.',
    lockedUse:
      'candidate source for torsional energy barriers and target comparator rows if experimental barrier extraction is insufficient',
    extractionStatus: 'source candidate found; numerical target extraction still pending',
  },
  {
    role: 'secondary spectral context',
    citation: 'J. Matthews and A. Sinha, J. Phys. Chem. A 113, 13100 (2009)',
    doi: '10.1021/jp902146z',
    url: 'https://pubs.acs.org/doi/10.1021/jp902146z',
    sourceType: 'rotational contour / OH-stretch action spectra',
    usefulBecause:
      'Provides jet-cooled spectral context for CH3OOH; useful for identity/spectral sanity but not the primary torsional scoring source.',
    lockedUse: 'context only unless primary torsion data cannot be extracted elsewhere',
    extractionStatus: 'backup/context source',
  },
];

const sourceLockDecision = {
  status: 'provisional source-lock path found; scoring still blocked',
  primarySource: sourceCandidates[0].citation,
  theoryCrossCheck: sourceCandidates[1].citation,
  reason:
    'The reserved target has at least one experimental spectroscopy source and one high-level theoretical torsion/barrier source tied to the same CH3OOH identity.',
};

const extractionPlan = [
  {
    step: 'extract geometry/torsion convention',
    source: 'Tyblewski et al. 1992 first; Dalbouha et al. 2015 as cross-check',
    block: 'do not alter the frozen repair parameters after extraction',
  },
  {
    step: 'extract target comparator',
    source: 'prefer experimental torsional/tunneling barrier if directly reported; otherwise use declared theoretical barrier from the 2015 source as source-grade computed comparator',
    block: 'record whether comparator is experimental, theoretical, or mixed; do not count mixed-source ambiguity as validation',
  },
  {
    step: 'freeze scoring grid',
    source: 'derive from the reserved CH3OOH rotor identity before model evaluation',
    block: 'no grid change after seeing whether the candidate passes',
  },
  {
    step: 'score only after extraction report',
    source: 'new scoring script must consume the extraction artifact',
    block: 'do not score directly from this source-lock screen',
  },
];

const blockedActions = [
  'do not score CH3OOH in this source-lock artifact',
  'do not tune release strength/onset/span from source values',
  'do not replace the reserved target after seeing source values unless the screen explicitly fails source lock',
  'do not count a theoretical-only pass as equivalent to experimental validation without labelling it as computed-comparator evidence',
];

const report = {
  source: 'peroxide-methyl-hydroperoxide-source-lock-screen.mjs',
  date: '2026-06-23',
  target,
  sourceCandidates,
  sourceLockDecision,
  extractionPlan,
  blockedActions,
};

const markdown = `# Methyl Hydroperoxide Source-Lock Screen

## Scope

This report follows the pre-lookup reservation of methyl hydroperoxide as the fresh peroxide-family rotor target. It records source candidates and an extraction plan only. It does not extract final scoring values, does not score the target, and does not change the frozen repair candidate.

Date: ${report.date}

## Reserved Target

${table(
  ['Field', 'Value'],
  [
    ['Molecule', target.molecule],
    ['Formula', target.formula],
    ['Reserved by', target.reservedBy],
    ['Reserved role', target.reservedRole],
    ['Frozen repair', `strength=${target.frozenRepair.releaseStrength}; onset=${target.frozenRepair.releaseOnsetDegrees}; span=${target.frozenRepair.releaseSpanDegrees}`],
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
    ['Primary source', sourceLockDecision.primarySource],
    ['Theory cross-check', sourceLockDecision.theoryCrossCheck],
    ['Reason', sourceLockDecision.reason],
  ],
)}

## Extraction Plan

${table(
  ['Step', 'Source', 'Block'],
  extractionPlan.map((row) => [row.step, row.source, row.block]),
)}

## Blocked Actions

${blockedActions.map((item) => `- ${item}`).join('\n')}

## Decision

The reserved CH3OOH target has a plausible source-lock path: Tyblewski et al. 1992 for experimental microwave/mm-wave spectroscopy and Dalbouha et al. 2015 for high-level torsional barrier/level data. The next allowed step is a separate extraction artifact. Scoring remains blocked.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('peroxide-methyl-hydroperoxide-source-lock-screen.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('peroxide-methyl-hydroperoxide-source-lock-screen.md', outDir), markdown);

console.log(markdown);
