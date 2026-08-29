# night20 / IRREDUCIBLE.md -- the irreducible-fibre, positive-genus target

Measurements only.  Lane: `night20/` (nothing outside it was written).
Read-only inputs: `night19/UNCONDITIONAL.md` (the target statement and the
mechanism), `night19/mate19.py` (the exact bivariate mate kernel, imported
unchanged).  Oracle: Singular (`std`, `lift`, `resultant`, `factorize`,
`absfact.lib::absFactorize`, `normal.lib::genus`).

Throughout `[F, G] := F_x G_y - F_y G_x`; a **mate** of `P` is a polynomial
`Q` with `[P, Q] = 1`.

---

## 0. The target, and why it is this one

night19 proved that `R = gamma x y^2 + c y` has no polynomial mate, and located
the mechanism: the formal solution sums to a *rational* mate
`Q_inf = -x/(gamma x y + c)` whose poles sit on the second component of the
**reducible** zero fibre `R = y (gamma x y + c)`.  Every `P` the campaign had
certified non-coordinate so far was certified that way -- by exhibiting a
reducible or disconnected fibre -- which is exactly the feature that produces
the pole.

So the target of this lane is a `P` whose non-coordinacy cannot come from
reducibility:

> **(T)**  `P` unimodular (`1` in `(P_x, P_y)`, i.e. no critical point),
> **all** fibres `P = c` irreducible over `Qbar`, and generic fibre of
> geometric genus `>= 1`.

`genus >= 1` is forced, not chosen: a coordinate has every fibre isomorphic to
the affine line, hence genus 0, and by **Neumann-Norbury** (*nontrivial
rational polynomials in two variables have reducible fibres*) a polynomial
whose generic fibre is rational and whose fibres are all irreducible is a
coordinate.  So "all fibres irreducible + genus 0" leaves only coordinates, and
`(T)` with `genus >= 1` is the whole of what is left.

One structural fact, used everywhere below and recorded as a measurement in its
own right: **the generic fibre is irreducible for every `P`.**  `P(x,y) - c` is
irreducible in `Qbar[x,y,c]` (it has degree 1 in `c` with unit leading
coefficient and its two coefficients `1` and `P` are coprime), so by Gauss it is
irreducible in `Qbar(c)[x,y]`.  The entire content of "all fibres irreducible"
therefore lies in the finitely many special values of `c`, and those are what
the instruments hunt.

---

## 1. Instruments (`inst20.py`, `mate20.py`, `gen20.py`)

**(i) Unimodularity.**  `ring 0,(x,y),dp; reduce(1, std(P_x, P_y))` must be `0`;
on success `lift(ideal(P_x,P_y), ideal(1))` returns an explicit Bezout pair
`(U, V)`, which is brought back into sympy and `U*P_x + V*P_y - 1` is expanded;
the certificate is accepted only when that expansion is the zero polynomial.

**(ii) Fibre irreducibility over `Qbar`, at every `c`.**  The generic fibre is
free (see above).  For the special values a finite superset is computed and
then every member of it is decided exactly:

* *superset.*  Project away `y`: write `P - c = sum_j b_j(x) y^j`, `n = deg_y`,
  `a(x) = b_n`, `D(x,c) = disc_y(P-c)`.  Off the roots of `a` the fibre is an
  `n`-sheeted cover of the `x`-line branched over the roots of `D`.  On a region
  of the `c`-line where no two roots of `D` collide, none escapes to `x = inf`,
  none meets a root of `a`, and `b_1..b_n` acquire no new common root with
  `b_0`, the branched-cover datum is a locally trivial family, so the number of
  connected components of the fibre is constant there.  The generic fibre is
  connected.  Hence every reducible value is a root of
  `disc_x(sqfree_x D) * lc_x(D) * lc_x(sqfree_x D) * Res_x(a, sqfree_x D) *
  cont_x(D) * Res_x(gcd(b_1..b_n), b_0)`.
  Projecting away `x` gives a second valid superset; the **intersection** of the
  two is used.
* *decision at a special value.*  For an irreducible `m(c)` in `Q[c]` of degree
  `k`, form `N(x,y) = Res_c(m(c), P - c) = prod_i (P - c_i)` over the conjugate
  roots and run Singular's `absFactorize` on `N`, over `Q`.  The conjugate
  fibres have the same number `r` of absolutely irreducible components and `N`
  has `k*r` of them, so `r = absfactors(N)/k`.  This keeps every factorisation
  over `Q`, where absolute factorisation is available, and answers the question
  over `Qbar`.

**(iii) Genus.**  `normal.lib::genus(ideal(P - c))` in the ring `(0,c),(x,y)`:
the geometric genus of the generic fibre, over `Q(c)`.  Cross-checked two ways
in the controls -- against the classical hyperelliptic value, and against
Baker's bound (the number of interior lattice points of the Newton polygon of
`P - c`, computed by Pick's formula in `gen20.interior`).

**(iv) The mate system.**  `[P, Q] = 1` is linear in the coefficients of `Q`;
on the carrier `S(D) = { x^i y^j : i+j <= D }` it is `M q = e_(0,0)`.  Decided
exactly over `Q` by `night19/mate19.py` (imported unchanged); on `EMPTY` the
transposed system `[M^T ; e^T] lambda = (0,..,0,1)` is solved and the resulting
`lambda` is re-verified by expansion against every column.  The null directions
`Q -> Q + h(P)` are counted (`1, P, P^2, ...` of degree `<= D`) and recorded per
carrier.

