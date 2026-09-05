# Astra 5 — direct conductor construction strike

September 5, 2026. Continues Astra 4 local commit `8921a59` on
`astra/jc2-missed-routes-2026-09-05`.

The proposed conductor correction method has now been analyzed to all orders.
I found an exact obstruction to its original trace choice, constructed an
explicit all-order family that provably never polynomializes, and excluded
additional unbounded families. The full collision subalgebra remains open;
no polynomial counterexample was obtained.

Detailed proofs are in
[CONDUCTOR_TERMINATION.md](astra5/CONDUCTOR_TERMINATION.md), with executable
checks in [verify_conductor_strike.py](astra5/verify_conductor_strike.py) and
results in [verification.json](astra5/verification.json).

## What was actually resolved

| Question | Result |
|---|---|
| Can both coordinates be corrected formally to all orders? | Exactly when their trace derivatives generate the unit ideal in C[r,r^-1]; all free kernels are retained |
| Can the old first-jet traces extend to a polynomial Keller pair? | No: their Liouville residue is -8/3 instead of 4/3 |
| Does fixing the residue and attaining arbitrarily high order establish progress toward termination? | No: an explicit polynomial sequence does both, but its formal limit satisfies c(Q+v)^2=1 and cannot be polynomial or rational |
| Does making both displayed coordinates nonconstant in both variables remove that control? | No: a target shear makes both vary while preserving the same obstruction |
| Can one component remain in C[c,cv], with arbitrary degree? | No counterexample: a residue obstruction or injectivity on a line forces failure/invertibility |
| What mixed weights can be discarded? | A component of greatest weight <=1 or least weight >=-1 forces invertibility; pairs with both greatest weights <=2, or both least weights >=-2, do too |
| Do conductor periods capture all infinity conditions? | No: two separate puncture residues on generic Delta fibres give stronger identities |
| Is there a global polynomial construction gate? | Yes: recover P from a gcd of derivatives of one polynomial potential, test closedness, integrate Q, then verify the original bracket and collision |

The family exclusions use an explicit published input,
[Gwozdziewicz's injectivity-on-one-line theorem](https://arxiv.org/abs/alg-geom/9305008),
together with the written residue and mixed-weight arguments. Their scopes
do not extend to all polynomial pairs in the subalgebra.

## The obstruction that changes the proposed plan

Let

\[
r=3cv-2,\quad \Delta=r^2-9c,\quad
s=(rv-3)/6,\quad z=\Delta(cv^2-1)/4.
\]

For every N>=1 the polynomials

\[
P_N=c,\qquad Q_N=-v+3s\sum_{j=0}^N\binom{-1/2}{j}z^j
\]

belong to the collision subalgebra, have the correct conductor residue, and
satisfy

\[
\{P_N,Q_N\}-1
=-(r+1)(2N+1)\binom{-1/2}{N}z^N\ne0.
\]

Their formal limit has Jacobian exactly 1 but obeys `c(Q_hat+v)^2=1`.
That equation cannot hold in the polynomial ring. The approximations exist
in every degree `7N+3`; raising conductor order does not repair the failure.

The general recursion is equally permissive: every immersed even Laurent
trace extends formally. Adding the correct conductor residue makes the
Liouville form formally exact as well. Therefore neither of those local
successes can serve as a counterexample selection criterion.

On a generic Delta=a^2 fibre, a polynomial Keller pair must have the two
individual residues `(a+2)/3` and `(-a+2)/3`. The displayed controls fail
these even when the sum of the two residues is correct. This is an exact
failure at infinity, not a numerical convergence issue.

## The resulting global construction equation

For the minimal corrected traces, `P|Delta=r^2/9` and
`Q|Delta=-6/r^2`, polynomiality and the Jacobian force

\[
PQ=\Delta(-s/6+\Delta W(v,c))-2/3.
\]

This is a necessary factorization with both coordinates free. It must still
pass the exact Jacobian equation; no suitable W and factors were found.

A complete global gate for the whole subalgebra uses a polynomial potential.
Every solution has

\[
H=K-2r/3,\quad K\in B,\qquad dH=P\,dQ-v\,dc.
\]

For any supplied H, compute

\[
g=\gcd(H_v,H_c+v).
\]

If the quotient one-form
`(H_v/g)dv+((H_c+v)/g)dc` is closed, integrate it to a polynomial Q.
Then `{g,Q}=1` follows exactly. Membership of both g and Q in B supplies
the collision. Conversely, every polynomial Keller pair in B arises this
way, up to a nonzero scaling of g.

The implemented gate includes positive controls from actual polynomial
automorphisms and negative controls with both constant and nonconstant gcds.
It is a test for a supplied potential, not an exhaustive potential search or
a promise that an admissible potential exists.

## Verification and remaining scope

`python astra5/verify_conductor_strike.py` produces seven PASS groups.
The explicit original brackets, collision evaluations, recurrence kernels,
residues, and potential reconstruction are checked exactly. The all-order
and all-degree arguments are written proofs, without external review or
proof-assistant formalization.

I did not rerun the old finite-field searches, extend low-degree projection
boxes, or count formal success as an actual candidate. The completed results
close the stated trace and support families and show why the suggested local
iteration is insufficient. Finding a polynomial potential or factorization
that passes all the global gates remains unresolved. The full subalgebra
has not been proved impossible.
