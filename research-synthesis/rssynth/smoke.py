"""Operational smoke test: one complete hub cycle in a temporary copy, with no experiment and no upstream mutation.

Every step runs against a throwaway copy of research-synthesis/; the real tree is hashed before and
after to prove it is untouched. Git is read only.
"""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

from . import core, generate, historical, ledger, roundtrip, sources, workflow


def _tree_hash(root: Path) -> str:
    files = {str(p.relative_to(root)): core.sha256_file(p) for p in sorted(root.rglob("*")) if p.is_file() and "__pycache__" not in p.parts}
    return core.sha256_bytes(core.canonical(files).encode())


def run() -> dict:
    real = core.ROOT
    before = _tree_hash(real)
    tmp = Path(tempfile.mkdtemp(prefix="rssynth-smoke-"))
    steps: list[dict] = []

    def step(name: str, ok: bool, detail) -> None:
        steps.append({"step": name, "ok": bool(ok), "detail": detail})

    head_fn, anc_fn = sources.remote_branch_head, sources.is_ancestor
    try:
        dest = tmp / "research-synthesis"
        shutil.copytree(real, dest, ignore=shutil.ignore_patterns("__pycache__"))
        core.ROOT = dest
        m = sources.load_manifest()
        # 1. a closed programme milestone and its pinned provenance
        gt = next(s for s in m["sources"] if s["source_key"] == "GT")
        arts = [a for a in sources.verify_artifacts(m) if a["source"] == "GT"]
        step("closed milestone pinned and provenance verified",
             arts and all((a.get("copy") == "ok" or not a["materialised"]) and a.get("pin") in ("ok", "git_unavailable") for a in arts),
             {"source": "GT", "branch": gt.get("branch"), "commit": gt["commit"][:12], "artifacts": len(arts), "materialised_ok": sum(a.get("copy") == "ok" for a in arts)})
        # 2. draft an unapproved relation (through the normal seed intake)
        seeds = tmp / "seeds"
        seeds.mkdir()
        (seeds / "candidate-relations.jsonl").write_text(json.dumps({"from": "CL::F8N-KAC-CONTROL", "to": "GT::GT-F79-ND-MATCHES-EDGE-LIFETIME", "connection_type": "tested_structural_analogy", "scope": "smoke test only", "rationale": "smoke-test draft; never reviewed"}) + "\n")
        before_ledger = core.sha256_file(dest / "ledger" / "connections.jsonl")
        rep = workflow.intake_seeds(seeds, label="smoke")
        staged = core.read_jsonl(dest / "proposals" / "candidate-relations.jsonl")[-1]
        step("unapproved relation drafted as a proposal only", rep["candidate_relations"] == 1 and staged["status"] == "proposed" and core.sha256_file(dest / "ledger" / "connections.jsonl") == before_ledger,
             {"proposal": staged.get("proposal_id"), "status": staged["status"]})
        # 3. validation
        loaded = sources.load_sources(m)
        shared = ledger.load_shared(dest)
        probs = ledger.validate_all(m, loaded, shared) + roundtrip.validate(dest, shared) + historical.validate_findings(m, shared["hist_findings"], shared["author_decisions"])
        step("validation", not probs, probs[:5])
        # 4. generation twice, byte-identical; themed Markdown/Mermaid and graph.json present
        f1 = generate.build(*generate.load_inputs())
        f2 = generate.build(*generate.load_inputs())
        themes = [k for k in f1 if k.startswith("themes/")]
        step("deterministic generation (themes, Mermaid, graph.json)", f1 == f2 and "graph.json" in f1 and any(k.endswith(".mmd") for k in themes),
             {"files": len(f1), "theme_files": len(themes)})
        generate.write(f1)
        # 5. negative and null retention
        contra, nulls = f1.get("contradictions.md", ""), f1.get("nulls.md", "")
        rejected = [p["proposal_id"] for p in shared["proposals"] if p["status"] == "rejected"]
        step("negative and null records retained", rejected and all(r in contra or r in nulls for r in rejected) and len(nulls) > 200,
             {"rejected_shown": len(rejected), "nulls_chars": len(nulls)})
        # 6. snapshot and integrity
        try:
            lock = workflow.create_snapshot("smoke-cycle", "smoke cycle")
            step("snapshot written and verified", not workflow.verify_snapshots(), {"content_hash": lock["content_hash"][:16]})
        except Exception as exc:  # noqa: BLE001 - a smoke step reports failure instead of crashing
            step("snapshot written and verified", False, str(exc))
            raise
        snap_file = next(p for p in (dest / "snapshots" / "smoke-cycle").rglob("*.md"))
        original = snap_file.read_bytes()
        snap_file.write_bytes(original + b"tampered\n")
        tampered = workflow.verify_snapshots()
        snap_file.write_bytes(original)
        step("tampering detected", bool(tampered), tampered[:1])
        # 7. a later stale-head notification (simulated branch movement; nothing is followed)
        sources.remote_branch_head = lambda branch: ("f" * 40) if branch == gt.get("branch") else head_fn(branch)
        sources.is_ancestor = lambda a, b: True if b == "f" * 40 else anc_fn(a, b)
        st = {s["source"]: s["state"] for s in sources.staleness(m)}
        step("stale-head notification reported, pin unchanged", st.get("GT") == "behind_branch_head" and sources.load_manifest()["sources"] == m["sources"],
             {"GT": st.get("GT")})
    finally:
        sources.remote_branch_head, sources.is_ancestor = head_fn, anc_fn
        core.ROOT = real
        shutil.rmtree(tmp, ignore_errors=True)
    after = _tree_hash(real)
    step("real research-synthesis tree untouched", before == after, {"tree_hash": after[:16]})
    return {"ok": all(s["ok"] for s in steps), "steps": steps}
