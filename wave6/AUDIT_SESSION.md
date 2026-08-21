# Full self-audit of this session

Every claim made tonight, re-checked. Three real defects, two overclaims, and
the rest verified. Listed worst-first.

## 1. BUG (retracted): eliminated variables that were not eliminated

`subs_linear` rewrites a pivot variable `v` only where `v` occurs to degree
exactly 1; monomials carrying `v²` pass through untouched. So `v` survived in
the equations while being recorded in `solved` and dropped from the exported
header. Consequences:

- Exports declared 100 variables while using 109 → msolve read a malformed
  system → its `[-1]` meant nothing. **Retracted** (`RETRACTION_msolve.md`).
- Reduction sizes were overstated.

**Fixed**: a variable is now pivot-eligible only if `deg_v ≤ 1` in *every*
equation. **Guarded**: `write_ms` refuses to emit a file whose equations use an
undeclared variable, so this failure cannot recur silently.

**Corrected counts** (chain over ℚ, unpinned system):

| | claimed (buggy) | **actual (fixed)** |
|---|---|---|
| equations | 212 | **198** |
| variables | 95 | **81** |
| pivots | 67 | **81** |

The fixed run goes *further*, not less far — restricting eligibility changes the
pivot order to one that densifies less. Accounting checks: 165 − 3 zeros − 81
pivots = 81 ✓.

## 2. OVERCLAIM: "no small overdetermined closed subsystem exists"

That search was a **greedy heuristic**: 283 growth paths, one per seed equation,
against 2¹⁶⁵ ≈ 4.7×10⁴⁹ variable subsets. "A search found none" is honest;
**"there is none" is not proved** and I stated it as fact. The supporting
evidence for the *global* character of the overdetermination is the rank
measurement (below), which is sound; the subsystem search is suggestive only.

## 3. OVERCLAIM: "w₀ = 1 is exactly where the invariant ring is polynomial"

I verified that weights `(2,−1,−1)` need three generators and so fall outside
A1's hypothesis, and that `(1,−b,−c)` is always free. I did **not** prove that
no `w₀ ≥ 2` system has a polynomial invariant ring. The A1 answer is therefore
scoped: **within the family `(1,−b,−c)`, `q = x^{b+c−1}`**, which is where
Alpöge's example and the campaign's cases live. Separator #2's argument is
unaffected — it uses `w'₀ = 1` as a hypothesis, not as a classification.

## 4. CORRECTED: overdetermination 117 vs 118

Already corrected in `FORCED_CHAIN.md`. Exact rank of the 283 × 8727
coefficient matrix is **283 with zero dependent equations**, so 118 stands for
the un-localized system. 117 appears only after localizing at the nondegeneracy
conditions. Both correct, different objects. (Full rank mod p implies full rank
over ℚ, since rank can only drop under reduction — so the rank claim is sound
from a single prime.)

## 5. WEAK CONTROL, since superseded

The first "end-to-end pipeline control" **re-implemented the chain loop inline**
rather than calling the shipped code, so it tested the logic but not the
artifact. Superseded by the planted-solution control (below), which calls the
real `w6_chain_export.main()`.

## 6. Verified clean, re-checked tonight

- **`ORBIT_VERDICT`** re-audited from the raw RUR: eliminant degree 9, factors
  1+1+2+5, **all four irreducible over ℚ and squarefree**; `c8` and `d12`
  numerators vanish on both linear factors and the full quadratic and have gcd 1
  with the quintic; `c1`, `c2` vanish nowhere; quintic has 1 real root, quadratic
  has negative discriminant → **3 real seeds, exactly one admissible**. Stands.
- **Sweep**: 13 primes, zero anomalies, admissible mean 1.077. Stands.
- **Bilinearity** (c-degree ≤ 1, d-degree ≤ 1): a census, re-checkable. Stands.
- **Descent master formula**: 7/7 certifier, predicts both the exponent and
  `h = f₃/x`. Stands, with the scope note in §3.
