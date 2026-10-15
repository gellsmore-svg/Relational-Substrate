"""Historical source adapter: private archives outside Git, public derived records inside it.

The historical archives are private. This module never extracts them and never writes their bytes
into the repository. It provides:

- `inventory_archive`: a read-only, extraction-free inventory of one ZIP (whole-file and per-member
  SHA-256, unsafe paths, duplicates, symlinks, nested archives, decompression limits). Inventories
  are written outside the repository.
- `validate_findings`: checks on the public derived records in sources/historical/findings.jsonl
  (identifiers, digests, evidence layers, verification level, privacy approval, conflicts, scope).
- `verify_local`: re-hashes the archive members that findings cite, when the archives are present.
  CI normally lacks them, so these checks are reported as requiring private input, never as passed.

Verification levels are kept apart:
1. local_source_verified: the archive and member bytes were present and hashed at intake;
2. public_pointer_attested: the public record is internally consistent, but CI cannot rebuild it;
3. numerically_reproduced: the result was independently recomputed (needs a reproduction record).
Author scientific acceptance is not a verification level: it is the record's review status, set
only by a human decision (explicit, or implicit through the round trip).
"""

from __future__ import annotations

import hashlib
import re
import stat
import zipfile
from pathlib import Path, PurePosixPath

from . import core

EVIDENCE_LAYERS = {"observation", "exact_result", "simulation_result", "inference", "interpretation", "negative_null", "question", "plan"}
VERIFICATION_LEVELS = {"local_source_verified", "public_pointer_attested", "numerically_reproduced"}
SOURCE_ROLES = {"primary_report", "run_ledger", "specification", "code", "result_table", "raw_array", "interpretation", "correction", "retrospective_baseline", "recovered_record", "future_question", "unknown"}
PRIVACY_DISPOSITIONS = {"unreviewed", "awaiting_publication_approval", "public_summary_approved", "withheld"}
CONSENT_KIND = "publication_consent"
NESTED_ARCHIVE_SUFFIXES = (".zip", ".tar", ".tgz", ".gz", ".bz2", ".xz", ".7z", ".rar", ".jar", ".whl")
EXECUTABLE_SUFFIXES = (".py", ".pyc", ".pyo", ".pkl", ".pickle", ".npy", ".npz", ".joblib", ".sh", ".exe", ".dll", ".so", ".bat", ".ps1")
MEDIA = {".md": "text/markdown", ".txt": "text/plain", ".json": "application/json", ".jsonl": "application/jsonl", ".csv": "text/csv", ".tsv": "text/tab-separated-values",
         ".py": "text/x-python", ".pyc": "application/x-python-bytecode", ".npy": "application/x-npy", ".npz": "application/x-npz", ".pdf": "application/pdf", ".png": "image/png",
         ".zip": "application/zip", ".html": "text/html", ".yaml": "text/yaml", ".yml": "text/yaml", ".tex": "text/x-tex", ".pkl": "application/x-pickle"}
MAX_TOTAL_UNCOMPRESSED = 2 * 1024**3
MAX_MEMBER_UNCOMPRESSED = 512 * 1024**2
MAX_RATIO = 200.0
MAX_SUMMARY_CHARS = 1200
MAX_QUOTE_CHARS = 160
HEX64 = re.compile(r"^[0-9a-f]{64}$")
LOCAL_ID = re.compile(r"^HIST::[A-Za-z0-9][A-Za-z0-9._-]*$")


class ArchiveError(Exception):
    pass


def findings_path(root: Path) -> Path:
    return root / "sources" / "historical" / "findings.jsonl"


def load_findings(root: Path) -> list[dict]:
    p = findings_path(root)
    return core.read_jsonl(p) if p.exists() else []


def load_intake_plan(root: Path) -> dict:
    p = root / "sources" / "historical" / "intake-plan.json"
    return core.read_json(p) if p.exists() else {}


def _sha256_stream(f) -> tuple[str, int]:
    h, n = hashlib.sha256(), 0
    for chunk in iter(lambda: f.read(1 << 20), b""):
        h.update(chunk)
        n += len(chunk)
    return h.hexdigest(), n


def unsafe_member_path(name: str) -> str | None:
    """Why a ZIP member path is unsafe to extract, or None."""
    if not name:
        return "empty path"
    if "\\" in name:
        return "backslash in path"
    if name.startswith("/") or re.match(r"^[A-Za-z]:", name):
        return "absolute path"
    parts = PurePosixPath(name).parts
    if any(part == ".." for part in parts):
        return "parent-directory traversal"
    if "\x00" in name:
        return "NUL in path"
    return None


