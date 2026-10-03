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

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

function penaltyBand(value) {
  if (value < 0.1) {
    return 'weak';
  }
  if (value < 0.2) {
    return 'watch';
  }
  return 'clear';
}

function residualBand(value) {
  const magnitude = Math.abs(value);
  if (magnitude > 0.12) {
    return 'weak';
  }
  if (magnitude > 0.08) {
    return 'watch';
  }
  return 'clear';
}

function addPenaltyFrontier(items, source, summary, labelKey = 'case') {
  items.push({
    source,
    label: summary[labelKey] ?? summary.formula ?? summary.label,
    challenger: summary.bestDecoy ?? summary.decoy ?? 'nearest decoy',
    metric: 'decoy penalty',
    value: summary.decoyPenalty,
    band: penaltyBand(summary.decoyPenalty),
  });
}

const calibration = await readJson('molecule-calibration-summary.json');
const stability = await readJson('t1-target-stability.json');
const ethaneTorsion = await readOptionalJson('ethane-torsion-sweep.json');
const peroxideTorsion = await readOptionalJson('peroxide-torsion-sweep.json');
const peroxideRefinement = await readOptionalJson('peroxide-nonlocal-refinement.json');
const peroxideReleaseSensitivity = await readOptionalJson('peroxide-anti-planar-release-sensitivity.json');
const peroxideCh3oohDiagnostic = await readOptionalJson('peroxide-methyl-hydroperoxide-scoring-diagnostic.json');
const peroxideSubstitutedPredeclaration = await readOptionalJson('peroxide-substituted-rotor-evidence-predeclaration.json');
const peroxideEthylSourceLock = await readOptionalJson('peroxide-ethyl-hydroperoxide-source-lock-screen.json');
const peroxideEthylHint = await readOptionalJson('peroxide-ethyl-hydroperoxide-search-hint-diagnostic.json');
const peroxideEthylScore = await readOptionalJson('peroxide-ethyl-hydroperoxide-evidence-scoring.json');
const peroxideEvidencePolicy = await readOptionalJson('peroxide-evidence-ledger-policy.json');
const peroxidePromotionReview = await readOptionalJson('peroxide-release-promotion-review.json');
const peroxideDualChannelPredeclaration = await readOptionalJson(
  'peroxide-dual-channel-model-form-predeclaration.json',
);
const peroxideDualChannelDiagnostic = await readOptionalJson('peroxide-dual-channel-feasibility-diagnostic.json');
const peroxideDualChannelReservation = await readOptionalJson('peroxide-dual-channel-target-reservation.json');
const peroxideDimethylSourceLock = await readOptionalJson('peroxide-dimethyl-source-lock-screen.json');
const peroxideObservableRouteDiagnostic = await readOptionalJson(
  'peroxide-observable-route-feasibility-diagnostic.json',
);
const peroxideObservableRouteReservation = await readOptionalJson(
  'peroxide-observable-route-target-reservation.json',
);
const peroxideDiethylSourceLock = await readOptionalJson('peroxide-diethyl-source-lock-screen.json');
const peroxideTbhpReservation = await readOptionalJson('peroxide-tbhp-target-reservation.json');
const peroxideTbhpScore = await readOptionalJson('peroxide-tbhp-observable-route-scoring.json');
const peroxidePeroxyformicReservation = await readOptionalJson(
  'peroxide-peroxyformic-target-reservation.json',
);
const peroxidePeroxyformicScore = await readOptionalJson(
  'peroxide-peroxyformic-profile-scoring.json',
);
const peroxideRelativeCrowding = await readOptionalJson(
  'peroxide-equilibrium-relative-crowding-diagnostic.json',
);
const peroxideV2Reservation = await readOptionalJson(
  'peroxide-v2-fresh-target-reservation.json',
);
const peroxideHmhpSourceLock = await readOptionalJson(
  'peroxide-hmhp-source-lock-screen.json',
);
const peroxideMethylChloroReservation = await readOptionalJson(
  'peroxide-methyl-chloroperoxide-reservation.json',
);
const peroxideMethylChloroSourceLock = await readOptionalJson(
  'peroxide-methyl-chloroperoxide-source-lock-screen.json',
);
const ionicLattice = await readOptionalJson('ionic-lattice-sweep.json');
const silicateNetwork = await readOptionalJson('silicate-network-sweep.json');
const mixedModifier = await readOptionalJson('mixed-modifier-sweep.json');
const boundaryTransition = await readOptionalJson('boundary-transition-sweep.json');
const phaseContinuity = await readOptionalJson('phase-continuity-sweep.json');
const neutralHydrazineReservation = await readOptionalJson(
  'neutral-hydrazine-torsion-target-reservation.json',
);
const neutralHydrazineSourceLock = await readOptionalJson(
  'neutral-hydrazine-torsion-source-lock-screen.json',
);
const roughnessBrdfPredeclaration = await readOptionalJson(
  'roughness-psd-brdf-model-form-predeclaration.json',
);
const roughnessTungstenReservation = await readOptionalJson(
  'roughness-tungsten-brdf-target-reservation.json',
);
const roughnessTungstenSourceLock = await readOptionalJson(
  'roughness-tungsten-brdf-source-lock-screen.json',
);
const roughnessSourceAvailability = await readOptionalJson(
  'roughness-psd-brdf-source-availability-screen.json',
);
const roughnessTayabalyReservation = await readOptionalJson(
  'roughness-tayabaly-brdf-target-reservation.json',
);
const roughnessTayabalySourceLock = await readOptionalJson(
  'roughness-tayabaly-brdf-source-lock-screen.json',
);
const roughnessPsdCrossPredeclaration = await readOptionalJson(
  'roughness-profile-psd-scatter-psd-predeclaration.json',
);
const roughnessBrdfFeasibility = await readOptionalJson(
  'roughness-psd-brdf-feasibility-diagnostic.json',
);

const frontiers = [];
const localToleranceFrontiers = [];

for (const control of calibration.controls) {
  frontiers.push({
    source: 'molecule decoy control',
    label: control.label,
    challenger: control.expectedFailure ?? control.candidate?.name ?? 'explicit decoy control',
    metric: 'decoy penalty',
    value: control.decoyPenalty,
    band: penaltyBand(control.decoyPenalty),
  });
}

if (ethaneTorsion) {
  frontiers.push({
    source: 'ethane torsion',
    label: 'weakest eclipsed conformer',
    challenger: 'eclipsed-like phase',
    metric: 'torsion penalty',
    value: ethaneTorsion.summary.weakestEclipsedPenalty,
    band: penaltyBand(ethaneTorsion.summary.weakestEclipsedPenalty),
  });
}

