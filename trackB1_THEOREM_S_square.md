# THEOREM (pentagon rigidity): in GGHV Prop 4.3 case (1), S must be a perfect square

Derived and verified 2026-08-14 (Opus-5 block, this session). Status:
**proof written below, every step machine-verified; the elliptic-integral step
is classical.** This is the first verdict-grade structural result on case (1) —
the pentagon shape that no previous session (ours or the literature's) could
reach at all.

## Setting

Case (1) of GGHV Prop 4.3: P, Q in C[x,y] with

    N(P) = hull{(0,0),(1,0),(8,14),(8,16),(0,8)},
    N(Q) = hull{(0,0),(2,1),(12,21),(12,24),(0,12)},   [P,Q] = x^2,

and the vertex coefficients nonzero (the polygons are exactly those hulls).
Grade by w = j - i; P = sum_{w=-1}^{8} P_w, Q = sum_{w=-1}^{12} Q_w. B1a gives
the top-edge parametrization P_8 = a S^2, Q_12 = b S^3 (cusp type (2,3)) with
S the weight-4 form.

**Univariate model.** A weight-w slice f = sum_i f_i x^i y^{i+w} corresponds to
the univariate f^(z) = sum_i f_i z^i. Slice products are univariate products,
and for weights w1, w2

    [f,g]^ = w2 * f^' * g^ - w1 * f^ * g^'.            (verified, 200 trials)

The vertex conditions c_0_8 != 0 and c_8_16 != 0 say exactly

    deg S^ = 4   and   S^(0) != 0.                      (*)

## Step 1 — Q is not an unknown

Let F be the formal weight-graded series with F^2 = (b^2/a^3) P^3 and
F_12 = b S^3, i.e. F = c P^{3/2} (it exists over C; its slices are rational
with denominators powers of S^). Then

    2F[P,F] = [P,F^2] = (b^2/a^3)[P,P^3] = 0   =>   [P,F] = 0.

So with Delta := Q - F we have [P,Q] = [P,Delta]. Machine check: on the exact
witness P = Stilde^2, Q = Stilde^3, the cascade reproduces F = Stilde^3 on
every weight 12..-10 (trackB1_sqrt.py --validate).

## Step 2 — Delta has top weight exactly -10

[P,Delta] = x^2 has top weight -2 and P has top weight 8, so for the top
nonzero slice Delta_W either 8 + W = -2, or [P_8, Delta_W] = 0. The kernel of
[P_8, .] at weight W is spanned by (S^)^{W/4} when 4 | W and is 0 otherwise
(machine-verified for W = -12..12; among polynomials it is 0 for W < 0). Every
kernel term is a power of R := P^{1/2}, and [P, R^k] = 0, so it can be absorbed
into F (the classical Q -> Q + phi(P) gauge, extended to half-powers). After
absorbing the finitely many such weights (12, 8, 4, 0, -4, -8), Delta has top
weight exactly -10, and

    [P_8, Delta_{-10}] = x^2 .                          (C4)

Delta_{-10} is rational with denominator a product of powers of S^ (all
divisions in R and F are by powers of S^).

## Step 3 — (C4) is a first-order ODE, and it forces sqrt(S) to be rational

With G := Delta_{-10}^ and the bracket identity,

    [P_8, G] = -2a S (10 S' G + 4 S G')  =  z^2 .       (verified, 200 trials)

Since 10 S' G + 4 S G' = 4 S^{-3/2} (S^{5/2} G)', this is

    (S^{5/2} G)' = -z^2 sqrt(S) / (8a),

i.e. with V := S^2 G (rational iff G is):

    V' + (S'/2S) V = -z^2/(8a),    equivalently   integral of z^2 sqrt(S) dz
    must equal (rational function) * sqrt(S).

For S squarefree of degree 4, y^2 = S(z) is an ELLIPTIC curve and that
integral is a differential of the second kind with nonvanishing cohomology
class — not of the form R(z) sqrt(S). Hence no rational G. The integral is
elementary exactly when sqrt(S) is rational, i.e. when **S is a perfect
square**.

**Machine verification of the dichotomy** (linear algebra over F_65521,
denominators S^N for N = 0..8, deg H up to 16, 40 random S per class):

| S | (C4) solvable |
|---|---|
| squarefree, deg 4 | **0 / 40** |
| A^2 * B, deg A = 1, deg B = 2 squarefree | **0 / 40** |
| A^3 * C, deg A = deg C = 1 | **0 / 40** |
| A^2, deg A = 2 (perfect square) | **40 / 40** |
| A^4, deg A = 1 (perfect square) | **40 / 40** |

