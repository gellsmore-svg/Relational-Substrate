"""Implicit human acceptance through the research round trip.

The author's rule: acceptance is implicit in the round trip. A round ends with a report and a
round-trip record listing what the agent reviewed and recommends. The author's next instruction
ratifies that list, except for any item the author objects to. Ratification is a human decision:
it is appended to proposals/author-decisions.jsonl and to each record's decision history.

Ratification accepts a recommendation as it was reported and never upgrades it:
- the accepted decision category is the one recorded in the round trip;
- the unreviewed-round cap, the pending-source rule and the HIST-intake rule still apply;
- a round trip lists only agent-reviewed records, so unreviewed proposals, seeds and external
  claims are never accepted this way.

Round-trip records (proposals/round-trips/RT-*.json) are immutable once written.
"""

from __future__ import annotations

import json
from pathlib import Path

from . import core

AUTHOR_IMPLICIT = "author (repository owner): implicit acceptance through the round trip"
KIND = "implicit_round_trip_acceptance"


def rt_dir(root: Path) -> Path:
    return root / "proposals" / "round-trips"


def decisions_path(root: Path) -> Path:
    return root / "proposals" / "author-decisions.jsonl"


def load_round_trips(root: Path) -> dict[str, dict]:
    d = rt_dir(root)
    return {p.stem: core.read_json(p) for p in sorted(d.glob("RT-*.json"))} if d.exists() else {}


def load_decisions(root: Path) -> list[dict]:
    p = decisions_path(root)
    return core.read_jsonl(p) if p.exists() else []


def _targets(root: Path) -> list[dict]:
    """Everything currently agent-reviewed and not yet accepted: the agent's open recommendations."""
    out = []
    for x in core.read_jsonl(root / "ledger" / "connections.jsonl"):
        if x.get("review_status") == "agent_reviewed":
            out.append({"target": x["connection_id"], "kind": "connection", "decision_category": x["decision_category"]})
    for x in core.read_jsonl(root / "proposals" / "candidate-relations.jsonl"):
        if x.get("status") == "agent_reviewed":
            out.append({"target": x["proposal_id"], "kind": "proposal", "decision_category": x["decision_category"]})
    for m in core.read_jsonl(root / "ledger" / "metaphors.jsonl"):
        if m.get("status") == "agent_reviewed":
            out.append({"target": m["metaphor_id"], "kind": "metaphor", "decision_category": None})
    return out


def open_round_trip(rt_id: str, date: str, report: str, reported_at: str, note: str = "", root: Path | None = None) -> dict:
    root = root or core.ROOT
    if not rt_id.startswith("RT-") or "/" in rt_id:
        raise ValueError("a round-trip id looks like RT-0001")
    path = rt_dir(root) / f"{rt_id}.json"
    if path.exists():
        raise FileExistsError(f"{rt_id} exists; round-trip records are immutable")
    if not (root.parent / report).exists() and not (root / report).exists():
        raise FileNotFoundError(f"report {report} not found")
    rec = {"round_trip_id": rt_id, "date": date, "report": report, "reported_at_commit": reported_at,
           "note": note, "recommendations": _targets(root)}
    core.write_json(path, rec)
    return rec


def ratify(rt_id: str, decision_id: str, date: str, instruction: str, objections: list[str] | None = None, root: Path | None = None) -> dict:
    """Apply the author's implicit acceptance of a round trip (idempotent per decision id)."""
    root = root or core.ROOT
    rts = load_round_trips(root)
    if rt_id not in rts:
        raise KeyError(f"no round trip {rt_id}")
    log = load_decisions(root)
    if any(d.get("round_trip") == rt_id and d.get("kind") == KIND for d in log if d["decision_id"] != decision_id):
        raise ValueError(f"{rt_id} is already ratified")
    objections = sorted(set(objections or []))
    recs = rts[rt_id]["recommendations"]
    unknown = set(objections) - {r["target"] for r in recs}
    if unknown:
        raise ValueError(f"objections name items not in {rt_id}: {sorted(unknown)}")
    accepted = [r["target"] for r in recs if r["target"] not in objections]
    if not any(d["decision_id"] == decision_id for d in log):
        entry = {"decision_id": decision_id, "date": date, "kind": KIND, "round_trip": rt_id, "instruction": instruction,
                 "accepted": accepted, "objected": objections, "decided_by": AUTHOR_IMPLICIT, "human": True,
                 "note": "Acceptance is implicit in the round trip (author's rule). Each item is accepted at the decision category the agent reported; nothing is upgraded."}
        with decisions_path(root).open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, sort_keys=True, ensure_ascii=False) + "\n")
    rec_path = f"proposals/reviews/{decision_id}.md"
    core.write_text(root / rec_path, _review_record(decision_id, date, rt_id, instruction, accepted, objections, rts[rt_id]))
    by = {r["target"]: r for r in recs}
    applied = {"connection": 0, "proposal": 0, "metaphor": 0}

    def _apply(rows: list[dict], key: str, status_field: str, kind: str) -> list[dict]:
        for x in rows:
            t = x.get(key)
            if t not in by or any(h.get("decision_id") == decision_id for h in x.get("decision_history", [])):
                continue
            if t in objections:
                st, dc, why = "under_review", x["decision_category"], f"The author objected to this item in round trip {rt_id} ({decision_id}); reopened."
            else:
                st, dc, why = "human_accepted", by[t]["decision_category"], f"Accepted implicitly through round trip {rt_id} ({decision_id}) at the reported decision category."
            x["decision_history"] = list(x.get("decision_history", [])) + [{"date": date, "actor": AUTHOR_IMPLICIT, "human": True, "status": st, "decision_category": dc, "decision_id": decision_id, "round_trip": rt_id, "basis": KIND, "rationale": why}]
            x[status_field] = st
            x["decision_category"] = dc
            if st == "human_accepted":
                x["review"] = {"reviewer": AUTHOR_IMPLICIT, "date": date, "record": rec_path, "human": True, "decision_id": decision_id}
            applied[kind] += 1
        return rows

    for rel, key, sf, kind in (("ledger/connections.jsonl", "connection_id", "review_status", "connection"),
                               ("proposals/candidate-relations.jsonl", "proposal_id", "status", "proposal")):
        p = root / rel
        core.write_jsonl(p, _apply(core.read_jsonl(p), key, sf, kind))
    mp = root / "ledger" / "metaphors.jsonl"
    ms = core.read_jsonl(mp)
    for m in ms:
        t = m.get("metaphor_id")
        if t in by and t not in objections and m.get("status") == "agent_reviewed":
            m["status"] = "human_accepted"
            m["review"] = dict(m.get("review", {}), human_reviewed=True, accepted_by=AUTHOR_IMPLICIT, decision_id=decision_id, round_trip=rt_id, date=date)
            applied["metaphor"] += 1
    core.write_jsonl(mp, ms)
    return {"decision_id": decision_id, "round_trip": rt_id, "accepted": len(accepted), "objected": objections, "applied": applied}


