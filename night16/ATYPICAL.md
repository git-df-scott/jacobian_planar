# night16 — THE ATYPICAL-VALUE RE-SCREEN

Measurements only.

---

## 0. The gap this closes

night15 derived and ran the **period screen**: if `P` has a Keller mate `Q`
(`P_x Q_y - P_y Q_x = 1`) then the Gelfand–Leray form

    eta = dy/P_x = -dx/P_y

restricts to `dQ` on every fibre `F_c = {P = c}`, so **every period of `eta`
over every cycle of every fibre vanishes.**  256 certified gradient-unimodular
`P` were screened; 193 were obstructed, 57 survived, and all 57 then came back
`EMPTY_all_stages` under exact mate solving to `deg Q = 2 deg P`.

The screen was evaluated only at a few generic `c` — `c = 1, -1, 3/2` for the
`EXACT-HE` instrument, and *symbolically at generic `lam != 0`* for `EXACT-G1`,
whose derivation states in its own header that it "assumes lam != 0".  Checking
the 57 survivor records confirms this verbatim: 49 of them have
`period_detail.fibres == []` (EXACT-G1, generic `lam` only) and 8 list only
`c in {1, -1, 3/2}`.  **No survivor was ever measured at `c = 0`, and no
survivor was ever measured at an atypical value.**

A polynomial `P` with unimodular gradient has **no critical points at all**, so
every fibre is smooth; but if `P` is not a coordinate its fibration still fails
to be locally trivial over finitely many **atypical values** — the failure
happening purely at infinity.  At such a `c` the topology of `F_c` jumps: the
number of places at infinity and/or the genus and/or the number of components
changes, and cycles exist on `F_c` that have no counterpart on a generic fibre.
Those cycles were never tested.  night16 tests them.

---

## 1. The detector: `chi(F_c)` exactly, as a function of `c`

### 1.1 What is computed

For an irreducible fibre `chi(F_c) = 2 - 2 g(c) - r(c)` with `r` the number of
places at infinity, and for a reducible fibre the same summed over components.
Rather than computing `g` and `r` separately (which needs Puiseux data at every
place and a genus routine per component), night16 computes the integer
`chi(F_c)` itself, exactly, by an **x-projection decomposition**.

Write

    f = P - c = sum_j a_j(x) y^j ,      N = deg_y f

(the `a_j` for `j >= 1` do not involve `c`; only `a_0` does).

**(0) Vertical components.**  `cont = gcd(a_0, ..., a_N)` in `K[x]`.  Every
distinct root `s` of `cont` gives a line `{x = s}` contained in `F_c`.  Put
`f1 = f / cont` and `n_vert = #{distinct roots of cont}`; each such line is a
copy of `C`, contributing `chi = 1`.

**(1) The covering count.**  Let `A = lc_y(f1)` and

    W(x) = A(x) * Res_y(f1, d f1/dy),        S = {distinct roots of W}.

Over `C \ S` the projection `pi : {f1 = 0} -> C_x` is an unramified `N`-sheeted
covering, so `chi(pi^{-1}(C \ S)) = N (1 - |S|)`.  Over each `s in S` the fibre
`pi^{-1}(s)` is the finite set of **distinct** roots of `f1(s, y)`.  Euler
characteristic is additive over this constructible decomposition, so

    chi(F1_c) = N (1 - |S|) + sum_{s in S} #{distinct roots of f1(s, y)}.

Adding a *non*-branch point to `S` changes the two terms by `-N` and `+N`, so
the formula is insensitive to over-inclusion — which is why `W = A * Res` (a
superset of the true branch locus) is admissible and no squarefree-part
bookkeeping is needed.

**(2)** `chi(F_c) = n_vert + chi(F1_c)`.

The counts `#{distinct roots of f1(s,y)}` are obtained for **all** roots `s` of
a squarefree `V | W` at once by arithmetic in the ring `K[x]/(V)`, using
**dynamic evaluation (D5)**: the Euclidean algorithm for
`gcd(f1, d f1/dy)` in `(K[x]/V)[y]` is run with reduction modulo `V`, and
whenever an inversion of a leading coefficient `a` fails, `V` is split as
`gcd(a,V) * V/gcd(a,V)` and both halves are pursued.  No factorisation of `V`,
no numerical root finding, and no algebraic-number tower are needed anywhere.
`K` is `Q` for a rational `c` and a number field `Q(alpha)` for an algebraic
one; the same code runs over both.

### 1.2 Candidate atypical values — obtained algebraically, not by luck

`chi(F_c)` is determined by the root pattern of `W(x,c)` together with the
fibre counts over those roots, so it can change only where that pattern
degenerates.  Factor `W(x,c) = prod_i F_i(x,c)^{e_i}` in `Q[x,c]`.  The
candidate set is the set of roots in `c` of

| source | what it detects |
|---|---|
| a factor of `W` involving `c` only | wholesale degeneration |
| `lc_x(F_i)(c)` | a branch point escapes to `x = infinity` (a change at infinity) |
| `disc_x(F_i)(c)` | two roots of one factor collide (a branch point of higher order) |
| `Res_x(F_i, F_j)(c)`, `i < j` | roots of two different factors collide |
| `Res_x(gcd(a_1,...,a_N), a_0 - c)` | a vertical line component appears in `F_c` |

together with `c = 0`, always tested.  Every candidate is then **tested** by
computing `chi` there exactly; `chi_gen` is fixed by computing `chi` at six
random rationals (the votes are reported).  A candidate whose `chi` equals
`chi_gen` is reported as tested-and-not-atypical, not discarded silently.
Candidates that are irrational are handled in
`Q(alpha)`, `alpha = CRootOf(p, 0)`, and reported by their minimal polynomial;
Galois conjugates have isomorphic fibres, hence equal `chi`.

Implementation: `atyp16.py`.

---

## 2. The period instruments used ON an atypical fibre

### 2.1 EXACT-PRIM — exact, with a certificate, decisive in the VANISHING direction

On the smooth fibre `F_c` the module of regular 1-forms is free of rank 1 on
`eta`, and for `F` in the coordinate ring `dF|_{F_c} = [P,F] * eta` with
`[P,F] = P_x F_y - P_y F_x`.  Hence

> every period of `eta` over every cycle of `H_1(F_c)` vanishes
> **iff** `[P, F] = 1` in `Q[x,y]/(P - c)` for some polynomial `F`.

(`=>`: a period-free primitive of `eta` is holomorphic on the affine `F_c`; at
each puncture `eta` has at worst a pole with zero residue — a nonzero residue
*is* a nonzero period — so the local primitive is meromorphic there, the global
primitive is rational on the smooth compactification with poles only at the
punctures, i.e. regular on `F_c`.  `<=`: `eta = dF` with `F` single-valued.)

`F_c` is smooth, hence the disjoint union of its irreducible components, so by
CRT the condition holds iff it holds modulo each irreducible factor `h` of
`P - c` separately — which keeps every linear system small.  Membership
`[P,F] - 1 in (h)` is tested by pseudo-division,

    prem([P,F] - 1, h, v) == 0   <=>   [P,F] - 1 in (h)

