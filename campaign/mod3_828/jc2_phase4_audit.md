# Phase 4 direct-attack audit — adversarial review

**Scope.** `session19_general_endgame.py`, `session19_parameter_lattice.py`,
`session19_general_chart.py`, `jc2_escape_hatch.py`, `jc2_target_72_108.py`,
`jc2_phase4_direct.py`, cross-read against `session19_report.md` and
`session20_report.md`. Test code: `jc2_phase4_audit.py` (33/33 of its own
checks land where independently predicted — see that file for exactly what
each line means before reading a bare PASS as "the audited code is fine";
several PASS lines report **confirmed bugs**). No audited file was modified.

## Verdict, up front

**The arithmetic behind the ten "open" chain degrees at (72,108) is correct.**
Every one of the ten was independently re-derived from scratch — via a
different sympy code path than the audited files use, and cross-checked once
more in plain Python `fractions.Fraction` with no sympy involved at all — and
all ten check out exactly, including the two exclusions (`k=1`, `k=2`).

**But "trustworthy as *the* target" is not supported.** The ten points are the
open points of **one** `(rho=3, m=1)` slice of a much larger admissible
parameter lattice that has never been searched. The claimed justification for
treating that slice as canonical — the lattice relation `n = b·k + H`
(claim 6) — is **not a general derivation**; it is Borisov's specific
numerical coincidence `rho = b` (both equal 3) restated as if it generalizes.
At every *other* admissible chart slope for the same cusp type, the whole
lattice is different, and none of those slices have been examined for
(72,108). Separately, two files in this repo (`jc2_escape_hatch.py`'s general
sweep and `jc2_target_72_108.py`'s own (72,108) analysis, plus
`session20_report.md` which reports both) still contain a **confirmed wrong
count** — a real, reproducible bug, not a stale-documentation nitpick — that
was fixed in `jc2_phase4_direct.py` but never back-ported to the files or the
report that state it in prose.

So: **use `jc2_phase4_direct.py`'s ten `R`'s, not `jc2_target_72_108.py`'s
eleven or `jc2_escape_hatch.py`'s twenty** — and treat "ten" as "ten within an
unjustifiably narrow slice," not "the admissible lattice at (72,108)."

---

## Ledger

| # | Claim | Axis | Verdict | Severity |
|---|---|---|---|---|
| 1 | Master identity `[q^D]K = g0^(a+b)(kR'+DR(log g0)')` | a | **SURVIVES** | — |
| 2 | Specialization to `g0=alpha(v+1)^m v^sigma`, order relations (Q)/(V) | a | **SURVIVES** | — |
| 3 | Chart-factor formulas (`det`, `A=eps(Q'-P')-1`) | a | **SURVIVES** | — |
| 4 | `m >= 1` forced, unconditionally | b | **SURVIVES**, given the stated `k>=1` hypothesis; the bare inequality *does* fail at `k=0`, but `k=0` is never fed through anywhere | note only |
| 5 | Boundary-case robustness (`D<=0`, `m=0`, `sigma=0`, non-coprime, `n` not divisible by `b`) | c | **No live bug**; real self-validation gaps found (functions accept mathematically-excluded inputs silently) | low |
| 6 | Escape criterion + late-added "forced constant ≠ 0" (k=1 closure) | d | **SURVIVES** — independently re-confirmed correct and necessary | — |
| 7 | `jc2_escape_hatch.py` §3: "20 of 40 lattice points have an inhabited escape" | d | **BUG CONFIRMED**: 7 of the 20 are false opens; true count 13/40 | **moderate** |
| 8 | `jc2_target_72_108.py` / `session20_report.md`: "11 of 12 (72,108) points open" | d | **BUG CONFIRMED (stale)**: superseded by `jc2_phase4_direct.py`'s own later fix (10 open), never back-ported | **moderate** |
| 9 | The ten explicit `R(v)` at (72,108) (`jc2_phase4_direct.py`) | d | **SURVIVES** — independently reproduced exactly, incl. a sympy-free cross-check | — |
| 10 | No floating point / no simplify-masking | e | **SURVIVES** | — |
| 11 | Lattice relation `n = b·k + H` (claim 6), specifically `G = b·k` | f | **NOT GENERAL** — coincidence of `rho=b`, `m+sigma=0`; fails at every other admissible `rho` | **significant — bears directly on the verdict** |
| 12 | False-CLOSED search (the dangerous direction) | d | **None found**, in the 40-point sweep + 12-point (72,108) family checked | reassuring, but not exhaustive |

