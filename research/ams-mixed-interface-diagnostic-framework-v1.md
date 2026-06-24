# AMS Mixed Interface Diagnostic Framework v1

## Purpose

This document condenses the recent interface work into a practical diagnostic framework.

The programme now has:

- refined interface variables
- loop families
- route classes
- route-reality criteria and grades
- obstruction-character classes
- mixed-subregion zone logic
- transition-likelihood judgments

That is enough structure that the next need is not more immediate taxonomy, but a compact way to diagnose what sort of mixed interface is actually being modelled.

## Core Question

Given a real or hypothesised interface case:

- which zones are present?
- which zone dominates?
- which transitions are most likely?
- what whole-interface outcome should currently be expected?

This framework answers those questions in a first-pass way.

## Active Core Layers

### Primitive Variables

- `B_in`
- `B_out`
- `J_bound`
- `J_trans`
- `Q_coh`
- `D`

### Derived Term

- `I_comp`

### Geometric Descriptors

- `L_depth`
- `L_span`
- `L_loop`
- `L_escape`

### Main Local Zones

- Zone A: route-dominant zone
- Zone B: pocket-dominant zone
- Zone C: diffusing fringe

### Main Dominance Modes

- `D1` route-dominant
- `D2` pocket-dominant
- `D3` diffusion-dominant
- `D4` mixed competitive

## Diagnostic Sequence

The framework should be used in the following order.

## Step 1: Identify the Main Local Zones Present

Ask:

1. Is there a genuine route-bearing zone?
2. Is there a bounded local pocketing zone?
3. Is there a diffusing fringe?

### Quick Signs

Route zone likely present when:

- one path has real completion-side leverage
- `L_escape` is genuinely present
- `J_trans` is at least moderate

Pocket zone likely present when:

- local activity is strong and bounded
- looping is dominant or near-dominant
- apparent progress exceeds real route viability

Diffusing fringe likely present when:

- route dominance weakens broadly
- no one bounded local structure dominates
- continuation broadens rather than sharpens

## Step 2: Judge Which Zone Has Dominance

Use the four weighting questions:

1. Which zone captures the event most strongly?
2. Which zone controls the strongest viable route?
3. Which zone sustains its logic the longest?
4. Which zone suppresses rival outcomes most effectively?

### Dominance Heuristic

If one zone wins clearly on both:

- event capture
- and outcome leverage

then treat the interface as mostly dominated by that zone.

If no zone wins clearly, treat the interface as:

- `D4` mixed competitive

## Step 3: Test Route Reality

Ask the five route-reality questions:

1. Does the event preserve forward continuity?
2. Does it preserve directional commitment?
3. Does it remain viable under actual progression?
4. Does progression dominate over local looping?
5. Does completion remain a live outcome?

### Outcome

If most answers are strong:

- real route present

If mixed:

- weak or blocked route

If mostly weak and local activity dominates:

- pseudo-route or diffuse field more likely

## Step 4: Identify the Obstruction Character

Ask:

1. Is one route being selectively preserved? -> `O1`
2. Is a route preserved and then blocked late? -> `O2`
3. Is local pocketing preserving activity but weakening onward continuity? -> `O3`
4. Is the route field biased toward inward return? -> `O4`
5. Is route dominance broadening without total collapse? -> `O5`
6. Is route coherence breaking into fragmented fields? -> `O6`

### Diagnostic Use

This step explains why the current route logic is taking its current form.

Best current shortcut:

- `O2` tends toward `R3`
- `O3` tends toward `R5`
- `O4` tends toward `R4`
- `O5` tends toward `R2`
- `O6` tends toward `R6`

## Step 5: Estimate the Most Likely Transition Flow

Ask:

1. Is the event likely to stay route-led? -> `A -> completion`
2. Is route logic decaying into pocket capture? -> `A -> B`
3. Is route logic broadening into diffusion? -> `A -> C`
4. Is pocket logic self-sustaining? -> `B -> B`
5. Is pocket logic bleeding into diffuse fringe? -> `B -> C`
6. Is the whole case mixed and unresolved? -> `D4`

### Strongest Current Dynamic Clues

- `A -> B` is one of the main frontier transitions
- `B -> B` and `B -> C` are the key pocket dynamics
- `D4 -> B` is often more likely than `D4 -> A` in frontier glass cases

