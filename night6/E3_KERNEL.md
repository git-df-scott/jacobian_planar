# night6 — the E3 kernel measurement (handoff section 3d)

All results below are **modular**, computed at `p = 999983` and `p = 1000003`.
Nothing here is a characteristic-zero statement.

Instrument: `night6/e3_final.py` (from-scratch build of the face system, the
E3 matrix, and all verification). Singular 4.x is used only as a Groebner
engine on the 6 residual equations in `q_2..q_7`; every point it returns is
rebuilt from scratch and verified by exact substitution. Raw log:
`night6/E3_KERNEL_run.log`. Machine-readable output:
`night6/e3_kernel_results.json`.

---

## 1. The face system, built from scratch

Face equation, in the brief's form:

        2*q*t' - 3*q'*t = u^2        q on u^1..u^8,   t on u^2..u^12
        gauges q_1 = q_8 = 1

Collecting the coefficient of `u^(n-1)` with `n = i+j`:

        sum_{i+j=n} (2j - 3i) q_i t_j  =  [n == 3],      n = 3..20

Measured: the row `n = 20` (the coefficient of `u^19`) vanishes identically —
its only term is `i=8, j=12` with `2*12 - 3*8 = 0`. It is the only such row.
That leaves

        **17 equations in 17 unknowns (q_2..q_7 and t_2..t_12)** — as specified.

The equation is linear in `t` at fixed `q`, and the rows `n = 3..13` are
triangular (the `i=1` term carries the coefficient `2n-5 != 0`), so
`t_2..t_12` are eliminated outright. Writing `q = u*A` (deg A = 7, `A_k =
q_{k+1}`) and `t = u^2*B` (deg B = 10, `B_k = t_{k+2}`) the same system reads
`sum_{i+j=m} (1 + 2j - 3i) A_i B_j = [m==0]`, `m = 0..17`, with `A_0 = A_7 = 1`.
Rows `m = 0..10` give `B_0..B_10`; rows `m = 11..16` are

        **6 residual equations in q_2..q_7, of total degree 9 each.**

Measured at both primes: `dim = 0`, `vdim = 35`.
This reproduces the handoff's count (35 solutions with the two gauges) and the
external T9 entry's "35 points", by an independent construction.

The lex Groebner basis is in shape position at both primes, with the
eliminant in `q_7` a **quintic in `q_7^7`** — the mu_7 structure of the
handoff, appearing here without being put in by hand:

p = 999983

        A6^35 - 29120*A6^28 - 488180*A6^21 + 310646*A6^14 - 221837*A6^7 + 60657
        A5 - 460450*A6^30 + 476168*A6^23 +  66010*A6^16 + 204123*A6^9 - 147465*A6^2
        A4 + 496633*A6^31 + 468195*A6^24 -  17695*A6^17 + 237645*A6^10 - 460160*A6^3
        A3 - 307947*A6^32 + 260259*A6^25 - 499325*A6^18 + 143221*A6^11 + 484208*A6^4
        A2 - 101858*A6^33 + 153068*A6^26 - 134735*A6^19 + 463978*A6^12 + 364585*A6^5
        A1 + 366918*A6^34 +  25024*A6^27 + 461711*A6^20 + 128695*A6^13 -  13756*A6^6

p = 1000003

        A6^35 - 241486*A6^28 -  53345*A6^21 + 473512*A6^14 + 456483*A6^7 + 74608
        A5 - 273258*A6^30 - 342005*A6^23 - 203864*A6^16 + 388333*A6^9 + 281247*A6^2
        A4 + 316992*A6^31 - 385289*A6^24 - 383555*A6^17 +  46548*A6^10 - 406590*A6^3
        A3 + 481613*A6^32 - 442653*A6^25 + 416962*A6^18 -  33793*A6^11 - 300413*A6^4
        A2 +  41559*A6^33 + 186584*A6^26 -  43751*A6^19 +  41222*A6^12 - 249191*A6^5
        A1 + 416212*A6^34 + 454733*A6^27 - 135787*A6^20 - 282409*A6^13 +  42988*A6^6

(`A_k = q_{k+1}`.) Neither prime has `7 | p-1`.

### Step 1 — face solutions found and verified

The eliminant is squarefree at both primes and factors as

| prime | irreducible factor degrees (all multiplicity 1) | sum | F_p-rational face solutions |
|---|---|---|---|
| 999983  | 1, 1, 3, 6, 6, 6, 6, 6      | 35 | **2** |
| 1000003 | 1, 2, 2, 3, 3, 6, 6, 6, 6   | 35 | **1** |

Rather than stop at the rational points, **each irreducible factor `h` was
handled in the residue field `F_p[T]/(h)`**, so that **all 35 face solutions
are covered at both primes** (the factor degrees sum to 35 in each case).

