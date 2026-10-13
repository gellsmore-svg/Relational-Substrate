"""Validated, deterministic views of the formal statement catalogue."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from rs_constraint_lab.coherence import SCORE_FIELDS, load_ledger

STATUSES = {
    "ALGEBRAIC_THEOREM", "FINITE_EXHAUSTIVE_RESULT", "NUMERICAL_KERNEL_RESULT",
    "MODEL_INFERENCE", "METHODOLOGICAL_PRINCIPLE", "OPEN_CONJECTURE", "OPEN_QUESTION",
}
REQUIRED = {
    "theorem_id", "title", "status", "statement", "assumptions", "scope",
    "proof_or_verification", "source_generations", "evidence_refs", "coherence_refs",
    "counterexample_scope", "dependencies", "notes",
}


class FormalError(ValueError):
    """Invalid catalogue or a stale generated view."""


def repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _jsonl(path: Path) -> list[dict]:
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise FormalError(f"{path}:{number}: invalid JSON") from exc
        if not isinstance(row, dict):
            raise FormalError(f"{path}:{number}: expected an object")
        rows.append(row)
    return rows


def load_catalog(root: Path | None = None) -> list[dict]:
    root = root or repository_root()
    return _jsonl(root / "constraint-lab/formal/theorem-catalog.jsonl")


def _check_reference(root: Path, reference: str) -> bool:
    if not isinstance(reference, str) or not reference:
        return False
    path, _, anchor = reference.partition("#")
    target = (root / path).resolve()
    if not target.is_relative_to(root.resolve()) or not target.is_file():
        return False
    if anchor:
        return f'<a id="{anchor}"></a>' in target.read_text(encoding="utf-8")
    return True


def validate_catalog(rows: list[dict], root: Path | None = None) -> list[str]:
    root = root or repository_root()
    problems = []
    identifiers = [r.get("theorem_id") for r in rows]
    known = {i for i in identifiers if isinstance(i, str)}
    if len(known) != len(identifiers):
        problems.append("theorem ids missing or not unique")
    findings, _relations = load_ledger(root / "constraint-lab/coherence")
    coherence_ids = {r["finding_id"] for r in findings}
    by_id = {r["theorem_id"]: r for r in rows if isinstance(r.get("theorem_id"), str)}
    for finding in findings:
        refs = finding.get("formal_refs", [])
        if not isinstance(refs, list) or any(not isinstance(ref, str) for ref in refs):
            problems.append(f"{finding['finding_id']}: invalid formal_refs")
            continue
        for ref in refs:
            if ref not in known:
                problems.append(f"{finding['finding_id']}: unknown formal ref {ref}")
            elif finding["finding_id"] not in by_id[ref].get("coherence_refs", []):
                problems.append(f"{ref}: missing reciprocal formal coherence link")
    graph = {}
    for row in rows:
        identifier = row.get("theorem_id")
        label = str(identifier)
        if not isinstance(identifier, str) or not re.fullmatch(r"CL-[TFNIMQ][0-9]{2}", identifier):
            problems.append(f"{label}: invalid namespaced id")
        if REQUIRED - row.keys():
            problems.append(f"{label}: missing schema fields")
        if row.keys() & SCORE_FIELDS:
            problems.append(f"{label}: scalar score forbidden")
        if row.get("status") not in STATUSES:
            problems.append(f"{label}: invalid status")
        for field in ("title", "statement", "scope", "counterexample_scope"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                problems.append(f"{label}: empty {field}")
        for field in ("assumptions", "source_generations", "evidence_refs", "coherence_refs", "dependencies"):
            values = row.get(field)
            if not isinstance(values, list) or any(not isinstance(v, str) for v in values):
                problems.append(f"{label}: {field} must be a string list")
                continue
            if field != "dependencies" and not values:
                problems.append(f"{label}: empty {field}")
        evidence = row.get("evidence_refs", [])
        for ref in evidence if isinstance(evidence, list) else []:
            if not _check_reference(root, ref):
                problems.append(f"{label}: missing evidence {ref}")
        coherence = row.get("coherence_refs", [])
        for ref in coherence if isinstance(coherence, list) else []:
            if not isinstance(ref, str) or ref not in coherence_ids:
                problems.append(f"{label}: unknown coherence id {ref}")
        dependencies = row.get("dependencies", [])
        if isinstance(dependencies, list) and isinstance(identifier, str):
            graph[identifier] = [d for d in dependencies if isinstance(d, str)]
            for dependency in graph[identifier]:
                if dependency not in known:
                    problems.append(f"{label}: unknown dependency {dependency}")
        proof = row.get("proof_or_verification")
        if not isinstance(proof, dict):
            problems.append(f"{label}: proof/verification must be an object")
            continue
        status = row.get("status")
        if status == "ALGEBRAIC_THEOREM":
            if not proof.get("proof_sketch") or not row.get("assumptions"):
                problems.append(f"{label}: theorem needs assumptions and proof")
            if not _check_reference(root, proof.get("derivation_ref", "")):
                problems.append(f"{label}: missing derivation")
        if status == "FINITE_EXHAUSTIVE_RESULT":
            if not proof.get("enumerated_domain") or type(proof.get("exact_count")) is not int or proof["exact_count"] <= 0:
                problems.append(f"{label}: exhaustive result needs domain and positive exact count")
            if not _check_reference(root, proof.get("verification_implementation", "")):
                problems.append(f"{label}: missing exhaustive verifier")
        if status == "NUMERICAL_KERNEL_RESULT":
            if not proof.get("method") or not proof.get("domain") or not isinstance(proof.get("tolerances"), dict) or not proof["tolerances"]:
                problems.append(f"{label}: numerical result needs method, domain and tolerances")
        if status in {"OPEN_CONJECTURE", "OPEN_QUESTION"}:
            if proof.get("resolution") != "open" or proof.get("proof_sketch") or proof.get("proved"):
                problems.append(f"{label}: open statement masquerades as proved")

    visiting, finished = set(), set()

    def visit(identifier: str) -> None:
        if identifier in visiting:
            problems.append(f"{identifier}: dependency cycle")
            return
        if identifier in finished:
            return
        visiting.add(identifier)
        for dependency in graph.get(identifier, []):
            if dependency in known:
                visit(dependency)
        visiting.remove(identifier)
        finished.add(identifier)

    for identifier in known:
        visit(identifier)
    return problems


def _link(reference: str) -> str:
    path, separator, anchor = reference.partition("#")
    suffix = f"#{anchor}" if separator else ""
    return f"[{Path(path).name}](../../{path}{suffix})"


def render_catalog(rows: list[dict]) -> str:
    lines = ["# Formal statement catalogue", "", "Generated from theorem-catalog.jsonl. Historical layers are not rewritten.", ""]
    for row in rows:
        lines += [
            f"## {row['theorem_id']}: {row['title']}", "",
            f"**{row['status']}**", "", row["statement"], "",
            "Assumptions: " + "; ".join(row["assumptions"]) + ".",
            "Scope: " + row["scope"], "",
        ]
        verification = row["proof_or_verification"]
        if "derivation_ref" in verification:
            lines.append("Proof: " + _link(verification["derivation_ref"]) + ". " + verification["proof_sketch"])
        elif "enumerated_domain" in verification:
            lines.append(f"Enumeration: {verification['enumerated_domain']}; exact count {verification['exact_count']}. Verifier: " + _link(verification["verification_implementation"]))
        elif "method" in verification:
            lines.append("Method: " + verification["method"])
            lines.append("Domain: " + verification["domain"])
            lines.append("Tolerances: " + chr(96) + json.dumps(verification["tolerances"], sort_keys=True) + chr(96))
            if verification.get("caveat"):
                lines.append("Method caveat: " + verification["caveat"])
        else:
            lines.append("Argument/next test: " + verification.get("argument", verification.get("next_test", "Open.")))
        lines.append("Evidence: " + ", ".join(_link(r) for r in row["evidence_refs"]))
        lines.append("Coherence: " + ", ".join(chr(96) + r + chr(96) for r in row["coherence_refs"]))
        lines.append("Dependencies: " + (", ".join(row["dependencies"]) or "none"))
        lines.append("Source generations: " + ", ".join(row["source_generations"]))
        lines += ["Boundary: " + row["counterexample_scope"]]
        if row["notes"]:
            lines += ["Notes: " + row["notes"]]
        lines += [""]
    return "\n".join(lines) + "\n"


def render_dependencies(rows: list[dict]) -> str:
    lines = ["flowchart TD"]
    for row in rows:
        identifier = row["theorem_id"].replace("-", "_")
        title = row["title"].replace('"', "'")
        lines.append(f'  {identifier}["{row["theorem_id"]}: {title}"]')
        for dependency in row["dependencies"]:
            lines.append(f"  {dependency.replace('-', '_')} --> {identifier}")
    return "\n".join(lines) + "\n"


def render_audit(rows: list[dict], root: Path) -> str:
    findings, _relations = load_ledger(root / "constraint-lab/coherence")
    index = {r["finding_id"]: r for r in findings}
    lines = [
        "# Historical backbone status audit", "",
        "Generated from status-audit.jsonl and the historical coherence ledger. "
        "The suggested formal reading does not change a historical epistemic layer.", "",
        "| Historical id / layer | Formal reading | Catalogue links | Scope |",
        "| --- | --- | --- | --- |",
    ]
    seen = set()
    for row in rows:
        finding = row["finding_id"]
        if finding in seen or finding not in index:
            raise FormalError(f"Duplicate or unknown audit finding {finding}")
        seen.add(finding)
        lines.append(f"| {finding} / {index[finding]['epistemic_layer']} | {row['formal_reading']} | {', '.join(row['theorem_refs'])} | {row['qualification']} |")
    return "\n".join(lines) + "\n"


def generated_views(root: Path | None = None) -> dict[Path, str]:
    root = root or repository_root()
    rows = load_catalog(root)
    problems = validate_catalog(rows, root)
    if problems:
        raise FormalError("\n".join(problems))
    directory = root / "constraint-lab/formal"
    audit = _jsonl(directory / "status-audit.jsonl")
    known = {r["theorem_id"] for r in rows}
    for row in audit:
        if not row.get("theorem_refs") or any(ref not in known for ref in row["theorem_refs"]):
            raise FormalError(f"Unknown or missing audit theorem reference: {row}")
        if row.get("formal_reading") not in STATUSES | {"HISTORICAL_SAMPLED_OBSERVATION", "INTERPRETATION"}:
            raise FormalError(f"Invalid audit formal reading: {row}")
        if not row.get("qualification"):
            raise FormalError(f"Audit qualification missing: {row}")
    return {
        directory / "theorem-catalog.md": render_catalog(rows),
        directory / "theorem-dependencies.mmd": render_dependencies(rows),
        directory / "status-audit.md": render_audit(audit, root),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--generate", action="store_true")
    mode.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    views = generated_views()
    for path, expected in views.items():
        if args.generate:
            path.write_text(expected, encoding="utf-8")
        elif not path.is_file() or path.read_text(encoding="utf-8") != expected:
            raise FormalError(f"Stale generated view: {path}")
    print(f"Formal catalogue valid: {len(load_catalog())} entries; {len(views)} deterministic views.")


if __name__ == "__main__":
    main()
