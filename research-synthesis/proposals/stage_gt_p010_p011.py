"""Stage agent-drafted cross-programme candidates from GT-P010 and GT-P011 (not yet in the live registry).

They cite GT findings that exist only at the proposed GT pin a81c505 (not yet adopted). They are
written to proposals/staged/ and must be appended to proposals/candidate-relations.jsonl only
after a named human adopts that pin (synth apply-pin). Nothing here is reviewed or accepted.

Usage: python3 research-synthesis/proposals/stage_gt_p010_p011.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTOR = "agent: Claude Opus 5.5 (session of 2026-10-15)"
DIMS = ("state", "transition_law", "support", "clock", "projection", "intervention", "horizon", "conditioning")


def comparison(**v):
    return {d: {"verdict": v[d][0], "note": v[d][1]} for d in DIMS}


def cand(pid, frm, to, ctype, basis, scope, rationale, comp, falsifiers, alternatives, source):
    return {
        "alternatives": alternatives, "comparison": comp, "connection_type": ctype,
        "controls": {"negative": [], "positive": []}, "counterevidence_refs": [], "decision_category": "candidate",
        "decision_history": [{"actor": ACTOR, "date": "2026-10-15", "decision_category": "candidate", "human": False, "rationale": f"Agent draft from {source}; unreviewed; staged pending GT pin adoption", "status": "proposed"}],
        "epistemic_basis": basis, "evidence_refs": [], "falsifiers": falsifiers, "from": frm,
        "independence": "shared_lineage", "independence_note": "GT and CL both descend from CL 8G (22e252e) and share the constraint DSL, kernel builder and coherence validator lineage; agreement is not independent evidence.",
        "origin": "agent_drafted", "proposal_id": pid, "rationale": rationale, "scope": scope, "staged_pending": {"requires_gt_pin": "a81c505a08ac5c4c83359234915bec65bb1f60c3", "source_handoff": source}, "status": "proposed", "to": to,
    }


ROWS = [
    cand("P::GT-C1", "GT::GT-F88-NK-LAYER-TRAFFIC-COMPARATOR", "CL::F8N-H1-MATCHED-PASSAGE-BOUNDARY", "untested_hypothesis", "formal",
         "Single-toggle finite chains; projection onto a count (GT) versus onto (P,h1) (CL)",
         "GT's NK is the stationary-conditional kernel on the edge-count projection, lifted uniformly within layers; CL's Kpi is the stationary-conditional kernel on (P,h1) and is the unique first-order kernel matching the adjacent joint there (CL-T89). NK may be the analogous unique lift on K.",
         comparison(state=("differs", "FREE graph vs (P,h1,h2)"), transition_law=("differs", "W4 templates vs 8M controllers"), support=("differs", "full hypercube vs recurrent augmented class"), clock=("differs", "CT vs pair-event epochs"), projection=("differs", "edge count k vs (P,h1); analogous role"), intervention=("not_applicable", "kernel comparison"), horizon=("differs", "entrance episodes vs first return/MFPT"), conditioning=("same", "stationary-conditional rates on the projection")),
         ["Among first-order CT kernels on K lifted uniformly, NK is not the unique one matching the stationary adjacent-layer flux"],
         ["The analogy may hold only at the level of 'stationary conditioning', with no uniqueness counterpart in CT"], "gravity-time/docs/gt-p010-shared-synthesis-handoff.md (C-1)"),
    cand("P::GT-C2", "GT::GT-F83-PCOMP-PERSISTENCE-IS-BETWEEN-LAYER-TRAFFIC", "CL::F8N-MFPT-RESIDUAL", "explicit_contrast", "observed",
         "GT FREE N=5,6 PCOMP vertex predicates; CL 8N non-neutral H2 systems",
         "Matching the adjacent joint on the projection removes PCOMP's apparent lifetime excess in GT (NK), whereas in CL Kpi matches the full stationary adjacent joint on (P,h1) yet sibling MFPTs still differ (446 slower, 274 faster): the projections discard different information (within-layer arrangement in GT; a routing-carrying history coordinate in CL).",
         comparison(state=("differs", "graph vs augmented history state"), transition_law=("differs", "PCOMP W4 vs 8M H2"), support=("differs", "full vs recurrent class"), clock=("differs", "CT/JT/local vs epochs"), projection=("differs", "k vs (P,h1)"), intervention=("not_applicable", "comparison of kernels"), horizon=("differs", "entrance episode vs MFPT"), conditioning=("same", "stationary-conditional matched comparator")),
         ["A GT family whose lifetime residual against NK equals its residual against ND", "A CL system in which Kpi removes every passage residual"],
         ["GT residuals do survive NK for PATHF, PATHH and CSPH: the contrast is family-specific"], "gravity-time/docs/gt-p010-shared-synthesis-handoff.md (C-2)"),
    cand("P::GT-C3", "GT::GT-F97-FIRST-HIT-SAMPLING-MATTERS", "CL::F8N-MATCHED-SOURCE-PASSAGE", "epistemic_compatibility", "methodological",
         "Post-event functionals in both programmes",
         "Both programmes condition post-event functionals on an explicit source law: CL on stationary class-conditioned sources (CL-T85), GT on the exact first-hit law at renewal (T12); in GT the first-hit law differs from the stationary restriction by L1 0.3-1.7.",
         comparison(state=("differs", ""), transition_law=("differs", ""), support=("differs", ""), clock=("differs", "epochs vs anchor-local counts"), projection=("differs", ""), intervention=("not_applicable", ""), horizon=("differs", "first return vs post-renewal survival"), conditioning=("same", "explicit source law")),
         ["A CL post-event functional invariant to replacing its source law"],
         ["The compatibility is methodological only; no shared quantity"], "gravity-time/docs/gt-p011-shared-synthesis-handoff.md (C-3)"),
]


def run(root: Path = ROOT) -> dict:
    out = root / "proposals" / "staged" / "2026-10-15-gt-p010-p011-candidates.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n" for r in ROWS), encoding="utf-8")
    return {"staged": len(ROWS), "path": str(out.relative_to(root))}


if __name__ == "__main__":
    print(run())