**(v) The rational mate.**  `Q = A/B` with `B` a product `g_1^k1 ... g_r^kr` of
prescribed generators: `P_x (A_y B - A B_y) - P_y (A_x B - A B_x) = B^2`, linear
in `A`, solved exactly over `Q`, and every solution is re-checked by
`[P, Q] - 1 = 0` in the fraction field.

---

## 2. Controls, verbatim

### 2.1 the instruments (`controls20.py` -> `controls20_log.txt`)

```
==============================================================================
K1  a COORDINATE must come out: unimodular, genus 0, all fibres irreducible
==============================================================================
  P = x + y**2                           deg=2  
     unimodular : YES   U = 1                        V = 0                         U*P_x+V*P_y-1 expands to 0
     genus(generic fibre, Singular/normal.lib over Q(c)) = 0   |  Baker bound = #interior lattice pts of Newton(P-c) = 0
     fibre irreducibility over Qbar: 0 candidate special value(s); all fibres irreducible = True
  P = x**10 + 2*x**5*y - x + y**2        deg=10 
     unimodular : YES   U = -1                       V = 5*x**4                    U*P_x+V*P_y-1 expands to 0
     genus(generic fibre, Singular/normal.lib over Q(c)) = 0   |  Baker bound = #interior lattice pts of Newton(P-c) = 4
     fibre irreducibility over Qbar: 0 candidate special value(s); all fibres irreducible = True
  P = x**12 + 4*x**9*y + 2*x**9 + 6*x**6*y**2 + 6*x**6*y + x**6 + 4*x**3*y**3 + 6*x**3*y**2 + 2*x**3*y - x + y**4 + 2*y**3 + y**2 deg=12 
     unimodular : YES   U = -1                       V = 3*x**2                    U*P_x+V*P_y-1 expands to 0
     genus(generic fibre, Singular/normal.lib over Q(c)) = 0   |  Baker bound = #interior lattice pts of Newton(P-c) = 15
     fibre irreducibility over Qbar: 0 candidate special value(s); all fibres irreducible = True
  K1 verdict: PASS

==============================================================================
K2  x*y -- report what it ACTUALLY is (no assumption)
==============================================================================
  P = x*y                                deg=2  
     unimodular : NO    reduce(1, std(P_x,P_y)) = 1
     genus(generic fibre, Singular/normal.lib over Q(c)) = 0   |  Baker bound = #interior lattice pts of Newton(P-c) = 0
     fibre irreducibility over Qbar: 1 candidate special value(s); all fibres irreducible = False
        c root of  c                                        -> 2 absolutely irreducible component(s)
  measured: unimodular = False (the ideal (P_x,P_y) = (y,x) is the maximal
  ideal at the origin, so 1 is NOT in it: x*y is NON-UNIMODULAR, it has
  the critical point (0,0)); genus = 0; the fibre c = 0 splits as x*y = 0
  into 2 absolutely irreducible components, so NOT all fibres are irreducible.
  K2 verdict: PASS

==============================================================================
K3  hyperelliptic y^2 - f(x): the classical genus floor((deg f - 1)/2)
==============================================================================
  P = y^2 - (x**5 + x + 1    )   Singular genus = 2    classical genus = 2    Baker interior-point bound = 2
  P = y^2 - (x**5 - x        )   Singular genus = 2    classical genus = 2    Baker interior-point bound = 2
  P = y^2 - (x**7 + x + 1    )   Singular genus = 3    classical genus = 3    Baker interior-point bound = 3
  P = y^2 - (x**6 + x + 1    )   Singular genus = 2    classical genus = 2    Baker interior-point bound = 2
  P = y^2 - (x**9 + x**2 + 1 )   Singular genus = 4    classical genus = 4    Baker interior-point bound = 4
  P = y^2 - (x**11 + x + 1   )   Singular genus = 5    classical genus = 5    Baker interior-point bound = 5
  K3 verdict: PASS   (two independent computations of the genus agree:
   Singular's normalisation genus, and the classical hyperelliptic value;
   the Newton-polygon interior count is an upper bound, as Baker's
   theorem requires.)

==============================================================================
K4  a P with a KNOWN reducible special fibre must be DETECTED
==============================================================================
  P = x**2*y + x                      candidate special c: ['c']                     all fibres irreducible = False
       (x + x^2 y at c=0 is x*(x*y+1))
        c root of c                        -> 2 absolutely irreducible component(s)
  P = x*y**2 + y                      candidate special c: ['c']                     all fibres irreducible = False
       (night19's P at c=0 is y*(x*y+1))
        c root of c                        -> 2 absolutely irreducible component(s)
  P = x**2*y**3 + x                   candidate special c: ['c']                     all fibres irreducible = False
       (x + x^2 y^3 at c=0 is x*(x*y^3+1))
        c root of c                        -> 2 absolutely irreducible component(s)
  P = x**2*y**2 - 3*x*y + x + 2       candidate special c: ['c + 1/4', 'c - 2']      all fibres irreducible = False
       (designed to split at some c)
        c root of c + 1/4                  -> 1 absolutely irreducible component(s)
        c root of c - 2                    -> 2 absolutely irreducible component(s)
  P = -x**2 + y**2                    candidate special c: ['c']                     all fibres irreducible = False
       (y^2-x^2 at c=0 is (y-x)(y+x))
        c root of c                        -> 2 absolutely irreducible component(s)
  K4 verdict: PASS

==============================================================================
K5  the target shape exists at all: unimodular + genus >= 1
==============================================================================
  P = x**2*y**3 + x                      deg=5  
     unimodular : YES   U = -2*x*y**3 + 1            V = 4*y**4/3                  U*P_x+V*P_y-1 expands to 0
     genus(generic fibre, Singular/normal.lib over Q(c)) = 1   |  Baker bound = #interior lattice pts of Newton(P-c) = 1
     fibre irreducibility over Qbar: 1 candidate special value(s); all fibres irreducible = False
        c root of  c                                        -> 2 absolutely irreducible component(s)
  (recorded as a measurement: this P is unimodular with a genus-1
   generic fibre, but its fibre c = 0 is reducible -- so it fails the
   third requirement.  Target = unimodular AND all fibres irreducible
   AND genus >= 1.  Genus >= 1 is forced by Neumann-Norbury: a
   nontrivial rational polynomial in two variables has a reducible
   fibre, so irreducible-fibres + genus 0 leaves only coordinates.)

CONTROLS PASS
```

