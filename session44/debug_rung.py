#!/usr/bin/env python3
"""Ground-truth check of uvw_hunt's rung-1 affine system against sympy."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
import sympy as sp  # noqa: E402

import ribbon46_reduction as r46  # noqa: E402
from uvw_hunt import State, TERMS, USED_A  # noqa: E402

x = sp.Symbol("x")
u_val = 1
A5s, aa, bb, tt = sp.symbols("A5s aa bb tt")

rows_poly = [
    -x,                       # p0 (x^84 invisible)
    u_val * x + aa * x**2,    # p1
    bb * x**2,                # p2  (v=0)
    tt * x**2,                # p3  (w=0)
]
subs = {r46.p[i]: rows_poly[i] for i in range(4)}
subs.update({r46.dp[i]: sp.diff(rows_poly[i], x) for i in range(4)})
subs.update({r46.c: 1, r46.A[1]: -1, r46.A[2]: sp.Rational(-1, 2),
             r46.A[3]: sp.Rational(-1, 3), r46.A[5]: A5s,
             r46.A[0]: 0, r46.A[4]: 0})

print("USED_A =", USED_A)
for name, expr, target in (("E2", r46.survivors[2], 0),
                           ("E1", r46.survivors[1], 0),
                           ("E0", r46.survivors[0], 1)):
    co = sp.expand((expr - target).subs(subs)).coeff(x, 1)
    print(f"[x^1] {name} = {sp.expand(co)}")

st = State(None, 1, 0, 0, 2)
# replicate rung 0 by hand
st.A[1], st.A[2], st.A[3] = map(st.conv, (-1,)), None, None  # placeholder
