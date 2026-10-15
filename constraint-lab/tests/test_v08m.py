"""Post-freeze durable M0 atlas and independent exact-law checks."""

from collections import defaultdict
from decimal import Decimal
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import subprocess

import pytest

pytest.importorskip("flint")
from flint import fmpq as Q
from rs_constraint_lab.gen008m_exec import BASE, DIRECTORY, OUTPUT, PLAN, TABLE, gate, items
from rs_constraint_lab.h2_roles import (
    STATES, RoleController, augmented_structure, fingerprint, kernel_from_events,
    lift, quotient, residual, role_of,
)
from rs_constraint_lab.h2_role_words import direct_word

ROOT = Path(__file__).resolve().parents[2]
FREEZE = "c5042fbb0103436d15591e009d0c58b173283e8f"


def read(path):
    return json.loads((ROOT/path).read_text())


def payload(item):
    return read(OUTPUT+"/"+item["item_id"]+".json")


def test_m0_freeze_prompt_and_item_integrity():
    plan = gate(ROOT,FREEZE)
    assert len(items())==73
    assert plan["pre_freeze_exposure"]["new_non_neutral_8M_primary_cells"]==0
    assert plan["plan_hash"]=="c74237447c4bfa0a6f1b130abe54a859e11224c0945c615e304ec150845a5036"
    prompt=ROOT/"constraint-lab/provenance/prompts/008M-v0.8m-agent-input.md"
    assert prompt.stat().st_size==58498
    assert sha256(prompt.read_bytes()).hexdigest()=="dfd22bb42ac9254dd3fb70031eb21c4b9e7663f51f22ae0895030f514c704991"
    for item in items():
        value=payload(item)
        assert value["item"]==item and value["result_hash"]==fingerprint(value["result"])
        assert value["frozen_analysis_plan_commit"]==FREEZE


@pytest.mark.parametrize("item",items(),ids=lambda item:item["item_id"])
def test_all_stationary_classifications_comparators_and_exact_residual(item):
    r=payload(item)["result"]
    pi=lift(tuple(Q(v) for v in r["stationary_orbit_masses"]))
    model=RoleController(item["role"],item["family"],item["m"])
    events=model.event_rows()
    rows=kernel_from_events(events)
    assert residual(pi,rows)==0
    assert [sorted(row.items()) for row in quotient(rows)]==[
        [(int(t),Q(v)) for t,v in row] for row in r["quotient_kernel"]]
    assert r["strict_H2"]==("H1_COMPILABLE" if item["m"]=="1" else "STRICT_H2")
    if item["m"]!="1":
        w=r["strict_H2_witness"]
        assert w["row_A"]!=w["row_B"]
        assert model.probabilities(w["P"],w["h1"],w["h2_A"])!=model.probabilities(w["P"],w["h1"],w["h2_B"])
    if item["family"]=="ANY":
        assert r["neutral_comparison"]["material_class"]=="MATERIAL_SILENT"
        assert r["uniform_H1_comparison"]["pair_equal"]
    ph1=tuple(Q(v) for v in r["stationary_P_H1"])
    kpi=tuple(tuple(Q(v) for v in row) for row in r["Kpi_H1"]["event_rows"])
    ku=tuple(tuple(Q(v) for v in row) for row in r["KU_H1"]["event_rows"])
    assert residual(ph1,kernel_from_events(kpi,1))==0
    assert all(sum(row)==1 for row in kpi+ku)
    for p,i in ((0,0),(13,3),(41,5),(63,4)):
        for e in range(6):
            assert ph1[p*6+i]*kpi[p*6+i][e]==sum(pi[(p*6+i)*6+j]*events[(p*6+i)*6+j][e] for j in range(6))
            assert ku[p*6+i][e]==sum(events[(p*6+i)*6+j][e] for j in range(6))/6
    for comparison in (r["neutral_comparison"],r["uniform_H1_comparison"]):
        assert abs(Decimal(comparison["chain_gap"]))<=Decimal("1e-25")
    words=r["words"]["word_summaries"]
    assert len(words)==18
    assert all(w["exact_equal"] for w in words if w["word_length"]<=3)
    assert all(w["exact_equal"] for w in words) if item["m"]=="1" else True
    # A fully labelled sample word independently recomputes exact H2/H1 paths.
    a,b=direct_word((0,1,9,41),pi,events,ph1,kpi)
    assert min(a,b)>0


def test_no_historical_artifact_or_book_overwritten():
    listed=subprocess.check_output(["git","ls-tree","-r","--name-only",BASE],cwd=ROOT,text=True).splitlines()
    protected=[p for p in listed if p.startswith(("books/","constraint-lab/reports/",
        "constraint-lab/exploration/","constraint-lab/provenance/prompts/","constraint-lab/coherence/snapshots/"))]
    changed=subprocess.check_output(["git","diff","--name-only","--diff-filter=DMRTUXB",BASE],
                                    cwd=ROOT,text=True).splitlines()
    assert not set(changed)&set(protected)


def test_both_complement_partners_executed_and_exact_word_controls():
    complement=read(TABLE+"complement.json")
    assert len(complement)==24
    assert all(c["kernel_exact"] and c["stationary_exact"] for c in complement)
    words=read(TABLE+"word-atlas.json")
    assert len(words)==73*18
    assert all(w["exact_equal"] for w in words if w["word_length"]<=3)
    assert all(w["exact_normalization_H2"]==w["exact_normalization_Kpi_H1"]=="1" for w in words)


def test_source_freeze_is_ancestor_and_original_8l_metadata_unchanged():
    subprocess.run(["git","merge-base","--is-ancestor",FREEZE,"HEAD"],cwd=ROOT,check=True)
    for path in ("constraint-lab/exploration/generation-008l/round-h2-0-plan.json",
                 "constraint-lab/exploration/generation-008l/round-h2-0-amendment-a.json"):
        old=subprocess.check_output(["git","show",BASE+":"+path],cwd=ROOT)
        assert (ROOT/path).read_bytes()==old


def test_exact_stationary_information_zero_certificates():
    certificates=read(TABLE+"information-certificates.json")
    assert len(certificates)==73
    assert sum(c["I_P_H2_given_H1_exact_zero"] for c in certificates)==25
    assert sum(c["experienced_H2_KL_uniform_exact_zero"] for c in certificates)==1
    for item,c in zip(sorted(items(),key=lambda i:i["item_id"]),certificates):
        assert c["system_id"]==item["item_id"]
        assert c["source_result_hash"]==payload(item)["result_hash"]
        assert c["I_P_H2_given_H1_exact_zero"]==(item["family"]=="ANY")
        if c["conditional_independence_obstruction"]:
            w=c["conditional_independence_obstruction"]
            assert Q(w["product_left"])!=Q(w["product_right"])
