# night18 / FAMILY.md — the `HE`, `deg g = 1` stratum as one explicit family

Measurements only.  Read-only inputs: `night17/SYNTHESIS.md` (§2.1),
`night17/records17.json`, `night17/{pk17,certs17,res17,mate17,coord17}.py`,
`night15/PERIODS.md`.  Instruments in this lane: `spk18.py` (bivariate
polynomial kernel with sympy coefficients), `fam18.py` (the family and the two
identities), `members18.py` (the cross-checks).

---

## 1. The parametrisation

night17 §2.1 solves `RES(HE)` on the stratum `deg g = 1` in closed form.  With
`P = g(x) y^2 + h(x) y + k(x)` the solution set, intersected with the
gradient-unimodular locus, is the image of the rational map

| symbol | value | range |
|---|---|---|
| `g`     | `gamma * (x - a)`                              | `gamma != 0` |
| `h`     | `h_0 + h_1 x + ... + h_H x^H`                  | free, `H = deg h` |
| `alpha` | free                                           | free |
| `beta`  | `h(a)^2 - alpha * a`                           | determined |
| `k`     | `(h^2 - alpha x - beta) / (4 gamma (x - a))`   | exact division |
| `P`     | `g y^2 + h y + k`                              | |

Free parameters: `gamma, a, alpha, h_0, ..., h_H` — **`H + 4 = deg h + 4`** of
them, matching night17's dimension count.  The support is `HE(1, H, 2H-1)`,
`deg P = max(3, 2H-1)`.  Open conditions cutting out the honest locus:

* `gamma != 0`   (otherwise `deg g != 1` and the point leaves the stratum),
* `h(a) != 0`    (night17 §2.1: on this stratum this **is** gradient-unimodularity).

The division defining `k` is exact **identically in the parameters**: the
numerator `h^2 - alpha x - beta` evaluated at `x = a` is
`h(a)^2 - alpha a - beta = 0` by the choice of `beta`.  `fam18.verify` records
the sympy division remainder as `0` for `H = 1, 2, 3`.

### 1.1 Written out, `deg h = 1` (5 parameters, `deg P = 3`, support `H3`)

```
P = gamma*(x - a)*y^2 + (h0 + h1*x)*y
    + h1^2/(4*gamma) * x + ( a*h1^2 + 2*h0*h1 - alpha ) / (4*gamma)
```

### 1.2 Written out, `deg h = 2` (6 parameters, `deg P = 3`, support `H4`)

```
P = gamma*(x - a)*y^2 + (h0 + h1*x + h2*x^2)*y
    + h2^2/(4*gamma) * x^3 + (a*h2^2 + 2*h1*h2)/(4*gamma) * x^2
    + (a^2*h2^2 + 2*a*h1*h2 + 2*h0*h2 + h1^2)/(4*gamma) * x
    + (a^3*h2^2 + 2*a^2*h1*h2 + 2*a*h0*h2 + a*h1^2 + 2*h0*h1 - alpha)/(4*gamma)
```

Machine-readable: `family18.json` (`H = 1, 2, 3`).

---

## 2. Verification (i) — the exact Bezout identity, as an identity in the parameters

Put `L := 2g = 2 gamma (x-a)`, so `P_y = L y + h`.  Expanding
`L^2 P_x` and reducing `L y = P_y - h` gives the **identity**

```
L^2 * P_x  +  ( -(gamma (P_y - 2h) + h' L) ) * P_y  =  gamma h^2 - h' h L + k' L^2  =:  R(x)
```

and `R` collapses to a **constant in `x`**:

```
R  =  gamma * h(a)^2          (checked: R - gamma*h(a)^2 expands to 0 for H = 1, 2, 3)
```

so with `A = L^2`, `B = -(gamma(P_y - 2h) + h' L)`,

```
U := A / (gamma h(a)^2),   V := B / (gamma h(a)^2),   U * P_x + V * P_y = 1.
```

`deg h = 1`:

```
U = 4*gamma*(x - a)^2 / (gamma*(a*h1 + h0)^2)
V = (2*a*gamma*y + 2*a*h1 - 2*gamma*x*y + h0 - h1*x) / (gamma*(a*h1 + h0)^2)
```

`deg h = 2`:

```
U = 4*gamma*(x - a)^2 / (gamma*(a^2*h2 + a*h1 + h0)^2)
V = (2*a*gamma*y + 2*a*h1 + 4*a*h2*x - 2*gamma*x*y + h0 - h1*x - 3*h2*x^2)
      / (gamma*(a^2*h2 + a*h1 + h0)^2)
```

**Check performed.**  `A*P_x + B*P_y - R` was expanded coefficientwise as a
polynomial in `x, y` whose coefficients are polynomials in
`gamma, a, alpha, h_0..h_H` over `Q`, and the residual dict is EMPTY:

| `deg h` | `k` remainder | `R - gamma*h(a)^2` | residual terms of `A P_x + B P_y - R` |
|---|---|---|---|
| 1 | `0` | `0` | **0** |
| 2 | `0` | `0` | **0** |
| 3 | `0` | `0` | **0** |

