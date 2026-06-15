# RI Structural Pattern Note: Fold Density And Polarizable Packing

Date: 2026-05-16

## Purpose

This note records the current refractive-index blocker through the lateral physical-pattern lens discussed as "invisible origami": fold density, packing, stored constraint, and polarizable response. The point is heuristic pattern discovery only. Validation still has to remain source-anchored and held-out.

## Current Diagnostic Result

The existing `analysis/ri-structural-descriptor-validation.mjs` script already tests the right scientific translation of the lateral pattern:

- fold density / compactness -> measured density or normalized density
- polarizable packing -> Lorentz-Lorenz response space
- framework crease density -> charge-balanced Al per oxygen
- cation field response -> charge-balanced Al per oxygen multiplied by cation field-strength delta

The pre-held-out guardrail currently blocks promotion:

| Measure | Result |
|---|---:|
| Guardrail status | BLOCKED under raw scale; not blocked under standardized feature scale |
| Original density-model condition number | 42.308 |
| Guardrail threshold | 30 |

This means the descriptor family is plausible but not yet statistically clean enough to freeze before a fresh RI lookup. Density, Al/O, and cation response are not perfectly collinear, but the calibration design is still too coupled for a defensible held-out prediction.

A companion descriptor table now exists in `analysis/ri-topology-volume-descriptor-diagnostic.mjs`. It does not fit or promote a model. It exposes topology class, molar volume, oxygen volume, tetrahedral packing density, Lorentz-Lorenz value, molar refraction, and oxygen refraction.

Key pattern from the descriptor table:

| Class / row | Oxygen volume | T packing density | Oxygen refraction |
|---|---:|---:|---:|
| Feldspar framework mean | 12.85498 | 0.03893 | 4.06704 |
| Kalsilite feldspathoid | 15.17858 | 0.03294 | 4.74395 |
| Sodium metasilicate glass | 15.5651 | 0.02142 | 4.73193 |

This is instructive because the known feldspathoid transfer failure is not merely "more Al." It sits in a looser oxygen-volume / lower T-packing region than the feldspar framework rows and has oxygen refraction closer to the depolymerized glass row. That supports treating topology class and packing as explicit descriptors before another RI prediction is attempted.

Feature-set guardrails were then rerun with standardized non-intercept columns. This matters because raw condition numbers were dominated by descriptor scale. Under standardized scale, the candidate families are numerically separable:

| Feature family | Standardized condition | Reading |
|---|---:|---|
| density + Al/O + cation-response/O | 2.3446 | separable |
| oxygen-volume + Al/O + cation-response/O | 1.9208 | separable |
| T-packing + Al/O + cation-response/O | 1.8002 | separable |
| minimal oxygen-volume + cation-response/O | 1.7766 | separable |
| minimal oxygen-volume + Al/O | 1.2774 | separable |

This is an inflection point. The packed-framework hypothesis is no longer blocked by descriptor collinearity once scale is handled correctly. It is still not validated, because no fresh RI target has been scored and topology-class fitting remains under-sampled.

## Pattern Reading

The emerging pattern is not "composition predicts RI." It is closer to:

> Refractive index appears to require a packed-framework descriptor: topology plus charge accounting plus a density/polarizability bridge.

The earlier NBO/T and framework-Al models fail because they treat framework charge and modifier identity as scalar labels. The failures suggest the missing variable is physical embedding: how tightly the framework is packed and how strongly the modifier cation polarizes or loosens that packing.

In invisible-origami language:

- two networks can have similar crease counts but different folded compactness;
- a larger cation can hold the same charge role while changing local spacing;
- a denser framework can increase optical response without changing simple NBO/T;
- an Al-rich framework can overpredict if its fold/packing class differs from the feldspar calibration class.

## Current Warnings

- Do not promote the density/Lorentz-Lorenz model while the condition number remains above the guardrail.
- Use standardized feature conditioning for descriptor-design guardrails; raw condition numbers are scale-sensitive and should not alone block a model family.
- Do not solve this by adding another scalar coefficient to the current RI benchmark.
- Do not use kalsilite/nepheline/feldspathoid behavior as validation for a feldspar-fit framework term unless topology class is explicit.
- Treat "fold density" as a pointer to measurable descriptors, not as an evidential claim.

## Claude Check-In Question

Claude was checked through the `sudo -u cello` environment on 2026-05-16 with this narrow question:

> We found that raw condition numbers blocked a refractive-index descriptor family using density/packing, Al/O, and cation field response, but standardized non-intercept feature conditioning gives low condition numbers between 1.28 and 2.35. Does this justify moving from "descriptor family blocked" to "descriptor family numerically separable but still unvalidated," provided no fresh RI target is scored yet and topology-class fitting remains under-sampled?

Claude's methodological answer: yes, that status change is sound. The cautions were:

- standardized conditioning proves numerical separability, not predictive validity;
- topology-class under-sampling remains the primary risk;
- scaler/standardization parameters must be derived from training rows only when a fresh target is scored;
- coefficient signs and magnitudes should be recorded before scoring;
- candidate families should remain parallel through at least one fresh validation round.

## Current-Corpus Coefficient Reading

The descriptor diagnostic now records current-corpus Lorentz-Lorenz coefficients before any future fresh RI target is selected. These are not validation coefficients.

| Feature family | Max abs LL residual | Coefficient sign reading |
|---|---:|---|
| density + Al/O + cation-response/O | 0.00153865 | all positive |
| oxygen-volume + Al/O + cation-response/O | 0.01676366 | all positive |
| T-packing + Al/O + cation-response/O | 0.01251646 | T-packing negative; Al/O and cation response positive |
| minimal oxygen-volume + cation-response/O | 0.03157709 | all positive |
| minimal oxygen-volume + Al/O | 0.01688174 | oxygen-volume negative; Al/O positive |

This changes the immediate ranking. The lowest standardized condition number is not automatically the best next design. The density family gives the best current-corpus residual and has physically straightforward positive signs. The minimal oxygen-volume + Al/O family has the cleanest standardized condition and an interpretable negative oxygen-volume sign, but its residual is much larger. The oxygen-volume + Al/O + cation-response family is separable but its positive oxygen-volume sign is harder to read as "looser packing lowers RI."

## Fresh Gehlenite Validation

A fresh sorosilicate RI validation was run in `analysis/external-ri-gehlenite-fresh-validation.mjs` after freezing two candidate families:

- density + Al/O + cation-response/O;
- minimal oxygen-volume + Al/O.

Target: Ca2Al2SiO7 gehlenite, scalar RI 1.66217 at 632.8 nm, computed as `(2*n_o + n_e)/3` from Burshtein, Shimony, and Levy, JOSA A 10, 2246-2247 (1993), where `n_o = 1.665` and `n_e - n_o = -0.0085`.

| Candidate family | Predicted RI | Measured RI | Error | Pass |
|---|---:|---:|---:|---|
| density + Al/O + cation-response/O | 1.62573 | 1.66217 | 0.03644 | no |
| minimal oxygen-volume + Al/O | 1.57186 | 1.66217 | 0.09031 | no |

Both frozen families failed. This is a real topology-transfer failure, not a marginal tolerance miss.

A post-failure bridge-oxygen diagnostic was also tested:

| Diagnostic | Predicted RI | Error | Reading |
|---|---:|---:|---|
| density + Al/O + cation-response/O + bridge-O fraction | 1.62615 | 0.03602 | no meaningful repair |

This rules out the simplest bridge-oxygen-fraction explanation. The missing term is more likely melilite/sorosilicate-specific embedding: Ca coordination environment, tetrahedral Al site role, electronic polarizability, or topology class itself, rather than generic bridge count.

## Next Useful Move

The next descriptor should reduce degeneracy before any fresh RI target is scored. The strongest candidates are:

1. topology class: glass, feldspar framework, feldspathoid framework, sorosilicate, chain/ring/sheet where relevant;
2. molar volume or density-normalized formula volume;
3. Lorentz-Lorenz-compatible molar refraction rather than raw refractive index;
4. cation polarizability or field strength as a typed modifier response, not only valence;
5. Al/O or Al/T separated by topology class, because oxygen-normalized Al extrapolated too high into feldspathoids.

The immediate research recommendation is diagnostic: expand the exposed descriptor table with topology class and molar-volume-compatible quantities, then rerun pre-lookup guardrails. Only if the design becomes well-conditioned should a new held-out RI row be selected.

After gehlenite, the immediate next move should be restrained:

1. Do not add a promoted repair term from gehlenite.
2. Add a melilite/sorosilicate diagnostic table that separates Ca coordination, tetrahedral Al role, and topology class from generic density/Al/O.
3. Reserve a second melilite-family target, preferably akermanite Ca2MgSi2O7 if source density and RI can be anchored, before changing any coefficients.
4. Treat gehlenite as evidence that scalar packing descriptors are insufficient across topology class.

## Melilite Topology Diagnostic

`analysis/ri-melilite-topology-diagnostic.mjs` now separates gehlenite, akermanite, and anorthite by topology class, Ca scaffold, T-site chemistry, oxygen volume, and non-tetrahedral charge.

Key contrast:

| Contrast | O volume delta | T Al fraction delta | Non-T charge/O delta | Measured RI delta | Reading |
|---|---:|---:|---:|---:|---|
| gehlenite vs anorthite | 0.51167 | 0.16667 | 0.32143 | 0.0805 | same broad Ca-Al-Si-O family, but melilite topology and Ca scaffold raise RI beyond scalar packing descriptors |
| gehlenite vs akermanite | -0.08527 | 0.66667 | 0 | pending | same melilite Ca scaffold; isolates T-site Al/Mg-Si chemistry if RI source is confirmed |

Akermanite is now the natural reserved target. It should not be scored from weak secondary snippets. Use it only after confirming a source-table RI value, ideally ordinary/extraordinary indices with wavelength or a reputable handbook/mineral-data value.

## Source-Qualified Akermanite Check

Akermanite was scored only as a source-qualified check, not as a paper-grade validation, using Webmineral's Akermanite Mineral Data table: density 2.944, `w = 1.632`, `e = 1.64`. The scalar target is `(2*w + e)/3 = 1.63467`. The source does not specify wavelength or uncertainty.

| Candidate family | Predicted RI | Measured RI | Error | Pass |
|---|---:|---:|---:|---|
| density + Al/O + cation-response/O | 1.57197 | 1.63467 | 0.0627 | no |
| minimal oxygen-volume + Al/O | 1.49063 | 1.63467 | 0.14404 | no |

This strengthens the gehlenite reading. The issue is not only tetrahedral Al in gehlenite: akermanite removes T-site Al but still fails badly. The missing signal is broader melilite/sorosilicate transfer or Ca-rich scaffold response. Treat this as source-qualified support, not as a primary validation row.

## Ca-Scaffold Response Diagnostic

`analysis/ri-ca-scaffold-response-diagnostic.mjs` isolates the variable-type problem exposed by akermanite.

| Row | Ca/O | Non-T charge/O | Al/O | Current cation-response/O | Density-family residual | Reading |
|---|---:|---:|---:|---:|---:|---|
| anorthite | 0.125 | 0.25 | 0.25 | 0.21905 | -0.00245 | Ca-bearing feldspar is handled reasonably |
| gehlenite | 0.28571 | 0.57143 | 0.28571 | 0.25034 | 0.03644 | high-Ca melilite underpredicted |
| akermanite | 0.28571 | 0.57143 | 0 | 0 | 0.0627 | Ca scaffold present, but current cation-response disappears |

This is the cleanest current diagnosis. The existing cation-response variable is not a general cation/polarizability variable. It is an Al-charge-compensation variable. That was adequate inside feldspar-like aluminosilicate rows, but it is structurally wrong for akermanite: Ca remains a dense non-tetrahedral scaffold even when there is no Al to compensate.

Next repair boundary:

- separate charge-compensation role from scaffold role;
- represent non-tetrahedral Ca/Mg per oxygen or per volume separately from Al/O;
- keep topology class explicit, because Ca in feldspar and Ca in melilite do not behave as the same scalar context;
- do not promote a repair from gehlenite/akermanite until another source-anchored target is reserved.

## Ca-Scaffold Repair Diagnostic

`analysis/ri-ca-scaffold-repair-diagnostic.mjs` tests the post-failure repair implied by the Ca-scaffold diagnosis. This is calibration debt because the split was introduced after the melilite failures.

| Family | Max abs residual | Gehlenite residual | Akermanite residual | Reading |
|---|---:|---:|---:|---|
| baseline density + Al/O + Al-comp response | 0.01881 | 0.0096 | 0.01356 | still misses melilite rows |
| split Ca scaffold family | 0.00423 | 0.00163 | -0.00056 | Ca/O split explains current melilite failures |
| split Ca/Mg scaffold family | 0.00436 | 0.00051 | 0 | Mg split adds local precision but is not yet justified |

This is a strong diagnostic result, but not a validation result. It supports the variable-type diagnosis: the earlier cation-response variable was too narrow because it represented Al charge compensation, not non-tetrahedral Ca scaffold response.

Claude check-in on 2026-05-16 agreed with this reading and warned that the residual collapse is too clean to trust without a fresh target. The unvalidated piece is the Ca scaffold term.

Recommended next target type:

1. hardystonite Ca2ZnSi2O7 if a strong RI source can be found: same melilite/Ca scaffold, no tetrahedral Al, Zn replacing Mg;
2. then a non-melilite Ca silicate such as merwinite or rankinite to test transfer outside melilite topology.

Do not promote the Ca scaffold repair unless a source-anchored hardystonite or equivalent is scored without refitting.

## Hardystonite Ca-Scaffold Validation

`analysis/external-ri-hardystonite-ca-scaffold-validation.mjs` scored hardystonite Ca2ZnSi2O7 as the fresh same-topology Ca-scaffold test after the Ca split was frozen.

Primary source: Handbook of Mineralogy hardystonite PDF, `D(meas.) = 3.396-3.443`, `omega = 1.669`, `epsilon = 1.657`; scalar RI `(2*omega + epsilon)/3 = 1.665`. Alternate Webmineral/Mindat values give scalar RI 1.66833.

| Family | Predicted RI | Primary RI | Primary error | Alternate RI | Alternate error | Pass |
|---|---:|---:|---:|---:|---:|---|
| split Ca scaffold | 1.72018 | 1.665 | 0.05518 | 1.66833 | 0.05185 | no |
| split Ca/Mg scaffold | 1.72683 | 1.665 | 0.06183 | 1.66833 | 0.0585 | no |

This fails in the opposite direction from gehlenite/akermanite. The Ca scaffold split fixed two melilite rows by raising predictions, then overpredicted the Zn melilite hardystonite.

Claude Opus check-in on 2026-05-16:

- this does not falsify Ca as a relevant descriptor, but it falsifies Ca scaffold as a sufficient general melilite variable;
- the direction flip shows the Ca scaffold term was absorbing variance that belongs to T1 cation chemistry;
- T1 occupancy is the actual changing variable across gehlenite/akermanite/hardystonite: Al -> Mg -> Zn while the Ca site is invariant;
- Zn is diagnostic because its contribution is not passed through additively; the T1 topology appears to buffer cation polarizability;
- the Ca scaffold term should be demoted to a covariate until an explicit T1 cation polarizability x T1-site topology term is tested.

Methodological reading: hardystonite is a useful failure. It confirms the validation process is exposing confounded variables rather than merely fitting rows.

## Melilite T1-Cation Diagnostic

`analysis/ri-melilite-t1-cation-diagnostic.mjs` records a first T1-cation diagnostic. The radius values are source-anchored. The polarizability values now include source-anchored dielectric scales, but those scales are not promoted as optical-RI validation predictors without a frozen conversion or calibration rule.

Source status:

- T1 tetrahedral ionic radii are source-anchored enough for descriptor diagnosis: Shannon effective ionic radii, reproduced in accessible radius tables, give Al3+ IV 0.39 A, Mg2+ IV 0.57 A, Zn2+ IV 0.60 A.
- T1 cation polarizabilities are source-anchored for descriptor diagnosis through the public Qin et al. 2023 ion dielectric polarizability database. That database records Shannon no-coordination values and coordination-specific MLR/ML values, including CN=4 values for Al3+, Mg2+, and Zn2+.
- The polarizability table is not yet optical-validation-grade. It is a dielectric-polarizability source, so an optical RI model needs an explicit frozen conversion, scale choice, or calibration rule before scoring another melilite.

| Melilite | T1 cation | Shannon no-CN polarizability | MLR CN4 polarizability | ML-extended CN4 polarizability | Measured RI | Ca-scaffold prediction | Ca-scaffold residual |
|---|---|---:|---:|---:|---:|---:|---:|
| gehlenite | Al | 0.79 | 1.5649 | 1.2527 | 1.66217 | 1.66054 | 0.00163 |
| akermanite | Mg | 1.32 | 2.07 | 1.9571 | 1.63467 | 1.63523 | -0.00056 |
| hardystonite | Zn | 2.04 | 2.7618 | 2.4089 | 1.665 | 1.72018 | -0.05518 |

Orderings:

- all three dielectric polarizability scales: Al < Mg < Zn.
- Measured RI: Mg < Al < Zn.
- Ca-scaffold residual: Zn is strongly negative while Al/Mg are near zero.

This rules out a simple monotonic free-ion polarizability pass-through. The better hypothesis is buffered T1 response: the melilite T1 site gates cation polarizability, especially for Zn, rather than adding it directly to RI.

Next model boundary:

- keep Ca scaffold as a topology baseline, not a full response term;
- choose and freeze one descriptor rule for T1 identity or dielectric-polarizability scale before using polarizability in validation;
- test an explicit T1 identity / polarizability x topology-buffer term;
- do not score another melilite until that scale choice and model form are frozen.

## Melilite T1 Field-Buffer Diagnostic

`analysis/ri-melilite-t1-field-buffer-diagnostic.mjs` splits the T1 effect into physical sub-descriptors: charge/radius, field strength `z/r2`, CN4 dielectric polarizability, polarizability normalized by charge and radius, and a Zn d10 class marker.

| Melilite | T1 class | Field z/r2 | MLR CN4 polarizability | d10 flag | Measured RI | Ca-scaffold residual |
|---|---|---:|---:|---:|---:|---:|
| gehlenite | trivalent high-field network former | 19.723866 | 1.5649 | 0 | 1.66217 | 0.00163 |
| akermanite | divalent s-block tetrahedral cation | 6.15574 | 2.07 | 0 | 1.63467 | -0.00056 |
| hardystonite | divalent d10 tetrahedral cation | 5.555556 | 2.7618 | 1 | 1.665 | -0.05518 |

The result sharpens the model-form boundary. Raw polarizability remains the wrong validation descriptor by itself: it orders Al < Mg < Zn, while measured RI orders Mg < Al < Zn. Field strength separates Al from the divalent T1 cations. The d10 class separates Zn from Mg despite their similar charge and radius and explains why hardystonite is the diagnostic failure.

The next frozen form should be:

1. Ca scaffold as melilite topology baseline;
2. T1 high-field term for Al-like occupancy;
3. T1 d10 / covalency class marker for Zn-like occupancy;
4. no raw polarizability pass-through unless a conversion/calibration rule is frozen first.

This remains calibration debt with only three melilite rows. The next validation should either test one of these existing T1 classes without adding a new class, or move outside melilite to test Ca-scaffold transfer independently of T1 chemistry.

## Melilite T1-Buffer Freeze Contract

`analysis/ri-melilite-t1-buffer-freeze-contract.mjs` freezes the next model form before any further RI lookup or scoring. It is not a fitted predictor. It has no new coefficients and scores no new material.

Allowed descriptor contract:

| Descriptor | Frozen use |
|---|---|
| Ca scaffold baseline | may shift melilite RI upward relative to feldspar/glass calibration, but cannot absorb T1 chemistry |
| T1 high-field term | separates trivalent high-field T1 cations from divalent Mg/Zn-like T1 cations |
| T1 d10 class | prevents Zn dielectric polarizability from being passed through additively |
| T1 dielectric polarizability | may be recorded as an ordered descriptor only; no direct optical pass-through without a frozen conversion rule |

Rejected shortcuts:

- raw cation response = Al/O x cation-field delta, because it collapses to zero for akermanite even though Ca scaffold remains optically important;
- raw T1 polarizability pass-through, because Al < Mg < Zn conflicts with measured Mg < Al < Zn behavior;
- Ca scaffold as a sufficient melilite variable, because hardystonite overprediction shows the Ca term absorbed T1 chemistry variance.

Frozen falsifiers:

| Expectation | Falsifier |
|---|---|
| Zn-like T1 occupancy should not inherit the full Ca-scaffold uplift | a fresh Zn-like melilite lands accurately on Ca-scaffold-only prediction without a Zn buffer |
| Mg-like T1 occupancy should stay closer to the Ca baseline than Zn-like occupancy | a fresh Mg-like melilite shows a hardystonite-like negative residual |
| Al-like high-field occupancy should not be inferred from dielectric polarizability | a fresh Al-like row follows raw polarizability ordering rather than high-field behavior |
| non-melilite Ca scaffold transfer should weaken if melilite topology is the carrier | a Ca-rich non-melilite silicate is accurately predicted by melilite Ca-scaffold baseline without topology adjustment |

Next target ranking:

1. same-class melilite repeat, if a source-grade Zn-, Mg-, or Al-bearing row can be found;
2. rankinite-like Ca silicate, because it removes Mg/Al/Zn T1 chemistry while retaining a Ca-rich silicate substrate;
3. wollastonite-like Ca chain silicate, as a broader Ca-scaffold transfer falsifier;
4. merwinite-like Ca-Mg silicate, useful but less clean because it mixes Mg chemistry and topology transfer.

## Rankinite Target Prequalification

`analysis/ri-rankinite-target-prequalification.mjs` source-qualifies rankinite Ca3Si2O7 as the next reserved Ca-scaffold transfer target if a same-class melilite repeat cannot be found first. No prediction was made and no coefficients were changed.

Primary source: Handbook of Mineralogy rankinite PDF. Secondary cross-check: Webmineral rankinite page.

| Property | Value | Policy |
|---|---:|---|
| D(meas.) | 2.96-3.00 | use measured-density midpoint unless sample-specific density is found before scoring |
| D(calc.) | 2.99-3.00 | record only |
| alpha | 1.640-1.643 | Handbook range |
| beta | 1.643-1.646 | Handbook range |
| gamma | 1.650-1.652 | Handbook range |
| Scalar RI range | 1.644333-1.647 | `(alpha + beta + gamma) / 3` |
| Scalar RI midpoint | 1.645667 | reserved target value for future scoring only |
| Lorentz-Lorenz midpoint | 0.36281636 | reserved LL target value for future scoring only |

Rankinite is useful because it is a Ca-rich sorosilicate without Mg/Al/Zn T1 chemistry. It tests whether the melilite Ca-scaffold baseline transfers outside melilite topology. That makes it a topology-transfer falsifier, not a direct melilite T1-buffer validation row.

Decision point:

- if a source-grade same-class melilite repeat can be found, prefer that next;
- otherwise score rankinite deliberately as a non-melilite Ca-scaffold transfer test under the frozen contract.

## Melilite Repeat Target Screen

`analysis/ri-melilite-repeat-target-screen.mjs` checked whether a same-class melilite repeat should precede rankinite. No candidate was scored.

| Candidate | Formula | Scalar RI | Source strength | Class-fit reading | Decision |
|---|---|---:|---|---|---|
| gugiaite | Ca2BeSi2O7 | 1.666667 | Handbook-backed | same melilite topology, but introduces Be T1 chemistry | defer |
| alumoakermanite | (Ca,Na)2(Al,Mg,Fe2+)(Si2O7) | 1.632 | Handbook-backed | same melilite topology, but mixed Ca/Na and Al/Mg/Fe chemistry | defer |
| rankinite | Ca3Si2O7 | 1.645667 | Handbook-backed with Webmineral cross-check | not melilite; clean Ca-rich scaffold transfer target with no Mg/Al/Zn T1 chemistry | prefer for next falsifier if no pure same-class melilite is found |

Gugiaite and alumoakermanite are useful later rows, but they are not clean repeats of the frozen Al/Mg/Zn T1 classes. Gugiaite adds Be as a new high-field T1 chemistry class. Alumoakermanite has mixed Ca/Na and Al/Mg/Fe occupancy. Promoting either before rankinite would blur the next test.

This resolves the decision point: rankinite is the cleaner next scoring target if the next question is topology-gated Ca-scaffold transfer.

## Rankinite Ca-Scaffold Transfer Validation

`analysis/external-ri-rankinite-ca-scaffold-transfer-validation.mjs` scored rankinite as the non-melilite Ca-scaffold transfer test under the frozen contract. This does not validate the melilite T1-buffer model. It asks whether the Ca-scaffold uplift that repaired gehlenite/akermanite transfers to a Ca-rich sorosilicate with different topology and no Mg/Al/Zn T1 chemistry.

Target:

| Measure | Value |
|---|---:|
| Formula | Ca3Si2O7 |
| Density used | 2.98 |
| Ca/O | 0.42857 |
| Oxygen volume | 13.82536 |
| Scalar RI range | 1.644333-1.647 |
| Scalar RI midpoint | 1.645667 |

Frozen candidate results:

| Candidate family | Predicted RI | Error | Pass | Residual |
|---|---:|---:|---|---:|
| baseline density + Al/O + Al-comp response | 1.63042 | 0.01525 | no | 0.01525 |
| split Ca scaffold family | 1.67378 | 0.02811 | no | -0.02811 |
| split Ca/Mg scaffold family | 1.68211 | 0.03644 | no | -0.03644 |

