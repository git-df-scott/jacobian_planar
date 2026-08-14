# THEOREM (pentagon rigidity): in GGHV Prop 4.3 case (1), S is NOT squarefree
# — and lies on one of exactly TWO components

> ## !! RETRACTION AND CORRECTION (2026-08-14, later same session) !!
>
> **The headline claim below — "S must be a perfect square" — is FALSE.**
> It was inferred from 40-random-sample tables per stratum. The solvable locus
> has a SECOND component of codimension 1 *inside* the `A^2*B` stratum, which
> random sampling in that stratum cannot see. The corrected statement, proved
> exactly (no sampling), is in the section **"THE EXACT TWO-COMPONENT
> CLASSIFICATION"** at the bottom of this file; read that section, not the
> headline. What survives unchanged:
>
> - **strengthened to an exact proof:** no squarefree S is admissible (this was
>   the sampled `0/40` row; it is now a finite exact computation);
> - **the consequence that actually mattered:** S's freedom still drops from 5
>   parameters to 3, because *both* components are 3-dimensional;
> - every algebraic identity, the cascade, and the ladder results.
>
> What changes: there is a second, never-searched 3-parameter family of S, and
> it had to be searched. It has been (see "FIRST SEARCH OF COMPONENT II").

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

---

# THE EXACT TWO-COMPONENT CLASSIFICATION (2026-08-14, supersedes the headline)

Everything above reduces case (1) to ONE criterion on the weight-4 form S
(deg S^ = 4, S^(0) != 0), reached independently by both proofs:

    (C4)  exists RATIONAL G with [P_8, G] = z^2,   P_8^ = a S^2
          <=>  exists POLYNOMIAL W_2 with 2a(S'W - 2SW') = b S^2 z^2
          <=>  int z^2 sqrt(S) dz  in  C(z)*sqrt(S).

Setting R := S^2 G, all three read

    (STAR)      2 S R' + S' R = 2 z^2 S ,     R rational.

(The two criteria are EQUIVALENT, not merely parallel: writing S = S1 S2^2 with
S1 squarefree and U := R S2, one has R S = U S1 S2, and U is always a
polynomial — see below. So R rational forces W = -(b/4a) R S polynomial.)

## Why the published tables were wrong

(STAR) is 7 linear equations in the 4 coefficients of R, so its solvable locus
is cut out by at most 3 conditions on the 5 coefficients of S. Sampling 40
random S per *stratum* cannot see a positive-codimension sublocus **of that
stratum**. That is exactly what was missed: the `A^2*B` row read 0/40 because
the solvable members of that stratum form a hypersurface inside it.

## The reduction that makes it finite

