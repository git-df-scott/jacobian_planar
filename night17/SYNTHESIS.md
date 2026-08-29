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
