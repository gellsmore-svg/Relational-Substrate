import { mkdir, writeFile } from 'node:fs/promises';

// P2 EXECUTION: test the grammar's pre-registered order-effect prediction against
// real fatigue data (Ti-6Al-4V ELI, CC0; Kamal/Rahman/Shamsaei et al., Data in Brief;
// PMC5458061 Table 1; Harvard Dataverse doi:10.7910/DVN/SUCU5X).
//
// Pre-registration: the directional hypothesis (gentle-first protects whole-history
// survival) was committed in analysis/grammar-order-effect-p2-data-scoping.mjs and
// derived from the model in analysis/grammar-order-effect-derivation.mjs BEFORE these
// numbers were extracted.
//
// Clean data-internal test (no external S-N needed): in low-high (L-H, gentle-first)
// two-block tests ending at eps_a=0.010, does the residual high-amplitude block life
// n2 EXCEED the virgin constant-amplitude life Nf(0.010)? The linear-damage (Miner)
// null forbids this (residual = Nf*(1 - D1) <= Nf for any prior damage D1>=0). The
// grammar predicts gentle pre-loading extends the harsh-block life (n2 > Nf_virgin) =
// the coaxing effect. Asserts no physical theory beyond this comparison; consistency
// stays capped.

const outDir = new URL('./out/', import.meta.url);

// --- Nf(0.010, Reps=-1) derived from the dataset's own D-labeled H-L tests ---
// Each D-label is the first-block damage fraction D1 = n1/Nf1, so Nf1 = n1/D1.
const nfDerivation = [
  { specimen: 'H-L_0.010-0.005(1)D0.25', n1: 512, D1: 0.25 },
  { specimen: 'H-L_0.010-0.005(3)D0.25', n1: 512, D1: 0.25 },
  { specimen: 'H-L_0.010-0.005(1)D0.50', n1: 1024, D1: 0.5 },
  { specimen: 'H-L_0.010-0.005(2)D0.50', n1: 1024, D1: 0.5 },
  { specimen: 'H-L_0.010-0.005(1)D0.75', n1: 1536, D1: 0.75 },
  { specimen: 'H-L_0.010-0.005(2)D0.75', n1: 1536, D1: 0.75 },
].map((r) => ({ ...r, impliedNf: r.n1 / r.D1 }));
const nfValues = nfDerivation.map((r) => r.impliedNf);
const Nf_010 = nfValues.reduce((s, v) => s + v, 0) / nfValues.length; // 2048, all identical
const nfConsistent = new Set(nfValues).size === 1;

// --- L-H (gentle-first) tests ending at eps_a2 = 0.010, Reps=-1 (Table 1) ---
const lhEndingAt010 = [
  { specimen: 'L-H_0.006-0.010(1)', epsA1: 0.006, n1: 38384, n2_at010: 2823 },
  { specimen: 'L-H_0.006-0.010(2)', epsA1: 0.006, n1: 38384, n2_at010: 2161 },
  { specimen: 'L-H_0.005-0.010(1)', epsA1: 0.005, n1: 500000, n2_at010: 3209 },
  { specimen: 'L-H_0.005-0.010(2)', epsA1: 0.005, n1: 500000, n2_at010: 2316 },
].map((r) => ({
  ...r,
  residualVsVirginRatio: Number((r.n2_at010 / Nf_010).toFixed(3)),
  exceedsVirgin: r.n2_at010 > Nf_010, // linear-null violation in the coaxing direction
}));

const nExceeding = lhEndingAt010.filter((r) => r.exceedsVirgin).length;
const meanRatio = lhEndingAt010.reduce((s, r) => s + r.residualVsVirginRatio, 0) / lhEndingAt010.length;
const allExceed = nExceeding === lhEndingAt010.length;

// Directional result: the linear-damage null predicts residual <= Nf_virgin; the
// grammar (coaxing / gentle-first protects) predicts residual > Nf_virgin.
const predictionConfirmed = allExceed;

