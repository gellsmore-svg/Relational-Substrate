"""v0.5 provenance, the block epoch solver, and the targeted pair grammar.

Generation 4 numeric outputs are not redefined here. The one-step
same-edge-count flux stays a structural invariant of the event model.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from rs_constraint_lab.census import build_slotted
from rs_constraint_lab.cli import main
from rs_constraint_lab.constraints import cross_order_class, parse_expression, relabel_constraint
from rs_constraint_lab.execution import build_plan
from rs_constraint_lab.grammar import build_grammar, canonical_id_tuple
from rs_constraint_lab.graphs import pair_classes
from rs_constraint_lab.memory_clocks import (
    epoch_kernel_block,
    epoch_kernel_float,
    float_stationary,
    layout,
    pair_event_epoch_memory_tv_float,
)
from rs_constraint_lab.passage import (
    PATH_CLASS,
    MATCHING_CLASS,
    eventual_committor,
    hit_passage,
    interaction_residual,
    prepare_direction,
    reference_source,
    state_interaction,
    super_singleton_gap,
)
from rs_constraint_lab.reconfiguration import (
    RECONFIGURATION_MEASURE,
    class_flux,
    focused_transition,
)
from rs_constraint_lab.spec import validate_spec
from rs_constraint_lab.state import relation_slots, slot_permutation_maps
from rs_constraint_lab.v05 import (
    ANALYSIS_VERSION,
    assess_pair_row,
    assess_singleton_row,
    require_effect_floor,
    targeted_catalogue,
)
from rs_constraint_lab.weights import alphabet_factors

LAB = Path(__file__).resolve().parents[1]
WEIGHTS = ("prohibit", "strong_favour")
FLOOR = 1e-6


def _sha(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rows():
    return [
        json.loads(line)
        for line in (LAB / "provenance" / "ledger.jsonl").read_text(encoding="utf-8").splitlines()
    ]


def _pair_spec() -> dict:
    return {
        "schema": "rs-constraint-lab.experiment/v1",
        "experiment_id": "generation-005-targeted-tp-pp-pairs",
        "generation": 5,
        "semantics": "hypergraph",
        "G": 0,
        "S": 0,
        "H": 0,
        "L": 0,
        "O": 3,
        "alphabet": "W4",
        "composition": "structural-simple",
        "analysis": "n4-targeted-pairs",
        "analysis_version": ANALYSIS_VERSION,
        "predicates": ["pair", "triad"],
        "weights": list(WEIGHTS),
        "cells": [{"N": 4, "K_max": 2, "A_max": 4, "cardinalities": [2]}],
        "reconfiguration_horizon": 16,
        "effect_floor": FLOOR,
        "effect_floor_reason": "unit-test floor; the census floor is chosen from solver residuals",
    }


def _kernel(n: int, text: str | None, rho: Fraction = Fraction(1)):
    slots = tuple(relation_slots(n, 3))
    constraints = () if text is None else (parse_expression(text, n, order=3),)
    return build_slotted(n, constraints, alphabet_factors("W4"), slots, rho), slots


def _one_bit_pair_landings(landing: np.ndarray, n_pairs: int) -> None:
    mask = (1 << n_pairs) - 1
    sources, targets = np.nonzero(landing > 1e-12)
    assert sources.size > 0
    for source, target in zip(sources.tolist(), targets.tolist()):
        flipped = (source ^ target) & mask
        assert flipped != 0 and flipped & (flipped - 1) == 0
        assert abs(int(source & mask).bit_count() - int(target & mask).bit_count()) == 1


@pytest.fixture(scope="module")
def targeted():
    return targeted_catalogue(_pair_spec())


def test_review_004_links_prompt_and_execution_and_the_final_v04_run():
    review = (LAB / "provenance" / "reviews" / "004-chatgpt-review-v0.4.md").read_text(encoding="utf-8")
    assert "not a line-by-line audit" in review
    assert "777ef71d123e8f85e6d1372225b5028744fc5ffe" in review
    assert "37143016886" in review
    assert "37142958088" in review
    assert "externally_verified_pending_import" in review
    assert "5acdf96aa311273fa02207e64c08b5509d144cc4f1921c9f101cd02570f77ede" in review
    assert "ae1979b484da8d30614776445e46f8b674e0d1a991688884685ba327296f398a" in review
    ledger = _rows()
    filed = next(row for row in ledger if row.get("review_id") == "004")
    assert filed["target_of_review"] == "research/constraint-lab-v0.4"
    assert filed["reviewed_commit"] == "777ef71d123e8f85e6d1372225b5028744fc5ffe"
    assert filed["ci_run_id"] == "37143016886"
    assert filed["preceding_ci_run_id"] == "37142958088"
    assert filed["execution_path"].endswith("004-n4-higher-order-reconfiguration.md")
    assert filed["line_by_line_audit"] is False
    first_003 = next(row for row in ledger if row["record_type"] == "prompt_representation" and row["prompt_id"] == "003")
    assert first_003["authored_prompt_status"] == "pending_verbatim_import"
    external = [
        row
        for row in ledger
        if row["record_type"] == "prompt_representation" and row["authored_prompt_status"] == "externally_verified_pending_import"
    ]
    by_id = {row["prompt_id"]: row for row in external}
    assert by_id["003"]["authored_prompt_sha256"] == "5acdf96aa311273fa02207e64c08b5509d144cc4f1921c9f101cd02570f77ede"
    assert by_id["003"]["authored_prompt_bytes"] == 27580
    assert by_id["003"]["authored_prompt_locally_present"] is False
    assert by_id["003"]["relationship"] == "unknown"
    assert by_id["004"]["authored_prompt_sha256"] == "ae1979b484da8d30614776445e46f8b674e0d1a991688884685ba327296f398a"
    assert by_id["004"]["authored_prompt_bytes"] == 32018
    assert by_id["004"]["agent_input_prompt_sha256"] == "f261527e522cc780f0937097b7de7706f7953f8bf69c59837442bbb7e1cf76ef"
    assert by_id["004"]["relationship"] == "unknown"


def test_prompt_005_agent_input_is_not_treated_as_the_authored_file():
    path = LAB / "provenance" / "prompts" / "005-v0.5-agent-input.md"
    assert path.stat().st_size == 39466
    assert _sha(path) == "e420caddf967d954c0b8b37aaa115b38c09341123a4047835e22e03ba64557c4"
    stored = next(row for row in _rows() if row["record_type"] == "prompt" and row["prompt_id"] == "005")
    assert stored["relationship"] == "unknown"
    assert stored["authored_prompt_sha256"] is None
    assert stored["authored_prompt_bytes"] is None
    assert stored["agent_input_prompt_sha256"] == stored["prompt_sha256"]
    assert stored["agent_input_prompt_bytes"] == 39466
    assert stored["harness_prompt_history_sha256"] == "dffc33fd4ea26411f1e05092e25046279e72c5a37d298c1bf90b88395071b8ae"
    assert stored["harness_prompt_history_bytes"] == 39464
    assert stored["relationship_agent_input_to_harness_prompt_history"] == "normalised"
    assert stored["result_branch"] == "research/constraint-lab-v0.5"
    assert "Review 005" in (LAB / "provenance" / "README.md").read_text(encoding="utf-8")


def test_same_edge_count_one_step_flux_is_a_structural_invariant():
    assert RECONFIGURATION_MEASURE == "max_abs_stationary_pair_event_class_flux_delta"
    table = pair_classes()
    assert table.path_name == PATH_CLASS == "e2-deg2110-tri0-comp2"
    assert table.matching_name == MATCHING_CLASS == "e2-deg1111-tri0-comp2"
    assert table.by_mask[table.path_mask]["edge_count"] == table.by_mask[table.matching_mask]["edge_count"] == 2
    assert table.path_mask != table.matching_mask
    for mask in range(64):
        for bit in range(6):
            nxt = mask ^ (1 << bit)
            assert abs(mask.bit_count() - nxt.bit_count()) == 1
            assert table.same_cardinality_nonisomorphic(mask, nxt) is False


def test_eventual_committor_matches_the_toy_chain_and_its_horizon_limit():
    landing = np.array(
        [
            [0.0, 1.0, 0.0],
            [0.25, 0.0, 0.75],
            [0.0, 0.0, 1.0],
        ],
        dtype=np.float64,
    )
    classes = np.array([0, 1, 2], dtype=np.int32)
    solved = eventual_committor(landing, classes, 0, 2, record_condition=True)
    assert solved["solver"]["failure"] is False
    assert solved["solver"]["method"] == "direct"
    assert solved["solver"]["matrix_dimension"] == 1
    assert solved["solver"]["precision"] == "float64"
    assert solved["solver"]["residual"] < 1e-12
    assert solved["q"][0] == pytest.approx(0.75)
    assert np.isnan(solved["q"][1]) and np.isnan(solved["q"][2])
    iterative = eventual_committor(landing, classes, 0, 2, method="iterative", iterative_tolerance=1e-14)
    assert iterative["q"][0] == pytest.approx(0.75)
    assert iterative["solver"]["failure"] is False
    mu = np.array([1.0, 0.0, 0.0])
    short = hit_passage(landing, mu, classes, 0, 2, horizon=1)
    longer = hit_passage(landing, mu, classes, 0, 2, horizon=2)
    limit = hit_passage(landing, mu, classes, 0, 2, horizon=40)
    assert short["hit_before_return"] == pytest.approx(0.0)
    assert longer["hit_before_return"] == pytest.approx(0.75)
    assert limit["hit_before_return"] == pytest.approx(solved["q"][0])
    assert limit["unresolved_within_horizon"] < 1e-12


def test_interaction_residual_identity_and_a_baseline_pair_is_zero():
    assert interaction_residual(0.5, 0.2, 0.1, 0.05) == pytest.approx(0.5 - 0.2 - 0.1 + 0.05)
    assert interaction_residual(0.2, 0.2, 0.2, 0.2) == pytest.approx(0.0)
    assert super_singleton_gap(0.5, 0.2, -0.4) == pytest.approx(0.1)
    q_tp = np.array([0.5, np.nan])
    q_t = np.array([0.2, 0.1])
    q_p = np.array([0.1, 0.1])
    q_0 = np.array([0.05, 0.1])
    state = state_interaction(q_tp, q_t, q_p, q_0)
    assert state[0] == pytest.approx(interaction_residual(0.5, 0.2, 0.1, 0.05))
    assert np.isnan(state[1])


def test_missing_effect_floor_and_a_changed_horizon_are_refused_before_a_solve():
    with pytest.raises(ValueError, match="effect_floor"):
        require_effect_floor({})
    slots = list(relation_slots(4, 3))
    constraint = parse_expression("form(0-1) | present(0-1-2) => prohibit", 4, order=3)
    with pytest.raises(RuntimeError, match="horizon"):
        assess_singleton_row(constraint, {"effect_floor": FLOOR, "reconfiguration_horizon": 8}, slots, {})
    other = parse_expression("form(0-1) | absent(0-2) => prohibit", 4, order=3)
    with pytest.raises(RuntimeError, match="horizon"):
        assess_pair_row(
            constraint,
            other,
            {"effect_floor": FLOOR, "alphabet": "W4", "reconfiguration_horizon": 32},
            slots,
            {},
            {},
        )


def test_plan_refuses_the_wrong_cardinality_before_enumeration():
    pair = _pair_spec()
    pair["cells"] = [{"N": 4, "K_max": 2, "A_max": 4, "cardinalities": [1]}]
    with pytest.raises(ValueError, match="cardinality 2"):
        build_plan(pair, 10)
    sensitivity = dict(pair)
    sensitivity["analysis"] = "n4-reconfiguration-sensitivity"
    sensitivity["cells"] = [{"N": 4, "K_max": 2, "A_max": 4, "cardinalities": [2]}]
    with pytest.raises(ValueError, match="cardinality above 1"):
        build_plan(sensitivity, 10)
    simplicial = dict(pair)
    simplicial["semantics"] = "simplicial"
    with pytest.raises(ValueError, match="simplicial"):
        validate_spec(simplicial)


def test_targeted_catalogue_canonicalises_complete_sets(targeted):
    coverage = targeted["coverage"]
    grammar = build_grammar(4, 2, WEIGHTS, a_max=4, predicates=("pair", "triad"), order=3)
    tp = [item for item in grammar.labelled if cross_order_class(item, 6) == "T->P"]
    pp = [item for item in grammar.labelled if cross_order_class(item, 6) == "P->P"]
    assert coverage["labelled_tp_weighted"] == len(tp)
    assert coverage["labelled_pp_weighted"] == len(pp)
    assert coverage["labelled_tp_structural"] * 2 == len(tp)
    assert coverage["labelled_pp_structural"] * 2 == len(pp)
    assert coverage["weighted_labelled_pairs"] == len(tp) * len(pp)
    assert coverage["invalid_pairs"] == 0
    assert coverage["labelled_pairs_accounted"] == coverage["weighted_labelled_pairs"]
    assert coverage["weight_grid_8x10x2x2"] == 320
    assert coverage["weight_grid_is_the_canonical_count"] is False
    assert coverage["canonical_weighted_pairs"] != 320
    assert coverage["canonical_weighted_pairs"] == len(targeted["representatives"])
    assert coverage["canonical_weighted_pairs"] == 4 * coverage["canonical_structural_pairs"]
    orbit_total = sum(int(size) * count for size, count in coverage["orbit_size_distribution"].items())
    assert orbit_total == coverage["weighted_labelled_pairs"]
    assert sum(coverage["orbit_size_distribution"].values()) == coverage["canonical_weighted_pairs"]
    assert coverage["canonical_weighted_pairs"] <= 20000
    groups: dict = {}
    for canon, alignment in zip(targeted["representatives"], targeted["alignments"]):
        key = (alignment["tp_orbit"], alignment["pp_orbit"], alignment["tp_weight"], alignment["pp_weight"])
        signature = (
            alignment["action_edge_relation"],
            alignment["tp_condition_vs_action"],
            alignment["pp_vertices_vs_tp_triad"],
        )
        groups.setdefault(key, []).append((canon, signature))
    mixed = [items for items in groups.values() if len({signature for _canon, signature in items}) > 1]
    assert mixed
    for items in mixed:
        canons = [canon for canon, _signature in items]
        assert len(set(canons)) == len(canons)
    slots = grammar.relation_slots
    maps = slot_permutation_maps(4, slots)
    labelled_index = {constraint.key(): index for index, constraint in enumerate(grammar.labelled)}
    for origin in (targeted["representatives"][0], targeted["representatives"][-1]):
        constraints = tuple(grammar.labelled[index] for index in origin)
        for slot_map in maps:
            image_ids = tuple(
                sorted(labelled_index[relabel_constraint(constraint, slot_map).key()] for constraint in constraints)
            )
            assert canonical_id_tuple(image_ids, grammar.image) == origin


def test_block_epoch_solver_matches_the_dense_solver_on_the_reference_kernels():
    cases = (
        (3, None),
        (3, "form(0-1) | present(0-1-2) => strong_favour"),
        (4, None),
        (4, "form(0-1) | present(0-1-2) => strong_favour"),
        (4, "form(0-1-2) | present(0-1) => strong_favour"),
        (4, "form(0-1) | present(0-1-2) => prohibit"),
    )
    table = pair_classes()
    shared_mu = None
    for n, text in cases:
        kernel, _slots = _kernel(n, text)
        n_pairs, _n_triads = layout(kernel)
        mask = (1 << n_pairs) - 1
        for source, row in enumerate(kernel.successors):
            if kernel.deadlock[source]:
                continue
            for target, prob in row:
                if not prob or target == source:
                    continue
                flipped = (source ^ target) & mask
                if flipped == 0:
                    assert (source & mask) == (target & mask)
                else:
                    assert flipped & (flipped - 1) == 0
        dense, dense_defect = epoch_kernel_float(kernel)
        block, block_defect = epoch_kernel_block(kernel)
        assert dense is not None and block is not None
        assert dense_defect is not None and block_defect is not None
        assert abs(dense_defect - block_defect) <= 1e-8
        assert float(np.max(np.abs(dense - block))) <= 1e-8
        sums = block.sum(axis=1)
        assert np.all((sums <= 1e-9) | (np.abs(sums - 1.0) <= 1e-8))
        assert block_defect >= 0.0
        _one_bit_pair_landings(block, n_pairs)
        pi, residual, _arithmetic, _periods = float_stationary(kernel)
        assert residual < 1e-8
        dense_tv, _dense_memory_defect = pair_event_epoch_memory_tv_float(kernel, pi, dense, dense_defect)
        block_tv, _block_memory_defect = pair_event_epoch_memory_tv_float(kernel, pi, block, block_defect)
        assert dense_tv is not None and block_tv is not None
        assert abs(dense_tv - block_tv) <= 1e-8
        if n != 4:
            continue
        for source_name, target_name in (
            (table.path_name, table.matching_name),
            (table.matching_name, table.path_name),
        ):
            dense_hit = focused_transition(kernel, pi, dense, source_name, target_name, table)
            block_hit = focused_transition(kernel, pi, block, source_name, target_name, table)
            assert dense_hit["passage"]["hit_before_return"] == pytest.approx(
                block_hit["passage"]["hit_before_return"], abs=1e-8
            )
        from rs_constraint_lab.passage import kernel_layout_index

        n_pairs, class_index, _table = kernel_layout_index(kernel, table)
        for source_name, target_name in (
            (table.path_name, table.matching_name),
            (table.matching_name, table.path_name),
        ):
            source = next(
                position
                for position, mask_id in enumerate(table.representatives)
                if table.by_mask[mask_id]["name"] == source_name
            )
            target = next(
                position
                for position, mask_id in enumerate(table.representatives)
                if table.by_mask[mask_id]["name"] == target_name
            )
            left = eventual_committor(dense, class_index, source, target)
            right = eventual_committor(block, class_index, source, target)
            assert left["solver"]["failure"] is False and right["solver"]["failure"] is False
            both = np.isfinite(left["q"]) & np.isfinite(right["q"])
            assert np.any(both)
            assert float(np.max(np.abs(left["q"][both] - right["q"][both]))) <= 1e-7
        if text is None:
            flux = class_flux(kernel, pi, block, table)
            for left_index, left_mask in enumerate(table.representatives):
                for right_index, right_mask in enumerate(table.representatives):
                    if table.by_mask[left_mask]["edge_count"] != table.by_mask[right_mask]["edge_count"]:
                        continue
                    if left_mask == right_mask:
                        continue
                    assert abs(float(flux[left_index, right_index])) <= 1e-12
            from rs_constraint_lab.passage import stationary_source_mu

            own = stationary_source_mu(kernel, pi, block)
            source = next(
                position
                for position, mask_id in enumerate(table.representatives)
                if table.by_mask[mask_id]["name"] == table.path_name
            )
            shared_mu = reference_source(own, class_index, source)
        if text is not None and shared_mu is not None:
            source = next(
                position
                for position, mask_id in enumerate(table.representatives)
                if table.by_mask[mask_id]["name"] == table.path_name
            )
            target = next(
                position
                for position, mask_id in enumerate(table.representatives)
                if table.by_mask[mask_id]["name"] == table.matching_name
            )
            first = prepare_direction(kernel, pi, block, class_index, n_pairs, source, target, shared_mu)
            second = prepare_direction(kernel, pi, block, class_index, n_pairs, source, target, shared_mu)
            assert first["mu_ref"] is shared_mu
            assert second["mu_ref"] is shared_mu


def test_sensitivity_uses_the_baseline_of_the_same_rate(targeted):
    slots = list(relation_slots(4, 3))
    constraint = parse_expression("form(0-1) | present(0-1-2) => strong_favour", 4, order=3)
    spec = {
        "effect_floor": FLOOR,
        "alphabet": "W4",
        "sensitivity_alphabets": ["W3"],
        "rho3_sensitivity": ["2"],
        "reconfiguration_horizon": 16,
    }
    cache: dict = {}
    row = assess_singleton_row(constraint, spec, slots, cache)
    assert set(row["probes"]) == {"primary", "rho2", "W3"}
    baseline_rhos = {key[2] for key in cache if key[0] == "baseline"}
    assert baseline_rhos == {"1", "2"}
    primary = row["probes"]["primary"]["path_to_matching"]
    varied = row["probes"]["rho2"]["path_to_matching"]
    alphabet = row["probes"]["W3"]["path_to_matching"]
    assert primary["baseline_rho"] == "1"
    assert varied["baseline_rho"] == "2"
    assert alphabet["baseline_rho"] == "1"
    assert alphabet["baseline_alphabet"] == "W3"
    for fields in (primary, varied, alphabet):
        assert fields["delta_hit_before_return"] == pytest.approx(
            fields["hit_before_return"] - fields["baseline_hit_before_return"]
        )
        assert fields["controlled_baseline_hit_before_return"] == pytest.approx(fields["baseline_hit_before_return"])
    event = primary["eventual"]
    assert event["solver"]["failure"] is False
    assert event["solver"]["precision"] == "float64"
    assert event["baseline_q_controlled"] == pytest.approx(event["baseline_q_stationary"])
    bare, _slots = _kernel(4, None)
    pi, _residual, _arithmetic, _periods = float_stationary(bare)
    landing, defect = epoch_kernel_block(bare)
    assert landing is not None and defect is not None
    from rs_constraint_lab.passage import kernel_layout_index, weighted_mean

    n_pairs, class_index, table = kernel_layout_index(bare)
    source = next(position for position, mask_id in enumerate(table.representatives) if table.by_mask[mask_id]["name"] == PATH_CLASS)
    target = next(position for position, mask_id in enumerate(table.representatives) if table.by_mask[mask_id]["name"] == MATCHING_CLASS)
    solved = eventual_committor(landing, class_index, source, target)
    q = solved["q"]
    assert interaction_residual(
        weighted_mean(q, reference_source(np.ones(bare.n_states) / bare.n_states, class_index, source)),
        weighted_mean(q, reference_source(np.ones(bare.n_states) / bare.n_states, class_index, source)),
        weighted_mean(q, reference_source(np.ones(bare.n_states) / bare.n_states, class_index, source)),
        weighted_mean(q, reference_source(np.ones(bare.n_states) / bare.n_states, class_index, source)),
    ) == pytest.approx(0.0)
    del targeted


def test_generation5_resume_keeps_the_completed_receipt(tmp_path):
    spec = _pair_spec()
    spec["experiment_id"] = "miniature-targeted-resume"
    path = tmp_path / "spec.json"
    path.write_text(json.dumps(spec), encoding="utf-8")
    out = tmp_path / "out"
    assert main(["run", str(path), "--out", str(out), "--workers", "1", "--shard-items", "1", "--max-shards", "1"]) == 0
    progress = json.loads((out / "progress.json").read_text(encoding="utf-8"))
    assert progress["status"] == "IN_PROGRESS"
    assert progress["completed"] == 1
    plan = json.loads((out / "plan.json").read_text(encoding="utf-8"))
    assert plan["estimates"]["cells"][0]["targeted_coverage"]["weight_grid_is_the_canonical_count"] is False
    assert plan["estimates"]["cells"][0]["targeted_coverage"]["canonical_weighted_pairs"] != 320
    done = next(
        shard["shard_id"]
        for shard in plan["shards"]
        if progress["shards"][shard["shard_id"]]["status"] == "completed"
    )
    receipt = (out / "shards" / done / "receipt.json").read_bytes()
    assert main(["run", str(path), "--out", str(out), "--workers", "1", "--shard-items", "1", "--max-shards", "1"]) == 0
    assert (out / "shards" / done / "receipt.json").read_bytes() == receipt
    again = json.loads((out / "progress.json").read_text(encoding="utf-8"))
    assert again["completed"] == 2
    assert again["status"] == "IN_PROGRESS"
