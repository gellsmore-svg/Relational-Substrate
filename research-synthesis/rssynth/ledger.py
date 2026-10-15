"""Shared records (concepts, connections, questions, metaphors, metaphor links), their validator, and the graph projection.

The shared ledger never copies or edits programme findings; it refers to them
by namespaced reference. Scientific edges, metaphor edges and provenance
edges are kept in separate sets at every level (schema, validator, export).
"""

from __future__ import annotations

from pathlib import Path

from . import core, historical, sources

FORBIDDEN_SCORE_FIELDS = {"score", "confidence", "probability", "similarity", "cosine", "overall_confidence", "overall_score", "finding_strength", "coherence_score", "strength_score", "master_score"}


def load_shared(root: Path | None = None) -> dict:
    root = root or core.ROOT
    return {
        "concepts": core.read_jsonl(root / "ledger" / "concepts.jsonl"),
        "connections": core.read_jsonl(root / "ledger" / "connections.jsonl"),
        "questions": core.read_jsonl(root / "ledger" / "questions.jsonl"),
        "metaphors": core.read_jsonl(root / "ledger" / "metaphors.jsonl"),
        "metaphor_links": core.read_jsonl(root / "ledger" / "metaphor-links.jsonl"),
        "proposals": core.read_jsonl(root / "proposals" / "candidate-relations.jsonl"),
        "metaphor_drafts": core.read_jsonl(root / "proposals" / "metaphor-drafts.jsonl"),
        "hist_findings": historical.load_findings(root),
        "hist_intake_plan": historical.load_intake_plan(root),
    }


# --- reference resolution ----------------------------------------------------------


class Resolver:
    def __init__(self, manifest: dict, source_nodes: dict, shared: dict):
        self.manifest = manifest
        self.source_nodes = source_nodes
        self.shared_ids = {}
        self.hist = {f.get("finding_id"): f for f in shared.get("hist_findings", [])}
        for c in shared["concepts"]:
            self.shared_ids[c["concept_id"]] = "concept"
        for q in shared["questions"]:
            self.shared_ids[q["question_id"]] = "shared_question"
        for x in shared["connections"]:
            self.shared_ids[x["connection_id"]] = "connection"
        for m in shared["metaphors"]:
            self.shared_ids[m["metaphor_id"]] = "metaphor"
        for p in shared["proposals"]:
            self.shared_ids[p["proposal_id"]] = "proposal"

    def resolve(self, ref: str) -> dict:
        """{'ok', 'kind', 'source', 'source_status', 'reason'} for one reference."""
        try:
            parts = core.parse_ref(ref)
        except ValueError as exc:
            return {"ok": False, "reason": str(exc)}
        ns = parts["namespace"]
        if ns in core.SHARED_NAMESPACES:
            kind = self.shared_ids.get(ref)
            return {"ok": kind is not None, "kind": kind, "source": "shared", "source_status": "shared", "reason": None if kind else "dangling shared reference"}
        src = sources.resolve_source(self.manifest, ns, parts["revision"])
        if src is None:
            return {"ok": False, "reason": f"no source for namespace {ns}" + (f" revision {parts['revision']}" if parts["revision"] else " (no default revision)")}
        if src["status"] in core.UNRESOLVABLE_SOURCE_STATUSES:
            return {"ok": False, "pending": True, "source": src["source_key"], "source_status": src["status"], "reason": f"source {src['source_key']} is {src['status']}"}
        key = f"{ns}::{parts['local']}"
        if src["status"] == "included_partial":
            # partial historical intake: only source-verified, publication-approved findings resolve; gaps stay pending
            f = self.hist.get(key)
            if f is None or not historical.finding_is_usable(f):
                return {"ok": False, "pending": True, "source": src["source_key"], "source_status": src["status"], "reason": f"{key} is not an intaken, source-verified and approved historical finding"}
            return {"ok": True, "kind": "historical_finding", "source": src["source_key"], "source_status": src["status"], "node": {"source": src["source_key"], "kind": "historical_finding", "created_generation": f.get("round_id") or f.get("experiment_id")}}
        if parts["revision"] and not src.get("default_revision"):
            return {"ok": src["status"] != "lineage_only", "kind": "source_revision_ref", "source": src["source_key"], "source_status": src["status"], "reason": "lineage-only revision is not ingested" if src["status"] == "lineage_only" else None}
        node = self.source_nodes.get(key)
        if node is None:
            return {"ok": False, "source": src["source_key"], "source_status": src["status"], "reason": f"{key} not found in pinned source {src['source_key']}@{src['commit'][:7]}"}
        return {"ok": True, "kind": node["kind"], "source": src["source_key"], "source_status": src["status"], "node": node}


