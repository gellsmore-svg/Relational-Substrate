## Proposed Solution

Both all-positive-\(m\) mechanisms are valid under the stated stationary-source and coarse-fibre conventions. I found no counterexample within that scope. The regeneration argument does give \(U_J=0\) for R00/R01/R02 ANY/FORM at \(k=2\) DOWN, and the R04/R11 FORM \(k=3\) UP flux equations give active-coordinate centering for every finite \(m>0\).

The presentation would benefit from explicitly defining the centering operator and distinguishing group invariance from stationarity. These are exposition gaps, not counterexamples to the reconstructed arguments.

This audit concerns stationary conditional graph-class sources, joint route contributions, graph-class targets, and original full states. It introduces no new scientific parameter point.

## Important Claims

1. Entrance-only status implies \(b_E=a_E\), but \(U_E=0\) additionally uses the stationary conditional-source construction.
2. For R00/R01/R02, the first entrance into \(J\) has a source-independent distribution on all 36 ordered history pairs.
3. The entire occupation on \(J\), including repeated visits, is consequently proportional across source classes.
4. For R04/R11, the common count-4 fibre mass \(y\) is justified across both ADJ and DISJ pairs; covariance alone would not establish this stronger equality.
5. The active count-4 fine-state mass is exactly \(x/36\), with \(x\) the total count-6 occupation.
6. The displayed flux ratio is algebraically correct, with a denominator strictly positive for \(m>0\).
7. The resulting argument proves the target-vector null, not a classification of all possible parameter-dependent supports or additional nulls.

## Supporting Reasoning

### Entrance States and Centering

The intended centering is
\[
U_z=b_z-\frac{b_S}{\pi_S}\pi_z
\]
for the coarse fibre \(S\) containing \(z\).

For either entrance set \(E\), no killed predecessor exists, so \(b_E=a_E\). The stationary conditional-source assumption supplies the further fact needed for centering: the predecessor material mask is determined by the arrival coarse state \((p,h_1)\), namely \(p\mathbin{\triangle}\{h_1\}\). Its graph class is therefore constant throughout that coarse fibre.

Because all stationary inflow into \(E\) comes from the source layer, \(a_c\) on a given entrance fibre is either zero or a fixed scalar multiple of \(\pi\). Thus \(U_E=0\). Entrance-only status alone would not prove this for arbitrary hidden source priors.

### R00/R01/R02 Regeneration

For \(k=2\) DOWN, the killed domain contains counts 0 and 1. Every route entrance is a count-1 state whose newest event dissolved an edge, hence \(h_1\) is absent: the entrance belongs to \(E\).

Write its sole present edge as \(f\) and its absent \(h_1\) as \(i\), with \(f\ne i\). The only internal event from \(E\) dissolves \(f\), producing
\[
(\varnothing,h_1=f,h_2=i).
\]
The histories are now distinct. R00/R01/R02 require equal history slots, so all six formation weights at this empty state are 1 for either ANY or FORM.

The total flux of dissolutions labelled \(f\) is uniform over the six labels. This follows from \(S_4\) invariance of the source occupation and covariance of the event probabilities, including any history-dependent rate at the preceding \(E\) state. It does not require the full \((f,i)\) distribution to be uniform.

The next event \(e\) is uniform independently of \(f\), and the resulting \(J\) state is
\[
(\{e\},h_1=e,h_2=f).
\]
Consequently, its entrance measure is a scalar multiple of the uniform measure on all 36 ordered \((e,f)\) pairs. Equality \(e=f\) is included.

There is no other route from \(E\) into \(J\), and the process cannot return to \(E\). Restricting the subsequent killed chain to counts 0 and \(J\), every source therefore has occupation
\[
b_c|_J=\lambda_c r
\]
for the same row \(r\). The common row includes arbitrarily many subsequent visits; the claim is not limited to first-entry distributions.

Stationary block balance gives
\[
\pi_B=\sum_c\pi(c)b_c
\]
for the complete source-layer class partition and joint first-step entrances. Hence \(\pi_J\) is also proportional to \(r\), proving \(U_J=0\).

At count 0, the lifted coarse hitting vector on a successor \(J\) fibre is constant over the six present-edge labels by \(S_4\) invariance and graph-class targets. Thus its one-step continuation is history independent, giving \(W_0=0\).

These statements cover every killed state: \(U_E=0\), \(U_J=0\), and \(W_0=0\).

### R04/R11 Readout Structure

For FORM R04/R11, only candidate \(h_2\), in the selected distinct relation to \(h_1\), receives weight \(m\). There is at most one selected candidate, so an active row has denominator \(D=m+5\).

At count 5 with \(h_1\) equal to the missing edge, formation cannot activate the selector. All rows there are uniform. At count 6, all events are dissolutions, so all rows are also uniform. Their coarse harmonic equations give
\[
g_6=\frac{g_6+4g_{JA}+g_{JD}}6,
\qquad
g_6=\frac{4g_{JA}+g_{JD}}5.
\]

