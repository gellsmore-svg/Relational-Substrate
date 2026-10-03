import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const reservation = JSON.parse(
  await readFile(
    new URL('peroxide-dual-channel-target-reservation.json', outDir),
    'utf8',
  ),
);

const target = {
  molecule: 'dimethyl peroxide',
  formula: 'CH3OOCH3',
  sourceLabel: 'MeOOMe',
  reservedBy: 'peroxide-dual-channel-target-reservation.mjs',
  predeclarationHash: reservation.predeclaration.hash,
};

const sourceCandidates = [
  {
    role: 'modern equilibrium-structure interpretation',
    citation:
      'O. Ferchichi, N. Derbel, N.-E. Jaidane, T. Cours, and A. Alijah, Phys. Chem. Chem. Phys. 19, 21500-21506 (2017)',
    doi: '10.1039/C7CP03134C',
    url: 'https://pubs.rsc.org/en/content/articlelanding/2017/cp/c7cp03134c',
    sourceType: 'high-level CCSD(T)-F12/MRCI structure and torsional-dynamics study',
    lockedUse:
      'distinguish the trans potential-energy minimum from the vibrationally averaged dynamical structure',
    extractionStatus:
      'article metadata and abstract source-locked; full numerical table not locally extracted',
  },
  {
    role: 'experimental gas electron diffraction source',
    citation: 'B. Haas and H. Oberhammer, J. Am. Chem. Soc. 106, 6146-6149 (1984)',
    doi: '10.1021/ja00333a004',
    url: 'https://pubs.acs.org/doi/10.1021/ja00333a004',
    sourceType: 'gas electron diffraction with large-amplitude O-O torsion model',
    lockedUse:
      'experimental vibrationally averaged/dynamical geometry and trans-barrier provenance',
    extractionStatus:
      'primary citation and abstract-level geometry available; values cross-checked by the NIST critical review',
  },
  {
    role: 'critical evaluated source',
    citation:
      'O. Dorofeeva, V. P. Novikov, and D. B. Neumann, J. Phys. Chem. Ref. Data 30, 475-513 (2001)',
    doi: '10.1063/1.1416900',
    url: 'https://www.nist.gov/system/files/documents/srd/JPCRD302001475p.pdf',
    sourceType: 'NIST critical evaluation of structure, spectroscopy, and internal rotation',
    lockedUse:
      'evaluated dynamical geometry and adopted trans/cis torsional potential values',
    extractionStatus: 'full PDF cached and text extracted locally',
  },
  {
    role: 'computed torsional profile',
    citation:
      'A. C. P. Bitencourt, M. Ragni, G. S. Maciel, V. Aquilanti, and F. V. Prudente, J. Chem. Phys. 129, 154316 (2008)',
    doi: '10.1063/1.2992554',
    url: 'https://repositorio.ufba.br/bitstream/ri/6014/1/C__Documents%20and%20Settings_rep...t.default_Cache_9_32_A9163d01.pdf',
    sourceType: 'B3LYP/6-311++G(3df,3pd) geometry and O-O torsional potential table',
    lockedUse: 'computed PES geometry, barriers, and Fourier coefficients',
    extractionStatus:
      'full PDF was already cached for ethyl hydroperoxide before the dimethyl target reservation',
  },
];

const constructDistinction = {
  potentialEnergyEquilibrium:
    'modern high-level work identifies a trans C-O-O-C minimum at 180 degrees; Bitencourt Table I likewise reports 180 degrees and zero trans barrier',
  dynamicalStructure:
    'the electron-diffraction analysis reports a skew, vibrationally averaged/dynamical angle near 119 degrees with a shallow adopted trans barrier',
  scoringRule:
    'do not compare a PES minimum prediction directly with the vibrationally averaged 119-degree structure as though both were equilibrium coordinates',
};