## Step 6: Assign Whole-Interface Outcome

After the earlier steps, assign the whole-interface outcome provisionally as:

### Mostly Route-Dominant

When:

- a real route remains strongest
- pocket capture is secondary
- diffusion does not dominate

### Mostly Pocket-Dominant

When:

- local bounded reseating governs the event
- route reality is weak or decaying
- pseudo-progression dominates

### Mostly Diffuse

When:

- route and pocket structures both weaken
- broad degraded continuation dominates

### Genuinely Mixed Competitive

When:

- route, pocket, and/or fringe logics all remain active
- no one local logic secures clear dominance

This last category should be used seriously, not as a vague fallback.

## Compact Decision Tree

### Question 1

Is there a genuinely completion-directed route?

- yes -> go to Question 2
- no -> go to Question 4

### Question 2

Is the route still strongest, or is local pocketing taking over?

- route strongest -> mostly route-dominant
- pocketing taking over -> mixed competitive or route -> pocket transition

### Question 3

Is the route failing late or completing?

- completing -> `R1` / successful handoff
- failing late -> `R3` / `O2`

### Question 4

Is local activity bounded and loop-dominant?

- yes -> pocket-dominant / `R5` / `O3`
- no -> go to Question 5

### Question 5

Is route coherence broadly weakening without one bounded local pocket dominating?

- yes -> mostly diffuse / `R2` or `R6` / `O5` or `O6`
- no -> mixed competitive

## Benchmark-Specific Quick Reads

## Air -> Glass

Best current read:

- mostly route-dominant
- with weak selective funnelling

## Glass -> Air

Best current read:

- often pocket-dominant or mixed competitive

Why:

- blocked routes
- pseudo-routes
- diffuse fringes

can all coexist.

## Air -> Polished Metal

Best current read:

- strongly route-real but inward-biased

This is the clearest reflection-side anchor.

## Air -> Oxidised Metal

Best current read:

- diffusion-dominant or fragmentation-adjacent

## Glass -> Crystal

Best current read:

- either route-dominant in selective regions
- or mixed competitive in frontier regions

## Crystal -> Air

Best current read:

- mostly route-dominant or inward-return biased

## Strongest Current Use Cases

This framework is most useful when:

- several local behaviours seem present at once
- the interface looks internally inconsistent
- the event seems to shift from genuine route to pseudo-route or diffuse failure

It is less necessary when the case is already very clean, such as:

- idealised polished-metal reflection

## Strongest Current Diagnostic Judgments

## 1. Glass Cases Are the Best Stress Tests

This is still the strongest general conclusion.

They allow:

- route reality
- route failure
- pseudo-route activity
- pocket capture
- diffusion

to coexist in one family of cases.

## 2. Route Reality Must Be Tested Before Looping Is Interpreted

This is another major stabilising result.

If the programme asks about looping first, it risks mistaking:

- active local motion

for:

- viable route structure

## 3. Obstruction Character Explains Why the Route Looks the Way It Does

This is the main value of the obstruction layer.

It connects:

- interface geometry
- route logic
- outcome tendency

## 4. Mixed Competitive Should Be Used Positively, Not as a Dumping Ground

This matters because many frontier cases are genuinely mixed.

That is a strength of the model, not a weakness.

## Current Weak Point

The framework is now practical, but it still needs one final tightening step:

- worked examples that run the full diagnostic chain from start to finish

That is the obvious next move if the framework is going to be used repeatedly rather than admired abstractly.

## Confidence

- confidence that the framework is now practically usable: `8/10`
- confidence that the diagnostic sequence is the right order: `8/10`
- confidence that mixed competitive is now a legitimate positive diagnosis: `8/10`
- confidence that no new primitive split is needed yet: `8/10`

## Recommendation

Keep the current framework unchanged.

The next gains should come from worked diagnostics, not more immediate abstraction.

## Next Move

The best next artifact is:

- `ams-mixed-interface-worked-examples-v1.md`

That should run the full diagnostic framework step by step on the strongest benchmark cases:

- `glass -> air`
- `glass -> crystal`
- `air -> oxidised metal`

so the framework becomes fully operational.*** End Patch
