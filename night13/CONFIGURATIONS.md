# night13 stage 2e — the four survivor configurations under the corrected probe

Measurements only. Every count says what was computed, in which ring and
characteristic. The protocol reconstruction is in `night13/CONFIG_STATUS.md`;
the screen that produced these configurations is in `night13/H_SCREEN.md`.

---

## 1. The configurations

`m = 42`, degree pair `(deg P, deg Q) = (84, 126)`, not divisibility-ordered.
The two top-ranked survivors of the unavoidable-singleton screen, each probed
in both characteristics in which it survives:

| tag | support `E` | `e0` / `e1` | `2 e0` / `3(m−e1)` | char |
|---|---|---|---|---|
| `top1_char2` | `{5, 8, 11, 17, 29, 32}` | 5 / 32 | 10 / 30 | 2 |
| `top1_char5` | `{5, 8, 11, 17, 29, 32}` | 5 / 32 | 10 / 30 | 5 |
| `top2_char2` | `{5, 8, 11, 23, 29, 32}` | 5 / 32 | 10 / 30 | 2 |
| `top2_char5` | `{5, 8, 11, 23, 29, 32}` | 5 / 32 | 10 / 30 | 5 |

**On the two working primes.** At 999983 and at 1000003 neither extreme-ray
factor vanishes, so both supports fail the screen there exactly as the stage-1
support `{2,14,29,41}` did (`H_SCREEN.md` §5). The dual-prime discipline of the
lane is carried out here as **dual-characteristic**: 2 and 5, the two primes
dividing `g = gcd(2 e0, 3(m−e1)) = 10`. This deviation is recorded in
`survivor_probe.py`'s docstring and in `H_SCREEN.md` §7.

---

## 2. Per-configuration tally — 220 sampled P-blocks each

`random.Random(7000 + s)`, `s = 0..219`; sample 0 dense, the rest with lower-block
density in `{0.25, 0.5, 0.75}`. All five controls pass in all four
configurations (gate `True` everywhere), including
`Cb2_extreme_rows_vanish_mod_char`.

| configuration | ring | gate | consistent | inconsistent | B forced to 0 | **profile realized** (`B ≠ 0` and both mandatory leading coefficients nonzero) |
|---|---|---|---|---|---|---|
| `top1_char2` | `F_2` | pass | 220 | 0 | **220** | **0** |
| `top1_char5` | `F_5` | pass | 0 | **220** | 0 | **0** |
| `top2_char2` | `F_2` | pass | 220 | 0 | **220** | **0** |
| `top2_char5` | `F_5` | pass | 0 | **220** | 0 | **0** |
| **total** | | 4/4 | **440** | **440** | **440** | **0** |

`consistent + inconsistent = 220` in every row; `degenerate_B_forced_zero =
consistent` in every row. No configuration produced a sample with `B ≠ 0`, so
the halt-and-commit gate never fired and no `HIT_` directory was written by this
session. Sources: `survivor_top1_char2.json`, `survivor_top1_char5.json`,
`survivor_top2_char2.json`, `survivor_top2_char5.json`; run log
`rerun_three.log` plus `s_top*.log`.

### Rank shape behind each verdict

| configuration | nonzero bracket rows | `rank A` | `rank (A|e)` | `rank A` without the `B` column |
|---|---|---|---|---|
| `top1_char2` | 7 | 2 | 2 | 1 |
| `top2_char2` | 7 | 2 | 2 | 1 |
| `top1_char5` | 868–940 (sample-dependent) | 185 | 186 | — |
| `top2_char5` | 897–991 (sample-dependent) | 185 | 186 | — |

* **char 2.** Consistent (`rank A = rank (A|e)`), but deleting the `B` column
  drops the rank from 2 to 1, so `B` is not free: it takes one fixed value on
  the entire solution set, and that value is `0` in all 220 samples of both
  configurations. The `(H^2, H^3)` leading profile is not realized — solutions
  exist, but not with the profile. Over `F_2` the top chart is a single point
  (every nonzero coefficient is 1) and Frobenius kills the `H^2` and `H^3` cross
  terms, which is why only 7 bracket rows survive at all.
* **char 5.** `rank (A|e) = rank A + 1` in every sample of both configurations:
  the exact linear system in `(B, lower Q coefficients)` has no solution at all,
  with or without a condition on `B`.

