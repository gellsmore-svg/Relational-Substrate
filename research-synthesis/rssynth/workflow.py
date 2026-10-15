"""Change control: snapshots, review decisions, seed intake, scope guard and the aggregate check."""

from __future__ import annotations

import datetime
import json
import subprocess
from pathlib import Path

from . import core, generate, ledger, sources

def snapshots_dir():
    return core.ROOT / "snapshots"
ALLOWED_PREFIXES = ("research-synthesis/", ".github/workflows/research-synthesis.yml")


# --- snapshots ----------------------------------------------------------------------


def _hash_tree(files: dict[str, bytes]) -> str:
    return core.sha256_bytes(core.canonical({k: core.sha256_bytes(v) for k, v in sorted(files.items())}).encode())


def create_snapshot(name: str, title: str) -> dict:
    """Immutable milestone view: generated files + lock (source pins, ledger and manifest digests, content hash)."""
    if not name or "/" in name or name.startswith("."):
        raise ValueError("snapshot name must be a simple directory name")
    dest = snapshots_dir() / name
    if dest.exists():
        raise FileExistsError(f"snapshot {name} exists; snapshots are immutable")
    manifest, loaded, shared, discovery = generate.load_inputs()
    files = generate.build(manifest, loaded, shared, discovery)
    if generate.stale(files):
        raise RuntimeError("generated views are stale; run generate before snapshot")
    data = {rel: text.encode("utf-8") for rel, text in files.items()}
    ledger_files = sorted(str(p.relative_to(core.ROOT)) for d in ("ledger", "proposals") for p in (core.ROOT / d).rglob("*") if p.is_file())
    lock = {
        "schema": "rssynth.snapshot-lock/v1",
        "name": name,
        "title": title,
        "manifest_sha256": core.sha256_file(sources.manifest_path()),
        "source_pins": {s["source_key"]: s.get("commit") for s in manifest["sources"]},
        "shared_record_sha256": {f: core.sha256_file(core.ROOT / f) for f in ledger_files},
        "view_sha256": {rel: core.sha256_bytes(b) for rel, b in sorted(data.items())},
        "content_hash": _hash_tree(data),
    }
    for rel, b in data.items():
        p = dest / "views" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b)
    core.write_json(dest / "lock.json", lock)
    return lock


def verify_snapshots() -> list[str]:
    problems = []
    if not snapshots_dir().exists():
        return problems
    for d in sorted(p for p in snapshots_dir().iterdir() if p.is_dir()):
        lock_path = d / "lock.json"
        if not lock_path.exists():
            problems.append(f"snapshot {d.name}: lock.json missing")
            continue
        lock = core.read_json(lock_path)
        data = {}
        for p in (d / "views").rglob("*"):
            if p.is_file():
                data[str(p.relative_to(d / "views"))] = p.read_bytes()
        if set(data) != set(lock["view_sha256"]):
            problems.append(f"snapshot {d.name}: file set changed")
        for rel, digest in lock["view_sha256"].items():
            if rel in data and core.sha256_bytes(data[rel]) != digest:
                problems.append(f"snapshot {d.name}: {rel} TAMPERED")
        if _hash_tree(data) != lock["content_hash"]:
            problems.append(f"snapshot {d.name}: content hash mismatch")
    return problems


# --- review decisions -------------------------------------------------------------------


def review_proposal(proposal_id: str, decision: str, reviewer: str, rationale: str, *, human: bool, root: Path | None = None) -> dict:
    """Record a decision on a proposal. 'agent_reviewed'/'human_accepted' promote it into the ledger after validation."""
    root = root or core.ROOT
    if decision not in ("agent_reviewed", "human_accepted", "rejected", "undetermined", "under_review"):
        raise ValueError(f"unknown decision {decision}")
    if decision == "human_accepted" and (not human or reviewer.lower().startswith("agent")):
        raise ValueError("human acceptance needs --human and a named human reviewer")
    prop_path = root / "proposals" / "candidate-relations.jsonl"
    props = core.read_jsonl(prop_path)
    (p,) = [x for x in props if x["proposal_id"] == proposal_id] or [None]
    if p is None:
        raise KeyError(proposal_id)
    rid = proposal_id.replace("::", "-")
    rec = f"proposals/reviews/{rid}-{decision}.md"
    core.write_text(root / rec, f"# Review record {proposal_id}\n\n- **Reviewer:** {reviewer}\n- **Human:** {human}\n- **Decision:** {decision}\n- **Date:** {datetime.date.today().isoformat()}\n\n## Rationale\n\n{rationale}\n")
    p["status"] = decision
    p["decision_rationale"] = rationale
    p["review"] = {"reviewer": reviewer, "date": datetime.date.today().isoformat(), "record": rec, "human": human}
    if decision in ("agent_reviewed", "human_accepted"):
        conns = core.read_jsonl(root / "ledger" / "connections.jsonl")
        n = 1 + max([int(x["connection_id"].split("::")[1]) for x in conns] or [0])
        new = {k: v for k, v in p.items() if k not in ("proposal_id", "status", "decision_rationale")}
        new.update({"connection_id": f"X::{n:04d}", "review_status": decision, "promoted_from": proposal_id})
        manifest = sources.load_manifest()
        loaded = sources.load_sources(manifest)
        shared = ledger.load_shared(root)
        R = ledger.Resolver(manifest, loaded["nodes"], shared)
        problems = ledger.validate_connection(new, R, in_ledger=True, root=root)
        if problems:
            raise ValueError("promotion refused: " + "; ".join(problems))
        conns.append(new)
        core.write_jsonl(root / "ledger" / "connections.jsonl", conns)
        p["promoted_to"] = new["connection_id"]
    core.write_jsonl(prop_path, props)
    return p


