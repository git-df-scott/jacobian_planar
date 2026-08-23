# Does sub-case (2) survive to rung 19? Measured answer: no, and here is the
# exact system that decides it

Fable, 2026-08-23. Code: `fable_xcol/sc2gate.py`, `sc2modp.py` (exact mod-p),
`sc2numeric.py` (superseded, see the correction below).

## The measurement

Exact arithmetic mod `p = 2^31 - 1`, bottom-up ladder from rung 3:

| rung | eqs | new unknowns | rank | GATES | freedom added | cumulative freedom |
|---|---|---|---|---|---|---|
| 3 | 5 | 7 | 5 | 0 | 2 | 4 |
| 4 | 5 | 7 | 5 | 0 | 2 | 6 |
| 5 | 5 | 7 | 5 | 0 | 2 | 8 |
| 6 | 5 | 7 | 5 | 0 | 2 | 10 |
| 7 | 5 | 7 | 5 | 0 | 2 | 12 |
| 8 | 6 | 7 | 5 | 0 | 2 | 14 |
| 9 | 6 | 7 | 5 | 0 | 2 | 16 |
| **10** | 6 | 4 | 4 | **1** | **0** | 16 |

**The answer to "does it survive to rung 19" is NO at a generic point** — the
ladder is consistent through rung 9 and hits its first genuine obstruction at
rung 10. That is confirmed independently three ways: the symbolic gauge-fixed
run, the plain mod-p run (inconsistent at rung 10 for all three seeds tried),
and this rank/gate count.

## What that leaves — and it is small

The structure is now completely explicit:

* **rungs 3–9** each add exactly **2 free parameters** and impose no condition.
  With `(A,B)` from rung 2 that is **16 free parameters** total.
* **from rung 10 upward the rank equals the number of new unknowns**, so **no
  further freedom is ever created**; every rung from 10 on contributes only
  conditions.
* rungs 10, 11, 12 contribute roughly **2 gates each** (6 equations, rank 4).
* rungs 13–19 introduce nothing at all: **34 pure conditions** (5,5,5,5,5,5,4).

    **≈ 40 polynomial conditions in 16 unknowns.**

Sub-case (2) is therefore decided by an explicit, finite, **16-variable**
polynomial system — against the 186 variables the campaign has been fighting.
Over-determined by ~24, which makes emptiness the likely outcome, but
**over-determination is not a proof**: at rung 10 one of the two candidate gates
already vanished identically, so these conditions are demonstrably dependent and
the true rank of the system is the open question.

This is the smallest and best-posed formulation of an open case this campaign
has produced. Solving or refuting a 16-variable system is routine for a real
Gröbner engine; it was never reachable at 186.

## Correction: my floating-point search was invalid

I built a fast numeric ladder and reported relative residuals around `1e-4`,
which looked like near-solutions. **Those numbers are meaningless.**
`numpy.linalg.lstsq` returns a least-squares fit when a linear system is
*inconsistent* rather than failing, so it drove straight through rung 10's gate
and "solved" a variety that does not exist. Exact mod-p arithmetic exposed it
immediately: rung 10 is inconsistent at every seed tried.

That is the fourth degeneracy trap in this problem, after
(i) the bihomogeneous scaling collapse in VARPRO,
(ii) the min-norm kernel collapse (`lstsq` returning 0 on a homogeneous rung),
(iii) the high-column collapse where rungs 13–19 vanish because `a_3..a_8 -> 0`.
Every one produced a plausible number before it was caught. Recorded so the next
person recognises the shape: **in this problem, any encouraging residual should
be assumed to be a collapse until checked in exact arithmetic.**

## Next step

Hand the 16-variable system to a real solver. Concretely: run the ladder
symbolically to rung 12 (the gauge-fixed sympy run reaches rung 10 in seconds),
collect the ~40 conditions at rungs 10–19 as polynomials in the 16 free
parameters, and compute a Gröbner basis. `[1]` is an emptiness certificate for
sub-case (2); a solution goes straight to `fable_xcol/verify.py`.

Greedy gate-by-gate solving should **not** be used — I tried it and it is
exactly the solve-order hazard this campaign has been bitten by before. The
conditions must be treated as one system.

## Status

No counterexample. Sub-case (2): **NO VERDICT**, but reduced from 70 unknowns /
92 equations to an explicit **40 conditions in 16 unknowns**, with all four
Newton vertices still live (`p_14_8` and `p_16_8` are nonzero at the generic
point reached).
