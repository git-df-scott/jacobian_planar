# Subcase 1 of GGHV Prop 4.3: the essential face is SOLVABLE, and rigid

Target (GGHV arXiv:2204.14178, Prop 4.3 case (1), verified verbatim against
`session44/refs_gghv2204_extract.txt` line 657):

    N(P) = {(0,0),(1,0),(8,14),(8,16),(0,8)}
    N(Q) = {(0,0),(2,1),(12,21),(12,24),(0,12)}     [P,Q] = x^2

## 1. The face the census missed

`FACE_STRUCTURE_CENSUS.md` records only faces on which the top bracket
component must VANISH (so face(P) = R^a, face(Q) = R^b).  For every shape
there is also at least one direction on which the top component must EQUAL
the target, and that face carries far more information because its equation
is inhomogeneous.  Enumerating all directions (`case1_face_derive.py`):

    dir      wP  wQ  wtop  w(x^2)   verdict
    (0,-1)    0   0     1     0     commute
    (1,0)     8  12    19     2     commute
    (-1,1)    8  12    20    -2     commute
    (-1,0)    0   0     1    -2     commute
    (2,-1)    2   3     4      4    MUST EQUAL THE TARGET   <=== essential

(the directions (1,-2),(1,-1),(3,-4) also "equal the target" but their faces
are single vertices and give only the corner relation a_{(1,0)} b_{(2,1)} = 1,
which is the n = 0 case of the equation below.)

So the ESSENTIAL face of subcase 1 is the pair of lower edges

    face(P): (1,0) -> (8,14)     8 lattice points,  primitive step (1,2)
    face(Q): (2,1) -> (12,21)   11 lattice points,  primitive step (1,2)

## 2. The essential-face equation (derived, then re-derived symbolically)

With u = x y^2,

    face(P) = x  f(u),   deg f = 7,   f = sum a_i u^i
    face(Q) = x^2 y g(u), deg g = 10, g = sum b_j u^j

and for these,

    [face P, face Q] = x^2 ( f g + 2 u f g' - 3 u f' g ).

Since w(x^2) = 4 = wP + wQ - w(1,1) this MUST equal x^2 exactly:

    W(u) := f g + 2 u f g' - 3 u f' g  ==  1
    W_N   = sum_{i+j=N} (1 + 2j - 3i) a_i b_j = delta_{N,0}.

The top coefficient N = 17 vanishes identically because 1 + 2*10 - 3*7 = 0 --
the arithmetic that makes the (2,3)-structure consistent at all.
Vertex conditions: a_0, a_7, b_0, b_10 all nonzero (all four are vertices).
`case1_face_derive.py` reproduces W from the raw polygons with sympy, with
no hand input; the two agree coefficient by coefficient.

### Immediate corollaries (exact, characteristic zero)

* f and g have only SIMPLE roots, none at u = 0, and no common root:
  at a multiple root of f both f and f' vanish, forcing W = 0 there, not 1.
  So the essential face form is NEVER a power of a linear form.
  (This is the exact opposite of the situation on the "commuting" faces,
  where R^2/R^3 structure with high multiplicities is what the campaign
  was hoping to exploit.)
* Symmetries: (a,b) -> (lam a, lam^{-1} b) and u -> t u.  Normalising
  a_0 = 1, a_7 = 1 (and then b_0 = 1 follows) leaves
  16 equations in the 16 unknowns a_1..a_6, b_1..b_10.
* Triangularity: W_N contains (1+2N) b_N, so b_1..b_10 are polynomials in
  a_1..a_6 and W_11..W_16 become 6 equations of degree 9 in a_1..a_6.

## 3. Verdict: the essential face is NOT empty.  It has exactly 35 solutions.

Five independent instruments, three of them completely different in kind:

    instrument                              k=0  k=1  k=2  k=3(=subcase 1)
    Singular std(), char 0                    1    3   10   (running)
    Singular std(), char 32003                1    3   10   35
    msolve, p = 2^30+3                        1    3   10   35
    msolve, p = 999999937                     -    -    -   35
    sympy solve() (exact, char 0)             1    3    -    -
    Frobenius / Murnaghan-Nakayama (char 0)   1    3   10   35

