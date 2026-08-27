# Independent verification of the (72,108) verdicts

Everything in this directory was built from scratch, in the original (x,y)
coordinates, without reusing the subcase agents' system builders.  The point
is that agreement should be evidence and not an echo.

## What was rebuilt and what it confirms

`indep2.py` — polygon lattice points by an exact half-plane test, and the
bracket expanded directly on monomials via
`[x^a y^b, x^c y^d] = (ad-bc) x^(a+c-1) y^(b+d-1)`.

    N(P) = conv{(0,0),(1,0),(8,14),(8,16)}   25 lattice points
    N(Q) = conv{(0,0),(2,1),(12,21),(12,24)} 47 lattice points
    92 bracket equations, splitting by w = j-2i as 17 / 18 / 19 / 19 / 19
    the target x^2 sits at the DEEPEST level w = -4

Independently reproduces the campaign's counts (72 unknowns, 92 equations)
and the essential-face phenomenon.

`uz_indep.py` — the substitution u = x y^2, z = 1/y re-derived here.  Its
Jacobian is det [[y^2, 2xy],[0, -y^-2]] = -1, hence

    [P,Q]_{x,y} = - [P,Q]_{u,z},    x^2 = u^2 z^4.

With P = f + p z + q z^2 and Q = g + r z + s z^2 + t z^3 the five identities
were derived by hand:

    z^0:  f'r - p g'                            = 0
    z^1:  2f's + p'r - p r' - 2q g'             = 0
    z^2:  3f't + 2p's + q'r - p s' - 2q r'      = 0
    z^3:  3p't + 2q's - p t' - 2q s'            = 0
    z^4:  3q't - 2q t'                          = -u^2

CROSSCHECK PASSES at three random seeds: the direct (x,y) bracket equals
minus the rebuilt (u,z) side, exactly.  So the reformulation both agents
relied on is sound.

## Confirmed numbers

* essential face `2 q t' - 3 q' t = u^2` with the two gauges q1 = q8 = 1:
  **17 equations, 17 unknowns, dim 0, vdim = 35** (Singular, p = 32003).
  Independently reproduces the degree-35 count reached by three other
  instruments, and the 35 = 5 covers x mu_7 structure follows from the
  residual gauge group (q_k -> L^(k-8) q_k with L^7 = 1 once q1 = q8 = 1).

* leading/trailing coefficient analysis of the face equation: with
  deg q = D, deg t = E, val q = d, val t = e, the extreme coefficients are
  (3D-2E) q_D t_E and (3d-2e) q_d t_e.  Subcase 2 needs q_1, q_8, t_2, t_12
  nonzero (they are the vertices), so d + e = 3 puts the target at the
  bottom and 3D = 2E forces **(deg q, deg t) = (8,12)** exactly.

## A characteristic-zero step, no computer needed

If p = s = 0 the remaining identities read  -2 q g' = 0,  3 f' t + q' r = 0,
f' r = 0.  Since q, t are nonzero and deg q = 8 gives q' =/= 0:
from f'r = 0 either f' = 0 or r = 0; if r = 0 then 3f't = 0 forces f' = 0;
if f' = 0 then q'r = 0 forces r = 0.  Either way f' = r = g' = 0, so f and g
are CONSTANTS, hence

    f_8  = 0   (the vertex (8,16) of N(P) is absent)
    g_12 = 0   (the vertex (12,24) of N(Q) is absent)

and the Newton polygons are not the claimed quadrilaterals.  So the whole
subcase turns on the single question "can (p,s) be nonzero?" -- which is
what the modular cascades answer.

## Independently verified witness

The exact characteristic-zero pair found on the deg q = 1 branch,

    P = x + a x^3 y^5 + x^5 y^10
    Q = x^2 y + (7a/6) x^4 y^6 + (7a^2/33 + 15/11) x^6 y^11
          + a(250 - 21a^2)/528 x^8 y^16,     7a^4 - 60a^2 + 150 = 0

was re-checked here: [P,Q] - x^2 reduces to exactly 0 modulo the quartic.
It is a genuine solution of the reduced Laurent problem and it is NOT a
counterexample -- its Newton polygon is the triangle conv{(0,0),(1,0),(5,10)},
the vertices (8,14) and (8,16) are absent, and [P,Q] = x^2 is not a nonzero
constant in original coordinates.
