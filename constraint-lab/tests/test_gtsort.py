"""GT-P008 proof-verification fixtures for the sorting-mechanism derivation.

Synthetic factors on N=4 kernels only (N=4 is not an E4 round size); no E4
scientific observable is computed here. Published tables are read only in the
extraction test at the end.
"""

from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from rs_constraint_lab import gt0, gte0a, gte0b, gtsort
from rs_constraint_lab.constraints import Choreography
from rs_constraint_lab.kernel import build_kernel
from rs_constraint_lab.state import edges

REPO = Path(__file__).resolve().parents[2]
FAMILIES = {**gte0a.FAMILIES, **gte0b.FAMILIES}
GRADE_OF = {"NULL": "none", "PATHF": "weak_suppress", "PATHH": "weak_favour", "CSPH": "strong_favour+weak_favour", "PCOMP": "weak_favour+weak_favour", "CLOSEW": "weak_favour"}


def synthetic_factors(eps: float) -> dict:
    return {"prohibit": Fraction(0), "neutral": Fraction(1), "weak_favour": Fraction(math.exp(eps)), "weak_suppress": Fraction(math.exp(-eps)),
            "strong_favour": Fraction(math.exp(2 * eps)), "strong_suppress": Fraction(math.exp(-2 * eps))}


def laws(scaffold: gt0.Scaffold, family: str, n: int, eps: float):
    with gt0.use_scaffold(scaffold):
        rules = gte0a.rules_for(family, GRADE_OF[family], n, "HELD", FAMILIES)
        kernel = build_kernel(n, Choreography(0, 0, rules), synthetic_factors(eps))
        chain = gte0a.chain_from_kernel(kernel, gt0.start_state(n, "HELD"))
        stat = gte0a.stationary(chain)
    assert stat["resolved"]
    return chain, stat


def occupancy(chain, law, n, e) -> float:
    i = edges(n).index(e)
    return float(law @ ((chain.states >> i) & 1))


def logit(p):
    return math.log(p / (1 - p))


# --- template algebra -----------------------------------------------------------------------------


@pytest.mark.parametrize("n", [4, 5, 6, 7])
def test_template_count_and_ordered_multiplicity(n):
    for e in itertools.combinations(range(n), 2):
        t = gtsort.path_templates(n, e)
        assert len(t) == 2 * (n - 2) * (n - 3)
        assert len(gtsort.closure_templates(n, e)) == n - 2


def test_held_graphs_match_gt0_presets():
    for name, held in gtsort.HELD.items():
        assert tuple(sorted(held)) == gt0.SCAFFOLDS[name].held


def _connected_graphs(k):
    allp = list(itertools.combinations(range(k), 2))
    for r in range(k - 1, len(allp) + 1):
        for held in itertools.combinations(allp, r):
            if gtsort.source(held) == list(range(k)) and gtsort._connected(held, k):
                yield held


@pytest.mark.parametrize("k", [2, 3, 4, 5])
def test_floor_formula_equals_enumeration_on_every_connected_held_graph(k):
    for held in _connected_graphs(k):
        for n in (k + 1, k + 2):
            for s in range(k):
                assert gtsort.floor_enumerated(n, held, s) == gtsort.floor_formula(held, s)


def test_only_k2_is_floor_free_among_connected_graphs():
    for k in (2, 3, 4, 5):
        for held in _connected_graphs(k):
            zero = all(gtsort.floor_formula(held, s) == 0 for s in range(k))
            assert zero == (k == 2)


@pytest.mark.parametrize("k", [2, 3, 4, 5])
def test_attachment_closed_form_equals_enumeration(k):
    for held in _connected_graphs(k):
        for n in (k + 1, k + 2, k + 3):
            p = k
            for s in range(k):
                assert gtsort.e0_path(n, held, (s, p)) == gtsort.e0_path_attachment_formula(n, held, s)


def test_probe_probe_and_closure_expectations():
    for name, held in gtsort.HELD.items():
        k = len(gtsort.source(held))
        for n in (k + 2, k + 3):
            T, D = 2 * (n - 2) * (n - 3), 2 * len(held)
            assert gtsort.e0_path(n, held, (k, k + 1)) == Fraction(T, 4) + Fraction(D, 2)
            for s in range(k):
                d = gtsort.held_degree(held, s)
                assert gtsort.e0_close(n, held, (s, k)) == Fraction(n - 2, 4) + Fraction(d, 4)


# --- S1: stationary balance identity on arbitrary positive rates ---------------------------------


def test_balance_identity_on_random_state_dependent_rates():
    rng = np.random.default_rng(20261015)
    m = 6
    size = 1 << m
    for _ in range(5):
        Fr = rng.uniform(0.1, 3.0, size=(size, m))
        Dr = rng.uniform(0.1, 3.0, size=(size, m))
        Q = np.zeros((size, size))
        for x in range(size):
            for e in range(m):
                y = x ^ (1 << e)
                Q[x, y] = Dr[x, e] if (x >> e) & 1 else Fr[x, e]
            Q[x, x] = -Q[x].sum()
        A = Q.T.copy()
        A[-1, :] = 1.0
        b = np.zeros(size)
        b[-1] = 1.0
        pi = np.linalg.solve(A, b)
        for e in range(m):
            x = (np.arange(size) >> e) & 1
            lhs = float(pi @ ((1 - x) * Fr[:, e]))
            rhs = float(pi @ (x * Dr[:, e]))
            assert abs(lhs - rhs) < 1e-12
            occ = float(pi @ x)
            fbar = lhs / (1 - occ)
            dbar = rhs / occ
            assert abs(occ / (1 - occ) - fbar / dbar) < 1e-10


