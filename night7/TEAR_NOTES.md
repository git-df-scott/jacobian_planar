# night7 — TEAR EVALUATOR notes

Detector for the non-properness locus (Jelonek set / asymptotic variety) of a
polynomial map `F = (P, Q) : A^2 -> A^2`.

Code: `night7/tear.py`. Raw run output: `night7/tear_run.json`.
Controls C1/C2/C3 run at import and hard-exit (`sys.exit(1)`) on failure; C4 is a
measurement with no pass/fail.

These notes record measurements and the literature statement implemented. No
conclusions are drawn.

---

## 1. Literature statement implemented (exact)

### 1.1 The statement the code implements

**Jelonek, "Note about the set `S_f` for a polynomial mapping `f : C^2 -> C^2`",
Bull. Polish Acad. Sci. Math. **49**(1) (2001), 67–72, Theorem 2.2.**

I could not obtain the full text of that Bulletin note online. I therefore used
its verbatim restatement, with attribution, in a paper I did read in full:

> **Theorem 2.3 ([21, Thm. 2.2]).** Consider a dominant polynomial map
> `f : C^2 -> C^2`, `(x_1,x_2) |-> f(x_1,x_2)`. Let
> `P_i(y_1,y_2,x_i) = sum_{k=0}^{n_i} P_{ik}(y_1,y_2) x_i^{n_i-k}` be the
> resultant of the polynomials `(f_1 - y_1, f_2 - y_2)` with respect to `x_j`
> for distinct `i,j in {1,2}`. Then, the Jelonek set of `f` is
> `{(y_1,y_2) in C^2 | P_{1,0} P_{2,0} = 0}`.

— B. El Hilany, E. Tsigaridas, *Computing the non-properness set of real
polynomial maps in the plane*, arXiv:2101.05245v3 [math.AG] (26 Jun 2023),
Section 2, Theorem 2.3, where reference `[21]` is exactly the Jelonek 2001
Bulletin note above.

The same paper gives the pseudo-code (its Algorithm 2, `Jelonek_2`) that
`tear.py` implements line for line:

```
1  g1 <- f1(x1,x2) - y1
2  g2 <- f2(x1,x2) - y2
3  r1 <- res_{x2}(g1,g2)  in (Z[y1,y2])[x1]
4  r2 <- res_{x1}(g1,g2)  in (Z[y1,y2])[x2]
5  p  <- lc_{x1}(r1) * lc_{x2}(r2)  in Z[y1,y2]
6  return p
```

In `tear.py`'s naming: `y1 = u`, `y2 = v`, `x1 = x`, `x2 = y`,
`R1 = res_y(P-u, Q-v)` (a polynomial in `x` over `Z[u,v]`) and
`R2 = res_x(P-u, Q-v)` (a polynomial in `y` over `Z[u,v]`).

### 1.2 The underlying general-`n` statement

**Jelonek, "The set of points at which a polynomial map is not proper",
Ann. Polon. Math. **58**(3) (1993), 259–266, Proposition 7** (read verbatim from
the ICM full text, `matwbn.icm.edu.pl/ksiazki/apm/apm58/apm5834.pdf`):

> **Proposition 7.** Let `f : C^n -> C^n` be a dominant polynomial map and let
> `C(f_1,...,f_n) ⊂ C(x_1,...,x_n)` be the induced field extension. Let
> `sum_{k=0}^{n_i} a^i_k(f) x_i^{n_i-k} = 0`, where the `a^i_k` are polynomials,
> be an **irreducible equation** of `x_i` over `C[f_1,...,f_n]`. Let
> `S = union_{i=1}^n {y in C^n : a^i_0(y) = 0}`. Then `f` is proper at a point
> `y` if and only if `y in C^n \ S`.

and its **Corollary 9** (`S` is either empty or a hypersurface) and **Remark
10 b)** ("We can effectively find an equation of the hypersurface `S`", via
Gröbner bases for the ideals `I_k = (y_1-f_1,...,y_n-f_n, y_{n+1}-x_k)`).

### 1.3 Difference from the task sketch, and why it matters

