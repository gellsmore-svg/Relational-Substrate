"""8J neutral/synthetic pre-freeze checks and immutable post-publication tests."""

from __future__ import annotations

import gzip
import json
import subprocess
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

import pytest

from rs_constraint_lab.coarse_process import (
    ObservedChain, analyse, chains_for, conditional_word_information, edge_chain,
    edge_map, hidden_path_words, lumpability, predictive_residual, project_words,
    published_models, sparse_words, triple_cmi, word_information,
)
from rs_constraint_lab.durable import canonical_json, read_json, sha256_file
from rs_constraint_lab.explore08 import FrozenPlanError, plan_hash
from rs_constraint_lab.gen008j_exec import (
    BASE, MANIFEST, PLAN, complement_validation, load_envelope, load_word_file,
    require_execution, validate_result,
)
from rs_constraint_lab.history import HistoryError

ROOT = Path(__file__).resolve().parents[2]
PUBLISHED = pytest.mark.skipif(not (ROOT / MANIFEST).exists(), reason="A/C word checks remain unopened until J0 publication")


def synthetic_pair():
    h = ObservedChain(({1: Fraction(1)}, {2: Fraction(1)}, {0: Fraction(1)}),
                      (Fraction(1, 3),) * 3, ("a", "a", "b"))
    k = ObservedChain(({0: Fraction(1, 2), 1: Fraction(1, 2)}, {0: Fraction(1)}),
                      (Fraction(2, 3), Fraction(1, 3)), ("a", "b"))
    return h, k


def test_sparse_engine_against_independent_hidden_path_enumeration():
    for chain in synthetic_pair():
        words, counts = sparse_words(chain)
        oracle, visits = hidden_path_words(chain)
        assert oracle == words
        assert visits > 0
        for length, law in words.items():
            assert sum(law.values()) == 1 and min(law.values()) > 0
            assert counts["reachable_words"][length] == len(law)


def test_synthetic_matched_pairs_can_have_different_triples():
    h, k = (sparse_words(chain)[0] for chain in synthetic_pair())
    assert h[1] == k[1] and h[2] == k[2]
    assert h[3] != k[3]
    assert word_information(h[1], k[1])[0] == 0
    assert word_information(h[3], k[3])[0] > 0
    assert triple_cmi(h[3])["exact_conditional_independence"] is False
    assert triple_cmi(k[3])["exact_conditional_independence"] is True


def test_finite_depth_rows_do_not_mislabel_consistency_as_proof():
    h, k = (sparse_words(chain)[0] for chain in synthetic_pair())
    assert predictive_residual(h, 1)["conditional_row_gap"] > 0
    assert predictive_residual(h, 2)["conditional_row_gap"] == 0
    assert predictive_residual(h, 2)["reading"] == "consistent at tested depth only"
    assert all(predictive_residual(k, r)["conditional_row_gap"] == 0 for r in range(1, 5))


def test_strong_lumpability_is_an_all_block_row_test():
    h, k = synthetic_pair()
    assert not lumpability(h)["strongly_lumpable"]
    assert lumpability(h)["witness"] is not None
    assert lumpability(k)["strongly_lumpable"]
    assert lumpability(k)["block_row_gap"] == 0


def test_word_information_chain_with_unequal_block_priors():
    a = {("a",): Fraction(1, 2), ("b",): Fraction(1, 3), ("c",): Fraction(1, 6)}
    b = {("a",): Fraction(1, 6), ("b",): Fraction(1, 3), ("c",): Fraction(1, 2)}
    mapping = {"a": 0, "b": 0, "c": 1}
    with localcontext() as ctx:
        ctx.prec = 160
        fine = word_information(a, b)[0]
        coarse = word_information(project_words(a, mapping), project_words(b, mapping))[0]
        conditional = conditional_word_information(a, b, mapping)
        assert fine >= coarse >= 0
        assert abs(fine - coarse - conditional) < Decimal("1e-25")
    assert conditional_word_information(a, a, mapping) == 0


def test_invalid_nonstationary_or_unnormalised_chain_rejected():
    h, _ = synthetic_pair()
    with pytest.raises(HistoryError):
        sparse_words(ObservedChain(h.rows, (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)), h.observations))
    with pytest.raises(HistoryError):
        sparse_words(ObservedChain(({0: Fraction(1, 2)},), (Fraction(1),), ("x",)))


