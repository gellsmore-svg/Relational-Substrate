"""Acceptance tests for the federated coherence layer (stdlib unittest; no research suite is run).

Mutation tests run on a temporary copy of research-synthesis/; the real tree
is never modified. Tests needing git objects skip when the pinned commits are
unreachable (e.g. a shallow clone).
"""

from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from rssynth import core, discover, generate, ledger, pins, sources, workflow  # noqa: E402

REAL_ROOT = core.ROOT


@contextmanager
def sandbox():
    """A temporary copy of research-synthesis/ with core.ROOT redirected to it."""
    tmp = Path(tempfile.mkdtemp(prefix="rssynth-test-"))
    dest = tmp / "research-synthesis"
    shutil.copytree(REAL_ROOT, dest, ignore=shutil.ignore_patterns("__pycache__"))
    core.ROOT = dest
    try:
        yield dest
    finally:
        core.ROOT = REAL_ROOT
        shutil.rmtree(tmp)


def inputs():
    m = sources.load_manifest()
    loaded = sources.load_sources(m)
    shared = ledger.load_shared()
    return m, loaded, shared


def git_pins_available() -> bool:
    m = sources.load_manifest()
    return sources.git_available() and all(sources.commit_reachable(s["commit"]) for s in m["sources"] if s.get("commit"))


class SourceLockAndHashes(unittest.TestCase):
    def test_real_tree_passes_full_check_without_git(self):
        rep = workflow.check(use_git=False, scope_base=None)
        self.assertTrue(rep["ok"], rep["errors"])

    def test_materialised_copies_match_recorded_digests_and_git_blob_ids(self):
        m = sources.load_manifest()
        for s in m["sources"]:
            for a in s.get("artifacts", []):
                if a.get("materialised"):
                    data = sources.materialised_path(s, a).read_bytes()
                    self.assertEqual(core.sha256_bytes(data), a["sha256"])
                    self.assertEqual(core.git_blob_id(data), a["git_blob"])

    @unittest.skipUnless(git_pins_available(), "pinned commits not reachable")
    def test_copies_equal_git_objects_at_the_pins(self):
        recs = sources.verify_artifacts(sources.load_manifest())
        self.assertTrue(all(r["pin"] == "ok" for r in recs), [r for r in recs if r["pin"] != "ok"])

    def test_tampered_copy_is_detected(self):
        with sandbox() as root:
            f = root / "sources/materialised/GT/gravity-time/coherence/findings.jsonl"
            f.write_text(f.read_text().replace("GT-F01-DENS-NULL", "GT-F01-DENS-NULX", 1))
            rep = workflow.check(use_git=False, scope_base=None)
            self.assertFalse(rep["ok"])
            self.assertTrue(any("TAMPERED" in e for e in rep["errors"]))

    def test_manifest_digest_edit_is_detected(self):
        with sandbox() as root:
            m = core.read_json(root / "sources/manifest.json")
            m["sources"][0]["artifacts"][0]["sha256"] = "0" * 64
            core.write_json(root / "sources/manifest.json", m)
            rep = workflow.check(use_git=False, scope_base=None)
            self.assertTrue(any("TAMPERED" in e for e in rep["errors"]))


class NamespacesAndCommits(unittest.TestCase):
    def test_two_default_revisions_in_one_namespace_collide(self):
        m = copy.deepcopy(sources.load_manifest())
        clone = copy.deepcopy(m["sources"][0])
        clone["source_key"] = "CL-DUP"
        m["sources"].append(clone)
        self.assertTrue(any("namespace collision" in p for p in sources.validate_manifest(m)))

    def test_abbreviated_or_missing_commit_rejected(self):
        m = copy.deepcopy(sources.load_manifest())
        m["sources"][1]["commit"] = m["sources"][1]["commit"][:7]
        self.assertTrue(any("abbreviated" in p for p in sources.validate_manifest(m)))

    def test_reserved_shared_namespace_cannot_be_a_source(self):
        m = copy.deepcopy(sources.load_manifest())
        m["sources"][1]["namespace"] = "X"
        self.assertTrue(any("reserved" in p for p in sources.validate_manifest(m)))

    def test_same_local_id_in_two_namespaces_stays_distinct(self):
        m, loaded, shared = inputs()
        R = ledger.Resolver(m, loaded["nodes"], shared)
        self.assertTrue(R.resolve("CL::F001-PAIRWISE-RISE")["ok"])
        self.assertFalse(R.resolve("GT::F001-PAIRWISE-RISE")["ok"])

    def test_dangling_reference_in_a_connection_fails(self):
        m, loaded, shared = inputs()
        bad = copy.deepcopy(shared)
        bad["connections"][0]["to"] = "GT::GT-F999-DOES-NOT-EXIST"
        self.assertTrue(any("not found in pinned source" in p for p in ledger.validate_all(m, loaded, bad)))

    def test_malformed_reference_fails(self):
        m, loaded, shared = inputs()
        bad = copy.deepcopy(shared)
        bad["connections"][0]["from"] = "cl:F001"
        self.assertTrue(any("malformed" in p for p in ledger.validate_all(m, loaded, bad)))


