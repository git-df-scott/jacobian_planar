"""Global first-row exactness with both triple roots and relaxed chart bounds."""
import sympy as s
from sympy.polys.rings import ring
from pathlib import Path
import json
A,T=s.symbols('A T')
q=3*A**4+60*A**3+394*A**2+620*A+475
K=s.QQ.alg_field_from_poly(s.Poly(q,A),alias='A')
ak=K.unit
rk=(3*ak**3+135*ak**2-851*ak+905)/K(6160)
sk=-ak-3*rk
beta=rk-1; gamma=sk-1
R,y=ring('y',K)
F=y*(y-beta);G=(y+1)*(y-gamma);D=F*G
def op(C):return 2*D*C.diff(y)-(3*F.diff(y)*G+F*G.diff(y))*C
cols=[op(y**j) for j in range(5)]
# RHS a has degree <=3 and a(-1)=0.
mat=[[c.get((i,),K.zero) for c in cols] for i in range(4,8)]
mat.append([sum(v*(-K.one)**m[0] for m,v in c.items()) for c in cols])
def kernel(mat,n):
    M=[r[:] for r in mat]; piv=[];row=0
    for col in range(n):
        cand=next((i for i in range(row,len(M)) if M[i][col]),None)
        if cand is None: continue
        M[row],M[cand]=M[cand],M[row]
        lead=M[row][col];M[row]=[v/lead for v in M[row]]
        for i in range(len(M)):
            if i!=row and M[i][col]:
                fac=M[i][col];M[i]=[v-fac*w for v,w in zip(M[i],M[row])]
        piv.append(col);row+=1
    ans=[]
    for free in [j for j in range(n) if j not in piv]:
        v=[K.zero]*n;v[free]=K.one
        for i,c in enumerate(piv):v[c]=-M[i][free]
        ans.append(v)
    return ans
ker=kernel(mat,5)
print('first-row primitive dimension',len(ker),flush=True)
for v in ker:
    C=sum((y**i)*v[i] for i in range(5)); a=op(C)/2
    print('C=',C.as_expr(),flush=True)
    print('a=',a.as_expr(),flush=True)
    print('a degree',a.degree(),flush=True)
    assert not sum(v*(-K.one)**m[0] for m,v in a.items())

# Next row: normalize the nonzero first-row scalar to one, so mu^2=1.
assert len(ker)==1
def value(poly,at):return sum(co*at**mon[0] for mon,co in poly.items())
def solve_affine(mat,rhs,n):
    M=[rr[:]+[v] for rr,v in zip(mat,rhs)];piv=[];row=0
    for col in range(n):
        cand=next((i for i in range(row,len(M)) if M[i][col]),None)
        if cand is None:continue
        M[row],M[cand]=M[cand],M[row];lead=M[row][col]
        M[row]=[v/lead for v in M[row]]
        for i in range(len(M)):
            if i!=row and M[i][col]:
                fac=M[i][col];M[i]=[v-fac*w for v,w in zip(M[i],M[row])]
        piv.append(col);row+=1
    if any(not any(rr[:n]) and rr[n] for rr in M):return None,None
    out=[K.zero]*n
    for i,c in enumerate(piv):out[c]=M[i][n]
    return out,[j for j in range(n) if j not in piv]
op2=lambda B:4*D*B.diff(y)-(7*F.diff(y)*G+5*F*G.diff(y))*B
columns=[op2(y**j) for j in range(7)]+[96*G*y**j for j in range(6)]
target=20*a*a
matrix=[[cc.get((i,),K.zero) for cc in columns] for i in range(10)]
rhs=[target.get((i,),K.zero) for i in range(10)]
for at,rhsval in [(-K.one,K.zero),(K.zero,value(a,K.zero)**2/(9*value(G,K.zero))),
                   (beta,value(a,beta)**2/(9*value(G,beta)))]:
    matrix.append([K.zero]*7+[at**j for j in range(6)]);rhs.append(rhsval)
vv,free=solve_affine(matrix,rhs,13)
print('nonzero first-row second forcing soluble',vv is not None,flush=True)
if vv is not None:
    PP=sum(y**j*vv[7+j] for j in range(6));BB=sum(y**j*vv[j] for j in range(7))
    assert op2(BB)+96*G*PP==target
    print('remaining free dimension',len(free),flush=True)
    print('particular b=',PP.as_expr(),flush=True)
    print('particular primitive B=',BB.as_expr(),flush=True)
