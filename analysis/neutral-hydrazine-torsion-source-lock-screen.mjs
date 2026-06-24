import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const reservation = JSON.parse(
  await readFile(
    new URL('neutral-hydrazine-torsion-target-reservation.json', outDir),
    'utf8',
  ),
);

const sources = [
  {
    role: 'experimental aggregate barrier',
    citation: 'NIST CCCBDB experimental data for neutral hydrazine',
    url: 'https://cccbdb.nist.gov/exp2x.asp?casno=302012&charge=0',
    availableData:
      'one barrier to internal rotation, 35.8 kJ mol-1; no paired angle-resolved second barrier row on the accessible neutral-species page',
    constructStatus: 'insufficient for the frozen two-barrier contract',
  },
  {
    role: 'primary computed torsion-wagging surface',
    citation:
      'W. Łodyga and J. Makarewicz, Torsion-wagging tunneling and vibrational states in hydrazine determined from its ab initio potential energy surface, J. Chem. Phys. 136, 174301 (2012)',
    doi: '10.1063/1.4705267',
    availableData:
      'accessible abstract reports two computed torsion barriers, labelled cis and trans, of 744 and 2706 cm-1',
    constructStatus:
      'computed 3D torsion-wagging PES; full numerical angle convention and stationary-point mapping are not accessible in the current source',
  },
  {
    role: 'equilibrium-angle context',
    citation:
      'neutral hydrazine conformational literature and secondary reviews',
    availableData: 'gauche equilibrium reported near 91.5 degrees',
    constructStatus:
      'not sufficient to join the NIST aggregate barrier and 2012 computed barriers into one source-locked profile',
  },
];

const requirements = reservation.frozenModel.sourceRequirements.map(
  (requirement) => {
    let status = 'not satisfied';
    if (requirement.startsWith('neutral hydrazine identity')) {
      status = 'satisfied';
    } else if (requirement.startsWith('source-defined equilibrium')) {
      status = 'secondary-context only; not locked to the barrier source';
    } else if (requirement.startsWith('at least two barrier')) {
      status =
        'two computed labels available, but full angle/construct mapping inaccessible';
    } else if (requirement.startsWith('all barrier angles')) {
      status = 'not locked';
    }
    return { requirement, status };
  },
);

const sourceLockDecision = {
  status: 'source-lock-failed-mixed-and-ambiguous-barrier-constructs',
  scoringAllowed: false,
  predeclarationHash: reservation.predeclaration.hash,
  reason:
    'the experimental source exposes only one aggregate neutral-hydrazine barrier, while the source with two computed barriers does not expose enough of its torsion-angle convention and stationary-point mapping in the accessible record to assign the values to the frozen model rows without an analyst choice',
  evidenceAction: 'none; do not score neutral hydrazine',
  recovery:
    'obtain the full 2012 primary article or a source table that explicitly maps equilibrium, cis, and trans torsion angles to energies under one construct',
};

const report = {
  source: 'neutral-hydrazine-torsion-source-lock-screen.mjs',
  date: '2026-06-24',
  target: reservation.predeclaration.target,
  sources,
  requirements,
  sourceLockDecision,
  blockedActions: [
    'do not combine the NIST aggregate experimental barrier with computed barrier rows',
    'do not infer cis/trans angle mapping from chemical intuition or model preference',
    'do not choose 744 or 2706 cm-1 as the 0 or 180 degree row without primary mapping',
    'do not score or modify the hydrazine-family model',
  ],
};

const markdown = `# Neutral Hydrazine Torsion Source Lock

Status: **${sourceLockDecision.status}**

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
  new URL('neutral-hydrazine-torsion-source-lock-screen.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('neutral-hydrazine-torsion-source-lock-screen.md', outDir),
  markdown,
);

console.log(`Neutral hydrazine source lock: ${sourceLockDecision.status}`);
