## Proposed solution

Both arguments support the claimed all-positive-\(m\) route-null identities within the stated scope: stationary graph-class-conditioned sources, complete graph-class target vectors, and the original fine states. I found no counterexample to the regeneration or flux arguments.

The proof should make several currently implicit justifications explicit, especially the meaning of “invariant killed occupation,” the distinction between raw weights and normalized transition probabilities, and the use of the lifted Kpi readout in the support argument.

## Important claims

- For R00/R01/R02, ANY or FORM, \(k=2\) DOWN, the first entrance into \(J\) has a universal uniform distribution on its 36 original fine states. Subsequent occupation on \(J\) is consequently source-proportional, giving \(U_J=0\).
- For FORM R04/R11, \(k=3\) UP, the stated flux equations are correct. Their denominator is positive for every \(m>0\), so they imply active-coordinate centering for every stationary source class.
- These conclusions establish route-null identities and sufficient cancellation mechanisms. They do not establish parameter-independent support classifications or exclude additional nulls.

## Supporting reasoning

### Regeneration

The role definitions imply that R00/R01/R02 can select an event only when \(h_1=h_2\).

A first downward step from count 2 produces a count-1 state in \(E\): its newly dissolved edge is \(h_1=i\), absent from the material, and the remaining present edge is \(f\ne i\).

The only internal successor of such an \(E\) state is obtained by dissolving \(f\), producing the empty state with histories \((f,i)\). These histories differ, so all six formation weights at this empty state equal 1. This conclusion holds even when dissolution from \(E\) was biased under ANY.

For each stationary graph-class source, covariance makes the aggregate flux indexed by \(f\) uniform over the six edge labels. Therefore the next formation \(e\), uniformly chosen independently of \(f\), produces the \(J\) state
\[
(\{e\},e,f)
\]
uniformly over all 36 pairs \((e,f)\).

There is no direct source injection into \(J\), and \(E\) cannot be revisited during the killed excursion: every internal entrance into count 1 is a formation and therefore has present \(h_1\). Once the common entrance distribution on \(J\) is reached, subsequent dynamics remain within \(J\) and count 0 until killing. Thus, for a common occupation row \(r\),
\[
b_c|_J=\alpha_c r.
\]
Stationary block balance gives
\[
\pi|_J=\left(\sum_c\pi(c)\alpha_c\right)r.
\]
This yields the required conditional centering \(U_J=0\), including fibrewise centering over \(h_2\).

The count-0 claim requires the lifted Kpi hitting vector: every successor lies in the same coarse \(J\) orbit, so applying the fine transition kernel gives a history-independent value there. It should not be justified merely by asserting that the full fine-state hitting vector is constant on \(J\); that stronger assertion is unnecessary for R01/R02.

### High-side readout

At count 5 with \(h_1\) equal to the missing edge, the FORM selector is inactive. Let its coarse hitting value be \(g_A\). Harmonicity gives
\[
6g_A=g_6+4g_{JA}+g_{JD}.
\]
At full material, every dissolution leads to this same coarse orbit, so \(g_6=g_A\). Hence
\[
5g_6=4g_{JA}+g_{JD}.
\]

At an arbitrary count-5 fine state, all five dissolution weights are 1. The formation weight is either 1 or \(m\), and its successor has value \(g_6\). The displayed identity therefore makes the normalized continuation equal to \(g_6\) in either case. Count 6 follows immediately. This establishes \(W_5=W_6=0\).

At count 4 with absent \(h_1=i\) and other missing edge \(j\), only \(h_2=j\) can activate FORM selection, and only when the relation of \(i,j\) is selected. All remaining histories have identical unit-weight rows within the fibre. Thus the readout has at most two levels.

### Flux and centering

The source enters the high side only at count 4 with present \(h_1\). Consequently the absent-\(h_1\) count-4 fibres, count 5, and count 6 have no direct source terms in their occupation balances.

Write \(x=b_c(\text{count }6)\). Covariance makes the count-6 marginal for each \(h_1\) equal to \(x/6\). Full-material transitions have probability \(1/6\) for every dissolution. A count-5 state with missing edge \(j\), \(h_1=j\), and specified \(h_2\) therefore has occupation \(x/36\).

Its next dissolution gives the active count-4 coordinate with occupation \(x/36\), after summing over its possible predecessors. This derivation uses the fact that the count-5 selector is inactive when \(h_1\) is its missing edge.

For fixed count-5 material, the probability of any specified dissolution is independent of which present edge is dissolved. It may depend on history through the common row denominator. Thus total inflow into a count-4 absent-\(h_1\) coarse fibre is independent of the dissolved edge. Covariance across the missing edge then makes its mass \(y\) common to all ordered distinct missing-edge pairs. Covariance alone would not establish this, because ADJ and DISJ pairs are different orbits.

The active count-5 occupation is
\[
\beta
=\frac{y-x/36}{6}+\frac{mx}{36D}
=\frac y6+\frac{5\delta x}{216D}.
\]
For fixed count-5 material there are exactly \(v\) active histories. All others have denominator 6, giving the stated balances
\[
y=\frac f6+v\beta\left(\frac1D-\frac16\right),
\qquad
\frac x6=\frac f6+v\beta\left(\frac mD-\frac16\right).
\]
Their elimination yields
\[
\frac xy=
\frac{36D(6D+v\delta)}
     {36D^2-5v\delta^2}.
\]

For \(v=1,4\), numerator and denominator are positive for every \(m>0\). The stationary restriction satisfies the same balances. Its active coordinate has mass \(\pi_6/36\), so equality of these ratios gives precisely \(U_{\mathrm{active}}=0\). Two-level readout and fibrewise zero sum of \(U\) then prove cancellation.

## Assumptions

- “Invariant” means invariant under vertex relabeling.
- The killed occupation comes from the specified stationary class-conditioned source on the return layer. Arbitrary invariant injections at counts 5 or 6 would introduce extra balance terms.
- The projection defining \(U\) uses stationary conditional distributions in each coarse fibre.
- The Kpi hitting vector is covariant for graph-class targets, and \(V,W\) have the intended lifted-readout definitions.
- Positive finite \(m\) ensures positive event probabilities, access to the return layer, and finite killed occupation.
- Stationary block balance uses all graph classes on the complete return layer.

## Counterexamples/failure modes

- Arbitrary hidden source priors can destroy uniform regeneration flux or entrance-only centering.
- Label-specific targets can distinguish the coarse \(J\) successors and invalidate the count-0 readout argument.
- Replacing FORM by ANY in the high-side proof invalidates the claim that every dissolution has unit weight.
- Treating “unit weight” as “probability \(1/6\)” at active count-5 states would invalidate the flux calculation; the proof correctly uses \(1/D\) there.
- S4 covariance alone cannot equate ADJ and DISJ missing-pair fibre masses.
- General independent event weights need not preserve either regeneration or the flux equations.
- No conclusion at \(m=0\), infinite \(m\), or about additional nulls follows from these proofs.

## Unresolved issues

The document does not define \(P,Q,U,V,W\) sufficiently for a fully standalone audit. In particular, the count-0 argument should explicitly identify \(V\) as the relevant continuation of the lifted Kpi hitting vector.

The phrase “for any invariant killed occupation” should be narrowed to occupations generated by the stated return-layer sources. Subject to that scope and the intended definitions, I found no invalid regeneration or flux step.

## Self-check

I reconstructed the entrance law, both flux balances, their elimination, denominator positivity, and the active-coordinate centering implication independently from the document and role definitions. I read no sibling work, made no edits, ran no scientific cells or parameter computations, and introduced no new scientific points. Agreement with another audit would not itself strengthen the proof.
