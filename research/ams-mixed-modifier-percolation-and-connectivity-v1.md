# AMS Mixed Modifier Percolation and Connectivity Study v1

## Purpose

This note extends the mixed Na/Mg silicate work by adding a connectivity layer.

The previous mixed-modifier model treated the glass as an internally heterogeneous field with four recurring subregions:

- `M1`: silica-rich route-preserving backbone
- `M2`: sodium-rich diffusing region
- `M3`: magnesium-rich selective or late-gate region
- `M4`: mixed-modifier competition region

That model explained why mixed Na/Mg silicates should often behave as `D4` mixed competitive fields rather than as simple averages of sodium silicate and magnesium silicate behavior.

The remaining question is not only what subregions exist, but how they connect.

For AMS modelling, the decisive issue is whether weak, diffusing, constraint-loosened regions become continuous enough to carry motion, degradation, or release across the material, or whether they remain isolated pockets interrupted by stronger local constraint.

## Core Claim

Mixed modifier behavior depends on subregion connectivity.

The same local ingredients can produce different whole-material behavior depending on whether sodium-rich diffusing regions percolate through the structure, whether magnesium-rich selective regions interrupt them, and whether silica-rich route-preserving regions remain a continuous backbone.

In AMS terms:

```text
Whole-material behavior
= local subregion character
+ connectivity between subregions
+ dominance of continuous pathways over isolated pockets
```

This makes percolation a necessary modelling layer, not an optional refinement.

## Subregion Connectivity Roles

### `M1`: Silica-Rich Route-Preserving Backbone

`M1` regions preserve stronger network continuity.

They support:

- `R1`: narrow viable route
- `O1`: funnelling obstruction
- `D1`: route-dominant behavior
- `G_A` or `G_B`: real route grades

Their functional role is not merely stiffness. They preserve through-going relational order.

If `M1` remains connected across the material, it can prevent sodium-rich diffusing zones from controlling the whole field. In that case, sodium-rich regions may still exist locally, but they do not become the dominant route of motion or degradation.

AMS reading:

```text
connected M1
=> preserved constraint backbone
=> M2 diffusion partly localised
=> D1/D4 rather than full D3
```

### `M2`: Sodium-Rich Diffusing Network

`M2` regions loosen local constraint and increase distributed mobility.

They support:

- `R2`: distributed weak routes
- `O5`: diffusing obstruction
- `D3`: diffusion-dominant behavior when connected
- `G_B` or `G_C`: weak or unreliable routes

The key difference is between isolated `M2` islands and connected `M2` pathways.

Isolated `M2` regions increase local compliance and mobility but do not necessarily dominate the material. Connected `M2` pathways create long-range channels for ion motion, softening, and preferential chemical attack.

AMS reading:

```text
isolated M2
=> local diffusion
=> D4 field with D3 pockets

connected M2
=> through-going weak-path network
=> D3-dominant behavior
```

This is the strongest percolation-sensitive part of the mixed-modifier model.

### `M3`: Magnesium-Rich Selective / Late-Gate Regions

`M3` regions do not simply strengthen the glass in a uniform way. They impose selective local constraint.

They support:

- `R1`: narrow viable route
- `R3`: blocked apparent route
- `O1`: funnelling
- `O2`: late-gate obstruction
- `D1` or `D4`: route-dominant or competitive behavior

Their main role in mixed Na/Mg systems is interruption.

Magnesium-rich regions can break sodium-rich diffusion pathways, force reseating of local motion, or turn an apparently available route into a late-gate failure.

AMS reading:

```text
M3 intersecting M2 path
=> route narrowing or late-gate obstruction
=> R2 interrupted into R3
=> D3 reduced toward D4
```

This is why adding a stronger modifier does not simply reverse sodium behavior. It can produce mixed competition rather than uniform strengthening.

### `M4`: Mixed-Modifier Competition Nodes

`M4` regions are local sites where modifier effects interfere rather than merely add.

