"""Source federation: pinned manifest, git access, materialised copies, adapters.

Programme ledgers stay authoritative in their own branches. This module reads
them at pinned commits, keeps byte-identical *non-authoritative* copies under
``sources/materialised/`` so validation works without the branch, and checks
those copies against both their recorded digest and (when git can reach the
pin) the git blob at the pinned commit.
"""

from __future__ import annotations

import ast
import json
import subprocess
from pathlib import Path

from . import core

MANIFEST = core.ROOT / "sources" / "manifest.json"
MATERIALISED = core.ROOT / "sources" / "materialised"


class SourceError(ValueError):
    pass


# --- git access (optional) ------------------------------------------------------


def _git(*args: str, data: bool = False):
    try:
        out = subprocess.run(["git", "-C", str(core.REPO), *args], capture_output=True, check=False)
    except FileNotFoundError:
        return None
    if out.returncode != 0:
        return None
    return out.stdout if data else out.stdout.decode().strip()


def git_available() -> bool:
    return _git("rev-parse", "--git-dir") is not None


def commit_reachable(commit: str) -> bool:
    return _git("cat-file", "-e", f"{commit}^{{commit}}") is not None


def git_file(commit: str, path: str) -> bytes | None:
    return _git("show", f"{commit}:{path}", data=True)


def remote_branch_head(branch: str) -> str | None:
    return _git("rev-parse", "--verify", "-q", f"refs/remotes/origin/{branch}")


def is_ancestor(a: str, b: str) -> bool | None:
    try:
        out = subprocess.run(["git", "-C", str(core.REPO), "merge-base", "--is-ancestor", a, b], capture_output=True)
    except FileNotFoundError:
        return None
    if out.returncode in (0, 1):
        return out.returncode == 0
    return None


def tracked_in_worktree(path: str) -> bool:
    return _git("ls-files", "--error-unmatch", path) is not None


# --- manifest ---------------------------------------------------------------------


def load_manifest(path: Path = MANIFEST) -> dict:
    m = core.read_json(path)
    if m.get("schema") != "rssynth.source-manifest/v1":
        raise SourceError("unknown manifest schema")
    return m


def sources_by_key(manifest: dict) -> dict[str, dict]:
    out = {}
    for s in manifest["sources"]:
        if s["source_key"] in out:
            raise SourceError(f"duplicate source key {s['source_key']}")
        out[s["source_key"]] = s
    return out


def materialised_path(source: dict, artifact: dict) -> Path:
    return MATERIALISED / source["source_key"] / artifact["path"]


def validate_manifest(manifest: dict) -> list[str]:
    """Structural problems: namespaces, defaults, commits, statuses, lineage targets."""
    problems = []
    try:
        keys = sources_by_key(manifest)
    except SourceError as exc:
        return [str(exc)]
    defaults: dict[str, str] = {}
    for k, s in keys.items():
        if s.get("status") not in core.SOURCE_STATUSES:
            problems.append(f"{k}: unknown status {s.get('status')!r}")
        ns = s.get("namespace")
        if not ns or not core.REF_RE.match(f"{ns}::x"):
            problems.append(f"{k}: invalid namespace {ns!r}")
        if ns in core.SHARED_NAMESPACES:
            problems.append(f"{k}: namespace {ns} is reserved for shared records")
        if s.get("default_revision"):
            if ns in defaults:
                problems.append(f"namespace collision: {ns} has two default revisions ({defaults[ns]}, {k})")
            defaults[ns] = k
        if s["status"] in ("included", "catalogued_only", "lineage_only"):
            c = s.get("commit") or ""
            if len(c) != 40 or any(ch not in "0123456789abcdef" for ch in c):
                problems.append(f"{k}: missing or abbreviated pinned commit")
        for a in s.get("artifacts", []):
            for field in ("path", "kind", "sha256", "git_blob"):
                if not a.get(field):
                    problems.append(f"{k}: artifact {a.get('path')} lacks {field}")
        for lin in s.get("lineage", []):
            if lin.get("target") not in keys:
                problems.append(f"{k}: lineage target {lin.get('target')} is not a declared source")
    for k, s in keys.items():
        if s["status"] == "included" and not s.get("default_revision"):
            # explicit revisions must be referenced as NS@REV::id
            pass
    return problems


def resolve_source(manifest: dict, namespace: str, revision: str | None) -> dict | None:
    for s in manifest["sources"]:
        if s["namespace"] != namespace:
            continue
        if revision is None and s.get("default_revision"):
            return s
        if revision is not None and (s.get("revision_label") == revision or s["source_key"] == revision or s.get("commit", "").startswith(revision)):
            return s
    return None


# --- verification -------------------------------------------------------------------


