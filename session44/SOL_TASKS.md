# Tasks for Sol (bigger-box compute; artifacts on branch claude/past-code-session-8mdjqn)

Context: Session 44 rebuilt the B=16 program on the F-system — the Pro
Mathematica 27 (2013) reduced system re-derived mechanically from the four
bracket equations, all controls passing (`session44/f_system.py`; see
`session44/B16_ABEL_LADDER.md` for the story). One decisive computation
exceeds our 15 GB box and is compute-walled, not math-walled.

## T1 — THE PRIORITY: decide µ1-rigidity at deg(q1)=8 (the "crack test")

Files: `session44/lead4/j7mu1_char0.ms`, `j7mu1_p65521.ms`, `j7mu1_p65539.ms`
(msolve input format; line 2 is the field characteristic).
36 equations / 27 unknowns; saturated with `mu1*s_sat − 1`.

Question: is the variety EMPTY (msolve prints `[-1]:`)?
- EMPTY at char 0 (or at both primes) ⟹ µ1-rigidity HOLDS at deg 8 ⟹ the
  earlier Abel-form NONEMPTY was a transcription artifact, and the paper's
  B>16 conjecture pattern extends.
- NONEMPTY ⟹ the 2013 conjecture is FALSE at deg 8 — extract a witness point
  (msolve default mode prints solutions if dim 0; `-P 2` for parametrization)
  and return it; we will replay it exactly and chase the mechanism.

Status on our box: defeated msolve char-0 (OOM), msolve mod-p solving (900 s),
msolve mod-p GB-only (2400 s), Singular mod-p (in flight). Needs RAM (or
magma). Run: `msolve -f j7mu1_char0.ms` (and the two mod-p files).

## T1b — the µ3=0 companion of the crack test  (ADDENDUM, run right after T1)

T1's three `.ms` files were generated in the gauge **µ3=1**.  The scaling
`(x,y) -> (λ^a x, λ^b y)` rescales µ3 by `λ^(a+b)`, so the gauge covers
every µ3 ≠ 0 — but the **µ3=0 stratum is fixed by the action and is a
separate branch that T1 cannot see.**  The companion systems with µ3 = 0
substituted exactly are committed alongside T1's:

    session44/lead4/j7mu1_mu3zero_char0.ms
    session44/lead4/j7mu1_mu3zero_p65521.ms
    session44/lead4/j7mu1_mu3zero_p65539.ms

Same question, same verdict standards as T1 (both primes must agree;
NONEMPTY needs witness replay into the F-system; char-0 confirmation
before any claim).  These systems are smaller than T1's (µ3=0 kills
terms), so try them FIRST if T1 stalls — a NONEMPTY here is just as much
of a crack as one in T1.

## T2 — extend the µ1-rigidity ladder: deg(q1) = 5, 6, 7

Same construction at j=4,5,6. Generate inputs with:
`python3 session44/f_system.py <j> --satvar mu1 --skipcal` (or ask us to
export .ms files as in T1 — say the word and they'll be on the branch in
minutes). j=4 also OOM'd here; j≤3 are EMPTY (verified grade).

## T3 — the (8,28)/(7/4,3)/(3,4)/max-144 family (the big open object)

The published never-attacked case reduces to charts of dimension 13 and 56
(via `session44/lead4/trackD_chain_map.reduced_candidates` +
`trackB1_shapes.run_pair`). Task: full Gröbner (mod 65521 + 65539) of the
dim-13 chart's system to get its actual components — we will then sample it
against the vertex gates for candidate reduced solutions. We can export
explicit .ms/.sing files on request.

## T4 — the two classic OOM-walled frontier systems (campaign backlog)

- B=16 corrected d=8 chart N: `wave5/ms/m16_d8_*.ms` (30 eq/23 unk) — on
  branch `claude/opus-5-counterexample-plan-sep6yk` (restored bundle).
- Pentagon seed-extension: 241 eq / 123 unk (see session43 ledger).
Both died at ~14 GB here. Any verdict is a first.

## Standards (binding)

EMPTY needs the raw `[-1]`/GB=1 output attached. NONEMPTY needs the witness
returned for exact replay — a modular/numerical point is CANDIDATE-UNVERIFIED
until it lifts and replays; nothing is a counterexample without explicit P,Q,
[P,Q]=1 coefficientwise, and a collision.
