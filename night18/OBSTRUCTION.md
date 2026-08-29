# night18 / OBSTRUCTION.md — the mate obstruction computed SYMBOLICALLY over the family

Measurements only.  The family is the one recovered in `night18/FAMILY.md`: the
`HE` stratum with `deg g = 1`, of dimension `deg h + 4`, every point of which
night17 certified gradient-unimodular, non-coordinate and period-free.  night17
decided nineteen of its points one at a time.  This lane decides the *family*.

Instruments: `mate18.py` (the mate system and its certificates, all linear
algebra done over the FIELD `Q(params)` with sympy's `DomainMatrix`, i.e. rref
in the rational function field — never at sample points), `obstruct18.py`
(stages 2 and 3), `cover18.py` / `cover12.py` (the chart walk), `verify18.py`
(specialisation sweep), `controls18.py` (the controls).
Logs: `controls18_log.txt`, `obstruct18_log.txt`, `cover18_log.txt`,
`cover12_log.txt`, `verify18_log.txt`.
Machine-readable: `controls18.json`, `obstruction18.json`, `cover18.json`,
`cover18_D12.json`, `verify18.json`.

---

## 0. Controls (run before any result; verbatim in `controls18_log.txt`)

```
==============================================================================
C1  the symbolic layer must reproduce night17's recorded lambda certificates
==============================================================================
  H3   d37142063698  D=3    night17 lambda (|supp|=8) against night18 M: True   | night18 own lambda (|supp|=8) verified: True  | verdict EMPTY_over_Q==EMPTY_over_Q
  H3   d37142063698  D=5    night17 lambda (|supp|=15) against night18 M: True  | night18 own lambda (|supp|=15) verified: True | verdict EMPTY_over_Q==EMPTY_over_Q
  H3   d37142063698  D=6    night17 lambda (|supp|=13) against night18 M: True  | night18 own lambda (|supp|=13) verified: True | verdict EMPTY_over_Q==EMPTY_over_Q
  H4   431f3f1966ca  D=3    night17 lambda (|supp|=8) against night18 M: True   | night18 own lambda (|supp|=8) verified: True  | verdict EMPTY_over_Q==EMPTY_over_Q
  H4   431f3f1966ca  D=5    night17 lambda (|supp|=14) against night18 M: True  | night18 own lambda (|supp|=17) verified: True | verdict EMPTY_over_Q==EMPTY_over_Q
  H4   431f3f1966ca  D=6    night17 lambda (|supp|=20) against night18 M: True  | night18 own lambda (|supp|=20) verified: True | verdict EMPTY_over_Q==EMPTY_over_Q
  H5   9667585bcb72  D=5    night17 lambda (|supp|=10) against night18 M: True  | night18 own lambda (|supp|=10) verified: True | verdict EMPTY_over_Q==EMPTY_over_Q
  H5   9667585bcb72  D=8    night17 lambda (|supp|=30) against night18 M: True  | night18 own lambda (|supp|=23) verified: True | verdict EMPTY_over_Q==EMPTY_over_Q
  H5   9667585bcb72  D=10   night17 lambda (|supp|=40) against night18 M: TRUNCATED_RECORD | night18 own lambda (|supp|=32) verified: True | verdict EMPTY_over_Q==EMPTY_over_Q
  C1 PASS
```

The `D = 10` row: `night17/mate17.stage` stores only the first 40 entries of
`lambda` in its record (`sorted(lam.items())[:40]`), and that stage's support is
exactly 40, so the recorded vector is a truncation and cannot be re-verified as
written.  It is reported as `TRUNCATED_RECORD`, not as a disagreement; at the
same point this lane solved and verified its own `lambda` (support 32).  The
other eight recorded certificates annihilate **this lane's independently built**
`M` exactly, and night17's solver re-run at the family's parameters returns a
bit-identical `lambda` dict in all nine.