### 2.2 the mate solver (`matectl20.py` -> `matectl20_log.txt`)

```
==============================================================================
M1  the mate solver must FIND the mate of a coordinate of degree >= 10
==============================================================================
  P10 = (y + x^5)^2 - x                    deg = 10   verdict = MATE
      Q = -x**5 - y
      deg Q = 5 ; [P,Q] - 1 = 0 ; verified = True
  P12 = ((y + x^3)^2 + (y + x^3))^2 - x    deg = 12   verdict = MATE
      Q = -x**3 - y
      deg Q = 3 ; [P,Q] - 1 = 0 ; verified = True
  P15 = (y + x^5)^3 - x                    deg = 15   verdict = MATE
      Q = -x**5 - y
      deg Q = 5 ; [P,Q] - 1 = 0 ; verified = True
  M1 verdict: PASS

==============================================================================
M2  the same code path must return EMPTY with a re-verified lambda on
    night19's P = x*y^2 + y (proved mate-free there)
==============================================================================
  P = x*y^2 + y   verdict = EMPTY
      D=1   EMPTY_over_Q   |lambda| = 2  lambda re-verified = True
      D=2   EMPTY_over_Q   |lambda| = 2  lambda re-verified = True
      D=3   EMPTY_over_Q   |lambda| = 3  lambda re-verified = True
      D=4   EMPTY_over_Q   |lambda| = 3  lambda re-verified = True
      D=12  EMPTY_over_Q   |lambda| = 7  lambda re-verified = True
  M2 verdict: PASS

==============================================================================
M3  the rational-mate solver must recover night19's rational mate
    Q_inf = -x/(x*y + 1)  of  P = x*y^2 + y   (gamma = c = 1)
==============================================================================
  {"found": true, "k": 1, "deg_A": 1, "A": "-x", "g": "x*y + 1", "Q": "-x/(x*y + 1)", "poles": "x*y + 1", "check": "0"}
  M3 verdict: PASS

MATE-SOLVER CONTROLS PASS
```

---

## 3. The generators, and the design reasoning

Three sweeps, all recorded in the lane.

**Sweep A (`gen20.py` + `search20.py`) -- Newton polygons with an interior
point and no torus critical points.**  Genus `>= 1` needs an interior lattice
point in `Newton(P - c) = conv(supp P u {0})` (Baker), so supports without one
are discarded for free.  For the critical points, Bernstein's theorem bounds the
number of solutions of `P_x = P_y = 0` in `(C*)^2` by
`MV(Newton(P_x), Newton(P_y))`; `MV = 0` therefore *forces* the torus part of
the critical locus to be empty for **every** choice of coefficients on that
support, and `MV = 0` in the plane means the two polygons are points or parallel
segments.  All such supports of size 2, 3, 4 were enumerated to degree 12, and
of size 2, 3 to degree 25; what remains is a one-variable gcd on the two axes,
and then Singular.

**Sweep B (`search2_20.py`) -- the coefficient-degenerate ones.**  `MV > 0` does
not imply a critical point exists, only that *generic* coefficients on that
support have one.  So a second sweep drops the `MV = 0` requirement and filters
instead by the Bernstein *degeneracy* condition (`gen20.torus_may_be_empty`):
an empty torus part forces `MV = 0` or a face system with a common torus zero in
some edge-normal direction; faces that are single monomials never vanish in the
torus, two faces on lattice segments of different primitive directions always
have a common torus zero, two on segments of the same direction have one iff the
corresponding univariate polynomials share a non-zero root.  Survivors go to
Singular in batches.  Run on all 3-term supports of degree `<= 10` with
coefficients in `{+-1, +-2, +-3}`: 717768 coefficient vectors, 3024 of them
critical-point-free.

