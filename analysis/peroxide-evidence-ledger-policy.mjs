import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

async function readOptionalJson(name) {
  try {
    return JSON.parse(await readFile(new URL(name, outDir), 'utf8'));
  } catch {
    return null;
  }
}

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

function policyFor(record) {
  if (!record) {
    return {
      ledgerClass: 'missing-artifact',
      confidenceAction: 'none',
      branchAction: 'none',
      reason: 'required artifact is missing; regenerate reports before accounting',
    };
  }

  if (record.kind === 'repair-predeclaration') {
    return {
      ledgerClass: 'parameter-freeze',
      confidenceAction: 'none',
      branchAction: 'defines frozen peroxide repair candidate',
      reason: 'freezes release parameters before later target scoring; not a scored target',
    };
  }

  if (record.kind === 'post-extraction-diagnostic') {
    return {
      ledgerClass: 'diagnostic-compatible',
      confidenceAction: 'none',
      branchAction: 'supports plausibility only',
      reason: 'the coordinate-consumption rule was introduced after this source extraction, so it cannot count as held-out evidence',
    };
  }

  if (record.kind === 'predeclared-computed-comparator') {
    return {
      ledgerClass: record.status === 'computed-comparator-pass' ? 'computed-comparator-heldout-pass' : 'computed-comparator-heldout-fail',
      confidenceAction: 'do not change global confidence automatically',
      branchAction:
        record.status === 'computed-comparator-pass'
          ? 'may support the peroxide repair branch after explicit ledger review'
          : 'should weaken or block the peroxide repair branch until retested under a new predeclared rule',
      reason:
        'target, rule, release parameters, and pass/fail threshold were predeclared, but the comparator is computed rather than experimental',
    };
  }

  if (record.kind === 'predeclared-observable-route-comparator') {
    const passed = record.status === 'heldout-observable-route-comparator-pass';
    return {
      ledgerClass: passed
        ? 'observable-route-heldout-pass'
        : 'observable-route-heldout-fail',
      confidenceAction: 'do not change global confidence automatically',
      branchAction: passed
        ? 'supports the observable-route selection branch, but does not promote the energy model or establish quantitative barrier accuracy'
        : 'blocks promotion of the observable-route selection branch pending a new predeclared model or target',
      reason:
        'the target and route mapping were reserved before numerical extraction, and experiment supports the torsional construct, but the scored barriers are computed and the clamped trans-route check is qualitative rather than a quantitative barrier prediction',
    };
  }

  if (record.kind === 'predeclared-intermediate-profile') {
    const passed = record.status === 'heldout-intermediate-profile-pass';
    return {
      ledgerClass: passed
        ? 'intermediate-profile-heldout-pass'
        : 'intermediate-profile-heldout-fail',
      confidenceAction: passed
        ? 'do not change global confidence automatically'
        : 'record a held-out model-form failure; do not increase global confidence',
      branchAction: passed
        ? 'supports quantitative transfer of the observable-route plus energy branch'
        : 'blocks promotion of the current observable-route plus released-energy model form',
      reason:
        'the target identity, three-coordinate source requirements, normalization, and quantitative thresholds were frozen before numerical extraction',
    };
  }

  if (record.kind === 'superseded-search-hint') {
    return {
      ledgerClass: 'not-evidence',
      confidenceAction: 'none',
      branchAction: 'none',
      reason: 'search-index preview values were superseded by full source extraction and are not the target row',
    };
  }

  return {
    ledgerClass: 'unclassified',
    confidenceAction: 'none',
    branchAction: 'manual review required',
    reason: 'artifact did not match a known peroxide evidence accounting class',
  };
}