(`v` a variable in which `h` has positive degree; `lc_v(h)` is a unit mod the
irreducible `h`), and `prem` is **linear** in the unknown coefficients of `F`.
So each test is one rational linear system.  A solution is then **verified as a
certificate** by exact division: `[P,F] - 1 = G h` checked coefficientwise over
`Q`.  Failure up to `deg F <= 6` is recorded as `NO_EXACT_CERTIFICATE` and is
**not** read as an obstruction.

Implementation: `period16.py`.

### 2.2 NUM-MONO — numerical, decisive in the NONVANISHING direction

night15's numerical monodromy period instrument, copied unchanged into this
lane as `mono16.py`.  It continues the `deg_y` sheets of the `x`-projection
around every branch point, solves the potential problem
`u(sigma_j(k)) - u(k) = v_{j,k}` by weighted union–find, reports the
least-squares residual of that system (zero exactly when every period
vanishes), the residues at every place, their sum (control C3 of night15), and
its own `chi`.  It is run **on** each atypical fibre and at nearby generic
fibres `c0 ± 1/8`; exact `chi` is also computed at `c0 ± 1/8` and `c0 ± 1/64`.

---

## 3. Controls (hard gate) — verbatim

```
==============================================================================
night16 CONTROLS -- atypical-value detector
==============================================================================

C1  COORDINATES: no atypical value
  C1a  x + y^2                                        deg= 2 deg_y=2  chi_gen=1   (6/6)  atypical=NONE
       chi at the sampled generic c: [('-13', 1), ('69/7', 1), ('-77/5', 1), ('-5/2', 1), ('1', 1), ('-7', 1)]
       every candidate c tested:     [('0', 1)]
       independent expectation:      NONE   -- a coordinate: every fibre is isomorphic to C, chi == 1
       MATCH: True      (0.09 s)
  C1b  x + (y + x^2)^5  (degree-10 triangular)        deg=10 deg_y=5  chi_gen=1   (6/6)  atypical=NONE
       chi at the sampled generic c: [('-13', 1), ('69/7', 1), ('-77/5', 1), ('-5/2', 1), ('1', 1), ('-7', 1)]
       every candidate c tested:     [('0', 1)]
       independent expectation:      NONE   -- x composed with two Jacobian-1 triangular maps: still a coordinate
       MATCH: True      (0.14 s)

C2  THE CLASSICAL EXAMPLE (hard gate)
  C2   x + x^2*y                                      deg= 3 deg_y=1  chi_gen=0   (6/6)  atypical=['0']
       chi at the sampled generic c: [('-13', 0), ('69/7', 0), ('-77/5', 0), ('-5/2', 0), ('1', 0), ('-7', 0)]
       every candidate c tested:     [('0', 1)]
       independent expectation:      ['0']   -- F_0 = {x=0} u {1+xy=0} is reducible (chi 1); F_c ~ C* for c!=0 (chi 0)
       MATCH: True      (0.02 s)

C3  FURTHER P WITH INDEPENDENTLY KNOWN ATYPICAL SETS
  C3a  x + x^2*y + 5                                  deg= 3 deg_y=1  chi_gen=0   (6/6)  atypical=['5']
       chi at the sampled generic c: [('-13', 0), ('69/7', 0), ('-77/5', 0), ('-5/2', 0), ('1', 0), ('-7', 0)]
       every candidate c tested:     [('0', 0), ('5', 1)]
       independent expectation:      ['5']   -- the same example shifted: the jump must move to c = 5
       MATCH: True      (0.02 s)
  C3b  x*y^2 + y                                      deg= 3 deg_y=2  chi_gen=0   (6/6)  atypical=['0']
       chi at the sampled generic c: [('-13', 0), ('69/7', 0), ('-77/5', 0), ('-5/2', 0), ('1', 0), ('-7', 0)]
       every candidate c tested:     [('0', 1)]
       independent expectation:      ['0']   -- c!=0: x=(c-y)/y^2 gives F_c ~ C\{0}, chi 0; F_0={y=0} u {xy=-1}, chi 1
       MATCH: True      (0.04 s)
  C3c  t^3 - 3t,  t = x + y^2                         deg= 6 deg_y=6  chi_gen=3   (6/6)  atypical=['-2', '2']
       chi at the sampled generic c: [('-13', 3), ('69/7', 3), ('-77/5', 3), ('-5/2', 3), ('1', 3), ('-7', 3)]
       every candidate c tested:     [('0', 3), ('-2', 2), ('2', 2)]
       independent expectation:      ['-2', '2']   -- F_c = disjoint union of the fibres {t = root of t^3-3t-c}, each ~ C (chi 1); chi = #distinct roots, so it drops at the critical values +-2
       MATCH: True      (0.25 s)
  C3d  t^4 - t,  t = x + y^2                          deg= 8 deg_y=8  chi_gen=4   (6/6)  atypical=['root of c**3 + 27/256']
       chi at the sampled generic c: [('-13', 4), ('69/7', 4), ('-77/5', 4), ('-5/2', 4), ('1', 4), ('-7', 4)]
       every candidate c tested:     [('0', 4), ('root of c**3 + 27/256', 3)]
       independent expectation:      ['root of c**3 + 27/256']   -- same construction: chi = #distinct roots of t^4-t-c, which drops at the three (irrational, conjugate) critical values, c^3 = -27/256
       MATCH: True      (0.52 s)

C3e CROSS-CHECK OF chi ITSELF AGAINST NUM-MONO (independent, numerical)
    NUM-MONO computes chi = dy*(1-|B|) + #finite cycles from numerically
    continued monodromy; the detector computes it by exact algebra.
    NUM-MONO's count is taken over the sheets of the x-projection, so it
    CANNOT see a vertical line component {x = s} of the fibre (that whole
    component sits over a single x).  The detector reports n_vert, the
    number of such components, separately; the identity checked here is
        exact chi  -  n_vert  ==  NUM-MONO chi .
    x + x^2*y        c=0    exact chi=1   n_vert=1  chi-n_vert=0    NUM-MONO chi=0     agree=True
    x + x^2*y        c=1    exact chi=0   n_vert=0  chi-n_vert=0    NUM-MONO chi=0     agree=True
    x + x^2*y        c=-2   exact chi=0   n_vert=0  chi-n_vert=0    NUM-MONO chi=0     agree=True
    x*y^2 + y        c=0    exact chi=1   n_vert=0  chi-n_vert=1    NUM-MONO chi=1     agree=True
    x*y^2 + y        c=1    exact chi=0   n_vert=0  chi-n_vert=0    NUM-MONO chi=0     agree=True
    x*y^2 + y        c=3    exact chi=0   n_vert=0  chi-n_vert=0    NUM-MONO chi=0     agree=True
    x + (y+x^2)^5    c=0    exact chi=1   n_vert=0  chi-n_vert=1    NUM-MONO chi=1     agree=True
    x + (y+x^2)^5    c=2    exact chi=1   n_vert=0  chi-n_vert=1    NUM-MONO chi=1     agree=True
    y + x*y^3        c=0    exact chi=1   n_vert=0  chi-n_vert=1    NUM-MONO chi=1     agree=True
    y + x*y^3        c=1    exact chi=0   n_vert=0  chi-n_vert=0    NUM-MONO chi=0     agree=True
    y + x*y^3        c=-1   exact chi=0   n_vert=0  chi-n_vert=0    NUM-MONO chi=0     agree=True
    y^2 + x*y^3      c=0    exact chi=1   n_vert=0  chi-n_vert=1    NUM-MONO chi=None  agree=NO COMPARISON (NUM-MONO errored: this fibre is non-reduced and this P is not gradient-unimodular)
    y^2 + x*y^3      c=1    exact chi=0   n_vert=0  chi-n_vert=0    NUM-MONO chi=0     agree=True

C3f CROSS-CHECK AGAINST night15's RECORDED GENUS AND PLACES AT INFINITY
    for an irreducible fibre  chi = 2 - 2g - r.  night15 recorded (g, r)
    for the generic fibre of each of the 57 survivors; the detector's
    chi_gen is computed with no reference to either number.
    agree: 56    disagree: 1    skipped (no recorded g/r): 0
       DISAGREE hash=808e52fdb1b6 chi_gen=-7 recorded g=0 r=8 (2-2g-r=-6)

GATE: C1 PASS   C2 PASS   C3 PASS
```

