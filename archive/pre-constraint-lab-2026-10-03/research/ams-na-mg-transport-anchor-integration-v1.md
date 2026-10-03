# AMS Na/Mg Transport Anchor Integration v1

## Purpose

This file integrates the strongest mobility anchor found in the source hunt into the AMS route model.

Anchor source:

- Amma, Lanagan, Kim, and Pantano, "Ionic Conductivity in Sodium-Alkaline Earth-Aluminosilicate Glasses," Journal of the American Ceramic Society, 2016. https://doi.org/10.1111/jace.14101
- Metadata page: https://pure.psu.edu/en/publications/ionic-conductivity-in-sodium-alkaline-earth-aluminosilicate-glass

The source is not the exact five-point Pannefieu Na/Mg series. It is still directly relevant because it studies sodium transport in `Na2O-RO-Al2O3-SiO2` glasses where `R = Mg, Ca, Sr, Ba`.

The AMS task is to map the source's transport findings into:

- `M2` sodium route viability
- `M3` alkaline-earth constraint strength
- `M1/M3` charge-compensation gate structures
- route grades
- activation-energy interpretation
- mobility score pressure

## Source Anchor Summary

Reported source points from the abstract/metadata:

- Alkaline-earth ions affect Na transport in aluminosilicate glasses.
- Ionic conductivity was measured for systematic `Na2O-RO-Al2O3-SiO2` glass compositions.
- `R = Mg, Ca, Sr, Ba`.
- `27Al` MAS NMR indicated all Al species were four-coordinated.
- Activation energy for ion conductivity changed with aluminum content and alkaline-earth ion identity.
- In the region where `[Al] < [Na]`, activation energy decreased with increasing aluminum content and decreasing alkaline-earth ionic radius.
- When `[Al] > [Na]`, composition dependence depended on the specific alkaline earth.
- The explanation involves free volume, dielectric constant, and structural changes around `AlO4` charge-compensation sites.
- Smaller, higher-field-strength alkaline-earth ions most strongly affect structures that require bridging of two `AlO4` sites for charge compensation.

## AMS Translation

### `M2`: Sodium Route Viability

In AMS language, Na transport is represented as `M2` route viability.

```text
M2
= sodium-supported mobile-route field
= distributed weak route potential
= R2/O5 pressure when connected
```

Transport evidence strengthens the claim that `M2` is not controlled by sodium content alone.

Instead:

```text
M2 viability
= sodium presence
+ local network openness
+ charge-compensation environment
+ alkaline-earth constraint field
+ available free volume
+ dielectric screening
```

This directly supports the earlier AMS claim:

```text
Na-rich regions do not automatically become material-scale mobility pathways.
They must be structurally admitted.
```

### `M3`: Alkaline-Earth Constraint Strength

In AMS language, alkaline-earth ions contribute to `M3` selective constraint.

```text
M3
= alkaline-earth selective constraint field
= local gate / charge-related constraint
= R1/R3 and O1/O2 pressure
```

The source's comparison of `Mg, Ca, Sr, Ba` gives a way to refine `M3`:

```text
smaller radius + higher field strength
=> stronger local charge-compensation effect
=> stronger M3 gate capacity
```

Relative AMS expectation:

```text
Mg: high M3 constraint
Ca: moderate-high M3 constraint
Sr: moderate M3 constraint
Ba: lower M3 constraint, larger-site disruption
```

This does not mean Mg always lowers mobility. The source indicates that activation energy behavior depends on Al/Na relation and alkaline-earth identity. AMS should therefore treat `M3` as a gate-shaping field, not as a simple mobility suppressor.

### `M1/M3`: Charge-Compensation Gate Structures

The source emphasizes `AlO4` charge-compensation sites.

AMS translation:

```text
AlO4 charge-compensation site
=> M1/M3 gate structure
```

Why:

```text
M1
= network-forming / backbone order

M3
= alkaline-earth selective constraint

AlO4 charge compensation
= place where network order and modifier constraint are coupled
```

A sodium ion moving through the glass does not encounter a neutral empty background. It encounters a field of locally structured charge-compensation gates.

AMS mapping:

```text
AlO4 site compensated by Na
=> route locally admitted for Na-like mobility

AlO4 sites bridged or constrained by alkaline earth
=> route narrowed, gated, or redirected

mixed charge-compensation environments
=> M4 junction possibility
```

This directly strengthens the `R2 -> R3` mapping used for mixed Na/Mg compositions.

## Activation Energy as Route Grade

The source uses activation energy for ion conductivity. AMS can map activation energy into route grade.

This mapping should remain qualitative unless numerical activation energies are imported into a future data table.

```text
lower activation energy
=> easier route completion
=> stronger R2 viability
=> G_B or possible G_A for transport

moderate activation energy
=> route exists but remains gated
=> G_B/G_C

higher activation energy
=> apparent or interrupted route
=> R3 pressure
=> G_C
```

Activation energy is therefore not merely a scalar barrier. In AMS terms it reports how costly route completion is under the current gate field.

