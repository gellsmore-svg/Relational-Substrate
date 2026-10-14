"""Pre-freeze tests: neutral N4 and non-N4 synthetic fixtures only."""

from fractions import Fraction as F
from decimal import Decimal
from itertools import product

import pytest

from rs_constraint_lab.history import HistoryError
from rs_constraint_lab.history_depth import DepthTwoState, SecondRecent, analyse_witness
from rs_constraint_lab.refinement import lumpability, partition_from_labels, refine


def test_two_slot_sentinel_and_pair_clock_updates():
    model = SecondRecent(F(1))
    start = DepthTwoState(0)
    first = model.advance(start, 3)
    assert (first.material, first.h1, first.h2) == (8, 3, None)
    triad = model.advance(first, 8)
    assert (triad.h1, triad.h2) == (3, None)
    second = model.advance(triad, 5)
    assert (second.h1, second.h2) == (5, 3)
    repeated = model.advance(second, 5)
    assert (repeated.h1, repeated.h2) == (5, 5)
    assert model.advance(first, 3).material == 0


@pytest.mark.parametrize("bad", [(None, 0), (6, None), (-1, None), (True, None)])
def test_invalid_history_rejected_without_target_execution(bad):
    with pytest.raises(HistoryError):
        SecondRecent(F(1)).pair_probabilities(*bad)


def test_neutral_all_register_rows_and_index_roundtrip():
    model = SecondRecent(F(1))
    for index in range(model.size):
        mask, h1, h2 = model.epoch_state(index)
        assert model.epoch_index(mask, h1, h2) == index
        assert model.full_probabilities(h1, h2) == (F(1,10),) * 10
        assert model.pair_probabilities(h1, h2) == (F(1,6),) * 6
    assert model.full_probabilities(None, None) == (F(1,10),) * 10
    assert model.full_probabilities(2, None) == (F(1,10),) * 10
    with pytest.raises(HistoryError):
        model.epoch_state(model.size)
    with pytest.raises(HistoryError):
        model.advance(DepthTwoState(0), 10)


def test_synthetic_three_slot_multiplier_two_not_n4_target():
    model = SecondRecent(F(2), pair_slots=3, triad_slots=1)
    assert model.size == 72
    assert model.full_probabilities(0, 2) == (F(1,5), F(1,5), F(2,5), F(1,5))
    assert model.pair_probabilities(0, 2) == (F(1,4), F(1,4), F(1,2))
    assert model.pair_probabilities(1, None) == (F(1,3),) * 3
    rows = model.epoch_kernel()
    result = refine(rows, partition_from_labels([model.epoch_state(s)[0] for s in range(model.size)]))
    assert result["stable_block_count"] == 72
    assert [r["after_count"] for r in result["refinement_chronology"]] == [24,72]
    for h1, h2 in product(range(3), repeat=2):
        assert model.pair_probabilities(h1,h2) == tuple(F(2 if e == h2 else 1,4) for e in range(3))
    assert all(sum(row.values()) == 1 for row in rows)
    assert lumpability(rows, result["stable_blocks"])[1] == 0


def test_neutral_canonical_witness_plumbing():
    value = analyse_witness(SecondRecent(F(1)))
    assert value["same_X"] and value["same_h1"]
    assert value["path_full_probability_A"] == F(1,1000)
    assert value["path_pair_probability_A"] == F(1,216)
    assert all(Decimal(value[k]) == 0 for k in ("pair_row_JS", "full_row_JS", "graph_class_JS"))
    assert value["changed_pair_slots"] == []
