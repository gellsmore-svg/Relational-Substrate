# AMS Expanded Library Scoreboard v1

## Purpose

This document scores the expanded formalised case library after:

- `ams-expanded-case-library-update-v1.md`

The goal is to assess the expanded cases before moving into broader element/material coverage.

Cases are scored by:

- anchor strength
- frontier value
- cluster contribution
- geometry maturity
- notation clarity

These are programme-steering scores, not truth scores.

## Scoring Criteria

Each score is from `1-10`.

### Anchor Strength

How useful the case is as a stabilising reference point.

### Frontier Value

How useful the case is for exposing unresolved model behaviour.

### Cluster Contribution

How much the case strengthens the current cluster map.

### Geometry Maturity

How well developed the geometric interpretation currently is.

### Notation Clarity

How cleanly the case can be represented using the current formal notation.

## Scoreboard

| Case | Anchor strength | Frontier value | Cluster contribution | Geometry maturity | Notation clarity | Current role |
|---|---:|---:|---:|---:|---:|---|
| air -> glass | 9 | 5 | 8 | 8 | 9 | broad entry anchor |
| air -> rough glass | 6 | 7 | 8 | 7 | 8 | entry-side degradation bridge |
| glass -> air | 7 | 10 | 10 | 8 | 9 | release frontier anchor |
| glass -> air [pocket-dominant] | 6 | 9 | 9 | 8 | 9 | pocket frontier subcase |
| glass -> air [diffuse-dominant] | 6 | 8 | 9 | 8 | 9 | diffuse release subcase |
| air -> polished metal | 10 | 5 | 8 | 8 | 9 | reflection anchor |
| air -> oxidised metal | 8 | 7 | 8 | 7 | 8 | degradation contrast anchor |
| glass -> crystal | 7 | 10 | 10 | 8 | 9 | compatibility frontier anchor |
| glass -> crystal [selective_success] | 8 | 6 | 8 | 8 | 9 | compatibility success subcase |
| glass -> crystal [late-gate dominated] | 6 | 9 | 9 | 8 | 9 | blocked compatibility subcase |
| glass -> crystal [mixed_frontier] | 6 | 10 | 10 | 8 | 9 | mixed compatibility frontier |
| crystal -> air | 8 | 7 | 8 | 7 | 8 | ordered release comparison |
| crystal -> air [ordered-return dominated] | 8 | 7 | 9 | 8 | 9 | return-side comparison subcase |

## Strongest Anchors

## 1. Air -> Polished Metal

Anchor strength:

- `10`

Why:

- cleanest reflection case
- strong `O4 / R4`
- high notation clarity
- low ambiguity compared with the frontier cases

## 2. Air -> Glass

Anchor strength:

- `9`

Why:

- cleanest broad entry handoff case
- stabilises the transmission side
- strong `R1 / R2` entry benchmark

## 3. Air -> Oxidised Metal

Anchor strength:

- `8`

Why:

- strongest degradation contrast case
- prevents the framework from becoming overly glass-centred

## 4. Crystal -> Air and Ordered-Return Subcase

Anchor strength:

- `8`

Why:

- ordered release and ordered return are now both better represented
- useful comparison against both glass release and polished metal return

## Strongest Frontiers

## 1. Glass -> Air

Frontier value:

- `10`

Why:

- release-side frontier anchor
- carries route reality, pocketing, diffusion, and mixed dynamics in one family

## 2. Glass -> Crystal

Frontier value:

- `10`

Why:

- strongest compatibility frontier
- strongest cross-whole transition case
- pressures `I_comp`, `L3`, `R3/R5`, and `O2/O3`

## 3. Glass -> Crystal [Mixed Frontier]

Frontier value:

- `10`

Why:

- cleanest high-pressure mixed compatibility subcase
- concentrates the programme’s hardest current distinctions

## 4. Glass -> Air [Pocket-Dominant]

Frontier value:

- `9`

Why:

- strongest pocket/pseudo-route release subcase

## 5. Glass -> Crystal [Late-Gate Dominated]

Frontier value:

- `9`

Why:

- cleanest blocked real compatibility route case

## Cluster Contribution Ranking

Highest cluster contribution:

- `glass -> air`
- `glass -> crystal`
- `glass -> crystal [mixed_frontier]`

all at:

- `10`

Why:

- they define the centre of the frontier cluster

Strong cluster contributors:

- `glass -> air [pocket-dominant]`
- `glass -> air [diffuse-dominant]`
- `glass -> crystal [late-gate dominated]`
- `crystal -> air [ordered-return dominated]`

all at:

- `9`

Why:

- each clarifies an important subfamily

## Geometry Maturity

Strongest geometry maturity:

- most major glass frontier cases now score `8`
- polished metal scores `8`
- ordered return subcase scores `8`

Lower but still useful:

- `air -> rough glass`
- `air -> oxidised metal`
- `crystal -> air`

at:

- `7`

Why:

- these are useful and reasonably clear, but would benefit from more material-specific geometry if developed further

## Notation Clarity

The notation is working well.

Most cases score:

- `9`

Cases scoring:

- `8`

are not weak, but carry more mixed or bridge-role ambiguity:

- `air -> rough glass`
- `air -> oxidised metal`
- `crystal -> air`

## Strongest Overall Cases

If the programme needed only a minimal benchmark set, the current strongest overall cases would be:

### Anchor set

- `air -> glass`
- `air -> polished metal`
- `air -> oxidised metal`
- `crystal -> air [ordered-return dominated]`

### Frontier set

- `glass -> air`
- `glass -> air [pocket-dominant]`
- `glass -> air [diffuse-dominant]`
- `glass -> crystal`
- `glass -> crystal [late-gate dominated]`
- `glass -> crystal [mixed_frontier]`

This ten-case set would preserve almost all the current interface programme’s useful discrimination.

## Weakest Current Cases

No case is useless, but the least mature are:

- `air -> rough glass`
- `crystal -> air`
- `air -> oxidised metal`

Reason:

- each is useful, but could benefit from more specific material geometry if the programme returns to them

## Strategic Findings

## 1. The Expanded Library Is Balanced Enough to Pause Expansion

This is the main result.

The library now has:

- anchors
- frontiers
- bridge cases
- degradation contrasts
- return-side comparisons

It does not need immediate broadening just to feel complete.

## 2. Glass Remains the Core Frontier

Again this is reinforced.

The highest frontier and cluster-contribution scores belong to the glass family.

## 3. The Return-Side Cluster Is Now Much Healthier

The ordered-return dominated crystal subcase was worth adding.

It prevents polished metal from carrying return-side logic alone.

## 4. The Next Major Step Should Not Be More Interface Subcases

The library is now good enough to support a move back toward:

- element/material coverage
- or a more formal mathematical/geometry sketch

rather than continued subcase expansion.

## Confidence

- confidence that the expanded library is now structurally balanced enough: `8/10`
- confidence that the scoring identifies the right anchors and frontiers: `8/10`
- confidence that immediate broad subcase expansion should pause: `9/10`
- confidence that the next step should return toward element/material coverage or formal geometry: `8/10`

## Recommendation

Pause interface subcase expansion.

Use this expanded library as the standard interface modelling toolkit for the next research phase.

## Next Move

The best next artifact is:

- `ams-element-material-coverage-plan-v1.md`

That should define how to resume the original larger aim:

- element-by-element
- molecule/material by molecule/material

while using the new interface notation and route/obstruction framework as a reusable modelling layer.*** End Patch
