# The essential face -- what I had been filtering out

## My error

The multi-face scan (MULTIFACE.md) selected faces with the test

    if w(target) >= w(top):  skip

keeping only faces where the bracket's top component VANISHES. But the
richest faces are exactly those where it EQUALS the target -- and those
were being discarded by that very filter. The subcase-1 agent found one of
them before it stopped; I had missed it entirely.

## The essential face, and it is SHARED

Re-scanning for w(top) == w(target):

  BOTH subcases have exactly one EDGE/EDGE essential face, direction
  (2,-1), weight w = 2i - j:

      P-face: (1,0) - (8,14)     lattice length 7
      Q-face: (2,1) - (12,21)    lattice length 10
      w(top) = 2 + 3 + w(-1,-1) = 4 = w(x^2)

  (The other equality directions have a single-point face on one side, so
  they give monomial conditions rather than a functional equation.)

Both subcases share this face identically. So one instrument covers the
WHOLE of the last open case below degree 125.

## The equation (identity verified independently)

Writing face(P) = x f(u), face(Q) = x^2 y g(u) with u = x y^2:

    [ x f(u), x^2 y g(u) ] = x^2 ( f g + 2u f g' - 3u f' g )

verified at (deg f, deg g) = (1,1), (2,3), (3,4), (7,10). Since the top
component must EQUAL x^2 rather than vanish:

    W(u) := f g + 2u f g' - 3u f' g  ==  1,    deg f = 7,  deg g = 10.

Coefficientwise W_N = sum_{i+j=N} (1 + 2j - 3i) a_i b_j = [N=0]. The top
coefficient carries the factor 1 + 2n - 3m = 1 + 20 - 21 = 0, so it
vanishes identically -- an internal consistency check that this face is
admissible at these degrees.

After the two scaling symmetries the system is 17 unknowns / 17 equations
-- far smaller than the 55-unknown face-parameterised system or the
71-unknown raw one, both of which DIED ON MEMORY (msolve exceeded 4 GB and
7 GB respectively, producing no output). The small system solved.

## Result

  validation ladder (m,n) = (2k+1, 3k+1), k = 0,1,2  ->  all NONEMPTY,
      so the instrument finds solutions where they exist.
  the real case (m,n) = (7,10), characteristic zero  ->  NONEMPTY,
      solution set zero-dimensional.

## What it means, precisely

A NECESSARY condition for a counterexample of either subcase is SATISFIED.
This neither finds nor excludes a counterexample:

  * not a counterexample -- the face equation constrains only the
    top-weight part of [P,Q]; the full bracket imposes many further
    conditions at lower weights, untested here;
  * but it closes off one cheap way both subcases could have died, and it
    is CONSTRUCTIVE: the solutions are the explicit leading face data
    (f, g) that any counterexample of this shape must have, fixing 19
    coefficients of P and Q and shrinking the next stage.

## Lesson carried forward

The two large formulations died on memory; the 17-unknown one solved in
minutes. Reduce the system by structure BEFORE handing it to a solver --
that is what worked, and it is the approach to keep using.

## The face equation is an ODE in a single quantity (verified)

Setting h = g^2 / f^3, one has h'/h = 2g'/g - 3f'/f, hence

    W  =  f g + 2u f g' - 3u f' g  =  f g * (u h)' / h        [VERIFIED True]

so the essential-face condition W = 1 is equivalent to the first-order
relation

    (u h)'  =  h / (f g),        h = g^2 / f^3.               [VERIFIED True]

(An earlier version of this with h = u f^-3 g^2 was WRONG -- the identity
check returned False and the extra factor of u was the error. The corrected
form above checks True.)

READING. The face data is governed by ONE scalar quantity h = g^2/f^3
rather than by two independent polynomials. That is a rigidity statement,
and it explains two things observed computationally:

  * why the solution set is FINITE (35 points) rather than a family;
  * why the coordinates sit in a degree-35 extension and are essentially
    never individually rational at a small prime -- the 35 solutions are
    Galois-conjugate points of one rigid configuration, not independent
    choices.

This is the cleanest description of the leading data any counterexample of
either open (72,108) subcase must have.