const release = await readOptionalJson('peroxide-release-repair-predeclaration.json');
const methyl = await readOptionalJson('peroxide-methyl-hydroperoxide-scoring-diagnostic.json');
const ethylHint = await readOptionalJson('peroxide-ethyl-hydroperoxide-search-hint-diagnostic.json');
const ethyl = await readOptionalJson('peroxide-ethyl-hydroperoxide-evidence-scoring.json');
const tbhp = await readOptionalJson('peroxide-tbhp-observable-route-scoring.json');
const peroxyformic = await readOptionalJson('peroxide-peroxyformic-profile-scoring.json');
const relativeCrowding = await readOptionalJson(
  'peroxide-equilibrium-relative-crowding-diagnostic.json',
);

function releaseParams(rule) {
  return rule
    ? `strength=${rule.releaseStrength}; onset=${rule.releaseOnsetDegrees}; span=${rule.releaseSpanDegrees}`
    : 'missing';
}

const records = [
  {
    id: 'peroxide-release-repair',
    target: 'H2O2/nonlocal peroxide repair',
    kind: 'repair-predeclaration',
    status: release?.status ?? 'missing',
    parameters: releaseParams(release?.frozenCandidate),
    sourceArtifact: 'analysis/out/peroxide-release-repair-predeclaration.json',
  },
  {
    id: 'methyl-hydroperoxide-diagnostic',
    target: 'methyl hydroperoxide (CH3OOH)',
    kind: 'post-extraction-diagnostic',
    status: methyl?.decision?.status ?? 'missing',
    parameters: releaseParams(methyl?.frozenRepair),
    sourceArtifact: 'analysis/out/peroxide-methyl-hydroperoxide-scoring-diagnostic.json',
  },
  {
    id: 'ethyl-hydroperoxide-search-hint',
    target: 'ethyl hydroperoxide search-index preview',
    kind: 'superseded-search-hint',
    status: ethylHint?.decision?.status ?? 'missing',
    parameters: 'n/a',
    sourceArtifact: 'analysis/out/peroxide-ethyl-hydroperoxide-search-hint-diagnostic.json',
  },
  {
    id: 'ethyl-hydroperoxide-computed-comparator',
    target: 'ethyl hydroperoxide (C2H5OOH; HOOEt)',
    kind: 'predeclared-computed-comparator',
    status: ethyl?.decision?.status ?? 'missing',
    parameters: releaseParams(ethyl?.frozenRule),
    sourceArtifact: 'analysis/out/peroxide-ethyl-hydroperoxide-evidence-scoring.json',
    sourceRatio: ethyl?.sourceComparators?.sourceBarrierRatio ?? null,
    predictedRatio: ethyl?.checks?.predictedPenaltyRatio ?? null,
  },
  {
    id: 'tbhp-observable-route-comparator',
    target: 'tert-butyl hydroperoxide ((CH3)3COOH; TBHP)',
    kind: 'predeclared-observable-route-comparator',
    status: tbhp?.status ?? 'missing',
    parameters: tbhp
      ? `selection tolerance=${tbhp.frozenParameters.selectionToleranceDegrees} degrees; ${releaseParams(tbhp.frozenParameters)}`
      : 'missing',
    sourceArtifact: 'analysis/out/peroxide-tbhp-observable-route-scoring.json',
    sourceRatio: tbhp
      ? `${tbhp.sourceComparators.equilibriumDegrees} -> ${tbhp.sourceComparators.transDegrees} degrees`
      : null,
    predictedRatio: tbhp?.predictions?.transSelection ?? null,
  },
  {
    id: 'peroxyformic-intermediate-profile',
    target: 'peroxyformic acid (HC(O)OOH)',
    kind: 'predeclared-intermediate-profile',
    status: peroxyformic?.status ?? 'missing',
    parameters: peroxyformic
      ? `selection tolerance=${peroxyformic.frozenParameters.selectionToleranceDegrees} degrees; ${releaseParams(peroxyformic.frozenParameters)}`
      : 'missing',
    sourceArtifact: 'analysis/out/peroxide-peroxyformic-profile-scoring.json',
    sourceRatio: peroxyformic
      ? peroxyformic.metrics.sourceOrdering.join(' < ')
      : null,
    predictedRatio: peroxyformic
      ? peroxyformic.metrics.predictedOrdering.join(' < ')
      : null,
  },
];

