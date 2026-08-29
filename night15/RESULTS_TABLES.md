### 6.1 Screening totals

| quantity | value |
|---|---|
| P generated and certified through the gate | 256 |
| NOT_SCREENED | 3 |
| PERIODS-NONVANISHING | 193 |
| PERIODS-VANISHING | 57 |
| UNRESOLVED | 3 |
| degrees covered | 3 .. 27 |
| deg_y values | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 22, 24, 26, 27] |
| exact Bezout unimodularity, residual 0 | 256 / 256 |
| SY = NON_COORDINATE | 256 |
| independent fibre witness NON_COORDINATE_BY_* | 254 |

### 6.2 Period verdict by instrument

| instrument | NONVANISHING | VANISHING | other |
|---|---|---|---|
| EXACT-G1 | 165 | 53 | 0 |
| EXACT-G1+NUM-MONO(normal form) | 5 | 0 | 0 |
| EXACT-HE | 6 | 0 | 1 |
| NUM-MONO | 17 | 4 | 5 |

### 6.3 Period verdict by species

| species | NONVANISHING | VANISHING | other |
|---|---|---|---|
| G2_multiple_root | 23 | 4 | 6 |
| S1_v_cubic | 43 | 17 | 0 |
| S5_mixed_support | 10 | 9 | 5 |
| v_power_m4 | 40 | 8 | 0 |
| v_power_m5 | 38 | 21 | 0 |
| v_power_m7 | 0 | 3 | 0 |
| v_quadratic | 49 | 4 | 0 |

### 6.3b Species S1..S5 as MEASURED (not as intended)

Each row counts the screened P for which the measurement itself puts the
member in that species.

| species (measured) | count | NONVANISHING | VANISHING | other |
|---|---|---|---|---|
| S1 v-cubic (m = 3) | 69 | 49 | 18 | 2 |
| S2 >= 3 places at infinity | 158 | 121 | 37 | 0 |
| S3 positive genus fibre | 158 | 158 | 0 | 0 |
| S4 fibre with >= 3 components | 36 | 13 | 23 | 0 |
| S5 sheared / mixed support | 24 | 10 | 9 | 5 |
| deg_y >= 3 (not v-quadratic) | 194 | 138 | 51 | 5 |

### 6.4 The (n, m) table for the v-power family G1

Every G1 member with the same `(n, m)` receives the same verdict; the
count is how many corpus members carry that pair.

