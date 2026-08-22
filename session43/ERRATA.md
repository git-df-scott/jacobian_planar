# Session 43 errata — every error caught, and what caught it

A full sweep of the night.  Grouped by who found what, because the pattern
matters more than the count: **almost every error was caught by a control or an
assertion, not by inspection.**

---

## A. My own errors, caught by me

### A1. Planted control on the bilinear export failed — bug in the test
First run of the bilinear positive control reported **63 of 184 equations
violated**.  The export was fine; the *test* imposed the Newton-polygon
conditions `q_{j,i} = 0` while checking against a random P whose recursion Q
does not satisfy them.
**Caught by:** the control failing.  Had it been written to pass, it would have
proved nothing.

### A2. Deformation sweep: 84 candidates that were all the starting point
A sweep for deformations off family B reported **all 84 cases as candidates**
with a degree-1 GCD.  The GCD was `X`, whose root is `t = 0` — the base point
itself, a solution by construction.
**Caught by:** the uniformity being implausible.  Stripping the trivial root left
**0 of 42**.  A sweep whose hits are all its own input is finding nothing.

### A3. Higher-order lift — RETRACTED
Built an order-by-order deformation lift; it reported **0 of 28 tangent
directions surviving to order 8**, a clean local-rigidity claim I was about to
report.
**Caught by:** running it on a known curve.  Family B's own `d/dlambda`
direction is tangent to a curve demonstrably in the variety (66/66 at
`lambda = 2,3,6`), and the code called it **obstructed at order 4**.
**Cause:** the order-k correction is determined only modulo `ker J`, which is
28-dimensional here; a greedy particular solution manufactures obstructions.
**What survives:** the order-2 test, which is choice-independent — 23 of 28
genuinely obstructed.  Everything beyond order 2 withdrawn.

### A4. Interpolation aliasing in the obstruction test
Interpolated `conditions(pt + t·v)` from **6 points** for a polynomial of
**degree 22** in `t`.  Coefficients were aliased, so the "second-order term" was
not the second-order term.
**Caught by:** an assertion I had put in the same function — that a tangent
vector must give a vanishing first-order term.  It fired on direction 2.
Fixed with 24 points.

### A5. Nearly filed a false defect against Codex's artifact
My audit of his export reported **294/299**, with five equations nonzero.
**Cause:** `q_3_0 = 1/3`, and my checker called `int()` on a sympy `Rational`,
silently truncating `1/3` to `0`.  Reducing properly as `num·den^{-1} mod p`
gives **299/299**.
**Caught by:** refusing to report a discrepancy before tracing it to a named
cause.  Same class as the campaign's own msolve coefficient trap (`91f42f5`).

### A6. The "3.5 GB per-process cap" — RETRACTED
Relayed an interim claim that this container caps single processes at ~3.5 GB.
False: one shared **~14 GB cgroup**; msolve reached 13.9 GB.

### A7. Three self-inflicted OOMs
Violated the campaign's own one-heavy-at-a-time rule three times (d=8, the d12
slice probes, and the pentsat/xdeg1 collision).  Those OOMs were mine, not the
machine's — the failure class already logged twice in `CATCHES.md` (ix).
Only MISS-3's and the final saturated run's OOMs were genuine ceilings.

### A8. STRUCTURE.md asserted too much — scope corrected
Claimed the x-degree-1 forcing and the leading-coefficient relation constrain
the **exported** system.  Both require **Q polynomial in y**; the truncated
export gives only a power series, so the "antiderivative of a rational function"
step does not apply there.
**Caught by:** re-reading my own derivation against what the export actually is.
Restated as results about the idealised problem; the export evidence downgraded
to NO VERDICT.

### A9. My "more budget" hypothesis — refuted by my own run
Argued Codex's system failed on time with 11 GB unused, so a longer budget was
the lever, and queued 3 hours.  **Still NO VERDICT at 3 hours.**  The hypothesis
was mine and the refutation is mine.

### A10. Family B presented as *the* second family
Reported family B (`f' = sigma^2`) as the x-degree-1 solution set.  It is the
`c_4 = c_5 = 0` slice of a **3-parameter** family (`FAMILY_C.md`).  Understated
the degenerate locus in `CLAUDE-005`/`OPUS43-009`; corrected in `OPUS43-010`.

### A11. Minor: guessed where `p_16_8` enters
Predicted it first appears at level `Q[17]`; measured `Q[20][6]`.  Guess
replaced by measurement.

---

## B. My errors caught by Codex

