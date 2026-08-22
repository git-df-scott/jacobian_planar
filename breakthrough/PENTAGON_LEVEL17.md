# Direct pentagon strike: level 17 doubles the forced root order

## Result

The one-variable `s = xy` ladder gives a new solver-free necessary condition:

    **(s - tau)^4 divides h_7(s).**

Level 18 had forced only `(s - tau)^2 | h_7`.  Level 17 therefore doubles the
known multiplicity.  This is an exclusion condition on the all-vertex target,
not a witness or an emptiness certificate; the pentagon verdict remains
**NO VERDICT**.

## Independent calculation

Put `z = s - tau`, normalize neither leading coefficient, and write

    h_8 = c0 z^8,        g_12 = c1 z^12,
    h_7 = z^2 (a0 + a1 z + ... + a6 z^6).

The complete level-19 solution is

    g_11 = (3 c1 / 2 c0) z^4 h_7 + (lambda / 8 c0) z^11.

At level 18, define the carried part

    T18 = <h_7,g_11>_(7,11) + <h_6,g_12>_(6,12),
    <f,g>_(a,b) := b f' g - a f g'.

The new `g_10` equation is

    D_10(g_10) = -T18 / (8 c0 z^7),
    D_k(f) := k f - z f'.

The quotient is polynomial and has zero `z^10` coefficient, so it lies in the
image of `D_10`; inversion coefficient-by-coefficient leaves precisely the
expected kernel constant `kappa z^10`.  This checks that no integration
constant was greedily discarded.

At level 17 the terms containing the new `g_9` and `h_5` are multiples of
`z^7`.  Hence its first obstruction is exactly divisibility by `z^7` of

    K17 = <h_7,g_10>_(7,10) + <h_6,g_11>_(6,11).

The low coefficients computed over the exact rational function field begin

    [z^1] K17 = 15 c1 a0^3 / (2 c0^2),
    [z^4] K17 mod (a0) = 6 c1 a1^3 / c0^2.

Because `c0*c1 != 0` in the vertex-saturated chart, divisibility first forces
`a0 = 0` and then `a1 = 0`.  Conversely, direct symbolic substitution of
`a0 = a1 = 0` makes every coefficient below `z^7` vanish.  Thus the condition
is equivalent to `z^4 | h_7`.

There is no hidden second obstruction: after division by `z^7`, the resulting
right-hand side has zero coefficient in the resonant `z^9` slot of `D_9`.
Coefficientwise inversion reconstructs a solution exactly (with the arbitrary
kernel multiple of `z^9` retained).  Hence fourfold divisibility is necessary
and sufficient for the **complete** level 17, not merely for its divisibility
gate.

The calculation is implemented in `pentagon_level17.py`.  Its controls verify
the level-18 quotient, the missing `D_10` resonance, exact inversion including
the kernel, both forcing coefficients, the converse, and the level-17 `D_9`
image condition.

## Consequence for the constructive hunt

The degree-eight row now has the form

    h_7(s) = (s - tau)^4 C_4(s),   deg(C_4) <= 4.

This removes two more parameters and shows that the concentration at the common
edge root continues.  Level 17 is now completely solved, with its kernel
constant retained.  The next direct attack is level 16 with this fourfold root
imposed.