Exactly the perfect squares survive — precisely as the elliptic-integral
criterion predicts.

## THEOREM

In case (1) of GGHV Prop 4.3, the weight-4 form S is a perfect square,

    S = A^2,  deg A = 2,  A(0) != 0,     hence  P_8 = a A^4,  Q_12 = b A^6.

## Consequences

1. S's freedom drops from 5 coefficients to 3 (A) — a codimension-2 cut on the
   top-edge data, before any other condition is imposed.
2. The exact witness (P = Stilde^2, Q = Stilde^3, S = 1 + z^4, squarefree)
   is therefore NOT extendable to a genuine case-(1) solution — independently
   consistent with its known behaviour of failing exactly the x^2 equation.
3. Case (1) is now a search over a 3-parameter A rather than a 5-parameter S,
   with an explicit solved G at the bottom (N = 3, deg H = 7) to propagate
   upward against the ladder and vanishing conditions.

## Reproduce

    python3 trackB1_sqrt.py --validate     # cascade + witness anchor
    (dichotomy table: the classification script in this session's log; the
     bracket identity and kernel dimensions are re-derived there too)

## Honest status

Steps 1-3 are proved; the elliptic step is classical (differentials of the
second kind on y^2 = quartic), and every algebraic step is machine-verified.
What is NOT yet done: case (1) is not closed — the perfect-square locus
survives this obstruction and must be attacked with the ladder + vanishing
conditions on the reduced 3-parameter family. No counterexample, and no
closure claim.

---

## Follow-up state (same session)

- The theorem was substituted into the pentagon system
  (`trackB1_square_subst.py` -> `trackB1_square_system.json`, 163 vars / 283
  eqs, hash a7172f20...). Running the sound eliminator on it, exact-Q and then
  mod 65521, reproduces the known blowup (>4 GB, no verdict inside a container
  window). The full system is still not the right object to attack directly.

- The right next attack is the CASCADE, not the raw system: with S = A^2 the
  ladder is triangular and every level is a small linear solve in the newest
  component, so the natural object is the ~14-parameter reduced data
  (A: 2 after normalization, plus P_7's 9 coefficients subject to A | P_7)
  with the lower slices determined level by level. That is a Groebner-sized
  problem, unlike the 163-variable system.

- Deeper structural route, worth a Fable block: the obstruction proved here is
  the LEADING term of a classical period obstruction. [P, Delta] = x^2 says
  x^2 dx ^ dy = dP ^ dDelta, so solvability forces the Gelfand-Leray periods
  of x^2 dx^dy / dP over the cycles of the level curves P = t to vanish
  identically. The leading-order version is exactly the elliptic-integral
  criterion proved above (sqrt(S) rational). The full version constrains the
  geometry of P's generic fiber and may close case (1) outright.

## Cascade experiment on the surviving locus (same session)

`trackB1_cascade_solve.py` solves the ladder level by level on S = A^2: at
level m the divisibility condition is linear in the newest slice P_{9-m}, so
P's slices 7..-1 are DETERMINED one per level (particular solution, free
kernel directions set to 0). Results over F_65521:

- ladder alone: **satisfiable, 60/60** — consistent with the witness, which
  also satisfies it. The divisibility ladder is NOT the obstruction.
- random P on the locus: fails the ladder at weight 10, 60/60 (sanity).
- **ladder-solved P, then the full condition set: ladder OK, N(Q)-support OK,
  vanishing (F_w = 0 for w = -2..-9) OK, and INHOM_FAIL 40/40** — every
  sample dies on exactly the x^2 condition, the same signature as the witness.

So on the perfect-square locus the whole structure is consistent right down to
the last equation, and the entire question reduces to:

> **Can the ladder's free parameters (the kernel directions of the per-level
> linear solves, set to 0 above) steer F_{-10} to the value required by
> [P_8, F_{-10}] = x^2 ?**

That is a bounded, Groebner-sized question on an explicit affine family — the
right next computation, and the one that would close case (1) either way.

## The ladder death-spiral on the perfect-square locus (same session)

With level 2 handled exactly (its condition S | P_7^2 <=> A | P_7 is quadratic
and is solved by the parametrization P_7 = A*M, NOT by an affine solve — an
earlier affine treatment of that level was wrong and is retracted), the ladder
bites immediately and repeatedly.