| n | m | genus | places at infinity | verdict | case | members |
|---|---|---|---|---|---|---|
| 1 | 2 | 0 | 2 | VANISHING | ii | 4 |
| 1 | 3 | 0 | 2 | VANISHING | ii | 5 |
| 1 | 4 | 0 | 2 | VANISHING | ii | 4 |
| 1 | 5 | 0 | 2 | VANISHING | ii | 5 |
| 2 | 2 | 0 | 3 | NONVANISHING | i | 5 |
| 2 | 3 | 0 | 3 | VANISHING | ii | 12 |
| 2 | 4 | 0 | 3 | NONVANISHING | i | 4 |
| 2 | 5 | 0 | 3 | VANISHING | ii | 5 |
| 3 | 2 | 1 | 2 | NONVANISHING | iii | 5 |
| 3 | 3 | 0 | 4 | NONVANISHING | i | 4 |
| 3 | 4 | 0 | 4 | VANISHING | ii | 4 |
| 3 | 5 | 1 | 2 | NONVANISHING | iv | 5 |
| 4 | 2 | 1 | 3 | NONVANISHING | iii | 5 |
| 4 | 3 | 1 | 3 | NONVANISHING | iii | 5 |
| 4 | 4 | 0 | 5 | NONVANISHING | i | 4 |
| 4 | 5 | 0 | 5 | VANISHING | ii | 11 |
| 5 | 2 | 2 | 2 | NONVANISHING | iii | 5 |
| 5 | 3 | 2 | 2 | NONVANISHING | iii | 4 |
| 5 | 4 | 2 | 2 | NONVANISHING | iii | 4 |
| 5 | 5 | 0 | 6 | NONVANISHING | i | 4 |
| 6 | 2 | 2 | 3 | NONVANISHING | iii | 4 |
| 6 | 3 | 1 | 5 | NONVANISHING | iii | 4 |
| 6 | 4 | 1 | 5 | NONVANISHING | iii | 4 |
| 6 | 5 | 2 | 3 | NONVANISHING | iii | 4 |
| 6 | 7 | 0 | 7 | VANISHING | ii | 3 |
| 7 | 2 | 3 | 2 | NONVANISHING | iii | 4 |
| 7 | 3 | 3 | 2 | NONVANISHING | iii | 4 |
| 7 | 4 | 3 | 2 | NONVANISHING | iii | 4 |
| 7 | 5 | 3 | 2 | NONVANISHING | iii | 4 |
| 8 | 2 | 3 | 3 | NONVANISHING | iii | 4 |
| 8 | 3 | 3 | 3 | NONVANISHING | iii | 6 |
| 8 | 4 | 2 | 5 | NONVANISHING | iii | 4 |
| 8 | 5 | 2 | 5 | NONVANISHING | iii | 4 |
| 9 | 2 | 4 | 2 | NONVANISHING | iii | 5 |
| 9 | 3 | 3 | 4 | NONVANISHING | iii | 4 |
| 9 | 4 | 3 | 4 | NONVANISHING | iii | 4 |
| 9 | 5 | 4 | 2 | NONVANISHING | iii | 4 |
| 10 | 2 | 4 | 3 | NONVANISHING | iii | 4 |
| 10 | 3 | 4 | 3 | NONVANISHING | iii | 4 |
| 10 | 4 | 4 | 3 | NONVANISHING | iii | 4 |
| 10 | 5 | 2 | 7 | NONVANISHING | iii | 4 |
| 11 | 2 | 5 | 2 | NONVANISHING | iii | 4 |
| 11 | 3 | 5 | 2 | NONVANISHING | iii | 4 |
| 11 | 4 | 5 | 2 | NONVANISHING | iii | 4 |
| 11 | 5 | 5 | 2 | NONVANISHING | iii | 4 |
| 12 | 2 | 5 | 3 | NONVANISHING | iii | 4 |
| 12 | 3 | 4 | 5 | NONVANISHING | iii | 4 |
| 12 | 4 | 3 | 7 | NONVANISHING | iii | 4 |
| 12 | 5 | 4 | 5 | NONVANISHING | iii | 5 |

### 6.5 Survivors (PERIODS-VANISHING) and their exact mate solve

57 survivors.