k is the rung of the ladder (m,n) = (2k+1, 3k+1) -- the same equation for the
essential face of the analogous smaller shape.  k = 3 IS subcase 1.  The
lower rungs are the validation: k=0 is solvable by hand (3 b_1 = 2), and all
instruments agree on every rung before being trusted on k=3.

### The combinatorial instrument

W == 1 makes psi := f^3/(u g^2) a degree-21 rational map of P^1 with
psi' = -f^2/(u^2 g^3), whose ramification is forced to be exactly

    over 0        [3^7]          (the 7 simple roots of f, tripled)
    over infinity [2^10, 1]      (the 10 roots of g, doubled; and u = 0)
    over psi(inf) [17, 1,1,1,1]

(Riemann-Hurwitz: 14 + 10 + 16 = 40 = 2*21 - 2, exactly saturated, so there
are no other critical points -- which is what forces W to be a constant).
The correspondence is an equivalence, so the face system is solvable iff a
genus-0 cover with that data exists.  Frobenius counts them:

    #triples in S_21 with product 1 = 255454710858547200000 = 5 * 21!

so there are exactly 5 such covers, all with trivial automorphism group,
and any such triple is automatically transitive (the complement of the
17-cycle's support has size 4, and 4 is not a union of 3-cycles, nor is
3 compatible with sigma_2 restricting to a transposition there).
5 covers * 7 (the mu_7 ambiguity in normalising a_7 = 1) = 35 solutions.

The counter was validated against brute-force enumeration in S_3..S_6 on ten
classes including three that return 0, so it detects nonexistence correctly.

### The arithmetic of the 35 solutions

msolve's eliminating polynomial for the reduced 6-variable system is, at
every prime tried, a polynomial in T^7 with quintic shape

    T^35 + c4 T^28 + c3 T^21 + c2 T^14 + c1 T^7 + c0

-- the mu_7 orbit structure made visible.  The quintic in s = T^7 is
irreducible mod p = 2^30+3 and factors 2+3 mod 999999937, so the FIVE COVERS
FORM A SINGLE GALOIS ORBIT over Q: they are defined over one quintic number
field, none of them is rational.

Cover counts along the ladder: k = 0,1,2,3 -> 1, 1, 2, 5.

## 4. What this settles and what it does not

SETTLED (and this is a negative result for the emptiness programme):

    The face analysis CANNOT empty subcase 1.  Every face of subcase 1 --
    the four commuting ones and the essential one -- is satisfiable, and the
    essential one is satisfiable in exactly 5 ways.  In particular the
    "root of multiplicity >= 3 kills a vertex coefficient" mechanism that
    was hoped to close it is unavailable on the essential face: there the
    roots are provably all simple.

SETTLED (and this is a strong positive constraint):

    In any subcase-1 counterexample the 8 coefficients of P on (1,0)-(8,14)
    and the 11 coefficients of Q on (2,1)-(12,21) -- 19 coefficients, out of
    P's 61 and Q's 125 -- are not free at all.  They are one of 5 explicit
    Galois-conjugate points, up to the 2-dimensional torus
    (a,b) -> (lam t^i a_i, lam^{-1} t^j b_j).  The other faces then pin
    P|_{i=8} = alpha x^8 y^14 (y-lam)^2, Q|_{i=12} = beta x^12 y^21 (y-lam)^3
    with lam != 0, and the (-1,1) faces to A R^2 and B R^3 with deg R = 4.

NOT SETTLED: whether subcase 1 is empty.  It survives every face condition.
Deciding it needs the sub-leading levels of the (2,-1)-weight cascade

    sum_{w1+w2 = W+1} [P_w1, Q_w2] = 0      (W = 3, 2, 1, ... , -21)

whose level-W new unknowns are P_{W-2} and Q_{W-1} and which enter linearly.
Level 3 has 18 equations in 19 unknowns and a guaranteed 1-dimensional
solution space (the Hamiltonian direction H = x y^2, which sends F to
-2xy f and G to -3 x^2 y^2 g, both supported exactly on the right slices),
so no obstruction appears there; the free parameters accumulate downward and
the obstruction, if any, is at the bottom where the vertices (0,8), (0,12)
must stay nonzero.