def lineage_shared(manifest: dict, a: str, b: str) -> bool:
    """True if two sources share an ancestor through declared lineage (or are the same source)."""
    if a == b:
        return True
    keys = sources.sources_by_key(manifest)

    def ancestors(k):
        seen, stack = {k}, [k]
        while stack:
            for lin in keys.get(stack.pop(), {}).get("lineage", []):
                if lin["target"] not in seen:
                    seen.add(lin["target"])
                    stack.append(lin["target"])
        return seen

    return bool(ancestors(a) & ancestors(b))


# --- validation ---------------------------------------------------------------------------


def _no_scores(rec: dict, label: str) -> list[str]:
    bad = sorted(set(rec) & FORBIDDEN_SCORE_FIELDS)
    return [f"{label}: scalar score field(s) {bad} are not allowed in shared records"] if bad else []


def unreviewed_round(manifest: dict, node: dict | None) -> bool:
    """True if a source node comes from a round its source declares closed but not yet reviewed."""
    if not node:
        return False
    src = sources.sources_by_key(manifest).get(node.get("source"), {})
    return str(node.get("created_generation")) in set(src.get("unreviewed_generations", []))


def validate_review_vector(rv, label: str) -> list[str]:
    if not isinstance(rv, dict):
        return [f"{label}: review_vector must be an object with the nine axes"]
    p = []
    if set(rv) != set(core.REVIEW_VECTOR_AXES):
        p.append(f"{label}: review_vector must have exactly the axes {list(core.REVIEW_VECTOR_AXES)} (missing {sorted(set(core.REVIEW_VECTOR_AXES) - set(rv))}, extra {sorted(set(rv) - set(core.REVIEW_VECTOR_AXES))})")
    for axis, v in rv.items():
        if not isinstance(v, dict) or not v.get("assessment"):
            p.append(f"{label}: review_vector.{axis} needs an 'assessment' (use 'unknown' when unknown)")
            continue
        extra = set(v) - {"assessment", "retrieval_score", "method", "status"}
        if extra:
            p.append(f"{label}: review_vector.{axis} has fields {sorted(extra)}; axes are not scored or summed")
        if "retrieval_score" in v and axis != "semantic_resemblance":
            p.append(f"{label}: only semantic_resemblance may carry a retrieval score")
    ev = rv.get("evidence_status", {})
    if isinstance(ev, dict) and ev.get("status") not in core.EVIDENCE_STATUSES:
        p.append(f"{label}: review_vector.evidence_status.status must be one of {sorted(core.EVIDENCE_STATUSES)}")
    return p


