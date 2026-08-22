# Session 43 — what happened overnight

Branch `claude/ce-acquisition-strategy-uyqftb`.  Lane: the **pentagon system**
(`wave1/pent_L23.ms`), coordinated with Codex on `codex/claude-opus5-mailbox`
(handshake CONNECTED; he holds trackB1, p108, and the Nullstellensatz ladders).

**No counterexample.**  What there is instead: the pentagon target was
mis-specified, and that is now proved rather than suspected.

---

## The headline

**`pent_L23.ms` is NONEMPTY, and its solution set contains a verified
4-parameter family of degenerate solutions.**

For any `f(y)` with `deg f <= 5`:

    P(x,y) = x + f(y)
    Q(x,y) = integral_0^y ( x + f(y) - f(s) )^2 ds

satisfies `{P,Q} = x^2` exactly, and Q has y-degree `2 deg f + 1 <= 11 < 13`, so
**every** condition at levels 13..23 vanishes identically.  With the campaign's
own gauge `p_1_0 = 1` this is a 4-parameter family.  Checked three ways: 66/66
conditions vanish numerically at random parameter values; the same point
substituted into the **original** exported degree-22 polynomials gives 66/66;
and `{P,Q} = x^2` holds symbolically over Q for general `f`.  Adding `y^6`
breaks exactly one condition — the level-13 one — exactly as the degree count
predicts.

Consequences:

1. **"Prove pentagon case (1) EMPTY" is false as exported.**  Both EMPTY and
   NONEMPTY on this system answer the wrong question.
2. **The export is missing its non-degeneracy conditions.**  The bottom-edge
   code is careful about exactly this (`c1, c8, d12 != 0`); `pent_L23.ms` has no
   analogue, and I confirmed it contains no saturation rows at all.
3. `P = x + f(y)` has no x-dependence beyond the linear term, so it is nowhere
   near a (72,108) configuration.  **This is not a counterexample and must not
   be reported as one.**

## Why every prior pentagon run was NO VERDICT by construction

Two independent structural reasons, both measured:

- **The system was never rigid.**  `pent/RUNLOG_NOTES.md` says the gauge
  `p_1_0 - 1` makes it rigid so msolve's solve mode (which needs a
  zero-dimensional input) applies.  Measured torus rank: raw **2**, with that
  gauge **1**, with `p_1_1 - 1` as well **0**.  One gauge was added where two
  were needed.
- **The variety is nonempty and at least 4-dimensional** (above), before even
  counting the torus.

So `pent_L18_g3` (OOM, 1798.9 s, 6.2 GB), `pent_L18_g2` (TIMEOUT 3600 s), wave1
L23 (exit 137, 13.9 GB) and the two 90-minute jobs could not have terminated
usefully at any budget.  That is roughly a dozen hours of compute explained.

## What the system actually is

Summing the exporter's recursion as a generating function gives, in closed form
and verified numerically at all 12 computed orders:

    **{P,Q} = P_x Q_y - P_y Q_x = x^2**

- It is **bilinear** in the coefficients of (P,Q).  The 43 MB / degree-22 /
  1,080,147-monomial export is that size *only because Q was eliminated*.
  Re-exported with Q kept: **84 KB, degree 2, 4,736 terms** — 228x fewer terms.
- `dP ^ dQ = d(x^3/3) ^ dy`, so with `s = x^3/3`, **det J_(s,y)(P,Q) = 1**: the
  pentagon searches for a Keller map on the 3:1 cyclic cover.
- Its **leading-coefficient relation is the campaign's bottom edge**: cancelling
  the top x-degree forces `b_n^m = c a_m^n`, whose `(m,n) = (2,3)` case is
  exactly `2 f g' - 3 f' g`.  The bottom edge is not a separate object.
