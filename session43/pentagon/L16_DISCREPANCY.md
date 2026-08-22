# The level-16 discrepancy, localised to one rational number

## Setting

Codex's explicit branch-1 witness (`codex/pentagon-level16-exact`, `2ba8e30`):

    c0 = c1 = lambda = 1 ,  kappa = eta = 0
    h_8 = z^8 , h_7 = z^8 , h_6 = z^8 , h_5 = z^7 , g_12 = z^12
    g_11 = (3/2) z^12 + (1/8) z^11        [matches MY independent level-19 result]

In my s-ladder this witness gives residual **exactly 0** at levels 19, 18 and 17,
and fails at level 16.

## The obstruction is the z^19 coefficient, and it has no unknowns

Only two pairs of level 16 reach degree 19:

    (6,10):  10 h_6' g_10 - 6 h_6 g_10'    ->  7+12 = 19,  8+11 = 19
    (7, 9):   9 h_7' g_9  - 7 h_7 g_9'     ->  7+12 = 19,  8+11 = 19

`(8,8)` tops out at 18, `(5,11)` at 18, `(4,12)` at 17.  So the new unknowns
`g_8` and `h_4` cannot reach `z^19`, and neither can the carried kernels
`kappa, eta` (they enter at `z^17` and `z^16`) — checked by including them as
unknowns explicitly.

## The forced reconstructions, each confirmed by hand

**`g_10`'s `z^12` coefficient**, from level 18's own `z^19` coefficient:

    (8,10): 10*8z^7*G12 z^12 - 8*z^8*12 G12 z^11 = (80 - 96) G12 = -16 G12
    (7,11): 11*8z^7*(3/2)z^12 - 7*z^8*18 z^11    = 132 - 126 = 6
    (6,12): 12*8z^7*z^12      - 6*z^8*12 z^11    = 96 - 72   = 24
    => -16 G12 + 30 = 0  =>  **G12 = 15/8**

**`g_9`'s `z^12` coefficient**, from level 17's `z^19` coefficient:

    (8, 9):  -24 G9
    (7,10):  150 - 157.5 = -15/2
    (6,11):  132 - 108   = 24
    (5,12):  contributes only at z^18
    => -24 G9 - 15/2 + 24 = 0  =>  **G9 = 11/16**

## The number

    10 * 8z^7 * (15/8)z^12  =  150
    -6 * z^8  * (45/2)z^11  = -135
     9 * 8z^7 * (11/16)z^12 =  +99/2
    -7 * z^8  * (33/4)z^11  = -231/4
    -------------------------------------
                              **27/4**

Confirmed by sympy coefficient extraction and by the hand sum above.  `27/4 != 0`.

## Status of the disagreement

**Not** a claim that Codex is wrong.  I retracted OPUS43-020 for making exactly
that mistake on an instrument that failed its control (ERRATA A20).  What is
different here:

* his `g_11` matches my independent level-19 derivation coefficient for coefficient;
* his witness clears levels 19, 18, 17 with residual exactly 0 — three passing
  controls on the very code path that then reports 16;
* the failing coefficient is a four-term sum I have now checked three ways.

Sent as OPUS43-023 with my full `g_10`, `g_9` and level-16 pair list.  One of us
has an arithmetic slip in a four-term sum, and one exchange should settle it.

## Consequence if I am right

Branch 1 would be dead and level 16 would reduce to Codex's **branch 2**
(`lambda = 0`, `h_6` matched to `(h_7/z^4)^2/(4c_0)`).  That is a *narrowing*, not
an emptiness result — and it must not be asserted until the discrepancy is
resolved.

Pentagon: **NO VERDICT**.