Status: rankinite supports topology-gated Ca-scaffold interpretation. The Ca-scaffold family fails transfer and overpredicts the Ca-rich non-melilite target. This means Ca scaffold cannot be reused as a transferable scalar without topology. It also should not be used to fit a new topology term yet; the result only justifies making topology an explicit gate before any further Ca-scaffold scoring.

Claude Opus check-in on 2026-05-16 agreed with the cautious interpretation:

- the no-Ca-scaffold baseline underpredicts rankinite, while the Ca-scaffold variants overpredict it;
- the overprediction grows as the scaffold term is made more explicit;
- this is consistent with a Ca response that worked inside melilite but overshoots in rankinite's different Si2O7 topology;
- the result falsifies scalar Ca-scaffold transfer, but does not identify the topology gate's functional form.

Methodological caveat: this is a single non-melilite falsifier. It cannot yet distinguish a real topology descriptor, such as bridge count, Si-O-Si angle, polyhedral connectivity, or oxygen-volume/fold-density class, from an unrelated rankinite-specific term. The next target should vary topology while keeping the Mg/Al/Zn-free Ca-silicate cation set as fixed as possible.

## Ca-Silicate Topology Target Screen

`analysis/ri-ca-silicate-topology-target-screen.mjs` screened the next target after the rankinite transfer failure. The goal was to vary topology while keeping the cation set as close as possible to Ca-Si-O. No candidate was scored.

| Candidate | Formula | Density | Scalar RI midpoint | Topology contrast | Decision |
|---|---|---:|---:|---|---|
| kilchoanite | Ca3Si2O7 | 2.992 | 1.648167 | dimorphous with rankinite; same ideal formula but different topology | promote next |
| larnite | Ca2SiO4 | 3.305 | 1.719667 | Ca-only silicate, but formula and polymerization differ strongly | defer |
| wollastonite | CaSiO3 | 2.975 | 1.636333 | Ca-only chain silicate, but Handbook density/optical ranges are broad | defer |

Kilchoanite is the cleanest topology discriminator because it is dimorphous with rankinite and keeps Ca3Si2O7 fixed. This makes it better than larnite or wollastonite for distinguishing a real topology gate from a rankinite-specific anomaly.

Next scoring boundary: score kilchoanite against the same frozen Ca-scaffold transfer families. If rankinite and kilchoanite behave differently despite the same formula, topology gating becomes much more concrete. If both fail similarly, the missing term may be broader Ca3Si2O7 / dimer-substrate behavior rather than a rankinite-specific topology issue.

## Kilchoanite Ca-Scaffold Transfer Validation

`analysis/external-ri-kilchoanite-ca-scaffold-transfer-validation.mjs` scored kilchoanite as the paired-polymorph topology discriminator after rankinite. It keeps the same ideal formula, Ca3Si2O7, but changes topology. This does not validate the melilite T1-buffer model.

Target:

| Measure | Value |
|---|---:|
| Formula | Ca3Si2O7 |
| Density used | 2.992 |
| Ca/O | 0.42857 |
| Oxygen volume | 13.76991 |
| Scalar RI range | 1.648-1.648333 |
| Scalar RI midpoint | 1.648167 |

Frozen candidate results:

| Candidate family | Predicted RI | Error | Pass | Residual |
|---|---:|---:|---|---:|
| baseline density + Al/O + Al-comp response | 1.63354 | 0.01463 | no | 0.01463 |
| split Ca scaffold family | 1.67592 | 0.02775 | no | -0.02775 |
| split Ca/Mg scaffold family | 1.68428 | 0.03611 | no | -0.03611 |

Rankinite/kilchoanite pair:

| Measure | Rankinite | Kilchoanite |
|---|---:|---:|
| Density | 2.98 | 2.992 |
| Scalar RI midpoint | 1.645667 | 1.648167 |
| Split Ca scaffold predicted RI | 1.67378 | 1.67592 |
| Split Ca scaffold residual | -0.02811 | -0.02775 |

Status: kilchoanite supports topology-gated Ca-scaffold interpretation, but not by isolating a rankinite-vs-kilchoanite optical difference. Instead, the pair shows that Ca3Si2O7 polymorphs have very similar scalar RI and both reject the melilite-derived Ca-scaffold uplift. The missing gate is therefore broader than a rankinite-specific anomaly: Ca scaffold needs topology/fold-density context before transfer outside melilite.

## Ca-Scaffold Topology-Gate Diagnostic

`analysis/ri-ca-scaffold-topology-gate-diagnostic.mjs` consolidates the melilite, rankinite, and kilchoanite Ca-scaffold results. It does not fit a repair term.

| Material | Topology gate class | Ca/O | O volume | Measured RI | Split Ca prediction | Split Ca residual |
|---|---|---:|---:|---:|---:|---:|
| gehlenite | melilite sheet scaffold | 0.285714 | 13.157262 | 1.66217 | 1.66054 | 0.00163 |
| akermanite | melilite sheet scaffold | 0.285714 | 13.229037 | 1.63467 | 1.63523 | -0.00056 |
| rankinite | Ca3Si2O7 polymorph scaffold | 0.428571 | 13.82536 | 1.645667 | 1.67378 | -0.028113 |
| kilchoanite | Ca3Si2O7 polymorph scaffold | 0.428571 | 13.76991 | 1.648167 | 1.67592 | -0.027753 |

Group summary:

| Topology gate class | Mean Ca/O | Mean O volume | Mean measured RI | Mean split-Ca residual |
|---|---:|---:|---:|---:|
| melilite sheet scaffold | 0.285714 | 13.19315 | 1.64842 | 0.000535 |
| Ca3Si2O7 polymorph scaffold | 0.428571 | 13.797635 | 1.646917 | -0.027933 |

Gate rules:

- Ca/O is not transferable by itself: Ca3Si2O7 polymorphs have higher Ca/O than melilites but are overpredicted by the melilite-derived Ca scaffold term.
- Oxygen volume is not sufficient by itself: melilite and Ca3Si2O7 rows are close enough in oxygen volume that volume alone does not explain the residual sign.
- Topology gate must remain categorical until a structural descriptor is sourced: rankinite and kilchoanite share formula and similar RI, so the gate separates melilite sheet scaffold from Ca3Si2O7 polymorph scaffold, not rankinite alone.

Next descriptor need: source structural descriptors for melilite vs Ca3Si2O7 topology: Si2O7 linkage geometry, Ca coordination/polyhedral connectivity, and bridge oxygen environment. Do not fit a topology coefficient from two melilites plus two Ca3Si2O7 polymorphs.

## Structural Gate Source Diagnostic

`analysis/ri-structural-gate-source-diagnostic.mjs` sources the structural side of the Ca-scaffold gate. No optical target was scored and no repair term was fit.

| Material / class | Gate class | Ca environment | Silicate unit | Source status |
|---|---|---|---|---|
| akermanite / melilite prototype | melilite sheet scaffold | CaO8 polyhedral layer between tetrahedral layers | isolated Si2O7 or related melilite tetrahedral sheet units | prototype/source-backed descriptor |
| rankinite | Ca-polyhedra sheet plus inserted disilicate | Ca coordination-polyhedra sheets | inserted Si2O7 groups | primary abstract-backed descriptor |
| kilchoanite | Ca3Si2O7 polymorph / mixed silicate-unit scaffold | multiple Ca sites; manganoan analogue reports four octahedral sites | SiO4 plus Si3O10 structural description | Handbook plus primary abstract-backed descriptor |

Source-backed descriptor candidates:

- Ca polyhedral environment class: melilite CaO8 layer vs rankinite Ca-polyhedra sheets vs kilchoanite multiple Ca sites.
- Silicate-unit connectivity class: melilite Si2O7/related tetrahedral sheet units; rankinite inserted Si2O7; kilchoanite SiO4 + Si3O10 structural description.
- Bridge oxygen overbonding / Si-O-Si angle class: promising, but exact values must be sourced before numeric use.

Rejected descriptor candidates:

- ideal formula class, because rankinite and kilchoanite share ideal Ca3Si2O7 but have distinct structural descriptions and similar optical response;
- Ca/O scalar, because Ca3Si2O7 rows have higher Ca/O yet are overpredicted by melilite-derived Ca scaffold;
- oxygen-volume scalar alone, because it does not distinguish residual sign cleanly across melilite and Ca3Si2O7 rows.

Important nuance: kilchoanite should not be treated as simply "rankinite with different topology." The Handbook cites the crystal structure as Ca6(SiO4)(Si3O10), and the manganoan kilchoanite structure work reports multiple Ca/Mn sites and Si-O-Si angle systematics. The safe gate is structural and categorical until exact bridge-angle and coordination descriptors are sourced.

