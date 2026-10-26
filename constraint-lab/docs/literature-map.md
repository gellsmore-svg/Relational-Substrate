# Literature map

The ontology is not taken from these sources. Each entry records a mathematical tool, the assumptions that come with it, what this laboratory does not inherit, and why the tool is useful. Page numbers are given only where the citation was checked closely enough to rely on them. Otherwise the entry names the work and the year.

## Finite Markov chains

**Levin, Peres, Wilmer, *Markov Chains and Mixing Times*.**  
Tool: irreducibility, period, stationary distribution, total variation, mixing.  
Assumptions: a time-homogeneous kernel on a countable state space.  
Not inherited: ergodic theorems are not read as claims about physical equilibrium. A point-mass start on a period-2 chain does not converge in total variation; the laboratory says so, and uses Cesàro language where that is the true statement.  
Useful because every Generation 1 grammar is a finite kernel.

**Kemeny and Snell, *Finite Markov Chains*.**  
Tool: absorbing classes, fundamental matrix, first-step analysis.  
Assumptions: finite state space, stationary transitions.  
Not inherited: the narrative of “absorption as the end of a process” in applied models. Halt is a completion we flag.  
Useful for hitting and absorption bookkeeping once a prohibit cuts the hypercube.

**Cover and Thomas, *Elements of Information Theory*; Shannon, “A Mathematical Theory of Communication”, 1948.**  
Tool: entropy rate of a stationary process, `−Σ_i π_i Σ_j P_ij log P_ij`.  
Assumptions: the chain is started in stationarity, or the rate is the asymptotic per-step entropy.  
Not inherited: an identification of entropy rate with thermodynamic entropy, or with uncertainty about the world.  
Useful as a single comparable number for how sharply a grammar concentrates the toggle choice.

## Symbolic dynamics and forbidden patterns

**Lind and Marcus, *An Introduction to Symbolic Dynamics and Coding*, 1995.**  
Tool: shifts of finite type; a local forbidden list defines a subshift.  
Assumptions: a fixed alphabet and a finite list of forbidden blocks, usually on a symbolic sequence.  
Not inherited: the identification of our relational state with a one-dimensional symbolic sequence. Our “forbidden” object is a transition of a hypercube, not a word in a shift space.  
Useful because a hard constraint (`weight = 0`) is exactly a local rule that deletes transitions, and the support graph is the resulting subshift’s analogue.

## Canonical labelling

**McKay and Piperno, “Practical graph isomorphism, II”, *Journal of Symbolic Computation* 60 (2014) 94–112. DOI 10.1016/j.jsc.2013.09.003. arXiv:1301.1493.**  
Tool: nauty/Traces canonical labelling and automorphism groups.  
Assumptions: the input is a coloured graph, and the goal is a canonical form under graph isomorphism.  
Not inherited: the software, in this generation. For `N ≤ 5`, `|S_N| ≤ 120`, and exact permutation tables are short enough to test by orbit enumeration.  
Useful as the tool to adopt when `N` leaves the range where `S_N` can be listed, or when the object being canonicalised is no longer a complete pairwise state.

## Higher-order relations

**Battiston, Cencetti, Iacopini, Latora, Lucas, Patania, Young, Petri, “Networks beyond pairwise interactions: structure and dynamics”, *Physics Reports* 874 (2020) 1–92. DOI 10.1016/j.physrep.2020.05.004.**  
Tool: the distinction between a graph, a hypergraph, and a simplicial complex, and the dynamical systems written on each.  
Assumptions: many of the reviewed models put a process on a fixed higher-order topology (contagion, synchronisation, diffusion).  
Not inherited: those particular dynamical models, and the assumption that the higher-order relation is static while a node state moves. In this laboratory the relation *is* the state, and constraints reweight changes of relation.  
Useful because it is the cleanest public statement of the distinction the semantics axis is required to keep.

**Battiston and coauthors, “The physics of higher-order interactions in complex systems”, arXiv:2110.06023.**  
Tool: a shorter map of the same territory.  
Assumptions: as above. A journal version is not cited here, because this note was written against the preprint.  
Not inherited: the physical modelling programme.  
Useful as a second entry point that does not collapse hypergraphs into simplicial complexes.