- **x-degree-1 solutions are forced degenerate — in the idealised problem.**
  The equation reduces to `Q_y|_u = (u-f)^2/(1+g)^3`, and an antiderivative of a
  rational function is polynomial only if the function already is, so `g` must be
  constant.  **Caveat, self-caught and recorded:** this needs Q polynomial in y,
  which the truncated export does not give — there Q is a power series and the
  step fails.  For the export I have evidence only (a nonzero `p_{j,1}` leaves
  21–26 of 66 conditions nonzero at a random point), which is NO VERDICT.

## Instruments built (all controls passing, in `session43/pentagon/`)

- `pentev.py` — evaluates all 66 conditions from the recursion in milliseconds.
  **Control: 66/66 agreement with the exported degree-22 polynomials at two
  independent random points.**
- `oracle.py` — the conditions are exactly affine in the late block, so
  consistency is a rank test, not a Groebner basis.  Controls: planted
  right-hand side → consistent and solution recovered; perturbed → inconsistent;
  and now a **real-data positive control** — it reports consistent on the
  degenerate family and the recovered points verify with zero residual.  The
  instrument has said YES on real data, which no pentagon instrument had.
- `bilinear.py`, `partial.py` — the bilinear export and a measured
  elimination-level tradeoff curve from 180 vars/degree 2 to 59 vars/degree 22.
- `degprof.py` — **14 variables enter affinely, not 13** (`p_11_6` was missed).
- `torus_scan.py` — the rank computation above.

## Corrections to the record

- **`pent/pent_slice.py` cannot find what it is looking for.**  It fixes 45 of 58
  parameters to uniformly random values; a random affine subspace of codimension
  45 meets a variety of dimension d only if `d >= 45`.  Its controls are sound
  and pass — the instrument is honest, it is aimed wrongly.
- I made the same class of error myself and it is recorded: 400 random
  perturbations off the degenerate family gave 0 consistent, which is evidence
  and **not** a proof, for exactly the reason above.
- My first planted-control on the bilinear export FAILED (63 violations) because
  the *test* imposed conditions the test point could not satisfy.  Fixed; the
  bug was in the control, not the export.
- An earlier interim claim of mine, that this container caps processes at
  ~3.5 GB, is **retracted**: one shared ~14 GB cgroup, and three of the night's
  OOMs were my own concurrency.

## Verdicts, in campaign language

| target | verdict |
|---|---|
| `pent_L23.ms` as exported (+ campaign gauge) | **NONEMPTY** — exact rational witness, verified against the original file |
| saturated pentagon (`p_16_8 != 0`) | **NO VERDICT** — `msolve -g 2` running |
| bilinear form, Groebner-only, 900 s | **NO VERDICT** (exit 124, 0 bytes) |
| bilinear form, Singular `slimgb` | running |
| original 43 MB export, Groebner-only | **NO VERDICT** (13 GB, killed at 13 min) |
| rigid chart `{p_1_0 != 0, p_1_1 != 0}` | **NO VERDICT** — the witness lies outside it |

## What I would do next

1. **Fix the export.**  Saturate the corner (`z * p_16_8 - 1`) and re-ask.  Until
   then the pentagon programme has no well-posed target.  A run is in flight.
2. **Use the leading relation as a filter before any solver.**  With `p_16_8 != 0`
   forced, `m = 8`, and `a_8 = y^14 (p_14_8 + p_15_8 y + p_16_8 y^2)` must be
   `lambda h^{8/g}` with `g = gcd(8,n)`.  Valuation 14 forces `8/g` to divide 14,
   so `g in {4,8}` and `n in {4,8,12}` — a finite case split, **derived, not
   verified, and resting on the idealised-problem hypothesis above**.  This is
   the lockpick: search the locus the constraints allow, not the ambient space.
3. **Audit the other exports for the same defect.**  trackB1 and p108 are exports
   of the same kind of Newton-polygon data.  If either lacks explicit
   non-degeneracy rows, a degenerate witness may satisfy it too, and a NONEMPTY
   there would be a false lead.  Flagged to Codex.