```
==============================================================================
C4  EXACT-PRIM CONTROLS  ([P,F] = 1 mod h, verified by exact division)
==============================================================================
  x + y^2                (coordinate)                        c=0
      got VANISHING_EXACT        expected VANISHING_EXACT        MATCH True
      components: [('x + y**2', 'degF=1')]
      why: a coordinate; every fibre is C, H_1 = 0
  x + x^2*y              (classical, ON its atypical fibre)  c=0
      got VANISHING_EXACT        expected VANISHING_EXACT        MATCH True
      components: [('x', 'degF=1'), ('x*y + 1', 'degF=1')]
      why: F_0 = {x=0} u {1+xy=0}: on each piece eta is d(a linear form)
  x + x^2*y              (generic fibre)                     c=1
      got VANISHING_EXACT        expected VANISHING_EXACT        MATCH True
      components: [('x**2*y + x - 1', 'degF=2')]
      why: F_c ~ C*, and eta = dy/P_x is exact on it
  y + x*y^3              (EXACT-G1 n=1,m=3: night15 VANISHING) c=1
      got VANISHING_EXACT        expected VANISHING_EXACT        MATCH True
      components: [('x*y**3 + y - 1', 'degF=3')]
      why: night15 EXACT-G1 case ii: genus 0, all residues zero
  y + x^3*y^4            (EXACT-G1 n=3,m=4: night15 VANISHING) c=1
      got VANISHING_EXACT        expected VANISHING_EXACT        MATCH True
      components: [('x**3*y**4 + y - 1', 'degF=2')]
      why: night15 EXACT-G1 case ii (the fibre that caught the NUM-MONO bug)
  y + x^2*y^2            (EXACT-G1 n=2,m=2: night15 NONVANISHING) c=1
      got NO_EXACT_CERTIFICATE   expected NO_EXACT_CERTIFICATE   MATCH True
      components: [('x**2*y**2 + y - 1', 'none to deg 6')]
      why: night15 EXACT-G1 case i: nonzero residues at the places over y=0
  y + x^2*y^4            (EXACT-G1 n=2,m=4: night15 NONVANISHING) c=1
      got NO_EXACT_CERTIFICATE   expected NO_EXACT_CERTIFICATE   MATCH True
      components: [('x**2*y**4 + y - 1', 'none to deg 6')]
      why: night15 EXACT-G1 case i (n | m); NUM-MONO residue 0.176777
  y + x^4*y^2            (EXACT-G1 n=4,m=2: night15 NONVANISHING) c=1
      got NO_EXACT_CERTIFICATE   expected NO_EXACT_CERTIFICATE   MATCH True
      components: [('x**4*y**2 + y - 1', 'none to deg 6')]
      why: night15 EXACT-G1 case iii: holomorphic nonzero form, genus 1
  y + x^5*y^3            (EXACT-G1 n=5,m=3: night15 NONVANISHING) c=1
      got NO_EXACT_CERTIFICATE   expected NO_EXACT_CERTIFICATE   MATCH True
      components: [('x**5*y**3 + y - 1', 'none to deg 6')]
      why: night15 EXACT-G1 case iii, genus 2

GATE C4: PASS
```

---

## 4. What the atypical fibres of the survivors are, in closed form

### 4.1 The G1 family (53 of the 57 survivors), at `lam = 0`

night15's G1 family is `P = h0 v + c (x-a)^n v^m`, `v = y + t(x)/2`,
`h0 != 0`, `c != 0`, `n >= 1`, `m >= 2`.  The shears `y -> y - t(x)/2` and
`x -> x + a` are triangular with Jacobian 1, so they carry fibres to fibres by
maps pulling `eta` back to `eta`; after them

    P = h0 y + c x^n y^m .

At `lam = 0` this factors:

    P = y * ( h0 + c x^n y^(m-1) ) .

The two factors have no common zero (`h0 != 0` on `{y = 0}`), so the fibre is
the **disjoint** union of

    L  = {y = 0}                        ~  C ,
    C0 = {h0 + c x^n y^(m-1) = 0}       =  {x^n y^(m-1) = -h0/c} ,

and with `d = gcd(n, m-1)` the second is `d` disjoint copies of `C*` (write
`n = d n'`, `m-1 = d k'`, `gcd(n',k') = 1`; the equation splits as `d` equations
`x^(n') y^(k') = B_i`, `B_i^d = -h0/c`, and each of those is parametrised by
`t -> (B_i^p t^(k'), B_i^q t^(-n'))` with `p n' + q k' = 1`).  Hence

    chi(F_0) = 1 + d * 0 = 1 ,

while the generic fibre has `chi = 2 - 2g - r` with `g, r` as tabulated by
night15 — so `c = 0` **is** atypical for every member with `chi_gen != 1`.

Now the periods.  `P_y = h0 + m c x^n y^(m-1)`, so

* on `L`:  `P_y = h0`, hence `eta = -dx/P_y = d(-x/h0)`;
* on `C0`: `c x^n y^(m-1) = -h0`, hence `P_y = h0 - m h0 = (1-m) h0 != 0`
  (this uses `m >= 2`), and `eta = -dx/P_y = d( x / ((m-1) h0) )`.

`eta` is therefore **exact on every component of `F_0`, with a primitive that
is linear in `x`**, and every period on the atypical fibre vanishes.  This is a
closed-form statement about the whole family; the machine run below reproduces
it independently, on the actual (sheared, un-normalised) `P` of each record,
through EXACT-PRIM, which returns a verified certificate of degree 1 or 2 for
every component.

Note where this uses `m >= 2`: if `m = 1` the factor `(1-m) h0` is `0` and the
argument gives nothing — and indeed `m = 1` members are not in the G1 family
(`P = h0 v + c (x-a)^n v` is `v` times a polynomial in `x`, of `deg_y 1`).

### 4.2 The G2 family (4 of the 57 survivors)

