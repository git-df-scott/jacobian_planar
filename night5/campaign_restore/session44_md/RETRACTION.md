# RETRACTION: the edge-gap / R^2-R^3 face analysis is WRONG

Found by the falsification test I built to check it (test_a5_face.py).
The prediction it was meant to test -- a_5 = 0 at lattice point (5,10) --
is REFUTED, and the reasoning behind it is invalid.

## The error

I claimed that on the (-2,1) face of the open subcase-2 polygons the two
face forms must commute, and inferred from lattice lengths 8 and 12 with
gcd 4 that

    face(P) = R^2,  face(Q) = R^3,  deg R = 4.

The commuting step is TRUE but VACUOUS. That face lies along direction
(1,2), so every monomial on it is x^k y^(2k) = u^k with u = x y^2. Both
face forms are therefore polynomials in the SINGLE quantity u, and

    [ A(u), B(u) ] = 0   identically, for ANY coefficients

-- two functions of one variable always have zero Jacobian. So the
vanishing of the top bracket component imposes NOTHING on that face, and
in particular does not force the face forms to be powers of a common R.
The "verification" I ran earlier confirmed only that the top component
must vanish; it never checked that this was a non-trivial condition. That
is the flaw: I verified an implication whose hypothesis was empty.

## What the test showed

Imposing [faceP,faceQ] = 0 directly (22 coefficients, no assumption of any
factorisation) together with the two zeros the descent genuinely found
(a_1 = a_2 = 0), and saturating by a_5:

    mod 65521 : NONEMPTY, dimension 22
    char 0    : NONEMPTY, dimension 22

So a_5 is FREE. The predicted third forced zero does not exist.

## What is RETRACTED

* EDGE_GAP_FINDING.md -- the whole R^2 face-form analysis, the derived
  "gap" R = c0 + c3 t^3 + c4 t^4, the at-most-a-double-root conclusion,
  and the claimed structural constraint on any counterexample.
* PREDICTION_AND_SUBCASE1.md -- the a_5 = 0 prediction (now refuted) and
  its section 4 R^2/R^3 claim for subcase 1's (-1,1) face, which fails for
  the same reason (that face also lies along (1,2)).
* FACE_STRUCTURE_CENSUS.md -- the census counted 1506 faces as carrying a
  forced R^a/R^b factorisation. Any face lying along a single primitive
  direction shared by both polygons is subject to the same vacuity, so
  those counts do NOT represent real constraints. The census must be
  redone with a genuine non-vacuity test before any of it is used.
* MULTIFACE.md -- the "eliminates N unknowns" figures rest on the same
  faulty inference and are withdrawn.

## What SURVIVES, and why

The ESSENTIAL FACE result is unaffected. On direction (2,-1) the top
component does NOT vanish -- it EQUALS the target -- giving

    [ x f(u), x^2 y g(u) ] = x^2 ( f g + 2u f g' - 3u f' g ) == x^2,

an identity I verified explicitly at (deg f, deg g) = (1,1),(2,3),(3,4),
(7,10). Here face(P) = x f(u) is simply the general form of a polynomial
supported on that face; no factorisation is assumed anywhere. The
resulting condition W(u) = 1 with deg f = 7, deg g = 10 is a genuine,
non-vacuous necessary condition, and its verdict stands:

    validation ladder (2k+1,3k+1), k=0,1,2 : NONEMPTY
    the real case (7,10), characteristic 0 : NONEMPTY, zero-dimensional

Both open subcases share that face, so this remains one honest instrument
covering the whole of the last open case below degree 125.

## Lesson

A "verified" chain is only as good as the non-triviality of each step. I
checked that the top bracket component must vanish and never asked whether
its vanishing said anything. The falsification test caught it -- which is
why it was built, and why predictions should be made falsifiable and then
actually tested rather than accumulated.
