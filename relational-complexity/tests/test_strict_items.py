"""Item types for a strict event law. They do not run an atlas round."""

from __future__ import annotations

from fractions import Fraction

import pytest

from rrc.items import execute_event_horizon, execute_strict_event_comparison


IDENTIFIED = {
    "n_states": 2,
    "bit_width": 1,
    "events": [
        {"name": "up", "kind": "toggle", "source": 0, "target": 1, "weight": 1},
        {"name": "down", "kind": "toggle", "source": 1, "target": 0, "weight": 1},
    ],
}


def _fraction(cell) -> Fraction:
    return Fraction(int(cell["num"]), int(cell["den"]))


def test_strict_comparison_keeps_a_conjugacy_and_drops_a_leaking_image():
    coupled = execute_strict_event_comparison(
        {
            "id": "coupled",
            "round_id": "fixture",
            "type": "strict_event_comparison",
            "role": "comparison",
            "family": "coupled_copies",
            "n_states": 4,
            "bit_width": 2,
            "events": [
                {"name": "together-up", "kind": "joint", "source": 0, "target": 3, "weight": 1},
                {"name": "together-down", "kind": "joint", "source": 3, "target": 0, "weight": 1},
            ],
            "reference": IDENTIFIED,
            "image_map": [0, 3],
        }
    )
    assert coupled["method"] == "event-kernel-0.2.0"
    assert coupled["new_primitive"] is False
    assert coupled["correspondence"]["image_invariant"] is True
    assert coupled["correspondence"]["conjugate"] is True
    assert [_fraction(cell) for cell in coupled["correspondence"]["restricted_rows"][0]] == [
        Fraction(0),
        Fraction(1),
    ]
    leaked = execute_strict_event_comparison(
        {
            "id": "leaked",
            "round_id": "fixture",
            "type": "strict_event_comparison",
            "family": "leaked_image",
            "n_states": 4,
            "bit_width": 2,
            "catalogue": "single_toggle",
            "rows": [[1, 1], [1, 1], [1, 1], [1, 1]],
            "reference": IDENTIFIED,
            "image_map": [0, 3],
        }
    )
    assert leaked["correspondence"]["image_invariant"] is False
    assert leaked["correspondence"]["conjugate"] is False
    assert leaked["correspondence"]["restricted_rows"] is None
    plain = execute_strict_event_comparison(
        {
            "id": "plain",
            "round_id": "fixture",
            "type": "strict_event_comparison",
            "family": "identified_interface",
            "n_states": 2,
            "bit_width": 1,
            "events": IDENTIFIED["events"],
        }
    )
    assert plain["correspondence"] is None
    assert "occupation" not in plain
    assert "stationary" not in plain


def test_event_horizon_powers_the_kernel_and_stores_no_intervention():
    report = execute_event_horizon(
        {
            "id": "back",
            "round_id": "fixture",
            "type": "event_horizon",
            "family": "identified_interface",
            "n_states": 2,
            "bit_width": 1,
            "events": IDENTIFIED["events"],
            "horizon": 2,
            "initial_state": 0,
            "labels": [0, 1],
            "subset": [0],
        }
    )
    assert report["method"] == "event-kernel-0.2.0"
    assert report["intervention"] is None
    assert report["new_primitive"] is False
    assert [_fraction(cell) for cell in report["horizon_distribution"]] == [Fraction(1), Fraction(0)]
    assert _fraction(report["subset_probability"]) == 1
    assert report["lumpability"]["exact"] is True
    assert report["lumpability"]["rows"] is not None
    assert "occupation" not in report
    assert "stationary" not in report
    with pytest.raises(ValueError, match="horizon"):
        execute_event_horizon(
            {
                "id": "far",
                "type": "event_horizon",
                "family": "identified_interface",
                "n_states": 2,
                "bit_width": 1,
                "events": IDENTIFIED["events"],
                "horizon": 5,
                "initial_state": 0,
                "labels": [0, 1],
                "subset": [0],
            }
        )