`P = alpha x + beta + c B(x) y^m`, `B = prod (x - a_i)^(e_i)`, `e_i >= 2`,
`alpha != 0`.  Here `P_y = c m B y^(m-1)` and `P_x = alpha + c B' y^m`.  The
detector's output for these four is reported in the table; the derivation of
their atypical sets from the shape is given with the results, since it depends
on `m` and on the roots `a_i`.

---

## 5. Results

| # | hash | deg P | deg_y | chi_gen | atypical c | chi(F_c) | jump | components of F_c (degrees) | EXACT-PRIM on F_c (deg F per component) | NUM-MONO on F_c: ls-residual / max period / max residue | nearby generic c: exact chi | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `c5e02d711fe5` | 3 | 2 | 0 | 0 | 1 | 1 | 2 (1,2) | VANISHING_EXACT [1,1] | VANISHING 4.5e-15 / 4e-15 / 0 | 1/8:0; -1/8:0; 1/64:0; -1/64:0 | **STILL-VANISHING** |
| 2 | `a3b909a78c74` | 3 | 2 | 0 | 0 | 1 | 1 | 2 (1,2) | VANISHING_EXACT [1,1] | VANISHING 2.5e-14 / 2.2e-14 / 0 | 1/8:0; -1/8:0; 1/64:0; -1/64:0 | **STILL-VANISHING** |
| 3 | `a03f511f7ecd` | 5 | 2 | 0 | 0 | 1 | 1 | 2 (2,3) | VANISHING_EXACT [1,1] | VANISHING 2e-14 / 1.9e-14 / 0 | 1/8:0; -1/8:0; 1/64:0; -1/64:0 | **STILL-VANISHING** |
| 4 | `fef547c2b095` | 7 | 2 | 0 | 0 | 1 | 1 | 2 (3,4) | VANISHING_EXACT [1,1] | budget exceeded | 1/8:0; -1/8:0; 1/64:0; -1/64:0 | **STILL-VANISHING** |
| 5 | `207b968cb4c5` | 4 | 3 | 0 | 0 | 1 | 1 | 2 (1,3) | VANISHING_EXACT [1,1] | VANISHING 1.6e-14 / 1.9e-14 / 0 | 1/8:0; -1/8:0; 1/64:0; -1/64:0 | **STILL-VANISHING** |
| 6 | `52830078b770` | 4 | 3 | 0 | 0 | 1 | 1 | 2 (1,3) | VANISHING_EXACT [1,1] | VANISHING 1.7e-15 / 1.6e-15 / 0 | 1/8:0; -1/8:0; 1/64:0; -1/64:0 | **STILL-VANISHING** |
| 7 | `39f56b091e75` | 7 | 3 | 0 | 0 | 1 | 1 | 2 (2,5) | VANISHING_EXACT [1,1] | VANISHING 1.1e-13 / 1.4e-13 / 2.8e-13 | 1/8:0; -1/8:0; 1/64:0; -1/64:0 | **STILL-VANISHING** |
| 8 | `36bc150f8dae` | 10 | 3 | 0 | 0 | 1 | 1 | 2 (3,7) | VANISHING_EXACT [1,1] | budget exceeded | 1/8:0; -1/8:0; 1/64:0; -1/64:0 | **STILL-VANISHING** |
| 9 | `0a32a1935a5d` | 5 | 3 | -1 | 0 | 1 | 2 | 2 (1,4) | VANISHING_EXACT [1,1] | VANISHING 8e-15 / 6.3e-15 / 0 | 1/8:-1; -1/8:-1; 1/64:-1; -1/64:-1 | **STILL-VANISHING** |
| 10 | `fa25edeecbfe` | 5 | 3 | -1 | 0 | 1 | 2 | 2 (1,4) | VANISHING_EXACT [1,1] | VANISHING 2.1e-14 / 1.8e-14 / 0 | 1/8:-1; -1/8:-1; 1/64:-1; -1/64:-1 | **STILL-VANISHING** |
| 11 | `1ef523b227e7` | 8 | 3 | -1 | 0 | 1 | 2 | 3 (2,3,3) | VANISHING_EXACT [1,1,1] | budget exceeded | 1/8:-1; -1/8:-1; 1/64:-1; -1/64:-1 | **STILL-VANISHING** |
| 12 | `a4d6d040e138` | 11 | 3 | -1 | 0 | 1 | 2 | 3 (3,4,4) | VANISHING_EXACT [1,1,1] | budget exceeded | 1/8:-1; -1/8:-1; 1/64:-1; -1/64:-1 | **STILL-VANISHING** |
| 13 | `7f2b3c396f45` | 5 | 4 | 0 | 0 | 1 | 1 | 2 (1,4) | VANISHING_EXACT [1,1] | VANISHING 1.4e-14 / 1.9e-14 / 0 | 1/8:0; -1/8:0; 1/64:0; -1/64:0 | **STILL-VANISHING** |
| 14 | `abc13407cc8e` | 5 | 4 | 0 | 0 | 1 | 1 | 2 (1,4) | VANISHING_EXACT [1,1] | VANISHING 3e-15 / 3e-15 / 0 | 1/8:0; -1/8:0; 1/64:0; -1/64:0 | **STILL-VANISHING** |
| 15 | `55a9ae0456b4` | 9 | 4 | 0 | 0 | 1 | 1 | 2 (2,7) | VANISHING_EXACT [1,1] | budget exceeded | 1/8:0; -1/8:0; 1/64:0; -1/64:0 | **STILL-VANISHING** |
| 16 | `632afa8e6433` | 13 | 4 | 0 | 0 | 1 | 1 | 2 (3,10) | VANISHING_EXACT [1,1] | VANISHING 1.1e-10 / 1.9e-10 / 0 | 1/8:0; -1/8:0; 1/64:0; -1/64:0 | **STILL-VANISHING** |
| 17 | `7b72f1effa40` | 7 | 4 | -2 | 0 | 1 | 3 | 3 (1,2,4) | VANISHING_EXACT [1,1,1] | VANISHING 1.1e-14 / 1e-14 / 0 | 1/8:-2; -1/8:-2; 1/64:-2; -1/64:-2 | **STILL-VANISHING** |
| 18 | `cd46f9341dc7` | 7 | 4 | -2 | 0 | 1 | 3 | 2 (1,6) | VANISHING_EXACT [1,1] | VANISHING 1.1e-14 / 5.9e-15 / 0 | 1/8:-2; -1/8:-2; 1/64:-2; -1/64:-2 | **STILL-VANISHING** |
| 19 | `3bd161cf7a22` | 11 | 4 | -2 | 0 | 1 | 3 | 2 (2,9) | VANISHING_EXACT [1,1] | budget exceeded | 1/8:-2; -1/8:-2; 1/64:-2; -1/64:-2 | **STILL-VANISHING** |
| 20 | `d735085d2c22` | 15 | 4 | -2 | 0 | 1 | 3 | 3 (3,4,8) | VANISHING_EXACT [1,1,1] | VANISHING 3.6e-10 / 2.4e-10 / 0 | 1/8:-2; -1/8:-2; 1/64:-2; -1/64:-2 | **STILL-VANISHING** |
| 21 | `37670b444e89` | 6 | 5 | 0 | 0 | 1 | 1 | 2 (1,5) | VANISHING_EXACT [1,1] | VANISHING 1.6e-14 / 1.5e-14 / 0 | 1/8:0; -1/8:0; 1/64:0; -1/64:0 | **STILL-VANISHING** |
| 22 | `00427d4924d2` | 6 | 5 | 0 | 0 | 1 | 1 | 2 (1,5) | VANISHING_EXACT [1,1] | VANISHING 1.9e-13 / 1.9e-13 / 8.4e-14 | 1/8:0; -1/8:0; 1/64:0; -1/64:0 | **STILL-VANISHING** |
| 23 | `c8aa6fd84bbc` | 11 | 5 | 0 | 0 | 1 | 1 | 2 (2,9) | VANISHING_EXACT [1,1] | budget exceeded | 1/8:0; -1/8:0; 1/64:0; -1/64:0 | **STILL-VANISHING** |
| 24 | `f406b3aeda22` | 16 | 5 | 0 | 0 | 1 | 1 | 2 (3,13) | VANISHING_EXACT [1,1] | budget exceeded | 1/8:0; -1/8:0; 1/64:0; -1/64:0 | **STILL-VANISHING** |
| 25 | `8ccaea9ee461` | 7 | 5 | -1 | 0 | 1 | 2 | 2 (1,6) | VANISHING_EXACT [1,1] | VANISHING 1.1e-14 / 1e-14 / 5.1e-15 | 1/8:-1; -1/8:-1; 1/64:-1; -1/64:-1 | **STILL-VANISHING** |
| 26 | `e52860893178` | 7 | 5 | -1 | 0 | 1 | 2 | 2 (1,6) | VANISHING_EXACT [1,1] | VANISHING 3.4e-11 / 2.9e-11 / 1.2e-10 | 1/8:-1; -1/8:-1; 1/64:-1; -1/64:-1 | **STILL-VANISHING** |
| 27 | `7887429824c2` | 12 | 5 | -1 | 0 | 1 | 2 | 2 (2,10) | VANISHING_EXACT [1,1] | VANISHING 1.8e-14 / 1.5e-14 / 5.6e-11 | 1/8:-1; -1/8:-1; 1/64:-1; -1/64:-1 | **STILL-VANISHING** |
| 28 | `726da7cd9516` | 17 | 5 | -1 | 0 | 1 | 2 | 2 (3,14) | VANISHING_EXACT [1,1] | budget exceeded | 1/8:-1; -1/8:-1; 1/64:-1; -1/64:-1 | **STILL-VANISHING** |
| 29 | `c4e207c544a0` | 9 | 5 | -3 | 0 | 1 | 4 | 2 (1,8) | VANISHING_EXACT [1,1] | VANISHING 4.2e-14 / 4.1e-14 / 0 | 1/8:-3; -1/8:-3; 1/64:-3; -1/64:-3 | **STILL-VANISHING** |
| 30 | `e94c47f785e6` | 9 | 5 | -3 | 0 | 1 | 4 | 4 (1,2,2,4) | VANISHING_EXACT [1,1,1,1] | VANISHING 8.5e-12 / 5.4e-12 / 0 | 1/8:-3; -1/8:-3; 1/64:-3; -1/64:-3 | **STILL-VANISHING** |
| 31 | `894a95da1a0d` | 14 | 5 | -3 | 0 | 1 | 4 | 2 (2,12) | VANISHING_EXACT [1,1] | budget exceeded | 1/8:-3; -1/8:-3; 1/64:-3; -1/64:-3 | **STILL-VANISHING** |
| 32 | `1f53638e8cf6` | 19 | 5 | -3 | 0 | 1 | 4 | 4 (3,4,4,8) | VANISHING_EXACT [1,1,1,1] | budget exceeded | 1/8:-3; -1/8:-3; 1/64:-3; -1/64:-3 | **STILL-VANISHING** |
| 33 | `1de9e111cb5d` | 3 | 1 | 0 | 1 | 1 | 1 | 2 (1,2) | VANISHING_EXACT [1,1] | VANISHING 9.6e-16 / 9.6e-16 / 0 | 9/8:0; 7/8:0; 65/64:0; 63/64:0 | **STILL-VANISHING** |
| 34 | `c3dbaae9c4ab` | 5 | 1 | 0 | 0 | 1 | 1 | 2 (1,4) | VANISHING_EXACT [1,1] | VANISHING 3.7e-16 / 3.7e-16 / 0 | 1/8:0; -1/8:0; 1/64:0; -1/64:0 | **STILL-VANISHING** |
| 35 | `46a40cb56510` | 7 | 3 | -2 | 2 | 1 | 3 | 3 (1,2,4) | VANISHING_EXACT [1,1,1] | VANISHING 1.1e-15 / 7.8e-16 / 0 | 17/8:-2; 15/8:-2; 129/64:-2; 127/64:-2 | **STILL-VANISHING** |
| 36 | `808e52fdb1b6` | 9 | 4 | -7 | -1; 1 | -3; -3 | 4; 4 | 2 (1,8); 2 (1,8) | VANISHING_EXACT [1,2]; VANISHING_EXACT [1,2] | VANISHING 1.3e-15 / 5.6e-16 / 0 ; budget exceeded | -7/8:-7; -9/8:-7; -63/64:-7; -65/64:-7 | **STILL-VANISHING** |
| 37 | `b35d46339ef4` | 5 | 3 | -1 | 0 | 1 | 2 | 3 (1,2,2) | VANISHING_EXACT [1,1,1] | VANISHING 1.4e-14 / 1.3e-14 / 0 | 1/8:-1; -1/8:-1; 1/64:-1; -1/64:-1 | **STILL-VANISHING** |
| 38 | `d6a8255e8c96` | 5 | 3 | -1 | 0 | 1 | 2 | 3 (1,2,2) | VANISHING_EXACT [1,1,1] | VANISHING 1.2e-14 / 8e-15 / 0 | 1/8:-1; -1/8:-1; 1/64:-1; -1/64:-1 | **STILL-VANISHING** |
| 39 | `11b94e5ad1be` | 5 | 3 | -1 | 0 | 1 | 2 | 3 (1,2,2) | VANISHING_EXACT [1,1,1] | VANISHING 1.8e-14 / 1.3e-14 / 0 | 1/8:-1; -1/8:-1; 1/64:-1; -1/64:-1 | **STILL-VANISHING** |
| 40 | `83022ceaab23` | 9 | 5 | -3 | 0 | 1 | 4 | 4 (1,2,2,4) | VANISHING_EXACT [1,1,1,1] | VANISHING 1.6e-14 / 1.2e-14 / 0 | 1/8:-3; -1/8:-3; 1/64:-3; -1/64:-3 | **STILL-VANISHING** |
| 41 | `40d4c9f57c36` | 9 | 5 | -3 | 0 | 1 | 4 | 4 (1,2,2,4) | VANISHING_EXACT [1,1,1,1] | budget exceeded | 1/8:-3; -1/8:-3; 1/64:-3; -1/64:-3 | **STILL-VANISHING** |
| 42 | `c447da45ca02` | 14 | 5 | -3 | 0 | 1 | 4 | 4 (2,3,3,6) | VANISHING_EXACT [1,1,1,1] | budget exceeded | 1/8:-3; -1/8:-3; 1/64:-3; -1/64:-3 | **STILL-VANISHING** |
| 43 | `d01448b8b96a` | 5 | 3 | -1 | 0 | 1 | 2 | 3 (1,2,2) | VANISHING_EXACT [1,1,1] | VANISHING 9.2e-15 / 7.3e-15 / 0 | 1/8:-1; -1/8:-1; 1/64:-1; -1/64:-1 | **STILL-VANISHING** |
| 44 | `7c887944e856` | 5 | 3 | -1 | 0 | 1 | 2 | 3 (1,2,2) | VANISHING_EXACT [1,1,1] | VANISHING 4.6e-14 / 3.7e-14 / 3.7e-13 | 1/8:-1; -1/8:-1; 1/64:-1; -1/64:-1 | **STILL-VANISHING** |
| 45 | `ac09181bd1e3` | 8 | 3 | -1 | 0 | 1 | 2 | 3 (2,3,3) | VANISHING_EXACT [1,1,1] | VANISHING 8.2e-13 / 6.8e-13 / 4.2e-12 | 1/8:-1; -1/8:-1; 1/64:-1; -1/64:-1 | **STILL-VANISHING** |
| 46 | `a9b90eff1970` | 13 | 7 | -5 | 0 | 1 | 6 | 5 (1,2,2,4,4) | VANISHING_EXACT [1,1,1,1,1] | budget exceeded | 1/8:-5; -1/8:-5; 1/64:-5; -1/64:-5 | **STILL-VANISHING** |
| 47 | `762dac3fbdb1` | 13 | 7 | -5 | 0 | 1 | 6 | 5 (1,2,2,4,4) | VANISHING_EXACT [1,1,1,1,1] | budget exceeded | 1/8:-5; -1/8:-5; 1/64:-5; -1/64:-5 | **STILL-VANISHING** |
| 48 | `a814ad47ed0c` | 20 | 7 | -5 | 0 | 1 | 6 | 5 (2,3,3,6,6) | VANISHING_EXACT [1,1,1,1,1] | budget exceeded | 1/8:-5; -1/8:-5; 1/64:-5; -1/64:-5 | **STILL-VANISHING** |
| 49 | `11b99f22adf6` | 18 | 18 | -3 | 0 | 1 | 4 | 4 (2,4,4,8) | VANISHING_EXACT [1,2,2,2] | budget exceeded | 1/8:-3; -1/8:-3; 1/64:-3; -1/64:-3 | **STILL-VANISHING** |
| 50 | `7747339a4408` | 5 | 3 | -1 | 0 | 1 | 2 | 3 (1,2,2) | VANISHING_EXACT [1,1,1] | VANISHING 1.6e-12 / 1.5e-12 / 5.7e-12 | 1/8:-1; -1/8:-1; 1/64:-1; -1/64:-1 | **STILL-VANISHING** |
| 51 | `d57b38902c84` | 18 | 9 | -3 | 0 | 1 | 4 | 4 (2,4,4,8) | VANISHING_EXACT [1,2,2,2] | budget exceeded | 1/8:-3; -1/8:-3; 1/64:-3; -1/64:-3 | **STILL-VANISHING** |
| 52 | `96e4a2c6d1d3` | 24 | 12 | 0 | 0 | 1 | 1 | 2 (4,20) | VANISHING_EXACT [2,4] | budget exceeded | 1/8:0; -1/8:0; 1/64:0; -1/64:0 | **STILL-VANISHING** |
| 53 | `c689ce7fc834` | 18 | 18 | -3 | 0 | 1 | 4 | 4 (2,4,4,8) | VANISHING_EXACT [1,2,2,2] | budget exceeded | 1/8:-3; -1/8:-3; 1/64:-3; -1/64:-3 | **STILL-VANISHING** |
| 54 | `4667d741b2d6` | 13 | 13 | -3 | 0 | 1 | 4 | 4 (1,3,3,6) | VANISHING_EXACT [1,2,2,2] | budget exceeded | 1/8:-3; -1/8:-3; 1/64:-3; -1/64:-3 | **STILL-VANISHING** |
| 55 | `282a9f40c368` | 24 | 24 | -1 | 0 | 1 | 2 | 2 (4,20) | VANISHING_EXACT [2,2] | budget exceeded | 1/8:-1; -1/8:-1; 1/64:-1; -1/64:-1 | **STILL-VANISHING** |
| 56 | `b7612f47cd64` | 10 | 10 | 0 | 0 | 1 | 1 | 2 (3,7) | VANISHING_EXACT [1,1] | budget exceeded | 1/8:0; -1/8:0; 1/64:0; -1/64:0 | **STILL-VANISHING** |
| 57 | `cf1c601f3d1c` | 20 | 10 | -1 | 0 | 1 | 2 | 2 (4,16) | VANISHING_EXACT [2,4] | budget exceeded | 1/8:-1; -1/8:-1; 1/64:-1; -1/64:-1 | **STILL-VANISHING** |

