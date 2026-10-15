"""Tiny exact proof fixtures, not new laboratory scientific cells."""

from __future__ import annotations

from collections import defaultdict
from hashlib import sha256
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import subprocess

import pytest

from rs_constraint_lab.refinement import (
    block_index, canonical_partition, lumpability, partition_from_labels, refine,
)
from rs_constraint_lab.synthesis import AUDIT, BASE, HEADS, branch_audit, diagram_views, verify

ROOT = Path(__file__).resolve().parents[2]


def partitions(size):
    def visit(state, blocks):
        if state == size:
            yield canonical_partition(blocks, size)
            return
        for i in range(len(blocks)):
            yield from visit(state + 1, blocks[:i] + [blocks[i] + [state]] + blocks[i + 1:])
        yield from visit(state + 1, blocks + [[state]])
    return list(visit(0, []))


def refines(fine, coarse, size):
    index = block_index(coarse, size)
    return all(len({index[state] for state in block}) == 1 for block in fine)


def words(rows, labels, initial, length):
    current = defaultdict(dict)
    for state, mass in enumerate(initial):
        if mass:
            current[(labels[state],)][state] = mass
    for _ in range(length - 1):
        following = defaultdict(lambda: defaultdict(F))
        for word, endpoints in current.items():
            for source, mass in endpoints.items():
                for target, probability in rows[source].items():
                    following[word + (labels[target],)][target] += mass * probability
        current = following
    return {word: dict(row) for word, row in current.items()}


def word_masses(rows, labels, initial, length):
    return {word: sum(row.values()) for word, row in words(rows, labels, initial, length).items()}


def pushed(initial, rows):
    result = [F(0)] * len(rows)
    for source, row in enumerate(rows):
        for target, probability in row.items():
            result[target] += initial[source] * probability
    return result


def trace_fixture():
    return (
        ({2: F(1, 2), 3: F(1, 2)}, {4: F(1)}, {5: F(1)}, {6: F(1)},
         {5: F(1, 2), 6: F(1, 2)}, {5: F(1)}, {6: F(1)}),
        ("A", "A", "B", "B", "B", "C", "D"),
    )


def weak_fixture():
    states = tuple(product(range(2), repeat=2))
    rows = []
    for _, hidden in states:
        p = F(1, 4) if hidden == 0 else F(3, 4)
        rows.append({target: (p if y == 1 else 1 - p) / 2
                     for target, (y, _) in enumerate(states)})
    return rows, tuple(y for y, _ in states), [F(1, 4)] * 4


def even_fixture():
    return ({0: F(1, 2), 1: F(1, 2)}, {2: F(1)}, {0: F(1, 2), 1: F(1, 2)}), (0, 1, 1), [F(1, 3)] * 3


KERNELS = (
    tuple({state: F(1)} for state in range(4)),
    tuple({(state + 1) % 4: F(1)} for state in range(4)),
    tuple({state: F(1, 4) for state in range(4)} for _ in range(4)),
    weak_fixture()[0],
)


@pytest.mark.parametrize("rows", KERNELS)
def test_coarsest_refinement_universal_property(rows):
    candidates = partitions(4)
    assert len(candidates) == len(set(candidates)) == 15
    for initial in candidates:
        stable = refine(rows, initial)["stable_blocks"]
        assert refines(stable, initial, 4)
        assert lumpability(rows, stable)[1] == 0
        assert refine(rows, stable)["stable_blocks"] == stable
        eligible = [p for p in candidates if refines(p, initial, 4) and lumpability(rows, p)[1] == 0]
        assert all(refines(other, stable, 4) for other in eligible)
        assert [p for p in eligible if all(refines(other, p, 4) for other in eligible)] == [stable]


@pytest.mark.parametrize("rows", KERNELS)
def test_observation_coarsening_and_induced_kernel_square(rows):
    candidates = partitions(4)
    stable = {p: refine(rows, p)["stable_blocks"] for p in candidates}
    for fine in candidates:
        for coarse in candidates:
            if not refines(fine, coarse, 4):
                continue
            a, b = stable[fine], stable[coarse]
            assert refines(a, b, 4) and len(a) >= len(b)
            qa, gap_a = lumpability(rows, a)
            qb, gap_b = lumpability(rows, b)
            assert gap_a == gap_b == 0
            b_of = block_index(b, 4)
            mapping = [b_of[block[0]] for block in a]
            for source, row in enumerate(qa):
                aggregate = defaultdict(F)
                for target, mass in row.items():
                    aggregate[mapping[target]] += mass
                assert dict(aggregate) == qb[mapping[source]]