def validate_history(x: dict, label: str, status_field: str) -> list[str]:
    hist = x.get("decision_history")
    if not isinstance(hist, list) or not hist:
        return [f"{label}: decision_history (append-only) is required"]
    p, prev, prev_date = [], None, ""
    for i, h in enumerate(hist):
        for f in ("date", "actor", "human", "status", "decision_category", "rationale"):
            if f not in h:
                p.append(f"{label}: decision_history[{i}] lacks {f}")
        st = h.get("status")
        if st not in core.STATUS_TRANSITIONS.get(prev, set()):
            p.append(f"{label}: decision_history[{i}] transition {prev!r} -> {st!r} is not allowed")
        if h.get("decision_category") not in core.DECISION_CATEGORIES:
            p.append(f"{label}: decision_history[{i}] decision_category {h.get('decision_category')!r}")
        if str(h.get("date", "")) < prev_date:
            p.append(f"{label}: decision_history dates go backwards at entry {i}")
        if st == "human_accepted" and (not h.get("human") or str(h.get("actor", "")).lower().startswith("agent")):
            p.append(f"{label}: decision_history[{i}] human acceptance needs a named human actor")
        prev, prev_date = st, str(h.get("date", ""))
    last = hist[-1]
    if last.get("status") != x.get(status_field) or last.get("decision_category") != x.get("decision_category"):
        p.append(f"{label}: current status/decision must equal the last decision_history entry")
    return p


def history_is_append_only(old_rows: list[dict], new_rows: list[dict], key: str) -> list[str]:
    """Every record's previous decision_history must be a prefix of its current one."""
    new = {r.get(key): r for r in new_rows}
    p = []
    for o in old_rows:
        n = new.get(o.get(key))
        oh = o.get("decision_history") or []
        if n is None:
            if oh:
                p.append(f"{o.get(key)}: a record with decision history was deleted")
            continue
        nh = n.get("decision_history") or []
        if nh[: len(oh)] != oh:
            p.append(f"{o.get(key)}: decision_history was rewritten (append-only)")
    return p


def validate_decision(x: dict, label: str, status_field: str, nodes: list[dict | None], pending: bool, manifest: dict) -> list[str]:
    p = []
    dc = x.get("decision_category")
    if dc not in core.DECISION_CATEGORIES:
        p.append(f"{label}: decision_category {dc!r} must be one of {sorted(core.DECISION_CATEGORIES)}")
    if x.get("epistemic_basis") not in core.EPISTEMIC_BASES:
        p.append(f"{label}: epistemic_basis {x.get('epistemic_basis')!r} must be one of {sorted(core.EPISTEMIC_BASES)}")
    if not isinstance(x.get("counterevidence_refs"), list):
        p.append(f"{label}: counterevidence_refs (a list, possibly empty) is required")
    st = x.get(status_field)
    if st not in ("proposed",) or "review_vector" in x:
        p += validate_review_vector(x.get("review_vector"), label)
    p += validate_history(x, label, status_field)
    if (st == "rejected") != (dc == "rejected"):
        p.append(f"{label}: status 'rejected' and decision 'rejected' go together")
    if pending and dc not in ("blocked_missing_source", "rejected"):
        p.append(f"{label}: references an unavailable source, so its decision must stay blocked_missing_source (or rejected)")
    if dc in core.ACCEPTED_DECISIONS:
        if any(unreviewed_round(manifest, n) for n in nodes):
            p.append(f"{label}: rests on a closed but unreviewed round; it cannot be {dc} (use qualified or candidate)")
        text = (x.get("rationale", "") + " " + x.get("claim", "")).lower()
        for term in core.PHYSICAL_OVERREACH_TERMS:
            if term in text:
                p.append(f"{label}: an accepted record must not assert '{term}'")
    return p


def stale_reviews(manifest: dict, connections: list[dict]) -> list[str]:
    """Connections reviewed against a source commit other than the current pin need re-review."""
    pins = {s["source_key"]: s.get("commit") for s in manifest["sources"]}
    out = []
    for x in connections:
        for src, commit in (x.get("reviewed_source_commits") or {}).items():
            if pins.get(src) and pins[src] != commit:
                out.append(f"{x['connection_id']}: reviewed against {src}@{commit[:7]}, current pin {pins[src][:7]}; needs re-review")
    return out


