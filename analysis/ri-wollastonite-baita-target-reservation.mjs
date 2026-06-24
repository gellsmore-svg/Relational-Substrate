import { mkdir, writeFile } from 'node:fs/promises';
import { formatPredeclaration, predeclare, requireScoringGate } from './predeclaration-gate.mjs';

// Target reservation for the first held-out RI consistency score under predictor
// v1 (predeclaration hash 9f8838307cc1a70d) with parameters locked from
// Shannon-Fischer 2016. Freezes the target identity and the exact scoring recipe
// -- including the conventional control's numeric definition -- BEFORE the paper's
// structural tables (cell volume, Ca coordination) are extracted.
//
// Transparency: the measured optical indices (alpha/beta/gamma) and density were
// seen at abstract level during screening. This does not compromise the test
// because predictor v1 is a FIXED-PARAMETER model whose equations and polarizability
// values were locked (from SF2016) independently of this target -- nothing in the
// predictor can be tuned to the measured n. The composition decision (accept the
// ~0.2-0.5% trace substitution as pure-enough CaSiO3) has been made by the operator.

const outDir = new URL('./out/', import.meta.url);

const target =
  'wollastonite-1A, Marincea et al., Crystals 16(4), 247 (2026), DOI 10.3390/cryst16040247; treat as pure CaSiO3 (trace Mg/Mn/Fe/Al/Ti accepted as pure-enough); same-sample measured alpha/beta/gamma + measured density + reported crystal structure';
const modelForm = 'structurally-resolved Anderson-Eggleton RI predictor v1 (Shannon-Fischer 2016 parameters)';
const descriptors = [
  'ca_coordination',
  'mean_ca_o_distance',
  't_site_polarizability',
  'silicate_connectivity',
  'density',
  'lorentz_lorenz',
];

const pre = predeclare({ target, modelForm, descriptors, heldOut: true });
requireScoringGate(pre, { target });

// Frozen Ca polarizability table (SF2016, coordination-resolved), repeated here so
// the reservation is self-contained for both the structural and control recipes.
const CA_ALPHA_BY_CN = { 5: 1.91, 6: 1.79, 7: 1.67, 8: 1.57, 9: 1.48, 10: 1.39, 11: 1.32, 12: 1.25 };
const caAgnostic =
  Object.values(CA_ALPHA_BY_CN).reduce((s, v) => s + v, 0) / Object.values(CA_ALPHA_BY_CN).length;

const frozenRecipe = {
  servesPredictor: '9f8838307cc1a70d',
  parameterSource: 'Shannon-Fischer 2016 (cached); alpha(Si4+,[4])=0.284; O2- eqn(6) alpha0=1.79, No=-1.776, nexp=1.20; Ca by CN per CA_ALPHA_BY_CN; AE relation c=2.26, b=4pi/3',
  molarVolume: 'Vm (per formula unit) and Van (per O) taken from the paper cell volume and Z: Vm = Vcell/Z, Van = Vcell/(3*Z); cross-check Vm against measured density 2.922(3) and M(CaSiO3)=116.16 g/mol',
  structuralPrediction:
    'alpha_T(struct) = alpha(Ca, by the CIF mean Ca coordination number) + 0.284 (Si) + 3 * alpha(O2-) with alpha(O2-) from eqn (6) using Van; n_struct via AE (4b) with Vm',
  conventionalControl: {
    definition:
      'structure-blind: alpha_T(conv) = alpha_Ca_agnostic + 0.284 (Si) + 3 * 1.79 (free-ion O2-, NO volume correction); n_conv via AE (4b) with the same Vm',
    caAgnosticValue: Number(caAgnostic.toFixed(4)),
    note: 'alpha_Ca_agnostic is the unweighted mean of the SF2016 Ca CN table, frozen here BEFORE extraction so the control cannot be tuned',
  },
  measuredComparator:
    'scalar mean index n_meas = (alpha + beta + gamma)/3 from the same-sample optical data',
  passFail: [
    '|n_struct - n_meas| <= 0.010',
    '|n_struct - n_meas| <= |n_conv - n_meas| (structural at least matches the structure-blind control)',
  ],
  extractAfterReservation: [
    'cell volume Vcell and Z from the paper crystallographic table',
    'mean Ca coordination number (the paper reports the Ca polyhedra)',
    'confirm Si is [4] tetrahedral and the silicate connectivity class (chain/pyroxenoid)',
    'confirm measured alpha/beta/gamma and density from the paper body',
  ],
};

const report = {
  source: 'ri-wollastonite-baita-target-reservation.mjs',
  date: '2026-06-24',
  status: 'wollastonite-1A reserved for the first held-out RI consistency score; structural tables not yet extracted',
  validationClaim: false,
  evidenceStatus: 'none; reservation only',
  consistencyCheckOnly: true,
  predeclaration: pre,
  frozenRecipe,
  blockedActions: [
    'do not change any locked polarizability value or equation after seeing the extracted structure',
    'do not redefine the conventional control after computing n_struct',
    'do not report a pass as independent evidence for the topology grammar or raise any confidence score',
  ],
  nextStep:
    'extract the frozen structural quantities from the cached Marincea 2026 PDF, then compute n_struct and n_conv and apply the pass/fail in a single scoring artifact',
};

const markdown = `# RI Wollastonite-1A Target Reservation (consistency score)

Status: **${report.status}**

This reserves the target and freezes the scoring recipe before structural extraction.
It is a consistency check only.

${formatPredeclaration(pre)}

## Frozen recipe

- serves predictor: \`${frozenRecipe.servesPredictor}\`
- parameters: ${frozenRecipe.parameterSource}
- molar volume: ${frozenRecipe.molarVolume}
- structural prediction: ${frozenRecipe.structuralPrediction}
- conventional control: ${frozenRecipe.conventionalControl.definition} (alpha_Ca_agnostic = ${frozenRecipe.conventionalControl.caAgnosticValue}, ${frozenRecipe.conventionalControl.note})
- measured comparator: ${frozenRecipe.measuredComparator}

## Pass/fail

${frozenRecipe.passFail.map((p) => `- ${p}`).join('\n')}

## To extract after reservation

${frozenRecipe.extractAfterReservation.map((e) => `- ${e}`).join('\n')}

Next step: ${report.nextStep}
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-wollastonite-baita-target-reservation.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('ri-wollastonite-baita-target-reservation.md', outDir), markdown);

console.log(`RI wollastonite-1A target reservation: ${pre.hash}`);