```
==============================================================================
C2  a FAMILY OF COORDINATES: the machinery must find the MATE, symbolically in t
==============================================================================
  P(t) = t**2*x**6 + 2*t*x**5 + 2*t*x**3*y + x**4 + 2*x**2*y - x + y**2
  deg P = 6 ; the construction's own mate Q0 has deg 3 ; [P,Q0]-1 terms = 0
  D=6   n=28    MATE_over_Q(t)  [P,Q]-1 terms = 0  deg Q = 3  t-dependent = True   Q = -t*x**3 - x**2 - y
        Fredholm: a lambda certificate exists = False (must be False)
  D=12  n=91    MATE_over_Q(t)  [P,Q]-1 terms = 0  deg Q = 3  t-dependent = True   Q = -t*x**3 - x**2 - y
        Fredholm: a lambda certificate exists = False (must be False)
  C2 PASS
```

`P(t)` is built from `(x, y)` by the Jacobian-1 moves
`(F,G) -> (F, G + t F^3 + F^2)`, swap, `(F,G) -> (F, G + F^2)`, so it is a
coordinate for every `t`.  The machinery returns a mate whose coefficients are
polynomial in `t` and whose `[P,Q] - 1` is EMPTY over `Q(t)`, and, at the same
carriers, the certificate search over `Q(t)` correctly finds **no** `lambda`.
So the layer detects CONSISTENCY over a family; it is not a machine that only
ever says EMPTY.

```
==============================================================================
C3  symbolic rank of M vs the rank at 5 random specialisations
==============================================================================
  deg h=1  D=3   n_cols=10  n_rows=13   rank(symbolic)=8    ranks at 5 random points = [8, 8, 8, 8, 8]  AGREE
  deg h=1  D=6   n_cols=28  n_rows=34   rank(symbolic)=25   ranks at 5 random points = [25, 25, 25, 25, 25]  AGREE
  deg h=2  D=3   n_cols=10  n_rows=15   rank(symbolic)=8    ranks at 5 random points = [8, 8, 8, 8, 8]  AGREE
  deg h=2  D=6   n_cols=28  n_rows=36   rank(symbolic)=25   ranks at 5 random points = [25, 25, 25, 25, 25]  AGREE
  C3 PASS

CONTROLS PASS
```

---

## 1. The symbolic mate system

`P` is the family of `FAMILY.md`; `deg P = 3` for both `deg h = 1` and
`deg h = 2`.  The carrier is `S(D) = { x^i y^j : i + j <= D }` and the system is
`M(params) q = e_{(0,0)}` with `M`'s columns `[P, x^i y^j]`.

| `deg h` | params | `D` | unknowns | equations | `rank_Q(params) M` | coker | ker | verdict | `|supp lambda|` | secs |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 5 | 3  | 10 | 13 | 8  | 5  | 2 | `EMPTY_over_Q(params)` | 8  | 0.3 |
| 1 | 5 | 6 = `2 deg P` | 28 | 34 | 25 | 9  | 3 | `EMPTY_over_Q(params)` | 20 | 2.4 |
| 2 | 6 | 3  | 10 | 15 | 8  | 7  | 2 | `EMPTY_over_Q(params)` | 8  | 0.9 |
| 2 | 6 | 6 = `2 deg P` | 28 | 36 | 25 | 11 | 3 | `EMPTY_over_Q(params)` | 20 | 58.4 |

Over a field exactly one of "`M q = e` solvable" and "`lambda` exists" holds, so
the certificate is obtained directly as the solution of the transposed system
`[M^T ; e_{(0,0)}^T] lambda = (0, ..., 0, 1)` — no support guessing.  Each
`lambda` is then RE-VERIFIED by exact expansion: `lambda^T M = 0` on **every**
column and `lambda^T e = 1`, over `Q(params)`.

### 1.1 The certificate, `deg h = 1`, carrier `deg Q <= 3` (support 8)

