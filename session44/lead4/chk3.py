"""Verify the w-graded bracket identity for subcase 2, symbolically."""
import sympy as sp
from collections import defaultdict
from trackB1_polygon import hull_rows
x,y,t = sp.symbols('x y t')
def lat(v):
    R=hull_rows([tuple(p) for p in v]); return [(i,j) for j in sorted(R) for i in range(R[j][0],R[j][1]+1)]
NP=[(0,0),(1,0),(8,14),(8,16)]; NQ=[(0,0),(2,1),(12,21),(12,24)]
a={p:sp.Symbol(f"a_{p[0]}_{p[1]}") for p in lat(NP)}
b={p:sp.Symbol(f"b_{p[0]}_{p[1]}") for p in lat(NQ)}
P=sum(a[p]*x**p[0]*y**p[1] for p in a)
Q=sum(b[p]*x**p[0]*y**p[1] for p in b)
br=sp.expand(sp.diff(P,x)*sp.diff(Q,y)-sp.diff(P,y)*sp.diff(Q,x))
# graded form: P = sum_m f_m(t) y^-m, Q = sum_n g_n(t) y^-n
f={m:sum(a[(i,2*i-m)]*t**i for (i,j) in a if 2*i-j==m) for m in (0,1,2)}
g={n:sum(b[(i,2*i-n)]*t**i for (i,j) in b if 2*i-j==n) for n in (0,1,2,3)}
pred=0
for m in f:
    for n in g:
        pred += (m*f[m]*sp.diff(g[n],t) - n*sp.diff(f[m],t)*g[n])*y**(1-m-n)
pred = sp.expand(pred.subs(t, x*y**2))
print("graded formula matches direct bracket:", sp.simplify(sp.expand(br-pred))==0)
# the five level equations
for S in range(0,6):
    e=0
    for m in f:
        for n in g:
            if m+n==S: e+= m*f[m]*sp.diff(g[n],t) - n*sp.diff(f[m],t)*g[n]
    e=sp.expand(e)
    pol=sp.Poly(e,t) if e!=0 else None
    print(f"  level m+n={S}: {'IDENTICALLY ZERO' if e==0 else 'poly in t, degs '+str(sorted(pol.monoms())[0][0])+'..'+str(pol.degree())+', #coeff eqs '+str(len(pol.monoms()))}")
