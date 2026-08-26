# Lane 7 — exact modular sweep of the collision-first incidence variety

Date: 2026-08-26.  Prime `p = 1000003` throughout, cross-checked at `p = 1000033`.
All arithmetic exact over `F_p`; no floating point anywhere in the search path.

**Verdict: NO CANDIDATE.  Zero nondegenerate consistent hits, and zero degenerate
consistent hits either — the collision rows killed every solvable `P` the sweep
found, including the known ones.**  What the sweep did produce is the first
measurement of the rank profile of this incidence variety, four small exact
theorems that explain the measurement, and an exact graded reduction of the live
height-`(4,6)` frontier at its two smallest templates.

Files added (nothing in the git repo was touched):

| file | role |
|---|---|
| `lane7_lib.py` | vectorised mod-`p` RREF, template/tensor cache, `delta` functional, bottom-row sub-block, independent sympy bracket |
| `lane7_controls.py` | 23 can-fail controls |
| `lane7_sweep.py` | sweeps A–E |
| `lane7_descent.py`, `lane7_obstruction.py`, `lane7_exact_descent.py` | graded Newton descent and its exact obstruction |
| `sweep_all.log`, `lane7_results_all.json`, `obstruction.log`, `lane7_exact_descent.json` | raw output |

`incidence.py` and `search.py` were read and used unmodified.

---

## 1. Controls — 23/23 PASS

The engine's shipped `controls()` passes.  On top of it:

**(a) Provably inconsistent systems must return ZERO solutions.**

| control | why it must fail | result |
|---|---|---|
| `A1` `P = x^3 - x^2` | the constant coefficient of `[P,Q]` is `P10*Q01 - P01*Q10`, so a `P` with no linear part makes that row identically zero against rhs 1 | engine returns `None`; fast path agrees |
| `A2` `P = y(x^2-x)` | restricting `[P,Q]=1` to `y=0` gives `-P_y(x,0) q'(x) = 1` with `P_y(x,0)=x^2-x` nonconstant | `None` (both bracket-only and full) |
| `A3` `P = y` | `[P,Q]=1` **is** solvable (`Q=-x`) but every solution has `Q(1,0)-Q(0,0) = -1`, so the two collision rows must kill it | bracket-only consistent, full system `None`, `delta = -1` |
| `A4` **constant-row guard** | rigged support (`p_supp = {1,x,x^2}`, `q_supp` deliberately missing `(0,1)`) for which no basis element of `Q` can produce a constant term | the `(0,0)` row **is present and identically zero** against rhs 1, and the engine correctly returns `None` |

`A4` is the exact bug that was warned about.  `Incidence.create` seeds
`targets = {(0,0)}` unconditionally and `system()` writes `rhs[target_index[(0,0)]] = 1`,
so the constant row cannot be dropped.  A **negative control** confirms the guard
can fail: deleting that one row from the same matrix makes `solve_affine` report
success (returning the identically-zero `Q`, i.e. solving `[P,Q]=0`) on a system
whose true answer is "inconsistent".

**(b) Every returned `Q` replayed independently.**  `lane7_lib.replay` rebuilds
`P_x Q_y - P_y Q_x` by symbolic differentiation in sympy over `Z` and reduces mod
`p`; it shares no code with `incidence.bracket`.  Every `Q` returned anywhere in
this lane (controls, sweeps, descent) was replayed this way.  No replay failure
occurred.

**(c) Systems known to admit solutions must return them.**

* `C0` (end-to-end positive control, the only one that exercises the *whole*
  pipeline including the collision rows): over `F_3`, `P = x^3 - x`, `Q = -y` is a
  genuine Artin–Schreier collision pair — `[P,Q]=1` and `P(0,0)=P(1,0)=Q(0,0)=Q(1,0)=0`.
  The engine **finds** it at `p=3` and it replays exactly; the same `P` is
  **rejected** at `p=1000003`, where `3x^2-1` is nonconstant.  This is also the
  reason the sweep uses `p ≫ deg`: char-`p` artifacts need `p ≤ deg`.
