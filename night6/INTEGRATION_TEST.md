# night6 — integration test for the E3 kernel (runbook step 3)

**Modular.** Everything below is computed at `p = 999983` and `p = 1000003`.
No characteristic-zero claim is made.

Instruments: `night6/integrate.py` (system builder), `night6/task1_run.py`
(main run), `night6/task1_controls.py` (controls). Singular 4.x is the
Groebner engine; the identities, the face solutions, the kernel and every
substitution check are built and run in Python from scratch. Raw logs:
`night6/INTEGRATION_TEST_run.log`, `night6/INTEGRATION_TEST_controls.log`.
Machine-readable: `night6/task1_p999983.json`, `night6/task1_p1000003.json`,
`night6/task1_controls.json`.

---

## 1. What was computed

At each face solution `(q,t)` the E3 kernel is 2-dimensional (night6/E3_KERNEL.md),
spanned by `(p1,s1)` and `(p2,s2)`. Set

        (p_, s_) = alpha*(p1,s1) + beta*(p2,s2)

and substitute into the full five identities of the handoff:

        E0:  f'r - p_ g'                           = 0      (z^0)
        E1:  2f's_ + p_'r - p_ r' - 2q g'          = 0      (z^1)
        E2:  3f't + 2p_'s_ + q'r - p_ s_' - 2q r'  = 0      (z^2)
        E3:  3p_'t + 2q's_ - p_ t' - 2q s_'        = 0      (z^3)
        E4:  3q't - 2q t'                          = -u^2   (z^4)

Unknowns: `f` on `u^0..u^8`, `g` on `u^0..u^12`, `r` on `u^1..u^12`, plus
`alpha, beta`. `f_0` and `g_0` never occur (only `f'`, `g'` appear), so the
live unknowns are `f_1..f_8`, `g_1..g_12`, `r_1..r_12`, `alpha`, `beta`.

**E4 and E3 as required.** E4 was verified exactly at every face solution
(residual of `3q't - 2qt' + u^2` identically zero in its residue field). E3
was verified to vanish **identically in the unknowns** — i.e. symbolically in
`alpha` and `beta`, not just at a point: the builder's E3 u-polynomial comes
out with no terms at all, at every face solution, in every chart. That is the
kernel property, re-derived inside the integration system.

Row counts, identical in every run: E0 gives 19 rows (`u^1..u^19`), E1 gives
19, E2 gives 19 — **57 equations**.

### The projective reduction

The system is weighted-homogeneous: with weight 1 on `(alpha,beta)`, weight 2
on `f` and on `r`, and weight 3 on `g`, each of E0, E1, E2 is homogeneous.
So "`(alpha,beta) != (0,0)`" is a projective question, settled by two charts:

        chart A :  alpha = 1, beta a free unknown     (33 unknowns)
        chart B :  alpha = 0, beta = 1                (32 unknowns)

Every `(alpha,beta) != (0,0)` is carried into exactly one of these by the
scaling. If both charts are empty, `(alpha,beta) = (0,0)` is forced.

Two variants per chart, as instructed:

        (a) free
        (b) vertex non-degeneracy imposed by Rabinowitsch inverses:
            f_8*Wf = 1  and  g_12*Wg = 1
            (f_8 is the vertex (8,16) of N(P), g_12 the vertex (12,24) of N(Q))

---

## 2. Coverage

Not only the F_p-rational face solutions: each irreducible factor `h` of the
degree-35 eliminant was handled in its residue field `F_p[T]/(h)` (Singular
`minpoly`), so **all 35 face solutions are covered at both primes**.

| prime | residue-field degrees | families | face solutions covered |
|---|---|---|---|
| 999983  | 1, 1, 3, 6, 6, 6, 6, 6    | 8 | 35 of 35 |
| 1000003 | 1, 2, 2, 3, 3, 6, 6, 6, 6 | 9 | 35 of 35 |

---

## 3. Result

**Every one of the 68 runs (17 face families x 2 charts x 2 variants, across
both primes) returned the unit ideal.** `|GB| = 1` with `G[1] = 1`,
`dim = -1`, in every case; no run returned a non-unit ideal.

        unit ideal = True   : 68 / 68
        unit ideal = False  :  0 / 68