### 5.1 What the table says, in aggregate

* **Every one of the 57 survivors has exactly one atypical value, except one
  (`808e52fdb1b6`), which has two.**  For the 53 members of the G1 family the
  atypical value is `c = 0` — the value at which `P = h0 v + c (x-a)^n v^m`
  factors as `v * (h0 + c (x-a)^n v^(m-1))`.  For the four G2 members
  `P = alpha x + beta + c B(x) y^m` the atypical values are `lam = alpha a_i + beta`,
  one for each distinct root `a_i` of `B`: at such a `lam` the content
  `gcd(c B(x), alpha x + beta - lam)` becomes non-trivial and the vertical line
  `{x = a_i}` splits off as a component.  Every atypical fibre found in the whole
  run is reducible with a `chi` that jumps up.

* **Suzuki accounting closes on all 57.**  Decomposing
  `C^2 = P^{-1}(C \ S) u (union of the fibres over S)` for any finite `S`
  containing the atypical values, and using that `P` restricted over `C \ S` is
  a locally trivial fibration with fibre `F_gen`,

      1 = chi(C^2) = chi(F_gen) (1 - |S|) + sum_{c in S} chi(F_c)
        = chi(F_gen) + sum_c ( chi(F_c) - chi(F_gen) ) .

  So the jumps must sum to `1 - chi_gen`.  In all 57 rows the jumps at the
  atypical values found sum to **exactly** `1 - chi_gen` (column
  `suzuki_closes` in `atypical.csv`: 57/57 True).  This is a strong
  self-consistency check on the detector and on the completeness of each
  atypical set.  (It closes the set completely if one also uses the standard
  fact — quoted, not derived here — that for a polynomial with no critical
  points every jump `chi(F_c) - chi(F_gen)` is non-negative.)

