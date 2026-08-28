# night12 -- MATE SEARCH v1: results

Measurements only. Nothing in this file is a conclusion. Ring labels as in
`MATE_V1.md`: **ring: Q** = exact rational arithmetic; **ring: F_p** = the
scheduling prime, which decides nothing.

Apparatus: `sy.py`, `screens.py`, `carriers.py`, `pool.py`, `exact.py`,
`v1.py`, `controls_v1.py` (all documented in `MATE_V1.md`), plus the three
files added by this run: `s1_retry.py`, `m1_run.py`, `sy_crosscheck.py`.

## 1. Hit gate

The gate is: a mate `Q` certified over `Q` by E3 (coefficientwise expansion
of `[P,Q] - 1`), for a `P` that S1/S2 passed, whose SY verdict is
`NON_COORDINATE`. On a hit the run halts and writes `night12/HIT_<hash>/`.

| quantity | value |
| --- | --- |
| P through the screened-and-passed pipeline | 30 |
| P through the M1 override arm | 200 |
| P through the undecided override arm | 13 |
| P through some arm, total | 243 |
| mates certified over Q (E3) | 20 |
| of those, SY NON_COORDINATE | 0 |
| **hit-gate status** | **NOT TRIPPED -- 0 hits; the run did not halt** |

Every mate certified in this run sits on a `P` that SY certifies
`COORDINATE`, and every `P` that SY certifies `NON_COORDINATE` reached an
exact emptiness certificate at every stage tried. The gate never fired.

## 2. Controls (hard gate)

`controls_v1.py` now carries an explicit gate with a nonzero exit code; see
the fix log in section 7.

**PASS -- 15 checks, 0 failed.**

| check | ok | detail |
| --- | --- | --- |
| SY[x] | ok | got COORDINATE, brief label COORDINATE |
| SY[x + y^2] | ok | got COORDINATE, brief label COORDINATE |
| SY[x + x^2*y] (unlabeled in brief) | ok | got NON_COORDINATE |
| SY[x*y] | ok | got NON_COORDINATE, brief label NON_COORDINATE |
| SY[x^2*y] | ok | got NON_COORDINATE, brief label NON_COORDINATE |
| SY[x + y^126] | ok | got COORDINATE, brief label COORDINATE |
| SY[x^126 + y^127 + x^2*y^2] (unlabeled in brief) | ok | got NON_COORDINATE |
| SY[x + y^2 + 2x^2y + x^4] | ok | got COORDINATE, brief label COORDINATE |
| C-POS screens pass | ok | S2=pass S1=pass |
| C-POS SY COORDINATE | ok | COORDINATE |
| C-POS mate found | ok | MATE |
| C-POS mate is exact_solution certified | ok |  |
| C-NEG rejected by S1 | ok | origin is a common zero of (P_x,P_y) |
| C-NEG no mate on override | ok | NO_MATE_ALL_STAGES |
| C-NEG every stage EMPTY_over_Q with a certificate | ok | Y:EMPTY_over_Q[lambda_exact], C:EMPTY_over_Q[lambda_exact], W:EMPTY_over_Q[lambda_exact] |

- **C-POS  P = x + y^126**: screens passed=True, SY=COORDINATE, outcome=MATE, deg Q = 1
- **C-NEG  P = x^126 + y^127 + x^2*y^2**: screens passed=False, SY=NON_COORDINATE, outcome=NO_MATE_ALL_STAGES

### Independent cross-check on the SY verdicts

`sy_crosscheck.py`. If `P` is a coordinate then `P - c` is irreducible for
every `c`, since an automorphism of the ring preserves irreducibility. So a
`c` for which `P - c` factors is an independent proof of `NON_COORDINATE`.
One-sided: `NO_FACTORISATION_FOUND` carries no information. Nothing here
feeds a decision; `sy.py` is untouched.

