"""Proof fixtures and canonical-document contracts, not a scientific census."""

from __future__ import annotations

import copy
import hashlib
import itertools
import math
import subprocess
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from rs_constraint_lab.coherence import load_ledger
from rs_constraint_lab.constraints import (
    Choreography, Constraint, DISSOLVE, FORM, parse_expression, structurally_simple,
)
from rs_constraint_lab.explore08e import mobius, reconstruct
from rs_constraint_lab.explore08f import CLASS_OF_MASK, decomposition
from rs_constraint_lab.formal import (
    STATUSES, generated_views, load_catalog, render_catalog, render_dependencies,
    repository_root, validate_catalog,
)
from rs_constraint_lab.grammar import canonical_id_tuple
from rs_constraint_lab.kernel import build_kernel, kernel_fingerprint
from rs_constraint_lab.memory_clocks import _epoch_flux, _epoch_kernel_exact, _stationary_exact
from rs_constraint_lab.state import relation_slots

ROOT = repository_root()
BASE = "ec319f24faa66ca9898363ccd7531334e82544c1"
FORMAL_PUBLICATION = "22e252e560cc711d337b6ae506b0fb76728247d6"


def kernel(rules, factors, n=3, order=2):
    return build_kernel(
        n, Choreography(0, 0, tuple(rules)), factors,
        relation_slots=relation_slots(n, order),
    )


def exponent(value: Fraction) -> int:
    assert value > 0
    assert value.numerator.bit_count() == value.denominator.bit_count() == 1
    return value.numerator.bit_length() - value.denominator.bit_length()


def log_table(rules, factors):
    result = kernel(rules, factors)
    return {(a, b): exponent(result.weights[(a << 1) | (b << 2)][0]) for a, b in itertools.product((0, 1), repeat=2)}


def test_multiplication_addition_order_and_duplicate_occurrences():
    rules = (
        parse_expression("form(0-1) | present(0-2) => alpha", 3),
        parse_expression("form(0-1) | absent(1-2) => beta", 3),
    )
    factors = {"alpha": Fraction(4), "beta": Fraction(1, 2)}
    result = kernel(rules, factors)
    reversed_result = kernel(reversed(rules), factors)
    assert kernel_fingerprint(result) == kernel_fingerprint(reversed_result)
    for state in range(8):
        expected = sum(exponent(factors[r.weight]) for r in rules if r.matches(state, 0))
        assert exponent(result.weights[state][0]) == expected
    doubled = kernel((rules[0], rules[0]), factors)
    assert doubled.weights[2][0] == 16
    assert not structurally_simple((rules[0], rules[0]))
    images = ((0, 1, 2), (2, 1, 0))
    assert canonical_id_tuple((2, 0), images) == canonical_id_tuple((0, 2), images)


@pytest.mark.parametrize("m", [Fraction(1, 4), Fraction(4)])
def test_six_slot_law_and_complementary_full_kernel_elimination(m):
    rules = tuple(parse_expression(f"form(0-1) | {literal}(0-2) => alpha", 4) for literal in ("present", "absent"))
    combined = kernel(rules, {"alpha": m}, n=4)
    unconditional = kernel((parse_expression("form(0-1) => alpha", 4),), {"alpha": m}, n=4)
    assert kernel_fingerprint(combined) == kernel_fingerprint(unconditional)
    assert combined.probability(0, 1) == m / (m + 5)
    assert combined.probability(0, 2) == 1 / (m + 5)


def test_equal_directions_remove_action_bit_not_gate():
    rules = tuple(parse_expression(f"{direction}(0-1) | present(0-2) => alpha", 3) for direction in ("form", "dissolve"))
    result = kernel(rules, {"alpha": Fraction(4)})
    for state in range(8):
        assert result.weights[state][0] == (4 if state & 2 else 1)
        assert result.weights[state][0] == result.weights[state ^ 1][0]


