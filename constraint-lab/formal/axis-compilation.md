# Axis compilation and the H/L boundary

This document specifies formal boundaries and future design sketches. It
implements no H2 controller, dynamic rule state, new support or scientific
computation. [State taxonomy](state-taxonomy.md) fixes X,H,eta,Z and observations.

## 1. A compilation class, not unqualified irreducibility

Write mathfrak-A for an explicit class of admissible compilers. A compiler takes
a source representation to a target representation and must preserve a declared
equivalence E. Record at least:

| Dimension | Required declaration |
| --- | --- |
| State | Baseline coordinates; permitted enlargement, recoding and hidden variables |
| Support | Permitted event targets, self-loops, simultaneous or register-only updates |
| Clock | One-for-one steps, permitted microsteps or epoch/time change |
| Observation | Preserved phi, allowed renaming/coarsening, comparison domain |
| Parameters | Exact alphabet, continuous factors or finite grades |
| Grammar | Existing parser/backend versus bounded runner; allowed K and J |
| Semantic typing | Whether H or eta may become ordinary relation/entity coordinates |
| Equivalence | All conditioned rows, conjugacy, all observed words, stationary words, or a statistic |
| Priors | Every reachable start or one declared transported initial law |

Define a successful compilation as an admissible transformation in mathfrak-A
whose resulting model satisfies E on its declared domain. One unsuccessful
compiler attempt is not proof that every admissible compiler fails.
An irreducibility statement has no determinate scope until these choices are
fixed. Symbols, hidden-state names or an attractive interpretation are not
capability witnesses.

## 2. Current-state compilation

CL-T12 gives arbitrary STRICTLY POSITIVE current-state event-weight rows on the
existing single-toggle support, using arbitrary positive factors and sufficient
K/J. It does not give missing targets, hard-zero universality, simultaneous
ordinary updates, free memory state or changed-clock equivalence.

At a fixed unchanged X, a fixed first-order kernel supplies one row. The 8H
same-X histories require two different rows, excluding EVERY such compiler,
even with unbounded K/J (CL-T28). At fixed enlarged (X,H), no analogous raw
kernel contradiction follows: the enlarged states are different.

<a id="cl-t64"></a>
## 3. CL-T64: Finite-history Markov augmentation

Let X,H,E be finite. Assume that conditional on the ENTIRE past the next event
and material successor have one homogeneous kernel

    W(e,x' | x,h),
    h'=U_H(h,x,e,x').