For any other count-5 history, every dissolution still has unit weight. Their five successor values sum to \(5g_6\), while the possibly biased formation also leads to \(g_6\). Normalizing by either 6 or \(D\) therefore gives the same continuation \(g_6\). Thus \(W_5=W_6=0\).

At count 4 with absent \(h_1=i\), write the missing edges as \(i,j\). Only \(h_2=j\) can activate a formation. If \(\operatorname{relation}(i,j)\) is not the selected relation, the entire fibre is inactive and \(W=0\). Otherwise the fibre has one active coordinate and five inactive coordinates.

### R04/R11 Occupation Flux

Let \(x\) be total count-6 occupation.

For a fixed count-5 missing edge \(j\), every present-edge dissolution has the same probability within each fine state: either \(1/6\) or \(1/D\). Thus its total incoming flux into the count-4 coarse fibre \((\text{missing }i,j;h_1=i)\) is independent of the dissolved edge \(i\ne j\). Covariance makes it independent of \(j\) as well. This proves the common fibre mass \(y\), including equality between the ADJ and DISJ cases.

The active count-4 fine state with \(h_2=j\) has a uniquely specified two-event history: dissolve \(j\) from count 6, then dissolve \(i\). Both relevant rows are uniform. Its mass is therefore \(x/36\).

An active count-5 state has missing edge \(i\), present \(h_1=j\), and \(h_2=i\). Its only predecessor material mask has missing edges \(i,j\). Summing over predecessor histories gives
\[
\beta=\frac{y-x/36}{6}+\frac{m}{D}\frac{x}{36}
=\frac y6+\frac{5\delta x}{216D}.
\]

For a fixed count-5 mask, there are precisely \(v\) active fine states, each of mass \(\beta\). With total occupation \(f\), the two flux equations follow:
\[
y=\frac f6+v\beta\left(\frac1D-\frac16\right),
\]
\[
\frac x6=\frac f6+v\beta\left(\frac mD-\frac16\right).
\]
Their difference and substitution yield
\[
\bigl(36D^2-5v\delta^2\bigr)x
=36D(6D+v\delta)y.
\]

The denominator has the stated positive coefficients for \(v=1,4\), and
\[
6D+v\delta=(6+v)m+30-v>0.
\]
The stationary restriction satisfies the same local balance equations. Therefore
\[
x/y=\pi_6/\pi_S,
\qquad
b_{\mathrm{active}}=x/36
=\frac{y}{\pi_S}\frac{\pi_6}{36},
\]
which proves \(U_{\mathrm{active}}=0\).

Finally, \(\sum_{z\in S}U_z=0\), and \(W\) has two levels:
\[
\sum_{z\in S}U_zW_z
=(W_{\mathrm{active}}-W_{\mathrm{inactive}})
U_{\mathrm{active}}=0.
\]

## Assumptions

- Coarse fibres are the material mask and \(h_1\), with \(h_2\) retained as the fine coordinate.
- \(U\) is stationary conditional centering within those fibres.
- The source distribution is stationary conditional on its graph class.
- Route entrances are joint contributions; normalizing separately by route would change the block-balance coefficients.
- Sources and occupations are \(S_4\)-invariant.
- \(m\) is finite and strictly positive.
- Killed hitting equations have unique solutions. Finite state space and positive paths to the return layer establish transience.
- Masses and the factors \(1/6,1/36\) refer to original full states, not uncorrected orbit masses.

## Counterexamples/Failure Modes

- Arbitrary hidden priors can break entrance-fibre centering and the uniform \(f\) marginal.
- Labelled targets can break the coarse-orbit equalities used for \(W_0\) and \(W_5\).
- Additional weighted candidates or altered direction filters can invalidate the unit-weight dissolution fluxes and denominator \(D\).
- Covariance alone cannot equate ADJ and DISJ count-4 fibre masses; the equal dissolution probabilities are essential.
- Equality of first-entry laws would be insufficient without the common subsequent killed kernel and the impossibility of revisiting \(E\).
- At \(m=0\), or an infinite-weight limit, positivity and the stated transience argument require separate treatment.

No failure mode above occurs under the stated model and scope.

## Unresolved Issues

The document should define \(P,U,V,W,K_\pi\) explicitly or reference their definitions. In particular, \(a_cP=a_c\) is ambiguous without identifying \(P\); it cannot mean that a class-conditioned source is stationary for the physical transition kernel.

“Invariant killed occupation” should explicitly mean \(S_4\)-invariant occupation, not a nonzero stationary measure for the transient killed kernel.

For signed linear combinations of source classes, use the homogeneous flux equation rather than dividing by \(y\). The null then extends by linearity, including combinations with \(x=y=0\).

This audit does not independently verify certificate counts, absence of further nulls, or the numerical five-orbit proportion.

## Self-Check

I reconstructed the selector gates from `h2_roles.py`, checked all predecessor and boundary claims, rederived both flux equations and their elimination, and checked the neutral case symbolically. At \(m=1\), the ratio is \(x/y=6\), consistent with an active coordinate carrying \(y/6\).

I used no computations or scientific cells, edited no files, and consulted no sibling path. Agreement with another path would not itself establish proof.