def validate_connection(x: dict, R: Resolver, *, in_ledger: bool, root: Path) -> list[str]:
    cid = x.get("connection_id") or x.get("proposal_id")
    p = []
    status_field = "review_status" if in_ledger else "status"
    allowed = core.LEDGER_REVIEW_STATUSES if in_ledger else core.PROPOSAL_STATUSES
    if x.get(status_field) not in allowed:
        p.append(f"{cid}: {status_field} {x.get(status_field)!r} not allowed here")
    ctype = x.get("connection_type")
    if ctype not in core.CONNECTION_TYPES:
        p.append(f"{cid}: connection_type {ctype!r} is not a scientific connection type" + (" (it is a metaphor link type)" if ctype in core.METAPHOR_LINK_TYPES else ""))
    p += _no_scores(x, cid)
    ends = {}
    for end in ("from", "to"):
        ref = x.get(end, "")
        res = R.resolve(ref)
        ends[end] = res
        if not res["ok"]:
            if res.get("pending") and x.get(status_field) in ("under_review", "undetermined", "proposed"):
                continue  # pending historical/external pointers may sit in unresolved records only
            p.append(f"{cid}: {end} {ref}: {res['reason']}")
        elif res.get("kind") == "metaphor":
            p.append(f"{cid}: a metaphor cannot be an endpoint of a scientific connection")
    for ref in x.get("evidence_refs", []):
        if ref.startswith("M::"):
            p.append(f"{cid}: a metaphor cannot be cited as evidence ({ref})")
        if "discover" in ref:
            p.append(f"{cid}: discovery output cannot be cited as evidence ({ref})")
    if x.get("origin") == "discovery_candidate" and x.get(status_field) in ("agent_reviewed", "human_accepted") and not x.get("review", {}).get("record"):
        p.append(f"{cid}: a discovery candidate needs a written review before promotion")
    comp = x.get("comparison", {})
    promoted = x.get(status_field) in ("agent_reviewed", "human_accepted")
    if ctype in core.EVIDENTIAL_CONNECTION_TYPES and promoted:
        for dim in core.COMPARISON_DIMENSIONS:
            v = comp.get(dim, {}).get("verdict")
            if v not in ("same", "differs", "not_applicable"):
                p.append(f"{cid}: evidential type {ctype} needs a definite comparison verdict for {dim}")
        for end in ("from", "to"):
            if ends[end].get("source_status") == "catalogued_only":
                p.append(f"{cid}: evidential type cannot rest on a catalogued-only document ({x.get(end)})")
    for dim in comp:
        if dim not in core.COMPARISON_DIMENSIONS:
            p.append(f"{cid}: unknown comparison dimension {dim}")
    ind = x.get("independence")
    if ind not in core.INDEPENDENCE:
        p.append(f"{cid}: independence {ind!r} must be one of {sorted(core.INDEPENDENCE)}")
    sa, sb = ends["from"].get("source"), ends["to"].get("source")
    if sa and sb and sa != "shared" and sb != "shared" and lineage_shared(R.manifest, sa, sb):
        if ind == "independent" and not x.get("independence_note"):
            p.append(f"{cid}: endpoints share lineage ({sa}, {sb}); 'independent' needs an independence_note")
    if sa and sb and sa == sb and sa != "shared":
        if not x.get("within_programme"):
            p.append(f"{cid}: both endpoints are in {sa}; mark within_programme (a suggestion for that programme's own ledger)")
        if in_ledger:
            p.append(f"{cid}: the shared ledger holds cross-programme relations only; a within-programme relation belongs to {sa}'s own ledger")
    if ctype == "shared_implementation_assumption" and ind not in ("shared_lineage", "same_source"):
        p.append(f"{cid}: a shared implementation assumption is by definition not independent")
    if ctype == "untested_hypothesis" and not x.get("falsifiers"):
        p.append(f"{cid}: an untested hypothesis must state what would falsify it")
    st = x.get(status_field)
    if st in ("agent_reviewed", "human_accepted", "rejected", "undetermined"):
        rv = x.get("review", {})
        rec = rv.get("record")
        if not rv.get("reviewer") or not rec:
            p.append(f"{cid}: status {st} needs review.reviewer and review.record")
        elif not (root / rec).exists():
            p.append(f"{cid}: review record {rec} does not exist")
        if st == "human_accepted" and (not rv.get("human") or str(rv.get("reviewer", "")).lower().startswith("agent")):
            p.append(f"{cid}: human_accepted requires a named human reviewer")
    if in_ledger and st == "human_accepted":
        for end in ("from", "to"):
            if ends[end].get("source") == "HIST" and (ends[end].get("source_status") != "included_partial" or ends[end].get("pending")):
                p.append(f"{cid}: historical claims cannot be accepted before intake")
    for key in ("rationale", "scope"):
        if not x.get(key):
            p.append(f"{cid}: {key} is required")
    pending = any(ends[e].get("pending") for e in ("from", "to"))
    p += validate_decision(x, cid, status_field, [ends[e].get("node") for e in ("from", "to")], pending, R.manifest)
    if in_ledger:
        rsc = x.get("reviewed_source_commits")
        srcs = {ends[e].get("source") for e in ("from", "to")} - {None, "shared"}
        if not isinstance(rsc, dict) or not srcs <= set(rsc):
            p.append(f"{cid}: reviewed_source_commits must name the commit each endpoint source was reviewed at")
    return p


