#!/usr/bin/env python3
"""The decisive cheap test, using bilinearity.

The pentagon is BILINEAR: split the unknowns into the h-block (33) and the
g-block (109).  For a FIXED h the 261 equations are LINEAR in g:

        M(h) . g = v(h),      M is 261 x 109.

So for any particular h, solvability is not a Groebner question at all -- it is
rank[M|v] == rank[M], pure linear algebra, milliseconds.  And when it holds,
solving the system HANDS BACK an explicit g, hence an explicit (P,Q).

Run over F_p with random h.  Two possible outcomes and both are informative:
  * consistent  -> an explicit solution exists at that h; lift and verify.
  * inconsistent-> the solvable h form a proper subvariety, and the RANK DEFECT
                   rank[M|v] - rank[M] measures how far off a generic h is,
                   which bounds how many conditions the h-locus must satisfy.

Erratum A15 discipline: the planted control runs FIRST, not after.  Last time a
search was run over 3000 points and only then was the control tried -- and the
control failed, invalidating everything.  Here the control is a planted
consistent system built from the same matrix.
"""
import sympy as sp, random, sys
P = (1 << 31) - 1
z = sp.Symbol('z'); TAU = sp.Integer(1); s = z + TAU
def hsup(a):
    return [i for i in range(9) if 0 <= i+a <= 16 and max(0,(i+a)-8) <= i <= min(8,(i+a)//2+1)]
def gsup(b):
    return [k for k in range(13) if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]
H = {8: z**8, 7: 2*z**8, 6: z**8, -1: sp.expand(s)}
G = {12: z**12, -1: sp.expand(s**2)}
hv, gv = [], []
for a in range(0,6):
    S=[sp.Symbol(f'h{a}_{i}') for i in hsup(a)]; hv+=S
    H[a]=sum(x*z**i for x,i in zip(S,hsup(a)))
for b in range(0,12):
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
    eqs += [sp.expand(c) for c in sp.Poly(e,z).all_coeffs() if c!=0]
print(f"{len(eqs)} equations, h-block {len(hv)}, g-block {len(gv)}", flush=True)

def rank_modp(rows, ncols):
    """Gaussian elimination mod P; returns rank.  rows are lists of ints."""
    rows=[r[:] for r in rows]; r=0
    for c in range(ncols):
        piv=None
        for i in range(r,len(rows)):
            if rows[i][c]%P: piv=i; break
        if piv is None: continue
        rows[r],rows[piv]=rows[piv],rows[r]
        inv=pow(rows[r][c],P-2,P)
        rows[r]=[(x*inv)%P for x in rows[r]]
        for i in range(len(rows)):
            if i!=r and rows[i][c]%P:
                f=rows[i][c]; rows[i]=[(a-f*b)%P for a,b in zip(rows[i],rows[r])]
        r+=1
        if r==len(rows): break
    return r

# pre-split each equation into its g-linear part once
Peq=[sp.Poly(e,*gv) for e in eqs]
def build(hval):
    M,vv=[],[]
    for p in Peq:
        row=[0]*len(gv); const=0
        for mon,co in p.terms():
            c=int(sp.Integer(sp.expand(co.subs(hval))) % P) if co.free_symbols else int(co)%P
            nz=[j for j,e in enumerate(mon) if e]
            if not nz: const=(const+c)%P
            else:
                assert len(nz)==1 and mon[nz[0]]==1, "not linear in g"
                row[nz[0]]=(row[nz[0]]+c)%P
        M.append(row); vv.append((-const)%P)
    return M,vv

random.seed(20260823)
def trial(tag, hval, force_consistent=False):
    M,vv=build(hval)
    if force_consistent:
        g0=[random.randrange(P) for _ in gv]
        vv=[sum(a*b for a,b in zip(row,g0))%P for row in M]
    rM=rank_modp(M,len(gv))
    rA=rank_modp([row+[t] for row,t in zip(M,vv)],len(gv)+1)
    print(f"{tag}: rank(M)={rM}  rank[M|v]={rA}  defect={rA-rM}  "
          f"{'CONSISTENT' if rA==rM else 'inconsistent'}", flush=True)
    return rA==rM

hval={x: sp.Integer(random.randrange(1,P)) for x in hv}
print("--- CONTROL FIRST (erratum A15): planted consistent RHS on the same M ---")
ok=trial("planted", hval, force_consistent=True)
assert ok, "PLANTED CONTROL FAILED -- rank test is broken, results below are void"
print("--- control passed; now the real right-hand side ---")
for t in range(3):
    hval={x: sp.Integer(random.randrange(1,P)) for x in hv}
    trial(f"random h #{t}", hval)
