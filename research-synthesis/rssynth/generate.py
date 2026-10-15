"""Deterministic generated views: front page, thematic projections, Mermaid and JSON.

Inputs: the pinned manifest, the adapters' projection of the pinned source
ledgers and the shared records. No timestamps, no environment-dependent
values; regenerating from the same inputs gives byte-identical files.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from . import core, ledger, sources

def gen_dir():
    return core.ROOT / "generated"
STATUS_TEXT = {"agent_reviewed": "AGENT-REVIEWED (awaiting human acceptance)", "human_accepted": "HUMAN-ACCEPTED (at the stated decision category)", "rejected": "REJECTED", "undetermined": "UNDETERMINED", "under_review": "UNDER REVIEW", "proposed": "PROPOSED (unreviewed)"}


def short(text: str, n: int = 140) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[: n - 1] + "…"


def esc(text: str) -> str:
    return str(text).replace("|", "\\|")


def mm(text: str) -> str:
    return '"' + short(text, 60).replace('"', "'") + '"'


def mid(ref: str) -> str:
    return "n_" + "".join(ch if ch.isalnum() else "_" for ch in ref)


def label(ref: str, nodes: dict) -> str:
    n = nodes.get(ref)
    if n is None:
        return ref
    return n.get("title") or n.get("label") or short(n.get("statement", ""), 70)


def build(manifest: dict, loaded: dict, shared: dict, discovery: dict | None) -> dict[str, str]:
    """Return {relative path: content}. Pure function of its inputs."""
    nodes = dict(loaded["nodes"])
    for c in shared["concepts"]:
        nodes[c["concept_id"]] = {"kind": "concept", "label": c["label"]}
    for q in shared["questions"]:
        nodes[q["question_id"]] = {"kind": "shared_question", "label": q["statement"]}
    for m in shared["metaphors"]:
        nodes[m["metaphor_id"]] = {"kind": "metaphor", "label": m["title"]}
    for x in shared["connections"]:
        nodes[x["connection_id"]] = {"kind": "connection", "label": f"{x['connection_type']} {x['from']} → {x['to']}"}
    files: dict[str, str] = {}
    graph = ledger.project_graph(manifest, loaded, shared)
    graph["shared_records"] = {k: sorted(shared[k], key=lambda r: core.canonical(r)) for k in ("concepts", "connections", "questions", "metaphors", "metaphor_links", "proposals", "metaphor_drafts")}
    graph["sources"] = manifest["sources"]
    graph["historical"] = {"findings": sorted(shared.get("hist_findings", []), key=lambda r: r.get("finding_id", "")), "intake_plan": shared.get("hist_intake_plan", {})}
    files["graph.json"] = core.canonical(graph) + "\n"

    # ---- provenance ---------------------------------------------------------------
    P = ["# Provenance and source dependence", "", "Generated view. Programme ledgers are authoritative in their own branches; the shared layer reads them at the pins below. **Local tree** says whether the path exists in this branch's checked-out tree; programme files do not, and are read from git objects or from the non-authoritative materialised copies under `sources/materialised/`.", ""]
    P += ["| Source | Programme | Role | Status | Branch | Pinned commit | Round boundary |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for s in manifest["sources"]:
        P.append(f"| `{s['source_key']}` ({s['namespace']}::) | {esc(s['programme'])} | {s['role']} | **{s['status'].upper()}** | `{s.get('branch') or '—'}` | `{(s.get('commit') or '—')[:12]}` | {esc(s.get('round_boundary') or s.get('note') or '—')} |")
    P += ["", "## Reviewed pins, schemas and round review state", "", "`commit` is the **reviewed source commit**. Moving branch heads are reported by `synth audit` and `synth check` (staleness) and are never substituted for a pin.", "", "| Source | Reviewed source commit | Source schema (validator blob) | Closed but unreviewed rounds | Note |", "| --- | --- | --- | --- | --- |"]
    for s in manifest["sources"]:
        sch = s.get("source_schema", {}).get("validator_git_blob")
        P.append(f"| `{s['source_key']}` | `{(s.get('reviewed_source_commit') or '—')[:12]}` | `{(sch or '—')[:12]}` | {', '.join(s.get('unreviewed_generations', [])) or '—'} | {esc(s.get('review_note', ''))} |")
    P += ["", "## Artifacts at the pins", "", "| Source | Path | Kind | sha256 | Materialised copy | Local tree |", "| --- | --- | --- | --- | --- | --- |"]
    for s in manifest["sources"]:
        for a in s.get("artifacts", []):
            local = "present" if (core.REPO / a["path"]).exists() else "ABSENT (not tracked on this branch)"
            P.append(f"| `{s['source_key']}` | `{a['path']}` | {a['kind']} | `{a['sha256'][:12]}…` | {'yes' if a.get('materialised') else 'no (pointer only)'} | {local} |")
    P += ["", "## Lineage", "", "Shared lineage means agreement on inherited code, kernels or validators is not independent evidence.", ""]
    for s in manifest["sources"]:
        for lin in s.get("lineage", []):
            P.append(f"- `{s['source_key']}` **{lin['relation']}** `{lin['target']}`: {lin['what']}")
    P += ["", "## Adapter reports", "", "| Source | Counts | Problems |", "| --- | --- | --- |"]
    for k in sorted(loaded["reports"]):
        r = loaded["reports"][k]
        P.append(f"| `{k}` | {', '.join(f'{a}: {n}' for a, n in sorted(r['counts'].items())) or '—'} | {len(r['problems'])} |")
    files["provenance.md"] = "\n".join(P) + "\n"
    M = ["graph LR"]
    for s in manifest["sources"]:
        M.append(f"  {mid(s['source_key'])}[{mm(s['source_key'] + ' — ' + s['status'] + ' @ ' + (s.get('commit') or 'none')[:7])}]:::{s['status']}")
    for s in manifest["sources"]:
        for lin in s.get("lineage", []):
            M.append(f"  {mid(s['source_key'])} -->|{lin['relation']}| {mid(lin['target'])}")
    M += ["  classDef included fill:#d8f0d8,stroke:#2a7a2a", "  classDef catalogued_only fill:#e6eefc,stroke:#2a4a8a", "  classDef lineage_only fill:#f2f2f2,stroke:#555", "  classDef missing fill:#fde2e2,stroke:#a33,stroke-dasharray: 4 3", "  classDef pending_intake fill:#fff4d6,stroke:#a07a00,stroke-dasharray: 4 3"]
    files["provenance.mmd"] = "\n".join(M) + "\n"

    # ---- links ----------------------------------------------------------------------
    conns = sorted(shared["connections"], key=lambda x: x["connection_id"])
    L = ["# Cross-programme connections", "", "Only records in `ledger/connections.jsonl`. Every one carries an explicit review status. Human acceptance is implicit in the round trip (`docs/cadence.md`): it accepts a reported recommendation at its stated decision category and never upgrades it. Evidential types compare formal objects on eight dimensions (see each review record). Independence is stated because GT and CL share 8G lineage.", ""]
    def unrev(x):
        return any(ledger.unreviewed_round(manifest, loaded["nodes"].get(x[e])) for e in ("from", "to"))

    L += ["**Decision category** is the category the agent recommended (rubric 03); human acceptance keeps it. **Review status** says who has reviewed it. A connection resting on a closed but **unreviewed** round (CL 008N, GT-P009) is marked and stays `qualified` (or `candidate`) even when human-accepted.", ""]
    L += ["| Id | Type | From | To | Decision | Review status | Rests on unreviewed round | Independence | Review record |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for x in conns:
        L.append(f"| {x['connection_id']} | {x['connection_type']} | `{x['from']}` | `{x['to']}` | {x['decision_category'].upper()} | {STATUS_TEXT.get(x['review_status'], x['review_status'])} | {'YES' if unrev(x) else 'no'} | {x['independence']} | [{x['review']['record'].split('/')[-1]}](../{x['review']['record']}) |")
    L += ["", "## Rationale", ""]
    for x in conns:
        L += [f"**{x['connection_id']}** ({x['connection_type']}; {STATUS_TEXT.get(x['review_status'])}). {x['rationale']}", ""]
    files["links.md"] = "\n".join(L) + "\n"
    M = ["graph LR"]
    used = set()
    for x in conns:
        for r in (x["from"], x["to"]):
            if r not in used:
                used.add(r)
                M.append(f"  {mid(r)}[{mm(r)}]")
        M.append(f"  {mid(x['from'])} -->|{x['connection_type']} · {x['review_status']}| {mid(x['to'])}")
    files["links.mmd"] = "\n".join(M) + "\n"

    # ---- contradictions and nulls ---------------------------------------------------
    C = ["# Contradictions, contrasts and qualifications", "", "Disagreement is kept as visible as agreement. Programme negative and null findings are in [nulls.md](nulls.md).", "", "## Cross-programme contrasts and qualifications", ""]
    for x in conns:
        if x["connection_type"] in ("explicit_contrast", "qualifies", "supersedes_interpretation"):
            C.append(f"- **{x['connection_id']}** {x['connection_type']}: `{x['from']}` / `{x['to']}`: {short(x['rationale'], 400)}")
    C += ["", "## Rejected and undetermined proposals (kept with rationale)", ""]
    for p in sorted(shared["proposals"], key=lambda p: p["proposal_id"]):
        if p["status"] in ("rejected", "undetermined") and "from" in p:
            C.append(f"- **{p['proposal_id']}** {STATUS_TEXT[p['status']]}: `{p['from']}` → `{p['to']}` ({p['connection_type']}). {short(p.get('decision_rationale', ''), 400)}")
    overrides = sorted((p for p in shared["proposals"] if p.get("relation_override")), key=lambda p: p["proposal_id"])
    C += ["", "## Author decisions on relation types", ""]
    C += [f"- `{p['proposal_id']}`: the seed proposed `{p['relation_override']['from']}`; the author classified it as **`{p['relation_override']['to']}`**" + (f", matching `{p['relation_override']['matches']}`" if p['relation_override'].get('matches') else "") + f" ({p['relation_override']['date']}). {p['relation_override']['rationale']}" for p in overrides] or ["- none"]
    C.append("")
    N = ["# Nulls, negative findings and qualified findings", "", "Negative results are evidence too. Statements are abbreviated; the pinned ledgers are authoritative.", "", "## Negative findings recorded by the programmes", "", "Findings whose structural roles include `negative_finding`, by source.", ""]
    for src in ("CL", "GT"):
        neg = sorted(k for k, v in loaded["nodes"].items() if v.get("source") == src and "negative_finding" in (v.get("structural_roles") or []))
        N.append(f"**{src}** ({len(neg)}):")
        N += [f"- `{k}` [{loaded['nodes'][k]['status']}]: {short(loaded['nodes'][k]['statement'])}" for k in neg]
        N.append("")
    N += ["## Qualified or superseded programme findings", ""]
    for src in ("CL", "GT"):
        q = sorted(k for k, v in loaded["nodes"].items() if v.get("source") == src and v.get("status") in ("qualified", "superseded") and v["kind"] != "formal_claim")
        N.append(f"- **{src}**: {len(q)}: " + ", ".join(f"`{k}`" for k in q))
    N += ["", "## Rejected false-attractor controls (rubric 03)", ""]
    for p in sorted(shared["proposals"], key=lambda p: p["proposal_id"]):
        if p.get("false_attractor_control"):
            N.append(f"- **{p['proposal_id']}** REJECTED: {p['rationale']} {short(p['decision_rationale'], 400)}")
    files["contradictions.md"] = "\n".join(C) + "\n"
    files["nulls.md"] = "\n".join(N) + "\n"

    # ---- questions --------------------------------------------------------------------
    Q = ["# Open questions and discriminating tests", "", "Shared cross-programme questions (`ledger/questions.jsonl`). No test listed here is authorised by this layer; each needs its programme's own frozen plan.", ""]
    for q in sorted(shared["questions"], key=lambda q: q["question_id"]):
        Q += [f"## {q['question_id']}: {q['statement']}", "", f"Status: **{q['status'].upper()}**. Refs: " + ", ".join(f"`{r}`" for r in q["refs"]), ""]
        for t in q["discriminating_tests"]:
            Q.append(f"- Test ({t['status']}): {t['test']}. Would show: {t['would_show']}.")
        if q.get("notes"):
            Q.append(f"- Note: {q['notes']}")
        Q.append("")
    Q += ["## Programme open questions (unresolved, from the pinned ledgers)", ""]
    for src in ("CL", "GT"):
        oq = sorted(k for k, v in loaded["nodes"].items() if v.get("source") == src and v["kind"] == "source_question" and v.get("status") == "unresolved")
        Q.append(f"- **{src}** ({len(oq)}): " + ", ".join(f"`{k}`" for k in oq))
    files["questions.md"] = "\n".join(Q) + "\n"

    # ---- candidate bridges --------------------------------------------------------------
    B = ["# Candidate bridges (proposals)", "", "Staged in `proposals/`; none is in the ledger. Status is shown in text.", "", "## Pairwise proposals", "", "| Id | Type | From | To | Status | Origin |", "| --- | --- | --- | --- | --- | --- |"]
    for p in sorted(shared["proposals"], key=lambda p: p["proposal_id"]):
        if p.get("kind") not in ("seed_claim", "external_claim"):
            origin = p["origin"] + (" · WITHIN-PROGRAMME (upstream suggestion; not promotable here)" if p.get("within_programme") else "") + (f" · from {p['derived_from_claim']}" if p.get("derived_from_claim") else "")
            B.append(f"| {p['proposal_id']} | {p['connection_type']} | `{p['from']}` | `{p['to']}` | {STATUS_TEXT[p['status']]} | {origin} |")
    seeds = sorted((p for p in shared["proposals"] if p.get("kind") == "seed_claim"), key=lambda p: p["proposal_id"])
    if seeds:
        B += ["", "## Author seed claims (multi-source; unapproved)", "", "Kept verbatim (`seed_record`). The seed's relation type is mapped conservatively: question-type relations map to no connection type, and an analogy maps to `untested_hypothesis` until a formal comparison is reviewed. A seed claim enters the ledger only after it is restated as pairwise connections and reviewed.", ""]
        for p in seeds:
            refs = ", ".join(f"`{r}`" for r in p["sources"])
            B += [f"### {p['proposal_id']}: {p['theme']} ({STATUS_TEXT[p['status']]})", "", f"- **Claim:** {p['claim']}", f"- **Cannot infer:** {p['cannot_infer']}", f"- **Discriminator:** {p['discriminator']}", f"- **Proposed relation:** `{p['relation_type_proposed']}` → mapped to `{p['connection_type']}`", f"- **Seed review status:** `{p['seed_review_status']}`" + (" (blocked on historical primary sources)" if p.get("blocked_on_historical_primary") else ""), f"- **Sources:** {refs}", ""]
    if discovery:
        B += ["", "## Retrieval diagnostics (not evidence)", "", f"{discovery['score_meaning']}", "", "Calibration: similarity and rank of reviewed connections among all cross-programme pairs:", ""]
        for c in discovery["reviewed_connection_calibration"]:
            B.append(f"- {c['connection_id']} ({c['connection_type']}): similarity {c['similarity']:.3f}, rank {c['rank_among_cross_pairs'] or 'unranked (no shared terms)'} of {c['cross_pairs']}")
        B += ["", "Top 10 unreviewed retrieval candidates:", ""]
        for c in discovery["candidates"][:10]:
            B.append(f"- {c['similarity']:.3f} `{c['from']}` ↔ `{c['to']}` (shared terms: {', '.join(c['shared_terms'][:5])}){' [' + ', '.join(c['flags']) + ']' if c['flags'] else ''}")
    ext = sorted((p for p in shared["proposals"] if p.get("kind") == "external_claim"), key=lambda p: p["proposal_id"])
    if ext:
        B += ["", "## Claims registered from the external 2026-10-15 synthesis (unapproved)", "", "Quoted verbatim from `reports/external-2026-10-15-cross-research-synthesis.md` (an exploratory synthesis; its cosines are retrieval measures). The mapping of cited items to pinned ids is the agent's (`source_mapping: agent`). Claims resting on private historical archives are `blocked_missing_source`. None is reviewed.", ""]
        for p in ext:
            B += [f"### {p['proposal_id']} ({p['section']}; {p['decision_category'].upper()}; {STATUS_TEXT.get(p['status'], p['status'])})", "", f"> {p['quote']}", "", f"- **Cited (as written):** {'; '.join(p['cited_as'])}"]
            if p.get("check_outcome"):
                B.append(f"- **Check against pinned records:** {p['check_outcome'].replace('_', ' ').upper()}. {p['check_note']}")
                if p.get("upstream_relations"):
                    B.append(f"- **Already related in the programme's ledger:** {', '.join(p['upstream_relations'])}")
                if p.get("restated_as"):
                    B.append(f"- **Restated as:** {', '.join(f'`{r}`' for r in p['restated_as'])}")
            if p.get("synthesis_assessment"):
                B.append(f"- **Synthesis's own assessment:** {p['synthesis_assessment']}")
            B.append(f"- **Mapped sources (agent):** {', '.join(f'`{r}`' for r in p['sources'])}")
            if p.get("unresolved_citations"):
                B.append(f"- **Unresolved citations:** {'; '.join(p['unresolved_citations'])}")
            if p.get("overlaps"):
                B.append(f"- **Overlaps:** {', '.join(f'`{o}`' for o in p['overlaps'])}")
            B += [f"- **Note:** {n}" for n in p.get("context_notes", [])[:-1]]
            B.append("")
        B += [f"*{ext[0]['context_notes'][-1]}*", ""]
    R = ledger.Resolver(manifest, loaded["nodes"], shared)
    unresolved = []
    for rec in shared["proposals"] + shared["questions"]:
        rid = rec.get("proposal_id") or rec.get("question_id")
        refs = rec.get("sources") or rec.get("refs") or [rec.get("from"), rec.get("to")]
        for ref in refs:
            if ref:
                res = R.resolve(ref)
                if not res["ok"]:
                    unresolved.append(f"- `{rid}` → `{ref}`: {res['reason']}")
    B += ["", "## Review diagnostics: unresolved references (staged, never shown as agreement)", ""] + (sorted(set(unresolved)) or ["- none"])
    files["candidate-bridges.md"] = "\n".join(B) + "\n"

    # ---- metaphors -------------------------------------------------------------------------
    links = sorted(shared["metaphor_links"], key=lambda link: link["link_id"])
    covers = defaultdict(list)
    for link in links:
        if link["link_type"] == "covers_concept":
            covers[link["to"]].append(link["from"])
    concepts = sorted(shared["concepts"], key=lambda c: c["concept_id"])
    MC = ["# Metaphor coverage", "", "Metaphors are explanations, **never evidence**. A metaphor's status never changes a finding's or connection's status. Each metaphor states what it does not mean.", "", "| Concept | Plain definition | Reviewed metaphors |", "| --- | --- | --- |"]
    for c in concepts:
        MC.append(f"| `{c['concept_id']}` {esc(c['label'])} | {esc(c['plain_definition'])} | {', '.join(f'`{m}`' for m in sorted(covers.get(c['concept_id'], []))) or '**none**'} |")
    MC += ["", "## The metaphors", ""]
    for m in sorted(shared["metaphors"], key=lambda m: m["metaphor_id"]):
        MC += [f"### {m['title']} (`{m['metaphor_id']}`; {m['status']}, non-evidentiary)", "", m["explanation"], "", "| In the picture | Stands for |", "| --- | --- |"]
        MC += [f"| {esc(r['figure'])} | {esc(r['object'])} |" for r in m["mapping"]]
        MC += ["", f"**Audience:** {m['audience']}. **Useful scope:** {m.get('useful_scope', 'not stated')}", "", "**It does not mean:** " + "; ".join(m["does_not_mean"]) + ".", "", "**Misleading readings:** " + "; ".join(m["misleading_readings"]) + ".", ""]
    files["metaphor-coverage.md"] = "\n".join(MC) + "\n"
    MO = ["# Overlapping metaphor coverage", "", "Concepts explained by more than one metaphor, and how metaphors relate to each other (complements, bridges, conflicts).", ""]
    for c in concepts:
        ms = sorted(covers.get(c["concept_id"], []))
        if len(ms) > 1:
            MO.append(f"- `{c['concept_id']}`: {', '.join(f'`{m}`' for m in ms)}")
    MO += ["", "| Link | Type | From | To | Note |", "| --- | --- | --- | --- | --- |"]
    for link in links:
        if link["link_type"] in ("complements", "conflicts_with", "bridges_metaphors"):
            MO.append(f"| {link['link_id']} | {link['link_type']} | `{link['from']}` | `{link['to']}` | {esc(link['note'])} |")
    MO += ["", "## Failures and required qualifications", ""]
    for link in links:
        if link["link_type"] in ("fails_for", "requires_qualification"):
            MO.append(f"- `{link['from']}` **{link['link_type']}** `{link['to']}`: {link['note']}")
    files["metaphor-overlap.md"] = "\n".join(MO) + "\n"
    illustrated = {link["to"] for link in links if link["link_type"] == "illustrates_relation"}
    MG = ["# Metaphor gaps: concepts and relations without an explanation", "", "## Concepts with no reviewed metaphor", ""]
    MG += [f"- `{c['concept_id']}` {c['label']}: {c['plain_definition']}" for c in concepts if not covers.get(c["concept_id"])]
    MG += ["", "## Connections with no illustrating metaphor", ""]
    MG += [f"- `{x['connection_id']}` {x['connection_type']} (`{x['from']}` → `{x['to']}`)" for x in conns if x["connection_id"] not in illustrated]
    MG += ["", "## Draft metaphors awaiting review (not counted as coverage)", ""]
    concept_ids = {c["concept_id"] for c in concepts}
    for m in sorted(shared["metaphor_drafts"], key=lambda m: m["metaphor_id"]):
        _, flags = ledger.split_draft_problems(ledger.validate_metaphor(m, concept_ids))
        line = f"- `{m['metaphor_id']}` {m['title']} ({m.get('origin', '')}) → {', '.join(m['concepts']) or 'no mapped concept'}"
        if m.get("unmapped_concept_targets"):
            line += f"; unmapped seed targets: {', '.join(m['unmapped_concept_targets'])}"
        MG.append(line)
        MG += [f"  - review flag: {f.split(': ', 1)[1]}" for f in flags]
    unmapped = sorted({t for m in shared["metaphor_drafts"] for t in m.get("unmapped_concept_targets", [])})
    if unmapped:
        MG += ["", "## Seed concept targets with no shared concept yet", "", "Candidates for new concepts, or for mapping by the author. Not created automatically.", ""] + [f"- `{t}`" for t in unmapped]
    MG += ["", "## Metaphors that overreach or need qualification", "", "Reviewed metaphors with recorded failures or qualifications. Drafts' review flags are listed above."]
    for link in links:
        if link["link_type"] in ("fails_for", "requires_qualification"):
            MG.append(f"- `{link['from']}` {link['link_type'].replace('_', ' ')} `{link['to']}`: {link['note']}")
    MG += ["", "Coverage counts are not evidence: several metaphors explaining one concept add nothing to any finding's support."]
    files["metaphor-gaps.md"] = "\n".join(MG) + "\n"
    MM = ["graph LR"]
    seen = set()
    for link in links:
        for r in (link["from"], link["to"]):
            if r not in seen:
                seen.add(r)
                shape = "([" + mm(r + " " + label(r, nodes)) + "])" if r.startswith("M::") else "[" + mm(r) + "]"
                MM.append(f"  {mid(r)}{shape}")
        MM.append(f"  {mid(link['from'])} -.->|{link['link_type']}| {mid(link['to'])}")
    MM.append("  %% dotted edges: metaphor layer only (non-evidentiary)")
    files["metaphor-links.mmd"] = "\n".join(MM) + "\n"

    # ---- chronology ---------------------------------------------------------------------------
    CH = ["# Chronology of change", "", "Order of first appearance of each programme generation in the pinned ledgers, then the shared layer's own records.", ""]
    for src in ("CL", "GT"):
        rows = [v for v in loaded["nodes"].values() if v.get("source") == src and v["kind"] != "formal_claim"]
        gens = Counter(str(v.get("created_generation")) for v in rows)
        order = list(dict.fromkeys(str(v.get("created_generation")) for v in rows))  # ledger row order = first appearance
        CH.append(f"**{src}** findings by generation, in order of first appearance: " + ", ".join(f"{g} ({gens[g]})" for g in order))
        CH.append("")
    CH += ["**Shared layer**:", ""]
    events = Counter((h["date"], h["status"].replace("_", "-"), "human" if h.get("human") else "agent") for x in shared["connections"] for h in x.get("decision_history", []))
    for (d, st, who), n in sorted(events.items()):
        CH.append(f"- {d}: {n} connection decisions {st} ({who})")
    snaps = sorted(p.name for p in (core.ROOT / "snapshots").glob("*") if p.is_dir()) if (core.ROOT / "snapshots").exists() else []
    CH += ["", "Snapshots: " + (", ".join(f"`{s}`" for s in snaps) or "none yet"), ""]
    pins = sorted(p.name for p in (core.ROOT / "proposals" / "pin-updates").glob("*.json")) if (core.ROOT / "proposals" / "pin-updates").exists() else []
    CH += ["Pin-update proposals: " + (", ".join(f"`{p}`" for p in pins) or "none yet")]
    files["chronology.md"] = "\n".join(CH) + "\n"

    # ---- themes ---------------------------------------------------------------------------------
    for c in concepts:
        cid = c["concept_id"]
        anchors = c.get("anchors", [])
        T = [f"# Theme: {c['label']}", "", f"`{cid}` ({c['kind']}, {c['status']})", "", f"**Definition.** {c['definition']}", "", f"**In plain words.** {c['plain_definition']}", "", "## Anchoring findings (pinned sources)", ""]
        for r in anchors:
            n = loaded["nodes"].get(r)
            T.append(f"- `{r}` [{n['kind']}, {n['epistemic_layer']}, {n['status']}]: {short(n['statement'], 220)}" if n else f"- `{r}`: unresolved")
        rel = [x for x in conns if x["from"] in anchors or x["to"] in anchors]
        T += ["", "## Connections touching this theme", ""]
        T += [f"- {x['connection_id']} {x['connection_type']} ({STATUS_TEXT[x['review_status']]}): `{x['from']}` → `{x['to']}`" for x in rel] or ["- none"]
        qs = [q for q in shared["questions"] if cid in q["refs"] or set(q["refs"]) & set(anchors)]
        T += ["", "## Questions", ""]
        T += [f"- {q['question_id']} ({q['status']}): {q['statement']}" for q in sorted(qs, key=lambda q: q["question_id"])] or ["- none"]
        T += ["", "## Metaphors (non-evidentiary)", ""]
        T += [f"- `{m}`" for m in sorted(covers.get(cid, []))] or ["- none (see metaphor-gaps.md)"]
        TM = ["graph LR", f"  {mid(cid)}[{mm(c['label'])}]:::concept"]
        for r in anchors:
            TM.append(f"  {mid(r)}[{mm(r)}] --- {mid(cid)}")
        for x in rel:
            TM.append(f"  {mid(x['from'])} -->|{x['connection_type']} · {x['review_status']}| {mid(x['to'])}")
        for m in sorted(covers.get(cid, [])):
            TM.append(f"  {mid(m)}([{mm(m)}]) -.->|metaphor| {mid(cid)}")
        TM.append("  classDef concept fill:#fff4d6,stroke:#a07a00")
        T += ["", f"Diagram: [{cid.split('::')[1]}.mmd]({cid.split('::')[1]}.mmd)", "", "```mermaid", *TM, "```", ""]
        files[f"themes/{cid.split('::')[1]}.md"] = "\n".join(T) + "\n"
        files[f"themes/{cid.split('::')[1]}.mmd"] = "\n".join(TM) + "\n"

    # ---- historical coverage and source attestation ---------------------------------------------
    hsrc = next((s for s in manifest["sources"] if s.get("source_key") == "HIST"), {})
    plan = shared.get("hist_intake_plan", {})
    hf = shared.get("hist_findings", [])
    HC = ["# Historical coverage and source attestation", "",
          f"**HIST status:** `{hsrc.get('status', 'absent')}`. Intake plan `{plan.get('plan_id', '—')}`: **{plan.get('status', '—')}**.", "",
          "Historical archives are private and stay outside the repository. A `HIST::` reference resolves only to a registered finding that was source-verified at intake and approved for publication by a logged human decision. Everything else stays pending, and records citing it stay `blocked_missing_source`.", "",
          "Verification levels are separate: **local source verified** (bytes hashed at intake), **public pointer attested** (record consistent, but CI cannot rebuild it), **numerically reproduced** (independently recomputed). Author acceptance is a review status, not a verification level.", "",
          "## Archives", "", "| Archive | Expected sha256 | Expected members | State |", "| --- | --- | ---: | --- |"]
    HC += [f"| `{a['name']}` | `{a['sha256'][:16]}…` | {a['entries']} | {a['state']} |" for a in plan.get("archives", [])]
    HC += ["", "## Coverage matrix", "", "Unknown means unknown, not false.", "", "| Source (landmark) | Question | Expected role | Inventoried | Read | Source-attested | Structured findings | Cross-compared |", "| --- | --- | --- | --- | --- | --- | ---: | --- |"]
    for lm in plan.get("landmarks", []):
        n = sum(1 for f in hf if f.get("member_path") == lm["path"])
        done = lm["state"] != "not_inventoried"
        HC.append(f"| `{lm['path']}`" + (f" ({esc(lm['caution'])})" if lm.get("caution") else "") + f" | {lm['question']} | {lm['role_expected']} | {'yes' if done else 'no'} | no | no | {n} | no |")
    HC += ["", f"Registered historical findings: **{len(hf)}**.", "", "## Records blocked on historical sources", "", "| Record | Kind | Decision | Missing anchors |", "| --- | --- | --- | --- |"]
    for p in sorted((p for p in shared["proposals"] if p.get("missing_anchors")), key=lambda p: p["proposal_id"]):
        HC.append(f"| `{p['proposal_id']}` | {p.get('kind') or 'proposal'} | {p['decision_category']} | " + "<br>".join(f"`{a['ref']}` ({a['state'].split(' ')[0]})" for a in p["missing_anchors"]) + " |")
    for q in shared["questions"]:
        hr = [r for r in q.get("refs", []) if r.startswith("HIST::")]
        if hr:
            HC.append(f"| `{q['question_id']}` | shared question | {q['status']} | " + "<br>".join(f"`{r}`" for r in hr) + " |")
    HC += ["", "## Cautions", ""] + [f"- {esc(c)}" for c in plan.get("cautions", [])]
    files["historical-coverage.md"] = "\n".join(HC) + "\n"

    # ---- front page -------------------------------------------------------------------------------
    st = Counter(x["review_status"] for x in conns)
    ps = Counter(p["status"] for p in shared["proposals"])
    I = ["# Relational Substrate: federated research map", "", "A navigable, generated view across research programmes. **It does not merge or rewrite any programme's ledger**, and it is not scientific validation. Global coherence here does not mean that everything agrees: contrasts, nulls and open questions are shown alongside links.", ""]
    I += ["## Sources", "", "| Source | Status | Pinned commit | Nodes read |", "| --- | --- | --- | --- |"]
    for s in manifest["sources"]:
        n = sum(1 for v in loaded["nodes"].values() if v.get("source") == s["source_key"])
        I.append(f"| {esc(s['programme'])} (`{s['namespace']}::`) | **{s['status'].upper()}** | `{(s.get('commit') or '—')[:12]}` | {n} |")
    I += ["", "## Shared layer", "", f"- Concepts: {len(concepts)}", f"- Cross-programme connections: {len(conns)} ({', '.join(f'{k}: {v}' for k, v in sorted(st.items()))})", f"- Proposals: {len(shared['proposals'])} ({', '.join(f'{k}: {v}' for k, v in sorted(ps.items()))})", f"- Shared questions: {len(shared['questions'])} ({sum(q['status'] == 'pending_source' for q in shared['questions'])} pending a missing source)", f"- Metaphors: {len(shared['metaphors'])} reviewed ({', '.join(f'{k}: {v}' for k, v in sorted(Counter(m['status'] for m in shared['metaphors']).items()))}), {len(shared['metaphor_drafts'])} draft (all non-evidentiary)", ""]
    dc = Counter(x["decision_category"] for x in conns)
    I += [f"- Connection decision categories (recommended by the agent; human acceptance keeps them): {', '.join(f'{k}: {v}' for k, v in sorted(dc.items()))}", "", "## Headlines", "", "- **Open cross-programme question:** XQ::01. Which declared comparator separates organisation (or history) from kinetics in both programmes? See [questions.md](questions.md).", "- **Contradiction resolved by scope:** X::0004. 'Reweighting can break reversibility' (CL) against 'single-witness templates are always reversible' (GT) differ in rule class (label covariance), not in fact. See [contradictions.md](contradictions.md).", ]
    resolved = [p for p in shared["proposals"] if p.get("relation_override")]
    I += [f"- **Author decision:** {p['proposal_id']} classified as `{p['relation_override']['to']}`" + (f" (matching {p['relation_override']['matches']})" if p['relation_override'].get('matches') else "") + ". See [contradictions.md](contradictions.md)." for p in sorted(resolved, key=lambda p: p["proposal_id"])]
    I += ["- **Limitation:** results from CL 008N and GT-P009 are closed but unreviewed; links resting on them are capped at `qualified`.", "- **Historical intake:** `HIST` is `" + hsrc.get("status", "absent") + "`; " + str(len(hf)) + " historical findings registered. See [historical-coverage.md](historical-coverage.md).", "- **Not claimed:** no record derives physical gravity, quantum behaviour or physical time.", ""]
    I += ["## Views", "", "| View | What it shows |", "| --- | --- |", "| [provenance.md](provenance.md) · [provenance.mmd](provenance.mmd) | Sources, pins, artifacts, lineage, local-tree presence |", "| [links.md](links.md) · [links.mmd](links.mmd) | Reviewed cross-programme connections with rationale |", "| [contradictions.md](contradictions.md) · [nulls.md](nulls.md) | Contrasts, qualifications, rejected proposals; programme negative and qualified findings; false-attractor controls |", "| [questions.md](questions.md) | Shared questions and discriminating tests; programme open questions |", "| [candidate-bridges.md](candidate-bridges.md) | Proposals and retrieval diagnostics (not evidence) |", "| [metaphor-coverage.md](metaphor-coverage.md) · [metaphor-overlap.md](metaphor-overlap.md) · [metaphor-gaps.md](metaphor-gaps.md) · [metaphor-links.mmd](metaphor-links.mmd) | Explanations, overlaps, conflicts, gaps, overreach |", "| [chronology.md](chronology.md) | Change over time |", "| [historical-coverage.md](historical-coverage.md) | Historical archives, coverage matrix, source attestation and records blocked on historical sources |", "| [graph.json](graph.json) | Lossless machine-readable export: all nodes, edges (scientific, metaphor, provenance kept separate), shared records, statuses and source pins |", ""]
    I += ["## Themes", ""] + [f"- [{c['label']}](themes/{c['concept_id'].split('::')[1]}.md)" for c in concepts]
    files["index.md"] = "\n".join(I) + "\n"
    return files


def load_inputs():
    manifest = sources.load_manifest()
    loaded = sources.load_sources(manifest)
    shared = ledger.load_shared()
    disc_path = core.ROOT / "proposals" / "discovery-diagnostics.json"
    discovery = core.read_json(disc_path) if disc_path.exists() else None
    return manifest, loaded, shared, discovery


def write(files: dict[str, str], dest=None) -> None:
    import shutil

    dest = dest or gen_dir()
    if dest.exists():
        shutil.rmtree(dest)
    for rel, text in files.items():
        core.write_text(dest / rel, text)


def stale(files: dict[str, str], dest=None) -> list[str]:
    """Generated files that differ from what the inputs produce (or are extra)."""
    dest = dest or gen_dir()
    out = []
    for rel, text in files.items():
        p = dest / rel
        if not p.exists() or p.read_text(encoding="utf-8") != text:
            out.append(rel)
    if dest.exists():
        for p in dest.rglob("*"):
            if p.is_file() and str(p.relative_to(dest)) not in files:
                out.append(str(p.relative_to(dest)) + " (unexpected)")
    return sorted(out)