class ForbiddenImplications(unittest.TestCase):
    def setUp(self):
        self.m, self.loaded, self.shared = inputs()

    def errs(self, shared):
        return ledger.validate_all(self.m, self.loaded, shared)

    def test_metaphor_cannot_be_cited_as_evidence(self):
        bad = copy.deepcopy(self.shared)
        bad["connections"][0]["evidence_refs"].append("M::two-towns")
        self.assertTrue(any("metaphor cannot be cited as evidence" in p for p in self.errs(bad)))

    def test_metaphor_cannot_be_a_connection_endpoint(self):
        bad = copy.deepcopy(self.shared)
        bad["connections"][0]["to"] = "M::two-towns"
        self.assertTrue(any("metaphor cannot be an endpoint" in p for p in self.errs(bad)))

    def test_metaphor_link_types_and_connection_types_are_disjoint(self):
        self.assertFalse(core.METAPHOR_LINK_TYPES & core.CONNECTION_TYPES)
        bad = copy.deepcopy(self.shared)
        bad["metaphor_links"][0]["link_type"] = "tested_structural_analogy"
        self.assertTrue(any("scientific connection types are not allowed here" in p for p in self.errs(bad)))
        bad2 = copy.deepcopy(self.shared)
        bad2["connections"][0]["connection_type"] = "covers_concept"
        self.assertTrue(any("it is a metaphor link type" in p for p in self.errs(bad2)))

    def test_metaphor_link_cannot_carry_evidence_fields(self):
        bad = copy.deepcopy(self.shared)
        bad["metaphor_links"][0]["supports"] = "GT::GT-F78-LIFETIME-NOT-SET-BY-STATIONARY-LAW"
        self.assertTrue(any("belongs to the scientific graph" in p for p in self.errs(bad)))

    def test_metaphors_must_be_non_evidentiary(self):
        bad = copy.deepcopy(self.shared)
        bad["metaphors"][0]["evidentiary"] = True
        self.assertTrue(any("non-evidentiary" in p for p in self.errs(bad)))

    def test_scalar_scores_are_refused(self):
        for group, idx in (("connections", 0), ("metaphors", 0)):
            bad = copy.deepcopy(self.shared)
            bad[group][idx]["confidence"] = 0.93
            self.assertTrue(any("scalar score" in p for p in self.errs(bad)), group)
        bad = copy.deepcopy(self.shared)
        bad["connections"][0]["cosine"] = 0.19
        self.assertTrue(any("scalar score" in p for p in self.errs(bad)))

    def test_discovery_output_cannot_be_cited(self):
        bad = copy.deepcopy(self.shared)
        bad["connections"][0]["evidence_refs"].append("proposals/discovery-diagnostics.json")
        self.assertTrue(any("discovery output cannot be cited" in p for p in self.errs(bad)))

    def test_smuggled_metric_or_agency_needs_a_disclaimer(self):
        bad = copy.deepcopy(self.shared)
        m = bad["metaphors"][0]
        m["explanation"] += " The cafés are pulled toward the centre by a force."
        problems = self.errs(bad)
        self.assertTrue(any("'force'" in p for p in problems) and any("'pull'" in p for p in problems))

    def test_metaphors_never_change_a_nodes_status(self):
        base = ledger.project_graph(self.m, self.loaded, self.shared)
        more = copy.deepcopy(self.shared)
        more["metaphors"].append(dict(more["metaphors"][0], metaphor_id="M::extra", illustrative_status="very convincing"))
        more["metaphor_links"].append({"link_id": "ML::999", "link_type": "requires_qualification", "from": "M::extra", "to": "GT::GT-F78-LIFETIME-NOT-SET-BY-STATIONARY-LAW", "note": "x"})
        after = ledger.project_graph(self.m, self.loaded, more)
        status = lambda g: {n["id"]: (n.get("status"), n.get("epistemic_layer")) for n in g["nodes"] if not n["id"].startswith("M::")}
        self.assertEqual(status(base), status(after))
        self.assertEqual(base["scientific_edges"], after["scientific_edges"])

    def test_discovery_never_writes_the_ledger_or_raises_status(self):
        with sandbox() as root:
            before = {p: core.sha256_file(p) for p in (root / "ledger").glob("*.jsonl")}
            g0 = ledger.project_graph(*inputs())
            m, loaded, shared = inputs()
            out = discover.discover(loaded["nodes"], shared, m)
            core.write_json(discover.diagnostics_path(), out)
            self.assertEqual(before, {p: core.sha256_file(p) for p in (root / "ledger").glob("*.jsonl")})
            self.assertEqual(g0, ledger.project_graph(*inputs()))
            self.assertEqual(out["score_kind"], "retrieval_similarity")
            self.assertTrue(all(c["status"] == "unreviewed_retrieval_candidate" for c in out["candidates"]))


