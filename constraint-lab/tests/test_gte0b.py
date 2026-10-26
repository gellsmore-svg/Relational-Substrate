"""Gravity-time open-thetical Round E0B contracts.

Pre-freeze tests use N=4 fixtures (not an E0B size) of reversible families and
structural checks. They compute no E0B composite, PCOMP or CLOSEW cell at N=5
or N=6.
"""

from __future__ import annotations

import json
import subprocess
import sys

import numpy as np
import pytest

from rs_constraint_lab import gt0, gte0a, gte0b
from rs_constraint_lab.explore08 import plan_hash
from rs_constraint_lab.explore08a import repository_root

REPO = repository_root()


@pytest.mark.parametrize("family,grade,mode", [("NULL", "none", "FREE"), ("CLOSE", "strong_favour", "FREE"), ("CLOSE", "strong_favour", "HELD")])
def test_hub_frame_is_transition_symmetric_and_silent_on_reversible_fixtures(family: str, grade: str, mode: str) -> None:
    kernel = gte0a.build(family, grade, 4, mode)
    chain = gte0a.chain_from_kernel(kernel, gt0.start_state(4, mode))
    classes = gte0b.hub_classes(chain, 4)
    for e in range(chain.n_slots):
        ok = chain.T[:, e] >= 0
        assert np.array_equal(classes[ok, e], classes[chain.T[ok, e], e])
    stat = gte0a.stationary(chain)
    frame = gte0b.event_order_frame(chain, stat["jump"], 4, classes)
    assert frame["pattern_asymmetry"] < 1e-12


def test_e0b_families_and_equal_ratio_pairs() -> None:
    assert gte0a.is_gradient("CLOSEW", gte0b.FAMILIES) and not gte0a.is_gradient("PCOMP", gte0b.FAMILIES)
    for a, b in gte0b.EQUAL_RATIO_PAIRS:
        fa, ga = a.split("-", 1)
        fb, gb = b.split("-", 1)
        def ratio(components):
            out = {}
            for kind, grade in components:
                factor = float(gte0a.FACTORS[grade])
                motif = kind.split("_")[0]
                out[motif] = out.get(motif, 1.0) * (factor if kind.endswith("_form") else 1.0 / factor)
            return out
        assert ratio(gte0b.FAMILIES[fa][ga]) == ratio(gte0b.FAMILIES[fb][gb])


def test_e0b_plan_contract() -> None:
    plan = gte0b.prepare_plan()
    assert plan["plan_hash"] == plan_hash(plan) and len(plan["items"]) == 36
    assert plan["new_primitives"] is False and plan["history"] is False and plan["parameter_fit"] is False
    blob = json.dumps(plan)
    assert "class_table\":" not in blob and "irreversible_flux_fraction\":" not in blob


def test_cli_refuses_without_a_frozen_plan() -> None:
    completed = subprocess.run([sys.executable, "-m", "rs_constraint_lab", "gte0b", "run", "--allow-unpushed"], cwd=REPO, capture_output=True, text=True, check=False)
    assert completed.returncode == 2 and "frozen plan" in completed.stderr.lower()