```
lambda_{0,0} = 1
lambda_{0,1} = (-2*a*h1 + h0) / (6*a*gamma)
lambda_{0,2} = (a*h1^2 - 2*h0*h1) / (12*a*gamma^2)
lambda_{0,3} = h0*h1^2 / (8*a*gamma^3)
lambda_{0,4} = (-a*h1^4 - 4*h0*h1^3) / (48*a*gamma^4)
lambda_{1,0} = -2*a/3
lambda_{1,1} = -h0 / (3*gamma)
lambda_{1,2} = -h0^2 / (6*a*gamma^2)
```

verified: `lambda^T M = 0 on all 10 columns and lambda^T e = 1`.

### 1.2 The certificate on the chart `a = 0`, `deg h = 1`, carrier `deg Q <= 6` (support 13)

```
lambda_{0,0} = 1                    lambda_{1,1} = -h0/(2*gamma)
lambda_{0,2} = -h1^2/(4*gamma^2)    lambda_{1,3} =  h0*h1^2/(8*gamma^3)
lambda_{0,3} =  h1^3/(4*gamma^3)    lambda_{1,5} = -5*h0*h1^4/(32*gamma^5)
lambda_{0,4} = -3*h1^4/(16*gamma^4) lambda_{1,6} =  h0*h1^5/(4*gamma^6)
lambda_{0,5} =  h1^5/(8*gamma^5)    lambda_{2,2} =  h0^2/(3*gamma^2)
lambda_{0,6} = -5*h1^6/(64*gamma^6) lambda_{3,3} = -h0^3/(4*gamma^3)
lambda_{0,7} =  3*h1^7/(64*gamma^7)
```

**`alpha` does not occur in any certificate.**  That is forced: by `FAMILY.md`
§5, `alpha` enters `P` only through the additive constant `-alpha/(4 gamma)`,
which the bracket does not see.  The full `deg h = 2` certificates are in
`cover18.json` / `obstruction18.json`.

---

## 2. The degeneration locus

The certificate is a rational object.  The identity `lambda^T M = 0`,
`lambda^T e = 1` is an identity of rational functions, so it specialises
verbatim at every parameter point where none of `lambda`'s denominators
vanishes.  The locus where the certificate above FAILS to be valid is therefore
exactly the vanishing of those denominators; the pivots and leading
coefficients used during the elimination are absorbed into them, because the
final object is re-verified by expansion and does not depend on how it was
found.

For every carrier tested (`D = 3` and `D = 6`), for both `deg h = 1` and
`deg h = 2`, the denominator ideal of the generic certificate is

```
    DEG  =  ( a * gamma )        i.e.  V(a)  union  V(gamma).
```

Both components are irreducible hypersurfaces:

| component | ideal | dimension | ambient | status |
|---|---|---|---|---|
| `V(gamma)` | `(gamma)` | `deg h + 3` | `deg h + 4` | **outside the family**: `k = (h^2 - alpha x - beta)/(4 gamma (x-a))` is not defined and `deg g = 1` fails |
| `V(a)` | `(a)` | `deg h + 3` | `deg h + 4` | inside the family; an artefact of the rref's pivot choice |

`rank M` did not drop anywhere: the symbolic rank equals the rank at every
specialisation tested (C3, and every point below), so there is no separate
rank-drop locus to add.

Also probed, though it is not a degeneration of the certificate but the
family's own excluded wall: `V(h(a))` = `V(a h1 + h0)` for `deg h = 1`,
`V(a^2 h2 + a h1 + h0)` for `deg h = 2`, dimension `deg h + 3`.  Points there
are period-free and non-coordinate but NOT gradient-unimodular (night17's `H6`
instance `fb63dd1ccaec` sits on it).

### 2.1 Exact verdicts on every component

Rational points were drawn on each component, `P` was instantiated there, and
the mate system was built and decided EXACTLY over `Q` (`night17/mate17.stage`,
plus this lane's own symbolic solver specialised, whose `lambda` was re-verified
over `Q` at every point).

**`deg h = 1`, component `V(a)` (4 points, all in the family):**

