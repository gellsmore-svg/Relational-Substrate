import { mkdir, writeFile } from 'node:fs/promises';

// Design + predeclaration for a SHARPER, SF2016-INDEPENDENT RI test (pursuing the
// "option 1" raised after the wollastonite-1A consistency pass). It scores nothing
// and looks up no target data. It (a) maps the observable space SF2016 cannot reach,
// (b) evaluates candidate RS-specific tests there, (c) predeclares the single viable
// falsifiable RS hypothesis, and (d) gives an honest independence assessment -- being
// clear about what a pass would and would not prove.
//
// Motivation: the wollastonite-1A score passed, but predictor v1 IS Shannon-Fischer
// 2016 (a scalar total-polarizability model), so it was a consistency check, not
// independent evidence for the topology grammar. A sharper test must predict
// something SF2016 structurally cannot.

const outDir = new URL('./out/', import.meta.url);

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

// What SF2016 structurally cannot predict (it is a SCALAR mean-index model).
const sf2016IndependentObservables = [
  {
    observable: 'optical anisotropy: birefringence magnitude (delta = gamma - alpha), optic sign, and indicatrix orientation',
    whySf2016Cannot: 'SF2016 collapses the polarizability tensor to one scalar alpha_T and predicts only the mean index; it carries no directional information',
  },
  {
    observable: 'additivity-rule deviation Delta = (alpha_obs - alpha_calc)/alpha_calc',
    whySf2016Cannot: 'SF2016 additivity predicts Delta = 0 by construction; the systematic residuals it flags (steric strain, edge-sharing, fast-ion paths) are exactly what its base rule does not capture',
  },
];

// Candidate RS-specific tests, each assessed for independence from established models.
const candidateTests = [
  {
    id: 'connectivity-anisotropy',
    hypothesis:
      'the optical anisotropy follows the silicate-connectivity topology: the high-index direction aligns with the dominant connectivity route, and birefringence magnitude ranks by connectivity dimensionality',
    sf2016Independent: true,
    rsNative: 'high -- "route/continuity along the connected covalent path" is the topology grammar applied to a directional observable',
    competingEstablishedModel: 'bond-polarizability tensor model (sum oriented bond polarizabilities)',
    independenceFromCompeting:
      'PARTIAL: RS predicts orientation/rank from connectivity topology ALONE (no bond-polarizability values), which is coarser and mechanistically distinct, but its predictions OVERLAP the bond-tensor model, so a pass is consistent with both and is not a clean discriminator',
    dataAccessibility: 'good: birefringence, optic sign, and indicatrix orientation are standard reported mineral properties; connectivity class is from the CIF',
    verdict: 'most viable sharper test; predeclared below',
  },
  {
    id: 'additivity-deviation',
    hypothesis: 'RS connectivity/topology predicts the sign and magnitude of the SF2016 additivity deviation Delta',
    sf2016Independent: true,
    rsNative: 'medium -- targets SF2016 residuals, which SF2016 itself attributes to structure',
    competingEstablishedModel: 'the SF2016 deviation-papers series (steric strain, polyhedral connectivity)',
    independenceFromCompeting:
      'WEAK: the SF2016 school already attributes Delta to structural motifs; RS would have to predict Delta from topology MORE cleanly or via a distinct feature to count as independent',
    dataAccessibility: 'poor: needs the SF2016 supplementary Delta table (~1200 minerals), which is paywalled; back at the data-access wall',
    verdict: 'secondary; data-blocked and contested',
  },
  {
    id: 'scalar-beyond-sf2016',
    hypothesis: 'RS scalar-index prediction beats SF2016 on the mean index for some structure class',
    sf2016Independent: false,
    rsNative: 'n/a',
    competingEstablishedModel: 'SF2016 itself',
    independenceFromCompeting: 'NONE: same observable SF2016 already predicts to ~1-2%; beating it marginally is not grammar evidence',
    dataAccessibility: 'n/a',
    verdict: 'rejected: not SF2016-independent',
  },
];

