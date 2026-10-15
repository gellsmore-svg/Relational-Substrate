"""Record the author's decisions and apply them to proposals (append-only, idempotent).

Each decision is a human decision by the programme author, relayed in a session.
- It is appended to proposals/author-decisions.jsonl (the log is never rewritten).
- It is applied to the named proposal as an appended decision-history entry (human: true)
  plus any declared field changes.
- A seed's verbatim seed_record is never changed.

Usage: python3 research-synthesis/proposals/author_decisions.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTHOR = "author (repository owner), decision relayed in a Claude Code session"

DECISIONS = [
    {
        "decision_id": "AD-0001",
        "date": "2026-10-15",
        "target": "P::SYN-C003",
        "kind": "relation_type",
        "instruction": "make SYN-C003 an explicit contrast, matching X::0003",
        "relation_override": {
            "from": "compatible_with",
            "to": "explicit_contrast",
            "matches": "X::0003",
            "rationale": "Author decision: the clock dependence in CL and GT is an explicit contrast of operations, as recorded in X::0003. CL's pair-event epoch hides triad events (a time change plus a projection); GT's continuous and jump clocks share one event sequence and differ only in holding-time weighting. The seed's compatibility reading survives as theme membership (C::clock-readout-dependence), not as the relation type.",
        },
        "status": "under_review",
        "decision_category": "candidate",
        "note": "The relation type is decided. The claim itself is not accepted, and X::0003 is not human-accepted by this decision.",
    },
]


def _vector(d: dict) -> dict:
    ov = d["relation_override"]
    return {
        "semantic_resemblance": {"assessment": "not used: decided on the formal operations"},
        "formal_comparability": {"assessment": "clock operations differ: epoch subsequence plus projection (CL) versus continuous time against the embedded jump chain (GT); see X::0003"},
        "observable_comparability": {"assessment": "both report clock-dependent conclusions; GT clock effects cannot create apparent memory, CL's epoch can"},
        "scope_compatibility": {"assessment": "CL Generation 3C (N=3); GT E0A and GT-P008 (N=5 and above)"},
        "evidence_status": {"assessment": "the definitions of the operations in both programmes", "status": "mixed"},
        "independence": {"assessment": "shared 8G lineage of the DSL; the contrast is between operations, not computed numbers"},
        "counterexamples_or_nulls": {"assessment": "none known"},
        "falsifiability": {"assessment": "a GT case where switching clocks alone changes Markov order would undo the contrast (impossible under the embedded-chain construction)"},
        "research_relevance": {"assessment": f"settles the seed/agent disagreement in favour of {ov['to']} (author decision {d['decision_id']})"},
    }


def run(root: Path = ROOT) -> dict:
    log_path = root / "proposals" / "author-decisions.jsonl"
    log = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines() if line.strip()] if log_path.exists() else []
    logged = {e["decision_id"] for e in log}
    new_log = [d for d in DECISIONS if d["decision_id"] not in logged]
    if new_log:
        with log_path.open("a", encoding="utf-8") as f:
            for d in new_log:
                f.write(json.dumps({**d, "decided_by": AUTHOR, "human": True}, sort_keys=True, ensure_ascii=False) + "\n")
    path = root / "proposals" / "candidate-relations.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    applied = 0
    for d in DECISIONS:
        for r in rows:
            if r.get("proposal_id") != d["target"]:
                continue
            if any(h.get("decision_id") == d["decision_id"] for h in r.get("decision_history", [])):
                continue
            ov = dict(d["relation_override"], decided_by=AUTHOR, human=True, date=d["date"], decision_id=d["decision_id"])
            r["relation_override"] = ov
            r["connection_type"] = ov["to"]
            r["status"] = d["status"]
            r["decision_category"] = d["decision_category"]
            r.setdefault("review_vector", _vector(d))
            r["decision_history"] = list(r.get("decision_history", [])) + [{"date": d["date"], "actor": AUTHOR, "human": True, "status": d["status"], "decision_category": d["decision_category"], "decision_id": d["decision_id"], "rationale": f"{ov['rationale']} {d['note']}"}]
            applied += 1
    path.write_text("".join(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    return {"logged": len(new_log), "applied": applied}


if __name__ == "__main__":
    print(run(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT))