Write S = S1 * S2^2 with S1 SQUAREFREE (the squarefree part), and set
U := R * S2. Then (STAR) becomes

    (STAR')     2 S1 U' + S1' U = 2 z^2 S1 S2 .

**U is always a polynomial.** A pole of U of order m at a root of S1 of
multiplicity k = 1 forces (leading-order balance) k = 2m or k >= m+1, both
impossible; and U has no poles off V(S1). Since deg S1 + 2 deg S2 = 4, only
deg S2 in {0,1,2} occur, giving exactly three cases.

### deg S2 = 0 — S squarefree: **NO SOLUTIONS** (exact, not sampled)

U = R is a polynomial of degree 3 (leading coefficients force r3 = 1/5). Four
of the seven equations solve triangularly,

    r3 = 1/5,   r2 = s3/(40 s4),   r1 = (16 s2 s4 - 7 s3^2)/(240 s4^2),
    r0 = (144 s1 s4^2 - 116 s2 s3 s4 + 35 s3^3)/(960 s4^3),

and the remaining three are conditions on S:

    -768 s0 s4^3 + 552 s1 s3 s4^2 + 256 s2^2 s4^2 - 460 s2 s3^2 s4 + 105 s3^4 = 0
    48 s0 s3 s4^2 + 240 s1 s2 s4^2 - 42 s1 s3^2 s4 - 116 s2^2 s3 s4 + 35 s2 s3^3 = 0
    128 s0 s2 s4^2 - 56 s0 s3^2 s4 + 144 s1^2 s4^2 - 116 s1 s2 s3 s4 + 35 s1 s3^3 = 0

Symmetries: S -> u S (R fixed) and S(z) -> S(tz), R -> t^-3 R(tz). Normalize
s4 = 1 and s3 in {1, 0}. The Groebner basis eliminates to a degree-5 factored
form; solving gives **exactly five solutions**, and EVERY ONE has discriminant
zero:

| S (up to the two symmetries) | type |
|---|---|
| (4z+1)^4 / 256 | perfect 4th power |
| (8z^2+4z+3)^2 / 64 | perfect square |
| (8z+7)^2 (128z^2-96z+63) / 8192 | A^2 B — **not** a perfect square |
| two conjugates over Q(sqrt(-3)), disc = 0 | non-squarefree |

and the s3 = 0 stratum forces s0 = 0, excluded by the vertex condition.
Hence: **no squarefree S satisfies (C4)** — the sampled 0/40 row is now a
theorem. Row 3 is the first sign that the perfect-square claim is false.

Consistency with the classical picture: for squarefree S the curve y^2 = S is
ELLIPTIC, and z^2 S dz/y has poles only at the two points at infinity — one
residue condition plus the 2-dimensional de Rham obstruction = **3 conditions**,
matching the three equations above exactly.

### deg S2 = 1 — S = c A^2 B, A linear, B = z^2 + u z + v squarefree

Here U |-> 2 S1 U' + S1' U is injective on polynomials of degree <= 4 with
5-dimensional image inside the 6-dimensional space of degree <= 5, so
solvability is exactly ONE linear condition on A given B. Computing it:

    (u^2 - 4v) * ( -10 a0 u^2 + 8 a0 v + 7 a1 u^3 - 12 a1 u v ) = 0

for A = a1 z + a0. The first factor is disc(B) — that is the degeneration
back to a perfect square. The second gives

> ### COMPONENT II (new)
>
>     S = c * A^2 * B,   B = z^2 + u z + v,
>     A = 2(5u^2 - 4v) z + u(7u^2 - 12v)
>
> with u != 0, v != 0, u^2 != 4v, 5u^2 != 4v, 7u^2 != 12v.
> Three parameters (c, u, v); one modulo both symmetries.

Consistency with the classical picture: y^2 = B is a RATIONAL curve, so the
de Rham obstruction vanishes and only the residue-at-infinity condition
survives — **1 condition**, matching. Row 3 of the squarefree table is exactly
the member of component II on which A divides U (making R polynomial).

### deg S2 = 2 — S = c A^2 perfect square: ALWAYS solvable

S1 is a constant, so (STAR') is 2 S1 U' = 2 z^2 S1 A, i.e. U = int z^2 A dz.

> ### COMPONENT I (old headline)
>
>     S = c * A^2,  deg A = 2.        Three parameters.

## CORRECTED THEOREM

In case (1) of GGHV Prop 4.3, the weight-4 form S satisfies

    S = c A^2   (component I)      or     S = c A^2 B with A = 2(5u^2-4v)z
                                          + u(7u^2-12v), B = z^2+uz+v
                                          (component II),

and in particular **S always has a repeated root**; no squarefree S occurs.
Both components are 3-dimensional, so the operative consequence is unchanged:
**S's freedom drops from 5 parameters to 3**, i.e. codimension 2 on the
top-edge data before any other condition is imposed.

## Verification (three independent checks, none reusing the derivation)

`trackB1_component2_verify.py`:

| check | result |
|---|---|
| CHECK 1: raw bracket `[P_8, G]` via `slice_bracket()` from trackB1_sqrt.py, exact Q | 15/15 give exactly `-8 z^2` |
| CHECK 2: polynomial `W` with `2a(S'W-2SW') = b S^2 z^2` | 15/15, W polynomial, ratio `-2` |
| CHECK 3: brute-force mod-65521 linear solve for `G = H/S^N` (no derivation used) | component II 25/25 solvable; random squarefree 0/25; random `A^2 B` off-component 0/25; random perfect squares 25/25 |

Reproduce:

    python3 trackB1_elliptic_locus.py       # the three squarefree conditions
    python3 trackB1_elliptic_solve.py       # the five solutions, all disc = 0
    python3 trackB1_star_full.py            # the A^2 B condition, component II
    python3 trackB1_component2_verify.py    # the three independent checks

## FIRST SEARCH OF COMPONENT II

`trackB1_cascade_general.py` generalizes the cascade to any admissible S. The
level-2 condition is S | P_7^2, i.e. **H(S) | P_7** with the HALF-RADICAL
H(S) = prod pi^ceil(e/2) — that is A on component I (deg 2) and A B on
component II (deg 3), and A^2 C on its A^3 C sub-stratum.

`trackB1_divisor_grid.py` sweeps the full divisor lattice P_7 = A^alpha B^beta M
with M random, 40 samples/cell, p = 65521:

| P_7 | component I | component II |
|---|---|---|
| generic | LADDER_BREAK 3 | LADDER_BREAK 3 |
| rad(S) * M | OBSTRUCTED 3 | OBSTRUCTED 3 |
| S * M | OBSTRUCTED 4 | OBSTRUCTED 4 |
| S^{3/2} * M | OBSTRUCTED 7 | OBSTRUCTED 7 |
| **S^2 (deg 8, forced)** | **SUPPORT_FAIL 8** | **SUPPORT_FAIL 8** |

Component I reproduces the previously published spiral table exactly
(3, 4, 7, then N(Q)-support failure at weight 8) — the regression holds — and
**component II behaves identically**: the ladder drives P_7 to c S^2 =
(c/a) P_8 on both components, and the forced family then fails the
N(Q)-support condition at weight 8. With the free kernel directions randomized
instead of zeroed, every cell on both components dies at level 3 or 4.
**No survivors: 0 in 1000 cells-samples across both components.**

Honest labels, unchanged: level 3's condition is proved; the deeper spiral
steps are measured on an explicit branch, not proved. Component II is now
searched to the same depth as component I, and no counterexample was found on
either.

## Side audit: the C4 test was scale-strict

`cascade()` declared INHOM_FAIL unless `[P_8, F_-10]` equals `-z^2` EXACTLY.
But `[P,Q] = kappa x^2` with `kappa != 0` is an equally good Keller pair
(replace Q by Q/kappa; N(Q) is unchanged), so the scale-invariant test is
"proportional to z^2". `trackB1_bracket_audit.py` re-classifies the raw bracket
as ZERO / PROPORTIONAL / OFF_SUPPORT. Result: **no verdict in the campaign
changes** — no sample has ever landed in PROPORTIONAL — but the test is now the
correct one, and the witness anchor still fails with bracket exactly 0.

---

# THE GAUGE CAVEAT IS RESOLVED — it never affected the formal-F proof

The caveat recorded above ("the [P_8,.]-kernel allows wtop(W) in {20,16,12,8,4}
... pinning that gauge is the last step needed to make the theorem
unconditional") applies to the SECOND (polynomial-W) proof only, and it is
worse there than stated: the gauge Q -> Q + lambda P is **not available at
all**, because (1,0) is a vertex of N(P) with nonzero coefficient and
(1,0) is NOT in N(Q) (N(Q)'s lower edge runs (0,0)-(2,1), so i = 1 needs
j >= 1). So lambda = 0 is forced; only Q -> Q + mu and P -> P + nu survive,
killing weights 12 and 16 but not 20.

None of that touches the FIRST proof, which needs no gauge on Q at all. It
absorbs kernel terms into F, and the only property F must have is [P, F] = 0.
Two facts make the descent airtight; both are now machine-verified
(`trackB1_gauge_resolve.py`):

**FACT 1 (kernel).** Among RATIONAL functions, ker [P_8,.] at weight W is
1-dimensional when (S^)^{W/4} is rational and 0 otherwise. Verified over
F_65521 by brute-force linear algebra with denominators S^N, N = 0..6,
deg H <= 20, for W = -12..12 on a component-I S, a component-II S and a
squarefree S: **75/75 cells match the prediction, 0 mismatches.** (Component I
has S = A^2 so the kernel is nonzero at every EVEN W; component II has
S = A^2 B so only at multiples of 4 — the kernel is *larger* on component I,
which is why the descent must be argued, not assumed.)

**FACT 2 (absorber).** Whenever that kernel is nonzero the absorber exists:
K = c a^{-W/8} P^{W/8} satisfies [P, K] = 0 and has top slice c (S^)^{W/4}.
Its slices are rational precisely because P_8 = a S^2 makes
P_8^{W/8} = a^{W/8} (S^)^{W/4} — exactly as rational as the kernel element
being absorbed. Verified by building P^{3/2} with genuine rational-slice
arithmetic (numerator + S-power exponent; the ladder's division by 2 S^3 just
increments the exponent, so no exact division is ever required) and checking
[P, P^{3/2}] = 0 slice by slice to depth 22 on both components:
**88/88 slices vanish.**

**Descent.** Delta := Q - F has Delta_12 = Q_12 - F_12 = b S^3 - b S^3 = 0, so
wtop(Delta) <= 11. While wtop(Delta) > -10, the weight-(8 + wtop) part of
[P,Delta] = x^2 is [P_8, Delta_wtop] alone and must vanish, so Delta_wtop lies
in the kernel (FACT 1) and is absorbed into F (FACT 2), strictly lowering
wtop. After at most 21 steps wtop(Delta) = -10 — it cannot go below, since
then the weight -2 part of [P,Delta] would be 0, not x^2 — and the weight -2
equation is [P_8, Delta_-10] = x^2 alone. That is (C4), with G = Delta_-10
rational.

**Status: the corrected theorem is UNCONDITIONAL.** No gauge is required, no
polynomiality is demanded of Delta, and the descent cannot stall. The two
components of the previous section are therefore the complete answer to the
top-edge question in case (1).

What remains open in case (1) is unchanged and is NOT this: the ladder spiral
at levels >= 4 is measured on an explicit branch rather than proved, on both
components.

---

# THE LADDER, RE-DERIVED CORRECTLY (2026-08-14) — the spiral is retracted

## The bug: the level <-> variable pairing was off by one

Every cascade solver so far solved level m for the slice P_{9-m}. That is wrong.
In the level-m condition S^3 | N_m, the terms of (P^3)_{24-m} carrying the two
newest slices are

    3 P_8^2 P_{8-m}   = 3a^2 S^4 P_{8-m}        -> S^3 divides it, drops
    6 P_8 P_7 P_{9-m} = 6a S^2 P_7 P_{9-m}      -> S | P_7, so S^3 divides it

so **level m constrains P_{10-m}**, one slice higher. The measured kernel
profile said so all along and was misread: `free == nun` at every level, i.e.
the matrix built against P_{9-m} has RANK ZERO. The solvers were fixing each
slice (to 0, or at random) one level BEFORE the level that constrains it, then
reporting the next level as OBSTRUCTED.

**Retracted:** the spiral table (OBSTRUCTED at 4, then 7, and the "forced"
endgame P_7 = c S^2 failing N(Q)-support at weight 8), on both components.
It measured an artifact. Level 3's condition S | P_7 stands — it is a condition
on P_7, exactly what level 3 constrains under the corrected pairing.

## What each level actually is

| level | constrains | nature |
|---|---|---|
| 2 | P_7 | H(S) \| P_7, H = half-radical (quadratic; by parametrization) |
| 3 | P_7 | S \| P_7 (proved; pure condition, no free slice) |
| 4 | P_6 | QUADRATIC — see below; **never obstructs** |
| 5..11 | P_{10-m} | linear in the newest slice, coupled to earlier free directions |
| 12..22 | — | pure obstructions |

## Level 4 is the perfect-square condition on P, and it always has solutions

Extracting rem(N_4, S^3) by finite differences: the whole condition sits in
S-adic digit 2 (so there is **no P_6-independent obstruction at level 4**), the
quadratic part is exactly (3/4)(X^2 mod S), and the linear part is
multiplication by a fixed beta in R = F_p[z]/(S). So with X := P_6 mod S,

    (3/4) X^2 + beta X + gamma = 0     in    R = F_p[z]/(S),

and completing the square, D := (4/9)beta^2 - (4/3)gamma is **identically zero
in R**. Level 4 is therefore the perfect-square condition

    ( X + (2/3) beta )^2 = 0   in R,

always solvable. Moreover -(2/3)beta == M^2/(4a) mod S EXACTLY (verified on
every sample), where P_7 = S M — i.e. level 4 says precisely

> **P is a perfect square to order 6**: T_2 = (P_6 - T_3^2)/(2T_4) is
> polynomial, where T = P^{1/2}, T_4 = sqrt(a) S, T_3 = M/(2 sqrt a),

relaxed by the slack H(S) | Y. The solution set is

    P_6 = M^2/(4a) + H(S)*y + S*z,     7 params (component I), 6 (component II)

and a constructed P_6 satisfies rem(N_4, S^3) = 0 verified directly against
build_N — **60/60 on component I, 60/60 on component II**.

## The levels are COUPLED, so they must be solved jointly

For generic level-4 free directions, level 5 is EMPTY (Singular: 1 in the
ideal, 8/8 samples) — which is what the per-level solvers reported. But the
JOINT variety in (level-4 params, P_5) is not empty:

| | params | equations | cumulative dimension |
|---|---|---|---|
| component I, level 5 | 15 | 108 | **DIM 13** (codim 2) |
| component II, level 5 | 14 | 108 | **DIM 13** (codim 1) |

So level 5 is passable — it merely cuts the level-4 free directions down by
codimension 1-2. Solving level by level with earlier directions frozen finds
nothing even where solutions exist. **Case (1) is re-opened as a live search.**

## The rational cascade — every condition globally defined

The exact-division cascade is only DEFINED where all earlier levels already
hold (pdiv_exact returns None otherwise), which is why interpolation past level
5 was impossible and why the per-level solvers kept mis-reporting. Carrying F's
slices as rational pairs (num, e) meaning num/S^e — the representation the
formal-F proof uses anyway — removes this entirely: since P_8 = a S^2 makes
F_12 = b S^3 polynomial, dividing by 2 b S^3 just increments e, so no exact
division is ever required and every condition

    w = 11..0    S^e | num          (F_w polynomial = Q_w, plus N(Q) support)
    w = -1       supported at i = 2 only  (the vertex (2,1))
    w = -2..-9   num = 0
    w = -10      [P_8, F_-10] proportional to z^2, nonzero

is a polynomial identity in the parameters, defined everywhere.
`trackB1_rational_cascade.py`. **Witness anchor: P = Stilde^2, Q = Stilde^3
satisfies every ladder and vanishing condition (violations: NONE) and fails
only the bottom bracket, which is exactly zero** — the expected signature.

## Reproduce

    python3 trackB1_offbyone_check.py      # the pairing bug, level 4 quadratic
    python3 trackB1_level4.py              # the ring quadratic; D == 0
    python3 trackB1_level4_solve.py        # constructive P_6, checked vs build_N
    python3 trackB1_rational_cascade.py    # globally-defined conditions + anchor
    python3 trackB1_cumulative2.py I 1     # cumulative dimension, level by level

## Honest status

Case (1) is NOT closed and NOT known to contain a counterexample. What changed
is that the two previously claimed obstructions are gone: the perfect-square
theorem is replaced by a two-component classification (proved exactly), and the
death spiral is retracted as an artifact. The live question is the dimension of
the accumulated variety as levels 6..22 plus support, vanishing and (C4) are
imposed — a well-posed, running computation on 41 (component I) / 40
(component II) parameters, not a blind search.
