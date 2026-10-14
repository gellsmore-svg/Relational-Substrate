"""GT-E0 published records: frozen-plan chronology, table hashes, frozen outcomes, ledger and atlas."""

from __future__ import annotations

import json

from rs_constraint_lab.durable import canonical_json, sha256_bytes
from rs_constraint_lab.explore08a import repository_root, verify_journey_chronology

REPO = repository_root()
E0A_PLAN = "2e5c97e3fdb1f5b2ed18ae652ab6af9f391efdf7"
E0A_RESULT = "c31ef92aaf6e5299b9cb15bd7b5c10e768d65f43"
E0B_PLAN = "50c4b2cb01813fb71d0e4702657fccfbf1535e94"
E0B_RESULT = "d99f97280d42be92f690f53c9152096688076313"


def _tables(name: str) -> dict:
    return json.loads((REPO / "gravity-time" / "reports" / name).read_text(encoding="utf-8"))


def test_e0_results_descend_from_their_frozen_plans() -> None:
    reports = verify_journey_chronology(REPO, REPO / "gravity-time" / "plans" / "journey.jsonl")
    pairs = {(r["frozen_plan_commit"], r["result_commit"]) for r in reports}
    assert (E0A_PLAN, E0A_RESULT) in pairs and (E0B_PLAN, E0B_RESULT) in pairs


def test_e0_table_payload_hashes_and_plan_hashes() -> None:
    for name, plan_rel, payload in (("round-e0a-tables.json", "round-e0a-plan.json", "18fa301bb93ce180d73edfd0e3a9c3a424ddb834a8d8491c03de4eac721e98cf"), ("round-e0b-tables.json", "round-e0b-plan.json", "f02c7c9592a6fa2b82f5b7d500b4f0d026cb735260a8675d950d3c5ff154cb80")):
        body = _tables(name)
        assert body["payload_sha256"] == payload
        assert sha256_bytes(canonical_json({k: v for k, v in body.items() if k != "payload_sha256"}).encode("utf-8")) == payload
        plan = json.loads((REPO / "gravity-time" / "plans" / plan_rel).read_text(encoding="utf-8"))
        assert body["plan_hash"] == plan["plan_hash"] and body["validation"]["ok"]


def test_e0_frozen_outcomes_are_recorded_as_computed() -> None:
    e0a = _tables("round-e0a-tables.json")["frozen_expectations"]
    failed = sorted(k for k, v in e0a.items() if not v["holds"])
    assert failed == ["X4-FREE-N6-PATHF-weak_favour", "X4-FREE-N6-PATHH-weak_suppress", "X4-HELD-N6-PATHF-weak_favour", "X4-HELD-N6-PATHH-weak_suppress"]
    e0b = _tables("round-e0b-tables.json")["frozen_expectations"]
    assert all(v["holds"] for v in e0b.values()) and len(e0b) == 48


def test_gt_coherence_ledger_after_e0() -> None:
    from rs_constraint_lab.coherence import build_markdown, build_mermaid, load_ledger, validate_ledger

    root = REPO / "gravity-time" / "coherence"
    findings, relations = load_ledger(root)
    assert validate_ledger(findings, relations) == []
    assert (root / "current-map.md").read_text(encoding="utf-8") == build_markdown(findings, relations)
    assert (root / "current-map.mmd").read_text(encoding="utf-8") == build_mermaid(findings, relations)
    ids = {row["finding_id"] for row in findings}
    assert {"GT-F12-SINGLE-WITNESS-REVERSIBLE", "GT-F14-SATURATION-HIDES-ARROW", "GT-F26-SELECTIVE-BASIN-WITH-ARROW", "GT-Q07-COEXISTENCE-SCALING"} <= ids
    assert "GT-F01-DENS-NULL" in ids and all("overall_score" not in row for row in findings)


def test_atlas_lists_every_executed_cell() -> None:
    text = (REPO / "gravity-time" / "reports" / "gt-e0-atlas.md").read_text(encoding="utf-8")
    for name in ("round-e0a-tables.json", "round-e0b-tables.json"):
        for key in _tables(name)["results"]:
            assert f"| {key} |" in text