```
  gamma=3  a=0 alpha=4  h0=1  h1=-2   D=3:EMPTY_over_Q  D=6:EMPTY_over_Q   (own lambda verified, |supp| 8 / 13)
  gamma=2  a=0 alpha=-4 h0=-4 h1=4    D=3:EMPTY_over_Q  D=6:EMPTY_over_Q   (own lambda verified, |supp| 8 / 13)
  gamma=2  a=0 alpha=-4 h0=-3 h1=-1   D=3:EMPTY_over_Q  D=6:EMPTY_over_Q   (own lambda verified, |supp| 8 / 13)
  gamma=-1 a=0 alpha=-4 h0=2  h1=-1   D=3:EMPTY_over_Q  D=6:EMPTY_over_Q   (own lambda verified, |supp| 8 / 13)
```

**`deg h = 1`, component `V(h(a)) = V(a h1 + h0)` (4 points, non-unimodular wall):**

```
  gamma=-2 a=1/2 alpha=-3 h0=1  h1=-2  D=3:EMPTY_over_Q  D=6:EMPTY_over_Q   (own lambda verified, |supp| 5 / 8)
  gamma=-2 a=1   alpha=3  h0=-2 h1=2   D=3:EMPTY_over_Q  D=6:EMPTY_over_Q   (own lambda verified, |supp| 5 / 8)
  gamma=-1 a=-1  alpha=1  h0=1  h1=1   D=3:EMPTY_over_Q  D=6:EMPTY_over_Q   (own lambda verified, |supp| 5 / 8)
  gamma=-3 a=-4  alpha=-1 h0=-4 h1=-1  D=3:EMPTY_over_Q  D=6:EMPTY_over_Q   (own lambda verified, |supp| 5 / 8)
```

**`deg h = 1`, component `V(gamma)` (4 points):** `NOT_A_POINT_OF_THE_FAMILY` —
`P` is not defined there (`1/gamma` in `k`), and `deg g = 1` fails.  Nothing to
decide.

**`deg h = 2`, component `V(a)` (4 points, all in the family):**

```
  gamma=3  a=0 alpha=4  h0=1  h1=-2 h2=2    D=3:EMPTY_over_Q  D=6:EMPTY_over_Q
  gamma=-2 a=0 alpha=1  h0=4  h1=-2 h2=-4   D=3:EMPTY_over_Q  D=6:EMPTY_over_Q
  gamma=-4 a=0 alpha=-4 h0=-1 h1=2  h2=-4   D=3:EMPTY_over_Q  D=6:EMPTY_over_Q
  gamma=-1 a=0 alpha=0  h0=1  h1=-2 h2=-1   D=3:EMPTY_over_Q  D=6:EMPTY_over_Q
```

**`deg h = 2`, component `V(h(a)) = V(a^2 h2 + a h1 + h0)` (4 points):**

```
  gamma=4 a=-1 alpha=-4 h0=-6 h1=-2 h2=4    D=3:EMPTY_over_Q  D=6:EMPTY_over_Q
  gamma=2 a=1  alpha=4  h0=-3 h1=7  h2=-4   D=3:EMPTY_over_Q  D=6:EMPTY_over_Q
  gamma=4 a=-2 alpha=3  h0=-4 h1=4  h2=3    D=3:EMPTY_over_Q  D=6:EMPTY_over_Q
  gamma=0 a=-1 alpha=-3 h0=-2 h1=-1 h2=1    NOT_A_POINT_OF_THE_FAMILY (this point also has gamma = 0)
```

**`deg h = 2`, component `V(gamma)` (4 points):** `NOT_A_POINT_OF_THE_FAMILY`.

Every certificate produced at every one of these points was verified exactly
over `Q` in this lane (`night18_lambda_verified = true` throughout,
`obstruction18.json`).

---

## 3. The degeneration locus is removable: a two-chart cover

The `V(a)` component is an artefact of the elimination, not of the problem, and
`cover18.py` shows it by re-solving the certificate ON the component: restrict
the parameters to `a = 0` and solve again over `Q(alpha, gamma, h_0..h_H)`.

