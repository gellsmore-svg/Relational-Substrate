"""Identity fixtures and definition checks.

These tests do not execute the RRC-001 cells. Soft-wedge and hard-wedge
lumpability are not computed here. The balance lemma and the hard-wedge
deadlock check explain cells that have already been run. The three hand
states below only lock the weight definition.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

from rrc import SIX_CLAIMS
from rrc.items import execute_lumpability, execute_propagation
from rrc.model import (
    build_weights,
    edge_list,
    grammar_form,
    lumpability,
    lumpable_closure,
    pair_depth,
    partition_labels,
    recurrent_class_count,
    stationary_balanced,
    stationary_dense,
)

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "constraint-lab" / "src"))


def test_six_claims_stay_distinct():
    assert len(SIX_CLAIMS) == 4
    assert len(set(SIX_CLAIMS)) == 4


def test_engine_does_not_special_case_six_nodes():
    root = Path(__file__).resolve().parents[1] / "src" / "rrc"
    sources = [path.read_text(encoding="utf-8") for path in sorted(root.glob("*.py"))]
    assert sources
    for source in sources:
        assert "n == 6" not in source
        assert "n==6" not in source


def test_path_index_is_not_complete_graph_distance():
    assert pair_depth([(2, 3), (0, 5)]) == [2, 0]


def test_unconstrained_interface_is_exactly_lumpable():
    spec = {
        "id": "fixture-r0",
        "round_id": "fixture",
        "n": 4,
        "role": "identity_check",
        "identity_check": True,
        "rule": {"family": "unconstrained"},
        "partition": {"kind": "hide_subset", "members": [0, 1, 2]},
        "augmentations": ["edge_count", "parity"],
        "closure": True,
    }
    result = execute_lumpability(spec)
    assert result["status"] == "complete"
    assert result["exact"] is True
    assert result["defect_l1"]["num"] == "0"
    assert result["identity"]["ok"] is True
    assert result["grammar"]["form"] == "unconstrained_lazy"
    assert result["grammar"]["event_shape"] == "single_toggle_or_hold"
    assert result["classes"]["recurrent_classes"] == 1
    assert result["classes"]["deadlock_states"] == 0
    assert result["closure"]["n_blocks"] == result["n_blocks"]
    for name in ("edge_count", "parity"):
        assert result["augmentations"][name]["exact"] is True


def test_unequal_state_independent_rates_stay_lumpable_and_reweight():
    spec = {
        "id": "fixture-rates",
        "round_id": "fixture",
        "n": 3,
        "role": "identity_check",
        "identity_check": True,
        "rule": {
            "family": "state_independent_rates",
            "incident_node": 0,
            "incident_weight": 5,
            "other_weight": 1,
        },
        "partition": {"kind": "hide_subset", "members": [0, 1]},
        "augmentations": [],
        "closure": True,
    }
    result = execute_lumpability(spec)
    assert result["exact"] is True
    assert result["identity"]["ok"] is True
    assert result["grammar"]["form"] == "reweighted_single_toggle"


def test_synthetic_kernel_detects_a_lumpability_failure():
    weights = np.zeros((4, 2), dtype=np.int32)
    weights[0, 0] = 1
    weights[2, 1] = 1
    weights[1, 0] = 1
    weights[3, 0] = 1
    labels = [state & 1 for state in range(4)]
    report = lumpability(weights, labels)
    assert report["exact"] is False
    assert report["defect_l1"] > 0
    closed = lumpable_closure(weights, labels)
    assert closed["exact"] is True
    assert closed["n_blocks"] > 2


def test_synthetic_kernel_accepts_a_lumpable_partition():
    weights = np.zeros((4, 2), dtype=np.int32)
    weights[:, 0] = 1
    labels = [state & 1 for state in range(4)]
    assert lumpability(weights, labels)["exact"] is True


def test_full_state_partition_is_lumpable():
    weights = np.zeros((4, 2), dtype=np.int32)
    weights[:, 0] = 1
    labels = list(range(4))
    report = lumpability(weights, labels)
    assert report["exact"] is True
    assert lumpable_closure(weights, labels)["n_blocks"] == 4


def test_halt_self_loops_are_recurrent_and_not_events():
    weights = np.zeros((4, 2), dtype=np.int32)
    classes = recurrent_class_count(weights)
    assert classes["deadlock_states"] == 4
    assert classes["recurrent_classes"] == 4
    assert classes["halt_completion"] == "halt_self_loop"


def test_wedge_weight_definition_on_three_states():
    hard = build_weights(3, {"family": "hard_wedge_formation"})
    assert hard[0].tolist() == [0, 0, 0]
    assert hard[1].tolist() == [1, 0, 0]
    assert hard[7].tolist() == [1, 1, 1]
    soft = build_weights(3, {"family": "soft_wedge", "common_weight": 4, "base_weight": 1})
    assert soft[0].tolist() == [1, 1, 1]
    assert soft[3].tolist() == [1, 1, 4]
    assert soft[7].tolist() == [4, 4, 4]


def test_cesaro_matches_dense_solve_on_a_calibration_chain():
    weights = build_weights(3, {"family": "calibration_weights"})
    cesaro = stationary_balanced(weights, "empty", 1e-12, 20000)
    other = stationary_balanced(weights, "uniform", 1e-12, 20000)
    dense = stationary_dense(weights)
    assert cesaro["converged"] and other["converged"]
    assert np.abs(cesaro["distribution"] - other["distribution"]).sum() < 1e-8
    assert np.abs(cesaro["distribution"] - dense).sum() < 1e-8


def test_propagation_identity_for_state_independent_rates():
    spec = {
        "id": "fixture-propagation",
        "round_id": "fixture",
        "type": "propagation",
        "n": 3,
        "role": "identity_check",
        "identity_check": True,
        "tolerance": 1e-12,
        "cross_tolerance": 1e-8,
        "max_iter": 20000,
        "dense_max_states": 1024,
        "base_rule": {"family": "unconstrained"},
        "perturbed_rule": {
            "family": "state_independent_rates",
            "incident_node": 0,
            "incident_weight": 5,
            "other_weight": 1,
        },
    }
    result = execute_propagation(spec)
    assert result["status"] == "complete"
    assert result["identity"]["ok"] is True
    for row in result["depths"]:
        assert row["occupation_abs_max"] < 1e-8
    far = result["edge_rate_perturbed"][2]
    assert abs(far - (1 / 11)) < 1e-8
    assert abs(result["edge_rate_base"][2] - (1 / 3)) < 1e-8


def test_laboratory_unconstrained_kernel_matches():
    from rs_constraint_lab.constraints import Choreography
    from rs_constraint_lab.exact import recurrent_components
    from rs_constraint_lab.kernel import build_kernel

    for n in (3, 4):
        kernel = build_kernel(n, Choreography(0, 0, ()), {})
        weights = build_weights(n, {"family": "unconstrained"})
        width = weights.shape[1]
        for state in range(weights.shape[0]):
            for edge in range(width):
                probability = kernel.probability(state, state ^ (1 << edge))
                assert probability.numerator == 1
                assert probability.denominator == width
        assert len(recurrent_components(kernel)) == recurrent_class_count(weights)["recurrent_classes"]


def test_two_subset_partition_rejects_overlap():
    with pytest.raises(ValueError):
        partition_labels(4, {"kind": "hide_two_subsets", "left": [0, 1], "right": [1, 2]}, "interface")


def test_grammar_form_names_a_failed_reduction_as_not_markovian():
    weights = np.zeros((4, 2), dtype=np.int32)
    weights[0, 0] = 1
    weights[2, 1] = 1
    labels = [0, 1, 0, 1]
    form = grammar_form(weights, labels, hidden=[1], visible=[0], exact=False)
    assert form["form"] == "not_markovian_on_interface"
    assert form["interface_markov"] is False


def test_edge_order_matches_laboratory():
    assert edge_list(4) == [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


def test_soft_wedge_balance_gives_orbit_rates():
    """Lemma used to read RRC-001. It does not rerun a lumpability cell.

    If the weight of toggling pair e ignores whether e is present, the
    probability proportional to the total weight is stationary, and the
    stationary toggle rate of e is the average of that weight.
    """
    from fractions import Fraction

    soft = {"family": "soft_wedge", "common_weight": 4, "base_weight": 1}
    boost = {
        "family": "soft_wedge_local_boost",
        "common_weight": 4,
        "base_weight": 1,
        "boost": 5,
        "boost_node": 0,
    }
    for n in (3, 4):
        for rule in (soft, boost):
            weights = build_weights(n, rule)
            size, width = weights.shape
            for edge in range(width):
                flipped = np.arange(size) ^ (1 << edge)
                assert np.array_equal(weights[:, edge], weights[flipped, edge])
            total_weight = weights.sum(axis=1).astype(np.float64)
            pi = total_weight / total_weight.sum()
            image = np.zeros(size)
            for state in range(size):
                row = weights[state].astype(np.float64)
                scale = pi[state] / row.sum()
                for edge in range(width):
                    image[state ^ (1 << edge)] += scale * row[edge]
            assert float(np.max(np.abs(image - pi))) < 1e-9

    for n in (3, 4, 6):
        weights = build_weights(n, boost)
        width = weights.shape[1]
        total = int(weights.sum())
        star = {i for i, (a, b) in enumerate(edge_list(n)) if a == 0 or b == 0}
        denominator = 5 * (n - 1) + (width - (n - 1))
        for edge in range(width):
            numerator = 5 if edge in star else 1
            assert Fraction(int(weights[:, edge].sum()), total) == Fraction(numerator, denominator)

    soft_w = build_weights(4, soft).astype(object)
    boost_w = build_weights(4, boost).astype(object)
    soft_mass = soft_w.sum(axis=1)
    boost_mass = boost_w.sum(axis=1)
    soft_total = int(soft_mass.sum())
    boost_total = int(boost_mass.sum())
    states = np.arange(soft_w.shape[0])
    for edge in range(soft_w.shape[1]):
        present = (states >> edge) & 1 == 1
        soft_occ = Fraction(int(soft_mass[present].sum()), soft_total)
        boost_occ = Fraction(int(boost_mass[present].sum()), boost_total)
        assert soft_occ == Fraction(43, 74)
        assert boost_occ == soft_occ


def test_hard_wedge_empty_graph_is_the_only_deadlock():
    """A present pair has weight 1, so only the empty graph can halt."""
    for n in (3, 4):
        weights = build_weights(n, {"family": "hard_wedge_formation"})
        assert int(weights[0].sum()) == 0
        assert int((weights.sum(axis=1) == 0).sum()) == 1
        present = 1  # the first pair, and nothing else
        assert int(weights[present, 0]) == 1
        classes = recurrent_class_count(weights)
        assert classes["deadlock_states"] == 1
        assert classes["recurrent_classes"] == 1


def test_opening_ledger_matches_laboratory_schema(tmp_path):
    from rs_constraint_lab.coherence import load_ledger, validate_ledger, write_views

    source = REPO / "relational-complexity" / "coherence"
    destination = tmp_path / "coherence"
    destination.mkdir()
    for name in ("findings.jsonl", "relations.jsonl"):
        (destination / name).write_text((source / name).read_text(encoding="utf-8"), encoding="utf-8")
    findings, relations = load_ledger(destination)
    assert validate_ledger(findings, relations) == []
    write_views(destination)
    assert (destination / "current-map.md").exists()
