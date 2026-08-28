# night14 CRUX_9caad9cebba8

Object (ring: Q[x,y]), family F2 -- F2 n=2 c=2 a=1 h0=2 t=[(0, Fraction(1, 1)), (1, Fraction(-2, 1)), (2, Fraction(1, 1))]

    P   = (1/2)*x^6 - 3*x^5 + 2*x^4*y + (15/2)*x^4 - 8*x^3*y + 2*x^2*y^2 - 10*x^3 + 12*x^2*y - 4*x*y^2 + (17/2)*x^2 - 8*x*y + 2*y^2 - 5*x + 4*y + (3/2)
    P_x = 3*x^5 - 15*x^4 + 8*x^3*y + 30*x^3 - 24*x^2*y + 4*x*y^2 - 30*x^2 + 24*x*y - 4*y^2 + 17*x - 8*y - 5
    P_y = 2*x^4 - 8*x^3 + 4*x^2*y + 12*x^2 - 8*x*y - 8*x + 4*y + 4

total degree 6, deg_x 6, deg_y 2, 15 terms.
hash = sha256 of the canonical string form of P, first 12 hex digits.

## (a) U-test -- 1 in (P_x, P_y)

    mod-p shadow (p = 999983, Singular groebner) : PASS   0.007 s
    char-0 verdict (Singular groebner, ring 0)   : PASS   0.007 s   <- recorded verdict

So P_x and P_y have no common zero over C: the critical locus of P is empty
and every fibre of P is smooth.

## (b) SY-certificate -- gradient-row reduction over Q

    verdict NON_COORDINATE   nodes = 4  leaves = 2   0.001 s

## Independent corroboration of (b) -- FIB-screen, no SY involved

    verdict NON_COORDINATE_BY_R
    (lambda, number of factors of P - lambda over Q, geometric genus if
     irreducible): [['0', 2, None], ['1', 1, 0], ['-1', 1, 0]]
    0.19 s

Reason recorded: because the U-test passed, every fibre of P is smooth, so
two distinct components of a fibre would meet in a singular point -- a
reducible fibre is therefore a disconnected one.  A coordinate has every
fibre isomorphic to the affine line, which is connected and of genus 0.  So
the observation above is by itself a proof that P is not a component of any
polynomial automorphism.

## Scope note

Gradient-unimodularity is the necessary condition (a) only.  Nothing here
measures whether P admits a Jacobian mate, and no such claim is made.

## Reproduce

    cd night14 && python3 -c "import json, poly14 as P, sy14, utest14, fib14; \
      r = [r for r in json.load(open('records.json')) if r['hash']=='9caad9cebba8'][0]; \
      print(r['poly'], r['u_q'], r['sy'], r['fib'])"
