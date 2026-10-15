"""Append forward-looking policy amendments to the author-decision log (append-only, idempotent).

Earlier decisions are never rewritten. An amendment changes how later round trips are handled and
records any audit note about earlier ones.

Usage: python3 research-synthesis/proposals/policy_amendments.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

AMENDMENTS = [
    {
        "decision_id": "AD-0004",
        "date": "2026-10-15",
        "kind": "policy_amendment",
        "human": True,
        "decided_by": "author (repository owner): operational close-out instruction of 2026-10-15, stage 6; applied by the agent",
        "instruction": "Make each round's recommendation list explicit in its published closure report, with scope, qualification and objections. A next task instruction should not indiscriminately accept unexamined claims. If policy change is needed, make it forward-looking with an append-only corrective note.",
        "rules": [
            "round-close records each recommendation with its scope, qualification and whether it rests on an unreviewed round",
            "generated/round-trips.md displays every open recommendation; ratification refuses any item that the round trip's closing commit did not display",
            "three acceptances stay separate: synthesis interpretation (round trip); scientific review of a CL/GT generation (never through the round trip); consent to publish private historical material (an explicit publication_consent decision only)",
        ],
        "grandfathered": ["RT-0001", "RT-0002"],
        "audit_note": "RT-0001 was opened retrospectively at the moment the implicit-acceptance rule was introduced and ratified in the same session (AD-0002). Its 15 items had been shown to the author only in prose (reports/2026-10-15-initial-federation.md, the PR #8 description and the generated links and metaphor views), not as a structured list before the instruction that ratified them. AD-0002 stands and is not rewritten; it accepted synthesis interpretations at their reported categories only. It is not scientific review of CL 008N or GT-P009 and not publication consent. RT-0002 listed no items.",
    },
    {
        "decision_id": "AD-0006",
        "date": "2026-10-16",
        "kind": "standing_pin_adoption",
        "human": True,
        "decided_by": "author (repository owner): instruction of 2026-10-16 after the GT-P012 report; applied by the agent",
        "instruction": "skip the central approval steps and integrate automatically",
        "rules": [
            "a milestone pin proposal is adopted without a per-pin named review (synth apply-pin --standing-decision AD-0006) when it descends from the current pin and carries no warnings (no rows removed or rewritten in place)",
            "a proposal with any warning (non-descent, removed or rewritten rows) still needs a named human reviewer",
            "adoption still runs the full sequence: pin, generate, check twice for byte identity, tests; staged candidates are appended and re-validated; snapshot and round-close follow, and the hub milestone branch is merged once CI is green",
            "the adoption record says that no line-by-line review took place; nobody's name is entered as reviewer",
            "this is not scientific review of any pinned generation (they stay listed in unreviewed_generations), not acceptance of any candidate connection, and not consent to publish private historical material",
        ],
        "note": "Forward-looking. Earlier pins and decisions are unchanged.",
    },
]


def run(root: Path = ROOT) -> dict:
    path = root / "proposals" / "author-decisions.jsonl"
    logged = {json.loads(line)["decision_id"] for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}
    new = [a for a in AMENDMENTS if a["decision_id"] not in logged]
    with path.open("a", encoding="utf-8") as f:
        for a in new:
            f.write(json.dumps(a, sort_keys=True, ensure_ascii=False) + "\n")
    return {"logged": len(new)}


if __name__ == "__main__":
    print(run(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT))