const classifiedRecords = records.map((record) => ({
  ...record,
  policy: policyFor(record.status === 'missing' ? null : record),
}));

const computedPasses = classifiedRecords.filter((record) => record.policy.ledgerClass === 'computed-comparator-heldout-pass');
const observableRoutePasses = classifiedRecords.filter(
  (record) => record.policy.ledgerClass === 'observable-route-heldout-pass',
);
const intermediateProfilePasses = classifiedRecords.filter(
  (record) => record.policy.ledgerClass === 'intermediate-profile-heldout-pass',
);
const intermediateProfileFails = classifiedRecords.filter(
  (record) => record.policy.ledgerClass === 'intermediate-profile-heldout-fail',
);
const diagnostics = classifiedRecords.filter((record) => record.policy.ledgerClass === 'diagnostic-compatible');
const notEvidence = classifiedRecords.filter((record) => record.policy.ledgerClass === 'not-evidence');
const warnings = [];

if (computedPasses.length > 0) {
  warnings.push('Computed-comparator passes are branch evidence candidates only; global confidence remains unchanged until explicit ledger policy promotes them.');
}
if (observableRoutePasses.length > 0) {
  warnings.push('Observable-route passes support qualitative route selection only; they do not validate absolute barrier magnitude or promote the energy model.');
}
if (intermediateProfileFails.length > 0) {
  warnings.push('A predeclared held-out intermediate profile failed; this overrides qualitative route support for model-promotion decisions.');
}
if (diagnostics.length > 0) {
  warnings.push('Post-extraction diagnostics support plausibility but are not held-out evidence.');
}
if (notEvidence.length > 0) {
  warnings.push('Superseded search hints must not be cited as target evidence.');
}

const ledger = {
  source: 'peroxide-evidence-ledger-policy.mjs',
  date: '2026-06-24',
  scope:
    'Policy ledger for peroxide torsion artifacts. Classifies what each result may support; does not change global confidence.',
  globalConfidenceAction: 'no automatic change',
  branchConfidenceAction:
    intermediateProfileFails.length > 0
      ? relativeCrowding?.status ===
        'exposed-equilibrium-relative-crowding-feasibility-pass'
        ? 'original energy form remains blocked; equilibrium-relative crowding redesign clears exposed feasibility and awaits fresh validation'
        : 'current observable-route plus released-energy model form is blocked by a held-out intermediate-profile failure'
      : intermediateProfilePasses.length > 0
        ? 'observable-route plus released-energy branch has quantitative held-out profile support'
        : observableRoutePasses.length > 0
          ? 'observable-route selection branch receives limited held-out support; energy-model promotion remains blocked'
          : computedPasses.length > 0
            ? 'peroxide repair branch has a predeclared computed-comparator pass available for human ledger review'
            : 'peroxide repair branch has no predeclared computed-comparator pass',
  reviewDecision: {
    status:
      intermediateProfileFails.length > 0
        ? relativeCrowding?.status ===
          'exposed-equilibrium-relative-crowding-feasibility-pass'
          ? 'heldout-failure-redesign-feasible-fresh-validation-required'
          : 'heldout-intermediate-profile-fail-model-redesign-required'
        : intermediateProfilePasses.length > 0
          ? 'quantitative-branch-support-no-automatic-global-promotion'
          : observableRoutePasses.length > 0
            ? 'limited-branch-support-no-model-promotion'
            : 'no-observable-route-pass',
    promoted: false,
    rationale:
      intermediateProfileFails.length > 0
        ? relativeCrowding?.status ===
          'exposed-equilibrium-relative-crowding-feasibility-pass'
          ? 'Peroxyformic acid falsified the absolute-angle crowding term. The separately predeclared equilibrium-relative redesign repairs H2O2, TBHP, and peroxyformic exposed pressure cases without fitted coefficients, but that agreement is not validation.'
          : 'Peroxyformic acid supplied the frozen unsaturated intermediate route, but the live absolute-angle cis-crowding term reversed the source energy ordering and made normalized-rise scoring undefined.'
        : intermediateProfilePasses.length > 0
          ? 'A predeclared three-coordinate held-out profile cleared the frozen ordering, rank-correlation, and normalized-error gates.'
          : observableRoutePasses.length > 0
            ? 'TBHP was genuinely held out from numerical extraction and its source-supported trans route clears the frozen qualitative selection gate. The check saturates at the clamped distance of 1 and uses computed effective barriers, so it is not a quantitative prediction of barrier magnitude.'
            : 'No passing held-out observable-route comparator is available.',
    nextGate:
      intermediateProfileFails.length > 0
        ? relativeCrowding?.status ===
          'exposed-equilibrium-relative-crowding-feasibility-pass'
          ? 'reserve one fresh peroxide-family torsional profile under the frozen equilibrium-relative crowding formula and quantitative profile thresholds before numerical source extraction'
          : 'predeclare a redesigned crowding descriptor that is relative to source-defined equilibrium topology, and test it first on exposed H2O2, TBHP, and peroxyformic-acid pressure cases before reserving another target'
        : 'predeclare a fresh peroxide-family target with a non-saturated intermediate route distance and a quantitative energy or barrier criterion before source lookup',
  },
  records: classifiedRecords,
  exposedRedesign: relativeCrowding
    ? {
        status: relativeCrowding.status,
        predeclarationHash: relativeCrowding.predeclarationHash,
        evidenceStatus: relativeCrowding.evidenceStatus,
        decision: relativeCrowding.decision,
      }
    : null,
  warnings,
};