CAVEAT, always: none of this produces a counterexample.  A candidate is not a
counterexample until it is lifted to honest polynomials in the original
coordinates with no denominators and the Jacobian verified to be a nonzero
constant exactly.  Nothing here has been lifted; these are conditions on a
reduced normal form.

## 5. Reusable

The essential face exists for EVERY shape in the campaign's catalogue and
the census never recorded it.  `case1_face_derive.py` finds it from the
polygons alone.  For any shape whose essential face system is EMPTY the
shape dies immediately, with no descent -- that is a cheap sieve the
campaign has not run.

## Files
  case1_face_derive.py  directions, faces, and the symbolic bracket identity
  case1_ladder.py       the system and the Singular ladder
  case1_msolve.py       msolve driver (NB: msolve mis-parses "(3)*x" style
                        coefficients -- caught by a two-line sanity system;
                        always emit plain products)
  case1_reduce.py       elimination of b_1..b_n -> 6 equations, 6 unknowns
  case1_points.py       reduced system at several primes
  case1_orbits.py       mu_7 structure and the quintic's factorisation
  case1_hurwitz.py      Frobenius/Murnaghan-Nakayama counter + brute-force
                        validation ("python3 case1_hurwitz.py validate")

# Part II: the (2,-1)-weight cascade below the face

## 6. The cascade, and why it is the right descent

Grading by w = 2i - j turns the whole problem into UNIVARIATE identities.
For u = x y^2 and slices written x^a y^b phi(u),

    [x^a y^b phi, x^c y^d psi] = x^{a+c-1} y^{b+d-1}
        [ (ad-bc) phi psi + (2a-b) u phi psi' - (2c-d) u phi' psi ]

