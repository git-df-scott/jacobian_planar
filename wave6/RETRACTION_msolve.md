# RETRACTION, same session: the reduced-system EMPTY verdicts were invalid

## What was claimed, briefly, and is now withdrawn

The forced chain reduced the seed-pinned pentagon system from 148 variables to
~94–100 and msolve returned **`[-1]` (EMPTY)** on both reduced exports in under
a second — against the *original* system, which produced no verdict in 280 s
here and 90 minutes for the campaign. Read naively that said: **the admissible
seed does not extend, mod p.** It says nothing of the kind.

## The bug

The exported header declared **100 variables while the equations used 109**.
Nine variables appeared in the equations without being declared, so msolve was
fed a malformed system.

Root cause, in my own substitution routine:

```
if dict(m).get(v, 0) != 1:
    nt[m] = ... ; continue        # monomial kept UNCHANGED
```

A pivot substitutes `v` only where `v` occurs to degree exactly 1. Monomials
containing `v²` or higher are passed through untouched — so `v` survives in the
system while being recorded in `solved` and removed from the exported variable
list. For the *original* bilinear system every variable has degree ≤ 1, so the
early c-pivots are safe; degree ≥ 2 first appears **after** a substitution puts
a polynomial in `d` next to another `d`, and every later pivot is then exposed.

## Why the fast `[-1]` should have been suspicious immediately

- Sub-second Gröbner on 217 equations in 100 variables is not plausible.
- An independent row-space computation showed **the constant is NOT in the row
  space** of either reduced system, so the emptiness was not linear — it had no
  cheap explanation.
- The control settles it: the same exporter, given a **well-formed** system with
  known solutions (the bottom edge at p = 999979), returns `[0, …]` and finds
  them. The pipeline works; the input did not.

## Fix and status

Pivot eligibility now requires `deg_v ≤ 1` in **every** equation, so an
eliminated variable is genuinely gone. Applied to all four chain scripts
(`w6_forced_chain.py`, `w6_forced_chain2.py`, `w6_chain_modp.py`,
`w6_chain_export.py`), and the reductions are being re-run.

**Consequently these previously reported counts are provisional and expected to
be too optimistic** (they counted not-fully-eliminated variables as eliminated):
`283/165 → 212/95`, the "all 51 c-variables eliminated" claim, and the
seed-pinned `267/148 → 194/77`. The *early* c-pivots are unaffected, so the
qualitative finding stands — the nondegeneracy conditions were being wasted,
`c_1_0 · d_0_1 = 0` with `c_1_0 ≠ 0` really does force `d_0_1 = 0`, and
`c_1_0 = 1` really is exact — but the headline reduction sizes must be re-taken.

## Method note

The Q-side reduction was verified by back-substitution at random points and
**passed** — because that check re-derives eliminated variables from their own
pivot expressions, which is self-consistent even when a variable has not really
been removed. It was blind to this failure mode. The check that caught it was
dumber and better: *count the symbols in the file you are about to hand the
solver.* Verify the artifact, not only the algorithm.