def inventory_archive(path: Path, expected_sha256: str | None = None, expected_entries: int | None = None, archive_id: str | None = None) -> dict:
    """Inventory a ZIP without extracting it. Raises ArchiveError if it cannot be opened."""
    path = Path(path)
    if not path.is_file():
        raise ArchiveError(f"archive not accessible: {path}")
    with path.open("rb") as f:
        whole, size = _sha256_stream(f)
    rep = {"archive_id": archive_id or path.name, "file_name": path.name, "sha256": whole, "bytes": size,
           "expected_sha256": expected_sha256, "expected_entries": expected_entries, "problems": [], "warnings": [], "members": []}
    if expected_sha256 and whole != expected_sha256:
        rep["problems"].append(f"whole-file sha256 {whole} != expected {expected_sha256}: stop (do not use a different archive)")
    try:
        zf = zipfile.ZipFile(path)
    except zipfile.BadZipFile as exc:
        raise ArchiveError(f"not a readable ZIP: {exc}") from exc
    with zf:
        infos = zf.infolist()
        if expected_entries is not None and len(infos) != expected_entries:
            rep["problems"].append(f"{len(infos)} members != expected {expected_entries}")
        seen, seen_fold, total = {}, {}, 0
        for zi in infos:
            name = zi.filename
            m = {"path": name, "is_dir": zi.is_dir(), "compressed_bytes": zi.compress_size, "bytes": zi.file_size,
                 "zip_timestamp_metadata": "%04d-%02d-%02dT%02d:%02d:%02d" % zi.date_time,
                 "media_type": MEDIA.get(PurePosixPath(name).suffix.lower(), "application/octet-stream"),
                 "privacy_review": "unreviewed", "source_role": "unknown", "flags": []}
            why = unsafe_member_path(name)
            if why:
                m["flags"].append(f"unsafe_path: {why}")
                rep["problems"].append(f"{name!r}: unsafe path ({why})")
            if name in seen:
                m["flags"].append("duplicate_path")
                rep["problems"].append(f"{name!r}: duplicate member path")
            elif name.lower() in seen_fold:
                m["flags"].append("case_fold_duplicate")
                rep["warnings"].append(f"{name!r}: differs from {seen_fold[name.lower()]!r} only by case")
            seen[name] = True
            seen_fold.setdefault(name.lower(), name)
            mode = (zi.external_attr >> 16) & 0xFFFF
            if stat.S_ISLNK(mode):
                m["flags"].append("symlink")
                rep["problems"].append(f"{name!r}: symbolic link member")
            if zi.flag_bits & 0x1:
                m["flags"].append("encrypted")
                rep["warnings"].append(f"{name!r}: encrypted member (not read)")
            if name.lower().endswith(NESTED_ARCHIVE_SUFFIXES):
                m["flags"].append("nested_archive")
                rep["warnings"].append(f"{name!r}: nested archive (inventoried as bytes only, not opened)")
            if name.lower().endswith(EXECUTABLE_SUFFIXES):
                m["flags"].append("never_execute")
            if zi.file_size > MAX_MEMBER_UNCOMPRESSED or (zi.compress_size and zi.file_size / zi.compress_size > MAX_RATIO and zi.file_size > 1024**2):
                m["flags"].append("decompression_limit")
                rep["problems"].append(f"{name!r}: exceeds decompression limits ({zi.file_size} bytes, ratio {zi.file_size / max(zi.compress_size, 1):.0f})")
            total += zi.file_size
            if total > MAX_TOTAL_UNCOMPRESSED:
                rep["problems"].append("total uncompressed size exceeds the limit; inventory stopped")
                break
            if not zi.is_dir() and "symlink" not in m["flags"] and "encrypted" not in m["flags"] and "decompression_limit" not in m["flags"] and not why:
                with zf.open(zi) as mf:
                    digest, n = _sha256_stream(mf)
                m["sha256"] = digest
                if n != zi.file_size:
                    rep["problems"].append(f"{name!r}: read {n} bytes, header says {zi.file_size}")
            rep["members"].append(m)
    rep["member_count"] = len(infos)
    rep["ok"] = not rep["problems"]
    return rep


def inventory_digest(rep: dict) -> str:
    """Content hash of an inventory (path -> sha256), recorded in public attestations."""
    return core.sha256_bytes(core.canonical({m["path"]: m.get("sha256") for m in rep["members"]}).encode())