Then define

    T((x,h),(x',h')) =
      sum_e W(e,x' | x,h) 1{h'=U_H(h,x,e,x')}.

Each term is nonnegative. Summing over x',h' gives one because each event has
one history-update target and W is stochastic. Conditional on the past the
right side depends only on current (x,h); hence this is the exact homogeneous
first-order joint kernel. A stochastic history update can replace the indicator
by a normalized conditional update kernel; no independent-noise assumption is
needed if the full joint conditional law is specified correctly.

The theorem is prior-free once an initial joint law is supplied. It says
nothing about whether H fits the original event grammar or entity-state S.
A finite alphabet, recursive notation, or Markovity of one coordinate ALONE
does not establish the hypothesis. CE-CLOSURE gives a counterexample.

<a id="cl-t65"></a>
## 4. CL-T65: Finite constraint-state kernel flattening

Let X,H,eta,E be finite and let ONE fixed meta-programme specify a closed,
homogeneous next-event/material law and joint H/eta update using only current
(X,H,eta), the event and its material successor. Sum over the events and update
outcomes exactly as in CL-T64. The result is a fixed finite stochastic kernel on
the product Z=(X,H,eta), reproducing its finite-dimensional joint process law.
Only reachable product states need be represented; the product cardinality is
an upper bound, not a claim of minimality.

Equivalently, if the current Z is already joint Markov-sufficient, its
constraint-oriented interpretation does not stop its row table from being T.
Finite eta or marginal Markovity of eta alone is NOT sufficient: X might still
read omitted history, a clock phase, an external driver or another interpreter
state. That missing information must be included; it need not have a finite
augmentation in arbitrary systems.

Thus finite closed L-style dynamics do not automatically add raw finite-kernel
expressivity when unrestricted augmentation is admitted. They may still expose
meaningful semantic architecture, modularity or compression under a specified
compiler. No unrestricted self-modification or physical ontology theorem follows.

<a id="cl-t66"></a>
## 5. CL-T66: A support obstruction survives flattening

Suppose every admissible target grammar event changes exactly one preserved
ordinary bit, and the clock preserves one event per tick. Then every target
one-step ordinary transition has Hamming distance one.
If a source gives positive probability to a different ordinary distance, no
such compiler can match its one-step ordinary rows. Arbitrary hidden variables,
positive weights and K/J do not alter this support invariant.

CE-SUPPORT gives a tiny exact source with all ordinary single-bit moves present
AND an additional two-bit move. A fixed finite kernel exists, but the additional
ordinary target cannot be manufactured by adjusting weights.
Microsteps, recoding the observed ordinary coordinates or different event support
change mathfrak-A. This is a formal obstruction, not an executed L capability.

## 6. Three different compilation questions

| Level | Question | Status for finite closed history/eta |
| --- | --- | --- |
| 1: Kernel | Fixed kernel on some augmented finite state? | Yes under CL-T64/T65 hypotheses |
| 2: Support-preserving grammar | Existing event grammar, support and clock? | Not guaranteed; CL-T66 gives an obstruction |
| 3: Ontology/category preserving | Without reclassifying H/eta as ordinary coordinates? | Requires an explicit semantic compiler contract |

These are distinct permissions, not automatically a total order of compiler
classes. Adding semantic preservation to a specified level-2 class creates a
smaller class; allowing different support at level 3 need not.

## 7. Costs and novelty taxonomy

Record separately: augmented-state count, extra variables, support changes,
K increase, J increase, parameter alphabet and synchronization burden.
Do not sum incompatible dimensions.

| Novelty class | Required evidence | What is insufficient |
| --- | --- | --- |
| Process-expressive relative to mathfrak-A | No admissible compiler preserves the specified process equivalence | One failed implementation or a new name |
| Representation | Strict baseline fails but explicit enlarged/recoded state succeeds | Calling enlargement absolute non-Markovianity |
| Semantic/modular | Explicit architecture preserved by the new representation but not a declared flat compiler | Merely interpreting a hidden bit as a rule |
| Compression | Constructive upper bound and justified lower bound or cost separation under stated budgets | Largest effect size or smaller counts under a different observation without qualification |
| Observational | A declared process distinction survives one observation but not another | Assuming universal information monotonicity |

Classes can overlap. 8H has process-expressive novelty relative to unchanged X
and representation novelty when augmentation is allowed. 8I's compression is
lossless for each DECLARED observed target, not a two-state representation of all
labelled-mask futures. Moving between observation levels changes the question.

<a id="cl-m04"></a>
## 8. CL-M04: Permanent axis-novelty test

Before claiming a new axis, declare baseline represented state; event support;
clock; observation; compiler class; grammar/alphabet/K/J budgets; equivalence;
and initial-law quantifiers. Attempt an explicit compiler. If alleging
impossibility, give a witness valid against ALL admissible compilers.
Classify process-expressive, representation, semantic/modular, compression
or observational novelty separately, retaining unresolved alternatives.
This is a methodological principle, not a new physical or kernel theorem.

<a id="cl-m05"></a>
## 9. CL-M05: Explanatory compression as a model-design principle

A representation may be useful when it exposes a small sufficient structure
for declared predictions that is obscure in a flat encoding.
Check the prediction target, equivalence, costs and lost distinctions explicitly.
This is an argued design principle, not a theorem that smaller representations
are always more explanatory or that any such representation is nature's ontology.
8I is a concrete worked example, not a universal compression sequence.

## 10. Unexecuted H2 design

Hold N4/O3, all ten ordinary bits, support and pair-clock semantics fixed.
Propose a two-slot register (h_1,h_2), initially both sentinel, with pair update
(h_1,h_2)'=(e,h_1); triad events preserve it. The hypothetical fixed law weights
the candidate equal to h_2 by m>0, others by one, and is neutral before h_2 exists.
It reads whichever older slot occurred, not a privileged pair name.

Choose distinct a=01,b=12,c=23. From all-zero ordinary X and the same sentinel
register compare proposed formation words (a,b,c) and (b,a,c).
Both have the same event count/multiset, complete endpoint X (path 01-12-23,
all triads absent), and h_1=c. Their h_2 are b and a.
Positivity would make both paths legal under the SAME proposed law.
At the endpoint the next pair-slot b probabilities would be m/(m+5) and
1/(m+5); full-event denominators would be m+9. No value is executed here.

The excluded H1 compiler reads only (X,h_1), preserves support/clock/observation,
and may have arbitrary K/J but NO extra hidden state, seed, time phase or
enlarged/reinterpreted register alphabet. One row at the identical endpoint
cannot match both proposed non-neutral rows. Two prior slots would suffice
for this specified law; a generic larger finite register could encode them too.
The latter is explicitly OUTSIDE the claimed H1 class, not an absolute
non-compilability theorem.

Neutral control m=1 removes the conditional distinction. The need for depth two
would be falsified for a proposed case if h_2 were recoverable from (X,h_1) on
its reachable domain, endpoints differed, a path were impossible, future rows
coincided, or a legal compiler within the declared H1 class reproduced all rows.
Implementation and any scientific verification require a FUTURE separately
frozen prompt; no H2 branch is opened in 8K.

## 11. Unexecuted L design and its ambiguity

A minimal diagnostic candidate uses eta in {0,1} to enable a predeclared
ordinary rule feature psi(X,e), with at least two candidate events receiving
different feature values. One fixed meta-programme decodes eta into the active
rule set. Initial eta is zero; it toggles when previous pair h_1=a and the new
pair is b; otherwise it is retained. Ordinary history H here means last-pair h_1.

The proposed (a,b,c)/(b,a,c) paths can then have identical X and h_1=c but
different eta, changing the enabled ordinary feature and future row.
Controls hold eta static or make the feature multiplier neutral.
This is a diagnostic design, not an executed L mechanism or a selected final
L grammar. No numerical result is reported.

Its limitation is decisive: eta is itself a function of ordinary event history.
It is historical by ORIGIN and constraint-configuring by ROLE.
Flattening to (X,h_1,eta) is allowed at kernel level and succeeds.
If declared H meant the COMPLETE ordinary past, deterministic eta derived from
that past could not differ while H was identical.
An alternative autonomous constraint event could separate origins, but would
change event support/clock and would need its own explicit future design.

Therefore the witness alone would establish dynamic constraint-state semantics,
not raw kernel advantage. A genuinely stronger L claim needs an independently
declared rule-decoder/semantic contract, support restriction or resource
separation that an admissible flat compiler fails. Which contract is scientifically
useful remains open. H2 is currently the cleaner nested capability test.

## 12. What the boundary does and does not settle

H summarises ordinary process history relative to X. eta configures constraint
machinery relative to a declared grammar. These descriptions can overlap.
Extensional finite kernels do not uniquely classify a coordinate as H or L.
Joint sufficiency permits flattening; representation, semantics and costs may
still justify maintaining the distinction. No L-positive empirical result,
ontology axis or claim of irreducible time is established by 8K.

## Generation 8L: executed strict-H1 compiler boundary

The earlier 8K designs remain historical and unexecuted THERE. H2-0 now verifies
the proposed common-start (a,b,c)/(b,a,c) witness at all three frozen grades.
At identical ten-bit X and last-pair h1=c, h2=b/a gives unequal ordinary full
and pair rows iff m!=1. CL-T69 rules out every fixed first-order compiler whose
state is exactly (X,h1), independent of positive K/J complexity.

Preserved: ordinary coordinates, single-toggle support, event clock,
observation, most-recent-pair semantics and all conditioned-row equivalence.
Excluded: hidden state, persistent random seed, phase/time, enlarged history
alphabet, recoding and per-history programs. The common-start witness makes
both conditions reachable under one law, not selected across experiments.

Unrestricted finite augmentation can encode the two-slot register in 36 values.
This does not satisfy the declared semantic H1 contract. The result applies
CL-M04; it does not defeat raw kernel flattening or resolve L semantics.
SECOND-RECENT is fixed throughout, so ontology L=0 remains unchanged.
See [history-depth proofs](history-depth.md#cl-t69).

## Generation 8M: Three Levels Of Structural Consequence

The strict semantic H1 compiler is exactly (X,h1), arbitrary positive K/J,
no recoding, hidden state, phase, changed support or clock. All non-neutral
one-role cells fail that row compiler. A stationary H1 Kpi nevertheless always
matches occupancy. H2-vs-uniform-H1 occupancy and H2-vs-Kpi longer-word gaps
answer different questions, neither defeating unrestricted augmentation.
The STAR/TRIANGLE conjugacy uses a non-vertex pair-coordinate permutation;
it is not an ontology-preserving identification of labelled relations.
See [ordered depth-two roles](history-role-depth-two.md).