---

## 3. Cross-characteristic agreement

| support | char 2 verdict | char 5 verdict | agree on realization |
|---|---|---|---|
| `{5, 8, 11, 17, 29, 32}` | 220 consistent, `B` forced 0, 0 realized | 220 inconsistent, 0 realized | **yes (0 = 0)** |
| `{5, 8, 11, 23, 29, 32}` | 220 consistent, `B` forced 0, 0 realized | 220 inconsistent, 0 realized | **yes (0 = 0)** |

The two characteristics **disagree on consistency** (all-consistent in char 2,
all-inconsistent in char 5) and **agree on the quantity of interest**: the
realized count is 0 on both sides, for both supports. The two supports agree
with each other configuration-for-configuration: identical tallies, identical
rank shapes.

---

## 4. Reproduction and independent re-verification

**Reproduction.** The three configurations `top1_char5`, `top2_char2`,
`top2_char5` were re-run in this session from the cached carriers with the same
fixed seeds. The predecessor's artifacts were preserved as
`survivor_<tag>_PRED.json` and compared field-by-field with the new output: all
three are **bit-identical apart from `elapsed_s`** (`consistent`,
`inconsistent`, `degenerate_B_forced_zero`, `consistent_with_nonzero_B`,
`n_hits`, `controls`, `gate`, `carrier`, `samples_head` all equal).

**Independent re-verification** (`verify_four.py`, `verify_four.json`), 20
samples per configuration, not reusing the probe's verdict path:

| check | `top1_char2` | `top1_char5` | `top2_char2` | `top2_char5` |
|---|---|---|---|---|
| consistency agrees under two independent rank seeds | yes | yes | yes | yes |
| system with the `B` column moved to the RHS at `B = 1` solvable | **no** | **no** | **no** | **no** |
| `B` in the plain solution | `0` (all 20) | n/a (inconsistent) | `0` (all 20) | n/a |
| `deg Q` of the plain solution | `1` (all 20) | n/a | `1` (all 20) | n/a |

The char-2 solutions are exactly the degenerate ones: `Q` collapses to degree 1
(the seeded monomial `y`), against the required `deg Q = 3m = 126`. This
reproduces, from an independent code path, the defect visible in
`HIT_char2_top1_char2_PRE_BTEST/hits.json`, where all 220 recorded entries carry
`bracket_is_one: true`, `deg_P: 84` and `deg_Q: 1`.

---

## 5. Overall verdict tally

| quantity | count |
|---|---|
| configurations probed | 4 of 4 (`{5,8,11,17,29,32}` and `{5,8,11,23,29,32}`, each in char 2 and char 5) |
| control gates passed | 4 / 4 |
| P-block samples | 880 (220 per configuration) |
| consistent systems | 440 (all in char 2) |
| inconsistent systems | 440 (all in char 5) |
| consistent with `B` forced to 0 | 440 / 440 |
| **samples realizing the profile (`B ≠ 0`, mandatory leading coefficients nonzero)** | **0 / 880** |
| exact brackets verified with the profile realized | 0 |
| `HIT_` directories written by this session | 0 |
| halt-and-commit gate | **not reached** |

Scope of the measurement: these four configurations, at `m = 42`, degree pair
`(84, 126)`, under the carriers `carrier_top{1,2}_char{2,5}.json` (96 lower
P-monomials, 256 lower Q-monomials, stage-1 greedy) and the sampling described
above, in `F_2` and `F_5`. Nothing here is measured at char 0, 999983 or
1000003, where these supports do not survive the screen.

---

## 6. File index (additions of this session)

| file | content |
|---|---|
| `CONFIG_STATUS.md` | reconstruction of the corrected protocol, written before computing |
| `CONFIGURATIONS.md` | this file |
| `rerun_three.log` | run log of the three re-run configurations |
| `survivor_top1_char5_PRED.json`, `survivor_top2_char2_PRED.json`, `survivor_top2_char5_PRED.json` | predecessor artifacts preserved for the bit-comparison |
| `verify_four.py`, `verify_four.json` | independent re-verification, 20 samples per configuration |

Note on provenance: `CONFIG_STATUS.md` was swept into the concurrent night12
lane's commit `5b37542` by that lane's staging; its content is unmodified.