## Node Modelling Chain

The refractive-index work is currently modelled as deterministic Node scripts under `analysis/`. Each script writes Markdown and JSON outputs under `analysis/out/`.

`analysis/ri-refractive-index-chain-runner.mjs` now regenerates the current RI chain in order:

```sh
node analysis/ri-refractive-index-chain-runner.mjs
```

The runner deliberately does not update `package.json`, because the package manifest already has unrelated local edits. The current chain contains 33 RI scripts and has been verified with all steps exiting 0.

## Structural Numeric-Readiness Diagnostic

`analysis/ri-structural-numeric-readiness-diagnostic.mjs` records which structural-gate descriptors are ready for modelling after the first source pass. No optical target was scored and no repair term was fit.

| Material / class | Ca coordination | Ca bond metric | Bridge-angle status |
|---|---|---|---|
| melilite prototype / akermanite class | 8 | CaO8 polyhedral layer; exact Ca-O distances not extracted | not source-extracted |
| rankinite | 7 in older structure summary; newer abstract gives Ca-polyhedra sheets | Ca-O 2.25-2.90 A in older summary | not source-extracted; bridge Si-O bonds are longer than nonbridge bonds |
| kilchoanite / manganoan analogue | four octahedral M sites in manganoan analogue | M-O means: 2.538, 2.380, 2.307, 2.346 A | not exact for pure kilchoanite; source links smaller Si-O-Si angles to higher bridge-O coordination |

Readiness boundary:

- ready now: categorical Ca coordination class, categorical silicate-unit connectivity class, source-status flags;
- partly ready: Ca bond-length ranges / mean M-O distances;
- blocked now: numeric Si-O-Si angle coefficient, numeric bridge oxygen coordination coefficient, continuous Ca bond-length correction across melilite/rankinite/kilchoanite.

This updated the runner to 19 RI scripts. The next quantitative step required comparable structure tables or CIF-derived values for melilite, rankinite, and kilchoanite.

## CIF Geometry Extraction Diagnostic

`analysis/ri-cif-geometry-extraction-diagnostic.mjs` now computes first-pass structural descriptors from COD CIF coordinates for gehlenite, akermanite, rankinite, and kilchoanite. This does not score a new optical target and does not fit a repair term.

Sources:

| Material | COD | Reference |
|---|---|---|
| gehlenite | 1000048 | Swainson et al. 1992, neutron diffraction study of the akermanite-gehlenite solid-solution series |
| akermanite | 9006935 | Kusaka et al. 2001, Ca2MgSi2O7 structure at 297 K |
| rankinite | 9012094 | Saburi et al. 1976, refinement of rankinite |
| kilchoanite | 9009443 | Taylor 1971, crystal structure of kilchoanite, Ca6(SiO4)(Si3O10) |

Fixed cutoffs:

| Descriptor family | Cutoff |
|---|---:|
| T-O bond neighborhood | 1.95 A |
| Ca/M-O scaffold neighborhood | 3.05 A |

Extracted descriptor candidates:

| Material | Bridge angle summary | Scaffold coordination summary | Mean scaffold distance summary |
|---|---:|---:|---:|
| gehlenite | 119.223-134.046 deg; mean 126.6345; n=2 | 8-8; mean 8 | 2.565838 A |
| akermanite | 119.064-139.177 deg; mean 129.1205; n=2 | 8-8; mean 8 | 2.574719 A |
| rankinite | 136.232 deg; n=1 | 7-7; mean 7 | 2.424649-2.514113 A; mean 2.467712 |
| kilchoanite | 117.474 deg; n=1 | 6-8; mean 6.5 | 2.364442-2.506952 A; mean 2.408663 |

Bridge rows:

| Material | Bridge row |
|---|---|
| gehlenite | O1: T2@1.6928 / T2@1.6928, angle 134.046 deg |
| gehlenite | O3: T2@1.6844 / Al1@1.7502, angle 119.223 deg |
| akermanite | O1: Si@1.6516 / Si@1.6516, angle 139.177 deg |
| akermanite | O3: Si@1.6076 / Mg@1.9206, angle 119.064 deg |
| rankinite | O4: Si1@1.6576 / Si2@1.6774, angle 136.232 deg |
| kilchoanite | O6: Si2@1.7068 / Si3@1.7166, angle 117.474 deg |

Scaffold rows:

| Material | Scaffold row |
|---|---|
| gehlenite | Ca1: coordination 8, mean Ca-O 2.565838 A |
| akermanite | Ca: coordination 8, mean Ca-O 2.574719 A |
| rankinite | Ca1/Ca2/Ca3: coordination 7, mean Ca-O 2.514113 / 2.424649 / 2.464375 A |
| kilchoanite | Ca1/Ca2/Ca3/Ca4: coordination 8 / 6 / 6 / 6, mean Ca-O 2.506952 / 2.394811 / 2.364442 / 2.368448 A |

Readiness boundary:

- promoted to CIF-derived candidate: bridge angle, Ca coordination count, mean Ca-O scaffold distance;
- still not coefficient-ready: bridge-angle and scaffold-distance optical terms, because the values depend on symmetry expansion, cutoff choice, and source CIF quality;
- safe immediate use: diagnostic separation of melilite sheet scaffold from Ca3Si2O7 polymorph scaffolds, replacing the previous fully blocked status for numeric structural descriptors.

This updated the runner to 20 RI scripts. The next modelling step was to test whether these CIF-derived descriptors separate the melilite-vs-Ca3Si2O7 residual pattern more cleanly than Ca/O and oxygen volume, without fitting a new optical coefficient from this tiny set.

## CIF Residual-Separation Diagnostic

`analysis/ri-cif-residual-separation-diagnostic.mjs` joins the CIF-derived local geometry to the frozen split-Ca residuals. It does not fit a new optical coefficient. It asks which physical geometry variables line up with the residual sign.

Important caveat: this is still a four-row diagnostic, not a model fit. The geometry values depend on the source CIF, symmetry expansion, and fixed cutoffs.

Joined rows:

| Material | Topology gate class | Split-Ca residual | Ca/O | O volume | Bridge angle mean | Ca coord mean | Mean Ca-O | Geometry status |
|---|---|---:|---:|---:|---:|---:|---:|---|
| gehlenite | melilite sheet scaffold | 0.00163 | 0.285714 | 13.157262 | 126.6345 | 8 | 2.565838 | available |
| akermanite | melilite sheet scaffold | -0.00056 | 0.285714 | 13.229037 | 129.1205 | 8 | 2.574719 | available |
| rankinite | Ca3Si2O7 polymorph scaffold | -0.028113 | 0.428571 | 13.82536 | 136.232 | 7 | 2.467712 | available |
| kilchoanite | Ca3Si2O7 polymorph scaffold | -0.027753 | 0.428571 | 13.76991 | 117.474 | 6.5 | 2.408663 | available |

Geometry group summary:

| Topology gate class | Materials | Mean residual | Mean bridge angle | Mean Ca coord | Mean Ca-O |
|---|---|---:|---:|---:|---:|
| melilite sheet scaffold | gehlenite, akermanite | 0.000535 | 127.8775 | 8 | 2.570278 |
| Ca3Si2O7 polymorph scaffold | rankinite, kilchoanite | -0.027933 | 126.853 | 6.75 | 2.438188 |

Readings:

- Ca scaffold geometry is more instructive than bridge angle as the first quantitative gate: gehlenite and akermanite have Ca coordination 8 and near-zero split-Ca residuals, while rankinite/kilchoanite have lower coordination means and roughly -0.028 split-Ca residuals.
- Bridge angle is topology-specific but not monotone against the residual in this small set: rankinite is 136.232 deg and kilchoanite is 117.474 deg, yet both have nearly identical negative residuals.
- The emerging physical motif is Ca scaffold compaction / coordination change, not simply "more Ca raises RI." Ca3Si2O7 rows show shorter mean Ca-O distances and lower effective coordination than the melilite rows, while the melilite-derived Ca uplift overpredicts RI.

Boundary: do not fit a threshold or coefficient from this. The next safe step is to use the now-paired melilite geometry rows to define candidate gate tests, then reserve a new held-out Ca-silicate target before any coefficient or threshold is proposed.

This updated the runner to 21 RI scripts.

## CIF Candidate-Gate Diagnostic

`analysis/ri-cif-candidate-gate-diagnostic.mjs` turns the four-row CIF residual separation into explicit candidate gate tests. It does not fit a coefficient and does not promote a threshold. A gate can only be used as a held-out validation hypothesis.

