# night14 CRUX_f036c423cf2f

Object (ring: Q[x,y]), family F2 -- F2 n=3 c=-2 a=2 h0=1 t=[(0, Fraction(3, 1))]

    P   = -2*x^3*y^2 - 6*x^3*y + 12*x^2*y^2 + (-9/2)*x^3 + 36*x^2*y - 24*x*y^2 + 27*x^2 - 72*x*y + 16*y^2 - 54*x + 49*y + (75/2)
    P_x = -6*x^2*y^2 - 18*x^2*y + 24*x*y^2 + (-27/2)*x^2 + 72*x*y - 24*y^2 + 54*x - 72*y - 54
    P_y = -4*x^3*y - 6*x^3 + 24*x^2*y + 36*x^2 - 48*x*y - 72*x + 32*y + 49

total degree 5, deg_x 3, deg_y 2, 12 terms.
hash = sha256 of the canonical string form of P, first 12 hex digits.

## (a) U-test -- 1 in (P_x, P_y)

    mod-p shadow (p = 999983, Singular groebner) : PASS   0.008 s
    char-0 verdict (Singular groebner, ring 0)   : PASS   0.008 s   <- recorded verdict

So P_x and P_y have no common zero over C: the critical locus of P is empty
and every fibre of P is smooth.

## (b) SY-certificate -- gradient-row reduction over Q

    verdict NON_COORDINATE   nodes = 1  leaves = 1   0.0 s

## Independent corroboration of (b) -- FIB-screen, no SY involved

    verdict NON_COORDINATE_BY_R
    (lambda, number of factors of P - lambda over Q, geometric genus if
     irreducible): [['0', 2, None], ['1', 1, 1], ['-1', 1, 1]]
    0.168 s

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
      r = [r for r in json.load(open('records.json')) if r['hash']=='f036c423cf2f'][0]; \
      print(r['poly'], r['u_q'], r['sy'], r['fib'])"
