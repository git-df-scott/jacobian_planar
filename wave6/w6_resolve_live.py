#!/usr/bin/env python3
"""Resolve the two LIVE shapes from the plane tangent-sweep search.

`w6_plane_sweep_search.py` tested 501 shapes: 499 EMPTY, **2 LIVE**. Its own
docstring defers two checks:

    "A solution with kappa != 0 and the divisibilities holding is a PLANE KELLER
     MAP OF TANGENT-SWEEP TYPE -- to be checked for non-injectivity before any
     claim is made."

Neither was done. So a LIVE shape is an unresolved candidate, and these two are
the only surviving ones in the whole sweep. This script finishes the job:

  1. solve the side-condition system exactly over Q (with kappa != 0, a != 0);
  2. check the DIVISIBILITIES  C^i | P  and  C^j | Q  -- if they fail, the pair
     (P/C^i, Q/C^j) is not polynomial and the shape dies here;
  3. build F = (P/C^i, Q/C^j) and verify det JF is a nonzero CONSTANT (Keller);
  4. test INJECTIVITY. A non-injective Keller F would be a counterexample.

Every outcome is informative: a surviving map is a candidate counterexample; a
death names which of (2), (3), (4) killed it, which is the missing entry in the
sweep's own bookkeeping.
"""
import sys
import sympy as sp

x, y, w = sp.symbols('x y w')
LIVE = [(1, 0, 0, 1, 1, 0, 1, 2), (1, 0, 0, 1, 1, 0, 1, 3)]


def sweep_q(p_poly):
    return sp.expand(sp.integrate(sp.Rational(1, 2) * w * sp.diff(p_poly, w), (w, 0, w)))


def br(A, B):
    return sp.expand(sp.diff(A, x) * sp.diff(B, y) - sp.diff(A, y) * sp.diff(B, x))


def resolve(al, be, mu, nu, s, i, j, d):
    print(f"\n=== shape (al,be,mu,nu,s,i,j,d) = {(al,be,mu,nu,s,i,j,d)}")
    c0, a, b, kap = sp.symbols('c0 a b kappa')
    ks = sp.symbols(f'k1:{d+1}')
    unk = [c0, a, b, kap] + list(ks)
    gam = c0 + a * x**al * y**be
    u = 1 + b * x**mu * y**nu
    wx = sp.expand(gam * u)
    p_poly = sum(ks[t - 1] * w**t for t in range(1, d + 1))
    q_poly = sweep_q(p_poly)
    P = sp.expand(p_poly.subs(w, wx) + 2 * gam)
    Q = sp.expand(q_poly.subs(w, wx) + gam * wx)
    C = sp.expand(gam * x**s)
    lhs = sp.expand(C * 2 * gam * br(gam, wx) - j * Q * br(P, C) + i * P * br(Q, C)
                    - kap * C**(i + j + 1))
    eqs = [sp.expand(c) for c in sp.Poly(lhs, x, y).coeffs()]
    t = sp.Symbol('t_sat')
    sols = sp.solve(eqs + [t * kap * a - 1], unk + [t], dict=True)
    print(f"  side-condition system: {len(eqs)} equations, "
          f"{len(sols)} solution branch(es) with kappa != 0, a != 0")
    if not sols:
        print("  -> NO SOLUTION once solved exactly: shape is EMPTY after all")
        return
    for si, sol in enumerate(sols):
        print(f"\n  --- branch {si}: {{" +
              ", ".join(f"{k}={v}" for k, v in sol.items() if k != t) + "}")
        Ps, Qs, Cs = (sp.expand(z.subs(sol)) for z in (P, Q, C))
        kv = sp.simplify(kap.subs(sol)) if kap in sol else kap
        print(f"      kappa = {kv}")
        if Cs == 0:
            print("      C == 0 identically -> DEAD (no map)")
            continue
        # (2) divisibilities
        F1n, r1 = sp.div(sp.Poly(Ps, x, y), sp.Poly(Cs**i, x, y)) if i else (sp.Poly(Ps, x, y), sp.Poly(0, x, y))
        F2n, r2 = sp.div(sp.Poly(Qs, x, y), sp.Poly(Cs**j, x, y)) if j else (sp.Poly(Qs, x, y), sp.Poly(0, x, y))
        if r1.as_expr() != 0 or r2.as_expr() != 0:
            print(f"      DIVISIBILITY FAILS: C^{i}|P remainder {r1.as_expr()!s:.40}, "
                  f"C^{j}|Q remainder {r2.as_expr()!s:.40}")
            print("      -> DEAD: (P/C^i, Q/C^j) is not polynomial")
            continue
        F1, F2 = F1n.as_expr(), F2n.as_expr()
        print(f"      F1 = {sp.factor(F1)}")
        print(f"      F2 = {sp.factor(F2)}")
        # (3) Keller
        detJ = sp.simplify(sp.diff(F1, x) * sp.diff(F2, y) - sp.diff(F1, y) * sp.diff(F2, x))
        print(f"      det JF = {sp.factor(detJ)}")
        isconst = (sp.simplify(sp.diff(detJ, x)) == 0 and sp.simplify(sp.diff(detJ, y)) == 0)
        if not isconst:
            print("      -> DEAD: det JF is not constant, F is not Keller")
            continue
        if sp.simplify(detJ) == 0:
            print("      -> DEAD: det JF == 0, degenerate")
            continue
        print("      *** KELLER with nonzero constant Jacobian ***")
        # (4) injectivity: look for a collision F(x,y) = F(X,Y) with (x,y) != (X,Y)
        X, Y = sp.symbols('X Y')
        sysc = [sp.expand(F1 - F1.subs({x: X, y: Y})), sp.expand(F2 - F2.subs({x: X, y: Y}))]
        gsol = sp.solve(sysc, [X, Y], dict=True)
        print(f"      collision system solutions: {gsol}")
        offdiag = [g for g in gsol if not (sp.simplify(g.get(X, X) - x) == 0
                                           and sp.simplify(g.get(Y, Y) - y) == 0)]
        if offdiag:
            print(f"      *** NON-INJECTIVE BRANCH FOUND: {offdiag} ***")
            print("      *** CANDIDATE COUNTEREXAMPLE -- verify exactly ***")
        else:
            print("      injective on the solved branches -> not a counterexample")


if __name__ == '__main__':
    for sh in LIVE:
        try:
            resolve(*sh)
        except Exception as e:
            print(f"  shape {sh} raised: {type(e).__name__}: {str(e)[:200]}")