**Iacopini, Petri, Barrat, Latora, “Simplicial models of social contagion”, *Nature Communications* 10 (2019) 2485.**  
Tool: a concrete simplicial interaction.  
Assumptions: contagion on a fixed simplicial complex; nodes carry an infection state.  
Not inherited: the contagion rule, and the fixed complex.  
Useful later, as a comparison target, if a simplicial cell is opened. It is not a template for Generation 1.

## Random graphs, motifs, adaptive networks

**Milo, Shen-Orr, Itzkovitz, Kashtan, Chklovskii, Alon, “Network motifs”, *Science* 298 (2002).**  
Tool: the idea of a small subgraph pattern that recurs above a stated null model.  
Assumptions: the null is typically a degree-preserving randomisation of a fixed observed network.  
Not inherited: that null. Our baseline is the uniform hypercube walk, which does not preserve degree. A motif here is a constraint grammar, not an over-represented subgraph of one dataset.  
Useful as a warning about what “motif” already means in the literature, so the catalogue does not silently switch meanings.

**Robins, Pattison, Kalish, Lusher, “An introduction to exponential random graph (p*) models for social networks”, *Social Networks* 29 (2007).**  
**Snijders, Pattison, Robins, Handcock, “New specifications for exponential random graph models”, *Sociological Methodology* 36 (2006).**  
Tool: exponential families of graph distributions; local configuration statistics with parameters.  
Assumptions: a distribution on graphs, often with a near-degeneracy problem when parameters push the mass onto a few extreme graphs.  
Not inherited: the social-network interpretation, and the estimation-from-data setting.  
Useful because a soft constraint in this laboratory is morally a local reweighting of a graph distribution, and the ERGM literature is the place where that reweighting is known to be capable of degenerating. Halt and near-absorbing corners are the corresponding phenomena here, and they are recorded rather than fitted away.

**Maslov and Sneppen, “Specificity and stability in topology of protein networks”, *Science* 296 (2002).**  
Tool: degree-preserving rewiring as a null.  
Assumptions: a fixed degree sequence on a simple graph.  
Not inherited: the null itself. The Generation 1 baseline toggles any edge and changes degrees freely. Degree-preserving rewiring is a later comparison kernel, not the unconstrained substrate.  
Useful so that a future “null model” discussion does not quietly replace `μ₀`.

**Gross and Blasius, “Adaptive coevolutionary networks: a review”, *Journal of the Royal Society Interface* 5 (2008).**  
**Cimini, Squartini, Saracco, Garlaschelli, Gabrielli, Caldarelli, “The statistical physics of real-world networks”, *Nature Physics* 15 (2019).**  
Tool: networks whose edges and whose node states co-evolve; ensembles of real networks.  
Assumptions: usually an embedding in a domain model (epidemic, game, regulatory net) with its own rates.  
Not inherited: those domain rates.  
Useful later, when `S > 0` gives entities a channel that co-evolves with the relations.

## Rewriting, closure, constraints on constraints

**Danos and Laneve, “Formal molecular biology”, *Theoretical Computer Science* 325 (2004).**  
Tool: Kappa calculus; site-graph rewriting with local rules.  
Assumptions: agents have sites, and rules are chemical.  
Not inherited: the molecular ontology. The archived programme already explored molecules; this laboratory does not start there.  
Useful as one existing calculus in which a local rule changes a relational complex, including by deletion.

**Tarski, “On the calculus of relations”, *Journal of Symbolic Logic* 6 (1941).**  
Tool: relation algebra.  
Assumptions: a Boolean algebra of binary relations with composition and converse.  
Not inherited: the claim that every higher-order fact reduces to an algebraic combination of binary relations. The hypergraph axis exists because that reduction is exactly what must remain optional.  
Useful if a later DSL grows composition operators, and as a reminder that “relation algebra” already has a meaning.

**Maturana and Varela, *Autopoiesis and Cognition*, 1980. Mossio and Moreno, “Organisational closure in biological organisms”, *History and Philosophy of the Life Sciences* 32 (2010).**  
Tool: organisational closure as a name for a network of constraints that maintains the conditions of its own existence.  
Assumptions: a biological individual, and a philosophical account of function.  
Not inherited: the biological claim, and the decision to treat closure as a primitive of the grammar.  
Useful at the interpretation level, after a grammar is observed to regenerate the conditions that keep it active. Generation 1 has `L = 0` and cannot yet express a constraint maintaining a constraint.

