# Lane 6: exhaustive modular shooting search on the collision-first (4,6) frontier

Date: 2026-08-26. Working directory
`/tmp/claude-0/-home-user-jacobian-planar/9c0f56a7-85d4-5d2a-8150-2daa4480a93e/scratchpad/lane6/`.
The git repository was neither read for state nor modified.

## Binding verdict

**No counterexample. No candidate.** Not one parameter point in any sweep
survived the polynomiality tower — 28,198,016 points evaluated across 22
primes. Step 3 of the brief (Hensel lifting, rational reconstruction, exact
SymPy replay of `P_x Q_y - P_y Q_x = 1`) was therefore never triggered.
Nothing here is called a counterexample.

The useful output is a sharper *negative* result plus two structural findings,
one of which is a methodological correction that matters for any future
modular lane. Both the result and its limits are in sections 5 and 6.

---

## 1. What was built, and the step-1 validation gate

`lane6_core.py` re-implements the kernel-retaining local recurrence from
scratch. It was not transcribed from the prior formulas: it was re-derived
from the Jacobian rows and then checked against the prior work's exact objects.

**Re-derivation.** With `P = p0 + p1 y + p2 y^2 + p3 y^3 + y^4` and
`Q = q0 + ... + q5 y^5 + c y^6`, the `y^{i+j-1}` coefficient of
`P_x Q_y - P_y Q_x` gives, for `j = 5,4,3,2,1,0`,

```
4 q_j' = sum_{i=0..3, k = j+4-i <= 6} [ k P_i' q_k - i P_i q_k' ]
```

and the three surviving rows are

```
E2 = 3 p0' q3 + 2 p1' q2 - p1 q2' + p2' q1 - 2 p2 q1' - 3 p3 q0'
E1 = 2 p0' q2 +   p1' q1 - p1 q1' - 2 p2 q0'
E0 =   p0' q1 - p1 q0'
```

All six `q_j` ODEs and all three rows were confirmed **identically equal** to
`ribbon46_reduction.py`'s `survivors` objects (`sp.expand(mine - ref) == 0`,
9/9 True). This replaces the 152-term expanded form by a straight-line
integrator costing ~24 series convolutions per rung, which is what makes an
exhaustive sweep affordable (~30-100 microseconds per parameter point to
rung 60).

**Rung bookkeeping** — measured, not assumed:

| rung | determined | retained kernel |
|---|---|---|
| `n=0` | `A1, A2, A3` | `u = p1[1]`, `v = p2[1]`, `w = p3[1]` FREE |
| `n=1` | `A5` (pivot `5a^2/4`), `p1[2]`, `p2[2]` | `p3[2]` |
| `n>=2` | `p3[n]` (pivot `(n+1)u/(4a)`), `p1[n+1]`, `p2[n+1]` (pivots `-(n+1)/a`) | `p3[n+1]` |

`A0` and `A4` provably do not occur in `E2, E1, E0` (checked directly on the
sympy objects), so they are set to 0. **There is no extra free kernel value:**
`p3[2]` is fixed at rung 2 by the pivot, so once the gauges are fixed the chart
is a genuine three-parameter shooting problem in `(u, v, w)`.

### Step-1 validation gate: PASSED

`lane6_validate.py`, every item:

* **(a)** The exact rational run at `(u,v,w) = (1,0,0)` reproduces **all 65**
  published coefficients of the boundary certificate — `p1[1..22]`,
  `p2[1..22]`, `p3[1..21]` — exactly, as rationals.
* **(b)** The free-shooting value of the forbidden degree-22 coefficient is

  ```
  p3[22] = 421966423176051225964907643652535431 / 885443715538058477568
  ```

  an **exact match** with the published value. `A1,A2,A3,A5 = -1,-1/2,-1/3,-1/5`
  also match, and `p3[2..21]` are all nonzero, as the prior certificate states.
* **(c)** The `F_p` engine reproduces the mod-`p` reduction of every one of
  those coefficients and of `p3[22]`, at `p = 41` (`p3[22] = 4`), `p = 43`
  (`11`) and `p = 67` (`61`).
