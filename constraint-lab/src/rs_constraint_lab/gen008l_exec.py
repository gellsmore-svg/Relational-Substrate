"""Freeze-gated, atomic H2-0 execution. No target runs during import."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from decimal import Decimal
from fractions import Fraction as F
import json
from pathlib import Path
import signal
import time

from rs_constraint_lab.coherence import canonical_ledger_bytes
from rs_constraint_lab.durable import atomic_write_json, canonical_json, read_json, sha256_file, sha256_bytes
from rs_constraint_lab.explore08 import FrozenPlanError, plan_hash, remote_contains, require_frozen_plan
from rs_constraint_lab.gen008i_predictive_exec import decode
from rs_constraint_lab.history import HistoryError, PRECISION
from rs_constraint_lab.history_depth import (
    CLOCK, VERSION, SecondRecent, analyse_kernel, analyse_refinement, analyse_temporal, analyse_witness, digest,
)
from rs_constraint_lab.predictive_state import balance_gap
from rs_constraint_lab.refinement import lumpability

BASE = "e81e7d5f67fa00f1d629f8bd4b365352d25c9eb1"
DIRECTORY = "constraint-lab/exploration/generation-008l"
PLAN = DIRECTORY + "/round-h2-0-plan.json"
CALIBRATION = DIRECTORY + "/calibration.json"
OUTPUT = "constraint-lab/reports/items/generation-008l-h2-0"
MANIFEST = "constraint-lab/reports/generation-008l-h2-0-tables.json"
TABLE = "constraint-lab/reports/tables/generation-008l-"
GRADES = (("m025", "1/4"), ("m1", "1"), ("m4", "4"))
ANALYSES = {"witness": analyse_witness, "kernel": analyse_kernel, "refinement": analyse_refinement, "temporal": analyse_temporal}
SOURCES = tuple("constraint-lab/src/rs_constraint_lab/" + name for name in (
    "history_depth.py", "gen008l_exec.py", "history.py", "refinement.py", "predictive_state.py",
    "gen008i_predictive_exec.py", "graphs.py", "state.py", "exact.py", "memory_clocks.py",
    "durable.py", "explore08.py", "coherence.py",
))
INPUTS = (DIRECTORY + "/charter.md", DIRECTORY + "/predeclared-expectations.md",
          "constraint-lab/provenance/prompts/008L-v0.8l-agent-input.md",
          "constraint-lab/tests/test_v08l_plumbing.py")


def repository_root():
    return Path(__file__).resolve().parents[3]


def items():
    return [{"item_id": f"H2-{kind.upper()}-{grade}", "kind": kind, "grade": grade, "m": m}
            for kind in ANALYSES for grade,m in GRADES]


@contextmanager
def watchdog(seconds):
    def alarm(signum, frame):
        raise TimeoutError("H2 item exceeded watchdog; earlier completed items retained")
    previous = signal.signal(signal.SIGALRM, alarm)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)


def validate_result(item, raw):
    r, kind, m = decode(raw), item["kind"], F(item["m"])
    gaps = {"witness": [], "kernel": ["stationary_residual", "uniform_joint_gap", "column_sum_gap",
            "history_pair_independence_gap", "stationary_one_step_H0_gap", "row_sum_gap", "full_vs_pair_quotient_gap"],
            "refinement": ["strong_lumpability_gap", "state_reordering_gap", "analytic_membership_gap"],
            "temporal": ["independent_forward_word_gap", "order_three_sufficiency_gap", "stationary_triples_H0_gap"]}
    if any(F(r[key]) for key in gaps[kind]):
        raise HistoryError("exact H2 validation failed")
    if kind == "refinement":
        expected = [64] if m == 1 else [64,384,2304]
        if r["block_counts_by_round"] != expected:
            raise HistoryError("actual refinement differs from predeclared expectation")
    if kind == "kernel" and (r["communicating_classes"] != 1 or r["period"] != 2):
        raise HistoryError("communicating/period expectation differs")
    if kind == "witness" and (not r["same_X"] or not r["same_h1"] or r["strict_H1_noncompilability"] != (m != 1)):
        raise HistoryError("same-(X,h1) witness invalid")
    if kind == "temporal":
        if not r["adjacent_event_independence_exact"] or not r["order_two_mask_independence_exact"]:
            raise HistoryError("exact adjacent null is absent")
        if r["pair_mask_markov_order"] != (1 if m == 1 else 3):
            raise HistoryError("observed order differs")
    info_key = "information_formula_gap"
    if info_key in r and Decimal(r[info_key]) > Decimal("1e-25"):
        raise HistoryError("information formula gap exceeds frozen tolerance")


def calibrate(root):
    if (root / PLAN).exists() or (root / CALIBRATION).exists():
        raise HistoryError("neutral calibration is one-time and precedes freeze")
    records = []
    for kind, analyse in ANALYSES.items():
        start = time.monotonic()
        with watchdog(120):
            result = analyse(SecondRecent(F(1)))
            validate_result({"kind": kind, "m": "1"}, result)
        records.append({"kind": kind, "wall_seconds": time.monotonic()-start,
                        "result_bytes": len(canonical_json(result).encode())})
        print("NEUTRAL", kind, records[-1], flush=True)
    receipt = {
        "neutral_measurements": records, "new_N4_non_neutral_H2_target_executions": 0,
        "historical_tests_run": ["constraint-lab/tests/test_v08k.py"],
        "plumbing_tests": "test_v08l_plumbing.py: neutral N4 and multiplier-two three-slot synthetic only",
        "initial_test_issue": "neutral decimal-zero formatting assertion; corrected to numerical equality before calibration",
        "prior_knowledge": "Prompt 008L and 8K symbolic H2 design; existing H1 information magnitudes; not independent discovery",
        "workers": 1, "numeric_threads": 1,
    }
    atomic_write_json(root / CALIBRATION, receipt)
    return receipt


def write_plan(root):
    if (root / PLAN).exists():
        raise HistoryError("refusing to replace frozen plan")
    calibration = read_json(root / CALIBRATION)
    document = {
        "experiment_id": "generation-008l-history-depth-two", "prompt_id": "008L", "round_id": "H2-0",
        "analysis_version": VERSION, "mode": "A", "parent_commit": BASE, "clock": CLOCK,
        "ontology": {"N":4,"O":3,"G":0,"S":0,"L":0,"H_pair":2,"hypergraph":"independent"},
        "controller": "SECOND-RECENT: only pair e=h2 receives m, unavailable h2 neutral",
        "history": {"initial":[None,None],"pair_update":"(h1,h2)'=(e,h1)","triad_update":"identity",
                    "depth_not_alphabet":"two prior pair slots, not one arbitrary 36-valued H1 symbol"},
        "grades": GRADES,
        "compiler_class": {
            "state":"exactly (complete ten-bit X, most-recent pair identity h1)",
            "allowed":["arbitrary positive K","arbitrary positive rule cardinality J"],
            "forbidden":["hidden state","persistent random seed","time phase","history alphabet enlargement",
                         "recoding h1","changed clock","changed support","changed observation","per-history program"],
            "equivalence":"all reachable history-conditioned ordinary future rows, one common fixed law",
            "initial_law":"common deterministic empty X and sentinel; structural claims arbitrary reachable augmented starts",
            "unrestricted_augmentation":"36-valued encoding allowed at raw kernel level but outside semantic H1",
        },
        "witness":{"a":"01","b":"12","c":"23","A":["a","b","c"],"B":["b","a","c"],
                   "start_material":0,"start_history":[None,None],"triads":0},
        "estimands":[
            "full/pair path probability, ten-bit endpoint identity, same h1, changed h2, support/baseline/constraints identity",
            "full/pair row gaps and JS; exact strict-H1 contradiction; mechanically classified shape laws and equal count laws",
            "2304 sparse recurrent states, six outgoing events each; row/column balance, uniform stationarity and marginals",
            "communicating classes/period; label covariance under all 24 vertex permutations",
            "raw full-event absorption for three pair masks, five histories including sentinel, all 16 triad masks",
            "generic exact mask refinement, reverse enumeration, memberships, chronology, compact merge obstruction schemas",
            "stationary event adjacent/lag-two joints; exact adjacent independence, lag repetition and 160-digit MI",
            "stationary material triples/quadruples; independent three-forward-step construction versus backward history reconstruction",
            "exact pair-mask order-two conditional null, order-three conditional information and sufficiency, positive failure witness",
            "stationary one-step material equality to H0 and stationary triple equality; no full-clock order assignment",
            "symbolic even/odd slot-chain factorisation; no new initial-history decay study",
        ],
        "items": items(),
        "work_counts":{"atomic_items":12,"grades":3,"recurrent_states_per_grade":2304,
                       "transitions_per_grade":13824,"generic_refinement_runs_with_reverse":6,
                       "forward_quadruple_terms_per_grade":2304*6**3,
                       "backward_word_terms_per_grade":2304*6,
                       "raw_triad_absorption_rows_per_grade":3*5*16,
                       "covariance_comparisons_per_grade":24*(36*6+64*6),
                       "same_mask_history_pairs_per_non_neutral_grade":64*630},
        "externally_predeclared_expectations_not_algorithm_inputs":{
            "non_neutral_refinement":[64,384,2304],"neutral_refinement":[64],
            "uniform_stationary":"1/2304","pair_mask_order_non_neutral":3,"event_slot_order_non_neutral":2,
            "adjacent_nulls":"exact","lag_two_repeat":"m/(m+5)",
        },
        "precision_decimal_digits":PRECISION,"logarithm":"natural","information_unit":"nats",
        "tolerances":{"rational_identities":"exact","row_sums":"exact","stationary_residual":"exact",
                      "uniform_joint_gap":"exact","refinement_membership":"exact","conditional_independence":"exact",
                      "order_sufficiency":"exact","information_formula_enumeration_gap":"1e-25"},
        "pre_freeze_exposure":calibration,
        "engineering":{"workers":1,"numeric_threads":1,"per_item_watchdog_seconds":120,
                       "disk_budget_bytes":64_000_000,"neutral_total_seconds":sum(r["wall_seconds"] for r in calibration["neutral_measurements"]),
                       "estimated_total_seconds":max(180,12*sum(r["wall_seconds"] for r in calibration["neutral_measurements"])),
                       "resume":"complete hash-valid matching envelopes only; never replace valid completed items",
                       "on_unexpected_result":"retain failed envelope, stop interpretation, explicit frozen amendment if required"},
        "source_sha256":{p:sha256_file(root/p) for p in SOURCES},
        "input_sha256":{p:sha256_file(root/p) for p in INPUTS},
        "calibration_sha256":sha256_file(root/CALIBRATION),
        "planning_coherence_sha256":sha256_bytes(canonical_ledger_bytes(root/"constraint-lab/coherence")),
    }
    document["plan_hash"] = plan_hash(document)
    atomic_write_json(root/PLAN,document)
    return document


def require_execution(root, commit):
    plan = require_frozen_plan(root,commit,PLAN,root/PLAN)
    if not remote_contains(root,commit):
        raise FrozenPlanError("H2-0 plan must be pushed before targets")
    if plan["analysis_version"] != VERSION or plan["items"] != items():
        raise FrozenPlanError("H2 analysis/item drift")
    for field in ("source_sha256","input_sha256"):
        for path,value in plan[field].items():
            if sha256_file(root/path) != value:
                raise FrozenPlanError("frozen artifact drift: "+path)
    if sha256_file(root/CALIBRATION) != plan["calibration_sha256"]:
        raise FrozenPlanError("neutral calibration drift")
    return plan


def load_envelope(root,item,plan,commit):
    envelope = read_json(root/OUTPUT/(item["item_id"]+".json"))
    if (envelope["item"] != item or envelope["plan_hash"] != plan["plan_hash"]
            or envelope["frozen_analysis_plan_commit"] != commit or envelope["analysis_version"] != VERSION
            or envelope["result_sha256"] != digest(envelope["result"])):
        raise HistoryError("cached H2 item mismatch")
    validate_result(item,envelope["result"])
    return envelope


def publish(root,envelopes,plan,commit):
    hashes = {}
    for kind in ANALYSES:
        data = []
        for e in envelopes:
            if e["item"]["kind"] != kind:
                continue
            excluded = {"kernel","stable_blocks","chronology","stationary_triples","stationary_quadruples"}
            data.append({k:v for k,v in e["result"].items() if k not in excluded})
        path = TABLE+kind+".json"
        atomic_write_json(root/path,{"clock":CLOCK,"data":data})
        hashes[path]=sha256_file(root/path)
    summary = {
        "round_id":"H2-0","prompt_id":"008L","status":"COMPLETE","analysis_version":VERSION,"clock":CLOCK,
        "frozen_analysis_plan_commit":commit,"plan_hash":plan["plan_hash"],"plan_file_sha256":sha256_file(root/PLAN),
        "item_sha256":{OUTPUT+"/"+e["item"]["item_id"]+".json":sha256_file(root/OUTPUT/(e["item"]["item_id"]+".json")) for e in envelopes},
        "table_sha256":hashes,"timings":{e["item"]["item_id"]:e["wall_seconds"] for e in envelopes},
        "atomic_items":12,"precision_decimal_digits":PRECISION,"new_non_neutral_H2_pre_freeze_executions":0,
        "stochastic_scientific_trajectories":0,
    }
    atomic_write_json(root/MANIFEST,summary)
    return summary


def execute(root,commit):
    plan,envelopes = require_execution(root,commit),[]
    for item in plan["items"]:
        path = root/OUTPUT/(item["item_id"]+".json")
        if path.exists():
            envelope = load_envelope(root,item,plan,commit)
        else:
            atomic_write_json(root/DIRECTORY/"status.json",{"status":"RUNNING","completed":len(envelopes),"item":item["item_id"]})
            start=time.monotonic()
            with watchdog(plan["engineering"]["per_item_watchdog_seconds"]):
                result = ANALYSES[item["kind"]](SecondRecent(F(item["m"])))
            envelope={"item":item,"analysis_version":VERSION,"plan_hash":plan["plan_hash"],
                      "frozen_analysis_plan_commit":commit,"result":result,"result_sha256":digest(result),
                      "wall_seconds":time.monotonic()-start}
            try:
                validate_result(item,result)
            except Exception:
                atomic_write_json(path.with_suffix(".failed.json"),envelope)
                raise
            atomic_write_json(path,envelope)
            envelope=read_json(path)
        envelopes.append(envelope)
        if sum(p.stat().st_size for p in (root/OUTPUT).glob("*.json")) > plan["engineering"]["disk_budget_bytes"]:
            raise HistoryError("frozen disk budget exceeded")
        print("COMPLETE",item["item_id"],f"{envelope['wall_seconds']:.3f}s",flush=True)
    result=publish(root,envelopes,plan,commit)
    atomic_write_json(root/DIRECTORY/"status.json",{"status":"COMPLETE","completed":12})
    return result


def verify(root,commit):
    plan=require_execution(root,commit)
    manifest=read_json(root/MANIFEST)
    if manifest["status"] != "COMPLETE" or manifest["plan_hash"] != plan["plan_hash"]:
        raise HistoryError("incomplete H2 publication")
    for path,value in {**manifest["item_sha256"],**manifest["table_sha256"]}.items():
        if sha256_file(root/path) != value:
            raise HistoryError("H2 publication hash mismatch: "+path)
    for item in plan["items"]:
        r=decode(load_envelope(root,item,plan,commit)["result"])
        if item["kind"] == "kernel":
            rows=[dict(row) for row in r["kernel"]]
            if digest([sorted(row.items()) for row in SecondRecent(F(item["m"])).epoch_kernel()]) != r["kernel_sha256"]:
                raise HistoryError("independent sparse-kernel replay failed")
            if balance_gap([F(1,2304)]*2304,rows):
                raise HistoryError("stationary certificate replay failed")
        if item["kind"] == "refinement":
            rows=SecondRecent(F(item["m"])).epoch_kernel()
            if lumpability(rows,r["stable_blocks"])[1] or digest(r["stable_blocks"]) != r["membership_sha256"]:
                raise HistoryError("refinement certificate replay failed")
        if item["kind"] == "temporal":
            if sum(row["probability"] for row in r["stationary_quadruples"]) != 1:
                raise HistoryError("stationary word certificate replay failed")
    return {"status":"VERIFIED","atomic_items":12,"plan_hash":plan["plan_hash"]}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=("calibrate","plan","execute","verify"))
    parser.add_argument("--frozen-plan-commit")
    args=parser.parse_args()
    root=repository_root()
    if args.command == "calibrate":
        result=calibrate(root)
    elif args.command == "plan":
        result=write_plan(root)
    else:
        result=(execute if args.command == "execute" else verify)(root,args.frozen_plan_commit)
    print(json.dumps(result,default=str,sort_keys=True))


if __name__ == "__main__":
    main()
