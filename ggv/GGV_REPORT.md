# GGV B=16 evidence campaign -- run record


Data only: what ran, on which artifact, its verdict class, its exit status and its peak resident set size. No interpretation of the recorded values appears in this file.


Engines: msolve 0.10.1 (built from source per the campaign tooling contract), Singular 4.3.2, sympy 1.14.0. Primes used: 1000003, 1000033, 1000039 (all 1 mod 3). System builder: `wave5/w5_b16_abel.py::build_system`, charts: `wave5/w5_b16_reduce.py::reduced_charts`, writer: `wave5/w5_b16_reduce.py::to_ms`. No equations were re-derived.


## Gate (run before every computation)

| result | check | recorded detail |
|---|---|---|
| PASS | GATE-1 w5_b16_abel.py prints ALL PASS | exit=0 |
| PASS | GATE-2 d=5 chart A p=1000003 re-solves to EMPTY | verdict=EMPTY exit=0 rss_kb=31568 wall=0.8s out_bytes=6 |
| PASS | GATE-2 d=5 chart B p=1000003 re-solves to EMPTY | verdict=EMPTY exit=0 rss_kb=5584 wall=0.01s out_bytes=6 |
| PASS | GATE-3 negative control: zero-dimensional ideal is NOT classified EMPTY | verdict=CANDIDATE-UNVERIFIED out_bytes=106 |
| PASS | GATE-3 negative control: 0-byte artifact is NOT classified EMPTY | verdict=NO-OUTPUT bytes=0 |
| PASS | GATE-3 positive control: a literal [-1]: artifact IS classified EMPTY | verdict=EMPTY |

Artifact: `ggv/logs/GATE.log`


## G1 ladder

No `ggv/ladder.tsv` present.


### G1 inputs as generated

| d | chart | #eqs | #vars | bytes (p=1000003) | rows written | gen (s) |
|---|---|---|---|---|---|---|
| 8 | A | 32 | 24 | 12068 | 32 | 4.26 |
| 8 | B | 32 | 23 | 10657 | 32 | 4.26 |
| 9 | A | 36 | 27 | 17455 | 36 | 5.99 |
| 9 | B | 36 | 26 | 15622 | 36 | 5.99 |
| 10 | A | 40 | 30 | 24353 | 40 | 8.78 |
| 10 | B | 40 | 29 | 22029 | 40 | 8.78 |
| 11 | A | 44 | 33 | 33544 | 44 | 11.06 |
| 11 | B | 44 | 32 | 30649 | 44 | 11.06 |
| 12 | A | 48 | 36 | 44974 | 48 | 13.99 |
| 12 | B | 48 | 35 | 41431 | 48 | 13.99 |


## G2 -- mu-eliminants, chart A (mu2 = 1): constraints on (mu0, mu3)

No eliminant artifacts present.


## G3 -- mu-eliminants, chart B (mu2 = 0, mu3 = 1): constraints on mu0

No eliminant artifacts present.


## G4 -- descent-recursion data table, d = 3..10 (no solving)

| d | polynomial satisfied by a_{2d} | discriminant | roots (data) | row1 next unknown | row1 linear coeff | row2 next unknown | row2 linear coeff |
|---|---|---|---|---|---|---|---|
| 3 | `-18*a6**2 - 3*a6 + 3/8` | `36` | `-1/4; 1/12` | a5 | `-32*a6 - 3` | a4 | `-28*a6 - 3` |
| 4 | `-26*a8**2 - 3*a8 + 3/8` | `48` | `-3/52 + sqrt(3)/13; -sqrt(3)/13 - 3/52` | a7 | `-48*a8 - 3` | a6 | `-44*a8 - 3` |
| 5 | `-34*a10**2 - 3*a10 + 3/8` | `60` | `-3/68 + sqrt(15)/34; -sqrt(15)/34 - 3/68` | a9 | `-64*a10 - 3` | a8 | `-60*a10 - 3` |
| 6 | `-42*a12**2 - 3*a12 + 3/8` | `72` | `-1/28 + sqrt(2)/14; -sqrt(2)/14 - 1/28` | a11 | `-80*a12 - 3` | a10 | `-76*a12 - 3` |
| 7 | `-50*a14**2 - 3*a14 + 3/8` | `84` | `-3/100 + sqrt(21)/50; -sqrt(21)/50 - 3/100` | a13 | `-96*a14 - 3` | a12 | `-92*a14 - 3` |
| 8 | `-58*a16**2 - 3*a16 + 3/8` | `96` | `-3/116 + sqrt(6)/29; -sqrt(6)/29 - 3/116` | a15 | `-112*a16 - 3` | a14 | `-108*a16 - 3` |
| 9 | `-66*a18**2 - 3*a18 + 3/8` | `108` | `-1/44 + sqrt(3)/22; -sqrt(3)/22 - 1/44` | a17 | `-128*a18 - 3` | a16 | `-124*a18 - 3` |
| 10 | `-74*a20**2 - 3*a20 + 3/8` | `120` | `-3/148 + sqrt(30)/74; -sqrt(30)/74 - 3/148` | a19 | `-144*a20 - 3` | a18 | `-140*a20 - 3` |

### Controls

