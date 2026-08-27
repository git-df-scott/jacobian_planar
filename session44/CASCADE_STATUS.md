# Status of the constructive route (end of this working stretch)

## What is established, and verified

1. ESSENTIAL FACE. Both open (72,108) subcases share one edge/edge face
   where the bracket's top component EQUALS the target rather than
   vanishing: direction (2,-1), deg f = 7, deg g = 10. Identity

       [ x f(u), x^2 y g(u) ] = x^2 ( f g + 2u f g' - 3u f' g ),  u = x y^2

   verified at (1,1), (2,3), (3,4), (7,10). Consistency check passes
   (top coefficient factor 1 + 2n - 3m = 0). Found by the subcase-1 agent;
   I had missed it because my face scan filtered out exactly the faces
   where the top component does not vanish.

2. FACE EQUATION SOLVED. W(u) = 1 reduces by triangular elimination to 6
   equations of degree 9 in 6 unknowns. msolve: NONEMPTY in characteristic
   zero, zero-dimensional, DEGREE 35. Cross-validated by the agent's
   independent run at prime 2147483647 (108-element basis, not (1)).

3. CASCADE STRUCTURE. Grading the 92 bracket equations by w = j - 2i:

       w=-4 : 17 eqs, 19 unknowns   the essential face (solved)
       w=-3 : 18 eqs, 19 new        LINEAR given deeper levels
       w=-2 : 19 eqs, 21 new        LINEAR
       w=-1 : 19 eqs, 13 new        LINEAR, overdetermined
       w= 0 : 19 eqs, 0  new        pure consistency

   Verified computationally: every level is degree 1 in its new unknowns.
   So with the face fixed the whole remaining problem is linear algebra.
   The cascade runs; on a test point it clears w=-3 (rank 18, 1 free) and
   w=-2 (rank 19, 2 free) and fails at w=-1, exactly where the counts say
   it should.

4. THE PARAMETER BUDGET, which is the honest headline:

       free parameters after the face : 1 + 2 + 13 = 16
       conditions at w=-1 and w=0     : 19 + 19 = 38

   Overdetermined by 22. That is a strong structural indication that face
   solutions do NOT extend -- i.e. that the subcase is empty -- though it
   is not a proof.

## The obstacle now blocking a verdict

Running the cascade on a GENUINE face solution requires an explicit one.
The 35 solutions are Galois-conjugate in a degree-35 extension:

  * msolve's RUR could not be parsed reliably -- no denominator/sign
    combination reproduced a solution that satisfied W(u) = 1, and I would
    not use an unverified parse;
  * iterated elimination is unambiguous but shows that at every prime
    tried (32003, 7919, 15013, 50021, 3001) fixing a rational root of the
    eliminant makes the remaining system EMPTY over that field. The other
    coordinates simply are not rational there.

So the face solutions are not available as tuples in a small prime field.

## The correct next step

Do the cascade over the quotient ring rather than at a point: perform the
linear algebra over K = GF(p)[T]/(eliminant), or equivalently keep the face
coefficients symbolic and reduce modulo the face ideal at each step. The
cascade being LINEAR is what makes this feasible -- it is matrix algebra
over a degree-35 field extension, not a Groebner computation.

If the w=-1 system is inconsistent over K, the subcase is EMPTY at that
prime for ALL 35 face solutions at once, which is a real verdict rather
than a sampling result.

## Honest assessment

No counterexample. The route is sound, fully mapped, and now blocked on one
concrete implementation step. The parameter count (16 against 38) points
toward emptiness, and I would not be surprised if the correct outcome here
is that the last open case below degree 125 dies -- which would itself be
worth having, since it is the computation GGHV said needed more power.
