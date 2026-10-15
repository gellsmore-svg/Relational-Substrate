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


# Author seed concept targets -> shared concepts, only where the meaning is the same.
# Everything else is kept verbatim and reported as an unmapped target (a coverage gap or a candidate concept).
SEED_CONCEPT_MAP = {
    "occupancy_vs_passage": "C::occupancy-vs-process",
    "predictive_sufficiency": "C::predictive-sufficiency",
    "higher_order_context": "C::higher-order-context",
    "clock_dependence": "C::clock-readout-dependence",
    "continuous_vs_jump_clock": "C::clock-readout-dependence",
}


def _seed_claim(row: dict, receipt: dict) -> dict:
    rel = row.get("relation_type_proposed")
    return {
        "kind": "seed_claim",
        "proposal_id": f"P::{row['proposal_id']}",
        "seed_id": row["proposal_id"],
        "seed_record": row,
        "claim": row.get("claim", ""),
        "cannot_infer": row.get("cannot_infer", ""),
        "discriminator": row.get("discriminator", ""),
        "theme": row.get("theme", ""),
        "sources": list(row.get("sources", [])),
        "relation_type_proposed": rel,
        "connection_type": ledger.SEED_RELATION_MAP.get(rel),
        "seed_review_status": row.get("review_status"),
        "blocked_on_historical_primary": "historical" in str(row.get("review_status", "")),
        "status": "proposed",
        "origin": "author_seed",
        "intake": receipt,
    }


def _seed_metaphor(row: dict, receipt: dict) -> dict:
    targets = list(row.get("concept_targets", []))
    mapped = sorted({SEED_CONCEPT_MAP[t] for t in targets if t in SEED_CONCEPT_MAP})
    return {
        "metaphor_id": f"M::{row['metaphor_id']}",
        "seed_id": row["metaphor_id"],
        "seed_record": row,
        "title": row.get("name", ""),
        "audience": row.get("audience", ""),
        "concepts": mapped,
        "concept_targets": targets,
        "unmapped_concept_targets": [t for t in targets if t not in SEED_CONCEPT_MAP],
        "mapping": [{"figure": a, "object": b} for a, b in row.get("maps", [])],
        "explanation": row.get("explanation", ""),
        "does_not_mean": [row["boundary"]] if row.get("boundary") else [],
        "misleading_readings": [row["misleading_if"]] if row.get("misleading_if") else [],
        "illustrative_status": f"author seed ({row.get('status')}); image suggestion: {row.get('image_suggestion', '')}",
        "review": {"owner": "programme author (human)", "process": "docs/cadence.md (metaphor review)", "human_reviewed": False},
        "status": "draft",
        "evidentiary": False,
        "origin": "author_seed",
        "intake": receipt,
    }


def intake_seeds(seed_dir: Path, root: Path | None = None, *, label: str | None = None) -> dict:
    """Stage the author's seed files as *unapproved* proposals. Never writes to the ledger.

    The seed files are copied verbatim to proposals/seeds/<label>/ with a sha256
    receipt. Records in the shared schema are staged as they are; records in the
    author pack schema (claims with 'sources'; metaphors with 'maps') are kept
    verbatim under 'seed_record' with mapped fields added. Re-running is
    idempotent: ids already staged are reported and skipped.
    """
    root = root or core.ROOT
    seed_dir = Path(seed_dir)
    label = label or datetime.date.today().isoformat()
    store = root / "proposals" / "seeds" / label
    store.mkdir(parents=True, exist_ok=True)
    receipt_files = {}
    for name in ("candidate-relations.jsonl", "metaphors.jsonl", "source-manifest.json"):
        src = seed_dir / name
        if src.exists():
            data = src.read_bytes()
            (store / name).write_bytes(data)
            receipt_files[name] = {"sha256": core.sha256_bytes(data), "bytes": len(data)}
    receipt = {"label": label, "stored_at": str(store.relative_to(root))}
    report = {"candidate_relations": 0, "metaphors": 0, "skipped_existing": [], "problems": [], "files": receipt_files}
    rel = seed_dir / "candidate-relations.jsonl"
    if rel.exists():
        props = core.read_jsonl(root / "proposals" / "candidate-relations.jsonl")
        have = {p["proposal_id"] for p in props}
        n = 1 + max([int(p["proposal_id"].split("::")[1]) for p in props if p["proposal_id"].split("::")[1].isdigit()] or [0])
        for row in core.read_jsonl(rel):
            if "claim" in row and "sources" in row:
                rec = _seed_claim(row, receipt)
                if rec["relation_type_proposed"] not in ledger.SEED_RELATION_MAP:
                    report["problems"].append(f"{rec['seed_id']}: unmapped relation type {rec['relation_type_proposed']!r}")
            else:
                rec = dict(row)
                rec.setdefault("proposal_id", f"P::{n:04d}")
                n += 1
                rec.update({"status": "proposed", "origin": "author_seed", "intake": receipt})
                for k in ("comparison", "controls", "alternatives", "falsifiers", "evidence_refs"):
                    rec.setdefault(k, {} if k in ("comparison", "controls") else [])
                rec.setdefault("independence", "unknown")
            if rec["proposal_id"] in have:
                report["skipped_existing"].append(rec["proposal_id"])
                continue
            props.append(rec)
            have.add(rec["proposal_id"])
            report["candidate_relations"] += 1
        core.write_jsonl(root / "proposals" / "candidate-relations.jsonl", props)
    met = seed_dir / "metaphors.jsonl"
    if met.exists():
        drafts = core.read_jsonl(root / "proposals" / "metaphor-drafts.jsonl")
        have = {m["metaphor_id"] for m in drafts} | {m["metaphor_id"] for m in core.read_jsonl(root / "ledger" / "metaphors.jsonl")}
        for row in core.read_jsonl(met):
            rec = _seed_metaphor(row, receipt) if "maps" in row else dict(row, status="draft", origin="author_seed", evidentiary=False, intake=receipt)
            if rec["metaphor_id"] in have:
                report["skipped_existing"].append(rec["metaphor_id"])
                continue
            drafts.append(rec)
            have.add(rec["metaphor_id"])
            report["metaphors"] += 1
        core.write_jsonl(root / "proposals" / "metaphor-drafts.jsonl", drafts)
    if (seed_dir / "source-manifest.json").exists():
        report["source_manifest"] = "stored verbatim; compared with sources/pin-spec.json in the intake report (pins are never adopted from a seed without review)"
    core.write_json(store / "receipt.json", report)
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
