"""Re-evaluate records blocked on historical sources against the current intake state (append-only, idempotent).

For each proposal whose decision is blocked_missing_source and which cites HIST:: references:
- records the specific missing anchors (`missing_anchors`), each mapped to the intake plan;
- appends one agent decision-history entry per intake plan, keeping the status and the block.

A record is unblocked only by a later intake that registers source-verified, approved HIST:: findings
for every anchor it cites. This script never unblocks anything.

Usage: python3 research-synthesis/proposals/reassess_blocked.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTOR = "agent: Claude Opus 5.5 (session of 2026-10-15)"
DATE = "2026-10-15"


def hist_refs(r: dict) -> list[str]:
    refs = [r.get("from"), r.get("to")] + list(r.get("sources", [])) + list(r.get("evidence_refs", []))
    return sorted({x for x in refs if isinstance(x, str) and x.startswith("HIST::")})


def run(root: Path = ROOT) -> dict:
    plan = json.loads((root / "sources" / "historical" / "intake-plan.json").read_text(encoding="utf-8"))
    landmarks = {lm["path"]: lm for lm in plan["landmarks"]}
    archive_state = {a["name"]: a["state"] for a in plan["archives"]}
    path = root / "proposals" / "candidate-relations.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    touched = 0
    for r in rows:
        refs = hist_refs(r)
        if r.get("decision_category") != "blocked_missing_source" or not refs:
            continue
        if any(h.get("reassessment") == plan["plan_id"] for h in r.get("decision_history", [])):
            continue
        anchors = []
        for ref in refs:
            local = ref.split("::", 1)[1]
            lm = landmarks.get(local)
            is_member = "/" in local or local.endswith(".md")
            anchors.append({"ref": ref, "landmark": bool(lm), "expected_member": local if is_member else None,
                            "state": "archive_inaccessible" if is_member else "no_member_path_named (a range or label; needs mapping to primary reports at intake)"})
        r["missing_anchors"] = anchors
        hist = r.get("decision_history") or []
        last = hist[-1] if hist else {"status": r.get("status")}
        r["decision_history"] = hist + [{
            "date": DATE, "actor": ACTOR, "human": False, "status": last["status"], "decision_category": "blocked_missing_source",
            "reassessment": plan["plan_id"],
            "rationale": "Re-evaluated against the historical intake of 2026-10-15: the archives (" + ", ".join(f"{k}: {v}" for k, v in sorted(archive_state.items())) + ") were not available, so no primary source was read. Still blocked on: " + ", ".join(a["ref"] for a in anchors) + ". Not reconstructed from the external synthesis or model memory.",
        }]
        r["status"] = last["status"]
        touched += 1
    path.write_text("".join(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    return {"reassessed": touched}


if __name__ == "__main__":
    print(run(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT))