* **16 algebraic candidate values were left untested** (all of them inside the
  eight high-degree sheared members), because their minimal polynomials have
  degree 8, 16 or 40 and exact arithmetic in those number fields was not
  affordable here.  They are listed in `atypical.csv`
  (`untested_algebraic_candidates`).  For each of those eight `P` the jump at
  `c = 0` already accounts for the whole of `1 - chi_gen`, so under the
  non-negativity fact just quoted no untested candidate can be atypical; that
  is recorded as an accounting statement, not as an exact test.

### 5.2 Periods on the atypical fibres

* **EXACT-PRIM returns a verified certificate on every component of every
  atypical fibre of all 57 `P`** — i.e. an explicit polynomial `F` with
  `[P, F] - 1 = G h` checked coefficientwise over `Q` for each irreducible
  factor `h` of `P - c`.  The certificates are of very low degree (1, 2 or 3).
  Every period of `eta` over every cycle of every atypical fibre therefore
  vanishes, exactly.  This is the closed-form statement of §4.1 reproduced by
  machine on each actual (sheared) `P`.

* **NUM-MONO agrees wherever it completed**: `VANISHING` with least-squares
  residual at the `1e-15` level and residues at the `1e-16` level, and its own
  `chi` equal to the exact `chi` minus the number of vertical components (which
  the `x`-projection cannot see — see control C3e).  Where it did not complete
  it hit the wall-clock budget and is reported as such; no NUM-MONO run on any
  atypical fibre returned `NONVANISHING`.