---

## Axis (a): algebra — re-deriving claim 1 independently

**Method.** Before opening `session19_general_endgame.py`'s derivation, I
derived `[q^D]K = g0^(a+b)(kR' + DR(log g0)')` by hand from the given hint
`J(y1,y2) = J(y1^a-y2^b,y2)/(a y1^(a-1))` (Route 2). Sketch: write
`F = y1^a-y2^b = y2^b·G` with `G = F/y2^b`; then
`J(F,y2) = y2^b·J(G,y2)` exactly (the `y2^b`-factor is "Jacobian-silent"
against `y2`); expand `G = q^D R(v) + O(q^{D+1})` and `y2 = q^{-ak}Y2(q,v)` in
`q`, extract the leading order of `J(G,y2)`, multiply back by `y2^b`, divide
by `a y1^{a-1} = a q^{bk-abk}(g0^{b(a-1)}+O(q))`, and simplify the `q`- and
`g0`-exponents. First pass had an arithmetic slip (`y2^b`'s `q`-exponent is
`-abk`, not `-bk`); once corrected the `q`- and `g0`-exponents collapse to
exactly `D` and `a+b`, reproducing the claim.

**Independent computational check** (`jc2_phase4_audit.py`, axis a): rather
than trust hand algebra alone, I built **explicit** formal power series
`Y1(q,v), Y2(q,v)` satisfying the exact defining relations
(`[q^i](Y1^a-Y2^b)=0` for `i<D`, `=g0^{ab}R` at `i=D`), with **nonzero
"gauge" freedom** injected at every intermediate order `q^1..q^{D-1}` — since
the report's formula for `[q^D]K` mentions only `g0, R, k, D`, never the
lower-order data, this is the sharpest test of whether that's really true.
Checked at `(a,b,k,D) = (2,3,2,3)`, `(1,1,1,1)`, `(3,2,3,4)`, and
`(2,4,1,2)` [non-coprime `a,b`, to see whether the *algebra* — as opposed to
the cusp-type *interpretation* — needs coprimality]. **All four pass exactly**
— the gauge freedom cancels completely, confirming the formula really is
gauge-invariant as claimed, and that coprimality is not used anywhere in the
identity itself (it is a separate, correctly-enforced interpretive constraint
on what counts as a valid cusp type, applied via `gcd(a,b)==1` filters
elsewhere).

Compared against the file afterward: `session19_general_endgame.py`'s Route 1
(factorization `y1=y2^{b/a}(1+eps)`) and Route 2 (chain-block projection,
matching my own derivation) match my independent result exactly, including
the operator `k·d/dv + D·(log g0)'`.

**`D=0` boundary.** Testing `D=0` inside the same construction shows it is
**degenerate under the framework's own definitions**: `g0` is defined
precisely so `Y1|_{q=0}=g0^b`, `Y2|_{q=0}=g0^a` — which forces the `q^0`
coefficient of `(y1^a-y2^b)/y2^b` to vanish identically. So `D=0` would force
`R=0`, contradicting "`R` is the leading *nonzero* coefficient at order `D`."
`D>=1` is baked into the setup, not a hypothesis anyone verifies — worth
knowing because nothing downstream checks it explicitly (see axis c).

