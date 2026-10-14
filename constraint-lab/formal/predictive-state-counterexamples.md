# Exact counterexamples and false converses

These are tiny symbolic mathematical fixtures, not new Constraint Laboratory
controllers, scientific cells or parameter searches. Their all-order arguments
are explicit below; bounded unit checks supplement rather than replace proof.
No scientific freeze is needed for these formal counterexamples.

## CE-TRACE: Trace equivalence need not be strong lumpability

| State | Observation | Transition |
| --- | --- | --- |
| s | A | u with 1/2, v with 1/2 |
| t | A | w with 1 |
| u | B | c with 1 |
| v | B | d with 1 |
| w | B | c with 1/2, d with 1/2 |
| c | C | c with 1 |
| d | D | d with 1 |

From s or t the future is B,C,C,... or B,D,D,..., each with mass 1/2.
This characterises EVERY finite word, not merely a finite-depth comparison.
Their two-step represented-state distributions agree and the intermediate
observation is B in either case.

Strong refinement first splits u,v,w by next-C probabilities 1,0,1/2.
It then separates s,t by their masses into those three blocks. Thus s,t are
trace equivalent but not in one strong block. The all-word equivalence partition
is not itself strongly lumpable. This is the standard branching-versus-linear
distinction, not a claim that the fixture discovers a new phenomenon; see the
[primary literature map](predictive-state-literature-map.md).

## CE-WEAK: First-order observations need not synchronize the strong refinement

States are (y,h) in {0,1}^2; observe y. Let

    T((y,h),(y',h'))=p_h(y')/2,
    p_0(1)=1/4, p_1(1)=3/4.

All entries are positive. The joint uniform law is stationary: every target
column sums to one. At each transition h' is redrawn uniformly independently
of y'. At stationary initialization and after any observed history, h_t is
therefore uniform conditional on current y_t. The output is iid fair binary,
hence first-order in the convention r>=1.

At fixed y the two hidden states have next-1 probabilities 1/4 and 3/4, so the
coarsest strong refinement consists of four singletons. Every finite observed
word leaves both current h values possible. No finite worst-case synchronization
length exists, even though the observed Markov order is one.

This also supplies a fully positive stationary WEAK lumping that is not strong.
It does not make 8H/8I's one-step invisibility a weak lumping: those outputs
have actual order-two dependencies.

## CE-EVEN: Three strong predictive states can have infinite observed order

Use states a,b,c, with observations 0,1,1 and transitions

    a -> a with 1/2, b with 1/2
    b -> c with 1
    c -> a with 1/2, b with 1/2.

Uniform (1/3,1/3,1/3) is stationary. The strong refinement has three singletons:
b and c differ in next-zero probability 0 versus 1/2.
Starting from an observed zero, each run of ones has even length before the
next zero. After a positive word 0 1^n, the endpoint is b if n is odd and c if
n is even. Choose arbitrarily long positive words with these different parities
but the same last r symbols (all ones). Their next-zero probabilities differ
for every finite r. Thus stationary observed Markov order is infinite.

No uniform finite synchronization length exists. Occurrence of a zero does
synchronize, and under stationarity a zero occurs almost surely eventually:
that is not worst-case bounded suffix synchronization.
Small strong-state count alone therefore bounds neither synchronization length
nor observed Markov order. This is not a claim that the N4 laboratory has
infinite order; its reviewed 8I processes have the proved finite orders.
If the three represented states are ordinary X with H=0, this is purely
projection-induced infinite order. Observed order alone does not establish a
history-axis capability or necessary generative H depth.

## CE-SUPPORT: Kernel flattening does not create missing event support

Let the ordinary state have two preserved binary coordinates x. A finite fixed
kernel gives x xor 1, x xor 2 and x xor 3 probability 1/3 each in one tick.
Add passive finite coordinates if desired; flattening into a fixed kernel is
immediate. Both ordinary single-bit toggles have positive probability.

An ordinary grammar restricted to exactly one ordinary bit flip per tick gives
x xor 3 probability zero, regardless of positive factors, hidden registers or
K/J budgets. Therefore it cannot represent this kernel while preserving ordinary
coordinates, output X and clock. The obstruction is support, not a poor fit.
Intermediate microsteps, altered support or changed observation are different
compiler permissions, not solutions in this class. CL-T12 never supplied them.

## CE-CLOSURE: Finite eta alone does not give joint Markovity

Let X_(t+1)=X_t xor X_(t-1) and eta_t=0 always.
The augmented pairs (X_(t-1),X_t) have deterministic cycle
(0,1)->(1,1)->(1,0)->(0,1); initialize uniformly on that cycle.
At current X=1, previous 0 and 1 both have positive probability and imply
different next X. Thus (X,eta) is NOT first-order, although eta is finite and
itself Markov. Capturing all relevant joint dependence is a necessary
hypothesis of the augmentation theorem; a finite register's existence is not it.

## Existing canonical counterexamples, reused without new cells

| Tempting converse | Existing obstruction |
| --- | --- |
| Same occupancy implies same dynamics | 8H CL-T31/T34: uniform occupancy for all m, different backtracking |
| Stationary one-step matching implies full process equality | 8H/8I CL-T31/T55/T56: same adjacent laws, different triples/order |
| Visible graph isomorphism alone implies a valid quotient | F011-QUOTIENT-INVALID; the complete law's stabilizer matters |
| Finite history alphabet determines temporal depth | A passive arbitrarily deep record can be irrelevant to an observation; a recursively updated one-bit cumulative parity can depend on an arbitrarily old event |
| Kernel conjugacy alone preserves a fixed observable | Conjugacy must transport the observation and relevant initial law too; 8F hidden-coordinate maps declared these obligations |

The first three are cited historical results, not re-executed scientific cells.
Last-pair depth, observed order, state count and alphabet size must not be
collapsed into one memory or complexity score.
