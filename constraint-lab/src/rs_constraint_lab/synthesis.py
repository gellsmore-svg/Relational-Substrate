"""Deterministic 8K branch metadata and conceptual diagram verification."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from itertools import combinations

from rs_constraint_lab.durable import atomic_write_json, atomic_write_text, sha256_bytes
from rs_constraint_lab.formal import repository_root

BASE = "6c8f052c2d3361516e08c5a3def10a15474096cc"
HEADS = {
    "canonical_predictive_8i": BASE,
    "alternate_role_8i": "6615c9f03a1fa30558f8cf519a125e610d393f31",
    "coarse_process_8j": "64a4fe67e585e5be03f6afb2a0613e147c509b63",
}
ARTIFACTS = {
    "catalogue": ("constraint-lab/formal/theorem-catalog.jsonl", "theorem_id"),
    "findings": ("constraint-lab/coherence/findings.jsonl", "finding_id"),
    "relations": ("constraint-lab/coherence/relations.jsonl", "relation_id"),
}
AUDIT = "constraint-lab/formal/branch-reconciliation-008i-008j.json"
DIAGRAMS = {
    "state-taxonomy": {
        "direction": "TB",
        "nodes": {"X": "Ordinary X", "H": "Historical H", "ETA": "Candidate constraint eta (not executed)",
                  "Z": "Augmented represented Z", "Y": "Raw observation Y",
                  "B": "Strong refinement block B", "BN": "Next Markov predictive block",
                  "YF": "Finer observation", "YC": "Coarser observation",
                  "BF": "Fine strong refinement", "BC": "Coarse strong refinement"},
        "edges": [("X", "Z", "coordinate", False), ("H", "Z", "coordinate", False),
                  ("ETA", "Z", "candidate coordinate", True), ("Z", "Y", "phi", False),
                  ("Z", "B", "rho_Y", False), ("B", "Y", "observation", False),
                  ("B", "BN", "quotient kernel", False), ("YF", "YC", "coarsening f", False),
                  ("BF", "BC", "induced strong quotient", False)],
    },
    "predictive-quotient-square": {
        "direction": "LR",
        "nodes": {"ZT": "Z_t", "ZN": "Z_(t+1)", "BT": "B_t", "BN": "B_(t+1)"},
        "edges": [("ZT", "ZN", "T", False), ("ZT", "BT", "rho_Y", False),
                  ("ZN", "BN", "rho_Y", False), ("BT", "BN", "bar-T_Y", False)],
    },
    "raw-observation-square": {
        "direction": "LR",
        "nodes": {"ZT": "Z_t", "ZN": "Z_(t+1)", "YT": "Y_t", "YN": "Y_(t+1)"},
        "edges": [("ZT", "ZN", "T", False), ("ZT", "YT", "phi", False),
                  ("ZN", "YN", "phi", False),
                  ("YT", "YN", "no guaranteed first-order kernel", True)],
    },
    "history-constraint-roles": {
        "direction": "TB",
        "nodes": {"PAST": "Past ordinary trajectory", "H": "H_t path summary",
                  "X": "Current X_t", "ETA": "Candidate eta_t",
                  "META": "Fixed common meta-programme", "LAW": "Event law"},
        "edges": [("PAST", "H", "summary", False), ("H", "LAW", "input", False),
                  ("X", "LAW", "input", False), ("ETA", "LAW", "constraint configuration", False),
                  ("META", "ETA", "update semantics", False)],
    },
}


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True).stdout


def branch_audit(root=None):
    root = root or repository_root()
    records, content = {}, {}
    for label, head in HEADS.items():
        records[label] = {"head": head, "artifacts": {}}
        content[label] = {}
        for name, (path, key) in ARTIFACTS.items():
            data = git(root, "show", head + ":" + path)
            rows = [json.loads(line) for line in data.splitlines()]
            index = {row[key]: row for row in rows}
            if len(rows) != len(index):
                raise ValueError("duplicate pinned branch identifiers")
            content[label][name] = index
            records[label]["artifacts"][name] = {
                "path": path, "rows": len(rows), "sha256": sha256_bytes(data),
                "ids": sorted(index),
            }
    conflicts = []
    for left, right in combinations(HEADS, 2):
        for name in ARTIFACTS:
            a, b = content[left][name], content[right][name]
            for identifier in sorted(a.keys() & b.keys()):
                if a[identifier] != b[identifier]:
                    conflicts.append({"namespace": name, "id": identifier, "heads": [left, right],
                                      "different_fields": sorted(key for key in a[identifier].keys() | b[identifier].keys()
                                                                 if a[identifier].get(key) != b[identifier].get(key))})
    maxima = {}
    for branch in content.values():
        for identifier in branch["catalogue"]:
            match = re.fullmatch(r"CL-([TFNIMQ])([0-9]+)", identifier)
            kind, number = match.groups()
            maxima[kind] = max(maxima.get(kind, 0), int(number))
    return {
        "kind": "pinned_repository_metadata_audit_not_scientific_computation",
        "heads": records,
        "merge_bases": [{"heads": [left, right],
                         "commit": git(root, "merge-base", HEADS[left], HEADS[right]).decode().strip()}
                        for left, right in combinations(HEADS, 2)],
        "identifier_conflicts": conflicts, "catalogue_maxima": maxima,
        "reserved_new_theorems": ["CL-T" + str(i) for i in range(60, 68)],
        "reserved_new_methods": ["CL-M04", "CL-M05"],
        "alias_records_needed": bool(conflicts),
        "policy": "No automatic merge or import. Qualify external citations by branch/head/path/ID; canonical promotion requires review or re-establishment. No collision means no invented alias.",
    }


def diagram_views(root=None):
    root = root or repository_root()
    result = {}
    for name, spec in DIAGRAMS.items():
        lines = ["flowchart " + spec["direction"]]
        for key, label in spec["nodes"].items():
            lines.append(f"  {key}[{json.dumps(label)}]")
        for source, target, label, dotted in spec["edges"]:
            if source not in spec["nodes"] or target not in spec["nodes"]:
                raise ValueError("unknown diagram endpoint")
            arrow = "-.->" if dotted else "-->"
            lines.append(f"  {source} {arrow}|{json.dumps(label)}| {target}")
        result[root / "constraint-lab/formal" / (name + ".mmd")] = "\n".join(lines) + "\n"
    return result


def verify(root=None):
    root = root or repository_root()
    audit = branch_audit(root)
    if audit["identifier_conflicts"]:
        raise ValueError("pinned branch collision needs explicit reconciliation")
    if json.loads((root / AUDIT).read_text()) != audit:
        raise ValueError("stale branch reconciliation audit")
    for path, expected in diagram_views(root).items():
        if path.read_text() != expected:
            raise ValueError(f"stale diagram: {path}")
    pinned = {identifier for record in audit["heads"].values()
              for identifier in record["artifacts"]["catalogue"]["ids"]}
    current = [json.loads(line) for line in (root / ARTIFACTS["catalogue"][0]).read_text().splitlines()]
    if any(row["theorem_id"] in pinned for row in current if row["source_generations"] == ["008K"]):
        raise ValueError("new catalogue ID reuses a pinned branch ID")
    return {"status": "VERIFIED", "pinned_heads": 3, "diagrams": len(DIAGRAMS), "identifier_conflicts": 0,
            "scientific_computation": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--generate", action="store_true")
    mode.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    root = repository_root()
    if args.generate:
        atomic_write_json(root / AUDIT, branch_audit(root))
        for path, content in diagram_views(root).items():
            atomic_write_text(path, content)
    print(json.dumps(verify(root), sort_keys=True))


if __name__ == "__main__":
    main()
