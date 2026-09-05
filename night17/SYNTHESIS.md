# night17 — THE INVERTED SEARCH: SOLVING FOR P

Instead of generating gradient-unimodular non-coordinate `P` and filtering them
through the period screen, this lane writes the period screen down as a system
of POLYNOMIAL EQUATIONS in the coefficients of `P` on a fixed support, solves
that system, and only then applies the certificates. Measurements only.

---

## 1. The residue equations

### 1.1 What has to vanish

night15/PERIODS.md derives the necessary condition. With `[P,Q] = 1` the
Gelfand–Leray form

    eta = dy / P_x = - dx / P_y

restricts on every fibre `F_c = {P = c}` to `dQ|_{F_c}`, hence is exact, hence
has zero period on every cycle of `F_c`. Two consequences are used here:

* a period around a puncture is `2 pi i` times the RESIDUE of `eta` there, so
  every residue at every place at infinity of every fibre must vanish;
* on a **genus-0** fibre those punctures carry all of `H_1`, so vanishing
  residues are equivalent to vanishing periods; on a fibre of **genus >= 1**
  vanishing residues are necessary but not sufficient, and this lane records
  such fibres as `UNDECIDED_BY_RESIDUES` rather than claiming either way.

### 1.2 The residue rule

For the shapes used here `eta` is a RADICAL DIFFERENTIAL in `x` alone,

    eta / dx  =  C * prod_i f_i(x)^(alpha_i),    alpha_i in Q,  C != 0.

*At a finite point `b`.* Write `f_i = (x-b)^(n_i) h_i` with `h_i(b) != 0`, put
`w = sum_i alpha_i n_i`, and let `r` be the ramification index of `x` at the
place. With `x - b = tau^r`, `dx = r tau^(r-1) dtau`, the order-`k` term of the
analytic part contributes `tau^(r(w+k)+r-1)`, which is `tau^(-1)` exactly when
`k = -w-1`. Hence

    residue = 0  unless w is an INTEGER <= -1,  and then
    residue = r * (prod_i h_i(b)^(alpha_i)) * [t^(-w-1)] prod_i (h_i(b+t)/h_i(b))^(alpha_i).

*At infinity.* With `u = 1/x`, `W = sum_i alpha_i deg f_i`, and
`F_i(u) = u^(deg f_i) f_i(1/u)` (so `F_i(0) = lc(f_i) != 0`),
`eta = - u^(-W-2) prod F_i(u)^(alpha_i) du`, and the same count gives

    residue = 0  unless W is an INTEGER >= -1,  and then
    residue = -r_inf * (prod lc(f_i)^(alpha_i)) * [u^(W+1)] prod (F_i/lc_i)^(alpha_i).

**Two things make this into algebra.** First, the prefactors
`r * prod h_i(b)^(alpha_i)` are nonzero — they are where all the roots of unity
and radicals live — so the residue vanishes **iff the bracketed Taylor
coefficient vanishes**, and that coefficient is a rational function of the
coefficients of `P`, of `b`, and of the fibre parameter, with a denominator
that is a power of a nonzero leading value. Clearing that denominator turns
"all residues vanish" into POLYNOMIAL EQUATIONS. Second, the exponent test
(`w` an integer `<= -1`; `W` an integer `>= -1`) is decided by the SUPPORT
alone, so on most supports most places are residue-free identically and
contribute no equation at all.

The implementation is `res17.py` (`residue_at_finite`, `residue_at_infinity`,
`series_coeff`); it is a reimplementation in this lane, sharing no code with
night15.

### 1.3 The two shapes

**HE — `deg_y P = 2`.** `P = g(x) y^2 + h(x) y + k(x)`, `w := P_y = 2gy+h`,

    w^2 = Delta_c := h^2 - 4 g k + 4 g c,       eta = - dx / Delta_c^(1/2),

so `eta/dx = Delta_c^(-1/2)` up to sign: one factor, `alpha = -1/2`.

* At a root of `Delta_c` of multiplicity `mu`: `w = -mu/2`, an integer `<= -1`
  iff `mu` is EVEN and `>= 2`. A **squarefree** `Delta_c` therefore has **no
  finite residues at all**.
* At infinity: `W = -deg(Delta_c)/2`, an integer `>= -1` iff `deg Delta_c` is
  even and `<= 2`. For `deg Delta_c = 0` the series is `1` and the coefficient
  of `u^1` is `0`; for `deg Delta_c = 2` the coefficient of `u^0` is `1`, so
  the residue is NONZERO. (This reproduces night15 EXACT-HE cases B, C, D.)
* Genus of the smooth model is `floor((deg Delta_0 - 1)/2)` with `Delta_0` the
  squarefree part.

Two facts about the stratification, proved below in 3.1, are used: under
gradient-unimodularity `Delta_c` has a multiple root only over a root of `g`,
and on the stratum this lane solves in, `Delta_c` is squarefree for every `c`.
So on that (open, generic) stratum

> **RES(HE):  all periods vanish  <=>  deg_x Delta_c <= 1 for every c
>  <=>  [x^j] g = 0 for j >= 2  and  [x^j](h^2 - 4 g k) = 0 for j >= 2.**

The `g`-equations come from the `4 g c` term: requiring the condition for EVERY
`c` kills the coefficients of `g` above degree 1 separately. The remaining
equations are QUADRATIC in the `h_i` and BILINEAR in `(g_i, k_j)`, and they are
LINEAR in the `k_j` with triangular leading terms `-4 g_top k_j` — which is
what makes the solution variety rational and explicitly parametrisable.

**SE — `P = A(x) + B(x) y^m`, `m >= 2`.** On `{P = lam}`, `y^m = (lam-A)/B` and
`P_y = m B y^(m-1)`, so

    eta = - y dx / (m (lam - A)) = -(1/m) (lam-A)^((1-m)/m) B^(-1/m) dx :

two factors, `alpha = ((1-m)/m, -1/m)`. With `p = deg A`, `q = deg B` and
`B = c prod (x-a_i)^(e_i)`:

