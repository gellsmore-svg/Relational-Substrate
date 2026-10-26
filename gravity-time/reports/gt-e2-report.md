# What the handover is, and when dissolving a relation enables anything

*A plain-English report for the human researcher on prompt GT-P005 (two rounds, E2A and E2B, 14 October 2026). It assumes no knowledge of the code. Detailed documents are listed at the end.*

## The question you asked

In the earlier experiments, a repeated pattern of four changes kept appearing. We called it the **handover**:
1. a relation forms between two outer entities;
2. one of them links to the fixed source;
3. the relation between the outer entities dissolves;
4. the link to the source dissolves.

It ran in the same direction in all 30 cases tested in E1. You asked:
- what produces this kind of ordered sequence;
- whether it is general or depends on choices we made;
- whether "a relation dissolving" actually *enables* the next change, or only comes before it.

## What I did

I worked in the smallest systems that can show the pattern: five entities, plus a small check at six. I used only rules the framework already has, so no new kind of rule was introduced.

**Before running anything**, I worked through the rules on paper. That gave an exact formula for how strongly each small loop of four changes is pushed one way rather than the other. I checked it on made-up rule strengths that the experiments never use.

**Round E2A** (46 cases, frozen before running):
- every strength of the two path rules (the rules that look two steps away);
- the four ways to combine them;
- controls that should show no direction at all;
- cases with "hard" rules that forbid some changes outright;
- two cases built to lower crowding;

each with and without a fixed source.

**Round E2B** (18 cases, chosen *because* of what E2A showed, and frozen before running) looked at the three kinds of hard rule combined with path rules of both directions.

All 64 cases finished. Every built-in check passed.

## What I found

**1. The direction of the handover is explained exactly, and it is not universal.**
- The formula says something simple. When two relations share an entity, the rules favour keeping the one whose *other* end is better connected and letting go of the one whose other end is less connected.
- With a fixed source, the source's members always have two extra links. So "keep the link to the source, let the outer relation go" is the favoured direction. That is the handover.
- Whether it runs forward or backward depends on a single number I'll call **σ**: whether the path rules mainly speed up dissolving or mainly slow down forming.
- Every rule in the earlier rounds had σ positive, which is why the direction never changed. It was a consequence of the rules we happened to choose, not a law of the model.

**2. Making σ negative reverses the handover. Usually you can't see it, but sometimes it is as strong as the original.**
- Most negative-σ rules pack the system with relations until almost every possible one is present. The reversal is then real but vanishingly small (a few parts in a hundred thousand at most).
- In two set-ups that keep the system from filling up, the reversed handover was clearly visible:
  - with a rule against crowding, it was about as strong as typical forward handovers (index −0.112, against 0.015 to 0.19 forward);
  - with a hard rule forbidding triangles, it was weaker but plain (−0.015 to −0.042).

**3. The overall flow follows σ, even though individual loops sometimes disagree.**
- In all 36 cases with a direction (and without the special one-way behaviour of point 5), the overall direction matched the sign of σ.
- But looked at loop by loop, up to a third of the flow runs against what its own loop favours, carried along by neighbouring loops.
- So the formula explains *what pushes*; the overall pattern is a property of the whole system. I could not prove that it must always follow σ. That stays open.

**4. In ordinary (soft) rules, dissolving a relation does not enable the next step. It just clears the way.**
- Take the step "outer relation dissolves, then the source link dissolves". Removing the outer relation leaves the source link's own tendency to dissolve unchanged, or even lowers it.
- The source link's dissolution still becomes the more likely *next* event, because the outer relation's own fast dissolution is no longer competing.
- That is an **opportunity effect**, not enabling. Looking eight events ahead, the effect has almost vanished.
- Across all the soft rules, nothing was ever made possible that was impossible before. In 59% of cases, the change in "what happens next" came mainly from this opportunity effect.