if (peroxideTorsion) {
  if (typeof peroxideTorsion.summary.lowestNearReferencePenalty === 'number') {
    localToleranceFrontiers.push({
      source: 'peroxide torsion tolerance',
      label: 'nearest local torsion neighbour',
      challenger: `${peroxideTorsion.summary.nearReferenceWindow} degree near-reference window`,
      metric: 'local tolerance penalty',
      value: peroxideTorsion.summary.lowestNearReferencePenalty,
      band: 'local',
    });
  }
  frontiers.push({
    source: 'peroxide torsion',
    label: 'nonlocal torsion challenger',
    challenger: 'nonlocal torsion decoy',
    metric: 'torsion penalty',
    value: peroxideRefinement?.summary.frontierPenalty ?? peroxideTorsion.summary.frontierPenalty ?? peroxideTorsion.summary.lowestNonLocalPenalty,
    band: penaltyBand(peroxideRefinement?.summary.frontierPenalty ?? peroxideTorsion.summary.frontierPenalty ?? peroxideTorsion.summary.lowestNonLocalPenalty),
  });
}

if (peroxideRefinement) {
  for (const item of peroxideRefinement.summary.byBand.filter((band) => band.band !== 'nonlocal')) {
    localToleranceFrontiers.push({
      source: 'peroxide torsion refinement',
      label: item.band,
      challenger: `${item.rows} refined torsion rows`,
      metric: 'weakest penalty',
      value: item.weakestPenalty,
      band: item.band === 'near-reference' ? 'local' : 'shoulder',
    });
  }
}

for (const report of [
  ['ionic lattice', ionicLattice, 'formula'],
  ['silicate network', silicateNetwork, 'formula'],
  ['mixed modifier', mixedModifier, 'formula'],
  ['boundary transition', boundaryTransition, 'case'],
  ['phase continuity', phaseContinuity, 'case'],
]) {
  const [source, data, labelKey] = report;
  if (!data) {
    continue;
  }
  for (const summary of data.summaries) {
    addPenaltyFrontier(frontiers, source, summary, labelKey);
  }
}

const residualFrontiers = [
  ...stability.weakestFamilies.slice(0, 6).map((family) => ({
    source: 'T1 family residual',
    label: family.family,
    challenger: 'best admissible T1 candidate',
    metric: 'residual',
    value: family.residual,
    magnitude: Math.abs(family.residual),
    band: residualBand(family.residual),
  })),
  ...stability.weakestParameters.slice(0, 6).map((parameter) => ({
    source: 'T1 parameter residual',
    label: parameter.parameter,
    challenger: 'derived target envelope',
    metric: 'mean residual',
    value: parameter.meanResidual,
    magnitude: Math.abs(parameter.meanResidual),
    band: residualBand(parameter.meanResidual),
  })),
];

const rankedPenaltyFrontiers = frontiers
  .filter((item) => typeof item.value === 'number')
  .sort((a, b) => a.value - b.value)
  .map((item) => ({ ...item, value: round(item.value) }));
const rankedResidualFrontiers = residualFrontiers
  .filter((item) => typeof item.value === 'number')
  .sort((a, b) => b.magnitude - a.magnitude)
  .map((item) => ({ ...item, value: round(item.value), magnitude: round(item.magnitude) }));

const weakestPenalty = rankedPenaltyFrontiers[0];
const weakestResidual = rankedResidualFrontiers[0];
const rankedNextTarget =
  weakestPenalty?.band === 'weak'
    ? `tighten ${weakestPenalty.source}: ${weakestPenalty.label}`
    : weakestPenalty?.band === 'watch'
      ? `watch and refine ${weakestPenalty.source}: ${weakestPenalty.label}`
    : weakestResidual?.band === 'weak'
      ? `tighten ${weakestResidual.source}: ${weakestResidual.label}`
      : 'add an independent external benchmark case rather than tuning existing diagnostics';
const nextTarget =
  roughnessPsdCrossPredeclaration?.status ===
  'profile-PSD versus scatter-derived-PSD model form frozen'
    ? 'implement synthetic known-answer checks for the frozen profile-PSD versus scatter-derived-PSD comparator before screening a fresh target'
    :
  roughnessTayabalySourceLock?.sourceLockDecision?.status ===
  'source-lock-failed-raw-angular-brdf-not-exposed'
    ? 'predeclare an independent-profile-PSD versus BRDF-derived-PSD shape comparator before any new target selection, or obtain the raw Tayabaly silicon-wafer angular BRDF rows'
    :
  roughnessTayabalyReservation?.status ===
  'Tayabaly optical-flat PSD/BRDF target reserved before full-text extraction'
    ? 'source-lock the reserved Tayabaly optical-flat profile PSD and wavelength-tagged angular BRDF without changing the frozen comparator'
    :
  roughnessTungstenSourceLock?.sourceLockDecision?.status ===
  'source-lock-failed-unpaired-psd-brdf-constructs'
    ? 'the three priority validation fronts are source-blocked; obtain wavelength-tagged M100 angular BRDF data, a neutral-hydrazine angle-mapped barrier table, or a fresh peroxide numerical torsion profile before further evidence-bearing scoring'
    : neutralHydrazineSourceLock?.sourceLockDecision?.status ===
  'source-lock-failed-mixed-and-ambiguous-barrier-constructs'
    ? 'advance the roughness/interface track with a predeclared measured BRDF or PSD comparator; peroxide v2 and neutral-hydrazine absolute transfer are source-blocked'
    : peroxideMethylChloroSourceLock?.sourceLockDecision?.status ===
  'source-lock-failed-numerical-profile-inaccessible'
    ? 'treat the peroxide v2 fresh-validation branch as source-blocked until a primary numerical one-dimensional torsional profile is supplied; do not reserve another metadata-only identity'
    : peroxideHmhpSourceLock?.sourceLockDecision?.status ===
  'source-lock-failed-coupled-conformer-profile'
    ? 'run a metadata-only source-availability screen for a fresh peroxide target with an explicit one-dimensional torsional scan before reserving another identity'
    : peroxideEvidencePolicy?.reviewDecision?.status ===
  'heldout-failure-redesign-feasible-fresh-validation-required'
    ? peroxideEvidencePolicy.reviewDecision.nextGate
    : peroxideEvidencePolicy?.reviewDecision?.status ===
  'heldout-intermediate-profile-fail-model-redesign-required'
    ? peroxideEvidencePolicy.reviewDecision.nextGate
    : peroxideEvidencePolicy?.reviewDecision?.status === 'limited-branch-support-no-model-promotion'
    ? peroxideEvidencePolicy.reviewDecision.nextGate
    : peroxideTbhpScore?.status === 'heldout-observable-route-comparator-pass'
    ? 'review the TBHP held-out comparator in the peroxide evidence ledger before any confidence or model promotion'
    : peroxideTbhpReservation?.status ===
        'tert-butyl hydroperoxide reserved before numerical source extraction'
      ? 'source-lock and score the reserved TBHP target under the frozen observable-route model'
    : peroxideDiethylSourceLock?.sourceLockDecision?.status ===
  'source-lock-failed-paired-torsional-comparator'
    ? 'predeclare a peroxide source-availability screen before reserving another observable-route target'
    : peroxideObservableRouteReservation?.status ===
        'fresh observable-route target reserved before source lookup'
      ? 'source-lock the reserved diethyl-peroxide equilibrium and nonlocal torsional comparator'
    : peroxideObservableRouteDiagnostic?.status === 'exposed-observable-route-feasibility-pass'
    ? 'reserve a new peroxide-like rotor before lookup for the frozen observable-route descriptor'
    : peroxideDimethylSourceLock?.sourceLockDecision?.scoringStatus === 'blocked-by-underspecified-target-mapping'
    ? 'redesign the peroxide selection descriptor around source-observable torsion inputs before reserving another target'
    : peroxideDualChannelReservation?.status === 'fresh dual-channel target reserved before source lookup'
    ? 'source-lock dimethyl peroxide geometry and torsional energy data without changing the frozen dual-channel model'
    : peroxideDualChannelDiagnostic?.status === 'exposed-feasibility-pass'
      ? 'reserve a fresh peroxide-like rotor before lookup and test the frozen dual-channel model unchanged'
    : peroxidePromotionReview?.status === 'promotion-blocked-cross-benchmark-regression'
    ? 'resolve the peroxide release tradeoff: improve nonlocal separation without increasing the H2O2 trans barrier penalty'
    : rankedNextTarget;
