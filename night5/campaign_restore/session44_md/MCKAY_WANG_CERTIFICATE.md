# The McKay-Wang certificate (JPAA 40 (1986) 245-257)

Source: J.H. McKay & S.S.-S. Wang, "An inversion formula for two
polynomials in two variables", J. Pure Appl. Algebra 40 (1986) 245-257.
New to this campaign -- no prior session used inversion formulas.

## What it gives us

**Corollary 14.** If f, g define an isomorphism of K[x,y], then N(f) is the
triangle with vertices (0,0), (k,0), (0,n) where k = deg f(x,0),
n = deg f(0,y); similarly N(g).

Contrapositive, which is the useful direction:

    det J(f,g) = const != 0   AND   N(f) is not that triangle
        ==>  (f,g) is not an automorphism
        ==>  (f,g) IS a counterexample to the Jacobian Conjecture.

This replaces the campaign's previous endgame requirement ("exhibit an
actual collision of two distinct points") with a published theorem. Finding
a Keller pair on any of our prescribed non-triangular shapes is, by itself,
finding a counterexample.

**Section 4 iteration** (a second, independent certificate). From border
polynomials alone,
    f_{i+1} = (-1)^(n_i+1)/(J_i c_i) Res_t(f_i(0,t) - x, g_i(0,t) - y)
    g_{i+1} = (-1)^(k_i)/(J_i d_i)   Res_t(f_i(t,0) - x, g_i(t,0) - y)
and S_i an automorphism ==> S_i = S_{i+2}. So S_0 != S_2 proves
non-automorphism. Cheap even in degree 108, since only border polynomials
enter. (Example 20 of the paper shows the converses fail, so this is a
one-way test -- used only in the direction stated.)

**Corollary 15**: deg(phi) = deg(phi^-1) for an isomorphism -- an extra
consistency check on any candidate.

## Validation (mckay_wang.py, both controls PASS)

- Control A: the tame automorphism f = x + y^2, g = y is Keller with
  triangular polygons -> correctly NOT certified as a counterexample.
- Control B: Mondello's characteristic-2 counterexample (arXiv:2608.02634),
  P = x + x^2y + x^4 + x^6y^2, Q = y + x^5 + x^6y + x^7y^2 + x^8y^3, is
  correctly detected as non-automorphism: N(P) has (6,2) and (2,1) outside
  its triangle (k=4, n=0), N(Q) has (8,3),(7,2),(6,1) outside (k=5, n=1).
  A known counterexample is detected, so the instrument has teeth.

## Applied to the open (72,108) case

GGHV Prop 4.3's proof gives original-coordinate corners
{(0,0),(1,0),(8,28),(0,4)} multiplied by (m,n) = (3,2):

    P: (0,0), (3,0), (24,84), (0,12)   -> k=3, n=12; (24,84) is outside
                                          the triangle -> NOT triangular
    Q: (0,0), (2,0), (16,56), (0,8)    -> k=2, n=8;  (16,56) is outside
                                          -> NOT triangular

So the target shape is certified non-automorphism-shaped. Consequence for
the endgame: if the branching descent (walk_branch.py) returns a CANDIDATE
on either subcase and it survives exact verification that det J is a
non-zero constant, then Corollary 14 makes it a counterexample outright.

Caveat kept explicit: Prop 4.3's polygons are stated in the reduced Laurent
coordinates L^(1), while Corollary 14 is a statement about honest
polynomials in K[x,y]. The check above is therefore run on the
ORIGINAL-coordinate corners, which is where the certificate applies. Any
candidate must still be lifted back to original coordinates and its
Jacobian verified exactly there before the certificate is invoked.
