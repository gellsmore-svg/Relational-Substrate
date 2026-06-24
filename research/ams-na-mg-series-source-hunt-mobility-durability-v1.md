# AMS Na/Mg Series Source Hunt: Mobility and Durability v1

## Purpose

This source hunt looks for direct evidence relevant to the pending mobility and durability predictions in the Na/Mg aluminosilicate series.

The target evidence is:

- electrical conductivity across Na/Mg aluminosilicate or Na/Mg silicate systems
- sodium diffusion or ion transport across mixed modifier systems
- leaching, dissolution, or ion-exchange durability in Na/Mg or nearby sodium aluminosilicate systems
- structural mapping tying Na/Mg distribution to transport or durability

The goal is to replace pending predictions with observed evidence where possible, while keeping partial analogues clearly separated from direct matches.

## Direct Target Series

The current AMS series is based on:

```text
50 mol% SiO2
12.5 mol% Al2O3
37.5 mol% total Na2O + MgO
X_Na2O = 0.00, 0.25, 0.50, 0.75, 1.00
```

Primary source:

- Pannefieu, Le Losq, Florian, and Moretti, "Effect of the Na/Mg mixing on the structure and properties of aluminosilicate melts," Journal of Non-Crystalline Solids, 2024. https://doi.org/10.1016/j.jnoncrysol.2024.123056

This source directly supports:

- controlled Na/Mg substitution
- non-linear density, molar volume, viscosity, and configurational entropy behavior
- Raman and NMR structural evidence
- preferential Na/Mg role-sharing

It does not directly measure:

- electrical conductivity
- sodium diffusion
- leaching
- chemical durability
- interface release

## Source Findings

### 1. Ionic Conductivity in Sodium-Alkaline Earth-Aluminosilicate Glasses

Source:

- Amma, Lanagan, Kim, and Pantano, "Ionic Conductivity in Sodium-Alkaline Earth-Aluminosilicate Glasses," Journal of the American Ceramic Society, 2016. https://doi.org/10.1111/jace.14101
- Metadata page: https://pure.psu.edu/en/publications/ionic-conductivity-in-sodium-alkaline-earth-aluminosilicate-glass

Reported relevance:

The study measured ionic conductivity in systematic `Na2O-RO-Al2O3-SiO2` glasses where `R = Mg, Ca, Sr, Ba`.

Key reported points from the metadata/abstract:

- Alkaline-earth ions affect Na transport in aluminosilicate glasses.
- The study measured ionic conductivity across systematic compositions.
- `27Al` MAS NMR indicated four-coordinated Al species.
- Activation energy for ion conductivity changed with aluminum content and alkaline-earth ion size.
- The authors explain results using free volume, dielectric constant, and structural changes around `AlO4` charge-compensation sites.
- Smaller, higher-field-strength alkaline-earth ions affect charge-compensation structures most strongly where alkaline earth ions bridge two `AlO4` sites.

AMS relevance:

This is a strong mobility anchor for the AMS model, although it is not the exact five-point Pannefieu series.

AMS mapping:

```text
alkaline-earth ion affects Na transport
=> M3-like selective constraint affects M2 mobility

charge-compensation structure changes
=> M1/M3 relation changes

activation energy changes with alkaline-earth identity and Al relation
=> mobility is not controlled by Na content alone
```

Evidence status:

```text
direct for Na transport in sodium-alkaline-earth aluminosilicate glasses
partial for the exact Na/Mg five-point series
```

Score effect:

```text
mobility prediction: pending -> partially supported
series score pressure: mild upward
family score pressure: mild upward
```

### 2. Na2O-Al2O3-SiO2 Ion Exchange and Durability

Source:

- "The structure of Na2O-Al2O3-SiO2 glass: impact on sodium ion exchange in H2O and D2O," Journal of Non-Crystalline Solids, 2001. https://doi.org/10.1016/S0022-3093(01)00890-0

Reported relevance:

This source studies sodium aluminosilicate glass structure and sodium ion exchange in water.

Key reported points from the accessible abstract:

- Sodium release was `10-50` times faster than matrix dissolution under the studied conditions.
- Alkali exchange is an important long-term reaction mechanism near silica saturation.
- Sodium release rates were slower in `D2O` than in `H2O`, while matrix dissolution was unaffected.
- Changes in Na exchange rate with increasing `Al2O3` could not be explained by non-bridging oxygen count alone.
- A structural energy barrier for alkali exchange was estimated using Na-O bond length, coordination, and binding-energy data.
- The barrier increased from `34 kJ mol^-1` for sodium disilicate to `49 kJ mol^-1` for a glass containing `15 mol% Al2O3`.
- The authors connect the increase to stronger Na bonding and increasing mechanical stiffness of the glass network.