* **(d)** At three random generic rational `(u,v,w)` the engine reproduces the
  documented closed forms `A5 = -(u^4+3u^2v+2uw+v^2)/5`,
  `p1[2] = (u^5+4u^3v+3u^2w+3uv^2+2vw+6)/4`,
  `p2[2] = -(3/8)(u^6+3u^4v+2u^3w-2uvw+12u-v^3-w^2)`, and the *measured* rung-2
  pivot equals the documented `(n+1)u/4`.
* **(e)** An independent SymPy replay through the original `survivors` objects
  at generic `(u,v,w)` confirms `E2 = E1 = 0`, `E0 = 1` coefficientwise through
  `x^8`; after the gauge generalisation the same replay passes at generic
  `(a, c, u, v, w)` using the **full** `p0 = a(x^84 - x)` including the `x^84`
  term.

The `F_p` engine was additionally cross-checked against the exact rational
engine **with the polynomiality caps switched on**: 5 generic points, 3 primes,
75 condition values, 0 mismatches.

---

## 2. Two exact symmetries — and why `c = 1` is not a safe gauge

**T1 — quasi-homogeneity.** With weights

```
wt(u,v,w,c) = (1,2,3,5),  wt(x) = -4,  wt(A_j) = j-1,  wt(p_i[n]) = i + 4(n-1)
```

the reduced row `E_d` is quasi-homogeneous of weight `d`, so under
`(u,v,w,c) -> (L u, L^2 v, L^3 w, L^5 c)`

```
E_d[n]  ->  L^(d + 4n) E_d[n].
```

Verified as an **exact identity of values** (not merely of vanishing) for all
68 conditions in range at `p = 41, 67, 101, 127, 131`, 300 random points each.

**T2 — rescaling `x`.** With `p0 = a(x^84 - x)` (locally `p0 = -a x`), the
substitution `X = a x` together with `q_j -> a q_j` gives

```
(a, c, u, v, w)  ~  (1, a c, u/a, v/a, w/a),
```

verified over 300 random points at `p = 101`. The check is sharp: the two
plausible alternatives `c/a` and `c` both fail.

**Consequence — a complete search slice.** T2 normalises `a = 1`, T1 then
normalises `u = 1`, and both stabilisers are trivial, so

```
{ a = 1, u = 1, (v, w, c) in F_p x F_p x F_p^* }        (p^2 (p-1) points)
```

meets every orbit of the `u != 0` chart exactly once. It costs the same as the
naive `(u,v,w)` grid at `c = 1`, but unlike that grid it is complete.

**The `c = 1` slice provably misses solutions.** At `p = 41`, sweeping
`(u,v,w,c)` exhaustively (2,689,600 points) finds **40** points passing the
first three cap conditions, whereas the `c = 1` slice finds **0**. The 40 form
a single T1-orbit whose `c`-coordinate lies outside the subgroup of fifth
powers mod 41, so the orbit never meets `c = 1`. Over `Qbar` the scaling is
always available and `c = 1` is harmless; over `F_p` it is not, because `F_p^*`
is not divisible. **A modular search restricted to `c = 1` can miss real
solutions.** Any future modular lane on this frontier should sweep `c` or use
the normalised slice above.

Orbit-count cross-check (three-condition solutions):

| p | `(u,v,w,c)` sweep | normalised slice | `(p-1)` x normalised |
|---|---|---|---|
| 29 | 56 | 2 | 56 |
| 37 | 72 | 2 | 72 |
| 41 | 40 | 1 | 40 |
| 43 | 0 | 0 | 0 |

---

## 3. Modular rigour limit

The recurrence divides by `n` (integrating `q_j' -> q_j`) and by `n+1`
(solving `p1[n+1]`, `p2[n+1]`). Mod `p` these fail at `n = p` and `n = p-1`,
so the last fully rigorous rung is `p-2` unless a cap has already removed the
division. The engine **raises** rather than silently producing garbage:
`rigour_limit(41) = 39`, `rigour_limit(43) = 41`, `rigour_limit(67) = 66`.
That is why `p = 67` was added — it is the smallest prime here that reaches
rung 60 with no modular degeneracy anywhere.

---

## 4. The sweeps and the survival histogram

### (i) Mandated primes, naive `(u,v,w)` grid at `c = 1`

Survival histogram (condition `k` is `E0[21+k] = 0` with `p3[22..20+k]` pinned
to 0 by the degree cap `deg p3 <= 21`):

