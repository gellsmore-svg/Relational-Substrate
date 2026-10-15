"""Pre-freeze synthetic and neutral passage only; no non-neutral ROLE target."""

from pathlib import Path

import pytest
pytest.importorskip("flint")
from flint import fmpq as Q
from rs_constraint_lab.h2_passage import layers, solve_boundary, analyse
from rs_constraint_lab.gen008m_exec import items

ROOT = Path(__file__).resolve().parents[2]


def test_synthetic_absorption_reward_and_independent_exact_routes():
    rows = ({0: Q(1, 2), 1: Q(1, 2)}, {2: Q(1)}, {2: Q(1)})
    assert solve_boundary(rows, {2: (Q(0),)}, reward=1, independent=True) == ((Q(3),), (Q(1),), (Q(0),))
    assert solve_boundary(rows, {1: (Q(1),), 2: (Q(0),)}, independent=True)[0] == (Q(1),)
    with pytest.raises(Exception):
        solve_boundary(rows, {})


def test_neutral_passage_controls_and_complete_task_domain():
    assert tuple(map(len, layers().values())) == (2, 3, 2)
    r = analyse(ROOT, items()[0], independent=True)
    assert r["controls"]["source_pushforward_match"]
    assert r["controls"]["H1_quotient_states"] == 28
    assert sum(len(v) for v in r["hitting"]["MFPT_differences"].values()) == 10
    assert len(r["hitting"]["committor_differences"]) == 3
    assert all(not v for row in r["hitting"]["MFPT_differences"].values() for v in row.values())
    assert all(not c["routing_active"] and not c["length_active"]
               for layer in r["layers"].values() for c in layer["comparison"].values())
