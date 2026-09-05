"""SUB-CASE (2): exact mod-p ladder WITH GATE SOLVING, rungs 2 -> 19.

At each rung the system M u = v may be inconsistent; the inconsistent rows are
the GATES, and they are functions of the free parameters chosen at earlier
rungs.  Rather than randomising blindly (which explores a variety that does not
exist) we SOLVE each gate for one free parameter:

  - re-run the ladder with that parameter set to several values,
  - interpolate the gate as a polynomial in it,
  - take a root mod p, fix the parameter, continue.

Everything is integers mod p, so "consistent" and "zero" are exact.
Question: does a point survive to rung 19 with all four vertices nonzero?
"""
import random, math, sys
from fractions import Fraction as F
P=(1<<31)-1   # Mersenne, = 3 mod 4 so square roots are cheap
def inv(a): return pow(a%P,P-2,P)
NP=[(0,0),(1,0),(8,14),(8,16)]; NQ=[(0,0),(2,1),(12,21),(12,24)]
def bounds(v,imax):
    lo,hi={},{}
    for i in range(imax+1):
        pts=[]
        for t in range(len(v)):
            (x1,y1),(x2,y2)=v[t],v[(t+1)%len(v)]
            if x1==x2==i: pts+=[y1,y2]
            elif (x1-i)*(x2-i)<=0 and x1!=x2: pts.append(y1+F(y2-y1,x2-x1)*(i-x1))
        if not pts: lo[i]=hi[i]=None; continue
        lo[i]=int(math.ceil(min(pts))); hi[i]=int(math.floor(max(pts)))
    return lo,hi
loP,hiP=bounds(NP,8); loQ,hiQ=bounds(NQ,12)
loP[0]=max(loP[0],1); loQ[0]=max(loQ[0],1)
def rg(lo,hi): return [] if lo is None or lo>hi else list(range(lo,hi+1))
AR={i:rg(loP[i],hiP[i]) for i in range(9)}; BR={k:rg(loQ[k],hiQ[k]) for k in range(13)}

def terms(A,B,d,skipA=None,skipB=None):
    acc={}
    for i in range(9):
        k=d+1-i
        if not (0<=k<=12): continue
        if (skipA is not None and i==skipA) or (skipB is not None and k==skipB): continue
        for ca,xa in zip(A[i],AR[i]):
            if ca==0: continue
            for cb,xb in zip(B[k],BR[k]):
                if cb==0: continue
                if xb: e=xa+xb-1; acc[e]=(acc.get(e,0)+i*ca*cb%P*xb)%P
                if xa: e=xa-1+xb; acc[e]=(acc.get(e,0)-k*ca*cb%P*xa)%P
    return acc

def rref(M,v):
    nr=len(M); nc=len(M[0]) if nr else 0
    Aug=[M[i][:]+[v[i]] for i in range(nr)]
    piv=[]; r=0
    for c in range(nc):
        pr=None
        for i in range(r,nr):
            if Aug[i][c]%P: pr=i;break
        if pr is None: continue
        Aug[r],Aug[pr]=Aug[pr],Aug[r]
        iv=inv(Aug[r][c]); Aug[r]=[x*iv%P for x in Aug[r]]
        for i in range(nr):
            if i!=r and Aug[i][c]%P:
                f=Aug[i][c]; Aug[i]=[(Aug[i][j]-f*Aug[r][j])%P for j in range(nc+1)]
        piv.append(c); r+=1
    gates=[Aug[i][nc]%P for i in range(r,nr) if all(Aug[i][j]%P==0 for j in range(nc))]
    part=[0]*nc
    for i,c in enumerate(piv): part[c]=Aug[i][nc]%P
    free=[c for c in range(nc) if c not in piv]
    ns=[]
    for fc in free:
        vec=[0]*nc; vec[fc]=1
        for i,c in enumerate(piv): vec[c]=(-Aug[i][fc])%P
        ns.append(vec)
    return part,ns,gates

