import { mkdir, writeFile } from 'node:fs/promises';
import { clamp01 } from './molecule-model.mjs';

const outDir = new URL('./out/', import.meta.url);

const cases = [
  {
    formula: 'NaCl',
    spacing: 2.82,
    routeBase: 0.68,
    cation: 'Na',
    anion: 'Cl',
  },
  {
    formula: 'LiF',
    spacing: 2.01,
    routeBase: 0.7,
    cation: 'Li',
    anion: 'F',
  },
];

const variants = [
  {
    name: 'alternating cubic lattice',
    type: 'reference',
    scale: 1,
    pattern: 'alternating',
  },
  {
    name: 'compressed alternating lattice',
    type: 'strained',
    scale: 0.76,
    pattern: 'alternating',
  },
  {
    name: 'expanded alternating lattice',
    type: 'strained',
    scale: 1.34,
    pattern: 'alternating',
  },
  {
    name: 'same-charge layers',
    type: 'decoy',
    scale: 1,
    pattern: 'layered',
  },
  {
    name: 'clustered charges',
    type: 'decoy',
    scale: 1,
    pattern: 'clustered',
  },
  {
    name: 'pair-only collapse',
    type: 'decoy',
    scale: 0.38,
    pattern: 'pair-collapse',
  },
];

function vec(x, y, z) {
  return { x, y, z };
}

function distance(a, b) {
  return Math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2);
}

function average(values) {
  return values.length ? values.reduce((sum, value) => sum + value, 0) / values.length : 0;
}

function standardDeviation(values) {
  const mean = average(values);
  return values.length ? Math.sqrt(values.reduce((sum, value) => sum + (value - mean) ** 2, 0) / values.length) : 0;
}

function latticeSites(testCase, variant) {
  const spacing = testCase.spacing * variant.scale;
  const sites = [];

  for (let x = 0; x < 2; x += 1) {
    for (let y = 0; y < 2; y += 1) {
      for (let z = 0; z < 2; z += 1) {
        let chargeSign = (x + y + z) % 2 === 0 ? 1 : -1;
        if (variant.pattern === 'layered') {
          chargeSign = z === 0 ? 1 : -1;
        }
        if (variant.pattern === 'clustered') {
          chargeSign = x === 0 ? 1 : -1;
        }
        if (variant.pattern === 'pair-collapse') {
          chargeSign = x < 1 ? 1 : -1;
        }

        sites.push({
          element: chargeSign > 0 ? testCase.cation : testCase.anion,
          charge: chargeSign,
          position: vec(x * spacing, y * spacing, z * spacing),
        });
      }
    }
  }

  return sites;
}

function pairMetrics(sites, referenceSpacing) {
  const unlikeDistances = [];
  const likeDistances = [];
  let nearestUnlikeMatches = 0;
  let nearestLikeFailures = 0;

  for (let i = 0; i < sites.length; i += 1) {
    const distances = [];
    for (let j = 0; j < sites.length; j += 1) {
      if (i === j) {
        continue;
      }
      const d = distance(sites[i].position, sites[j].position);
      distances.push({ distance: d, unlike: sites[i].charge !== sites[j].charge });
      if (sites[i].charge !== sites[j].charge) {
        unlikeDistances.push(d);
      } else {
        likeDistances.push(d);
      }
    }
    distances.sort((a, b) => a.distance - b.distance);
    if (distances[0]?.unlike) {
      nearestUnlikeMatches += 1;
    } else {
      nearestLikeFailures += 1;
    }
  }

  const nearUnlike = unlikeDistances.filter((value) => value <= referenceSpacing * 1.05).length;
  const nearLike = likeDistances.filter((value) => value <= referenceSpacing * 1.05).length;

  return {
    unlikeDistances,
    likeDistances,
    nearestUnlikeRate: nearestUnlikeMatches / sites.length,
    nearestLikeFailureRate: nearestLikeFailures / sites.length,
    nearUnlike,
    nearLike,
    meanUnlikeDistance: average(unlikeDistances),
    meanLikeDistance: average(likeDistances),
    unlikeDistanceSpread: standardDeviation(unlikeDistances),
  };
}