* `C1` `P = x` returns `Q = y + x^2 - x`, replayed.
* `C2` 25 coordinates `P = λ((y+f(x))^{py} - f(1)^{py} x)` per template
  (`ribbon12`, `t44`, `t84`): all bracket-consistent, all replayed, and `delta`
  matches the closed form `-1/(λ f(1)^{py-1})` exactly in every case.

**(x) Cross-checks.**  `X1`: on 40 random dense `P` the numpy path reproduces
`incidence.system`'s matrix entrywise and its rank/consistency verdict.
`X2`: bracket nullity is `>= 2` always.  `A5`: the bottom-row sub-block never
rejects a `P` that the full system accepts.

---

## 2. Four small exact theorems (used as filters and as controls)

Let `p(x)=P(x,0)`, `q(x)=Q(x,0)`, `r(x)=P_y(x,0)`, `s(x)=Q_y(x,0)`.  Restricting
`[P,Q]=1` to the line `y=0` — which contains **both** normalized collision points —
gives the Bezout identity

```
    p'(x) s(x) - r(x) q'(x) = 1 ,      p(0)=p(1)=q(0)=q(1)=0 .
```

1. **`(P10,P01) != (0,0)`.**  The constant coefficient of `[P,Q]` is
   `P10*Q01 - P01*Q10`.  A `P` with no linear part is dead on the spot.
2. **`y | P` is impossible.**  Then `p' = 0`, so `r(x) q'(x) = -1` forces `q` linear,
   and `q(0)=q(1)=0` forces `q = 0`.  Contradiction.
3. **`P` with no `y` at all is impossible.**  Then `r = 0`, so `p'(x) s(x) = 1`
   forces `p` linear, and `p(0)=p(1)=0` forces `p = 0`.
4. **The collision defect is an invariant of `P`.**  If `[P,Q]=[P,Q']=1` then
   `Q-Q' ∈ ker X_P ⊇ k[P]`, and every `f(P)` takes the *same* value at `(0,0)` and
   `(1,0)` because `P` does.  Hence

   ```
       delta(P) := Q(1,0) - Q(0,0)
   ```

   does not depend on which mate `Q` is chosen.  Since a constant is always in the
   kernel, `Q(0,0)=0` can always be arranged, so

   > **the full collision system is consistent  iff  `[P,Q]=1` is solvable AND `delta(P) = 0`.**

Theorem 4 is the structural core of this lane: it splits the search into a
*solvability* question and a *single scalar* question, and it is what the sweep
actually measures.  Theorems 2 and 3 killed **392/1092**, **323/1159** and
**759/2047** of all sparse support patterns on `t44`, `ribbon12` and `t84`
respectively, before any linear algebra.

---

## 3. Sweeps and statistics

Templates (all with `Q`-triangle = `3/2 ×` `P`-triangle, as in `search.py`):

| name | `(px,py,qx,qy)` | `#P` | `#Q` | bracket rows |
|---|---|---|---|---|
| `ribbon12` | `(12,2,18,3)` | 21 | 40 | 60 |
| `t44` | `(4,4,6,6)` | 15 | 28 | 45 |
| `t84` | `(8,4,12,6)` | 25 | 49 | 90 |
| `t164` | `(16,4,24,6)` | 45 | 91 | 180 |

`t44`, `t84`, `t164` are the requested **live height-`(4,6)`** territory at small
x-degree; `ribbon12` is control territory (the `(2,3)` kill applies).
About 176,000 exact `F_p` linear systems were solved in total.

### 3.1 Random dense `P` — the rank profile is a delta function

57,000 random dense `P` (20,000 `ribbon12` + 20,000 `t44` + 12,000 `t84` at
`p=1000003`, plus 5,000 `t44` at `p=1000033`), each with `P(0,0)=P(1,0)=0`
imposed by the engine's own decoder:

