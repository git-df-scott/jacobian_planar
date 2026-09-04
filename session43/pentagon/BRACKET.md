# What the pentagon system actually is: {P, Q} = x^2

**Verified numerically, 12 orders, random point, zero violations.**

## Derivation

The exporter's recursion (`wave1/w1_h1b_sparsity.py`) is

    Q[0] = 1 ;  Q[1] = x^2
    (k+1) Q[k+1] = sum_{a=1..k} [ a P[a] Q[b]' - (k+1-a) P[a]' Q[b] ],  b = k+1-a

Multiply by y^{k+1} and sum over k >= 1.  With `y d/dy P = sum a P_a y^a` and
`P_0(x) = x` (the gauges p_0_0 = 0, p_0_1 = 1), the sums close to

    y Q_y - x^2 y = (y P_y) Q_x - (P_x - 1)(y Q_y)

which rearranges to

    **P_x Q_y - P_y Q_x  =  x^2**

i.e. the Poisson bracket / Jacobian determinant of (P, Q) equals x^2.  The
conditions Q[j][i] = 0 for j = 13..23, i <= j-13 are then Newton-polygon
vanishing conditions on the unique Q determined by P.

Checked directly: rebuilding P and Q from the recursion at a random point and
forming `P_x Q_y - P_y Q_x - x^2` gives **0 at every order y^0..y^11**.

## Why this matters computationally

`{P,Q} = x^2` is **bilinear** in the coefficients of P and Q -- total degree 2.
The exported `pent_L23.ms` has degree 22 and 1,080,147 monomials **only because
Q was eliminated**: the recursion solves for Q in terms of P and substitutes.
Keeping Q as unknowns gives a sparse bilinear system instead, and the
Newton-polygon conditions `Q[j][i] = 0` are then simply *linear* (they set
individual q-coefficients to zero).

This is Example 14's lesson in its exact form: the low-variable form is degree
22 with a million terms; the high-variable form is degree 2 and sparse.

## Why it matters mathematically

    dP ^ dQ = {P,Q} dx ^ dy = x^2 dx ^ dy = d(x^3/3) ^ dy

So with `s = x^3/3`,

    **det J_{(s,y)}(P, Q) = 1.**

The pentagon system is looking for a **Keller map in the coordinates (s, y)**,
where `s = x^3/3` is a 3:1 cyclic cover of the x-line.  P and Q are polynomial
in (x,y), hence algebraic-but-not-polynomial in (s,y): the object under search
is a Keller map on a cyclic cover / orbifold quotient, not on the plane itself.

This is the same 2,3-weighting that appears in the campaign's bottom edge
(`2 f g' - 3 f' g = w^2`, `wave6/bottomedge/analyse.py`), and it is the same
quotient-and-descent geometry as `session43/pathA_results.md`, where the
descent exponent of a C*-quotient was shown to satisfy k = m+l'-1 >= 1.  The
two halves of the campaign are looking at one structure from two sides.

## Status

Reformulation and identity: **verified**.  No witness, no emptiness proof.
Verdict language unchanged: EMPTY / NONEMPTY / NO VERDICT.
