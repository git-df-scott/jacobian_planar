import sympy as sp, sys
from itertools import product
sys.path.insert(0,'.')
import chi_exact as CE
from pathS_scan2 import plane_cut, n_Csing
from pathS_modification import slice_AB, components
x,y=sp.symbols('x y')
vals=[0,1,-1,2,-2,3,-3,sp.Rational(1,2),sp.Rational(1,3),4]
ks=[0,1,-1,sp.Rational(-1,4),2,-2,sp.Rational(1,3),3]
chi1=0; surv=[]; red=0; hfail=0
for a,b,c in product(vals,repeat=3):
    if (a,b,c)==(0,0,0): continue
    for k in ks:
        try:
            nC=n_Csing(a,b,c,k)
            if nC is sp.oo or nC%2==1: continue
            cut=plane_cut(a,b,c,k)
            if not sp.sympify(cut).free_symbols: continue
            if 3-2*CE.chi_plane_curve(cut)-nC!=1: continue
            chi1+=1
            A,B=slice_AB(a,b,c,k); Bx=sp.expand(B.as_expr())
            comps=components(A)
            if any(Bx!=0 and sp.simplify(sp.rem(Bx,sp.expand(f),x))==0 for f,_ in comps):
                red+=1; continue
            hit=[list(sp.groebner([sp.expand(f),Bx],x,y,order='grevlex').exprs)!=[sp.Integer(1)] for f,_ in comps]
            if comps and all(hit): surv.append((a,b,c,k))
            else: hfail+=1
        except Exception: pass
print("planes with chi(S)=1 :", chi1)
print("  killed by 1-dim centre (S reducible):", red)
print("  killed by H_1 (a component not hit) :", hfail)
print("  SURVIVING chi + H_1 ALONE, no Chau citation used:", len(surv))
for s in surv: print("     ",s)
