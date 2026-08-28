# The face-power premise is false; the correct structure sits on the other face

Session 44, lead 4.  Everything below was checked by machine, not asserted.

## 1. The premise I was told to impose is not true

FACE_STRUCTURE_CENSUS.md and EDGE_GAP_FINDING.md state, as a VERIFIED fact,
that on the w-maximal face of the open (72,108) subcase 2 (w(i,j) = j - 2i,
the face from (0,0) to (8,16) of N(P) and from (0,0) to (12,24) of N(Q))
the two face forms must commute, and that therefore

    face(P) = R^2,  face(Q) = R^3,  deg R = 4.

The first half is true and the second half does not follow.  Both were
re-derived here:

  * the commuting statement is VACUOUS on this face.  The face lies on the
    line j = 2i THROUGH THE ORIGIN, so every monomial on it is a power of
    t = x*y^2, both face forms are polynomials in that single monomial, and
    [f(t), g(t)] = 0 for ALL coefficient values.  Machine check: the
    w-level 0 component of [P,Q] is identically zero as a polynomial in the
    25 + 47 unknown coefficients (chk3.py).

  * explicit counterexample to the conclusion:
        F = 1 + x^8 y^16 = 1 + t^8 ,   G = 1 + x^12 y^24 = 1 + t^12 .
    [F,G] = 0 (direct: 8*24 - 16*12 = 0 on the only cross term), F has 8
    distinct roots in t, so F is not the square of a quartic.  A commuting
    pair on this face need not be (R^2, R^3).

  So the 12 "perfect-power" constraints the census promised for subcase 2
  do not exist, and the 1506-face census inherits the same error wherever
  the recorded face runs through the origin.  Imposing them up front, as
  the brief asked, would have cut down the solution set illegitimately and
  could have produced a spurious EMPTY.

## 2. What IS true, and it is better

Grade both polynomials by the same weight.  N(P) and N(Q) are thin in it:

    P = f0(t) + f1(t)/y + f2(t)/y^2                    (w = 0,-1,-2)
    Q = g0(t) + g1(t)/y + g2(t)/y^2 + g3(t)/y^3        (w = 0,...,-3)

with t = x*y^2.  Then [P,Q] = sum_{m,n} (m f_m g_n' - n f_m' g_n) y^(1-m-n),
verified symbolically against the direct bracket, and [P,Q] = x^2 splits
into exactly five polynomial identities in the single variable t:

    m+n=0:  0 = 0                                        (the vacuous face)
    m+n=1:  f1 g0' - f0' g1 = 0
    m+n=2:  2 f2 g0' + f1 g1' - f1' g1 - 2 f0' g2 = 0
    m+n=3:  -3 f0' g3 + f1 g2' - 2 f1' g2 + 2 f2 g1' - f2' g1 = 0
    m+n=4:  f1 g3' - 3 f1' g3 + 2 f2 g2' - 2 f2' g2 = 0
    m+n=5:  2 f2 g3' - 3 f2' g3 = t^2

The last line is the real structural constraint, and it lives on the
w-MINIMAL face, not the maximal one.  Note what it would say if its right
side were 0: 2FG' = 3F'G forces G^2 = c F^3, i.e. exactly F = R^2, G = R^3.
The census's (2,3) instinct was aimed at the right pair of exponents and
the wrong face; on the right face the equation is INHOMOGENEOUS, so the
perfect-power conclusion is exactly what fails, by t^2.

## 3. The core system, solved

With f2 = t*A(t) (deg A = 7) and g3 = t^2*B(t) (deg B = 10), the m+n=5
identity is

    sum_{i+j=k} (1 + 2j - 3i) A_i B_j = [k = 0],   k = 0 .. 17

(k=17 vanishes identically).  The B_k coefficient in equation k is
(1+2k)A_0 and A_0 = a_(1,0) != 0 is a vertex of N(P), so B_0..B_10 are
determined recursively by A and SIX conditions in A_1..A_7 remain.

Result (msolve): with the two torus gauges A_0 = A_7 = 1 the core is
zero-dimensional of degree 35 (mod p), 5 orbits under the residual 7th-root
symmetry, and it has a REAL solution, refined here to 50 digits:

    A1..A6 = 6.1298098450469486093, 10.428028694953402845,
             14.443610252206055511, 11.622126922383210434,
             8.0612642217651886963, 3.1688557269090078589

with B_10 = 0.2391437768... != 0, i.e. all four vertex non-degeneracies of
the two bottom faces hold.  Residual of 2 f2 g3' - 3 f2' g3 - t^2 at that
point: 5e-55.

So the bottom face alone does NOT kill subcase 2 -- but it reduces its
face data from 19 free coefficients to 35 points.
