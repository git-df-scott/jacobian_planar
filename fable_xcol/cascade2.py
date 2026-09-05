"""Continue the exact x-column descent, imposing perfect-power gates (unconditional).
Tracks: gates, their factor structure, and the denominator ledger."""
import sympy as sp, pickle, sys
from sympy import Rational as R
y=sp.Symbol('y'); al,be,r=sp.symbols('alpha beta r')
NP=[(0,0),(1,0),(8,14),(8,16),(0,8)]; NQ=[(0,0),(2,1),(12,21),(12,24),(0,12)]
def bounds(v,imax):
    lo,hi={},{}
    for i in range(imax+1):
        pts=[]
        for t in range(len(v)):
            (x1,y1),(x2,y2)=v[t],v[(t+1)%len(v)]
            if x1==x2==i: pts+=[y1,y2]
            elif (x1-i)*(x2-i)<=0 and x1!=x2: pts.append(y1+R(y2-y1,x2-x1)*(i-x1))
        lo[i]=int(sp.ceiling(min(pts))); hi[i]=int(sp.floor(max(pts)))
    return lo,hi
loP,hiP=bounds(NP,8); loQ,hiQ=bounds(NQ,12); loP[0]=max(loP[0],1); loQ[0]=max(loQ[0],1)
W=y**7*(y-r)
a={i:sum(sp.Symbol(f'a{i}_{j}')*y**j for j in range(loP[i],hiP[i]+1)) for i in range(9)}
b={k:sum(sp.Symbol(f'b{k}_{j}')*y**j for j in range(loQ[k],hiQ[k]+1)) for k in range(13)}
a[8]=sp.expand(al*W**2); b[12]=sp.expand(be*W**3)
NONZERO={al,be,r}
def rung(d,sub):
    e=0
    for i in range(9):
        k=d+1-i
        if 0<=k<=12: e+= i*a[i]*sp.diff(b[k],y)-k*sp.diff(a[i],y)*b[k]
    e=sp.expand(sp.expand(e).subs(sub)-(1 if d==2 else 0))
    return [] if e==0 else [c for c in sp.Poly(e,y).all_coeffs() if c!=0]
def strip(g):
    """remove factors forced nonzero; return list of (factor, multiplicity) that must vanish"""
    g=sp.factor(sp.together(g)); n,dd=sp.fraction(g)
    out=[]
    for f,m in sp.factor_list(sp.expand(n))[1]:
        if f.is_number or f in NONZERO: continue
        out.append((f,m))
    return out
sub={}; log=[]; denoms=set(); free_params=[]
for d in range(18,6,-1):
    new=[]
    i0,k0=d-11,d-7
    if 0<=i0<=8: new+=[sp.Symbol(f'a{i0}_{j}') for j in range(loP[i0],hiP[i0]+1)]
    if 0<=k0<=12: new+=[sp.Symbol(f'b{k0}_{j}') for j in range(loQ[k0],hiQ[k0]+1)]
    new=[n for n in new if n not in sub]
    cs=rung(d,sub)
    if not cs: print(f"d={d}: vacuous",flush=True); continue
    imposed=[]; branch=False
    for it in range(12):
        cs=rung(d,sub)
        new=[n for n in new if n not in sub]
        if not cs: break
        M=sp.zeros(len(cs),len(new)); v=sp.zeros(len(cs),1)
        for ii,c in enumerate(cs):
            p=sp.expand(c)
            for jj,nv in enumerate(new): M[ii,jj]=sp.expand(sp.diff(p,nv))
            v[ii,0]=sp.expand(p.subs({nv:0 for nv in new}))
        ns=M.T.nullspace()
        gates=[sp.factor(sp.expand((n.T*v)[0,0])) for n in ns]; gates=[g for g in gates if g!=0]
        if not gates: break
        prog=False
        for g in gates:
            fs=strip(g)
            if len(fs)==1:
                f=fs[0][0]; vs=[x for x in f.free_symbols if x not in NONZERO]
                if not vs: print(f"d={d}: gate has no free var -> EMPTY on this chart: {f}",flush=True); branch=True; break
                s1=sp.solve(f,vs[0],dict=True)
                if s1:
                    sub[vs[0]]=sp.simplify(s1[0][vs[0]])
                    for den in sp.denom(sp.together(sub[vs[0]])).free_symbols: denoms.add(str(den))
                    sub={k_:sp.simplify(sp.expand(v_).subs(sub)) for k_,v_ in sub.items()}
                    imposed.append(f); prog=True; break
            elif len(fs)>1:
                print(f"d={d}: REDUCIBLE gate (BRANCH): {[str(f) for f,_ in fs]}",flush=True); branch=True; break
        if branch or not prog: break
    if branch: log.append((d,'branch',None)); break
    print(f"d={d}: imposed {len(imposed)} forced gate(s)",flush=True)
    for f in imposed: print("      FORCED:",f,flush=True)
    cs=rung(d,sub); new=[n for n in new if n not in sub]
    s=sp.solve(cs,new,dict=True) if (cs and new) else [{}]
    if not s: print(f"d={d}: STUCK"); log.append((d,'stuck',cs)); break
    for k_,v_ in s[0].items():
        for den in sp.denom(sp.together(v_)).free_symbols: denoms.add(str(den))
        sub[k_]=sp.simplify(v_)
    sub={k_:sp.simplify(sp.expand(v_).subs(sub)) for k_,v_ in sub.items()}
    res=rung(d,sub); fr=[n for n in new if n not in sub]; free_params+=fr
    print(f"d={d}: solved {len(s[0])}, free {len(fr)}, residual {len(res)}",flush=True)
    log.append((d,'ok',imposed))
print("\nDENOMINATORS:",sorted(denoms))
pickle.dump((sub,log,free_params),open('cascade.pkl','wb'))
