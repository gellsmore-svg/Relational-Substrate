"""Command line: python3 research-synthesis/synth <command> (or PYTHONPATH=research-synthesis python3 -m rssynth)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import core, discover, generate, ledger, pins, sources, workflow


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
    ap2 = sub.add_parser("apply-pin", help="adopt a reviewed pin proposal (named human reviewer)")
    ap2.add_argument("--source", required=True)
    ap2.add_argument("--commit", required=True)
    ap2.add_argument("--reviewed-by", required=True)
    si = sub.add_parser("intake-seeds", help="stage the author's seed files as unapproved proposals")
    si.add_argument("dir")
    a = ap.parse_args(argv)

    if a.cmd == "audit":
        m = sources.load_manifest()
        print(json.dumps({"staleness": sources.staleness(m), "artifacts": sources.verify_artifacts(m)}, indent=2))
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
        rep = pins.propose_pin(sources.load_manifest(), a.source, a.commit, note=a.note)
        print(json.dumps({k: rep[k] for k in ("source", "current_commit", "proposed_commit", "descends_from_current", "warnings")}, indent=2))
        return 0
    if a.cmd == "apply-pin":
        pins.apply_pin(a.source, a.commit, reviewed_by=a.reviewed_by)
        print("pin adopted; run generate and check")
        return 0
    if a.cmd == "intake-seeds":
        print(json.dumps(workflow.intake_seeds(Path(a.dir)), indent=2))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