@pytest.fixture(scope="module")
def neutral():
    return analyse(published_models(ROOT)["I0-NEUTRAL"], independent=True)


def test_neutral_all_lengths_are_exact_controls(neutral):
    result, words = neutral
    validate_result(result)
    assert all(row["exact_equal"] and Decimal(row["word_JS"]) == 0 for row in result["word_atlas"])
    assert all(Decimal(row["I_model_class_word_given_edge_word"]) == 0 for row in result["process_information"])
    assert result["first_visible_word_length"] == {"graph_class": None, "edge_count": None}
    assert result["validation"]["independent_crosscheck_performed"]
    for model in ("H", "Kpi"):
        for projection in ("graph_class", "edge_count"):
            assert result["diagnostics"][model][projection]["strongly_lumpable"]
            assert result["diagnostics"][model][projection]["exact_conditional_independence"]
    assert len(words["words"]) == 12


def test_neutral_direct_edge_engine_and_class_pushforward():
    h, k, checks = chains_for(published_models(ROOT)["I0-NEUTRAL"])
    assert checks["Kpi_covariance_transition_comparisons"] == 24 * 64 * 6
    assert len(h.rows) == 28 and len(k.rows) == 11
    for chain in (h, k):
        classes = sparse_words(chain)[0]
        edges = sparse_words(edge_chain(chain))[0]
        assert all(project_words(classes[length], edge_map()) == edges[length] for length in range(1, 7))


def test_canonical_word_serialisation_is_order_independent(neutral):
    _, words = neutral
    raw = canonical_json(words).encode()
    assert gzip.compress(raw, mtime=0) == gzip.compress(raw, mtime=0)
    assert json.loads(raw)["clock"] == "pair-event epoch"
    for block in words["words"]:
        assert list(block["rows"]) == sorted(block["rows"], key=lambda row: row["word"])


def test_execution_rejects_missing_freeze():
    with pytest.raises(FrozenPlanError):
        require_execution(ROOT, None)


@PUBLISHED
def test_published_freeze_receipt_input_hashes_and_counts():
    summary = read_json(ROOT / MANIFEST)
    plan = require_execution(ROOT, summary["frozen_analysis_plan_commit"])
    assert plan_hash(plan) == summary["plan_hash"]
    assert plan["word_lengths"] == [1, 2, 3, 4, 5, 6]
    assert len(plan["items"]) == summary["model_items"] == 23
    assert plan["pre_freeze_exposure"]["actual_A_C_target_word_analyses"] == 0
    for path, expected in {**summary["item_sha256"], **summary["table_sha256"]}.items():
        assert sha256_file(ROOT / path) == expected


@PUBLISHED
def test_published_words_complete_exact_controls_and_reassembly():
    summary = read_json(ROOT / MANIFEST)
    plan = require_execution(ROOT, summary["frozen_analysis_plan_commit"])
    envelopes = []
    for item in plan["items"]:
        envelope = load_envelope(ROOT, item, plan, summary["frozen_analysis_plan_commit"])
        result = envelope["result"]
        words = load_word_file(ROOT, envelope)
        for block in words["words"]:
            rows = block["rows"]
            assert sum(Fraction(row["P_H"]) for row in rows) == 1
            assert sum(Fraction(row["P_Kpi"]) for row in rows) == 1
            if block["word_length"] <= 2 or result["family"] == "B" or item["item_id"] == "J0-NEUTRAL":
                assert all(row["P_H"] == row["P_Kpi"] for row in rows)
        envelopes.append(envelope)
    assert len(complement_validation(ROOT, envelopes)) == 23


@PUBLISHED
def test_selected_published_target_rows_recomputed_independently():
    models = published_models(ROOT)
    for key in ("I0-SAME_ANY-m025", "I0-ADJ_FORM-m4", "I0-DISJ_DISSOLVE-m025", "I0-FORM_ANY-m4"):
        for chain in chains_for(models[key])[:2]:
            oracle, _ = hidden_path_words(chain, 3)
            path = ROOT / "constraint-lab/reports/items/generation-008j" / (key.replace("I0-", "J0-") + ".json")
            envelope = read_json(path)
            words = load_word_file(ROOT, envelope)
            for block in words["words"]:
                if block["projection"] != "graph_class" or block["word_length"] > 3:
                    continue
                column = "P_H" if len(chain.rows) == 28 else "P_Kpi"
                actual = {tuple(row["word"]): Fraction(row[column]) for row in block["rows"]}
                assert oracle[block["word_length"]] == actual