const peroxideReleaseGuidance = peroxideReleaseSensitivity
  ? {
      current: peroxideReleaseSensitivity.current,
      directionReading: peroxideReleaseSensitivity.directionReading,
      bestDiagnostic: peroxideReleaseSensitivity.topCandidates?.[0] ?? null,
      leastDisruptiveNonzero: peroxideReleaseSensitivity.topNonzeroCandidates?.[0] ?? null,
    }
  : null;
const peroxideCh3oohGuidance = peroxideCh3oohDiagnostic
  ? {
      status: peroxideCh3oohDiagnostic.decision.status,
      evidenceStatus: peroxideCh3oohDiagnostic.decision.evidenceStatus,
      reading: peroxideCh3oohDiagnostic.decision.reading,
      nextGate: peroxideCh3oohDiagnostic.decision.nextGate,
      frozenRepair: peroxideCh3oohDiagnostic.frozenRepair,
      sourceComparators: peroxideCh3oohDiagnostic.sourceComparators,
      diagnosticChecks: peroxideCh3oohDiagnostic.diagnosticChecks,
    }
  : null;
const peroxideNextEvidenceGate = peroxideSubstitutedPredeclaration
  ? {
      status: peroxideSubstitutedPredeclaration.status,
      target: peroxideSubstitutedPredeclaration.reservedTarget,
      frozenRule: peroxideSubstitutedPredeclaration.frozenRule,
      predeclarationHash: peroxideSubstitutedPredeclaration.predeclaration?.hash ?? null,
      sourceLockStatus: peroxideEthylSourceLock?.sourceLockDecision?.status ?? 'source lock not yet run',
      sourceLockReason: peroxideEthylSourceLock?.sourceLockDecision?.reason ?? null,
      primaryCandidate: peroxideEthylSourceLock?.sourceLockDecision?.primaryCandidate ?? null,
      hint: peroxideEthylHint
        ? {
            status: peroxideEthylHint.decision.status,
            evidenceStatus: peroxideEthylHint.decision.evidenceStatus,
            ratio: peroxideEthylHint.hintedValues.transCisRatio,
            threshold: peroxideEthylHint.hintedValues.ratioThreshold,
            margin: peroxideEthylHint.hintedValues.margin,
          }
        : null,
      score: peroxideEthylScore
        ? {
            status: peroxideEthylScore.decision.status,
            evidenceStatus: peroxideEthylScore.decision.evidenceStatus,
            reading: peroxideEthylScore.decision.reading,
            confidenceEffect: peroxideEthylScore.decision.confidenceEffect,
            sourceRatio: peroxideEthylScore.sourceComparators.sourceBarrierRatio,
            predictedRatio: peroxideEthylScore.checks.predictedPenaltyRatio,
          }
        : null,
    }
  : null;
const peroxideEvidencePolicyGuidance = peroxideEvidencePolicy
  ? {
      globalConfidenceAction: peroxideEvidencePolicy.globalConfidenceAction,
      branchConfidenceAction: peroxideEvidencePolicy.branchConfidenceAction,
      computedComparatorPasses: peroxideEvidencePolicy.records.filter(
        (record) => record.policy?.ledgerClass === 'computed-comparator-heldout-pass',
      ).length,
      observableRoutePasses: peroxideEvidencePolicy.records.filter(
        (record) => record.policy?.ledgerClass === 'observable-route-heldout-pass',
      ).length,
      intermediateProfileFails: peroxideEvidencePolicy.records.filter(
        (record) => record.policy?.ledgerClass === 'intermediate-profile-heldout-fail',
      ).length,
      reviewDecision: peroxideEvidencePolicy.reviewDecision ?? null,
      exposedRedesign: peroxideEvidencePolicy.exposedRedesign ?? null,
      warnings: peroxideEvidencePolicy.warnings,
    }
  : null;
const peroxidePromotionGuidance = peroxidePromotionReview
  ? {
      status: peroxidePromotionReview.status,
      decision: peroxidePromotionReview.decision,
      currentLiveRelease: peroxidePromotionReview.currentLiveRelease,
      candidateRelease: peroxidePromotionReview.candidateRelease,
      candidateMetrics: peroxidePromotionReview.candidateMetrics,
      failedChecks: peroxidePromotionReview.failedChecks,
      nextModelRequirement: peroxidePromotionReview.nextModelRequirement,
    }
  : null;
