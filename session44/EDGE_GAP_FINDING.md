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