**Sweep C (`search3_20.py`) -- the DESIGNED sweep, aimed straight at (T).**
The Newton polygon can be made to force irreducibility of *every* fibre:
`Newton(F G) = Newton(F) + Newton(G)`, so a polynomial whose Newton polygon is
2-dimensional, Minkowski-**indecomposable**, and touches both axes (no monomial
factor) is irreducible.  For `c != P(0,0)` the fibre has polygon
`N1 = conv(supp P u {0})`; for `c = P(0,0)` the `(0,0)` vertex disappears and it
has `N0 = conv(supp P \ {0})`.  **If both `N1` and `N0` are 2-dimensional,
indecomposable and touch both axes, then all fibres are irreducible, whatever
the coefficients.**  `gen20.indecomposable` decides indecomposability by
searching the edge-multiplicity vectors `0 <= n_i <= m_i` with
`sum n_i d_i = 0`.  Sweep C enumerates exactly those supports (with an interior
lattice point) and sweeps coefficients in
`{+-1, +-2, +-3, +-4, +-6, +-1/2}` against the same critical-point filters.
This is the intersection of the three conditions of `(T)`, attacked from the
geometric side.

---

## 4. What the sweeps measured

### 4.1 the census

| | |
|---|---|
| polynomials certified **unimodular** (Groebner + expanded Bezout residual `0`) | **3408** |
| of those, generic fibre of **genus `>= 1`** | **3408** |
| degrees covered | 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25 |
| genera covered | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 |
| **all fibres irreducible** (the third gate) | **0** |
| **objects meeting the full triple gate (T)** | **0** |

Every one of the 3408 certified objects has **exactly one** reducible fibre:

| number of reducible fibres | count |
|---|---|
| 1 | 3408 |

and in **every** case that single reducible value is `c0 = P(0,0)` -- exactly
the value at which the Newton polygon of `P - c` loses its `(0,0)` vertex
(3408 of 3408; 0 exceptions).  The number of absolutely irreducible components of
that one fibre:

| components | count |
|---|---|
| 2 | 2601 |
| 3 | 528 |
| 4 | 255 |
| 5 | 12 |
| 6 | 4 |
| 7 | 4 |
| 8 | 2 |
| 9 | 2 |

### 4.2 the designed sweep

Sweep C found supports in abundance whose Newton design already forces every
fibre to be irreducible (500 at degree 4, 3066 at degree 5, 10111 at degree 6,
36604 at degree 7, 90352 at degree 8, of sizes 3-5, all with an interior lattice
point).  On those supports, no critical-point-free polynomial was found in the
coefficient box swept -- the log `search3_log.txt` carries the running count.
The tension the sweep exposes, recorded as the measurement it is: an
indecomposable 2-dimensional Newton polygon makes `Newton(P_x)` and
`Newton(P_y)` 2-dimensional too, so `MV(Newton(P_x), Newton(P_y)) > 0` and a
critical point can only be avoided by a Bernstein degeneracy of the
coefficients; whereas `MV = 0`, which is what every critical-point-free `P`
found in sweeps A and B realises, forces the Newton polygon to be thin, and a
thin polygon has the decomposable `N0` that produces the reducible fibre.

---

## 5. Mate verdicts

143 of the certified objects were mate-solved exactly over `Q` (`run20.py`),
carriers escalated as `S(1), ..., S(2 deg P)` (`4 deg P` for the smallest, and
capped at `D = 26` for the high-degree end, which is recorded per row in the
csv).  Result:

| verdict | count |
|---|---|
| `MATE_over_Q` | **0** |
| `EMPTY_over_Q`, with a `lambda` re-verified by expansion | **143** |

every `lambda` re-verified: **True**.  The same code path finds the mate of the
coordinates `(y+x^5)^2 - x` (degree 10), `((y+x^3)^2 + (y+x^3))^2 - x`
(degree 12) and `(y+x^5)^3 - x` (degree 15) -- see the control §2.2.

### 5.1 per-object table (first 60 rows; the full 143 rows are in `irreducible.csv`)

