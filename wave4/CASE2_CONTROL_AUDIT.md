# Case (2) at p = 1000003: the EMPTY verdict's own control never completed

## What the artifacts say

`wave4/artifacts/c2_full_results.json` records exactly two runs at p = 1000003
on the case-(2) system (`trackA_system_case2.json`, chart `d_3_3 = 1`):

| run | polys | vars | out_bytes | planted point? |
|---|---|---|---|---|
| `full_one_pin_p1000003` | 98 | 71 | **6** → `[-1]` EMPTY | no |
| `full_one_mutant_p1000003` | 96 | 71 | **0** | **yes** |

The "mutant" run is the **P-POS control**: the same system with a solution
planted, so that a solver which cannot find it has no authority over the
"pin" run's EMPTY. Its output is **0 bytes** at a peak RSS of 3.9 GB — a memory
failure, which by the campaign's own standing rule is **NO VERDICT**.

>  **So the EMPTY was accepted while the control that was supposed to validate
>  it did not complete.**

This is not a criticism of the conclusion — case (2) is separately certified
EMPTY at 65521, 32003 and 65537 — but the p = 1000003 leg is unsupported, and
the control was *built and run and failed*, which is the specific situation the
campaign's corrections 5–7 exist to catch.

## The plant is real — verified here, without any solver

The recorded planted point covers 72 variables but omits `sat`, the
Rabinowitsch variable. Solving the saturation row (equation 93,
`c_1_0·c_8_14·c_8_16·d_12_21·d_12_24·d_2_1·sat − 1`) for it gives
`sat = 666673`, and then

>  **the planted point satisfies 96 of 96 equations.**

So `c2_full_one_mutant_p1000003.ms` is **NONEMPTY by construction**, and any run
of it returning EMPTY or no-verdict is a failed control, not a result. Checked
by direct evaluation — no Gröbner engine involved.

(My first pass reported 95/96 because I had not supplied `sat`. Same shape as
the `−p0·r0·t−1` sign slip earlier tonight: when a saturated system looks one
equation short of satisfied, the missing equation is almost always the
saturation row and the fault is almost always mine.)

## Status

Singular `slimgb` is being run on the mutant system now — the engine the
campaign never pointed at it. If it recovers the plant, the control passes and
the p = 1000003 EMPTY becomes supported. If it cannot, that leg stays
unvalidated and should be labelled as such rather than counted among the three
certified primes.
