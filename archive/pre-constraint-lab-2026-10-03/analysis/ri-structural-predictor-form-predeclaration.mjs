import { mkdir, writeFile } from 'node:fs/promises';
import { formatPredeclaration, predeclare, requireScoringGate } from './predeclaration-gate.mjs';

// RI structural PREDICTOR form predeclaration (the next step after the descriptor
// model-form freeze in ri-structural-model-form-predeclaration.mjs, hash recorded
// there). This freezes the predictor EQUATION and the calibration/scoring protocol
// using only the already-frozen descriptor set, BEFORE any held-out target exists.
//
// It scores nothing, fits nothing, and asserts no evidence. It is the one RI step
// that is genuinely unblocked by the held-out-data wall: predeclaration must
// precede the target anyway, so it can be done now.
//
// Design choice: a FIXED-PARAMETER structurally-resolved Lorentz-Lorenz predictor.
// There are NO fitted coefficients -- every parameter comes from a named published
// refractivity/polarizability table and is locked before the target is consulted.
// This removes the target-implied-coefficient failure mode that sank the earlier
// Al-boost and Ca/Mg-scaffold repairs, and makes the test sharp: does structurally
// resolved refractivity beat plain composition-only Lorentz-Lorenz on a fresh
// held-out mineral?

const outDir = new URL('./out/', import.meta.url);

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const modelForm = 'structurally-resolved Lorentz-Lorenz RI predictor v0 (fixed published parameters, no fitted coefficients)';
const target =
  'future source-locked pure Ca-Si-O material/polytype; optical constants, measured density, and paired CIF must be reserved before scoring, and the predictor parameter tables locked before the target is consulted';
const descriptors = [
  'ca_coordination',
  'mean_ca_o_distance',
  't_site_polarizability',
  'silicate_connectivity',
  'density',
  'lorentz_lorenz',
];

const pre = predeclare({ target, modelForm, descriptors, heldOut: true });
// Prove the predictor form clears the hard gate while leaving scoring blocked.
requireScoringGate(pre, { target });

const equation = {
  conversion:
    'predict the scalar mean refractive index n by solving the Lorentz-Lorenz relation (n^2-1)/(n^2+2) = (rho/M) * R_molar for n, using the source-locked measured density rho and the formula mass M from the locked CIF stoichiometry',
  conventionalControl:
    'R_conv = sum over formula ions of (stoichiometry_i * R_i_published), with fixed published free-ion electronic refractivities for Ca2+, Si4+, O2- and NO structural resolution; this is the conventional comparator prediction n_conv',
  structuralModel:
    'R_struct = R_Ca(structurally selected) + R_Tsite(structurally selected) + R_O(structurally split), each term read from a named published table and selected -- not fitted -- by the frozen structural descriptors',
  termSelection: [
    'R_Ca: coordination-resolved Ca-O contribution selected by ca_coordination and mean_ca_o_distance from a published coordination-resolved cation electronic-polarizability table',
    'R_Tsite: T-site occupant contribution selected by t_site_polarizability from the versioned radii/polarizability table already named for that descriptor',
    'R_O: the N_O oxygens are split into bridging vs non-bridging by silicate_connectivity class (orthosilicate / sorosilicate / chain / ring / framework), each fraction taking a fixed published bridging-O or non-bridging-O electronic refractivity',
  ],
  noFreeParameters:
    'there are no regression coefficients and no scalar uplift terms; every numeric input is a published, source-locked constant',
};

const passFail = [
  'absolute: |n_struct - n_measured| <= 0.010 on the scalar mean index of the source-locked held-out target',
  'value-added: |n_struct - n_measured| <= 0.70 * |n_conv - n_measured| (structural prediction must beat the conventional Lorentz-Lorenz control by at least 30 percent)',
  'both conditions must hold on a fresh held-out target with extraction code, equation, and all published parameters unchanged from this predeclaration',
];

const calibrationProtocol = [
  'no calibration fit is performed; the model has fixed published parameters only',
  'the published Ca-O / T-site / bridging-O / non-bridging-O parameter tables must be NAMED and source-locked before the held-out target optical and density values are consulted',
  'already-exposed pure Ca-Si-O minerals (larnite COD 9017424, rankinite, kilchoanite) may be used only as exposed reference sanity checks of the equation, never as the held-out validation target',
  'merwinite and spurrite are excluded even as reference checks for substrate claims (Mg / carbonate confounds)',
  'the held-out target must not influence parameter-table selection in any way',
];

