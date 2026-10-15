"""Exact refinement fixtures; new non-neutral analysis requires frozen publication."""

from __future__ import annotations

import json
import subprocess
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import pytest

from rs_constraint_lab.durable import sha256_file
from rs_constraint_lab.explore08 import FrozenPlanError, plan_hash
from rs_constraint_lab.gen008i_predictive_exec import (
    BASE, GRADES, MANIFEST, OUTPUT, PLAN, decode, digest, items, require_execution, validate_result,
)
from rs_constraint_lab.history import HistoryError, RecentReversal
from rs_constraint_lab.predictive_state import (
    PROJECTIONS, analyse_projection, balance_gap, commute, edge_role_partition,
    forward_triples, geometry, observation_labels,
)
from rs_constraint_lab.refinement import (
    canonical_partition, lumpability, partition_from_labels, refine,
)

ROOT = Path(__file__).resolve().parents[2]
PUBLISHED = (ROOT / MANIFEST).exists()
POST_FREEZE = pytest.mark.skipif(not PUBLISHED, reason="new non-neutral predictive analysis stays unopened until frozen execution")


def test_initial_partition_already_lumpable():
    rows = ({0: Fraction(1, 2), 2: Fraction(1, 2)}, {1: Fraction(1, 2), 2: Fraction(1, 2)}, {2: Fraction(1)})
    result = refine(rows, ((0, 1), (2,)))
    assert result["stable_blocks"] == ((0, 1), (2,))
    assert result["refinement_rounds"] == 0
    assert result["merge_obstructions"] == []


def test_one_split_and_merge_obstruction():
    rows = ({2: Fraction(1)}, {1: Fraction(1)}, {2: Fraction(1)})
    result = refine(rows, ((0, 1), (2,)))
    assert result["stable_blocks"] == ((0,), (1,), (2,))
    assert result["refinement_rounds"] == 1
    witness = result["merge_obstructions"][0]
    assert witness["merge_obstruction"]["probability_A"] != witness["merge_obstruction"]["probability_B"]
    assert result["distinct_next_observation_rows_within_current_observation"]


def test_later_distinction_requires_recursive_refinement():
    rows = tuple({target: Fraction(1)} for target in (2, 3, 4, 5, 4, 5))
    result = refine(rows, ((0, 1), (2, 3), (4,), (5,)))
    assert result["refinement_rounds"] == 2
    assert result["stable_block_count"] == 6
    assert [step["after_count"] for step in result["refinement_chronology"]] == [5, 6]
    assert not result["distinct_next_observation_rows_within_current_observation"]
    assert any(row["next_observation_obstruction"] is None for row in result["merge_obstructions"])


@pytest.mark.parametrize("parameter,expected", [(Fraction(1), 2), (Fraction(2), 3)])
def test_synthetic_neutral_parameter_collapse(parameter, expected):
    probability = parameter / (parameter + 1)
    rows = ({0: probability, 2: 1 - probability}, {1: Fraction(1, 2), 2: Fraction(1, 2)}, {2: Fraction(1)})
    assert refine(rows, ((0, 1), (2,)))["stable_block_count"] == expected


@pytest.mark.parametrize("rows,partition", [
    (({0: 0.5, 1: 0.5}, {1: 1}), ((0,), (1,))),
    (({0: Fraction(1, 2)},), ((0,),)),
    (({1: Fraction(1)},), ((0,),)),
    (({0: Fraction(1)},), ((0, 0),)),
    (({0: Fraction(1)},), ((), (0,))),
])
def test_invalid_exact_inputs_rejected(rows, partition):
    with pytest.raises(HistoryError):
        refine(rows, partition)


def test_arbitrary_state_reordering_preserves_recursive_partition():
    rows = tuple({target: Fraction(1)} for target in (2, 3, 4, 5, 4, 5))
    labels = ("a", "a", "b", "b", "c", "d")
    order = (4, 2, 0, 5, 1, 3)
    inverse = {old: new for new, old in enumerate(order)}
    permuted = tuple({inverse[target]: mass for target, mass in rows[old].items()} for old in order)
    original = refine(rows, partition_from_labels(labels))
    actual = refine(permuted, partition_from_labels([labels[old] for old in order]))
    restored = canonical_partition([[order[state] for state in block] for block in actual["stable_blocks"]], 6)
    assert restored == original["stable_blocks"]