| result | check | recorded detail |
|---|---|---|
| PASS | d=3 row0 involves a_6 and no other unknown | others=[] |
| PASS | d=3 row1 is degree 1 in a_5 | deg=1 |
| PASS | d=3 row2 is degree 1 in a_4 | deg=1 |
| PASS | d=3 row1 round-trip: r1 - c1*a_5 is free of a_5 |  |
| PASS | d=3 row2 round-trip: r2 - c2*a_4 is free of a_4 |  |
| PASS | d=3 NEGATIVE CONTROL: perturbed row0 changes the a_6 polynomial |  |
| PASS | d=3 NEGATIVE CONTROL: perturbed row0 changes the discriminant | delta=72 |
| PASS | d=4 row0 involves a_8 and no other unknown | others=[] |
| PASS | d=4 row1 is degree 1 in a_7 | deg=1 |
| PASS | d=4 row2 is degree 1 in a_6 | deg=1 |
| PASS | d=4 row1 round-trip: r1 - c1*a_7 is free of a_7 |  |
| PASS | d=4 row2 round-trip: r2 - c2*a_6 is free of a_6 |  |
| PASS | d=4 NEGATIVE CONTROL: perturbed row0 changes the a_8 polynomial |  |
| PASS | d=4 NEGATIVE CONTROL: perturbed row0 changes the discriminant | delta=104 |
| PASS | d=5 row0 involves a_10 and no other unknown | others=[] |
| PASS | d=5 row1 is degree 1 in a_9 | deg=1 |
| PASS | d=5 row2 is degree 1 in a_8 | deg=1 |
| PASS | d=5 row1 round-trip: r1 - c1*a_9 is free of a_9 |  |
| PASS | d=5 row2 round-trip: r2 - c2*a_8 is free of a_8 |  |
| PASS | d=5 NEGATIVE CONTROL: perturbed row0 changes the a_10 polynomial |  |
| PASS | d=5 NEGATIVE CONTROL: perturbed row0 changes the discriminant | delta=136 |
| PASS | d=6 row0 involves a_12 and no other unknown | others=[] |
| PASS | d=6 row1 is degree 1 in a_11 | deg=1 |
| PASS | d=6 row2 is degree 1 in a_10 | deg=1 |
| PASS | d=6 row1 round-trip: r1 - c1*a_11 is free of a_11 |  |
| PASS | d=6 row2 round-trip: r2 - c2*a_10 is free of a_10 |  |
| PASS | d=6 NEGATIVE CONTROL: perturbed row0 changes the a_12 polynomial |  |
| PASS | d=6 NEGATIVE CONTROL: perturbed row0 changes the discriminant | delta=168 |
| PASS | d=7 row0 involves a_14 and no other unknown | others=[] |
| PASS | d=7 row1 is degree 1 in a_13 | deg=1 |
| PASS | d=7 row2 is degree 1 in a_12 | deg=1 |
| PASS | d=7 row1 round-trip: r1 - c1*a_13 is free of a_13 |  |
| PASS | d=7 row2 round-trip: r2 - c2*a_12 is free of a_12 |  |
| PASS | d=7 NEGATIVE CONTROL: perturbed row0 changes the a_14 polynomial |  |
| PASS | d=7 NEGATIVE CONTROL: perturbed row0 changes the discriminant | delta=200 |
| PASS | d=8 row0 involves a_16 and no other unknown | others=[] |
| PASS | d=8 row1 is degree 1 in a_15 | deg=1 |
| PASS | d=8 row2 is degree 1 in a_14 | deg=1 |
| PASS | d=8 row1 round-trip: r1 - c1*a_15 is free of a_15 |  |
| PASS | d=8 row2 round-trip: r2 - c2*a_14 is free of a_14 |  |
| PASS | d=8 NEGATIVE CONTROL: perturbed row0 changes the a_16 polynomial |  |
| PASS | d=8 NEGATIVE CONTROL: perturbed row0 changes the discriminant | delta=232 |
| PASS | d=9 row0 involves a_18 and no other unknown | others=[] |
| PASS | d=9 row1 is degree 1 in a_17 | deg=1 |
| PASS | d=9 row2 is degree 1 in a_16 | deg=1 |
| PASS | d=9 row1 round-trip: r1 - c1*a_17 is free of a_17 |  |
| PASS | d=9 row2 round-trip: r2 - c2*a_16 is free of a_16 |  |
| PASS | d=9 NEGATIVE CONTROL: perturbed row0 changes the a_18 polynomial |  |
| PASS | d=9 NEGATIVE CONTROL: perturbed row0 changes the discriminant | delta=264 |
| PASS | d=10 row0 involves a_20 and no other unknown | others=[] |
| PASS | d=10 row1 is degree 1 in a_19 | deg=1 |
| PASS | d=10 row2 is degree 1 in a_18 | deg=1 |
| PASS | d=10 row1 round-trip: r1 - c1*a_19 is free of a_19 |  |
| PASS | d=10 row2 round-trip: r2 - c2*a_18 is free of a_18 |  |
| PASS | d=10 NEGATIVE CONTROL: perturbed row0 changes the a_20 polynomial |  |
| PASS | d=10 NEGATIVE CONTROL: perturbed row0 changes the discriminant | delta=296 |
| PASS | d=5 control: the recorded a_10 polynomial has at least one root recorded | {'-sqrt(15)/34 - 3/68': 1, '-3/68 + sqrt(15)/34': 1} |

Full rows (each row's complete polynomial and full linear part): `ggv/recursion_table.json`


## G5

No G5 artifacts present.

