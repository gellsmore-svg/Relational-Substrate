import { mkdir, writeFile } from 'node:fs/promises';
import { formatPredeclaration, predeclare, requireScoringGate } from './predeclaration-gate.mjs';

// RI structural predictor v1 -- reconciled to the locked parameter source
// (Shannon & Fischer 2016; see ri-predictor-parameter-source-lock.mjs). This
// SUPERSEDES v0 (hash b764feb54971f5a9), which predeclared Lorentz-Lorenz + a
// bridging/non-bridging oxygen split that the authoritative source does not use.
//
// v1 adopts the source's own machinery: the Anderson-Eggleton relation (c=2.26),
// the polarizability additivity rule, the anion-volume O2- correction, and the
// coordination-resolved cation polarizabilities. Equations are transcribed
// verbatim from the cached preprint (pages 5-8) and re-verified by round-trip.
//
// IMPORTANT FRAMING (carried from the parameter-lock finding): SF2016 is already a
// validated structural RI predictor, so v1 is explicitly a CONSISTENCY CHECK --
// does resolving Ca coordination and anion volume FROM THE CIF reproduce the
// measured index, and does that structural resolution beat a coordination-agnostic
// control? A pass shows the RS structural descriptors are compatible with
// established polarizability theory; it is NOT independent evidence for the
// topology grammar and must not by itself raise unification confidence.
//
// Scores nothing, fits nothing.

const outDir = new URL('./out/', import.meta.url);

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const modelForm = 'structurally-resolved Anderson-Eggleton RI predictor v1 (Shannon-Fischer 2016 parameters; fixed, no fitted coefficients)';
const target =
  'reserved pure-ish Ca-Si-O target (wollastonite-1A, Marincea et al. Crystals 2026) pending the trace-composition decision; predictor parameters are locked from Shannon-Fischer 2016 independently of the target';
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

// Equations transcribed verbatim from Shannon-Fischer 2016 (cached preprint, pp.5-8).
const equations = {
  general_1b: 'alpha = (n^2 - 1) * Vm / ( 4*pi + (4*pi/3 - c) * (n^2 - 1) )',
  anderson_eggleton_4a: 'alpha_AE = (n^2 - 1) * Vm / ( 4*pi + (4*pi/3 - 2.26) * (n^2 - 1) )  [c = 2.26]',
  predict_n_4b: 'n = sqrt( 4*pi*alpha / ( (c - b)*alpha + Vm ) + 1 ),  with c = 2.26, b = 4*pi/3',
  additivity_5: 'alpha_T = sum_i m_i * alpha_e(ion_i)   [m_i = count of ion i in the formula unit]',
  anion_volume_6: 'alpha_minus = alpha_minus_free * 10^( -No / Van^nexp ),  with O2- params alpha_minus_free = 1.79, No = -1.776, nexp = 1.20; Van = anion molar volume',
  notes: [
    'Vm and Van are molar volumes in Angstrom^3 (per formula unit / per anion); alpha in Angstrom^3',
    'forward (4a) and inverse (4b) verified to round-trip in ri-structural-predictor-v1-model.mjs',
    'eqn (6) parameter interpretation (free-ion alpha vs reported 1.79) must be ANCHORED against a SF2016 worked example (e.g. its SiO2 / MgO oxygen value) before scoring; flagged in the model module',
  ],
};

// Locked, source-derived inputs (from ri-predictor-parameter-source-lock.mjs).
const lockedInputs = {
  relationConstant: 'c = 2.26 (Anderson-Eggleton), b = 4*pi/3',
  caCoordinationResolved: 'alpha(Ca2+) by CN: [5]1.910 [6]1.790 [7]1.670 [8]1.570 [9]1.480 [10]1.390 [11]1.320 [12]1.250 (Angstrom^3)',
  silicon: 'alpha(Si4+,[4]) = 0.284',
  oxygen: 'anion-volume model, eqn (6), O2- params alpha_minus_free=1.79, No=-1.776, nexp=1.20',
  traceIons: 'alpha([4]Al)=0.40, [5]Al=0.43, [6]Al=0.47; Mg/Mn/Fe/Ti available in the same table if the composition decision includes them',
};