AMS relevance:

This is a strong durability/ion-exchange analogue, but it lacks Mg.

AMS mapping:

```text
Na release faster than matrix dissolution
=> M2 weak-path / ion-exchange behavior can be distinct from whole-network dissolution

Al2O3 raises exchange barrier
=> M1 charge-linked network constraint suppresses M2 release

NBO count alone insufficient
=> route behavior depends on local structure, not simple site count
```

Evidence status:

```text
direct for Na aluminosilicate ion exchange
partial analogue for Na/Mg aluminosilicate durability
```

Score effect:

```text
durability prediction: pending -> partially supported by analogue
series score pressure: mild upward
family score pressure: neutral-to-mild upward
```

### 3. Na/Mg Mixing in Aluminosilicate Melts

Source:

- Pannefieu et al., 2024. https://doi.org/10.1016/j.jnoncrysol.2024.123056

Reported relevance:

This remains the primary direct source for the composition path and structural/rheological non-linearity.

AMS relevance:

Although it does not measure mobility or durability, it supplies the structural basis needed for those predictions:

```text
Na/Mg sub-networks
preferential role-sharing
non-ideal entropy
non-linear viscosity
Raman/NMR structural changes
```

AMS mapping:

```text
role-sharing
=> M4 mixed-competition nodes

non-ideal entropy
=> non-random route organisation

non-linear viscosity
=> route availability and route completion are not linear
```

Evidence status:

```text
direct for structural/rheological series
indirect for mobility/durability predictions
```

Score effect:

```text
supports retaining series at 7.5
does not by itself justify mobility/durability upgrade
```

### 4. Mixed Modifier and Mixed Alkali Chemical Durability

Source:

- Dilmore, Clark, and Hench, "Chemical Durability of Na2O-K2O-CaO-SiO2 Glasses," Journal of the American Ceramic Society, 1978. DOI listed at ResearchGate page: https://doi.org/10.1111/j.1151-2916.1978.tb09355.x
- Accessible metadata page: https://www.researchgate.net/publication/230526668_Chemical_Durability_of_Na2O-K2O-CaO-SiO2_Glasses

Reported relevance:

The accessible abstract reports that the mixed-alkali effect on chemical durability depends on corrosion solution pH.

Key reported points:

- For `pH < 9`, alkali-ion leaching is the major corrosion mode and the mixed-alkali effect is large.
- For `pH >= 9`, congruent glass dissolution controls the rate and the effect is diminished.
- The effect also depends on extent of reaction and surface-area/solution-volume ratio.

AMS relevance:

This is not Na/Mg and not aluminosilicate, so it is only an analogue. It is still useful because it supports the AMS distinction between ion-release routes and matrix dissolution routes.

AMS mapping:

```text
ion leaching dominant
=> M2 / O5 weak-path behavior matters

matrix dissolution dominant
=> whole-network dissolution overrides modifier-path specificity

pH changes mechanism
=> route class depends on external boundary condition
```

Evidence status:

```text
indirect analogue only
```

Score effect:

```text
durability prediction: conceptual support only
no direct score change
```

### 5. Na2O-MgO-CaO-SiO2 Dissolution in HF Solutions

Source:

- Spierings and Van Dijk, "The Dissolution Of Na2O-MgO-CaO-SiO2 Glass In Aqueous HF Solutions," Journal of Materials Science, 1987. Metadata page: https://www.britglass.org.uk/knowledge-base/digital-library-and-information-services/dissolution-na2o-mgo-cao-sio2-glass-aqueous

Reported relevance:

The metadata reports dissolution of Na2O-MgO-CaO-SiO2 glass in aqueous HF plus strong-acid solutions at varying temperatures.

Key reported points:

- Dissolution rate increases with higher HF concentration.
- Dissolution rate increases with higher strong acid concentration.
- Dissolution rate increases with higher temperature.
- Models are discussed for the relationship between dissolution rate and `H+` concentration.

AMS relevance:

This contains both Na and Mg in a silicate glass, but it is a harsh HF dissolution system and includes Ca. It is therefore not a clean Na/Mg mixed-modifier durability test.

AMS mapping:

```text
external chemical boundary dominates
=> interface/boundary condition can override internal route differences
```

Evidence status:

```text
weak direct compositional relevance
strong warning about boundary-condition dominance
```

Score effect:

```text
no upgrade
adds caution to durability prediction
```

### 6. Mixed Glass Former Sodium Ion Dynamics

Source:

- "Mixed network former effect on the ion-dynamics of Sodium Alumino-Phospho-Silicate glasses," Acta Materialia, 2025. https://doi.org/10.1016/j.actamat.2025.120837