def validate_metaphor(m: dict, concept_ids: set) -> list[str]:
    mid = m.get("metaphor_id", "?")
    p = [f"{mid}: missing {f}" for f in core.METAPHOR_REQUIRED if f not in m]
    if m.get("evidentiary") is not False:
        p.append(f"{mid}: metaphors are non-evidentiary (evidentiary must be false)")
    if m.get("status") not in core.METAPHOR_STATUSES:
        p.append(f"{mid}: status {m.get('status')!r}")
    for c in m.get("concepts", []):
        if c not in concept_ids:
            p.append(f"{mid}: concept {c} not defined")
    for row in m.get("mapping", []):
        if not row.get("figure") or not row.get("object"):
            p.append(f"{mid}: each mapping row needs a figure and the mathematical object it stands for")
    text = " ".join([m.get("explanation", "")] + [r.get("figure", "") for r in m.get("mapping", [])]).lower()
    disclaimers = " ".join(m.get("does_not_mean", [])).lower()
    for term in core.SMUGGLING_TERMS:
        if term in text and term not in disclaimers:
            p.append(f"{mid}: uses '{term}' without disclaiming it in does_not_mean (metric/locality/agency/force must not be smuggled in)")
    if not m.get("misleading_readings"):
        p.append(f"{mid}: must list at least one misleading reading")
    if not m.get("useful_scope"):
        p.append(f"{mid}: useful scope missing (state where the metaphor helps and for whom)")
    p += _no_scores({k: v for k, v in m.items() if k != "illustrative_status"}, mid)
    return p


SEED_RELATION_MAP = {
    # author seed relation_type_proposed -> shared connection type (None: a question, not a connection)
    "compatible_with": "epistemic_compatibility",
    "contrasts_with": "explicit_contrast",
    "qualifies": "qualifies",
    "candidate_mechanism_analogy": "untested_hypothesis",
    "shared_question": None,
    "raises_shared_question": None,
}
DRAFT_FLAG_MARKERS = ("without disclaiming", "not defined", "misleading reading", "useful scope missing")


def split_draft_problems(problems: list[str]) -> tuple[list[str], list[str]]:
    """For drafts, semantic issues are review flags; structural issues stay errors."""
    flags = [x for x in problems if any(m in x for m in DRAFT_FLAG_MARKERS)]
    return [x for x in problems if x not in flags], flags


