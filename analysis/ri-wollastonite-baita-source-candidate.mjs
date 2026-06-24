import { mkdir, writeFile } from 'node:fs/promises';

// RI source-availability update: a candidate that may finally satisfy the
// long-deferred wollastonite polytype source lock (see
// ri-wollastonite-polytype-source-lock-screen.mjs, which deferred wollastonite for
// lack of a polytype-locked optical+density row).
//
// Marincea, Dumitras, Hatert, Sava Ghinet, Dinca, Iancu, Depret, "Crystal Structure
// vs. Vibrational Behavior of Wollastonite-1A from Baita Bihor, Bihor Mountains,
// Romania", Crystals 16(4), 247 (2026), DOI 10.3390/cryst16040247. Gold open access;
// cached via the Liege ORBI institutional repository.
//
// This is a SCREEN-LEVEL record only. It uses abstract/metadata facts (Crossref +
// the publisher abstract) and does NOT extract the paper's structural or optical
// tables for scoring. It scores nothing and reserves nothing; it records that the
// source appears to clear the optical/density/polytype/structure requirements and
// states the two conditions that must be settled before reserving and scoring.

const outDir = new URL('./out/', import.meta.url);

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const candidate = {
  citation:
    'S. Marincea, D. Dumitras, F. Hatert, A.-M. Sava Ghinet, D. Dinca, S. Iancu, A. Depret, Crystal Structure vs. Vibrational Behavior of Wollastonite-1A from Baita Bihor, Bihor Mountains, Romania, Crystals 16(4), 247 (2026)',
  doi: '10.3390/cryst16040247',
  openAccess: 'gold; OA copies at MDPI (Akamai-blocked to non-browser clients), DOAJ, and Liege ORBI',
  cached: 'analysis/source-cache/marincea-2026-wollastonite-1a-baita.pdf (via ORBI; source-cache is gitignored)',
  abstractVerifiedFacts: [
    'polytype explicitly identified as wollastonite-1A',
    'refraction indices alpha = 1.616, beta = 1.629, gamma = 1.631; 2V_alpha = 39 degrees',
    'measured density Dm = 2.922(3) g/cm3',
    'chemical structural formula (Ca1.000Mg0.002Mn0.001Fe0.001)(Al0.004Ti0.001Si0.994)O3 -- essentially CaSiO3 with trace substitution',
    'title and scope indicate a crystal-structure determination on the same material (same-sample optics + density + structure)',
  ],
};

// The six lock requirements from ri-wollastonite-polytype-source-lock-screen.mjs,
// reassessed against this candidate at abstract level only.
const requirementCheck = [
  {
    field: 'single polytype identity',
    requiredBefore: 'explicit Wo-1A/WO1T, Wollastonite-2M/parawollastonite, or other singular polytype',
    candidateState: 'satisfied at abstract level: explicitly wollastonite-1A',
    cleared: true,
  },
  {
    field: 'polytype-specific optical constants',
    requiredBefore: 'alpha, beta, gamma for the same polytype with source citation',
    candidateState: 'satisfied at abstract level: alpha/beta/gamma reported for this wollastonite-1A sample',
    cleared: true,
  },
  {
    field: 'polytype-specific measured density',
    requiredBefore: 'measured density for the same polytype/source row',
    candidateState: 'satisfied at abstract level: Dm = 2.922(3) measured for the same sample',
    cleared: true,
  },
  {
    field: 'paired CIF / structure',
    requiredBefore: 'coordinates for the same polytype',
    candidateState: 'likely satisfied same-sample (paper reports the crystal structure); to be confirmed at source lock without scoring',
    cleared: true,
  },
  {
    field: 'composition hygiene',
    requiredBefore: 'pure Ca-Si-O, excluding Mn/Fe-substituted rows',
    candidateState:
      'JUDGMENT REQUIRED: trace substitution Mg 0.002, Mn 0.001, Fe 0.001 (Ca site) and Al 0.004, Ti 0.001 (Si site); ~99.5 percent pure CaSiO3 but not strictly Mg/Mn/Fe-free',
    cleared: false,
  },
  {
    field: 'pre-score gate classification',
    requiredBefore: 'CIF-derived Ca coordination, mean Ca-O, connectivity under the fixed extractor before optical scoring',
    candidateState: 'deferred to the scoring step after reservation and parameter lock',
    cleared: false,
  },
];

