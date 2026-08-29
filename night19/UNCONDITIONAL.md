# night19 / UNCONDITIONAL.md — the slice `R = gamma x y^2 + c y` has no polynomial mate, at EVERY carrier

Measurements only.  Read-only inputs: `night18/OBSTRUCTION.md` §5.3 (the closed
form, verified there at `D = 2..24`), `night18/FAMILY.md` (the stratum and its
carrier-preserving moves), `night14/sy14.py` + `night14/poly14.py` (the
Shpilrain–Yu certificate, imported unchanged).

Instruments, all written in this lane:
`mate19.py` (bivariate kernel, the mate system, exact linear algebra over `Q`,
Bézout search), `prove19.py` (the machine verification, `D = 2..60`, over
`Q(gamma, c)`), `controls19.py` (C1/C2/C3), `mech19.py` (the mechanism checks),
`cor19.py` (transport along Jacobian-1 moves), `broken19.py` (the deliberately
broken cases and the hit gate).
Logs: `prove19_log.txt`, `controls19_log.txt`, `mech19_log.txt`, `cor19_log.txt`,
`broken19_log.txt`.  Machine-readable: `prove19.json`, `controls19.json`,
`mech19.json`, `cor19.json`, `broken19.json`.

Throughout, `[F, G] := F_x G_y - F_y G_x`, and a **mate** of `P` is a polynomial
`Q` with `[P, Q] = 1`.

---

## 0. Controls (run and passed before anything below was claimed; verbatim from `controls19_log.txt`)

```
==============================================================================
C1  a COORDINATE with a known mate: the machinery must FIND the mate
    and must NOT produce a valid lambda
==============================================================================
  P = x + y^2        D=1  MATE_over_Q    Q = (1)*x^0*y^1            [P,Q]-1 terms = 0  | lambda exists = False  ok
  P = x + y^2        D=2  MATE_over_Q    Q = (1)*x^0*y^1            [P,Q]-1 terms = 0  | lambda exists = False  ok
  P = x + y^2        D=3  MATE_over_Q    Q = (1)*x^0*y^1            [P,Q]-1 terms = 0  | lambda exists = False  ok
  P = x + y^2        D=4  MATE_over_Q    Q = (1)*x^0*y^1            [P,Q]-1 terms = 0  | lambda exists = False  ok
  P = x + y^2        D=5  MATE_over_Q    Q = (1)*x^0*y^1            [P,Q]-1 terms = 0  | lambda exists = False  ok
  P = x + y^2        D=6  MATE_over_Q    Q = (1)*x^0*y^1            [P,Q]-1 terms = 0  | lambda exists = False  ok
  P10 = (y + x^5)^2 - x   deg P = 10 ; construction's own mate deg 5 ; [P,Q0]-1 terms = 0
  P10                D=5  MATE_over_Q    Q = (-1)*x^0*y^1 + (-1)*x^5*y^0 [P,Q]-1 terms = 0  | lambda exists = False  ok (0.0s)
  P10                D=6  MATE_over_Q    Q = (-1)*x^0*y^1 + (-1)*x^5*y^0 [P,Q]-1 terms = 0  | lambda exists = False  ok (0.0s)
  P10                D=7  MATE_over_Q    Q = (-1)*x^0*y^1 + (-1)*x^5*y^0 [P,Q]-1 terms = 0  | lambda exists = False  ok (0.0s)
  C1 PASS
```

```
==============================================================================
C2  the closed-form lambda at rational (gamma, c), verified over Q alone
==============================================================================
  gamma=1     c=1     D=2   closed lambda verified over Q: True  | independent solve: EMPTY_over_Q   (own lambda |supp|=2 verified=True)
  gamma=1     c=1     D=3   closed lambda verified over Q: True  | independent solve: EMPTY_over_Q   (own lambda |supp|=3 verified=True)
  gamma=1     c=1     D=5   closed lambda verified over Q: True  | independent solve: EMPTY_over_Q   (own lambda |supp|=4 verified=True)
  gamma=1     c=1     D=8   closed lambda verified over Q: True  | independent solve: EMPTY_over_Q   (own lambda |supp|=5 verified=True)
  gamma=1     c=1     D=11  closed lambda verified over Q: True  | independent solve: EMPTY_over_Q   (own lambda |supp|=7 verified=True)
  gamma=1     c=1     D=14  closed lambda verified over Q: True  | independent solve: EMPTY_over_Q   (own lambda |supp|=8 verified=True)
  ...  (36 further rows omitted here; all True)
  C2 PASS
```

(42 rows in all — 7 rational `(gamma, c)` points × 6 carriers; the full list is
in `controls19_log.txt` and `controls19.json`.  Every row: the closed-form
`lambda`, specialised and checked purely over `Q`, annihilates every column and
pairs to 1 with `e_{(0,0)}`; and an independent exact solve at the same point
returns `EMPTY_over_Q` with its own re-verified `lambda`.)