**5. Real enabling needs a hard rule, and even then it need not create a direction.**
- With a rule that forbids some changes outright, dissolving a relation can make a forbidden change possible. I call this **strict enabling**. I found it in three different settings:
  - **no direction at all.** A rule forbidding triangles, or one forbidding any two relations from sharing an entity: removing one relation makes another possible in up to 87% of matched cases, yet the system has no preferred direction.
  - **a direction that follows σ.** The triangle rule plus a path rule.
  - **a new kind of direction.** A rule forbidding a relation from forming while a two-step path leads to it. Here, once a relation dissolves it cannot come back while that path exists. This **one-way release** creates the strongest flow seen in either round. It always runs "keep the better-connected link" — even when σ is negative. It is the one case where the σ rule fails.
- When something is strictly enabled, it happens before the removed relation comes back only about **half** the time. Dissolution opens a window; it does not commit the system.
- Surprisingly, the changes that dissolution makes possible are *not* more likely to come immediately afterwards. What dissolution makes possible and what tends to follow it are different questions.

**6. Two smaller boundaries.**
- **Forbidding shared entities switches off path rules completely.** Every reachable arrangement then has no two relations meeting at an entity, so a path rule never has anything to act on.
- **The fixed source can block things.** It is not just a reference point. Under some hard rules, its own internal links count against other relations forming, so no outer entity can ever link to it.

## What is a model result and what is not

- Everything above is about a small mathematical model of relations forming and dissolving.
- The direction found here is a mathematical property of chosen rules, of a kind well understood in probability theory. It is not the physical arrow of time, not thermodynamic entropy, and not gravity.
- As an interpretation for the relational framework only, the clearest lesson is that **"direction", "attraction" and "enabling" are three different things** in this model. Evidence for one says nothing about the others.
  - The handover does not pull outer entities in. Even the reversed handover leaves them less attached than with no rule at all.
  - Strict enabling can happen with no direction.

## What I recommend next (not done)

1. **Study one-way release** (my recommendation).
   - It is the only place where the σ explanation fails, and the only directed sequence without loops.
   - It is also the clearest case of a release that cannot be undone.
   - It is cheap and exact, and it bears directly on the other programme's open question about dissolution.
2. **Try to prove the overall-direction rule,** or find a counterexample (a mathematical companion to option 1).
3. **Test the fixed source's structure** (a bigger or differently shaped source). This has become more important, now that we know the source can act as a constraint, not just a reference.
4. **The "clock split" question** from E1, which E2 did not address.
5. **FREE systems with seven entities.** I'd now give this low priority: nothing found here suggests a mechanism for a centre forming by itself.

## Decisions I need from you

1. Should the next prompt study **one-way release** (option 1, with option 2 alongside), or something else?
2. Should the two suggested findings for the **Constraint Laboratory** go to that programme? These are the exact formula for CL-Q04, and the enabling results for CL-Q05. They are written up (synthesis, section 6) but not entered in its records.
3. Do you want the new distinctions adopted as ontology proposals (`docs/ontology-proposals.md` OP-10 to OP-12)? They are:
   - two kinds of direction;
   - four senses of "enables";
   - a fixed source acting as a constraint.
4. PR #6 is still a draft and has not been merged. Should it stay that way?

## Where to look

| What | File |
| --- | --- |
| This report | `gravity-time/reports/gt-e2-report.md` |
| The formula and its proof | `gravity-time/docs/e2-formal-mechanism.md` |
| How dissolution was tested | `gravity-time/reports/gt-e2-dissolution-analysis.md` |
| Map of mechanisms and counterexamples | `gravity-time/reports/gt-e2-mechanism-atlas.md` |
| Every case, every number | `gravity-time/reports/gt-e2a-atlas.md`, `gt-e2b-atlas.md` |
| Reasoning between the rounds | `gravity-time/reports/gt-e2a-reflection.md` |
| Overall synthesis and next steps | `gravity-time/reports/gt-e2-synthesis.md` |
| What was done, when, with which checks | `gravity-time/provenance/execution-GT-P005.md` |