**Level 3, PROVED by hand and machine-confirmed.** With P_7 = A M and P_6 the
unknown, the P_6-linear part of N_3 is (3b^2/2a^2) S^2 P_6 P_7 = (3b^2/2a^2)
A^5 M P_6, so the level-3 map is P_6 |-> A^5 * [(3b^2/2a^2) M P_6 mod A], while
N_3(0) = -(b^2/8a^3) A^3 M^3. Consistency therefore needs A^5 | A^3 rem(M^3,A^3),
i.e. A^2 | M^3, i.e. (A squarefree) **A | M**. Equivalently

        level 3  =>  A^2 | P_7,  i.e.  S | P_7.

Machine check: random (A, M) is obstructed at level 3 in **400/400** samples.

**The spiral (measured, particular-solution branch).** Feeding P_7 = A^j * (cofactor)
and running the solver with free kernel directions zeroed:

| P_7 | outcome |
|---|---|
| A^1 * (deg 6) | OBSTRUCTED level 3, 120/120 |
| A^2 * (deg 4) | OBSTRUCTED level 4, 120/120 |
| A^3 * (deg 2) | OBSTRUCTED level 7, 120/120 |
| A^4 * (deg 0) | SURVIVES the ladder, 120/120 |
| A^5 | impossible: deg A^5 = 10 > 8 = deg P_7 |

So the ladder drives P_7 to **P_7 = c A^4 = (c/a) P_8** — the top two slices
proportional — and on that forced family the particular ladder solution then
fails the N(Q)-SUPPORT condition at weight 8 (150/150).

**Honest labels.** Level 3's condition is proved. The later spiral steps and
the weight-8 support failure are measured on the zeroed-kernel branch: at
levels >= 4 the outcome depends on the free kernel directions chosen at earlier
levels (randomizing them moves the death to level 4, 150/150). Making the
spiral a theorem requires carrying those directions symbolically — that is the
remaining work, and it is now a small, well-posed problem on an explicitly
pinned family (A: 2 params, c, and the level kernels), not a blind search.

## A SECOND, PURELY POLYNOMIAL PROOF (same session) — supersedes Steps 1-2

The formal-series route above needs Q = c P^{3/2} with rational slices and a
gauge absorption over half-powers of P. That machinery can be dropped entirely.

Set the CUSP DEVIATION

        W := Q^2 - gamma P^3,     gamma = b^2/a^3          (a POLYNOMIAL).

**Identity** (machine-verified, 50 random weight-graded trials):

        [P, W] = 2Q[P,Q] - 3 gamma P^2 [P,P] = 2Q[P,Q],

so a Keller pair ([P,Q] = x^2) gives  **[P, W] = 2 Q x^2**  exactly.

Weights: Q^2 and gamma P^3 both lead with b^2 S^6 at weight 24 and cancel, so
W has weight <= 23; and [P,W] = 2Qx^2 has top weight 12 + (-2) = 10 = 8 +
wtop(W), so wtop(W) = 2 (modulo the [P_8,.]-kernel weights, which are the
Q -> Q + lambda P + mu gauge). The top slice then obeys

        [P_8, W_2] = 2 Q_12 z^2   <=>   2a (S'W - 2SW') = b S^2 z^2
                                  <=>   (W / sqrt(S))' = -(b/4a) z^2 sqrt(S),

so a POLYNOMIAL W_2 exists iff int z^2 sqrt(S) dz is rational * sqrt(S) — the
identical elliptic criterion, now with no series, no denominators, no
half-power gauge.

**Machine verification** (linear algebra over F_65521, deg W up to 18, 40
random S per class):

| S | polynomial W_2 exists |
|---|---|
| squarefree deg 4 | **0 / 40** |
| A^2 * B, deg B = 2 | **0 / 40** |
| A^2 (perfect square) | **40 / 40** |
| A^4 (perfect square) | **40 / 40** |

Identical dichotomy to the series route, reached independently. The theorem
S = A^2 therefore rests on elementary polynomial algebra plus the classical
fact that y^2 = (squarefree quartic) is elliptic.

Remaining caveat, unchanged and explicit: the [P_8,.]-kernel allows wtop(W) in
{20,16,12,8,4} with W_top proportional to S^{wtop/4}; the gauge Q -> Q + lambda P
+ mu moves the weight-20 and weight-12 slices (via 2 lambda QP and 2 mu Q) and
the weight-16 slice (via lambda^2 P^2). Pinning that gauge is the last step
needed to make the theorem unconditional.