```
==============================================================================
C3  unimodular (exact Bezout, zero residual) and NON-COORDINATE (SY + fibre)
==============================================================================
  Bezout over Q(gamma,c):  U = 4*gamma*x^2/c^2 ,  V = (c - 2*gamma*x*y)/c^2
     U*P_x + V*P_y - 1  expands to 0 terms  (must be 0)
     search at gamma=1     c=1     : U*P_x + V*P_y = 1 found at deg <= 2, residual 0 terms
     search at gamma=2     c=3     : U*P_x + V*P_y = 1 found at deg <= 2, residual 0 terms
     search at gamma=-1    c=5     : U*P_x + V*P_y = 1 found at deg <= 2, residual 0 terms
     search at gamma=3     c=-7    : U*P_x + V*P_y = 1 found at deg <= 2, residual 0 terms
     search at gamma=1/2   c=2/3   : U*P_x + V*P_y = 1 found at deg <= 2, residual 0 terms
     search at gamma=-4    c=-9    : U*P_x + V*P_y = 1 found at deg <= 2, residual 0 terms
     search at gamma=7     c=1/5   : U*P_x + V*P_y = 1 found at deg <= 2, residual 0 terms
     Shpilrain-Yu at gamma=1     c=1     : NON_COORDINATE   nodes=1 leaves=1
     Shpilrain-Yu at gamma=2     c=3     : NON_COORDINATE   nodes=1 leaves=1
     Shpilrain-Yu at gamma=-1    c=5     : NON_COORDINATE   nodes=1 leaves=1
     Shpilrain-Yu at gamma=3     c=-7    : NON_COORDINATE   nodes=1 leaves=1
     Shpilrain-Yu at gamma=1/2   c=2/3   : NON_COORDINATE   nodes=1 leaves=1
     Shpilrain-Yu at gamma=-4    c=-9    : NON_COORDINATE   nodes=1 leaves=1
     Shpilrain-Yu at gamma=7     c=1/5   : NON_COORDINATE   nodes=1 leaves=1
     Shpilrain-Yu sanity  x + y^2          : COORDINATE       (a coordinate; must be COORDINATE)
     Shpilrain-Yu sanity  (y+x^5)^2 - x    : COORDINATE       (a coordinate; must be COORDINATE)
     fibre witness: P = c*y + gamma*x*y**2  factors as y*(c + gamma*x*y)
       -> the zero fibre P = 0 has 2 distinct irreducible components: {y = 0} and {gamma x y + c = 0}.
       -> {gamma x y + c = 0} is isomorphic to A^1 minus a point (x = -c/(gamma y)),
          so it is not isomorphic to the affine line; a coordinate has every fibre
          irreducible and isomorphic to A^1.
  C3 PASS

CONTROLS PASS
```

The C1 rows are the hard gate: the same code path that reports `EMPTY_over_Q`
below **finds** the mate `Q = y` of the coordinate `x + y^2`, and **finds** the
mate `Q = -(y + x^5)` of the degree-10 triangular composition
`P = (y + x^5)^2 - x` (built from `(x, y)` by the Jacobian-1 moves
`(P,Q) -> (P, Q + P^5)`, `(P,Q) -> (Q, -P)`, `(P,Q) -> (P, Q + P^2)`,
`(P,Q) -> (Q, -P)`), with `[P,Q] - 1` equal to 0 term by term; and at those same
carriers the certificate search, run unconditionally, returns **no** `lambda`.

---

## 1. The mate system, and the row formula in closed form

Fix a field `k` of characteristic 0, `gamma in k^*`, `c in k`, and

```
    P  =  gamma * x * y^2  +  c * y ,      P_x = gamma*y^2 ,   P_y = 2*gamma*x*y + c .
```

For `Q = sum_{(i,j)} q_{ij} x^i y^j` the equation `[P, Q] = 1` is **linear** in
the `q_{ij}`.  On the carrier `S(D) = { x^i y^j : i + j <= D }` it is
`M q = e_{(0,0)}`, where the column of `M` indexed by `x^i y^j` is the
coefficient vector of `[P, x^i y^j]` and `e_{(0,0)}` is the coefficient vector
of `1`.

### 1.1 Lemma (the row formula)

For all integers `i, j >= 0`,

```
    [P, x^i y^j]  =  (j - 2i) * gamma * x^i y^{j+1}   -   c * i * x^{i-1} y^j ,        (†)
```

the second term being absent when `i = 0`.

*Proof.*  `(x^i y^j)_y = j x^i y^{j-1}` and `(x^i y^j)_x = i x^{i-1} y^j`, so

```
  P_x * (x^i y^j)_y = gamma*y^2 * j x^i y^{j-1}            =  j*gamma * x^i y^{j+1}
  P_y * (x^i y^j)_x = (2*gamma*x*y + c) * i x^{i-1} y^j    =  2i*gamma * x^i y^{j+1} + c*i * x^{i-1} y^j
```

and subtracting gives (†).  ∎

So **every column of `M` meets at most two rows**: the row `(i, j+1)` with entry
`(j - 2i) gamma`, and the row `(i-1, j)` with entry `-c i`.  For `i = j = 0` both
entries vanish: the column of the constant term of `Q` is identically zero.

`prove19.py` §(A) compares (†), monomial by monomial, with the bracket computed
by honest polynomial multiplication in `mate19.bracket`, for all 496 monomials
with `i + j <= 30`: **they agree**.

