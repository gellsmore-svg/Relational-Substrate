# AMS Mixed Modifier Property Comparison v1

## Purpose

This document compares the AMS mixed Na/Mg silicate internal-subregion model against conventional mixed-modifier and mixed-cation glass behaviour.

It follows:

- `ams-mixed-modifier-subregion-model-v1.md`
- `ams-glass-modifier-material-property-table-v1.md`

The goal is to decide whether the AMS diagnosis:

- mixed Na/Mg silicate as a `D4` internal heterogeneous material field

is directionally supported, contradicted, or underconstrained by conventional property behaviour.

## External Anchors Used

The conventional side is anchored against current and stable glass-science sources:

- MDPI Materials, `Elastic Properties and Hardness of Mixed Alkaline Earth Silicate Oxynitride Glasses`
- Journal of Non-Crystalline Solids, `Mixed alkaline earth effect in sodium aluminosilicate glasses`
- PMC, `Structural origins of the Mixed Alkali Effect in Alkali Aluminosilicate Glasses`
- Britannica, `Properties of oxide glasses`
- NPG Asia Materials, `Origin of the mixed alkali effect in silicate glass`
- Ceramics International, `Study of the mixed alkali effect in glasses and its relation to glass structure and alkali earth ion content`
- Acta Materialia, `Mixed network former effect on the ion-dynamics of Sodium Alumino-Phospho-Silicate glasses`

## Conventional Points Used

The comparison relies on these conventional observations:

- mixed modifier effects are property-specific and often nonlinear
- mobility/conductivity properties are especially sensitive to mixed-cation structure
- viscosity, hardness, glass transition, and chemical durability may deviate from simple linear mixing
- some systems show little or no mixed modifier effect for selected mechanical properties
- modifier ion location, non-bridging oxygen environments, ring structure, percolation channels, and local structural changes matter
- soda lowers viscosity and softening behaviour in silica glass, while stabilising oxides such as magnesia can improve durability in suitable compositions

## AMS Model Being Tested

From:

- `ams-mixed-modifier-subregion-model-v1.md`

the current AMS profile is:

```text
mixed_na_mg_silicate_internal
= Subregions{M1,M2,M3,M4}
= Dom{D4 material field}
= Route{R1,R2,R3,(R5 local)}
= Obst{O1,O2,O5,(O3 local)}
= Grade{G_B/G_C,(G_D local)}
= Flow{M1->M2, M2->M3, M3->M1, M1->M4}
```

Subregions:

- `M1`: silica-rich route-preserving zone
- `M2`: sodium-rich diffusing zone
- `M3`: magnesium-rich selective / late-gate zone
- `M4`: mixed-modifier competition zone

## Property Axis 1: Ion Mobility / Conductivity

## Conventional Reading

Mixed alkali and mixed modifier behaviour often shows strong effects in ion mobility and conductivity. Simulations and structural studies emphasise that modifier-ion location, cation environments, ring size, and percolation-like pathways can strongly affect mobility.

## AMS Reading

The AMS model predicts:

- sodium-rich zones should support more mobile/diffusive pathway behaviour
- magnesium-rich zones should constrain or interrupt mobility more strongly
- mixed zones should produce heterogeneous mobility paths rather than one averaged mobility field

Formal shorthand:

```text
ion_mobility[mixed_na_mg]
= Subregions{M2,M3,M4}
= Dom{D4}
= Route{R2,R3,(R5 local)}
= Obst{O5,O2,(O3 local)}
= Flow{M2 pathways interrupted or restructured by M3/M4}
```

## Fit Judgment

Strong directional fit.

Reason:

- conventional mixed-cation work emphasises non-simple mobility behaviour and local structural control
- AMS predicts exactly that mixed systems should be path-dependent and heterogeneous

## Revision Needed?

No major revision.

But AMS should be careful not to assume that mixed modifiers always raise or lower mobility in one simple direction. The right claim is:

- mixed modifiers restructure mobility pathways

not:

- mixed modifiers always increase or decrease mobility.

## Property Axis 2: Durability / Chemical Resistance

## Conventional Reading

Silica glass has strong chemical resistance. Soda can reduce water durability if excessive, while stabilising oxides such as lime or magnesia can improve durability in suitable soda-lime-silica style compositions. Mixed cation systems can show nonlinear durability behaviour, depending on composition and local network structure.

## AMS Reading

AMS predicts:

- sodium-rich zones are vulnerability points because route dominance and network constraint weaken
- magnesium-rich zones can restore or increase local constraint
- mixed systems may have durability governed by whether sodium-rich diffusing zones percolate or remain interrupted by stronger constraint zones

Formal shorthand:

```text
durability[mixed_na_mg]
= Subregions{M1,M2,M3,M4}
= Dom{D4}
= Route{R1/R3 vs R2}
= Obst{O1/O2 vs O5}
= Key{whether M2 forms connected weak pathways}
```

