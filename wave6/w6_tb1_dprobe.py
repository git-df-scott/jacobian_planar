# Same variable-projection test, but eliminating the d-block (110 unknowns)
# instead of the c-block (51). NOT symmetric: more unknowns against the same
# 283 equations, so this is the direction with the best chance of consistency.
# A consistent probe here yields a full point and is an immediate NONEMPTY.
import sys, random
sys.path.insert(0,'/home/user/jacobian_planar/wave6')
from w6_tb1_rank import load, parse_poly, evalmono, rank_modp, SRC
from collections import defaultdict

vs,p,body = load(SRC)
D  = sorted(v for v in vs if v.startswith('d_'))
OTH= sorted(v for v in vs if not v.startswith('d_'))
dset=set(D)
polys=[parse_poly(b,p) for b in body]
lin=[]
for i,poly in enumerate(polys):
    dg=max((sum(e for v,e in m if v in dset) for m in poly), default=0)
    if dg<=1: lin.append(i)
print(f"d-block width {len(D)}, other {len(OTH)}; {len(lin)}/{len(body)} equations affine-linear in d")
didx={v:j for j,v in enumerate(D)}; nc=len(D)
rng=random.Random(777)
for t in range(8):
    pt={v: rng.randrange(1,p) for v in OTH}
    rows=[]
    for i in lin:
        row=[0]*(nc+1)
        for m,co in polys[i].items():
            dv=[v for v,e in m if v in dset]
            rest=tuple((v,e) for v,e in m if v not in dset)
            val=co*evalmono(rest,pt,p)%p
            if dv: row[didx[dv[0]]]=(row[didx[dv[0]]]+val)%p
            else:  row[nc]=(row[nc]-val)%p
        rows.append(row)
    rA,_   = rank_modp([r[:nc] for r in rows], nc, p)
    rAug,_ = rank_modp(rows, nc+1, p)
    print(f"  probe {t+1}: rank M = {rA}/{nc}, rank[M|n] = {rAug} -> "
          f"{'CONSISTENT *** HIT ***' if rA==rAug else 'inconsistent'}", flush=True)