def test_all_word_trace_equality_does_not_imply_strong_equivalence():
    rows, labels = trace_fixture()
    result = refine(rows, partition_from_labels(labels))
    assert result["refinement_rounds"] == 2 and result["stable_block_count"] == 7
    assert result["state_to_block"][0] != result["state_to_block"][1]
    initial_a, initial_b = [F(1)] + [F(0)] * 6, [F(0), F(1)] + [F(0)] * 5
    assert pushed(pushed(initial_a, rows), rows) == pushed(pushed(initial_b, rows), rows)
    assert {labels[target] for target in rows[0]} == {labels[target] for target in rows[1]} == {"B"}
    assert rows[5] == {5: F(1)} and rows[6] == {6: F(1)}
    for length in range(1, 7):
        assert word_masses(rows, labels, initial_a, length) == word_masses(rows, labels, initial_b, length)


def test_stationary_weak_lumping_without_strong_lumping_or_synchronization():
    rows, labels, pi = weak_fixture()
    assert pushed(pi, rows) == pi
    result = refine(rows, partition_from_labels(labels))
    assert result["stable_block_count"] == 4
    assert lumpability(rows, partition_from_labels(labels))[1] > 0
    # Equal target-pair entries give the all-history uniform-hidden posterior inductively.
    assert all(row[0] == row[1] and row[2] == row[3] for row in rows)
    for length in range(1, 7):
        endpoints = words(rows, labels, pi, length)
        assert len(endpoints) == 2 ** length
        for word, masses in endpoints.items():
            assert set(masses) == {2 * word[-1], 2 * word[-1] + 1}
            assert len(set(masses.values())) == 1
            assert sum(masses.values()) == F(1, 2 ** length)


@pytest.mark.parametrize("depth", (1, 2, 3, 5, 8))
def test_small_state_count_gives_no_finite_observed_order_bound(depth):
    rows, labels, pi = even_fixture()
    assert pushed(pi, rows) == pi
    assert refine(rows, partition_from_labels(labels))["stable_block_count"] == 3
    n = depth if depth % 2 else depth + 1
    contexts = [(0,) + (1,) * n, (0,) + (1,) * (n + 1)]
    assert contexts[0][-depth:] == contexts[1][-depth:]
    endpoint_sets = []
    for word in contexts:
        endpoint_sets.append(set(words(rows, labels, pi, len(word))[word]))
    assert endpoint_sets == [{1}, {2}]
    assert sum(p for target, p in rows[1].items() if labels[target] == 0) == 0
    assert sum(p for target, p in rows[2].items() if labels[target] == 0) == F(1, 2)


def test_two_observation_synchronization_and_order_two_witness():
    rows = ({1: F(1)}, {2: F(1)}, {0: F(1)})
    labels, pi = (1, 1, 0), [F(1, 3)] * 3
    result = refine(rows, partition_from_labels(labels))
    assert result["stable_block_count"] == 3
    pairs = words(rows, labels, pi, 2)
    assert len(pairs) == 3 and all(len(row) == 1 for row in pairs.values())
    assert set(pairs[0, 1]) == {0} and set(pairs[1, 1]) == {1}
    assert {labels[target] for target in rows[0]} == {1}
    assert {labels[target] for target in rows[1]} == {0}


def flatten(states, event_law, update):
    index = {state: i for i, state in enumerate(states)}
    rows = []
    for state in states:
        row = defaultdict(F)
        for event, probability in event_law(state).items():
            row[index[update(state, event)]] += probability
        rows.append(dict(row))
    return rows


def test_finite_history_augmentation_and_eta_alone_insufficiency():
    states = tuple(product(range(2), repeat=2))  # (ordinary current, previous)
    event_law = lambda state: {state[0] ^ state[1]: F(1)}
    update = lambda state, event: (event, state[0])
    rows = flatten(states, event_law, update)
    for i, state in enumerate(states):
        assert rows[i] == {states.index((state[0] ^ state[1], state[0])): F(1)}
    labels = tuple(state[0] for state in states)
    pi = [F(0), F(1, 3), F(1, 3), F(1, 3)]
    assert pushed(pi, rows) == pi
    assert lumpability(rows, partition_from_labels(labels))[1] > 0
    # A constant eta cannot remove the two supported previous-state distinctions.
    assert rows[states.index((1, 0))] != rows[states.index((1, 1))]