* at a root `a_i` of `B` (a puncture, `y -> infinity`): `w = -e_i/m`, so a
  residue can be nonzero only when **`m | e_i` and `e_i >= m`**, and then the
  equation is the vanishing of `[t^(e_i/m - 1)]` of an explicit analytic
  product;
* at a root of `lam - A` (an affine point, `y = 0`): for generic `lam` the root
  is simple and `w = (1-m)/m` is not an integer — no residue, ever;
* at infinity: `W = -(p(m-1)+q)/m`, so a residue can be nonzero only when
  `m | p(m-1)+q` and `p(m-1)+q <= m`. In the unimodular case `p = 1` (see 3.2)
  this needs `m | q-1` and `q <= 1`, so for `deg B >= 2` the places over
  `x = infinity` are residue-free identically.

Genus and puncture count come from Riemann–Hurwitz for `y^m = (lam-A)/B`:
`2g - 2 = -2m + sum (m - gcd(m, v))` over the zeros/poles of `(lam-A)/B` on
`P^1` (`v` = order), and the punctures are the places over the `a_i` together
with those over `x = infinity`, `sum_i gcd(m,e_i) + gcd(m, p-q)`.

The `(x,y)` swap negates the bracket and carries SE to `P = A(y) + B(y) x^n`,
which is the night14/night15 **v-power** family `P = h0 y + c x^n y^m`; that
instance is used below both as a support family and as a cross-check.

### 1.4 One honest caveat about closedness

"Every residue vanishes" is not, by itself, a Zariski-CLOSED condition on the
HE supports: it holds either when `deg Delta_c <= 1` or when `deg Delta_c >= 3`
(where the exponent test fails and there is no residue at infinity at all).
The second branch is not a loophole — there `Delta_0` has degree `>= 3`, the
fibre has genus `>= 1`, and residues no longer decide. This lane therefore
imposes the CLOSED system `deg Delta_c <= 1` (residues vanish AND genus 0) as
the working system, and treats the genus `>= 1` branch as its own class of
supports with verdict `UNDECIDED_BY_RESIDUES` handed to NUM-MONO.

---

## 2. Solving the combined system

Unimodularity is not imposed by Rabinowitsch here; it is imposed BY
CONSTRUCTION and then re-certified by an exact Bezout identity
`U P_x + V P_y - 1 = 0` expanded coefficientwise over `Q` with an EMPTY residual
(`certs17.unimodular`, producer EUCLID over `Q(x)[y]` or LINALG over `Q`).
Coordinates are excluded afterwards by Shpilrain–Yu (`certs17.sy`) and,
independently, by a fibre witness: every fibre of a coordinate is isomorphic to
`A^1` (the fibres are the images of the lines `{x = c}` under the automorphism
`(P,Q)`), so a generic fibre of genus `>= 1` or with `>= 2` punctures certifies
NON-COORDINATE.

### 2.1 The HE strata, solved in closed form

Let `Delta = h^2 - 4 g k` and `R := g' Delta - g Delta'`. Multiplying `P_x` by
`4 g^2` and substituting `2 g y = w - h` gives, on `{P_y = 0}` (i.e. `w = 0`),

    4 g^2 P_x = g' h^2 - 2 g h h' + 4 g^2 k' = g' Delta - g Delta' = R(x).      (*)

So `P` has a critical point with `g != 0` exactly when `R` has a root off
`V(g)`; over a root `a` of `g` one has `P_y(a, y) = h(a)`, so a critical point
there needs `h(a) = 0` as well. In particular (*) also shows that a multiple
root of `Delta_c` off `V(g)` IS a critical point, so **for unimodular `P` the
polynomial `Delta_c` can only be non-squarefree over roots of `g`.**

**Stratum `deg g = 0` (`g = gamma`).** RES(HE) says `Delta = alpha x + beta`.
Then `R = -gamma alpha`, so unimodularity `<=>` `alpha != 0`. And then, with
`w = 2 gamma y + h`,

    4 gamma P = w^2 - Delta = w^2 - alpha x - beta,
    x = (w^2 - 4 gamma P - beta)/alpha,   y = (w - h(x))/(2 gamma),

so `(x,y)` is a polynomial function of `(P,w)`: `(P,w)` is a polynomial
automorphism and **`P` is a COORDINATE.** On this stratum the residue system,
unimodularity and coordinacy therefore coincide: it contributes no survivors,
and it is the stratum that carries the mandatory control (`x + y^2` and the
degree-10 and degree-12 triangular compositions all live here).

**Stratum `deg g = 1` (`g = gamma (x-a)`).** RES(HE) says `Delta = alpha x +
beta`, and the divisibility `4 g | h^2 - (alpha x + beta)` forces
`beta = h(a)^2 - alpha a`, i.e. `Delta(a) = h(a)^2`. Then

    R = gamma (alpha x + beta) - gamma (x-a) alpha = gamma Delta(a) = gamma h(a)^2,

a nonzero constant iff `h(a) != 0`, which is also exactly the condition ruling
out a critical point over the root of `g`. So

> on this stratum **RES(HE) + `h(a) != 0` <=> gradient-unimodular**, with the
> explicit rational parametrisation
>
>     g = gamma (x - a),  h arbitrary,  alpha arbitrary,
>     beta = h(a)^2 - alpha a,  k = (h^2 - alpha x - beta) / (4 gamma (x-a)),
>
> of dimension `deg h + 4` inside the support `HE(1, H, 2H-1)`.

`Delta_c = alpha x + beta + 4 gamma (x-a) c` has degree 1 for all but one `c`,
so the smooth model of the fibre is a line in `w`, genus 0; the affine fibre is
that line minus ONE point — the second point over `x = a`, `w = -h(a)`, where
`y = (w-h)/(2g)` blows up. Hence the **generic fibre is `A^1` minus a point**:
genus 0, TWO punctures, both residues zero. That is simultaneously

* the reason the periods vanish (genus 0, no residues), and
* a fibre witness that `P` is **NOT a coordinate** (a coordinate's fibres are
  `A^1`), independently of Shpilrain–Yu.