class DiscoveryBehaviour(unittest.TestCase):
    def synthetic(self):
        nodes = {}
        for i in range(6):
            nodes[f"CL::A{i}"] = {"kind": "source_finding", "source": "CL", "statement": "frozen checks items controls verification exact pass"}
        nodes["CL::B"] = {"kind": "source_finding", "source": "CL", "statement": "history register restores markov sufficiency of the projected pair process"}
        nodes["GT::C"] = {"kind": "source_finding", "source": "GT", "statement": "frozen checks items controls hold for every cell"}
        nodes["GT::D"] = {"kind": "source_finding", "source": "GT", "statement": "episode lifetime differs at matched stationary occupancy"}
        nodes["GT::E"] = {"kind": "source_finding", "source": "GT", "statement": "frozen checks items controls numerical qualification"}
        return nodes

    def test_boilerplate_false_positive_ranks_high_and_is_not_promoted(self):
        out = discover.discover(self.synthetic(), {"connections": [], "proposals": []}, {}, limit=10)
        top = out["candidates"][0]
        self.assertIn("frozen", top["shared_terms"])  # a lexical false positive ranks first
        self.assertEqual(top["status"], "unreviewed_retrieval_candidate")

    def test_near_duplicates_and_single_nodes_cannot_dominate(self):
        out = discover.discover(self.synthetic(), {"connections": [], "proposals": []}, {}, limit=50)
        from collections import Counter

        per_node = Counter(x for c in out["candidates"] for x in (c["from"], c["to"]))
        self.assertLessEqual(max(per_node.values()), discover.TOP_PER_NODE)
        cluster_pairs = Counter(("A" if c["from"].startswith("CL::A") else c["from"], c["to"]) for c in out["candidates"])
        self.assertLessEqual(max(cluster_pairs.values()), discover.MAX_PER_CLUSTER)

    def test_reviewed_links_can_have_zero_similarity(self):
        m, loaded, shared = inputs()
        cal = discover.discover(loaded["nodes"], shared, m)["reviewed_connection_calibration"]
        self.assertTrue(any(c["similarity"] == 0.0 for c in cal))  # absence of similarity is not absence of structure