### 1.2 What a certificate is

Over a field, `M q = e` is solvable **iff** there is no `lambda` with
`lambda^T M = 0` and `lambda^T e_{(0,0)} = 1` (Fredholm alternative for a linear
system: `e` lies in the column space iff every functional annihilating the
column space annihilates `e`).  Such a `lambda` is a *certificate* of the EMPTY
verdict, and it is checkable by pure expansion, with no reference to how it was
found.

---

## 2. The theorem, and its proof

> **Theorem.**  Let `k` be a field of characteristic 0, `gamma in k^*`,
> `c in k`, and `P = gamma x y^2 + c y`.  Then there is **no** polynomial
> `Q in k[x, y]` with `[P, Q] = 1` — of any degree whatsoever.

### 2.1 The functional

Define a `k`-linear functional `Lambda` on `k[x, y]` on the monomial basis:

```
    Lambda( x^a y^b )  =  0                                    if a != b,
    Lambda( (x y)^n )  =  lambda_n  :=  (-1)^n c^n / ( (n+1) gamma^n ) ,   n >= 0.
```

`lambda_0 = 1`.  This is well defined on all of `k[x,y]` (a linear map is
determined by arbitrary values on a basis), and `Lambda(F)` is a **finite** sum
for every polynomial `F`: no convergence question arises.  The denominators
`n + 1` are invertible because `char k = 0`, and the denominators `gamma^n`
because `gamma != 0`.

Equivalently, `lambda_n` is the unique solution of

```
    lambda_0 = 1 ,        lambda_{n+1}  =  - c (n+1) lambda_n / ( (n+2) gamma ) .     (‡)
```

*Check.*  `(-1)^{n+1} c^{n+1} / ((n+2) gamma^{n+1})` equals
`-c(n+1)/((n+2) gamma) * (-1)^n c^n/((n+1) gamma^n)` after cancelling `(n+1)`. ∎

### 2.2 `Lambda` annihilates the image of `[P, -]`

> **Proposition.**  `Lambda( [P, x^i y^j] ) = 0` for every `i, j >= 0`.

*Proof.*  By (†),

```
    Lambda( [P, x^i y^j] )  =  (j - 2i) * gamma * Lambda( x^i y^{j+1} )
                               -  c * i * Lambda( x^{i-1} y^j ) .
```

`Lambda(x^i y^{j+1})` is nonzero only if `i = j + 1`.  `Lambda(x^{i-1} y^j)` is
nonzero only if `i - 1 = j`, i.e. again `i = j + 1`.  The two conditions are
**the same**, so:

*Case A, `i != j + 1`.*  Both terms are 0, and the sum is 0.

*Case B, `i = j + 1`.*  Write `j = n`, `i = n + 1` (`n >= 0`); note
`i - 1 = n` and `j + 1 = n + 1`, so both `Lambda` values sit on the diagonal.
Here `j - 2i = n - 2(n+1) = -(n+2)`, so

```
    Lambda( [P, x^{n+1} y^n] )  =  -(n+2) * gamma * lambda_{n+1}  -  c (n+1) * lambda_n .
```

Substituting the closed form,

```
   -(n+2)*gamma * (-1)^{n+1} c^{n+1} / ((n+2) gamma^{n+1})  =  -(-1)^{n+1} c^{n+1}/gamma^n  =  (-1)^n c^{n+1}/gamma^n
   -c(n+1) * (-1)^n c^n / ((n+1) gamma^n)                   =  -(-1)^n c^{n+1}/gamma^n
```

and the two cancel:  `Lambda([P, x^{n+1} y^n]) = 0`.  (This is exactly the
recursion (‡) rearranged.)  ∎

Note that the case split is over **all** `(i, j)` in `Z_{>=0}^2`; no degree
bound was used anywhere.

### 2.3 Conclusion

Suppose `Q in k[x,y]` satisfies `[P, Q] = 1`.  Write `Q = sum q_{ij} x^i y^j`, a
**finite** sum.  `[P, -]` is `k`-linear in its second argument, so

```
    1  =  [P, Q]  =  sum_{ij} q_{ij} [P, x^i y^j] ,
```

and applying the linear functional `Lambda` to both sides,

```
    Lambda(1)  =  sum_{ij} q_{ij} * Lambda( [P, x^i y^j] )  =  0
```

by the Proposition (a finite sum of zeros).  But `Lambda(1) = Lambda((xy)^0)
= lambda_0 = 1`.  So `1 = 0` in `k`, a contradiction.  Hence no such `Q`
exists.  ∎

### 2.4 The same statement in carrier form, with the boundary spelled out

For a fixed `D`, let `lambda^{(D)}` be `Lambda` restricted to the row index set
of `M`.  Then `lambda^{(D)}` is exactly night18's closed form:

**(a) The support cut is forced by the row set.**  By (†) the rows met by the
column `(i, j)` are `(i, j+1)` of total degree `i + j + 1 <= D + 1` and
`(i-1, j)` of total degree `i + j - 1 <= D - 1`.  So every row of `M` has total
degree `<= D + 1`, and a diagonal row `(n, n)` can occur only when
`2n <= D + 1`, i.e.