**Feinberg, *Foundations of Chemical Reaction Network Theory*.**  
Tool: deficiency, complex balance, and the way a reaction graph constrains steady states.  
Assumptions: mass-action (or a relative) on species concentrations.  
Not inherited: species, concentrations, and mass-action.  
Useful later if a rate presentation replaces the embedded jump chain.

**Kauffman, “Metabolic stability and epigenesis in randomly constructed genetic nets”, *Journal of Theoretical Biology* 22 (1969). Mortveit and Reidys, *An Introduction to Sequential Dynamical Systems*.**  
Tool: Boolean networks and sequential dynamical systems; local rules, global attractors.  
Assumptions: a fixed wiring and a synchronous or ordered update of node states.  
Not inherited: the fixed wiring. Here the wiring is the state.  
Useful as a comparison once `S > 0` gives each entity a bit and the relations are the dependency graph.

## Path ensembles

**Redner, *A Guide to First-Passage Processes*, 2001.**  
Tool: first-passage and hitting times.  
Assumptions: usually a Markov process with an absorbing target.  
Not inherited: a privileged target state. The laboratory does not designate “the triangle” or “the empty graph” as the success state of the search.  
Useful when a later report asks how long a declared pattern takes to appear. That question has to be declared as a question, not built into the census.

**E and Vanden-Eijnden, “Transition-path theory and path-finding algorithms for the study of rare events”, *Annual Review of Physical Chemistry* 61 (2010).**  
Tool: ensembles of reactive trajectories between two sets.  
Assumptions: a reversible diffusion, or a Markov jump process, with designated reactant and product sets.  
Not inherited: the reactant/product split, and the molecular-dynamics setting.  
Useful once a motif has two operational sets worth connecting. Doob’s h-transform, which conditions a chain on hitting a set, is a related tool and is not used in Generation 1. Using it would change the measure under study; if it is used later, the conditioned kernel must be labelled as conditioned.

## Probability as reweighting

**Jaynes, “Information theory and statistical mechanics”, *Physical Review* 106 (1957).**  
Tool: maximum entropy subject to constraints, as a way to choose a measure.  
Assumptions: the constraints are expected values, and the prior is specified.  
Not inherited: the claim that the physical ensemble *is* the maximum-entropy distribution, and the use of that claim as an ontological argument.  
Useful because our soft constraints are a declared reweighting, which is the same mathematical gesture, aimed at transitions rather than at a static ensemble.

**Richardson and Domingos, “Markov logic networks”, *Machine Learning* 62 (2006) 107–136.**  
Tool: first-order formulae as weighted constraints on a Markov network.  
Assumptions: a grounded graphical model, trained or hand-weighted, usually for prediction.  
Not inherited: learning weights from data, and the closed-world database interpretation.  
Useful as a neighbouring language in which “formula ⇒ weight” is already formal. Our DSL is smaller and is enumerated rather than learned.

**Ashby, *An Introduction to Cybernetics*, 1956.**  
Tool: requisite variety; a regulator has to have enough internal variety to meet the variety of disturbances.  
Assumptions: a regulator/disturbance split.  
Not inherited: that split, and the managerial reading.  
Useful at the interpretation level if a constraint grammar is later seen to be small relative to the state space it organises. It is not a Generation 1 statistic.

## Event sourcing

**Fowler, “Event Sourcing”, 2005 (martinfowler.com).**  
Tool: persist the sequence of events, and treat current state as a fold over that sequence.  
Assumptions: a software system whose audit log is the source of truth.  
Not inherited: the enterprise-application setting.  
Useful because a trajectory in this laboratory is the research object. Replay is the test that the fold is deterministic.

## Constructive deletion

Quotients, matroid deletion and contraction, and negative design in self-assembly all treat removal as a structure-forming operation. They are analogies. The laboratory does not import matroid axioms or a chemical designer. They are listed so that “deletion can be generative” is recognised as an existing mathematical idea, which makes it safer to notice the phenomenon in a census and less tempting to hard-code it as a primitive.

## Deferred libraries

XGI, HyperNetX, and GUDHI become relevant when a hypergraph cell or a simplicial cell is actually executed. They are not dependencies of Generation 1. Stochastic hybrid systems, with a continuous state and a discrete mode, wait until `S` or `G` introduces a continuous coordinate. Using them earlier would smuggle a geometry or a clock into a pre-geometric cell.
