"""Post-freeze factor census: exact equations, not numerical zero tests."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import subprocess

import pytest
pytest.importorskip("flint")

from rs_constraint_lab.gen008m_exec import read
from rs_constraint_lab.gen008o_exec import BASE, OUTPUT, TABLE, gate, items, valid
from rs_constraint_lab.h2_roles import fingerprint
from rs_constraint_lab.status_history import validate_status_history
from rs_constraint_lab.stopping_factorization import analyse

ROOT = Path(__file__).resolve().parents[2]
FREEZE = "bf3fae54c438a8d586bb578e5d5430274274ed00"


def test_f0_plan_prompt_context_and_complete_hash_addressed_universe():
    plan = gate(ROOT, FREEZE)
    assert plan["pre_freeze_exposure"]["new_non_neutral_8O_factor_diagnostics"] == 0
    assert plan["hub_context_commit"] == "38c2501bbab22ca1eb2288ea76a962ac0170d5e6"
    assert len(plan["items"]) == 73
    assert plan["plan_hash"] == "42477b27c57169520249aef7274e3e35f4cb7c9202cf72505f99dd13d25c12fc"
    prompt = ROOT / "constraint-lab/provenance/prompts/008O-v0.8o-agent-input.md"
    assert prompt.stat().st_size == 55165
    assert sha256(prompt.read_bytes()).hexdigest() == "531b2bd99e603c0f5b03eb44e0f526a517f66a2e4f444a51aa6eb62acf19db3d"
    for item in items():
        assert valid(ROOT / OUTPUT / (item["item_id"] + ".json"), item, plan, FREEZE)


@pytest.mark.parametrize("item", items(), ids=lambda item: item["item_id"])
def test_exact_new_occupation_full_sparse_equations_and_immutable_route_rows(item):
    stored = read(ROOT / OUTPUT / (item["item_id"] + ".json"))
    # Reproduce only the frozen derived diagnostics, not the old passage solves.
    actual = analyse(ROOT, item)
    assert fingerprint(actual) == stored["result_hash"]
    assert actual["dimensions"] == {"full_Z": 2304, "full_S": 384, "sector_Z": 120, "sector_S": 28}
    for row in actual["rows"]:
        assert row["bilinear_product_zero"] == (not any(row["DeltaR"]))
        if row["mechanism"] == "N0_UPSTREAM_ANNIHILATION":
            assert row["U_zero"]
        elif row["mechanism"] == "N1_TARGET_INSENSITIVITY":
            assert not row["U_zero"] and row["W_zero"]
        elif row["mechanism"] == "N2_BILINEAR_ORTHOGONALITY":
            assert not row["U_zero"] and not row["W_zero"] and row["bilinear_product_zero"]
        else:
            assert row["mechanism"] == "ACTIVE" and not row["bilinear_product_zero"]


def test_reassembled_counts_transports_and_exact_timing_aggregation():
    rows = read(ROOT / (TABLE + "route-null-factorization.json"))
    primary = [r for r in rows if r["m"] != "1"]
    assert len(primary) == 1008 and len(rows) == 1022
    assert Counter(r["route"] for r in primary if r["bilinear_product_zero"]) == {"UP": 100, "DOWN": 100}
    timing = read(ROOT / (TABLE + "timing-factorization.json"))
    assert len([r for r in timing if r["structured_nonzero"] and r["aggregation_annihilates"]]) == 20
    v = read(ROOT / (TABLE + "factor-validation.json"))
    assert v["items"] == 73 and v["status"] == "VERIFIED"
    assert len(v["conjugacies"]) == 114 and all(r["exact"] for r in v["conjugacies"])
    for name, digest in v["table_hashes"].items():
        assert sha256((ROOT / (TABLE + name + ".json")).read_bytes()).hexdigest() == digest


def test_no_hub_import_no_upstream_overwrite_no_hub_evidence_and_status_history():
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=ROOT)
    assert not git("ls-files", "research-synthesis/")
    before_paths = git("ls-tree", "-r", "--name-only", BASE).decode().splitlines()
    protected = {p for p in before_paths if p.startswith(("books/", "constraint-lab/reports/", "constraint-lab/exploration/",
                   "constraint-lab/coherence/snapshots/", "constraint-lab/provenance/prompts/"))}
    assert not protected.intersection(git("diff", "--name-only", BASE).decode().splitlines())
    old = git("show", BASE + ":constraint-lab/coherence/findings.jsonl").splitlines()
    new = (ROOT / "constraint-lab/coherence/findings.jsonl").read_bytes().splitlines()
    assert validate_status_history(ROOT, old, new)
    for path, key in (("coherence/findings.jsonl", "finding_id"), ("formal/theorem-catalog.jsonl", "theorem_id")):
        for line in (ROOT / "constraint-lab" / path).read_text().splitlines():
            row = json.loads(line)
            if "008O" in row.get("source_generations", []) or row.get("created_generation") == "008O":
                assert all(not ref.startswith(("X::", "XQ::", "research-synthesis/")) and "synthesis-handoffs" not in ref
                           for ref in row["evidence_refs"]), row[key]
