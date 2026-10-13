"""Deterministic views of the coherence ledger.

``findings.jsonl`` and ``relations.jsonl`` are the record. Markdown and
Mermaid are generated from them. A finding is not given a scalar score.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

EPISTEMIC_LAYERS = {
    "OBSERVATION",
    "INFERENCE",
    "RS_GLOBAL_COHERENCE_INTERPRETATION",
    "METHODOLOGICAL",
    "OPEN_QUESTION",
}
MAGNITUDE_CLASSES = {
    "zero_within_floor",
    "very_small",
    "small",
    "moderate",
    "large",
    "very_large",
    "not_applicable",
}
TEMPORAL_CHARACTERS = {
    "instantaneous",
    "local",
    "transient",
    "finite_horizon_integrated",
    "persistent",
    "stationary",
    "unknown",
    "not_applicable",
}
STRUCTURAL_ROLES = {
    "gate",
    "bias",
    "memory",
    "forgetting",
    "routing",
    "shape_selection",
    "occupancy_shift",
    "support_boundary",
    "dissolution_enabler",
    "formation_enabler",
    "normalisation_effect",
    "projection_loss",
    "equivalence",
    "symmetry",
    "interaction",
    "methodological_correction",
    "expressiveness",
    "negative_finding",
    "open_question",
    "unknown",
}
ROBUSTNESS_KEYS = (
    "exactness",
    "replication",
    "control_separation",
    "parameter_robustness",
    "projection_robustness",
)
RELATION_TYPES = {
    "supports",
    "undermines",
    "refines",
    "qualifies",
    "bounds",
    "explains",
    "depends_on",
    "derived_from",
    "contrasts_with",
    "is_equivalent_to",
    "is_projection_of",
    "is_coarse_graining_of",
    "supersedes_interpretation",
    "compatible_with",
    "raises_question",
    "motivates",
    "raised_by",
    "motivated_by",
    "partially_answered_by",
    "enables",
    "corrects",
}
STATUSES = {"active", "qualified", "superseded", "unresolved", "historical_observation"}
SCORE_FIELDS = {
    "overall_confidence",
    "overall_score",
    "finding_strength",
    "coherence_score",
    "strength_score",
    "master_score",
}
VISIBLE_STATUSES = {"active", "qualified", "unresolved"}


class CoherenceError(ValueError):
    """The ledger does not match its schema."""


def ledger_dir(root: Path | None = None) -> Path:
    if root is not None:
        return root
    return Path(__file__).resolve().parents[2] / "coherence"


def _load_jsonl(path: Path) -> list[dict]:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise CoherenceError(f"{path.name}:{line_number} is not JSON") from exc
    return rows


def load_ledger(root: Path | None = None) -> tuple[list[dict], list[dict]]:
    directory = ledger_dir(root)
    return _load_jsonl(directory / "findings.jsonl"), _load_jsonl(directory / "relations.jsonl")


def validate_ledger(findings: list[dict], relations: list[dict]) -> list[str]:
    problems = []
    finding_ids = [row.get("finding_id") for row in findings]
    if len(finding_ids) != len(set(finding_ids)):
        problems.append("finding ids are not unique")
    relation_ids = [row.get("relation_id") for row in relations]
    if len(relation_ids) != len(set(relation_ids)):
        problems.append("relation ids are not unique")
    known = set(finding_ids)
    for row in findings:
        if set(row) & SCORE_FIELDS:
            problems.append(f"{row.get('finding_id')} carries a scalar score")
        layer = row.get("epistemic_layer")
        if layer not in EPISTEMIC_LAYERS:
            problems.append(f"{row.get('finding_id')} has no recognised epistemic layer")
        if row.get("magnitude_class") not in MAGNITUDE_CLASSES:
            problems.append(f"{row.get('finding_id')} has no magnitude class")
        if row.get("temporal_character") not in TEMPORAL_CHARACTERS:
            problems.append(f"{row.get('finding_id')} has no temporal character")
        if row.get("status") not in STATUSES:
            problems.append(f"{row.get('finding_id')} has no status")
        robustness = row.get("robustness_vector")
        if not isinstance(robustness, dict) or set(robustness) != set(ROBUSTNESS_KEYS):
            problems.append(f"{row.get('finding_id')} robustness vector is missing or summed")
        elif any(type(robustness[key]) is not int or not 0 <= robustness[key] <= 5 for key in ROBUSTNESS_KEYS):
            problems.append(f"{row.get('finding_id')} robustness coordinate is outside 0–5")
        roles = row.get("structural_roles")
        if not isinstance(roles, list) or any(role not in STRUCTURAL_ROLES for role in roles):
            problems.append(f"{row.get('finding_id')} has an unknown structural role")
        if layer == "OBSERVATION" and not row.get("evidence_refs"):
            problems.append(f"{row.get('finding_id')} observation has no evidence reference")
        if not row.get("statement"):
            problems.append(f"{row.get('finding_id')} has an empty statement")
    for row in relations:
        if set(row) & SCORE_FIELDS:
            problems.append(f"{row.get('relation_id')} carries a scalar score")
        if row.get("relation_type") not in RELATION_TYPES:
            problems.append(f"{row.get('relation_id')} uses an uncontrolled relation")
        if row.get("from_finding") not in known or row.get("to_finding") not in known:
            problems.append(f"{row.get('relation_id')} names a missing finding")
        if not row.get("rationale"):
            problems.append(f"{row.get('relation_id')} has no rationale")
    return problems


def _relations_for(finding_id: str, relations: list[dict]) -> str:
    parts = []
    for row in relations:
        if row["from_finding"] == finding_id:
            parts.append(f"{row['relation_type']} → {row['to_finding']}")
        elif row["to_finding"] == finding_id:
            parts.append(f"{row['from_finding']} {row['relation_type']} →")
    return "; ".join(parts)


def _literal(value) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def build_markdown(findings: list[dict], relations: list[dict]) -> str:
    lines = [
        "# Current coherence map",
        "",
        "Generated from `findings.jsonl` and `relations.jsonl`. Magnitude, robustness, and temporal character stay in separate columns. There is no summed score.",
        "",
        "| ID | Layer | Finding | Literal value | Magnitude | Temporal character | Robustness vector | Structural role | Status | Key relations | Generation |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in findings:
        robustness = row["robustness_vector"]
        vector = "[" + ", ".join(str(robustness[key]) for key in ROBUSTNESS_KEYS) + "]"
        cells = [
            row["finding_id"],
            row["epistemic_layer"],
            row["statement"].replace("|", "/"),
            _literal(row.get("literal_value")).replace("|", "/"),
            row["magnitude_class"],
            row["temporal_character"],
            vector,
            ", ".join(row["structural_roles"]),
            row["status"],
            _relations_for(row["finding_id"], relations).replace("|", "/"),
            row["created_generation"],
        ]
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    return "\n".join(lines)


def _visible_ids(findings: list[dict], relations: list[dict]) -> set[str]:
    visible = {
        row["finding_id"]
        for row in findings
        if row["status"] in VISIBLE_STATUSES or row["epistemic_layer"] == "OPEN_QUESTION"
    }
    for row in relations:
        if row["relation_type"] == "supersedes_interpretation":
            visible.add(row["from_finding"])
            visible.add(row["to_finding"])
    return visible


def _mermaid_label(row: dict) -> str:
    text = row["statement"].replace('"', "'").replace("\n", " ")
    if len(text) > 90:
        text = text[:87] + "..."
    return text


def _node_id(finding_id: str) -> str:
    return finding_id.replace("-", "_")


def build_mermaid(findings: list[dict], relations: list[dict]) -> str:
    visible = _visible_ids(findings, relations)
    by_layer: dict[str, list[dict]] = {layer: [] for layer in (
        "OBSERVATION",
        "INFERENCE",
        "METHODOLOGICAL",
        "RS_GLOBAL_COHERENCE_INTERPRETATION",
        "OPEN_QUESTION",
    )}
    for row in findings:
        if row["finding_id"] in visible:
            by_layer[row["epistemic_layer"]].append(row)
    titles = {
        "OBSERVATION": "Observed dynamics",
        "INFERENCE": "Inferences",
        "METHODOLOGICAL": "Methodological corrections",
        "RS_GLOBAL_COHERENCE_INTERPRETATION": "RS and global-coherence interpretations",
        "OPEN_QUESTION": "Open questions",
    }
    lines = [
        "%% Generated from findings.jsonl and relations.jsonl.",
        "%% Historical nodes appear when a later finding supersedes their interpretation.",
        "flowchart TD",
    ]
    for layer, title in titles.items():
        rows = by_layer[layer]
        if not rows:
            continue
        lines.append(f"  subgraph {layer} [{title}]")
        for row in rows:
            lines.append(f'    {_node_id(row["finding_id"])}["{row["finding_id"]}: {_mermaid_label(row)}"]')
        lines.append("  end")
    for row in relations:
        if row["from_finding"] in visible and row["to_finding"] in visible:
            lines.append(f"  {_node_id(row['from_finding'])} -->|{row['relation_type']}| {_node_id(row['to_finding'])}")
    lines.append("")
    return "\n".join(lines)


def canonical_ledger_bytes(root: Path | None = None) -> bytes:
    directory = ledger_dir(root)
    findings = (directory / "findings.jsonl").read_bytes().rstrip(b"\n")
    relations = (directory / "relations.jsonl").read_bytes().rstrip(b"\n")
    return findings + b"\n" + relations + b"\n"


def snapshot_text(root: Path | None = None, *, title: str) -> str:
    findings, relations = load_ledger(root)
    problems = validate_ledger(findings, relations)
    if problems:
        raise CoherenceError("; ".join(problems))
    digest = hashlib.sha256(canonical_ledger_bytes(root)).hexdigest()
    body = build_markdown(findings, relations)
    return (
        f"# {title}\n\n"
        "Immutable generated view. The canonical record is `findings.jsonl` and `relations.jsonl`.\n\n"
        f"canonical_ledger_sha256: `{digest}`\n\n"
        + body
    )


def write_views(root: Path | None = None) -> dict:
    directory = ledger_dir(root)
    findings, relations = load_ledger(directory)
    problems = validate_ledger(findings, relations)
    if problems:
        raise CoherenceError("; ".join(problems))
    markdown = build_markdown(findings, relations)
    mermaid = build_mermaid(findings, relations)
    (directory / "current-map.md").write_text(markdown, encoding="utf-8")
    (directory / "current-map.mmd").write_text(mermaid, encoding="utf-8")
    return {
        "findings": len(findings),
        "mermaid_sha256": hashlib.sha256(mermaid.encode("utf-8")).hexdigest(),
        "markdown_sha256": hashlib.sha256(markdown.encode("utf-8")).hexdigest(),
        "relations": len(relations),
    }


def write_snapshot(root: Path | None, name: str, title: str) -> str:
    directory = ledger_dir(root)
    text = snapshot_text(directory, title=title)
    path = directory / "snapshots" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