| hash | deg P | deg_y | label | mate verdict | stages |
|---|---|---|---|---|---|
| c5e02d711fe5 | 3 | 2 | G1 h0=-3 c=2 a=0 n=1 m=2 t=[(0, Fraction(1,  | EMPTY_all_stages | D=3:EMPTY_over_Q/lambda_exact; D=5:EMPTY_over_Q/lambda_exact; D=6:EMPTY_over_Q/lambda_exact |
| a3b909a78c74 | 3 | 2 | G1 h0=-1 c=1 a=0 n=1 m=2 t=[(0, Fraction(-3, | EMPTY_all_stages | D=3:EMPTY_over_Q/lambda_exact; D=5:EMPTY_over_Q/lambda_exact; D=6:EMPTY_over_Q/lambda_exact |
| 1de9e111cb5d | 3 | 1 | G2 alpha=-1 beta=1 c=3 B=[(Fraction(0, 1), 2 | EMPTY_all_stages | D=3:EMPTY_over_Q/lambda_exact; D=5:EMPTY_over_Q/lambda_exact; D=6:EMPTY_over_Q/lambda_exact |
| 207b968cb4c5 | 4 | 3 | G1 h0=1 c=3 a=0 n=1 m=3 t=[(0, Fraction(-1,  | EMPTY_all_stages | D=4:EMPTY_over_Q/lambda_exact; D=6:EMPTY_over_Q/lambda_exact; D=8:EMPTY_over_Q/lambda_exact |
| 52830078b770 | 4 | 3 | G1 h0=-3 c=2 a=-1 n=1 m=3 t=[(0, Fraction(-1 | EMPTY_all_stages | D=4:EMPTY_over_Q/lambda_exact; D=6:EMPTY_over_Q/lambda_exact; D=8:EMPTY_over_Q/lambda_exact |
| a03f511f7ecd | 5 | 2 | G1 h0=-3 c=-1 a=2 n=1 m=2 t=[(0, Fraction(-3 | EMPTY_all_stages | D=5:EMPTY_over_Q/lambda_exact; D=8:EMPTY_over_Q/lambda_exact; D=10:EMPTY_over_Q/lambda_exact |
| 0a32a1935a5d | 5 | 3 | G1 h0=2 c=2 a=0 n=2 m=3 t=[(0, Fraction(-2,  | EMPTY_all_stages | D=5:EMPTY_over_Q/lambda_exact; D=8:EMPTY_over_Q/lambda_exact; D=10:EMPTY_over_Q/lambda_exact |
| fa25edeecbfe | 5 | 3 | G1 h0=-3 c=1 a=-1 n=2 m=3 t=[(0, Fraction(-2 | EMPTY_all_stages | D=5:EMPTY_over_Q/lambda_exact; D=8:EMPTY_over_Q/lambda_exact; D=10:EMPTY_over_Q/lambda_exact |
| 7f2b3c396f45 | 5 | 4 | G1 h0=-1 c=1 a=2 n=1 m=4 t=[(0, Fraction(2,  | EMPTY_all_stages | D=5:EMPTY_over_Q/lambda_exact; D=8:EMPTY_over_Q/lambda_exact; D=10:EMPTY_over_Q/lambda_exact |
| abc13407cc8e | 5 | 4 | G1 h0=-3 c=2 a=-1 n=1 m=4 t=[(0, Fraction(-1 | EMPTY_all_stages | D=5:EMPTY_over_Q/lambda_exact; D=8:EMPTY_over_Q/lambda_exact; D=10:EMPTY_over_Q/lambda_exact |
| c3dbaae9c4ab | 5 | 1 | G2 alpha=-1 beta=1 c=-1 B=[(Fraction(1, 1),  | EMPTY_all_stages | D=5:EMPTY_over_Q/lambda_exact; D=8:EMPTY_over_Q/lambda_exact; D=10:EMPTY_over_Q/lambda_exact |
| b35d46339ef4 | 5 | 3 | G1 h0=-1 c=1 a=1 n=2 m=3 t=[(0, Fraction(-2, | EMPTY_all_stages | D=5:EMPTY_over_Q/lambda_exact; D=8:EMPTY_over_Q/lambda_exact; D=10:EMPTY_over_Q/lambda_exact |
| d6a8255e8c96 | 5 | 3 | G1 h0=-1 c=1 a=-1 n=2 m=3 t=[(0, Fraction(-3 | EMPTY_all_stages | D=5:EMPTY_over_Q/lambda_exact; D=8:EMPTY_over_Q/lambda_exact; D=10:EMPTY_over_Q/lambda_exact |
| 11b94e5ad1be | 5 | 3 | G1 h0=-1 c=1 a=1 n=2 m=3 t=[(0, Fraction(2,  | EMPTY_all_stages | D=5:EMPTY_over_Q/lambda_exact; D=8:EMPTY_over_Q/lambda_exact; D=10:EMPTY_over_Q/lambda_exact |
| d01448b8b96a | 5 | 3 | G1 h0=-1 c=1 a=1 n=2 m=3 t=[(0, Fraction(-1, | EMPTY_all_stages | D=5:EMPTY_over_Q/lambda_exact; D=8:EMPTY_over_Q/lambda_exact; D=10:EMPTY_over_Q/lambda_exact |
| 7c887944e856 | 5 | 3 | G1 h0=-1 c=1 a=0 n=2 m=3 t=[(0, Fraction(-3, | EMPTY_all_stages | D=5:EMPTY_over_Q/lambda_exact; D=8:EMPTY_over_Q/lambda_exact; D=10:EMPTY_over_Q/lambda_exact |
| 7747339a4408 | 5 | 3 | G1 h0=-1 c=1 a=1 n=2 m=3 t=[(0, Fraction(2,  | EMPTY_all_stages | D=5:EMPTY_over_Q/lambda_exact; D=8:EMPTY_over_Q/lambda_exact; D=10:EMPTY_over_Q/lambda_exact |
| 37670b444e89 | 6 | 5 | G1 h0=-1 c=2 a=0 n=1 m=5 t=[(0, Fraction(1,  | EMPTY_all_stages | D=6:EMPTY_over_Q/lambda_exact; D=9:EMPTY_over_Q/lambda_exact; D=12:EMPTY_over_Q/lambda_exact |
| 00427d4924d2 | 6 | 5 | G1 h0=-1 c=1 a=-1 n=1 m=5 t=[(0, Fraction(-3 | EMPTY_all_stages | D=6:EMPTY_over_Q/lambda_exact; D=9:EMPTY_over_Q/lambda_exact; D=12:EMPTY_over_Q/lambda_exact |
| fef547c2b095 | 7 | 2 | G1 h0=1 c=-1 a=0 n=1 m=2 t=[(0, Fraction(-1, | EMPTY_all_stages | D=7:EMPTY_over_Q/lambda_exact; D=11:EMPTY_over_Q/lambda_exact; D=14:EMPTY_over_Q/lambda_exact |
| 39f56b091e75 | 7 | 3 | G1 h0=-1 c=2 a=0 n=1 m=3 t=[(0, Fraction(-3, | EMPTY_all_stages | D=7:EMPTY_over_Q/lambda_exact; D=11:EMPTY_over_Q/lambda_exact; D=14:EMPTY_over_Q/lambda_exact |
| 7b72f1effa40 | 7 | 4 | G1 h0=-1 c=-1 a=1 n=3 m=4 t=[] | EMPTY_all_stages | D=7:EMPTY_over_Q/lambda_exact; D=11:EMPTY_over_Q/lambda_exact; D=14:EMPTY_over_Q/lambda_exact |
| cd46f9341dc7 | 7 | 4 | G1 h0=2 c=3 a=0 n=3 m=4 t=[(0, Fraction(2, 1 | EMPTY_all_stages | D=7:EMPTY_over_Q/lambda_exact; D=11:EMPTY_over_Q/lambda_exact; D=14:EMPTY_over_Q/lambda_exact |
| 8ccaea9ee461 | 7 | 5 | G1 h0=-1 c=3 a=0 n=2 m=5 t=[(0, Fraction(2,  | EMPTY_all_stages | D=7:EMPTY_over_Q/lambda_exact; D=11:EMPTY_over_Q/lambda_exact; D=14:EMPTY_over_Q/lambda_exact |
| e52860893178 | 7 | 5 | G1 h0=2 c=1 a=2 n=2 m=5 t=[(0, Fraction(2, 1 | EMPTY_all_stages | D=7:EMPTY_over_Q/lambda_exact; D=11:EMPTY_over_Q/lambda_exact; D=14:EMPTY_over_Q/lambda_exact |
| 46a40cb56510 | 7 | 3 | G2 alpha=1 beta=1 c=-1 B=[(Fraction(1, 1), 4 | EMPTY_all_stages | D=7:EMPTY_over_Q/lambda_exact; D=11:EMPTY_over_Q/lambda_exact; D=14:EMPTY_over_Q/lambda_exact |
| 1ef523b227e7 | 8 | 3 | G1 h0=2 c=-2 a=2 n=2 m=3 t=[(0, Fraction(-3, | EMPTY_all_stages | D=8:EMPTY_over_Q/lambda_exact; D=12:EMPTY_over_Q/lambda_exact; D=16:EMPTY_over_Q/lambda_exact |
| ac09181bd1e3 | 8 | 3 | G1 h0=-1 c=1 a=0 n=2 m=3 t=[(0, Fraction(1,  | EMPTY_all_stages | D=8:EMPTY_over_Q/lambda_exact; D=12:EMPTY_over_Q/lambda_exact; D=16:EMPTY_over_Q/lambda_exact |
| 55a9ae0456b4 | 9 | 4 | G1 h0=-1 c=3 a=1 n=1 m=4 t=[(0, Fraction(2,  | EMPTY_all_stages | D=9:EMPTY_over_Q/lambda_exact; D=14:EMPTY_over_Q/lambda_exact; D=18:EMPTY_over_Q/lambda_exact |
| c4e207c544a0 | 9 | 5 | G1 h0=1 c=-2 a=2 n=4 m=5 t=[(0, Fraction(-1, | EMPTY_all_stages | D=9:EMPTY_over_Q/lambda_exact; D=14:EMPTY_over_Q/lambda_exact; D=18:EMPTY_over_Q/lambda_exact |
| e94c47f785e6 | 9 | 5 | G1 h0=2 c=-2 a=2 n=4 m=5 t=[(0, Fraction(-3, | EMPTY_all_stages | D=9:EMPTY_over_Q/lambda_exact; D=14:EMPTY_over_Q/lambda_exact; D=18:EMPTY_over_Q/lambda_exact |
| 808e52fdb1b6 | 9 | 4 | G2 alpha=2 beta=-1 c=-1 B=[(Fraction(0, 1),  | EMPTY_all_stages | D=9:EMPTY_over_Q/lambda_exact; D=14:EMPTY_over_Q/lambda_exact; D=18:EMPTY_over_Q/lambda_exact |
| 83022ceaab23 | 9 | 5 | G1 h0=-1 c=1 a=-1 n=4 m=5 t=[] [S4 intent] | EMPTY_all_stages | D=9:EMPTY_over_Q/lambda_exact; D=14:EMPTY_over_Q/lambda_exact; D=18:EMPTY_over_Q/lambda_exact |
| 40d4c9f57c36 | 9 | 5 | G1 h0=-1 c=1 a=0 n=4 m=5 t=[(0, Fraction(-1, | EMPTY_all_stages | D=9:EMPTY_over_Q/lambda_exact; D=14:EMPTY_over_Q/lambda_exact; D=18:EMPTY_over_Q/lambda_exact |
| 36bc150f8dae | 10 | 3 | G1 h0=2 c=3 a=1 n=1 m=3 t=[(0, Fraction(3, 1 | EMPTY_all_stages | D=10:EMPTY_over_Q/lambda_exact; D=15:EMPTY_over_Q/lambda_exact; D=20:EMPTY_over_Q/lambda_exact |
| b7612f47cd64 | 10 | 10 | G1 h0=2 c=3 a=1 n=1 m=3 t=[(0, Fraction(3, 1 | EMPTY_all_stages | D=10:EMPTY_over_Q/lambda_exact; D=15:EMPTY_over_Q/lambda_exact; D=20:EMPTY_over_Q/lambda_exact |
| a4d6d040e138 | 11 | 3 | G1 h0=2 c=-2 a=0 n=2 m=3 t=[(0, Fraction(2,  | EMPTY_all_stages | D=11:EMPTY_over_Q/lambda_exact; D=17:EMPTY_over_Q/lambda_exact; D=22:EMPTY_over_Q/lambda_exact |
| 3bd161cf7a22 | 11 | 4 | G1 h0=-1 c=2 a=0 n=3 m=4 t=[(0, Fraction(1,  | EMPTY_all_stages | D=11:EMPTY_over_Q/lambda_exact; D=17:EMPTY_over_Q/lambda_exact; D=22:EMPTY_over_Q/lambda_exact |
| c8aa6fd84bbc | 11 | 5 | G1 h0=1 c=-2 a=1 n=1 m=5 t=[(0, Fraction(3,  | EMPTY_all_stages | D=11:EMPTY_over_Q/lambda_exact; D=17:EMPTY_over_Q/lambda_exact; D=22:EMPTY_over_Q/lambda_exact |
| 7887429824c2 | 12 | 5 | G1 h0=-3 c=1 a=-1 n=2 m=5 t=[(1, Fraction(3, | EMPTY_all_stages | D=12:EMPTY_over_Q/lambda_exact; D=18:EMPTY_over_Q/lambda_exact; D=24:EMPTY_over_Q/lambda_exact |
| 632afa8e6433 | 13 | 4 | G1 h0=2 c=3 a=1 n=1 m=4 t=[(0, Fraction(-2,  | EMPTY_all_stages | D=13:EMPTY_over_Q/lambda_exact; D=20:EMPTY_over_Q/lambda_exact; D=26:EMPTY_over_Q/lambda_exact |
| a9b90eff1970 | 13 | 7 | G1 h0=-1 c=1 a=1 n=6 m=7 t=[(0, Fraction(2,  | EMPTY_all_stages | D=13:EMPTY_over_Q/lambda_exact; D=20:EMPTY_over_Q/lambda_exact; D=26:EMPTY_over_Q/lambda_exact |
| 762dac3fbdb1 | 13 | 7 | G1 h0=-1 c=1 a=0 n=6 m=7 t=[(0, Fraction(-3, | EMPTY_all_stages | D=13:EMPTY_over_Q/lambda_exact; D=20:EMPTY_over_Q/lambda_exact; D=26:EMPTY_over_Q/lambda_exact |
| 4667d741b2d6 | 13 | 13 | G1 h0=-1 c=1 a=-1 n=4 m=5 t=[] [S4 intent] | | EMPTY_all_stages | D=13:EMPTY_over_Q/lambda_exact; D=20:EMPTY_over_Q/lambda_exact; D=26:EMPTY_over_Q/lambda_exact |
| 894a95da1a0d | 14 | 5 | G1 h0=-1 c=-2 a=2 n=4 m=5 t=[(0, Fraction(-2 | EMPTY_all_stages | D=14:EMPTY_over_Q/lambda_exact; D=21:EMPTY_over_Q/lambda_exact; D=28:EMPTY_over_Q/lambda_exact |
| c447da45ca02 | 14 | 5 | G1 h0=-1 c=1 a=0 n=4 m=5 t=[(0, Fraction(-2, | EMPTY_all_stages | D=14:EMPTY_over_Q/lambda_exact; D=21:EMPTY_over_Q/lambda_exact; D=28:EMPTY_over_Q/lambda_exact |
| d735085d2c22 | 15 | 4 | G1 h0=1 c=1 a=-1 n=3 m=4 t=[(0, Fraction(1,  | EMPTY_all_stages | D=15:EMPTY_over_Q/lambda_exact; D=23:EMPTY_over_Q/lambda_exact; D=30:EMPTY_over_Q/lambda_exact |
| f406b3aeda22 | 16 | 5 | G1 h0=1 c=-1 a=0 n=1 m=5 t=[(0, Fraction(-1, | EMPTY_all_stages | D=16:EMPTY_over_Q/lambda_exact; D=24:EMPTY_over_Q/lambda_exact; D=32:EMPTY_over_Q/lambda_exact |
| 726da7cd9516 | 17 | 5 | G1 h0=-1 c=-2 a=0 n=2 m=5 t=[(0, Fraction(3, | EMPTY_all_stages | D=17:EMPTY_over_Q/lambda_exact; D=26:EMPTY_over_Q/lambda_exact; D=34:EMPTY_over_Q/lambda_exact |
| 11b99f22adf6 | 18 | 18 | G1 h0=2 c=-2 a=2 n=4 m=5 t=[(0, Fraction(-3, | EMPTY_all_stages | D=18:EMPTY_over_Q/lambda_exact; D=27:EMPTY_over_Q/lambda_exact; D=36:EMPTY_over_Q/lambda_exact |
| d57b38902c84 | 18 | 9 | G1 h0=-1 c=1 a=0 n=4 m=5 t=[(0, Fraction(-1, | EMPTY_all_stages | D=18:EMPTY_over_Q/lambda_exact; D=27:EMPTY_over_Q/lambda_exact; D=36:EMPTY_over_Q/lambda_exact |
| c689ce7fc834 | 18 | 18 | G1 h0=2 c=-2 a=2 n=4 m=5 t=[(0, Fraction(-3, | EMPTY_all_stages | D=18:EMPTY_over_Q/lambda_exact; D=27:EMPTY_over_Q/lambda_exact; D=36:EMPTY_over_Q/lambda_exact |
| 1f53638e8cf6 | 19 | 5 | G1 h0=-3 c=3 a=1 n=4 m=5 t=[(0, Fraction(-2, | EMPTY_all_stages | D=19:EMPTY_over_Q/lambda_exact; D=29:EMPTY_over_Q/lambda_exact; D=38:EMPTY_over_Q/lambda_exact |
| a814ad47ed0c | 20 | 7 | G1 h0=-1 c=1 a=0 n=6 m=7 t=[(0, Fraction(3,  | EMPTY_all_stages | D=20:EMPTY_over_Q/lambda_exact; D=30:EMPTY_over_Q/lambda_exact; D=40:EMPTY_over_Q/lambda_exact |
| cf1c601f3d1c | 20 | 10 | G1 h0=-3 c=1 a=-1 n=2 m=3 t=[(0, Fraction(-2 | EMPTY_all_stages | D=20:EMPTY_over_Q/lambda_exact; D=30:EMPTY_over_Q/lambda_exact; D=40:EMPTY_over_Q/lambda_exact |
| 96e4a2c6d1d3 | 24 | 12 | G1 h0=-1 c=1 a=-1 n=1 m=5 t=[(0, Fraction(-3 | NOT_CERTIFIED | D=24:EMPTY_over_Q/lambda_exact; D=36:EMPTY_over_Q/lambda_exact; D=48:NOT_CERTIFIED/none |
| 282a9f40c368 | 24 | 24 | G1 h0=-3 c=1 a=-1 n=2 m=5 t=[(1, Fraction(3, | NOT_CERTIFIED | D=24:EMPTY_over_Q/lambda_exact; D=36:EMPTY_over_Q/lambda_exact; D=48:NOT_CERTIFIED/none |

mate verdicts: {'EMPTY_all_stages': 55, 'NOT_CERTIFIED': 2}

