# Human book readability: research basis for the `human-book-readability` skill (v1)

Prepared 2026-10-03 as the evidence base for `.claude/skills/human-book-readability/`. It records what the skill assumes, why, and with what confidence, so the skill can be revised rather than inherited as an unexplained prompt. Citations were checked against publisher or index records at the time of writing. Where a finding is contested, that is noted.

## 1. The core problem

Readability formulas measure surface features: word length, syllables, sentence length and familiar-word lists. Those features correlate with difficulty in general-audience text, but they do not measure whether a reader can *build the intended mental model*. A philosophical sentence made of short words can be incomprehensible. A long, carefully signposted sentence can be easy.

For serious non-fiction, the binding constraints are conceptual:

- how many unfamiliar ideas must be held together;
- whether each has been prepared;
- whether the text supplies the inferences that connect them;
- whether the reader's prior knowledge can carry the rest.

**Consequence for the skill:** surface metrics are *low-level indicators only* and are never reported as a comprehension score.

Benjamin (2012), *Reconstructing Readability*, *Educational Psychology Review* 24, 63–88, reviews the limits of classic formulas and argues for multi-level text analysis. Crossley et al. (2023), working with the CLEAR corpus of 4,724 excerpts with human ease judgements, found that NLP-derived indices of lexical sophistication, cohesion and syntactic complexity substantially outperform classic formulas. Even those indices explained only about half the variance. Text-only measurement has a ceiling.

## 2. Working memory and cognitive load

- **Capacity.** Working memory holds only a few novel chunks at once: about four, per Cowan (2001), "The magical number 4 in short-term memory", *Behavioral and Brain Sciences* 24(1), 87–114. This revises Miller's (1956) "seven plus or minus two". The figure is for *chunks*, and what counts as a chunk depends on prior knowledge.
- **Cognitive load theory (CLT).** Sweller (1988, *Cognitive Science* 12) and later work hold that learning fails when processing demands exceed working-memory capacity. Sweller (2010), "Element interactivity and intrinsic, extraneous, and germane cognitive load", *Educational Psychology Review* 22, 123–138, makes **element interactivity** the defining mechanism: intrinsic load comes from how many elements must be processed *simultaneously because they interact*. Ten independent facts are easier than four mutually dependent ones.
- **Extraneous load** is imposed by presentation rather than content. Examples are split attention, redundancy, and undefined terms used before their definition.
- **Expertise reversal.** Kalyuga, Ayres, Chandler and Sweller (2003), "The expertise reversal effect", *Educational Psychologist* 38(1), 23–31, found that support which helps novices (worked examples, integrated explanation) can hinder experts. Scaffolding should fade as the reader's schema grows.
- **Caveat.** CLT's load *measures* are contested. Self-report ratings are weak, and the theory has faced replication and construct critiques (see the 2023 *Educational Psychology Review* discussion of replication and theory expansion). The skill therefore uses CLT as a *design heuristic* for estimating relative load, not as a measurement instrument.

**Skill implication:** estimate *interacting* novel concepts per passage, not just counts. Treat more than four simultaneously interacting unfamiliar concepts, without a prior chunk to hold them, as high risk.

## 3. Comprehension models

- **Construction–integration.** Kintsch (1988), *Psychological Review* 95, holds that readers build a propositional *textbase* and integrate it with prior knowledge into a *situation model*. Comprehension is the quality of the situation model, not recall of wording.
- **Repairing inference calls.** Britton and Gülgöz (1991), "Using Kintsch's computational model to improve instructional text", *Journal of Educational Psychology* 83, 329–345, revised a text to make explicit every inference the reader would otherwise have to supply. This improved recall and made learners' knowledge structures closer to the author's. Unstated inferential steps are a primary, *repairable* cause of difficulty.
- **Reverse cohesion effect.** McNamara, Kintsch, Songer and Kintsch (1996), "Are good texts always better?", *Cognition and Instruction* 14(1), 1–43, found that low-knowledge readers benefit from highly coherent text. High-knowledge readers sometimes learn more deeply from less explicit text, because they must generate the links themselves. Cohesion should be calibrated to the intended reader, not maximised blindly.
- **Situation-model dimensions.** Zwaan and Radvansky (1998, *Psychological Bulletin* 123) list time, space, causation, intentionality and protagonist/entity continuity. In expository and philosophical prose, causal and logical continuity matter most.