def validate_seed_claim(x: dict, R: "Resolver") -> list[str]:
    """An author seed claim (multi-source). Kept verbatim; never a ledger connection until reviewed and restated."""
    pid = x.get("proposal_id", "?")
    p = []
    if x.get("origin") != "author_seed" or not isinstance(x.get("seed_record"), dict):
        p.append(f"{pid}: a seed claim keeps origin author_seed and its verbatim seed_record")
    if x.get("status") not in ("proposed", "under_review", "rejected", "undetermined"):
        p.append(f"{pid}: a seed claim cannot be promoted directly; restate it as a pairwise connection and review that")
    if x.get("relation_type_proposed") not in SEED_RELATION_MAP:
        p.append(f"{pid}: unmapped seed relation type {x.get('relation_type_proposed')!r}")
    else:
        ov = x.get("relation_override")
        if ov:
            # the only exception to the seed mapping: a recorded human (author) decision
            if not ov.get("human") or str(ov.get("decided_by", "")).lower().startswith("agent") or ov.get("to") not in core.CONNECTION_TYPES:
                p.append(f"{pid}: a relation_override must be a recorded human decision naming a shared connection type")
            elif x.get("connection_type") != ov.get("to"):
                p.append(f"{pid}: connection_type must equal the author's relation_override")
            elif ov.get("from") != x.get("relation_type_proposed"):
                p.append(f"{pid}: relation_override.from must name the seed's proposed relation type")
            if not any(h.get("human") and h.get("date") == ov.get("date") for h in x.get("decision_history", [])):
                p.append(f"{pid}: a relation_override needs a matching human entry in decision_history")
        elif x.get("connection_type") != SEED_RELATION_MAP[x["relation_type_proposed"]]:
            p.append(f"{pid}: connection_type does not follow the declared seed mapping")
    nodes, pending = [], False
    for ref in x.get("sources", []):
        res = R.resolve(ref)
        pending |= bool(res.get("pending"))
        nodes.append(res.get("node"))
        if not res["ok"] and not res.get("pending"):
            p.append(f"{pid}: source {ref}: {res['reason']}")
    p += _no_scores(x, pid)
    p += validate_decision(x, pid, "status", nodes, pending, R.manifest)
    return p


def validate_external_claim(x: dict, R: "Resolver", root: Path) -> list[str]:
    """A claim registered from an external synthesis: verbatim quote, agent-labelled mapping, never promoted directly."""
    pid = x.get("proposal_id", "?")
    p = []
    if x.get("origin") != "external_synthesis" or not str(x.get("provenance_ref", "")).startswith("EXT::"):
        p.append(f"{pid}: an external claim keeps origin external_synthesis and an EXT:: provenance_ref")
    if x.get("source_mapping") != "agent":
        p.append(f"{pid}: the mapping of cited items to ids must be labelled source_mapping: agent")
    if x.get("connection_type") is not None:
        p.append(f"{pid}: an external claim is not a connection (connection_type must be null)")
    if x.get("status") not in ("proposed", "under_review", "rejected", "undetermined"):
        p.append(f"{pid}: an external claim cannot be promoted directly; restate it as pairwise proposals and review those")
    doc = None
    for src in R.manifest["sources"]:
        if src["namespace"] == "EXT":
            for a in src.get("artifacts", []):
                f = core.REPO / a["path"]
                if f.exists():
                    doc = f.read_text(encoding="utf-8")
    if not x.get("quote") or doc is None or x["quote"] not in doc:
        p.append(f"{pid}: quote must appear verbatim in the stored external document")
    nodes, pending = [], False
    for ref in x.get("sources", []):
        res = R.resolve(ref)
        pending |= bool(res.get("pending"))
        nodes.append(res.get("node"))
        if not res["ok"] and not res.get("pending"):
            p.append(f"{pid}: source {ref}: {res['reason']}")
    p += _no_scores(x, pid)
    p += validate_decision(x, pid, "status", nodes, pending, R.manifest)
    return p


