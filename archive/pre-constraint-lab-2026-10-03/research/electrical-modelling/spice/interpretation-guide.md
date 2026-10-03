# AMS SPICE Output Interpretation Guide

## Purpose

This guide explains how to read the starter SPICE outputs through AMS-facing variables.

The simulations remain classical equivalent-circuit models. The AMS work is in how the outputs are decomposed:

```text
same total response
-> different internal distribution
-> different constraint, storage, boundary, and evenness profile
```

## Raw Output Note

`ngspice wrdata` repeats the sweep variable alongside each requested vector.

For AC outputs, values are complex, so columns usually appear in repeated groups:

```text
frequency real imag
```

For transient outputs, values are real, so columns usually appear in repeated pairs:

```text
time value
```

The first job is not polished plotting. It is comparison.

## First Comparison: Distributed vs Concentrated Storage

Use:

```text
03_distributed_rc_ladder.cir
04_concentrated_interface_lockup.cir
08_same_impedance_different_distribution.cir
```

Ask:

- Which route holds output amplitude flatter for longer?
- Which route accumulates more phase lag?
- Which route shows stronger interface/node stress?
- Does the concentrated interface route degrade earlier?

AMS reading:

```text
distributed storage -> lower local P_stress, potentially higher Q_even
concentrated storage -> higher B_bottle/J_bound stress, potentially lower Q_even
```

## Second Comparison: Bottleneck Stress

Use:

```text
05_bottleneck_route.cir
```

Change:

```text
RGOOD=100, 10, 1
RBOT fixed
```

Ask:

- Does the route improve globally while stress concentrates around `Rbottle`?
- Does the bottleneck parasitic capacitance dominate high-frequency behaviour?

AMS reading:

```text
lower non-bottleneck resistance can increase effective pressure at the bottleneck
```

## Third Comparison: Boundary Return

Use:

```text
06_transmission_line_mismatch.cir
```

Change:

```text
RLOAD=50, 25, 100, 200, 1Meg
```

Ask:

- Which termination gives the flattest response?
- Which creates the strongest ripple or phase irregularity?

AMS reading:

```text
poor J_bound -> boundary return -> lower Q_even
```

## Fourth Comparison: Amplitude-Conditioned Storage/Leakage

Use:

```text
07_nonlinear_dielectric_proxy.cir
```

Change:

```text
AMP=0.1, 1, 5, 10
BETA=0, 0.01, 0.05, 0.1
```

Ask:

- Does output shape change with amplitude?
- Does leakage become more significant under stronger drive?

AMS reading:

```text
route storage/release is no longer amplitude-even
Q_even_A falls as nonlinear leakage rises
```

## AMS Variable Checklist

| Variable | Look For |
|---|---|
| `Q_even_f` | flat response across frequency |
| `Q_even_A` | stable response across amplitude |
| `B_bottle` | one component/node dominating stress |
| `K_store` | capacitance or delayed release |
| `J_bound` | termination/contact/interface quality |
| `J_trans` | smooth route continuity |
| `Phi_lag` | phase delay or group delay |
| `L_leak` | dissipative loss |
| `X_frag` | distortion, ripple, irregularity, harmonic content |

## Guardrail

Do not read any circuit element as a substrate object.

The interpretation layer is:

```text
equivalent circuit behaviour
-> AMS route variables
-> design heuristics for secondary material regimes
```