| template | bracket rank | bracket nullity | full rank | full nullity | bracket-consistent | full-consistent |
|---|---|---|---|---|---|---|
| `ribbon12` | 38 (100%) | 2 (100%) | 39 (100%) | 1 (100%) | 0 | 0 |
| `t44` | 26 (100%) | 2 (100%) | 27 (100%) | 1 (100%) | 0 | 0 |
| `t84` | 47 (100%) | 2 (100%) | 48 (100%) | 1 (100%) | 0 | 0 |
| `t44` @ `p=1000033` | 26 (100%) | 2 (100%) | 27 (100%) | 1 (100%) | 0 | 0 |

**There is no distribution.**  Every single random dense `P` has exactly the same
corank.  The reason is now clear: `ker X_P` restricted to the `Q`-triangle is
exactly `span{1, P}` (dimension 2), because `P^2` never fits inside a `3/2`-scaled
triangle; the two collision rows then remove the constant and leave `span{P}`,
which is precisely the `γ` direction of the stated gauge `(P,Q) → (αP, γP + α⁻¹Q)`.
So the gauge accounts for the entire generic nullity, and the incidence variety
has no generic rank variation to exploit.

Consistency for a random dense `P` requires the rhs to lie in a rank-`(nq-2)`
column space inside a `60`- (resp. `45`, `90`-) dimensional row space, i.e. a
codimension-22 (resp. 19, 43) condition.  Zero hits in 57,000 draws is exactly
what that predicts, and no amount of random dense sampling will ever change it.
The bottom-row sub-block, by contrast, is consistent for **100%** of random dense
`P` — the `y=0` restriction alone has no power against dense `P` (it only bites on
sparse and leading-form-constrained ones, see below).

### 3.2 Rank drops — what is structurally special about them

A larger-than-generic solution space does occur, and it is fully explained:

| family | bracket nullity | full nullity | bracket-consistent |
|---|---|---|---|
| generic `P` | 2 | 1 | never |
| `P = A^2` (composite), 200 per template | **4** | **3** | **never** |
| coordinate boundary `f(1)=0` (`P` becomes a `py`-th power) | **4** (`ribbon12`), **7** (`t84`, `t164`) | — | **never** |

**A rank drop is an anti-signal, not a signal.**  If `P = f(P_0)` then
`ker X_P ⊇ k[P_0]`, which is strictly bigger than `k[P]`, so the nullity rises;
but `[f(P_0),Q] = f'(P_0)·[P_0,Q]` can equal `1` only if `f'(P_0)` is a nonzero
constant, i.e. only if `f` is linear and no drop happened.  So on this variety

> nullity `> 2`  ⟺  `P` is a composite (non-primitive) polynomial  ⟹  provably inconsistent.

600 composite `P` and 100 boundary `P` confirmed this with zero exceptions.

### 3.3 Sparse exhaustive sweep

Sparse `P` = a chosen set of `k` monomials with the `(px,0)` coefficient forced by
the collision.  Coefficients are reduced by the exact gauge
`P_ij → α s^j P_ij` (α from `P → αP`, `s` from `(x,y) → (x,sy)`, both of which
preserve the template, both collision points and solvability); for `k ≤ 2` this
leaves at most `gcd(Δj, p-1) ≤ 6` orbit representatives, so those patterns are
**exhaustive over all of `F_p`**, not a sample.

| template | patterns | provably dead (Thm 2,3) | exhaustive over `F_p` | systems solved | bracket-consistent | full-consistent |
|---|---|---|---|---|---|---|
| `t44` (k≤4) | 1092 | 392 | 30 | 58,126 | 91 | **0** |
| `ribbon12` (k≤3) | 1159 | 323 | 88 | 6,691 | 451 | **0** |
| `t84` (k≤3) | 2047 | 759 | 112 | 16,180 | 175 | **0** |

Every single bracket-consistent sparse `P` in all three templates has support
`{(0,1)} ∪ {bottom-row monomials}`, i.e.

```
    P = c·y + g(x),   g(0)=g(1)=0 ,
```

