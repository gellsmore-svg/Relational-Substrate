"""Finite contextual separators, observer boundaries and sparse compatibility."""

from fractions import Fraction
import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_checker(filename, module_name):
    spec = importlib.util.spec_from_file_location(module_name, ROOT / "provenance" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


A = load_checker("context-probe-analysis-check.py", "context_probes")
OLD = load_checker("label-sync-analysis-check.py", "existing_sparse_sync")


def scaled_component():
    return A.component(4, [A.event("a", 2 * z + d, 2 * (1 - z) + d, d + 1)
                           for z in range(2) for d in range(2)])


def test_calibration_recovers_raw_shared_and_private_weights_from_hand_fractions():
    system = A.component(2, [A.event("a", 0, 1, 3), A.event("p", 0, 0, 2), A.event("q", 0, 1, 4)])
    probe = A.probe_family(system["handshake"])[1]["component"]
    row = A.composed_kernel(system, probe)[0]
    assert row == [Fraction(1, 5), 0, Fraction(1, 10), Fraction(2, 5), Fraction(3, 10), 0]
    result = A.assess(system, [0, 1])
    assert result["reconstructed"][0] == {"shared": {"a": [0, 3], "b": [0, 0]}, "private": [2, 4]}


def test_private_label_redistribution_is_safe_for_the_declared_observer():
    system = A.private_redistribution()
    observation = [0, 0, 1, 1]
    result = A.assess(system, observation)
    assert result["signature"]["exact"]
    assert all(report["exact"] for report in result["probes"])
    assert not A.full_label_stable(system, observation)
    assert result["reconstructed"][0]["private"] == [0, 1]


def test_making_the_private_labels_shared_changes_the_allowed_contexts():
    system = A.private_redistribution(("p", "q"))
    result = A.assess(system, [0, 0, 1, 1])
    assert not result["signature"]["exact"]
    assert not next(report for report in result["probes"] if report["label"] == "p")["exact"]


def test_private_relabelling_commutes_at_weighted_matrix_level_with_the_sparse_product():
    system = A.private_redistribution()
    partner = A.component(2, [A.event("a", 0, 1, 3), A.event("r", 0, 0, 2), A.event("q", 1, 0)])
    combined = OLD.compose(system, partner)
    left = A.collapse_private(combined)
    right = OLD.compose(A.collapse_private(system), A.collapse_private(partner))
    assert OLD.labelled_weights(left) == OLD.labelled_weights(right)
    assert OLD.kernel(combined) == OLD.kernel(right)
    with pytest.raises(ValueError, match="outside handshake"):
        A.collapse_private(system, "a")


def test_a_label_observing_recipient_can_already_see_the_private_difference():
    matrices = A.label_matrices(A.private_redistribution())
    assert sum(matrices["p"][0]) == 1 and sum(matrices["q"][0]) == 0
    assert sum(matrices["p"][1]) == 0 and sum(matrices["q"][1]) == 1
    # Every row has total one; these are also the normalised label probabilities.
    assert A.assess(A.private_redistribution(), [0, 0, 1, 1])["signature"]["exact"]


def test_internal_private_loop_and_halt_are_separated_even_by_a_constant_component_observation():
    system = A.component(2, [A.event("p", 0, 0)])
    report = A.assess(system, [0, 0])["probes"][0]
    assert not report["exact"] and report["rows"] is None
    assert report["witness"]["states"] == [0, 2]
    assert report["witness"]["first_row"] == [Fraction(1, 2), Fraction(1, 2)]
    assert report["witness"]["second_row"] == [0, 1]


def test_removing_calibration_can_hide_raw_scale():
    system = scaled_component()
    partner = A.component(2, [A.event("a", 0, 1), A.event("a", 1, 0)])
    _, report = A.inspect_context(system, [0, 0, 1, 1], partner)
    assert report["exact"]
    calibrated = A.assess(system, [0, 0, 1, 1])
    assert not calibrated["signature"]["exact"]
    assert not next(report for report in calibrated["probes"] if report["label"] == "a")["exact"]


@pytest.mark.parametrize("mode", ["hold", "flip", "reset"])
def test_uniform_context_signature_allows_evolving_hidden_state(mode):
    system = A.template_system((0, 3), (0, 3), mode)
    assert A.assess(system, [0, 0, 1, 1])["signature"]["exact"]


def test_empty_handshake_reduces_to_aggregate_private_weight_condition():
    system = A.component(2, [A.event("p", 0, 1, 2), A.event("q", 1, 0, 2)], ())
    result = A.assess(system, [0, 0])
    assert len(result["probes"]) == 1 and result["signature"]["exact"]
    assert result["reconstructed"] == [{"shared": {}, "private": [2]}] * 2


def test_identity_observation_and_all_halt_are_valid_boundaries():
    system = A.component(2, [])
    assert A.assess(system, [0, 0])["signature"]["exact"]
    assert A.assess(scaled_component(), [0, 1, 2, 3])["signature"]["exact"]


def test_duplicate_zero_and_nonunit_events_preserve_raw_aggregation():
    first = A.component(2, [A.event("a", 0, 1), A.event("a", 0, 1, 2), A.event("p", 0, 0, 0)])
    second = A.component(2, [A.event("a", 0, 1, 3)])
    assert A.signatures(first, [0, 1]) == A.signatures(second, [0, 1])
    assert A.assess(first, [0, 1])["reconstructed"] == A.assess(second, [0, 1])["reconstructed"]


@pytest.mark.parametrize("case", ["private", "scale", "halt"])
def test_dense_context_laws_match_the_existing_sparse_event_policy(case):
    system = {"private": A.private_redistribution(), "scale": scaled_component(),
              "halt": A.component(2, [A.event("p", 0, 0)])}[case]
    for probe in A.probe_family(system["handshake"]):
        partner = probe["component"]
        assert A.composed_kernel(system, partner) == OLD.kernel(OLD.compose(system, partner))


def test_probe_alphabet_and_signature_namespaces_do_not_collide():
    system = A.component(2, [A.event("private", 0, 1), A.event("p", 0, 0)], ("private", "_probe"))
    result = A.assess(system, [0, 1])
    assert result["reconstructed"][0]["shared"]["private"] == [0, 1]
    assert result["reconstructed"][0]["private"] == [1, 0]
    assert A.probe_family(system["handshake"])[0]["component"]["events"][0]["label"] == "_probe_"


def test_invalid_weights_observations_and_handshakes_are_rejected():
    for invalid in (-1, True, Fraction(1, 2)):
        with pytest.raises(ValueError, match="weight"):
            A.component(2, [A.event("a", 0, 1, invalid)])
    for observation in ([0], [0, 2], [False, True]):
        with pytest.raises(ValueError, match="observation"):
            A.assess(A.component(2, []), observation)
    with pytest.raises(ValueError, match="handshake"):
        A.composed_kernel(A.component(2, []), A.component(2, [], ()))


def test_predeclared_signature_probe_and_reconstruction_domains_agree():
    result = A.run_checks()
    assert result["template_count"] == 22
    assert result["validation"] == {"systems": 1452, "stable": 66, "unstable": 1386,
                                    "probe_laws": 4356, "reconstructed_signatures": 5808}
    assert result["scientific_worker_invocations"] == result["new_atlas_cells"] == 0
    assert result["status"] == "verified"
