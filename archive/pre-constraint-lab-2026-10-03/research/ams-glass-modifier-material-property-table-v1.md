# AMS Glass Modifier Material Property Table v1

## Purpose

This document compares the AMS glass-modifier gradient model against conventional material-property categories.

It follows:

- `ams-glass-modifier-case-study-v1.md`
- `ams-glass-modifier-composition-gradient-v1.md`

The goal is to check whether the AMS route/obstruction/dominance profiles fit known glass-property behaviour well enough to remain useful before any score recalibration.

This is not a numerical glass-science model. It is a structured comparison layer.

## External Anchors Used

The conventional-property side is anchored against stable glass-science references:

- Britannica, `Properties of oxide glasses`
- Journal of Non-Crystalline Solids, `Effect of network formers and modifiers on the crystallization resistance of oxide glasses`
- NPG Asia Materials, `Origin of the mixed alkali effect in silicate glass`
- Chemistry LibreTexts, `Glass Formers and Network Modifiers`
- PMC/NIST-hosted historical discussion of viscosity in alkali silicate binary glasses

Key conventional points used:

- silica is a major glass former with high softening temperature, low thermal expansion, strong chemical/electrical resistance, and broad optical transparency
- soda / sodium oxide acts as a flux and lowers viscosity and melting/softening behaviour
- too much soda can reduce water durability unless stabilising oxides such as lime or magnesia are present
- network modifiers significantly alter glass structure and properties
- alkali-ion placement around non-bridging oxygen and mixed-cation effects matter to ion dynamics and intermediate structure
- modifier effects are composition-sensitive, not binary

## AMS Property-Axis Mapping

The current AMS model maps conventional property categories to route/obstruction behaviour as follows.

| Conventional property axis | AMS modelling axis | Main variables/classes |
|---|---|---|
| optical transmission | route viability through network | `R1`, `R2`, `J_trans`, `Q_coh`, `L_escape` |
| durability / chemical resistance | network persistence and resistance to route disruption | `R1`, `O1`, low `O5`, low destructive `D` |
| viscosity / melting / softening | ease of network rearrangement and slip | `S`, `R2`, `O5`, lowered lock-up |
| ionic mobility | mobile modifier pathway availability | `R2`, local `Z_C`, `O5`, dynamic coordination |
| surface/interface behaviour | entry/release quality and local subregion dominance | `B_in`, `B_out`, `Z_A/Z_B/Z_C`, `D1-D4` |
| glass stability / crystallization resistance | persistence of non-periodic higher-order whole | balance of `R1`, `R2`, obstruction distribution, modifier load |

## Comparison Set

The property table compares:

- pure silica glass
- low sodium silicate
- high sodium silicate
- magnesium-rich silicate
- mixed sodium/magnesium silicate

## Property Table

| Composition case | Optical transmission | Durability / resistance | Viscosity / softening | Ionic mobility | Surface/interface behaviour | AMS fit |
|---|---|---|---|---|---|---|
| pure silica glass | strong baseline transmission | high | high viscosity / high softening | low | route-dominant unless surface degraded | strong |
| low sodium silicate | still transmissive, less cleanly route-dominant | reduced relative to pure silica | lowered | increased | more `Z_C`, more diffusion pressure | strong |
| high sodium silicate | transmission can remain but with weaker route reality | weaker, water/durability risk rises | much lowered | higher | `D3/D4`, more `O5`, local `O2/O3` possible | moderate/strong |
| magnesium-rich silicate | more selective / structured transmission | stabilising relative to high sodium | lowered less diffusively than sodium-rich cases | lower than sodium-rich mobility | more `O1/O2`, stronger local constraint | moderate/strong |
| mixed Na/Mg silicate | locally variable | stabilised relative to high sodium if Mg contributes constraint | composition-sensitive | composition-sensitive | `D4` likely, heterogeneous subregions | promising but under-specified |

## Case Analysis

## 1. Pure Silica Glass

### Conventional Property Reading

Pure silica glass is the strongest baseline network former case in this comparison:

- high thermal/softening resistance
- high viscosity relative to modified silicates
- strong chemical/electrical resistance
- broad transparency

### AMS Reading

```text
pure_silica_glass
= Zones{Z_A, Z_C}
= Dom{D1/D3 depending surface}
= Route{R1, R2}
= Obst{O1, O5}
= Grade{G_A/G_B/G_C}
= Flow{Z_A->completion, Z_A->Z_C under rough/degraded conditions}
```

### Fit Judgment

Strong.

The conventional property profile fits the AMS reading well:

- strong network persistence supports `R1`
- non-periodic glass structure supports `R2`
- surface degradation can still activate `O5/D3`

