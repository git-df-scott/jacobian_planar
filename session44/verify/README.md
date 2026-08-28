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

---

# INDEPENDENT END-TO-END VERDICT ON SUBCASE 2

Reached entirely with instruments built in this directory.

## How the blocker was cleared

The campaign had been stuck because the 35 essential-face solutions live in a
degree-35 extension and would not come out as explicit tuples: msolve's RUR
would not parse, and its eliminant is taken with respect to a linear form of
its own choosing, which had produced wrong substitutions.

FGLM clears it in 28 seconds.  The face ideal is zero-dimensional with
vdim 35, so `stdfglm` converts the cheap degree-order basis to a lex basis,
which for a zero-dimensional ideal is triangular.  At p = 5189 it is:

    t9^5 + ...                     <- DEGREE 5: the five covers
    t8^7 + (quartic in t9)         <- DEGREE 7: the mu_7
    t2 - 1                         <- t2 = 1 exactly
    every other coordinate = a polynomial in t8, t9

So 35 = 5 x 7 is not inferred, it is read off the basis.  Because 7 does not
divide p-1, x -> x^7 is a bijection of F_p*, so each root of the quintic has
exactly ONE seventh root: five roots of the quintic give exactly five
F_p-rational points, one per cover, covering all 35 by the mu_7 symmetry.

All five were substituted back and verified against 2 q t' - 3 q' t = u^2,
exactly, at both primes.  5/5 at p = 5189 and 5/5 at p = 5441.

## The verdict

At an explicit face point the four identities E0..E3 become 75 equations in
51 unknowns (f1..f8, p1..p8, g1..g12, r1..r12, s2..s12 -- f0 and g0 are
absent, as they must be, since constant terms never enter the bracket), of
degrees 1 and 2.

    CONTROL (no vertex condition):        LIVE, dim 0     <- engine is sound
    MAIN (f8 and g12 both nonzero):       EMPTY, 5/5 covers, p = 5189
                                          EMPTY, 5/5 covers, p = 5441

Each cover decides in under a second.  The hours the other routes spent were
spent working over field extensions; with an explicit rational face point at
a well-chosen prime the system collapses.

## The mechanism, which is sharper than the verdict

Without any vertex condition the system at a face point is dim 0 with
vdim 10, and its lex basis begins with `s9^4` -- a NILPOTENT.  The reduced
solution set is therefore a single fat point at the origin: the only solution
is

    f = p = r = s = g = 0,

i.e. P = a00 + q(u) z^2 and Q = b00 + t(u) z^3 and nothing else.  In
particular f8 = 0 and g12 = 0, so the vertices (8,16) of N(P) and (12,24) of
N(Q) are both absent and neither Newton polygon is the claimed quadrilateral.

This reproduces, independently and by a different route, the conclusion the
two subcase agents reached: the only survivors are the triangular pairs.

## Status

MODULAR, at two primes, with a passing positive control and a passing
soundness control.  A characteristic-zero run (`fglm_char0.sing`, stdfglm over
Q on the face ideal) is the remaining step; with the face available over Q the
same 75/51 system decides the subcase over Q(face) and the result becomes a
theorem rather than evidence.

---

# THE OBSTRUCTION HAS A SHORT CERTIFICATE

Probing *why* the system is empty turned up something sharper than the
verdict, and it is the right object for a characteristic-zero proof.

At a face point, modulo the ideal generated by E0..E3:

    f8   is NOT in the ideal          g12   is NOT in the ideal
    f8^2 IS  in the ideal             g12^2 IS  in the ideal

so both vertex coordinates are nilpotent of index exactly 2.  That is what
produces the fat point of length 10 seen earlier, and it says the vertices
(8,16) and (12,24) cannot be nonzero -- without any Rabinowitsch trick.

Singular's `lift` produces the certificate explicitly:

    f8^2 = sum_i h_i E_i ,   72 nonzero multipliers, degrees 0..3
    verified inside Singular: chk - f8^2 == 0

Checked at two covers; identical structure at both.

## Why this matters

A modular Groebner verdict does not lift to characteristic zero without a
bound on bad primes, which nobody has computed here.  An explicit identity
does: if the same certificate can be written with multipliers whose
coefficients lie in the face ring -- i.e.

    f8^2 = sum_i h_i E_i   modulo the face ideal, over Q

-- then f8 vanishes on every solution in characteristic zero and subcase 2 is
empty as a THEOREM, not as evidence.  The identity is finite and independently
checkable by expansion, so it needs no trust in any Groebner engine.

What stands in the way is only the face ideal over Q: the certificate above
is computed at an F_p point.  Two routes, neither yet completed here:
reconstruct the face lex basis from many primes (data collection in
`recon.py`), or compute it over Q directly.

## What is NOT claimed

The certificate is currently a MOD-P object.  Nothing above upgrades the
verdict to characteristic zero yet.  A shortcut that was considered and
REJECTED: reconstructing the lex basis from many primes gives `<face>` inside
`<reconstructed>`, i.e. V(reconstructed) inside V(face) -- the wrong
inclusion.  Proving emptiness over V(reconstructed) would not cover V(face),
so that route needs an ideal-membership check in the other direction, which
is exactly the characteristic-zero computation it was meant to avoid.
