#!/usr/bin/env python3
"""Concept graph for Coherent Biblical Ontology, second edition.

Single source of truth for the concepts the reader must acquire and how they
depend on one another. Generates:

  books/v2/analysis/concept-graph.json   machine-readable nodes, edges, metrics
  books/v2/analysis/concept-graph.md     human-readable inventory and analysis
  books/v2/analysis/concept-graph.mmd    Mermaid source (REQUIRES backbone)
  books/v2/analysis/terms-edition2.json  term list for the readability script

Edge types (A -[TYPE]-> B):
  REQUIRES                A cannot be understood before B (prerequisite)
  SUPPORTS                A gives reason to accept B
  EXPLAINS                A accounts for B
  CONSTRAINS              A limits admissible readings of B
  DISTINGUISHES           A is defined partly by contrast with B
  ANALOGOUS_TO            A and B share relational form
  NOT_IDENTICAL_TO        a guardrail: A must not be collapsed into B
  GENERALISES/SPECIALISES taxonomy
  EVIDENCED_BY            A is supported by evidence node B
  SCRIPTURALLY_BOUNDED_BY A is bounded by Scripture node B
  USED_BY                 B uses A at a later point in the book

Run: python3 books/v2/tools/build_concept_graph.py
"""

from __future__ import annotations

import json
from collections import defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis"