### Score Implication

Hold:

- pure silica glass: `8`
- broader `SiO2`: `9`

## 2. Low Sodium Silicate

### Conventional Property Reading

Sodium modification lowers viscosity and softening behaviour by disrupting the pure silica network. At lower modification levels, the glass can remain strongly glass-like and transmissive while becoming easier to melt/process and more composition-sensitive.

### AMS Reading

```text
low_sodium_silicate_glass
= Zones{Z_A med, Z_C, (Z_B local weak)}
= Dom{D1/D3, local D4}
= Route{R1 weakened, R2 stronger, (R3 weak)}
= Obst{O5 stronger, (O1 weak), (O2 weak)}
= Grade{G_B/G_C}
= Flow{Z_A->completion weakly, Z_A->Z_C, local D4->Z_C}
```

### Fit Judgment

Strong.

The conventional decrease in viscosity/process temperature maps well to:

- weaker lock-up
- stronger distributed route behaviour
- more `O5`
- more `R2`

### Score Implication

Hold:

- `7`

Upward pressure remains if material-specific cases align.

## 3. High Sodium Silicate

### Conventional Property Reading

Higher sodium modification more strongly disrupts the network. Conventional glass science expects larger property shifts, including lower viscosity / melting behaviour, increased ionic mobility, and possible durability loss if stabilisers are absent or insufficient.

### AMS Reading

```text
high_sodium_silicate_glass
= Zones{Z_C, Z_A weak, (Z_B local)}
= Dom{D3 or D4}
= Route{R2, R3, (R5 local)}
= Obst{O5, O2, (O3 local)}
= Grade{G_C, (G_D local)}
= Flow{Z_A->Z_C, D4->Z_C, local Z_A->Z_B}
```

### Fit Judgment

Moderate/strong.

The AMS model fits the directional property shift:

- weaker route dominance
- stronger diffusion-like behaviour
- higher modifier mobility
- more local incompatibility

But exact high-sodium behaviour is composition-specific, so the confidence should remain restrained.

### Score Implication

Hold:

- `6.5`

## 4. Magnesium-Rich Silicate

### Conventional Property Reading

Magnesia is conventionally treated as a stabilising oxide in soda-lime-silica style contexts, and alkaline-earth modifiers differ from alkali modifiers. Magnesium-rich silicates are also structurally important in mineral contexts.

### AMS Reading

```text
magnesium_rich_silicate
= Zones{Z_A, (Z_B local), (Z_C)}
= Dom{D1 or D4}
= Route{R1, R3, (R2)}
= Obst{O1, O2, (O5)}
= Grade{G_B/G_C}
= Flow{Z_A->completion in structured regions, Z_A->late failure in strained regions}
```

### Fit Judgment

Moderate/strong.

The AMS reading of magnesium as more constraint-forming than sodium is consistent with the conventional idea that stabilising oxides can improve durability and alter network behaviour differently from sodium fluxing alone.

The model should avoid overstating this until specific magnesium silicate systems are tabulated.

### Score Implication

Hold:

- `7`

## 5. Mixed Sodium/Magnesium Silicate

### Conventional Property Reading

Mixed modifier systems are composition-sensitive. Glass properties often depend strongly on where modifier ions sit, how they relate to non-bridging oxygen, and how mixed-cation arrangements affect ion dynamics and intermediate structure.

### AMS Reading

```text
mixed_na_mg_silicate
= Zones{Z_A, Z_B, Z_C}
= Dom{D4}
= Route{R1, R2, R3, (R5 local)}
= Obst{O1, O2, O5, (O3 local)}
= Grade{G_B/G_C, (G_D local)}
= Flow{Z_A->completion, Z_A->late failure, Z_A->Z_C, local Z_A->Z_B}
```

### Fit Judgment

Promising but under-specified.

The AMS prediction that mixed systems become locally heterogeneous and `D4`-rich is plausible, and conventional mixed-cation studies support the importance of ion location and intermediate structure.

However, this case needs more direct composition-specific comparison before becoming high-confidence.

### Score Implication

Hold:

- `6.5`

## Property-by-Property AMS Fit

## Optical Transmission

Best fit:

- pure silica glass
- low sodium silicate

Moderate fit:

- high sodium silicate
- mixed Na/Mg silicate

AMS interpretation:

- optical transmission depends on whether route reality remains viable through the network
- sodium-rich cases likely shift from cleaner `R1/R2` balance toward weaker `R2/R3` and more `O5`

## Durability / Chemical Resistance

Best fit:

- pure silica glass
- magnesium-rich / stabilised silicate contexts

Weaker:

