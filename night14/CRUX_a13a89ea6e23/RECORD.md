# night14 CRUX_a13a89ea6e23

Object (ring: Q[x,y]), family F2 -- F2 n=2 c=-2 a=2 h0=1 t=[(0, Fraction(-2, 1)), (1, Fraction(2, 1)), (2, Fraction(-1, 1))]

    P   = (-1/2)*x^6 + 4*x^5 + 2*x^4*y - 14*x^4 - 12*x^3*y - 2*x^2*y^2 + 28*x^3 + 28*x^2*y + 8*x*y^2 + (-69/2)*x^2 - 32*x*y - 8*y^2 + 25*x + 17*y - 9
    P_x = -3*x^5 + 20*x^4 + 8*x^3*y - 56*x^3 - 36*x^2*y - 4*x*y^2 + 84*x^2 + 56*x*y + 8*y^2 - 69*x - 32*y + 25
    P_y = 2*x^4 - 12*x^3 - 4*x^2*y + 28*x^2 + 16*x*y - 32*x - 16*y + 17

total degree 6, deg_x 6, deg_y 2, 15 terms.
hash = sha256 of the canonical string form of P, first 12 hex digits.

## (a) U-test -- 1 in (P_x, P_y)

    mod-p shadow (p = 999983, Singular groebner) : PASS   0.008 s
    char-0 verdict (Singular groebner, ring 0)   : PASS   0.008 s   <- recorded verdict

So P_x and P_y have no common zero over C: the critical locus of P is empty
and every fibre of P is smooth.

## (b) SY-certificate -- gradient-row reduction over Q

    verdict NON_COORDINATE   nodes = 4  leaves = 2   0.001 s

## Independent corroboration of (b) -- FIB-screen, no SY involved

    verdict NON_COORDINATE_BY_R
    (lambda, number of factors of P - lambda over Q, geometric genus if
     irreducible): [['0', 2, None], ['1', 1, 0], ['-1', 1, 0]]
    0.198 s

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
      r = [r for r in json.load(open('records.json')) if r['hash']=='a13a89ea6e23'][0]; \
      print(r['poly'], r['u_q'], r['sy'], r['fib'])"
