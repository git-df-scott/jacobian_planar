#!/usr/bin/env python3
"""Odd m on the 2:3 ray is empty for a leading-term reason, not a computation.

Top level:  2 f g' - 3 f' g = T^2,  f = f_2 (deg m, top coeff nonzero by the
nondegeneracy at the polygon vertex), g = g_3 (deg d).

Coefficient of T^(m+d-1), the top: (2d - 3m)*f_m*g_d.
If 2d != 3m this is nonzero, so deg(LHS) = m + d - 1, and LHS = T^2 forces
m + d - 1 = 2, i.e. m + d = 3.
So either m + d = 3 (only m = 1, 2 with the vertex (1,0) present), or 2d = 3m,
which needs m EVEN.

Hence for odd m >= 3 the leading level alone is unsatisfiable: EMPTY, with no
Groebner basis required.  This is why m=5 ground for 900s without finishing --
the obstruction is at the top coefficient, which a degrevlex GB reaches last.
"""
from fractions import Fraction

print(f"{'m':>3}  {'2d=3m -> d':>10}  {'m+d=3 possible?':>16}  verdict")
for m in range(1, 17):
    d = Fraction(3 * m, 2)
    ok_ratio = d.denominator == 1
    ok_small = (3 - m) >= 1
    if ok_ratio:
        v = f"leading term cancels at deg g_3 = {int(d)}; needs the full computation"
    elif ok_small:
        v = f"degenerate branch m+deg g_3 = 3 (deg g_3 = {3-m})"
    else:
        v = "EMPTY at the top coefficient alone"
    print(f"{m:>3}  {str(d):>10}  {str(ok_small):>16}  {v}")