| P | deg | unimodular (Bezout U, V; residual) | Baker | genus | candidate special c | reducible c | all fibres irred. | mate | top carrier D | \|lambda\| | lambda verified | certificate id | rational mate | poles |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `-x**3*y**2 + y + 1` | 5 | `U=-4*x**4/3`, `V=2*x**3*y + 1`, residual `0` | 1 | 1 | 1 | ['c - 1'] | False | EMPTY | 20 | 6 | True | `lam-de1a255bc7-D20` | False | None |
| `x**3*y**2 + y + 1` | 5 | `U=4*x**4/3`, `V=-2*x**3*y + 1`, residual `0` | 1 | 1 | 1 | ['c - 1'] | False | EMPTY | 20 | 6 | True | `lam-f67fd88e64-D20` | False | None |
| `x**3*y**2 - y + 1` | 5 | `U=4*x**4/3`, `V=-2*x**3*y - 1`, residual `0` | 1 | 1 | 1 | ['c - 1'] | False | EMPTY | 20 | 6 | True | `lam-a76fe424e2-D20` | False | None |
| `x**3*y**2 - y - 1` | 5 | `U=4*x**4/3`, `V=-2*x**3*y - 1`, residual `0` | 1 | 1 | 1 | ['c + 1'] | False | EMPTY | 20 | 6 | True | `lam-432cf744e0-D20` | False | None |
| `-x**4*y**2 + y + 1` | 6 | `U=-x**5`, `V=2*x**4*y + 1`, residual `0` | 1 | 1 | 1 | ['c - 1'] | False | EMPTY | 24 | 6 | True | `lam-4df9f3e4ac-D24` | False | None |
| `x**4*y**2 + y + 1` | 6 | `U=x**5`, `V=-2*x**4*y + 1`, residual `0` | 1 | 1 | 1 | ['c - 1'] | False | EMPTY | 24 | 6 | True | `lam-41ab6c887c-D24` | False | None |
| `x**4*y**2 - y + 1` | 6 | `U=x**5`, `V=-2*x**4*y - 1`, residual `0` | 1 | 1 | 1 | ['c - 1'] | False | EMPTY | 24 | 6 | True | `lam-9e6eb9756f-D24` | False | None |
| `x**4*y**2 - y - 1` | 6 | `U=x**5`, `V=-2*x**4*y - 1`, residual `0` | 1 | 1 | 1 | ['c + 1'] | False | EMPTY | 24 | 6 | True | `lam-29df87a644-D24` | False | None |
| `-x**4*y**3 + y + 1` | 7 | `U=-9*x**5*y/4`, `V=3*x**4*y**2 + 1`, residual `0` | 1 | 1 | 1 | ['c - 1'] | False | EMPTY | 14 | 4 | True | `lam-2ef0c6a50c-D14` | False | None |
| `-x**5*y**2 + y + 1` | 7 | `U=-4*x**6/5`, `V=2*x**5*y + 1`, residual `0` | 2 | 2 | 1 | ['c - 1'] | False | EMPTY | 14 | 4 | True | `lam-1819e9509d-D14` | False | None |
| `x**4*y**3 + y + 1` | 7 | `U=9*x**5*y/4`, `V=-3*x**4*y**2 + 1`, residual `0` | 1 | 1 | 1 | ['c - 1'] | False | EMPTY | 14 | 4 | True | `lam-505d96e06a-D14` | False | None |
| `x**4*y**3 - y + 1` | 7 | `U=9*x**5*y/4`, `V=-3*x**4*y**2 - 1`, residual `0` | 1 | 1 | 1 | ['c - 1'] | False | EMPTY | 14 | 4 | True | `lam-0d5fb404b1-D14` | False | None |
| `x**4*y**3 - y - 1` | 7 | `U=9*x**5*y/4`, `V=-3*x**4*y**2 - 1`, residual `0` | 1 | 1 | 1 | ['c + 1'] | False | EMPTY | 14 | 4 | True | `lam-87b9483f89-D14` | False | None |
| `x**5*y**2 + y + 1` | 7 | `U=4*x**6/5`, `V=-2*x**5*y + 1`, residual `0` | 2 | 2 | 1 | ['c - 1'] | False | EMPTY | 14 | 4 | True | `lam-f08a93028d-D14` | False | None |
| `x**5*y**2 - y + 1` | 7 | `U=4*x**6/5`, `V=-2*x**5*y - 1`, residual `0` | 2 | 2 | 1 | ['c - 1'] | False | EMPTY | 14 | 4 | True | `lam-dc164cddf8-D14` | False | None |
| `x**5*y**2 - y - 1` | 7 | `U=4*x**6/5`, `V=-2*x**5*y - 1`, residual `0` | 2 | 2 | 1 | ['c + 1'] | False | EMPTY | 14 | 4 | True | `lam-8168442def-D14` | False | None |
| `-x**3*y**5 + y + 1` | 8 | `U=-25*x**4*y**3/3`, `V=5*x**3*y**4 + 1`, residual `0` | 1 | 1 | 1 | ['c - 1'] | False | EMPTY | 16 | 4 | True | `lam-81fe753e47-D16` | False | None |
| `-x**5*y**3 + y + 1` | 8 | `U=-9*x**6*y/5`, `V=3*x**5*y**2 + 1`, residual `0` | 2 | 2 | 1 | ['c - 1'] | False | EMPTY | 16 | 4 | True | `lam-ce798da440-D16` | False | None |
| `-x**6*y**2 + y + 1` | 8 | `U=-2*x**7/3`, `V=2*x**6*y + 1`, residual `0` | 2 | 2 | 1 | ['c - 1'] | False | EMPTY | 16 | 4 | True | `lam-3f4a9dcbe6-D16` | False | None |
| `x**3*y**5 + y + 1` | 8 | `U=25*x**4*y**3/3`, `V=-5*x**3*y**4 + 1`, residual `0` | 1 | 1 | 1 | ['c - 1'] | False | EMPTY | 16 | 4 | True | `lam-738e90b141-D16` | False | None |
| `x**3*y**5 - y + 1` | 8 | `U=25*x**4*y**3/3`, `V=-5*x**3*y**4 - 1`, residual `0` | 1 | 1 | 1 | ['c - 1'] | False | EMPTY | 16 | 4 | True | `lam-4a383ac101-D16` | False | None |
| `x**3*y**5 - y - 1` | 8 | `U=25*x**4*y**3/3`, `V=-5*x**3*y**4 - 1`, residual `0` | 1 | 1 | 1 | ['c + 1'] | False | EMPTY | 16 | 4 | True | `lam-56d44607bb-D16` | False | None |
| `x**5*y**3 + y + 1` | 8 | `U=9*x**6*y/5`, `V=-3*x**5*y**2 + 1`, residual `0` | 2 | 2 | 1 | ['c - 1'] | False | EMPTY | 16 | 4 | True | `lam-a311b54021-D16` | False | None |
| `x**5*y**3 - y + 1` | 8 | `U=9*x**6*y/5`, `V=-3*x**5*y**2 - 1`, residual `0` | 2 | 2 | 1 | ['c - 1'] | False | EMPTY | 16 | 4 | True | `lam-1971fb7fba-D16` | False | None |
| `x**5*y**3 - y - 1` | 8 | `U=9*x**6*y/5`, `V=-3*x**5*y**2 - 1`, residual `0` | 2 | 2 | 1 | ['c + 1'] | False | EMPTY | 16 | 4 | True | `lam-5b25af1886-D16` | False | None |
| `x**6*y**2 + y + 1` | 8 | `U=2*x**7/3`, `V=-2*x**6*y + 1`, residual `0` | 2 | 2 | 1 | ['c - 1'] | False | EMPTY | 16 | 4 | True | `lam-0fdecef857-D16` | False | None |
| `-x**5*y**4 + y + 1` | 9 | `U=-16*x**6*y**2/5`, `V=4*x**5*y**3 + 1`, residual `0` | 2 | 2 | 1 | ['c - 1'] | False | EMPTY | 18 | 4 | True | `lam-3a232fd0f9-D18` | False | None |
| `-x**6*y**3 + y + 1` | 9 | `U=-3*x**7*y/2`, `V=3*x**6*y**2 + 1`, residual `0` | 1 | 1 | 1 | ['c - 1'] | False | EMPTY | 18 | 4 | True | `lam-9d38242527-D18` | False | None |
| `-x**7*y**2 + y + 1` | 9 | `U=-4*x**8/7`, `V=2*x**7*y + 1`, residual `0` | 3 | 3 | 1 | ['c - 1'] | False | EMPTY | 18 | 4 | True | `lam-4c69a9b07b-D18` | False | None |
| `x**5*y**4 + y + 1` | 9 | `U=16*x**6*y**2/5`, `V=-4*x**5*y**3 + 1`, residual `0` | 2 | 2 | 1 | ['c - 1'] | False | EMPTY | 18 | 4 | True | `lam-285ca2b243-D18` | False | None |
| `x**5*y**4 - y + 1` | 9 | `U=16*x**6*y**2/5`, `V=-4*x**5*y**3 - 1`, residual `0` | 2 | 2 | 1 | ['c - 1'] | False | EMPTY | 18 | 4 | True | `lam-c1c6bea8a9-D18` | False | None |
| `x**5*y**4 - y - 1` | 9 | `U=16*x**6*y**2/5`, `V=-4*x**5*y**3 - 1`, residual `0` | 2 | 2 | 1 | ['c + 1'] | False | EMPTY | 18 | 4 | True | `lam-4a207772dd-D18` | False | None |
| `x**6*y**3 + y + 1` | 9 | `U=3*x**7*y/2`, `V=-3*x**6*y**2 + 1`, residual `0` | 1 | 1 | 1 | ['c - 1'] | False | EMPTY | 18 | 4 | True | `lam-1a86032864-D18` | False | None |
| `x**6*y**3 - y + 1` | 9 | `U=3*x**7*y/2`, `V=-3*x**6*y**2 - 1`, residual `0` | 1 | 1 | 1 | ['c - 1'] | False | EMPTY | 18 | 4 | True | `lam-df8b64c3e5-D18` | False | None |
| `x**6*y**3 - y - 1` | 9 | `U=3*x**7*y/2`, `V=-3*x**6*y**2 - 1`, residual `0` | 1 | 1 | 1 | ['c + 1'] | False | EMPTY | 18 | 4 | True | `lam-88c5025ccd-D18` | False | None |
| `x**7*y**2 + y + 1` | 9 | `U=4*x**8/7`, `V=-2*x**7*y + 1`, residual `0` | 3 | 3 | 1 | ['c - 1'] | False | EMPTY | 18 | 4 | True | `lam-a14e23798b-D18` | False | None |
| `x**7*y**2 - y + 1` | 9 | `U=4*x**8/7`, `V=-2*x**7*y - 1`, residual `0` | 3 | 3 | 1 | ['c - 1'] | False | EMPTY | 18 | 4 | True | `lam-01a493d4ac-D18` | False | None |
| `x**7*y**2 - y - 1` | 9 | `U=4*x**8/7`, `V=-2*x**7*y - 1`, residual `0` | 3 | 3 | 1 | ['c + 1'] | False | EMPTY | 18 | 4 | True | `lam-42df416346-D18` | False | None |
| `-x**4*y**6 + y + 1` | 10 | `U=-9*x**5*y**4`, `V=6*x**4*y**5 + 1`, residual `0` | 1 | 1 | 1 | ['c - 1'] | False | EMPTY | 20 | 4 | True | `lam-c7ee25ee58-D20` | False | None |
| `x**4*y**6 + y + 1` | 10 | `U=9*x**5*y**4`, `V=-6*x**4*y**5 + 1`, residual `0` | 1 | 1 | 1 | ['c - 1'] | False | EMPTY | 20 | 4 | True | `lam-12575e6066-D20` | False | None |
| `x**4*y**6 - y + 1` | 10 | `U=9*x**5*y**4`, `V=-6*x**4*y**5 - 1`, residual `0` | 1 | 1 | 1 | ['c - 1'] | False | EMPTY | 20 | 4 | True | `lam-9c0a2fc25d-D20` | False | None |
| `x**4*y**6 - y - 1` | 10 | `U=9*x**5*y**4`, `V=-6*x**4*y**5 - 1`, residual `0` | 1 | 1 | 1 | ['c + 1'] | False | EMPTY | 20 | 4 | True | `lam-a466d6e0ad-D20` | False | None |
| `x**6*y**4 + y + 1` | 10 | `U=8*x**7*y**2/3`, `V=-4*x**6*y**3 + 1`, residual `0` | 1 | 1 | 1 | ['c - 1'] | False | EMPTY | 20 | 4 | True | `lam-cc9be262eb-D20` | False | None |
| `x**3*y**8 + y + 1` | 11 | `U=64*x**4*y**6/3`, `V=-8*x**3*y**7 + 1`, residual `0` | 1 | 1 | 1 | ['c - 1'] | False | EMPTY | 22 | 4 | True | `lam-bad624b54f-D22` | False | None |
| `x**6*y**5 + y + 1` | 11 | `U=25*x**7*y**3/6`, `V=-5*x**6*y**4 + 1`, residual `0` | 2 | 2 | 1 | ['c - 1'] | False | EMPTY | 22 | 4 | True | `lam-3532a9da47-D22` | False | None |
| `x**7*y**4 + y + 1` | 11 | `U=16*x**8*y**2/7`, `V=-4*x**7*y**3 + 1`, residual `0` | 3 | 3 | 1 | ['c - 1'] | False | EMPTY | 22 | 4 | True | `lam-da78d50ed7-D22` | False | None |
| `x**9*y**2 + y + 1` | 11 | `U=4*x**10/9`, `V=-2*x**9*y + 1`, residual `0` | 4 | 4 | 1 | ['c - 1'] | False | EMPTY | 22 | 4 | True | `lam-15c87cf830-D22` | False | None |
| `x**10*y**2 + y + 1` | 12 | `U=2*x**11/5`, `V=-2*x**10*y + 1`, residual `0` | 4 | 4 | 1 | ['c - 1'] | False | EMPTY | 24 | 4 | True | `lam-e7cdb9e011-D24` | False | None |
| `x**5*y**7 + y + 1` | 12 | `U=49*x**6*y**5/5`, `V=-7*x**5*y**6 + 1`, residual `0` | 2 | 2 | 1 | ['c - 1'] | False | EMPTY | 24 | 4 | True | `lam-a26fb99d1c-D24` | False | None |
| `x**7*y**5 + y + 1` | 12 | `U=25*x**8*y**3/7`, `V=-5*x**7*y**4 + 1`, residual `0` | 3 | 3 | 1 | ['c - 1'] | False | EMPTY | 24 | 4 | True | `lam-cebc4ed910-D24` | False | None |
| `x**10*y**3 + y + 1` | 13 | `U=9*x**11*y/10`, `V=-3*x**10*y**2 + 1`, residual `0` | 4 | 4 | 1 | ['c - 1'] | False | EMPTY | 26 | 4 | True | `lam-313101597c-D26` | False | None |
| `x**11*y**2 + y + 1` | 13 | `U=4*x**12/11`, `V=-2*x**11*y + 1`, residual `0` | 5 | 5 | 1 | ['c - 1'] | False | EMPTY | 26 | 4 | True | `lam-12907d37f9-D26` | False | None |
| `x**5*y**8 + y + 1` | 13 | `U=64*x**6*y**6/5`, `V=-8*x**5*y**7 + 1`, residual `0` | 2 | 2 | 1 | ['c - 1'] | False | EMPTY | 26 | 4 | True | `lam-93a210a5e8-D26` | False | None |
| `x**7*y**6 + y + 1` | 13 | `U=36*x**8*y**4/7`, `V=-6*x**7*y**5 + 1`, residual `0` | 3 | 3 | 1 | ['c - 1'] | False | EMPTY | 26 | 4 | True | `lam-3332a1a44d-D26` | False | None |
| `x**11*y**3 + y + 1` | 14 | `U=9*x**12*y/11`, `V=-3*x**11*y**2 + 1`, residual `0` | 5 | 5 | 1 | ['c - 1'] | False | EMPTY | 26 | 3 | True | `lam-3066b39225-D26` | False | None |
| `x**3*y**11 + y + 1` | 14 | `U=121*x**4*y**9/3`, `V=-11*x**3*y**10 + 1`, residual `0` | 1 | 1 | 1 | ['c - 1'] | False | EMPTY | 26 | 3 | True | `lam-8c90f920a6-D26` | False | None |
| `x**5*y**9 + y + 1` | 14 | `U=81*x**6*y**7/5`, `V=-9*x**5*y**8 + 1`, residual `0` | 2 | 2 | 1 | ['c - 1'] | False | EMPTY | 26 | 3 | True | `lam-b0ccebf81b-D26` | False | None |
| `x**8*y**6 + y + 1` | 14 | `U=9*x**9*y**4/2`, `V=-6*x**8*y**5 + 1`, residual `0` | 3 | 3 | 1 | ['c - 1'] | False | EMPTY | 26 | 3 | True | `lam-e09d49f31e-D26` | False | None |
| `x**9*y**5 + y + 1` | 14 | `U=25*x**10*y**3/9`, `V=-5*x**9*y**4 + 1`, residual `0` | 4 | 4 | 1 | ['c - 1'] | False | EMPTY | 26 | 3 | True | `lam-bcfd4aed45-D26` | False | None |
| `x**10*y**5 + y + 1` | 15 | `U=5*x**11*y**3/2`, `V=-5*x**10*y**4 + 1`, residual `0` | 2 | 2 | 1 | ['c - 1'] | False | EMPTY | 26 | 3 | True | `lam-1d7bd356a7-D26` | False | None |

