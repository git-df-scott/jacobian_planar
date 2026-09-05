# JC2 closing-record corrections — 2026-09-04

September 5 continuation: [Astra 7](ASTRA_7_LIVE_SYSTEMS_CLOSED.md) resolves
both live degree-14 systems retained by Astra 6. This is a complete
arbitrary-c-degree obstruction for (4,10) and (6,8), not a full obstruction
for the collision subalgebra. The next unexcluded potential v-degree is
15, with coordinate degrees (6,9). Both leading branches and the non-even
root-trace cases in (6,8) are included in the new valuation proof.

This file governs interpretation of the recovered and historical records.
Original reports are preserved, including their retracted claims. The full
source ledger is [CATCHES.md at the frozen Claude head](https://github.com/git-df-scott/jacobian_planar/blob/b233c708e9b43c597f6f2fa2e82a9b04fb5dd55a/CATCHES.md).

## September 5 addendum — Astra 4

Subsequent [Astra 5](ASTRA_5_CONDUCTOR_STRIKE.md) correction: an immersed
conductor trace always extends formally, and an explicit polynomial sequence
passes every finite order while its limit is provably nonpolynomial. Formal
success cannot be promoted to evidence of termination. The original first-jet
trace choice is itself globally excluded by its residue. New all-degree
mixed-weight exclusions apply with the exact scope in the Astra 5 report.

The [new audit](ASTRA_4_MISSED_ROUTES.md) adds these scoped corrections:

| Historical claim or priority | Correct interpretation |
|---|---|
| A rational mate with poles on proper fibre components may fail to yield D_P(A)=b(P) | False. Whole-fibre products clear all finite denominators by the valid pole theorem, even for reducible fibres. The explicit night19 control has A=-xy and D_P(A)=P. |
| Missing initial values or greater x-degree could rescue the monic height-(4,6) lane | Superseded by Astra 4's complete algebraic-integral reduction and all-degree proof. Nonconstant leading y coefficients are outside that theorem. |
| Monodromy-fixed sheets can universally be counted as staying by the current code | Requires a missing Keller-specific justification or explicit boundary marks. The code alone does not establish the converse to staying implies fixed. No Keller counterexample to that converse is claimed. |
| H3 source depth should remain the first counterexample attack | Its fixed topological class already fails the escaping-curve budget and cannot be rescued by the new marks. Deeper trees do not repair that class. |
| Cubic target projections of the x=1 subalgebra are the first open frontier | Their plane degrees are at most 12, already excluded by known degree bounds. The arbitrary-degree subalgebra instead has Astra 4's exact conductor/parity description. |

The marking re-screen covers only 39 distinct complete printed signatures,
not every historical representation. The new all-degree and geometric proofs
are written arguments with checked algebra, without external review or
proof-assistant formalization. The September 4 corrections below remain in
force except where this addendum explicitly supersedes a search priority.

## 1. New correction: the recovered night26 degree-six model is impossible

The recovered [night26/CLOSING_STRIKE.md](night26/CLOSING_STRIKE.md) proposes

\[
t=r^2+2u^2r,\qquad R=r^3
\]

and asks for a faithful rational plane chart with `t,R` polynomial and
`dt wedge dR = dx wedge dy`. It labels that construction **GO**. That label
is superseded: **no such chart can exist**.

Here is a direct characteristic-zero proof. Suppose a chart existed. Put
`A=C[x,y]`; faithfulness says `Frac(A)=C(u,r)`, so `r` belongs to `Frac(A)`.
Polynomiality of the intended second coordinate says `r^3=Q` belongs to A.
Therefore r is integral over A, being a root of the monic polynomial
`Z^3-Q`. The polynomial ring A is integrally closed, so r belongs to A.
It is nonconstant. Consequently

\[
J(P,Q)=J(P,r^3)=3r^2J(P,r),
\]

which cannot be a nonzero constant in `C[x,y]`: the nonconstant polynomial
`r^2` divides it. Contradiction.

More generally, a coordinate of a characteristic-zero Keller pair cannot be
a nontrivial pure power of an element of the full rational function field.
The same argument works for `Q=c*r^m+d`, with `m>1`, `c!=0`, and constant d.
In this model it is enough that `t` and `r^3` polynomialize faithfully; no
analysis of toric charts, ramification at infinity, or the degree-six
monodromy is needed to obtain the obstruction.

This correction does **not** refute the archived curve identities, field-degree
calculation, or tests of particular chart families. Those identities did not
test whether a purported Keller coordinate had a rational root in the full
function field. Nor does it exclude every degree-six primitive construction:
the obstruction is the particular choice `R=r^3`.

The two original commits, all twelve files, and their patch and bundle are
preserved in [record/RECOVERY.json](record/RECOVERY.json). Their exact algebra
was not rerun for this archival task. The new impossibility argument above is
a written proof, not a claim produced by the archived test suite.

## 2. Governing historical corrections

| Historical claim or failure | Correct interpretation |
|---|---|
| Framework endgame has no rational R because one can evaluate at v=-1 | False when R has a pole there. The rational escape hatch is explicit; use repaired pole-order/realization arguments with their chart hypotheses. |
| The nine enumerated framework charts exhaust all possibilities | Retracted in the later adjudication. A finite chart list alone is not a family-wide proof. |
| Two framework closures are independent | Some purported legs were algebraically equivalent; independence must be checked at the premise level. |
| Weighted-homogeneous plane Keller maps are always linear | The earlier mixed-sign hypothesis was dropped. Same-sign triangular maps give immediate counterexamples to that broad statement. |
| B=16 EMPTY rows from the printed GGV system | Void for the intended problem after the row-3 transcription/source correction. Use only explicitly re-established corrected equations and certificates. Later summaries disagree on the restored range; this record does not resolve that by taking the largest claimed range. |
| Rank criterion decides the whole B=16 ladder | The cited criterion was found unable to fail in its implementation; it cannot justify uncomputed cells. |
| A small numerical residual or failure of many starts proves emptiness | Planted roots were missed. These are finder diagnostics, not exclusion certificates. |
| msolve exit code 0 and output `[-1]` prove EMPTY | A parser failure could produce exactly that output. Read stderr and require valid inputs and a certificate appropriate to the stated field. |
| Several modular EMPTY primes prove characteristic-zero EMPTY | No. A separate exact argument or a justified specialization argument is required. |
| A solver's returned basis or reduce-to-zero check is itself a unit certificate | Ideal containment and a complete contradiction identity are different checks. Verify the actual identity representing 1. |
| Early pentagon truncations or `pent_L23.ms` exhaust the desired polygon | Degenerate positive-dimensional families inhabit the unsaturated core; some truncations omit the very conditions needed to detect a full extension. |
| The pentagon cascade may discard homogeneous kernels | It may not. Greedy particular lifts caused false contradictions; all free kernel coordinates must be retained. |
| Bottom seeds fix six independent pentagon vertices | They leave a residual torus parameter. Astra 3 proves and uses one specific normalization of it. |
| The j=2i face universally forces a square/cube, quartic-discriminant or double-root restriction | Earlier broad versions were withdrawn because commuting on that face can be vacuous. Astra 3 derives its relation from the separate highest-x edge with nonzero endpoints. |
| Level 16 forces the earlier `sigma^6` divisibility ladder | Superseded by the joint condition and the exact surviving witness on the level-16 branch. |
| Four prime counts prove one Galois orbit | The statistical inference was retracted. Exact factorization and Astra 2's independent completeness argument provide the later evidence. |
| Degree-35/quintic data automatically identify the old degree-1144 object | The provenance map remains unresolved; Astra 2 and 3 do not depend on identifying that object. |
| All `(9,27)` archive labels name the paper's full polygon | Several name different compiler strata. The actual support translation must be checked before transferring a kill. |
| Above-125 monomial certificates close all corresponding published cases | They close the generated strata. The unprinted lower corner and corrected c' range remain load-bearing provenance gaps. |
| A nonempty reduced `{P,Q}=x^2` system is a JC2 counterexample | A reverse lift to a polynomial plane Keller pair and independent noninvertibility evidence are still needed. |
| An ambient three-dimensional construction automatically descends to a planar Keller map | The induced plane Jacobian, polynomiality, and collision transport require separate proofs. |
| A genus-one exact primitive polynomialized on a quotient realizes the original curve | The quotient can lose the finite field extension and become triangular. Faithfulness is essential. |
| Primitive degree three was the next live degree in night25 | Night26's own subsequent degree audit supersedes that search recommendation. Its replacement `R=r^3` model is now excluded by section 1. |
| Source/target survivors are algebraic realizations | They are necessary-condition blueprints until a polynomial map is constructed. Bounded tree searches do not cover arbitrary boundary depth. |
| Missing in one checkout means missing from the campaign | Several “ABSENT” statements meant “not fetched.” This record inventories all frozen refs and restores two truly unpublished commits. |
| Sessions 43–44 are absent | They are present on later branches/PRs #19 and #20, although absent from the old main layout. Session labels are reused across workstreams. |
| A message saved locally was delivered | Repository notes explicitly distinguish unsent mailbox drafts from delivered messages. This closeout sends no mailbox messages. |

## 3. Supersession by the three Astra runs

Astra 1 conservatively left Proposition 4.3(2) characteristic zero UNKNOWN
after reconciling the historical modular records. Astra 2 supplied a separate
five-orbit completeness argument and exact 26-multiplier contradiction.
Astra 3 supplied the pentagon's complete graded prefix, affine and boundary
certificates, good-reduction checks, and valuation argument. Thus both
Proposition 4.3 polygons are now excluded in this campaign's computer-assisted
record. Their written proofs have not received external peer review or
proof-assistant formalization.

The statements “pentagon open” in earlier reports remain historical. The
separate above-125 `(3,4)` chain and other JC2 configurations are not settled
by these exclusions. No explicit JC2 counterexample has been produced.
# Astra 6 global-potential update — 2026-09-05

`ASTRA_6_GLOBAL_POTENTIAL_STRIKE.md` supersedes the previous global search
formulation with an exact gcd eigenfunction criterion. It proves a
v-degree-at-most-13 obstruction with unbounded c-degree, but leaves the
full collision subalgebra open. The degree-14 coverage list contains both
(4,10) and (6,8), not only the latter. The (6,8) leading-root alternatives
include both rho=2/3 and rho=4/3; dividing by 2-3rho would lose a branch.
Even trace of the quadratic approximate root is sufficient for a further
obstruction, but is not established for arbitrary candidates. No new
finite-order conductor lift is used as evidence for polynomial termination.