def build(d,A,B):
    ia=d-1 if 0<=d-1<=8 else None; kb=d if 0<=d<=12 else None
    unk=[]
    if ia is not None: unk+=[('a',ia,j) for j in range(len(AR[ia]))]
    if kb is not None: unk+=[('b',kb,j) for j in range(len(BR[kb]))]
    known=terms(A,B,d,skipA=ia,skipB=kb)
    cols={}
    for ui,(typ,idx,j) in enumerate(unk):
        if typ=='a':
            i=idx; k=d+1-i
            if not (0<=k<=12): continue
            xa=AR[i][j]
            for cb,xb in zip(B[k],BR[k]):
                if cb==0: continue
                if xb: e=xa+xb-1; cols.setdefault(e,{}); cols[e][ui]=(cols[e].get(ui,0)+i*cb%P*xb)%P
                if xa: e=xa-1+xb; cols.setdefault(e,{}); cols[e][ui]=(cols[e].get(ui,0)-k*cb%P*xa)%P
        else:
            k=idx; i=d+1-k
            if not (0<=i<=8): continue
            xb=BR[k][j]
            for ca,xa in zip(A[i],AR[i]):
                if ca==0: continue
                if xb: e=xa+xb-1; cols.setdefault(e,{}); cols[e][ui]=(cols[e].get(ui,0)+i*ca%P*xb)%P
                if xa: e=xa-1+xb; cols.setdefault(e,{}); cols[e][ui]=(cols[e].get(ui,0)-k*ca%P*xa)%P
    exps=sorted(set(list(cols)+list(known)))
    M=[[cols.get(e,{}).get(ui,0) for ui in range(len(unk))] for e in exps]
    v=[(-known.get(e,0))%P for e in exps]
    return unk,M,v

def ladder(tvals, upto, seed=0):
    """tvals: list of chosen free-parameter values (consumed in order).
       returns (A,B,gates_at_upto, n_consumed) ; gates_at_upto = list of gate values"""
    rnd=random.Random(seed)
    A={i:[0]*len(AR[i]) for i in range(9)}; B={k:[0]*len(BR[k]) for k in range(13)}
    Av=tvals[0]; Bv=tvals[1]; ptr=2
    for idx,e in enumerate(AR[1]): A[1][idx]= Av if e==0 else (2*Av*Av%P*Bv%P if e==1 else 0)
    for idx,e in enumerate(BR[2]): B[2][idx]= inv(Av) if e==1 else (Bv if e==2 else 0)
    for d in range(3,upto+1):
        unk,M,v=build(d,A,B)
        if not unk:
            acc=terms(A,B,d)
            return A,B,[c%P for c in acc.values() if c%P],ptr
        part,ns,gates=rref(M,v)
        if any(g%P for g in gates):
            return A,B,[g%P for g in gates if g%P],ptr
        sol=part[:]
        for vec in ns:
            t = tvals[ptr] if ptr<len(tvals) else rnd.randrange(1,P)
            ptr+=1
            sol=[(sol[i]+t*vec[i])%P for i in range(len(sol))]
        for ui,(typ,idx,j) in enumerate(unk):
            if typ=='a': A[idx][j]=sol[ui]
            else: B[idx][j]=sol[ui]
    return A,B,[],ptr


def pmul(a,b,f):
    r=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b): r[i+j]=(r[i+j]+x*y)%P
    return pmod(r,f)
def pmod(a,f):
    a=a[:]
    df=len(f)-1; iv=inv(f[-1])
    while len(a)-1>=df and len(a)>1:
        while a and a[-1]%P==0: a.pop()
        if len(a)-1<df: break
        c=a[-1]*iv%P; sh=len(a)-1-df
        for i in range(len(f)): a[sh+i]=(a[sh+i]-c*f[i])%P
        while a and a[-1]%P==0: a.pop()
    return a if a else [0]
def pgcd(a,b):
    a=a[:];b=b[:]
    while True:
        while b and b[-1]%P==0: b.pop()
        if not b or (len(b)==1 and b[0]%P==0): break
        a=pmod(a,b); a,b=b,a
    while a and a[-1]%P==0: a.pop()
    return a if a else [0]
def ppow(base,e,f):
    r=[1]; b=pmod(base,f)
    while e:
        if e&1: r=pmul(r,b,f)
        b=pmul(b,b,f); e>>=1
    return r
