# night14 -- PROSPECTOR

Lane: night14 only.  Instruments reimplemented in-lane (night12 read as
reference only).  All verdicts below are measurements produced by the two
instruments; no conclusions beyond what the instruments state are recorded.

## 0. The two measured properties

For P in Q[x,y]:

* **(a) U-test** -- 1 lies in the ideal (P_x, P_y) over Q.  Equivalently
  (Nullstellensatz) P_x and P_y have no common zero over C; equivalently the
  critical locus of P is empty; equivalently every fibre of P is smooth.
  Instrument: `utest14.py`, Singular `groebner` over the ring `0,(x,y),dp`,
  with a mod-p shadow at p = 999983 recorded as a fast prefilter.  Exact
  logical status of the shadow, recorded so it is not over-read: writing
  I_Z = (P_x, P_y) in Z[x,y] after clearing denominators, 1 in I_Q holds iff
  some nonzero integer N lies in I_Z, and then 1 lies in I_p for every prime
  p not dividing N.  So a char-0 PASS forces a mod-p PASS for all but
  finitely many p (hence a mod-p FAIL is *evidence* of a char-0 FAIL, failing
  only on the finitely many p dividing N), while a mod-p PASS is not by
  itself a char-0 proof (a critical point whose coordinates have p in a
  denominator disappears mod p).  The char-0 run is therefore executed on
  every candidate and **the char-0 answer is the recorded verdict**.
* **(b) SY-certificate** -- the Shpilrain-Yu gradient-row reduction over Q on
  the rows (P_x, P_y), total-degree-then-lex order, elementary reduction when
  one leading monomial divides the other, branching when both do, memoized
  normalized rows.  Reaching a node (c, 0) with c a nonzero constant is the
  COORDINATE verdict; an exhausted DAG with no such node is the
  NON_COORDINATE verdict.  Instrument: `sy14.py`.

Background recorded, not asserted as a result of this lane: (a) is a
*necessary* condition for P to admit a Jacobian mate; it is not sufficient,
and nothing in this lane measures the existence of a mate.

### Instrument validation (both reproduced by running the modules)

`python3 sy14.py`:

| polynomial | SY verdict | expected |
|---|---|---|
| x | COORDINATE | COORDINATE |
| y | COORDINATE | COORDINATE |
| x + y^2 | COORDINATE | COORDINATE |
| y + x^3 | COORDINATE | COORDINATE |
| x + y^2 + 2x^2y + x^4 | COORDINATE | COORDINATE |
| x + x^2*y | NON_COORDINATE | NON_COORDINATE |
| x*y | NON_COORDINATE | NON_COORDINATE |
| x^2 + y^2 | NON_COORDINATE | NON_COORDINATE |

`python3 utest14.py`: x, x+y^2, y+x^3, x+x^2y all PASS; the two negative
controls x*y and x^2+y^2 (and x^2*y) **FAIL** the U-test -- their gradients
vanish at the origin.  They are therefore the intended negative controls for
the *pairing* of the two tests: SY NON_COORDINATE alone is not the measured
quantity, the pairing U=PASS with SY=NON_COORDINATE is.

## 1. Design guidance recorded

A coordinate has every fibre isomorphic to the affine line.  A U-passing P has
every fibre smooth.  By Abhyankar-Moh / Suzuki-type results, a P all of whose
fibres are smooth, irreducible, rational and with one place at infinity is a
coordinate.  So an object with U = PASS and SY = NON_COORDINATE must break
one of: positive genus in some fibre, two or more places at infinity, or a
reducible (here necessarily *disconnected*, since fibres are smooth) special
fibre -- while every fibre stays smooth.  The families below are built to
break exactly one of these while holding smoothness.

## 2. F2 -- the constant-discriminant family, derived

Take

    P = g(x)*y^2 + h(x)*y + k(x),      g, h, k in Q[x],   g != 0.

Then

    P_y = 2*g*y + h,
    P_x = g'*y^2 + h'*y + k'.

Write the discriminant D = h^2 - 4*g*k.

**Branch 1: a critical point with g(x0) != 0.**  P_y = 0 gives y = -h/(2g).
Substitute and clear denominators:

    4*g^2 * P_x |_(y = -h/2g)
      = g' * (4*g^2*y^2) + h' * (4*g^2*y) + 4*g^2*k'
      = g'*h^2 - 2*g*h*h' + 4*g^2*k'.

Now differentiate D:  D' = 2*h*h' - 4*g'*k - 4*g*k', hence
4*g*k' = 2*h*h' - 4*g'*k - D', so 4*g^2*k' = g*(2*h*h' - 4*g'*k - D').
Substituting,

    4*g^2 * P_x |_(y = -h/2g)
      = g'*h^2 - 2*g*h*h' + 2*g*h*h' - 4*g*g'*k - g*D'
      = g'*(h^2 - 4*g*k) - g*D'

    ==>   **4*g^2 * P_x |_(P_y = 0)  =  g'*D - g*D'  =:  R(x).**

