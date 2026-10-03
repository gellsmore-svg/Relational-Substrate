import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const reservation = JSON.parse(
  await readFile(
    new URL('peroxide-observable-route-target-reservation.json', outDir),
    'utf8',
  ),
);

const target = {
  molecule: 'diethyl peroxide',
  formula: 'C2H5OOC2H5',
  reservedBy: 'peroxide-observable-route-target-reservation.mjs',
  predeclarationHash: reservation.predeclaration.hash,
};

const primarySource = {
  citation:
    'H. Yue et al., Dimeric Product of Peroxy Radical Self-Reaction Probed with VUV Photoionization Mass Spectrometry and Theoretical Calculations: The Case of C2H5OOC2H5, Int. J. Mol. Sci. 24, 3731 (2023)',
  doi: '10.3390/ijms24043731',
  articleUrl: 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9965172/',
  repositoryUrl: 'https://hal.science/hal-04248375v1',
  localPdf: 'analysis/source-cache/lin-2023-diethyl-peroxide.pdf',
  localText: 'analysis/source-cache/lin-2023-diethyl-peroxide.txt',
  localSupplementPdf: 'analysis/source-cache/lin-2023-diethyl-peroxide-supplement.pdf',
  localSupplementText: 'analysis/source-cache/lin-2023-diethyl-peroxide-supplement.txt',
};

const equilibriumExtraction = {
  construct: 'potential-energy equilibrium geometry',
  method: 'CCSD(T)-F12/aug-cc-pVTZ',
  sourceLocation: 'main article Figure 5 and supplementary Table S1',
  atomOrder: 'C-left, O-left, O-right, C-right',
  coordinatesAngstrom: [
    [-1.500797, -0.492605, 0.232234],
    [-0.635888, 0.316853, -0.545016],
    [0.635888, -0.316842, -0.545022],
    [1.500798, 0.492601, 0.232243],
  ],
  derivedCOOCDihedralDegrees: 110.009,
  derivation:
    'standard signed four-point dihedral from the source Cartesian coordinates; absolute value used under the frozen 0-180-degree torsion convention',
  sourceReportedOOAngstrom: 1.421,
};

const comparatorScreen = [
  {
    candidate: 'isolated-product O-O torsional scan',
    result: 'not present',
    reason:
      'the article optimizes the neutral/cation structures and calculates the C2H5O2 self-reaction PES, but does not report an isolated C-O-O-C constrained torsion profile',
  },
  {
    candidate: 'self-reaction transition-state energies',
    result: 'rejected',
    reason:
      'reaction-path energies describe formation chemistry, not nonlocal conformers of isolated diethyl peroxide',
  },
  {
    candidate: 'neutral-to-cation structural change',
    result: 'rejected',
    reason:
      'ionization changes electronic state and O-O bond length; it is not a same-surface torsion comparator',
  },
  {
    candidate: 'older infrared spectrum',
    result: 'insufficient',
    reason:
      'provides vibrational identification/context but no source-defined nonlocal C-O-O-C coordinate with barrier energy',
  },
];

const sourceLockDecision = {
  status: 'source-lock-failed-paired-torsional-comparator',
  equilibriumGeometryLocked: true,
  nonlocalComparatorLocked: false,
  scoringAllowed: false,
  evidenceStatus: 'none',
  reason:
    'The equilibrium torsion is source-locked, but no accessible source supplies the predeclared same-surface nonlocal torsion coordinate and energy ordering. The target must be recorded as a source-lock failure.',
};

const blockedActions = [
  'do not treat the self-reaction PES as an isolated-product torsional PES',
  'do not use the cation geometry as a nonlocal neutral conformer',
  'do not generate an unpredeclared quantum-chemistry scan and call it external validation',
  'do not change the 45-degree selection tolerance or live energy release parameters',
  'do not switch targets without retaining this failed source-lock result',
];

const possibleRecovery = {
  userDownloadNeededNow: false,
  reason:
    'The relevant open-access article and supplement were obtained directly. A download would help only if a specific independent paper with a diethyl-peroxide O-O torsional scan or barrier table is identified.',
  searchCandidate:
    'continue literature search for an isolated diethyl-peroxide hindered-rotation calculation; otherwise predeclare a source-availability screen before selecting the next target',
};

const report = {
  source: 'peroxide-diethyl-source-lock-screen.mjs',
  date: '2026-06-23',
  target,
  primarySource,
  equilibriumExtraction,
  comparatorScreen,
  sourceLockDecision,
  blockedActions,
  possibleRecovery,
};

const markdown = `# Diethyl Peroxide Source-Lock Screen

## Decision

Status: **${sourceLockDecision.status}**

- equilibrium geometry locked: yes
- nonlocal torsional comparator locked: no
- scoring allowed: no
- evidence status: none

${sourceLockDecision.reason}

## Locked Equilibrium Geometry

| Field | Value |
|---|---|
| construct | ${equilibriumExtraction.construct} |
| method | ${equilibriumExtraction.method} |
| source location | ${equilibriumExtraction.sourceLocation} |
| atom order | ${equilibriumExtraction.atomOrder} |
| derived C-O-O-C torsion | ${equilibriumExtraction.derivedCOOCDihedralDegrees} degrees |
| source-reported O-O length | ${equilibriumExtraction.sourceReportedOOAngstrom} A |

The torsion was derived from the source Cartesian coordinates using the
standard four-point dihedral formula.

## Comparator Screen

| Candidate | Result | Reason |
|---|---|---|
${comparatorScreen.map((row) => `| ${row.candidate} | ${row.result} | ${row.reason} |`).join('\n')}

## Download Requirement

User download needed now: **no**.

${possibleRecovery.reason}

## Blocked Actions

${blockedActions.map((item) => `- ${item}`).join('\n')}
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-diethyl-source-lock-screen.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(new URL('peroxide-diethyl-source-lock-screen.md', outDir), markdown);

console.log(`Diethyl peroxide source lock: ${sourceLockDecision.status}`);
console.log(`Equilibrium C-O-O-C torsion: ${equilibriumExtraction.derivedCOOCDihedralDegrees} degrees`);
