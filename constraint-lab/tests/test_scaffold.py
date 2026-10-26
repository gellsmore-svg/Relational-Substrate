"""Configurable held scaffold (GT-P007): semantics, covariance, legacy default."""

from __future__ import annotations

import itertools
import math

import numpy as np
import pytest

from rs_constraint_lab import gt0, gte0a, gte0b, gtkernel, gtobs
from rs_constraint_lab.state import edges

FAMILIES = {**gte0a.FAMILIES, **gte0b.FAMILIES}
CASES = [("NULL", "none"), ("PATHF", "weak_suppress"), ("PATHH", "weak_favour"), ("CSPH", "strong_favour+weak_favour"), ("PCOMP", "weak_favour+weak_favour"), ("CLOSEW", "weak_favour")]


def test_default_is_the_legacy_triangle():
    assert gt0.active_scaffold() == gt0.SCAFFOLDS["K3"]
    assert gt0.source() == gt0.SOURCE == (0, 1, 2)
    assert gt0.held_pairs() == ((0, 1), (0, 2), (1, 2))


def test_context_restores_the_default():
    with gt0.use_scaffold("K2"):
        assert gt0.source() == (0, 1)
        with gt0.use_scaffold("P3"):
            assert gt0.held_pairs() == ((0, 1), (1, 2))
        assert gt0.source() == (0, 1)
    assert gt0.active_scaffold().name == "K3"


@pytest.mark.parametrize("scaffold", ["K2", "P3", "K3"])
@pytest.mark.parametrize("n", [4, 5])
@pytest.mark.parametrize("family,grade", CASES)
def test_kernel_matches_rule_strings_exhaustively(scaffold, n, family, grade):
    with gt0.use_scaffold(scaffold):
        cmp = gtkernel.compare_with_build_kernel(family, grade, n, "HELD", FAMILIES)
    assert cmp["same_states"] and cmp["same_targets"] and cmp["weights_identical"], cmp


@pytest.mark.parametrize("scaffold", ["K2", "P3", "K3"])
def test_held_edges_never_dissolve_and_free_slots_toggle(scaffold):
    n = 5
    with gt0.use_scaffold(scaffold):
        chain, _ = gtkernel.reachable_chain(n, "HELD", FAMILIES["NULL"]["none"])
        held = gt0.held_slot_indices(n)
        free = gt0.free_slot_indices(n)
        assert len(chain.states) == 2 ** len(free)
        assert (chain.W[:, held] == 0).all()
        assert (chain.W[:, free] > 0).all()
        for e in held:
            assert (((chain.states >> e) & 1) == 1).all()


def test_p3_chord_is_free_and_classified_c():
    with gt0.use_scaffold("P3"):
        classes = gt0.slot_classes(5)
        chord = edges(5).index((0, 2))
        assert classes[chord] == "C"
        assert classes.count("C") == 1 and classes.count("S") == 2
        assert chord in gt0.free_slot_indices(5)
    assert gt0.slot_classes(5).count("C") == 0


@pytest.mark.parametrize("scaffold,n,group", [("K3", 5, 6 * 2), ("P3", 5, 2 * 2), ("K2", 5, 2 * 6), ("K3", 6, 6 * 6), ("P3", 6, 2 * 6), ("K2", 6, 2 * 24)])
def test_automorphism_group_sizes(scaffold, n, group):
    auts = gt0.SCAFFOLDS[scaffold].automorphisms(n)
    assert len(auts) == group and auts[0] == tuple(range(n))


def _permute_chain_codes(states, n, perm):
    E = edges(n)
    pos = {pair: i for i, pair in enumerate(E)}
    out = np.zeros_like(states)
    slot_map = []
    for e, (a, b) in enumerate(E):
        pa, pb = perm[a], perm[b]
        slot_map.append(pos[(min(pa, pb), max(pa, pb))])
    for e in range(len(E)):
        out |= ((states >> e) & 1) << slot_map[e]
    return out, slot_map


@pytest.mark.parametrize("family,grade", CASES)
def test_relabelling_covariance_of_p3(family, grade):
    """Moving the P3 middle from vertex 1 to vertex 2 permutes the kernel and nothing else."""
    n = 5
    perm = (0, 2, 1, 3, 4)
    other = gt0.Scaffold("P3-middle2", ((0, 2), (1, 2)))
    with gt0.use_scaffold("P3"):
        a, _ = gtkernel.reachable_chain(n, "HELD", FAMILIES[family][grade])
    with gt0.use_scaffold(other):
        b, _ = gtkernel.reachable_chain(n, "HELD", FAMILIES[family][grade])
    mapped, slot_map = _permute_chain_codes(a.states, n, perm)
    order = np.argsort(mapped)
    assert np.array_equal(mapped[order], b.states)
    Wa = a.W[order][:, np.argsort(slot_map)]
    assert np.array_equal(Wa, b.W)


@pytest.mark.parametrize("scaffold", ["K2", "P3", "K3"])
@pytest.mark.parametrize("n", [5, 6])
def test_null_baseline_geometry(scaffold, n):
    with gt0.use_scaffold(scaffold):
        k = len(gt0.source())
        K = len(gt0.held_pairs())
        M = math.comb(n, 2) - K
        assert len(gt0.free_slot_indices(n)) == M
        assert len(gt0.attach_slot_indices(n)) == k * (n - k)
        chain, _ = gtkernel.reachable_chain(n, "HELD", FAMILIES["NULL"]["none"])
        stat = gtobs.stationary(chain, gtobs.start_index(chain, n, "HELD"))
        D = gtobs.source_distances(chain.states, n)
        h = gtobs.held_observables(chain, stat["ct"], n, D, per_unit_time=True)
        assert h["null_attachment_fraction"] == pytest.approx(k * (n - k) / M)
        assert h["attachment_fraction"] == pytest.approx(k * (n - k) / M, abs=1e-12)
        assert np.allclose(stat["ct"], 1.0 / len(chain.states), atol=1e-15)


@pytest.mark.parametrize("scaffold", ["K2", "P3"])
def test_class_table_symmetry_under_new_scaffolds(scaffold):
    n = 5
    with gt0.use_scaffold(scaffold):
        chain, _ = gtkernel.reachable_chain(n, "HELD", FAMILIES["PATHH"]["weak_favour"])
        stat = gtobs.stationary(chain, gtobs.start_index(chain, n, "HELD"))
        arrays = gtobs.structure_arrays(chain, n)
        table, sym = gtobs.class_table(chain, stat["ct"], stat["jump"], n, "HELD", arrays)
        assert sym <= 1e-12
        assert sum(t["orbit_size"] for t in table) == len(chain.states)


def test_reference_held_observables_agree_under_p3():
    """gt0.held_observables (reference, kernel-based) against gtobs (arrays) under P3."""
    n = 5
    with gt0.use_scaffold("P3"):
        kernel = gte0a.build("PATHF", "weak_suppress", n, "HELD", FAMILIES)
        chain = gte0a.chain_from_kernel(kernel, gt0.start_state(n, "HELD"))
        stat = gtobs.stationary(chain, gtobs.start_index(chain, n, "HELD"))
        states = [int(s) for s in chain.states]
        ref = gt0.held_observables(kernel, states, stat["jump"], n)
        D = gtobs.source_distances(chain.states, n)
        new = gtobs.held_observables(chain, stat["jump"], n, D)
        assert ref["attachment_fraction"] == pytest.approx(new["attachment_fraction"], abs=1e-12)
        assert ref["null_attachment_fraction"] == pytest.approx(new["null_attachment_fraction"])
