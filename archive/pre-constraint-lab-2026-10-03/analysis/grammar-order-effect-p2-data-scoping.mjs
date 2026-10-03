import { mkdir, writeFile } from 'node:fs/promises';

// P2 scoping: is there ACCESSIBLE fatigue coaxing data to test the grammar's
// whole-history order-effect prediction (gentle-first survives more cycles-to-first-
// failure than harsh-first at matched severity)? See
// docs/grammar-native-prediction-scoping-2026-06-24.md and the P1 derivation
// (analysis/grammar-order-effect-derivation.mjs).
//
// This scopes data + designs the test. It scores nothing and asserts no evidence.

const outDir = new URL('./out/', import.meta.url);

const dataSource = {
  title: 'Cyclic Deformation and Fatigue Data for Ti-6Al-4V ELI under Variable Amplitude Loading',
  venue: 'Data in Brief (data paper); PMC5458061 (open access)',
  repository: 'Harvard Dataverse, doi:10.7910/DVN/SUCU5X',
  license: 'CC0 1.0 (public domain) -- fully reusable',
  files: 'H-L.zip (high-low, id 3008844), L-H.zip (low-high, id 3008843, downloaded), plus PO/VA constant + variable-amplitude data',
  confirmedAccessible: true,
  structure: [
    'two-level block loading with BOTH sequences: low-high (L-H = gentle-first) and high-low (H-L = harsh-first)',
    'per-specimen folders named by the amplitude PAIR, e.g. L-H_0.006-0.008, L-H_0.006-0.010, at R=0 and R=-1',
    'the SAME amplitude pairs appear in both L-H and H-L archives -> matched pairs that isolate ORDER as the variable',
    'per the data paper Table 1: 15 H-L rows (11 at R=-1, 4 at R=0) and 10 L-H rows (6 at R=-1, 4 at R=0); 25 two-block tests',
    'cycles-to-failure available from Table 1 (n1 first block, n2 second-block-to-failure) and countable from the peak-valley xlsx per specimen',
  ],
};

const testDesign = {
  prediction:
    'whole-history endpoint (cycles-to-first-failure): at a matched amplitude pair and matched first-block fraction, LOW-HIGH (gentle-first) outlasts HIGH-LOW (harsh-first). This is the model-derived direction (P1), and the order-independent baseline (Miner / linear damage) predicts the null (no order effect).',
  protocol: [
    'for each amplitude pair x R condition present in both archives, take total cycles to failure N = n1 + n2 for L-H and for H-L',
    'where constant-amplitude Nf(eps_a) is available (PO/VA data or paper), also compute the Miner sum D = n1/Nf1 + n2/Nf2 per test; the classic signature is D(L-H) > 1 > D(H-L)',
    'pre-register the directional hypothesis L-H life > H-L life BEFORE extracting the numbers; report sign-consistency across matched pairs and the paired effect size',
  ],
  endpoint: 'cycles-to-first-failure (whole-history), NOT residual strength -- the P1 derivation showed a residual/final-state endpoint is recency-dominated and would show the OPPOSITE sign',
  registeredDescriptorsNeeded: 'none new for the directional test (it is a sign test on measured lives); a magnitude test would need a grammar->cycles calibration',
};

const honestFraming = {
  whatAPassShows:
    'directional CORROBORATION of the grammar-native prediction against the order-INDEPENDENT baseline (Miner / linear damage), which predicts no order effect. This is the first real-data corroboration of a distinctive RS-grammar claim.',
  whatAPassDoesNotShow:
    'it does NOT distinguish the grammar from established NONLINEAR cumulative-damage models (Corten-Dolan, damage-curve, double-linear Miner, etc.), which ALSO predict the sequence effect. The "no-established-competitor" claim holds only against the simplest standard baseline (Miner), not against the nonlinear-damage literature.',
  toBeDecisive:
    'the grammar would need a MAGNITUDE or cross-pair PATTERN prediction competitive with the nonlinear-damage models -- which requires calibrating the grammar abstract identity units to fatigue life, reintroducing the derived-vs-calibrated tension flagged in the scoping memo.',
  knownEffectCaveat:
    'the L-H>H-L sequence effect is well documented in fatigue (the "coaxing effect"); the grammar gets the SIGN right, which is reassuring but expected for any reasonable memory model. Value is in (a) it being a pre-registered grammar-native prediction confirmed on real data and (b) setting up the harder magnitude test.',
};

const verdict = 'accessible fatigue coaxing data CONFIRMED (CC0, matched L-H/H-L pairs); the directional test is feasible and pre-registerable; a pass would corroborate the grammar vs the Miner null but not vs nonlinear-damage models';

const report = {
  source: 'grammar-order-effect-p2-data-scoping.mjs',
  date: '2026-06-24',
  status: verdict,
  validationClaim: false,
  evidenceStatus: 'none; data scoping + test design only, nothing scored',
  dataSource,
  testDesign,
  honestFraming,
  secondarySources:
    'the loading-sequence-effect literature is large (many two-stage block-loading datasets); Ti-6Al-4V ELI (CC0) is the cleanest open primary. A second open dataset would strengthen cross-material robustness if the directional test is run.',
  recommendation: [
    'run the DIRECTIONAL test first: extract cycles-to-failure for matched L-H/H-L amplitude pairs from the cached/CC0 data and check L-H life > H-L life, pre-registering the hypothesis. Modest but genuine: the first real-data corroboration of a grammar-native prediction.',
    'only if it passes, decide whether to attempt the MAGNITUDE prediction (calibrate grammar->life, compare to nonlinear-damage models) -- the harder, potentially-decisive but calibration-tainted step.',
    'keep confidence capped regardless: a directional corroboration vs the Miner null is not decisive grammar evidence.',
  ],
  nextExecution: 'cache H-L.zip (id 3008844) alongside the downloaded L-H.zip, parse cycles-to-failure per specimen, pair by amplitude+R, run the sign test',
};

const markdown = `# P2 Data Scoping: fatigue coaxing data for the grammar order-effect test

Status: **${report.status}**

Scopes data + designs the test; scores nothing.

## Data source (confirmed accessible)

- ${dataSource.title}
- ${dataSource.venue}; ${dataSource.repository}; license ${dataSource.license}
- files: ${dataSource.files}

Structure:
${dataSource.structure.map((s) => `- ${s}`).join('\n')}

## Test design

- prediction: ${testDesign.prediction}
- endpoint: ${testDesign.endpoint}
- protocol:
${testDesign.protocol.map((p) => `  - ${p}`).join('\n')}

## Honest framing

- a pass shows: ${honestFraming.whatAPassShows}
- a pass does NOT show: ${honestFraming.whatAPassDoesNotShow}
- to be decisive: ${honestFraming.toBeDecisive}
- known-effect caveat: ${honestFraming.knownEffectCaveat}

## Recommendation

${report.recommendation.map((r) => `- ${r}`).join('\n')}

Next execution: ${report.nextExecution}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('grammar-order-effect-p2-data-scoping.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('grammar-order-effect-p2-data-scoping.md', outDir), markdown);

console.log(`P2 fatigue coaxing data scoping: ${report.status}`);