def test_finite_constraint_state_fixed_kernel_flattening():
    states = tuple(product(range(2), repeat=2))  # abstract ordinary symbol, enable state
    def law(state):
        p = F(1, 4) if state[1] == 0 else F(3, 4)
        return {0: 1 - p, 1: p}
    update = lambda state, event: (state[0] ^ event, 1 - state[1])
    rows = flatten(states, law, update)
    assert all(sum(row.values()) == 1 for row in rows)
    for i, (ordinary, eta) in enumerate(states):
        for target, probability in rows[i].items():
            next_ordinary, next_eta = states[target]
            assert next_eta == 1 - eta
            assert probability == law((ordinary, eta))[ordinary ^ next_ordinary]
    # Sum over event histories equals iteration of the fixed augmented kernel.
    current = {states[0]: F(1)}
    pi = [F(1), F(0), F(0), F(0)]
    for _ in range(4):
        following = defaultdict(F)
        for state, mass in current.items():
            for event, probability in law(state).items():
                following[update(state, event)] += mass * probability
        current = following
        pi = pushed(pi, rows)
        assert pi == [current[state] for state in states]


def test_fixed_support_grammar_cannot_generate_a_missing_observed_jump():
    rows = tuple({state ^ toggle: F(1, 3) for toggle in (1, 2, 3)} for state in range(4))
    for state, row in enumerate(rows):
        assert sum(row.values()) == 1
        ordinary_support = {state ^ 1, state ^ 2}
        assert row[state ^ 3] > 0 and state ^ 3 not in ordinary_support


def test_stationary_markovisation_matches_pairs_but_not_triples():
    rows, labels, pi = even_fixture()
    assert pushed(pi, rows) == pi
    q, marginal = ({0: F(1, 2), 1: F(1, 2)}, {0: F(1, 4), 1: F(3, 4)}), [F(1, 3), F(2, 3)]
    assert pushed(marginal, q) == marginal
    assert word_masses(rows, labels, pi, 1) == word_masses(q, (0, 1), marginal, 1)
    assert word_masses(rows, labels, pi, 2) == word_masses(q, (0, 1), marginal, 2)
    assert word_masses(rows, labels, pi, 3).get((0, 1, 0), F(0)) == 0
    assert word_masses(q, (0, 1), marginal, 3)[0, 1, 0] == F(1, 24)


def test_pinned_branch_reconciliation_and_namespaces():
    audit = branch_audit(ROOT)
    assert audit == json.loads((ROOT / AUDIT).read_text())
    assert audit["identifier_conflicts"] == [] and not audit["alias_records_needed"]
    assert audit["catalogue_maxima"] == {"T": 59, "F": 8, "N": 8, "I": 2, "M": 3, "Q": 6}
    assert [record["artifacts"]["catalogue"]["rows"] for record in audit["heads"].values()] == [68, 68, 76]
    assert verify(ROOT)["scientific_computation"] is False
    for branch in ("alternate_role_8i", "coarse_process_8j"):
        result = subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", HEADS[branch], "HEAD"])
        assert result.returncode == 1
    assert subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", BASE, "HEAD"]).returncode == 0


def test_branch_source_references_exist_without_copying_results():
    references = {
        "alternate_role_8i": [
            "constraint-lab/reports/generation-008i-historical-role-grammar.md",
            "constraint-lab/formal/history-role-grammar.md",
        ],
        "coarse_process_8j": [
            "constraint-lab/reports/generation-008j-coarse-process-memory.md",
            "constraint-lab/formal/coarse-process-memory.md",
            "constraint-lab/provenance/reviews/008I-chatgpt-review-v0.8i.md",
        ],
    }
    for branch, paths in references.items():
        for path in paths:
            subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", HEADS[branch] + ":" + path], check=True)
    assert not (ROOT / "constraint-lab/reports/tables/generation-008j-word-atlas.json").exists()
    assert not (ROOT / "constraint-lab/exploration/generation-008k/round-k0-plan.json").exists()


def test_generated_conceptual_diagrams_match_structure():
    diagrams = diagram_views(ROOT)
    assert len(diagrams) == 4
    assert all(path.read_text() == expected for path, expected in diagrams.items())
    assert "no guaranteed first-order kernel" in next(text for path, text in diagrams.items() if path.stem == "raw-observation-square")