def test_k2_affine_bound_and_count_scope_counterexample():
    rules = (
        parse_expression("form(0-1) => alpha", 3),
        parse_expression("form(0-1) | present(0-2) => beta", 3),
        parse_expression("form(0-1) | absent(1-2) => gamma", 3),
    )
    coefficients = mobius(log_table(rules, {"alpha": Fraction(2), "beta": Fraction(4), "gamma": Fraction(1, 2)}))
    assert coefficients == {"c": 0, "a": 2, "b": 1, "d": 0}
    count = parse_expression("form(0-1) | count>=1 => alpha", 3)
    assert count.k() == 2
    assert mobius(log_table((count,), {"alpha": Fraction(2)}))["d"] == -1
    with pytest.raises(ValueError):
        parse_expression("form(0-1) | count>=1 => alpha", 3, order=3)


@pytest.mark.parametrize("requirements", [(1, 1), (1, 0), (0, 1), (0, 0)])
@pytest.mark.parametrize("m", [Fraction(1, 4), Fraction(4)])
def test_k3_interaction_and_raw_polarity_sign(requirements, m):
    rule = Constraint(FORM, 0, ((1, requirements[0]), (2, requirements[1])), "alpha")
    table = log_table((rule,), {"alpha": m})
    coefficient = mobius(table)["d"]
    sign = (-1) ** requirements.count(0)
    assert coefficient == exponent(m) * sign
    assert abs(coefficient * math.log(2) - math.log(float(m)) * sign) <= 1e-15


def _mobius(values):
    width = len(values)
    assert width and width & (width - 1) == 0
    coefficients = list(values)
    for bit in range(width.bit_length() - 1):
        for mask in range(width):
            if mask & (1 << bit):
                coefficients[mask] -= coefficients[mask ^ (1 << bit)]
    return coefficients


def test_selected_three_literal_top_derivative_and_contradiction():
    required = (0, 1, 0)
    rule = Constraint(FORM, 0, tuple(zip((1, 2, 3), required)), "alpha")
    result = kernel((rule,), {"alpha": Fraction(4)}, order=3)
    values = [exponent(result.weights[mask << 1][0]) for mask in range(8)]
    assert rule.k() == 4
    assert _mobius(values)[7] == 2 * (-1) ** required.count(0)
    contradictory = parse_expression("form(0-1) | present(0-1-2) & absent(0-1-2) => alpha", 3, order=3)
    assert all(not contradictory.matches(state, 0) for state in range(16))


def test_mobius_and_corner_reconstruction_exact():
    values = [Fraction(3, 7), Fraction(-4, 5), Fraction(11), Fraction(9, 2), Fraction(-8), Fraction(1, 3), Fraction(2), Fraction(17, 6)]
    coefficients = _mobius(values)
    for corner in range(8):
        rebuilt = sum(coefficient for mask, coefficient in enumerate(coefficients) if mask & corner == mask)
        assert rebuilt == values[corner]
        corner_rebuilt = sum(values[u] * int(u == corner) for u in range(8))
        assert corner_rebuilt == values[corner]
    two_gate = {(0, 0): Fraction(3), (1, 0): Fraction(4), (0, 1): Fraction(-1), (1, 1): Fraction(8)}
    assert reconstruct(mobius(two_gate)) == two_gate


def test_current_state_constructor_uses_actual_parser_without_action_conditions():
    slots = relation_slots(3, 3)
    rules, factors, desired = [], {}, {}
    for state in range(16):
        for action, relation in enumerate(slots):
            label = "factor_" + chr(97 + state) + chr(97 + action)
            desired[state, action] = Fraction(state + action + 1, state + 2)
            factors[label] = desired[state, action]
            direction = "dissolve" if state & (1 << action) else "form"
            conditions = []
            for other, gate in enumerate(slots):
                if other == action:
                    continue
                literal = "present" if state & (1 << other) else "absent"
                conditions.append(f"{literal}({'-'.join(map(str, gate))})")
            expression = f"{direction}({'-'.join(map(str, relation))}) | " + " & ".join(conditions) + f" => {label}"
            rules.append(parse_expression(expression, 3, order=3))
    assert len(rules) == 4 * 16
    assert structurally_simple(rules)
    assert max(rule.k() for rule in rules) == 4
    result = kernel(rules, factors, order=3)
    for state in range(16):
        assert result.weights[state] == tuple(desired[state, action] for action in range(4))


