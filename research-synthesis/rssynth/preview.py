"""Validated hypothetical intake in a discarded copy; never adopts a live pin."""

from pathlib import Path
import shutil
import tempfile

from . import core, generate, ledger, pins, sources, workflow


def preview_pins(proposal_paths, staged_candidates, staged_questions, output):
    original = core.ROOT
    output = Path(output).resolve()
    if not output.is_relative_to((original / "proposals/previews").resolve()):
        raise ValueError("preview output must be under proposals/previews, never canonical sources/generated")
    proposals = [core.read_json(Path(p)) for p in proposal_paths]
    candidates = core.read_jsonl(Path(staged_candidates))
    questions = core.read_jsonl(Path(staged_questions))
    guarded = [original / "sources/pin-spec.json", original / "sources/manifest.json"]
    before = {str(p): core.sha256_file(p) for p in guarded}
    with tempfile.TemporaryDirectory(prefix="rssynth-preview-") as tmp:
        dest = Path(tmp) / "research-synthesis"
        shutil.copytree(original, dest, ignore=shutil.ignore_patterns("__pycache__", "previews"))
        try:
            core.ROOT = dest
            spec = core.read_json(dest / "sources/pin-spec.json")
            for proposal in proposals:
                if proposal["status"] != "proposed":
                    raise ValueError("preview requires pending proposals, not a simulated adoption")
                commit = proposal["proposed_commit"]
                metadata = pins.checked_metadata(proposal["source_metadata"], commit)
                if core.sha256_bytes(core.canonical(metadata).encode()) != proposal["source_metadata_sha256"]:
                    raise ValueError("preview metadata digest mismatch")
                for source in spec["sources"]:
                    if source["source_key"] == proposal["source"]:
                        source.update(metadata)
                        source["commit"] = commit
            core.write_json(dest / "sources/pin-spec.json", spec)
            manifest = pins.build_manifest(by="agent: HYPOTHETICAL PREVIEW ONLY, no human adoption")
            pins.write_manifest(manifest)
            prop_path = dest / "proposals/candidate-relations.jsonl"
            props = core.read_jsonl(prop_path)
            known = {p["proposal_id"] for p in props}
            updates = {p["proposal_id"]: p for p in candidates}
            for old in props:
                new = updates.get(old["proposal_id"])
                if new and new.get("decision_history", [])[:len(old.get("decision_history", []))] != old.get("decision_history", []):
                    raise ValueError("staged reconciliation must preserve existing decision history")
            props = [updates.get(p["proposal_id"], p) for p in props]
            props += [p for p in candidates if p["proposal_id"] not in known]
            core.write_jsonl(prop_path, props)
            core.write_jsonl(dest / "ledger/questions.jsonl", questions)
            files = generate.build(*generate.load_inputs())
            generate.write(files)
            again = generate.build(*generate.load_inputs())
            if files != again:
                raise ValueError("hypothetical generation not deterministic")
            check = workflow.check(use_git=True, scope_base=None)
            if not check["ok"]:
                raise ValueError("preview validation failed: " + "; ".join(check["errors"]))
            lock = workflow.create_snapshot("hypothetical-cl8p-gtp011", "HYPOTHETICAL, NOT ADOPTED: CL8P and GT-P011")
            receipt = {"status": "VALIDATED_HYPOTHETICAL_NOT_ADOPTED", "human_pin_review": "pending",
                       "source_pins": {s["source_key"]: s.get("commit") for s in manifest["sources"]},
                       "check": check, "generated_twice_byte_identical": True,
                       "canonical_pins_unchanged": True, "before_hashes": before,
                       "view_sha256": {k: core.sha256_bytes(v.encode()) for k,v in files.items()}}
        finally:
            core.ROOT = original
    if before != {str(p): core.sha256_file(p) for p in guarded}:
        raise AssertionError("canonical pin files mutated by preview")
    output.mkdir(parents=True, exist_ok=True)
    core.write_json(output / "receipt.json", receipt)
    core.write_json(output / "hypothetical-manifest.json", manifest)
    core.write_json(output / "hypothetical-snapshot-lock.json", lock)
    for name, text in files.items():
        core.write_text(output / "views" / name, text)
    return receipt
