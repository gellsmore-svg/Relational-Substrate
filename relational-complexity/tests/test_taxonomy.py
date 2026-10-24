"""The composition taxonomy is a library note. It does not run a cell."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE = (ROOT / "docs" / "composition-taxonomy.md").read_text(encoding="utf-8")

OPEN_ROWS = (
    "IDEA-L01",
    "IDEA-L04",
    "IDEA-L06",
    "IDEA-L09",
    "IDEA-L11",
    "IDEA-L13",
    "IDEA-L15",
    "IDEA-L17",
)
PARTIAL_ROWS = ("IDEA-L08", "IDEA-L14", "IDEA-L16")
UNCHANGED_EXPLORED = ("IDEA-L02", "IDEA-L03", "IDEA-L05", "IDEA-L07")


def _rows(name: str) -> list[dict]:
    path = ROOT / "atlas" / name
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_four_readings_and_eight_families_are_formulated():
    for heading in (
        "### Relational dependency",
        "### Relational reach",
        "### Relational composition",
        "### Relational recursion",
    ):
        assert heading in NOTE
    for index in range(1, 9):
        assert f"## C{index} " in NOTE
    assert "No scientific cell is attached to this note." in NOTE
    assert "Associativity is undefined" in NOTE
    assert "Six levels of composition are not a target." in NOTE
    assert "placeholder experiment" in NOTE


def test_new_idea_rows_stay_open_and_old_rows_keep_their_status():
    ideas = {row["idea_id"]: row for row in _rows("ideas.jsonl")}
    assert len(ideas) == len(_rows("ideas.jsonl"))
    for idea_id in OPEN_ROWS:
        assert ideas[idea_id]["status"] == "open"
    for idea_id in PARTIAL_ROWS:
        assert ideas[idea_id]["status"] == "partial"
    assert "src/rrc/composition.py" in ideas["IDEA-L16"]["methods"]
    assert "independent bit" in ideas["IDEA-L16"]["methods"]
    for idea_id in UNCHANGED_EXPLORED:
        assert ideas[idea_id]["status"] == "explored"
    assert ideas["IDEA-G01"]["status"] == "partial"
    for idea_id in ("IDEA-L15", "IDEA-L16", "IDEA-L17"):
        assert "docs/composition-taxonomy.md" in ideas[idea_id]["formulation"]
        assert idea_id in NOTE
    assert "IDEA-L05" in ideas["IDEA-L16"]["related"]
    assert "IDEA-G01" in ideas["IDEA-L16"]["related"]


def test_composition_coverage_stays_open_and_questions_are_not_closed():
    coverage = {row["coverage_id"]: row for row in _rows("coverage.jsonl")}
    for coverage_id in ("COV-COMPOSITION", "COV-COMPOSITION-LIBRARY"):
        assert coverage[coverage_id]["status"] == "open"
        assert "docs/composition-taxonomy.md" in coverage[coverage_id]["notes"]
    questions = {row["question_id"]: row for row in _rows("questions.jsonl")}
    for index in range(1, 13):
        assert questions[f"ATLAS-Q{index:02d}"]["status"] == "open"
    assert "second application become undefined" in questions["ATLAS-Q12"]["statement"]
