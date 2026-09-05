# Sol 5: collision-first Hamiltonian incidence

Date: 2026-08-25. Branch: `codex/sol5-collision-first`.

## Binding hit gate

A counterexample is reported only after producing explicit original
polynomials `P,Q` over a characteristic-zero field, verifying `[P,Q]=1`
coefficient by coefficient, and verifying two distinct source points with the
same image. Numerical and finite-field points are `CANDIDATE-UNVERIFIED` until
they lift and replay exactly.

## New formulation

Normalize a hypothetical collision by affine source and target changes:

    a=(0,0), b=(1,0), P(a)=P(b)=Q(a)=Q(b)=0.

For fixed `P`, the original Keller equation is linear in `Q`:

    X_P(Q) = P_x Q_y - P_y Q_x = 1.

`collision_first/incidence.py` constructs this full coefficient matrix and
adds the two `Q` collision rows. It never passes through `[P,Q]=x^2`, a Laurent
map, or a reverse-polynomiality test. Thus a hit is already in the original
polynomial coordinates.

Three independent controls pass:

1. the matrix product agrees with an independently assembled direct bracket;
2. the Keller automorphism `(x,y)` passes the Jacobian gate and fails the
   forced `P` collision gate;
3. an explicit colliding polynomial pair passes both collision gates and fails
   the Jacobian gate.

`collision_first/search.py` eliminates the four collision values identically,
fixes one driver gauge, searches all remaining coefficients over `C`, and uses
an independently finite-differenced analytic Jacobian control.

## First numerical reconnaissance

The height `(2,3)` ribbon at x-degrees `(12,18)` approached a small raw defect:

    first sweep             2.303125860650e-5
    continued LM sweep      1.611072393188e-6

Both required top/right `Q` vertices remained nonzero. However coefficient
norms grew and the tangent matrix developed several near-null singular values,
so this was classified as escape toward infinity, not a candidate.

The same parameterization at the first degree-126 edge `(84,126)` stopped at
raw norm `2.896386697533e-1` after 300 evaluations and drove the right `Q`
vertex to `1.87e-5`. The shared-factor height `(4,6)` version stopped at
`8.063297720519e-1` after 120 evaluations and drove that vertex to `9.61e-6`.
These are negative numerical screens only.

## Exact closure of every height `(2,3)` collision ribbon

The small numerical residual led to an exact obstruction. Write the complete
family, with its nonzero constant top coefficients normalized, as

    P = u(x) + v(x)y + y^2,
    Q = q0(x) + q1(x)y + q2(x)y^2 + c y^3,  c != 0.

Solving the `y^3,y^2,y^1` Jacobian rows exactly gives

    q2 = (3/2)c v + A,
    q1 = (3/2)c u + (3/8)c v^2 + A v + B,
    q0 = (3/4)cuv + Au - (1/16)c v^3 + (1/2)Bv + C.

The constant row is then

    dH/dx = 1,
    H = (3c/64)(v^2-4u)^2 - (B/4)(v^2-4u).

Hence `H=x+K`. If `w=v^2-4u` is constant, `H` is constant. If `w` has positive
degree `d`, the nonzero quadratic leading term gives `deg H=2d`. Either way
`deg H` cannot equal one. This is a characteristic-zero contradiction.

`collision_first/ribbon23_certificate.py` reconstructs the full Jacobian,
checks every upper row is identically zero under the displayed formulas, and
checks that its constant row is exactly `dH/dx`.

Therefore **every polynomial height `(2,3)` ribbon with both top vertices
present is EMPTY over characteristic zero, at every x-degree**. The proof is
stronger than the normalized collision search because it does not use the
collision equations at all.

## Exact reduction of the live height `(4,6)` frontier

The first shared-factor family does not suffer the preceding even-degree
contradiction. Write

    P = p0+p1*y+p2*y^2+p3*y^3+y^4,
    Q = q0+...+q5*y^5+c*y^6,  c != 0.

`collision_first/ribbon46_reduction.py` treats differentiation as an exact
derivation on the polynomial ring in `p0,...,p3`. Starting at the `y^8`
Jacobian row, each row through `y^3` is a closed polynomial one-form. The
script integrates those forms successively to reconstruct `q5,...,q0`, with
one integration constant per row, and independently substitutes the result
back into the complete Jacobian. All seven upper rows vanish exactly.

Only three original Jacobian rows survive:

    E2=0, E1=0, E0=1.

At the degree-126 weighted triangle, `deg p_i=84-21i` and the reconstructed
`deg q_j=126-21j`. The three identities contribute respectively 147, 168, and
189 coefficient equations, 504 total. The exact reduction therefore replaces
the numerical system of 658 complex variables and 945 bracket rows by

    212 P coefficients + 7 integration constants, 504 equations,

before imposing the two collision values. No coefficient was divided out and
no resonance was assumed nonzero. This is the first live collision-first
elimination target.

## Verdict and next lane

**No counterexample yet.** The collision-first engine is validated, and its
first apparent numerical signal converted into an exact all-degree closure.

The next live family is the reduced shared-factor height `(4,6)` frontier.
Blind optimization is not promising; its first degree-126 basin remained far
from zero and collapsed a required vertex. The next step is to export the 504
reduced equations with the two collision values, eliminate the remaining
linear constants, and search the saturated residual system over several primes
and extension fields. Smoothness is required before any Hensel-lift claim.