def test_8i_historical_artifacts_preserved():
    paths = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", BASE], cwd=ROOT, text=True).splitlines()
    immutable = ("constraint-lab/reports/", "constraint-lab/exploration/", "constraint-lab/provenance/prompts/",
                 "constraint-lab/provenance/executions/", "constraint-lab/provenance/reviews/",
                 "constraint-lab/coherence/snapshots/", "books/", "research-methods/")
    for path in paths:
        if path.startswith(immutable):
            historical = subprocess.check_output(["git", "show", BASE + ":" + path], cwd=ROOT)
            assert (ROOT / path).read_bytes() == historical, path
    for path in ("constraint-lab/coherence/findings.jsonl", "constraint-lab/coherence/relations.jsonl",
                 "constraint-lab/formal/theorem-catalog.jsonl", "constraint-lab/provenance/ledger.jsonl"):
        historical = subprocess.check_output(["git", "show", BASE + ":" + path], cwd=ROOT)
        assert (ROOT / path).read_bytes().startswith(historical)


@PUBLISHED
def test_full_384_state_invariant_triples_preserve_label_silence():
    from collections import defaultdict
    from rs_constraint_lab.graphs import pair_classes
    from rs_constraint_lab.history_roles import RoleController
    from rs_constraint_lab.role_atlas import fingerprint, serial_rows

    models = published_models(ROOT)
    table = pair_classes()
    for key in ("I0-SAME_ANY-m025", "I0-ADJ_FORM-m4", "I0-DISJ_FORM-m025"):
        record = models[key]
        rows = RoleController(record["feature"], record["m"]).kernel()
        assert fingerprint(serial_rows(rows)) == record["full_kernel_fingerprint"]
        labelled = defaultdict(lambda: [Fraction(0)] * 6)
        for source, row in enumerate(rows):
            for middle, first in row.items():
                for target, second in rows[middle].items():
                    word = (table.name_of[source // 6], table.name_of[middle // 6], table.name_of[target // 6])
                    labelled[word][middle % 6] += record["stationary_joint"][source] * first * second
        envelope = read_json(ROOT / "constraint-lab/reports/items/generation-008j" / (key.replace("I0-", "J0-") + ".json"))
        expected = {tuple(row["word"]): Fraction(row["P_H"]) for row in envelope["result"]["triples"]["graph_class"]}
        assert {word: sum(masses) for word, masses in labelled.items()} == expected
        assert all(masses == [sum(masses) / 6] * 6 for masses in labelled.values())


@PUBLISHED
def test_word_model_information_is_monotone_with_prefix_length():
    rows = read_json(ROOT / "constraint-lab/reports/tables/generation-008j-word-atlas.json")["rows"]
    for key in {row["controller_id"] for row in rows}:
        for projection in ("graph_class", "edge_count"):
            values = [Decimal(row["word_JS"]) for row in rows if row["controller_id"] == key and row["projection"] == projection]
            assert all(right + Decimal("1e-25") >= left for left, right in zip(values, values[1:]))


@pytest.mark.skipif(not (ROOT / "constraint-lab/coherence/snapshots/through-generation-008j.md").exists(), reason="8J snapshot checked after close-out")
def test_generation_008j_snapshot_and_ledger_prefixes(tmp_path):
    import hashlib
    from rs_constraint_lab.coherence import canonical_ledger_bytes, snapshot_text

    directory = ROOT / "constraint-lab/coherence"
    for name, count in (("findings.jsonl", 168), ("relations.jsonl", 260)):
        lines = (directory / name).read_bytes().splitlines(keepends=True)
        (tmp_path / name).write_bytes(b"".join(lines[:count]))
    assert hashlib.sha256(canonical_ledger_bytes(tmp_path)).hexdigest() == "c30ebe30b20199c1cbfa3bcc2fc291db976d19cbd25936e6beb1d7a081a8cde3"
    snapshot = directory / "snapshots/through-generation-008j.md"
    assert snapshot.read_text() == snapshot_text(tmp_path, title="Coherence map through Generation 8J")
    assert sha256_file(snapshot) == "79256157053a6410270907e49d25ba941ffd0c56efbc8a16202623c746729a4b"
