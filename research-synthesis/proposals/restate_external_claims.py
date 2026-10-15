"""Restate the checkable claims of the external synthesis as pairwise proposals (2026-10-15).

For each external claim not blocked on historical archives:
- **Check it** against the pinned records, and record the outcome: verified,
  partially_verified, consistent, superseded_context or not_restatable. This becomes an
  appended `under_review` decision-history entry, never a rewrite.
- **Cross-programme pairs** become ordinary pairwise proposals (`origin: agent_restatement`).
- **Within-programme pairs** are recorded as upstream suggestions (`within_programme: true`),
  which the validator never lets into the shared ledger. They belong to the programme's own
  ledger.
- **Existing upstream relations** are cited instead of duplicated.
- **Single-source or purely interpretive claims** are not restated, and the reason is recorded.

Idempotent: proposals that already exist are not recreated, and a claim already carrying
this restatement's history entry is not appended again.

Usage: python3 research-synthesis/proposals/restate_external_claims.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-10-15"
ACTOR = "agent: Claude Opus 5.5 (restatement check)"
PINS = {"CL": "e650d71bda7203c8018d8bd134c5496a03d74a11", "GT": "79fa6b0119449bd56359acf4436015df27855f43", "SC": "aa06213ce42e5166ae2a0d21846a2a7c218f6b50"}
SC_DOC = "SC::stochastic-calculator/RS_FINDINGS.md"

# claim -> (outcome, decision category, check note, upstream relations cited, restatement proposal ids, review-vector evidence status)
CHECKS = {
    "EXT-C02": ("verified", "candidate", "CL F8M-STRICT-H2-ROLE-ATLAS states all 72 non-neutral one-role cells fail strong projection; F8M-STATIONARY-H1-MATCHING states Kpi-H1 matches one/two-time (P,h1) and material one/two/three-time laws; F8M-H2-STATIONARY-H1-RESIDUAL states first differences at length four. Within CL; already related upstream. Cross-programme analogue: X::0001.", ["CL::R8M-011 (bounds)"], [], "numerical_exact"),
    "EXT-C05": ("verified", "candidate", "GT-F69 (equal-ratio pairs share the continuous law to first order) and GT-F71 (post hoc: PATHF sorts only through formation, PATHH only through lifetime). Contained in two GT records; no relation needed.", [], [], "post_hoc_exploratory"),
    "EXT-C06": ("verified", "candidate", "GT-F71 gives the continuous sign in 16/16 within-reference contrasts, post hoc; GT-F68 exhibits first-order reversal shapes (7 strict reversals); GT-Q18 (full-strength test) is open. No upstream relation between GT-F68 and GT-F71.", [], ["P::EXT-C06-U1"], "mixed"),
    "EXT-C08": ("verified", "candidate", "SC RS_FINDINGS.md at aa06213 (SC-026): pure readout correct in 50/50 at 500/2,000/8,000 proposals; ready readout correct in 0/50, 1/50, 1/50. SC is catalogued only, so this is a document-level check.", [], ["P::EXT-C08-R1"], "qualitative_report"),
    "EXT-C09": ("partially_verified", "qualified", "GT part verified: GT-F51 (one-way release only under hard path-formation exclusion) and GT-F54 (soft ladder continuous to the hard ban), related upstream by GT-R86. CL part unresolved: no Generation 2 finding in the pinned CL ledger. Cross-programme restatement uses CL-T01 (zero outside the log algebra) instead.", ["GT::GT-R86 (supersedes_interpretation)"], ["P::EXT-C09-R1"], "mixed"),
    "EXT-C10": ("verified", "candidate", "GT-F69: PCOMP's continuous law is uniform while its per-event law sorts. GT-F30 (E0B) calls PCOMP 'uniform in every mode', which holds for the continuous-time law; GT-F69 refines it. No upstream relation.", [], ["P::EXT-C10-U1"], "theorem"),
    "EXT-C12": ("verified", "candidate", "SC RS_FINDINGS.md (SC-026/027) reports pure and ready observers disagreeing on the same trajectories. Covered by the same restatement as EXT-C08.", [], ["P::EXT-C08-R1"], "qualitative_report"),
    "EXT-C14": ("verified", "candidate", "CL F8H-CURRENT-VS-INITIAL-MEMORY states current history stays efficacious while initial-slot information decays; already related upstream to F018. See also P::FA-05 and X::0007.", ["CL::R-8H-HISTORY-19 (refines)"], [], "numerical_exact"),
    "EXT-C15": ("verified", "candidate", "CL F8M-H2-STATIONARY-DEPENDENCE: I(P;H2|H1) exactly zero in ANY cells; F8M-HISTORY-ONLY-STRUCTURAL-SILENCE: word comparisons first differ at L4. The count of 24 ANY cells is stated in the CL 8M report (generation-008m-h2-structural-consequence.md), not in the ledger rows.", ["CL::R8M-013 (compatible_with)"], [], "numerical_exact"),
    "EXT-C16": ("verified", "candidate", "GT-F62: raw gathering largely vanishes under null-density standardisation. GT-F67 and GT-F70: the floor is an exact lever with an unsignable residue, and margins change sign with strength. 'Held topology is not emergent' holds by definition (held). No upstream relations between GT-F62 and GT-F61, or between GT-F70 and GT-F67.", [], ["P::EXT-C16-U1", "P::EXT-C16-U2"], "theorem"),
    "EXT-C17": ("consistent", "candidate", "Consistent with SC's own self-assessment in RS_FINDINGS.md ('designed invariant-preserving stochastic rewriting ... no claim of theoretical novelty'). A single-source assessment of SC: not restated pairwise.", [], [], "qualitative_report"),
    "EXT-C19": ("not_restatable", "candidate", "An interpretive map over three shared concepts; there are no source records to pair. Tracked by XQ::07.", [], [], "unknown"),
    "EXT-C20": ("verified", "candidate", "A definition proposal. Restated as an untested formal hypothesis relating it to CL-T59's strong lumpings (see P::EXT-C20-R1, with a proof sketch).", [], ["P::EXT-C20-R1"], "unexecuted_plan"),
    "EXT-C21": ("consistent", "candidate", "Consistent with GT-Q15 (displacement undefined) answered only partly by GT-F72 (upstream GT-R127), and with the shared layer's rejection of P::FA-01. A broad negative claim: not restated pairwise.", ["GT::GT-R127 (partially_answered_by)"], [], "qualitative_report"),
    "EXT-C22": ("superseded_context", "qualified", "Written before E5A. GT-P009 (E5A) has since run: GT-F74 and GT-F76 are already related upstream to GT-Q19 (GT-R128, GT-R129). Those results are closed but unreviewed.", ["GT::GT-R128 (partially_answered_by)", "GT::GT-R129 (partially_answered_by)"], [], "numerical_exact"),
}


def proposal(pid, claim, a, b, ctype, scope, rationale, falsifiers, *, within, comparison=None, alternatives=(), evidence=()):
    return {
        "proposal_id": pid, "from": a, "to": b, "connection_type": ctype, "status": "proposed", "decision_category": "candidate",
        "epistemic_basis": "formal" if ctype in ("untested_hypothesis", "refines") else "observed",
        "scope": scope, "rationale": rationale, "comparison": comparison or {}, "independence": "same_source" if within else "shared_lineage",
        "controls": {"positive": [], "negative": []}, "alternatives": list(alternatives), "falsifiers": list(falsifiers), "evidence_refs": list(evidence), "counterevidence_refs": [],
        "origin": "agent_restatement", "derived_from_claim": f"P::{claim}", "within_programme": within,
        "decision_history": [{"date": DATE, "actor": ACTOR, "human": False, "status": "proposed", "decision_category": "candidate", "rationale": f"Restated from P::{claim} after checking it against pinned records; unreviewed" + ("; within-programme: a suggestion for that programme's own ledger, not promotable here" if within else "")}],
    }


PROPOSALS = [
    proposal("P::EXT-C06-U1", "EXT-C06", "GT::GT-F68-FIRST-ORDER-SORTING-INDEX", "GT::GT-F71-SORTING-DECOMPOSITION-POSTHOC", "qualifies",
             "GT-P008 sorting index", "The first-order reversal shapes of GT-F68 qualify GT-F71's post hoc 16/16 agreement: agreement on published references does not extend to references where the index predicts reversals, which are untested at W4 (GT-Q18).",
             ["A W4 test of the reversal graphs agreeing with the index (would remove the qualification)"], within=True, evidence=["GT::GT-Q18-REVERSAL-AT-W4"]),
    proposal("P::EXT-C08-R1", "EXT-C08", SC_DOC, "C::clock-readout-dependence", "instance_of_theme",
             "SC apparatus (catalogued only), SC-026/027", "SC-026 is an instance of readout dependence: on the same trajectories, pure readout was correct in 50/50 trials, while ready readout was correct in 0/50, 1/50 and 1/50. Also covers EXT-C12 (observers disagreeing without loss of identity).",
             ["SC records showing the two readouts measure different trajectories (would make it a state difference, not a readout difference)"], within=False, alternatives=["The ready criterion may test a different property, not readout of the same one"]),
    proposal("P::EXT-C09-R1", "EXT-C09", "CL::CL-T01", "GT::GT-F51-ONE-WAY-RELEASE-MODE", "epistemic_compatibility",
             "Admissibility versus weighting: CL log-additive algebra (zero excluded) and GT hard path-formation exclusion (FREE N=5)",
             "CL-T01 places the zero weight outside the logarithmic algebra; GT-F51 finds a mode of succession (one-way release) that appears only at the hard ban and at no positive factor (compare GT-F54). Both say hard admissibility is a different kind of constraint from soft weighting. No shared mechanism is asserted.",
             ["A positive-factor GT cell with one-way transitions (impossible with positive rates)", "A CL zero-weight effect reproduced by finite weights in the log algebra"], within=False,
             comparison={"support": {"verdict": "same", "note": "zero removes transitions in both"}}, evidence=["GT::GT-F54-HARD-BAN-END-OF-SOFT-LADDER", "CL::F8D-LOG-ADDITIVITY"]),
    proposal("P::EXT-C10-U1", "EXT-C10", "GT::GT-F69-CLOCK-SEPARATED-SORTING", "GT::GT-F30-ARROW-BELONGS-TO-RATIO", "refines",
             "PCOMP stationary laws", "GT-F69 refines GT-F30's 'uniform in every mode': PCOMP's continuous-time law is uniform at any strength, while its per-event law sorts. 'Uniform' holds for the continuous clock only.",
             ["A PCOMP cell whose per-event law is uniform (contradicts GT-F69 S6)"], within=True),
    proposal("P::EXT-C16-U1", "EXT-C16", "GT::GT-F62-NATIVE-GATHERING-IS-DENSITY-COMPOSITION", "GT::GT-F61-NATIVE-K2-RAW-GATHERING", "qualifies",
             "GT E4A gathering", "GT-F62 qualifies GT-F61: the raw above-null attachment under K2 and the star largely vanishes under null-density standardisation (except CSPH under K2). It overlaps the author seed P::SYN-C007.",
             ["A density-standardised margin that stays positive across families"], within=True),
    proposal("P::EXT-C16-U2", "EXT-C16", "GT::GT-F70-MARGIN-NOT-FIRST-ORDER", "GT::GT-F67-FLOOR-IS-AN-EXACT-ODDS-LEVER", "refines",
             "GT-P008 floor and margins", "GT-F70 refines GT-F67: the floor is an exact odds lever (GT-F67), but total-margin signs change between weak and W4 strength (GT-F70), so the floor alone does not fix the sign of total attachment bias.",
             ["A W4 margin whose sign follows the floor in every reference"], within=True),
    proposal("P::EXT-C20-R1", "EXT-C20", "CL::CL-T59", "C::predictive-sufficiency", "untested_hypothesis",
             "Finite chains; observation block-measurable; epsilon = 0",
             "Hypothesis: a strong lumping whose blocks determine the declared readout refines the synthesis's prospective equivalence at epsilon = 0. States in one block have equal future readout laws at every horizon, so they are equivalent; the converse need not hold. CL-T59's ladders would then be instances. Proof sketch: under strong lumpability the block process is Markov with a block-determined kernel, so Law(o(X_h) | x) depends on x only through its block.",
             ["A strong lumping with a block-measurable readout and two same-block states whose future readout laws differ (contradicts lumpability)", "The synthesis's intervention family U includes interventions that do not respect the blocks"], within=False,
             alternatives=["With non-trivial intervention families U, lumpability must hold for each intervened kernel, which is stronger"]),
]


def run(root: Path = ROOT) -> dict:
    path = root / "proposals" / "candidate-relations.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    have = {r["proposal_id"] for r in rows}
    added = [p for p in PROPOSALS if p["proposal_id"] not in have]
    for p in added:
        if not p["within_programme"]:
            p["reviewed_source_commits"] = {ns: PINS[ns] for ns in PINS if p["from"].startswith(ns + "::") or p["to"].startswith(ns + "::")}
    appended = 0
    for r in rows:
        cid = r.get("proposal_id", "").removeprefix("P::")
        if r.get("kind") != "external_claim" or cid not in CHECKS:
            continue
        if any(h.get("actor") == ACTOR for h in r.get("decision_history", [])):
            continue
        outcome, dc, note, upstream, restated, ev = CHECKS[cid]
        r["check_outcome"] = outcome
        r["check_note"] = note
        r["upstream_relations"] = upstream
        r["restated_as"] = restated
        r["review_vector"] = {
            "semantic_resemblance": {"assessment": "not used: the claim was checked directly against records"},
            "formal_comparability": {"assessment": note},
            "observable_comparability": {"assessment": "see check note"},
            "scope_compatibility": {"assessment": "checked at the current pins (CL e650d71, GT 79fa6b0, SC aa06213)"},
            "evidence_status": {"assessment": f"evidence behind the claim: {ev}", "status": ev},
            "independence": {"assessment": "the synthesis restates programme records; it is not independent evidence"},
            "counterexamples_or_nulls": {"assessment": "none found in the cited records" if outcome in ("verified", "consistent") else outcome.replace("_", " ")},
            "falsifiability": {"assessment": "see restated proposals" if restated else "not restated"},
            "research_relevance": {"assessment": "see overlaps"},
        }
        r["status"] = "under_review"
        r["decision_category"] = dc
        r["decision_history"] = list(r["decision_history"]) + [{"date": DATE, "actor": ACTOR, "human": False, "status": "under_review", "decision_category": dc, "rationale": f"Checked against pinned records: {outcome}. " + (f"Restated as {', '.join(restated)}. " if restated else "") + (f"Upstream relations: {', '.join(upstream)}." if upstream else "")}]
        appended += 1
    path.write_text("".join(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n" for r in rows + added), encoding="utf-8")
    return {"proposals_added": len(added), "claims_checked": appended}


if __name__ == "__main__":
    print(run(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT))