def test_projection_residual_zero_lower_order_moments_exact():
    c = Fraction(2)
    residual = {}
    for g1, g2 in itertools.product((0, 1), repeat=2):
        projected = -c / 4 + c / 2 * (g1 + g2)
        residual[g1, g2] = c * g1 * g2 - projected
    assert sum(residual.values()) == 0
    for index in (0, 1):
        assert sum(value * (corner[index] - Fraction(1, 2)) for corner, value in residual.items()) == 0


def test_nested_projection_chain_on_fixed_synthetic_distributions():
    left = np.arange(1, 65, dtype=float)
    right = left[::-1] ** 2
    result = decomposition(left / left.sum(), right / right.sum())
    assert abs(result["pairmask_chain_gap"]) <= 1e-12
    assert abs(result["class_chain_gap"]) <= 1e-12
    assert result["I_model_shape_given_edgecount"] >= -1e-12
    assert result["I_model_label_given_class"] >= -1e-12


def test_exact_stationary_factorisation_epoch_arrival_and_period_fixture():
    rule = parse_expression("form(0-1) | present(0-1-2) => alpha", 3, order=3)
    result = kernel((rule,), {"alpha": Fraction(7, 3)}, order=3)
    full_stationary = _stationary_exact(result)
    epoch, defect = _epoch_kernel_exact(result)
    arrival = _epoch_flux(result, full_stationary)
    assert defect == 0
    assert sum(full_stationary) == sum(arrival) == 1
    for state in range(16):
        assert full_stationary[state] == full_stationary[state ^ 2] == full_stationary[state ^ 4]
        assert arrival[state] == arrival[state ^ 2] == arrival[state ^ 4]
        assert arrival[state] == sum(arrival[source] * epoch[source].get(state, 0) for source in range(16))
        assert sum(epoch[state].values()) == 1
        for target, probability in epoch[state].items():
            assert probability > 0
            assert (state & 7).bit_count() % 2 != (target & 7).bit_count() % 2
        assert any(epoch[state].get(target, 0) * epoch[target].get(state, 0) > 0 for target in range(16))


def test_other_pair_dependency_counterexample_balance_symbolically():
    sigma = [Fraction(n, 14) for n in (3, 4, 2, 5)]
    # Core indices are (b,z)=(0,0),(1,0),(0,1),(1,1).
    transitions = ({1: 1, 2: 1}, {0: 1, 3: 1}, {3: 3, 0: 1}, {2: 1, 1: 1})
    for state in range(4):
        incoming = sum(sigma[source] * transitions[source].get(state, 0) for source in range(4))
        assert incoming == sigma[state] * sum(transitions[state].values())
    total = [Fraction(n, 144) for n in (30, 40, 24, 50)]
    assert total == [sigma[i] * (12 if i == 2 else 10) / Fraction(72, 7) for i in range(4)]
    arrival = [sum(sigma[source] * transitions[source].get(i, 0) for source in range(4)) + 4 * sigma[i] for i in range(4)]
    arrival = [v / sum(arrival) for v in arrival]
    assert arrival == [Fraction(n, 88) for n in (18, 24, 16, 30)]
    assert arrival[0] + arrival[1] == Fraction(21, 44)
    assert arrival[2] + arrival[3] == Fraction(23, 44)


def test_shape_given_edge_corollary_and_hidden_polarity_conjugacy():
    for class_id in range(11):
        masks = [mask for mask in range(64) if CLASS_OF_MASK[mask] == class_id]
        k = masks[0].bit_count()
        assert all(mask.bit_count() == k for mask in masks)
        for action in range(6):
            assert sum(bool(mask & (1 << action)) for mask in masks) * 6 == k * len(masks)
    left = np.array([Fraction(3, 4) / 32 if mask & 1 else Fraction(1, 4) / 32 for mask in range(64)], dtype=float)
    right = np.array([Fraction(1, 3) / 32 if mask & 1 else Fraction(2, 3) / 32 for mask in range(64)], dtype=float)
    assert abs(decomposition(left, right)["I_model_shape_given_edgecount"]) <= 1e-12
    rules = [parse_expression(f"form(0-1) | {literal}(0-1-2) => alpha", 3, order=3) for literal in ("present", "absent")]
    kernels = [kernel((rule,), {"alpha": Fraction(3)}, order=3) for rule in rules]
    for state in range(16):
        for target, probability in kernels[0].successors[state]:
            assert kernels[1].probability(state ^ 8, target ^ 8) == probability