const conditionsBeforeScoring = [
  {
    condition: 'composition-purity decision',
    detail:
      'decide whether ~0.2-0.5 percent natural trace substitution (Mg/Mn/Fe/Al/Ti) counts as pure-enough Ca-Si-O. The original exclusion rule targeted structural substitution (e.g. Mg-bearing merwinite); this is far below that. If trace substitution is NOT accepted, this target should be treated as Ca-dominant control rather than a pure held-out validation. This is a programme/discipline call, not made here.',
  },
  {
    condition: 'predictor parameter source lock',
    detail:
      'name and freeze the published refractivity/polarizability tables required by the structural predictor (predeclaration hash b764feb54971f5a9): coordination-resolved cation electronic polarizabilities (e.g. Shannon 1993 dielectric polarizabilities), the T-site occupant table, and bridging-O vs non-bridging-O oxygen refractivities. These must be locked independently of this target value (alpha/beta/gamma already seen at abstract level, so parameters must be the canonical published constants, not chosen to hit the answer).',
  },
];

const report = {
  source: 'ri-wollastonite-baita-source-candidate.mjs',
  date: '2026-06-24',
  status:
    'candidate source located that appears to clear the wollastonite polytype optical/density/structure lock; scoring gated on a composition-purity decision and the predictor parameter lock',
  validationClaim: false,
  evidenceStatus: 'none; screen-level record, no structural/optical extraction, no score, no reservation',
  servesPredictorForm: 'b764feb54971f5a9',
  candidate,
  requirementCheck,
  conditionsBeforeScoring,
  realisticOutlook:
    'This materially improves the RI track outlook: contrary to a pure data-wall reading, a recent (2026) open-access same-sample optical+density+structure source for an explicitly named pure-ish Ca-Si-O polytype does exist. RI is now the most likely of the three fronts to reach a genuine held-out score, pending the two conditions above.',
  nextStep:
    'if trace composition is accepted, lock the predictor parameter tables, then reserve this wollastonite-1A target (freeze identity before extracting its structural/optical tables for scoring), classify under the fixed extractor, and score n_struct vs the conventional control under predictor form b764feb54971f5a9',
};

const markdown = `# RI Wollastonite-1A Source Candidate (Baita Bihor, 2026)

## Scope

Screen-level update to the deferred wollastonite source lock. Uses abstract/metadata
facts only; extracts no structural or optical tables, scores nothing, reserves nothing.

Status: **${report.status}**

Serves predictor form: \`${report.servesPredictorForm}\`. Evidence status: ${report.evidenceStatus}.

## Candidate

- ${candidate.citation}
- DOI ${candidate.doi}; open access (${candidate.openAccess})
- cached: ${candidate.cached}

### Abstract-verified facts

${candidate.abstractVerifiedFacts.map((item) => `- ${item}`).join('\n')}

## Requirement Re-check (abstract level)

${table(
  ['Lock requirement', 'Required before', 'Candidate state', 'Cleared'],
  requirementCheck.map((row) => [row.field, row.requiredBefore, row.candidateState, row.cleared ? 'yes' : 'no']),
)}

## Conditions before scoring

${conditionsBeforeScoring.map((row) => `- **${row.condition}** — ${row.detail}`).join('\n')}

## Realistic outlook

${report.realisticOutlook}

## Next step

${report.nextStep}
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-wollastonite-baita-source-candidate.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('ri-wollastonite-baita-source-candidate.md', outDir), markdown);

console.log(`RI wollastonite-1A source candidate: ${report.status}`);
