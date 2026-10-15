"""Vector-assisted discovery: deterministic TF-IDF cosine retrieval of cross-programme candidate pairs.

The similarity is a *retrieval measurement*: not a probability, not a
confidence in scientific correctness, not a substitute for mathematical
review. Low similarity is not evidence against structural convergence.
Output goes to proposals/discovery-diagnostics.json only; this module never
writes to the ledger and never changes any status.
"""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict

from . import core

def diagnostics_path():
    return core.ROOT / "proposals" / "discovery-diagnostics.json"
STOP = set("a an and are as at be been between both but by can does each for from has have if in into is it its may more most no not of on one only or other same so such than that the their then there these this those through to under was were when where which while with without within".split())
# Formal-object dimensions (01 prompt, Stage C). Missing evidence for a dimension stays 'unknown'.
DIMENSION_TERMS = {
    "state": ("state", "mask", "graph", "register", "augmented", "hypergraph"),
    "transition_law": ("kernel", "rate", "rates", "transition", "rule", "rules", "template", "weight", "weights"),
    "support": ("support", "prohibit", "hard", "admissib", "reachable", "absorbing", "one-way"),
    "clock": ("clock", "epoch", "jump", "per-event", "continuous", "time"),
    "projection": ("projection", "projected", "quotient", "class", "observable", "readout"),
    "intervention": ("control", "matched", "intervention", "comparator", "held"),
    "horizon": ("stationary", "horizon", "transient", "lag", "finite-horizon"),
    "conditioning": ("conditional", "conditioned", "source", "given", "entrance"),
}
TOP_PER_NODE = 3
MAX_PER_CLUSTER = 2
NEAR_DUPLICATE = 0.9
INHERITED_WORDING = 0.8


def tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z][a-z0-9\-]+", text.lower()) if t not in STOP and len(t) > 2]


def tfidf(docs: dict[str, str]) -> dict[str, dict[str, float]]:
    tf = {k: Counter(tokens(v)) for k, v in docs.items()}
    df = Counter(t for c in tf.values() for t in c)
    n = len(docs)
    vecs = {}
    for k, c in tf.items():
        v = {t: (1 + math.log(f)) * math.log((1 + n) / (1 + df[t])) for t, f in c.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        vecs[k] = {t: x / norm for t, x in v.items()}
    return vecs


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(t, 0.0) for t, x in a.items())


def _clusters(keys: list[str], vecs: dict) -> dict[str, str]:
    """Greedy near-duplicate clustering within one source (deterministic order)."""
    rep = {}
    reps: list[str] = []
    for k in keys:
        for r in reps:
            if cosine(vecs[k], vecs[r]) >= NEAR_DUPLICATE:
                rep[k] = r
                break
        else:
            reps.append(k)
            rep[k] = k
    return rep


def dimension_tags(a: str, b: str) -> dict[str, str]:
    la, lb = a.lower(), b.lower()
    out = {}
    for dim, terms in DIMENSION_TERMS.items():
        ia, ib = any(t in la for t in terms), any(t in lb for t in terms)
        out[dim] = "mentioned_both" if ia and ib else ("mentioned_one_side" if ia or ib else "unknown")
    return out


def discover(nodes: dict, shared: dict, manifest: dict, *, programmes=("CL", "GT"), limit: int = 40) -> dict:
    docs = {k: v["statement"] for k, v in nodes.items() if v.get("source") in programmes and v["kind"] in ("source_finding", "formal_claim", "source_question") and v.get("statement")}
    vecs = tfidf(docs)
    by_source = defaultdict(list)
    for k in sorted(docs):
        by_source[nodes[k]["source"]].append(k)
    cluster = {}
    for src, keys in by_source.items():
        cluster.update(_clusters(keys, vecs))
    reviewed = {(x["from"], x["to"]) for x in shared["connections"] + shared["proposals"]}
    reviewed |= {(b, a) for a, b in reviewed}
    a_keys, b_keys = by_source[programmes[0]], by_source[programmes[1]]
    pairs = []
    for a in a_keys:
        for b in b_keys:
            s = cosine(vecs[a], vecs[b])
            if s > 0:
                pairs.append((round(s, 6), a, b))
    pairs.sort(key=lambda p: (-p[0], p[1], p[2]))
    per_node, per_cluster, out = Counter(), Counter(), []
    for s, a, b in pairs:
        if per_node[a] >= TOP_PER_NODE or per_node[b] >= TOP_PER_NODE:
            continue
        ck = (cluster[a], cluster[b])
        if per_cluster[ck] >= MAX_PER_CLUSTER:
            continue
        per_node[a] += 1
        per_node[b] += 1
        per_cluster[ck] += 1
        shared_terms = sorted(set(vecs[a]) & set(vecs[b]), key=lambda t: -(vecs[a][t] * vecs[b][t]))[:8]
        flags = []
        if s >= INHERITED_WORDING:
            flags.append("possible_inherited_wording_shared_lineage")
        if (a, b) in reviewed:
            flags.append("already_reviewed")
        out.append({"from": a, "to": b, "similarity": s, "shared_terms": shared_terms, "dimension_tags": dimension_tags(docs[a], docs[b]), "flags": flags, "status": "unreviewed_retrieval_candidate"})
        if len(out) >= limit:
            break
    rank = {(a, b): i for i, (_, a, b) in enumerate(pairs, 1)}
    calibration = []
    for x in shared["connections"]:
        a, b = x["from"], x["to"]
        key = (a, b) if (a, b) in rank else (b, a)
        if a in vecs and b in vecs:
            calibration.append({"connection_id": x["connection_id"], "connection_type": x["connection_type"], "similarity": round(cosine(vecs[a], vecs[b]), 6), "rank_among_cross_pairs": rank.get(key), "cross_pairs": len(pairs)})
    return {
        "schema": "rssynth.discovery/v1",
        "reviewed_connection_calibration": sorted(calibration, key=lambda c: c["connection_id"]),
        "calibration_note": "Ranks of connections that passed formal review. Reviewed structural links typically rank far below the top candidates: low similarity is not evidence of no convergence.",
        "score_kind": "retrieval_similarity",
        "score_meaning": "TF-IDF cosine between statement texts. A ranking aid for human review: not a probability, not a confidence in correctness, not evidence of structural convergence; a low value is not evidence against it.",
        "method": {"tokeniser": "lowercase [a-z][a-z0-9-]+, stop-words removed, length > 2", "weighting": "sublinear tf times smoothed idf over the CL+GT statement corpus", "pairs": "cross-programme only", "controls": {"top_per_node": TOP_PER_NODE, "max_per_near_duplicate_cluster": MAX_PER_CLUSTER, "near_duplicate_cosine": NEAR_DUPLICATE, "inherited_wording_flag_cosine": INHERITED_WORDING}, "embedding_model": None},
        "corpus": {p: len(by_source[p]) for p in programmes},
        "candidates": out,
        "known_false_positive_patterns": [
            "Shared vocabulary with different formal objects: 'clock' in CL (pair-event epoch, a projection) and GT (continuous vs jump time) - see X::0003",
            "Shared vocabulary from inherited method text (scope boilerplate, 'W4', 'exact') under the common 8G lineage",
            "Numbers and family names matching without a shared estimand",
        ],
    }
