#!/usr/bin/env python3
"""Session 44 — exact symbolic descent of the (4,6) ribbon on the u = 0 chart.

On u = 0 the kernel coefficients (n+1)u/4 all vanish: no p3 kernel is ever
consumed by its rung.  Rung 2's E0 row becomes the pure condition
O(v,w) = (2 v^4 + 3 v w^2 + 18 w)/16 = 0, and all deeper structure couples the
kernels.  This script walks the recurrence exactly over Q(v,w,t2,t3,...):

  - at rung n, solve E2[x^n], E1[x^n] linearly for p1[n+1], p2[n+1]
    (their coefficients are nonzero constants at u=0);
  - E0[x^n] is then a condition C_n(v, w, t2, ..) ; report whether it is
    linear in the newest kernel (determines it), or kernel-free (a condition
    on the curve), or coupled.

Everything is exact sympy over Q.  Output is a structure map of the chart.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
import sympy as sp  # noqa: E402

import ribbon46_reduction as r46  # noqa: E402

x = sp.Symbol("x")
v, w = sp.symbols("v w")
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8

# kernel symbols t_m = p3[m]
t = {m: sp.Symbol(f"t{m}") for m in range(2, NMAX + 2)}

# series with symbolic coefficients, u = 0 chart
p1c = {0: sp.Integer(0), 1: sp.Integer(0)}
p2c = {0: sp.Integer(0), 1: v}
p3c = {0: sp.Integer(0), 1: w}
for m in range(2, NMAX + 2):
    p3c[m] = t[m] if m <= 21 else sp.Integer(0)


def series(coeffs, top):
    return sum(coeffs.get(k, sp.Integer(0)) * x**k for k in range(top + 1))


A1 = sp.Integer(-1)
A2 = sp.Integer(0)                     # -u/2
A3 = sp.Rational(-1, 3) * v            # -(u^2+v)/3
A5 = sp.Rational(-1, 5) * v**2         # -(u^4+3u^2v+2uw+v^2)/5

conditions = []
for n in range(2, NMAX + 1):
    # unknowns for this rung
    r_, s_ = sp.symbols(f"P1_{n+1} P2_{n+1}")
    p1c[n + 1] = r_ if n + 1 <= 63 else sp.Integer(0)
    p2c[n + 1] = s_ if n + 1 <= 42 else sp.Integer(0)
    top = n + 1
    rows = [series({0: 0, 1: -1}, 1),  # p0 = -x
            series(p1c, top), series(p2c, top), series(p3c, top)]
    sub = {r46.p[i]: rows[i] for i in range(4)}
    sub.update({r46.dp[i]: sp.diff(rows[i], x) for i in range(4)})
    sub.update({r46.c: 1, r46.A[1]: A1, r46.A[2]: A2, r46.A[3]: A3,
                r46.A[5]: A5, r46.A[0]: 0, r46.A[4]: 0})
    e2 = sp.expand((r46.survivors[2]).subs(sub)).coeff(x, n)
    e1 = sp.expand((r46.survivors[1]).subs(sub)).coeff(x, n)
    sol = sp.solve([e2, e1], [r_, s_], dict=True)
    assert len(sol) == 1, f"rung {n}: E2/E1 solve not unique: {sol}"
    p1c[n + 1] = sp.expand(sol[0][r_]) if n + 1 <= 63 else sp.Integer(0)
    p2c[n + 1] = sp.expand(sol[0][s_]) if n + 1 <= 42 else sp.Integer(0)
    rows = [series({0: 0, 1: -1}, 1),
            series(p1c, top), series(p2c, top), series(p3c, top)]
    sub = {r46.p[i]: rows[i] for i in range(4)}
    sub.update({r46.dp[i]: sp.diff(rows[i], x) for i in range(4)})
    sub.update({r46.c: 1, r46.A[1]: A1, r46.A[2]: A2, r46.A[3]: A3,
                r46.A[5]: A5, r46.A[0]: 0, r46.A[4]: 0})
    e0 = sp.expand((r46.survivors[0] - 1).subs(sub)).coeff(x, n)
    cond = sp.expand(e0)
    ker_syms = sorted([tm for m, tm in t.items() if cond.has(tm)],
                      key=str)
    if not ker_syms:
        conditions.append((n, sp.factor(cond)))
        print(f"rung {n}: KERNEL-FREE condition: {sp.factor(cond)}")
    else:
        newest = max((m for m in t if cond.has(t[m])))
        d_new = sp.diff(cond, t[newest])
        lin = not any(d_new.has(t[m]) for m in t) and not d_new.has(v, w) \
            or not any(sp.diff(cond, t[m]).free_symbols & set(t.values())
                       for m in t)
        print(f"rung {n}: involves kernels {[str(k) for k in ker_syms]}; "
              f"newest t{newest}, d/dt{newest} = {sp.factor(d_new)}")
        conditions.append((n, cond))

print()
print("== summary of conditions ==")
for n, cnd in conditions:
    kers = [str(tm) for m, tm in t.items() if sp.sympify(cnd).has(tm)]
    print(f"rung {n}: kernels {kers}: "
          f"{sp.factor(cnd) if not kers else str(cnd)[:200]}")