const peroxideDualChannelGuidance =
  peroxideDualChannelPredeclaration && peroxideDualChannelDiagnostic
    ? {
        status: peroxideDualChannelDiagnostic.status,
        predeclarationHash: peroxideDualChannelDiagnostic.predeclarationHash,
        energy: peroxideDualChannelDiagnostic.channels.energy,
        selection: peroxideDualChannelDiagnostic.channels.selection,
        evidenceStatus: peroxideDualChannelDiagnostic.evidenceStatus,
        decision: peroxideDualChannelDiagnostic.decision,
        nextGate: peroxideDualChannelDiagnostic.nextGate,
        reservation: peroxideDualChannelReservation
          ? {
              status: peroxideDualChannelReservation.status,
              target: peroxideDualChannelReservation.reservedTarget,
              predeclarationHash: peroxideDualChannelReservation.predeclaration.hash,
              nextGate: peroxideDualChannelReservation.nextGate,
              sourceLock: peroxideDimethylSourceLock
                ? {
                    sourceStatus: peroxideDimethylSourceLock.sourceLockDecision.sourceStatus,
                    scoringStatus: peroxideDimethylSourceLock.sourceLockDecision.scoringStatus,
                    evidenceEligibility: peroxideDimethylSourceLock.sourceLockDecision.evidenceEligibility,
                    reason: peroxideDimethylSourceLock.sourceLockDecision.reason,
                  }
                : null,
            }
          : null,
      }
  : null;
const peroxideObservableRouteGuidance = peroxideObservableRouteDiagnostic
  ? {
      status: peroxideObservableRouteDiagnostic.status,
      predeclarationHash: peroxideObservableRouteDiagnostic.predeclarationHash,
      cases: peroxideObservableRouteDiagnostic.cases,
      evidenceStatus: peroxideObservableRouteDiagnostic.evidenceStatus,
      decision: peroxideObservableRouteDiagnostic.decision,
      liveEnergyRelease: peroxideObservableRouteDiagnostic.liveEnergyRelease,
      reservation: peroxideObservableRouteReservation
        ? {
            target: peroxideObservableRouteReservation.reservedTarget,
            predeclarationHash: peroxideObservableRouteReservation.predeclaration.hash,
          }
        : null,
      sourceLock: peroxideDiethylSourceLock
        ? {
            status: peroxideDiethylSourceLock.sourceLockDecision.status,
            equilibriumTorsion:
              peroxideDiethylSourceLock.equilibriumExtraction.derivedCOOCDihedralDegrees,
            scoringAllowed: peroxideDiethylSourceLock.sourceLockDecision.scoringAllowed,
            reason: peroxideDiethylSourceLock.sourceLockDecision.reason,
            userDownloadNeededNow:
              peroxideDiethylSourceLock.possibleRecovery.userDownloadNeededNow,
          }
        : null,
      tbhp: peroxideTbhpReservation
        ? {
            reservationHash: peroxideTbhpReservation.predeclaration.hash,
            scoreStatus: peroxideTbhpScore?.status ?? 'not yet scored',
            evidenceStatus: peroxideTbhpScore?.evidenceStatus ?? 'n/a',
            confidenceAction: peroxideTbhpScore?.confidenceAction ?? 'n/a',
            equilibriumDegrees: peroxideTbhpScore?.sourceComparators?.equilibriumDegrees ?? null,
            transDegrees: peroxideTbhpScore?.sourceComparators?.transDegrees ?? null,
            transSelection: peroxideTbhpScore?.predictions?.transSelection ?? null,
          }
        : null,
      peroxyformic: peroxidePeroxyformicReservation
        ? {
            reservationHash: peroxidePeroxyformicReservation.predeclaration.hash,
            scoreStatus: peroxidePeroxyformicScore?.status ?? 'not yet scored',
            orderingMatches:
              peroxidePeroxyformicScore?.metrics?.orderingMatches ?? null,
            spearman: peroxidePeroxyformicScore?.metrics?.spearman ?? null,
            normalizationValid:
              peroxidePeroxyformicScore?.metrics?.normalizationValid ?? null,
            diagnosis: peroxidePeroxyformicScore?.diagnosis ?? null,
            decision: peroxidePeroxyformicScore?.decision ?? null,
          }
        : null,
      relativeCrowding: peroxideRelativeCrowding
        ? {
            status: peroxideRelativeCrowding.status,
            predeclarationHash: peroxideRelativeCrowding.predeclarationHash,
            evidenceStatus: peroxideRelativeCrowding.evidenceStatus,
            checks: peroxideRelativeCrowding.checks,
            peroxyformicSpearman:
              peroxideRelativeCrowding.cases.peroxyformic.spearman,
            peroxyformicMae:
              peroxideRelativeCrowding.cases.peroxyformic.normalizedMae,
            h2o2RatioFactor:
              peroxideRelativeCrowding.cases.h2o2.ratioFactor,
            decision: peroxideRelativeCrowding.decision,
          }
        : null,
      v2Reservation: peroxideV2Reservation
        ? {
            target: peroxideV2Reservation.reservedTarget,
            predeclarationHash: peroxideV2Reservation.predeclaration.hash,
            sourceLockStatus:
              peroxideHmhpSourceLock?.sourceLockDecision?.status ??
              'not yet run',
            scoringAllowed:
              peroxideHmhpSourceLock?.sourceLockDecision?.scoringAllowed ??
              null,
            reason:
              peroxideHmhpSourceLock?.sourceLockDecision?.reason ?? null,
            recovery:
              peroxideHmhpSourceLock?.sourceLockDecision?.recovery ?? null,
          }
        : null,
      methylChloroperoxide: peroxideMethylChloroReservation
        ? {
            target: peroxideMethylChloroReservation.target,
            predeclarationHash:
              peroxideMethylChloroReservation.predeclaration.hash,
            sourceLockStatus:
              peroxideMethylChloroSourceLock?.sourceLockDecision?.status ??
              'not yet run',
            scoringAllowed:
              peroxideMethylChloroSourceLock?.sourceLockDecision
                ?.scoringAllowed ?? null,
            reason:
              peroxideMethylChloroSourceLock?.sourceLockDecision?.reason ??
              null,
            recovery:
              peroxideMethylChloroSourceLock?.sourceLockDecision?.recovery ??
              null,
          }
        : null,
    }
  : null;

