# The v-cascade: a second, dual complete cascade — and it verifies the first

## The grading

`v(x^i y^j) = 2i - j`.  A `v`-homogeneous piece of degree `d` is `y^-d F_d(r)`
with `r = x y^2`, since `x^i y^(2i-d) = y^-d (x y^2)^i`.  Using the controlled
identity `{y^a F(r), y^b G(r)} = y^(a+b+1)(b F' G - a F G')` with `a = -d`,
`b = -e`, the bracket lands on `v`-level `d+e-1`, and `x^2 = y^-4 r^2`, so

    **sum_{d+e = V+1} [ d F_d G_e' - e F_d' G_e ] = delta_{V,4} r^2**

`v` runs over `[-8, 2]` on `N(P)` and `[-12, 3]` on `N(Q)`, giving levels
`V = 4 .. -20` — **25 levels**, against the `w`-cascade's 22.

## Two independent triangulations, same total

    w-cascade (w = j - i) : 22 levels, **301 equations**
    v-cascade (v = 2i - j) : 25 levels, **301 equations**

Two completely different gradings of the same system, decomposed differently,
totalling the same.  That is a strong independent check on both.

## The top level is the lower edge, and it is decided

`V = 4` is `(d,e) = (2,3)`, i.e.

    2 F_2 G_3' - 3 F_2' G_3 = r^2

which is exactly `LOWER_EDGE.md`'s relation — **CONTROL: PASS**, the two
expressions differ by zero.  That level alone is **NONEMPTY** (282-element
basis, 5.6 s, with the contradictory-row negative control returning `[1]` in
0.005 s).

## Why the two cascades are worth having both

They are not the same conditions rearranged.  The `w`-cascade's top level is
**homogeneous** — the leading forms are both functions of `u`, so their bracket
vanishes identically, and the content only appears further down.  The
`v`-cascade's top level is **inhomogeneous**: `v(x^2) = 4 = v(P) + v(Q) - 1`
exactly, so the very first level already carries the `r^2`.  An inhomogeneous
top is strictly more restrictive, and the two cascades cut the variable set
along different lines, so conditions from one are new information for the other.

## Descent structure

Going down from `V = 4`, level `V` introduces `F_{V-2}` and `G_{V-1}`:

    V = 4 .. -6   : both new
    V = -7 .. -11 : only G new
    V = -12 .. -20: nothing new -> 9 levels of PURE CONDITIONS

## Status

Pentagon **NO VERDICT**.  Lower edge / v-level 4: **NONEMPTY** (controlled).
Levels 4+3 combined are queued as a single decidable system (34 equations, 36
unknowns, both mutable vertices saturated).
