# The edge-gap finding (Session 44, active analysis)

Derived from the deep symbolic descent's own output, not from a new run.

## What the descent forced

Obstructions found so far on the open (72,108) subcase 2, exactly and in
characteristic zero:

    level 4:  a_2_1^2 = 0                  -> a_2_1 = 0
    level 6:  a_1_1^2 * a_4_2 = 0          -> branch a_1_1 = 0
    level 8:  4 * a_4_2^2 = 0              -> a_4_2 = 0
    level 12: a_3_2^4 - 9 a_3_2^2 a_6_3 + 27 a_6_3^2 = 0

In the naming a_j_i = coefficient of x^i y^j, the forced coefficients are

    a_2_1 = x^1 y^2   -> lattice point (1,2)
    a_4_2 = x^2 y^4   -> lattice point (2,4)
    a_6_3 = x^3 y^6   -> lattice point (3,6)   (appears at level 12)

Every one lies on the line j = 2i, which is exactly the edge of
N(P) = {(0,0),(1,0),(8,14),(8,16)} running from the vertex (0,0) to the
vertex (8,16). The descent is walking ALONG that edge, from the bottom up.

## Intrinsic reformulation

On that face the (m,n) = (3,2) structure gives face forms that are powers
of a common form R: P's face form is R^2 (length 8 = 2*4), Q's is R^3
(length 12 = 3*4), with R of length 4. Writing R(t) = c0 + c1 t + c2 t^2 +
c3 t^3 + c4 t^4 and p(t) = R(t)^2, the face coefficients are

    a_0 = c0^2,  a_1 = 2 c0 c1,  a_2 = 2 c0 c2 + c1^2,  ...,  a_8 = c4^2.

The corner (0,0) is a vertex, so a_0 != 0, so c0 != 0. Then the descent's
a_1 = a_2 = 0 solve to

    c1 = 0  and  c2 = 0.

So the descent's obstructions are EQUIVALENT to a GAP in the face root:

    R(t) = c0 + c3 t^3 + c4 t^4 ,   c0 != 0,  c4 != 0.

That is a clean, intrinsic statement replacing three coordinate-dependent
obstructions.

## The sharp consequence

GGHV's Prop 4.3 proof repeatedly uses face forms that are POWERS OF A
LINEAR FORM (e.g. "l_{1,-2}(P) = lambda (z - lambda_1)^{8m}"). Test whether
that shape is compatible with the gap:

    R = lambda (t - alpha)^4  =>  c1 = -4 alpha^3 lambda,
                                  c2 =  6 alpha^2 lambda.
    c1 = c2 = 0  with lambda != 0  =>  alpha = 0  =>  c0 = lambda alpha^4 = 0.

But c0 != 0 (vertex). CONTRADICTION.

    ==> If the face root on the (0,0)-(8,16) edge must be a power of a
        linear form, then open subcase 2 is EMPTY.

    ==> Conversely, if subcase 2 is NOT empty, then its face root has at
        least two distinct roots. Indeed R = c0 + c3 t^3 + c4 t^4 has
        discriminant c0^2 (256 c0 c4^3 - 27 c3^4), which is nonzero unless
        256 c0 c4^3 = 27 c3^4 -- so generically R is separable.

Either way this is a sharp, checkable prediction about any counterexample
of this shape, and it is the first structural statement the campaign has
extracted about what a (72,108) counterexample would have to LOOK like.

## Status and what is needed

NOT a proof of emptiness. The implication is conditional on the face root
being a linear power on THIS face, which GGHV assert for the faces they
analyse in Prop 4.3 but which is not established here for this one. The
honest next step is to determine, from the corner-chain data of the (8,28)
case, whether the (0,0)-(8,16) face form is required to be a linear power.
If yes, subcase 2 dies immediately by the argument above -- with no
Groebner basis, no solver, and no waiting on the descent.

## Update: GGHV's Proposition 3.12 located, and case (1) eliminated

Source: Guccione-Guccione-Valqui, "The Two-Dimensional Jacobian Conjecture
and the Lower Side of the Newton Polygon", arXiv:1605.09430, Prop 3.12.
This is the tool GGHV-2022 use to eliminate cases by forcing multiplicities
of linear factors in face forms.

