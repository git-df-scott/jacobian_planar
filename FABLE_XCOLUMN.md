# The x-column descent: an independent third grading, and what it establishes

Fable, 2026-08-22. Code: `xcol.py`, `xdesc.py`, `d19audit.py`, `gates.py`,
`cascade2.py`, `a7check.py` (repo root, `fable_xcol/`). Everything below is
built **from the two Newton polygons alone** — no campaign code, no
`z = s - tau`, no eighth-power ansatz, no `pentev`/`wcascade` lineage. That
independence is the point: it is the first instrument that can check the
descent without inheriting its assumptions.

## The construction

Write `P = sum_{i=0}^{8} a_i(y) x^i`, `Q = sum_{k=0}^{12} b_k(y) x^k`. Then
`{P,Q} = x^2` splits by **x-column**:

    rung d :  sum_{i+k=d+1} [ i a_i b_k' - k a_i' b_k ] = delta_{d,2}

with `a_i, b_k` supported in the y-ranges cut out of `N(P)`, `N(Q)` by the
vertical line at that x-exponent. This is a *third* grading, transverse to
both the w-cascade and the v-cascade (which OPUS43-028/ERRATA A21 showed are
the same system twice).

## RESULT A — independent reconstruction: 302 equations, 186 unknowns

Convex hulls alone give column bounds `val(a_i) = 2(i-1)` (`i>=1`),
`deg(a_i) = 8+i`; `val(b_k) = 2k-3` (`k>=2`), `deg(b_k) = 12+k`. Counting:

    P columns: 60 coefficients      Q columns: 124 coefficients
    total 184, plus the two additive normalisations p_0_0, q_0_0  =  186
    equations, by x-column d = 19..0:  4,7,8,9,10,11,12,13,14,15,16,17,18,
                                        19,20,21,22,23,22,21   TOTAL = 302

**302 / 186 reproduced exactly**, from the polygons only. The campaign's
system size is independently confirmed. (`xcol.py`.)

## RESULT B — the pure-condition block here is 148 equations

New unknowns enter at rung `d` as `a_{d-11}` and `b_{d-7}`. **All 184
coefficients have entered by rung `d = 7`**, and rungs `d = 6, 5, 4, 3, 2, 1,
0` introduce none: they are

    148 pure conditions on at most 30 surviving parameters
    (184 unknowns - 154 equations used by rungs 19..7 = 30, before gauge)

This is the same phenomenon as OPUS43-029's "levels 7 down to -2 are pure
conditions", found independently and in a different grading — but here the
pure block is **148 equations, not 59**. Two different gradings give two
different (both valid) presentations of the same overdetermination; the
x-column one is far more overdetermined and is therefore the better place to
look for a contradiction.

## RESULT C — rung 19 is exactly solvable, and rigorously has no deleted stratum

Rung 19 receives only `(i,k) = (8,12)`, so it is the **exact global** identity

    8 a_8 b_12' - 12 a_8' b_12 = 0     (not an edge truncation)

Hence `b_12^2 = c a_8^3` as polynomials. With the polygon's
`val a_8 = 14, deg a_8 = 16, val b_12 = 21, deg b_12 = 24` this forces

    **W := y^7 (y - r),   a_8 = alpha W^2,   b_12 = beta W^3**

a 3-parameter family `(alpha, beta, r)` — and 7 coefficients minus 4 equations
= 3 confirms it is the *general* solution, not a branch. A full component
audit (`d19audit.py`) finds exactly two components: this one, and `b_12 = 0`
(which violates the vertex `q_24_12 != 0`). Every degenerate stratum
(`a8_16 = 0`, `b12_24 = 0`, `a8_14 = 0`) collapses onto vertex violations.
**Rung 19 is closed, with nothing deleted.**

Corollary (already reported as Verified Result 2): `q_21_12 = -beta r^3` and
`p_14_8 = alpha r^2`, so given the vertices `p_16_8, q_24_12 != 0`,

    **q_21_12 != 0  <=>  p_14_8 != 0  <=>  r != 0**

