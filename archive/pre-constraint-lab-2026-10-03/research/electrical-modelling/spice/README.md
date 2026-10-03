# AMS High-Frequency AC SPICE Starter Models

## Purpose

These circuits support:

`research/ams-high-frequency-ac-spice-modelling-plan-v1.md`

They are classical SPICE models. They do not model `T0`, vortons, or substrate ontology directly.

The aim is to compare secondary material route behaviours and interpret the outputs through AMS-facing variables:

```text
Q_even_f
Q_even_A
B_bottle
K_store
J_bound
J_trans
Phi_lag
L_leak
X_frag
```

## Running

With `ngspice` installed:

```text
ngspice -b 01_baseline_resistor.cir
```

Or run the full starter set:

```text
bash run-all.sh
```

Each file writes a small `.csv` output where practical.

## Interpretation

Use `results-template.md` to record:

- what was varied
- what classical behaviour appeared
- which AMS variable best explains the difference
- whether same-total-impedance routes behaved differently
- whether constraint was distributed or concentrated

Use `interpretation-guide.md` for the first comparisons to run.

## Guardrail

No component in these files should be interpreted as a substrate cell or vorton.

The files operate at the `T2` equivalent-circuit level only.