def validate_metaphor_link(link: dict, ids: dict) -> list[str]:
    lid = link.get("link_id", "?")
    t = link.get("link_type")
    p = []
    if t not in core.METAPHOR_LINK_TYPES:
        p.append(f"{lid}: {t!r} is not a metaphor link type" + (" (scientific connection types are not allowed here)" if t in core.CONNECTION_TYPES else ""))
        return p
    frm, to = link.get("from", ""), link.get("to", "")
    if ids.get(frm) != "metaphor":
        p.append(f"{lid}: metaphor links start at a metaphor ({frm})")
    want = {"covers_concept": {"concept"}, "illustrates_relation": {"connection"}, "bridges_metaphors": {"metaphor"}, "complements": {"metaphor"}, "conflicts_with": {"metaphor"}, "fails_for": {"concept", "connection", "source_finding", "formal_claim"}, "requires_qualification": {"concept", "connection", "source_finding", "formal_claim"}}[t]
    if ids.get(to) not in want:
        p.append(f"{lid}: {t} must point to {sorted(want)}, not {ids.get(to)} ({to})")
    if not link.get("note"):
        p.append(f"{lid}: a note is required")
    for f in ("supports", "evidence_refs", "review_status"):
        if f in link:
            p.append(f"{lid}: field {f} belongs to the scientific graph, not to metaphor links")
    return p


def validate_all(manifest: dict, loaded: dict, shared: dict, root: Path | None = None) -> list[str]:
    root = root or core.ROOT
    p = []
    R = Resolver(manifest, loaded["nodes"], shared)
    seen = set()
    for group, key in (("concepts", "concept_id"), ("connections", "connection_id"), ("questions", "question_id"), ("metaphors", "metaphor_id"), ("metaphor_links", "link_id"), ("proposals", "proposal_id"), ("metaphor_drafts", "metaphor_id")):
        for r in shared[group]:
            rid = r.get(key)
            want_ns = {"concepts": "C", "connections": "X", "questions": "XQ", "metaphors": "M", "metaphor_drafts": "M", "proposals": "P", "metaphor_links": "ML"}[group]
            if not rid or not str(rid).startswith(want_ns + "::"):
                p.append(f"{group}: id {rid!r} must use namespace {want_ns}::")
            if (group, rid) in seen or (group in ("metaphors", "metaphor_drafts") and ("metaphors" if group == "metaphor_drafts" else "metaphor_drafts", rid) in seen):
                p.append(f"{group}: duplicate id {rid}")
            seen.add((group, rid))
    concept_ids = {c["concept_id"] for c in shared["concepts"]}
    for c in shared["concepts"]:
        for ref in c.get("anchors", []):
            res = R.resolve(ref)
            if not res["ok"] and not res.get("pending"):
                p.append(f"{c['concept_id']}: anchor {ref}: {res['reason']}")
        if not c.get("definition") or not c.get("plain_definition"):
            p.append(f"{c['concept_id']}: definition and plain_definition are required")
    for x in shared["connections"]:
        p += validate_connection(x, R, in_ledger=True, root=root)
    for x in shared["proposals"]:
        if x.get("kind") == "seed_claim":
            p += validate_seed_claim(x, R)
            continue
        if x.get("kind") == "external_claim":
            p += validate_external_claim(x, R, root)
            continue
        p += validate_connection(x, R, in_ledger=False, root=root)
        if not x.get("decision_rationale") and x.get("status") in ("rejected", "undetermined"):
            p.append(f"{x['proposal_id']}: rejected/undetermined proposals keep their rationale")
    for q in shared["questions"]:
        if q.get("status") not in core.QUESTION_STATUSES:
            p.append(f"{q.get('question_id')}: status {q.get('status')!r}")
        for ref in q.get("refs", []):
            res = R.resolve(ref)
            if not res["ok"] and not (res.get("pending") and q.get("status") == "pending_source"):
                if res.get("pending"):
                    p.append(f"{q['question_id']}: pending source {ref} requires status pending_source")
                else:
                    p.append(f"{q['question_id']}: {ref}: {res['reason']}")
        if not q.get("discriminating_tests"):
            p.append(f"{q.get('question_id')}: at least one candidate discriminating test is required")
    for m in shared["metaphors"]:
        p += validate_metaphor(m, concept_ids)
    for m in shared["metaphor_drafts"]:
        errors, _flags = split_draft_problems(validate_metaphor(m, concept_ids))
        p += errors
    for m in shared["metaphors"]:
        if m.get("status") == "draft":
            p.append(f"{m['metaphor_id']}: drafts belong in proposals/metaphor-drafts.jsonl")
    ids = dict(R.shared_ids)
    ids.update({k: v["kind"] for k, v in loaded["nodes"].items()})
    for link in shared["metaphor_links"]:
        p += validate_metaphor_link(link, ids)
    return p


