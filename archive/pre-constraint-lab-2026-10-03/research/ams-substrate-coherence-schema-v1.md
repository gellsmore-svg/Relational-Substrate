# AMS Substrate Coherence Schema v1

## Purpose

This schema is the working record format for the AMS substrate coherence programme.

It is designed to stop the research from drifting into loose prose, hidden assumptions, or fake precision.

## Shared Fields

Every record should contain:

- `Record ID`
- `Workstream`
- `Tree anchor`
- `Scale`
- `Case name`
- `Observed description`
- `Observed source notes`
- `AMS interpretation`
- `Competing thin explanation`
- `Confidence`
- `Confidence score (1-10)`
- `Open questions`

## Confidence Scale

Use four levels only:

- `Observed`: direct conventional chemistry or material behaviour
- `Strong AMS inference`: AMS mapping is coherent and tightly constrained
- `Conjectural AMS extension`: plausible but not strongly constrained
- `Open`: unresolved or currently weak

## Confidence Score Scale

Use a `1-10` score alongside the qualitative label.

- `1-2`: barely formed, mostly placeholder
- `3-4`: weak, possible but underconstrained
- `5-6`: moderate, coherent first-pass mapping
- `7-8`: strong, comparatively well-supported within the current corpus
- `9`: very strong, unusually coherent across multiple comparisons
- `10`: reserved for cases that remain exceptionally strong after repeated pressure

Early pilot scores should usually cluster in the `4-7` range.

The score should be revised as:

- more T1B cases are added
- non-persistent topology interactions become clearer
- T1C stress tests expose scaling success or failure

## T1B Entry Schema

- `Element`
- `Formation name`
- `Formula`
- `Structure type`
- `Bonding mode`
- `Geometry / symmetry`
- `Persistence conditions`
- `Phase tendencies`
- `Reactivity profile`
- `Threshold notes`
- `Closure type`
- `Coupling type`
- `Lock-up conditions`
- `Slip tolerance`
- `Strain distribution`
- `Return-path viability`
- `Higher-order tendency`

## Non-Persistent Topology Schema

- `Topology class`
- `Definition`
- `Failure mechanism`
- `Runtime signature`
- `Threshold dependence`
- `Temporary persistence mode`
- `Interaction with stable T1B cases`
- `Catalytic or destabilising role`
- `Likely T1C consequences`

## T1C Entry Schema

- `Formation type`
- `Constituent basis`
- `Boundary significance`
- `Persistence profile`
- `Memory behaviour`
- `Threshold behaviour`
- `Failure modes`
- `Redistribution behaviour`
- `Part-replacement tolerance`
- `Higher-order identity assessment`
- `Status`
  - aggregate only
  - marginal whole
  - stable higher-order whole
  - kind-bearing whole

## Required Comparison Questions

Each record must answer:

1. What is directly observed?
2. What does conventional chemistry or materials science already explain here?
3. What does AMS explain differently?
4. Does AMS reduce fragmentation or merely rename it?
5. Does the case support stable identity, unstable identity, or higher-order identity?

## Minimal Pilot Workflow

For each pilot element:

1. Choose representative T1B cases.
2. Record conventional structure first.
3. Map AMS closure and coupling grammar.
4. Compare against non-persistent topology classes.
5. Identify the best T1C escalation cases.

This schema should be used before scaling the programme.