The task sketch said the non-properness set is *contained in* the union of the
zero sets of the leading coefficients. The literature is sharper, and the two
statements differ in a way that is worth recording:

* **Prop. 7 (1993)** is an equality, but only for the **irreducible (minimal)
  equation** of `x_i` over `C[f_1,...,f_n]` — i.e. for the leading coefficient
  of the *minimal polynomial* of `x_i`, not of the raw resultant. The raw
  resultant `res_{x_j}(f_1-y_1, f_2-y_2)` is in general a proper multiple of
  that minimal polynomial (extra factors, extra content), so replacing the
  minimal polynomial by the raw resultant gives, a priori, only a
  **containment** `S_f ⊆ V(lc(r_1) · lc(r_2))` — which is exactly the sketch in
  the task.
* **Thm. 2.2 (2001), for `n = 2` only**, upgrades this to an **equality** for
  the raw resultant: `J_f = {P_{1,0} P_{2,0} = 0}`. This is the statement the
  code implements, and it is what licenses reading the computed locus as *the*
  Jelonek set rather than as an upper bound — but only for `n = 2`, only over
  `C`, and only for **dominant** `f`.

`tear.py` therefore reports both: the locus polynomial `lc(R1)·lc(R2)` and its
factorisation, plus flags for every hypothesis that is not met.

### 1.4 Hypotheses and degenerate cases handled explicitly

`tear.py` never silently swallows a degeneracy. Flags emitted:

| flag | meaning |
|---|---|
| `NOT_DOMINANT` | `det Jac(P,Q) == 0`; Thm. 2.2 hypothesis "dominant" fails |
| `RESULTANT_IDENTICALLY_ZERO:R1/R2` | the resultant vanishes identically (a common factor / non-generically-finite situation); no leading coefficient exists, locus is not computed |
| `DEGREE_ZERO_IN_SOURCE_VAR:R1/R2` | the resultant is free of the surviving source variable; the "leading coefficient" is the resultant itself |
| `DEGREE_DROP:Rk(a<b)` | the actual degree `a` in the source variable is below the Sylvester bound `b = deg_s(g1)·deg_e(g2) + deg_s(g2)·deg_e(g1)`; i.e. degree drops for **all** `(u,v)`, not just special ones |
| `POSITIVE_CHARACTERISTIC` | computation is over `GF(p)`; the characteristic-zero theorem is **not** claimed to apply |
| `FACTORISATION_UNAVAILABLE` | sympy cannot factor a genuinely multivariate polynomial over `GF(p)`; a partial description is reported instead of a fabricated factorisation |

Ground field: exact `Q` (via `ZZ[u,v]` coefficient rings) for C1/C2/C3;
`GF(2)` for C4. `GF(999983)` is reachable with `tear(P, Q, char=999983)`.

---

## 2. Hand derivation for C2: `F = (x, x*y)`

Expected answer, derived by hand before running the evaluator.

`F(x,y) = (u,v) = (x, xy)`.

**Dominance.** `det Jac = det [[1, 0], [y, x]] = x ≢ 0`, so `F` is dominant and
Thm. 2.2 applies.

**Fibres.** For `u ≠ 0` the system `x = u`, `xy = v` has the unique solution
`(x,y) = (u, v/u)`, which stays in a bounded set as `(u,v)` ranges over a
compact set avoiding `{u = 0}`. So `F` is proper over `C^2 \ {u = 0}`.

**Points of non-properness.** Fix any `v_0`.
* If `v_0 ≠ 0`: take `x_k = 1/k`, `y_k = k v_0`. Then `F(x_k,y_k) = (1/k, v_0)
  -> (0, v_0)` while `|(x_k,y_k)| -> ∞`.
* If `v_0 = 0`: take `x_k = 1/k^2`, `y_k = k`. Then `F(x_k,y_k) =
  (1/k^2, 1/k) -> (0,0)` while `|(x_k,y_k)| -> ∞`.

So every point of the line `{u = 0}` lies in `S_F`, and by the previous
paragraph no other point does.

**Conclusion (hand):** `S_F = {u = 0}`, the line `u = 0`, exactly.