Every face solution — all 35, at both primes — was rebuilt in the gauge
`q_1 = q_8 = 1` and **verified by exact substitution**: the residual of
`2*q*t' - 3*q'*t - u^2` is identically zero in its residue field, and
`t_2 != 0`, `t_12 != 0`, `q_8 != 0` (so `deg q = 8`, `deg t = 12`) in every
case.

The two F_p-rational face solutions at `p = 999983`:

        q_1..q_8  = 1, 837658, 498604, 437449, 256910, 618550, 960107, 1
        t_2..t_12 = 1, 225111, 498604, 357087, 674165, 741731, 721534,
                    301137, 732566, 103107, 883773

        q_1..q_8  = 1, 205335, 857249, 261184, 943005, 154272, 759672, 1
        t_2..t_12 = 1, 136890, 857249, 298496, 372801, 500138, 323440,
                    296555, 817497, 316382, 679231

The one at `p = 1000003`:

        q_1..q_8  = 1, 266414, 799341, 819280, 305052, 868145, 422048, 1
        t_2..t_12 = 1, 844278, 799341, 936320, 829885, 301560, 414274,
                    898882, 986828,  80442, 709713

---

## 2. The E3 operator and its matrix

        E3(p_, s_) = 3*p_'*t + 2*q'*s_ - p_*t' - 2*q*s_'

with `p_` on `u^1..u^8` (8 columns) and `s_` on `u^2..u^12` (11 columns) — 19
columns. Coefficient of `u^(n-1)`, `n = i+j`:

        sum_{i+j=n} (3i - j) p_i t_j  +  sum_{i+j=n} (2i - 2j) q_i s_j

`n` runs 3..20, so the rows are `u^2..u^19`: **an 18 x 19 matrix**, no
identically zero rows.

Note on the support restriction the brief asks about: in this formulation
`s_` already starts at `u^2`, so `(p_, s_) = (0, c*q)` — which has
`val s_ = val q = 1` — **is not in the column span at all**. It is excluded by
the parametrisation, not by an extra condition. For reference the same
operator was also built with `s_` allowed from `u^1` (19 x 20). In that
relaxed matrix the row `u^1` is **identically zero** for every `(q,t)`
whatsoever (its only term is `q_1 s_1` with coefficient `2*1 - 2*1 = 0`), and
`(0, q)` is in the kernel for every `(q,t)` whatsoever (`E3(0,q) = 2q'q -
2qq' = 0` identically).

---

## 3. Steps 2 and 3 — the measurement

**For every one of the 35 face solutions, at both primes:**

| quantity | value |
|---|---|
| support-restricted E3 matrix | 18 x 19 (rows `u^2..u^19`), no zero rows |
| rank | **17** |
| **kernel dimension (support-restricted)** | **2** |
| relaxed matrix (`s_` from `u^1`) | 19 x 20, row `u^1` identically zero |
| relaxed rank | 17 |
| relaxed kernel dimension | 3 |
| `(0, q)` in the relaxed kernel | yes |

So, stated as the brief asks: **the kernel computed here — which is already
support-restricted — is NONZERO. Its dimension is 2, at every one of the 35
face solutions, at both primes.**

Every kernel basis vector was verified by substitution: `E3(p_, s_)` is
identically zero in the residue field for each one.

A basis at the first F_p-rational face solution, `p = 999983` (as polynomial
pairs; the basis is in reduced row-echelon form, hence the leading `1`s):

        vector 1
          p_ = 529017*u^1 + 325071*u^2 + 739013*u^3 + 979572*u^4
             + 214257*u^5 + 812422*u^6 + 326742*u^7
          s_ = 764500*u^2 + 325071*u^3 + 695518*u^4 + 512327*u^5
             + 356819*u^6 + 892649*u^7 + 596346*u^8 + 609687*u^9
             + 231592*u^10 + 1*u^11
          val p_ = 1, deg p_ = 7,  val s_ = 2, deg s_ = 11

        vector 2
          p_ = 298630*u^1 + 373496*u^2 + 855542*u^3 + 408072*u^4
             + 654148*u^5 +  29381*u^6 + 692734*u^7 + 326742*u^8
          s_ = 149315*u^2 + 373496*u^3 + 331477*u^4 +  30821*u^5
             + 344223*u^6 + 180859*u^7 + 162337*u^8 + 316939*u^9
             + 377288*u^10 + 1*u^12
          val p_ = 1, deg p_ = 8,  val s_ = 2, deg s_ = 12

At the second F_p-rational face solution, `p = 999983`:

        vector 1
          p_ = 982983*u^1 + 195156*u^2 + 724435*u^3 + 351442*u^4
             + 761312*u^5 + 602893*u^6 + 728723*u^7
          s_ = 991483*u^2 + 195156*u^3 +  11855*u^4 + 601353*u^5
             + 813645*u^6 + 313758*u^7 + 937007*u^8 + 278295*u^9
             + 745274*u^10 + 1*u^11
        vector 2
          p_ = 656402*u^1 + 551526*u^2 +  83016*u^3 + 951333*u^4
             + 236522*u^5 + 972362*u^6 +  64972*u^7 + 728723*u^8
          s_ = 328201*u^2 + 551526*u^3 +  96852*u^4 + 172964*u^5
             + 311164*u^6 + 548231*u^7 + 196334*u^8 + 783005*u^9
             + 780104*u^10 + 1*u^12

