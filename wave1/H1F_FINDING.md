# H1f — the exact-ℚ blocker is NOT gone. AUDIT_REPORT §2 misreads its own artifact.

## The claim on record

`AUDIT_REPORT.md` §2, dated 2026-08-14, under "Exact-Q certificate status":

> "The char-0 edge eliminant — the single computation everything stalled on —
> **completed via msolve**: `trackB_edgeQ.msolve.out`, 796KB, **elimination
> polynomial degree 1144**, matching the independently certified vdim. **That is
> the unblock**; the remaining Q work is factor-over-Q then per-factor branch
> closure (Decision 4), which is window-sized and mirrors the proven mod-p
> pattern."

Plan 43 inherits this: H1f begins "Per-irreducible-factor RUR-consistency of the
deg-1144 eliminant".

## What the file actually contains

Parsed with PARI/GP (the file is a nested msolve vector; GP evaluates it
natively, Python cannot — the coefficients are written `<bignum>/2^k`):

```
V             = [0, [1, A]]        dim 0
A = V[2][2]   = 28 entries
each entry    = 7 coordinates
each coordinate = a 2-element vector  [lower, upper]
                  with dyadic endpoints, denominators 2^127 / 2^128
max nested vector length anywhere in the file = 2
```

**There is no degree-1144 coefficient list in the file. There is no elimination
polynomial in the file at all.**

What it holds is msolve's **real-solution output**: 28 real solution boxes for
the case-(2) edge system, each box giving 7 coordinate intervals — 7 being
exactly `|EDGE_VARS| = {d_3_3, d_4_5, d_5_7, d_6_9, d_7_11, d_8_13, d_9_15}`.
796 KB is the size of 196 thousand-bit interval endpoints, not of a polynomial.

## What survives, and what does not

**Survives — the number 1144.** It is independently corroborated: I recomputed
`vdim = 1144` today in Singular on the pinned edge chart, and msolve 0.10.1
returned 1144 solutions on the same system, at three primes each (`MANIFEST.md`
§G.1–G.2). The edge variety really does have 1144 points. That was never in
doubt and is not affected.

**Does not survive — "that is the unblock".** The elimination polynomial was
never produced. The exact-ℚ route is still blocked at exactly the point
AUDIT_REPORT declares it cleared, and has been believed cleared since
2026-08-14. Every downstream plan step that starts "factor the degree-1144
eliminant over ℚ" — Decision 4, and Plan 43's H1f as written — **has no input.**

## Why the misread is easy to make

msolve is invoked the same way for both jobs; the mode is set by flags, not by
the output filename. A 796 KB file of long integers looks like a big polynomial
if it is not parsed. Nothing in the filename `trackB_edgeQ.msolve.out`
distinguishes "eliminant" from "real solutions", and the run log records only
completion. The campaign's own silent-lie table exists for exactly this class of
failure — a tool returning a plausible wrong-shaped answer — and this is a new
entry for it: **msolve's solve mode and its eliminant mode write
indistinguishable-looking output.**

## Incidental, and NOT to be over-read

The 28 boxes are **real** solutions of the edge system. Plan 43 §H1f says
explicitly: *"Strike 'real solutions' — realness is irrelevant."* JC2 is a
question over ℂ; a real point on the edge variety is neither necessary nor
sufficient for anything downstream. These are recorded as a byproduct, not as
progress.

## Status of H1f after this

| item | status |
|---|---|
| RUR-per-irreducible-factor of the deg-1144 eliminant | **BLOCKED — the eliminant does not exist.** Must be computed before H1f can begin |
| Route-2 prime hygiene at p ≡ 1 (mod 3) | UNCHECKED |
| Route-1 / Route-2 provenance-disjointness | UNCHECKED |
| gauge-quotient integrity on the CASE2 dim-2 survivor | UNCHECKED |

The first line is the whole point: H1f was not a computation waiting to be run,
it was a computation waiting for an input that was never produced.

## Correction to AUDIT_REPORT.md

§2's "0 charts CLOSED. The route was rebuilt twice and **the blocker is now
gone**" should read: the blocker is **not** gone. Nothing about the mod-p
verdicts changes — those are independent and are separately controlled (A6).
