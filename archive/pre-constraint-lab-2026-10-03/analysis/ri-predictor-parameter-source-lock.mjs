import { mkdir, writeFile } from 'node:fs/promises';

// Parameter source-lock for the RI structural predictor (predeclaration hash
// b764feb54971f5a9). The predictor needs published electronic-polarizability
// values locked from a NAMED, accessible source before any target is scored.
//
// Source located and cached: R.D. Shannon and R.X. Fischer, "Empirical electronic
// polarizabilities of ions for the prediction and interpretation of refractive
// indices: Oxides and oxysalts", American Mineralogist 101, 2288-2300 (2016),
// DOI 10.2138/am-2016-5730. Open MSA author preprint (minsocam.org); cached at
// analysis/source-cache/shannon-fischer-2016-polarizabilities-preprint.pdf (+.txt).
//
// This is the canonical, purpose-built source for predicting refractive index from
// ion polarizabilities, derived from ~2600 nD measurements on 1200 minerals + 675
// synthetic compounds. It is BETTER suited than the paywalled SF2006 PRB paper.
//
// This step scores nothing and fits nothing. It locks parameters AND records that
// the locked source is structurally inconsistent with predictor v0, so a v1
// reconciliation is required before scoring (see findings).

const outDir = new URL('./out/', import.meta.url);

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const source = {
  citation:
    'R.D. Shannon, R.X. Fischer, Empirical electronic polarizabilities of ions for the prediction and interpretation of refractive indices: Oxides and oxysalts, American Mineralogist 101, 2288-2300 (2016)',
  doi: '10.2138/am-2016-5730',
  access: 'open MSA author preprint at minsocam.org (final paywalled at GeoScienceWorld); also a Univ. Antwerp repository copy',
  cached: 'analysis/source-cache/shannon-fischer-2016-polarizabilities-preprint.pdf (+ .txt)',
  basis: '~2600 nD (589.3 nm) measurements on 1200 minerals, 675 synthetic compounds; least-squares fit of 270 electronic polarizabilities for 76 cations in various coordinations',
};

// Locked relation. The exact algebraic form of eqn (4a) is rendered as an image in
// the preprint and was NOT captured by text extraction; it is locked BY REFERENCE
// here and must be transcribed verbatim from the source equation when the predictor
// is coded. Variables and the constant are confirmed from the surrounding text.
const relation = {
  name: 'Anderson-Eggleton (AE) relationship, eqn (4a) of Shannon-Fischer 2016',
  constant: 'c = 2.26 (Eggleton 1991), used throughout SF2016',
  variables: 'total polarizability alpha_T, refractive index nD at 589.3 nm, molar volume Vm in Angstrom^3',
  additivity: 'alpha_T = sum over ions of alpha_e(ion) (polarizability additivity rule)',
  note: 'NOT pure Lorentz-Lorenz; transcribe the literal eqn (4a) from the cached source before implementing',
  provenanceLines: 'preprint ~lines 44, 206-273 (.txt)',
};

// Locked numeric parameters (Angstrom^3), with provenance to the cached .txt.
const caCoordinationResolved = [
  { cn: 5, alpha: 1.910 },
  { cn: 6, alpha: 1.790 },
  { cn: 7, alpha: 1.670 },
  { cn: 8, alpha: 1.570 },
  { cn: 9, alpha: 1.480 },
  { cn: 10, alpha: 1.390 },
  { cn: 11, alpha: 1.320 },
  { cn: 12, alpha: 1.250 },
];

const lockedParameters = {
  oxygen: {
    descriptor: 'anion-volume-dependent O2- polarizability via eqn (6)',
    refValue: 'alpha-(O2-) = 1.79 Angstrom^3, No = -1.776 (whole-dataset refinement)',
    range: 'effective O2- polarizability varies with anion volume, e.g. ~1.44 Angstrom^3 in SiO2 upward',
    provenanceLines: 'preprint ~lines 780-828 (.txt)',
    note: 'this is the source structural mechanism for oxygen; it REPLACES the bridging/non-bridging split assumed in predictor v0',
  },
  silicon: {
    ion: 'Si4+ ([4]-coordinate)',
    alpha: 0.284,
    provenanceLines: 'preprint ~lines 986-1000, 2782 (.txt)',
  },
  calciumCoordinationResolved: {
    ion: 'Ca2+ resolved by coordination number CN (the bracketed [CN] in the cation table)',
    values: caCoordinationResolved,
    selector: 'ca_coordination descriptor selects the row; alpha decreases monotonically with CN',
    wollastoniteNote: 'wollastonite Ca is ~6-coordinate -> alpha(Ca2+,[6]) = 1.790 Angstrom^3 expected, to be confirmed from the CIF at scoring',
    provenanceLines: 'preprint cation table ~lines 2373-2387 (.txt)',
  },
  traceIonsAvailable: {
    note: 'if the trace-composition decision includes them, the same table provides them; partial values already seen',
    aluminium: 'alpha([4]Al3+)=0.40, alpha([5]Al3+)=0.43, alpha([6]Al3+)=0.47 (preprint ~line 1000)',
    others: 'Mg2+, Mn2+, Fe2+, Ti4+ present in the same coordination-resolved cation table; extract at scoring if needed',
  },
};