const sourceLockRequirements = [
  'held-out target: optical constants (alpha/beta/gamma preferred), measured density, and paired CIF all locked to ONE material/polytype identity',
  'parameter tables: a named publication for coordination-resolved cation electronic polarizabilities/refractivities, a named publication or the versioned table for T-site occupants, and named published bridging-O vs non-bridging-O oxygen refractivities',
  'stoichiometry and formula mass M taken from the locked CIF, not from a mineral-page summary',
  'pre-score CIF gate classification (ca_coordination, mean_ca_o_distance, silicate_connectivity) computed by the fixed extractor before n is predicted',
];

const blockedShortcuts = [
  {
    shortcut: 'fitting any coefficient to the exposed minerals',
    reason: 'reintroduces the target-implied-coefficient failure mode; the predictor must stay fixed-parameter',
  },
  {
    shortcut: 'reporting a conventional Lorentz-Lorenz pass as substrate evidence',
    reason: 'the conventional control is the baseline to beat, never itself the substrate result',
  },
  {
    shortcut: 'using broad pooled or secondary mineral-page optical/density rows',
    reason: 'a held-out target needs a primary, polytype-locked optical+density row, per the wollastonite source-lock screen',
  },
  {
    shortcut: 'counting an exposed reference-check pass as held-out validation',
    reason: 'value may be claimed only on a fresh held-out target, not on calibration/exposed rows',
  },
];

const nextGate = [
  { step: 'parameter source lock', passCondition: 'all published refractivity/polarizability tables named and frozen' },
  { step: 'target source lock', passCondition: 'one pure Ca-Si-O polytype with optical + measured density + paired CIF' },
  { step: 'pre-score classification', passCondition: 'structural descriptors extracted from the CIF before n is computed' },
  { step: 'held-out score', passCondition: 'n_struct meets both absolute and value-added gates without any change to equation or parameters' },
];

const report = {
  source: 'ri-structural-predictor-form-predeclaration.mjs',
  date: '2026-06-24',
  status:
    'RI structural predictor equation and protocol predeclared (fixed-parameter, no fitted coefficients); scoring remains blocked until parameter tables and a held-out target are source-locked',
  validationClaim: false,
  evidenceStatus: 'none; predictor form frozen, nothing scored or fitted',
  predeclaration: pre,
  equation,
  passFail,
  calibrationProtocol,
  sourceLockRequirements,
  blockedShortcuts,
  nextGate,
};

const markdown = `# RI Structural Predictor-Form Predeclaration

## Scope

This freezes the predictor EQUATION and the scoring/calibration protocol for the
next source-locked material-RI attempt, building on the frozen descriptor set in
\`ri-structural-model-form-predeclaration.mjs\`. It scores no target, fits no
coefficient, and asserts no evidence. It is the RI step that the held-out-data wall
does not block, because predeclaration must precede the target regardless.

Date: ${report.date}

${formatPredeclaration(pre)}

## Predictor Equation (frozen)

- conversion: ${equation.conversion}
- conventional control: ${equation.conventionalControl}
- structural model: ${equation.structuralModel}
- no free parameters: ${equation.noFreeParameters}

### Structural term selection

${equation.termSelection.map((item) => `- ${item}`).join('\n')}

## Pass/Fail (frozen)

${passFail.map((item) => `- ${item}`).join('\n')}

## Calibration / held-out protocol

${calibrationProtocol.map((item) => `- ${item}`).join('\n')}

## Source-lock requirements before scoring

${sourceLockRequirements.map((item) => `- ${item}`).join('\n')}

## Blocked shortcuts

${table(['Shortcut', 'Reason blocked'], blockedShortcuts.map((row) => [row.shortcut, row.reason]))}

## Next scoring gate

${table(['Step', 'Pass condition'], nextGate.map((row) => [row.step, row.passCondition]))}

## Reading

The earlier RI repairs failed because coefficients were, in effect, implied by the
targets they were meant to predict. This predictor form removes that degree of
freedom entirely: it is a fixed-parameter, structurally-resolved Lorentz-Lorenz
prediction whose only question is whether resolving oxygen bridging/non-bridging and
Ca-O coordination from the structure beats a composition-only Lorentz-Lorenz control
on a fresh held-out mineral. If a clean target is ever source-locked, this is a
genuine, hard-to-game test of the topology grammar against a conventional baseline.
Until then it is readiness only, and changes no confidence.

Status: ${report.status}
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-structural-predictor-form-predeclaration.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('ri-structural-predictor-form-predeclaration.md', outDir), markdown);

console.log(`RI structural predictor form predeclaration: ${pre.hash}`);