```
    n  <=  floor( (D + 1) / 2 )  =:  N(D) .
```

Outside that range `Lambda`'s values are simply not entries of `lambda^{(D)}`.
This is the cut `n <= floor((D+1)/2)` of night18 §5.3 — and it is `floor(D/2)`
only when `D` is even, which is the instrument error night18 recorded.

**(b) Every diagonal row up to the cut really is a row.**  For `1 <= n <= N(D)`,
the column `(n, n-1)` lies in `S(D)` (its degree is `2n - 1 <= D`, because
`2n <= D + 1`) and by (†) it meets the row `(n, n)` with entry
`((n-1) - 2n) gamma = -(n+1) gamma != 0`.  The row `(0, 0)` is the target row and
is present by construction.  So `supp lambda^{(D)}` is contained in the row set,
with no phantom entries.  (`prove19.py` checks this at every `D` as the column
`supp_are_rows`.)

**(c) Every column of `S(D)` is covered.**  §2.2 is a computation over all
`(i, j)` with no upper bound, so in particular over all `(i, j) in S(D)`.  The
only place where the truncation could bite is Case B with `n + 1 > N(D)`, i.e.
the column `(i, j) = (N(D) + 1, N(D))`, whose vanishing needs the entry
`lambda_{N(D)+1}` that `lambda^{(D)}` does not carry.  That column is **not in
`S(D)`**: its total degree is `2 N(D) + 1`, which is `D + 1` when `D` is even
and `D + 2` when `D` is odd — in both cases `> D`.  **No column of any carrier
is left uncovered.**

So for every `D >= 0`, `lambda^{(D)T} M = 0` on every column of `S(D)` and
`lambda^{(D)T} e_{(0,0)} = 1`: the system is inconsistent at every carrier.

### 2.5 Exactly what the result covers, and what it does not

* It covers `P = gamma x y^2 + c y` over any field of characteristic 0, for
  **every** `gamma != 0` and **every** `c` (including `c = 0`, where `P` is not
  unimodular — the certificate does not care).  `gamma != 0` is needed
  (`gamma^n` in the denominator); `char k = 0` is needed (`n + 1` in the
  denominator), so **nothing is claimed in characteristic `p`**.
* Because the carrier `S(D)` with `D` arbitrary exhausts `k[x,y]`, and §2.4(c)
  shows no column of any carrier escapes the certificate, the carrier-relative
  statement upgrades to the absolute one: **`P` has no polynomial mate of any
  degree.**  Equivalently: `P` is not the first component of any polynomial map
  `(P, Q): A^2 -> A^2` of Jacobian 1.
* By §3 below (`cor19.py`, Lemmas L1/L3) the same holds for every member of
  night18's `deg h = 1` stratum, since an explicit Jacobian-1 translation-shear
  carries it to this slice up to an additive constant.
* It is **not** a statement about `deg h >= 2` members (the shear used in L3 has
  `deg h <= 1`), nor about any other stratum, nor about the Jacobian conjecture.
  `P` is unimodular and non-coordinate (C3), so it is a point where the
  Jacobian conjecture's hypothesis on a *pair* is not even reachable; that is a
  statement about `P` alone, not about pairs in general.

---

## 3. Transport along Jacobian-1 moves (`cor19.py`, verbatim from `cor19_log.txt`)

```
==============================================================================
L1  Jacobian-1 invariance of the bracket
==============================================================================
  T = (x + (x**2 - 5*x + y)**3, x**2 - 5*x + y) ,  det J(T) = 1
  [P o T, Q o T] - ([P,Q] o T) expands to 0   (must be 0)

==============================================================================
L3  the explicit move to the slice, over Q(gamma, a, alpha, h0, h1)
==============================================================================
  P o T - ( gamma x y^2 + h(a) y ) = -alpha/(4*gamma)
  is it free of x and y (i.e. a constant)? True

TRANSPORT CHECKS PASS
```

**L1** is the general invariance `[P o T, Q o T] = ([P, Q]) o T` for
`det J(T) = 1`; hence `P` has a mate iff `P o T` has one, and adding a constant
to `P` changes nothing.  **L3** exhibits the explicit move for night18's
`deg h = 1` stratum: `T(x, y) = (x + a, y - h1/(2 gamma))` has Jacobian 1 and

```
    P o T  =  gamma x y^2 + h(a) y  -  alpha / (4 gamma) ,        h(a) = h0 + h1 a ,
```

checked symbolically over `Q(gamma, a, alpha, h0, h1)`.  Combined with §2:

> **Corollary.**  Every member of the `HE`, `deg g = 1`, `deg h = 1` stratum of
> `night18/FAMILY.md` (5 parameters, `gamma != 0`) has **no polynomial mate of
> any degree**.

(The additive constant `-alpha/(4 gamma)` is invisible to the bracket, which is
why `alpha` never appeared in any night18 certificate.)

---

## 4. Machine verification, `D = 2 .. 60`, over `Q(gamma, c)`