Statement (paraphrased): for (rho,sigma) in V cap ](0,-1),(1,-1)[ and R a
(rho,sigma)-homogeneous non-monomial with [G,R] = R^i, writing
R = x^(u/rho) r(z) with z = x^(-sigma/rho) y, ONE of these holds:
  (1) rho | l and r = xi * h^j for a linear h != z;
  (2) there are theta, t' in N with theta <= N1, 0 < t' < l*theta and
      (rho,sigma) = -dir(t' st(R) + theta(1,1)); then r has a linear
      factor of multiplicity theta;
  (3) similar with theta | N2, and then nu2 > 0.
Notation 3.10: (upsilon1, nu1) := en(R) - st(R), (upsilon2, nu2) := st(R),
N1 = gcd(upsilon1, nu1), N2 = gcd(upsilon2, nu2).

### What is now established

CASE (1) IS INCOMPATIBLE WITH THE EDGE GAP.
Case (1) says the face root r is xi*h^j for a LINEAR h that is explicitly
NOT z. Our gap analysis showed that a gapped root which is a pure power of
a linear form forces that linear form to be h = z (alpha = 0), because any
other alpha forces c0 = 0 and c0 != 0 is required by the vertex (0,0).
Since case (1) forbids h = z, case (1) cannot occur on this face.

So the open subcase-2 face must fall under case (2) or case (3).

Combined with the multiplicity result proved above -- a gapped R has AT
MOST a double root -- case (2) can only occur with theta <= 2. If the
data of this face force theta >= 3, subcase 2 is EMPTY.

### Where this becomes uncertain, stated honestly

Deciding between (2) and (3) needs the correct (rho,sigma), st(R) and
en(R) for THIS face in THEIR conventions, and that is a notation-matching
task I have not yet verified rather than asserted. Two specific risks:

  * If st(R) = (0,0) for our face then nu2 = 0, which would rule out case
    (3) (it concludes nu2 > 0), and case (2)'s direction equation would
    reduce to (rho,sigma) = -dir(theta(1,1)) = (-1,-1). That direction is
    NOT in the required range ](0,-1),(1,-1)[, which would rule out case
    (2) as well -- and with case (1) already gone, that would be a
    contradiction, i.e. subcase 2 EMPTY.
  * BUT the face direction also has to lie in ](0,-1),(1,-1)[ for the
    proposition to apply at all. The edge (0,0)-(8,16) has edge vector
    (1,2), so its outer normal is (2,-1)-ish, which appears to fall
    OUTSIDE that interval. If so, Prop 3.12 simply does not apply to this
    face and the whole route is void.

Both possibilities are live and they point in opposite directions, so no
conclusion is drawn here. The next step is narrow and well defined: fix
GGHV's (rho,sigma) convention, compute st and en of R for this face in it,
and check membership in ](0,-1),(1,-1)[. That single check either kills
subcase 2 outright or closes this route cleanly.


## VERIFICATION PASS (run explicitly, results below)

Every step of the chain was re-derived from the polygons rather than
assumed. Results:

  CLAIM 1  (0,0)-(8,16) is the w-max face of N(P) for w(i,j) = j - 2i,
           and (0,0)-(12,24) is the w-max face of N(Q).
           w on N(P) = {(0,0):0, (1,0):-2, (8,14):-2, (8,16):0};
           w on N(Q) = {(0,0):0, (2,1):-3, (12,21):-3, (12,24):0}.   VERIFIED

  CLAIM 2  the two face forms MUST commute. For monomials,
           [x^a y^b, x^c y^d] = (ad-bc) x^(a+c-1) y^(b+d-1), so
           w(result) = w(first) + w(second) + 1, giving max w = 1 for
           [P,Q]; the target x^2 has w = -4 < 1, so the w=1 component
           vanishes identically, i.e. [face(P), face(Q)] = 0.        VERIFIED
           (This was the step previously ASSUMED; it is now derived.)

  CLAIM 3  lattice lengths 8 and 12, gcd 4, so face(P) = R^2,
           face(Q) = R^3 with deg R = 4.                            VERIFIED

  CLAIM 4  a1 = 2 c0 c1 and a2 = 2 c0 c2 + c1^2; with c0 != 0 the
           descent's a1 = a2 = 0 solve uniquely to c1 = c2 = 0.      VERIFIED

  CLAIM 5  every root pattern with multiplicity >= 3 (patterns 4, 3+1,
           2+2) forces c0 = 0, contradicting the vertex (0,0).       VERIFIED

## CORRECTION: the Proposition 3.12 route is VOID

Checked rather than assumed, and it fails. Prop 3.12 requires
(rho,sigma) in ](0,-1),(1,-1)[, an arc from 270 to 315 degrees. Our face
is the maximiser of j - 2i, i.e. (rho,sigma) = (-2,1), at 153.43 degrees
-- outside the admissible arc. So Proposition 3.12 does NOT apply to this
face in these coordinates, and NO emptiness conclusion follows from it.
This is the risk that was flagged when the route was recorded; it has now
materialised, and the route is closed rather than left dangling.

## WHAT STANDS AFTER VERIFICATION

Independent of Prop 3.12, and now fully derived:

  Any counterexample of the open (72,108) subcase-2 shape has, on the
  N(P) face from (0,0) to (8,16), a face form R^2 with
      R(t) = c0 + c3 t^3 + c4 t^4,   c0 != 0,  c4 != 0,
  so R has AT MOST A DOUBLE ROOT, and its discriminant is
      c0^2 (256 c0 c4^3 - 27 c3^4).

That is a genuine, verified structural constraint on any counterexample of
this shape -- the campaign's first such statement -- and it is what should
be carried forward, not the Prop 3.12 speculation.

================================================================================

# INDEPENDENT TEST OF THE a_10_5 PREDICTION -- and a RETRACTION of CLAIM 3

Run in session44/lead4 as `uz_*.py`.  Method: a completely independent
formulation of `[P,Q] = x^2` on the subcase-2 polygons, cross-checked against a
direct bracket computation in (x,y); it does NOT use any face-form assumption.

## The reformulation

Put u = x y^2, v = y, z = 1/v.  A monomial x^i y^j is u^i v^(j-2i), so the
weight w = j - 2i is the v-exponent, and both polygons are thin in it:
w in {0,-1,-2} on N(P) and {0,-1,-2,-3} on N(Q).  Hence

    P = f(u) + p(u) z + q(u) z^2                deg_u <= 8
    Q = g(u) + r(u) z + s(u) z^2 + t(u) z^3     deg_u <= 12

with p,q,r = O(u), s,t = O(u^2), and (since d(u,v)/d(x,y) = y^2 and
dv/dz = -z^-2)

    [P,Q]_{x,y} = x^2     <==>     [P,Q]_{u,z} = -u^2 z^4 .

Dictionary to the descent's symbols a_j_i = coeff of x^i y^j:

    f_a = a_{2a}_{a}  (the (0,0)-(8,16) face!),  p_a = a_{2a-1}_{a},
    q_a = a_{2a-2}_{a}                so   a_2_1 = f1, a_4_2 = f2,
                                           a_10_5 = f5, a_1_1 = p1,
                                           a_3_2 = p2, a_6_3 = f3,
                                           a_0_1 = q1 (= 1, scaling gauge).

Everything is weighted-homogeneous for W(f_a)=5a+1, W(p_a)=5a-2, W(q_a)=5a-5
(the residual gauge torus), and the equation of bidegree (u^n, z^k) has weight
5n-3k+2.  Eliminating g,r,s,t (they are determined triangularly) leaves 45
obstructions in f1..f8, p1..p8, q2..q8, exactly over Q.

## Validation

  * the (u,z) equations reproduce a direct (x,y) bracket on random data;
  * the descent's obstructions come out IDENTICALLY:
        level  4: (2,0) = f1^2                        = a_2_1^2
        level  6: (3,0) = p1^2 f2 /5 (mod f1)          = a_1_1^2 a_4_2
        level  8: (4,0) = 12/5 f2^2 (mod f1, p1)       = 4 a_4_2^2
        level 12: (6,0) = -(27 f3^2 - 9 f3 p2^2 + p2^4)/7 (mod f1,f2,p1)
                                = a_3_2^4 - 9 a_3_2^2 a_6_3 + 27 a_6_3^2
  * control: msolve over GF(65521) gives ideal + (a_2_1 - 1) = (1), so
    a_2_1 = 0 really is forced.

## a_2_1 = 0 and a_4_2 = 0 are THEOREMS over Q, not hypotheses

The task's two inputs need not be assumed; radical propagation on the exact
obstruction system proves both unconditionally in characteristic zero:

    (2,0) = f1^2                      =>  a_2_1 = f1 = 0        (all branches)
    (3,0) = (1/5) f2 p1^2             =>  f2 = 0  or  p1 = 0
      on p1 = 0:  (4,0) = (12/5) f2^2 =>  f2 = 0
    hence                                 a_4_2 = f2 = 0        (all branches)

So the descent's level-4 and level-8 conclusions hold with no branch caveat,
exactly over Q.  (The level-6 obstruction a_1_1^2 a_4_2 is reproduced here as
the single monomial f2 p1^2.)

## The cascade that decides everything

The obstructions split by z-degree into a triangular cascade:

    (n,4), n=13..18   6 eqs, in q2..q8 ONLY
    (n,3), n=13..19   7 eqs, LINEAR homogeneous in p over Q[q]
    (n,2), n=13..19   7 eqs, LINEAR in f, quadratic in p (no f*p mixing --
                      forbidden by the weight)
    (n,1), n=13..19   7 eqs
    (n,0), n= 2..19  18 eqs

The q-layer, with the torus gauge q8 = 1 (q8 = a_14_8 != 0 is exactly the
vertex (8,14) of N(P)), is 0-dimensional of degree 35 -- confirmed
independently by Singular (dim = 0, vdim = 35), which is what makes the
enumeration below provably exhaustive rather than merely a sample.  Over GF(999983) its
eliminating polynomial factors into irreducibles of degrees 1,1,3,6,6,6,6,6;
running the cascade over GF(999983)[a]/(h) for every factor covers ALL 35
solutions.  For each one the p-layer kernel is 2-dimensional and ker(M) on the
f-layer is 2-dimensional, so the whole remaining system is 4 unknowns and 25
equations -- decided instantly by Singular.

## RESULT

For every one of the 35 q's (128/128 saturation tests, GF(999983); repeated for
9 GF(p)-rational q's at 8 further primes):

    f1 = f2 = f3 = f4 = f5 = f6 = f7 = f8 = 0   and
    p1 = p2 = p3 = p4 = p5 = p6 = p7 = p8 = 0   are ALL forced.

So:

  1. a_10_5 = f5 = 0 IS forced ON SUBCASE 2 (i.e. once a_14_8 != 0, the vertex
     (8,14), is imposed).  The prediction of PREDICTION_AND_SUBCASE1.md
     survives its falsification test in that -- and only that -- reading; see
     "SHARPENING" below, where an exact char-0 solution with a_2_1 = a_4_2 = 0
     and a_10_5 != 0 is exhibited on a degenerate polygon.

  2. But so are a_6_3, a_8_4, a_12_6, a_14_7 and a_16_8.  The only solutions
     are   P = a_00 + q(u) z^2 ,  Q = b_00 + t(u) z^3 ,  with 2qt' - 3q't = u^2
     -- verified end to end: [P,Q] = x^2 exactly, with
        N(P) = conv{(0,0),(1,0),(8,14)}  and  N(Q) = conv{(0,0),(2,1),(12,21)},
     triangles, NOT the subcase-2 quadrilaterals.

  3. a_16_8 = 0 kills the vertex (8,16).  Modulo the prime, therefore,
     OPEN SUBCASE 2 IS EMPTY.

## RETRACTION: CLAIM 3 above is WRONG

CLAIM 2 ("the two face forms must commute") is true but VACUOUS, and CLAIM 3
does not follow from it.  On the w-max face the face forms are

    face(P) = sum_a a_{2a}_a x^a y^{2a} = f(x y^2),   face(Q) = g(x y^2),

i.e. both are polynomials in the SINGLE quantity u = x y^2, so
[face(P), face(Q)] = 0 identically for ARBITRARY coefficients (checked
symbolically on random f of degree 8 and g of degree 12).  The lemma
"commuting quasi-homogeneous forms are powers of a common form" needs a
POSITIVE weight; here the face has w-degree 0 for the indefinite weight
w = j - 2i, and the w = 0 graded piece is a commutative subalgebra in which
every pair commutes.  So gcd(8,12) = 4 gives NOTHING, and

    face(P) = R^2,  face(Q) = R^3,  deg R = 4        is UNFOUNDED.

A second defect: the premise "a_0 = c0^2 != 0 because (0,0) is a vertex" is
not a constraint at all -- a_0_0 is the constant term of P, which never occurs
in [P,Q] (constants are in the kernel of the bracket).  It is a free
normalisation, and the descent's ideal is entirely independent of it.

Consistency check on the retraction: the true forced face form is
f = a_0_0 (a constant), which is NOT of the shape R^2 with
R = c0 + c3 u^3 + c4 u^4 and c4 != 0.  The gapped-quartic picture, the
"at most a double root" statement and the discriminant c0^2(256 c0 c4^3 -
27 c3^4) should all be withdrawn.  What survives is stronger and different:
the face collapses to a single point, and subcase 2 is empty.

## Status / caveats

  * The elimination and the 45 obstructions are EXACT over Q.
  * The decision (all f_a, p_a forced to 0) is MODULAR.  It is COMPLETE over
    all 35 solutions of the q-layer at THREE primes:
        p =  999983  eliminant factors 1,1,3,6,6,6,6,6   -> 128/128 forced-zero
        p = 1000003  eliminant factors 1,2,2,3,3,6,6,6,6 -> 144/144 forced-zero
        p = 1500007  eliminant factors 2,3,6,6,6,6,6     -> 112/112 forced-zero
    and holds for 9 GF(p)-rational q at 8 further primes.  It is not yet a
    characteristic-zero proof: a mod-p verdict does not formally lift, though a
    char-0 point with f5 != 0 would reduce to one mod almost every prime, so two
    complete primes plus eight partial ones is strong.
  * Direct Groebner attempts on the whole ungauged 20-23 variable system
    (msolve, GF(65521), 90 min) did not terminate; the layered cascade is what
    makes the problem decidable at all.
  * It covers deg q = 8, which is forced by the vertex (8,14) of N(P), so it
    covers all of subcase 2.

## SHARPENING: the vertex condition is INDISPENSABLE (exact, char 0)

The branch deg q = 1 (q = u, i.e. a_14_8 = 0 -- outside subcase 2, but inside
the descent's raw ideal, which only imposes SUPPORTS) is decided exactly over
Q by radical propagation: obstruction (16,2) = c*p8^2, then (14,2) = c*p7^2,
(17,1) = c*p6^3, (14,1) = c*p5^3, (16,0) = c*f8^2, each a pure power of a
single variable, so p5 = p6 = p7 = p8 = f8 = 0 exactly.  The remainder is 9
unknowns / 11 obstructions, and on the ansatz f = a00 + u^5, p = alpha u^3 the
entire system collapses to the SINGLE exact equation

        7 alpha^4 - 60 alpha^2 + 150 = 0        (irreducible over Q)

giving, over the quartic field K = Q[alpha]/(that), the EXACT solution

  P = a00 + x + alpha x^3 y^5 + x^5 y^10
  Q = b00 + x^2 y + (7 alpha/6) x^4 y^6 + (7 alpha^2/33 + 15/11) x^6 y^11
          + (alpha(250 - 21 alpha^2)/528) x^8 y^16

verified symbolically:  [P,Q] = x^2  identically in K[x,y].  Its supports lie
inside N(P) and N(Q), and

        a_2_1 = 0 ,   a_4_2 = 0 ,   but   a_10_5 = 1 != 0 .

So, stated precisely:

  * from the bracket equation + supports + (a_2_1 = 0, a_4_2 = 0) ALONE,
    a_10_5 = 0 does NOT follow -- there is an explicit characteristic-zero
    counterexample;
  * it follows only once the vertex condition a_14_8 != 0 (the vertex (8,14)
    of N(P)) is also imposed -- i.e. only on genuine subcase 2, where in fact
    the whole face collapses and the subcase is empty.

This witness also refutes the edge-gap pattern head on: its face coefficients
along (0,0)-(8,16) are (a00, 0,0,0,0, 1, 0,0,0), i.e. a_1 = a_2 = 0 with
a_5 != 0 -- exactly the opposite of the predicted "gap at 1,2,5".  (f = a00+u^5
is of course not R^2 either.)

Branch tally for the RAW ideal (supports + f1 = f2 = 0, no vertex condition).
deg q must lie in {1,2,4,6,8}: the leading coefficient of 2qt' - 3q't = u^2 is
(2 deg t - 3 deg q) q_top t_top, so either 2 deg t = 3 deg q (deg q even) or
deg q + deg t - 1 = 2, i.e. q = u.  Verified computationally as well -- fixing
q_m = 1, q_a = 0 for a > m and solving the q-layer gives

    m = 1,2  q-layer imposes nothing        m = 3,5,7  EMPTY
    m = 4,6,8                SOLUTIONS

    deg q = 8  a_14_8 != 0  -- SUBCASE 2.  a_10_5 = 0 forced (with everything
                              else on the face); complete over all 35 q at two
                              primes.  Subcase 2 is EMPTY.
    deg q = 2                 a_10_5 = 0 forced (msolve, GF(999983): the
                              saturated ideal is (1)).
    deg q = 1                 a_10_5 != 0 POSSIBLE -- the exact witness above.
    deg q = 4, 6              pending.

None of the deg q < 8 branches has the vertex (8,14), so none of them can
affect the subcase-2 conclusion.
