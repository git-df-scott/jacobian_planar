# night14 CRUX_90ed45a6e2a0

Object (ring: Q[x,y]), family F2 -- F2 n=4 c=2 a=-1 h0=-1 t=[(0, Fraction(-3, 1)), (2, Fraction(3, 1))]

    P   = (9/2)*x^8 + 18*x^7 + 6*x^6*y + 18*x^6 + 24*x^5*y + 2*x^4*y^2 - 18*x^5 + 30*x^4*y + 8*x^3*y^2 - 45*x^4 + 12*x^2*y^2 - 18*x^3 - 30*x^2*y + 8*x*y^2 + (33/2)*x^2 - 24*x*y + 2*y^2 + 18*x - 7*y + 6
    P_x = 36*x^7 + 126*x^6 + 36*x^5*y + 108*x^5 + 120*x^4*y + 8*x^3*y^2 - 90*x^4 + 120*x^3*y + 24*x^2*y^2 - 180*x^3 + 24*x*y^2 - 54*x^2 - 60*x*y + 8*y^2 + 33*x - 24*y + 18
    P_y = 6*x^6 + 24*x^5 + 4*x^4*y + 30*x^4 + 16*x^3*y + 24*x^2*y - 30*x^2 + 16*x*y - 24*x + 4*y - 7

total degree 8, deg_x 8, deg_y 2, 20 terms.
hash = sha256 of the canonical string form of P, first 12 hex digits.

## (a) U-test -- 1 in (P_x, P_y)

    mod-p shadow (p = 999983, Singular groebner) : PASS   0.008 s
    char-0 verdict (Singular groebner, ring 0)   : PASS   0.007 s   <- recorded verdict

So P_x and P_y have no common zero over C: the critical locus of P is empty
and every fibre of P is smooth.

## (b) SY-certificate -- gradient-row reduction over Q

    verdict NON_COORDINATE   nodes = 4  leaves = 2   0.001 s

## Independent corroboration of (b) -- FIB-screen, no SY involved

    verdict NON_COORDINATE_BY_R
    (lambda, number of factors of P - lambda over Q, geometric genus if
     irreducible): [['0', 2, None], ['1', 1, 1], ['-1', 1, 1]]
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
      r = [r for r in json.load(open('records.json')) if r['hash']=='90ed45a6e2a0'][0]; \
      print(r['poly'], r['u_q'], r['sy'], r['fib'])"