const json = {
  source: 'model-frontier-report.mjs',
  status: 'frontier report over current topology sandbox diagnostics',
  nextTarget,
  weakestPenalty,
  weakestResidual,
  peroxideReleaseGuidance,
  peroxideCh3oohGuidance,
  peroxideNextEvidenceGate,
  peroxideEvidencePolicyGuidance,
  peroxidePromotionGuidance,
  peroxideDualChannelGuidance,
  peroxideObservableRouteGuidance,
  neutralHydrazineGuidance: neutralHydrazineReservation
    ? {
        predeclarationHash: neutralHydrazineReservation.predeclaration.hash,
        sourceLockStatus:
          neutralHydrazineSourceLock?.sourceLockDecision?.status ??
          'not yet run',
        scoringAllowed:
          neutralHydrazineSourceLock?.sourceLockDecision?.scoringAllowed ??
          null,
        reason:
          neutralHydrazineSourceLock?.sourceLockDecision?.reason ?? null,
        recovery:
          neutralHydrazineSourceLock?.sourceLockDecision?.recovery ?? null,
      }
    : null,
  roughnessBrdfGuidance: roughnessBrdfPredeclaration
    ? {
        modelFormHash: roughnessBrdfPredeclaration.predeclaration.hash,
        reservationHash:
          roughnessTungstenReservation?.predeclaration?.hash ?? null,
        sourceLockStatus:
          roughnessTungstenSourceLock?.sourceLockDecision?.status ??
          'not yet run',
        scoringAllowed:
          roughnessTungstenSourceLock?.sourceLockDecision?.scoringAllowed ??
          null,
        reason:
          roughnessTungstenSourceLock?.sourceLockDecision?.reason ?? null,
        recovery:
          roughnessTungstenSourceLock?.sourceLockDecision?.recovery ?? null,
        replacementScreenStatus:
          roughnessSourceAvailability?.status ?? 'not yet run',
        replacementSource:
          roughnessSourceAvailability?.selected?.source ?? null,
        replacementReservationHash:
          roughnessTayabalyReservation?.predeclaration?.hash ?? null,
        replacementReservationStatus:
          roughnessTayabalyReservation?.status ?? 'not yet run',
        replacementSourceLockStatus:
          roughnessTayabalySourceLock?.sourceLockDecision?.status ??
          'not yet run',
        replacementSourceLockReason:
          roughnessTayabalySourceLock?.sourceLockDecision?.reason ?? null,
        replacementLockedTarget:
          roughnessTayabalySourceLock?.lockedTarget ?? null,
        psdCrossModelFormHash:
          roughnessPsdCrossPredeclaration?.predeclaration?.hash ?? null,
        psdCrossModelFormStatus:
          roughnessPsdCrossPredeclaration?.status ?? 'not yet run',
        scorerStatus: roughnessBrdfFeasibility?.status ?? 'not yet run',
        scorerEvidenceStatus:
          roughnessBrdfFeasibility?.evidenceStatus ?? null,
        sourceDataTemplate:
          'analysis/roughness-tungsten-source-data.example.json',
      }
    : null,
  localToleranceFrontiers,
  rankedPenaltyFrontiers,
  rankedResidualFrontiers,
};