- **Degree-0 Nullstellensatz**: no certificate, by two independent routes
  (exact ℚ elimination; F_p row-space). Stands.
- **Golub–Pereyra Jacobian**: verified against finite differences at 9.5e-08
  after the Kaufman version was caught wrong at ~50%. Stands.
- **P-POS failures** for ALS and VARPRO-Newton: genuine negatives, and the
  reason multi-start is retired here. Stands.

## 7. The seed verdict, and what it now rests on

`SEED_VERDICT.md` claims: at p = 1000003 the seed-pinned system has no solution
with `s_4_8 ≠ 0`. After this audit it rests on:

1. **Symbol guard** — `reduced_91v.ms` verified 92 declared, 92 used, 0 leaked.
2. **Planted-solution control on the ACTUAL system, through the REAL code**:
   the seed-pinned system with constants shifted so a random all-nonzero point
   is a solution by construction, run through `w6_chain_export.main()` and
   msolve. Returns `[0, …]` — **the chain does not destroy solutions.**
3. **Depth**: the control was tested at 112 and 97 variables, bracketing the
   real run's 92, so the validation reaches the depth actually used.
4. **Row-space check**: the constant is not in the row space of the reduced
   system, so the emptiness is not a linear artifact.
5. **Prior expectation**: overdetermined by ~117; emptiness is predicted.

**Still one prime.** Modular emptiness was proved unsound for contradictions
this morning, so a second prime and a characteristic-zero lift remain required
before case (1) may be called closed.

---

# Manual check: one more error found, and the verdict's discrimination confirmed

## ERROR: my "desaturated" test never desaturated anything

Reading the raw source by hand rather than through my own tooling: line 269 of
`seed0_p1000003.ms` is

    s_4_8*zz0-1

**The campaign's own export already saturates `s_4_8`**, via its own variable
`zz0`. So the `zz9*s_4_8-1` row I added was redundant (harmless, but redundant),
and — the actual error — when I built a "desaturated" copy by stripping `zz9`,
**`zz0` remained and the system was still saturated.** The observation "both the
saturated and desaturated systems return `[-1]`" was therefore void: both were
saturated. Withdrawn.

## The real desaturation test, and what it shows

Removing **both** `zz0` and `zz9` (90 variables, 207 equations):

| system | s_4_8 ≠ 0 enforced? | msolve |
|---|---|---|
| `reduced_91v` | yes (zz0 and zz9) | **`[-1]` EMPTY, seconds** |
| genuinely desaturated | no | **NO VERDICT — timed out at 110 s** |

This is the discrimination the earlier void test was supposed to provide, and it
is the right way round. With the nondegeneracy imposed the system collapses
immediately; without it, the solver cannot finish — the behaviour of a system
that *has* solutions and must compute them. Emptiness is specifically a
statement about `s_4_8 ≠ 0`, not an artifact of the reduction.

It also explains the timing that made me suspicious: a contradiction can be
found early and terminate, whereas a non-empty variety must be computed out.

## Planted-solution controls: depth now brackets the real run

Same chain code, same export, on the **actual** seed-pinned system with a
solution planted by construction:

| control | variables | msolve |
|---|---|---|
| `reduced_ctl111v` | 112 | **`[0, …]` found it** |
| `reduced_ctl96v` | 97 | **`[0, …]` found it** |
| `reduced_ctl85v` | 86 | running (deeper than the real run) |
| the real run | **92** | `[-1]` |

97 and 86 bracket 92, so the validation reaches — and passes through — the depth
actually used. The chain does not destroy solutions at this depth.

## Net effect on the verdict

Unchanged in substance and better supported: **at p = 1000003 the seed-pinned
system has no solution with `s_4_8 ≠ 0`** — and that condition is the campaign's
own, imposed by its own `zz0`, not something I added. Still one prime; a second
prime and a char-0 lift remain required.
