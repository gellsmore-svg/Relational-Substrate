import { mkdir, writeFile } from 'node:fs/promises';

// Cross-domain scoping for the grammar's order-effect prediction. After the fatigue
// corroboration (materials), the question is whether the SAME pre-registered
// directional law holds in a SECOND, unconnected domain -- which is the unification
// thesis's only no-established-competitor space (no theory links metal fatigue and
// cardiac ischemia, yet the grammar predicts the same directional order effect in both).
//
// Pre-registration: the prediction is the same P1-derived directional law already
// committed in grammar-order-effect-derivation.mjs and grammar-order-effect-p2-data-
// scoping.mjs -- gentle/mild-first protects whole-history survival (and harsh-first
// sensitises) at matched total severity, beating the order-INDEPENDENT null. It is
// domain-agnostic and is NOT fit to biological data.
//
// Consistency only; confidence unchanged.

const outDir = new URL('./out/', import.meta.url);

const preRegisteredPrediction = {
  law: 'gentle/mild-first protects whole-history survival; harsh-first sensitises; the same encounters in a different ORDER give different survival (order is non-commutative)',
  source: 'P1 derivation (grammar-order-effect-derivation.mjs); committed before any biological data was consulted',
  crossDomainClaim: 'the SAME directional law holds across domains with no connecting established theory (materials fatigue <-> biological preconditioning) -- this is the unification thesis, and the only no-established-competitor space the grammar has',
  biologicalMapping: [
    'gentle-first / coaxing (fatigue) <-> preconditioning (mild stress before a severe insult)',
    'residual harsh life > virgin (fatigue) <-> preconditioned damage < unconditioned damage (the severe insult is less damaging after mild pre-exposure)',
    'harsh-first sensitises (fatigue) <-> postconditioning is weaker / sensitisation; ORDER matters: pre > post for the same intervention',
  ],
};

// Accessible data located (open-access; quantitative; correct order structure).
const dataFound = [
  {
    source: 'Wever et al., Determinants of the Efficacy of Cardiac Ischemic Preconditioning: A Systematic Review and Meta-Analysis of Animal Studies, PLOS One 10(10):e0142021 (2015)',
    access: 'open access (PLOS One); PMC4651366',
    structure: '503 animal studies, 785 preconditioned-vs-control comparisons of myocardial infarct size',
    directionalResult: 'mild-first preconditioning reduces infarct size by 24.6% [95% CI 23.5, 25.6] -- robust, large-n confirmation that gentle-first protects',
    note: 'meta-analytic effect; the cleanest aggregate directional test',
  },
  {
    source: 'Ischemic conditioning strategies comparisons (e.g. Scientific Reports 2025, s41598-025-17442-y; open access)',
    access: 'open access',
    structure: 'pre- vs post- vs remote-conditioning infarct-size comparisons (same intervention, different timing/order)',
    directionalResult: 'preconditioning (mild-first) is the MOST effective; postconditioning the least -- ORDER-dependence in the predicted direction (gentle-first best)',
    note: 'the direct biological analog of fatigue L-H vs H-L (same intervention, different order)',
  },
  {
    source: 'Primary study examples (e.g. Frontiers Cardiovasc Med 2024, fcvm.2024.1376367; PMC10978780; open access)',
    access: 'open access',
    structure: 'per-animal infarct-size tables, preconditioned vs control (e.g. 1.8 +/- 1.1% vs 12.8 +/- 3.3%, p<0.005)',
    directionalResult: 'preconditioned damage far below control -- single-study confirmation with extractable tables',
    note: 'usable for a quantitative execution step if wanted',
  },
];

const honestFraming = {
  whatItShows:
    'the grammar\'s pre-registered directional law is corroborated in a SECOND, unconnected domain (cardiac ischemia) with robust open-access quantitative data, AND the order-specificity (pre > post) matches. Two domains with no connecting theory show the same directional order effect -- the cross-domain REACH that is the lens\'s distinctive value.',
  whatItDoesNotShow:
    'this is NOT decisive evidence for a literal shared substrate. Preconditioning / adaptation is a famous, well-established phenomenon studied independently in each field; a skeptic can say "any memory/adaptive system shows preconditioning, so its appearance in both domains is unsurprising." The grammar gets the DIRECTION right (as in fatigue), which is reassuring but expected of any memory model. As established earlier, magnitude is a lens, not a quantitative prediction.',
  status:
    'directional cross-domain corroboration for the LENS standing (the grammar organises and directionally predicts across domains with no connecting theory); consistency-only; confidence UNCHANGED.',
};

const report = {
  source: 'grammar-order-effect-crossdomain-scoping.mjs',
  date: '2026-06-25',
  status: 'cross-domain preconditioning data CONFIRMED accessible; the directional law is corroborated in a second, unconnected domain (cardiac ischemia) -- directional reach for the lens, not decisive evidence',
  consistencyCheckOnly: true,
  validationClaim: false,
  raisesConfidence: false,
  preRegisteredPrediction,
  dataFound,
  honestFraming,
  recommendation: [
    'scoping outcome: accessible, open-access, quantitative biological preconditioning data exists with the correct order structure, and at the meta-analytic level it already corroborates the directional prediction (24.6% infarct reduction; pre > post order-dependence).',
    'optional execution step: extract per-comparison effect sizes from one open dataset/meta-analysis and the pre-vs-post order comparison, and record them alongside the fatigue result as a two-domain directional ledger. This sharpens the cross-domain claim but does not change its status (directional, not decisive).',
    'do NOT chase magnitude across domains (calibration trap, already settled) and do NOT claim a literal shared mechanism -- the defensible claim is cross-domain directional reach under one grammar.',
    'this is the natural endpoint of the order-effect arc: the grammar now has its distinctive prediction corroborated in TWO unconnected domains, which is the strongest honest support the unification-as-lens framing can have. Confidence stays capped.',
  ],
};

const markdown = `# Cross-Domain Order-Effect Scoping: biological preconditioning

Status: **${report.status}**

Consistency check only; confidence unchanged. Pre-registration: ${preRegisteredPrediction.source}.

## Pre-registered prediction (domain-agnostic)

- ${preRegisteredPrediction.law}
- cross-domain claim: ${preRegisteredPrediction.crossDomainClaim}
- biological mapping:
${preRegisteredPrediction.biologicalMapping.map((m) => `  - ${m}`).join('\n')}

## Accessible data found

${dataFound.map((d) => `- **${d.source}** (${d.access})\n  - structure: ${d.structure}\n  - directional result: ${d.directionalResult}`).join('\n')}

## Honest framing

- what it shows: ${honestFraming.whatItShows}
- what it does NOT show: ${honestFraming.whatItDoesNotShow}
- status: ${honestFraming.status}

## Recommendation

${report.recommendation.map((r) => `- ${r}`).join('\n')}
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('grammar-order-effect-crossdomain-scoping.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('grammar-order-effect-crossdomain-scoping.md', outDir), markdown);

console.log(`Cross-domain preconditioning scoping: ${report.status}`);