At the F_p-rational face solution, `p = 1000003`:

        vector 1
          p_ = 781952*u^1 + 298119*u^2 +  29177*u^3 + 832103*u^4
             +  56763*u^5 +  43165*u^6 + 981038*u^7
          s_ = 390976*u^2 + 298119*u^3 + 200707*u^4 + 271254*u^5
             + 540706*u^6 +  88528*u^7 + 737798*u^8 +  48081*u^9
             + 715637*u^10 + 1*u^11
        vector 2
          p_ = 229643*u^1 + 526482*u^2 + 817160*u^3 + 909451*u^4
             +  58849*u^5 + 560620*u^6 +  58154*u^7 + 981038*u^8
          s_ = 614823*u^2 + 526482*u^3 + 620019*u^4 + 881659*u^5
             + 543391*u^6 + 243826*u^7 + 808829*u^8 + 359345*u^9
             + 604237*u^10 + 1*u^12

The bases over the degree 2, 3 and 6 residue fields are in the raw log and in
`e3_kernel_results.json`; their shape is the same in every case — one vector
with `val p_ = 1, deg p_ = 7, val s_ = 2, deg s_ = 11` and one with
`val p_ = 1, deg p_ = 8, val s_ = 2, deg s_ = 12`.

### Measured degree/valuation data on the kernel

Across all 35 face solutions at both primes, every kernel basis vector has
`val p_ = 1` and `val s_ = 2`, i.e. `val s_ = val p_ + 1`. That is the
relation the handoff's valuation analysis of E3 predicts (`b = a + 1` with
`a = val p`, `b = val s`). The observed `(deg p_, deg s_)` pairs are `(7,11)`
and `(8,12)`, both of the form `deg s_ = deg p_ + 4`, which is the third of
the three cases the handoff's top-degree analysis leaves open.

---

## 4. Controls

**Negative / genericity control.** The same E3 matrix built from *random*
`(q,t)` with `q_1 = q_8 = 1` (verified NOT to satisfy the face equation), 5
seeds at each prime, all 10 trials identical:

        support-restricted 18 x 19 : rank 18, kernel dimension 1
        relaxed            19 x 20 : rank 18, kernel dimension 2
        (0, q) in the relaxed kernel : yes

So a nonzero support-restricted kernel is **not by itself a face phenomenon**:
with 19 columns and 18 rows the kernel is at least 1-dimensional for any
`(q,t)` at all. What the face equation buys is exactly one further rank drop,
18 -> 17, i.e. kernel dimension 1 -> **2**. That extra drop is the content of
the measurement.

**Positive control.** `E3(0, q) = 2q'q - 2qq' = 0` identically; the relaxed
matrix confirms `(0,q)` in its kernel in every case, on-face and off-face
alike.

**Structural controls that agreed with independent sources.** `dim = 0` and
`vdim = 35` for the residual ideal (handoff: 35 solutions with these two
gauges, confirmed there by six instruments; external T9 entry: 35 points); the
eliminant is a quintic in `q_7^7` (handoff: msolve gives an exact irreducible
quintic in `T^7`, five covers times mu_7); the row `u^19` of the face system
vanishes identically, forcing 17 equations rather than 18.

---

## 5. Step 4 — cross-prime consistency

| | p = 999983 | p = 1000003 | agree |
|---|---|---|---|
| residual ideal dim | 0 | 0 | yes |
| residual ideal vdim | 35 | 35 | yes |
| face solutions covered | 35 of 35 | 35 of 35 | yes |
| support-restricted E3 shape | 18 x 19 | 18 x 19 | yes |
| rank, every face solution | 17 | 17 | yes |
| **kernel dimension, every face solution** | **2** | **2** | **yes** |
| relaxed kernel dimension | 3 | 3 | yes |

No disagreement between the primes on any quantity measured. The eliminant's
*factorisation pattern* differs between the primes (1,1,3,6,6,6,6,6 versus
1,2,2,3,3,6,6,6,6), as does the number of F_p-rational face solutions (2
versus 1); these are properties of the residue fields, not of the geometry,
and the full 35 are covered at both primes with identical kernel data.

---

## 6. Scope

Modular only. Two primes, agreeing. No claim is made here about
characteristic zero, about whether these kernel elements integrate against the
other four identities `E0, E1, E2, E4`, or about anything downstream. The
prepared response in `night6/RUNBOOK_KERNEL_NONZERO.md` lists the steps that
would have to come next; none of them has been run.