`prove19.py` writes the closed form down from the formula — not from any
elimination — builds `M` by honest polynomial multiplication, and checks
`lambda^T M = 0` on **every** column and `lambda^T e = 1` over the field
`Q(gamma, c)`, plus the support-inside-the-row-set condition of §2.4(b).

| `D` | unknowns | equations | `|supp lambda|` | supp are rows | verified over `Q(gamma,c)` | secs |
|---|---|---|---|---|---|---|
| 2 | 6 | 8 | 2 | True | **True** | 0.04 |
| 3 | 10 | 12 | 3 | True | **True** | 0.08 |
| 4 | 15 | 18 | 3 | True | **True** | 0.14 |
| 5 | 21 | 26 | 4 | True | **True** | 0.21 |
| 6 | 28 | 33 | 4 | True | **True** | 0.28 |
| 7 | 36 | 42 | 5 | True | **True** | 0.39 |
| 8 | 45 | 53 | 5 | True | **True** | 0.51 |
| 9 | 55 | 63 | 6 | True | **True** | 0.64 |
| 10 | 66 | 75 | 6 | True | **True** | 0.87 |
| 11 | 78 | 89 | 7 | True | **True** | 0.9 |
| 12 | 91 | 102 | 7 | True | **True** | 1.06 |
| 13 | 105 | 117 | 8 | True | **True** | 1.31 |
| 14 | 120 | 134 | 8 | True | **True** | 1.49 |
| 15 | 136 | 150 | 9 | True | **True** | 1.67 |
| 16 | 153 | 168 | 9 | True | **True** | 1.99 |
| 17 | 171 | 188 | 10 | True | **True** | 2.18 |
| 18 | 190 | 207 | 10 | True | **True** | 2.32 |
| 19 | 210 | 228 | 11 | True | **True** | 2.66 |
| 20 | 231 | 251 | 11 | True | **True** | 2.9 |
| 21 | 253 | 273 | 12 | True | **True** | 3.3 |
| 22 | 276 | 297 | 12 | True | **True** | 3.66 |
| 23 | 300 | 323 | 13 | True | **True** | 3.96 |
| 24 | 325 | 348 | 13 | True | **True** | 4.23 |
| 25 | 351 | 375 | 14 | True | **True** | 4.7 |
| 26 | 378 | 404 | 14 | True | **True** | 5.13 |
| 27 | 406 | 432 | 15 | True | **True** | 5.49 |
| 28 | 435 | 462 | 15 | True | **True** | 6.07 |
| 29 | 465 | 494 | 16 | True | **True** | 6.44 |
| 30 | 496 | 525 | 16 | True | **True** | 7.09 |
| 31 | 528 | 558 | 17 | True | **True** | 7.46 |
| 32 | 561 | 593 | 17 | True | **True** | 8.05 |
| 33 | 595 | 627 | 18 | True | **True** | 8.67 |
| 34 | 630 | 663 | 18 | True | **True** | 9.18 |
| 35 | 666 | 701 | 19 | True | **True** | 9.68 |
| 36 | 703 | 738 | 19 | True | **True** | 9.96 |
| 37 | 741 | 777 | 20 | True | **True** | 10.99 |
| 38 | 780 | 818 | 20 | True | **True** | 11.31 |
| 39 | 820 | 858 | 21 | True | **True** | 11.71 |
| 40 | 861 | 900 | 21 | True | **True** | 13.19 |
| 41 | 903 | 944 | 22 | True | **True** | 13.49 |
| 42 | 946 | 987 | 22 | True | **True** | 14.0 |
| 43 | 990 | 1032 | 23 | True | **True** | 14.8 |
| 44 | 1035 | 1079 | 23 | True | **True** | 15.83 |
| 45 | 1081 | 1125 | 24 | True | **True** | 16.46 |
| 46 | 1128 | 1173 | 24 | True | **True** | 17.52 |
| 47 | 1176 | 1223 | 25 | True | **True** | 18.37 |
| 48 | 1225 | 1272 | 25 | True | **True** | 19.49 |
| 49 | 1275 | 1323 | 26 | True | **True** | 20.1 |
| 50 | 1326 | 1376 | 26 | True | **True** | 20.22 |
| 51 | 1378 | 1428 | 27 | True | **True** | 21.44 |
| 52 | 1431 | 1482 | 27 | True | **True** | 22.0 |
| 53 | 1485 | 1538 | 28 | True | **True** | 23.1 |
| 54 | 1540 | 1593 | 28 | True | **True** | 24.49 |
| 55 | 1596 | 1650 | 29 | True | **True** | 26.75 |
| 56 | 1653 | 1709 | 29 | True | **True** | 29.59 |
| 57 | 1711 | 1767 | 30 | True | **True** | 30.73 |
| 58 | 1770 | 1827 | 30 | True | **True** | 32.41 |
| 59 | 1830 | 1889 | 31 | True | **True** | 32.32 |
| 60 | 1891 | 1950 | 31 | True | **True** | 33.47 |

`all_verified = True` (`prove19.json`).  Row-formula check: True (496 monomials, `i+j <= 30`).

---

## 5. The mechanism: why *this* `P` has no mate

Three descriptions of the same fact; all three are checked in `mech19.py`
(`mech19_log.txt`).

