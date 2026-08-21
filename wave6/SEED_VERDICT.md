# The admissible seed does NOT extend, at p = 1000003

The campaign's most promising open lead — *does the single admissible
bottom-edge seed extend to a full solution of pentagon case (1)?* — has a
verdict at one prime. Two Gröbner runs previously failed to produce one (a
90-minute timeout and an OOM, both NO VERDICT).

## Route: sieve, then solve

Direct Gröbner never reached the seed-pinned system at **148 variables**. The
forced chain (exact implications, mod p) reduces it to **91 variables / 208
equations**, and msolve then returns

    [-1]        i.e. EMPTY

in seconds — both with the saturation `zz9 * s_4_8 - 1` enforcing `s_4_8 ≠ 0`,
and with it removed.

**Sound direction.** Every chain step is an implication: a solution of the
original system (with the nondegeneracy used in the division steps) maps to a
solution of the reduced one. So *reduced EMPTY ⟹ the original has no such
solution.* The divisions used only `s_4_8`, so the conclusion is precisely:

>  **At p = 1000003 the seed-pinned pentagon system has NO solution with
>  s_4_8 ≠ 0.** The admissible seed does not extend at this prime.

By the Galois argument already on record — the five admissible seeds form one
orbit (`ORBIT_VERDICT.md`) and "extends" is Galois-invariant — this decides all
five, not one.

## Why the verdict is believed this time

An identical-looking `[-1]` was **retracted an hour earlier**
(`RETRACTION_msolve.md`) because the exported file used 9 variables it never
declared. So this one was not accepted until:

1. **Symbol guard.** `write_ms` now refuses to emit a file whose equations use
   an undeclared variable. `reduced_91v.ms` verified: 92 declared, 92 used, 0
   undeclared.
2. **End-to-end pipeline control.** The *whole* pipeline — forced chain, export,
   saturation, msolve — was run on the **bottom edge at p = 999979, a system
   whose answer is known**. It reduced 18 variables to 6 and msolve returned
   `[0, …]` with a **degree-9 eliminant** — reproducing exactly the degree-9
   eliminant the campaign found independently. The chain preserves the solution
   set, and the solver finds solutions when they exist.
3. **Independent row-space check.** The constant is not in the row space of the
   reduced system, so the emptiness is *not* linear — it is a genuine Gröbner
   consequence, not an arithmetic accident.
4. The result is what theory predicts: the system is overdetermined by ~117, so
   emptiness is the overwhelmingly expected outcome. A solution would have been
   the surprise.

## What is NOT established

- **This is one prime.** This campaign proved *this morning* that modular
  emptiness is unsound for contradictions. A second prime is required, and then
  characteristic-zero confirmation, before case (1) may be called closed.
- Generating the seed-pinned system at a second prime needs the seed at that
  prime; the machinery exists (the bottom edge was censused at 13 primes) but
  was not run here.
- The desaturated copy is also empty, but that does **not** upgrade the claim to
  "no solutions at all": the chain's division steps already assumed
  `s_4_8 ≠ 0`, so both verdicts speak only about admissible solutions.

## Status

Pentagon case (1)'s most promising lead is **dead at p = 1000003**, pending a
second prime and a char-0 lift. This does not close case (1) — it closes the
seed route into it, which is what three sessions of compute were spent on.
