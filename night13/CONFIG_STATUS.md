# night13 — reconstruction of the corrected probe protocol, and configuration status

Measurements only. Written **before** any new computation in this session, from
the files present on branch `claude/fable-6o0nqe` at commit `da9a396`
("snapshot: state at session interruption").

---

## 1. What the four configurations are

`H_SCREEN.md` §6–§7 fixes them. At `m = 42`, degree pair `(deg P, deg Q) =
(84, 126)`, the screen's survivors are exactly the H-supports whose extreme-ray
factors `2·e0` and `3·(m − e1)` share a common prime. The two top-ranked
survivors (`rank_char2.json`, key `"42"`, field `ranked`) are

| rank | support `E` | `e0` | `e1` | `2 e0` | `3(m − e1)` | `g` | survives in char |
|---|---|---|---|---|---|---|---|
| 1 | `{5, 8, 11, 17, 29, 32}` | 5 | 32 | 10 | 30 | 10 | 2 and 5 |
| 2 | `{5, 8, 11, 23, 29, 32}` | 5 | 32 | 10 | 30 | 10 | 2 and 5 |

A **configuration** is a (support, characteristic) pair, so there are four:
`top1_char2`, `top1_char5`, `top2_char2`, `top2_char5`.

**Recorded deviation on the two working primes.** The lane's dual-prime
discipline is 999983 / 1000003. `H_SCREEN.md` §5 and the docstring of
`survivor_probe.py` state that both of these primes divide neither `2 e0 = 10`
nor `3(m − e1) = 30`, so at 999983 and at 1000003 these supports fail the
unavoidable-singleton screen exactly as the stage-1 support `{2,14,29,41}` did.
Probing there would only re-measure the two-row obstruction. The dual-prime
discipline is therefore carried out as **dual-characteristic**: each support is
probed in both characteristics in which it survives, 2 and 5. That is the sense
in which "cross-prime agreement" is reported below.

---

## 2. The corrected protocol, as coded in `survivor_probe.py`

Per configuration:

1. **Carrier build** (`build_carrier`, cached as `carrier_<tag>.json`).
   Characteristic-aware leading supports (`screen.leading_supports`: in char 2
   the `H^2` cross terms die, in char 3 the `H^3` ones), Newton hulls of
   `supp(H^2) ∪ {(0,0),(1,0)}` and `supp(H^3) ∪ {(0,0),(0,1)}`, maximal lower
   pools, then the stage-1 greedy — net-singleton score with a generic-rank-gain
   tie-break (`PS.TIE_POOL_CAP`), stopping at 96 lower P-monomials and 256 lower
   Q-monomials. `(1,0)` and `(0,1)` are seeded. Incidence is char-aware
   (`class Inc`: a route counts only when `p1 a2 − p2 a1 ≢ 0 mod char`).

2. **Control gate** — five controls, all must pass:
   `C0_positive_control`, `Ca_leading_bracket_identically_zero`,
   `Cb_degenerate_carrier_row_identities`, `Cb2_extreme_rows_vanish_mod_char`
   (the two extreme-ray rows `(2e0−1, 2(m−e0))` and `(3e1, 3(m−e1)−1)` must
   vanish mod the characteristic — this is *why* the support survives),
   `Cc_rank_sanity` (nonzero rank, constant row present, both extreme rows
   absent from the matrix).

3. **220 sampled P-blocks.** `random.Random(7000 + s)`, `s = 0..219`; sample 0
   is dense (`ones = 1.0`), the rest use a lower-block density drawn from
   `{0.25, 0.5, 0.75}`. Top block: `h_(e0) = 1` (chart), all other `h_e` and `A`
   uniform on the nonzero residues; `a_(1,0)` forced nonzero.

4. **Consistency.** `build_Q_system(P, H^3, C_Q, char)` gives the exact linear
   system in the `1 + |C_Q|` unknowns `(B, lower Q coefficients)`;
   `K.rank_modp(..., augment=True)` gives `rank_A`, `rank_Ae` and the
   Rouché–Capelli verdict `consistent`.

5. **The correction — the realization check.** This is what the earlier,
   uncorrected run lacked. A consistent system only *realizes* the `(H^2, H^3)`
   leading profile if the `Q` leading form survives, i.e. `B ≠ 0`.
   `B_free(rows, ...)` compares `rank` of the full matrix with `rank` of the
   matrix with column 0 (the `B` column) deleted:

   * equal ranks ⇒ the `B` column lies in the span of the others ⇒ the solution
     set projects onto all of `F_char` in the `B` coordinate, so a solution with
     `B ≠ 0` exists;
   * unequal ⇒ `B` is **forced** to one fixed value on the whole solution set;
     if that value is 0 the sample is tallied `degenerate_B_forced_zero`.

   When `B` is free, a solution with `B = 1` is built by moving column 0 to the
   right-hand side, the polynomial `Q` is assembled, and the sample counts as
   `consistent_with_nonzero_B` only if **both** `K.bracket(P, Q, char) ==
   {(0,0): 1}` exactly **and** `deg P = 2m`, `deg Q = 3m` (mandatory leading
   coefficients nonzero, profile realized).

Tally keys: `consistent`, `consistent_with_nonzero_B`, `inconsistent`,
`degenerate_B_forced_zero`. Halt-and-commit fires only on
`consistent_with_nonzero_B > 0`, writing `HIT_char<c>_<tag>/hits.json`.

---

## 3. Which configuration the predecessor tested, and what it found

`HIT_char2_top1_char2_PRE_BTEST/hits.json` is the **uncorrected** run of
`top1_char2`: 220 recorded "hits", each with `consistent: true`,
`bracket_is_one: true`, `deg_P: 84` — and **`deg_Q: 1`**. The bracket was
satisfied by taking `Q` to be (essentially) the single monomial `y`: `B = 0`,
the `H^3` leading form gone, the `(84, 126)` profile not realized. That is the
defect the `B` test was written to catch, and the directory was renamed
`_PRE_BTEST` rather than deleted.

The corrected re-run of that same configuration is
`survivor_top1_char2.json`: gate `True`, tally
`consistent 220 / inconsistent 0 / degenerate_B_forced_zero 220 /
consistent_with_nonzero_B 0`, `n_hits 0`. This matches the predecessor's final
report verbatim — "220/220 consistent but B forced to zero in every one".

**So the tested configuration is `top1_char2`, and the three remaining are
`top1_char5`, `top2_char2`, `top2_char5`.**

## 4. Pre-existing artifacts for the three remaining configurations

The interruption snapshot already contains `survivor_top1_char5.json`,
`survivor_top2_char2.json`, `survivor_top2_char5.json` and their logs
(`s_top1_char5.log`, `s_top2_char2.log`, `s_top2_char5.log`), written after the
`B` test was added. They were never reported. They are **not** taken on trust:
they are copied to `survivor_<tag>_PRED.json` and each configuration is re-run
from the same code with the same fixed seeds; agreement or disagreement of the
two tallies is reported in `CONFIGURATIONS.md`.