Route-grade translation:

| Transport condition | AMS route reading | Route grade |
|---|---|---|
| low activation energy, high conductivity | connected `M2`, `R2/O5/D3` | `G_B` or `G_A` |
| moderate activation energy, moderate conductivity | gated `M2`, `R2 -> R3`, `D4` | `G_B/G_C` |
| high activation energy, low conductivity | interrupted `M2`, `R3/O2/D1-D4` | `G_C` |
| anomalous activation energy across mixed sites | `M4` junction competition | `G_C`, local `G_D` |

## Al/Na Ratio as Gate Regime

The source distinguishes behavior where:

```text
[Al] < [Na]
```

and:

```text
[Al] > [Na]
```

AMS translation:

### `[Al] < [Na]`

There is more sodium than required for simple Al charge compensation.

AMS expectation:

```text
some Na can participate in more mobile modifier-like routes
=> M2 route pressure increases
```

But alkaline-earth identity still affects the gate field.

Route reading:

```text
M2 available
M3 shapes route cost
R2 viability depends on M1/M3 gate structure
```

### `[Al] > [Na]`

There is more Al charge demand than sodium can satisfy alone.

AMS expectation:

```text
alkaline-earth ions become more involved in charge-compensation structures
=> M3 gate behavior becomes more composition-specific
```

Route reading:

```text
M1/M3 coupling intensifies
route class depends strongly on alkaline-earth identity
R2 may narrow into R3
```

This explains why the source reports alkaline-earth-specific behavior when `[Al] > [Na]`.

## Transport Model Update

Previous AMS mobility claim:

```text
Ion mobility follows M2 connectivity.
```

Refined claim:

```text
Ion mobility follows M2 connectivity as admitted or gated by M1/M3 charge-compensation structures.
```

Expanded form:

```text
Na mobility
= M2 route potential
x M1 network admission
x M3 gate condition
x M4 mixed-junction interference
```

In route notation:

```text
connected M2 + permissive M1/M3 gates
=> R2/O5/D3

near-connected M2 + restrictive M1/M3 gates
=> R2 -> R3 / O5 -> O2 / D4

high M4 junction density
=> non-linear transport behavior
```

## Integration with Pannefieu Na/Mg Series

The Pannefieu series has:

```text
50 mol% SiO2
12.5 mol% Al2O3
37.5 mol% total Na2O + MgO
```

For the five points:

```text
X=0.00: Na = 0, Mg high
X=0.25: Na lower than Mg
X=0.50: Na = Mg
X=0.75: Na higher than Mg
X=1.00: Na high, Mg = 0
```

The transport anchor suggests the following refinement:

| `X_Na2O` | Previous mobility class | Refined gate reading | Updated confidence |
|---:|---|---|---|
| 0.00 | low | no sodium route; Mg/Al gate baseline | high |
| 0.25 | low-moderate | sodium route appears but Mg/Al gates dominate | moderate |
| 0.50 | moderate / non-linear | strongest `M4` competition between Na route and Mg/Al gates | moderate-strong |
| 0.75 | high / threshold | sodium route near-connected; residual Mg gates may still distort | moderate |
| 1.00 | high | sodium route dominant; Al gates still shape transport | moderate-high |

The key update is that even `X=1.00` is not pure unconstrained sodium diffusion. Al charge-compensation structures still shape route cost.

## Score Pressure

Previous mobility status:

```text
pending
```

After source hunt:

```text
partially supported
```

After transport integration:

```text
partially supported with formal route mechanism
```

Score effect:

```text
Na/Mg aluminosilicate series: retain 7.5/10
confidence strengthened within moderate band

mixed Na/Mg silicate family: retain 7/10
upward pressure strengthened
```

No numerical score increase yet.

Reason:

The transport anchor is strong, but it is not the exact Pannefieu composition series and does not supply a full five-point Na/Mg conductivity curve.

## Revised Mobility Evidence Status

```text
mobility_prediction_status:
from: pending
to: partially supported with adjacent direct evidence
```

Meaning:

```text
The mechanism is supported in sodium-alkaline-earth aluminosilicate glasses.
The exact Na/Mg series still needs direct conductivity or diffusion measurements.
```

## Implications for Future Modelling

Future Na/Mg transport cases should record:

```text
Al/Na ratio
alkaline-earth identity
alkaline-earth ionic radius
alkaline-earth field strength
Al coordination
free volume proxy
dielectric constant
activation energy for conductivity
conductivity
Na diffusion coefficient if available
```

These fields will let AMS translate conventional transport data into:

```text
M2 route viability
M3 gate strength
M1/M3 charge-compensation gate class
M4 junction pressure
route grade
dominance class
```

## Next Artifact

The next useful artifact should be:

```text
ams-na-mg-score-recalibration-v8.md
```

That file should update the score log with:

- mixed Na/Mg silicate family retained at `7`
- Na/Mg aluminosilicate series retained at `7.5`
- mobility status upgraded from pending to partially supported
- no durability upgrade beyond analogue support
- no interface-release upgrade