const findings = [
  {
    id: 'form-inconsistency',
    severity: 'blocks scoring under v0',
    finding:
      'predictor v0 (hash b764feb54971f5a9) is inconsistent with the only accessible authoritative parameter source on two axes',
    detail: [
      'conversion: v0 predeclared Lorentz-Lorenz; SF2016 derives and uses Anderson-Eggleton (c=2.26). Using SF2016 alpha values with Lorentz-Lorenz is internally inconsistent.',
      'oxygen: v0 predeclared a bridging/non-bridging O split with separate fixed refractivities; SF2016 instead models O2- polarizability as a function of anion volume (one mechanism, eqn 6). No published bridging/non-bridging split values exist in this source.',
      'cation coordination: v0 predeclared coordination-resolved cation polarizabilities -- this IS consistent with SF2016 (Ca2+ is tabulated per CN).',
    ],
    consequence:
      'do not score under v0. Emit a reconciled predictor v1 that adopts the Anderson-Eggleton relation and the SF2016 anion-volume O2- model, keeps coordination-resolved cation polarizabilities, and freezes the literal eqn (4a)/eqn (6) forms transcribed from the cached source -- all before any target lookup.',
  },
  {
    id: 'novelty-vs-established-method',
    severity: 'strategic; affects how any RI pass may be interpreted',
    finding:
      'Shannon-Fischer 2016 is ALREADY a complete, validated structural RI predictor: coordination-resolved cation polarizabilities + anion-volume O2- + Anderson-Eggleton predicts nD across ~2600 compounds.',
    detail: [
      'a structural RS predictor built on these locked parameters would, to first order, recapitulate established crystal chemistry rather than test a novel topology grammar.',
      'a wollastonite pass under this predictor would demonstrate CONSISTENCY with established polarizability theory, not independent evidence for the unification thesis.',
      'to add independent evidence, the RS predictor would have to predict something SF2016 does not, or use a genuinely different mechanism that still matches measured nD.',
    ],
    consequence:
      'interpret any RI result accordingly: a pass is a consistency check (still useful, and still gated by the held-out discipline), but it should not by itself raise unification-thesis confidence. This connects to docs/information-limitation-assessment-2026-06-24.md.',
  },
];

const report = {
  source: 'ri-predictor-parameter-source-lock.mjs',
  date: '2026-06-24',
  status:
    'parameter source located, cached, and partially locked; predictor v0 found inconsistent with the source, so a reconciled v1 is required before scoring',
  validationClaim: false,
  evidenceStatus: 'none; parameters locked from a published source, nothing scored or fitted',
  servesPredictorForm: 'b764feb54971f5a9',
  source,
  relation,
  lockedParameters,
  findings,
  nextStep:
    'emit RI structural predictor v1 reconciled to Shannon-Fischer 2016 (Anderson-Eggleton relation + anion-volume O2- + coordination-resolved cations), transcribing the literal eqn (4a) and eqn (6) forms from the cached preprint, and define the conventional vs structural contrast so that the test is not merely a restatement of SF2016; only then settle the composition decision, reserve the wollastonite-1A target, and score',
};

const markdown = `# RI Predictor Parameter Source-Lock

## Scope

Locks the published electronic-polarizability parameters the RI structural predictor
(\`b764feb54971f5a9\`) requires, from a named accessible source. Scores nothing,
fits nothing. It also records that the locked source is inconsistent with predictor
v0, so a reconciled v1 is needed before any target is scored.

Status: **${report.status}**

## Locked source

- ${source.citation}
- DOI ${source.doi}; ${source.access}
- cached: ${source.cached}
- basis: ${source.basis}

## Locked relation

- ${relation.name}; ${relation.constant}
- variables: ${relation.variables}
- additivity: ${relation.additivity}
- ${relation.note} (provenance: ${relation.provenanceLines})

## Locked parameters (Angstrom^3)

### Ca2+ coordination-resolved (selector: ca_coordination)

${table(['CN', 'alpha(Ca2+)'], caCoordinationResolved.map((r) => [`[${r.cn}]`, r.alpha]))}

${lockedParameters.calciumCoordinationResolved.wollastoniteNote} (provenance: ${lockedParameters.calciumCoordinationResolved.provenanceLines}).

### Si4+ and O2-

- Si4+ ([4]): alpha = ${lockedParameters.silicon.alpha} (provenance: ${lockedParameters.silicon.provenanceLines})
- O2-: ${lockedParameters.oxygen.refValue}; ${lockedParameters.oxygen.range} (provenance: ${lockedParameters.oxygen.provenanceLines})
- O2- note: ${lockedParameters.oxygen.note}

### Trace ions (only if composition decision includes them)

- ${lockedParameters.traceIonsAvailable.aluminium}
- ${lockedParameters.traceIonsAvailable.others}

## Findings

${findings
  .map(
    (f) =>
      `### ${f.id} (${f.severity})\n\n${f.finding}\n\n${f.detail.map((d) => `- ${d}`).join('\n')}\n\nConsequence: ${f.consequence}`,
  )
  .join('\n\n')}

## Next step

${report.nextStep}
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-predictor-parameter-source-lock.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('ri-predictor-parameter-source-lock.md', outDir), markdown);

console.log(`RI predictor parameter source-lock: ${report.status}`);
