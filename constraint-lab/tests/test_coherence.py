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


GRADE_ASYMMETRY_STATEMENT = (
    "At m=1/4 the action slot has probability 1/21 and each other slot has probability 4/21. "
    "Total variation from the uniform six-slot law is 5/42. At m=4 the action slot has probability 4/9 "
    "and each other slot has probability 1/9. Total variation is 5/18. The ratio of those total variations "
    "is 7/3, which is also the ratio of the balanced informations' Jensen-Shannon terms and of the "
    "closed-form edge drifts. Five unweighted slots remain in the normalising total, so the reciprocal "
    "grades sit at different distances from uniformity."
)
DRIFT_DIRECTION_STATEMENT = (
    "Suppressing a dissolution raises expected edge count, favouring a dissolution lowers it, and "
    "suppressing a formation lowers it. The reweighted slot is a dissolution that would have removed an "
    "edge, or a formation that would have added one, and the grade moves the probability of that slot. "
    "This is the local sign of the Generation 8 sparse/dense occupancy axis. Unconditional rules move the "
    "balanced mean by twice the one-gate conditional mean, because the gate no longer switches the rule off. "
    "The sign does not determine how much stationary mass sits on each edge-count layer."
)


def test_generation_008d_corrections_keep_the_historical_statements() -> None:
    findings, relations = load_ledger(ROOT)
    by_id = {row["finding_id"]: row for row in findings}
    historical = by_id["F8C-GRADE-ASYMMETRY"]
    assert historical["statement"] == GRADE_ASYMMETRY_STATEMENT
    assert historical["status"] == "qualified"
    assert "7/3" in historical["statement"]
    drift = by_id["F8C-DRIFT-DIRECTION"]
    assert drift["statement"] == DRIFT_DIRECTION_STATEMENT
    assert drift["status"] == "qualified"
    assert drift["magnitude_class"] == "large"
    correction = by_id["F8D-CORRECT-GRADE-ASYMMETRY"]
    assert correction["status"] == "active"
    assert "information geometry" in correction["statement"].lower() or "Information geometry" in correction["statement"]
    scope = by_id["F8D-DRIFT-MAGNITUDE-SCOPE"]
    assert "F010-OCCUPANCY-AXIS" in scope["statement"]
    typed = {(row["relation_type"], row["from_finding"], row["to_finding"]) for row in relations}
    assert ("corrects", "F8D-CORRECT-GRADE-ASYMMETRY", "F8C-GRADE-ASYMMETRY") in typed
    assert ("qualifies", "F8D-DRIFT-MAGNITUDE-SCOPE", "F8C-DRIFT-DIRECTION") in typed
    markdown = build_markdown(findings, relations)
    mermaid = build_mermaid(findings, relations)
    assert "F8D-CORRECT-GRADE-ASYMMETRY" in markdown
    assert "F8D-DRIFT-MAGNITUDE-SCOPE" in markdown
    assert "F8D_CORRECT_GRADE_ASYMMETRY" in mermaid
    assert "corrects" in mermaid
    assert "F8C_GRADE_ASYMMETRY" in mermaid
    for row in findings:
        if row["epistemic_layer"] == "OBSERVATION":
            assert row["evidence_refs"]
        assert "overall_score" not in row


def test_generation_008d_composition_nodes_answer_the_open_questions() -> None:
    findings, relations = load_ledger(ROOT)
    by_id = {row["finding_id"]: row for row in findings}
    for question in ("Q-GATE-COMPOSITION", "Q-WEAK-GRADE"):
        assert by_id[question]["epistemic_layer"] == "OPEN_QUESTION"
        assert by_id[question]["status"] == "qualified"
        assert by_id[question]["created_generation"] == "008C"
    assert by_id["Q-META-CONSTRAINT"]["status"] == "unresolved"
    typed = {(row["relation_type"], row["from_finding"], row["to_finding"]) for row in relations}
    assert ("partially_answered_by", "Q-GATE-COMPOSITION", "F8D-ADDITIVE-FEATURE-GRAMMAR") in typed
    assert ("partially_answered_by", "Q-WEAK-GRADE", "F8D-WEAK-GRADE-SURFACE") in typed
    assert ("compatible_with", "F8D-COMPLEMENTARY-ELIMINATION", "F009-TWO-LEVEL-COLLAPSE") in typed
    assert ("raises_question", "F8D-NO-GATE-PRODUCT", "Q-META-CONSTRAINT") in typed
    layers = {row["epistemic_layer"] for row in findings if row["created_generation"] == "008D"}
    assert {"OBSERVATION", "INFERENCE", "RS_GLOBAL_COHERENCE_INTERPRETATION", "OPEN_QUESTION", "METHODOLOGICAL"} <= layers
    for row in findings:
        if row["created_generation"] == "008D" and row["epistemic_layer"] == "OBSERVATION":
            assert any(ref.startswith("constraint-lab/reports/") for ref in row["evidence_refs"])
    markdown = build_markdown(findings, relations)
    assert "F8D-NO-GATE-PRODUCT" in markdown
    assert "Q-META-CONSTRAINT" in markdown


def test_generation_008e_scope_correction_qualifies_without_rewriting() -> None:
    findings, relations = load_ledger(ROOT)
    by_id = {row["finding_id"]: row for row in findings}
    for node in ("F8D-NO-GATE-PRODUCT", "F8D-ADDITIVE-FEATURE-GRAMMAR", "F8D-RS-COMPOSITIONAL-BOUND"):
        assert by_id[node]["status"] == "qualified"
        assert by_id[node]["created_generation"] == "008D"
    assert "no independent conjunction coefficient exists" in by_id["F8D-NO-GATE-PRODUCT"]["statement"]
    assert by_id["Q-META-CONSTRAINT"]["status"] == "unresolved"
    assert by_id["Q-K3-CONJUNCTION"]["epistemic_layer"] == "OPEN_QUESTION"
    assert by_id["F8E-K2-SCOPE-CORRECTION"]["status"] == "active"
    typed = {(row["relation_type"], row["from_finding"], row["to_finding"]) for row in relations}
    assert ("raises_question", "F8E-K2-SCOPE-CORRECTION", "Q-K3-CONJUNCTION") in typed
    assert ("qualifies", "F8E-K2-SCOPE-CORRECTION", "F8D-NO-GATE-PRODUCT") in typed
    assert ("raises_question", "F8D-NO-GATE-PRODUCT", "Q-META-CONSTRAINT") in typed
    markdown = build_markdown(findings, relations)
    assert "F8E-K2-SCOPE-CORRECTION" in markdown and "Q-K3-CONJUNCTION" in markdown
