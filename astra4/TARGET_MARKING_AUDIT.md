# A missing hypothesis in the target-cover implementation

September 5, 2026; base record `efff2dc5c31a71030ccf931d22b9cd2047c0e172`.

## 1. What the code assumes

In `docs/plans/audit/vitushkin/gapcheck.g`, CheckCurve assigns

```
n := D - NrMovedPoints(meridian);
e := D - n;
s := D - NrMovedPoints(local_group);
```

and computes the escaping-curve Euler characteristic using only cycles and
local orbits of size greater than one. `dicrit.g` likewise tracks nontrivial
cycles. The fundamental-group quotient kills every fixed meridian lift.
Thus the implementation identifies **all fixed sheets with staying sheets**.

The actual local implication of the Keller condition is that a staying
sheet is fixed. The converse additionally requires that no unramified sheet
is missing from the affine source. In the escape bridge's own notation,
the transverse ramification length is `r_E=1-k_E`. An escaping component
with k_E=0 would have r_E=1 and would be invisible to moved-point counts.

I did not find a proof excluding this case in the audited record or its
cited framework source. Borisov's
[Frameworks for two-dimensional Keller maps](https://arxiv.org/html/1901.04073v2)
states that at least one dicritical component is ramified, which does not
assert that every dicritical component is ramified. This is a missing
justification for the universal scope of the screen, not a claim that a
Keller map with an escaping fixed sheet has been constructed.

## 2. Two exact controls clarify the logical gap

Consider the smooth affine surface

\[
X=\{uw=v(v-1)\}\subset\mathbb A^3
\]

and its open embedding

\[
\mathbb A^2\longrightarrow X,\qquad
(x,y)\longmapsto(x,xy,y(xy-1)).
\]

Its image is exactly X minus the line L given by u=0,v=1. The inverse
is `x=u, y=v/u` on u!=0 and `x=u, y=w/(v-1)` on v!=1. These opens
cover X minus L. Smoothness follows because the only simultaneous zero
of the three partial derivatives of uw-v(v-1) does not lie on X.

The form `omega=du wedge dv/u` extends to a nowhere-zero regular
two-form on X and restricts to dx wedge dy. At u=0, differentiation of
the equation gives `omega=du wedge dw/(2v-1)`, which is regular and
nonvanishing there. Therefore the source being A2, even with an extending
nonvanishing volume form, does not alone forbid such a missing curve.

Projecting X to `(u,w)` gives the polynomial plane map

\[
(x,y)\longmapsto(x,xy^2-y),\qquad J=2xy-1.
\]

The finite completion has equation `v^2-v-uw=0`. Over a generic point
of u=0 its two sheets v=0,1 are unramified, so a small transverse meridian
is the identity. One sheet stays and one escapes. Equivalently, for fixed
w the quadratic `xy^2-y=w` has one root tending to -w and another
escaping as x tends to zero.

This explicitly disproves fixed=staying for general polynomial plane maps.
Its Jacobian is nonconstant, so it is **not** a Keller counterexample and
does not disprove an additional, properly proved Keller-specific theorem.

## 3. The data needed for a complete marked screen

Let f_i be the number of fixed points of the meridian of target component i,
u_i the number of those sheets assigned to escaping components, and c_i^m
the number of nontrivial meridian cycles. Then the correct generic counts are

\[
n_i=f_i-u_i,\qquad e_i=D-f_i+u_i,\qquad c_i=c_i^m+u_i.
\]

At a singular point p, the actual staying count s_p is at most the number
of common fixed points of the local subgroup. Marks must be invariant
under longitude transport and compatible with specialization to local
orbits. They are not freely chosen independent integers.

Within the same finite-normal-cover stratification, the source equation is

\[
\chi(X_{aff})=D(1-m+\nu)+\sum_i n_i(1-k_i)+\sum_p s_p,
\]

where k_i counts normalization branches over singular target points and
nu is the sum of branch-count-minus-one over singular points. Write
delta for the total loss of the previously assumed local staying points.
Changing the marks changes the old computed Euler values by

\[
\chi(X_{aff})_{new}=\chi(X_{aff})_{old}
 +\sum_i u_i(k_i-1)-\delta,
\]

\[
\chi(R)_{new}=\chi(R)_{old}
 -\sum_i u_i(k_i-1)+\delta.
\]

In particular their sum is unchanged. The campaign's necessary conditions
chi(Xaff)=1 and chi(R)>=1 require the old sum to be at least 2, even
before the local and longitude checks.

The source fundamental-group quotient must also kill only staying lifts.
The fibre Euler, dicritical and singular-line tests need the actual marked
counts. Re-running the old unmarked census to greater degree would not
resolve this missing hypothesis.

## 4. What happens to the archived candidates

`rescreen_marked_logs.py` extracts complete single-line printed Euler-stage
rows of degree at least six from the retained Vitushkin logs. It reads 39
distinct numerical signatures. It is **not** a replay of the group
enumerations: rows removed before Euler computation, wrapped or otherwise
incomplete rows, and unprinted representations are outside its coverage.
The JSON records the input hashes and the actual matching row(s).

Allowing all integer marks consistent with at least one staying sheet per
target component and the total local-fixed budget gives one coarse survivor:

| Datum | Value |
|---|---|
| Log / curve | sweep16.log / cc_line_tan1 |
| Curve components | cusp `(t^2,t^3)` and tangent line `(1+2t,1+3t)` |
| Cover degree and group | 6, S4 in its degree-six action |
| Meridian types | one 4-cycle; two 2-cycles |
| Old generic fixed counts | (2,2) |
| k | (3,2) |
| Old local fixed counts | (0,2,0) |
| Old Euler values | chi(Xaff)=2, chi(R)=0 |
| Proposed escaping fixed counts | (0,1) |
| Required local staying loss | 2 |
| Proposed new Euler values | 1,1 |

It fails local incidence. The two common fixed points lie over the
transverse cusp/line intersection `(1/4,-1/8)`. Each is a singleton local
sheet, with separate smooth inverse images of the two crossing divisors.
No fixed sheet is deleted along the cusp, and just one is deleted along
the line. Thus at most one of these two points can be on a deleted divisor;
the Euler equations require both to be deleted. An isolated omitted point
cannot supply the difference: the affine open source cannot omit an
isolated codimension-two component in a normal affine surface (the local
Hartogs extension argument rules this out). Hence this coarse survivor dies.

For H3 specifically, the marked source equation simplifies to
`chi(Xaff)=3u+s`, with s=0 or1. Requiring 1 forces u=0,s=1, exactly
the original marking, and chi(R) remains zero. So the established H3
topological exclusion survives this audit. Increasing its boundary-tree
depth is not a path to a counterexample within that same class.

## 5. What remains genuinely unresolved

A universal target census needs either a proved Keller-specific theorem
that eliminates escaping fixed sheets or explicit boundary marks with full
peripheral and local compatibility. The present arithmetic audit does not
settle that general question. It finds no revived example among the stated
39 retained signatures, and it does not validate earlier filters that
discarded rows before those signatures were printed.