def roots_mod(c):
    """all roots in F_P of the poly with coeff list c (ascending)"""
    while len(c)>1 and c[-1]%P==0: c.pop()
    if len(c)<=1: return []
    if len(c)==2: return [(-c[0]*inv(c[1]))%P]
    # g = gcd(x^P - x, c) = product of distinct linear factors
    xp=ppow([0,1],P,c)
    sub=xp[:]+[0]*max(0,2-len(xp))
    sub=[(sub[i]-(1 if i==1 else 0))%P for i in range(max(len(xp),2))]
    g=pgcd(c[:],sub)
    if len(g)<=1: return []
    out=[]
    def split(h):
        while len(h)>1 and h[-1]%P==0: h.pop()
        if len(h)<=1: return
        if len(h)==2: out.append((-h[0]*inv(h[1]))%P); return
        for _ in range(60):
            a=random.randrange(0,P)
            t=ppow([a,1],(P-1)//2,h)
            t=[(t[i]-(1 if i==0 else 0))%P for i in range(max(len(t),1))]
            d=pgcd(h[:],t)
            while len(d)>1 and d[-1]%P==0: d.pop()
            if 1<len(d)<len(h):
                q=h[:]
                # divide h by d
                num=h[:]; den=d[:]; quo=[0]*(len(num)-len(den)+1); ivd=inv(den[-1])
                while len(num)>=len(den) and any(num):
                    while num and num[-1]%P==0: num.pop()
                    if len(num)<len(den): break
                    cc=num[-1]*ivd%P; sh=len(num)-len(den)
                    quo[sh]=cc
                    for i in range(len(den)): num[sh+i]=(num[sh+i]-cc*den[i])%P
                    while num and num[-1]%P==0: num.pop()
                split(d); split(quo); return
        return
    split(g)
    return sorted(set(out))

def poly_roots(pts):
    """Lagrange-interpolate through (x,y) mod P and return roots by brute search
       over the interpolation degree using resultant-free factoring for deg<=4."""
    n=len(pts)
    # Newton divided differences -> coefficients
    xs=[x for x,_ in pts]; ys=[y for _,y in pts]
    coef=ys[:]
    for j in range(1,n):
        for i in range(n-1,j-1,-1):
            coef[i]=(coef[i]-coef[i-1])*inv((xs[i]-xs[i-j])%P)%P
    # expand to standard basis
    c=[0]*n; c[0]=coef[n-1]
    for k in range(n-2,-1,-1):
        new=[0]*n
        for i in range(n-1): new[i+1]=(new[i+1]+c[i])%P
        for i in range(n): new[i]=(new[i]-xs[k]*c[i])%P
        new[0]=(new[0]+coef[k])%P
        c=new
    while len(c)>1 and c[-1]%P==0: c.pop()
    deg=len(c)-1
    if deg<=0: return [],deg
    rr=roots_mod(c[:])
    return (rr if rr else None), deg

if __name__=='__main__':
    seed=int(sys.argv[1]) if len(sys.argv)>1 else 1
    rnd=random.Random(seed)
    tvals=[rnd.randrange(1,P) for _ in range(60)]
    spent=set()
    print("mod-p ladder with gate solving (exact arithmetic)\n")
    d=3
    while d<=19:
        A,B,gates,used=ladder(tvals,d,seed)
        if not gates:
            print(f"  rung {d}: CONSISTENT   (free params consumed: {used})")
            d+=1; continue
        solved=False
        for k in range(used-1,1,-1):
            if k in spent: continue
            pts=[]
            for xv in [1,2,3,4,5,6,7,8]:
                tt=tvals[:]; tt[k]=xv
                _,_,g2,_=ladder(tt,d,seed)
                pts.append((xv,(g2[0]%P) if g2 else 0))
            root,deg=poly_roots(pts)
            if deg<=0: continue          # gate does not depend on this parameter
            if root is None:
                print(f"  rung {d}: gate has degree {deg} in param #{k} -- needs factoring")
                continue
            tvals[k]=root[0]
            A,B,g3,_=ladder(tvals,d,seed)
            if not g3:
                spent.add(k)
                print(f"  rung {d}: GATE solved for param #{k} (degree {deg}) -> CONSISTENT")
                solved=True; break
        if not solved:
            print(f"  rung {d}: could not clear the gate with any unspent parameter -> STOP")
            break
        d+=1
    reached=min(d,19)
    print(f"\n=== FINAL STATE: reached rung {reached} ===")
    A,B,gates,used=ladder(tvals,reached,seed)
    print(f"  outstanding gates: {len(gates)}   parameters spent on gates: {sorted(spent)}")
    for nm,val in [("p_14_8 = a8_14",A[8][0]),("p_16_8 = a8_16",A[8][-1]),
                   ("q_21_12 = b12_21",B[12][0]),("q_24_12 = b12_24",B[12][-1])]:
        print(f"  {nm:20s} = {'NONZERO' if val%P else 'ZERO'}")
