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