- high sodium silicate without sufficient stabilising structure

AMS interpretation:

- durability corresponds to resistance against destructive route and network disruption
- sodium-rich systems increase route mobility and weakening
- magnesium-rich systems preserve more local constraint

## Viscosity / Melting Behaviour

Best fit:

- sodium silicate gradient

AMS interpretation:

- lower viscosity and softening behaviour correspond to weaker lock-up, more slip, and more distributed route freedom
- high sodium modification should increase `R2/O5/D3` tendencies

## Ionic Mobility

Best fit:

- sodium-containing systems
- mixed modifier systems

AMS interpretation:

- ionic mobility tracks dynamic modifier pathway availability
- sodium cases especially strengthen the idea of local route/pathway modulation

## Surface / Interface Behaviour

Best fit:

- high sodium silicate
- mixed Na/Mg silicate
- rough glass cases

AMS interpretation:

- modifier distribution can create local subregion heterogeneity
- this supports `D4` in mixed systems and `D3` in diffuse-dominant cases

## Where the AMS Gradient Model Fits Well

## 1. Sodium Lowers Network Constraint

The AMS shift toward:

- weaker `R1`
- stronger `R2`
- stronger `O5`
- more `D3`

fits conventional expectations about sodium fluxing and network modification.

## 2. Excess Sodium Raises Durability/Water-Resistance Concerns

The AMS reading of high sodium as:

- more route-disruptive
- more diffusion-prone
- more locally unstable

fits the conventional warning that too much soda can lead to water attack unless stabilised.

## 3. Magnesium Acts More Like Stabilising Constraint Than Sodium

The AMS contrast:

- sodium as distributed weakening
- magnesium as local constraint / stabilising participation

is directionally well aligned with stabilising oxide language.

## 4. Mixed Systems Should Be Heterogeneous

The AMS `D4` reading for mixed modifiers fits the conventional emphasis on ion location, non-bridging oxygen environments, and composition-structure-property correlations.

## Where the AMS Model Needs Revision or More Detail

## 1. Sodium Effects Are Not Monotonic in Every Property

The AMS gradient currently treats sodium increase mainly as a shift toward diffusion and weaker route dominance.

That is useful, but some properties may respond nonlinearly or have composition-specific optima.

Needed refinement:

- composition-specific subcases

## 2. Magnesium Needs More Direct Material Cases

The stabilising reading is plausible, but too broad.

Needed refinement:

- specific magnesium silicates
- comparison against calcium/lime and other alkaline-earth modifiers

## 3. Mixed Modifier Systems Need Dedicated Modelling

The `D4` diagnosis is promising, but it needs real subregion detail.

Needed refinement:

- mixed alkali / mixed modifier case studies
- internal subregion interface notation

## 4. Optical Transmission Needs Wavelength / Defect / Surface Separation Later

The current model uses optical transmission as a broad property axis.

Later work should separate:

- bulk transparency
- scattering
- surface reflection
- absorption
- wavelength-dependent behaviour

## Score Recalibration Judgment

No score changes yet.

Current holds:

- pure silica glass: `8`
- broader `SiO2`: `9`
- sodium silicates: `7`
- magnesium silicates: `7`
- high sodium silicate: `6.5`
- mixed Na/Mg silicate: `6.5`

Reason:

- conventional-property comparison supports the model directionally
- but not enough for score increase without more specific case studies

## Strongest Current Conclusion

The modifier-gradient model is directionally coherent against conventional glass-property categories.

The strongest supported AMS pattern is:

- sodium modification pushes toward distributed weakening, diffusion, and route broadening
- magnesium-rich modification pushes toward local constraint, selectivity, and later route failure under strain
- mixed systems likely produce local heterogeneity and should be treated as `D4` candidates

## Next Modelling Priority

The best next technical target is:

- mixed modifier internal subregions

Reason:

- the strongest unresolved prediction from this comparison is that mixed Na/Mg systems should produce heterogeneous local zones
- the interface framework is already well suited to model that

## Confidence

- confidence that the conventional-property comparison supports the AMS gradient directionally: `8/10`
- confidence that no score change should occur yet: `9/10`
- confidence that mixed modifier subregion modelling is the next best depth target: `8/10`

## Recommendation

Do not recalibrate scores yet.

Proceed to:

- `ams-mixed-modifier-subregion-model-v1.md`

That should model mixed Na/Mg silicate as an internal heterogeneous material field with:

- sodium-rich diffusing zones
- magnesium-rich selective/late-gate zones
- silica-rich route-preserving zones

and test whether the mixed-interface framework can handle internal material heterogeneity as well as external optical interfaces.