Group centres:

| Group | Materials | Mean residual | Mean Ca coordination | Mean Ca-O | Mean bridge angle |
|---|---|---:|---:|---:|---:|
| melilite sheet scaffold | gehlenite, akermanite | 0.000535 | 8 | 2.570278 | 127.8775 |
| Ca3Si2O7 polymorph scaffold | rankinite, kilchoanite | -0.027933 | 6.75 | 2.438188 | 126.853 |

Candidate gates:

| Gate | Candidate rule | Observed gap | Status | Current-row result |
|---|---|---|---|---|
| coordination-only Ca scaffold gate | melilite-like if mean Ca coordination is 8 | 7 to 8 | diagnostic candidate only | yes on current rows |
| mean Ca-O scaffold-distance gate | melilite-like if mean Ca-O is at least 2.53 A | 2.467712 to 2.565838 A | diagnostic candidate only | yes on current rows |
| bridge-angle mean gate | no stable one-dimensional rule from current rows | rankinite high-angle and kilchoanite low-angle both have nearly identical negative residuals | reject as first scalar gate | not applicable |
| Ca/O scalar gate | reject as transferable scaffold gate | Ca3Si2O7 has higher Ca/O but lower measured response than the melilite-derived Ca uplift predicts | reject as transferable gate | not applicable |

Row-level checks:

| Material | Ca coord gate | Ca-O distance gate | Split-Ca residual |
|---|---|---|---:|
| gehlenite | melilite-like | melilite-like | 0.00163 |
| akermanite | melilite-like | melilite-like | -0.00056 |
| rankinite | non-melilite-like | non-melilite-like | -0.028113 |
| kilchoanite | non-melilite-like | non-melilite-like | -0.027753 |

Reading: the candidate gate is now concrete enough to falsify. Melilite-like Ca scaffold means Ca coordination 8 and long mean Ca-O distance near 2.57 A under the fixed extraction method. The Ca3Si2O7 rows are more compact and lower-coordinate, so the melilite-derived Ca uplift should not transfer.

Boundary: do not turn either numeric boundary into a model coefficient yet. The next target should be chosen before scoring, and should have both optical constants and an ambient-pressure CIF.

This updated the runner to 22 RI scripts at that point in the chain.

## Held-Out Larnite Reservation

`analysis/ri-heldout-larnite-reservation-diagnostic.mjs` reserves larnite as the next held-out Ca-silicate target before CIF geometry extraction and before RI scoring. It does not score a prediction and does not fit a coefficient.

Reserved target:

| Field | Value |
|---|---|
| Material | larnite |
| Formula | Ca2SiO4 |
| Role | held-out Ca-only non-melilite silicate target |
| Topology class | Ca orthosilicate / beta-dicalcium silicate |
| Reservation status | reserved before CIF geometry extraction and before RI scoring |
| Reason | keeps Ca-Si-O chemistry but changes polymerization and Ca scaffold away from melilite and Ca3Si2O7 |

Optical source:

| Field | Value |
|---|---:|
| Source | Handbook of Mineralogy, Larnite, Mineral Data Publishing version 1.2 |
| URL | https://handbookofmineralogy.org/pdfs/larnite.pdf |
| Measured density range | 3.28-3.33 |
| Density for future scoring | 3.305 |
| alpha range | 1.700-1.715 |
| beta range | 1.715-1.723 |
| gamma range | 1.725-1.740 |
| Scalar RI range | 1.713333-1.726 |
| Scalar RI midpoint | 1.719666 |

CIF source:

| Field | Value |
|---|---|
| COD ID | 9017424 |
| CIF URL | https://www.crystallography.net/cod/9017424.cif |
| COD card | https://www.crystallography.net/cod/9017424.html |
| Reference | Yamnova et al. 2011, beta-Ca2SiO4 larnite structure |
| Source material | synthetic |
| Space group | P 1 21/n 1 |
| Cell | a=5.5051, b=6.7551, c=9.3108, beta=94.513 |
| Calculated density | 3.314 |
| Coordinates / disorder | coordinates yes; disorder no |

Rejected alternatives:

- wollastonite remains useful later, but the prior screen flagged broad Handbook density and optical ranges;
- gugiaite / alumoakermanite remain useful same-scaffold melilite stress tests, but need source-qualified RI and CIF pairing first;
- another Ca3Si2O7 polymorph is useful if source-qualified, but rankinite and kilchoanite already establish the first Ca3Si2O7 pair.

Locked pre-score expectations:

- do not fit a new coefficient before scoring larnite;
- keep the existing split-Ca family and candidate gate definitions frozen;
- extract larnite CIF geometry before optical scoring, then classify the gate without changing thresholds;
- if larnite is lower-coordinate or compact by the fixed extractor, the candidate gate predicts non-transfer of melilite Ca uplift.

This updated the runner to 23 RI scripts at that point in the chain.

## Held-Out Larnite Gate Classification

`analysis/ri-cif-geometry-extraction-diagnostic.mjs` now includes the reserved larnite COD row, and `analysis/ri-larnite-gate-classification-diagnostic.mjs` performs the required pre-score classification. This does not score larnite RI and does not fit a coefficient.

Larnite CIF source:

| Field | Value |
|---|---|
| COD ID | 9017424 |
| CIF URL | https://www.crystallography.net/cod/9017424.cif |
| Reference | Yamnova et al. 2011, beta-Ca2SiO4 larnite structure |

Extracted descriptors under the fixed CIF geometry extractor:

| Descriptor | Value |
|---|---:|
| Bridge angle | n/a; isolated SiO4 orthosilicate has no T-O-T bridge under the current T-neighbor rule |
| Ca coordination range | 7-8 |
| Mean Ca coordination | 7.5 |
| Mean Ca-O range | 2.498765-2.513969 A |
| Mean Ca-O | 2.506367 A |

Frozen gate result:

| Gate | Frozen rule | Larnite value | Melilite-like? | Pre-score prediction |
|---|---|---:|---|---|
| coordination-only Ca scaffold gate | melilite-like if mean Ca coordination is 8 | 7.5 | no | non-transfer of melilite Ca uplift |
| mean Ca-O scaffold-distance gate | melilite-like if mean Ca-O is at least 2.53 A | 2.506367 | no | non-transfer of melilite Ca uplift |
| bridge-angle mean gate | rejected as first scalar gate before larnite reservation | n/a | n/a | not used |

Pre-score status:

- larnite is now classified before optical scoring as a compact/lower-coordinate non-melilite Ca scaffold;
- the held-out order is preserved: gate classification happened before RI scoring;
- the next allowed move was optical scoring under the frozen split-Ca family and frozen gate classification;
- expected diagnostic outcome: non-transfer of the melilite Ca uplift.

This updated the runner to 24 RI scripts at that point in the chain.

## Larnite Ca-Scaffold Transfer Validation

`analysis/external-ri-larnite-ca-scaffold-transfer-validation.mjs` then scored larnite after the gate classification was frozen. No coefficients, thresholds, density handling, or source interpretation were changed.

Target:

| Field | Value |
|---|---:|
| Formula | Ca2SiO4 |
| Density used | 3.305 |
| Ca/O | 0.5 |
| Oxygen volume | 13.02852 |
| Scalar RI range | 1.713333-1.726 |
| Scalar RI midpoint | 1.719666 |

Frozen candidate results:

| Candidate family | Predicted RI | Error | Pass | Reading |
|---|---:|---:|---|---|
| baseline density + Al/O + Al-comp response | 1.71769 | 0.00198 | yes | density-dominant baseline happens to fit larnite |
| split Ca scaffold family | 1.75034 | 0.03067 | no | melilite-derived Ca uplift overpredicts |
| split Ca/Mg scaffold family | 1.76092 | 0.04125 | no | Mg split does not apply and still overpredicts |

Status:

```text
larnite strengthens topology-gated Ca-scaffold interpretation: Ca-scaffold family failed transfer
```

Important reading:

- the result is not a general material-RI pass, because the baseline family is an older reference family and the broader material-property gate remains unresolved;
- the result does strengthen the specific topology-gate diagnosis: the post-failure melilite Ca scaffold uplift should not be reused as a scalar Ca/O term outside melilite;
- larnite joins rankinite and kilchoanite as a non-melilite Ca-silicate overprediction for the split-Ca repair;
- the next useful step is not another scalar Ca coefficient. It is either a structural gate model with the baseline/density family kept as a control, or a new held-out target selected to test whether density-only success on larnite is accidental.

This updated the runner to 25 RI scripts at that point in the chain.

## Larnite Density-Control Contrast