| P | SY verdict | brief label | fibre check | agreement |
| --- | --- | --- | --- | --- |
| `x` | COORDINATE | COORDINATE | NO_FACTORISATION_FOUND | - |
| `x + y^2` | COORDINATE | COORDINATE | NO_FACTORISATION_FOUND | - |
| `x + x^2*y` | NON_COORDINATE | ? | REDUCIBLE_FIBRE | agrees |
| `x*y` | NON_COORDINATE | NON_COORDINATE | REDUCIBLE_FIBRE | agrees |
| `x^2*y` | NON_COORDINATE | NON_COORDINATE | REDUCIBLE_FIBRE | agrees |
| `x + y^126` | COORDINATE | COORDINATE | NO_FACTORISATION_FOUND | - |
| `x^126 + y^127 + x^2*y^2` | NON_COORDINATE | ? | NO_FACTORISATION_FOUND | - |
| `x + y^2 + 2x^2y + x^4` | COORDINATE | COORDINATE | NO_FACTORISATION_FOUND | - |

- `x + x^2*y`: `P - (0)` factors as `x | xy+1`.
- `x*y`: `P - (0)` factors as `x | y`.
- `x^2*y`: `P - (0)` factors as `x | y`.

Disagreements: **0**.

This settles the one discrepancy the predecessor recorded. The note in
`controls_v1_log.txt` says the brief labels `x + x^2*y` a coordinate; the
validation table in `sy.py` in fact carries `?` for it (unlabeled), and the
factorisation `x + x^2*y = x*(1 + x*y)` is an independent proof that it is
not a coordinate. The SY implementation's verdict stands.

## 3. Screen tally

S2 (`gcd(P_x,P_y)` a unit) runs first, then S1 (`1` in `(P_x,P_y)` over Q,
Groebner). S3 is recorded as a selection bias, never a gate.

| family | n | S2 pass | S1 pass | S1 reject | S1 timeout | S2 reject | passed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HDC | 8 | 8 | 8 | 0 | 0 | 0 | **8** |
| M1 | 120 | 120 | 0 | 111 | 9 | 0 | **0** |
| M1L | 80 | 80 | 0 | 80 | 0 | 0 | **0** |
| V0_A_rand_sparse_lin | 44 | 44 | 1 | 41 | 2 | 0 | **1** |
| V0_B_rand_sparse_nolin | 22 | 5 | 0 | 5 | 0 | 17 | **0** |
| V0_C_struct_x | 33 | 31 | 10 | 20 | 1 | 2 | **10** |
| V0_D_leadsq | 36 | 36 | 0 | 33 | 3 | 0 | **0** |
| V0_E_leadcube | 28 | 28 | 0 | 21 | 7 | 0 | **0** |
| V0_F_coord | 11 | 11 | 11 | 0 | 0 | 0 | **11** |
| **total** | **382** | 363 | 30 | 311 | 22 | 19 | **30** |

**The M1 measurement.** Every one of the 200 M1 and M1L `P` is rejected by S1:
the gradient pair `(P_x, P_y)` has a common zero over `Qbar`. This is a
property of the family as `carriers.make_P` builds it, not of the screen. It
reproduces at small `m`, where the Groebner computation is immediate: for
`P = x + A*H^2` with `H` a form of degree `m`,

```
P_x = 1 + 2A*H*H_x,   P_y = 2A*H*H_y
```

so a common zero needs `H = 0` or `H_y = 0`. On `H = 0` we get `P_x = 1`, no
zero; but `H_y = 0` is a union of lines through the origin, and restricting
`1 + 2A*H*H_x` to such a line gives a one-variable polynomial of degree
`2m - 1 > 0`, which has roots. So the M1 shape carries gradient common zeros
generically. Small-`m` confirmation (S2 pass, S1 reject at every one):

```
m= 5 degP= 10  S2=pass  S1=reject (HAS_COMMON_ZERO 0)
m= 8 degP= 16  S2=pass  S1=reject (HAS_COMMON_ZERO 0)
m=11 degP= 22  S2=pass  S1=reject (HAS_COMMON_ZERO 0)
m=14 degP= 28  S2=pass  S1=reject (HAS_COMMON_ZERO 0)
```

A common zero `(a,b)` of `(P_x,P_y)` makes the Keller equation read `0 = 1`
there, so each of these `P` has no mate at any degree whatsoever. That is a
complete emptiness statement for the M1 pool, carrier-independent, and it is
the reason no M1 `P` entered the screened-and-passed pipeline. Section 5
records what the exact decision layer says about them on override.

## 4. Screened-and-passed pipeline: per-P verdicts

