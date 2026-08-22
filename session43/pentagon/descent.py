#!/usr/bin/env python3
"""Full descent of the edge ladder, rungs 19 -> 12, at the pentagon's degrees.

The reduction  raw rung == y^(2d-4) * edge rung  is CONTROLLED in edgeladder.py
(PASS at every d = 12..19).  Here we run the descent itself:

  rung 19 pins A_8 and B_12;  rung d (18..12) solves for B_{d-7} and any
  leftover equations are RESIDUAL CONDITIONS on the A_i -- i.e. solver-free
  algebraic constraints on the pentagon's p_{j,i}.
"""
import sympy as sp
y = sp.symbols('y')
M, N = 8, 12

def rung_edge(d, A, B):
    s = 0
    for i in range(1, M + 1):
        k = d + 1 - i
        if 2 <= k <= N and i in A and k in B:
            s += (2*k - 3*i)*A[i]*B[k] + y*(i*A[i]*sp.diff(B[k], y) - k*sp.diff(A[i], y)*B[k])
    return sp.expand(s)

al, be, r = sp.symbols('alpha beta r', nonzero=True)
A = {8: al*(y - r)**2}
B = {12: be*(y - r)**3}

def gen(name, deg):
    c = [sp.Symbol(f'{name}{i}') for i in range(deg + 1)]
    return sum(c[i]*y**i for i in range(deg + 1)), c

Acoef = {}
for i in range(1, 8):
    A[i], Acoef[i] = gen(f'a{i}_', 10 - i)

allresid = []
for d in range(18, 11, -1):
    k = d + 1 - M                      # the new unknown B_k
    B[k], cB = gen(f'b{k}_', 15 - k)
    eqs = sp.Poly(rung_edge(d, A, B), y).all_coeffs()
    sol = sp.solve(eqs, cB, dict=True)
    if not sol:
        print(f"rung {d}: NO SOLUTION for B_{k}  -> the edge ladder is inconsistent here")
        break
    s = sol[0]
    B[k] = sp.expand(B[k].subs(s))
    free = [c for c in cB if c not in s]
    resid = sorted({sp.factor(sp.simplify(e.subs(s))) for e in eqs} - {0}, key=sp.count_ops)
    allresid += resid
    print(f"rung {d:2d}: solved B_{k} ({len(cB)} coeffs, {len(eqs)} eqs), "
          f"free={len(free)}, residual conditions={len(resid)}")
    for x in resid:
        print("        COND:", x)
    # is B_k a multiple of (y-r)^j * A_{k-4} ?  (the pattern seen at rung 18)
    for j in range(0, 5):
        for src in list(Acoef) + [None]:
            cand = (y - r)**j * (A[src] if src else 1)
            qt = sp.cancel(sp.factor(B[k]) / cand)
            if qt.free_symbols.isdisjoint({y}) and qt != 0:
                print(f"        FORM: B_{k} = ({sp.factor(qt)}) * (y-r)^{j}"
                      + (f" * A_{src}" if src else ""))
                break
        else:
            continue
        break

print("\nALL RESIDUAL CONDITIONS:", len(allresid))
for x in sorted(set(allresid), key=sp.count_ops):
    print("  ", x)