i.e. OPUS43-029's "one vertex that is not automatic" **is** automatic.

## RESULT D — a clean-denominator certificate for the top of the descent

Running the descent rungs 19 -> 15 and logging every parameter that ever
appears in a denominator, the **entire ledger is `{alpha, beta, r}`** — and
all three are forced-nonzero vertex quantities. So on rungs 19..15 there is
**no deleted vanishing locus**: the systemic bug identified in
`FABLE_SWEEP_REPORT.md` (B1) does **not** occur at the top of this grading.
This is the first positive no-bug certificate anyone has produced for any part
of the descent, and it is exactly the audit the campaign's own descent failed
(it divided by `g9_8` at level 8 and `g9_11` at level 13).

## RESULT E — the gates, and an independent confirmation of the rung-17 condition

Gates are computed canonically (left nullspace of the rung's coefficient
matrix, so the gate ideal does not depend on solve order), then stripped of
forced-nonzero factors:

    d = 18 : no gate                       (rung closes freely)
    d = 17 : ONE gate, a perfect square -> forced, no branch
             (b_11 / y^19)'(r) = 0
    d = 16 : no gate
    d = 15 : ONE gate, perfect square    -> forced, no branch
             3 beta (b10_18 + 2 b10_19 r + 3 b10_20 r^2 + 4 b10_21 r^3
                     + 5 b10_22 r^4)
             = b11_21^2 + 6 b11_21 b11_22 r + 12 b11_21 b11_23 r^2
               + 9 b11_22^2 r^2 + 36 b11_22 b11_23 r^3 + 36 b11_23^2 r^4

**Conditions sit at odd rungs, none at even** — 17 and 15 carry one each, 18
and 16 carry none. That is the same parity pattern OPUS43-014 found on the
lower edge (conditions at 19, 17, 15, 13; nothing at 18, 16, 14, 12), obtained
here by an unrelated route.

And the identification is exact. After rung 18 is solved,

    a_7(r) = (2 alpha r^12 / (3 beta)) * G,        G := (b_11/y^19)'(r)

so with `alpha, beta, r != 0`, **G = 0 <=> a_7(r) = 0** — precisely the
campaign's rung-17 condition `A_7(r) = 0`. Two instruments with no shared
code, no shared grading and no shared coordinates agree on the condition.
Bonus: `b_11(r) = 0` holds *identically* once rung 18 is solved.
(`a7check.py`.)

## RESULT F — the endgame carries no grading (angle 8, closed)

Scan of the 59-condition / 19-parameter endgame (`endgame.pkl`) for a torus
grading: **rank 0**. No weight vector makes it quasi-homogeneous, so the
variety is not a cone, the origin is not a solution (3 conditions are nonzero
there), and no weight-based decomposition is available. Angle 8 is closed
negative — cheap, and it removes a hypothesis from the board.

## What this does NOT establish

No counterexample, and no emptiness. The pentagon stays **NO VERDICT**. The
descent in this grading is running below rung 15; every gate so far has been
a perfect power (forced, unbranched), so no branch choice has yet been spent
and no generality has been lost — but that is a statement about rungs 19..15,
not about the pentagon.

## Why this grading is the right place to continue

1. It is assumption-free: polygons only. It cannot inherit a deleted stratum
   from the `z = s - tau` descent, so it is the natural instrument for
   discharging the `g8_6 = g8_7 = 0` inheritance that all six EMPTY verdicts
   rest on.
2. Its pure-condition block is 148 equations on <= 30 parameters, versus 59 on
   19 — far more overdetermined, so a contradiction (if the pentagon is empty)
   should surface earlier and more cheaply here.
3. Every gate so far is a perfect power, i.e. unconditional. If that persists,
   the descent has **no branch points at all** in this grading, and the whole
   pentagon reduces to one chain of forced substitutions — which is either a
   single explicit `(P,Q)` or a single explicit contradiction.
