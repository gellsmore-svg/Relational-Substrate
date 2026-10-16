"""Command line: python3 research-synthesis/synth <command> (or PYTHONPATH=research-synthesis python3 -m rssynth)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import core, discover, generate, historical, ledger, pins, preview, roundtrip, smoke, sources, workflow


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="synth", description="Federated research-coherence layer (read-only over programme ledgers).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("audit", help="show pins, branch heads, artifact verification and lineage")
    pn = sub.add_parser("pin", help="rebuild sources/manifest.json and materialised copies from sources/pin-spec.json")
    pn.add_argument("--by", default="agent", help="who records the ingestion receipt")
    sub.add_parser("validate", help="validate manifest, source ledgers (under their pinned vocabularies) and shared records")
    d = sub.add_parser("update-candidates", aliases=["discover"], help="write retrieval diagnostics to proposals/ (never the ledger)")
    d.add_argument("--limit", type=int, default=40)
    sub.add_parser("generate", help="regenerate deterministic views under generated/")
    c = sub.add_parser("check", help="CI check: integrity, validation, staleness, snapshots, scope")
    c.add_argument("--no-git", action="store_true", help="verify materialised copies only")
    c.add_argument("--scope-base", default="origin/main")
    s = sub.add_parser("snapshot", help="write an immutable milestone snapshot")
    s.add_argument("--name", required=True)
    s.add_argument("--title", required=True)
    r = sub.add_parser("review", help="record a decision on a proposal")
    r.add_argument("--id", required=True)
    r.add_argument("--decision", required=True, choices=["agent_reviewed", "human_accepted", "rejected", "undetermined", "under_review"])
    r.add_argument("--reviewer", required=True)
    r.add_argument("--rationale", required=True)
    r.add_argument("--human", action="store_true")
    r.add_argument("--decision-category", choices=sorted(core.DECISION_CATEGORIES))
    pp = sub.add_parser("propose-pin", help="diff a newer commit of a source against its pin (writes a proposal)")
    pp.add_argument("--source", required=True)
    pp.add_argument("--commit", required=True)
    pp.add_argument("--note", default="")
    pp.add_argument("--metadata", type=Path, help="source-metadata proposal JSON (branch, closed rounds, review state, artifacts)")
    pv = sub.add_parser("preview-pins", help="validate a hypothetical intake in a discarded copy, never adopt")
    pv.add_argument("--proposal", type=Path, action="append", required=True)
    pv.add_argument("--staged-candidates", type=Path, required=True)
    pv.add_argument("--staged-questions", type=Path, required=True)
    pv.add_argument("--out", type=Path, required=True)
    ap2 = sub.add_parser("apply-pin", help="adopt a pin proposal (named reviewer or logged standing decision)")
    ap2.add_argument("--source", required=True)
    ap2.add_argument("--commit", required=True)
    who = ap2.add_mutually_exclusive_group(required=True)
    who.add_argument("--reviewed-by", help="the named human who reviewed the proposal")
    who.add_argument("--standing-decision", help="author's logged standing pin instruction, AD-0006")
    si = sub.add_parser("intake-seeds", help="stage the author's seed files as unapproved proposals")
    si.add_argument("dir")
    rc = sub.add_parser("round-close", help="end a round: record the agent's open recommendations for implicit acceptance")
    rc.add_argument("--id", required=True, help="RT-0001, RT-0002, ...")
    rc.add_argument("--date", required=True)
    rc.add_argument("--report", required=True, help="repo-relative path of the round's report")
    rc.add_argument("--reported-at", required=True, help="commit the report describes")
    rc.add_argument("--note", default="")
    ra = sub.add_parser("ratify", help="apply the author's implicit acceptance of a round trip (their next instruction)")
    ra.add_argument("--round-trip", required=True)
    ra.add_argument("--decision-id", required=True, help="AD-000N in proposals/author-decisions.jsonl")
    ra.add_argument("--date", required=True)
    ra.add_argument("--instruction", required=True, help="the author's instruction that closed the round trip, verbatim")
    ra.add_argument("--object", action="append", default=[], help="an item the author objected to (repeatable)")
    hi = sub.add_parser("hist-inventory", help="inventory private historical ZIPs without extracting them (output outside the repo)")
    hi.add_argument("--archive", action="append", required=True, help="path to an archive (repeatable)")
    hi.add_argument("--out", required=True, help="directory outside the repository for the private inventory")
    hv = sub.add_parser("hist-verify", help="re-hash the archive members that historical findings cite")
    hv.add_argument("--archive-dir", required=True)
    sub.add_parser("smoke-cycle", help="run one complete hub cycle in a temporary copy (no experiment, no upstream mutation)")
    a = ap.parse_args(argv)

    if a.cmd == "audit":
        m = sources.load_manifest()
        print(json.dumps({"staleness": sources.staleness(m), "continuation_candidates": sources.continuation_candidates(m),
                          "artifacts": sources.verify_artifacts(m)}, indent=2))
        return 0
    if a.cmd == "pin":
        m = pins.build_manifest(by=a.by)
        pins.write_manifest(m)
        print(f"manifest written: {len(m['sources'])} sources")
        return 0
    if a.cmd == "validate":
        m = sources.load_manifest()
        loaded = sources.load_sources(m)
        problems = sources.validate_manifest(m) + [p for r in loaded["reports"].values() for p in r["problems"]] + ledger.validate_all(m, loaded, ledger.load_shared())
        print("\n".join(problems) or "valid")
        return 1 if problems else 0
    if a.cmd in ("update-candidates", "discover"):
        m = sources.load_manifest()
        loaded = sources.load_sources(m)
        out = discover.discover(loaded["nodes"], ledger.load_shared(), m, limit=a.limit)
        core.write_json(discover.diagnostics_path(), out)
        print(f"wrote {discover.diagnostics_path().relative_to(core.REPO)}: {len(out['candidates'])} retrieval candidates (not evidence)")
        return 0
    if a.cmd == "generate":
        files = generate.build(*generate.load_inputs())
        generate.write(files)
        print(f"generated {len(files)} files")
        return 0
    if a.cmd == "check":
        rep = workflow.check(use_git=not a.no_git, scope_base=None if a.no_git else a.scope_base)
        print(json.dumps(rep, indent=2))
        return 0 if rep["ok"] else 1
    if a.cmd == "snapshot":
        lock = workflow.create_snapshot(a.name, a.title)
        print(f"snapshot {a.name}: content hash {lock['content_hash']}")
        return 0
    if a.cmd == "review":
        p = workflow.review_proposal(a.id, a.decision, a.reviewer, a.rationale, human=a.human, decision_category=a.decision_category)
        print(json.dumps(p, indent=2))
        return 0
    if a.cmd == "propose-pin":
        rep = pins.propose_pin(sources.load_manifest(), a.source, a.commit, note=a.note,
                               metadata=core.read_json(a.metadata) if a.metadata else None)
        print(json.dumps({k: rep[k] for k in ("source", "current_commit", "proposed_commit", "descends_from_current", "warnings")}, indent=2))
        return 0
    if a.cmd == "apply-pin":
        if a.standing_decision:
            pins.auto_apply_pin(a.source, a.commit, decision_id=a.standing_decision)
        else:
            pins.apply_pin(a.source, a.commit, reviewed_by=a.reviewed_by)
        print("pin adopted; run generate and check")
        return 0
    if a.cmd == "preview-pins":
        result = preview.preview_pins(a.proposal, a.staged_candidates, a.staged_questions, a.out)
        print(json.dumps({"status": result["status"], "canonical_pins_unchanged": True,
                          "counts": result["check"]["info"]["counts"]}, indent=2))
        return 0
    if a.cmd == "round-close":
        rec = roundtrip.open_round_trip(a.id, a.date, a.report, a.reported_at, a.note)
        print(f"{a.id}: {len(rec['recommendations'])} recommendations await the author's next instruction")
        return 0
    if a.cmd == "ratify":
        print(json.dumps(roundtrip.ratify(a.round_trip, a.decision_id, a.date, a.instruction, a.object), indent=2))
        return 0
    if a.cmd == "hist-inventory":
        m = sources.load_manifest()
        expected = {x["name"]: x for x in historical.hist_source(m).get("expected_archives", [])}
        ok = True
        for path in a.archive:
            name = Path(path).name
            exp = expected.get(name, {})
            try:
                rep = historical.inventory_archive(Path(path), exp.get("sha256"), exp.get("entries"), archive_id=name)
            except historical.ArchiveError as exc:
                print(json.dumps({"archive": name, "error": str(exc)}))
                ok = False
                continue
            out = historical.write_private_inventory(rep, Path(a.out))
            ok &= rep["ok"] and bool(exp)
            print(json.dumps({"archive": name, "expected": bool(exp), "sha256": rep["sha256"], "members": rep["member_count"], "ok": rep["ok"], "problems": rep["problems"][:20], "warnings": len(rep["warnings"]), "inventory_digest": historical.inventory_digest(rep), "written": str(out)}, indent=2))
        return 0 if ok else 1
    if a.cmd == "hist-verify":
        m = sources.load_manifest()
        rep = historical.verify_local(m, historical.load_findings(core.ROOT), Path(a.archive_dir))
        print(json.dumps(rep, indent=2))
        return 1 if rep["problems"] else 0
    if a.cmd == "smoke-cycle":
        rep = smoke.run()
        print(json.dumps(rep, indent=2))
        return 0 if rep["ok"] else 1
    if a.cmd == "intake-seeds":
        print(json.dumps(workflow.intake_seeds(Path(a.dir)), indent=2))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