### 5.1 Combinatorial: two terms ⟹ the incidence graph is a forest

For a general `P = sum_{(a,b) in A} p_{ab} x^a y^b`,

```
    [P, x^i y^j]  =  sum_{(a,b) in A} p_{ab} * (a j - b i) * x^{a+i-1} y^{b+j-1} .      (‡‡)
```

(Checked in `broken19.py` against expanded brackets on 637 (case, monomial)
pairs.)  So the column `(i, j)` meets the translates of `(i, j)` by the **shift
vectors** `s_{ab} = (a-1, b-1)`, with coefficient `p_{ab}(a j - b i)`, which
vanishes exactly on the ray `a j = b i`.

When `|A| = 2` every column meets **at most two** rows, so the columns are
*edges* of a graph whose vertices are the rows — and all edges are the *same*
translation `delta = (a_2 - a_1, b_2 - b_1)`.  A graph all of whose edges are one
fixed translation of `Z^2` is a disjoint union of paths: it has **no cycles**.
`lambda^T M = 0` then says: assign potentials to vertices with a prescribed ratio
across each edge — always integrable on a forest.  The only way it can fail is
the *forced zeros*: a column meeting only one row forces that row's `lambda` to
be 0, and this can propagate to the row `(0, 0)`, where `lambda` must be 1.  That
is exactly what happens for the coordinate `x + y^2` (also a two-term `P`), and
it is what does **not** happen here.  `broken19.py` measures the cycle rank of
the bipartite incidence graph on `S(12)` and the forced-zero propagation: for
`P = gamma x y^2 + c y` the cycle rank is **0** and the forced zeros do **not**
reach `(0, 0)`.

For this `P` the forced zeros are, explicitly, the rows `(0, k)` for `k >= 2`
(from the columns `(0, j)`, `j >= 1`, which lose their second term because
`i = 0`) and the rows `(i-1, 2i)` for `i >= 1` (from the columns `j = 2i`, which
lose their first term because `j - 2i = 0`).  Neither family meets the diagonal
`{(n, n)}`, which is why the diagonal certificate survives.

### 5.2 Graded: `P` is isobaric for the mixed weight `w = (-1, +1)`

Both monomials of `P` — `x y^2` and `y` — have `w`-weight `j - i = 1`.  So `P`
is quasi-homogeneous for the weight `w(x) = -1`, `w(y) = +1`, and (checked on
every carrier monomial with `i + j <= 10`) `[P, -]` raises `w`-weight by exactly
`1`.  Since the target `1` has `w`-weight `0`, only the `w`-weight `(-1)` part of
`Q` can matter, and

```
    { monomials of w-weight -1 }  =  { x^{m+1} y^m : m >= 0 }
    { monomials of w-weight  0 }  =  { (x y)^n : n >= 0 }
```

are both **one-parameter chains**.  The whole mate problem collapses to a scalar
recursion in one index — which is why the certificate is diagonal, one-step, and
uniform in `D`.  This is the sharp point: the weight `w` has **mixed signs**, so
its weight-0 piece is an infinite ray with no upper end and the recursion has
nowhere to terminate.  For `x + y^2` the isobaric weight is `w = (2, 1)`, with
both signs **positive**: the graded pieces are finite-dimensional and the
recursion terminates — hence a mate.

### 5.3 Analytic: the recursion, the non-terminating tail, and the rational mate

Writing the weight-`(-1)` part of `Q` as `sum_m q_m x^{m+1} y^m`, (†) turns
`[P, Q] = 1` into

```
    -c q_0 = 1                       (coefficient of (xy)^0)
    -gamma (m+1) q_{m-1} - c (m+1) q_m = 0      (coefficient of (xy)^m, m >= 1)
```

i.e. `q_0 = -1/c` and `q_m = -(gamma/c) q_{m-1}`, so
`q_m = -(1/c) (-gamma/c)^m` — **never zero**.  The recursion never terminates,
so no polynomial `Q` can satisfy it.  `mech19.py` makes the failure explicit:
for the truncation `Q_N = sum_{m <= N} q_m x^{m+1} y^m`,

```
    [P, Q_N] - 1  =  - gamma (N + 2) q_N (x y)^{N+1}   != 0    for every N,
```

verified symbolically for `N = 0 .. 12`.  The unique formal solution sums to a
**rational** mate,

```
    Q_inf  =  - x / ( gamma x y + c ) ,          [P, Q_inf] = 1   (verified exactly),
```

whose polar locus `{ gamma x y + c = 0 }` is precisely the second component of
the **reducible zero fibre** `P = y (gamma x y + c)`.  That component is
isomorphic to `A^1` minus a point, not to `A^1`.  So: `P` does have a mate, but
only after inverting the equation of one component of its own zero fibre, and
`Lambda` is exactly the functional that detects the pole.

---

## 6. The design constraint, and the deliberately broken cases

### 6.1 The constraint

From §5.1: **for the certificate construction of §2 to have a chance of failing,
`P` must not have a two-term support** (and, more generally, must not have a
support lying on a line — see K3 below), because

