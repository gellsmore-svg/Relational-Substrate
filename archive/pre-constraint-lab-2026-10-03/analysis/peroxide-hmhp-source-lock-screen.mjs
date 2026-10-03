import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const reservation = JSON.parse(
  await readFile(
    new URL('peroxide-v2-fresh-target-reservation.json', outDir),
    'utf8',
  ),
);

const sources = [
  {
    role: 'primary spectroscopy and structure source',
    citation:
      'J. L. Fry et al., OH-Stretch Vibrational Spectroscopy of Hydroxymethyl Hydroperoxide, J. Phys. Chem. A 110, 7072-7079 (2006)',
    doi: '10.1021/jp0612127',
    repository: 'CaltechAUTHORS record 9ht0w-2tp16',
    localSupportingInformation:
      'analysis/source-cache/fry-2006-hmhp-supporting-information.pdf',
  },
  {
    role: 'author dissertation reproduction of article chapter',
    citation:
      'J. L. Fry, Spectroscopy and Kinetics of Atmospheric Reservoir Species, Caltech PhD thesis (2006), Chapter 8',
    url: 'https://thesis.caltech.edu/1547/',
    localText: 'analysis/source-cache/fry-2006-thesis.txt',
  },
];

const extractedConformers = [
  {
    label: 'HMHP-A',
    relativeEnergyCm1: 301,
    zpeCorrectedRelativeEnergyCm1: 215,
    dihedralsDegrees: {
      D6: 123.33384465,
      D7: -68.85675108,
      D8: -113.21992691,
    },
    hydrogenBondTopology: 'RO-H donor',
  },
  {
    label: 'HMHP-B',
    relativeEnergyCm1: 0,
    zpeCorrectedRelativeEnergyCm1: 0,
    dihedralsDegrees: {
      D6: 120.89328016,
      D7: -69.8005525,
      D8: 74.8494432,
    },
    hydrogenBondTopology: 'OO-H donor',
  },
  {
    label: 'HMHP-C',
    relativeEnergyCm1: 76,
    zpeCorrectedRelativeEnergyCm1: 13,
    dihedralsDegrees: {
      D6: 123.38100855,
      D7: -70.41308955,
      D8: -246.0408624,
    },
    hydrogenBondTopology: 'RO-H donor',
  },
];

const requirements = reservation.frozenContract.sourceRequirements.map(
  (requirement) => ({
    requirement,
    pass:
      requirement.startsWith('one source-defined potential-energy equilibrium')
        ? true
        : false,
  }),
);

const sourceLockDecision = {
  status: 'source-lock-failed-coupled-conformer-profile',
  scoringAllowed: false,
  predeclarationHash: reservation.predeclaration.hash,
  reason:
    'the source reports optimized conformers whose O-O-H and C-O-O-H-related dihedrals and intramolecular hydrogen-bond donor topology change together; these are not three points on one isolated torsional coordinate under a fixed companion-coordinate rule',
  evidenceAction: 'none; do not score HMHP under the v2 contract',
  recovery:
    'a separate primary source with a one-dimensional relaxed or fixed-coordinate HMHP O-O torsional scan could unlock the target, but the conformer table cannot be converted into that scan',
};

const report = {
  source: 'peroxide-hmhp-source-lock-screen.mjs',
  date: '2026-06-24',
  target: reservation.reservedTarget,
  sources,
  extractedConformers,
  requirements,
  sourceLockDecision,
  blockedActions: [
    'do not select three conformers as equilibrium/intermediate/nonlocal rows',
    'do not infer a one-dimensional barrier from conformer relative energies',
    'do not choose one changing dihedral while ignoring the changing hydrogen-bond topology',
    'do not score or tune the equilibrium-relative crowding model on HMHP',
  ],
};

const markdown = `# HMHP Source-Lock Screen

Status: **${sourceLockDecision.status}**

The source provides three optimized HMHP conformers, but not the frozen
one-dimensional three-coordinate torsional profile.

| Conformer | Relative energy | ZPE-corrected energy | D6 | D7 | D8 | H-bond donor |
|---|---:|---:|---:|---:|---:|---|
${extractedConformers
  .map(
    (row) =>
      `| ${row.label} | ${row.relativeEnergyCm1} cm-1 | ${row.zpeCorrectedRelativeEnergyCm1} cm-1 | ${row.dihedralsDegrees.D6} | ${row.dihedralsDegrees.D7} | ${row.dihedralsDegrees.D8} | ${row.hydrogenBondTopology} |`,
  )
  .join('\n')}

Reason: ${sourceLockDecision.reason}.

Scoring allowed: **no**.

Recovery: ${sourceLockDecision.recovery}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-hmhp-source-lock-screen.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('peroxide-hmhp-source-lock-screen.md', outDir),
  markdown,
);

console.log(`HMHP source lock: ${sourceLockDecision.status}`);