**Hand resultant computation.**
`g1 = x - u`, `g2 = xy - v`.

* `R1 = res_y(g1, g2)`: `deg_y g1 = 0`, so `R1 = g1^{deg_y g2} = (x - u)^1`.
  Degree in `x` is `1`, `lc_x(R1) = 1`.
* `R2 = res_x(g1, g2)`: both are degree `1` in `x`; the Sylvester determinant is
  `det [[1, -u], [y, -v]] = -v + u y`. Degree in `y` is `1`, `lc_y(R2) = u`.
* Locus polynomial: `1 · u = u`, so the locus is `{u = 0}`.

This matches the hand-derived `S_F` exactly, and matches the evaluator output
(`locus_polynomial = "u"`, `locus_components = ["u"]`).

---

## 3. Calibration table

`R1 = res_y(P-u, Q-v) ∈ (Z[u,v])[x]`, `R2 = res_x(P-u, Q-v) ∈ (Z[u,v])[y]`.
"deg" = degree in the surviving source variable; "bound" = Sylvester bound.
Locus = `V(lc_x(R1) · lc_y(R2))`.

### C1 — tame automorphisms (char 0, exact over Q) — locus must be EMPTY

| # | map `(P, Q)` | `R1` | deg / bound | `lc_x(R1)` | `R2` | deg / bound | `lc_y(R2)` | locus poly | locus |
|---|---|---|---|---|---|---|---|---|---|
| T1 deg 2 | `(x, x^2+y)` | `x - u` | 1 / 1 | `1` | `y - v + u^2` | 1 / 1 | `1` | `1` | **EMPTY** |
| T2 deg 3 | `(x+y^3+2y-1, 3x+3y^3+7y+5)` | `-x + 27u^3 - 27u^2v + 216u^2 + 9uv^2 - 144uv + 583u - v^3 + 24v^2 - 194v + 529` | 1 / 6 | `-1` | `y + 3u - v + 8` | 1 / 6 | `1` | `-1` | **EMPTY** |
| T3 deg 4 | `(x+y^2, x^2+2xy^2+y^4+y)` | `x + u^4 - 2u^2v - u + v^2` | 1 / 8 | `1` | `y + u^2 - v` | 1 / 8 | `1` | `1` | **EMPTY** |
| T4 deg 5 | `(2x+y+(x+y-3)^5, x+y-3)` | `-x + u - v^5 - v - 3` | 1 / 10 | `-1` | `y + u - v^5 - 2v - 6` | 1 / 10 | `1` | `-1` | **EMPTY** |
| T5 deg 6 | `(x^6+2x^3y+x+y^2, x^3+y)` | `x - u + v^2` | 1 / 12 | `1` | `-y - u^3 + 3u^2v^2 - 3uv^4 + v^6 + v` | 1 / 12 | `-1` | `-1` | **EMPTY** |

(T2 = `aff(1,2,3,7,-1,5) ∘ (x+y^3, y)`; T3 = `(x, y+x^2) ∘ (x+y^2, y)`;
T4 = `(x+y^5, y) ∘ aff(2,1,1,1,0,-3)`; T5 = `(x+y^2, y) ∘ (x, y+x^3)`.)

`DEGREE_DROP` is flagged on T2–T5: for an automorphism both resultants are
linear in the surviving source variable, far below the Sylvester bound. The
leading coefficients are units (`±1`), so the locus polynomial is a nonzero
constant and the locus is empty. **C1 outcome: PASS (5/5 empty).**

### C2 — `(x, x*y)` (char 0) — locus must be nonempty and equal `{u = 0}`

| | `R1` | deg / bound | `lc_x(R1)` | `R2` | deg / bound | `lc_y(R2)` | locus poly | locus |
|---|---|---|---|---|---|---|---|---|
| `(x, xy)` | `x - u` | 1 / 1 | `1` | `uy - v` | 1 / 1 | `u` | `u` | `{u = 0}` |

Components `["u"]`, `locus_empty = False`, no flags. Agrees with the hand
derivation in §2. **C2 outcome: PASS.**

### C3 — `(x^2, y)` (char 0) — locus must be EMPTY

