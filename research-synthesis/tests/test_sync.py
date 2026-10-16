"""Administrative adoption, branch discovery and mathematical scope regressions."""

import copy
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from rssynth import core, pins, preview, sources
from test_rssynth import sandbox

CL = "08d7017be85616df7bc5b2934e8076bdcc73a319"


class Synchronisation(unittest.TestCase):
    def test_adoption_updates_commit_and_continuation_metadata_together(self):
        with sandbox() as root:
            before_gt = sources.sources_by_key(sources.load_manifest())["GT"]
            meta=core.read_json(root/"proposals/source-metadata/CL-synchronisation-2026-10-16.json")
            pins.propose_pin(sources.load_manifest(),"CL",CL,metadata=meta)
            # Synthetic sandbox reviewer only; never a live adoption or author decision.
            m=pins.apply_pin("CL",CL,reviewed_by="Test Human (sandbox fixture only)")
            source=sources.sources_by_key(m)["CL"]
            self.assertEqual((source["commit"],source["branch"],source["revision_label"]),(CL,meta["branch"],"008p"))
            self.assertEqual(source["unreviewed_generations"],["008O","008P"])
            self.assertEqual(len(source["closed_milestones"]),3)
            self.assertEqual(sources.sources_by_key(m)["GT"], before_gt)

    def test_correct_commit_with_old_branch_is_rejected_before_writes(self):
        with sandbox() as root:
            # Recreate the abandoned-branch configuration even after live adoption.
            spec_path=root/"sources/pin-spec.json"
            spec=core.read_json(spec_path)
            for source in spec["sources"]:
                if source["source_key"]=="CL":
                    source["branch"]="research/constraint-lab-v0.8n-h2-controlled-passage"
            core.write_json(spec_path,spec)
            pins.propose_pin(sources.load_manifest(),"CL",CL)
            path=root/"sources/pin-spec.json"
            before=path.read_bytes()
            with self.assertRaisesRegex(sources.SourceError,"abandoned/parallel branch"):
                pins.apply_pin("CL",CL,reviewed_by="Test Human (sandbox fixture only)")
            self.assertEqual(path.read_bytes(),before)

    def test_metadata_never_replaces_named_human_review(self):
        with self.assertRaisesRegex(sources.SourceError,"named human"):
            pins.apply_pin("CL",CL,reviewed_by="agent: test")

    def test_stale_proposal_cannot_replace_current_pin(self):
        with sandbox() as root:
            pins.propose_pin(sources.load_manifest(), "CL", CL)
            path = root/"proposals/pin-updates"/f"CL-{CL[:12]}.json"
            proposal = core.read_json(path)
            proposal["current_commit"] = "0"*40
            core.write_json(path, proposal)
            before = (root/"sources/pin-spec.json").read_bytes()
            with self.assertRaisesRegex(sources.SourceError, "stale"):
                pins.apply_pin("CL", CL, reviewed_by="Test Human (sandbox fixture only)")
            self.assertEqual(before, (root/"sources/pin-spec.json").read_bytes())

    def test_standing_decision_does_not_approve_cl_status_rewrite(self):
        with sandbox() as root:
            proposal = core.read_json(root/"proposals/pin-updates/CL-08d7017be856.json")
            self.assertTrue(proposal["warnings"])
            with self.assertRaisesRegex(sources.SourceError, "no warnings"):
                pins.auto_apply_pin("CL", CL)

    def test_tampered_metadata_digest_is_rejected(self):
        with sandbox() as root:
            meta=core.read_json(root/"proposals/source-metadata/CL-synchronisation-2026-10-16.json")
            pins.propose_pin(sources.load_manifest(),"CL",CL,metadata=meta)
            path=root/"proposals/pin-updates"/f"CL-{CL[:12]}.json"
            prop=core.read_json(path);prop["source_metadata"]["revision_label"]="invented"
            core.write_json(path,prop)
            with self.assertRaisesRegex(sources.SourceError,"digest changed"):
                pins.apply_pin("CL",CL,reviewed_by="Test Human (sandbox fixture only)")

    def test_metadata_cannot_change_source_authority(self):
        with self.assertRaisesRegex(sources.SourceError,"unsupported"):
            pins.checked_metadata({"status":"included"},CL)

    def test_cl_successor_is_visible_even_when_old_tracked_branch_is_current(self):
        m={"sources":[{"source_key":"CL","branch":"old","commit":"a"*40}]}
        with patch.object(sources,"_git",return_value="research/constraint-lab-v0.8p-stopping-sufficiency "+CL),patch.object(sources,"is_ancestor",return_value=True):
            candidates=sources.continuation_candidates(m)
        self.assertEqual(candidates[0]["completion"],"unknown_do_not_ingest")
        self.assertEqual(candidates[0]["pinned_commit"],"a"*40)

    def test_declared_closed_and_unknown_head_remain_distinct(self):
        m={"sources":[{"source_key":"CL","branch":"old","commit":"a"*40,
            "closed_milestones":[{"commit":CL,"scientific_review":"pending"}]}]}
        refs="research/constraint-lab-v0.8p-stopping-sufficiency "+CL+"\nresearch/constraint-lab-v0.8q-ongoing "+"b"*40
        with patch.object(sources,"_git",return_value=refs),patch.object(sources,"is_ancestor",return_value=True):
            a,b=sources.continuation_candidates(m)
        self.assertEqual(a["completion"],"declared_closed_milestone")
        self.assertEqual(b["completion"],"unknown_do_not_ingest")

    def test_method_version_does_not_follow_unrelated_main_commits(self):
        m={"sources":[{"source_key":"OTR","branch":"main","commit":"a"*40,"role":"shared_method",
            "artifacts":[{"path":"method.md","git_blob":"same"}]}]}
        with patch.object(sources,"remote_branch_head",return_value="b"*40),patch.object(sources,"_git",return_value="same"):
            self.assertEqual(sources.staleness(m)[0]["state"],"current")
        self.assertEqual(m["sources"][0]["commit"],"a"*40)
        with patch.object(sources,"remote_branch_head",return_value="b"*40),patch.object(sources,"_git",return_value="changed"),patch.object(sources,"is_ancestor",return_value=True):
            self.assertEqual(sources.staleness(m)[0]["state"],"behind_branch_head")

    def test_uniform_count_reset_is_not_single_toggle_support(self):
        # Parameter-free three-slot incidence witness, not a GT or CL model run.
        x=frozenset({0})
        layer=[frozenset(c) for c in combinations(range(3),2)]
        reset={y:Fraction(1,len(layer)) for y in layer}
        legal=[y for y in layer if len(x ^ y)==1]
        self.assertEqual(len(legal),2)
        self.assertEqual(reset[frozenset({1,2})],Fraction(1,3))
        self.assertNotIn(frozenset({1,2}),legal)

    def test_preview_validates_new_references_without_adopting_pins(self):
        with sandbox() as root:
            before=(root/"sources/pin-spec.json").read_bytes()
            for name in ("CL-08d7017be856.json",):
                path=root/"proposals/pin-updates"/name
                fixture=core.read_json(path);fixture["status"]="proposed"
                core.write_json(path,fixture)
            result=preview.preview_pins(
                [root/"proposals/pin-updates/CL-08d7017be856.json"],
                root/"proposals/staged/2026-10-15-gt-p010-p011-candidates.jsonl",
                root/"proposals/staged/2026-10-16-synchronisation-questions.jsonl",
                root/"proposals/previews/test")
            self.assertEqual(result["status"],"VALIDATED_HYPOTHETICAL_NOT_ADOPTED")
            self.assertTrue(result["check"]["ok"])
            self.assertEqual(before,(root/"sources/pin-spec.json").read_bytes())

    def test_preview_refuses_canonical_output_destination(self):
        with self.assertRaisesRegex(ValueError,"never canonical"):
            preview.preview_pins([],"unused","unused",core.ROOT/"generated")


if __name__=="__main__":unittest.main()
