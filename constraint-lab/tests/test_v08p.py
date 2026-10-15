"""Proof-first consolidation: no new actual scientific parameter cells."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import subprocess

import pytest
pytest.importorskip("flint")
from flint import fmpq as Q, fmpq_mat as Mat

from rs_constraint_lab.gen008p_proofs import TABLE, proof_checks, polynomial_flux, selector_identities
from rs_constraint_lab.h2_roles import ready
from rs_constraint_lab.stopping_factorization import eye, is_zero
from rs_constraint_lab.stopping_sufficiency import all_length_certificate, realization, stationary, synthetic_examples

ROOT = Path(__file__).resolve().parents[2]
BASE = "99565d14e9c0fc172d925fd335965e127d950868"


@pytest.fixture(scope="module")
def examples():
    return synthetic_examples()


@pytest.mark.parametrize("name", ("eventual_not_all_lengths", "aggregation_erases_target", "all_lengths_not_all_paths", "parity_not_timing_equality"))
def test_stationary_fixture_original_chain_and_exact_adjacent_law(name, examples):
    t, v = examples[name]
    pi, c, l, k = Mat([v["pi"]]), v["C"], v["L"], v["Kpi"]
    assert pi*t == pi and l*c == eye(c.ncols())
    coarse = pi*c
    assert coarse*k == coarse
    for s in range(c.ncols()):
        for target in range(c.ncols()):
            flow = sum(pi[0,z]*t[z,w]*c[z,s]*c[w,target] for z in range(t.nrows()) for w in range(t.nrows()))
            assert flow == coarse[0,s]*k[s,target]


def test_eventual_equality_does_not_imply_all_lengths_or_no_propagated_defect(examples):
    _, v = examples["eventual_not_all_lengths"]
    assert v["a"]*v["P"] == v["a"]
    assert v["U"] == Mat([[-Q(4,49), Q(4,49)]])
    assert is_zero(v["eventual_delta"])
    assert v["certificate"]["first_differing_j"] == 1
    assert not v["certificate"]["all_lengths_equal"]


def test_destination_aggregation_erases_nonzero_vector(examples):
    _, v = examples["aggregation_erases_target"]
    assert v["eventual_delta"] == Mat([[Q(2,45), -Q(2,45)]])
    assert is_zero(v["eventual_delta"]*Mat([[1],[1]]))
    # a is the post-first-step source from the singleton A0 state.
    t, _ = examples["aggregation_erases_target"]
    assert v["a"].tolist()[0] == t.tolist()[0][2:]


def test_all_return_lengths_do_not_imply_strong_lumpability_or_path_equality(examples):
    t,v = examples["all_lengths_not_all_paths"]
    assert v["certificate"]["all_lengths_equal"]
    assert (t*v["C"])[1,2] != (t*v["C"])[2,2]
    pi, c, k = Mat([v["pi"]]), v["C"], v["Kpi"]
    fine, coarse = pi, pi*c
    for i, observed in enumerate((0,1,2)):
        if i:
            fine, coarse = fine*t, coarse*k
        fine = Mat([[fine[0,z] if c[z,observed] else 0 for z in range(t.nrows())]])
        coarse = Mat([[coarse[0,s] if s == observed else 0 for s in range(k.nrows())]])
    assert sum(fine.tolist()[0])-sum(coarse.tolist()[0]) == Q(3,11680)


def test_parity_does_not_force_even_timing_equality(examples):
    _,v = examples["parity_not_timing_equality"]
    a,q,p,r = (v[k] for k in ("a","Q","P","R"))
    assert a*p == a
    for j in (1,3,5):
        assert is_zero(a*q**j*r) and is_zero(a*p*(q*p)**j*r)
    assert a*(q**2-p*(q*p)**2)*r == Mat([[-Q(3,200)]])


@pytest.mark.parametrize("name", ("eventual_not_all_lengths", "aggregation_erases_target", "all_lengths_not_all_paths", "parity_not_timing_equality"))
def test_block_realization_dual_and_noncommuting_order(name, examples):
    _,v = examples[name]
    a,q,p,r = (v[k] for k in ("a","Q","P","R"))
    h,e,f = realization(q,p,a,r)
    for j in range(9):
        assert e*h**j*f == a*(q**j-p*(q*p)**j)*r
        assert (f.transpose()*(h.transpose()**j)*e.transpose()).transpose() == e*h**j*f
    if name == "eventual_not_all_lengths":
        assert q*p != p*q


def test_source_spans_and_target_aggregation_are_declared_separately(examples):
    _,v = examples["aggregation_erases_target"]
    q,p,r,a = (v[k] for k in ("Q","P","R","a"))
    m = Mat(a.tolist()+(-a).tolist())
    assert not all_length_certificate(q,p,m,r)["all_lengths_equal"]
    # Signed test rows are not asserted to be physical probability starts.
    assert m[1,0] < 0
    zero = Mat([[0,0]])
    assert all_length_certificate(q,p,zero,r)["all_lengths_equal"]


def test_invalid_types_and_nonstochastic_synthetic_input_rejected():
    with pytest.raises(ValueError):
        stationary(Mat([[1,1],[0,1]]))
    with pytest.raises(ValueError):
        realization(eye(17),eye(17),Mat([[0]*17]),Mat([[1]]*17))
    with pytest.raises(ValueError):
        realization(eye(2),Mat([[1,1],[0,1]]),Mat([[1,0]]),Mat([[1],[1]]))


def test_symbolic_positive_domain_and_original_state_selector_identities():
    assert set(polynomial_flux()) == {"1","4"}
    assert selector_identities()["candidate_checks"] == 13824


def test_readonly_old_certificate_followup_and_generated_proof_output():
    actual = ready(proof_checks(ROOT))
    assert json.loads((ROOT/TABLE).read_text()) == actual
    rows = actual["published_followup"]["family_followup"]
    assert len(rows) == 200
    assert Counter(r["proof_family"] for r in rows) == {
        "ALL_POSITIVE_M_REGENERATION":48,"ALL_POSITIVE_M_EXIT_RATIO":32,
        "ALL_POSITIVE_M_TWO_LEVEL_FLUX_CENTERING":24,"PREVIOUS_CL_T95_ALL_POSITIVE_M":96}
    assert len(actual["published_followup"]["timing_twenty_finite_only"]) == 20
    assert actual["new_actual_scientific_cells"] == 0


def test_parent_prompt_and_plan_are_pinned_without_manufactured_review():
    prompt = ROOT/"constraint-lab/provenance/prompts/008P-v0.8p-agent-input.md"
    assert prompt.stat().st_size == 34016
    assert sha256(prompt.read_bytes()).hexdigest() == "5d9888ce73f1f7766553260219759f4ec01bba4588a986326687584de449413b"
    assert not (ROOT/"constraint-lab/provenance/reviews/008O-chatgpt-review-v0.8o.md").exists()
    planpath="constraint-lab/exploration/generation-008p/round-p0-formal-plan.json"
    original=subprocess.check_output(["git","show","3991f8c2ba4310d92df077ea9b730178ad7e996b:"+planpath],cwd=ROOT)
    assert original == (ROOT/planpath).read_bytes()


def test_preserve_parent_evidence_and_no_hub_science_import():
    changed = subprocess.check_output(["git","diff","--name-only",BASE],cwd=ROOT,text=True).splitlines()
    old = subprocess.check_output(["git","ls-tree","-r","--name-only",BASE],cwd=ROOT,text=True).splitlines()
    protected = {p for p in old if p.startswith(("books/","constraint-lab/reports/","constraint-lab/exploration/",
        "constraint-lab/coherence/snapshots/","constraint-lab/provenance/prompts/"))}
    assert not protected.intersection(changed)
    assert not subprocess.check_output(["git","ls-files","research-synthesis/"],cwd=ROOT)
