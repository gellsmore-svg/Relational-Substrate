# H0 analytic expectations before execution

These formulas are externally predeclared analytic expectations. Their symbolic
derivations are allowed before freeze; no non-neutral H0 numerical/exact W4
row, kernel, shape, information, stationarity or eigenvalue verification has run.

For p=6 pair slots and r=4 hidden triad slots, non-sentinel history gives full
normaliser m+p+r-1=m+9. The pair-event probability is (m+5)/(m+9).
Hidden-only events preserve pair mask and history, hence summing the geometric
waiting law gives next-pair slot probability w_e/(m+5). The sentinel is uniform.

The two specified histories have probability 1/[10(m+9)] each. Their endpoints
have the same ten material bits and differ only in history. Non-neutral rows
exchange the m-weighted slot; the pair-row JS is
[m ln(2m/(m+1))+ln(2/(m+1))]/(m+5), with denominator m+9 for full rows.

At the specified path, both remembered slots are present. Both next-pair
edge-count laws have weights (m+2,3)/(m+5) on counts (2,4). Dissolving the
middle versus end slot yields different graph classes. Classification is
mechanical; equality of edge-count laws does not imply class-law equality.

For fixed output (p',j) of the recurrent pair-epoch chain, incoming states are
(p' xor 2^j,i), i=0..5. Their transition weights sum to
[m+5]/[m+5]=1. Thus uniform joint occupancy is a stationary candidate, to be
verified exactly. All positive transitions permit connectivity, and two repeats
give a two-step return; pair parity implies period two, not convergence from
a fixed-parity start to the full stationary vector.

The six-slot history chain is Q=Pi+lambda(I-Pi), where Pi has all entries 1/6
and lambda=(m-1)/(m+5). Hence Q^k=Pi+lambda^k(I-Pi). Current history can still
affect the next event while initial-history dependence decays.

Averaging q_h over uniform h gives 1/6 for each next pair slot. Under that
stationary averaging, occupancy and one-step pair statistics may agree with
H=0 even when repeat probability m/(m+5) and consecutive-slot information
ln(6)+a ln(a)+5b ln(b) differ, a=m/(m+5), b=1/(m+5).

After the first observed pair transition, h is exactly the one-hot difference
of successive pair masks. That suffices for order at most two; differing
history-conditioned rows would prove first-order insufficiency. These order
and one-step equality statements refer to the pair-event clock, not the
full-event clock with arbitrarily many intervening triad events.

No theorem catalogue entry or new scientific coherence finding is appended
until the frozen H0 verification is complete.