**Chart-factor generality** (`session19_general_chart.py`). Independently
re-derived both `det ∂(q,v)/∂(x1,x2) = -eps·x1^(P+P'-1)x2^(Q+Q'-1)v^{-w}` and
`A := ord_{v=-1}(1/det) = eps(Q'-P')-1` by hand, via explicit inversion of
`(x1,x2) -> (U,q,v)` (solving the 2×2 log-linear system
`P log x1 + Q log x2 = log U`, `P' log x1 + Q' log x2 = log q + w log v`).
Both match the file's formulas exactly. Cross-checked symbolically on 6 fresh
unimodular charts not in the file's own test set — all pass.

**Nothing broke here.** Claim 1, its specialization, and the chart-factor
formulas all survive independent re-derivation by two different methods
(hand algebra + a from-scratch symbolic construction with an explicit
gauge-invariance stress test).

---

## Axis (b): hidden assumptions in "`m >= 1` forced"

The argument: `A~_n(U) = sum_i c_{i,n+rho·i} U^i`, and `y1` having
nonnegative exponents forces `j = n+rho·i >= 0`; at `n=-bk` this needs
`i >= ceil(bk/rho)`, and the claim is `ceil(bk/rho) >= 1` always, hence
`U | g^b`, hence `m = ord_{U=0}g >= 1`.

**Attack 1 — `k=0`: succeeds, on the bare inequality.**
`ceil(b·0/rho) = ceil(0) = 0`, which does **not** force `i>=1`. So the
displayed inequality genuinely fails at `k=0`, and "`m>=1` always" as a
statement about the raw formula is false there.

**But this doesn't reach a live bug.** `k>=1` ("`y1` has a genuine pole along
`E`") is stated as an explicit input hypothesis in `session19_report.md`'s
parameter table, and *every* downstream loop over `k` in all six audited
files starts at 1: `session19_general_endgame.py` §6 (`for k_ in
range(1,8)`), `jc2_escape_hatch.py` §3 (`for kk in range(1,8)`),
`jc2_target_72_108.py` / `jc2_phase4_direct.py` (`for k in range(1,
N//B+1)`). `k=0` is never smuggled through anywhere.

**Attack 2 — `rho > b·k`: fails, tried and did not break.** `ceil(x) >= 1`
for *any* `x > 0`, regardless of magnitude — tested `rho=1000` against
`b·k=1`: `ceil(1/1000) = 1`, still `>=1`. No `rho`, however large relative to
`b·k`, can defeat this. The task's suspicion here does not pan out.

**Attack 3 — negative `sigma`: fails, irrelevant by construction.** `sigma`
is the axis order at `v=0` (a different corner of the chart entirely); it
does not appear anywhere in the `v=-1` corner-order argument (confirmed by
inspection of `min_U_order()` in `session19_general_endgame.py` §6, which
takes only `b, k, rho`).

---

## Axis (c): boundary cases — silent nonsense or refusal?

Probed the shared escape-solving logic (the function underlying
`escape_solution` in `jc2_escape_hatch.py` / `jc2_target_72_108.py`) directly
with excluded parameter values:

| input | result | assessment |
|---|---|---|
| `k=0` | returns `None` (explicit `if k==0: return None` guard) | handled |
| `a=b=1` | claim-1 construction passes cleanly | handled (tested under axis a) |
| `D=0` | **silently returns a "solution"** (deg S=4, no warning) | **robustness gap** — `D=0` was shown degenerate under axis (a); the function does not check `D>=1` |
| `D=-5` | **silently returns a "solution"**, same as above | **robustness gap** |
| `m=0` | **silently returns a "solution"** with `p=(a+b)·0-1=-1` (a *negative* pole order, i.e. actually a zero, treated without comment) | **robustness gap** — no cross-check against the `m>=1` lemma proved elsewhere in the same campaign |
| `sigma=0` | accepted; forces `CONST=D·sigma·s0=0` identically, matching `jc2_escape_hatch.py`'s own docstring remark that "a nonzero Keller constant needs sigma != 0" | correct, not a bug |
| non-coprime `(a,b)=(2,4)` | claim-1 algebra unaffected; lattice-enumeration code correctly filters via explicit `gcd(a,b)==1` elsewhere | handled |
| `n` not divisible by `b` (tested `N=7,B=5`) | `range(1, N//B+1)` still correctly yields `k<=floor(n/b)` via Python's floor division | **no bug** — tried and did not break |

