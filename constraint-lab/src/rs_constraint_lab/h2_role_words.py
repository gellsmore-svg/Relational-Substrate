"""Exact S4-compressed stationary material words for H2 versus Kpi-H1."""

from __future__ import annotations

from collections import defaultdict
from functools import cache
from hashlib import sha256

from flint import fmpq as Q

from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.h2_roles import (
    MASK_MAPS, canonical, fingerprint, js, number, state_index,
)
from rs_constraint_lab.history import HistoryError


@cache
def word_orbits(length):
    if type(length) is not int or length < 1:
        raise HistoryError("positive word length required")
    if length==1:
        words = {(p,) for p in pair_classes().representatives}
    else:
        words = {canonical_word(word+(word[-1] ^ (1<<e),))
                 for word,_ in word_orbits(length-1) for e in range(6)}
    result = []
    for word in sorted(words):
        size = len({tuple(mm[p] for p in word) for mm in MASK_MAPS})
        result.append((word,size))
    if sum(size for _,size in result) != 64*6**(length-1):
        raise HistoryError("word orbit support incomplete")
    return tuple(result)


def canonical_word(word):
    return min(tuple(mm[p] for p in word) for mm in MASK_MAPS)


def event(a,b):
    change = a ^ b
    if not change or change & (change-1):
        raise HistoryError("word step must be one pair toggle")
    return change.bit_length()-1


def distribution_summary(records,projection):
    # Canonical records encode the complete exact distribution; S4 orbits have
    # constant probabilities, so their sizes weight normalization and JS.
    h,b = {},{}
    nh,nb = sha256(),sha256()
    max_gap,representative,count = Q(0),None,0
    for word,size,a,c in records:
        if min(a,c)<=0:
            raise HistoryError("positive support changed")
        nh.update((canonical([word,size,a])+"\n").encode())
        nb.update((canonical([word,size,c])+"\n").encode())
        h[word] = a*size
        b[word] = c*size
        count += size
        if abs(a-c)>max_gap:
            max_gap,representative = abs(a-c),word
    if sum(h.values())!=1 or sum(b.values())!=1:
        raise HistoryError("exact word normalization failed")
    return {"projection":projection,"positive_words_H2":count,"positive_words_Kpi_H1":count,
            "stored_records":len(records),"exact_normalization_H2":"1","exact_normalization_Kpi_H1":"1",
            "H2_hash":nh.hexdigest(),"Kpi_H1_hash":nb.hexdigest(),
            "hash_encoding":"lexicographic [word,orbit_size,per_labelled_word_probability] JSONL" if projection=="pair_mask"
                else "lexicographic [word,1,probability] JSONL",
            "exact_equal":not max_gap,"maximum_exact_probability_gap":max_gap,
            "maximally_separating_word":representative,"JS":number(js(h,b))}


def analyse_words(pi,events,ph1,kpi,max_length=6, independent=False):
    scalar_h,scalar_b = {},{}
    # Initial-history mixtures are needed only before two toggles synchronize
    # the full H2 register in labelled material words.
    first_vectors = {}
    output,first = [],{"pair_mask":None,"graph_class":None,"edge_count":None}
    table = pair_classes()
    for length in range(1,max_length+1):
        records = []
        coarse = {name:defaultdict(lambda:[Q(0),Q(0)]) for name in ("graph_class","edge_count")}
        for word,size in word_orbits(length):
            p0 = word[0]
            if length==1:
                a = sum(pi[state_index(p0,i,j)] for i in range(6) for j in range(6))
                b = sum(ph1[p0*6+i] for i in range(6))
            elif length==2:
                e = event(word[0],word[1])
                vector = tuple(sum(pi[state_index(p0,i,j)]*events[state_index(p0,i,j)][e]
                                   for j in range(6)) for i in range(6))
                first_vectors[word] = vector
                a = sum(vector)
                b = sum(ph1[p0*6+i]*kpi[p0*6+i][e] for i in range(6))
            else:
                prefix,e = word[:-1],event(word[-2],word[-1])
                previous = event(word[-3],word[-2])
                if length==3:
                    a = sum(first_vectors[prefix][i]*events[state_index(word[-2],previous,i)][e]
                            for i in range(6))
                else:
                    older = event(word[-4],word[-3])
                    a = scalar_h[prefix]*events[state_index(word[-2],previous,older)][e]
                b = scalar_b[prefix]*kpi[word[-2]*6+previous][e]
            if independent and length<=4:
                ah,bh = direct_word(word,pi,events,ph1,kpi)
                if (a,b)!=(ah,bh):
                    raise HistoryError("independent direct forward word route differs")
            scalar_h[word],scalar_b[word] = a,b
            records.append((word,size,a,b))
            for name,observations in (("graph_class",tuple(table.name_of[p] for p in word)),
                                       ("edge_count",tuple(p.bit_count() for p in word))):
                coarse[name][observations][0] += size*a
                coarse[name][observations][1] += size*b
        summary = distribution_summary(records,"pair_mask")
        summary["word_length"] = length
        summaries = [summary]
        for name,values in coarse.items():
            record = distribution_summary([(word,1,a,b) for word,(a,b) in sorted(values.items())],name)
            record["word_length"] = length
            summaries.append(record)
        for record in summaries:
            if length<=2 and not record["exact_equal"]:
                raise HistoryError("mandatory matched L1/L2 equality failed")
            # Since h1 is reconstructed by adjacent masks, matching adjacent
            # (P,h1) laws additionally forces every three-mask stationary law.
            if length==3 and not record["exact_equal"]:
                raise HistoryError("derived material L3 equality failed")
            if not record["exact_equal"] and first[record["projection"]] is None:
                first[record["projection"]] = length
        output.extend(summaries)
    return {"clock":"pair-event epoch","orientation":"(Y_0,...,Y_(L-1)), stationary forward",
            "max_length":max_length,"word_summaries":output,"first_difference":first,
            "independent_forward_through_L4":independent}


def direct_word(word,pi,events,ph1,kpi):
    p = word[0]
    h = {(i,j):pi[state_index(p,i,j)] for i in range(6) for j in range(6)}
    b = {i:ph1[p*6+i] for i in range(6)}
    for next_p in word[1:]:
        e = event(p,next_p)
        next_h,next_b = defaultdict(Q),defaultdict(Q)
        for (i,j),mass in h.items():
            next_h[e,i] += mass*events[state_index(p,i,j)][e]
        for i,mass in b.items():
            next_b[e] += mass*kpi[p*6+i][e]
        h,b,p = dict(next_h),dict(next_b),next_p
    return sum(h.values()),sum(b.values())