Reported relevance:

The accessible abstract reports sodium-ion dynamics and conductivity in sodium alumino-phospho-silicate glasses as SiO2 substitutes for P2O5 at fixed Al2O3 and Na2O.

Key reported points:

- Composition, structure, and conductivity are linked.
- Conductivity changes non-linearly with network-former composition.
- Na diffusion coefficients and critical hopping distance are correlated with structural changes.

AMS relevance:

This is not Na/Mg mixed modifier evidence. It is a useful transport analogue showing that sodium mobility depends on structural pathway variables, not only sodium concentration.

AMS mapping:

```text
critical hopping distance / diffusion coefficients
=> route length and route viability analogue

composition-dependent Na dynamics
=> M2 route behavior depends on surrounding network grammar
```

Evidence status:

```text
analogue only
```

Score effect:

```text
mobility prediction receives conceptual support
no direct family score change
```

## Evidence Upgrade Table

| Prediction field | Previous status | Source hunt result | Updated status |
|---|---|---|---|
| Na/Mg structure role-sharing | observed | Pannefieu 2024 directly supports | strong |
| viscosity non-linearity | observed | Pannefieu 2024 directly supports | strong |
| Na mobility affected by alkaline-earth context | pending | Amma et al. 2016 directly supports in related sodium-alkaline-earth aluminosilicates | partially supported |
| Na ion exchange depends on aluminosilicate structure | pending | 2001 Na aluminosilicate ion-exchange study supports | partially supported |
| Na/Mg-specific durability curve | pending | no clean five-point match found | still pending |
| Na/Mg-specific conductivity curve across Pannefieu series | pending | no exact match found | still pending |
| surface/interface release | pending | no direct evidence found | still pending |

## Updated Prediction Status

### Mobility

Previous:

```text
pending
```

Updated:

```text
partially supported
```

Reason:

The Amma et al. sodium-alkaline-earth aluminosilicate conductivity paper directly supports the idea that alkaline-earth ions, including Mg-family contexts, affect Na transport through structural changes. It is not the exact Pannefieu five-point series, but it is close enough to move mobility from pure prediction to partial support.

### Durability

Previous:

```text
pending
```

Updated:

```text
partially supported by analogues, still pending for Na/Mg-specific curve
```

Reason:

The Na aluminosilicate ion-exchange paper strongly supports the idea that sodium release and matrix dissolution are distinct route processes and that Al-linked structure alters Na exchange barriers. The mixed-alkali durability paper supports the route distinction between leaching and matrix dissolution. But no clean Na/Mg five-point durability series was found.

### Interface Release

Previous:

```text
pending
```

Updated:

```text
still pending
```

Reason:

No direct source was found tying Na/Mg subregion exposure to optical reflection, transmission, polishing, scattering, or release behavior.

## Score Reassessment

Current series score:

```text
Na/Mg aluminosilicate series: 7.5/10
```

Updated judgment:

```text
retain 7.5/10
confidence: moderate, slightly strengthened
```

Reason:

The source hunt strengthens mobility plausibility but does not yet provide direct conductivity or durability curves for the exact five-point series.

Current family score:

```text
mixed Na/Mg silicate family: 7/10
```

Updated judgment:

```text
retain 7/10
upward pressure mildly strengthened
```

Reason:

The mobility evidence is relevant and the durability analogues are coherent, but the family still needs a cleaner Na/Mg silicate or aluminosilicate transport/durability series.

## Most Important New Anchor

The strongest new anchor is:

```text
Amma et al. 2016: Ionic Conductivity in Sodium-Alkaline Earth-Aluminosilicate Glasses
```

Why it matters:

```text
It directly ties sodium transport to alkaline-earth identity, aluminum relation, free volume, dielectric constant, and charge-compensation structure.
```

AMS implication:

```text
M2 mobility is not independent.
It is gated by M1/M3 charge-compensation and local constraint structure.
```

## Remaining Evidence Gap

The key missing source remains:

```text
conductivity or diffusion measured across the exact Pannefieu-style Na/Mg substitution series
or
chemical durability measured across the exact Pannefieu-style Na/Mg substitution series
```

Without that, the AMS mobility/durability model is coherent and partially supported, but not directly confirmed.

## Next Artifact

The next useful artifact should be:

```text
ams-na-mg-transport-anchor-integration-v1.md
```

That file should integrate the Amma et al. conductivity result into the AMS route model more formally:

- map alkaline-earth ion size and field strength into `M3` constraint strength
- map Al charge-compensation sites into `M1/M3` gate structures
- map activation energy changes into route-grade changes
- update the mobility prediction grid with a stronger structural basis
