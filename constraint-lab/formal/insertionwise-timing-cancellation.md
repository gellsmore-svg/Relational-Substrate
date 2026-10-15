# Insertionwise Timing Cancellation

Date: 2026-10-15. Keep destination vectors, target-summed timing, and route-joint probabilities separate.

## General Conditions

Let r=R 1 be the column of immediate exit probabilities. The entrance insertion vanishes when aP=a. At four events the two surviving insertion scalars are
s1=a Q(I-P)QP r and s2=a Q^2(I-P)r.
For a declared family M these vanish separately iff MQ(I-P)QP r=0 and MQ^2(I-P)r=0. Useful sufficient readout conditions are that QP r is P-invariant on support reached after one killed step, and r is P-invariant on support reached after two. More generally the reachable signed rows may annihilate these columns without either column vanishing globally.

These conditions are not consequences of eventual return normalization. Even r constant at one layer need not make QP r constant at an earlier layer, because survival probability can depend on hidden history. Parity excludes odd return lengths but does not exclude an even-length residual.

## Restricted All-Weight Control

For FORM R03/R09 on k=2 DOWN, a four-event sparse-side return must have directions DISSOLVE,DISSOLVE,FORM,FORM. After the third event there is exactly one edge, equal to h1. The fourth formation cannot select h1; FORM recent selectors therefore give unit formation weights and total return probability 5/6, independent of h2. At the empty state after the second event the next formation is certain and every successor has that same 5/6 readout. Thus both surviving timing insertions vanish on this route for every m>0. Complement gives DISSOLVE on k=4 UP.

This is a route-specific sufficient condition, not a proof of the twenty complete UP+DOWN timing nulls. Other routes and layers have nonconstant survival/exit readouts. The complete twenty total nulls remain verified at the two published grades only.

## Existing Twenty and Active Controls

The immutable 8O table has twenty structured nonzero four-event vectors with zero target sums in each insertion: FORM/DISSOLVE R03 at k=2 matching, k=3 P4, k=4 cycle, and R09 at k=2 path, k=4 pendant, at both grades. Nearby other source classes for the same role/family/layer are timing-active. Therefore role alone, parity alone, stationary adjacent-law matching alone, and ordinary normalization alone cannot explain the source-selective total zeros.

The read-only 8P proof-check summary preserves all twenty destination vectors and insertion scalars plus active controls. No all-m identity for the complete twenty, no all-horizon extension, and no new actual cell is claimed. A general source/readout annihilation criterion is exact but is not itself a structural explanation of each finite example.