def verify_artifacts(manifest: dict, *, use_git: bool = True) -> list[dict]:
    """One record per artifact: digest of the materialised copy, git blob at the pin, worktree presence."""
    records = []
    have_git = use_git and git_available()
    for s in manifest["sources"]:
        reach = commit_reachable(s["commit"]) if have_git and s.get("commit") else None
        for a in s.get("artifacts", []):
            rec = {"source": s["source_key"], "path": a["path"], "kind": a["kind"], "materialised": bool(a.get("materialised"))}
            if a.get("materialised"):
                p = materialised_path(s, a)
                if not p.exists():
                    rec["copy"] = "missing"
                else:
                    data = p.read_bytes()
                    rec["copy"] = "ok" if core.sha256_bytes(data) == a["sha256"] and core.git_blob_id(data) == a["git_blob"] else "TAMPERED"
            if reach is None:
                rec["pin"] = "git_unavailable"
            elif not reach:
                rec["pin"] = "pin_unreachable"
            else:
                blob = _git("rev-parse", f"{s['commit']}:{a['path']}")
                rec["pin"] = "ok" if blob == a["git_blob"] else ("path_missing_at_pin" if blob is None else "PIN_DIGEST_MISMATCH")
            rec["in_checked_out_tree"] = tracked_in_worktree(a["path"]) if have_git else None
            records.append(rec)
    return records


def staleness(manifest: dict) -> list[dict]:
    """Has the tracked branch moved past the pin? Informational; never auto-updates."""
    out = []
    for s in manifest["sources"]:
        if not s.get("branch") or not s.get("commit"):
            continue
        head = remote_branch_head(s["branch"])
        if head is None:
            out.append({"source": s["source_key"], "state": "branch_not_visible"})
        elif head == s["commit"]:
            out.append({"source": s["source_key"], "state": "current", "head": head})
        else:
            anc = is_ancestor(s["commit"], head)
            out.append({"source": s["source_key"], "state": "behind_branch_head" if anc else "diverged_from_branch", "head": head})
    return out


# --- adapters -------------------------------------------------------------------------


def _literal_sets(py_source: str) -> dict:
    """Module-level constant sets/tuples from a validator file, read with ast (never executed)."""
    out = {}
    tree = ast.parse(py_source)
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                value = ast.literal_eval(node.value)
            except Exception:
                continue
            if isinstance(value, (set, tuple, frozenset)):
                out[node.targets[0].id] = set(value)
    return out


def _artifact(source: dict, kind: str) -> dict | None:
    for a in source.get("artifacts", []):
        if a["kind"] == kind:
            return a
    return None


def _read_artifact(source: dict, kind: str) -> bytes | None:
    a = _artifact(source, kind)
    if a is None:
        return None
    p = materialised_path(source, a)
    if p.exists():
        return p.read_bytes()
    if commit_reachable(source["commit"]):
        return git_file(source["commit"], a["path"])
    return None


def adapt_coherence_ledger(source: dict) -> dict:
    """Validate and project a programme coherence ledger (findings + relations) under its own pinned vocabulary."""
    ns = source["namespace"]
    problems: list[str] = []
    validator = _read_artifact(source, "validator")
    if validator is None:
        raise SourceError(f"{source['source_key']}: pinned validator unavailable")
    vocab = _literal_sets(validator.decode("utf-8"))
    layers = vocab.get("EPISTEMIC_LAYERS", set())
    statuses = vocab.get("STATUSES", set())
    rel_types = vocab.get("RELATION_TYPES", set())
    rob_keys = vocab.get("ROBUSTNESS_KEYS", set())
    if not (layers and statuses and rel_types):
        raise SourceError(f"{source['source_key']}: validator vocabulary not found; upstream schema incompatible")
    findings = [json.loads(line) for line in (_read_artifact(source, "findings") or b"").decode().splitlines() if line.strip()]
    relations = [json.loads(line) for line in (_read_artifact(source, "relations") or b"").decode().splitlines() if line.strip()]
    core_fields = set(source["adapter_options"]["core_finding_fields"])
    allowed_extra = set(source["adapter_options"].get("extra_finding_fields", []))
    nodes, edges, seen = {}, [], set()
    for f in findings:
        fid = f.get("finding_id")
        missing = core_fields - f.keys()
        if missing:
            problems.append(f"{ns}::{fid} lacks {sorted(missing)}")
        extra = f.keys() - core_fields - allowed_extra
        if extra:
            problems.append(f"{ns}::{fid} has undeclared fields {sorted(extra)}")
        if fid in seen:
            problems.append(f"duplicate finding id {ns}::{fid}")
        seen.add(fid)
        if f.get("epistemic_layer") not in layers:
            problems.append(f"{ns}::{fid} layer {f.get('epistemic_layer')!r} not in pinned vocabulary")
        if f.get("status") not in statuses:
            problems.append(f"{ns}::{fid} status {f.get('status')!r} not in pinned vocabulary")
        rv = f.get("robustness_vector")
        if rob_keys and (not isinstance(rv, dict) or set(rv) != rob_keys):
            problems.append(f"{ns}::{fid} robustness vector malformed")
        kind = "source_question" if f.get("epistemic_layer") == "OPEN_QUESTION" else "source_finding"
        nodes[f"{ns}::{fid}"] = {
            "kind": kind,
            "source": source["source_key"],
            "local_id": fid,
            "statement": f.get("statement", ""),
            "epistemic_layer": f.get("epistemic_layer"),
            "status": f.get("status"),
            "scope": f.get("scope", ""),
            "created_generation": f.get("created_generation"),
            "created_commit": f.get("created_commit"),
            "structural_roles": f.get("structural_roles", []),
            "magnitude_class": f.get("magnitude_class"),
            "observable": f.get("observable", ""),
        }
    rid_seen = set()
    for r in relations:
        rid = r.get("relation_id")
        if rid in rid_seen:
            problems.append(f"duplicate relation id {ns}::{rid}")
        rid_seen.add(rid)
        if r.get("relation_type") not in rel_types:
            problems.append(f"{ns}::{rid} relation type {r.get('relation_type')!r} not in pinned vocabulary")
        a, b = f"{ns}::{r.get('from_finding')}", f"{ns}::{r.get('to_finding')}"
        if a not in nodes or b not in nodes:
            problems.append(f"{ns}::{rid} names a missing finding")
            continue
        edges.append({"kind": "source_relation", "source": source["source_key"], "id": f"{ns}::{rid}", "from": a, "to": b, "type": r["relation_type"], "rationale": r.get("rationale", "")})
    return {"nodes": nodes, "edges": edges, "problems": problems, "vocabulary": {k: sorted(v) for k, v in vocab.items() if k in ("EPISTEMIC_LAYERS", "STATUSES", "RELATION_TYPES")}, "counts": {"findings": len(findings), "relations": len(relations)}}


