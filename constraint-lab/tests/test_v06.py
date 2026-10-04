"""v0.6 matched controls. Generation 5 outputs are not redefined here."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from rs_constraint_lab.cli import main
from rs_constraint_lab.constraints import parse_expression, relabel_constraint
from rs_constraint_lab.grammar import build_grammar, canonical_id_tuple
from rs_constraint_lab.passage import interaction_residual
from rs_constraint_lab.spec import validate_spec
from rs_constraint_lab.state import relation_slots, slot_permutation_maps
from rs_constraint_lab.v06 import (
    ANALYSIS_6,
    ANCHOR_EXPRESSIONS,
    CONTROL_MAPPING_VERSION,
    PUBLISHED_ANCHOR,
    WEIGHT_ORDER,
    _grammar,
    _minimal_spec,
    _record_by_expressions,
    assess_target_row,
    graded_catalogue,
    numerical_preflight,
)
from rs_constraint_lab.weights import ENUMERATED_WEIGHTS

LAB = Path(__file__).resolve().parents[1]
FLOOR = 1e-8


def _rows():
    path = LAB / "provenance" / "ledger.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_review_005_links_v05_and_the_final_head_run():
    review = (LAB / "provenance" / "reviews" / "005-chatgpt-review-v0.5.md").read_text(encoding="utf-8")
    assert "not a line-by-line audit" in review
    assert "003a7c64a35ce8e781e7208117e09702ce63a715" in review
    assert "37151937623" in review
    assert "37151793037" in review
    assert "research/constraint-lab-v0.5" in review
    filed = next(row for row in _rows() if row.get("review_id") == "005")
    assert filed["target_of_review"] == "research/constraint-lab-v0.5"
    assert filed["reviewed_commit"] == "003a7c64a35ce8e781e7208117e09702ce63a715"
    assert filed["ci_run_id"] == "37151937623"
    assert filed["preceding_ci_run_id"] == "37151793037"
    assert filed["ci_conclusion_recorded"] == "success"
    assert filed["execution_path"].endswith("005-targeted-pair-interaction.md")
    assert filed["prompt_ids"] == ["005"]
    assert filed["line_by_line_audit"] is False


def test_prompt_005_authored_metadata_is_not_assigned_to_the_agent_input():
    agent = LAB / "provenance" / "prompts" / "005-v0.5-agent-input.md"
    assert agent.stat().st_size == 39466
    assert _sha(agent) == "e420caddf967d954c0b8b37aaa115b38c09341123a4047835e22e03ba64557c4"
    external = next(
        row
        for row in _rows()
        if row["record_type"] == "prompt_representation"
        and row["prompt_id"] == "005"
        and row["authored_prompt_status"] == "externally_verified_pending_import"
    )
    assert external["authored_prompt_sha256"] == "ec8b7df93edc98525aebddb866a845d8a11a57df497dd941797d5be489066e5d"
    assert external["authored_prompt_bytes"] == 39468
    assert external["authored_prompt_locally_present"] is False
    assert external["authored_prompt_path"] is None
    assert external["relationship"] == "unknown"
    assert external["agent_input_prompt_sha256"] != external["authored_prompt_sha256"]
    text = (LAB / "provenance" / "README.md").read_text(encoding="utf-8")
    assert "not in this working environment" in text
    assert "ec8b7df93edc98525aebddb866a845d8a11a57df497dd941797d5be489066e5d" in text


def test_prompt_006_keeps_authored_and_agent_input_apart():
    path = LAB / "provenance" / "prompts" / "006-v0.6-agent-input.md"
    digest = _sha(path)
    assert path.stat().st_size == 42694
    assert digest == "980d809393477c146fd45b63bf41e7d0af4cb1ef84141d7062d6e82965c487b0"
    assert digest not in path.read_text(encoding="utf-8")
    stored = next(row for row in _rows() if row["record_type"] == "prompt" and row["prompt_id"] == "006")
    assert stored["prompt_sha256"] == digest
    assert stored["prompt_bytes"] == 42694
    assert stored["authored_prompt_sha256"] is None
    assert stored["authored_prompt_bytes"] is None
    assert stored["authored_prompt_path"] is None
    assert stored["relationship"] == "unknown"
    assert stored["authored_prompt_status"] == "pending_verbatim_import"
    assert stored["content_status"] == "agent_input_verbatim"
    assert stored["review_ids"] == []


@pytest.fixture(scope="module")
def catalogue():
    return graded_catalogue(_minimal_spec())


def test_target_family_contains_the_v05_prohibit_anchor_and_the_full_lattice(catalogue):
    coverage = catalogue["coverage"]
    assert coverage["labelled_target_systems"] == 1200
    assert coverage["labelled_targets_accounted"] == 1200
    assert coverage["canonical_target_systems"] == 100
    assert coverage["canonical_structural_targets"] == 4
    assert coverage["orbit_size_distribution"] == {"12": 100}
    assert sum(int(size) * count for size, count in coverage["orbit_size_distribution"].items()) == 1200
    assert coverage["geometry_polarity_weight_cells_not_exactly_one"] == []
    assert coverage["deletion_class_counts"] == {
        "both_prohibit": 4,
        "exactly_one_prohibit": 32,
        "neither_prohibit": 64,
    }
    assert coverage["geometries"] == ["contains_p_companion_edge", "contains_t_action_edge"]
    assert set(coverage["polarities"]) == {"present", "absent"}
    anchor = _record_by_expressions(catalogue, ANCHOR_EXPRESSIONS)
    assert anchor["expressions"] == list(ANCHOR_EXPRESSIONS)
    assert anchor["deletion_class"] == "both_prohibit"
    assert anchor["geometry"] == "contains_p_companion_edge"
    assert anchor["polarity"] == "absent"
    cells = {(row["geometry"], row["polarity"], row["w_P"], row["w_T"]) for row in catalogue["records"]}
    assert len(cells) == 100
    assert {row["w_P"] for row in catalogue["records"]} == set(WEIGHT_ORDER)
    assert {row["w_T"] for row in catalogue["records"]} == set(ENUMERATED_WEIGHTS)


def test_controls_preserve_actions_weights_polarity_and_deduplicate(catalogue):
    assert catalogue["coverage"]["canonical_condition_erased_controls"] == 15
    assert catalogue["coverage"]["distinct_labelled_condition_erased_controls"] == 150
    assert catalogue["coverage"]["collapsed_same_as_action_present"] == 300
    assert catalogue["coverage"]["unsatisfiable_same_as_action_absent"] == 300
    assert catalogue["coverage"]["canonical_face_controls"] == 100
    assert catalogue["coverage"]["live_face_equal_to_erasure"] == 0
    assert catalogue["control_3"]["added"] is False
    assert catalogue["control_3"]["spans_same_adjacent_and_disjoint"] is True
    grammar = _grammar(WEIGHT_ORDER, 4)
    slots = grammar.slot_list()
    for record in catalogue["records"]:
        assert record["control_mapping_version"] == CONTROL_MAPPING_VERSION
        assert record["erased_control_id"]
        assert record["target_id"]
        assert len(record["faces"]) == 3
        weights = set()
        edges = set()
        for text in record["erased_expressions"]:
            parsed = parse_expression(text, 4, order=3)
            assert parsed.conditions == ()
            weights.add(parsed.weight)
            edges.add(slots[parsed.action])
        assert weights == {record["w_P"], record["w_T"]}
        assert edges == {tuple(int(part) for part in record["action_edges"][name].split("-")) for name in ("P", "T")}
        triad = tuple(int(part) for part in record["triad"].split("-"))
        face_names = {tuple(int(part) for part in face["face"].split("-")) for face in record["faces"]}
        assert face_names == {tuple(face) for face in __import__("itertools").combinations(triad, 2)}
        live = []
        for face in record["faces"]:
            assert face["polarity"] == record["polarity"]
            if face["status"] == "unsatisfiable_absent_on_action":
                assert face["relation_to_action"] == "same"
                assert record["polarity"] == "absent"
                assert face["control_id"] is None
            elif face["status"] == "redundant_collapse_to_erasure":
                assert face["relation_to_action"] == "same"
                assert record["polarity"] == "present"
                assert face["control_id"] == record["erased_control_id"]
            else:
                assert face["status"] == "live"
                assert face["relation_to_action"] in {"adjacent", "disjoint"}
                parsed = parse_expression(
                    next(text for text in face["expressions"] if " | " in text),
                    4,
                    order=3,
                )
                assert parsed.weight == record["w_T"]
                assert ("present" if parsed.conditions[0][1] else "absent") == record["polarity"]
                live.append(face["control_id"])
        assert record["matched_control_ids"][0] == record["erased_control_id"]
        assert len(record["matched_control_ids"]) == len(set(record["matched_control_ids"]))
        assert catalogue["control_mapping_version"] == CONTROL_MAPPING_VERSION
    again = graded_catalogue(_minimal_spec())
    assert again["sha256"] == catalogue["sha256"]
    assert [row["target_id"] for row in again["records"]] == [row["target_id"] for row in catalogue["records"]]


def test_complete_set_canonicalisation_is_stable_under_relabelling(catalogue):
    grammar = build_grammar(4, 2, WEIGHT_ORDER, a_max=4, predicates=("pair", "triad"), order=3)
    index = {constraint.key(): position for position, constraint in enumerate(grammar.labelled)}
    anchor = _record_by_expressions(catalogue, ANCHOR_EXPRESSIONS)
    original = tuple(anchor["canonical_ids"])
    slots = relation_slots(4, 3)
    for slot_map in slot_permutation_maps(4, slots):
        imaged = []
        for constraint_id in original:
            image = relabel_constraint(grammar.labelled[constraint_id], slot_map)
            imaged.append(index[image.key()])
        assert canonical_id_tuple(tuple(imaged), grammar.image) == original


def test_interaction_identity_is_unchanged():
    assert interaction_residual(4.0, 3.0, 2.0, 1.0) == pytest.approx(0.0)
    assert interaction_residual(0.25, 0.1, 0.2, 0.05) == pytest.approx(0.0)


def test_anchor_reproduces_v05_and_pairwise_controls_are_triad_flat(catalogue):
    spec = _minimal_spec()
    spec["_spec_hash"] = "test-spec-hash"
    grammar = _grammar(WEIGHT_ORDER, 4)
    anchor = _record_by_expressions(catalogue, ANCHOR_EXPRESSIONS)
    row = assess_target_row(anchor, spec, grammar, {})
    assert row["support_violations"] == 0
    assert row["support_removed"] == 768
    assert row["work_item_key"] != row["item_key"]
    q0 = {}
    for direction, published in PUBLISHED_ANCHOR.items():
        got = row["directions"][direction]["target"]
        for field, expected in (
            ("Q0", published["Q0"]),
            ("QT", published["QT"]),
            ("QP", published["QP"]),
            ("QTP", published["QTP"]),
            ("I", published["I"]),
            ("G", published["G"]),
            ("delta_S", published["delta_S"]),
        ):
            assert got[field] == pytest.approx(expected, abs=1e-12)
        q0[direction] = got["Q0"]
        for control in row["directions"][direction]["controls"]:
            assert control["S_T"] == pytest.approx(0.0, abs=FLOOR)
            assert control["S_TP"] == pytest.approx(0.0, abs=FLOOR)
            assert control["delta_S"] == pytest.approx(0.0, abs=FLOOR)
            assert row["directions"][direction]["controls"]
        assert row["directions"][direction]["target"]["Q0"] == q0[direction]
    assert row["directions"]["path_to_matching"]["target"]["state_sign"]["coherence"] == "positive"
    assert row["directions"]["matching_to_path"]["target"]["state_sign"]["coherence"] == "negative"


def test_reference_kernels_agree_across_solvers():
    report = numerical_preflight(_minimal_spec())
    assert report["floor_decision"] == "keep_1e-8"
    assert report["worst_numerical_gap"] < 1e-10
    for name, gap in report["landing_block_vs_dense"].items():
        assert gap < 1e-10, name
    for name, gap in report["committor_direct_vs_iterative"].items():
        assert gap < 1e-10, name
    assert report["anchor_versus_published_I_gap"] < 1e-12


def test_generation6_resume_keeps_the_completed_receipt(tmp_path):
    spec = _minimal_spec(experiment_id="miniature-graded-resume")
    path = tmp_path / "spec.json"
    path.write_text(json.dumps(spec), encoding="utf-8")
    out = tmp_path / "out"
    assert main(["run", str(path), "--out", str(out), "--workers", "1", "--shard-items", "1", "--max-shards", "1"]) == 0
    progress = json.loads((out / "progress.json").read_text(encoding="utf-8"))
    assert progress["status"] == "IN_PROGRESS"
    assert progress["completed"] == 1
    plan = json.loads((out / "plan.json").read_text(encoding="utf-8"))
    assert plan["estimates"]["cells"][0]["graded_coverage"]["canonical_target_systems"] == 100
    assert plan["header"]["control_mapping_version"] == CONTROL_MAPPING_VERSION
    done = next(
        shard["shard_id"]
        for shard in plan["shards"]
        if progress["shards"][shard["shard_id"]]["status"] == "completed"
    )
    receipt = (out / "shards" / done / "receipt.json").read_bytes()
    result = json.loads((out / "shards" / done / "result.json").read_text(encoding="utf-8"))
    assert result["graded_rows"][0]["control_mapping_version"] == CONTROL_MAPPING_VERSION
    assert main(["run", str(path), "--out", str(out), "--workers", "1", "--shard-items", "1", "--max-shards", "1"]) == 0
    assert (out / "shards" / done / "receipt.json").read_bytes() == receipt
    again = json.loads((out / "progress.json").read_text(encoding="utf-8"))
    assert again["completed"] == 2


def test_simplicial_semantics_and_nonzero_axes_stay_refused():
    spec = _minimal_spec()
    validate_spec(spec)
    refused = dict(spec)
    refused["semantics"] = "simplicial"
    with pytest.raises(ValueError, match="simplicial"):
        validate_spec(refused)
    for axis in ("H", "S", "G", "L"):
        moved = dict(spec)
        moved[axis] = 1
        with pytest.raises(ValueError, match=axis):
            validate_spec(moved)
    assert spec["analysis"] == ANALYSIS_6
