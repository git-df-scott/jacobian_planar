# Above 125: what is built, what is blocked, and exactly what unblocks it

Date 2026-08-14. Companion to `SESSION_CORRECTIONS.md`.

## The goal

GGHV 2204.14178 leaves a counterexample possible only at max degree >= 125, or
at the pair (72,108)/(108,72). The (72,108) shape is case (8,28), worked in
`SESSION_CORRECTIONS.md`. This file covers >= 125.

## What IS available (verified, `trackE_literature_verified.md` E6)

The companion paper "Some Algorithms Related to the Jacobian Conjecture" (same
four authors), §6, describes the shape of **all 34 possible counterexamples
with max <= 150**, as CHAIN DATA: a sequence A0, A1, ... (corners, first
coordinates often fractional) plus a cusp-type pair (m,n). Degree pairs are
(m(a+b), n(a+b)) for A0 = (a,b). The rows with max >= 125:

- families: F2 (3,5) 125 -> (75,125); F24 (3,4) 128 -> (96,128);
  F11 (2,5) 140 -> (56,140); F9 (3,5) 140 -> (84,140);
  F7 (2,7) 147 -> (42,147); F8 (3,7) 147 -> (63,147)
- length-1 chains: (7,35)/(19/7,5); (8,28)/(7/4,3); (9,36)/(17/9,4);
  (11,33)/(19/4,8); (12,33)/(11/3,8); (7,42)/(13/7,6)
- length-2 chains: (8,40)/(8,28)/(11/4,7); (9,36)/(9,24)/(11/3,8);
  (10,40)/(16/5,6)/(23/10,3); (10,40)/(18/5,8)/(8/5,3);
  (12,30)/(16/3,10)/(11/6,3); (12,36)/(12,33)/(11/3,8);
  (12,36)/(9,24)/(11/3,8); (12,36)/(21/4,9)/(19/4,8);
  (12,36)/(21/4,9)/(12/4,5)
- length-3 chain: (12,36)/(12,30)/(16/3,10)/(11/6,3)

Smallest maxes: 125, 126 (two shapes, (84,126) and (126,84)), 128, 132, 135
(four shapes).

## What IS built: a per-pair verdict machine

`trackB1_polygon.py` + `trackB1_shapes.py`. Given ANY reduced Newton-polygon
pair and bracket right-hand side, it:

1. computes the hull rows from the vertex list;
2. checks applicability — one polygon's j = 0 row must be exactly {(0,0),(1,0)}
   and the other's exactly {(0,0)} — and reports OUT OF SCOPE otherwise rather
   than mis-analysing;
3. orients itself (for (8,28) P drives with [P,Q] = x^2; for (9,27) Q drives, so
   it uses [Q,P] = -x);
4. runs the y-adic recursion, which makes the non-driver a FUNCTION of the
   driver, with no square roots and no denominators beyond p_10;
5. emits the exact condition system and its exact Jacobian rank (dual numbers
   over F_p[eps]/(eps^2) — a finite difference over F_p is a secant, not a
   derivative).

Measured, with only the trivial `p_00` column identically zero in every case:

| shape | params | conditions | exact rank | dim bound |
|---|---|---|---|---|
| (8,28) case (1) | 61 | 110 | 60 | 1 |
| (8,28) case (2) | 25 | 188 | 24 | 1 |
| (9,27) | 172 | 103 | 103 | 69 |

This is Decision 1's regression bar in the only form that is sound without
GGHV §4: the machine does not GUESS polygons, it VERIFIES a given pair.

**Honest read.** These are NECESSARY conditions and their strength varies by
shape: extraordinarily strong on both (8,28) shapes, weak on (9,27). The machine
does NOT reprove GGHV's closure of (9,27) — their §5 argument uses more than the
polygons. So a "dim bound" from this machine is an upper bound on what the
polygons alone can say, not a verdict.

## What is BLOCKED, precisely

The chain data above is NOT the reduced polygon pair. Getting from
(A0, A1, ..., m, n) to N(P), N(Q) and the bracket right-hand side is exactly
GGHV §4's reduction (chain data -> automorphism sequence -> reduced pair), and
it is genuinely per-case: I tried to infer it from the two published reduced
shapes and it does not pattern-match.

- (9,27), a length-2 chain (9,27)/(9,24)/(11/3,8) with (m,n) = (2,3):
  A0 = n*(3,9) and A1 = n*(3,8) exactly, and the reduced polygons are
  N(P) = 2*{(0,0),(3,8),(3,9),(0,9)} + the extra vertex (1,1),
  N(Q) = 3*{(0,0),(3,8),(3,9),(0,9)} + the extra vertex (1,0).
- (8,28), a length-1 chain (8,28)/(11/4,7) with (m,n) = (2,3):
  A0 = (8,28) is NOT n*(lattice point) — 8/3 is not an integer — yet its reduced
  polygons have base pair (4,7),(4,8) with N(P) = 2*base + (1,0) and
  N(Q) = 3*base + (2,1).

Two examples with incompatible relations between A0 and the base pair. Fitting a
rule to them would be hand-guessing with nothing to check it against — the exact
failure mode that produced the three results retracted this session.

## One invariant that IS verified, and is a usable check

Across both published reduced shapes, the extra vertices satisfy

        eps_P + eps_Q = (r + 1, 1)      where [P,Q] = x^r.

- (9,27): (1,1) + (1,0) = (2,1), r = 1.
- (8,28): (1,0) + (2,1) = (3,1), r = 2.

Any candidate reduced pair violating this is wrong. (It is also exactly what the
verdict machine needs: it forces one polygon's j = 0 row to be {(0,0),(1,0)}.)

## What unblocks it

Re-derive GGHV §4's reduction and validate it by reproducing the published
reduced pairs for (9,27), (9,24), (8,28) and (7,21) from their chain data alone,
including the bracket right-hand side. That is Fable-grade mathematics, not a
computation to run longer. Once a pair is derived, the verdict machine returns
its condition count and exact Jacobian rank in seconds, so triage across all 34
shapes is then cheap.

**Status: not started, and deliberately not faked.** No above-125 shape has been
tested, because no above-125 reduced polygon pair is known to me.