| | `R1` | deg / bound | `lc_x(R1)` | `R2` | deg / bound | `lc_y(R2)` | locus poly | locus |
|---|---|---|---|---|---|---|---|---|
| `(x^2, y)` | `x^2 - u` | 2 / 2 | `1` | `y^2 - 2vy + v^2` | 2 / 2 | `1` | `1` | **EMPTY** |

No flags. The map is finite (2:1 onto `A^2`), and the locus is empty even
though the map is not injective. **C3 outcome: PASS.**

### C4 — MEASUREMENT ONLY, characteristic 2

Pair from `night5/mondello/mondello_map.json` (Mondello, arXiv:2608.02634,
`k = closure(F_2)`):

```
P = x + x^2 y + x^4 + x^6 y^2
Q = y + x^5 + x^6 y + x^7 y^2 + x^8 y^3
```

Computed over `GF(2)`. **The characteristic-zero theorem of §1.1 is NOT claimed
to apply here.** This block is a record of what the same resultant /
leading-coefficient recipe produces in characteristic 2, nothing more.

`deg P = 8`, `deg Q = 11`, `det Jac = 1` in `GF(2)[x,y]`.

Verbatim locus data:

| quantity | value (over `GF(2)`) |
|---|---|
| `R1 = res_y(P-u, Q-v)` | `v^2 x^18 + u^3 x^16 + u v x^16 + x^16 + u x^15` |
| `deg_x R1` | `18` (Sylvester bound `34`) |
| `lc_x(R1) = P_{1,0}` | `v^2` |
| `R2 = res_x(P-u, Q-v)` | `y^19 + u^8 y^18 + u^5 y^18 + u v^2 y^18 + v^4 y^18 + v y^18 + u^3 v^2 y^17 + v^2 y^17 + u^5 v^2 y^16 + u^3 v^3 y^16 + u v^4 y^16 + v^6 y^16 + v^3 y^16` |
| `deg_y R2` | `19` (Sylvester bound `34`) |
| `lc_y(R2) = P_{2,0}` | `1` |
| locus polynomial `P_{1,0}·P_{2,0}` | `v^2` |
| locus (zero set of that polynomial) | `{v = 0}` |
| irreducible components | `["v"]` (monomial, factored by inspection) |
| `locus_empty` | `False` |
| flags | `POSITIVE_CHARACTERISTIC`, `DEGREE_DROP:R1(18<34)`, `DEGREE_DROP:R2(19<34)` |

Recorded as a characteristic-2 computation only.

---

## 4. Sources consulted

* Z. Jelonek, *The set of points at which a polynomial map is not proper*,
  Annales Polonici Mathematici **58**(3) (1993), 259–266.
  Full text read: http://matwbn.icm.edu.pl/ksiazki/apm/apm58/apm5834.pdf
  (record: https://eudml.org/doc/262458). Proposition 7, Corollary 9, Remark 10.
* Z. Jelonek, *Note about the set `S_f` for a polynomial mapping
  `f : C^2 -> C^2`*, Bull. Polish Acad. Sci. Math. **49**(1) (2001), 67–72,
  Theorem 2.2. **Not read directly** (no accessible full text found); used via
  the verbatim restatement below.
* B. El Hilany, E. Tsigaridas, *Computing the non-properness set of real
  polynomial maps in the plane*, arXiv:2101.05245v3 [math.AG], 26 Jun 2023.
  Read in full text: https://arxiv.org/pdf/2101.05245 — Section 2, Theorem 2.2
  (attributed to [19, Prop. 7] = Jelonek 1993), Theorem 2.3 (attributed to
  [21, Thm. 2.2] = Jelonek 2001), Algorithm 1 (`Jelonek_n`), Algorithm 2
  (`Jelonek_2`), Theorems 2.4/2.5 (complexity).
* Z. Jelonek, M. Lasoń, *Quantitative properties of the non-properness set of a
  polynomial map, a positive characteristic case*, arXiv:1906.06160.
  Read; it concerns uniruledness degree bounds in positive characteristic and
  supplies no resultant recipe, so it is cited here only as context for C4
  being labelled a characteristic-2 measurement.