the elementary automorphism `(x,y) → (x, cy+g(x))`.  These are **degenerate**
(the `(0,py)` vertex is zero for `py ≥ 2`), they are the known family, and none of
them is full-consistent because `delta = -1/c ≠ 0`.  For `k ≥ 3` the coefficient
sweep is over a small set (`±1,±2,±3,±5`), not exhaustive — that is the main gap
in this section.

### 3.4 The coordinate stratum — closed form, and the same closure at `(4,6)`

`P = λ((y+f(x))^{py} - f(1)^{py} x)` with `f(0)=0`, `deg f = px/py`, is a genuine
coordinate (`(w^{py} + μx, w)` is a polynomial automorphism for `w = y+f(x)`), it
sits exactly on the template with **both** `P`-vertices nonzero, and it satisfies
`P(0,0)=P(1,0)=0` by construction.  1,800 samples across `ribbon12`, `t44`, `t84`,
`t164` and the alternate prime:

* bracket-consistent: **100%** (400/400 per template) — the sweep does find the
  known solvable stratum, so it is not blind;
* `delta = 0`: **0 of 1,800**, and `delta` matches the closed form
  `-1/(λ f(1)^{py-1})` exactly in every checked case;
* `Q`'s top and right Newton vertices reachable anywhere in the solution space:
  **0 of 400 per template** — every solvable `P` here has a Newton-degenerate `Q`;
* full-consistent: **0**.

The closed form settles the stratum without any search: `delta = 0` forces
`f(1) = 0`, which forces `μ = 0`, which makes `P = λ(y+f)^{py}` a perfect power —
degenerate, non-primitive, and provably inconsistent (§3.2).  Sampling on that
boundary confirms it: never bracket-consistent, nullity jumps to 4/7.

This reproduces the known `(2,3)` closure **and extends the same closure to the
live `(4,6)` templates** for the coordinate stratum, which was not previously
recorded.  It is much weaker than the `(2,3)` ribbon theorem (that one covers all
`P`, this one only the coordinate stratum), but it is exact.

### 3.5 Newton leading-form stratum

Any Keller pair on these triangles must have edge forms `λh^{py}` and `μh^{qy}`
for a common weighted-homogeneous `h` (the top graded piece of the bracket has to
vanish).  A fully random dense `P` does **not** satisfy this, which is another way
of seeing why §3.1 finds nothing.  36,000 `P` drawn from the stratum
`P = λ(y+f(x))^{py} + (arbitrary lower-weighted-degree terms)`, with 0, 1, 3 and
all lower terms randomized:

| lower terms | bottom-block consistent | bracket-consistent |
|---|---|---|
| all | 3000/3000 | 0 |
| 3 | 871–1729 / 3000 | 0 |
| 1 | 332–643 / 3000 | 0 |
| 0 | **0** / 3000 | 0 |

Still zero.  Being on the correct Newton stratum is necessary and nowhere near
sufficient; the surviving conditions are of high codimension, which motivated the
graded descent below.

---

## 4. Exact graded descent on the live `(4,6)` frontier

Weights `(1,d)`, `d = px/py`.  Writing `P = Σ P_a`, `Q = Σ Q_b` by weighted degree,

```
    [P,Q]_g = Σ_{a+b = g+1+d} [P_a, Q_b] = δ_{g,0} ,
```

and at level `k` (with `g = px+qx-1-d-k`) the only unknown blocks are `P_{px-k}`
and `Q_{qx-k}` — everything else is already fixed.  Two facts make this exact
rather than heuristic:

* the level-`k` matrix `A_k` depends **only** on the two top forms (the unknowns
  pair with `Q_top` and `P_top` respectively), so it is the same for every history;
* the level-`(k+1)` right-hand side is **affine** in the level-`k` unknowns.