```
==============================================================================
COVER  deg h = 1,  carrier deg Q <= 3
==============================================================================
  [d=0] generic                            EMPTY_over_Q(params)   denominators=['a', 'gamma']  (0.2s)
  [d=1] generic & {a=0}                    EMPTY_over_Q(params)   denominators=['gamma', 'h1']  (0.1s)
  [d=2] generic & {a=0} & {h1=0}           EMPTY_over_Q(params)   denominators=['gamma']  (0.0s)
==============================================================================
COVER  deg h = 1,  carrier deg Q <= 6
==============================================================================
  [d=0] generic                            EMPTY_over_Q(params)   denominators=['a', 'gamma']  (4.4s)
  [d=1] generic & {a=0}                    EMPTY_over_Q(params)   denominators=['gamma']  (0.3s)
==============================================================================
COVER  deg h = 2,  carrier deg Q <= 3
==============================================================================
  [d=0] generic                            EMPTY_over_Q(params)   denominators=['a', 'gamma']  (1.8s)
  [d=1] generic & {a=0}                    EMPTY_over_Q(params)   denominators=['gamma', 'h1']  (0.5s)
  [d=2] generic & {a=0} & {h1=0}           EMPTY_over_Q(params)   denominators=['gamma']  (0.1s)
==============================================================================
COVER  deg h = 2,  carrier deg Q <= 6
==============================================================================
  [d=0] generic                            EMPTY_over_Q(params)   denominators=['a', 'gamma']  (59.5s)
  [d=1] generic & {a=0}                    EMPTY_over_Q(params)   denominators=['gamma']  (0.9s)
```

Every branch terminates on `gamma`, the stratum's own defining non-vanishing.
So, at the carrier `deg Q <= 2 deg P = 6`,

> **two** exactly verified symbolic certificates — the generic one and the one
> on `a = 0` — cover the ENTIRE `deg h + 4`-dimensional family, `deg h = 1` and
> `deg h = 2`, with **empty** degeneration locus inside the family
> (`gamma != 0`).  At the smaller carrier `deg Q <= 3` the cover needs three
> charts (`generic`, `a = 0`, `a = 0 & h1 = 0`), again with empty residue.

Note the cover holds on `gamma != 0` alone: it does not even need
`h(a) != 0`, so it covers the non-unimodular wall as well.

---

## 4. One certificate, many `P`: the specialisation sweep (`verify18.py`)

60 random rational parameter points per row; for each, the chart whose
restriction the point satisfies and whose denominators do not vanish is picked,
its SYMBOLIC `lambda` is substituted, and `lambda^T M = 0` / `lambda^T e = 1`
are verified EXACTLY over `Q` at that point.

```
SPECIALISATION SWEEP -- one symbolic certificate, many P
  deg h=1  D=3    60 points; charts used {generic: 51, a=0: 8, a=0 & h1=0: 1}; verifies over Q at 60 / 60
  deg h=1  D=6    60 points; charts used {generic: 51, a=0: 9};                verifies over Q at 60 / 60
  deg h=2  D=3    60 points; charts used {generic: 49, a=0: 10, a=0 & h1=0: 1}; verifies over Q at 60 / 60
  deg h=2  D=6    60 points; charts used {generic: 49, a=0: 11};               verifies over Q at 60 / 60
ALL VERIFIED
```

---

## 5. The carrier `deg Q <= 4 deg P = 12`, and a closed form

### 5.1 Directly, `deg h = 1` (`cover12.py`, full 5-parameter family)

```
==============================================================================
COVER  deg h = 1,  carrier deg Q <= 12 (= 4 deg P)
==============================================================================
  [d=0] generic                            EMPTY_over_Q(params)   denominators=['a', 'gamma']  (451.9s)
  [d=1] generic & {a=0}                    EMPTY_over_Q(params)   denominators=['gamma']  (1.9s)
```

`n = 91` unknowns, `102` equations, `|supp lambda| = 59` on the generic chart
and `42` on `a = 0`; same two-chart cover, same empty degeneration locus inside
the family.

### 5.2 `deg h = 2` at `D = 12`, via the carrier-preserving translation (`red2_18.py`)