The smallest member is `P = x y^2 + y` (up to a shear and a scale); NUM-MONO
confirms 2 punctures and `ls_residual/scale ~ 1e-15` on the fibres tested.

**Stratum `deg g >= 2`.** RES(HE) contains `[x^j] g = 0` for `j >= 2`, so with
`g_top != 0` adjoined the ideal is the unit ideal — no solutions at all. This
is a Groebner measurement, recorded per support in section 4.

### 2.2 The SE supports, solved by the exponent test

Unimodularity for `P = A + B y^m`, `m >= 2`: `P_y = m B y^(m-1)` and
`P_x = A' + B' y^m`. On `{y = 0}` one needs `A'` nowhere zero, so `A' = alpha`
is a nonzero constant and `A = alpha x + beta`; over a root `b` of `B` one needs
`B'(b) = 0`, i.e. every root of `B` is a MULTIPLE root (`e_i >= 2`). Those two
conditions are also sufficient, and they are exactly night15's G2 family.

Given that, section 1.3 leaves **one equation per root `a_i` with `m | e_i`**
and none at infinity. Consequently:

* if `m` divides NO `e_i`, the residue system is EMPTY: *every* point of the
  support is a solution, and the whole (unimodular, `e_i >= 2`) family
  satisfies (c') by construction;
* if some `e_i = m`, the equation is the nonzero constant `1 = 0`: the support
  has NO solutions;
* if some `e_i = 2m`, the equation is `alpha = 0`, which is incompatible with
  unimodularity: again no solutions;
* larger multiples of `m` give genuine polynomial equations in
  `(alpha, beta, c, a_i)`, solved by Groebner per support.

Genus and punctures come from the Riemann–Hurwitz count of 1.3; the supports
with `gcd`s making the genus positive are kept and reported as
`UNDECIDED_BY_RESIDUES`, not as survivors.

---

## 3. Controls — verbatim

Instruments: `res17.py` (residues), `certs17.py` (Bezout + Shpilrain–Yu),
`mate17.py` (exact mate solve), `coord17.py` (coordinate pairs with a verified
mate). Full logs: `controls17_log.txt` / `controls17.json`,
`mate17_control.txt`.

### 3.1 C1 — THE MANDATORY CONTROL (coordinates must satisfy the equations)

```
==============================================================================
C1  MANDATORY CONTROL -- coordinates must SATISFY the residue equations
==============================================================================
HE  x + y^2                          deg=2   deg_y=2  deg Delta_c=1 genus=0  all-res-zero=True  SY=COORDINATE  -> SATISFIES the equations
HE  triangular composition, deg 10   deg=10  deg_y=2  deg Delta_c=1 genus=0  all-res-zero=True  SY=COORDINATE  -> SATISFIES the equations
HE  triangular composition, deg 12   deg=12  deg_y=2  deg Delta_c=1 genus=0  all-res-zero=True  SY=COORDINATE  -> SATISFIES the equations
HE  triangular composition, deg 6    deg=6   deg_y=2  deg Delta_c=1 genus=0  all-res-zero=True  SY=COORDINATE  -> SATISFIES the equations
SE  x + y^2 (coordinate)             genus=0 punctures=1  equations=[]  SY=COORDINATE  -> SATISFIES
SE  x + y^3 (coordinate)             genus=0 punctures=1  equations=[]  SY=COORDINATE  -> SATISFIES
SE  x + y^4 (coordinate)             genus=0 punctures=1  equations=[]  SY=COORDINATE  -> SATISFIES
SE  x + y^5 (coordinate)             genus=0 punctures=1  equations=[]  SY=COORDINATE  -> SATISFIES
```

The three triangular compositions are built by the bracket-preserving moves
`(F,G) -> (F, G+p(F))` and `(F,G) -> (G,-F)` from `(x,y)`, so each comes with an
explicit `Q` for which `[P,Q] - 1 = 0` was expanded coefficientwise over `Q`
and came out identically zero. They are members of the supports H1/H2 (`g`
constant), and in the sweep the same check is repeated at INSTANCE level:
substituting each instance's coefficient vector into that support's residue
equations returned `0` for every equation on every instance, coordinates
included ("by-construction check ... = True" in `run17_log.txt`).

### 3.2 C2 — negatives (a residue that must NOT vanish)

```
    x^2 + y^2 (HE)                                 res_inf = 1              -> NONZERO ok
    x*y (HE, g=x)                                  res_inf = 1              -> NONZERO ok
    y + x^2 y^4 (SE-swap n=2 m=4, night15 witness) equations = ['h0/(2*lam)']   -> NONZERO ok
    y + x^2 y^2 (SE-swap n=2 m=2)                  equations = ['1']            -> NONZERO ok
    y + x^3 y^6 (SE-swap n=3 m=6)                  equations = ['2*h0/(3*lam)'] -> NONZERO ok
```

The `n=2, m=4` row is night15's own instrument-bug witness: EXACT-G1 first
claimed "residue nonzero iff `n = m`", NUM-MONO contradicted it at `n=2, m=4`,
and the corrected rule is `n | m`. This lane's engine, derived independently
from the exponent rule of 1.2, reproduces the corrected rule exactly — nonzero
residue iff `n >= 2`, `m >= n`, `n | m` — on every `(n,m)` tested.

### 3.3 C3 — residues sum to zero

Structural in this engine: the several places over one branch point differ only
by the branch of the radical, i.e. by a root of unity multiplying the nonzero
prefactor, and those roots of unity sum to zero whenever more than one place
lies over the point. Checked numerically as well through C5.

### 3.4 C4 — cross-instrument (HE17 vs SE17 on `P = A(x) + B(x) y^2`)

```
    x + y^2                    SE17: res-zero=True  genus=0 | HE17: res-zero=True  genus=0  -> AGREE
    x + (x-1)^2 y^2            SE17: res-zero=False genus=0 | HE17: res-zero=False genus=0  -> AGREE
    x + (x-1)^3 y^2            SE17: res-zero=True  genus=0 | HE17: res-zero=True  genus=0  -> AGREE
    x + x^2(x-1)^2 y^2         SE17: res-zero=False genus=0 | HE17: res-zero=False genus=0  -> AGREE
    x + (x-1)^4 y^2            SE17: res-zero=False genus=0 | HE17: res-zero=False genus=0  -> AGREE
    x + x^2 (x-1)^3 y^2        SE17: res-zero=False genus=0 | HE17: res-zero=False genus=0  -> AGREE
    x^2 + y^2                  SE17: res-zero=False genus=0 | HE17: res-zero=False genus=0  -> AGREE
```

> **An instrument error found by this control and fixed, recorded because it
> changed answers.** The first HE17 read only the residue at `x = infinity`
> and reported `x + (x-1)^2 y^2` as residue-free, while SE17 reported a nonzero
> residue at the puncture over `x = 1`. SE17 was right: there
> `Delta_c = 4(x-1)^2 (c-x)` has a DOUBLE root, the exponent `w = -1` is an
> integer, and the residue is the (nonzero) leading coefficient. The finite
> places are not optional: the general rule of 1.2 must be applied at every
> branch point, not only at infinity. `res17.he_finite_residues` does that now,
> by factoring `Delta_c` over `Q(c)` and reducing the residue coefficient
> modulo each irreducible factor. All seven rows agree after the fix.

### 3.5 C5 — cross-night numeric (night15 NUM-MONO, imported read-only)

```
    x + y^2 (coordinate)       VANISHING      expect VANISHING      ok   [c=1 rel=3.93e-16 punct=1 g=0; c=-1 rel=3.07e-16 punct=1 g=0]
    x*y^2 + y                  VANISHING      expect VANISHING      ok   [c=1 rel=1.94e-15 punct=2 g=0; c=-1 rel=8.89e-15 punct=2 g=0]
    x^2 + y^2                  NONVANISHING   expect NONVANISHING   ok   [c=1 rel=9.33e-01 punct=2 g=0; c=-1 rel=1.14e+00 punct=2 g=0]
    y + x^2 y^4                NONVANISHING   expect NONVANISHING   ok   [c=1 rel=5.55e-01 punct=3 g=0; c=-1 rel=5.35e-01 punct=3 g=0]
    y + x^2 y^3                VANISHING      expect VANISHING      ok   [c=1 rel=2.11e-14 punct=3 g=0; c=-1 rel=2.11e-14 punct=3 g=0]
    x + (x-1)^3 y^2            VANISHING      expect VANISHING      ok   [c=1 rel=6.34e-16 punct=4 g=0; c=-1 rel=9.82e-15 punct=3 g=0]
```

### 3.6 The mate-solver control (mandatory before any EMPTY is trusted)

```
MATE-SOLVER CONTROL -- recover the mate of a known coordinate
      D=10  n=66    MATE_over_Q      (1.0s)
  coordinate deg 10  (known mate deg 5): MATE_over_Q     ok  [1.0s]
      [P,Q]-1 residual terms = 0 ; deg Q = 5
      D=12  n=91    MATE_over_Q      (2.8s)
  coordinate deg 12  (known mate deg 6): MATE_over_Q     ok  [2.8s]
      [P,Q]-1 residual terms = 0 ; deg Q = 6
  negative control x*y        -> EMPTY_over_Q_all_stages
  negative control x^2 + y^2  -> EMPTY_over_Q_all_stages
CONTROL PASS
```

The solver recovers the mate of a degree-10 and a degree-12 coordinate with a
zero coefficientwise residual, and returns exactly-verified `lambda`
certificates on the two standard negatives.

---

## 4. The sweep

`systems17.py` (systems + Groebner), `sweep17.py` (instance builders, screening,
certificates), `run17.py` (driver), `supp17.py` (three follow-ups),
`deep17.py` (deeper mate escalation). Logs: `run17_log.txt` / `run17_out.txt`,
`supp17_log.txt`, `deep17_out.txt`. Machine-readable: `records17.json`,
`supp17.json`, `deep17.json`, `synthesis.csv`.

**33 supports swept**, spanning the required classes:

| class | supports |
|---|---|
| genus 0 with 2 places at infinity | H1–H8 (`deg g <= 1`), V1 |
| genus 0 with >= 3 places | E1, E4, E5, E7, E12, V2, V3, V4 |
| positive-genus fibres | E6 (g=1), E10 (g=1), E11 (g=2), E13 (g=1), E14 (g=2), V5 (g=1) |
| v-quadratic | H1–H10, E1–E5, E9, E10, E12, V1, V5, V6 |
| v-cubic and higher | E6–E8, E11, E13, E14, V2, V3, V4 |
| mixed Newton supports | M1 (y-shear), M2 (y- then x-shear), M3 (x-shear) |
| strata the system kills | H9, H10, E2, E3, E8, E9, V6 |

Degrees of the instances run: 2, 3, 5, 6, 7, 8, 9, 11, 12, 15, 29.

### 4.1 Per support: system size, solution structure, survivors

| support | shape | unknowns | residue equations | solution structure | instances | survivors |
|---|---|---|---|---|---|---|
| H1 | HE(G=0,H=1,K=2) | 6 | -4*g0*k2 + h1**2 | proper ideal (Groebner basis of 1 elements); solvable with h1 nonzero | 2 | 0 |
| H2 | HE(G=0,H=3,K=6) | 12 | -4*g0*k2 + 2*h0*h2 + h1**2; -4*g0*k3 + 2*h0*h3 + 2*h1*h2; -4*g0*k4 + 2*h1*h3 + h2**2 ... (5 total) | Groebner not attempted (12 unknowns, 5 equations); structure read off directly: every equation is LINEAR in the k_j with triangular leading term -4 g_ | 1 | 0 |
| H3 | HE(G=1,H=1,K=1) | 6 | -4*g1*k1 + h1**2 | proper ideal (Groebner basis of 1 elements) | 1 | 1 |
| H4 | HE(G=1,H=2,K=3) | 9 | -4*g0*k2 - 4*g1*k1 + 2*h0*h2 + h1**2; -4*g0*k3 - 4*g1*k2 + 2*h1*h2; -4*g1*k3 + h2**2 | proper ideal (Groebner basis of 7 elements) | 1 | 1 |
| H5 | HE(G=1,H=3,K=5) | 12 | -4*g0*k2 - 4*g1*k1 + 2*h0*h2 + h1**2; -4*g0*k3 - 4*g1*k2 + 2*h0*h3 + 2*h1*h2; -4*g0*k4 - 4*g1*k3 + 2*h1*h3 + h2**2 ... (5 total) | Groebner not attempted (12 unknowns, 5 equations); structure read off directly: every equation is LINEAR in the k_j with triangular leading term -4 g_ | 1 | 1 |
| H6 | HE(G=1,H=5,K=9) | 18 | -4*g0*k2 - 4*g1*k1 + 2*h0*h2 + h1**2; -4*g0*k3 - 4*g1*k2 + 2*h0*h3 + 2*h1*h2; -4*g0*k4 - 4*g1*k3 + 2*h0*h4 + 2*h1*h3 + h2**2 ... (9 total) | Groebner not attempted (18 unknowns, 9 equations); structure read off directly: every equation is LINEAR in the k_j with triangular leading term -4 g_ | 1 | 0 |
| H7 | HE(G=1,H=8,K=15) | 27 | -4*g0*k2 - 4*g1*k1 + 2*h0*h2 + h1**2; -4*g0*k3 - 4*g1*k2 + 2*h0*h3 + 2*h1*h2; -4*g0*k4 - 4*g1*k3 + 2*h0*h4 + 2*h1*h3 + h2**2 ... (15 total) | Groebner not attempted (27 unknowns, 15 equations); structure read off directly: every equation is LINEAR in the k_j with triangular leading term -4 g | 1 | 1 |
| H8 | HE(G=1,H=15,K=29) | 48 | -4*g0*k2 - 4*g1*k1 + 2*h0*h2 + h1**2; -4*g0*k3 - 4*g1*k2 + 2*h0*h3 + 2*h1*h2; -4*g0*k4 - 4*g1*k3 + 2*h0*h4 + 2*h1*h3 + h2**2 ... (29 total) | Groebner not attempted (48 unknowns, 29 equations); structure read off directly: every equation is LINEAR in the k_j with triangular leading term -4 g | 1 | 1 |
| H9 | HE(G=2,H=2,K=2) | 9 | g2; -4*g0*k2 - 4*g1*k1 - 4*g2*k0 + 2*h0*h2 + h1**2; -4*g1*k2 - 4*g2*k1 + 2*h1*h2 ... (4 total) | UNIT IDEAL with g2 nonzero adjoined: NO SOLUTIONS | 0 | 0 |
| H10 | HE(G=0,H=0,K=2) | 5 | -4*g0*k2 | proper ideal (Groebner basis of 1 elements); solvable with k2 nonzero | 0 | 0 |
| E1 | SE(m=2;3) | 4 | none (every point of the support solves) | no equations: the whole support solves | 2 | 2 |
| E2 | SE(m=2;2) | 4 | 1 | UNIT IDEAL with alpha c nonzero adjoined: NO SOLUTIONS | 0 | 0 |
| E3 | SE(m=2;4) | 4 | -alpha | UNIT IDEAL with alpha c nonzero adjoined: NO SOLUTIONS | 0 | 0 |
| E4 | SE(m=2;5) | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 1 |
| E5 | SE(m=2;9) | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 1 |
| E6 | SE(m=3;2) | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 0 |
| E7 | SE(m=3;4) | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 1 |
| E8 | SE(m=3;3) | 4 | 1 | UNIT IDEAL with alpha c nonzero adjoined: NO SOLUTIONS | 0 | 0 |
| E9 | SE(m=2;2,3) | 5 | 1 | UNIT IDEAL with alpha c nonzero adjoined: NO SOLUTIONS | 0 | 0 |
| E10 | SE(m=2;3,3) | 5 | none (every point of the support solves) | no equations: the whole support solves | 1 | 0 |
| E11 | SE(m=3;5,4) | 5 | none (every point of the support solves) | no equations: the whole support solves | 1 | 0 |
| E12 | SE(m=2;27) | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 0 |
| E13 | SE(m=4;3) | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 0 |
| E14 | SE(m=5;3) | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 0 |
| V1 | v-power  P = h0 y + c x^1 y^2 | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 1 |
| V2 | v-power  P = h0 y + c x^2 y^3 | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 1 |
| V3 | v-power  P = h0 y + c x^2 y^5 | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 1 |
| V4 | v-power  P = h0 y + c x^3 y^4 | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 1 |
| V5 | v-power  P = h0 y + c x^4 y^2 | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 0 |
| V6 | v-power  P = h0 y + c x^2 y^4 | 4 | -alpha | UNIT IDEAL with alpha c nonzero adjoined: NO SOLUTIONS | 0 | 0 |
| M1 | shear image | 10 | none (every point of the support solves) | shear image of a solved support; Jacobian-1 shears preserve eta and all periods (control G3) | 1 | 1 |
| M2 | shear image | 15 | none (every point of the support solves) | shear image of a solved support; Jacobian-1 shears preserve eta and all periods (control G3) | 1 | 1 |
| M3 | shear image | 6 | none (every point of the support solves) | shear image of a solved support; Jacobian-1 shears preserve eta and all periods (control G3) | 1 | 1 |

### 4.2 Per instance: certificates and mate verdicts

| support | id | deg | deg_y | screen | genus | punctures | Bezout | SY | survivor | mate | NUM-MONO rel |
|---|---|---|---|---|---|---|---|---|---|---|---|
| H1 | `1e8144b39dbd` | 2 | 2 | PERIODS_VANISH | 0 | - | OK residual 0 (EUCLID) | COORDINATE | no | - | 4.6e-16 |
| H1 | `05448ae01b6d` | 2 | 2 | PERIODS_VANISH | 0 | - | OK residual 0 (EUCLID) | COORDINATE | no | - | 4.8e-16 |
| H2 | `f9c3e6131ab8` | 6 | 2 | PERIODS_VANISH | 0 | - | OK residual 0 (EUCLID) | COORDINATE | no | - | 1.1e-15 |
| H3 | `d37142063698` | 3 | 2 | PERIODS_VANISH | 0 | - | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=3:EMPTY_over_Q;D=5:EMPTY_over_Q;D=6:EMPTY_over_Q | 2.0e-13 |
| H4 | `431f3f1966ca` | 3 | 2 | PERIODS_VANISH | 0 | - | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=3:EMPTY_over_Q;D=5:EMPTY_over_Q;D=6:EMPTY_over_Q | 3.6e-15 |
| H5 | `9667585bcb72` | 5 | 2 | PERIODS_VANISH | 0 | - | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=5:EMPTY_over_Q;D=8:EMPTY_over_Q;D=10:EMPTY_over_Q | 5.8e-14 |
| H6 | `fb63dd1ccaec` | 9 | 2 | PERIODS_VANISH | 0 | - | NOT_CERTIFIED (None) | NON_COORDINATE | no | - | 3.4e-15 |
| H7 | `2c6dbb9e3815` | 15 | 2 | PERIODS_VANISH | 0 | - | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=15:EMPTY_over_Q;D=23:EMPTY_over_Q | - |
| H8 | `02299003cb19` | 29 | 2 | PERIODS_VANISH | 0 | - | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=29:EMPTY_over_Q | - |
| E1 | `4b3d403b5051` | 5 | 2 | PERIODS_VANISH | 0 | 3 | OK residual 0 (LINALG) | NON_COORDINATE | yes | D=5:EMPTY_over_Q;D=8:EMPTY_over_Q;D=10:EMPTY_over_Q | 6.9e-14 |
| E1 | `e57028c3921e` | 5 | 2 | PERIODS_VANISH | 0 | 3 | OK residual 0 (LINALG) | NON_COORDINATE | yes | D=5:EMPTY_over_Q;D=8:EMPTY_over_Q;D=10:EMPTY_over_Q | 5.4e-15 |
| E4 | `168e0b30d46b` | 7 | 2 | PERIODS_VANISH | 0 | 3 | OK residual 0 (LINALG) | NON_COORDINATE | yes | D=7:EMPTY_over_Q;D=11:EMPTY_over_Q;D=14:EMPTY_over_Q | 4.3e-14 |
| E5 | `65551d9727e7` | 11 | 2 | PERIODS_VANISH | 0 | 3 | OK residual 0 (LINALG) | NON_COORDINATE | yes | D=11:EMPTY_over_Q;D=17:EMPTY_over_Q;D=22:EMPTY_over_Q | 1.3e-13 |
| E6 | `b520c37ad02b` | 5 | 3 | UNDECIDED_BY_RESIDUES_genus>=1 | 1 | 2 | OK residual 0 (LINALG) | NON_COORDINATE | no | - | 1.5e+00 |
| E7 | `f2782c9f083f` | 7 | 3 | PERIODS_VANISH | 0 | 4 | OK residual 0 (LINALG) | NON_COORDINATE | yes | D=7:EMPTY_over_Q;D=11:EMPTY_over_Q;D=14:EMPTY_over_Q | 6.9e-14 |
| E10 | `5ba43826fa42` | 8 | 2 | UNDECIDED_BY_RESIDUES_genus>=1 | 1 | 3 | OK residual 0 (LINALG) | NON_COORDINATE | no | - | 1.4e+00 |
| E11 | `e507bc4e8db0` | 12 | 3 | UNDECIDED_BY_RESIDUES_genus>=1 | 2 | 3 | OK residual 0 (LINALG) | NON_COORDINATE | no | - | - |
| E12 | `13aa79d7382f` | 29 | 2 | PERIODS_VANISH | 0 | 3 | NOT_CERTIFIED (None) | NON_COORDINATE | no | - | - |
| E13 | `462652ead2a6` | 7 | 4 | UNDECIDED_BY_RESIDUES_genus>=1 | 1 | 3 | OK residual 0 (LINALG) | NON_COORDINATE | no | - | 2.0e+00 |
| E14 | `5497083f3554` | 8 | 5 | UNDECIDED_BY_RESIDUES_genus>=1 | 2 | 2 | OK residual 0 (LINALG) | NON_COORDINATE | no | - | 2.1e+00 |
| V1 | `2f401c620811` | 3 | 2 | PERIODS_VANISH | 0 | 2 | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=3:EMPTY_over_Q;D=5:EMPTY_over_Q;D=6:EMPTY_over_Q | 8.9e-15 |
| V2 | `977aeb39d938` | 5 | 3 | PERIODS_VANISH | 0 | 3 | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=5:EMPTY_over_Q;D=8:EMPTY_over_Q;D=10:EMPTY_over_Q | 2.1e-14 |
| V3 | `3d71c055f95f` | 7 | 5 | PERIODS_VANISH | 0 | 3 | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=7:EMPTY_over_Q;D=11:EMPTY_over_Q;D=14:EMPTY_over_Q | 1.8e-15 |
| V4 | `8cf19228f363` | 7 | 4 | PERIODS_VANISH | 0 | 4 | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=7:EMPTY_over_Q;D=11:EMPTY_over_Q;D=14:EMPTY_over_Q | 1.2e-13 |
| V5 | `e1961840267e` | 6 | 2 | UNDECIDED_BY_RESIDUES_genus>=1 | 1 | 3 | OK residual 0 (EUCLID) | NON_COORDINATE | no | - | 1.6e+00 |
| M1 | `2d9fa751f027` | 5 | 2 | PERIODS_VANISH | 0 | - | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=5:EMPTY_over_Q;D=8:EMPTY_over_Q;D=10:EMPTY_over_Q | 2.0e-13 |
| M2 | `97e25aa31406` | 6 | 6 | PERIODS_VANISH | 0 | 2 | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=6:EMPTY_over_Q;D=9:EMPTY_over_Q;D=12:EMPTY_over_Q | - |
| M3 | `61cc00cd7420` | 5 | 5 | PERIODS_VANISH | 0 | 2 | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=5:EMPTY_over_Q;D=8:EMPTY_over_Q;D=10:EMPTY_over_Q | - |

### 4.3 The synthesised P (survivors)

* `d37142063698`  (support H3, degree 3) — `P = 1*x*y^2 + 1*x*y + (1/4)*x + 1*y`
* `431f3f1966ca`  (support H4, degree 3) — `P = (1/4)*x^3 + 1*x^2*y + 1*x*y^2 + (3/4)*x^2 + 1*x*y - 1*y^2 + (3/2)*x + 1*y + (7/4)`
* `9667585bcb72`  (support H5, degree 5) — `P = (1/8)*x^5 + (1/4)*x^4 + 1*x^3*y + (1/8)*x^3 + 1*x^2*y + 2*x*y^2 + (1/4)*x^2 + (1/4)*x + 1*y + (-3/8)`
* `2c6dbb9e3815`  (support H7, degree 15) — `P = (1/4)*x^15 + (1/2)*x^14 + (1/4)*x^13 + (1/2)*x^12 + (1/2)*x^11 + (3/4)*x^9 + 1*x^8*y + (1/2)*x^8 + 1*x^7*y + (1/2)*x^7 + 1*x^6 + 1*x^5*y + (1/2)*x^4 + (1/4)*x^3 + 1*x^2*y + 1*x*y^2 + (1/2)*x + 1*y + (-1/4)`
* `02299003cb19`  (support H8, degree 29) — `P = (1/4)*x^29 + (1/2)*x^28 + (1/4)*x^27 + 1*x^15*y + 1*x^14*y + (1/2)*x^14 + (1/2)*x^13 + 1*x*y^2 + 1*y + (-1/4)`
* `4b3d403b5051`  (support E1, degree 5) — `P = 1*x^3*y^2 + 1*x`
* `e57028c3921e`  (support E1, degree 5) — `P = 3*x^3*y^2 - 9*x^2*y^2 + 9*x*y^2 - 3*y^2 + 2*x + 1`
* `168e0b30d46b`  (support E4, degree 7) — `P = 1*x^5*y^2 + 1*x`
* `65551d9727e7`  (support E5, degree 11) — `P = 1*x^9*y^2 + 1*x`
* `f2782c9f083f`  (support E7, degree 7) — `P = 1*x^4*y^3 + 1*x`
* `2f401c620811`  (support V1, degree 3) — `P = 1*x*y^2 + 1*y`
* `977aeb39d938`  (support V2, degree 5) — `P = 1*x^2*y^3 + 1*y`
* `3d71c055f95f`  (support V3, degree 7) — `P = 1*x^2*y^5 + 1*y`
* `8cf19228f363`  (support V4, degree 7) — `P = 1*x^3*y^4 + 1*y`
* `2d9fa751f027`  (support M1, degree 5) — `P = 1*x^5 + 2*x^4 + 2*x^3*y + 2*x^3 + 2*x^2*y + 1*x*y^2 + 2*x^2 + 1*x*y + (5/4)*x + 1*y`
* `97e25aa31406`  (support M2, degree 6) — `P = 1*y^6 + 3*x*y^4 + 2*y^5 + 3*x^2*y^2 + 4*x*y^3 + 2*y^4 + 1*x^3 + 2*x^2*y + 3*x*y^2 + 1*y^3 + 1*x^2 + 1*x*y + (5/4)*y^2 + (5/4)*x + 1*y`
* `61cc00cd7420`  (support M3, degree 5) — `P = 1*x^3*y^2 + 3*x^2*y^3 + 3*x*y^4 + 1*y^5 + 1*x + 1*y`

### 4.4 The three supplementary items

```
S1  H10 = HE(G=0,H=0,K=2) with BOTH g0 != 0 and k2 != 0
    equations: ['-4*g0*k2']
    Rabinowitsch (g0 != 0, k2 != 0): unsolvable = True   basis = [1]

S2  H6 = HE(G=1,H=5,K=9), a second instance with h(a) != 0
    g = x + 1, h = 2*x**5 + x**4 + x + 1, h(a) = -1, Delta = x + 2
    deg 9  PERIODS_VANISH  unimod=UNIMODULAR_CERTIFIED (EUCLID, residual 0)  SY=NON_COORDINATE
    NUM-MONO: c=1 rel = 3.2e-14
      D=9   n=55    EMPTY_over_Q     (0.5s)
      D=14  n=120   EMPTY_over_Q     (2.7s)
      D=18  n=190   EMPTY_over_Q     (10.7s)
    mate: EMPTY_over_Q_all_stages

S3  E12 = SE(m=2; 27), deg 29, closed-form Bezout
    U = -27*x**26*y**2 + 1
    V = 729*x**25*y**3/2
    U P_x + V P_y - 1 expanded over Q: 0 residual terms
    screen=PERIODS_VANISH  SY=NON_COORDINATE  survivor=True
      D=29  n=465   EMPTY_over_Q     (0.4s)

    closed-form Bezout re-checked on further SE members:
      alpha=1 c=1 m=2 roots=[(0, 3)]  deg P=5  residual terms = 0
      alpha=2 c=3 m=2 roots=[(1, 3)]  deg P=5  residual terms = 0
      alpha=1 c=1 m=3 roots=[(0, 5), (2, 4)]  deg P=12  residual terms = 0
      alpha=1 c=3 m=3 roots=[(0, 4)]  deg P=7  residual terms = 0
```

The H6 instance that the driver drew first had `h(a) = 0` and came back
`NOT_CERTIFIED` by the Bezout producers — not an instrument failure but the
sharpness of 2.1: on the `deg g = 1` stratum unimodularity IS `h(a) != 0`, and
that instance sits on the excluded wall. The second instance, with
`h(a) = -1`, certifies immediately.

### 4.5 Deeper mate escalation

Every survivor of degree `<= 7` was re-run at `deg Q <= 2 deg P, 3 deg P,
4 deg P` (`deep17.py`): thirteen instances, `EMPTY_over_Q` with an exactly
verified `lambda` at every stage, **0 mates found**. Largest carrier decided:
435 unknowns (`deg P = 7`, `deg Q <= 28`).

---

## 5. Measurements

**M1. The mandatory control passed on every coordinate tested**, at support
level (the residue equations) and at instance level (substituting the
coefficient vector into the equations returned `0` for every equation), for
`x + y^2`, `x + y^m` (`m = 2,3,4,5`) and triangular compositions of degree 6,
10 and 12 with verified mates.

**M2. Nineteen `P` were synthesised satisfying (a), (b) and (c') by
construction** — degrees 3, 3, 3, 5, 5, 5, 5, 5, 5, 6, 7, 7, 7, 7, 9, 11, 15,
29, 29 — each with

* an exact Bezout certificate `U P_x + V P_y - 1 = 0` with an EMPTY residual;
* the Shpilrain–Yu verdict `NON_COORDINATE`;
* a fibre witness of non-coordinacy (generic fibre of genus 0 with 2, 3 or 4
  punctures, never `A^1`);
* all residues zero and genus 0 on the generic fibre, exactly and symbolically,
  and (where the numeric instrument was run) `ls_residual/scale <= 3.2e-14` from
  night15's NUM-MONO.

**M3. Every one of them has an EMPTY mate system over `Q`.** Nineteen for
nineteen `EMPTY_over_Q` at every carrier attempted — `deg Q <= 2 deg P` for all
of them and `deg Q <= 4 deg P` for the thirteen of degree `<= 7` — each with a
`lambda` solved and verified exactly over `Q` (`lambda^T A = 0` on every column,
`lambda^T e = 1`). **No mate system was consistent; the hit gate did not
fire.**

**M4. The necessary condition (c') is very far from sufficient.** The inverted
search produces survivors in unbounded families, not in ones and twos: on the
`HE`, `deg g = 1` stratum the solution set of the residue system INTERSECTED
with the unimodular locus is a rational variety of dimension `deg h + 4` whose
every point is a non-coordinate survivor, giving survivors at every odd degree
`>= 3`; on the `SE` supports with `m` dividing no `e_i`, the residue system is
EMPTY — every unimodular member of the support is a survivor. So (c') removes
no member of these families at all, and the 193/256 rejection rate night15
measured is a property of that corpus, not of the condition.

**M5. Supports whose residue system has no solution off the coordinate locus
(the brief's item 4), with Groebner evidence.**

| support | shape | residue system | evidence |
|---|---|---|---|
| H1, H2 | `HE`, `g` constant | `[x^j](h^2 - 4 g k) = 0`, `j >= 2` | solvable, but every unimodular solution is a COORDINATE (2.1: `4 g P = w^2 - alpha x - beta` exhibits the inverse), confirmed by Shpilrain–Yu on all three instances |
| H9 | `HE(2,2,2)` | `g2 = 0`, ... | Rabinowitsch with `g2 != 0`: Groebner basis `[1]` — NO solutions |
| H10 | `HE(0,0,2)` | `-4 g0 k2 = 0` | with `k2 != 0` only: basis `[k2 z1 - 1, g0]`, i.e. solutions force `g0 = 0` (no `y^2` term, outside the support); with `g0 != 0` AND `k2 != 0`: basis `[1]` — NO solutions |
| E2 | `SE(m=2; 2)` | `1 = 0` | basis `[1]` — NO solutions |
| E3 | `SE(m=2; 4)` | `-alpha = 0` | basis `[1]` with `alpha != 0` adjoined; `alpha != 0` is FORCED by unimodularity (2.2), so the residue condition and unimodularity are incompatible on this support |
| E8 | `SE(m=3; 3)` | `1 = 0` | basis `[1]` — NO solutions |
| E9 | `SE(m=2; 2,3)` | `1 = 0` | basis `[1]` — NO solutions |
| V6 | v-power `h0 y + c x^2 y^4` | `h0/(2 lam) = 0` | basis `[1]` with `h0 != 0, c != 0` — NO solutions |

The pattern behind the `SE` rows is the exponent rule: `e_i = m` puts the
residue equation at the LEADING Taylor coefficient, which is a nonzero constant
(`1 = 0`), and `e_i = 2m` puts it at the next one, which is `alpha` — the very
coefficient unimodularity needs nonzero.

**M6. Positive-genus supports: residues vanish, periods do not.** On E6, E10,
E11, E13, E14 and V5 the residue system is EMPTY (no equations at all) and the
generic fibre has genus 1 or 2, so residues cannot decide. These are recorded
as `UNDECIDED_BY_RESIDUES`, never as survivors. night15's NUM-MONO, run on the
same members, returns `ls_residual/scale` between `1.15` and `2.15` on the
fibres `c = 1, -1` — i.e. NONVANISHING periods. The obstruction there is
carried entirely by the genus part of `H_1`, which the residue equations do not
see: a second, independent reason not to treat (c') as the whole condition.

**M7. Mixed Newton supports behave as the shear control requires.** M1
(`y -> y + x + x^2`), M2 (`y`- then `x`-shear, which raises `deg_y` to 4 and
makes the Newton support genuinely two-dimensional) and M3 (`x -> x + y`) are
Jacobian-1 images of H3 and E1 members. All three keep the unimodularity and
non-coordinacy certificates, keep `PERIODS_VANISH`, and return
`EMPTY_over_Q` at every carrier — as they must, since a Jacobian-1 change of
variables carries mates to mates and `eta` to `eta`.

---

## 6. Hit-gate status

**No mate system was consistent.** Every mate solve in this lane — 19
survivors, plus 13 deeper escalations, plus the negative controls — returned
`EMPTY_over_Q` with a `lambda` certificate verified exactly over `Q`, on
carriers up to `deg Q <= 4 deg P`. The mate solver's own control (recovering
the mate of a degree-10 and a degree-12 coordinate, coefficientwise residual 0)
passed before any of those verdicts was recorded. `night17/HIT_<hash>/` was
therefore never written.
