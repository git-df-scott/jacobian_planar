# Operation 108 — the literature's last open case below 125

## What the literature says (verified from the papers this session)

GGHV, arXiv:2204.14178 (2022), Theorem 2.1: a counterexample has
max(deg) >= 125 OR (deg P, deg Q) = (72,108)/(108,72). Their frontier
below 125 was {(56,84), (66,99), (72,108) x2, (80,120)}; they discarded
everything except ONE of the two (72,108) cases, and say verbatim: "we
couldn't solve the corresponding system of polynomial equations, thus it
is left open" and "With enough computing power we would be able to raise
it up from 108 to 125, since there is only one case left."

Their instrument: approximate roots. P = C^2, Q = C^3 + lambda C^-1 + F;
polynomiality of D_k := C_k C_3^(5-2k) turns the tail conditions
P_{-k} = 0 (k=1..8), Q_{-k} = 0 (k=1..5) into a polynomial system in the
d-coefficients, which their CAS (Mathematica-style elimination) could not
finish for the surviving case. That was 2022; solvers and our machinery
have moved.

Xu (arXiv:1604.07683v3, Feb 2022) independently "suggests case (99,66)
is open" (an unknown split in his framework) — GGHV-2022 discards
(66,99) by their system route, so the Xu doubt is answered *by them*;
reproducing their (66,99) kill with our tools is the natural control for
anything we claim about (72,108).

## What this campaign has (and the gap found today)

The two (72,108) cases ARE our hand-entered trackB1 shapes:
  (8,28) case (1) pentagons      params=61 conds=110 rank=60 dim<=1
  (8,28) case (2) quadrilaterals params=25 conds=188 rank=24 dim<=1
Never queued into any verdict ledger until tonight (they lived as
pipeline regression fixtures). Both are SMALL. Two-prime Gröbner is
running now (state_108.json, budget 3600s/prime).

## Protocol

1. RUNNING: two-prime mod-p Gröbner on both reduced chart systems.
   EMPTY at 2 primes on the surviving case = strong mod-p signal for
   "max >= 125"; NONEMPTY = witness replay, then exact lift attempt.
   Caveat stated up front: the chart system is the local Newton-polygon
   model; a mod-p chart EMPTY is not yet a char-0 discard of the case.
2. Derive (not transcribe) the GGHV D_k system in sympy with the paper's
   printed formulas as controls (f_system.py discipline), for BOTH
   (72,108) cases and for (66,99).
3. Control: reproduce their published (66,99) kill with our derivation +
   msolve. Only then run the open (72,108) system: mod-p two-prime
   first, then char-0; delegate char-0 to sol if it resists this box.
4. Any survivor: full reverse-lift protocol (exact, char-0, collision
   exhibited) before any claim. A reduced/modular survivor is never a CE.

## Stakes

EMPTY (char-0, both routes): max(deg) >= 125 — a new theorem-grade bound
(would need writing up properly with GGHV's Thm 2.1).
NONEMPTY: the only literature-sanctioned CE door below 125 is open and
we hold explicit coefficient data for it.