* `|A| = 2`  ⟹  every column meets ≤ 2 rows  ⟹  the row graph is a disjoint
  union of translates by one fixed vector  ⟹  **no cycles**  ⟹  the ratio
  constraints are always integrable, and the only obstruction to the certificate
  is the forced-zero propagation reaching `(0,0)`;
* supports on a line (any `|A|`) still admit an isobaric weight `w` orthogonal to
  that line, so `[P,-]` is still graded and the problem still collapses to a
  chain in one index.

So the property to **avoid**, if one wants this construction to fail, is:
*the support `A` lies on a line* (equivalently: the differences `A - A` span a
rank-1 lattice; equivalently: `P` is quasi-homogeneous).  Breaking it means
taking `A` whose difference lattice has **rank 2**: then columns meet three or
more rows, they are hyperedges rather than edges, the bipartite incidence graph
acquires cycles, and no one-step scalar recursion is available.

A caveat we record because it changes the reading: a scalar *holonomy* around a
cycle is defined only when every column meets exactly two rows — i.e. only in the
rank-1 case, where there are no cycles to go around.  When the difference lattice
has rank 2 the columns are hyperedges and there is no scalar transport; the
honest analogue of "is the holonomy trivial" is the linear-algebra question
itself, which we therefore decide exactly.  What we report per case is: the rank
of the difference lattice, the maximum number of rows per column, the **cycle
rank** (first Betti number) of the bipartite incidence graph on `S(12)`, and the
exact verdict with a re-verified `lambda`.

### 6.2 The cases

Seven polynomials (the base `K0` and six deformations), each certified **unimodular** (`(P_x, P_y) = (1)` by Gröbner
basis, plus an explicit Bézout identity `U P_x + V P_y = 1` found by exact
linear algebra with **zero** residual) and **non-coordinate** (Shpilrain–Yu via
`night14/sy14.py`, plus a reducible-zero-fibre witness).

```
| case | `P` | `|A|` | shift differences | rank | max rows/col | cycle rank on `S(12)` | forest | Bezout resid | SY | fibre | verdicts `D = 3,5,7,9,11,13,15` | `|supp lambda|` | diagonal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K0 | `x*y**2 + y` | 2 | [[1, 1]] | 1 | 2 | 0 | True | 0 | NON_COORDINATE | `y*(x*y + 1)` | EMPTY_over_Q | 3, 4, 5, 6, 7, 8, 9 | Y, Y, Y, Y, Y, Y, Y |
| K1 | `x**2*y + x` | 2 | [[1, 1]] | 1 | 2 | 0 | True | 0 | NON_COORDINATE | `x*(x*y + 1)` | EMPTY_over_Q | 3, 4, 5, 6, 7, 8, 9 | Y, Y, Y, Y, Y, Y, Y |
| K2 | `x*y**3 + y` | 2 | [[1, 2]] | 1 | 2 | 0 | True | 0 | NON_COORDINATE | `y*(x*y**2 + 1)` | EMPTY_over_Q | 2, 3, 4, 4, 5, 6, 6 | n, n, n, n, n, n, n |
| K3 | `x**2*y**3 + x*y**2 + y` | 3 | [[1, 1], [2, 2]] | 1 | 3 | 59 | n/a (|A|>2) | 0 | NON_COORDINATE | `y*(x**2*y**2 + x*y + 1)` | EMPTY_over_Q | 3, 3, 4, 5, 5, 6, 7 | Y, Y, Y, Y, Y, Y, Y |
| K4 | `x*y**2 + y**2 + y` | 3 | [[0, 1], [1, 1]] | 2 | 3 | 52 | n/a (|A|>2) | 0 | NON_COORDINATE | `y*(x*y + y + 1)` | EMPTY_over_Q | 5, 9, 12, 19, 27, 30, 41 | n, n, n, n, n, n, n |
| K5 | `x*y**2 + y**3 + y` | 3 | [[0, 2], [1, 1]] | 2 | 3 | 51 | n/a (|A|>2) | 0 | NON_COORDINATE | `y*(x*y + y**2 + 1)` | EMPTY_over_Q | 3, 6, 9, 10, 15, 20, 21 | n, n, n, n, n, n, n |
| K6 | `x*y**2 + y**3 + y**2 + y` | 4 | [[0, 1], [0, 2], [1, 1]] | 2 | 4 | 128 | n/a (|A|>2) | 0 | NON_COORDINATE | `y*(x*y + y**2 + y + 1)` | EMPTY_over_Q | 5, 9, 14, 19, 27, 28, 41 | n, n, n, n, n, n, n |

(`forest` = the row graph with columns as edges is acyclic, defined only for `|A| = 2`;
`diagonal` = `lambda` is supported on `{(n,n)}`, i.e. the closed-form shape;
`Bezout resid` = number of terms of `U P_x + V P_y - 1`, which must be 0;
all `lambda` re-verified by expansion: `lambda_verified = True` in every row.)
```

Full output, including the Bézout cofactors and every `lambda`, is in
`broken19_log.txt` / `broken19.json`.

### 6.3 What the broken cases measured