---

## 6. The rational mate, and where its poles are

The night19 mechanism asks whether a *rational* `Q` with `[P, Q] = 1` still
exists, and where its poles sit.  Reason to expect the answer to depend on the
genus, recorded as design reasoning: `[P, Q] = 1` says that on each fibre
`P = c` the restriction of `dQ` is the Gelfand-Leray form
`omega_c = dx/P_y = -dy/P_x`.  The differential of a rational function on a
curve has zero residues **and** zero periods.  On a genus-0 fibre only the
residues can obstruct exactness; from genus 1 on there are `2g` further periods
to kill.  So the pole mechanism that produced night19's `Q_inf` should be
available exactly in genus 0.

Measured (`ratcmp20.py` -> `ratcmp20_log.txt`), with the pole divisor searched
over all products `g_1^k1 ... g_r^kr`, `k_i <= 4`, of the components of the
reducible fibres, numerator degree `<= max(12, 2 deg P)`:

```
====================================================================================================
rational mate on the pole divisor of the reducible fibre: genus 0 vs genus >= 1
====================================================================================================
P                           deg  genus  rat mate   pole divisor of Q (or box searched)    Q
x*y^2 + y            (night19)    3      0  FOUND      x*y + 1                                -x/(x*y + 1)
x + x^2*y                     3      0  FOUND      x*y + 1                                y/(x*y + 1)
x + x^3*y                     4      0  FOUND      (x**2*y + 1)**2                        (x**2*y**2 + 2*y)/(2*x**4*y**2 + 4*x**2*y + 2)
x + x^2*y^2                   4      0  none in box  24 denominators x deg A <= 12          
x + x^4*y                     5      0  FOUND      (x**3*y + 1)**3                        (x**6*y**3 + 3*x**3*y**2 + 3*y)/(3*x**9*y**3 + 9*x**6*y**2 + 9*x**3*y + 3)
x*y^2 + 2*y                   3      0  FOUND      x*y + 2                                -x/(x*y + 2)
x^2*y^2 + y                   4      0  none in box  24 denominators x deg A <= 12          
x + x^2*y^3                   5      1  none in box  23 denominators x deg A <= 12          
x^3*y^2 + y                   5      1  none in box  23 denominators x deg A <= 12          
x^4*y^2 + y                   6      1  none in box  22 denominators x deg A <= 12          
x^4*y^3 + y                   7      1  none in box  21 denominators x deg A <= 14          
x^5*y^2 + y                   7      2  none in box  21 denominators x deg A <= 14          
x + x^3*y^3                   6      0  none in box  22 denominators x deg A <= 12          
x^2*y^5 + x                   7      2  none in box  21 denominators x deg A <= 14          

tally: genus 0 with a rational mate: 5 of 8 ; genus >= 1 with a rational mate: 0 of 6
```