`TAU_a : (x,y) -> (x + a, y)` has Jacobian 1 and maps the carrier
`{ deg <= D }` onto itself, and it carries the member with parameters
`(gamma, a, alpha, h)` to the member with `a = 0` and `h(x) -> h(x + a)`;
`alpha` may additionally be set to `0` because it only shifts `P` by a constant,
which `[P, Q]` does not see.  On that slice (free parameters
`gamma, h0, h1, h2`):

```
  deg h=2  slice {a=0, alpha=0}  D=6   n=28  rows=36   EMPTY_over_Q(params)  |supp|=14  denominators=['gamma']
  deg h=2  slice {a=0, alpha=0}  D=12  n=91  rows=105  EMPTY_over_Q(params)  |supp|=45  denominators=['gamma']
```

### 5.3 The slice `R = gamma x y^2 + c y` and a closed-form certificate

For `deg h = 1` BOTH carrier-preserving moves are available (`FAMILY.md` §5:
the shear `y -> y - h1/(2 gamma)` has degree 0 there), so every member is
carried onto the two-parameter slice

```
    R(gamma, c)  =  gamma * x * y^2  +  c * y ,        c = h(a).
```

`red18.py` solves the certificate on `R`:

```
SLICE  R(gamma, c) = gamma x y^2 + c y
  D=3   n=10   rows=12   EMPTY_over_Q(params)  |supp lambda|=3   denominators=['gamma']  (0.0s)
  D=6   n=28   rows=33   EMPTY_over_Q(params)  |supp lambda|=4   denominators=['gamma']  (0.1s)
     pulled back to 6 random deg h = 1 members at D=6:  verified over Q at 6 / 6
  D=12  n=91   rows=102  EMPTY_over_Q(params)  |supp lambda|=7   denominators=['gamma']  (0.5s)
     pulled back to 6 random deg h = 1 members at D=12: verified over Q at 6 / 6
  D=18  n=190  rows=207  EMPTY_over_Q(params)  |supp lambda|=10  denominators=['gamma']  (2.2s)
```

and the answer has a closed form:

> ### the obstruction
> ```
>     lambda_{n,n}  =  (-1)^n * c^n / ( (n+1) * gamma^n ) ,    0 <= n <= floor((D+1)/2)
>     lambda_m      =  0                                        for every other monomial m
> ```
> a DIAGONAL functional on the coefficients of `[P, Q]`, with the only
> denominator a power of `gamma`.

`closed18.py` writes that formula down independently of any elimination and
verifies `lambda^T M = 0` on every column and `lambda^T e = 1` over
`Q(gamma, c)`:

```
  D=2 ... D=24   |supp lambda| = 2 ... 13   verified over Q(gamma,c): True   at every D
  CLOSED FORM VERIFIED at every carrier tested
```

(23 carriers, up to `n = 325` unknowns and `348` equations at `D = 24 = 8 deg P`.)

> **An instrument error found and fixed, recorded because it changed answers.**
> The first version of `closed18.py` cut the diagonal at `n <= floor(D/2)` and
> reported `verified = False` at every ODD `D` while passing at every even `D`.
> The cut is wrong: the row monomials of `M` run up to total degree `D + 1`, so
> `(n, n)` is a row exactly when `2n <= D + 1`, i.e. `n <= floor((D+1)/2)` —
> which coincides with `floor(D/2)` only for even `D`.  With the corrected cut
> all 23 carriers verify.  The rref-produced certificates had the right support
> all along; it was the hand-written formula that was short by one entry.

---

## 6. Measurements

**N1.  A symbolic certificate EXISTS.**  For the `HE`, `deg g = 1` family with
its parameters kept symbolic, at `deg h = 1` (5 parameters) and `deg h = 2`
(6 parameters), a vector `lambda(params)` with entries rational in the
parameters, satisfying `lambda^T M = 0` on every column of the mate system and
`lambda^T e_{(0,0)} = 1`, was solved over `Q(params)` and verified by exact
expansion, at the carriers `deg Q <= 3`, `deg Q <= 6 = 2 deg P` and
`deg Q <= 12 = 4 deg P`.

