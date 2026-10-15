"""Validate live-ledger status-only transitions without rewriting old snapshots."""

from hashlib import sha256
import json


def validate_status_history(root, before, after):
    """Allow only byte-identical prefix rows or explicitly hash-linked statuses.

    Receipts must also exist in the append-only provenance ledger. Statements,
    ordering and creation metadata remain protected across later generations.
    """
    if len(after) < len(before):
        raise ValueError("historical finding deleted")
    ledger = [json.loads(line) for line in (root / "constraint-lab/provenance/ledger.jsonl").read_bytes().splitlines()]
    edges = {}
    for path in sorted((root / "constraint-lab/provenance/status-changes").glob("*.json")):
        receipt = json.loads(path.read_text())
        if not any(row.get("record_type") == "coherence_status_change" and
                   row.get("prompt_id") == receipt["prompt_id"] and
                   row.get("transitions") == receipt["transitions"] for row in ledger):
            raise ValueError("status receipt missing from provenance ledger: " + str(path))
        for change in receipt["transitions"]:
            if change["changed_fields"] != ["status"] or change["from"] == change["to"]:
                raise ValueError("not a status-only transition")
            key = change["before_row_sha256"]
            if key in edges:
                raise ValueError("ambiguous status transition")
            edges[key] = change
    for old, new in zip(before, after):
        if old == new:
            continue
        a, b = json.loads(old), json.loads(new)
        if a["finding_id"] != b["finding_id"] or {**a, "status": b["status"]} != b:
            raise ValueError("historical statement/metadata/order changed")
        digest, target, status, seen = sha256(old).hexdigest(), sha256(new).hexdigest(), a["status"], set()
        while digest != target:
            if digest in seen or digest not in edges:
                raise ValueError("historical row change lacks hash-linked authorization")
            seen.add(digest)
            change = edges[digest]
            if change["finding_id"] != a["finding_id"] or change["from"] != status:
                raise ValueError("status transition identity mismatch")
            digest, status = change["after_row_sha256"], change["to"]
        if status != b["status"]:
            raise ValueError("final status does not match receipt")
    return True
