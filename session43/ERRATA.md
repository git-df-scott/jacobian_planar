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

## A17 — I ran a verification job concurrently with a heavy solver, and it
## triggered the OOM

`eighth_g2` (msolve `-g 2`, 179 vars) was killed at 270 s, exit 137.  `dmesg`:

    claude invoked oom-killer: ... oom_memcg=.../claude-code-bash, task=msolve
    Killed process 23036 (msolve) total-vm:21976024kB, anon-rss:13961020kB

msolve had reached **13.96 GB** of a ~15 GB shared cgroup, so it was within
seconds of dying on its own.  But the allocation that *tripped* the killer came
from a claude-side process — my `verify_all.py` sweep, which I started while the
solver was running.

So unlike the two Cor 5.7 OOMs (where the only other process was 101 MB and I
checked before attributing), **this one I cannot cleanly call a genuine ceiling**.
The verdict is `NO VERDICT` either way, but the *cause* is mixed, and recording
it as a clean memory ceiling would be an overclaim.

This is A7 recurring: **one heavy job at a time**.  Writing that rule down three
times has not made me follow it; the fix is the same as A13's — the guard, not
the note.  `runner.sh` should refuse to start a solver while another is running,
and I should not start sympy sweeps against a live solver.

**Wider consequence.**  Three targets have now hit ~14 GB: the degree-22 export,
both Cor 5.7 shapes, and the 179-variable eighth-power target.  **This box cannot
decide the pentagon as a monolithic system, at any of the formulations tried.**
That is a real finding and it redirects the work: the w-cascade is
block-triangular with a largest block of 20 equations, so the right move is 22
small solver calls, not one large one.

## A18 — the v43 OOM, with three of my own jobs running alongside it

`msolve -g 2` on v-cascade levels 4+3 (38 vars, 36 equations) was OOM-killed,
exit 137, after reaching ~12 GB.  **Three of my own sympy jobs were running at the
time** — `descend2.py` (1.0 GB, 37 minutes), `l16_h6.py` (249 MB) and
`verify_sol_l16.py` (173 MB), about 1.4 GB together.  As in A17 I cannot call
this a clean memory ceiling: the verdict is `NO VERDICT` and the cause is mixed.

That is the **fourth** violation of one-heavy-job-at-a-time (A7, A13, A17, A18),
and worse, two of those jobs were **superseded work** — Codex's exact level-16
branching condition had already made both obsolete and I left them burning memory
for half an hour.

Informative anyway: a 38-variable, 36-equation system blowing past 12 GB says
v-cascade levels 4+3 is a genuinely hard Groebner problem, not an artefact.

## A19 — `pkill -f` / `pgrep -f` keeps matching my own shell

Three times today a `pkill -f <pattern>` or a `pgrep -f` loop has killed the
command issuing it, because the pattern appears in the caller's own command line:
once on `queue/runner.sh` (killing two background watchers), once on `msolve`
(killing a command mid-heredoc, losing an unwritten file), and once on
`l16_h6.py`.  Exit 144 each time.

Fix, now used: resolve PIDs first with `ps -eo pid,args | grep <pat> | grep -v
grep | awk '{print $1}'` and kill those, never `pkill -f` on a pattern that
appears in the current command.

## A20 — I reported a DISAGREEMENT with Codex on the strength of an instrument
## that fails its own control. Retracted.

I tested Codex's level-16 branch 1 (`sigma^5 | h_7` and `sigma^2 | h_6`) and
reported **INCONSISTENT at level 16**, contradicting his derivation, and sent that
to him as OPUS43-020.

Building a second, independent test in exact `F_p` arithmetic exposed the
problem.  That harness carries a control: `sigma^2 | h_7` **must** clear level 18,
since level 18's condition is exactly `sigma^2 | h_7` — proved three independent
ways (2-variable w-cascade, 1-variable s-ladder, diagonal recursion).  The
harness reports it **INCONSISTENT at level 18**.

**Control failed => every verdict from that harness is void**, including:

* branch 1 INCONSISTENT at level 16 (the claimed disagreement) — **RETRACTED**;
* `sigma^{4..8} | h_7` INCONSISTENT at level 16 — **suspect**, same code path;
* `sigma^{0..4} | h_6` INCONSISTENT at level 17 — **suspect**, same code path.

Two bugs found and fixed along the way, and the control still fails, so there is
at least a third:

1. `h_6` was fixed numerically although `h_6` is one of **level 18's unknowns**
   (level `L` introduces `h_{L-12}` and `g_{L-8}`), over-constraining the level.
2. `sp.Matrix.rank(iszerofunc=...)` does **not** do modular arithmetic in the
   pivots — it eliminates over `ZZ` and only tests zero mod `p`.  That is not an
   `F_p` rank.  Replaced with an explicit mod-`p` rref.

**What I should have done:** run the control *before* reporting the
disagreement.  I have written that rule down twice already (A15, and the
"controls before output" lesson in the sweep) and broke it again, this time in
the worst possible direction — telling a collaborator his correct result was
wrong.  To his credit, the thing that caught it was building the second
instrument he effectively asked for.

The scientific position is now: **Codex's level-16 branching condition stands
unchallenged.**  I have no working independent test of it.  Producing one — or an
explicit `F_p` witness of branch 1 — is my job before I say anything further
about his result.

## A21 — "36 new conditions from the v-cascade" was wrong; the two cascades are
## the same equations regraded

I reported (B3/B4, OPUS43-024/025/026) that substituting the eighth-power theorem
into the 45 v-cascade bottom conditions leaves **36 new conditions tying the two
ends together**.  Codex (`cc04dad`, `PENTAGON_VBOTTOM_BRANCH2.md`) proved the
framing wrong, term by term and without any specialisation:

for a monomial `p_{j,i} q_{l,k}`, writing `d = 2i-j`, `e = 2k-l`, its coefficient
at v-level `V` is `d k - e i`, while its coefficient in the w-ladder at
`a = j-i`, `b = l-k` is `b i - a k` — **and these are identically equal.**  If it
occurs at `r^n` then `a + b = n - V`.

So every one of the 45 v-bottom equations **is literally a coefficient of a
w-level equation**, distributed over w-levels 20..12 as `9,8,7,6,5,4,3,2,1`.
They are not independent information; the two cascades are one system in two
gradings.  That is also the real reason both totalled exactly 301 — I had
recorded the coincidence as mutual verification, which it is, but then
misread it as independence.

**What survives:** the 301 = 301 agreement is still a genuine cross-check of the
two support reconstructions.  What does not survive is "36 new conditions".  The
correct statement is that 39 of the 45 are implied by w-levels 15..20, and 6 are
coefficients of w-levels 14, 13, 12 — which my own descent has since cleared, so
all 45 are now accounted for.

Practical consequence, and it is a simplification: **the v-cascade need not be
tracked separately.** Attack the w-cascade only.

## A22 — RESOLVED: the pentagon sits at (72,108) via a 3:1 cyclic cover

**RESOLVED in the campaign's favour.** `BRACKET.md` derives
`dP ^ dQ = x^2 dx ^ dy = d(x^3/3) ^ dy`, so with `s = x^3/3` the pentagon
searches for a Keller map in coordinates `(s,y)`, and `s = x^3/3` is a **3:1
cyclic cover of the x-line**. Recomputing degrees straight from the s-ladder
supports, where `P = sum h_{a,i} y^a (xy)^i` gives the monomial `x^i y^(i+a)`:

    P : x-degree 8,  y-degree 16,  total degree 24
    Q : x-degree 12, y-degree 24,  total degree 36

The x-degrees `8` and `12` match `EDGE_LADDER.md`'s `m` and `n` exactly, and
`3 * (24,36) = (72,108)`. So the ordinary `(x,y)` degrees are `(24,36)` and the
campaign's `(72,108)` is that object counted through the cover. The factor of
three IS the cover. The `B = (4,8)` versus `L = 3` tension noted below is
bookkeeping about which coordinates `B` is written in, not a contradiction.

**The consequence that matters more than the resolution.** `BRACKET.md` states:

> the object under search is a Keller map on a cyclic cover / orbifold
> quotient, **not on the plane itself** — `P` and `Q` are polynomial in
> `(x,y)`, hence algebraic-but-**not-polynomial** in `(s,y)`.

So a NONEMPTY pentagon would **not**, by itself, be a counterexample to the
plane Jacobian conjecture. It would be a Keller map on a 3:1 cover, and
descending to the plane needs a further argument nothing here supplies. This
cuts both ways: the EMPTY verdicts are weaker evidence about JC2 than "the
(72,108) case is closed" would suggest, and a hypothetical witness would have
been weaker as a counterexample than the framing implies.

### A22, as originally raised, retained for the record

## A22 (original) — OPEN VERIFICATION GAP: does the pentagon system really sit at (72,108)?

**Status: a question I could not settle from the repository, raised rather than
answered. Not a claim that anything is wrong.**

The pentagon's Newton polygons, as recorded in `EDGE_LADDER.md` and audited in
`WITNESS.md`, are

    N(P): (0,0), (1,0), (8,14), (8,16), (0,8)
    N(Q): (0,0), (2,1), (12,21), (12,24), (0,12)

Taking total degree as `max(i+j)` over the vertices gives

    deg P = 8 + 16 = 24 ,   deg Q = 12 + 24 = 36 ,

not `72` and `108`. The ratio is right — `24 : 36 = 72 : 108 = 2 : 3` — and
indeed `(72,108) = 3 * (24,36)`, so the two differ by an exact factor of three.

The top vertices do factor consistently with the GGV framework `en(P) = 2B`,
`en(Q) = 3B`:

    en(P) = (8,16) = 2 * (4,8) ,  en(Q) = (12,24) = 3 * (4,8) ,  so B = (4,8) .

But `41.md` records `L = 3` for `(72,108)` and `L = 4` for `(108,72)`, where `L`
is the first coordinate of `B`. Here that coordinate is `4`.

### Why this matters, and why it does NOT invalidate the computations

It does not affect whether the EMPTY verdicts are correct. Those are statements
about an explicitly constructed polynomial system, they were computed in
characteristic 0, and the pipeline that produced them now passes an end-to-end
positive control (an automorphism at `(2,4)` -> NONEMPTY) and a negative control
(`(2,3)` -> EMPTY in all 12 charts). What is in question is not whether the
system is empty but **which degree pair the system is about**.

That distinction is sharp here. If the pentagon is literally `(24,36)` in
ordinary coordinates, then its max degree is `36`, comfortably inside the range
where JC2 is already known (Moh: max degree at most 100), and emptiness would be
expected rather than informative. If instead the pentagon is a reduced or
blown-up representation whose ordinary degrees are `(72,108)`, the verdicts bear
on genuinely open territory.

### What would settle it

One of:

* the explicit map from a pentagon solution `(h_a, g_b)` back to a pair
  `(P,Q)` in ordinary `x, y` coordinates, from which `deg P` can be read off
  directly; or
* the derivation that produced these vertices from `(72,108)` — attributed in
  `EDGE_LADDER.md` to Codex's reconstruction — including whichever coordinates
  the polygon is expressed in; or
* a statement of `B` and `L` for `(72,108)` that reconciles `L = 3` with
  `B = (4,8)`.

Flagged for Codex, who reconstructed the polygons. Until it is resolved, the
correct phrasing of every verdict in this campaign is "the pentagon system is
empty", not "there is no counterexample at (72,108)".


## A23 — I wrote A22 to the wrong file

`cat >> ERRATA.md` was run from the repository root, where no `ERRATA.md`
existed, so it CREATED one instead of appending to the real errata at
`session43/ERRATA.md`. The entry was then committed, so it looked filed while
sitting in a file nothing reads.

Same class as the earlier slip where `wcascade.py` was written to the repository
root instead of `session43/pentagon` and sat uncommitted for a cycle. The lesson
is the same and evidently needed restating: a redirect or heredoc resolves
against the shell's current directory, which in this session RESETS between
tool calls. Use absolute paths for appends, and verify the target exists before
appending rather than after.

A22 has been merged into this file and the stray root copy deleted.