(`case1_cascade.py verify`: checked on 54 explicit cases).  The slices of
N(P) are w = 2..-8 with 8,8,9,8,7,6,5,4,3,2,1 coefficients (61 in all,
matching the campaign's own parameter count for this shape) and those of
N(Q) are w = 3..-12 with 125 coefficients.  Level W of

    sum_{w1+w2 = W+1} [P_w1, Q_w2] = delta_{W,4} x^2

has exactly TWO new unknown slices, P_{W-2} and Q_{W-1}, and they enter
LINEARLY through L_W(p,q) = [face P, q] + [p, face Q].  Everything else at
that level is a product of slices already settled.  So the whole system is a
linear cascade over a growing parameter space -- unlike the y-adic descent,
whose unknowns are not organised by the face at all.

Ranks of L_W at an explicit face point (`case1_ranks.py`):

    W       3   2   1   0  -1  -2  -3  -4  -5  -6  -7  -8 .. -11  -12..-21
    ker     2   3   3   1   0   0   0   0   0   0   0     0          0
    coker   1   1   2   2   4   5   6   7   8   9  10    10          10..1

Total: 9 free parameters against 150 cokernel rows.  Running the cascade
symbolically in those parameters (`case1_descend.py`) all the way to W = -21
takes about a minute and produces 124 genuine conditions of degree up to 24
in the 9 parameters.  The first three levels (W = 3,2,1) impose NOTHING --
their cokernel rows are automatically satisfied -- and conditions start at
W = 0 with a binary quartic in two of the parameters only.

## 7. The point that must not be forgotten: the trivial solution

The all-parameters-zero point ALWAYS solves the cascade, because it gives

    P = face(P) = x f(u),    Q = face(Q) = x^2 y g(u),   [P,Q] = x^2

exactly.  That is a real solution of the bracket equation, but its Newton
polygon is the single essential edge, not the pentagon.  So the cascade
ideal is NEVER the unit ideal and "the ideal is proper" proves nothing.
The emptiness question for subcase 1 is precisely whether the cascade has a
solution with the FOUR remaining vertices present:

    P at (0,8)  = slice P_{-8}          P at (8,16)  = slice P_0, i = 8
    Q at (0,12) = slice Q_{-12}         Q at (12,24) = slice Q_0, i = 12

all nonzero (the other four vertices lie on the essential face and are
nonzero there already).  `case1_nondeg.py` adjoins the Rabinowitsch
inverse of their product and reruns the decision.

## 8. Verdict of the cascade: EMPTY modulo p

Instrument validation, run before the verdict was trusted:

  POSITIVE CONTROL (`case1_validate.py`): the all-parameters-zero point of
  the cascade was substituted back into the slices, P and Q reassembled as
  honest polynomials over F_p, and the bracket computed DIRECTLY by
  polynomial multiplication.  Result: 8 monomials in P and 11 in Q, all
  inside the polygons, and P_x Q_y - P_y Q_x = x^2 exactly.  The slice
  bookkeeping, base points, bracket formula, level ranges and linear solves
  are therefore all correct end to end.

  NEGATIVE CONTROL: with the vertex non-degeneracy conditions REMOVED, the
  same decision engine reports a live component (dimension 2) rather than
  EMPTY -- the instrument does not answer EMPTY unconditionally.

  ENVIRONMENT CHECK (`case1_envcheck.py`): the campaign's own Singular
  pipeline, re-run in this container on trackD_targets_validate.json,
  reproduces the EMPTY verdict the independent run reported.

  FACE REDUCTION: the essential-face variety still has vdim 35 modulo each
  prime used, so no face solutions are lost or gained by the reduction.

  SYMMETRY: it suffices to test ONE point per cover.  The mu_7 ambiguity
  (u -> t u, a_i -> t^i a_i, b_j -> t^j b_j) is induced by the genuine
  symmetry (x,y) -> (tx, y) followed by P -> t^{-1}P, Q -> t^{-2}Q, which
  preserves the Newton polygons and the equation [P,Q] = x^2.  Likewise
  (P,Q) -> (lam P, lam^{-1} Q).  So the 35 face points form 5 orbits and a
  representative of each is enough.

Result, for each of the FIVE covers, at primes where all five are
F_p-rational (5189, 5441, 7523 -- chosen with 7 not dividing p-1 so the
7th root is unique):

    the cascade conditions down to level W = -11 (88 of the 124), together
    with the four vertex conditions
        P(0,8) != 0, P(8,16) != 0, Q(0,12) != 0, Q(12,24) != 0
    generate the UNIT IDEAL.

    ==> over the algebraic closure of F_p there is NO pair (P,Q) with
        support in N(P), N(Q), all vertices present, and [P,Q] = x^2.

Only a subset of the conditions is used, which is the safe direction: fewer
conditions means a larger variety, so emptiness of the subsystem implies
emptiness of the full system.

## 9. What this is, stated exactly

THIS IS A MODULAR RESULT.  It says subcase 1 has no realisation in
characteristic p, for the primes tested.  It is NOT a characteristic-zero
proof.  A characteristic-zero solution would reduce to a solution modulo
almost every prime, so the modular emptiness at several independently chosen
primes is strong evidence that subcase 1 is empty over C -- but a specific
prime can be a bad prime, and no bound on bad primes has been computed here.
Turning this into a theorem needs the same cascade run over the quintic
number field of the five covers (or over Q with the face left as an ideal),
which is a heavier but entirely mechanical computation.

AND, INDEPENDENTLY OF ALL OF THAT: even a non-degenerate (P,Q) here would
NOT be a counterexample to the Jacobian Conjecture.  GGHV Prop 4.3 is a
one-way implication: a counterexample in case (8,28) forces such a (P,Q) to
exist.  Producing one does not run the implication backwards.  And nothing
in this work has been lifted to honest polynomials in the original
coordinates with the Jacobian verified to be a nonzero constant -- the
standard caveat applies in full.

## Files (part II)
  case1_cascade.py   slices, the bracket formula and its verification,
                     level-by-level bookkeeping
  case1_ranks.py     ranks / kernels / cokernels of L_W
  case1_point.py     an explicit F_p point of the face variety, verified
  case1_descend.py   the symbolic cascade in the free parameters
  case1_nondeg.py    cascade + the four vertex non-degeneracy conditions
  case1_verdict.py   all five covers at one prime
  case1_validate.py  positive and negative controls
  case1_envcheck.py  the campaign pipeline on the known-EMPTY target
