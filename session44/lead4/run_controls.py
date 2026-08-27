"""POSITIVE controls: shapes with an explicitly known (P,Q).  The walk must
NOT return EMPTY on these.

  C1  P = 1 + x,           Q = 1 + x^2 y          [P,Q] = x^2
  C2  P = 1 + x + a x^2 y, Q = 1 + x^2 y          [P,Q] = x^2   (any a)
  C3  P = 1 + x + y^2,     Q = 1 + y              [P,Q] = 1
"""
import sympy as sp, wgrade as W
x, y = sp.symbols("x y")

CTRL = [
    ("C1", [(0,0),(1,0)], [(0,0),(2,1)], 2, 1+x, 1+x**2*y),
    ("C2", [(0,0),(1,0),(2,1)], [(0,0),(2,1)], 2, 1+x+3*x**2*y, 1+x**2*y),
    ("C3", [(0,0),(1,0),(0,2)], [(0,0),(0,1)], 0, 1+x+y**2, 1+y),
]
for nm, NP, NQ, r, P, Q in CTRL:
    br = sp.expand(sp.diff(P,x)*sp.diff(Q,y) - sp.diff(P,y)*sp.diff(Q,x))
    assert br == x**r, (nm, br)
    print(f"=== {nm}: witness [P,Q] = x^{r} verified; NP={NP} NQ={NQ}")
    for wt in W.weight_candidates(NP, NQ):
        for tdir in [None]:
            wk = W.Walk(NP, NQ, r, wt, gauge=[("P",(1,0),1)] if (1,0) in NP else [])
            c = wk.run()
            nd = W.nondeg_exprs(wk, "P") + W.nondeg_exprs(wk, "Q")
            free = wk.unassigned()
            out, fn = W.singular_verdict(c, free, nd, char=0, tag=f"ctrl_{nm}")
            print(f"    weight {wt}: {len(c)} conditions, {len(free)} free")
            for L in out.splitlines(): print("      "+L)

# ---- C4: a richer positive control, several w-levels ----------------------
a, lam = sp.Rational(3), sp.Rational(2)
P4 = 1 + x + a*x**2*y
Q4 = 1 + x**2*y + lam*P4**2
br = sp.expand(sp.diff(P4,x)*sp.diff(Q4,y) - sp.diff(P4,y)*sp.diff(Q4,x))
assert br == x**2, br
def supp(e):
    p = sp.Poly(e, x, y); return [m for m in p.monoms()]
NP4, NQ4 = W.hull_vertices(supp(P4)), W.hull_vertices(supp(Q4))
print(f"=== C4: witness [P,Q]=x^2 verified; NP={NP4} NQ={NQ4}")
for wt in W.weight_candidates(NP4, NQ4):
    wk = W.Walk(NP4, NQ4, 2, wt, gauge=[("P",(1,0),1)])
    c = wk.run()
    nd = W.nondeg_exprs(wk,"P") + W.nondeg_exprs(wk,"Q")
    out, fn = W.singular_verdict(c, wk.unassigned(), nd, char=0, tag="ctrl_C4")
    print(f"    weight {wt}: {len(c)} conditions, {len(wk.unassigned())} free")
    for L in out.splitlines(): print("      "+L)