Every `P` here passed S2 and S1. Order per `P`: SY, then the Q-degree
escalation Y -> C -> W, each decided exactly over `Q`, stopping at the first
stage that yields a mate. Cell format `VERDICT[cert]n=unknowns`, with
`lam` = `lambda_exact`, `rank` = `rank_full_column_exact`, `sol` =
`exact_solution`.

### verdicts

| hash | family | profile | deg P | SY | stage Y | stage C | stage W | outcome | bracket=1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `28072e1d99e9` | HDC | (143,13) | 143 | COORD | MATE[sol]n=857 | - | - | MATE | True |
| `1410212dbd72` | HDC | (132,1) | 132 | COORD | MATE[sol]n=132 | - | - | MATE | True |
| `a10ee6c835f4` | HDC | (132,12) | 132 | COORD | MATE[sol]n=791 | - | - | MATE | True |
| `e97f275c150c` | HDC | (130,1) | 130 | COORD | MATE[sol]n=130 | - | - | MATE | True |
| `b7d738c97e6d` | HDC | (128,1) | 128 | COORD | MATE[sol]n=128 | - | - | MATE | True |
| `f8b3d1bf96f8` | HDC | (126,1) | 126 | COORD | MATE[sol]n=126 | - | - | MATE | True |
| `3e52e6ee53ad` | HDC | (121,11) | 121 | COORD | MATE[sol]n=725 | - | - | MATE | True |
| `c11e0c48a5fc` | HDC | (110,10) | 110 | COORD | MATE[sol]n=659 | - | - | MATE | True |
| `bfd27e14c46e` | V0_A_rand_sparse_lin | (4,-) | 4 | NON-COORD | EMPTY[lam]n=4 | EMPTY[lam]n=11 | EMPTY[lam]n=13 | EMPTY_all_stages_tried | - |
| `14efba30d718` | V0_C_struct_x | (108,-) | 108 | NON-COORD | EMPTY[lam]n=55 | EMPTY[lam]n=121 | EMPTY[lam]n=214 | EMPTY_all_stages_tried | - |
| `393be222c29c` | V0_C_struct_x | (108,-) | 108 | NON-COORD | EMPTY[lam]n=55 | EMPTY[lam]n=123 | EMPTY[lam]n=214 | EMPTY_all_stages_tried | - |
| `682706856007` | V0_C_struct_x | (108,-) | 108 | NON-COORD | EMPTY[lam]n=55 | EMPTY[lam]n=110 | EMPTY[lam]n=214 | EMPTY_all_stages_tried | - |
| `0c061d633814` | V0_C_struct_x | (96,-) | 96 | NON-COORD | EMPTY[lam]n=49 | EMPTY[lam]n=121 | EMPTY[lam]n=190 | EMPTY_all_stages_tried | - |
| `963c989df902` | V0_C_struct_x | (96,-) | 96 | NON-COORD | EMPTY[lam]n=47 | EMPTY[lam]n=113 | EMPTY[lam]n=186 | EMPTY_all_stages_tried | - |
| `2d0d42277f10` | V0_C_struct_x | (84,-) | 84 | NON-COORD | EMPTY[lam]n=43 | EMPTY[lam]n=96 | EMPTY[lam]n=166 | EMPTY_all_stages_tried | - |
| `ad4d9b110acd` | V0_C_struct_x | (9,-) | 9 | NON-COORD | EMPTY[lam]n=6 | EMPTY[lam]n=18 | EMPTY[lam]n=24 | EMPTY_all_stages_tried | - |
| `7d595c3bd034` | V0_C_struct_x | (6,-) | 6 | COORD | MATE[sol]n=6 | - | - | MATE | True |
| `8ba8b61b4912` | V0_C_struct_x | (6,-) | 6 | NON-COORD | EMPTY[lam]n=2 | EMPTY[lam]n=9 | EMPTY[lam]n=9 | EMPTY_all_stages_tried | - |
| `1deacb524623` | V0_C_struct_x | (4,-) | 4 | NON-COORD | EMPTY[lam]n=2 | EMPTY[lam]n=4 | EMPTY[lam]n=4 | EMPTY_all_stages_tried | - |
| `5bf4f9822cd4` | V0_F_coord | (9,-) | 9 | COORD | MATE[sol]n=17 | - | - | MATE | True |
| `693586fd5f7e` | V0_F_coord | (9,-) | 9 | COORD | MATE[sol]n=17 | - | - | MATE | True |
| `d9103ff114e1` | V0_F_coord | (9,-) | 9 | COORD | MATE[sol]n=9 | - | - | MATE | True |
| `2253023eddc1` | V0_F_coord | (6,-) | 6 | COORD | MATE[sol]n=11 | - | - | MATE | True |
| `241c5be4e3a9` | V0_F_coord | (6,-) | 6 | COORD | MATE[sol]n=8 | - | - | MATE | True |
| `40c3553b8128` | V0_F_coord | (6,-) | 6 | COORD | MATE[sol]n=6 | - | - | MATE | True |
| `6df7f7c0a35c` | V0_F_coord | (6,-) | 6 | COORD | MATE[sol]n=8 | - | - | MATE | True |
| `84d01285324b` | V0_F_coord | (6,-) | 6 | COORD | MATE[sol]n=11 | - | - | MATE | True |
| `a4012387e160` | V0_F_coord | (4,-) | 4 | COORD | MATE[sol]n=5 | - | - | MATE | True |
| `eb6976b38508` | V0_F_coord | (4,-) | 4 | COORD | MATE[sol]n=4 | - | - | MATE | True |
| `fbf00970ade6` | V0_F_coord | (4,-) | 4 | COORD | MATE[sol]n=5 | - | - | MATE | True |