# --- seed intake ----------------------------------------------------------------------------


def intake_seeds(seed_dir: Path, root: Path | None = None) -> dict:
    """Stage the author's seed files as *unapproved* proposals. Never writes to the ledger."""
    root = root or core.ROOT
    report = {"candidate_relations": 0, "metaphors": 0, "problems": []}
    rel = seed_dir / "candidate-relations.jsonl"
    if rel.exists():
        props = core.read_jsonl(root / "proposals" / "candidate-relations.jsonl")
        have = {p["proposal_id"] for p in props}
        n = 1 + max([int(p["proposal_id"].split("::")[1]) for p in props if p["proposal_id"].split("::")[1].isdigit()] or [0])
        for row in core.read_jsonl(rel):
            row = dict(row)
            row.setdefault("proposal_id", f"P::{n:04d}")
            n += 1
            if row["proposal_id"] in have:
                report["problems"].append(f"duplicate proposal id {row['proposal_id']}")
                continue
            row["status"] = "proposed"
            row["origin"] = "author_seed"
            for k in ("comparison", "controls", "alternatives", "falsifiers", "evidence_refs"):
                row.setdefault(k, {} if k in ("comparison", "controls") else [])
            row.setdefault("independence", "unknown")
            props.append(row)
            report["candidate_relations"] += 1
        core.write_jsonl(root / "proposals" / "candidate-relations.jsonl", props)
    met = seed_dir / "metaphors.jsonl"
    if met.exists():
        drafts = core.read_jsonl(root / "proposals" / "metaphor-drafts.jsonl")
        for row in core.read_jsonl(met):
            row = dict(row, status="draft", origin="author_seed", evidentiary=False)
            drafts.append(row)
            report["metaphors"] += 1
        core.write_jsonl(root / "proposals" / "metaphor-drafts.jsonl", drafts)
    manifest_seed = seed_dir / "source-manifest.json"
    if manifest_seed.exists():
        report["source_manifest"] = "received; compare by hand with sources/pin-spec.json and verify every path at its pinned commit before adopting (see docs/cadence.md)"
    return report


# --- scope guard and aggregate check --------------------------------------------------------


def scope_violations(base: str = "origin/main") -> list[str] | None:
    """Paths changed on this branch outside the shared layer (None if git cannot tell)."""
    out = subprocess.run(["git", "-C", str(core.REPO), "diff", "--name-only", f"{base}...HEAD"], capture_output=True, text=True)
    if out.returncode != 0:
        return None
    return sorted(p for p in out.stdout.split() if not p.startswith(ALLOWED_PREFIXES))


def check(*, use_git: bool = True, scope_base: str | None = "origin/main") -> dict:
    report: dict = {"errors": [], "warnings": [], "info": {}}
    manifest = sources.load_manifest()
    report["errors"] += [f"manifest: {p}" for p in sources.validate_manifest(manifest)]
    for rec in sources.verify_artifacts(manifest, use_git=use_git):
        if rec.get("copy") in ("missing", "TAMPERED"):
            report["errors"].append(f"materialised copy {rec['source']}:{rec['path']} {rec['copy']}")
        if rec["pin"] in ("PIN_DIGEST_MISMATCH", "path_missing_at_pin"):
            report["errors"].append(f"pin {rec['source']}:{rec['path']} {rec['pin']}: upstream changed under the pin; stop and review")
        if rec["pin"] == "pin_unreachable":
            report["warnings"].append(f"pin {rec['source']} unreachable in this clone (verified against materialised copy only)")
    loaded = sources.load_sources(manifest)
    for k, r in loaded["reports"].items():
        report["errors"] += [f"source {k}: {p}" for p in r["problems"]]
    shared = ledger.load_shared()
    report["errors"] += [f"shared: {p}" for p in ledger.validate_all(manifest, loaded, shared)]
    disc_path = core.ROOT / "proposals" / "discovery-diagnostics.json"
    files = generate.build(manifest, loaded, shared, core.read_json(disc_path) if disc_path.exists() else None)
    report["errors"] += [f"generated view stale: {p}" for p in generate.stale(files)]
    report["errors"] += verify_snapshots()
    if use_git:
        report["info"]["staleness"] = sources.staleness(manifest)
        for s in report["info"]["staleness"]:
            if s["state"] not in ("current",):
                report["warnings"].append(f"source {s['source']}: {s['state']} (a newer round may need a pin review)")
        if scope_base:
            v = scope_violations(scope_base)
            if v is None:
                report["warnings"].append("scope guard skipped (base ref not available)")
            elif v:
                report["errors"].append("files outside research-synthesis/ changed: " + ", ".join(v))
    report["info"]["counts"] = {"source_nodes": len(loaded["nodes"]), "connections": len(shared["connections"]), "proposals": len(shared["proposals"]), "metaphors": len(shared["metaphors"])}
    report["ok"] = not report["errors"]
    return report