`analysis/ri-larnite-density-control-contrast-diagnostic.mjs` compares the larnite control-row pass against the split-Ca failure across the non-melilite Ca-silicate rows. It does not fit a coefficient and does not promote either family.

Key rows:

| Material | Formula | Density | Ca/O | Measured RI | Baseline prediction | Baseline residual | Split-Ca prediction | Split-Ca residual |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| rankinite | Ca3Si2O7 | 2.98 | 0.428571 | 1.645667 | 1.63042 | 0.01525 | 1.67378 | -0.02811 |
| kilchoanite | Ca3Si2O7 | 2.992 | 0.428571 | 1.648167 | 1.63354 | 0.01463 | 1.67592 | -0.02775 |
| larnite | Ca2SiO4 | 3.305 | 0.5 | 1.719666 | 1.71769 | 0.00198 | 1.75034 | -0.03067 |

Interpretation:

- the larnite baseline pass is a control-row success, not a repair validation;
- the baseline family still misses rankinite and kilchoanite, so it is not a general RI solution;
- the split-Ca term is consistently too large outside melilite;
- larnite proves that "non-transfer" does not mean low RI, because larnite has high RI and still rejects the melilite-derived Ca uplift;
- the next variable is suppression or gating of Ca scaffold response, with density/polarizability kept as the conventional comparator.

Next useful tests:

1. reserve another high-density Ca-silicate with optical constants and CIF geometry to test whether the baseline density-family larnite pass repeats;
2. state a gate-suppressed Ca scaffold diagnostic as a model-form hypothesis, but do not fit it from rankinite, kilchoanite, and larnite;
3. audit whether the baseline family is mostly a crude Lorentz-Lorenz density proxy rather than substrate-specific evidence.

This updated the runner to 26 RI scripts at that point in the chain.

## Density-Control Falsifier Reservation

`analysis/ri-density-control-falsifier-reservation-diagnostic.mjs` reserves the next density-control target after the larnite contrast. It does not score a prediction and does not fit or promote a model.

Candidate screen:

| Material | Formula | Composition class | Density for future scoring | Scalar RI range | CIF status | Decision |
|---|---|---|---:|---:|---|---|
| merwinite | Ca3Mg(SiO4)2 | Ca-Mg-Si-O; not pure Ca-Si-O | 3.235 | 1.71-1.717333 | COD 9000285; coordinates yes | reserve |
| spurrite | Ca5(SiO4)2(CO3) | Ca-Si-C-O; adds carbonate | 3.02 | 1.661667-1.666 | pending source-qualified CIF | defer |
| wollastonite | CaSiO3 | Ca-Si-O | 2.975 | 1.625-1.647667 | not selected; polytype issue | defer |
| hatrurite | Ca3SiO5 | Ca-Si-O | n/a | n/a | optical/density source unusable | reject for current gate |

Reserved target:

| Field | Value |
|---|---|
| Material | merwinite |
| Formula | Ca3Mg(SiO4)2 |
| Role | high-density Mg-bearing Ca-silicate density-control falsifier |
| Optical source | Handbook of Mineralogy, Merwinite PDF |
| Optical row | D(meas.) 3.15-3.32; D(calc.) 3.33; alpha 1.702-1.710; beta 1.710-1.714; gamma 1.718-1.728 |
| CIF source | COD 9000285 |
| CIF reference | Moore and Araki 1972, merwinite atomic arrangement |
| CIF status | coordinates yes; disorder no |

Locked pre-score expectations:

- do not score merwinite in the reservation artifact;
- when scored later, use the frozen baseline, split-Ca, and split-Ca/Mg families;
- keep Mg chemistry visible as a limitation;
- if the density-family pass repeats while split-Ca/Mg fails or overpredicts, density/polarizability pressure increases;
- if density fails too, larnite was probably a local control-row accident.

This updated the runner to 27 RI scripts at that point in the chain.

## Merwinite Density-Control Validation

`analysis/external-ri-merwinite-density-control-validation.mjs` scores merwinite after reservation under the frozen baseline, split-Ca, and split-Ca/Mg families. Coefficients, thresholds, density handling, and source interpretation are unchanged. Merwinite is Mg-bearing, so this is not pure Ca-Si-O continuation.

Target:

| Field | Value |
|---|---:|
| Formula | Ca3Mg(SiO4)2 |
| Density used | 3.235 |
| Ca/O | 0.375 |
| Mg/O | 0.125 |
| Oxygen volume | 12.70097 |
| Scalar RI range | 1.71-1.717333 |
| Scalar RI midpoint | 1.713666 |

Frozen candidate results:

| Candidate family | Predicted RI | Error | Pass | Reading |
|---|---:|---:|---|---|
| baseline density + Al/O + Al-comp response | 1.69837 | 0.0153 | no | larnite baseline success does not repeat |
| split Ca scaffold family | 1.70737 | 0.0063 | yes | passes this Mg-bearing row, but not promotable |
| split Ca/Mg scaffold family | 1.70952 | 0.00415 | yes | passes, but Mg/O was introduced after akermanite |

Status:

```text
merwinite breaks density-control pass; larnite baseline success remains local
```

Important reading:

- merwinite falsifies the simple idea that the larnite baseline pass automatically repeats in another high-density Ca-silicate-family row;
- the split-Ca and split-Ca/Mg passes cannot be promoted because merwinite contains Mg and the Mg/O term is post-akermanite calibration debt;
- the next target should reduce the Mg confound, preferably a source-qualified dense Ca-rich silicate/carbonate such as spurrite only after a CIF row is selected, or a polytype-controlled wollastonite row if source uncertainty can be reduced.

This updates the runner to 28 RI scripts.

## Post-Merwinite Target Reservation

`analysis/ri-post-merwinite-target-reservation-diagnostic.mjs` reserves the next target after merwinite. It does not score a prediction and does not fit or promote a model. The reservation removes merwinite's Mg confound but introduces carbonate, so it is a confound-substitution control contrast rather than a clean Ca-Si-O validation row.

Candidate screen:

| Material | Formula | Composition class | Density for future scoring | Scalar RI range | CIF status | Decision |
|---|---|---|---:|---:|---|---|
| spurrite | Ca5(SiO4)2(CO3) | Ca-Si-C-O; adds carbonate but removes Mg | 3.02 | 1.661667-1.666 | COD 9004961; coordinates yes | reserve |
| wollastonite | CaSiO3 | Ca-Si-O | 2.975 | 1.625-1.647667 | not selected; polytype issue | defer |
| hatrurite | Ca3SiO5 | Ca-Si-O | n/a | n/a | optical/density source unusable | reject for current gate |

Reserved target:

| Field | Value |
|---|---|
| Material | spurrite |
| Formula | Ca5(SiO4)2(CO3) |
| Role | Ca-rich silicate-carbonate post-merwinite confound-substitution target |
| Optical source | Handbook of Mineralogy, Spurrite PDF |
| Optical row | D(meas.) 3.02; D(calc.) 3.025; alpha 1.637-1.641; beta 1.672-1.676; gamma 1.676-1.681 |
| CIF source | COD 9004961 |
| CIF reference | Grice 2005, The structure of spurrite, tilleyite and scawtite, and relationships to other silicate-carbonate minerals |
| CIF status | coordinates yes; disorder no |

Locked pre-score expectations:

- do not score spurrite in the reservation artifact;
- when scored later, use the frozen baseline, split-Ca, and split-Ca/Mg families;
- treat carbonate chemistry as a limitation, not as pure Ca-Si-O continuation;
- if split-Ca passes spurrite while Mg/O is zero, the merwinite split-Ca pass is less likely to be only an Mg artifact;
- if split-Ca fails spurrite, the merwinite split-Ca pass remains Mg/topology-confounded.

Important reading:

- spurrite is not a programme-level RI validation row because it substitutes a carbonate confound for the merwinite Mg confound;
- a polytype-locked wollastonite row would be higher-value if a source-specific optical/CIF alignment can be found;
- any spurrite score must be read as a control contrast under the frozen families, not as support for promoting split-Ca or split-Ca/Mg.

This updates the runner to 29 RI scripts.

## Wollastonite Polytype Source-Lock Screen

`analysis/ri-wollastonite-polytype-source-lock-screen.mjs` checks whether wollastonite can become the next clean Ca-Si-O target after spurrite reservation. It does not score a prediction, does not compute a gate classification, and does not fit or promote a model.

Decision:

```text
defer wollastonite; fall back to spurrite scoring only as a Mg-removed/carbonate-introduced control contrast unless a polytype-specific optical row is found
```

Broad optical source:

| Field | Value |
|---|---|
| Source | Handbook of Mineralogy, Wollastonite PDF |
| Optical/density row | D(meas.) 2.86-3.09; D(calc.) 2.90; alpha 1.616-1.640; beta 1.628-1.650; gamma 1.631-1.653 |
| Scalar RI range | 1.625-1.647667 |
| Scalar RI midpoint | 1.636334 |
| Polytype-specific | no |

CIF candidates:

| COD ID | Mineral name | Polytype/read | Density calc. | Space group | Coordinates | Reference |
|---|---|---|---:|---|---|---|
| 9005777 | Wollastonite | WO1T / triclinic wollastonite-like row | 2.916 | P -1 | yes | Ohashi 1984, Polysynthetically-twinned structures of enstatite and wollastonite |
| 9008151 | Wollastonite-2M | parawollastonite / Wollastonite-2M | 2.914 | P 1 21/a 1 | yes | Trojer 1968, The crystal structure of parawollastonite |
| 9011913 | Wollastonite-2M | Wollastonite-2M | 2.933 | P 1 21/a 1 | yes | Mamedov and Belov 1956, The crystal structure of wollastonite |

Lock status:

- locked: paired CIF candidates exist for specific wollastonite polytype rows;
- not locked: optical constants and measured density for the same selected polytype;
- not locked: optical-sample composition hygiene;
- not run: CIF-derived Ca coordination and mean Ca-O pre-score classification, because no single source-locked polytype was selected.

Important reading:

- wollastonite remains the higher-value chemistry target because it is pure Ca-Si-O;
- the broad Handbook scalar RI range must not be used as a held-out target;
- do not average WO1T/triclinic and Wollastonite-2M/parawollastonite rows;
- without a polytype-specific optical/density source, the next scoreable target remains spurrite, read only as Mg-removed/carbonate-introduced control contrast.

This updates the runner to 30 RI scripts.

## Spurrite Confound-Substitution Validation

`analysis/external-ri-spurrite-confound-substitution-validation.mjs` scores reserved spurrite under the frozen baseline, split-Ca, and split-Ca/Mg families after the wollastonite source-lock screen. No coefficient, threshold, density handling, or carbonate descriptor is added.

Target:

| Field | Value |
|---|---:|
| Formula | Ca5(SiO4)2(CO3) |
| Density used | 3.02 |
| Ca/O | 0.45455 |
| Mg/O | 0 |
| C/O | 0.09091 |
| Oxygen volume | 13.3823 |
| Scalar RI range | 1.661667-1.666 |
| Scalar RI midpoint | 1.663833 |

Frozen candidate results:

| Candidate family | Predicted RI | Error | Pass | Reading |
|---|---:|---:|---|---|
| baseline density + Al/O + Al-comp response | 1.64084 | 0.02299 | no | density baseline misses this carbonate row |
| split Ca scaffold family | 1.68693 | 0.0231 | no | Ca scaffold family still fails after Mg removal |
| split Ca/Mg scaffold family | 1.69584 | 0.03201 | no | Mg/O is zero and family still misses |

Status:

```text
spurrite split-Ca fails under carbonate limitation; merwinite pass remains Mg/topology-confounded
```

Important reading:

- spurrite removes the merwinite Mg confound but introduces carbonate, so this remains control-contrast evidence only;
- all frozen families fail spurrite under 0.01 tolerance;
- the split-Ca failure means the merwinite split-Ca pass remains Mg/topology-confounded;
- carbonate prevents using the spurrite failure as a clean Ca-Si-O falsifier;
- the clean Ca-Si-O path remains blocked until a polytype-specific wollastonite optical/density row, or another pure Ca-Si-O row, is source-locked.

This updates the runner to 31 RI scripts.

## Pure Ca-Si-O Source Exhaustion Screen

`analysis/ri-pure-ca-si-o-source-exhaustion-screen.mjs` records the post-spurrite source state for a clean pure Ca-Si-O held-out target. It does not score a prediction, fit a model, or relax the source rules after the carbonate-confounded spurrite failure.

Gate requirements:

- pure Ca-Si-O composition with no Mg, carbonate, hydroxyl, alkali, Fe/Mn substitution, or cement-phase ambiguity;
- source-anchored optical constants with one material/polytype identity;
- source-anchored measured density for the same material/polytype identity;
- paired CIF with coordinates for the same material/polytype identity;
- pre-score CIF gate classification before optical prediction;
- no broad pooled optical ranges or secondary aggregate rows as held-out targets.

Candidate screen:

| Material | Formula | Decision | Blocking field |
|---|---|---|---|
| wollastonite | CaSiO3 | defer | Handbook optical/density row is broad and not polytype-specific, despite useful COD polytype CIFs |
| wollastonite-1A / 2M / 3A-4A-5A-7A secondary rows | CaSiO3 | reject for scoring | secondary aggregate optical/density rows are repeated across polytype pages and not primary-source matched |
| hatrurite | Ca3SiO5 | reject for current gate | Handbook/RRUFF row reports n = n.d.; D(meas.) = n.d.; D(calc.) = n.d. |
| pseudowollastonite | CaSiO3 | defer | no source-grade alpha/beta/gamma plus measured-density row found in this screen |
| larnite | Ca2SiO4 | exhausted | already classified before scoring and then scored |
| rankinite and kilchoanite | Ca3Si2O7 | exhausted | already used in topology-transfer sequence |

Decision:

```text
do not score another target until a polytype-specific wollastonite/pseudowollastonite optical-density row or another pure Ca-Si-O source-locked row is found
```

Important reading:

- the clean Ca-Si-O branch is source-blocked, not model-ready;
- do not infer that no pure Ca-Si-O target exists in the literature;
- infer only that no new target is reserved under the current source-lock rules in this screen;
- the next productive artifact should either unlock a primary polytype-specific optical/density source or move to a model-form diagnostic that treats the Ca-scaffold family as failed outside its source domain.

This updates the runner to 32 RI scripts.

## Ca-Scaffold Model-Form Quarantine

`analysis/ri-ca-scaffold-model-form-quarantine-diagnostic.mjs` records the model-form boundary after the post-merwinite branch and pure Ca-Si-O source-exhaustion screen. It does not score a target, fit a coefficient, or promote a new RI repair.

Evidence ledger:

| Material | Formula | Status | Reading |
|---|---|---|---|
| hardystonite | Ca2ZnSi2O7 | failed split-Ca transfer | same-topology success is not automatic once T1 cation chemistry changes |
| rankinite | Ca3Si2O7 | failed split-Ca transfer | scalar Ca/O uplift overpredicts outside melilite |
| kilchoanite | Ca3Si2O7 | failed split-Ca transfer | rankinite miss is not an isolated polymorph anomaly |
| larnite | Ca2SiO4 | failed split-Ca transfer; baseline passed locally | baseline pass is local control-row success, not model validation |
| merwinite | Ca3Mg(SiO4)2 | baseline failed; split-Ca and split-Ca/Mg passed | pass is not promotable because Mg chemistry is confounded |
| spurrite | Ca5(SiO4)2(CO3) | all frozen families failed | carbonate prevents clean Ca-Si-O falsification, but merwinite pass remains confounded |
| wollastonite/pseudowollastonite/hatrurite | CaSiO3 / Ca3SiO5 | not scored | source lock is exhausted under current gate; do not use broad/secondary rows |

Family status:

| Family | Status | Boundary |
|---|---|---|
| baseline density + Al/O + Al-comp response | reference diagnostic only | later misses prevent validation use |
| split Ca scaffold family | quarantined outside its source domain | failed hardystonite, rankinite, kilchoanite, larnite, and spurrite; merwinite pass is Mg-confounded |
| split Ca/Mg scaffold family | quarantined outside its source domain | inherits split-Ca failures and adds Mg/O calibration debt |

Reopen conditions:

- predeclare a new model form before scoring another target;
- source-lock a clean held-out target with optical constants, measured density, and paired CIF before prediction;
- classify the target under frozen CIF/structural gates before optical scoring;
- do not reuse rankinite, kilchoanite, larnite, merwinite, or spurrite as fresh validation;
- do not treat Mg-bearing or carbonate-bearing rows as pure Ca-Si-O validation;
- keep density/Lorentz-Lorenz comparators labelled as conventional control evidence.

Decision:

```text
do not score further material-RI targets under baseline, split-Ca, or split-Ca/Mg as candidate repairs; use them only as reference diagnostics until a new source-locked model form is predeclared
```

Important reading:

- the active Ca-scaffold repair programme is model-form blocked, not merely target-blocked;
- split-Ca and split-Ca/Mg remain useful forensic diagnostics, but not active candidate repairs;
- the next legitimate RI step is either a predeclared structural model form or a primary-source unlock for a clean held-out target followed by pre-score gate classification.

This updates the runner to 33 RI scripts.
