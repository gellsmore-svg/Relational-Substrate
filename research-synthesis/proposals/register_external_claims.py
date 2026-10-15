"""Register the claims of the external 2026-10-15 cross-research synthesis as unapproved proposals.

The synthesis is stored verbatim in reports/external-2026-10-15-cross-research-synthesis.md.
- Each claim keeps a verbatim quote, checked here against the stored file, plus its section,
  what the synthesis cites (as written) and its own assessment where it gives one.
- The mapping of cited items to pinned finding ids is the agent's own work and is labelled
  `source_mapping: agent`, because the synthesis cites reports and generations, not ids.
- The synthesis is the claim's provenance (`provenance_ref`), not its evidence.
- Claims resting on private historical archives are blocked_missing_source.
- Nothing is reviewed or promoted. Re-running replaces only records with origin
  `external_synthesis` and leaves every other record untouched.

Usage: python3 research-synthesis/proposals/register_external_claims.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = "reports/external-2026-10-15-cross-research-synthesis.md"
PROV = "EXT::2026-10-15-cross-research-synthesis"
DATE = "2026-10-15"
SYN_PINS = "The synthesis reviewed CL at 9b2f857 (8M) and observed GT at 2bd18c6 (GT-P009 prompt stored, before E5A ran); the shared layer pins CL e650d71 (8N) and GT 79fa6b0 (GT-P009 closed)."

H = {
    "w11": "HIST::rs_work_round11/findings.md",
    "w46": "HIST::rs_work_round46_moments/REPORT.md",
    "w47": "HIST::rs_work_round47/REPORT.md",
    "w48": "HIST::rs_work_round48/REPORT.md",
    "l506": "HIST::rs_sources/RS_Baseline_Post_506Z/RS_Baseline_Post_506Z/02_EXPERIMENT_LEDGER_505_506.md",
    "l507": "HIST::rs_sources/RS_Baseline_Post_507/RS_Baseline_Post_507/RS_507_Integrated_Ledger.md",
    "n507": "HIST::rs_sources/RS_Baseline_Post_507/RS_Baseline_Post_507/RS_507_Negatives_And_Corrections.md",
}
SC = "SC::stochastic-calculator/RS_FINDINGS.md"

# (id, section, verbatim quote, cited_as (as written), synthesis assessment or None, sources, epistemic basis,
#  unresolved citations, overlaps, context notes)
CLAIMS = [
    ("EXT-C01", "§0, §4", "The most defensible common finding is **future-relevant relational information**.",
     ["Historical Work 11, 46, 47, 48", "CL 8H–8M conditioned-row and temporal-word tests"], "Strong mathematical family resemblance; different kernels",
     [H["w11"], H["w46"], H["w47"], H["w48"], "CL::F8H-FIXED-STATE-NONCOMPILABILITY", "CL::CL-T29", "CL::F8M-H2-STATIONARY-H1-RESIDUAL"], "interpretive",
     [], ["C::predictive-sufficiency", "P::SYN-C001", "XQ::07"], []),
    ("EXT-C02", "§4", "Thus **stationary occupancy match does not entail matching longer temporal organisation**.",
     ["CL 8M: all 72 non-neutral tested cells strict H2; Kπ matches one-/two-time (P,h1) laws; process words first differ at length four"], None,
     ["CL::F8M-STRICT-H2-ROLE-ATLAS", "CL::F8M-STATIONARY-H1-MATCHING", "CL::F8M-H2-STATIONARY-H1-RESIDUAL"], "observed",
     [], ["C::occupancy-vs-process", "X::0001", "P::FA-03"], []),
    ("EXT-C03", "§0, §5", "A second strong common thread is **contextual relational topology**.",
     ["Historical 505G–J, 507O/Q/U/W", "CL 8C gate/slot, 8F shape at fixed count, 8M role classes", "GT E2 cycle affinity, E4/P008 witness floor and degree"], "Strong mechanism-level analogy, not unified law",
     [H["l507"], "CL::F8C-PROJECTION-GEOMETRY", "CL::F8F-FIRST-PATH-SHAPE", "GT::GT-F64-CHORD-SWITCHES-SITE-OFF", "GT::GT-F67-FLOOR-IS-AN-EXACT-ODDS-LEVER", "GT::GT-F68-FIRST-ORDER-SORTING-INDEX"], "interpretive",
     [], ["C::higher-order-context", "P::SYN-C004", "P::0004"], []),
    ("EXT-C04", "§0, §5", "There is, however, **no demonstrated common universal operator** tying historical reconstruction, Constraint Laboratory gates and Gravity/Time witness floors into one dynamical law.",
     ["Historical reconstruction", "CL gates", "GT witness floors"], None,
     [H["l507"], "CL::F8C-PROJECTION-GEOMETRY", "GT::GT-F67-FLOOR-IS-AN-EXACT-ODDS-LEVER"], "interpretive",
     [], ["XQ::07"], []),
    ("EXT-C05", "§5", "PATHF and PATHH can have equivalent local balance but sort through different kinetics, respectively faster formation and longer survival.",
     ["GT-P008"], None,
     ["GT::GT-F69-CLOCK-SEPARATED-SORTING", "GT::GT-F68-FIRST-ORDER-SORTING-INDEX"], "observed",
     [], [], ["Within-GT restatement; checkable against GT-P008's derivation (S5)."]),
    ("EXT-C06", "§5", "A first-order formula correctly accounted for all **16 published within-reference ordering comparisons**, but this comparison was **post hoc** and seven algebraic reversal shapes have not been checked at full strength.",
     ["GT-P008"], None,
     ["GT::GT-F71-SORTING-DECOMPOSITION-POSTHOC", "GT::GT-F68-FIRST-ORDER-SORTING-INDEX", "GT::GT-Q18-REVERSAL-AT-W4"], "observed",
     [], [], ["Within-GT restatement."]),
    ("EXT-C07", "§0, §7", "A third thread is that **persistence is not a single quantity**.",
     ["Historical 505–507 retention/resilience/reconstruction", "SC-026 readout", "GT-P008/P009 metastability"], "Moderate conceptual connection; direct benchmark absent",
     [H["l506"], H["l507"], SC, "GT::GT-Q19-METASTABLE-FREE-REFERENCE"], "interpretive",
     [], ["C::passage-and-persistence", "P::FA-02", "P::SYN-C008"], ["GT-P009 (E5A) has since run: GT-F74 to GT-F82 bear on GT-Q19."]),
    ("EXT-C08", "§7", "SC-026 offers a particularly sharp measurement distinction",
     ["SC-026 (pure versus ready readout, 50/50 against 0–1/50)"], None,
     [SC], "observed",
     [], ["C::clock-readout-dependence"], ["SC is catalogued only; the numbers are checkable in the SC document but were not checked here."]),
    ("EXT-C09", "§6", "The concrete result is **qualitative support versus quantitative measure**.",
     ["CL Generation 2 census (hard count gates open new supports; soft weights do not)", "GT E2–E3 one-way release under hard path-formation exclusion; witness-hitting-set recovery bound"], "Strong finite-grammar distinction",
     ["GT::GT-F51-ONE-WAY-RELEASE-MODE", "GT::GT-F54-HARD-BAN-END-OF-SOFT-LADDER", "GT::GT-F55-PERSISTENT-ABSENCE-TWO-MECHANISMS"], "observed",
     ["CL Generation 2 census: no Generation 2 finding exists in the pinned CL ledger (generations 001, 003C, … 008N); cited at report level only", "GT witness-hitting-set recovery bound: a GT formal-note theorem, not a ledger finding"],
     ["C::admissibility-vs-weighting", "X::0006"], []),
    ("EXT-C10", "§8", "**Event order versus time spent:** the Gravity/Time branch distinguishes jump/event and continuous-time occupancy.",
     ["GT clocks; PCOMP uniform in continuous time, sorted per event"], None,
     ["GT::GT-F69-CLOCK-SEPARATED-SORTING", "GT::GT-F30-ARROW-BELONGS-TO-RATIO"], "observed",
     [], ["C::clock-readout-dependence", "X::0003", "P::SYN-C003"], []),
    ("EXT-C11", "§8", "**Mean versus distribution:** historical Work 45 provided a valid closed mean recurrence; Work 46 showed that this was not a closed law for precision; Work 47 repaired a particular total-variance criterion under fixed schedule assumptions.",
     ["Historical Work 45, 46, 47"], None,
     [H["w46"], H["w47"]], "observed",
     ["Historical Work 45: no primary path listed in the synthesis"], [], []),
    ("EXT-C12", "§8", "**Actual structure versus readout:** the Stochastic Calculator shows how “ready” and “pure” observers can disagree without a corresponding loss of identity.",
     ["Stochastic Calculator observers"], None,
     [SC], "observed",
     [], ["C::clock-readout-dependence"], ["SC is catalogued only; not checked here."]),
    ("EXT-C13", "§9", "507: no simple universal order-scaling law, slow-formation-implies-long-persistence law, staged directional-backbone-then-diffuse-repair cascade, single scalar persistence parameter or universal viability corridor.",
     ["507 negatives"], None,
     [H["l507"], H["n507"]], "observed",
     [], [], ["A negative result; preserved as such."]),
    ("EXT-C14", "§9", "CL 8H: a history register may affect present transitions even after **initial** history has been forgotten; current-history efficacy is not retention of the starting register.",
     ["CL 8H"], None,
     ["CL::F8H-CURRENT-VS-INITIAL-MEMORY", "CL::F018-LOCAL-VERSUS-INITIAL"], "observed",
     [], ["P::FA-05", "X::0007", "C::retention-vs-current-dependence"], []),
    ("EXT-C15", "§9", "CL 8M: **all 24 history-only ANY cells** show zero stationary material–older-history conditional information under the reported conditioning, yet temporal word differences persist",
     ["CL 8M"], None,
     ["CL::F8M-H2-STATIONARY-DEPENDENCE", "CL::F8M-HISTORY-ONLY-STRUCTURAL-SILENCE", "CL::F8M-H2-STATIONARY-H1-RESIDUAL"], "observed",
     [], ["C::occupancy-vs-process"], []),
    ("EXT-C16", "§9", "GT E4/P008: raw gathering largely disappears after density standardisation; held source topology is not an emergent object; local witness floors do not by themselves determine the sign of total attachment bias.",
     ["GT E4, GT-P008"], None,
     ["GT::GT-F62-NATIVE-GATHERING-IS-DENSITY-COMPOSITION", "GT::GT-F70-MARGIN-NOT-FIRST-ORDER", "GT::GT-F72-NO-LABELLED-CENTRE-AT-FINITE-N"], "observed",
     [], ["P::SYN-C007", "P::FA-01"], []),
    ("EXT-C17", "§9", "Stochastic Calculator: successful numerical invariants are **programmed constraints**; the apparatus has not generated an RS-specific explanatory advantage beyond ordinary probability and computer science.",
     ["Stochastic Calculator"], None,
     [SC], "interpretive",
     [], [], ["SC is catalogued only; not checked here. A negative assessment; preserved as such."]),
    ("EXT-C18", "§9", "Proposed 508A/B results, visible only through prior-conversation summaries rather than this archive's primary execution records, did **not** produce a credible quantum-interference mechanism",
     ["508A/B (prior-conversation summaries; secondary-unverified by the synthesis's own account)"], None,
     [H["l507"]], "observed",
     ["508A/B primary execution records: not in the archive by the synthesis's own account"], ["C::physical-attraction"], ["The synthesis itself labels this secondary and unverified."]),
    ("EXT-C19", "§10", "The above results support a provisional **three-axis research map**, not a new ontology",
     ["Axis A admissibility and support; Axis B predictive sufficiency and history; Axis C persistence and operational consequence"], None,
     ["C::admissibility-vs-weighting", "C::predictive-sufficiency", "C::passage-and-persistence"], "interpretive",
     [], ["XQ::07"], ["An interpretive map; the synthesis states the axes do not provably collapse to one primitive."]),
    ("EXT-C20", "§10", "A useful formal target is the following **research proposal**, not an experimentally established RS law.",
     ["Prospective equivalence x ~_(U,H,O,ε) y over a declared future-intervention family, horizon, readout class and fidelity"], None,
     ["C::predictive-sufficiency", "CL::CL-T59"], "formal",
     [], ["XQ::07"], ["A definition proposal, not a result. The synthesis notes it is an equivalence only in some regimes (e.g. ε=0)."]),
    ("EXT-C21", "§0", "No branch establishes a fundamental physical substrate; no emergent metric, displacement, acceleration, gravitational clock law, Born rule or Bell-compatible correlation model has been demonstrated.",
     ["All branches"], None,
     ["GT::GT-Q15-DISPLACEMENT-DEFINITION-GAP", "GT::GT-F72-NO-LABELLED-CENTRE-AT-FINITE-N", "C::physical-attraction"], "interpretive",
     [], ["P::FA-01"], ["A negative claim; consistent with the shared layer's physical-overreach guard."]),
    ("EXT-C22", "§7", "That is an exceptionally useful direct test of the historical identity language, but it has not yet produced the requisite evidence.",
     ["GT-P009 FREE persistence (planned at the time)"], None,
     ["GT::GT-Q19-METASTABLE-FREE-REFERENCE", "GT::GT-F74-INTACT-MOTIFS-NO-CT-PERSISTENCE", "GT::GT-F76-FLEXIBLE-ORGANISATION-OUTLIVES-ND-QUALIFIED", "GT::GT-F78-LIFETIME-NOT-SET-BY-STATIONARY-LAW"], "interpretive",
     [], ["XQ::04", "P::SYN-C008"], ["Superseded in context: GT-P009 (E5A) has since run at 79fa6b0, after the synthesis. Its results are closed but unreviewed (GT-P009 is in unreviewed_generations)."]),
]


def build(root: Path = ROOT) -> list[dict]:
    text = (root / DOC).read_text(encoding="utf-8")
    out = []
    for cid, section, quote, cited, assessment, refs, basis, unresolved, overlaps, notes in CLAIMS:
        if quote not in text:
            raise SystemExit(f"{cid}: quote not found verbatim in {DOC}")
        blocked = any(r.startswith("HIST::") for r in refs)
        dc = "blocked_missing_source" if blocked else "candidate"
        out.append({
            "kind": "external_claim",
            "proposal_id": f"P::{cid}",
            "origin": "external_synthesis",
            "provenance_ref": f"{PROV}#{section}",
            "section": section,
            "quote": quote,
            "cited_as": cited,
            "synthesis_assessment": assessment,
            "sources": refs,
            "source_mapping": "agent",
            "unresolved_citations": unresolved,
            "overlaps": overlaps,
            "context_notes": notes + [SYN_PINS],
            "connection_type": None,
            "status": "proposed",
            "decision_category": dc,
            "epistemic_basis": basis,
            "counterevidence_refs": [],
            "decision_history": [{"date": DATE, "actor": "agent: Claude Opus 5.5 (registration)", "human": False, "status": "proposed", "decision_category": dc,
                                  "rationale": "Registered from the external synthesis; cited items mapped to pinned ids by the agent; unreviewed" + ("; rests on private historical archives (unavailable)" if blocked else "")}],
        })
    return out


def write(root: Path = ROOT) -> int:
    path = root / "proposals" / "candidate-relations.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    keep = [r for r in rows if r.get("origin") != "external_synthesis"]
    new = build(root)
    path.write_text("".join(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n" for r in keep + new), encoding="utf-8")
    return len(new)


if __name__ == "__main__":
    print(f"registered {write(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT)} external claims")