# --- graph projection ---------------------------------------------------------------------


def project_graph(manifest: dict, loaded: dict, shared: dict) -> dict:
    """The federated, reader-facing projection. Deterministic. Never authoritative."""
    nodes = {}
    for k, v in loaded["nodes"].items():
        src = sources.sources_by_key(manifest).get(v["source"], {})
        nodes[k] = {"id": k, **v, "source_commit": src.get("commit"), "unreviewed_round": unreviewed_round(manifest, v)}
    for c in shared["concepts"]:
        nodes[c["concept_id"]] = {"id": c["concept_id"], "kind": "concept", "label": c["label"], "status": c.get("status"), "epistemic_layer": "SHARED_CONCEPT"}
    for q in shared["questions"]:
        nodes[q["question_id"]] = {"id": q["question_id"], "kind": "shared_question", "label": q["statement"], "status": q["status"], "epistemic_layer": "OPEN_QUESTION"}
    for m in shared["metaphors"]:
        nodes[m["metaphor_id"]] = {"id": m["metaphor_id"], "kind": "metaphor", "label": m["title"], "status": m["status"], "epistemic_layer": "METAPHOR_NON_EVIDENTIARY"}
    for s in manifest["sources"]:
        sid = f"SOURCE::{s['source_key']}"
        nodes[sid] = {"id": sid, "kind": "source", "label": s["programme"], "status": s["status"], "commit": s.get("commit"), "branch": s.get("branch"), "epistemic_layer": "PROVENANCE"}
    scientific = [dict(e) for e in loaded["edges"]]
    for x in shared["connections"]:
        scientific.append({"kind": "cross_programme_connection", "id": x["connection_id"], "from": x["from"], "to": x["to"], "type": x["connection_type"], "review_status": x["review_status"], "independence": x["independence"]})
    metaphor = [{"kind": "metaphor_link", "id": link["link_id"], "from": link["from"], "to": link["to"], "type": link["link_type"]} for link in shared["metaphor_links"]]
    provenance = []
    for s in manifest["sources"]:
        for lin in s.get("lineage", []):
            provenance.append({"kind": "lineage", "from": f"SOURCE::{s['source_key']}", "to": f"SOURCE::{lin['target']}", "type": lin["relation"], "note": lin["what"]})
    for k, v in loaded["nodes"].items():
        provenance.append({"kind": "membership", "from": k, "to": f"SOURCE::{v['source']}", "type": "recorded_in"})
    key = lambda e: (e["kind"], e.get("id") or "", e["from"], e["to"], e["type"])
    return {
        "schema": "rssynth.graph/v1",
        "nodes": [nodes[k] for k in sorted(nodes)],
        "scientific_edges": sorted(scientific, key=key),
        "metaphor_edges": sorted(metaphor, key=key),
        "provenance_edges": sorted(provenance, key=key),
        "note": "Federated projection. Programme ledgers are authoritative; metaphor edges are non-evidentiary and never alter a node's status.",
    }
