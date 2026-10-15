# Metaphor coverage

Metaphors are explanations, **never evidence**. A metaphor's status never changes a finding's or connection's status. Each metaphor states what it does not mean.

| Concept | Plain definition | Reviewed metaphors |
| --- | --- | --- |
| `C::admissibility-vs-weighting` Admissibility versus weighting | Forbidding something is different in kind from merely making it rare, even when the results sometimes look similar. | `M::heavy-door-locked-door` |
| `C::clock-readout-dependence` Clock and readout dependence | What you see depends on how you count time and what you choose to watch. | `M::minutes-and-moves` |
| `C::higher-order-context` Higher-order and topological context | Whether one link changes can depend on the shape of the links around it. | **none** |
| `C::history-as-predictive-variable` History as a predictive variable | Sometimes the present snapshot is enough to predict what comes next; sometimes you also need to know how you got here. | `M::photo-and-diary` |
| `C::matched-control-design` Matched-control design | A fair comparison keeps chosen things equal on purpose, and you must know what else that silently keeps equal. | `M::two-towns` |
| `C::occupancy-vs-process` Occupancy does not fix process | Knowing how often something is the case does not tell you how long it lasts or how it gets there. | `M::two-towns` |
| `C::passage-and-persistence` Retention, resilience, reconstruction, occupancy and passage | How common something is, how you reach it, how long it lasts, whether it bounces back and whether it can be rebuilt are five different questions. | `M::rotating-committee` |
| `C::physical-attraction` Physical gravitational attraction (external notion) | Gravity as physicists mean it, which none of these models derives. | **none** |
| `C::predictive-sufficiency` Future-relative predictive sufficiency | A summary is good enough when adding more detail about the present or past would not improve your forecast of the thing you care about. | `M::photo-and-diary` |
| `C::retention-vs-current-dependence` Retention versus current dependence | Forgetting where you started is not the same as ignoring where you are now. | **none** |
| `C::reversibility-and-arrow` Reversibility and stationary arrow | A process has a direction when, even in balance, it runs around some loops more one way than the other. | **none** |
| `C::selection-vs-persistence` Selection is not persistence | Picking the tallest person in a room does not show that tallness lasts. | `M::tallest-in-the-room` |
| `C::shared-lineage` Shared code and kernel lineage | Two reports written with the same calculator can agree because of the calculator. | **none** |

## The metaphors

### A heavy door and a locked door (`M::heavy-door-locked-door`; agent_reviewed, non-evidentiary)

A door that gets heavier is used less and less, and some counts of use slide smoothly toward what happens when it is locked. But locking it is different in kind: some routes stop existing, and some changes can no longer be undone. Forbidding is not just extreme discouragement, even when a few numbers look continuous.

| In the picture | Stands for |
| --- | --- |
| a heavier and heavier door | a soft suppression factor 1/2, 1/4, 1/9, 1/16 on a transition |
| a locked door | a hard prohibition (zero rate; outside the log-weight algebra) |
| how often the door is used | stationary observables such as flux or partner index |
| which rooms can be reached at all | the support and reachable class (one-way transitions) |

**Audience:** thoughtful non-specialist reader. **Useful scope:** Helps separate soft suppression from hard prohibition, including why some observables look continuous while support changes.

**It does not mean:** Rooms and doors are not space: they label states and transitions; Nobody pushes the door; there are no forces; It does not say every observable is continuous.

**Misleading readings:** Concluding that hard bans are 'just' strong weights (support changes, GT-F51); Concluding that they are always discontinuous (GT-F54).

### Counting minutes or counting moves (`M::minutes-and-moves`; agent_reviewed, non-evidentiary)

In a board game where moves happen at random rates, whether the white pieces or the black pieces finish first can depend on whether you count minutes or moves. That is GT's clock dependence: the same sequence of moves, weighted differently. If you also stop recording the moves of one kind of piece, the record you keep can look as if it remembers things the full game does not: that is CL's epoch, which hides events as well as changing the clock.

| In the picture | Stands for |
| --- | --- |
| minutes on a wall clock | continuous model time |
| the number of moves made | jump (event) count |
| counting only the moves of one kind of piece | CL's pair-event epoch: a time change plus a projection that hides triad events |

**Audience:** thoughtful non-specialist reader. **Useful scope:** Helps explain why clock choice changes conclusions, and why CL's epoch (hiding events) differs from GT's two clocks.

**It does not mean:** Nobody is playing: moves happen at random rates and no one decides them; Neither count is physical time; It does not say one clock is the true one.

**Misleading readings:** Treating CL's and GT's clock effects as one phenomenon (X::0003 records the contrast).

### A photograph and a diary (`M::photo-and-diary`; agent_reviewed, non-evidentiary)

