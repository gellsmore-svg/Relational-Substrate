"""Pre-freeze combinatorial, neutral and synthetic tests; no ROLE target."""

from collections import Counter
from decimal import Decimal
from itertools import product

import pytest

pytest.importorskip("flint")
from flint import fmpq as Q
from rs_constraint_lab.h2_roles import (
    MASK_MAPS, SLOT_MAPS, STATES, RoleController, analyse_stationary,
    augmented_structure, covariance_check, kernel_from_events, quotient,
    relation, role_of, role_structure, stationary,
)
from rs_constraint_lab.h2_role_words import analyse_words, direct_word, word_orbits
from rs_constraint_lab.history import HistoryError


def test_independent_role_orbits_and_ternary_split():
    atlas,_ = role_structure()
    assert len(atlas)==12
    assert Counter(r["orbit_size"] for r in atlas)=={6:4,24:8}
    assert sum(r["orbit_size"] for r in atlas)==216
    seen = {tuple(t) for r in atlas for t in r["orbit"]}
    assert seen == set(product(range(6),repeat=3))
    # Independent classification: equalities, pair intersections and common
    # vertex distinguish every orbit, including STAR versus TRIANGLE.
    descriptors = {}
    for h1,h2,e in seen:
        common = bool(set(((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))[h1]) &
                      set(((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))[h2]) &
                      set(((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))[e]))
        key = relation(h1,h2),relation(h1,e),relation(h2,e),common
        descriptors.setdefault(key,set()).add(role_of(h1,h2,e))
    assert len(descriptors)==12 and all(len(v)==1 for v in descriptors.values())
    assert atlas[5]["ternary_discriminator"]=="STAR"
    assert atlas[6]["ternary_discriminator"]=="TRIANGLE"
    assert [r["role_id"] for r in atlas if r["candidate_equals_h2"]]==["R00","R04","R11"]
    assert [r["role_id"] for r in atlas if r["candidate_equals_h1"]]==["R00","R03","R09"]


def test_augmented_orbits_and_burnside_count():
    blocks,lookup = augmented_structure()
    assert len(blocks)==120
    assert Counter(map(len,blocks))=={6:16,12:24,24:80}
    assert sorted(s for block in blocks for s in block)==list(range(2304))
    fixed = sum(sum(mm[p]==p and sm[i]==i and sm[j]==j for p,i,j in STATES)
                for sm,mm in zip(SLOT_MAPS,MASK_MAPS))
    assert fixed//24==len(blocks) and fixed%24==0
    assert len(augmented_structure(1)[0])==28


def test_structural_role_covariance_all_triples():
    for h1,h2,e in product(range(6),repeat=3):
        for sm in SLOT_MAPS:
            assert role_of(h1,h2,e)==role_of(sm[h1],sm[h2],sm[e])


def test_neutral_and_sentinel_validation_after_valid_call():
    model = RoleController(5,"FORM","1")
    assert model.probabilities(7,1,2)==(Q(1,6),)*6
    assert model.probabilities(7,None,None,full=True)==(Q(1,10),)*10
    assert model.probabilities(7,1,None,full=True)==(Q(1,10),)*10
    for bad in (True,-1,6,"1"):
        with pytest.raises(HistoryError):
            model.probabilities(7,bad,2)
    with pytest.raises(HistoryError):
        model.probabilities(7,None,2)


def test_synthetic_exact_stationary_solver_independent_algorithms():
    rows = ({0:Q(1,3),1:Q(2,3)},{0:Q(1,4),1:Q(3,4)})
    assert stationary(rows)==(Q(3,11),Q(8,11))
    assert stationary(rows,"fflu")==stationary(rows)


@pytest.fixture(scope="module")
def neutral():
    return analyse_stationary(RoleController(0,"ANY","1"),independent_solve=True)


def test_neutral_comparators_and_full_residual(neutral):
    result,data = neutral
    assert result["strict_H2"]=="H1_COMPILABLE"
    assert result["stationary_P"]==(Q(1,64),)*64
    assert result["stationary_orbit_masses"]==tuple(Q(len(b),2304) for b in augmented_structure()[0])
    assert result["neutral_comparison"]["material_class"]=="MATERIAL_SILENT"
    assert result["uniform_H1_comparison"]["pair_equal"]
    assert all(Decimal(v)==0 for v in result["stationary_information"].values())


def test_neutral_word_compression_and_independent_forward(neutral):
    result,data = neutral
    words = analyse_words(*data,max_length=4,independent=True)
    assert all(w["exact_equal"] for w in words["word_summaries"])
    assert all(x is None for x in words["first_difference"].values())
    assert sum(size for _,size in word_orbits(4))==64*6**3
    for word,_ in word_orbits(3):
        assert direct_word(word,*data)==(Q(1,64*36),)*2


def test_published_8l_non_neutral_word_regression_not_new_role():
    from fractions import Fraction
    from rs_constraint_lab.history_depth import SecondRecent
    historical = SecondRecent(Fraction(4))
    events = tuple(tuple(Q(str(v)) for v in historical.pair_probabilities(i,j)) for p,i,j in STATES)
    data = ((Q(1,2304),)*2304,events,(Q(1,384),)*384,((Q(1,6),)*6,)*384)
    words = analyse_words(*data,max_length=4,independent=True)
    assert all(w["exact_equal"] for w in words["word_summaries"] if w["word_length"]<=3)
    assert words["first_difference"]["pair_mask"]==4
