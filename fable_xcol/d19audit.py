"""Audit d=19: is sp.solve's answer the GENERAL solution, or did it delete components?
Closed form predicts a_8 = alpha*W^2, b_12 = beta*W^3, W = y^7(y-r): a 3-dim family."""
import sympy as sp
y=sp.Symbol('y')
a8=sum(sp.Symbol(f'a8_{j}')*y**j for j in range(14,17))
b12=sum(sp.Symbol(f'b12_{j}')*y**j for j in range(21,25))
A=[sp.Symbol(f'a8_{j}') for j in range(14,17)]; B=[sp.Symbol(f'b12_{j}') for j in range(21,25)]
E=sp.expand(8*a8*sp.diff(b12,y)-12*sp.diff(a8,y)*b12)
cs=[c for c in sp.Poly(E,y).all_coeffs() if c!=0]
print("d=19 equations:",len(cs))
for c in cs: print("   ",sp.factor(c))
# closed form check
al,be,r=sp.symbols('alpha beta r')
W=y**7*(y-r)
cf={}
pa=sp.Poly(sp.expand(al*W**2),y); pb=sp.Poly(sp.expand(be*W**3),y)
for j in range(14,17): cf[sp.Symbol(f'a8_{j}')]=pa.coeff_monomial(y**j)
for j in range(21,25): cf[sp.Symbol(f'b12_{j}')]=pb.coeff_monomial(y**j)
print("closed form satisfies all d=19 eqs:",all(sp.simplify(c.subs(cf))==0 for c in cs))
# is it the general solution? primary decomposition by hand: solve with a8_16 != 0 and separately =0
gen=sp.solve(cs,A+B,dict=True)
print("\nsp.solve components:",len(gen))
for g in gen: print("   ",{str(k):sp.factor(v) for k,v in g.items()})
# the DELETED stratum test: force the leading vertex a8_16 = 0 (allowed? vertex must be nonzero -> not allowed)
# but force b12_24 = 0 (also a vertex) - and the intermediate strata:
for name,extra in [("a8_16=0",{sp.Symbol('a8_16'):0}),("b12_24=0",{sp.Symbol('b12_24'):0}),
                   ("a8_14=0 (p_14_8=0)",{sp.Symbol('a8_14'):0})]:
    cc=[sp.expand(c.subs(extra)) for c in cs]; cc=[c for c in cc if c!=0]
    s=sp.solve(cc,[v for v in A+B if v not in extra],dict=True)
    print(f"stratum {name}: {len(cc)} eqs -> {len(s)} components", [{str(k):v for k,v in x.items()} for x in s][:2])