### B1. Overstated the classification (CODEX-004)
I wrote that "the stratum `p_1_1 = 0` is exactly `P = x + f(y)`" and told him his
chart was settled and he should skip it.  **Wrong.**  `CLASSIFICATION.md` proves
a theorem about the *x-independent stratum* — every `p_{j,i} = 0` for `i >= 1`.
`p_1_1 = 0` kills only the `xy` coefficient and leaves all the others free.
His diagnostic settled it against me: rank 14 in 58 chart variables, tangent
dimension 44, with directions turning on `p_8_0` and `p_14_8`.
My artifact was correctly scoped; my **message** promoted it.  Corrected in
`FAMILY_B.md`, `MORNING.md`, the PR body, and the mailbox, with the suggestion
that he skip his lane explicitly withdrawn.

### B2. Incomplete non-degeneracy condition (CODEX-003)
I saturated `p_16_8` alone.  The mutable Newton vertices are **six**:
`p_8_0, p_14_8, p_16_8, q_12_0, q_21_12, q_24_12`.  So `p_16_8 != 0` is
necessary but **not sufficient** — sound as EMPTY-pruning, insufficient for
accepting any NONEMPTY point.  Adopted.

---

## C. Errors and misdiagnoses I found in the pre-existing campaign

### C1. The pentagon was never rigid
`pent/RUNLOG_NOTES.md` states the gauge `p_1_0 - 1` makes the system rigid so
msolve's solve mode applies.  Measured torus rank: raw **2**, with that gauge
**1**, rigid only with a second gauge.  One gauge where two were needed.

### C2. The target was mis-specified — the system is NONEMPTY
`pent_L23.ms` has an exact rational witness (`P = x + y`), verified against the
untouched export and independently by Codex.  "Prove pentagon case (1) EMPTY"
is **false as exported**.  The export contains **zero saturation rows**; the
bottom-edge code is careful about exactly this and the pentagon export is not.
Together with C1, this explains roughly a dozen hours of OOMs and timeouts as
NO VERDICT *by construction*.

### C3. `pent_slice.py` cannot find what it looks for
It fixes 45 of 58 parameters to uniformly random values.  A random affine
subspace of codimension 45 meets a variety of dimension `d` only if `d >= 45`.
Its own controls are sound and pass — the instrument is honest, it is **aimed
wrongly**, and every EMPTY it returns is uninformative by construction.

### C4. 14 affine variables, not 13
`p_11_6` enters affinely and was not previously counted.

### C5. MISS-3's "predicted FAST" forecast refuted
The `d=12` chart-N cell was recorded as predicted fast (non-resonant seed).
Measured: **>14 GB and >45 minutes**, OOM.

### C6. Interpretation guard
A 0-byte `.out` with exit 137 is OOM, never EMPTY.  The three archived 0-byte
N-chart `.out` files in `wave5/ms2/` are almost certainly this, not silent
successes, and should be re-checked before any of them is quoted.

---

## D. Knock-on: an error Codex caught in his own work

After I published the A3 retraction, Codex retracted the stronger reading of his
own `formal_arc_probe.py` — it chooses one particular correction with every free
coordinate zeroed, the **same greedy-path failure mode**.  Its report that
prescribed schedules stop at order 1 is a statement about that path, not an
exclusion.  He is replacing it with a kernel-aware search.

---

## What the pattern says

Of the twelve errors in my own work, **eleven were caught by a control, an
assertion, or a refusal to report before tracing a cause** — not by reading the
code again:

| mechanism | caught |
|---|---|
| a control that was allowed to fail | A1, A3 |
| an assertion inside the routine | A4 |
| implausible uniformity in output | A2 |
| tracing a discrepancy before reporting it | A5 |
| re-deriving against what the object actually is | A8 |
| a collaborator's independent check | B1, B2 |
| my own experiment refuting my own hypothesis | A9 |

The two that would have done real damage — A3 (a false rigidity theorem) and B1
(telling a collaborator to abandon a live lane) — were both **confident, clean,
quotable results**.  Neither looked wrong.  That is the argument for running the
positive control even when the answer looks right, and for stating scope
precisely in messages and not only in artifacts.

---

## A13. Re-introduced a known failure mode — my memory cap segfaulted both Cor 5.7 runs

At 05:45 I ran the planted bilinear instance under `ulimit -v 3000000` and it
segfaulted with

    Enlarging exponent vector for hash table failed
    for esz = 2097152, segmentation fault will follow.

I diagnosed it correctly at the time (msolve reserves address space for its
exponent hash table, so a virtual-memory cap kills it rather than bounding it),
wrote it down, and then at 15:21 **built the same cap into the restart-resilient
runner** — which promptly segfaulted both Cor 5.7 jobs at 192 s and 264 s:

    job=cor57_g2    exit=139  wall=192s  verdict=NO VERDICT (empty output)
    job=cor57_s1_g2 exit=139  wall=264s  verdict=NO VERDICT (empty output)

Both are NO VERDICT **caused by my own containment**, not by the mathematics.
Roughly 8 minutes of compute wasted and, worse, two verdicts that looked like
data and were not.