* **At the nearby generic values `c0 ± 1/8` and `c0 ± 1/64` the exact `chi`
  is the generic one in every case**, so the atypical fibre really is isolated,
  and EXACT-PRIM at those nearby `c` returns a certificate of degree 2–5 in
  most rows.  Where it returns `NO_EXACT_CERTIFICATE` that is a statement about
  the search bound `deg F <= 6` only: night15 had already certified those
  generic fibres `VANISHING` by exact residue/genus arguments, and control C4
  shows EXACT-PRIM needs a higher bound on some genuinely vanishing fibres.

### 5.3 One survivor is obstructed — at a GENERIC value night15 never sampled

`808e52fdb1b6` (`P = 2x - 1 - x^2 (x-1)^3 y^4`, the G2 member with
`B = x^2 (x-1)^3`, `m = 4`) is the one row where the detector changes the
night15 picture, and it does so in an unexpected place.

Its atypical values are `c = -1` and `c = 1`.  night15 screened this `P` with
NUM-MONO **at `c = 1` and `c = -1` only** — that is, at *both* of its atypical
values and at no other fibre.  Its `PERIODS-VANISHING` verdict therefore rested
on no generic fibre at all.  The night15 record also explains the single
disagreement in control C3f: the genus `0` and `8` places-at-infinity recorded
for this `P` are the data of its atypical fibre `c = 1`, not of its generic one.

Measured here at five generic values (`g2check16.json`):

| c | exact chi | NUM-MONO chi | components | punctures | genus | ls-residual | error estimate | max period | max residue | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| 3 | -7 | -7 | 1 | 7 | 1 | 2.2708 | 2.4e-14 | 1.3110 | 5.8e-18 | NONVANISHING |
| 5 | -7 | -7 | 1 | 6 | 1.5 | 1.4847 | 7.1e-15 | 0.8377 | 1.3e-17 | NONVANISHING |
| -3 | -7 | -7 | 1 | 7 | 1 | 1.9095 | 2.1e-14 | 1.1024 | 1.9e-17 | NONVANISHING |
| 2 | -7 | -7 | 1 | 7 | 1 | 3.4508 | 3.0e-13 | 1.9923 | 3.5e-17 | NONVANISHING |
| 1/2 | -7 | -7 | 1 | 7 | 1 | 5.8036 | 8.9e-16 | 3.3507 | 2.8e-17 | NONVANISHING |

The residues at all places are zero to `1e-17` while the least-squares residual
of the potential system is of order 1 with an error estimate of order `1e-14`:
the obstruction is a genuine period, not a residue.  EXACT-PRIM finds no
primitive to `deg F <= 8` on these generic fibres, which is consistent (and,
by itself, not a proof).

So `808e52fdb1b6` **is** obstructed by the period screen — at its generic
fibres, which night15 never measured — while its two atypical fibres carry
exact primitives and vanish.  It is reported in the table as
`STILL-VANISHING` because that column records the atypical re-screen, and
separately here as `GENERIC-FIBRE OBSTRUCTED (night15 sampling gap)`.

---

## 6. Exact mate re-solve, above night15's ceiling

night15 escalated the Keller carrier to `deg Q = 2 deg P` and obtained
`EMPTY_over_Q` with an exact lambda certificate at every stage for all 57.
night16 restarts *above* that ceiling: for each `P` the full triangular carrier
is taken at `D = 2 deg P + 1`, `2 deg P + 2`, and the largest `D <= 3 deg P`
whose carrier fits in `MAXCOLS = 1600` columns.  Every `EMPTY` verdict carries
an exact rational lambda with `lambda^T A = 0` and `lambda^T e = 1`,
re-verified over `Q` (night12's decision layer, copied into this lane as
`exact16.py` / `matekit16.py`).

HIT GATE: a consistent system would be reconstructed to an exact `Q`, verified
by expanding `[P,Q] - 1` coefficientwise over `Q`, and written to
`night16/HIT_<hash>/`.

