import { readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

async function readJson(name) {
  return JSON.parse(await readFile(new URL(name, outDir), 'utf8'));
}

async function readOptionalJson(name) {
  try {
    return await readJson(name);
  } catch {
    return null;
  }
}

const coordinate = await readJson('molecule-coordinate-sweep.json');
const calibration = await readJson('molecule-calibration-summary.json');
const coupling = await readJson('t1-coupling-patterns.json');
const sweep = await readJson('t1-coupling-sweep.json');
const stability = await readJson('t1-target-stability.json');
const refinement = await readJson('t1-local-refinement.json');
const ethaneTorsion = await readOptionalJson('ethane-torsion-sweep.json');
const peroxideTorsion = await readOptionalJson('peroxide-torsion-sweep.json');
const peroxideRefinement = await readOptionalJson('peroxide-nonlocal-refinement.json');
const ionicLattice = await readOptionalJson('ionic-lattice-sweep.json');
const silicateNetwork = await readOptionalJson('silicate-network-sweep.json');
const mixedModifier = await readOptionalJson('mixed-modifier-sweep.json');
const boundaryTransition = await readOptionalJson('boundary-transition-sweep.json');
const phaseContinuity = await readOptionalJson('phase-continuity-sweep.json');

const assumptions = [
  {
    category: 'Ontology Boundary',
    items: [
      {
        assumption: 'T0 substrate is not directly simulated.',
        status: 'foundational',
        risk: 'The model can only test coherence of inferred behaviour, not visibility or proof of substrate.',
      },
      {
        assumption: 'No material middle layer is allowed between T0 substrate and T1 vortons.',
        status: 'hard guardrail',
        risk: 'Any future model that inserts cells, lattices, particles, or material fillers at this level violates the ontology.',
      },
      {
        assumption: 'Vortons are treated as candidate stable primary topology, not as conventional particles.',
        status: 'foundational',
        risk: 'The numeric parameters are descriptors of coupling grammar, not evidence that a specific vorton shape exists.',
      },
      {
        assumption: 'Atoms and molecules are T2 secondary material regimes, not T1 vorton species.',
        status: 'hard guardrail',
        risk: 'The molecule bench cannot be used to claim that atoms have been derived from T1; it only constrains possible T1 coupling grammar.',
      },
      {
        assumption: 'Matter is treated as real perceived geometry/grammar arising from stable substrate expression.',
        status: 'interpretive',
        risk: 'This is a Relational Substrate framing assumption; the software does not prove perception, matter, or ontology.',
      },
    ],
  },
  {
    category: 'Reference Data',
    items: [
      {
        assumption: 'Classical molecular geometries can be used as calibration anchors.',
        status: 'working',
        risk: 'The anchors constrain coherence but do not define the Relational Substrate ontology.',
      },
      {
        assumption: 'Rounded gas-phase geometry values are adequate for this early-stage test bench.',
        status: 'temporary',
        risk: 'Higher-precision and source-specific values may alter family envelopes.',
      },
      {
        assumption: 'The current molecule cases are representative enough to test initial family behaviour.',
        status: 'temporary',
        risk: 'The sample is too small for strong claims; more families and more examples per family are needed.',
      },
      {
        assumption: 'NaCl and LiF are only gas-phase ionic pair proxies.',
        status: ionicLattice ? 'explicit limitation with focused diagnostic' : 'explicit limitation',
        risk: 'The molecule coordinate bench does not represent ionic crystal lattices or bulk material behaviour; the ionic lattice sweep is a separate topology/control diagnostic.',
      },
      {
        assumption: 'Benzene and pyridine are planar aromatic proxies.',
        status: 'working',
        risk: 'Substitution, resonance detail, and full electronic structure are outside current scope.',
      },
    ],
  },
  {
    category: 'T2 Molecule Scoring',
    items: [
      {
        assumption: 'Known reference geometries should rank first against generated perturbations.',
        status: 'sanity check',
        risk: 'Passing this check shows internal calibration only, not physical derivation.',
      },
      {
        assumption: 'No generated perturbation should beat the reference in the current calibration stage.',
        status: 'sanity check',
        risk: 'If a generated perturbation beats the reference, the score grammar or reference construction needs review.',
      },
      {
        assumption: 'Near-reference rate is a useful proxy for coherence envelope width.',
        status: 'working',
        risk: 'The 95% threshold is conventional within this bench and may need calibration.',
      },
      {
        assumption: 'Strong-failure rate is a useful proxy for constraint severity.',
        status: 'working',
        risk: 'The failure threshold is model-defined, not empirically established.',
      },
      {
        assumption: 'Different molecule families need different weights over the same coherence variables.',
        status: 'working',
        risk: 'Family-specific weights improve coherence but may hide overfitting until more reference cases are added.',
      },
      {
        assumption: 'Explicit decoy controls should score below the reference geometry.',
        status: 'stress test',
        risk: 'A weak decoy penalty identifies an underweighted constraint even when the reference still ranks first.',
      },
      {
        assumption: 'Ethane torsion phase should separate staggered-like and eclipsed-like conformers.',
        status: ethaneTorsion ? 'focused diagnostic' : 'pending diagnostic',
        risk: 'The current torsion metric separates phase, but the steric/crowding feature remains too flat for rotatable conformer work.',
      },
      {
        assumption: 'Peroxide torsion should expose skew preference without being fitted as a new anchor.',
        status: peroxideRefinement ? 'focused diagnostic with nonlocal refinement' : peroxideTorsion ? 'focused diagnostic' : 'pending diagnostic',
        risk: 'Peroxide mixes torsion, polarity, and H-H separation; weak nonlocal separation would show that rotatable covalent is still too ethane-specific.',
      },
      {
        assumption: 'Ionic pair proxies should not be mistaken for bulk ionic lattice behaviour.',
        status: ionicLattice ? 'focused diagnostic' : 'pending diagnostic',
        risk: 'The lattice sweep tests only a tiny alternating-charge grammar; it is not a crystal physics model and should not be merged into molecule calibration as if it were one.',
      },
      {
        assumption: 'Silicate and aluminosilicate network order requires separate material-structure diagnostics.',
        status: silicateNetwork ? 'focused diagnostic' : 'pending diagnostic',
        risk: 'The silicate network sweep is graph-level only; it does not simulate real glass structure, crystal order, melt history, or measured material properties.',
      },
      {
        assumption: 'Mixed modifier transport order needs pressure testing apart from static network continuity.',
        status: mixedModifier ? 'focused diagnostic' : 'pending diagnostic',
        risk: 'The mixed-modifier sweep is route-level only; it does not simulate diffusion, conductivity, glass transition behaviour, or durability.',
      },
      {
        assumption: 'Boundary and interface transitions need separate route-splitting diagnostics.',
        status: boundaryTransition ? 'focused diagnostic' : 'pending diagnostic',
        risk: 'The boundary transition sweep is route-level only; it does not simulate optical equations, surface roughness, crystallography, or measured interface behaviour.',
      },
      {
        assumption: 'Phase continuity must be tested apart from apparent transmission strength.',
        status: phaseContinuity ? 'focused diagnostic' : 'pending diagnostic',
        risk: 'The phase continuity sweep is still a route-memory diagnostic; it does not implement wave optics or measured phase behaviour.',
      },
    ],
  },
  {
    category: 'T1 Coupling Descriptors',
    items: [
      {
        assumption: 'T1-to-T2 coupling can be represented by route count, closure topology, polarity mode, angular constraint, torsion mode, and distribution mode.',
        status: 'candidate mechanism',
        risk: 'These descriptors are plausible grammar categories, not demonstrated physical primitives.',
      },
      {
        assumption: 'The current family descriptors are sufficient for the current molecule families.',
        status: 'temporary',
        risk: 'Additional molecule families may require new descriptors or split existing descriptors.',
      },
      {
        assumption: 'Descriptor priors are allowed only for broad features not directly present in T2 metrics.',
        status: 'discipline rule',
        risk: 'Too much prior information would reintroduce hand placement and weaken the test.',
      },
      {
        assumption: 'Admissibility gates can reject incoherent T1 candidates before scoring.',
        status: 'working',
        risk: 'Bad guardrails could exclude valid candidates or admit incoherent ones.',
      },
    ],
  },
  {
    category: 'T1 Numeric Parameters',
    items: [
      {
        assumption: 'Ten scalar parameters can represent the first-pass T1 coupling envelope.',
        status: 'working',
        risk: 'The real coupling grammar may require additional dimensions or non-scalar structure.',
      },
      {
        assumption: 'The current parameters are comparable across families.',
        status: 'working',
        risk: 'A value like angularConstraint may not mean exactly the same thing in a ring and a bent polar molecule.',
      },
      {
        assumption: 'T2 metrics can derive T1 target envelopes through one shared formula.',
        status: 'current test',
        risk: 'The formula may fail when more molecule families are added.',
      },
      {
        assumption: 'Residuals between T1 candidates and derived targets are meaningful coherence diagnostics.',
        status: 'working',
        risk: 'Residuals measure fit to the current formula, not truth of the Relational Substrate theory.',
      },
      {
        assumption: 'Local refinement around best candidates can distinguish coarse-grid error from formula weakness.',
        status: 'validated for current run',
        risk: 'Refinement improves fit but may also make overfitting easier if used without new data.',
      },
    ],
  },
  {
    category: 'Sweep Mechanics',
    items: [
      {
        assumption: 'Discrete parameter grids are adequate for early exploration.',
        status: 'temporary',
        risk: 'Coarse grids create residuals that may disappear under local refinement.',
      },
      {
        assumption: 'Current guardrails are strict enough to prevent obviously incoherent candidates.',
        status: 'working',
        risk: 'Guardrails are hand-authored and need pressure testing.',
      },
      {
        assumption: 'Top candidate score is a useful ranking metric.',
        status: 'working',
        risk: 'A high score only means fit to current target/weight assumptions.',
      },
      {
        assumption: 'Counting iterations and rejection categories is a useful scale marker.',
        status: 'working',
        risk: 'Large iteration counts do not imply better truth, only broader search coverage.',
      },
    ],
  },
  {
    category: 'Current Empirical Status',
    items: [
      {
        assumption: 'The current system is coherent enough to extend, not mature enough to claim derivation.',
        status: 'summary',
        risk: 'The model should remain framed as a coherence test bench.',
      },
      {
        assumption: 'The current best evidence is internal consistency across reference ranking, decoy rejection, family validation, T1 target derivation, stability, and local refinement.',
        status: 'summary',
        risk: 'Internal consistency can still be circular if new independent calibration cases are not added.',
      },
      {
        assumption: 'The next meaningful stress test is adding independent cases without per-family tuning.',
        status: 'next-step',
        risk: 'If new cases are fitted by special rules instead of shared descriptors, the model becomes overfit instead of more explanatory.',
      },
    ],
  },
];

const metrics = {
  t2: {
    molecules: coordinate.molecules,
    coordinateIterations: coordinate.totalIterations,
    families: calibration.families.length,
    allFamiliesPassCurrentSanityCheck: calibration.families.every((family) => family.status === 'passes current sanity check'),
    decoyControls: calibration.controls.length,
    allDecoyControlsRejected: calibration.controls.every((control) => control.referenceBeatsDecoy),
    weakDecoyControls: calibration.controls
      .filter((control) => control.decoyPenalty < 0.1 || control.decoyRank <= 25)
      .map((control) => control.label),
  },
  t1: {
    descriptorFamilies: coupling.families.length,
    sweepIterations: sweep.totalIterations,
    sweepAccepted: sweep.acceptedIterations,
    sweepRejected: sweep.rejectedIterations,
    refinementIterations: refinement.totalIterations,
    refinementAccepted: refinement.acceptedIterations,
    weakestFamilyBeforeRefinement: stability.weakestFamilies[0].family,
    weakestParametersBeforeRefinement: stability.weakestParameters.map((parameter) => parameter.parameter),
  },
  focusedDiagnostics: {
    ethaneTorsion: ethaneTorsion
      ? {
          weakestEclipsedPenalty: ethaneTorsion.summary.weakestEclipsedPenalty,
          meanEclipsedPenalty: ethaneTorsion.summary.meanEclipsedPenalty,
          diagnosis: ethaneTorsion.summary.diagnosis,
        }
      : null,
    peroxideTorsion: peroxideTorsion
      ? {
          lowestNearReferencePenalty: peroxideTorsion.summary.lowestNearReferencePenalty,
          lowestNonLocalPenalty: peroxideTorsion.summary.lowestNonLocalPenalty,
          frontierPenalty: peroxideTorsion.summary.frontierPenalty ?? peroxideTorsion.summary.lowestNonLocalPenalty,
          refinedFrontierPenalty: peroxideRefinement?.summary.frontierPenalty ?? null,
          diagnosis: peroxideTorsion.summary.diagnosis,
        }
      : null,
    ionicLattice: ionicLattice
      ? {
          diagnosis: ionicLattice.diagnosis,
          summaries: ionicLattice.summaries.map((summary) => ({
            formula: summary.formula,
            referenceScore: summary.referenceScore,
            bestDecoy: summary.bestDecoy,
            bestDecoyScore: summary.bestDecoyScore,
            decoyPenalty: summary.decoyPenalty,
            referenceBeatsDecoys: summary.referenceBeatsDecoys,
          })),
        }
      : null,
    silicateNetwork: silicateNetwork
      ? {
          diagnosis: silicateNetwork.diagnosis,
          summaries: silicateNetwork.summaries.map((summary) => ({
            formula: summary.formula,
            referenceScore: summary.referenceScore,
            bestDecoy: summary.bestDecoy,
            bestDecoyScore: summary.bestDecoyScore,
            decoyPenalty: summary.decoyPenalty,
            referenceBeatsDecoys: summary.referenceBeatsDecoys,
          })),
        }
      : null,
    mixedModifier: mixedModifier
      ? {
          diagnosis: mixedModifier.diagnosis,
          summaries: mixedModifier.summaries.map((summary) => ({
            formula: summary.formula,
            referenceScore: summary.referenceScore,
            bestDecoy: summary.bestDecoy,
            bestDecoyScore: summary.bestDecoyScore,
            decoyPenalty: summary.decoyPenalty,
            referenceBeatsDecoys: summary.referenceBeatsDecoys,
          })),
        }
      : null,
    boundaryTransition: boundaryTransition
      ? {
          diagnosis: boundaryTransition.diagnosis,
          summaries: boundaryTransition.summaries.map((summary) => ({
            case: summary.case,
            referenceScore: summary.referenceScore,
            bestDecoy: summary.bestDecoy,
            bestDecoyScore: summary.bestDecoyScore,
            decoyPenalty: summary.decoyPenalty,
            referenceBeatsDecoys: summary.referenceBeatsDecoys,
          })),
        }
      : null,
    phaseContinuity: phaseContinuity
      ? {
          diagnosis: phaseContinuity.diagnosis,
          summaries: phaseContinuity.summaries.map((summary) => ({
            case: summary.case,
            referenceScore: summary.referenceScore,
            bestDecoy: summary.bestDecoy,
            bestDecoyScore: summary.bestDecoyScore,
            decoyPenalty: summary.decoyPenalty,
            referenceBeatsDecoys: summary.referenceBeatsDecoys,
          })),
        }
      : null,
  },
};

const json = {
  status: 'current Relational Substrate sandbox modelling assumptions',
  generatedFrom: [
    'molecule-coordinate-sweep.json',
    'molecule-calibration-summary.json',
    't1-coupling-patterns.json',
    't1-coupling-sweep.json',
    't1-target-stability.json',
    't1-local-refinement.json',
    'ethane-torsion-sweep.json',
    'peroxide-torsion-sweep.json',
    'peroxide-nonlocal-refinement.json',
    'ionic-lattice-sweep.json',
    'silicate-network-sweep.json',
    'mixed-modifier-sweep.json',
    'boundary-transition-sweep.json',
    'phase-continuity-sweep.json',
  ],
  metrics,
  assumptions,
};

await writeFile(new URL('model-assumptions.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate Sandbox Modelling Assumptions

## Scope

This report lists the assumptions currently built into the Relational Substrate topology and molecule coherence sandbox.

It does not prove the Relational Substrate theory. It makes the modelling commitments explicit so future changes can be judged against them.

## Current Scale

| Area | Metric | Value |
|---|---|---:|
| T2 coordinate bench | Molecules | ${metrics.t2.molecules} |
| T2 coordinate bench | Coordinate iterations | ${metrics.t2.coordinateIterations} |
| T2 calibration | Families | ${metrics.t2.families} |
| T2 calibration | All families pass current sanity check | ${metrics.t2.allFamiliesPassCurrentSanityCheck ? 'yes' : 'no'} |
| T2 decoy controls | Controls | ${metrics.t2.decoyControls} |
| T2 decoy controls | All references beat decoys | ${metrics.t2.allDecoyControlsRejected ? 'yes' : 'no'} |
| T2 decoy controls | Weak controls | ${metrics.t2.weakDecoyControls.length ? metrics.t2.weakDecoyControls.join(', ') : 'none'} |
| Focused diagnostics | Ethane weakest eclipsed penalty | ${metrics.focusedDiagnostics.ethaneTorsion ? metrics.focusedDiagnostics.ethaneTorsion.weakestEclipsedPenalty : 'not run'} |
| Focused diagnostics | Peroxide lowest near-reference penalty | ${metrics.focusedDiagnostics.peroxideTorsion ? metrics.focusedDiagnostics.peroxideTorsion.lowestNearReferencePenalty : 'not run'} |
| Focused diagnostics | Peroxide lowest nonlocal penalty | ${metrics.focusedDiagnostics.peroxideTorsion ? metrics.focusedDiagnostics.peroxideTorsion.lowestNonLocalPenalty : 'not run'} |
| Focused diagnostics | Peroxide refined frontier penalty | ${metrics.focusedDiagnostics.peroxideTorsion?.refinedFrontierPenalty ?? 'not run'} |
| Focused diagnostics | Ionic lattice diagnosis | ${metrics.focusedDiagnostics.ionicLattice ? metrics.focusedDiagnostics.ionicLattice.diagnosis : 'not run'} |
| Focused diagnostics | Silicate network diagnosis | ${metrics.focusedDiagnostics.silicateNetwork ? metrics.focusedDiagnostics.silicateNetwork.diagnosis : 'not run'} |
| Focused diagnostics | Mixed modifier diagnosis | ${metrics.focusedDiagnostics.mixedModifier ? metrics.focusedDiagnostics.mixedModifier.diagnosis : 'not run'} |
| Focused diagnostics | Boundary transition diagnosis | ${metrics.focusedDiagnostics.boundaryTransition ? metrics.focusedDiagnostics.boundaryTransition.diagnosis : 'not run'} |
| Focused diagnostics | Phase continuity diagnosis | ${metrics.focusedDiagnostics.phaseContinuity ? metrics.focusedDiagnostics.phaseContinuity.diagnosis : 'not run'} |
| T1 descriptors | Families | ${metrics.t1.descriptorFamilies} |
| T1 sweep | Candidates tried | ${metrics.t1.sweepIterations} |
| T1 sweep | Accepted | ${metrics.t1.sweepAccepted} |
| T1 sweep | Rejected | ${metrics.t1.sweepRejected} |
| T1 refinement | Local candidates tried | ${metrics.t1.refinementIterations} |
| T1 refinement | Accepted | ${metrics.t1.refinementAccepted} |

## Assumptions

${assumptions
  .map(
    (section) => `### ${section.category}

| Assumption | Status | Risk / Limitation |
|---|---|---|
${section.items.map((item) => `| ${item.assumption} | ${item.status} | ${item.risk} |`).join('\n')}
`
  )
  .join('\n')}

## Working Interpretation

The current model is a coherence test bench. It has a candidate mechanism path from substrate disturbance to T1 coupling grammar to T2 material regimes, but it has not derived matter from first principles.

The main live assumption is that the same T2-derived target formula can survive more molecule families without per-family tuning. That is the next stress test.
`;

await writeFile(new URL('model-assumptions.md', outDir), markdown);

console.log(`Wrote ${new URL('model-assumptions.md', outDir).pathname}`);
