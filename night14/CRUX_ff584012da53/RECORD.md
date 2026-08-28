# night14 CRUX_ff584012da53

Object (ring: Q[x,y]), family F2 -- F2 n=4 c=2 a=2 h0=-1 t=[(0, Fraction(3, 1)), (1, Fraction(-2, 1)), (2, Fraction(-1, 1))]

    P   = (1/2)*x^8 - 2*x^7 - 2*x^6*y - 5*x^6 + 12*x^5*y + 2*x^4*y^2 + 34*x^5 - 10*x^4*y - 16*x^3*y^2 + (-55/2)*x^4 - 80*x^3*y + 48*x^2*y^2 - 116*x^3 + 240*x^2*y - 64*x*y^2 + (569/2)*x^2 - 256*x*y + 32*y^2 - 239*x + 95*y + (141/2)
    P_x = 4*x^7 - 14*x^6 - 12*x^5*y - 30*x^5 + 60*x^4*y + 8*x^3*y^2 + 170*x^4 - 40*x^3*y - 48*x^2*y^2 - 110*x^3 - 240*x^2*y + 96*x*y^2 - 348*x^2 + 480*x*y - 64*y^2 + 569*x - 256*y - 239
    P_y = -2*x^6 + 12*x^5 + 4*x^4*y - 10*x^4 - 32*x^3*y - 80*x^3 + 96*x^2*y + 240*x^2 - 128*x*y - 256*x + 64*y + 95

total degree 8, deg_x 8, deg_y 2, 21 terms.
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
    0.196 s

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
      r = [r for r in json.load(open('records.json')) if r['hash']=='ff584012da53'][0]; \
      print(r['poly'], r['u_q'], r['sy'], r['fib'])"
