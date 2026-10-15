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

from rssynth import core, discover, generate, ledger, pins, roundtrip, sources, workflow  # noqa: E402

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
        self.assertTrue(all(r["pin"] in ("ok", "local_in_branch") for r in recs), [r for r in recs if r["pin"] not in ("ok", "local_in_branch")])

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
        text = files["contradictions.md"] + files["nulls.md"]
        for token in ("X::0003", "X::0004", "P::0001", "P::0002", "P::0008", "REJECTED", "negative_finding", "P::FA-01", "SYN-C003"):
            self.assertIn(token, text)


class ViewsCoverageAndReadability(unittest.TestCase):
    def test_every_concept_has_a_theme_page_and_front_page_links_views(self):
        files = generate.build(*generate.load_inputs())
        m, loaded, shared = inputs()
        for c in shared["concepts"]:
            self.assertIn(f"themes/{c['concept_id'].split('::')[1]}.md", files)
        for view in ("provenance.md", "links.md", "contradictions.md", "nulls.md", "questions.md", "candidate-bridges.md", "metaphor-coverage.md", "metaphor-overlap.md", "metaphor-gaps.md", "metaphor-links.mmd", "chronology.md", "graph.json"):
            self.assertIn(view, files)
            self.assertIn(view, files["index.md"])

    def test_statuses_in_text_and_mermaid_views_stay_small(self):
        files = generate.build(*generate.load_inputs())
        self.assertIn("HUMAN-ACCEPTED", files["links.md"])
        self.assertIn("EXTERNAL_STORED", files["provenance.md"])
        self.assertIn("PENDING_INTAKE", files["provenance.md"])
        for rel, text in files.items():
            if rel.endswith(".mmd") or rel.startswith("themes/"):
                self.assertLess(text.count("-->") + text.count("-.->") + text.count("---"), 80, rel)

    def test_absent_sources_are_marked_absent_from_the_local_tree(self):
        files = generate.build(*generate.load_inputs())
        self.assertIn("ABSENT (not tracked on this branch)", files["provenance.md"])

    def test_graph_export_keeps_edge_families_separate(self):
        g = json.loads(generate.build(*generate.load_inputs())["graph.json"])
        self.assertEqual({"schema", "nodes", "scientific_edges", "metaphor_edges", "provenance_edges", "note", "shared_records", "sources"}, set(g))
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