function scoreVariant(testCase, variant) {
  const sites = latticeSites(testCase, variant);
  const metrics = pairMetrics(sites, testCase.spacing);
  const spacingStrain = clamp01(Math.abs(testCase.spacing * variant.scale - testCase.spacing) / (testCase.spacing * 0.45));
  const alternationIntegrity = clamp01(metrics.nearestUnlikeRate);
  const likeChargeSeparation = clamp01(1 - metrics.nearLike / Math.max(metrics.likeDistances.length, 1));
  const routeContinuity = clamp01(testCase.routeBase + alternationIntegrity * 0.18 - spacingStrain * 0.18 - metrics.nearestLikeFailureRate * 0.22);
  const latticeGeometry = clamp01(1 - spacingStrain * 0.74 - metrics.unlikeDistanceSpread / (testCase.spacing * 3));
  const polarityOrdering = clamp01(alternationIntegrity * 0.72 + likeChargeSeparation * 0.28);
  const collapseRisk = clamp01((1 - likeChargeSeparation) * 0.42 + spacingStrain * 0.38 + metrics.nearestLikeFailureRate * 0.2);

  const score = clamp01(
    alternationIntegrity * 0.24 +
      latticeGeometry * 0.2 +
      polarityOrdering * 0.2 +
      routeContinuity * 0.18 +
      likeChargeSeparation * 0.12 +
      (1 - collapseRisk) * 0.06
  );

  return {
    formula: testCase.formula,
    variant: variant.name,
    type: variant.type,
    score: Number(score.toFixed(4)),
    spacing: Number((testCase.spacing * variant.scale).toFixed(4)),
    alternationIntegrity: Number(alternationIntegrity.toFixed(3)),
    latticeGeometry: Number(latticeGeometry.toFixed(3)),
    polarityOrdering: Number(polarityOrdering.toFixed(3)),
    routeContinuity: Number(routeContinuity.toFixed(3)),
    likeChargeSeparation: Number(likeChargeSeparation.toFixed(3)),
    collapseRisk: Number(collapseRisk.toFixed(3)),
    nearestUnlikeRate: Number(metrics.nearestUnlikeRate.toFixed(3)),
    nearestLikeFailureRate: Number(metrics.nearestLikeFailureRate.toFixed(3)),
    nearLike: metrics.nearLike,
  };
}

const rows = cases.flatMap((testCase) => variants.map((variant) => scoreVariant(testCase, variant)));
const summaries = cases.map((testCase) => {
  const caseRows = rows.filter((row) => row.formula === testCase.formula);
  const reference = caseRows.find((row) => row.type === 'reference');
  const decoys = caseRows.filter((row) => row.type === 'decoy');
  const strained = caseRows.filter((row) => row.type === 'strained');
  const bestDecoy = decoys.reduce((best, row) => (row.score > best.score ? row : best), decoys[0]);
  const bestStrained = strained.reduce((best, row) => (row.score > best.score ? row : best), strained[0]);

  return {
    formula: testCase.formula,
    referenceScore: reference.score,
    bestStrained: bestStrained.variant,
    bestStrainedScore: bestStrained.score,
    bestDecoy: bestDecoy.variant,
    bestDecoyScore: bestDecoy.score,
    decoyPenalty: Number((reference.score - bestDecoy.score).toFixed(4)),
    referenceBeatsDecoys: decoys.every((row) => reference.score > row.score),
  };
});

const weak = summaries.filter((summary) => summary.decoyPenalty < 0.1 || !summary.referenceBeatsDecoys);
const diagnosis = weak.length
  ? `weak ionic lattice separation for ${weak.map((item) => item.formula).join(', ')}`
  : 'ionic lattice controls separate alternating lattice order from same-charge or collapsed decoys';

const json = {
  source: 'ionic-lattice-sweep.mjs',
  status: 'focused ionic lattice diagnostic; not part of molecule calibration',
  diagnosis,
  summaries,
  rows,
};

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ionic-lattice-sweep.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate Ionic Lattice Sweep

## Scope

This diagnostic addresses the current limitation that \`NaCl\` and \`LiF\` are only gas-phase pair proxies in the molecule coordinate bench.

It does not add bulk material behaviour to the molecule calibration. It tests a tiny ionic-lattice grammar: alternating unlike neighbours should outrank same-charge layers, clustered charges, and pair-collapse decoys.

## Summary

Diagnosis: ${diagnosis}.

| Formula | Reference score | Best strained | Best strained score | Best decoy | Best decoy score | Decoy penalty | Reference beats decoys |
|---|---:|---|---:|---|---:|---:|---|
${summaries
  .map(
    (summary) =>
      `| ${summary.formula} | ${summary.referenceScore} | ${summary.bestStrained} | ${summary.bestStrainedScore} | ${summary.bestDecoy} | ${summary.bestDecoyScore} | ${summary.decoyPenalty} | ${summary.referenceBeatsDecoys ? 'yes' : 'no'} |`
  )
  .join('\n')}

## Variant Rows

| Formula | Variant | Type | Score | Spacing | Alternation | Geometry | Polarity ordering | Route continuity | Like-charge separation | Collapse risk | Nearest unlike rate | Nearest like failure rate | Near-like pairs |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
${rows
  .map(
    (row) =>
      `| ${row.formula} | ${row.variant} | ${row.type} | ${row.score} | ${row.spacing} | ${row.alternationIntegrity} | ${row.latticeGeometry} | ${row.polarityOrdering} | ${row.routeContinuity} | ${row.likeChargeSeparation} | ${row.collapseRisk} | ${row.nearestUnlikeRate} | ${row.nearestLikeFailureRate} | ${row.nearLike} |`
  )
  .join('\n')}

## Reading

This is a topology/control diagnostic, not a crystal physics model. The useful question is whether a minimal route grammar can distinguish alternating ionic order from obvious wrong arrangements before the project attempts richer lattice or bulk-material modelling.
`;

await writeFile(new URL('ionic-lattice-sweep.md', outDir), markdown);

console.log(`Cases tested: ${cases.length}`);
console.log(`Diagnosis: ${diagnosis}`);
console.log(`Wrote ${new URL('ionic-lattice-sweep.md', outDir).pathname}`);
