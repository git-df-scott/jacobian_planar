# night14 CRUX_e26d53b6cb1e

Object (ring: Q[x,y]), family F2b -- F2b n=2 c=-1 h0=2 d_n=1 s=[(0, Fraction(1, 1)), (1, Fraction(-2, 1))]

    P   = -1*x^4 - 2*x^3*y - 1*x^2*y^2 + x^3 + x^2*y + (-1/4)*x^2 + 2*x + 2*y + (-3/4)
    P_x = -4*x^3 - 6*x^2*y - 2*x*y^2 + 3*x^2 + 2*x*y + (-1/2)*x + 2
    P_y = -2*x^3 - 2*x^2*y + x^2 + 2

total degree 4, deg_x 4, deg_y 2, 9 terms.
hash = sha256 of the canonical string form of P, first 12 hex digits.

## (a) U-test -- 1 in (P_x, P_y)

    mod-p shadow (p = 999983, Singular groebner) : PASS   0.008 s
    char-0 verdict (Singular groebner, ring 0)   : PASS   0.007 s   <- recorded verdict

So P_x and P_y have no common zero over C: the critical locus of P is empty
and every fibre of P is smooth.

## (b) SY-certificate -- gradient-row reduction over Q

    verdict NON_COORDINATE   nodes = 3  leaves = 2   0.0 s

## Independent corroboration of (b) -- FIB-screen, no SY involved

    verdict NON_COORDINATE_BY_R
    (lambda, number of factors of P - lambda over Q, geometric genus if
     irreducible): [['0', 1, 0], ['1', 1, 0], ['-1', 1, 0], ['1/4', 2, None]]
    0.208 s

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
      r = [r for r in json.load(open('records.json')) if r['hash']=='e26d53b6cb1e'][0]; \
      print(r['poly'], r['u_q'], r['sy'], r['fib'])"