# id: (term, definition, epistemic category, maturity, difficulty 1-5,
#      abstraction 1-5, decomposable, load-bearing, misunderstanding, example)
N = {
 # ---- method and epistemology
 "scripture": ("Scripture as governing frame", "Scripture is received as truthful revelation and bounds what the ontology may claim; interpretation remains corrigible.", "scriptural commitment", "settled", 2, 2, False, True, "that Scripture supplies technical physics", "Genesis 1 read as ontology, not a journal article"),
 "creator-creature": ("Creator/creature distinction", "God is uncreated and self-existent; everything else is created, dependent and not divine.", "theological claim", "settled", 2, 3, False, True, "that the substrate is part of God", "Psalm 100:3; Romans 1:25"),
 "creation-real": ("Creation is real from the beginning", "Genesis 1:1 is real instantiation; what follows is formation within created reality.", "scriptural commitment", "settled", 1, 2, False, False, "that darkness means non-being", "earth, waters and darkness present before light"),
 "darkness": ("Darkness as created condition", "Genesis 1 darkness is a real, unmanifested condition of creation, not nothing and not evil.", "theological inference", "settled", 2, 3, False, False, "moral darkness read back into Genesis 1", "a silent string under tension"),
 "description": ("Description", "Observation, measurement, mathematical representation and prediction of how things behave.", "philosophical claim", "settled", 1, 2, False, False, "that description is trivial", "an equation predicting an orbit"),
 "ontology": ("Ontology", "The account of what must be there for described behaviour to be possible.", "philosophical claim", "settled", 2, 4, False, True, "ontology as mere speculation", "asking what a field is, not only how it behaves"),
 "desc-not-ont": ("Description is not ontology", "Predictive and mathematical success does not by itself settle what kind of reality is described.", "philosophical claim", "settled", 3, 4, True, True, "that this dismisses science", "two interpretations of one quantum formalism"),
 "assumptions": ("Metaphysical assumptions are always present", "Every ontology, scientific or theological, starts from assumptions that should be made visible.", "philosophical claim", "settled", 2, 3, False, True, "that naming assumptions is relativism", "methodological naturalism as a choice"),
 "epistemic-levels": ("Levels of claim", "Observation, mathematical description, inference, model, interpretation, theology, Scripture and RS hypothesis are different kinds of claim.", "methodological", "settled", 2, 3, True, True, "that labelling claims weakens them", "a measured half-life versus its interpretation"),
 "coherence": ("Coherence", "Claims fitting together: non-contradiction is necessary, but coherence also requires real connection, faithful translation across boundaries and preserved distinctions.", "philosophical claim", "settled", 2, 3, False, True, "coherence as mere consistency", "a story whose parts do not contradict"),
 "local-coherence": ("Local coherence", "A model explains a bounded phenomenon internally.", "philosophical claim", "settled", 2, 3, False, False, "local success as truth", "an equation fitting one regime"),
 "regional-coherence": ("Regional coherence", "Several adjacent domains integrate (chemistry with physics).", "philosophical claim", "settled", 2, 3, False, False, "", "molecular biology joining chemistry"),
 "global-coherence": ("Global coherence", "The whole account of reality — physics, life, persons, morality, history, Scripture — is connected, translates faithfully across its boundaries, keeps its meaning through layers and cycles, and preserves its distinctions.", "methodological thesis", "working", 4, 5, True, True, "that it overrides evidence", "a worldview that explains physics but makes responsibility unintelligible fails globally"),
 "knowing-coherence": ("Human knowing is coherence-based", "Ordinary knowledge assembles the most coherent account from incomplete evidence under uncertainty.", "philosophical claim (supported by cognitive science)", "settled", 3, 3, False, True, "that the brain runs an RS algorithm", "a doctor's diagnosis; a jury's verdict"),
 "coherence-not-fidelity": ("Coherence is not fidelity", "A coherent account can still be false; agreement can harden an early error (false attractor).", "philosophical claim", "settled", 3, 4, False, True, "that coherence guarantees truth", "a confident consensus built on one mistaken premise"),
 "empirical-constraint": ("Observation constrains ontology", "Robust observation and logic rule out incompatible ontologies even when they cannot display the right one.", "methodological", "settled", 2, 3, False, True, "that coherence ignores evidence", "a model contradicting measured light speed is ruled out"),
 "connectivity": ("Connectivity", "Domains genuinely connected by intelligible transitions, not merely placed side by side.", "methodological (author-supplied)", "working", 3, 4, False, False, "connection as mere juxtaposition", "physics to chemistry to life"),
 "boundary-validity": ("Boundary validity", "A concept crossing a domain boundary keeps what is relevant without collapsing categories.", "methodological (author-supplied)", "working", 4, 4, False, True, "translation as relabelling", "physical consequence to moral responsibility"),
 "propagation-cycle": ("Propagation stability and cycle consistency", "A claim keeps its meaning through explanatory layers, and returns materially the same when translated round a cycle of domains.", "methodological (author-supplied)", "working", 4, 5, False, True, "that plausible paragraphs add up to coherence", "identity: physical → organism → person → body"),
 "not-proof": ("Not an empirical proof", "The deep ontology behind observation is not directly measurable; RS is a coherence exercise constrained by observation, not a proof.", "methodological", "settled", 3, 4, False, True, "that unprovable means unconstrained", "no instrument displays 'relation as such'"),
 "analogy-vs-identity": ("Structural analogy is not ontological identity", "Shared relational form across domains does not make the domains the same kind of thing.", "philosophical claim", "settled", 3, 4, False, True, "that a shared grammar means a shared substance", "a letter and a nerve impulse both transmit; neither is the other"),
 "category": ("Ontological categories", "Material, biological, personal, spiritual and divine realities are genuinely distinct kinds.", "philosophical/theological claim", "settled", 3, 4, True, True, "that relation erases category", "a body and a person"),
 # ---- physical ontology
 "relation": ("Relation", "A real standing-between of things in which each conditions the other; interactional relation holds between complete things, constitutive relation partly makes things what they are — RS proposes the latter at the base.", "ontological interpretation", "working", 3, 4, True, True, "relation as a mental association", "a knot exists only as the crossing of strands"),
 "object-first": ("Object-first picture", "The assumption that reality is basically isolated objects in empty space with relations added afterwards.", "philosophical claim", "settled", 2, 3, False, False, "that rejecting it denies objects", "billiard balls in a void"),
 "substrate": ("Relational substrate", "The proposed created relational order within which physical things are constituted and act; not matter, not a field, not God.", "RS working hypothesis", "working", 4, 5, True, True, "a hidden jelly or ether; a second world; a deity", "the order of a language within which words have their sense"),
 "runtime": ("Created runtime order", "Creation as operating, distinguished from its origin; the domain of ordinary physical process.", "ontological interpretation", "working", 3, 4, False, True, "that creation is software", "the difference between composing and performing"),
 "mediation": ("Mediated influence", "Nothing affects anything across a gap of non-relation; influence passes through relational continuity.", "RS working hypothesis", "working", 3, 4, False, False, "that this denies fields or long-range effects", "a wave across a pond"),
 "possibility": ("Constrained possibility (T0)", "What creation is capable of: the space of admissible configurations and transitions.", "RS working hypothesis", "working", 4, 5, True, True, "that possibility is a hidden stuff", "the legal moves of chess, not a game"),
 "admissibility": ("Admissibility", "Whether a transition is possible at all — a hard boundary of the possible.", "RS experimental result (formal) + interpretation", "working", 3, 4, False, True, "admissible as morally permitted", "a door that exists versus one that does not"),
 "tendency": ("Tendency", "How likely an admissible transition is relative to others; a weighting, not a permission.", "RS experimental result (formal)", "working", 3, 4, False, True, "tendency as necessity", "a well-worn path"),
 "actualisation": ("Actualisation (T1)", "The coming-to-be of one admissible configuration among the possible.", "RS working hypothesis", "working", 4, 5, False, True, "actualisation as creation from nothing", "one game actually played"),
 "stochasticity": ("Stochasticity", "Description by probabilities over defined possibilities; neutral between epistemic probability and ontic indeterminacy; not lawlessness.", "mathematical / scientific consensus", "settled", 3, 4, True, True, "stochastic = random = chaotic", "dice: each roll open, the distribution fixed"),
 "constrained-stochasticity": ("Constrained stochastic actualisation", "RS hypothesis that actualisation is ontically stochastic: genuinely open among admissible options until it occurs, shaped by constraint.", "RS working hypothesis", "frontier", 4, 5, True, True, "that RS proves indeterminism", "radioactive decay: open timing, exact half-life"),
 "identity-invariant": ("Invariant", "What a class of admissible changes leaves unchanged; one carrier or certificate of identity, not necessarily all of it.", "mathematical + RS model result", "settled", 3, 4, False, True, "identity = a conserved number", "a number reached by 4,000 different paths; a knot's type"),
 "equivalence": ("Identity as relational equivalence", "Identity continuity is preservation of the relevant relational equivalence class across admissible change, relative to what reachable future consequences can discriminate.", "ontological interpretation (author-supplied research) + RS model support", "working", 4, 5, True, True, "that 'same' is purely observer-relative", "two coins that look alike but one is counterfeit"),
 "recovery-kinds": ("Kinds of recovery", "Functional, structural, equivalence-class and lineage-specific recovery are distinct; reconstruction is not automatically restoration of identity.", "ontological distinction (author-supplied research, negative results)", "working", 3, 4, False, True, "that working again means the same again", "a rebuilt organisation without its lineage"),
 "individual-continuity": ("Individual continuity", "Being the same continuing individual, not merely an equivalent replacement; requires lineage and history beyond equivalence; open in RS research.", "ontological distinction", "open", 4, 4, False, True, "that equivalence settles individuality", "two coins from the same die"),
 "provenance": ("Provenance", "Past distinctions that survive in present relational structure; part of identity where consequential, safely ignored only where no reachable future can consume them.", "ontological interpretation (author-supplied research)", "working", 4, 4, False, True, "provenance as a separate record or memory substance", "a bent paper clip; a forged signature's history"),
 "discriminability": ("Future discriminability", "Whether any admissible future interaction could tell two states apart; the criterion for 'same' in the relevant domain.", "ontological interpretation (author-supplied research)", "working", 4, 5, False, True, "that it means what a human happens to measure", "two keys alike until one is tried in the lock"),
 "projection": ("Projection and coarse-graining", "A description that maps several distinct underlying states to one visible state; it can hide distinctions that later matter.", "mathematical + RS model result (constraint lab G1b)", "working", 3, 4, False, True, "that equal descriptions mean equal things", "one family label hiding 1,042 distinct kernels"),
 "persistence": ("Persistence", "Continued re-actualisation within the same relevant equivalence class.", "ontological interpretation", "working", 3, 4, False, True, "persistence as inertness", "a flame maintaining itself"),
 "information-loss": ("Preservation is not reconstruction", "Admissible change preserves an equivalence class, but destroyed distinctions are not recovered by conservation; recovery needs surviving information.", "RS experimental result (model)", "working", 3, 3, False, False, "that identity is indestructible", "an erased relation never repaired (0/1,800)"),
 "memory-configuration": ("Memory as persisting configuration", "Past distinctions embodied in present relations so that they alter future admissibility, tendency, correlation or response; no separate memory substance required.", "RS working hypothesis", "frontier", 3, 4, False, False, "memory as stored pictures", "metal fatigue depending on loading order"),
 "difference": ("Source distinction", "A distinguishable state or relation at a source that could make a difference to something else.", "ontological interpretation", "working", 2, 3, False, True, "difference as subjective contrast", "a dark mark on white paper"),
 "transmit": ("Transmit (relational availability)", "A source distinction becomes able to have consequence beyond its locality; depletion of the source is one subcase, not the definition.", "RS interpretive grammar", "working", 3, 4, False, True, "that the source must lose what it transmits", "a lighthouse; an atom emitting light; a spoken name"),
 "carry": ("Carry (recoverable constrained continuity)", "The relevant distinction stays recoverably constrained across one or more, possibly changing, carrier realisations.", "RS interpretive grammar (implemented in model)", "working", 4, 5, True, True, "the carrier as a travelling thing", "a relay message; a certificate replaced at each step"),
 "substitutability": ("Carrier substitutability", "The vehicle may change while the carried correlation is preserved.", "RS experimental result (model) + interpretation", "working", 3, 4, False, False, "nothing persists", "a wave moving through water whose molecules stay"),
 "receive": ("Receive (consequential reception)", "A compatible receiver is changed in a way that depends on the carried distinction; arrival is not reception, and once-only is a property of some receivers.", "RS interpretive grammar", "working", 3, 4, False, True, "reception as mere arrival; reception as necessarily once-only", "a letter read and acted on"),
 "endogenous-carrier": ("Endogenous carriers (open)", "Whether created order generates carrier and lineage architecture from minimal relations; not demonstrated — models used designed protocols.", "open question", "open", 4, 5, False, False, "that RS has shown carriers emerge by themselves", "the calculator's designed certificate"),
 "compatibility": ("Receiver compatibility", "What a receiver can register and how it responds (once, repeatedly, cumulatively, idempotently) is set by its own admissibility.", "ontological interpretation + RS model example", "working", 3, 4, False, False, "that every receiver must count arrivals once", "the eye and radio waves; a thermostat; a ledger"),
 "tcr": ("Transmit–Carry–Receive", "The grammar by which a source distinction becomes consequential beyond its locality: relational availability, recoverable constrained carriage, compatible consequential reception.", "RS interpretive grammar", "working", 4, 5, True, True, "that soul or revelation is a physical signal", "seeing a stone in daylight"),
 "nested-tcr": ("Nested and composed T-C-R", "Transmissions compose in sequence and in parallel, and nest across scales.", "RS working hypothesis", "frontier", 4, 5, True, False, "that everything is one signal", "nerve impulse within perception within conversation"),
 "joint-process": ("Marginals versus joint process", "Equal chances for each event do not fix how events are related; the joint process, covariance and global dynamics can differ.", "mathematical + author-supplied research", "settled", 3, 4, False, True, "same odds, same behaviour", "two crowds of coin-tossers, one independent, one in pairs"),
 "aggregation": ("Aggregation", "Many independent or weakly dependent chance events average into a stable mean (laws of large numbers).", "scientific consensus / mathematical", "settled", 2, 3, False, True, "that averaging needs coordination", "steady tyre pressure"),
 "layered-stability": ("Layered stability", "A whole may be stable in mean, concentrated, exactly conserved or still stochastic in different respects; mean closure is not fluctuation closure, which is not full relational closure.", "mathematical + author-supplied research", "working", 4, 4, False, True, "that 'stable' means one thing", "same average, different fluctuations"),
 "coordination": ("Coordination of fluctuations", "Consequence-aligned, state-dependent relations between stochastic events that stabilise aggregates; mean closure can hold while fluctuation closure stays open.", "RS experimental result (model)", "working", 4, 5, True, False, "coordination as a hidden controller", "two errors that cancel because they are tied"),
 "local-global": ("Local and global constraint", "What a local rule permits differs from what whole-system orchestration achieves; both must be stated.", "RS experimental result (model)", "working", 3, 4, False, False, "local rules always suffice", "local cancellation exact but slower"),
 "regularity": ("Emergent regularity / effective determinism", "Stable, law-like aggregate behaviour arising from constrained stochastic processes.", "scientific consensus + RS interpretation", "working", 3, 4, True, True, "that regularity proves determinism", "gas laws from molecular chaos"),
 "mathematics": ("Mathematics describes regularity", "Mathematics captures stable relations and invariants with great success without thereby being the reality.", "philosophical claim", "settled", 3, 4, False, True, "that this demotes mathematics", "Navier–Stokes as an effective description of fluids"),
 "time": ("Time as ordering of actualisation", "Time is the ordering of change, not an independent container.", "ontological interpretation", "working", 4, 5, False, False, "that this denies relativity", "clocks as processes"),
 "matter": ("Matter as stable form", "Matter is real, stable relational form, not primitive substance.", "ontological interpretation", "working", 3, 4, False, True, "that matter is unreal", "a whirlpool or a knot"),
 "manifestation": ("Manifestation", "Created order presenting itself to other things — detectable, encounterable; distinct from conscious awareness of it.", "ontological interpretation", "working", 3, 3, False, False, "manifestation as an explanation of consciousness", "the stone visible in daylight"),
 "purpose-upstream": ("Purpose shapes possibility", "Divine purpose constrains what is possible; possibility constrains actualisation; the substrate itself intends nothing.", "theological inference", "working", 4, 5, False, True, "that the substrate is a mind", "a composer's intention fixing the instrument's range"),
 "non-agentic": ("Non-agentic runtime", "Created runtime order is ordered without being intelligent, purposive or divine in itself.", "theological/ontological claim", "settled", 3, 4, False, True, "that lawful runtime means God is absent", "seedtime and harvest"),
 "constraint-generative": ("Constraint is generative", "Boundaries make stable form possible rather than merely limiting.", "ontological interpretation + scriptural theme", "settled", 2, 3, False, False, "constraint as oppression", "riverbanks making a river"),
 # ---- bridge and theology
 "bridge": ("No metaphysical gulf", "Because material order is relational at base, relational realities of life and persons are not bolted onto an alien, disconnected world.", "philosophical inference", "working", 5, 5, True, True, "that morality is physics", "a world of sealed objects cannot ground promise-keeping"),
 "life": ("Life as sustained organisation", "Living things maintain, repair and reproduce organised form under hierarchical constraint; life is given and sustained by God.", "theological inference + scientific consensus", "working", 3, 3, False, True, "life as a vital fluid; life as nothing but chemistry", "a cell repairing itself"),
 "higher-order": ("Higher-order wholes", "A whole becomes real when its parts are coupled so that disturbance spreads and the whole retains properties no part has.", "ontological interpretation", "working", 3, 4, False, False, "every heap is a whole", "an organism versus a crowd"),
 "consciousness": ("Consciousness", "Real awareness, embodied and participating in shared reality, not reducible to physical configuration.", "philosophical/theological claim", "open", 4, 5, False, True, "that RS explains consciousness", "seeing as an act, not only a signal"),
 "personhood": ("Personhood", "A centre of awareness, relation, agency, address and responsibility; deeper than embodiment.", "theological claim", "settled", 4, 4, False, True, "person = body", "Father and Spirit are persons without bodies"),
 "soul-spirit": ("Soul and spirit", "Scripture's vocabulary for the inner person, given by God and not reducible to runtime configuration.", "scriptural commitment", "settled", 4, 4, False, True, "soul as a physical signal or field", "Ecclesiastes 12:7"),
 "embodiment": ("Embodiment", "The mode by which creaturely persons exist and act in created order; good and meaningful.", "theological claim", "settled", 3, 3, False, True, "body as prison", "Genesis 2:7"),
 "image": ("Image of God", "Humanity's relational, representative, image-bearing calling before God.", "scriptural commitment", "settled", 3, 4, False, True, "image as a material feature", "Genesis 1:27"),
 "three-admissibility": ("Three kinds of 'allowed'", "Physical possibility, operational capability and moral rightness are different questions.", "philosophical claim", "settled", 3, 4, True, True, "if it is possible it is permitted", "lying is possible, within ability, and wrong"),
 "alignment": ("Alignment", "Fitting the order a thing or person is made for; in persons, a moral and relational reality, not only structural.", "theological inference", "working", 4, 4, False, True, "alignment as a physics measure of goodness", "an instrument in tune"),
 "corruption": ("Corruption as distortion", "Real, parasitic disorder of what is good: wrongdoing (wrong in itself) and its entrenchment as misalignment persists and spreads — not a rival substance.", "theological inference", "working", 4, 4, True, True, "evil as a thing; or evil as unreal", "a lie: transmission that misdirects"),
 "limitation": ("Limitation is not corruption", "Finitude is good creaturehood; corruption is distortion.", "theological claim", "settled", 2, 3, False, False, "that being finite is sin", "needing sleep"),
 "restoration": ("Restoration and redemption", "God's work in Christ restoring and consummating creation and persons; not substrate repair.", "scriptural commitment + theological inference", "settled", 4, 4, False, True, "redemption as mechanism", "resurrection of the same person"),
 "resurrection": ("Resurrection", "Embodied identity raised and transformed, continuous with the person who died.", "scriptural commitment", "settled", 4, 4, False, True, "a new copy", "Luke 24:39"),
 "divine-action": ("Divine action is not substrate process", "God acts as Creator and Lord, not as one more cause inside created admissibility.", "theological claim", "settled", 4, 5, False, True, "miracles as hidden physics", "the resurrection of Christ"),
}