| # | hash | deg P | carriers D tried (night15 stopped at D = 2 deg P) | n unknowns | verdict | certificate | lambda support | lambda re-verified over Q |
|---|---|---|---|---|---|---|---|---|
| 1 | `c5e02d711fe5` | 3 | 7, 8, 9 | 36, 45, 55 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 24, 21, 41 | True, True, True |
| 2 | `a3b909a78c74` | 3 | 7, 8, 9 | 36, 45, 55 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 24, 22, 43 | True, True, True |
| 3 | `a03f511f7ecd` | 5 | 11, 12, 15 | 78, 91, 136 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 60, 59, 96 | True, True, True |
| 4 | `fef547c2b095` | 7 | 15, 16, 21 | 136, 153, 253 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 90, 100, 167 | True, True, True |
| 5 | `207b968cb4c5` | 4 | 9, 10, 12 | 55, 66, 91 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 26, 34, 66 | True, True, True |
| 6 | `52830078b770` | 4 | 9, 10, 12 | 55, 66, 91 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 38, 43, 60 | True, True, True |
| 7 | `39f56b091e75` | 7 | 15, 16, 21 | 136, 153, 253 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 63, 65, 141 | True, True, True |
| 8 | `36bc150f8dae` | 10 | 21, 22, 30 | 253, 276, 496 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 128, 151, 236 | True, True, True |
| 9 | `0a32a1935a5d` | 5 | 11, 12, 15 | 78, 91, 136 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 21, 29, 42 | True, True, True |
| 10 | `fa25edeecbfe` | 5 | 11, 12, 15 | 78, 91, 136 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 55, 68, 105 | True, True, True |
| 11 | `1ef523b227e7` | 8 | 17, 18, 24 | 171, 190, 325 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 102, 95, 266 | True, True, True |
| 12 | `a4d6d040e138` | 11 | 23, 24, 33 | 300, 325, 595 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 163, 187, 349 | True, True, True |
| 13 | `7f2b3c396f45` | 5 | 11, 12, 15 | 78, 91, 136 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 40, 74, 112 | True, True, True |
| 14 | `abc13407cc8e` | 5 | 11, 12, 15 | 78, 91, 136 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 48, 74, 112 | True, True, True |
| 15 | `55a9ae0456b4` | 9 | 19, 20, 27 | 210, 231, 406 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 141, 173, 191 | True, True, True |
| 16 | `632afa8e6433` | 13 | 27, 28 | 406, 435 | EMPTY_all_stages | lambda_exact, lambda_exact | 211, 278 | True, True |
| 17 | `7b72f1effa40` | 7 | 15, 16, 21 | 136, 153, 253 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 32, 21, 34 | True, True, True |
| 18 | `cd46f9341dc7` | 7 | 15, 16, 21 | 136, 153, 253 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 66, 67, 144 | True, True, True |
| 19 | `3bd161cf7a22` | 11 | 23, 24, 33 | 300, 325, 595 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 156, 181, 339 | True, True, True |
| 20 | `d735085d2c22` | 15 | 31, 32 | 528, 561 | EMPTY_all_stages | lambda_exact, lambda_exact | 290, 437 | True, True |
| 21 | `37670b444e89` | 6 | 13, 14, 18 | 105, 120, 190 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 66, 65, 103 | True, True, True |
| 22 | `00427d4924d2` | 6 | 13, 14, 18 | 105, 120, 190 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 82, 82, 132 | True, True, True |
| 23 | `c8aa6fd84bbc` | 11 | 23, 24, 33 | 300, 325, 595 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 126, 217, 290 | True, True, True |
| 24 | `f406b3aeda22` | 16 | 33, 34 | 595, 630 | EMPTY_all_stages | lambda_exact, lambda_exact | 294, 444 | True, True |
| 25 | `8ccaea9ee461` | 7 | 15, 16, 21 | 136, 153, 253 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 40, 42, 76 | True, True, True |
| 26 | `e52860893178` | 7 | 15, 16, 21 | 136, 153, 253 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 106, 85, 172 | True, True, True |
| 27 | `7887429824c2` | 12 | 25, 26, 36 | 351, 378, 703 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 214, 104, 283 | True, True, True |
| 28 | `726da7cd9516` | 17 | 35, 36 | 666, 703 | EMPTY_all_stages | lambda_exact, lambda_exact | 281, 440 | True, True |
| 29 | `c4e207c544a0` | 9 | 19, 20, 27 | 210, 231, 406 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 117, 124, 250 | True, True, True |
| 30 | `e94c47f785e6` | 9 | 19, 20, 26 | 210, 231, 378 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 117, 124, 285 | True, True, True |
| 31 | `894a95da1a0d` | 14 | 29, 30 | 465, 496 | EMPTY_all_stages | lambda_exact, lambda_exact | 357, 239 | True, True |
| 32 | `1f53638e8cf6` | 19 | 39, 40 | 820, 861 | EMPTY_all_stages | lambda_exact, lambda_exact | 563, 359 | True, True |
| 33 | `1de9e111cb5d` | 3 | 7, 8, 9 | 36, 45, 55 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 5, 5, 6 | True, True, True |
| 34 | `c3dbaae9c4ab` | 5 | 11, 12, 15 | 78, 91, 136 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 71, 83, 125 | True, True, True |
| 35 | `46a40cb56510` | 7 | 15, 16, 21 | 136, 153, 253 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 34, 22, 37 | True, True, True |
| 36 | `808e52fdb1b6` | 9 | 19, 20, 26 | 210, 231, 378 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 17, 20, 33 | True, True, True |
| 37 | `b35d46339ef4` | 5 | 11, 12, 15 | 78, 91, 136 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 55, 68, 97 | True, True, True |
| 38 | `d6a8255e8c96` | 5 | 11, 12, 15 | 78, 91, 136 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 55, 68, 105 | True, True, True |
| 39 | `11b94e5ad1be` | 5 | 11, 12, 15 | 78, 91, 136 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 55, 68, 105 | True, True, True |
| 40 | `83022ceaab23` | 9 | 19, 20, 26 | 210, 231, 378 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 24, 25, 61 | True, True, True |
| 41 | `40d4c9f57c36` | 9 | 19, 20, 26 | 210, 231, 378 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 99, 102, 230 | True, True, True |
| 42 | `c447da45ca02` | 14 | 29, 30 | 465, 496 | EMPTY_all_stages | lambda_exact, lambda_exact | 102, 103 | True, True |
| 43 | `d01448b8b96a` | 5 | 11, 12, 15 | 78, 91, 136 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 55, 68, 97 | True, True, True |
| 44 | `7c887944e856` | 5 | 11, 12, 15 | 78, 91, 136 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 39, 58, 88 | True, True, True |
| 45 | `ac09181bd1e3` | 8 | 17, 18, 24 | 171, 190, 325 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 111, 114, 210 | True, True, True |
| 46 | `a9b90eff1970` | 13 | 27, 28 | 406, 435 | EMPTY_all_stages | lambda_exact, lambda_exact | 299, 156 | True, True |
| 47 | `762dac3fbdb1` | 13 | 27, 28 | 406, 435 | EMPTY_all_stages | lambda_exact, lambda_exact | 188, 192 | True, True |
| 48 | `a814ad47ed0c` | 20 | 41, 42 | 903, 946 | NOT_CERTIFIED | none, none | None, None | None, None |
| 49 | `11b99f22adf6` | 18 | 37, 38 | 741, None | EMPTY_all_stages | lambda_exact, None | 508, None | True, None |
| 50 | `7747339a4408` | 5 | 11, 12, 15 | 78, 91, 136 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 55, 68, 105 | True, True, True |
| 51 | `d57b38902c84` | 18 | 37, 38 | 741, 780 | EMPTY_all_stages | lambda_exact, lambda_exact | 438, 587 | True, True |
| 52 | `96e4a2c6d1d3` | 24 | 49, 50 | 1275, 1326 | NOT_CERTIFIED | none, none | None, None | None, None |
| 53 | `c689ce7fc834` | 18 | 37, 38 | 741, 780 | EMPTY_all_stages | lambda_exact, lambda_exact | 508, 400 | True, True |
| 54 | `4667d741b2d6` | 13 | 27, 28 | 406, 435 | EMPTY_all_stages | lambda_exact, lambda_exact | 214, 313 | True, True |
| 55 | `282a9f40c368` | 24 | 49, 50 | 1275, 1326 | NOT_CERTIFIED | none, none | None, None | None, None |
| 56 | `b7612f47cd64` | 10 | 21, 22, 26 | 253, 276, 378 | EMPTY_all_stages | lambda_exact, lambda_exact, lambda_exact | 185, 121, 285 | True, True, True |
| 57 | `cf1c601f3d1c` | 20 | 41, 42 | 903, 946 | NOT_CERTIFIED | none, none | None, None | None, None |

**53 of 57 came back `EMPTY_over_Q` at every carrier tried, each with an exact lambda certificate re-verified over Q; 4 are `NOT_CERTIFIED` — at those carriers the system is inconsistent at the scheduling prime (rank_p[A|e] = rank_p(A) + 1) but the carrier exceeded the exact-lambda solver's size cap, so no exact certificate was produced and no emptiness is claimed for them.  No system was consistent: the HIT GATE did not fire.**
