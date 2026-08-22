# Target queue, ranked — hunting a NONEMPTY

## Why this order

**A NONEMPTY on trackB1 is immediately meaningful and nothing else here is.**
`trackB1_sat_p1000003.ms` is pentagon case (1), unpinned, saturated on all four
nondegeneracy conditions `c_1_0, c_8_14, d_12_21, s_4_8`. A solution of *that*
system is an admissible point of case (1) — a counterexample candidate. Every
other target below is ground-clearing by comparison.

| tier | target | why |
|---|---|---|
| **1** | `trackB1_sat_p1000003.ms` (166 var / 284 eq) | NONEMPTY = counterexample candidate |
| **2** | `p108_525122` surviving leaves | 3 of 5 already EMPTY; only 2 leaves left, closest to the main line |
| **3** | 13 sweep NO-VERDICT cells | ranked below |

## The composed pipeline

Leaves now run **branch -> forced chain -> slimgb -> msolve**:

1. **branch** on monomial equations `uv = 0` — shrinks the *case space*;
2. **forced chain** — exact substitutions, shrinks the *system*;
3. **slimgb**, then **msolve** if it stalls — two independent engines.

Every step is an exact implication, so an EMPTY downstream still proves the leaf
empty. Only what survives all four reaches a verdict.

trackB1 is a good fit for step 1: it carries `c_1_0·d_0_1 = 0` and
`c_1_0·d_1_1 = 0`, and `c_1_0` is saturated nonzero — so the `c_1_0 = 0` branch
dies instantly against the saturation row, and the surviving branch *forces*
`d_0_1 = d_1_1 = 0`.

## Tier 3, ranked by proximity then residual size

| rank | cell | size |
|---|---|---|
| 1 | `wave5/ms/m16_d6_p1000003.ms` | 17v / 22eq |
| 2 | `wave5/ms/m16_d7_p1000033.ms` | 20v / 26eq |
| 3 | `wave5/ms2/b16r_d5_A_q.ms` | 15v / 20eq (char 0) |
| 4 | `wave5/ms2/b16r_d6_A_q.ms` | 18v / 24eq (char 0) |
| 5 | `wave5/ms2/b16r_d7_A_q.ms` | 21v / 28eq (char 0) |
| 6 | `wave5/ms/u16_d7_q.ms` | 19v / 25eq (char 0) |
| 7–8 | `wave4/artifacts/{c2_w4_one_real,probe_w4m4_real}_p1000003.ms` | 20v / 19eq |

**Excluded deliberately:** the 14 `bottomedge/be_*` cells. They are NO VERDICT
only because they are *nonempty and slow* — each has 5 F_p-rational seeds and a
degree-9 eliminant. Listing them as leads would be counting known results as
discoveries.

`campaign/d23_borisov/sf_h_system.ms` also appears as NO VERDICT in the sweep
(90 s budget) but has since been decided separately: **NONEMPTY, dim 0,
vdim 14** — see `SF_TARGET_RESOLVED.md`.
