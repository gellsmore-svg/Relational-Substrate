"""Shared primitives: paths, canonical JSON, hashing, vocabularies and namespaced references.

Everything here is deterministic and uses the standard library only.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # research-synthesis/
REPO = ROOT.parent

# --- vocabularies -------------------------------------------------------------

# Upstream (programme) coherence vocabulary, read from the pinned coherence.py
# blob 1fc80911d9 shared by CL 8G, CL 8N and GT. The adapter checks that the
# pinned validator still has this blob before trusting these sets.
UPSTREAM_LAYERS = {"OBSERVATION", "INFERENCE", "RS_GLOBAL_COHERENCE_INTERPRETATION", "METHODOLOGICAL", "OPEN_QUESTION"}
UPSTREAM_STATUSES = {"active", "qualified", "superseded", "unresolved", "historical_observation"}

# Shared-layer node kinds. Kept disjoint so source findings, cross-programme
# interpretation, formal claims, open questions and metaphors never blur.
NODE_KINDS = {"source_finding", "formal_claim", "source_question", "concept", "connection", "shared_question", "metaphor", "source_document"}

# Scientific connection types (cross-programme). Ordered roughly by strength.
CONNECTION_TYPES = {
    "exact_theorem_correspondence",  # same formal object and statement under stated maps
    "tested_structural_analogy",  # declared map between formal objects, checked on both sides
    "common_definition",  # both programmes define the same quantity the same way
    "shared_implementation_assumption",  # common code/kernel/validator lineage, not evidence
    "epistemic_compatibility",  # claims can both hold; no shared mechanism asserted
    "explicit_contrast",  # claims differ in a stated, checkable way
    "qualifies",  # one claim limits the scope of the other
    "supersedes_interpretation",  # a later reading replaces an earlier one (directed)
    "untested_hypothesis",  # a proposed bridge with no check yet
    "instance_of_theme",  # a finding is an instance of a shared concept/theme
}
EVIDENTIAL_CONNECTION_TYPES = {"exact_theorem_correspondence", "tested_structural_analogy", "common_definition"}

# Review statuses. Only these may appear in ledger/connections.jsonl.
LEDGER_REVIEW_STATUSES = {"agent_reviewed", "human_accepted", "rejected", "undetermined", "under_review"}
PROPOSAL_STATUSES = {"proposed", "under_review", "agent_reviewed", "rejected", "undetermined", "human_accepted"}
INDEPENDENCE = {"independent", "shared_lineage", "same_source", "unknown"}
COMPARISON_DIMENSIONS = ("state", "transition_law", "support", "clock", "projection", "intervention", "horizon", "conditioning")

QUESTION_STATUSES = {"open", "partially_answered", "answered", "retired", "pending_source"}

# Metaphor layer: link types are disjoint from every scientific type.
METAPHOR_LINK_TYPES = {"covers_concept", "illustrates_relation", "bridges_metaphors", "complements", "conflicts_with", "fails_for", "requires_qualification"}
METAPHOR_STATUSES = {"draft", "agent_reviewed", "human_accepted", "retired"}
METAPHOR_REQUIRED = ("metaphor_id", "title", "audience", "concepts", "mapping", "explanation", "does_not_mean", "misleading_readings", "illustrative_status", "review", "status", "evidentiary")
# Words that would smuggle metric, locality, agency or mechanical force into the primitive substrate
# when used without qualification in a metaphor's mapping.
SMUGGLING_TERMS = ("distance", "space", "force", "push", "pull", "wants", "tries", "decides", "intends", "moves through", "travels", "attracts", "gravity")

SOURCE_STATUSES = {"included", "catalogued_only", "lineage_only", "missing", "pending_intake"}

assert not (METAPHOR_LINK_TYPES & CONNECTION_TYPES)

# --- references ---------------------------------------------------------------

REF_RE = re.compile(r"^(?P<ns>[A-Z][A-Z0-9-]*)(?:@(?P<rev>[A-Za-z0-9._-]+))?::(?P<local>[A-Za-z0-9._:#/+-]+)$")
SHARED_NAMESPACES = {"C": "concept", "X": "connection", "XQ": "shared_question", "M": "metaphor", "P": "proposal"}


def parse_ref(ref: str) -> dict:
    """Split 'NS[@REV]::LOCAL'. Raises ValueError on malformed refs."""
    m = REF_RE.match(ref)
    if not m:
        raise ValueError(f"malformed reference {ref!r}")
    return {"namespace": m.group("ns"), "revision": m.group("rev"), "local": m.group("local")}


# --- canonical JSON and hashing ------------------------------------------------


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(Path(path).read_bytes())


def git_blob_id(data: bytes) -> str:
    """The git object id of a blob with these bytes (independent of git itself)."""
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    path = Path(path)
    if not path.exists():
        return []
    rows = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{n}: invalid JSON ({exc})") from exc
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(canonical(r) + "\n" for r in rows), encoding="utf-8")


def read_json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, obj) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