const markdown = `# Peroxide Evidence Ledger Policy

## Scope

This ledger classifies peroxide torsion artifacts by what they are allowed to
support. It does not compute a new confidence score and does not promote
computed-comparator evidence into global theory confidence.

Date: ${ledger.date}

Global confidence action: ${ledger.globalConfidenceAction}

Branch action: ${ledger.branchConfidenceAction}

Review decision: **${ledger.reviewDecision.status}**

Promotion: **${ledger.reviewDecision.promoted ? 'yes' : 'no'}**

Rationale: ${ledger.reviewDecision.rationale}

Next gate: ${ledger.reviewDecision.nextGate}

## Records

${table(
  ['ID', 'Target', 'Status', 'Ledger class', 'Parameters', 'Source ratio', 'Predicted ratio', 'Confidence action', 'Branch action'],
  classifiedRecords.map((record) => [
    record.id,
    record.target,
    record.status,
    record.policy.ledgerClass,
    record.parameters,
    record.sourceRatio ?? '',
    record.predictedRatio ?? '',
    record.policy.confidenceAction,
    record.policy.branchAction,
  ]),
)}

## Reasons

${classifiedRecords.map((record) => `- ${record.id}: ${record.policy.reason}`).join('\n')}

## Warnings

${warnings.map((warning) => `- ${warning}`).join('\n')}
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('peroxide-evidence-ledger-policy.json', outDir), `${JSON.stringify(ledger, null, 2)}\n`);
await writeFile(new URL('peroxide-evidence-ledger-policy.md', outDir), markdown);

console.log('Peroxide evidence ledger policy');
console.log(`Records: ${classifiedRecords.length}`);
console.log(`Computed-comparator passes: ${computedPasses.length}`);
console.log(`Observable-route passes: ${observableRoutePasses.length}`);
console.log(`Intermediate-profile passes: ${intermediateProfilePasses.length}`);
console.log(`Intermediate-profile fails: ${intermediateProfileFails.length}`);
console.log(`Warnings: ${warnings.length}`);
console.log(`Wrote ${new URL('peroxide-evidence-ledger-policy.md', outDir).pathname}`);
