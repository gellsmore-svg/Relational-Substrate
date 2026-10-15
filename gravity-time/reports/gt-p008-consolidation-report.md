# What does the shape of a reference really do? A consolidation (GT-P008)

*A plain-English report for the human researcher on prompt GT-P008, 15 October 2026. This was a consolidation: mathematics, a re-reading of published results and an architecture review. **No new experiment was run.** File references are at the end.*

## What did we actually learn?

**1. The "support" a fixed reference gives a site acts like an exact lever, not a law.**
- In the last round, the less-supported parts of a fixed reference attracted more links: the middle of an open path, the centre of a star.
- I can now prove a precise statement. Under the rule sets that carry a direction of flow, each permanent supporting path at a site multiplies the long-run odds of a link there by exactly one half, times a second factor.
- That second factor depends on everything else going on in the system. It cannot be worked out, or even given a sign, from local information alone.

**2. That lever accounts for most of the sorting we saw, but not all of it.**
- In the open path and the star, the lever makes up 71–100% of the difference between sites. That is an exact bookkeeping split, not an experiment that removed the support.
- The remainder pushes in the same direction in 8 of 9 cases.
- The likely reason is a feedback: a popular site creates supporting paths for its neighbours, which makes them less popular still. This is a plausible explanation, not a proof.

**3. "Less support means more links" is not a general law. I found cases where it fails.**
- When the rules are weak, a second ingredient matters as much as support: **how many permanent links a site itself has.** At these system sizes, more permanent links makes a site *more* attractive, and the effect changes with system size.
- The resulting formula correctly predicts the direction of every within-reference comparison in the published data (16 of 16).
- But it also implies that some reference shapes would favour a **more**-supported site. I constructed seven such shapes. Whether that still happens at full rule strength is untested.

**4. One rule set has support everywhere yet produces no sorting at all in long-run occupancy.**
- PCOMP scales formation and breaking equally, so its long-run occupancy is perfectly uniform, provably, at any strength.
- It still sorts if you count by events instead of time. Which clock you use matters.

**5. The triangle's suppression of links is not a simple consequence of its support.**
- With very weak rules, the triangle reference at 5 entities would *favour* links to itself (at 6 entities the weak-rule effect is exactly zero).
- At the published strength it strongly disfavours them.
- So the effect reverses as the rules strengthen. The triangle result is a strong-rule, whole-system effect, not a local one.

**6. Two rule sets that look locally identical behave identically only to first approximation.**
- PATHF and PATHH have exactly the same local balance. I proved that their long-run behaviour agrees to first order, so every difference between them is a second-order effect.
- They reach the same sorting by opposite routes. PATHF makes links to favoured sites form faster. PATHH makes them last longer.

**7. Gathering is still mostly about crowding.** Nothing in this review changes the E4 conclusion: once you adjust for how crowded the system is, the "extra" links to a fixed reference largely disappear.

**8. A self-made reference would have to be temporary, and that is a definition problem before it is an experiment.**
- In a finite system where every link can change, no named entity can stay "the centre" forever: the mathematics forbids it.
- So a reference the system makes for itself can only be **long-lived, not permanent**. The real question becomes whether some pattern survives much longer than the links it is made of.
- That can be measured now, exactly, with no new machinery, but only once we agree what pattern to look for.

## What was proved, and what was not

**Proved (with proofs written out and checked):**
- the exact lever (point 1), and that local information cannot give its sign;
- PCOMP's uniformity (point 4);
- the weak-rule formula with its second ingredient (point 3), and the existence of reversal shapes;
- the strength-reversal for the triangle (point 5);
- the first-order agreement of PATHF and PATHH (point 6);
- the clock difference;
- that no named entity can be a permanent centre (point 8).

**Observed, but not proved:**
- the 71–100% share;
- the reinforcing remainder;
- the formula predicting all 16 directions (a fact about the published cases, found after the data were known).

**Not resolved:**
- why the remainder reinforces (the feedback is a conjecture);
- whether the reversal shapes reverse at full strength;
- a formula for the triangle's actual suppression;
- one clock-dependent exception: in the four-path, one rule's sorting flips direction when counted by events.

## Things that went against expectation, or remain uncomfortable

- The support count by itself does **not** order sites, even at the simplest level. Held degree matters as much.
- The triangle's suppression **reverses** between weak and full-strength rules (at 5 entities).
- PCOMP has support but **no time-based sorting**.
- When the open path's closing link is present, its middle loses its advantage entirely, and in time-based counting it even falls slightly behind.
- In the four-path, PATHF's sorting is weakly reversed when counted by events.
- **One correction to the last round:** the closing link of the open path is rare under two of the rules but **not** under CSPH (about half the time).
- **A second qualification:** comparing two sites inside one system controls crowding and size, but not the sites' different positions. It is a matched comparison, not an experiment on support.

