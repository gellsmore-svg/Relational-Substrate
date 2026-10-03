import { mkdir, readFile, writeFile } from 'node:fs/promises';

// Shared-weights degradation test.
//
// The coordinate bench ranks each reference geometry against its perturbation
// population using PER-FAMILY weights (familyScore). The headline "all references
// rank first" result therefore leans on weights tuned per family over very few
// cases — the named overfitting risk. This report re-reads the same sweep and asks:
// how much does that result degrade under ONE shared weight vector (genericScore,
// the single fixed `scoreCandidate` vector — no per-family tuning)?
//
// Both scores already exist per candidate in the sweep; molecule-coordinate-sweep
// now also stores the reference's rank/above/within-5% under the generic vector.
// The gap between the family-tuned and shared-vector columns is a direct, if rough,
// estimate of how load-bearing per-family tuning is. It does not prove or disprove
// AMS; it only measures tuning dependence inside the bench.

const outDir = new URL('./out/', import.meta.url);
const sweepPath = new URL('./out/molecule-coordinate-sweep.json', import.meta.url);

const sweep = JSON.parse(await readFile(sweepPath, 'utf8'));
const results = sweep.results;

const rate = (n, d) => (d ? n / d : 0);
const pct = (x) => `${(x * 100).toFixed(2)}%`;

const rows = results.map((r) => ({
  formula: r.formula,
  family: r.family,
  iterations: r.iterations,
  familyRank: r.referenceRank,
  genericRank: r.referenceGenericRank,
  familyAbove: r.aboveReference,
  genericAbove: r.genericAboveReference,
  familyNearRate: rate(r.withinFivePercent, r.iterations),
  genericNearRate: rate(r.genericWithinFivePercent, r.iterations),
  // family weights keep the reference first only because of per-family tuning
  // when the generic (shared) vector drops it below rank 1:
  tuningDependent: r.referenceRank === 1 && r.referenceGenericRank > 1,
}));

const total = rows.length;
const familyRank1 = rows.filter((r) => r.familyRank === 1).length;
const genericRank1 = rows.filter((r) => r.genericRank === 1).length;
const tuningDependent = rows.filter((r) => r.tuningDependent);
const worst = [...rows].sort((a, b) => b.genericRank - a.genericRank)[0];
const familyAboveTotal = rows.reduce((s, r) => s + r.familyAbove, 0);
const genericAboveTotal = rows.reduce((s, r) => s + r.genericAbove, 0);
const meanFamilyNear = rate(rows.reduce((s, r) => s + r.familyNearRate, 0), total);
const meanGenericNear = rate(rows.reduce((s, r) => s + r.genericNearRate, 0), total);

// Per-family rollup.
const families = [...new Set(rows.map((r) => r.family))].sort();
const familyRollup = families.map((fam) => {
  const fr = rows.filter((r) => r.family === fam);
  return {
    family: fam,
    cases: fr.length,
    allRankFirstFamily: fr.every((r) => r.familyRank === 1),
    allRankFirstGeneric: fr.every((r) => r.genericRank === 1),
    tuningDependent: fr.filter((r) => r.tuningDependent).length,
    avgFamilyNear: rate(fr.reduce((s, r) => s + r.familyNearRate, 0), fr.length),
    avgGenericNear: rate(fr.reduce((s, r) => s + r.genericNearRate, 0), fr.length),
  };
});