**p = 41, all 18 rigorous rungs 22..39, 67,240 points**

| rung n | this condition alone | all of 22..n | random-hypersurface expectation |
|---|---|---|---|
| 22 | 1625 | 1625 | 1640.00 |
| 23 | 1770 | 40 | 40.00 |
| 24 | 1515 | **0** | 0.98 |
| 25..39 | ~1600 each | 0 | ~0 |

**p = 43**, rungs 22..41, 77,658 points: 1774 / 37 / 0 (expectation 1806 / 42 / 0.98).
**p = 67**, rungs 22..60, 296,274 points, 58 conditions (39 `p3` caps, 19 `p2`
caps): 4485 / 71 / **1** / 0 (expectation 4422 / 66 / 0.99).

### (ii) Definitive sweep on the complete gauge-free slice

| p | points | depth | after `p3[22]` | after `p3[23]` | after `p3[24]` | after `p3[25]` | survivors |
|---|---|---|---|---|---|---|---|
| 41 | 67,240 | rung 39 | 1654 | 38 | **1** | 0 | 0 |
| 43 | 77,658 | rung 41 | 1774 | 37 | 0 | 0 | 0 |
| 67 | 296,274 | rung 60 | 4485 | 71 | **1** | 0 | 0 |

The two three-condition solutions are `(a,u,v,w,c) = (1,1,30,13,36)` at `p=41`
and `(1,1,12,5,13)` at `p=67`. Both die at `p3[25]`.

**Answer to the Bezout question.** The counts track the naive random-
hypersurface expectation `(p-1)p^2 / p^(n-21)` to within sampling noise at
every level, at every prime. **There is no anomalous structure in the tower's
first three levels** — the three conditions behave exactly like three generic
hypersurfaces. The obstruction is not visible as a degeneracy in the counts;
it appears abruptly at the fourth condition.

---

## 5. The sharp finding: 22 primes, 24 partial solutions, zero survivors

Complete gauge-free slice at every prime. `N1 = #{E0[22]=0}` (a surface),
`N2` (a curve), `N3` (finite):

| p | points | depth | N1 | N1/p^2 | N2 | N2/p | N3 | first failure of the N3 points |
|---|---|---|---|---|---|---|---|---|
| 29 | 23,548 | 27 | 765 | 0.910 | 35 | 1.207 | 2 | `p3[25]` x2 |
| 31 | 28,830 | 27 | 931 | 0.969 | 29 | 0.935 | 1 | `p3[25]` |
| 37 | 49,284 | 27 | 1311 | 0.958 | 37 | 1.000 | 2 | `p3[25]` x2 |
| 41 | 67,240 | **39** | 1654 | 0.984 | 38 | 0.927 | 1 | `p3[25]` |
| 43 | 77,658 | **41** | 1774 | 0.959 | 37 | 0.860 | 0 | - |
| 47 | 101,614 | 27 | 2180 | 0.987 | 33 | 0.702 | 1 | `p3[25]` |
| 53 | 146,068 | 27 | 2762 | 0.983 | 49 | 0.925 | 2 | `p3[25]` x2 |
| 59 | 201,898 | 27 | 3335 | 0.958 | 45 | 0.763 | 0 | - |
| 61 | 223,260 | 27 | 3626 | 0.975 | 56 | 0.918 | 1 | `p3[25]` |
| 67 | 296,274 | **60** | 4485 | 0.999 | 71 | 1.060 | 1 | `p3[25]` |
| 71 | 352,870 | 27 | 4782 | 0.949 | 68 | 0.958 | 2 | `p3[25]` x2 |
| 73 | 383,688 | 27 | 5228 | 0.981 | 73 | 1.000 | 0 | - |
| 79 | 486,798 | 27 | 6067 | 0.972 | 67 | 0.848 | 0 | - |
| 83 | 564,898 | 27 | 6664 | 0.967 | 87 | 1.048 | 1 | `p3[25]` |
| 89 | 697,048 | 27 | 7907 | 0.998 | 94 | 1.056 | 0 | - |
| 97 | 903,264 | 27 | 9149 | 0.972 | 82 | 0.845 | 2 | `p3[25]` x2 |
| 101 | 1,020,100 | 27 | 9814 | 0.962 | 97 | 0.960 | 1 | `p3[26]` |
| 103 | 1,082,118 | 27 | 10630 | 1.002 | 120 | 1.165 | 1 | `p3[25]` |
| 107 | 1,213,594 | 27 | 11369 | 0.993 | 101 | 0.944 | 0 | - |
| 109 | 1,283,148 | 27 | 11895 | 1.001 | 118 | 1.083 | 1 | `p3[25]` |
| 113 | 1,430,128 | 27 | 12514 | 0.980 | 111 | 0.982 | 2 | `p3[25]`, `p3[27]` |
| 127 | 2,032,254 | 27 | 16057 | 0.996 | 117 | 0.921 | 3 | `p3[25]` x3 |

