
### 5.1 What the table says, in aggregate

* **Every one of the 57 survivors has exactly one atypical value, except one
  (`808e52fdb1b6`), which has two.**  For the 53 members of the G1 family the
  atypical value is `c = 0` — the value at which `P = h0 v + c (x-a)^n v^m`
  factors as `v * (h0 + c (x-a)^n v^(m-1))`.  For the four G2 members
  `P = alpha x + beta + c B(x) y^m` the atypical values are `lam = alpha a_i + beta`,
  one for each distinct root `a_i` of `B`: at such a `lam` the content
  `gcd(c B(x), alpha x + beta - lam)` becomes non-trivial and the vertical line
  `{x = a_i}` splits off as a component.  Every atypical fibre found in the whole
  run is reducible with a `chi` that jumps up.

* **Suzuki accounting closes on all 57.**  Decomposing
  `C^2 = P^{-1}(C \ S) u (union of the fibres over S)` for any finite `S`
  containing the atypical values, and using that `P` restricted over `C \ S` is
  a locally trivial fibration with fibre `F_gen`,

      1 = chi(C^2) = chi(F_gen) (1 - |S|) + sum_{c in S} chi(F_c)
        = chi(F_gen) + sum_c ( chi(F_c) - chi(F_gen) ) .

  So the jumps must sum to `1 - chi_gen`.  In all 57 rows the jumps at the
  atypical values found sum to **exactly** `1 - chi_gen` (column
  `suzuki_closes` in `atypical.csv`: 57/57 True).  This is a strong
  self-consistency check on the detector and on the completeness of each
  atypical set.  (It closes the set completely if one also uses the standard
  fact — quoted, not derived here — that for a polynomial with no critical
  points every jump `chi(F_c) - chi(F_gen)` is non-negative.)

* **16 algebraic candidate values were left untested** (all of them inside the
  eight high-degree sheared members), because their minimal polynomials have
  degree 8, 16 or 40 and exact arithmetic in those number fields was not
  affordable here.  They are listed in `atypical.csv`
  (`untested_algebraic_candidates`).  For each of those eight `P` the jump at
  `c = 0` already accounts for the whole of `1 - chi_gen`, so under the
  non-negativity fact just quoted no untested candidate can be atypical; that
  is recorded as an accounting statement, not as an exact test.

### 5.2 Periods on the atypical fibres

* **EXACT-PRIM returns a verified certificate on every component of every
  atypical fibre of all 57 `P`** — i.e. an explicit polynomial `F` with
  `[P, F] - 1 = G h` checked coefficientwise over `Q` for each irreducible
  factor `h` of `P - c`.  The certificates are of very low degree (1, 2 or 3).
  Every period of `eta` over every cycle of every atypical fibre therefore
  vanishes, exactly.  This is the closed-form statement of §4.1 reproduced by
  machine on each actual (sheared) `P`.

* **NUM-MONO agrees wherever it completed**: `VANISHING` with least-squares
  residual at the `1e-15` level and residues at the `1e-16` level, and its own
  `chi` equal to the exact `chi` minus the number of vertical components (which
  the `x`-projection cannot see — see control C3e).  Where it did not complete
  it hit the wall-clock budget and is reported as such; no NUM-MONO run on any
  atypical fibre returned `NONVANISHING`.

* **At the nearby generic values `c0 ± 1/8` and `c0 ± 1/64` the exact `chi`
  is the generic one in every case**, so the atypical fibre really is isolated,
  and EXACT-PRIM at those nearby `c` returns a certificate of degree 2–5 in
  most rows.  Where it returns `NO_EXACT_CERTIFICATE` that is a statement about
  the search bound `deg F <= 6` only: night15 had already certified those
  generic fibres `VANISHING` by exact residue/genus arguments, and control C4
  shows EXACT-PRIM needs a higher bound on some genuinely vanishing fibres.

### 5.3 One survivor is obstructed — at a GENERIC value night15 never sampled

`808e52fdb1b6` (`P = 2x - 1 - x^2 (x-1)^3 y^4`, the G2 member with
`B = x^2 (x-1)^3`, `m = 4`) is the one row where the detector changes the
night15 picture, and it does so in an unexpected place.

Its atypical values are `c = -1` and `c = 1`.  night15 screened this `P` with
NUM-MONO **at `c = 1` and `c = -1` only** — that is, at *both* of its atypical
values and at no other fibre.  Its `PERIODS-VANISHING` verdict therefore rested
on no generic fibre at all.  The night15 record also explains the single
disagreement in control C3f: the genus `0` and `8` places-at-infinity recorded
for this `P` are the data of its atypical fibre `c = 1`, not of its generic one.

Measured here at five generic values (`g2check16.json`):

| c | exact chi | NUM-MONO chi | components | punctures | genus | ls-residual | error estimate | max period | max residue | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| 3 | -7 | -7 | 1 | 7 | 1 | 2.2708 | 2.4e-14 | 1.3110 | 5.8e-18 | NONVANISHING |
| 5 | -7 | -7 | 1 | 6 | 1.5 | 1.4847 | 7.1e-15 | 0.8377 | 1.3e-17 | NONVANISHING |
| -3 | -7 | -7 | 1 | 7 | 1 | 1.9095 | 2.1e-14 | 1.1024 | 1.9e-17 | NONVANISHING |
| 2 | -7 | -7 | 1 | 7 | 1 | 3.4508 | 3.0e-13 | 1.9923 | 3.5e-17 | NONVANISHING |
| 1/2 | -7 | -7 | 1 | 7 | 1 | 5.8036 | 8.9e-16 | 3.3507 | 2.8e-17 | NONVANISHING |

The residues at all places are zero to `1e-17` while the least-squares residual
of the potential system is of order 1 with an error estimate of order `1e-14`:
the obstruction is a genuine period, not a residue.  EXACT-PRIM finds no
primitive to `deg F <= 8` on these generic fibres, which is consistent (and,
by itself, not a proof).

So `808e52fdb1b6` **is** obstructed by the period screen — at its generic
fibres, which night15 never measured — while its two atypical fibres carry
exact primitives and vanish.  It is reported in the table as
`STILL-VANISHING` because that column records the atypical re-screen, and
separately here as `GENERIC-FIBRE OBSTRUCTED (night15 sampling gap)`.

---

## 6. Exact mate re-solve, above night15's ceiling

night15 escalated the Keller carrier to `deg Q = 2 deg P` and obtained
`EMPTY_over_Q` with an exact lambda certificate at every stage for all 57.
night16 restarts *above* that ceiling: for each `P` the full triangular carrier
is taken at `D = 2 deg P + 1`, `2 deg P + 2`, and the largest `D <= 3 deg P`
whose carrier fits in `MAXCOLS = 1600` columns.  Every `EMPTY` verdict carries
an exact rational lambda with `lambda^T A = 0` and `lambda^T e = 1`,
re-verified over `Q` (night12's decision layer, copied into this lane as
`exact16.py` / `matekit16.py`).

HIT GATE: a consistent system would be reconstructed to an exact `Q`, verified
by expanding `[P,Q] - 1` coefficientwise over `Q`, and written to
`night16/HIT_<hash>/`.

