"""T4 applied: the lift pipeline run over every real mod-p point this session
produced, plus the status of the H2 queue's LIVE/TIMEOUT targets."""
import ast, json, os, sys
import sympy as sp
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
sys.path.insert(0,HERE); sys.path.insert(0,os.path.join(ROOT,'wave4'))
import lift_pipeline as LP
import w4_c2_reduce as RED, w4_c2_residual as RS

print("="*78); print("T4 -- LIFT PIPELINE, controls then real targets"); print("="*78)
res={"controls":[],"targets":[]}
allok=True
for n,o,note in LP.controls():
    allok &= o
    res["controls"].append([n,bool(o),note])
    print(f"    [{'PASS' if o else 'FAIL'}] {n}   {note}")

print("\n  TARGET 1 -- the case-(2) w=-4 mod-p points (chart d_3_3=1, gauge d_2_1=1)")
polysQ, gsyms = RED.reduced_polys_Q()
names=[str(s) for s in gsyms]
i3=names.index('d_3_3'); i2=names.index('d_2_1')
sysQ = list(polysQ) + [gsyms[i3]-1, gsyms[i2]-1]
print(f"    system over Q: {len(sysQ)} generators in {len(gsyms)} variables")
OUT=os.path.join(ROOT,'wave4','artifacts')
for p in (1000003,1000033,1000039):
    f=os.path.join(OUT,f"casc_w4_real_one_p{p}.out")
    if not os.path.exists(f) or os.path.getsize(f)==0:
        print(f"    p={p}: no RUR artifact yet ({f}) -- skipped"); continue
    rur=RS.parse_rur(f)
    vals,_=RS.rur_values(rur)
    sign=None
    for s in (1,-1):
        ok,_=RS.verify_rur(vals,s,rur,p,chart='one',gauge=RS.GAUGE_BY_CHART['one'])
        if ok: sign=s; break
    if sign is None:
        print(f"    p={p}: RUR sign undetermined -- skipped"); continue
    w=sp.Symbol('w'); fpoly=sum(c*w**i for i,c in enumerate(rur['elim']))
    roots=[int(r)%p for r in sp.ground_roots(sp.Poly(fpoly,w,modulus=p,symmetric=False))]
    print(f"    p={p}: eliminant degree {rur['deg']}, {len(roots)} F_p-rational root(s)")
    for r in roots:
        pt=[]
        for v in names:
            cs=vals[v]
            a=0
            for c in reversed(cs): a=(a*r+c)%p
            pt.append((sign*a)%p)
        chk=[int(sp.Integer(sp.expand(g.subs({gsyms[i]:sp.Integer(pt[i]) for i in range(len(names))}))))%p for g in sysQ]
        if any(chk):
            print(f"      root {r}: NOT a mod-p root of the exact system -- skipped "
                  f"({sum(1 for v in chk if v)} generators nonzero)")
            continue
        rec=LP.pipeline(sysQ, gsyms, pt, p, K=8)
        rec.update(target="case2_w4_chart_one", root=r)
        res["targets"].append(rec)
        print(f"      root {r}: {rec['status']}  ({rec.get('lift_note','')[:60]})")
        if rec['status']=='VERIFIED-RATIONAL-POINT':
            print(f"      *** CANDIDATE-UNVERIFIED: exact rational point "
                  f"{rec['rational_point']}")

print("\n  TARGET 2 -- the H2 (Track D) queue")
st=json.load(open(os.path.join(ROOT,'h2','h2_state.json')))
import collections
c=collections.Counter(v['verdict'] for v in st.values())
print(f"    verdicts on record: {dict(c)}")
live=[k for k,v in st.items() if v['verdict'] in ('LIVE','DISAGREE')]
print(f"    LIVE/DISAGREE targets with a mod-p point to lift: {len(live)}")
res["h2_queue"]={"verdicts":dict(c),"live":live,
                 "note":"the lift stage needs a mod-p SOLUTION; EMPTY and TIMEOUT "
                        "targets produce none, so there is nothing to lift yet"}
json.dump(res, open(os.path.join(HERE,'lift_results.json'),'w'), indent=1)
print("\n"+"="*78)
print(f"    controls: {sum(1 for _,o,_ in res['controls'] if o)}/{len(res['controls'])} passed")
print("="*78)