def test_selected_representation_constructions_without_search():
    factors = {"alpha": Fraction(4), "beta": Fraction(2)}
    and_rule = Constraint(FORM, 0, ((1, 1), (2, 1)), "alpha")
    assert log_table((and_rule,), factors) == {(0, 0): 0, (1, 0): 0, (0, 1): 0, (1, 1): 2}
    for corners in (((0, 1), (1, 0)), ((0, 0), (1, 1))):
        rules = [Constraint(FORM, 0, tuple(zip((1, 2), corner)), "alpha") for corner in corners]
        values = log_table(rules, factors)
        assert all(values[corner] == (2 if corner in corners else 0) for corner in values)
        assert mobius(values)["d"] != 0
    simple = (Constraint(FORM, 0, (), "alpha"), Constraint(FORM, 0, ((1, 0),), "beta"), Constraint(FORM, 0, ((1, 1),), "beta"))
    stacked = (Constraint(FORM, 0, (), "alpha"), Constraint(FORM, 0, (), "beta"))
    assert structurally_simple(simple) and not structurally_simple(stacked)
    assert set(log_table(simple, factors).values()) == set(log_table(stacked, factors).values()) == {3}


def test_catalog_schema_generated_views_and_namespaces():
    rows = load_catalog()
    assert validate_catalog(rows) == []
    assert {r["status"] for r in rows} <= STATUSES
    assert len([r for r in rows if r["status"] == "ALGEBRAIC_THEOREM"]) == 25
    assert all(r["theorem_id"].startswith("CL-") for r in rows)
    for path, expected in generated_views().items():
        assert path.read_text(encoding="utf-8") == expected
    assert render_catalog(rows) == render_catalog(copy.deepcopy(rows))
    assert render_dependencies(rows) == render_dependencies(copy.deepcopy(rows))


@pytest.mark.parametrize("mutation,match", [
    (lambda r: r.update(status="PROVED_EVERYTHING"), "invalid status"),
    (lambda r: r.update(assumptions=[]), "assumptions"),
    (lambda r: r.update(dependencies=["CL-MISSING"]), "unknown dependency"),
    (lambda r: r.update(evidence_refs=["../outside.md"]), "missing evidence"),
    (lambda r: r.update(evidence_refs=None), "must be a string list"),
    (lambda r: r.update(dependencies=None), "must be a string list"),
    (lambda r: r.update(coherence_refs=["MISSING"]), "unknown coherence"),
    (lambda r: r.update(overall_score=1), "scalar score"),
    (lambda r: r["proof_or_verification"].update(proof_sketch=""), "needs assumptions and proof"),
    (lambda r: r.update(dependencies=["CL-T01"]), "dependency cycle"),
])
def test_catalog_rejects_invalid_contracts(mutation, match):
    rows = copy.deepcopy(load_catalog())
    mutation(rows[0])
    assert any(match in message for message in validate_catalog(rows))


def test_numerical_finite_and_open_obligations():
    rows = copy.deepcopy(load_catalog())
    next(r for r in rows if r["status"] == "NUMERICAL_KERNEL_RESULT")["proof_or_verification"]["tolerances"] = {}
    next(r for r in rows if r["status"] == "FINITE_EXHAUSTIVE_RESULT")["proof_or_verification"]["exact_count"] = None
    next(r for r in rows if r["status"] == "OPEN_QUESTION")["proof_or_verification"]["proved"] = True
    messages = validate_catalog(rows)
    assert any("numerical result" in m for m in messages)
    assert any("positive exact count" in m for m in messages)
    assert any("masquerades" in m for m in messages)
    assert any("not unique" in m for m in validate_catalog(load_catalog() + [load_catalog()[0]]))


def _git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, check=True).stdout


