# night12 -- MATE SEARCH v1

Measurements only. Nothing in this file is a conclusion.

> **STATUS ANNOTATION (added when the v1 pipeline was run to completion).**
> The results of the run are in **`V1_RESULTS.md`**; this file remains the
> method note. Four things recorded there amend what is written below.
>
> 1. **Section 5's family M1 does not survive S1.** All 200 M1/M1L `P` are
>    rejected by S1: for `P = x + A*H^2 + P_lower` the gradient is
>    `P_x = 1 + 2A H H_x + ...`, `P_y = 2A H H_y + ...`, so a common zero needs
>    `H = 0` (where `P_x = 1`, no zero) or `H_y = 0`; the latter is a union of
>    lines through the origin, and `1 + 2A H H_x` restricted to such a line has
>    degree `2m - 1 > 0` and therefore has roots. The shape carries gradient
>    common zeros generically, which reproduces at `m = 5, 8, 11, 14`. Such a
>    `P` has no mate at any degree, so the `mu_3` grading argument of section 5
>    is correct about the grading but is never reached.
> 2. **The carrier anchors were being scaled away.** Section 5 says carriers
>    are thinned with `(0,0)` and `(0,1)` always retained; in fact both
>    `carriers.carrier` and `v1.general_carrier` put the anchors into the base
>    point set *before* the stage scaling, so whenever the stage bound fell
>    below the polygon degree the anchor `(0,1)` was shrunk below the lattice
>    and dropped -- stage Y for every `P`, and stages Y and C for M1. For an M1
>    `P` the column `(0,1)` is the only one in the `mu_3` grading that can meet
>    the Keller constant row (through the linear term `x` of `P`, via
>    `a = (1,1) - (1,0)`), so with it gone that row was identically zero and
>    stage Y returned `EMPTY_over_Q` by the degenerate zero-row certificate for
>    every M1 `P` -- true of the carrier built, but vacuous. Fixed by adjoining
>    the anchors both scaled and unscaled, which makes every carrier a superset
>    of the old one at every stage.
> 3. **Section 3's S1 has a third outcome, `timeout`, which is undecided.**
>    22 `P` returned it in the screen phase and, since the driver selects by the
>    `passed` flag, fell out of the run with no verdict at all. They are picked
>    up by `s1_retry.py` (S1 again, longer budget) and by the override arms.
> 4. **Section 4's hit gate is unchanged and was never tripped.** 243 `P`
>    reached a decision arm; 20 mates were certified over `Q` by E3, all on `P`
>    that SY certifies `COORDINATE`.

Ring labels: **ring: Q** = exact rational arithmetic; **ring: F_p** = the
finite field, used in v1 for **scheduling only**.

v1 supersedes the decision procedure of `MATE_SEARCH.md` (v0). The v0 file now
carries a status annotation at its head recording why: v0's dual-prime gate
can produce **false negatives**, because reduction mod `p` can lower `rank(A)`
without lowering `rank([A|e])`, so a rationally consistent system can look
inconsistent mod `p` (`A = [p]`, `e = [1]` is the one-variable instance).
Every v0 negative is therefore **support-and-prime-relative**. In v1 no
verdict rests on a modular computation.

---

## 1. What makes a v1 verdict exact

Three certificate types, all checked over `Q`:

**(E1) `lambda_exact`.** An explicit rational vector `lambda` with
`lambda^T M = 0` on every column and `lambda^T e_00 = 1`, verified by exact
arithmetic. Its existence proves `M q = e` is unsolvable over `Q`. Two
sources: the degenerate one, where the constant row of `M` is identically zero
so `lambda = e_00` works verbatim (this is the whole certificate for a `P`
with a gradient zero at the origin); and the general one, solved by exact
`Fraction` elimination on the pivot-row block, whose left null space is
one-dimensional and so canonical once normalised by `lambda^T e_00 = 1`.

**(E2) `rank_full_column_exact`.** If the scheduling prime returns
`rank_p(A) = n` and `rank_p([A|e]) = n+1` (with `n` the unknown count after
kernel deflation), then since reduction mod `p` can only *lower* rank, both
numbers are **lower bounds** for the ranks over `Q`:

```
rank_Q(A)     >= rank_p(A) = n,   and  rank_Q(A) <= n   (only n columns)
rank_Q([A|e]) >= rank_p([A|e]) = n+1 > n = rank_Q(A)
```

so the system is inconsistent over `Q`. The lower-bound direction is what
makes this exact rather than probabilistic; the random row compression can
only lower ranks too, so it cannot manufacture this certificate. This is
exactly the configuration v0 could not tell apart from a false negative.

**(E3) `exact_solution`.** A rational `Q` (reconstructed multi-modularly, by
CRT plus rational reconstruction) which is then certified by expanding
`P_x Q_y - P_y Q_x - 1` coefficientwise over `Q` and checking it is
identically zero. The reconstruction route is a search heuristic; the
expansion is the proof.

Anything reaching none of these is recorded as **`NOT_CERTIFIED`** and is
never reported as an emptiness result.

---

## 2. Kernel deflation (and why it is exactly right here)

The Keller system always carries the trivial directions `Q -> Q + h(P)`,
since `[P, f(P)] = 0`. They must be quotiented out or `A` cannot have full
column rank and certificate E2 can never fire.

