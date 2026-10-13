"""Coherence ledger contracts.

The JSONL files are the record. These tests check the schema and that the
generated views match those files. They do not score a finding.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from rs_constraint_lab.coherence import (
    SCORE_FIELDS,
    build_markdown,
    build_mermaid,
    load_ledger,
    snapshot_text,
    validate_ledger,
    write_snapshot,
)
from rs_constraint_lab.explore08a import repository_root

ROOT = repository_root() / "constraint-lab" / "coherence"


def test_committed_ledger_is_valid_and_views_match() -> None:
    findings, relations = load_ledger(ROOT)
    assert validate_ledger(findings, relations) == []
    assert (ROOT / "current-map.md").read_text(encoding="utf-8") == build_markdown(findings, relations)
    assert (ROOT / "current-map.mmd").read_text(encoding="utf-8") == build_mermaid(findings, relations)
    ids = [row["finding_id"] for row in findings]
    assert len(ids) == len(set(ids))
    relation_ids = [row["relation_id"] for row in relations]
    assert len(relation_ids) == len(set(relation_ids))
    assert "F008A-PLUGIN-INITIAL-MI" in ids
    historical = next(row for row in findings if row["finding_id"] == "F008A-PLUGIN-INITIAL-MI")
    assert historical["status"] == "historical_observation"


def test_dimensions_stay_separate_and_no_scalar_score_exists() -> None:
    findings, relations = load_ledger(ROOT)
    for row in findings:
        assert row["epistemic_layer"]
        assert row["magnitude_class"]
        assert isinstance(row["robustness_vector"], dict)
        assert set(row["robustness_vector"]) == {
            "exactness",
            "replication",
            "control_separation",
            "parameter_robustness",
            "projection_robustness",
        }
        assert not set(row) & SCORE_FIELDS
        if row["epistemic_layer"] == "OBSERVATION":
            assert row["evidence_refs"]
    for row in relations:
        assert not set(row) & SCORE_FIELDS
        assert row["rationale"]
    blob = (ROOT / "findings.jsonl").read_text(encoding="utf-8") + (ROOT / "relations.jsonl").read_text(encoding="utf-8")
    for name in SCORE_FIELDS:
        assert f'"{name}"' not in blob


def test_mermaid_uses_legal_ids_and_keeps_the_superseded_node() -> None:
    findings, relations = load_ledger(ROOT)
    mermaid = build_mermaid(findings, relations)
    assert "F001_PAIRWISE_RISE[" in mermaid
    assert "F008A_PLUGIN_INITIAL_MI[" in mermaid
    assert "supersedes_interpretation" in mermaid
    assert "subgraph OBSERVATION" in mermaid
    assert "subgraph OPEN_QUESTION" in mermaid


def test_snapshot_is_deterministic(tmp_path: Path) -> None:
    findings, relations = load_ledger(ROOT)
    (tmp_path / "findings.jsonl").write_text((ROOT / "findings.jsonl").read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "relations.jsonl").write_text((ROOT / "relations.jsonl").read_text(encoding="utf-8"), encoding="utf-8")
    first = snapshot_text(tmp_path, title="Through Generation 008C")
    second = snapshot_text(tmp_path, title="Through Generation 008C")
    assert first == second
    assert "canonical_ledger_sha256:" in first
    digest = write_snapshot(tmp_path, "through-generation-008c.md", "Through Generation 008C")
    again = write_snapshot(tmp_path, "through-generation-008c.md", "Through Generation 008C")
    assert digest == again
    stored = (tmp_path / "snapshots" / "through-generation-008c.md").read_text(encoding="utf-8")
    assert stored.startswith("# Through Generation 008C")
    assert len(findings) > 0 and len(relations) > 0


def test_schema_rejections() -> None:
    findings, relations = load_ledger(ROOT)
    scored = json.loads(json.dumps(findings[0]))
    scored["overall_score"] = 0.83
    assert any("scalar score" in item for item in validate_ledger([scored], []))
    bare = json.loads(json.dumps(findings[0]))
    bare["evidence_refs"] = []
    bare["epistemic_layer"] = "OBSERVATION"
    assert any("evidence" in item for item in validate_ledger([bare], []))
    broken = json.loads(json.dumps(relations[0]))
    broken["to_finding"] = "missing-node"
    assert any("missing finding" in item for item in validate_ledger(findings, [broken]))
    unknown = json.loads(json.dumps(relations[0]))
    unknown["relation_type"] = "proves"
    assert any("uncontrolled" in item for item in validate_ledger(findings, [unknown]))


def test_views_raise_on_an_invalid_ledger(tmp_path: Path) -> None:
    from rs_constraint_lab.coherence import CoherenceError, write_views

    (tmp_path / "findings.jsonl").write_text("{}\n", encoding="utf-8")
    (tmp_path / "relations.jsonl").write_text("", encoding="utf-8")
    with pytest.raises(CoherenceError):
        write_views(tmp_path)