const sourceLockDecision = {
  sourceStatus: 'source-locked; paired geometry and torsional comparators available',
  scoringStatus: 'blocked-by-underspecified-target-mapping',
  reason:
    'The frozen selection descriptor evaluates a full family score, which requires terminal-group geometry, steric clearance, and polarity/charge inputs. The target reservation froze only the C-O-O-C torsion mapping and did not freeze a dimethyl-peroxide charge rule or methyl-group coordinate construction before source lookup.',
  evidenceEligibility:
    'not pristine fresh evidence because the Bitencourt PDF containing the MeOOMe row was locally cached before target reservation; extraction can be diagnostic only',
};

const extractedPreview = {
  nistEvaluatedDynamicModel: {
    equilibriumAngleDegrees: 119,
    transBarrierCm1: 87,
    cisBarrierCm1: 4700,
    provenance:
      'trans angle/barrier from electron diffraction; cis barrier adopted from theoretical calculations',
  },
  bitencourtComputedPes: {
    equilibriumAngleDegrees: 180,
    transBarrierCm1: 0,
    cisBarrierCm1: 3904.37,
    method: 'B3LYP/6-311++G(3df,3pd)',
  },
};

const blockedActions = [
  'do not invent partial charges after lookup',
  'do not replace terminal hydrogens with methyl pseudo-atoms without a predeclared coordinate and steric rule',
  'do not treat the 119-degree dynamical structure as the modern PES equilibrium geometry',
  'do not count the pre-existing cached MeOOMe source as pristine held-out evidence',
  'do not tune energy release parameters from either dimethyl-peroxide source interpretation',
];

const nextGate = [
  'record this target as a diagnostic source-lock success but scoring-contract failure',
  'redesign the selection descriptor to consume only predeclared source-observable torsion quantities, or predeclare full terminal-group geometry and charge rules',
  'reserve another fresh target only after the revised descriptor is frozen',
];

const report = {
  source: 'peroxide-dimethyl-source-lock-screen.mjs',
  date: '2026-06-23',
  target,
  sourceCandidates,
  constructDistinction,
  sourceLockDecision,
  extractedPreview,
  blockedActions,
  nextGate,
};

const markdown = `# Dimethyl Peroxide Source-Lock Screen

## Decision

- Source status: **${sourceLockDecision.sourceStatus}**
- Scoring status: **${sourceLockDecision.scoringStatus}**
- Evidence eligibility: ${sourceLockDecision.evidenceEligibility}

Source scarcity is not the blocker. The frozen target mapping is incomplete:
the full family-score selection channel needs geometry, steric, and polarity
inputs that were not frozen before lookup.

## Construct Distinction

| Construct | Source reading |
|---|---|
| potential-energy equilibrium | ${constructDistinction.potentialEnergyEquilibrium} |
| dynamical structure | ${constructDistinction.dynamicalStructure} |
| scoring rule | ${constructDistinction.scoringRule} |

## Source-Locked Preview

| Source interpretation | Angle | Trans barrier | Cis barrier |
|---|---:|---:|---:|
| NIST evaluated dynamical model | ${extractedPreview.nistEvaluatedDynamicModel.equilibriumAngleDegrees} degrees | ${extractedPreview.nistEvaluatedDynamicModel.transBarrierCm1} cm-1 | ${extractedPreview.nistEvaluatedDynamicModel.cisBarrierCm1} cm-1 |
| Bitencourt computed PES | ${extractedPreview.bitencourtComputedPes.equilibriumAngleDegrees} degrees | ${extractedPreview.bitencourtComputedPes.transBarrierCm1} cm-1 | ${extractedPreview.bitencourtComputedPes.cisBarrierCm1} cm-1 |

## Why Scoring Is Blocked

${sourceLockDecision.reason}

## Blocked Actions

${blockedActions.map((item) => `- ${item}`).join('\n')}

## Next Gate

${nextGate.map((item) => `- ${item}`).join('\n')}
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-dimethyl-source-lock-screen.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(new URL('peroxide-dimethyl-source-lock-screen.md', outDir), markdown);

console.log(`Dimethyl peroxide source status: ${sourceLockDecision.sourceStatus}`);
console.log(`Dimethyl peroxide scoring status: ${sourceLockDecision.scoringStatus}`);