```
mean N1/p^2 = 0.9752      mean N2/p = 0.9594      mean N3 = 1.0909
24 three-condition solutions in total:
    22 die at p3[25],  1 at p3[26],  1 at p3[27]
survivors of the FULL tower, all 22 primes: 0
N3 distribution over primes: {0: 6, 1: 9, 2: 6, 3: 1}
```

Reading these by Lang-Weil and Chebotarev:

* `N1/p^2 -> 1` : `{E0[22] = 0}` is a surface with **one** absolutely
  irreducible component.
* `N2/p -> 1` : `{E0[22] = E0[23] = 0}` is a curve with **one** absolutely
  irreducible component.
* `mean N3 -> ~1` : the three-condition system is a **genuinely non-empty**
  zero-dimensional scheme with about one Galois orbit. The observed
  fixed-point distribution `{0,1,2,3}` with mean 1.09 is close to the
  fixed-point spectrum of `S_5` acting on 5 points (mean exactly 1), i.e. one
  closed point of degree roughly 4-5 with large Galois group.
* **6 of 22 primes have `N3 = 0`.** A `Q`-rational point of that finite scheme
  would reduce to an `F_p`-point at every prime of good reduction, so the
  three-condition system already has **no rational solution** — before the
  fourth condition is even applied.
* `{E0[22] = E0[23] = E0[24] = E0[25] = 0}` has **no `F_p`-point at any of the
  22 primes**, on the complete gauge-free slice.

For a non-empty zero-dimensional scheme over `Q`, the average number of
`F_p`-points is exactly 1 per closed point. Observing 0 at all 22 primes is
therefore strong evidence — **not proof** — that the four-condition system is
empty, i.e. that the swept chart of the collision-first `(4,6)` frontier
contains no polynomial Keller pair at all.

This strictly extends the prior work, which closed only the single planted
rational specialisation `u = 1, v = w = 0`.

---

## 6. What was established, and what was not

**Established.**

1. An independent re-derivation and re-implementation of the `(4,6)` reduction
   and the kernel-retaining recurrence, validated against the published
   rational seed to the last digit (65 exact coefficients plus `p3[22]`).
2. Two exact symmetries of the tower — quasi-homogeneity with weights
   `(1,2,3,5)` and the `x`-rescaling `a`-action — and from them a complete
   gauge-free search slice.
3. That the prior scripts' `c = 1` gauge, harmless in characteristic zero,
   makes a **modular** search incomplete; demonstrated concretely at `p = 41`.
4. Exhaustive emptiness of the polynomiality tower over that complete slice at
   22 primes, including the mandated 41 and 43 at full rigorous depth and
   `p = 67` with all 58 conditions through rung 60 and no modular degeneracy.
5. That the three-condition system is non-empty over `Qbar` but has no
   `Q`-rational point, and that the fourth condition kills every `F_p`-point of
   it at every prime tested.

**Not established — flagged honestly.**

* **This is not a proof.** Everything past section 1 is modular. Making
  section 5 a theorem needs a Groebner/resultant elimination of
  `{E0[22],...,E0[25]}` over `Q[v,w,c]`; those polynomials were not computed
  here (the recurrence supplies them only by evaluation, and they are large).