Stated as a measurement: at every one of the 35 face solutions, at both
primes, in both charts and both variants, the identities E0, E1, E2 have **no
common zero** once `(alpha,beta)` is scaled to be nonzero. Equivalently

        (alpha, beta) = (0, 0) is forced,  hence  p_ = 0 and s_ = 0.

This **reproduces the session-44 recorded mod-p verdict** that `p` is forced
to `0` on this branch (handoff section 3a). Nothing here disagrees with it.
No flag is raised.

By the handoff's own section 3d, `p = s = 0` then makes `f` and `g` constant
by hand — but that step is not part of this measurement and is not claimed
here; what is measured is only that both charts are empty, at both primes.

---

## 4. Controls

An empty answer is worthless without evidence the instrument can produce a
non-empty one. Three controls, all run at both primes and (C2, C3) at all 17
face families:

**C1 — identity control.** The five coded expressions E0..E4 were compared,
at 4 random numeric choices of `f, p, q, g, r, s, t` over F_p with the
handoff's supports, against the `z^k` coefficients of the bracket
`[P,Q]_{u,z} = P_u Q_z - P_z Q_u` computed directly from
`P = f + p z + q z^2`, `Q = g + r z + s z^2 + t z^3`.
**Agreement at every seed, both primes.** This validates the signs and
coefficients of the identities as coded, independently of the handoff text.

**C2 — positive control.** The same builder with `(p_,s_) = (0,0)` — the
branch the handoff's section 3d treats by hand. At all 17 face families, both
primes:

        unit ideal = False,  dim = 0,  |GB| = 33

and the known point `f_1..f_8 = g_1..g_12 = r_1..r_12 = 0` (i.e. `f` and `g`
constant, `r = 0`) was **substituted back and verified exactly**: all 57
equations vanish. So the instrument does find solutions when they are there,
and the section 3d branch is exactly where they are.

**C3 — control with a known answer, known for a reason.** The same
`(p_,s_) = (0,0)` branch with the vertex non-degeneracy `f_8 != 0`,
`g_12 != 0` imposed. At all 17 face families, both primes: **unit ideal**,
`dim = -1`. That is precisely what the handoff's hand argument predicts
(`p = s = 0` forces `f`, `g` constant, so `f_8 = 0`), reproduced by the
machine. C2 and C3 together show the Rabinowitsch conditions are live — they
turn a non-empty branch into an empty one — so the empty answers in section 3
are not an artefact of the non-degeneracy encoding.

Control summary (both primes, all 17 families):

| control | result |
|---|---|
| C1 coded identities vs direct (u,z) bracket | agree, 4 seeds x 2 primes |
| C2 `(p_,s_)=(0,0)`, free | NOT unit, dim 0, known point verified exactly, 17/17 x 2 primes |
| C3 `(p_,s_)=(0,0)`, vertices non-degenerate | unit ideal, 17/17 x 2 primes |

---

## 5. Cross-prime consistency

| | p = 999983 | p = 1000003 | agree |
|---|---|---|---|
| face system dim / vdim | 0 / 35 | 0 / 35 | yes |
| face solutions covered | 35 of 35 | 35 of 35 | yes |
| E3 identically zero in the unknowns | all runs | all runs | yes |
| E4 verified exactly | all families | all families | yes |
| chart A free — unit ideal | all families | all families | yes |
| chart A Rabinowitsch — unit ideal | all families | all families | yes |
| chart B free — unit ideal | all families | all families | yes |
| chart B Rabinowitsch — unit ideal | all families | all families | yes |
| C2 non-unit, dim 0 | all families | all families | yes |
| C3 unit ideal | all families | all families | yes |

No disagreement between the primes on any quantity measured.

---

## 6. Scope

Modular only, two primes, agreeing. The runbook
(`night6/RUNBOOK_KERNEL_NONZERO.md`) step 3 says: "No full solution => the
direction does not integrate; record, done." That is where this stops. Steps
4-6 of the runbook (lifting, reversing the reduction, detectors) are not
reached and were not run.