@pytest.fixture(scope="module")
def neutral_results():
    return {projection: analyse_projection(RecentReversal(Fraction(1)), projection) for projection in PROJECTIONS}


@pytest.mark.parametrize("projection,count", tuple(zip(PROJECTIONS, (64, 11, 7, 2))))
def test_neutral_production_partition_and_information(neutral_results, projection, count):
    result = neutral_results[projection]
    validate_result({"kind": "refine", "projection": projection, "m": "1"}, result)
    assert result["stable_block_count"] == result["initial_block_count"] == count
    assert result["refinement_rounds"] == 0
    assert Decimal(result["temporal_information"]["conditional_MI"]) == 0
    assert result["synchronization"]["markov_order"] == 1
    assert result["synchronization"]["synchronization_length"] == 1


def test_missing_freeze_refused_before_scientific_execution():
    with pytest.raises(FrozenPlanError):
        require_execution(ROOT, None)
    assert len(items()) == 15


def load_primary():
    plan = json.loads((ROOT / PLAN).read_text())
    return {
        (item["grade"], item["projection"]): decode(json.loads((ROOT / OUTPUT / (item["item_id"] + ".json")).read_text())["result"])
        for item in plan["items"] if item["kind"] == "refine"
    }


@POST_FREEZE
@pytest.mark.parametrize("projection", PROJECTIONS)
@pytest.mark.parametrize("grade,m", GRADES)
def test_published_refinement_certificates(projection, grade, m):
    result = load_primary()[grade, projection]
    validate_result({"kind": "refine", "projection": projection, "m": m}, result)
    rows = RecentReversal(Fraction(m)).epoch_kernel()
    quotient, gap = lumpability(rows, result["stable_blocks"])
    assert gap == balance_gap(result["stationary_mass"], quotient) == 0
    assert result["stationary_triples"] == [
        {"word": list(word), "probability": probability}
        for word, probability in sorted(forward_triples(rows, projection).items())
    ]
    labels = observation_labels(projection)
    assert all(len({labels[state] for state in block}) == 1 for block in result["stable_blocks"])
    if Fraction(m) != 1:
        assert result["stable_blocks"] == load_primary()["m4" if grade == "m025" else "m025", projection]["stable_blocks"]
        assert all(row["next_observation_obstruction"] is not None for row in result["merge_obstructions"])
    assert result["one_step_H0_gap"] == 0


@POST_FREEZE
def test_plan_and_published_files_have_deterministic_hashes():
    manifest = json.loads((ROOT / MANIFEST).read_text())
    plan = json.loads((ROOT / PLAN).read_text())
    assert plan_hash(plan) == plan["plan_hash"] == manifest["plan_hash"]
    assert plan["pre_freeze_exposure"]["new_non_neutral_variant_target_executions"] == 0
    assert plan["pre_freeze_exposure"]["blind_round"] is False
    for path, sha in manifest["item_sha256"].items():
        assert sha256_file(ROOT / path) == sha
        envelope = json.loads((ROOT / path).read_text())
        assert digest(envelope["result"]) == envelope["result_sha256"]
    assert len(manifest["item_sha256"]) == 15
    for path, sha in {**plan["source_sha256"], **plan["input_sha256"]}.items():
        assert sha256_file(ROOT / path) == sha


@POST_FREEZE
def test_exact_commuting_quotient_ladder():
    records = commute(load_primary())
    assert len(records) == 9
    assert all(record["exact_block_transition_gap"] == record["stationary_pushforward_gap"] == 0 for record in records)
    assert sum(map(len, geometry()[2])) == 384
    assert sum(map(len, edge_role_partition())) == 384


