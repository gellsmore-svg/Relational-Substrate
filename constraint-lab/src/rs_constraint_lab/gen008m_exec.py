"""Freeze-gated single-worker M0 supervisor, resume and exact verification."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import time

from flint import fmpq as Q

from rs_constraint_lab.durable import atomic_write_json, sha256_file
from rs_constraint_lab.explore08 import plan_hash, remote_contains, require_frozen_plan
from rs_constraint_lab.h2_roles import (
    VERSION, PRECISION, STATES, RoleController, analyse_stationary, augmented_atlas,
    augmented_structure, canonical, covariance_check, fingerprint, kernel_from_events,
    lift, ln, number, quotient, ready, residual, role_structure, stationary,
)
from rs_constraint_lab.h2_role_words import analyse_words, word_orbits
from rs_constraint_lab.history import HistoryError

BASE = "147d3156e396f92e3a4a12252468e5fc9dced8cd"
DIRECTORY = "constraint-lab/exploration/generation-008m"
PLAN = DIRECTORY + "/round-m0-plan.json"
OUTPUT = "constraint-lab/reports/items/generation-008m-m0"
TABLE = "constraint-lab/reports/tables/generation-008m-"
SOURCES = tuple("constraint-lab/src/rs_constraint_lab/"+name for name in (
    "h2_roles.py","h2_role_words.py","gen008m_exec.py","durable.py","explore08.py",
    "graphs.py","state.py","exact.py","history.py",
)) + ("constraint-lab/pyproject.toml",)
INPUTS = (DIRECTORY+"/charter.md",DIRECTORY+"/open-thetical-possibilities.md",
          DIRECTORY+"/predeclared-expectations.md","constraint-lab/tests/test_v08m_plumbing.py",
          "constraint-lab/provenance/prompts/008M-v0.8m-agent-input.md",
          TABLE+"h2-role-atlas.json",TABLE+"augmented-s4-orbits.json")


def root():
    return Path(__file__).resolve().parents[3]


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path,value):
    atomic_write_json(path,ready(value))


def items():
    result = [{"item_id":"M0-NEUTRAL","role":0,"family":"ANY","m":"1"}]
    for family in ("ANY","FORM","DISSOLVE"):
        for role in range(12):
            for grade,m in (("m025","1/4"),("m4","4")):
                result.append({"item_id":f"M0-{family}-R{role:02d}-{grade}",
                               "role":role,"family":family,"m":m})
    return result


def structural_outputs(repository):
    role_atlas = role_structure()[0]
    orbit_atlas = augmented_atlas()
    if len(role_atlas)!=12 or len(orbit_atlas)!=120:
        raise HistoryError("independent orbit expectation differs: stop")
    if Counter(row["orbit_size"] for row in orbit_atlas)!={6:16,12:24,24:80}:
        raise HistoryError("augmented orbit sizes differ: stop")
    for suffix,content in (("h2-role-atlas.json",role_atlas),("augmented-s4-orbits.json",orbit_atlas)):
        path = repository/(TABLE+suffix)
        if path.exists() and read(path)!=ready(content):
            raise HistoryError("refusing to replace structural atlas")
        if not path.exists():
            write(path,content)
    return role_atlas,orbit_atlas


def calibrate(repository):
    path = repository/DIRECTORY/"calibration.json"
    if path.exists() or (repository/PLAN).exists():
        raise HistoryError("calibration is one-time before freeze")
    structural_outputs(repository)
    start = time.monotonic()
    result,data = analyse_stationary(RoleController(0,"ANY","1"),independent_solve=True)
    stationary_seconds = time.monotonic()-start
    start = time.monotonic()
    words = analyse_words(*data,max_length=6,independent=True)
    word_seconds = time.monotonic()-start
    if any(not row["exact_equal"] for row in words["word_summaries"]):
        raise HistoryError("neutral all-word equality failed")
    # Synthetic dense 120-state rational balance, not a ROLE controller.
    synthetic = tuple({j:Q((i+2*j)%13+1,1) for j in range(120)} for i in range(120))
    synthetic = tuple({j:w/sum(row.values()) for j,w in row.items()} for row in synthetic)
    start = time.monotonic()
    synthetic_pi = stationary(synthetic)
    synthetic_seconds = time.monotonic()-start
    if residual(synthetic_pi,synthetic):
        raise HistoryError("synthetic stationary solve failed")
    value = {
        "new_non_neutral_8M_targets_executed":0,"neutral_stationary_seconds":stationary_seconds,
        "neutral_words_L1_L6_seconds":word_seconds,"neutral_item_bytes":len(canonical(result).encode()),
        "synthetic_dense_120_solve_seconds":synthetic_seconds,
        "word_support":[{"length":l,"S4_records":len(word_orbits(l)),
                         "labelled_words":sum(size for _,size in word_orbits(l))} for l in range(1,7)],
        "historical_regressions":"test_v08l_plumbing.py (published H1/H2 only); no new non-neutral ROLE",
        "engineering_test_correction":"pre-freeze neutral decimal string parsed as Decimal, not fmpq; no scientific exposure",
        "workers":1,"numeric_threads":1,"timeout_seconds_per_item":300,
        "estimate_seconds_per_primary_item":max(5*(stationary_seconds+word_seconds),30),
        "disk_budget_bytes":300_000_000,
    }
    write(path,value)
    print(json.dumps(value,indent=2),flush=True)


def make_plan(repository):
    path = repository/PLAN
    if path.exists():
        raise HistoryError("refusing to replace frozen plan")
    cal = read(repository/DIRECTORY/"calibration.json")
    value = {
        "experiment_id":"generation-008m-h2-structural-consequence","round_id":"M0","prompt_id":"008M",
        "analysis_version":VERSION,"parent_commit":BASE,"mode":"OTR bounded palette / Mode A exact cells",
        "ontology":{"N":4,"O":3,"G":0,"S":0,"L":0,"H_pair":2,"hypergraph":"independent"},
        "clock":"pair-event epoch","ordinary_support":"six pair and four triad single toggles",
        "controller":"one ordered S4 role indicator, optionally conjoined with FORM or DISSOLVE; selected weight m, otherwise 1",
        "sentinel":"if either unavailable all weights 1; pair update (e,h1); triad update identity",
        "triad_closure":"unit triad weights, no triad read, pair weights unchanged during triad excursions",
        "compiler":{"H1_state":"exactly complete X and most recent pair identity h1",
                    "allow":["arbitrary positive K/J"],"exclude":["hidden state","phase","persistent seed",
                    "expanded/re-encoded history alphabet","changed support","changed clock","per-history programme"],
                    "equivalence":"all reachable conditioned pair/full rows; strong projection to (P,h1)",
                    "augmentation":"allowed at raw kernel level, not semantic H1"},
        "items":items(),"non_neutral_primary_systems":72,"neutral_baselines":1,
        "stationary_method":"python-flint 0.8.0 exact 120-state fmpq_mat dixon solve; fflu independent solve EVERY item; full 2304 sparse residual",
        "stationary_symmetry":"generated kernel all 24 permutations, all states/events; all orbit-member block sums exact",
        "H1_comparators":{"KU":"uniform average of NORMALISED H2 rows over h2; exact 28-orbit H1 solve, full 384 residual",
                          "Kpi":"stationary conditional pi(h2|P,h1) average; exact one/two-time H1 joint and balance",
                          "H0":"not opened; redundant for declared depth-specific question"},
        "stationary_estimands":["P","edge count","graph class","ordered history pair","orbit joint","P,h1",
            "strict H2/H1 strong-lumping classification and explicit witness","neutral exact density/shape categories",
            "KL pair/class/count plus direct conditional shape and chain gap","I(P;H1)","I(P;H2|H1)",
            "I(P;H1,H2)","I(H1;H2)","experienced h2 expected KL to uniform",
            "H2 versus KU exact laws, KL density/shape and JS","Kpi H1 exact adjacent equality"],
        "words":{"lengths":[1,2,3,4,5,6],"projections":["pair_mask","graph_class","edge_count"],
                 "orientation":"stationary forward (Y_0,...,Y_(L-1))",
                 "encoding":"S4 orbit-canonical labelled-mask words with exact per-word mass and orbit size; deterministic expansion",
                 "coarse_encoding":"aggregate complete mask-word census by graph class or edge count",
                 "metrics":["positive support counts","exact normalization","canonical exact distribution SHA256",
                            "equal-prior JS nats","maximum rational probability gap","lexicographic first maximum word",
                            "first exact distinguishing length, or none through 6"],
                 "independent_check":"direct hidden-state forward propagation through L4 EVERY item",
                 "matched_controls":"L1/L2 mandatory; derived L3 material matching also exact; neutral all lengths"},
        "formal_expectations_not_algorithm_inputs":{"roles":12,"direction_cells":24,"S4_augmented_orbits":120,
            "orbit_size_counts":{"6":16,"12":24,"24":80},"ANY":"product uniform material x stationary history",
            "complement":"FORM/DISSOLVE conjugacy","support":"one recurrent class, period two",
            "word_L3":"adjacent H1 matching plus register recovery implies material triples match"},
        "precision_decimal_digits":PRECISION,"logarithm":"natural","information_unit":"nats",
        "tolerances":{"rational_identities":"exact","classification":"exact distribution equality",
                      "stationary_residual":"exact","quotient":"exact","word_normalization":"exact",
                      "matched_laws":"exact","information_chain_gap":"1e-25"},
        "resources":cal,"execution":{"workers":1,"numeric_threads":1,"watchdog_seconds":300,
            "heartbeat_seconds":5,"resume":"skip only valid matching freeze/source/payload hashes",
            "atomic_write":"existing fsync/parse/replace durable API","retry":"no automatic scientific retries",
            "quarantine":"retain separate failure receipt, stop supervisor, preserve all completed items",
            "split":"if time/memory limit reached stop; freeze engineering amendment before splitting stage, never change scientific depth/estimands",
            "merge":"restartable deterministic summary assembly, complement check both executed partners"},
        "pre_freeze_exposure":{"new_non_neutral_8M_primary_cells":0,"calibration":"neutral and synthetic only",
            "prior_related":"8L and alternate H1 role/coarse branches known; not blind to generic structural possibility",
            "not_imported":"no alternate scientific output copied into M0"},
        "input_hashes":{p:sha256_file(repository/p) for p in INPUTS},
        "source_hashes":{p:sha256_file(repository/p) for p in SOURCES},
    }
    value["plan_hash"] = plan_hash(value)
    write(path,value)
    print("PLAN",value["plan_hash"],sha256_file(path),flush=True)


def gate(repository,freeze):
    plan = require_frozen_plan(repository,freeze,PLAN,repository/PLAN)
    if not remote_contains(repository,freeze):
        raise HistoryError("M0 execution requires pushed plan")
    for path,digest in (plan["input_hashes"] | plan["source_hashes"]).items():
        if sha256_file(repository/path)!=digest:
            raise HistoryError(f"frozen source/input drift: {path}")
    if plan["analysis_version"]!=VERSION:
        raise HistoryError("analysis version mismatch")
    return plan


def valid_item(path,item,plan,freeze):
    if not path.exists():
        return False
    value = read(path)
    if (value.get("item")!=item or value.get("frozen_analysis_plan_commit")!=freeze or
        value.get("plan_hash")!=plan["plan_hash"] or fingerprint(value["result"])!=value.get("result_hash")):
        raise HistoryError(f"invalid existing item, do not overwrite: {path}")
    return True


def worker(repository,freeze,item_id):
    plan = gate(repository,freeze)
    item = next(x for x in plan["items"] if x["item_id"]==item_id)
    path = repository/OUTPUT/(item_id+".json")
    if valid_item(path,item,plan,freeze):
        print("RESUME",item_id,flush=True)
        return
    start = time.monotonic()
    print("STATIONARY",item_id,flush=True)
    result,data = analyse_stationary(RoleController(item["role"],item["family"],item["m"]),independent_solve=True)
    print("WORDS",item_id,round(time.monotonic()-start,3),flush=True)
    result["words"] = analyse_words(*data,max_length=6,independent=True)
    if item["m"]=="1" and any(not x["exact_equal"] for x in result["words"]["word_summaries"]):
        raise HistoryError("neutral all-length control failed")
    value = {"item":item,"frozen_analysis_plan_commit":freeze,"plan_hash":plan["plan_hash"],
             "source_hashes":plan["source_hashes"],"result":ready(result),"result_hash":fingerprint(result),
             "wall_seconds":time.monotonic()-start,"status":"VERIFIED"}
    size = sum(p.stat().st_size for p in (repository/OUTPUT).glob("*.json"))
    if size+len(canonical(value).encode()) > plan["resources"]["disk_budget_bytes"]:
        raise HistoryError("frozen disk budget exceeded; stop before publishing item")
    write(path,value)
    ln.cache_clear()
    print("DONE",item_id,round(value["wall_seconds"],3),value["result_hash"],flush=True)


def run(repository,freeze,only=None):
    plan = gate(repository,freeze)
    selected = [item for item in plan["items"] if only is None or item["item_id"]==only]
    if not selected:
        raise HistoryError("unknown selected item")
    for item in selected:
        item_id = item["item_id"]
        if valid_item(repository/OUTPUT/(item_id+".json"),item,plan,freeze):
            print("RESUME",item_id,flush=True)
            continue
        process = subprocess.Popen([sys.executable,"-m","rs_constraint_lab.gen008m_exec","worker",
                                    "--freeze",freeze,"--item",item_id],cwd=repository)
        start = time.monotonic()
        while process.poll() is None:
            elapsed = time.monotonic()-start
            write(repository/DIRECTORY/"status.json",{"active_item":item_id,"elapsed_seconds":elapsed,
                    "frozen_analysis_plan_commit":freeze,"state":"running","workers":1})
            if elapsed>plan["execution"]["watchdog_seconds"]:
                process.kill()
                process.wait()
                break
            time.sleep(5)
        if process.returncode:
            write(repository/DIRECTORY/"quarantine"/(item_id+".json"),{
                "item":item,"returncode":process.returncode,"elapsed_seconds":time.monotonic()-start,
                "state":"quarantined","notes":"Completed valid items retained. Diagnose and amend before methodological change."})
            raise HistoryError(f"item quarantined: {item_id}")
    write(repository/DIRECTORY/"status.json",{"state":"selected_items_complete","frozen_analysis_plan_commit":freeze,
                                           "selected_items":len(selected)})


def verify_merge(repository,freeze):
    plan = gate(repository,freeze)
    results,summary = {},[]
    for item in plan["items"]:
        path = repository/OUTPUT/(item["item_id"]+".json")
        if not valid_item(path,item,plan,freeze):
            raise HistoryError(f"missing item {item['item_id']}")
        value = read(path)
        r = value["result"]
        events = RoleController(item["role"],item["family"],item["m"]).event_rows()
        pi = lift(tuple(Q(v) for v in r["stationary_orbit_masses"]))
        if residual(pi,kernel_from_events(events)):
            raise HistoryError("independent reassembly full sparse stationary residual")
        if r["full_stationary_residual"]!="0" or r["Kpi_H1"]["adjacent_law_gap"]!="0":
            raise HistoryError("nonzero exact validation gap")
        if any(w["exact_normalization_H2"]!="1" or w["exact_normalization_Kpi_H1"]!="1"
               for w in r["words"]["word_summaries"]):
            raise HistoryError("word normalization receipt differs")
        results[item["item_id"]] = value
        summary.append({"system_id":item["item_id"],**item,
            "strict_H2":r["strict_H2"],**r["neutral_comparison"],
            "stationary_information":r["stationary_information"],
            "uniform_H1_comparison":r["uniform_H1_comparison"],
            "first_word_difference":r["words"]["first_difference"],
            "Kpi_H1_adjacent_gap":r["Kpi_H1"]["adjacent_law_gap"],
            "stationary_residual":r["full_stationary_residual"],
            "result_hash":value["result_hash"],"wall_seconds":value["wall_seconds"]})
    complement = []
    _,lookup = augmented_structure()
    for role in range(12):
        for grade in ("m025","m4"):
            a,b = (results[f"M0-{family}-R{role:02d}-{grade}"]["result"] for family in ("FORM","DISSOLVE"))
            multiplier = "1/4" if grade=="m025" else "4"
            form = RoleController(role,"FORM",multiplier)
            dissolve = RoleController(role,"DISSOLVE",multiplier)
            if any(form.probabilities(p,i,j)!=dissolve.probabilities(p^63,i,j) for p,i,j in STATES):
                raise HistoryError("explicit FORM/DISSOLVE kernel map differs")
            pa = lift(tuple(Q(v) for v in a["stationary_orbit_masses"]))
            pb = lift(tuple(Q(v) for v in b["stationary_orbit_masses"]))
            if any(pa[s]!=pb[((p^63)*6+i)*6+j] for s,(p,i,j) in enumerate(STATES)):
                raise HistoryError("FORM/DISSOLVE stationary complement differs")
            if any(a["words"]["word_summaries"][n]["JS"]!=b["words"]["word_summaries"][n]["JS"]
                   for n in range(18)):
                # Log summation can differ only below frozen numerical gap.
                import mpmath as mp
                if any(abs(mp.mpf(x["JS"])-mp.mpf(y["JS"]))>mp.mpf("1e-25")
                       for x,y in zip(a["words"]["word_summaries"],b["words"]["word_summaries"])):
                    raise HistoryError("complement word information differs")
            complement.append({"role":role,"grade":grade,"stationary_exact":True,
                               "kernel_exact":True,
                               "word_information_agrees":True})
    words = [{"system_id":key,**row} for key,value in results.items()
             for row in value["result"]["words"]["word_summaries"]]
    equivalent = {}
    for label,key in (("kernel","kernel_fingerprint"),):
        groups = defaultdict(list)
        for identity,value in results.items():
            groups[value["result"][key]].append(identity)
        equivalent[label] = list(groups.values())
    for label,key in (("stationary_material","stationary_P"),("stationary_joint","stationary_orbit_masses")):
        groups = defaultdict(list)
        for identity,value in results.items():
            groups[fingerprint(value["result"][key])].append(identity)
        equivalent[label] = list(groups.values())
    for suffix,content in (("summary.json",summary),("word-atlas.json",words),
            ("complement.json",complement),("equivalences.json",equivalent)):
        write(repository/(TABLE+suffix),content)
    validation = {"status":"VERIFIED","items":len(results),"non_neutral":72,"neutral":1,
        "full_sparse_stationary_residuals_exact":len(results),"complement_pairs":24,
        "word_rows":len(words),"plan_hash":plan["plan_hash"],"frozen_analysis_plan_commit":freeze,
        "payload_hashes":{key:value["result_hash"] for key,value in results.items()},
        "table_hashes":{suffix:sha256_file(repository/(TABLE+suffix)) for suffix in
                        ("summary.json","word-atlas.json","complement.json","equivalences.json")}}
    write(repository/(TABLE+"validation.json"),validation)
    print("VERIFIED",len(results),"items",fingerprint(validation),flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("calibrate","plan","run","worker","verify"))
    parser.add_argument("--freeze")
    parser.add_argument("--item")
    args = parser.parse_args()
    repository = root()
    if args.action=="calibrate":
        calibrate(repository)
    elif args.action=="plan":
        make_plan(repository)
    elif args.action=="run":
        run(repository,args.freeze,args.item)
    elif args.action=="worker":
        worker(repository,args.freeze,args.item)
    else:
        verify_merge(repository,args.freeze)


if __name__=="__main__":
    main()