def test_historical_artifacts_and_ledger_prefixes_preserved():
    old_paths = set(_git("ls-tree", "-r", "--name-only", BASE).decode().splitlines())
    changed = set(_git("diff", "--name-only", BASE, "--", "constraint-lab/reports", "constraint-lab/exploration", "constraint-lab/provenance", "constraint-lab/coherence/snapshots").decode().splitlines())
    allowed = {"constraint-lab/provenance/ledger.jsonl"}
    assert (old_paths & changed) <= allowed
    # The formal increment preserved books. Later book publications on main
    # are independent work, so audit that historical claim at its publication.
    assert _git("diff", "--name-only", BASE, FORMAL_PUBLICATION, "--", "books") == b""
    for path in ("constraint-lab/coherence/findings.jsonl", "constraint-lab/coherence/relations.jsonl", "constraint-lab/provenance/ledger.jsonl"):
        assert (ROOT / path).read_bytes().startswith(_git("show", f"{BASE}:{path}"))
    findings, _relations = load_ledger()
    general = next(row for row in findings if row["finding_id"] == "F8E-GENERAL-K-INTERACTION")
    assert general["status"] == "qualified"
    assert any(row["finding_id"] == "F8F-GENERAL-K-SCOPE" for row in findings)
    assert any(row["finding_id"] == "F8F-PREFREEZE-SCIENCE-GATE" for row in findings)


def test_prompt_representation_is_not_authored_hash():
    path = ROOT / "constraint-lab/provenance/prompts/008G-v0.8g-agent-input.md"
    contents = path.read_bytes()
    assert len(contents) == 45632
    assert hashlib.sha256(contents).hexdigest() == "81703b51e2d869da5fda862d9528c854846cdf8b037f54aac6ad400a7f1e704e"
    assert b"81703b51e2d869da5fda862d9528c854846cdf8b037f54aac6ad400a7f1e704e" not in contents
    assert not (ROOT / "constraint-lab/exploration/generation-008g/round-g0-plan.json").exists()

def test_formal_coherence_join_cites_committed_derivations():
    findings, relations = load_ledger()
    catalogue = {row["theorem_id"]: row for row in load_catalog()}
    new = [row for row in findings if row["created_generation"] == "008G"]
    assert len(new) == 13
    for row in new:
        assert row["formal_refs"]
        for reference in row["formal_refs"]:
            assert row["finding_id"] in catalogue[reference]["coherence_refs"]
        for path in row["evidence_refs"]:
            assert (ROOT / path).exists()
            _git("cat-file", "-e", "HEAD:" + path)
        assert "overall_score" not in row
    assert any(row["from_finding"] == "F8G-FORMAL-COUNT-SCOPE" and row["relation_type"] == "qualifies" for row in relations)
    assert any(row["from_finding"] == "F8G-FORMAL-SHAPE-INVARIANCE" and row["to_finding"] == "Q-SCALE-N" and row["relation_type"] == "bounds" for row in relations)
    assert all(next(f for f in findings if f["finding_id"] == question)["status"] == "unresolved" for question in ("Q-H-POSITIVE", "Q-META-CONSTRAINT", "Q-SCALE-N"))


def test_8g_snapshot_from_immutable_ledger_prefix(tmp_path):
    from rs_constraint_lab.coherence import canonical_ledger_bytes, snapshot_text

    directory = ROOT / "constraint-lab/coherence"
    for name, count in (("findings.jsonl", 105), ("relations.jsonl", 149)):
        prefix = b"".join((directory / name).read_bytes().splitlines(keepends=True)[:count])
        (tmp_path / name).write_bytes(prefix)
    expected = snapshot_text(tmp_path, title="Through Generation 008G")
    assert snapshot_text(tmp_path, title="Through Generation 008G") == expected
    assert (directory / "snapshots/through-generation-008g.md").read_text() == expected
    assert hashlib.sha256(expected.encode()).hexdigest() == "0ef6f87567e45a006eb14b80dde4cb98e6542fa8ae30097b587f2ecb90111e4c"
    assert hashlib.sha256(canonical_ledger_bytes(tmp_path)).hexdigest() == "c3fb60db0d338d83069e52015a0a5d78d972ec6775ad8fc08c29dd11fadec0e3"