Outcome tally: {'MATE': 20, 'EMPTY_all_stages_tried': 10}.

SY x outcome: {('COORDINATE', 'MATE'): 20, ('NON_COORDINATE', 'EMPTY_all_stages_tried'): 10}.

### Mates certified over Q

Each row's `Q` was reconstructed multi-modularly and then certified by
expanding `P_x Q_y - P_y Q_x - 1` coefficientwise over `Q`; the
reconstruction is a heuristic, the expansion is the proof.

| hash | family | deg P | deg Q | divisibility-ordered | [P,Q]-1 = 0 over Q | SY | \|supp Q\| |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `28072e1d99e9` | HDC | 143 | 13 | True | True | COORDINATE | 2 |
| `a10ee6c835f4` | HDC | 132 | 12 | True | True | COORDINATE | 2 |
| `1410212dbd72` | HDC | 132 | 1 | True | True | COORDINATE | 1 |
| `e97f275c150c` | HDC | 130 | 1 | True | True | COORDINATE | 1 |
| `b7d738c97e6d` | HDC | 128 | 1 | True | True | COORDINATE | 1 |
| `f8b3d1bf96f8` | HDC | 126 | 1 | True | True | COORDINATE | 1 |
| `3e52e6ee53ad` | HDC | 121 | 11 | True | True | COORDINATE | 2 |
| `c11e0c48a5fc` | HDC | 110 | 10 | True | True | COORDINATE | 2 |
| `5bf4f9822cd4` | V0_F_coord | 9 | 3 | True | True | COORDINATE | 2 |
| `693586fd5f7e` | V0_F_coord | 9 | 3 | True | True | COORDINATE | 2 |
| `d9103ff114e1` | V0_F_coord | 9 | 1 | True | True | COORDINATE | 1 |
| `7d595c3bd034` | V0_C_struct_x | 6 | 1 | True | True | COORDINATE | 1 |
| `84d01285324b` | V0_F_coord | 6 | 2 | True | True | COORDINATE | 2 |
| `2253023eddc1` | V0_F_coord | 6 | 2 | True | True | COORDINATE | 2 |
| `6df7f7c0a35c` | V0_F_coord | 6 | 3 | True | True | COORDINATE | 2 |
| `241c5be4e3a9` | V0_F_coord | 6 | 3 | True | True | COORDINATE | 2 |
| `40c3553b8128` | V0_F_coord | 6 | 1 | True | True | COORDINATE | 1 |
| `a4012387e160` | V0_F_coord | 4 | 2 | True | True | COORDINATE | 2 |
| `fbf00970ade6` | V0_F_coord | 4 | 2 | True | True | COORDINATE | 2 |
| `eb6976b38508` | V0_F_coord | 4 | 1 | True | True | COORDINATE | 1 |

All 20 verified coefficientwise over Q: True.

## 5. M1 override arm

