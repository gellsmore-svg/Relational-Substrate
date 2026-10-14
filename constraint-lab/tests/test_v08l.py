"""Post-freeze exact H2 capability, certificate and provenance checks."""

from collections import defaultdict
from decimal import Decimal
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
import subprocess

import pytest

from rs_constraint_lab.durable import sha256_file
from rs_constraint_lab.explore08 import FrozenPlanError
from rs_constraint_lab.gen008i_predictive_exec import decode
from rs_constraint_lab.gen008l_exec import (
    BASE, MANIFEST, OUTPUT, PLAN, items, require_execution, verify,
)
from rs_constraint_lab.history_depth import DepthTwoState, SecondRecent, digest
from rs_constraint_lab.history import HistoryError
from rs_constraint_lab.predictive_state import conditional_information
from rs_constraint_lab.refinement import canonical_partition, lumpability, partition_from_labels, signatures
from rs_constraint_lab.state import edges

ROOT = Path(__file__).resolve().parents[2]
GRADES = (("m025",F(1,4)),("m1",F(1)),("m4",F(4)))


def result(kind, grade):
    return decode(json.loads((ROOT / OUTPUT / f"H2-{kind.upper()}-{grade}.json").read_text())["result"])


def freeze_commit():
    return json.loads((ROOT / MANIFEST).read_text())["frozen_analysis_plan_commit"]


def test_frozen_gate_provenance_and_all_atomic_hashes():
    with pytest.raises(FrozenPlanError):
        require_execution(ROOT,None)
    assert verify(ROOT,freeze_commit())["atomic_items"] == 12
    receipt=json.loads((ROOT/"constraint-lab/exploration/generation-008l/freeze-receipt.json").read_text())
    assert receipt["actual_new_N4_non_neutral_H2_target_executions_before_freeze"] == 0
    assert receipt["pushed_before_target_execution"]
    assert len(items()) == 12
    prompt=ROOT/"constraint-lab/provenance/prompts/008L-v0.8l-agent-input.md"
    assert prompt.stat().st_size == 49422
    assert sha256_file(prompt) == "5808e05877dfa8587737e10dba0c41b85ce4745e7388635c57ade8389071b340"
    assert sha256_file(prompt) not in prompt.read_text()
    ledger=[json.loads(x) for x in (ROOT/"constraint-lab/provenance/ledger.jsonl").read_text().splitlines()]
    authored=next(r for r in ledger if r["record_type"]=="prompt_representation" and r["prompt_id"]=="008K")
    assert authored["authored_prompt_bytes"] == 54276 and authored["agent_input_prompt_bytes"] == 54279
    assert authored["authored_prompt_sha256"] != authored["agent_input_prompt_sha256"]


@pytest.mark.parametrize("grade,m",GRADES)
def test_common_start_same_X_h1_and_exact_row_contradiction(grade,m):
    model=SecondRecent(m)
    a,b,c=[edges(4).index(pair) for pair in ((0,1),(1,2),(2,3))]
    paths=[]
    for events in ((a,b,c),(b,a,c)):
        state=DepthTwoState(0)
        mass=F(1)
        for e in events:
            target=model.advance(state,e)
            mass*=model.full_row(state)[target]
            state=target
        paths.append((state,mass))
    left,right=[p[0] for p in paths]
    assert left.material.to_bytes(2,"little") == right.material.to_bytes(2,"little") == bytes((41,0))
    assert left.h1 == right.h1 == c and (left.h2,right.h2)==(b,a)
    assert paths[0][1] == paths[1][1] == 1/(100*(m+9)) > 0
    row_a=model.full_probabilities(left.h1,left.h2)
    row_b=model.full_probabilities(right.h1,right.h2)
    assert [e for e in range(10) if row_a[e]!=row_b[e]] == ([] if m==1 else [a,b])
    for triad in range(6,10):
        assert model.advance(left,triad).h2 == b
    r=result("witness",grade)
    assert r["pair_row_gap"] == abs(m-1)/(m+5)
    assert r["full_row_gap"] == abs(m-1)/(m+9)
    assert r["edge_count_laws"][0] == r["edge_count_laws"][1]
    assert r["graph_class_laws"][0] == r["graph_class_laws"][1] if m==1 else r["graph_class_laws"][0] != r["graph_class_laws"][1]
    assert Decimal(r["information_formula_gap"]) <= Decimal("1e-25")