Therefore every level after the first is a plain linear solve once the level-`(k+1)`
consistency conditions are appended as extra rows (implemented as a one-step
lookahead in `lane7_exact_descent.py`).  The single genuinely nonlinear step is
level 1 → 2, where both level-1 blocks are unknown simultaneously and the
obstruction is a system of **quadrics** in the level-1 free parameters.  Those
quadrics are formed exactly and decided with a Gröbner basis over `F_p`
(`lane7_obstruction.py`).

Results (three independent `(λ, μ, h)` per template; `h = y + c x^d`, the only
weighted-homogeneous shape of weighted degree `d`):

| template | level-1 nullity | level-2 obstruction functionals | quadrics | Gröbner = unit ideal? | `F_p` points found | descent dies at |
|---|---|---|---|---|---|---|
| `ribbon12` `(2,3)` | 2 | 1 | 1 | no | 20 | level **3**, `g=20` |
| `t44` `(4,6)` | 5 | 3 | 3 | no | 20 | level **2**, `g=6` |
| `t84` `(4,6)` | 4 | 3 | 3 | no | 20 | level **2**, `g=15` |

Reading:

* The level-2 obstruction ideal is **not** the unit ideal on any template — the
  nondegenerate stratum is not empty at level 2.  Its solution locus has positive
  codimension (on `t44`: two homogeneous quadrics in 4 of the 5 parameters, so a
  cone over an intersection of two quadrics in `P^3`).  **This is precisely why the
  blind sweeps of §3 see nothing**: the surviving set is a codimension-3 subvariety
  of a 5-dimensional space, which random sampling misses with probability
  `1 - O(1/p)`.  A random walk down the descent (120 trials) reported failure at
  level 2 in 100% of cases — a false negative that the exact treatment corrects.
* Feeding 20 explicit `F_p` points of that variety back into the descent, level 2
  is consistent **without** lookahead (nullity 4 on `t44`, 5 on `t84`) but the three
  level-3 conditions are unsatisfiable, at every one of the 20 points, for all
  three `(λ,μ,h)` choices, on both `(4,6)` templates.
* `ribbon12`, the known-dead `(2,3)` control, survives one level longer and dies at
  level 3.  The `(2,3)` ribbon theorem says it must die somewhere; it does.

**Honest limit of this section.**  The 20 points per instance are points of a
positive-dimensional variety chosen by random slicing, so "dies at level 2→3" is a
strong randomized statement, not a proof.  Making it a proof requires eliminating
levels 1 and 2 *jointly* (5 + 8 variables, quadrics) rather than sampling level 2.
That Gröbner computation is the obvious next step and is well within reach.

---

## 5. What would have been flagged, and what was

A nondegenerate consistent hit (both `P` vertices and both `Q` vertices nonzero,
full system consistent, replayed) is a `CANDIDATE-UNVERIFIED` and is printed
loudly and saved exactly.  **Count: 0.**  Degenerate consistent hits are logged
and not flagged.  **Count: 0** — the collision rows rejected every solvable `P`
that appeared, degenerate ones included, because `delta(P) ≠ 0` on all of them.
The `(2,3)` control behaved as required: no consistent hit at all on `ribbon12`,
degenerate or otherwise, so the exact `(2,3)` closure is not contradicted.

## 6. Next steps, in order of value

1. **Joint elimination of descent levels 1 and 2** on `t44` and `t84`
   (5 + 8 variables, quadrics, over `F_p`).  If the joint ideal is the unit ideal,
   the smallest live `(4,6)` templates are closed **exactly**, matching the `(2,3)`
   theorem in strength.  This is the single highest-value follow-up.
2. Push the descent lookahead two levels instead of one, which turns the level-2
   sampling into an exact linear condition at level 3.
3. Extend the sparse exhaustive gauge argument from `k ≤ 2` to `k = 3` by solving
   the consistency condition symbolically in the one residual parameter instead of
   sampling small coefficients.
4. Re-run the whole lane at a prime `p ≡ 1 (mod 4)` and `p ≡ 1 (mod 3)`
   (`1000033` was used only for the random sweep) — some coordinate normalizations
   need square/cube roots that do not exist mod `1000003`.