`m1_run.py`. Every M1/M1L `P` is S1-rejected, so none reaches the pipeline of
section 4. This arm runs them through SY and the exact decision layer anyway,
under an explicit override of the screens -- exactly the route control C-NEG
takes. The S1 rejection already proves emptiness at every degree; what this
arm adds is the carrier-level certificate at each stage of the `mu_3` carrier.
The hit gate stays armed here.

| quantity | value |
| --- | --- |
| P run | 200 |
| SY verdicts | {'NON_COORDINATE': 200} |
| outcomes | {'EMPTY_all_stages_tried': 200} |
| mates | 0 |
| hits | 0 |

By profile:

| profile | n | SY NON_COORDINATE | EMPTY all stages | NOT_CERTIFIED | mates |
| --- | --- | --- | --- | --- | --- |
| M1 (126,189) | 30 | 30 | 30 | 0 | 0 |
| M1 (128,192) | 30 | 30 | 30 | 0 | 0 |
| M1 (130,195) | 30 | 30 | 30 | 0 | 0 |
| M1 (132,198) | 30 | 30 | 30 | 0 | 0 |
| M1L (126,189) | 20 | 20 | 20 | 0 | 0 |
| M1L (128,192) | 20 | 20 | 20 | 0 | 0 |
| M1L (130,195) | 20 | 20 | 20 | 0 | 0 |
| M1L (132,198) | 20 | 20 | 20 | 0 | 0 |

Certificates over all M1 stage evaluations: {('EMPTY_over_Q', 'rank_full_column_exact'): 578, ('EMPTY_over_Q', 'lambda_exact'): 22}.

### first 40 records (all 200 in `m1_records.json` and `V1_RECORDS_M1/`)

