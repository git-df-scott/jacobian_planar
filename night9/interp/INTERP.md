# night9/interp — CRT interpolation across primes

Scope note. Measurements only. Every result is labelled with its
characteristic or with the ring it was computed in. No assessment of what any
of these numbers mean is offered. **Every object produced here is filed
CANDIDATE-UNVERIFIED, regardless of outcome**, per the brief.

Script: `night9/interp/interp.py`.
Data: `night9/interp/9fad1aac9556_interp.json`.
Independent hand-plus-symbolic audit of the distinguished vector:
`night9/interp/AUDIT.md`.

## 1. Input

The cross-prime matrix (`night9/CROSS_PRIME.md` §4) records exactly one of the
twelve distinguished supports as non-degenerate NONEMPTY at three or more
distinct primes:

    hash 9fad1aac9556      primes 2, 3, 5      modulus M = 30
    S_P = (0,10) (1,0) (2,1) (3,0)      (this order fixes the a-indexing)
    S_Q = (0,1)  (2,1) (3,10) (4,0)     (this order fixes the b-indexing)

Complete non-degenerate solution sets re-enumerated here (exhaustive-bilinear,
`solution_list_is_complete = true` at each prime):

| characteristic | total F_p solutions | non-degenerate |
|---|---|---|
| p = 2 | 3 | 3 |
| p = 3 | 6 | 4 |
| p = 5 | 20 | 20 |

## 2. The matching criterion (stated)

Two solutions at two different primes are declared MATCHED when both hold.

* **(M1) support pattern.** The zero / non-zero pattern of the coefficient
  vector is identical across the primes: the index sets
  `{i : a_i != 0 in F_p}` and `{j : b_j != 0 in F_p}` agree.
* **(M2) collision image.** The two collision values `v_P = P(0,1) = P(1,0)`
  and `v_Q = Q(0,1) = Q(1,0)` (convention `0^0 = 1`) of the coefficient-wise
  CRT lift reduce, at every prime, to that prime's values. Because `v_P` and
  `v_Q` are integer-linear in the coefficients, (M2) is implied by
  coefficient-wise CRT; it is therefore **recorded as a check, not used to
  prune**. It held for all 32 tuples below.

A MATCHED TUPLE is one solution per prime satisfying (M1). Support patterns
seen across the three primes: 4. Patterns present at **all three** primes: 1,
namely `P` non-zero on indices {0,1} and `Q` non-zero on indices {0,2,3}.
Matched tuples formed from that pattern: 1 x 2 x 16 = **32**.

## 3. Lifting, reconstruction, exact verification over Q

Two lifts are computed per coefficient from its CRT residue mod 30:

* **(R1)** the symmetric integer representative in `(-15, 15]`;
* **(R2)** Wang rational reconstruction with numerator and denominator bounded
  by `floor(sqrt(M/2)) = 3`, recorded as FAILED when no such rational exists.

Both lifts are substituted **exactly over Q** (sympy, rational arithmetic)
into `det J - 1 = P_x Q_y - P_y Q_x - 1` and into the two collision
equalities.

| quantity | value |
|---|---|
| matched tuples | 32 |
| (M2) check held | 32 / 32 |
| R2 rational reconstruction succeeded for every coefficient | 2 / 32 |
| collision equalities exact over Q (R1 lift) | **32 / 32** |
| `det J - 1` identically zero over Q (R1 lift) | **0 / 32** |
| `det J - 1` identically zero over Q (R2 lift, where defined) | **0 / 2** |
| tuples passing exact verification over Q | **0** |

Distinct `det J - 1` residuals over Z among the 32 R1 lifts: **15**. The
smallest-coefficient one, attained by two tuples (`a = (1,1,0,0)`,
`b = (1,0,1,1)` and its negation `a = (-1,-1,0,0)`, `b = (-1,0,-1,-1)`), is

    det J - 1  =  -30 x^3 y^9 - 30 x^2 y^19  =  -30 x^2 y^9 (x + y^10)

i.e. `P = y^10 + x`, `Q = y + x^3 y^10 + x^4`. This is the vector audited
independently in `AUDIT.md`; `30 = 2 * 3 * 5`. All other 13 residuals carry
larger integer coefficients, and 12 of the 15 additionally carry a non-zero
constant term (`+90` or `+120`), so the `(0,0)` Keller equation itself fails
over Z for those.

**No object produced by this stage passed exact verification over Q.**

## 4. Files

* `night9/interp/interp.py` — the script (matching criterion in its docstring).
* `night9/interp/9fad1aac9556_interp.json` — all 32 matched tuples, each with
  its per-prime residues, collision images, tear class, both lifts, and both
  exact-over-Q check records; every entry carries `"label":
  "CANDIDATE-UNVERIFIED"`.
* `night9/interp/AUDIT.md` — the independent recomputation of the
  distinguished residual.