class AuthorPackSeedIntake(unittest.TestCase):
    CLAIM = {"proposal_id": "SYN-T001", "claim": "c", "cannot_infer": "n", "discriminator": "d", "theme": "t", "relation_type_proposed": "candidate_mechanism_analogy", "review_status": "candidate", "sources": ["CL::F003-CLOCK-SPLIT", "GT::GT-F69-CLOCK-SEPARATED-SORTING", "HIST::some/archive/path.md"]}
    METAPHOR = {"metaphor_id": "META-T", "name": "n", "audience": "general", "concept_targets": ["clock_dependence", "brand_new_target"], "maps": [["stopwatch", "continuous time"]], "explanation": "e", "boundary": "not physical time", "misleading_if": "read as physics", "image_suggestion": "i", "status": "proposed_non_evidentiary"}

    def stage(self, root):
        seeds = root / "incoming-pack"
        seeds.mkdir()
        (seeds / "candidate-relations.jsonl").write_text(json.dumps(self.CLAIM) + "\n")
        (seeds / "metaphors.jsonl").write_text(json.dumps(self.METAPHOR) + "\n")
        return seeds

    def test_pack_schema_is_kept_verbatim_and_mapped_conservatively(self):
        with sandbox() as root:
            before = {p: core.sha256_file(p) for p in (root / "ledger").glob("*.jsonl")}
            rep = workflow.intake_seeds(self.stage(root), label="test-pack")
            self.assertEqual((rep["candidate_relations"], rep["metaphors"]), (1, 1))
            claim = [p for p in core.read_jsonl(root / "proposals/candidate-relations.jsonl") if p["proposal_id"] == "P::SYN-T001"][0]
            self.assertEqual(claim["seed_record"], self.CLAIM)
            self.assertEqual((claim["kind"], claim["status"], claim["connection_type"]), ("seed_claim", "proposed", "untested_hypothesis"))
            draft = [m for m in core.read_jsonl(root / "proposals/metaphor-drafts.jsonl") if m["metaphor_id"] == "M::META-T"][0]
            self.assertEqual(draft["concepts"], ["C::clock-readout-dependence"])
            self.assertEqual(draft["unmapped_concept_targets"], ["brand_new_target"])
            self.assertIs(draft["evidentiary"], False)
            self.assertEqual(before, {p: core.sha256_file(p) for p in (root / "ledger").glob("*.jsonl")})
            self.assertTrue((root / "proposals/seeds/test-pack/receipt.json").exists())
            self.assertEqual(ledger.validate_all(*inputs()), [])

    def test_intake_is_idempotent(self):
        with sandbox() as root:
            seeds = self.stage(root)
            workflow.intake_seeds(seeds, label="test-pack")
            again = workflow.intake_seeds(seeds, label="test-pack")
            self.assertEqual((again["candidate_relations"], again["metaphors"]), (0, 0))
            self.assertEqual(sorted(again["skipped_existing"]), ["M::META-T", "P::SYN-T001"])

    def test_seed_claim_cannot_be_promoted_or_remapped(self):
        with sandbox() as root:
            workflow.intake_seeds(self.stage(root), label="test-pack")
            with self.assertRaises(ValueError):
                workflow.review_proposal("P::SYN-T001", "agent_reviewed", "agent: test", "promote", human=False)
            m, loaded, shared = inputs()
            bad = copy.deepcopy(shared)
            x = [p for p in bad["proposals"] if p["proposal_id"] == "P::SYN-T001"][0]
            x["connection_type"] = "tested_structural_analogy"
            self.assertTrue(any("seed mapping" in p for p in ledger.validate_all(m, loaded, bad)))
            x["connection_type"], x["status"] = "untested_hypothesis", "agent_reviewed"
            self.assertTrue(any("cannot be promoted directly" in p for p in ledger.validate_all(m, loaded, bad)))

    def test_stored_author_seeds_are_byte_identical_to_their_receipt(self):
        store = REAL_ROOT / "proposals/seeds/2026-10-15-author-pack"
        if not store.exists():
            self.skipTest("author pack not staged")
        receipt = core.read_json(store / "receipt.json")
        for name, rec in receipt["files"].items():
            self.assertEqual(core.sha256_file(store / name), rec["sha256"])


