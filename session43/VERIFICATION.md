# Verification sweep — every theorem re-checked against an independent source

All of tonight's theorems were derived from **my** reconstruction of the
pentagon's Newton-polygon supports.  Codex's `p11zero_full_sat_p1000003.ms`
(branch `codex/pentagon-p11-zero-search`, 186 vars / 306 equations, degree 2) was
built **independently from the bracket**.  Testing the theorems against his
equations is therefore a genuine cross-check rather than a restatement.

## V1 — the w-grading is real, and it is his equations that say so

Grading `w(x^i y^j) = j - i`, every term `p_{j,i} q_{j',k}` of the bracket lands
on `x^(i+k-1) y^(j+j'-1)`, so its `w` is `(j-i) + (j'-k)`.  An equation is
`w`-homogeneous iff the grading is genuine.

First pass reported **114 of 299 non-homogeneous — FAIL**.  That was my parser,
not the grading: Codex's export substitutes the gauges `p_0_1 = 1` and
`q_1_2 = 1`, so those factors are **invisible in the text** and each carries
`w = -1`.  Crediting `-1` per elided factor:

    **0 non-homogeneous out of 299.  PASS.**

## V2 — per-level equation counts, two independent reconstructions

| level | Codex | mine | | level | Codex | mine |
| --- | --- | --- | --- | --- | --- | --- |
| 20 | 19 | 19 | | 9 | 14 | 14 |
| 19 | 20 | 20 | | 8 | 13 | 13 |
| 18 | 20 | 20 | | 7 | 12 | 12 |
| 17 | 20 | 20 | | 6 | 11 | 11 |
| 16 | 20 | 20 | | 5 | 10 | 10 |
| 15 | 19 | 19 | | 4 | 9 | 9 |
| 14 | 19 | 19 | | 3 | 8 | 8 |
| 13 | 18 | 18 | | 2 | 7 | 7 |
| 12 | 17 | 17 | | 1 | 6 | 6 |
| 11 | 16 | 16 | | 0 | **4** | **5** |
| 10 | 15 | 15 | | -1 | **2** | **3** |

**Levels 20 through 1 agree exactly.**  Levels 0 and -1 differ by one each,
totalling 299 against my 301 — and the difference is fully explained, not waved
away: Codex's variable list contains **neither `p_1_1` nor `q_1_1`**, because his
branch is the `p_1_1 = 0` chart and `q_1_1` is eliminated with it.  My cascade is
the general chart.  Those two variables appear only at levels 0 and -1, which is
exactly where the counts differ, and nowhere else — which is exactly what the
table shows.  (`p_0_1` and `q_1_2` are likewise absent, being gauged to 1,
confirming the elided-factor correction of V1 from a second direction.)

## V3 — the theorems, tested on his level-20 block

Random points over `F_p`, five trials each:

| check | result |
| --- | --- |
| upper-edge family `A = c0 G^2`, `Qh = c1 G^3` satisfies level 20 | **95/95 vanish — PASS** |
| eighth-power family `A = c0 (t-tau)^8`, `Qh = c1 (t-tau)^12` | **95/95 vanish — PASS** |
| NEGATIVE: generic `A`, `Qh` | **0/95 vanish — PASS** |
| NEGATIVE: eighth-power family against level **19** | **0/100 vanish — PASS** |

The last one matters: it shows the top block is not accidentally satisfied by
everything, and that the eighth-power family does not trivially solve the next
level down.

## What this establishes, and what it does not

**Established.**  The block-triangular w-structure, the per-level equation
counts, and the upper-edge and eighth-power families are all confirmed against a
second, independently constructed statement of the same problem.  The one
disagreement is a scope difference (general chart vs `p_1_1 = 0`) that predicts
its own location exactly.

**Not established.**  None of this decides the pentagon.  These verify that the
theorems are true consequences of the bracket; they say nothing about whether a
point satisfying *all* levels exists.  Pentagon: **NO VERDICT**.

## Reproduction

    python3 session43/pentagon/verify_all.py     # needs /tmp/red/full_sat.ms,
    # i.e. git cat-file -p origin/codex/pentagon-p11-zero-search:codex_p11zero/p11zero_full_sat_p1000003.ms