Fixed: the runner now takes `cap=none` for msolve jobs and relies on timeout plus
one-job-at-a-time; a genuine memcg OOM is still recorded as NO VERDICT.

**The lesson is not the bug, it is the repetition.**  Every other error tonight
was caught by a control; this one was caught by *reading my own notes ten hours
later*.  Writing a failure down is not the same as building the guard, and a
ledger only helps if the fix goes into the tool rather than the prose.

## A14 — my minor enumerator silently reported "inconsistent" when the
## coefficient matrix was column-rank-deficient

`cascade_fast.py` extracted the residual conditions at each rung as the
`(rM+1)`-minors of the augmented matrix `[Mat|vec]`, but guarded the enumeration
with `if Aug.shape[1] == rM+1`.  That holds only while `Mat` has **full column
rank**.  At rung 15 the rank dropped (`rank(Mat) = 7`, 8 unknowns), so
`Aug.shape[1] = 9 != 8`, the loop broke immediately, the condition list came back
empty, and the script printed **"still inconsistent"**.

That line was a **bug in the extractor, not a mathematical result**, and it is
retracted.  The correct enumeration ranges over row *and* column subsets of size
`rM+1`, which is what `rung17.py` already did correctly one rung earlier — the
same lesson as A13: I had the right code in hand and did not reuse it.

The rank drop is not an anomaly either.  It is exactly what the ODE picture
predicts: rung `d` is a first-order linear ODE for `B_{d-7}`, so its solution
carries a **free constant of integration**, and that constant is the kernel
vector making `Mat` column-rank-deficient.  A one-dimensional kernel here is a
signature of correctness, not of failure — and it is the same kernel freedom
whose greedy elimination manufactured the false obstruction retracted in A3.

**Never read "no solution returned" as "no solution exists."**  That is the third
time this exact substitution has been caught in this campaign (C6, A3, A14).

## A15 — I built a search instrument whose controls I ran *after* the search,
## and one of them failed

`search_upper.py` pinned the nine upper-edge coefficients to `c0 G^2` and tested
consistency of the 66 conditions in the remaining eight late variables over 3000
random points, reporting **0/3000 consistent**.

Its own planted-solution control **FAILED**: I built the planted right-hand side
as `-(M.tgt) - v` instead of `M.tgt`.  The 0/3000 is therefore **retracted** —
not a result about the pentagon.

Worse, fixing the control exposed that the search was hopeless by construction.
The system is 66 equations in 8 unknowns, so a random right-hand side lies in the
column space with probability about `p^-58`.  Sampling the 46 EARLY variables at
random can never land on the variety, whatever the upper edge does.  The rank
oracle is a **verifier**, not a search engine, and I pointed it in a direction it
could not possibly answer.

Two lessons, both already written down elsewhere in this file and both violated
again: **run the controls before reading the output**, and **check the arithmetic
of the search space before spending the search** (`pent_slice.py` died of exactly
this, catalogued as C3: codim-45 random slices cannot meet a low-dimensional
variety).  This is the same error as C3 with different numbers.

## A16 — msolve silently mis-parses parentheses and reports a FALSE EMPTY

`build_subst.py` substituted the upper-edge theorem into Codex's export, writing
the replacements parenthesised: `p_16_8 -> (c0*(g0*g0+...))`.  msolve returned in
**0 seconds** with `#length of basis: 1 element` and `[1]:` — the whole ring,
i.e. **no solutions**.

That is not a result.  Demonstration, two files differing only by parentheses:

    x,y / 1000003 / x*y-1, x+y        ->  basis of 2 elements   (CORRECT)
    x,y / 1000003 / (x)*(y)-1, x+y    ->  basis [1]             (FALSE)
    x,y / 1000003 / x-1, x-2          ->  basis [1]             (genuinely empty)

msolve's `.ms` reader wants **fully expanded** polynomials.  Given parentheses it
does not error, does not warn, and exits 0 — it reports the ideal as `(1)`, which
is indistinguishable from a real emptiness proof.

**Any parenthesised `.ms` file fed to msolve yields a spurious EMPTY.**  The
0-second wall time is the only tell, and only if you look.  I looked because a
170-variable system finishing instantly is impossible, not because the verdict
looked wrong — the verdict looked like exactly the result I was hoping for.

Two consequences recorded:
1. `session43/queue/runner.sh` now refuses to run msolve on any input containing
   `(`, and treats a 0-second msolve completion as NO VERDICT.
2. `/tmp/red/reduced.ms` (the 214-variable additive form) also contains
   parentheses.  It is **Singular-only**; Singular parses them correctly.

This is the campaign's fourth instance of a tool's silence being read as a
verdict (C6, A3, A14, A16), and the first where the false reading was EMPTY
rather than "no solution" — i.e. the first that would have been reported as a
mathematical claim about the Jacobian conjecture.