def write_private_inventory(rep: dict, out_dir: Path) -> Path:
    """Write an inventory outside the repository (refuses a path inside the Git working tree)."""
    out_dir = Path(out_dir).resolve()
    if out_dir == core.REPO.resolve() or core.REPO.resolve() in out_dir.parents:
        raise ArchiveError(f"private inventories must be written outside the repository ({out_dir})")
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / f"inventory-{rep['archive_id']}.json"
    core.write_json(p, rep)
    return p


def _expected(manifest: dict) -> dict[str, dict]:
    src = next((s for s in manifest["sources"] if s.get("source_key") == "HIST"), {})
    return {a["name"]: a for a in src.get("expected_archives", [])}


def hist_source(manifest: dict) -> dict:
    return next((s for s in manifest["sources"] if s.get("source_key") == "HIST"), {})


def finding_is_usable(f: dict) -> bool:
    """A finding may substantiate a HIST:: reference: source-verified at intake and approved for publication."""
    return (f.get("verification", {}).get("level") in ("local_source_verified", "numerically_reproduced")
            and f.get("privacy", {}).get("disposition") == "public_summary_approved"
            and f.get("review_status") not in ("rejected", None))


def validate_findings(manifest: dict, findings: list[dict], decisions: list[dict] | None = None) -> list[str]:
    p = []
    expected = _expected(manifest)
    src = hist_source(manifest)
    status = src.get("status")
    # publication consent is its own explicit human decision; round-trip acceptance is never consent
    consents = {d["decision_id"]: d for d in (decisions or []) if d.get("human") and d.get("kind") == CONSENT_KIND}
    if findings and status == "pending_intake":
        p.append("HIST is pending_intake: no historical finding may be registered until intake passes the custody gate")
    if status == "included_partial":
        verified = {a.get("name"): a for a in src.get("verified_archives", [])}
        for name, a in verified.items():
            if name not in expected or a.get("sha256") != expected[name]["sha256"]:
                p.append(f"HIST verified archive {name} does not match the expected archive hash")
        if not any(finding_is_usable(f) for f in findings):
            p.append("HIST is included_partial but has no source-verified, publication-approved finding")
    ids, by_exp = set(), {}
    for f in findings:
        fid = f.get("finding_id", "?")
        if not LOCAL_ID.match(str(fid)):
            p.append(f"{fid}: finding_id must look like HIST::<local-id>")
        if fid in ids:
            p.append(f"{fid}: duplicate finding_id")
        ids.add(fid)
        for k in ("archive_id", "archive_sha256", "member_path", "member_sha256", "anchor", "evidence_layer", "claim", "summary", "outcome", "limitations", "verification", "privacy", "review_status", "decision_history", "source_role", "provenance"):
            if k not in f:
                p.append(f"{fid}: missing {k}")
        arch = expected.get(f.get("archive_id"))
        if arch is None:
            p.append(f"{fid}: archive {f.get('archive_id')!r} is not an expected HIST archive")
        elif f.get("archive_sha256") != arch["sha256"]:
            p.append(f"{fid}: archive_sha256 does not match the expected digest of {f['archive_id']}")
        if not HEX64.match(str(f.get("member_sha256", ""))):
            p.append(f"{fid}: member_sha256 must be a sha256 hex digest")
        why = unsafe_member_path(str(f.get("member_path", "")))
        if why:
            p.append(f"{fid}: member_path is unsafe ({why})")
        if f.get("evidence_layer") not in EVIDENCE_LAYERS:
            p.append(f"{fid}: evidence_layer {f.get('evidence_layer')!r} must be one of {sorted(EVIDENCE_LAYERS)}")
        if f.get("source_role") not in SOURCE_ROLES:
            p.append(f"{fid}: source_role {f.get('source_role')!r} must be one of {sorted(SOURCE_ROLES)}")
        v = f.get("verification", {})
        lvl = v.get("level")
        if lvl not in VERIFICATION_LEVELS:
            p.append(f"{fid}: verification.level {lvl!r} must be one of {sorted(VERIFICATION_LEVELS)} (author acceptance is a review status, not a verification level)")
        if lvl in ("local_source_verified", "numerically_reproduced") and not (v.get("date") and HEX64.match(str(v.get("inventory_digest", "")))):
            p.append(f"{fid}: {lvl} needs verification.date and the inventory_digest of the intake inventory")
        if lvl == "numerically_reproduced" and not v.get("reproduction"):
            p.append(f"{fid}: numerically_reproduced needs a reproduction record")
        pr = f.get("privacy", {})
        if pr.get("disposition") not in PRIVACY_DISPOSITIONS:
            p.append(f"{fid}: privacy.disposition must be one of {sorted(PRIVACY_DISPOSITIONS)}")
        if pr.get("disposition") != "public_summary_approved":
            p.append(f"{fid}: a public historical record needs privacy approval (disposition public_summary_approved)")
        elif not pr.get("approved_by") or str(pr["approved_by"]).lower().startswith("agent") or pr.get("decision_id") not in consents:
            p.append(f"{fid}: privacy approval must be a logged human publication_consent decision (approved_by and decision_id in author-decisions); round-trip acceptance is not consent")
        else:
            c = consents[pr["decision_id"]]
            for field, limit in (c.get("limits") or {}).items():
                if len(str(f.get(field, ""))) > int(limit):
                    p.append(f"{fid}: {field} exceeds the {limit}-character limit of {c['decision_id']}")
            if f.get("member_path") in set(c.get("excluded_members") or []):
                p.append(f"{fid}: {f['member_path']} is excluded from publication by {c['decision_id']}")
        for k in ("summary", "claim"):
            text = str(f.get(k, ""))
            if len(text) > MAX_SUMMARY_CHARS:
                p.append(f"{fid}: {k} is longer than {MAX_SUMMARY_CHARS} characters; public records hold short derived summaries")
            for q in re.findall(r"\"([^\"]+)\"|“([^”]+)”", text):
                if len(q[0] or q[1]) > MAX_QUOTE_CHARS and not pr.get("quote_approved"):
                    p.append(f"{fid}: {k} quotes more than {MAX_QUOTE_CHARS} characters of source text without quote approval")
        if f.get("review_status") not in core.PROPOSAL_STATUSES:
            p.append(f"{fid}: review_status {f.get('review_status')!r}")
        hist = f.get("decision_history") or []
        if hist and hist[-1].get("status") != f.get("review_status"):
            p.append(f"{fid}: review_status must equal the last decision_history entry")
        if f.get("review_status") == "human_accepted" and not (hist and hist[-1].get("human")):
            p.append(f"{fid}: human_accepted needs a human decision")
        exp = f.get("experiment_id")
        if exp:
            by_exp.setdefault((f.get("archive_id"), exp), []).append(f)
    for (arch, exp), fs in by_exp.items():
        members = {f.get("member_sha256") for f in fs}
        if len(members) > 1:
            declared = {r for f in fs for r in (f.get("supersedes", []) + f.get("conflicts_with", []))}
            if not declared & {f.get("finding_id") for f in fs}:
                p.append(f"experiment {exp} in {arch}: findings cite different source files ({sorted(f['finding_id'] for f in fs)}) with no declared supersession or conflict")
    return p


