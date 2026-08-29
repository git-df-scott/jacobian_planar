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
