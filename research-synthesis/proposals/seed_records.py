"""Agent-drafted seed content for the shared ledger (GT-P009 session, 2026-10-15).

The author's seed files (seeds/*.jsonl) were not supplied. This script writes the
agent's drafts so their origin is explicit and reproducible; rerunning it
regenerates the same records. Each reviewed connection gets a written review
record under proposals/reviews/. Nothing here is human-accepted.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWER = "agent: Claude Opus 5.5 (session of 2026-10-15)"
DATE = "2026-10-15"


def comp(**kw):
    return {d: {"verdict": v[0], "note": v[1]} for d, v in kw.items()}


CONNECTIONS = [
    {
        "connection_id": "X::0001",
        "from": "CL::F8N-MFPT-RESIDUAL",
        "to": "GT::GT-F78-LIFETIME-NOT-SET-BY-STATIONARY-LAW",
        "connection_type": "tested_structural_analogy",
        "scope": "Finite irreducible stationary Markov chains as studied in each programme: CL N=4 O=3 H2 pair-epoch chains; GT FREE N=5,6 O=2 graph chains. Stationary horizon only.",
        "rationale": "Both programmes exhibit, exactly and on their own side, a passage-type statistic that differs between two processes whose matched stationary quantities are equal: CL ordered-sibling MFPTs differ (446 slower, 274 faster) at identical source/target occupancy, clock and Kac recurrence; GT flexible-motif episode lifetimes differ by up to x25 between PCOMP and a comparator with the same stationary law, density, mean rate and edge lifetime. Map: matched occupancy <-> matched stationary law/density; Kac recurrence control <-> CT edge-lifetime calibration; MFPT <-> entrance-episode lifetime.",
        "comparison": comp(
            state=("differs", "CL: (pair mask, two-slot history) on N=4 O=3; GT: labelled graphs on N=5,6"),
            transition_law=("differs", "CL: H2 role controllers vs stationary-conditional Kpi-H1; GT: PCOMP path templates vs the ND Metropolis comparator"),
            support=("same", "both positive on an irreducible finite class"),
            clock=("differs", "CL: pair-event epoch (discrete); GT: continuous time and jump chain"),
            projection=("differs", "CL: material/class sets D; GT: predicate sets A"),
            intervention=("differs", "CL: matched controller with equal adjacent laws; GT: matched density and mean rate only"),
            horizon=("same", "stationary"),
            conditioning=("differs", "CL: stationary conditional source law; GT: entrance (Palm) episodes"),
        ),
        "independence": "shared_lineage",
        "independence_note": "Both branches descend from CL 8G and share the coherence validator, but the two computations use different chains and code paths. The convergence is a generic property of finite Markov chains (stationary mass does not fix first-passage laws), so it corroborates the method, not either programme's mechanism.",
        "controls": {"positive": ["CL: Kac recurrence equal by CL-T88 (control holds)", "GT: NULL and the ND fixed point reproduce closed forms (E5A frozen identities)"], "negative": ["Neither programme claims the difference is physical", "GT PATHF, with ND fully matched, shows only small differences, so the effect is not universal"]},
        "alternatives": ["The common pattern is the textbook fact that stationary laws do not determine hitting-time distributions; no deeper shared mechanism is implied", "GT's difference is driven by rate heterogeneity; CL's by history roles: different mechanisms"],
        "falsifiers": ["A CL or GT case where a declared matched control equalises the passage statistic as well (would narrow, not refute, the analogy)", "An error in either exact computation"],
        "evidence_refs": ["CL::CL-T88", "CL::CL-T89", "GT::GT-F79-ND-MATCHES-EDGE-LIFETIME"],
        "origin": "agent_drafted",
        "review_status": "agent_reviewed",
    },
    {
        "connection_id": "X::0002",
        "from": "CL::F8H-TEMPORAL-TESTS-REQUIRED",
        "to": "GT::GT-F82-E5A-COMPARATOR-AND-NUMERICAL-QUALIFICATIONS",
        "connection_type": "epistemic_compatibility",
        "scope": "Methodological findings of CL 8H and GT E5A; no shared formal object is asserted.",
        "rationale": "Both programmes conclude, from their own exact results, that one-time stationary occupancy is not a sufficient test: CL requires multi-time statistics, conditional process tests and Markov-order checks with explicit clock and projection; GT requires a comparator that declares where activity sits. The recommendations are compatible and mutually reinforcing as method, not as evidence about any mechanism.",
        "comparison": comp(
            state=("not_applicable", "methodological"), transition_law=("not_applicable", "methodological"), support=("not_applicable", "methodological"),
            clock=("same", "both insist the clock is declared"), projection=("same", "both insist the projection is declared"), intervention=("differs", "CL: process tests; GT: kinetic comparator"),
            horizon=("not_applicable", "methodological"), conditioning=("not_applicable", "methodological"),
        ),
        "independence": "shared_lineage",
        "independence_note": "GT adopted CL's coherence discipline from 8G; methodological agreement is expected and is not independent confirmation.",
        "controls": {"positive": [], "negative": []},
        "alternatives": ["The agreement reflects the shared method lineage rather than independent discovery"],
        "falsifiers": ["A programme showing that occupancy alone suffices for a declared persistence or history claim"],
        "evidence_refs": ["CL::F8H-PROCESS-GRAMMAR-WITHOUT-OCCUPANCY", "GT::GT-F78-LIFETIME-NOT-SET-BY-STATIONARY-LAW"],
        "origin": "agent_drafted",
        "review_status": "agent_reviewed",
    },
    {
        "connection_id": "X::0003",
        "from": "CL::F003-CLOCK-SPLIT",
        "to": "GT::GT-F20-TRIAD-CLOCK-REVERSAL",
        "connection_type": "explicit_contrast",
        "scope": "CL Generation 3C (N=3 independent triad) and GT E0A (FREE N=5). Both report clock dependence; the clock operations differ.",
        "rationale": "Both programmes find that conclusions depend on the clock, but the operations are not the same. CL's pair-event epoch counts only pair events and hides triad events, so a first-order full process looks memoryful on the epoch (projection plus time change). GT's continuous time and jump clock share one event sequence and differ only in holding-time weighting, so they change orderings (relaxation, sorting) but cannot create apparent memory. Treating them as one phenomenon would be an error; the shared theme is that the clock belongs to the estimand.",
        "comparison": comp(
            state=("differs", "CL: N=3 pair+triad; GT: N=5 graphs"), transition_law=("differs", "different rule families"), support=("same", "positive rates"),
            clock=("differs", "CL: epoch subsequence of pair events vs full events; GT: continuous time vs embedded jump chain"),
            projection=("differs", "CL epoch also projects out triad events; GT has no projection between its clocks"),
            intervention=("not_applicable", "none"), horizon=("differs", "CL: next-event statistics; GT: relaxation times"), conditioning=("same", "stationary"),
        ),
        "independence": "shared_lineage",
        "independence_note": "Shared lineage of the DSL; the contrast is between formal operations, not between computed numbers.",
        "controls": {"positive": ["CL-T15 relates the epoch law to the full-event law by a resolvent"], "negative": ["GT clocks share the state sequence by construction"]},
        "alternatives": ["A unified statement may exist: every clock is a random time change, and CL adds a projection"],
        "falsifiers": ["A GT case where switching between continuous and jump clocks alone changes Markov order (impossible under the embedded-chain construction)"],
        "evidence_refs": ["CL::CL-T15", "GT::GT-F69-CLOCK-SEPARATED-SORTING"],
        "origin": "agent_drafted",
        "review_status": "agent_reviewed",
    },
    {
        "connection_id": "X::0004",
        "from": "CL::F001-PAIRWISE-RISE",
        "to": "GT::GT-F12-SINGLE-WITNESS-REVERSIBLE",
        "connection_type": "explicit_contrast",
        "scope": "Reversibility of memoryless pairwise reweighting: CL Generation 1 labelled rules (N=2-5) versus GT label-covariant single-witness templates (O=2, N=5,6).",
        "rationale": "An apparent contradiction ('reweighting can break reversibility' versus 'every single-witness composition is reversible') dissolves on the formal objects. CL Generation 1 rules are labelled: each acts on one named edge and reads present/absent literals on other named edges (constraint-lab/docs/constraint-dsl.md). GT-F12 covers only label-covariant templates whose weight depends on witness counts. Label covariance plus single-witness structure gives a Gibbs potential; labelled multi-literal rules need not. GT-F13 shows label-covariant two-witness templates also break reversibility. The boundary is label covariance and witness arity.",
        "comparison": comp(
            state=("differs", "CL N=2-5 labelled graphs; GT N=5,6"), transition_law=("differs", "labelled literal rules vs covariant witness-count templates"), support=("same", "positive within the declared K bounds"),
            clock=("same", "stationary law (clock-free statement)"), projection=("not_applicable", "full state"), intervention=("not_applicable", "none"),
            horizon=("same", "stationary"), conditioning=("same", "none"),
        ),
        "independence": "shared_lineage",
        "independence_note": "Same DSL lineage; the contrast is decided by rule class, read from both programmes' definitions.",
        "controls": {"positive": ["GT: 32 gradient cells reversible to 6.5e-14"], "negative": ["GT-F13: covariant two-witness PATH templates are irreversible"]},
        "alternatives": ["Some CL Generation 1 cells may be label-covariant by accident; those should then be reversible"],
        "falsifiers": ["A label-covariant single-witness GT template that is irreversible", "An irreversible CL Generation 1 cell whose rule set is label-covariant and single-witness"],
        "evidence_refs": ["GT::GT-F13-NONGRADIENT-ARROW"],
        "origin": "agent_drafted",
        "review_status": "agent_reviewed",
    },
    {
        "connection_id": "X::0005",
        "from": "GT::GT-F05-RELATIONAL-POTENTIAL",
        "to": "CL::CL-T01",
        "connection_type": "shared_implementation_assumption",
        "scope": "GT templates built with the CL 8G DSL.",
        "rationale": "GT's relational potential (pi proportional to m^S) is the Gibbs law of a multiplicative-weight template. That multiplicative composition is CL-T01, inherited with the 8G DSL and kernel builder on which the GT branch was created. The agreement is shared implementation, not independent evidence.",
        "comparison": comp(
            state=("same", "pair graphs"), transition_law=("same", "multiplicative weights per matched rule instance"), support=("same", "positive multipliers (zero prohibit excluded)"),
            clock=("not_applicable", "algebraic"), projection=("not_applicable", "algebraic"), intervention=("not_applicable", "none"), horizon=("not_applicable", "algebraic"), conditioning=("not_applicable", "none"),
        ),
        "independence": "shared_lineage",
        "controls": {"positive": [], "negative": []},
        "alternatives": [],
        "falsifiers": ["A GT kernel built with non-multiplicative composition that still yields m^S (would make the relation incidental)"],
        "evidence_refs": [],
        "origin": "agent_drafted",
        "review_status": "agent_reviewed",
    },
    {
        "connection_id": "X::0006",
        "from": "GT::GT-F54-HARD-BAN-END-OF-SOFT-LADDER",
        "to": "CL::CL-T01",
        "connection_type": "qualifies",
        "scope": "Admissibility vs weighting: CL-T01's log-additive algebra (zero excluded) and GT's soft-to-hard path-formation ladder (FREE N=5).",
        "rationale": "CL-T01 places the zero (prohibit) weight outside the logarithmic algebra. GT-F54 shows that, for the measured stationary observables (partner index, flux), the hard ban sits at the continuous end of the soft ladder 1/2, 1/4, 1/9, 1/16, 0. 'Outside the algebra' therefore does not imply 'discontinuous in every observable'. The support still changes (one-way transitions, GT-F51), so the qualification is limited to those observables.",
        "comparison": comp(
            state=("differs", "algebraic statement vs N=5 graphs"), transition_law=("same", "multiplicative path-formation factor"), support=("differs", "zero removes transitions; positive factors keep them"),
            clock=("not_applicable", "stationary observables"), projection=("differs", "GT measures partner index and flux only"), intervention=("not_applicable", "none"), horizon=("same", "stationary"), conditioning=("not_applicable", "none"),
        ),
        "independence": "shared_lineage",
        "controls": {"positive": ["GT-F51: one-way transitions appear only at the hard end"], "negative": []},
        "alternatives": ["Continuity may fail for other observables (reachability, one-way release counts)"],
        "falsifiers": ["A stationary GT observable that jumps discontinuously between factor 1/16 and 0 on the same reachable class"],
        "evidence_refs": ["GT::GT-F51-ONE-WAY-RELEASE-MODE", "CL::F8D-LOG-ADDITIVITY"],
        "origin": "agent_drafted",
        "review_status": "agent_reviewed",
    },
    {
        "connection_id": "X::0007",
        "from": "CL::F018-LOCAL-VERSUS-INITIAL",
        "to": "GT::GT-F81-HUB-SELECTION-MEMORY-BY-FAMILY",
        "connection_type": "epistemic_compatibility",
        "scope": "CL H=0 Generations 8-8B (N=4) and GT E5A lagged hub (FREE N=5,6).",
        "rationale": "CL separates exact dependence on current higher-order structure from memory of the initial triad, which the visible pair process forgets. GT finds that a selected hub's advantage (a memory of an initial selection) decays toward zero in every law while current-state rules still shape the decay rate. The two are compatible instances of retention being distinct from current dependence; no shared formal object is asserted.",
        "comparison": comp(
            state=("differs", "N=4 pair+triad vs N=5,6 graphs"), transition_law=("differs", "different families"), support=("same", "positive, irreducible"),
            clock=("differs", "CL pair epoch; GT both clocks"), projection=("differs", "CL visible pair process; GT selected-vertex degree"), intervention=("not_applicable", "none"), horizon=("differs", "CL next-slot; GT lags 0-16"), conditioning=("differs", "CL initial triad; GT stationary start with selection"),
        ),
        "independence": "shared_lineage",
        "controls": {"positive": [], "negative": []},
        "alternatives": ["Decay of initial memory is generic for irreducible chains; the compatibility is weak"],
        "falsifiers": ["A GT hub advantage that does not decay (impossible under GT-F72's assumptions)"],
        "evidence_refs": ["GT::GT-F72-NO-LABELLED-CENTRE-AT-FINITE-N", "CL::F8H-CURRENT-VS-INITIAL-MEMORY"],
        "origin": "agent_drafted",
        "review_status": "agent_reviewed",
    },
    {
        "connection_id": "X::0008",
        "from": "CL::F8G-FORMAL-H-L-DISTINCTION",
        "to": "GT::GT-Q22-IDENTITY-THROUGH-REPLACEMENT",
        "connection_type": "qualifies",
        "scope": "The CL history axis H (rules reading reachable histories at identical state) and GT's proposed replacement-completion observable.",
        "rationale": "CL's H axis concerns rules that read history at identical complete current state. GT-Q22 asks only for an observable computed on trajectories; no rule reads it. CL's distinction therefore qualifies GT-Q22: answering it does not require or test a history axis, and the 8G compilation gate is not engaged.",
        "comparison": comp(
            state=("differs", "CL axis definition vs GT observable"), transition_law=("differs", "CL: rule reads history; GT: rule does not"), support=("not_applicable", "definitional"),
            clock=("not_applicable", "definitional"), projection=("not_applicable", "definitional"), intervention=("not_applicable", "definitional"), horizon=("not_applicable", "definitional"), conditioning=("not_applicable", "definitional"),
        ),
        "independence": "shared_lineage",
        "controls": {"positive": [], "negative": []},
        "alternatives": [],
        "falsifiers": ["A GT design in which the dynamics must respond to replacement completion (would engage H)"],
        "evidence_refs": ["CL::F8G-FORMAL-COMPILATION-TEST"],
        "origin": "agent_drafted",
        "review_status": "agent_reviewed",
    },
    {
        "connection_id": "X::0009",
        "from": "CL::CL-T88",
        "to": "GT::GT-F79-ND-MATCHES-EDGE-LIFETIME",
        "connection_type": "tested_structural_analogy",
        "scope": "Stationary-flux identities of finite irreducible chains used as controls.",
        "rationale": "Both are 'matching X fixes Y' identities that turn an apparent discriminator into a control. CL-T88: starting from the stationary conditional law on D, E[tau_D^+] = 1/pi(D), so equal occupancy forces equal Kac recurrence. GT-F79: E_pi[q] = 2M J_edge by exchangeability, so matching density and mean rate forces equal CT edge present-lifetime. Map: pi(D) <-> edge occupancy; Kac recurrence <-> edge present-lifetime; both follow from stationary flux balance across a set boundary.",
        "comparison": comp(
            state=("differs", "CL general finite chain; GT exchangeable FREE graph chains"), transition_law=("differs", "general vs exchangeable toggle chains"), support=("same", "irreducible"),
            clock=("differs", "CL discrete steps; GT continuous time"), projection=("differs", "CL set D; GT single slot"), intervention=("same", "both used as matched controls"), horizon=("same", "stationary"), conditioning=("differs", "CL stationary-conditional start; GT stationary rates"),
        ),
        "independence": "shared_lineage",
        "independence_note": "Both are standard stationary-flux identities; each was verified in its own programme (CL exact atlas; GT 12 laws to 7e-15). Their agreement is mathematical, not empirical.",
        "controls": {"positive": ["CL-F10 exact atlas checks", "GT E5A post hoc verification on 12 laws"], "negative": []},
        "alternatives": [],
        "falsifiers": ["A counterexample to either identity under its stated assumptions"],
        "evidence_refs": ["CL::F8N-MFPT-RESIDUAL"],
        "origin": "agent_drafted",
        "review_status": "agent_reviewed",
    },
]

PROPOSALS = [
    {"proposal_id": "P::0001", "from": "CL::F003-CLOCK-SPLIT", "to": "GT::GT-F69-CLOCK-SEPARATED-SORTING", "connection_type": "exact_theorem_correspondence", "status": "rejected",
     "scope": "Clock dependence in both programmes", "rationale": "Initial draft: the CL clock split and GT's clock-separated sorting are the same phenomenon.",
     "decision_rationale": "Rejected after comparing formal objects: CL's epoch hides triad events (projection plus time change), GT's clocks share one event sequence. Replaced by X::0003 (explicit contrast).",
     "comparison": {}, "independence": "shared_lineage", "controls": {"positive": [], "negative": []}, "alternatives": [], "falsifiers": [], "evidence_refs": [], "origin": "agent_drafted",
     "review": {"reviewer": REVIEWER, "date": DATE, "record": "proposals/reviews/P-0001.md", "human": False}},
    {"proposal_id": "P::0002", "from": "CL::F001-PAIRWISE-RISE", "to": "GT::GT-F12-SINGLE-WITNESS-REVERSIBLE", "connection_type": "explicit_contrast", "status": "rejected",
     "scope": "Reversibility", "rationale": "Initial draft: the two findings contradict each other.",
     "decision_rationale": "Rejected as a contradiction: the rule classes differ (labelled literal rules vs label-covariant single-witness templates). Kept as a scoped contrast in X::0004.",
     "comparison": {}, "independence": "shared_lineage", "controls": {"positive": [], "negative": []}, "alternatives": [], "falsifiers": [], "evidence_refs": [], "origin": "agent_drafted",
     "review": {"reviewer": REVIEWER, "date": DATE, "record": "proposals/reviews/P-0002.md", "human": False}},
    {"proposal_id": "P::0003", "from": "GT::GT-F67-FLOOR-IS-AN-EXACT-ODDS-LEVER", "to": "CL::CL-T18", "connection_type": "untested_hypothesis", "status": "proposed",
     "scope": "Single-toggle chains whose rates do not read the toggled slot",
     "rationale": "GT's stationary balance identity (odds = E[F|x_e=0]/E[D|x_e=1]; GT transfer note T-8) may contain CL-T18's autonomous single-action occupancy factorisation as the special case where F and D read only hidden bits.",
     "comparison": {}, "independence": "unknown", "controls": {"positive": [], "negative": []}, "alternatives": ["CL-T18's factorisation may need assumptions S1 does not supply (independence of the other pair bits)"],
     "falsifiers": ["A CL-T18 system whose action odds differ from the S1 ratio", "A hidden-bit coupling that breaks the 'rates do not read the toggled slot' assumption"], "evidence_refs": [], "origin": "agent_drafted"},
    {"proposal_id": "P::0004", "from": "GT::GT-F68-FIRST-ORDER-SORTING-INDEX", "to": "CL::F016-CURRENT-SLOT-INFORMATION", "connection_type": "tested_structural_analogy", "status": "undetermined",
     "scope": "Higher-order context effects on pair events", "rationale": "Both describe dependence of a pair event on higher-order current structure (GT: witness floor and held degree; CL: triad gate).",
     "decision_rationale": "Undetermined: the objects differ (a first-order stationary odds expansion around the uniform law versus local conditional slot information) and no map between witness counts and gate literals has been checked. Theme membership is recorded through C::higher-order-context instead.",
     "comparison": {}, "independence": "shared_lineage", "controls": {"positive": [], "negative": []}, "alternatives": [], "falsifiers": ["A declared map under which the two statistics disagree in sign"], "evidence_refs": [], "origin": "agent_drafted",
     "review": {"reviewer": REVIEWER, "date": DATE, "record": "proposals/reviews/P-0004.md", "human": False}},
    {"proposal_id": "P::0005", "from": "HIST::505-507", "to": "C::occupancy-vs-process", "connection_type": "untested_hypothesis", "status": "proposed",
     "scope": "Historical archives 505-507 / Work 11 / 46-48 (not available)",
     "rationale": "Pending pointer only. The 01 prompt names historical evidence that may bear on these themes. Nothing from it is claimed until the archives are taken in under a declared intake procedure.",
     "comparison": {}, "independence": "unknown", "controls": {"positive": [], "negative": []}, "alternatives": [], "falsifiers": ["Intake shows the archive does not address the theme"], "evidence_refs": [], "origin": "agent_drafted"},
    {"proposal_id": "P::0006", "from": "EXT::2026-10-15-cross-research-synthesis", "to": "C::predictive-sufficiency", "connection_type": "untested_hypothesis", "status": "proposed",
     "scope": "The external 2026-10-15 synthesis (not supplied)",
     "rationale": "Pending pointer only. The supplied-but-missing synthesis is a dated interpretation; its claims must be registered as proposals when the file is supplied.",
     "comparison": {}, "independence": "unknown", "controls": {"positive": [], "negative": []}, "alternatives": [], "falsifiers": ["The synthesis does not make this claim"], "evidence_refs": [], "origin": "agent_drafted"},
    {"proposal_id": "P::0007", "from": "GT::GT-F80-CLOSEW-CLOSURE-RECOVERY", "to": "CL::Q-H2-CONTROLLED-PASSAGE", "connection_type": "untested_hypothesis", "status": "undetermined",
     "scope": "Recovery/persistence under closure vs controlled passage",
     "rationale": "GT's closure-driven recovery of flexible organisations might be a passage phenomenon in CL's sense (return to a declared set under matched controls).",
     "decision_rationale": "Undetermined: GT's comparator is qualified (X-KINHET) and CL's question uses a matched-source design GT has not applied. Recorded as shared question XQ::01 instead.",
     "comparison": {}, "independence": "shared_lineage", "controls": {"positive": [], "negative": []}, "alternatives": ["GT's effect is rate heterogeneity (GT-F78)"], "falsifiers": ["Under a CL-style matched-source design the GT effect vanishes"], "evidence_refs": [], "origin": "agent_drafted",
     "review": {"reviewer": REVIEWER, "date": DATE, "record": "proposals/reviews/P-0007.md", "human": False}},
    {"proposal_id": "P::0008", "from": "CL::CL-F05", "to": "GT::GT-F82-E5A-COMPARATOR-AND-NUMERICAL-QUALIFICATIONS", "connection_type": "common_definition", "status": "rejected",
     "scope": "Discovery candidate (rank 1 by TF-IDF cosine 0.19 on 2026-10-15)", "rationale": "Top-ranked retrieval candidate from rssynth discover.",
     "decision_rationale": "Rejected: a false positive from shared methodological boilerplate ('frozen', 'checks', 'items', 'controls'). CL-F05 is a finite verification record for H0 items; GT-F82 is a comparator and numerical qualification for E5A. No shared formal object. Kept as a test case of retrieval false positives.",
     "comparison": {}, "independence": "shared_lineage", "controls": {"positive": [], "negative": []}, "alternatives": [], "falsifiers": [], "evidence_refs": [], "origin": "discovery_candidate",
     "review": {"reviewer": REVIEWER, "date": DATE, "record": "proposals/reviews/P-0008.md", "human": False}},
]

QUESTIONS = [
    {"question_id": "XQ::01", "status": "open", "statement": "Which declared comparison process separates organisation (or history) from kinetics in both programmes, and does each programme's design transfer to the other?",
     "refs": ["CL::Q-H2-CONTROLLED-PASSAGE", "GT::GT-Q21-KINETICS-AWARE-COMPARATOR", "C::matched-control-design"],
     "discriminating_tests": [{"test": "Apply CL's matched-source passage design (CL-T85, CL-T89) to GT's flexible predicates on the same 12 E5A laws", "would_show": "whether GT's CLOSEW/PATHF signals survive a CL-style matched control", "status": "proposed_not_authorised"},
                              {"test": "Report CL MFPT residuals in an anchor-local event clock", "would_show": "whether CL's residuals depend on where activity sits", "status": "proposed_not_authorised"}]},
    {"question_id": "XQ::02", "status": "open", "statement": "Does GT's stationary balance identity (T-8) hold for CL O=3 templates and contain CL-T18 as a special case?",
     "refs": ["GT::GT-F67-FLOOR-IS-AN-EXACT-ODDS-LEVER", "CL::CL-T18"],
     "discriminating_tests": [{"test": "Check the two hypotheses of S1 (single toggles; rates independent of the toggled slot) on each CL template family, then compare odds on CL-T18 systems", "would_show": "exact correspondence, partial overlap or failure", "status": "proposed_not_authorised"}]},
    {"question_id": "XQ::03", "status": "open", "statement": "Can every clock dependence in both programmes be written as a random time change plus a declared projection, and which effects need the projection?",
     "refs": ["CL::F003-CLOCK-SPLIT", "GT::GT-F20-TRIAD-CLOCK-REVERSAL", "C::clock-readout-dependence"],
     "discriminating_tests": [{"test": "Express CL's pair epoch as a time change of the full process composed with the triad projection; check which CL memory effects vanish without the projection", "would_show": "whether clock effects and projection effects separate cleanly", "status": "proposed_not_authorised"}]},
    {"question_id": "XQ::04", "status": "open", "statement": "Can identity through replacement be defined as a trajectory observable that never engages a history axis, and does it distinguish GT's flexible organisations from flicker?",
     "refs": ["GT::GT-Q22-IDENTITY-THROUGH-REPLACEMENT", "CL::F8H-FIXED-STATE-NONCOMPILABILITY", "C::history-as-predictive-variable"],
     "discriminating_tests": [{"test": "Define replacement completion on GT E5A laws and confirm by inspection that no rule reads it (8G gate not engaged)", "would_show": "whether persistence through turnover is replacement or flicker", "status": "proposed_not_authorised"}]},
    {"question_id": "XQ::05", "status": "pending_source", "statement": "What do the historical 505-507 / Work 11 / 46-48 materials contribute to the occupancy-versus-process and predictive-sufficiency themes?",
     "refs": ["HIST::505-507", "HIST::work-11", "HIST::46-48"],
     "discriminating_tests": [{"test": "Take the archives in under a declared intake procedure (05_HISTORICAL_INTAKE.md, not supplied), then register each claim as a proposal", "would_show": "which historical claims are primary evidence and which are interpretation", "status": "blocked_on_source"}]},
    {"question_id": "XQ::06", "status": "open", "statement": "Which claims of the 2026-10-15 cross-research synthesis survive source checking against the pinned ledgers?",
     "refs": ["P::EXT-C01", "P::EXT-C02", "P::EXT-C09", "P::EXT-C22"],
     "discriminating_tests": [{"test": "Review each registered claim (P::EXT-C01 to P::EXT-C22) against the pinned ledgers; restate checkable ones as pairwise proposals", "would_show": "agreement, qualification or rejection per claim", "status": "claims_registered_review_pending"}],
     "notes": "The synthesis is stored verbatim (reports/external-2026-10-15-cross-research-synthesis.md); 22 claims are registered as proposals, 7 of them blocked on private historical archives."},
    {"question_id": "XQ::07", "status": "open", "statement": "Is there a common mathematical operator behind CL's predictive sufficiency and GT's persistence, or only a common question?",
     "refs": ["C::predictive-sufficiency", "C::passage-and-persistence", "C::occupancy-vs-process"],
     "discriminating_tests": [{"test": "Write both as functionals of the same generator and stopping sets, and check whether one determines the other on a shared small chain", "would_show": "a shared operator, a one-way relation, or none", "status": "proposed_not_authorised"}],
     "notes": "The stronger common element is currently a question, not a universal operator, and not a derivation of gravity."},
]

REVIEW_TEMPLATE = """# Review record {rid}