**None of the robustness gaps are live bugs** — `D`, `m`, `k` are never fed
out-of-hypothesis values anywhere in the actual (72,108) computation (`D` is
always `(a+b)k+1-rho >= 3` there, `m=1` is hardcoded, `k` always starts at 1).
But the functions themselves perform **no precondition validation** — if
reused elsewhere with a `D<=0` or `m<=0` from a different part of the
campaign, they would produce a plausible-looking but meaningless "escape"
with no error.

---

## Axis (d): the late-added condition, and a wider bug it exposes

**Claim being tested.** The escape is inhabited iff `k | D(m+sigma)`,
`deg S = p - D(m+sigma)/k >= 0`, `k·p != D·m`, **and** the ODE's forced
constant is nonzero (added after the original three conditions).

**Independent re-verification, from scratch.** Built the linear system for
the degree-`d` polynomial `S` directly (not via `sympy.linsolve`/`symarray`
as the audited code does, but via `sympy.Matrix.nullspace()` — a different
code path), for all 12 `(72,108)` lattice points (`a=2,b=3,m=1,sigma=-1`,
`D=5k-2`, `k=1..12`). Key structural fact, re-derived independently: because
the `v(v+1)S'` and `vS` terms in the escape ODE both carry an explicit factor
of `v`, the forced constant is *exactly* `CONST = D·sigma·s0` (`s0 = S(0)`) —
no simplification assumption, a direct polynomial fact. Results:

- **The null space is exactly 1-dimensional at all 12 points.** This matters
  because `jc2_phase4_direct.py`'s normalization (`sub[lead]=1`, all other
  free symbols `=0`) would be an *arbitrary, unjustified gauge choice* if the
  solution space were 2+ dimensional — a different choice could then flip a
  "forced c=0" into a genuine nonzero escape, i.e. a **false CLOSED**, the
  dangerous direction. Confirmed nullity `=1` everywhere: **no such ambiguity
  exists**.
- `k=1` (`D=3`): null space's unique basis vector has `s0=0` **identically**,
  so `CONST=0` for *every* scalar multiple. **The late-added condition is
  verified correct and necessary for k=1.**
- `k=2` (`D=8`): **also** lands in the identical "`s0` forced to 0" bucket —
  i.e. the file's `k·p=D·m` shortcut (`2·4=8=8·1`) and the file's `k=1`
  "forced constant" check are two *proof routes* to the same underlying
  linear-algebra fact, not two logically independent phenomena. Worth being
  precise about this: nobody should expect a *third*, differently-shaped
  self-kill lurking elsewhere in this family — the mechanism really is
  singular (a forced-zero linear functional on a 1-dimensional null space),
  and it accounts for exactly these two points.
- `k=3..12`: all ten independently confirmed **genuinely open**, with the
  exact nonzero constants reproduced (`-455/243` at `k=3` after un-normalizing
  from the file's own `S`-scale of `-243`, etc. — see `jc2_phase4_audit.py`
  output for all ten).

**Cross-checking the ten explicit `R(v)` formulas.** Re-verified all ten of
`jc2_phase4_direct.py`'s printed `S(v)` polynomials by direct substitution
(`Poly.degree()==0` check, not `simplify()`) — every one satisfies
`k·v(v+1)S' - 4k·vS - D·S = CONST` with the *exact* claimed nonzero constant.
Additionally cross-checked the `k=3,D=13` case in **pure Python
`fractions.Fraction`, no sympy at all**, with a hand-coded polynomial
derivative, at four distinct rational `v` (`2`, `5`, `-3/7`, `11/4`) — all
four give `-455` exactly.

**The wider bug this method exposes.** Applying the identical, uniform
null-space check to `jc2_escape_hatch.py` §3's own general 40-point sweep
(five `(a,b,rho)` families, `k=1..7`, `m=1,2`) — first faithfully reproducing
its reported "20 of 40 escape open" — turns up:

> **7 of the 20 points that file calls "ESCAPE OPEN" are false opens**: the
> forced constant is identically zero on their (1-dimensional) solution
> space, exactly the pattern later fixed for (72,108)'s `k=1` — but this file
> was never patched. **True count: 13/40, not 20/40.**

The seven:

```
(a,b)=(2,3) rho=3 k=1 D=3  m=1 sigma=-1
(a,b)=(2,3) rho=3 k=1 D=3  m=2 sigma=-1
(a,b)=(2,3) rho=3 k=2 D=8  m=2 sigma=-1
(a,b)=(2,3) rho=8 k=7 D=28 m=2 sigma=-11
(a,b)=(1,4) rho=3 k=1 D=3  m=1 sigma=-1
(a,b)=(1,4) rho=3 k=1 D=3  m=2 sigma=-1
(a,b)=(1,4) rho=3 k=2 D=8  m=2 sigma=-1
```

Note the first row: `(a,b,rho,k,D,m,sigma)=(2,3,3,1,3,1,-1)` is **exactly**
the (72,108) `k=1` point — it was sitting, uncorrected, in
`jc2_escape_hatch.py`'s own printed output (`rows[:14]` in that file's source)
the entire time. **This invalidates:**

- `jc2_escape_hatch.py`'s own headline claim: *"20 of 40 admissible lattice
  points have an INHABITED escape"* — wrong; 13.
- `session20_report.md` §2: *"Open at 20 of 40 lattice points, including
  D=13,23,28"* — repeats the wrong count verbatim.
- `jc2_target_72_108.py`'s (72,108)-specific analysis, which predates the fix
  and still reports `k=1,D=3` as `ESCAPE OPEN`, concluding *"11 remain open
  at the endgame level"* and, in its closing summary, *"NOT ESTABLISHED: The
  other 11 chain degrees remain open."* — wrong; 10, and `jc2_phase4_direct.py`
  (the same repo, one file over, three hours later by file timestamp) already
  has the fix.
- `session20_report.md` §3 (the `(72,108)` table) and §5 (Scorecard), both of
  which say *"11 of the twelve... survive"* / *"Eleven of the twelve (72,108)
  chain degrees survive everything this session could throw at them"* — same
  staleness, repeated twice more in the same document.

This is a real, reproducible, file-timestamp-confirmed inconsistency (not
merely "the docs are behind"): `jc2_target_72_108.py` (Aug 12, 22:03) and
`session20_report.md` (Aug 12, 22:14) both predate `jc2_phase4_direct.py`
(Aug 13, 01:22), which contains the correct, later analysis but was never
back-ported into either. **A reader consulting `session20_report.md` or
`jc2_target_72_108.py` alone — which is exactly how a reader would normally
approach this repository — gets the wrong number and would treat `D=3` (k=1)
as a live target when it is provably not.**

**Searched for the reverse (false CLOSED) across both the 40-point sweep and
the 12-point (72,108) family: found none.** No point that any audited file
discards is actually open, in either dataset checked. This is the more
important direction to get right (per the task's own framing — a false
CLOSED discards real territory), and it held up everywhere I looked. I did
not, however, exhaustively search the *entire* admissible `(a,b,rho,k,m)`
space for false closeds — only the 40 points `jc2_escape_hatch.py` itself
examines plus the 12-point (72,108) family — so this is reassuring evidence,
not a certificate.

---

## Axis (e): numerics