# --- S4/S6: first-order theorems on synthetic-epsilon N=4 kernels ---------------------------------

N4_SCAFFOLDS = [gt0.SCAFFOLDS["K2"], gt0.SCAFFOLDS["P3"], gt0.SCAFFOLDS["K3"], gt0.Scaffold("N4S", ((0, 1), (0, 2)))]
EPS = 1e-4


@pytest.mark.parametrize("family", ["PATHF", "PATHH", "CSPH", "PCOMP", "CLOSEW"])
@pytest.mark.parametrize("sc", N4_SCAFFOLDS, ids=lambda s: s.name)
def test_first_order_continuous_and_jump_coefficients(sc, family):
    n = 4
    held = sc.held
    plus = laws(sc, family, n, EPS)
    minus = laws(sc, family, n, -EPS)
    jd = gtsort.jump_first_order(family, n, held)
    for e in gtsort.free_slots(n, held):
        d_ct = (logit(occupancy(plus[0], plus[1]["ct"], n, e)) - logit(occupancy(minus[0], minus[1]["ct"], n, e))) / (2 * EPS)
        assert abs(d_ct - float(gtsort.kappa(family, n, held, e))) < 1e-6
        d_jump = (occupancy(plus[0], plus[1]["jump"], n, e) - occupancy(minus[0], minus[1]["jump"], n, e)) / (2 * EPS)
        assert abs(d_jump - jd[e]) < 1e-6


@pytest.mark.parametrize("sc", N4_SCAFFOLDS, ids=lambda s: s.name)
def test_equal_ratio_pair_has_equal_first_order_continuous_law(sc):
    n = 4
    f = [laws(sc, "PATHF", n, s * EPS)[1]["ct"] for s in (1, -1)]
    h = [laws(sc, "PATHH", n, s * EPS)[1]["ct"] for s in (1, -1)]
    df = (f[0] - f[1]) / (2 * EPS)
    dh = (h[0] - h[1]) / (2 * EPS)
    assert np.abs(df - dh).max() < 1e-6
    assert np.abs(df).max() > 1e-3


@pytest.mark.parametrize("sc", N4_SCAFFOLDS, ids=lambda s: s.name)
def test_pcomp_continuous_law_is_uniform_at_any_strength(sc):
    chain, stat = laws(sc, "PCOMP", 4, math.log(2.0))
    assert np.abs(stat["ct"] - 1.0 / len(stat["ct"])).max() < 1e-12


def test_margin_slope_matches_finite_difference_k2_n4():
    sc, n = gt0.SCAFFOLDS["K2"], 4
    held = sc.held
    A = [e for e in gtsort.free_slots(n, held) if gtsort.slot_class(held, e) == "A"]
    F = gtsort.free_slots(n, held)

    def margin(eps):
        chain, stat = laws(sc, "PATHF", n, eps)
        ea = sum(occupancy(chain, stat["ct"], n, e) for e in A)
        ef = sum(occupancy(chain, stat["ct"], n, e) for e in F)
        return ea / ef - len(A) / len(F)

    fd = (margin(EPS) - margin(-EPS)) / (2 * EPS)
    assert abs(fd - gtsort.margin_slope("PATHF", n, held)) < 1e-6


def test_closew_gibbs_matches_kernel_law_n4():
    sc = gt0.SCAFFOLDS["P3"]
    chain, stat = laws(sc, "CLOSEW", 4, math.log(2.0))
    g = gtsort.closew_gibbs_orbits(4, sc.held)
    for orbit, verts in (("1", [1]), ("0+2", [0, 2])):
        for clock in ("continuous", "jump"):
            law = stat["ct"] if clock == "continuous" else stat["jump"]
            occ = np.mean([occupancy(chain, law, 4, (v, 3)) for v in verts])
            assert abs(occ - g[clock][orbit]) < 1e-12


# --- published tables (read only) ----------------------------------------------------------------


def test_extraction_checks_on_published_tables():
    out = gtsort.build(REPO)
    worst = out["extraction_checks"]["max_abs_deviation"]
    assert worst["floor_vs_published_analytic"] == 0
    for key in ("null_orbits", "pcomp_ct_orbits", "closew_ct", "closew_jump", "balance_pathf", "balance_pathh", "jump_activity", "floor_vs_census", "null_witness_total_vs_e0"):
        assert worst[key] < 1e-9, key
    sel = out["extraction_checks"]["selected_published_values"]
    assert [round(v, 3) for v in sel["P3-N5-PATHF middle/ends ct"]] == [0.332, 0.177]
    assert [round(v, 3) for v in sel["S4-N6-PATHF centre/leaves ct"]] == [0.363, 0.093]


def _same(a, b) -> bool:
    """Structural equality; floats within 1e-12 absolute or 1e-9 relative (summation order differs across machines)."""
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_same(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b))
    if isinstance(a, float) or isinstance(b, float):
        return isinstance(a, (int, float)) and isinstance(b, (int, float)) and math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)
    return a == b


def test_committed_secondary_json_is_reproducible():
    path = REPO / gtsort.OUT_RELPATH
    if not path.is_file():
        pytest.skip("secondary analysis not yet written")
    assert _same(json.loads(path.read_text(encoding="utf-8")), json.loads(json.dumps(gtsort.build(REPO), sort_keys=True)))
