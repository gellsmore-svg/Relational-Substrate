# AMS Optical Numeric Benchmark Table v1

## Purpose

This file adds the first numeric benchmark values to the AMS optical route model.

It covers:

- air to fused silica reflectance at normal and oblique incidence
- `s` and `p` polarisation differences
- representative normal-incidence metal reflectance at 550 nm
- representative metal skin depth at 550 nm
- AMS route-class assignment for each case

This moves the optical model from qualitative mechanism into testable numeric comparison.

## Source Basis

Primary source anchors:

- HyperPhysics, "Fresnel's Equations." https://hyperphysics.phy-astr.gsu.edu/hbase/phyopt/freseq.html
- Physics LibreTexts, "Reflection and Transmission at Boundaries and the Fresnel Equations." https://phys.libretexts.org/Bookshelves/Optics/Physical_Optics_%28Tatum%29/02%3A_Reflection_and_Transmission_at_Boundaries_and_the_Fresnel_Equations
- RefractiveIndex.INFO, fused silica and metal optical constants database. https://refractiveindex.info/
- Johnson and Christy, "Optical constants of the noble metals." https://doi.org/10.1103/PhysRevB.6.4370
- Johnson and Christy, "Optical constants of transition metals." https://doi.org/10.1103/PhysRevB.9.5056
- Rakic et al., "Optical properties of metallic films for vertical-cavity optoelectronic devices." https://doi.org/10.1364/AO.37.005271
- Babar and Weaver, "Optical constants of Cu, Ag, and Au revisited." https://doi.org/10.1364/AO.54.000477

## Data Caveat

The metal values below are representative working values near:

```text
wavelength: 550 nm
medium 1: air, n = 1
incidence: normal unless otherwise stated
```

They are not final reference values.

Metal optical constants vary with:

```text
dataset
surface quality
film thickness
oxidation
tarnish
grain structure
annealing
temperature
measurement method
```

Use this table as a first AMS benchmark, not as a precision optics design table.

## Equations Used

### Dielectric Fresnel Coefficients

For air to fused silica:

```text
n1 = 1.000
n2 = 1.459
```

Snell's law:

```text
n1 sin(theta_i) = n2 sin(theta_t)
```

Reflectance:

```text
R_s = |r_s|^2
R_p = |r_p|^2
R_avg = (R_s + R_p) / 2
```

### Normal-Incidence Metal Reflectance

For complex refractive index:

```text
N = n + i k
```

normal-incidence reflectance from air:

```text
R = ((n - 1)^2 + k^2) / ((n + 1)^2 + k^2)
```

### Skin Depth

Approximate optical skin depth:

```text
delta = lambda / (4 pi k)
```

with:

```text
lambda = 550 nm
```

## Benchmark 1: Air to Fused Silica

Assumptions:

```text
n_air = 1.000
n_fused_silica = 1.459
non-absorbing clean interface
no roughness / coating / contamination correction
```

| Incidence angle | Transmitted angle | `R_s` | `R_p` | `R_avg` | AMS route class |
|---:|---:|---:|---:|---:|---|
| 0 deg | 0.00 deg | 0.0348 | 0.0348 | 0.0348 | balanced clean admission |
| 30 deg | 20.04 deg | 0.0509 | 0.0216 | 0.0363 | `s` return rises, `p` return falls |
| 45 deg | 28.99 deg | 0.0823 | 0.0068 | 0.0446 | near Brewster-side `p` admission |
| 60 deg | 36.41 deg | 0.1622 | 0.0024 | 0.0823 | high `s` return, strong `p` admission |

### AMS Reading

At normal incidence:

```text
R_avg ~= 3.48 percent
T_avg ~= 96.52 percent
```

Route interpretation:

```text
clean air -> fused silica
=> high B_in
=> high J_bound
=> low D
=> most route admitted
=> small unavoidable route-return from delay contrast
```

At oblique incidence:

```text
s and p routes separate.
```

AMS interpretation:

```text
polarisation changes boundary-coupling geometry.
```

The `p` route approaches a low-reflection condition near Brewster geometry, while the `s` route returns more strongly as angle increases.

## Benchmark 2: Representative Metals at 550 nm

Representative working optical constants:

| Metal | `n` | `k` | Reflectance `R` | Skin depth `delta` | AMS route class |
|---|---:|---:|---:|---:|---|
| Ag | 0.14 | 3.98 | 0.967 | 11.0 nm | broad coherent `R1_return` |
| Al | 1.44 | 7.38 | 0.905 | 5.9 nm | strong return, oxide/coating sensitive |
| Au | 0.47 | 2.41 | 0.764 | 18.2 nm | yellow-filtered return |
| Cu | 0.77 | 2.43 | 0.659 | 18.0 nm | red/orange-filtered return |
| Fe | 2.91 | 3.28 | 0.553 | 13.3 nm | weaker return, oxidation-sensitive |

