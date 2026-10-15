"""Pinning and milestone pin updates.

``build_manifest`` turns ``sources/pin-spec.json`` into ``sources/manifest.json``
and the materialised copies, verifying every path at its pinned commit.
``propose_pin`` diffs a newer commit's ledger against the current pin and
writes a proposal; it never edits the manifest. ``apply_pin`` adopts a
reviewed proposal (a human decision recorded with the reviewer's name).
"""

from __future__ import annotations

import datetime
import json
import shutil

from . import core, sources

def spec_path_default() -> "core.Path":
    return core.ROOT / "sources" / "pin-spec.json"


def pin_proposals_dir():
    return core.ROOT / "proposals" / "pin-updates"


def build_manifest(spec_path=None, *, date: str | None = None, by: str = "agent") -> dict:
    spec = core.read_json(spec_path or spec_path_default())
    if spec.get("schema") != "rssynth.pin-spec/v1":
        raise sources.SourceError("unknown pin-spec schema")
    out = {"schema": "rssynth.source-manifest/v1", "generated_from": "sources/pin-spec.json", "sources": []}
    for s in spec["sources"]:
        entry = {k: v for k, v in s.items() if k != "artifacts"}
        entry["adapter_options"] = {"core_finding_fields": spec["core_finding_fields"], "extra_finding_fields": s.get("extra_finding_fields", [])}
        entry.pop("extra_finding_fields", None)
        entry["artifacts"] = []
        if s["status"] in ("included", "catalogued_only", "lineage_only"):
            if not sources.commit_reachable(s["commit"]):
                raise sources.SourceError(f"{s['source_key']}: pinned commit {s['commit']} is not reachable; fetch it first")
            for a in s.get("artifacts", []):
                entry["artifacts"].append(sources.pin_artifact(s["commit"], a["path"], a["kind"], materialise=bool(a.get("materialise")) and s["status"] == "included", source_key=s["source_key"], description=a.get("description", "")))
            entry["ingestion_receipt"] = {"date": date or datetime.date.today().isoformat(), "by": by, "checks": ["commit reachable", "every artifact path present at the pinned commit", "sha256 and git blob recorded", "materialised copies written byte-identically"]}
        out["sources"].append(entry)
    problems = sources.validate_manifest(out)
    if problems:
        raise sources.SourceError("; ".join(problems))
    return out


def write_manifest(manifest: dict) -> None:
    # drop stale materialised copies of sources that no longer materialise anything
    core.write_json(sources.manifest_path(), manifest)


def _ledger_rows(commit: str, path: str) -> dict[str, dict]:
    data = sources.git_file(commit, path)
    if data is None:
        return {}
    rows = [json.loads(line) for line in data.decode().splitlines() if line.strip()]
    key = "finding_id" if rows and "finding_id" in rows[0] else "relation_id"
    return {r[key]: r for r in rows}


def propose_pin(manifest: dict, source_key: str, new_commit: str, *, note: str = "") -> dict:
    """Diff the source's ledgers between the current pin and ``new_commit``; flag upstream rewrites."""
    s = sources.sources_by_key(manifest)[source_key]
    if not sources.commit_reachable(new_commit):
        raise sources.SourceError(f"{new_commit} not reachable")
    anc = sources.is_ancestor(s["commit"], new_commit)
    report = {"schema": "rssynth.pin-proposal/v1", "source": source_key, "current_commit": s["commit"], "proposed_commit": new_commit, "descends_from_current": anc, "note": note, "artifacts": [], "status": "proposed"}
    for a in s.get("artifacts", []):
        new = sources.git_file(new_commit, a["path"])
        entry = {"path": a["path"], "kind": a["kind"], "changed": None if new is None else core.git_blob_id(new) != a["git_blob"], "present": new is not None}
        if a["kind"] in ("findings", "relations") and new is not None:
            old_rows, new_rows = _ledger_rows(s["commit"], a["path"]), _ledger_rows(new_commit, a["path"])
            entry["added"] = sorted(set(new_rows) - set(old_rows))
            entry["removed"] = sorted(set(old_rows) - set(new_rows))
            entry["rewritten"] = sorted(k for k in set(old_rows) & set(new_rows) if old_rows[k] != new_rows[k])
        report["artifacts"].append(entry)
    rewritten = [k for a in report["artifacts"] for k in a.get("rewritten", [])]
    removed = [k for a in report["artifacts"] for k in a.get("removed", [])]
    report["warnings"] = []
    if anc is False:
        report["warnings"].append("proposed commit does not descend from the current pin (branch rewritten or parallel revision)")
    if rewritten:
        report["warnings"].append(f"{len(rewritten)} upstream rows changed in place; shared connections citing them need re-review")
    if removed:
        report["warnings"].append(f"{len(removed)} upstream rows removed")
    pin_proposals_dir().mkdir(parents=True, exist_ok=True)
    core.write_json(pin_proposals_dir() / f"{source_key}-{new_commit[:12]}.json", report)
    return report


def apply_pin(source_key: str, new_commit: str, *, reviewed_by: str, spec_path=None) -> dict:
    """Adopt a reviewed pin: update the spec, rebuild the manifest, record the decision on the proposal."""
    if not reviewed_by or reviewed_by.lower().startswith("agent"):
        raise sources.SourceError("a pin is adopted only with a named human reviewer")
    spec_path = spec_path or spec_path_default()
    prop_path = pin_proposals_dir() / f"{source_key}-{new_commit[:12]}.json"
    if not prop_path.exists():
        raise sources.SourceError("no pin proposal for this commit; run propose-pin first")
    spec = core.read_json(spec_path)
    for s in spec["sources"]:
        if s["source_key"] == source_key:
            s["commit"] = new_commit
    core.write_json(spec_path, spec)
    stale = sources.materialised_dir() / source_key
    if stale.exists():
        shutil.rmtree(stale)
    manifest = build_manifest(spec_path, by=f"human review: {reviewed_by}")
    write_manifest(manifest)
    prop = core.read_json(prop_path)
    prop.update({"status": "adopted", "reviewed_by": reviewed_by, "adopted_on": datetime.date.today().isoformat()})
    core.write_json(prop_path, prop)
    return manifest