## What this means for a fixed reference

- A held reference is a useful boundary condition, but it is **not a neutral ruler**.
  - Its own links act as supporting paths.
  - Its shape tilts the environment even at first order.
  - It lasts forever by decree.
- So none of the held-reference results can simply be carried over to a structure the system makes for itself.

## What it means for the bridge to larger questions

- **New capabilities, demonstrated in the model:**
  - an exact account of how a structure's support enters the long-run odds;
  - a weak-rule formula for which sites a structure favours;
  - a clean separation of time-based and event-based sorting.
- **Still undefined:** what counts as the same thing over time, displacement, interaction between two structures, and acceleration.
- The architecture review sets out what each would require, and in what order. A self-made long-lived pattern comes first, then a rule for its identity, then displacement.

**None of this is attraction, force, or a statement about real space or time.**

## What I recommend next (not done)

1. **Principal: test whether the rules can maintain anything on their own, with no fixed reference.**
   - First agree on a short list of candidate patterns (a triangle, a star, a two-step path).
   - Then measure, exactly, how much longer each survives than its parts, against the no-rule baseline, in both ways of counting time.
   - It is cheap: under half an hour at 5–6 entities.
   - A "no" answer would be informative too: it would mean held references are not stand-ins for anything these rules make.
2. **Fallback: the reversal test.** Build the two reference shapes where the weak-rule formula says the more-supported site should win, and run them at full strength. It takes minutes and decisively tests the formula against the plain support explanation.
3. **Anytime, without an experiment:** the second-order mathematics that would explain the PATHF/PATHH difference and the reinforcing remainder.

## Decisions I need from you

1. Which next step: the persistence test (with definitions agreed first), the reversal test, the second-order mathematics, or a pause?
2. If the persistence test: which patterns, which baseline, and which time lags for the hub control (see the options document)?
3. Should the cross-programme suggestions (`docs/gt-p008-cross-programme-transfer.md`) go to the Constraint Laboratory?
4. Should the revised ontology proposal (OP-16, now qualified) and the new one (OP-18, "persistence before reference") be adopted?

## Integrity questions (GT-P008 §5), briefly

1. **Does the support formula imply the sorting direction?** No. It gives an exact local lever. The direction also depends on held degree (at first order) and on a global remainder (at full strength). Reversal shapes exist.
2. **What is the remainder?**
   - Four-path: held degree (at first order) plus second-order effects that split PATHF from PATHH.
   - Open path's closing link: it equalises internal support, and the middle's advantage then disappears.
   - Star against four-path: total support does not decide either the sorting or the margins.
3. **What do the clocks do?**
   - Support never changes the cycle balances that carry direction.
   - It changes one-step chances exactly, time-based occupancy through the lever plus the remainder, and event-based occupancy additionally through how fast states turn over.
4. **How much gathering is crowding?** Most of it. Adjusted margins are near zero or negative, except CSPH under the single link. At 6 entities, 12–31% of the baseline weight sits on rarely visited crowding levels.
5. **What is the status of E3B's neutralised triangle?** It is an instrument, not a rule. E4 confirmed that support suppresses links, but not E3B's stronger gathering.
6. **What does "emergent" mean?** Five different things: instant selection, a conditioned frame, a symmetry of the long-run law, genuine (temporary) persistence, and identity across change. Only the last two would count. None has been shown.
7. **What capabilities now exist?** Exact sorting mechanics around fixed structures. Drift, displacement, acceleration, metric and physical time remain undefined and are not equated with event order.
8. **Where are the explanations independent of gravity?** All of them. The lever, the degree effect, the clock separation and the exchangeability limit are facts about this relational grammar.
9. **What did this fail to resolve?** The full-strength remainder, the reversal shapes at full strength, the triangle's actual suppression, the four-path event-clock exception, second-order theory, and anything at 7 or more entities.

## Where to look

| What | File |
| --- | --- |
| This report | `gravity-time/reports/gt-p008-consolidation-report.md` |
| The mathematics, every claim labelled | `gravity-time/docs/e4-sorting-mechanism-derivation.md` |
| Re-read published numbers (post hoc) | `gravity-time/reports/gt-p008-secondary-analyses.md` (+ `.json`) |
| What a self-made reference would need | `gravity-time/docs/reference-architecture-review.md` |
| Next-step options and decision gates | `gravity-time/docs/gt-p008-next-round-options.md` |
| Starting audit and corrections to earlier wording | `gravity-time/docs/gt-p008-coverage-and-integrity-audit.md` |
| What was done, in what order | `gravity-time/provenance/execution-GT-P008.md` |
