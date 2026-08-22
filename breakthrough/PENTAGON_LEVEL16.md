# Pentagon level 16: the quick multiplicity wall breaks

## Verdict

**NO VERDICT** for the pentagon.  Level 16 is not equivalent to
`(s-tau)^6 | h_7`, so the proposed level 16/15/14 quick kill path does not
continue.

Put `z=s-tau` and retain the complete level-17 family:

    h_7 = z^4(a_0+a_1z+...+a_4z^4),
    h_6 = b_0+b_1z+...+b_8z^8,
    g_11 = (3c_1/2c_0)z^4h_7 + (lambda/8c_0)z^11.

In the vertex chart `c_0 c_1 != 0`, complete level 16 is solvable if and only if

    F_0 := a_0^2-4c_0b_0 = 0,
    F_1 := a_0a_1-2c_0b_1 = 0,
    a_0^3 lambda = 0.                                  (1)

Equivalently, it is the union of two branches:

* `a_0=0`, `b_0=b_1=0` (so `z^5|h_7` and `z^2|h_6`); or
* `lambda=0`, with the constant and linear coefficients of `h_6` equal to
  those of `(h_7/z^4)^2/(4c_0)`.

This is a joint condition on `h_7`, `h_6`, and the level-19 kernel constant.
It neither forces `z^6|h_7` nor creates an emptiness result.

## Independent diagonal derivation

The level-18 equation is inverted with `D_10(f)=10f-zf'`, retaining
`kappa z^10`.  The level-17 equation is then inverted with `D_9`, retaining its
kernel.  Crucially, the complete level-17 unknown is

    W_9 = g_9-(3c_1/2c_0)z^4h_5,

not `g_9` alone.  Thus `h_5` remains arbitrary and
`g_9=W_9+(3c_1/2c_0)z^4h_5`.  Dropping this coupling manufactures a false
level-16 resonant obstruction.

After substituting the complete solution, the carried level-16 term is

    K_16 = <h_7,g_9>_(7,9)+<h_6,g_10>_(6,10)+<h_5,g_11>_(5,11).

The new `h_4,g_8` terms are divisible by `z^7`, so the first gate is
`z^7|K_16`.  Its coefficients below degree seven are zero through degree two,
then have the triangular form

    [z^3]K_16 = -9c_1 F_0^2/(4c_0^3),
    [z^4]K_16 = -33c_1 F_0F_1/(4c_0^3),
    [z^5]K_16 mod F_0 = -15c_1 F_1^2/(2c_0^3),
    [z^6]K_16 mod (F_0,F_1) = -693a_0^3lambda/(1024c_0^3).

Because `c_0c_1` is nonzero, these equations are set-theoretically equivalent
to (1).  Conversely, direct substitution of either branch makes every low
coefficient vanish.

There is no second obstruction.  At level 16 the complete new unknown is

    W_8 = g_8-(3c_1/2c_0)z^4h_4.

After division by `8c_0z^7`, the `z^8` resonant coefficient of its `D_8`
equation vanishes on both branches of (1), and coefficientwise inversion
reconstructs `W_8` with its kernel constant retained.

## Sharpness and scope

The displayed triangular coefficients show sharpness: violating `F_0` already
fails at degree three; after `F_0=0`, violating `F_1` fails at degree five; and
after both matching equations, `a_0lambda != 0` fails at degree six.  Conditions
on `h_7` alone cannot describe level 16.

The derivation assumes the same vertex-saturated support, exact edge degrees,
nonzero `c_0,c_1`, characteristic zero, and validity of the one-variable
pentagon ladder used at level 17.  Vanishing endpoints, lower-degree residual
edges, or a different exposed Newton face remain separate strata.  Therefore
this result cannot support `EMPTY`; it only replaces the proposed multiplicity
wall by the exact branching condition (1).

`pentagon_level16.py` verifies every formula symbolically, retains all three
kernel constants, checks both branches, checks the `D_8` resonance, and
reconstructs a complete level-16 solution.

It also supplies a concrete characteristic-zero witness for the potentially
rank-dropping first branch: `c_0=c_1=lambda=1`, `a_4=b_8=d_7=1`, with every
other `a_i,b_i,d_i` and both earlier kernel constants zero.  Thus
`h_7=z^8,h_6=z^8,h_5=z^7`; coefficientwise reconstruction gives `g_10,g_9,g_8`
and direct substitution makes the complete levels 19, 18, 17, and 16 vanish.
All three displayed rows retain exact degree.  This witness is independent of
generic `solve()[0]` case choices and proves that the first branch is genuinely
alive at level 16.