@pytest.mark.parametrize("grade,m",GRADES)
def test_full_rows_history_update_and_pair_absorption_all_raw_triads(grade,m):
    model=SecondRecent(m)
    for raw in range(16):
        for h1,h2 in ((None,None),(1,None),(2,4),(3,3)):
            state=DepthTwoState(41|(raw<<6),h1,h2)
            full=model.full_row(state)
            assert sum(full.values())==1 and len(full)==10
            for target in full:
                e=(state.material^target.material).bit_length()-1
                assert (state.material^target.material).bit_count()==1
                assert (target.h1,target.h2)==((e,h1) if e<6 else (h1,h2))
    for direct in model.direct_next_pair_slots(41,5,3):
        assert direct==list(model.pair_probabilities(5,3))
    r=result("kernel",grade)
    assert r["raw_triad_absorption_rows"]==240 and r["full_vs_pair_quotient_gap"]==0


@pytest.mark.parametrize("grade,m",GRADES)
def test_uniform_joint_stationarity_and_support_period(grade,m):
    r=result("kernel",grade)
    rows=[dict(row) for row in r["kernel"]]
    assert len(rows)==2304 and sum(map(len,rows))==13824
    assert r["communicating_classes"]==1 and r["unique_stationary"] and r["period"]==2
    incoming=[F(0)]*2304
    for source,row in enumerate(rows):
        p,i,j=SecondRecent(m).epoch_state(source)
        assert sum(row.values())==1
        for target,mass in row.items():
            pp,e,ii=SecondRecent(m).epoch_state(target)
            assert pp==p^(1<<e) and ii==i and (pp.bit_count()-p.bit_count())%2==1
            incoming[target]+=mass/F(2304)
    assert incoming==[F(1,2304)]*2304
    assert r["pair_marginal"]==[F(1,64)]*64
    assert r["history_pair_marginal"]==[F(1,36)]*36
    assert r["history_pair_independence_gap"]==0
    model=SecondRecent(m)
    diagonal=model.epoch_index(0,2,2)
    middle=model.epoch_index(4,2,2)
    assert rows[diagonal][middle]>0 and rows[middle][diagonal]>0


@pytest.mark.parametrize("grade,m",GRADES)
def test_generic_multi_round_memberships_and_compact_certificates(grade,m):
    model=SecondRecent(m)
    r=result("refinement",grade)
    assert r["block_counts_by_round"]==([64] if m==1 else [64,384,2304])
    assert r["refinement_rounds"]==(0 if m==1 else 2)
    blocks=canonical_partition(r["stable_blocks"],2304)
    assert digest(blocks)==r["membership_sha256"]
    rows=model.epoch_kernel()
    assert lumpability(rows,blocks)[1]==0
    if m==1:
        assert blocks==partition_from_labels([model.epoch_state(s)[0] for s in range(2304)])
    else:
        first=canonical_partition([part["members"] for split in r["chronology"][0]["splits"] for part in split["parts"]],2304)
        assert first==partition_from_labels([(p,j) for p,i,j in map(model.epoch_state,range(2304))])
        assert blocks==tuple((s,) for s in range(2304))
        assert r["generic_merge_certificate_count"]==40320
        assert r["merge_obstruction_classes"]=={"different_h2_immediate":34560,"same_h2_different_h1_later":5760}
        immediate=signatures(rows,partition_from_labels([model.epoch_state(s)[0] for s in range(2304)]))
        later=signatures(rows,first)
        a,b=model.epoch_index(41,0,3),model.epoch_index(41,5,3)
        assert immediate[a]==immediate[b] and later[a]!=later[b]
        assert not r["immediate_observed_rows_separate_all"]


@pytest.mark.parametrize("grade,m",GRADES)
def test_exact_adjacent_nulls_and_lag_two_positive_information(grade,m):
    r=result("temporal",grade)
    assert r["adjacent_event_joint"]==[[F(1,36)]*6 for _ in range(6)]
    expected=[[(m if e==j else 1)/(6*(m+5)) for e in range(6)] for j in range(6)]
    assert r["lag_two_event_joint"]==expected
    assert r["lag_two_repeat"]==m/(m+5)
    triples={tuple(row["word"]):row["probability"] for row in r["stationary_triples"]}
    assert len(triples)==2304 and set(triples.values())=={F(1,2304)}
    assert conditional_information(triples)==(Decimal(0),True)
    quads={(row["word"][0],tuple(row["word"][1:3]),row["word"][3]):row["probability"]
           for row in r["stationary_quadruples"]}
    cmi,_=conditional_information(quads)
    assert sum(quads.values())==1 and len(quads)==13824
    assert abs(cmi-Decimal(r["lag_two_event_MI"])) <= Decimal("1e-25")
    assert (cmi==0)==(m==1)
    assert r["pair_mask_markov_order"]==(1 if m==1 else 3)
    assert r["event_slot_markov_order"]==(1 if m==1 else 2)
    assert r["order_three_sufficiency_gap"]==0
    assert Decimal(r["information_formula_gap"])<=Decimal("1e-25")
    witness=r["order_two_failure_witness"]
    assert (witness is None)==(m==1)
    if witness:
        assert witness["next_row_A"]!=witness["next_row_B"]
        assert witness["positive_triple_mass_A"]>0 and witness["positive_triple_mass_B"]>0