def _review_record(did: str, date: str, rt_id: str, instruction: str, accepted: list[str], objected: list[str], rt: dict) -> str:
    cats = {r["target"]: r["decision_category"] for r in rt["recommendations"]}
    lines = [f"# Review record {did}: implicit acceptance through round trip {rt_id}", "",
             f"- **Decided by:** {AUTHOR_IMPLICIT}", "- **Human:** True", f"- **Date:** {date}",
             f"- **Round trip:** `proposals/round-trips/{rt_id}.json` (report `{rt['report']}`, reported at `{rt['reported_at_commit'][:12]}`)",
             f"- **Author instruction that closed the round trip:** \"{instruction}\"", "",
             "Each item below is accepted at the decision category the agent reported. Nothing is upgraded: the unreviewed-round cap, the pending-source rule and the HIST-intake rule still apply.", "",
             "| Item | Decision category | Outcome |", "| --- | --- | --- |"]
    lines += [f"| `{t}` | {cats[t] or '— (metaphor, non-evidentiary)'} | accepted |" for t in accepted]
    lines += [f"| `{t}` | {cats[t] or '—'} | objected (reopened) |" for t in objected]
    return "\n".join(lines) + "\n"


def validate(root: Path, shared: dict) -> list[str]:
    """Implicit acceptances must trace to a logged ratification of a round trip that listed the item."""
    p = []
    rts = load_round_trips(root)
    log = load_decisions(root)
    ids = [d.get("decision_id") for d in log]
    if len(ids) != len(set(ids)):
        p.append("author-decisions: duplicate decision_id")
    rat = {d["decision_id"]: d for d in log if d.get("kind") == KIND}
    seen_rt = {}
    for did, d in rat.items():
        if not d.get("human"):
            p.append(f"{did}: a round-trip ratification is a human decision")
        rt = rts.get(d.get("round_trip"))
        if rt is None:
            p.append(f"{did}: round trip {d.get('round_trip')} does not exist")
            continue
        if d["round_trip"] in seen_rt:
            p.append(f"{did}: round trip {d['round_trip']} is ratified twice ({seen_rt[d['round_trip']]})")
        seen_rt[d["round_trip"]] = did
        listed = {r["target"] for r in rt["recommendations"]}
        if set(d.get("accepted", [])) | set(d.get("objected", [])) != listed or set(d.get("accepted", [])) & set(d.get("objected", [])):
            p.append(f"{did}: accepted and objected items must partition the items listed in {d['round_trip']}")
    for rt_id, rt in rts.items():
        if rt.get("round_trip_id") != rt_id:
            p.append(f"{rt_id}: round_trip_id does not match the file name")
    cats = {}
    for did, d in rat.items():
        rt = rts.get(d.get("round_trip"), {})
        for r in rt.get("recommendations", []):
            if r["target"] in d.get("accepted", []):
                cats[(did, r["target"])] = r["decision_category"]

    def _check(x: dict, key: str, status_field: str) -> None:
        for h in x.get("decision_history", []):
            if h.get("basis") != KIND:
                continue
            did, t = h.get("decision_id"), x.get(key)
            if did not in rat:
                p.append(f"{t}: cites {did}, which is not a logged round-trip ratification")
            elif h.get("status") == "human_accepted":
                if (did, t) not in cats:
                    p.append(f"{t}: {did} did not accept it (not listed in {rat[did]['round_trip']}, or objected)")
                elif h.get("decision_category") != cats[(did, t)]:
                    p.append(f"{t}: implicit acceptance changed the decision category ({cats[(did, t)]} -> {h.get('decision_category')}); ratification never upgrades")

    for x in shared["connections"]:
        _check(x, "connection_id", "review_status")
    for x in shared["proposals"]:
        _check(x, "proposal_id", "status")
    for m in shared["metaphors"]:
        rv = m.get("review", {})
        if m.get("status") == "human_accepted" and rv.get("decision_id") in rat and (rv["decision_id"], m["metaphor_id"]) not in cats:
            p.append(f"{m['metaphor_id']}: {rv['decision_id']} did not accept it")
        if m.get("status") == "human_accepted" and not rv.get("human_reviewed"):
            p.append(f"{m['metaphor_id']}: human_accepted needs review.human_reviewed")
    return p


def open_round_trips(root: Path) -> list[str]:
    ratified = {d.get("round_trip") for d in load_decisions(root) if d.get("kind") == KIND}
    return sorted(set(load_round_trips(root)) - ratified)
