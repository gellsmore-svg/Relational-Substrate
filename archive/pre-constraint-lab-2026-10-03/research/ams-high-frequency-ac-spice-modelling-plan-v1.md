# AMS High-Frequency AC SPICE Modelling Plan v1

## Purpose

This note turns the AMS high-frequency AC modelling entry into a practical simulation plan.

The goal is not to prove AMS in SPICE. SPICE is a classical circuit solver. The goal is to use SPICE to compare equivalent electrical routes and then interpret the differences through AMS-facing variables:

```text
Q_even
B_bottle
K_store
J_bound
J_trans
L_leak
X_frag
Phi_lag
P_stress
```

The central question is:

```text
can AMS-guided decomposition reveal constraint, storage, interface, and evenness differences
that simple lumped totals hide?
```

## Modelling Guardrail

This file models secondary material regimes, not `T0` directly.

The corrected AMS chain remains:

```text
continuous substrate
-> local organised disturbance
-> torsion/tension/alignment expression
-> candidate closure-pattern
-> stable primary topology/vorton
-> coupled vorton regimes
-> secondary material regimes
-> perceived matter
```

SPICE operates at the `T2` representation level:

```text
secondary material route behaviour
-> equivalent circuit
-> frequency/amplitude response
-> AMS interpretive variables
```

No SPICE component should be treated as a substrate cell or vorton.

## Core Hypothesis

For high-frequency AC, route quality is not captured by total impedance alone.

AMS predicts that routes with the same nominal impedance can differ materially in:

- frequency evenness
- amplitude evenness
- phase lag distribution
- interface stress
- bottleneck stress
- storage/release quality
- loss concentration
- failure tendency

The first useful test is therefore:

```text
same total impedance, different internal distribution
```

## Common Observables

For every circuit, record:

```text
|Z(f)|        impedance magnitude
phase(f)     phase angle
gain(f)      output/input amplitude
delay(f)     phase-derived or group-delay proxy
P_loss(x)    power loss by component or region
V_stress(x)  local voltage stress
I_stress(x)  local current stress
THD proxy    harmonic distortion where nonlinear elements are used
```

AMS-derived summary variables:

```text
Q_even_f     evenness across frequency
Q_even_A     evenness across amplitude
B_bottle     largest normalised local stress
K_store      total and local storage capacity
J_bound      inferred interface continuity quality
J_trans      inferred route continuity quality
Phi_lag      phase lag and where it concentrates
L_leak       dissipative loss tendency
X_frag       distortion/noise/incoherent breakup proxy
```

## Suggested Sweep Ranges

Use broad ranges first, then narrow around interesting transitions.

Frequency:

```text
10 Hz -> 100 MHz
```

or, if the simulator/model is simple enough:

```text
1 Hz -> 1 GHz
```

Amplitude:

```text
10 mV
100 mV
1 V
5 V
10 V
```

For nonlinear experiments, include enough amplitude range to reveal state dependence.

## Circuit 1: Baseline Pure Resistor

### Purpose

Establish the control case.

### Circuit

```text
Vin -> R -> ground
```

### Expected Classical Behaviour

- impedance mostly flat
- phase near zero
- loss entirely resistive

### AMS Interpretation

```text
R_route high or low depending on R
K_store minimal
Phi_lag minimal
Q_even high across frequency if parasitics omitted
```

### Use

This is the clean baseline. It is not realistic at high frequency, but it anchors the comparison.

## Circuit 2: Resistor With Parasitic Capacitance

### Purpose

Show how storage changes route behaviour even when nominal resistance is unchanged.

### Circuit

```text
Vin -> R -> output
output -> C_parasitic -> ground
```

### Sweep

Vary:

```text
C_parasitic = 1 pF, 10 pF, 100 pF, 1 nF
```

### Expected Classical Behaviour

- low-pass behaviour
- increasing phase lag
- high-frequency attenuation

### AMS Interpretation

```text
K_store increases
Phi_lag increases
Q_even decreases at high frequency
route response becomes storage-limited
```

### AMS Question

Does the route remain even across the intended frequency range, or does storage dominate?

## Circuit 3: Distributed RC Ladder

### Purpose

Compare distributed storage/loss with concentrated storage/loss.

### Circuit

Use an `N`-section ladder:

```text
Vin -> R1 -> R2 -> R3 -> ... -> RN -> output
        |     |     |           |
        C1    C2    C3          CN
        |     |     |           |
      ground ground ground     ground
```

### Sweep

Compare:

```text
N = 1, 3, 10, 30
same total R
same total C
```

### Expected Classical Behaviour

- distributed delay
- smoother phase behaviour as sections increase
- different attenuation shape from one lumped RC

### AMS Interpretation

```text
distributed K_store
lower local P_stress
potentially higher Q_even than concentrated lock-up
```

### AMS Question

Does distributing storage improve frequency evenness compared with one equivalent lumped capacitance?

## Circuit 4: Concentrated Interface Lock-Up

### Purpose

Model a route where the same total storage is concentrated at one boundary.

### Circuit

```text
Vin -> R_left -> node_interface -> R_right -> output
node_interface -> C_interface -> ground
```

Compare with the distributed RC ladder using:

```text
R_left + R_right = total ladder R
C_interface = total ladder C
```

### Expected Classical Behaviour

- same simple total values may not produce same frequency/phase behaviour
- local node stress at interface
- stronger frequency-dependent phase concentration

### AMS Interpretation

```text
J_bound lower
K_store concentrated
P_stress concentrated
B_bottle higher
Q_even lower than distributed case if interface dominates
```

### AMS Question

Can two routes with the same total resistance and capacitance differ in evenness because one concentrates storage at an interface?

## Circuit 5: Bottleneck In Otherwise Good Route

### Purpose

Test the theory-of-constraints point in an AC setting.

### Circuit

```text
Vin -> R_good1 -> R_bottle -> R_good2 -> output
```

Add optional parasitics around `R_bottle`:

```text
R_bottle parallel C_bottle
R_bottle series L_bottle
```

### Sweep

Keep `R_bottle` fixed and reduce `R_good1` and `R_good2`.

### Expected Classical Behaviour

- total resistance drops until bottleneck dominates
- local power/stress concentrates at bottleneck
- parasitics create frequency-dependent effects

### AMS Interpretation

```text
B_bottle rises as non-bottleneck route improves
P_stress concentrates
Q_even may degrade if bottleneck has parasitic storage or inductive discontinuity
```

### AMS Question

Does improving the rest of the route increase stress and distortion at the bottleneck?

## Circuit 6: Transmission Line With Termination Mismatch

### Purpose

Model high-frequency route delay, reflection, and boundary return.

### Circuit

Use a lossy transmission line model:

```text
Vin -> transmission line -> R_load
```

Compare:

```text
matched termination
under-terminated
over-terminated
open-like termination
short-like termination
```

### Expected Classical Behaviour

- reflections under mismatch
- standing-wave-like behaviour
- frequency-dependent gain and phase

### AMS Interpretation

```text
J_trans = route continuity through line
J_bound = termination quality
boundary return increases when J_bound is poor
Q_even falls under reflection-heavy cases
```

### AMS Question

Can boundary return be treated as route incompatibility rather than only a terminal impedance fact?

## Circuit 7: Nonlinear Dielectric Proxy

### Purpose

Model amplitude-dependent storage and release.

### Circuit

Use a voltage-dependent capacitor or behavioural capacitance:

```text
C(V) = C0 * (1 + alpha * V^2)
```

or a piecewise capacitor if the simulator supports it.

### Sweep

Sweep amplitude at fixed frequencies, then sweep frequency at fixed amplitudes.

### Expected Classical Behaviour

- amplitude-dependent phase and gain
- possible distortion
- harmonic generation in transient simulations

### AMS Interpretation

```text
K_store depends on route pressure
Q_even_A decreases
Phi_lag becomes amplitude-dependent
X_frag rises if distortion appears
```

### AMS Question

Does stored mismatch release evenly, or does the route become amplitude-conditioned?

## Circuit 8: Same Impedance, Different Distribution

### Purpose

This is the core AMS comparison.

### Build Two Or More Routes

Route A:

```text
distributed mild loss and storage
```

Route B:

```text
same total loss and storage concentrated at one interface
```

Route C:

```text
same total impedance with one bottleneck plus otherwise excellent route
```

### Expected Classical Behaviour

Depending on construction, simple totals can match while frequency response, phase, and local stress differ.

### AMS Interpretation

```text
same total impedance does not imply same route quality
Q_even, B_bottle, J_bound, and Phi_lag separate the designs
```

### AMS Question

Which design gives the most even response across the operating frequency and amplitude range?

## Scoring Table

For each circuit, score:

| Variable | Meaning | Classical proxy |
|---|---|---|
| `Q_even_f` | frequency evenness | flatness of gain/phase/impedance |
| `Q_even_A` | amplitude evenness | stability across amplitude sweep |
| `B_bottle` | strongest constraint | max local power or voltage/current stress |
| `K_store` | storage/lock-up | capacitance, stored energy, delayed release |
| `J_bound` | interface quality | reflection, contact loss, local phase jump |
| `J_trans` | route continuity | attenuation, delay smoothness |
| `Phi_lag` | delayed reseating | phase lag, group delay |
| `L_leak` | dissipative loss | heat/power loss |
| `X_frag` | incoherent breakup | distortion, noise proxy, harmonic content |

## Expected AMS-Relevant Result

The expected result is not:

```text
SPICE proves AMS
```

The expected result is:

```text
AMS gives a disciplined way to ask which equivalent route is more even,
less bottlenecked, less interface-stressed, and less storage-distorted
across frequency and amplitude
```

If this proves useful, AMS has changed the modelling emphasis in a materially relevant way.

## Practical Next Step

Build a small repository folder for the simulations:

```text
research/electrical-modelling/spice/
```

Suggested files:

```text
README.md
01_baseline_resistor.cir
02_resistor_parasitic_cap.cir
03_distributed_rc_ladder.cir
04_concentrated_interface_lockup.cir
05_bottleneck_route.cir
06_transmission_line_mismatch.cir
07_nonlinear_dielectric_proxy.cir
08_same_impedance_different_distribution.cir
results-template.md
```

The next useful research note is an interpretation guide for reading SPICE outputs through AMS variables.