For a `P` that has passed **S2** (`gcd(P_x,P_y)` a unit), `P` is not a proper
composition `h(R)`, so the exact kernel `{Q : [P,Q] = 0}` is precisely `Q[P]`.
Its part living on a carrier `S` is spanned by the powers `P^k` whose support
fits inside `S`. Deleting the single column at `lead(P)^k` for exactly those
`k` is a genuine quotient: the coefficients of a carrier `Q` at the monomials
`lead(P)^k` are triangular in the `c_k`, so every `Q` has a unique
representative with them zeroed. A `P^k` that does **not** fit the carrier
contributes no kernel and is **not** deflated -- deleting its column would
shrink the search space instead of quotienting it, and would make an
emptiness verdict false. The deflated dimension is recorded per stage as
`deflated_kernel_dim`.

So the deflation is complete *because* S2 ran first; the screen and the
solver are interlocked, not independent.

---

## 3. The P-screens (run before any mate matrix is built)

| screen | test | why it is a gate |
| --- | --- | --- |
| **S2** | `gcd(P_x, P_y)` is a unit (Singular, `ring 0,(x,y),dp`) | `P = h(R)` with `deg h > 1` gives `P_x = h'(R)R_x`, `P_y = h'(R)R_y`, so the gcd is nonconstant. Cheap, and run first. |
| **S1** | `1` in the ideal `(P_x, P_y)` over `Q` (Groebner, `std`, `dim == -1`) | at a common zero `(a,b)` of `P_x,P_y` the Keller equation reads `0 = 1`, so a common zero kills **every** mate. A cheap pre-check runs first: if `P_x` and `P_y` both have zero constant term the origin is a common zero. |
| **S3** | `places_at_infinity` = distinct roots of the leading form as a binary form; `genus_newton` = interior lattice points of `NP(P)` (Pick) | recorded as a **selection bias, not a gate**. Theorem on file: a `P` with rational irreducible generic fibre that has a mate is a coordinate, so a viable `P` wants positive genus or several places at infinity. `genus_newton` equals the geometric genus of the generic fibre only under nondegeneracy; it is recorded with that caveat. |

---

## 4. The non-coordinate certificate (Shpilrain-Yu), and the hit gate

Rows are the gradient pair `(P_x, P_y)` over `Q`, ordered by total degree then
lex. The elementary reduction is `f <- f - (LT(f)/LT(g))*g` whenever
`LM(g) | LM(f)`, and symmetrically; both directions apply only when
`LM(f) = LM(g)`, which is the only branch point. Normalised rows are
memoised; each reduction strictly lowers the leading monomial of the row it
touches, in a well-order, so the DAG terminates.

- reaching `(c, 0)`, `c` a nonzero constant -> **COORDINATE**
- a fully exhausted DAG with no such leaf -> **NON_COORDINATE**

**The hit gate** is: a mate `Q` certified over `Q` by E3, for a `P` that S1/S2
passed and that SY certifies **NON_COORDINATE**. Such a pair is written to
`night12/HIT_<hash>/` and the run stops.

---

## 5. Family M1 and the Q-degree escalation

**M1**, the cusp-square `mu_3` carrier, at the exact 2:3 profiles under 200:

```
deg P = n = 2m,  deg Q = 3m,   (n,3m) in {(126,189),(128,192),(130,195),(132,198)}
H_m       sparse form, monomials x^i y^(m-i) with i = 2 (mod 3), 2..6 terms
P         = x + A*H_m^2 + P_lower,  every P_lower monomial has i = 1 (mod 3)
Q carrier top B*H_m^3, exponents a = 0 (mod 3)
```

The `mu_3` grading closes: `supp(P)` sits in `a = 1 (mod 3)`, `supp(Q)` in
`a = 0 (mod 3)`, and then both `P_x Q_y` and `P_y Q_x` land in `a = 0 (mod 3)`,
which is the class containing the constant monomial the Keller equation needs.
A pleasant consequence: among the powers of `P` only `P^0 = 1` meets the
carrier grading (`P^k` sits in `a = k (mod 3)`, and `P^3` has degree `6m`,
above every stage bound), so on the M1 carrier the deflation is the single
column `(0,0)` -- whose column in `A` is identically zero anyway, since the
factor `p1*a2 - p2*a1` vanishes at `a = (0,0)`.

**Escalation stages**, per `P`, stopping at the first stage that yields a mate:

| stage | `deg Q` bound | carrier |
| --- | --- | --- |
| **Y** | `deg P - 1` (younger-mate stage) | stage-scaled `H^3` polygon (M1) or stage-scaled `NP(P)` (other pools) |
| **C** | `floor(3 deg P / 2)` | the `H^3` carrier |
| **W** | `2 deg P - 1` | widened |

Emptiness is never claimed beyond the stage actually tried: each stage records
its own carrier (`n_raw`, `thin_t`, `n_used`, `deflated_kernel_dim`) and its
own certificate. Carriers above `cap = 1500` are thinned (on `b` for M1, on
both exponents otherwise) and the thinning index is recorded.

---

## 6. Files

| file | contents |
| --- | --- |
| `sy.py` | Shpilrain-Yu certificate + validation set |
| `screens.py` | S1 / S2 (Singular) and S3 diagnostics |
| `carriers.py` | family M1 and the `mu_3` Q-carriers |
| `pool.py` | the screened P pools (M1, M1L, HDC, V0) |
| `exact.py` | the exact-over-Q decision layer (E1/E2/E3) |
| `v1.py` | driver: screen phase, pipeline phase, hit gate |
| `controls_v1.py` | brief item (6) controls + the SY validation set |
| `v1_screens.csv/.json` | one row per screened `P` |
| `v1_records.json`, `V1_RECORDS/` | one record per `P` through the pipeline |
| `controls_v1_log.txt`, `controls_v1.json` | control outcomes |