**Skill implication:** the most valuable revision usually inserts a missing inferential step or a missing "because". Shortening sentences is usually less valuable. The cohesion target depends on the declared reader.

## 4. Cohesion and coherence

- **Cohesion versus coherence.** Halliday and Hasan (1976), *Cohesion in English*, define cohesion as the linguistic ties in a text (reference, substitution, conjunction, lexical repetition). Coherence is the reader's resulting sense of connected meaning. Cohesion supports coherence but does not guarantee it.
- **Coh-Metrix.** Graesser, McNamara, Louwerse and Cai (2004), "Coh-Metrix: Analysis of text on cohesion and language", *Behavior Research Methods* 36(2), 193–202, operationalise referential cohesion (argument and noun overlap between adjacent sentences), deep or causal cohesion (connectives), situation-model indices, syntactic simplicity and word concreteness.
- **Entity continuity.** The entity-grid model of Barzilay and Lapata (2008), "Modeling local coherence: an entity-based approach", *Computational Linguistics* 34(1), 1–34, tracks how discourse entities persist across sentences and in which grammatical roles. Coherent text shows characteristic patterns in which the same entity remains salient across adjacent sentences. Centering theory (Grosz, Joshi and Weinstein 1995, *Computational Linguistics* 21(2)) explains why abrupt shifts of the central entity raise processing cost and why ambiguous pronouns fail.

**Skill implication:**

- Measure adjacent-paragraph content-word overlap as a crude referential-cohesion proxy.
- Flag paragraphs that share no key term with their predecessor and open with no connective.
- Flag pronouns ("this", "it", "that") opening a paragraph after a long gap.

## 5. Sentence-level processing

- **Dependency locality.** Gibson (1998, *Cognition* 68; 2000) found that difficulty rises with the distance between dependent words and the number of new discourse referents introduced in between. Very long sentences are costly mainly when they hold long unresolved dependencies or nest clauses, not because of length as such.
- **Nominalisation and passive density** raise abstraction and hide agents. This is common in theological and philosophical prose ("the actualisation of the admissibility of...").

**Skill implication:**

- Flag sentences over 40 words, and sentences with several nested qualifiers.
- Flag strings of three or more abstract nominalisations.
- Do not mechanically split sentences that carry one clear causal chain.

## 6. Schema, scaffolding, examples and analogy

- **Advance organisers.** Ausubel (1960, *Journal of Educational Psychology* 51) found that a short, higher-level framing before unfamiliar material aids integration, especially for novices.
- **Concept maps.** Novak and Gowin (1984); Nesbit and Adesope (2006) meta-analysis, *Review of Educational Research* 76. Explicit relational structure supports learning, so diagrams of concept relations earn their place for complex dependency structures.
- **Worked examples and concrete instances** reduce load for novices (CLT). They should come *close to* the abstraction they instantiate. A distant example forces the abstraction to be held unsupported.
- **Analogy.** Gentner (1983, *Cognitive Science* 7) treats analogy as structure mapping. Learners carry over relational structure and also surface features unless told otherwise. Analogies need explicit limits (what maps, what does not); otherwise they become hidden mechanisms.

## 7. Spacing, reactivation and repetition

- **Spacing and retrieval.** Cepeda et al. (2006, *Psychological Bulletin* 132) found that re-encountering material after a delay strengthens retention more than massed repetition. In a book, a *short* reactivation of a key concept after long absence is useful. Re-explaining it at full length immediately is redundancy.
- **Redundancy effect** (CLT). Presenting the same information twice in different forms to a reader who already has it *increases* load.