class Conformance0204(unittest.TestCase):
    """Architecture contract (02), discovery rubric (03), acceptance list (04)."""

    def setUp(self):
        self.m, self.loaded, self.shared = inputs()

    def errs(self, shared):
        return ledger.validate_all(self.m, self.loaded, shared)

    def test_decision_history_is_append_only_and_transitions_are_checked(self):
        old = copy.deepcopy(self.shared["connections"])
        new = copy.deepcopy(old)
        new[0]["decision_history"][0]["rationale"] = "rewritten"
        self.assertTrue(any("rewritten" in p for p in ledger.history_is_append_only(old, new, "connection_id")))
        appended = copy.deepcopy(old)
        appended[0]["decision_history"].append(dict(appended[0]["decision_history"][-1], status="under_review"))
        self.assertEqual(ledger.history_is_append_only(old, appended, "connection_id"), [])
        bad = copy.deepcopy(self.shared)
        bad["connections"][0]["decision_history"] = [dict(bad["connections"][0]["decision_history"][0], status="human_accepted")]
        self.assertTrue(any("transition" in p or "human" in p for p in self.errs(bad)))
        stale = copy.deepcopy(self.shared)
        stale["connections"][0]["review_status"] = "under_review"
        self.assertTrue(any("last decision_history entry" in p for p in self.errs(stale)))

    def test_unreviewed_rounds_cap_the_decision(self):
        bad = copy.deepcopy(self.shared)
        x = [c for c in bad["connections"] if c["connection_id"] == "X::0001"][0]  # CL 008N and GT-P009
        x["decision_category"] = "accepted_bounded"
        x["decision_history"][-1]["decision_category"] = "accepted_bounded"
        self.assertTrue(any("unreviewed round" in p for p in self.errs(bad)))
        x3 = [c for c in self.shared["connections"] if c["connection_id"] == "X::0003"][0]
        self.assertEqual(x3["decision_category"], "accepted_bounded")  # older, reviewed rounds may be accepted

    def test_unresolved_sources_stay_blocked(self):
        bad = copy.deepcopy(self.shared)
        p = [x for x in bad["proposals"] if x["proposal_id"] == "P::SYN-C001"][0]
        self.assertEqual(p["decision_category"], "blocked_missing_source")
        p["decision_category"] = "candidate"
        p["decision_history"][-1]["decision_category"] = "candidate"
        self.assertTrue(any("must stay blocked_missing_source" in e for e in self.errs(bad)))

    def test_review_vector_has_nine_unsummed_axes(self):
        bad = copy.deepcopy(self.shared)
        bad["connections"][0]["review_vector"]["overall"] = {"assessment": "high"}
        self.assertTrue(any("exactly the axes" in p for p in self.errs(bad)))
        bad2 = copy.deepcopy(self.shared)
        bad2["connections"][0]["review_vector"]["formal_comparability"]["score"] = 4
        self.assertTrue(any("not scored or summed" in p for p in self.errs(bad2)))
        bad3 = copy.deepcopy(self.shared)
        bad3["connections"][0]["review_vector"]["falsifiability"]["retrieval_score"] = 0.9
        self.assertTrue(any("only semantic_resemblance" in p for p in self.errs(bad3)))

    def test_false_attractors_are_recorded_rejected_and_cannot_be_promoted(self):
        fa = {p["proposal_id"]: p for p in self.shared["proposals"] if p.get("false_attractor_control")}
        self.assertEqual(set(fa), {"P::FA-01", "P::FA-02", "P::FA-03", "P::FA-04", "P::FA-05"})
        self.assertTrue(all(p["status"] == "rejected" and p["decision_category"] == "rejected" and p["counterevidence_refs"] for p in fa.values()))
        with sandbox():
            with self.assertRaises(Exception):
                workflow.review_proposal("P::FA-01", "agent_reviewed", "agent: test", "promote", human=False)

    def test_metaphor_coverage_is_not_corroboration(self):
        # sixth false attractor: coverage by several metaphors adds no evidence to any finding
        base = ledger.project_graph(self.m, self.loaded, self.shared)
        more = copy.deepcopy(self.shared)
        for i in range(3):
            more["metaphors"].append(dict(more["metaphors"][0], metaphor_id=f"M::cover-{i}"))
            more["metaphor_links"].append({"link_id": f"ML::9{i}", "link_type": "covers_concept", "from": f"M::cover-{i}", "to": "C::occupancy-vs-process", "note": "x"})
        after = ledger.project_graph(self.m, self.loaded, more)
        self.assertEqual(base["scientific_edges"], after["scientific_edges"])
        self.assertFalse(any("evidence_count" in n for n in after["nodes"]))

    def test_unreachable_pin_fails_with_actionable_diagnostic(self):
        with sandbox() as root:
            m = core.read_json(root / "sources/manifest.json")
            m["sources"][1]["commit"] = "1" * 40
            core.write_json(root / "sources/manifest.json", m)
            rep = workflow.check(use_git=True, scope_base=None)
            msgs = [e for e in rep["errors"] if "not reachable" in e]
            self.assertTrue(msgs and "fetch" in msgs[0])

    def test_graph_json_is_lossless(self):
        g = json.loads(generate.build(*generate.load_inputs())["graph.json"])
        for k in ("concepts", "connections", "questions", "metaphors", "metaphor_links", "proposals", "metaphor_drafts"):
            self.assertEqual(len(g["shared_records"][k]), len(self.shared[k]))
        conn = [c for c in g["shared_records"]["connections"] if c["connection_id"] == "X::0001"][0]
        self.assertIn("review_vector", conn)
        self.assertIn("decision_history", conn)
        node = [n for n in g["nodes"] if n["id"] == "GT::GT-F78-LIFETIME-NOT-SET-BY-STATIONARY-LAW"][0]
        self.assertTrue(node["unreviewed_round"])
        self.assertEqual(len(node["source_commit"]), 40)

    def test_required_view_names(self):
        files = generate.build(*generate.load_inputs())
        for c in self.shared["concepts"]:
            stem = c["concept_id"].split("::")[1]
            self.assertIn(f"themes/{stem}.mmd", files)
        self.assertIn("YES", files["links.md"])  # unreviewed-round marker shown in text
        self.assertIn("Review diagnostics: unresolved references", files["candidate-bridges.md"])
        self.assertIn("HIST::", files["candidate-bridges.md"])
        self.assertIn("overreach", files["metaphor-gaps.md"])
        self.assertIn("Open cross-programme question", files["index.md"])

    def test_metaphors_need_useful_scope(self):
        bad = copy.deepcopy(self.shared)
        bad["metaphors"][0].pop("useful_scope")
        self.assertTrue(any("useful scope missing" in p for p in self.errs(bad)))

    def test_accepted_records_cannot_claim_physics(self):
        bad = copy.deepcopy(self.shared)
        x = [c for c in bad["connections"] if c["decision_category"] == "accepted_bounded"][0]
        x["rationale"] += " This derives gravity."
        self.assertTrue(any("must not assert 'gravity'" in p for p in self.errs(bad)))

    def test_false_positive_seed_is_rejected_and_unresolved_seed_stays_unresolved(self):
        with sandbox() as root:
            seeds = root / "fp-seeds"
            seeds.mkdir()
            rows = [{"proposal_id": "SYN-FP1", "claim": "basin is gravity", "cannot_infer": "", "discriminator": "", "theme": "fp", "relation_type_proposed": "compatible_with", "review_status": "candidate", "sources": ["GT::GT-F09-POTENTIAL-AS-MECHANISM", "C::physical-attraction"]},
                    {"proposal_id": "SYN-UN1", "claim": "historical bridge", "cannot_infer": "", "discriminator": "", "theme": "un", "relation_type_proposed": "compatible_with", "review_status": "candidate", "sources": ["CL::F004-PASSAGE-AFTER-OCCUPANCY", "HIST::rs_work_round11/findings.md"]}]
            (seeds / "candidate-relations.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
            workflow.intake_seeds(seeds, label="fp")
            rec = workflow.review_proposal("P::SYN-FP1", "rejected", "agent: test", "shared metaphor only; no derived acceleration", human=False, decision_category="rejected")
            self.assertEqual((rec["status"], rec["decision_category"]), ("rejected", "rejected"))
            self.assertEqual([h["status"] for h in rec["decision_history"]], ["proposed", "rejected"])
            with self.assertRaises(ValueError):
                workflow.review_proposal("P::SYN-UN1", "undetermined", "agent: test", "trying to advance", human=False, decision_category="candidate")
            self.assertEqual(ledger.validate_all(*inputs()), [])


class ExternalSynthesisClaims(unittest.TestCase):
    def setUp(self):
        self.m, self.loaded, self.shared = inputs()
        self.ext = {p["proposal_id"]: p for p in self.shared["proposals"] if p.get("kind") == "external_claim"}

    def test_claims_are_registered_with_verbatim_quotes_and_agent_mapping(self):
        self.assertEqual(len(self.ext), 22)
        doc = (REAL_ROOT / "reports/external-2026-10-15-cross-research-synthesis.md").read_text(encoding="utf-8")
        for p in self.ext.values():
            self.assertIn(p["quote"], doc)
            self.assertEqual((p["source_mapping"], p["origin"]), ("agent", "external_synthesis"))
            self.assertIn(p["status"], ("proposed", "under_review"))  # under_review once checked against records
            self.assertTrue(p["provenance_ref"].startswith("EXT::"))

    def test_historical_claims_are_blocked_and_others_candidate(self):
        for p in self.ext.values():
            hist = any(r.startswith("HIST::") for r in p["sources"])
            if hist:
                self.assertEqual(p["decision_category"], "blocked_missing_source", p["proposal_id"])
            else:
                self.assertIn(p["decision_category"], ("candidate", "qualified"), p["proposal_id"])

    def test_altered_quote_or_promotion_is_refused(self):
        bad = copy.deepcopy(self.shared)
        x = [p for p in bad["proposals"] if p["proposal_id"] == "P::EXT-C02"][0]
        x["quote"] = x["quote"].replace("does not entail", "entails")
        self.assertTrue(any("verbatim" in e for e in ledger.validate_all(self.m, self.loaded, bad)))
        with sandbox():
            with self.assertRaises(ValueError):
                workflow.review_proposal("P::EXT-C02", "agent_reviewed", "agent: test", "promote", human=False)

    def test_registration_is_idempotent_and_keeps_other_records(self):
        import importlib.util

        spec = importlib.util.spec_from_file_location("reg", REAL_ROOT / "proposals/register_external_claims.py")
        reg = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(reg)
        with sandbox() as root:
            before = core.read_jsonl(root / "proposals/candidate-relations.jsonl")
            reg.write(root)
            after = core.read_jsonl(root / "proposals/candidate-relations.jsonl")
            self.assertEqual(sorted(json.dumps(r, sort_keys=True) for r in before), sorted(json.dumps(r, sort_keys=True) for r in after))


class ExternalClaimRestatement(unittest.TestCase):
    def setUp(self):
        self.m, self.loaded, self.shared = inputs()
        self.props = {p["proposal_id"]: p for p in self.shared["proposals"]}

    def test_checked_claims_link_to_existing_restatements(self):
        checked = [p for p in self.props.values() if p.get("kind") == "external_claim" and p.get("check_outcome")]
        self.assertEqual(len(checked), 15)
        for c in checked:
            self.assertEqual(c["status"], "under_review")
            self.assertEqual([h["status"] for h in c["decision_history"]], ["proposed", "under_review"])
            for r in c["restated_as"]:
                rp = self.props[r]
                self.assertTrue(rp["derived_from_claim"] == c["proposal_id"] or c["proposal_id"].removeprefix("P::") in rp["rationale"], (c["proposal_id"], r))
        blocked = [p for p in self.props.values() if p.get("kind") == "external_claim" and p["decision_category"] == "blocked_missing_source"]
        self.assertTrue(blocked and all(not p.get("check_outcome") for p in blocked))

    def test_cited_upstream_relations_exist_in_pinned_ledgers(self):
        edge_ids = {e["id"] for e in self.loaded["edges"]}
        for p in self.props.values():
            for rel in p.get("upstream_relations", []):
                self.assertIn(rel.split(" ")[0], edge_ids, p["proposal_id"])

    def test_within_programme_relations_never_enter_the_shared_ledger(self):
        u1 = self.props["P::EXT-C06-U1"]
        self.assertTrue(u1["within_programme"])
        with sandbox():
            with self.assertRaises(ValueError):
                workflow.review_proposal("P::EXT-C06-U1", "agent_reviewed", "agent: test", "promote", human=False, decision_category="qualified")
        bad = copy.deepcopy(self.shared)
        x = dict(bad["connections"][0], connection_id="X::0999", **{"from": "GT::GT-F68-FIRST-ORDER-SORTING-INDEX", "to": "GT::GT-F71-SORTING-DECOMPOSITION-POSTHOC"})
        bad["connections"].append(x)
        self.assertTrue(any("cross-programme relations only" in e for e in ledger.validate_all(self.m, self.loaded, bad)))
        unmarked = copy.deepcopy(self.shared)
        [p for p in unmarked["proposals"] if p["proposal_id"] == "P::EXT-C06-U1"][0]["within_programme"] = False
        self.assertTrue(any("mark within_programme" in e for e in ledger.validate_all(self.m, self.loaded, unmarked)))

    def test_restatement_is_idempotent_and_append_only(self):
        import importlib.util

        spec = importlib.util.spec_from_file_location("restate", REAL_ROOT / "proposals/restate_external_claims.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with sandbox() as root:
            before = core.read_jsonl(root / "proposals/candidate-relations.jsonl")
            self.assertEqual(mod.run(root), {"proposals_added": 0, "claims_checked": 0})
            after = core.read_jsonl(root / "proposals/candidate-relations.jsonl")
            self.assertEqual(before, after)
            self.assertEqual(ledger.history_is_append_only(before, after, "proposal_id"), [])


class AuthorDecisions(unittest.TestCase):
    def setUp(self):
        self.m, self.loaded, self.shared = inputs()

    def syn3(self, shared):
        return [p for p in shared["proposals"] if p["proposal_id"] == "P::SYN-C003"][0]

    def test_syn_c003_is_an_explicit_contrast_by_author_decision(self):
        p = self.syn3(self.shared)
        self.assertEqual(p["seed_record"]["relation_type_proposed"], "compatible_with")  # verbatim seed untouched
        self.assertEqual((p["connection_type"], p["relation_override"]["matches"]), ("explicit_contrast", "X::0003"))
        self.assertTrue(p["decision_history"][-1]["human"])
        x3 = [c for c in self.shared["connections"] if c["connection_id"] == "X::0003"][0]
        self.assertEqual(x3["connection_type"], "explicit_contrast")
        # AD-0001 did not accept X::0003; its acceptance came later and separately, through round trip RT-0001 (AD-0002)
        self.assertFalse(any(h.get("decision_id") == "AD-0001" for h in x3["decision_history"]))
        self.assertEqual((x3["review_status"], x3["decision_history"][-1]["decision_id"]), ("human_accepted", "AD-0002"))

    def test_override_must_be_human_and_consistent(self):
        bad = copy.deepcopy(self.shared)
        self.syn3(bad)["relation_override"]["human"] = False
        self.assertTrue(any("recorded human decision" in e for e in ledger.validate_all(self.m, self.loaded, bad)))
        bad2 = copy.deepcopy(self.shared)
        self.syn3(bad2)["connection_type"] = "qualifies"
        self.assertTrue(any("must equal the author's relation_override" in e for e in ledger.validate_all(self.m, self.loaded, bad2)))
        bad3 = copy.deepcopy(self.shared)
        self.syn3(bad3)["decision_history"] = self.syn3(bad3)["decision_history"][:1]
        self.assertTrue(any("matching human entry" in e for e in ledger.validate_all(self.m, self.loaded, bad3)))

    def test_decision_log_is_append_only_and_idempotent(self):
        import importlib.util

        spec = importlib.util.spec_from_file_location("ad", REAL_ROOT / "proposals/author_decisions.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with sandbox() as root:
            before = (root / "proposals/author-decisions.jsonl").read_bytes()
            self.assertEqual(mod.run(root), {"logged": 0, "applied": 0})
            self.assertEqual(before, (root / "proposals/author-decisions.jsonl").read_bytes())

    def test_views_show_the_decision_not_an_open_disagreement(self):
        files = generate.build(*generate.load_inputs())
        self.assertIn("Author decision:** P::SYN-C003 classified as `explicit_contrast`", files["index.md"])
        self.assertNotIn("Author decision required", files["contradictions.md"] + files["index.md"])


class ImplicitRoundTripAcceptance(unittest.TestCase):
    """The author's rule: human acceptance is implicit in the round trip, at the reported category."""

    def _reopen(self, root, cid):
        rows = core.read_jsonl(root / "ledger/connections.jsonl")
        for x in rows:
            if x["connection_id"] == cid:
                for st in ("under_review", "agent_reviewed"):
                    x["decision_history"].append({"date": "2026-10-16", "actor": "agent: test", "human": False, "status": st, "decision_category": x["decision_category"], "rationale": "test"})
                x["review_status"] = "agent_reviewed"
                x["review"] = {"reviewer": "agent: test", "date": "2026-10-16", "record": x["review"]["record"], "human": False}
        core.write_jsonl(root / "ledger/connections.jsonl", rows)

    def _problems(self, root):
        m, loaded, shared = inputs()
        return ledger.validate_all(m, loaded, shared) + roundtrip.validate(root, shared)

    def test_rt0001_ratified_by_ad0002_without_upgrades(self):
        m, loaded, shared = inputs()
        self.assertEqual(roundtrip.validate(REAL_ROOT, shared), [])
        self.assertEqual(roundtrip.open_round_trips(REAL_ROOT), [])
        rt = roundtrip.load_round_trips(REAL_ROOT)["RT-0001"]
        cats = {r["target"]: r["decision_category"] for r in rt["recommendations"]}
        for x in shared["connections"]:
            self.assertEqual((x["review_status"], x["decision_category"]), ("human_accepted", cats[x["connection_id"]]))
            self.assertTrue(x["decision_history"][-1]["human"])
        self.assertEqual(cats["X::0001"], "qualified")  # rests on unreviewed 008N / GT-P009: the cap holds through acceptance
        self.assertTrue(all(m["status"] == "human_accepted" and m["evidentiary"] is False for m in shared["metaphors"]))

    def test_seeds_and_external_claims_are_never_listed(self):
        rt = roundtrip.load_round_trips(REAL_ROOT)["RT-0001"]
        self.assertFalse([r for r in rt["recommendations"] if r["target"].startswith(("P::SYN-", "P::EXT-"))])

    def test_ratification_cannot_upgrade_a_category(self):
        with sandbox() as root:
            rows = core.read_jsonl(root / "ledger/connections.jsonl")
            x = [r for r in rows if r["connection_id"] == "X::0006"][0]  # qualified, not on an unreviewed round
            x["decision_history"][-1]["decision_category"] = x["decision_category"] = "accepted_bounded"
            core.write_jsonl(root / "ledger/connections.jsonl", rows)
            self.assertTrue(any("never upgrades" in p for p in self._problems(root)))

    def test_a_round_trip_is_ratified_once_and_immutable(self):
        with sandbox() as root:
            with self.assertRaises(ValueError):
                roundtrip.ratify("RT-0001", "AD-0099", "2026-10-16", "again")
            with self.assertRaises(FileExistsError):
                roundtrip.open_round_trip("RT-0001", "2026-10-16", "research-synthesis/README.md", "0" * 40)

    def test_objection_reopens_and_the_rest_are_accepted(self):
        with sandbox() as root:
            self._reopen(root, "X::0002")
            self._reopen(root, "X::0006")
            rt = roundtrip.open_round_trip("RT-0002", "2026-10-16", "research-synthesis/README.md", "0" * 40)
            self.assertEqual({r["target"] for r in rt["recommendations"]}, {"X::0002", "X::0006"})
            self.assertEqual(roundtrip.open_round_trips(root), ["RT-0002"])
            rep = roundtrip.ratify("RT-0002", "AD-0003", "2026-10-16", "next prompt", objections=["X::0002"])
            self.assertEqual((rep["accepted"], rep["objected"]), (1, ["X::0002"]))
            conns = {x["connection_id"]: x for x in core.read_jsonl(root / "ledger/connections.jsonl")}
            self.assertEqual(conns["X::0002"]["review_status"], "under_review")
            self.assertEqual((conns["X::0006"]["review_status"], conns["X::0006"]["decision_category"]), ("human_accepted", "qualified"))
            self.assertEqual(self._problems(root), [])
            with self.assertRaises(ValueError):
                roundtrip.ratify("RT-0002", "AD-0004", "2026-10-16", "x", objections=["X::0009"])

    def test_citing_an_unlogged_ratification_is_rejected(self):
        with sandbox() as root:
            rows = core.read_jsonl(root / "ledger/connections.jsonl")
            rows[0]["decision_history"][-1]["decision_id"] = "AD-0777"
            core.write_jsonl(root / "ledger/connections.jsonl", rows)
            self.assertTrue(any("not a logged round-trip ratification" in p for p in self._problems(root)))


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