def verify_local(manifest: dict, findings: list[dict], archive_dir: Path | None) -> dict:
    """Re-hash the members findings cite, if the private archives are present. Never reports a pass without bytes."""
    out = {"archives": {}, "members": [], "requires_private_input": []}
    expected = _expected(manifest)
    for name, a in expected.items():
        path = Path(archive_dir) / name if archive_dir else None
        if not path or not path.is_file():
            out["archives"][name] = "inaccessible"
            out["requires_private_input"].append(f"whole-file sha256 of {name}")
            continue
        with path.open("rb") as f:
            digest, _ = _sha256_stream(f)
        out["archives"][name] = "verified" if digest == a["sha256"] else "HASH_MISMATCH"
    for f in findings:
        name = f.get("archive_id")
        if out["archives"].get(name) != "verified":
            out["members"].append({"finding_id": f.get("finding_id"), "state": "requires_private_input"})
            out["requires_private_input"].append(f"{f.get('finding_id')}: {f.get('member_path')}")
            continue
        with zipfile.ZipFile(Path(archive_dir) / name) as zf:
            try:
                with zf.open(f["member_path"]) as mf:
                    digest, _ = _sha256_stream(mf)
                state = "verified" if digest == f["member_sha256"] else "DIGEST_MISMATCH"
            except KeyError:
                state = "MEMBER_MISSING"
        out["members"].append({"finding_id": f.get("finding_id"), "state": state})
    out["problems"] = [f"archive {k}: {v}" for k, v in out["archives"].items() if v == "HASH_MISMATCH"] + [f"{m['finding_id']}: {m['state']}" for m in out["members"] if m["state"] in ("DIGEST_MISMATCH", "MEMBER_MISSING")]
    return out