Sometimes a photograph of the present is all you need to forecast what happens next. Sometimes two identical photographs lead to different futures, and only the diary tells them apart: then history is a predictive variable. A historian can read a diary without the diary changing anything; a council that acts on the diary is different. Only the second makes history part of the rules.

| In the picture | Stands for |
| --- | --- |
| a photograph of the present | the complete current state x |
| a diary of recent events | a history register h (augmented state) |
| a forecast of the next event | the conditional law of the next transition |
| a photograph good enough that the diary adds nothing | Markov (predictive) sufficiency of the state for the declared observable |
| a historian reading the diary versus a council acting on it | a trajectory observable versus a rule that reads history (CL's H axis) |

**Audience:** thoughtful non-specialist reader. **Useful scope:** Helps separate predictive sufficiency of the current state from history as a predictive variable, and an observer reading history from a rule acting on it.

**It does not mean:** Memory is not a mind and nothing is remembered unless the model declares an augmented state; The diary is not stored anywhere in the substrate unless it is part of the declared state; It says nothing about physical time.

**Misleading readings:** Thinking more diary is always better: beyond the sufficient register, extra history adds nothing (CL predictive quotients); Thinking a long diary means long memory: in irreducible chains information about the initial state decays.

### A committee whose members rotate (`M::rotating-committee`; agent_reviewed, non-evidentiary)

A committee can keep meeting for a long time while its members come and go. That is different from a fixed group of people who all have to stay. But a long-running committee does not prove anyone is keeping it together: if members rejoin as fast as they leave, the committee may last simply because everything around the chair is busy.

| In the picture | Stands for |
| --- | --- |
| the chair | the anchor vertex c (an observation index, not a privileged entity) |
| the committee meets while it has at least two members | the flexible predicate F_2PATH(c): deg(c) >= 2 |
| a member leaving or joining while the committee still meets | an eligible within-episode turnover toggle (counted by Omega) |
| a member who leaves and rejoins at once | flicker: counted twice by Omega, not a replacement |

**Audience:** thoughtful non-specialist reader. **Useful scope:** Helps explain persistence of an anchored property through member turnover, and why long life alone does not show organisation.

**It does not mean:** The committee has no purpose or identity; nobody intends it to continue; Long life is not identity through complete replacement (not defined in E5A); The chair has no special power in the rules.

**Misleading readings:** Reading persistence through turnover as organisation (GT-F78 shows uneven activity can produce it); Reading Omega as the number of replacements.

### Picking the tallest person in the room (`M::tallest-in-the-room`; agent_reviewed, non-evidentiary)

If you pick the tallest person in a room, they are tall by construction; that tells you nothing about whether height lasts. In these models 'height' (number of links) keeps changing, and whoever was picked drifts back to average. The useful question is how fast, compared with a fair baseline.

| In the picture | Stands for |
| --- | --- |
| picking whoever is tallest right now | selecting a maximum-degree vertex at a stationary start |
| checking later whether they still stand out | the lagged degree gap against a uniformly chosen vertex |
| everyone being equally likely to be tallest in the long run | exchangeability: no labelled vertex stays distinguished (GT-F72) |

**Audience:** thoughtful non-specialist reader. **Useful scope:** Helps explain why selecting an extreme vertex is not evidence that it stays special.

**It does not mean:** People and heights are labels for vertices and degrees; there is no space or body; Drifting back is not motion; It does not say any vertex is special.

**Misleading readings:** Reading a slow return to average as a lasting centre.

### Two towns with the same number of open cafés (`M::two-towns`; agent_reviewed, non-evidentiary)

Two towns can have exactly the same number of cafés open on an average day. In one, each café stays open for years; in the other, cafés open and close every week in a busy quarter while the quiet quarter hardly changes. Counting open cafés on a random day cannot tell the towns apart. Following one café over time can.

| In the picture | Stands for |
| --- | --- |
| a town | a stochastic process (its generator) |
| the number of cafés open on a random day | stationary occupancy / prevalence pi(A) |
| how long one café stays open | entrance-episode lifetime L = pi(A)/J_A |
| a busy quarter where cafés open and close every week | states with high total transition rate |

**Audience:** thoughtful non-specialist reader. **Useful scope:** Helps a reader see why matched occupancy (or density) cannot settle questions about lifetime or passage; useful for CL-T88/F8N and GT-F78/F79.

**It does not mean:** There is no space: 'town' and 'quarter' label groups of states, not places; Cafés are not agents; nothing chooses to open or close; It does not say which process is more real, more organised or better.

**Misleading readings:** Reading the long-lived town as 'more organised': in GT's PCOMP the long life comes from uneven activity, with no structural preference at all (GT-F78); Reading 'busy quarter' as physical crowding.