This is the exact constructive handle.  A critical point with g(x0) != 0
exists iff R(x0) = 0 for some x0 with g(x0) != 0.

**Branch 2: a critical point with g(x0) = 0.**  Then P_y = h(x0), so we also
need h(x0) = 0; but then D(x0) = h(x0)^2 - 4*g(x0)*k(x0) = 0.  If in addition
D(x0) != 0 this branch is empty.  (When D(x0) = 0 the branch contributes iff
the quadratic g'(x0)*y^2 + h'(x0)*y + k'(x0) has a root in C, i.e. unless it
is a nonzero constant.)

**Criterion (general F2).**  The critical locus of P = g y^2 + h y + k is
empty iff

  (i) every root of R = g'*D - g*D' is a root of g, and
  (ii) at every common root x0 of g and h, the polynomial
       g'(x0)*y^2 + h'(x0)*y + k'(x0) is a nonzero constant.

**Specialization D = c0, a nonzero constant.**  Then D' = 0 and R = c0*g'.
Condition (ii) is vacuous (branch 2 is empty, as shown).  Condition (i) says:
every root of g' is a root of g.

* If g is a nonzero constant then g' = 0 and R = 0 identically, so *every* x0
  gives a critical point: **g must be nonconstant**.
* If g = c * prod_i (x - a_i)^{m_i} with r >= 2 distinct roots, then g' has
  degree n - 1 (n = deg g) and vanishes at a_i to order exactly m_i - 1,
  which accounts for n - r of its roots; the remaining r - 1 roots are not
  roots of g, so (i) fails.  Hence r = 1:

      **g = c * (x - a)^n,  c != 0,  n >= 1.**

* Solving h^2 - 4*g*k = c0 for h: h^2 = c0 in Q[x]/((x-a)^n).  That ring is
  local with nilpotent maximal ideal, so from (h/h0 - 1)(h/h0 + 1) = 0 with
  h0^2 = c0 one factor is a unit and h = +-h0 + g*t for an arbitrary t in
  Q[x].  Then k = (h^2 - c0)/(4g) = (2*h0*t + g*t^2)/4 (taking the + sign).

**F2 normal form.**  With g = c(x-a)^n, h = h0 + g*t, k = (2 h0 t + g t^2)/4:

    4*g*P = (2*g*y + h)^2 - c0 = (2*g*y + h)^2 - h0^2
          = g*(2y + t) * (2*h0 + g*(2y + t)),

so, setting v = y + t(x)/2 (a triangular automorphism of Q[x,y], which
preserves both measured properties),

    **P = h0*v + c*(x - a)^n * v^2,     h0 != 0,  c != 0,  n >= 1.**

Directly: P_x = c*n*(x-a)^(n-1)*v^2 and P_v = h0 + 2*c*(x-a)^n*v, so a common
zero needs (x-a)^(n-1)*v^2 = 0, i.e. v = 0 or x = a, and either forces
P_v = h0 != 0.  The critical locus is empty for every n >= 1 -- the U-test
PASS is *derived*, not merely observed, for this family.

The fibre P = 0 is  v * (h0 + c*(x-a)^n * v) = 0: two components, disjoint
because v = 0 forces the second factor to equal h0 != 0.  So the fibre P = 0
is smooth and disconnected -- the "reducible special fibre" route of section
1, with every fibre still smooth.  This is the independent (non-SY)
corroboration used in each CRUX record.

The same shape at y-degree 1 (the g = 0 boundary, P = k + h*y with h = x^2,
k = x) is the object `x + x^2*y`.

## 3. The other prospected families

* **F1 -- multi-place-at-infinity designs.**  Top form with two or more
  distinct non-associate irreducible factors: x^a*y^b*(x+y)^c mixtures plus
  lower terms tuned against critical points.
* **F2b -- nonconstant discriminant.**  Uses the general criterion of
  section 2: choose g = c(x-a)^n and D with all roots of R = g'D - g D' at
  roots of g, i.e. genuinely nonconstant D; these have positive-genus fibres.
* **F3 -- near-coordinate twists.**  Triangular/affine images and small
  corrections of coordinates.
* **F4 -- random sparse with a linear term**, as background.

## 4. Results

See `RESULTS.md` (per-family tallies) and `records.csv` / `records.json` (per
candidate: family, degree, U mod-p, U char-0, SY verdict, timings).  Objects
measured with U = PASS and SY = NON_COORDINATE are committed one directory
each as `CRUX_<hash>/`.