**N2.  The degeneration locus of the generic certificate is
`V(a * gamma)`** — two irreducible hypersurfaces of dimension `deg h + 3` in the
`deg h + 4`-dimensional parameter space.  `V(gamma)` is not part of the family
at all (`P` is undefined there and `deg g = 1` fails).  `V(a)` is inside the
family and is an artefact of the elimination's pivot choice.  No rank-drop locus
was found: the symbolic rank of `M` equals its rank at every specialisation
tested (C3 and every point of §2.1).

**N3.  Exact verdicts on every component.**  Sixteen rational points were drawn
across the components (`V(a)`, `V(gamma)`, and the probed wall `V(h(a))`), for
`deg h = 1` and `deg h = 2`, and each one's mate system was built and decided
exactly over `Q` at `deg Q <= 3` and `deg Q <= 6`.  Result:
**`EMPTY_over_Q` at every point of every component that is a point of the
family, each with its own `lambda` verified exactly over `Q`**; the points on
`V(gamma)` are not points of the family and were reported as such.

**N4.  The degeneration locus is removable inside the family.**  Re-solving the
certificate ON the component `a = 0` produces a second certificate whose only
denominator is `gamma`.  So at the carrier `deg Q <= 2 deg P = 6` (and at
`deg Q <= 4 deg P = 12` for `deg h = 1`), **two** exactly verified symbolic
certificates cover the entire `deg h + 4`-dimensional family, with EMPTY
degeneration locus inside it.  At `deg Q <= 3` three charts are needed
(`generic`, `a = 0`, `a = 0 & h1 = 0`), again with empty residue.

**N5.  The carrier-relative statement.**  Stated as the brief asks, carrier
explicit:

> For every `(gamma, a, alpha, h_0, h_1)` with `gamma != 0` — that is, for the
> whole `5`-dimensional `deg h = 1` stratum, `deg P = 3`, support `HE(1,1,1)` —
> the mate system of `P` on the carrier `S(D) = { x^i y^j : i + j <= D }` is
> INCONSISTENT over `Q`, for `D = 3`, `D = 6 = 2 deg P` and `D = 12 = 4 deg P`,
> and the inconsistency is witnessed by ONE of two symbolic `lambda(params)`
> per carrier.  The same holds for the whole `6`-dimensional `deg h = 2`
> stratum (`deg P = 3`, support `HE(1,2,3)`) at `D = 3` and `D = 6`, and at
> `D = 12` after the carrier-preserving translation to `a = 0`.
>
> On the two-parameter slice `R = gamma x y^2 + c y`, onto which every member of
> the `deg h = 1` stratum is carried by carrier-preserving Jacobian-1 moves, the
> statement holds at **every carrier `D = 2, ..., 24`** with the single closed
> form `lambda_{n,n} = (-1)^n c^n / ((n+1) gamma^n)`.

This replaces night17's nineteen point verdicts by finitely many certificates
covering infinitely many `P` at once — every odd degree `>= 3` on the `deg h`
axis, and a continuum in each degree.

**N6.  What is NOT measured here.**  The statement is carrier-relative: it says
the mate system is inconsistent on the carriers listed, not that no `Q` of any
degree exists.  Nothing here is a statement about the Jacobian conjecture, and
nothing here is a claim about strata other than `HE` with `deg g = 1`.

---

## 7. Hit-gate status

**No mate system was consistent.**  Every symbolic solve returned
`EMPTY_over_Q(params)` with a `lambda` verified by exact expansion over
`Q(params)`; every exact solve at a rational point of the degeneration locus
returned `EMPTY_over_Q` with a `lambda` verified exactly over `Q`; and the
consistency detector was shown to work on a family of coordinates (control C2,
which returned `MATE_over_Q(t)` with a residual of 0 terms and NO certificate).
`night18/HIT_<hash>/` was therefore never written.