class AncestryStalenessAndRevisions(unittest.TestCase):
    def setUp(self):
        self.m, self.loaded, self.shared = inputs()

    def test_shared_lineage_requires_independence_note(self):
        self.assertTrue(ledger.lineage_shared(self.m, "CL", "GT"))
        self.assertFalse(ledger.lineage_shared(self.m, "CL", "SC"))
        bad = copy.deepcopy(self.shared)
        x = bad["connections"][0]
        x["independence"] = "independent"
        x.pop("independence_note", None)
        self.assertTrue(any("share lineage" in p for p in ledger.validate_all(self.m, self.loaded, bad)))

    def test_shared_implementation_assumption_cannot_be_independent(self):
        bad = copy.deepcopy(self.shared)
        x = [c for c in bad["connections"] if c["connection_type"] == "shared_implementation_assumption"][0]
        x["independence"] = "independent"
        x["independence_note"] = "claimed"
        self.assertTrue(any("by definition not independent" in p for p in ledger.validate_all(self.m, self.loaded, bad)))

    def test_lineage_only_revision_is_not_ingested(self):
        R = ledger.Resolver(self.m, self.loaded["nodes"], self.shared)
        r = R.resolve("CL@008g::F001-PAIRWISE-RISE")
        self.assertFalse(r["ok"])
        self.assertIn("lineage-only", r["reason"])

    def test_inherited_cl_copy_on_gt_branch_is_not_counted(self):
        gt = [k for k, v in self.loaded["nodes"].items() if v["source"] == "GT"]
        self.assertTrue(all(k.startswith("GT::GT-") for k in gt))

    def test_stale_branch_is_reported_not_followed(self):
        orig = sources.remote_branch_head
        try:
            sources.remote_branch_head = lambda b: "f" * 40
            states = {s["source"]: s["state"] for s in sources.staleness(self.m)}
            self.assertIn(states["GT"], ("behind_branch_head", "diverged_from_branch"))
        finally:
            sources.remote_branch_head = orig

    @unittest.skipUnless(git_pins_available() and sources.commit_reachable("9b2f857"), "older CL commit not reachable")
    def test_propose_pin_flags_parallel_or_older_revision_and_rewrites(self):
        with sandbox():
            rep = pins.propose_pin(sources.load_manifest(), "CL", sources._git("rev-parse", "9b2f857"))
            self.assertFalse(rep["descends_from_current"])
            self.assertTrue(rep["warnings"])
            self.assertTrue(any(a.get("removed") for a in rep["artifacts"]))  # 8N rows absent at 8M

    def test_apply_pin_needs_a_named_human(self):
        with sandbox():
            with self.assertRaises(sources.SourceError):
                pins.apply_pin("GT", "0" * 40, reviewed_by="agent: me")

    def test_incompatible_upstream_schema_stops(self):
        src = copy.deepcopy([s for s in self.m["sources"] if s["source_key"] == "GT"][0])
        with sandbox() as root:
            v = root / "sources/materialised/GT/constraint-lab/src/rs_constraint_lab/coherence.py"
            v.write_text("# vocabulary removed\n")
            with self.assertRaises(sources.SourceError):
                sources.adapt_coherence_ledger(src)

    def test_undeclared_upstream_field_is_reported(self):
        src = copy.deepcopy([s for s in self.m["sources"] if s["source_key"] == "GT"][0])
        src["adapter_options"]["extra_finding_fields"] = []
        out = sources.adapt_coherence_ledger(src)
        self.assertTrue(any("undeclared fields ['dependence']" in p for p in out["problems"]))


class RegenerationAndSnapshots(unittest.TestCase):
    def test_regeneration_is_idempotent_and_matches_committed_views(self):
        a = generate.build(*generate.load_inputs())
        b = generate.build(*generate.load_inputs())
        self.assertEqual(a, b)
        self.assertEqual(generate.stale(a), [])

    def test_edited_generated_view_is_detected(self):
        with sandbox() as root:
            (root / "generated/links.md").write_text("edited by hand\n")
            rep = workflow.check(use_git=False, scope_base=None)
            self.assertTrue(any("generated view stale: links.md" in e for e in rep["errors"]))

    def test_snapshot_is_immutable_and_tamper_evident(self):
        with sandbox() as root:
            lock = workflow.create_snapshot("test-snap", "test")
            self.assertEqual(workflow.verify_snapshots(), [])
            with self.assertRaises(FileExistsError):
                workflow.create_snapshot("test-snap", "again")
            (root / "snapshots/test-snap/views/index.md").write_text("changed\n")
            problems = workflow.verify_snapshots()
            self.assertTrue(any("TAMPERED" in p for p in problems))
            self.assertEqual(len(lock["content_hash"]), 64)


class NegativeAndContradictoryPreservation(unittest.TestCase):
    def test_rejected_and_undetermined_keep_rationale(self):
        m, loaded, shared = inputs()
        bad = copy.deepcopy(shared)
        p = [x for x in bad["proposals"] if x["status"] == "rejected"][0]
        p.pop("decision_rationale")
        self.assertTrue(any("keep their rationale" in e for e in ledger.validate_all(m, loaded, bad)))

    def test_contrasts_and_rejections_are_visible(self):
        files = generate.build(*generate.load_inputs())
        text = files["contradictions-and-nulls.md"]
        for token in ("X::0003", "X::0004", "P::0001", "P::0002", "P::0008", "REJECTED", "negative_finding"):
            self.assertIn(token, text)


