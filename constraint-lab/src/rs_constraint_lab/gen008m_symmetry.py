"""Separately frozen M1: opposite-pair conjugacy of STAR and TRIANGLE."""

from __future__ import annotations

import argparse
from functools import cache
from hashlib import sha256
from pathlib import Path
import time

from flint import fmpq as Q

from rs_constraint_lab.durable import sha256_file
from rs_constraint_lab.explore08 import require_frozen_plan,remote_contains
from rs_constraint_lab.gen008l_exec import watchdog
from rs_constraint_lab.gen008m_exec import DIRECTORY,OUTPUT,TABLE,read,write
from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.h2_roles import (
    PAIRS,STATES,RoleController,canonical,distribution_comparison,fingerprint,lift,role_of,state_index,
)
from rs_constraint_lab.h2_role_words import canonical_word,direct_word,event,word_orbits
from rs_constraint_lab.history import HistoryError

PLAN = DIRECTORY+"/round-m1-plan.json"
OPPOSITE = tuple(next(j for j,b in enumerate(PAIRS) if not set(a)&set(b)) for a in PAIRS)
MASKS = tuple(sum(1<<OPPOSITE[e] for e in range(6) if p>>e&1) for p in range(64))


def probabilities(data):
    pi,events,ph1,kpi = data
    @cache
    def compute(word):
        if len(word)<=3:
            return direct_word(word,*data)
        a,b=compute(word[:-1])
        p=word[-2]
        e=event(p,word[-1])
        i,j=event(word[-3],p),event(word[-4],word[-3])
        return a*events[state_index(p,i,j)][e],b*kpi[p*6+i][e]
    return compute


def restore(repository,identity):
    result=read(repository/OUTPUT/(identity+".json"))["result"]
    model=RoleController(result["controller"]["role"],result["controller"]["family"],result["controller"]["m"])
    data=(lift(tuple(Q(v) for v in result["stationary_orbit_masses"])),model.event_rows(),
          tuple(Q(v) for v in result["stationary_P_H1"]),
          tuple(tuple(Q(v) for v in row) for row in result["Kpi_H1"]["event_rows"]))
    return result,data


def probe(repository):
    mapped_roles={}
    for i in range(6):
        for j in range(6):
            for e in range(6):
                source=role_of(i,j,e)
                mapped_roles.setdefault(source,set()).add(role_of(OPPOSITE[i],OPPOSITE[j],OPPOSITE[e]))
    if any(v!={6 if k==5 else 5 if k==6 else k} for k,v in mapped_roles.items()):
        raise HistoryError("opposite-pair role mapping differs")
    table=pair_classes()
    classes={}
    for p in range(64):
        classes.setdefault(table.name_of[p],set()).add(table.name_of[MASKS[p]])
    if any(len(v)!=1 for v in classes.values()):
        raise HistoryError("opposite pair does not induce a graph-class map")
    records=[]
    for family in ("ANY","FORM","DISSOLVE"):
        for grade in ("m025","m4"):
            ids=[f"M0-{family}-R{r:02d}-{grade}" for r in (5,6)]
            (ra,da),(rb,db)=[restore(repository,identity) for identity in ids]
            for s,(p,i,j) in enumerate(STATES):
                target=state_index(MASKS[p],OPPOSITE[i],OPPOSITE[j])
                if da[0][s]!=db[0][target] or any(da[1][s][e]!=db[1][target][OPPOSITE[e]] for e in range(6)):
                    raise HistoryError("full H2 kernel/stationary conjugacy fails")
            for p in range(64):
                for i in range(6):
                    target=MASKS[p]*6+OPPOSITE[i]
                    if da[2][p*6+i]!=db[2][target]:
                        raise HistoryError("H1 joint transport fails")
                    for e in range(6):
                        if da[3][p*6+i][e]!=db[3][target][OPPOSITE[e]]:
                            raise HistoryError("Kpi conjugacy fails")
                        if Q(ra["KU_H1"]["event_rows"][p*6+i][e])!=Q(rb["KU_H1"]["event_rows"][target][OPPOSITE[e]]):
                            raise HistoryError("KU conjugacy fails")
            fa,fb=probabilities(da),probabilities(db)
            checked=0
            for length in range(1,7):
                digests_a,digests_b=[sha256(),sha256()],[sha256(),sha256()]
                for word,size in word_orbits(length):
                    mapped=canonical_word(tuple(MASKS[p] for p in word))
                    if fa(word)!=fb(mapped):
                        raise HistoryError("exact transformed word probability differs")
                    for model in range(2):
                        digests_a[model].update((canonical([word,size,fa(word)[model]])+"\n").encode())
                        digests_b[model].update((canonical([word,size,fb(word)[model]])+"\n").encode())
                    checked+=1
                for result,digests in ((ra,digests_a),(rb,digests_b)):
                    stored=next(w for w in result["words"]["word_summaries"]
                                if w["projection"]=="pair_mask" and w["word_length"]==length)
                    if [d.hexdigest() for d in digests]!=[stored["H2_hash"],stored["Kpi_H1_hash"]]:
                        raise HistoryError("independent M1 word hashes differ from immutable M0")
            a,b=tuple(Q(v) for v in ra["stationary_P"]),tuple(Q(v) for v in rb["stationary_P"])
            records.append({"family":family,"grade":grade,"systems":ids,
                "kernel_conjugacy_exact":True,"stationary_transport_exact":True,
                "KU_transport_exact":True,"Kpi_transport_exact":True,
                "word_orbits_checked":checked,"independent_M0_word_hashes_reproduced":24,
                "stationary_STAR_vs_TRIANGLE":distribution_comparison(a,b)})
            print("VERIFIED",family,grade,checked,"word orbits",flush=True)
    return {"opposite_slot_map":OPPOSITE,"material_map":MASKS,
            "role_map":{k:next(iter(v)) for k,v in mapped_roles.items()},
            "graph_class_map":{k:next(iter(v)) for k,v in classes.items()},
            "records":records,"scope":"S4-external slot permutation, not vertex relabelling; no new process",
            "word_lengths":[1,2,3,4,5,6],"prior_exposure":"complete M0; explanation tested after separate freeze"}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze",required=True)
    args=parser.parse_args()
    repository=Path(__file__).resolve().parents[3]
    plan=require_frozen_plan(repository,args.freeze,PLAN,repository/PLAN)
    if not remote_contains(repository,args.freeze):
        raise HistoryError("M1 plan must be pushed")
    for path,digest in (plan["source_hashes"]|plan["input_hashes"]).items():
        if sha256_file(repository/path)!=digest:
            raise HistoryError("M1 source/input drift: "+path)
    destination=repository/(TABLE+"m1-opposite-pair.json")
    if destination.exists():
        value=read(destination)
        if value["frozen_analysis_plan_commit"]!=args.freeze or fingerprint(value["result"])!=value["result_hash"]:
            raise HistoryError("invalid existing M1 receipt; do not overwrite")
        print("RESUME M1 verified")
        return
    start=time.monotonic()
    with watchdog(120):
        result=probe(repository)
    write(destination,{"frozen_analysis_plan_commit":args.freeze,"plan_hash":plan["plan_hash"],
          "result":result,"result_hash":fingerprint(result),"wall_seconds":time.monotonic()-start,"status":"VERIFIED"})


if __name__=="__main__":
    main()