## Metal Benchmark Interpretation

### Silver

Numeric result:

```text
R ~= 96.7 percent
delta ~= 11 nm
```

AMS reading:

```text
very high coherent return
very shallow penetration
excellent clean visible mirror route
```

Route:

```text
R1_return / O2_deep-entry block / D1_return / G_A
```

### Aluminium

Numeric result:

```text
R ~= 90.5 percent
delta ~= 5.9 nm
```

AMS reading:

```text
strong return and very shallow penetration,
but surface oxide/coating layer is route-critical.
```

Route:

```text
R1_return with oxide-gated R3/D4 terminal layer
```

### Gold

Numeric result:

```text
R ~= 76.4 percent at 550 nm
delta ~= 18.2 nm
```

AMS reading:

```text
lower green-region reflectance than silver because spectral absorption/filtering is active.
```

This is consistent with gold's yellow appearance:

```text
blue/violet routes absorbed more strongly
red/yellow-biased routes returned
```

Route:

```text
R1_return + spectral R5/O3 absorption
```

### Copper

Numeric result:

```text
R ~= 65.9 percent at 550 nm
delta ~= 18.0 nm
```

AMS reading:

```text
visible return is spectrally biased rather than neutral.
```

Route:

```text
red/orange-biased R1_return + shorter-wavelength R5/O3 capture
```

### Iron

Numeric result:

```text
R ~= 55.3 percent at 550 nm
delta ~= 13.3 nm
```

AMS reading:

```text
iron has weaker clean visible return than Ag/Al/Au/Cu and is practically dominated by oxidation/roughness in many real surfaces.
```

Route:

```text
R1_return if polished
R5/R6 oxide-dominated in ordinary surfaces
```

## Glass vs Metal Numeric Contrast

| Case | Reflectance at clean normal incidence | AMS route meaning |
|---|---:|---|
| air -> fused silica | 0.0348 | most route admitted into dielectric through-route |
| air -> silver | 0.967 | route overwhelmingly returned |
| air -> aluminium | 0.905 | route strongly returned, shallow skin depth |
| air -> gold | 0.764 | strong but spectrally filtered return |
| air -> copper | 0.659 | coloured / filtered return |
| air -> iron | 0.553 | weaker return, oxidation-sensitive |

AMS summary:

```text
fused silica:
low route return, high through-route

metals:
high route return, shallow lossy entry
```

## Route Confidence Table

| Case | Numeric support | Route assignment confidence | Main limitation |
|---|---|---|---|
| fused silica normal incidence | strong | high | assumes clean uncoated surface |
| fused silica oblique s/p | strong | high | no coating/roughness correction |
| Ag 550 nm | strong representative | moderate-high | tarnish / dataset variation |
| Al 550 nm | strong representative | moderate | oxide/coating layer changes result |
| Au 550 nm | strong representative | moderate-high | spectral curve needed for colour fully |
| Cu 550 nm | moderate | moderate | colour requires multi-wavelength curve |
| Fe 550 nm | moderate | moderate | oxidation and surface state dominate |

## Score Assessment

Optical numeric benchmark table:

```text
score: 8.5/10
confidence: moderate-high
```

Reason:

This table materially strengthens the optical model because it:

- gives real reflectance magnitudes
- shows the fused-silica / metal contrast numerically
- demonstrates polarisation-dependent boundary routes
- includes metal skin-depth estimates
- ties route assignments to quantitative optical constants

Limitations:

- metal constants are representative, not final tabulated reference values
- only one metal wavelength is benchmarked
- no oxide/tarnish/coating correction is applied
- no multi-wavelength colour table is included
- no experimental roughness model is included

## Effect on Optical Master Model

Previous optical route master score:

```text
8.5/10
```

Updated pressure:

```text
retain 8.5/10
confidence strengthened
```

Do not move to 9 yet because:

```text
multi-wavelength metal colour curves
coatings
roughness
oxide layers
plasmonics
Rayleigh scattering
and nonlinear/laser damage
remain unmapped.
```

## Next Artifact

The next useful artifact should be:

```text
ams-optical-colour-and-spectrum-route-table-v1.md
```

Purpose:

Extend the numeric benchmark from one wavelength to spectral behaviour:

- Ag flat visible return
- Au blue absorption / yellow appearance
- Cu short-wavelength absorption / red-orange appearance
- Al UV-visible return with oxide/coating sensitivity
- Fe oxidation and lower visible return
- fused silica UV-visible-IR transmission windows

This will turn colour from a qualitative route-filter claim into a spectral route table.
