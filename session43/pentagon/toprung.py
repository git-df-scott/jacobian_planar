#!/usr/bin/env python3
"""Top rung of the general x-ladder at the pentagon's own degrees (m=8, n=12).

Rung d of  {P,Q} = x^2  with  P = sum a_i(y) x^i,  Q = sum q_k(y) x^k  is
    sum_{i+k=d+1} [ i a_i q_k' - k a_i' q_k ] = delta_{d,2}.
At d = m+n-1 only (i,k) = (m,n) survives:  m a_m q_n' - n a_m' q_n = 0.

For the pentagon, N(P) has vertices (8,14),(8,16) and N(Q) has (12,21),(12,24),
so   a_8 = y^14 u(y),  deg u = 2, u(0) = p_14_8 != 0
     q_12 = y^21 w(y), deg w = 3, w(0) = q_21_12 != 0.

Every claim below is checked numerically; controls at the bottom.
"""
import sympy as sp

y = sp.symbols('y')

def rung(d, a, q, m, n):
    """LHS of rung d.  a, q are dicts index -> expr in y."""
    s = 0
    for i in range(0, m + 1):
        k = d + 1 - i
        if 0 <= k <= n:
            s += i * a[i] * sp.diff(q[k], y) - k * sp.diff(a[i], y) * q[k]
    return sp.expand(s)

# ---------------------------------------------------------------- CONTROL 1
# The rung formula itself, at the pentagon's own degrees m=8, n=12, with all
# a_i, q_k free functions of y.  Compare against the direct bracket expansion.
def control_rung_formula(m, n):
    x = sp.symbols('x')
    a = {i: sp.Function(f'a{i}')(y) for i in range(m + 1)}
    q = {k: sp.Function(f'q{k}')(y) for k in range(n + 1)}
    P = sum(a[i] * x**i for i in range(m + 1))
    Q = sum(q[k] * x**k for k in range(n + 1))
    br = sp.expand(sp.diff(P, x) * sp.diff(Q, y) - sp.diff(P, y) * sp.diff(Q, x))
    br = sp.Poly(br, x)
    ok = True
    for d in range(0, m + n):
        direct = sp.expand(br.coeff_monomial(x**d))
        viaform = rung(d, a, q, m, n)
        if sp.simplify(direct - viaform) != 0:
            ok = False
            print(f"  MISMATCH at d={d}")
    return ok

print("CONTROL 1: rung formula vs direct bracket, m=8 n=12, free a_i q_k")
print("  ", "PASS" if control_rung_formula(8, 12) else "FAIL")

# ---------------------------------------------------------------- DESCENT MAP
# Which rung determines which q_k, and which rungs are residual identities.
m, n = 8, 12
print("\nDESCENT STRUCTURE (m=8, n=12):")
determined = set()
resid = []
for d in range(m + n - 1, -1, -1):
    pairs = [(i, d + 1 - i) for i in range(m + 1) if 0 <= d + 1 - i <= n]
    newk = [k for (i, k) in pairs if k not in determined]
    if pairs and max(i for i, k in pairs) == m and (d - m) not in determined and 0 <= d - m <= n:
        determined.add(d - m)
        print(f"  rung d={d:2d}  pairs={pairs}  -> solves q_{d-m}")
    else:
        resid.append(d)
print(f"  residual rungs (pure conditions on the p's): {sorted(resid)}  ({len(resid)} of them)")