`grep`-checked all six files for decimal literals, `float(`, `.evalf(`,
`numpy` — **none found** (only prose mentions of "arXiv:2204.14178" and
"(8,28) system," not numeric literals). Every `==0` zero-test in all six
files is preceded by `cancel(...)`, `cancel(expand(...))`, or
`Poly(...).degree()==0` / `.coeff_monomial(...)` — canonicalizing operations
with a completeness guarantee for rational-function identities, not
best-effort `simplify()` calls that could silently fail to reduce a nonzero
residual to a recognizable form. The one place a **fractional power** appears
— the `D=13` homogeneous solution `R_h = C(v/(v+1))^{13/3}`, exactly the kind
of expression that can trip up symbolic simplification — was independently
re-derived by hand (`d/dv[v^{13/3}(v+1)^{-13/3}] = (13/3)v^{10/3}(v+1)^{-16/3}`,
and `3v(v+1)` times that equals `13·v^{13/3}(v+1)^{-13/3}` exactly, matching
`R_h`'s own form) and confirmed via `cancel()`, which is a complete algorithm
here since `vp` is declared `positive=True` (branch-free). No masking found.

---

## Axis (f): the lattice relation `n = b·k + H`

**Is it forced, or fitted to one data point?** Traced the derivation in
`jc2_target_72_108.py` §1 explicitly: `G := deg g`, and by the (independently
re-verified) general relation `deg g = m + e = m + rho·k + sigma`. The file
then substitutes **Borisov's specific numbers** `(m,sigma,rho)=(1,-1,3)` to
get `G = 3k`, and immediately treats "`G = b·k`" (`b=3` for cusp `(2,3)`) as
if it were the general formula, using it verbatim to enumerate all 12 points
of the (72,108) lattice in §2 (`G, H = B*k, N - B*k`, no re-derivation via
`m,rho,sigma` per `k`).

**This is not general.** `G = m+rho·k+sigma` equals `b·k` for *every* `k`
simultaneously only if the `k`-independent part matches, i.e. only if
`rho = b` **and** `m+sigma = 0` **both** hold — two independent coincidences,
not consequences of the framework. Verified directly: for cusp `(2,3)`,
there are at least 8 admissible `rho` in `1..40` (values where
`(a+b) | 1+rho-rho²`, required for `sigma` to be an integer at all):
`3, 8, 13, 18, 23, 28, 33, 38`. At `rho=3`: `G(k) = 3k = b·k` for every `k`
— checks out, this is the one the campaign uses. At `rho=8` (`sigma=-11`):
`G(k) = 8k-10`, which equals `3k` only by coincidence at the single point
`k=2`, never identically. Every other admissible `rho` in the scanned range
gives yet another distinct, non-`b·k` formula.

**Consequences:**

1. **The D=13,23,28 retrodiction doesn't actually need claim 6.** It follows
   directly from relation `(Q): D=(a+b)k+1-rho`, established independently in
   Session 19, evaluated at `(a,b,rho)=(2,3,3)`, `k=3,5,6` — no reference to
   `G`, `H`, or `n=b·k+H` required. Re-derived directly: `D(2,3,3,k)` at
   `k=3,5,6` gives exactly `13,23,28`. So the retrodiction is real, but it was
   already implied by (Q); claim 6 doesn't add independent confirming
   evidence for *that* part.
2. **What claim 6 uniquely contributes is the upper bound** `k <= n/b` (via
   `H = n-bk >= 0`), which is what turns the unbounded family `D=(a+b)k+1-rho`
   into a *finite* 12-point lattice at (72,108). That bound rests on
   `H=n-G` being validated at exactly **one** `(k, n)` pair — Borisov's own
   certified box at `k=3`, `n=33` — with no second real construction to
   confirm the linear form `H=n-3k` (rather than some other function of `k`
   that also happens to equal 24 at `k=3`) generalizes.
3. **The practical upshot for (72,108):** both `jc2_target_72_108.py` and
   `jc2_phase4_direct.py` hardcode `rho, m, sig = 3, 1, -1` with **no scan**
   over the (at least 7) other admissible `rho`, nor over `m=2,3,...`. "The
   (72,108) chain-degree lattice" is really *the `rho=3, m=1` slice of the
   (72,108) lattice* — inherited wholesale from the one existing certified
   construction at a different degree pair, `(66,99)`, not derived for
   `(72,108)` on its own terms. Whether any of the other slices contain
   escape points, self-kills, or (most importantly) an actual realizable
   Keller pair is completely open and untouched by any of the six audited
   files.

---

## What survived (and what was actually tried)

- **Claim 1** (master identity): independent hand derivation (Route 2, as
  instructed) + a from-scratch symbolic construction with explicit
  gauge-freedom injected at every intermediate order, on 4 parameter sets
  including a non-coprime cusp type. No discrepancy anywhere.
- **Claim 2 / order relations (Q),(V)**: direct exponent algebra, trivial but
  checked; no discrepancy.
- **Chart-factor formulas**: independently re-derived by hand via explicit
  coordinate inversion, matched on 6 charts outside the file's own test set.
- **`m>=1` forced**: survives as stated, given the explicit `k>=1` hypothesis.
  Attacked with `k=0` (breaks the bare inequality but is never live), `rho`
  up to 1000× `b·k` (does not break it), negative `sigma` (irrelevant to this
  lemma). Two of three attacks failed outright; the third doesn't reach a
  live bug.
- **The late-added "forced constant" condition and the ten explicit R's**:
  independently reproduced via a different sympy code path (`Matrix.nullspace`
  instead of `linsolve`/`symarray`), confirming no hidden multi-dimensional
  gauge ambiguity anywhere in the 12-point family, and cross-checked once
  more in pure Python with no sympy involved.
- **Numerics**: no floats anywhere; all zero-tests use canonicalizing
  operations; the one fractional-power identity independently confirmed by
  hand.
- **False-CLOSED search**: none found in the 40+12 points checked.

## Bugs found (and what they invalidate)

1. **`jc2_escape_hatch.py` §3**: 7/20 "ESCAPE OPEN" verdicts are false
   (forced constant identically zero). Invalidates that file's "20 of 40"
   headline and the note claiming "the endgame equation alone kills none of
   them" among those 20 (7 of them it does kill). True count 13/40.
2. **`jc2_target_72_108.py`** (predates the fix): reports `k=1,D=3` as
   "ESCAPE OPEN," concludes "11 remain open." Superseded by
   `jc2_phase4_direct.py` (later, same repo) which gets 10. Never corrected.
3. **`session20_report.md`** repeats both stale counts three times (§2: "20
   of 40"; §3 table and prose: "11 of the twelve... survive"; §5 Scorecard:
   "Eleven of the twelve... survive"). All three should read 13/40 and 10/12
   respectively, per `jc2_phase4_direct.py`'s own later, correct analysis.
4. **Claim 6 / `G=b·k`** is not a general relation; it's presented as one.
   Invalidates the implicit claim that the (72,108) 12-point lattice is *the*
   admissible lattice at that degree pair, rather than one untested slice of
   a larger, unexamined space (at least 8 admissible `rho` values found for
   the same cusp type, each giving a different lattice).
5. **Robustness gaps** (not live bugs): the shared escape-solving logic does
   not validate `D>=1` or `m>=1`, silently processing excluded inputs.

None of these bugs touch the *arithmetic* of the ten `R(v)` in
`jc2_phase4_direct.py`, which I independently reproduced exactly.

---

## Blunt final verdict

**Trust the ten `R(v)` formulas in `jc2_phase4_direct.py` — the arithmetic is
right, independently reproduced twice over by different methods including a
sympy-free spot check.** Do **not** trust the framing that they constitute
*the* target at (72,108): they are the open points of one specific,
historically-inherited `(rho=3, m=1)` construction slice, not a
demonstrated-exhaustive search of the admissible lattice, and the one piece
of machinery (`n=b·k+H`) offered as justification for treating that slice as
canonical does not actually generalize past the single data point it was
built from. Before spending real effort realizing any of these ten `R`'s by
an actual chain/ladder/pin tower, the more urgent open question is whether
*other* `rho` (or `m`) give a more promising — or a more clearly empty —
lattice; nothing in this repository currently answers that. And in the
meantime, `session20_report.md` and `jc2_target_72_108.py` should not be
quoted for "how many chain degrees are open" without the correction in this
document — they currently say 11 and 20 respectively, where the
independently-verified numbers are 10 and 13.
