"""Post-freeze exact passage receipts and independent full-state checks."""

from hashlib import sha256
import json
from pathlib import Path
import subprocess

import pytest
pytest.importorskip("flint")
from flint import fmpq as Q
from rs_constraint_lab.gen008n_exec import BASE, DIRECTORY, OUTPUT, TABLE, gate, items, valid
from rs_constraint_lab.h2_roles import fingerprint
from rs_constraint_lab.h2_passage_verify import verify
from rs_constraint_lab.status_history import validate_status_history

ROOT = Path(__file__).resolve().parents[2]
FREEZE = "b4835b812226da179d75d1758e6d2b934fa3f852"


def read(path):
    return json.loads((ROOT / path).read_text())


def test_frozen_zero_exposure_and_all_hash_addressed_items():
    p = gate(ROOT, FREEZE)
    assert p["pre_freeze_exposure"]["new_non_neutral_8N_passage_outputs"] == 0
    assert len(p["items"]) == 73
    assert p["plan_hash"] == "d913549ba4d3f702b482ce8e24e2939b8390a62137704402c7800bcf1cd41236"
    for item in items():
        assert valid(ROOT / OUTPUT / (item["item_id"] + ".json"), item, p, FREEZE)
    prompt = ROOT / "constraint-lab/provenance/prompts/008N-v0.8n-agent-input.md"
    assert prompt.stat().st_size == 55200
    assert sha256(prompt.read_bytes()).hexdigest() == "fe9c95fcf2640b17f582e2a77c24e416eca67d60d5d1174e5f94c854fda45261"


@pytest.mark.parametrize("item", items(), ids=lambda item: item["item_id"])
def test_full_state_return_path_sums_hitting_aggregations_and_controls(item):
    value = read(OUTPUT + "/" + item["item_id"] + ".json")
    r = value["result"]
    assert verify(ROOT, item, r)["exact"]
    for layer in r["layers"].values():
        assert layer["H2"]["lengths"]["2"] == layer["Kpi"]["lengths"]["2"]
        for row in layer["comparison"].values():
            assert row["routing_active"] == any(Q(x) for x in row["delta_R"])
    if item["m"] == "1":
        assert all(not row["routing_active"] and not row["length_active"]
                   for layer in r["layers"].values() for row in layer["comparison"].values())


def test_tables_reassemble_all_tasks_and_conjugate_controls():
    v = read(TABLE + "validation.json")
    assert v["status"] == "VERIFIED" and v["items"] == 73
    assert len(v["conjugacies"]) == 30 and all(c["exact"] for c in v["conjugacies"])
    for suffix, digest in v["table_hashes"].items():
        assert sha256((ROOT / (TABLE + suffix + ".json")).read_bytes()).hexdigest() == digest
    assert len(read(TABLE + "mfpt.json")) == 730
    assert len(read(TABLE + "committor.json")) == 219
    assert len(read(TABLE + "summary.json")) == 511


def test_immutable_inputs_books_snapshots_and_explicit_status_history():
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=ROOT)
    paths = git("ls-tree", "-r", "--name-only", BASE).decode().splitlines()
    protected = {p for p in paths if p.startswith(("books/", "constraint-lab/reports/", "constraint-lab/exploration/",
                    "constraint-lab/coherence/snapshots/", "constraint-lab/provenance/prompts/"))}
    assert not protected & set(git("diff", "--name-only", BASE).decode().splitlines())
    before = git("show", BASE + ":constraint-lab/coherence/findings.jsonl").splitlines()
    after = (ROOT / "constraint-lab/coherence/findings.jsonl").read_bytes().splitlines()
    assert validate_status_history(ROOT, before, after)
    changed = list(after)
    row = json.loads(changed[0]); row["statement"] += " unauthorized"
    changed[0] = json.dumps(row).encode()
    with pytest.raises(ValueError):
        validate_status_history(ROOT, before, changed)
    with pytest.raises(ValueError):
        validate_status_history(ROOT, before, after[:len(before)-1])
