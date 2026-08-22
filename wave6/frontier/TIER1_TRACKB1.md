# Tier 1: trackB1 over Q — NO VERDICT, and why

`trackB1_sat_p1000003.ms` (166 var / 284 eq, saturated on `c_1_0, c_8_14,
d_12_21, s_4_8`) is the one target where **NONEMPTY would mean a counterexample
candidate**: a solution is an admissible point of pentagon case (1).

## Result

    leaves: 2   EMPTY=1   NONEMPTY=0   NOVERDICT=1
    unresolved leaf: c_1_0!=0;  281 eq / 163 vars  (both engines: no verdict)
    VERDICT: NO VERDICT

The branch did exactly what was predicted: `c_1_0 = 0` dies **instantly** against
the saturation row `zsat·c_1_0·c_8_14·d_12_21·s_4_8 − 1`, which is a clean
confirmation that the saturation is doing its job. But the surviving branch is
281 equations in 163 variables — against a root of 284 in 166. Branching bought
**3 variables.**

## Why branching fails here, stated as a rule

trackB1 has only **2 single-monomial equations, and both involve `c_1_0`**:

    c_1_0 · d_0_1 = 0        c_1_0 · d_1_1 = 0

So one split exhausts the entire monomial structure and the tree is one node
deep. Compare the h-branch frontier: 6 monomial equations over 8 variables with
`c_46` in four of them, which collapsed into 15 easy leaves.

>  **Branching converts a wall into progress in proportion to the number of
>  *independent* monomial equations. One shared pivot variable gives one split,
>  and one split gives nothing.**

That is the second clean demonstration of the method's boundary tonight (the
first being the (9,27) systems), and it is worth more than another win: it says
when *not* to reach for it.

## What replaces it

Reduce harder before branching. The exact ℚ forced chain reaches **81 variables**
on this system; the char-0 exporter had capped at 119 on a 60 000-term budget.
The cap is now 900 000 and the deeper export is rebuilding. 81 variables is
inside the range where `slimgb` has been finishing in seconds all night, so the
reduction — not the solver, and not the branching — is the lever here.