def adapt_theorem_catalog(source: dict) -> dict:
    ns = source["namespace"]
    raw = _read_artifact(source, "theorem_catalog")
    if raw is None:
        return {"nodes": {}, "edges": [], "problems": [f"{source['source_key']}: theorem catalogue unavailable"]}
    nodes, edges, problems = {}, [], []
    for line in raw.decode().splitlines():
        if not line.strip():
            continue
        t = json.loads(line)
        tid = t.get("theorem_id")
        if not tid or f"{ns}::{tid}" in nodes:
            problems.append(f"{ns}: missing or duplicate theorem id {tid!r}")
            continue
        nodes[f"{ns}::{tid}"] = {"kind": "formal_claim", "source": source["source_key"], "local_id": tid, "statement": t.get("statement", ""), "title": t.get("title", ""), "status": t.get("status"), "epistemic_layer": "FORMAL_" + str(t.get("status")), "scope": t.get("scope", ""), "assumptions": t.get("assumptions"), "counterexample_scope": t.get("counterexample_scope", "")}
        refs = t.get("coherence_refs") or []
        if isinstance(refs, str):
            try:
                refs = ast.literal_eval(refs)
            except Exception:
                refs = []
        for ref in refs:
            edges.append({"kind": "source_catalogue_link", "source": source["source_key"], "id": f"{ns}::{tid}->{ref}", "from": f"{ns}::{tid}", "to": f"{ns}::{ref}", "type": "catalogued_with", "rationale": "theorem catalogue coherence_refs"})
    return {"nodes": nodes, "edges": edges, "problems": problems}


def adapt_documents(source: dict) -> dict:
    ns = source["namespace"]
    nodes = {}
    for a in source.get("artifacts", []):
        if a["kind"] == "document":
            nodes[f"{ns}::{a['path']}"] = {"kind": "source_document", "source": source["source_key"], "local_id": a["path"], "statement": a.get("description", ""), "status": source["status"], "epistemic_layer": "DOCUMENT"}
    return {"nodes": nodes, "edges": [], "problems": []}


def load_sources(manifest: dict) -> dict:
    """Run every adapter for included/catalogued sources. Returns merged nodes, edges, per-source reports."""
    nodes, edges, reports = {}, [], {}
    for s in manifest["sources"]:
        rep = {"status": s["status"], "problems": [], "counts": {}}
        if s["status"] in ("included",):
            for adapter in s.get("adapters", []):
                fn = {"coherence_ledger_v1": adapt_coherence_ledger, "theorem_catalog_v1": adapt_theorem_catalog, "document_v1": adapt_documents}[adapter]
                out = fn(s)
                for k, v in out["nodes"].items():
                    if k in nodes:
                        rep["problems"].append(f"node collision {k}")
                    nodes[k] = v
                edges.extend(out["edges"])
                rep["problems"].extend(out["problems"])
                rep["counts"][adapter] = len(out["nodes"])
        elif s["status"] == "catalogued_only":
            out = adapt_documents(s)
            nodes.update(out["nodes"])
            rep["counts"]["document_v1"] = len(out["nodes"])
        reports[s["source_key"]] = rep
    return {"nodes": nodes, "edges": edges, "reports": reports}


# --- pinning ------------------------------------------------------------------------------


def pin_artifact(commit: str, path: str, kind: str, *, materialise: bool, source_key: str, description: str = "") -> dict:
    data = git_file(commit, path)
    if data is None:
        raise SourceError(f"{path} not present at {commit}")
    rec = {"path": path, "kind": kind, "sha256": core.sha256_bytes(data), "bytes": len(data), "git_blob": core.git_blob_id(data), "materialised": materialise}
    if description:
        rec["description"] = description
    if materialise:
        dest = MATERIALISED / source_key / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    return rec
