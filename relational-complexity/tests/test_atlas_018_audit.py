"""Adversarial software fixtures for the independent saved-record checker."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "provenance/atlas-018-independent-check.py"
MODULE_SPEC = importlib.util.spec_from_file_location("atlas_018_audit", SCRIPT)
AUDIT = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(AUDIT)


def fixture():
    spec = {"id": "fixture", "round_id": "software-fixture", "family": "two_bits",
            "n_states": 4, "bit_width": 2, "catalogue": "single_toggle",
            "rows": [[1, 1] for _ in range(4)]}
    expected = AUDIT.oracle(spec)
    result = {"item_id": spec["id"], "round_id": spec["round_id"], "family": spec["family"],
              "plan_hash": "fixture-plan", "spec_hash": AUDIT.canonical_hash(spec),
              "status": "complete", "engine_version": "fixture-engine",
              "type": "strict_event_comparison", "method": "event-kernel-0.2.0",
              "clock": "one_declared_event", "semantics": "bitmask", "bit_width": 2,
              "n_states": 4, "new_primitive": False, "halt_self_loop_is_event": False,
              "event_count": 8, "correspondence": None, **expected}
    result["probabilities"] = [[{"num": str(cell.numerator), "den": str(cell.denominator)}
                                for cell in row] for row in expected["probabilities"]]
    return spec, result


def check(spec, result):
    raw = json.dumps(result).encode()
    receipt = {"item_id": result["item_id"], "plan_hash": result["plan_hash"],
               "spec_hash": result["spec_hash"], "status": "complete",
               "result_sha256": hashlib.sha256(raw).hexdigest()}
    return AUDIT.check_record(spec, result, receipt, raw, "fixture-plan", "fixture-engine")


def test_checker_accepts_the_hand_enumerated_square():
    spec, result = fixture()
    assert AUDIT.oracle(spec)["probabilities"] == [
        [0, Fraction(1, 2), Fraction(1, 2), 0],
        [Fraction(1, 2), 0, 0, Fraction(1, 2)],
        [Fraction(1, 2), 0, 0, Fraction(1, 2)],
        [0, Fraction(1, 2), Fraction(1, 2), 0],
    ]
    assert check(spec, result)["probability_cells_checked"] == 16


def test_checker_rejects_semantic_drift_even_with_a_fresh_valid_receipt():
    spec, original = fixture()
    for field in ("probability", "kind", "input", "correspondence"):
        result = deepcopy(original)
        if field == "probability":
            result["probabilities"][0][1] = {"num": "1", "den": "3"}
            result["probabilities"][0][2] = {"num": "2", "den": "3"}
        elif field == "kind":
            result["events"][0]["kind"] = "joint"
        elif field == "input":
            result["spec_hash"] = "wrong-input"
        else:
            result["correspondence"] = {"conjugate": True}
        with pytest.raises(ValueError):
            check(spec, result)


def test_oracle_checks_zero_weight_semantics_and_duplicate_names():
    spec, _result = fixture()
    spec.pop("catalogue")
    spec["events"] = [{"name": "bad", "kind": "toggle", "source": 0, "target": 3, "weight": 0}]
    with pytest.raises(ValueError, match="kind"):
        AUDIT.oracle(spec)
    event = {"name": "duplicate", "kind": "toggle", "source": 0, "target": 1, "weight": 1}
    spec["events"] = [event, event.copy()]
    with pytest.raises(ValueError, match="name"):
        AUDIT.oracle(spec)


def test_image_bijection_does_not_imply_invariance():
    spec, _result = fixture()
    spec["image_map"] = [0, 3]
    spec["reference"] = {"n_states": 2, "bit_width": 1,
                         "catalogue": "single_toggle", "rows": [[1], [1]]}
    compared = AUDIT.expected_correspondence(spec, AUDIT.oracle(spec)["probabilities"])
    assert compared["image_invariant"] is False
    assert compared["conjugate"] is False
    assert compared["restricted_rows"] is None


def test_invariant_image_with_wrong_law_is_not_conjugate():
    spec, _result = fixture()
    spec["image_map"] = [0, 3]
    spec["reference"] = {"n_states": 2, "bit_width": 1,
                         "catalogue": "single_toggle", "rows": [[1], [1]]}
    identity = [[Fraction(source == target) for target in range(4)] for source in range(4)]
    compared = AUDIT.expected_correspondence(spec, identity)
    assert compared["image_invariant"] is True
    assert compared["conjugate"] is False
    assert compared["restricted_rows"] == [[1, 0], [0, 1]]


def test_checker_rejects_an_unrelated_four_bit_kernel_under_the_recoding():
    spec = {"n_states": 16, "bit_width": 4, "catalogue": "single_toggle",
            "rows": [[1, 1, 1, 1] for _ in range(16)]}
    with pytest.raises(ValueError, match="recoded kernel"):
        AUDIT.coupled_encoding(AUDIT.oracle(spec)["probabilities"])
