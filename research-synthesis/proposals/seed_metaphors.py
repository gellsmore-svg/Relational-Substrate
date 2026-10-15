"""Agent-drafted metaphors and metaphor links (the author's seeds/metaphors.jsonl was not supplied).

Metaphors are explanations, never evidence. Agent-reviewed ones go to
ledger/metaphors.jsonl; drafts stay in proposals/metaphor-drafts.jsonl.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = {"owner": "programme author (human)", "process": "docs/cadence.md (metaphor review)", "reviewed_by": "agent: Claude Opus 5.5 (session of 2026-10-15)", "human_reviewed": False}
AUDIENCE = "thoughtful non-specialist reader"

METAPHORS = [
    {
        "metaphor_id": "M::two-towns",
        "title": "Two towns with the same number of open cafés",
        "concepts": ["C::occupancy-vs-process", "C::matched-control-design"],
        "mapping": [
            {"figure": "a town", "object": "a stochastic process (its generator)"},
            {"figure": "the number of cafés open on a random day", "object": "stationary occupancy / prevalence pi(A)"},
            {"figure": "how long one café stays open", "object": "entrance-episode lifetime L = pi(A)/J_A"},
            {"figure": "a busy quarter where cafés open and close every week", "object": "states with high total transition rate"},
        ],
        "explanation": "Two towns can have exactly the same number of cafés open on an average day. In one, each café stays open for years; in the other, cafés open and close every week in a busy quarter while the quiet quarter hardly changes. Counting open cafés on a random day cannot tell the towns apart. Following one café over time can.",
        "does_not_mean": ["There is no space: 'town' and 'quarter' label groups of states, not places", "Cafés are not agents; nothing chooses to open or close", "It does not say which process is more real, more organised or better"],
        "misleading_readings": ["Reading the long-lived town as 'more organised': in GT's PCOMP the long life comes from uneven activity, with no structural preference at all (GT-F78)", "Reading 'busy quarter' as physical crowding"],
        "illustrative_status": "illustrative only; matches the qualitative content of CL-T88/F8N and GT-F78, not their numbers",
        "status": "agent_reviewed",
    },
    {
        "metaphor_id": "M::photo-and-diary",
        "title": "A photograph and a diary",
        "concepts": ["C::history-as-predictive-variable", "C::predictive-sufficiency"],
        "mapping": [
            {"figure": "a photograph of the present", "object": "the complete current state x"},
            {"figure": "a diary of recent events", "object": "a history register h (augmented state)"},
            {"figure": "a forecast of the next event", "object": "the conditional law of the next transition"},
            {"figure": "a photograph good enough that the diary adds nothing", "object": "Markov (predictive) sufficiency of the state for the declared observable"},
            {"figure": "a historian reading the diary versus a council acting on it", "object": "a trajectory observable versus a rule that reads history (CL's H axis)"},
        ],
        "explanation": "Sometimes a photograph of the present is all you need to forecast what happens next. Sometimes two identical photographs lead to different futures, and only the diary tells them apart: then history is a predictive variable. A historian can read a diary without the diary changing anything; a council that acts on the diary is different. Only the second makes history part of the rules.",
        "does_not_mean": ["Memory is not a mind and nothing is remembered unless the model declares an augmented state", "The diary is not stored anywhere in the substrate unless it is part of the declared state", "It says nothing about physical time"],
        "misleading_readings": ["Thinking more diary is always better: beyond the sufficient register, extra history adds nothing (CL predictive quotients)", "Thinking a long diary means long memory: in irreducible chains information about the initial state decays"],
        "illustrative_status": "illustrative only",
        "status": "agent_reviewed",
    },
    {
        "metaphor_id": "M::minutes-and-moves",
        "title": "Counting minutes or counting moves",
        "concepts": ["C::clock-readout-dependence"],
        "mapping": [
            {"figure": "minutes on a wall clock", "object": "continuous model time"},
            {"figure": "the number of moves made", "object": "jump (event) count"},
            {"figure": "counting only the moves of one kind of piece", "object": "CL's pair-event epoch: a time change plus a projection that hides triad events"},
        ],
        "explanation": "In a board game where moves happen at random rates, whether the white pieces or the black pieces finish first can depend on whether you count minutes or moves. That is GT's clock dependence: the same sequence of moves, weighted differently. If you also stop recording the moves of one kind of piece, the record you keep can look as if it remembers things the full game does not: that is CL's epoch, which hides events as well as changing the clock.",
        "does_not_mean": ["Nobody is playing: moves happen at random rates and no one decides them", "Neither count is physical time", "It does not say one clock is the true one"],
        "misleading_readings": ["Treating CL's and GT's clock effects as one phenomenon (X::0003 records the contrast)"],
        "illustrative_status": "illustrative only",
        "status": "agent_reviewed",
    },
    {
        "metaphor_id": "M::heavy-door-locked-door",
        "title": "A heavy door and a locked door",
        "concepts": ["C::admissibility-vs-weighting"],
        "mapping": [
            {"figure": "a heavier and heavier door", "object": "a soft suppression factor 1/2, 1/4, 1/9, 1/16 on a transition"},
            {"figure": "a locked door", "object": "a hard prohibition (zero rate; outside the log-weight algebra)"},
            {"figure": "how often the door is used", "object": "stationary observables such as flux or partner index"},
            {"figure": "which rooms can be reached at all", "object": "the support and reachable class (one-way transitions)"},
        ],
        "explanation": "A door that gets heavier is used less and less, and some counts of use slide smoothly toward what happens when it is locked. But locking it is different in kind: some routes stop existing, and some changes can no longer be undone. Forbidding is not just extreme discouragement, even when a few numbers look continuous.",
        "does_not_mean": ["Rooms and doors are not space: they label states and transitions", "Nobody pushes the door; there are no forces", "It does not say every observable is continuous"],
        "misleading_readings": ["Concluding that hard bans are 'just' strong weights (support changes, GT-F51)", "Concluding that they are always discontinuous (GT-F54)"],
        "illustrative_status": "illustrative only",
        "status": "agent_reviewed",
    },
    {
        "metaphor_id": "M::rotating-committee",
        "title": "A committee whose members rotate",
        "concepts": ["C::passage-and-persistence"],
        "mapping": [
            {"figure": "the chair", "object": "the anchor vertex c (an observation index, not a privileged entity)"},
            {"figure": "the committee meets while it has at least two members", "object": "the flexible predicate F_2PATH(c): deg(c) >= 2"},
            {"figure": "a member leaving or joining while the committee still meets", "object": "an eligible within-episode turnover toggle (counted by Omega)"},
            {"figure": "a member who leaves and rejoins at once", "object": "flicker: counted twice by Omega, not a replacement"},
        ],
        "explanation": "A committee can keep meeting for a long time while its members come and go. That is different from a fixed group of people who all have to stay. But a long-running committee does not prove anyone is keeping it together: if members rejoin as fast as they leave, the committee may last simply because everything around the chair is busy.",
        "does_not_mean": ["The committee has no purpose or identity; nobody intends it to continue", "Long life is not identity through complete replacement (not defined in E5A)", "The chair has no special power in the rules"],
        "misleading_readings": ["Reading persistence through turnover as organisation (GT-F78 shows uneven activity can produce it)", "Reading Omega as the number of replacements"],
        "illustrative_status": "illustrative only",
        "status": "agent_reviewed",
    },
    {
        "metaphor_id": "M::tallest-in-the-room",
        "title": "Picking the tallest person in the room",
        "concepts": ["C::selection-vs-persistence"],
        "mapping": [
            {"figure": "picking whoever is tallest right now", "object": "selecting a maximum-degree vertex at a stationary start"},
            {"figure": "checking later whether they still stand out", "object": "the lagged degree gap against a uniformly chosen vertex"},
            {"figure": "everyone being equally likely to be tallest in the long run", "object": "exchangeability: no labelled vertex stays distinguished (GT-F72)"},
        ],
        "explanation": "If you pick the tallest person in a room, they are tall by construction; that tells you nothing about whether height lasts. In these models 'height' (number of links) keeps changing, and whoever was picked drifts back to average. The useful question is how fast, compared with a fair baseline.",
        "does_not_mean": ["People and heights are labels for vertices and degrees; there is no space or body", "Drifting back is not motion", "It does not say any vertex is special"],
        "misleading_readings": ["Reading a slow return to average as a lasting centre"],
        "illustrative_status": "illustrative only",
        "status": "agent_reviewed",
    },
]

DRAFTS = [
    {
        "metaphor_id": "M::fading-echo",
        "title": "A fading echo in a shaped hall",
        "concepts": ["C::retention-vs-current-dependence"],
        "mapping": [
            {"figure": "the echo of a clap", "object": "information about the initial condition, which decays"},
            {"figure": "the shape of the hall", "object": "current higher-order structure that shapes the next event"},
        ],
        "explanation": "A clap's echo fades, but the shape of the hall goes on colouring every new sound. Forgetting the clap is not the same as ignoring the hall.",
        "does_not_mean": ["There is no hall, sound or space: these label states and dependence", "Nothing hears or remembers"],
        "misleading_readings": ["Thinking the hall is fixed: in these models the current structure itself changes"],
        "illustrative_status": "draft; not reviewed",
        "status": "draft",
    }
]

LINKS = [
    ("covers_concept", "M::two-towns", "C::occupancy-vs-process", "Core reading: one-time counts cannot separate processes"),
    ("covers_concept", "M::two-towns", "C::matched-control-design", "Same average count, different lifetimes: what a matched comparison does and does not fix"),
    ("illustrates_relation", "M::two-towns", "X::0001", "Illustrates the matched-occupancy, different-passage analogy"),
    ("requires_qualification", "M::two-towns", "GT::GT-F78-LIFETIME-NOT-SET-BY-STATIONARY-LAW", "The 'slow town' must not be read as organised; GT-F78 is a heterogeneity effect"),
    ("covers_concept", "M::photo-and-diary", "C::history-as-predictive-variable", "Photograph versus diary"),
    ("covers_concept", "M::photo-and-diary", "C::predictive-sufficiency", "A photograph good enough that the diary adds nothing"),
    ("illustrates_relation", "M::photo-and-diary", "X::0008", "Historian versus council: observable versus rule reading history"),
    ("fails_for", "M::photo-and-diary", "C::retention-vs-current-dependence", "A diary suggests memory accumulates; in irreducible chains initial information decays"),
    ("covers_concept", "M::minutes-and-moves", "C::clock-readout-dependence", "Minutes versus moves"),
    ("illustrates_relation", "M::minutes-and-moves", "X::0003", "Same moves weighted differently (GT) versus hiding one kind of move (CL)"),
    ("requires_qualification", "M::minutes-and-moves", "CL::F003-CLOCK-SPLIT", "Hiding moves also changes what is observed, not only the clock"),
    ("covers_concept", "M::heavy-door-locked-door", "C::admissibility-vs-weighting", "Heavy versus locked"),
    ("illustrates_relation", "M::heavy-door-locked-door", "X::0006", "Some counts continuous along the ladder; support changes at the end"),
    ("covers_concept", "M::rotating-committee", "C::passage-and-persistence", "Persistence through turnover versus fixed membership"),
    ("requires_qualification", "M::rotating-committee", "GT::GT-F76-FLEXIBLE-ORGANISATION-OUTLIVES-ND-QUALIFIED", "Omega counts toggles including flicker; long life may be heterogeneity"),
    ("covers_concept", "M::tallest-in-the-room", "C::selection-vs-persistence", "Selection is not persistence"),
    ("complements", "M::two-towns", "M::rotating-committee", "Read together: long life may be busyness, not organisation"),
    ("conflicts_with", "M::rotating-committee", "M::two-towns", "The committee invites an organisation reading of GT-F76 that the two towns warn against; keep both visible"),
    ("bridges_metaphors", "M::photo-and-diary", "M::minutes-and-moves", "Hiding moves (a projection) can make a record look as if it needs a diary"),
]


def write_all(root: Path = ROOT) -> None:
    for m in METAPHORS + DRAFTS:
        m["audience"] = AUDIENCE
        m["review"] = dict(REVIEW)
        m["evidentiary"] = False
        m["origin"] = "agent_drafted"
    links = [{"link_id": f"ML::{i:03d}", "link_type": t, "from": a, "to": b, "note": n} for i, (t, a, b, n) in enumerate(LINKS, 1)]

    def dump(path, rows):
        (root / path).write_text("".join(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")

    dump("ledger/metaphors.jsonl", METAPHORS)
    dump("proposals/metaphor-drafts.jsonl", DRAFTS)
    dump("ledger/metaphor-links.jsonl", links)


if __name__ == "__main__":
    write_all(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT)