await writeFile(new URL('model-frontier-report.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate Sandbox Frontier Report

## Scope

This report ranks the current sandbox pressure points across molecule controls, focused torsion diagnostics, material/interface diagnostics, and T1 residual reports.

It does not add a new model. It prevents the next step from being chosen by habit when an existing weak separation or residual already points to a better target.

## Next Target

${nextTarget}.

## Weakest Decoy / Challenger Separations

| Rank | Source | Label | Challenger | Metric | Value | Band |
|---:|---|---|---|---|---:|---|
${rankedPenaltyFrontiers
  .slice(0, 14)
  .map(
    (item, index) =>
      `| ${index + 1} | ${item.source} | ${item.label} | ${item.challenger} | ${item.metric} | ${item.value} | ${item.band} |`
  )
  .join('\n')}

## Local Tolerance Context

| Source | Label | Context | Metric | Value | Band |
|---|---|---|---|---:|---|
${localToleranceFrontiers
  .map((item) => `| ${item.source} | ${item.label} | ${item.challenger} | ${item.metric} | ${round(item.value)} | ${item.band} |`)
  .join('\n')}

${
  peroxideReleaseGuidance
    ? `## Peroxide Release Diagnostic Guidance

The peroxide nonlocal frontier is currently limited by the anti-planar release term, not by molecule-family weights.

| Setting | Strength | Onset | Span | Near weakest | Shoulder weakest | Nonlocal weakest | Weakest nonlocal angle | Trans penalty |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| current | ${peroxideReleaseGuidance.current.release.strength} | ${peroxideReleaseGuidance.current.release.onset} | ${peroxideReleaseGuidance.current.release.span} | ${peroxideReleaseGuidance.current.nearWeakest} | ${peroxideReleaseGuidance.current.shoulderWeakest} | ${peroxideReleaseGuidance.current.nonlocalWeakest} | ${peroxideReleaseGuidance.current.nonlocalWeakestAngle} | ${peroxideReleaseGuidance.current.transPenalty} |
| best diagnostic | ${peroxideReleaseGuidance.bestDiagnostic.release.strength} | ${peroxideReleaseGuidance.bestDiagnostic.release.onset} | ${peroxideReleaseGuidance.bestDiagnostic.release.span} | ${peroxideReleaseGuidance.bestDiagnostic.nearWeakest} | ${peroxideReleaseGuidance.bestDiagnostic.shoulderWeakest} | ${peroxideReleaseGuidance.bestDiagnostic.nonlocalWeakest} | ${peroxideReleaseGuidance.bestDiagnostic.nonlocalWeakestAngle} | ${peroxideReleaseGuidance.bestDiagnostic.transPenalty} |
| least-disruptive nonzero | ${peroxideReleaseGuidance.leastDisruptiveNonzero.release.strength} | ${peroxideReleaseGuidance.leastDisruptiveNonzero.release.onset} | ${peroxideReleaseGuidance.leastDisruptiveNonzero.release.span} | ${peroxideReleaseGuidance.leastDisruptiveNonzero.nearWeakest} | ${peroxideReleaseGuidance.leastDisruptiveNonzero.shoulderWeakest} | ${peroxideReleaseGuidance.leastDisruptiveNonzero.nonlocalWeakest} | ${peroxideReleaseGuidance.leastDisruptiveNonzero.nonlocalWeakestAngle} | ${peroxideReleaseGuidance.leastDisruptiveNonzero.transPenalty} |

Reading: ${peroxideReleaseGuidance.directionReading}. This is diagnostic guidance only; any repair must be predeclared against a fresh held-out rotor target before it can count.
`
    : ''
}

${
  peroxideCh3oohGuidance
    ? `## Peroxide CH3OOH Diagnostic Status

The reserved methyl hydroperoxide target now has a source extraction and a diagnostic scoring consumer. This confirms compatibility with the extracted source ordering, but it is not evidence-counting because the CH3OOH coordinate-consumption rule was introduced after source extraction.

| Field | Value |
|---|---|
| status | ${peroxideCh3oohGuidance.status} |
| frozen release | strength=${peroxideCh3oohGuidance.frozenRepair.releaseStrength}; onset=${peroxideCh3oohGuidance.frozenRepair.releaseOnsetDegrees}; span=${peroxideCh3oohGuidance.frozenRepair.releaseSpanDegrees} |
| source trans OH barrier | ${peroxideCh3oohGuidance.sourceComparators.transBarrierCm1} cm-1 |
| source cis OH barrier | ${peroxideCh3oohGuidance.sourceComparators.cisBarrierCm1} cm-1 |
| source trans/cis ratio | ${peroxideCh3oohGuidance.sourceComparators.sourceBarrierRatio} |
| predicted trans/cis penalty ratio | ${peroxideCh3oohGuidance.diagnosticChecks.predictedPenaltyRatio} |
| qualitative ordering | ${peroxideCh3oohGuidance.diagnosticChecks.qualitativeOrderingPass ? 'pass' : 'fail'} |
| evidence status | ${peroxideCh3oohGuidance.evidenceStatus} |

Reading: ${peroxideCh3oohGuidance.reading}. Next gate: ${peroxideCh3oohGuidance.nextGate}.
`
    : ''
}

${
  peroxideNextEvidenceGate
    ? `## Peroxide Next Evidence Gate

A future evidence-counting substituted-peroxide gate was predeclared before lookup. The ethyl hydroperoxide target now has source extraction and a computed-comparator scoring pass, but it is not experimental validation and should not raise global confidence automatically.

| Field | Value |
|---|---|
| target | ${peroxideNextEvidenceGate.target.target} (${peroxideNextEvidenceGate.target.formula}) |
| predeclaration hash | ${peroxideNextEvidenceGate.predeclarationHash} |
| frozen rule | ${peroxideNextEvidenceGate.frozenRule.name} |
| frozen release | strength=${peroxideNextEvidenceGate.frozenRule.releaseStrength}; onset=${peroxideNextEvidenceGate.frozenRule.releaseOnsetDegrees}; span=${peroxideNextEvidenceGate.frozenRule.releaseSpanDegrees} |
| pass/fail | ${peroxideNextEvidenceGate.frozenRule.passFail} |
| source-lock status | ${peroxideNextEvidenceGate.sourceLockStatus} |
| primary source candidate | ${peroxideNextEvidenceGate.primaryCandidate ?? 'n/a'} |
| block | ${peroxideNextEvidenceGate.sourceLockReason ?? 'n/a'} |
| non-locking source hint | ${
        peroxideNextEvidenceGate.hint
          ? `${peroxideNextEvidenceGate.hint.status}; old hinted trans/cis ratio ${peroxideNextEvidenceGate.hint.ratio}; ${peroxideNextEvidenceGate.hint.evidenceStatus}`
          : 'n/a'
      } |
| computed-comparator score | ${
        peroxideNextEvidenceGate.score
          ? `${peroxideNextEvidenceGate.score.status}; source ratio ${peroxideNextEvidenceGate.score.sourceRatio}; predicted ratio ${peroxideNextEvidenceGate.score.predictedRatio}; ${peroxideNextEvidenceGate.score.evidenceStatus}`
          : 'n/a'
      } |
| score reading | ${peroxideNextEvidenceGate.score ? peroxideNextEvidenceGate.score.reading : 'n/a'} |
| confidence effect | ${peroxideNextEvidenceGate.score ? peroxideNextEvidenceGate.score.confidenceEffect : 'n/a'} |
`
    : ''
}

${
  peroxideEvidencePolicyGuidance
    ? `## Peroxide Evidence Accounting

The peroxide evidence policy ledger classifies the ethyl result as branch-level computed-comparator support only.

| Field | Value |
|---|---|
| global confidence action | ${peroxideEvidencePolicyGuidance.globalConfidenceAction} |
| branch confidence action | ${peroxideEvidencePolicyGuidance.branchConfidenceAction} |
| computed-comparator held-out passes | ${peroxideEvidencePolicyGuidance.computedComparatorPasses} |
| observable-route held-out passes | ${peroxideEvidencePolicyGuidance.observableRoutePasses} |
| intermediate-profile held-out fails | ${peroxideEvidencePolicyGuidance.intermediateProfileFails} |
| review decision | ${peroxideEvidencePolicyGuidance.reviewDecision?.status ?? 'n/a'} |
| promotion | ${peroxideEvidencePolicyGuidance.reviewDecision?.promoted ? 'yes' : 'no'} |
| next gate | ${peroxideEvidencePolicyGuidance.reviewDecision?.nextGate ?? 'n/a'} |
| exposed redesign | ${peroxideEvidencePolicyGuidance.exposedRedesign?.status ?? 'n/a'} |
| warnings | ${peroxideEvidencePolicyGuidance.warnings.join('; ')} |
`
    : ''
}

${
  peroxidePromotionGuidance
    ? `## Peroxide Release Promotion Review

The frozen candidate is not promoted because it creates a cross-benchmark regression.

| Field | Value |
|---|---|
| status | ${peroxidePromotionGuidance.status} |
| decision | ${peroxidePromotionGuidance.decision} |
| current live release | strength=${peroxidePromotionGuidance.currentLiveRelease.strength}; onset=${peroxidePromotionGuidance.currentLiveRelease.onset}; span=${peroxidePromotionGuidance.currentLiveRelease.span} |
| candidate release | strength=${peroxidePromotionGuidance.candidateRelease.strength}; onset=${peroxidePromotionGuidance.candidateRelease.onset}; span=${peroxidePromotionGuidance.candidateRelease.span} |
| candidate H2O2 trans barrier | ${peroxidePromotionGuidance.candidateMetrics.h2o2TransCm1} cm-1 |
| candidate H2O2 trans error | ${peroxidePromotionGuidance.candidateMetrics.transErrorPct}% |
| candidate H2O2 cis/trans ratio error | ${peroxidePromotionGuidance.candidateMetrics.ratioErrorPct}% |
| failed checks | ${peroxidePromotionGuidance.failedChecks.join('; ')} |
| next requirement | ${peroxidePromotionGuidance.nextModelRequirement} |
`
    : ''
}

${
  peroxideDualChannelGuidance
    ? `## Peroxide Dual-Channel Model Form

The exposed feasibility diagnostic separates structural route selection from
absolute barrier energy. The selection channel improves nonlocal clearance
without changing the live energy channel.

| Field | Value |
|---|---|
| status | ${peroxideDualChannelGuidance.status} |
| predeclaration hash | ${peroxideDualChannelGuidance.predeclarationHash} |
| live energy release | strength=${peroxideDualChannelGuidance.energy.release.strength}; onset=${peroxideDualChannelGuidance.energy.release.onset}; span=${peroxideDualChannelGuidance.energy.release.span} |
| energy trans barrier | ${peroxideDualChannelGuidance.energy.transBarrierCm1} cm-1 |
| energy cis barrier | ${peroxideDualChannelGuidance.energy.cisBarrierCm1} cm-1 |
| selection nonlocal weakest | ${peroxideDualChannelGuidance.selection.nonlocalWeakest} at ${peroxideDualChannelGuidance.selection.nonlocalWeakestAngle} degrees |
| selection near-reference weakest | ${peroxideDualChannelGuidance.selection.nearWeakest} |
| new fitted coefficients | ${peroxideDualChannelGuidance.selection.newCoefficients} |
| evidence status | ${peroxideDualChannelGuidance.evidenceStatus} |
| reserved fresh target | ${peroxideDualChannelGuidance.reservation ? `${peroxideDualChannelGuidance.reservation.target.target} (${peroxideDualChannelGuidance.reservation.target.formula})` : 'not yet reserved'} |
| target predeclaration hash | ${peroxideDualChannelGuidance.reservation?.predeclarationHash ?? 'n/a'} |
| source status | ${peroxideDualChannelGuidance.reservation?.sourceLock?.sourceStatus ?? 'not yet run'} |
| scoring status | ${peroxideDualChannelGuidance.reservation?.sourceLock?.scoringStatus ?? 'not yet run'} |
| evidence eligibility | ${peroxideDualChannelGuidance.reservation?.sourceLock?.evidenceEligibility ?? 'n/a'} |
| next gate | ${peroxideDualChannelGuidance.reservation?.sourceLock ? 'redesign selection descriptor around source-observable torsion inputs before another target reservation' : (peroxideDualChannelGuidance.reservation?.nextGate ?? peroxideDualChannelGuidance.nextGate)} |

Decision: ${peroxideDualChannelGuidance.decision}.
`
    : ''
}

${
  peroxideObservableRouteGuidance
    ? `## Peroxide Observable-Route Redesign

The post-failure redesign consumes only source-defined torsion coordinates and
their construct labels. It removes the unfrozen charge, steric, and terminal
group coordinate dependencies.

| Field | Value |
|---|---|
| status | ${peroxideObservableRouteGuidance.status} |
| predeclaration hash | ${peroxideObservableRouteGuidance.predeclarationHash} |
| new fitted coefficients | 0 |
| live energy release | strength=${peroxideObservableRouteGuidance.liveEnergyRelease.strength}; onset=${peroxideObservableRouteGuidance.liveEnergyRelease.onset}; span=${peroxideObservableRouteGuidance.liveEnergyRelease.span} |
| evidence status | ${peroxideObservableRouteGuidance.evidenceStatus} |
| reserved target | ${peroxideObservableRouteGuidance.reservation ? `${peroxideObservableRouteGuidance.reservation.target.target} (${peroxideObservableRouteGuidance.reservation.target.formula})` : 'not yet reserved'} |
| target predeclaration hash | ${peroxideObservableRouteGuidance.reservation?.predeclarationHash ?? 'n/a'} |
| source-lock status | ${peroxideObservableRouteGuidance.sourceLock?.status ?? 'not yet run'} |
| locked equilibrium torsion | ${peroxideObservableRouteGuidance.sourceLock ? `${peroxideObservableRouteGuidance.sourceLock.equilibriumTorsion} degrees` : 'n/a'} |
| scoring allowed | ${peroxideObservableRouteGuidance.sourceLock ? (peroxideObservableRouteGuidance.sourceLock.scoringAllowed ? 'yes' : 'no') : 'n/a'} |
| user download needed now | ${peroxideObservableRouteGuidance.sourceLock ? (peroxideObservableRouteGuidance.sourceLock.userDownloadNeededNow ? 'yes' : 'no') : 'n/a'} |
| TBHP reservation hash | ${peroxideObservableRouteGuidance.tbhp?.reservationHash ?? 'n/a'} |
| TBHP score status | ${peroxideObservableRouteGuidance.tbhp?.scoreStatus ?? 'n/a'} |
| TBHP source route | ${peroxideObservableRouteGuidance.tbhp?.equilibriumDegrees ?? 'n/a'} to ${peroxideObservableRouteGuidance.tbhp?.transDegrees ?? 'n/a'} degrees |
| TBHP trans selection distance | ${peroxideObservableRouteGuidance.tbhp?.transSelection ?? 'n/a'} |
| next gate | ${peroxideObservableRouteGuidance.tbhp?.scoreStatus === 'heldout-observable-route-comparator-pass' ? 'review TBHP in the peroxide evidence ledger before promotion' : (peroxideObservableRouteGuidance.sourceLock ? 'predeclare a source-availability screen before another target reservation' : 'reserve a new target before source lookup')} |

Decision: ${peroxideObservableRouteGuidance.decision}.

## Peroxyformic-Acid Intermediate Profile

The first non-saturated three-coordinate held-out profile fails the frozen
combined route/energy model.

| Field | Value |
|---|---|
| reservation hash | ${peroxideObservableRouteGuidance.peroxyformic?.reservationHash ?? 'n/a'} |
| score status | ${peroxideObservableRouteGuidance.peroxyformic?.scoreStatus ?? 'n/a'} |
| source/predicted ordering match | ${peroxideObservableRouteGuidance.peroxyformic?.orderingMatches ?? 'n/a'} |
| Spearman rank correlation | ${peroxideObservableRouteGuidance.peroxyformic?.spearman ?? 'n/a'} |
| normalized-rise scoring valid | ${peroxideObservableRouteGuidance.peroxyformic?.normalizationValid ?? 'n/a'} |
| diagnosis | ${peroxideObservableRouteGuidance.peroxyformic?.diagnosis ?? 'n/a'} |
| decision | ${peroxideObservableRouteGuidance.peroxyformic?.decision ?? 'n/a'} |

## Equilibrium-Relative Crowding Redesign

The redesign is predeclared under hash
\`${peroxideObservableRouteGuidance.relativeCrowding?.predeclarationHash ?? 'n/a'}\`
and evaluated only on exposed pressure cases.

| Field | Value |
|---|---|
| status | ${peroxideObservableRouteGuidance.relativeCrowding?.status ?? 'n/a'} |
| H2O2 ratio factor | ${peroxideObservableRouteGuidance.relativeCrowding?.h2o2RatioFactor ?? 'n/a'} |
| peroxyformic Spearman | ${peroxideObservableRouteGuidance.relativeCrowding?.peroxyformicSpearman ?? 'n/a'} |
| peroxyformic normalized-rise MAE | ${peroxideObservableRouteGuidance.relativeCrowding?.peroxyformicMae ?? 'n/a'} |
| evidence status | ${peroxideObservableRouteGuidance.relativeCrowding?.evidenceStatus ?? 'n/a'} |
| decision | ${peroxideObservableRouteGuidance.relativeCrowding?.decision ?? 'n/a'} |

## Fresh v2 Target Source Lock

| Field | Value |
|---|---|
| target | ${peroxideObservableRouteGuidance.v2Reservation?.target?.target ?? 'n/a'} |
| predeclaration hash | ${peroxideObservableRouteGuidance.v2Reservation?.predeclarationHash ?? 'n/a'} |
| source-lock status | ${peroxideObservableRouteGuidance.v2Reservation?.sourceLockStatus ?? 'n/a'} |
| scoring allowed | ${peroxideObservableRouteGuidance.v2Reservation?.scoringAllowed === null ? 'n/a' : peroxideObservableRouteGuidance.v2Reservation?.scoringAllowed ? 'yes' : 'no'} |
| reason | ${peroxideObservableRouteGuidance.v2Reservation?.reason ?? 'n/a'} |
| recovery | ${peroxideObservableRouteGuidance.v2Reservation?.recovery ?? 'n/a'} |

## Adjacent-Family Source Lock

| Field | Value |
|---|---|
| target | ${peroxideObservableRouteGuidance.methylChloroperoxide?.target?.target ?? 'n/a'} |
| predeclaration hash | ${peroxideObservableRouteGuidance.methylChloroperoxide?.predeclarationHash ?? 'n/a'} |
| source-lock status | ${peroxideObservableRouteGuidance.methylChloroperoxide?.sourceLockStatus ?? 'n/a'} |
| scoring allowed | ${peroxideObservableRouteGuidance.methylChloroperoxide?.scoringAllowed === null ? 'n/a' : peroxideObservableRouteGuidance.methylChloroperoxide?.scoringAllowed ? 'yes' : 'no'} |
| reason | ${peroxideObservableRouteGuidance.methylChloroperoxide?.reason ?? 'n/a'} |
| recovery | ${peroxideObservableRouteGuidance.methylChloroperoxide?.recovery ?? 'n/a'} |
`
    : ''
}

## Weakest T1 Residuals

| Rank | Source | Label | Comparator | Metric | Value | Magnitude | Band |
|---:|---|---|---|---|---:|---:|---|
${rankedResidualFrontiers
  .slice(0, 12)
  .map(
    (item, index) =>
      `| ${index + 1} | ${item.source} | ${item.label} | ${item.challenger} | ${item.metric} | ${item.value} | ${item.magnitude} | ${item.band} |`
  )
  .join('\n')}

## Neutral Hydrazine Absolute-Transfer Gate

| Field | Value |
|---|---|
| predeclaration hash | ${json.neutralHydrazineGuidance?.predeclarationHash ?? 'n/a'} |
| source-lock status | ${json.neutralHydrazineGuidance?.sourceLockStatus ?? 'n/a'} |
| scoring allowed | ${json.neutralHydrazineGuidance?.scoringAllowed === null ? 'n/a' : json.neutralHydrazineGuidance?.scoringAllowed ? 'yes' : 'no'} |
| reason | ${json.neutralHydrazineGuidance?.reason ?? 'n/a'} |
| recovery | ${json.neutralHydrazineGuidance?.recovery ?? 'n/a'} |

## Roughness PSD/BRDF Gate

| Field | Value |
|---|---|
| model-form hash | ${json.roughnessBrdfGuidance?.modelFormHash ?? 'n/a'} |
| target reservation hash | ${json.roughnessBrdfGuidance?.reservationHash ?? 'n/a'} |
| source-lock status | ${json.roughnessBrdfGuidance?.sourceLockStatus ?? 'n/a'} |
| scoring allowed | ${json.roughnessBrdfGuidance?.scoringAllowed === null ? 'n/a' : json.roughnessBrdfGuidance?.scoringAllowed ? 'yes' : 'no'} |
| reason | ${json.roughnessBrdfGuidance?.reason ?? 'n/a'} |
| recovery | ${json.roughnessBrdfGuidance?.recovery ?? 'n/a'} |
| replacement screen | ${json.roughnessBrdfGuidance?.replacementScreenStatus ?? 'n/a'} |
| replacement source | ${json.roughnessBrdfGuidance?.replacementSource ?? 'n/a'} |
| replacement reservation hash | ${json.roughnessBrdfGuidance?.replacementReservationHash ?? 'n/a'} |
| replacement reservation status | ${json.roughnessBrdfGuidance?.replacementReservationStatus ?? 'n/a'} |
| replacement source-lock status | ${json.roughnessBrdfGuidance?.replacementSourceLockStatus ?? 'n/a'} |
| replacement source-lock reason | ${json.roughnessBrdfGuidance?.replacementSourceLockReason ?? 'n/a'} |
| PSD cross-measurement model hash | ${json.roughnessBrdfGuidance?.psdCrossModelFormHash ?? 'n/a'} |
| PSD cross-measurement model status | ${json.roughnessBrdfGuidance?.psdCrossModelFormStatus ?? 'n/a'} |
| scorer status | ${json.roughnessBrdfGuidance?.scorerStatus ?? 'n/a'} |
| scorer evidence status | ${json.roughnessBrdfGuidance?.scorerEvidenceStatus ?? 'n/a'} |
| source-data template | ${json.roughnessBrdfGuidance?.sourceDataTemplate ?? 'n/a'} |

## Reading

Weak decoy penalties mean a diagnostic can still rank the reference first while failing to create enough clearance against a plausible wrong arrangement. Local tolerance rows are reported for context but should not be treated as hard decoy failures. High residuals mean the T1 target formula or admissible grid still does not match a T2-derived envelope cleanly.
`;

await writeFile(new URL('model-frontier-report.md', outDir), markdown);

console.log(`Next target: ${nextTarget}`);
console.log(`Wrote ${new URL('model-frontier-report.md', outDir).pathname}`);
