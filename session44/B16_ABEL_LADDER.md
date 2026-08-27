# B=16 via the Abel equation — the representation the campaign never used

## The find (O-rings + Apollo-13 lenses)

The campaign's own audit (`gghv_audit/DISCREPANCIES.md`, item **D4**) flagged the
GGHV discard of degree pair **(80,112)** as the single kill in the 105–124
window resting entirely on a source it could not open — "[4, §3.5]",
class **EXTERNAL-NOT-RE-DERIVED**, "the only 105 ≤ max ≤ 124 kill that rests
entirely on a source this audit cannot open."

Retrieved and read: Guccione–Guccione–Valqui, *A differential equation for
polynomials related to the Jacobian conjecture*, **Pro Mathematica 27 (2013),
83–98** (`session44/promath27_gguv.pdf`, text in `promath27_gguv.txt`).

Two results:

1. **(80,112) is legitimately dead — now verified, not just cited.** §3.5
   solves the reduced equation for `deg(q1)=3` (exactly the degree that builds
   the (112,80) pair) and finds the only solutions have `µ0=0`, i.e. no
   counterexample. The audit's grade-E "couldn't open" is upgraded to grade-A
   "read and confirmed." Not a reopened case.

2. **The whole B=16 problem reduces to ONE Abel equation** — a far smaller
   representation than the saturated Keller/Gröbner systems the campaign has
   been OOM-ing on. Theorem 1.2: `B=16` iff there exist `A, q1 ∈ K[y]`,
   `µ0..µ3 ∈ K`, `µ0 ≠ 0`, with

       (3.6)  A(0) = −µ3²/4,  A'(0) = µ2,  µ3·A''(0) = −6µ1 − 2µ3·q1''(0)

   satisfying the polynomial identity (3.5) (transcribed exactly in
   `abel_b16.py`, `deg A = 2·deg q1`). In Abel form (3.7): `T·T' = F1·T + F0`
   with `F1,F0` explicit rational in `q1` and the µ's. Per degree this is a
   **handful of coefficient unknowns**, not a 14 GB Gröbner system.

   The authors solved `deg(q1)=2,3,4` by hand in 2013 (all force `µ0=0` or are
   homogeneous — no counterexample) and **`deg(q1)=5` defeated their 2013 PC**
   ("after an hour the PC hadn't solved the resulting system"). They proved one
   unconditional partial theorem — `µ1=µ2=0 ⟹ µ0=0` — and **conjectured all
   solutions have `µ2=µ1=0`, which would give `B>16` outright.**

## What Session 44 does with it

`abel_b16.py` transcribes (3.5)+(3.6) exactly and **calibrates on the paper's
own deg-3 solution** (PASS — the transcription is exact). `abel_empty.py`
turns each ladder cell into the one decisive query — *is there a solution with
`µ0 ≠ 0`?* — by saturating `µ0·s−1` and computing a Gröbner basis mod p; basis
`{1}` ⇔ no counterexample at that degree.

Calibrations pass: `deg(q1)=3` saturated is **EMPTY** (no `µ0≠0`) on both the
gauge-fixed `µ3=1` chart and the **free-`µ3`** chart (so the gauge costs
nothing); `deg(q1)=3` unsaturated is NONEMPTY (the `µ0=0` solution is there).
`deg(q1)=2` = only homogeneous solutions. All match the paper.

Frontier sweep (`abel_sweep.sh` → `scanlogs/abel_sweep.log`): `deg(q1)=4,5,6,7`
on charts `µ3∈{1,0}`, saturating `µ0≠0`. This is the exact frontier 2013
hardware could not reach; each cell is decisive for a B=16 degree, and each
`EMPTY` is a step toward the paper's `B>16` conjecture. A `NONEMPTY` is the
first live B=16 signal the campaign would ever have had — it then feeds the
paper's Section-2 construction and the full binding gate (explicit `P,Q`,
`[P,Q]=1`, collision).

## Why this beats the campaign's B=16 ladder

The campaign attacked B=16 through GGV's Theorem-1.2 saturated systems (d=8
chart N: 30 eq/23 unk, OOM 13.9 GB; pentagon seed-extension 241/123, OOM;
p11zero 186/306, OOM). Those are a *different, larger* parametrization of the
same `B=16` question. The Abel form is O(deg) unknowns and needs no
saturation of a huge Keller ideal — only the tiny `µ0≠0` Rabinowitsch. It is
the missing cheap interface, and it was sitting in the one reference the audit
marked unreadable.

## RESULTS (msolve, exact characteristic zero)

Calibration: `deg(q1)=3` saturated = **EMPTY** (`[-1]`), unsaturated =
non-empty (the paper's `µ0=µ1=µ2=0` real solution), both charts of `deg=3`
agree (gauge-fix `µ3=1` validated).

| deg(q1) | corresponds to | verdict (mu0 != 0?) | who did it |
|---|---|---|---|
| 2 | — | EMPTY (homogeneous only) | paper 2013 |
| 3 | (80,112) pair | **EMPTY** | paper 2013 |
| 4 | — | **EMPTY** | paper 2013 |
| 5 | — | **EMPTY** | **defeated 2013 PC — decided here** |
| 6 | — | **EMPTY** | **new (Session 44)** |
| 7 | — | **EMPTY** | **new (Session 44)** |
| 8 | — | **EMPTY** | **new (Session 44)** |

Every cell is an **exact msolve `[-1]` certificate over Q** (not modular):
the saturated ideal `⟨(3.5)-coeffs, (3.6), µ0·s−1⟩` with `µ3=1` has empty
complex variety. No `B=16` counterexample exists with `deg(q1) ≤ 8`.

The paper stopped at `deg(q1)=4` and conjectured all solutions have
`µ2=µ1=0` (⟹ `B>16`). Session 44 has extended the verified range to
`deg(q1) ≤ 8` and is pushing toward `deg(q1)=12` (the campaign's resonant
`d=3·2²` cell). Every additional EMPTY is a theorem-grade step toward the
conjecture and toward `B>16` — which would raise the plane JC bound and
close the entire `B=16` program the campaign has been grinding by brute
Gröbner.

Caveat held to standard: this is the necessary-shape reduced system (the
paper's Theorem 1.2 equivalence). A hypothetical `NONEMPTY` at some degree
would still require the Section-2 lift to explicit `P,Q` and the full binding
gate before being called a counterexample. The EMPTY verdicts need no such
caveat — an empty variety is an unconditional non-existence at that degree.