# Evidence and Scripture nodes (sources, not reader concepts)
E = {
 "E-sc": "Stochastic calculator SC-001–SC-027R (2026-09)",
 "E-cl": "Constraint Laboratory Generation 001 (2026-10-03)",
 "E-topo": "Topological instantiation anchors (2026-07)",
 "E-order": "Order-effect corroboration on fatigue data (2026-06)",
 "E-statmech": "Statistical mechanics and kinetic theory (mainstream)",
 "E-qm": "Quantum theory: Born-rule probabilities; interpretations divided (mainstream)",
 "E-decay": "Radioactive decay statistics (mainstream)",
 "E-relphys": "Relational positions in philosophy of physics (Leibniz, Rovelli, structural realism)",
 "E-cogsci": "Cognitive science of inference under uncertainty (predictive processing, Bayesian cognition)",
 "E-multipath": "False-attractor observations behind Multipath Reasoning (method origin; unvalidated)",
 "E-hysteresis": "Physical hysteresis and path dependence (mainstream)",
 "E-noether": "Conservation laws and symmetry (mainstream)",
 "E-cl1b": "Constraint Laboratory Generation 1b (2026-10-03): exact kernels hidden within coarse families",
 "E-cl2": "Constraint Laboratory Generation 2 (2026-10-03): count-gated prohibitions open supports; soft weights do not",
 "E-cl3": "Constraint Laboratory Generation 3 (2026-10-03): hidden triadic relation yields non-Markov pairwise process",
 "E-conv": "Author-supplied conversational research (502-series, ring, hidden fibres, coherence dimensions); not repository experiments",
}
S = {
 "S-gen1": "Genesis 1:1–5", "S-gen27": "Genesis 2:7", "S-col1": "Colossians 1:16–17",
 "S-heb113": "Hebrews 11:3", "S-rom120": "Romans 1:20,25", "S-ps100": "Psalm 100:3",
 "S-john1": "John 1:1–4", "S-acts17": "Acts 17:25–28", "S-rom8": "Romans 8:19–22",
 "S-1cor15": "1 Corinthians 15", "S-eccl127": "Ecclesiastes 12:7", "S-john424": "John 4:24",
 "S-gen822": "Genesis 8:22; Jeremiah 31:35–36", "S-james1": "James 1:14–15", "S-rev21": "Revelation 21:1–5",
 "S-heb13": "Hebrews 1:3", "S-prov252": "Proverbs 25:2", "S-1thes523": "1 Thessalonians 5:23",
 "S-isa55": "Isaiah 55:10–11", "S-rom10": "Romans 10:14–17",
}