// The predeclared falsifiable RS hypothesis (connectivity-anisotropy). This is a
// TEST DESIGN: it freezes the hypothesis and falsification criteria BEFORE any
// held-out anisotropy dataset is reserved. It does NOT yet score; it also flags that
// RS has no implemented anisotropy descriptors, so scoring requires new registered
// descriptors (connectivity_dimensionality, indicatrix_orientation) first.
const predeclaredHypothesis = {
  name: 'RS topological-anisotropy rule v0 (DESIGN; not yet scored)',
  orientationClaim:
    'H1: for 1D chain silicates (inosilicates) the high-index axis (gamma) lies within 30 degrees of the chain-extension axis; for 2D sheet silicates (phyllosilicates) the low-index axis (alpha) lies within 30 degrees of the sheet normal',
  magnitudeClaim:
    'H2: birefringence delta ranks by connectivity anisotropy: delta(sheet, 2D) > delta(chain, 1D) > delta(framework, 3D) and delta(isolated/orthosilicate) is low; ranks compared on a held-out set, not absolute values',
  falsification: [
    'H1 falsified if, on a fresh held-out set of >=8 minerals across >=3 connectivity classes, the high/low-index axis misaligns with the predicted connectivity direction beyond 30 degrees in more than 20 percent of cases',
    'H2 falsified if the predicted connectivity-dimensionality ordering of median delta is violated on the held-out set',
  ],
  heldOutProtocol:
    'reserve minerals (identity + connectivity class from CIF) BEFORE looking up their measured birefringence/optic orientation; classify connectivity from structure only; no per-mineral tuning',
  newDescriptorsRequired: ['connectivity_dimensionality (0D/1D/2D/3D)', 'indicatrix_orientation_vs_connectivity'],
  notScored: true,
};

const honestConclusion = [
  'Within the scalar refractive index, RS is captured by SF2016 (the wollastonite-1A pass demonstrated this): RI is effectively a CLOSED domain for novel RS evidence at the scalar level.',
  'The only SF2016-independent opening that is RS-grammar-native and data-accessible is optical ANISOTROPY (connectivity -> indicatrix orientation + birefringence rank). It is predeclared above.',
  'But even this is not a clean discriminator: it competes with the established bond-polarizability tensor model, whose predictions overlap. A pass would show topology SUFFICES to predict the anisotropy pattern (a parsimony point weakly favoring the grammar), not that the grammar is uniquely correct.',
  'Pursuing it also REQUIRES extending RS into anisotropy (new descriptors + a directional model RS does not currently have); it is a genuinely new research direction, not a quick score.',
  'Net: a sharper RI test exists and is now designed/predeclared, but RI cannot give DECISIVE independent grammar evidence. This confirms and extends the information-limitation assessment: the programme should weigh whether to build RS anisotropy (uncertain payoff) or seek a different domain where the grammar makes a prediction with no established competitor.',
];

const report = {
  source: 'ri-anisotropy-topology-test-design.mjs',
  date: '2026-06-24',
  status: 'sharper SF2016-independent RI test designed and predeclared (connectivity-anisotropy); not scored; RI judged largely closed for decisive novel RS evidence',
  validationClaim: false,
  evidenceStatus: 'none; design + falsifiable predeclaration only',
  sf2016IndependentObservables,
  candidateTests,
  predeclaredHypothesis,
  honestConclusion,
};

const markdown = `# Sharper, SF2016-Independent RI Test: Design + Predeclaration

Status: **${report.status}**

Scores nothing; looks up no target data. Pursues "option 1" after the wollastonite-1A
consistency pass: find an RI test predicting something SF2016 structurally cannot.

## What SF2016 cannot predict (it is a scalar model)

${table(['Observable', 'Why SF2016 cannot reach it'], sf2016IndependentObservables.map((o) => [o.observable, o.whySf2016Cannot]))}

## Candidate RS-specific tests

${table(
  ['Test', 'SF2016-independent', 'RS-native', 'vs established model', 'data', 'verdict'],
  candidateTests.map((t) => [t.id, t.sf2016Independent ? 'yes' : 'no', t.rsNative, t.independenceFromCompeting.split(':')[0], t.dataAccessibility.split(':')[0], t.verdict]),
)}

## Predeclared falsifiable hypothesis: ${predeclaredHypothesis.name}

- ${predeclaredHypothesis.orientationClaim}
- ${predeclaredHypothesis.magnitudeClaim}

Falsification:
${predeclaredHypothesis.falsification.map((f) => `- ${f}`).join('\n')}

Held-out protocol: ${predeclaredHypothesis.heldOutProtocol}.
New descriptors required before scoring: ${predeclaredHypothesis.newDescriptorsRequired.join(', ')}.

## Honest conclusion

${honestConclusion.map((c) => `- ${c}`).join('\n')}
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-anisotropy-topology-test-design.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('ri-anisotropy-topology-test-design.md', outDir), markdown);

console.log(`RI anisotropy-topology test design: ${report.status}`);