// The structural-vs-conventional contrast (the heart of the consistency check).
const contrast = {
  structural:
    'alpha_T from coordination-resolved cation polarizabilities (Ca selected by its CIF coordination number; Si [4]) plus N_O * alpha(O2-) via the eqn (6) anion-volume correction using Van from the CIF, then n via AE (4b) with Vm from the CIF/measured density',
  conventional:
    'alpha_T from coordination-AGNOSTIC cation polarizabilities (a single fixed alpha per element, not resolved by CIF coordination) plus N_O * fixed free-ion alpha(O2-) with NO volume correction, then n via AE (4b) with the same Vm',
  whatItTests:
    'whether resolving Ca coordination and oxygen anion-volume from the structure improves the predicted index over a structure-blind baseline at fixed composition and molar volume',
};

const passFail = [
  'absolute: |n_struct - n_measured(mean of alpha,beta,gamma)| <= 0.010',
  'value-added: |n_struct - n_measured| <= |n_conv - n_measured| (structural at least matches the coordination-agnostic control; a strict improvement is reported but the gate only requires non-worse, because SF2016 shows the structural resolution is usually a small correction for low-RI silicates)',
  'both evaluated on the reserved held-out target with equations and locked parameters unchanged from this predeclaration',
];

const consistencyCheckFraming = [
  'this is a CONSISTENCY CHECK, not independent evidence for the topology grammar',
  'SF2016 already predicts nD across ~2600 compounds with this machinery; v1 reuses it',
  'a pass demonstrates the RS structural descriptors (Ca coordination, connectivity-as-anion-environment) are compatible with established polarizability theory on a fresh held-out mineral',
  'a pass must NOT by itself raise inferential-convergence, cross-domain, or unification-thesis confidence',
  'a FAILURE would be informative: it would mean the RS structural reading is inconsistent even with established crystal chemistry on this target',
];

const nextGate = [
  { step: 'eqn-6 anchor', passCondition: 'O2- anion-volume parameters reproduce a SF2016 worked oxygen value (e.g. its SiO2 value) within rounding' },
  { step: 'composition decision', passCondition: 'trace substitution in wollastonite-1A accepted as pure-enough, or target treated as Ca-dominant control' },
  { step: 'target reservation', passCondition: 'wollastonite-1A identity frozen and its CIF/optical/density tables extracted only after reservation' },
  { step: 'held-out score', passCondition: 'n_struct meets the absolute and value-added gates with no change to equations or locked parameters' },
];

const report = {
  source: 'ri-structural-predictor-v1-predeclaration.mjs',
  date: '2026-06-24',
  status: 'RI structural predictor v1 predeclared (reconciled to Shannon-Fischer 2016 / Anderson-Eggleton); explicit consistency check; supersedes v0; scoring still gated',
  validationClaim: false,
  evidenceStatus: 'none; predictor form frozen, nothing scored or fitted',
  supersedes: 'b764feb54971f5a9 (v0: Lorentz-Lorenz + bridging/non-bridging O split, inconsistent with the locked source)',
  predeclaration: pre,
  equations,
  lockedInputs,
  contrast,
  passFail,
  consistencyCheckFraming,
  nextGate,
};

const markdown = `# RI Structural Predictor v1 Predeclaration (consistency check)

## Scope

Reconciles the RI structural predictor to the locked parameter source (Shannon-Fischer
2016), superseding v0. Adopts the source's Anderson-Eggleton machinery verbatim.
Scores nothing. Framed explicitly as a consistency check, not novel evidence.

Date: ${report.date}. Supersedes: ${report.supersedes}.

${formatPredeclaration(pre)}

## Equations (transcribed from Shannon-Fischer 2016, pp.5-8)

- general (1b): ${equations.general_1b}
- Anderson-Eggleton (4a): ${equations.anderson_eggleton_4a}
- predict n (4b): ${equations.predict_n_4b}
- additivity (5): ${equations.additivity_5}
- anion-volume O2- (6): ${equations.anion_volume_6}

${equations.notes.map((n) => `- note: ${n}`).join('\n')}

## Locked inputs

${Object.entries(lockedInputs).map(([k, v]) => `- ${k}: ${v}`).join('\n')}

## Structural vs conventional contrast

- structural: ${contrast.structural}
- conventional control: ${contrast.conventional}
- what it tests: ${contrast.whatItTests}

## Pass/fail

${passFail.map((p) => `- ${p}`).join('\n')}

## Consistency-check framing (carried from the parameter-lock finding)

${consistencyCheckFraming.map((c) => `- ${c}`).join('\n')}

## Next gate

${table(['Step', 'Pass condition'], nextGate.map((r) => [r.step, r.passCondition]))}

Status: ${report.status}
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-structural-predictor-v1-predeclaration.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('ri-structural-predictor-v1-predeclaration.md', outDir), markdown);

console.log(`RI structural predictor v1 predeclaration: ${pre.hash}`);