class ViewsCoverageAndReadability(unittest.TestCase):
    def test_every_concept_has_a_theme_page_and_front_page_links_views(self):
        files = generate.build(*generate.load_inputs())
        m, loaded, shared = inputs()
        for c in shared["concepts"]:
            self.assertIn(f"themes/{c['concept_id'].split('::')[1]}.md", files)
        for view in ("provenance.md", "links.md", "contradictions-and-nulls.md", "questions.md", "candidate-bridges.md", "metaphor-coverage.md", "metaphor-overlap.md", "metaphor-gaps.md", "chronology.md", "graph.json"):
            self.assertIn(view, files)
            self.assertIn(view, files["index.md"])

    def test_statuses_in_text_and_mermaid_views_stay_small(self):
        files = generate.build(*generate.load_inputs())
        self.assertIn("AGENT-REVIEWED", files["links.md"])
        self.assertIn("MISSING", files["provenance.md"])
        self.assertIn("PENDING_INTAKE", files["provenance.md"])
        for rel, text in files.items():
            if rel.endswith(".mmd") or rel.startswith("themes/"):
                self.assertLess(text.count("-->") + text.count("-.->") + text.count("---"), 80, rel)

    def test_absent_sources_are_marked_absent_from_the_local_tree(self):
        files = generate.build(*generate.load_inputs())
        self.assertIn("ABSENT (not tracked on this branch)", files["provenance.md"])

    def test_graph_export_keeps_edge_families_separate(self):
        g = json.loads(generate.build(*generate.load_inputs())["graph.json"])
        self.assertEqual({"schema", "nodes", "scientific_edges", "metaphor_edges", "provenance_edges", "note"}, set(g))
        self.assertTrue(all(e["kind"] == "metaphor_link" for e in g["metaphor_edges"]))
        self.assertFalse(any(e["kind"] == "metaphor_link" for e in g["scientific_edges"]))


class ReviewAndHistoricalIntake(unittest.TestCase):
    def test_promotion_refused_for_incomplete_evidential_comparison(self):
        with sandbox():
            with self.assertRaises(ValueError):
                workflow.review_proposal("P::0004", "agent_reviewed", "agent: test", "trying to promote", human=False)

    def test_human_acceptance_needs_a_named_human(self):
        with sandbox():
            with self.assertRaises(ValueError):
                workflow.review_proposal("P::0003", "human_accepted", "agent: test", "x", human=True)

    def test_historical_claims_cannot_be_accepted_before_intake(self):
        m, loaded, shared = inputs()
        bad = copy.deepcopy(shared)
        x = bad["connections"][0]
        x["from"] = "HIST::505-507"
        problems = ledger.validate_all(m, loaded, bad)
        self.assertTrue(any("is pending_intake" in p for p in problems))

    def test_pending_pointers_allowed_only_in_unresolved_records(self):
        m, loaded, shared = inputs()
        self.assertEqual(ledger.validate_all(m, loaded, shared), [])  # P::0005, XQ::05 are pending
        bad = copy.deepcopy(shared)
        q = [q for q in bad["questions"] if q["question_id"] == "XQ::05"][0]
        q["status"] = "open"
        self.assertTrue(any("requires status pending_source" in p for p in ledger.validate_all(m, loaded, bad)))

    def test_seed_intake_stages_unapproved_proposals_only(self):
        with sandbox() as root:
            seeds = root / "incoming"
            seeds.mkdir()
            (seeds / "candidate-relations.jsonl").write_text(json.dumps({"from": "CL::F003-CLOCK-SPLIT", "to": "GT::GT-F69-CLOCK-SEPARATED-SORTING", "connection_type": "tested_structural_analogy", "scope": "s", "rationale": "r"}) + "\n")
            before = core.sha256_file(root / "ledger/connections.jsonl")
            rep = workflow.intake_seeds(seeds)
            self.assertEqual(rep["candidate_relations"], 1)
            self.assertEqual(before, core.sha256_file(root / "ledger/connections.jsonl"))
            staged = core.read_jsonl(root / "proposals/candidate-relations.jsonl")[-1]
            self.assertEqual((staged["status"], staged["origin"]), ("proposed", "author_seed"))


class NonMutationOfResearchRecords(unittest.TestCase):
    def test_branch_changes_only_the_shared_layer(self):
        v = workflow.scope_violations("origin/main")
        if v is None:
            self.skipTest("origin/main not available")
        self.assertEqual(v, [])

    def test_generation_writes_only_under_generated(self):
        with sandbox() as root:
            snapshot = {p: core.sha256_file(p) for p in root.rglob("*") if p.is_file() and "generated" not in p.parts}
            generate.write(generate.build(*generate.load_inputs()))
            after = {p: core.sha256_file(p) for p in root.rglob("*") if p.is_file() and "generated" not in p.parts}
            self.assertEqual(snapshot, after)


if __name__ == "__main__":
    unittest.main()