* **Rank-1 supports (`K0`, `K1`, `K2`, `K3`).**  Cycle rank 0 when `|A| = 2`.
  The certificate not only exists but keeps a **closed form on a line**: for
  `K1 = x + x^2 y` it is again the diagonal `lambda_{n,n} = (-1)^n/(n+1)`; for
  `K2 = y + x y^3` (shift difference `(1,2)`) it moves to the line `(n, 2n)`
  with `lambda_{n,2n} = (-1)^n * 2 / ((n+1)(n+2))`; for the three-term rank-1
  `K3 = y + x y^2 + x^2 y^3` it is diagonal with the entries at `n = 1 mod 3`
  dropped.  (These shapes are read off from the solved `lambda` at the carriers computed, `D <= 15`; the entries are in `broken19.json`.  Support grows like `D/2`.)  So *the certificate construction of §2
  survives every rank-1 deformation we built* — as predicted.
* **Rank-2 supports (`K4`, `K5`, `K6`).**  Cycle rank of the bipartite
  incidence graph on `S(12)` jumps to 52, 51, 128; columns meet 3 or 4 rows;
  the diagonal/line shape is **destroyed** (`lambda_is_diagonal = False` at
  every carrier), and the support of `lambda` grows roughly like the number of
  rows (`|supp| = 41` at `D = 15` for `K4` and `K6`, against `9` for `K0`).
  **A certificate still exists at every carrier tested** — it is just no longer
  a closed form.  So rank 2 breaks the *construction*, not the *conclusion*, on
  these examples.
* Every `lambda` reported was re-verified by expansion (`lambda_verified = True`
  in all rows).
* No statement here is all-`D` except for `K0` (§2); the rank-2 rows are
  carrier-relative, `D <= 15`.

---

## 7. Hit-gate status

**No mate system was consistent.**  Every solve in §6 returned `EMPTY_over_Q`
with a `lambda` verified by exact expansion; the consistency detector was shown
to work on two coordinates in control C1 (`x + y^2` and the degree-10
composition), where it returns the mate with zero residual and no `lambda`.
`night19/HIT_<hash>/` was therefore never written.

---

## 8. Measurements

**N1.**  The row formula (†) is proved and machine-checked against expanded
brackets on all 496 monomials of `S(30)`.

**N2.**  The functional `Lambda(x^a y^b) = [a = b] (-1)^a c^a/((a+1) gamma^a)`
annihilates `[P, x^i y^j]` for **every** `(i, j) in Z_{>=0}^2` and has
`Lambda(1) = 1`; hence `P = gamma x y^2 + c y` has **no polynomial mate of any
degree**, over any field of characteristic 0 with `gamma != 0`.  Proof in §2;
the carrier-by-carrier form, with the boundary column `(N(D)+1, N(D))` shown to
lie outside `S(D)`, in §2.4.

**N3.**  Machine verification of the closed form over `Q(gamma, c)` at
`D = 2 .. 60` — 59 carriers, up to 1891 unknowns and 1953 equations — all
verified, including the check that `lambda`'s support consists of genuine rows.

**N4.**  Controls: C1 (mate found on two coordinates, no `lambda` there),
C2 (the closed form re-checked over `Q` alone at 7 rational `(gamma, c)` and 6
carriers, 42 rows), C3 (exact Bézout `U = 4 gamma x^2/c^2`,
`V = (c - 2 gamma x y)/c^2` with residual 0 over `Q(gamma, c)`; Shpilrain–Yu
`NON_COORDINATE` at 7 rational points, `COORDINATE` on the two C1 coordinates;
reducible zero fibre `y (gamma x y + c)`).

**N5.**  Transport: `[P o T, Q o T] = [P,Q] o T` for `det J(T) = 1`, and the
explicit `T(x,y) = (x + a, y - h1/(2 gamma))` carrying night18's `deg h = 1`
stratum onto the slice up to the additive constant `-alpha/(4 gamma)`.  Hence
that entire 5-parameter stratum is mateless at all degrees.

**N6.**  Mechanism: `P` is isobaric for the mixed weight `w = (-1, +1)`, the
mate problem collapses to the scalar recursion `q_m = -(gamma/c) q_{m-1}` whose
solution never vanishes, every truncation leaves the residual
`-gamma(N+2) q_N (xy)^{N+1} != 0`, and the unique formal solution is the
rational mate `-x/(gamma x y + c)` with poles on a component of the reducible
zero fibre `y(gamma x y + c)`.

**N7.**  Design constraint and its test: the construction needs the support of
`P` to lie on a line.  Six certified unimodular non-coordinate polynomials were
built, four with rank-1 support and three (`K4`, `K5`, `K6`) with rank-2
support.  Rank 1 keeps a closed-form `lambda` on a line; rank 2 destroys the
closed form (cycle rank 52 / 51 / 128, `lambda` support growing like the row
count) but a certificate **still exists** at every carrier tested, so all seven
verdicts are `EMPTY_over_Q`.

**N8.  What is NOT measured.**  Nothing here is a statement about the Jacobian
conjecture; nothing here concerns characteristic `p`; the rank-2 cases of §6 are
carrier-relative (`D <= 15`) and no all-`D` claim is made for them; and the
`deg h >= 2` members of night18's stratum are not covered by §3, since the shear
used there requires `deg h <= 1`.
