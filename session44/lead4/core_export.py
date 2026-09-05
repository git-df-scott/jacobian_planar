import sympy as sp, json, pickle, os
from core_reduce import build
A,B,conds = build()
unk=[sp.Symbol(f"A{i}") for i in range(1,7)]
ints=[]
for c in conds:
    p=sp.Poly(c,*unk)
    d=sp.lcm([sp.denom(sp.nsimplify(co)) for co in p.coeffs()])
    q=sp.expand(c*d)
    assert all(sp.Rational(co).q==1 for co in sp.Poly(q,*unk).coeffs()), "not integral"
    ints.append(sp.Poly(q,*unk))
    print("cond: deg",q.as_poly(*unk).total_degree(),"terms",len(p.coeffs()))
pickle.dump([sp.srepr(p.as_expr()) for p in ints], open("core_conds.pkl","wb"))
# also B10 numerator for the Q-vertex nondegeneracy
b10=sp.together(B[10]); num=sp.numer(b10)
pickle.dump(sp.srepr(sp.expand(num)), open("core_b10.pkl","wb"))
def ms(p): return str(p.as_expr()).replace("**","^")
open("core.ms","w").write("A1,A2,A3,A4,A5,A6\n0\n" + ",\n".join(ms(p) for p in ints) + "\n")
open("core_p.ms","w").write("A1,A2,A3,A4,A5,A6\n1073741827\n" + ",\n".join(ms(p) for p in ints) + "\n")
print("wrote core.ms")
