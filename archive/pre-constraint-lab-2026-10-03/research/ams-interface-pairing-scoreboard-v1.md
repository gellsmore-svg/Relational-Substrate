# AMS Interface Pairing Scoreboard v1

## Purpose

This document ranks the current real interface pairings from:

- `ams-real-interface-pairings-v1.md`

The aim is to decide which pairings are currently:

- strongest as explanatory benchmarks
- clearest in variable structure
- most mature geometrically
- most useful for the next experimental pass

This is a steering document. It is meant to stop the interface programme from trying to deepen every frontier at once.

## Scoring Criteria

Each pairing is scored from `1-10` on four dimensions:

- `Explanatory strength`
  - how well the current AMS interface model gives a coherent account of the pairing
- `Variable clarity`
  - how clearly the current variables discriminate the outcome
- `Geometry maturity`
  - how far the geometric picture has progressed beyond verbal summary
- `Next-step usefulness`
  - how useful the pairing is for the next round of model refinement

These are not truth scores. They are programme-steering scores.

## Scoreboard

| Pairing | Explanatory strength | Variable clarity | Geometry maturity | Next-step usefulness | Notes |
|---|---:|---:|---:|---:|---|
| air -> glass | 8 | 8 | 7 | 9 | strongest current handoff benchmark |
| glass -> air | 7 | 7 | 6 | 8 | strongest practical `B_out` test so far |
| air -> crystal | 8 | 8 | 7 | 8 | best ordered-entry benchmark |
| crystal -> air | 7 | 7 | 6 | 8 | strong exit-side case, but still underdeveloped |
| air -> polished metal | 8 | 9 | 7 | 9 | strongest current reflection benchmark |
| air -> oxidised metal | 8 | 8 | 7 | 9 | strongest boundary-layer degradation benchmark |
| glass -> metal | 7 | 8 | 6 | 8 | strong mixed transmission/reflection case |
| glass -> crystal | 7 | 7 | 5 | 10 | strongest current `I_comp` pressure case |

## Ranking by Immediate Value

## Tier 1: Highest Immediate Value

### 1. Glass -> Crystal

Why it ranks first for next-step usefulness:

- it pressures `I_comp` directly
- both wholes are transmissive
- the difficulty is not transmission versus reflection, but transmission grammar versus transmission grammar
- it exposes whether the current interface model can handle cross-whole compatibility rather than only success versus failure

Why it is not yet the strongest overall case:

- geometry maturity is still only `5`
- current explanation is promising but still partly schematic

### 2. Air -> Glass

Why it remains central:

- it is the cleanest handoff case in the entire current programme
- it supports the glass-transmission model directly
- it helps stabilise `B_in`, `I_comp`, `R`, and `S`

This is not the weakest problem, but it is still one of the best anchors.

### 3. Air -> Polished Metal

Why it remains central:

- it is the cleanest reflection benchmark
- variable clarity is highest here
- it stabilises the reflection-side interpretation of:
  - weak admission
  - strong boundary response
  - structured return

This is one of the strongest anchor cases in the whole optical programme.

### 4. Air -> Oxidised Metal

Why it ranks highly:

- it tests whether the model can preserve metallic identity while degrading reflective behaviour
- it makes surface-layer ontology unavoidable
- it is the strongest current bridge between interface logic and material degradation

## Tier 2: Strong but Not Yet Decisive

### 5. Air -> Crystal

This remains a very strong ordered-entry benchmark, but it is slightly less strategically urgent than air -> glass because:

- crystal-style admission is already conceptually cleaner
- the glass side still carries more unresolved distributed-permissive complexity

### 6. Glass -> Air

This is the most practical exit-side case.

It ranks below the leading pairings because:

- release geometry is still less mature than entry geometry
- the model still handles admission more sharply than release

### 7. Crystal -> Air

This is conceptually important, but still dependent on underdeveloped boundary-relaxation geometry.

It should be revisited soon, but it is not the most productive next deep pass.

### 8. Glass -> Metal

This is a good mixed case, but not yet the sharpest frontier.

It is useful because:

- the source whole is transmissive
- the receiving whole is strongly reflective

But it is partly derivative of stronger anchor cases:

- air -> glass
- air -> polished metal

## Cross-Score Findings

## 1. Anchor Cases and Frontier Cases Are Different

The strongest anchor cases are:

- air -> glass
- air -> polished metal
- air -> oxidised metal

The strongest frontier case is:

- glass -> crystal

This distinction matters.

Anchor cases stabilise the model.
Frontier cases expose where it is still weak.

## 2. Entry-Side Cases Still Outperform Exit-Side Cases

The scoreboard confirms an earlier trend:

- entry geometry is currently more mature than exit geometry

This does not mean exit is less important. It means the next deepening pass should avoid trying to solve both at full depth simultaneously unless one of the pairings forces it.

## 3. Surface-Layer Ontology Is Now Non-Optional

The polished-metal and oxidised-metal pairings together show that:

- bulk identity
- surface-layer behaviour

must be treated distinctly.

This is now no longer a side detail.

## 4. `I_comp` Now Has a Clear Main Test Case

If `I_comp` is to survive, the case that will justify it is:

- glass -> crystal

That is the pairing where the interface problem is hardest to reduce to:

- simple admission failure
- simple reflection
- simple defect burden

## Recommendation

Do not deepen everything at once.

The best next pass is:

## Primary deepening target

- `glass -> crystal`

Reason:

- strongest current compatibility frontier
- strongest direct test of `I_comp`
- highest next-step usefulness score

## Secondary anchor-maintenance targets

- `air -> glass`
- `air -> polished metal`
- `air -> oxidised metal`

Reason:

- they keep the broader model stable while the harder compatibility case is deepened

## What Not To Prioritise Next

Do not make the next main pass:

- glass -> metal
- crystal -> air

These remain useful, but neither currently pressures the model as efficiently as glass -> crystal.

## Confidence

- scoreboard usefulness confidence: `9/10`
- confidence in the anchor/frontier distinction: `9/10`
- confidence that glass -> crystal should be the next main deepening target: `8/10`

## Next Move

The most useful next artifact is:

- `ams-glass-to-crystal-compatibility-study-v1.md`

That should focus on:

- distributed permissive order meeting structured nested order
- whether `I_comp` can be derived cleanly from current variables
- what geometric features of the interface matter most
- whether the current variable set needs one more split before it can handle cross-transmissive handoff sharply