and across the 143 mate-solved objects of the census (all of genus `>= 1`), the
rational-mate search over the same kind of box returned **found = 0**.

So the measurement is: for the genus-0 unimodular non-coordinates the night19
rational mate is there and its pole divisor is supported on a **component of the
reducible fibre** (`-x/(xy+1)` and `-1/y` for night19's own `P = x y^2 + y`;
`y/(xy+1)` for `x + x^2 y`; `(x^2y+1)^2` and `(x^3y+1)^3` for `x + x^3 y` and
`x + x^4 y`, i.e. the same component with higher pole order), while for every
positive-genus object measured here no rational mate exists on any divisor
supported on the fibre components inside the searched box -- the pole mechanism
does not simply migrate to another divisor, it goes away.

---

## 7. Hit gate

No mate system was consistent.  `MATE_over_Q` count over every object solved:
**0**.  The hit gate was not reached, and no `HIT_<hash>/` directory was
written.

---

## 8. Files

`inst20.py` (instruments), `gen20.py` (Newton-polygon generator, mixed volume,
Bernstein degeneracy, Minkowski indecomposability), `search20.py` (sweep A),
`search2_20.py` (sweep B), `search3_20.py` (sweep C), `pipe20.py`
(certification pipeline), `mate20.py` (mate + rational mate), `run20.py`
(mate-solving run), `controls20.py`, `matectl20.py`, `ratcmp20.py`,
`assemble20.py`.
Logs: `controls20_log.txt`, `matectl20_log.txt`, `ratcmp20_log.txt`,
`search20_raw_log.txt`, `search2_log.txt`, `search3_log.txt`, `pipe20_log.txt`,
`pipe2_log.txt`, `pipe20b_log.txt`, `run20_log.txt`, `run20sel_log.txt`.
Machine-readable: `irreducible.csv`, `stats20.json`, `cert20.json`,
`cert2_20.json`, `cert20b.json`, `cert20c.json`, `mate20_pass1.json`,
`mate20_sel.json`, `ratcmp20.json`, `controls20.json`.