| hash | family | profile | deg P | SY | stage Y | stage C | stage W | outcome | bracket=1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `3a10caa740af` | M1 | (128,192) | 128 | NON-COORD | EMPTY[rank]n=1019 | EMPTY[rank]n=1164 | EMPTY[rank]n=687 | EMPTY_all_stages_tried | - |
| `3ae71d521cf2` | M1 | (128,192) | 128 | NON-COORD | EMPTY[rank]n=763 | EMPTY[rank]n=589 | EMPTY[rank]n=1032 | EMPTY_all_stages_tried | - |
| `4f98c90a14e5` | M1 | (128,192) | 128 | NON-COORD | EMPTY[rank]n=766 | EMPTY[rank]n=585 | EMPTY[rank]n=1029 | EMPTY_all_stages_tried | - |
| `696d11fa66fb` | M1 | (128,192) | 128 | NON-COORD | EMPTY[rank]n=1140 | EMPTY[rank]n=881 | EMPTY[rank]n=769 | EMPTY_all_stages_tried | - |
| `7972afa70ca9` | M1 | (128,192) | 128 | NON-COORD | EMPTY[rank]n=1140 | EMPTY[rank]n=881 | EMPTY[rank]n=769 | EMPTY_all_stages_tried | - |
| `9b3c8294cbca` | M1 | (128,192) | 128 | NON-COORD | EMPTY[rank]n=1282 | EMPTY[rank]n=1457 | EMPTY[rank]n=862 | EMPTY_all_stages_tried | - |
| `9f89273e77b0` | M1 | (128,192) | 128 | NON-COORD | EMPTY[rank]n=766 | EMPTY[rank]n=585 | EMPTY[rank]n=1029 | EMPTY_all_stages_tried | - |
| `abf912228e54` | M1 | (128,192) | 128 | NON-COORD | EMPTY[rank]n=1012 | EMPTY[rank]n=782 | EMPTY[rank]n=1371 | EMPTY_all_stages_tried | - |
| `d91f0a35e866` | M1 | (128,192) | 128 | NON-COORD | EMPTY[rank]n=1155 | EMPTY[rank]n=1313 | EMPTY[rank]n=772 | EMPTY_all_stages_tried | - |
| `e65c2b7013d1` | M1 | (128,192) | 128 | NON-COORD | EMPTY[rank]n=766 | EMPTY[rank]n=585 | EMPTY[rank]n=1029 | EMPTY_all_stages_tried | - |
| `238afcc2d1fe` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=1009 | EMPTY[rank]n=1149 | EMPTY[rank]n=668 | EMPTY_all_stages_tried | - |
| `29a7e5b7fa2d` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=940 | EMPTY[rank]n=721 | EMPTY[rank]n=1248 | EMPTY_all_stages_tried | - |
| `32321981b664` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=1063 | EMPTY[rank]n=819 | EMPTY[rank]n=1410 | EMPTY_all_stages_tried | - |
| `32cc359c635c` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=1124 | EMPTY[rank]n=866 | EMPTY[rank]n=1492 | EMPTY_all_stages_tried | - |
| `372ce6b89272` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=940 | EMPTY[rank]n=723 | EMPTY[rank]n=1245 | EMPTY_all_stages_tried | - |
| `384a86ccf404` | M1 | (126,189) | 126 | NON-COORD | EMPTY[lam]n=120 | EMPTY[lam]n=288 | EMPTY[rank]n=499 | EMPTY_all_stages_tried | - |
| `4425d722d5cb` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=937 | EMPTY[rank]n=721 | EMPTY[rank]n=1245 | EMPTY_all_stages_tried | - |
| `4b2a04ad2c2d` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=1063 | EMPTY[rank]n=819 | EMPTY[rank]n=1410 | EMPTY_all_stages_tried | - |
| `50f6f382924b` | M1 | (126,189) | 126 | NON-COORD | EMPTY[lam]n=265 | EMPTY[rank]n=600 | EMPTY[rank]n=1053 | EMPTY_all_stages_tried | - |
| `6172814e299c` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=751 | EMPTY[rank]n=578 | EMPTY[rank]n=997 | EMPTY_all_stages_tried | - |
| `7b784eda6f16` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=884 | EMPTY[rank]n=1006 | EMPTY[rank]n=585 | EMPTY_all_stages_tried | - |
| `856bf513c37f` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=751 | EMPTY[rank]n=578 | EMPTY[rank]n=997 | EMPTY_all_stages_tried | - |
| `8e5e6feaf057` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=1246 | EMPTY[rank]n=946 | EMPTY[rank]n=803 | EMPTY_all_stages_tried | - |
| `8f2c47c74b37` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=751 | EMPTY[rank]n=578 | EMPTY[rank]n=997 | EMPTY_all_stages_tried | - |
| `919a3cb203ce` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=1246 | EMPTY[rank]n=946 | EMPTY[rank]n=803 | EMPTY_all_stages_tried | - |
| `98df01611310` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=1063 | EMPTY[rank]n=817 | EMPTY[rank]n=1412 | EMPTY_all_stages_tried | - |
| `9fb80fd463ee` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=880 | EMPTY[rank]n=999 | EMPTY[rank]n=585 | EMPTY_all_stages_tried | - |
| `a07d5fc1933f` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=379 | EMPTY[rank]n=864 | EMPTY[rank]n=760 | EMPTY_all_stages_tried | - |
| `a64141ef2e54` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=876 | EMPTY[rank]n=674 | EMPTY[rank]n=1163 | EMPTY_all_stages_tried | - |
| `bdf970d43272` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=1246 | EMPTY[rank]n=946 | EMPTY[rank]n=803 | EMPTY_all_stages_tried | - |
| `c00279a4a40a` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=751 | EMPTY[rank]n=578 | EMPTY[rank]n=997 | EMPTY_all_stages_tried | - |
| `c08694448753` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=1384 | EMPTY[rank]n=529 | EMPTY[rank]n=915 | EMPTY_all_stages_tried | - |
| `c7f503d68aa9` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=1384 | EMPTY[rank]n=516 | EMPTY[rank]n=904 | EMPTY_all_stages_tried | - |
| `cd385e5d1fbf` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=1385 | EMPTY[rank]n=531 | EMPTY[rank]n=918 | EMPTY_all_stages_tried | - |
| `d7107cddb129` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=628 | EMPTY[rank]n=1434 | EMPTY[rank]n=1262 | EMPTY_all_stages_tried | - |
| `d7d92cc96981` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=1064 | EMPTY[rank]n=802 | EMPTY[rank]n=1400 | EMPTY_all_stages_tried | - |
| `e55899a67cbe` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=1123 | EMPTY[rank]n=1285 | EMPTY[rank]n=749 | EMPTY_all_stages_tried | - |
| `ebf2e38df467` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=749 | EMPTY[rank]n=578 | EMPTY[rank]n=998 | EMPTY_all_stages_tried | - |
| `f2fa7b4332a8` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=872 | EMPTY[rank]n=674 | EMPTY[rank]n=1162 | EMPTY_all_stages_tried | - |
| `f8992646640a` | M1 | (126,189) | 126 | NON-COORD | EMPTY[rank]n=1136 | EMPTY[rank]n=1292 | EMPTY[rank]n=752 | EMPTY_all_stages_tried | - |