R = "REQUIRES"
EDGES = [
 # method spine
 ("creator-creature", R, "scripture"), ("creation-real", R, "scripture"), ("darkness", R, "creation-real"),
 ("ontology", R, "description"), ("desc-not-ont", R, "ontology"), ("desc-not-ont", R, "description"),
 ("assumptions", R, "ontology"), ("epistemic-levels", R, "desc-not-ont"), ("epistemic-levels", R, "assumptions"),
 ("local-coherence", R, "coherence"), ("regional-coherence", R, "local-coherence"),
 ("global-coherence", R, "regional-coherence"), ("connectivity", R, "coherence"),
 ("boundary-validity", R, "connectivity"), ("boundary-validity", R, "category"), ("propagation-cycle", R, "boundary-validity"),
 ("global-coherence", R, "propagation-cycle"), ("global-coherence", R, "desc-not-ont"),
 ("global-coherence", R, "empirical-constraint"), ("knowing-coherence", R, "coherence"),
 ("coherence-not-fidelity", R, "knowing-coherence"), ("empirical-constraint", R, "description"),
 ("not-proof", R, "desc-not-ont"), ("not-proof", R, "global-coherence"), ("not-proof", R, "empirical-constraint"),
 ("analogy-vs-identity", R, "category"), ("category", R, "creator-creature"),
 # physical spine
 ("object-first", R, "assumptions"), ("relation", R, "object-first"),
 ("substrate", R, "relation"), ("substrate", R, "creator-creature"), ("runtime", R, "substrate"),
 ("runtime", R, "creation-real"), ("mediation", R, "relation"),
 ("possibility", R, "substrate"), ("admissibility", R, "possibility"), ("tendency", R, "admissibility"),
 ("actualisation", R, "possibility"), ("stochasticity", R, "tendency"),
 ("constrained-stochasticity", R, "stochasticity"), ("constrained-stochasticity", R, "admissibility"),
 ("constrained-stochasticity", R, "actualisation"),
 ("identity-invariant", R, "constrained-stochasticity"), ("projection", R, "identity-invariant"),
 ("discriminability", R, "admissibility"), ("equivalence", R, "identity-invariant"), ("equivalence", R, "discriminability"),
 ("equivalence", R, "projection"), ("provenance", R, "equivalence"), ("persistence", R, "equivalence"),
 ("information-loss", R, "identity-invariant"), ("memory-configuration", R, "provenance"),
 ("memory-configuration", R, "admissibility"),
 ("difference", R, "relation"), ("transmit", R, "difference"), ("carry", R, "transmit"),
 ("carry", R, "persistence"), ("carry", R, "equivalence"), ("substitutability", R, "carry"),
 ("compatibility", R, "admissibility"), ("receive", R, "carry"), ("receive", R, "compatibility"), ("tcr", R, "transmit"), ("tcr", R, "carry"), ("tcr", R, "receive"),
 ("nested-tcr", R, "tcr"), ("joint-process", R, "stochasticity"), ("aggregation", R, "stochasticity"),
 ("layered-stability", R, "aggregation"), ("layered-stability", R, "coordination"), ("regularity", R, "aggregation"),
 ("recovery-kinds", R, "equivalence"), ("individual-continuity", R, "provenance"), ("individual-continuity", R, "equivalence"),
 ("resurrection", R, "individual-continuity"), ("recovery-kinds", R, "individual-continuity"), ("individual-continuity", "NOT_IDENTICAL_TO", "equivalence"), ("recovery-kinds", R, "provenance"), ("endogenous-carrier", R, "carry"), ("coordination", R, "joint-process"),
 ("coordination", R, "constrained-stochasticity"), ("coordination", R, "relation"),
 ("local-global", R, "coordination"), ("regularity", R, "constrained-stochasticity"),
 ("regularity", R, "identity-invariant"), ("regularity", R, "coordination"),
 ("mathematics", R, "regularity"), ("mathematics", R, "desc-not-ont"),
 ("time", R, "actualisation"), ("matter", R, "persistence"), ("manifestation", R, "matter"),
 ("purpose-upstream", R, "possibility"), ("purpose-upstream", R, "creator-creature"),
 ("non-agentic", R, "runtime"), ("non-agentic", R, "purpose-upstream"),
 ("constraint-generative", R, "admissibility"),
 # bridge and theology
 ("bridge", R, "relation"), ("bridge", R, "global-coherence"), ("bridge", R, "tcr"),
 ("bridge", R, "analogy-vs-identity"), ("life", R, "persistence"), ("life", R, "tcr"),
 ("higher-order", R, "coordination"), ("higher-order", R, "life"),
 ("consciousness", R, "manifestation"), ("consciousness", R, "category"),
 ("embodiment", R, "matter"), ("personhood", R, "embodiment"), ("personhood", R, "category"),
 ("soul-spirit", R, "personhood"), ("image", R, "personhood"),
 ("three-admissibility", R, "admissibility"), ("three-admissibility", R, "personhood"),
 ("alignment", R, "three-admissibility"), ("corruption", R, "alignment"), ("corruption", R, "tcr"),
 ("limitation", R, "corruption"), ("restoration", R, "corruption"), ("resurrection", R, "restoration"),
 ("resurrection", R, "equivalence"), ("divine-action", R, "non-agentic"),
 ("restoration", R, "divine-action"),
 # v2.1 relation types
 ("projection", "CAN_HIDE", "provenance"), ("discriminability", "CAN_REVEAL", "provenance"),
 ("provenance", "CONSEQUENTIAL_FOR", "receive"), ("identity-invariant", "PRESERVES", "equivalence"),
 ("carry", "CARRIES", "difference"), ("equivalence", "QUALIFIES", "identity-invariant"),
 ("compatibility", "QUALIFIES", "receive"), ("joint-process", "QUALIFIES", "regularity"),
 ("equivalence", "SUPERSEDES", "information-loss"),
 ("tcr", "NOT_ESTABLISHED_BY", "E-sc"), ("constrained-stochasticity", "NOT_ESTABLISHED_BY", "E-qm"),
 ("relation", "NOT_ESTABLISHED_BY", "E-cl"),
 ("coordination", "QUALIFIES", "aggregation"), ("recovery-kinds", "DISTINGUISHES", "information-loss"),
 ("recovery-kinds", "CONSTRAINS", "resurrection"), ("endogenous-carrier", "NOT_ESTABLISHED_BY", "E-sc"),
 ("projection", "EVIDENCED_BY", "E-cl3"), ("memory-configuration", "EVIDENCED_BY", "E-cl3"),
 ("recovery-kinds", "EVIDENCED_BY", "E-conv"), ("aggregation", "EVIDENCED_BY", "E-statmech"),
 # supports / explains / constrains
 ("relation", "SUPPORTS", "global-coherence"), ("bridge", "SUPPORTS", "global-coherence"),
 ("knowing-coherence", "SUPPORTS", "global-coherence"), ("regularity", "EXPLAINS", "mathematics"),
 ("identity-invariant", "EXPLAINS", "persistence"), ("tcr", "EXPLAINS", "mediation"),
 ("admissibility", "CONSTRAINS", "actualisation"), ("purpose-upstream", "CONSTRAINS", "possibility"),
 ("scripture", "CONSTRAINS", "substrate"), ("empirical-constraint", "CONSTRAINS", "substrate"),
 ("coherence-not-fidelity", "CONSTRAINS", "global-coherence"), ("matter", "EXPLAINS", "manifestation"),
 ("constraint-generative", "SUPPORTS", "identity-invariant"), ("memory-configuration", "EXPLAINS", "persistence"),
 # distinctions and guardrails
 ("stochasticity", "DISTINGUISHES", "constrained-stochasticity"), ("admissibility", "DISTINGUISHES", "tendency"),
 ("regularity", "DISTINGUISHES", "mathematics"), ("receive", "DISTINGUISHES", "transmit"),
 ("limitation", "DISTINGUISHES", "corruption"), ("three-admissibility", "DISTINGUISHES", "admissibility"),
 ("local-coherence", "DISTINGUISHES", "global-coherence"),
 ("substrate", "NOT_IDENTICAL_TO", "creator-creature"), ("substrate", "NOT_IDENTICAL_TO", "soul-spirit"),
 ("tcr", "NOT_IDENTICAL_TO", "soul-spirit"), ("personhood", "NOT_IDENTICAL_TO", "embodiment"),
 ("alignment", "NOT_IDENTICAL_TO", "admissibility"), ("corruption", "NOT_IDENTICAL_TO", "limitation"),
 ("restoration", "NOT_IDENTICAL_TO", "persistence"), ("regularity", "NOT_IDENTICAL_TO", "mathematics"),
 ("coherence", "NOT_IDENTICAL_TO", "coherence-not-fidelity"), ("consciousness", "NOT_IDENTICAL_TO", "matter"),
 ("divine-action", "NOT_IDENTICAL_TO", "actualisation"), ("purpose-upstream", "NOT_IDENTICAL_TO", "non-agentic"),
 # cross-domain analogy (form, not identity)
 ("tcr", "ANALOGOUS_TO", "corruption"), ("tcr", "ANALOGOUS_TO", "life"),
 ("identity-invariant", "ANALOGOUS_TO", "resurrection"), ("persistence", "ANALOGOUS_TO", "personhood"),
 ("coordination", "ANALOGOUS_TO", "higher-order"), ("knowing-coherence", "ANALOGOUS_TO", "constrained-stochasticity"),
 # taxonomy
 ("global-coherence", "GENERALISES", "regional-coherence"), ("nested-tcr", "GENERALISES", "tcr"),
 ("constrained-stochasticity", "SPECIALISES", "stochasticity"), ("three-admissibility", "GENERALISES", "admissibility"),
 # evidence
 ("identity-invariant", "EVIDENCED_BY", "E-sc"), ("identity-invariant", "EVIDENCED_BY", "E-topo"),
 ("identity-invariant", "EVIDENCED_BY", "E-noether"), ("tcr", "EVIDENCED_BY", "E-sc"), ("projection", "EVIDENCED_BY", "E-cl1b"),
 ("equivalence", "EVIDENCED_BY", "E-conv"), ("provenance", "EVIDENCED_BY", "E-conv"), ("joint-process", "EVIDENCED_BY", "E-conv"),
 ("coordination", "EVIDENCED_BY", "E-conv"), ("propagation-cycle", "EVIDENCED_BY", "E-conv"), ("admissibility", "EVIDENCED_BY", "E-cl2"),
 ("admissibility", "EVIDENCED_BY", "E-cl"), ("tendency", "EVIDENCED_BY", "E-cl"),
 ("coordination", "EVIDENCED_BY", "E-sc"), ("local-global", "EVIDENCED_BY", "E-sc"),
 ("information-loss", "EVIDENCED_BY", "E-sc"), ("regularity", "EVIDENCED_BY", "E-statmech"),
 ("regularity", "EVIDENCED_BY", "E-decay"), ("regularity", "EVIDENCED_BY", "E-sc"),
 ("constrained-stochasticity", "EVIDENCED_BY", "E-qm"), ("memory-configuration", "EVIDENCED_BY", "E-order"),
 ("memory-configuration", "EVIDENCED_BY", "E-hysteresis"), ("relation", "EVIDENCED_BY", "E-relphys"),
 ("knowing-coherence", "EVIDENCED_BY", "E-cogsci"), ("coherence-not-fidelity", "EVIDENCED_BY", "E-multipath"),
 # scripture
 ("creation-real", "SCRIPTURALLY_BOUNDED_BY", "S-gen1"), ("darkness", "SCRIPTURALLY_BOUNDED_BY", "S-gen1"),
 ("creator-creature", "SCRIPTURALLY_BOUNDED_BY", "S-ps100"), ("creator-creature", "SCRIPTURALLY_BOUNDED_BY", "S-rom120"),
 ("substrate", "SCRIPTURALLY_BOUNDED_BY", "S-col1"), ("substrate", "SCRIPTURALLY_BOUNDED_BY", "S-heb113"),
 ("runtime", "SCRIPTURALLY_BOUNDED_BY", "S-heb13"), ("non-agentic", "SCRIPTURALLY_BOUNDED_BY", "S-gen822"),
 ("regularity", "SCRIPTURALLY_BOUNDED_BY", "S-gen822"), ("desc-not-ont", "SCRIPTURALLY_BOUNDED_BY", "S-prov252"),
 ("purpose-upstream", "SCRIPTURALLY_BOUNDED_BY", "S-john1"), ("life", "SCRIPTURALLY_BOUNDED_BY", "S-acts17"),
 ("embodiment", "SCRIPTURALLY_BOUNDED_BY", "S-gen27"), ("personhood", "SCRIPTURALLY_BOUNDED_BY", "S-john424"),
 ("soul-spirit", "SCRIPTURALLY_BOUNDED_BY", "S-eccl127"), ("soul-spirit", "SCRIPTURALLY_BOUNDED_BY", "S-1thes523"),
 ("corruption", "SCRIPTURALLY_BOUNDED_BY", "S-james1"), ("corruption", "SCRIPTURALLY_BOUNDED_BY", "S-rom8"),
 ("restoration", "SCRIPTURALLY_BOUNDED_BY", "S-rev21"), ("resurrection", "SCRIPTURALLY_BOUNDED_BY", "S-1cor15"),
 ("tcr", "SCRIPTURALLY_BOUNDED_BY", "S-isa55"), ("tcr", "SCRIPTURALLY_BOUNDED_BY", "S-rom10"),
 ("divine-action", "SCRIPTURALLY_BOUNDED_BY", "S-col1"),
]