This is a polynomial identity in the parameters, not a sample-point check.
Unimodularity is therefore automatic on the whole family away from the single
hypersurface `gamma * h(a)^2 = 0`, which is exactly the excluded wall
`gamma = 0` (off the stratum) union `h(a) = 0`.

---

## 3. Verification (ii) — all residues vanish identically

The Gelfand–Leray form is `eta = -dx / Delta_c^(1/2)` with
`Delta_c = h^2 - 4 g k + 4 g c` (night17 §1.3).  The identity to check is

```
Delta := h^2 - 4 g k  =  alpha x + beta        identically in the parameters
```

**Checked**: `Delta - (alpha x + beta)` expands to `0` for `H = 1, 2, 3`.  Hence

```
Delta_c = alpha x + beta + 4 gamma (x - a) c ,        deg_x Delta_c <= 1 for every c.
```

Consequences, by the exponent rule of night17 §1.2, valid **identically over
the parameter field**:

* every finite branch point is a simple root (`mu = 1`), so `w = -mu/2 = -1/2`
  is not an integer and **no finite place carries a residue**;
* at infinity `W = -deg(Delta_c)/2 = -1/2` for the generic `c` — not an
  integer, so there is nothing to compute;
* on the single fibre `c = -alpha/(4 gamma)` where `Delta_c` degenerates to the
  constant `beta + 4 gamma a c ...`, `deg Delta_c = 0`, `W = 0 >= -1` is an
  integer, the analytic factor is the constant series `1`, and the required
  Taylor coefficient is `[u^1] 1 = 0`, so the residue is **`0`**.

So `RES(HE)` holds identically and the genus of the smooth fibre is
`floor((deg Delta_0 - 1)/2) = 0`: genus 0 with two punctures, which is
simultaneously night17's fibre witness of NON-COORDINACY.

---

## 4. Cross-check against night17's recorded instances (`members18.py`)

Both identities hold, so the hard gate's fallback branch was not triggered.
The cross-checks were run anyway.

### 4.1 Every night17 `HE` instance with `deg g = 1` is recovered exactly

Parameters were read back off each recorded `P` (`gamma = lc(g)`, `a` its root,
`alpha, beta` from `h^2 - 4gk`, `h_i` from the `y`-coefficient), the family was
re-instantiated at those parameters, and the two polynomials were subtracted
coefficientwise.

```
  H1   1e8144b39dbd   not on this stratum: deg g = 0
  H1   05448ae01b6d   not on this stratum: deg g = 0
  H2   f9c3e6131ab8   not on this stratum: deg g = 0
  H3   d37142063698   MEMBER   deg h=1  gamma=1  a=0   alpha=2  h(a)=1
  H4   431f3f1966ca   MEMBER   deg h=2  gamma=1  a=1   alpha=1  h(a)=3
  H5   9667585bcb72   MEMBER   deg h=3  gamma=2  a=0   alpha=3  h(a)=1
  H6   fb63dd1ccaec   MEMBER   deg h=5  gamma=1  a=-1  alpha=1  h(a)=0
  H7   2c6dbb9e3815   MEMBER   deg h=8  gamma=1  a=0   alpha=1  h(a)=1
  H8   02299003cb19   MEMBER   deg h=15 gamma=1  a=0   alpha=1  h(a)=1
```

Six for six, with a zero difference dict in every case, and
`beta = h(a)^2 - alpha a` confirmed on each.  The `H6` row lands on `h(a) = 0`
— the wall the family's own Bezout denominator names — which is precisely why
night17 recorded that instance as `NOT_CERTIFIED` by its Bezout producers.
`H1`/`H2` sit on the `deg g = 0` stratum and are correctly reported as
non-members.

### 4.2 Five random parameter points, judged by night17's instruments

```
  deg h=1 gamma=-2 a=-2 alpha=-2 h0=-3 h1=-2   uni=UNIMODULAR_CERTIFIED  SY=NON_COORDINATE  res0=True genus=0
  deg h=1 gamma=3  a=-3 alpha=-3 h0=2  h1=1    uni=UNIMODULAR_CERTIFIED  SY=NON_COORDINATE  res0=True genus=0
  deg h=2 gamma=2  a=2  alpha=2  h0=-3 h1=3  h2=-1        uni=UNIMODULAR_CERTIFIED  SY=NON_COORDINATE  res0=True genus=0
  deg h=2 gamma=-1 a=0  alpha=3  h0=1  h1=-1 h2=3         uni=UNIMODULAR_CERTIFIED  SY=NON_COORDINATE  res0=True genus=0
  deg h=3 gamma=2  a=0  alpha=4  h0=3  h1=-3 h2=-1 h3=3   uni=UNIMODULAR_CERTIFIED  SY=NON_COORDINATE  res0=True genus=0

CROSS-CHECK PASS
```

`uni` is `night17/certs17.unimodular` (exact Bezout, residual 0 terms), `SY` is
`night17/certs17.sy` (Shpilrain–Yu), `res0`/`genus` are `night17/res17.he17`.
Machine-readable: `members18.json`.