## 5b. Undecided arm (non-M1 S1 timeouts)

`undecided_run.py`. Same override route, for the 13 non-M1 `P` whose S1 timed
out in the screen phase and which therefore carried no verdict at all. These
certificates are carrier-level and independent of S1: they decide the mate
system on the carrier each stage built and nothing beyond it, and they neither
assume nor establish unimodularity of the gradient pair, so they stand
whichever way S1 resolves.

SY verdicts: {'NON_COORDINATE': 13}. Outcomes: {'EMPTY_all_stages_tried': 13}. Certificates: {('EMPTY_over_Q', 'rank_full_column_exact'): 26, ('EMPTY_over_Q', 'lambda_exact'): 13}.

### verdicts

| hash | family | profile | deg P | SY | stage Y | stage C | stage W | outcome | bracket=1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `6b274c42d9fa` | V0_A_rand_sparse_lin | (108,-) | 108 | NON-COORD | EMPTY[rank]n=533 | EMPTY[rank]n=1208 | EMPTY[lam]n=232 | EMPTY_all_stages_tried | - |
| `099afc5c42d1` | V0_A_rand_sparse_lin | (84,-) | 84 | NON-COORD | EMPTY[rank]n=1194 | EMPTY[rank]n=690 | EMPTY[rank]n=1206 | EMPTY_all_stages_tried | - |
| `c2f7d911eb7d` | V0_C_struct_x | (108,-) | 108 | NON-COORD | EMPTY[lam]n=55 | EMPTY[lam]n=130 | EMPTY[lam]n=219 | EMPTY_all_stages_tried | - |
| `353930b6090f` | V0_D_leadsq | (108,-) | 108 | NON-COORD | EMPTY[rank]n=715 | EMPTY[lam]n=191 | EMPTY[lam]n=314 | EMPTY_all_stages_tried | - |
| `4b0168e86ca6` | V0_D_leadsq | (108,-) | 108 | NON-COORD | EMPTY[rank]n=577 | EMPTY[rank]n=1327 | EMPTY[lam]n=258 | EMPTY_all_stages_tried | - |
| `a749e2c23fd8` | V0_D_leadsq | (84,-) | 84 | NON-COORD | EMPTY[rank]n=434 | EMPTY[rank]n=1010 | EMPTY[lam]n=189 | EMPTY_all_stages_tried | - |
| `4bf75e2a6727` | V0_E_leadcube | (126,-) | 126 | NON-COORD | EMPTY[rank]n=1397 | EMPTY[rank]n=353 | EMPTY[rank]n=619 | EMPTY_all_stages_tried | - |
| `e92addca7753` | V0_E_leadcube | (126,-) | 126 | NON-COORD | EMPTY[lam]n=179 | EMPTY[rank]n=406 | EMPTY[rank]n=706 | EMPTY_all_stages_tried | - |
| `47828c7b4cff` | V0_E_leadcube | (108,-) | 108 | NON-COORD | EMPTY[rank]n=1441 | EMPTY[rank]n=826 | EMPTY[rank]n=1453 | EMPTY_all_stages_tried | - |
| `88c4316f3f46` | V0_E_leadcube | (108,-) | 108 | NON-COORD | EMPTY[rank]n=1038 | EMPTY[lam]n=275 | EMPTY[rank]n=461 | EMPTY_all_stages_tried | - |
| `06f912c99bed` | V0_E_leadcube | (96,-) | 96 | NON-COORD | EMPTY[rank]n=686 | EMPTY[lam]n=181 | EMPTY[lam]n=302 | EMPTY_all_stages_tried | - |
| `1cfba17d6930` | V0_E_leadcube | (84,-) | 84 | NON-COORD | EMPTY[rank]n=1396 | EMPTY[rank]n=810 | EMPTY[rank]n=1396 | EMPTY_all_stages_tried | - |
| `5a108b477ba8` | V0_E_leadcube | (84,-) | 84 | NON-COORD | EMPTY[rank]n=471 | EMPTY[rank]n=1092 | EMPTY[lam]n=210 | EMPTY_all_stages_tried | - |