- **Reviewer:** {reviewer}
- **Date:** {date}
- **Status set:** {status}
- **Decision category (agent recommendation):** {decision}
- **Human acceptance:** not given. This record supports agent review only; adoption needs the author's review of the draft PR.

## Claim

{rationale}

## Formal comparison

| Dimension | Verdict | Note |
| --- | --- | --- |
{rows}

## Checks performed

- Source identifiers resolved at the pinned commits (`sources/manifest.json`).
- Statements and scopes read in full from the pinned ledgers.
- Independence: {independence}. {independence_note}

## Alternatives and falsifiers

{alts}
"""


PINS = {"CL": "e650d71bda7203c8018d8bd134c5496a03d74a11", "GT": "79fa6b0119449bd56359acf4436015df27855f43"}
RETRIEVAL = "TF-IDF cosine over statements (rssynth discover, 2026-10-15); a ranking aid only"

# Conformance fields (architecture contract 02, discovery rubric 03). Decision categories are the agent's
# recommendation; review_status says who reviewed. Links resting on closed-but-unreviewed rounds (CL 008N,
# GT-P009) are capped at 'qualified'.
DECISIONS = {
    "X::0001": ("qualified", "observed", ["GT::GT-F77-PATHF-CENTRES-PERSIST-AGAINST-MATCHED-ND"], 0.0, "numerical_exact", "Both sides exact on finite chains; rests on 008N and GT-P009, both closed but unreviewed"),
    "X::0002": ("qualified", "methodological", [], 0.061497, "mixed", "Methodological agreement under shared lineage; GT side from unreviewed GT-P009"),
    "X::0003": ("accepted_bounded", "formal", [], 0.023507, "mixed", "The contrast of clock operations follows from the two definitions"),
    "X::0004": ("accepted_bounded", "formal", [], 0.038925, "mixed", "The rule classes are read from both programmes' definitions"),
    "X::0005": ("accepted_bounded", "formal", [], 0.0, "theorem", "A lineage fact: GT kernels use the CL 8G DSL"),
    "X::0006": ("qualified", "observed", ["GT::GT-F51-ONE-WAY-RELEASE-MODE"], 0.0, "mixed", "Holds only for the measured stationary observables; the support still changes"),
    "X::0007": ("qualified", "interpretive", [], 0.030043, "mixed", "Weak, generic compatibility; GT side from unreviewed GT-P009"),
    "X::0008": ("qualified", "methodological", [], 0.050017, "qualitative_report", "A definitional qualification of an open GT-P009 question"),
    "X::0009": ("qualified", "formal", [], 0.103294, "theorem", "Both identities proved; GT side from unreviewed GT-P009"),
}


def review_vector(*, retrieval, evidence, formal, observable, scope, independence, counter, falsify, relevance):
    return {
        "semantic_resemblance": {"assessment": "lexical retrieval only; not evidence", "retrieval_score": retrieval, "method": RETRIEVAL} if retrieval is not None else {"assessment": "unknown"},
        "formal_comparability": {"assessment": formal},
        "observable_comparability": {"assessment": observable},
        "scope_compatibility": {"assessment": scope},
        "evidence_status": {"assessment": evidence[1], "status": evidence[0]},
        "independence": {"assessment": independence},
        "counterexamples_or_nulls": {"assessment": counter},
        "falsifiability": {"assessment": falsify},
        "research_relevance": {"assessment": relevance},
    }


def history(*entries):
    return [{"date": DATE, "actor": REVIEWER, "human": False, "status": st, "decision_category": dc, "rationale": why} for st, dc, why in entries]


def add_conformance(x: dict) -> None:
    dc, basis, counter, score, ev, note = DECISIONS[x["connection_id"]]
    comp = x["comparison"]
    x["decision_category"] = dc
    x["epistemic_basis"] = basis
    x["counterevidence_refs"] = counter
    x["reviewed_source_commits"] = {ns: PINS[ns] for ns in ("CL", "GT") if x["from"].startswith(ns + "::") or x["to"].startswith(ns + "::")}
    x["review_vector"] = review_vector(
        retrieval=score, evidence=(ev, note),
        formal="; ".join(f"{d}: {comp[d]['verdict']}" for d in ("state", "transition_law", "support")),
        observable="; ".join(f"{d}: {comp[d]['verdict']}" for d in ("projection", "clock")),
        scope="; ".join(f"{d}: {comp[d]['verdict']}" for d in ("horizon", "conditioning", "intervention")),
        independence=f"{x['independence']}: {x.get('independence_note', 'shared 8G lineage')}",
        counter="; ".join(x["alternatives"]) or "none recorded",
        falsify="; ".join(x["falsifiers"]) or "none recorded",
        relevance=x["scope"])
    x["decision_history"] = history(("agent_reviewed", dc, f"Agent review on {DATE}: {note}. Awaiting the author's acceptance."))


FALSE_ATTRACTORS = [
    ("P::FA-01", "GT::GT-F09-POTENTIAL-AS-MECHANISM", "C::physical-attraction", "tested_structural_analogy",
     "Tempting: the GT relational basin is gravitational attraction.",
     "Rejected (false-attractor control, rubric 03): the shared word is 'basin' or 'attractive'. GT derives no acceleration, metric, displacement or moving object, and raw gathering is density composition (GT-F62). A metaphor is not a derivation.",
     ["GT::GT-F62-NATIVE-GATHERING-IS-DENSITY-COMPOSITION", "GT::GT-F72-NO-LABELLED-CENTRE-AT-FINITE-N"]),
    ("P::FA-02", "GT::GT-F74-INTACT-MOTIFS-NO-CT-PERSISTENCE", "GT::GT-F80-CLOSEW-CLOSURE-RECOVERY", "common_definition",
     "Tempting: retention and reconstruction are the same persistence.",
     "Rejected (false-attractor control): in the same E5A laws intact motifs are not retained beyond ND (GT-F74), while closure re-forms lost links in flexible organisations (GT-F80). Retention and reconstruction vary independently.",
     ["GT::GT-F74-INTACT-MOTIFS-NO-CT-PERSISTENCE"]),
    ("P::FA-03", "CL::CL-T31", "GT::GT-F19-ACTIVITY-WITHOUT-BASIN", "exact_theorem_correspondence",
     "Tempting: a stationary match means an identical path law.",
     "Rejected (false-attractor control): both records show a stationary match (CL-T31: H0 occupancy and one-step rows; GT-F19: COMPETE's law equals NULL's) together with different processes (CL-T33: exact order two; GT-F19: different activity; GT-F78: different lifetimes).",
     ["CL::CL-T33", "CL::F8H-PROCESS-GRAMMAR-WITHOUT-OCCUPANCY", "GT::GT-F78-LIFETIME-NOT-SET-BY-STATIONARY-LAW"]),
    ("P::FA-04", "CL::F8C-PROJECTION-GEOMETRY", "CL::CL-T55", "common_definition",
     "Tempting: the same abstract graph class carries the same higher-order role.",
     "Rejected (false-attractor control): graph-class conditioning retains only part of the slot information (F8C-PROJECTION-GEOMETRY), graph-only quotienting is invalid for labelled rules (F011), and the graph-class-preserving refinement needs 28 marked-pair roles (CL-T55).",
     ["CL::F011-QUOTIENT-INVALID", "CL::CL-T55"]),
    ("P::FA-05", "CL::F8H-CURRENT-VS-INITIAL-MEMORY", "GT::GT-F81-HUB-SELECTION-MEMORY-BY-FAMILY", "common_definition",
     "Tempting: persistent current-history efficacy is persistent memory of the initial register.",
     "Rejected (false-attractor control): CL-F8H shows current history stays efficacious while initial information decays, so the two are distinct. GT-F81 measures only decay of an initial selection. The compatible reading is X::0007, not an identity.",
     ["CL::F8H-CURRENT-VS-INITIAL-MEMORY"]),
]


def write_all(root: Path = ROOT) -> None:
    (root / "proposals" / "reviews").mkdir(parents=True, exist_ok=True)
    for x in CONNECTIONS:
        add_conformance(x)
        rid = x["connection_id"].replace("::", "-")
        x["review"] = {"reviewer": REVIEWER, "date": DATE, "record": f"proposals/reviews/{rid}.md", "human": False}
        rows = "\n".join(f"| {d} | {v['verdict']} | {v['note']} |" for d, v in x["comparison"].items())
        alts = "\n".join([f"- Alternative: {a}" for a in x["alternatives"]] + [f"- Falsifier: {f}" for f in x["falsifiers"]]) or "- none recorded"
        (root / x["review"]["record"]).write_text(REVIEW_TEMPLATE.format(rid=x["connection_id"], reviewer=REVIEWER, date=DATE, status=x["review_status"], decision=x["decision_category"], rationale=x["rationale"], rows=rows, independence=x["independence"], independence_note=x.get("independence_note", ""), alts=alts), encoding="utf-8")
    for pid, a, b, ctype, rationale, decision, counter in FALSE_ATTRACTORS:
        PROPOSALS.append({"proposal_id": pid, "from": a, "to": b, "connection_type": ctype, "status": "rejected", "scope": "False-attractor control (discovery rubric 03)", "rationale": rationale, "decision_rationale": decision,
                          "comparison": {}, "independence": "unknown", "controls": {"positive": [], "negative": []}, "alternatives": [], "falsifiers": [], "evidence_refs": [], "origin": "agent_drafted", "false_attractor_control": True, "within_programme": a.split("::")[0] == b.split("::")[0],
                          "review": {"reviewer": REVIEWER, "date": DATE, "record": f"proposals/reviews/{pid.replace('::', '-')}.md", "human": False}, "counterevidence_refs": counter})
    for p in PROPOSALS:
        pending = p["from"].startswith(("HIST::", "EXT::"))
        dc = {"rejected": "rejected", "undetermined": "candidate", "proposed": "blocked_missing_source" if pending else "candidate"}[p["status"]]
        p["decision_category"] = dc
        p["epistemic_basis"] = "question" if p["connection_type"] == "untested_hypothesis" else "formal"
        p.setdefault("counterevidence_refs", [])
        if p["status"] == "proposed":
            p["decision_history"] = history(("proposed", dc, "Agent draft; unreviewed"))
        else:
            p["review_vector"] = review_vector(retrieval=None, evidence=("unknown", "not assessed beyond the decision rationale"), formal=p.get("decision_rationale", ""), observable="unknown", scope=p["scope"], independence=p["independence"], counter="; ".join(p["counterevidence_refs"]) or "see decision rationale", falsify="; ".join(p["falsifiers"]) or "unknown", relevance="unknown")
            p["decision_history"] = history(("proposed", "candidate", "Agent draft"), (p["status"], dc, p["decision_rationale"]))
    for p in PROPOSALS:
        if "review" in p:
            (root / p["review"]["record"]).write_text(f"# Review record {p['proposal_id']}\n\n- **Reviewer:** {REVIEWER}\n- **Date:** {DATE}\n- **Decision:** {p['status']}\n\n## Proposal\n\n{p['rationale']}\n\n## Decision rationale\n\n{p['decision_rationale']}\n", encoding="utf-8")

    def dump(path, rows):
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text("".join(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")

    dump("ledger/connections.jsonl", CONNECTIONS)
    existing = [json.loads(line) for line in (root / "proposals/candidate-relations.jsonl").read_text().splitlines() if line.strip()] if (root / "proposals/candidate-relations.jsonl").exists() else []
    dump("proposals/candidate-relations.jsonl", PROPOSALS + [r for r in existing if r.get("origin") in ("author_seed", "external_synthesis", "agent_restatement")])
    dump("ledger/questions.jsonl", QUESTIONS)


if __name__ == "__main__":
    write_all(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT)