# Chapter of first introduction under the selected architecture (see architecture-candidates.md).
INTRO = {}  # filled from analysis/chapter-map.json if present


def load_intro():
    p = OUT / "chapter-map.json"
    if p.exists():
        return json.loads(p.read_text())["first_introduction"]
    return {}


def metrics():
    req = defaultdict(set)      # node -> prerequisites
    dep = defaultdict(set)      # node -> direct dependents
    und = defaultdict(set)
    for a, t, b in EDGES:
        if a in N and b in N:
            und[a].add(b); und[b].add(a)
            if t == R:
                req[a].add(b); dep[b].add(a)
    # prerequisite depth (longest chain), memoised
    depth = {}
    def d(n, stack=()):
        if n in depth:
            return depth[n]
        if n in stack:
            raise SystemExit(f"cycle in REQUIRES at {n}: {stack}")
        depth[n] = 1 + max((d(p, stack + (n,)) for p in req[n]), default=0)
        return depth[n]
    for n in N:
        d(n)
    # transitive dependents
    trans = {}
    for n in N:
        seen, q = set(), deque(dep[n])
        while q:
            x = q.popleft()
            if x not in seen:
                seen.add(x); q.extend(dep[x])
        trans[n] = len(seen)
    # Brandes betweenness on the undirected all-type graph (concept nodes only)
    bc = dict.fromkeys(N, 0.0)
    for s in N:
        stack, pred, sigma, dist = [], defaultdict(list), dict.fromkeys(N, 0), dict.fromkeys(N, -1)
        sigma[s], dist[s] = 1, 0
        q = deque([s])
        while q:
            v = q.popleft(); stack.append(v)
            for w in und[v]:
                if dist[w] < 0:
                    dist[w] = dist[v] + 1; q.append(w)
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]; pred[w].append(v)
        delta = dict.fromkeys(N, 0.0)
        while stack:
            w = stack.pop()
            for v in pred[w]:
                delta[v] += sigma[v] / sigma[w] * (1 + delta[w])
            if w != s:
                bc[w] += delta[w]
    n = len(N)
    norm = (n - 1) * (n - 2)
    bc = {k: v / norm for k, v in bc.items()}
    # cross-domain reach: count of distinct domains among neighbours
    dom = {k: ("method" if k in METHOD else "physical" if k in PHYS else "theology") for k in N}
    reach = {k: len({dom[x] for x in und[k]} | {dom[k]}) for k in N}
    return req, dep, depth, trans, bc, reach, dom