They support:

- `D4`: mixed competitive dominance
- local `R5`: loop-dominated pseudo-route
- local `O3`: pocketing
- possible `G_C` or `G_D`: apparent or pseudo-route grades

`M4` regions matter because they can act as transition nodes between `M1`, `M2`, and `M3`.

They may:

- redirect sodium-rich diffusion
- trap release into shallow or elongated loops
- convert a real weak route into a pseudo-route
- delay mobility until enough neighboring `M2` regions connect

AMS reading:

```text
M4 at subregion junction
=> competitive handoff
=> local R5/O3 behavior
=> D4 maintained unless M2 becomes continuous
```

## Connectivity Regimes

### Regime 1: Isolated Sodium-Rich Islands

Profile:

```text
M2 isolated inside connected M1/M3 field
```

Expected AMS behavior:

- local diffusion increases
- whole-material mobility remains limited
- durability weakness remains local
- release routes are interrupted before becoming through-going

Dominance:

```text
D1/D4 with local D3 pockets
```

Route/obstruction profile:

```text
R1 + local R2
O1 + local O5
G_A/G_B whole field, G_C locally
```

Interpretation:

The material contains sodium-like loosened zones, but they do not control the field. This is not sodium-dominated behavior.

### Regime 2: Connected Sodium-Rich Pathways

Profile:

```text
M2 connected across the material
```

Expected AMS behavior:

- ion mobility rises sharply
- chemical durability becomes more vulnerable along weak paths
- softening and relaxation become easier
- optical or surface irregularity may increase if connected paths reach interfaces

Dominance:

```text
D3
```

Route/obstruction profile:

```text
R2
O5
G_B/G_C
```

Interpretation:

This is the threshold at which sodium-rich behavior stops being local and becomes material-scale. In conventional terms this is where mobility and degradation become pathway-controlled rather than merely composition-controlled.

### Regime 3: Interrupted Sodium Pathways

Profile:

```text
M2 nearly connected, but repeatedly cut by M1/M3 regions
```

Expected AMS behavior:

- mobility rises but remains discontinuous
- durability weakness appears uneven
- routes often begin as `R2` but terminate as `R3`
- late-gate failures become common

Dominance:

```text
D4
```

Route/obstruction profile:

```text
R2 -> R3
O5 -> O2
G_B/G_C
```

Interpretation:

This is the central mixed-modifier regime. It is not a simple average of sodium and magnesium behavior. It is a competitive field in which diffusing routes repeatedly encounter selective gates.

### Regime 4: Connected Constraint Backbone

Profile:

```text
M1/M3 connected, M2 discontinuous
```

Expected AMS behavior:

- network continuity remains dominant
- mobility is locally enhanced but globally constrained
- durability remains stronger than in connected `M2` regimes
- interface release tends to be route-preserving or late-gated rather than diffuse

Dominance:

```text
D1/D4
```

Route/obstruction profile:

```text
R1/R3
O1/O2
G_A/G_B with local G_C
```

Interpretation:

This regime explains why mixed modifier systems can retain substantial stiffness or durability even when local sodium-rich regions exist.

### Regime 5: Mixed-Modifier Competition Mesh

Profile:

```text
M4 frequent at junctions between M1, M2, and M3
```

Expected AMS behavior:

- route handoff becomes unstable
- weak routes do not simply percolate
- local trapping and reseating increase
- properties become non-linear with composition

Dominance:

```text
D4
```

Route/obstruction profile:

```text
R1/R2/R3 with local R5
O1/O2/O5 with local O3
G_B/G_C, local G_D
```

Interpretation:

This is the most characteristic mixed modifier result. It predicts non-linear behavior because the material is governed by competing pathway types, not by a single averaged modifier effect.

### Regime 6: Fragmented High-Disorder Field

Profile:

```text
M2 abundant, M1 broken, M3 unable to impose coherent interruption
```

Expected AMS behavior:

- route field fragments
- mobility may be high but incoherent
- durability weakness spreads
- release behavior becomes diffuse or irregular

Dominance:

```text
D3 trending toward R6/O6 behavior
```

Route/obstruction profile:

```text
R2/R6
O5/O6
G_C
```

Interpretation:

This is not stable mixed competition. It is the collapse of the mixed field toward broad diffusion and fragmentation.

## Property Implications

### Ion Mobility

Ion mobility is the strongest connectivity-sensitive property.

AMS expectation:

```text
isolated M2 < interrupted M2 < connected M2
```

When sodium-rich regions connect, mobility should rise more sharply than composition alone would imply.

When magnesium-rich or silica-rich regions interrupt those paths, mobility should be suppressed relative to a sodium-only expectation.

### Chemical Durability

Durability depends on whether weak regions are merely present or connected.

AMS expectation:

```text
local M2 pockets
=> local vulnerability

connected M2
=> through-going degradation paths

M1/M3 interruption
=> delayed or uneven degradation
```

This means durability should not be predicted from sodium content alone. Connectivity determines whether sodium-rich weakness becomes material-scale.

### Viscosity and Softening

Viscosity and softening depend on competition between connected diffusing paths and connected constraint paths.

AMS expectation:

```text
connected M2
=> easier relaxation / lower constraint

connected M1/M3
=> stronger retained constraint

M4 mesh
=> non-linear composition response
```

The important point is non-linearity. A mixed field can soften less or more than expected depending on which pathway system becomes continuous first.

### Optical and Surface Behavior

Optical behavior should be treated cautiously at this stage.

Connectivity may matter when subregion contrast reaches interface-relevant scale or when surface-connected weak paths alter scattering, polishing response, or release behavior.

AMS expectation:

```text
surface-connected M2
=> greater diffuse release risk

M1-dominant surface
=> cleaner route release

M4-rich surface
=> mixed reflection/transmission behavior
```

This should not yet be scored strongly without specific composition, microstructure, and wavelength cases.

## Whole-Field Decision Table

| Connectivity condition | AMS dominance | Route profile | Obstruction profile | Main property implication |
|---|---:|---|---|---|
| isolated `M2` islands | `D1/D4` | `R1` + local `R2` | `O1` + local `O5` | local mobility only |
| connected `M2` pathways | `D3` | `R2` | `O5` | high mobility and degradation vulnerability |
| interrupted `M2` pathways | `D4` | `R2 -> R3` | `O5 -> O2` | mixed modifier suppression / non-linearity |
| connected `M1/M3` backbone | `D1/D4` | `R1/R3` | `O1/O2` | retained constraint and durability |
| frequent `M4` junctions | `D4` | `R1/R2/R3`, local `R5` | `O1/O2/O5`, local `O3` | non-linear mixed behavior |
| fragmented high-disorder field | `D3/R6` | `R2/R6` | `O5/O6` | diffuse mobility and broad weakness |

## Score Judgment

No score change is made at this stage.

Current score remains:

```text
mixed Na/Mg silicate: 6.5/10, upward pressure
```

Reason:

The connectivity model improves explanatory structure, especially for ion mobility, durability, and non-linear mixed modifier behavior. However, it still needs at least one specific composition case with an explicit connectivity estimate before the score should move to 7.

Score movement condition:

```text
6.5 -> 7
if a specific Na/Mg silicate composition can be mapped into M1/M2/M3/M4 proportions
and its observed mobility/durability/viscosity behavior matches the predicted connectivity regime.
```

## Next Artifact

The next useful artifact should be:

```text
ams-mixed-modifier-connectivity-scorecard-v1.md
```

That scorecard should assign comparative 1-10 fit values to the six connectivity regimes against:

- ion mobility
- chemical durability
- viscosity / softening
- interface release behavior
- explanatory distinctiveness over a simple composition-average model

This will decide whether the mixed Na/Mg silicate family can responsibly move from 6.5 to 7.
