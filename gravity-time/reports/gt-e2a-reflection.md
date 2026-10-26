# GT Round E2A — recursive reflection and the E2A → E2B selection

*Prompt GT-P005, deliverable 4.*
- *Written after the E2A results (result commit `32ac7f6`, tables payload `e4147f1e181b`), and before any E2B code, plan or cell.*
- *Numbers are from `reports/round-e2a-tables.json`; every cell is in `reports/gt-e2a-atlas.md`.*
- *Layers: [O] observation, [M] mechanism, [RS] interpretation; [P] none; [T] none.*

## 1. What E2A observed

1. **The pre-freeze identity held everywhere** [M, O].
   - A = σ·(deg r − deg q) held on every intact square of all 46 cells (I1, error ≤ 1e-15).
   - Disjoint squares carry zero affinity (I2).
   - All 10 σ = 0 cells are reversible (I3).
   - At HELD N=5 no attachment/probe square is reversed (I5, 20 of 20).
   - The affinity was also recomputed from the rule strings with exact fractions on 120 sampled squares per cell, and agreed.
2. **The aggregated orientation follows σ in every irreversible cell** [O]. This covers 32 cells with σ ≠ 0, across five grades, two modes and two sizes, with the partner-frame index and (HELD) the handover index. One cell (HELD PATHF strong_favour, index −7e-13) falls below the declared 1e-12 floor. Its sign agrees, but it is recorded as zero.
3. **The handover reverses when σ < 0, and the reversal is large when the cell is not saturated** [O].
   - The opposed-density cell ADPF (strong adjacency suppression plus path_form weak_favour, σ = −log 2) is unsaturated at HELD N=5 (4.3 relations). It carries flux 0.152 with handover index −0.112, as strong as any forward handover.
   - Every other σ < 0 cell saturates (10 of 10 relations). Its reversed index is real in sign but tiny, from 1e-12 to 4e-5.

   So E1's 30/30 invariance was a property of the σ > 0 families chosen, not of path rules.
4. **Local affinity does not describe all of the current** [O].
   - In every irreversible cell, between 6% and 36% of the circulation on adjacent squares runs against the affinity of its own square.
   - Squares on disjoint slots have zero affinity, yet up to 35% of total flux passes across their edges in an oriented way (HELD N=6). This is current threaded through by neighbouring cycles.
   - The net oriented circulation on attachment/probe squares nevertheless has the sign of σ in every cell, including HELD N=6, where 1,152 of 13,824 such squares with nonzero affinity are locally reversed.
5. **In soft rules, the handover's release step is an opportunity effect, not enabling** [O].
   - Look at the step "probe–probe dissolves, then attachment dissolves" (DP→DA) in HELD PATHH weak_favour. Removing the probe–probe relation **lowers** the attachment's own dissolution rate (log ratio −0.17, since it loses path witnesses).
   - It also removes a fast competing event from the total. Attachment dissolution becomes the more likely next event (log jump ratio +0.39), entirely through the normalisation (+0.56).
   - The effect on passage within 8 events is +0.011.
   - In PATHF weak_suppress the step is pure normalisation (rate change 0).
   - **No soft cell shows strict enabling.**
6. **Strict enabling occurs only with a hard component, and its relation to directed succession varies** [O].
   - **EXCL** (hard closure exclusion): strict enabling (removing one attachment of a probe makes another attachment admissible in 87% of matched cases) and **no arrow**. The cell is reversible.
   - **EXPH / EXPF** (hard closure exclusion plus a path term): strict enabling **and** circulation following σ.
   - **Hard path-form prohibition (FREE)**: strict enabling (adjacent 19%, disjoint 47% of matched cases) **and** the largest FREE flux in the round (0.23), with **σ = 0**. No intact square carries affinity; the flux runs on 510 one-way transitions. Its partner index is +0.108.
7. **One-step precedence does not track enabling** [O]. In the hard path-form cell, after an executed dissolution, the formations it strictly enables are *less* likely than average as the next event (precedence 0.72 adjacent, 0.95 disjoint). An intervention instrument and the observed sequence answer different questions.
8. **The partner frame reads FREE circulation better than the existing frames** [O]. Its index is 1.3–2.3 times the hub-frame asymmetry and 7–32 times the class-free asymmetry in every FREE irreversible cell. It needs no held source.
9. **The scaffold is itself a witness** [O, M]. Under hard path-form prohibition in HELD, the source triangle supplies a two-path to every attachment slot, so no attachment can ever form. The cell is a trivial probe-only chain. The imposed reference changes what a hard rule can do.
10. **Hard path-dissolve prohibition arrests** [O]. Both modes are absorbing in the complete graph: once supported, nothing can be released.

## 2. What was unexpected

- **The size of the reversed handover in ADPF.** The opposed-density cell was predeclared, but nothing predicted that reversal would be as strong as the forward handover once saturation was removed.
- **A directed mode of succession with σ = 0.** Hard path-form prohibition produces the strongest FREE irreversibility in the round, with no local cycle affinity at all. It is a distinct mechanism (one-way admissibility), not a soft cycle.
- **Enabling is invisible in precedence.** Strictly enabled events are *not* over-represented right after the enabling dissolution.
- **Strict enabling with no arrow** (EXCL). The CL-Q05 sense of "dissolution enables a distinct configuration" is fully present in a reversible chain.
- **Current through zero-affinity squares.** Its scale is large, up to 35% of flux.

