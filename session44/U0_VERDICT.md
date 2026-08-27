# The u=0 chart of the (4,6) collision frontier: DEAD

Chart: sol6 slice `p0 = x^84 - x`, `c=1`, `p_i(0)=0`, with `u = p1[1] = 0` —
the codim-1 stratum where the generic kernel pivot `(n+1)u/4` vanishes and
sol6's three-parameter recurrence changes character.  Session 44 result:
**empty, with exact certificates at every special locus.**

## Structure (all exact)

- Rung 2 collapses to the quartic `C2: 2v^4 + 3v w^2 + 18w = 0`.
- On the curve, kernels t_2..t_21 are consumed linearly (kernel coefficient
  `~ (n+1)(vw+3)`, derived exactly at rung 3: `c1 = (vw+3)/2`).
- First pure conditions at rungs 23+ (numerators N_23..N_26 of degree
  339/359/379/399 over the curve's function field).

## The kill, by stratum

1. **Generic locus (v != 0, vw != -3):** function-field walk over
   `K = F_p(v)[w]/(3vw^2+18w+2v^4)` computes N_23..N_26 completely
   (extension fields included).  `gcd(N_23,...,N_26) = v^54 (p=29),
   v^64 (p=1000003), v^64 (p=999983)` — pure denominator powers, **no common
   zero with v != 0 at three independent primes.**  (Char-0 emptiness up to
   the standard finitely-many-bad-primes caveat; exact K-walk over Q
   available on demand.)  `session44/u0_exact.py`, logs in
   `session44/scanlogs/u0_exact_p*.log`.
2. **Exceptional stratum `vw = -3` (where c1 = 0):** exactly the five points
   `2v^5 = 27, w = -3/v`.  The rung-3 condition there is
   `(5v^10 - 162v^5 + 81)/(64 v^4)`, and `5v^10 - 162v^5 + 81 = -4779/4 != 0`
   modulo `2v^5 = 27`.  **Exact sympy certificate; stratum dead at rung 3.**
3. **`(v,w) = (0,0)` (where the w-quadratic degenerates):** exact rational
   walk; conditions at rungs 23, 24 vanish identically; the point dies at
   rung 25 with exact obstruction `-3687131628801855/2^20`.  Kernel pattern
   is Z/5-graded (only t_{5k+4} nonzero; t_4 = 9 exactly).
4. **Pointwise control:** every quartic point over F_29 (28), F_31 (41),
   F_101 (131) dies by rung 25; branch-tracking walker
   (`session44/u0_solve.py`) with no branch discarded.

## Companion result: the generic chart (u != 0)

Full `F_29^3` and `F_31^3` grids: zero survivors of six stacked obstructions
(rungs 22-27).  u-symbolic slices (all u in F_p-bar over a fixed (v,w)):
obstruction numerators deg_u ~ 108-123 with trivial gcd per tested slice;
40 random slices at p=10007 in `scanlogs/generic_slices_p10007.log`.
Degree box of O_22: (deg_u, deg_v, deg_w) ~ (108, 54, 32).

## Net

The entire sol6 (4,6) frontier slice — the campaign's only live reduced
frontier as of Aug 26 — is dead on the u=0 chart with certificates, and dead
on the generic chart at every point tested (two full prime grids + slice
certificates).  Remaining formal gap: generic-chart points all of whose
coordinates are irrational at every tested prime; closable by trivariate
elimination (interpolation program sized above) if wanted.