const report = {
  source: 'grammar-order-effect-fatigue-test.mjs',
  date: '2026-06-25',
  status: predictionConfirmed
    ? 'grammar order-effect prediction CONFIRMED on real fatigue data vs the linear-damage null'
    : 'grammar order-effect prediction NOT confirmed',
  consistencyCheckOnly: true,
  validationClaim: false,
  raisesConfidence: false,
  dataSource: 'Ti-6Al-4V ELI, PMC5458061 Table 1, Harvard Dataverse doi:10.7910/DVN/SUCU5X (CC0)',
  preRegistration: 'direction committed in grammar-order-effect-p2-data-scoping.mjs and grammar-order-effect-derivation.mjs before extraction',
  virginLife: {
    epsA: 0.010, condition: 'Reps=-1',
    Nf: Nf_010,
    derivedFrom: 'D-labeled H-L tests (D1 = n1/Nf1); all six imply the same Nf',
    consistent: nfConsistent,
    derivation: nfDerivation,
  },
  test: {
    question: 'do gentle-first (L-H) residual high-amplitude lives exceed the virgin life Nf(0.010)=2048?',
    linearNull: 'residual <= Nf_virgin (Miner: residual = Nf*(1-D1) <= Nf for D1>=0)',
    grammarPrediction: 'residual > Nf_virgin (gentle pre-loading extends the harsh-block life = coaxing)',
    rows: lhEndingAt010,
    countExceedingVirgin: `${nExceeding}/${lhEndingAt010.length}`,
    meanResidualVsVirginRatio: Number(meanRatio.toFixed(3)),
  },
  predictionConfirmed,
  interpretation: [
    `RESULT: ${nExceeding}/${lhEndingAt010.length} gentle-first tests have a residual high-amplitude life EXCEEDING the virgin Nf(0.010)=2048 (mean ratio ${meanRatio.toFixed(3)}, i.e. +${Math.round((meanRatio - 1) * 100)}%). This VIOLATES the linear-damage (Miner) null in the coaxing direction and matches the grammar's pre-registered prediction (gentle-first protects).`,
    'This is the first real-data corroboration of a distinctive RS-grammar prediction: it beats the order-INDEPENDENT linear-damage baseline (which is the clean no-established-competitor claim from the scoping memo).',
    'HONEST LIMITS: (1) the coaxing effect is well documented in fatigue, so getting the SIGN right is reassuring but expected for any memory model; (2) it does NOT beat established NONLINEAR cumulative-damage models, which also predict coaxing; (3) only the gentle-first (L-H) side is cleanly testable here -- the harsh-first (H-L) residual-reduction side needs Nf(0.006), which is not in this dataset (web lookup was rate-limited); (4) n=4, one material, one amplitude endpoint; (5) Nf(0.010)=2048 is derived from the D-labels under the standard D1=n1/Nf1 reading (self-consistent across six tests).',
    'CONFIDENCE: unchanged. A directional corroboration vs the Miner null is not decisive grammar evidence; per the scoping memo, decisiveness would need a MAGNITUDE prediction competitive with nonlinear-damage models (requires grammar->life calibration). The cap stays.',
  ],
  nextStep: 'to strengthen: obtain Nf(eps_a) for 0.005/0.006/0.008 (constant-amplitude S-N for this material) to test the harsh-first residual-reduction side and compute full Miner sums for all matched pairs; then, only if still clean, attempt the magnitude test vs a nonlinear-damage model.',
};

const markdown = `# Grammar Order-Effect: Fatigue Coaxing Test (P2 execution)

Status: **${report.status}**

Consistency check only; confidence unchanged. Data: ${report.dataSource}.
Pre-registration: ${report.preRegistration}.

## Virgin life (data-internal)

Nf(eps_a=0.010, Reps=-1) = **${Nf_010}** cycles, derived from the D-labeled H-L tests
(D1 = n1/Nf1); all six imply the same value (consistent: ${nfConsistent}).

| D-labeled specimen | n1 | D1 | implied Nf |
|---|---|---|---|
${nfDerivation.map((r) => `| ${r.specimen} | ${r.n1} | ${r.D1} | ${r.impliedNf} |`).join('\n')}

## Test: gentle-first residual high-amplitude life vs virgin

Linear-damage null: residual <= ${Nf_010}. Grammar (coaxing): residual > ${Nf_010}.

| L-H specimen | first block | residual n2 @0.010 | n2 / Nf_virgin | exceeds virgin? |
|---|---|---|---|---|
${lhEndingAt010.map((r) => `| ${r.specimen} | ${r.n1} @ ${r.epsA1} | ${r.n2_at010} | ${r.residualVsVirginRatio} | ${r.exceedsVirgin ? 'YES' : 'no'} |`).join('\n')}

Count exceeding virgin: **${nExceeding}/${lhEndingAt010.length}**; mean ratio **${meanRatio.toFixed(3)}**.

Prediction confirmed: **${predictionConfirmed ? 'YES' : 'no'}**.

## Interpretation

${report.interpretation.map((i) => `- ${i}`).join('\n')}

## Next step

${report.nextStep}
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('grammar-order-effect-fatigue-test.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('grammar-order-effect-fatigue-test.md', outDir), markdown);

console.log(`Grammar order-effect fatigue test: ${report.status}`);
console.log(`  Nf(0.010)=${Nf_010} (consistent ${nfConsistent}); L-H residual > virgin in ${nExceeding}/${lhEndingAt010.length}; mean ratio ${meanRatio.toFixed(3)}`);