## 6. Certificates emitted

| arm | (verdict, certificate) | count |
| --- | --- | --- |
| pipeline | ('EMPTY_over_Q', 'lambda_exact') | 30 |
| pipeline | ('MATE_over_Q', 'exact_solution') | 20 |
| M1 override | ('EMPTY_over_Q', 'rank_full_column_exact') | 578 |
| M1 override | ('EMPTY_over_Q', 'lambda_exact') | 22 |
| undecided override | ('EMPTY_over_Q', 'rank_full_column_exact') | 26 |
| undecided override | ('EMPTY_over_Q', 'lambda_exact') | 13 |

`NOT_CERTIFIED` records (never reported as emptiness): **0**.

## 7. Mechanics fixed in this run

The mathematical contracts are frozen: the S1/S2/S3 screens, the
Shpilrain-Yu certificate algorithm, and the E1/E2/E3 exact decisions are
untouched. Every change below is mechanics, and each is logged with what it
did and which direction it moves a verdict.

**(F1) `controls_v1.py` had no gate.** It printed its measurements and always
exited 0, so a regression in C-POS, C-NEG or the SY validation set could not
stop a pipeline run, and the brief's hard-gate requirement had nothing to
enforce it. Added `assess()`: 15 named checks with an explicit PASS/FAIL and a
nonzero exit code. It asserts only properties the controls already measured.

**(F2) carrier anchors were being scaled away** (`carriers.carrier` and
`v1.general_carrier`). Both build their polygon by scaling a base point set to
the stage bound, and both put the anchors `(0,0)` and `(0,1)` into that base
*before* scaling. When the stage bound is below the polygon degree -- which is
stage Y for every `P`, and stages Y and C for M1, where `H^3` has degree `3m`
-- the scale factor is `< 1` and `(0,1)` is shrunk below the lattice and
dropped, contradicting each function's own documented contract that `(0,0)`
and `(0,1)` are always retained.

What that did to the verdicts: the Keller row at the constant monomial gets a
contribution from carrier column `a` only when `a = (1,1) - p` for some
`p` in `supp(P)`. For an M1 `P` the linear term `p = (1,0)` gives `a = (0,1)`,
and that is the only column in the `mu_3` grading that can meet the constant
row. With `(0,1)` deleted the whole row was identically zero, so stage Y
returned `EMPTY_over_Q` for every M1 `P` via the degenerate zero-row
`lambda = e_00` certificate. That verdict was true of the carrier actually
built, but vacuous: no `Q` on it could have satisfied the equation.

The fix adjoins the anchors both scaled and unscaled, so the polygon is the
hull of the union. Taking the union rather than replacing matters: when the
stage bound exceeds the polygon degree (stage W) the old scaling inflated the
anchors outward, and simply un-scaling them would have SHRUNK stage W.
Enlarging is the only safe direction, since a larger carrier can only
strengthen an emptiness verdict and can only help a mate be found -- it can
never turn a true emptiness into a false one. Verified superset at every
stage on a sample M1 `P`: `n_raw` Y 882 -> 885, C 2012 -> 2012, W 3541 -> 3541,
with `(0,1)` present at all three.

**(F3) S1 timeouts were undecided and silently dropped.** The screen phase ran
S1 with a 90 s budget under 4-way parallelism. A `timeout` is neither a pass
nor a reject, but `v1.py` selects the pipeline by `passed`, so those `P` fell
out of the run without any recorded verdict. `s1_retry.py` re-runs the same S1
predicate on exactly those `P`, serially and with a long budget, and folds the
resolved verdicts back into `v1_screens.json`.

**(F4) the M1 profiles carried no records.** All 200 M1/M1L `P` are S1-rejected
(section 3), so `v1.py`'s pipeline phase, which is gated on `passed`, ran on
zero of them and the family the brief puts first had no per-P record at all.
`m1_run.py` adds the override arm of section 5. It changes no gate: the S1
rejection stands, the override is explicit and recorded per record
(`screens_overridden`), the records are kept in separate files from the
screened-and-passed arm, and the hit gate stays armed.

**(F5) no independent check on the SY verdicts.** Added `sy_crosscheck.py`
(section 2). It feeds no decision.