**Skill implication:**

- Track *reactivation distance*: words since a concept's last substantive use.
- Recommend a one-clause reminder when a load-bearing concept returns after a long gap (heuristically, more than about 8,000 words, or a chapter boundary with intervening unrelated material).
- Flag near-duplicate explanations closer than that.

## 8. Expert–novice differences and the curse of knowledge

- **Curse of knowledge.** Camerer, Loewenstein and Weber (1989, *Journal of Political Economy* 97) found that informed agents cannot easily simulate an uninformed perspective. Authors systematically underestimate inferential distance. Hinds (1999, *Journal of Experimental Psychology: Applied* 5) found that experts underestimate novice task difficulty.
- **Inferential distance** is the number of unstated steps between what the text says and what the reader must already believe in order to follow it. It is the most important single construct for technical-philosophical books, and the hardest to see from the author's chair.

**Skill implication:** adversarial "naive reader" passes must be run from explicitly declared reader profiles. Each pass reports the specific points at which the profile could not follow.

## 9. Plain language

ISO 24495-1:2023, *Plain language — Part 1: Governing principles and guidelines*, frames plain language around four principles: readers can *find* what they need, *understand* it, *use* it, and the text is *relevant*. For books, "find" translates into signposting and navigation, and "use" into the reader being able to apply the concept later. Plain language does not forbid technical terms. It requires that terms earn their place and are defined before use.

## 10. Narrative momentum and voice

For long-form non-fiction, engagement depends on a sense of question and progression: each section answers something the reader now wants answered and raises the next question. Excessive chapter previews and summaries, repeated thesis statements and meta-commentary consume attention without adding schema. This is the redundancy effect again, at chapter scale. Machine-generated prose shows identifiable habits:

- reflexive triplets;
- "not X but Y" constructions;
- em-dash saturation;
- inflated adjectives ("profound", "crucial");
- micro-sections;
- bullet dependence.

These degrade the sense of an authored argument. *(This last point is practitioner consensus and editorial observation rather than a controlled finding; the skill treats it as style guidance.)*

## 11. Philosophical and theological prose

Specific risks:

- **Equivocation:** a term changes sense across chapters.
- **Category slippage:** an analogy treated as identity.
- **Modal drift:** "may" becoming "is" without new evidence.
- **Authority layering:** Scripture, inference and speculation stated in the same register.

The text-comprehension literature does not measure these directly. The skill handles them through a *terminology register* (one sense per term, tracked) and an *epistemic register* (claim strength must match support). Both are readability issues in the strict sense: a reader cannot build a correct situation model from equivocal terms.

## 12. Design decisions derived from the research

1. Report a **vector**, never a scalar comprehension score.
2. The **Human Context Load (HCL)** vector for a passage is:
   - novel concepts;
   - active prerequisites;
   - interaction density (CLT element interactivity);
   - abstraction;
   - dependency depth;
   - recall distance (spacing);
   - terminology burden;
   - implicit inferential steps (Britton and Gülgöz);
   - scaffolding support (examples, analogies with limits, diagrams);
   - familiarity (prior knowledge, McNamara et al. 1996).
   These combine into a risk *category* by explicit rules, not by a weighted sum.
3. Automated script output is **evidence for a human or model judgement**, not the judgement itself.
4. Calibrate to a **declared reader profile**, because cohesion and scaffolding effects reverse with expertise.
5. Separate the **concept graph** (which ideas depend on which) from the **text** (where they appear). Check that the text's order is a topological ordering of the graph, and measure the distance between a prerequisite's introduction and its use.
6. Preserve flow. Decomposing a concept into acquisition steps is good; fragmenting prose into micro-sections is not. Score digestibility and continuity together.

## 13. Known limitations of v1

