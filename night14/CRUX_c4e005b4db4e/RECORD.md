# night14 CRUX_c4e005b4db4e

Object (ring: Q[x,y]):

    P = x + x^2*y

    P_x = 2*x*y + 1
    P_y = x^2

sha256(to_str(P))[:12] = c4e005b4db4e ; total degree 3 ; family F3-seed
(the object also arises as the y-degree-1 boundary case of the F2 normal form,
see PROSPECTOR.md).

## Measurement (a) U-test

    mod-p shadow (p = 999983, Singular groebner) : PASS       0.008 s
    char-0 verdict (ring 0, Singular groebner)   : PASS       0.007 s

So 1 in (P_x, P_y) over Q; equivalently P_x, P_y have no common zero over C;
equivalently the critical locus of P is empty and every fibre of P is smooth.

Hand check of the same statement: P_y = x^2 = 0 forces x = 0, and then
P_x = 1 != 0.  Explicit unimodular combination over Q[x,y], verified by
expansion:

    1 = (1 - 2*x*y) * P_x  +  4*y^2 * P_y
      = (1 - 2*x*y)*(2*x*y + 1) + 4*y^2*x^2
      = 1 - 4*x^2*y^2 + 4*x^2*y^2.

## Measurement (b) SY-certificate

    rows (P_x, P_y) = (2*x*y + 1, x^2)
    LM(P_x) = x*y  (tdeg 2), LM(P_y) = x^2 (tdeg 2)
    x*y does not divide x^2 and x^2 does not divide x*y

    -> no elementary reduction applies at the root; the DAG is a single node,
       one leaf, and no (c, 0) leaf occurs.

    SY verdict: NON_COORDINATE     nodes = 1  leaves = 1   < 0.001 s

## Independent corroboration of (b), not relying on the SY instrument

The fibre P = 0 is  x*(1 + x*y) = 0, the union of the line {x = 0} and the
curve {x*y = -1}.  The two components are disjoint (x = 0 forces x*y = 0).
So the fibre P = 0 is a disconnected (hence reducible, hence non-line) smooth
curve.  A coordinate has every fibre isomorphic to the affine line, which is
connected.  Therefore P is not a component of any polynomial automorphism.

## Status of this object

Both measured properties hold: U-test PASS (char 0) and SY NON_COORDINATE,
with the non-coordinate half independently corroborated by the fibre argument.

Scope note recorded with the object: gradient-unimodularity is the necessary
condition (a) only.  This object is not measured here to possess a Jacobian
mate, and no such claim is made from these two measurements.

## Reproduce

    cd night14 && python3 -c "import poly14 as P, sy14, utest14; \
      p = P.clean({(1,0):1,(2,1):1}); print(utest14.utest(p), sy14.certify(p))"
