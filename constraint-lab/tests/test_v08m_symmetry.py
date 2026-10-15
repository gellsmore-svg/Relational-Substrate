"""Post-M1 exact permutation and frozen result receipts."""

import json
from pathlib import Path
import subprocess

import pytest
pytest.importorskip("flint")
from rs_constraint_lab.durable import sha256_file
from rs_constraint_lab.explore08 import require_frozen_plan
from rs_constraint_lab.gen008m_exec import DIRECTORY,TABLE
from rs_constraint_lab.gen008m_symmetry import MASKS,OPPOSITE,PLAN
from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.h2_roles import SLOT_MAPS,fingerprint,role_of

ROOT=Path(__file__).resolve().parents[2]
FREEZE="ef31659a6313350f849751efe166f9438fa10b88"


def test_m1_separate_freeze_and_all_inputs_immutable():
    plan=require_frozen_plan(ROOT,FREEZE,PLAN,ROOT/PLAN)
    for path,digest in (plan["source_hashes"]|plan["input_hashes"]).items():
        assert sha256_file(ROOT/path)==digest
    subprocess.run(["git","merge-base","--is-ancestor",plan["M0_result_commit"],FREEZE],cwd=ROOT,check=True)
    assert plan["new_controllers"]==plan["new_stationary_solves"]==0


def test_opposite_pair_map_is_not_vertex_relabelling():
    assert OPPOSITE==(5,4,3,2,1,0)
    assert OPPOSITE not in SLOT_MAPS
    assert all(MASKS[MASKS[p]]==p and MASKS[p].bit_count()==p.bit_count() for p in range(64))
    for i in range(6):
        for j in range(6):
            for e in range(6):
                r=role_of(i,j,e)
                assert role_of(OPPOSITE[i],OPPOSITE[j],OPPOSITE[e])==(6 if r==5 else 5 if r==6 else r)
    table=pair_classes()
    mapping={}
    for p in range(64):
        mapping.setdefault(table.name_of[p],set()).add(table.name_of[MASKS[p]])
    assert all(len(v)==1 for v in mapping.values())
    assert sum(k not in v for k,v in mapping.items())==2


def test_m1_all_six_pair_receipts_and_independent_word_hashes():
    value=json.loads((ROOT/(TABLE+"m1-opposite-pair.json")).read_text())
    assert value["result_hash"]==fingerprint(value["result"])
    assert value["frozen_analysis_plan_commit"]==FREEZE
    records=value["result"]["records"]
    assert len(records)==6
    for row in records:
        assert row["kernel_conjugacy_exact"] and row["stationary_transport_exact"]
        assert row["KU_transport_exact"] and row["Kpi_transport_exact"]
        assert row["word_orbits_checked"]==25263
        assert row["independent_M0_word_hashes_reproduced"]==24
        assert row["stationary_STAR_vs_TRIANGLE"]["material_class"]==(
            "MATERIAL_SILENT" if row["family"]=="ANY" else "SHAPE_ONLY")
