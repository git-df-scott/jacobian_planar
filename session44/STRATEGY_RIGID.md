# The rigid-catalog strategy (Session 44, night synthesis)

Everything the night established, composed:

1. Full-depth measurement: every chart of every published shape <= 150 has
   dim <= 1 at full bracket depth, and the 1 is the scaling gauge. The
   <=150 landscape is a FINITE LIST OF RIGID SYSTEMS - nothing or finitely
   many points each. (Re-rank in progress: 20/77 so far, all dim_full=1.)
2. Two-prime EMPTY logic re-checked for the rigid case: verdicts are
   geometric (GB=<1> over F_p kills F_p-bar points; a char-0 point reduces
   to F_p-bar for all but finitely many p). Sound. Residual risk unchanged
   (finite bad-prime set), recorded.
3. THE INSTRUMENT the results point at: at full depth the walker's affine
   tower is deterministic given the gauge t = p10 (kernel total ~ 1).
   Excess conditions = polynomials in t alone. Port the walker to
   K = F_p(t) using the u0_exact flint nmod_poly machinery (built and
   validated this session):
     - walk with t symbolic; collect excess-condition numerators in t;
     - gcd has no roots  -> chart EMPTY at p over ALL gauges (exhaustive,
       no sampling, no Groebner, polynomial cost);
     - roots -> finitely many candidate gauges -> walk each
       deterministically -> explicit point -> independent bracket gate.
   Two primes; gate-passing survivors go to exact char-0 lift.
   This DECIDES each rigid chart mod p - including every current timeout,
   the (72,108) subcases (params 25/61), and the 125..150 tier.
4. Mechanism view: the known CE mechanisms (dim-3 factorization
   multivaluedness; Mondello's hidden cubic) share the skeleton "P,Q are
   approximate powers of a common C; multivaluedness = factorization".
   GGHV's reduction of the one open case is literally P = C^2,
   Q = C^3 + lambda C^-1 + F. The last open case wears the known
   mechanism's shape. Rigid + C^2/C^3 + symbolic-gauge walker is the
   aimed shot.

Build order: walk_t.py (walker x u0_exact synthesis) -> (72,108) pair ->
rigid catalog sweep -> 125..150 tier. Groebner lanes keep running as the
independent second route.
