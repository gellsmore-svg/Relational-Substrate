import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const reservation = JSON.parse(
  await readFile(
    new URL('peroxide-peroxyformic-target-reservation.json', outDir),
    'utf8',
  ),
);

const source = {
  primaryCitation:
    'Y. N. Indulkar, M. K. Louie, and A. Sinha, UV Photochemistry of Peroxyformic Acid (HC(O)OOH): An Experimental and Computational Study Investigating 355 nm Photolysis, J. Phys. Chem. A 118 (2014)',
  doi: '10.1021/jp5039688',
  accessibleAuthorVersion:
    'M. K. Louie, An Experimental and Theoretical Investigation of Atmospheric Reactions Involving Organic Acids, UC San Diego dissertation (2015), Chapter 2 reproducing the article',
  url: 'https://escholarship.org/uc/item/7mg20796',
  figure: 'Figure 2.8b',
};

const lockedConstruct = {
  molecule: 'peroxyformic acid',
  formula: 'HC(O)OOH',
  coordinate: 'C-O-O-H torsion chi',
  electronicState: 'ground electronic state X 1A-prime',
  method: 'ground-state ab initio torsional potential; all other coordinates fixed at equilibrium',
  energyReference: 'respective ground-state equilibrium geometry',
  sourceResolution:
    'values below are read from plotted markers; use ±0.01 eV digitization uncertainty',
  coordinates: [
    {
      role: 'equilibrium',
      torsionDegrees: 0,
      relativeEnergyEv: 0,
      uncertaintyEv: 0.01,
    },
    {
      role: 'intermediate',
      torsionDegrees: 30,
      relativeEnergyEv: 0.06,
      uncertaintyEv: 0.01,
    },
    {
      role: 'nonlocal',
      torsionDegrees: 90,
      relativeEnergyEv: 0.17,
      uncertaintyEv: 0.01,
    },
  ],
};

const intermediateDistance = 30;
const sourceLockDecision = {
  status: 'source-locked-three-coordinate-profile',
  predeclarationHash: reservation.predeclaration.hash,
  requirements: {
    equilibrium: true,
    intermediate:
      intermediateDistance >= 10 && intermediateDistance < 45,
    nonlocal: true,
    sameSurface: true,
    relativeEnergies: true,
  },
  scoringAllowed: true,
  evidenceEligibility:
    'held-out computed potential profile from a primary study, with experiment motivating the torsional construct; not an experimental barrier measurement',
  limitation:
    'relative energies are digitized from the published figure rather than tabulated; the expected ordering contrast is much larger than the stated digitization uncertainty',
};

const report = {
  source: 'peroxide-peroxyformic-source-lock-screen.mjs',
  date: '2026-06-24',
  target: reservation.target,
  sourceReference: source,
  lockedConstruct,
  sourceLockDecision,
  blockedActions: [
    'do not substitute an excited-state curve for the frozen ground-state profile',
    'do not move the intermediate coordinate after inspecting model output',
    'do not tune the energy or selection formulas',
    'propagate the plotted-value limitation into the scoring report',
  ],
};

const markdown = `# Peroxyformic-Acid Source Lock

Status: **${sourceLockDecision.status}**

Source: ${source.primaryCitation}. DOI: ${source.doi}.

Accessible author version: ${source.accessibleAuthorVersion}.

The frozen source rows all come from ${source.figure}, the ground-state
C-O-O-H torsional potential.

| Role | Torsion | Relative energy | Uncertainty |
|---|---:|---:|---:|
${lockedConstruct.coordinates
  .map(
    (row) =>
      `| ${row.role} | ${row.torsionDegrees} degrees | ${row.relativeEnergyEv} eV | ±${row.uncertaintyEv} eV |`,
  )
  .join('\n')}

Scoring allowed: **${sourceLockDecision.scoringAllowed ? 'yes' : 'no'}**.

Evidence eligibility: ${sourceLockDecision.evidenceEligibility}.

Limitation: ${sourceLockDecision.limitation}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-peroxyformic-source-lock-screen.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('peroxide-peroxyformic-source-lock-screen.md', outDir),
  markdown,
);

console.log(`Peroxyformic source lock: ${sourceLockDecision.status}`);
