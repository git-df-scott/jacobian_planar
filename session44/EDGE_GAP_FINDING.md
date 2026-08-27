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