METHOD = {"scripture", "creator-creature", "creation-real", "darkness", "description", "ontology", "desc-not-ont",
          "assumptions", "epistemic-levels", "coherence", "local-coherence", "regional-coherence", "global-coherence",
          "knowing-coherence", "coherence-not-fidelity", "empirical-constraint", "not-proof", "analogy-vs-identity",
          "category", "connectivity", "boundary-validity", "propagation-cycle"}
PHYS = {"relation", "object-first", "substrate", "runtime", "mediation", "possibility", "admissibility", "tendency",
        "actualisation", "stochasticity", "constrained-stochasticity", "identity-invariant", "persistence",
        "information-loss", "memory-configuration", "difference", "equivalence", "provenance",
        "discriminability", "projection", "compatibility", "joint-process", "aggregation", "layered-stability",
        "recovery-kinds", "endogenous-carrier", "individual-continuity", "transmit", "carry", "substitutability", "receive",
        "tcr", "nested-tcr", "coordination", "local-global", "regularity", "mathematics", "time", "matter",
        "manifestation", "purpose-upstream", "non-agentic", "constraint-generative"}


def main():
    intro = load_intro()
    req, dep, depth, trans, bc, reach, dom = metrics()
    interacting = {k: len(req[k]) + 1 for k in N}
    # load-bearing index components (reported separately; ranking uses rank-sum, not weights)
    ranks = {}
    for key, vals in (("trans", trans), ("bc", bc), ("depth", depth), ("reach", reach)):
        order = sorted(N, key=lambda k: -vals[k])
        for i, k in enumerate(order):
            ranks.setdefault(k, 0)
            ranks[k] += i
    ranked = sorted(N, key=lambda k: ranks[k])
    nodes = []
    for k, v in N.items():
        term, defi, cat, mat, diff, absn, decomp, lb, mis, ex = v
        nodes.append({
            "id": k, "term": term, "definition": defi, "epistemic_category": cat, "research_maturity": mat,
            "domain": dom[k], "prerequisites": sorted(req[k]), "dependents": sorted(dep[k]),
            "cross_domain_relations": sorted({b for a, t, b in EDGES if a == k and t in ("ANALOGOUS_TO", "NOT_IDENTICAL_TO")}
                                             | {a for a, t, b in EDGES if b == k and t in ("ANALOGOUS_TO", "NOT_IDENTICAL_TO")}),
            "evidence": sorted(b for a, t, b in EDGES if a == k and t == "EVIDENCED_BY"),
            "scripture_bounds": sorted(b for a, t, b in EDGES if a == k and t == "SCRIPTURALLY_BOUNDED_BY"),
            "intended_first_introduction": intro.get(k, {}).get("first"),
            "reactivation_points": intro.get(k, {}).get("reactivate", []),
            "example_needed": ex, "common_misunderstanding": mis, "conceptual_difficulty": diff,
            "abstraction_level": absn, "simultaneously_interacting_concepts": interacting[k],
            "decomposable": decomp, "context_load_hint": diff + absn + interacting[k],
            "load_bearing_declared": lb,
            "metrics": {"prerequisite_depth": depth[k], "transitive_dependents": trans[k],
                        "betweenness": round(bc[k], 4), "cross_domain_reach": reach[k],
                        "rank_sum": ranks[k], "rank": ranked.index(k) + 1},
        })
    graph = {"version": "2.0", "generated_by": "books/v2/tools/build_concept_graph.py",
             "edge_types": sorted({t for _, t, _ in EDGES}),
             "nodes": nodes,
             "evidence_nodes": [{"id": k, "label": v} for k, v in E.items()],
             "scripture_nodes": [{"id": k, "reference": v} for k, v in S.items()],
             "edges": [{"source": a, "type": t, "target": b} for a, t, b in EDGES]}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "concept-graph.json").write_text(json.dumps(graph, indent=1, ensure_ascii=False) + "\n")

    # Mermaid: REQUIRES backbone (B --> A means B is needed for A) plus NOT_IDENTICAL guardrails
    lines = ["%% Generated by books/v2/tools/build_concept_graph.py — prerequisite backbone and guardrails",
             "flowchart TB"]
    for k, v in N.items():
        lines.append(f'  {k.replace("-", "_")}["{v[0]}"]')
    for a, t, b in EDGES:
        if a in N and b in N and t == R:
            lines.append(f"  {b.replace('-', '_')} --> {a.replace('-', '_')}")
        elif a in N and b in N and t == "NOT_IDENTICAL_TO":
            lines.append(f"  {a.replace('-', '_')} -. not identical .- {b.replace('-', '_')}")
    for dname, members in (("Method", METHOD), ("Physical ontology", PHYS),
                           ("Life, persons, theology", set(N) - METHOD - PHYS)):
        lines.append(f'  subgraph {dname.split(",")[0].replace(" ", "_")}["{dname}"]')
        lines.append("    " + " & ".join(m.replace("-", "_") for m in sorted(members)))
        lines.append("  end")
    (OUT / "concept-graph.mmd").write_text("\n".join(lines) + "\n")

    # Markdown
    md = ["# Concept graph — *Coherent Biblical Ontology*, second edition", "",
          "Generated by `books/v2/tools/build_concept_graph.py` (the single source of truth); machine-readable form in "
          "`concept-graph.json`, Mermaid in `concept-graph.mmd`.", "",
          f"{len(N)} reader concepts, {len(E)} evidence nodes, {len(S)} Scripture nodes, {len(EDGES)} typed edges.", "",
          "## Load-bearing analysis", "",
          "Ranked by **rank-sum** across four separately reported measures (no weighted scalar): transitive "
          "dependents (how much of the book rests on it), betweenness (how often it lies on the shortest path between "
          "other concepts, undirected over all edge types), prerequisite depth (how much must precede it), and "
          "cross-domain reach (method / physical / theology neighbours).", "",
          "| Rank | Concept | Transitive dependents | Betweenness | Prereq depth | Cross-domain reach | Declared load-bearing | Difficulty | Abstraction |",
          "|---:|---|---:|---:|---:|---:|---|---:|---:|"]
    for i, k in enumerate(ranked[:25], 1):
        v = N[k]
        md.append(f"| {i} | {v[0]} | {trans[k]} | {bc[k]:.3f} | {depth[k]} | {reach[k]} | {'yes' if v[7] else 'no'} | {v[4]} | {v[5]} |")
    md += ["", "## Inventory", ""]
    for dname, members in (("Method and epistemology", METHOD), ("Physical ontology", PHYS),
                           ("Life, persons and theology", set(N) - METHOD - PHYS)):
        md += [f"### {dname}", ""]
        for k in [x for x in N if x in members]:
            v = N[k]
            node = next(n for n in nodes if n["id"] == k)
            md += [f"**{v[0]}** (`{k}`) — {v[1]}", "",
                   f"- category: {v[2]}; maturity: {v[3]}; difficulty {v[4]}/5; abstraction {v[5]}/5; "
                   f"decomposable: {'yes' if v[6] else 'no'}; interacting concepts at introduction: {interacting[k]}",
                   f"- requires: {', '.join(sorted(req[k])) or '—'}; direct dependents: {', '.join(sorted(dep[k])) or '—'}",
                   f"- first introduction: {node['intended_first_introduction'] or 'tbd'}"
                   + (f"; reactivated: {', '.join(node['reactivation_points'])}" if node['reactivation_points'] else ""),
                   f"- example: {v[9]}; common misunderstanding: {v[8] or '—'}"]
            if node["evidence"] or node["scripture_bounds"]:
                md.append(f"- evidence: {', '.join(E[e] for e in node['evidence']) or '—'}; Scripture: "
                          f"{', '.join(S[s] for s in node['scripture_bounds']) or '—'}")
            md.append("")
    md += ["## Guardrail edges (NOT_IDENTICAL_TO)", ""]
    for a, t, b in EDGES:
        if t == "NOT_IDENTICAL_TO":
            md.append(f"- {N[a][0]} ≠ {N[b][0]}")
    md += ["", "## Structural analogies (ANALOGOUS_TO — form, not identity)", ""]
    for a, t, b in EDGES:
        if t == "ANALOGOUS_TO":
            md.append(f"- {N[a][0]} ∼ {N[b][0]}")
    (OUT / "concept-graph.md").write_text("\n".join(md) + "\n")

    # terms file for the readability script
    alias = {"tcr": ["T-C-R", "TCR", "Transmit, Carry, Receive"], "possibility": ["T0"], "actualisation": ["T1", "actualised"],
             "manifestation": ["T2"], "stochasticity": ["stochastic"], "admissibility": ["admissible"],
             "identity-invariant": ["invariant"], "substrate": ["Relational Substrate"],
             "global-coherence": ["globally coherent"], "regularity": ["effective determinism"]}
    terms = []
    for k, v in N.items():
        short = {"equivalence": "equivalence class", "provenance": "provenance", "projection": "projection",
                 "joint-process": "joint process", "compatibility": "compatible receiver",
                 "boundary-validity": "boundary validity", "propagation-cycle": "cycle consistency","tcr": "Transmit–Carry–Receive", "possibility": "constrained possibility", "actualisation": "actualisation",
                 "identity-invariant": "invariant", "substrate": "substrate", "constrained-stochasticity": "constrained stochastic",
                 "regularity": "regularity", "carry": "carrier", "transmit": "transmit", "receive": "reception",
                 "difference": "difference", "persistence": "persistence", "coordination": "coordination",
                 "global-coherence": "global coherence", "local-coherence": "local coherence",
                 "regional-coherence": "regional coherence", "admissibility": "admissibility", "tendency": "tendency",
                 "stochasticity": "stochasticity", "relation": "relation", "personhood": "personhood",
                 "corruption": "corruption", "alignment": "alignment", "restoration": "restoration",
                 "analogy-vs-identity": "structural analogy", "category": "category"}.get(k)
        if short:
            terms.append({"id": k, "term": short, "aliases": alias.get(k, []),
                          "requires": [p for p in sorted(req[k]) if p in {
                              "tcr", "possibility", "actualisation", "identity-invariant", "substrate",
                              "constrained-stochasticity", "regularity", "carry", "transmit", "receive", "difference",
                              "persistence", "coordination", "global-coherence", "local-coherence", "regional-coherence",
                              "admissibility", "tendency", "stochasticity", "relation", "personhood", "corruption",
                              "alignment", "restoration", "analogy-vs-identity", "category"}]})
    (OUT / "terms-edition2.json").write_text(json.dumps({"terms": terms}, indent=1, ensure_ascii=False) + "\n")
    print("top load-bearing:", ", ".join(N[k][0] for k in ranked[:15]))


if __name__ == "__main__":
    main()