@POST_FREEZE
def test_every_published_merge_obstruction_replays():
    count = 0
    for result in load_primary().values():
        quotient = [dict(row) for row in result["quotient_kernel"]]
        for record in result["merge_obstructions"]:
            left, right = record["block_A"], record["block_B"]
            witness = record["merge_obstruction"]
            target = witness["target_blocks_after_merge"]
            a = sum(quotient[left].get(block, 0) for block in target)
            b = sum(quotient[right].get(block, 0) for block in target)
            assert a == witness["probability_A"] != witness["probability_B"] == b
            assert record["next_observation_obstruction"] is not None
            count += 1
    assert count == 1986


@POST_FREEZE
def test_role_atlas_and_observable_pair_bijections():
    orbit = decode(json.loads((ROOT / OUTPUT / "I-ORBIT-ATLAS.json").read_text())["result"])
    assert orbit["orbit_count"] == 28
    assert sum(row["stationary_mass"] for row in orbit["orbit_atlas"]) == 1
    assert all(row["exact_gap"] == 0 for row in orbit["covariance"])
    assert all(row["comparisons"] == 24 * 384 * 6 for row in orbit["covariance"])
    assert len({(row["predecessor_class"], row["graph_class"]) for row in orbit["orbit_atlas"]}) == 28
    results = load_primary()
    for grade in ("m025", "m4"):
        for projection, size in (("labelled_mask", 384), ("graph_class", 28), ("edge_count", 12), ("parity", 2)):
            sync = results[grade, projection]["synchronization"]
            assert sync["bijection_verified"] and sync["legal_ordered_observation_pairs"] == size
            assert sync["markov_order"] == (1 if projection == "parity" else 2)
        for projection in PROJECTIONS:
            for source, row in enumerate(RecentReversal(Fraction(results[grade, projection]["m"])).epoch_kernel()):
                assert all(((source // 6).bit_count() ^ (target // 6).bit_count()) & 1 for target in row)


def test_predictive_snapshot_uses_immutable_ledger_prefix(tmp_path):
    from rs_constraint_lab.coherence import snapshot_text
    snapshot = ROOT / "constraint-lab/coherence/snapshots/through-generation-008i.md"
    if not snapshot.exists():
        pytest.skip("snapshot not yet published")
    for name, count in (("findings.jsonl", 140), ("relations.jsonl", 205)):
        historical = subprocess.run(
            ["git", "-C", str(ROOT), "show", "6c8f052c2d3361516e08c5a3def10a15474096cc:constraint-lab/coherence/" + name],
            capture_output=True, check=True,
        ).stdout
        lines = historical.splitlines(keepends=True)
        (tmp_path / name).write_bytes(b"".join(lines[:count]))
    assert snapshot.read_text() == snapshot_text(tmp_path, title="Through Generation 008I (Predictive State)")


def test_prompt_variant_and_reviewed_artifacts_preserved():
    path = ROOT / "constraint-lab/provenance/prompts/008I-v0.8i-predictive-state-agent-input.md"
    assert len(path.read_bytes()) == 54159
    assert sha256_file(path) == "99cce12712ab204a60c6c67a8bbe7c75492a2a43562289e0cdf3d1029a2e70fc"
    def git(*args):
        return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, check=True).stdout
    previous = set(git("ls-tree", "-r", "--name-only", BASE).decode().splitlines())
    changed = set(git("diff", "--name-only", BASE, "--", "books", "constraint-lab/reports",
                      "constraint-lab/exploration", "constraint-lab/provenance",
                      "constraint-lab/coherence/snapshots").decode().splitlines())
    assert previous & changed <= {"constraint-lab/provenance/ledger.jsonl"}
    for name in ("formal/theorem-catalog.jsonl", "coherence/findings.jsonl",
                 "coherence/relations.jsonl", "provenance/ledger.jsonl"):
        before = git("show", BASE + ":constraint-lab/" + name)
        after = (ROOT / "constraint-lab" / name).read_bytes()
        if name != "coherence/findings.jsonl":
            assert after.startswith(before)
            continue
        from rs_constraint_lab.status_history import validate_status_history
        assert validate_status_history(ROOT, before.splitlines(), after.splitlines())
        for old, current in zip(before.splitlines(), after.splitlines()):
            row = json.loads(old)
            if row["finding_id"] in {"Q-H-MINIMAL-STATE", "Q-H-COARSE-GRAINING"}:
                assert json.loads(current) == {**row, "status": "qualified"}