## 3. How the explanation changed

| Level (GT-P005 section 3) | After E2A |
| --- | --- |
| Local rate asymmetry | The path components' cross-counts are asymmetric (far-endpoint degree); closure and adjacency are symmetric |
| Cycle affinity | Exact identity A = σ·Δdeg on adjacent squares, 0 on disjoint ones (theorem, all positive-factor rules) |
| Stationary current | Follows σ in aggregate (32/32), but not square by square (6–36% counter), with large through-flow on zero-affinity squares |
| Event-order asymmetry | Handover and partner indices take the sign of σ. At saturation they are real but negligible. The one-step release looks like enabling but is normalisation |

The handover orientation now has a **proven local explanation**, with a stated domain. Its **aggregated orientation** is an empirical regularity over the 32 cells, with no counterexample found. Its **causal reading** ("dissolution enables the next step") is **not supported** in soft rules: it is kinetic sequencing through competition for the next event.

## 4. Live possibilities after E2A

| Possibility (from GT-P005 section 1) | Status |
| --- | --- |
| Orientation follows the signs and incidence of the PATH rules | **Locally proven;** aggregated in 32/32 |
| Contingent on grading, support or frame | **Grading: yes** (sign of σ); **frame:** the partner frame generalises the source frame |
| Local affinity with weak, absent or reversed aggregate | Weak/absent at saturation; no aggregate reversal; square-level counter-circulation is common |
| Dissolution raises later event probability without changing admissibility | **Yes, in every soft cell,** mostly through normalisation |
| Dissolution opens a pathway only with hard constraints | **Yes;** and then it may or may not come with direction |
| Several micro-cycles hidden in the handover | Role classes differ (attachment/attachment squares carry balanced ± affinity; attachment/probe squares carry the signed part) |
| Other forms of ordered succession | **Yes:** a one-way admissibility mode with σ = 0 |
| Grammar forbids some behaviours | Hard path-form plus HELD forbids attachment; hard path-dissolve arrests |

## 5. Selecting E2B

Candidates were compared factor by factor (OTR section 6), with no combined score.

| Candidate | Information value | Novelty | Discriminates | Cost | Risk |
| --- | --- | --- | --- | --- | --- |
| **Hard/soft interface: strict enabling, one-way succession and σ** | High: the only place where enabling and direction meet; the one-way mode is unexplained | High: a new mode | Is one-way succession oriented by its own rule? Does σ still predict orientation with a hard component? When does enabling bring direction? | Low (N=5) | Must not "build" an enabling example. Mitigated by a full hard × soft cross with negative controls |
| Search for aggregated-orientation counterexamples among soft rules (mixed strong/weak path pairs) | Moderate | Low | Tests the 32/32 regularity | Low | More of the same pattern |
| Precedence versus intervention, finer horizons | Moderate | Low | Measured in E2A already | Low | Low |
| Through-flow on zero-affinity squares (cycle decomposition) | Moderate | Moderate | Mathematical | Moderate (needs cycle-basis machinery) | Mostly known Markov mathematics |
| FREE N=7 hubs, source-size control, clock split (GT-Q09) | Low for this mandate; not authorised (FREE N=7) or not addressed by E2A | — | — | High | — |

**Choice: E2B maps the hard/soft interface at N=5.** The reason is that E2A revealed three relations between strict enabling and directed succession:
- enabling without direction (EXCL);
- enabling with soft direction (EXPH/EXPF);
- enabling with one-way direction (path-form prohibit, σ = 0).

The soft-rule handover itself turned out not to be enabling. The most informative next boundary is where admissibility, not rate, structures succession.

**Design principles fixed here, before writing E2B:**
- **Hard components:** the three existing hard formation exclusions — path_form prohibit, close_form prohibit and adj_form prohibit. The last is new: formation is forbidden while either endpoint has any neighbour.
- **Each crossed with soft path terms of both σ signs** (path_dissolve weak_favour, path_dissolve weak_suppress, path_form weak_suppress, path_form weak_favour), plus no soft term.
  - Combinations already run in E2A are cited, not re-run.
  - path_form soft terms are omitted under path_form prohibit, where they can never act.
- **New observables:**
  - the share of flux carried by one-way transitions;
  - one-way transitions classified by the partner-frame degree sign;
  - a race committor: after removing g, the probability that the enabled slot f toggles before g is restored.
- **Comparators and controls:**
  - the reversible hard-gradient cells (adj_form prohibit alone, close_form prohibit alone, cited from E2A);
  - the σ > 0 and σ < 0 soft partners with no hard component (cited from E2A);
  - NULL.
- **Held out for a future confirmatory test:** N=6 FREE, the strong grades, and the close_dissolve / adj hard dissolution rules (arrest-prone).
- **E2B is adaptively chosen.** It is not independent confirmation of anything in E2A.