## Fit Judgment

Moderate/strong fit.

Reason:

- conventional stabilising-oxide behaviour supports the broad sodium/magnesium contrast
- but durability is highly composition- and system-dependent

## Revision Needed?

Refine the AMS claim:

- durability depends less on average sodium content alone and more on whether sodium-rich diffusing zones become connected enough to dominate the route field.

That is a useful correction.

## Property Axis 3: Viscosity / Softening Behaviour

## Conventional Reading

Soda lowers viscosity and melting/softening behaviour in silica glass. Mixed modifier systems can show nonlinear viscosity or glass-transition behaviour, but effects differ by system. Some mixed alkaline-earth systems show minima or deviations from linearity, and not every property shows a strong mixed effect.

## AMS Reading

AMS predicts:

- sodium-rich zones reduce network lock-up and increase slip/distributed continuation
- magnesium-rich zones add local constraint and may preserve selective route structures
- mixed zones can produce nonadditive behaviour if pathway weakening and local constraint compete

Formal shorthand:

```text
viscosity[mixed_na_mg]
= Subregions{M2,M3,M4}
= Dom{D4}
= Route{R2 vs R1/R3}
= Obst{O5 vs O1/O2}
= Flow{distributed weakening competing with local constraint}
```

## Fit Judgment

Strong directional fit, moderate specificity.

Reason:

- AMS handles nonlinearity and competition well
- but cannot yet predict a specific viscosity trend without composition and temperature detail

## Revision Needed?

Yes, a precision guardrail:

- AMS should model viscosity/softening as a competition between route weakening and local constraint, not as a monotonic sodium/magnesium average.

## Property Axis 4: Glass Transition / Stability

## Conventional Reading

Glass transition and stability can show nonlinear dependence on modifier type and composition. Some studies show maxima/minima or deviations tied to local structural changes, while others show absent or weak mixed modifier effects in certain property families.

## AMS Reading

AMS predicts:

- `D4` internal heterogeneity should be most visible where local structure and pathway connectivity affect transition behaviour
- M1/M3 route-preserving zones should raise local stability
- M2 diffusing zones should lower local lock-up
- M4 competition zones should generate non-simple behaviour

Formal shorthand:

```text
glass_transition[mixed_na_mg]
= Dom{D4}
= Compete{M1/M3 constraint, M2 diffusion, M4 local competition}
= Outcome{composition-sensitive, possible nonlinear trend}
```

## Fit Judgment

Moderate/strong fit.

Reason:

- conventional literature supports nonlinear, system-specific behaviour
- AMS predicts non-simple local competition

## Revision Needed?

Do not claim mixed Na/Mg systems necessarily show a strong mixed effect in every stability measure.

The right claim is:

- if a property depends strongly on local pathway continuity and modifier environment, a `D4` internal-field effect is more likely to appear.

## Property Axis 5: Optical Behaviour

## Conventional Reading

Optical behaviour in glasses depends on composition, network structure, defects, surface quality, and wavelength. Many silicate glasses remain transparent, but modifiers can change refractive index, scattering, absorption, and surface/interface behaviour.

## AMS Reading

AMS predicts:

- pure route-preserving regions support cleaner propagation
- sodium-rich diffusing regions may increase route weakening and scattering risk
- magnesium-rich selective regions may preserve stronger local route structure
- mixed local zones may produce local route reality variation

Formal shorthand:

```text
optics[mixed_na_mg]
= Subregions{M1,M2,M3,M4}
= Route{R1,R2,R3,(R5)}
= Obst{O1,O5,O2,(O3)}
= Dom{D4 where subregions are heterogeneous}
```

## Fit Judgment

Moderate fit.

Reason:

- AMS gives a coherent qualitative structure
- but optical behaviour needs more explicit separation between:
  - bulk transmission
  - surface scattering
  - absorption
  - wavelength dependence

## Revision Needed?

Yes:

- optical claims should remain cautious until wavelength, defect, and surface quality are separated.

## Property Axis 6: Surface / Interface Behaviour

## Conventional Reading

Glass properties and surface behaviour depend strongly on composition, modifier distribution, durability, and local structure. Mixed modifier effects can alter local environments and therefore may alter surface and interface behaviour.

## AMS Reading

This is the strongest fit for the current model.

AMS predicts:

- terminal layers in mixed systems can differ strongly from bulk averages
- sodium-rich surface subregions may favour diffusion and weakened release
- magnesium-rich regions may favour selective or late-gate behaviour
- mixed terminal layers may become `D4`

Formal shorthand:

```text
surface[mixed_na_mg]
= Zones{Z_A,Z_B,Z_C}
= Dom{D4}
= Route{R1,R2,R3,(R5)}
= Obst{O1,O2,O5,(O3)}
= Flow{route, pocket, and fringe behaviours depending local terminal composition}
```

## Fit Judgment

Strong qualitative fit.

Reason:

- the AMS interface framework was built exactly for this type of local heterogeneity
- conventional mixed-modifier work supports local environment significance

## Revision Needed?

No major revision.

But the model needs direct composition-specific surface cases later.

## Overall Comparison Table

| Property axis | Conventional support for non-simple local behaviour | AMS fit | Main caution |
|---|---:|---|---|
| ion mobility / conductivity | high | strong | direction not monotonic |
| durability / chemical resistance | medium/high | moderate/strong | depends on connected weak zones |
| viscosity / softening | high | strong directional, moderate specific | needs composition/temperature |
| glass transition / stability | medium/high | moderate/strong | mixed effect not universal |
| optical behaviour | medium | moderate | needs wavelength/defect/surface split |
| surface/interface behaviour | high | strong | needs specific terminal-layer cases |

## Strongest Findings

## 1. `D4` Internal Heterogeneity Is Well Supported Directionally

This is the main result.

Conventional mixed-modifier and mixed-cation glass science repeatedly points away from simple averaging and toward local structural effects.

That aligns strongly with:

- `mixed_na_mg_silicate_internal = D4 material field`

## 2. Ion Mobility Is the Strongest Conventional Anchor

The mixed-modifier model fits ion mobility particularly well because conventional work already emphasises:

- modifier ion location
- percolation channels
- ring/intermediate structure
- local cation environments

These map cleanly into AMS subregion and route language.

## 3. Durability Needs a Connectivity Condition

This is an important refinement.

The AMS durability claim should be:

- sodium-rich diffusing zones matter most when they connect enough to dominate degradation pathways

not simply:

- more sodium equals less durable.

## 4. Viscosity Needs Competition Language

AMS should treat viscosity/softening as:

- route weakening competing with local constraint

not:

- a single modifier average.

## 5. Optical Claims Should Remain More Cautious

The interface model is promising, but optical behaviour needs a later dedicated split by:

- wavelength
- defect
- surface
- absorption
- bulk transmission

## Recalibration Judgment

No score change yet.

Current score:

- mixed Na/Mg silicate: `6.5`

Post-comparison status:

- upward pressure toward `7`
- not enough to move yet

Reason:

- the model is directionally supported, especially for ion mobility and surface/interface behaviour
- but no specific composition case has been modelled deeply enough

## What Would Justify a Move to `7`

A move from `6.5 -> 7` would be justified after one of:

- a specific mixed Na/Mg composition case is modelled using property data
- an internal subregion/percolation case shows strong fit
- a surface/interface case directly uses mixed modifier composition
- a mobility/durability comparison demonstrates clear explanatory gain over averaged modifier language

## Current Weak Points

## 1. No Composition-Specific Case Yet

The model still lacks a worked composition example.

## 2. Na/Mg Is Less Directly Documented Than Na/K or Ca/Mg in the Quick Source Set

The conventional evidence strongly supports mixed modifier logic generally, but direct Na/Mg silicate comparison remains underdeveloped in this file.

## 3. Optical Behaviour Remains Under-Specified

The AMS model should not overclaim here yet.

## Recommendation

Keep:

- mixed Na/Mg silicate at `6.5`

but mark it as:

- high-priority watchlist

The next move should be a targeted internal-subregion/percolation study because that is where the conventional comparison and AMS model now meet most directly.

## Next Move

The best next artifact is:

- `ams-mixed-modifier-percolation-and-connectivity-v1.md`

That should ask:

- when do sodium-rich diffusing zones connect enough to dominate mobility or degradation?
- when do magnesium-rich / silica-rich constraint zones interrupt those pathways?
- when does the mixed field remain `D4` rather than collapsing into mostly `D3` or mostly `D1`?

## Sources

- Britannica, `Properties of oxide glasses`: https://www.britannica.com/science/amorphous-solid/Properties-of-oxide-glasses
- MDPI Materials, `Elastic Properties and Hardness of Mixed Alkaline Earth Silicate Oxynitride Glasses`: https://www.mdpi.com/1996-1944/15/14/5022
- Journal of Non-Crystalline Solids, `Mixed alkaline earth effect in sodium aluminosilicate glasses`: https://www.sciencedirect.com/science/article/pii/S0022309313001518
- PMC, `Structural origins of the Mixed Alkali Effect in Alkali Aluminosilicate Glasses`: https://pmc.ncbi.nlm.nih.gov/articles/PMC7031271/
- NPG Asia Materials, `Origin of the mixed alkali effect in silicate glass`: https://www.nature.com/articles/s41427-019-0180-4
- Ceramics International, `Study of the mixed alkali effect in glasses and its relation to glass structure and alkali earth ion content`: https://www.sciencedirect.com/science/article/abs/pii/0272884289900539
- Acta Materialia, `Mixed network former effect on the ion-dynamics of Sodium Alumino-Phospho-Silicate glasses`: https://www.sciencedirect.com/science/article/pii/S1359645425001296