def test_prompt_and_review_representations_remain_distinct():
    from rs_constraint_lab.durable import sha256_file
    prompt = ROOT / "constraint-lab/provenance/prompts/008K-v0.8k-agent-input.md"
    assert prompt.stat().st_size == 54279
    assert sha256_file(prompt) == "ecc61164c45b2c6b2f2282e7251418d7f4f8f1c4179c86674cd2e2955576806f"
    assert "ecc61164c45b2c6b2f2282e7251418d7f4f8f1c4179c86674cd2e2955576806f" not in prompt.read_text()
    ledger = [json.loads(line) for line in (ROOT / "constraint-lab/provenance/ledger.jsonl").read_text().splitlines()]
    authored = next(row for row in ledger if row["record_type"] == "prompt_representation"
                    and row["prompt_id"] == "008I" and row.get("authored_prompt_bytes") == 54103)
    assert authored["authored_prompt_sha256"] == "78728586acc1c47a0b0f3af9b418c0b6e66b06a081e39cc5ce17bde1dc4af43a"
    assert authored["agent_input_prompt_sha256"] != authored["authored_prompt_sha256"]
    review = (ROOT / "constraint-lab/provenance/reviews/008I-predictive-state-chatgpt-review-v0.8i.md").read_text()
    assert "No rerun required" in review and "not blind" in review


def test_only_recorded_historical_question_status_fields_change():
    path = "constraint-lab/coherence/findings.jsonl"
    before = subprocess.run(["git", "-C", str(ROOT), "show", BASE + ":" + path],
                            capture_output=True, check=True).stdout.splitlines()
    after = (ROOT / path).read_bytes().splitlines()
    record_path = ROOT / "constraint-lab/provenance/status-changes/008K-h-questions.json"
    record = json.loads(record_path.read_text())
    transitions = {row["finding_id"]: row for row in record["transitions"]}
    assert set(transitions) == {"Q-H-MINIMAL-STATE", "Q-H-COARSE-GRAINING"}
    assert len(after) >= len(before)
    from rs_constraint_lab.status_history import validate_status_history
    assert validate_status_history(ROOT, before, after)
    for old, new in zip(before, after):
        original = json.loads(old)
        identifier = original["finding_id"]
        if identifier not in transitions:
            continue
        change = transitions[identifier]
        assert original["status"] == change["from"] == "unresolved"
        assert json.loads(new) == {**original, "status": change["to"]}
        assert change["to"] == "qualified" and change["changed_fields"] == ["status"]
        assert sha256(old).hexdigest() == change["before_row_sha256"]
        assert sha256(new).hexdigest() == change["after_row_sha256"]
    relations = [json.loads(line) for line in (ROOT / "constraint-lab/coherence/relations.jsonl").read_text().splitlines()]
    assert all(any(r["from_finding"] == identifier and r["relation_type"] == "partially_answered_by"
                   for r in relations) for identifier in transitions)
    ledger = [json.loads(line) for line in (ROOT / "constraint-lab/provenance/ledger.jsonl").read_text().splitlines()]
    status_record = next(r for r in ledger if r["record_type"] == "coherence_status_change" and r["prompt_id"] == "008K")
    assert status_record["transitions"] == record["transitions"]


def test_canonical_historical_artifacts_immutable_and_ledgers_append_only():
    def git(*args):
        return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, check=True).stdout
    original = set(git("ls-tree", "-r", "--name-only", BASE).decode().splitlines())
    changed = set(git("diff", "--name-only", BASE, "--", "books", "constraint-lab/reports",
                      "constraint-lab/exploration", "constraint-lab/provenance",
                      "constraint-lab/coherence/snapshots").decode().splitlines())
    assert original & changed <= {"constraint-lab/provenance/ledger.jsonl"}
    for path in ("constraint-lab/formal/theorem-catalog.jsonl",
                 "constraint-lab/formal/status-audit.jsonl",
                 "constraint-lab/coherence/relations.jsonl",
                 "constraint-lab/provenance/ledger.jsonl"):
        assert (ROOT / path).read_bytes().startswith(git("show", BASE + ":" + path))


def test_8k_snapshot_reproduces_its_pinned_ledger_not_future_statuses(tmp_path):
    from rs_constraint_lab.coherence import canonical_ledger_bytes, snapshot_text
    receipt = json.loads((ROOT / "constraint-lab/exploration/generation-008k/coherence-receipt.json").read_text())
    commit = receipt["ledger_commit"]
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", commit, "HEAD"], check=True)
    for name in ("findings.jsonl", "relations.jsonl"):
        content = subprocess.run(["git", "-C", str(ROOT), "show", commit + ":constraint-lab/coherence/" + name],
                                 capture_output=True, check=True).stdout
        (tmp_path / name).write_bytes(content)
    expected = snapshot_text(tmp_path, title=receipt["title"]).encode()
    actual = (ROOT / receipt["snapshot_path"]).read_bytes()
    assert actual == expected
    assert sha256(actual).hexdigest() == receipt["snapshot_sha256"]
    assert sha256(canonical_ledger_bytes(tmp_path)).hexdigest() == receipt["canonical_ledger_sha256"]
