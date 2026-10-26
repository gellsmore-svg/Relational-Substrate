"""The frozen vocabulary in docs/definitions.md matches the engine's words."""

from pathlib import Path

from rrc import SIX_CLAIMS

ROOT = Path(__file__).resolve().parents[1]
DEFINITIONS = (ROOT / "docs" / "definitions.md").read_text(encoding="utf-8")

GRAMMAR_FORMS = (
    "unconstrained_lazy",
    "reweighted_single_toggle",
    "not_markovian_on_interface",
    "outside_grammar",
)
AUGMENTATIONS = (
    "interface",
    "edge_count",
    "parity",
    "interface_wedge_counts",
)


def test_definitions_name_every_grammar_form_and_augmentation():
    for word in GRAMMAR_FORMS + AUGMENTATIONS:
        assert f"`{word}`" in DEFINITIONS


def test_definitions_keep_the_four_sixes_apart():
    for claim in SIX_CLAIMS:
        assert claim.replace("_", " ") in DEFINITIONS or claim in DEFINITIONS
    assert "six levels of composition" in DEFINITIONS
    assert "six edges along a path" in DEFINITIONS
    assert "six units of context" in DEFINITIONS
    assert "six constituent nodes" in DEFINITIONS


def test_exactness_is_strong_lumpability_and_not_a_stationary_distance():
    assert "Strong lumpability" in DEFINITIONS
    assert "not total variation of a stationary marginal" in DEFINITIONS
    assert "Weak lumpability" in DEFINITIONS