- The automated cohesion proxy is lexical overlap, not semantic similarity or coreference resolution.
- Concept detection depends on a supplied term list.
- No reader testing has been done. The skill's recommendations are research-informed heuristics, not validated predictions of comprehension for any particular book.
- Future versions could add embedding-based cohesion, coreference resolution, and calibration against reader comprehension data.

## References (verified)

- Ausubel, D. P. (1960). The use of advance organizers in the learning and retention of meaningful verbal material. *Journal of Educational Psychology*, 51, 267–272.
- Barzilay, R., & Lapata, M. (2008). Modeling local coherence: An entity-based approach. *Computational Linguistics*, 34(1), 1–34. https://aclanthology.org/J08-1001/
- Benjamin, R. G. (2012). Reconstructing readability. *Educational Psychology Review*, 24, 63–88. https://link.springer.com/article/10.1007/s10648-011-9181-8
- Britton, B. K., & Gülgöz, S. (1991). Using Kintsch's computational model to improve instructional text. *Journal of Educational Psychology*, 83, 329–345. https://eric.ed.gov/?id=EJ436892
- Camerer, C., Loewenstein, G., & Weber, M. (1989). The curse of knowledge in economic settings. *Journal of Political Economy*, 97(5), 1232–1254.
- Cepeda, N. J., et al. (2006). Distributed practice in verbal recall tasks. *Psychological Bulletin*, 132(3), 354–380.
- Cowan, N. (2001). The magical number 4 in short-term memory. *Behavioral and Brain Sciences*, 24(1), 87–114.
- Crossley, S., et al. (2023). A large-scaled corpus for assessing text readability (CLEAR). *Behavior Research Methods*. https://www.researchgate.net/publication/359277397
- Gentner, D. (1983). Structure-mapping: A theoretical framework for analogy. *Cognitive Science*, 7(2), 155–170.
- Gibson, E. (1998). Linguistic complexity: Locality of syntactic dependencies. *Cognition*, 68(1), 1–76.
- Graesser, A. C., McNamara, D. S., Louwerse, M. M., & Cai, Z. (2004). Coh-Metrix. *Behavior Research Methods*, 36(2), 193–202. https://link.springer.com/article/10.3758/BF03195564
- Grosz, B. J., Joshi, A. K., & Weinstein, S. (1995). Centering. *Computational Linguistics*, 21(2), 203–225.
- Halliday, M. A. K., & Hasan, R. (1976). *Cohesion in English*. Longman.
- Hinds, P. J. (1999). The curse of expertise. *Journal of Experimental Psychology: Applied*, 5(2), 205–221.
- ISO 24495-1:2023. *Plain language — Part 1: Governing principles and guidelines*. https://www.sis.se/en/produkter/standardization/information-sciences-publishing/writing-and-transliteration/iso-24495-12023/
- Kalyuga, S., Ayres, P., Chandler, P., & Sweller, J. (2003). The expertise reversal effect. *Educational Psychologist*, 38(1), 23–31.
- Kintsch, W. (1988). The role of knowledge in discourse comprehension: A construction-integration model. *Psychological Review*, 95(2), 163–182.
- McNamara, D. S., Kintsch, E., Songer, N. B., & Kintsch, W. (1996). Are good texts always better? *Cognition and Instruction*, 14(1), 1–43.
- Miller, G. A. (1956). The magical number seven, plus or minus two. *Psychological Review*, 63(2), 81–97.
- Nesbit, J. C., & Adesope, O. O. (2006). Learning with concept and knowledge maps: A meta-analysis. *Review of Educational Research*, 76(3), 413–448.
- Sweller, J. (1988). Cognitive load during problem solving. *Cognitive Science*, 12(2), 257–285.
- Sweller, J. (2010). Element interactivity and intrinsic, extraneous, and germane cognitive load. *Educational Psychology Review*, 22, 123–138. https://link.springer.com/article/10.1007/s10648-010-9128-5
- Zwaan, R. A., & Radvansky, G. A. (1998). Situation models in language comprehension and memory. *Psychological Bulletin*, 123(2), 162–185.