const lines = [];
lines.push('# Shared-Weights Degradation Test');
lines.push('');
lines.push('This report does not prove AMS. It measures how much the coordinate bench\'s');
lines.push('"all references rank first" result depends on per-family weight tuning, by');
lines.push('re-ranking each reference under a single shared weight vector (no per-family');
lines.push('tuning). The gap is an internal overfitting-sensitivity estimate only.');
lines.push('');
lines.push('- **Family weights**: per-family vector tuned over that family\'s cases (`familyScore`).');
lines.push('- **Shared weights**: one fixed generic vector applied to every family (`genericScore`).');
lines.push('- **Tuning-dependent**: reference ranks #1 under family weights but **not** under shared weights.');
lines.push('');
lines.push('## Headline');
lines.push('');
lines.push('| Metric | Family weights | Shared weights |');
lines.push('|---|---:|---:|');
lines.push(`| References ranking #1 (of ${total}) | ${familyRank1} | ${genericRank1} |`);
lines.push(`| Tuning-dependent references | 0 (by definition) | ${tuningDependent.length} |`);
lines.push(`| Total perturbations beating their reference | ${familyAboveTotal} | ${genericAboveTotal} |`);
lines.push(`| Mean near-reference rate (envelope width) | ${pct(meanFamilyNear)} | ${pct(meanGenericNear)} |`);
lines.push(`| Worst reference rank | 1 | ${worst.genericRank} (${worst.formula}) |`);
lines.push('');
if (tuningDependent.length === 0) {
  lines.push('**Reading:** every reference still ranks #1 under a single shared vector, so');
  lines.push('per-family weights are **not** what keeps references on top — they sharpen the');
  lines.push('envelope but are not load-bearing for the headline ranking claim. Overfitting');
  lines.push('risk from tuning is lower than the family-weight structure suggests, though the');
  lines.push('envelope still widens under shared weights (less discrimination).');
} else {
  lines.push(`**Reading:** ${tuningDependent.length} reference(s) lose rank #1 under a single shared`);
  lines.push('vector, so per-family weights are doing load-bearing work for those cases — that');
  lines.push('is where tuning, not geometry, secures the result. These are the overfit-sensitive');
  lines.push('cases to watch as independent cases are added:');
  lines.push('');
  for (const r of tuningDependent) {
    lines.push(`- **${r.formula}** (${r.family}): family rank 1 → shared rank ${r.genericRank}, ${r.genericAbove} perturbation(s) above reference.`);
  }
}
lines.push('');
lines.push('## Per-Family');
lines.push('');
lines.push('| Family | Cases | All #1 (family) | All #1 (shared) | Tuning-dependent | Near-rate family | Near-rate shared |');
lines.push('|---|---:|:---:|:---:|---:|---:|---:|');
for (const f of familyRollup) {
  lines.push(`| ${f.family} | ${f.cases} | ${f.allRankFirstFamily ? 'yes' : 'no'} | ${f.allRankFirstGeneric ? 'yes' : 'no'} | ${f.tuningDependent} | ${pct(f.avgFamilyNear)} | ${pct(f.avgGenericNear)} |`);
}
lines.push('');
lines.push('## Per-Molecule');
lines.push('');
lines.push('| Molecule | Family | Rank (family) | Rank (shared) | Above ref (family) | Above ref (shared) | Near-rate family | Near-rate shared |');
lines.push('|---|---|---:|---:|---:|---:|---:|---:|');
for (const r of rows) {
  lines.push(`| ${r.formula} | ${r.family} | ${r.familyRank} | ${r.genericRank} | ${r.familyAbove} | ${r.genericAbove} | ${pct(r.familyNearRate)} | ${pct(r.genericNearRate)} |`);
}
lines.push('');
lines.push('## Caveat');
lines.push('');
lines.push('Shared weights here means the existing fixed `scoreCandidate` vector, which was');
lines.push('itself hand-set (not learned). A reference still ranking first under it shows the');
lines.push('family tuning is not the only thing separating reference from perturbation, but it');
lines.push('does not establish that the shared vector is correct — only that the ranking result');
lines.push('survives removing the per-family layer. The genuine next test remains adding new');
lines.push('independent molecule families and re-checking both columns.');
lines.push('');

const markdown = lines.join('\n');
await mkdir(outDir, { recursive: true });
await writeFile(new URL('shared-weights-degradation.md', outDir), markdown);
await writeFile(
  new URL('shared-weights-degradation.json', outDir),
  JSON.stringify({ headline: { total, familyRank1, genericRank1, tuningDependent: tuningDependent.length, familyAboveTotal, genericAboveTotal, meanFamilyNear, meanGenericNear, worst }, familyRollup, rows }, null, 2),
);

console.log(`References ranking #1 — family: ${familyRank1}/${total}, shared: ${genericRank1}/${total}`);
console.log(`Tuning-dependent references: ${tuningDependent.length}`);
console.log(`Mean near-reference rate — family: ${pct(meanFamilyNear)}, shared: ${pct(meanGenericNear)}`);
console.log(`Wrote ${new URL('shared-weights-degradation.md', outDir).pathname}`);
