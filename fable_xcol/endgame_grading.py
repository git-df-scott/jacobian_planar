import sympy as sp, pickle, sys
from sympy import Matrix
src = sys.argv[1]
conds, sub = pickle.load(open(src,'rb'))
conds = [sp.expand(c) for c in conds if sp.expand(c)!=0]
vs = sorted(set().union(*[c.free_symbols for c in conds]), key=str)
print(f"{src}: {len(conds)} conditions, {len(vs)} params")
# grading: find integer w with <w, m1-m2> = 0 for all monomial pairs in each cond
rows=[]
for c in conds:
    P = sp.Poly(c, *vs); ms = P.monoms()
    m0 = ms[0]
    for m in ms[1:]:
        rows.append([a-b for a,b in zip(m, m0)])
if not rows:
    print("no rows"); sys.exit()
M = Matrix(rows)
ns = M.nullspace()
print("GRADING TORUS RANK =", len(ns))
for v in ns:
    d = sp.lcm([x.q for x in v]); vv=[int(x*d) for x in v]
    g = sp.gcd(vv); vv=[x//g for x in vv]
    print("  weight vector:", dict(zip([str(x) for x in vs], vv)))
    print("  all-positive:", all(x>0 for x in vv), " all-nonzero:", all(x!=0 for x in vv))
# homogeneity check per condition (are all conds already homogeneous in total degree?)
degs = [sp.Poly(c,*vs).total_degree() for c in conds]
homog = [len(set(sum(m) for m in sp.Poly(c,*vs).monoms()))==1 for c in conds]
print("conds homogeneous in standard grading:", sum(homog), "/", len(conds))
print("total degrees:", sorted(set(degs)))
# does the system have a constant term anywhere (i.e. is origin a solution)?
zero = {v:0 for v in vs}
at0 = [sp.simplify(c.subs(zero)) for c in conds]
print("conditions nonzero at origin:", sum(1 for a in at0 if a!=0))