def test_non_neutral_partition_memberships_equal():
    assert result("refinement","m025")["stable_blocks"]==result("refinement","m4")["stable_blocks"]


def test_prior_artifacts_and_frozen_sources_unchanged():
    def git(*args):
        return subprocess.run(["git","-C",str(ROOT),*args],capture_output=True,check=True).stdout
    original=set(git("ls-tree","-r","--name-only",BASE).decode().splitlines())
    changed=set(git("diff","--name-only",BASE,"--","books","constraint-lab/reports","constraint-lab/exploration",
                    "constraint-lab/provenance","constraint-lab/coherence/snapshots").decode().splitlines())
    assert original & changed <= {"constraint-lab/provenance/ledger.jsonl"}
    for path,value in json.loads((ROOT/PLAN).read_text())["source_sha256"].items():
        assert sha256_file(ROOT/path)==value
    for path in ("constraint-lab/provenance/ledger.jsonl","constraint-lab/formal/theorem-catalog.jsonl",
                 "constraint-lab/coherence/relations.jsonl"):
        assert (ROOT/path).read_bytes().startswith(git("show",BASE+":"+path))


def test_only_authorised_h2_question_status_changes():
    from hashlib import sha256
    path="constraint-lab/coherence/findings.jsonl"
    old=subprocess.run(["git","-C",str(ROOT),"show",BASE+":"+path],capture_output=True,check=True).stdout.splitlines()
    current=(ROOT/path).read_bytes().splitlines()
    receipt=json.loads((ROOT/"constraint-lab/provenance/status-changes/008L-h2-question.json").read_text())
    assert len(receipt["transitions"])==1
    change=receipt["transitions"][0]
    assert change["finding_id"]=="Q-H2-LAST-PAIR-COMPILER"
    for before,after in zip(old,current):
        original=json.loads(before)
        if original["finding_id"]!=change["finding_id"]:
            assert before==after
            continue
        assert original["status"]=="unresolved"
        assert json.loads(after)=={**original,"status":"qualified"}
        assert sha256(before).hexdigest()==change["before_row_sha256"]
        assert sha256(after).hexdigest()==change["after_row_sha256"]
    assert change["changed_fields"]==["status"]
    findings=[json.loads(x) for x in current]
    assert next(f for f in findings if f["finding_id"]=="Q-L-COMPILER-SEMANTICS")["status"]=="unresolved"
    relations=[json.loads(x) for x in (ROOT/"constraint-lab/coherence/relations.jsonl").read_text().splitlines()]
    assert any(r["from_finding"]==change["finding_id"] and r["relation_type"]=="partially_answered_by"
               for r in relations)


def test_typed_cache_validation_after_equal_valued_valid_calls():
    model=SecondRecent(F(1))
    for probabilities in (model.full_probabilities,model.pair_probabilities):
        for valid,invalid in (((1,None),(True,None)),((0,None),(False,None)),
                              ((0,1),(0,True)),((1,0),(1,False))):
            probabilities(*valid)
            with pytest.raises(HistoryError):
                probabilities(*invalid)


def test_original_freeze_and_results_remain_immutable_after_validation_amendment():
    from hashlib import sha256
    from rs_constraint_lab.gen008l_exec import ORIGINAL_OUTPUT
    original_commit="3e71f0687e6097de87efdcab455e1b28c8b2a765"
    def blob(path):
        return subprocess.run(["git","-C",str(ROOT),"show",original_commit+":"+path],
                              capture_output=True,check=True).stdout
    original_manifest="constraint-lab/reports/generation-008l-h2-0-tables.json"
    manifest=json.loads((ROOT/original_manifest).read_text())
    for path in [original_manifest,*manifest["item_sha256"],*manifest["table_sha256"],
                 "constraint-lab/exploration/generation-008l/round-h2-0-plan.json",
                 "constraint-lab/exploration/generation-008l/freeze-receipt.json"]:
        assert (ROOT/path).read_bytes()==blob(path)
    original_plan=json.loads(blob("constraint-lab/exploration/generation-008l/round-h2-0-plan.json"))
    for path,value in original_plan["source_sha256"].items():
        assert sha256(blob(path)).hexdigest()==value
    for item in items():
        original=json.loads((ROOT/ORIGINAL_OUTPUT/(item["item_id"]+".json")).read_text())
        amended=json.loads((ROOT/OUTPUT/(item["item_id"]+".json")).read_text())
        assert original["result_sha256"]==amended["result_sha256"]
        assert original["analysis_version"]!=amended["analysis_version"]
    replay=json.loads((ROOT/"constraint-lab/exploration/generation-008l/amendment-a-replay.json").read_text())
    assert replay["all_four_summary_table_hashes_equal"]
    assert all(r["exact_equal"] for r in replay["result_comparisons"])
