import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const reservation = JSON.parse(
  await readFile(
    new URL('peroxide-methyl-chloroperoxide-reservation.json', outDir),
    'utf8',
  ),
);

const sources = [
  {
    role: 'primary torsional-potential study',
    citation:
      'E. Drougas and A. M. Kosmas, Quantum mechanical studies of isomeric and conformeric structures of methyl-chloro-peroxide, International Journal of Quantum Chemistry 98, 335-341 (2004)',
    doi: '10.1002/qua.20012',
    accessibleContent: 'title, abstract, and bibliographic metadata',
    lockedClaim:
      'the study explicitly investigates the torsional potential of CH3OOCl and identifies a skew peroxide minimum',
  },
  {
    role: 'secondary bibliographic confirmation',
    citation:
      'Theoretical Investigation of Halogen-Oxygen Bonding and Its Implications in Atmospheric Chemistry (2007)',
    url: 'https://pmc.ncbi.nlm.nih.gov/articles/PMC1939913/',
    accessibleContent: 'reference and contextual discussion',
    lockedClaim:
      'confirms the identity and citation but does not reproduce the required torsional profile',
  },
];

const requirements = reservation.frozenContract.sourceRequirements.map(
  (requirement) => ({
    requirement,
    status:
      requirement.startsWith('one source-defined ground-state')
        ? 'metadata-supported-but-not-numerically-locked'
        : 'not accessible',
  }),
);

const sourceLockDecision = {
  status: 'source-lock-failed-numerical-profile-inaccessible',
  scoringAllowed: false,
  predeclarationHash: reservation.predeclaration.hash,
  reason:
    'accessible primary metadata confirms that a CH3OOCl torsional potential was studied, but it does not expose the equilibrium angle, intermediate and nonlocal scan rows, relative energies, scan increment, relaxation rule, or signed torsion convention required by the frozen contract',
  evidenceAction: 'none; do not score or infer profile values',
  recovery:
    'obtain the full primary article or an author manuscript/supplement that exposes the numerical torsional scan; otherwise retire this identity from the active fresh-target queue',
};

const report = {
  source: 'peroxide-methyl-chloroperoxide-source-lock-screen.mjs',
  date: '2026-06-24',
  target: reservation.target,
  sources,
  requirements,
  sourceLockDecision,
  blockedActions: [
    'do not digitize a profile that is not available',
    'do not use abstract language such as skew minimum as a numerical coordinate',
    'do not borrow CH3OOCl values from reaction-PES or secondary papers',
    'do not score the v2 model on incomplete rows',
  ],
};

const markdown = `# Methyl Chloroperoxide Source-Lock Screen

Status: **${sourceLockDecision.status}**

The primary metadata confirms that CH3OOCl has a studied torsional potential,
but the numerical profile required by reservation
\`${sourceLockDecision.predeclarationHash}\` is not accessible.

| Requirement | Status |
|---|---|
${requirements
  .map((row) => `| ${row.requirement} | ${row.status} |`)
  .join('\n')}

Reason: ${sourceLockDecision.reason}.

Scoring allowed: **no**.

Recovery: ${sourceLockDecision.recovery}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-methyl-chloroperoxide-source-lock-screen.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('peroxide-methyl-chloroperoxide-source-lock-screen.md', outDir),
  markdown,
);

console.log(`Methyl chloroperoxide source lock: ${sourceLockDecision.status}`);
