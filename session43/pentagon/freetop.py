#!/usr/bin/env python3
"""Same bilinear rank test, but with the CHOSEN top data set free.

Only h_8 = c0 (s-tau)^8 is theorem-backed (the eighth-power theorem), and c0
and tau are normalisations, so h_8 = z^8 is genuinely without loss.  h_7 = 2z^8
and h_6 = z^8 were a CHOICE -- one point of branch 1, which verify_descent.py
already flagged as "ONE POINT of branch 1, not the generic branch".  g_12 =
z^12 likewise.

So free them and re-run the count.  The bracket is bilinear in the coefficients
of P and of Q, so freeing h_6, h_7 just enlarges the h-block and freeing g_12
just enlarges the g-block; the system stays LINEAR in g for fixed h and the
rank test still applies.

What matters is dim leftker(M) = (#equations - rank M), the number of
conditions that fall on the h-block alone, versus the size of the h-block.
NOT the rank defect, which is at most 1 by construction and says nothing.
"""
import sympy as sp, random
Pm=(1<<31)-1
z=sp.Symbol('z'); TAU=sp.Integer(1); s=z+TAU
def hsup(a):
    return [i for i in range(9) if 0 <= i+a <= 16 and max(0,(i+a)-8) <= i <= min(8,(i+a)//2+1)]
def gsup(b):
    return [k for k in range(13) if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]
def run(tag, free_h67, free_g12):
    H={8:z**8, -1:sp.expand(s)}; G={-1:sp.expand(s**2)}
    hv,gv=[],[]
    rng=range(0,8) if free_h67 else range(0,6)
    if not free_h67: H[7]=2*z**8; H[6]=z**8
    for a in rng:
        S=[sp.Symbol(f'h{a}_{i}') for i in hsup(a)]; hv+=S
        H[a]=sum(x*z**i for x,i in zip(S,hsup(a)))
    grng=range(0,13) if free_g12 else range(0,12)
    if not free_g12: G[12]=z**12
    for b in grng:
        S=[sp.Symbol(f'g{b}_{k}') for k in gsup(b)]; gv+=S
        G[b]=sum(x*z**k for x,k in zip(S,gsup(b)))
    eqs=[]
    for L in range(20,-3,-1):
        e=0
        for a in range(-1,9):
            b=L-a
            if a in H and b in G: e += b*sp.diff(H[a],z)*G[b] - a*H[a]*sp.diff(G[b],z)
        e=sp.expand(e-(s**2 if L==-2 else 0))
        if e==0: continue
        eqs+=[sp.expand(c) for c in sp.Poly(e,z).all_coeffs() if c!=0]
    Peq=[sp.Poly(e,*gv) for e in eqs]
    def rank_modp(rows,nc):
        rows=[r[:] for r in rows]; r=0
        for c in range(nc):
            piv=None
            for i in range(r,len(rows)):
                if rows[i][c]%Pm: piv=i;break
            if piv is None: continue
            rows[r],rows[piv]=rows[piv],rows[r]
            inv=pow(rows[r][c],Pm-2,Pm)
            rows[r]=[(x*inv)%Pm for x in rows[r]]
            for i in range(len(rows)):
                if i!=r and rows[i][c]%Pm:
                    f=rows[i][c]; rows[i]=[(a-f*b)%Pm for a,b in zip(rows[i],rows[r])]
            r+=1
            if r==len(rows): break
        return r
    hval={x:sp.Integer(random.randrange(1,Pm)) for x in hv}
    M,vv=[],[]
    for p in Peq:
        row=[0]*len(gv); const=0
        for mon,co in p.terms():
            c=int(sp.Integer(sp.expand(co.subs(hval)))%Pm) if co.free_symbols else int(co)%Pm
            nz=[j for j,e in enumerate(mon) if e]
            if not nz: const=(const+c)%Pm
            else:
                assert len(nz)==1 and mon[nz[0]]==1
                row[nz[0]]=(row[nz[0]]+c)%Pm
        M.append(row); vv.append((-const)%Pm)
    # control first (erratum A15)
    g0=[random.randrange(Pm) for _ in gv]
    vp=[sum(a*b for a,b in zip(r,g0))%Pm for r in M]
    rM=rank_modp(M,len(gv))
    rc=rank_modp([r+[t] for r,t in zip(M,vp)],len(gv)+1)
    assert rc==rM, f"{tag}: PLANTED CONTROL FAILED"
    rA=rank_modp([r+[t] for r,t in zip(M,vv)],len(gv)+1)
    nc=len(eqs)-rM
    print(f"{tag}: eqs={len(eqs)} h-block={len(hv)} g-block={len(gv)} rank(M)={rM}")
    print(f"    control PASS | conditions on h = eqs - rank(M) = {nc}"
          f" vs h-block {len(hv)}  -> expected dim {len(hv)-nc}"
          f"  [{'CONSISTENT' if rA==rM else 'inconsistent at this h'}]", flush=True)
random.seed(7)
run("witness fixed (h_7=2z^8, h_6=z^8, g_12=z^12)", False, False)
run("h_6,h_7 FREE                                ", True,  False)
run("h_6,h_7 and g_12 all FREE                   ", True,  True)