* **The swept chart is narrower than "the `u != 0` chart", and this is the
  most important gap.** The prior recurrence script — and hence this sweep —
  takes `p1(0) = p2(0) = p3(0) = 0`. That is **not** a gauge. The collision
  normalisation `P(0,0)=P(1,0)=Q(0,0)=Q(1,0)=0` forces only
  `p0(0) = p0(1) = 0`, and the `y`-shears `y -> y + f(x)` that preserve both
  the weighted triangle and the two collision points satisfy `f(0) = f(1) = 0`,
  so they cannot move `p1(0), p2(0), p3(0)`. Restoring generic constants
  `g1, g2, g3` and solving the rung-0 system symbolically gives **exactly one**
  solution branch for `(A1, A2, A3)` for generic `g` — the only degeneracy is
  the vanishing of one explicit 34-term polynomial in `g,u,v,w` — and it
  specialises at `g = 0` to the documented `-1, -u/2, -(u^2+v)/3`. **Rung 0 imposes no condition on
  `g1, g2, g3` whatsoever** — they are unobstructed extra directions of the
  frontier that the prior ansatz sets to zero by hand. (At most one of them is
  removable by a constant `y`-shear, and only at the cost of re-deriving the
  `p0 = x^84 - x` pinning, since a constant shear moves the collision points
  off `y = 0`.) The full local problem is therefore
  `(a, c, p1(0), p2(0), p3(0), u, v, w)` — six essential parameters after the
  2-torus, versus the three swept here. `41^6 ~ 4.8e9` puts that beyond
  exhaustive `F_p` search; it needs the tangent-space / rank descent on the
  evaluation representation that the prior audit already recommended.
* Rungs beyond `p-2` are not rigorous mod `p`. That is why the rung-60 claim is
  carried by `p = 67` and `p = 41, 43` carry only rung-39 / rung-41 claims.
* `Q(1) = 0`, the second collision endpoint, was never reached — as in the
  prior work, everything dies far earlier.

---

## 7. Controls

Because the headline result is negative, the pipeline was controlled in both
directions (`lane6_control.py`, both PASS).

**Positive control.** At `p = 67` the point `(u,v,w) = (57,61,25)` passes the
first three conditions. Its rows were rebuilt and replayed independently
through the original `survivors` objects, with the true `p0 = x^84 - x`:

```
deg p3 = 21                                     (cap deg p3 <= 21 satisfied)
p3[22] = p3[23] = p3[24] = p3[25] = 0
E2   coefficients x^0..x^24 mod 67 : ALL VANISH
E1   coefficients x^0..x^24 mod 67 : ALL VANISH
E0-1 coefficients x^0..x^24 mod 67 : ALL VANISH
[x^25](E0-1) mod 67 = 49             -> fourth cap condition FAILS
engine-recorded conditions E0[22..25] = [0,0,0,49]   (matches the replay)
```

So the machinery demonstrably certifies genuine partial solutions
coefficientwise against the original objects: a real candidate would not have
been missed.

**Negative control.** The published rational seed `(1,0,0)` replays with
`E2, E1, E0-1` all vanishing through `x^21` and `[x^22](E0-1) = 1 != 0` mod 67,
reproducing the prior boundary certificate through the new pipeline.

---

## 8. Compute

28,198,016 parameter points. About 16 minutes of single-core wall time in
the sweeps themselves, plus the SymPy validation, controls and symmetry
checks — roughly 25 minutes total. One process at a time, one core.

## 9. Files

| file | role |
|---|---|
| `lane6_core.py` | the re-derived recurrence; `QQRing` (exact) and `FpRing` (numpy-vectorised) share one code path; gauges `a`, `c` are parameters |
| `lane6_validate.py` | **step-1 gate**: exact seed reproduction, `p3[22]`, mod-`p` agreement, generic closed forms, SymPy replay |
| `lane6_sweep.py` | naive `(u,v,w)` grid at `c=1`, rigour-limit logic, survival histogram |
| `lane6_stats.py` | multi-prime Lang-Weil / Chebotarev statistics on the naive grid |
| `lane6_gauge.py` | `c`- (and optionally `a`-) swept grid; showed the `c=1` slice is incomplete |
| `lane6_complete.py` | **definitive** sweep on the complete gauge-free slice; re-verifies both symmetries at every prime |
| `lane6_control.py` | positive and negative end-to-end controls |
| `lane6_chart_width.py` | the `p_i(0) = 0` chart-width test |
| `run_*.txt`, `lane6_*.json` | raw run logs and machine-readable results |
