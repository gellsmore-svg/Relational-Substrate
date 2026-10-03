import { readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const calibrationUrl = new URL('molecule-calibration-summary.json', outDir);
const coordinateUrl = new URL('molecule-coordinate-sweep.json', outDir);

function percent(value) {
  return `${(value * 100).toFixed(2)}%`;
}

function scoreGate(pass, weight) {
  return pass ? weight : 0;
}

function familyGateScore(family) {
  const rankGate = family.allReferenceFirst;
  const overfitGate = family.aboveReferenceTotal === 0;
  const envelopeGate = family.averageNearRate > 0 && family.averageNearRate < 0.09;
  const failureGate = family.averageFailureRate > 0.01;

  return {
    rankGate,
    overfitGate,
    envelopeGate,
    failureGate,
    score:
      scoreGate(rankGate, 0.35) +
      scoreGate(overfitGate, 0.35) +
      scoreGate(envelopeGate, 0.15) +
      scoreGate(failureGate, 0.15),
  };
}

const mechanismPath = [
  'continuous T0 substrate',
  'local organised disturbance',
  'torsion/tension/alignment expression',
  'candidate closure-pattern',
  'stable primary topology/vorton',
  'coupled vorton regime',
  'secondary material regime',
  'perceived matter',
];

const patternDescriptors = {
  'diatomic covalent': {
    patternName: 'paired closure bridge',
    routeCount: 'one dominant coupling route',
    closureTopology: 'two stable primary closures held in a shared tension path',
    polarityMode: 'neutral or polar imbalance is expressed as directional route bias, not as a material filler',
    angularConstraint: 'minimal; the main constraint is separation stability',
    torsionMode: 'low torsion demand',
    distributionMode: 'local pair coupling',
    candidateMechanism:
      'Two compatible vorton regimes settle into a shared route where closure identity remains intact while the interclosure tension path resists both collapse and separation.',
    admissibilityGates: [
      'bond-length stability must dominate the near-reference envelope',
      'route continuity must survive small coordinate perturbations',
      'polarity skew may bias the route but must not create a third material entity',
    ],
  },
  'bent polar': {
    patternName: 'two-route angular hinge',
    routeCount: 'two coupled routes around one dominant closure',
    closureTopology: 'central closure accepts two bounded routes whose mutual angle is part of the stable regime',
    polarityMode: 'polarity is a directional asymmetry across the coupled routes',
    angularConstraint: 'strong; coherence depends on preserving a non-linear angle',
    torsionMode: 'low to moderate depending on out-of-plane displacement',
    distributionMode: 'local asymmetric multi-route coupling',
    candidateMechanism:
      'A central vorton regime admits two compatible coupling routes. The routes cannot collapse into a line because the polarity/tension balance is stabilised by angular separation.',
    admissibilityGates: [
      'angle perturbations must narrow the coherence envelope',
      'polarity balance must be a real constraint, not an afterthought',
      'route competition must preserve central closure identity',
    ],
  },
  'trigonal pyramidal covalent': {
    patternName: 'three-route polar canopy',
    routeCount: 'three coupled routes around one dominant closure',
    closureTopology: 'central closure holds three bounded routes in a non-planar canopy rather than a flat brace',
    polarityMode: 'polarity is expressed through out-of-plane asymmetry across the three routes',
    angularConstraint: 'strong; coherence depends on preserving pyramidal angle distribution',
    torsionMode: 'moderate to high because flattening changes the polarity-bearing geometry',
    distributionMode: 'local three-route coupling with vertical polarity bias',
    candidateMechanism:
      'A central vorton regime admits three compatible coupling routes whose stable state is not planar. The route set holds a directional polarity because the canopy cannot collapse into a flat three-route brace without changing the constraint grammar.',
    admissibilityGates: [
      'pyramidal geometry must remain distinct from trigonal planar geometry',
      'flattening should reduce coherence by disturbing polarity-bearing route alignment',
      'three-route polarity must remain a coupling constraint, not a hidden material component',
    ],
  },
  'linear triatomic': {
    patternName: 'opposed route line',
    routeCount: 'two opposed coupling routes',
    closureTopology: 'central closure carries opposed routes that minimise net lateral imbalance',
    polarityMode: 'balanced cases cancel globally; polar cases retain an axial bias',
    angularConstraint: 'very strong; deviation from line creates immediate strain',
    torsionMode: 'low torsion demand unless the line is warped',
    distributionMode: 'axial route coupling',
    candidateMechanism:
      'A central vorton regime is constrained by two opposed route couplings. The stable state is the one where lateral tension cancels or resolves into a single axial polarity.',
    admissibilityGates: [
      'linearity must be a high-sensitivity constraint',
      'opposed route perturbations must create strong failure rates',
      'polarity must distinguish balanced and biased linear regimes',
    ],
  },
  'linear unsaturated covalent': {
    patternName: 'linear unsaturated route spine',
    routeCount: 'one high-retention axial route with terminal route constraints',
    closureTopology: 'two central closure regimes hold a stiff axial route while terminal routes preserve linear extension',
    polarityMode: 'usually balanced globally, with polarity appearing as axial bias when termini differ',
    angularConstraint: 'very strong; bending the axis should sharply degrade coherence',
    torsionMode: 'low admissible torsion because the reference spine is linear',
    distributionMode: 'axial multi-route coupling with high bond-order retention',
    candidateMechanism:
      'An unsaturated route spine behaves as a stiff linear coupling grammar: the central route resists bending and terminal perturbation while preserving route continuity across the whole axis.',
    admissibilityGates: [
      'linear reference geometry must outrank bent or warped variants',
      'bond distribution must remain a high-sensitivity constraint',
      'the unsaturated spine must not be treated as a material rod inserted between closures',
    ],
  },
  'tetrahedral covalent': {
    patternName: 'four-route spatial brace',
    routeCount: 'four coupled routes',
    closureTopology: 'central closure distributes four route constraints through a three-dimensional brace',
    polarityMode: 'often globally balanced, but local asymmetries must remain bounded',
    angularConstraint: 'strong three-dimensional angle distribution',
    torsionMode: 'moderate; torsion matters as a proxy for spatial route integrity',
    distributionMode: 'saturated spatial coupling',
    candidateMechanism:
      'A central vorton regime stabilises four route couplings by distributing tension through a spatial arrangement. Flattening or crowding overloads the shared closure grammar.',
    admissibilityGates: [
      'reference geometry must outrank planar or crowded variants',
      'angle distribution must narrow the coherence envelope',
      'steric pressure must express route interference rather than hidden matter',
    ],
  },
  'rotatable covalent': {
    patternName: 'rotatable single-route hinge',
    routeCount: 'one dominant interclosure route plus local substituent routes',
    closureTopology: 'two coupled closure groups remain bonded while torsional reseating changes the surrounding route presentation',
    polarityMode: 'neutral cases distribute polarity weakly; polar cases retain a torsion-sensitive directional bias',
    angularConstraint: 'moderate; local angles must persist while rotation remains admissible',
    torsionMode: 'high but permissive; torsion changes should be constrained without forcing planarity',
    distributionMode: 'local hinge coupling with rotatable route presentation',
    candidateMechanism:
      'Two compatible closure regimes share a persistent route while the attached route set can reseat around that route. Coherence requires the hinge to preserve identity without treating every torsion as failure.',
    admissibilityGates: [
      'reference torsion should rank above collapsed or crowded alternatives',
      'torsion sensitivity must be present without behaving like planar lock',
      'rotatable behaviour must remain a coupling grammar, not an inserted mechanical joint',
    ],
  },
  'trigonal planar covalent': {
    patternName: 'three-route planar brace',
    routeCount: 'three coupled routes',
    closureTopology: 'central closure distributes three route constraints through a flat angular brace',
    polarityMode: 'often globally balanced, with local route polarity cancelling through planar symmetry',
    angularConstraint: 'strong planar angle distribution without ring closure',
    torsionMode: 'high sensitivity to out-of-plane warping',
    distributionMode: 'planar three-route coupling',
    candidateMechanism:
      'A central vorton regime stabilises three route couplings in a planar arrangement. The route grammar is not cyclic like an aromatic ring, but it still rejects pyramidal or warped displacement.',
    admissibilityGates: [
      'reference geometry must outrank pyramidal or warped variants',
      'planar angle distribution must matter without invoking ring closure',
      'route balance must remain centralised rather than distributed around a loop',
    ],
  },
  'asymmetric planar covalent': {
    patternName: 'uneven planar polarity brace',
    routeCount: 'three coupled routes with unequal route demand',
    closureTopology: 'central closure distributes planar routes while one route carries stronger polarity/tension bias',
    polarityMode: 'polarity is not cancelled by symmetry; it remains a directed constraint across the planar brace',
    angularConstraint: 'strong planar angle distribution with unequal route lengths',
    torsionMode: 'high sensitivity to out-of-plane warping because planar polarity depends on route alignment',
    distributionMode: 'centralised planar coupling with asymmetric route weighting',
    candidateMechanism:
      'A central vorton regime stabilises three route couplings in a plane, but one route carries stronger polarity and tension demand. Coherence requires the unequal routes to remain jointly bounded without becoming a ring or a hidden intermediate entity.',
    admissibilityGates: [
      'reference geometry must outrank symmetric, warped, or polarity-flattened variants',
      'unequal route lengths must contribute to the coherence envelope',
      'polarity bias must be resolved as route constraint, not as a material filler',
    ],
  },
  'aromatic ring': {
    patternName: 'distributed ring route',
    routeCount: 'six cyclically coupled routes',
    closureTopology: 'multiple closures participate in a recurrent route whose identity is distributed around a loop',
    polarityMode: 'neutral or heteroatom-biased distribution across the ring',
    angularConstraint: 'strong planar angle distribution',
    torsionMode: 'high sensitivity to warping',
    distributionMode: 'cyclic distributed coupling',
    candidateMechanism:
      'A set of compatible vorton regimes closes into a recurrent route. Stability belongs to the distributed loop, so local displacement, polarity skew, or planarity loss degrades the whole route.',
    admissibilityGates: [
      'ring/distributed route must be highly constrained',
      'planarity and route continuity must matter together',
      'heteroatom polarity must bias the ring without breaking distributed identity',
    ],
  },
  'ionic pair': {
    patternName: 'separated polarity lock',
    routeCount: 'one dominant polarity route',
    closureTopology: 'two unlike closures hold separation through complementary polarity constraint',
    polarityMode: 'polarity is the dominant admissibility condition',
    angularConstraint: 'minimal in pair proxy form',
    torsionMode: 'low in pair proxy form',
    distributionMode: 'pairwise separation coupling; crystal behaviour not represented yet',
    candidateMechanism:
      'Two unlike vorton regimes are constrained by complementary polarity. The stable pair is a separation lock, not a covalent sharing route and not a model of an ionic lattice.',
    admissibilityGates: [
      'polarity/separation must dominate over angular behaviour',
      'pair model must remain explicitly distinct from crystal lattice behaviour',
      'no extra charged substance may be inserted between closures',
    ],
  },
};

const calibration = JSON.parse(await readFile(calibrationUrl, 'utf8'));
const coordinate = JSON.parse(await readFile(coordinateUrl, 'utf8'));

const families = calibration.families.map((family) => {
  const descriptor = patternDescriptors[family.family];
  const gates = familyGateScore(family);
  const molecules = calibration.rows.filter((row) => row.family === family.family).map((row) => row.formula);

  return {
    family: family.family,
    molecules,
    descriptor,
    validation: {
      cases: family.cases,
      allReferenceFirst: family.allReferenceFirst,
      aboveReferenceTotal: family.aboveReferenceTotal,
      averageNearRate: family.averageNearRate,
      averageFailureRate: family.averageFailureRate,
      dominantConstraints: family.dominantConstraints,
      gateScore: Number(gates.score.toFixed(3)),
      gates,
    },
  };
});

const json = {
  source: ['molecule-coordinate-sweep.json', 'molecule-calibration-summary.json'],
  status: 'candidate T1 coupling descriptors; not proof and not a hidden material layer',
  mechanismPath,
  excludedMiddleLayer:
    'These descriptors do not introduce cells, particles, lattices, or material components between T0 substrate and T1 vortons.',
  families,
  nextWork: [
    'turn each descriptor into bounded numerical parameters',
    'generate competing T1 coupling candidates per family',
    'score candidates against the existing T2 coordinate calibration without per-molecule tuning',
  ],
};

await writeFile(new URL('t1-coupling-patterns.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate T1 Coupling Pattern Descriptors

## Scope

This report adds candidate T1 coupling descriptors beneath the current T2 molecule calibration bench.

It does not prove the Relational Substrate theory, does not derive matter from first principles, and does not insert a hidden material layer. The purpose is narrower: define mechanism-facing descriptors that can later be converted into bounded parameters and tested against the existing T2 coordinate results.

## Mechanism Path

${mechanismPath.map((step, index) => `${index + 1}. ${step}`).join('\n')}

## Guardrail

${json.excludedMiddleLayer}

Vortons remain candidate stable primary topology. Molecules remain secondary material regimes. The descriptors below are coupling grammars between those levels, not additional material things.

## Family Descriptors

${families
  .map(
    ({ family, molecules, descriptor, validation }) => `### ${family}

Molecules currently covered: ${molecules.join(', ')}

Candidate pattern: ${descriptor.patternName}

| Field | Descriptor |
|---|---|
| Route count | ${descriptor.routeCount} |
| Closure topology | ${descriptor.closureTopology} |
| Polarity mode | ${descriptor.polarityMode} |
| Angular constraint | ${descriptor.angularConstraint} |
| Torsion mode | ${descriptor.torsionMode} |
| Distribution mode | ${descriptor.distributionMode} |

Candidate mechanism:

${descriptor.candidateMechanism}

Admissibility gates:

${descriptor.admissibilityGates.map((gate) => `- ${gate}`).join('\n')}

Current validation:

| Cases | References first | Above-reference candidates | Avg near-reference rate | Avg strong-failure rate | Dominant constraints | Gate score |
|---:|---|---:|---:|---:|---|---:|
| ${validation.cases} | ${validation.allReferenceFirst ? 'yes' : 'no'} | ${validation.aboveReferenceTotal} | ${percent(validation.averageNearRate)} | ${percent(validation.averageFailureRate)} | ${validation.dominantConstraints} | ${validation.gateScore} |
`
  )
  .join('\n')}

## Interpretation

Every current family passes the coarse gate because each reference geometry ranks first and no generated perturbation beats the reference. That only says the T2 calibration layer is internally sane enough to support the next modelling step.

The next step is to turn each descriptor into bounded numerical parameters. Candidate parameter sets can then be iterated in volume against the existing T2 coordinate calibration. If a family cannot be made coherent without per-molecule tuning, the candidate T1 coupling grammar is wrong or incomplete.
`;

await writeFile(new URL('t1-coupling-patterns.md', outDir), markdown);

console.log(`Read ${coordinateUrl.pathname}`);
console.log(`Read ${calibrationUrl.pathname}`);
console.log(`Wrote ${new URL('t1-coupling-patterns.md', outDir).pathname}`);
